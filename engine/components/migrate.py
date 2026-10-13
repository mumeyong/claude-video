"""Data-migration explainer components (first used in Bongkar Arsitektur EP02).

keycap · bookshelf · sync_pipe · twin_table · cutover_switch · padlock · series_bumper
Pure drawing from explicit progress values; all variation is hash-seeded (deterministic).
"""
import math

from .. import tokens as tk
from ..ease import clamp, lerp, mix, out_expo, in_out_cubic, in_cubic, prog, glide, pop
from .infra import _elbow, _along, _draw_poly, _h, arch_node
from . import icons

GREEN = tk.CHAPTER[1][0]


# ── keycap ──────────────────────────────────────────────────────────────
def keycap(c, cx, cy, label, press=0.0, size=220, sub=""):
    """3D-ish key: top face + darker base; press 0..1 pushes it down (pulse it for a tap)."""
    w = h = size
    depth = size * 0.11
    dy = depth * 0.8 * press
    base = c.theme("faint", "d_line")
    c.shadow(cx - w / 2, cy - h / 2 + depth, w, h, size * 0.16, 30, 16, 0.12)
    c.fill_rrect(cx - w / 2, cy - h / 2 + depth, w, h, size * 0.16, mix(base, (0, 0, 0, 1), 0.15))
    c.fill_rrect(cx - w / 2, cy - h / 2 + dy, w, h, size * 0.16, c.theme("card", "d_card"))
    c.stroke_rrect(cx - w / 2, cy - h / 2 + dy, w, h, size * 0.16, c.theme("line", "d_line"), 2)
    if sub:
        c.text(cx - w / 2 + size * 0.12, cy - h / 2 + dy + size * 0.22, sub, tk.F["mono_med"], size * 0.12,
               c.theme("muted", "d_muted"), 1, 0.06)
    c.text(cx, cy + dy + size * 0.16, label, tk.F["display"], size * 0.46, c.theme("ink", "d_ink"), 1, -0.03,
           align="c")


# ── bookshelf ───────────────────────────────────────────────────────────
_SPINE = [tk.CHAPTER[i][0] for i in (0, 1, 2, 3, 4, 5)]


def shelf_books(x, y, w, h, rows=4, seed=3):
    """Deterministic book layout → list of (x, y, bw, bh, color_index)."""
    books = []
    row_h = h / rows
    for r in range(rows):
        bx = x + 18
        k = 0
        while True:
            bw = 26 + 22 * _h(r * 97 + k, seed)
            if bx + bw > x + w - 18:
                break
            bh = row_h * (0.62 + 0.3 * _h(r * 131 + k, seed + 1))
            books.append((bx, y + (r + 1) * row_h - 14 - bh, bw - 4, bh, int(_h(r * 71 + k, seed + 2) * 6)))
            bx += bw
            k += 1
    return books


def bookshelf(c, x, y, w, h, t, rows=4, seed=3, pulled=None, changed=None, falling=None, ghost=0.0,
              diff=None, diff_p=0.0):
    """pulled: {i: p} slides book i up/out · changed: {i: p} flashes a new color · falling: (i, p) drops a book.
    ghost 0..1 desaturates (a frozen copy). diff: book indices marked red on this copy (diff_p)."""
    c.card(x, y, w, h, r=26)
    row_h = h / rows
    for r in range(rows):
        sy = y + (r + 1) * row_h - 14
        c.fill_rrect(x + 12, sy, w - 24, 10, 5, c.theme("faint", "d_line"))
    books = shelf_books(x, y, w, h, rows, seed)
    pulled, changed = pulled or {}, changed or {}
    grey = c.theme("faint", "d_line")
    for i, (bx, by, bw, bh, ci) in enumerate(books):
        col = _SPINE[ci]
        if i in changed and changed[i] > 0:
            flash = math.sin(math.pi * clamp(changed[i]))
            col = mix(col, _SPINE[(ci + 3) % 6], clamp(changed[i] * 2))
            if flash > 0.05:
                c.fill_rrect(bx - 3, by - 3, bw + 6, bh + 6, 6, GREEN, 0.35 * flash)
        col = mix(col, grey, ghost)
        dy = -bh * 0.55 * math.sin(math.pi * clamp(pulled.get(i, 0.0)))
        rot = 0.0
        if falling and falling[0] == i:
            p = clamp(falling[1])
            dy = 380 * in_cubic(p)
            rot = 1.6 * in_out_cubic(p)
            col = mix(col, tk.C["rec"], clamp(p * 2))
        with c.at(0, dy, 1.0, origin=(bx + bw / 2, by + bh / 2), rot=rot):
            c.fill_rrect(bx, by, bw, bh, 5, col, 0.92)
            c.fill_rrect(bx + 4, by + bh * 0.18, bw - 8, 5, 2, (1, 1, 1, 1), 0.45)
        if diff and i in diff and diff_p > 0:
            c.stroke_rrect(bx - 4, by - 4, bw + 8, bh + 8, 6, tk.C["rec"], 3, diff_p)
    return books


# ── sync pipe ───────────────────────────────────────────────────────────
def sync_pipe(c, t, src, dst, p_pipe=1.0, p_full=0.0, p_inc=0.0, open_badge=0.0, labels=("full copy", "incremental sync")):
    """src/dst = node dicts for arch_node (x, y, w, h, kind, label, a). Two lanes between them:
    lane 1 crates move while 0 < p_full < 1 (full copy); lane 2 dots stream with density p_inc."""
    arch_node(c, src)
    arch_node(c, dst)
    acc = c.theme("accent", "d_accent")
    sx, sy = src["x"] + src["w"] / 2, src["y"] + src["h"]
    dx, dy = dst["x"] + dst["w"] / 2, dst["y"]
    lanes = []
    for k, off in enumerate((-70, 70)):
        pts = _elbow((sx + off, sy), (dx + off, dy))
        lanes.append(pts)
        _draw_poly(c, pts, p_pipe, c.theme("faint", "d_line"), 10, 1.0)
    if p_pipe >= 1:
        lx, ly = _along(lanes[0], 0.5)
        c.text(lx - 24, ly - 20, labels[0].upper(), tk.F["mono_med"], 18, c.theme("muted", "d_muted"),
               clamp(p_full * 4), 0.14, align="r")
        lx, ly = _along(lanes[1], 0.5)
        c.text(lx + 24, ly - 20, labels[1].upper(), tk.F["mono_med"], 18, c.theme("muted", "d_muted"),
               clamp(p_inc * 4), 0.14)
    # lane 1: crates (a batch of 7 travels the lane once over p_full)
    if 0 < p_full < 1:
        for k in range(7):
            f = clamp(p_full * 1.6 - k * 0.09)
            if 0 < f < 1:
                bx, by = _along(lanes[0], f)
                c.fill_rrect(bx - 26, by - 22, 52, 44, 8, mix(acc, (1, 1, 1, 1), 0.15))
                c.line(bx - 26, by - 6, bx + 26, by - 6, (1, 1, 1, 1), 2, 0.6)
    # lane 2: steady stream of dots
    if p_inc > 0:
        n = int(10 * p_inc) + 1
        for k in range(n):
            f = (t * 0.45 + k / n) % 1.0
            px, py = _along(lanes[1], f)
            c.circle(px, py, 8, GREEN, min(1, f * 6, (1 - f) * 6))
    if open_badge > 0:
        bx, by = src["x"] + src["w"] - 18, src["y"] - 18
        with c.at(0, 0, max(0.01, pop(clamp(open_badge))), origin=(bx, by)):
            c.fill_rrect(bx - 90, by - 22, 110, 44, 22, GREEN)
            c.text(bx - 35, by + 8, "OPEN", tk.F["mono_bold"], 20, (1, 1, 1, 1), 1, 0.12, align="c")


# ── twin table ──────────────────────────────────────────────────────────
def twin_table(c, x, y, w, rows, row_h=96, titles=("LEGACY", "ALIBABA CLOUD")):
    """rows: [dict(name, count, h_left, h_right, slide, lock, bad=None|index, fix=0..1)].
    Right row slides in (slide), then locks to the left row (lock): green link + check.
    bad = index of a wrong char in h_right (red) until fix → shows the correct char."""
    gap = 70
    cw = (w - gap) / 2
    lx, rx = x, x + cw + gap
    hdr = 64
    total_h = hdr + row_h * len(rows) + 20
    c.card(lx, y, cw, total_h, r=24)
    c.card(rx, y, cw, total_h, r=24)
    for cx_, title in ((lx, titles[0]), (rx, titles[1])):
        c.text(cx_ + 24, y + 42, title, tk.F["mono_bold"], 19, c.theme("muted", "d_muted"), 1, 0.16)
        c.line(cx_ + 1, y + hdr, cx_ + cw - 1, y + hdr, c.theme("line", "d_line"), 1)
    ink, muted = c.theme("ink", "d_ink"), c.theme("muted", "d_muted")
    for i, r in enumerate(rows):
        ry = y + hdr + 10 + i * row_h
        # left (legacy) row
        c.text(lx + 24, ry + 38, r["name"], tk.F["mono_med"], 24, ink, 1, 0.02)
        c.text(lx + 24, ry + 72, f"{r['count']} rows", tk.F["mono"], 18, muted, 1)
        c.text(lx + cw - 24, ry + 72, r["h_left"], tk.F["mono"], 18, muted, 1, align="r")
        # right (cloud) row slides in
        s = glide(clamp(r.get("slide", 0)))
        if s <= 0.01:
            continue
        ox = 160 * (1 - s)
        a = clamp(s * 2)
        c.text(rx + 24 + ox, ry + 38, r["name"], tk.F["mono_med"], 24, ink, a, 0.02)
        c.text(rx + 24 + ox, ry + 72, f"{r['count']} rows", tk.F["mono"], 18, muted, a)
        hr = r["h_right"]
        bad, fix = r.get("bad"), clamp(r.get("fix", 0))
        hx = rx + cw - 24 + ox
        if bad is not None and fix < 1:
            # draw char by char from the right edge so the wrong char can be red
            shown = hr[:bad] + (hr[bad] if fix < 0.5 else r["h_left"][bad]) + hr[bad + 1:]
            tw = c.measure(shown, tk.F["mono"], 18)[0]
            pre_w = c.measure(shown[:bad], tk.F["mono"], 18)[0]
            c.text(hx - tw, ry + 72, shown, tk.F["mono"], 18, muted, a)
            cw_ = c.measure(shown[bad], tk.F["mono"], 18)[0]
            c.fill_rrect(hx - tw + pre_w - 3, ry + 52, cw_ + 6, 28, 5, tk.C["rec"], a * (1 - fix))
            c.text(hx - tw + pre_w, ry + 72, shown[bad], tk.F["mono_bold"], 18, (1, 1, 1, 1), a * (1 - fix))
        else:
            c.text(hx, ry + 72, hr if bad is None else r["h_left"], tk.F["mono"], 18, muted, a, align="r")
        lk = clamp(r.get("lock", 0))
        if lk > 0:
            col = GREEN
            c.stroke_rrect(lx + 10, ry, cw - 20, row_h - 12, 14, col, 2.5, lk)
            c.stroke_rrect(rx + 10, ry, cw - 20, row_h - 12, 14, col, 2.5, lk)
            mx, my = x + cw + gap / 2, ry + (row_h - 12) / 2
            c.line(lx + cw - 10, my, lx + cw - 10 + (gap + 20) * glide(lk), my, col, 4, lk)
            pk = pop(lk, 1.8)
            with c.at(0, 0, max(0.01, pk), origin=(mx, my)):
                c.circle(mx, my, 22, col)
                icons.check(c, mx, my, 20, (1, 1, 1, 1), 3.5)
        elif bad is not None and r.get("slide", 0) >= 1 and fix < 1:
            mx, my = x + cw + gap / 2, ry + (row_h - 12) / 2
            c.circle(mx, my, 22, tk.C["rec"])
            c.line(mx - 8, my - 8, mx + 8, my + 8, (1, 1, 1, 1), 3.5)
            c.line(mx - 8, my + 8, mx + 8, my - 8, (1, 1, 1, 1), 3.5)
    return total_h


# ── cutover switch ──────────────────────────────────────────────────────
def cutover_switch(c, t, x, y, w, h, p_flip=0.0, p_rollback=0.0, flow=1.0):
    """App on top; fork to legacy (left) and Alibaba Cloud (right). Lever flips left→right with p_flip.
    After the flip the legacy track turns dashed and gets a 'rollback plan' label (p_rollback)."""
    app = dict(x=x + w / 2 - 150, y=y, w=300, h=100, kind="svc", label="app")
    legacy = dict(x=x, y=y + h - 110, w=330, h=110, kind="svc", label="legacy")
    cloud = dict(x=x + w - 330, y=y + h - 110, w=330, h=110, kind="svc", label="Alibaba Cloud")
    fork = (x + w / 2, y + 230)
    top = (x + w / 2, y + 100)
    to_l = [fork, (legacy["x"] + legacy["w"] / 2, fork[1] + 120), (legacy["x"] + legacy["w"] / 2, legacy["y"])]
    to_c = [fork, (cloud["x"] + cloud["w"] / 2, fork[1] + 120), (cloud["x"] + cloud["w"] / 2, cloud["y"])]
    flip = in_out_cubic(clamp(p_flip))
    faint, acc = c.theme("faint", "d_line"), c.theme("accent", "d_accent")
    _draw_poly(c, [top, fork], 1, faint, 10)
    # legacy track: solid before, dashed (rollback) after
    if flip < 1:
        _draw_poly(c, to_l, 1, faint, 10, 1 - flip)
    if flip > 0:
        c.ctx.set_dash([14, 12])
        _draw_poly(c, to_l, 1, c.theme("muted", "d_muted"), 4, flip)
        c.ctx.set_dash([])
    _draw_poly(c, to_c, 1, faint, 10)
    # packets on the active track
    active = to_l if flip < 0.5 else to_c
    for k in range(5):
        f = (t * 0.6 + k / 5) % 1.0
        px, py = _along([top, fork] + active[1:], f)
        col = acc if flip < 0.5 else GREEN
        c.circle(px, py, 9, col, flow * min(1, f * 6, (1 - f) * 6) * (1 - math.sin(math.pi * flip) * 0.9))
    # lever
    ang = lerp(-0.6, 0.6, flip)
    c.circle(fork[0], fork[1], 26, c.theme("ink", "d_ink"))
    c.line(fork[0], fork[1], fork[0] + 110 * math.sin(ang), fork[1] + 110 * math.cos(ang), c.theme("ink", "d_ink"), 10)
    c.circle(fork[0] + 110 * math.sin(ang), fork[1] + 110 * math.cos(ang), 20, GREEN if flip > 0.5 else acc)
    for nd in (app, legacy, cloud):
        arch_node(c, nd)
    if p_rollback > 0:
        mx, my = to_l[1][0] + 10, to_l[1][1] - 30
        c.text(mx, my, "ROLLBACK PLAN", tk.F["mono_bold"], 20, c.theme("muted", "d_muted"), glide(clamp(p_rollback)), 0.14)
        c.text(mx, my + 30, "← jalan balik siap", tk.F["serif"], 32, acc, glide(clamp(p_rollback)))


# ── padlock ─────────────────────────────────────────────────────────────
def padlock(c, cx, cy, s, p_open=0.0, color=None):
    """Padlock; shackle lifts and swings open with p_open."""
    color = color or c.theme("ink", "d_ink")
    o = in_out_cubic(clamp(p_open))
    bw, bh = s, s * 0.78
    c.ctx.save()
    c.ctx.translate(cx + s * 0.28, cy - bh * 0.1 - s * 0.18 * o)
    c.ctx.rotate(-0.7 * o)
    c.ctx.translate(-(cx + s * 0.28), -(cy - bh * 0.1))
    c.ctx.new_path()
    c.ctx.arc(cx, cy - bh * 0.1, s * 0.28, math.pi, 2 * math.pi)
    c.ctx.line_to(cx + s * 0.28, cy + bh * 0.05)
    c.ctx.move_to(cx - s * 0.28, cy - bh * 0.1)
    c.ctx.line_to(cx - s * 0.28, cy + bh * 0.05)
    c.src(color)
    c.ctx.set_line_width(s * 0.11)
    c.ctx.set_line_cap(1)
    c.ctx.stroke()
    c.ctx.restore()
    c.fill_rrect(cx - bw / 2, cy, bw, bh, s * 0.14, mix(color, GREEN, o))
    c.circle(cx, cy + bh * 0.42, s * 0.08, c.theme("card", "d_card"))


# ── series bumper ───────────────────────────────────────────────────────
def series_bumper(c, t, t0, t1, ep, sub, color, title=("BONGKAR", "ARSITEKTUR")):
    """Full-bleed color panel that wipes up at t0, holds, wipes out ending at t1 (draw at z >= 100)."""
    pin = glide(prog(t, t0, 0.4))
    pout = in_cubic(prog(t, t1 - 0.35, 0.35))
    top = tk.H * (1 - pin) - tk.H * pout
    c.src(color)
    c.ctx.rectangle(0, top, tk.W, tk.H)
    c.ctx.fill()
    a = glide(prog(t, t0 + 0.15, 0.4)) * (1 - pout)
    x = tk.L["col_x"]
    with c.layer((0, 0, tk.W, tk.H), a, 10 * (1 - out_expo(prog(t, t0 + 0.15, 0.4)))):
        c.text(x, 760, title[0], tk.F["display"], 150, (1, 1, 1, 1), 1, -0.06)
        c.text(x, 900, title[1], tk.F["display"], 150, (1, 1, 1, 1), 1, -0.06)
        c.text(x, 1010, f"EP {ep:02d}", tk.F["mono_bold"], 40, (1, 1, 1, 1), 0.85, 0.2)
        c.text(x, 1090, sub, tk.F["ui"], 34, (1, 1, 1, 1), 0.8, -0.01)
