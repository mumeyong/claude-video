"""Reel motion (opt-in, 2026-10-10): the brand-reel layer — warm paper inside a viewfinder HUD, a dot logo that gathers
on an orbit, iris + pixel-block wipes, smear entrances, highlighter swipes, floating chips, count-up pills, a formula,
tilted card planes, hard-cut stat panels, verb slams on the six world colors, a logo end card.

Ported from the claude.ai Motion film "Six Worlds, One Walk" (mumeyong.dev brand reel ’26, 16:9, 31,4 s) and re-laid
for 1080×1920. For brand teasers / brand moments only (STYLE §1) — explainer videos keep STYLE §3.

    v.hud = False                                             # the reel brings its own HUD
    v.add(0, v.duration, lambda c, t: viewfinder(c, t, section(t), v.duration, dark=d(t)), z=90)
    dot_gather(c, t, t0, 540, 820, 150)                       # logo build (2,0 s), then orbit(...) around it
    iris(c, t, t1, 540, 820, GREEN, mode="open")              # green circle swells over everything
    with smear(c, p, dy=60, bbox=(x, y, w, h)): c.text(...)   # the reel's entrance (and exit via out=)
    float_chips(c, t, t0, [("Kubernetes", WORLDS[1], 90, 420, -1), ...], t_out=...)
    count_pill(c, t, t0, 540, 1100, 1200, 10000, label="CONCURRENT REQ", suffix="+")
    pixel_wipe(c, t, t0)                                      # ink blocks sweep the frame, leave paper
    reel_sfx(v, "chips", t0, n=8)                             # every move has a matching sound helper

Every function is frame = f(t): absolute times in, no state. Colors come from tokens (brand_paper, reel_ink,
reel_green, brand_seal, REEL_WORLDS).
"""
import math
import random
from contextlib import contextmanager

import cairo

from .. import tokens as tk
from ..ease import clamp, in_cubic, in_out_cubic, lerp, mix, out_cubic, pop
from .brand import _ENSO, mumei_mark
from .motion import fmt_id

PAPER, INK, GREEN, SEAL = tk.C["brand_paper"], tk.C["reel_ink"], tk.C["reel_green"], tk.C["brand_seal"]
WORLDS = tk.REEL_WORLDS
M, F = tk.M, tk.F
MUTED = mix(INK, PAPER, 0.38)             # 62% ink on paper — HUD, labels
FAINT = mix(INK, PAPER, 0.55)             # operators, kickers


def _seg(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= b)


def _eob(p, s=1.7):
    return pop(clamp(p), s) if p > 0 else 0.0


def _lum(col):
    return 0.2126 * col[0] + 0.7152 * col[1] + 0.0722 * col[2]


def ink_on(bg):
    """Paper or ink — whichever reads on the ground color bg."""
    return PAPER if _lum(bg) < 0.62 else INK


@contextmanager
def _xf(c, tx=0.0, ty=0.0, sx=1.0, sy=1.0, rot=0.0, origin=(0.0, 0.0), skew=0.0):
    cx = c.ctx
    cx.save()
    cx.translate(tx + origin[0], ty + origin[1])
    if rot:
        cx.rotate(rot)
    if skew:
        cx.transform(cairo.Matrix(1, 0, math.tan(skew), 1, 0, 0))
    if sx != 1.0 or sy != 1.0:
        cx.scale(sx, sy)
    cx.translate(-origin[0], -origin[1])
    try:
        yield c
    finally:
        cx.restore()


# ── the reel's entrance / exit ──────────────────────────────────────────
@contextmanager
def smear(c, p, bbox, dx=0.0, dy=0.0, out=0.0, blur=None, out_scale=0.3):
    """The reel's entrance: from offset (dx, dy) with a horizontal stretch (+25% when dx ≠ 0) and blur 16 → 0, opacity
    rising 1.6× faster than p. out 0..1 = the reel's exit: scale up out_scale (30%) around the bbox centre, blur 18,
    fade.
    bbox (x, y, w, h) = the element at rest. Draw the element at rest inside the block."""
    q = 1 - clamp(p)
    a = min(1.0, clamp(p) * 1.6) * (1 - out)
    bl = q * (M["reel_smear_blur"] if blur is None else blur) + out * M["reel_out_blur"]
    x, y, w, h = bbox
    o = (x + w / 2, y + h / 2)
    s = 1 + out * out_scale
    if p <= 0 or a <= 0.002:
        with c.group(0.0):
            yield c
        return
    with _xf(c, q * dx, q * dy, s * (1 + (q * 0.25 if dx else 0)), s, origin=o):
        with c.layer((x - 40, y - 40, w + 80, h + 80), a, bl):
            yield c


def smear_p(t, t0, dur=None):
    """Entrance progress for smear(): out_cubic over reel_smear_in (0 before t0)."""
    return out_cubic(_seg(t, t0, t0 + (dur or M["reel_smear_in"])))


def out_p(t, t_out, dur=None):
    """Exit progress for smear(out=…): in_cubic over reel_out from t_out (0 when t_out is None)."""
    return 0.0 if t_out is None else in_cubic(_seg(t, t_out, t_out + (dur or M["reel_out"])))


def smear_words(c, t, t0, x, base, text, font, size, color, ls=0.0, align="l", stagger=0.09, dy=70, t_out=None):
    """A line whose words smear up one by one (blur + rise 70 px, 0.09 s apart). Returns the line width."""
    words = text.split(" ")
    widths = [c.measure(w + (" " if i < len(words) - 1 else ""), font, size, ls)[0] for i, w in enumerate(words)]
    total = sum(widths)
    x0 = x if align == "l" else (x - total / 2 if align == "c" else x - total)
    o = out_p(t, t_out)
    for i, w in enumerate(words):
        with smear(c, smear_p(t, t0 + i * stagger), (x0, base - size, widths[i], size * 1.25), dy=dy, out=o):
            c.text(x0, base, w, font, size, color, ls=ls)
        x0 += widths[i]
    return total


# ── viewfinder HUD ──────────────────────────────────────────────────────
def viewfinder(c, t, section, total, dark=0.0, brand="mumeyong.dev", tag="brand reel", fmt="1080 × 1920 · 60 fps",
               alpha=1.0):
    """The reel's HUD (draw at z >= 90 with v.hud = False): four corner brackets, **brand** / tag top-left, running
    timecode top-right, section label + format bottom, a thin progress bar (t / total) along the bottom.
    dark 0..1 flips it to paper-on-color (over an iris, a pixel wipe, a verb slam)."""
    col = mix(MUTED, (*PAPER[:3], 0.62), clamp(dark))
    size, ls, _ = tk.T["hud"]
    W, H = tk.W, tk.H
    i, k, lw = 40, 28, 2.0
    cx = c.ctx
    c.src(col, alpha)
    cx.set_line_width(lw)
    for (x, y, sx, sy) in ((i, i, 1, 1), (W - i, i, -1, 1), (i, H - i, 1, -1), (W - i, H - i, -1, -1)):
        cx.move_to(x, y + sy * k)
        cx.line_to(x, y)
        cx.line_to(x + sx * k, y)
    cx.stroke()
    top, bot, xl, xr = 74, H - 92, 88, W - 88
    bw = c.text(xl, top, brand, F["mono_bold"], size, col, alpha, ls)
    c.text(xl + bw, top, "  /  " + tag, F["mono"], size, col, alpha, ls)
    T = max(0.0, t)
    s, f = int(T), int((T - int(T)) * tk.FPS)
    c.text(xr, top, "TC %02d:%02d:%02d:%02d" % (s // 3600, s // 60 % 60, s % 60, f), F["mono"], size, col, alpha,
           ls, align="r")
    c.text(xl, bot, section.upper(), F["mono"], size, col, alpha, ls)
    c.text(xr, bot, fmt.upper(), F["mono"], size, col, alpha, ls, align="r")
    by = H - 62
    c.fill_rrect(xl, by, xr - xl, 2, 0, col, alpha * 0.25)
    c.fill_rrect(xl, by, (xr - xl) * clamp(T / total), 2, 0, col, alpha)


# ── logo: dots gather → mark, orbit, iris ───────────────────────────────
_rg = random.Random(3)
_SRC = _ENSO[::max(1, len(_ENSO) // 150)][:150]
_GATHER = [(_rg.uniform(0, 2 * math.pi), _rg.random(), _rg.random(), _rg.random(), _rg.random()) for _ in _SRC]


def dot_gather(c, t, t0, cx, cy, r, ring=True, alpha=1.0):
    """Logo build from t0: ~150 dots drift on a wide flattened orbit, gather (staggered) onto the ensō's own stroke
    (0 → 1.35 s), the crisp mumei mark takes over (1.15 → 1.5 s), the seal stamps (1.5 → 1.85 s); a thin green ring
    swells from 1.5r to 3r behind it. ~22% of the dots wear the six world colors. r = ensō radius px."""
    u = t - t0
    if u < 0:
        return
    crisp = out_cubic(_seg(u, 1.15, 1.5))
    if ring:
        ra = out_cubic(_seg(u, 0.7, 1.1)) * alpha
        if ra > 0:
            c.ctx.new_path()
            c.ctx.arc(cx, cy, lerp(1.5 * r, 3 * r, out_cubic(_seg(u, 0.7, 2.3))), 0, 2 * math.pi)
            c.src(GREEN, 0.38 * ra)
            c.ctx.set_line_width(2.5)
            c.ctx.stroke()
    if crisp < 1:
        k = r / 100
        for (px, py, _, _), (a0, rf, d, sz, w) in zip(_SRC, _GATHER):
            p = in_out_cubic(_seg(u, d * 0.35, 1.25 + d * 0.2))
            a = a0 + u * 0.9 * (1 - p)
            rad = r * (1.7 + 2.6 * rf)
            x = cx + lerp(math.cos(a) * rad, px * r, p)
            y = cy + lerp(math.sin(a) * rad * 0.55, py * r, p)
            col = WORLDS[int(w * 100) % 6] if w < 0.22 else INK
            c.circle(x, y, (1.1 + sz * 1.7) * k * 1.6 * lerp(1, 0.75, p), col, (1 - crisp) * lerp(0.55, 0.95, p) * alpha)
    if crisp > 0:
        mumei_mark(c, cx, cy, r * (1 + math.sin(u * 2.4) * 0.008), p_enso=1.0, p_seal=_seg(u, 1.5, 1.85),
                   flecks=crisp, alpha=crisp * alpha, ink=INK)


def orbit(c, t, cx, cy, rx, ry, tilt=-0.22, alpha=1.0, n=70, speed=2.4, sats=None):
    """Dotted elliptical orbit (tilted) with satellites riding it — default: a green 7 px sat + a seal 4.5 px sat
    opposite. sats = [(color, radius, phase)]."""
    if alpha <= 0.002:
        return
    sats = sats if sats is not None else ((GREEN, 7.0, 0.0), (SEAL, 4.5, 3.1))
    with c.at(0, 0, 1.0, origin=(cx, cy), rot=tilt):
        for i in range(n):
            a = i / n * 2 * math.pi
            c.circle(cx + math.cos(a) * rx, cy + math.sin(a) * ry, 1.5, INK, 0.45 * alpha)
        for col, rr, ph in sats:
            b = t * speed + ph
            c.circle(cx + math.cos(b) * rx, cy + math.sin(b) * ry, rr, col, alpha)


def iris(c, t, t0, cx, cy, color=None, mode="open", dur=None):
    """Circle wipe from t0. mode="open": a disc of color swells from (cx, cy) over the whole frame (soft edge, eases
    in — the logo's exit). mode="close": a full-frame disc of color shrinks to the point, revealing what's under
    (the next scene's entrance). Draw at z >= 100. Returns progress 0..1."""
    color = color or GREEN
    p = _seg(t, t0, t0 + (dur or (0.85 if mode == "open" else M["reel_iris"])))
    far = max(math.hypot(x - cx, y - cy) for x in (0, tk.W) for y in (0, tk.H)) * 1.04
    cxx = c.ctx
    if mode == "open":
        if p <= 0:
            return p
        R = lerp(10, far / 0.82, in_cubic(p))
        g = cairo.RadialGradient(cx, cy, R * 0.82, cx, cy, R)
        g.add_color_stop_rgba(0, *color[:3], 1)
        g.add_color_stop_rgba(1, *color[:3], 0)
        cxx.set_source(g)
        cxx.new_path()
        cxx.arc(cx, cy, R, 0, 2 * math.pi)
        cxx.fill()
    elif p < 1:
        c.circle(cx, cy, lerp(far, 0, in_out_cubic(p)), color)
    return p


def pixel_wipe(c, t, t0, color=None, after=PAPER, block=None, diag=0.28):
    """Block wipe from t0: blocks flip to color along a diagonal front (left → right, bottom-up lean), hold
    reel_block_hold, then turn into `after` (None = vanish, revealing what's under). Draw at z >= 100.
    Returns the share of blocks currently showing color (0..1) — use it to flip the viewfinder dark."""
    color = color or INK
    B = block or M["reel_block"]
    sweep, hold = M["reel_block_sweep"], M["reel_block_hold"]
    if t < t0:
        return 0.0
    cols, rows = math.ceil(tk.W / B), math.ceil(tk.H / B)
    cx = c.ctx
    ink_cells, after_cells = [], []
    for x in range(cols):
        for y in range(rows):
            d = x / (cols - 1) * (1 - diag) + (rows - 1 - y) / (rows - 1) * diag
            ti = t0 + d * sweep
            if ti <= t < ti + hold:
                ink_cells.append((x, y))
            elif t >= ti + hold and after is not None:
                after_cells.append((x, y))
    for cells, col in ((ink_cells, color), (after_cells, after)):
        if cells:
            cx.new_path()
            for x, y in cells:
                cx.rectangle(x * B, y * B, B + 0.5, B + 0.5)
            c.src(col)
            cx.fill()
    return len(ink_cells) / (cols * rows)


# ── type accents ────────────────────────────────────────────────────────
def highlight(c, t, t0, x, y, w, h, color=None, dur=None, alpha=1.0):
    """Highlighter swipe behind text: a skewed (−8°) soft-green bar grows left → right from t0. Draw before the text."""
    p = in_out_cubic(_seg(t, t0, t0 + (dur or M["reel_hl"])))
    if p <= 0:
        return
    with _xf(c, 0, 0, p, 1.0, origin=(x, y + h / 2), skew=math.radians(-8)):
        c.fill_rrect(x, y, w, h, 6, color or mix(GREEN, PAPER, 0.62), alpha)


def highlight_phrase(c, t, t0, x, base, text, phrase, font, size, ls=0.0, align="l", color=None, dur=None):
    """highlight() under `phrase` inside a line of text drawn at (x, base) — measures it for you. Returns its bbox."""
    i = text.find(phrase)
    if i < 0:
        return None
    full = c.measure(text, font, size, ls)[0]
    x0 = x if align == "l" else (x - full / 2 if align == "c" else x - full)
    px = x0 + (c.measure(text[:i], font, size, ls)[0] if i else 0)
    pw = c.measure(phrase, font, size, ls)[0]
    box = (px - 10, base - size * 0.30, pw + 20, size * 0.40)
    highlight(c, t, t0, *box, color=color, dur=dur)
    return box


def type_clip(c, t, t0, x, base, text, font, size, color, ls=0.0, align="c", dur=None, alpha=1.0):
    """Wordmark reveal: the text is uncovered one character step at a time (a clip, no caret) from t0."""
    if t < t0:
        return
    n = round(len(text) * _seg(t, t0, t0 + (dur or M["reel_type"]))) / max(1, len(text))
    w, _, _ = c.measure(text, font, size, ls)
    x0 = x if align == "l" else (x - w / 2 if align == "c" else x - w)
    with c.clip(x0 - 10, base - size * 1.3, (w + 20) * n, size * 1.8):
        c.text(x0, base, text, font, size, color, alpha, ls)


# ── chips, pills ────────────────────────────────────────────────────────
def reel_chip(c, x, y, label, color, size=26, alpha=1.0):
    """Paper chip with a colored rounded square + label (top-left at x, y). Returns (w, h)."""
    sq = size + 2
    tw = c.measure(label, F["ui_semi"], size, -0.01)[0]
    h = sq + 28
    w = 16 + sq + 14 + tw + 24
    c.shadow(x, y, w, h, 16, 34, 14, 0.08 * alpha)
    c.fill_rrect(x, y, w, h, 16, PAPER, alpha)
    c.stroke_rrect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, 16, (*INK[:3], 0.12), 1.5, alpha)
    c.fill_rrect(x + 16, y + 14, sq, sq, 8, color, alpha)
    c.text(x + 16 + sq + 14, y + h / 2 + size * 0.36, label, F["ui_semi"], size, INK, alpha, -0.01)
    return w, h


def float_chips(c, t, t0, chips, t_out=None, stagger=None, size=26):
    """Chips fly in from their side (−1 left / +1 right) with the smear, one every reel_chip_stagger, then idle-float
    (±6 px) at a ±2,5° tilt; at t_out they push back out to their side, blurring. chips = [(label, color, x, y, side)]:
    x is the chip's LEFT edge for side −1 and its RIGHT edge for side +1 (so both rows hug the safe column)."""
    st = stagger or M["reel_chip_stagger"]
    o = out_p(t, t_out)
    for i, (label, color, x, y, side) in enumerate(chips):
        ti = t0 + i * st
        if t < ti:
            continue
        p = out_cubic(_seg(t, ti, ti + 0.42))
        w = c.measure(label, F["ui_semi"], size, -0.01)[0] + size + 56
        h = size + 30
        if side > 0:
            x -= w
        dx = math.sin(t * 0.9 + i) * 6 + side * o * 260
        dy = math.cos(t * 0.7 + i * 2) * 5
        with _xf(c, dx, dy, rot=math.radians(2.5 if i % 2 else -2.5), origin=(x + w / 2, y + h / 2)):
            with smear(c, p, (x, y, w, h), dx=side * 320, out=o, out_scale=0.0):
                reel_chip(c, x, y, label, color, size)


def pill(c, cx, y, text, size=36, label=None, scale=1.0, alpha=1.0, width_of=None):
    """Dark pill centred on cx (top at y): a soft-green dot, optional small tracked label, mono-bold text.
    width_of = a longer string to size the pill by (keeps it steady while a number counts). Returns (w, h)."""
    lab = size * 0.55
    lw = c.measure(label, F["mono_med"], lab, 0.14)[0] + 16 if label else 0
    tw = c.measure(width_of or text, F["mono_bold"], size, 0)[0]
    h = size + 30
    w = 30 + 12 + 16 + lw + tw + 30
    if scale <= 0.001 or alpha <= 0.002:
        return w, h
    with c.at(0, 0, scale, origin=(cx, y + h / 2)):
        x = cx - w / 2
        c.fill_rrect(x, y, w, h, h / 2, INK, alpha)
        c.circle(x + 36, y + h / 2, 6, mix(GREEN, PAPER, 0.3), alpha)
        xx = x + 58
        if label:
            c.text(xx, y + h / 2 + lab * 0.36, label, F["mono_med"], lab, PAPER, 0.6 * alpha, 0.14)
            xx += lw
        c.text(xx, y + h / 2 + size * 0.36, text, F["mono_bold"], size, PAPER, alpha)
    return w, h


def count_pill(c, t, t0, cx, y, v0, v1, label=None, fmt=None, suffix="", dur=None, t_out=None, size=36):
    """Dark pill that pops at t0 (pop 1.7) with a number counting v0 → v1 (Indonesian format by default);
    suffix ('+') lands when the count finishes. Returns the value shown."""
    if t < t0:
        return v0
    fmt = fmt or (lambda v: fmt_id(v))
    d = dur or M["reel_count"]
    v = lerp(v0, v1, out_cubic(_seg(t, t0 + 0.05, t0 + 0.05 + d)))
    done = t >= t0 + 0.05 + d
    pill(c, cx, y, fmt(v) + (suffix if done else ""), size, label, max(0.0, _eob(_seg(t, t0, t0 + 0.4))),
         1 - out_p(t, t_out), width_of=fmt(v1) + suffix)
    return v


# ── formula, cards, tilted plane ────────────────────────────────────────
def _paper_card(c, x, y, w, h, r=20, alpha=1.0, active=0.0, dark=False):
    c.shadow(x, y, w, h, r, 60, 22, 0.10 * alpha)
    c.fill_rrect(x, y, w, h, r, INK if dark else PAPER, alpha)
    if not dark:
        c.stroke_rrect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, r, mix((*INK[:3], 0.13), (*GREEN[:3], 1), active), 1.5,
                       alpha)
    if active > 0:
        c.stroke_rrect(x - 4, y - 4, w + 8, h + 8, r + 4, GREEN, 4, 0.25 * active * alpha)


def formula(c, t, t0, boxes, cards, target, op="+", t_out=None):
    """'A + B + C = result' from t0: cards pop up one by one (0.22 s apart), operators fade in between consecutive
    boxes, each card lights green in turn (from 1.15 s), dotted lines converge from each card's bottom-centre to
    target (x, y) (1.25 → 2.15 s). Pop the result yourself at t0 + 2.0 (count_pill). boxes = [(x, y, w, h)],
    cards = [(kicker, title, sub)]. Returns the time the result should land."""
    o = out_p(t, t_out)
    for i, ((x, y, w, h), (kick, title, sub)) in enumerate(zip(boxes, cards)):
        ti = t0 + i * 0.22
        if t < ti:
            continue
        p = _eob(_seg(t, ti, ti + 0.45), 1.6)
        act = 1.0 if t0 + 1.15 + i * 0.32 < t < t0 + 1.55 + i * 0.32 else 0.0
        ts = min(64, h * 0.3)
        with _xf(c, 0, lerp(60, 0, min(1, p)), 0.9 + 0.1 * p, 0.9 + 0.1 * p, origin=(x + w / 2, y + h / 2)):
            with c.group(1 - o):
                _paper_card(c, x, y, w, h, active=act)
                c.text(x + 30, y + 30 + 19, kick.upper(), F["mono"], 19, MUTED, 1, 0.16)
                c.text(x + 30, y + 30 + 19 + 18 + ts * 0.8, title, F["display"], ts, INK, 1, -0.04)
                c.text(x + 30, y + h - 30, sub, F["ui_reg"], 26, MUTED, 1)
        if i and op:
            (px, py, pw, ph) = boxes[i - 1]
            mx, my = (px + pw / 2 + x + w / 2) / 2, (py + ph / 2 + y + h / 2) / 2
            c.text(mx, my + 22, op, F["display_semi"], 64, FAINT, out_cubic(_seg(t, t0 + 0.25 + i * 0.22,
                                                                                   t0 + 0.55 + i * 0.22)) * (1 - o),
                   align="c")
    ln = in_out_cubic(_seg(t, t0 + 1.25, t0 + 2.15))
    if ln > 0:
        tx, ty = target
        for (x, y, w, h) in boxes:
            sx, sy = x + w / 2, y + h
            for k in range(int(30 * ln) + 1):
                uu = k / 30
                s3 = uu * uu * (3 - 2 * uu)
                c.circle(lerp(sx, tx, s3), lerp(sy + 8, ty - 8, uu), 2.2, GREEN, 0.7 * (1 - o))
    return t0 + 2.0


def pop_card(c, t, t0, x, y, w, h, draw=None, image=None, label=None, color=None, r=None, alpha=1.0):
    """A card that pops in at t0 (from −40, +80 px, scale .86 → 1, pop 1.5): paper card, optional image (cover),
    custom draw(c, x, y, w, h), and a chip label bottom-left."""
    if t < t0:
        return
    p = _eob(_seg(t, t0, t0 + 0.5), 1.5)
    r = r if r is not None else (22 if w > 400 else 16)
    a = min(1.0, _seg(t, t0, t0 + 0.15)) * alpha
    s = 0.86 + 0.14 * p
    with _xf(c, lerp(-40, 0, min(1, p)), lerp(80, 0, min(1, p)), s, s, origin=(x + w / 2, y + h / 2)):
        with c.group(a):
            _paper_card(c, x, y, w, h, r)
            if image:
                c.image(image, x, y, w, h, r)
            if draw:
                draw(c, x, y, w, h)
            if label:
                sz = 22 if w > 400 else 18
                reel_chip(c, x + 14, y + h - 14 - (sz + 30), label, color or INK, sz)


def tilt_plane(c, t, t0, t1, box, draw, rx=(34, 26), rz=(-16, -10), t_out=None):
    """Fake-perspective plane over [t0, t1]: content drawn by draw(c, t) in plane coords inside box (x, y, w, h) is
    laid back (rotateX, as a vertical squash) and turned (rotateZ), easing from the first to the second angle while
    it pushes in slowly (+1,2%/s). At t_out: blur + drain + fade."""
    k = in_out_cubic(_seg(t, t0, t1))
    ax, az = math.radians(lerp(*rx, k)), math.radians(lerp(*rz, k))
    o = out_p(t, t_out, 0.5)
    s = 0.98 + (t - t0) * 0.012 + o * 0.08
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    m = c.ctx
    m.save()
    m.translate(cx, cy)
    m.scale(1, math.cos(ax))
    m.rotate(az)
    m.scale(s, s)
    m.translate(-cx, -cy)
    try:
        with c.layer((x - 120, y - 120, w + 240, h + 240), 1 - o, o * 12):
            draw(c, t)
    finally:
        m.restore()


# ── stats, verbs, end card ──────────────────────────────────────────────
def _fit(c, text, font, size, maxw, ls=-0.045):
    w = c.measure(text, font, size, ls)[0]
    return size if w <= maxw else size * maxw / w


def stat_panel(c, t, t0, dur, v0, v1, label, fmt=None, bg=None, num=None, box=None, size=280, t_out=None):
    """Hard-cut stat panel, visible [t0, t0 + dur): a giant number counts v0 → v1 in 0.6 s (blur-rising in), a
    tracked label fades in under it; a colored panel (bg) pops .92 → 1. fmt(v) → str (default fmt_id)."""
    if not (t0 <= t < t0 + dur):
        return
    u = t - t0
    fmt = fmt or (lambda v: fmt_id(v))
    x, y, w, h = box or (tk.L["col_x"], 330, tk.L["col_w"], 1180)
    ink = ink_on(bg) if bg else INK
    num = num or (mix(GREEN, PAPER, 0.3) if bg and _lum(bg) < 0.3 else ink)
    a = 1 - out_p(t, t_out, 0.3)
    s = lerp(0.92, 1, min(1.05, _eob(_seg(u, 0, 0.35), 1.4))) if bg else 1.0
    with c.at(0, 0, s, origin=(x + w / 2, y + h / 2)):
        with c.group(a):
            if bg:
                c.fill_rrect(x, y, w, h, 28, bg)
            txt = fmt(lerp(v0, v1, out_cubic(_seg(u, 0, 0.6))))
            sz = _fit(c, fmt(v1), F["display"], size, w - 120)
            base = y + h / 2 + sz * 0.3
            ns = 1 + u * 0.02
            with c.at(0, 0, ns, origin=(x + w / 2, base - sz * 0.35)):
                with smear(c, out_cubic(_seg(u, 0, 0.3)), (x, base - sz, w, sz * 1.2), dy=40):
                    c.text(x + w / 2, base, txt, F["display"], sz, num, 1, -0.045, align="c")
            c.text(x + w / 2, base + 90, label.upper(), F["mono_med"], 24, ink, 0.7 * out_cubic(_seg(u, 0.2, 0.5)),
                   0.16, align="c")


def verb_slam(c, t, t0, words, colors=None, each=None, cx=None, base=1010, size=260, maxw=780, tile=True, dot=True):
    """Verb slams from t0, one word every `each` s (default 0.43): the ground hard-cuts to the word's color, the word
    whips in from alternating sides (520 px, 0.2 s smear), keeps pushing (+8%/s), and a seal dot lands after it.
    The last word also gets a tiled background of itself scrolling in alternating rows. Returns the ink in use
    (PAPER = dark ground → flip the viewfinder)."""
    each = each or 0.43
    colors = colors or WORLDS
    cx = tk.W / 2 if cx is None else cx
    u0 = t - t0
    if u0 < 0:
        return INK
    k = min(len(words) - 1, int(u0 / each))
    u = u0 - k * each
    bg = colors[k % len(colors)]
    ink = ink_on(bg)
    c.fill_rrect(0, 0, tk.W, tk.H, 0, bg)
    word = words[k]
    if tile and k == len(words) - 1:
        ta = out_cubic(_seg(u, 0, 0.2))
        row = (" ".join([word] * 4))
        for r in range(13):
            off = (1 if r % 2 else -1) * (u0 * 260) - 400
            c.text(off, 40 + r * 150 + 120, row, F["display"], 150, ink, 0.16 * ta, -0.045)
    sz = _fit(c, word, F["display"], size, maxw, -0.05)
    w = c.measure(word, F["display"], sz, -0.05)[0]
    p = out_cubic(_seg(u, 0, M["reel_slam"]))
    side = -1 if k % 2 else 1
    sc = 1 + u * 0.08
    with c.at(0, 0, sc, origin=(cx, base - sz * 0.35)):
        with smear(c, p, (cx - w / 2, base - sz, w, sz * 1.2), dx=side * 520):
            c.text(cx, base, word, F["display"], sz, ink, 1, -0.05, align="c")
        if dot and p > 0.85:
            c.circle(cx + w / 2 + 40, base - sz * 0.13, 28 * sz / 280, SEAL, out_cubic(_seg(u, 0.12, 0.2)))
    return ink


def end_card(c, t, t0, cx=None, cy=820, r=130, name="mumeyong.dev", sub=None, cta=None, lift=180):
    """Logo end card from t0: 8 dots spiral in → the mumei mark grows (pop) inside a swelling green ring → seal
    stamps (0.95 s) → mark lifts by `lift` px and shrinks 15% → dotted orbit + the six world dots on an arc →
    wordmark clip-types in (1.35 s) → serif sub smears up (1.95 s) → dark CTA pill pops (2.3 s). Needs ~3.2 s."""
    u = t - t0
    if u < 0:
        return
    cx = tk.W / 2 if cx is None else cx
    lf = in_out_cubic(_seg(u, 1.05, 1.55))
    y = cy - lift * lf
    conv = in_out_cubic(_seg(u, 0, 0.6))
    if conv < 1:
        for i in range(8):
            a = i / 8 * 2 * math.pi + u * 1.6
            rr = lerp(2 * r, 0, conv)
            c.circle(cx + math.cos(a) * rr, y + math.sin(a) * rr, 9, GREEN if i % 4 == 0 else INK, 1 - conv * 0.6)
    grow = _eob(_seg(u, 0.5, 1.0), 1.6)
    ring = out_cubic(_seg(u, 0.45, 0.8))
    if ring > 0:
        c.ctx.new_path()
        c.ctx.arc(cx, y, lerp(0.45 * r, 1.15 * r, out_cubic(_seg(u, 0.45, 1.2))), 0, 2 * math.pi)
        c.src(GREEN, 0.6 * ring * (1 - lf * 0.6))
        c.ctx.set_line_width(3)
        c.ctx.stroke()
    if grow > 0:
        rr = 0.62 * r * grow * lerp(1, 0.85, lf) * (1 + u * 0.006)
        mumei_mark(c, cx, y, rr, p_seal=_seg(u, 0.95, 1.25), flecks=1.0, ink=INK)
    ob = out_cubic(_seg(u, 1.2, 1.6))
    if ob > 0:
        orbit(c, u, cx, y, 1.27 * r, 0.34 * r, -0.25, ob, n=64, speed=2.2, sats=((GREEN, 6.5, 0.0),))
        for i in range(6):
            a = -2.4 + i * 0.32
            c.circle(cx + math.cos(a) * 1.77 * r, y + math.sin(a) * 0.92 * r, 5, WORLDS[i],
                     out_cubic(_seg(u, 1.5 + i * 0.06, 1.8 + i * 0.06)))
    nb = cy + 2.1 * r - lift + 40
    nsz = _fit(c, name, F["display"], 120, tk.L["col_w"])
    type_clip(c, t, t0 + 1.35, cx, nb, name, F["display"], nsz, INK, -0.045)
    if sub:
        with smear(c, smear_p(t, t0 + 1.95, 0.4), (cx - 420, nb + 30, 840, 70), dy=30):
            c.text(cx - tk.L["col_w"] / 2, nb + 84, sub, F["serif"], 46 * tk.SERIF_SCALE, mix(INK, PAPER, 0.3),
                   align="c", width=tk.L["col_w"])
    if cta:
        pill(c, cx, nb + (170 if sub else 70), cta, 28, scale=max(0.0, _eob(_seg(u, 2.3, 2.65), 1.6)),
             alpha=float(u >= 2.3))


# ── sound ───────────────────────────────────────────────────────────────
def reel_sfx(v, move, t0, n=1, each=None):
    """Register the sounds that belong to a reel move started at t0:
    gather · iris · smear · chips (n) · count · wipe · highlight · formula (n cards) · cards (n) · stats (n panels,
    each s) · verbs (n words, each s) · end."""
    s = v.sfx
    if move == "gather":
        s("chime", t0 + 1.15, 0.5); s("pop", t0 + 1.5, 0.9)
    elif move == "iris":
        s("whoosh", t0, 0.8)
    elif move == "smear":
        s("whoosh", t0, 0.5)
    elif move == "chips":
        for i in range(n):
            s("pop", t0 + i * (each or M["reel_chip_stagger"]), 0.45 + 0.04 * i)
    elif move == "count":
        for k in range(int((each or M["reel_count"]) / 0.12)):
            s("tick", t0 + 0.05 + k * 0.12, 0.35)
    elif move == "wipe":
        s("whoosh", t0 + 0.1, 0.6)
    elif move == "highlight":
        s("click", t0, 0.5)
    elif move == "formula":
        for i in range(n):
            s("pop", t0 + i * 0.22, 0.7)
        s("chime", t0 + 2.0, 0.8)
    elif move == "cards":
        for i in range(n):
            s("pop", t0 + i * (each or M["reel_card_stagger"]), 0.5 + 0.05 * i)
    elif move == "stats":
        for i in range(n):
            s("thud", t0 + i * (each or 1.1), 0.9)
    elif move == "verbs":
        for i in range(n):
            s("thud", t0 + i * (each or 0.43), 1.0); s("whoosh", t0 + i * (each or 0.43), 0.4)
    elif move == "end":
        s("thud", t0, 0.9); s("pop", t0 + 0.95, 0.8); s("chime", t0 + 1.35, 0.8); s("pop", t0 + 2.3, 0.6)
    else:
        raise ValueError(f"reel_sfx: unknown move {move!r}")
