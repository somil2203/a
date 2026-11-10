"""Bhai Dooj · Din 5 — reference-grammar edit. Audio: VO-forward, soft tanpura/pad bed, a light tick under each caption build,
paper pops on props (cards, pills, calendar), stamp thumps; impacts only at the hook, the turn (Kartik Dvitiya) and Tathastu."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KD = os.path.dirname(HERE)
sys.path.insert(0, f"{KD}/tools")
import kd  # noqa: E402
T = kd.Timing(HERE); at = T.at; END = T.end + 2.0

CAPS = ["मौत के देवता", "जिनके दरवाज़े", "साल में एक", "खाना खाने", "आज भाई दूज", "और ये कहानी", "पद्म पुराण", "सूर्य देव", "भाई और बहन", "यम बने",
        "और यमुना, धरती", "यमुना बार-बार", "भैया", "पर यम के", "हर दिन", "आज नहीं", "न्योते पर", "फिर आई", "और इस बार", "यमराज मना", "यमुना ने आरती",
        "माथे पर", "और अपने हाथों", "यमराज इतने", "बहन, जो चाहो", "आप होते", "यमुना ने अपने", "यमराज बोले", "तथास्तु", "सोचिए", "धनतेरस पर", "और आज", "पाँच दिन"]
POPS = ["ख़ुद किसी", "उसी दरवाज़े", "यम और यमुना", "हर जीव", "सोना", "स्वर्ग", "अमरता", "हर साल इसी", "और जो भाई", "पाँच दिये", "ये रील", "दीपोत्सव"]


def audio():
    import music, mixlib  # noqa: E401
    sec = [(0, at("आज भाई दूज"), {"pad": 1.0, "sub": 1.0, "pad_bright": 450}),
           (at("आज भाई दूज") - 0.3, at("यमुना बार-बार"), {"tanpura": 0.9, "pad": 0.5, "pad_bright": 1200}),
           (at("यमुना बार-बार") - 0.3, at("फिर आई"), {"tanpura": 0.8, "drums": 0.55, "pad": 0.4}),
           (at("फिर आई") - 0.3, at("आप होते"), {"tanpura": 1.0, "pad": 0.8, "drums": 0.45, "pad_bright": 1600}),
           (at("आप होते") - 0.3, at("यमराज बोले"), {"tanpura": 0.8, "pad": 0.6, "pad_bright": 900}),
           (at("यमराज बोले") - 0.3, END, {"tanpura": 1.0, "pad": 0.9, "pad_bright": 1700})]
    hits = [(0.02, "boom", 1.0), (at("खाना खाने"), "bellhi", 0.6), (at("आज भाई दूज"), "bell", 0.5), (at("फिर आई"), "boom", 0.8),
            (at("माथे पर") + 0.2, "bellhi", 0.6), (at("तथास्तु"), "boom", 1.0), (at("और आज"), "bell", 0.6), (at("आज पूरी"), "bellhi", 0.7)]
    mel = (at("यमुना ने आरती"), [(0, 1.0, 7), (1.0, 1.0, 9), (2.0, 2.0, 11), (4.2, 0.8, 12), (5.0, 2.4, 11), (7.6, 2.8, 7)])
    st = music.score(END, 138.59, sec, hits, mel, bpm=88, seed=15)
    cues = [(0.0, "big-impact", -13), (0.05, "deep-wind-hum", -17, {"max_len": 5, "fade_out": 1.5}), (at("साल में एक") - 0.2, "whoosh-transition", -18),
            (at("आज भाई दूज") - 0.15, "whoosh-fast", -20), (at("पद्म पुराण"), "kd-placeholder", 0)]
    cues = [c for c in cues if c[1] != "kd-placeholder"] + [(at("पद्म पुराण") + 0.35, "stamp-thump", -14)]
    cues += [(at(k) - 0.02, "text-tick", -22) for k in CAPS] + [(at(k), "paper-pop", -17) for k in POPS]
    cues += [(at("यमुना बार-बार") + 0.3 + i * 1.12, "paper-pop", -20) for i in range(13)]
    cues += [(at("सूर्य देव"), "harp-sweep", -18), (at("और यमुना, धरती"), "river-water", -24, {"max_len": 4, "fade_out": 1.5}), (at("यमराज मना"), "whoosh-transition", -18),
             (at("तथास्तु"), "stamp-thump", -10), (at("तथास्तु") + 0.05, "light-energy", -16), (at("आज पूरी"), "stamp-thump", -12), (at("धनतेरस पर"), "reverse-impact", -17),
             (at("माथे पर") + 0.2, "magic-sparkle", -18)]
    return mixlib.mixdown(HERE, st, cues, END, music_db=-8.0)


if __name__ == "__main__":
    audio()
