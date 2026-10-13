"""Payday / detective components (first used in "kenapa-bank-down-gajian").

tear_calendar · suspect_card · red_string · cashier · ledger · paper_sheet · queue_dots
Signature move they share: a sheet gets torn off (calendar page, cleared suspect card, ledger photocopy).
Pure functions of their progress values and t; all variation is hash-seeded.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, prog, glide
from .infra import _draw_poly, _along, _h

RED = tk.CHAPTER[5][0]
WHITE = (1, 1, 1, 1)


def _zigzag_top(cx, x, y, w, n=14, d=7):
    """Path piece: torn/perforated top edge from (x, y) to (x + w, y)."""
    cx.move_to(x, y)
    for k in range(n):
        cx.line_to(x + (k + 0.5) * w / n, y + d * (0.4 + 0.6 * _h(k, 5)))
        cx.line_to(x + (k + 1) * w / n, y)


def torn_flight(p, w, h):
    """(dx, dy, rot, alpha) of a sheet torn off and falling away, p 0..1 (gravity: dy ~ p²)."""
    p = clamp(p)
    return w * 0.45 * p, h * 1.6 * p * p - h * 0.12 * math.sin(math.pi * p), 0.75 * p, 1 - p ** 3


# ── desk tear-off calendar ──────────────────────────────────────────────
def _cal_page(c, x, y, w, h, num, color, circle_p=0.0, sub="", sub_p=0.0, torn=False):
    cx = c.ctx
    c.shadow(x, y, w, h, 10, 18, 6, 0.08)
    cx.new_path()
    if torn:
        _zigzag_top(cx, x, y, w)
    else:
        cx.move_to(x, y)
        cx.line_to(x + w, y)
    cx.line_to(x + w, y + h - 10)
    cx.arc(x + w - 10, y + h - 10, 10, 0, math.pi / 2)
    cx.line_to(x + 10, y + h)
    cx.arc(x + 10, y + h - 10, 10, math.pi / 2, math.pi)
    cx.close_path()
    c.src(c.theme("card", "d_card"))
    cx.fill()
    size = h * 0.56
    ncol = color if num >= 25 else c.theme("ink", "d_ink")
    c.text(x + w / 2, y + h * 0.62, str(num), tk.F["display"], size, ncol, 1, -0.05, align="c")
    if sub and sub_p > 0:
        c.text(x + w / 2, y + h * 0.88, sub, tk.F["mono_bold"], max(17, h * 0.085), c.theme("ink2", "d_muted"),
               glide(clamp(sub_p)), 0.12, align="c")
    if circle_p > 0:
        # hand-drawn marker loop: overshoots its start, radius wobbles (deterministic)
        mx, my = x + w / 2, y + h * 0.43
        rx, ry = w * 0.4, h * 0.3
        n = 60
        pts = []
        for i in range(n + 1):
            u = i / n
            a = -2.2 + u * (2 * math.pi + 0.7)
            k = 1 + 0.06 * math.sin(u * 9 + 1.3) + 0.05 * u
            pts.append((mx + rx * k * math.cos(a), my + ry * k * math.sin(a) - 4 * u))
        _draw_poly(c, pts, clamp(circle_p), color, max(4, w * 0.022), 0.9)


def tear_calendar(c, x, y, w, h, t, t0, start=21, end=25, step=0.2, month="OKTOBER", color=None, circle_p=0.0,
                  sub="", sub_p=0.0):
    """Desk tear-off calendar: color header band with the month, two rings, page with the date.
    Pages start..end-1 are torn off one by one from t0 (every `step` s, 0.5 s flight) until `end` shows.
    circle_p 0..1 draws a hand marker loop around the date; sub (e.g. '09.01') fades in under it with sub_p."""
    color = color or RED
    hb = h * 0.2
    py, ph = y + hb, h - hb
    # thickness: page edges peeking out under the stack
    for k in (2, 1):
        c.fill_rrect(x + k * 3, y + h - 8 + k * 5, w - k * 6, 10, 4, c.theme("faint", "d_line"), 0.8)
    c.shadow(x, y, w, h, 16, 30, 12, 0.10)
    c.fill_rrect(x, y, w, h, 16, c.theme("card", "d_card"))
    torn_n = sum(1 for k in range(end - start) if t >= t0 + k * step)
    shown = start + torn_n
    _cal_page(c, x, py, w, ph, shown, color, circle_p if shown == end else 0.0, sub if shown == end else "",
              sub_p, torn=torn_n > 0)
    # header band + rings (drawn over the page top)
    c.fill_rrect(x, y, w, hb + 14, 16, color)
    c.fill_rrect(x, y + hb - 2, w, 16, 0, color)
    c.text(x + w / 2, y + hb * 0.66, month, tk.F["mono_bold"], max(17, hb * 0.32), WHITE, 1, 0.22, align="c")
    for rx in (x + w * 0.24, x + w * 0.76):
        c.fill_rrect(rx - 7, y - 16, 14, 34, 7, c.theme("ink2", "d_muted"))
    # pages in flight
    for k in range(end - start):
        tk_ = t0 + k * step
        p = prog(t, tk_, 0.5)
        if 0 < p < 1:
            dx, dy, rot, a = torn_flight(p, w, ph)
            with c.at(dx, dy, 1.0, origin=(x, py + 6), rot=rot):
                with c.group(a):
                    _cal_page(c, x, py, w, ph, start + k, color, torn=True)


# ── suspect board ───────────────────────────────────────────────────────
def pin(c, x, y, r=13, color=None):
    """Push pin seen from above: colored head + highlight."""
    color = color or RED
    c.shadow(x - r, y - r + 4, 2 * r, 2 * r, r, 8, 4, 0.18)
    c.circle(x, y, r, color)
    c.circle(x - r * 0.3, y - r * 0.3, r * 0.32, WHITE, 0.55)


def suspect_card(c, x, y, w, h, num, name, label, icon=None, reveal=1.0, tear=0.0, rot=0.0, focus=0.0, dim=0.0,
                 color=None):
    """Polaroid-style suspect card pinned at its top center.
    icon(c, box) draws the 'photo' (box = x, y, w, h); before reveal the photo is a big '?'.
    tear 0..1: the card is ripped off the board (a scrap stays under the pin) and falls away.
    focus 0..1: red frame; dim 0..1: fades the card back. Returns the pin point."""
    color = color or RED
    px, py = x + w / 2, y + 18
    if tear > 0:
        # scrap left under the pin
        cx = c.ctx
        cx.new_path()
        cx.move_to(px - 34, y)
        cx.line_to(px + 30, y)
        cx.line_to(px + 22, y + 30)
        cx.line_to(px + 4, y + 38)
        cx.line_to(px - 18, y + 28)
        cx.close_path()
        c.src(c.theme("card", "d_card"))
        cx.fill()
    if tear < 1:
        dx, dy, trot, a = torn_flight(tear, w, h) if tear > 0 else (0, 0, 0, 1)
        with c.at(dx, dy, 1.0, origin=(px, py), rot=rot + trot * 0.8):
            with c.group(a * (1 - 0.55 * clamp(dim))):
                c.card(x, y, w, h, r=10)
                ph_x, ph_y, ph_w, ph_h = x + 18, y + 44, w - 36, h * 0.56
                c.fill_rrect(ph_x, ph_y, ph_w, ph_h, 6, mix(c.theme("bg", "d_bg"), color, 0.06))
                c.text(ph_x + 14, ph_y + 30, f"#{num:02d}", tk.F["mono_bold"], 18, c.theme("muted", "d_muted"), 1, 0.12)
                q = 1 - clamp(reveal * 2)
                if q > 0:
                    c.text(ph_x + ph_w / 2, ph_y + ph_h * 0.7, "?", tk.F["display"], ph_h * 0.62,
                           c.theme("faint", "d_line"), q, align="c")
                ra = clamp(reveal * 2 - 1)
                if ra > 0 and icon:
                    with c.group(ra):
                        icon(c, (ph_x, ph_y, ph_w, ph_h))
                if ra > 0:
                    c.text(x + 22, ph_y + ph_h + 58, name, tk.F["display"], 46, c.theme("ink", "d_ink"), ra, -0.04)
                    tw = c.measure(label, tk.F["mono_bold"], 19, 0.08)[0] + 26
                    c.fill_rrect(x + 22, ph_y + ph_h + 82, tw, 36, 18, tk.C["accent"], 0.1 * ra)
                    c.text(x + 35, ph_y + ph_h + 106, label, tk.F["mono_bold"], 19, tk.C["accent"], ra, 0.08)
                if focus > 0:
                    c.stroke_rrect(x - 8, y - 8, w + 16, h + 16, 16, color, 4, clamp(focus))
    pin(c, px, py, color=color)
    return px, py


def red_string(c, pts, p, sag=46, color=None, width=3):
    """Detective string through the pins, sagging between them; p 0..1 draws it left→right."""
    if p <= 0 or len(pts) < 2:
        return
    color = color or RED
    path = []
    for j, ((ax, ay), (bx, by)) in enumerate(zip(pts, pts[1:])):
        for i in range(0 if j == 0 else 1, 25):
            u = i / 24
            path.append((ax + (bx - ax) * u, ay + (by - ay) * u + sag * 4 * u * (1 - u)))
    _draw_poly(c, path, clamp(p), color, width, 0.9)


# ── supermarket checkout (top-down) ─────────────────────────────────────
def cashier(c, cx, cy, s, t, busy=1.0, seed=0, color=None, alpha=1.0):
    """Checkout counter seen from above, centered on (cx, cy), width s: belt with items moving, register, cashier.
    busy 0..1 = how fast the belt runs and how full it is."""
    if alpha <= 0.002:
        return
    color = color or RED
    w, h = s, s * 0.46
    x, y = cx - w / 2, cy - h / 2
    ink2 = c.theme("ink2", "d_muted")
    with c.group(alpha):
        c.shadow(x, y, w, h, s * 0.08, 12, 5, 0.08)
        c.fill_rrect(x, y, w, h, s * 0.08, c.theme("card", "d_card"))
        c.stroke_rrect(x, y, w, h, s * 0.08, c.theme("line", "d_line"), 1.5)
        # belt
        bx, by, bw, bh = x + w * 0.06, y + h * 0.22, w * 0.6, h * 0.4
        c.fill_rrect(bx, by, bw, bh, bh * 0.25, mix(c.theme("faint", "d_line"), ink2, 0.15))
        with c.clip(bx, by, bw, bh, bh * 0.25):
            for k in range(3):
                f = (t * 0.35 * (0.4 + busy) + k / 3 + _h(seed, 2)) % 1.0
                iw = bh * (0.55 + 0.3 * _h(k, seed))
                ix = bx + bw * f - iw
                ic = mix(color, c.theme("card", "d_card"), 0.35 + 0.4 * _h(k, seed + 1))
                c.fill_rrect(ix, by + bh * 0.2, iw, bh * 0.6, 3, ic, clamp(busy * 1.5))
        # register + cashier
        rx, ry, rs = x + w * 0.74, y + h * 0.16, h * 0.42
        c.fill_rrect(rx, ry, rs * 1.2, rs, 4, ink2)
        blink = 0.5 + 0.5 * math.sin(t * 5 + seed * 1.7)
        c.fill_rrect(rx + rs * 0.15, ry + rs * 0.18, rs * 0.9, rs * 0.4, 2, color, 0.4 + 0.6 * blink * busy)
        c.circle(x + w * 0.8, y + h + s * 0.09, s * 0.07, ink2)


def queue_dots(c, pts, t, n=6, speed=0.22, jam=0.0, r=9, seed=0, color=None, alpha=1.0):
    """People walking along polyline pts toward its end. jam 0..1: they slow down and bunch up near the end."""
    if alpha <= 0.002:
        return
    color = color or c.theme("ink2", "d_muted")
    sp = speed * (1 - 0.85 * clamp(jam))
    for i in range(n):
        f = (i / n + t * sp + _h(seed, 4)) % 1.0
        fj = 1 - (1 - f) ** (1 + 2.5 * clamp(jam))
        x, y = _along(pts, fj)
        a = clamp(f / 0.12) * clamp((1 - f) / 0.08 + clamp(jam))
        c.circle(x, y, r * (0.85 + 0.3 * _h(i, seed + 9)), color, a * alpha)


# ── ledger (buku kas) ───────────────────────────────────────────────────
def paper_sheet(c, x, y, w, h, rows=6, filled=1.0, alpha=1.0, torn=True, dashed=False, color=None):
    """One ledger sheet: torn top edge, ruled lines, mono 'entries' filled up to `filled` (0..1)."""
    if alpha <= 0.002:
        return
    color = color or RED
    cx = c.ctx
    with c.group(alpha):
        c.shadow(x, y, w, h, 6, 14, 6, 0.08)
        cx.new_path()
        if torn:
            _zigzag_top(cx, x, y, w, n=10, d=6)
        else:
            cx.move_to(x, y)
            cx.line_to(x + w, y)
        cx.line_to(x + w, y + h)
        cx.line_to(x, y + h)
        cx.close_path()
        c.src(c.theme("card", "d_card"))
        cx.fill_preserve()
        c.src(c.theme("line", "d_line"))
        cx.set_line_width(1.2)
        if dashed:
            c.src(color, 0.6)
            cx.set_dash([8, 6])
        cx.stroke()
        cx.set_dash([])
        _ledger_rows(c, x + w * 0.1, y + h * 0.18, w * 0.8, h * 0.74, rows, filled, color)


def _ledger_rows(c, x, y, w, h, rows, filled, color):
    rh = h / rows
    c.line(x + w * 0.62, y - rh * 0.3, x + w * 0.62, y + h - rh * 0.3, color, 1.5, 0.35)
    for i in range(rows):
        ly = y + i * rh
        c.line(x, ly + rh * 0.35, x + w, ly + rh * 0.35, c.theme("faint", "d_line"), 1, 0.9)
        a = clamp(filled * rows - i)
        if a > 0:
            lw = w * (0.3 + 0.25 * _h(i, 3)) * a
            c.line(x + 2, ly, x + 2 + lw, ly, c.theme("ink2", "d_muted"), max(2, rh * 0.16), 0.8)
            c.line(x + w * 0.7, ly, x + w * (0.78 + 0.18 * _h(i, 8)) * (0.85 + 0.15 * a), ly, color,
                   max(2, rh * 0.16), 0.8 * a)


def ledger(c, cx, cy, s, t, filled=1.0, hot=0.0, writing=0.0, title="BUKU KAS", color=None, alpha=1.0):
    """Open ledger book seen from above, centered on (cx, cy), width s. Cover in the signature color, two ruled pages.
    filled 0..1 = entries written; writing 0..1 = a pen scribbling a new entry; hot 0..1 = overloaded (red glow,
    pages blush, pen frantic). Title in mono on the spine tab."""
    if alpha <= 0.002:
        return
    color = color or RED
    w, h = s, s * 0.66
    x, y = cx - w / 2, cy - h / 2
    with c.group(alpha):
        if hot > 0:
            pulse = 0.75 + 0.25 * math.sin(t * 7)
            c.shadow(x - 10, y - 10, w + 20, h + 20, 24, 50, 0, 0.45 * clamp(hot) * pulse, color)
        c.shadow(x, y, w, h, 18, 30, 12, 0.12)
        c.fill_rrect(x - 10, y - 10, w + 20, h + 20, 20, mix(color, (0, 0, 0, 1), 0.15))
        pg = mix(c.theme("card", "d_card"), color, 0.10 * clamp(hot))
        for side in (0, 1):
            px = x + side * w / 2
            c.fill_rrect(px + (4 if side else 0), y, w / 2 - 4, h, 8, pg)
            _ledger_rows(c, px + w * 0.06, y + h * 0.16, w * 0.38, h * 0.76, 7,
                         clamp(filled * 2 - side), color)
        c.line(cx, y + 6, cx, y + h - 6, (0, 0, 0, 1), 2, 0.18)
        if writing > 0:
            fr = 3.0 + 6.0 * clamp(hot)
            px = x + w * 0.58 + w * 0.3 * (0.5 + 0.5 * math.sin(t * fr))
            py = y + h * (0.3 + 0.5 * ((t * 0.6) % 1.0))
            with c.group(clamp(writing)):
                c.line(px, py, px + s * 0.16, py - s * 0.2, c.theme("ink", "d_ink"), max(4, s * 0.025))
                c.circle(px, py, max(2.5, s * 0.01), c.theme("ink", "d_ink"))
        if title:
            tw = c.measure(title, tk.F["mono_bold"], 18, 0.12)[0] + 28
            c.fill_rrect(cx - tw / 2, y + h + 22, tw, 36, 8, color)
            c.text(cx, y + h + 46, title, tk.F["mono_bold"], 18, WHITE, 1, 0.12, align="c")
