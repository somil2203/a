"""Eklavya — reference-grammar edit. Audio mix."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0
CAPS = ['और शिष्य ने', 'निषाद', 'द्रोणाचार्य से', 'द्रोण ने मना', 'एकलव्य ने जंगल', 'और उसी', 'एक दिन', 'एकलव्य ने उसके', 'और कुत्ते', 'अर्जुन हैरान', 'द्रोण पहुँचे', 'एकलव्य बोला', 'द्रोण बोले', 'एकलव्य ने बिना', 'अब आप']
HITS = ['महाभारत', 'सात बाण', 'गुरुदेव ने', 'आप ही', 'दाएँ हाथ']
BIG = ['द्रोण ने मना', 'काटकर']


def audio():
    import music, mixlib  # noqa: E401
    n = len(CAPS); cut = [at(CAPS[int(n * f)]) for f in (0.25, 0.5, 0.75)]
    sec = [(0, cut[0], {"tanpura": 0.9, "pad": 0.8, "pad_bright": 800}), (cut[0] - 0.3, cut[1], {"tanpura": 0.8, "pad": 0.5, "drums": 0.4}),
           (cut[1] - 0.3, cut[2], {"tanpura": 0.9, "pad": 0.7, "drums": 0.55, "pad_bright": 1200}), (cut[2] - 0.3, END, {"tanpura": 1.0, "pad": 1.0, "pad_bright": 1800})]
    hits = [(0.02, "boom", 0.9)] + [(at(k), "bell", 0.5) for k in HITS] + [(at(k), "boom", 0.9) for k in BIG]
    mel = (cut[2], [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11)])
    st = music.score(END, 146.83, sec, hits, mel, bpm=82, seed=24)
    cues = [(0.0, "big-impact", -14)] + [(at(k) - 0.02, "text-tick", -22) for k in CAPS] + [(at(k), "paper-pop", -18) for k in HITS] + [(at(k), "light-energy", -16) for k in BIG]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-8.0)


if __name__ == "__main__":
    audio()
