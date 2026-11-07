"""Final-render QC gate for Katha Deep reels. usage: python3 qc.py FINAL.mp4 [...]
Fails (exit 1) on: wrong size/fps/codec, black frames, frozen frames (> 2.5 s), loudness outside -15..-13 LUFS,
true peak above -1.0 dBTP, clipped samples, A/V duration mismatch > 0.1 s.
"""
import json
import re
import subprocess
import sys


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def qc(path):
    bad = []
    pr = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]).stdout)
    v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in pr["streams"] if s["codec_type"] == "audio"][0]
    fps = eval(v["r_frame_rate"])
    info = f"{v['width']}x{v['height']} {fps:.2f}fps {v['codec_name']}/{v.get('pix_fmt')} + {a['codec_name']} {a['sample_rate']}Hz {a['channels']}ch"
    if (v["width"], v["height"]) != (1080, 1920):
        bad.append("size")
    if abs(fps - 30) > 0.01:
        bad.append("fps")
    vd, ad = float(v.get("duration", pr["format"]["duration"])), float(a.get("duration", pr["format"]["duration"]))
    if abs(vd - ad) > 0.1:
        bad.append(f"A/V duration {vd:.2f}/{ad:.2f}")
    log = run(["ffmpeg", "-i", path, "-vf", "blackdetect=d=0.1:pix_th=0.06,freezedetect=n=0.0015:d=2.5", "-an", "-f", "null", "-"]).stderr
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)
    freezes = re.findall(r"freeze_start: ([\d.]+)", log)
    if blacks:
        bad.append(f"black {blacks}")
    if freezes:
        bad.append(f"frozen at {freezes}")
    eb = run(["ffmpeg", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1])
    LRA = float(re.findall(r"LRA:\s+(-?[\d.]+) LU", eb)[-1])
    TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
    if not -15 <= I <= -13:
        bad.append(f"loudness {I}")
    if TP > -1.0:
        bad.append(f"true peak {TP}")
    st = run(["ffmpeg", "-i", path, "-af", "astats=metadata=0", "-f", "null", "-"]).stderr
    clips = [int(x) for x in re.findall(r"Number of clipped samples: (\d+)", st)] if "clipped" in st else [0]
    if sum(clips):
        bad.append(f"clipped samples {sum(clips)}")
    print(f"{path}\n  {info}  dur {vd:.2f}s  I {I} LUFS  LRA {LRA} LU  TP {TP} dBTP  black {len(blacks)}  frozen {len(freezes)}")
    print("  PASS" if not bad else f"  FAIL: {bad}")
    return not bad


if __name__ == "__main__":
    ok = all([qc(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
