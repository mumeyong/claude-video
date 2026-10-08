"""Physical-motion upgrades (opt-in, 2026-10-08): springs, landings, contact shadows, ghost trails.

Nothing here changes existing components — new videos call these explicitly.

    s = settle(t, t0)                                  # 0 → ~1.06 → 1 scale for a small pop
    with squash(c, cx, base_y, land(t, t_land)):       # squash-and-stretch after a drop
        kios(c, ...)
    contact_shadow(c, cx, base_y, w, lift=drop_px)     # soft ellipse under a grounded object
    ghost_trail(c, t, lambda c, tt: shuttle(c, *pos(tt)))   # fast mover without 60 fps strobing
"""
import math
from contextlib import contextmanager

import cairo

from .. import tokens as tk
from ..ease import clamp, out_spring, prog


def settle(t, t0, dur=None):
    """Spring progress 0 → ~1.06 → 1 starting at t0 (use as a scale for small pops, or as a camera ease)."""
    if t < t0:
        return 0.0
    return out_spring(prog(t, t0, dur or tk.M["settle"]))


def land(t, t_land, dur=None):
    """Squash amount after a landing at t_land: +1 = squashed flat … −0.4 = stretched rebound … 0 = rest."""
    dur = dur or tk.M["land_dur"]
    if t < t_land or t > t_land + dur:
        return 0.0
    u = (t - t_land) / dur
    return math.cos(u * math.pi * 1.5) * (1 - u) * (1 if u < 1 / 3 else 0.4)


@contextmanager
def squash(c, cx, base_y, amount):
    """Non-uniform scale anchored at the object's foot (cx, base_y): amount > 0 = wider & shorter."""
    k = tk.M["land_squash"] * amount
    cx_ = c.ctx
    cx_.save()
    if abs(k) > 1e-4:
        cx_.translate(cx, base_y)
        cx_.scale(1 + k, 1 - k)
        cx_.translate(-cx, -base_y)
    try:
        yield c
    finally:
        cx_.restore()


def contact_shadow(c, cx, base_y, w, lift=0.0, alpha=1.0):
    """Soft ellipse shadow on the floor under an object of width w; lift (px above the floor) shrinks + fades it."""
    f = clamp(1 - lift / max(1.0, w * 1.5))
    if f <= 0.02 or alpha <= 0.01:
        return
    rx, ry = w * 0.55 * (0.6 + 0.4 * f), w * 0.07 * (0.6 + 0.4 * f)
    cx_ = c.ctx
    cx_.save()
    cx_.translate(cx, base_y)
    cx_.scale(1, ry / rx)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, rx)
    a = 0.16 * f * alpha * (1 - 0.6 * c.dark)
    g.add_color_stop_rgba(0, 0, 0, 0, a)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cx_.set_source(g)
    cx_.arc(0, 0, rx, 0, 2 * math.pi)
    cx_.fill()
    cx_.restore()


def ghost_trail(c, t, draw_at, n=None, span=None, alpha=0.45):
    """Draw draw_at(c, tt) at t plus n fading ghosts reaching `span` seconds back (frame = f(t), so it's exact).
    Use only for small fast objects — each ghost is a full extra draw."""
    n = n or tk.M["trail_n"]
    span = span or tk.M["trail_span"]
    for k in range(n, 0, -1):
        with c.group(alpha * (1 - k / (n + 1))):
            draw_at(c, t - span * k / n)
    draw_at(c, t)
