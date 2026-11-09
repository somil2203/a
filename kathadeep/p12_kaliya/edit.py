"""Kaliya Daman — animated. Audio mix (picture: scenes.js via tools/anim/render.js)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0


def audio():
    import music, mixlib  # noqa: E401
    sec = [(0, at("एक दिन"), {"pad": 0.9, "sub": 1.0, "pad_bright": 400}),
           (at("एक दिन") - 0.3, at("फिर कृष्ण कदंब"), {"tanpura": 0.8, "pad": 0.5, "pad_bright": 900}),
           (at("फिर कृष्ण कदंब") - 0.3, at("तभी कृष्ण"), {"pad": 0.9, "sub": 1.0, "drums": 0.7, "pad_bright": 500}),
           (at("तभी कृष्ण") - 0.3, at("कालिया थककर"), {"tanpura": 1.0, "drums": 1.0, "pad": 0.7, "pad_bright": 1800}),
           (at("कालिया थककर") - 0.3, at("कल सुबह"), {"tanpura": 0.9, "pad": 0.9, "pad_bright": 1500}),
           (at("कल सुबह") - 0.3, END, {"tanpura": 0.8, "drums": 0.6, "pad": 0.6})]
    hits = [(0.05, "boom", 0.8), (at("उसी पानी") + 1.2, "boom", 1.0), (at("कालिया नाग"), "boom", 1.0), (at("और बेहोश"), "bayan", 0.8),
            (at("सबको फिर") + 0.3, "bellhi", 0.6), (at("छलाँग") + 0.9, "boom", 1.0), (at("सिर्फ़ बलराम"), "bell", 0.5), (at("कुंडली ढीली"), "boom", 0.8),
            (at("कालिया के फनों"), "boom", 0.9), (at("नृत्य"), "bellhi", 0.8)] + [(at("नृत्य") + 0.42 * i, "dayan" if i % 2 else "bayan", 0.55) for i in range(1, 12)] + \
           [(at("प्रभु"), "bell", 0.6), (at("तुम्हारे फनों") + 0.5, "bellhi", 0.7), (at("कल सुबह"), "bell", 0.6)]
    mel = (at("नृत्य") + 0.2, [(0, 0.5, 7), (0.5, 0.5, 9), (1.0, 0.5, 11), (1.5, 1.0, 12), (2.6, 0.5, 11), (3.1, 0.5, 9), (3.6, 1.2, 7)])
    st = music.score(END, 146.83, sec, hits, mel, bpm=110, seed=12)
    cues = [(0.0, "deep-wind-hum", -15, {"max_len": 4, "fade_out": 1.5}), (at("कि ऊपर") + 0.4, "whoosh-fast", -19), (at("उसी पानी") + 1.15, "water-splash", -12),
            (at("कालिया नाग") - 0.3, "reverse-impact", -14), (at("कालिया नाग"), "big-impact", -13), (at("ज़हर उगलता"), "fire-beam", -19),
            (at("कृष्ण ने अपनी") + 0.4, "light-energy", -15), (at("छलाँग") - 0.1, "whoosh-transition", -16), (at("छलाँग") + 0.85, "water-splash", -11),
            (at("कालिया ने उन्हें"), "heartbeat-impact", -15), (at("तभी कृष्ण") + 0.4, "cinematic-synth-riser", -16, {"max_len": 2.6, "fade_out": 0.3}),
            (at("कुंडली ढीली"), "big-impact", -13), (at("और कृष्ण उछलकर"), "whoosh-deep-impact", -14), (at("नृत्य") - 0.1, "trailer-impact", -13),
            (at("तब नाग"), "harp-sweep", -16), (at("समुद्र के"), "river-water", -21, {"max_len": 3, "fade_out": 1}), (at("अब गरुड़"), "wind-swoosh", -16),
            (at("कल सुबह") - 0.2, "bell-chime", -16)]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-6.0)


if __name__ == "__main__":
    audio()
