"""Ek Din, 5 Naam — standalone Chhoti Diwali reel (no series part).
Narak Chaturdashi across India: Chhoti Diwali (North), Roop Chaudas (Rajasthan), Kali Chaudas (Gujarat),
Bhoot Chaturdashi (Bengal: 14 lamps for 14 generations of ancestors), Deepavali itself in Tamil Nadu
(pre-dawn 'Ganga snanam aachaa?'). Rule: whatever the narration names is what the frame shows.
Only individual state outlines are drawn (Natural Earth admin-1); no national boundary is drawn.
"""
import math
import os
import sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
from kd import CREAM, GOLD, RED, Scene, W, H  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

A = f"{KD}/art/full"
R3 = f"{KD}/renders3d"
T = kd.Timing(HERE)
at = T.at
END = T.end + 1.6
TAG = "KATHA DEEP · CHHOTI DIWALI"
MET = "ART: THE MET · OPEN ACCESS (CC0)"
SHP = "/home/user/a/cocacola/10_MAPS/data/ne_10m_admin_1_states_provinces.shp"
STATE_IDX = {"Rajasthan": 1610, "Gujarat": 1612, "West Bengal": 537, "Tamil Nadu": 2242, "Uttar Pradesh": 1644}
NAMES = [("CHHOTI DIWALI", CREAM), ("ROOP CHAUDAS", GOLD), ("KALI CHAUDAS", RED), ("BHOOT CHATURDASHI", (170, 200, 255)), ("DEEPAVALI", GOLD)]


@lru_cache(8)
def state_img(name, box=420, col=(245, 193, 72)):
    """One state's outline (gold stroke, translucent fill, glow) fitted in a box. Equirectangular with cos(lat)."""
    import shapefile
    sh = shapefile.Reader(SHP).shape(STATE_IDX[name])
    pts = sh.points
    lat0 = sum(p[1] for p in pts) / len(pts)
    k = math.cos(math.radians(lat0))
    xs = [p[0] * k for p in pts]
    ys = [-p[1] for p in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    s = (box - 40) / max(maxx - minx, maxy - miny)
    im = Image.new("RGBA", (box, box))
    d = ImageDraw.Draw(im)
    parts = list(sh.parts) + [len(pts)]
    for a, b in zip(parts[:-1], parts[1:]):
        poly = [((xs[i] - minx) * s + 20 + (box - 40 - (maxx - minx) * s) / 2, (ys[i] - miny) * s + 20 + (box - 40 - (maxy - miny) * s) / 2) for i in range(a, b)]
        if len(poly) > 2:
            d.polygon(poly, fill=(*col, 60), outline=(*col, 255), width=5)
    glow = im.filter(ImageFilter.GaussianBlur(14))
    out = Image.new("RGBA", im.size)
    out.alpha_composite(glow)
    out.alpha_composite(im)
    return out


def state_at(name, ts, x, y, box=420, label=True):
    def f(base, t, sc):
        if t < ts:
            return
        k = kd.eo((t - ts) / 0.4)
        im = state_img(name, box)
        kd.paste_fade(base, im, (x, y + 30 * (1 - k)), k)
        if label:
            lab = kd.text_img(name.upper(), "mono", 26, CREAM)
            kd.paste_fade(base, lab, (x + box / 2 - lab.width / 2, y + box - 18), k)
    return f


def name_cascade(ts):
    """The five names stack in, one every 0.3 s (hook)."""
    def f(base, t, sc):
        for i, (n, c) in enumerate(NAMES):
            tt = ts + i * 0.3
            if t < tt:
                continue
            k = kd.eo((t - tt) / 0.3)
            ch = kd.chip(n, 64, c, c)
            kd.paste_fade(base, ch, (W / 2 - ch.width / 2, 620 + i * 190 + 30 * (1 - k)), k)
    return f


def count14(ts, te):
    """Counts 1 -> 14 in step with the ring of diyas."""
    def f(base, t, sc):
        if t < ts:
            return
        n = min(14, 1 + int((t - ts) / ((te - ts) / 14)))
        im = kd.text_img(str(n), "anton", 260, GOLD)
        kd.paste_fade(base, im, (W / 2 - im.width / 2, 1330), 1.0)
        lab = kd.text_img("DIYE · PEEDHIYAN", "mono", 30, CREAM)
        kd.paste_fade(base, lab, (W / 2 - lab.width / 2, 1640), kd.eo((t - ts) / 0.4))
    return f


@lru_cache(2)
def tamil_img(size=96):
    f = ImageFont.truetype(f"{KD}/fonts/NotoSansTamil.ttf", size, layout_engine=ImageFont.Layout.RAQM)
    try:
        f.set_variation_by_axes([100, 700])
    except Exception:
        pass
    txt = "கங்கா ஸ்நானம் ஆச்சா?"
    l, t_, r, b = f.getbbox(txt)
    im = Image.new("RGBA", (r - l + 60, b - t_ + 60))
    ImageDraw.Draw(im).text((30 - l, 30 - t_), txt, font=f, fill=(*GOLD, 255))
    sh = im.split()[3].filter(ImageFilter.GaussianBlur(9))
    out = Image.new("RGBA", im.size)
    shade = Image.new("RGBA", im.size, (0, 0, 0, 0))
    shade.putalpha(sh.point(lambda v: int(v * 0.8)))
    out.alpha_composite(shade, (4, 5))
    out.alpha_composite(im)
    return out


def tamil_line(ts):
    def f(base, t, sc):
        if t < ts:
            return
        k = kd.eo((t - ts) / 0.4)
        im = tamil_img(92)
        if im.width > W - 60:
            im = im.resize((W - 60, int(im.height * (W - 60) / im.width)), Image.LANCZOS)
        kd.paste_fade(base, im, (W / 2 - im.width / 2, 900 + 20 * (1 - k)), k)
        tr = kd.text_img("“GANGA SNANAM AACHAA?”", "anton", 64, CREAM)
        kd.paste_fade(base, tr, (W / 2 - tr.width / 2, 1060), k)
    return f


def BG_dawn():
    """Pre-dawn sky over the sea: deep indigo to saffron horizon, sun about to rise."""
    import numpy as np
    y = np.linspace(0, 1, H)[:, None, None]
    top, mid, low = np.array([18, 16, 48]), np.array([150, 60, 70]), np.array([255, 170, 80])
    a = np.where(y < 0.62, top + (mid - top) * (y / 0.62), mid + (low - mid) * ((y - 0.62) / 0.38))
    sky = Image.fromarray(np.repeat(a, W, 1).astype("uint8"))

    def f(lt, fr, fi):
        im = sky.copy().convert("RGBA")
        d = ImageDraw.Draw(im)
        r = 150
        cy = H * 0.86 - 60 * kd.ss(fr)
        d.ellipse((W / 2 - r, cy - r, W / 2 + r, cy + r), fill=(255, 205, 120, 255))
        g = im.filter(ImageFilter.GaussianBlur(40))
        im = Image.blend(im, g, 0.35)
        d = ImageDraw.Draw(im)
        d.rectangle((0, H * 0.86, W, H), fill=(30, 22, 40, 255))
        for i in range(14):
            yy = H * 0.87 + i * 18
            d.line((W / 2 - 160 + i * 6, yy, W / 2 + 160 - i * 6, yy), fill=(255, 190, 110, 90 - i * 5), width=3)
        return im.convert("RGB")
    return f


def merge_to_one(ts, te):
    """Five name chips shrink into one glowing diya flame."""
    def f(base, t, sc):
        if t < ts:
            return
        k = kd.ss((t - ts) / max(0.1, te - ts))
        for i, (n, c) in enumerate(NAMES):
            ch = kd.chip(n, 52, c, c)
            x0, y0 = W / 2 - ch.width / 2, 560 + i * 150
            x, y = kd.lerp(x0, W / 2 - ch.width / 2, k), kd.lerp(y0, 1180, k)
            kd.paste_fade(base, ch, (x, y), 1 - k)
        if k > 0.5:
            kk = (k - 0.5) * 2
            fl = Image.new("RGBA", (W, H))
            d = ImageDraw.Draw(fl)
            r = 70 * kk
            d.ellipse((W / 2 - r * 0.6, 1180 - r * 1.6, W / 2 + r * 0.6, 1180 + r * 0.4), fill=(255, 200, 100, int(255 * kk)))
            base.alpha_composite(fl.filter(ImageFilter.GaussianBlur(30)))
            base.alpha_composite(fl.filter(ImageFilter.GaussianBlur(4)))
    return f


def scenes():
    s = []
    s.append(Scene(0, at("उत्तर भारत"), kd.BG_plate("night"), fx=[name_cascade(at("पर इसके नाम"))],
                   caps=[(0.0, "AAJ KA DIN: EK", "NAAM: PAANCH", GOLD, at("पाँच।"))], grade_kind=None, flash=(0, 0.35, (0, 0, 0))))
    s.append(Scene(at("उत्तर भारत"), at("राजस्थान"), kd.BG_kb(f"{R3}/threshold.png", (0.5, 0.52, 1.0), (0.5, 0.60, 0.78)),
                   caps=[(at("उत्तर भारत"), "UTTAR BHARAT:", "CHHOTI DIWALI", GOLD, at("छोटी दिवाली")),
                         (at("देहरी"), "DEHRI PAR", "PEHLE DIYE", GOLD, at("पहले दिये"))],
                   fx=[kd.flicker(0.07), kd.embers(30, 21, (255, 180, 90), 60, 0.6), state_at("Uttar Pradesh", at("उत्तर भारत") + 0.2, 620, 1380, 340)],
                   grade_kind="flame"))
    s.append(Scene(at("राजस्थान"), at("गुजरात"), kd.BG_kb(f"{A}/37908.jpg", (0.55, 0.40, 0.80), (0.60, 0.48, 0.58)),
                   caps=[(at("राजस्थान"), "RAJASTHAN:", "ROOP CHAUDAS", GOLD, at("रूप चौदस")),
                         (at("सूरज"), "SURYODAY SE PEHLE:", "UBTAN + SNAAN", GOLD, at("उबटन"))],
                   fx=[state_at("Rajasthan", at("राजस्थान"), 620, 1330, 380)], credit=MET, grade_kind="warm"))
    s.append(Scene(at("गुजरात"), at("बंगाल"), kd.BG_kb(f"{A}/849495.jpg", (0.48, 0.26, 0.42), (0.48, 0.22, 0.34)),
                   caps=[(at("गुजरात"), "GUJARAT:", "KALI CHAUDAS", RED, at("काली चौदस")),
                         (at("माँ महाकाली"), "MAA MAHAKALI KI PUJA", None, None),
                         (at("ताकि"), "HAR DAR, HAR BURI NAZAR", "DOOR", GOLD, at("दूर रहे"))],
                   fx=[state_at("Gujarat", at("गुजरात"), 640, 1360, 360)], credit=MET, grade_kind="warm"))
    s.append(Scene(at("बंगाल"), at("और तमिलनाडु"), kd.BG_kb(f"{R3}/diya_ring.png", (0.5, 0.45, 1.0), (0.5, 0.40, 0.82)),
                   caps=[(at("बंगाल"), "BENGAL:", "BHOOT CHATURDASHI", (170, 200, 255), at("भूत चतुर्दशी")),
                         (at("चौदह दिये"), "14 DIYE =", "14 PEEDHIYON KE LIYE", GOLD, at("पूर्वजों"))],
                   fx=[kd.flicker(0.06), state_at("West Bengal", at("बंगाल"), 720, 980, 300, False), count14(at("चौदह दिये"), at("पूर्वजों") + 1.6)],
                   grade_kind="flame"))
    s.append(Scene(at("और तमिलनाडु"), at("भोर में"), kd.BG_kb(f"{A}/38135.jpg", (0.5, 0.45, 0.9), (0.5, 0.32, 0.6)),
                   caps=[(at("और तमिलनाडु"), "AUR TAMIL NADU?", None, None),
                         (at("दीपावली है"), "WAHAN AAJ HI", "DEEPAVALI", GOLD, at("दीपावली है"))],
                   fx=[state_at("Tamil Nadu", at("और तमिलनाडु"), 640, 1330, 380)], credit=MET, grade_kind="warm"))
    s.append(Scene(at("भोर में"), at("नाम पाँच"), BG_dawn(),
                   caps=[(at("भोर में"), "BHOR MEIN SAWAAL:", None, None),
                         (at("यानी"), "YAANI:", "GANGA SNAAN HUA?", GOLD, at("गंगा स्नान"))],
                   over=[tamil_line(at("गंगा स्नानम्"))], grade_kind=None))
    s.append(Scene(at("नाम पाँच"), at("आपके यहाँ"), kd.BG_plate("red"), fx=[merge_to_one(at("नाम पाँच") + 0.2, at("पर दिया एक") + 0.6)],
                   caps=[(at("नाम पाँच"), "NAAM PAANCH, REET ALAG...", "PAR DIYA EK", GOLD, at("पर दिया एक"))], grade_kind=None))
    s.append(Scene(at("आपके यहाँ"), END, kd.BG_plate("night"), fx=[kd.embers(50, 23, (255, 190, 110), 70, 0.8), kd.light_glow(0.5, 0.62, 300, (255, 190, 110), 0.7, 0.1)],
                   caps=[(at("आपके यहाँ"), "AAPKE YAHAN", "AAJ KO KYA KEHTE HAIN?", GOLD, at("आज के दिन"))],
                   over=[kd.chips_at([(at("कमेंट"), "COMMENT KARO", "c", 1300, {"size": 60}),
                                      (at("कमेंट") + 0.4, "FOLLOW · KATHA DEEP", "c", 1460, {"size": 46})])], grade_kind=None))
    return s


def audio():
    import music
    import mixlib
    sa = 155.56  # D# — bright, festive; Kafi-ish colour
    sec = [(0, at("उत्तर भारत"), {"pad": 0.8, "tanpura": 0.5, "pad_bright": 900}),
           (at("उत्तर भारत") - 0.3, at("नाम पाँच"), {"tanpura": 0.8, "drums": 0.6, "pad": 0.4}),
           (at("नाम पाँच") - 0.3, END, {"tanpura": 1.0, "pad": 0.9, "pad_bright": 1700})]
    hits = [(0.05, "bell", 0.7)] + [(at(p), "bellhi", 0.45) for p in ("राजस्थान", "गुजरात", "बंगाल", "और तमिलनाडु")] + [(at("पर दिया एक"), "bell", 0.7)]
    mel = (at("नाम पाँच"), [(0, 0.8, 7), (0.8, 0.8, 10), (1.6, 1.6, 12), (3.4, 0.8, 10), (4.2, 2.4, 7), (6.8, 2.6, 0)])
    st = music.score(END, sa, sec, hits, mel, bpm=96, seed=4)
    cues = [(0.0, "magic-sparkle", -16), (at("उत्तर भारत") - 0.2, "soft-fire-woosh", -15),
            (at("राजस्थान") - 0.2, "whoosh-transition", -17), (at("गुजरात") - 0.2, "whoosh-deep-impact", -16),
            (at("बंगाल") - 0.2, "wind-swoosh", -17), (at("चौदह दिये"), "light-energy", -19),
            (at("और तमिलनाडु") - 0.2, "whoosh-transition", -17), (at("भोर में"), "river-water", -22, {"max_len": 5, "fade_out": 1.5}),
            (at("नाम पाँच") - 0.2, "harp-sweep", -15), (at("पर दिया एक"), "bell-chime", -14)]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-6.0)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "still":
        for t in sys.argv[2:]:
            kd.still(scenes(), float(t), f"{HERE}/qc_{t}.png", TAG)
    if mode in ("picture", "all"):
        kd.render(scenes(), f"{HERE}/picture.mp4", TAG, t_end=END)
    if mode in ("audio", "all"):
        audio()
