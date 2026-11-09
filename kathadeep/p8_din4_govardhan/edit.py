"""Deepotsav · DIN 4/5 — Govardhan. Source: Bhagavata Purana 10.24 (Indra-yajna in Braj, Krishna questions Nanda,
'our wealth is our cows, our support is the hill', the Govardhan puja) and 10.25 (Indra's pralaya clouds, Krishna lifts
Govardhan in one hand 'as a child holds a mushroom' 10.25.19, seven days), 10.27 (Indra's apology, Surabhi/Kamadhenu's
abhisheka, the name Govinda).
Look: monsoon cinematic. Series top-left Anton captions (as Din 1/2) + kinetic Devanagari subtitles, cool storm grade
with rain streaks + lightning only in the storm section, warm gold after the lift. One picture per spoken keyword.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

import kd, kdextra, kdv2  # noqa: E401,E402
from kd import CREAM, GOLD, RED, W, H  # noqa: E402

A = f"{KD}/art/full"
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0
TAG = "DEEPOTSAV · DIN 4/5"
kd.CAP_MODE = "topleft"
kd.TRANS = "cut"
kd.SUBS = T
MET = "ART: THE MET · OPEN ACCESS (CC0)"
BLUE = (150, 200, 255)


# ------------------------------------------------------------------ monsoon fx
def rain(density=1.0, seed=4, slant=0.22, alpha=150):
    """Falling rain streaks (3 depth layers, near = longer, faster, brighter)."""
    rng = np.random.default_rng(seed)
    layers = []
    for depth, (n, ln, sp, a, wd) in enumerate([(160, 34, 1900, 0.45, 1), (110, 60, 2600, 0.7, 2), (40, 110, 3400, 1.0, 3)]):
        n = int(n * density)
        layers.append((rng.uniform(0, W, n), rng.uniform(0, H, n), ln, sp, a, wd))

    def f(base, t, sc):
        lay = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(lay)
        for xs, ys, ln, sp, a, wd in layers:
            yy = (ys + t * sp) % (H + ln) - ln
            xx = (xs + yy * slant) % W
            col = (210, 228, 255, int(alpha * a))
            for x, y in zip(xx, yy):
                d.line((x, y, x + ln * slant, y + ln), fill=col, width=wd)
        base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.6)))
    return f


def lightning(times, seed=9):
    """Forked bolt + sky flash at each time (0.35 s)."""
    rng = np.random.default_rng(seed)
    bolts = []
    for _ in times:
        x = rng.uniform(W * 0.25, W * 0.75); y = -20; pts = [(x, y)]
        while y < H * 0.55:
            y += rng.uniform(40, 90); x += rng.uniform(-70, 70); pts.append((x, y))
        bolts.append(pts)

    def f(base, t, sc):
        for ts, pts in zip(times, bolts):
            dt = t - ts
            if not 0 <= dt <= 0.35:
                continue
            k = 1 - dt / 0.35
            k = k * (0.6 + 0.4 * (math.sin(dt * 90) > 0))
            lay = Image.new("RGBA", (W, H), (190, 210, 255, int(90 * k)))
            d = ImageDraw.Draw(lay)
            d.line(pts, fill=(235, 242, 255, int(255 * k)), width=7)
            glow = lay.filter(ImageFilter.GaussianBlur(14))
            base.alpha_composite(glow)
            d2 = Image.new("RGBA", (W, H)); ImageDraw.Draw(d2).line(pts, fill=(255, 255, 255, int(255 * k)), width=3)
            base.alpha_composite(d2)
    return f


def BG_storm(seed=2):
    """Churning pralaya clouds (procedural, moving) for the 'aandhi / bijli' beat."""
    rng = np.random.default_rng(seed)
    octs = [cv2_resize(rng.random((s, int(s * 0.6))).astype(np.float32)) for s in (6, 12, 24, 48)]

    def f(lt, fr, fi):
        acc = np.zeros((H, W), np.float32)
        for i, o in enumerate(octs):
            sh = int(lt * (60 + 40 * i)) % W
            acc += np.roll(o, sh, 1) / (2 ** i)
        acc = (acc - acc.min()) / (acc.max() - acc.min())
        y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        v = acc * (1.0 - 0.6 * y)
        rgb = np.stack([18 + 70 * v, 24 + 84 * v, 40 + 110 * v], 2)
        return Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    return f


def cv2_resize(a):
    import cv2
    return cv2.resize(a, (W, H), interpolation=cv2.INTER_CUBIC)


def counter7(ts, te, y=1180):
    """'DIN 1..7' ticking counter (seven days and nights)."""
    def f(base, t, sc):
        if t < ts:
            return
        n = 1 + min(6, int((t - ts) / max(0.1, (te - ts)) * 7))
        im = kd.text_img(f"DIN {n} / 7", "anton", 120, CREAM)
        kd.paste_fade(base, im, (W / 2 - im.width / 2, y), kd.eo((t - ts) / 0.25))
    return f


# ------------------------------------------------------------------ shot list
def scenes():
    P = lambda i, wf=0.72, mv="push", focus=None: kdv2.BG_auto(f"{A}/{i}.jpg", wf, mv, focus)
    Q = lambda i, a, b, mv="push": kdv2.BG_para(f"{A}/{i}.jpg", a, b, mv)

    def cap(t, l1, l2=None, c=GOLD, t2=None):
        return [(t, l1, l2, c, t2)]
    storm = [rain(1.0), lightning([at("बिजली") + 0.05])]
    S = [
        # HOOK — 7-year-old, a whole mountain, on his hand
        (0.0, P(38422, 0.95, "rise", (0.5, 0.30)), dict(caps=cap(0.0, "7 SAAL KA BACHCHA"), credit=MET, flash=(0, 0.35, (0, 0, 0)))),
        (at("सात दिन तक"), Q(37968, (0.50, 0.52, 0.76), (0.50, 0.50, 0.66), "pull"), dict(caps=cap(at("सात दिन तक"), "7 DIN TAK..."), credit=MET, trans="zoom")),
        (at("एक पूरा पहाड़"), Q(37968, (0.50, 0.18, 0.62), (0.50, 0.14, 0.52), "rise"), dict(caps=cap(at("एक पूरा पहाड़"), "EK POORA PAHAAD"), credit=MET, grade="night")),
        (at("उसके हाथ"), Q(37968, (0.46, 0.40, 0.34), (0.46, 0.37, 0.24), "push"), dict(caps=cap(at("उसके हाथ"), "USKE HAATH PAR", c=RED), credit=MET, trans="flash", shake=(at("उसके हाथ"), 0.5))),
        # tracker
        (at("कल गोवर्धन"), kd.BG_plate("night"), dict(caps=cap(at("कल गोवर्धन"), "KAL: GOVARDHAN PUJA", "DEEPOTSAV · CHAUTHA DIYA", GOLD, at("चौथा दिया")),
                                                     over=[kdextra.five_diyas(at("कल गोवर्धन") + 0.2, 4), kd.deva_card(at("कल गोवर्धन") + 0.1, "गोवर्धन पूजा", None, None, y=640, size=150, color=(255, 226, 160))], fx=[kd.embers(40, 8, (255, 200, 120), 60, 0.6)], grade=None, trans="whip")),
        (at("आज उसकी"), P(810836, 0.70, "left", (0.55, 0.36)), dict(caps=cap(at("आज उसकी"), "AAJ: USKI KAHANI"), credit=MET)),
        # Bhagavata, Braj, Indra yajna
        (at("भागवत"), Q(37999, (0.50, 0.55, 0.42), (0.45, 0.62, 0.34), "right"), dict(caps=cap(at("भागवत"), "BHAGAVAT PURAN 10.24"), credit=MET, trans="push")),
        (at("ब्रज में"), P(37931, 0.42, "left", (0.62, 0.45)), dict(caps=cap(at("ब्रज में"), "BRAJ"), credit=MET, trans="whip")),
        (at("इंद्र देव"), Q(38037, (0.74, 0.42, 0.26), (0.74, 0.40, 0.20), "push"), dict(caps=cap(at("इंद्र देव"), "INDRA DEV"), credit=MET, trans="zoom")),
        (at("यज्ञ होता"), kd.BG_plate("red"), dict(caps=cap(at("यज्ञ होता"), "HAR SAAL: BADA YAGYA"), fx=[kd.flicker(0.16), kd.embers(70, 3, (255, 170, 70), 140, 0.9)],
                                                  over=[kd.deva_card(at("यज्ञ होता") + 0.15, "यज्ञ", None, "INDRA KE NAAM", y=760, size=210, color=(255, 196, 110))], grade=None)),
        # Krishna asks Nanda
        (at("नन्हे"), Q(37903, (0.80, 0.58, 0.28), (0.80, 0.62, 0.20), "push"), dict(caps=cap(at("नन्हे"), "NANHE KRISHNA"), credit=MET, trans="whip")),
        (at("नंद बाबा"), Q(37902, (0.62, 0.55, 0.30), (0.60, 0.55, 0.22), "left"), dict(caps=cap(at("नंद बाबा"), "NAND BABA SE PRASHN"), credit=MET)),
        (at("किसके लिए"), kd.BG_plate("gold"), dict(over=[kd.deva_card(at("किसके लिए"), "ये यज्ञ", "किसके लिए?", None, y=700, size=150, color=(255, 236, 190))], grade=None, trans="zoom")),
        (at("नंद बोले"), Q(37900, (0.60, 0.55, 0.28), (0.62, 0.55, 0.20), "right"), dict(caps=cap(at("नंद बोले"), "NAND BABA"), credit=MET)),
        (at("इंद्र के लिए"), Q(75004, (0.68, 0.42, 0.62), (0.68, 0.36, 0.48), "push"), dict(caps=cap(at("इंद्र के लिए"), "INDRA KE LIYE"), credit=MET, trans="zoom")),
        (at("बारिश देते"), Q(37883, (0.50, 0.20, 0.70), (0.50, 0.16, 0.58), "fall"), dict(caps=cap(at("बारिश देते"), "WAHI BAARISH DETE HAIN"), credit=MET, fx=[rain(0.5, 1, alpha=110)], grade="teal")),
        # Krishna's answer
        (at("कृष्ण बोले"), Q(849485, (0.28, 0.50, 0.46), (0.27, 0.46, 0.34), "push"), dict(caps=cap(at("कृष्ण बोले"), "KRISHNA BOLE:"), credit=MET, trans="whip")),
        (at("हमारी गायें"), P(65576, 0.50, "left", (0.50, 0.45)), dict(caps=cap(at("हमारी गायें"), "HAMARA DHAN = GAAYEIN"), credit=MET, trans="zoom")),
        (at("हमारा सहारा"), Q(37996, (0.22, 0.48, 0.30), (0.24, 0.48, 0.24), "rise"), dict(caps=cap(at("हमारा सहारा"), "HAMARA SAHARA"), credit=MET)),
        (at("गोवर्धन पर्वत"), Q(37968, (0.30, 0.24, 0.40), (0.62, 0.22, 0.40), "right"), dict(caps=cap(at("गोवर्धन पर्वत"), "GOVARDHAN PARVAT"), credit=MET)),
        (at("पूजा इनकी"), Q(37996, (0.62, 0.26, 0.34), (0.66, 0.26, 0.26), "left"), dict(caps=cap(at("पूजा इनकी"), "POOJA INKI KIJIYE"), credit=MET, trans="zoom")),
        (at("और ब्रजवासियों"), P(876115, 0.62, "rise", (0.50, 0.32)), dict(caps=cap(at("और ब्रजवासियों"), "BRAJ NE KI GOVARDHAN PUJA"), credit=MET, trans="whip")),
        # Indra's rage, the storm
        (at("इंद्र का अहंकार"), Q(75004, (0.66, 0.34, 0.40), (0.66, 0.32, 0.28), "push"), dict(caps=cap(at("इंद्र का अहंकार"), "INDRA KA AHANKAAR", c=RED), credit=MET, grade="ember", shake=(at("भड़क") , 0.6), trans="flash", flash=(at("इंद्र का अहंकार"), 0.3, (255, 60, 30)))),
        (at("प्रलय"), Q(37883, (0.50, 0.12, 0.55), (0.50, 0.10, 0.40), "fall"), dict(caps=cap(at("प्रलय"), "PRALAY KE BAADAL"), credit=MET, grade="night", fx=[rain(0.6, 2)], trans="zoom")),
        (at("मूसलाधार"), Q(37968, (0.50, 0.10, 0.70), (0.50, 0.08, 0.56), "fall"), dict(caps=cap(at("मूसलाधार"), "MOOSALADHAAR BAARISH"), credit=MET, grade="night", fx=[rain(1.4, 3, alpha=180)])),
        (at("आँधी"), BG_storm(), dict(caps=cap(at("आँधी"), "AANDHI", "BIJLI", RED, at("बिजली")), fx=storm, grade=None, shake=(at("बिजली"), 0.5), trans="whip")),
        (at("ब्रज डूबने"), Q(37847, (0.30, 0.58, 0.40), (0.30, 0.60, 0.30), "left"), dict(caps=cap(at("ब्रज डूबने"), "BRAJ DOOBNE LAGA", c=RED), credit=MET, grade="night", fx=[rain(1.2, 5, alpha=170)], trans="zoom")),
        (at("गायें, ग्वाले"), Q(37847, (0.30, 0.25, 0.36), (0.30, 0.26, 0.28), "right"), dict(caps=cap(at("गायें, ग्वाले"), "GAAYEIN · GWALE"), credit=MET, grade="night", fx=[rain(1.2, 6, alpha=170)])),
        (at("सब दौड़े"), Q(37847, (0.62, 0.26, 0.34), (0.62, 0.24, 0.24), "push"), dict(caps=cap(at("सब दौड़े"), "SAB DAUDE KRISHNA KI OR"), credit=MET, grade="teal", fx=[rain(1.0, 7, alpha=150)], trans="zoom")),
        # The lift
        (at("और तब"), Q(37968, (0.47, 0.52, 0.52), (0.47, 0.46, 0.42), "rise"), dict(caps=cap(at("और तब"), "AUR TAB..."), credit=MET, fx=[rain(0.7, 8, alpha=120)], trans="iris")),
        (at("एक हाथ से"), Q(37968, (0.46, 0.38, 0.26), (0.46, 0.34, 0.19), "push"), dict(caps=cap(at("एक हाथ से"), "EK HAATH SE"), credit=MET, fx=[kd.light_glow(0.5, 0.42, 420, (255, 220, 150), 0.35, 0.15)], trans="zoom")),
        (at("उठा लिया"), Q(37968, (0.50, 0.30, 0.56), (0.50, 0.42, 0.76), "pull"), dict(caps=cap(at("उठा लिया"), "POORA GOVARDHAN", "UTHA LIYA", GOLD, at("उठा लिया")), credit=MET, shake=(at("उठा लिया"), 0.8), trans="flash", flash=(at("उठा लिया"), 0.35, (255, 240, 210)))),
        (at("जैसे कोई"), kd.BG_plate("gold"), dict(over=[kd.deva_card(at("जैसे कोई") + 0.1, "दधार लीलया विष्णुः", "छत्राकमिव बालकः", "BHAGAVATA PURANA 10.25.19", y=640, size=104, color=(255, 232, 170)),
                                                       kd.chips_at([(at("कुकुरमुत्ता"), "JAISE BAALAK KUKURMUTTA UTHA LE", "c", 1160, {"size": 42})])], grade=None, trans="push")),
        (at("सात दिन,"), Q(37968, (0.55, 0.70, 0.52), (0.55, 0.74, 0.42), "left"), dict(caps=cap(at("सात दिन,"), "7 DIN · 7 RAAT", None), over=[counter7(at("सात दिन,") + 0.2, at("पूरा ब्रज"))], credit=MET, trans="whip")),
        (at("पूरा ब्रज"), Q(876115, (0.50, 0.80, 0.56), (0.50, 0.82, 0.46), "push"), dict(caps=cap(at("पूरा ब्रज"), "POORA BRAJ SURAKSHIT"), credit=MET)),
        # Indra humbled, Kamadhenu, Govinda
        (at("इंद्र का घमंड"), Q(38432, (0.50, 0.42, 0.80), (0.50, 0.40, 0.66), "fall"), dict(caps=cap(at("इंद्र का घमंड"), "INDRA KA GHAMAND", "TOOT GAYA", RED, at("टूट")), credit=MET, trans="flash", flash=(at("टूट"), 0.25, (255, 255, 255)))),
        (at("हाथ जोड़कर"), Q(38432, (0.50, 0.30, 0.46), (0.50, 0.28, 0.36), "push"), dict(caps=cap(at("हाथ जोड़कर"), "HAATH JODKAR AAYE"), credit=MET)),
        (at("कामधेनु"), Q(65576, (0.30, 0.38, 0.22), (0.30, 0.38, 0.16), "push"), dict(caps=cap(at("कामधेनु"), "KAMDHENU"), credit=MET, fx=[kd.light_glow(0.5, 0.45, 520, (255, 215, 140), 0.30, 0.15)], trans="zoom")),
        (at("अभिषेक"), Q(858237, (0.46, 0.30, 0.60), (0.46, 0.27, 0.46), "rise"), dict(caps=cap(at("अभिषेक"), "KRISHNA KA ABHISHEK"), credit=MET, fx=[rain(0.35, 11, slant=0.0, alpha=110), kd.light_glow(0.5, 0.3, 480, (255, 225, 160), 0.3, 0.1)])),
        (at("उस दिन"), Q(37929, (0.13, 0.30, 0.22), (0.13, 0.30, 0.16), "push"), dict(caps=cap(at("उस दिन"), "US DIN NAAM PADA:"), credit=MET, trans="whip")),
        (at("गोविंद"), kd.BG_plate("gold"), dict(fx=[kd.embers(60, 12, (255, 210, 130), 90, 0.8)],
                                               over=[kd.deva_card(at("गोविंद"), "गोविंद", None, "GO (GAAY) KE RAKSHAK", y=720, size=230, color=(255, 238, 190))],
                                               grade=None, trans="flash", flash=(at("गोविंद"), 0.3, (255, 240, 200)))),
        # outro: Annakut tomorrow, Bhai Dooj day after
        (at("इसीलिए"), kd.BG_plate("red"), dict(fx=[kd.embers(50, 13, (255, 190, 110), 70, 0.7)], over=[kd.deva_card(at("अन्नकूट"), "अन्नकूट", None, "56 BHOG", y=700, size=200, color=(255, 214, 150))], caps=cap(at("इसीलिए"), "KAL: ANNAKUT", "56 BHOG KYUN? KAL BATAYENGE", GOLD, at("अन्नकूट")), grade=None, trans="whip")),
        (at("और परसों"), kd.BG_plate("night"), dict(caps=cap(at("और परसों"), "PARSON: PAANCHVA DIYA", "BHAI DOOJ", GOLD, at("भाई दूज")),
                                                   over=[kdextra.five_diyas(at("और परसों") + 0.1, 4),
                                                         kd.chips_at([(at("यमराज"), "YAMRAJ + BEHEN YAMUNA", "c", 1330, {"size": 46}),
                                                                      (T.end + 0.2, "FOLLOW · KATHA DEEP", "c", 1470, {"size": 44})])],
                                                   fx=[kd.embers(40, 14, (255, 200, 120), 60, 0.6)], grade=None, trans="zoom")),
    ]
    return kdv2.keyword_shots(S, END)


def audio():
    import music, mixlib  # noqa: E401
    sa = 146.83   # D
    sec = [(0, at("कल गोवर्धन"), {"pad": 0.8, "sub": 0.7, "pad_bright": 600}),
           (at("कल गोवर्धन") - 0.3, at("इंद्र का अहंकार"), {"tanpura": 0.9, "pad": 0.4, "drums": 0.45}),
           (at("इंद्र का अहंकार") - 0.3, at("और तब"), {"pad": 0.9, "sub": 1.0, "drums": 0.9, "pad_bright": 400}),
           (at("और तब") - 0.3, at("इंद्र का घमंड"), {"tanpura": 1.0, "pad": 0.9, "sub": 0.6, "pad_bright": 1800}),
           (at("इंद्र का घमंड") - 0.3, END, {"tanpura": 0.9, "pad": 0.7, "drums": 0.5, "pad_bright": 1400})]
    hits = [(0.05, "boom", 0.9), (at("उसके हाथ"), "boom", 0.9), (at("कल गोवर्धन"), "bell", 0.5), (at("इंद्र का अहंकार"), "boom", 1.0),
            (at("बिजली"), "boom", 1.0), (at("और तब"), "bellhi", 0.6), (at("उठा लिया"), "boom", 1.0), (at("गोविंद"), "bell", 0.8),
            (at("और परसों"), "bell", 0.5), (T.end, "bell", 0.6)]
    mel = (at("उठा लिया") + 0.5, [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11), (7.6, 2.8, 7)])
    st = music.score(END, sa, sec, hits, mel, bpm=96, seed=8)
    cues = [(0.0, "deep-wind-hum", -15, {"max_len": 4, "fade_out": 1.5}), (at("उसके हाथ") - 0.1, "big-impact", -13),
            (at("कल गोवर्धन") - 0.2, "whoosh-transition", -17), (at("यज्ञ होता"), "campfire-crackles", -18, {"max_len": 2.3, "fade_out": 0.6}),
            (at("बारिश देते"), "river-water", -24, {"max_len": 1.6, "fade_out": 0.6}),
            (at("इंद्र का अहंकार") - 0.1, "trailer-impact", -12), (at("प्रलय") - 0.3, "distant-thunder", -12),
            (at("मूसलाधार") - 0.2, "river-water", -17, {"max_len": 10, "fade_out": 2.5}), (at("आँधी") - 0.2, "wind-swoosh", -14),
            (at("बिजली"), "big-impact", -11), (at("बिजली") + 0.1, "distant-thunder", -12),
            (at("सब दौड़े") - 0.2, "whoosh-fast", -17), (at("और तब") - 0.4, "cinematic-synth-riser", -17, {"max_len": 2.2, "fade_out": 0.3}),
            (at("उठा लिया") - 0.05, "whoosh-deep-impact", -11), (at("उठा लिया") + 0.1, "light-energy", -16),
            (at("इंद्र का घमंड") - 0.1, "reverse-impact", -15), (at("कामधेनु") - 0.1, "harp-sweep", -15),
            (at("गोविंद") - 0.1, "magic-sparkle", -15), (at("और परसों") - 0.2, "bell-chime", -16)]
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
