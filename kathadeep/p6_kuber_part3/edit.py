"""Kuber · PART 3 (finale) — Nalakubar & Manigriv. Continues Kuber Part 2 ('Nalakubar ki apni kahani?
Use ek din khud Shri Krishna ne mukt kiya tha'). Source: Bhagavata Purana 10.9 (Yashoda binds Krishna to the
mortar: Damodara) and 10.10 (Kubera's sons, intoxicated, Narada's curse to become twin arjuna trees in Nanda's
courtyard; Krishna drags the mortar between them, the trees fall, the brothers praise him).
Rule: whoever the narration names is on screen (Kuber, Narad, Yashoda & Kanha, the trees, the brothers).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd, kdextra, kdv2  # noqa: E401,E402
from kd import CREAM, GOLD, RED, Scene  # noqa: E402

A, R3 = f"{KD}/art/full", f"{KD}/renders3d"
T = kd.Timing(HERE); at = T.at; END = T.end + 1.8
TAG = "KUBER KI LANKA · PART 3"
kd.CAP_MODE = "mono"
kd.TRANS = "cut"
kd.SUBS = T; MET = "ART: THE MET · OPEN ACCESS (CC0)"
REF = {"size": 30, "fg": CREAM, "border": (200, 160, 100)}


def BG_sky(top=(126, 178, 230), low=(250, 214, 170)):
    """Daylight storybook sky with soft sun-rays (Gokul by day)."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    y = np.linspace(0, 1, kd.H)[:, None, None]
    a = np.array(top) * (1 - y) + np.array(low) * y
    sky = Image.fromarray(np.repeat(a, kd.W, 1).astype("uint8")).convert("RGBA")

    def f(lt, fr, fi):
        im = sky.copy()
        ov = Image.new("RGBA", im.size)
        d = ImageDraw.Draw(ov)
        cx, cy = kd.W * 0.8, kd.H * 0.12
        for i in range(12):
            import math
            a0 = i * 30 + lt * 3
            d.pieslice((cx - 1800, cy - 1800, cx + 1800, cy + 1800), a0, a0 + 9, fill=(255, 250, 225, 40))
        im.alpha_composite(ov.filter(ImageFilter.GaussianBlur(8)))
        return im.convert("RGB")
    return f


def scenes():
    s = []
    s.append(Scene(0, at("कल रावण"), kd.BG_kb(f"{R3}/trees.png", (0.5, 0.40, 0.90), (0.5, 0.34, 0.70)),
                   caps=[(0.0, "KUBER KE DO BETE", "DEVTAON JAISE AMEER", GOLD, 1.6),
                         (at("और फिर एक दिन"), "AUR PHIR EK DIN:", "DONO PED BAN GAYE", RED, at("दोनों पेड़"))],
                   grade_kind="warm", flash=(0, 0.4, (0, 0, 0))))
    s.append(Scene(at("कल रावण"), at("भागवत"), BG_sky(),
                   over=[kd.chips_at([(at("कल रावण") + 0.2, "PART 2: NALAKUBAR KA SHRAAP → RAVAN", "c", 820, {"size": 44})])],
                   caps=[(at("कल रावण"), "YAAD HAI", "NALAKUBAR?", GOLD, at("नलकूबर याद")), (at("आज उसी"), "AAJ:", "USI KI KAHANI", GOLD, at("उसी की"))], grade_kind=None))
    s.append(Scene(at("भागवत"), at("एक दिन कैलाश"), kd.BG_kb(f"{A}/38770.jpg", (0.5, 0.40, 0.85), (0.5, 0.33, 0.60)),
                   caps=[(at("भागवत"), "BHAGAVAT PURAN:", None, None),
                         (at("नलकूबर और"), "NALAKUBAR + MANIGRIV", "KUBER KE BETE", GOLD, at("कुबेर के बेटे")),
                         (at("धन था"), "DHAN, TAAQAT...", "AUR NASHA", RED, at("उसका नशा"))],
                   over=[kd.chips_at([(at("भागवत") + 0.3, "BHAGAVATA PURANA 10.10", "c", 300, REF), (at("नलकूबर और"), "KUBER (DHANADA) · PITA", "c", 400, {"size": 34})])],
                   credit=MET, grade_kind="warm"))
    s.append(Scene(at("एक दिन कैलाश"), at("तभी वहाँ"), BG_sky((70, 140, 170), (190, 225, 230)),
                   fx=[kd.light_glow(0.5, 0.75, 420, (120, 200, 255), 0.45, 0.25), kd.embers(60, 41, (150, 210, 255), 50, 0.6, (1, 4)), kdextra.two_princes(at("नशे में धुत"), y=820, h=300, color=(20, 30, 50), glow=(120, 190, 255))],
                   caps=[(at("एक दिन कैलाश"), "KAILASH KE PAAS,", "NADI MEIN", GOLD, at("नदी में")),
                         (at("नशे में धुत"), "NASHE MEIN DHUT", "DONO BHAI", RED, at("दोनों भाई"))], grade_kind=None))
    s.append(Scene(at("तभी वहाँ"), at("और श्राप"), kd.BG_kb(f"{A}/78252.jpg", (0.82, 0.42, 0.36), (0.84, 0.40, 0.26)),
                   caps=[(at("तभी वहाँ"), "TABHI AAYE:", "DEVARSHI NARAD", GOLD, at("देवर्षि नारद")),
                         (at("स्त्रियों ने"), "STRIYON NE VASTRA PEHNE...", "PAR UNHE HOSH NAHI", RED, at("पर कुबेर")),
                         (at("नारद ने देखा"), "DHAN KE AHANKAAR NE", "ANDHA KAR DIYA", RED, at("अंधा"))],
                   credit=MET, grade_kind="warm"))
    s.append(Scene(at("और श्राप"), at("दोनों गोकुल"), BG_sky(), fx=[kd.light_glow(0.5, 0.55, 380, (255, 190, 110), 0.5, 0.2)],
                   over=[kd.big_text(at("जाओ, पेड़"), "PED BAN JAO", 780, 170, RED),
                         kd.chips_at([(at("पर साथ में"), "KRIPA: BHAGWAN KHUD MUKT KARENGE", "c", 1000, {"size": 44})])],
                   caps=[(at("और श्राप"), "NARAD KA", "SHRAAP", RED, at("जाओ, पेड़"))], shake=(at("जाओ, पेड़"), 0.5), grade_kind=None))
    s.append(Scene(at("दोनों गोकुल"), at("फिर एक दिन,"), kd.BG_kb(f"{R3}/trees.png", (0.5, 0.55, 1.0), (0.5, 0.62, 0.82)),
                   caps=[(at("दोनों गोकुल"), "GOKUL, NAND BABA", "KA AANGAN", GOLD, at("आँगन")),
                         (at("अर्जुन के"), "ARJUN KE", "DO PED", GOLD, at("दो पेड़"))], grade_kind="warm"))
    s.append(Scene(at("फिर एक दिन,"), at("कान्हा ओखली"), kd.BG_kb(f"{A}/849507.jpg", (0.50, 0.42, 0.70), (0.40, 0.46, 0.46)),
                   caps=[(at("फिर एक दिन,"), "MAA YASHODA NE", "NATKHAT KANHA KO", GOLD, at("नटखट")),
                         (at("ओखली से"), "OKHLI SE", "BAANDH DIYA", GOLD, at("बाँध"))], credit=MET, grade_kind="warm"))
    s.append(Scene(at("कान्हा ओखली"), at("ओखली फँसी"), kd.BG_kb(f"{R3}/trees.png", (0.5, 0.70, 0.62), (0.5, 0.74, 0.46)),
                   caps=[(at("कान्हा ओखली"), "OKHLI GHASEET'TE KANHA", "DONO PEDON KE BEECH SE", GOLD, at("बीच से"))], grade_kind="warm"))
    s.append(Scene(at("ओखली फँसी"), at("पेड़ों से"), kd.BG_kb(f"{R3}/trees_fallen.png", (0.5, 0.62, 0.80), (0.5, 0.64, 0.62)),
                   caps=[(at("ओखली फँसी"), "OKHLI PHANSI...", "PED JAD SE UKHAD GAYE", RED, at("जड़ से"))],
                   shake=(at("जड़ से"), 0.8), flash=(at("जड़ से"), 0.25, (255, 230, 190)), grade_kind="warm"))
    s.append(Scene(at("पेड़ों से"), at("इसीलिए"), BG_sky((60, 80, 150), (240, 190, 140)), fx=[kdextra.two_princes(at("पेड़ों से") + 0.2, y=880, h=330)],
                   caps=[(at("पेड़ों से"), "PRAKAT HUE:", "NALAKUBAR + MANIGRIV", GOLD, at("प्रकट हुए") + 0.9),
                         (at("हाथ जोड़कर"), "HAATH JODKAR", "KRISHNA KI STUTI", GOLD, at("स्तुति"))], grade_kind=None))
    s.append(Scene(at("इसीलिए"), at("आज लक्ष्मी"), kd.BG_kb(f"{A}/39331.jpg", (0.5, 0.40, 0.80), (0.55, 0.35, 0.55)),
                   caps=[(at("इसीलिए"), "ISILIYE KRISHNA:", "DAMODAR", GOLD, at("दामोदर")),
                         (at("जिनके उदर"), "DAAM (RASSI) +", "UDAR (PET)", GOLD, at("रस्सी"))],
                   over=[kd.chips_at([(at("इसीलिए") + 0.3, "BHAGAVATA PURANA 10.9", "c", 300, REF)])], credit=MET, grade_kind="warm"))
    s.append(Scene(at("आज लक्ष्मी"), at("कुबेर की कहानी"), kd.BG_kb(f"{A}/39211.jpg", (0.45, 0.45, 0.85), (0.42, 0.32, 0.55)),
                   caps=[(at("आज लक्ष्मी"), "AAJ LAKSHMI-KUBER PUJA", None, None),
                         (at("कुबेर का वरदान"), "KUBER KA VARDAAN:", "DHAN", GOLD, at("है धन")),
                         (at("और उनके बेटों"), "BETON KI SEEKH:", "DHAN + VINAMRATA", GOLD, at("विनम्रता"))], credit=MET, grade_kind="warm"))
    s.append(Scene(at("कुबेर की कहानी"), END, BG_sky(), fx=[kd.embers(50, 43, (255, 190, 110), 70, 0.7)],
                   over=[kd.chips_at([(at("कुबेर की कहानी") + 0.3, "PART 1 · LANKA   PART 2 · SHRAAP   PART 3 · MUKTI", "c", 900, {"size": 36}),
                                      (at("कमेंट"), "COMMENT KARO: AGLI KAHANI?", "c", 1080, {"size": 50}),
                                      (at("कमेंट") + 0.3, "FOLLOW · KATHA DEEP", "c", 1230, {"size": 44})])],
                   caps=[(at("कुबेर की कहानी"), "KUBER KI KAHANI:", "POORI", GOLD, at("पूरी होती"))], grade_kind=None))
    TR = {at("कल रावण"): "whip", at("एक दिन कैलाश"): "whip", at("तभी वहाँ"): "zoom", at("और श्राप"): "zoom", at("दोनों गोकुल"): "whip", at("ओखली फँसी"): "flash", at("पेड़ों से"): "flash", at("इसीलिए"): "whip", at("कुबेर की कहानी"): "zoom"}
    for sc in s:
        sc.trans = TR.get(sc.t0, "cut")
    return kdv2.expand(s)


def audio():
    import music, mixlib  # noqa: E401
    sa = 138.59
    sec = [(0, at("कल रावण"), {"pad": 0.8, "sub": 0.6, "pad_bright": 700}),
           (at("कल रावण") - 0.3, at("तभी वहाँ"), {"tanpura": 0.8, "pad": 0.4}),
           (at("तभी वहाँ") - 0.3, at("दोनों गोकुल"), {"tanpura": 0.7, "pad": 0.7, "sub": 0.5, "pad_bright": 600}),
           (at("दोनों गोकुल") - 0.3, at("पेड़ों से"), {"tanpura": 0.8, "drums": 0.7}),
           (at("पेड़ों से") - 0.3, END, {"tanpura": 1.0, "pad": 0.9, "pad_bright": 1700})]
    hits = [(0.05, "boom", 0.9), (at("जाओ, पेड़"), "boom", 1.0), (at("दोनों गोकुल"), "bell", 0.5), (at("जड़ से"), "boom", 1.0),
            (at("पेड़ों से"), "bellhi", 0.7), (at("दामोदर"), "bell", 0.6), (T.end, "bell", 0.6)]
    mel = (at("पेड़ों से") + 0.4, [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11), (7.6, 2.8, 7)])
    st = music.score(END, sa, sec, hits, mel, bpm=92, seed=6)
    cues = [(0.0, "deep-wind-hum", -15, {"max_len": 4, "fade_out": 1.5}), (at("कल रावण") - 0.2, "whoosh-transition", -16),
            (at("एक दिन कैलाश") - 0.2, "river-water", -21, {"max_len": 7, "fade_out": 2}), (at("तभी वहाँ"), "harp-sweep", -15),
            (at("जाओ, पेड़"), "trailer-impact", -12), (at("दोनों गोकुल") - 0.2, "wind-swoosh", -17),
            (at("कान्हा ओखली"), "whoosh-fast", -17), (at("जड़ से") - 0.1, "big-impact", -12), (at("जड़ से"), "distant-thunder", -16),
            (at("पेड़ों से"), "light-energy", -16), (at("इसीलिए") - 0.2, "bell-chime", -16), (at("कुबेर की कहानी") - 0.2, "magic-sparkle", -16)]
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
