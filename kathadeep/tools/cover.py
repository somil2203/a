"""Clean cover: art crop (no burned-in captions) + darkened top + two-line cover text + series tag.
usage: python3 cover.py OUT.jpg ART_PATH cx cy wf GRADE TAG "LINE 1" "LINE 2"
"""
import sys
import kd
from PIL import Image, ImageDraw
out, art, cx, cy, wf, gk, tag, c1, c2 = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:6]), *sys.argv[6:10]
im = kd.grade(kd.kb_frame(kd.load_rgb(art), (cx, cy, wf), (cx, cy, wf), 0), gk if gk != "none" else None)
im = kd.finish(im, 0).convert("RGBA")
ov = Image.new("RGBA", im.size); d = ImageDraw.Draw(ov)
for y in range(im.height):
    d.line((0, y, im.width, y), fill=(0, 0, 0, int(215 * max(0, 1 - y / (im.height * 0.5)))))
im.alpha_composite(ov)
y = 330
for line, col in ((c1, kd.CREAM), (c2, kd.GOLD)):
    size = 150 if len(line) <= 13 else int(150 * 13 / len(line))
    t = kd.text_img(line, "anton", size, col)
    im.alpha_composite(t, (int(kd.W / 2 - t.width / 2), y)); y += int(size * 1.02)
p = kd.tag_pill(tag); im.alpha_composite(p, (kd.W - p.width - 44, 70))
im.convert("RGB").save(out, quality=92)
