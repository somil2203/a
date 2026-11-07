"""Sone ki Lanka · Kuber · PART 2 (continues Dhanteras Special 2, which ended:
'Par Ravan aur Kuber ki kahani mein ek mod abhi baaki hai. Part 2 kal.')
Sources: Valmiki Ramayana, Uttarakanda 13-15 (Kubera's envoy killed, Alaka attacked, Pushpaka taken) and
Uttarakanda 26 (Rambha; Nalakubara's curse: head splits into seven pieces). Variant flagged on screen:
Yuddhakanda 13 (Ravana cites Brahma's curse after Punjikasthala). Tease: Bhagavata Purana 10.10 (Nalakubara freed by Krishna).
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
from kd import CREAM, GOLD, RED, Scene, W, H  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

A = f"{KD}/art/full"
T = kd.Timing(HERE)
at = T.at
END = T.end + 1.8
TAG = "KUBER KI LANKA · PART 2"
MET = "ART: THE MET · OPEN ACCESS (CC0)"
REF = {"size": 30, "fg": CREAM, "border": (200, 160, 100)}


def family_tree(ts):
    """Vishrava -> Kuber, Ravan ; Kuber -> Nalakubar ; Rambha linked to Nalakubar."""
    nodes = {"VISHRAVA": (540, 640, 0.0), "KUBER": (300, 900, 0.3), "RAVAN": (780, 900, 0.5),
             "NALAKUBAR": (300, 1180, at("नलकूबर के पास") - ts), "RAMBHA": (300, 1450, at("रिश्ते में") - ts)}
    edges = [("VISHRAVA", "KUBER"), ("VISHRAVA", "RAVAN"), ("KUBER", "NALAKUBAR"), ("NALAKUBAR", "RAMBHA")]

    def f(base, t, sc):
        lt = t - ts
        d = ImageDraw.Draw(base)
        for a_, b_ in edges:
            if lt < nodes[b_][2]:
                continue
            k = kd.eo((lt - nodes[b_][2]) / 0.35)
            x0, y0 = nodes[a_][:2]
            x1, y1 = nodes[b_][:2]
            d.line((x0, y0 + 40, x0 + (x1 - x0) * k, y0 + 40 + (y1 - y0 - 80) * k), fill=(222, 172, 92), width=5)
        for n, (x, y, t0) in nodes.items():
            if lt < t0:
                continue
            k = kd.eo((lt - t0) / 0.3)
            col = RED if n == "RAVAN" else GOLD
            c = kd.chip(n, 52, col, col)
            kd.paste_fade(base, c, (x - c.width / 2, y - c.height / 2), k)
        if lt > nodes["RAMBHA"][2]:
            lab = kd.text_img("RISHTE MEIN RAVAN KI BAHU", "mono", 28, CREAM)
            kd.paste_fade(base, lab, (560, 1430), kd.eo((lt - nodes["RAMBHA"][2]) / 0.3))
    return f


def recap(ts):
    def f(base, t, sc):
        for i, (txt, dt) in enumerate((("LANKA", 0.0), ("PUSHPAK VIMAN", at("पुष्पक") - ts))):
            if t < ts + dt:
                continue
            k = kd.eo((t - ts - dt) / 0.3)
            c = kd.chip(txt, 70, CREAM, (200, 160, 100))
            x, y = W / 2 - c.width / 2, 820 + i * 220
            kd.paste_fade(base, c, (x, y), k)
            ks = kd.eo((t - ts - dt - 0.5) / 0.3)
            if ks > 0:
                d = ImageDraw.Draw(base)
                d.line((x + 10, y + c.height / 2, x + 10 + (c.width - 20) * ks, y + c.height / 2), fill=RED, width=12)
    return f


def shatter(ts):
    """Big '7' that splits into seven shards (the curse)."""
    rng = random.Random(4)
    shards = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-3, 3)) for _ in range(7)]

    def f(base, t, sc):
        if t < ts:
            return
        lt = t - ts
        im = kd.text_img("7", "anton", 640, RED)
        if lt < 0.9:
            kd.paste_fade(base, im, (W / 2 - im.width / 2, 650), kd.eo(lt / 0.2))
            return
        k = kd.eo((lt - 0.9) / 0.8)
        w, h = im.size
        for i, (dx, dy, rot) in enumerate(shards):
            m = Image.new("L", (w, h), 0)
            ImageDraw.Draw(m).rectangle((0, h * i / 7, w, h * (i + 1) / 7 + 2), fill=255)
            p = im.copy()
            p.putalpha(Image.fromarray((__import__("numpy").minimum(__import__("numpy").array(im.split()[3]), __import__("numpy").array(m)))))
            p = p.rotate(rot * 8 * k, Image.BICUBIC, expand=False)
            kd.paste_fade(base, p, (W / 2 - w / 2 + dx * 260 * k, 650 + dy * 160 * k), 1 - 0.35 * k)
    return f


def drops():
    e = kd.Embers(70, 12, (120, 200, 255), 60, (2, 5))
    return lambda base, t, sc: e.draw(base, -t, 0.8)   # falling


def scenes():
    s = []
    s.append(Scene(0, at("जवाब"), kd.BG_kb(f"{A}/454357.jpg", (0.50, 0.32, 0.95), (0.48, 0.24, 0.62)),
                   caps=[(0.0, "SITA LANKA MEIN QAID", "PAR RAVAN CHHOO NA SAKA", RED, at("पर छू"))],
                   over=[kd.big_text(at("क्यों?"), "KYUN?", 1250, 230, GOLD)], credit=MET, grade_kind="ember",
                   flash=(0, 0.4, (0, 0, 0))))
    s.append(Scene(at("जवाब"), at("कल हमने"), kd.BG_kb(f"{A}/39232.jpg", (0.5, 0.55, 0.95), (0.5, 0.48, 0.62)),
                   caps=[(at("जवाब"), "JAWAB CHHIPA HAI", "KUBER KE GHAR MEIN", GOLD, at("कुबेर के घर"))], credit=MET, grade_kind="warm"))
    s.append(Scene(at("कल हमने"), at("वाल्मीकि"), kd.BG_plate("red"), fx=[recap(at("कल हमने") + 0.6)],
                   caps=[(at("कल हमने"), "KAL HUMNE DEKHA:", "KUBER SE CHHINE", RED, at("कुबेर से छिन")),
                         (at("पर रावण यहीं"), "PAR RAVAN", "YAHIN NAHI RUKA", RED, at("नहीं रुका"))], grade_kind=None))
    s.append(Scene(at("वाल्मीकि"), at("रावण ने उस"), kd.BG_kb(f"{A}/37954.jpg", (0.40, 0.40, 0.38), (0.44, 0.36, 0.24)),
                   caps=[(at("वाल्मीकि"), "VALMIKI RAMAYAN:", "UTTARAKAND", GOLD, at("उत्तरकांड")),
                         (at("कुबेर ने दूत"), "KUBER KA DOOT:", "'ADHARM CHHODO'", GOLD, at("अधर्म"))],
                   over=[kd.chips_at([(at("उत्तरकांड"), "VALMIKI RAMAYANA · UTTARAKANDA 13–15", "c", 1690, REF)])],
                   credit=MET, grade_kind="warm"))
    s.append(Scene(at("रावण ने उस"), at("अलकापुरी"), kd.BG_kb(f"{A}/454358.jpg", (0.62, 0.40, 0.62), (0.64, 0.44, 0.44)),
                   caps=[(at("रावण ने उस"), "RAVAN NE DOOT KO", "MAAR DALA", RED, at("मार डाला"))],
                   shake=(at("मार डाला"), 0.6), flash=(at("मार डाला"), 0.25, (200, 30, 20)), credit=MET, grade_kind="ember"))
    s.append(Scene(at("अलकापुरी"), at("फिर एक रात"), kd.BG_kb(f"{A}/454358.jpg", (0.45, 0.80, 0.72), (0.55, 0.82, 0.50)),
                   caps=[(at("अलकापुरी"), "AUR HAMLA:", "ALAKAPURI PAR", RED, at("चढ़ाई"))], credit=MET, grade_kind="ember"))
    s.append(Scene(at("फिर एक रात"), at("रम्भा पर"), kd.BG_kb(f"{A}/74682.jpg", (0.5, 0.55, 0.85), (0.5, 0.62, 0.62)),
                   caps=[(at("फिर एक रात"), "EK RAAT,", "KAILASH KE PAAS", GOLD, at("कैलाश"))], credit=MET, grade_kind="ember"))
    s.append(Scene(at("रम्भा पर"), at("रम्भा ने"), kd.BG_kb(f"{A}/38419.jpg", (0.5, 0.45, 0.46), (0.5, 0.38, 0.34)),
                   caps=[(at("रम्भा पर"), "APSARA", "RAMBHA", GOLD, at("रम्भा पर"))], credit=MET, grade_kind="warm"))
    s.append(Scene(at("रम्भा ने"), at("पर ताक़त"), kd.BG_plate("red"), fx=[family_tree(at("रम्भा ने"))],
                   caps=[(at("रम्भा ने"), "RAMBHA NE", "HAATH JODE", GOLD, at("हाथ जोड़े"))], grade_kind=None))
    s.append(Scene(at("पर ताक़त"), at("जब नलकूबर"), kd.BG_plate("red"),
                   fx=[kd.light_glow(0.5, 0.6, 380, (200, 30, 20), 0.5, 0.35)],
                   caps=[(at("पर ताक़त"), "TAAQAT KE NASHE MEIN", "EK NA SUNI", RED, at("एक न सुनी"))], grade_kind=None))
    s.append(Scene(at("जब नलकूबर"), at("आज के बाद"), kd.BG_plate("teal"), fx=[drops(), kd.light_glow(0.5, 0.6, 300, (140, 210, 255), 0.6, 0.15)],
                   caps=[(at("जब नलकूबर"), "NALAKUBAR NE", "HAATH MEIN JAL LIYA", GOLD, at("हाथ में जल")),
                         (at("श्राप दिया"), "AUR DIYA:", "SHRAAP", RED, at("श्राप दिया"))], grade_kind=None))
    s.append(Scene(at("आज के बाद"), at("और यहीं से"), kd.BG_plate("red"), fx=[shatter(at("सात टुकड़ों"))],
                   caps=[(at("आज के बाद"), "STREE KO ICHCHHA", "KE BINA CHHUA...", RED, at("इच्छा के बिना")),
                         (at("सात टुकड़ों"), "...TO SIR KE", "7 TUKDE", RED, at("सात टुकड़ों"))],
                   over=[kd.chips_at([(at("आज के बाद") + 0.3, "VALMIKI RAMAYANA · UTTARAKANDA 26", "c", 1690, REF)])],
                   shake=(at("सात टुकड़ों") + 0.9, 0.5), grade_kind=None))
    s.append(Scene(at("और यहीं से"), at("रावण धमकाता"), kd.BG_kb(f"{A}/38036.jpg", (0.60, 0.58, 0.30), (0.62, 0.60, 0.22)),
                   caps=[(at("और यहीं से"), "YAHIN SE", "KAHANI MUDTI HAI", GOLD, at("मुड़ती")),
                         (at("अशोक वाटिका"), "SITA:", "MAHINON QAID MEIN", GOLD, at("महीनों"))], credit=MET, grade_kind="warm"))
    s.append(Scene(at("रावण धमकाता"), at("एक बात और"), kd.BG_plate("red"), fx=[kd.light_glow(0.5, 0.55, 420, (190, 20, 10), 0.45, 0.4)],
                   over=[kd.big_text(at("पर छू नहीं"), "CHHOO NAHI SAKA", 900, 150, GOLD)],
                   caps=[(at("रावण धमकाता"), "RAVAN DHAMKATA RAHA,", "DARATA RAHA...", RED, at("डराता"))], grade_kind=None))
    s.append(Scene(at("एक बात और"), at("जिस कुबेर"), kd.BG_plate("night"),
                   over=[kd.chips_at([(at("एक बात और") + 0.2, "UTTARAKAND 26 · NALAKUBAR KA SHRAAP", "c", 820, {"size": 40}),
                                      (at("युद्धकांड"), "YUDDHAKAND 13 · BRAHMA KA SHRAAP", "c", 960, {"size": 40})])],
                   caps=[(at("एक बात और"), "EK BAAT AUR:", None, None),
                         (at("ग्रंथ में"), "DO PRASANG,", "SEEKH EK", GOLD, at("सीख एक"))], grade_kind=None))
    s.append(Scene(at("जिस कुबेर"), at("धन छीना"), kd.BG_kb(f"{A}/37532.jpg", (0.5, 0.55, 0.92), (0.5, 0.45, 0.58)),
                   caps=[(at("जिस कुबेर"), "KUBER KA DHAN CHHEENA...", None, None),
                         (at("उसी कुबेर"), "KUBER KE BETE KA SHRAAP:", "SITA KI DHAAL", GOLD, at("सीता की ढाल"))], credit=MET, grade_kind="warm"))
    s.append(Scene(at("धन छीना"), at("और नलकूबर"), kd.BG_kb(f"{A}/72821.jpg", (0.45, 0.40, 0.55), (0.50, 0.45, 0.38)),
                   caps=[(at("धन छीना") - 0.4, "DHAN CHHEENA JA SAKTA HAI.", "MARYADA NAHI.", GOLD, at("धन छीना") + 1.9)], credit=MET, grade_kind="warm"))
    s.append(Scene(at("और नलकूबर"), END, kd.BG_kb(f"{A}/37939.jpg", (0.55, 0.70, 0.60), (0.58, 0.80, 0.40)),
                   caps=[(at("और नलकूबर"), "NALAKUBAR KI", "APNI KAHANI?", GOLD, at("अपनी कहानी")),
                         (at("श्रीकृष्ण ने"), "KRISHNA NE", "MUKT KIYA", GOLD, at("मुक्त"))],
                   over=[kd.chips_at([(at("फ़ॉलो"), "FOLLOW · KATHA DEEP", "c", 1560, {"size": 50}),
                                      (at("श्रीकृष्ण ने"), "BHAGAVATA PURANA 10.10", "c", 1690, REF)])],
                   credit=MET, grade_kind="warm"))
    return s


def audio():
    import music
    import mixlib
    sa = 138.59  # C# — Marwa colour (Sa re Ga Ma# Dha Ni): unresolved, tense
    sec = [(0, at("कल हमने"), {"pad": 0.9, "sub": 0.8, "pad_bright": 600, "pad_ratios": (1, 1.06, 1.5, 2)}),
           (at("कल हमने") - 0.3, at("फिर एक रात"), {"tanpura": 0.8, "drums": 0.6, "sub": 0.4}),
           (at("फिर एक रात") - 0.3, at("जब नलकूबर"), {"tanpura": 0.9, "pad": 0.6, "pad_bright": 900}),
           (at("जब नलकूबर") - 0.3, at("और यहीं से"), {"pad": 0.9, "sub": 0.9, "pad_bright": 500, "pad_ratios": (1, 1.06, 1.5, 2)}),
           (at("और यहीं से") - 0.3, at("जिस कुबेर"), {"tanpura": 0.9, "drums": 0.5}),
           (at("जिस कुबेर") - 0.3, END, {"tanpura": 1.0, "pad": 0.8, "pad_bright": 1500})]
    hits = [(0.05, "boom", 1.0), (at("क्यों?"), "bayan", 0.9), (at("जवाब"), "bell", 0.5), (at("मार डाला"), "boom", 0.8),
            (at("श्राप दिया"), "boom", 0.9), (at("सात टुकड़ों") + 0.9, "boom", 0.9), (at("अशोक वाटिका"), "bellhi", 0.4),
            (at("जिस कुबेर"), "bell", 0.6), (at("धन छीना"), "bellhi", 0.5), (T.end, "bell", 0.6)]
    mel = (at("जिस कुबेर") + 0.4, [(0, 1.0, 11), (1.0, 1.4, 9), (2.6, 0.6, 6), (3.2, 2.2, 4), (5.6, 0.8, 1), (6.4, 2.6, 0),
                                     (9.4, 0.8, -1), (10.2, 3.0, 0)])
    st = music.score(END, sa, sec, hits, mel, bpm=80, seed=2)
    cues = [(0.0, "deep-wind-hum", -14, {"max_len": 5, "fade_out": 2}),
            (at("जवाब") - 0.2, "whoosh-transition", -16),
            (at("कल हमने") - 0.2, "whoosh-fast", -16),
            (at("पुष्पक"), "sword-slash", -20),
            (at("रावण ने उस") - 0.2, "whoosh-deep-impact", -15),
            (at("मार डाला"), "big-impact", -14),
            (at("अलकापुरी"), "distant-thunder", -15),
            (at("फिर एक रात") - 0.2, "wind-swoosh", -16),
            (at("रम्भा पर"), "harp-sweep", -15),
            (at("पर ताक़त"), "heartbeat-impact", -13),
            (at("हाथ में जल"), "water-splash", -14),
            (at("श्राप दिया") - 0.1, "trailer-impact", -12),
            (at("सात टुकड़ों") + 0.85, "sword-slash", -13),
            (at("और यहीं से") - 0.3, "reverse-impact", -15),
            (at("एक बात और") - 0.2, "whoosh-transition", -17),
            (at("धन छीना") - 0.3, "bell-chime", -15),
            (at("और नलकूबर") - 0.2, "magic-sparkle", -16)]
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
