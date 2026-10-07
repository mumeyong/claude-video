"""Commuter-line (KRL) components (first used in "roadmap-cloud-engineer").

route_strip · train · cert_card · save_button
Signature move they share: the train glides to the next station and every station it passed lights up.
Pure functions of their progress values and t.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, out_expo, out_back, in_out_cubic, prog, pulse
from .infra import _draw_poly

ORANGE = tk.CHAPTER[2][0]
WHITE = (1, 1, 1, 1)


# ── vertical route with stations ────────────────────────────────────────
def route_strip(c, x, ys, t, p_draw=1.0, reach=0.0, lit=(), names=(), subs=(), color=None, label_a=1.0, dead=(),
                active=None, width=14):
    """Vertical line at x through stations at ys (top→bottom).
    p_draw 0..1 draws the grey track; reach 0..1 = how far down the line is colored (the train's progress).
    lit[k] 0..1 fills station k; dead[k] 0..1 greys it out (skipped); active = index with a pulsing ring.
    names/subs: labels right of each station."""
    color = color or ORANGE
    y0, y1 = ys[0] - 60, ys[-1] + 60
    faint = c.theme("faint", "d_line")
    yd = y0 + (y1 - y0) * in_out_cubic(clamp(p_draw))
    if p_draw > 0:
        c.line(x, y0, x, yd, faint, width)
    if reach > 0:
        c.line(x, y0, x, min(yd, y0 + (y1 - y0) * clamp(reach)), color, width)
    for k, y in enumerate(ys):
        a = clamp((yd - y) / 40 + 1)
        if a <= 0:
            continue
        lk = clamp(lit[k]) if k < len(lit) else 0.0
        dk = clamp(dead[k]) if k < len(dead) else 0.0
        ring = mix(mix(faint, color, lk), faint, dk)
        s = out_back(a, 1.8)
        c.circle(x, y, 26 * s, c.theme("card", "d_card"), a)
        c.ctx.new_path()
        c.ctx.arc(x, y, 22 * s, 0, 2 * math.pi)
        c.src(ring, a)
        c.ctx.set_line_width(8)
        c.ctx.stroke()
        if lk > 0:
            c.circle(x, y, 13 * s * lk * (1 - dk), color, a)
        if active == k:
            ph = (t * 0.9) % 1.0
            c.ctx.new_path()
            c.ctx.arc(x, y, 26 + 26 * out_expo(ph), 0, 2 * math.pi)
            c.src(color, 0.5 * (1 - ph) * a)
            c.ctx.set_line_width(3)
            c.ctx.stroke()
        la = a * label_a * (1 - 0.6 * dk)
        if la > 0 and k < len(names):
            ink = mix(c.theme("ink2", "d_muted"), c.theme("ink", "d_ink"), lk)
            if k < len(subs) and subs[k]:
                c.text(x + 52, y - 20, subs[k], tk.F["mono_bold"], 17, mix(c.theme("muted", "d_muted"), color, lk),
                       la, 0.14)
            c.text(x + 52, y + 18, names[k], tk.F["display_semi"], 36, ink, la, -0.03)


# ── train (front view) ──────────────────────────────────────────────────
def train(c, cx, cy, s, color=None, alpha=1.0, ghost=False, t=0.0):
    """Commuter train seen from the front, centered (cx, cy), height s. ghost = dashed outline only."""
    if alpha <= 0.002:
        return
    color = color or ORANGE
    w, h = s * 0.66, s
    x, y = cx - w / 2, cy - h / 2
    r = w * 0.32
    if ghost:
        c.stroke_rrect(x, y, w, h, r, color, 3, alpha, dash=[10, 8])
        c.stroke_rrect(x + w * 0.14, y + h * 0.12, w * 0.72, h * 0.3, r * 0.4, color, 2, alpha * 0.7, dash=[6, 6])
        return
    with c.group(alpha):
        c.shadow(x, y, w, h, r, 24, 10, 0.18)
        c.fill_rrect(x, y, w, h, r, color)
        c.fill_rrect(x + w * 0.12, y + h * 0.1, w * 0.76, h * 0.32, r * 0.45, mix(WHITE, color, 0.12))
        c.line(x + w * 0.16, y + h * 0.2, x + w * 0.4, y + h * 0.14, WHITE, 3, 0.8)
        c.fill_rrect(x, y + h * 0.52, w, h * 0.08, 0, WHITE, 0.85)
        c.fill_rrect(x + w * 0.38, y + h * 0.64, w * 0.24, h * 0.1, 4, mix(color, (0, 0, 0, 1), 0.25))
        glow = 0.75 + 0.25 * math.sin(t * 4)
        for sx in (x + w * 0.2, x + w * 0.8):
            c.circle(sx, y + h * 0.82, w * 0.08, (1, 0.96, 0.8, 1), glow)


# ── certificate = ticket ────────────────────────────────────────────────
def cert_card(c, x, y, w, h, title, sub="", color=None, alpha=1.0, rot=0.0, label="SERTIFIKAT"):
    """Certificate drawn as a perforated ticket: notches, stub with a seal, mono label, title."""
    if alpha <= 0.002:
        return
    color = color or ORANGE
    with c.at(0, 0, 1.0, origin=(x + w / 2, y + h / 2), rot=rot):
        with c.group(alpha):
            c.card(x, y, w, h, r=18)
            bg = c.theme("bg", "d_bg")
            sx = x + w * 0.72
            for yy in (y, y + h):
                c.circle(sx, yy, 16, bg)
            c.ctx.set_dash([6, 8])
            c.line(sx, y + 22, sx, y + h - 22, c.theme("faint", "d_line"), 2.5)
            c.ctx.set_dash([])
            c.fill_rrect(x, y, 12, h, 6, color)
            c.text(x + 34, y + 44, label, tk.F["mono_bold"], 17, color, 1, 0.16)
            c.text(x + 34, y + h * 0.62, title, tk.F["display_semi"], min(44, h * 0.3), c.theme("ink", "d_ink"), 1, -0.03)
            if sub:
                c.text(x + 34, y + h - 26, sub, tk.F["mono_med"], 17, c.theme("muted", "d_muted"), 1, 0.06)
            mx, my, mr = sx + (x + w - sx) / 2, y + h / 2, min(h * 0.24, (x + w - sx) * 0.34)
            c.circle(mx, my, mr, color, 0.18)
            c.ctx.new_path()
            c.ctx.arc(mx, my, mr, 0, 2 * math.pi)
            c.src(color)
            c.ctx.set_line_width(3)
            c.ctx.stroke()
            c.circle(mx, my, mr * 0.45, color)


# ── save (bookmark) CTA ─────────────────────────────────────────────────
def _bookmark(c, x, y, s, color, fill=0.0, alpha=1.0):
    w, h = s * 0.7, s
    cx_ = c.ctx
    cx_.new_path()
    cx_.move_to(x - w / 2, y - h / 2)
    cx_.line_to(x + w / 2, y - h / 2)
    cx_.line_to(x + w / 2, y + h / 2)
    cx_.line_to(x, y + h * 0.2)
    cx_.line_to(x - w / 2, y + h / 2)
    cx_.close_path()
    if fill > 0:
        c.src(color, alpha * fill)
        cx_.fill_preserve()
    c.src(color, alpha)
    cx_.set_line_width(3)
    cx_.set_line_join(1)
    cx_.stroke()


def save_button(c, cx, y, t, t_click, w=300, h=72):
    """'Save' (outlined bookmark) → pressed at t_click → 'Tersimpan' with a filled bookmark."""
    p = in_out_cubic(prog(t, t_click + 0.08, 0.3))
    press = pulse(t, t_click, 0.22)
    with c.at(0, 0, 1 - 0.07 * press, origin=(cx, y + h / 2)):
        col = mix(c.theme("card", "d_card"), ORANGE, p)
        c.fill_rrect(cx - w / 2, y, w, h, h / 2, col)
        c.stroke_rrect(cx - w / 2, y, w, h, h / 2, c.theme("line", "d_line"), 1.5, 1 - p)
        ink = mix(c.theme("ink", "d_ink"), WHITE, p)
        _bookmark(c, cx - 70, y + h / 2, 28, ink, fill=p)
        c.text(cx + 18, y + h / 2 + 10, "Save", tk.F["ui_bold"], 28, ink, 1 - p, -0.02, align="c")
        c.text(cx + 18, y + h / 2 + 10, "Tersimpan", tk.F["ui_bold"], 28, ink, p, -0.02, align="c")


def station_dots(c, x0, x1, y, n, lit, color=None, r=14):
    """Compact horizontal route (recap bookend): n stations between x0 and x1, lit 0..1 each."""
    color = color or ORANGE
    faint = c.theme("faint", "d_line")
    c.line(x0, y, x1, y, faint, 8)
    done = clamp((sum(clamp(v) for v in lit) - 1) / max(1, n - 1))
    if done > 0:
        c.line(x0, y, x0 + (x1 - x0) * done, y, color, 8)
    for k in range(n):
        px = x0 + (x1 - x0) * k / (n - 1)
        lk = clamp(lit[k]) if k < len(lit) else 0
        c.circle(px, y, r + 4, c.theme("card", "d_card"))
        c.circle(px, y, r, mix(faint, color, lk))
        c.text(px, y + r + 36, str(k + 1), tk.F["mono_bold"], 20, mix(c.theme("muted", "d_muted"), color, lk), 1, 0.04,
               align="c")
