"""Classroom-whiteboard components (first used in "ai-lupa-obrolan-panjang").

papan_tulis · papan_geo · penghapus · memori
Metaphor: a chat with an AI is a whiteboard. Every message is one handwritten row; with every new message the whole
board is read again from the first row (stateless); the board's size is the context window; when it is full the top
row gets erased first — and that is where your name was.
Signature: an orange reading band sweeps the board top → bottom; the eraser lifts off the tray and wipes the top row.
Pure functions of their progress values (frame = f(t)). Colors from tokens; shading via material (flat | paper | lit).
"""
import math

from .. import tokens as tk
from ..ease import clamp, lerp
from . import material as mat

ORANGE = tk.CHAPTER[2][0]            # signature: AI ink, reading band, eraser handle, lit memory cells
INK = tk.C["brand_ink"]              # the black marker (your rows)
F = tk.F


def papan_geo(x, y, w, h, slots=8, scroll=0.0):
    """Geometry of papan_tulis drawn with the same x, y, w, h (no drawing): f, surface box, rows box, row_h,
    text_x, base(i) = baseline y of row slot i (after scroll), band(i) = (y, h) of slot i, tray box, eraser rest
    (cx, cy) of the eraser lying on the tray, font size."""
    f = w / 848
    rim = 18 * f
    sx, sy, sw, sh = x + rim, y + rim, w - 2 * rim, h - 2 * rim
    top, bot = sy + 22 * f, sy + sh - 22 * f
    row_h = (bot - top) / slots
    size = clamp(row_h * 0.58, 22, 50 * f)
    gut = 96 * f
    tray = (x + w * 0.08, y + h - 4 * f, w * 0.84, 30 * f)
    return dict(
        f=f, rim=rim, surface=(sx, sy, sw, sh), rows=(sx, top, sw, bot - top), row_h=row_h, size=size,
        gut_x=sx + 30 * f, text_x=sx + 30 * f + gut, text_w=sw - 60 * f - gut,
        base=lambda i: top + (i - scroll) * row_h + row_h * 0.68,
        band=lambda i: (top + (i - scroll) * row_h, row_h),
        tray=tray, rest=(x + w * 0.74, y + h - 4 * f - 22 * f))


def _segments(text):
    """'Bantu |rencan|ain' → ('Bantu rencanain', [char offsets of the token boundaries])."""
    parts = text.split("|")
    cuts, n = [], 0
    for p in parts[:-1]:
        n += len(p)
        cuts.append(n)
    return "".join(parts), cuts


def papan_tulis(c, x, y, w, h, rows=(), scroll=0.0, slots=8, scan=None, scan_a=1.0, tok=0.0, ghost=0.07,
                eraser=1.0, look="paper", color=None, alpha=1.0, font=None):
    """Whiteboard on the wall, top-left (x, y), size w × h (+ a marker tray under it).
    rows: dicts {text, who ('kamu' | 'ai'), slot (row index before scroll), write 0..1 (handwritten left → right),
    gone 0..1 (wiped left → right by the eraser), a (alpha)}. Text may contain '|' token cuts — tok 0..1 shows them
    as small ticks. scroll: rows moved up by this many slots (clipped at the top edge). scan: reading band position
    (slot units, None = off). eraser: alpha of the eraser resting on the tray (0 while it is in someone's hand).
    font: row typeface (default the handwritten serif; F["ui"] = clean Apple-style rows)."""
    if alpha <= 0.002:
        return
    col = ORANGE if color is None else color
    font = font or F["serif"]
    g = papan_geo(x, y, w, h, slots, scroll)
    f = g["f"]
    with c.group(alpha):
        # frame + surface
        mat.body(c, look, mat.rrect_path(x, y, w, h, 14 * f), (x, y, w, h), tk.C["faint"], r=14 * f)
        sx, sy, sw, sh = g["surface"]
        mat.body(c, look, mat.rrect_path(sx, sy, sw, sh, 6 * f), g["surface"], tk.C["card"], shadow=False)
        mat.inset(c, look, mat.rrect_path(sx, sy, sw, sh, 6 * f), g["surface"], 0.6)
        # tray + markers + eraser at rest
        tx, ty, tw, th = g["tray"]
        mat.body(c, look, mat.rrect_path(tx, ty, tw, th, 8 * f), g["tray"], tk.C["muted"], r=8 * f, lift=0.6)
        for i, mc in enumerate((INK, col)):
            mx = tx + 60 * f + i * 150 * f
            mat.body(c, look, mat.rrect_path(mx, ty - 16 * f, 120 * f, 18 * f, 9 * f),
                     (mx, ty - 16 * f, 120 * f, 18 * f), tk.C["card"], r=9 * f, lift=0.3)
            c.fill_rrect(mx + 92 * f, ty - 16 * f, 28 * f, 18 * f, 9 * f, mc)
        if eraser > 0.002:
            penghapus(c, g["rest"][0], g["rest"][1], f, look=look, color=col, alpha=eraser)

        rx, ry, rw, rh = g["rows"]
        size = g["size"]
        widest = max([c.measure(_segments(r["text"])[0], font, size)[0] for r in rows] or [0.0])
        if widest > g["text_w"]:                 # a wider face (Inter) shrinks to fit the board, same for every row
            size *= g["text_w"] / widest
        with c.clip(sx, ry - 4 * f, sw, rh + 8 * f):
            # reading band (behind the ink)
            if scan is not None and scan_a > 0.002:
                by, bh = g["band"](scan)
                c.fill_rrect(sx + 12 * f, by + 4 * f, sw - 24 * f, bh - 8 * f, 10 * f, col, 0.13 * scan_a)
                c.fill_rrect(sx + 12 * f, by + 4 * f, 7 * f, bh - 8 * f, 3 * f, col, 0.9 * scan_a)
            for r in rows:
                a = r.get("a", 1.0)
                wr, gone = clamp(r.get("write", 1.0)), clamp(r.get("gone", 0.0))
                if a <= 0.002 or wr <= 0.0:
                    continue
                b = g["base"](r["slot"])
                if b < ry - g["row_h"] or b > ry + rh + g["row_h"]:
                    continue
                ink = INK if r["who"] == "kamu" else col
                c.text(g["gut_x"], b - size * 0.12, "KAMU" if r["who"] == "kamu" else "AI", F["mono_med"],
                       max(17, 17 * f), tk.C["muted"], a * (1 - gone), ls=0.12)
                text, cuts = _segments(r["text"])
                tw_ = c.measure(text, font, size)[0]
                x0 = g["text_x"]
                x1 = x0 + tw_ * wr
                xg = x0 + (tw_ + 12 * f) * gone
                if gone > 0 and ghost > 0:       # whiteboard ghosting where the eraser passed
                    with c.clip(x0 - 6 * f, b - size, max(0.0, xg - x0 + 6 * f), size * 1.4):
                        c.text(x0, b, text, font, size, ink, a * ghost)
                if x1 > xg:
                    with c.clip(xg, b - size * 1.1, x1 - xg + 2 * f, size * 1.6):
                        c.text(x0, b, text, font, size, ink, a)
                    if wr < 1:                   # marker tip
                        c.circle(x1, b - size * 0.25, 4 * f, ink, a)
                if cuts and tok > 0.002:
                    for k, n in enumerate(cuts):
                        cx = x0 + c.measure(text[:n], font, size)[0]
                        if cx > xg and cx < x1:
                            p = clamp(tok * len(cuts) * 1.0 - k * 0.7)
                            c.line(cx, b + size * 0.18, cx, b + size * 0.18 - size * 1.0 * p, col, 3 * f, a)
    return g


def penghapus(c, cx, cy, s=1.0, look="paper", color=None, smudge=0.0, rot=0.0, alpha=1.0):
    """Whiteboard eraser centred on (cx, cy): a handle block in color on a grey felt pad (pad faces down, the
    board side). smudge 0..1 = ink picked up on the felt edge. Size 200 × 64 at s = 1."""
    if alpha <= 0.002:
        return
    col = ORANGE if color is None else color
    w, h = 200 * s, 64 * s
    x, y = -w / 2, -h / 2
    with c.group(alpha), c.at(cx, cy, 1.0, rot=rot):
        mat.body(c, look, mat.rrect_path(x + 10 * s, y, w - 20 * s, h * 0.62, 16 * s),
                 (x + 10 * s, y, w - 20 * s, h * 0.62), col, r=16 * s, lift=0.8)
        fy = y + h * 0.58
        mat.body(c, look, mat.rrect_path(x, fy, w, h * 0.42, 6 * s), (x, fy, w, h * 0.42),
                 tk.C.get("body", tk.C["muted"]), r=6 * s, shadow=False)
        for i in range(7):                      # felt fibres
            fx = x + 14 * s + i * (w - 28 * s) / 6
            c.line(fx, fy + 6 * s, fx + 4 * s, fy + h * 0.42 - 6 * s, tk.C["faint"], 1.2 * s, 0.5)
        if smudge > 0.002:
            for i, (u, v_, ln) in enumerate(((0.12, 0.35, 0.5), (0.3, 0.6, 0.45), (0.55, 0.42, 0.3))):
                sx = x + w * u
                c.line(sx, fy + h * 0.42 * v_, sx + w * ln * smudge, fy + h * 0.42 * v_, INK, 4 * s, 0.55)


def memori(c, x, y, w, cells=8, lit=0.0, look="paper", color=None, label="GPU memory", alpha=1.0):
    """GPU memory as a memory stick, top-left (x, y), width w (height 0.2 w): dark board, `cells` chips in a row,
    the first `lit` (float) of them lit in color, gold-ish contacts along the bottom edge, mono label above."""
    if alpha <= 0.002:
        return
    col = ORANGE if color is None else color
    h = w * 0.2
    f = w / 848
    with c.group(alpha):
        c.text(x, y - 14 * f, label.upper(), F["mono_med"], max(19, 19 * f), tk.C["muted"], 1.0, ls=0.16)
        mat.body(c, look, mat.rrect_path(x, y, w, h, 10 * f), (x, y, w, h), INK, r=10 * f, lift=0.5)
        n = max(1, int(round(cells)))
        gap = 12 * f
        cw = (w - 40 * f - gap * (n - 1)) / n
        for i in range(n):
            px = x + 20 * f + i * (cw + gap)
            on = clamp(lit - i)
            c.fill_rrect(px, y + 18 * f, cw, h * 0.52, 5 * f, tk.C["muted"], 0.55)
            if on > 0:
                c.fill_rrect(px, y + 18 * f, cw, h * 0.52, 5 * f, col, on)
        pins = 34
        pw = (w - 60 * f) / pins
        for i in range(pins):
            c.fill_rrect(x + 30 * f + i * pw + pw * 0.2, y + h - 22 * f, pw * 0.6, 16 * f, 2 * f,
                         tk.C["faint"], 0.9)
        c.fill_rrect(x + w * 0.42, y + h - 24 * f, 14 * f, 26 * f, 3 * f, tk.C["bg"], 1.0)   # key notch
