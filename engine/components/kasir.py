"""Cashier-receipt components (first used in "ai-gratis-siapa-bayar").

struk · struk_h · stempel · saklar
Metaphor: every free AI answer is a line on a thermal receipt that totals Rp0 — turn the receipt over and the back is
full: the real bill (GPU, per hour, electricity) is addressed to someone else (subscription, investor, ads, data).
Signature: the receipt turns over on its vertical axis (flip 0 → 1, a fake-3D yaw), the back side's rows get stamped.
Pure functions of their progress values (frame = f(t)). The paper stays white and its print stays dark in the dark
section too — it is a physical object, not UI. Colors from tokens; shading via material (look="flat" | "paper").
"""
import math
from contextlib import nullcontext

from .. import tokens as tk
from ..ease import clamp, lerp, mix, out_cubic
from . import material as mat
from .keynote import yaw

GREEN = tk.CHAPTER[1][0]             # signature: stamps, the real-cost rows, the switch when on
PAPER = tk.C["card"]
INK = tk.C["brand_ink"]               # thermal print
F = tk.F


def _dims(w):
    f = w / 600
    return dict(f=f, pad=44 * f, head=160 * f, row=60 * f, total=140 * f, foot=74 * f, zig=16 * f)


def struk_h(side, w):
    """Height (without the torn edge) of a struk side drawn at width w — rows count by their g (0..1)."""
    d = _dims(w)
    rows = sum(clamp(r.get("g", 1.0)) for r in side.get("rows", ()))
    return d["head"] + d["row"] * rows + (d["total"] if side.get("total") else 0) + (d["foot"] if side.get("foot")
                                                                                     else 0)


def _dash(c, x0, x1, y, f, alpha):
    c.ctx.save()
    c.ctx.set_dash([10 * f, 8 * f])
    c.line(x0, y, x1, y, INK, max(1.5, 2 * f), 0.35 * alpha)
    c.ctx.restore()


def stempel(c, cx, cy, text, p, color=None, size=40, rot=-0.14, alpha=1.0):
    """Rubber stamp centred on (cx, cy): rounded frame + mono-bold text. p 0..1 presses it on (1.12 → 1, opacity
    first) — quiet, no slam. Use an iOS spring for p (ios_at(t, t0, "snappy"))."""
    if p <= 0.002 or alpha <= 0.002:
        return
    color = color or GREEN
    tw = c.measure(text, F["mono_bold"], size, 0.08)[0]
    w, h = tw + size * 1.3, size * 1.75
    s = lerp(1.12, 1.0, clamp(p))
    with c.at(0, 0, s, origin=(cx, cy), rot=rot):
        with c.group(clamp(p * 2.5) * 0.9 * alpha):
            c.stroke_rrect(cx - w / 2, cy - h / 2, w, h, size * 0.28, color, max(3.0, size * 0.1))
            c.text(cx, cy + size * 0.36, text, F["mono_bold"], size, color, 1, 0.08, align="c")


def _side(c, x, y, w, side, color, alpha):
    """One printed face of the receipt (paper already drawn). Returns row centres + total centre."""
    d = _dims(w)
    f, pad = d["f"], d["pad"]
    muted = mix(INK, PAPER, 0.5)
    c.text(x + w / 2, y + 70 * f, side.get("title", ""), F["mono_bold"], 30 * f, INK, alpha, 0.14, align="c")
    if side.get("sub"):
        c.text(x + w / 2, y + 108 * f, side["sub"], F["mono"], 21 * f, muted, alpha, 0.04, align="c")
    _dash(c, x + pad, x + w - pad, y + 140 * f, f, alpha)
    ys, yy = [], y + d["head"]
    for r in side.get("rows", ()):
        g = clamp(r.get("g", 1.0))
        rh = d["row"] * g
        cy = yy + rh / 2
        ys.append(cy)
        a = clamp(r.get("a", 1.0)) * alpha
        col = r.get("color") or INK
        if r.get("hi", 0) > 0.002:
            hw = (w - 2 * pad + 24 * f) * out_cubic(clamp(r["hi"]))
            c.fill_rrect(x + pad - 12 * f, cy - 24 * f, hw, 48 * f, 10 * f, mix(PAPER, color, 0.16), alpha)
        base = cy + 9 * f
        if r.get("ph") and a < 0.998 * alpha and g > 0.3:              # dotted placeholder until the row inks in
            c.text(x + pad, base, r["ph"], F["mono"], 26 * f, muted, alpha * (1 - a / max(alpha, 1e-3)), 0.0)
        if a > 0.002 and g > 0.3:
            if r.get("kind") == "head":
                c.text(x + pad, base, r["l"], F["mono_bold"], 20 * f, col, a, 0.18)
            else:
                c.text(x + pad, base, r["l"], F["mono"], 26 * f, col, a, 0.0)
                if r.get("r"):
                    c.text(x + w - pad, base, r["r"], F["mono_med"], 26 * f, col, a, 0.0, align="r")
            st = clamp(r.get("strike", 0))
            if st > 0 and r.get("r"):
                rw = c.measure(r["r"], F["mono_med"], 26 * f)[0]
                c.line(x + w - pad - rw - 6 * f, cy, x + w - pad - rw - 6 * f + (rw + 12 * f) * st, cy,
                       tk.C["accent"], max(2.5, 4 * f), alpha)
        if r.get("stamp", 0) > 0.002:
            stempel(c, x + w * 0.66, cy, r.get("stamp_text", "✓"), r["stamp"], color, 22 * f,
                    rot=-0.1 + 0.05 * math.sin(len(ys) * 2.3), alpha=alpha)
        yy += rh
    tot = side.get("total")
    ty = None
    if tot:
        _dash(c, x + pad, x + w - pad, yy + 22 * f, f, alpha)
        ty = yy + 84 * f
        a = clamp(tot.get("a", 1.0)) * alpha
        col = tot.get("color") or INK
        c.text(x + pad, ty + 12 * f, tot.get("l", "TOTAL"), F["mono_bold"], 28 * f, col, a, 0.12)
        vw = c.text(x + w - pad, ty + 22 * f, tot.get("r", ""), F["display"], 64 * f, col, a, -0.04, align="r")
        st = clamp(tot.get("strike", 0))
        if st > 0:
            c.line(x + w - pad - vw - 10 * f, ty + 2 * f, x + w - pad - vw - 10 * f + (vw + 20 * f) * st, ty + 2 * f,
                   tk.C["accent"], max(3.0, 7 * f), alpha)
        yy += d["total"]
    if side.get("foot"):
        c.text(x + w / 2, yy + 44 * f, side["foot"], F["mono"], 20 * f, muted, alpha, 0.06, align="c")
    return ys, ty


def struk(c, x, y, w, front, back=None, flip=0.0, feed=1.0, look="flat", color=None, alpha=1.0):
    """Thermal receipt, top-left (x, y), width w; height follows the rows (struk_h). Straight top (the printer
    cut), torn zigzag bottom. A side = dict(title, sub, rows=[dict(l, r, a, g, color, strike, stamp, stamp_text,
    hi, ph, kind="head"|None)], total=dict(l, r, a, strike, color), foot). a = ink 0..1, g = row height 0..1 (the
    receipt lengthens as rows print), hi = highlight bar, ph = placeholder text shown until the row inks in.
    flip 0..1 turns it over on its vertical axis (front → back; the side facing the camera is drawn).
    feed 0..1 = how far it has come out of a printer slot at its bottom edge (the top line prints first).
    Returns dict(h, rows=[row centre y], total=y of the total line) for the side facing the camera."""
    if alpha <= 0.002:
        return dict(h=0, rows=[], total=None)
    color = color or GREEN
    ang = math.pi * clamp(flip)
    side = front if (back is None or math.cos(ang) >= 0) else back
    a_eff = ang if side is front else ang - math.pi
    d = _dims(w)
    h = struk_h(side, w)
    z = d["zig"]
    n = max(6, int(w / (26 * d["f"])))
    pts = [(x, y), (x + w, y), (x + w, y + h)]
    for k in range(1, n + 1):
        pts.append((x + w - w * k / n + w / (2 * n), y + h + z))
        pts.append((x + w - w * k / n, y + h))
    pts.append((x, y + h))
    drop = (h + z + 30) * (1 - clamp(feed))
    out = dict(h=h, rows=[], total=None)
    with c.group(alpha):
        slot = c.clip(x - w, y - 3 * h, 3 * w, 4 * h + z + 2) if feed < 0.999 else nullcontext()
        with slot:
            with yaw(c, x + w / 2, y + h / 2, a_eff):
                with c.at(0, drop):
                    if look == "flat":
                        c.shadow(x, y, w, h, 6, 30, 12, 0.08)
                    mat.body(c, look, mat.poly_path(pts), (x, y, w, h + z), PAPER, r=4, lift=0.6)
                    turn = abs(math.sin(a_eff))
                    ys, ty = _side(c, x, y, w, side, color, 1.0 - 0.6 * turn)
                    if turn > 0.01:                                      # the edge-on face catches a little shade
                        c.fill_rrect(x, y, w, h + z, 0, INK, 0.12 * turn)
                    out.update(rows=[yy + drop for yy in ys], total=None if ty is None else ty + drop)
    return out


def saklar(c, x, y, w, on=0.0, color=None, alpha=1.0):
    """iOS-style toggle, top-left (x, y), width w (height 0.6 w). on 0..1 slides the knob right and fills the track
    with color (feed it an iOS spring: ios_at(t, t0, "snappy"))."""
    if alpha <= 0.002:
        return
    color = color or GREEN
    h = w * 0.6
    on_ = clamp(on)
    c.fill_rrect(x, y, w, h, h / 2, mix(tk.C["faint"], color, on_), alpha)
    kr = h / 2 - max(3.0, w * 0.035)
    kx = lerp(x + h / 2, x + w - h / 2, on)
    c.shadow(kx - kr, y + h / 2 - kr, 2 * kr, 2 * kr, kr, 8, 3, 0.12 * alpha)
    c.circle(kx, y + h / 2, kr, tk.C["card"], alpha)
