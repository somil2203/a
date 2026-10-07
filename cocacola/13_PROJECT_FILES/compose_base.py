"""Coca-Cola Short compositor: shots + motion graphics + captions + grade -> silent 1080x1920 30fps.

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
END = 54.6
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


