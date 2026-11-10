"""Annakut · 56 Bhog kyun? — animated storybook format. Picture: scenes.js (rendered by tools/anim/render.js). This file: audio mix."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0


def audio():
    import music, mixlib  # noqa: E401
    sa = 146.83
    sec = [(0, at("आज अन्नकूट"), {"pad": 0.9, "sub": 0.6, "pad_bright": 900}),
           (at("आज अन्नकूट") - 0.3, at("तभी हुआ"), {"tanpura": 0.9, "pad": 0.5, "drums": 0.7}),
           (at("तभी हुआ") - 0.3, at("अब छप्पन"), {"tanpura": 1.0, "pad": 1.0, "sub": 0.6, "pad_bright": 1800}),
           (at("अब छप्पन") - 0.3, at("बारिश थमी"), {"tanpura": 0.8, "drums": 0.8}),
           (at("बारिश थमी") - 0.3, at("तो आज"), {"tanpura": 0.9, "pad": 0.6, "drums": 0.9, "pad_bright": 1400}),
           (at("तो आज") - 0.3, END, {"tanpura": 1.0, "pad": 0.9, "pad_bright": 1600})]
    hits = [(0.02, "boom", 1.0), (0.05, "bell", 0.6), (at("ख़ुद को"), "boom", 0.8), (at("आज अन्नकूट"), "bell", 0.7), (at("पर छप्पन ही"), "bayan", 0.8),
            (at("खीर"), "dayan", 0.5), (at("हलवा"), "dayan", 0.5), (at("पुए"), "dayan", 0.5), (at("पूड़ियाँ"), "dayan", 0.5),
            (at("विशाल रूप"), "boom", 1.0), (at("मैं ही"), "bellhi", 0.7), (at("अन्न का"), "bell", 0.6), (at("लोक-मान्यता"), "bayan", 0.9),
            (at("एक दाना"), "boom", 0.8), (at("छप्पन।"), "boom", 1.0), (at("हमारा प्रेम"), "bellhi", 0.6), (T.end, "bell", 0.6)]
    mel = (at("तभी हुआ") + 0.3, [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11), (7.6, 2.8, 7)])
    st = music.score(END, sa, sec, hits, mel, bpm=100, seed=10)
    cues = [(0.0, "big-impact", -13), (0.05, "harp-sweep", -18), (at("ख़ुद को") - 0.1, "light-energy", -17), (at("पूरे ब्रज") + 0.4, "magic-sparkle", -17),
            (at("आज अन्नकूट") - 0.2, "whoosh-transition", -17), (at("इंद्र के यज्ञ"), "campfire-crackles", -20, {"max_len": 3, "fade_out": 0.8}),
            (at("खीर") - 0.05, "whoosh-fast", -21), (at("हलवा") - 0.05, "whoosh-fast", -21), (at("पुए") - 0.05, "whoosh-fast", -21), (at("पूड़ियाँ") - 0.05, "whoosh-fast", -21),
            (at("विशाल रूप") - 0.3, "cinematic-synth-riser", -17, {"max_len": 1.6, "fade_out": 0.3}), (at("विशाल रूप") + 0.2, "big-impact", -13),
            (at("और वो सारा") + 0.2, "magic-sparkle", -16), (at("यही है") + 0.3, "harp-sweep", -16), (at("ये शास्त्र") + 1.2, "trailer-impact", -15),
            (at("पर जब") - 0.2, "distant-thunder", -17), (at("बारिश थमी") - 0.1, "wind-swoosh", -19), (at("माँ यशोदा"), "campfire-crackles", -20, {"max_len": 4, "fade_out": 1}),
            (at("छप्पन।") - 0.1, "big-impact", -13), (at("कल, पाँचवाँ") - 0.2, "bell-chime", -16), (at("यमराज") - 0.1, "deep-wind-hum", -18, {"max_len": 3, "fade_out": 1})]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-6.0)


if __name__ == "__main__":
    audio()
