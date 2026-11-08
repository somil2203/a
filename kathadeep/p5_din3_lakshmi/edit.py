"""Deepotsav · Din 3/5 — Lakshmi Puja: 'Lakshmi kise chunti hain?'
Continues Din 2 ('Kal teesra diya — badi Diwali, Lakshmi puja').
Sources: Vishnu Purana 1.9 (Durvasa's garland, Indra, Airavata, Shri leaves the three worlds -> churning);
Bhagavata Purana 8.8.19-24 (Lakshmi surveys gods and sages: austerity without conquest of anger, knowledge
without freedom from attachment; chooses Mukunda, who wants nothing from her).
Rule: what the narration names is what the frame shows (Indra -> Indra; garland -> the garland; Vishnu -> Vishnu).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd, kdextra, kdv2  # noqa: E401,E402
from kd import CREAM, GOLD, RED, Scene  # noqa: E402

A, R3 = f"{KD}/art/full", f"{KD}/renders3d"
T = kd.Timing(HERE); at = T.at; END = T.end + 1.8
TAG = "DEEPOTSAV · DIN 3/5"
kd.CAP_MODE = "lower"
kd.TRANS = "cut"; MET = "ART: THE MET · OPEN ACCESS (CC0)"
REF = {"size": 30, "fg": CREAM, "border": (200, 160, 100)}


def window_tint(alpha=150):
    from PIL import Image, ImageDraw
    def f(base, t, sc):
        ov = Image.new("RGBA", base.size)
        x0, y0, x1, y1 = kd.FRAME
        ImageDraw.Draw(ov).rectangle((x0, y0, x1, y1), fill=(60, 12, 10, alpha))
        base.alpha_composite(ov)
    return f


def credit_footer(base, t, sc):
    c = kd.text_img("ART: THE MET OPEN ACCESS (CC0) · 3D: KATHA DEEP", "monor", 20, (120, 80, 50), shadow=False)
    kd.paste_fade(base, c, (kd.W / 2 - c.width / 2, 1840), 0.9)


def scenes():
    s = []
    s.append(Scene(0, at("आज बड़ी"), kd.BG_framed(f"{A}/78259.jpg", (0.50, 0.40, 0.62), (0.50, 0.34, 0.44)),
                   caps=[(0.0, "LAKSHMI JI NE", "SWARG CHHOD DIYA THA", RED, 1.3), (at("जानते हैं"), "JAANTE HAIN", "KYUN?", GOLD, at("क्यों"))],
                   grade_kind=None, vig=False, flash=(0, 0.4, (0, 0, 0))))
    s.append(Scene(at("आज बड़ी"), at("विष्णु पुराण"), kd.BG_framed(f"{A}/849494.jpg", (0.5, 0.45, 0.8), (0.5, 0.40, 0.6)), fx=[window_tint(120), kdextra.five_diyas(at("आज बड़ी") + 0.3, 3, y=820, x0=92, step=172, size=118)],
                   caps=[(at("आज बड़ी"), "AAJ BADI DIWALI", None, None), (at("आज तीसरा"), "TEESRA DIYA:", "LAKSHMI PUJA", GOLD, at("लक्ष्मी पूजा"))], grade_kind=None, vig=False))
    s.append(Scene(at("विष्णु पुराण"), at("देवराज इंद्र"), kd.BG_framed(f"{R3}/mala.png", (0.5, 0.48, 1.0), (0.5, 0.50, 0.80)),
                   caps=[(at("विष्णु पुराण"), "VISHNU PURAN:", "RISHI DURVASA KI MAALA", GOLD, at("ऋषि दुर्वासा"))],
                   over=[kd.chips_at([(at("विष्णु पुराण") + 0.3, "VISHNU PURANA 1.9", "c", 1400, REF)])],
                   fx=[kd.embers(30, 31, (255, 210, 140), 40, 0.6, (1, 3))], grade_kind=None, vig=False))
    s.append(Scene(at("देवराज इंद्र"), at("उन्होंने वो"), kd.BG_framed(f"{A}/38509.jpg", (0.5, 0.48, 0.80), (0.5, 0.42, 0.58)),
                   caps=[(at("देवराज इंद्र"), "DEVRAJ INDRA", "KO DI DIVYA MAALA", GOLD, at("फूलों की")),
                         (at("इंद्र ऐरावत"), "INDRA,", "AIRAVAT PAR", GOLD, at("ऐरावत"))], grade_kind=None, vig=False))
    s.append(Scene(at("उन्होंने वो"), at("दुर्वासा क्रोधित"), kd.BG_framed(f"{R3}/mala.png", (0.5, 0.40, 0.55), (0.5, 0.75, 0.75)),
                   caps=[(at("उन्होंने वो"), "MAALA HAATHI KE", "SIR PAR RAKH DI", GOLD, at("सिर पर")),
                         (at("और हाथी"), "HAATHI NE", "ZAMEEN PAR PHENK DI", RED, at("ज़मीन"))],
                   shake=(at("ज़मीन"), 0.5), grade_kind=None, vig=False))
    s.append(Scene(at("दुर्वासा क्रोधित"), at("और स्वर्ग"), kd.BG_framed(f"{R3}/mala_fallen.png", (0.5, 0.52, 1.0), (0.5, 0.56, 0.78)),
                   caps=[(at("दुर्वासा क्रोधित"), "DURVASA KA", "SHRAAP", RED, at("बोले")),
                         (at("जैसे ये"), "JAISE MAALA GIRI,", "VAISE VAIBHAV GIREGA", RED, at("वैभव"))],
                   flash=(at("दुर्वासा क्रोधित"), 0.3, (200, 30, 20)), grade_kind=None, vig=False))
    s.append(Scene(at("और स्वर्ग"), at("इसी के बाद"), kd.BG_framed(f"{A}/849502.jpg", (0.48, 0.45, 0.62), (0.48, 0.38, 0.42)),
                   caps=[(at("और स्वर्ग"), "SWARG SE", "SHRI CHALI GAYIN", GOLD, at("श्री चली")),
                         (at("तीनों लोक"), "TEENON LOK", "PHEEKE PAD GAYE", CREAM, at("फीके"))],
                   grade_kind=None, vig=False))
    s.append(Scene(at("इसी के बाद"), at("पर अब"), kd.BG_framed(f"{A}/38601.jpg", (0.5, 0.48, 0.85), (0.5, 0.35, 0.55)),
                   caps=[(at("इसी के बाद"), "PHIR SAMUDRA MANTHAN,", "LAKSHMI PRAKAT HUIN", GOLD, at("लक्ष्मी जी फिर"))], grade_kind=None, vig=False))
    s.append(Scene(at("पर अब"), at("भागवत"), kd.BG_framed(f"{A}/38542.jpg", (0.5, 0.45, 0.85), (0.5, 0.38, 0.6)), fx=[window_tint(90)], over=[kd.big_text(at("किसे चुनेंगी"), "?", 620, 520, GOLD)],
                   caps=[(at("पर अब"), "AB SAWAAL:", "LAKSHMI KISE CHUNENGI?", GOLD, at("किसे चुनेंगी"))], grade_kind=None, vig=False))
    s.append(Scene(at("भागवत"), at("और फिर उन्होंने"), kd.BG_framed(f"{A}/659913.jpg", (0.55, 0.5, 0.40), (0.6, 0.5, 0.30)), fx=[window_tint(110)],
                   over=[kd.chips_at([(at("भागवत") + 0.3, "BHAGAVATA PURANA 8.8", "c", 1400, REF),
                                      (at("किसी में तप"), "TAP THA", 120, 820, {"size": 56}),
                                      (at("पर क्रोध"), "PAR KRODH NAHI JEETA", 300, 950, {"size": 56, "fg": RED, "border": RED}),
                                      (at("किसी में ज्ञान"), "GYAAN THA", 120, 1150, {"size": 56}),
                                      (at("पर मोह"), "PAR MOH NAHI CHHOOTA", 300, 1280, {"size": 56, "fg": RED, "border": RED})])],
                   caps=[(at("भागवत"), "BHAGAVAT PURAN:", "HAR DEV, HAR RISHI KO DEKHA", GOLD, at("हर देव"))], grade_kind=None, vig=False))
    s.append(Scene(at("और फिर उन्होंने"), at("ये कहानी"), kd.BG_framed(f"{A}/38571.jpg", (0.5, 0.48, 0.80), (0.55, 0.40, 0.55)),
                   caps=[(at("और फिर उन्होंने"), "LAKSHMI NE CHUNA:", "VISHNU", GOLD, at("विष्णु को")),
                         (at("जिन्हें"), "JINHE LAKSHMI SE", "KUCH NAHI CHAHIYE THA", GOLD, at("कुछ भी"))],
                   fx=[kd.light_glow(0.55, 0.42, 380, (255, 210, 140), 0.35, 0.1)], grade_kind=None, vig=False))
    s.append(Scene(at("ये कहानी"), at("कल चौथा"), kd.BG_framed(f"{A}/849502.jpg", (0.50, 0.75, 0.50), (0.50, 0.70, 0.40)),
                   caps=[(at("ये कहानी"), "LAKSHMI AHANKAAR", "KE GHAR MEIN NAHI TIKTIN", RED, at("अहंकार")),
                         (at("वो वहाँ"), "WAHAN RAHTI HAIN,", "JAHAN SAMMAAN HAI", GOLD, at("जहाँ सम्मान"))],
                   fx=[kd.flicker(0.05)], grade_kind=None, vig=False))
    s.append(Scene(at("कल चौथा"), END, kd.BG_paper_plate(), fx=[kdextra.five_diyas(at("कल चौथा"), 3, y=820, x0=92, step=172, size=118), kd.embers(40, 33, (255, 180, 90), 60, 0.6)],
                   over=[kd.chips_at([(at("फ़ॉलो"), "FOLLOW · 5 DIN · 5 DIYE", "c", 1360, {"size": 50})])],
                   caps=[(at("कल चौथा"), "KAL: DIN 4", "GOVARDHAN", GOLD, at("गोवर्धन"))], grade_kind=None, vig=False))
    for sc in s:
        sc.over.append(credit_footer)
    TR = {at("विष्णु पुराण"): "push", at("उन्होंने वो"): "zoom", at("दुर्वासा क्रोधित"): "flash", at("इसी के बाद"): "push", at("पर अब"): "zoom", at("भागवत"): "push", at("और फिर उन्होंने"): "zoom", at("कल चौथा"): "push"}
    for sc in s:
        sc.trans = TR.get(sc.t0, "cut")
    return kdv2.expand(s)


def audio():
    import music, mixlib  # noqa: E401
    sa = 146.83
    sec = [(0, at("आज बड़ी"), {"pad": 0.8, "tanpura": 0.4, "pad_bright": 900}),
           (at("आज बड़ी") - 0.3, at("विष्णु पुराण"), {"tanpura": 0.9, "pad": 0.5}),
           (at("विष्णु पुराण") - 0.3, at("इसी के बाद"), {"tanpura": 0.7, "drums": 0.6, "sub": 0.5}),
           (at("इसी के बाद") - 0.3, at("ये कहानी"), {"tanpura": 1.0, "pad": 0.7, "pad_bright": 1400}),
           (at("ये कहानी") - 0.3, END, {"tanpura": 1.0, "pad": 0.9, "drums": 0.4, "pad_bright": 1700})]
    hits = [(0.05, "bell", 0.7), (at("आज तीसरा"), "bellhi", 0.5), (at("ज़मीन"), "boom", 0.8), (at("दुर्वासा क्रोधित"), "boom", 0.9),
            (at("लक्ष्मी जी फिर"), "bell", 0.6), (at("विष्णु को"), "bellhi", 0.6), (at("कल चौथा"), "bell", 0.6)]
    mel = (at("और फिर उन्होंने"), [(0, 0.8, 7), (0.8, 1.2, 9), (2.0, 0.8, 11), (2.8, 2.0, 12), (5.0, 0.8, 11), (5.8, 2.2, 7)])
    st = music.score(END, sa, sec, hits, mel, bpm=88, seed=5)
    cues = [(0.0, "magic-sparkle", -16), (at("आज बड़ी") - 0.2, "soft-fire-woosh", -15), (at("विष्णु पुराण") - 0.2, "harp-sweep", -15),
            (at("और हाथी"), "whoosh-fast", -14), (at("ज़मीन"), "big-impact", -15), (at("दुर्वासा क्रोधित"), "trailer-impact", -13),
            (at("और स्वर्ग") - 0.2, "deep-wind-hum", -16, {"max_len": 4, "fade_out": 1.5}), (at("इसी के बाद") - 0.2, "water-splash", -17),
            (at("पर अब") - 0.2, "reverse-impact", -16), (at("पर क्रोध"), "heartbeat-impact", -16), (at("और फिर उन्होंने") - 0.2, "harp-sweep", -14),
            (at("कल चौथा"), "bell-chime", -14)]
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
