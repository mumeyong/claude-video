"""Serverless / kitchen explainer components (first used in Bongkar Arsitektur EP03).

flame · burner · oven · order_ticket · ticket_rail · dag_flow · lake_pantry · server_rack
Pure drawing from explicit progress values and t; flicker/blink is a deterministic function of t + seed.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, glide, pop
from .infra import _h
from . import icons

ORANGE = tk.CHAPTER[2][0]
WHITE = (1, 1, 1, 1)


# ── flame ───────────────────────────────────────────────────────────────
def _tongue(c, cx, cy, H, r, sway, color, alpha=1.0):
    """Teardrop: round bottom (radius r) at cy, tip H above, tip shifted by sway."""
    if H <= r or r <= 0.5:
        return
    tx, ty = cx + sway, cy - H
    k = H - r
    cx_ = c.ctx
    cx_.new_path()
    cx_.move_to(tx, ty)
    cx_.curve_to(tx + r * 0.25, ty + k * 0.45, cx + r, cy - r - k * 0.35, cx + r, cy - r)
    cx_.arc(cx, cy - r, r, 0, math.pi)
    cx_.curve_to(cx - r, cy - r - k * 0.35, tx - r * 0.25, ty + k * 0.45, tx, ty)
    cx_.close_path()
    c.src(color, alpha)
    cx_.fill()


def flame(c, cx, cy, size, p, t, seed=0, hot=0.0, color=None):
    """Flame standing on (cx, cy). size = full height at p=1. p 0..1 grows/shrinks it (0 = nothing at all).
    hot 0..1 tints toward red (overloaded)."""
    p = clamp(p)
    if p <= 0.01:
        return
    col = mix(color or ORANGE, tk.C["rec"], clamp(hot))
    core = mix(col, WHITE, 0.6)
    fl = 1 + 0.07 * math.sin(t * 11 + seed) + 0.05 * math.sin(t * 17.3 + seed * 2.1)
    H = size * p * fl
    r = size * 0.24 * (0.45 + 0.55 * p)
    sway = r * 0.35 * math.sin(t * 6.5 + seed * 1.3)
    c.shadow(cx - r * 2, cy - H * 0.8, r * 4, H * 0.8, r * 2, 40, 0, 0.22 * p, col)
    for side in (-1, 1):
        fs = 1 + 0.12 * math.sin(t * 9 + seed + side * 2)
        _tongue(c, cx + side * r * 0.55, cy, H * 0.62 * fs, r * 0.62, sway * 1.4 + side * r * 0.3, col, 0.85)
    _tongue(c, cx, cy, H, r, sway, col)
    _tongue(c, cx, cy - r * 0.08, H * 0.52, r * 0.55, sway * 0.6, core)


# ── burner (stove, side view) ───────────────────────────────────────────
def burner(c, cx, cy, s, fire, t, seed=0, hot=0.0, label=None, label_a=1.0, cold=0.0):
    """Stove whose top surface is at y=cy; flame rises from it. fire 0..1 = flame size; the knob turns with it.
    cold 0..1 greys the body (a stove that has no flame and no gas line). label under the body (mono)."""
    bh = s * 0.34
    body = mix(c.theme("card", "d_card"), c.theme("faint", "d_line"), 0.35 * cold)
    ink2 = c.theme("ink2", "d_muted")
    c.shadow(cx - s / 2, cy, s, bh, s * 0.07, 26, 12, 0.10)
    c.fill_rrect(cx - s / 2, cy, s, bh, s * 0.07, body)
    c.stroke_rrect(cx - s / 2, cy, s, bh, s * 0.07, c.theme("line", "d_line"), 1.5)
    c.fill_rrect(cx - s / 2 + s * 0.06, cy + bh * 0.62, s * 0.5, bh * 0.14, bh * 0.07, c.theme("line", "d_line"))
    # knob turns with the fire
    kx, ky, kr = cx + s * 0.33, cy + bh * 0.52, bh * 0.24
    c.circle(kx, ky, kr, mix(ink2, ORANGE, clamp(fire * 3)))
    ang = -math.pi / 2 + 1.4 * clamp(fire * 3)
    c.line(kx, ky, kx + kr * 0.75 * math.cos(ang), ky + kr * 0.75 * math.sin(ang), WHITE, max(2, kr * 0.22))
    # burner head + grate prongs
    c.fill_rrect(cx - s * 0.26, cy - s * 0.045, s * 0.52, s * 0.05, s * 0.02, ink2)
    for dx in (-0.36, 0.36):
        c.line(cx + s * dx, cy, cx + s * dx * 0.9, cy - s * 0.07, ink2, max(2, s * 0.02))
    flame(c, cx, cy - s * 0.04, s * 0.62, fire, t, seed, hot)
    if label and label_a > 0:
        c.text(cx, cy + bh + 34, label, tk.F["mono_med"], max(16, s * 0.085), c.theme("muted", "d_muted"),
               label_a, 0.08, align="c")


# ── oven (batch) ────────────────────────────────────────────────────────
def oven(c, cx, cy, s, heat, t, seed=0):
    """Square oven centered on (cx, cy); the window glows orange with heat 0..1 (gentle pulse)."""
    w, h = s, s * 0.82
    x, y = cx - w / 2, cy - h / 2
    ink2 = c.theme("ink2", "d_muted")
    c.fill_rrect(x, y, w, h, s * 0.09, c.theme("card", "d_card"))
    c.stroke_rrect(x, y, w, h, s * 0.09, ink2, max(2, s * 0.025))
    for k in range(3):
        c.circle(x + w * (0.25 + 0.25 * k), y + h * 0.13, s * 0.035, mix(ink2, ORANGE, clamp(heat * 2)))
    wx, wy, ww, wh = x + w * 0.14, y + h * 0.27, w * 0.72, h * 0.58
    c.fill_rrect(wx, wy, ww, wh, s * 0.05, c.theme("line", "d_line"))
    glow = clamp(heat) * (0.82 + 0.18 * math.sin(t * 3.2 + seed))
    if glow > 0.01:
        c.shadow(wx, wy, ww, wh, s * 0.05, 30, 0, 0.35 * glow, ORANGE)
        c.fill_rrect(wx, wy, ww, wh, s * 0.05, ORANGE, 0.85 * glow)
        c.fill_rrect(wx + ww * 0.12, wy + wh * 0.62, ww * 0.76, wh * 0.08, wh * 0.04, WHITE, 0.5 * glow)


# ── order ticket + rail ─────────────────────────────────────────────────
def order_ticket(c, x, y, w, h, title, lines=(), alpha=1.0, rot=0.0, done=0.0):
    """Paper kitchen ticket hanging from (x + w/2, y). Mono title, serif 'handwritten' lines, zigzag bottom."""
    if alpha <= 0.002:
        return
    with c.at(0, 0, 1.0, origin=(x + w / 2, y), rot=rot):
        with c.group(alpha):
            c.shadow(x, y, w, h, 6, 18, 8, 0.12)
            cx_ = c.ctx
            cx_.new_path()
            cx_.move_to(x, y)
            cx_.line_to(x + w, y)
            cx_.line_to(x + w, y + h)
            n = 7
            for k in range(n):
                cx_.line_to(x + w - (k + 0.5) * w / n, y + h - 12)
                cx_.line_to(x + w - (k + 1) * w / n, y + h)
            cx_.close_path()
            c.src(c.theme("card", "d_card"))
            cx_.fill()
            c.fill_rrect(x, y, w, 10, 2, ORANGE)
            c.circle(x + w / 2, y + 24, 6, c.theme("faint", "d_line"))
            c.text(x + 16, y + 62, title, tk.F["mono_bold"], 19, c.theme("ink", "d_ink"), 1, 0.06)
            for i, ln in enumerate(lines):
                c.text(x + 16, y + 104 + i * 34, ln, tk.F["serif"], min(32, w * 0.2), c.theme("ink2", "d_muted"), 1)
            if done > 0:
                p = pop(clamp(done), 1.8)
                bx, by = x + w - 26, y + 44
                with c.at(0, 0, max(0.01, p), origin=(bx, by)):
                    c.circle(bx, by, 18, tk.C["ok"])
                    icons.check(c, bx, by, 16, WHITE, 3)


def ticket_rail(c, x, y, w, tickets, tw=150, th=190, alpha=1.0):
    """Rail at y with tickets: [dict(x, title, lines, p, rot, done, drop)].
    p 0..1 drops the ticket onto the rail; drop = (dy, fade) moves it down off the rail (into a burner)."""
    c.fill_rrect(x, y - 6, w, 12, 6, c.theme("faint", "d_line"), alpha)
    c.fill_rrect(x, y - 6, w, 4, 2, WHITE, 0.6 * alpha)
    for tkt in tickets:
        p = clamp(tkt.get("p", 1.0))
        if p <= 0:
            continue
        dy, fade = tkt.get("drop", (0.0, 0.0))
        ty = y - 4 - 140 * (1 - pop(p, 1.4)) + dy
        rot = tkt.get("rot", 0.0) * (0.3 + 0.7 * p)
        order_ticket(c, tkt["x"] - tw / 2, ty, tw, th, tkt["title"], tkt.get("lines", ()),
                     alpha * clamp(p * 3) * (1 - clamp(fade)), rot, tkt.get("done", 0.0))
        if dy < 4:
            c.fill_rrect(tkt["x"] - 10, y - 10, 20, 20, 6, c.theme("ink2", "d_muted"), alpha * clamp(p * 3))


# ── Airflow DAG band ────────────────────────────────────────────────────
def dag_flow(c, x, y, w, tasks, p=1.0, title="AIRFLOW · DAG", sub="schedule: daily", box_h=80, alpha=1.0):
    """tasks: [dict(label, run 0..1, done 0..1)]. Boxes left→right with arrows drawn by p.
    waiting = muted outline · running = orange outline + progress bar · done = green ✓. Returns total height."""
    n = len(tasks)
    gap, pad, hdr = 40, 28, 56
    bw = (w - 2 * pad - gap * (n - 1)) / n
    total = hdr + box_h + pad
    c.card(x, y, w, total, r=24, alpha=alpha)
    muted, ink = c.theme("muted", "d_muted"), c.theme("ink", "d_ink")
    c.text(x + pad, y + 38, title, tk.F["mono_bold"], 18, muted, alpha, 0.16)
    c.text(x + w - pad, y + 38, sub, tk.F["mono"], 17, muted, alpha, 0.04, align="r")
    by = y + hdr
    for i, tsk in enumerate(tasks):
        bx = x + pad + i * (bw + gap)
        a = alpha * clamp((p * (n + 1) - i) * 1.5)
        if a <= 0.002:
            continue
        run, done = clamp(tsk.get("run", 0)), clamp(tsk.get("done", 0))
        if i > 0:
            ax0, ax1, ay = bx - gap + 6, bx - 8, by + box_h / 2
            c.line(ax0, ay, ax1, ay, c.theme("faint", "d_line"), 3, a)
            c.line(ax1, ay, ax1 - 9, ay - 7, c.theme("faint", "d_line"), 3, a)
            c.line(ax1, ay, ax1 - 9, ay + 7, c.theme("faint", "d_line"), 3, a)
        green = tk.C["ok"]
        fill = mix(c.theme("card", "d_card"), green, 0.12 * done)
        c.fill_rrect(bx, by, bw, box_h, 16, fill, a)
        edge = mix(mix(c.theme("faint", "d_line"), ORANGE, clamp(run * 8)), green, done)
        c.stroke_rrect(bx, by, bw, box_h, 16, edge, 2.5, a)
        c.text(bx + bw / 2, by + box_h / 2 + 7 - (6 if 0 < run < 1 and done < 1 else 0), tsk["label"],
               tk.F["mono_med"], 19 if bw > 150 else 17, mix(muted, ink, clamp(run * 8)), a, 0.0, align="c")
        if 0 < run and done < 1:
            c.fill_rrect(bx + 14, by + box_h - 20, bw - 28, 6, 3, c.theme("line", "d_line"), a)
            c.fill_rrect(bx + 14, by + box_h - 20, (bw - 28) * run, 6, 3, ORANGE, a)
        if done > 0:
            pk = pop(done, 1.8)
            cx_, cy_ = bx + bw - 4, by + 4
            with c.at(0, 0, max(0.01, pk), origin=(cx_, cy_)):
                c.circle(cx_, cy_, 16, green, a)
                icons.check(c, cx_, cy_, 14, WHITE, 3, alpha=a)
    return total


def dag_state(t, t0, n, step=0.55):
    """Tasks that run one after another from t0: list of (run, done) for n tasks."""
    out = []
    for i in range(n):
        s = t0 + i * step
        out.append((clamp((t - s) / (step * 0.8)), glide(clamp((t - s - step * 0.8) / 0.25))))
    return out


# ── Paimon pantry (data lake) ───────────────────────────────────────────
def lake_pantry(c, x, y, w, h, t, title="Paimon", sub="DATA LAKE · TABLES", tables=(), p_tables=1.0, level=1.0):
    """Data-lake card: animated water in the lower half and table 'jars' standing on it (stagger by p_tables)."""
    c.card(x, y, w, h, r=26)
    c.text(x + 32, y + 62, title, tk.F["display_semi"], 46, c.theme("ink", "d_ink"), 1, -0.03)
    c.text(x + w - 32, y + 56, sub, tk.F["mono_med"], 17, c.theme("muted", "d_muted"), 1, 0.14, align="r")
    acc = c.theme("accent", "d_accent")
    wy = y + h * (1 - 0.42 * clamp(level))
    with c.clip(x + 1, y + 1, w - 2, h - 2, 25):
        for k, (amp, sp, a) in enumerate(((10, 1.3, 0.10), (7, -1.8, 0.16))):
            cx_ = c.ctx
            cx_.new_path()
            cx_.move_to(x, y + h)
            for i in range(41):
                px = x + w * i / 40
                cx_.line_to(px, wy + 10 * k + amp * math.sin(i * 0.5 + t * sp + k))
            cx_.line_to(x + w, y + h)
            cx_.close_path()
            c.src(acc, a)
            cx_.fill()
    n = len(tables)
    if n:
        jw = min(200, (w - 64 - 20 * (n - 1)) / n)
        for i, name in enumerate(tables):
            p = pop(clamp(p_tables * (n + 1) - i), 1.6)
            if p <= 0.01:
                continue
            jx = x + 32 + i * (jw + 20)
            jy = wy - 70 + 4 * math.sin(t * 1.4 + i)
            with c.at(0, 30 * (1 - p), 1.0, origin=(jx + jw / 2, jy)):
                with c.group(clamp(p * 2)):
                    c.fill_rrect(jx, jy, jw, 70, 16, c.theme("card", "d_card"))
                    c.stroke_rrect(jx, jy, jw, 70, 16, ORANGE, 2.5)
                    c.fill_rrect(jx + 16, jy + 16, 10, 38, 5, ORANGE)
                    c.text(jx + 38, jy + 44, name, tk.F["mono_med"], 20, c.theme("ink", "d_ink"), 1, 0.0)


# ── server rack ─────────────────────────────────────────────────────────
def server_rack(c, x, y, w, h, t, units=6, on=1.0, seed=0, label=None, dashed=False, alpha=1.0):
    """Rack of 1U servers with seeded blinking LEDs. on 0..1 fades LEDs out (0 = retired, grey).
    dashed = empty placeholder outline only."""
    if alpha <= 0.002:
        return
    muted = c.theme("muted", "d_muted")
    if dashed:
        c.stroke_rrect(x, y, w, h, 22, c.theme("faint", "d_line"), 3, alpha, dash=[14, 12])
        return
    with c.group(alpha):
        c.card(x, y, w, h, r=22)
        top = y + (52 if label else 24)
        if label:
            c.text(x + 24, y + 38, label, tk.F["mono_bold"], 17, muted, 1, 0.16)
        uh = (y + h - 24 - top) / units
        for u in range(units):
            uy = top + u * uh
            c.fill_rrect(x + 20, uy + 6, w - 40, uh - 12, 10, c.theme("line", "d_line"))
            for k in range(3):
                c.fill_rrect(x + 40 + k * 22, uy + uh / 2 - 3, 14, 6, 3, c.theme("faint", "d_line"))
            for k in range(2):
                ph = _h(u * 7 + k, seed)
                lit = 1.0 if (t * (0.7 + 1.6 * ph) + ph) % 1.0 < 0.62 else 0.35
                col = mix(c.theme("faint", "d_line"), tk.C["ok"] if k == 0 else ORANGE, clamp(on) * lit)
                c.circle(x + w - 46 - k * 26, uy + uh / 2, 7, col)
