"""Chitragupta — reference-grammar edit. Audio mix: soft bed, ticks under caption builds, paper pops, quill scratches."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0
CAPS = ["आपका हर", "सवाल है", "आज सुबह", "पर यमलोक", "चित्रगुप्त।", "यमराज ने ब्रह्मा", "अनगिनत", "तब ब्रह्मा", "और बहुत समय", "उनकी काया", "हाथ में क़लम",
        "ब्रह्मा बोले", "तब से", "और उसी", "इसीलिए आज", "क़लम और दवात", "तो अगली", "क़लम चल"]


def audio():
    import music, mixlib  # noqa: E401
    sec = [(0, at("आज सुबह"), {"pad": 1.0, "sub": 0.9, "pad_bright": 450}),
           (at("आज सुबह") - 0.3, at("तब ब्रह्मा"), {"tanpura": 0.8, "pad": 0.5, "pad_bright": 1000}),
           (at("तब ब्रह्मा") - 0.3, at("तब से"), {"tanpura": 1.0, "pad": 1.0, "pad_bright": 1800}),
           (at("तब से") - 0.3, at("इसीलिए आज"), {"tanpura": 0.8, "drums": 0.5, "pad": 0.5}),
           (at("इसीलिए आज") - 0.3, END, {"tanpura": 1.0, "pad": 0.8, "pad_bright": 1500})]
    hits = [(0.02, "boom", 0.9), (at("सवाल है"), "bayan", 0.7), (at("चित्रगुप्त।"), "boom", 0.9), (at("उनकी काया") + 0.3, "bellhi", 0.8),
            (at("इसलिए कायस्थ"), "bell", 0.5), (at("इसलिए नाम") + 1.0, "bell", 0.6), (at("यमराज फ़ैसला"), "bayan", 0.7), (at("क़लम चल"), "boom", 0.9)]
    mel = (at("उनकी काया") + 0.3, [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11)])
    st = music.score(END, 138.59, sec, hits, mel, bpm=86, seed=16)
    cues = [(0.0, "big-impact", -14), (0.1, "deep-wind-hum", -18, {"max_len": 4, "fade_out": 1.5}), (at("पर यमलोक") - 0.2, "whoosh-transition", -18),
            (at("चित्रगुप्त।"), "light-energy", -16), (at("यमराज ने ब्रह्मा") - 0.2, "whoosh-fast", -20), (at("उनकी काया") + 0.2, "magic-sparkle", -15),
            (at("और परंपरा") + 0.3, "stamp-thump", -11), (at("इसीलिए आज"), "bell-chime", -17)]
    cues += [(at(k) - 0.02, "text-tick", -22) for k in CAPS]
    cues += [(at(k) + 0.6, "paper-pop", -17) for k in ["तुम मेरी", "इसलिए कायस्थ", "और मेरे भीतर"]] + [(at("इसलिए नाम") + 1.0, "paper-pop", -16), (at("आज सुबह"), "paper-pop", -17)]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-8.0)


if __name__ == "__main__":
    audio()
