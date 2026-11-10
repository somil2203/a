"""Vamana & Raja Bali — animated (Bali Pratipada). Audio mix."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0


def audio():
    import music, mixlib  # noqa: E401
    sec = [(0, at("आज बलि"), {"pad": 1.0, "sub": 1.0, "drums": 0.6, "pad_bright": 600}),
           (at("आज बलि") - 0.3, at("बलि उस समय"), {"tanpura": 0.9, "pad": 0.6, "pad_bright": 1200}),
           (at("बलि उस समय") - 0.3, at("तभी गुरु"), {"tanpura": 0.8, "drums": 0.7}),
           (at("तभी गुरु") - 0.3, at("और जैसे ही"), {"pad": 0.9, "sub": 0.9, "pad_bright": 500}),
           (at("और जैसे ही") - 0.3, at("तब बलि ने सिर"), {"pad": 1.0, "sub": 1.0, "drums": 1.0, "pad_bright": 1800}),
           (at("तब बलि ने सिर") - 0.3, END, {"tanpura": 1.0, "pad": 0.9, "pad_bright": 1600})]
    hits = [(0.02, "boom", 1.0), (0.42, "boom", 1.0), (at("आज बलि"), "bell", 0.6), (at("तीनों लोक"), "bayan", 0.7), (at("वामन रूप"), "bellhi", 0.6),
            (at("तीन क़दम"), "dayan", 0.6), (at("स्वयं विष्णु"), "boom", 1.0), (at("जो वचन"), "bell", 0.5), (at("वामन बढ़ने"), "boom", 0.8),
            (at("पहले क़दम") + 0.35, "boom", 1.0), (at("दूसरे क़दम") + 0.35, "boom", 1.0), (at("और तीसरा"), "bayan", 0.8), (at("प्रभु") + 2.0, "bellhi", 0.8),
            (at("मैं हमेशा"), "bell", 0.6), (at("आज रात"), "bell", 0.6)]
    mel = (at("भगवान प्रसन्न") + 0.2, [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11), (7.6, 2.8, 7)])
    st = music.score(END, 146.83, sec, hits, mel, bpm=96, seed=13)
    cues = [(0.0, "big-impact", -12), (0.4, "whoosh-deep-impact", -12), (at("एक छोटा") - 0.1, "harp-sweep", -18), (at("और उसने"), "cinematic-synth-riser", -18, {"max_len": 2, "fade_out": 0.3}),
            (at("देवता"), "wind-swoosh", -19), (at("भगवान विष्णु"), "light-energy", -16), (at("बलि उस समय"), "river-water", -24, {"max_len": 6, "fade_out": 2}),
            (at("तभी गुरु") - 0.1, "reverse-impact", -16), (at("स्वयं विष्णु"), "trailer-impact", -13), (at("और जैसे ही") + 0.6, "water-splash", -20),
            (at("वामन बढ़ने") - 0.2, "cinematic-trailer-riser", -15, {"max_len": 3.5, "fade_out": 0.5}), (at("पहले क़दम") + 0.3, "big-impact", -11),
            (at("दूसरे क़दम") + 0.3, "big-impact", -11), (at("प्रभु") + 1.9, "whoosh-deep-impact", -13), (at("मैं हमेशा"), "magic-sparkle", -16),
            (at("आज रात") - 0.2, "bell-chime", -16)]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-7.0)


if __name__ == "__main__":
    audio()
