"""Styled procedural score — opt-in successor of the `pulse` score in music.py (stereo, 48 kHz, deterministic).

    v.music = dict(style="lofi", key="F", mood="warm")       # style · key · mood (+ optional seed)

Each style is its own band: instruments, groove (16-step grid + swing), tempo range, transition and space (reverb).
On top of the style, every video gets
  · a seeded **motif** (4–6 notes) — the video's own melody, played from the second chapter on, shifted per chapter
  · **two progressions per mood** — chapters alternate, so the harmony moves through the video instead of looping
  · **arrangement that builds** — intro sparse → chapter 1 adds bass + drums → later chapters add the motif;
    every 8th bar a fill, the bar before a new section a style-specific transition; dark recap = no drums, filtered
  · **humanised** timing/velocity (seeded rng → same file every time)

Sections, beat snapping and the key/mood tables come from music.py. Video tempo (v.bpm) must sit in the style's
range — `check` warns otherwise (the HUD shows the same number).
"""
from functools import lru_cache

import numpy as np

from .music import KEYS, MOODS, SR, _f, _voicing, sections

# second progression per mood (chapters alternate A/B) — one chord per bar
MOODS_B = {
    "warm":   [(0, (0, 4, 7, 11)), (4, (0, 3, 7, 10)), (5, (0, 4, 7, 11)), (5, (0, 3, 7, 10))],    # Imaj7 iii7 IVmaj7 iv7
    "tense":  [(0, (0, 3, 7, 10)), (5, (0, 3, 7, 10)), (8, (0, 4, 7, 11)), (7, (0, 4, 7, 10))],    # i7 iv7 VImaj7 V7
    "bright": [(0, (0, 4, 7, 14)), (7, (0, 4, 7, 14)), (9, (0, 3, 7, 10)), (5, (0, 4, 7, 11))],    # Iadd9 Vadd9 vi7 IVmaj7
    "dreamy": [(0, (0, 4, 7, 11, 14)), (2, (0, 3, 7, 10, 14)), (5, (0, 4, 7, 11, 14)), (4, (0, 3, 7, 10))],
}
SCALE = {"tense": (0, 3, 5, 7, 10)}          # minor pentatonic; every other mood: major pentatonic
SCALE_MAJ = (0, 2, 4, 7, 9)

# 16-step grids ("x" hit · "o" ghost/accent-off · "." rest)
STYLES = {
    "lofi": dict(
        bpm=(76, 94), swing=0.60, reverb=0.28, room=1.6, lowpass=5200, pump=0.0,
        kick="x.....x..x......", snare="....x.......x...", hat="x.o.x.o.x.o.x.oo", perc=None,
        chords="epiano", chord_rhythm="x.............o.", bass="sub", bass_rhythm="x.....x..x......",
        lead="felt", transition="reverse", desc="boom-bap, Rhodes, vinyl — santai, ngobrol"),
    "marimba": dict(
        bpm=(100, 116), swing=0.54, reverb=0.20, room=1.2, lowpass=None, pump=0.0,
        kick="x.......x.......", snare="....x.......x...", hat=None, perc="xoxoxoxoxoxoxoxo",
        chords="softpad", chord_rhythm="x...............", bass="pluck", bass_rhythm="x.....x.x.......",
        ostinato="x.xx.x.xx.x.x.xx", lead="mallet", transition="gliss", desc="mallet + clap — main-main, keynote"),
    "ambient": dict(
        bpm=(70, 90), swing=0.50, reverb=0.45, room=2.8, lowpass=None, pump=0.0,
        kick=None, snare=None, hat=None, perc=None,
        chords="widepad", chord_rhythm="x...............", bass="sub", bass_rhythm="x...............",
        broken="x.....x.....x...", lead="felt", transition="reverse", desc="felt piano + pad, tanpa drum — tenang, dalam"),
    "garage": dict(
        bpm=(126, 136), swing=0.62, reverb=0.15, room=1.0, lowpass=None, pump=0.35,
        kick="x......x..x.....", snare="....x.......x...", hat="..x...x...x...xo", perc="o.o.o.o.o.o.o.o.",
        chords="stab", chord_rhythm="..x..x....x..x..", bass="sub", bass_rhythm="x......x..x.....",
        lead="pluck", transition="riser", desc="2-step shuffle, chord stab — cepat, urban"),
    "cinematic": dict(
        bpm=(88, 110), swing=0.50, reverb=0.35, room=2.2, lowpass=None, pump=0.0,
        kick="x.......x.......", snare=None, hat=None, perc=None, taiko=True,
        chords="widepad", chord_rhythm="x...............", bass="sub", bass_rhythm="x.......x.......",
        ostinato="xxxxxxxxxxxxxxxx", lead="bell", transition="taiko", desc="ostinato string + taiko — tegang, berita"),
}


# ── DSP ─────────────────────────────────────────────────────────────────
def _t(dur):
    return np.arange(max(1, int(SR * dur))) / SR


def _filt(x, lo=None, hi=None, order=2):
    """Zero-phase Butterworth-shaped band filter in the frequency domain (lo = highpass, hi = lowpass)."""
    n = len(x)
    X = np.fft.rfft(x, n)
    f = np.fft.rfftfreq(n, 1 / SR) + 1e-9
    H = np.ones_like(f)
    if hi:
        H /= np.sqrt(1 + (f / hi) ** (2 * order))
    if lo:
        H *= 1 / np.sqrt(1 + (lo / f) ** (2 * order))
    return np.fft.irfft(X * H, n)


def _env(dur, attack=0.004, decay=None, release=0.05):
    t = _t(dur)
    e = np.minimum(1.0, t / max(attack, 1e-4))
    if decay:
        e = e * np.exp(-t / decay)
    r = int(SR * release)
    if 0 < r < len(e):
        e[-r:] *= np.linspace(1, 0, r)
    return e


def _pan(p):
    a = (np.clip(p, -1, 1) + 1) * np.pi / 4
    return np.cos(a), np.sin(a)


def _conv(x, ir):
    n = len(x) + len(ir) - 1
    m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]


def _reverb(stereo, room, seed):
    """Synthetic stereo hall: decaying, darkening noise IR (seeded)."""
    rng = np.random.default_rng(seed + 99)
    t = _t(room)
    out = np.zeros_like(stereo)
    for ch in range(2):
        ir = rng.standard_normal(len(t)) * np.exp(-t * 6.9 / room)
        ir = _filt(ir, lo=180, hi=5200) * np.minimum(1, t / 0.012)
        ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
        out[:, ch] = _conv(stereo[:, ch], ir)
    return out


# ── instruments (mono, cached; velocity applied by the caller) ───────────
@lru_cache(maxsize=None)
def epiano(m, dur):
    f, t = _f(m), _t(dur)
    idx = 1.6 * np.exp(-t / 0.22) + 0.25
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    y += 0.12 * np.sin(2 * np.pi * f * 7.0 * t) * np.exp(-t / 0.05)          # tine
    y *= 1 + 0.10 * np.sin(2 * np.pi * 4.6 * t)                              # tremolo
    return y * _env(dur, 0.003, 1.4, 0.12)


@lru_cache(maxsize=None)
def mallet(m, dur):
    f, t = _f(m), _t(dur)
    k = 0.5 + 0.5 * np.clip((72 - m) / 24, 0, 1)                             # low notes ring longer
    y = (np.sin(2 * np.pi * f * t) * np.exp(-t / (0.42 * k))
         + 0.32 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t / (0.10 * k))
         + 0.10 * np.sin(2 * np.pi * f * 9.24 * t) * np.exp(-t / 0.03))
    return y * _env(dur, 0.0015, None, 0.04)


@lru_cache(maxsize=None)
def felt(m, dur):
    f, t = _f(m), _t(dur)
    y = np.zeros_like(t)
    for k in range(1, 8):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)
        if fk > SR * 0.45:
            break
        y += (1 / k ** 1.7) * np.sin(2 * np.pi * fk * t) * np.exp(-t / (1.8 / k ** 0.7))
    return y * _env(dur, 0.009, None, 0.2)


@lru_cache(maxsize=None)
def pluck(m, dur):
    f, t = _f(m), _t(dur)
    y = np.zeros_like(t)
    for k in range(1, 13):
        if f * k > SR * 0.45:
            break
        y += (1 / k) * np.sin(2 * np.pi * f * k * t) * np.exp(-t / (0.35 / (1 + 0.6 * k)))
    return y * _env(dur, 0.002, None, 0.05)


@lru_cache(maxsize=None)
def bell(m, dur):
    f, t = _f(m), _t(dur)
    y = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d)
            for r, a, d in ((1, 1.0, 1.2), (2.76, 0.4, 0.5), (5.4, 0.15, 0.2), (8.93, 0.06, 0.08)))
    return y * _env(dur, 0.002, None, 0.3)


@lru_cache(maxsize=None)
def saw_pad(m, dur, detune, attack, bright):
    f, t = _f(m) * (1 + detune), _t(dur)
    y = np.zeros_like(t)
    for k in range(1, 7):
        y += (bright ** (k - 1) / k) * np.sin(2 * np.pi * f * k * t + k * 0.7)
    return y * _env(dur, attack, None, min(0.6, dur * 0.4))


@lru_cache(maxsize=None)
def string_note(m, dur):
    f, t = _f(m), _t(dur)
    y = sum((0.75 ** (k - 1) / k) * np.sin(2 * np.pi * f * k * t) for k in range(1, 9))
    return y * _env(dur, 0.012, 0.35, 0.04)


@lru_cache(maxsize=None)
def sub(m, dur):
    f, t = _f(m), _t(dur)
    return (np.sin(2 * np.pi * f * t) + 0.15 * np.sin(4 * np.pi * f * t)) * _env(dur, 0.006, None, 0.06)


# ── drums (a few seeded variants each → no machine-gun) ─────────────────
def _noise(n, rng):
    return rng.standard_normal(n)


def make_kit(rng):
    kit = {}
    t = _t(0.5)
    for name, f0, f1, sweep, dec in (("boom", 46, 70, 22, 0.20), ("round", 52, 90, 30, 0.11),
                                     ("tight", 55, 140, 45, 0.08), ("taiko", 62, 40, 9, 0.45)):
        fr = f0 + f1 * np.exp(-t * sweep)
        y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / dec) * np.minimum(1, t / 0.002)
        if name == "taiko":
            y += 0.5 * _filt(_noise(len(t), rng), lo=60, hi=900) * np.exp(-t / 0.12)
        if name == "boom":
            y = _filt(y, hi=1800)
        kit[name] = [y]
    for name, maker in (("snare", lambda r: 0.8 * _filt(_noise(int(SR * .25), r), lo=900, hi=7000) * _env(.25, .001, .07)
                                   + 0.5 * np.sin(2 * np.pi * 190 * _t(.25)) * _env(.25, .001, .05)),
                        ("rim", lambda r: (np.sin(2 * np.pi * 1700 * _t(.06)) + 0.6 * np.sin(2 * np.pi * 460 * _t(.06)))
                                * _env(.06, .0005, .012) + 0.3 * _filt(_noise(int(SR * .06), r), lo=2000) * _env(.06, .0005, .006)),
                        ("clap", _clap),
                        ("hat", lambda r: _filt(_noise(int(SR * .07), r), lo=7000) * _env(.07, .0005, .018)),
                        ("shaker", lambda r: _filt(_noise(int(SR * .09), r), lo=4500, hi=12000) * _env(.09, .012, .03))):
        kit[name] = [maker(rng) for _ in range(3)]
    return kit


def _clap(rng):
    """Three quick noise bursts (hands not quite together) + a short room tail."""
    out = np.zeros(int(SR * 0.25))
    for i in range(3):
        burst = _filt(_noise(int(SR * 0.2), rng), lo=900, hi=6000) * _env(0.2, 0.001, 0.012 if i < 2 else 0.09)
        a = int(SR * 0.011 * i)
        n = min(len(out) - a, len(burst))
        out[a:a + n] += burst[:n]
    return out


def _hit(kit, name, i):
    v = kit[name]
    return v[i % len(v)]


# ── composition ─────────────────────────────────────────────────────────
def _grid(s):
    return {i: c for i, c in enumerate(s or "") if c != "."}


def _motif(rng, scale):
    """4–6 scale degrees + rhythm (16th steps) — the video's own little theme."""
    n = int(rng.integers(4, 7))
    degs = [0]
    for _ in range(n - 1):
        degs.append(int(np.clip(degs[-1] + rng.choice([-2, -1, 1, 1, 2, 3]), -2, 7)))
    steps = sorted(rng.choice(np.arange(0, 16, 2), size=n, replace=False).tolist())
    return list(zip(steps, degs))


def _deg_to_midi(tonic, scale, deg):
    o, i = divmod(deg, len(scale))
    return tonic + 12 * o + scale[i]


def compose_styled(video, key, mood, seed, style):
    st = STYLES[style]
    rng = np.random.default_rng(seed)
    kit = make_kit(rng)
    dur = video.duration
    n_total = int(SR * (dur + 3.0))
    buses = {b: np.zeros((n_total, 2)) for b in ("drums", "bass", "chords", "lead", "fx")}
    send = np.zeros((n_total, 2))                           # reverb send
    pump = np.ones(n_total)
    beat = 60.0 / video.bpm
    step = beat / 4
    bar = 4 * beat
    tonic = 48 + KEYS[key]
    scale = SCALE.get(mood, SCALE_MAJ)
    motif = _motif(rng, scale)
    progs = (MOODS[mood], MOODS_B[mood])
    secs = sections(video)

    def put(bus, t0, sig, gain, pan=0.0, rev=0.0):
        a = int(round(t0 * SR))
        if a >= n_total or a + len(sig) <= 0 or gain <= 0:
            return
        s0 = max(0, -a)
        a = max(0, a)
        b = min(n_total, a + len(sig) - s0)
        seg = sig[s0:s0 + (b - a)] * gain
        gl, gr = _pan(pan)
        buses[bus][a:b, 0] += seg * gl
        buses[bus][a:b, 1] += seg * gr
        if rev:
            send[a:b, 0] += seg * gl * rev
            send[a:b, 1] += seg * gr * rev

    def human(t, amt=0.004):
        return t + float(np.clip(rng.normal(0, amt), -2 * amt, 2 * amt))

    def vel(v, amt=0.08):
        return v * float(np.clip(1 + rng.normal(0, amt), 0.75, 1.2))

    swing_off = (st["swing"] - 0.5) * 2 * step
    chapters_seen = 0
    for si, (s_t, kind, idx) in enumerate(secs):
        e_t = secs[si + 1][0] if si + 1 < len(secs) else dur
        if kind == "chapter":
            chapters_seen += 1
        level = {"intro": 1, "dark": 0, "outro": 4}.get(kind, 2 if chapters_seen <= 1 else 3)
        prog = progs[((idx or 0) + seed) % 2] if kind == "chapter" else progs[0]
        n_steps = int(np.ceil((e_t - s_t) / step - 1e-6))
        for k in range(n_steps):
            s = k % 16
            b_in = k // 16
            tb = s_t + k * step + (swing_off if s % 2 else 0.0)
            if tb >= dur:
                break
            last_bar = s_t + (b_in + 1) * bar >= e_t - 1e-6 and (e_t - s_t) > 2 * bar
            fill_bar = (b_in % 8 == 7) or last_bar
            root, ivs = prog[0] if kind == "outro" else prog[b_in % 4]
            chord = _voicing(tonic, root, ivs, tonic + (-5 if level == 0 else 2), tonic + (9 if level == 0 else 16))
            bm = tonic - 12 + root
            while bm > tonic - 5:
                bm -= 12
            outro_tail = kind == "outro" and b_in >= 2

            # chords
            ch_hit = _grid(st["chord_rhythm"]).get(s)
            if level == 0 and s == 0:
                for m in chord:
                    put("chords", tb, saw_pad(m, bar + 0.6, 0.0, 0.5, 0.35), 0.05, -0.3 + 0.2 * (m % 3), 0.5)
            elif ch_hit and not outro_tail and level > 0:
                inst = st["chords"]
                for j, m in enumerate(chord):
                    if inst == "epiano":
                        ln = bar - s * step + 0.2 if ch_hit == "x" else 2 * step
                        put("chords", human(tb + j * 0.012), epiano(m, round(ln, 2)), vel(0.055 if ch_hit == "x" else 0.035),
                            -0.25 + 0.5 * j / max(1, len(chord) - 1), 0.4)
                    elif inst == "stab":
                        put("chords", human(tb), pluck(m + 12, 0.22), vel(0.05), -0.3 + 0.6 * j / max(1, len(chord) - 1), 0.3)
                    else:                                                   # softpad / widepad
                        wide = inst == "widepad"
                        for d, p in ((0.0025, -0.7), (-0.0025, 0.7)) if wide else ((0.0015, -0.3), (-0.0015, 0.3)):
                            put("chords", tb, saw_pad(m, bar + 0.4, d, 0.35 if wide else 0.15, 0.45), 0.03, p, 0.5)
            if kind == "outro" and k == 0:
                for m in chord + [chord[0] + 12]:
                    put("chords", tb, felt(m, 3.5), 0.06, 0.0, 0.6)

            # bass
            if level >= 2 or (level == 1 and style == "ambient") or (kind == "outro" and b_in < 2):
                bh = _grid(st["bass_rhythm"]).get(s)
                if bh and not (fill_bar and s >= 12 and style != "ambient"):
                    if st["bass"] == "pluck":
                        put("bass", human(tb, 0.002), pluck(bm, 0.3), vel(0.20), 0.0)
                    else:
                        ln = beat * (4 if style in ("ambient", "cinematic") else 1.5)
                        put("bass", human(tb, 0.002), sub(bm + (12 if style == "garage" and s == 10 else 0), round(ln, 2)),
                            vel(0.22), 0.0)
            elif level == 0 and s == 0:
                put("bass", tb, sub(bm, round(bar, 2)), 0.16, 0.0)

            # drums
            drums_on = level >= 2 or (level == 1 and style in ("lofi", "marimba")) or (kind == "outro" and b_in == 0)
            stop = fill_bar and s >= 12 and style in ("lofi", "garage")          # drop-out before the turn
            if drums_on and not stop:
                kh = _grid(st["kick"]).get(s)
                if kh and level >= 2:
                    name = {"lofi": "boom", "garage": "tight", "cinematic": "taiko"}.get(style, "round")
                    put("drums", human(tb, 0.002), _hit(kit, name, 0), vel(0.5), 0.0, 0.08 if style == "cinematic" else 0)
                    if st["pump"]:
                        a = int(round(tb * SR))
                        seg = pump[a:a + int(SR * 0.25)]
                        seg *= 1 - st["pump"] * np.exp(-np.arange(len(seg)) / (SR * 0.07))
                sh = _grid(st["snare"]).get(s)
                if sh and level >= 2:
                    name = "rim" if style == "lofi" else "clap" if style in ("marimba", "garage") else "snare"
                    put("drums", human(tb), _hit(kit, name, k), vel(0.32), 0.05, 0.25)
                hh = _grid(st["hat"]).get(s)
                if hh:
                    put("drums", human(tb, 0.006), _hit(kit, "hat", k), vel(0.16 if hh == "x" else 0.09, 0.15), 0.35)
                ph = _grid(st["perc"]).get(s)
                if ph and (level >= 2 or style == "marimba"):
                    name = "shaker" if style == "marimba" else "rim"
                    put("drums", human(tb, 0.006), _hit(kit, name, k), vel(0.13 if ph == "x" else 0.07, 0.15), -0.35)
                if fill_bar and style in ("marimba", "cinematic", "garage") and s >= 12 and level >= 2:
                    put("drums", human(tb), _hit(kit, "snare" if style != "cinematic" else "taiko", k),
                        0.10 + 0.05 * (s - 12), 0.1, 0.2)
            if st.get("taiko") and level >= 2 and s == 0 and b_in % 2 == 0:
                put("drums", tb, _hit(kit, "taiko", 0), 0.45, 0.0, 0.2)

            # ostinato / broken chords (style texture)
            if level >= 2 and st.get("ostinato") and _grid(st["ostinato"]).get(s) and not outro_tail:
                tones = _voicing(tonic, root, ivs, tonic + 12, tonic + 26)[:4]
                pat = (0, 2, 1, 3, 2, 1, 3, 0)[(s + (idx or 0)) % 8]
                m = tones[pat % len(tones)]
                if style == "cinematic":
                    m = bm + 12 + (7 if s % 4 == 2 else 0)
                    put("lead", human(tb, 0.002), string_note(m, step * 0.95), vel(0.07), -0.4 + 0.8 * (s % 2), 0.25)
                else:
                    put("lead", human(tb, 0.003), mallet(m, 0.35), vel(0.075 if s % 4 == 0 else 0.05), 0.2 - 0.4 * (s % 2), 0.2)
            if st.get("broken") and _grid(st["broken"]).get(s) and level >= 1 and not outro_tail:
                tones = _voicing(tonic, root, ivs, tonic + 7, tonic + 24)
                m = tones[(b_in + s // 6) % len(tones)]
                put("lead", human(tb, 0.008), felt(m, 2.0), vel(0.06), -0.2 + 0.4 * (s / 16), 0.5)

            # motif (the video's theme) — from the 2nd chapter on, and once in the outro
            if (level == 3 or (kind == "outro" and b_in == 0)) and b_in % 2 == 0:
                for ms, deg in motif:
                    if ms == s:
                        shift = 0 if kind == "outro" else ((idx or 0) % 3)
                        m = _deg_to_midi(tonic + 12, scale, deg + shift)
                        inst = {"felt": felt, "mallet": mallet, "pluck": pluck, "bell": bell}[st["lead"]]
                        put("lead", human(tb, 0.005), inst(m, 1.2 if st["lead"] in ("felt", "bell") else 0.45),
                            vel(0.075), 0.15, 0.45)
            if level == 0 and s == 0 and b_in % 2 == 0:
                put("lead", tb, bell(_deg_to_midi(tonic + 24, scale, int(rng.integers(0, 5))), 2.4), 0.05, 0.3, 0.6)

        # transition into the NEXT section (style-specific; not the same riser every time)
        if si + 1 < len(secs):
            nxt = secs[si + 1][0]
            tr = st["transition"]
            nroot, nivs = progs[0][0]
            target = _voicing(tonic, nroot, nivs, tonic + 2, tonic + 16)
            if tr == "reverse":
                for j, m in enumerate(target[:3]):
                    put("fx", nxt - 1.6, felt(m, 1.6)[::-1] * np.linspace(0, 1, int(SR * 1.6)) ** 2, 0.05, -0.4 + 0.4 * j, 0.5)
            elif tr == "gliss":
                notes = [_deg_to_midi(tonic + 12, scale, d) for d in range(0, 8)]
                for j, m in enumerate(notes):
                    put("fx", nxt - beat + j * beat / 8, mallet(m, 0.3), 0.035 + 0.006 * j, -0.5 + j / 7, 0.3)
            elif tr == "riser":
                ln = min(2 * beat, nxt)
                r = _filt(rng.standard_normal(int(SR * ln)), lo=1500, hi=9000) * np.linspace(0, 1, int(SR * ln)) ** 2.5
                put("fx", nxt - ln, r, 0.07, -0.15, 0.2)
                put("fx", nxt - ln, np.roll(r, 211), 0.07, 0.15, 0.2)
            elif tr == "taiko":
                hits = [nxt - beat * x for x in (2, 1.5, 1, 0.75, 0.5, 0.375, 0.25, 0.125)]
                for j, th in enumerate(hits):
                    put("fx", th, _hit(kit, "taiko", 0), 0.12 + 0.03 * j, 0.0, 0.2)
            if kind != "intro" or tr in ("taiko", "riser"):
                t_i = _t(1.2)
                imp = np.sin(2 * np.pi * 44 * t_i) * np.exp(-t_i / 0.4)
                put("fx", nxt, imp, 0.16 if tr in ("taiko", "riser") else 0.08, 0.0, 0.35)

    y = np.zeros((n_total, 2))
    for name, b in buses.items():
        y += b * pump[:, None] if name in ("chords", "bass") else b
    y += _reverb(send, st["room"], seed) * st["reverb"] * 2.2
    if style == "lofi":                                      # vinyl bed
        crk = np.zeros(n_total)
        pos = rng.integers(0, n_total, size=int(dur * 9))
        crk[pos] = rng.uniform(-1, 1, size=len(pos))
        crk = _filt(crk, lo=900, hi=6000) * 0.5 + _filt(rng.standard_normal(n_total), lo=300, hi=3000) * 0.004
        y += np.stack([crk, np.roll(crk, 37)], 1) * 0.6
    if st["lowpass"]:
        for ch in range(2):
            y[:, ch] = _filt(y[:, ch], hi=st["lowpass"])
    y = y[: int(SR * dur)]
    fade = int(SR * 0.04)
    y[:fade] *= np.linspace(0, 1, fade)[:, None]
    y = np.tanh(y * 1.25) / 1.25
    rms = np.sqrt(np.mean(y ** 2)) or 1.0
    y *= 0.16 / rms
    peak = np.max(np.abs(y)) or 1.0
    if peak > 0.95:
        y *= 0.95 / peak
    return y


def audition(dest, key="F"):
    """Write a 40 s demo per style (intro → 2 chapters → dark recap → outro) + the SFX kit strips (user runs)."""
    import pathlib
    from ..video import Video
    from .sfx import export_library, write_wav
    dest = pathlib.Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    moods = {"lofi": "warm", "marimba": "bright", "ambient": "dreamy", "garage": "tense", "cinematic": "tense"}
    for style, st in STYLES.items():
        bpm = sum(st["bpm"]) // 2
        v = Video(duration=40.0, bpm=bpm)
        for num, lab, a, b, dark in ((None, "INTRO", 0, 6, False), (0, "SATU", 6, 16, False), (1, "DUA", 16, 27, False),
                                     (None, "INTINYA", 27, 33, True), (None, "OUTRO", 33, 40, False)):
            v.chapter(num, lab, a, b, dark)
        y = compose_styled(v, key, moods[style], 1234, style)
        write_wav(dest / f"music_{style}.wav", y)
        print(f"✓ {dest}/music_{style}.wav  ({bpm} BPM · {moods[style]} · {st['desc']})")
    export_library(dest)
