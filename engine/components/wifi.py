"""Home-WiFi components (first used in "wifi-ep01-lampu-los", series Bongkar WiFi Rumah).

modem · modem_led · fiber_route · route_point · patchcord
Signature move (EP01): light pulses ride the fiber from the ISP office to the house; where the cable is cut they stop,
and the camera rides back to the modem lamp that tells you so. Pulse positions are pure functions of t (frame = f(t)).
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix
from .kampung import rumah

PURPLE = tk.CHAPTER[3][0]           # signature: the light in the fiber
JACKET = tk.CHAPTER[2][0]           # patchcord jacket (fiber patch cables are yellow/orange)
LEDS = ("POWER", "PON", "LOS", "INTERNET", "WLAN")


# ── modem ───────────────────────────────────────────────────────────────
def _geom(cx, cy, w):
    h = w * 0.40
    y0 = cy - h / 2
    gap = w * 0.78 / len(LEDS)
    xs = [cx - w * 0.39 + gap * (i + 0.5) for i in range(len(LEDS))]
    return h, y0, xs, y0 + h * 0.56


def modem_led(cx, cy, w, name):
    """Center (x, y) of LED `name` on a modem drawn with the same cx, cy, w."""
    _, _, xs, ly = _geom(cx, cy, w)
    return xs[LEDS.index(name)], ly


def led_state(t, code):
    """(color, on 0..1) for a state code: '' off · 'g' green · 'gb' green blinking · 'r' red · 'rb' red blinking."""
    if not code:
        return None, 0.0
    col = tk.C["ok"] if code[0] == "g" else tk.C["rec"]
    on = 1.0
    if code.endswith("b"):
        on = 0.15 + 0.85 * (0.5 + 0.5 * math.cos(2 * math.pi * 2.2 * t)) ** 3
    return col, on


def modem(c, cx, cy, w, t, lights, focus=None, focus_p=0.0, labels=True, alpha=1.0, antenna=True):
    """ONT / home modem, front view, centered (cx, cy), width w (height ≈ 0.4 w + antennas).
    lights = {name: code} for LEDS (codes: see led_state). focus = one LED name: the others dim by focus_p and a
    blue ring outlines it."""
    h, y0, xs, ly = _geom(cx, cy, w)
    x0 = cx - w / 2
    body, top = c.theme("card", "d_card"), c.theme("bg", "d_bg")
    with c.group(alpha):
        if antenna:
            for k, ax in enumerate((x0 + w * 0.12, x0 + w * 0.88)):
                with c.at(0, 0, 1, origin=(ax, y0), rot=(-0.12 if k == 0 else 0.12)):
                    c.fill_rrect(ax - w * 0.018, y0 - h * 0.95, w * 0.036, h * 0.98, w * 0.018, c.theme("ink2", "d_line"))
        c.shadow(x0, y0, w, h, w * 0.06, 34, 14, 0.09)
        c.fill_rrect(x0, y0, w, h, w * 0.06, body)
        c.fill_rrect(x0 + w * 0.03, y0 + h * 0.08, w * 0.94, h * 0.10, h * 0.05, top)          # top bevel
        c.stroke_rrect(x0, y0, w, h, w * 0.06, c.theme("line", "d_line"), 1.5)
        c.text(x0 + w * 0.06, y0 + h * 0.36, "ONT", tk.F["mono_bold"], max(17, w * 0.026), c.theme("muted", "d_muted"),
               1, 0.18)
        r = w * 0.022
        size = max(17, w * 0.026)
        for name, x in zip(LEDS, xs):
            col, on = led_state(t, lights.get(name, ""))
            dim = 1 - 0.65 * clamp(focus_p) if focus and name != focus else 1.0
            c.circle(x, ly, r, c.theme("faint", "d_line"), dim)
            if col is not None and on > 0.01:
                c.circle(x, ly, r * 2.0, col, 0.18 * on * dim)                              # soft lamp halo
                c.circle(x, ly, r, col, on * dim)
            if labels and w >= 420:
                c.text(x, ly + r + size * 1.5, name, tk.F["mono_med"], size, c.theme("ink2", "d_muted"), dim,
                       0.04, align="c")
        if focus and focus_p > 0.01:
            fx = xs[LEDS.index(focus)]
            fw = max(w * 0.15, c.measure(focus, tk.F["mono_med"], size)[0] + 30)
            fh = r * 2 + size * 2.2 + 26
            c.stroke_rrect(fx - fw / 2, ly - r - 16, fw, fh, 16, tk.C["accent"], 3, clamp(focus_p))


# ── fiber route: ISP office → pole (ODP box) → house ─────────────────────
def _route_pts(box):
    x, y, w, h = box
    a = (x + w * 0.36, y + h * 0.14)                   # leaves the ISP office
    b = (x + w * 0.56, y + h * 0.33)                   # top of the pole
    o = (x + w * 0.56, y + h * 0.46)                   # ODP box
    d = (x + w * 0.70, y + h * 0.80)                   # enters the house wall
    pts = []
    for i in range(25):                                # office → pole top, sagging
        u = i / 24
        pts.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u + math.sin(math.pi * u) * h * 0.06))
    for i in range(1, 9):                              # down the pole to the ODP
        u = i / 8
        pts.append((b[0], b[1] + (o[1] - b[1]) * u))
    for i in range(1, 31):                             # drop cable to the house, sagging
        u = i / 30
        pts.append((o[0] + (d[0] - o[0]) * u, o[1] + (d[1] - o[1]) * u + math.sin(math.pi * u) * h * 0.05))
    return pts


def _cum(pts):
    out = [0.0]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        out.append(out[-1] + math.hypot(x2 - x1, y2 - y1))
    return out


def route_point(box, f):
    """(x, y) at arc fraction f (0 = ISP office, 1 = house) of fiber_route drawn in box."""
    pts = _route_pts(box)
    cum = _cum(pts)
    s = clamp(f) * cum[-1]
    for i in range(1, len(pts)):
        if cum[i] >= s:
            u = (s - cum[i - 1]) / max(1e-6, cum[i] - cum[i - 1])
            return (pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * u, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * u)
    return pts[-1]


ODP_F = 0.53     # arc fraction of the ODP box (where the drop cable starts)


def fiber_route(c, box, t, p_draw=1.0, flow=1.0, cut=0.0, cut_at=0.78, house_light=0.0, labels=True,
                speed=0.32, n=5, alpha=1.0, mark=0.0):
    """Street scene in box (x, y, w, h): ISP office (top left) → pole with the black ODP box → your house (bottom
    right), joined by one fiber cable. p_draw draws the cable along its length; flow 0..1 shows light pulses riding
    it; cut 0..1 opens a break at arc fraction cut_at (pulses die there, the cable after it goes dark);
    mark 0..1 = blue '?' ring on the ODP (the place you can't see from home)."""
    x, y, w, h = box
    ink, ink2, faint = c.theme("ink", "d_ink"), c.theme("ink2", "d_muted"), c.theme("faint", "d_line")
    card = c.theme("card", "d_card")
    size = 20
    with c.group(alpha):
        # ISP office
        bw, bh = w * 0.36, h * 0.30
        c.shadow(x, y, bw, bh, 18, 26, 10, 0.07)
        c.fill_rrect(x, y, bw, bh, 18, card)
        c.fill_rrect(x, y, bw, bh * 0.2, 18, PURPLE)
        c.fill_rrect(x, y + bh * 0.1, bw, bh * 0.1, 0, PURPLE)
        c.text(x + 20, y + bh * 0.15, "ISP", tk.F["mono_bold"], 20, (1, 1, 1, 1), 1, 0.2)
        for r_ in range(3):
            for k in range(4):
                wx = x + 22 + k * (bw - 44) / 4
                c.fill_rrect(wx, y + bh * 0.3 + r_ * bh * 0.22, (bw - 44) / 4 - 12, bh * 0.13, 4, faint)
        # pole + ODP
        px = x + w * 0.56
        c.line(px, y + h * 0.28, px, y + h * 0.98, ink2, 10)
        c.line(px - w * 0.07, y + h * 0.31, px + w * 0.07, y + h * 0.31, ink2, 7)
        ow, oh = w * 0.11, h * 0.10
        c.fill_rrect(px - ow / 2, y + h * 0.46 - oh / 2, ow, oh, 8, ink)
        c.fill_rrect(px - ow / 2 + 8, y + h * 0.46 - oh / 2 + 8, ow - 16, 6, 3, c.theme("ink2", "d_line"))
        # house
        rumah(c, x + w * 0.80, y + h, w * 0.34, t, light=house_light)
        if labels:
            c.text(x, y + bh + 36, "kantor ISP", tk.F["mono_med"], size, ink2, 1, 0.04)
            c.text(px + ow / 2 + 16, y + h * 0.46 + 8, "ODP", tk.F["mono_bold"], size, ink2, 1, 0.12)
            c.text(px + ow / 2 + 16, y + h * 0.46 + 36, "kotak di tiang", tk.F["mono"], size - 1, c.theme("muted", "d_muted"), 1)
        # cable
        pts = _route_pts(box)
        cum = _cum(pts)
        L = cum[-1]
        drawn = clamp(p_draw) * L
        s_cut = cut_at * L
        gap = 26 * clamp(cut)

        def seg(s0, s1, col, width, a=1.0):
            path = [p for p, cs in zip(pts, cum) if s0 <= cs <= s1]
            if s0 > 0:
                path.insert(0, route_point(box, s0 / L))
            if s1 < L:
                path.append(route_point(box, s1 / L))
            for (x1, y1), (x2, y2) in zip(path, path[1:]):
                c.line(x1, y1, x2, y2, col, width, a)

        lit_end = min(drawn, s_cut - gap / 2) if cut > 0.01 else drawn
        seg(0, lit_end, ink, 6)
        if cut > 0.01 and drawn > s_cut + gap / 2:
            seg(s_cut + gap / 2, drawn, faint, 6)                 # dark cable after the break
        if cut > 0.01:
            cx_, cy_ = route_point(box, cut_at)
            k = clamp(cut)
            for sgn in (-1, 1):
                c.line(cx_ - 14 * k, cy_ + sgn * 14 * k, cx_ + 14 * k, cy_ - sgn * 14 * k, tk.C["rec"], 5)
        # light pulses (+ a short trail) — positions are a pure function of t
        if flow > 0.01:
            for i in range(n):
                f = (t * speed + i / n) % 1.0
                for g in range(4):
                    fg = f - g * 0.012
                    s_ = fg * L
                    if fg < 0 or s_ > drawn or (cut > 0.01 and s_ > s_cut - gap / 2):
                        continue
                    px_, py_ = route_point(box, fg)
                    c.circle(px_, py_, 8 - g * 1.5, PURPLE, flow * (1 - g * 0.24))
        if mark > 0.01:
            mx, my = px, y + h * 0.46
            c.stroke_rrect(mx - ow / 2 - 14, my - oh / 2 - 14, ow + 28, oh + 28, 14, tk.C["accent"], 3, clamp(mark))


def patchcord(c, x0, y0, x1, y1, bend=0.0, alpha=1.0):
    """The short fiber patch cable behind the modem, from the wall socket (x0, y0) to the modem port (x1, y1).
    bend 0..1 pinches it into a sharp kink halfway (the classic home-side cause of a red LOS)."""
    mx, my = (x0 + x1) / 2, max(y0, y1) + 120
    k = clamp(bend)
    kx, ky = mx + 50 * k, my + 60 * k
    pts = []
    for i in range(41):
        u = i / 40
        if u < 0.5:
            v_ = u / 0.5
            px_ = x0 + (kx - x0) * v_
            py_ = y0 + (ky - y0) * v_ + math.sin(math.pi * v_) * 40 * (1 - k)
        else:
            v_ = (u - 0.5) / 0.5
            px_ = kx + (x1 - kx) * v_
            py_ = ky + (y1 - ky) * v_ + math.sin(math.pi * v_) * 40 * (1 - k)
        pts.append((px_, py_))
    with c.group(alpha):
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            c.line(xa, ya, xb, yb, JACKET, 14)
        for (xx, yy) in ((x0, y0), (x1, y1)):
            c.fill_rrect(xx - 22, yy - 14, 44, 28, 6, mix(JACKET, (0, 0, 0, 1), 0.25))
        c.fill_rrect(x0 - 50, y0 - 46, 100, 70, 14, c.theme("card", "d_card"))
        c.stroke_rrect(x0 - 50, y0 - 46, 100, 70, 14, c.theme("line", "d_line"), 1.5)
    return kx, ky
