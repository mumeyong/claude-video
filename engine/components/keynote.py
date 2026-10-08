"""Keynote motion (opt-in, 2026-10-08): the Apple product-film / iOS feel — silk springs with no visible bounce,
shapes that morph (Dynamic Island, App Store card expand), bento grids that assemble, text that inks in, a hero
that shrinks from full-bleed into place, a 3D-ish turn, button presses, floating sheets.

Pairs with kinetic.py (Rig, sheen, parallax). STYLE §6d lists both. No frosted-glass blur (banned, §8).

    m = Morph((440, 300, 200, 56), r=28)                    # a pill …
    m.to(t1, (81, 600, 848, 520), r=44)                     # … grows into a card (silk spring)
    m.draw(c, t, C["ink"], content=lambda c, box, k: …)     # k = index of the key we're on / blending to
    bento(c, t, t0, (X, 600, CW, 800), [(0, 0, 2, 1, draw_a), (0, 1, 1, 1, draw_b), …], cols=2, rows=3)
    with yaw(c, cx, cy, turn_at(t, t0)): phone(...)          # product turns to face the camera
"""
import math
from contextlib import contextmanager

from .. import tokens as tk
from ..ease import clamp, in_out_cubic, lerp, out_quint, prog
from .kinetic import spring_p, spring_at


# ── shape morph (Dynamic Island / card expand) ──────────────────────────
class Morph:
    """A rounded rect whose box + radius spring between keys. Content cross-fades between keys."""

    def __init__(self, box, r=None, preset="silk"):
        self.base = (tuple(box), tk.L["radius_card"] if r is None else r)
        self.preset = preset
        self.keys = []  # (t, dur, box, r, preset)

    def to(self, t, box, r=None, dur=None, preset=None):
        preset = preset or self.preset
        self.keys.append((float(t), dur or tk.SPRING[preset][2], tuple(box), r, preset))
        self.keys.sort(key=lambda k: k[0])
        return self

    def state(self, t):
        """(box, r, k, blend): k = index of the last key started (0 = base), blend 0..1 into it."""
        box, r = self.base
        k, blend = 0, 1.0
        for i, (kt, d, kb, kr, preset) in enumerate(self.keys):
            if t < kt:
                break
            p = prog(t, kt, d)
            e = spring_p(p, preset)
            box = tuple(lerp(a, b, e) for a, b in zip(box, kb))
            r = lerp(r, r if kr is None else kr, e)
            k, blend = i + 1, in_out_cubic(clamp(p * 2.2))
        x, y, w, h = box
        return (x, y, max(1.0, w), max(1.0, h)), min(r, w / 2, h / 2), k, blend

    def draw(self, c, t, color, content=None, shadow="card", alpha=1.0):
        """Fill the shape; content(c, box, k) draws inside it (clipped), old key fading out as the new fades in."""
        box, r, k, blend = self.state(t)
        x, y, w, h = box
        if shadow:
            sh = tk.SHADOW[shadow]
            c.shadow(x, y, w, h, r, sh["blur"], sh["dy"], sh["alpha"] * alpha * (1 - 0.6 * c.dark))
        c.fill_rrect(x, y, w, h, r, color, alpha)
        if content is None:
            return
        with c.clip(x, y, w, h, r):
            if k > 0 and blend < 1:
                with c.group(alpha * (1 - blend)):
                    content(c, box, k - 1)
            with c.group(alpha * (blend if k > 0 else 1.0)):
                content(c, box, k)


# ── bento grid ──────────────────────────────────────────────────────────
def bento(c, t, t0, area, tiles, cols=2, rows=2, gap=None, t_out=None, card=True):
    """Tiles assemble into a grid: each rises + scales from .94 + fades, staggered outward from the first tile.
    tiles: [(col, row, col_span, row_span, draw(c, x, y, w, h, p))] — p 0..1 is that tile's own entrance."""
    M = tk.M
    gap = M["bento_gap"] if gap is None else gap
    X, Y, W, H = area
    cw, rh = (W - gap * (cols - 1)) / cols, (H - gap * (rows - 1)) / rows
    b = 0.0 if t_out is None else in_out_cubic(prog(t, t_out, M["out"]))
    if t < t0 or b >= 1:
        return
    for (col, row, cs, rs, draw) in tiles:
        x, y = X + col * (cw + gap), Y + row * (rh + gap)
        w, h = cw * cs + gap * (cs - 1), rh * rs + gap * (rs - 1)
        ti = t0 + math.hypot(col, row) * M["bento_stagger"]
        p = out_quint(prog(t, ti, M["bento_in"]))
        if p <= 0.002:
            continue
        s = 0.94 + 0.06 * p
        with c.at(0, (1 - p) * 40 - b * 16, s, origin=(x + w / 2, y + h / 2)):
            with c.group(p * (1 - b)):
                if card:
                    c.card(x, y, w, h, r=tk.L["radius_bento"])
                draw(c, x, y, w, h, p)


# ── product turn ────────────────────────────────────────────────────────
def turn_at(t, t0, from_angle=None, dur=None):
    """Yaw angle (radians) easing from from_angle to 0 (facing the camera) on a silk spring."""
    a0 = tk.M["turn_from"] if from_angle is None else from_angle
    return a0 * (1 - spring_at(t, t0, "silk", dur))


@contextmanager
def yaw(c, cx, cy, angle):
    """Fake 3D turn around the vertical axis through (cx, cy): horizontal squash by cos + slight shear."""
    k = math.cos(angle)
    cx_ = c.ctx
    cx_.save()
    cx_.translate(cx, cy)
    if abs(angle) > 1e-4:
        import cairo
        cx_.transform(cairo.Matrix(max(0.05, k), math.sin(angle) * 0.08, 0, 1, 0, 0))
    cx_.translate(-cx, -cy)
    try:
        yield c
    finally:
        cx_.restore()


# ── iOS micro-interactions ──────────────────────────────────────────────
def press(t, t0):
    """Button press scale: 1 → .94 in 0.12 s, then springs back (snappy). Use as c.at(scale=press(t, t_tap))."""
    if t < t0:
        return 1.0
    dip = tk.M["press_dip"]
    if t < t0 + 0.12:
        return 1 - dip * out_quint(prog(t, t0, 0.12))
    return 1 - dip + dip * spring_at(t, t0 + 0.12, "snappy")


def sheet(c, t, t_in, t_out, box, draw, dim=None, r=None):
    """Floating sheet that slides up from below the frame on a silk spring and dims what's behind it.
    box = resting (x, y, w, h). draw(c, x, y, w, h) draws the sheet contents. Exit = slide back down."""
    dim = tk.M["sheet_dim"] if dim is None else dim
    a = spring_at(t, t_in, "silk")
    b = 0.0 if t_out is None else in_out_cubic(prog(t, t_out, tk.M["out"] * 1.4))
    vis = min(1.0, a) * (1 - b)
    if vis <= 0.002:
        return
    c.src(c.theme("ink", "d_bg"), dim * vis)
    c.ctx.rectangle(0, 0, tk.W, tk.H)
    c.ctx.fill()
    x, y, w, h = box
    dy = (1 - a) * (tk.H - y) + b * (tk.H - y)
    r = tk.L["radius_bento"] if r is None else r
    with c.at(0, dy):
        c.card(x, y, w, h, r=r, shadow="chat")
        c.fill_rrect(x + w / 2 - 36, y + 14, 72, 8, 4, c.theme("faint", "d_line"))  # grabber
        draw(c, x, y, w, h)
