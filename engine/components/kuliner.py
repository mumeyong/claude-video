"""Food-lot components (first used in "bongkar-ep05-legacy-container-hybrid").

ruko · kios · flip_sign · gapura · visitor
Signature move: the split-flap direction board flips its destination, and the visitor stream turns with it.
Pure functions of their progress values and t; jitter is hash-seeded.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix
from .infra import _h

GREEN = tk.CHAPTER[1][0]
WHITE = (1, 1, 1, 1)


def _awning(c, x, y, w, h, color, stripes=6, alpha=1.0):
    """Striped awning (scalloped bottom) from (x, y), width w, height h."""
    sw = w / stripes
    for k in range(stripes):
        col = color if k % 2 == 0 else c.theme("card", "d_card")
        c.fill_rrect(x + k * sw, y, sw + 0.5, h, 0, col, alpha)
        c.circle(x + k * sw + sw / 2, y + h, sw / 2, col, alpha)
    c.stroke_rrect(x, y, w, h, 2, color, 2, alpha)


# ── ruko (legacy) ───────────────────────────────────────────────────────
def ruko(c, x, base_y, w, h, t, label="Toko Lama", label_rot=-0.03, door=0.7, hot=0.0, alpha=1.0, seed=0):
    """Two-storey shophouse standing on base_y. door 0..1 = rolling door open; hot 0..1 = overloaded (red flicker)."""
    ink2, faint = c.theme("ink2", "d_muted"), c.theme("faint", "d_line")
    red = tk.C["rec"]
    yt = base_y - h
    fl = 0.5 + 0.5 * math.sin(t * 23 + seed) if hot > 0 else 0.0
    with c.group(alpha):
        c.shadow(x, yt, w, h, 10, 26, 10, 0.08)
        c.fill_rrect(x, yt, w, h, 8, mix(c.theme("card", "d_card"), c.theme("faint", "d_line"), 0.25))
        c.stroke_rrect(x, yt, w, h, 8, c.theme("line", "d_line"), 1.5)
        c.fill_rrect(x - 8, yt - 16, w + 16, 22, 4, ink2)                    # parapet
        # upper floor: two windows
        for k in range(2):
            wx = x + w * (0.12 + 0.44 * k)
            c.fill_rrect(wx, yt + h * 0.08, w * 0.32, h * 0.2, 4, faint)
            c.line(wx + w * 0.16, yt + h * 0.08, wx + w * 0.16, yt + h * 0.28, c.theme("card", "d_card"), 3)
        # signboard (hand-painted, a bit crooked)
        sy = yt + h * 0.34
        with c.at(0, 0, 1, origin=(x + w / 2, sy + h * 0.06), rot=label_rot):
            c.fill_rrect(x + w * 0.08, sy, w * 0.84, h * 0.12, 4, ink2)
            c.text(x + w / 2, sy + h * 0.095, label, tk.F["serif"], max(20, h * 0.08), WHITE, 1, align="c")
        _awning(c, x + w * 0.04, yt + h * 0.5, w * 0.92, h * 0.07, mix(ink2, red, hot * fl), 7)
        # rolling door
        dx, dy, dw, dh = x + w * 0.12, yt + h * 0.62, w * 0.76, h * 0.38
        c.fill_rrect(dx, dy, dw, dh, 2, mix(c.theme("ink", "d_bg"), red, 0.5 * hot * fl), 0.85)
        shut = dh * (1 - clamp(door))
        c.fill_rrect(dx, dy, dw, shut, 2, faint)
        n = int(shut / 12)
        for k in range(1, n + 1):
            c.line(dx + 4, dy + k * 12, dx + dw - 4, dy + k * 12, c.theme("muted", "d_muted"), 1.5, 0.6)


# ── kios kontainer (container) ──────────────────────────────────────────
def kios(c, x, base_y, w, h, t, label=None, color=None, open_=1.0, alpha=1.0, seed=0):
    """Container stall: corrugated box, serving hatch (open_ 0..1 lifts the flap), label on the side."""
    color = color or GREEN
    yt = base_y - h
    body = mix(c.theme("card", "d_card"), color, 0.85)
    with c.group(alpha):
        c.shadow(x, yt, w, h, 6, 24, 10, 0.1, color)
        c.fill_rrect(x, yt, w, h, 6, body)
        for k in range(1, int(w / 16)):
            c.line(x + k * 16, yt + 6, x + k * 16, base_y - 6, WHITE, 2, 0.22)
        c.fill_rrect(x, yt, w, 10, 4, mix(body, (0, 0, 0, 1), 0.15))
        c.fill_rrect(x, base_y - 10, w, 10, 4, mix(body, (0, 0, 0, 1), 0.15))
        # hatch + flap
        hx, hy, hw, hh = x + w * 0.14, yt + h * 0.24, w * 0.72, h * 0.36
        c.fill_rrect(hx, hy, hw, hh, 4, c.theme("ink", "d_bg"), 0.82)
        c.fill_rrect(hx - 6, hy + hh, hw + 12, 10, 3, mix(body, WHITE, 0.6))          # counter
        fh = hh * 0.55 * clamp(open_)
        c.fill_rrect(hx - 8, hy - fh, hw + 16, max(6, fh), 3, mix(body, (0, 0, 0, 1), 0.08))
        for k in range(3):                                                           # hanging lamps
            lx = hx + hw * (0.2 + 0.3 * k)
            c.circle(lx, hy + 16, 6, WHITE, 0.9 * clamp(open_))
        if label:
            c.text(x + w / 2, base_y - h * 0.12, label, tk.F["mono_bold"], max(17, min(22, w * 0.12)), WHITE, 1,
                   0.08, align="c")


# ── split-flap board (Nginx) ────────────────────────────────────────────
def _flap_char(c, x, y, cw, ch, old, new, p, color, ink):
    """One split-flap cell at (x, y). p 0..1 = flip progress from old to new char."""
    c.fill_rrect(x, y, cw, ch, 4, c.theme("ink", "d_bg"))
    ch_ = old if p < 0.5 else new
    sy = abs(math.cos(p * math.pi)) if 0 < p < 1 else 1.0
    cx = c.ctx
    cx.save()
    cx.translate(x + cw / 2, y + ch / 2)
    cx.scale(1, max(0.02, sy))
    cx.translate(-(x + cw / 2), -(y + ch / 2))
    col = ink if (p < 0.5 and old != new) else color
    c.text(x + cw / 2, y + ch * 0.74, ch_, tk.F["mono_bold"], ch * 0.66, col, 1, 0, align="c")
    cx.restore()
    c.line(x + 2, y + ch / 2, x + cw - 2, y + ch / 2, (0, 0, 0, 1), 2, 0.5)


def flip_sign(c, x, y, w, rows, t, row_h=78, title=None, color=None, cells=10, alpha=1.0):
    """Direction board. rows: [{label, dest, prev=None, t_flip=None, stuck=None (char index), color=None}].

    Each destination is `cells` split-flap cells on the right; chars flip one by one from prev to dest at t_flip.
    """
    color = color or GREEN
    ink = c.theme("d_ink", "d_ink")
    th = 44 if title else 0
    h = th + len(rows) * row_h + 24
    with c.group(alpha):
        c.shadow(x, y, w, h, 18, 30, 12, 0.12)
        c.fill_rrect(x, y, w, h, 18, mix(c.theme("ink2", "d_card"), (0, 0, 0, 1), 0.35))
        c.stroke_rrect(x, y, w, h, 18, color, 3)
        if title:
            c.text(x + 26, y + 36, title, tk.F["mono_bold"], 18, color, 1, 0.16)
        cw = min(46, (w * 0.56) / cells - 4)
        cx0 = x + w - 22 - cells * (cw + 4)
        for i, r in enumerate(rows):
            ry = y + th + 12 + i * row_h
            c.text(x + 26, ry + row_h * 0.62, r["label"], tk.F["mono_med"], max(17, row_h * 0.3), ink, 1, 0.02)
            c.text(cx0 - 16, ry + row_h * 0.62, "→", tk.F["ui_semi"], row_h * 0.36, color, 1, align="r")
            new = r["dest"].upper().ljust(cells)[:cells]
            old = (r.get("prev") or r["dest"]).upper().ljust(cells)[:cells]
            tf = r.get("t_flip")
            rc = r.get("color") or color
            for k in range(cells):
                p = 1.0 if tf is None else clamp((t - tf - k * 0.05) / 0.14)
                if r.get("stuck") == k and tf is not None and t < tf + k * 0.05 + 0.5:
                    p = min(p, 0.45)                                  # one flap hangs half-way, then drops
                _flap_char(c, cx0 + k * (cw + 4), ry + 8, cw, row_h - 16, old[k], new[k], p, rc, ink)


def flip_cues(row, cells=10):
    """SFX times for a flipping row (one tick per changed char)."""
    tf = row.get("t_flip")
    if tf is None:
        return []
    new = row["dest"].upper().ljust(cells)[:cells]
    old = (row.get("prev") or row["dest"]).upper().ljust(cells)[:cells]
    return [tf + k * 0.05 for k in range(cells) if new[k] != old[k]][::2]


# ── gapura (SLB) ────────────────────────────────────────────────────────
def gapura(c, cx, base_y, w, h, t, label="PINTU DEPAN", lane=None, booth=True, color=None, alpha=1.0):
    """The single front gate: two pillars, a beam with the label, two lane lamps (lane 0/1 lit), satpam booth."""
    color = color or GREEN
    ink2 = c.theme("ink2", "d_muted")
    x0, x1 = cx - w / 2, cx + w / 2
    pw = 34
    with c.group(alpha):
        for px in (x0, x1 - pw):
            c.fill_rrect(px, base_y - h, pw, h, 8, ink2)
            c.fill_rrect(px - 8, base_y - 14, pw + 16, 14, 4, ink2)
        c.fill_rrect(x0 - 20, base_y - h - 70, w + 40, 76, 14, color)
        c.text(cx, base_y - h - 20, label, tk.F["mono_bold"], 26, WHITE, 1, 0.16, align="c")
        for k, lx in enumerate((cx - w * 0.22, cx + w * 0.22)):
            on = 1.0 if lane == k else 0.25
            c.circle(lx, base_y - h + 26, 13, color if lane == k else c.theme("faint", "d_line"), 1)
            if lane == k:
                c.circle(lx, base_y - h + 26, 26, color, 0.2 * on)
        if booth:
            bx, bw, bh = x0 - 120, 90, 120
            c.fill_rrect(bx, base_y - bh, bw, bh, 10, c.theme("card", "d_card"))
            c.stroke_rrect(bx, base_y - bh, bw, bh, 10, c.theme("line", "d_line"), 1.5)
            c.fill_rrect(bx + 12, base_y - bh + 18, bw - 24, 40, 4, c.theme("faint", "d_line"))
            c.circle(bx + bw / 2, base_y - bh + 40, 10, ink2)                            # satpam in the window
            c.text(bx + bw / 2, base_y - 22, "SATPAM", tk.F["mono_bold"], 17, ink2, 1, 0.08, align="c")


def visitor(c, x, y, s, t, color=None, walk=1.0, alpha=1.0, seed=0):
    """Tiny person, feet at (x, y), height s, bobbing while walking."""
    color = color or c.theme("ink2", "d_ink")
    bob = abs(math.sin(t * 9 + _h(seed, 2) * 6)) * s * 0.05 * walk
    with c.group(alpha):
        c.fill_rrect(x - s * 0.17, y - s * 0.72 - bob, s * 0.34, s * 0.5, s * 0.15, color)
        c.circle(x, y - s * 0.86 - bob, s * 0.14, color)
        ph = math.sin(t * 9 + _h(seed, 2) * 6) * walk
        c.line(x - s * 0.07, y - s * 0.26 - bob, x - s * 0.07 + ph * s * 0.08, y, color, s * 0.09)
        c.line(x + s * 0.07, y - s * 0.26 - bob, x + s * 0.07 - ph * s * 0.08, y, color, s * 0.09)


def walk_path(pts, f):
    """Point at fraction f (0..1) along a polyline pts (equal time per segment)."""
    f = clamp(f)
    n = len(pts) - 1
    i = min(n - 1, int(f * n))
    u = f * n - i
    (x0, y0), (x1, y1) = pts[i], pts[i + 1]
    return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u


def fade_ends(f, k=8):
    """Alpha for something travelling 0..1: fades in at the start, out at the end."""
    return clamp(min(f * k, (1 - f) * k))


