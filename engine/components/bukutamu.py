"""Guestbook components (first used in "wifi-ep04-restart-router", Bongkar WiFi Rumah EP 04).

buku_tamu · buku_geo
Metaphor: the router is the guard at the gate (EP 02) who writes every connection into a guestbook, one row each
(the NAT table). The page fills up, new guests wait; a restart tears the page out and the book is clean again — but
every restart leaves a torn stub at the binding, and a binding full of stubs is a symptom, not a cure.
Signature: the right page lifts off the binding and falls away (tear 0 → 1), a clean page underneath.
Pure functions of their progress values (frame = f(t)). The book is a physical object: paper stays paper in the dark
section. Colors from tokens; shading via material (look="flat" | "paper" | "lit").
"""
import math

from .. import tokens as tk
from ..ease import clamp, lerp, mix
from . import material as mat
from .payday import torn_flight
from .kasir import stempel

RED = tk.CHAPTER[5][0]               # signature: the cardboard cover, stubs, stamps
PAPER = tk.C["brand_paper"]
INK = tk.C["brand_ink"]
F = tk.F
NROWS = 8
COLS = ("JAM", "TAMU", "TUJUAN")


def buku_geo(x, y, w):
    """Geometry of buku_tamu drawn with the same x, y, w (no drawing): dict with f, h, left/right page boxes,
    rows (baseline y of each right-page row), row_h, mem (memory meter box), gutter x."""
    f = w / 900
    h = w * 0.64
    m, top, bot = 20 * f, 18 * f, 26 * f
    pw = w / 2 - m
    ph = h - top - bot
    left = (x + m, y + top, pw, ph)
    right = (x + w / 2, y + top, pw, ph)
    head = 96 * f
    row_h = (ph - head - 18 * f) / NROWS
    rows = [y + top + head + row_h * (i + 1) - 14 * f for i in range(NROWS)]
    mem = (left[0] + 44 * f, y + top + ph - 120 * f, pw - 88 * f, 34 * f)
    return dict(f=f, h=h, left=left, right=right, rows=rows, row_h=row_h, mem=mem, gutter=x + w / 2)


def _page_path(px, py, pw, ph, f, torn_left=False):
    """Right-page outline; torn_left gives it the ragged edge it has once it is ripped off the binding."""
    if not torn_left:
        return mat.rrect_path(px, py, pw, ph, 6 * f)
    pts = [(px + pw, py), (px + pw, py + ph)]
    n = 16
    for k in range(n + 1):
        yy = py + ph - ph * k / n
        jag = (7 if k % 2 else 0) * f + 3 * f * math.sin(k * 2.7)
        pts.append((px + jag, yy))
    return mat.poly_path(pts)


def _ruled(c, px, py, pw, ph, g, alpha):
    f = g["f"]
    muted = mix(INK, PAPER, 0.55)
    x0, x1 = px + 30 * f, px + pw - 26 * f
    cx = [x0, x0 + 96 * f, x0 + 236 * f]
    for k, lab in enumerate(COLS):
        c.text(cx[k], py + 64 * f, lab, F["mono_med"], 20 * f, muted, alpha, 0.14)
    c.line(x0, py + 84 * f, x1, py + 84 * f, INK, max(1.5, 2.2 * f), 0.5 * alpha)
    for yy in g["rows"]:
        c.line(x0, yy + 14 * f, x1, yy + 14 * f, tk.C["accent"], max(1.0, 1.4 * f), 0.16 * alpha)
    c.line(cx[1] - 14 * f, py + 40 * f, cx[1] - 14 * f, py + ph - 20 * f, RED, max(1.0, 1.6 * f), 0.35 * alpha)
    return cx


def _right_page(c, look, px, py, pw, ph, g, rows, fill, stamp, stamp_p, color, alpha, torn=False, shadow=False):
    f = g["f"]
    mat.body(c, look, _page_path(px, py, pw, ph, f, torn), (px, py, pw, ph), PAPER, alpha, r=6 * f,
             lift=0.6, shadow=shadow)
    cx = _ruled(c, px, py, pw, ph, g, alpha)
    n = len(rows)
    shown = clamp(fill) * n
    for i, r in enumerate(rows[:NROWS]):
        a = clamp(shown - i) * clamp(r.get("a", 1.0)) * alpha
        if a <= 0.002:
            continue
        base = g["rows"][i]
        c.text(cx[0], base, r.get("jam", ""), F["mono"], 22 * f, INK, a, 0.0)
        c.text(cx[1], base + 2 * f, r.get("tamu", ""), F["serif"], 32 * f, INK, a, 0.0)
        c.text(cx[2], base + 2 * f, r.get("ke", ""), F["serif"], 32 * f, INK, a, 0.0)
    if stamp and stamp_p > 0.002:
        stempel(c, px + pw * 0.55, py + ph * 0.56, stamp, stamp_p, color, 44 * f, rot=-0.16, alpha=alpha)


def buku_tamu(c, x, y, w, rows=(), fill=1.0, under=(), under_fill=0.0, tear=0.0, stubs=0.0, mem=0.0,
              stamp=None, stamp_p=0.0, title="BUKU TAMU", sub="POS · ROUTER", look="flat", color=None, alpha=1.0):
    """Open guestbook lying on the desk, top-left (x, y), width w (height 0.64 w): cardboard cover in color, left page
    = title + sub + a hand-drawn MEMORY meter (mem 0..1, turns color when nearly full), right page = ruled rows.
    rows = [dict(jam, tamu, ke, a)] on the top right page, inked in order by fill 0..1 (max NROWS rows).
    tear 0..1 rips that page off the binding and drops it away (with its rows and its stamp), revealing the page
    under it (under / under_fill). stubs (float) = torn stubs already sticking out of the binding, the last one
    fading in. stamp = text pressed on the top page by stamp_p 0..1 (stempel). Returns buku_geo(x, y, w)."""
    g = buku_geo(x, y, w)
    if alpha <= 0.002:
        return g
    color = color or RED
    f, h = g["f"], g["h"]
    lx, ly, lw, lh = g["left"]
    rx, ry, rw, rh = g["right"]
    muted = mix(INK, PAPER, 0.5)
    with c.group(alpha):
        if look == "flat":
            c.shadow(x, y, w, h, 16 * f, 40 * f, 16 * f, 0.09)
        mat.body(c, look, mat.rrect_path(x, y, w, h, 16 * f), (x, y, w, h), color, r=16 * f, lift=1.0)
        # left page: title, sub, memory meter
        mat.body(c, look, mat.rrect_path(lx, ly, lw, lh, 6 * f), (lx, ly, lw, lh), PAPER, r=6 * f, shadow=False)
        c.text(lx + 44 * f, ly + 96 * f, title, F["mono_bold"], 34 * f, INK, 1, 0.12)
        c.text(lx + 44 * f, ly + 140 * f, sub, F["mono"], 22 * f, muted, 1, 0.08)
        c.line(lx + 44 * f, ly + 172 * f, lx + lw - 44 * f, ly + 172 * f, INK, max(1.5, 2.2 * f), 0.35)
        c.text(lx + 44 * f, ly + 250 * f, "semua tamu", F["serif"], 34 * f, muted, 1, 0.0)
        c.text(lx + 44 * f, ly + 292 * f, "wajib dicatat.", F["serif"], 34 * f, muted, 1, 0.0)
        mx, my, mw, mh = g["mem"]
        c.text(mx, my - 18 * f, "MEMORY", F["mono_med"], 20 * f, muted, 1, 0.16)
        m = clamp(mem)
        c.stroke_rrect(mx, my, mw, mh, 6 * f, INK, max(1.5, 2.4 * f), 0.55)
        if m > 0.004:
            hot = clamp((m - 0.7) / 0.25)
            c.fill_rrect(mx + 5 * f, my + 5 * f, (mw - 10 * f) * m, mh - 10 * f, 4 * f, mix(muted, color, hot), 0.85)
        # gutter shade
        c.fill_rrect(g["gutter"] - 10 * f, ly, 20 * f, lh, 6 * f, INK, 0.08)
        # page under the top one (clean, or refilling)
        _right_page(c, look, rx, ry, rw, rh, g, list(under), under_fill, None, 0.0, color, 1.0)
        # torn stubs at the binding
        ns = max(0.0, stubs)
        for k in range(int(math.ceil(ns))):
            a = clamp(ns - k)
            sx = g["gutter"] + (4 + 7 * k) * f
            pts = [(sx, ry + 2 * f)]
            for j in range(13):
                yy = ry + rh * j / 12
                pts.append((sx + (9 + 5 * ((j + k) % 2)) * f, yy))
            pts.append((sx, ry + rh))
            mat.body(c, look, mat.poly_path(pts), (sx, ry, 16 * f, rh), mix(PAPER, color, 0.08), a, r=2, lift=0.2,
                     shadow=look != "flat")
            c.line(sx + 9 * f, ry + 6 * f, sx + 9 * f, ry + rh - 6 * f, color, max(1.0, 1.4 * f), 0.35 * a)
        # the top page — rips off along the binding and falls away
        p = clamp(tear)
        if p < 0.999:
            dx, dy, rot, a = torn_flight(p, rw, rh)
            lift = math.sin(math.pi * min(1.0, p * 2)) * 0.6
            with c.at(dx * 0.8, dy, 1.0, origin=(rx, ry), rot=rot * 0.7):
                _right_page(c, look, rx, ry, rw, rh, g, list(rows), fill, stamp, stamp_p, color, a,
                            torn=p > 0.001, shadow=p > 0.001)
                if lift > 0.01:
                    c.fill_rrect(rx, ry, rw, rh, 6 * f, INK, 0.05 * lift * a)
    return g
