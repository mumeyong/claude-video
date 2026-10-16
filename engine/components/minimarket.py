"""Minimarket-shelf components (first used in "flash-sale-keranjang"): a rack with yellow price strips, a boxed
product, a stock tag that flips, and people's hands that point (cart) or grab (checkout). Everything is drawn around
its own anchor so a scene can place it under one transform (rack-local coordinates)."""
import math

from .. import tokens as tk
from ..ease import clamp, mix
from . import material as mat

BACK = tk.hexc("#F3F4F6")        # rack back panel
FRAME = tk.hexc("#C9CFD8")       # uprights + top cap
BOARD = tk.hexc("#E3E7EC")       # shelf board top
PRICE = tk.hexc("#FFD43B")       # minimarket yellow price strip
PRICE_INK = tk.hexc("#2B2C29")
FILL = [tk.hexc("#B9C4D3"), tk.hexc("#D5C7B5"), tk.hexc("#C3D2C6"), tk.hexc("#D9C3CB"), tk.hexc("#C8C6DA")]
SKIN = [tk.hexc("#E8B48F"), tk.hexc("#C98E66"), tk.hexc("#A86F4C"), tk.hexc("#F1C6A4")]
SLEEVE = [tk.hexc("#4A5568"), tk.hexc("#8C6D5A"), tk.hexc("#5E7C6B"), tk.hexc("#9AA3AE"),
          tk.hexc("#6B5B7B"), tk.hexc("#3F4E66")]
CAP, BASE, LIP = 40, 50, 34      # top cap, plinth, board thickness (px at scale 1)
PROD_W, PROD_H = 180, 220        # product box at scale 1


def _h(i, k):
    """Seeded 0..1 hash."""
    return (math.sin(i * 12.9898 + k * 78.233) * 43758.5453) % 1.0


def rak_geo(w, h, rows):
    """Board-top y (where items stand) of each row, rack centered on (0, 0). rows = row heights (px)."""
    y = -h / 2 + CAP
    out = []
    for r in rows:
        y += r
        out.append(y - LIP)
    return out


def rak(c, w, h, rows, look="flat", stock=None, alpha=1.0):
    """Shelf rack centered on (0, 0): back panel, uprights, boards with a yellow price lip.
    stock(c, i, x0, y_board, w_inner) draws row i's items standing on y_board (before the lip covers their feet)."""
    if alpha <= 0.002:
        return
    x0, y0 = -w / 2, -h / 2
    with c.group(alpha):
        mat.body(c, look, mat.rrect_path(x0, y0, w, h, 18), (x0, y0, w, h), FRAME, form="box", lift=1.0)
        c.fill_rrect(x0 + 26, y0 + CAP, w - 52, h - CAP - BASE, 6, BACK)
        ys = rak_geo(w, h, rows)
        for i, yb in enumerate(ys):
            c.fill_rrect(x0 + 26, yb - 14, w - 52, 14, 3, BOARD)
            if stock:
                stock(c, i, x0 + 26, yb, w - 52)
            mat.body(c, look, mat.rrect_path(x0 + 14, yb, w - 28, LIP, 6), (x0 + 14, yb, w - 28, LIP), PRICE,
                     form="box", lift=0.0, shadow=False)
            for k in range(6):                                   # price slips printed on the strip
                px = x0 + 40 + k * (w - 80) / 6
                c.fill_rrect(px, yb + 9, 52, 7, 3, PRICE_INK, 0.18)


def filler(c, i, x0, y, w, seed=0, gap=None, alpha=1.0):
    """A row of muted everyday goods (boxes + bottles) standing on y — background stock, never the hero."""
    k, x = 0, x0 + 14
    while True:
        bottle = _h(seed * 31 + k, 1) > 0.6
        bw = 46 if bottle else 70 + 40 * _h(seed * 31 + k, 2)
        bh = (120 if bottle else 90) + 70 * _h(seed * 31 + k, 3)
        if x + bw > x0 + w - 10:
            break
        col = FILL[int(_h(seed * 31 + k, 4) * len(FILL)) % len(FILL)]
        if bottle:
            c.fill_rrect(x + 12, y - bh - 22, bw - 24, 26, 6, mat.tone(col, -0.15), alpha)
        c.fill_rrect(x, y - bh, bw, bh, 12 if bottle else 8, col, alpha)
        c.fill_rrect(x + 8, y - bh * 0.62, bw - 16, bh * 0.22, 4, mat.tone(col, 0.45), alpha)
        x += bw + (gap if gap is not None else 10 + 8 * _h(seed * 31 + k, 5))
        k += 1


def produk(c, cx, by, color, s=1.0, look="flat", grey=0.0, alpha=1.0, ghost=False):
    """The hero product: a box with a lid band and a lightning badge, bottom-center at (cx, by).
    grey 0..1 drains the color (sold out); ghost=True draws an impossible duplicate (dashed outline, pale)."""
    if alpha <= 0.002:
        return
    w, h = PROD_W * s, PROD_H * s
    x, y = cx - w / 2, by - h
    col = mix(color, tk.C["faint"], grey)
    if ghost:
        c.fill_rrect(x, y, w, h, 18 * s, col, alpha * 0.22)
        c.stroke_rrect(x, y, w, h, 18 * s, col, 4 * s, alpha, dash=[14 * s, 10 * s])
        return
    with c.group(alpha):
        mat.body(c, look, mat.rrect_path(x, y, w, h, 18 * s), (x, y, w, h), col, form="box", lift=0.0)
        c.fill_rrect(x, y + 34 * s, w, 16 * s, 0, mat.tone(col, -0.25), 0.55)
        bx, byy = cx, y + h * 0.58
        c.circle(bx, byy, 44 * s, (1, 1, 1, 1), 0.95)
        bolt = [(8, -30), (-16, 4), (-1, 4), (-8, 30), (16, -6), (1, -6)]
        ctx = c.ctx
        ctx.new_path()
        ctx.move_to(bx + bolt[0][0] * s, byy + bolt[0][1] * s)
        for px, py in bolt[1:]:
            ctx.line_to(bx + px * s, byy + py * s)
        ctx.close_path()
        c.src(col)
        ctx.fill()


def empty_spot(c, cx, by, s=1.0, alpha=1.0):
    """Outline where a product used to stand (already sold)."""
    w, h = PROD_W * s, PROD_H * s
    c.stroke_rrect(cx - w / 2, by - h, w, h, 18 * s, tk.C["faint"], 3 * s, alpha, dash=[10 * s, 9 * s])


def label_stok(c, cx, y, text, ink, flip=1.0, alpha=1.0, w=250, h=66):
    """Hanging stock tag (yellow, mono bold) centered on cx, top at y. flip 0..1 = vertical squash of a flip."""
    if alpha <= 0.002:
        return
    sy = max(0.02, abs(flip))
    ctx = c.ctx
    ctx.save()
    ctx.translate(cx, y + h / 2)
    ctx.scale(1, sy)
    ctx.translate(-cx, -(y + h / 2))
    c.fill_rrect(cx - w / 2 + 6, y + 6, w, h, 14, (0, 0, 0, 1), alpha * 0.10)
    c.fill_rrect(cx - w / 2, y, w, h, 14, PRICE, alpha)
    c.text(cx, y + h * 0.66, text, tk.F["mono_bold"], 34, ink, alpha, 0.04, align="c")
    ctx.restore()


def tangan(c, x, y, ang, kind="point", sleeve=None, skin=None, s=1.0, alpha=1.0):
    """A person's hand reaching in: the fingertip (point) or fist front (grab) at (x, y), pointing along ang
    (radians, 0 = to the right); the arm runs back out of frame. kind = 'point' (index finger) | 'grab' (fist)."""
    if alpha <= 0.002:
        return
    sleeve = sleeve or SLEEVE[0]
    skin = skin or SKIN[0]
    dark = mat.tone(skin, -0.18)
    ctx = c.ctx
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    with c.group(alpha):
        if kind == "point":
            fx = -110                                            # fist sits behind the extended finger
            c.fill_rrect(-1500, -34, 1500 + fx - 90, 116, 40, sleeve)
            c.fill_rrect(fx - 120, -30, 40, 108, 14, mat.tone(sleeve, -0.2))
            c.fill_rrect(fx - 96, -24, 112, 100, 36, skin)
            c.fill_rrect(fx - 8, -18, 118, 30, 15, skin)         # index finger
            c.fill_rrect(fx + 80, -14, 22, 22, 9, mat.tone(skin, 0.25))   # nail
            for k in range(3):
                c.fill_rrect(fx - 6, 18 + k * 18, 26, 14, 7, dark)
            c.fill_rrect(fx - 70, -36, 64, 26, 13, dark)          # thumb
        else:
            c.fill_rrect(-1500, -54, 1500 - 150, 116, 40, sleeve)
            c.fill_rrect(-180, -50, 40, 108, 14, mat.tone(sleeve, -0.2))
            c.fill_rrect(-150, -52, 150, 112, 40, skin)
            for k in range(4):
                c.fill_rrect(-34, -44 + k * 26, 30, 20, 9, dark)
            c.fill_rrect(-110, -66, 76, 28, 14, dark)             # thumb over the top
    ctx.restore()
