"""Blueprint / floor-plan components (first used in the channel intro video "kenalan-mumeyong").

bp_grid · bp_house · outline_text · dimension · phone_wire · city_map
Signature move they share: lines draw first (p_draw), then the shape "becomes real" (p_fill).
Pure functions of their progress values and t; all variation is hash-seeded.
"""
import math

from .. import tokens as tk
from ..draw import PangoCairo
from ..ease import clamp, mix, in_out_cubic, glide, pop
from .infra import _draw_poly, _h

TEAL = tk.CHAPTER[4][0]
WHITE = (1, 1, 1, 1)


def _line_col(c, color=None):
    return color or mix(TEAL, c.theme("ink", "d_ink"), 0.15)


# ── blueprint paper ─────────────────────────────────────────────────────
def bp_grid(c, x, y, w, h, alpha=1.0, r=26, minor=24, major=120, card=True):
    """Card with a teal blueprint grid (minor + major lines). In dark sections it reads as a classic blueprint."""
    if card:
        c.card(x, y, w, h, r=r, alpha=alpha)
    with c.clip(x + 1, y + 1, w - 2, h - 2, r - 1):
        for step, a in ((minor, 0.07), (major, 0.16)):
            k = 1
            while k * step < w:
                c.line(x + k * step, y, x + k * step, y + h, TEAL, 1, a * alpha)
                k += 1
            k = 1
            while k * step < h:
                c.line(x, y + k * step, x + w, y + k * step, TEAL, 1, a * alpha)
                k += 1


def _segs_draw(c, segs, p, color, width):
    """Draw polylines one after another; p 0..1 over their total length."""
    lens = [sum(math.dist(a, b) for a, b in zip(s, s[1:])) for s in segs]
    total = sum(lens) or 1
    d = total * clamp(p)
    for s, L in zip(segs, lens):
        if d <= 0:
            break
        _draw_poly(c, s, min(1.0, d / L) if L else 1.0, color, width)
        d -= L


# ── floor plan ──────────────────────────────────────────────────────────
def house_rooms(x, y, w, h):
    """Room rects of bp_house (same geometry): [living, server room, bedroom]."""
    vx, hy = x + w * 0.56, y + h * 0.58
    return [(x, y, vx - x, hy - y), (vx, y, x + w - vx, hy - y), (x, hy, w, y + h - hy)]


def bp_house(c, x, y, w, h, p_draw, p_fill=0.0, color=None, width=5, scribble=0.0, fit=None, fill_alpha=0.16):
    """Floor plan: outer walls, two inner walls (with door gaps), door arc, windows.

    scribble 0..1: a wrong diagonal wall gets drawn (0–.5), then crossed out (.5–1) — a revision mark.
    fit = (room_index, p): that room is missing (dashed slot) and slides in from the right as p goes 0→1.
    Returns the room rects."""
    col = _line_col(c, color)
    rooms = house_rooms(x, y, w, h)
    vx, hy = x + w * 0.56, y + h * 0.58
    door = w * 0.11
    segs = [
        [(x, y + h * 0.3), (x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y + h * 0.42)],   # outer, door gap left
        [(vx, y), (vx, hy - door * 1.4)],                                                        # inner vertical
        [(x, hy), (vx - door * 1.2, hy)],                                                        # inner horizontal, left
        [(vx + door * 0.2, hy), (x + w, hy)],                                                    # inner horizontal, right
    ]
    fi, fp = fit if fit else (None, 1.0)
    # room fills (the "becomes real" half of the signature move)
    if p_fill > 0:
        for i, (rx, ry, rw, rh) in enumerate(rooms):
            if i == fi:
                continue
            c.fill_rrect(rx + 4, ry + 4, rw - 8, rh - 8, 6, TEAL, fill_alpha * clamp(p_fill * (1.4 - 0.2 * i)))
    _segs_draw(c, segs, p_draw, col, width)
    if p_draw >= 1:
        # door arc (entrance, left wall) + windows
        cx_ = c.ctx
        cx_.new_path()
        cx_.arc(x, y + h * 0.42, h * 0.12, -math.pi / 2, 0)
        c.src(col, 0.6)
        cx_.set_line_width(2)
        cx_.stroke()
        for wx0, wx1 in ((0.18, 0.36), (0.68, 0.86)):
            c.line(x + w * wx0, y, x + w * wx1, y, c.theme("card", "d_card"), width + 2)
            c.line(x + w * wx0, y - 5, x + w * wx1, y - 5, col, 2)
            c.line(x + w * wx0, y + 5, x + w * wx1, y + 5, col, 2)
    if scribble > 0:
        s1 = clamp(scribble * 2)
        ax, ay, bx, by = x + w * 0.2, y + h * 0.66, x + w * 0.42, y + h * 0.94
        _draw_poly(c, [(ax, ay), (bx, by)], s1, col, width - 1, 0.8)
        s2 = clamp(scribble * 2 - 1)
        if s2 > 0:
            for k in range(3):
                o = (k - 1) * 14
                _draw_poly(c, [(ax - 10 + o, by - 6), (bx + 10 + o, ay + 6)], clamp(s2 * 3 - k), tk.C["rec"], 3)
    if fi is not None:
        rx, ry, rw, rh = rooms[fi]
        c.stroke_rrect(rx + 6, ry + 6, rw - 12, rh - 12, 8, col, 2, 0.6 * (1 - clamp(fp * 3 - 2)), dash=[10, 8])
        e = in_out_cubic(clamp(fp))
        dx = (1 - e) * (w * 0.75)
        a = clamp(fp * 3)
        c.fill_rrect(rx + 4 + dx, ry + 4, rw - 8, rh - 8, 6, TEAL, (0.12 + 0.2 * clamp(fp * 2 - 1)) * a)
        c.stroke_rrect(rx + 4 + dx, ry + 4, rw - 8, rh - 8, 6, col, width - 1, a)
    return rooms


# ── dimension line ──────────────────────────────────────────────────────
def dimension(c, x1, y1, x2, y2, label, p, color=None, off=0):
    """Architect's dimension line between two points (horizontal or vertical), ticks at both ends, label in the middle."""
    if p <= 0:
        return
    col = _line_col(c, color)
    e = glide(clamp(p))
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    hx, hy = (x2 - x1) / 2 * e, (y2 - y1) / 2 * e
    c.line(mx - hx, my - hy, mx + hx, my + hy, col, 2)
    horiz = abs(x2 - x1) >= abs(y2 - y1)
    for (px, py) in ((mx - hx, my - hy), (mx + hx, my + hy)):
        if horiz:
            c.line(px, py - 12, px, py + 12, col, 2)
        else:
            c.line(px - 12, py, px + 12, py, col, 2)
    a = clamp(p * 2 - 0.6)
    if a > 0:
        tw = c.measure(label, tk.F["mono_med"], 18, 0.04)[0] + 20
        lx, ly = (mx, my - 22 - off) if horiz else (mx + 24 + off, my)
        al = "c" if horiz else "l"
        bx = lx - tw / 2 if horiz else lx - 10
        c.fill_rrect(bx, ly - 22, tw, 32, 8, c.theme("card", "d_card"), a)
        c.text(lx, ly, label, tk.F["mono_med"], 18, col, a, 0.04, align=al)


# ── outline text (signature move) ───────────────────────────────────────
def outline_text(c, x, y, text, font, size, p_draw, p_fill, color=None, fill=None, ls=-0.05, align="l", width=3):
    """Text (baseline at y) whose outline is revealed left→right by p_draw, then filled by p_fill. Returns width."""
    if p_draw <= 0 and p_fill <= 0:
        return 0.0
    col = _line_col(c, color)
    fill = fill or c.theme("ink", "d_ink")
    lay = c.layout(text, font, size, ls)
    tw, th, base = c.extents(lay)
    if ls > 0:
        tw -= ls * size
    dx = 0 if align == "l" else (-tw / 2 if align == "c" else -tw)
    x0 = x + dx
    cx = c.ctx
    if p_fill > 0:
        cx.move_to(x0, y - base)
        c.src(fill, clamp(p_fill))
        PangoCairo.show_layout(cx, lay)
        cx.new_path()
    if p_draw > 0:
        ol = 1 - clamp(p_fill) * 0.85
        with c.clip(x0 - 12, y - base - 20, (tw + 24) * clamp(p_draw), th + 40):
            cx.move_to(x0, y - base)
            PangoCairo.layout_path(cx, lay)
            c.src(col, ol)
            cx.set_line_width(width)
            cx.set_line_join(1)
            cx.stroke()
        # the pen tip while drawing
        if 0 < p_draw < 1:
            c.circle(x0 + (tw + 12) * p_draw, y - size * 0.35, 6, col)
    return tw


# ── phone wireframe ─────────────────────────────────────────────────────
def phone_wire(c, cx, cy, s, p, kind, label=None, color=None, fill=0.0):
    """Wireframe phone (height s) that draws on with p; glyph by kind: bank · ticket · qris. fill 0..1 tints it teal."""
    if p <= 0:
        return
    col = _line_col(c, color)
    w, h = s * 0.52, s
    x, y = cx - w / 2, cy - h / 2
    r = w * 0.16
    if fill > 0:
        c.fill_rrect(x, y, w, h, r, TEAL, 0.14 * clamp(fill))
    _draw_poly(c, [(x + r, y), (x + w - r, y), (x + w, y + r), (x + w, y + h - r), (x + w - r, y + h),
                   (x + r, y + h), (x, y + h - r), (x, y + r), (x + r, y)], clamp(p * 1.4), col, 3)
    a = clamp(p * 2 - 1)
    if a <= 0:
        return
    c.fill_rrect(cx - w * 0.16, y + h * 0.05, w * 0.32, h * 0.025, 3, col, a)
    gx, gy, gs = cx, cy, w * 0.62
    if kind == "bank":
        c.stroke_rrect(gx - gs / 2, gy - gs * 0.32, gs, gs * 0.64, 8, col, 3, a)
        c.fill_rrect(gx - gs * 0.36, gy - gs * 0.14, gs * 0.2, gs * 0.15, 3, col, a)
        c.line(gx - gs * 0.36, gy + gs * 0.16, gx + gs * 0.2, gy + gs * 0.16, col, 3, a)
    elif kind == "ticket":
        c.stroke_rrect(gx - gs / 2, gy - gs * 0.3, gs, gs * 0.6, 6, col, 3, a)
        for sy in (-1, 1):
            c.circle(gx + gs * 0.18, gy + sy * gs * 0.3, gs * 0.07, c.theme("card", "d_card"), a)
        for k in range(5):
            c.line(gx + gs * 0.18, gy - gs * 0.2 + k * gs * 0.1, gx + gs * 0.18, gy - gs * 0.15 + k * gs * 0.1, col, 2, a)
    else:  # qris
        q = gs * 0.9
        qx, qy = gx - q / 2, gy - q / 2
        for fx, fy in ((0, 0), (1, 0), (0, 1)):
            bx, by = qx + fx * q * 0.68, qy + fy * q * 0.68
            c.stroke_rrect(bx, by, q * 0.32, q * 0.32, 3, col, 3, a)
            c.fill_rrect(bx + q * 0.1, by + q * 0.1, q * 0.12, q * 0.12, 2, col, a)
        for i in range(16):
            if _h(i, 7) > 0.45:
                c.fill_rrect(qx + q * (0.42 + 0.14 * (i % 4)), qy + q * (0.42 + 0.14 * (i // 4)), q * 0.1, q * 0.1, 2,
                             col, a)
    if label:
        c.text(cx, y + h + 34, label, tk.F["mono_med"], 19, c.theme("muted", "d_muted"), a, 0.1, align="c")


# ── city map ────────────────────────────────────────────────────────────
def city_map(c, x, y, w, h, blocks, cols=3, rows=3, street=34, pin=None, pin_p=0.0, alpha=1.0):
    """Blueprint city: cols×rows blocks separated by streets.
    blocks: [dict(col, row, label, draw 0..1, lit 0..1, cw=1, rh=1)] · pin = (col, row) for the 'kamu di sini' pin.
    Returns {(col, row): rect}."""
    bp_grid(c, x, y, w, h, alpha)
    pad = 30
    bw = (w - 2 * pad - street * (cols - 1)) / cols
    bh = (h - 2 * pad - street * (rows - 1)) / rows
    col_line = _line_col(c)
    rects = {}
    for b in blocks:
        cw, rh = b.get("cw", 1), b.get("rh", 1)
        bx = x + pad + b["col"] * (bw + street)
        by = y + pad + b["row"] * (bh + street)
        ww, hh = bw * cw + street * (cw - 1), bh * rh + street * (rh - 1)
        rects[(b["col"], b["row"])] = (bx, by, ww, hh)
        d, lit = clamp(b.get("draw", 1.0)), clamp(b.get("lit", 0.0))
        if lit > 0:
            c.fill_rrect(bx, by, ww, hh, 14, TEAL, (0.12 + 0.6 * lit) * alpha)
        _draw_poly(c, [(bx + 14, by), (bx + ww - 14, by), (bx + ww, by + 14), (bx + ww, by + hh - 14),
                       (bx + ww - 14, by + hh), (bx + 14, by + hh), (bx, by + hh - 14), (bx, by + 14), (bx + 14, by)],
                   d, col_line, 3, alpha)
        la = clamp(d * 2 - 1) * alpha
        if la > 0 and b.get("label"):
            ink = mix(c.theme("ink", "d_ink"), WHITE, lit)
            for i, ln in enumerate(b["label"].split("\n")):
                c.text(bx + 18, by + 40 + i * 28, ln, tk.F["ui_semi"], 24, ink, la, -0.01)
            if b.get("sub"):
                c.text(bx + 18, by + hh - 20, b["sub"], tk.F["mono_med"], 16, mix(c.theme("muted", "d_muted"), WHITE, lit),
                       la, 0.1)
    if pin and pin in rects and pin_p > 0:
        bx, by, ww, hh = rects[pin]
        px, py = bx + ww - 40, by + 26
        s = pop(clamp(pin_p), 1.8)
        with c.at(0, 0, max(0.01, s), origin=(px, py + 30)):
            c.circle(px, py, 18, tk.C["rec"])
            c.ctx.new_path()
            c.ctx.move_to(px - 12, py + 10)
            c.ctx.line_to(px, py + 34)
            c.ctx.line_to(px + 12, py + 10)
            c.ctx.close_path()
            c.src(tk.C["rec"])
            c.ctx.fill()
            c.circle(px, py, 7, WHITE)
    return rects
