"""Build the voice + SFX + music mix for the Nokia Short.

usage: python3 render_audio.py SRC.mp4 OUT.wav
"""
import subprocess
import sys

import numpy as np

import timeline as TL

SR = 48000
A = TL.A
DUR = TL.DURATION
N = int(DUR * SR) + SR // 2
rng = np.random.default_rng(42)


def read_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def ffilter(x, chain):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-af", chain, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    y = np.frombuffer(p.stdout, np.float32).copy()
    out = np.zeros_like(x)
    out[:min(len(x), len(y))] = y[:len(x)]
    return out


def tvec(d):
    return np.arange(int(d * SR)) / SR


def onepole_lp(x, fc):
    """Time-varying one-pole lowpass; fc scalar or array."""
    fc = np.broadcast_to(np.asarray(fc, np.float64), x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    s = 0.0
    for i in range(len(x)):
        s = a[i] * s + (1 - a[i]) * x[i]
        y[i] = s
    return y


def env(n, att, rel_shape=4.0):
    t = np.linspace(0, 1, n)
    a = int(att * n)
    e = np.ones(n)
    if a > 0:
        e[:a] = np.linspace(0, 1, a)
    e[a:] = np.exp(-rel_shape * np.linspace(0, 1, n - a))
    return e


# ------------------------------------------------------------ SFX
def whoosh(d=0.45, up=True):
    n = int(d * SR)
    x = rng.normal(0, 1, n)
    t = np.linspace(0, 1, n)
    fc = 300 + 5000 * (t if up else 1 - t) ** 1.5
    y = onepole_lp(x, fc) - onepole_lp(x, fc * 0.25)
    e = np.sin(np.pi * t) ** 2
    return y * e * 0.9


def boom(d=0.9, f0=110, f1=38, click=0.4):
    t = tvec(d)
    f = f1 + (f0 - f1) * np.exp(-t * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t * 4.0)
    nz = onepole_lp(rng.normal(0, 1, len(t)), 1800) * np.exp(-t * 35) * click
    return (y + nz) * 0.95


def stamp():
    t = tvec(0.35)
    y = boom(0.35, 160, 60, 1.2)
    y += onepole_lp(rng.normal(0, 1, len(t)), 3500) * np.exp(-t * 40) * 0.6
    return y


def pop(f=900):
    t = tvec(0.07)
    fr = f * (1 + 0.6 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 55) * 0.5


def tick(f=2400, amp=0.35):
    t = tvec(0.04)
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 140) * amp


def ding():
    t = tvec(1.4)
    y = sum(a * np.sin(2 * np.pi * 1568 * r * t) * np.exp(-t * dcy)
            for r, a, dcy in [(1, 1, 3), (2.76, .4, 6), (5.4, .2, 9), (2, .25, 4)])
    return y * 0.32


def crack():
    t = tvec(0.5)
    y = np.zeros(len(t))
    for _ in range(14):
        s = int(rng.uniform(0, 0.12) * SR)
        l = int(rng.uniform(0.005, 0.03) * SR)
        y[s:s + l] += rng.normal(0, 1, l) * np.exp(-np.linspace(0, 6, l)) * rng.uniform(.3, 1)
    y = y - onepole_lp(y, 1500)
    y += sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 12) * 0.08 for f in (2900, 4170, 5230))
    return y * 0.8


def riser(d):
    t = tvec(d)
    p = t / d
    x = rng.normal(0, 1, len(t))
    y = (onepole_lp(x, 400 + 7000 * p ** 2) - onepole_lp(x, 200 + 1500 * p ** 2)) * p ** 2.2 * 0.7
    f = 160 + 700 * p ** 2
    y += np.sin(2 * np.pi * np.cumsum(f) / SR) * p ** 2 * 0.18
    return y


def shimmer(d=0.9):
    t = tvec(d)
    y = np.zeros(len(t))
    for i, f in enumerate([1318, 1760, 2093, 2637, 3136]):
        s = int(i * 0.06 * SR)
        tt = t[: len(t) - s]
        y[s:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 5) * 0.12
    return y


def printer(d=0.55):
    y = np.zeros(int(d * SR))
    for k in np.arange(0, d - 0.03, 0.028):
        c = tick(rng.uniform(3000, 4200), 0.18)
        s = int(k * SR)
        y[s:s + len(c)] += c[: len(y) - s]
    return y


def nokia_tune():
    # opening phrase of Tarrega's Gran Vals (public domain)
    notes = [(88, .5), (86, .5), (78, 1), (80, 1)]  # E6 D6 F#5 G#5 in MIDI
    beat = 0.14
    out = []
    for m, l in notes:
        f = 440 * 2 ** ((m - 69) / 12)
        t = tvec(beat * l * 1.0)
        tone = sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 3, 5))
        out.append(tone * np.exp(-t * 6) * 0.5)
    y = np.concatenate(out)
    return y - onepole_lp(y, 500)


def reverse_swell(d=0.5):
    t = tvec(d)
    x = rng.normal(0, 1, len(t))
    return (x - onepole_lp(x, 2000)) * (t / d) ** 3 * 0.4


def add(buf, sig, t, gain=1.0):
    s = int(t * SR)
    if s < 0:
        sig = sig[-s:]
        s = 0
    e = min(len(buf), s + len(sig))
    buf[s:e] += sig[: e - s] * gain


def build_sfx():
    b = np.zeros(N)
    add(b, boom(1.0, 90, 35, 0.2), 0.0, 0.5)
    add(b, whoosh(0.5), 0.02, 0.35)
    add(b, stamp(), A["stamp"], 0.9)
    add(b, tick(1800), A["stamp"] + 0.2, 0.6)
    add(b, reverse_swell(0.35), A["kyun"] - 0.33, 0.6)
    add(b, boom(1.2, 70, 30, 0.6), A["kyun"], 0.9)
    add(b, whoosh(0.4, False), A["era"] - 0.08, 0.5)
    for k in range(10):
        add(b, tick(2600 - k * 120, 0.3), A["era"] + 0.12 + k * 0.06)
    add(b, whoosh(0.35), A["houses_in"] - 0.15, 0.45)
    add(b, boom(0.9, 90, 35, 0.3), A["houses_in"], 0.5)
    for k in range(12):  # matches the Blender village: house k lights at frame 12 + 3k
        add(b, pop(650 + k * 55), A["houses_in"] + (12 + 3 * k) / 30, 0.45)
    add(b, nokia_tune(), A["nokia_word"], 0.28)
    add(b, whoosh(0.3), A["proof"] - 0.1, 0.4)
    add(b, shimmer(0.6), A["proof"] + 0.1, 0.35)
    add(b, tick(1200, 0.4), A["battery"])
    for d in range(6):
        add(b, tick(2000, 0.35), A["battery"] + 0.45 + d * 0.32)
    add(b, ding() * 0.6, A["battery"] + 0.95, 0.5)
    add(b, whoosh(0.56, False), A["drop_start"], 0.5)
    add(b, boom(0.7, 140, 45, 1.0), A["drop_hit"], 1.0)
    add(b, crack(), A["drop_hit"], 0.7)
    add(b, stamp(), A["drop_hit"] + 0.12, 0.7)
    add(b, whoosh(0.3), A["receipt"] - 0.05, 0.35)
    add(b, printer(0.6), A["receipt"] + 0.3, 0.6)
    add(b, ding(), A["receipt_total"], 0.7)
    add(b, riser(A["beat_hit"] - A["apple_seg"]), A["apple_seg"], 0.55)
    add(b, boom(0.8, 120, 40, 0.8), A["y2007"] + 0.15, 0.75)
    add(b, whoosh(0.6), A["apple_word"] - 0.2, 0.5)
    add(b, shimmer(1.0), A["apple_word"], 0.5)
    add(b, boom(1.6, 80, 28, 1.0), A["beat_hit"], 1.0)
    add(b, reverse_swell(0.3), A["beat_hit"] - 0.3, 0.5)
    add(b, whoosh(0.5), A["flip_start"] - 0.05, 0.8)
    add(b, boom(0.6, 100, 40, 0.3), A["flip_end"], 0.6)
    add(b, boom(1.2, 70, 30, 0.3), A["end"], 0.6)
    add(b, shimmer(1.0), A["end"] + 0.15, 0.4)
    return b


# ------------------------------------------------------------ music
def note(f, d, kind="bass"):
    t = tvec(d)
    if kind == "bass":
        y = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t)
        return y * env(len(t), 0.02, 3.5)
    if kind == "pad":
        y = sum(np.sin(2 * np.pi * f * dt * t + p) for dt, p in ((1, 0), (1.004, 1), (0.996, 2)))
        return y / 3 * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.3)
    if kind == "pluck":
        y = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(6 * np.pi * f * t)
        return y * np.exp(-t * 12)


def kick():
    t = tvec(0.35)
    f = 45 + 120 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def hat():
    t = tvec(0.05)
    x = rng.normal(0, 1, len(t))
    return (x - onepole_lp(x, 7000)) * np.exp(-t * 90) * 0.4


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def build_music():
    m = np.zeros(N)
    bpm = 104
    beat = 60 / bpm
    prog = [(45, [57, 60, 64]), (41, [53, 57, 60]), (48, [55, 60, 64]), (43, [55, 59, 62])]  # Am F C G

    def section(t0, t1, intensity, drums=True, arp=False):
        t = t0
        i = 0
        while t < t1 - 0.01:
            bar = int(i // 4)
            root, chord = prog[bar % 4]
            for k in range(2):
                tt = t + k * beat / 2
                if tt < t1:
                    add(m, note(hz(root - 12), beat / 2 * 0.95), tt, 0.35 * intensity)
            if i % 4 == 0:
                for c in chord:
                    add(m, note(hz(c), min(beat * 4, t1 - t) + 0.05, "pad"), t, 0.06 * intensity)
            if drums:
                add(m, kick(), t, 0.55 * intensity)
                add(m, hat(), t + beat / 2, 0.5 * intensity)
            if arp:
                for k in range(4):
                    tt = t + k * beat / 4
                    if tt < t1:
                        add(m, note(hz(chord[k % 3] + 12), 0.2, "pluck"), tt, 0.07 * intensity)
            t += beat
            i += 1

    section(0.0, A["kyun"] - 0.05, 0.9, drums=True)
    section(A["era"], A["apple_seg"], 0.75, drums=True, arp=True)
    # suspense drone
    d = A["beat_hit"] - A["apple_seg"]
    t = tvec(d)
    drone = (np.sin(2 * np.pi * hz(33) * t) + 0.5 * np.sin(2 * np.pi * hz(40) * t)) * np.minimum(1, t / 0.4)
    add(m, drone, A["apple_seg"], 0.35)
    k = A["apple_seg"]
    while k < A["beat_hit"] - 0.1:
        add(m, tick(1500, 0.3), k, 0.6)
        k += beat / 2
    section(A["beat_hit"], A["end"], 1.15, drums=True, arp=True)
    for c in [45, 57, 60, 64, 69]:
        add(m, note(hz(c), 1.3, "pad"), A["end"], 0.09)
    add(m, note(hz(33), 1.2), A["end"], 0.4)
    # simple reverb
    ir_t = tvec(0.9)
    ir = rng.normal(0, 1, len(ir_t)) * np.exp(-ir_t * 6)
    ir /= np.sqrt(np.sum(ir ** 2))
    L = len(m) + len(ir)
    wet = np.fft.irfft(np.fft.rfft(m, L) * np.fft.rfft(ir, L), L)[: len(m)]
    return m * 0.8 + wet * 0.35


def main():
    src, out = sys.argv[1], sys.argv[2]
    raw = read_audio(src)
    voice = np.zeros(N, np.float32)
    fade = int(0.006 * SR)
    for (a, b, _), sf in zip(TL.EDL, TL.STARTF):
        n = int(TL.NF[TL.STARTF.index(sf)] / TL.FPS * SR)
        seg = raw[int(a * SR): int(a * SR) + n].copy()
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        s = int(sf / TL.FPS * SR)
        voice[s: s + len(seg)] += seg
    voice = ffilter(voice, "highpass=f=85,afftdn=nf=-28,equalizer=f=250:t=q:w=1:g=-2,"
                           "equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-22dB:ratio=3:attack=5:release=90:makeup=4")
    voice /= np.max(np.abs(voice)) + 1e-9
    voice *= 0.7

    sfx = build_sfx()
    music = build_music()
    music /= np.max(np.abs(music)) + 1e-9
    # sidechain duck music under voice
    win = int(0.05 * SR)
    e = np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, "same"))
    e = onepole_lp(e, 6.0)
    duck = 1 - 0.65 * np.clip(e / 0.08, 0, 1)
    mix = voice + music * 0.22 * duck + sfx * 0.45
    mix = mix.astype(np.float32)
    mix = ffilter(mix, "loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.84")
    mix = mix[: int(DUR * SR)]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-ac", "2", out], input=mix.tobytes(), check=True)


if __name__ == "__main__":
    main()
