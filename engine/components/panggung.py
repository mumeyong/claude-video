"""Hajatan-stage components (first used in "ai-butuh-cloud-engineer").

panggung · panggung_geo · sorot
Metaphor: AI is the singer (biduan) everyone sees on a hajatan stage. The infra lives in the dark under the stage
(kolong panggung): a generator = GPU, a cable drum = network, a road case = storage, a rental slip = cost. The crew
member at the mixer in the dark wing (kru sound) = the cloud engineer.
Signature: a soft pool of follow-spot light (sorot) searches the dark parts; whatever it touches lights up and stays lit.
Pure functions of their parameters (frame = f(t)). Colors from tokens; shading via material (look="flat" | "paper" | "lit").
"""
import math

from .. import tokens as tk
from ..ease import clamp, lerp, mix
from . import material as mat

PURPLE = tk.CHAPTER[3][0]            # signature: dress, lamps, spot, generator, headset
C, F = tk.C, tk.F
DARK = C["d_card"]                   # the unlit parts (kolong, wing)
DIM = 0.13                           # how much of an unlit prop shows in the dark (a silhouette)
ITEMS = ("genset", "kabel", "peti", "nota", "kru")


def panggung_geo(x, y, w, h):
    """Geometry of panggung() drawn with the same x, y, w, h (no drawing): dict with floor (deck top y), deck_h,
    kolong / wing rects, singer (cx, base_y, s), lamps [(x, y)], and items {name: (x, y, w, h)} for genset · kabel ·
    peti · nota · kru — use the boxes to aim the spot and to place tags."""
    tr_y, tr_h = y + 0.03 * h, 0.035 * h
    fy, dh = y + 0.52 * h, 0.035 * h
    ground = y + h - 0.035 * h
    kol = (x, fy + dh, w, y + h - fy - dh)
    wing = (x + 0.70 * w, tr_y + tr_h, 0.30 * w, fy - tr_y - tr_h)
    gw, gh = 0.20 * w, 0.17 * h
    kr = 0.072 * w
    pw, ph = 0.17 * w, 0.13 * h
    nw, nh = 0.105 * w, 0.15 * h
    items = {
        "genset": (x + 0.15 * w - gw / 2, ground - gh, gw, gh),
        "kabel": (x + 0.39 * w - kr, ground - 2 * kr, 2 * kr, 2 * kr),
        "peti": (x + 0.60 * w - pw / 2, ground - ph, pw, ph),
        "nota": (x + 0.80 * w - nw / 2, kol[1] + 0.07 * h, nw, nh),
        "kru": (x + 0.73 * w, fy - 0.235 * h, 0.15 * w, 0.235 * h),
    }
    return dict(truss=(x, tr_y, w, tr_h), floor=fy, deck_h=dh, ground=ground, kolong=kol, wing=wing,
                singer=(x + 0.43 * w, fy, 0.29 * h), lamps=[(x + 0.24 * w, tr_y + tr_h), (x + 0.58 * w, tr_y + tr_h)],
                items=items)


def sorot(c, cx, cy, r, amount=1.0, color=None):
    """Follow-spot pool on a dark surface: a soft disc of light (bright core, long falloff) — light, not a neon glow."""
    if amount <= 0.002:
        return
    import cairo
    color = color or PURPLE
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, r)
    lt = mat.tone(color, 0.82)
    g.add_color_stop_rgba(0.0, *lt[:3], 0.42 * amount)
    g.add_color_stop_rgba(0.55, *lt[:3], 0.22 * amount)
    g.add_color_stop_rgba(1.0, *lt[:3], 0.0)
    ctx = c.ctx
    ctx.save()
    ctx.set_source(g)
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()


# ── props ───────────────────────────────────────────────────────────────
def _genset(c, look, box, t, run, color, a):
    x, y, w, h = box
    fh = h * 0.16                                                    # frame rails + wheels
    mat.body(c, look, mat.rrect_path(x, y, w, h - fh, w * 0.05), (x, y, w, h - fh), color, a, lift=0.4)
    for k in range(5):                                               # louvres
        yy = y + h * 0.16 + k * h * 0.09
        c.line(x + w * 0.10, yy, x + w * 0.48, yy, mat.tone(color, -0.35), max(2.0, w * 0.018), a)
    px, py, pw, ph = x + w * 0.58, y + h * 0.14, w * 0.32, h * 0.38                # control panel
    c.fill_rrect(px, py, pw, ph, w * 0.03, C["card"], a)
    lamp = mix(C["faint"], C["ok"], clamp(run))
    c.circle(px + pw * 0.28, py + ph * 0.3, w * 0.035, lamp, a)
    c.circle(px + pw * 0.68, py + ph * 0.3, w * 0.035, C["faint"], a)
    c.fill_rrect(px + pw * 0.15, py + ph * 0.6, pw * 0.7, ph * 0.18, ph * 0.09, C["muted"], a * 0.6)
    c.fill_rrect(x - w * 0.02, y + h - fh, w * 1.04, fh * 0.42, fh * 0.2, C["ink2"], a)
    for wx in (x + w * 0.16, x + w * 0.84):
        c.circle(wx, y + h - fh * 0.3, fh * 0.32, C["ink2"], a)
    ex, ey = x + w * 0.2, y                                          # exhaust pipe + puffs while running
    c.fill_rrect(ex - w * 0.03, ey - h * 0.14, w * 0.06, h * 0.15, w * 0.02, C["muted"], a)
    if run > 0.01:
        for k in range(3):
            ph_ = (t * 0.7 + k / 3) % 1.0
            r = w * (0.04 + 0.07 * ph_)
            c.circle(ex + w * 0.05 * ph_, ey - h * 0.16 - h * 0.45 * ph_, r, C["muted"], a * run * 0.45 * (1 - ph_))


def _kabel(c, look, box, color, a):
    x, y, w, h = box
    cx, cy, r = x + w / 2, y + h / 2, w / 2
    mat.body(c, look, mat.circle_path(cx, cy, r), box, C["faint"], a, lift=0.4)
    c.circle(cx, cy, r * 0.78, mat.tone(color, -0.25), a)                       # wound cable
    for k in range(4):
        c.ctx.new_path()
        c.ctx.arc(cx, cy, r * (0.72 - 0.11 * k), 0, 2 * math.pi)
        c.src(mat.tone(color, 0.15), a * 0.55)
        c.ctx.set_line_width(max(1.5, r * 0.03))
        c.ctx.stroke()
    c.circle(cx, cy, r * 0.28, C["faint"], a)
    c.circle(cx, cy, r * 0.1, C["ink2"], a)


def _peti(c, look, box, a):
    x, y, w, h = box
    mat.body(c, look, mat.rrect_path(x, y, w, h, w * 0.04), box, C["ink2"], a, lift=0.4)
    c.line(x, y + h * 0.3, x + w, y + h * 0.3, C["muted"], max(2.0, h * 0.03), a)           # lid seam
    s = w * 0.12
    for (qx, qy) in ((x, y), (x + w - s, y), (x, y + h - s), (x + w - s, y + h - s)):        # metal corners
        c.fill_rrect(qx, qy, s, s, s * 0.2, C["faint"], a)
    c.fill_rrect(x + w * 0.38, y + h * 0.16, w * 0.24, h * 0.1, h * 0.04, C["faint"], a)       # latch
    c.fill_rrect(x + w * 0.3, y + h * 0.5, w * 0.4, h * 0.22, h * 0.03, C["card"], a * 0.85)  # stencil plate
    c.line(x + w * 0.36, y + h * 0.61, x + w * 0.64, y + h * 0.61, C["ink2"], max(1.5, h * 0.025), a)


def _nota(c, look, box, color, a):
    x, y, w, h = box
    with c.at(0, 0, 1.0, origin=(x + w / 2, y), rot=0.07):          # taped on a touch crooked
        mat.body(c, look, mat.rrect_path(x, y, w, h, 4), box, C["card"], a, lift=0.3)
        c.fill_rrect(x, y, w, h * 0.13, 4, color, a)
        for k in range(5):
            yy = y + h * (0.28 + 0.12 * k)
            c.line(x + w * 0.14, yy, x + w * (0.86 if k % 2 == 0 else 0.62), yy, C["faint"], max(1.5, w * 0.03), a)
        c.line(x + w * 0.14, y + h * 0.9, x + w * 0.86, y + h * 0.9, C["ink2"], max(2.0, w * 0.04), a)
        c.fill_rrect(x + w * 0.3, y - h * 0.05, w * 0.4, h * 0.1, 2, C["faint"], a * 0.9)    # tape


def _kru(c, box, t, color, a):
    """Sound crew at the mixer, seen from the side, facing the stage (left), headset on."""
    x, y, w, h = box
    s = h
    hx, hy, hr = x + w * 0.55, y + s * 0.2, s * 0.1
    c.fill_rrect(hx - s * 0.13, hy + s * 0.1, s * 0.26, s * 0.42, s * 0.1, C["ink2"], a)      # torso
    c.fill_rrect(hx - s * 0.2, hy + s * 0.28, s * 0.2, s * 0.06, s * 0.03, C["ink2"], a)      # arm to the faders
    c.circle(hx, hy, hr, mat.tone(C["orange_pill"], -0.25), a)                               # head
    c.ctx.new_path()                                                                         # headset band + cup
    c.ctx.arc(hx, hy, hr * 1.18, math.pi * 1.05, math.pi * 1.95)
    c.src(color, a)
    c.ctx.set_line_width(max(2.0, s * 0.025))
    c.ctx.stroke()
    c.fill_rrect(hx + hr * 0.6, hy - hr * 0.35, hr * 0.55, hr * 0.8, hr * 0.2, color, a)
    c.line(hx - hr * 1.1, hy + hr * 0.4, hx - hr * 0.2, hy + hr * 0.95, color, max(1.5, s * 0.012), a)  # mic arm
    dx, dy, dw, dh = x - w * 0.02, y + s * 0.62, w * 0.62, s * 0.12                          # mixer desk
    c.fill_rrect(dx, dy, dw, dh, s * 0.02, C["muted"], a)
    for k in range(6):
        fx = dx + dw * (0.12 + 0.15 * k)
        c.line(fx, dy + dh * 0.25, fx, dy + dh * 0.75, C["ink2"], max(1.5, s * 0.01), a)
        kk = 0.5 + 0.35 * math.sin(k * 1.9 + 0.8)
        c.fill_rrect(fx - s * 0.012, dy + dh * (0.2 + 0.5 * kk) - s * 0.008, s * 0.024, s * 0.016, 2, C["card"], a)
    c.fill_rrect(dx + dw * 0.45, y + s * 0.74, s * 0.035, s * 0.26, 2, C["ink2"], a)          # desk leg / stool
    c.fill_rrect(x + w * 0.62, y + s * 0.74, s * 0.035, s * 0.26, 2, C["ink2"], a)


def _biduan(c, cx, base_y, s, color, swap, a):
    """Singer at the mic (a person, not a robot). swap 0..1 crossfades to the next singer (other dress + hair)."""
    for k, (dress, a_k) in enumerate(((color, 1 - swap), (mat.tone(C["ok"], -0.1), swap))):
        if a_k * a <= 0.002:
            continue
        aa = a_k * a
        hr = s * 0.085
        hy = base_y - s + hr
        skin = mat.tone(C["orange_pill"], 0.25)
        if k == 0:                                                           # long hair behind the head
            c.fill_rrect(cx - hr * 1.1, hy - hr * 0.9, hr * 2.2, hr * 3.0, hr, C["ink2"], aa)
        c.circle(cx, hy, hr, skin, aa)
        if k == 1:                                                           # short hair + bun
            c.circle(cx - hr * 0.2, hy - hr * 0.5, hr * 0.85, C["ink2"], aa)
            c.circle(cx - hr * 0.9, hy - hr * 0.9, hr * 0.45, C["ink2"], aa)
        c.ctx.new_path()                                                     # dress: a soft trapezoid
        top, bot = hy + hr * 1.3, base_y - s * 0.02
        c.ctx.move_to(cx - s * 0.08, top)
        c.ctx.line_to(cx + s * 0.08, top)
        c.ctx.line_to(cx + s * 0.17, bot)
        c.ctx.line_to(cx - s * 0.17, bot)
        c.ctx.close_path()
        c.src(dress, aa)
        c.ctx.fill()
        c.line(cx + s * 0.06, top + s * 0.06, cx + s * 0.17, hy + hr * 0.6, skin, max(2.0, s * 0.04), aa)   # arm
    mx = cx + s * 0.2                                                        # mic stand
    c.line(mx, base_y, mx, base_y - s * 0.72, C["ink2"], max(2.0, s * 0.018), a)
    c.line(mx, base_y - s * 0.72, mx - s * 0.04, base_y - s * 0.8, C["ink2"], max(2.0, s * 0.018), a)
    c.circle(mx - s * 0.045, base_y - s * 0.81, s * 0.025, C["ink2"], a)
    c.fill_rrect(mx - s * 0.08, base_y - s * 0.02, s * 0.16, s * 0.02, s * 0.01, C["ink2"], a)


def _speaker(c, look, x, y, w, h, a):
    for k, (yy, hh) in enumerate(((y, h * 0.55), (y + h * 0.55, h * 0.45))):
        mat.body(c, look, mat.rrect_path(x, yy, w, hh - 4, 8), (x, yy, w, hh - 4), C["ink2"], a, lift=0.3)
        r = min(w, hh) * 0.3
        c.circle(x + w / 2, yy + hh / 2 - 2, r, C["muted"], a)
        c.circle(x + w / 2, yy + hh / 2 - 2, r * 0.4, C["ink2"], a)


# ── the stage ───────────────────────────────────────────────────────────
def panggung(c, x, y, w, h, t, lit=None, spot=None, show=1.0, run=0.0, pack=None, swap=0.0, banner="LIVE",
             look="flat", color=None, alpha=1.0):
    """Hajatan stage cut open from the side, box (x, y, w, h): truss + two lamps, backdrop, speaker stack, the
    singer at a mic (lit by the lamps, show 0..1), a dark wing on the right with the sound crew at a mixer, the deck,
    and the dark space under it (kolong) with scaffolding, generator, cable drum, road case and a rental slip.
    lit = {name: 0..1} for genset · kabel · peti · nota · kru (unlit = a dim silhouette in the dark).
    spot = (cx, cy, r, amount) — follow-spot pool, drawn on the dark parts only. run 0..1 = generator running (lamp +
    exhaust puffs, pure function of t). pack = {name: 0..1} draws a dashed 'container' box around a prop.
    swap 0..1 = the next singer. Geometry: panggung_geo(x, y, w, h)."""
    if alpha <= 0.002:
        return
    color = color or PURPLE
    lit = lit or {}
    pack = pack or {}
    g = panggung_geo(x, y, w, h)
    fy, dh = g["floor"], g["deck_h"]
    lv = {k: lerp(DIM, 1.0, clamp(lit.get(k, 0.0))) for k in ITEMS}
    with c.group(alpha):
        bx, by, bw = x + 0.05 * w, g["truss"][1] + g["truss"][3] + 0.02 * h, 0.65 * w             # backdrop
        bhh = fy - by
        c.fill_rrect(bx, by, bw, bhh, 6, mix(C["bg"], color, 0.10))
        c.fill_rrect(bx + bw * 0.3, by + bhh * 0.1, bw * 0.4, bhh * 0.13, 6, mix(C["bg"], color, 0.22))
        c.text(bx + bw * 0.5, by + bhh * 0.1 + bhh * 0.09, banner, F["mono_bold"], max(17, bhh * 0.07),
               mat.tone(color, -0.2), 1, 0.3, align="c")
        for lx, ly in g["lamps"]:                                                # show light onto the singer
            scx, sby, ss = g["singer"]
            if show > 0.01:
                c.ctx.new_path()
                c.ctx.move_to(lx - w * 0.02, ly + h * 0.04)
                c.ctx.line_to(lx + w * 0.02, ly + h * 0.04)
                c.ctx.line_to(scx + ss * 0.45, sby)
                c.ctx.line_to(scx - ss * 0.45, sby)
                c.ctx.close_path()
                c.src(mat.tone(color, 0.85), 0.32 * show)
                c.ctx.fill()
        _speaker(c, look, x + 0.08 * w, fy - 0.22 * h, 0.12 * w, 0.22 * h, 1.0)
        scx, sby, ss = g["singer"]
        mat.spill(c, look, scx, sby, ss * 0.6, color, show)
        c.fill_rrect(scx - ss * 0.42, sby - 6, ss * 0.84, 12, 6, mat.tone(color, 0.75), 0.6 * show)   # light pool
        _biduan(c, scx, sby, ss, color, clamp(swap), 1.0)

        wx, wy, ww, wh = g["wing"]                                             # dark wing + kolong
        kx, ky, kw, kh = g["kolong"]
        c.fill_rrect(wx, wy, ww, wh, 0, DARK)
        c.fill_rrect(kx, ky, kw, kh, 0, DARK)
        for k in range(4):                                                     # wing curtain folds
            fx = wx + ww * (0.12 + 0.25 * k)
            c.line(fx, wy, fx, wy + wh, mat.tone(DARK, 0.08), max(2.0, ww * 0.03))
        if spot:
            scx_, scy_, sr, sa = spot
            with c.clip(wx, wy, ww, wh):
                sorot(c, scx_, scy_, sr, sa, color)
            with c.clip(kx, ky, kw, kh):
                sorot(c, scx_, scy_, sr, sa, color)
        with c.clip(kx, ky, kw, kh):                                           # scaffolding
            pole = mat.tone(DARK, 0.16)
            xs = [kx + kw * f for f in (0.03, 0.27, 0.51, 0.73, 0.97)]
            for px in xs:
                c.line(px, ky, px, ky + kh, pole, max(3.0, w * 0.008))
            for a_, b_ in zip(xs, xs[1:]):
                c.line(a_, ky + kh * 0.08, b_, ky + kh * 0.9, pole, max(2.0, w * 0.004), 0.7)
            c.line(kx, g["ground"], kx + kw, g["ground"], mat.tone(DARK, 0.2), max(2.0, h * 0.004))
            it = g["items"]
            gx, gy, gw_, gh_ = it["genset"]
            c.line(gx + gw_ * 0.9, gy + gh_ * 0.4, gx + gw_ * 1.4, ky + 4, mat.tone(color, -0.2), max(3, w * 0.006),
                   lv["genset"])                                               # power cable up to the deck
            _genset(c, look, it["genset"], t, clamp(run), color, lv["genset"])
            _kabel(c, look, it["kabel"], color, lv["kabel"])
            _peti(c, look, it["peti"], lv["peti"])
            _nota(c, look, it["nota"], color, lv["nota"])
            for name in ("genset", "kabel", "peti", "nota"):
                p = clamp(pack.get(name, 0.0))
                if p > 0.002:
                    ix, iy, iw, ih = it[name]
                    pad = 0.018 * w
                    c.stroke_rrect(ix - pad, iy - pad, iw + 2 * pad, ih + 2 * pad, 12, mat.tone(color, 0.45),
                                   max(2.5, w * 0.004), p, dash=[14, 10])
        with c.clip(wx, wy, ww, wh):
            _kru(c, g["items"]["kru"], t, color, lv["kru"])

        tx, ty, tw_, th_ = g["truss"]                                          # truss + lamps on top
        c.fill_rrect(tx, ty, tw_, th_, 4, C["ink2"])
        n = 18
        for k in range(n):
            x0 = tx + tw_ * k / n
            c.line(x0, ty + th_ * 0.2, x0 + tw_ / n, ty + th_ * 0.8, C["muted"], max(1.5, h * 0.003))
        for lx, ly in g["lamps"]:
            c.fill_rrect(lx - w * 0.03, ly, w * 0.06, h * 0.05, w * 0.012, C["ink2"])
            c.fill_rrect(lx - w * 0.025, ly + h * 0.04, w * 0.05, h * 0.012, 3, mix(C["faint"], mat.tone(color, 0.6),
                                                                                      clamp(show)))
        c.fill_rrect(x, fy, w, dh, 0, C["ink2"])                               # deck
        c.line(x, fy + 2, x + w, fy + 2, C["muted"], max(2.0, dh * 0.12))
    return g
