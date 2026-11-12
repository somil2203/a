"""Tat Tvam Asi — reference-grammar edit. Audio mix."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0
CAPS = ['बारह साल', 'छांदोग्य', 'और घमंड', 'पिता ने पूछा', 'और अनजाना', 'श्वेतकेतु बोला', 'पिता बोले — इस', 'सुबह बोले', 'नमक दिखा', 'ऊपर से', 'पिता बोले — दिखता', 'वैसे ही', 'वही सत्य', 'वो तुम हो', 'उपनिषद की अगली', 'जब एक स्त्री']
HITS = ['और घमंड', 'इस पानी', 'ऊपर से', 'बीच से', 'नीचे से']
BIG = ['तत् त्वम्']


def audio():
    import music, mixlib  # noqa: E401
    n = len(CAPS); cut = [at(CAPS[int(n * f)]) for f in (0.25, 0.5, 0.75)]
    sec = [(0, cut[0], {"tanpura": 0.9, "pad": 0.8, "pad_bright": 800}), (cut[0] - 0.3, cut[1], {"tanpura": 0.8, "pad": 0.5, "drums": 0.4}),
           (cut[1] - 0.3, cut[2], {"tanpura": 0.9, "pad": 0.7, "drums": 0.55, "pad_bright": 1200}), (cut[2] - 0.3, END, {"tanpura": 1.0, "pad": 1.0, "pad_bright": 1800})]
    hits = [(0.02, "boom", 0.9)] + [(at(k), "bell", 0.5) for k in HITS] + [(at(k), "boom", 0.9) for k in BIG]
    mel = (cut[2], [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11)])
    st = music.score(END, 138.59, sec, hits, mel, bpm=86, seed=18)
    cues = [(0.0, "big-impact", -14)] + [(at(k) - 0.02, "text-tick", -22) for k in CAPS] + [(at(k), "paper-pop", -18) for k in HITS] + [(at(k), "light-energy", -16) for k in BIG]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-8.0)


if __name__ == "__main__":
    audio()
