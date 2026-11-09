"""python3 build_times.py PROJ  -> PROJ/times.js
Needs PROJ/vo/alignment.json, PROJ/roman.txt (Hinglish, '/' = subtitle phrase break, same word count as the script),
PROJ/keys.txt (one Devanagari phrase per line: timing anchors used by scenes.js)."""
import json, re, sys, os
P = sys.argv[1]
a = json.load(open(f"{P}/vo/alignment.json"))
txt, st, en = "".join(a["characters"]), a["character_start_times_seconds"], a["character_end_times_seconds"]
words = []
for m in re.finditer(r"[^\s—]+", txt):
    core = re.sub(r"[।,.?!…—]", "", m.group())
    if core:
        words.append((core, st[m.start()], en[m.end() - 1]))
toks, brk = [], []
for seg in open(f"{P}/roman.txt", encoding="utf-8").read().split("/"):
    ws = seg.split()
    for j, w in enumerate(ws):
        toks.append(w); brk.append(j == len(ws) - 1)
if len(toks) != len(words):
    for i, (w, r) in enumerate(zip(words, toks)):
        print(i, w[0], r)
    sys.exit(f"word count mismatch: roman {len(toks)} vs script {len(words)}")
KEY = set(open(f"{P}/keywords.txt", encoding="utf-8").read().split()) if os.path.exists(f"{P}/keywords.txt") else set()
subs = [dict(w=r, a=round(w[1], 3), b=round(w[2], 3), br=k, key=r.strip(",.?!") in KEY) for w, r, k in zip(words, toks, brk)]
def at(ph):
    i = txt.index(ph); return round(st[i], 3)
times = {k.strip(): at(k.strip()) for k in open(f"{P}/keys.txt", encoding="utf-8") if k.strip()}
times["END"] = round(en[-1] + 2.0, 3)
times["VO_END"] = round(en[-1], 3)
open(f"{P}/times.js", "w").write("window.TIMES=" + json.dumps(times, ensure_ascii=False) + ";\nwindow.SUBS=" + json.dumps(subs, ensure_ascii=False) + ";\n")
print("ok", len(subs), "words,", len(times), "anchors, END", times["END"])
