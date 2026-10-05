"""Shared motion recipes: how things enter, leave, and type."""
import math

from .. import tokens as tk
from ..ease import inout, out_expo, in_cubic, prog


def appear(c, t, t_in, t_out, bbox, draw, rise=None, scale=None, blur=None,
           d_in=None, d_out=None, pad=70):
    """Standard element entrance/exit: rise + scale-up + blur-in, blur-out + fade.

    bbox = (x, y, w, h) of the element (pad adds room for its shadow).
    draw(c) draws the element at rest.
    """
    M = tk.M
    rise = M["card_rise"] if rise is None else rise
    scale = M["card_scale"] if scale is None else scale
    blur = M["card_blur"] if blur is None else blur
    a, b = inout(t, t_in, t_out, d_in or M["card_in"], d_out or M["out"], out_expo, in_cubic)
    vis = a * (1 - b)
    if vis <= 0.002:
        return 0.0
    bl = blur * (1 - a) + M["out_blur"] * b
    dy = rise * (1 - a) - 18 * b
    sc = scale + (1 - scale) * a
    x, y, w, h = bbox
    with c.at(0, dy, sc, origin=(x + w / 2, y + h / 2)):
        with c.layer((x - pad, y - pad, w + 2 * pad, h + 2 * pad), vis, bl):
            draw(c)
    return vis


def fade(c, t, t_in, t_out, draw, d_in=0.4, d_out=0.3):
    """Plain opacity in/out (for small things: labels, tags)."""
    a, b = inout(t, t_in, t_out, d_in, d_out, out_expo, in_cubic)
    vis = a * (1 - b)
    if vis <= 0.002:
        return 0.0
    with c.group(vis):
        draw(c)
    return vis


def typed(text, t, t0, cps=None):
    """Typewriter state: (full_chars_text, partial_char, partial_alpha, done)."""
    cps = cps or tk.M["type_cps"]
    if t < t0:
        return "", "", 0.0, False
    n = (t - t0) * cps
    k = int(n)
    if k >= len(text):
        return text, "", 0.0, True
    return text[:k], text[k], n - k, False


def type_end(text, t0, cps=None):
    return t0 + len(text) / (cps or tk.M["type_cps"])


def type_cues(text, t0, cps=None, name="key", gain=0.5):
    """SFX cues for each typed character (spaces are skipped)."""
    cps = cps or tk.M["type_cps"]
    return [(name, t0 + i / cps, gain * (0.85 + 0.3 * ((i * 7919) % 13) / 13))
            for i, ch in enumerate(text) if not ch.isspace()]


def stagger(i, step=None):
    return i * (step if step is not None else tk.M["word_stagger"])


def count(t, t0, dur, v0, v1):
    """Eased count-up value."""
    return v0 + (v1 - v0) * out_expo(prog(t, t0, dur))


def fmt_id(v, decimals=0):
    """Indonesian number format: 2951 → '2.951', 44.4 → '44,4'."""
    s = f"{v:,.{decimals}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def bezier_point(p0, p1, p2, p3, u):
    a = (1 - u) ** 3; b = 3 * u * (1 - u) ** 2; cc = 3 * u * u * (1 - u); d = u ** 3
    return (a * p0[0] + b * p1[0] + cc * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + cc * p2[1] + d * p3[1])


def bezier_partial(c, p0, p1, p2, p3, p, steps=48):
    """Path of the first p (0..1) of a cubic bezier, as a polyline."""
    if p <= 0:
        return
    cx = c.ctx
    cx.new_path()
    cx.move_to(*p0)
    n = max(2, int(steps * p))
    for i in range(1, n + 1):
        cx.line_to(*bezier_point(p0, p1, p2, p3, p * i / n))


def wobble(t, seed=0, amp=1.0, hz=0.3):
    """Tiny deterministic idle float (use 2-4 px) so resting cards feel alive."""
    return amp * math.sin(t * hz * 2 * math.pi + seed * 1.7)
