"""Craft v2 (2026-10-12, STYLE §3) — the motion-designer moves the engine was missing, distilled from the
HyperFrames animation skills (GSAP DrawSVG / SplitText / MorphSVG / MotionPath, seam doctrine) and Remotion's
markup rules. All pure frame = f(t), all on the Apple grammar (one leader, real curves, quiet exits).

Paths are plain point lists [(x, y), …] (polylines). Build them with `pts_bezier`, `pts_circle`, `pts_rrect`,
`pts_poly`, or flatten any cairo path with `pts_cairo(c, build)`. Proof sheet: `videos/_lab/craft-lab`.
"""
import math

from .. import tokens as tk
from ..ease import clamp, lerp, prog, curve, ios_spring
from .motion import fmt_id, bezier_point


# ── paths as point lists ─────────────────────────────────────────────────────────────────────────────────────────
def pts_poly(pts, closed=False):
    """A polyline (optionally closed: the first point is appended at the end)."""
    pts = [tuple(p) for p in pts]
    return pts + [pts[0]] if closed and pts[0] != pts[-1] else pts


def pts_bezier(p0, p1, p2, p3, n=48):
    """Cubic bezier as n + 1 points."""
    return [bezier_point(p0, p1, p2, p3, i / n) for i in range(n + 1)]


def pts_circle(cx, cy, r, n=96, start=-math.pi / 2, sweep=2 * math.pi):
    """Circle / arc as points, starting at 12 o'clock and going clockwise (rings start at 12, HyperFrames rule)."""
    return [(cx + r * math.cos(start + sweep * i / n), cy + r * math.sin(start + sweep * i / n)) for i in range(n + 1)]


def pts_rrect(x, y, w, h, r, n_corner=10):
    """Rounded rect outline, clockwise from the top-left straight edge, closed."""
    r = min(r, w / 2, h / 2)
    out = []
    for cx, cy, a0 in ((x + w - r, y + r, -math.pi / 2), (x + w - r, y + h - r, 0.0),
                       (x + r, y + h - r, math.pi / 2), (x + r, y + r, math.pi)):
        for i in range(n_corner + 1):
            a = a0 + (math.pi / 2) * i / n_corner
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out + [out[0]]


def pts_cairo(c, build, tolerance=0.5):
    """Flatten any cairo path: build(ctx) draws it (move_to / curve_to / arc …); returns its first sub-path's points."""
    cx = c.ctx
    cx.save()
    cx.new_path()
    build(cx)
    tol = cx.get_tolerance()
    cx.set_tolerance(tolerance)
    flat = cx.copy_path_flat()
    cx.set_tolerance(tol)
    cx.new_path()
    cx.restore()
    out, start = [], None
    for kind, pt in flat:
        if kind == 0:          # MOVE_TO
            if out:
                break
            start = pt
            out.append(pt)
        elif kind == 1:        # LINE_TO
            out.append(pt)
        elif kind == 3 and start:   # CLOSE_PATH
            out.append(start)
    return out


def _cum(pts):
    d = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d.append(d[-1] + math.hypot(x1 - x0, y1 - y0))
    return d


def path_len(pts):
    return _cum(pts)[-1]


def trim(pts, p0, p1=None):
    """Sub-polyline between arc-length fractions p0 and p1 (one argument = from the start to p0)."""
    if p1 is None:
        p0, p1 = 0.0, p0
    p0, p1 = clamp(p0), clamp(p1)
    if p1 <= p0 or len(pts) < 2:
        return []
    d = _cum(pts)
    L = d[-1] or 1.0
    a, b = p0 * L, p1 * L

    def at(s):
        for i in range(1, len(d)):
            if d[i] >= s:
                k = (s - d[i - 1]) / max(1e-9, d[i] - d[i - 1])
                return (lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k)), i
        return pts[-1], len(pts) - 1
    pa, ia = at(a)
    pb, ib = at(b)
    return [pa] + list(pts[ia:ib]) + [pb]


def path_point(pts, u, smooth=1):
    """(x, y, heading) at arc-length fraction u. Heading = tangent angle, low-passed over ±smooth samples so it
    doesn't snap at corners."""
    seg = trim(pts, 0.0, clamp(u))
    if not seg:
        x, y = pts[0]
    else:
        x, y = seg[-1]
    d = _cum(pts)
    L = d[-1] or 1.0
    s = clamp(u) * L
    i = next((k for k in range(1, len(d)) if d[k] >= s), len(d) - 1)
    lo, hi = max(1, i - smooth), min(len(pts) - 1, i + smooth)
    dx = pts[hi][0] - pts[lo - 1][0]
    dy = pts[hi][1] - pts[lo - 1][1]
    return x, y, math.atan2(dy, dx)


def _poly(c, pts):
    cx = c.ctx
    cx.new_path()
    cx.move_to(*pts[0])
    for p in pts[1:]:
        cx.line_to(*p)


def stroke_partial(c, pts, p, color, width=4.0, alpha=1.0, p0=0.0, cap="round"):
    """Stroke the first p (or p0..p) of a polyline by arc length — exact, round caps hidden at p ≈ 0."""
    import cairo
    seg = trim(pts, p0, p)
    if len(seg) < 2 or alpha <= 0.002 or path_len(seg) < 0.5:
        return
    _poly(c, seg)
    cx = c.ctx
    c.src(color, alpha)
    cx.set_line_width(width)
    cx.set_line_cap({"round": cairo.LineCap.ROUND, "butt": cairo.LineCap.BUTT}[cap])
    cx.set_line_join(cairo.LineJoin.ROUND)
    cx.stroke()


# ── 1 · draw_on: a pen traces the path, then the fill / label follows ────────────────────────────────────────────
def draw_on(c, t, t0, pts, color, width=4.0, dur=None, t_out=None, fill=None, fill_alpha=1.0, alpha=1.0):
    """Stroke draw-on (DrawSVG): 0 → full length on the 'draw' curve (power2.out) in dur (tk.M['draw_in']); a fill
    (closed paths) fades in over draw_fill after the stroke lands. Exit = quiet fade. Endpoints must sit on real
    elements — a line drawn into empty space is filler. Chain segments with draw_chain(t0, durs)."""
    M = tk.M
    dur = M["draw_in"] if dur is None else dur
    p = curve("draw")(prog(t, t0, dur))
    if p <= 0.0005:
        return
    b = 0.0 if t_out is None else curve("apple_in")(prog(t, t_out, M["quiet_out"]))
    a = alpha * (1 - b)
    if a <= 0.002:
        return
    if fill is not None:
        f = curve("apple_out")(prog(t, t0 + dur, M["draw_fill"]))
        if f > 0.002:
            _poly(c, pts)
            c.src(fill, fill_alpha * f * a)
            c.ctx.fill()
    stroke_partial(c, pts, p, color, width, a)


def draw_chain(t0, durs, chain=None):
    """Start times of chained draw_on segments: each starts at draw_chain (75 %) of the previous one's duration."""
    k = tk.M["draw_chain"] if chain is None else chain
    out, s = [], t0
    for d in durs:
        out.append(s)
        s += d * k
    return out


def mark(c, t, t0, kind, bbox, color, width=5.0, dur=None, t_out=None, seed=0, alpha=1.0):
    """Hand-drawn annotation that draws itself (Remotion annotations): kind = underline · circle · box · strike ·
    bracket. Deliberate imperfection (IDENTITY.md): a seeded wobble, the circle overshoots its start a little."""
    x, y, w, h = bbox
    rnd = lambda k: math.sin(seed * 12.9898 + k * 78.233) * 0.5      # deterministic −0.5..0.5
    if kind == "underline":
        y0 = y + h + 10
        pts = pts_bezier((x - 6, y0 + 4 * rnd(1)), (x + w * 0.3, y0 + 6 + 4 * rnd(2)),
                         (x + w * 0.7, y0 - 4 + 4 * rnd(3)), (x + w + 8, y0 + 2 * rnd(4)), 40)
    elif kind == "strike":
        ym = y + h * 0.55
        pts = pts_bezier((x - 8, ym + 6 * rnd(1)), (x + w * 0.35, ym - 4), (x + w * 0.65, ym + 4),
                         (x + w + 8, ym - 6 * rnd(2)), 40)
    elif kind == "circle":
        cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2 + 26, h / 2 + 22
        n, sweep = 120, 2 * math.pi * 1.08
        pts = [(cx + rx * (1 + 0.03 * rnd(i // 30)) * math.cos(-2.2 + sweep * i / n),
                cy + ry * (1 + 0.04 * rnd(i // 30 + 9)) * math.sin(-2.2 + sweep * i / n)) for i in range(n + 1)]
    elif kind == "bracket":
        bx = x - 22
        pts = [(bx + 14, y - 6), (bx, y - 6), (bx, y + h + 6), (bx + 14, y + h + 6)]
    else:  # box
        pts = pts_rrect(x - 16, y - 12, w + 32, h + 24, 14)
    draw_on(c, t, t0, pts, color, width, dur, t_out, alpha=alpha)


# ── 2 · split_rise: type rises from behind its own line mask, per line / word / char ──────────────────────────────
def _order(n, order, seed):
    if order == "end":
        return [n - 1 - i for i in range(n)]
    if order == "center":
        mid = (n - 1) / 2
        return [abs(i - mid) for i in range(n)]
    if order == "edges":
        mid = (n - 1) / 2
        return [mid - abs(i - mid) for i in range(n)]
    if order == "random":
        return [((i * 2654435761 + seed * 40503) % 1000) / 1000 * (n - 1) for i in range(n)]
    return list(range(n))


def split_rise(c, t, t_in, t_out, x, y, text, font, size, color, by="line", order="start", accent=None,
               each=None, gap=None, dy=None, ls=0.0, line_h=1.0, exit="quiet", seed=0, alpha=1.0):
    """SplitText-style masked reveal. text may have several lines (\\n) and *accent* words (drawn in `accent`).
    by: line (0.65 s, +0.10 s per line) · word (0.45 s, +0.07) · char (0.35 s, +0.025 — punch lines only).
    order: start · end · center · edges · random (seeded). Whole stagger ≤ split_cap (0.5 s). Each piece rises
    0.9 × size from behind a mask padded 0.2 em; opacity leads. exit: quiet (fade + .98) or 'mask' (reverse, up).
    y = first baseline. Returns the block height."""
    M = tk.M
    each = M[f"split_{by}"] if each is None else each
    gap = M[f"split_{by}_gap"] if gap is None else gap
    dy = size * 0.9 if dy is None else dy
    lines = text.split("\n")
    lh = size * line_h
    # pieces: (line index, x offset, string, is_accent)
    pieces = []
    for li, ln in enumerate(lines):
        words = ln.split(" ")
        if by == "line":
            pieces.append((li, 0.0, ln, None))
            continue
        cur = 0.0
        for wi, wd in enumerate(words):
            acc = wd.startswith("*") and wd.rstrip(".,!?:;").endswith("*")
            clean = wd.replace("*", "")
            prefix = " ".join(w.replace("*", "") for w in words[:wi]) + (" " if wi else "")
            cur = c.measure(prefix, font, size, ls)[0] if wi else 0.0
            if by == "word":
                pieces.append((li, cur, clean, acc))
            else:
                for ci, ch in enumerate(clean):
                    off = c.measure(prefix + clean[:ci], font, size, ls)[0] if (prefix or ci) else 0.0
                    pieces.append((li, off, ch, acc))
    n = len(pieces)
    rank = _order(n, order, seed)
    top = max(rank) if rank else 0
    step = gap if top * gap <= M["split_cap"] or top == 0 else M["split_cap"] / top
    b = 0.0
    if t_out is not None:
        b = curve("apple_in")(prog(t, t_out, M["quiet_out"] if exit == "quiet" else each * 0.6))
    if b >= 1:
        return len(lines) * lh
    for (li, off, s, acc), r in zip(pieces, rank):
        ti = t_in + r * step
        mv = ios_spring(t - ti, *tk.IOS["smooth"]) if t > ti else 0.0
        op = curve("apple_out")(prog(t, ti, each * M["op_lead"] * 1.6))
        if op <= 0.002:
            continue
        base = y + li * lh
        col = accent if (acc and accent is not None) else color
        yy = base + dy * (1 - mv)
        a = alpha * op
        if exit == "quiet":
            a *= 1 - b
        else:
            yy -= b * dy
        with c.clip(x - size * 0.3, base - size * 1.0, 3000, size * 1.3):
            if by == "line" and "*" in s:
                _accent_line(c, x, yy, s, font, size, color, accent or color, a, ls)
            else:
                c.text(x + off, yy, s, font, size, col, a, ls)
    return len(lines) * lh


def _accent_line(c, x, y, s, font, size, color, accent, a, ls):
    parts = s.split("*")
    cur = x
    for i, part in enumerate(parts):
        if part:
            cur += c.text(cur, y, part, font, size, accent if i % 2 else color, a, ls)


# ── 3 · count_up: tabular digits, the number grows with its count ────────────────────────────────────────────────
def count_up(c, t, t0, x, y, v0, v1, font, size, color, dur=None, decimals=0, suffix="", suffix_font=None,
             suffix_color=None, scale_from=None, align="l", t_out=None, alpha=1.0):
    """Count v0 → v1 on apple_out in dur (1.2–2.5 s, tk.M['count_dur']) with tabular figures (no jitter as digit
    widths change), Indonesian format (fmt_id), rounded. The number scales scale_from → 1 on the SAME curve, anchored
    at its baseline (x by align). The suffix slides in after the count lands. No overshoot — it's data.
    Several stats in one frame share t0 + dur (a chord)."""
    M = tk.M
    dur = M["count_dur"] if dur is None else dur
    s0 = M["count_scale"] if scale_from is None else scale_from
    p = curve("apple_out")(prog(t, t0, dur))
    op = curve("apple_out")(prog(t, t0, 0.3))
    if t_out is not None:
        op *= 1 - curve("apple_in")(prog(t, t_out, M["quiet_out"]))
    if op <= 0.002:
        return
    v = lerp(v0, v1, p)
    v = round(v, decimals) if decimals else round(v)
    txt = f'<span font_features="tnum">{fmt_id(v, decimals)}</span>'
    w_full = c.measure(f'<span font_features="tnum">{fmt_id(v1, decimals)}</span>', font, size, markup=True)[0]
    ox = {"l": x, "c": x - w_full / 2, "r": x - w_full}[align]
    sc = lerp(s0, 1.0, p)
    with c.at(0, 0, sc, origin=(ox, y)):
        c.text(ox, y, txt, font, size, color, alpha * op, markup=True)
    if suffix:
        sp = curve("apple_out")(prog(t, t0 + dur * 0.85, 0.4))
        if sp > 0.002:
            sf = suffix_font or tk.F["serif"]
            c.text(ox + w_full * sc + size * 0.08, y + 20 * (1 - sp), suffix, sf, size * 0.55,
                   suffix_color or color, alpha * op * sp)


# ── 4 · morph_path: one shape becomes another ────────────────────────────────────────────────────────────────────
def resample(pts, n=128):
    """n points evenly spaced by arc length (closed shapes: pass a closed point list)."""
    d = _cum(pts)
    L = d[-1] or 1.0
    out, j = [], 1
    for i in range(n):
        s = L * i / n
        while j < len(d) - 1 and d[j] < s:
            j += 1
        k = (s - d[j - 1]) / max(1e-9, d[j] - d[j - 1])
        out.append((lerp(pts[j - 1][0], pts[j][0], k), lerp(pts[j - 1][1], pts[j][1], k)))
    return out


def _area(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p))) / 2


_MORPH = {}


def morph_pair(a, b, n=128):
    """(A, B) resampled to n points, same winding, B rotated so Σ|aᵢ − bᵢ|² is smallest (no twisting). Cached."""
    key = (tuple(a), tuple(b), n)
    if key in _MORPH:
        return _MORPH[key]
    A, B = resample(a, n), resample(b, n)
    if (_area(A) > 0) != (_area(B) > 0):
        B = B[::-1]
    best, bk = None, 0
    for k in range(0, n, 2):
        s = sum((A[i][0] - B[(i + k) % n][0]) ** 2 + (A[i][1] - B[(i + k) % n][1]) ** 2 for i in range(0, n, 4))
        if best is None or s < best:
            best, bk = s, k
    B = B[bk:] + B[:bk]
    _MORPH[key] = (A, B)
    return A, B


def morph_path(c, t, t0, a, b, color, dur=None, n=128, alpha=1.0, draw=None):
    """Shape morph A → B (MorphSVG) on apple_in_out in dur (0.6–1.2 s, tk.M['morph_dur']). a / b = closed point
    lists. Default: fills the shape in color; draw(c, pts, p) to shade it yourself (e.g. material.body via a path).
    Hold shape A 0.6–1.5 s first. Returns the current points."""
    dur = tk.M["morph_dur"] if dur is None else dur
    A, B = morph_pair(a, b, n)
    p = curve("apple_in_out")(prog(t, t0, dur))
    pts = [(lerp(pa[0], pb[0], p), lerp(pa[1], pb[1], p)) for pa, pb in zip(A, B)]
    if draw:
        draw(c, pts, p)
    elif alpha > 0.002:
        _poly(c, pts)
        c.ctx.close_path()
        c.src(color, alpha)
        c.ctx.fill()
    return pts


# ── 5 · path_at: travel along a path (MotionPath) ────────────────────────────────────────────────────────────────
def path_at(c, t, t0, dur, pts, draw, rotate=False, ease="apple_in_out", trail=None, trail_color=None, width=4.0):
    """Move draw(c) (drawn around 0, 0) along pts by arc length in dur. rotate=True only for things with a nose
    (packet, kurir, shuttle). trail = draw the travelled part of the path as a stroke behind it."""
    u = curve(ease)(prog(t, t0, dur))
    if trail:
        stroke_partial(c, pts, u, trail_color or tk.C["line"], width)
    x, y, ang = path_point(pts, u)
    with c.at(x, y, 1.0, origin=(0, 0), rot=ang if rotate else 0.0):
        draw(c)
    return x, y, ang


# ── 6 · shutter: real sub-frame motion blur for fast moves ───────────────────────────────────────────────────────
def shutter(c, t, draw_at, speed=None, angle=None, n=None, sharp=True, gate=None, fps=60):
    """Shutter-accumulation motion blur (Remotion CameraMotionBlur): draw_at(c, tt) n times across a 180° shutter
    (1/120 s at 60 fps) centred on t, averaged. Only when speed (px/s) ≥ gate (300): below it, draws sharp once.
    Never on text that must be read at that moment; 1–3 blurred beats per video."""
    M = tk.M
    angle = M["shutter_angle"] if angle is None else angle
    n = M["shutter_n"] if n is None else n
    gate = M["shutter_gate"] if gate is None else gate
    if speed is not None and speed < gate:
        draw_at(c, t)
        return
    win = angle / 360 / fps
    cx = c.ctx
    cx.push_group()
    for k in range(n):
        tt = t + (k / (n - 1) - 0.5) * win
        cx.push_group()
        draw_at(c, tt)
        cx.pop_group_to_source()
        cx.paint_with_alpha(1 / n)
    cx.pop_group_to_source()
    cx.paint_with_alpha(0.6 if sharp else 1.0)
    if sharp:
        cx.push_group()
        draw_at(c, t)
        cx.pop_group_to_source()
        cx.paint_with_alpha(0.4)


# ── 7 · seams: carry (velocity-matched) and rack_cut (the one visible cut) ───────────────────────────────────────
def carry(c, t, t_cut, bbox, old, new, axis="y", direction=-1, travel=None, blur=0.0):
    """Cut-the-curve seam: old accelerates out along ONE direction (apple_in, carry_out 0.3 s), the cut lands
    mid-motion, new continues the same way and decelerates (apple_out, carry_in 0.42 s, starts at opacity .35).
    Zero overlap — one side per frame. Keep one direction per video (default up: direction=-1 on y).
    blur = equal peak on both sides at the cut (text ≤ 8, surfaces 12–18)."""
    M = tk.M
    travel = M["carry_travel"] if travel is None else travel
    x, y, w, h = bbox
    if t < t_cut:
        p = curve("apple_in")(prog(t, t_cut - M["carry_out"], M["carry_out"]))
        d = direction * travel * p                      # keeps going the way it was heading
        a = max(0.0, 1 - p / 0.3) if p > 0 else 1.0     # opacity gone at 30 % of the travel
        bl = blur * p
        draw = old
    else:
        p = curve("apple_out")(prog(t, t_cut, M["carry_in"]))
        d = -direction * travel * (1 - p)               # arrives from behind, same direction
        a = lerp(0.35, 1.0, clamp(p / 0.5))
        bl = blur * (1 - p)
        draw = new
    if a <= 0.002:
        return
    tx, ty = (0, d) if axis == "y" else (d, 0)
    with c.at(tx, ty):
        with c.layer((x, y, w, h), a, bl):
            draw(c)


def rack_cut(c, t, t_cut, bbox, old, new, blur=None, breathe=None):
    """Defocus cut on the SAME surface: old stays opaque while blur ramps 0 → 10 px (power2.in, 0.25 s) with a
    1 → 1.04 lens breath; hard swap at peak blur; new sharpens 10 → 0 (power2.out, ≥ 0.3 s). Max once per ~8 s,
    never during a hold or over text being read."""
    M = tk.M
    blur = M["rack_blur"] if blur is None else blur
    breathe = M["rack_breathe"] if breathe is None else breathe
    x, y, w, h = bbox
    if t < t_cut:
        p = prog(t, t_cut - M["rack_in"], M["rack_in"]) ** 2
        draw = old
    else:
        q = prog(t, t_cut, M["rack_out"])
        p = (1 - q) ** 2
        draw = new
    s = lerp(1.0, breathe, p)
    with c.at(0, 0, s, origin=(x + w / 2, y + h / 2)):
        with c.layer((x, y, w, h), 1.0, blur * p):
            draw(c)
