"""Badminton components (first used in "bongkar-ep07-azure-ai-infra").

gpu_card · lapangan · pemain · shuttle · shuttle_arc · pelontar · rep_dots · jadwal · gor
Signature move: a shuttle arcs over the net; each landing lights one repetition dot (training).
Pure functions of their progress values and t.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, out_expo

ORANGE = tk.CHAPTER[2][0]
WHITE = (1, 1, 1, 1)


# ── GPU ─────────────────────────────────────────────────────────────────
def gpu_card(c, x, y, w, h, t, on=1.0, label="GPU", color=None, alpha=1.0, seed=0):
    """GPU board: heatsink fins + two fans that spin while on; on 0..1 lights the edge/fans in the signature color."""
    color = color or ORANGE
    body = c.theme("ink2", "d_card")
    with c.group(alpha):
        if on > 0.01:
            c.shadow(x, y, w, h, 12, 26, 8, 0.22 * on, color)
        c.fill_rrect(x, y, w, h, 12, body)
        c.stroke_rrect(x, y, w, h, 12, mix(c.theme("faint", "d_line"), color, on), 3)
        for k in range(int(w / 14)):                                           # fins
            c.line(x + 10 + k * 14, y + 8, x + 10 + k * 14, y + h * 0.18, c.theme("muted", "d_muted"), 2, 0.5)
        r = min(h * 0.3, w * 0.18)
        for j, fx in enumerate((x + w * 0.3, x + w * 0.7)):
            fy = y + h * 0.58
            c.circle(fx, fy, r, mix(c.theme("ink", "d_bg"), color, 0.25 * on))
            spin = t * 9 * on + seed + j
            for b in range(3):
                a = spin + b * 2 * math.pi / 3
                c.line(fx, fy, fx + r * 0.85 * math.cos(a), fy + r * 0.85 * math.sin(a), mix(c.theme("muted", "d_muted"),
                       color, on), 4)
            c.circle(fx, fy, r * 0.22, mix(c.theme("muted", "d_muted"), color, on))
        if label:
            c.text(x + 12, y + h - 10, label, tk.F["mono_bold"], max(17, h * 0.13), mix(c.theme("muted", "d_muted"),
                   color, on), 1, 0.1)


# ── court + players ─────────────────────────────────────────────────────
def lapangan(c, x, base_y, w, t, lights=1.0, label=None, color=None, alpha=1.0, lamp_h=260):
    """Side-view court on base_y from x to x + w: floor, lines, net at the middle, two overhead lamps."""
    color = color or ORANGE
    mid = x + w / 2
    with c.group(alpha):
        if lights > 0.01:                                                       # light cones
            for lx in (x + w * 0.25, x + w * 0.75):
                cxx = c.ctx
                cxx.new_path()
                cxx.move_to(lx - 18, base_y - lamp_h)
                cxx.line_to(lx + 18, base_y - lamp_h)
                cxx.line_to(lx + w * 0.2, base_y)
                cxx.line_to(lx - w * 0.2, base_y)
                cxx.close_path()
                c.src(color, 0.08 * lights)
                cxx.fill()
        c.fill_rrect(x, base_y, w, 22, 6, mix(c.theme("faint", "d_line"), color, 0.25 * lights))
        for f in (0.04, 0.3, 0.7, 0.96):
            c.line(x + w * f, base_y + 3, x + w * f, base_y + 19, WHITE, 3, 0.9)
        # net
        nh = 110
        c.fill_rrect(mid - 4, base_y - nh - 30, 8, nh + 30, 3, c.theme("ink2", "d_muted"))
        for k in range(6):
            yy = base_y - nh - 20 + k * 14
            c.line(mid - 3, yy, mid + 3, yy, c.theme("muted", "d_muted"), 1.5)
        c.fill_rrect(mid - 6, base_y - nh - 30, 12, 8, 2, WHITE)
        # lamps
        for lx in (x + w * 0.25, x + w * 0.75):
            c.line(lx, base_y - lamp_h - 40, lx, base_y - lamp_h, c.theme("muted", "d_muted"), 3)
            c.fill_rrect(lx - 26, base_y - lamp_h - 8, 52, 16, 6, c.theme("ink2", "d_muted"))
            c.circle(lx, base_y - lamp_h + 10, 9, mix(c.theme("faint", "d_line"), color, lights))
            if lights > 0.01:
                c.circle(lx, base_y - lamp_h + 10, 22, color, 0.25 * lights)
        if label:
            c.text(x, base_y + 56, label, tk.F["mono_bold"], 19, mix(c.theme("muted", "d_muted"), color, lights), 1,
                   0.14)


def pemain(c, x, base_y, s, t, swing=0.0, facing=1, color=None, alpha=1.0):
    """Player (height s) on base_y with a racket; swing 0..1 brings the racket from back to front over the head."""
    color = color or c.theme("ink2", "d_ink")
    f = facing
    with c.group(alpha):
        hip = base_y - s * 0.45
        c.line(x, hip, x - f * s * 0.12, base_y, color, s * 0.08)
        c.line(x, hip, x + f * s * 0.14, base_y, color, s * 0.08)
        c.fill_rrect(x - s * 0.13, base_y - s * 0.84, s * 0.26, s * 0.42, s * 0.1, color)
        c.circle(x, base_y - s * 0.94, s * 0.1, color)
        sh = (x, base_y - s * 0.78)
        a = (-2.4 + 2.6 * clamp(swing)) if f > 0 else (math.pi + 2.4 - 2.6 * clamp(swing))
        hx, hy = sh[0] + s * 0.3 * math.cos(a), sh[1] + s * 0.3 * math.sin(a)
        c.line(sh[0], sh[1], hx, hy, color, s * 0.06)
        rx, ry = hx + s * 0.28 * math.cos(a), hy + s * 0.28 * math.sin(a)
        c.line(hx, hy, rx, ry, color, s * 0.025)
        cxx = c.ctx
        cxx.save()
        cxx.translate(rx + s * 0.08 * math.cos(a), ry + s * 0.08 * math.sin(a))
        cxx.rotate(a)
        cxx.scale(1, 0.7)
        cxx.new_path()
        cxx.arc(0, 0, s * 0.1, 0, 2 * math.pi)
        cxx.restore()
        c.src(color)
        cxx.set_line_width(s * 0.025)
        cxx.stroke()


def shuttle(c, x, y, s, rot=0.0, color=None, alpha=1.0):
    """Shuttlecock at (x, y) (cork position), size s, pointing along rot (radians; 0 = cork to the right)."""
    color = color or ORANGE
    with c.at(0, 0, 1, origin=(x, y), rot=rot):
        with c.group(alpha):
            cxx = c.ctx
            cxx.new_path()
            cxx.move_to(x - s * 0.15, y - s * 0.18)
            cxx.line_to(x - s * 1.1, y - s * 0.5)
            cxx.line_to(x - s * 1.1, y + s * 0.5)
            cxx.line_to(x - s * 0.15, y + s * 0.18)
            cxx.close_path()
            c.src(c.theme("card", "d_ink"))
            cxx.fill_preserve()
            c.src(c.theme("muted", "d_muted"))
            cxx.set_line_width(2)
            cxx.stroke()
            c.circle(x, y, s * 0.24, color)


def shuttle_arc(x0, y0, x1, y1, peak, u):
    """(x, y, angle) at u 0..1 on a parabola from (x0, y0) to (x1, y1) rising `peak` px above the higher end."""
    u = clamp(u)
    x = x0 + (x1 - x0) * u
    top = min(y0, y1) - peak
    y = (1 - u) ** 2 * y0 + 2 * u * (1 - u) * (2 * top - (y0 + y1) / 2) + u ** 2 * y1
    dx = x1 - x0
    dy = 2 * (1 - u) * ((2 * top - (y0 + y1) / 2) - y0) + 2 * u * (y1 - (2 * top - (y0 + y1) / 2))
    return x, y, math.atan2(dy, dx)


def pelontar(c, x, base_y, s, t, fire=0.0, color=None, alpha=1.0, facing=-1):
    """Shuttle launcher (height s) on a tripod; fire 0..1 = one shot (recoil). facing -1 shoots to the left."""
    color = color or ORANGE
    ink2 = c.theme("ink2", "d_muted")
    rec = math.sin(clamp(fire) * math.pi) * s * 0.06
    with c.group(alpha):
        for dx in (-0.25, 0.0, 0.25):
            c.line(x, base_y - s * 0.4, x + dx * s, base_y, ink2, 5)
        bx, by = x - s * 0.32 - facing * rec, base_y - s * 0.78
        c.fill_rrect(bx, by, s * 0.64, s * 0.4, 12, color)
        c.fill_rrect(bx + (0 if facing < 0 else s * 0.52) - (s * 0.2 if facing < 0 else 0), by + s * 0.12,
                     s * 0.32, s * 0.14, 6, ink2)                                    # barrel
        c.fill_rrect(x - s * 0.08, by - s * 0.5, s * 0.16, s * 0.5, 6, c.theme("card", "d_card"))   # tube
        c.stroke_rrect(x - s * 0.08, by - s * 0.5, s * 0.16, s * 0.5, 6, ink2, 2)
        for k in range(4):
            c.circle(x, by - s * 0.42 + k * s * 0.1, s * 0.04, color)


def rep_dots(c, x, y, n, n_on, color=None, r=8, gap=24, alpha=1.0):
    """Row of n repetition dots starting at (x, y); n_on (float) filled, the last one fading in."""
    color = color or ORANGE
    for k in range(n):
        f = clamp(n_on - k)
        c.circle(x + k * gap, y, r, c.theme("faint", "d_line"), alpha)
        if f > 0:
            c.circle(x + k * gap, y, r * (0.6 + 0.4 * out_expo(f)), color, alpha * f)


# ── coach's schedule + venues ───────────────────────────────────────────
def jadwal(c, x, y, w, rows, t, title="JADWAL PELATIH", playhead=None, color=None, row_h=70, alpha=1.0):
    """Schedule board. rows: [{label, blocks: [(f0, f1)], color, p (0..1 reveal), struck: (f0, f1) or None}].
    playhead 0..1 = current time marker across the timeline."""
    color = color or ORANGE
    h = 70 + len(rows) * row_h + 20
    lx = x + 190
    tw = w - 190 - 30
    with c.group(alpha):
        c.card(x, y, w, h, r=24)
        c.text(x + 28, y + 50, title, tk.F["serif"], 40, c.theme("ink2", "d_ink"), 1)
        for i, r in enumerate(rows):
            ry = y + 80 + i * row_h
            c.text(x + 28, ry + row_h * 0.55, r["label"], tk.F["mono_med"], 19, c.theme("ink2", "d_ink"), 1, 0.02)
            c.fill_rrect(lx, ry + row_h * 0.25, tw, row_h * 0.5, 8, c.theme("bg", "d_bg"))
            p = clamp(r.get("p", 1.0))
            col = r.get("color", color)
            for f0, f1 in r.get("blocks", ()):
                if p <= f0:
                    continue
                e = min(f1, p)
                c.fill_rrect(lx + tw * f0, ry + row_h * 0.25, tw * (e - f0), row_h * 0.5, 8, col)
            st = r.get("struck")
            if st:
                sx0, sx1 = lx + tw * st[0], lx + tw * st[1]
                c.stroke_rrect(sx0, ry + row_h * 0.25, sx1 - sx0, row_h * 0.5, 8, tk.C["rec"], 2, dash=[6, 6])
                c.line(sx0 + 6, ry + row_h * 0.5, sx1 - 6, ry + row_h * 0.5, tk.C["rec"], 4)
        if playhead is not None:
            px = lx + tw * clamp(playhead)
            c.line(px, y + 70, px, y + h - 14, c.theme("accent", "d_accent"), 3)
            c.circle(px, y + 70, 7, c.theme("accent", "d_accent"))


def gor(c, x, y, w, h, label, sub=None, ok=0.0, color=None, alpha=1.0):
    """Sports hall card (arched roof) = one cloud. ok 0..1 pops a check on the roof."""
    color = color or ORANGE
    with c.group(alpha):
        c.card(x, y, w, h, r=22)
        cxx = c.ctx
        rx, ry, rw = x + 30, y + h * 0.55, w - 60
        cxx.new_path()
        cxx.move_to(rx, ry)
        cxx.curve_to(rx + rw * 0.1, ry - h * 0.32, rx + rw * 0.9, ry - h * 0.32, rx + rw, ry)
        cxx.close_path()
        c.src(mix(c.theme("card", "d_card"), color, 0.25))
        cxx.fill_preserve()
        c.src(color)
        cxx.set_line_width(4)
        cxx.stroke()
        c.fill_rrect(rx, ry, rw, h * 0.18, 4, mix(c.theme("card", "d_card"), color, 0.12))
        for k in range(5):
            c.fill_rrect(rx + 14 + k * (rw - 28) / 5, ry + 10, (rw - 28) / 5 - 10, h * 0.1, 3,
                         c.theme("faint", "d_line"))
        c.text(x + w / 2, y + h - 44, label, tk.F["display_semi"], 30, c.theme("ink", "d_ink"), 1, -0.02, align="c")
        if sub:
            c.text(x + w / 2, y + h - 16, sub, tk.F["mono_med"], 17, c.theme("muted", "d_muted"), 1, 0.06, align="c")
        if ok > 0.01:
            from .icons import check
            cx_, cy_ = x + w - 34, y + 34
            with c.at(0, 0, max(0.01, ok), origin=(cx_, cy_)):
                c.circle(cx_, cy_, 22, tk.C["ok"])
                check(c, cx_, cy_, 18, WHITE, 3.5)
