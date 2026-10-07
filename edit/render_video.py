"""Render the graphics/caption/camera pass of the Nokia Short to a silent MP4.

usage: python3 render_video.py SRC.mp4 OUT.mp4 [--frames a:b] [--stills dir]
"""
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import timeline as TL

W, H = 1080, 1920
SW, SH = 1620, 2880
FPS = TL.FPS
A = TL.A
HERE = os.path.dirname(os.path.abspath(__file__))
FX, FY = 0.47, 0.42  # face centre in source (normalised)

FONTS = {
    "anton": f"{HERE}/fonts/anton.woff",
    "black": "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
    "bold": "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
    "mono": f"{HERE}/fonts/jbm.woff",
}
YELLOW = (255, 212, 0, 255)
RED = (255, 64, 64, 255)
GREEN = (60, 220, 120, 255)
BLUE = (70, 150, 255, 255)
WHITE = (255, 255, 255, 255)

PX0, PY0, PX1, PY1 = 90, 1215, 910, 1545  # lower graphics panel
PCX, PCY = (PX0 + PX1) // 2, (PY0 + PY1) // 2
CAP_Y = 1120


# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lin(t, a, b):
    if b <= a:
        return float(t >= a)
    return clamp((t - a) / (b - a))


def eo(x):
    return 1 - (1 - x) ** 3


def eio(x):
    return x * x * (3 - 2 * x)


def eback(x, s=1.9):
    x = clamp(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


@lru_cache(None)
def font(k, s):
    return ImageFont.truetype(FONTS[k], s)


@lru_cache(1024)
def text_img(txt, fk, size, fill=WHITE, stroke=0, stroke_fill=(0, 0, 0, 255), shadow=0):
    f = font(fk, size)
    bb = f.getbbox(txt, stroke_width=stroke)
    pad = stroke + shadow * 3 + 4
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    im = Image.new("RGBA", (w, h))
    ImageDraw.Draw(im).text((pad - bb[0], pad - bb[1]), txt, font=f, fill=fill,
                            stroke_width=stroke, stroke_fill=stroke_fill)
    if shadow:
        a = im.getchannel("A").filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: int(v * 0.75))
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 255))
        sh.putalpha(a)
        out = Image.new("RGBA", (w, h))
        out.alpha_composite(sh, (0, min(shadow, pad // 2)))
        out.alpha_composite(im)
        return out
    return im


def with_alpha(img, alpha):
    if alpha >= 0.999:
        return img
    img = img.copy()
    img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
    return img


def put(layer, img, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if img is None or alpha <= 0.004 or scale <= 0.01:
        return
    if abs(scale - 1) > 1e-3:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BICUBIC)
    if rot:
        img = img.rotate(rot, Image.BICUBIC, expand=True)
    img = with_alpha(img, alpha)
    x, y = int(round(cx - img.width / 2)), int(round(cy - img.height / 2))
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(layer.width, x + img.width), min(layer.height, y + img.height)
    if x1 <= x0 or y1 <= y0:
        return
    layer.alpha_composite(img.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))


def vgrad(size, top, bot):
    w, h = size
    t = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(top)[None, None, :] * (1 - t) + np.array(bot)[None, None, :] * t)
    arr = np.repeat(arr, w, axis=1).astype(np.uint8)
    return Image.fromarray(arr, "RGB" if len(top) == 3 else "RGBA")


def rr_mask(size, r, box=None):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box or (0, 0, size[0] - 1, size[1] - 1), radius=r, fill=255)
    return m


def glow(img, radius, color, strength=1.0):
    a = img.getchannel("A").filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(min(255, v * strength)))
    g = Image.new("RGBA", img.size, color[:3] + (255,))
    g.putalpha(a)
    return g


def padded(img, p):
    out = Image.new("RGBA", (img.width + 2 * p, img.height + 2 * p))
    out.alpha_composite(img, (p, p))
    return out


# ---------------------------------------------------------------- assets
def make_nokia(w=220, h=520):
    body = vgrad((w, h), (64, 84, 120), (24, 32, 52)).convert("RGBA")
    body.putalpha(rr_mask((w, h), 70))
    d = ImageDraw.Draw(body)
    d.rounded_rectangle((8, 8, w - 9, h - 9), radius=64, outline=(110, 130, 170, 255), width=3)
    d.rounded_rectangle((w * .36, 26, w * .64, 34), radius=4, fill=(10, 12, 20, 255))
    t = text_img("NOKIA", "black", 24, (235, 240, 255, 255))
    body.alpha_composite(t, (int(w / 2 - t.width / 2), 40))
    d.rounded_rectangle((24, 80, w - 25, 250), radius=18, fill=(30, 34, 40, 255))
    lcd = vgrad((w - 70, 140), (170, 196, 120), (130, 160, 92)).convert("RGBA")
    ld = ImageDraw.Draw(lcd)
    for i in range(4):
        ld.rectangle((8, 100 - i * 18, 8 + 6 + i * 3, 108 - i * 18), fill=(40, 60, 30, 255))
        ld.rectangle((lcd.width - 22, 100 - i * 18, lcd.width - 8, 108 - i * 18), fill=(40, 60, 30, 255))
    tt = text_img("12:07", "mono", 30, (40, 60, 30, 255))
    lcd.alpha_composite(tt, (lcd.width // 2 - tt.width // 2, 48))
    body.alpha_composite(lcd, (35, 95))
    d.ellipse((w * .16, 268, w * .84, 330), fill=(176, 190, 212, 255), outline=(120, 135, 160, 255), width=3)
    d.line((w * .5, 274, w * .5, 324), fill=(120, 135, 160, 255), width=3)
    for r in range(4):
        for c in range(3):
            x = 34 + c * (w - 68) / 3 + 6
            y = 350 + r * 40
            d.ellipse((x, y, x + (w - 68) / 3 - 12, y + 28), fill=(210, 214, 222, 255))
    hl = vgrad((w, h), (255, 255, 255, 70), (255, 255, 255, 0))
    m = rr_mask((w, h), 70)
    hlm = Image.new("L", (w, h))
    ImageDraw.Draw(hlm).rectangle((0, 0, w * .35, h), fill=255)
    hl.putalpha(Image.fromarray(np.minimum(np.array(hl.getchannel("A")), np.minimum(np.array(m), np.array(hlm)))))
    body.alpha_composite(hl)
    return body


def make_nokia_back(w=220, h=520):
    b = vgrad((w, h), (44, 60, 92), (18, 24, 40)).convert("RGBA")
    b.putalpha(rr_mask((w, h), 70))
    t = text_img("NOKIA", "black", 30, (120, 140, 180, 255))
    b.alpha_composite(t, (w // 2 - t.width // 2, h // 2))
    return b


def make_iphone(w=250, h=480):
    body = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(body)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=40, fill=(200, 200, 206, 255))
    d.rounded_rectangle((5, 5, w - 6, h - 6), radius=36, fill=(10, 10, 12, 255))
    sx0, sy0, sx1, sy1 = 20, 64, w - 20, h - 76
    scr = vgrad((sx1 - sx0, sy1 - sy0), (30, 60, 140), (120, 40, 140)).convert("RGBA")
    sd = ImageDraw.Draw(scr)
    cols = [(255, 90, 80), (90, 200, 120), (255, 190, 60), (80, 160, 255), (240, 240, 245),
            (255, 120, 180), (120, 220, 230), (170, 120, 255)]
    gs = (scr.width - 30) / 4
    for r in range(4):
        for c in range(4):
            x, y = 12 + c * gs, 34 + r * (gs + 14)
            sd.rounded_rectangle((x + 4, y, x + gs - 6, y + gs - 10), radius=10, fill=cols[(r * 4 + c) % 8] + (255,))
    sd.text((scr.width // 2 - 20, 6), "9:41", font=font("bold", 18), fill=WHITE)
    body.alpha_composite(scr, (sx0, sy0))
    d.rounded_rectangle((w * .4, 30, w * .6, 36), radius=3, fill=(60, 60, 66, 255))
    d.ellipse((w / 2 - 22, h - 60, w / 2 + 22, h - 16), fill=(24, 24, 28, 255), outline=(70, 70, 78, 255), width=3)
    d.rounded_rectangle((w / 2 - 8, h - 46, w / 2 + 8, h - 30), radius=3, outline=(110, 110, 118, 255), width=2)
    gl = Image.new("RGBA", (w, h))
    ImageDraw.Draw(gl).polygon([(0, 0), (w * .75, 0), (0, h * .55)], fill=(255, 255, 255, 34))
    gl.putalpha(Image.fromarray(np.minimum(np.array(gl.getchannel("A")), np.array(rr_mask((w, h), 40)))))
    body.alpha_composite(gl)
    return body


def make_house(lit):
    w, h = 104, 96
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    wall = (92, 104, 130, 255) if not lit else (120, 128, 150, 255)
    d.polygon([(6, 44), (52, 6), (98, 44)], fill=(150, 70, 60, 255) if lit else (90, 70, 70, 255))
    d.rectangle((16, 42, 88, 94), fill=wall)
    wc = (255, 206, 90, 255) if lit else (40, 46, 60, 255)
    d.rectangle((26, 54, 46, 72), fill=wc)
    d.rectangle((60, 60, 78, 94), fill=(60, 50, 50, 255))
    if lit:
        g = glow(im.crop((0, 0, w, h)), 8, (255, 200, 80), 0.6)
        out = Image.new("RGBA", (w, h))
        out.alpha_composite(g)
        out.alpha_composite(im)
        return out
    return im


def make_battery(level, w=380, h=170, color=GREEN):
    im = Image.new("RGBA", (w + 24, h))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h - 1), radius=26, outline=(240, 240, 245, 255), width=10)
    d.rounded_rectangle((w + 4, h * .32, w + 22, h * .68), radius=6, fill=(240, 240, 245, 255))
    n = 4
    gap = 12
    bw = (w - 40 - gap * (n - 1)) / n
    for i in range(n):
        if level * n > i + 0.01:
            x = 20 + i * (bw + gap)
            d.rounded_rectangle((x, 20, x + bw, h - 21), radius=8, fill=color)
    return im


def make_stamp(text, color, size=110, rot=-12, seed=1):
    t = text_img(text, "anton", size, color)
    pw, ph = t.width + 60, t.height + 30
    im = Image.new("RGBA", (pw, ph))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, pw - 5, ph - 5), radius=18, outline=color, width=10)
    im.alpha_composite(t, (30, 15))
    rng = np.random.default_rng(seed)
    a = np.array(im.getchannel("A")).astype(np.float32)
    noise = rng.random(a.shape)
    noise = np.array(Image.fromarray((noise * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))) / 255
    a *= np.clip((noise - 0.25) * 3.0, 0.35, 1.0)
    im.putalpha(Image.fromarray(a.astype(np.uint8)))
    return im.rotate(rot, Image.BICUBIC, expand=True)


def make_chip(text, accent, size=34):
    t = text_img(text, "bold", size, WHITE)
    w, h = t.width + 64, t.height + 26
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(14, 16, 24, 225), outline=accent[:3] + (200,), width=3)
    d.ellipse((20, h / 2 - 7, 34, h / 2 + 7), fill=accent)
    im.alpha_composite(t, (44, 13))
    return im


def make_3d_text(txt, size, front=(255, 212, 0), side=(150, 95, 0), depth=16):
    f = text_img(txt, "anton", size, front + (255,))
    s = text_img(txt, "anton", size, side + (255,))
    pad = depth + 30
    im = Image.new("RGBA", (f.width + 2 * pad, f.height + 2 * pad))
    sh = glow(padded(f, 0), 18, (0, 0, 0), 1.0)
    im.alpha_composite(sh, (pad + depth, pad + depth + 10))
    for i in range(depth, 0, -1):
        k = 0.6 + 0.4 * (1 - i / depth)
        layer = s if i > 1 else s
        if k < 1:
            layer = Image.eval(s, lambda v: v)  # same image, darkening via alpha mix below
        im.alpha_composite(layer, (pad + i, pad + i))
    im.alpha_composite(f, (pad, pad))
    return im


def make_receipt(lines_shown, total_shown):
    w, h = 470, 300
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    pts = [(0, 0), (w, 0), (w, h - 16)]
    for i in range(12, -1, -1):
        pts.append((i * w / 12, h - (16 if i % 2 == 0 else 0)))
    d.polygon(pts, fill=(246, 244, 236, 255))
    hdr = text_img("REPAIR BILL", "mono", 34, (30, 30, 30, 255))
    im.alpha_composite(hdr, (w // 2 - hdr.width // 2, 14))
    d.line((24, 66, w - 24, 66), fill=(30, 30, 30, 255), width=2)
    items = ["SCREEN", "BATTERY", "BODY"]
    for i, it in enumerate(items[:lines_shown]):
        a = text_img(it, "mono", 28, (60, 60, 60, 255))
        b = text_img("₹0", "black", 30, (60, 60, 60, 255))
        y = 80 + i * 42
        im.alpha_composite(a, (28, y))
        im.alpha_composite(b, (w - 28 - b.width, y - 2))
        d.line((40 + a.width, y + 30, w - 40 - b.width, y + 30), fill=(170, 170, 170, 255), width=2)
    if total_shown:
        d.line((24, 212, w - 24, 212), fill=(30, 30, 30, 255), width=3)
        a = text_img("TOTAL", "mono", 34, (20, 20, 20, 255))
        b = text_img("₹0", "black", 52, (20, 160, 80, 255))
        im.alpha_composite(a, (28, 228))
        im.alpha_composite(b, (w - 28 - b.width, 216))
    return im


ASSET = {}


def assets():
    if ASSET:
        return ASSET
    ASSET["nokia"] = make_nokia()
    ASSET["nokia_back"] = make_nokia_back()
    ASSET["nokia_glow"] = padded(ASSET["nokia"], 40)
    ASSET["nokia_glow"] = glow(ASSET["nokia_glow"], 24, (90, 160, 255), 1.4)
    ASSET["iphone"] = make_iphone()
    ASSET["iphone_glow"] = glow(padded(ASSET["iphone"], 60), 40, (170, 210, 255), 1.6)
    ASSET["house0"] = make_house(False)
    ASSET["house1"] = make_house(True)
    mini = make_nokia().resize((26, 62), Image.LANCZOS)
    ASSET["mini"] = mini
    ASSET["mini_glow"] = glow(padded(mini, 14), 7, (90, 170, 255), 2.0)
    ASSET["sold"] = make_stamp("SOLD", (235, 40, 40, 255), 120, -12, 3)
    ASSET["unbreak"] = make_stamp("UNBREAKABLE", (255, 212, 0, 255), 76, -8, 5)
    ASSET["y2007"] = make_3d_text("2007", 230)
    ASSET["chip_2013"] = make_chip("2013: PHONE BUSINESS SOLD TO MICROSOFT", (255, 90, 80, 255), 30)
    ASSET["chip_no1"] = make_chip("WORLD'S #1 PHONE MAKER  ·  1998–2011", BLUE, 30)
    ASSET["chip_era"] = make_chip("THE NOKIA ERA", BLUE, 40)
    ASSET["chip_ip"] = make_chip("9 JAN 2007  ·  iPHONE ANNOUNCED", (200, 220, 255, 255), 30)
    ASSET["grain"] = [np.random.default_rng(i).normal(0, 1, (H // 2, W // 2)).astype(np.float32) for i in range(6)]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * .62)) ** 2 + ((yy - H * .42) / (H * .62)) ** 2)
    ASSET["vig"] = np.clip(1 - 0.55 * np.clip(r - 0.45, 0, None) ** 1.6, 0.35, 1)[..., None]
    x = np.linspace(0, 1, 256)
    curve = np.clip(0.5 + (x - 0.5) * 1.12 + 0.03 * np.sin(2 * np.pi * x), 0, 1)
    ASSET["lut"] = [np.clip(curve * 255 + o, 0, 255).astype(np.uint8)
                    for o in ((x * 6 - 2), (x * 2 - 1), (5 - x * 8))]
    return ASSET


# ---------------------------------------------------------------- 3D renders
R3D = os.environ.get("R3D", os.path.join(HERE, "r3d"))
CUTS = [  # name, t0, t1
    ("village", A["houses_in"], A["proof"]),
    ("battery", A["battery"], A["drop_start"] - 0.5),
    ("drop", A["drop_start"] - 0.5, A["receipt"]),
    ("iphone", A["y2007"], A["beat_hit"]),
]


@lru_cache(64)
def r3d(name, idx):
    d = os.path.join(R3D, name)
    files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    idx = max(0, min(len(files) - 1, idx))
    return Image.open(os.path.join(d, files[idx])).convert("RGBA")


def active_cut(t):
    for name, t0, t1 in CUTS:
        if t0 <= t < t1:
            return name, t0, t1
    return None


def cutaway_bg(name, t, t0, t1):
    idx = int(round((t - t0) * FPS))
    im = r3d(name, idx).convert("RGB")
    p = lin(t, t0, t1)
    z = (1.10 - 0.10 * eo(lin(t, t0, t0 + 0.25))) * (1 + 0.04 * p)
    sx = sy = 0.0
    for ts, amp in SHAKES:
        if t >= ts:
            k = amp * math.exp(-(t - ts) * 9)
            sx += k * math.sin((t - ts) * 71)
            sy += k * math.cos((t - ts) * 53)
    w, h = im.size
    k = (w / W) / z
    out = im.transform((W, H), Image.AFFINE, (k, 0, w / 2 - k * W / 2 + sx * k, 0, k, h / 2 - k * H / 2 + sy * k),
                       Image.BICUBIC)
    return out.filter(ImageFilter.UnsharpMask(2, 60, 2))


# ---------------------------------------------------------------- camera
SPANS = [  # t0, t1, z0, z1, face_oy
    (0.00, A["kyun"], 1.40, 1.52, .30),
    (A["kyun"], A["era"], 1.72, 1.84, .36),
    (A["era"], A["proof"], 1.30, 1.38, .30),
    (A["proof"], A["battery"], 1.55, 1.60, .30),
    (A["battery"], A["drop_start"] - 0.5, 1.30, 1.34, .30),
    (A["drop_start"] - 0.5, A["receipt"], 1.38, 1.42, .30),
    (A["receipt"], A["apple_seg"], 1.30, 1.34, .30),
    (A["apple_seg"], A["beat_hit"], 1.32, 1.64, .31),
    (A["beat_hit"], 99, 1.36, 1.42, .30),
]
SHAKES = [(A["stamp"], 16), (A["kyun"], 10), (A["drop_hit"], 26), (A["y2007"], 10), (A["beat_hit"], 22)]


def cam(t):
    for t0, t1, z0, z1, oy in SPANS:
        if t0 <= t < t1:
            z = z0 + (z1 - z0) * eio(lin(t, t0, min(t1, A["end"])))
            break
    sx = sy = 0.0
    for ts, amp in SHAKES:
        if t >= ts:
            k = amp * math.exp(-(t - ts) * 9)
            sx += k * math.sin((t - ts) * 71)
            sy += k * math.cos((t - ts) * 53)
    rot = 0.0
    if t >= A["flip_start"]:
        rot = 180 * eio(lin(t, A["flip_start"], A["flip_end"]))
    return z, oy, sx, sy, rot


def coverage(rot):
    th = math.radians(rot)
    return abs(math.cos(th)) + (H / W) * abs(math.sin(th))


def transform_src(src, z, oy, sx, sy, rot):
    cy = FY - (oy - 0.5) / z
    hw = 0.5 / z
    cx = clamp(FX, hw, 1 - hw) + sx / (W * z)
    cy = clamp(cy, hw, 1 - hw) + sy / (H * z)
    zz = z * coverage(rot)
    k = (SW / W) / zz
    th = math.radians(rot)
    c, s = math.cos(th), math.sin(th)
    a, b, d, e = k * c, k * s, -k * s, k * c
    Cx, Cy = cx * SW, cy * SH
    return src.transform((W, H), Image.AFFINE,
                         (a, b, Cx - a * W / 2 - b * H / 2, d, e, Cy - d * W / 2 - e * H / 2),
                         Image.BILINEAR)


def rotate_layer(layer, rot):
    if rot == 0:
        return layer
    s = coverage(rot)
    th = math.radians(rot)
    c, sn = math.cos(th), math.sin(th)
    k = 1 / s
    a, b, d, e = k * c, k * sn, -k * sn, k * c
    return layer.transform((W, H), Image.AFFINE,
                           (a, b, W / 2 - a * W / 2 - b * H / 2, d, e, H / 2 - d * W / 2 - e * H / 2),
                           Image.BILINEAR)


# ---------------------------------------------------------------- grade
def grade(img, t):
    as_ = assets()
    arr = np.asarray(img)
    out = np.empty_like(arr)
    for ch in range(3):
        out[..., ch] = as_["lut"][ch][arr[..., ch]]
    f = out.astype(np.float32)
    sat, dark, cool = 1.10, 0.0, 0.0
    if A["kyun"] <= t < A["era"]:
        sat, dark = 0.45, 0.18
    if A["era"] <= t < A["houses_in"]:
        sat, dark = 0.6, 0.55
    if A["apple_seg"] <= t < A["beat_hit"]:
        p = lin(t, A["apple_seg"], A["beat_hit"])
        sat, dark, cool = 1.10 - 0.45 * p, 0.28 * p, 0.35 * p
    lum = f @ np.array([0.299, 0.587, 0.114], np.float32)
    f = lum[..., None] + (f - lum[..., None]) * sat
    if cool:
        f += np.array([-14, 0, 18], np.float32) * cool
    f *= as_["vig"] * (1 - dark)
    return f


def finish(f, fi):
    g = assets()["grain"][fi % 6]
    g = np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None]
    f = f + g * 5.0
    return np.clip(f, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- panel
def panel_bg(world, layer, alpha, grow=1.0):
    if alpha <= 0:
        return
    x0, y0, x1, y1 = PX0, PY0, PX1, PY1
    cy = (y0 + y1) / 2
    hh = (y1 - y0) / 2 * (0.88 + 0.12 * grow)
    y0, y1 = int(cy - hh), int(cy + hh)
    crop = world.crop((x0, y0, x1, y1)).resize(((x1 - x0) // 8, (y1 - y0) // 8), Image.BILINEAR)
    crop = crop.filter(ImageFilter.GaussianBlur(3)).resize((x1 - x0, y1 - y0), Image.BILINEAR)
    arr = (np.asarray(crop).astype(np.float32) * 0.35 + np.array([8, 10, 18]) * 0.65).astype(np.uint8)
    p = Image.fromarray(arr).convert("RGBA")
    p.putalpha(rr_mask(p.size, 40).point(lambda v: int(v * alpha)))
    layer.alpha_composite(p, (x0, y0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x0, y0, x1 - 1, y1 - 1), radius=40, outline=(255, 255, 255, int(70 * alpha)), width=2)


def phone_spin(layer, img, back, cx, cy, ang, scale):
    c = math.cos(math.radians(ang))
    face = img if c >= 0 else back
    w = max(2, int(face.width * scale * max(abs(c), 0.04)))
    h = int(face.height * scale)
    f = face.resize((w, h), Image.BICUBIC)
    th = int(18 * scale * abs(math.sin(math.radians(ang))))
    if th > 1:
        side = Image.new("RGBA", (th, h), (20, 26, 40, 255))
        side.putalpha(rr_mask((th, h), min(th // 2, 30)))
        sx = cx + (w / 2 if math.sin(math.radians(ang)) * c > 0 else -w / 2 - th)
        put(layer, side, sx + th / 2, cy)
    put(layer, f, cx, cy)


def draw_panel(t, world, L):
    """Lower-panel graphics. L = RGBA layer that rotates with the world."""
    as_ = assets()
    # --- A: hook
    if t < A["kyun"]:
        a = eo(lin(t, 0.0, 0.18))
        panel_bg(world, L, a, a)
        sc = 0.56 * (0.7 + 0.3 * eback(lin(t, 0.0, 0.3)))
        ang = 360 * eo(lin(t, 0.0, 0.95)) + 8 * math.sin(t * 3)
        put(L, r3d("turntable", int(t * FPS)), 300, PCY, 0.62 * (0.7 + 0.3 * eback(lin(t, 0.0, 0.3))))
        ts = A["stamp"]
        if t >= ts:
            p = lin(t, ts, ts + 0.13)
            put(L, as_["sold"], 300, PCY, 2.3 - 1.3 * eo(p), clamp(p * 3))
        t2 = text_img("NOKIA", "anton", 96, WHITE)
        t3 = text_img("SOLD ITSELF?", "anton", 64, (255, 90, 80, 255))
        put(L, t2, 680, PCY - 52, 1, eo(lin(t, 0.15, 0.35)))
        put(L, t3, 680 + 30 * (1 - eo(lin(t, ts - 0.02, ts + 0.2))), PCY + 48, 1, eo(lin(t, ts - 0.02, ts + 0.2)))
        return
    if t < A["houses_in"]:
        return
    # --- C2: houses
    if t < A["proof"]:
        a = eo(lin(t, A["houses_in"], A["houses_in"] + 0.18))
        panel_bg(world, L, a, a)
        for k in range(12):
            r, c = divmod(k, 6)
            hx = PX0 + 85 + c * 130
            hy = PY0 + 112 + r * 150
            tl = A["houses_in"] + 0.25 + (c * 2 + r) * 0.045
            lit = t >= tl
            put(L, as_["house1" if lit else "house0"], hx, hy, 0.9 + 0.1 * eback(lin(t, A["houses_in"], A["houses_in"] + 0.25)), a)
            if lit:
                p = eback(lin(t, tl, tl + 0.18))
                pulse = 1.0
                if t >= A["nokia_word"]:
                    pulse = 1 + 0.28 * math.exp(-(t - A["nokia_word"]) * 6)
                    put(L, as_["mini_glow"], hx + 30, hy - 40, pulse, 0.9)
                put(L, as_["mini"], hx + 30, hy - 40, p * pulse)
        return
    # --- D: proof
    if t < A["apple_seg"]:
        panel_bg(world, L, 1.0)
        tb, td, tr = A["battery"], A["drop_start"] - 0.5, A["receipt"]
        if t < tb:  # hero phone
            p = eback(lin(t, A["proof"], A["proof"] + 0.25))
            put(L, r3d("nokia_still", 0), PCX, PCY, 0.62 * p)
            sw = lin(t, A["proof"] + 0.1, A["proof"] + 0.4)
            if 0 < sw < 1:
                g = Image.new("RGBA", (60, 400), (255, 255, 255, 90)).rotate(20, expand=True)
                gl = Image.new("RGBA", (W, H))
                put(gl, g, PCX - 140 + 280 * sw, PCY)
                m = Image.new("L", (W, H))
                m.paste(as_["nokia"].resize((int(220 * .58), int(520 * .58))).getchannel("A"),
                        (int(PCX - 220 * .58 / 2), int(PCY - 520 * .58 / 2)))
                gl.putalpha(Image.fromarray(np.minimum(np.asarray(gl.getchannel("A")), np.asarray(m))))
                L.alpha_composite(gl)
        elif t < td:  # battery
            p = eo(lin(t, tb, tb + 0.25))
            put(L, as_["nokia"], 230 - 60 * (1 - p), PCY + 10, 0.5)
            put(L, make_battery(1.0), 620, PCY + 20, 0.9 * (0.7 + 0.3 * eback(lin(t, tb, tb + 0.25))), p)
            day = 1 + int(clamp((t - (tb + 0.45)) / 0.32, 0, 6))
            dt = text_img(f"DAY {day}", "mono", 54, YELLOW)
            put(L, dt, 620, PY0 + 58, 1, p)
            lab = text_img("STILL 100%", "black", 36, GREEN)
            put(L, lab, 620, PY1 - 48, 1, eo(lin(t, tb + 0.9, tb + 1.1)))
        elif t < tr:  # drop test
            floor_y = PY1 - 40
            d = ImageDraw.Draw(L)
            fa = int(160 * eo(lin(t, td, td + 0.2)))
            for i in range(9):
                x = PX0 + 40 + i * 92
                d.line((x, floor_y, PCX + (x - PCX) * 1.6, PY1 - 4), fill=(200, 210, 230, fa // 2), width=2)
            d.line((PX0 + 20, floor_y, PX1 - 20, floor_y), fill=(220, 225, 240, fa), width=3)
            th = A["drop_hit"]
            sc = 0.42
            ph = 520 * sc
            rest_y = floor_y - ph / 2
            if t < A["drop_start"]:
                y = PY0 + 100 + 6 * math.sin(t * 14)
                rot = 6 * math.sin(t * 9)
            elif t < th:
                p = lin(t, A["drop_start"], th)
                y = PY0 + 100 + (rest_y - PY0 - 100) * p * p
                rot = 6 + 30 * p
            else:
                b = t - th
                y = rest_y - 60 * abs(math.sin(b * 9)) * math.exp(-b * 7)
                rot = 36 * math.exp(-b * 8) * math.cos(b * 10)
            if t >= th:
                k = eo(lin(t, th, th + 0.08))
                rng = np.random.default_rng(7)
                for j in range(9):
                    ang = math.pi + rng.random() * math.pi * 0.0 + (j / 8) * math.pi
                    ang = math.radians(rng.uniform(190, 350)) if j % 2 else math.radians(rng.uniform(0, 25) + 170 * (j % 3 == 0))
                    ln = rng.uniform(80, 260) * k
                    pts = [(PCX, floor_y)]
                    x, yy = PCX, floor_y
                    for s in range(4):
                        x += math.cos(ang) * ln / 4 + rng.uniform(-10, 10)
                        yy = floor_y + abs(math.sin(ang)) * ln / 4 * (s + 1) * 0.15
                        pts.append((x, min(yy, PY1 - 6)))
                    d.line(pts, fill=(255, 255, 255, 230), width=3)
            put(L, as_["nokia"], PCX, y, sc, 1, rot)
            if t >= th + 0.12:
                p = lin(t, th + 0.12, th + 0.25)
                put(L, as_["unbreak"], PCX, PY0 + 95, 2.0 - 1.0 * eo(p), clamp(p * 3))
        else:  # receipt
            p = eo(lin(t, tr, tr + 0.25))
            n = int(clamp((t - (tr + 0.3)) / 0.2, 0, 3))
            tot = t >= A["receipt_total"] - 0.1
            put(L, make_receipt(n, tot), PCX, PCY + 200 * (1 - p), 1.0, p)
            if t >= A["receipt_total"]:
                q = lin(t, A["receipt_total"], A["receipt_total"] + 0.12)
                put(L, make_stamp("FREE", (40, 200, 110, 255), 70, -14, 9), PCX + 230, PCY - 60, 1.8 - 0.8 * eo(q), clamp(q * 3))
        return
    # --- E: Apple
    if t < A["beat_hit"]:
        ta = A["apple_word"] - 0.05
        if t >= ta:
            p = eo(lin(t, ta, ta + 0.35))
            panel_bg(world, L, p, p)
            put(L, as_["iphone_glow"], 320, PCY + 220 * (1 - p), 0.62, p * (0.7 + 0.3 * math.sin(t * 6)))
            put(L, as_["iphone"], 320, PCY + 220 * (1 - p), 0.62)
            put(L, text_img("iPHONE", "anton", 92, WHITE), 670, PCY - 40, 1, eo(lin(t, ta + 0.1, ta + 0.3)))
            put(L, text_img("BY APPLE", "black", 34, (180, 200, 230, 255)), 670, PCY + 40, 1, eo(lin(t, ta + 0.18, ta + 0.38)))
        return
    # --- F: flip (VS)
    if t < A["end"]:
        tb = A["beat_hit"]
        panel_bg(world, L, 1.0)
        p = eo(lin(t, tb, tb + 0.6))
        nk = r3d("nokia_still", 0)
        gray = Image.merge("RGBA", (*(nk.convert("L"),) * 3, nk.getchannel("A")))
        put(L, nk, 260, PCY + 40 * p, 0.62, 1 - 0.7 * p, -18 * p)
        put(L, gray, 260, PCY + 40 * p, 0.62, 0.7 * p, -18 * p)
        put(L, as_["iphone_glow"], 560, PCY - 20 * p, 0.6, 0.5)
        put(L, r3d("iphone_still", 0), 560, PCY - 20 * p, 0.66)
        put(L, text_img("↓", "black", 120, RED), 140, PCY, 1, p)
        put(L, text_img("↑", "black", 120, GREEN), 760, PCY, 1, p)
        return


def draw_cut_overlay(name, t, t0, L):
    as_ = assets()
    if name == "battery":
        tb = A["battery"]
        day = 1 + int(clamp((t - (tb + 0.45)) / 0.3, 0, 5))
        put(L, make_chip(f"DAY {day}", YELLOW, 52), 540, 300, 1, eo(lin(t, tb + 0.2, tb + 0.4)))
        put(L, text_img("BATTERY: STILL 100%", "black", 56, GREEN, 6, (0, 0, 0, 255), 6), 540, 1500, 1,
            eo(lin(t, tb + 0.9, tb + 1.1)))
    if name == "drop":
        th = A["drop_hit"]
        if t >= th + 0.1:
            p = lin(t, th + 0.1, th + 0.24)
            put(L, as_["unbreak"], 540, 1450, (2.0 - 1.0 * eo(p)) * 1.3, clamp(p * 3))
    if name == "iphone":
        if t >= A["apple_word"] + 0.25:
            p = eo(lin(t, A["apple_word"] + 0.25, A["apple_word"] + 0.45))
            put(L, as_["chip_ip"], 540, 590, 1.1, p)


def draw_top(t, L):
    """Top-of-frame facts and big type (also rotates with the world)."""
    as_ = assets()
    ts = A["stamp"]
    if ts + 0.15 <= t < A["kyun"]:
        p = eo(lin(t, ts + 0.15, ts + 0.35))
        put(L, as_["chip_2013"], 540, 190 - 30 * (1 - p), 1, p)
    if A["era"] <= t < A["houses_in"]:
        lt = t - A["era"]
        p = eback(lin(lt, 0, 0.16))
        yr = 2007 - int(clamp((lt - 0.12) / 0.06, 0, 9))
        put(L, make_3d_text_cached(str(yr)), 540, 620, 1.3 - 0.3 * p, clamp(lt * 8))
        put(L, text_img("◀◀  REWIND", "black", 46, (200, 210, 230, 255)), 540, 380, 1, eo(lin(lt, 0.05, 0.2)))
        put(L, as_["chip_era"], 540, 860, 0.8 + 0.2 * eback(lin(lt, 0.5, 0.7)), eo(lin(lt, 0.5, 0.65)))
        # timeline ruler
        d = ImageDraw.Draw(L)
        off = 600 * eo(lin(lt, 0, 0.75))
        for i, y in enumerate(range(1998, 2010)):
            x = 540 + (y - 2007) * 150 + off
            if -50 < x < W + 50:
                col = (255, 212, 0, 255) if y == 2007 else ((90, 160, 255, 255) if y < 2007 else (120, 120, 130, 255))
                d.line((x, 980, x, 1010), fill=col, width=4)
                tt = text_img(str(y), "mono", 30, col)
                put(L, tt, x, 1040)
        d.line((0, 995, W, 995), fill=(200, 210, 230, 160), width=2)
    if A["houses_in"] + 0.9 <= t < A["proof"] and t >= A["nokia_word"] + 0.1:
        p = eo(lin(t, A["nokia_word"] + 0.1, A["nokia_word"] + 0.3))
        put(L, as_["chip_no1"], 540, 190 - 30 * (1 - p), 1, p)
    if A["y2007"] <= t < A["y2007"]:
        p = lin(t, A["y2007"], A["y2007"] + 0.14)
        sc = (2.0 - 1.0 * eo(p)) * (1 + 0.04 * lin(t, A["y2007"], A["beat_hit"]))
        put(L, as_["y2007"], 540, 250, sc * 0.85, clamp(p * 3))

    if A["beat_hit"] + 0.1 <= t < A["flip_start"] + 0.1:
        p = eback(lin(t, A["beat_hit"] + 0.1, A["beat_hit"] + 0.3))
        put(L, text_img("GAME CHANGED", "anton", 120, WHITE, 0, (0, 0, 0, 255), 8), 540, 230, p)


@lru_cache(16)
def make_3d_text_cached(s):
    return make_3d_text(s, 230)


def draw_kyun(t, L):
    if A["kyun"] <= t < A["era"]:
        lt = t - A["kyun"]
        p = eback(lin(lt, 0, 0.14), 2.4)
        sc = (1.8 - 0.8 * p) * (1 + 0.08 * lt)
        img = text_img("KYUN?", "anton", 260, YELLOW, 10, (0, 0, 0, 255), 10)
        put(L, glow(padded(img, 30), 30, (255, 200, 0), 0.8), 540, 1430, sc, 0.6)
        put(L, img, 540, 1430, sc, clamp(lt * 10))


# ---------------------------------------------------------------- captions
PAGES = TL.caption_pages()
STYLE_COL = {None: WHITE, "hl": YELLOW, "red": RED, "apple": (220, 235, 255, 255)}


def draw_captions(t, L):
    if A["kyun"] <= t < A["era"] or t >= A["end"]:
        return
    for s, e, words in PAGES:
        if not (s <= t < e):
            continue
        size = 84
        imgs = []
        for txt, ws, we, st in words:
            active = ws <= t < we + 0.05
            col = (YELLOW if st is None else STYLE_COL[st]) if active else STYLE_COL[st]
            imgs.append(text_img(txt, "black", size, col, 9, (0, 0, 0, 255), 6))
        gap = 18
        total = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
        k = min(1.0, 900 / total)
        x = 520 - total * k / 2
        for img, (txt, ws, we, st) in zip(imgs, words):
            w = img.width * k
            if t >= ws - 0.02:
                p = lin(t, ws - 0.02, ws + 0.1)
                sc = k * (0.6 + 0.4 * eback(p))
                if ws <= t < we:
                    sc *= 1.08
                cy = 1580 if A["y2007"] <= t < A["beat_hit"] else CAP_Y
                put(L, img, x + w / 2, cy + 14 * (1 - eo(p)), sc, clamp(p * 2.5))
            x += w + gap * k
        return


def draw_end(t, frozen, fi):
    lt = t - A["end"]
    p = eo(lin(lt, 0, 0.35))
    sm = frozen.resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1 + 3 * p)).resize((W, H), Image.BILINEAR)
    base = Image.blend(frozen, sm, p)
    f = np.asarray(base).astype(np.float32) * (1 - 0.55 * p)
    img = Image.fromarray(finish(f, fi)).convert("RGBA")
    L = Image.new("RGBA", (W, H))
    put(L, text_img("TO NOKIA SE", "black", 70, WHITE, 0, (0, 0, 0, 255), 6), 540, 800, 1, eo(lin(lt, 0.05, 0.25)))
    q = eback(lin(lt, 0.15, 0.35))
    put(L, text_img("GALTI KAHAN", "anton", 150, YELLOW, 0, (0, 0, 0, 255), 8), 540, 930, 0.8 + 0.2 * q, clamp(q * 2))
    q2 = eback(lin(lt, 0.25, 0.45))
    put(L, text_img("HUI?", "anton", 150, YELLOW, 0, (0, 0, 0, 255), 8), 540, 1100, 0.8 + 0.2 * q2, clamp(q2 * 2))
    put(L, make_chip("COMMENT MEIN BATAO  ↓", YELLOW, 38), 540, 1290, 1, eo(lin(lt, 0.5, 0.7)))
    img.alpha_composite(L)
    return img.convert("RGB")


# ---------------------------------------------------------------- frames
def src_frames(src):
    fb = SW * SH * 3
    for (a, b, _), nf in zip(TL.EDL, TL.NF):
        cmd = ["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-i", src, "-t", f"{nf / FPS + 0.2:.3f}",
               "-vf", f"fps={FPS},scale={SW}:{SH}:flags=lanczos", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        last = None
        for _ in range(nf):
            buf = p.stdout.read(fb)
            if len(buf) < fb:
                buf = last
            last = buf
            yield Image.frombuffer("RGB", (SW, SH), buf, "raw", "RGB", 0, 1)
        p.kill()
        p.wait()


def compose(src, t, fi):
    cut = active_cut(t)
    if cut:
        bg = cutaway_bg(cut[0], t, cut[1], cut[2])
        f = np.asarray(bg).astype(np.float32) * assets()["vig"]
        lt = t - cut[1]
        if lt < 0.1:  # flash-cut into the 3D shot
            f = f + 120 * (1 - lt / 0.1)
        world = Image.fromarray(finish(f, fi)).convert("RGBA")
        L = Image.new("RGBA", (W, H))
        draw_cut_overlay(cut[0], t, cut[1], L)
        draw_top(t, L)
        world.alpha_composite(L)
        return world
    z, oy, sx, sy, rot = cam(t)
    bg = transform_src(src, z, oy, 0, 0, 0) if rot == 0 else None
    if rot == 0:
        bg = transform_src(src, z, oy, sx, sy, 0)
    else:
        bg = transform_src(src, z, oy, sx, sy, rot)
    if A["era"] <= t < A["houses_in"]:
        bg = bg.resize((W // 8, H // 8), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)
    f = grade(bg, t)
    if A["beat_hit"] <= t < A["beat_hit"] + 0.2:
        f = f + 255 * 0.85 * (1 - lin(t, A["beat_hit"], A["beat_hit"] + 0.2)) ** 2
    world = Image.fromarray(finish(f, fi)).convert("RGBA")
    L = Image.new("RGBA", (W, H))
    draw_panel(t, world.convert("RGB") if rot == 0 else world.convert("RGB"), L)
    draw_top(t, L)
    if rot:
        L = rotate_layer(L, rot)
    world.alpha_composite(L)
    K = Image.new("RGBA", (W, H))
    draw_kyun(t, K)
    world.alpha_composite(K)
    return world


def main():
    src_path, out_path = sys.argv[1], sys.argv[2]
    fr = (0, TL.TOTAL_FRAMES)
    stills = None
    if "--frames" in sys.argv:
        a, b = sys.argv[sys.argv.index("--frames") + 1].split(":")
        fr = (int(a), int(b))
    if "--stills" in sys.argv:
        stills = sys.argv[sys.argv.index("--stills") + 1]
        os.makedirs(stills, exist_ok=True)
    assets()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                            "-pix_fmt", "yuv420p", out_path], stdin=subprocess.PIPE)
    frozen = None
    gen = src_frames(src_path)
    for fi in range(TL.TOTAL_FRAMES):
        t = fi / FPS
        if fi < TL.VOICE_FRAMES:
            src = next(gen)
            if fi < fr[0]:
                continue
            _, _, _, _, rot = cam(t)
            if 0 < rot < 180:  # motion blur on the flip
                acc = None
                for k in range(4):
                    im = compose(src, t + k / (4 * FPS), fi)
                    a = np.asarray(im.convert("RGB")).astype(np.float32)
                    acc = a if acc is None else acc + a
                frame = Image.fromarray((acc / 4).astype(np.uint8)).convert("RGBA")
            else:
                frame = compose(src, t, fi)
            frozen = frame.convert("RGB")
            C = Image.new("RGBA", (W, H))
            draw_captions(t, C)
            frame.alpha_composite(C)
            out = frame.convert("RGB")
        else:
            if frozen is None:
                continue
            out = draw_end(t, frozen, fi)
        if fi >= fr[1]:
            break
        if fi >= fr[0]:
            enc.stdin.write(out.tobytes())
            if stills and fi % 15 == 0:
                out.resize((W // 3, H // 3)).save(f"{stills}/f{fi:04d}.jpg", quality=85)
            if fi % 30 == 0:
                print("frame", fi, file=sys.stderr, flush=True)
    enc.stdin.close()
    enc.wait()


if __name__ == "__main__":
    main()
