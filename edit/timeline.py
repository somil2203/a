"""Shared edit decision list + word timings for the Nokia Short.

All source times are seconds in the raw IMG_8626.mp4. Output times are derived
from the frame-rounded EDL so audio and video stay sample/frame locked.
"""

FPS = 30

# (src_in, src_out, label)
EDL = [
    (12.86, 14.84, "hook"),     # "Nokia ne apni company hi bech di"
    (14.87, 15.45, "kyun"),     # "Kyun?"
    (16.58, 19.95, "era"),      # "2007 se pehle lagbhag har ghar mein ek Nokia ka phone hota tha"
    (22.43, 27.60, "proof"),    # "Wo phone na uski battery ... na kuch repair cost aata tha"
    (28.38, 30.88, "apple"),    # "Lekin jab 2007 mein Apple aaya" + natural beat
    (31.05, 32.70, "flip"),     # "To uske baad poora game palat gaya"
]
END_FRAMES = 36  # 1.2 s end card

NF = [round((b - a) * FPS) for a, b, _ in EDL]
STARTF = [sum(NF[:i]) for i in range(len(NF))]
VOICE_FRAMES = sum(NF)
TOTAL_FRAMES = VOICE_FRAMES + END_FRAMES
DURATION = TOTAL_FRAMES / FPS


def seg_out_start(i):
    return STARTF[i] / FPS


def src2out(t):
    for i, (a, b, _) in enumerate(EDL):
        if a - 0.05 <= t <= b + 0.05:
            return seg_out_start(i) + (t - a)
    raise ValueError(t)


# Caption words: (text, src_start, src_end, style). "|" = page break.
# style: None (white), "hl" (yellow), "red", "apple" (white glow)
_W = [
    ("NOKIA", 12.88, 13.14, "hl"), ("NE", 13.14, 13.32, None), ("APNI", 13.32, 13.54, None),
    "|", ("COMPANY", 13.54, 13.94, "hl"), ("HI", 13.94, 14.04, None),
    "|", ("BECH", 14.04, 14.38, "red"), ("DI", 14.38, 14.80, "red"),
    "|", ("2007", 16.62, 17.00, "hl"), ("SE", 17.00, 17.14, None), ("PEHLE", 17.14, 17.38, None),
    "|", ("LAGBHAG", 17.38, 17.82, None), ("HAR", 17.82, 17.96, "hl"), ("GHAR", 17.96, 18.18, "hl"), ("MEIN", 18.18, 18.38, None),
    "|", ("EK", 18.38, 18.56, None), ("NOKIA", 18.56, 18.86, "hl"),
    "|", ("KA", 18.86, 19.02, None), ("PHONE", 19.02, 19.22, None), ("HOTA", 19.22, 19.44, None), ("THA", 19.44, 19.85, None),
    "|", ("WO", 22.45, 22.60, None), ("PHONE", 22.60, 22.80, "hl"),
    "|", ("NA", 22.80, 22.92, None), ("USKI", 22.92, 23.26, None), ("BATTERY", 23.26, 23.56, "hl"),
    "|", ("KHATAM", 23.56, 23.82, "red"), ("HOTI", 23.82, 24.02, None), ("THI", 24.02, 24.50, None),
    "|", ("NA", 24.70, 24.86, None), ("US", 24.86, 25.10, None), ("PHONE", 25.10, 25.36, None), ("KA", 25.36, 25.54, None),
    "|", ("KABHI", 25.54, 25.74, None), ("TOOTTA", 25.74, 26.08, "red"), ("THA", 26.08, 26.22, None),
    "|", ("NA", 26.22, 26.36, None), ("KUCH", 26.36, 26.70, None), ("REPAIR", 26.70, 27.02, "hl"),
    "|", ("COST", 27.02, 27.25, "hl"), ("AATA", 27.25, 27.44, None), ("THA", 27.44, 27.58, None),
    "|", ("LEKIN", 28.40, 28.80, None), ("JAB", 28.80, 29.10, None),
    "|", ("2007", 29.10, 29.80, "hl"), ("MEIN", 29.80, 29.95, None),
    "|", ("APPLE", 29.95, 30.25, "apple"), ("AAYA", 30.25, 30.60, None),
    "|", ("TO", 31.08, 31.20, None), ("USKE", 31.20, 31.45, None), ("BAAD", 31.45, 31.65, None),
    "|", ("POORA", 31.70, 31.90, None), ("GAME", 31.90, 32.10, "hl"),
    "|", ("PALAT", 32.10, 32.30, "red"), ("GAYA", 32.30, 32.60, "red"),
]


def caption_pages():
    pages, cur = [], []
    for w in _W:
        if w == "|":
            if cur:
                pages.append(cur)
            cur = []
        else:
            txt, s, e, st = w
            cur.append((txt, src2out(s), src2out(e), st))
    if cur:
        pages.append(cur)
    out = []
    for i, p in enumerate(pages):
        start = p[0][1]
        end = p[-1][2] + 0.30
        if i + 1 < len(pages):
            end = min(end, pages[i + 1][0][1])
        out.append((start, end, p))
    return out


# Output-time anchors for graphics / sound (seconds)
def T(src):
    return src2out(src)


A = dict(
    stamp=T(14.04),          # "bech" -> SOLD stamp
    kyun=seg_out_start(1),
    era=seg_out_start(2),
    houses_in=T(17.35),
    nokia_word=T(18.56),
    proof=seg_out_start(3),
    battery=T(22.80),
    drop_start=T(25.20),
    drop_hit=T(25.76),
    receipt=T(26.22),
    receipt_total=T(27.30),
    apple_seg=seg_out_start(4),
    y2007=T(29.10),
    apple_word=T(29.95),
    beat_hit=seg_out_start(5),
    flip_start=T(32.06),
    flip_end=T(32.48),
    end=VOICE_FRAMES / FPS,
)

if __name__ == "__main__":
    print("frames", NF, "total", TOTAL_FRAMES, "dur", round(DURATION, 2))
    for k, v in A.items():
        print(f"{k:14s} {v:6.2f}")
    for s, e, p in caption_pages():
        print(f"{s:5.2f}-{e:5.2f}", " ".join(w[0] for w in p))
