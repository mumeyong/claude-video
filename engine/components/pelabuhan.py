"""Container-port components (first used in "kubernetes-bukan-jawaban").

crane · peti_kemas · paket · kurir
Metaphor: Kubernetes is a container port (crane = scheduler, yard = node, box = container); a one-app job is just one
parcel, and a courier on a motorbike (VM / serverless) carries it fine. Signature: the gantry crane's trolley slides,
the spreader drops, lifts, and sets its load down — snappy. Pure functions of their progress values and t.
"""
import math

from .. import tokens as tk
from ..ease import clamp

GREEN = tk.CHAPTER[1][0]            # signature: crane + containers
KRAFT = (0.80, 0.62, 0.40, 1)       # cardboard parcel
WHITE = (1, 1, 1, 1)


def _shade(col, k):
    return (col[0] * k, col[1] * k, col[2] * k, col[3])


# ── shipping container ─────────────────────────────────────────────────
def peti_kemas(c, x, y, w, h, color=None, label=None, alpha=1.0):
    """Shipping container (x, y, w, h), side view: corrugated panel, top/bottom rails, corner castings, label."""
    color = color or GREEN
    with c.group(alpha):
        c.fill_rrect(x, y, w, h, 4, color)
        rib = max(10, w / 18)
        k = x + rib
        while k < x + w - rib * 0.6:
            c.line(k, y + h * 0.12, k, y + h * 0.88, _shade(color, 0.82), max(2, rib * 0.28))
            k += rib
        c.fill_rrect(x, y, w, h * 0.09, 3, _shade(color, 0.72))
        c.fill_rrect(x, y + h * 0.91, w, h * 0.09, 3, _shade(color, 0.72))
        cs = max(6, h * 0.12)
        for cx_, cy_ in ((x, y), (x + w - cs, y), (x, y + h - cs), (x + w - cs, y + h - cs)):
            c.fill_rrect(cx_, cy_, cs, cs, 2, _shade(color, 0.55))
        if label:
            fs = max(17, h * 0.26)
            lw = c.measure(label, tk.F["mono_bold"], fs)[0] + fs
            c.fill_rrect(x + w / 2 - lw / 2, y + h / 2 - fs * 0.85, lw, fs * 1.6, 6, WHITE, 0.92)
            c.text(x + w / 2, y + h / 2 + fs * 0.36, label, tk.F["mono_bold"], fs, _shade(color, 0.6), 1, 0.06,
                   align="c")


def paket(c, cx, base_y, s, alpha=1.0, label=None):
    """Small cardboard parcel (width s) standing on base_y: kraft box, tape strip, optional label below."""
    h = s * 0.72
    x, y = cx - s / 2, base_y - h
    with c.group(alpha):
        c.fill_rrect(x, y, s, h, 4, KRAFT)
        c.fill_rrect(x, y, s, h * 0.18, 3, _shade(KRAFT, 0.86))
        c.fill_rrect(cx - s * 0.08, y, s * 0.16, h, 2, _shade(KRAFT, 1.12))
        if label:
            c.text(cx, base_y + 30, label, tk.F["mono_med"], 20, c.theme("ink2", "d_muted"), 1, 0.04, align="c")


# ── gantry crane ───────────────────────────────────────────────────────
def crane(c, x, base_y, w, h, t, trolley=0.5, hoist=0.0, load=None, color=None, lamp=0.0, alpha=1.0):
    """Gantry crane standing on base_y from x to x + w, beam h px above the ground (cantilevered 12% to the left).
    trolley 0..1 = trolley position along the beam (0 = cantilever tip, 1 = right leg); hoist 0..1 lowers the spreader
    from the beam to the ground. load(c, cx, y) draws what hangs under the spreader (cx centre, y = its top).
    lamp 0..1 lights the blinking warning lamp on top (night). Returns (spreader_cx, spreader_bottom_y)."""
    color = color or GREEN
    leg = max(16, w * 0.035)
    by = base_y - h
    bx0, bx1 = x - w * 0.12, x + w
    ink2 = c.theme("ink2", "d_muted")
    with c.group(alpha):
        for lx in (x, x + w - leg):                                    # legs + bracing + wheels
            c.fill_rrect(lx, by, leg, h, 4, color)
            c.circle(lx + leg / 2, base_y - 6, leg * 0.42, ink2)
        for k in range(3):
            y0 = by + h * (0.2 + 0.26 * k)
            c.line(x + leg, y0, x + w * 0.16, y0 + h * 0.13, _shade(color, 0.8), 4)
            c.line(x + w - leg, y0, x + w * 0.84, y0 + h * 0.13, _shade(color, 0.8), 4)
        c.fill_rrect(bx0, by - 30, bx1 - bx0, 34, 6, color)              # beam
        for k in range(1, 12):
            kx = bx0 + (bx1 - bx0) * k / 12
            c.line(kx, by - 26, kx + 14, by, _shade(color, 0.8), 3)
        c.fill_rrect(x + w * 0.62, by - 92, w * 0.2, 64, 8, c.theme("card", "d_card"))      # operator cab
        c.stroke_rrect(x + w * 0.62, by - 92, w * 0.2, 64, 8, _shade(color, 0.8), 3)
        c.fill_rrect(x + w * 0.65, by - 80, w * 0.14, 26, 4, c.theme("faint", "d_line"))
        if lamp > 0.01:
            on = 0.25 + 0.75 * (0.5 + 0.5 * math.cos(2 * math.pi * 1.2 * t)) ** 4
            c.circle(x + w * 0.72, by - 104, 16, tk.C["rec"], 0.2 * lamp * on)
            c.circle(x + w * 0.72, by - 104, 8, tk.C["rec"], lamp * on)
        tx = bx0 + 40 + (bx1 - bx0 - 80) * clamp(trolley)
        c.fill_rrect(tx - 34, by + 4, 68, 30, 6, ink2)                  # trolley
        top, bottom = by + 40, base_y - 40
        sy = top + (bottom - top) * clamp(hoist)
        for dx in (-18, 18):
            c.line(tx + dx, by + 34, tx + dx * 1.6, sy, ink2, 3)
        c.fill_rrect(tx - 70, sy, 140, 16, 5, _shade(color, 0.7))     # spreader
        if load is not None:
            load(c, tx, sy + 16)
    return tx, sy + 16


# ── courier motorbike ──────────────────────────────────────────────────
def kurir(c, x, base_y, s, t, ride=0.0, box=True, color=None, alpha=1.0, facing=1):
    """Courier on a motorbike, side view, length s, wheels on base_y, x = rear wheel. ride 0..1 spins the wheels
    (rolling) and bobs the rider a little. box = delivery box on the rack. facing 1 = to the right."""
    color = color or GREEN
    ink2 = c.theme("ink2", "d_ink")
    r = s * 0.17
    with c.group(alpha), c.at(0, 0, 1, origin=(x + s / 2, base_y)):        # at() saves the ctx for the flip
        if facing < 0:
            c.ctx.translate(x + s / 2, 0)
            c.ctx.scale(-1, 1)
            c.ctx.translate(-(x + s / 2), 0)
        rx, fx, wy = x + r, x + s - r, base_y - r
        bob = math.sin(t * 14) * 2 * ride
        spin = t * 10 * ride
        for wx in (rx, fx):
            c.circle(wx, wy, r, ink2)
            c.circle(wx, wy, r * 0.55, c.theme("card", "d_card"))
            for k in range(3):
                a = spin + k * math.pi / 3
                c.line(wx - math.cos(a) * r * 0.5, wy - math.sin(a) * r * 0.5, wx + math.cos(a) * r * 0.5,
                       wy + math.sin(a) * r * 0.5, ink2, 3)
        c.fill_rrect(rx, wy - r * 1.3, fx - rx - r * 0.2, r * 0.9, r * 0.4, color)            # body
        c.line(fx - r * 0.2, wy - r * 0.4, fx, wy, ink2, max(3, s * 0.02))                    # fork
        c.line(fx - r * 0.5, wy - r * 1.9, fx - r * 0.2, wy - r * 0.4, ink2, max(3, s * 0.02))
        c.line(fx - r * 0.8, wy - r * 1.95, fx - r * 0.25, wy - r * 1.95, ink2, max(3, s * 0.025))  # handlebar
        hx, hy = x + s * 0.48, wy - r * 1.4 + bob                     # rider (seat → hip)
        c.fill_rrect(hx - s * 0.06, hy - s * 0.32, s * 0.13, s * 0.3, s * 0.05, ink2)
        c.circle(hx + s * 0.02, hy - s * 0.4, s * 0.075, color)        # helmet
        c.line(hx + s * 0.04, hy - s * 0.25, fx - r * 0.6, wy - r * 1.95, ink2, max(3, s * 0.03))
        c.line(hx, hy, hx + s * 0.16, wy - r * 0.6, ink2, max(3, s * 0.035))
        if box:
            bw = s * 0.3
            c.fill_rrect(x + s * 0.02, hy - bw * 0.95, bw, bw * 0.9, 6, color)
            c.fill_rrect(x + s * 0.02, hy - bw * 0.95, bw, bw * 0.18, 6, _shade(color, 0.75))
