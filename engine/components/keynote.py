"""Keynote motion (2026-10-08; Apple craft layer = default from 2026-10-11, STYLE §3): the Apple product-film / iOS feel — silk springs with no visible bounce,
shapes that morph (Dynamic Island, App Store card expand), bento grids that assemble, text that inks in, a hero
that shrinks from full-bleed into place, a 3D-ish turn, button presses, floating sheets.

Pairs with kinetic.py (Rig, sheen, parallax). STYLE §3 lists both. No frosted-glass blur (STYLE §4).

    m = Morph((440, 300, 200, 56), r=28)                    # a pill …
    m.to(t1, (81, 600, 848, 520), r=44)                     # … grows into a card (silk spring)
    m.draw(c, t, C["ink"], content=lambda c, box, k: …)     # k = index of the key we're on / blending to
    bento(c, t, t0, (X, 600, CW, 800), [(0, 0, 2, 1, draw_a), (0, 1, 1, 1, draw_b), …], cols=2, rows=3)
    with yaw(c, cx, cy, turn_at(t, t0)): phone(...)          # product turns to face the camera
"""
import math
from contextlib import contextmanager

from .. import tokens as tk
from ..ease import clamp, curve, in_out_cubic, ios_settle, ios_spring, lerp, out_quint, prog
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


# ── Apple motion craft (STYLE §3, 2026-10-11 — the default grammar for every new video) ───────────
# One leader at a time · arrive ON the stressed word · hold still after arriving · opacity leads, position follows ·
# exits faster + quieter than entrances · continuity (shared element / depth swap) instead of exit-then-enter.
_ARRIVE = {}


def ios_at(t, t0, preset="smooth"):
    """iOS spring progress (tk.IOS preset) for a move that starts at t0. 0 before t0, may overshoot for snappy/bouncy."""
    return ios_spring(t - t0, *tk.IOS[preset])


def ios_dur(preset="smooth"):
    """Visual duration (s) of an iOS spring preset — use it to budget holds."""
    return ios_settle(*tk.IOS[preset])


def arrive(t_hit, preset="smooth", frac=0.9):
    """Start time so the move is `frac` of the way there exactly at t_hit — land ON the stressed word
    (t_hit = T.word("L07", "kode")), don't start on it. Never earlier than needed, never late."""
    key = (preset, frac)
    if key not in _ARRIVE:
        dt = 0.0
        while ios_at(dt, 0.0, preset) < frac and dt < 4:
            dt += 1 / 240
        _ARRIVE[key] = dt
    return t_hit - _ARRIVE[key]


def follow(t_lead, i=1, gap=None):
    """Start time of the i-th follower: one leader moves, the rest follow tk.M['follow_gap'] apart
    (and with ≤ tk.M['follow_amp'] of the leader's travel)."""
    return t_lead + i * (tk.M["follow_gap"] if gap is None else gap)


def presence(t, t_in, t_out=None, preset="smooth"):
    """(move, opacity) of an element on the Apple grammar: move = iOS spring 0→1 from t_in (position/scale),
    opacity leads (done at op_lead of the move) and fades out quietly from t_out (apple_in, quiet_out)."""
    M = tk.M
    mv = ios_at(t, t_in, preset)
    op = curve("apple_out")(prog(t, t_in, ios_dur(preset) * M["op_lead"]))
    if t_out is not None:
        op *= 1 - curve("apple_in")(prog(t, t_out, M["quiet_out"]))
    return mv, op


def rise(c, t, t_in, t_out, bbox, draw, dy=None, preset="smooth", scale=None):
    """Apple fade-up: draw(c) at rest; arrives from dy below and a touch small (rise_scale), opacity first,
    no blur. Exit = quiet (fade + scale .98, faster than the entrance). Travel scales gently with object height."""
    M = tk.M
    x, y, w, h = bbox
    mv, op = presence(t, t_in, t_out, preset)
    if op <= 0.002:
        return
    dy = M["rise_dy"] * (1 + min(1.2, h / 900)) if dy is None else dy
    s0 = M["rise_scale"] if scale is None else scale
    b = 0.0 if t_out is None else curve("apple_in")(prog(t, t_out, M["quiet_out"]))
    s = lerp(s0, 1.0, mv) * lerp(1.0, M["quiet_scale"], b)
    with c.at(0, dy * (1 - mv), s, origin=(x + w / 2, y + h / 2)):
        with c.group(op):
            draw(c)


def wipe(c, t, t0, bbox, draw, t_out=None, dur=None, direction="right", soft=None):
    """Soft-edged mask wipe (keynote title / product reveal): a feathered edge sweeps across bbox on apple_out and
    uncovers draw(c). direction: right · left · up · down. Exit = quiet fade."""
    import cairo
    M = tk.M
    dur = M["wipe_in"] if dur is None else dur
    soft = M["wipe_soft"] if soft is None else soft
    p = curve("apple_out")(prog(t, t0, dur))
    b = 0.0 if t_out is None else curve("apple_in")(prog(t, t_out, M["quiet_out"]))
    vis = 1 - b
    if p <= 0.001 or vis <= 0.002:
        return
    x, y, w, h = bbox
    if p >= 0.999:
        with c.group(vis):
            draw(c)
        return
    horiz = direction in ("right", "left")
    L = w if horiz else h
    f = p * L * (1 + soft) - soft * L          # px of the leading edge along the sweep
    u0, u1 = f, f + soft * L
    if direction == "right":
        g = cairo.LinearGradient(x + u0, 0, x + u1, 0)
    elif direction == "left":
        g = cairo.LinearGradient(x + w - u0, 0, x + w - u1, 0)
    elif direction == "down":
        g = cairo.LinearGradient(0, y + u0, 0, y + u1)
    else:  # up
        g = cairo.LinearGradient(0, y + h - u0, 0, y + h - u1)
    g.add_color_stop_rgba(0, 0, 0, 0, vis)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cx = c.ctx
    cx.push_group()
    draw(c)
    cx.pop_group_to_source()
    cx.mask(g)


def depth_swap(c, t, t_swap, bbox, old, new, dur=None):
    """Keynote push-through: old content falls back (scale → .92, fades fast) while new content comes forward from
    1.06 to rest — one continuous move, no empty frame. old(c) / new(c) draw at rest inside bbox."""
    M = tk.M
    dur = M["swap_dur"] if dur is None else dur
    x, y, w, h = bbox
    o = (x + w / 2, y + h / 2)
    q = curve("apple_in_out")(prog(t, t_swap, dur))
    if q < 1:
        a_old = 1 - curve("apple_out")(prog(t, t_swap, dur * 0.55))
        if a_old > 0.002:
            with c.at(0, 0, lerp(1.0, M["swap_back"], q), origin=o):
                with c.group(a_old):
                    old(c)
    if t >= t_swap:
        a_new = curve("apple_out")(prog(t, t_swap + dur * 0.2, dur * 0.6))
        if a_new > 0.002:
            with c.at(0, 0, lerp(M["swap_front"], 1.0, curve("apple_out")(prog(t, t_swap, dur))), origin=o):
                with c.group(a_new):
                    new(c)


def focus_pull(c, t, t0, t1, bbox, draw):
    """Rack focus: while a foreground element (sheet, card, number) is up between t0 and t1, the background
    draw(c) goes soft — depth-of-field blur + scale .965 + dim. Depth, not a frosted-glass panel (STYLE §4)."""
    M = tk.M
    k = curve("apple")(prog(t, t0, 0.6)) * (1 - (0.0 if t1 is None else curve("apple")(prog(t, t1, 0.6))))
    if k <= 0.002:
        draw(c)
        return
    x, y, w, h = bbox
    with c.at(0, 0, lerp(1.0, M["focus_scale"], k), origin=(x + w / 2, y + h / 2)):
        with c.layer(bbox, 1 - M["focus_dim"] * k, M["focus_blur"] * k):
            draw(c)


# ── Apple camera: motivated, never decorative ───────────────────────────
def dolly(v, t0, t1, zoom=None, x=None, y=None, base=1.0):
    """Slow push over a HOLD (the only motion allowed while the content rests): base → base + dolly_zoom,
    apple_dolly curve across the whole hold. Don't stack it on top of a big content move."""
    z = base + (tk.M["dolly_zoom"] if zoom is None else zoom)
    v.camera.key(t0, zoom=z, x=x, y=y, dur=max(0.3, t1 - t0), ease=curve("apple_dolly"))
    return v.camera


def push(v, t, box, zoom=1.08, dur=0.9):
    """Motivated push to the next focus (the thing being spoken about), apple_in_out. Time it with arrive()."""
    return v.camera.focus(t, box, zoom=zoom, dur=dur, ease=curve("apple_in_out"))


def cut(v, t, zoom=1.0, x=None, y=None):
    """Hard camera cut (keynote edit) — new framing on the beat/word, no move. Contrast for the next hold."""
    return v.camera.key(t, zoom=zoom, x=x, y=y, dur=0.001)
