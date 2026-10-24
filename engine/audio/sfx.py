"""Procedural UI sound effects (numpy, 48 kHz mono float32). Deterministic.

Names used by cues: key, click, pop, send, whoosh, whoosh_dark, chime, tick, rec, thud.
To use a real sample instead, drop assets/sfx/<name>.wav — it overrides the synth.

Kits (opt-in, `v.sfx_kit = "wood"`): glass · wood · soft · mech · water. A kit swaps the material of every UI sound
(modal synthesis) and makes them musical: pitched to the score's key, quick runs of pop/tick climb the scale,
chime = the key's triad, thud = the tonic, whooshes rotate 4 variants, ±1 dB per cue. No kit = the classic set.
water = bubbles (2026-10-23, motion-design UI ref): every note is a "bloop" whose pitch rises as it decays (a real
bubble), pops get a small higher droplet after them, whooshes carry a seeded fizz of tiny bubbles.
"""
import pathlib
import subprocess
from functools import lru_cache

import numpy as np

SR = 48000
ROOT = pathlib.Path(__file__).resolve().parents[2]


def _t(dur):
    return np.arange(int(SR * dur)) / SR


def _env(dur, attack=0.002, decay=0.05):
    t = _t(dur)
    return np.minimum(1, t / max(attack, 1e-4)) * np.exp(-t / decay)


def _noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def _onepole_lp(x, a):
    """a: array or scalar smoothing coefficient 0..1 (higher = brighter)."""
    y = np.empty_like(x)
    acc = 0.0
    a = np.broadcast_to(a, x.shape)
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def key(variant=0):
    d = 0.035
    n = _noise(int(SR * d), 10 + variant)
    hp = np.diff(n, prepend=0)  # bright click
    body = np.sin(2 * np.pi * (1800 + 260 * variant) * _t(d))
    return 0.35 * (0.7 * hp + 0.3 * body) * _env(d, 0.0005, 0.006)


def click():
    d = 0.06
    return 0.5 * (np.sin(2 * np.pi * 1300 * _t(d)) * _env(d, 0.0003, 0.012)
                  + 0.4 * np.diff(_noise(int(SR * d), 3), prepend=0) * _env(d, 0.0002, 0.003))


def pop():
    d = 0.09
    t = _t(d)
    f = 950 * np.exp(-t * 28) + 280
    return 0.45 * np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(d, 0.001, 0.03)


def send():
    d = 0.12
    t = _t(d)
    f = 480 + 1100 * (t / d) ** 0.6
    return 0.3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(d, 0.003, 0.05)


def whoosh(dur=0.5, seed=7, dark=False):
    t = _t(dur)
    n = _noise(len(t), seed)
    shape = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    sweep = 0.02 + 0.25 * shape if not dark else 0.01 + 0.08 * shape
    y = _onepole_lp(n, sweep) * shape
    if dark:
        y += 0.6 * np.sin(2 * np.pi * 55 * t) * np.exp(-t * 4) * np.minimum(1, t / 0.02)
    return 0.5 * y / (np.abs(y).max() + 1e-9)


def chime():
    d = 0.9
    t = _t(d)
    y = (np.sin(2 * np.pi * 1318.5 * t) * np.exp(-t * 5)
         + 0.7 * np.sin(2 * np.pi * 1975.5 * t) * np.exp(-np.maximum(t - 0.07, 0) * 5) * (t > 0.07))
    return 0.25 * y * np.minimum(1, t / 0.003)


def tick():
    d = 0.02
    return 0.3 * np.sin(2 * np.pi * 3200 * _t(d)) * _env(d, 0.0002, 0.004)


def rec():
    d = 0.14
    return 0.3 * np.sin(2 * np.pi * 880 * _t(d)) * _env(d, 0.003, 0.08)


def thud():
    d = 0.35
    t = _t(d)
    f = 120 * np.exp(-t * 12) + 45
    return 0.7 * np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(d, 0.002, 0.12)


# ── kits ─────────────────────────────────────────────────────────────────
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7,
        "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
KITS = {   # modes: (ratio, amp, decay s) · strike: noise click · base: octave offset of the pop register
    "glass": dict(modes=((1, 1, .22), (2.32, .45, .12), (4.25, .25, .06), (6.63, .12, .03)), strike=.12, base=72),
    "wood":  dict(modes=((1, 1, .09), (3.93, .40, .035), (9.24, .12, .012)), strike=.30, base=67),
    "soft":  dict(modes=((1, 1, .07), (2.0, .15, .04)), strike=0.0, base=64, drop=True),
    "mech":  dict(modes=((1, .6, .02), (2.7, .5, .012), (5.1, .3, .006)), strike=.60, base=72),
    "water": dict(modes=((1, 1, .045), (2.0, .05, .015)), strike=0.0, base=67, rise=.6),
}
DROPLET = (0.045, 4, 0.35)      # water pop: a second, smaller bubble — (delay s, scale steps up, gain)
FIZZ = 7                         # water whoosh: tiny bubbles riding the swell


def _hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _fft_filt(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR) + 1e-9
    H = np.ones_like(f)
    if hi:
        H /= np.sqrt(1 + (f / hi) ** 4)
    if lo:
        H /= np.sqrt(1 + (lo / f) ** 4)
    return np.fft.irfft(X * H, len(x))


@lru_cache(maxsize=None)
def modal(kit, m, length=1.0, seed=0):
    """One struck note of the kit's material at midi m."""
    k = KITS[kit]
    d = max(md for _, _, md in k["modes"]) * 5 * length
    t = _t(d)
    f = _hz(m) * ((1 + 0.5 * np.exp(-t * 40)) if k.get("drop") else 1)     # 'soft' = bubble: pitch falls in
    if k.get("rise"):                                    # 'water' = real bubble: pitch rises while it rings out
        f = f * (1 + k["rise"] * (1 - np.exp(-t / (k["modes"][0][2] * length))))
    y = np.zeros_like(t)
    for ratio, amp, dec in k["modes"]:
        if _hz(m) * ratio > SR * 0.45:
            continue
        y += amp * np.sin(2 * np.pi * np.cumsum(f * ratio) / SR) * np.exp(-t / (dec * length))
    if k["strike"]:
        y += k["strike"] * _fft_filt(_noise(len(t), 40 + seed), lo=2500) * np.exp(-t / 0.002)
    return 0.4 * y * np.minimum(1, t / (0.003 if k.get("rise") else 0.0008))


@lru_cache(maxsize=None)
def whoosh_v(variant, dark=False, tonic=48):
    """Four whoosh shapes (length, peak position, brightness) — rotated per cue instead of one stock whoosh."""
    dur, peak, lo_hi = ((0.42, .55, (300, 2500)), (0.6, .7, (200, 4000)), (0.35, .4, (500, 6000)),
                        (0.7, .62, (150, 3000)))[variant % 4]
    if dark:
        dur, lo_hi = dur + 0.4, (80, 900)
    t = _t(dur)
    n = _noise(len(t), 70 + variant + (9 if dark else 0))
    x = t / dur
    shape = np.where(x < peak, (x / peak) ** 2, ((1 - x) / (1 - peak)) ** 1.5)
    darkv, bright = _fft_filt(n, hi=lo_hi[0] * 2), _fft_filt(n, lo=lo_hi[0], hi=lo_hi[1])
    y = (darkv * (1 - shape) + bright * shape) * shape
    if dark:
        y = y / (np.abs(y).max() + 1e-9) + 0.5 * np.sin(2 * np.pi * _hz(tonic - 12) * t) * np.sin(np.pi * x) ** 2
    return 0.5 * y / (np.abs(y).max() + 1e-9)


def kit_sample(kit, name, i, deg, tonic, minor):
    """Synth one cue of a kit. deg = scale step for pitched cues (pop/tick/send)."""
    scale = (0, 3, 5, 7, 10) if minor else (0, 2, 4, 7, 9)
    base = KITS[kit]["base"]
    root = tonic + ((base - tonic) // 12) * 12

    def note(d, octave=0):
        o, j = divmod(d, len(scale))
        return root + 12 * (o + octave) + scale[j]

    if name == "pop":
        a = modal(kit, note(deg), 1.0, i % 3)
        if not KITS[kit].get("rise"):
            return a
        delay, up, gain = DROPLET
        b = gain * modal(kit, note(deg + up), 0.6, 0)
        out = np.zeros(int(SR * delay) + len(b))
        out[:len(a)] += a[:len(out)]
        out[int(SR * delay):] += b
        return out
    if name == "tick":
        return 0.6 * modal(kit, note(deg, 1), 0.35, i % 3)
    if name == "click":
        return 0.5 * modal(kit, note(4, 1), 0.25, i % 3)
    if name == "send":
        a = modal(kit, note(deg), 0.6, 0)
        b = modal(kit, note(deg + 2), 0.8, 1)
        out = np.zeros(int(SR * 0.06) + len(b))
        out[:len(a)] += a[:len(out)]
        out[int(SR * 0.06):] += b
        return out
    if name == "chime":
        third = 3 if minor else 4
        parts = [modal(kit, root + 12 + iv, 2.5, j) for j, iv in enumerate((0, third, 7, 12))]
        out = np.zeros(int(SR * 0.07) * 3 + len(parts[-1]))
        for j, s_ in enumerate(parts):
            a = int(SR * 0.07) * j
            out[a:a + len(s_)] += s_ * (0.7 if j < 3 else 0.55)
        return out * 0.8
    if name == "thud":
        t = _t(0.45)
        f = _hz(tonic - 12) * (1 + 1.5 * np.exp(-t * 18))
        body = 0.8 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.14) * np.minimum(1, t / 0.002)
        knock = modal(kit, note(0, -1), 0.6, 0)
        body[:len(knock)] += 0.5 * knock[:len(body)]
        return body
    if name in ("whoosh", "whoosh_dark"):
        w = whoosh_v(i, name == "whoosh_dark", tonic)
        if not KITS[kit].get("rise"):
            return w
        w = 0.6 * w
        rng = np.random.default_rng(90 + i)
        for at, d in zip(np.sort(rng.uniform(0.15, 0.85, FIZZ)), rng.integers(4, 12, FIZZ)):
            b = 0.35 * modal(kit, note(int(d)), 0.4, 0)
            a = int(at * len(w))
            n = min(len(b), len(w) - a)
            w[a:a + n] += b[:n]
        return w
    return SYNTH[name]()


SYNTH = {
    "key": lambda: key(0), "key1": lambda: key(1), "key2": lambda: key(2), "key3": lambda: key(3),
    "click": click, "pop": pop, "send": send, "whoosh": whoosh,
    "whoosh_dark": lambda: whoosh(0.9, 11, dark=True), "chime": chime, "tick": tick, "rec": rec, "thud": thud,
}


@lru_cache(maxsize=None)
def sample(name):
    override = ROOT / "assets" / "sfx" / f"{name}.wav"
    if override.exists():
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(override), "-f", "f32le", "-ac", "1",
                              "-ar", str(SR), "-"], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.float32).astype(np.float64)
    if name not in SYNTH:
        raise KeyError(f"unknown sfx {name!r}; known: {sorted(SYNTH)}")
    return SYNTH[name]().astype(np.float64)


def track(cues, duration, kit=None, key="C", minor=False):
    """Mix cues [(name, t, gain)] into one mono track. kit = None → classic synth set."""
    if kit:
        return _track_kit(cues, duration, kit, key, minor)
    out = np.zeros(int(SR * (duration + 1.5)))
    for i, (name, t, gain) in enumerate(cues):
        if name == "key":  # rotate keyboard variants so typing doesn't machine-gun
            name = ("key", "key1", "key2", "key3")[(i * 7) % 4]
        s = sample(name) * gain
        a = int(t * SR)
        if a < 0 or a >= len(out):
            continue
        b = min(len(out), a + len(s))
        out[a:b] += s[: b - a]
    return out[: int(SR * duration)]


def _track_kit(cues, duration, kit, key, minor):
    if kit not in KITS:
        raise KeyError(f"unknown sfx kit {kit!r}; known: {sorted(KITS)}")
    tonic = 48 + NOTE[key]
    out = np.zeros(int(SR * (duration + 3.0)))
    last = {}                                       # name → (t, deg): quick repeats climb the scale
    count = {}
    for name, t, gain in sorted(cues, key=lambda c: c[1]):
        i = count.get(name, 0)
        count[name] = i + 1
        prev = last.get(name)
        if prev and t - prev[0] < (0.9 if name == "pop" else 0.4):
            deg = (prev[1] + 1) % 8
        else:
            deg = (0, 2, 4, 2)[i % 4]
        last[name] = (t, deg)
        override = ROOT / "assets" / "sfx" / f"{name}.wav"
        s = sample(name) if override.exists() or name in ("key", "rec") else kit_sample(kit, name, i, deg, tonic, minor)
        s = s * gain * 10 ** (((i * 7919) % 21 - 10) / 200)          # ±0.5 dB, deterministic
        a = int(t * SR)
        if a < 0 or a >= len(out):
            continue
        b = min(len(out), a + len(s))
        out[a:b] += s[: b - a]
    return out[: int(SR * duration)]


def write_wav(path, y):
    """Mono (n,) or stereo (n, 2) float → 16-bit WAV."""
    pcm = (np.clip(y, -1, 1) * 32767).astype("<i2")
    ch = 2 if pcm.ndim == 2 else 1
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", str(ch), "-i", "-",
                    str(path)], input=pcm.tobytes(), check=True)


def export_library(dest):
    """Write every synth SFX to dest/ to audition them — classic set + one demo strip per kit
    (pop run, tick run, click, send, chime, thud, whoosh ×4, whoosh_dark) in C major."""
    dest = pathlib.Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for name in SYNTH:
        write_wav(dest / f"{name}.wav", np.concatenate([sample(name), np.zeros(SR // 4)]))
        print(f"✓ {dest / name}.wav")
    demo = ([("pop", 0.3 + 0.18 * j, 1.0) for j in range(5)] + [("tick", 1.6 + 0.08 * j, 1.0) for j in range(8)]
            + [("click", 2.6, 1.0), ("send", 3.0, 1.0), ("chime", 3.6, 1.0), ("thud", 5.0, 1.0)]
            + [("whoosh", 6.0 + 0.9 * j, 1.0) for j in range(4)] + [("whoosh_dark", 9.8, 1.0)])
    for kit in KITS:
        write_wav(dest / f"kit_{kit}.wav", 0.8 * track(demo, 11.5, kit, "C"))
        print(f"✓ {dest}/kit_{kit}.wav")
