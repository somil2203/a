"""Nachiketa aur Yamraj · PART 2 (continues Dhanteras Special 3, which ended:
'Par Yamraj ne Nachiketa ko jawab kya diya — maut ke baad kya hota hai? Part 2 kal.')
Source: Kathopanishad 1.2.1-2, 1.2.18, 1.2.20, 1.3.3-4, 1.3.6/9, 1.3.14, 2.3.18.
usage: python3 edit.py [picture|still T|audio|all]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
from kd import CREAM, GOLD, RED, Scene  # noqa: E402

A = f"{KD}/art/full"
R3 = f"{KD}/renders3d"
T = kd.Timing(HERE)
at = T.at
END = T.end + 1.8
TAG = "KATHOPANISHAD · PART 2"
MET = "ART: THE MET · OPEN ACCESS (CC0)"


def scenes():
    s = []
    # 1 HOOK — the question, Yamraj (a different Calcutta Art Studio Yama print from Part 1)
    s.append(Scene(0, at("कठोपनिषद"), kd.BG_kb(f"{A}/838323.jpg", (0.40, 0.42, 0.62), (0.40, 0.33, 0.44)),
                   caps=[(0.0, "MAUT KE BAAD", "KYA HOTA HAI?", RED, 1.0),
                         (at("आज —"), "AAJ:", "YAMRAJ KA JAWAB", GOLD, at("यमराज का जवाब"))],
                   fx=[kd.embers(30, 2, (255, 120, 60), 70, 0.6)], credit=MET, grade_kind="warm",
                   flash=(0.0, 0.5, (0, 0, 0))))
    # 2 Kathopanishad title + 'do raaste'
    s.append(Scene(at("कठोपनिषद"), at("प्रेय —"), kd.BG_plate("night"),
                   over=[kd.deva_card(at("कठोपनिषद"), "कठोपनिषद्", None, "ADHYAY 1 · VALLI 2", y=860, size=120)],
                   caps=[(at("कठोपनिषद"), "YAMRAJ BOLE:", "DO RAASTE", GOLD, at("दो रास्ते"))],
                   fx=[kd.embers(40, 3, (255, 200, 140), 50, 0.5, (1, 3))], grade_kind=None))
    # 3 Preya / Shreya fork
    s.append(Scene(at("प्रेय —"), at("मूर्ख"), kd.BG_fork("night"),
                   over=[kd.chips_at([(at("प्रेय —"), "PREYA · JO ACHHA LAGE", 60, 560, {"size": 44, "fg": (200, 190, 215), "border": (150, 140, 170)}),
                                      (at("श्रेय —"), "SHREYA · JO SAHI HO", 470, 720, {"size": 44})])],
                   caps=[(at("प्रेय —"), "DO RAASTE:", None, None)], grade_kind=None))
    # 4 Dheer chooses shreya — Yama, Regent of the South (with his buffalo)
    s.append(Scene(at("मूर्ख"), at("फिर यमराज ने"), kd.BG_kb(f"{A}/72302.jpg", (0.50, 0.42, 0.95), (0.48, 0.30, 0.62)),
                   caps=[(at("मूर्ख"), "MOORKH: PREYA", "DHEER: SHREYA", GOLD, at("धीर")),
                         (at("और नचिकेता..."), "NACHIKETA NE", "SONA THUKRAYA", GOLD, at("तुमने सोना"))],
                   over=[kd.chips_at([(at("मूर्ख") + 0.4, "KATHOPANISHAD 1.2.2", "c", 1690, {"size": 30, "fg": CREAM, "border": (200, 160, 100)})])],
                   credit=MET, grade_kind="night"))
    # 5-7 The secret: heart-lotus + light of the atma; the shloka
    s.append(Scene(at("फिर यमराज ने"), at("वो अणु"), kd.BG_kb(f"{R3}/lotus.png", (0.5, 0.52, 1.0), (0.5, 0.56, 0.7)),
                   caps=[(at("फिर यमराज ने"), "SABSE BADA", "RAHASYA", GOLD, at("रहस्य")),
                         (at("आत्मा न"), "ATMA: NA JANM,", "NA MRITYU", GOLD, at("न मरती")),
                         (at("शरीर मरता"), "SHARIR MARTA HAI.", "ATMA NAHI.", GOLD, at("आत्मा नहीं"))],
                   over=[kd.deva_card(at("न जायते"), "न जायते म्रियते वा", "विपश्चित्", "KATHOPANISHAD 1.2.18", y=1180, size=96)],
                   fx=[kd.embers(36, 4, (255, 210, 150), 40, 0.6, (1, 4))], grade_kind=None))
    # 8 Smaller than the atom, greater than the great
    s.append(Scene(at("वो अणु"), at("फिर यमराज ने समझाया"), kd.BG_stars(),
                   caps=[(at("वो अणु"), "ANU SE CHHOTI,", "MAHAN SE MAHAN", GOLD, at("और महान")),
                         (at("हर जीव"), "HAR JEEV KE", "HRIDAY MEIN", GOLD, at("हृदय"))],
                   fx=[kd.light_glow(0.5, 0.55, 160, (255, 220, 170), 0.8, 0.2)],
                   over=[kd.chips_at([(at("वो अणु") + 0.5, "KATHOPANISHAD 1.2.20", "c", 1690, {"size": 30, "fg": CREAM, "border": (200, 160, 100)})])],
                   grade_kind=None))
    # 9-11 The chariot (Met 74726, War Chariot drawing) with labels
    lab = {"size": 40}
    s.append(Scene(at("फिर यमराज ने समझाया"), at("और फिर यमराज"), kd.BG_contain(f"{A}/74726.jpg", "red", 0.50, 1.0, (1.18, 1.25)),
                   caps=[(at("फिर यमराज ने समझाया"), "YAMRAJ KA", "RATH", GOLD, at("एक रथ")),
                         (at("जिसकी"), "LAGAAM DHEELI =", "GHODE BEKAABU", RED, at("उसके घोड़े")),
                         (at("जिसका"), "SAARTHI SAMAJHDAAR =", "MANZIL", GOLD, at("मंज़िल"))],
                   over=[kd.chips_at([(at("शरीर, रथ"), "SHARIR = RATH", 560, 1140, lab),
                                      (at("बुद्धि"), "BUDDHI = SAARTHI", 520, 690, lab),
                                      (at("मन, लगाम"), "MAN = LAGAAM", 330, 1260, lab),
                                      (at("इंद्रियाँ"), "INDRIYAN = GHODE", 40, 690, lab),
                                      (at("स्वामी —"), "ATMA = SWAMI", 600, 1380, {"size": 46, "fg": (30, 10, 4), "bg": (245, 193, 72, 245)}),
                                      (at("शरीर, रथ"), "KATHOPANISHAD 1.3.3–4", "c", 1690, {"size": 30, "fg": CREAM, "border": (200, 160, 100)})])],
                   credit=MET, grade_kind=None, shake=(at("उसके घोड़े"), 0.6)))
    # 12 Uttishthata jagrata
    s.append(Scene(at("और फिर यमराज"), at("उठो"), kd.BG_plate("gold"),
                   over=[kd.deva_card(at("उत्तिष्ठत"), "उत्तिष्ठत जाग्रत", "प्राप्य वरान्निबोधत", "KATHOPANISHAD 1.3.14", y=820, size=104, color=(255, 226, 160))],
                   caps=[(at("और फिर यमराज"), "AUR PHIR", "YAMRAJ BOLE:", GOLD, at("बोले"))],
                   fx=[kd.embers(50, 6, (255, 200, 120), 80, 0.7)], grade_kind=None))
    # 13a Go to the wise — sage teaching (Pahari, Met 37951)
    s.append(Scene(at("उठो"), at("ये रास्ता"), kd.BG_kb(f"{A}/37951.jpg", (0.66, 0.55, 0.36), (0.72, 0.60, 0.25)),
                   caps=[(at("उठो"), "UTHO. JAAGO.", "GURU SE GYAAN PAO", GOLD, at("श्रेष्ठ"))],
                   credit=MET, grade_kind="warm"))
    # 13b Razor's edge
    s.append(Scene(at("ये रास्ता"), at("सदियों"), kd.BG_kb(f"{R3}/razor.png", (0.5, 0.5, 1.0), (0.5, 0.45, 0.78)),
                   caps=[(at("ये रास्ता"), "YE RAASTA:", "CHHURE KI DHAAR", RED, at("छुरे"))],
                   fx=[kd.embers(20, 7, (255, 220, 180), 30, 0.4, (1, 3))], grade_kind=None))
    # 14 Vivekananda (typographic card; no photo)
    s.append(Scene(at("सदियों"), at("और नचिकेता?"), kd.BG_plate("teal"),
                   over=[kd.big_text(at("स्वामी विवेकानंद"), "SWAMI", 760, 170, CREAM), kd.big_text(at("विवेकानंद"), "VIVEKANANDA", 940, 170, GOLD),
                         kd.chips_at([(at("इसी मंत्र"), "“UTHO, JAAGO, AUR TAB TAK MAT RUKO…”", "c", 1200, {"size": 40})])],
                   caps=[(at("सदियों"), "SADIYON BAAD:", None, None)], grade_kind=None))
    # 15 Beyond death (Calcutta Art Studio, Sheshanarayana — Brahma on the lotus of light)
    s.append(Scene(at("और नचिकेता?"), at("तो मौत"), kd.BG_kb(f"{A}/849519.jpg", (0.52, 0.30, 0.80), (0.50, 0.22, 0.50)),
                   caps=[(at("और नचिकेता?"), "AUR NACHIKETA?", None, None),
                         (at("मृत्यु से ये"), "MRITYU SE VIDYA PAAKAR,", "MRITYU KE PAAR", GOLD, at("मृत्यु के पार"))],
                   over=[kd.chips_at([(at("मृत्यु से ये"), "KATHOPANISHAD 2.3.18", "c", 1690, {"size": 30, "fg": CREAM, "border": (200, 160, 100)})])],
                   credit=MET, grade_kind="warm"))
    # 16 Answer + CTA — Nachiketa (same silhouette design as Part 1) before the light
    s.append(Scene(at("तो मौत"), END, kd.BG_plate("night", drift=True),
                   fx=[kd.light_glow(0.5, 0.62, 420, (255, 200, 130), 0.95, 0.06), kd.embers(60, 8, (255, 190, 110), 70, 0.8),
                       kd.silhouette_boy(540, 1250, 360)],
                   caps=[(at("तो मौत"), "MAUT KE BAAD?", None, None),
                         (at("जो सच"), "JO SACH MEIN TUM HO...", "WO KABHI MARTA NAHI.", GOLD, at("वो कभी"))],
                   over=[kd.chips_at([(T.end + 0.2, "FOLLOW · KATHA DEEP", "c", 1660, {"size": 48})])], grade_kind=None))
    return s


def audio():
    sys.path.insert(0, f"{KD}/tools")
    import music
    import mixlib
    sa = 130.81  # C — Yaman colour (Sa Re Ga Ma# Pa Dha Ni): serene
    sec = [(0, at("कठोपनिषद"), {"pad": 0.8, "sub": 0.6, "pad_bright": 600}),
           (at("कठोपनिषद") - 0.5, at("फिर यमराज ने"), {"tanpura": 0.8, "pad": 0.5}),
           (at("फिर यमराज ने") - 0.4, at("फिर यमराज ने समझाया"), {"tanpura": 1.0, "pad": 0.7, "pad_bright": 1400}),
           (at("फिर यमराज ने समझाया"), at("और फिर यमराज"), {"tanpura": 0.7, "drums": 0.55}),
           (at("और फिर यमराज") - 0.3, at("और नचिकेता?"), {"tanpura": 1.0, "pad": 0.8, "drums": 0.35, "pad_bright": 1600}),
           (at("और नचिकेता?") - 0.5, END, {"tanpura": 0.9, "pad": 0.9, "pad_bright": 1800})]
    hits = [(0.05, "boom", 0.9), (at("कठोपनिषद"), "bell", 0.5), (at("न जायते") - 0.1, "bellhi", 0.6),
            (at("स्वामी —"), "bayan", 0.6), (at("उत्तिष्ठत"), "boom", 0.7), (at("उत्तिष्ठत"), "bell", 0.6),
            (at("जो सच") - 0.1, "bellhi", 0.55), (T.end, "bell", 0.6)]
    # bansuri phrase in Yaman under the final answer
    mel = (at("और नचिकेता?") + 0.5, [(0, 1.2, 7), (1.2, 0.6, 9), (1.8, 0.6, 11), (2.4, 2.0, 12), (4.6, 0.8, 11), (5.4, 0.8, 9),
                                      (6.2, 2.4, 7), (8.8, 0.8, 6), (9.6, 0.8, 4), (10.4, 3.0, 2), (13.6, 3.6, 0)])
    st = music.score(END, sa, sec, hits, mel, bpm=76, seed=3)
    cues = [(0.0, "deep-wind-hum", -14, {"fade_out": 3, "max_len": 7}),
            (at("कठोपनिषद") - 0.25, "whoosh-transition", -16),
            (at("प्रेय —") - 0.2, "wind-swoosh", -16),
            (at("फिर यमराज ने") - 0.3, "harp-sweep", -14),
            (at("न जायते") - 0.3, "light-energy", -18),
            (at("वो अणु") - 0.2, "magic-sparkle", -16),
            (at("फिर यमराज ने समझाया") - 0.2, "whoosh-fast", -15),
            (at("उसके घोड़े"), "fast-sword-whoosh", -18),
            (at("और फिर यमराज") - 0.4, "cinematic-trailer-riser", -16, {"max_len": 3.0, "fade_out": 0.6}),
            (at("उत्तिष्ठत"), "trailer-impact", -13),
            (at("ये रास्ता"), "sword-slash", -16),
            (at("सदियों") - 0.2, "whoosh-deep-impact", -15),
            (at("और नचिकेता?") - 0.2, "harp-sweep", -15),
            (at("तो मौत") - 0.3, "reverse-impact", -15),
            (at("जो सच"), "bell-chime", -14)]
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
