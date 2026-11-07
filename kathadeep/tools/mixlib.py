"""Audio post for Katha Deep: VO master + ducked score + SFX -> mix.wav (-14 LUFS integrated, -1.5 dBTP).
Matches yesterday's episodes (measured -14.3/-14.5 LUFS integrated, peaks below -1.5 dBFS).
"""
import json
import os
import re
import subprocess

import numpy as np

SR = 48000
KD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path, mono=True):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-ac", "1" if mono else "2", "-ar", str(SR), "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()
    return a if mono else a.reshape(-1, 2)


def sfx(name):
    d = f"{KD}/sfx"
    f = [x for x in os.listdir(d) if re.match(rf"mixkit_\d+_{name}\.mp3$", x)][0]
    return load(f"{d}/{f}")


def master_vo(proj):
    """De-mud, gentle compression, presence, two-pass loudnorm to -16 LUFS. No edits to timing."""
    raw = f"{proj}/vo/raw.wav" if os.path.exists(f"{proj}/vo/raw.wav") else f"{proj}/vo/raw.mp3"
    out = f"{proj}/vo/master.wav"
    chain = "highpass=f=70,equalizer=f=280:t=q:w=1.2:g=-2,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2," \
            "equalizer=f=3200:t=q:w=1.4:g=1.5,equalizer=f=9000:t=h:w=2000:g=1"
    st = subprocess.run(["ffmpeg", "-i", raw, "-af", chain + ",loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    m = json.loads(st[st.rindex("{"):st.rindex("}") + 1])
    ln = f"loudnorm=I=-16:TP=-1.5:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", chain + "," + ln, "-ar", str(SR), "-ac", "1", out], check=True)
    return load(out)


def envelope(x, win=0.12):
    k = int(win * SR)
    p = np.convolve(x ** 2, np.ones(k) / k, "same")
    return np.sqrt(p)


def duck_gain(vo, depth_db=-4, attack=0.08, release=0.45):
    """Music gain curve: dips by depth_db while the narrator speaks, recovers in gaps."""
    e = envelope(vo)
    speaking = (e > 0.02).astype(np.float32)
    # smooth with asymmetric attack/release
    g = np.empty_like(speaking)
    a_c, r_c = 1 / (attack * SR), 1 / (release * SR)
    acc = 0.0
    for i in range(0, len(speaking), 64):
        target = speaking[i]
        c = a_c if target > acc else r_c
        acc += (target - acc) * min(1, c * 64)
        g[i:i + 64] = acc
    lo = 10 ** (depth_db / 20)
    return 1 - (1 - lo) * g


def place(buf, sig, t, g_db=0.0, fade_out=None, max_len=None):
    g = 10 ** (g_db / 20)
    s = int(t * SR)
    if max_len:
        sig = sig[: int(max_len * SR)].copy()
    if fade_out:
        sig = sig.copy()
        nf = min(len(sig), int(fade_out * SR))
        sig[-nf:] *= np.linspace(1, 0, nf)
    if s < 0:
        sig, s = sig[-s:], 0
    e = min(len(buf), s + len(sig))
    if buf.ndim == 2:
        buf[s:e] += (sig[: e - s] * g)[:, None]
    else:
        buf[s:e] += sig[: e - s] * g


def mixdown(proj, music_st, cues, dur, music_db=-17.0, out=None):
    """music_st: (n,2) score; cues: [(t, sfx_name, gain_db, kw)]."""
    n = int(dur * SR)
    vo = np.zeros(n, np.float32)
    v = master_vo(proj)
    vo[: min(n, len(v))] = v[:n]
    mus = np.zeros((n, 2), np.float32)
    m = music_st[:n]
    mus[: len(m)] = m
    mus *= 10 ** (music_db / 20)
    mus *= duck_gain(vo)[:, None]
    fx = np.zeros((n, 2), np.float32)
    for c in cues:
        t, name, gdb = c[:3]
        kw = c[3] if len(c) > 3 else {}
        place(fx, sfx(name), t, gdb, **kw)
    mix = vo[:, None] + mus + fx
    tmp = f"{proj}/mix_pre.wav"
    import wave
    with wave.open(tmp, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    out = out or f"{proj}/mix.wav"
    st = subprocess.run(["ffmpeg", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    mm = json.loads(st[st.rindex("{"):st.rindex("}") + 1])
    ln = f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={mm['input_i']}:measured_TP={mm['input_tp']}:measured_LRA={mm['input_lra']}:measured_thresh={mm['input_thresh']}:offset={mm['target_offset']}:linear=true"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", ln + ",alimiter=limit=0.84:level=false", "-ar", str(SR), out], check=True)
    os.remove(tmp)
    # report voice-vs-music balance in speech regions
    sp = envelope(vo) > 0.02
    vr = 20 * np.log10(np.sqrt(np.mean(vo[sp] ** 2)) + 1e-9)
    mr = 20 * np.log10(np.sqrt(np.mean(mus[sp].mean(1) ** 2)) + 1e-9)
    print(f"voice over music during speech: {vr - mr:.1f} dB")
    return out
