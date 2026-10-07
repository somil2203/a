"""PHASE 1: master the VO -> 01_VO/MASTER_VO.wav + 01_VO/timemap.json

Measured on the raw file: noise floor -70..-87 dBFS in pauses, speech ~-26 dBFS RMS,
-24.9 LUFS integrated, MP3 band-limited at 16 kHz, no mains hum (50/60 Hz peaks are
voice harmonics). So processing stays light: tighten pauses, de-click, gentle NR,
HPF, de-ess, 2.5:1 compression, small presence lift, two-pass loudnorm to -16 LUFS.
"""
import json
import os
import re
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = f"{ROOT}/01_VO/RAW_VO.mp3"
OUT = f"{ROOT}/01_VO/MASTER_VO.wav"
SR = 48000

# pause targets (seconds). Default trims dead air; dramatic beats keep more room.
DEFAULT_PAUSE = 0.34
KEEP = {  # raw silence start (approx) -> kept length
    3.30: 0.62,   # "right?" ... "Wrong."  (suspense before the reversal)
    18.91: 0.50,  # "one problem." ... "Money."
    29.95: 0.42,  # "the crazy part." ... "In 2007"
    46.88: 0.85,  # "the real founders?" ... "Most people"  (let the question land)
}


def decode():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", RAW, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def silences():
    log = subprocess.run(["ffmpeg", "-i", RAW, "-af", "silencedetect=n=-40dB:d=0.3", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(st, en))


def tighten(x):
    """Remove the middle of long pauses; returns audio and a raw->new piecewise-linear map."""
    keep_segments = []  # (raw_a, raw_b)
    cur = 0.0
    for s, e in silences():
        if s < 0.2:
            continue
        target = DEFAULT_PAUSE
        for k, v in KEEP.items():
            if abs(s - k) < 0.15:
                target = v
        length = e - s
        if length <= target + 0.02:
            continue
        cut_a = s + target / 2
        cut_b = e - target / 2
        keep_segments.append((cur, cut_a))
        cur = cut_b
    keep_segments.append((cur, len(x) / SR))
    xf = int(0.012 * SR)
    out = []
    tmap = []
    t_new = 0.0
    for a, b in keep_segments:
        seg = x[int(a * SR):int(b * SR)].copy()
        if out:
            seg[:xf] *= np.linspace(0, 1, xf)
            out[-1][-xf:] *= np.linspace(1, 0, xf)
        out.append(seg)
        tmap.append([a, b, t_new])
        t_new += len(seg) / SR
    return np.concatenate(out), tmap


def run_filter(x, chain):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", chain,
                        "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).copy()


def main():
    x = decode()
    x, tmap = tighten(x)
    chain = ",".join([
        "adeclick=w=55:o=75",
        "afftdn=nr=6:nf=-62:tn=1",
        "highpass=f=70:poles=2",
        "equalizer=f=280:t=q:w=1.0:g=-1.5",
        "deesser=i=0.35:m=0.5:f=0.5",
        "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:knee=4:makeup=2",
        "equalizer=f=3200:t=q:w=1.4:g=1.5",
        "highshelf=f=9000:g=1",
    ])
    y = run_filter(x, chain)
    # two-pass loudnorm to -16 LUFS (VO stem; final mix lands at -14)
    meas = subprocess.run(["ffmpeg", "-v", "info", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                           "loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-"],
                          input=y.tobytes(), capture_output=True).stderr.decode()
    m = json.loads(meas[meas.rfind("{"):meas.rfind("}") + 1])
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    z = run_filter(y, ln)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-c:a", "pcm_s24le", OUT], input=z.tobytes(), check=True)
    json.dump(tmap, open(f"{ROOT}/01_VO/timemap.json", "w"), indent=1)
    print(f"raw {len(x)/SR:.2f}s after tighten; wrote {OUT}")


if __name__ == "__main__":
    main()
