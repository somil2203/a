"""Brahma Vimohana — animated. Audio mix."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0


def audio():
    import music, mixlib  # noqa: E401
    sec = [(0, at("भागवत पुराण"), {"tanpura": 0.9, "pad": 0.8, "drums": 0.5, "pad_bright": 1400}),
           (at("भागवत पुराण") - 0.3, at("ये सब देख"), {"tanpura": 0.8, "drums": 0.7}),
           (at("ये सब देख") - 0.3, at("और तब कृष्ण"), {"pad": 0.9, "sub": 0.9, "pad_bright": 500}),
           (at("और तब कृष्ण") - 0.3, at("ऐसे पूरा"), {"tanpura": 1.0, "drums": 0.9, "pad": 0.6, "pad_bright": 1600}),
           (at("ऐसे पूरा") - 0.3, at("ब्रह्मा का घमंड"), {"pad": 1.0, "sub": 1.0, "pad_bright": 900}),
           (at("ब्रह्मा का घमंड") - 0.3, END, {"tanpura": 1.0, "pad": 0.9, "drums": 0.5, "pad_bright": 1600})]
    hits = [(0.02, "boom", 1.0), (0.05, "bellhi", 0.6), (at("ख़ुद कृष्ण लौटते"), "boom", 0.8), (at("बछड़े चरते"), "dayan", 0.5), (at("उन्होंने सोचा"), "bayan", 0.8),
            (at("एक गुफा"), "boom", 0.8), (at("वो ख़ुद"), "boom", 1.0), (at("हर बछड़ा बन"), "bell", 0.5), (at("हर ग्वाल-बाल बन"), "bell", 0.5)] + \
           [(at(k), "dayan", 0.5) for k in ["वही चेहरे", "वही लाठियाँ", "वही बाँसुरी", "वही शरारतें"]] + \
           [(at("गुफा में भी"), "bayan", 0.7), (at("चतुर्भुज"), "boom", 1.0), (at("वो कृष्ण के चरणों"), "bellhi", 0.7), (at("बस एक पल"), "boom", 0.8), (at("भाई दूज"), "bell", 0.6)]
    mel = (at("ब्रह्मा का घमंड") + 0.3, [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11), (7.6, 2.8, 7)])
    st = music.score(END, 138.59, sec, hits, mel, bpm=98, seed=14)
    cues = [(0.0, "big-impact", -12), (0.1, "magic-sparkle", -17), (at("बछड़े चरते"), "whoosh-fast", -20), (at("ये सब देख") - 0.2, "harp-sweep", -16),
            (at("ब्रह्मा ने सारे") + 0.2, "cinematic-synth-riser", -16, {"max_len": 2.5, "fade_out": 0.4}), (at("एक गुफा") + 0.6, "whoosh-deep-impact", -14),
            (at("वो ख़ुद") - 0.1, "light-energy", -14), (at("हर बछड़ा बन"), "magic-sparkle", -17), (at("ऐसे पूरा"), "wind-swoosh", -19),
            (at("फिर ब्रह्मा लौटे"), "reverse-impact", -16), (at("चतुर्भुज") - 0.2, "trailer-impact", -12), (at("वो कृष्ण के चरणों"), "harp-sweep", -16),
            (at("बस एक पल") - 0.1, "bell-chime", -15), (at("भाई दूज") - 0.2, "deep-wind-hum", -18, {"max_len": 3, "fade_out": 1})]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-7.0)


if __name__ == "__main__":
    audio()
