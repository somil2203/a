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
    """Keyword shot list: whatever word is spoken, its own picture is on screen (one image per keyword)."""
    P = lambda i, wf=0.72, mv="push", focus=None: kdv2.BG_auto(f"{A}/{i}.jpg", wf, mv, focus)
    R = lambda n, a, b, mv="push": kdv2.BG_para(f"{R3}/{n}.png", a, b, mv)
    sil = lambda col=(14, 8, 6), glow=(255, 214, 140), y=880: kdextra.two_princes(0, y=y, h=330, color=col, glow=glow)
    def cap(t, l1, l2=None, c=GOLD, t2=None):
        return [(t, l1, l2, c, t2)]
    S = [
        (0.0, P(38387, 0.85, "push"), dict(caps=cap(0, "KUBER KE DO BETE"), credit=MET, flash=(0, 0.3, (0, 0, 0)))),
        (at("देवताओं"), P(446749, 0.62, "orbit"), dict(caps=cap(at("देवताओं"), "DEVTAON JAISE AMEER"), credit=MET)),
        (at("और फिर एक दिन"), kdv2.BG_para(f"{A}/37939.jpg", (0.62, 0.55, 0.42), (0.62, 0.52, 0.34), "rise"), dict(caps=cap(at("और फिर एक दिन"), "AUR PHIR EK DIN: DONO PED BAN GAYE"), credit=MET, trans="zoom")),
        (at("कल रावण"), P(74475, 0.40, "left"), dict(caps=cap(at("कल रावण"), "RAVAN KO SHRAAP DENE WALA"), credit=MET, trans="whip")),
        (at("नलकूबर याद"), P(38468, 0.80, "push"), dict(caps=cap(at("नलकूबर याद"), "NALAKUBAR (YAKSH) YAAD HAI?"), credit=MET)),
        (at("आज उसी"), P(72618, 0.30, "left", focus=(0.30, 0.55)), dict(caps=cap(at("आज उसी"), "AAJ: USI KI KAHANI"), credit=MET)),
        (at("भागवत"), P(37855, 0.55, "right"), dict(caps=cap(at("भागवत"), "BHAGAVAT PURAN 10.10"), credit=MET, trans="whip")),
        (at("नलकूबर और"), P(38293, 0.80, "push"), dict(caps=cap(at("नलकूबर और"), "NALAKUBAR + MANIGRIV · KUBER KE BETE"), credit=MET)),
        (at("धन था"), P(39405, 0.80, "push"), dict(caps=cap(at("धन था"), "DHAN"), credit=MET, trans="zoom")),
        (at("ताक़त थी"), P(38936, 0.80, "rise"), dict(caps=cap(at("ताक़त थी"), "TAAQAT"), credit=MET)),
        (at("उसका नशा"), P(56203, 0.42, "orbit", focus=(0.32, 0.52)), dict(caps=cap(at("उसका नशा"), "AUR NASHA", c=RED), credit=MET, trans="zoom")),
        (at("एक दिन कैलाश"), P(849508, 0.70, "fall"), dict(caps=cap(at("एक दिन कैलाश"), "KAILASH KE PAAS"), credit=MET, trans="whip")),
        (at("नदी में"), P(765654, 0.32, "left", focus=(0.22, 0.45)), dict(caps=cap(at("नदी में"), "NADI MEIN"), credit=MET)),
        (at("नशे में धुत"), P(54183, 0.45, "right"), dict(caps=cap(at("नशे में धुत"), "NASHE MEIN DHUT", c=RED), credit=MET)),
        (at("स्त्रियों के साथ"), P(454054, 0.45, "right"), dict(caps=cap(at("स्त्रियों के साथ"), "JAL-KREEDA"), credit=MET)),
        (at("तभी वहाँ"), kdv2.BG_para(f"{A}/78252.jpg", (0.82, 0.42, 0.36), (0.84, 0.40, 0.27), "push"), dict(caps=cap(at("तभी वहाँ"), "DEVARSHI NARAD"), credit=MET, trans="zoom")),
        (at("स्त्रियों ने"), P(73148, 0.70, "fall"), dict(caps=cap(at("स्त्रियों ने"), "STRIYON NE VASTRA PEHNE"), credit=MET)),
        (at("पर कुबेर"), P(38475, 0.55, "push"), dict(caps=cap(at("पर कुबेर"), "PAR UNHE HOSH NAHI", c=RED), credit=MET)),
        (at("नारद ने देखा"), P(446266, 0.55, "left"), dict(caps=cap(at("धन के"), "DHAN KA AHANKAAR = ANDHAPAN", c=RED), credit=MET, trans="zoom")),
        (at("और श्राप"), P(765654, 0.32, "rise", focus=(0.78, 0.40)), dict(caps=cap(at("और श्राप"), "NARAD KA SHRAAP:", "PED BAN JAO", RED, at("जाओ, पेड़")), credit=MET, shake=(at("जाओ, पेड़"), 0.5), trans="flash")),
        (at("पर साथ में"), P(38517, 0.60, "rise"), dict(caps=cap(at("पर साथ में"), "PAR SAATH MEIN KRIPA"), credit=MET)),
        (at("एक दिन स्वयं"), P(72719, 0.55, "push"), dict(caps=cap(at("एक दिन स्वयं"), "BHAGWAN KHUD MUKT KARENGE"), credit=MET, trans="zoom")),
        (at("दोनों गोकुल"), P(37848, 0.38, "left"), dict(caps=cap(at("दोनों गोकुल"), "GOKUL · NAND BABA KA AANGAN"), credit=MET, trans="whip")),
        (at("अर्जुन के"), kdv2.BG_para(f"{A}/37939.jpg", (0.66, 0.62, 0.36), (0.66, 0.58, 0.28), "push"), dict(caps=cap(at("अर्जुन के"), "ARJUN KE DO PED"), credit=MET)),
        (at("फिर एक दिन,"), P(39258, 0.70, "fall"), dict(caps=cap(at("फिर एक दिन,"), "MAA YASHODA"), credit=MET, trans="whip")),
        (at("नटखट"), kdv2.BG_para(f"{A}/849507.jpg", (0.36, 0.48, 0.44), (0.34, 0.50, 0.34), "push"), dict(caps=cap(at("नटखट"), "NATKHAT KANHA"), credit=MET)),
        (at("ओखली से"), kdv2.BG_para(f"{A}/37939.jpg", (0.38, 0.80, 0.30), (0.40, 0.80, 0.22), "push"), dict(caps=cap(at("ओखली से"), "OKHLI SE BAANDH DIYA"), credit=MET, trans="zoom")),
        (at("कान्हा ओखली"), kdv2.BG_para(f"{A}/37939.jpg", (0.55, 0.78, 0.40), (0.60, 0.78, 0.32), "left"), dict(caps=cap(at("कान्हा ओखली"), "DONO PEDON KE BEECH SE"), credit=MET)),
        
        (at("ओखली फँसी"), kdv2.BG_para(f"{A}/37939.jpg", (0.68, 0.55, 0.30), (0.68, 0.60, 0.48), "pull"), dict(caps=cap(at("ओखली फँसी"), "OKHLI PHANSI...", "PED JAD SE UKHAD GAYE", RED, at("जड़ से")), credit=MET, shake=(at("जड़ से"), 0.9), flash=(at("जड़ से"), 0.25, (255, 240, 210)), trans="zoom")),
        (at("पेड़ों से"), kdv2.BG_para(f"{A}/37939.jpg", (0.62, 0.84, 0.26), (0.62, 0.84, 0.19), "push"), dict(caps=cap(at("पेड़ों से"), "PRAKAT HUE: NALAKUBAR + MANIGRIV"), fx=[kd.light_glow(0.5, 0.55, 380, (255, 230, 170), 0.35, 0.2)], credit=MET, trans="flash")),
        (at("हाथ जोड़कर"), P(37926, 0.55, "rise"), dict(caps=cap(at("हाथ जोड़कर"), "HAATH JODKAR STUTI"), credit=MET)),
        (at("इसीलिए"), P(39331, 0.70, "push"), dict(caps=cap(at("इसीलिए"), "ISILIYE KRISHNA: DAMODAR"), credit=MET, trans="whip")),
        (at("जिनके उदर"), kd.BG_plate("gold"), dict(over=[kd.deva_card(at("जिनके उदर"), "दाम (रस्सी) + उदर (पेट)", None, "BHAGAVATA PURANA 10.9", y=820, size=92, color=(255, 226, 160))], grade=None)),
        (at("आज लक्ष्मी"), P(78264, 0.62, "push"), dict(caps=cap(at("आज लक्ष्मी"), "AAJ LAKSHMI-KUBER PUJA"), credit=MET, trans="zoom")),
        (at("कुबेर का वरदान"), P(39006, 0.80, "orbit"), dict(caps=cap(at("कुबेर का वरदान"), "KUBER KA VARDAAN"), credit=MET)),
        (at("है धन"), P(39406, 0.80, "push"), dict(caps=cap(at("है धन"), "DHAN"), credit=MET, trans="zoom")),
        (at("और उनके बेटों"), P(39360, 0.75, "rise"), dict(caps=cap(at("और उनके बेटों"), "BETON KI SEEKH:", "DHAN + VINAMRATA", GOLD, at("विनम्रता")), credit=MET)),
        (at("कुबेर की कहानी"), BG_sky(), dict(over=[kd.chips_at([(at("कुबेर की कहानी") + 0.2, "PART 1 · LANKA   PART 2 · SHRAAP   PART 3 · MUKTI", "c", 820, {"size": 36})])],
                                         caps=cap(at("कुबेर की कहानी"), "KUBER KI KAHANI: POORI"), grade=None, trans="whip")),
        (at("अगली"), kd.BG_plate("red"), dict(fx=[kd.embers(50, 43, (255, 190, 110), 70, 0.7)],
                                            over=[kd.chips_at([(at("अगली"), "COMMENT KARO: AGLI KAHANI?", "c", 900, {"size": 50}), (at("कमेंट"), "FOLLOW · KATHA DEEP", "c", 1060, {"size": 44})])], grade=None)),
    ]
    return kdv2.keyword_shots(S, END)


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
