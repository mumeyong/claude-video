"""The brand mark from mumeyong.dev — the "mumei" (無名, nameless) emblem — and the opening brand sting.

An ensō left open at the upper right (heavy where the brush starts, thinning, breaking into a dry-brush tail) and a
blank vermilion hanko seal, tilted 4°, where a name would be signed, holding only a seed dot. Geometry ported from
the site (src/scripts/atlas/particles.ts → emblemPoints; public/favicon.svg for the seal).

    PRE_ROLL = 1.2                     # top of scenes.py: voice + all times start after the sting (opt-in)
    brand_intro(v)                     # in build(): registers the sting overlay + its SFX at t = 0
    PRE_ROLL = 2.05 ; brand_intro(v, version=2)   # new videos (2026-10-09): the long "all-out" sting, 2,45 s
    mumei_mark(c, cx, cy, r)           # the static mark anywhere (outro, cover)
"""
import math
import random

from .. import tokens as tk
from ..ease import clamp, in_cubic, in_out_sine, out_expo, prog, glide

PAPER, INK, SEAL = tk.C["brand_paper"], tk.C["brand_ink"], tk.C["brand_seal"]
STING = 1.5                                     # seconds; PRE_ROLL a bit shorter so the hook starts under the exit
STING2 = 2.45                                   # version 2 (pair with PRE_ROLL = 2.05: the voice starts under the wipe)


def _enso_points(density=8.0):
    """[(x, y, t, size)] in unit space (radius ≈ 0.86); t = 0..1 along the stroke. Port of emblemPoints()."""
    st = 0.085 / density
    rnd = random.Random(7)
    pts = []
    a0, sweep = -0.95, math.pi * 2 * 0.9
    n = round((sweep * 0.9) / st)
    for i in range(n + 1):
        t = i / n
        a = a0 + sweep * t
        r = 0.86 + 0.035 * math.sin(a * 3 + 1.2)
        w = 0.035 + 0.16 * (1 - t) ** 0.8 * min(1.0, t * 9 + 0.35)
        rows = max(1, round(w / (st * 0.85)))
        for k in range(rows):
            if t > 0.7 and rnd.random() < ((t - 0.7) / 0.3) * 0.75:   # dry brush: the tail loses bristles
                continue
            off = 0.0 if rows == 1 else (k / (rows - 1) - 0.5) * w
            jr = r + off + (rnd.random() - 0.5) * st * 0.7
            ja = a + ((rnd.random() - 0.5) * st * 0.8) / r
            pts.append((math.cos(ja) * jr, math.sin(ja) * jr, t, st))
    return pts


_ENSO = _enso_points()
# two ink flecks flicked off at the open gap (favicon.svg), unit space
_FLECKS = ((0.07, -0.95, 0.047), (0.197, -0.91, 0.032))
# the seal (favicon.svg): center, half-size, tilt, corner radius, seed dot radius — unit space
_SEAL = (1.19, 0.92, 0.182, math.radians(4), 0.04, 0.047)


def mumei_mark(c, cx, cy, r, p_enso=1.0, p_seal=1.0, flecks=1.0, alpha=1.0, ink=None, seal=None, paper=None):
    """The emblem with its ensō centred at (cx, cy), radius r px. p_enso 0..1 paints the stroke along its path;
    p_seal 0..1 stamps the seal (slams in from 1.6×); flecks 0..1 fades the two ink flecks in."""
    ink, seal, paper = ink or INK, seal or SEAL, paper or PAPER
    with c.group(alpha):
        if p_enso > 0:
            cxx = c.ctx
            cxx.new_path()
            for x, y, t, st in _ENSO:
                if t > p_enso:
                    continue
                tip = clamp((p_enso - t) / 0.03)             # the wet tip is a little thinner
                rad = st * r * (0.45 + 0.3 * tip)
                px, py = cx + x * r, cy + y * r
                cxx.new_sub_path()
                cxx.arc(px, py, rad, 0, 2 * math.pi)
            c.src(ink)
            cxx.fill()
        if flecks > 0.01:
            for fx, fy, fr in _FLECKS:
                c.circle(cx + fx * r, cy + fy * r, fr * r * (0.6 + 0.4 * out_expo(flecks)), ink, flecks)
        if p_seal > 0:
            sx, sy, h, rot, rr, dot = _SEAL
            px, py = cx + sx * r, cy + sy * r
            s = 1 + 0.6 * (1 - out_expo(p_seal))
            with c.at(0, 0, s, origin=(px, py), rot=rot):
                with c.group(clamp(p_seal * 3)):
                    c.fill_rrect(px - h * r, py - h * r, 2 * h * r, 2 * h * r, rr * r, seal)
                    c.circle(px, py, dot * r, paper)


def brand_sting(c, t, t0=0.0, dur=STING):
    """Full-screen opening sting (draw at z >= 100): paper → the ensō is brushed in → flecks → the seal stamps →
    the mark shrinks into the HUD corner while the paper fades to reveal the video."""
    u = t - t0
    if u < 0 or u > dur:
        return
    W, H, MID = tk.W, tk.H, tk.W / 2
    ex = dur - 0.4                                             # exit starts
    out = in_out_sine(prog(u, ex, 0.4))
    paper_a = 1 - in_cubic(prog(u, ex + 0.05, 0.35))
    c.src(PAPER, paper_a)
    c.ctx.rectangle(0, 0, W, H)
    c.ctx.fill()
    # the mark: centre stage → flies to the HUD brand corner
    r0, cx0, cy0 = 190.0, MID - 30, 860.0
    r1, cx1, cy1 = 16.0, tk.L["hud_x"] + 14, tk.L["hud_top"] - 6
    r = r0 + (r1 - r0) * out
    cx, cy = cx0 + (cx1 - cx0) * out, cy0 + (cy1 - cy0) * out
    p_enso = in_out_sine(prog(u, 0.05, 0.7))
    mumei_mark(c, cx, cy, r, p_enso=p_enso, p_seal=prog(u, 0.82, 0.25), flecks=prog(u, 0.72, 0.15),
               alpha=1 - prog(u, dur - 0.12, 0.12))
    wa = glide(prog(u, 0.95, 0.35)) * (1 - prog(u, ex, 0.15))
    c.text(MID, 1210, "MUMEYONG", tk.F["mono_med"], 30, INK, wa, 0.3, align="c")
    c.text(MID, 1260, "mumeyong.dev", tk.F["mono"], 22, tk.C["muted"], wa * 0.9, 0.06, align="c")


# ── version 2: the long sting ───────────────────────────────────────────
_rg = random.Random(11)
_GRAIN = [(_rg.uniform(0, tk.W), _rg.uniform(0, tk.H), _rg.uniform(0.6, 1.8)) for _ in range(900)]
_BLOT = [(_rg.uniform(0, 2 * math.pi), _rg.uniform(0.55, 1.0), _rg.uniform(0.25, 0.55)) for _ in range(14)]
_BLEED = [(_rg.uniform(-1, 1), _rg.uniform(-1, 1), _rg.uniform(0.3, 1.0)) for _ in range(9)]
_A0, _SWEEP = -0.95, math.pi * 2 * 0.9          # the ensō path (same as _enso_points)


def _path_xy(p):
    a = _A0 + _SWEEP * p
    rr = 0.86 + 0.035 * math.sin(a * 3 + 1.2)
    return math.cos(a) * rr, math.sin(a) * rr


def _wipe_x(y, q):
    """Brushy diagonal edge of the exit wipe at height y, progress q 0..1 (left → right)."""
    return (-260 + (tk.W + 520) * q + (y - tk.H / 2) * 0.22
            + 34 * math.sin(y * 0.011 + 5 * q) + 14 * math.sin(y * 0.047 + 1.7))


def brand_sting2(c, t, t0=0.0, dur=STING2):
    """The long opening sting (z >= 100), all on paper: an ink drop falls and blooms where the brush starts → the ensō
    is brushed in (wet tip bleeding, slow push-in) → the flecks flick off the dry tail → the seal stamps (shadow,
    press ring, settle) → MUMEYONG arrives letter by letter over a brushed underline → a brushy wipe reveals the
    video while the mark flies into the HUD corner. Times are fractions of dur (default 2,45 s)."""
    u = t - t0
    if u < 0 or u > dur:
        return
    k = dur / STING2                                           # stretch every beat with dur
    W, H, MID = tk.W, tk.H, tk.W / 2
    ctx = c.ctx
    t_drop, t_brush, t_brush_d = 0.22 * k, 0.26 * k, 1.0 * k
    t_fleck, t_seal, t_word, t_exit = 1.18 * k, 1.36 * k, 1.5 * k, 1.95 * k
    q = in_out_sine(prog(u, t_exit, dur - t_exit))             # exit wipe progress
    # paper (+ grain) everywhere right of the wipe edge
    ctx.new_path()
    ctx.move_to(_wipe_x(-40, q), -40)
    for i in range(1, 25):
        y = -40 + (H + 80) * i / 24
        ctx.line_to(_wipe_x(y, q), y)
    ctx.line_to(W + 600, H + 40)
    ctx.line_to(W + 600, -40)
    ctx.close_path()
    c.src(PAPER)
    ctx.fill_preserve()
    ctx.save()
    ctx.clip()
    for gx, gy, gr in _GRAIN:
        c.circle(gx, gy, gr, INK, 0.035)
    ctx.restore()
    if q > 0.001:                                              # a faint wash along the wet edge
        for i in range(24):
            y = H * i / 23
            c.circle(_wipe_x(y, q) + 10, y, 46, INK, 0.05)
    # the mark: slow push-in, then flies to the HUD corner
    fly = in_out_sine(prog(u, t_exit, 0.42 * k))
    push = 1 + 0.07 * in_out_sine(prog(u, 0.2 * k, 1.75 * k))
    r0, cx0, cy0 = 200.0 * push, MID - 32, 820.0
    r1, cx1, cy1 = 16.0, tk.L["hud_x"] + 14, tk.L["hud_top"] - 6
    r = r0 + (r1 - r0) * fly
    cx, cy = cx0 + (cx1 - cx0) * fly, cy0 + (cy1 - cy0) * fly
    a_mark = 1 - prog(u, dur - 0.12, 0.12)
    sx0, sy0 = _path_xy(0.0)
    # ink drop: falls onto the brush's starting point, then blooms into a blot
    if u < t_drop:
        f = in_cubic(prog(u, 0.0, t_drop))
        dy = (1 - f) * (cy0 + sy0 * r0 + 200)
        c.ctx.save()
        c.ctx.translate(cx + sx0 * r, cy + sy0 * r - dy)
        c.ctx.scale(0.7, 1.3)
        c.circle(0, 0, 11, INK)
        c.ctx.restore()
    else:
        bloom = glide(prog(u, t_drop, 0.35 * k)) * (1 - prog(u, t_brush + 0.5 * k, 0.4 * k))
        if bloom > 0.01:
            bx, by = cx + sx0 * r, cy + sy0 * r
            for ang, dist, rad in _BLOT:
                c.circle(bx + math.cos(ang) * dist * r * 0.09 * bloom, by + math.sin(ang) * dist * r * 0.09 * bloom,
                         rad * r * 0.08 * bloom, INK, a_mark)
            ring = prog(u, t_drop, 0.3 * k)
            if ring < 1:
                ctx.new_path()
                ctx.arc(bx, by, r * (0.05 + 0.22 * out_expo(ring)), 0, 2 * math.pi)
                c.src(INK, 0.25 * (1 - ring))
                ctx.set_line_width(2)
                ctx.stroke()
    p_enso = in_out_sine(prog(u, t_brush, t_brush_d))
    p_seal = prog(u, t_seal, 0.2 * k)
    mumei_mark(c, cx, cy, r, p_enso=p_enso, p_seal=p_seal, flecks=out_expo(prog(u, t_fleck, 0.18 * k)), alpha=a_mark)
    if 0 < p_enso < 1 or prog(u, t_brush + t_brush_d, 0.3 * k) < 1:      # wet tip bleeding into the paper
        tx, ty = _path_xy(p_enso)
        wet = 1 - prog(u, t_brush + t_brush_d, 0.3 * k)
        for bx_, by_, br in _BLEED:
            c.circle(cx + (tx + bx_ * 0.03) * r, cy + (ty + by_ * 0.03) * r, br * r * 0.03, INK, 0.22 * wet * a_mark)
    # seal: shadow before it lands, a press ring after
    sx, sy, h_, _, _, _ = _SEAL
    spx, spy = cx + sx * r, cy + sy * r
    pre = prog(u, t_seal - 0.15 * k, 0.15 * k) * (1 - prog(u, t_seal + 0.05 * k, 0.1 * k))
    if pre > 0.01:
        c.fill_rrect(spx - h_ * r * 1.3, spy - h_ * r * 1.1, 2.6 * h_ * r, 2.6 * h_ * r, 10, INK, 0.12 * pre)
    ring = prog(u, t_seal + 0.18 * k, 0.4 * k)
    if 0 < ring < 1:
        e_ = out_expo(ring)
        c.stroke_rrect(spx - h_ * r * (1.1 + 0.6 * e_), spy - h_ * r * (1.1 + 0.6 * e_), 2 * h_ * r * (1.1 + 0.6 * e_),
                       2 * h_ * r * (1.1 + 0.6 * e_), 12, SEAL, 3, 0.35 * (1 - ring) * a_mark)
    # wordmark + brushed underline + url
    wa = 1 - prog(u, t_exit, 0.25 * k)
    if u >= t_word and wa > 0.002:
        from .kinetic import track_line
        with c.group(wa):
            track_line(c, t, t0 + t_word, None, MID, 1235, tk.BRAND_NAME.upper(), "display", 92, INK, ls=0.04,
                       align="c", flash=SEAL, d_in=0.55 * k)
            ul = in_out_sine(prog(u, t_word + 0.2 * k, 0.4 * k))
            if ul > 0:
                x0, x1, y0 = MID - 230, MID - 230 + 460 * ul, 1272
                for i in range(30):
                    f = i / 29
                    if x0 + 460 * f > x1:
                        break
                    c.circle(x0 + 460 * f, y0 + 2 * math.sin(f * 7), 5.5 * (1 - 0.65 * f), SEAL)
            c.text(MID, 1340, "mumeyong.dev", tk.F["mono"], 26, tk.C["muted"], glide(prog(u, t_word + 0.35 * k, 0.3)),
                   0.12, align="c")


def brand_intro(v, t0=0.0, dur=None, version=1):
    """Register the opening sting on video v (overlay above the HUD) + its sounds. Pair with PRE_ROLL in scenes.py.
    version=2 = the long sting (STING2 s, PRE_ROLL = 2.05) — new videos from 2026-10-09; 1 = the original 1,5 s."""
    if version == 2:
        dur = dur or STING2
        k = dur / STING2
        v.add(t0, t0 + dur, lambda c, t: brand_sting2(c, t, t0, dur), z=120)
        v.sfx("pop", t0 + 0.22 * k, 0.6)                    # the drop lands
        v.sfx("whoosh", t0 + 0.3 * k, 0.35)                 # the brush stroke
        v.sfx("tick", t0 + 1.18 * k, 0.5)                   # flecks
        v.sfx("thud", t0 + 1.36 * k, 0.8)                   # the seal
        v.sfx("chime", t0 + 1.55 * k, 0.45)                 # wordmark (pitched to the score's key with a kit)
        v.sfx("whoosh", t0 + 1.95 * k, 0.45)                # wipe into the video
        return t0 + dur
    dur = dur or STING
    v.add(t0, t0 + dur, lambda c, t: brand_sting(c, t, t0, dur), z=120)
    v.sfx("whoosh", t0 + 0.05, 0.3)                         # the brush stroke
    v.sfx("thud", t0 + 0.82, 0.7)                           # the seal
    v.sfx("whoosh", t0 + dur - 0.4, 0.35)                   # into the video
    return t0 + dur
