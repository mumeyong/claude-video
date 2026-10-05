"""Content widgets: stat tiles, waveform, REC bar, filmstrip, phone, comment bubble, cursor."""
import math

from .. import tokens as tk
from ..ease import out_expo, in_out_cubic, prog, pulse, clamp, lerp
from . import icons
from .motion import count, fmt_id


def _rand(i, seed=0):
    """Deterministic hash noise in [0, 1)."""
    x = math.sin(i * 12.9898 + seed * 78.233) * 43758.5453
    return x - math.floor(x)


# ── stat tile ───────────────────────────────────────────────────────────
def stat(c, x, y, w, h, value, label, t, t0, decimals=0, suffix="", dur=1.2, highlight=False):
    """Count-up stat card ('2.951' / 'baris kode'). Indonesian number format."""
    c.card(x, y, w, h, r=18)
    v = count(t, t0, dur, 0, value)
    col = c.theme("accent", "d_accent") if highlight else c.theme("accent", "d_accent")
    size, ls, _ = tk.T["stat"]
    c.text(x + w / 2, y + h * 0.58, fmt_id(v, decimals) + suffix, tk.F["display"], size, col, 1, ls, align="c")
    c.text(x + w / 2, y + h * 0.84, label, tk.F["ui"], 18, c.theme("muted", "d_muted"), 1, align="c")


def big_number(c, x, y, value, t, t0, decimals=1, suffix=" s", caption="", sub="", dur=1.0):
    """Free-standing big number with mono caption above ('WAKTU VIDEO / 44,4 s / frame 2.663')."""
    if caption:
        c.text(x, y - 74, caption, tk.F["mono_med"], 17, c.theme("muted", "d_muted"), 1, 0.18)
    v = count(t, t0, dur, 0, value)
    c.text(x, y, fmt_id(v, decimals) + suffix, tk.F["display"], 64, c.theme("ink", "d_ink"), 1, -0.04)
    if sub:
        c.text(x, y + 40, sub, tk.F["mono"], 20, c.theme("muted", "d_muted"), 1)


# ── waveform ────────────────────────────────────────────────────────────
def waveform(c, x, y, w, h, t, t0, dur, colors=None, bar=5, gap=3, seed=1, segments=None, env=None):
    """Waveform drawn left→right from t0 over dur. y is the center line.

    colors: list of colors cycled per segment; segments: list of fractions where segments split
    (draws 'S1/S2' style markers). env: optional list of 0..1 amplitudes (real VO envelope).
    """
    colors = colors or [tk.C["accent"]]
    n = int(w // (bar + gap))
    p = in_out_cubic(prog(t, t0, dur))
    shown = int(n * p)
    seg_edges = [int(f * n) for f in (segments or [])]
    for i in range(n):
        bx = x + i * (bar + gap)
        if i >= shown:
            c.line(bx, y, x + w, y, c.theme("faint", "d_line"), 1.5)
            break
        if env is not None:
            a = env[int(i / n * len(env))]
        else:
            word = 0.35 + 0.65 * abs(math.sin(i * 0.21 + seed)) * (0.5 + 0.5 * math.sin(i * 0.05 + seed * 3))
            a = clamp(word * (0.55 + 0.45 * _rand(i, seed)))
            if (i // 9 + seed) % 7 == 0:
                a *= 0.12  # gaps between words
        seg = sum(1 for e in seg_edges if i >= e)
        col = colors[seg % len(colors)]
        bh = max(3, a * h)
        c.fill_rrect(bx, y - bh / 2, bar, bh, bar / 2, col)
    for k, e in enumerate(seg_edges):
        if e < shown:
            ex = x + e * (bar + gap) - gap / 2
            c.line(ex, y - h * 0.62, ex, y + h * 0.55, c.theme("ink2", "d_ink"), 2)
            c.circle(ex, y - h * 0.62, 4, c.theme("ink2", "d_ink"))


def rec_bar(c, x, y, w, t, t0, h=84):
    """Recording pill: red mic button, blinking REC, running timer, live red bars."""
    c.card(x, y, w, h, r=h / 2)
    c.circle(x + h / 2, y + h / 2, h / 2 - 12, tk.C["rec"])
    icons.mic(c, x + h / 2, y + h / 2, 26, (1, 1, 1, 1), 2.2)
    blink = 1.0 if (t * 1.2) % 1 < 0.6 else 0.25
    c.circle(x + h + 22, y + h / 2, 7, tk.C["rec"], blink)
    c.text(x + h + 40, y + h / 2 + 8, "REC", tk.F["mono_bold"], 22, c.theme("ink", "d_ink"), 1, 0.1)
    el = max(0.0, t - t0)
    c.text(x + h + 140, y + h / 2 + 9, f"{int(el // 60):02d}:{el % 60:04.1f}", tk.F["mono_med"], 26,
           c.theme("ink", "d_ink"), 1)
    bx0 = x + h + 300
    n = int((x + w - 30 - bx0) // 10)
    for i in range(n):
        a = 0.2 + 0.8 * abs(math.sin(t * 9 + i * 0.7)) * _rand(i + int(t * 12), 3)
        bh = 8 + a * 34 * (i / n) ** 0.4
        c.fill_rrect(bx0 + i * 10, y + h / 2 - bh / 2, 4, bh, 2, tk.C["rec"])


# ── filmstrip / phone ───────────────────────────────────────────────────
def filmstrip(c, x, y, w, h, images, t, head=None, head_label=None, colors=None):
    """Row of thumbnails in a card with an optional blue playhead at fraction `head`."""
    c.card(x, y, w, h, r=16)
    n = max(1, len(images) if images else len(colors or []) or 8)
    gap = 8
    tw = (w - 24 - gap * (n - 1)) / n
    for i in range(n):
        tx = x + 12 + i * (tw + gap)
        if images:
            c.image(images[i], tx, y + 12, tw, h - 24, r=6)
        else:
            col = (colors or [tk.C["faint"]])[i % len(colors or [1])]
            c.fill_rrect(tx, y + 12, tw, h - 24, 6, col)
    if head is not None:
        hx = x + 12 + (w - 24) * head
        c.line(hx, y - 24, hx, y + h + 36, c.theme("accent", "d_accent"), 3)
        if head_label:
            from .pill import size_label
            size_label(c, hx, y - 58, head_label)


def phone(c, x, y, w, h, image=None, draw_screen=None, dark=True):
    """Phone mockup. Either an image path or draw_screen(c, sx, sy, sw, sh)."""
    r = w * 0.13
    c.shadow(x, y, w, h, r, 40, 18, 0.25)
    c.fill_rrect(x, y, w, h, r, (0.05, 0.05, 0.07, 1) if dark else (1, 1, 1, 1))
    b = w * 0.035
    sx, sy, sw, sh = x + b, y + b, w - 2 * b, h - 2 * b
    if image:
        c.image(image, sx, sy, sw, sh, r=r - b)
    elif draw_screen:
        with c.clip(sx, sy, sw, sh, r - b):
            draw_screen(c, sx, sy, sw, sh)


# ── comment bubble (hook) ───────────────────────────────────────────────
def comment(c, x, y, w, user, text, initial=None, highlight=None):
    """TikTok 'Balas komentar' bubble with tail. text may contain \\n. highlight = substring to mark."""
    size, ls, lh = tk.T["comment"]
    lines = text.split("\n")
    h = 92 + len(lines) * size * lh
    cx = c.ctx
    c.shadow(x, y, w, h, 26, 40, 16, 0.22)
    c.fill_rrect(x, y, w, h, 26, (1, 1, 1, 1))
    cx.new_path()
    cx.move_to(x + 6, y + h - 30); cx.line_to(x, y + h + 26); cx.line_to(x + 50, y + h - 2); cx.close_path()
    c.src((1, 1, 1, 1)); cx.fill()
    c.circle(x + 56, y + 58, 26, (0.92, 0.93, 0.95, 1))
    c.text(x + 56, y + 68, (initial or user[:1]).upper(), tk.F["ui_semi"], 28, tk.C["muted"], 1, align="c")
    c.text(x + 104, y + 46, f"Balas komentar {user}", tk.F["ui_reg"], 24, tk.C["muted"], 1)
    for i, ln in enumerate(lines):
        by = y + 92 + i * size * lh
        if highlight and highlight in ln:
            pre = ln.split(highlight)[0]
            hx = x + 104 + c.measure(pre, tk.F["ui_bold"], size, ls)[0]
            hw = c.measure(highlight, tk.F["ui_bold"], size, ls)[0]
            c.fill_rrect(hx - 2, by - size * 0.35, hw + 4, size * 0.42, 3, (1.0, 0.86, 0.2, 0.75))
        c.text(x + 104, by, ln, tk.F["ui_bold"], size, tk.C["ink"], 1, ls)


# ── cursor ──────────────────────────────────────────────────────────────
class Cursor:
    """Mouse pointer moving through keyframes [(t, x, y)], clicking at times in `clicks`."""

    def __init__(self, keys, clicks=(), show=None, hide=None):
        self.keys = sorted(keys)
        self.clicks = list(clicks)
        self.show = self.keys[0][0] - 0.3 if show is None else show
        self.hide = hide

    def pos(self, t):
        ks = self.keys
        if t <= ks[0][0]:
            return ks[0][1:]
        for (t0, x0, y0), (t1, x1, y1) in zip(ks, ks[1:]):
            if t0 <= t <= t1:
                p = in_out_cubic(prog(t, t0, t1 - t0))
                # slight arc so moves feel hand-made
                arc = math.sin(math.pi * p) * 0.08 * math.hypot(x1 - x0, y1 - y0)
                return lerp(x0, x1, p), lerp(y0, y1, p) - arc
        return ks[-1][1:]

    def cues(self):
        return [("click", t, 0.7) for t in self.clicks]

    def draw(self, c, t):
        a = out_expo(prog(t, self.show, 0.3))
        if self.hide is not None:
            a *= 1 - prog(t, self.hide, 0.3)
        if a <= 0.002:
            return
        x, y = self.pos(t)
        press = max((pulse(t, ct, 0.2) for ct in self.clicks), default=0.0)
        for ct in self.clicks:
            rp = prog(t, ct, 0.5)
            if 0 < rp < 1:
                c.ctx.new_path()
                c.ctx.arc(x, y, 8 + 36 * out_expo(rp), 0, 6.2832)
                c.src(tk.C["accent"], 0.45 * (1 - rp) * a)
                c.ctx.set_line_width(3)
                c.ctx.stroke()
        with c.at(0, 0, 1 - 0.15 * press, origin=(x, y)):
            icons.pointer(c, x, y, 36, a)
