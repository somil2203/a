"""Coca-Cola Short audio post: MASTER_VO + 3-act music arc + synced SFX -> 12_RENDERS/mix.wav

Music arc (all Mixkit Stock Music Free License):
  HOOK + 1886 STORY  0 -> crazy         613 "Sicilian Coffee" (Eugenio Mininni): old-world plucks, motif enters on "So he creates a drink"
  BREATH             crazy -> timeline  music out; riser + heartbeat
  REVEAL             timeline -> today  597 "Vertigo" (Eugenio Mininni): driving tension for 1903 / cocaine removed
  AFTERMATH          today -> end       682 "Classical vibes 2" (Grigoriy Nuzhny): documentary resolution
"""

import json
import os
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
END = 54.6
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
    m1 = fades(load(f"{M}/mixkit_613_sicilian-coffee.mp3", 0.0, T["crazy"] + 0.25), 0.3, 0.45)
    m2 = fades(load(f"{M}/mixkit_597_vertigo.mp3", 60.0, T["today"] + 0.5 - T["timeline"]), 0.04, 0.8)
    m3 = fades(load(f"{M}/mixkit_682_classical-vibes-2.mp3", 10.0, END - T["today"] + 0.4), 0.7, 2.4)
    for m, t0, db in ((m1, 0.0, -2.0), (m2, T["timeline"] - 0.02, 2.5), (m3, T["today"] - 0.3, 0.0)):
        m = m / (10 ** (rms_db(m) / 20)) * 10 ** (-20 / 20)
        place(mus, m, t0, db)

    # ---------------- sound design
    fx = np.zeros(N, np.float32)
    P = place
    # hook: swell -> 0.8 s impact (COCAINE slam) -> 1.2 s molecule transformation -> 2.0 s question
    r = sfx("784")
    P(fx, r[int(9.2 * SR):int(10.0 * SR)], 0.0, -8)
    P(fx, sfx("3181"), 0.0, -14, fade_out=0.8)
    P(fx, sfx("788"), 0.8, -3, fade_out=1.6)
    P(fx, sfx("759"), 0.79, -6)
    P(fx, sfx("2299"), 0.8, -3)
    P(fx, sfx("1492"), 1.12, -8)
    P(fx, sfx("3000"), 1.25, -10)
    P(fx, sfx("2925"), 1.5, -14)
    P(fx, sfx("2568"), 2.0, -9)
    P(fx, sfx("2303"), T["cocaine"] - 0.04, -6)
    P(fx, sfx("1133"), T["joke"], -8)
    P(fx, sfx("1104"), T["joke"] + 0.1, -12)
    P(fx, sfx("166"), T["atl"] - 0.05, -10)
    P(fx, sfx("2568"), T["y1886"], -11)
    P(fx, sfx("3124"), T["atlanta"], -9)
    P(fx, sfx("1133"), T["pharm"], -9)
    P(fx, sfx("1489"), T["apoth"] - 0.1, -11)
    P(fx, sfx("498"), T["morphine"], -8)
    P(fx, sfx("2925"), T["search"], -14)
    P(fx, sfx("2833"), T["drink"] - 0.05, -9, fade_out=1.0)
    P(fx, sfx("1530"), T["medicine"] - 0.15, -9)
    P(fx, sfx("2568"), T["two"] + 0.1, -11)
    P(fx, sfx("2568"), T["two"] + 0.25, -12)
    P(fx, sfx("1492"), T["coca1"] - 0.1, -10)
    P(fx, sfx("166"), T["kola"] - 0.15, -10)
    P(fx, sfx("1104"), T["name"], -10)
    P(fx, sfx("2299"), T["name_cola"], -6)
    P(fx, sfx("166"), T["people"] - 0.05, -11)
    P(fx, sfx("1530"), T["people"] + 1.1, -11)          # ENERGY! banner
    P(fx, sfx("1133"), T["claims_ad"], -10)
    P(fx, sfx("1530"), T["claims_ad"] + 0.12, -11)      # CURES HEADACHES! banner
    P(fx, sfx("525"), T["amazing"] + 0.55, -8)          # bottles clink on the cheers
    P(fx, sfx("1530"), T["amazing"] + 0.4, -12)
    P(fx, sfx("2364"), T["ofcourse"] + 0.5, -13)
    r = sfx("645")
    P(fx, r[-int(1.65 * SR):], T["crazy"] - 0.05, -6)
    P(fx, sfx("498"), T["crazy"] + 0.25, -8)
    P(fx, sfx("1143"), T["timeline"] - 0.2, -6)
    P(fx, sfx("1064"), T["timeline"] + 0.2, -12)
    P(fx, sfx("2908"), T["y1903"], -9)
    P(fx, sfx("1104"), T["news"], -10)
    P(fx, sfx("364")[: int(2.0 * SR)], T["news"], -24, fade_out=0.8)
    P(fx, sfx("1492"), T["removed_shot"] - 0.1, -10)
    P(fx, sfx("759"), T["removed"] - 0.02, -10)
    P(fx, sfx("2299"), T["removed"], -6)
    P(fx, sfx("2623"), T["leaves"], -13)
    P(fx, sfx("3181"), T["today"], -10, fade_out=1.0)
    P(fx, sfx("3120"), T["extract"] + 0.3, -11)
    P(fx, sfx("3000"), T["extract"] + 0.6, -14)
    P(fx, sfx("2299"), T["cocaine2"], -8)
    P(fx, sfx("166"), T["nj"] - 0.05, -10)
    P(fx, sfx("1490"), T["nj"] + 0.1, -14)
    P(fx, sfx("3124"), T["jersey"], -9)
    P(fx, sfx("2568"), T["jersey"] + 0.25, -11)
    P(fx, sfx("2364"), T["opencue"] - 0.02, -4)
    P(fx, sfx("2833"), T["opencue"] + 0.15, -12, fade_out=0.8)
    P(fx, sfx("2925"), T["remember"], -16)
    P(fx, sfx("2299"), T["name_end"] - 0.15, -8)
    P(fx, sfx("788"), T["name_end"] + 0.2, -10, fade_out=2.0)

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
