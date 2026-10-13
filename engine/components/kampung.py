"""Kampung components (first used in "bongkar-ep04-monolith-event-driven").

kentongan · sound_rings · rumah · rumah_gede · gang · portal · ronda_man
Signature move: the kentongan (event) is struck → sound rings run down the gang → only the houses (functions) that
listen light up, work, and go dark again. Pure functions of their progress values and t; jitter is hash-seeded.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, out_cubic, in_out_cubic, glide
from .infra import _h

TEAL = tk.CHAPTER[4][0]
WHITE = (1, 1, 1, 1)


def _poly(c, pts, color, alpha=1.0):
    cx = c.ctx
    cx.new_path()
    cx.move_to(*pts[0])
    for p in pts[1:]:
        cx.line_to(*p)
    cx.close_path()
    c.src(color, alpha)
    cx.fill()


def _roof_color(c):
    return c.theme("ink2", "d_muted")


def _window(c, x, y, w, h, light, t, busy=0.0, broken=0.0, seed=0, color=None):
    """Window pane: dark glass → glowing signature color; busy = 3 bouncing work dots; broken = red + X."""
    color = color or TEAL
    glass = c.theme("faint", "d_line")
    lit = mix(color, tk.C["rec"], broken)
    if light > 0.01:
        c.circle(x + w / 2, y + h / 2, max(w, h) * 0.95, lit, 0.16 * light)
    c.fill_rrect(x, y, w, h, 6, mix(glass, lit, clamp(light)))
    c.line(x + w / 2, y + 4, x + w / 2, y + h - 4, c.theme("card", "d_card"), 3, 0.8)
    c.line(x + 4, y + h / 2, x + w - 4, y + h / 2, c.theme("card", "d_card"), 3, 0.8)
    if busy > 0.01 and broken < 0.5:
        for k in range(3):
            ph = (t * 2.4 + k * 0.33 + _h(seed, 3)) % 1.0
            dy = -abs(math.sin(ph * math.pi)) * h * 0.18
            c.circle(x + w * (0.3 + 0.2 * k), y + h * 0.72 + dy, max(3, w * 0.05), WHITE, busy)
    if broken > 0.01:
        m = min(w, h) * 0.28
        c.line(x + w / 2 - m, y + h / 2 - m, x + w / 2 + m, y + h / 2 + m, WHITE, 5, broken)
        c.line(x + w / 2 - m, y + h / 2 + m, x + w / 2 + m, y + h / 2 - m, WHITE, 5, broken)


def _spark(c, x, y, s, t, p, seed=0):
    """Short-circuit spark: jagged rays flickering around (x, y)."""
    if p <= 0.01:
        return
    red = tk.C["rec"]
    for k in range(6):
        ang = k / 6 * 2 * math.pi + _h(k, seed) * 0.6
        fl = 0.5 + 0.5 * math.sin(t * 31 + k * 2.1)
        r0, r1 = s * 0.35, s * (0.6 + 0.4 * fl)
        c.line(x + r0 * math.cos(ang), y + r0 * math.sin(ang), x + r1 * math.cos(ang), y + r1 * math.sin(ang),
               red, 4, p * (0.4 + 0.6 * fl))


# ── kentongan + rings ───────────────────────────────────────────────────
def kentongan(c, cx, top_y, s, hit=0.0, color=None, alpha=1.0, label=None):
    """Bamboo slit drum hanging from a pos-ronda post. top_y = top of the post arm, s = drum height.

    hit 0..1 = one strike (mallet swings in, drum swings and settles). The post stands on top_y + s * 2.1.
    """
    color = color or TEAL
    ink2 = c.theme("ink2", "d_muted")
    post_x = cx - s * 0.55
    base = top_y + s * 2.1
    with c.group(alpha):
        # post + arm + little roof
        c.fill_rrect(post_x - s * 0.06, top_y - s * 0.05, s * 0.12, base - top_y + s * 0.05, s * 0.04, ink2)
        c.fill_rrect(post_x - s * 0.06, top_y - s * 0.05, s * 0.75, s * 0.09, s * 0.04, ink2)
        _poly(c, [(post_x - s * 0.3, top_y - s * 0.05), (post_x + s * 0.1, top_y - s * 0.32),
                  (post_x + s * 0.5, top_y - s * 0.05)], ink2, 0.9)
        c.fill_rrect(post_x - s * 0.3, base - s * 0.04, s * 0.6, s * 0.08, s * 0.04, ink2, 0.6)
        # string + swinging drum
        sw = 0.22 * math.sin(hit * math.pi * 4) * (1 - hit) if 0 < hit < 1 else 0.0
        hx, hy = cx, top_y + s * 0.04
        with c.at(0, 0, 1, origin=(hx, hy), rot=sw):
            c.line(hx, hy, hx, hy + s * 0.18, ink2, 3)
            dx, dy, dw, dh = hx - s * 0.17, hy + s * 0.18, s * 0.34, s
            c.shadow(dx, dy, dw, dh, dw / 2, 18, 8, 0.12)
            c.fill_rrect(dx, dy, dw, dh, dw / 2, mix(c.theme("card", "d_card"), color, 0.22))
            c.stroke_rrect(dx, dy, dw, dh, dw / 2, color, 3)
            for f in (0.2, 0.8):  # bamboo nodes
                c.line(dx + 3, dy + dh * f, dx + dw - 3, dy + dh * f, color, 3, 0.6)
            c.fill_rrect(hx - s * 0.035, dy + dh * 0.3, s * 0.07, dh * 0.4, s * 0.035, c.theme("ink", "d_bg"), 0.85)
        # mallet: rests to the right, swings in on the hit
        if 0 < hit < 1:
            d = s * 0.42 * clamp(abs(hit - 0.12) / 0.12)
        else:
            d = s * 0.42
        mx, my = cx + s * 0.17 + d, top_y + s * 0.7
        c.line(mx, my, mx + s * 0.45, my + s * 0.35, ink2, s * 0.06)
        c.fill_rrect(mx - s * 0.04, my - s * 0.09, s * 0.14, s * 0.18, s * 0.06, ink2)
        if label:
            c.text(cx - s * 0.05, base + s * 0.32, label, tk.F["mono_bold"], max(17, s * 0.14), color, 1, 0.12,
                   align="c")


def sound_rings(c, cx, cy, p, color=None, n=3, r0=20, r_max=420, width=5, alpha=1.0, squash=1.0, arc=None):
    """n expanding rings after a strike; p 0..1 over the whole spread. squash scales them vertically (< 1 = street
    view); arc=(a0, a1) radians draws only that part (e.g. (-1.4, 1.4) = rightward half, keeps the left edge clean)."""
    if p <= 0 or p >= 1.2:
        return
    color = color or TEAL
    cx_ = c.ctx
    for k in range(n):
        pk = clamp((p - k * 0.14) / 0.72)
        if pk <= 0 or pk >= 1:
            continue
        r = r0 + (r_max - r0) * out_cubic(pk)
        cx_.save()
        cx_.translate(cx, cy)
        cx_.scale(1, squash)
        cx_.new_path()
        cx_.arc(0, 0, r, *(arc or (0, 2 * math.pi)))
        cx_.restore()
        c.src(color, alpha * (1 - pk) * 0.9)
        cx_.set_line_width(width * (1 - 0.5 * pk))
        cx_.stroke()


# ── houses ──────────────────────────────────────────────────────────────
def rumah(c, cx, base_y, s, t, light=0.0, busy=0.0, sleep=0.0, broken=0.0, label=None, label_rot=0.0,
          label_color=None, color=None, alpha=1.0, seed=0):
    """Small house (one function), width s, standing on base_y. light/busy/sleep/broken 0..1. Label = signboard."""
    color = color or TEAL
    x, h = cx - s / 2, s * 0.62
    yt = base_y - h
    with c.group(alpha):
        c.shadow(x, yt, s, h, 10, 20, 8, 0.08)
        c.fill_rrect(x, yt, s, h, 8, c.theme("card", "d_card"))
        c.stroke_rrect(x, yt, s, h, 8, c.theme("line", "d_line"), 1.5)
        _poly(c, [(x - s * 0.08, yt + 2), (cx, yt - s * 0.36), (x + s * 1.08, yt + 2)], _roof_color(c))
        _window(c, x + s * 0.12, yt + h * 0.2, s * 0.38, h * 0.42, light, t, busy, broken, seed, color)
        c.fill_rrect(x + s * 0.62, base_y - h * 0.66, s * 0.24, h * 0.66, 5, c.theme("faint", "d_line"))
        c.circle(x + s * 0.81, base_y - h * 0.33, max(2.5, s * 0.02), c.theme("ink2", "d_muted"))
        if broken > 0.01:
            _spark(c, x + s * 0.31, yt + h * 0.41, s * 0.4, t, broken, seed)
        if sleep > 0.01:
            for k in range(2):
                ph = (t * 0.45 + k * 0.5 + _h(seed, 5)) % 1.0
                zx = cx + s * 0.32 + ph * s * 0.18
                zy = yt - s * 0.3 - ph * s * 0.35
                c.text(zx, zy, "z", tk.F["serif"], s * (0.2 + 0.08 * k), c.theme("muted", "d_muted"),
                       sleep * min(1, ph * 5, (1 - ph) * 3))
        if label:
            lc = label_color or c.theme("ink2", "d_ink")
            fs = max(17, s * 0.15)
            with c.at(0, 0, 1, origin=(cx, base_y + fs * 1.4), rot=label_rot):
                c.text(cx, base_y + fs * 1.7, label, tk.F["mono_med"], fs, lc, 1, 0.02, align="c")


def rumah_gede(c, x, base_y, w, h, rooms, t, trip=0.0, closed=0.0, p_labels=1.0, color=None, alpha=1.0,
               mcb=True):
    """The monolith: one wide house, rooms in a row under one roof, one MCB box on the left wall.

    rooms: [{label, light, busy, broken}] · trip 0..1 = MCB trips, everything goes dark · closed 0..1 = renovation board.
    """
    color = color or TEAL
    yt = base_y - h
    n = len(rooms)
    roof_h = h * 0.38
    with c.group(alpha):
        c.shadow(x, yt, w, h, 14, 34, 14, 0.08)
        c.fill_rrect(x, yt, w, h, 12, c.theme("card", "d_card"))
        c.stroke_rrect(x, yt, w, h, 12, c.theme("line", "d_line"), 1.5)
        _poly(c, [(x - w * 0.04, yt + 2), (x + w * 0.12, yt - roof_h), (x + w * 0.88, yt - roof_h),
                  (x + w * 1.04, yt + 2)], _roof_color(c))
        pad = 46 if mcb else 20
        rx0 = x + pad + (40 if mcb else 0)
        rw = (x + w - 20 - rx0) / max(1, n)
        for k, rm in enumerate(rooms):
            rx = rx0 + k * rw
            if k:
                c.line(rx, yt + 14, rx, base_y - 14, c.theme("line", "d_line"), 2)
            lt = rm.get("light", 1.0) * (1 - trip)
            wx, wy, ww, wh = rx + rw * 0.14, yt + h * 0.16, rw * 0.72, h * 0.42
            _window(c, wx, wy, ww, wh, lt, t, rm.get("busy", 0.0) * (1 - trip), rm.get("broken", 0.0), k, color)
            if rm.get("broken", 0.0) > 0.01:
                _spark(c, wx + ww / 2, wy + wh / 2, ww * 0.6, t, rm["broken"] * (1 - 0.6 * trip), k + 7)
            la = clamp(p_labels * n - k)
            if la > 0 and rm.get("label"):
                c.text(rx + rw / 2, base_y - h * 0.18, rm["label"], tk.F["mono_med"], max(17, min(22, rw * 0.13)),
                       c.theme("ink2", "d_ink"), glide(la), 0.02, align="c")
        if mcb:
            bx, by = x + 22, yt + h * 0.2
            c.fill_rrect(bx, by, 44, 76, 8, c.theme("faint", "d_line"))
            lever = mix(tk.C["ok"], tk.C["rec"], clamp(trip * 2))
            ly = by + 18 + 30 * in_out_cubic(clamp(trip * 2))
            c.fill_rrect(bx + 12, ly, 20, 26, 5, lever)
            c.text(bx + 22, by + 106, "MCB", tk.F["mono_bold"], 17, c.theme("muted", "d_muted"), 1, 0.1, align="c")
        if closed > 0.01:
            p = glide(closed)
            bw, bh = w * 0.82, 92
            cxb, cyb = x + w / 2, yt + h * 0.45
            with c.at(0, -40 * (1 - p), 1, origin=(cxb, cyb), rot=-0.05):
                with c.group(clamp(closed * 3)):
                    c.shadow(cxb - bw / 2, cyb - bh / 2, bw, bh, 8, 18, 8, 0.12)
                    c.fill_rrect(cxb - bw / 2, cyb - bh / 2, bw, bh, 8, tk.C["rec"])
                    for sx in (-1, 1):
                        c.circle(cxb + sx * (bw / 2 - 22), cyb, 7, WHITE, 0.8)
                    c.text(cxb, cyb + 17, "TUTUP · RENOVASI", tk.F["mono_bold"], 44, WHITE, 1, 0.08, align="c")


def gang(c, x, y, w, alpha=1.0):
    """Street under a row of houses: kerb line + dashed centre line."""
    with c.group(alpha):
        c.line(x, y, x + w, y, c.theme("faint", "d_line"), 5)
        cx_ = c.ctx
        cx_.new_path()
        cx_.move_to(x + 10, y + 40)
        cx_.line_to(x + w - 10, y + 40)
        c.src(c.theme("faint", "d_line"), 0.8)
        cx_.set_line_width(4)
        cx_.set_dash([26, 22])
        cx_.stroke()
        cx_.set_dash([])


def portal(c, cx, base_y, w, p_open=0.0, label="NAT gateway", color=None, alpha=1.0):
    """Kampung portal gate: two posts + striped boom (pivot on the left post). p_open 0..1 lifts the boom."""
    color = color or TEAL
    ink2 = c.theme("ink2", "d_muted")
    ph = 120
    lx, rx = cx - w / 2, cx + w / 2
    with c.group(alpha):
        for px in (lx, rx):
            c.fill_rrect(px - 10, base_y - ph, 20, ph, 6, ink2)
        by = base_y - ph * 0.62
        ang = -1.2 * in_out_cubic(clamp(p_open))
        with c.at(0, 0, 1, origin=(lx, by), rot=ang):
            c.fill_rrect(lx - 6, by - 12, w + 12, 24, 12, c.theme("card", "d_card"))
            seg = (w + 12) / 8
            for k in range(0, 8, 2):
                c.fill_rrect(lx - 6 + k * seg, by - 12, seg, 24, 4 if 0 < k < 7 else 12, color)
            c.stroke_rrect(lx - 6, by - 12, w + 12, 24, 12, color, 2)
        c.circle(lx, by, 13, ink2)
        if label:
            c.text(cx, base_y + 40, label, tk.F["mono_bold"], 22, color, 1, 0.12, align="c")


def ronda_man(c, x, base_y, s, t, walk=0.0, arm=0.0, color=None, alpha=1.0):
    """Tiny night-watch figure (height s) standing on base_y. walk 0..1 = step cycle amplitude; arm 0..1 raises the
    mallet arm (toward the kentongan on his left)."""
    color = color or c.theme("ink2", "d_ink")
    ph = math.sin(t * 9.0) * walk
    hip_y = base_y - s * 0.42
    with c.group(alpha):
        for sgn in (1, -1):
            fx = x + sgn * ph * s * 0.16
            c.line(x, hip_y, fx, base_y, color, s * 0.08)
        c.fill_rrect(x - s * 0.13, base_y - s * 0.8, s * 0.26, s * 0.42, s * 0.1, color)
        c.circle(x, base_y - s * 0.9, s * 0.11, color)
        sh_y = base_y - s * 0.72
        ar = clamp(arm)
        c.line(x, sh_y, x - s * (0.12 + 0.2 * ar), sh_y + s * (0.3 - 0.45 * ar), color, s * 0.06)
        c.line(x, sh_y, x + s * 0.08 - ph * s * 0.1, sh_y + s * 0.3, color, s * 0.06)
