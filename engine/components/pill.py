"""Pills, chips, tags, selection boxes — the small UI vocabulary."""
from .. import tokens as tk
from ..ease import out_back, out_expo, prog


def chip(c, x, y, label, dot, alpha=1.0, h=40):
    """Context chip ('● CLAUDE.md') — white pill, colored dot. Returns width."""
    size, ls, _ = tk.T["chip"]
    tw = c.measure(label, tk.F["ui_semi"], size, ls)[0]
    w = tw + 50
    sh = tk.SHADOW["card_tight"]
    c.shadow(x, y, w, h, h / 2, sh["blur"], sh["dy"], sh["alpha"] * alpha)
    c.fill_rrect(x, y, w, h, h / 2, c.theme("card", "d_card"), alpha)
    c.circle(x + 19, y + h / 2, 4.5, dot, alpha)
    c.text(x + 32, y + h / 2 + 8, label, tk.F["ui_semi"], size, c.theme("ink2", "d_ink"), alpha, ls)
    return w


def chip_width(c, label):
    size, ls, _ = tk.T["chip"]
    return c.measure(label, tk.F["ui_semi"], size, ls)[0] + 50


def tag(c, x, y, label, color=None, alpha=1.0, align="l", h=36):
    """Soft blue tag ('ukuran video'). align='r' puts its right edge at x. Returns width."""
    color = color or tk.C["accent"]
    size, ls, _ = tk.T["tag"]
    w = c.measure(label, tk.F["ui"], size, ls)[0] + 30
    if align == "r":
        x -= w
    c.fill_rrect(x, y, w, h, h / 2, (*color[:3], 0.10), alpha)
    c.text(x + 15, y + h / 2 + 7, label, tk.F["ui"], size, color, alpha, ls)
    return w


def word_pill(c, x, y, word, color, size=104, alpha=1.0, pad_x=34, pad_y=18):
    """Big colored pill with white display text ('keyframe.' / 'kode.'). Returns (w, h)."""
    f = tk.F["display"]
    ls = -0.055
    tw, _, _ = c.measure(word, f, size, ls)
    w, h = tw + pad_x * 2, size * 0.98 + pad_y * 2
    sh = tk.SHADOW["pill"]
    c.shadow(x, y, w, h, h / 2, sh["blur"], sh["dy"], sh["alpha"] * alpha, color)
    c.fill_rrect(x, y, w, h, h / 2, color, alpha)
    c.text(x + pad_x, y + pad_y + size * 0.78, word, f, size, (1, 1, 1, 1), alpha, ls)
    return w, h


def size_label(c, cx, y, text, alpha=1.0):
    """Tiny blue pill with white mono text, centered at cx ('522 × 148')."""
    size, ls, _ = tk.T["label"]
    w = c.measure(text, tk.F["mono_med"], size, ls)[0] + 20
    h = 28
    c.fill_rrect(cx - w / 2, y, w, h, 6, tk.C["accent"], alpha)
    c.text(cx, y + 20, text, tk.F["mono_med"], size, (1, 1, 1, 1), alpha, ls, align="c")


def select_box(c, t, t0, x, y, w, h, label=None, t_out=None, pad=10):
    """Design-tool selection: blue frame + square handles + size label. Pops in at t0."""
    p = out_expo(prog(t, t0, 0.45))
    b = 0.0 if t_out is None else prog(t, t_out, 0.25)
    vis = p * (1 - b)
    if vis <= 0.002:
        return
    acc = c.theme("accent", "d_accent")
    s = 0.92 + 0.08 * out_back(prog(t, t0, 0.45))
    x0, y0, ww, hh = x - pad, y - pad, w + 2 * pad, h + 2 * pad
    with c.at(0, 0, s, origin=(x0 + ww / 2, y0 + hh / 2)):
        c.stroke_rrect(x0, y0, ww, hh, 2, acc, 2.0, vis)
        for hx, hy in ((x0, y0), (x0 + ww, y0), (x0, y0 + hh), (x0 + ww, y0 + hh)):
            c.fill_rrect(hx - 6, hy - 6, 12, 12, 2, (1, 1, 1, 1), vis)
            c.stroke_rrect(hx - 6, hy - 6, 12, 12, 2, acc, 2.0, vis)
    if label:
        size_label(c, x0 + ww / 2, y0 + hh + 12, label, vis)


def strike(c, t, t0, x1, x2, y, width=7, dur=0.5, alpha=1.0):
    """Blue strike-through drawn left→right."""
    p = out_expo(prog(t, t0, dur))
    if p > 0:
        c.line(x1, y, x1 + (x2 - x1) * p, y, c.theme("accent", "d_accent"), width, alpha)
