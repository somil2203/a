"""Coca-Cola Short: shots + maps + motion graphics + captions + grade -> silent 1080x1920 30 fps.

usage: python3 compose.py OUT.mp4 [--from S] [--to S] [--stills DIR]
Shared helpers (grading, VideoClip, text, captions primitives) live in compose_base.py.
"""
import json
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from compose_base import (ACCENT, B, CYAN, DIM, END, FPS, GOLD, GREEN, H, P, ROOT, VIG, W, WHITE, VideoClip, chip,
                          clamp, cover, eback, eio, eo, finish, font, glow, grade, lin, pad_img, photo,
                          put, rr, seq_frame, text_img, with_alpha)

def grid_bg(t, tint=(10, 14, 24), line=(40, 70, 110), spacing=90, drift=12):
    im = Image.new("RGB", (W, H), tint)
    d = ImageDraw.Draw(im)
    off = (t * drift) % spacing
    for x in range(-spacing, W + spacing, spacing):
        d.line((x + off, 0, x + off, H), fill=line, width=1)
    for y in range(-spacing, H + spacing, spacing):
        d.line((0, y + off, W, y + off), fill=line, width=1)
    return im


def label(L, t, t0, text, y=300, accent=CYAN, size=36):
    p = eo(lin(t, t0, t0 + 0.25))
    put(L, chip(text, accent, size), W / 2, y - 24 * (1 - p), 1.0, p)


A = f"{ROOT}/06_ARCHIVE"


def bpath(vid):
    """B-roll file by Mixkit id (download names are truncated)"""
    hits = [f for f in os.listdir(B) if f.startswith(f"mixkit_{vid}_")]
    return f"{B}/{hits[0]}"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
CREAM = (238, 226, 196, 255)
COKE_RED = (205, 30, 40, 255)
LEAF = (120, 200, 110, 255)
NUT = (205, 150, 90, 255)


@lru_cache(None)
def serif(size):
    from PIL import ImageFont
    return ImageFont.truetype(SERIF, size)


def serif_text(txt, size, fill=CREAM, shadow=6):
    f = serif(size)
    bb = f.getbbox(txt)
    im = Image.new("RGBA", (bb[2] - bb[0] + 20 + 4 * shadow, bb[3] + 20 + 4 * shadow))
    d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", im.size)
        ImageDraw.Draw(sh).text((10 + 2 * shadow - bb[0], 10 + 2 * shadow + 3), txt, font=f, fill=(0, 0, 0, 220))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(shadow)))
    d.text((10 + 2 * shadow - bb[0], 10 + 2 * shadow), txt, font=f, fill=fill)
    return im


def credit(L, text, y=1840):
    put(L, text_img(text, "reg", 22, (215, 215, 220, 210)), W / 2, y, 1, 0.9)


@lru_cache(4)
def archive(name, mode="RGB"):
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(f"{A}/{name}").convert(mode)
    if max(im.size) > 3000:
        im.thumbnail((3000, 3000), Image.LANCZOS)
    return im


# ------------------------------------------------------------------ words / captions
WORDS = json.load(open(f"{ROOT}/11_CAPTIONS/words_master.json"))
_w = []
for i, (t, s, e) in enumerate(WORDS):
    if t in ("...", "…"):
        continue
    if t.startswith("-") and _w:
        _w[-1][0] += t
        continue
    _w.append([t, s, e])
for i, w in enumerate(_w):  # "cola nuts" -> "kola nuts" (the nut is spelled kola)
    if w[0].lower() == "cola" and i + 1 < len(_w) and _w[i + 1][0].lower().startswith("nuts"):
        w[0] = "kola"
    if w[0] == "Coca" and i + 1 < len(_w) and _w[i + 1][0] == "Cola" and w[1] > 39:
        w[0] = "Coca-Cola"
        _w[i + 1][0] = ""
_w = [w for w in _w if w[0]]
for i in range(len(_w)):
    nxt = _w[i + 1][1] if i + 1 < len(_w) else _w[i][1] + 0.6
    _w[i][2] = min(nxt, _w[i][1] + 0.7)
WORDS = _w


def wt(word, after=0.0):
    for t, s, e in WORDS:
        if s >= after and t.lower().strip(",.?!").startswith(word.lower()):
            return s
    raise KeyError(word)


EMPH = {"coca-cola": COKE_RED, "cocaine": ACCENT, "joke.": GOLD, "1886,": GOLD, "atlanta.": GOLD, "pemberton": GOLD,
        "morphine": ACCENT, "addiction,": ACCENT, "cure.": CYAN, "medicine": GOLD, "two": GOLD, "coca": LEAF,
        "leaves": LEAF, "kola": NUT, "nuts.": NUT, "cola.": NUT, "energy,": GREEN, "headaches,": GREEN,
        "amazing.": GREEN, "crazy": ACCENT, "1903,": GOLD, "fear": ACCENT, "removed": ACCENT, "cocaine.": ACCENT,
        "never": ACCENT, "extract,": CYAN, "out,": ACCENT, "new": GOLD, "jersey.": GOLD, "coke,": COKE_RED,
        "name": GOLD, "came": GOLD, "from.": GOLD, "leaf": LEAF}
PAGES, cur = [], []
for w in WORDS:
    cur.append(w)
    if w[0][-1] in ".?!," or len(cur) >= 3:
        PAGES.append(cur)
        cur = []
if cur:
    PAGES.append(cur)
NO_CAPS = []


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
            col = EMPH.get(txt.lower(), WHITE)
            imgs.append((text_img(txt.upper(), "black", 70, col, 0, (0, 0, 0, 255), 7), ws, we, ws <= t < we))
        gap = 20
        tw = sum(i[0].width for i in imgs) + gap * (len(imgs) - 1)
        k2 = min(1.0, 940 / tw)
        x = W / 2 - tw * k2 / 2
        for img, ws, we, active in imgs:
            w = img.width * k2
            if t >= ws - 0.03:
                p = lin(t, ws - 0.03, ws + 0.09)
                sc = k2 * (0.85 + 0.15 * eback(p)) * (1.06 if active else 1.0)
                put(L, img, x + w / 2, 1430 + 10 * (1 - eo(p)), sc, clamp(p * 2.2))
            x += w + gap * k2
        return


# ------------------------------------------------------------------ maps (Natural Earth, public domain)
LAT0 = 36.0
KX = math.cos(math.radians(LAT0))
MAP_BOUNDS = (-100.0, -60.0, 18.0, 54.0)  # lon0, lon1, lat0, lat1
MAP_PPD = 200  # base pixels per degree (lat)


def proj(lon, lat):
    x = (lon - MAP_BOUNDS[0]) * KX * MAP_PPD
    y = (MAP_BOUNDS[3] - lat) * MAP_PPD
    return x, y


@lru_cache(1)
def map_layers():
    sf = shapefile.Reader(f"{ROOT}/10_MAPS/data/ne_10m_admin_1_states_provinces.shp")
    fields = [f[0] for f in sf.fields[1:]]
    iname, iadm = fields.index("name"), fields.index("admin")
    w = int((MAP_BOUNDS[1] - MAP_BOUNDS[0]) * KX * MAP_PPD)
    h = int((MAP_BOUNDS[3] - MAP_BOUNDS[2]) * MAP_PPD)
    base = Image.new("RGB", (w, h), (8, 14, 26))
    d = ImageDraw.Draw(base)
    hi = {"Georgia": Image.new("L", (w, h)), "New Jersey": Image.new("L", (w, h))}
    for sr in sf.iterShapeRecords():
        rec = sr.record
        bb = sr.shape.bbox
        if bb[2] < MAP_BOUNDS[0] or bb[0] > MAP_BOUNDS[1] or bb[3] < MAP_BOUNDS[2] or bb[1] > MAP_BOUNDS[3]:
            continue
        usa = rec[iadm] == "United States of America"
        pts = sr.shape.points
        parts = list(sr.shape.parts) + [len(pts)]
        for a, b in zip(parts[:-1], parts[1:]):
            ring = [proj(*p) for p in pts[a:b]]
            if len(ring) < 3:
                continue
            d.polygon(ring, fill=(26, 38, 58) if usa else (16, 22, 34), outline=(70, 110, 160) if usa else (40, 55, 75))
            if rec[iname] in hi and usa:
                ImageDraw.Draw(hi[rec[iname]]).polygon(ring, fill=255)
    return base, hi


ATLANTA = (-84.388, 33.749)
MAYWOOD = (-74.062, 40.902)


def map_view(t, c_lonlat, ppd_out, highlight=(), pins=()):
    """render the map centred on c_lonlat at ppd_out output-pixels per degree"""
    base, hi = map_layers()
    cx, cy = proj(*c_lonlat)
    s = MAP_PPD / ppd_out  # base pixels per output pixel
    bg = base.transform((W, H), Image.AFFINE, (s, 0, cx - W / 2 * s, 0, s, cy - H / 2 * s), Image.BILINEAR, fillcolor=(8, 14, 26))
    L = Image.new("RGBA", (W, H))
    for name, a in highlight:
        if a <= 0:
            continue
        m = hi[name].transform((W, H), Image.AFFINE, (s, 0, cx - W / 2 * s, 0, s, cy - H / 2 * s), Image.BILINEAR)
        fill = Image.new("RGBA", (W, H), (205, 40, 45, 255))
        fill.putalpha(m.point(lambda v: int(v * 0.38 * a)))
        L.alpha_composite(glow(fill, 18, (255, 60, 60), 1.0 * a))
        L.alpha_composite(fill)
    for (lon, lat), txt, sub, a in pins:
        if a <= 0:
            continue
        x, y = proj(lon, lat)
        px, py = (x - cx) / s + W / 2, (y - cy) / s + H / 2
        r = 16 + 40 * ((t * 1.2) % 1)
        ring = Image.new("RGBA", (200, 200))
        ImageDraw.Draw(ring).ellipse((100 - r, 100 - r, 100 + r, 100 + r), outline=(255, 230, 160, int(200 * (1 - (t * 1.2) % 1) * a)), width=4)
        put(L, ring, px, py)
        dot = Image.new("RGBA", (40, 40))
        ImageDraw.Draw(dot).ellipse((8, 8, 32, 32), fill=(255, 220, 120, 255), outline=(20, 20, 20, 255), width=3)
        put(L, dot, px, py, eback(clamp(a)), clamp(a * 2))
        put(L, chip(txt, GOLD, 40), px, py - 100, 1, a)
        if sub:
            put(L, text_img(sub, "semi", 28, DIM), px, py - 40 + 70, 1, a)
    return bg, L


# ------------------------------------------------------------------ shots
T = {}


def shot_video(clip, t0, z0=1.0, z1=1.08, look="warm", extra=None):
    def fn(t, fi):
        im = clip.frame(t - t0, z0 + (z1 - z0) * eio(lin(t, t0, t0 + clip.dur)))
        L = Image.new("RGBA", (W, H))
        f = grade(im, look)
        if extra:
            f = extra(t, f, L)
        return f, L
    return fn


def shot_3d(name, t0, extra=None):
    def fn(t, fi):
        im = seq_frame(name, int(round((t - t0) * FPS)))
        L = Image.new("RGBA", (W, H))
        f = grade(im, "none")
        if extra:
            f = extra(t, f, L)
        return f, L
    return fn


HOOK_IMPACT = 0.8
HOOK_MOL = 1.2


def hook_pour_fn(clip):
    def fn(t, fi):
        z = 1.32 - 0.14 * eo(lin(t, 0, 1.2))
        sx = sy = 0.0
        if t >= HOOK_IMPACT:
            k = 26 * math.exp(-(t - HOOK_IMPACT) * 10)
            sx, sy = k * math.sin(t * 90), k * math.cos(t * 70)
        im = clip.frame(t, z)
        im = im.transform((W, H), Image.AFFINE, (1, 0, sx, 0, 1, sy), Image.BICUBIC)
        f = grade(im, "warm")
        f = np.clip((f - 128) * 1.18 + 128, 0, 255)  # extra punch for the very first frames
        if t < 0.07:
            f = f + 140 * (1 - t / 0.07)
        if HOOK_IMPACT <= t < HOOK_IMPACT + 0.1:
            f = f + 170 * (1 - (t - HOOK_IMPACT) / 0.1)
        L = Image.new("RGBA", (W, H))
        p = eback(lin(t, 0.28, 0.48), 2.2)
        f = f * (1 - 0.35 * clamp(p))
        put(L, text_img("COCA", "anton", 250, WHITE, 0, (0, 0, 0, 255), 12), W / 2 - 230, 860, 1.5 - 0.5 * clamp(p), clamp(p * 2))
        m = lin(t, HOOK_IMPACT - 0.02, HOOK_IMPACT + 0.12)
        old = text_img("-COLA", "anton", 250, WHITE, 0, (0, 0, 0, 255), 12)
        put(L, old, W / 2 + 240 + 220 * eo(m), 860 - 160 * eo(m), 1.5 - 0.5 * clamp(p) + 0.6 * m, clamp(p * 2) * (1 - eo(m)), -40 * m)
        if m > 0:
            new = text_img("INE", "anton", 250, ACCENT, 0, (0, 0, 0, 255), 12)
            sc = 1.6 - 0.6 * eback(m, 2.6)
            put(L, glow(pad_img(new, 30), 30, (255, 30, 30), 0.9), W / 2 + 150, 860, sc, clamp(m * 2))
            put(L, new, W / 2 + 150, 860, sc, clamp(m * 2))
        return f, L
    return fn


def hook_mol_fn(clip):
    """1.2 s: the bubbles 'become' the molecule (3D render screened over the soda macro), then the question"""
    def fn(t, fi):
        lt = t - HOOK_MOL
        im = clip.frame(lt, 1.12 + 0.06 * lt)
        f = grade(im, "warm") * 0.42
        mol = np.asarray(seq_frame("mol_in", int(round(lt * FPS)))).astype(np.float32)
        f = 255 - (255 - f) * (255 - mol * 1.15) / 255  # screen blend
        if lt < 0.08:
            f = f + 120 * (1 - lt / 0.08)
        L = Image.new("RGBA", (W, H))
        q = eback(lin(t, 2.0, 2.25))
        put(L, chip("THE ORIGINAL RECIPE?", GOLD, 44), W / 2, 330, 0.9 + 0.1 * clamp(q), clamp(q))
        credit(L, "Structure: PubChem CID 446220 (3D conformer)")
        return f, L
    return fn


def hook_extra(t, f, L):
    """over the bubbles: COCA-COLA, then the second half turns into -INE on 'cocaine'"""
    tc = T["cocaine"]
    f = f * 0.5
    m = eback(lin(t, tc - 0.06, tc + 0.16), 2.4)
    if m > 0:
        w = text_img("COCAINE?", "anton", 230, ACCENT, 0, (0, 0, 0, 255), 12)
        put(L, glow(pad_img(w, 30), 30, (255, 30, 30), 0.8), W / 2, 860, 1.5 - 0.5 * m, clamp(m * 2))
        put(L, w, W / 2, 860, 1.5 - 0.5 * m, clamp(m * 2))
        if t < tc + 0.1:
            f = f + 110 * (1 - lin(t, tc - 0.02, tc + 0.1))
    put(L, chip("THE ORIGINAL RECIPE?", GOLD, 44), W / 2, 330, 1, 1 - lin(t, T["bubbles"] + 0.3, T["bubbles"] + 0.6))
    return f


def ad_fx(label_text, focus):
    def fx(t, f, L):
        k = 1 - lin(t, T["joke"], T["joke"] + 0.15)
        if k > 0 and label_text:
            f = f + 150 * k
        if label_text:
            label(L, t, T["joke"] + 0.15, label_text, 300, GOLD)
        credit(L, "Library of Congress, Prints & Photographs (no known restrictions)")
        return f
    return fx


def shot_archive(name, t0, dur, cx, cy, z0, z1, look, fx=None):
    def fn(t, fi):
        im = cover(archive(name), W, H, cx, cy, z0 + (z1 - z0) * eio(lin(t, t0, t0 + dur)))
        L = Image.new("RGBA", (W, H))
        f = grade(im, look)
        if fx:
            f = fx(t, f, L)
        return f, L
    return fn


def shot_map_atlanta(t, fi):
    t0 = T["atl"]
    p = eio(lin(t, t0, t0 + 2.3))
    c = (-86.0 + 1.6 * p, 35.0 - 1.2 * p)
    bg, L = map_view(t, c, 55 + 110 * p,
                     highlight=[("Georgia", eo(lin(t, t0 + 0.4, t0 + 0.9)))],
                     pins=[(ATLANTA, "ATLANTA, GEORGIA", "", eo(lin(t, T["atlanta"] - 0.1, T["atlanta"] + 0.25)))])
    py = eo(lin(t, T["y1886"] - 0.1, T["y1886"] + 0.25))
    put(L, text_img("1886", "anton", 180, GOLD, 0, (0, 0, 0, 255), 10), W / 2, 330, 0.9 + 0.1 * py, py)
    credit(L, "Map data: Natural Earth (public domain)")
    return grade(bg, "none"), L


def shot_map_nj(t, fi):
    t0 = T["nj"]
    p = eio(lin(t, t0, t0 + 2.2))
    a = ATLANTA
    b = MAYWOOD
    zoom = 120 + 260 * eio(lin(t, t0 + 1.4, t0 + 3.1)) - 40 * math.sin(math.pi * p)
    c = (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)
    bg, L = map_view(t, c, zoom,
                     highlight=[("Georgia", 0.35 * (1 - p)), ("New Jersey", eo(lin(t, t0 + 1.5, t0 + 2.0)))],
                     pins=[(ATLANTA, "ATLANTA", "", 0.6 * (1 - p)),
                           (MAYWOOD, "MAYWOOD, NEW JERSEY", "", eo(lin(t, T["jersey"] - 0.3, T["jersey"] + 0.1)))])
    # dashed flight line
    d = ImageDraw.Draw(L)
    x0, y0 = proj(*a)
    x1, y1 = proj(*b)
    s = MAP_PPD / zoom
    cx, cy = proj(*c)
    P0 = ((x0 - cx) / s + W / 2, (y0 - cy) / s + H / 2)
    P1 = ((x1 - cx) / s + W / 2, (y1 - cy) / s + H / 2)
    q = eio(lin(t, t0, t0 + 2.2))
    for k in range(40):
        u0, u1 = k / 40, (k + 0.5) / 40
        if u1 > q:
            break
        d.line((P0[0] + (P1[0] - P0[0]) * u0, P0[1] + (P1[1] - P0[1]) * u0,
                P0[0] + (P1[0] - P0[0]) * u1, P0[1] + (P1[1] - P0[1]) * u1), fill=(255, 220, 140, 220), width=5)
    pb = eo(lin(t, T["jersey"] + 0.15, T["jersey"] + 0.45))
    if pb > 0:
        box = rr((860, 170), 22, (10, 12, 18, 230), (255, 200, 80, 200), 2)
        box.alpha_composite(text_img("STEPAN COMPANY PLANT (as reported)", "mono", 26, GOLD), (28, 22))
        box.alpha_composite(text_img("DEA-licensed to import coca leaf", "semi", 36, WHITE), (28, 72))
        put(L, box, W / 2, 1180 + 30 * (1 - pb), 1, pb)
    credit(L, "Map data: Natural Earth (public domain)")
    return grade(bg, "none"), L


def shot_pemberton(t, fi):
    t0 = T["pharm"]
    bg = Image.new("RGB", (W, H), (14, 10, 6))
    L = Image.new("RGBA", (W, H))
    ph = archive("john_pemberton.jpg")
    ph = ImageOps.grayscale(ph).convert("RGB")
    ph = Image.blend(ph, Image.new("RGB", ph.size, (120, 85, 45)), 0.22)
    z = 1.0 + 0.06 * eio(lin(t, t0, t0 + 1.8))
    card = ph.resize((int(ph.width * 2.0), int(ph.height * 2.0)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    frame = Image.new("RGBA", (card.width + 60, card.height + 60), (190, 160, 110, 255))
    ImageDraw.Draw(frame).rectangle((10, 10, frame.width - 11, frame.height - 11), outline=(90, 60, 30, 255), width=6)
    frame.paste(card, (30, 30))
    put(L, glow(pad_img(frame, 40), 40, (255, 190, 120), 0.35), W / 2, 760, z)
    put(L, frame, W / 2, 760, z, eo(lin(t, t0, t0 + 0.2)))
    put(L, serif_text("JOHN STITH PEMBERTON", 52), W / 2, 1230, 1, eo(lin(t, T["pemb"] - 0.2, T["pemb"] + 0.15)))
    put(L, text_img("PHARMACIST · ATLANTA · 1831–1888", "mono", 30, GOLD), W / 2, 1300, 1,
        eo(lin(t, T["pemb"], T["pemb"] + 0.3)))
    credit(L, "Portrait: public domain (before 1888), via Wikimedia Commons")
    return grade(bg, "none"), L


def apothecary_fx(t, f, L):
    tm = T["morphine"]
    put(L, chip("MORPHINE ADDICTION", ACCENT, 38), W / 2, 300, 1, eo(lin(t, tm - 0.1, tm + 0.2)) * (1 - lin(t, T["search"] - 0.1, T["search"] + 0.1)))
    put(L, chip("SEARCHING FOR A CURE", CYAN, 38), W / 2, 300, 1, eo(lin(t, T["search"], T["search"] + 0.25)))
    return f


def drink_fx(t, f, L):
    label(L, t, T["drink"] + 0.15, "1886 · A NEW 'BRAIN TONIC'", 300, GOLD)
    return f


def shot_formula(t, fi):
    t0 = T["medicine"] - 0.15
    bg = Image.new("RGB", (W, H), (30, 22, 14))
    paper = archive("loc_coca_cola_trademark_1893.tif")
    bg = cover(paper, W, H, 0.5, 0.75, 1.6)
    bg = Image.blend(bg, Image.new("RGB", (W, H), (25, 18, 10)), 0.72)
    L = Image.new("RGBA", (W, H))
    put(L, serif_text("MEDICINE", 120, CREAM), W / 2, 520, 1, eo(lin(t, t0, t0 + 0.3)))
    put(L, text_img("named after two key ingredients", "semi", 38, DIM), W / 2, 630, 1, eo(lin(t, T["two"], T["two"] + 0.3)))
    for k, (lab, col) in enumerate([("INGREDIENT 1", LEAF), ("INGREDIENT 2", NUT)]):
        p = eback(lin(t, T["two"] + 0.1 + k * 0.15, T["two"] + 0.4 + k * 0.15))
        slot = rr((420, 420), 30, (0, 0, 0, 120), col[:3] + (220,), 4)
        slot.alpha_composite(text_img("?", "anton", 180, col), (210 - 45, 100))
        put(L, slot, 300 + 480 * k, 980, 0.8 + 0.2 * p, clamp(p))
        put(L, text_img(lab, "mono", 28, col), 300 + 480 * k, 1230, 1, clamp(p))
    put(L, text_img("+", "anton", 140, CREAM), W / 2, 980, 1, eo(lin(t, T["two"] + 0.3, T["two"] + 0.5)))
    return grade(bg, "none"), L


def shot_ingredients(t, fi):
    t0 = T["coca1"]
    L = Image.new("RGBA", (W, H))
    top = cover(photo(f"{P}/coca_leaves_a.jpg"), W, H // 2, 0.35, 0.5, 1.0 + 0.06 * lin(t, t0, t0 + 2.5))
    bot = cover(photo(f"{P}/kola_nut.jpg"), W, H // 2, 0.62, 0.5, 1.15 + 0.06 * lin(t, t0, t0 + 2.5))
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    pa = eo(lin(t, t0, t0 + 0.3))
    pb = eo(lin(t, T["kola"] - 0.15, T["kola"] + 0.2))
    canvas.paste(top, (int(-W * (1 - pa)), 0))
    if pb > 0:
        canvas.paste(bot, (int(W * (1 - pb)), H // 2))
    ImageDraw.Draw(L).line((0, H // 2, W, H // 2), fill=(255, 255, 255, 120), width=3)
    put(L, chip("COCA LEAF · Erythroxylum coca", LEAF, 36), W / 2, 200, 1, pa)
    put(L, chip("KOLA NUT", NUT, 40), W / 2, H // 2 + 90, 1, pb)
    credit(L, "Photos: luis perez (coca), mmmavocado (kola) · CC BY 2.0", 1850)
    return grade(canvas, "warm"), L


def shot_name(t, fi):
    t0 = T["name"]
    doc = archive("loc_coca_cola_trademark_1893.tif")
    z = 1.9 + 0.5 * eio(lin(t, t0, t0 + 1.9))
    bg = cover(doc, W, H, 0.5, 0.42, z)
    L = Image.new("RGBA", (W, H))
    f = grade(bg, "warm") * 0.8
    p1 = eback(lin(t, t0 + 0.1, t0 + 0.4))
    p2 = eback(lin(t, T["name_cola"] - 0.1, T["name_cola"] + 0.2))
    put(L, text_img("COCA", "anton", 170, LEAF, 0, (0, 0, 0, 255), 10), W / 2 - 190 + 40 * eo(lin(t, T["name_cola"], T["name_cola"] + 0.3)), 1180, clamp(p1) * 0.2 + 0.8, clamp(p1))
    put(L, text_img("COLA", "anton", 170, NUT, 0, (0, 0, 0, 255), 10), W / 2 + 190 - 40 * eo(lin(t, T["name_cola"], T["name_cola"] + 0.3)), 1180, clamp(p2) * 0.2 + 0.8, clamp(p2))
    label(L, t, t0 + 0.2, "TRADEMARK REGISTRATION · 1893", 300, GOLD)
    credit(L, "Library of Congress, Prints & Photographs (no known restrictions)")
    return f, L


CLAIMS = [("headaches", "CURES HEADACHES!", 640)]


def claim_banner(txt):
    banner = Image.new("RGBA", (900, 150))
    d = ImageDraw.Draw(banner)
    d.rounded_rectangle((0, 0, 899, 149), radius=14, fill=(236, 224, 190, 245), outline=(120, 30, 20, 255), width=6)
    tx = serif_text(txt, 70 if len(txt) < 12 else 58, (130, 20, 15, 255), 0)
    banner.alpha_composite(tx, (450 - tx.width // 2, 75 - tx.height // 2))
    return banner


def shot_claims(t, fi):
    t0 = T["claims_ad"]
    ad = archive("loc_drink_coca_cola_5c_1890s.tif")
    bg = cover(ad, W, H, 0.5, 0.35, 1.25 + 0.12 * eio(lin(t, t0, t0 + 4.3)))
    L = Image.new("RGBA", (W, H))
    f = grade(bg, "warm") * 0.45
    for k, (wd, txt, y) in enumerate(CLAIMS):
        tw = wt(wd, 23)
        p = eback(lin(t, tw - 0.05, tw + 0.25))
        if p <= 0:
            continue
        put(L, claim_banner(txt), W / 2, y, 0.85 + 0.15 * clamp(p), clamp(p), 2)
    credit(L, "Background: 'Drink Coca-Cola 5¢', 1890s, Library of Congress")
    return f, L


def vintage(f):
    """old-film treatment for 'period' human moments: warm sepia, lifted blacks, flicker"""
    lum = f @ np.array([0.299, 0.587, 0.114], np.float32)
    sep = np.stack([lum * 1.08 + 12, lum * 0.95 + 6, lum * 0.78], -1)
    return f * 0.35 + sep * 0.65


def energy_fx(t, f, L):
    f = vintage(f)
    p = eback(lin(t, wt("energy", 23) - 0.05, wt("energy", 23) + 0.25))
    put(L, claim_banner("ENERGY!"), W / 2, 520, 0.85 + 0.15 * clamp(p), clamp(p), -3)
    put(L, text_img("CLAIMS OF THE ERA", "mono", 34, GOLD), W / 2, 300, 1, eo(lin(t, T["people"], T["people"] + 0.3)))
    return f


def amazing_fx(t, f, L):
    f = vintage(f) * 1.05
    p = eback(lin(t, wt("feel", 23) - 0.05, wt("feel", 23) + 0.25))
    put(L, claim_banner("FEEL AMAZING!"), W / 2, 520, 0.85 + 0.15 * clamp(p), clamp(p), 2)
    return f


def ofcourse_fx(t, f, L):
    p = eo(lin(t, T["ofcourse"] + 0.5, T["ofcourse"] + 0.8))
    put(L, chip("IT HAD COCAINE IN IT.", ACCENT, 40), W / 2, 1260, 1, p)
    return f


_DOF_MASK = None


def tilt_shift(f, sharp_until=0.42, full_blur_at=0.62, radius=14):
    """lens-style depth of field: top of frame sharp, falling off to a soft blur below"""
    global _DOF_MASK
    if _DOF_MASK is None:
        y = np.linspace(0, 1, H)[:, None, None]
        _DOF_MASK = np.clip((y - sharp_until) / (full_blur_at - sharp_until), 0, 1).astype(np.float32)
    img = Image.fromarray(np.clip(f, 0, 255).astype(np.uint8))
    small = img.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(radius / 4))
    bl = np.asarray(small.resize((W, H), Image.BILINEAR)).astype(np.float32)
    return f * (1 - _DOF_MASK) + bl * _DOF_MASK


def news_fx(t, f, L):
    f = tilt_shift(vintage(f) * 0.9, 0.36, 0.55, 22)
    pf = eo(lin(t, T["fear"] - 0.1, T["fear"] + 0.25))
    put(L, chip("PUBLIC FEAR OVER COCAINE GROWS", ACCENT, 38), W / 2, 300, 0.9 + 0.1 * pf, pf)
    return f


def mol_in_fx(t, f, L):
    put(L, chip("COCAINE · C17H21NO4", ACCENT, 38), W / 2, 300, 1, eo(lin(t, T["ofcourse"] + 0.3, T["ofcourse"] + 0.6)))
    credit(L, "Structure: PubChem CID 446220 (3D conformer)")
    return f


def mol_out_fx(t, f, L):
    tr = T["removed"]
    put(L, chip("COCAINE REMOVED · c. 1903", ACCENT, 38), W / 2, 300, 1, eo(lin(t, tr, tr + 0.25)))
    if t >= tr:
        k = 1 - lin(t, tr, tr + 0.18)
        f = f + 120 * k
    return f


def shot_crazy(t, fi):
    bg = Image.new("RGB", (W, H), (4, 4, 6))
    L = Image.new("RGBA", (W, H))
    t0 = T["crazy"]
    for k, (w, c, d) in enumerate([("BUT HERE'S", WHITE, 0.0), ("THE CRAZY", ACCENT, 0.4), ("PART.", ACCENT, 0.8)]):
        p = eo(lin(t, t0 + d, t0 + d + 0.25))
        put(L, text_img(w, "anton", 160, c), W / 2, 700 + k * 190 + 40 * (1 - p), 1.0 + 0.03 * (t - t0), p)
    return grade(bg, "none"), L


def shot_timeline(t, fi):
    t0 = T["timeline"]
    bg = grid_bg(t, (10, 8, 6), (40, 32, 22), 90, 6)
    L = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(L)
    x0, x1, y = 140, 940, 820
    p = eio(lin(t, t0 + 0.2, T["y1903"] + 0.4))
    d.line((x0, y, x1, y), fill=(120, 100, 70, 255), width=4)
    d.line((x0, y, x0 + (x1 - x0) * p, y), fill=GOLD, width=8)
    for yr, xf in [(1886, 0.0), (1890, 0.235), (1895, 0.53), (1900, 0.82), (1903, 1.0)]:
        xx = x0 + (x1 - x0) * xf
        d.line((xx, y - 20, xx, y + 20), fill=(200, 180, 140, 255), width=3)
        put(L, text_img(str(yr), "mono", 30, CREAM if xf <= p + 0.01 else (120, 100, 70, 255)), xx, y + 60)
    put(L, text_img("1903", "anton", 200, GOLD, 0, (0, 0, 0, 255), 10), W / 2, 560, 1, eo(lin(t, T["y1903"] - 0.1, T["y1903"] + 0.25)))
    return grade(bg, "none"), L


def leaves_fx(t, f, L):
    label(L, t, T["leaves"] + 0.4, "COCA LEAF · STILL IN THE RECIPE", 300, LEAF)
    return f


def today_fx(t, f, L):
    label(L, t, T["today"] + 0.15, "TODAY", 300, CYAN)
    return f


def lab_fx(t, f, L):
    te, tc = T["extract"], T["cocaine2"]
    pe = eo(lin(t, te + 0.4, te + 0.7))
    put(L, chip("COCA-LEAF EXTRACT", LEAF, 40), W / 2, 300, 1, pe)
    pc = eo(lin(t, tc - 0.1, tc + 0.2))
    if pc > 0:
        badge = rr((600, 120), 24, (10, 12, 18, 230), ACCENT[:3] + (220,), 3)
        tx = text_img("COCAINE", "anton", 74, ACCENT)
        badge.alpha_composite(tx, (300 - tx.width // 2, 60 - tx.height // 2))
        ImageDraw.Draw(badge).line((40, 64, 560, 56), fill=WHITE, width=8)
        put(L, badge, W / 2, 1180, 0.9 + 0.1 * pc, pc, -4)
    return f


def open_fx(t, f, L):
    return f


def shot_end(t, fi, clip):
    t0 = T["remember"]
    im = clip.frame(t - t0, 1.0 + 0.06 * eio(lin(t, t0, END)))
    f = grade(im, "warm") * (1 - 0.45 * eo(lin(t, t0, t0 + 0.4)))
    L = Image.new("RGBA", (W, H))
    tn = T["name_end"]
    p1 = eback(lin(t, tn - 0.2, tn + 0.15))
    p2 = eback(lin(t, tn + 0.15, tn + 0.5))
    put(L, text_img("COCA", "anton", 190, LEAF, 0, (0, 0, 0, 255), 10), W / 2, 620, 0.8 + 0.2 * clamp(p1), clamp(p1))
    put(L, text_img("coca leaf", "semi", 40, WHITE), W / 2, 740, 1, clamp(p1))
    put(L, text_img("+", "anton", 120, CREAM), W / 2, 850, 1, clamp(p2))
    put(L, text_img("COLA", "anton", 190, NUT, 0, (0, 0, 0, 255), 10), W / 2, 1000, 0.8 + 0.2 * clamp(p2), clamp(p2))
    put(L, text_img("kola nut", "semi", 40, WHITE), W / 2, 1120, 1, clamp(p2))
    fade = lin(t, END - 0.8, END)
    return f * (1 - fade), with_alpha(L, 1 - fade) if fade > 0 else L


# ------------------------------------------------------------------ edit decision list
def build():
    T.update(
        bubbles=wt("original") - 0.08, cocaine=wt("cocaine"), joke=wt("This") - 0.1, atl=wt("It's") - 0.1,
        y1886=wt("1886"), atlanta=wt("Atlanta"), pharm=wt("A", 9) - 0.1, pemb=wt("Pemberton"),
        apoth=wt("struggling") - 0.6, morphine=wt("morphine"), search=wt("searching"), drink=wt("So", 15) - 0.1,
        medicine=wt("medicine"), two=wt("two"), coca1=wt("Coca", 18.9) - 0.1, kola=wt("kola"),
        name=wt("Coca", 21.3) - 0.15, name_cola=wt("Cola", 22.0), people=wt("People") - 0.1, ofcourse=wt("Of") - 0.1,
        crazy=wt("But", 29) - 0.1, timeline=wt("Around") - 0.1, y1903=wt("1903"), fear=wt("fear"),
        removed_shot=wt("company", 33.5) - 0.1, removed=wt("removed"), leaves=wt("But", 36) - 0.1,
        today=wt("To", 39) - 0.1, extract=wt("coca", 41.8) - 0.1, cocaine2=wt("cocaine", 43), nj=wt("processed") - 0.1,
        jersey=wt("Jersey"), open=wt("So", 48) - 0.1, opencue=wt("open"), remember=wt("remember") - 0.1,
        name_end=wt("name", 50),
    )
    T.update(claims_ad=wt("cured") - 0.12, amazing=wt("made", 25) - 0.1, news=wt("public") - 0.12)
    clips = {
        "pour": VideoClip(bpath("5081"), 1.2, 0.42, HOOK_MOL + 0.1),
        "molbg": VideoClip(bpath("5080"), 9.0, 0.5, 1.6),
        "bubbles": VideoClip(bpath("5080"), 4.0, 0.5, 2.6),
        "retro": VideoClip(bpath("41357"), 0.6, 0.5, 1.8),
        "cheers": VideoClip(bpath("5085"), 1.9, 0.5, 1.6),
        "wry": VideoClip(bpath("5088"), 1.2, 0.5, 1.5),
        "news": VideoClip(bpath("41191"), 4.0, 0.66, 1.6),
        "drink": VideoClip(bpath("5096"), 4.0, 0.5, 2.0),
        "can": VideoClip(bpath("5077"), 2.0, 0.5, 2.9),
        "lab": VideoClip(bpath("4719"), 3.0, 0.62, 3.3),
        "open": VideoClip(bpath("5093"), 7.4 - (T["opencue"] - T["open"]), 0.4, 2.2),
        "end": VideoClip(bpath("5083"), 2.0, 0.5, END - T["remember"] + 0.1),
    }
    edl = [
        (0.0, HOOK_MOL, hook_pour_fn(clips["pour"]), "pour"),
        (HOOK_MOL, HOOK_MOL + 44 / FPS, hook_mol_fn(clips["molbg"]), "molbg"),
        (HOOK_MOL + 44 / FPS, T["joke"], shot_video(clips["bubbles"], HOOK_MOL + 44 / FPS, 1.05, 1.15, "warm", hook_extra), "bubbles"),
        (T["joke"], T["atl"], shot_archive("loc_drink_coca_cola_5c_1890s.tif", T["joke"], 1.9, 0.5, 0.3, 1.0, 1.12, "warm",
                                          ad_fx("REAL 1890s ADVERTISEMENT", 0.3)), None),
        (T["atl"], T["pharm"], shot_map_atlanta, None),
        (T["pharm"], T["apoth"], shot_pemberton, None),
        (T["apoth"], T["drink"], shot_3d("apothecary", T["apoth"], apothecary_fx), None),
        (T["drink"], T["medicine"] - 0.15, shot_video(clips["drink"], T["drink"], 1.0, 1.08, "warm", drink_fx), "drink"),
        (T["medicine"] - 0.15, T["coca1"], shot_formula, None),
        (T["coca1"], T["name"], shot_ingredients, None),
        (T["name"], T["people"], shot_name, None),
        (T["people"], T["claims_ad"], shot_video(clips["retro"], T["people"], 1.0, 1.06, "warm", energy_fx), "retro"),
        (T["claims_ad"], T["amazing"], shot_claims, None),
        (T["amazing"], T["ofcourse"], shot_video(clips["cheers"], T["amazing"], 1.0, 1.08, "warm", amazing_fx), "cheers"),
        (T["ofcourse"], T["crazy"], shot_video(clips["wry"], T["ofcourse"], 1.0, 1.06, "warm", ofcourse_fx), "wry"),
        (T["crazy"], T["timeline"], shot_crazy, None),
        (T["timeline"], T["news"], shot_timeline, None),
        (T["news"], T["removed_shot"], shot_video(clips["news"], T["news"], 1.0, 1.08, "warm", news_fx), "news"),
        (T["removed_shot"], T["leaves"], shot_3d("mol_out", T["removed_shot"], mol_out_fx), None),
        (T["leaves"], T["today"], shot_3d("leaves", T["leaves"], leaves_fx), None),
        (T["today"], T["extract"], shot_video(clips["can"], T["today"], 1.0, 1.08, "warm", today_fx), "can"),
        (T["extract"], T["nj"], shot_video(clips["lab"], T["extract"], 1.0, 1.1, "tech", lab_fx), "lab"),
        (T["nj"], T["open"], shot_map_nj, None),
        (T["open"], T["remember"], shot_video(clips["open"], T["open"], 1.0, 1.06, "warm", open_fx), "open"),
        (T["remember"], END, lambda t, fi: shot_end(t, fi, clips["end"]), "end"),
    ]
    NO_CAPS.extend([(T["name"], T["people"]), (T["crazy"], T["timeline"]), (T["name_end"] - 0.2, END)])
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
    cur_clip = None
    for fi in range(int(t_from * FPS + 0.01), int(t_to * FPS + 0.01)):
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
