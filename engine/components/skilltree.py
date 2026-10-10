"""Skill-tree components (first used in "jalur-karier-cloud").

branch · skill_tile · skill_tree · name_card
Metaphor: a career as a game skill tree that grows bottom → top — every level opens new branches (tools), and the
top branches turn out to be questions (decisions), not tools. Signature: a branch creeps up from its parent with a
bright tip, the tile's ring charges round, then the tile unlocks (border + tint + ✓) with a small pop.
Pure functions of their progress values (frame = f(t)); colors from tokens (light + dark theme).
"""
import math

import cairo

from .. import tokens as tk
from ..ease import clamp, mix

RED = tk.CHAPTER[5][0]              # signature: branches, rings, unlocked tiles
F, C = tk.F, tk.C


def _cubic(p0, p1, p2, p3, u):
    a = (1 - u) ** 3
    b = 3 * (1 - u) ** 2 * u
    c = 3 * (1 - u) * u ** 2
    d = u ** 3
    return (a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1])


def _branch_pts(x0, y0, x1, y1, p=1.0, n=40):
    k = (y0 - y1) * 0.55
    ctrl = ((x0, y0), (x0, y0 - k), (x1, y1 + k), (x1, y1))
    m = max(2, int(n * p))
    return [_cubic(*ctrl, p * i / m) for i in range(m + 1)]


def _poly(c, pts):
    cx = c.ctx
    cx.new_path()
    cx.move_to(*pts[0])
    for q in pts[1:]:
        cx.line_to(*q)


def branch(c, x0, y0, x1, y1, p, color=None, width=6, ghost=1.0, alpha=1.0):
    """Branch from a parent's top (x0, y0) up to a child's bottom (x1, y1) as a vertical S-curve.
    ghost 0..1 = the locked path (thin, dashed, faint); p 0..1 grows the colored branch with a bright tip."""
    color = color or RED
    cx = c.ctx
    if ghost > 0:
        _poly(c, _branch_pts(x0, y0, x1, y1))
        c.src(c.theme("faint", "d_muted"), alpha * ghost * 0.8)
        cx.set_line_width(3)
        cx.set_dash([2, 12])
        cx.set_line_cap(cairo.LineCap.ROUND)
        cx.stroke()
        cx.set_dash([])
    p = clamp(p)
    if p <= 0:
        return
    pts = _branch_pts(x0, y0, x1, y1, p)
    _poly(c, pts)
    c.src(color, alpha)
    cx.set_line_width(width)
    cx.set_line_cap(cairo.LineCap.ROUND)
    cx.set_line_join(cairo.LineJoin.ROUND)
    cx.stroke()
    if p < 1:                                  # the creeping tip
        tx, ty = pts[-1]
        c.circle(tx, ty, width * 1.6, color, alpha)
        c.circle(tx, ty, width * 0.8, c.theme("card", "d_ink"), alpha)


def _check(c, x, y, s, color, alpha=1.0, width=4):
    cx = c.ctx
    cx.new_path()
    cx.move_to(x - s * 0.45, y + s * 0.02)
    cx.line_to(x - s * 0.12, y + s * 0.34)
    cx.line_to(x + s * 0.48, y - s * 0.32)
    c.src(color, alpha)
    cx.set_line_width(width)
    cx.set_line_cap(cairo.LineCap.ROUND)
    cx.set_line_join(cairo.LineJoin.ROUND)
    cx.stroke()


def _fit(c, text, font, size, maxw, lo=20):
    w = c.measure(text, font, size)[0]
    return size if w <= maxw else max(lo, size * maxw / w)


def skill_tile(c, cx, cy, w, h, label, charge=0.0, unlock=0.0, kind="tool", sub=None, color=None, alpha=1.0):
    """One tile of the tree, centred on (cx, cy). Locked = dashed outline + '• • •'. charge 0..1 runs the ring of the
    status dot round and fades the label in; unlock 0..1 = solid border, tint, ✓ and a small pop.
    kind 'question' unlocks to a solid tile with white text and a '?' dot; 'root' = round node with the label inside."""
    color = color or RED
    charge, unlock = clamp(charge), clamp(unlock)
    card, ink, faint = c.theme("card", "d_card"), c.theme("ink", "d_ink"), c.theme("faint", "d_muted")
    sc = 1 + 0.07 * math.sin(math.pi * unlock)
    with c.group(alpha), c.at(0, 0, sc, origin=(cx, cy)):
        x, y = cx - w / 2, cy - h / 2
        if kind == "root":
            r = min(w, h) / 2
            c.circle(cx, cy, r + 10, color, 0.18 * charge)
            c.circle(cx, cy, r, mix(card, color, unlock))
            c.text(cx, cy + 8, label, F["mono_bold"], 22, mix(ink, C["card"], unlock), 1, 0.06, align="c")
            return
        solid = kind == "question"
        r = 20
        c.shadow(x, y, w, h, r, blur=24, dy=8, alpha=0.06 * max(charge, 0.3))
        fill = mix(card, color, 0.10 * unlock) if not solid else mix(card, color, unlock)
        c.fill_rrect(x, y, w, h, r, fill, 0.55 + 0.45 * max(charge, unlock))
        if unlock < 1:
            c.stroke_rrect(x, y, w, h, r, faint, 2, 1 - unlock, dash=[8, 8])
        if unlock > 0:
            c.stroke_rrect(x, y, w, h, r, color, 3, unlock)
        # status dot on the left: ring charges, then fills
        dx, dy, dr = x + 40, cy, 17
        c.circle(dx, dy, dr, faint, 0.5 * (1 - unlock))
        if charge > 0:
            cxx = c.ctx
            cxx.new_path()
            cxx.arc(dx, dy, dr, -math.pi / 2, -math.pi / 2 + 2 * math.pi * charge)
            c.src(C["card"] if solid and unlock > 0.5 else color)
            cxx.set_line_width(4)
            cxx.stroke()
        if unlock > 0:
            if solid:
                c.text(dx, dy + 9, "?", F["display"], 28, C["card"], unlock, align="c")
            else:
                c.circle(dx, dy, dr * unlock, color)
                _check(c, dx, dy, 15, C["card"], unlock, 3.5)
        # label: '• • •' while locked → the real label fades in with the charge
        tx, maxw = x + 70, w - 70 - 20
        if charge < 1:
            c.text(tx, cy + 9, "• • •", F["mono_bold"], 24, faint, 1 - charge, 0.1)
        if charge > 0:
            col = mix(ink, C["card"], unlock) if solid else ink
            size = _fit(c, label, F["ui_semi"], 30, maxw)
            if sub:
                c.text(tx, cy + 1, label, F["ui_semi"], size, col, charge, -0.01)
                subc = mix(c.theme("muted", "d_muted"), C["card"], unlock) if solid else c.theme("muted", "d_muted")
                c.text(tx, cy + 28, sub, F["mono"], 18, subc, charge, 0.04)
            else:
                c.text(tx, cy + 10, label, F["ui_semi"], size, col, charge, -0.01)


def skill_tree(c, nodes, edges, alpha=1.0):
    """nodes: {id: dict(x, y, w, h, label, charge, unlock, kind='tool', sub=None, a=1.0)} (x, y = centre);
    edges: [(parent_id, child_id, p, ghost)] — p grows the branch from the parent's top to the child's bottom."""
    with c.group(alpha):
        for a, b, p, ghost in edges:
            na, nb = nodes[a], nodes[b]
            branch(c, na["x"], na["y"] - na["h"] / 2, nb["x"], nb["y"] + nb["h"] / 2, p, ghost=ghost,
                   alpha=min(na.get("a", 1.0), nb.get("a", 1.0)))
        for n in nodes.values():
            skill_tile(c, n["x"], n["y"], n["w"], n["h"], n["label"], n.get("charge", 0.0), n.get("unlock", 0.0),
                       n.get("kind", "tool"), n.get("sub"), alpha=n.get("a", 1.0))


def name_card(c, x, y, w, h, role, task, year="", level="", color=None, alpha=1.0):
    """Business card (x, y, w, h): color stripe on the left, 'KARTU NAMA · year' + level pill, the role big
    (may contain '\\n'), a hairline, then 'TUGAS' + the task line."""
    color = color or RED
    ink, muted = c.theme("ink", "d_ink"), c.theme("muted", "d_muted")
    with c.group(alpha):
        c.card(x, y, w, h, r=28)
        with c.clip(x, y, w, h, 28):
            c.fill_rrect(x, y, 16, h, 0, color)
        px = x + 64
        c.text(px, y + 76, f"KARTU NAMA · {year}" if year else "KARTU NAMA", F["mono_med"], 22, muted, 1, 0.18)
        if level:
            lw = c.measure(level, F["mono_bold"], 22, 0.1)[0] + 36
            c.fill_rrect(x + w - 48 - lw, y + 46, lw, 44, 22, color)
            c.text(x + w - 48 - lw / 2, y + 76, level, F["mono_bold"], 22, C["card"], 1, 0.1, align="c")
        lines = role.split("\n")
        size = min(_fit(c, ln, F["display"], 76, w - 64 - 48, lo=40) for ln in lines)
        for i, ln in enumerate(lines):
            c.text(px, y + 110 + size * (0.95 + i), ln, F["display"], size, ink, 1, -0.045)
        c.line(px, y + h - 140, x + w - 48, y + h - 140, c.theme("line", "d_line"), 2)
        c.text(px, y + h - 92, "TUGAS", F["mono_med"], 20, muted, 1, 0.18)
        size = _fit(c, task, F["ui"], 38, w - 64 - 48, lo=24)
        c.text(px, y + h - 44, task, F["ui"], size, c.theme("ink2", "d_ink"), 1, -0.015)
