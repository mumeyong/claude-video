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
    """Underdamped spring 0→1 (overshoots once, settles). p is 0..1 of the window."""
    if p <= 0: return 0.0
    if p >= 1: return 1.0
    w = 2 * math.pi * freq
    return 1 - math.exp(-damping * w * p) * math.cos(w * math.sqrt(1 - damping ** 2) * p)


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


def ease(t, start, dur, fn=out_expo):
    return fn(prog(t, start, dur))


def inout(t, t_in, t_out, d_in=0.55, d_out=0.35, fn_in=out_expo, fn_out=in_cubic):
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
