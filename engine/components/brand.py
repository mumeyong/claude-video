"""The brand mark from mumeyong.dev — the "mumei" (無名, nameless) emblem — and the opening brand sting.

An ensō left open at the upper right (heavy where the brush starts, thinning, breaking into a dry-brush tail) and a
blank vermilion hanko seal, tilted 4°, where a name would be signed, holding only a seed dot. Geometry ported from
the site (src/scripts/atlas/particles.ts → emblemPoints; public/favicon.svg for the seal).

    PRE_ROLL = 1.2                     # top of scenes.py: voice + all times start after the sting (opt-in)
    brand_intro(v)                     # in build(): registers the sting overlay + its SFX at t = 0
    mumei_mark(c, cx, cy, r)           # the static mark anywhere (outro, cover)
"""
import math
import random

from .. import tokens as tk
from ..ease import clamp, in_cubic, in_out_sine, out_expo, prog

PAPER, INK, SEAL = tk.C["brand_paper"], tk.C["brand_ink"], tk.C["brand_seal"]
STING = 1.5                                     # seconds; PRE_ROLL a bit shorter so the hook starts under the exit


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
    wa = out_expo(prog(u, 0.95, 0.35)) * (1 - prog(u, ex, 0.15))
    c.text(MID, 1210, "MUMEYONG", tk.F["mono_med"], 30, INK, wa, 0.3, align="c")
    c.text(MID, 1260, "mumeyong.dev", tk.F["mono"], 22, tk.C["muted"], wa * 0.9, 0.06, align="c")


def brand_intro(v, t0=0.0, dur=STING):
    """Register the opening sting on video v (overlay above the HUD) + its sounds. Pair with PRE_ROLL in scenes.py."""
    v.add(t0, t0 + dur, lambda c, t: brand_sting(c, t, t0, dur), z=120)
    v.sfx("whoosh", t0 + 0.05, 0.3)                         # the brush stroke
    v.sfx("thud", t0 + 0.82, 0.7)                           # the seal
    v.sfx("whoosh", t0 + dur - 0.4, 0.35)                   # into the video
    return t0 + dur
