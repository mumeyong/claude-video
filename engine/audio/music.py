"""Procedural score — a music bed composed from the video's own structure (numpy, 48 kHz mono, deterministic).

Used automatically by the mix when videos/<slug>/audio/music.* is missing. It is not a loop: the arrangement follows
the chapters — INTRO light groove, numbered chapters full groove (each chapter its own arp pattern), dark RECAP drums
out + darker pad + bells, OUTRO resolves on the tonic. Every section change lands on the beat nearest the chapter
start, with a riser into it and a soft impact on it. Tempo = video.bpm (HUD shows the same number).

Per-video character (key, mood, seed) is seeded from the slug, or set it in scenes.py:
    v.music = dict(key="D", mood="tense")   # moods: warm · tense · bright · dreamy
    v.music = dict(style="lofi", key="F", mood="warm")   # styled score (audio/score.py): lofi · marimba ·
                                            # ambient · garage · cinematic — own band, groove, tempo range, motif
    v.music = False                         # no generated music
No style = "pulse": the original sine-pad / four-on-the-floor score below (finished videos keep it).
Drop a real track at audio/music.(wav|mp3) and it wins over the generator.
"""
import zlib

import numpy as np

SR = 48000

KEYS = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7,
        "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
KEY_ORDER = ["A", "D", "F", "C", "E", "G", "Bb", "Eb"]

# one chord per bar, 4-bar cycle: (root offset from tonic, chord intervals)
MOODS = {
    "warm":   [(0, (0, 4, 7, 11)), (9, (0, 3, 7, 10)), (5, (0, 4, 7, 11)), (7, (0, 4, 7, 9))],     # Imaj7 vi7 IVmaj7 V6
    "tense":  [(0, (0, 3, 7, 14)), (8, (0, 4, 7, 11)), (3, (0, 4, 7, 14)), (10, (0, 4, 7, 9))],    # i(add9) VImaj7 III VII6
    "bright": [(5, (0, 4, 7, 11)), (7, (0, 4, 7, 10)), (4, (0, 3, 7, 10)), (9, (0, 3, 7, 10))],    # IVmaj7 V7 iii7 vi7
    "dreamy": [(0, (0, 4, 7, 11, 14)), (5, (0, 4, 7, 11, 14)), (9, (0, 3, 7, 10, 14)), (5, (0, 4, 7, 9, 14))],
}
ARPS = [(0, 1, 2, 3), (0, 2, 1, 3), (3, 2, 1, 0), (0, 2, 3, 1), (1, 3, 0, 2)]


def _f(m):
    return 440.0 * 2 ** ((m - 69) / 12)


STYLE_NAMES = ("pulse", "lofi", "marimba", "ambient", "garage", "cinematic")


def style_of(video):
    conf = getattr(video, "music", None)
    return conf.get("style", "pulse") if isinstance(conf, dict) else "pulse"


def config(video, slug):
    """(key name, mood, seed) or None when the video opts out."""
    conf = getattr(video, "music", None)
    if conf is False:
        return None
    conf = conf if isinstance(conf, dict) else {}
    seed = int(conf.get("seed", zlib.crc32(slug.encode()) % 10_000))
    key = conf.get("key", KEY_ORDER[seed % len(KEY_ORDER)])
    mood = conf.get("mood", list(MOODS)[(seed // 7) % len(MOODS)])
    if key not in KEYS or mood not in MOODS:
        raise ValueError(f"music: unknown key {key!r} or mood {mood!r}")
    if style_of(video) not in STYLE_NAMES:
        raise ValueError(f"music: unknown style {style_of(video)!r}; known: {', '.join(STYLE_NAMES)}")
    return key, mood, seed


def sections(video):
    """[(t, kind, idx)] — kind: intro · chapter · dark · outro; t snapped to the nearest beat."""
    beat = 60.0 / video.bpm
    off = video.beat_offset
    out = []
    for ch in video.chapters:
        lab = ch.label.upper()
        if lab == "OUTRO":
            kind = "outro"
        elif ch.dark:
            kind = "dark"
        elif lab == "INTRO":
            kind = "intro"
        else:
            kind = "chapter"
        t = off + round((ch.start - off) / beat) * beat
        t = max(0.0, t)
        if out and kind == out[-1][1] and ch.num == out[-1][2]:
            continue
        if out and abs(t - out[-1][0]) < 1e-6:
            out[-1] = (t, kind, ch.num)
        else:
            out.append((t, kind, ch.num))
    if not out or out[0][0] > 0:
        out.insert(0, (0.0, "intro", None))
    return out


def plan(video, slug):
    """Text description of the generated score (for `check`)."""
    cfg = config(video, slug)
    if cfg is None:
        return ["music: off (v.music = False)"]
    key, mood, seed = cfg
    style = style_of(video)
    lines = [f"music: generated · {style} · {key} {mood} · {video.bpm} BPM · seed {seed}  (audio/music.* overrides)"]
    if style != "pulse":
        from .score import STYLES
        lo, hi = STYLES[style]["bpm"]
        if not lo <= video.bpm <= hi:
            lines.append(f"  ⚠ {style} wants {lo}–{hi} BPM — set Video(..., bpm=...) in that range")
    for t, kind, idx in sections(video):
        lines.append(f"    {t:7.2f}  {kind}{'' if idx is None else ' ' + str(idx)}")
    return lines


# ── voices ──────────────────────────────────────────────────────────────
def _tone(freq, dur, partials, attack=0.005, decay=None, release=0.05, detune=0.0, ph=0.0):
    n = max(1, int(SR * dur))
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k, a in partials:
        f = freq * k
        if f > SR * 0.45:
            continue
        y += a * np.sin(2 * np.pi * f * t + k * ph)
        if detune:
            y += 0.7 * a * np.sin(2 * np.pi * f * (1 + detune) * t + k * ph + 1.3)
    env = np.minimum(1.0, t / attack) if attack > 0 else np.ones(n)
    if decay:
        env = env * np.exp(-t / decay)
    r = int(SR * release)
    if 0 < r < n:
        env[-r:] *= np.linspace(1.0, 0.0, r)
    return y * env


def _kick():
    d = 0.32
    t = np.arange(int(SR * d)) / SR
    f = 52 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11) * np.minimum(1, t / 0.002)


def _put(buf, t0, sig, gain=1.0):
    a = int(round(t0 * SR))
    if a >= len(buf) or a + len(sig) <= 0:
        return
    s0 = max(0, -a)
    a = max(0, a)
    b = min(len(buf), a + len(sig) - s0)
    buf[a:b] += gain * sig[s0:s0 + (b - a)]


def _voicing(tonic_midi, root, ivs, lo, hi):
    """Chord notes folded into [lo, hi] (keeps the pad in one register → smooth voice leading)."""
    notes = []
    for iv in ivs:
        m = tonic_midi + root + iv
        while m < lo:
            m += 12
        while m > hi:
            m -= 12
        notes.append(m)
    return sorted(set(notes))


def compose(video, slug):
    """Float64 array, length = video.duration: mono for "pulse", (n, 2) stereo for styled scores."""
    cfg = config(video, slug)
    if cfg is None:
        return None
    key, mood, seed = cfg
    if style_of(video) != "pulse":
        from .score import compose_styled
        return compose_styled(video, key, mood, seed, style_of(video))
    rng = np.random.default_rng(seed)
    dur = video.duration
    n_total = int(SR * (dur + 2.0))
    pad, bass, drums, lead, fx = (np.zeros(n_total) for _ in range(5))
    pump = np.ones(n_total)
    beat = 60.0 / video.bpm
    bar = 4 * beat
    off = video.beat_offset
    tonic = 48 + KEYS[key]                     # C3..B3
    prog = MOODS[mood]
    secs = sections(video)
    noise = np.diff(np.diff(rng.standard_normal(int(SR * 2.5)), prepend=0), prepend=0) * 0.25

    def sec_at(t):
        cur = secs[0]
        for s in secs:
            if s[0] <= t + 1e-6:
                cur = s
        return cur

    def chord_at(n, kind):
        if kind == "outro":
            return prog[0]
        return prog[(n // 4) % 4]

    first = int(np.floor((0 - off) / beat))
    last = int(np.ceil((dur - off) / beat))
    for n in range(first, last + 1):
        tb = off + n * beat
        if tb < -1e-6 or tb >= dur:
            continue
        st, kind, idx = sec_at(tb)
        b = n % 4
        root, ivs = chord_at(n, kind)
        sec_start = abs(tb - st) < 1e-6
        # pad — on every bar, and re-struck when a section starts mid-bar
        if b == 0 or sec_start:
            length = (4 - b) * beat + 0.35
            dark = kind == "dark"
            notes = _voicing(tonic, root, ivs, tonic + (-5 if dark else 2), tonic + (9 if dark else 16))
            parts = ((1, 1.0), (2, 0.08)) if dark else ((1, 1.0), (2, 0.22), (3, 0.07))
            g = 0.055 if kind != "intro" else 0.05
            for m in notes:
                _put(pad, tb, _tone(_f(m), length, parts, attack=0.35 if dark else 0.18, release=0.4,
                                    detune=0.0018, ph=m * 0.37), g)
        # bass
        bm = tonic - 12 + root
        while bm > tonic - 5:
            bm -= 12
        if kind in ("intro", "chapter"):
            _put(bass, tb, _tone(_f(bm), beat * 0.92, ((1, 1.0), (2, 0.18)), attack=0.004, release=0.06),
                 0.20 if kind == "chapter" else 0.15)
        elif kind == "dark" and b == 0:
            _put(bass, tb, _tone(_f(bm), bar, ((1, 1.0),), attack=0.3, release=0.8), 0.17)
        elif kind == "outro" and b == 0 and tb < st + 2 * bar:
            _put(bass, tb, _tone(_f(bm), bar * 1.5, ((1, 1.0),), attack=0.05, release=1.2), 0.17)
        # drums
        if kind == "chapter" or (kind == "intro" and b in (0, 2)):
            _put(drums, tb, _kick(), 0.42)
            k = int(SR * 0.3)
            a = int(round(tb * SR))
            seg = pump[a:a + k]
            seg *= 1 - 0.38 * np.exp(-np.arange(len(seg)) / (SR * 0.06))
        if kind in ("intro", "chapter"):
            h0 = int(rng.integers(0, len(noise) - 3000))
            hat = noise[h0:h0 + int(SR * 0.045)] * np.exp(-np.arange(int(SR * 0.045)) / (SR * 0.012))
            _put(drums, tb + beat / 2, hat, 0.55 if kind == "chapter" else 0.35)
            if kind == "chapter" and b == 3:
                _put(drums, tb + beat * 0.75, hat, 0.25)
        # lead arp (8ths in chapters, quarters in intro, one slow bar in outro)
        tones = _voicing(tonic, root, ivs, tonic + 12, tonic + 26)
        if len(tones) >= 4:
            tones = tones[:4]
        pat = ARPS[((idx or 0) + seed) % len(ARPS)]
        steps = {"chapter": 2, "intro": 1}.get(kind, 0)
        if kind == "outro" and tb < st + bar:
            steps = 1
        for h in range(steps):
            step = n * steps + h
            m = tones[pat[step % 4] % len(tones)]
            vel = 0.085 if (step % 4 == 0) else 0.06
            _put(lead, tb + h * beat / steps,
                 _tone(_f(m), 0.42, ((1, 1.0), (2, 0.45), (3, 0.2), (4, 0.08)), attack=0.003, decay=0.16,
                       release=0.05), vel)
        if kind == "dark" and b == 0:
            _put(lead, tb, _tone(_f(tones[-1]), 2.2, ((1, 1.0), (2.76, 0.3), (5.4, 0.08)), attack=0.004,
                                 decay=0.7, release=0.3), 0.07)
        # transition: riser over the bar before a section start, soft impact on it
        if sec_start and st > 0.01:
            r_len = int(SR * min(bar, st))
            ramp = np.linspace(0, 1, r_len) ** 2.2
            r0 = int(rng.integers(0, len(noise) - r_len)) if len(noise) > r_len else 0
            riser = noise[r0:r0 + r_len] * ramp if len(noise) > r_len else np.zeros(r_len)
            sweep_f = np.linspace(_f(tonic + 12), _f(tonic + 36), r_len)
            riser = riser + 0.12 * np.sin(2 * np.pi * np.cumsum(sweep_f) / SR) * ramp
            _put(fx, st - r_len / SR, riser, 0.16 if kind != "dark" else 0.1)
            imp_len = 1.1
            t_i = np.arange(int(SR * imp_len)) / SR
            impact = np.sin(2 * np.pi * 46 * t_i) * np.exp(-t_i / 0.35) + noise[:len(t_i)] * np.exp(-t_i / 0.25) * 0.6
            _put(fx, st, impact, 0.28)

    y = (pad + bass) * pump + drums + lead + fx
    y = y[: int(SR * dur)]
    fade = int(SR * 0.04)
    y[:fade] *= np.linspace(0, 1, fade)
    y = np.tanh(y * 1.3) / 1.3
    rms = np.sqrt(np.mean(y ** 2)) or 1.0
    y *= 0.16 / rms
    peak = np.max(np.abs(y)) or 1.0
    if peak > 0.95:
        y *= 0.95 / peak
    return y


def write_music(video, slug, path):
    """Compose and write a WAV (user-side: part of the mix). Returns path, or None if music is off."""
    from .sfx import write_wav
    y = compose(video, slug)
    if y is None:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    write_wav(path, y)
    return path
