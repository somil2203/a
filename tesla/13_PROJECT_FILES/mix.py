"""Audio post: MASTER_VO + 3-act music arc + synced SFX -> 12_RENDERS/mix.wav (-14 LUFS, -1 dBTP)

Music arc (all Mixkit Stock Music Free License):
  HOOK + STORY   0 -> crazy      464 "Sci-Fi Score" (Arulo): sparse tension, pulse enters on "It's 2003"
  BREATH         crazy -> net    music cut; synth riser + heartbeat (silence before the reveal)
  CONFLICT       net -> crowd    552 "Masking the Masters" (Eugenio Mininni): orchestral-hybrid drop on "In 2007"
  AFTERMATH      crowd -> end    546 "The Farewell" (Eugenio Mininni): emotional resolution
"""
import json
import os
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
END = 49.6
T = json.load(open(f"{ROOT}/13_PROJECT_FILES/anchors.json"))
N = int(END * SR)


def load(path, start=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", path]
    if dur:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()


def sfx(name):
    d = f"{ROOT}/03_SFX"
    f = [x for x in os.listdir(d) if x.startswith(f"mixkit_{name}_")][0]
    return load(f"{d}/{f}")


def place(buf, sig, t, gain_db=0.0, fade_out=None):
    g = 10 ** (gain_db / 20)
    s = int(t * SR)
    sig = sig * g
    if fade_out:
        n = min(len(sig), int(fade_out * SR))
        sig = sig.copy()
        sig[-n:] *= np.linspace(1, 0, n)
    if s < 0:
        sig, s = sig[-s:], 0
    e = min(len(buf), s + len(sig))
    buf[s:e] += sig[:e - s]


def fades(x, fin, fout):
    x = x.copy()
    a, b = int(fin * SR), int(fout * SR)
    if a:
        x[:a] *= np.linspace(0, 1, a) ** 2
    if b:
        x[-b:] *= np.linspace(1, 0, b) ** 1.5
    return x


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def main():
    vo = np.zeros(N, np.float32)
    v = load(f"{ROOT}/01_VO/MASTER_VO.wav")
    vo[:min(N, len(v))] = v[:N]

    # ---------------- music arc
    mus = np.zeros(N, np.float32)
    M = f"{ROOT}/02_MUSIC"
    a_end = T["crazy"] + 0.25
    m1 = fades(load(f"{M}/mixkit_464_sci-fi-score.mp3", 12.8, a_end), 0.4, 0.45)
    m2 = fades(load(f"{M}/mixkit_552_masking-the-masters.mp3", 68.0, T["crowd"] + 0.6 - T["net"]), 0.03, 0.9)
    m3 = fades(load(f"{M}/mixkit_546_the-farewell.mp3", 21.5, END - T["crowd"] + 0.3), 0.8, 2.2)
    for m, t0, db in ((m1, 0.0, -2.0), (m2, T["net"], 3.0), (m3, T["crowd"] - 0.3, 0.0)):
        m = m / (10 ** (rms_db(m) / 20)) * 10 ** (-20 / 20)  # level-match each cue to -20 dBFS RMS
        place(mus, m, t0, db)

    # ---------------- sound design (timed to the picture anchors)
    fx = np.zeros(N, np.float32)
    P = place
    P(fx, sfx("2303"), 0.0, -8)
    for k in range(18):  # typing the question
        P(fx, sfx("1119"), 0.05 + k * 1.05 / 18, -20)
    P(fx, sfx("3124"), T["answer"], -10)
    P(fx, sfx("2568"), T["answer"] + 0.25, -12)
    P(fx, sfx("759"), T["wrong"] - 0.02, -3)
    P(fx, sfx("2299"), T["wrong"], -4)
    P(fx, sfx("1143"), T["wrong"] - 0.15, -8)
    P(fx, sfx("1088"), T["y2003"] - 0.35, -10, fade_out=0.6)
    P(fx, sfx("2908"), T["y2003"] + 0.45, -9)
    P(fx, sfx("166"), T["engineers"] - 0.05, -10)
    P(fx, sfx("1133"), T["eberhard"], -9)
    P(fx, sfx("1133"), T["tarp"], -9)
    P(fx, sfx("3120"), T["idea"] + 0.1, -10)
    P(fx, sfx("2596"), T["idea"] + 0.15, -14)
    P(fx, sfx("1492"), T["car"] - 0.15, -8)
    P(fx, sfx("1133"), T["roadster"], -9)
    P(fx, sfx("2299"), T["roadster"], -9)
    P(fx, sfx("2297"), T["storm"], -12, fade_out=0.6)
    P(fx, sfx("2601"), T["flash"] - 0.05, -6, fade_out=1.0)
    P(fx, sfx("2596"), T["nikola"] - 0.15, -10)
    P(fx, sfx("2303"), T["nikola"], -10)
    P(fx, sfx("498"), T["money"] - 0.05, -4)
    P(fx, sfx("2299"), T["money"], -6)
    P(fx, sfx("1523"), T["door"] + 0.1, -5)
    P(fx, sfx("784"), T["muskname"] - 1.6, -12, fade_out=0.2)
    P(fx, sfx("2568"), T["factcheck"], -12)
    P(fx, sfx("788"), T["muskname"], -6, fade_out=1.5)
    P(fx, sfx("3120"), T["seriesA"], -11)
    P(fx, sfx("1064"), T["invests"], -11)
    P(fx, sfx("2299"), T["chairman"], -8)
    P(fx, sfx("2303"), T["control"], -9)
    r = sfx("645")
    P(fx, r[-int(1.75 * SR):], T["crazy"] - 0.05, -6)
    P(fx, sfx("498"), T["crazy"] + 0.2, -8)
    P(fx, sfx("1143"), T["net"] - 0.2, -5)
    P(fx, sfx("2568"), T["y2007"], -11)
    P(fx, sfx("498"), T["pushed"] - 0.05, -4)
    P(fx, sfx("2908"), T["pushed"], -8)
    P(fx, sfx("1492"), T["sued"] - 0.1, -9)
    P(fx, sfx("3194"), T["sued"] + 0.25, -10)
    P(fx, sfx("1530"), T["doc"], -8)
    P(fx, sfx("1104"), T["doc"] + 0.3, -10)
    P(fx, sfx("2568"), T["doc_musk"], -10)
    P(fx, sfx("2299"), T["cofounder"], -6)
    P(fx, fades(sfx("364")[: int(4.2 * SR)], 0.4, 0.8), T["crowd"], -20)
    P(fx, sfx("166"), T["crowd"] - 0.05, -10)
    for k in range(12):
        P(fx, sfx("2568"), T["believes"] + k * 0.09, -19)
    P(fx, sfx("1133"), T["realf"], -10)
    P(fx, sfx("1133"), T["realf"] + 0.12, -12)
    P(fx, sfx("788"), T["names"], -9, fade_out=2.5)

    # ---------------- ducking: music dips ~9 dB under speech, released in pauses
    win = int(0.04 * SR)
    env = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, "same"))
    speech = (env > 10 ** (-38 / 20)).astype(np.float32)
    att, rel = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.35 * SR))
    g = np.empty_like(speech)
    s = 0.0
    for i in range(len(speech)):
        a = att if speech[i] > s else rel
        s = a * s + (1 - a) * speech[i]
        g[i] = s
    duck = 10 ** ((-9 * g) / 20)

    mix = vo + mus * duck * 10 ** (-3 / 20) + fx * 10 ** (-2 / 20)
    stem_dir = f"{ROOT}/12_RENDERS"
    os.makedirs(stem_dir, exist_ok=True)
    raw = mix.astype(np.float32).tobytes()
    meas = subprocess.run(["ffmpeg", "-v", "info", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                           "loudnorm=I=-14:TP=-1:LRA=9:print_format=json", "-f", "null", "-"],
                          input=raw, capture_output=True).stderr.decode()
    m = json.loads(meas[meas.rfind("{"):meas.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          f"alimiter=limit=0.89:attack=2:release=60")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", ln,
                    "-ac", "2", "-c:a", "pcm_s24le", f"{stem_dir}/mix.wav"], input=raw, check=True)
    for name, x in (("stem_music", mus * duck * 10 ** (-3 / 20)), ("stem_sfx", fx * 10 ** (-2 / 20))):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-c:a", "pcm_s24le", f"{stem_dir}/{name}.wav"], input=x.astype(np.float32).tobytes(), check=True)
    print("voice", round(rms_db(vo), 1), "music", round(rms_db(mus * duck * 10 ** (-3 / 20)), 1), "sfx",
          round(rms_db(fx * 10 ** (-2 / 20)), 1))


if __name__ == "__main__":
    main()
