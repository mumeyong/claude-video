"""Designed TikTok cover (1080×1920) — set per video with `v.cover = lambda c: cover(c, ...)` in scenes.py.

TikTok's profile grid crops covers to the centre 3:4 (≈ y 240–1680), so everything important sits in y 430–1500.
Default look "air" (2026-10-19): one flat ground, one hook, one small hero, lots of empty space — a cover is read at
thumbnail size, so less is louder. The layout is fixed (the profile grid reads as one channel); ground, ink, accent,
title and hero change per video. look="glow" keeps the older canvas + glow + tag-pill layout.

    cover(c, "Sedang\\ndiproses?", turn="Uangmu lagi nunggu bus.", kicker="23.40 · transfer antar bank",
          bg=YELLOW, ink=INK, color=RED, hero=lambda c, box: ...)   # box = (x, y, w, h), keep the hero small
"""
import cairo

from .. import tokens as tk
from .headline import Headline
from . import icons

TOP, BOTTOM = 430, 1500          # inside the 3:4 grid crop
AIR = dict(title_max=200, title_ls=-0.045, title_lead=0.9, turn_max=88, kicker=28,
           hero_h=380,           # the hero never grows past this — the rest stays empty
           brand=24, display="Inter Display ExtraBold", grain=0.05)


def cover(c, title, hero=None, kicker="", color=None, tags=(), badge="", turn="", bg=None, ink=None, look="air"):
    """title: '\\n' splits lines, *word* = serif italic turn. turn: one quiet serif line under the title.
    tags: shown as one small mono line (air) or pills (glow)."""
    if look == "glow":
        return _glow(c, title, hero, kicker, color, tags, badge)
    color = color or tk.C["accent"]
    bg, ink = bg or tk.C["bg"], ink or tk.C["ink"]
    W, H, X, CW = tk.W, tk.H, tk.L["col_x"], tk.L["col_w"]
    cx = c.ctx
    c.src(bg)
    cx.rectangle(0, 0, W, H)
    cx.fill()
    y = TOP + 40
    if kicker:
        c.circle(X + 8, y - 9, 8, color)
        c.text(X + 30, y, kicker.upper(), tk.F["mono_bold"], AIR["kicker"], ink, 0.75, 0.16)
    # title: as large as the longest line allows
    lines = title.split("\n")
    size = AIR["title_max"]
    for ln in lines:
        w = c.measure(_markup(ln), AIR["display"], size, AIR["title_ls"], markup=True)[0]
        if w > CW:
            size *= CW / w
    y += 40 + size * 0.78
    for i, ln in enumerate(lines):
        c.text(X - size * 0.03, y, _markup(ln), AIR["display"], size, ink, 1, AIR["title_ls"], markup=True)
        if i < len(lines) - 1:
            y += size * AIR["title_lead"]
    if turn:
        ts = min(AIR["turn_max"], AIR["turn_max"] * CW / c.measure(turn, tk.F["serif"], AIR["turn_max"])[0])
        y += ts * 1.25
        c.text(X, y, turn, tk.F["serif"], ts, ink, 0.85)
    # hero: small, bottom-anchored above the brand row, empty space between it and the title
    by = BOTTOM - 20
    if hero:
        hh = min(AIR["hero_h"], by - 90 - (y + 120))
        if hh > 80:
            hero(c, (X, by - 70 - hh, CW, hh))
    icons.play_logo(c, X + 20, by - 9, 20, ink)
    c.text(X + 52, by, tk.BRAND, tk.F["mono_bold"], AIR["brand"], ink, 1, 0.2)
    right = badge or "  ·  ".join(tags)
    if right:
        c.text(X + CW, by, right.upper(), tk.F["mono_bold"], AIR["brand"], ink, 0.6, 0.14, align="r")
    _grain(c, AIR["grain"])


def _markup(line):
    """*word* → Instrument Serif italic, the rest stays in the display face."""
    from gi.repository import GLib
    parts = line.split("*")
    return "".join(f'<span font_desc="{tk.F["serif"]}">{GLib.markup_escape_text(p)}</span>' if i % 2
                   else GLib.markup_escape_text(p) for i, p in enumerate(parts))


def _grain(c, amount, seed=7):
    """Seeded paper grain so a flat ground doesn't look like an empty slide."""
    import numpy as np
    n = np.random.default_rng(seed).integers(0, 256, size=(tk.H, tk.W), dtype=np.uint8)
    v = (n * amount).astype(np.uint8)
    px = np.ascontiguousarray(np.dstack([v, v, v, np.full_like(n, int(255 * amount))]))   # premultiplied BGRA
    surf = cairo.ImageSurface.create_for_data(memoryview(px), cairo.FORMAT_ARGB32, tk.W, tk.H, tk.W * 4)
    c.ctx.set_source_surface(surf, 0, 0)
    c.ctx.paint()


def _glow(c, title, hero, kicker, color, tags, badge):
    color = color or tk.C["accent"]
    W, H, X, CW = tk.W, tk.H, tk.L["col_x"], tk.L["col_w"]
    cx = c.ctx
    # background: canvas + glow in the video's signature color
    c.src(tk.C["bg"])
    cx.rectangle(0, 0, W, H)
    cx.fill()
    for (gx, gy, rad, a) in ((W * 0.9, TOP + 60, 900, 0.22), (W * 0.05, BOTTOM - 100, 950, 0.16)):
        g = cairo.RadialGradient(gx, gy, 0, gx, gy, rad)
        g.add_color_stop_rgba(0, *color[:3], a)
        g.add_color_stop_rgba(1, *color[:3], 0)
        cx.set_source(g)
        cx.rectangle(0, 0, W, H)
        cx.fill()
    # kicker
    y = TOP + 40
    if kicker:
        c.circle(X + 8, y - 8, 8, color)
        c.text(X + 28, y, kicker.upper(), tk.F["mono_med"], 26, tk.C["ink2"], 1, 0.2)
    # title (fully shown — no animation)
    h = Headline(title, x=X, y=y + 30, style="headline_lg", width=CW)
    h.draw(c, 1e6, 0.0)
    hero_top = h.bottom(c) + 40
    # tags + brand row at the bottom of the safe zone
    tag_y = BOTTOM - 150
    if hero:
        hero(c, (X, hero_top, CW, tag_y - 30 - hero_top))
    tx = X
    for lbl in tags:                      # big pills: covers are seen as small thumbnails
        tw = c.measure(lbl, tk.F["ui_semi"], 34, -0.01)[0] + 44
        if tx + tw > X + CW:
            break
        c.fill_rrect(tx, tag_y, tw, 68, 34, color, 0.14)
        c.text(tx + 22, tag_y + 46, lbl, tk.F["ui_semi"], 34, color, 1, -0.01)
        tx += tw + 12
    by = BOTTOM - 40
    icons.play_logo(c, X + 22, by - 10, 22, tk.C["ink"])
    c.text(X + 58, by, tk.BRAND, tk.F["mono_bold"], 24, tk.C["ink"], 1, 0.2)
    if badge:
        c.text(X + CW, by, badge, tk.F["mono_bold"], 24, color, 1, 0.16, align="r")
