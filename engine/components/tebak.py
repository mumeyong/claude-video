"""Predictive-keyboard components (first used in "ai-ngarang-jawaban").

keyboard_hp · suggest_bar · token_line
Metaphor: the phone keyboard that guesses your next word — an LLM is the giant version of it. Signature: the top
word in the suggestion bar jumps into the sentence (its probability bar full, the others deflate), token by token.
Pure functions of their progress values (frame = f(t)); colors from tokens.
"""
from .. import tokens as tk
from ..ease import clamp, lerp, mix, out_cubic, pop

PURPLE = tk.CHAPTER[3][0]           # signature: picked slot, probability bars, token pills
F, C = tk.F, tk.C
ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")
KB_RATIO = 0.56                     # keyboard height / width


def _theme(dark):
    if dark:
        return dict(base=C["d_card"], key=mix(C["d_card"], C["d_ink"], 0.12), ink=C["d_ink"], muted=C["d_muted"],
                    line=C["d_line"], ground=C["d_bg"])
    return dict(base=mix(C["bg"], C["faint"], 0.35), key=C["card"], ink=C["ink"], muted=C["muted"], line=C["line"],
                ground=C["card"])


def keyboard_hp(c, x, y, w, press=None, press_p=0.0, keys=1.0, dark=False, alpha=1.0):
    """Phone keyboard (top-left x, y; width w, height KB_RATIO·w): three letter rows + shift/backspace + 123 / spasi / enter.
    press = letter whose key pops up a preview (press_p 0..1). keys 0..1 fades the keys in row by row.
    Returns its height."""
    h = w * KB_RATIO
    if alpha <= 0.002:
        return h
    th = _theme(dark)
    c.fill_rrect(x, y, w, h, 28, th["base"], alpha)
    pad, gap = w * 0.018, w * 0.012
    kw = (w - 2 * pad - 9 * gap) / 10
    kh = (h - 2 * pad - 3 * gap) / 4
    size = kh * 0.42
    for r in range(4):
        a = alpha * clamp(keys * 4 - r)
        if a <= 0.002:
            continue
        ky = y + pad + r * (kh + gap)
        if r < 3:
            row = ROWS[r]
            rw = len(row) * kw + (len(row) - 1) * gap
            kx = x + (w - rw) / 2
            if r == 2:                                       # shift + backspace around the last row
                sw = (w - 2 * pad - rw - 2 * gap) / 2
                for sx, glyph in ((x + pad, "↑"), (x + w - pad - sw, "←")):
                    c.fill_rrect(sx, ky, sw, kh, 10, th["key"], a * 0.7)
                    c.text(sx + sw / 2, ky + kh * 0.66, glyph, F["ui"], size, th["muted"], a, align="c")
            for ch in row:
                c.fill_rrect(kx, ky + 2, kw, kh, 10, (0, 0, 0, 1), a * 0.08)
                c.fill_rrect(kx, ky, kw, kh, 10, th["key"], a)
                c.text(kx + kw / 2, ky + kh * 0.66, ch, F["ui_reg"], size, th["ink"], a, align="c")
                if press == ch and press_p > 0:
                    p = pop(clamp(press_p), 1.6)
                    pw, ph = kw * 1.5, kh * 1.7
                    with c.at(0, 0, max(0.01, p), origin=(kx + kw / 2, ky)):
                        c.shadow(kx + kw / 2 - pw / 2, ky - ph, pw, ph, 14, 18, 6, 0.08 * a)
                        c.fill_rrect(kx + kw / 2 - pw / 2, ky - ph, pw, ph, 14, th["key"], a)
                        c.text(kx + kw / 2, ky - ph * 0.3, ch, F["ui_reg"], size * 1.6, th["ink"], a, align="c")
                kx += kw + gap
        else:                                                # 123 · spasi · enter
            bw = kw * 1.6
            sp = w - 2 * pad - 2 * bw - 2 * gap
            for bx, bwid, label in ((x + pad, bw, "123"), (x + pad + bw + gap, sp, "spasi"),
                                    (x + w - pad - bw, bw, "→")):
                c.fill_rrect(bx, ky, bwid, kh, 10, th["key"], a * (1.0 if label == "spasi" else 0.7))
                c.text(bx + bwid / 2, ky + kh * 0.64, label, F["ui"], size * 0.8, th["muted"], a, align="c")
    return h


def suggest_bar(c, x, y, w, words, probs=None, bars=1.0, pick=None, pick_p=0.0, missing=None, missing_p=0.0,
                color=None, dark=False, h=96, size=34, alpha=1.0, word_a=None):
    """Suggestion strip (x, y, w, h) with one slot per word, hairlines between them. probs (0..1 each) draw a
    probability bar under every word, grown by `bars`. pick = slot index that lights up in the signature color
    (pick_p 0..1). missing = label of an extra dashed slot on the right that doesn't exist (missing_p fades it in);
    pass the label in words instead to make it a real slot. word_a = per-slot alphas (a word that just left).
    Returns the slot centres [(cx, cy)] (the dashed slot last)."""
    color = color or PURPLE
    th = _theme(dark)
    n = len(words)
    mw = w * 0.27 if missing else 0.0
    sw = (w - mw - (12 if missing else 0)) / max(1, n)
    centres = [(x + sw * (i + 0.5), y + h * 0.5) for i in range(n)]
    if alpha <= 0.002:
        return centres + ([(x + w - mw / 2, y + h / 2)] if missing else [])
    c.fill_rrect(x, y, w - mw - (12 if missing else 0), h, 22, th["ground"], alpha)
    c.stroke_rrect(x, y, w - mw - (12 if missing else 0), h, 22, th["line"], 1.5, alpha)
    for i, word in enumerate(words):
        sx = x + sw * i
        if i:
            c.line(sx, y + h * 0.24, sx, y + h * 0.76, th["line"], 2, alpha)
        hot = pick_p if pick == i else 0.0
        if hot > 0:
            c.fill_rrect(sx + 8, y + 8, sw - 16, h - 16, 16, color, alpha * 0.14 * clamp(hot))
        wa = alpha * (1.0 if word_a is None else word_a[i])
        cy = y + h * (0.58 if probs is None else 0.5)
        c.text(sx + sw / 2, cy, word, F["ui_semi"] if hot > 0.5 else F["ui"], size, mix(th["ink"], color, hot), wa,
               -0.01, align="c")
        if probs is not None:
            bw = (sw - 56) * clamp(probs[i]) * clamp(bars)
            by = y + h - 24
            c.fill_rrect(sx + 28, by, sw - 56, 8, 4, th["line"], alpha)
            if bw > 1:
                c.fill_rrect(sx + 28, by, bw, 8, 4, mix(th["muted"], color, 0.4 + 0.6 * hot), wa)
    if missing and missing_p > 0:
        a = alpha * clamp(missing_p)
        mx = x + w - mw
        c.stroke_rrect(mx, y, mw, h, 22, th["muted"], 2.5, a, dash=[10, 8])
        c.text(mx + mw / 2, y + h * 0.6, missing, F["ui"], size * 0.9, th["muted"], a, -0.01, align="c")
        centres.append((mx + mw / 2, y + h / 2))
    return centres


def token_line(c, x, base, tokens, n, width, size=48, color=None, ink=None, pills=0.0, src=None, line_h=None,
               font=None, alpha=1.0, tint=None):
    """Text built from tokens (strings; a leading space = word start), wrapped at `width`. n (float) = how many are
    in: the token at floor(n) is on its way — it flies from src (x, y) to its place (scale .7 → 1) when src is
    given, else fades in. pills 0..1 tints every token's box (alternating) so the cut into tokens shows
    (tint = the two pill colors (a, b); default purple / purple-blue).
    Returns the caret (x, baseline) after the last arrived token."""
    color = color or PURPLE
    ink = ink or C["ink"]
    font = font or F["ui"]
    lh = line_h or size * 1.32
    cx, cy = x, base
    k = int(n)
    f = n - k
    caret = (x, base)
    for i, tok in enumerate(tokens):
        if i > k or (i == k and f <= 0):
            break
        tw = c.measure(tok, font, size, -0.01)[0]
        lead = c.measure(" ", font, size)[0] if tok.startswith(" ") else 0.0
        if cx + tw > x + width and cx > x:
            cx, cy = x, cy + lh
            tok, tw, lead = tok.lstrip(" "), c.measure(tok.lstrip(" "), font, size, -0.01)[0], 0.0
        p = 1.0 if i < k else out_cubic(clamp(f))
        a = alpha * (1.0 if (i < k or src is not None) else p)
        tx, ty, s = cx, cy, 1.0
        if i == k and src is not None:
            tx, ty, s = lerp(src[0] - tw / 2, cx, p), lerp(src[1] + size * 0.35, cy, p), lerp(0.7, 1.0, p)
        with c.at(0, 0, s, origin=(tx + tw / 2, ty - size * 0.35)):
            if pills > 0:
                ta, tb = tint or (PURPLE, mix(PURPLE, C["accent"], 0.5))
                c.fill_rrect(tx + lead - 4, ty - size * 0.86, tw - lead + 8, size * 1.12, 10, ta if i % 2 == 0 else tb,
                             a * 0.13 * pills)
            c.text(tx, ty, tok, font, size, mix(ink, color, (1 - p) if i == k else 0.0), a, -0.01)
        cx += tw
        if i < k or p >= 1:
            caret = (cx, cy)
    return caret
