"""Satyakama Jabala — reference-grammar edit. Audio mix."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0
CAPS = ["गुरु ने पूछा", "और उस बच्चे", "जो कोई", "छांदोग्य", "सत्यकाम नाम", "उसने माँ", "बेटा, जवानी", "मुझे नहीं", "मैं जबाला", "सत्यकाम गुरु", "और सत्यकाम ने",
        "गुरु बोले", "जाओ", "फिर गुरु", "सत्यकाम बोले", "और जब गायें", "तो एक बैल", "उसे ब्रह्म", "जन्म से", "ये रील"]


def audio():
    import music, mixlib  # noqa: E401
    sec = [(0, at("छांदोग्य"), {"tanpura": 0.9, "pad": 0.7, "pad_bright": 900}),
           (at("छांदोग्य") - 0.3, at("सत्यकाम गुरु"), {"tanpura": 0.8, "pad": 0.6, "pad_bright": 700}),
           (at("सत्यकाम गुरु") - 0.3, at("फिर गुरु"), {"tanpura": 0.9, "pad": 0.5, "drums": 0.4}),
           (at("फिर गुरु") - 0.3, at("तो एक बैल"), {"tanpura": 0.8, "drums": 0.6, "pad": 0.5}),
           (at("तो एक बैल") - 0.3, END, {"tanpura": 1.0, "pad": 1.0, "pad_bright": 1800})]
    hits = [(0.02, "boom", 0.8), (at("वो सच बोल"), "bellhi", 0.6), (at("कहना") + 0.2, "bell", 0.6), (at("मैं तुम्हें") + 0.4, "bell", 0.6),
            (at("मैं नहीं लौटूँगा"), "bayan", 0.8), (at("तो एक बैल"), "bell", 0.5), (at("अग्नि"), "bell", 0.5), (at("हंस"), "bell", 0.5), (at("और एक जल"), "bell", 0.5),
            (at("उसे ब्रह्म"), "boom", 0.9), (at("सच से"), "bellhi", 0.8)]
    mel = (at("तो एक बैल"), [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11), (7.6, 2.8, 7)])
    st = music.score(END, 146.83, sec, hits, mel, bpm=84, seed=17)
    cues = [(0.0, "big-impact", -15), (at("छांदोग्य"), "paper-pop", -17), (at("कहना") + 0.2, "paper-pop", -15), (at("माँ की बात"), "paper-pop", -16),
            (at("मैं तुम्हें") + 0.4, "stamp-thump", -11), (at("और जब गायें"), "whoosh-transition", -18), (at("तो एक बैल") - 0.2, "magic-sparkle", -16),
            (at("अग्नि"), "soft-fire-woosh", -18), (at("हंस") - 0.05, "water-splash", -22), (at("उसे ब्रह्म"), "light-energy", -15), (at("ये रील"), "paper-pop", -16)]
    cues += [(at(k) - 0.02, "text-tick", -22) for k in CAPS]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-8.0)


if __name__ == "__main__":
    audio()
