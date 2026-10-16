"""Material layer (2026-10-12, STYLE §1) — light, shade and texture, so a hero reads as a rendered object, not an icon.

The look of a video is how its objects are SHADED, not only what they are. Every primitive here takes look=:
  "flat"  — plain fills (every video before 2026-10-12)
  "lit"   — soft studio light from the top-left: body gradient, ambient occlusion at the edges, a bright top rim
            (light catching the material), a sheen, a cast shadow that grows with the object; grain on the frame.
  "paper" — cut paper: flat color, fibre texture, a short stacked shadow (layers lying on each other), a paper ground,
            parts placed a touch off-square by hand.
Volume comes from light only — no extrusion (STYLE §4). Every function is pure (frame = f(t)); textures are seeded
and cached, never re-rolled per frame.

    body(c, look, rrect_path(x, y, w, h, r), (x, y, w, h), color)          # any shape: pass a path builder
    cable(c, look, pts, 14, color)                                          # tubes: cables, pipes, poles seen side-on
    stage(c, look, color) · rain(c, t, look, box) · finish(c, look)         # ground, weather, grain + vignette
"""
import math
from functools import lru_cache

import cairo
import numpy as np

from .. import tokens as tk
from ..draw import _rrect_path, array_to_surface, gaussian
from ..ease import clamp, mix

LOOKS = ("flat", "lit", "paper")
WHITE = (1, 1, 1, 1)
BLACK = (0, 0, 0, 1)


def tone(color, k):
    """k > 0 lightens toward white, k < 0 darkens toward black (alpha kept)."""
    tgt = (1.0, 1.0, 1.0) if k > 0 else (0.0, 0.0, 0.0)
    a = clamp(abs(k))
    return tuple(c + (g - c) * a for c, g in zip(color[:3], tgt)) + (color[3] if len(color) > 3 else 1.0,)


def tilt(look, seed=0):
    """Hand-placed rotation (radians) for a part in the paper look; 0 otherwise. Same seed → same angle."""
    if look != "paper":
        return 0.0
    v = math.sin(seed * 12.9898 + 4.1) * 43758.5453
    return (2 * (v - math.floor(v)) - 1) * tk.LOOK["paper"]["tilt"]


# ── path builders (callables that add a path to a cairo context) ────────
def rrect_path(x, y, w, h, r):
    """Rounded rect path builder."""
    return lambda ctx: _rrect_path(ctx, x, y, w, h, r)


def poly_path(pts):
    """Closed polygon path builder."""
    def p(ctx):
        ctx.move_to(*pts[0])
        for q in pts[1:]:
            ctx.line_to(*q)
        ctx.close_path()
    return p


def circle_path(cx, cy, r):
    """Circle path builder."""
    def p(ctx):
        ctx.new_sub_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
    return p


def drop_path(cx, cy, s, stretch=0.0):
    """Water-drop outline (same geometry as hujan.tetes): height s, round belly centred on (cx, cy)."""
    r = s * 0.34
    tip = cy - s * (0.62 + 0.45 * stretch)

    def p(ctx):
        ctx.move_to(cx, tip)
        ctx.curve_to(cx + r * 0.25, tip + s * 0.25, cx + r, cy - r * 0.55, cx + r, cy)
        ctx.arc(cx, cy, r, 0, math.pi)
        ctx.curve_to(cx - r, cy - r * 0.55, cx - r * 0.25, tip + s * 0.25, cx, tip)
        ctx.close_path()
    return p


def drop_box(cx, cy, s, stretch=0.0):
    """Bounding box of drop_path."""
    r = s * 0.34
    tip = cy - s * (0.62 + 0.45 * stretch)
    return (cx - r, tip, 2 * r, cy + r - tip)


# ── textures (seeded, cached) ───────────────────────────────────────────
@lru_cache(maxsize=8)
def _noise_tile(size, blur, seed):
    """Grey noise tile (size × size, repeats) around mid-grey; blur > 0 = paper fibre, 0 = film grain."""
    rng = np.random.default_rng(seed)
    n = rng.random((size, size), dtype=np.float32)
    if blur > 0:
        a = np.repeat((n * 255).astype(np.uint8)[:, :, None], 4, axis=2)
        n = gaussian(a, blur)[:, :, 0].astype(np.float32) / 255
        n = (n - n.mean()) / (n.std() + 1e-6) * 0.18 + 0.5          # restore contrast after the blur
        streak = rng.random((size, 1), dtype=np.float32)                # long horizontal fibres
        n = np.clip(n + (np.repeat(streak, size, axis=1) - 0.5) * 0.08, 0, 1)
    g = (n * 255).astype(np.uint8)
    arr = np.empty((size, size, 4), np.uint8)
    arr[..., 0] = arr[..., 1] = arr[..., 2] = g
    arr[..., 3] = 255
    return array_to_surface(arr)


def _texture(c, kind, alpha, anchor=(0.0, 0.0)):
    """Paint a repeating texture over the current clip with soft light. kind: 'grain' (screen-anchored film grain)
    or 'fibre' (paper fibre, anchored to the object so it moves with it)."""
    if alpha <= 0.002:
        return
    ctx = c.ctx
    ctx.save()
    if kind == "grain":
        tile = _noise_tile(256, 0, 7)
        ctx.identity_matrix()                       # one grain per device pixel, whatever the scale/camera
        ctx.set_source_surface(tile, 0, 0)
    else:
        tile = _noise_tile(384, 1.2, 11)
        ctx.translate(*anchor)
        ctx.set_source_surface(tile, 0, 0)
    ctx.get_source().set_extend(cairo.EXTEND_REPEAT)
    ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT)
    ctx.paint_with_alpha(alpha)
    ctx.restore()


# ── the body: one shape in the look's material ──────────────────────────
def body(c, look, path, bbox, color, alpha=1.0, form="box", r=None, lift=1.0, shadow=True):
    """Fill a shape in the look's material. path(ctx) builds the shape (rrect_path, poly_path, circle_path,
    drop_path); bbox = its bounds (x, y, w, h), which size the light and the shadow.
    form: "box" (light from the top-left) · "cyl" (pole / tube standing up: a light band down its left third)
          · "drop" (clear liquid: light core, dark rim, specular dot).
    r = corner radius of the cast shadow (default min side / 8); lift = shadow distance (0 = lying flat on the
    surface below, 1 = standing off it); shadow=False for parts that sit inside another body.
    Bigger objects get a deeper, softer shadow (apple-design: bigger surfaces read thicker)."""
    if alpha <= 0.002:
        return
    x, y, w, h = bbox
    ctx = c.ctx
    if look == "flat":
        ctx.new_path()
        path(ctx)
        c.src(color, alpha)
        ctx.fill()
        return
    r = min(w, h) / 8 if r is None else r
    k = clamp(max(w, h) / 600, 0.25, 1.8)                         # size factor: 600 px = token values
    if look == "paper":
        P = tk.LOOK["paper"]
        if shadow and lift > 0:
            c.shadow(x, y, w, h, r, P["soft_blur"] * k, P["soft_dy"] * k * lift, P["soft_alpha"] * alpha)
            ctx.save()
            ctx.translate(0, P["stack_dy"] * clamp(k, 0.5, 1.4) * lift)
            ctx.new_path()
            path(ctx)
            c.src(tk.C["brand_ink"], P["stack_alpha"] * alpha)
            ctx.fill()
            ctx.restore()
        ctx.save()
        ctx.new_path()
        path(ctx)
        c.src(color, alpha)
        ctx.fill_preserve()
        ctx.clip()
        _texture(c, "fibre", P["fibre"] * alpha, (x, y))
        _rim(c, path, bbox, P["edge"] * alpha, 2.0)              # the cut edge catching light
        ctx.restore()
        return

    P = tk.LOOK["lit"]
    if shadow and lift > 0:
        sh_r = min(w, h) / 2 if form in ("drop", "cyl") else r
        c.shadow(x + 4 * k * lift, y, w, h, sh_r, P["shadow_blur"] * k, P["shadow_dy"] * k * lift,
                 P["shadow_alpha"] * alpha)
        c.shadow(x, y, w, h, sh_r, 6 * k, 4 * k, P["contact_alpha"] * alpha)
    ctx.save()
    ctx.new_path()
    path(ctx)
    ctx.clip_preserve()
    if form == "cyl":
        g = cairo.LinearGradient(x, 0, x + w, 0)
        for o, kk in ((0.0, -P["lo"] * 0.8), (0.28, P["hi"]), (0.55, 0.0), (1.0, -P["lo"])):
            g.add_color_stop_rgba(o, *tone(color, kk)[:3], alpha)
    elif form == "drop":
        g = cairo.RadialGradient(x + w * 0.42, y + h * 0.62, 0, x + w * 0.5, y + h * 0.6, max(w, h) * 0.62)
        g.add_color_stop_rgba(0.0, *tone(color, 0.35)[:3], 0.72 * alpha)
        g.add_color_stop_rgba(0.65, *color[:3], 0.86 * alpha)
        g.add_color_stop_rgba(1.0, *tone(color, -0.4)[:3], 0.96 * alpha)
    else:
        g = cairo.LinearGradient(x, y, x + w * 0.35, y + h)
        g.add_color_stop_rgba(0.0, *tone(color, P["hi"])[:3], alpha)
        g.add_color_stop_rgba(0.55, *color[:3], alpha)
        g.add_color_stop_rgba(1.0, *tone(color, -P["lo"])[:3], alpha)
    ctx.set_source(g)
    ctx.fill()
    if form == "box":                                             # ambient occlusion: edges a touch darker
        ctx.save()
        ctx.translate(x + w / 2, y + h / 2)
        ctx.scale(max(1.0, w / 2), max(1.0, h / 2))
        g = cairo.RadialGradient(0, 0, 0.55, 0, 0, 1.2)
        g.add_color_stop_rgba(0, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0, 0, 0, P["ao"] * alpha)
        ctx.set_source(g)
        ctx.paint()
        ctx.restore()
        g = cairo.LinearGradient(x, y, x + w, y + h)              # sheen band
        g.add_color_stop_rgba(0.0, 1, 1, 1, 0)
        g.add_color_stop_rgba(0.18, 1, 1, 1, P["sheen"] * alpha)
        g.add_color_stop_rgba(0.36, 1, 1, 1, 0)
        ctx.set_source(g)
        ctx.paint()
        _rim(c, path, bbox, P["rim"] * alpha, P["rim_w"] * clamp(k, 0.6, 1.5))
    elif form == "drop":                                          # specular highlight + a small hot dot
        c.circle(x + w * 0.33, y + h * 0.56, w * 0.13, WHITE, 0.55 * alpha)
        c.circle(x + w * 0.3, y + h * 0.5, w * 0.05, WHITE, 0.9 * alpha)
        _rim(c, path, bbox, 0.35 * alpha, 2.0)
    ctx.restore()


def _rim(c, path, bbox, alpha, width):
    """Bright top edge (inside the current clip): the path stroked white, fading out down the first third."""
    if alpha <= 0.002:
        return
    x, y, w, h = bbox
    ctx = c.ctx
    g = cairo.LinearGradient(0, y, 0, y + min(h * 0.35, 120))
    g.add_color_stop_rgba(0, 1, 1, 1, alpha)
    g.add_color_stop_rgba(1, 1, 1, 1, 0)
    ctx.new_path()
    path(ctx)
    ctx.set_source(g)
    ctx.set_line_width(width * 2)
    ctx.stroke()


def inset(c, look, path, bbox, alpha=1.0):
    """Recess (a window cut into a body, a tray): darker toward its top-left edge, as if the rim shades it.
    Draw it over the recess fill. flat: nothing."""
    if look == "flat" or alpha <= 0.002:
        return
    x, y, w, h = bbox
    ctx = c.ctx
    a = (0.22 if look == "lit" else 0.14) * alpha
    d = min(w, h) * 0.16
    ctx.save()
    ctx.new_path()
    path(ctx)
    ctx.clip()
    for g in (cairo.LinearGradient(0, y, 0, y + d), cairo.LinearGradient(x, 0, x + d * 0.7, 0)):
        g.add_color_stop_rgba(0, 0, 0, 0, a)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g)
        ctx.paint()
    ctx.restore()


def caustic(c, look, cx, y, w, color, alpha=1.0):
    """Light focused through a drop onto the surface under it (lit only): a soft bright ellipse in the drop's color."""
    if look != "lit" or alpha <= 0.002:
        return
    ctx = c.ctx
    ctx.save()
    ctx.translate(cx, y)
    ctx.scale(w * 0.6, w * 0.18)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
    g.add_color_stop_rgba(0, *tone(color, 0.6)[:3], 0.55 * alpha)
    g.add_color_stop_rgba(1, *color[:3], 0)
    ctx.set_source(g)
    ctx.paint()
    ctx.restore()


def spill(c, look, cx, cy, r, color, amount=1.0):
    """Light of a glowing part falling on what's around it (lit: soft; paper: a flat pale disc; flat: nothing).
    Subtle by design — this is light, not a neon glow (STYLE §4)."""
    if look == "flat" or amount <= 0.002:
        return
    ctx = c.ctx
    if look == "paper":
        c.circle(cx, cy, r * 0.55, tone(color, 0.55), 0.5 * amount)
        return
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, r)
    g.add_color_stop_rgba(0, *tone(color, 0.3)[:3], tk.LOOK["lit"]["spill"] * amount)
    g.add_color_stop_rgba(1, *color[:3], 0)
    ctx.save()
    ctx.set_source(g)
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()


# ── tubes: cables, pipes ────────────────────────────────────────────────
def _stroke(c, pts, color, width, alpha, dx=0.0, dy=0.0):
    ctx = c.ctx
    ctx.new_path()
    ctx.move_to(pts[0][0] + dx, pts[0][1] + dy)
    for p in pts[1:]:
        ctx.line_to(p[0] + dx, p[1] + dy)
    c.src(color, alpha)
    ctx.set_line_width(width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()


def cable(c, look, pts, width, color, alpha=1.0, shadow=True):
    """A round cable along polyline pts. lit: shadow on the surface behind, dark edge, body, a highlight line
    along its upper-left side; paper: a paper strip with its short stacked shadow; flat: one stroke."""
    if alpha <= 0.002 or len(pts) < 2:
        return
    if look == "flat":
        _stroke(c, pts, color, width, alpha)
        return
    if look == "paper":
        if shadow:
            _stroke(c, pts, tk.C["brand_ink"], width, tk.LOOK["paper"]["stack_alpha"] * alpha, 0, width * 0.45)
        _stroke(c, pts, color, width, alpha)
        _stroke(c, pts, WHITE, max(1.5, width * 0.12), 0.35 * alpha, -width * 0.12, -width * 0.3)
        return
    if shadow:
        _stroke(c, pts, BLACK, width * 1.25, 0.07 * alpha, width * 0.5, width * 1.1)
        _stroke(c, pts, BLACK, width * 1.05, 0.10 * alpha, width * 0.25, width * 0.55)
    _stroke(c, pts, tone(color, -0.35), width, alpha)
    _stroke(c, pts, color, width * 0.72, alpha, -width * 0.04, -width * 0.06)
    _stroke(c, pts, WHITE, max(1.5, width * 0.18), 0.45 * alpha, -width * 0.16, -width * 0.24)


# ── the frame: ground, weather, finish ──────────────────────────────────
def stage(c, look, color, alpha=1.0, horizon=0.66):
    """Full-frame ground for a look, tinted by the video's signature color. lit: a studio sweep (light from the
    top-left, a floor below `horizon`); paper: a paper ground with fibre. Use as (part of) Video.stage."""
    if alpha <= 0.002 or look == "flat":
        return
    W, H = tk.W, tk.H
    ctx = c.ctx
    ctx.save()
    ctx.push_group()
    if look == "lit":
        top = tone(mix(tk.C["bg"], color, 0.08), 0.35)
        mid = mix(tk.C["bg"], color, 0.12)
        floor = mix(tk.C["studio_floor"], color, 0.10)
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgba(0, *top[:3], 1)
        g.add_color_stop_rgba(horizon - 0.08, *mid[:3], 1)
        g.add_color_stop_rgba(horizon + 0.06, *floor[:3], 1)
        g.add_color_stop_rgba(1, *tone(floor, -0.06)[:3], 1)
        ctx.set_source(g)
        ctx.paint()
        g = cairo.RadialGradient(W * 0.15, H * 0.12, 0, W * 0.15, H * 0.12, H * 0.75)   # key light
        g.add_color_stop_rgba(0, 1, 1, 1, 0.65)
        g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.set_source(g)
        ctx.paint()
    else:
        c.src(mix(tk.C["paper_ground"], color, 0.06))
        ctx.paint()
        _texture(c, "fibre", tk.LOOK["paper"]["fibre"] * 1.4)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(alpha)
    ctx.restore()


def rain(c, t, look, box, color, density=1.0, n=70, speed=1500, length=70, slant=0.16, seed=3, alpha=1.0):
    """Background rain in a look (pure function of t). lit: out-of-focus streaks (a wide faint stroke + a thin
    core = shallow depth of field) and a few soft bokeh drops close to the lens; paper: short paper strips with
    their stacked shadow, falling slower; flat: hujan()-style streaks."""
    if density <= 0.001 or alpha <= 0.001:
        return
    x, y, w, h = box
    span = h + length * 2

    def hsh(i, k):
        v = math.sin(i * 12.9898 + k * 78.233 + seed * 37.719) * 43758.5453
        return v - math.floor(v)

    sp_k = 0.45 if look == "paper" else 1.0
    with c.clip(x, y, w, h):
        for i in range(n):
            a = clamp((density - hsh(i, 4)) * 8) * (0.35 + 0.35 * hsh(i, 3)) * alpha
            if a <= 0.01:
                continue
            depth = hsh(i, 5)                                       # 0 far … 1 near
            sp = speed * sp_k * (0.7 + 0.6 * depth)
            ln = length * (0.6 + 0.8 * depth)
            yy = y - ln + (hsh(i, 1) * span + t * sp) % span
            xx = x - slant * h + hsh(i, 0) * (w + slant * h) + slant * (yy - y)
            seg = [(xx, yy), (xx - slant * ln, yy - ln)]
            if look == "lit":
                _stroke(c, seg, color, 3 + 9 * depth, a * 0.18)
                _stroke(c, seg, tone(color, 0.5), 1.5 + 1.5 * (1 - depth), a * 0.55 * (1 - 0.6 * depth))
            elif look == "paper":
                seg = [(xx, yy), (xx - slant * ln * 0.5, yy - ln * 0.5)]
                _stroke(c, seg, tk.C["brand_ink"], 6, a * 0.12, 0, 4)
                _stroke(c, seg, tone(color, 0.25), 6, a * 0.9)
            else:
                _stroke(c, seg, color, 3, a)
        if look == "lit":                                            # bokeh: big soft drops near the lens
            for i in range(5):
                bx = x + w * hsh(i, 8)
                by = y + (h * hsh(i, 9) + t * 22 * (1 + hsh(i, 6))) % h
                br = 40 + 50 * hsh(i, 7)
                g = cairo.RadialGradient(bx, by, br * 0.6, bx, by, br)
                g.add_color_stop_rgba(0, *tone(color, 0.6)[:3], 0.10 * density * alpha)
                g.add_color_stop_rgba(1, *tone(color, 0.6)[:3], 0)
                c.ctx.set_source(g)
                c.ctx.arc(bx, by, br, 0, 2 * math.pi)
                c.ctx.fill()


def finish(c, look, alpha=1.0):
    """Frame finish for a look (use in Video.finish): static film grain + a soft vignette. flat: nothing."""
    if look == "flat" or alpha <= 0.002:
        return
    P = tk.LOOK[look]
    W, H = tk.W, tk.H
    ctx = c.ctx
    g = cairo.RadialGradient(W / 2, H * 0.45, H * 0.35, W / 2, H * 0.45, H * 0.8)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, P["vignette"] * alpha)
    ctx.save()
    ctx.set_source(g)
    ctx.paint()
    ctx.restore()
    ctx.save()
    ctx.rectangle(0, 0, W, H)
    ctx.clip()
    _texture(c, "grain", P["grain"] * alpha)
    ctx.restore()
