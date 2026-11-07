"""Deepotsav · Din 2/5 — Chhoti Diwali / Narak Chaturdashi (continues Deepotsav Din 1, which ended:
'Kal doosra diya, Chhoti Diwali aur Narakasur ki kahani. Follow kar lijiye, paanchon diye saath jalayenge.')
Source: Bhagavata Purana 10.59 (Bhaumasura/Naraka; Mura; Aditi's earrings, Varuna's umbrella; 16,000 princesses
sent to Dvaraka). Satyabhama slaying Naraka is presented as folk tradition, not as the Bhagavata account.
usage: python3 edit.py [picture|still T..|audio|all]
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
from kd import CREAM, GOLD, RED, Scene, W, H  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

A = f"{KD}/art/full"
R3 = f"{KD}/renders3d"
T = kd.Timing(HERE)
at = T.at
END = T.end + 1.8
TAG = "DEEPOTSAV · DIN 2/5"
MET = "ART: THE MET · OPEN ACCESS (CC0)"


def BG_bars():
    """Captivity: dark plate behind iron bars, a big counter."""
    def f(lt, fr, fi):
        im = kd.mandala_plate("red").convert("RGBA")
        ov = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(ov)
        for i in range(9):
            x = 40 + i * 125 + 14 * math.sin(lt * 0.3)
            d.rectangle((x, 0, x + 26, H), fill=(14, 6, 6, 235))
            d.rectangle((x + 4, 0, x + 9, H), fill=(80, 50, 40, 160))
        d.rectangle((0, 1380, W, 1412), fill=(14, 6, 6, 235))
        im.alpha_composite(ov)
        return im.convert("RGB")
    return f


def counter(ts, y=780):
    def f(base, t, sc):
        if t < ts:
            return
        k = kd.eo((t - ts) / 1.6)
        v = int(16000 * k) // 100 * 100 if k < 1 else 16000
        im = kd.text_img(f"{v:,}", "anton", 260, CREAM)
        kd.paste_fade(base, im, (W / 2 - im.width / 2, y), min(1, (t - ts) / 0.2))
    return f


def diya_icon(lit, glow=False, size=150):
    im = Image.new("RGBA", (size + 80, size + 120))
    d = ImageDraw.Draw(im)
    cx, cy = (size + 80) / 2, size * 0.9
    d.chord((cx - size / 2, cy - size * 0.45, cx + size / 2, cy + size * 0.45), 0, 180, fill=(196, 92, 40, 255) if lit else (110, 60, 40, 255))
    d.polygon([(cx + size / 2 - 6, cy), (cx + size / 2 + 26, cy - 14), (cx + size / 2 - 2, cy + 18)], fill=(196, 92, 40, 255) if lit else (110, 60, 40, 255))
    if lit or glow:
        fl = Image.new("RGBA", im.size)
        fd = ImageDraw.Draw(fl)
        fd.ellipse((cx + size / 2 - 4, cy - 70, cx + size / 2 + 26, cy + 2), fill=(255, 200, 90, 255 if lit else 90))
        im.alpha_composite(fl.filter(ImageFilter.GaussianBlur(10)))
        im.alpha_composite(fl.filter(ImageFilter.GaussianBlur(2)))
    return im


def five_diyas(ts, y=1060):
    names = ["DHANTERAS", "CHHOTI\nDIWALI", "LAKSHMI\nPUJA", "GOVARDHAN", "BHAI\nDOOJ"]

    def f(base, t, sc):
        if t < ts:
            return
        for i, n in enumerate(names):
            k = kd.eo((t - ts - i * 0.12) / 0.3)
            if k <= 0:
                continue
            ic = diya_icon(i < 2, glow=(i == 2 and math.sin(t * 6) > -0.2))
            x = 30 + i * 206
            kd.paste_fade(base, ic, (x, y + 20 * (1 - k)), k)
            for j, ln in enumerate(n.split("\n")):
                lab = kd.text_img(ln, "mono", 24, GOLD if i < 2 else (200, 180, 160))
                kd.paste_fade(base, lab, (x + ic.width / 2 - lab.width / 2, y + 190 + j * 30), k)
    return f


def scenes():
    s = []
    s.append(Scene(0, at("और उन्हें"), BG_bars(), fx=[counter(0.1)],
                   caps=[(0.0, "RAJKUMARIYAN", "EK ASUR KI QAID MEIN", RED, at("एक असुर"))], grade_kind=None, flash=(0, 0.4, (0, 0, 0))))
    s.append(Scene(at("और उन्हें"), at("दिवाली के"), kd.BG_kb(f"{A}/37849.jpg", (0.30, 0.42, 0.30), (0.27, 0.33, 0.20)),
                   caps=[(at("और उन्हें"), "CHHUDANE AAYE", "SHRI KRISHNA", GOLD, at("श्रीकृष्ण")),
                         (at("गरुड़ पर"), "GARUD PAR,", "SATYABHAMA KE SAATH", GOLD, at("सत्यभामा"))],
                   credit=MET, grade_kind="warm"))
    s.append(Scene(at("दिवाली के"), at("भागवत"), kd.BG_kb(f"{R3}/diyas2.png", (0.5, 0.5, 1.0), (0.5, 0.56, 0.82)),
                   caps=[(at("दिवाली के"), "5 DIN · 5 DIYE", "5 KAHANIYAN", GOLD, at("पाँच कहानियाँ")),
                         (at("आज दूसरा"), "AAJ DOOSRA DIYA:", "CHHOTI DIWALI", GOLD, at("छोटी दिवाली"))],
                   fx=[kd.flicker(0.08), kd.embers(30, 2, (255, 170, 80), 60, 0.6)], grade_kind="flame"))
    s.append(Scene(at("भागवत"), at("राजधानी"), kd.BG_plate("red"),
                   fx=[kd.chips_at([(at("भूमि"), "BHUMI DEVI", "c", 760, {"size": 60}),
                                    (at("भौमासुर"), "PUTRA: BHAUMASUR", "c", 940, {"size": 60, "fg": RED, "border": RED}),
                                    (at("नरकासुर कहती"), "= NARAKASUR", "c", 1120, {"size": 72, "fg": RED, "border": RED})])],
                   caps=[(at("भागवत"), "BHAGAVAT PURAN:", None, None),
                         (at("भूमि"), "BHUMI DEVI KA PUTRA", "BHAUMASUR", RED, at("भौमासुर")),
                         (at("दुनिया उसे"), "DUNIYA KAHTI HAI:", "NARAKASUR", RED, at("नरकासुर कहती"))],
                   over=[kd.chips_at([(at("भागवत") + 0.3, "BHAGAVATA PURANA 10.59", "c", 1690, {"size": 30, "fg": CREAM, "border": (200, 160, 100)})])],
                   grade_kind=None))
    s.append(Scene(at("राजधानी"), at("देवमाता"), kd.BG_kb(f"{A}/37849.jpg", (0.72, 0.40, 0.28), (0.74, 0.36, 0.20)),
                   caps=[(at("राजधानी"), "RAJDHANI:", "PRAGJYOTISHPUR", GOLD, at("प्रागज्योतिषपुर")),
                         (at("ताक़त"), "TAAQAT KA", "GHAMAND", RED, at("घमंड"))],
                   credit=MET, grade_kind="ember"))
    s.append(Scene(at("देवमाता"), at("और हज़ारों"), kd.BG_layer(kd.BG_plate("red"), f"{R3}/kundal.png", 0.5, 0.56, 0.95, 1.05, glow=(255, 190, 90)),
                   over=[kd.chips_at([(at("देवमाता"), "CHHEENE: ADITI KE KUNDAL", "c", 1500, {"size": 46}),
                                      (at("वरुण"), "CHHEENA: VARUN KA CHHATRA", "c", 1610, {"size": 46})])],
                   caps=[(at("देवमाता"), "DEVTAON SE", "CHHEENA", RED, at("कुंडल"))], grade_kind=None))
    s.append(Scene(at("और हज़ारों"), at("देवराज"), kd.BG_kb(f"{A}/37846.jpg", (0.46, 0.33, 0.30), (0.40, 0.30, 0.24)),
                   caps=[(at("और हज़ारों"), "HAZARON RAJKUMARIYAN", "BANDI", RED, at("बंदी"))],
                   credit=MET, grade_kind="night"))
    s.append(Scene(at("देवराज"), at("और कृष्ण"), kd.BG_kb(f"{A}/38767.jpg", (0.5, 0.40, 0.85), (0.5, 0.25, 0.55)),
                   caps=[(at("देवराज"), "INDRA PAHUNCHE", "DWARKA", GOLD, at("द्वारका पहुँचे"))], credit=MET, grade_kind="warm"))
    s.append(Scene(at("और कृष्ण"), at("किले"), kd.BG_kb(f"{A}/822850.jpg", (0.5, 0.60, 0.70), (0.5, 0.42, 0.50)),
                   caps=[(at("और कृष्ण"), "GARUD PAR", "UD CHALE", GOLD, at("उड़ चले"))], credit=MET, grade_kind="warm"))
    ck = {"size": 42}
    s.append(Scene(at("किले"), at("सुदर्शन चक्र"), kd.BG_kb(f"{R3}/fort.png", (0.5, 0.55, 1.0), (0.5, 0.52, 0.72)),
                   caps=[(at("किले"), "KILE KE CHAARON OR:", "5 DEEWAREIN", GOLD, at("पहाड़")),
                         (at("और पहरे"), "PEHRE PAR:", "MUR · 5 SIR", RED, at("मुर।"))],
                   over=[kd.chips_at([(at("पहाड़"), "PAHAD", 60, 1520, ck), (at("शस्त्र"), "SHASTRA", 290, 1520, ck),
                                      (at("जल,"), "JAL", 560, 1520, ck), (at("अग्नि"), "AGNI", 720, 1520, ck),
                                      (at("वायु"), "VAYU", 890, 1520, ck)])],
                   fx=[kd.embers(40, 3, (255, 140, 60), 90, 0.7)], grade_kind=None))
    s.append(Scene(at("सुदर्शन चक्र"), at("फिर नरकासुर"),
                   kd.BG_layer(kd.BG_plate("red"), f"{R3}/chakra.png", 0.5, 0.58, 0.85, 1.0, rot_speed=220, glow=(255, 170, 60)),
                   caps=[(at("सुदर्शन चक्र"), "SUDARSHAN", "CHAKRA", GOLD, at("चक्र चला")),
                         (at("कट गए"), "MUR KA ANT", None, None),
                         (at("मुरारी"), "TABHI SE KRISHNA =", "MURARI", GOLD, at("मुरारी"))],
                   flash=(at("कट गए"), 0.35, (255, 220, 160)), grade_kind=None))
    s.append(Scene(at("फिर नरकासुर"), at("कई लोक"), kd.BG_kb(f"{A}/74649.jpg", (0.62, 0.45, 0.42), (0.66, 0.40, 0.30)),
                   caps=[(at("फिर नरकासुर"), "NARAKASUR", "SAAMNE AAYA", RED, at("सामने")),
                         (at("उसका भी"), "SUDARSHAN SE", "NARAKASUR KA ANT", GOLD, at("अंत कर"))],
                   shake=(at("उसका भी"), 0.7), flash=(at("अंत कर"), 0.3, (255, 200, 140)), credit=MET, grade_kind="warm"))
    s.append(Scene(at("कई लोक"), at("भूमि देवी ने"), kd.BG_plate("night"),
                   over=[kd.chips_at([(at("कई लोक"), "BHAGAVAT PURAN · VADH: KRISHNA", "c", 820, {"size": 44}),
                                      (at("सत्यभामा के हाथों"), "LOK PARAMPARA · VADH: SATYABHAMA", "c", 960, {"size": 44, "fg": CREAM, "border": (200, 160, 100)})])],
                   caps=[(at("कई लोक"), "EK AUR", "PARAMPARA", GOLD, at("लोक-परंपराओं"))], grade_kind=None))
    s.append(Scene(at("भूमि देवी ने"), at("पर असली"), kd.BG_kb(f"{A}/849523.jpg", (0.5, 0.52, 0.95), (0.5, 0.45, 0.70)),
                   caps=[(at("भूमि देवी ने"), "BHUMI DEVI NE", "LAUTAYE KUNDAL + CHHATRA", GOLD, at("कुंडल और"))], credit=MET, grade_kind="warm"))
    s.append(Scene(at("पर असली"), at("कृष्ण ने सबको"), kd.BG_plate("night"),
                   over=[kd.big_text(at("अपनाएगा"), "?", 760, 520, GOLD)],
                   caps=[(at("पर असली"), "QAID SE CHHOOTI", "RAJKUMARIYAN...", CREAM, at("क़ैद से")),
                         (at("अपनाएगा"), "APNAYEGA", "KAUN?", RED, at("कौन"))], grade_kind=None))
    s.append(Scene(at("कृष्ण ने सबको"), at("इसीलिए"), kd.BG_kb(f"{A}/37846.jpg", (0.60, 0.62, 0.36), (0.52, 0.64, 0.28)),
                   caps=[(at("कृष्ण ने सबको"), "KRISHNA NE DIYA", "SAMMAN", GOLD, at("सम्मान")),
                         (at("द्वारका भेजकर"), "DWARKA BHEJA,", "PATNI KA PAD", GOLD, at("पत्नी का"))],
                   credit=MET, grade_kind="warm"))
    s.append(Scene(at("इसीलिए"), at("कल तीसरा"), kd.BG_kb(f"{R3}/diyas_close.png", (0.5, 0.5, 1.0), (0.52, 0.55, 0.80)),
                   caps=[(at("इसीलिए"), "ISILIYE AAJ:", "SUBAH SNAAN", GOLD, at("सुबह स्नान")),
                         (at("शाम को"), "SHAAM KO DIYA:", "QAID SE AZAADI", GOLD, at("आज़ादी"))],
                   fx=[kd.flicker(0.07), kd.embers(50, 5, (255, 180, 90), 80, 0.8)], grade_kind="flame"))
    s.append(Scene(at("कल तीसरा"), END, kd.BG_plate("red"), fx=[kd.embers(40, 9, (255, 180, 90), 60, 0.6)],
                   over=[five_diyas(at("कल तीसरा")),
                         kd.chips_at([(at("फ़ॉलो"), "FOLLOW · 5 DIN · 5 DIYE", "c", 1500, {"size": 50})])],
                   caps=[(at("कल तीसरा"), "KAL: DIN 3", "LAKSHMI PUJA", GOLD, at("लक्ष्मी पूजा"))], grade_kind=None))
    return s


def audio():
    import music
    import mixlib
    sa = 146.83  # D — Bhairav colour for the battle, resolving to Sa
    sec = [(0, at("दिवाली के"), {"pad": 0.8, "sub": 0.7, "pad_bright": 700, "tanpura": 0.4}),
           (at("दिवाली के") - 0.3, at("देवराज"), {"tanpura": 0.9, "pad": 0.5}),
           (at("देवराज") - 0.3, at("पर असली"), {"tanpura": 0.7, "drums": 0.9, "sub": 0.5}),
           (at("पर असली"), at("कृष्ण ने सबको"), {"pad": 0.6, "pad_bright": 500}),
           (at("कृष्ण ने सबको") - 0.2, END, {"tanpura": 1.0, "pad": 0.8, "drums": 0.45, "pad_bright": 1600})]
    hits = [(0.05, "boom", 1.0), (at("दिवाली के"), "bell", 0.6), (at("आज दूसरा"), "bellhi", 0.5),
            (at("सुदर्शन चक्र"), "boom", 0.8), (at("कट गए"), "bayan", 0.9), (at("उसका भी"), "boom", 0.8),
            (at("कृष्ण ने सबको"), "bell", 0.6), (at("कल तीसरा"), "bellhi", 0.6), (T.end, "bell", 0.7)]
    mel = (at("कृष्ण ने सबको") + 0.3, [(0, 0.8, 7), (0.8, 0.8, 8), (1.6, 1.6, 11), (3.4, 0.6, 12), (4.0, 2.2, 11),
                                        (6.4, 0.8, 8), (7.2, 2.0, 7), (9.4, 0.8, 5), (10.2, 0.8, 4), (11.0, 2.6, 1), (13.8, 3.2, 0)])
    st = music.score(END, sa, sec, hits, mel, bpm=92, seed=1)
    cues = [(0.0, "heartbeat-impact", -12), (0.4, "deep-wind-hum", -16, {"fade_out": 2, "max_len": 4}),
            (at("और उन्हें") - 0.25, "whoosh-fast", -14),
            (at("दिवाली के") - 0.2, "soft-fire-woosh", -14),
            (at("भागवत") - 0.2, "whoosh-transition", -17),
            (at("देवमाता"), "magic-sparkle", -16),
            (at("और हज़ारों") - 0.2, "deep-wind-hum", -17, {"max_len": 3, "fade_out": 1}),
            (at("और कृष्ण") - 0.1, "wind-swoosh", -12),
            (at("किले") - 0.2, "distant-thunder", -15),
            (at("अग्नि"), "fire-beam", -20, {"max_len": 2, "fade_out": 0.8}),
            (at("जल,"), "water-splash", -20),
            (at("सुदर्शन चक्र") - 0.1, "fast-sword-whoosh", -12),
            (at("कट गए"), "sword-slash", -12),
            (at("कट गए"), "big-impact", -15),
            (at("उसका भी"), "trailer-impact", -12),
            (at("कई लोक") - 0.2, "whoosh-transition", -17),
            (at("पर असली") - 0.2, "reverse-impact", -16),
            (at("इसीलिए") - 0.2, "campfire-crackles", -22, {"max_len": 5, "fade_out": 1.5}),
            (at("कल तीसरा"), "bell-chime", -14)]
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
