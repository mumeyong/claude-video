"""Dark-section components: recap diagram (steps → rules) and the outro CTA."""
from .. import tokens as tk
from ..ease import prog, in_out_cubic, pulse, pop
from . import icons
from .motion import bezier_partial


def step_row(c, x, y, w, num, label, active=0.0, h=62):
    """Left-column chapter row ('01 ATURAN'). active 0..1 brightens it."""
    c.fill_rrect(x, y, w, h, 14, tk.C["d_card"], 0.55 + 0.45 * active)
    c.stroke_rrect(x + 0.5, y + 0.5, w - 1, h - 1, 14, tk.C["d_line"], 1, 0.5 + 0.5 * active)
    c.fill_rrect(x + 14, y + 16, 38, 30, 8, (1, 1, 1, 0.06))
    c.text(x + 33, y + 38, f"{num:02d}", tk.F["mono_med"], 17, tk.C["d_muted"], 0.6 + 0.4 * active, align="c")
    col = tuple(a + (b - a) * active for a, b in zip(tk.C["d_muted"], tk.C["d_ink"]))
    c.text(x + 66, y + 40, label, tk.F["ui_semi"], 24, col, 1, -0.02)


def rule_box(c, x, y, w, idx, label, color, fill=0.0, h=62):
    """Right-column rule slot. fill 0 = dashed empty slot, 1 = filled with numbered label."""
    if fill < 1:
        c.stroke_rrect(x, y, w, h, 14, tk.C["d_line"], 1.5, 1 - fill, dash=[6, 6])
        c.stroke_rrect(x + 18, y + 20, 22, 22, 5, color, 2, 0.6 * (1 - fill))
    if fill > 0:
        s = 0.9 + 0.1 * pop(fill)
        with c.at(0, 0, s, origin=(x + w / 2, y + h / 2)):
            c.fill_rrect(x, y, w, h, 14, (0.12, 0.17, 0.32, 1), fill)
            c.stroke_rrect(x + 0.5, y + 0.5, w - 1, h - 1, 14, tk.C["d_accent"], 1.5, 0.5 * fill)
            c.fill_rrect(x + 18, y + 20, 22, 22, 5, color, fill)
            c.text(x + 29, y + 37, str(idx), tk.F["mono_bold"], 15, (0.05, 0.05, 0.1, 1), fill, align="c")
            c.text(x + 54, y + 40, label, tk.F["ui_semi"], 24, tk.C["d_ink"], fill, -0.02)


def connector(c, x1, y1, x2, y2, p, color=None, width=2.5):
    """S-curve from (x1,y1) to (x2,y2), drawn to fraction p."""
    if p <= 0:
        return
    mx = (x1 + x2) / 2
    bezier_partial(c, (x1, y1), (mx, y1), (mx, y2), (x2, y2), p)
    c.src(color or tk.C["d_accent"], 0.9)
    c.ctx.set_line_width(width)
    c.ctx.stroke()


def segments(c, x, y, n, k, w=34, gap=10, h=4):
    """'━━ ━━ ── ── ──  02 / 05' progress."""
    for i in range(n):
        col = tk.C["d_accent"] if i < k else (1, 1, 1, 0.18)
        c.fill_rrect(x + i * (w + gap), y, w, h, 2, col)
    c.text(x + n * (w + gap) + 14, y + 8, f"{k:02d} / {n:02d}", tk.F["mono"], 19, tk.C["d_muted"], 1, 0.1)


# ── outro ───────────────────────────────────────────────────────────────
def follow_button(c, cx, y, t, t_click, w=300, h=72):
    """'+ Follow' (blue) → pressed at t_click → '✓ Following' (dark)."""
    p = in_out_cubic(prog(t, t_click + 0.08, 0.3))
    press = pulse(t, t_click, 0.22)
    s = 1 - 0.07 * press
    with c.at(0, 0, s, origin=(cx, y + h / 2)):
        blue = tk.C["accent"]
        dark = (0.13, 0.15, 0.2, 1)
        col = tuple(a + (b - a) * p for a, b in zip(blue, dark))
        c.shadow(cx - w / 2, y, w, h, h / 2, 26, 10, 0.35 * (1 - p), blue)
        c.fill_rrect(cx - w / 2, y, w, h, h / 2, col)
        c.text(cx, y + h / 2 + 10, "+ Follow", tk.F["ui_bold"], 28, (1, 1, 1, 1), 1 - p, -0.02, align="c")
        if p > 0:
            icons.check(c, cx - 78, y + h / 2, 22, (1, 1, 1, 1), 3, p, p)
            c.text(cx + 14, y + h / 2 + 10, "Following", tk.F["ui_bold"], 28, (1, 1, 1, 1), p, -0.02, align="c")


def contact_pill(c, cx, y, text, sub="", color=None, icon="globe", w=None, h=64, alpha=1.0):
    """Dark pill with icon + bold text + tiny mono sub-label ('mumeyong.dev  SITUS')."""
    tw = c.measure(text, tk.F["ui_bold"], 28, -0.02)[0]
    sw = c.measure(sub, tk.F["mono_med"], 14, 0.2)[0] if sub else 0
    w = w or tw + sw + 110
    x = cx - w / 2
    fill = color or (0.10, 0.12, 0.17, 1)
    c.fill_rrect(x, y, w, h, h / 2, fill, alpha)
    ink = (1, 1, 1, 1)
    if icon == "globe":
        icons.globe(c, x + 38, y + h / 2, 24, ink, alpha=alpha)
    elif icon == "wa":
        icons.wa(c, x + 38, y + h / 2, 24, ink, alpha=alpha)
    c.text(x + 64, y + h / 2 + 10, text, tk.F["ui_bold"], 28, ink, alpha, -0.02)
    if sub:
        c.text(x + 64 + tw + 14, y + h / 2 + 6, sub, tk.F["mono_med"], 14, ink, 0.6 * alpha, 0.2)
