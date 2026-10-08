"""Household-electricity components (first used in "biaya-cloud-bocor").

pulse_phase · token_meter · stop_kontak · steker · alat
Signature move: the meter's pulse LED blinks fast; every fixed leak slows it down. The blink phase is the integral of a
piecewise rate, so any t renders the same (frame = f(t)).
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, out_spring

TEAL = tk.CHAPTER[4][0]
RED = tk.C["rec"]
WHITE = (1, 1, 1, 1)


def pulse_phase(t, rates):
    """rates = [(t_start, hz), …] sorted; returns blink phase (cycles) at t."""
    ph = 0.0
    for i, (ts, hz) in enumerate(rates):
        if t <= ts:
            break
        te = min(t, rates[i + 1][0]) if i + 1 < len(rates) else t
        ph += hz * max(0.0, te - ts)
    return ph


def rate_at(t, rates):
    hz = rates[0][1]
    for ts, h in rates:
        if t >= ts:
            hz = h
    return hz


def token_meter(c, x, y, w, h, t, rates, calm=0.0, bar=None, label="PRABAYAR", color=None, alpha=1.0):
    """Prepaid electricity meter (top-left x, y; w × h). rates drive the pulse LED; calm 0..1 = LCD 'boros' → 'normal';
    bar 0..1 = consumption bar on the LCD (defaults to 1 - 0.85 * calm)."""
    color = color or TEAL
    bar = (1 - 0.85 * calm) if bar is None else bar
    ink2, muted = c.theme("ink2", "d_muted"), c.theme("muted", "d_muted")
    with c.group(alpha):
        c.shadow(x, y, w, h, 22, 30, 12, 0.12)
        c.fill_rrect(x, y, w, h, 22, mix(c.theme("card", "d_card"), c.theme("faint", "d_line"), 0.35))
        c.stroke_rrect(x, y, w, h, 22, c.theme("line", "d_line"), 1.5)
        c.text(x + 20, y + 36, label, tk.F["mono_bold"], 17, muted, 1, 0.16)
        # LCD
        lx, ly, lw, lh = x + 18, y + 52, w - 36, h * 0.3
        lcd = mix(c.theme("ink", "d_bg"), color, 0.35)
        c.fill_rrect(lx, ly, lw, lh, 10, lcd)
        c.text(lx + 14, ly + 30, "LAJU", tk.F["mono_bold"], 17, mix(WHITE, color, 0.3), 0.85, 0.12)
        c.fill_rrect(lx + 14, ly + 42, lw - 28, 14, 7, WHITE, 0.15)
        c.fill_rrect(lx + 14, ly + 42, (lw - 28) * clamp(bar), 14, 7, mix(RED, color, calm))
        st = "normal" if calm > 0.5 else "boros"
        c.text(lx + lw - 14, ly + lh - 14, st, tk.F["mono_bold"], max(17, lh * 0.2), mix(RED, color, calm) if calm < 0.5
               else color, 1, 0.06, align="r")
        # keypad
        kw = (w - 36 - 3 * 10) / 4
        for r in range(3):
            for k in range(4):
                c.fill_rrect(x + 18 + k * (kw + 10), ly + lh + 22 + r * (kw * 0.62 + 8), kw, kw * 0.62, 6,
                             c.theme("card", "d_card"))
        # pulse LED (imp/kWh)
        ph = pulse_phase(t, rates) % 1.0
        flash = math.exp(-ph * 9)
        led = mix(RED, color, calm)
        ex, ey = x + w - 34, y + 28
        c.circle(ex, ey, 9, mix(c.theme("faint", "d_line"), led, 0.35))
        c.circle(ex, ey, 9, led, flash)
        c.circle(ex, ey, 22, led, 0.25 * flash)
        c.text(ex - 16, ey + 6, "imp", tk.F["mono"], 17, muted, 1, 0.04, align="r")


def stop_kontak(c, x, y, w, n, color=None, alpha=1.0):
    """Long power strip (top-left x, y; width w, height 46) with n sockets; returns the socket centers."""
    color = color or TEAL
    h = 46
    with c.group(alpha):
        c.shadow(x, y, w, h, 14, 18, 8, 0.1)
        c.fill_rrect(x, y, w, h, 14, c.theme("card", "d_card"))
        c.stroke_rrect(x, y, w, h, 14, c.theme("line", "d_line"), 1.5)
        c.fill_rrect(x + 10, y + 12, 22, 22, 6, color)                              # switch
        pts = []
        for k in range(n):
            sx = x + 60 + (w - 80) * (k + 0.5) / n
            c.circle(sx, y + h / 2, 15, c.theme("faint", "d_line"))
            c.circle(sx - 5, y + h / 2, 3, c.theme("ink2", "d_muted"))
            c.circle(sx + 5, y + h / 2, 3, c.theme("ink2", "d_muted"))
            pts.append((sx, y + h / 2))
    return pts


def steker(c, x, y, s, rot=0.0, cable_to=None, sag=60, alpha=1.0):
    """Plug whose prongs point down at (x, y) (size s); optional cable from its top to cable_to (sagging bezier)."""
    ink2 = c.theme("ink2", "d_muted")
    with c.group(alpha):
        if cable_to:
            cx_ = c.ctx
            cx_.new_path()
            cx_.move_to(x, y - s * 0.9)
            tx, ty = cable_to
            cx_.curve_to(x, y - s * 0.9 - sag, tx, ty + sag, tx, ty)
            c.src(ink2)
            cx_.set_line_width(5)
            cx_.stroke()
        with c.at(0, 0, 1, origin=(x, y), rot=rot):
            c.line(x - s * 0.18, y - s * 0.2, x - s * 0.18, y + s * 0.15, c.theme("muted", "d_muted"), 4)
            c.line(x + s * 0.18, y - s * 0.2, x + s * 0.18, y + s * 0.15, c.theme("muted", "d_muted"), 4)
            c.fill_rrect(x - s * 0.36, y - s * 0.9, s * 0.72, s * 0.72, s * 0.18, ink2)


def _tile(c, x, y, w, h, label, sub, hi, fixed, color):
    c.card(x, y, w, h, r=18, shadow="card_tight")
    if hi > 0.01:
        c.stroke_rrect(x - 4, y - 4, w + 8, h + 8, 21, color, 3, hi)
    c.text(x + w / 2, y + h - 30, label, tk.F["mono_bold"], 17, c.theme("ink2", "d_ink"), 1, 0.04, align="c")
    if sub:
        c.text(x + w / 2, y + h - 10, sub, tk.F["mono"], 17, mix(c.theme("muted", "d_muted"), color, fixed), 1, 0,
               align="c")


def alat(c, kind, x, y, w, h, t, fixed=0.0, hi=0.0, label="", sub="", color=None, seed=0):
    """One appliance tile. kind: colokan_t · kulkas · ac · charger · lampu. fixed 0..1 = the leak is dealt with."""
    color = color or TEAL
    ink2, muted, faint = c.theme("ink2", "d_muted"), c.theme("muted", "d_muted"), c.theme("faint", "d_line")
    _tile(c, x, y, w, h, label, sub, hi, fixed, color)
    cx, cy = x + w / 2, y + (h - 44) / 2 + 6
    s = min(w, h - 44) * 0.8
    leak = 1 - fixed
    if kind == "colokan_t":
        for k in range(3):                                               # stacked T adapters, crooked
            with c.at(0, 0, 1, origin=(cx, cy), rot=(k - 1) * 0.18 * leak):
                bx, by = cx - s * 0.2 + k * s * 0.12, cy + s * 0.25 - k * s * 0.24
                c.fill_rrect(bx - s * 0.18, by - s * 0.12, s * 0.36, s * 0.24, 6, ink2)
                c.circle(bx - s * 0.07, by, 3, c.theme("card", "d_card"))
                c.circle(bx + s * 0.07, by, 3, c.theme("card", "d_card"))
        for k in range(3):
            c.text(cx - s * 0.36 + k * s * 0.36, cy - s * 0.42, "?", tk.F["serif"], s * 0.3, RED, leak, align="c")
        if fixed > 0.01:
            with c.at(0, 0, 1, origin=(cx, cy), rot=-0.08):
                c.fill_rrect(cx - s * 0.48, cy - s * 0.55, s * 0.96, s * 0.3, 6, mix(WHITE, color, 0.12), fixed)
                c.text(cx, cy - s * 0.33, "tim-payment", tk.F["serif"], max(17, s * 0.2), color, fixed, align="c")
    elif kind == "kulkas":
        fx, fy, fw, fh = cx - s * 0.36, cy - s * 0.5, s * 0.72, s
        c.stroke_rrect(fx, fy, fw, fh, 10, ink2, 3)
        c.line(fx, fy + fh * 0.32, fx + fw, fy + fh * 0.32, ink2, 3)
        n = int(round(4 * leak + 0.49))
        for k in range(n):                                               # old boxes inside
            bx = fx + 8 + (k % 2) * (fw / 2 - 4)
            by = fy + fh * 0.38 + (k // 2) * fh * 0.3
            c.fill_rrect(bx, by, fw / 2 - 12, fh * 0.24, 4, mix(faint, RED, 0.35))
            c.text(bx + (fw / 2 - 12) / 2, by + fh * 0.17, "lama", tk.F["mono"], 17, muted, 1, 0, align="c")
    elif kind == "ac":
        ax, ay, aw, ah = cx - s * 0.5, cy - s * 0.32, s, s * 0.36
        c.fill_rrect(ax, ay, aw, ah, 10, c.theme("card", "d_card"))
        c.stroke_rrect(ax, ay, aw, ah, 10, ink2, 3)
        for k in range(3):
            c.line(ax + 12, ay + ah - 8 - k * 7, ax + aw - 12, ay + ah - 8 - k * 7, muted, 2)
        badge = "2 PK" if fixed < 0.5 else "½ PK"
        c.text(ax + aw - 12, ay + 24, badge, tk.F["mono_bold"], 17, RED if fixed < 0.5 else color, 1, 0, align="r")
        # CPU bar: barely used
        c.text(ax, cy + s * 0.3, "CPU", tk.F["mono_bold"], 17, muted, 1, 0.08)
        bw = aw - 50
        c.fill_rrect(ax + 48, cy + s * 0.3 - 12, bw, 12, 6, faint)
        use = 0.12 + 0.03 * math.sin(t * 3 + seed)
        use = use + (0.62 - use) * fixed
        c.fill_rrect(ax + 48, cy + s * 0.3 - 12, bw * use, 12, 6, mix(RED, color, fixed))
    elif kind == "charger":
        bx, by = cx, cy - s * 0.05
        glow = leak * (0.6 + 0.4 * math.sin(t * 5 + seed))
        if glow > 0.01:
            c.circle(bx, by, s * 0.32, RED, 0.12 * glow)
        c.fill_rrect(bx - s * 0.16, by - s * 0.2, s * 0.32, s * 0.36, 8, ink2)
        c.circle(bx + s * 0.08, by - s * 0.1, 4, RED if leak > 0.5 else faint)
        cxx = c.ctx                                                       # dangling cable, no phone
        cxx.new_path()
        cxx.move_to(bx, by + s * 0.16)
        cxx.curve_to(bx, by + s * 0.5, bx + s * 0.4, by + s * 0.2, bx + s * 0.36, by + s * 0.46)
        c.src(ink2)
        cxx.set_line_width(4)
        cxx.stroke()
        c.fill_rrect(bx + s * 0.31, by + s * 0.44, s * 0.1, s * 0.06, 2, ink2)
    elif kind == "lampu":
        lx, ly = cx - s * 0.08, cy + s * 0.05
        on = leak
        if on > 0.01:
            c.circle(lx, ly - s * 0.08, s * 0.3, color, 0.18 * on)
        c.circle(lx, ly - s * 0.08, s * 0.17, mix(faint, color, on))
        c.fill_rrect(lx - s * 0.08, ly + s * 0.06, s * 0.16, s * 0.12, 3, ink2)
        c.line(lx, ly + s * 0.18, lx, ly + s * 0.45, ink2, 3)
        sx, sy = cx + s * 0.32, cy - s * 0.32                             # the sun: it's daytime
        c.circle(sx, sy, s * 0.1, tk.CHAPTER[2][0])
        for k in range(8):
            a = k / 8 * 2 * math.pi
            c.line(sx + s * 0.14 * math.cos(a), sy + s * 0.14 * math.sin(a), sx + s * 0.2 * math.cos(a),
                   sy + s * 0.2 * math.sin(a), tk.CHAPTER[2][0], 3)
    if fixed > 0.01:                                                      # ✓ badge, top-right of the tile
        from . import icons
        bx, by = x + w - 18, y + 18
        p = out_spring(clamp(fixed))                                     # settles with a small overshoot
        with c.at(0, 0, max(0.01, p), origin=(bx, by)):
            c.circle(bx, by, 16, tk.C["ok"])
            icons.check(c, bx, by, 13, WHITE, 3)
