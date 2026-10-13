"""Easing + timing math. Everything here is a pure function of time."""
import math


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    """Lerp two RGBA tuples."""
    return tuple(lerp(a, b, t) for a, b in zip(c1, c2))


def prog(t, start, dur):
    """0→1 linear progress of t through [start, start+dur]."""
    if dur <= 0:
        return 1.0 if t >= start else 0.0
    return clamp((t - start) / dur)


def linear(p): return p
def out_cubic(p): return 1 - (1 - p) ** 3
def out_quart(p): return 1 - (1 - p) ** 4
def out_quint(p): return 1 - (1 - p) ** 5
def in_cubic(p): return p ** 3
def in_out_cubic(p): return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2
def in_out_sine(p): return -(math.cos(math.pi * p) - 1) / 2


def out_expo(p):
    return 1.0 if p >= 1 else 1 - 2 ** (-10 * p)


def out_back(p, s=1.5):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def spring(p, damping=0.55, freq=2.2):
    """Underdamped spring 0→1 (overshoots once, settles). p is 0..1 of the window.
    Starts at rest (zero velocity — the sin term), so there is no first-frame jolt (2026-10-13, refs.pdf §08)."""
    if p <= 0: return 0.0
    if p >= 1: return 1.0
    w = 2 * math.pi * freq
    wd = w * math.sqrt(1 - damping ** 2)
    return 1 - math.exp(-damping * w * p) * (math.cos(wd * p) + damping * w / wd * math.sin(wd * p))


# Window springs (2026-10-13, refs.pdf §08 "make motion feel expensive"): drop-in replacements for out_expo /
# out_back on p = prog(t, t0, dur) — same window, about the same speed, but they start AT REST. out_expo / out_back
# jump to full speed on the first frame, which reads as a pop / jitter on every entrance. Default for all motion.
def glide(p):
    """Critically damped spring over the window: accelerates for ~10 %, then a long glide to rest. Replaces out_expo."""
    if p <= 0: return 0.0
    if p >= 1: return 1.0
    w = 10.0     # residual at p = 1 is 0.05 % — no visible snap
    return 1 - math.exp(-w * p) * (1 + w * p)


_POP = {}


def pop(p, s=1.5):
    """Underdamped spring over the window with the SAME overshoot as out_back(p, s) (s 1.5 ≈ 8 %, 1.8 ≈ 11 %), but it
    starts at rest and is settled by p = 1. Replaces out_back."""
    if s not in _POP:
        os_ = max(1e-4, 4 * s ** 3 / (27 * (s + 1) ** 2))       # out_back's peak overshoot
        ln = math.log(os_)
        z = -ln / math.sqrt(math.pi ** 2 + ln ** 2)              # damping ratio with that overshoot
        _POP[s] = (z, 6.5 / (2 * math.pi * z))                   # freq: envelope < 0.3 % at p = 1
    z, f = _POP[s]
    return spring(p, damping=z, freq=f)


def out_spring(p):
    """Gentle settle 0→1: one small overshoot (~6%), then rest. For small pops and camera stops (opt-in, fx.py)."""
    return spring(p, damping=0.72, freq=1.3)


_BEZ = {}


def bezier(x1, y1, x2, y2):
    """CSS cubic-bezier(x1, y1, x2, y2) as an easing function p → value (Newton + bisection on x). Cached.
    Apple's curves live in tk.EASE — use curve("apple_out") etc. instead of raw numbers in scenes."""
    key = (x1, y1, x2, y2)
    if key in _BEZ:
        return _BEZ[key]

    def bx(s): return 3 * x1 * s * (1 - s) ** 2 + 3 * x2 * s * s * (1 - s) + s ** 3
    def by(s): return 3 * y1 * s * (1 - s) ** 2 + 3 * y2 * s * s * (1 - s) + s ** 3
    def dx(s): return 3 * x1 * (1 - s) ** 2 + 6 * (x2 - x1) * s * (1 - s) + 3 * (1 - x2) * s * s

    def fn(p):
        if p <= 0: return 0.0
        if p >= 1: return 1.0
        s = p
        for _ in range(8):
            d = dx(s)
            if abs(d) < 1e-6:
                break
            s2 = s - (bx(s) - p) / d
            if not 0 <= s2 <= 1:
                break
            s = s2
        if abs(bx(s) - p) > 1e-5:   # Newton wandered: bisection fallback
            lo, hi = 0.0, 1.0
            for _ in range(40):
                s = (lo + hi) / 2
                lo, hi = (s, hi) if bx(s) < p else (lo, s)
        return by(s)
    _BEZ[key] = fn
    return fn


def curve(name):
    """Named easing from tk.EASE: 'apple' · 'apple_out' · 'apple_in' · 'apple_in_out' · 'apple_dolly'."""
    from .tokens import EASE
    return bezier(*EASE[name])


def lerp_scale(s0, s1, p):
    """Perceptual scale interpolation (Remotion 'perceptual-scale'): lerp in log space, so a 2.4 → 1 shrink
    doesn't feel like it brakes early. Use for big scale moves (full-bleed shrink, push)."""
    if s0 <= 0 or s1 <= 0:
        return lerp(s0, s1, p)
    return s0 * (s1 / s0) ** p


def nudge(p):
    """Slow–fast–slow reposition (HyperFrames 'nudge-curve'): power3.in over 20 % of the time (10 % of the
    distance) → linear burst 18 % (65 %) → power4.out tail 62 % (25 %). For sliding a composed group aside."""
    p = clamp(p)
    if p < 0.20:
        return 0.10 * (p / 0.20) ** 3
    if p < 0.38:
        return 0.10 + 0.65 * (p - 0.20) / 0.18
    return 0.75 + 0.25 * (1 - (1 - (p - 0.38) / 0.62) ** 4)


def keys(t, frames, eases=None):
    """Multi-keyframe value: frames = [(t0, v0), (t1, v1), …], clamped on both sides; eases = one fn per segment
    (default apple_in_out). Values may be numbers or tuples. Stops dead at every key — for 2+ targets use track()."""
    if t <= frames[0][0]:
        return frames[0][1]
    for i in range(len(frames) - 1):
        (a, va), (b, vb) = frames[i], frames[i + 1]
        if t < b:
            fn = (eases[i] if eases else None) or curve("apple_in_out")
            k = fn(clamp((t - a) / max(1e-6, b - a)))
            if isinstance(va, (tuple, list)):
                return tuple(lerp(x, y, k) for x, y in zip(va, vb))
            return lerp(va, vb, k)
    return frames[-1][1]


def ios_spring(dt, response=0.5, damping=1.0):
    """SwiftUI-style spring by real time: value 0→1 `dt` seconds after the move starts.
    response = period of the undamped spring (s) · damping = dampingFraction (1 = critically damped, no overshoot;
    0.85 = iOS .snappy, ~1% overshoot; 0.7 = .bouncy). Starts with zero velocity, so it never 'jumps'."""
    if dt <= 0:
        return 0.0
    w0 = 2 * math.pi / max(1e-3, response)
    z = damping
    if z >= 1:   # critically damped (the iOS default feel: fast, then glides to rest)
        return 1 - math.exp(-w0 * dt) * (1 + w0 * dt)
    wd = w0 * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w0 * dt) * (math.cos(wd * dt) + z * w0 / wd * math.sin(wd * dt))


def ios_settle(response=0.5, damping=1.0, eps=0.002):
    """Seconds until an ios_spring stays within eps of 1 (its visual duration)."""
    t, step, last_out = 0.0, 1 / 240, 0.0
    while t < 6 * response + 2:
        t += step
        if abs(1 - ios_spring(t, response, damping)) > eps:
            last_out = t
    return last_out + step


# ── retargeting springs (2026-10-13, refs.pdf §08 track()) ─────────────────────────────
def _preset(spec):
    """tk.IOS name or a (response, dampingFraction) tuple."""
    if isinstance(spec, str):
        from .tokens import IOS
        return IOS[spec]
    return spec


def track(t, frames, preset="smooth"):
    """Value at t of something that changes target several times: frames = [(t0, v0), (t1, v1), …] sorted by time.
    One spring per change, summed — a new target mid-move bends the motion instead of stopping and restarting it,
    and frame 812 is still computed without simulating 0–811. Values may be numbers or tuples (x, y) / RGBA.
    preset = tk.IOS name ('smooth' cards/camera · 'snappy' UI/leading edges · 'hero' big type/lockups ·
    'bouncy' small stickers) or (response, damping). Use this instead of keys() for anything with 2+ targets."""
    resp, z = _preset(preset)
    v0 = frames[0][1]
    if isinstance(v0, (tuple, list)):
        v = list(v0)
        for (_, a), (tc, b) in zip(frames, frames[1:]):
            s = ios_spring(t - tc, resp, z)
            for j in range(len(v)):
                v[j] += (b[j] - a[j]) * s
        return tuple(v)
    v = v0
    for (_, a), (tc, b) in zip(frames, frames[1:]):
        v += (b - a) * ios_spring(t - tc, resp, z)
    return v


def track_settle(frames, preset="smooth"):
    """Time the last spring of a track() is visually at rest — budget the next hold from here."""
    return frames[-1][0] + ios_settle(*_preset(preset))


def indicator(t, stops, width, lead="lead", trail="trail"):
    """A tab / highlight that stretches while it travels: the leading edge is stiffer than the trailing one.
    stops = [(t0, x0), (t1, x1), …] (left edge). Returns (left, right)."""
    a, b = track(t, stops, lead), track(t, stops, trail)
    return min(a, b), max(a, b) + width


def swap_alpha(t, t_in, t_out=None):
    """Text inside a morphing box: fades in just after the morph starts (t_in), out just before the next (t_out)."""
    a = clamp((t - t_in - 0.08) / 0.12)
    return a if t_out is None else min(a, clamp((t_out - 0.1 - t) / 0.1))


def ease(t, start, dur, fn=glide):
    return fn(prog(t, start, dur))


def inout(t, t_in, t_out, d_in=0.55, d_out=0.35, fn_in=glide, fn_out=in_cubic):
    """Presence of an element that enters at t_in and leaves at t_out.

    Returns (a, b): a = eased entry progress 0→1, b = eased exit progress 0→1.
    Visible amount = a * (1 - b).  t_out=None means it never leaves.
    """
    a = fn_in(prog(t, t_in, d_in))
    b = 0.0 if t_out is None else fn_out(prog(t, t_out, d_out))
    return a, b


def pulse(t, start, dur):
    """0→1→0 bump over the window (sin)."""
    p = prog(t, start, dur)
    return math.sin(math.pi * p) if 0 < p < 1 else 0.0


def blink(t, hz=1.0):
    """Caret blink: 1 for the first half of each period."""
    return 1.0 if (t * hz) % 1.0 < 0.5 else 0.0
