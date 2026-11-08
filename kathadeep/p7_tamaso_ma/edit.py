"""Diwali standalone — 'Tamaso ma jyotirgamaya' (Brihadaranyaka Upanishad 1.3.28) on Amavasya night.
Visuals: moonless sky; a 1st–3rd century CE stone lamp (The Met 38758) for 'hazaron saal purana';
three diyas on three steps lighting one per line of the mantra (new 3D)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd, kdextra, kdv2  # noqa: E401,E402
from kd import CREAM, GOLD, Scene  # noqa: E402

A, R3 = f"{KD}/art/full", f"{KD}/renders3d"
T = kd.Timing(HERE); at = T.at; END = T.end + 1.8
TAG = "KATHA DEEP · DEEPAVALI"
kd.CAP_MODE = "mono"
kd.TRANS = "cut"; MET = "ART: THE MET · OPEN ACCESS (CC0)"


def BG_black():
    from PIL import Image
    blk = Image.new("RGB", (kd.W, kd.H), (4, 3, 3))
    return lambda lt, fr, fi: blk


def scenes():
    s = []
    G = lambda n: f"{R3}/ghat{n}.png"
    def add(sc, tr=None):
        sc.trans = tr
        s.append(sc)
    _open = kd.BG_kb(G(0), (0.5, 0.40, 1.0), (0.5, 0.42, 0.84))
    add(Scene(0, at("और फिर भी"), (lambda lt, fr, fi: _open(lt, fr, fi)),
              caps=[(0.0, "AAJ AMAVASYA HAI", None, None), (at("आसमान"), "AASMAAN MEIN", "CHAAND NAHI", CREAM, at("चाँद"))], grade_kind="moonless"))
    add(Scene(at("और फिर भी"), at("हज़ारों"), kd.BG_kb(G(6), (0.5, 0.55, 1.0), (0.5, 0.55, 0.85)),
              caps=[(at("और फिर भी"), "PHIR BHI AAJ:", "SAAL KI SABSE ROSHAN RAAT", GOLD, at("सबसे रोशन"))],
              fx=[kd.embers(70, 51, (255, 190, 100), 90, 0.8, (1, 4))], grade_kind="flame"), "flash")
    add(Scene(at("हज़ारों"), at("असतो मा"), kd.BG_kb(f"{A}/38758.jpg", (0.5, 0.55, 0.45), (0.5, 0.55, 0.36)),
              caps=[(at("हज़ारों"), "HAZAARON SAAL PURANA", "EK MANTRA", GOLD, at("एक मंत्र")),
                    (at("बृहदारण्यक"), "BRIHADARANYAKA", "UPANISHAD", GOLD, at("उपनिषद"))],
              over=[kd.chips_at([(at("हज़ारों") + 0.3, "STONE LAMP · INDIA · 1ST–3RD CENTURY CE", "c", 330, {"size": 32}),
                                 (at("बृहदारण्यक"), "BRIHADARANYAKA UPANISHAD 1.3.28", "c", 430, {"size": 30, "fg": CREAM, "border": (200, 160, 100)})])],
              credit=MET, grade_kind="warm"), "zoom")
    for ph, nxt, g, l1, tr in [("असतो मा", "तमसो मा", 2, "असतो मा सद्गमय", "cut"), ("तमसो मा", "मृत्योर्मा", 4, "तमसो मा ज्योतिर्गमय", "zoom"),
                               ("मृत्योर्मा", "असत्य से", 6, "मृत्योर्मा अमृतं गमय", "iris")]:
        add(Scene(at(ph), at(nxt), kd.BG_kb(G(g), (0.5, 0.60, 0.85), (0.5, 0.58, 0.70)),
                  over=[kd.deva_card(at(ph), l1, None, None, y=300, size=104, color=(255, 226, 160))], fx=[kd.flicker(0.05)], grade_kind="flame"), tr)
    for ph, nxt, txt in [("असत्य से", "अँधेरे से", "ASATYA → SATYA"), ("अँधेरे से", "मृत्यु से", "ANDHERA → ROSHNI"), ("मृत्यु से", "दिवाली का", "MRITYU → AMRIT")]:
        add(Scene(at(ph), at(nxt), BG_black(), fx=[kd.light_glow(0.5, 0.5, 380, (255, 190, 110), 0.55, 0.15)],
                  over=[kd.big_text(at(ph), txt, 820, 150 if len(txt) < 15 else 128, GOLD)], grade_kind=None), "zoom")
    add(Scene(at("दिवाली का"), at("आज जब"), kd.BG_kb(G(6), (0.5, 0.62, 0.55), (0.5, 0.52, 1.0)),
              caps=[(at("दिवाली का"), "DIWALI KA POORA ARTH", "IN 3 PANKTIYON MEIN", GOLD, at("तीन पंक्तियों"))],
              fx=[kd.embers(60, 52, (255, 190, 110), 70, 0.8)], grade_kind="flame"), "cut")
    add(Scene(at("आज जब"), END, BG_black(),
              caps=[(at("आज जब"), "AAJ DIYA JALAYEN,", "TO YE MANTRA BOLIYE", GOLD, at("ये मंत्र")),
                    (at("शुभ दीपावली"), "SHUBH", "DEEPAVALI", GOLD, at("शुभ दीपावली") + 0.4)],
              fx=[kd.light_glow(0.5, 0.5, 340, (255, 190, 100), 0.9, 0.12), kd.embers(60, 53, (255, 190, 110), 70, 0.8)],
              over=[kd.deva_card(at("शुभ दीपावली"), "शुभ दीपावली", None, None, y=760, size=150, color=(255, 214, 140)),
                    kd.chips_at([(at("शुभ दीपावली") + 0.5, "FOLLOW · KATHA DEEP", "c", 1560, {"size": 46})])], grade_kind=None), "iris")
    return kdv2.expand(s)


def audio():
    import music, mixlib  # noqa: E401
    sa = 130.81
    sec = [(0, at("और फिर भी"), {"pad": 0.8, "pad_bright": 500, "sub": 0.5}),
           (at("और फिर भी") - 0.3, at("असतो मा"), {"tanpura": 0.9, "pad": 0.5}),
           (at("असतो मा") - 0.3, END, {"tanpura": 1.0, "pad": 0.9, "pad_bright": 1600})]
    hits = [(0.05, "boom", 0.6), (at("और फिर भी"), "bell", 0.6), (at("असतो मा"), "bellhi", 0.5), (at("तमसो मा"), "bellhi", 0.55),
            (at("मृत्योर्मा"), "bellhi", 0.6), (at("शुभ दीपावली"), "bell", 0.8)]
    mel = (at("दिवाली का"), [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 12), (4.2, 1.0, 11), (5.2, 3.0, 7)])
    st = music.score(END, sa, sec, hits, mel, bpm=72, seed=7)
    cues = [(0.0, "deep-wind-hum", -17, {"max_len": 5, "fade_out": 2}), (at("और फिर भी") - 0.2, "soft-fire-woosh", -14),
            (at("हज़ारों") - 0.2, "harp-sweep", -16), (at("असतो मा") - 0.1, "soft-fire-woosh", -18), (at("तमसो मा") - 0.1, "soft-fire-woosh", -18),
            (at("मृत्योर्मा") - 0.1, "soft-fire-woosh", -18), (at("शुभ दीपावली"), "bell-chime", -13)]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-6.5)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "still":
        for t in sys.argv[2:]:
            kd.still(scenes(), float(t), f"{HERE}/qc_{t}.png", TAG)
    if mode in ("picture", "all"):
        kd.render(scenes(), f"{HERE}/picture.mp4", TAG, t_end=END)
    if mode in ("audio", "all"):
        audio()
