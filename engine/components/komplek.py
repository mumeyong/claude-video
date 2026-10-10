"""Housing-estate (komplek) components (first used in "wifi-ep02-connected-no-internet", Bongkar WiFi Rumah EP 02).

wifi_icon · pos_satpam · buku_alamat
Metaphor: your devices are houses in a komplek, the router is the guard post at the gate, the boom barrier is the
link to the ISP, and the guard's address book is DNS. Signature: the striped boom lifts (or doesn't) on a heavy spring.
Pure functions of their progress values and t.
"""
import math

from .. import tokens as tk
from ..ease import clamp, out_back, in_out_cubic

ORANGE = tk.CHAPTER[2][0]           # signature: boom barrier + test envelope
WHITE = (1, 1, 1, 1)


def _arc(c, cx, cy, r, a0, a1, color, width, alpha=1.0):
    cx_ = c.ctx
    cx_.new_path()
    cx_.arc(cx, cy, r, a0, a1)
    c.src(color, alpha)
    cx_.set_line_width(width)
    cx_.set_line_cap(1)                 # round
    cx_.stroke()


# ── WiFi status icon ───────────────────────────────────────────────────
def wifi_icon(c, cx, cy, s, bars=3.0, bang=0.0, color=None, alpha=1.0):
    """Status-bar WiFi fan: dot at (cx, cy) (the fan's point), 3 arcs up to radius s. bars 0..3 (float) lights the
    dot + arcs from the inside out; bang 0..1 pops the coral '!' badge at the lower right."""
    on = color or c.theme("ink", "d_ink")
    off = c.theme("faint", "d_line")
    wid = s * 0.15
    a0, a1 = math.radians(-135), math.radians(-45)
    with c.group(alpha):
        lit = clamp(bars * 3)                       # the dot lights in the first third of bar 1
        c.circle(cx, cy - wid * 0.2, wid * 0.62, off)
        if lit > 0:
            c.circle(cx, cy - wid * 0.2, wid * 0.62, on, lit)
        for k in range(3):
            r = s * (0.38 + 0.31 * k)
            _arc(c, cx, cy, r, a0, a1, off, wid)
            p = clamp(bars - k)
            if p > 0:
                _arc(c, cx, cy, r, a0, a1, on, wid, p)
        b = out_back(clamp(bang))
        if b > 0.01:
            bx, by, br = cx + s * 0.62, cy - s * 0.08, s * 0.24
            with c.at(0, 0, b, origin=(bx, by)):
                c.circle(bx, by, br * 1.18, c.theme("bg", "d_bg"))
                c.circle(bx, by, br, tk.C["rec"])
                c.fill_rrect(bx - br * 0.11, by - br * 0.62, br * 0.22, br * 0.78, br * 0.11, WHITE)
                c.circle(bx, by + br * 0.48, br * 0.13, WHITE)


# ── guard post + boom barrier ──────────────────────────────────────────
def pos_satpam(c, cx, base_y, s, t, p_open=0.0, arm=None, confused=0.0, label="POS", color=None, alpha=1.0):
    """Guard post (width s) standing on base_y with a guard in the window, and a striped boom barrier pivoting on a
    post just right of the booth, reaching `arm` px (default 1.3 s) across the road. p_open 0..1 lifts the boom
    (feed a heavy spring; > 1 overshoots a little). confused 0..1 pops a '?' over the guard.
    Returns (pivot_x, pivot_y, arm_len)."""
    color = color or ORANGE
    arm = s * 1.3 if arm is None else arm
    ink2, card = c.theme("ink2", "d_muted"), c.theme("card", "d_card")
    h = s * 0.95
    x, yt = cx - s / 2, base_y - h
    with c.group(alpha):
        c.shadow(x, yt, s, h, 10, 24, 10, 0.08)
        c.fill_rrect(x, yt, s, h, 10, card)
        c.stroke_rrect(x, yt, s, h, 10, c.theme("line", "d_line"), 1.5)
        c.fill_rrect(x - s * 0.08, yt - s * 0.14, s * 1.16, s * 0.16, 8, ink2)          # flat roof slab
        c.text(cx, yt - s * 0.035, label, tk.F["mono_bold"], max(17, s * 0.1), card, 1, 0.2, align="c")
        wx, wy, ww, wh = x + s * 0.12, yt + h * 0.14, s * 0.76, h * 0.42
        c.fill_rrect(wx, wy, ww, wh, 8, c.theme("faint", "d_line"))
        gx = wx + ww * 0.5 + math.sin(t * 0.7) * s * 0.015                            # the guard, breathing
        gy = wy + wh
        c.fill_rrect(gx - s * 0.13, gy - wh * 0.42, s * 0.26, wh * 0.42, s * 0.08, ink2)
        c.circle(gx, gy - wh * 0.6, s * 0.085, ink2)
        c.fill_rrect(gx - s * 0.1, gy - wh * 0.6 - s * 0.1, s * 0.2, s * 0.05, 4, color)  # cap band
        c.fill_rrect(x + s * 0.1, yt + h * 0.66, s * 0.8, h * 0.05, 3, c.theme("line", "d_line"))   # counter
        q = out_back(clamp(confused))
        if q > 0.01:
            qx, qy = gx + s * 0.34, wy - s * 0.12
            with c.at(0, 0, q, origin=(qx, qy + s * 0.1)):
                c.fill_rrect(qx - s * 0.13, qy - s * 0.2, s * 0.26, s * 0.3, s * 0.1, card)
                c.stroke_rrect(qx - s * 0.13, qy - s * 0.2, s * 0.26, s * 0.3, s * 0.1, color, 2.5)
                c.text(qx, qy + s * 0.05, "?", tk.F["display"], s * 0.24, color, 1, align="c")
        # boom barrier
        px, py = x + s + s * 0.16, base_y - s * 0.42
        c.fill_rrect(px - s * 0.05, py - s * 0.04, s * 0.1, base_y - py + s * 0.04, 5, ink2)
        ang = -1.3 * in_out_cubic(clamp(p_open)) if p_open <= 1 else -1.3 * p_open
        bh = max(14, s * 0.1)
        with c.at(0, 0, 1, origin=(px, py), rot=ang):
            c.fill_rrect(px, py - bh / 2, arm, bh, bh / 2, card)
            seg = arm / 7
            for k in range(1, 7, 2):
                c.fill_rrect(px + k * seg, py - bh / 2, seg, bh, 3, color)
            c.stroke_rrect(px, py - bh / 2, arm, bh, bh / 2, color, 2)
            c.fill_rrect(px + arm - s * 0.04, py, s * 0.025, s * 0.12, 3, ink2)        # hanging tip strut
        c.circle(px, py, s * 0.065, ink2)
    return px, py, arm


# ── the guard's address book (DNS) ──────────────────────────────────────
def buku_alamat(c, x, y, w, h, rows, scan=None, fail=0.0, found=0.0, title="BUKU ALAMAT", chip="DNS",
                color=None, alpha=1.0):
    """Address book card (x, y, w, h): ring binding on the left, title + chip, rows of (name, number).
    scan = (row_index, p) moves a highlight band onto that row (p 0..1). fail 0..1 turns the numbers into a red '?'
    and slams a tilted ERROR stamp; found 0..1 inks the numbers in (green) — use with sheen/swap for the new book."""
    color = color or ORANGE
    ink, ink2, muted = c.theme("ink", "d_ink"), c.theme("ink2", "d_muted"), c.theme("muted", "d_muted")
    with c.group(alpha):
        c.card(x, y, w, h, r=24)
        c.fill_rrect(x, y, 70, h, 24, c.theme("bg", "d_bg"))
        for k in range(6):
            ry = y + 70 + k * (h - 140) / 5
            c.circle(x + 35, ry, 11, c.theme("card", "d_card"))
            c.stroke_rrect(x + 22, ry - 5, 30, 10, 5, ink2, 3)
        tx = x + 110
        c.text(tx, y + 78, title, tk.F["mono_bold"], 24, muted, 1, 0.18)
        cw_ = c.measure(chip, tk.F["mono_bold"], 24)[0] + 36
        c.fill_rrect(x + w - cw_ - 36, y + 44, cw_, 48, 24, color)
        c.text(x + w - cw_ / 2 - 36, y + 77, chip, tk.F["mono_bold"], 24, WHITE, 1, 0.1, align="c")
        row_h = (h - 150) / max(1, len(rows))
        if scan is not None:
            i, p = scan
            ry = y + 120 + row_h * i
            c.fill_rrect(tx - 18, ry + 6, (w - 150) * clamp(p * 1.4), row_h - 12, 14, color, 0.14)
        for i, (name, num) in enumerate(rows):
            ry = y + 120 + row_h * i + row_h * 0.62
            c.text(tx, ry, name, tk.F["mono_med"], 32, ink, 1)
            nw = c.measure(name, tk.F["mono_med"], 32)[0]
            lx0, lx1 = tx + nw + 20, x + w - 300
            for dx in range(int(lx0), int(lx1), 18):
                c.circle(dx, ry - 8, 2.5, c.theme("faint", "d_line"))
            fx = x + w - 48
            if fail > 0.01:
                c.text(fx, ry, num, tk.F["mono"], 30, muted, 1 - clamp(fail * 2), align="r")
                c.text(fx, ry, "?", tk.F["display"], 44, tk.C["rec"], clamp(fail * 2 - 1), align="r")
            elif found > 0.01:
                c.text(fx, ry, num, tk.F["mono_med"], 30, tk.C["ok"], clamp(found), align="r")
            else:
                c.text(fx, ry, num, tk.F["mono"], 30, muted, 1, align="r")
        st = clamp(fail * 2 - 1)
        if st > 0.01:
            sx, sy = x + w * 0.58, y + h * 0.58
            k = 1 + 0.6 * (1 - out_back(st))
            with c.at(0, 0, k, origin=(sx, sy), rot=-0.16):
                c.stroke_rrect(sx - 150, sy - 52, 300, 104, 16, tk.C["rec"], 6, st)
                c.text(sx, sy + 22, "ERROR", tk.F["mono_bold"], 58, tk.C["rec"], st, 0.12, align="c")
