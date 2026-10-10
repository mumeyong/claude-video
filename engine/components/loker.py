"""Locker-room components (first used in "foto-whatsapp-lewat-mana", reel look).

loker · loker_cell · kotak · kunci · centang · foto
Metaphor: a WhatsApp photo is locked into a box on your phone with a brand-new key, the box waits in the server's
left-luggage lockers (loker penitipan), and the key never goes to the locker — it travels inside the end-to-end chat
message. Signature: a locker door swinging on a heavy spring, swallowing or handing out the box.
Pure functions of their progress values and t (frame = f(t)); colors from tokens (reel palette).
"""
import math

import cairo

from .. import tokens as tk
from ..ease import clamp, mix

TERRA = tk.REEL_WORLDS[2]           # signature: boxes, lockers, the box route
PAPER, INK, GREEN = tk.C["brand_paper"], tk.C["reel_ink"], tk.C["reel_green"]
F = tk.F


def _shade(col, k):
    return (col[0] * k, col[1] * k, col[2] * k, col[3])


def _hash(*a):
    h = 2166136261
    for v in a:
        h = ((h ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return h


def _partial(c, pts, p):
    """Stroke the first p (0..1) of polyline pts (current source/width already set)."""
    if p <= 0:
        return
    segs = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total, left = sum(segs), sum(segs) * clamp(p)
    cx = c.ctx
    cx.new_path()
    cx.move_to(*pts[0])
    for (a, b), d in zip(zip(pts, pts[1:]), segs):
        if left >= d:
            cx.line_to(*b)
            left -= d
        else:
            f = left / d if d else 0
            cx.line_to(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            break
    cx.stroke()


# ── the photo ───────────────────────────────────────────────────────────
HEX = "0123456789abcdef"


def foto(c, x, y, w, h, t=0.0, scramble=0.0, seed=7, r=14, alpha=1.0):
    """A holiday snapshot (sky, sun, two hills) in (x, y, w, h). scramble 0..1 crossfades it into what the server sees:
    an ink tile of seeded hex characters that re-roll 10× a second (data acak — not matrix rain)."""
    with c.group(alpha), c.clip(x, y, w, h, r):
        if scramble < 1:
            with c.group(1 - scramble):
                c.fill_rrect(x, y, w, h, 0, mix(tk.REEL_WORLDS[1], PAPER, 0.62))
                c.circle(x + w * 0.70, y + h * 0.34, min(w, h) * 0.13, tk.REEL_WORLDS[4])
                cx = c.ctx
                for (k, col, base, amp) in ((0, tk.REEL_WORLDS[0], 0.70, 0.22), (1, _shade(tk.REEL_WORLDS[0], 0.75),
                                                                                   0.82, 0.16)):
                    cx.new_path()
                    cx.move_to(x, y + h)
                    for i in range(25):
                        u = i / 24
                        cx.line_to(x + w * u, y + h * (base - amp * math.sin(math.pi * (u * 1.3 + k * 0.45))))
                    cx.line_to(x + w, y + h)
                    cx.close_path()
                    c.src(col)
                    cx.fill()
        if scramble > 0:
            with c.group(scramble):
                c.fill_rrect(x, y, w, h, 0, INK)
                fs = max(17, min(w, h) / 7)
                cols, rows = max(1, int(w / (fs * 0.8))), max(1, int(h / (fs * 1.3)))
                tick = int(t * 10)
                for j in range(rows):
                    line = "".join(HEX[_hash(seed, j, i, tick) % 16] for i in range(cols))
                    c.text(x + (w - cols * fs * 0.62) / 2, y + (h - rows * fs * 1.3) / 2 + (j + 0.8) * fs * 1.3,
                           line, F["mono_med"], fs, PAPER, 0.85, 0.0)


# ── the locked box ──────────────────────────────────────────────────────
def kotak(c, cx, base_y, s, lid=0.0, lock=1.0, inside=None, color=None, alpha=1.0, label=None):
    """Lock box (width s, height ≈ 0.62 s) standing on base_y. lid 0..1 lifts the lid back; lock 0..1 turns the
    keyhole bolt shut. inside(c, top_y) draws something sinking into the open box (drawn behind the body)."""
    color = color or TERRA
    w, h = s, s * 0.5
    x, top = cx - w / 2, base_y - h
    lh = s * 0.14
    with c.group(alpha):
        if inside:
            with c.clip(x - s, top - 3 * s, w + 2 * s, 3 * s + 2):
                inside(c, top)
        c.shadow(x, top, w, h, s * 0.06, 30, 12, 0.10)
        c.fill_rrect(x, top, w, h, s * 0.06, color)
        c.fill_rrect(x, top + h * 0.48, w, h * 0.12, 0, _shade(color, 0.86))           # strap
        pw, ph = s * 0.24, h * 0.52                                                     # front plate + keyhole
        px, py = cx - pw / 2, top + h * 0.26
        c.fill_rrect(px, py, pw, ph, s * 0.03, mix(PAPER, color, 0.18))
        kx, ky = cx, py + ph * 0.42
        ang = lock * math.pi / 2
        c.circle(kx, ky, s * 0.032, INK)
        c.ctx.save()
        c.ctx.translate(kx, ky)
        c.ctx.rotate(ang)
        c.fill_rrect(-s * 0.012, 0, s * 0.024, s * 0.07, s * 0.01, INK)
        c.ctx.restore()
        if label:
            c.text(cx, base_y + 40, label, F["mono_med"], max(17, s * 0.09), INK, 0.7, 0.16, align="c")
        # lid: hinged at the back-right corner, swings up and back
        a = clamp(lid) * 1.15
        c.ctx.save()
        c.ctx.translate(x + w, top)
        c.ctx.rotate(a)
        c.fill_rrect(-w - 4, -lh, w + 8, lh, s * 0.05, _shade(color, 0.9))
        c.fill_rrect(-w / 2 - s * 0.08, -lh * 0.62, s * 0.16, lh * 0.3, lh * 0.15, _shade(color, 0.7))
        c.ctx.restore()


# ── the key ─────────────────────────────────────────────────────────────
def kunci(c, cx, cy, s, rot=0.0, color=None, alpha=1.0):
    """Key of length s centred on (cx, cy), bow on the left, teeth down at the right end, rotated by rot (radians)."""
    color = color or GREEN
    r = s * 0.2
    with c.group(alpha):
        c.ctx.save()
        c.ctx.translate(cx, cy)
        c.ctx.rotate(rot)
        x0 = -s / 2
        c.circle(x0 + r, 0, r, color)
        c.circle(x0 + r, 0, r * 0.42, PAPER)
        c.fill_rrect(x0 + r * 1.7, -s * 0.045, s - r * 1.7, s * 0.09, s * 0.03, color)
        for k, (dx, dh) in enumerate(((0.80, 0.16), (0.92, 0.11))):
            c.fill_rrect(x0 + s * dx, 0, s * 0.07, s * dh, s * 0.015, color)
        c.ctx.restore()


# ── WhatsApp-style ticks ────────────────────────────────────────────────
def centang(c, x, y, s, p1=1.0, p2=0.0, color=None, alpha=1.0, width=None):
    """Ticks drawn on: first ✓ by p1, the second (offset right) by p2. (x, y) = bottom-left of the first tick, s = its
    height. Grey/ink = delivered, never blue (blue = read). Returns the total width."""
    color = color or INK
    lw = width or max(2.5, s * 0.14)
    c.src(color, alpha)
    c.ctx.set_line_width(lw)
    c.ctx.set_line_cap(cairo.LineCap.ROUND)
    c.ctx.set_line_join(cairo.LineJoin.ROUND)
    for k, p in enumerate((p1, p2)):
        ox = x + k * s * 0.5
        pts = [(ox, y - s * 0.45), (ox + s * 0.32, y - s * 0.08), (ox + s * 0.95, y - s * 0.95)]
        _partial(c, pts, p)
    return s * 1.45


# ── the locker wall ─────────────────────────────────────────────────────
def loker_cell(x, y, w, h, cols, rows, i, pad=None, gap=None):
    """(x, y, w, h) of cell i (row-major) in a loker() drawn with the same geometry."""
    pad = pad if pad is not None else min(w, h) * 0.035
    gap = gap if gap is not None else min(w, h) * 0.022
    cw = (w - 2 * pad - (cols - 1) * gap) / cols
    ch = (h - 2 * pad - (rows - 1) * gap) / rows
    col, row = i % cols, i // cols
    return x + pad + col * (cw + gap), y + pad + row * (ch + gap), cw, ch


def loker(c, x, y, w, h, t=0.0, cols=3, rows=3, doors=None, lit=None, inside=None, first=1, label=None, color=None,
          alpha=1.0):
    """Left-luggage locker wall (x, y, w, h): cols × rows numbered doors on a frame + a header plate (label).
    doors = {i: open 0..1} swings door i open on its left hinge (it turns toward the camera and folds out past the
    hinge); lit = {i: 0..1} rings door i and lights its number; inside = {i: fn(c, cx, cy, cw, ch)} draws what sits
    in cell i (seen when its door is open)."""
    color = color or TERRA
    doors, lit, inside = doors or {}, lit or {}, inside or {}
    frame = mix(color, PAPER, 0.55)
    door = mix(color, PAPER, 0.22)
    cx = c.ctx
    with c.group(alpha):
        c.shadow(x, y, w, h, 18, 50, 20, 0.10)
        c.fill_rrect(x, y, w, h, 18, frame)
        if label:
            c.text(x + w / 2, y - 22, label, F["mono_med"], 22, INK, 0.65, 0.18, align="c")
        for i in range(cols * rows):
            dx, dy, dw, dh = loker_cell(x, y, w, h, cols, rows, i)
            op = clamp(doors.get(i, 0.0))
            if op > 0.001:
                c.fill_rrect(dx, dy, dw, dh, 8, _shade(frame, 0.45))
                c.fill_rrect(dx, dy, dw, dh * 0.12, 8, _shade(frame, 0.32))
                if i in inside:
                    with c.clip(dx, dy, dw, dh, 8):
                        inside[i](c, dx + dw / 2, dy + dh / 2, dw, dh)
            a = op * math.radians(112)
            ex = dw * math.cos(a)                      # free edge x offset from the hinge (negative past 90°)
            grow = dh * 0.10 * math.sin(a)             # the free edge comes toward the camera → taller
            back = math.cos(a) < 0
            col = _shade(door, 0.8) if back else door
            cx.new_path()
            cx.move_to(dx, dy)
            cx.line_to(dx + ex, dy - grow)
            cx.line_to(dx + ex, dy + dh + grow)
            cx.line_to(dx, dy + dh)
            cx.close_path()
            c.src(col)
            cx.fill_preserve()
            c.src(_shade(door, 0.7), 0.5)
            cx.set_line_width(2)
            cx.stroke()
            if op < 0.5:                                # front details while it still faces us
                k = 1 - op * 2
                fx = lambda u: dx + ex * u
                with c.group(k):
                    for v in range(3):                  # vents
                        vy = dy + dh * 0.62 + v * dh * 0.07
                        c.line(fx(0.25), vy, fx(0.75), vy, _shade(door, 0.75), max(2, dh * 0.018))
                    num = f"{first + i:02d}"
                    li = clamp(lit.get(i, 0.0))
                    pw_ = max(30, abs(ex) * 0.42)
                    c.fill_rrect(fx(0.5) - pw_ / 2, dy + dh * 0.14, pw_, dh * 0.2, 6,
                                 mix(PAPER, GREEN, li * 0.9))
                    c.text(fx(0.5), dy + dh * 0.14 + dh * 0.15, num, F["mono_bold"], max(17, dh * 0.12),
                           mix(INK, PAPER, li), 1, 0.06, align="c")
                    c.fill_rrect(fx(0.84) - 5, dy + dh * 0.42, 10, dh * 0.16, 5, _shade(door, 0.55))   # handle
            li = clamp(lit.get(i, 0.0))
            if li > 0 and op < 0.05:
                c.stroke_rrect(dx - 6, dy - 6, dw + 12, dh + 12, 12, GREEN, 4, li)
