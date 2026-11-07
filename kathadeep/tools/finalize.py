"""Mux picture + mix -> FINAL mp4, run QC gate, export cover frame and Hindi SRT.
usage: python3 finalize.py EPISODE_DIR OUTNAME COVER_T "COVER LINE 1" "COVER LINE 2"
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kd  # noqa: E402
import qc  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

ep, name, cover_t, c1, c2 = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5]
final = f"{ep}/{name}"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ep}/picture.mp4", "-i", f"{ep}/mix.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", final], check=True)
ok = qc.qc(final)

# cover: frame from the film, darkened, with big two-line cover text
fr = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(cover_t), "-i", f"{ep}/picture.mp4", "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                    capture_output=True, check=True).stdout
import io  # noqa: E402
im = Image.open(io.BytesIO(fr)).convert("RGBA")
ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
for y in range(im.height):
    a = int(200 * max(0, 1 - y / (im.height * 0.55)))
    d.line((0, y, im.width, y), fill=(0, 0, 0, a))
im.alpha_composite(ov)
y = 420
for line, col in ((c1, kd.CREAM), (c2, kd.GOLD)):
    size = 150 if len(line) <= 14 else int(150 * 14 / len(line)) if len(line) < 24 else 92
    t = kd.text_img(line, "anton", size, col)
    im.alpha_composite(t, (int(kd.W / 2 - t.width / 2), y))
    y += int(size * 1.05)
im.convert("RGB").save(f"{ep}/cover.jpg", quality=92)

# Hindi SRT from ElevenLabs alignment, one sentence per cue
T = kd.Timing(ep)
txt = T.text
cues, start = [], 0
for m in re.finditer(r"[।?\n]", txt):
    seg = txt[start:m.end()].strip()
    if seg.strip("।?\n "):
        i0 = start + (len(txt[start:m.end()]) - len(txt[start:m.end()].lstrip()))
        cues.append((T.st[i0], T.en[m.end() - 1], seg))
    start = m.end()


def ts(x):
    h, r = divmod(x, 3600)
    m_, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m_):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


with open(f"{ep}/captions_hi.srt", "w") as f:
    for k, (a, b, s) in enumerate(cues, 1):
        f.write(f"{k}\n{ts(a)} --> {ts(max(b, a + 0.8))}\n{s}\n\n")
print("cover + srt written", "QC PASS" if ok else "QC FAIL")
sys.exit(0 if ok else 1)
