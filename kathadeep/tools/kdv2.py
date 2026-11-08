"""Katha Deep edit grammar v2 (retention editing).

Research-driven changes over v1 (see STUDIO.md 'Edit grammar v2'):
  * 2.5D parallax on every painting / render: a monocular depth map (Depth-Anything-V2-Small) drives a
    per-pixel shift so near layers move more than far ones while the camera travels.
  * Shot rhythm: one painting is covered in several 1.2-2.6 s shots (wide -> medium -> close-up on the
    subject, which is found from the depth map), cut on the spoken word, each with its own move.
  * Speed-ramped moves: a fast push in the first ~0.35 s, then a slow drift.
  * Transitions chosen by meaning: hard cut by default; zoom-punch, flash, whip, iris only where marked.
"""
import math
import os
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image

import kd
from kd import W, H, Scene

KD = kd.KD
_pipe = None


def _depth_model():
    global _pipe
    if _pipe is None:
        from transformers import pipeline
        _pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=-1)
    return _pipe


@lru_cache(64)
def load_pair(path, maxside=2400):
    """(rgb float32 HxWx3, depth float32 HxW in 0..1, 1 = near) with an on-disk depth cache."""
    rgb = kd.load_rgb(path, maxside)
    cache = f"{KD}/depth/{os.path.basename(path)}.{rgb.width}x{rgb.height}.npy"
    if os.path.exists(cache):
        d = np.load(cache)
    else:
        small = rgb.copy()
        small.thumbnail((1100, 1100))
        pd = _depth_model()(small)["predicted_depth"].squeeze().numpy().astype(np.float32)
        pd = (pd - pd.min()) / (pd.max() - pd.min() + 1e-6)
        d = cv2.resize(pd, (rgb.width, rgb.height), interpolation=cv2.INTER_CUBIC)
        d = cv2.GaussianBlur(d, (0, 0), 3)
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        np.save(cache, d)
    return np.asarray(rgb).astype(np.float32), d


def subject_point(path, rect):
    """Where a close-up should land: inside the central 70% of rect, score = nearness^2 x local detail
    (so paper margins, printed captions and blank walls lose to faces, hands and props)."""
    rgb, d = load_pair(path)
    x0, y0, x1, y1 = (int(v) for v in rect)
    mx, my = int((x1 - x0) * 0.15), int((y1 - y0) * 0.12)
    x0, x1, y0, y1 = x0 + mx, x1 - mx, y0 + my, y1 - my
    sub_d = d[y0:y1, x0:x1]
    if sub_d.size == 0:
        return 0.5, 0.5
    g = cv2.cvtColor(rgb[y0:y1, x0:x1].astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
    det = cv2.GaussianBlur(np.abs(cv2.Laplacian(g, cv2.CV_32F)), (0, 0), 9)
    yy = np.linspace(1.25, 0.75, sub_d.shape[0], dtype=np.float32)[:, None]   # faces usually sit high
    sc = (sub_d ** 2) * det * yy
    thr = np.quantile(sc, 0.90)
    ys, xs = np.nonzero(sc >= thr)
    h, w = d.shape
    return float((x0 + xs.mean()) / w), float((y0 + ys.mean()) / h)


def render_para(path, rect, out_wh, shift, dolly=0.0):
    """Crop rect (x0,y0,x1,y1 in source px) to out_wh with parallax.
    shift=(sx, sy): pixels that the NEAREST layer moves relative to the farthest; dolly: extra scale of near layers."""
    rgb, d = load_pair(path)
    ow, oh = out_wh
    x0, y0, x1, y1 = rect
    sx = (x1 - x0) / ow
    sy = (y1 - y0) / oh
    gx, gy = np.meshgrid(np.arange(ow, dtype=np.float32), np.arange(oh, dtype=np.float32))
    mapx = (x0 + gx * sx).astype(np.float32)
    mapy = (y0 + gy * sy).astype(np.float32)
    dep = cv2.remap(d, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    k = dep - 0.35
    cxs, cys = (x0 + x1) / 2, (y0 + y1) / 2
    mapx2 = (mapx - shift[0] * sx * k - (mapx - cxs) * dolly * k).astype(np.float32)
    mapy2 = (mapy - shift[1] * sy * k - (mapy - cys) * dolly * k).astype(np.float32)
    out = cv2.remap(rgb, mapx2, mapy2, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def ramp(x):
    """Fast push for the first ~25% then a slow drift (speed ramp)."""
    x = kd.clamp(x)
    return 0.55 * (1 - (1 - min(1, x / 0.25)) ** 3) + 0.45 * x


MOVES = {   # (shift_x, shift_y, dolly) at the end of the shot, start at the negated value
    "push": (0, 0, 0.10), "pull": (0, 0, -0.08), "left": (46, 0, 0.03), "right": (-46, 0, 0.03),
    "rise": (0, 40, 0.03), "fall": (0, -36, 0.03), "orbit": (40, 18, 0.06),
}


def _rect(src_wh, c, out_aspect):
    sw, sh = src_wh
    cx, cy, wf = c
    w = wf * sw
    h = w / out_aspect
    if h > sh:
        h = sh
        w = h * out_aspect
    x0 = kd.clamp(cx * sw - w / 2, 0, sw - w)
    y0 = kd.clamp(cy * sh - h / 2, 0, sh - h)
    return (x0, y0, x0 + w, y0 + h)


def BG_para(path, a, b, move="push", amp=1.0, out=(W, H), window=None):
    """Ken Burns a->b with a speed ramp and depth parallax. window: (x0,y0,x1,y1) to draw into a frame look."""
    rgb, _ = load_pair(path)
    sw, sh = rgb.shape[1], rgb.shape[0]
    ow, oh = (window[2] - window[0], window[3] - window[1]) if window else out
    mx, my, md = MOVES[move]

    def f(lt, fr, fi):
        e = ramp(fr)
        c = tuple(kd.lerp(a[i], b[i], e) for i in range(3))
        r = _rect((sw, sh), c, ow / oh)
        u = (e - 0.5) * 2
        img = render_para(path, r, (ow, oh), (mx * u * amp, my * u * amp), md * u * amp)
        if not window:
            return img
        base = kd.parchment("ivory").copy().convert("RGBA")
        from PIL import ImageDraw, ImageFilter
        sh_ = Image.new("RGBA", (W, H))
        ImageDraw.Draw(sh_).rectangle((window[0] + 10, window[1] + 16, window[2] + 10, window[3] + 16), fill=(60, 30, 10, 120))
        base.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(16)))
        base.paste(img, (window[0], window[1]))
        base.alpha_composite(kd.frame_overlay())
        return base.convert("RGB")
    f.meta = {"path": path, "a": a, "b": b, "window": window}
    return f


def coverage(path, base, t0, t1, cut_times, window=None, moves=("push", "left", "rise", "orbit", "right", "pull")):
    """Split [t0,t1) into shots at cut_times (and so no shot exceeds ~2.6 s); frame them wide / medium /
    close-on-subject, alternating moves. Returns [(s0, s1, bgfunc)]."""
    cuts = sorted(t for t in cut_times if t0 + 0.9 < t < t1 - 0.9)
    pts = [t0] + cuts + [t1]
    seg = []
    for s0, s1 in zip(pts[:-1], pts[1:]):
        n = max(1, int(round((s1 - s0) / 2.2)))
        for k in range(n):
            seg.append((s0 + (s1 - s0) * k / n, s0 + (s1 - s0) * (k + 1) / n))
    rgb, _ = load_pair(path)
    sw, sh = rgb.shape[1], rgb.shape[0]
    asp = ((window[2] - window[0]) / (window[3] - window[1])) if window else W / H
    cx, cy, wf = base
    fx, fy = subject_point(path, _rect((sw, sh), base, asp))
    framings = [(cx, cy, wf), ((cx + fx) / 2, (cy + fy) / 2, wf * 0.70), (fx, fy, wf * 0.46),
                (cx, cy, wf * 0.86), (fx, fy, wf * 0.58)]
    out = []
    for i, (s0, s1) in enumerate(seg):
        fa = framings[i % len(framings)]
        fb = (fa[0], fa[1], fa[2] * 0.92)
        out.append((s0, s1, BG_para(path, fa, fb, moves[i % len(moves)], window=window)))
    return out


def expand(scenes, cut_extra=None):
    """Replace every scene whose bg carries .meta (a painting or render) with parallax coverage shots.
    Inner cuts are hard cuts; the scene's own entry transition is kept on its first shot."""
    out = []
    for sc in scenes:
        meta = getattr(sc.bg, "meta", None)
        if not meta:
            out.append(sc)
            continue
        caps_t = [c[0] for c in sc.caps] + [c[4] for c in sc.caps if len(c) > 4 and c[4]]
        extra = (cut_extra or {}).get(sc.t0, [])
        shots = coverage(meta["path"], meta["b"], sc.t0, sc.t1, caps_t + extra, meta.get("window"))
        for j, (s0, s1, bg) in enumerate(shots):
            n = Scene(s0, s1, bg, sc.caps, sc.fx, sc.over, sc.credit, sc.grade_kind, sc.shake, sc.flash, sc.vig)
            n.trans = getattr(sc, "trans", None) if j == 0 else "cut"
            out.append(n)
    return out


def BG_auto(path, wf=0.75, move="push", focus=None, window=None):
    """One image, one shot: crop centred on the subject (or `focus`=(cx,cy)), gentle zoom with parallax."""
    rgb, _ = load_pair(path)
    sw, sh = rgb.shape[1], rgb.shape[0]
    asp = ((window[2] - window[0]) / (window[3] - window[1])) if window else W / H
    if focus is None:
        focus = subject_point(path, (0, 0, sw, sh))
    a = (focus[0], focus[1], wf)
    b = (focus[0], focus[1], wf * 0.86)
    return BG_para(path, a, b, move, window=window)


def keyword_shots(shots, t_end):
    """shots: [(t0, bgfunc, dict(caps=..., fx=..., over=..., trans=..., grade=..., shake=..., flash=..., credit=...))].
    Each shot runs until the next one starts. One image per spoken keyword."""
    out = []
    for i, (t0, bg, kw) in enumerate(shots):
        t1 = shots[i + 1][0] if i + 1 < len(shots) else t_end
        sc = Scene(t0, t1, bg, kw.get("caps", ()), kw.get("fx", ()), kw.get("over", ()), kw.get("credit"),
                   kw.get("grade", "warm"), kw.get("shake"), kw.get("flash"), kw.get("vig", True))
        sc.trans = kw.get("trans", "cut")
        out.append(sc)
    return out
