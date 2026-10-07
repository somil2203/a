"""Tesla Short compositor: shots + motion graphics + captions + grade -> silent 1080x1920 30fps.

usage: python3 compose.py OUT.mp4 [--from S] [--to S] [--stills DIR]
Timeline is in MASTER_VO.wav seconds (see 01_VO/timemap.json and 11_CAPTIONS/words_master.json).
"""
import io
import json
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
END = 49.6
B = f"{ROOT}/04_BROLL"
P = f"{ROOT}/05_PHOTOS"
R3D = f"{ROOT}/07_3D/renders"

FONTS = {
    "anton": "/home/user/a/edit/fonts/anton.woff",
    "black": "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
    "bold": "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
    "semi": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    "reg": "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
    "mono": "/home/user/a/edit/fonts/jbm.woff",
}
WHITE = (255, 255, 255, 255)
ACCENT = (232, 33, 39, 255)      # signal red
CYAN = (90, 200, 255, 255)
GOLD = (236, 190, 110, 255)
GREEN = (70, 220, 140, 255)
DIM = (170, 180, 195, 255)


# ------------------------------------------------------------------ helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lin(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def eo(x):
    return 1 - (1 - clamp(x)) ** 3


def eio(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def eback(x, s=1.7):
    x = clamp(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


@lru_cache(None)
def font(k, s):
    return ImageFont.truetype(FONTS[k], s)


@lru_cache(2048)
def text_img(txt, fk, size, fill=WHITE, stroke=0, stroke_fill=(0, 0, 0, 255), shadow=0, tracking=0):
    f = font(fk, size)
    if tracking:
        parts = [text_img(c, fk, size, fill, stroke, stroke_fill, 0, 0) for c in txt]
        w = sum(p.width for p in parts) + tracking * (len(parts) - 1)
        h = max(p.height for p in parts)
        im = Image.new("RGBA", (w, h))
        x = 0
        for p in parts:
            im.alpha_composite(p, (x, 0))
            x += p.width + tracking
    else:
        bb = f.getbbox(txt, stroke_width=stroke)
        asc, desc = f.getmetrics()
        pad = stroke + 4
        im = Image.new("RGBA", (bb[2] - bb[0] + 2 * pad, asc + desc + 2 * pad))
        ImageDraw.Draw(im).text((pad - bb[0], pad), txt, font=f, fill=fill, stroke_width=stroke,
                                stroke_fill=stroke_fill)
    if shadow:
        a = im.getchannel("A").filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: int(v * 0.8))
        out = Image.new("RGBA", (im.width + 4 * shadow, im.height + 4 * shadow))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 255))
        sh.putalpha(a)
        out.alpha_composite(sh, (2 * shadow, 2 * shadow + shadow // 2))
        out.alpha_composite(im, (2 * shadow, 2 * shadow))
        return out
    return im


def with_alpha(img, a):
    if a >= 0.999:
        return img
    img = img.copy()
    img.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
    return img


def put(layer, img, cx, cy, scale=1.0, alpha=1.0, rot=0.0, anchor="c"):
    if img is None or alpha <= 0.004 or scale <= 0.01:
        return
    if abs(scale - 1) > 1e-3:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BICUBIC)
    if rot:
        img = img.rotate(rot, Image.BICUBIC, expand=True)
    img = with_alpha(img, alpha)
    x = cx - img.width / 2 if anchor == "c" else cx
    y = cy - img.height / 2
    x, y = int(round(x)), int(round(y))
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(layer.width, x + img.width), min(layer.height, y + img.height)
    if x1 > x0 and y1 > y0:
        layer.alpha_composite(img.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))


def glow(img, r, color, k=1.0):
    a = img.getchannel("A").filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(min(255, v * k)))
    g = Image.new("RGBA", img.size, color[:3] + (255,))
    g.putalpha(a)
    return g


def pad_img(img, p):
    o = Image.new("RGBA", (img.width + 2 * p, img.height + 2 * p))
    o.alpha_composite(img, (p, p))
    return o


def rr(size, r, fill, outline=None, width=2):
    im = Image.new("RGBA", size)
    ImageDraw.Draw(im).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=r, fill=fill, outline=outline,
                                         width=width)
    return im


def chip(text, accent=CYAN, size=30, fk="mono"):
    t = text_img(text, fk, size, WHITE)
    w, h = t.width + 60, t.height + 18
    im = rr((w, h), h // 2, (8, 10, 16, 215), accent[:3] + (190,), 2)
    ImageDraw.Draw(im).ellipse((20, h / 2 - 6, 32, h / 2 + 6), fill=accent)
    im.alpha_composite(t, (42, 9))
    return im


def cover(img, w=W, h=H, cx=0.5, cy=0.5, zoom=1.0):
    """crop-to-fill with focal point and zoom"""
    s = max(w / img.width, h / img.height) * zoom
    nw, nh = img.width * s, img.height * s
    x0 = clamp(cx * nw - w / 2, 0, nw - w)
    y0 = clamp(cy * nh - h / 2, 0, nh - h)
    return img.transform((w, h), Image.AFFINE, (1 / s, 0, x0 / s, 0, 1 / s, y0 / s), Image.BICUBIC)


# ------------------------------------------------------------------ grading
def _curve(lift, gamma, gain):
    x = np.linspace(0, 1, 256)
    y = np.clip(lift + (gain - lift) * x ** gamma, 0, 1)
    y = y + 0.06 * np.sin(np.pi * (y - 0.5)) * (1 - abs(2 * y - 1))  # soft S
    return np.clip(y * 255, 0, 255).astype(np.uint8)


LOOKS = {  # per-channel (lift, gamma, gain), saturation
    "tech": ([(0.01, 1.05, 0.98), (0.02, 1.0, 0.99), (0.05, 0.95, 1.0)], 0.92),
    "warm": ([(0.02, 0.95, 1.0), (0.015, 1.0, 0.97), (0.01, 1.08, 0.92)], 1.0),
    "archive": ([(0.05, 0.95, 0.96), (0.04, 1.0, 0.9), (0.03, 1.1, 0.78)], 0.0),
    "night": ([(0.0, 1.1, 0.95), (0.01, 1.05, 0.97), (0.04, 0.95, 1.0)], 0.85),
    "neutral": ([(0.0, 1.0, 1.0), (0.0, 1.0, 1.0), (0.0, 1.0, 1.0)], 1.0),
    "mono": ([(0.02, 1.05, 0.95), (0.02, 1.05, 0.95), (0.03, 1.0, 0.98)], 0.0),
}
_LUT = {k: [_curve(*c) for c in v[0]] for k, v in LOOKS.items()}


def grade(img, look):
    if look == "none":
        return np.asarray(img).astype(np.float32)
    a = np.asarray(img)
    o = np.empty_like(a)
    for c in range(3):
        o[..., c] = _LUT[look][c][a[..., c]]
    f = o.astype(np.float32)
    sat = LOOKS[look][1]
    if sat != 1.0:
        lum = f @ np.array([0.299, 0.587, 0.114], np.float32)
        if sat == 0.0 and look == "archive":
            f = np.stack([lum * 1.06, lum * 0.98, lum * 0.86], -1)
        else:
            f = lum[..., None] + (f - lum[..., None]) * sat
    return f


_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((_xx - W / 2) / (W * 0.7)) ** 2 + ((_yy - H * 0.47) / (H * 0.62)) ** 2)
VIG = np.clip(1 - 0.5 * np.clip(_r - 0.5, 0, None) ** 1.5, 0.4, 1)[..., None]
GRAIN = [np.random.default_rng(i).normal(0, 1, (H // 2, W // 2)).astype(np.float32) for i in range(8)]


def finish(f, fi, grain=4.0, vig=True):
    if vig:
        f = f * VIG
    g = GRAIN[fi % 8]
    f = f + np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None] * grain
    return np.clip(f, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ media sources
class VideoClip:
    """Decodes a 9:16 crop of a landscape clip at 1242x2208 (headroom for push-ins), resampled to 30 fps."""

    def __init__(self, path, start, cx=0.5, dur=4.0):
        self.path, self.start, self.cx, self.dur = path, start, cx, dur
        self.frames = None

    def load(self):
        if self.frames is not None:
            return
        info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                               "-of", "csv=p=0", self.path], capture_output=True, text=True).stdout.split(",")
        sw, sh = int(info[0]), int(info[1])
        cw = int(sh * 9 / 16)
        x = int(clamp(self.cx * sw - cw / 2, 0, sw - cw))
        ow, oh = 1242, 2208
        cmd = ["ffmpeg", "-v", "error", "-ss", f"{self.start:.3f}", "-i", self.path, "-t", f"{self.dur + 0.2:.3f}",
               "-vf", f"crop={cw}:{sh}:{x}:0,scale={ow}:{oh}:flags=lanczos,fps={FPS}",
               "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
        raw = subprocess.run(cmd, capture_output=True, check=True).stdout
        n = len(raw) // (ow * oh * 3)
        self.frames = [Image.frombuffer("RGB", (ow, oh), raw[i * ow * oh * 3:(i + 1) * ow * oh * 3], "raw", "RGB", 0, 1)
                       for i in range(n)]

    def frame(self, lt, zoom=1.0):
        self.load()
        i = min(len(self.frames) - 1, int(lt * FPS))
        im = self.frames[i]
        z = zoom * (W / 1242) ** -1 * (1242 / W)  # 1.0 == full crop
        s = (1242 / W) / zoom
        return im.transform((W, H), Image.AFFINE, (s, 0, (1242 - W * s) / 2, 0, s, (2208 - H * s) / 2),
                            Image.BICUBIC)

    def free(self):
        self.frames = None


@lru_cache(8)
def photo(name):
    return Image.open(name).convert("RGB")


@lru_cache(64)
def _seq_file(path):
    return Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 50, 2))


def seq_frame(shot, i):
    """frame i at 30 fps; sequences rendered with frame_step>1 are blended between neighbours"""
    d = f"{R3D}/{shot}"
    files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    nums = [int(f[1:5]) for f in files]
    step = (nums[1] - nums[0]) if len(nums) > 1 else 1
    x = clamp(i / step, 0, len(files) - 1)
    a, frac = int(x), x - int(x)
    ia = _seq_file(f"{d}/{files[a]}")
    if frac < 0.01 or a + 1 >= len(files):
        return ia
    return Image.blend(ia, _seq_file(f"{d}/{files[a + 1]}"), frac)


# ------------------------------------------------------------------ words / captions
WORDS = json.load(open(f"{ROOT}/11_CAPTIONS/words_master.json"))
FIX = {"Mark": "Marc", "Tarpening,": "Tarpenning,"}
_w = []
for i, (t, s, e) in enumerate(WORDS):
    t = FIX.get(t, t)
    if t.startswith("-") and _w:
        _w[-1][0] += t
        continue
    _w.append([t, s, e])
for i in range(len(_w)):
    nxt = _w[i + 1][1] if i + 1 < len(_w) else _w[i][1] + 0.6
    _w[i][2] = min(nxt, _w[i][1] + 0.7)
WORDS = _w


def wt(word, after=0.0):
    """start time of the first word matching `word` (case-insensitive prefix) after time `after`"""
    for t, s, e in WORDS:
        if s >= after and t.lower().strip(",.?!").startswith(word.lower()):
            return s
    raise KeyError(word)


EMPH = {"tesla?": ACCENT, "wrong.": ACCENT, "2003.": GOLD, "eberhard": GOLD, "tarpenning,": GOLD, "electric": CYAN,
        "cool.": CYAN, "nikola": GOLD, "tesla.": GOLD, "money.": ACCENT, "2004,": GOLD, "billionaire": WHITE,
        "musk.": ACCENT, "millions,": GREEN, "chairman,": ACCENT, "control.": ACCENT, "crazy": ACCENT, "2007,": GOLD,
        "pushed": ACCENT, "out": ACCENT, "sued,": ACCENT, "co-founder.": ACCENT, "everyone": CYAN, "real": GOLD,
        "founders?": GOLD, "never": ACCENT, "names.": GOLD}

# caption pages: break on punctuation or every 3 words
PAGES = []
cur = []
for w in WORDS:
    cur.append(w)
    if w[0][-1] in ".?!," or len(cur) >= 3:
        PAGES.append(cur)
        cur = []
if cur:
    PAGES.append(cur)
NO_CAPS = []  # (t0, t1) windows where the words are already big on screen


def draw_captions(t, L):
    for a, b in NO_CAPS:
        if a <= t < b:
            return
    for k, pg in enumerate(PAGES):
        s = pg[0][1]
        e = PAGES[k + 1][0][1] if k + 1 < len(PAGES) else pg[-1][2] + 0.4
        e = min(e, pg[-1][2] + 0.5)
        if not (s - 0.04 <= t < e):
            continue
        imgs = []
        for txt, ws, we in pg:
            key = txt.lower()
            col = EMPH.get(key, WHITE)
            active = ws <= t < we
            imgs.append((text_img(txt.upper(), "black", 70, col, 0, (0, 0, 0, 255), 7), ws, we, active))
        gap = 20
        tw = sum(i[0].width for i in imgs) + gap * (len(imgs) - 1)
        k2 = min(1.0, 940 / tw)
        x = W / 2 - tw * k2 / 2
        for img, ws, we, active in imgs:
            w = img.width * k2
            if t >= ws - 0.03:
                p = lin(t, ws - 0.03, ws + 0.09)
                sc = k2 * (0.85 + 0.15 * eback(p)) * (1.06 if active else 1.0)
                put(L, img, x + w / 2, 1430 + 10 * (1 - eo(p)), sc, clamp(p * 2.2) * (1.0 if active or t > we else 0.92))
            x += w + gap * k2
        return


# ------------------------------------------------------------------ shared graphics
def grid_bg(t, tint=(10, 14, 24), line=(40, 70, 110), spacing=90, drift=12):
    im = Image.new("RGB", (W, H), tint)
    d = ImageDraw.Draw(im)
    off = (t * drift) % spacing
    for x in range(-spacing, W + spacing, spacing):
        d.line((x + off, 0, x + off, H), fill=line, width=1)
    for y in range(-spacing, H + spacing, spacing):
        d.line((0, y + off, W, y + off), fill=line, width=1)
    return im


def label(L, t, t0, text, y=300, accent=CYAN, size=30):
    p = eo(lin(t, t0, t0 + 0.25))
    put(L, chip(text, accent, size), W / 2, y - 24 * (1 - p), 1.0, p)


def year_tag(L, t, t0, year, y=250):
    p = eo(lin(t, t0, t0 + 0.3))
    im = text_img(year, "anton", 120, GOLD, 0, (0, 0, 0, 255), 6)
    put(L, im, W / 2, y + 30 * (1 - p), 0.9 + 0.1 * p, p)


def lightning_bolt(seed, length=1300, x0=700, y0=0):
    rng = np.random.default_rng(seed)
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)

    def branch(x, y, ang, ln, w, depth):
        pts = [(x, y)]
        for _ in range(int(ln / 40)):
            ang += rng.normal(0, 0.35)
            x += math.sin(ang) * 40
            y += math.cos(ang) * 40
            pts.append((x, y))
            if depth < 2 and rng.random() < 0.08:
                branch(x, y, ang + rng.choice([-0.8, 0.8]), ln * 0.35, max(1, w - 2), depth + 1)
        d.line(pts, fill=(235, 240, 255, 255), width=w)

    branch(x0, y0, 0.15, length, 6, 0)
    out = Image.new("RGBA", (W, H))
    out.alpha_composite(glow(im, 18, (150, 170, 255), 2.2))
    out.alpha_composite(glow(im, 5, (210, 220, 255), 1.6))
    out.alpha_composite(im)
    return out


@lru_cache(1)
def roadster_blueprint():
    """Edge-traced blueprint of the real 2008 Roadster photo (so the 'idea' literally becomes the car)."""
    im = photo(f"{P}/roadster_2008.jpg")
    im = cover(im, W, 560, cx=0.6, cy=0.62, zoom=1.0)
    g = ImageOps.grayscale(im).filter(ImageFilter.GaussianBlur(1.6))
    e = g.filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 34 else 0)
    e = e.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    bp = Image.new("RGBA", e.size, (130, 210, 255, 255))
    bp.putalpha(e)
    return bp, im


# ------------------------------------------------------------------ shot functions -> (rgb float, overlay rgba)
T = {}  # anchors computed in build()


def shot_search(t, fi):
    bg = grid_bg(t, (6, 9, 16), (22, 36, 58))
    L = Image.new("RGBA", (W, H))
    # glass search bar
    p = 1.0
    z = 1.0 + 0.06 * eio(lin(t, 0, 1.85))
    bar = rr((960, 150), 75, (255, 255, 255, 30), (255, 255, 255, 110), 3)
    put(L, glow(pad_img(bar, 30), 30, (80, 150, 255), 0.35), W / 2, 820, z)
    put(L, bar, W / 2, 820, z)
    full = "who started tesla?"
    n = int(clamp((t - 0.05) / 1.05) * len(full))
    q = full[:n]
    tx = text_img(q if q else " ", "semi", 64, WHITE)
    put(L, tx, 180, 820, 1.0, p, anchor="l")
    if int(t * 2.5) % 2 == 0 or n < len(full):
        cur = Image.new("RGBA", (5, 72), (255, 255, 255, 230))
        put(L, cur, 188 + tx.width, 820, 1.0, p)
    ic = Image.new("RGBA", (60, 60))
    ImageDraw.Draw(ic).ellipse((8, 8, 40, 40), outline=(255, 255, 255, 200), width=5)
    ImageDraw.Draw(ic).line((36, 36, 52, 52), fill=(255, 255, 255, 200), width=6)
    put(L, ic, 120, 820, 1.0, p)
    # suggestion rows appear as the question completes
    for k, s in enumerate(["tesla founder", "tesla history", "who owns tesla"]):
        a = eo(lin(t, 1.25 + k * 0.08, 1.45 + k * 0.08))
        put(L, text_img(s, "reg", 42, DIM), 180, 960 + k * 78, 1.0, a, anchor="l")
    return grade(bg, "none"), L


def answer_card(t, t0):
    """Musk 2006 photo inside an 'answer' card"""
    ph = photo(f"{P}/musk_2006.jpg")
    face = cover(ph, 720, 860, cx=0.37, cy=0.27, zoom=1.9 + 0.08 * lin(t, t0, t0 + 2.0))
    card = Image.new("RGBA", (780, 1100), (0, 0, 0, 0))
    base = rr((780, 1100), 36, (14, 16, 22, 245), (255, 255, 255, 60), 2)
    card.alpha_composite(base)
    m = Image.new("L", (720, 860), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 719, 859), radius=26, fill=255)
    fc = face.convert("RGBA")
    fc.putalpha(m)
    card.alpha_composite(fc, (30, 30))
    card.alpha_composite(text_img("ELON MUSK", "black", 72, WHITE), (40, 912))
    ok = Image.new("RGBA", (70, 70))
    ImageDraw.Draw(ok).ellipse((0, 0, 69, 69), fill=GREEN)
    ImageDraw.Draw(ok).line((18, 36, 30, 48, 52, 22), fill=(0, 0, 0, 255), width=8)
    card.alpha_composite(ok, (680, 924))
    card.alpha_composite(text_img("Founder of Tesla?", "reg", 36, DIM), (44, 1010))
    return card


def credit(L, text, y=1840):
    put(L, text_img(text, "reg", 22, (210, 210, 215, 200)), W / 2, y, 1, 0.85)


def shot_answer(t, fi):
    t0 = T["answer"]
    bg = grid_bg(t, (6, 9, 16), (22, 36, 58))
    L = Image.new("RGBA", (W, H))
    p = eback(lin(t, t0, t0 + 0.3))
    put(L, glow(pad_img(answer_card(t, t0), 40), 40, (60, 140, 255), 0.5), W / 2, 780, 0.8 + 0.08 * p, clamp(p))
    put(L, answer_card(t, t0), W / 2, 780, 0.8 + 0.08 * p, clamp(p * 1.5))
    credit(L, "Photo: FlyingSinger (2006), CC BY 2.0, cropped")
    return grade(bg, "none"), L


@lru_cache(1)
def shards():
    """Voronoi shards of the answer card, each with its own drift vector"""
    card = answer_card(T["wrong"], T["answer"])
    rng = np.random.default_rng(3)
    pts = rng.random((26, 2)) * [card.width, card.height]
    pts = np.vstack([pts, [[card.width * 0.55, card.height * 0.42]]])
    yy, xx = np.mgrid[0:card.height, 0:card.width]
    d = ((xx[..., None] - pts[:, 0]) ** 2 + (yy[..., None] - pts[:, 1]) ** 2)
    lab = d.argmin(-1)
    out = []
    for k in range(len(pts)):
        m = Image.fromarray(((lab == k) * 255).astype(np.uint8))
        bb = m.getbbox()
        if not bb:
            continue
        piece = card.crop(bb)
        a = ImageChops.multiply(piece.getchannel("A"), m.crop(bb))
        piece.putalpha(a)
        c = np.array([(bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2])
        v = (c - [card.width * 0.55, card.height * 0.42])
        v = v / (np.linalg.norm(v) + 1e-6) * rng.uniform(500, 1500) + rng.normal(0, 120, 2)
        out.append((piece, c - [card.width / 2, card.height / 2], v, rng.uniform(-260, 260)))
    return out


def shot_wrong(t, fi):
    tw = T["wrong"]
    bg = grid_bg(t, (6, 9, 16), (22, 36, 58))
    L = Image.new("RGBA", (W, H))
    if t < tw:
        put(L, answer_card(t, T["answer"]), W / 2, 780, 0.88 + 0.02 * math.sin(t * 60))
    else:
        dt = t - tw
        for piece, off, v, spin in shards():
            x = W / 2 + off[0] * 0.88 + v[0] * dt * (1 + dt)
            y = 780 + off[1] * 0.88 + v[1] * dt * (1 + dt) + 900 * dt * dt
            put(L, piece, x, y, 0.88 - 0.22 * clamp(dt * 2), clamp(1.2 - dt * 1.3), spin * dt)
        p = eback(lin(t, tw + 0.02, tw + 0.16), 2.5)
        put(L, glow(pad_img(text_img("WRONG.", "anton", 250, ACCENT), 40), 30, (255, 40, 40), 0.9), W / 2, 880,
            1.4 - 0.4 * p, clamp(p))
        put(L, text_img("WRONG.", "anton", 250, (255, 255, 255, 255)), W / 2, 880, 1.4 - 0.4 * p, clamp(p))
    f = grade(bg, "none")
    if tw <= t < tw + 0.12:
        f = f + 160 * (1 - (t - tw) / 0.12)
    return f, L


def shot_3d(name, t0, look="none"):
    def fn(t, fi):
        im = seq_frame(name, int(round((t - t0) * FPS)))
        return grade(im, look), Image.new("RGBA", (W, H))
    return fn


def shot_video(clip, t0, z0=1.0, z1=1.08, look="tech", extra=None):
    def fn(t, fi):
        p = lin(t, t0, t0 + clip.dur)
        im = clip.frame(t - t0, z0 + (z1 - z0) * eio(p))
        L = Image.new("RGBA", (W, H))
        f = grade(im, look)
        if extra:
            f = extra(t, f, L)
        return f, L
    return fn


def shot_photo(path, t0, dur, cx, cy, z0, z1, look, fx=None):
    def fn(t, fi):
        p = eio(lin(t, t0, t0 + dur))
        im = cover(photo(path), W, H, cx, cy, z0 + (z1 - z0) * p)
        L = Image.new("RGBA", (W, H))
        f = grade(im, look)
        if fx:
            f = fx(t, f, L)
        return f, L
    return fn


def engineers_extra(t, f, L):
    label(L, t, T["engineers"] + 0.2, "2003 · SAN CARLOS, CALIFORNIA", 300, GOLD)
    return f


def dossier_card(name1, name2, role, photo_path=None, monogram=None):
    c = rr((440, 640), 28, (12, 14, 20, 240), (255, 255, 255, 70), 2)
    if photo_path:
        ph = cover(photo(photo_path), 380, 420, 0.5, 0.33, 1.0)
        ph = ImageOps.grayscale(ph).convert("RGB")
        ph = Image.blend(ph, Image.new("RGB", ph.size, (40, 70, 110)), 0.12).convert("RGBA")
        m = Image.new("L", ph.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), radius=18, fill=255)
        ph.putalpha(m)
        c.alpha_composite(ph, (30, 30))
    else:
        box = rr((380, 420), 18, (24, 30, 44, 255))
        mg = text_img(monogram, "anton", 170, (90, 120, 170, 255))
        box.alpha_composite(mg, (190 - mg.width // 2, 210 - mg.height // 2))
        c.alpha_composite(box, (30, 30))
    c.alpha_composite(text_img(name1, "bold", 40, DIM), (34, 470))
    c.alpha_composite(text_img(name2, "black", 52, WHITE), (32, 512))
    c.alpha_composite(text_img(role, "mono", 26, GOLD), (36, 585))
    return c


def shot_dossier(t, fi):
    bg = grid_bg(t, (8, 14, 28), (30, 58, 96), 70, 8)
    L = Image.new("RGBA", (W, H))
    te, tt, ti = T["eberhard"], T["tarp"], T["idea"]
    ce = dossier_card("MARTIN", "EBERHARD", "ENGINEER · CO-FOUNDER", f"{P}/eberhard.jpg")
    ct = dossier_card("MARC", "TARPENNING", "ENGINEER · CO-FOUNDER", monogram="MT")
    up = eio(lin(t, ti, ti + 0.45))
    y = 800 - 430 * up
    s = 1.12 - 0.5 * up
    pe = eback(lin(t, te - 0.1, te + 0.25))
    put(L, ce, 290 + 60 * up, y + 60 * (1 - clamp(pe)), s, clamp(pe * 1.4), -3 * (1 - up))
    pt = eback(lin(t, tt - 0.1, tt + 0.25))
    credit(L, "Eberhard photo: Nicki Dugan, CC BY-SA 2.0, cropped & desaturated", 1800)
    put(L, ct, 790 - 60 * up, y + 60 * (1 - clamp(pt)), s, clamp(pt * 1.4), 3 * (1 - up))
    # "crazy idea": blueprint of the eventual car draws itself left -> right
    if t >= ti:
        bp, _ = roadster_blueprint()
        r = eio(lin(t, ti + 0.15, ti + 1.25))
        w = int(bp.width * r)
        if w > 2:
            seg = bp.crop((0, 0, w, bp.height))
            L.alpha_composite(glow(seg, 6, (80, 170, 255), 1.4), (0, 760))
            L.alpha_composite(seg, (0, 760))
            d = ImageDraw.Draw(L)
            d.line((w, 760, w, 1320), fill=(160, 220, 255, 200), width=3)
        credit(L, "Blueprint traced from photo by loudumo, CC BY 2.0")
        put(L, chip("THE IDEA: AN ELECTRIC CAR PEOPLE ACTUALLY WANT", CYAN, 27), W / 2, 700,
            1.0, eo(lin(t, ti + 0.6, ti + 0.9)))
    return grade(bg, "none"), L


def roadster_fx(t, f, L):
    t0 = T["roadster"]
    # blueprint lines dissolve into the real photo
    k = 1 - lin(t, t0, t0 + 0.18)
    if k > 0:
        f = f + 140 * k
    label(L, t, t0 + 0.25, "TESLA ROADSTER · FIRST CAR, 2008", 300, CYAN)
    credit(L, "Photo: loudumo, CC BY 2.0, cropped")
    return f


def storm_fx(t, f, L):
    f = f * 1.9 + 6
    tf = T["flash"]
    if tf - 0.05 <= t < tf + 0.35:
        k = 1 - lin(t, tf, tf + 0.35)
        bolt = lightning_bolt(11, 1500, 760, -40)
        L.alpha_composite(with_alpha(bolt, k))
        f = f * (1 + 1.4 * k)
    return f


def tesla_fx(t, f, L):
    t0 = T["nikola"]
    k = 1 - lin(t, t0, t0 + 0.25)
    if k > 0:
        f = f + 200 * k
    # thin electric arcs crawl along the frame edges
    rng = np.random.default_rng(int(t * 30))
    d = ImageDraw.Draw(L)
    for side in range(2):
        x = 60 if side == 0 else W - 60
        pts = [(x + rng.normal(0, 14), y) for y in range(200, 1700, 60)]
        if rng.random() < 0.55:
            arc = Image.new("RGBA", (W, H))
            ImageDraw.Draw(arc).line(pts, fill=(200, 220, 255, 200), width=2)
            L.alpha_composite(glow(arc, 8, (120, 160, 255), 1.5))
            L.alpha_composite(arc)
    label(L, t, t0 + 0.2, "NIKOLA TESLA · INVENTOR · 1856–1943", 300, GOLD)
    credit(L, "Photo: Library of Congress, Bain Collection (public domain)")
    return f


def money_fx(t, f, L):
    tm = T["money"]
    if t >= tm:
        p = eback(lin(t, tm, tm + 0.14), 2.2)
        f = f * (1 - 0.55 * clamp(p))
        put(L, glow(pad_img(text_img("MONEY.", "anton", 230, ACCENT), 30), 26, (255, 30, 30), 0.8), W / 2, 880,
            1.5 - 0.5 * p, clamp(p))
        put(L, text_img("MONEY.", "anton", 230, WHITE), W / 2, 880, 1.5 - 0.5 * p, clamp(p))
    else:
        label(L, t, T["problem"] - 0.2, "PROBLEM #1", 300, ACCENT)
    return f


def silhouette_fx(t, f, L):
    label(L, t, T["walks"] - 0.6, "FEBRUARY 2004", 300, GOLD)
    tf = T["factcheck"]
    p = eo(lin(t, tf, tf + 0.3))
    if p > 0:
        box = rr((900, 190), 22, (10, 12, 18, 230), (255, 200, 80, 200), 2)
        box.alpha_composite(text_img("FACT CHECK", "mono", 26, GOLD), (28, 20))
        box.alpha_composite(text_img("In 2004 Musk had ~$180M from PayPal.", "semi", 34, WHITE), (28, 62))
        box.alpha_composite(text_img("He became a billionaire years later.", "semi", 34, DIM), (28, 112))
        put(L, box, W / 2, 1640 - 1640 + 1180 + 30 * (1 - p), 1, p)
    return f


def musk_reveal_fx(t, f, L):
    t0 = T["muskname"]
    k = 1 - lin(t, t0, t0 + 0.2)
    if k > 0:
        f = f + 180 * k
    p = eback(lin(t, t0 + 0.05, t0 + 0.3))
    put(L, text_img("ELON MUSK", "anton", 150, WHITE, 0, (0, 0, 0, 255), 10), W / 2, 1180, 1.2 - 0.2 * p, clamp(p))
    put(L, text_img("JOINS TESLA · 2004", "mono", 32, GOLD), W / 2, 1290, 1, eo(lin(t, t0 + 0.25, t0 + 0.5)))
    credit(L, "Photo: FlyingSinger (2006), CC BY 2.0, cropped")
    return f


def shot_seriesA(t, fi):
    bg = grid_bg(t, (7, 10, 18), (24, 40, 64))
    L = Image.new("RGBA", (W, H))
    t0 = T["seriesA"]
    put(L, text_img("SERIES A · FEBRUARY 2004", "mono", 34, DIM), W / 2, 330, 1, eo(lin(t, t0, t0 + 0.3)))
    # ring: Musk's share of the $7.5M round
    share = 6.5 / 7.5
    p = eio(lin(t, T["invests"], T["invests"] + 0.9)) * share
    ring = Image.new("RGBA", (640, 640))
    d = ImageDraw.Draw(ring)
    d.ellipse((20, 20, 620, 620), outline=(40, 50, 70, 255), width=34)
    if p > 0:
        d.arc((20, 20, 620, 620), -90, -90 + 360 * p, fill=ACCENT, width=34)
    put(L, glow(ring, 14, (255, 40, 40), 0.7), W / 2, 820, 1, eo(lin(t, t0, t0 + 0.3)))
    put(L, ring, W / 2, 820, 1, eo(lin(t, t0, t0 + 0.3)))
    val = 6.5 * p / share
    put(L, text_img(f"${val:.1f}M", "anton", 150, WHITE), W / 2, 790, 1, eo(lin(t, t0, t0 + 0.3)))
    put(L, text_img("of $7.5M from Musk", "semi", 38, DIM), W / 2, 905, 1, eo(lin(t, T["invests"], T["invests"] + 0.4)))
    # chairman + control
    tc = T["chairman"]
    pc = eback(lin(t, tc, tc + 0.25))
    put(L, chip("CHAIRMAN OF THE BOARD", ACCENT, 34), W / 2, 1200, 0.9 + 0.1 * pc, clamp(pc))
    tl = T["control"]
    pl = eo(lin(t, tl, tl + 0.3))
    put(L, chip("LARGEST SHAREHOLDER", ACCENT, 34), W / 2, 1290, 0.9 + 0.1 * pl, pl)
    return grade(bg, "none"), L


def shot_crazy(t, fi):
    bg = Image.new("RGB", (W, H), (4, 4, 6))
    L = Image.new("RGBA", (W, H))
    t0 = T["crazy"]
    words = [("BUT HERE'S", WHITE, 0.0), ("THE CRAZY", ACCENT, 0.35), ("PART.", ACCENT, 0.75)]
    for k, (w, c, d) in enumerate(words):
        p = eo(lin(t, t0 + d, t0 + d + 0.25))
        im = text_img(w, "anton", 160, c)
        sweep = 1 - abs(((t - t0 - d) * 1.5) % 2 - 1)
        put(L, im, W / 2, 700 + k * 190 + 40 * (1 - p), 1.0 + 0.03 * (t - t0), p)
    return grade(bg, "none"), L


def network_fx_wrap(fn):
    def g(t, fi):
        f, L = fn(t, fi)
        tp = T["pushed"]
        if t < tp + 0.3:
            year_tag(L, t, T["y2007"], "2007", 260)
            if t >= tp:
                L2 = Image.new("RGBA", (W, H))
                year_tag(L2, t, T["y2007"], "2007", 260)
        if t >= tp:
            put(L, chip("REMOVED AS CEO", ACCENT, 34), W / 2, 1270, 1, eo(lin(t, tp, tp + 0.25)))
        return f, L
    return g


def signing_fx(t, f, L):
    label(L, t, T["sued"] - 0.2, "JUNE 2009 · EBERHARD SUES", 300, ACCENT)
    return f


def shot_document(t, fi):
    t0 = T["doc"]
    bg = Image.new("RGB", (W, H), (10, 10, 12))
    L = Image.new("RGBA", (W, H))
    paper = Image.new("RGBA", (900, 1240), (238, 234, 224, 255))
    d = ImageDraw.Draw(paper)
    d.text((60, 60), "SETTLEMENT", font=font("black", 64), fill=(20, 20, 24))
    d.text((60, 140), "Eberhard v. Musk & Tesla Motors · September 2009", font=font("reg", 26), fill=(80, 80, 90))
    d.line((60, 190, 840, 190), fill=(30, 30, 30), width=3)
    rng = np.random.default_rng(5)
    y = 230
    for k in range(7):
        ln = rng.uniform(0.55, 1.0)
        d.rounded_rectangle((60, y, 60 + 780 * ln, y + 14), radius=7, fill=(200, 196, 186))
        y += 40
    d.text((60, 540), "The following individuals may describe", font=font("semi", 34), fill=(30, 30, 34))
    d.text((60, 585), "themselves as founders of Tesla:", font=font("semi", 34), fill=(30, 30, 34))
    names = ["Martin Eberhard", "Marc Tarpenning", "Ian Wright", "J.B. Straubel", "Elon Musk"]
    for k, n in enumerate(names):
        d.text((90, 660 + k * 66), "•  " + n, font=font("bold", 40), fill=(20, 20, 24))
    d.text((60, 1150), "Illustrative recreation of publicly reported terms", font=font("reg", 22), fill=(120, 120, 130))
    # highlight Musk line, then CO-FOUNDER stamp
    tm = T["doc_musk"]
    hp = eio(lin(t, tm, tm + 0.4))
    if hp > 0:
        hl = Image.new("RGBA", (int(330 * hp), 58), (255, 70, 60, 110))
        paper.alpha_composite(hl, (120, 660 + 4 * 66 - 2))
    # camera: slow push toward the names list
    z = 1.0 + 0.22 * eio(lin(t, t0, t0 + 3.4))
    cy = 740 - 150 * (z - 1)
    put(L, paper, W / 2, cy, 0.76 * z, eo(lin(t, t0, t0 + 0.25)), -1.5)
    ts = T["cofounder"]
    if t >= ts:
        p = lin(t, ts, ts + 0.12)
        st = rr((560, 150), 18, (0, 0, 0, 0), ACCENT, 10)
        tx = text_img("CO-FOUNDER", "anton", 100, ACCENT)
        st.alpha_composite(tx, (280 - tx.width // 2, 75 - tx.height // 2))
        put(L, st, 650, 1080, 1.6 - 0.8 * eo(p), clamp(p * 3), 10)
    return grade(bg, "none"), L


CROWD_TAGS = [(0.32, 0.55), (0.62, 0.48), (0.45, 0.66), (0.75, 0.62), (0.22, 0.72), (0.55, 0.78), (0.38, 0.45),
              (0.68, 0.72), (0.28, 0.6), (0.82, 0.5), (0.5, 0.56), (0.6, 0.86)]


def crowd_fx(t, f, L):
    tb = T["believes"]
    for k, (x, y) in enumerate(CROWD_TAGS):
        tk = tb + k * 0.09
        if t >= tk:
            p = eback(lin(t, tk, tk + 0.18))
            tag = chip("MUSK", ACCENT, 24, "mono")
            put(L, tag, x * W, y * H - 60, 0.6 + 0.4 * clamp(p), clamp(p))
            ImageDraw.Draw(L).line((x * W, y * H - 40, x * W, y * H), fill=(255, 80, 70, int(200 * clamp(p))), width=2)
    put(L, text_img("“MUSK BUILT TESLA”", "anton", 96, WHITE, 0, (0, 0, 0, 255), 8), W / 2, 420, 1,
        eo(lin(t, T["muskbuilt"], T["muskbuilt"] + 0.3)))
    return f


def shot_founders(t, fi):
    t0 = T["realf"]
    bg = Image.new("RGB", (W, H), (6, 7, 10))
    L = Image.new("RGBA", (W, H))
    ce = dossier_card("MARTIN", "EBERHARD", "CO-FOUNDER · 2003", f"{P}/eberhard.jpg")
    ct = dossier_card("MARC", "TARPENNING", "CO-FOUNDER · 2003", monogram="MT")
    z = 1.0 + 0.05 * lin(t, t0, t0 + 2.0)
    put(L, ce, 300, 860, 1.05 * z, eo(lin(t, t0, t0 + 0.3)), -2)
    put(L, ct, 780, 860, 1.05 * z, eo(lin(t, t0 + 0.12, t0 + 0.42)), 2)
    put(L, text_img("THE REAL FOUNDERS", "anton", 110, GOLD), W / 2, 330, 1, eo(lin(t, t0 + 0.2, t0 + 0.5)))
    credit(L, "Eberhard photo: Nicki Dugan, CC BY-SA 2.0, cropped & desaturated")
    return grade(bg, "none"), L


def names_wrap(fn):
    def g(t, fi):
        f, L = fn(t, fi)
        put(L, text_img("FOUNDED TESLA · JULY 1, 2003", "mono", 32, GOLD), W / 2, 330, 1,
            eo(lin(t, T["names"] + 0.4, T["names"] + 0.8)) * (1 - lin(t, END - 1.0, END - 0.3)))
        fade = lin(t, END - 0.9, END)
        return f * (1 - fade), L
    return g


# ------------------------------------------------------------------ edit decision list
def build():
    T.update(
        answer=wt("Elon") - 0.05, wrong=wt("Wrong"), y2003=wt("It's") - 0.1, engineers=wt("Two") - 0.1,
        eberhard=wt("Martin"), tarp=wt("Marc"), idea=wt("have"), car=wt("An", 10.5) - 0.05, roadster=wt("actually") - 0.45,
        storm=wt("They", 13) - 0.1, flash=wt("company", 13), nikola=wt("Nikola") - 0.5, problem=wt("problem"),
        money=wt("Money"), door=wt("Then") - 0.1, walks=wt("walks"), factcheck=wt("young"), muskname=wt("Elon", 22) - 0.05,
        seriesA=wt("He", 23.5) - 0.07, invests=wt("invests"), chairman=wt("chairman"), control=wt("control"),
        crazy=wt("But", 27) - 0.1, net=wt("In", 28.9) - 0.1, y2007=wt("2007"), pushed=wt("pushed"),
        sued=wt("He", 34.5) - 0.07, doc=wt("settlement") - 0.25, doc_musk=wt("Musk", 36.5), cofounder=wt("co-founder"),
        crowd=wt("So", 39) - 0.1, believes=wt("everyone"), muskbuilt=wt("believes"), realf=wt("but", 43.5) - 0.1,
        names=wt("Most") - 0.15,
    )
    clips = {
        "eng": VideoClip(f"{B}/mixkit_39839_man-working-on-computer-in-an-office_4k.mp4", 4.0, 0.37, 1.4),
        "head": VideoClip(f"{B}/mixkit_49_closeup-of-red-sports-car_4k.mp4", 3.9, 0.45, 1.2),
        "storm": VideoClip(f"{B}/mixkit_4422_thunderstorm-at-night_4k.mp4", 10.83 - (T["flash"] - T["storm"]), 0.68, 2.0),
        "wallet": VideoClip(f"{B}/mixkit_18299_person-realizes-that-they-no-longer-have_4k.mp4", 3.0, 0.55, 2.8),
        "sil": VideoClip(f"{B}/mixkit_1038_dancer-in-the-dark-back-view.mp4", 0.2, 0.5, 2.0),
        "sign": VideoClip(f"{B}/mixkit_307_person-signing-a-contract_4k.mp4", 2.0, 0.62, 1.8),
        "crowd": VideoClip(f"{B}/mixkit_4401_crowds-of-people-cross-a-street-junction.mp4", 4.0, 0.5, 4.3),
    }
    edl = [
        (0.0, T["answer"], shot_search, None),
        (T["answer"], T["wrong"] - 0.12, shot_answer, None),
        (T["wrong"] - 0.12, T["y2003"], shot_wrong, None),
        (T["y2003"], T["engineers"], shot_3d("year2003", T["y2003"]), None),
        (T["engineers"], T["eberhard"] - 0.1, shot_video(clips["eng"], T["engineers"], 1.0, 1.06, "night", engineers_extra), "eng"),
        (T["eberhard"] - 0.1, T["car"], shot_dossier, None),
        (T["car"], T["roadster"], shot_video(clips["head"], T["car"], 1.05, 1.15, "tech"), "head"),
        (T["roadster"], T["storm"], shot_photo(f"{P}/roadster_2008.jpg", T["roadster"], 1.6, 0.6, 0.6, 1.05, 1.18, "tech", roadster_fx), None),
        (T["storm"], T["nikola"], shot_video(clips["storm"], T["storm"], 1.0, 1.1, "night", storm_fx), "storm"),
        (T["nikola"], T["problem"] - 0.6, shot_photo(f"{ROOT}/06_ARCHIVE/nikola_tesla_bain_04851.jpg", T["nikola"], 2.2, 0.5, 0.38, 1.25, 1.42, "archive", tesla_fx), None),
        (T["problem"] - 0.6, T["door"], shot_video(clips["wallet"], T["problem"] - 0.6, 1.0, 1.12, "warm", money_fx), "wallet"),
        (T["door"], T["door"] + 1.8, shot_3d("doorway", T["door"]), None),
        (T["door"] + 1.8, T["muskname"], shot_video(clips["sil"], T["door"] + 1.8, 1.0, 1.1, "night", silhouette_fx), "sil"),
        (T["muskname"], T["seriesA"], shot_photo(f"{P}/musk_2006.jpg", T["muskname"], 1.0, 0.36, 0.3, 1.9, 2.05, "tech", musk_reveal_fx), None),
        (T["seriesA"], T["crazy"], shot_seriesA, None),
        (T["crazy"], T["net"], shot_crazy, None),
        (T["net"], T["sued"], network_fx_wrap(shot_3d("network", T["net"])), None),
        (T["sued"], T["doc"], shot_video(clips["sign"], T["sued"], 1.0, 1.1, "warm", signing_fx), "sign"),
        (T["doc"], T["crowd"], shot_document, None),
        (T["crowd"], T["realf"], shot_video(clips["crowd"], T["crowd"], 1.0, 1.08, "tech", crowd_fx), "crowd"),
        (T["realf"], T["names"], shot_founders, None),
        (T["names"], END, names_wrap(shot_3d("names", T["names"])), None),
    ]
    NO_CAPS.extend([(T["wrong"], T["y2003"] + 0.35), (T["muskname"], T["seriesA"]), (T["money"], T["door"]), (T["crazy"], T["net"])])
    return edl, clips


def main():
    out = sys.argv[1]
    a = sys.argv[2:]
    t_from = float(a[a.index("--from") + 1]) if "--from" in a else 0.0
    t_to = float(a[a.index("--to") + 1]) if "--to" in a else END
    stills = a[a.index("--stills") + 1] if "--stills" in a else None
    if stills:
        os.makedirs(stills, exist_ok=True)
    edl, clips = build()
    json.dump({k: round(v, 3) for k, v in T.items()}, open(f"{ROOT}/13_PROJECT_FILES/anchors.json", "w"), indent=1)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    n0, n1 = int(t_from * FPS), int(t_to * FPS)
    cur_clip = None
    for fi in range(n0, n1):
        t = fi / FPS
        for (a0, a1, fn, ck) in edl:
            if a0 <= t < a1:
                break
        if ck != cur_clip and cur_clip:
            clips[cur_clip].free()
        cur_clip = ck
        f, L = fn(t, fi)
        frame = Image.fromarray(finish(f, fi, 4.0, True)).convert("RGBA")
        frame.alpha_composite(L)
        C = Image.new("RGBA", (W, H))
        draw_captions(t, C)
        frame.alpha_composite(C)
        rgb = frame.convert("RGB")
        enc.stdin.write(rgb.tobytes())
        if stills and fi % 15 == 0:
            rgb.resize((W // 4, H // 4)).save(f"{stills}/f{fi:05d}.jpg", quality=82)
        if fi % 60 == 0:
            print(f"t={t:.1f}", file=sys.stderr, flush=True)
    enc.stdin.close()
    enc.wait()


if __name__ == "__main__":
    main()
