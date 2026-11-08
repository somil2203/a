"""Shared extras: Deepotsav diya tracker, prince silhouettes, moonless sky."""
import math
import random
import kd
from kd import W, H, GOLD, CREAM
from PIL import Image, ImageDraw, ImageFilter


def diya_icon(lit, glow=False, size=150):
    im = Image.new("RGBA", (size + 80, size + 120))
    d = ImageDraw.Draw(im)
    cx, cy = (size + 80) / 2, size * 0.9
    body = (196, 92, 40, 255) if lit else (110, 60, 40, 255)
    d.chord((cx - size / 2, cy - size * 0.45, cx + size / 2, cy + size * 0.45), 0, 180, fill=body)
    d.polygon([(cx + size / 2 - 6, cy), (cx + size / 2 + 26, cy - 14), (cx + size / 2 - 2, cy + 18)], fill=body)
    if lit or glow:
        fl = Image.new("RGBA", im.size)
        ImageDraw.Draw(fl).ellipse((cx + size / 2 - 4, cy - 70, cx + size / 2 + 26, cy + 2), fill=(255, 200, 90, 255 if lit else 90))
        im.alpha_composite(fl.filter(ImageFilter.GaussianBlur(10)))
        im.alpha_composite(fl.filter(ImageFilter.GaussianBlur(2)))
    return im


def five_diyas(ts, lit_n, y=1060, x0=30, step=206, size=150):
    names = ["DHANTERAS", "CHHOTI\nDIWALI", "LAKSHMI\nPUJA", "GOVARDHAN", "BHAI\nDOOJ"]

    def f(base, t, sc):
        if t < ts:
            return
        for i, n in enumerate(names):
            k = kd.eo((t - ts - i * 0.12) / 0.3)
            if k <= 0:
                continue
            ic = diya_icon(i < lit_n, glow=(i == lit_n and math.sin(t * 6) > -0.2), size=size)
            x = x0 + i * step
            kd.paste_fade(base, ic, (x, y + 20 * (1 - k)), k)
            for j, ln in enumerate(n.split("\n")):
                lab = kd.text_img(ln, "mono", 24, GOLD if i < lit_n else (200, 180, 160))
                kd.paste_fade(base, lab, (x + ic.width / 2 - lab.width / 2, y + size * 1.27 + j * 30), k)
    return f


def two_princes(ts, cx=540, y=1150, h=360, color=(14, 8, 6), glow=(255, 214, 140)):
    """Nalakubara and Manigriva as crowned silhouettes with folded hands, stepping out of light."""
    def one(d, x, s):
        P = lambda px, py: (x + px * s, y + py * s)
        d.ellipse((*P(-30, 20), *P(30, 82)), fill=color)
        d.polygon([P(-26, 26), P(-18, -10), P(-6, 14), P(0, -22), P(6, 14), P(18, -10), P(26, 26)], fill=color)  # crown
        d.polygon([P(-34, 84), P(34, 84), P(56, 250), P(-56, 250)], fill=color)
        d.rectangle((*P(-40, 245), *P(-12, 360)), fill=color)
        d.rectangle((*P(12, 245), *P(40, 360)), fill=color)
        d.polygon([P(-30, 100), P(-6, 150), P(6, 150), P(30, 100), P(0, 128)], fill=color)  # folded hands

    def f(base, t, sc):
        if t < ts:
            return
        k = kd.eo((t - ts) / 0.8)
        g = Image.new("RGBA", (W, H))
        gd = ImageDraw.Draw(g)
        r = 360 * k
        gd.ellipse((cx - r, y + 120 - r, cx + r, y + 120 + r), fill=(*glow, int(140 * k)))
        base.alpha_composite(g.filter(ImageFilter.GaussianBlur(70)))
        lay = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(lay)
        s = h / 360
        one(d, cx - 120, s)
        one(d, cx + 120, s)
        kd.paste_fade(base, lay, (0, 30 * (1 - k)), k)
    return f


def BG_amavasya(seed=9):
    """Moonless night: deep sky, sparse stars, and the empty place where the moon would be."""
    import numpy as np
    rng = random.Random(seed)
    y = np.linspace(0, 1, H)[:, None, None]
    a = np.array([6, 6, 18]) * (1 - y) + np.array([22, 12, 30]) * y
    sky = Image.fromarray(np.repeat(a, W, 1).astype("uint8")).convert("RGBA")
    d = ImageDraw.Draw(sky)
    for _ in range(260):
        x, yy, r = rng.random() * W, rng.random() * H * 0.8, rng.choice([1, 1, 1.5, 2])
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(255, 245, 225, rng.randint(90, 230)))
    sky = sky.filter(ImageFilter.GaussianBlur(0.5))

    def f(lt, fr, fi):
        im = sky.copy()
        dd = ImageDraw.Draw(im)
        cx, cy, R = W * 0.68, H * 0.30, 150
        n = 44
        for i in range(n):  # dashed outline: the missing moon
            if i % 2:
                continue
            a0, a1 = 360 * i / n, 360 * (i + 1) / n
            dd.arc((cx - R, cy - R, cx + R, cy + R), a0 + lt * 4, a1 + lt * 4, fill=(220, 210, 255, 120), width=3)
        return im.convert("RGB")
    return f
