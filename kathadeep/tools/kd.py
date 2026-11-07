"""Katha Deep compositor engine (shared by every episode).

An episode's edit.py builds a list of Scene objects keyed to VO words, then calls render().
Visual language (matched to Deepotsav Din 1 / Dhanteras Special 2 & 3):
  - museum-art plates (The Met Open Access, CC0) with slow Ken Burns, warm grade, vignette, grain, embers
  - condensed all-caps Hinglish captions top-left: line 1 cream, line 2 gold/red, revealed on the spoken word
  - dark-red mandala plates for lists, shlokas and calls to action; gold-bordered chips
  - mono series tag top-right, mono art credit bottom-left
Output: raw RGB frames piped to ffmpeg -> silent 1080x1920 30 fps H.264.
"""
import math
import os
import random
import subprocess
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
KD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = {
    "anton": f"{KD}/fonts/Anton-Regular.ttf",
    "mono": f"{KD}/fonts/SpaceMono-Bold.ttf",
    "monor": f"{KD}/fonts/SpaceMono-Regular.ttf",
    "deva": f"{KD}/fonts/TiroDevanagariSanskrit-Regular.ttf",
    "devas": f"{KD}/fonts/NotoSerifDevanagari.ttf",
}
CREAM = (250, 242, 228)
GOLD = (245, 193, 72)
RED = (232, 72, 58)
DIM = (210, 190, 170)


# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ss(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def eo(x):
    return 1 - (1 - clamp(x)) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


# ------------------------------------------------------------------ timing from ElevenLabs alignment
class Timing:
    def __init__(self, proj):
        import json
        a = json.load(open(f"{proj}/vo/alignment.json"))
        self.text = "".join(a["characters"])
        self.st = a["character_start_times_seconds"]
        self.en = a["character_end_times_seconds"]
        self.end = self.en[-1]

    def at(self, phrase, n=0, end=False):
        """Start (or end) time of the n-th occurrence of phrase in the script."""
        i = -1
        for _ in range(n + 1):
            i = self.text.index(phrase, i + 1)
        return self.en[i + len(phrase) - 1] if end else self.st[i]


# ------------------------------------------------------------------ text
@lru_cache(None)
def font(k, s):
    return ImageFont.truetype(FONT[k], s, layout_engine=ImageFont.Layout.RAQM)


@lru_cache(4096)
def text_img(txt, fk, size, fill=CREAM, shadow=True, tracking=0):
    f = font(fk, size)
    l, t, r, b = f.getbbox(txt)
    pad = 30
    w, h = r - l + 2 * pad + tracking * len(txt), b - t + 2 * pad
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    if tracking:
        x = pad - l
        for ch in txt:
            d.text((x, pad - t), ch, font=f, fill=fill)
            x += f.getlength(ch) + tracking
    else:
        d.text((pad - l, pad - t), txt, font=f, fill=fill)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        a = im.split()[3].filter(ImageFilter.GaussianBlur(9))
        sh.putalpha(a.point(lambda v: int(v * 0.85)))
        out = Image.new("RGBA", (w + 6, h + 6))
        out.alpha_composite(sh, (5, 6))
        out.alpha_composite(im, (0, 0))
        im = out
    return im


def paste_fade(base, im, xy, alpha):
    if alpha <= 0.003:
        return
    if alpha < 0.997:
        im = im.copy()
        im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(xy[0]), int(xy[1])))


# ------------------------------------------------------------------ source images
@lru_cache(64)
def load_rgb(path, maxside=3200):
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bgc = Image.new("RGBA", im.size, (0, 0, 0, 255))
        bgc.alpha_composite(im)
        im = bgc
    im = im.convert("RGB")
    s = maxside / max(im.size)
    if s < 1:
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im


@lru_cache(32)
def load_rgba(path, maxside=2400):
    im = Image.open(path).convert("RGBA")
    s = maxside / max(im.size)
    if s < 1:
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im


def rect_from(src, cx, cy, wf):
    """9:16 crop rect centred at (cx,cy) (fractions of source) with width = wf * source width.
    Clamped inside the image; if 9:16 at that width overflows the height, width shrinks."""
    sw, sh = src.size
    w = wf * sw
    h = w * 16 / 9
    if h > sh:
        h = sh
        w = h * 9 / 16
    x0 = clamp(cx * sw - w / 2, 0, sw - w)
    y0 = clamp(cy * sh - h / 2, 0, sh - h)
    return (x0, y0, x0 + w, y0 + h)


def kb_frame(src, a, b, t):
    """Ken Burns: interpolate crop (cx,cy,wf) a->b with ease, return 1080x1920 RGB."""
    e = ss(t)
    cx, cy, wf = (lerp(a[i], b[i], e) for i in range(3))
    r = rect_from(src, cx, cy, wf)
    return src.transform((W, H), Image.EXTENT, r, Image.BICUBIC)


# ------------------------------------------------------------------ grading & texture
def grade(im, kind):
    if kind is None:
        return im
    a = np.asarray(im).astype(np.float32) / 255
    if kind == "warm":
        a = a * np.array([1.06, 0.97, 0.86]) + np.array([0.02, 0.0, -0.01])
    elif kind == "night":
        lum = a.mean(2, keepdims=True)
        a = a * 0.6 + lum * np.array([0.18, 0.26, 0.42]) * 1.2
        a = a * np.array([0.92, 0.98, 1.12])
    elif kind == "ember":
        lum = a.mean(2, keepdims=True)
        a = a * 0.55 + lum * np.array([0.62, 0.30, 0.16]) * 1.25
    elif kind == "teal":
        lum = a.mean(2, keepdims=True)
        a = a * 0.5 + lum * np.array([0.2, 0.42, 0.38]) * 1.3
    elif kind == "flame":   # tint bright highlights toward candle orange
        lum = a.mean(2, keepdims=True)
        w = np.clip((lum - 0.55) / 0.4, 0, 1)
        a = a * (1 - w) + (a * np.array([1.0, 0.72, 0.38]) + np.array([0.05, 0.02, 0])) * w
        a = a * np.array([1.04, 0.96, 0.88])
    elif kind == "dim":
        a = a * 0.55
    a = np.clip(a, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8))


@lru_cache(1)
def vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H * 0.52) / (H * 0.62)) ** 2)
    v = np.clip(1.08 - 0.62 * d ** 2.2, 0.28, 1.0)
    top = np.clip(1 - (1 - y / (H * 0.30)), 0, 1) * 0.35 + 0.65  # darker top for caption legibility
    v = v * np.minimum(1, top)
    return v[..., None]


@lru_cache(1)
def grains():
    rng = np.random.default_rng(3)
    return [rng.normal(0, 6.5, (H // 2, W // 2, 1)).astype(np.float32) for _ in range(8)]


def finish(im, fi, vig=True):
    a = np.asarray(im).astype(np.float32)
    if vig:
        a *= vignette()
    g = grains()[fi % 8]
    a += np.repeat(np.repeat(g, 2, 0), 2, 1)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


# ------------------------------------------------------------------ particles
class Embers:
    def __init__(self, n=60, seed=1, color=(255, 170, 70), rise=110, size=(2, 6), area=(0, 1)):
        rng = random.Random(seed)
        self.p = [(rng.random(), rng.uniform(*area), rng.uniform(0.4, 1.0), rng.uniform(*size), rng.random() * 6.28)
                  for _ in range(n)]
        self.color, self.rise = color, rise

    def draw(self, base, t, alpha=1.0):
        ov = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(ov)
        for x0, y0, sp, sz, ph in self.p:
            y = (y0 * H - t * self.rise * sp) % (H + 40) - 20
            x = x0 * W + math.sin(t * 0.7 + ph) * 26
            a = int(255 * alpha * (0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 2.3 + ph))) * min(1, y / (H * 0.25) + 0.2))
            r = sz
            d.ellipse((x - r, y - r, x + r, y + r), fill=(*self.color, max(0, a)))
        ov = ov.filter(ImageFilter.GaussianBlur(1.6))
        base.alpha_composite(ov)


# ------------------------------------------------------------------ plates
@lru_cache(8)
def mandala_plate(tone="red"):
    """Dark radial plate with ornamental rings (series look for lists / shlokas / CTA)."""
    pal = {"red": ((122, 30, 24), (28, 5, 6)), "night": ((40, 30, 70), (6, 5, 16)),
           "gold": ((120, 70, 20), (24, 10, 4)), "teal": ((20, 64, 62), (4, 12, 14))}[tone]
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((x - W / 2) ** 2 + (y - H * 0.6) ** 2) / (H * 0.75)
    t = np.clip(d, 0, 1)[..., None]
    a = np.array(pal[0]) * (1 - t) + np.array(pal[1]) * t
    im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    ov = Image.new("RGBA", (W, H))
    dr = ImageDraw.Draw(ov)
    cx, cy = W / 2, H * 0.6
    col = (255, 190, 120, 34)
    for r in (300, 380, 470, 560):
        dr.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=3)
    for k in range(24):
        a_ = 2 * math.pi * k / 24
        px, py = cx + math.cos(a_) * 425, cy + math.sin(a_) * 425
        dr.ellipse((px - 26, py - 26, px + 26, py + 26), outline=col, width=3)
    for k in range(48):
        a_ = 2 * math.pi * k / 48
        dr.line((cx + math.cos(a_) * 300, cy + math.sin(a_) * 300, cx + math.cos(a_) * 380, cy + math.sin(a_) * 380), fill=(255, 190, 120, 20), width=2)
    im.alpha_composite(ov.filter(ImageFilter.GaussianBlur(0.8)))
    return im.convert("RGB")


def chip(txt, size=50, fg=GOLD, border=GOLD, bg=(24, 8, 6, 235), padx=34, pady=22, w=None):
    t = text_img(txt, "anton", size, fg, shadow=False)
    tw, th = t.size
    bw = w or tw + 2 * padx - 60
    bh = th + 2 * pady - 60
    im = Image.new("RGBA", (bw + 8, bh + 8))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, bw + 4, bh + 4), radius=22, fill=bg, outline=border, width=5)
    im.alpha_composite(t, (4 + padx - 30, 4 + pady - 30))
    return im


@lru_cache(16)
def tag_pill(txt):
    t = text_img(txt, "mono", 30, (245, 228, 196), shadow=False)
    w, h = t.size[0] - 60 + 44, t.size[1] - 60 + 26
    im = Image.new("RGBA", (w + 6, h + 6))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, w + 3, h + 3), radius=12, fill=(20, 8, 6, 200), outline=(222, 172, 92, 255), width=3)
    im.alpha_composite(t, (3 + 22 - 30, 3 + 13 - 30))
    return im


# ------------------------------------------------------------------ scene model
class Scene:
    """t0..t1 on the master clock. bg: callable(local_t, frac, fi) -> RGB image.
    caps: [(time, line1, line2, color2)] top-left caption updates.
    fx: list of callables(base_rgba, global_t, scene) drawn after bg, before captions.
    over: list of callables(base_rgba, global_t, scene) drawn after captions."""

    def __init__(self, t0, t1, bg, caps=(), fx=(), over=(), credit=None, grade_kind="warm", shake=None, flash=None, vig=True):
        self.t0, self.t1, self.bg = t0, t1, bg
        self.caps, self.fx, self.over = list(caps), list(fx), list(over)
        self.credit, self.grade_kind, self.shake, self.flash, self.vig = credit, grade_kind, shake, flash, vig

    def frame(self, t, fi, tag):
        dur = max(1e-3, self.t1 - self.t0)
        lt = t - self.t0
        im = self.bg(lt, clamp(lt / dur), fi)
        im = grade(im, self.grade_kind)
        if self.shake and self.shake[0] <= t <= self.shake[0] + self.shake[1]:
            k = 1 - (t - self.shake[0]) / self.shake[1]
            dx, dy = int(math.sin(t * 91) * 16 * k), int(math.cos(t * 77) * 12 * k)
            im = im.transform((W, H), Image.AFFINE, (1, 0, dx, 0, 1, dy), Image.BICUBIC)
        base = im.convert("RGBA")
        for f in self.fx:
            f(base, t, self)
        base = finish(base.convert("RGB"), fi, self.vig).convert("RGBA")
        draw_caps(base, t, self.caps)
        for f in self.over:
            f(base, t, self)
        if tag:
            p = tag_pill(tag)
            base.alpha_composite(p, (W - p.width - 44, 70))
        if self.credit:
            c = text_img(self.credit, "monor", 22, (232, 214, 190), shadow=True)
            paste_fade(base, c, (44 - 30, H - 118), 0.72)
        if self.flash and self.flash[0] <= t <= self.flash[0] + self.flash[1]:
            k = 1 - (t - self.flash[0]) / self.flash[1]
            fl = Image.new("RGBA", (W, H), (*self.flash[2], int(200 * k * k)))
            base.alpha_composite(fl)
        return base.convert("RGB")


CAP_X, CAP_Y, CAP_SIZE, CAP_LH = 66, 190, 112, 112


def draw_caps(base, t, caps):
    """caps: list of (time, line1, line2, color2, time2). The active caption is the last whose time <= t.
    line2 (if any) appears at time2. Each line slides up 26px and fades in over 0.22 s."""
    cur = None
    for c in caps:
        if c[0] <= t:
            cur = c
    if not cur:
        return
    t1, l1, l2, col2, t2 = (list(cur) + [None] * 5)[:5]
    y = CAP_Y
    for line, ts, col in ((l1, t1, CREAM), (l2, t2 if t2 is not None else t1, col2 or GOLD)):
        if not line:
            continue
        if ts is None or t < ts:
            y += CAP_LH
            continue
        k = eo((t - ts) / 0.22)
        size = CAP_SIZE if len(line) <= 17 else int(CAP_SIZE * 17 / len(line)) if len(line) < 26 else 74
        im = text_img(line, "anton", size, col)
        paste_fade(base, im, (CAP_X - 30, y - 30 + 26 * (1 - k)), k)
        y += int(size * 1.0)


# ------------------------------------------------------------------ backgrounds
def BG_kb(path, a, b, maxside=3200):
    src = load_rgb(path, maxside)

    def f(lt, fr, fi):
        return kb_frame(src, a, b, fr)
    return f


def BG_plate(tone="red", drift=True):
    def f(lt, fr, fi):
        im = mandala_plate(tone)
        if drift:
            s = 1.0 + 0.04 * fr
            w, h = W / s, H / s
            im = im.transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) / 2 + 20 * fr, (W + w) / 2, (H + h) / 2 + 20 * fr), Image.BICUBIC)
        return im
    return f


def BG_layer(bgf, path, cx=0.5, cy=0.55, scale0=0.8, scale1=0.9, rot_speed=0.0, glow=None, alpha_in=None):
    """Composite an RGBA render (e.g. chakra, kundal) centred over another background, with scale/rotation."""
    sprite = load_rgba(path)

    def f(lt, fr, fi):
        im = bgf(lt, fr, fi).convert("RGBA")
        s = lerp(scale0, scale1, ss(fr))
        sp = sprite
        if rot_speed:
            sp = sp.rotate(-lt * rot_speed, Image.BICUBIC)
        w = int(W * s)
        h = int(sp.height * w / sp.width)
        sp = sp.resize((w, h), Image.BICUBIC)
        if glow:
            g = sp.split()[3].filter(ImageFilter.GaussianBlur(40))
            gl = Image.new("RGBA", sp.size, (*glow, 0))
            gl.putalpha(g.point(lambda v: int(v * 0.8)))
            im.alpha_composite(gl, (int(W * cx - w / 2), int(H * cy - h / 2)))
        k = 1.0 if alpha_in is None else eo(lt / alpha_in)
        paste_fade(im, sp, (W * cx - w / 2, H * cy - h / 2), k)
        return im.convert("RGB")
    return f


# ------------------------------------------------------------------ overlays
def embers(n=50, seed=1, color=(255, 170, 70), rise=110, alpha=0.9, size=(2, 6)):
    e = Embers(n, seed, color, rise, size)
    return lambda base, t, sc: e.draw(base, t, alpha)


def flicker(strength=0.10, color=(255, 140, 50)):
    def f(base, t, sc):
        k = strength * (0.5 + 0.3 * math.sin(t * 13.1) + 0.2 * math.sin(t * 29.7 + 1.3))
        base.alpha_composite(Image.new("RGBA", (W, H), (*color, int(255 * k * 0.5))))
    return f


def light_glow(cx, cy, r, color=(255, 190, 110), strength=0.55, pulse=0.12):
    @lru_cache(1)
    def blob():
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt((x - cx * W) ** 2 + (y - cy * H) ** 2) / r
        a = np.clip(np.exp(-d * d * 1.6), 0, 1)
        return a

    def f(base, t, sc):
        k = strength * (1 + pulse * math.sin(t * 5.3))
        a = (blob() * 255 * k).clip(0, 255).astype(np.uint8)
        g = Image.new("RGBA", (W, H), (*color, 0))
        g.putalpha(Image.fromarray(a))
        base.alpha_composite(g)
    return f


def chips_at(items):
    """items: [(time, text, x, y, kw)] -> chip appears (slide+fade) at time and stays for the scene."""
    def f(base, t, sc):
        for it in items:
            ts, txt, x, y = it[:4]
            kw = it[4] if len(it) > 4 else {}
            if t < ts:
                continue
            k = eo((t - ts) / 0.25)
            c = chip(txt, **kw)
            xx = W / 2 - c.width / 2 if x == "c" else x
            paste_fade(base, c, (xx, y + 30 * (1 - k)), k)
    return f


def deva_card(ts, line1, line2=None, ref=None, y=880, size=92, color=GOLD):
    """Centred Devanagari shloka lines (+ small mono reference) revealed at ts."""
    def f(base, t, sc):
        if t < ts:
            return
        k = eo((t - ts) / 0.45)
        yy = y
        for ln in (line1, line2):
            if not ln:
                continue
            im = text_img(ln, "deva", size, color)
            paste_fade(base, im, (W / 2 - im.width / 2, yy + 20 * (1 - k)), k)
            yy += int(size * 1.45)
        if ref:
            r = text_img(ref, "monor", 26, (238, 214, 180))
            paste_fade(base, r, (W / 2 - r.width / 2, yy + 20), k * 0.85)
    return f


def big_text(ts, txt, y, size=150, color=CREAM, te=None):
    def f(base, t, sc):
        if t < ts or (te and t > te):
            return
        k = eo((t - ts) / 0.3)
        im = text_img(txt, "anton", size, color)
        s = 1.12 - 0.12 * k
        if abs(s - 1) > 0.005:
            im = im.resize((int(im.width * s), int(im.height * s)), Image.BICUBIC)
        paste_fade(base, im, (W / 2 - im.width / 2, y - (im.height - text_img(txt, 'anton', size, color).height) / 2), k)
    return f


def silhouette_boy(x, y, h=330, color=(12, 6, 6)):
    """Nachiketa as in Part 1: a small boy silhouette with a topknot (drawn as vector)."""
    def f(base, t, sc):
        d = ImageDraw.Draw(base)
        s = h / 330
        cx = x
        def P(px, py):
            return (cx + px * s, y + py * s)
        d.ellipse((*P(-34, 0), *P(34, 66)), fill=color)               # head
        d.ellipse((*P(-14, -26), *P(14, 4)), fill=color)              # topknot
        d.polygon([P(-30, 66), P(30, 66), P(58, 230), P(-58, 230)], fill=color)   # torso/dhoti
        d.rectangle((*P(-40, 225), *P(-12, 330)), fill=color)         # legs
        d.rectangle((*P(12, 225), *P(40, 330)), fill=color)
        d.polygon([P(-30, 80), P(-52, 86), P(-66, 200), P(-48, 202)], fill=color)  # arms
        d.polygon([P(30, 80), P(52, 86), P(66, 200), P(48, 202)], fill=color)
    return f


# ------------------------------------------------------------------ render
def render(scenes, out, tag=None, xfade=0.24, t_end=None):
    t_end = t_end or scenes[-1].t1
    n = int(round(t_end * FPS))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out],
                         stdin=subprocess.PIPE)
    si = 0
    for fi in range(n):
        t = fi / FPS
        while si < len(scenes) - 1 and t >= scenes[si + 1].t0:
            si += 1
        sc = scenes[si]
        im = sc.frame(t, fi, tag)
        if si > 0 and t - sc.t0 < xfade and getattr(sc, "xfade", True):
            prev = scenes[si - 1]
            k = ss((t - sc.t0) / xfade)
            im = Image.blend(prev.frame(t, fi, tag), im, k)
        p.stdin.write(im.tobytes())
        if fi % 300 == 0:
            print(f"  frame {fi}/{n}", flush=True)
    p.stdin.close()
    p.wait()


def still(scenes, t, out, tag=None):
    for i, sc in enumerate(scenes):
        if sc.t0 <= t < sc.t1 or i == len(scenes) - 1:
            sc.frame(t, int(t * FPS), tag).save(out)
            return


# ------------------------------------------------------------------ extra backgrounds
def BG_contain(path, tone="red", cy=0.56, width=0.96, zoom=(1.0, 1.06), paper=True):
    """A wide painting/drawing shown whole, on a plate (for labelled diagrams)."""
    src = load_rgb(path, 2600)

    def f(lt, fr, fi):
        im = BG_plate(tone, drift=False)(lt, fr, fi).convert("RGBA")
        z = lerp(zoom[0], zoom[1], ss(fr))
        w = int(W * width * z)
        h = int(src.height * w / src.width)
        s = src.resize((w, h), Image.BICUBIC).convert("RGBA")
        sh = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((40, 40, w + 40, h + 40), fill=(0, 0, 0, 170))
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        x, y = int(W / 2 - w / 2), int(H * cy - h / 2)
        im.alpha_composite(sh, (x - 40 + 8, y - 40 + 14))
        im.alpha_composite(s, (x, y))
        return im.convert("RGB")
    return f


def BG_fork(tone="night"):
    """Two paths splitting from the viewer: left dim (preya), right golden (shreya)."""
    def f(lt, fr, fi):
        im = mandala_plate(tone).copy().convert("RGBA")
        ov = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(ov)
        k = eo(lt / 1.2)
        base_y, fork_y = H * 0.98, H * lerp(0.98, 0.62, k)
        d.polygon([(W * 0.40, base_y), (W * 0.60, base_y), (W * 0.53, fork_y), (W * 0.47, fork_y)], fill=(70, 50, 60, 220))
        ly = H * lerp(0.62, 0.36, eo((lt - 0.6) / 1.2))
        d.polygon([(W * 0.47, fork_y), (W * 0.51, fork_y), (W * 0.24, ly), (W * 0.20, ly)], fill=(90, 80, 100, 200))
        d.polygon([(W * 0.49, fork_y), (W * 0.53, fork_y), (W * 0.82, ly), (W * 0.78, ly)], fill=(240, 185, 80, 235))
        im.alpha_composite(ov.filter(ImageFilter.GaussianBlur(2)))
        g = ov.filter(ImageFilter.GaussianBlur(28))
        im.alpha_composite(g)
        return im.convert("RGB")
    return f


def BG_stars(seed=5, n=900):
    """Zoom from a single point of light out to a field of stars (anor aniyan mahato mahiyan)."""
    rng = np.random.default_rng(seed)
    pts = rng.normal(0, 1, (n, 2)) * np.array([0.9, 1.4])
    mag = rng.uniform(0.3, 1.0, n)
    col = rng.choice([0, 1, 2], n, p=[0.6, 0.25, 0.15])
    cols = [(255, 236, 210), (255, 190, 120), (170, 200, 255)]

    def f(lt, fr, fi):
        im = Image.new("RGB", (W, H), (6, 5, 14))
        d = ImageDraw.Draw(im)
        z = 40 * (1 - ss(fr)) + 1.0          # start zoomed in on the centre point
        for (x, y), m, c in zip(pts, mag, col):
            sx, sy = W / 2 + x * W * 0.32 / z * 3, H * 0.55 + y * H * 0.2 / z * 3
            if 0 <= sx < W and 0 <= sy < H:
                r = max(1.0, 2.6 * m)
                d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=cols[c])
        im = im.filter(ImageFilter.GaussianBlur(0.6))
        return im
    return f
