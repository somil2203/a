"""Original procedural score for Katha Deep (no third-party music, no licence questions).

Layers: tanpura (Karplus-Strong + jawari buzz), sustained drone pad, low sub swells, tabla-like
dayan/bayan strokes on a theka, temple-bell partials, bansuri-like lead (sine + breath, meend & vibrato),
all through a shared convolution reverb. A project calls score(...) with sections and hits.
"""
import numpy as np

SR = 48000
rng = np.random.default_rng(11)


def t_(n):
    return np.arange(n) / SR


def env_adsr(n, a=0.01, d=0.1, s=0.6, r=0.3):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[na:na + nd] = np.linspace(1, s, len(e[na:na + nd]))
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def onepole(x, a):
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # only used on short buffers
        acc += a * (x[i] - acc)
        y[i] = acc
    return y


def lp(x, fc):
    """Cheap FFT low-pass with soft knee."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / fc) ** 4)
    return np.fft.irfft(X, len(x))


def hp(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (fc / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def ks_pluck(f0, dur, bright=0.5, decay=0.9985):
    """Karplus-Strong string; returns mono buffer."""
    n = int(dur * SR)
    p = int(SR / f0)
    buf = rng.uniform(-1, 1, p)
    buf = buf * bright + np.convolve(buf, np.ones(4) / 4, "same") * (1 - bright)
    out = np.empty(n)
    idx = 0
    for i in range(n):
        v = buf[idx]
        nxt = buf[(idx + 1) % p]
        buf[idx] = decay * 0.5 * (v + nxt)
        out[i] = v
        idx = (idx + 1) % p
    return out


_TAN_CACHE = {}


def tanpura_note(f0, dur=5.0):
    key = (round(f0, 2), dur)
    if key not in _TAN_CACHE:
        x = ks_pluck(f0, dur, 0.85, 0.9993)
        x += 0.5 * ks_pluck(f0 * 1.0015, dur, 0.85, 0.9993)
        x = np.tanh(2.2 * x) * 0.6 + 0.4 * x           # jawari-style buzz
        x = hp(x, 70)
        x *= np.exp(-t_(len(x)) * 0.35)
        _TAN_CACHE[key] = x / (np.abs(x).max() + 1e-9)
    return _TAN_CACHE[key]


def bell(f0, dur=4.0):
    tt = t_(int(dur * SR))
    parts = [(1, 1.0, 1.2), (2.76, 0.55, 1.9), (5.40, 0.32, 2.8), (8.93, 0.18, 3.6), (0.5, 0.35, 0.8)]
    x = sum(a * np.sin(2 * np.pi * f0 * r * tt + rng.uniform(0, 6)) * np.exp(-tt * d) for r, a, d in parts)
    x[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return x / np.abs(x).max()


def dayan(f0=520, dur=0.6, open_=True):
    tt = t_(int(dur * SR))
    d = 6 if open_ else 22
    x = (np.sin(2 * np.pi * f0 * tt) + 0.5 * np.sin(2 * np.pi * f0 * 2.0 * tt) + 0.3 * np.sin(2 * np.pi * f0 * 3.0 * tt)) * np.exp(-tt * d)
    x += rng.normal(0, 1, len(tt)) * np.exp(-tt * 120) * 0.4
    return x / np.abs(x).max()


def bayan(f0=95, dur=0.9, bend=0.7):
    tt = t_(int(dur * SR))
    f = f0 * (1 + bend * np.exp(-tt * 9))  # characteristic pitch glide (ge)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-tt * 4.5)
    x += rng.normal(0, 1, len(tt)) * np.exp(-tt * 90) * 0.15
    return x / np.abs(x).max()


def sub_boom(dur=2.5, f0=48):
    tt = t_(int(dur * SR))
    f = f0 * (1 + 1.5 * np.exp(-tt * 14))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.6)
    return x / np.abs(x).max()


def pad(f0, dur, ratios=(1, 1.5, 2, 3), bright=900):
    n = int(dur * SR)
    tt = t_(n)
    x = np.zeros(n)
    for k, r in enumerate(ratios):
        for det in (-0.25, 0.0, 0.25):
            f = f0 * r * (1 + det / 100)
            ph = rng.uniform(0, 1)
            x += ((tt * f + ph) % 1.0 * 2 - 1) / (k + 1)  # saw
    x = lp(x, bright)
    x *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * tt)
    return x / (np.abs(x).max() + 1e-9)


def bansuri(notes, base):
    """notes: [(start_s, dur_s, semitone_from_Sa)] -> mono buffer starting at 0 (length to last note end)."""
    end = max(s + d for s, d, _ in notes) + 1.0
    n = int(end * SR)
    out = np.zeros(n)
    prev = None
    for s, d, st in notes:
        m = int(d * SR)
        tt = t_(m)
        f_target = base * 2 ** (st / 12)
        f_start = prev if prev else f_target
        glide = np.exp(-tt * 18)
        f = f_target + (f_start - f_target) * glide           # meend
        f *= 1 + 0.006 * np.sin(2 * np.pi * 5.2 * tt) * np.clip(tt / 0.35, 0, 1)  # vibrato
        ph = 2 * np.pi * np.cumsum(f) / SR
        tone = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
        breath = lp(rng.normal(0, 1, m), 2500) * 0.12
        e = env_adsr(m, 0.09, 0.2, 0.75, min(0.4, d * 0.5))
        a = int(s * SR)
        out[a:a + m] += (tone + breath) * e
        prev = f_target
    return out / (np.abs(out).max() + 1e-9)


def reverb_ir(sec=3.2, damp=1.9):
    n = int(sec * SR)
    tt = t_(n)
    ir = rng.normal(0, 1, n) * np.exp(-tt * damp)
    ir = lp(ir, 5000)
    ir[: int(0.012 * SR)] = 0
    return ir / np.sqrt(np.sum(ir ** 2))


def conv(x, ir):
    n = len(x) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[: len(x)]


def place(buf, sig, t, g=1.0):
    a = int(t * SR)
    if a >= len(buf):
        return
    e = min(len(buf), a + len(sig))
    buf[a:e] += sig[: e - a] * g


def fade_mask(n, sections, key, fade=1.2):
    """Gain envelope (0..level) for a layer from sections [(t0,t1,{layer:level})]."""
    g = np.zeros(n)
    for t0, t1, lv in sections:
        v = lv.get(key, 0)
        if not v:
            continue
        a, b = int(t0 * SR), min(n, int(t1 * SR))
        seg = np.ones(b - a) * v
        fa = min(int(fade * SR), (b - a) // 2)
        seg[:fa] *= np.linspace(0, 1, fa)
        seg[-fa:] *= np.linspace(1, 0, fa)
        g[a:b] = np.maximum(g[a:b], seg)
    return g


def score(dur, sa, sections, hits=(), melody=None, bpm=84, seed=1):
    """sa: tonic Hz. sections: [(t0,t1,{'tanpura':g,'pad':g,'drums':g,'sub':g})].
    hits: [(t, kind, gain)] kinds: bell, boom, bayan, dayan, bellhi. melody: (start, notes) for bansuri.
    Returns stereo float32 (n,2)."""
    global rng
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    dry = np.zeros(n)
    wet_send = np.zeros(n)

    # tanpura: Pa Sa' Sa' Sa cycle
    tan = np.zeros(n)
    cyc = [sa * 1.5 / 2, sa, sa, sa / 2]
    step = 1.25
    t = 0.0
    k = 0
    while t < dur:
        place(tan, tanpura_note(cyc[k % 4], 5.0), t, 0.55 if k % 4 != 3 else 0.7)
        t += step if k % 4 != 3 else step * 1.6
        k += 1
    tan *= fade_mask(n, sections, "tanpura")
    dry += tan
    wet_send += tan * 0.5

    pd = np.zeros(n)
    for t0, t1, lv in sections:
        if lv.get("pad"):
            p = pad(sa / 2, t1 - t0 + 2.4, ratios=lv.get("pad_ratios", (1, 1.5, 2, 3)), bright=lv.get("pad_bright", 900))
            place(pd, p, t0, 1.0)
    pd *= fade_mask(n, sections, "pad", 2.0)
    dry += pd * 0.45
    wet_send += pd * 0.35

    sb = np.zeros(n)
    for t0, t1, lv in sections:
        if lv.get("sub"):
            tt = t_(int((t1 - t0) * SR))
            place(sb, np.sin(2 * np.pi * sa / 4 * tt), t0, 1.0)
    sb *= fade_mask(n, sections, "sub", 1.5)
    dry += sb * 0.35

    # drums: keherwa-like theka, 8 beats: dha ge na ti | na ke dhi na
    dr = np.zeros(n)
    beat = 60 / bpm / 2
    pat = ["DHA", "GE", "NA", "TI", "NA", "KE", "DHI", "NA"]
    for t0, t1, lv in sections:
        g = lv.get("drums", 0)
        if not g:
            continue
        t = t0
        i = 0
        while t < t1:
            s = pat[i % 8]
            if s in ("DHA", "DHI", "GE"):
                place(dr, bayan(sa / 2.0 if s != "GE" else sa / 2.2, 0.9), t, 0.9)
            if s in ("DHA", "NA", "DHI", "TI"):
                place(dr, dayan(sa * 2 if s != "TI" else sa * 2.5, 0.5, s != "TI"), t, 0.55 if s != "TI" else 0.35)
            if s == "KE":
                place(dr, dayan(sa * 3, 0.15, False), t, 0.2)
            t += beat
            i += 1
    dr *= fade_mask(n, sections, "drums", 0.3)
    dry += dr * 0.7
    wet_send += dr * 0.18

    for t, kind, g in hits:
        if kind == "bell":
            s = bell(sa * 4, 5)
        elif kind == "bellhi":
            s = bell(sa * 6, 4)
        elif kind == "boom":
            s = sub_boom(3.0, sa / 3)
        elif kind == "bayan":
            s = bayan(sa / 2, 1.2, 1.0)
        elif kind == "dayan":
            s = dayan(sa * 2, 0.6)
        else:
            continue
        place(dry, s, t, g)
        place(wet_send, s, t, g * 0.6)

    if melody:
        st, notes = melody
        m = bansuri(notes, sa * 2)
        place(dry, m, st, 0.38)
        place(wet_send, m, st, 0.45)

    ir_l, ir_r = reverb_ir(), reverb_ir()
    L = dry + conv(wet_send, ir_l) * 0.55
    R = dry + conv(wet_send, ir_r) * 0.55
    st = np.stack([L, R], 1)
    st /= np.abs(st).max() + 1e-9
    return (st * 0.89).astype(np.float32)
