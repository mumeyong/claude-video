"""Designed TikTok cover (1080×1920) — set per video with `v.cover = lambda c: cover(c, ...)` in scenes.py.

TikTok's profile grid crops covers to the centre 3:4 (≈ y 240–1680), so everything important sits in y 430–1500.
The layout is fixed (brand DNA → the profile grid reads as one channel); title, hero, color and tags change per video.

    cover(c, "Kenalan: aku *Mumeyong*.", kicker="KENALAN", color=TEAL, tags=["4 cloud", "$14.000 / bulan"],
          hero=lambda c, box: ...)          # box = (x, y, w, h) area for the video's hero object
"""
import cairo

from .. import tokens as tk
from .headline import Headline
from . import icons

TOP, BOTTOM = 430, 1500          # inside the 3:4 grid crop


def cover(c, title, hero=None, kicker="", color=None, tags=(), badge=""):
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
