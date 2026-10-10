"""Headline + kicker — the signature element.

Headline syntax:
    "Kasih *aturan* main."        *word*  → accent blue
    "Tulis _tiap_ detiknya."      _word_  → italic serif, accent blue
    "Bukan ~satu prompt~."        ~words~ → strike-through target (animate with strike_at)
    "Lalu buku\\npanduan *gaya*."  \\n     → forced line break (else wraps to column width)
"""
import re

from .. import tokens as tk
from ..ease import curve, out_expo, in_cubic, in_out_cubic, mix, prog
from .motion import appear  # noqa: F401  (re-export convenience)

_TOKEN = re.compile(r"([*_~])[^*_~]+?\1[.,:;!?]*|\S+")
_MARKED = re.compile(r"^([*_~])(.+?)\1([.,:;!?]*)$")
_KIND = {"*": "accent", "_": "serif", "~": "plain"}


def _parse(text):
    """→ list of lines; each line = list of (word, kind, strike)."""
    lines = []
    for raw in text.split("\n"):
        words = []
        for m in _TOKEN.finditer(raw):
            tok = m.group(0)
            mm = _MARKED.match(tok)
            if not mm:
                words.append((tok, "plain", False))
                continue
            mark, inner, punct = mm.groups()
            parts = inner.split()  # a marker may span several words: "*dua kata*"
            for i, w in enumerate(parts):
                # punctuation right after the marker sticks to the last word; words() splits it back to ink
                words.append((w + (punct if i == len(parts) - 1 else ""), _KIND[mark], mark == "~"))
        lines.append(words)
    return lines


class Headline:
    def __init__(self, text, x=None, y=None, style="headline", width=None, ink="ink", accent="accent", align="l"):
        """align='c' centers each line on x (default x = canvas center)."""
        self.text = text
        self.align = align
        if align == "c" and x is None:
            x = tk.W / 2
        self.x = tk.L["col_x"] if x is None else x
        self.y = tk.L["headline_y"] if y is None else y
        self.size, self.ls, self.lh = tk.T[style]
        self.width = width or tk.L["col_w"] + 60
        self.ink, self.accent = ink, accent
        self._words = None  # [(word, kind, strike, x, baseline, w)]

    def _font(self, kind):
        if kind == "serif":
            return tk.F["serif"], self.size * tk.SERIF_SCALE, 0.0
        return tk.F["display"], self.size, self.ls

    def words(self, c):
        if self._words is not None:
            return self._words
        out = []
        base = self.y + self.size * 0.75
        lh = self.size * self.lh
        space = c.measure("a a", tk.F["display"], self.size, self.ls)[0] - c.measure("aa", tk.F["display"], self.size, self.ls)[0]
        line_i = 0
        x0 = self.x - self.width / 2 if self.align == "c" else self.x
        for line in _parse(self.text):
            x = x0
            for (w, kind, strike) in line:
                # split trailing punctuation from a marked word so "." stays ink
                m = re.match(r"^(.*?)([.,:;!?]+)$", w) if kind != "plain" else None
                parts = [(m.group(1), kind), (m.group(2), "plain")] if m and m.group(1) else [(w, kind)]
                ww = sum(c.measure(p, *self._font(k))[0] for p, k in parts)
                if x > x0 and x + ww > x0 + self.width:
                    line_i += 1
                    x = x0
                for p, k in parts:
                    f, s, ls = self._font(k)
                    pw = c.measure(p, f, s, ls)[0]
                    out.append((p, k, strike, x, base + line_i * lh, pw))
                    x += pw + (2 if k == "serif" else 0)
                x += space
            line_i += 1
        if self.align == "c":  # re-center each line on self.x
            lines = {}
            for w in out:
                lo, hi = lines.get(w[4], (1e9, -1e9))
                lines[w[4]] = (min(lo, w[3]), max(hi, w[3] + w[5]))
            out = [(w, k, s_, x_ + self.x - (lines[b][0] + lines[b][1]) / 2, b, pw)
                   for (w, k, s_, x_, b, pw) in out]
        self._words = out
        return out

    def bottom(self, c):
        ws = self.words(c)
        return (ws[-1][4] if ws else self.y) + self.size * 0.28

    def draw(self, c, t, t_in, t_out=None, strike_at=None, stagger=None, reveal="blur", exit="blur"):
        """Words blur+rise in one by one from t_in; all blur out from t_out.
        reveal: "blur" (default) · "mask" (each word springs up from behind its baseline, kinetic.py)
                · "ink" (Apple: whole line fades in faint, then words ink in one by one)
                · "rise" (Apple: each LINE fades up as one piece on an iOS spring, opacity first, no blur)
                · "wipe" (Apple keynote title: a feathered mask sweeps across each line)
        exit:   "blur" (default) · "mask" (words leave up through the mask) · "dim" (drain to grey, then fade)
                · "quiet" (Apple: fade + slight drop in scale, faster than the entrance)"""
        M = tk.M
        if reveal in ("rise", "wipe"):
            return self._draw_apple(c, t, t_in, t_out, strike_at, stagger, reveal, exit)
        if reveal != "blur" or exit != "blur":
            return self._draw_kinetic(c, t, t_in, t_out, strike_at, stagger, reveal, exit)
        stg = M["word_stagger"] if stagger is None else stagger
        ink = c.theme(self.ink, "d_ink")
        acc = c.theme(self.accent, "d_accent")
        ws = self.words(c)
        # group punctuation with its word for staggering
        idx, k = [], -1
        for (w, kind, *_r) in ws:
            if not (kind == "plain" and re.fullmatch(r"[.,:;!?]+", w) and k >= 0):
                k += 1
            idx.append(k)
        for (w, kind, strike, x, base, pw), i in zip(ws, idx):
            a = out_expo(prog(t, t_in + i * stg, M["word_in"]))
            b = 0.0 if t_out is None else in_cubic(prog(t, t_out, M["out"]))
            vis = a * (1 - b)
            if vis <= 0.002:
                continue
            blur = M["word_blur"] * (1 - a) + M["out_blur"] * b
            dy = M["word_rise"] * (1 - a) - 14 * b
            f, s, ls = self._font(kind)
            col = acc if kind != "plain" else ink
            bbox = (x - 8, base - s, pw + 16, s * 1.35)
            with c.layer(bbox, vis, blur):
                c.text(x, base + dy, w, f, s, col, 1.0, ls)
        if strike_at is not None:
            self._strike(c, t, strike_at, t_out)

    def _groups(self, ws):
        idx, k = [], -1
        for (w, kind, *_r) in ws:
            if not (kind == "plain" and re.fullmatch(r"[.,:;!?]+", w) and k >= 0):
                k += 1
            idx.append(k)
        return idx

    def _lines(self, c):
        """[(baseline, x0, x1, [word tuples])] top → bottom."""
        out = {}
        for wd in self.words(c):
            out.setdefault(wd[4], []).append(wd)
        return [(b, min(w[3] for w in ws), max(w[3] + w[5] for w in ws), ws) for b, ws in sorted(out.items())]

    def _draw_apple(self, c, t, t_in, t_out, strike_at, stagger, reveal, exit):
        from .keynote import rise, wipe
        from .kinetic import dim_color, dim_alpha
        M = tk.M
        stg = (M["rise_line_stagger"] if reveal == "rise" else 0.14) if stagger is None else stagger
        ink = c.theme(self.ink, "d_ink")
        acc = c.theme(self.accent, "d_accent")
        b_dim = 0.0 if (t_out is None or exit != "dim") else prog(t, t_out, M["dim_out"])
        if b_dim >= 1:
            return
        quiet_out = t_out if exit != "dim" else None
        for i, (base, x0, x1, ws) in enumerate(self._lines(c)):
            def body(c, ws=ws):
                for (w, kind, strike, x, b_, pw) in ws:
                    f, s, ls = self._font(kind)
                    col = acc if kind != "plain" else ink
                    if b_dim > 0:
                        col = dim_color(c, col, b_dim)
                    c.text(x, b_, w, f, s, col, dim_alpha(b_dim) if b_dim > 0 else 1.0, ls)
            box = (x0 - 12, base - self.size, x1 - x0 + 24, self.size * 1.35)
            ti = t_in + i * stg
            if reveal == "rise":
                rise(c, t, ti, quiet_out, box, body, dy=self.size * 0.34)
            else:
                wipe(c, t, ti, box, body, t_out=quiet_out)
        if strike_at is not None:
            self._strike(c, t, strike_at, t_out)

    def _draw_kinetic(self, c, t, t_in, t_out, strike_at, stagger, reveal, exit):
        from .kinetic import mask_word, dim_color, dim_alpha
        M = tk.M
        stg = (M["word_stagger"] * 1.4) if stagger is None else stagger
        ink = c.theme(self.ink, "d_ink")
        acc = c.theme(self.accent, "d_accent")
        ws = self.words(c)
        for (w, kind, strike, x, base, pw), i in zip(ws, self._groups(ws)):
            f, s, ls = self._font(kind)
            col = acc if kind != "plain" else ink
            ti = t_in + i * stg
            if reveal == "ink":
                a0 = out_expo(prog(t, t_in, M["word_in"]))
                k = in_out_cubic(prog(t, t_in + 0.25 + i * M["ink_stagger"], M["ink_in"]))
                b = 0.0 if t_out is None else prog(t, t_out, M["quiet_out"] if exit == "quiet" else M["dim_out"])
                if a0 <= 0.002 or b >= 1:
                    continue
                col = mix(c.theme("faint", "d_line"), col, k)
                if exit == "quiet":
                    c.text(x, base + 6 * b, w, f, s, col, a0 * (1 - curve("apple_in")(b)), ls)
                    continue
                c.text(x, base, w, f, s, dim_color(c, col, b) if exit == "dim" else col, a0 * dim_alpha(b), ls)
                continue
            if reveal == "mask":
                mask_word(c, t, ti, t_out, x, base, w, f, s, col, ls, exit="mask" if exit == "mask" else "dim")
                continue
            # blur reveal with a kinetic exit
            a = out_expo(prog(t, ti, M["word_in"]))
            if a <= 0.002:
                continue
            b = 0.0 if t_out is None else prog(t, t_out, {"mask": M["out"], "quiet": M["quiet_out"]}.get(exit, M["dim_out"]))
            if b >= 1:
                continue
            dy = M["word_rise"] * (1 - a)
            if exit == "quiet":
                with c.layer((x - 8, base - s, pw + 16, s * 1.35), a * (1 - curve("apple_in")(b)), M["word_blur"] * (1 - a)):
                    c.text(x, base + dy + 6 * b, w, f, s, col, 1.0, ls)
                continue
            if exit == "mask":
                b = in_cubic(b)
                with c.clip(x - 10, base - s * 1.02, pw + 20, s * 1.30):
                    with c.layer((x - 8, base - s, pw + 16, s * 1.35), a, M["word_blur"] * (1 - a)):
                        c.text(x, base + dy - b * s * 1.05, w, f, s, col, 1.0, ls)
            else:
                with c.layer((x - 8, base - s, pw + 16, s * 1.35), a * dim_alpha(b), M["word_blur"] * (1 - a)):
                    c.text(x, base + dy, w, f, s, dim_color(c, col, b), 1.0, ls)
        if strike_at is not None:
            self._strike(c, t, strike_at, t_out)

    def _strike(self, c, t, t0, t_out):
        segs = {}
        for (w, kind, strike, x, base, pw) in self.words(c):
            if strike:
                s = segs.setdefault(base, [x, x + pw])
                s[1] = x + pw
        p = out_expo(prog(t, t0, 0.5))
        b = 0.0 if t_out is None else in_cubic(prog(t, t_out, tk.M["out"]))
        if p <= 0 or b >= 1:
            return
        for base, (x1, x2) in segs.items():
            y = base - self.size * 0.30
            c.line(x1 - 6, y, x1 - 6 + (x2 - x1 + 12) * p, y, c.theme("accent", "d_accent"),
                   self.size * 0.075, 1 - b)


def kicker(c, t, t_in, t_out, label, color, x=None, y=None):
    """'● 02 · NASKAH' — mono label with a chapter-colored dot."""
    x = tk.L["col_x"] if x is None else x
    y = tk.L["kicker_y"] if y is None else y
    a = out_expo(prog(t, t_in, 0.5))
    b = 0.0 if t_out is None else in_cubic(prog(t, t_out, tk.M["out"]))
    vis = a * (1 - b)
    if vis <= 0.002:
        return
    dx = -14 * (1 - a)
    size, ls, _ = tk.T["kicker"]
    with c.layer((x - 20, y - 30, 700, 50), vis, 6 * (1 - a) + 8 * b):
        c.circle(x + 5 + dx, y - 1, 5, color)
        c.text(x + 24 + dx, y + 8, label, tk.F["mono_med"], size, c.theme("ink2", "d_muted"), 1, ls)
