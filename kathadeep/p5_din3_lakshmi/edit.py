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
    """Keyword shot list in the manuscript-frame look: each spoken name/thing gets its own picture."""
    F = kd.FRAME
    P = lambda i, wf=0.7, mv="push", focus=None: kdv2.BG_auto(f"{A}/{i}.jpg", wf, mv, focus, window=F)
    G = lambda wf, mv, focus: kdv2.BG_auto(f"{KD}/art/other/garlands_flickr.jpg", wf, mv, focus, window=F)
    def cap(t, l1, l2=None, t2=None):
        return [(t, l1, l2, GOLD, t2)]
    S = [
        (0.0, P(78259, 0.62, "push", (0.5, 0.40)), dict(caps=cap(0.0, "LAKSHMI JI NE", "SWARG CHHOD DIYA THA", 1.3))),
        (at("जानते हैं"), P(74979, 0.42, "left", (0.75, 0.38)), dict(caps=cap(at("जानते हैं"), "JAANTE HAIN", "KYUN?", at("क्यों")))),
        (at("आज बड़ी"), P(849494, 0.70, "rise", (0.5, 0.42)), dict(caps=cap(at("आज बड़ी"), "AAJ BADI DIWALI"), trans="push")),
        (at("पाँच दिये"), kd.BG_paper_plate(), dict(fx=[kdextra.five_diyas(at("पाँच दिये"), 3, y=820, x0=92, step=172, size=118)],
                                                  caps=cap(at("पाँच दिये"), "5 DIN · 5 DIYE ·", "AAJ TEESRA", at("आज तीसरा")))),
        (at("लक्ष्मी पूजा"), P(38518, 0.62, "push", (0.45, 0.42)), dict(caps=cap(at("लक्ष्मी पूजा"), "TEESRA DIYA:", "LAKSHMI PUJA", at("लक्ष्मी पूजा")), trans="zoom")),
        (at("विष्णु पुराण"), P(38515, 0.70, "rise"), dict(caps=cap(at("विष्णु पुराण"), "VISHNU PURAN 1.9"), trans="push")),
        (at("ऋषि दुर्वासा"), G(0.60, "left", (0.30, 0.50)), dict(caps=cap(at("ऋषि दुर्वासा"), "RISHI DURVASA KI", "DIVYA MAALA", at("ऋषि दुर्वासा") + 0.6))),
        (at("देवराज इंद्र"), P(38509, 0.75, "push", (0.5, 0.45)), dict(caps=cap(at("देवराज इंद्र"), "DEVRAJ INDRA"), trans="zoom")),
        (at("फूलों की"), G(0.40, "orbit", (0.55, 0.45)), dict(caps=cap(at("फूलों की"), "PHOOLON KI DIVYA MAALA"))),
        (at("इंद्र ऐरावत"), P(453145, 0.62, "right", (0.45, 0.70)), dict(caps=cap(at("इंद्र ऐरावत"), "AIRAVAT HAATHI"), trans="zoom")),
        (at("उन्होंने वो"), P(453145, 0.36, "push", (0.40, 0.70)), dict(caps=cap(at("उन्होंने वो"), "MAALA HAATHI KE", "SIR PAR", at("सिर पर")))),
        (at("और हाथी"), G(0.75, "fall", (0.65, 0.55)), dict(caps=cap(at("और हाथी"), "HAATHI NE", "ZAMEEN PAR PHENK DI", at("ज़मीन")), shake=(at("ज़मीन"), 0.6), flash=(at("ज़मीन"), 0.2, (255, 240, 220)))),
        (at("दुर्वासा क्रोधित"), kd.BG_paper_plate(), dict(over=[kd.big_text(at("दुर्वासा क्रोधित"), "DURVASA", 700, 150, (255, 214, 140)),
                                                                kd.big_text(at("क्रोधित"), "KA KRODH", 880, 150, (255, 120, 90))],
                                                          flash=(at("दुर्वासा क्रोधित"), 0.3, (200, 30, 20)), trans="flash")),
        (at("जैसे ये"), P(446753, 0.62, "fall", (0.5, 0.68)), dict(caps=cap(at("जैसे ये"), "JAISE MAALA GIRI,", "VAISE VAIBHAV GIREGA", at("वैभव")))),
        (at("और स्वर्ग"), P(849502, 0.58, "left", (0.48, 0.40)), dict(caps=cap(at("और स्वर्ग"), "SWARG SE", "SHRI CHALI GAYIN", at("श्री चली")), trans="zoom")),
        (at("तीनों लोक"), P(38251, 0.62, "pull", (0.5, 0.45)), dict(caps=cap(at("तीनों लोक"), "TEENON LOK", "PHEEKE PAD GAYE", at("फीके")))),
        (at("इसी के बाद"), P(37989, 0.40, "rise", (0.40, 0.55)), dict(caps=cap(at("इसी के बाद"), "SAMUDRA MANTHAN"), trans="push")),
        (at("लक्ष्मी जी फिर"), P(38542, 0.70, "push", (0.5, 0.40)), dict(caps=cap(at("लक्ष्मी जी फिर"), "LAKSHMI PHIR", "PRAKAT HUIN", at("प्रकट")), trans="zoom")),
        (at("पर अब"), P(38601, 0.70, "pull", (0.5, 0.35)), dict(caps=cap(at("पर अब"), "LAKSHMI", "KISE CHUNENGI?", at("किसे चुनेंगी")))),
        (at("भागवत"), P(659913, 0.45, "left", (0.62, 0.50)), dict(caps=cap(at("भागवत"), "BHAGAVAT PURAN 8.8:", "HAR DEV...", at("हर देव")), trans="push")),
        (at("हर ऋषि"), P(37955, 0.32, "right", (0.62, 0.78)), dict(caps=cap(at("हर ऋषि"), "...HAR RISHI KO DEKHA"))),
        (at("किसी में तप"), P(37956, 0.30, "push", (0.62, 0.45)), dict(caps=cap(at("किसी में तप"), "TAP THA...", "PAR KRODH NAHI JEETA", at("पर क्रोध")), flash=(at("पर क्रोध"), 0.2, (200, 40, 30)))),
        (at("किसी में ज्ञान"), P(37955, 0.30, "left", (0.45, 0.72)), dict(caps=cap(at("किसी में ज्ञान"), "GYAAN THA...", "PAR MOH NAHI CHHOOTA", at("पर मोह")))),
        (at("और फिर उन्होंने"), P(38571, 0.70, "push", (0.55, 0.42)), dict(caps=cap(at("और फिर उन्होंने"), "LAKSHMI NE CHUNA:", "VISHNU", at("विष्णु को")), fx=[kd.light_glow(0.5, 0.4, 380, (255, 210, 140), 0.3, 0.1)], trans="zoom")),
        (at("जिन्हें"), P(38120, 0.62, "rise", (0.5, 0.42)), dict(caps=cap(at("जिन्हें"), "JINHE LAKSHMI SE", "KUCH NAHI CHAHIYE THA", at("कुछ भी")))),
        (at("ये कहानी"), P(453313, 0.70, "pull", (0.5, 0.55)), dict(caps=cap(at("ये कहानी"), "AHANKAAR KE GHAR MEIN", "LAKSHMI NAHI TIKTIN", at("अहंकार")), trans="push")),
        (at("वो वहाँ"), P(688470, 0.42, "push", (0.30, 0.55)), dict(caps=cap(at("वो वहाँ"), "WAHAN RAHTI HAIN,", "JAHAN SAMMAAN HAI", at("जहाँ सम्मान")), trans="zoom")),
        (at("कल चौथा"), P(37968, 0.62, "rise", (0.48, 0.45)), dict(caps=cap(at("कल चौथा"), "KAL: DIN 4", "GOVARDHAN", at("गोवर्धन")), trans="push")),
        (at("फ़ॉलो"), kd.BG_paper_plate(), dict(fx=[kdextra.five_diyas(at("फ़ॉलो"), 3, y=760, x0=92, step=172, size=118)],
                                              over=[kd.chips_at([(at("फ़ॉलो") + 0.2, "FOLLOW · 5 DIN · 5 DIYE", "c", 1200, {"size": 46})])],
                                              caps=cap(at("फ़ॉलो"), "PAANCHON DIYE", "SAATH JALAYENGE", at("साथ")))),
    ]
    out = kdv2.keyword_shots(S, END)
    for sc in out:
        sc.grade_kind, sc.vig = None, False
        sc.over = list(sc.over) + [credit_footer]
    return out


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
