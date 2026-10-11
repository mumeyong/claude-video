"""Rainy-day home components (first used in "wifi-ep03-lemot-pas-hujan", Bongkar WiFi Rumah EP 03).

hujan · tetes · odp_box · rumah_potong · rumah_geo · along
Metaphor: a leaking gutter (talang bocor) — the rain is everywhere, but only one joint drips. The house is cut open:
inside the router and the phone stay dry; outside the drop cable runs from the ODP box on the pole along the eave
like a gutter. Signature: one drop leaves the rain, slides along the cable and slips through the gap in the ODP lid,
and the light in the fiber goes weak. Everything is a pure function of t and its progress values (frame = f(t)).
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix

TEAL = tk.CHAPTER[4][0]             # signature: water + the light in the fiber
WHITE = (1, 1, 1, 1)


def _h(i, k=0, seed=0):
    """Deterministic hash → 0..1 (seeded, no global randomness)."""
    v = math.sin(i * 12.9898 + k * 78.233 + seed * 37.719) * 43758.5453
    return v - math.floor(v)


def along(pts, f):
    """(x, y, angle) at arc-length fraction f (0..1) of polyline pts."""
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(segs) or 1.0
    d = clamp(f) * total
    for (a, b), L in zip(zip(pts, pts[1:]), segs):
        if d <= L or L == segs[-1]:
            u = d / L if L else 0.0
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, math.atan2(b[1] - a[1], b[0] - a[0])
        d -= L
    return pts[-1][0], pts[-1][1], 0.0


def _sag(p0, p1, sag, n=14):
    """Points of a cable hanging between p0 and p1 (parabolic sag)."""
    return [(p0[0] + (p1[0] - p0[0]) * k / n, p0[1] + (p1[1] - p0[1]) * k / n + sag * 4 * (k / n) * (1 - k / n))
            for k in range(n + 1)]


def _polyline(c, pts, color, width, alpha=1.0):
    ctx = c.ctx
    ctx.new_path()
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    c.src(color, alpha)
    ctx.set_line_width(width)
    ctx.set_line_cap(1)
    ctx.set_line_join(1)
    ctx.stroke()


def _poly(c, pts, color, alpha=1.0):
    ctx = c.ctx
    ctx.new_path()
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    c.src(color, alpha)
    ctx.fill()


# ── rain + one drop ─────────────────────────────────────────────────────
def hujan(c, box, t, density=1.0, color=None, n=110, speed=1700, length=54, slant=0.16, width=3.0, seed=1,
          alpha=1.0):
    """Rain streaks inside box (x, y, w, h), clipped to it. density 0..1 thins the rain streak by streak (each has
    its own threshold), so 1 → 0 is the rain stopping, not fading. Positions are a pure function of t."""
    if density <= 0.001 or alpha <= 0.001:
        return
    x, y, w, h = box
    col = color or mix(c.theme("muted", "d_muted"), TEAL, 0.35)
    span = h + length * 2
    with c.clip(x, y, w, h):
        for i in range(n):
            a = clamp((density - _h(i, 4, seed)) * 8) * (0.35 + 0.35 * _h(i, 3, seed))
            if a <= 0.01:
                continue
            sp = speed * (0.85 + 0.3 * _h(i, 2, seed))
            yy = y - length + (_h(i, 1, seed) * span + t * sp) % span
            xx = x - slant * h + _h(i, 0, seed) * (w + slant * h) + slant * (yy - y)
            c.line(xx, yy, xx - slant * length, yy - length, col, width, a * alpha)


def tetes(c, cx, cy, s, color=None, alpha=1.0, stretch=0.0):
    """One water drop, height s, its round belly centred on (cx, cy). stretch 0..1 pulls the tip up (falling)."""
    if alpha <= 0.001:
        return
    col = color or TEAL
    r = s * 0.34
    tip = cy - s * (0.62 + 0.45 * stretch)
    ctx = c.ctx
    ctx.new_path()
    ctx.move_to(cx, tip)
    ctx.curve_to(cx + r * 0.25, tip + s * 0.25, cx + r, cy - r * 0.55, cx + r, cy)
    ctx.arc(cx, cy, r, 0, math.pi)
    ctx.curve_to(cx - r, cy - r * 0.55, cx - r * 0.25, tip + s * 0.25, cx, tip)
    ctx.close_path()
    c.src(col, alpha)
    ctx.fill()
    c.circle(cx - r * 0.38, cy - r * 0.18, r * 0.2, WHITE, 0.55 * alpha)


# ── the ODP box on the pole, close-up ───────────────────────────────────
def odp_box(c, cx, cy, w, t, lid=0.0, wet=0.0, glow=1.0, label="ODP", color=None, alpha=1.0):
    """Fiber distribution box (ODP) on a pole, close-up, centred on (cx, cy), width w (height 1.3 w). The front is
    cut open: a splice tray with fiber loops and three splice sleeves. lid 0..1 tilts the cap open at the right
    (the gap water gets in); wet 0..1 pools water at the bottom + beads on the splices; glow 0..1 = light in the
    fiber (it flickers as wet rises). Returns dict(gap=(x, y), splice=(x, y), out=(x, y), cap=(x, y, w, h))."""
    col = color or TEAL
    h = w * 1.3
    x0, y0 = cx - w / 2, cy - h / 2
    body, ink2 = c.theme("ink2", "d_line"), c.theme("ink", "d_bg")
    pole = c.theme("faint", "d_line")
    flick = 1.0 - clamp(wet) * (0.35 + 0.35 * (0.5 + 0.5 * math.sin(t * 9.0) * math.sin(t * 3.7)))
    lum = clamp(glow) * flick
    with c.group(alpha):
        c.fill_rrect(cx - w * 0.07, y0 - h * 0.35, w * 0.14, h * 1.75, w * 0.03, pole)            # the pole
        for k in (0.18, 0.82):                                                                    # steel bands
            c.fill_rrect(cx - w * 0.11, y0 + h * k, w * 0.22, w * 0.05, w * 0.02, c.theme("line", "d_line"))
        c.shadow(x0, y0, w, h, w * 0.06, 34, 14, 0.10)
        c.fill_rrect(x0, y0, w, h, w * 0.06, body)
        ix, iy, iw, ih = x0 + w * 0.09, y0 + h * 0.13, w * 0.82, h * 0.66                          # cut-open window
        c.fill_rrect(ix, iy, iw, ih, w * 0.035, c.theme("card", "d_card"))
        tx, ty, tw, th = ix + iw * 0.08, iy + ih * 0.1, iw * 0.84, ih * 0.62                       # splice tray
        c.fill_rrect(tx, ty, tw, th, w * 0.03, c.theme("bg", "d_bg"))
        c.stroke_rrect(tx, ty, tw, th, w * 0.03, c.theme("line", "d_line"), 2)
        lw = max(2.5, w * 0.012)
        for k in range(2):                                                                         # fiber loops
            m = w * (0.05 + 0.05 * k)
            c.stroke_rrect(tx + m, ty + m, tw - 2 * m, th - 2 * m, (th - 2 * m) * 0.45,
                           mix(c.theme("faint", "d_line"), col, 0.25 + 0.75 * lum), lw, 0.9)
        sx = [tx + tw * f for f in (0.3, 0.5, 0.7)]
        sy = ty + th * 0.5
        for k, x_ in enumerate(sx):                                                                # splice sleeves
            c.fill_rrect(x_ - w * 0.055, sy - w * 0.022, w * 0.11, w * 0.044, w * 0.022,
                         col if k == 1 else c.theme("muted", "d_muted"), 0.35 + 0.65 * lum if k == 1 else 0.8)
        for k in range(6):                                                                         # light pulses
            f = (t * 0.32 + k / 6) % 1.0
            px = tx + w * 0.05 + (tw - w * 0.1) * f
            c.circle(px, ty + w * 0.05, lw * 1.5, col, lum * min(1, f * 6, (1 - f) * 6))
        if wet > 0.01:                                                                             # water + beads
            wh = ih * 0.22 * clamp(wet)
            ctx = c.ctx
            with c.clip(ix, iy, iw, ih, w * 0.035):
                ctx.new_path()
                ctx.move_to(ix, iy + ih)
                for k in range(25):
                    xx = ix + iw * k / 24
                    ctx.line_to(xx, iy + ih - wh + math.sin(xx * 0.05 + t * 2.4) * w * 0.008)
                ctx.line_to(ix + iw, iy + ih)
                ctx.close_path()
                c.src(col, 0.32)
                ctx.fill()
            for k, (dx, dy) in enumerate(((-0.03, -0.035), (0.04, 0.03), (0.0, 0.045))):
                b = clamp(wet * 3 - k)
                if b > 0:
                    tetes(c, sx[1] + w * dx, sy + w * dy, w * 0.05, col, b)
        c.text(cx, y0 + h * 0.9, label, tk.F["mono_bold"], max(17, w * 0.075), WHITE, 0.9, 0.2, align="c")
        for k, dx in enumerate((-0.18, 0.0, 0.18)):                                                # cables out
            cx_ = cx + w * dx
            c.line(cx_, y0 + h, cx_ + w * 0.05 * dx * 4, y0 + h * 1.35, ink2 if k != 1 else col, lw * 2.2,
                   1.0 if k != 1 else 0.4 + 0.6 * lum)
        cap_w, cap_h = w * 1.08, h * 0.1                                                          # the cap / lid
        cx0, cy0 = cx - cap_w / 2, y0 - cap_h * 0.6
        ang = -0.16 * clamp(lid)
        with c.at(0, 0, 1, origin=(cx0, cy0 + cap_h), rot=ang):
            c.fill_rrect(cx0, cy0, cap_w, cap_h, cap_h * 0.35, c.theme("ink", "d_line"))
        gap = (cx0 + cap_w - w * 0.08, cy0 + cap_h + math.sin(ang) * cap_w * 0.4)
    return dict(gap=gap, splice=(sx[1], sy), out=(cx, y0 + h * 1.35), cap=(cx0, cy0, cap_w, cap_h))


# ── the house, cut open, with the pole outside ──────────────────────────
def rumah_geo(x, base_y, w, h):
    """Geometry of rumah_potong drawn with the same x, base_y, w, h (no drawing): dict with router, phone,
    phone_box, window, odp (box), cable (ODP → router points), feeder, wall_x, inside (x, y, w, h), eave, top, th."""
    hx0, hx1 = x + w * 0.03, x + w * 0.60
    top = base_y - h * 0.52
    th = max(10, w * 0.016)                                                    # cut-section thickness
    inside = (hx0 + th, top + th, hx1 - hx0 - 2 * th, base_y - top - th)
    ix, iy, iw, ih = inside
    px = x + w * 0.86                                                          # pole
    odp = (px - w * 0.035, base_y - h * 0.66, w * 0.07, w * 0.09)
    eave = (hx1 + w * 0.05, top - h * 0.02)
    router = (hx1 - th - w * 0.08, base_y - h * 0.24)
    phone = (hx0 + th + w * 0.12, base_y - h * 0.15)
    pw, ph = w * 0.06, w * 0.11
    hole = (hx1, top + h * 0.06)
    cable = (_sag((odp[0] + odp[2] / 2, odp[1] + odp[3]), eave, h * 0.06, 12)
             + [(hx1 + w * 0.012, top + h * 0.01), hole, (router[0] + w * 0.03, hole[1]),
                (router[0] + w * 0.03, router[1] - w * 0.03)])
    feeder = [(x + w + 40, base_y - h * 0.86), (px, base_y - h * 0.86), (px, odp[1])]
    return dict(hx0=hx0, hx1=hx1, top=top, th=th, inside=inside, px=px, odp=odp, eave=eave, router=router,
                phone=phone, phone_box=(phone[0] - pw / 2, phone[1] - ph / 2, pw, ph),
                window=(ix + iw * 0.06, iy + ih * 0.18, iw * 0.26, ih * 0.3), cable=cable, feeder=feeder,
                peak=(hx0 + (hx1 - hx0) / 2, base_y - h * 0.82), wall_x=hx1)


def rumah_potong(c, x, base_y, w, h, t, light=1.0, loss=0.0, screen=None, odp_lid=0.0, rain=0.0, color=None,
                 alpha=1.0):
    """Cut-away house in the rain, scene (x, base_y - h) → (x + w, base_y). Left 60 %: the house with its front wall
    removed — a phone on a sofa, the router on a shelf. Right: the pole with a small ODP box; the drop cable hangs
    from the ODP to the eave and runs along it like a gutter, through the wall, down to the router.
    light 0..1 = pulses in the fiber; loss 0..1 = the pulses after the ODP go weak and flicker.
    screen(c, sx, sy, sw, sh) draws the phone's screen; rain 0..1 = rain seen through the back window.
    Returns rumah_geo(x, base_y, w, h)."""
    col = color or TEAL
    ink2, card = c.theme("ink2", "d_muted"), c.theme("card", "d_card")
    line, faint = c.theme("line", "d_line"), c.theme("faint", "d_line")
    wall = c.theme("ink2", "d_line")
    g = rumah_geo(x, base_y, w, h)
    hx0, hx1, top, th, peak = g["hx0"], g["hx1"], g["top"], g["th"], g["peak"]
    px, odp, eave, router, phone = g["px"], g["odp"], g["eave"], g["router"], g["phone"]
    cable, feeder = g["cable"], g["feeder"]
    with c.group(alpha):
        c.line(x - 40, base_y, x + w + 40, base_y, c.theme("faint", "d_line"), 3)                                  # ground
        # inside: back wall, floor, sofa, shelf
        ix, iy, iw, ih = g["inside"]
        c.fill_rrect(ix, iy, iw, ih, 4, c.theme("bg_warm", "d_card"))
        wx, wy, ww, wh = g["window"]                                                              # back window
        c.fill_rrect(wx, wy, ww, wh, 6, mix(card, c.theme("muted", "d_muted"), 0.18))
        hujan(c, (wx, wy, ww, wh), t, rain, n=16, speed=520, length=22, width=2.0, seed=7)
        c.stroke_rrect(wx, wy, ww, wh, 6, faint, 3)
        c.line(wx + ww / 2, wy, wx + ww / 2, wy + wh, faint, 3)
        c.fill_rrect(phone[0] - w * 0.09, base_y - h * 0.09, w * 0.24, h * 0.09, 10, c.theme("faint", "d_line"))
        c.fill_rrect(phone[0] - w * 0.09, base_y - h * 0.15, w * 0.04, h * 0.15, 8, c.theme("faint", "d_line"))
        c.fill_rrect(router[0] - w * 0.07, router[1] + w * 0.03, w * 0.16, w * 0.012, 3, ink2)   # shelf
        # walls + roof (cut section)
        c.fill_rrect(hx0, top, th, base_y - top, 2, wall)
        c.fill_rrect(hx1 - th, top, th, base_y - top, 2, wall)
        c.fill_rrect(hx0 - w * 0.01, top - th * 0.5, hx1 - hx0 + w * 0.02, th, 2, wall)
        rl, rr = (hx0 - w * 0.05, top + h * 0.01), (hx1 + w * 0.05, top + h * 0.01)
        _poly(c, [rl, peak, rr], c.theme("bg", "d_bg"))                                         # attic (dry)
        _polyline(c, [rl, peak, rr], wall, th * 1.3)
        _polyline(c, [(rr[0] - w * 0.005, rr[1]), (rr[0] + w * 0.012, rr[1] + h * 0.03)], ink2, th * 0.7)  # talang
        # router (front view, small)
        rw, rh = w * 0.1, w * 0.04
        rx, ry = router[0] - rw / 2, router[1] - rh / 2
        for k, ax in enumerate((rx + rw * 0.18, rx + rw * 0.82)):
            with c.at(0, 0, 1, origin=(ax, ry), rot=(-0.15 if k == 0 else 0.15)):
                c.fill_rrect(ax - w * 0.004, ry - rh * 1.1, w * 0.008, rh * 1.12, 3, ink2)
        c.fill_rrect(rx, ry, rw, rh, rh * 0.25, card)
        c.stroke_rrect(rx, ry, rw, rh, rh * 0.25, line, 1.5)
        for k in range(4):
            c.circle(rx + rw * (0.22 + 0.19 * k), ry + rh * 0.55, max(2.0, w * 0.0045), tk.C["ok"], 0.9)
        # phone on the sofa
        pbx, pby, pw, ph = g["phone_box"]
        c.fill_rrect(pbx, pby, pw, ph, pw * 0.16, c.theme("ink", "d_line"))
        sx, sy, sw, sh = pbx + pw * 0.07, pby + pw * 0.07, pw * 0.86, ph - pw * 0.14
        if screen is not None:
            with c.clip(sx, sy, sw, sh, pw * 0.11):
                screen(c, sx, sy, sw, sh)
        else:
            c.fill_rrect(sx, sy, sw, sh, pw * 0.11, card)
        # pole + feeder + ODP
        c.fill_rrect(px - w * 0.009, base_y - h * 0.92, w * 0.018, h * 0.92, 4, c.theme("muted", "d_muted"))
        c.fill_rrect(px - w * 0.05, base_y - h * 0.9, w * 0.1, w * 0.01, 3, c.theme("muted", "d_muted"))
        _polyline(c, feeder, ink2, max(3, w * 0.006))
        _polyline(c, cable, ink2, max(3, w * 0.006))
        ox, oy, ow, oh = odp
        lid = clamp(odp_lid)
        c.fill_rrect(ox, oy, ow, oh, ow * 0.12, c.theme("ink2", "d_line"))
        with c.at(0, 0, 1, origin=(ox - ow * 0.04, oy), rot=-0.25 * lid):
            c.fill_rrect(ox - ow * 0.04, oy - oh * 0.12, ow * 1.08, oh * 0.14, oh * 0.05, c.theme("ink", "d_line"))
        c.text(ox + ow / 2, oy + oh * 0.66, "ODP", tk.F["mono_bold"], max(17, ow * 0.3), WHITE, 0.85, 0.1,
               align="c")
        # light pulses: bright along the feeder, weak (and flickering) after the ODP when loss > 0
        if light > 0.01:
            pr = max(3.0, w * 0.0065)
            for k in range(4):
                f = (t * 0.45 + k / 4) % 1.0
                fx, fy, _ = along(feeder, f)
                c.circle(fx, fy, pr, col, light * min(1, f * 8, (1 - f) * 8))
            fl = 0.5 + 0.5 * math.sin(t * 11.0) * math.sin(t * 4.3)
            k_loss = 1.0 - clamp(loss) * (0.55 + 0.4 * fl)
            for k in range(6):
                f = (t * 0.3 + k / 6) % 1.0
                fx, fy, _ = along(cable, f)
                c.circle(fx, fy, pr, col, light * k_loss * min(1, f * 10, (1 - f) * 10))
    return g
