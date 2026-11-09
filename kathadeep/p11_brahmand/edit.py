"""Yashoda & the Brahmand — animated. Audio mix (picture: scenes.js via tools/anim/render.js)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0


def audio():
    import music, mixlib  # noqa: E401
    sec = [(0, at("गोकुल की बात"), {"pad": 1.0, "sub": 0.7, "pad_bright": 900}),
           (at("गोकुल की बात") - 0.3, at("और कान्हा ने मुँह"), {"tanpura": 0.8, "drums": 0.6, "pad": 0.3}),
           (at("और कान्हा ने मुँह") - 0.3, at("यशोदा काँप"), {"pad": 1.0, "sub": 0.8, "tanpura": 0.6, "pad_bright": 2000}),
           (at("यशोदा काँप") - 0.3, at("तभी कान्हा"), {"pad": 0.8, "sub": 1.0, "pad_bright": 500}),
           (at("तभी कान्हा") - 0.3, at("अगली कहानी"), {"tanpura": 1.0, "pad": 0.9, "pad_bright": 1600}),
           (at("अगली कहानी") - 0.3, END, {"pad": 0.8, "sub": 0.9, "drums": 0.6, "pad_bright": 400})]
    hits = [(0.05, "bell", 0.6), (at("पूरा ब्रह्मांड"), "boom", 1.0), (at("गोकुल की बात"), "bell", 0.5), (at("मैया, कान्हा"), "dayan", 0.6),
            (at("क्यों खाई"), "bayan", 0.7), (at("और कान्हा ने मुँह") + 1.0, "bellhi", 0.6), (at("आकाश"), "boom", 0.8)] + \
           [(at(k), "bell", 0.35) for k in ["दिशाएँ", "पर्वत", "द्वीप", "समुद्र", "पूरी पृथ्वी", "अग्नि", "वायु", "चंद्रमा", "तारे"]] + \
           [(at("ख़ुद यशोदा"), "boom", 0.9), (at("स्वयं भगवान"), "boom", 1.0), (at("बस एक बच्चा"), "bellhi", 0.6), (at("कालिया"), "boom", 0.9)]
    mel = (at("तभी कान्हा") + 0.3, [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11), (7.6, 2.8, 7)])
    st = music.score(END, 138.59, sec, hits, mel, bpm=90, seed=11)
    cues = [(0.0, "harp-sweep", -17), (at("और उस छोटे") + 0.5, "cinematic-synth-riser", -16, {"max_len": 2.4, "fade_out": 0.3}), (at("पूरा ब्रह्मांड") - 0.05, "big-impact", -13),
            (at("बलराम") - 0.2, "whoosh-fast", -19), (at("और कान्हा ने मुँह") + 0.6, "light-energy", -15), (at("भागवत पुराण") - 0.1, "reverse-impact", -16),
            (at("आकाश") - 0.1, "magic-sparkle", -17), (at("समुद्र") - 0.1, "water-splash", -20), (at("अग्नि"), "soft-fire-woosh", -18), (at("वायु") - 0.1, "wind-swoosh", -19),
            (at("और उसी में") + 0.4, "whoosh-transition", -17), (at("यशोदा काँप"), "heartbeat-impact", -15), (at("स्वयं भगवान"), "trailer-impact", -13),
            (at("तभी कान्हा") + 0.4, "harp-sweep", -15), (at("अगली कहानी") - 0.2, "deep-wind-hum", -16, {"max_len": 4, "fade_out": 1.5})]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-7.6)


if __name__ == "__main__":
    audio()
