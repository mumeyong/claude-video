"""Water-main components (first used in "wifi-ep05-lemot-jam-8-malam", Bongkar WiFi Rumah EP 05).

rusun_air · rusun_geo · aliran
Metaphor: an apartment block (rusun) cut open. One riser pipe comes up from the street (= the ISP's shared bandwidth)
and every unit has a tap on it (= a home that is online). In the afternoon a few taps are open and the water runs
hard; at 20.00 every window lights up, every tap opens, and the water column in the riser thins toward the top —
the tap on the top floor (yours) only drips (peak hour, oversubscription).
Signature: the clock on the roof jumps 14.00 → 20.00, windows light one by one, taps open, the column thins.
Pure functions of their progress values and t (water shimmer + drips are deterministic) — frame = f(t).
Colors from tokens; shading via material (look="flat" | "paper" | "lit").
"""
from .. import tokens as tk
from ..ease import clamp, mix
from . import material as mat
from .craft import stroke_partial

TEAL = tk.CHAPTER[4][0]              # signature: water, lit windows, the clock
INK2 = tk.C["ink2"]
F = tk.F
FLOORS, UNITS = 5, 2


def rusun_geo(x, y, w, h):
    """Geometry of rusun_air drawn with the same box (no drawing): dict with f, roof, ground, street (pipe y),
    riser (x), top (riser top y), sign (clock box), units [dict(box, win, tap, nozzle, basin, floor, side, hf)]
    (unit i = floor * 2 + side, floor 0 = bottom, side 0 = left), route (street pipe → riser → top-right tap)."""
    f = w / 900
    bx, bw = x + 20 * f, w - 40 * f
    roof = y + 104 * f
    ground = y + h - 170 * f
    street = ground + 84 * f
    xr = x + w / 2
    fh = (ground - roof - 20 * f) / FLOORS
    units = []
    for k in range(FLOORS):
        top = ground - (k + 1) * fh
        for side in range(UNITS):
            if side == 0:
                ux, uw = bx + 18 * f, xr - 34 * f - (bx + 18 * f)
            else:
                ux = xr + 34 * f
                uw = bx + bw - 18 * f - ux
            uy, uh = top + 12 * f, fh - 24 * f
            ww = 150 * f
            win = (ux + 26 * f if side == 0 else ux + uw - 26 * f - ww, uy + 20 * f, ww, uh - 52 * f)
            tx = xr - 92 * f if side == 0 else xr + 92 * f
            ty = uy + 30 * f
            units.append(dict(box=(ux, uy, uw, uh), win=win, tap=(tx, ty), nozzle=(tx, ty + 22 * f),
                              basin=(tx - 42 * f, uy + uh - 30 * f, 84 * f, 24 * f), floor=k, side=side))
    top_y = units[-1]["tap"][1]
    for u in units:
        u["hf"] = (street - u["tap"][1]) / (street - top_y)
    you = units[-1]
    route = [(x - 90 * f, street), (xr, street), (xr, top_y), (you["tap"][0], top_y)]
    sign = (xr - 130 * f, y, 260 * f, 78 * f)
    return dict(f=f, roof=roof, ground=ground, street=street, riser=xr, top=top_y, units=units, route=route,
                sign=sign, body=(bx, roof, bw, ground - roof))


def pressure(hf, demand, cap=4.0, n=FLOORS * UNITS):
    """Water pressure 0..1 at height fraction hf of the riser when `demand` taps' worth are open. Below `cap` the
    pipe keeps up (barely any loss); above it the column thins toward the top."""
    over = clamp((demand - cap) / max(1e-6, n - cap))
    return clamp(1 - hf * (0.08 * demand / n + 0.9 * over))


def aliran(c, t, pts, width, color=None, alpha=1.0, speed=0.35, n=5, dash=0.1):
    """Water running along polyline pts: a band of `width` with lighter shimmer dashes travelling start → end
    (deterministic in t; color-only on top of the band, so a still pipe reads as still)."""
    color = color or TEAL
    if width <= 0.3 or alpha <= 0.002:
        return
    stroke_partial(c, pts, 1.0, color, width, alpha)
    for k in range(n):
        u = (t * speed + k / n) % 1.0
        stroke_partial(c, pts, min(1.0, u + dash), mat.tone(color, 0.45), width * 0.34, alpha * 0.9, p0=u)


def rusun_air(c, x, y, w, h, t, taps=None, lights=None, night=0.0, supply=1.0, cap=4.0, clock="14.00",
              clock_b=None, clock_p=0.0, look="flat", color=None, alpha=1.0):
    """Apartment block cut open, box (x, y, w, h) (≈ 900 × 1050 at f = 1): roof clock, 5 floors × 2 units, one riser
    pipe up the middle fed from the street pipe (enters from the left, may bleed off-frame).
    taps: 10 values 0..1 (tap i open) · lights: 10 values 0..1 (window i lit) · night 0..1 (unlit glass goes dark) ·
    supply 0..1 (water in the street pipe) · cap = taps the pipe can feed at full pressure · clock / clock_b /
    clock_p: the roof clock cross-fades clock → clock_b. Each tap's stream = tap × pressure at its height; under
    ~0.3 it breaks into drips."""
    if alpha <= 0.002:
        return
    color = color or TEAL
    g = rusun_geo(x, y, w, h)
    f = g["f"]
    n = FLOORS * UNITS
    taps = list(taps or [0.0] * n)
    lights = list(lights or [0.0] * n)
    demand = sum(taps)
    wall = mat.tone(INK2, 0.86)
    slab = mat.tone(INK2, 0.62)
    pipe = mat.tone(INK2, 0.45)
    metal = mat.tone(INK2, 0.15)
    glass_day = mat.tone(color, 0.8)
    glass_off = mix(glass_day, mat.tone(INK2, -0.3), clamp(night))
    lit = mat.tone(color, 0.55)
    with c.group(alpha):
        # street + building
        gy = g["ground"]
        mat.body(c, look, mat.rrect_path(x - 120 * f, gy, w + 240 * f, y + h - gy, 0), (x - 120 * f, gy, w + 240 * f,
                 y + h - gy), mat.tone(INK2, 0.74), shadow=False)
        bx, by, bw, bh = g["body"]
        mat.body(c, look, mat.rrect_path(bx, by, bw, bh, 10 * f), g["body"], wall, r=10 * f)
        c.fill_rrect(bx - 10 * f, by - 14 * f, bw + 20 * f, 18 * f, 6 * f, slab)
        # roof clock
        sx, sy, sw, sh = g["sign"]
        c.line(sx + 40 * f, sy + sh, sx + 40 * f, by - 14 * f, slab, 6 * f)
        c.line(sx + sw - 40 * f, sy + sh, sx + sw - 40 * f, by - 14 * f, slab, 6 * f)
        c.fill_rrect(sx, sy, sw, sh, 14 * f, mat.tone(INK2, -0.55))
        pb = clamp(clock_p) if clock_b else 0.0
        if pb < 1:
            c.text(sx + sw / 2, sy + 56 * f, clock, F["mono_bold"], 46 * f, lit, 1 - pb, 0.04, align="c")
        if pb > 0:
            c.text(sx + sw / 2, sy + 56 * f, clock_b, F["mono_bold"], 46 * f, lit, pb, 0.04, align="c")
        # units
        for i, u in enumerate(g["units"]):
            ux, uy, uw, uh = u["box"]
            c.fill_rrect(ux, uy, uw, uh, 8 * f, mat.tone(INK2, 0.92))
            mat.inset(c, look, mat.rrect_path(ux, uy, uw, uh, 8 * f), u["box"])
            wx, wy, ww, wh = u["win"]
            c.fill_rrect(wx, wy, ww, wh, 6 * f, mix(glass_off, lit, clamp(lights[i])))
            c.line(wx + ww / 2, wy, wx + ww / 2, wy + wh, wall, 4 * f)
            c.line(wx, wy + wh * 0.45, wx + ww, wy + wh * 0.45, wall, 4 * f)
            bxx, byy, bww, bhh = u["basin"]
            c.fill_rrect(bxx, byy, bww, bhh, 8 * f, slab)
        for k in range(1, FLOORS):
            yy = gy - k * (gy - g["roof"] - 20 * f) / FLOORS
            c.line(bx, yy, bx + bw, yy, slab, 5 * f)
        # pipes: street → riser, a spout per tap
        xr, st, top = g["riser"], g["street"], g["top"]
        for u in g["units"]:
            tx, ty = u["tap"]
            mat.cable(c, look, [(xr, ty), (tx, ty)], 16 * f, pipe, shadow=False)
        mat.cable(c, look, [(x - 160 * f, st), (xr, st), (xr, top - 12 * f)], 46 * f, pipe)
        # water: street band, then a riser column that thins with height
        wmax = 28 * f
        aliran(c, t, [(x - 160 * f, st), (xr - wmax / 2, st)], wmax * clamp(supply), color, speed=0.28)
        steps = 28
        left, right = [], []
        for s in range(steps + 1):
            hf = s / steps
            yy = st - (st - top) * hf
            half = wmax / 2 * clamp(supply) * pressure(hf, demand, cap, n)
            left.append((xr - half, yy))
            right.append((xr + half, yy))
        if supply > 0.01:
            ctx = c.ctx
            ctx.move_to(*left[0])
            for p in left[1:] + right[::-1]:
                ctx.line_to(*p)
            ctx.close_path()
            c.src(color)
            ctx.fill()
            for k in range(4):
                u0 = (t * 0.32 + k / 4) % 1.0
                yy = st - (st - top) * u0
                half = wmax / 2 * clamp(supply) * pressure(u0, demand, cap, n) * 0.34
                if half > 0.6:
                    c.line(xr, yy, xr, max(top, yy - 26 * f), mat.tone(color, 0.45), 2 * half)
        # taps, streams, drips
        for i, u in enumerate(g["units"]):
            tx, ty = u["tap"]
            nx, ny = u["nozzle"]
            p = clamp(taps[i])
            c.fill_rrect(tx - 14 * f, ty - 14 * f, 28 * f, 36 * f, 8 * f, metal)
            hx = 22 * f * (1 if u["side"] else -1)
            c.line(tx, ty - 14 * f, tx + hx * (0.4 + 0.6 * p), ty - 24 * f - 6 * f * p, metal, 6 * f)
            if p <= 0.01:
                continue
            s = p * clamp(supply) * pressure(u["hf"], demand, cap, n)
            fall = u["basin"][1] - ny
            drip = clamp((0.3 - s) / 0.12)
            sw_ = 16 * f * s * (1 - drip)
            if sw_ > 0.4:
                c.fill_rrect(nx - sw_ / 2, ny, sw_, fall * clamp(p * 3), sw_ / 2, color)
            if drip > 0.01 and s > 0.004:
                for j in range(2):
                    q = (t * 1.15 + i * 0.37 + j * 0.5) % 1.0
                    c.circle(nx, ny + 4 * f + q * (fall - 8 * f), 6 * f * (0.8 + 0.3 * q), color,
                             drip * (1 - 0.35 * q))
