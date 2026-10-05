"""Procedural UI sound effects (numpy, 48 kHz mono float32). Deterministic.

Names used by cues: key, click, pop, send, whoosh, whoosh_dark, chime, tick, rec, thud.
To use a real sample instead, drop assets/sfx/<name>.wav — it overrides the synth.
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


def track(cues, duration):
    """Mix cues [(name, t, gain)] into one mono track."""
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


def write_wav(path, mono):
    pcm = (np.clip(mono, -1, 1) * 32767).astype("<i2")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    str(path)], input=pcm.tobytes(), check=True)


def export_library(dest):
    """Write every synth SFX to dest/ to audition them."""
    dest = pathlib.Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for name in SYNTH:
        write_wav(dest / f"{name}.wav", np.concatenate([sample(name), np.zeros(SR // 4)]))
        print(f"✓ {dest / name}.wav")
