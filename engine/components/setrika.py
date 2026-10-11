"""Clothes-iron components (first used in "ai-butuh-listrik").

setrika · uap_panas · pembangkit
Metaphor: one data-center GPU draws about as much power as two household irons that are never unplugged. A data
center = a building full of tens of thousands of irons (a small town's worth of power); all of it turns into heat
that has to be carried away, so the building moves next to its "socket" — a power plant with water nearby.
Signature: the iron's indicator lamp clicks on → heat lines rise from the soleplate (drawn once, then still).
Pure functions of their progress values (frame = f(t)) — nothing idles, so holds stay still. Colors from tokens.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix

CORAL = tk.C["orange_pill"]          # signature: indicator lamp, heat lines, power bar
F = tk.F


def setrika(c, cx, base_y, s, lamp=0.0, color=None, alpha=1.0, cord=True, plate=True):
    """Household iron, side view, tip to the right, standing on base_y; width s (height ≈ 0.6 s).
    lamp 0..1 lights the indicator lamp (color change only — no glow). cord draws the cable out of the back.
    Returns the soleplate's top-centre (where heat lines start)."""
    if alpha <= 0.002:
        return (cx, base_y)
    color = color or CORAL
    lamp = clamp(lamp)
    x0, x1 = cx - s / 2, cx + s / 2
    shell = c.theme("card", "d_card")
    edge = c.theme("faint", "d_muted")
    ink2 = c.theme("ink2", "d_ink")
    steel = c.theme("muted", "d_muted")
    lw = max(2.0, s * 0.012)
    ctx = c.ctx
    with c.group(alpha):
        if cord:                                                     # cable out of the back, sagging to the floor
            ctx.new_path()
            ctx.move_to(x0 + s * 0.04, base_y - s * 0.2)
            ctx.curve_to(x0 - s * 0.16, base_y - s * 0.16, x0 - s * 0.12, base_y - s * 0.02, x0 - s * 0.3,
                         base_y - s * 0.01)
            c.src(ink2, 0.8)
            ctx.set_line_width(max(3.0, s * 0.018))
            ctx.stroke()
        c.shadow(x0, base_y - s * 0.32, s, s * 0.32, s * 0.08, s * 0.06, s * 0.02, 0.09)
        ph = s * 0.065                                               # soleplate: flat, pointed tip on the right
        if plate:
            ctx.new_path()
            ctx.move_to(x0 + s * 0.02, base_y)
            ctx.line_to(x1 - s * 0.02, base_y)
            ctx.line_to(x1, base_y - ph * 0.6)
            ctx.line_to(x1 - s * 0.06, base_y - ph)
            ctx.line_to(x0, base_y - ph)
            ctx.close_path()
            c.src(steel)
            ctx.fill()
        ctx.new_path()                                               # shell: tall at the back, sweeping to the tip
        ctx.move_to(x0 + s * 0.01, base_y - ph)
        ctx.line_to(x0 + s * 0.03, base_y - s * 0.3)
        ctx.curve_to(x0 + s * 0.3, base_y - s * 0.36, x1 - s * 0.24, base_y - s * 0.3, x1 - s * 0.04, base_y - ph)
        ctx.close_path()
        c.src(shell)
        ctx.fill_preserve()
        c.src(edge)
        ctx.set_line_width(lw)
        ctx.stroke()
        c.line(x0 + s * 0.04, base_y - ph - s * 0.035, x1 - s * 0.12, base_y - ph - s * 0.035, color, lw * 2.2, 0.85)
        ctx.new_path()                                               # handle loop on top
        ctx.move_to(x0 + s * 0.1, base_y - s * 0.31)
        ctx.curve_to(x0 + s * 0.12, base_y - s * 0.6, x0 + s * 0.3, base_y - s * 0.6, x0 + s * 0.62, base_y - s * 0.56)
        ctx.curve_to(x0 + s * 0.72, base_y - s * 0.55, x0 + s * 0.74, base_y - s * 0.4, x0 + s * 0.7, base_y - s * 0.3)
        c.src(ink2)
        ctx.set_line_width(s * 0.07)
        ctx.set_line_cap(1)
        ctx.stroke()
        dx, dy = x0 + s * 0.45, base_y - s * 0.2                     # temperature dial
        c.circle(dx, dy, s * 0.05, edge)
        c.circle(dx, dy, s * 0.036, shell)
        c.line(dx, dy, dx + s * 0.03, dy - s * 0.022, ink2, lw * 1.4)
        lx, ly = x0 + s * 0.2, base_y - s * 0.19                     # indicator lamp
        c.circle(lx, ly, s * 0.034, edge)
        c.circle(lx, ly, s * 0.026, mix(c.theme("faint", "d_bg"), color, lamp))
    return (cx + s * 0.05, base_y - s * 0.34)


def uap_panas(c, cx, base_y, w, h, p, color=None, n=3, alpha=1.0, width=None, seed=0):
    """Heat lines rising from (cx, base_y): n wavy strokes across w, each drawn bottom → top as p goes 0 → 1
    (staggered), fading toward the top. Static once p = 1 — the signature move draws them once, then holds."""
    if alpha <= 0.002 or p <= 0:
        return
    color = color or CORAL
    width = width or max(3.0, w * 0.035)
    ctx = c.ctx
    steps = 28
    for i in range(n):
        f = 0.5 if n == 1 else i / (n - 1)
        x = cx - w / 2 + f * w
        hi = h * (0.86 + 0.14 * math.sin(seed * 1.7 + i * 2.3))
        pi = clamp(p * 1.35 - i * 0.12)
        if pi <= 0:
            continue
        amp = w * 0.07
        ph = seed * 0.9 + i * 1.3
        pts = [(x + amp * math.sin(ph + k / steps * 2 * math.pi * 1.25), base_y - hi * k / steps)
               for k in range(int(steps * pi) + 1)]
        ctx.set_line_cap(1)
        ctx.set_line_width(width)
        for k in range(len(pts) - 1):                               # per-segment alpha: fades out toward the top
            a = alpha * (1 - 0.85 * k / steps)
            c.line(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], color, width, a)


def pembangkit(c, x, base_y, w, h, steam=0.0, color=None, alpha=1.0, label="PEMBANGKIT LISTRIK"):
    """Power plant standing on base_y from x to x + w, height h: a curved cooling tower on the right, a turbine hall
    with a chimney on the left, a mono label under it. steam 0..1 puffs a cloud out of the tower (drawn, then still).
    Returns the socket point on the hall's left wall (where a cable plugs in)."""
    if alpha <= 0.002:
        return (x, base_y - h * 0.2)
    color = color or CORAL
    wall = c.theme("card", "d_card")
    edge = c.theme("faint", "d_muted")
    ink2 = c.theme("ink2", "d_ink")
    lw = max(2.0, w * 0.006)
    ctx = c.ctx
    with c.group(alpha):
        hx, hw, hh = x, w * 0.5, h * 0.42                            # turbine hall + chimney
        c.fill_rrect(hx + hw * 0.66, base_y - h * 0.82, hw * 0.12, h * 0.82, 4, wall)
        c.stroke_rrect(hx + hw * 0.66, base_y - h * 0.82, hw * 0.12, h * 0.82, 4, edge, lw)
        c.fill_rrect(hx + hw * 0.66, base_y - h * 0.78, hw * 0.12, h * 0.05, 2, color, 0.85)
        c.shadow(hx, base_y - hh, hw, hh, 10, 22, 8, 0.07)
        c.fill_rrect(hx, base_y - hh, hw, hh, 10, wall)
        c.stroke_rrect(hx, base_y - hh, hw, hh, 10, edge, lw)
        for k in range(4):                                           # hall windows
            c.fill_rrect(hx + hw * (0.1 + k * 0.21), base_y - hh * 0.62, hw * 0.13, hh * 0.3, 4,
                         c.theme("faint", "d_line"))
        tx0, tx1 = x + w * 0.56, x + w                               # hyperbolic cooling tower
        tw = tx1 - tx0
        top, waist = base_y - h, base_y - h * 0.35
        ctx.new_path()
        ctx.move_to(tx0, base_y)
        ctx.curve_to(tx0 + tw * 0.2, waist, tx0 + tw * 0.2, top + h * 0.15, tx0 + tw * 0.12, top)
        ctx.line_to(tx1 - tw * 0.12, top)
        ctx.curve_to(tx1 - tw * 0.2, top + h * 0.15, tx1 - tw * 0.2, waist, tx1, base_y)
        ctx.close_path()
        c.src(wall)
        ctx.fill_preserve()
        c.src(edge)
        ctx.set_line_width(lw)
        ctx.stroke()
        c.line(tx0 + tw * 0.1, base_y - h * 0.12, tx1 - tw * 0.1, base_y - h * 0.12, edge, lw)
        if steam > 0:                                                # steam cloud above the tower
            st = clamp(steam)
            puffs = [(tx0 + tw * fx, top - h * 0.05 + h * fy * st, tw * fr * (0.7 + 0.3 * st), clamp(st * 1.6 - k * 0.2))
                     for k, (fx, fy, fr) in enumerate(((0.5, 0.0, 0.2), (0.32, -0.1, 0.16), (0.66, -0.13, 0.17),
                                                       (0.48, -0.22, 0.15)))]
            for px, py, pr, a in puffs:                              # outline pass, then fill = one clean cloud
                c.circle(px, py, pr + lw * 1.5, edge, a)
            for px, py, pr, a in puffs:
                c.circle(px, py, pr, wall, a)
        if label:
            c.text(x + w / 2, base_y + 46, label, F["mono_med"], max(17.0, min(22.0, w * 0.05)), ink2, 1, 0.14,
                   align="c")
    return (hx, base_y - hh * 0.4)
