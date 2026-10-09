"""Kinetic motion (opt-in, 2026-10-08): springs with personality, a persistent hero, mask / tracking text,
light-sweep swaps, lockups, parallax, slow drift. Studied from @davianmotion, translated to the light-glass brand.

Nothing here changes old videos — new videos pick their motion signature in PLAN.md and call these.

    hero = Rig(540, 980)                                   # ONE object that lives across scenes
    hero.to(T.line("L05").start, x=330, s=0.85, preset="heavy", anticip=0.05)
    with hero.place(c, t):                                 # draw the hero around (0, 0)
        phone(c, -150, -300, 300, 600, draw_screen=...)

    track_line(c, t, t_in, t_out, X, 900, "WHILE THEY", "display", 88, C["ink"])     # tracking collapses
    Headline("Muncul dari *balik* garis.").draw(c, t, t_in, t_out, reveal="mask", exit="dim")
    sheen(c, t, t_swap, (x, y, w, h), r=36)                # light band sweeps; swap content at its middle
    old, new = swap(t, t_swap)
    with parallax(c, v, t, 0.5): background(c, t)          # moves half as much as the camera
"""
import math
from contextlib import contextmanager

import cairo

from .. import tokens as tk
from ..ease import clamp, in_cubic, in_out_cubic, in_out_sine, lerp, mix, out_expo, prog, spring


# ── springs ─────────────────────────────────────────────────────────────
def spring_p(p, preset="snappy"):
    """Spring curve 0→1 (may overshoot) for p 0..1 of the preset's window. Presets: tk.SPRING."""
    d, f, _ = tk.SPRING[preset]
    return spring(p, d, f)


def spring_at(t, t0, preset="snappy", dur=None):
    """Spring progress at t for a move starting at t0 (0 before t0, settles to exactly 1)."""
    if t < t0:
        return 0.0
    return spring_p(prog(t, t0, dur or tk.SPRING[preset][2]), preset)


def anticipate(p, k=0.06, preset="snappy", wind=0.22):
    """Wind-up then spring: dips to −k during the first `wind` of the window, then springs to 1."""
    if p <= 0:
        return 0.0
    if p < wind:
        return -k * math.sin(math.pi / 2 * p / wind)
    return -k + (1 + k) * spring_p((p - wind) / (1 - wind), preset)


# ── persistent hero (shared element) ────────────────────────────────────
class Rig:
    """Position / scale / rotation / alpha of ONE object over the whole video. Instead of exiting and
    re-entering between scenes, the hero moves to its next spot (spring + optional wind-up) — scenes connect.

    State keys: x, y (design px of the object's origin), s (scale), rot (radians), a (alpha 0..1).
    """

    def __init__(self, x=tk.W / 2, y=tk.H / 2, s=1.0, rot=0.0, a=1.0):
        self.base = dict(x=x, y=y, s=s, rot=rot, a=a)
        self.keys = []  # (t, dur, preset, anticip, {changed keys})

    def to(self, t, dur=None, preset="snappy", anticip=0.0, **state):
        """From t, move the given keys to new values (others keep their value)."""
        bad = set(state) - set(self.base)
        if bad:
            raise KeyError(f"Rig keys are x, y, s, rot, a — not {sorted(bad)}")
        self.keys.append((float(t), dur or tk.SPRING[preset][2], preset, anticip, state))
        self.keys.sort(key=lambda k: k[0])
        return self

    def state(self, t):
        st = dict(self.base)
        for (kt, d, preset, k, change) in self.keys:
            if t < kt:
                break
            p = prog(t, kt, d)
            e = anticipate(p, k, preset) if k else spring_p(p, preset)
            ea = in_out_cubic(p)  # alpha never overshoots
            for key, val in change.items():
                st[key] = lerp(st[key], val, ea if key == "a" else e)
        st["a"] = clamp(st["a"])
        return st

    def speed(self, t, dt=1 / 120):
        """Screen speed (px/s) at t — feed motion_blur() for fast moves."""
        a, b = self.state(t - dt), self.state(t)
        return math.hypot(b["x"] - a["x"], b["y"] - a["y"]) / dt

    @contextmanager
    def place(self, c, t, bbox=None, blur_k=None):
        """Draw the hero around (0, 0) at its current state. bbox (around 0,0) enables speed blur."""
        st = self.state(t)
        bl = motion_blur(self.speed(t), blur_k) if bbox is not None else 0.0
        with c.at(st["x"], st["y"], st["s"], origin=(0, 0), rot=st["rot"]):
            if bbox is not None:
                with c.layer(bbox, st["a"], bl):
                    yield st
            else:
                with c.group(st["a"]):
                    yield st


def motion_blur(speed, k=None):
    """Blur (px) for something moving at `speed` px/s — 0 at rest, capped (tk.M['mblur_*'])."""
    k = tk.M["mblur_k"] if k is None else k
    return min(tk.M["mblur_max"], max(0.0, speed - 300) * k)


# ── always-alive camera on the hero ─────────────────────────────────────
def drift(t, t0, t1, zoom=None, rot=None, seed=0):
    """Slow continuous push over a whole scene: (scale, rot, dx, dy). Nothing ever sits perfectly still."""
    zoom = tk.M["drift_zoom"] if zoom is None else zoom
    rot = tk.M["drift_rot"] if rot is None else rot
    p = in_out_sine(prog(t, t0, max(0.01, t1 - t0)))
    ph = seed * 1.7
    return (1 + zoom * p, rot * (p - 0.5) * 2 + 0.002 * math.sin(t * 0.7 + ph),
            3 * math.sin(t * 0.45 + ph), 4 * math.sin(t * 0.33 + ph * 2))


@contextmanager
def drifting(c, t, t0, t1, origin, **kw):
    s, r, dx, dy = drift(t, t0, t1, **kw)
    with c.at(dx, dy, s, origin=origin, rot=r):
        yield c


@contextmanager
def parallax(c, v, t, depth):
    """Re-apply v.camera at a different depth for the body: 1 = normal, 0.5 = moves half (far), 1.4 = near."""
    z, fx, fy = v.camera.state(t)
    cx_ = c.ctx
    cx_.save()
    W2, H2 = tk.W / 2, tk.H / 2
    cx_.translate(fx, fy)          # undo the camera …
    cx_.scale(1 / z, 1 / z)
    cx_.translate(-W2, -H2)
    zk = 1 + (z - 1) * depth       # … and redo it at this depth
    cx_.translate(W2, H2)
    cx_.scale(zk, zk)
    cx_.translate(-(W2 + (fx - W2) * depth), -(H2 + (fy - H2) * depth))
    try:
        yield c
    finally:
        cx_.restore()


# ── text ────────────────────────────────────────────────────────────────
_WIDTHS = {}


def _prefix_widths(c, text, font, size, ls):
    key = (text, font, size, ls)
    if key not in _WIDTHS:
        _WIDTHS[key] = [c.measure(text[:i], font, size, ls)[0] if i else 0.0 for i in range(len(text) + 1)]
    return _WIDTHS[key]


def dim_color(c, color, b):
    """Exit tint: color drains toward muted over the first part of the exit (b 0..1)."""
    return mix(color, c.theme("muted", "d_muted"), clamp(b / 0.55))


def dim_alpha(b):
    return 1 - in_cubic(clamp((b - 0.35) / 0.65))


def track_line(c, t, t_in, t_out, x, y, text, font, size, color, ls=None, align="l", spread=None,
               flash=None, d_in=None, d_out=None):
    """One line of type whose letters arrive left→right while the extra tracking collapses to rest.
    Letters flash in `flash` color (default accent) and settle to `color`. Exit = dim (grey) then fade.
    font = tk.F key ('display', 'ui_bold', 'mono_bold' …). y = baseline. Returns the resting width."""
    M = tk.M
    f = tk.F[font]
    ls = (0.0 if text.isupper() else tk.T["headline"][1]) if ls is None else ls  # caps need air
    spread = M["track_spread"] if spread is None else spread
    d_in = d_in or M["track_in"]
    d_out = d_out or M["dim_out"]
    ws = _prefix_widths(c, text, f, size, ls)
    total = ws[-1]
    g = out_expo(prog(t, t_in, d_in))
    b = 0.0 if t_out is None else prog(t, t_out, d_out)
    if g <= 0 or b >= 1:
        return total
    extra = size * spread * (1 - g)
    n = len(text)
    span = total + extra * (n - 1)
    x0 = x if align == "l" else (x - span / 2 if align == "c" else x - span)
    flash = c.theme("accent", "d_accent") if flash is None else flash
    stg = d_in * 0.45 / max(1, n)
    bl = M["word_blur"] * 0.6 * (1 - g)
    with c.layer((x0 - 20, y - size * 1.1, span + 40, size * 1.5), dim_alpha(b), bl):
        for i, ch in enumerate(text):
            if ch == " ":
                continue
            a = out_expo(prog(t, t_in + i * stg, d_in * 0.5))
            if a <= 0.002:
                continue
            col = dim_color(c, mix(flash, color, clamp(a * 1.4 - 0.2)), b)
            c.text(x0 + ws[i] + extra * i, y, ch, f, size, col, a, ls)
    return total


def mask_word(c, t, t_in, t_out, x, base, word, font, size, color, ls=0.0, d_in=None, exit="mask"):
    """One word that rises from behind its own baseline mask (and leaves up through it, or dims)."""
    M = tk.M
    d_in = d_in or M["mask_in"]
    a = spring_at(t, t_in, "snappy", d_in)
    if t_out is None:
        b = 0.0
    else:
        b = (in_cubic if exit == "mask" else (lambda p: p))(prog(t, t_out, M["out"] if exit == "mask" else M["dim_out"]))
    if a <= 0.001 or b >= 1:
        return
    w = c.measure(word, font, size, ls)[0]
    dy = (1 - a) * size * 1.05
    alpha = 1.0
    if exit == "mask":
        dy -= b * size * 1.05
    else:
        color, alpha = dim_color(c, color, b), dim_alpha(b)
    with c.clip(x - 10, base - size * 1.02, w + 20, size * 1.30):
        c.text(x, base + dy, word, font, size, color, alpha, ls)


# ── content swaps ───────────────────────────────────────────────────────
def sheen(c, t, t0, bbox, r=None, dur=None, width=None, angle=0.35):
    """A soft light band sweeps across bbox (clipped to its rounded rect). Swap content at its middle
    (t0 + dur/2, see swap()). Light: white band · dark: pale blue. No glow outside the shape."""
    dur = dur or tk.M["sheen_dur"]
    p = prog(t, t0, dur)
    if p <= 0 or p >= 1:
        return
    x, y, w, h = bbox
    r = tk.L["radius_card"] if r is None else r
    width = width or max(120, w * 0.35)
    u = in_out_cubic(p)
    span = w + h * math.tan(angle) + 2 * width
    bx = x - width - h * math.tan(angle) + span * u
    col = c.theme("card", "d_accent")
    peak = 0.75 * math.sin(math.pi * p)
    cx_ = c.ctx
    with c.clip(x, y, w, h, r):
        cx_.save()
        cx_.translate(bx, y)
        cx_.transform(cairo.Matrix(1, 0, -math.tan(angle), 1, 0, 0))  # skew → diagonal band
        g = cairo.LinearGradient(-width / 2, 0, width / 2, 0)
        g.add_color_stop_rgba(0, *col[:3], 0)
        g.add_color_stop_rgba(0.5, *col[:3], peak)
        g.add_color_stop_rgba(1, *col[:3], 0)
        cx_.set_source(g)
        cx_.rectangle(-width / 2, 0, width, h)
        cx_.fill()
        cx_.restore()


def swap(t, t0, dur=None):
    """(old_alpha, new_alpha) for content swapped under a sheen starting at t0."""
    dur = dur or tk.M["sheen_dur"]
    k = in_out_cubic(prog(t, t0 + dur * 0.35, dur * 0.3))
    return 1 - k, k


# ── lockups ─────────────────────────────────────────────────────────────
def lockup(c, t, t_in, t_out, cx, base, left, right, sep="×", style="headline", colors=None, gap=None):
    """'A × B' lockup: the two words fly in from opposite edges on a heavy spring (speed-blurred), the
    separator settles in after them; exit = dim then fade. base = baseline. For collabs, versus, before/after."""
    size, ls, _ = tk.T[style]
    f = tk.F["display"]
    ink = c.theme("ink", "d_ink")
    cl, cr = colors or (ink, c.theme("accent", "d_accent"))
    gap = size * 0.4 if gap is None else gap
    wl, wr = c.measure(left, f, size, ls)[0], c.measure(right, f, size, ls)[0]
    ws = c.measure(sep, tk.F["ui"], size * 0.5)[0]
    # shrink to the safe column, then keep it inside (long word pairs / off-center cx)
    col_x, col_w = tk.L["col_x"], tk.L["col_w"]
    k = min(1.0, col_w / (wl + wr + ws + 2 * gap))
    if k < 1:
        size, gap = size * k, gap * k
        wl, wr = c.measure(left, f, size, ls)[0], c.measure(right, f, size, ls)[0]
        ws = c.measure(sep, tk.F["ui"], size * 0.5)[0]
    total = wl + wr + ws + 2 * gap
    cx = min(max(cx, col_x + total / 2), col_x + col_w - total / 2)
    x_l = cx - total / 2
    x_s, x_r = x_l + wl + gap, x_l + wl + gap + ws + gap
    b = 0.0 if t_out is None else prog(t, t_out, tk.M["dim_out"])
    if t < t_in or b >= 1:
        return
    dur = tk.SPRING["heavy"][2]
    for word, x, side, col, td in ((left, x_l, -1, cl, 0.0), (right, x_r, 1, cr, 0.08)):
        e = spring_at(t, t_in + td, "heavy")
        if e <= 0:
            continue
        off = side * (1 - e) * tk.W * 0.35
        vel = abs(spring_at(t, t_in + td, "heavy") - spring_at(t - 1 / 120, t_in + td, "heavy")) * 120 * tk.W * 0.35
        bl = motion_blur(vel)
        with c.layer((x + off - 30, base - size, c.measure(word, f, size, ls)[0] + 60, size * 1.4),
                     dim_alpha(b) * in_out_cubic(prog(t, t_in + td, dur * 0.4)), bl):
            c.text(x + off, base, word, f, size, dim_color(c, col, b), 1.0, ls)
    s = spring_at(t, t_in + dur * 0.45, "snappy")
    if s > 0:
        with c.at(0, 0, s, origin=(x_s + ws / 2, base - size * 0.18)):
            c.text(x_s, base - size * 0.02, sep, tk.F["ui"], size * 0.5, dim_color(c, c.theme("muted", "d_muted"), b),
                   dim_alpha(b))


def curtain(c, t, t0, dur=None, color=None, reverse=False):
    """Full-screen fade from (or, reverse=True, to) a color — cold opens out of darkness. Draw at z >= 100."""
    dur = dur or tk.M["curtain"]
    p = in_out_cubic(prog(t, t0, dur))
    a = p if reverse else 1 - p
    if a <= 0.002:
        return
    c.src(color or tk.C["d_bg"], a)
    c.ctx.rectangle(0, 0, tk.W, tk.H)
    c.ctx.fill()
