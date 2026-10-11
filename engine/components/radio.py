"""Radio-studio components (first used in "prompt-diproses-di-mana", reel look).

on_air · mic_studio · paku_nota
Metaphor: sending a prompt = sending a request slip to a radio studio across the sea (the data center). The slips
pile up on the announcer's note spike (the queue), the announcer is the GPU, and when it's your turn the ON AIR lamp
lights and the answer is broadcast back live, one token at a time (streaming).
Pure functions of their progress values (frame = f(t)); colors from tokens.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, lerp, out_cubic

ORANGE = tk.CHAPTER[2][0]           # signature: ON AIR lamp, request slips, broadcast waves
F, C = tk.F, tk.C
PAPER, INK = C["brand_paper"], C["reel_ink"]
SLIP = mix(ORANGE, PAPER, 0.84)


def on_air(c, cx, cy, w, on=0.0, label="ON AIR", color=None, alpha=1.0, mount=True):
    """ON AIR box lamp centred on (cx, cy), width w (height 0.34 w). on 0..1 lights the panel (dark glass → color,
    the label from faint to paper). mount draws the wall bracket on top."""
    if alpha <= 0.002:
        return
    color = color or ORANGE
    on = clamp(on)
    h = w * 0.34
    x, y = cx - w / 2, cy - h / 2
    if mount:
        c.line(cx - w * 0.22, y - h * 0.42, cx - w * 0.22, y, mix(INK, PAPER, 0.4), max(3.0, w * 0.018), alpha)
        c.line(cx + w * 0.22, y - h * 0.42, cx + w * 0.22, y, mix(INK, PAPER, 0.4), max(3.0, w * 0.018), alpha)
    c.shadow(x, y, w, h, h * 0.22, 24, 10, 0.08 * alpha)
    c.fill_rrect(x, y, w, h, h * 0.22, INK, alpha)                       # housing
    b = h * 0.12
    c.fill_rrect(x + b, y + b, w - 2 * b, h - 2 * b, h * 0.14, mix(mix(INK, PAPER, 0.18), color, on), alpha)
    if on > 0:                                                            # lit glass: a lighter band on top
        c.fill_rrect(x + b * 1.6, y + b * 1.5, w - 3.2 * b, (h - 2 * b) * 0.28, h * 0.08, mix(color, PAPER, 0.45),
                     alpha * on * 0.6)
    size = h * 0.44
    c.text(cx, cy + size * 0.36, label, F["mono_bold"], size, mix(mix(INK, PAPER, 0.42), PAPER, on), alpha, 0.12,
           align="c")


def mic_studio(c, cx, cy, s, on=0.0, color=None, alpha=1.0, facing=-1):
    """Broadcast microphone (capsule height s) centred on (cx, cy), hanging from a boom arm that reaches down to a
    desk clamp on the `facing` side (−1 = arm to the left). on 0..1 lights the ring around its neck.
    Returns the point in front of the grille where broadcast waves start."""
    if alpha <= 0.002:
        return (cx, cy)
    color = color or ORANGE
    arm = mix(INK, PAPER, 0.3)
    lw = max(4.0, s * 0.06)
    ex, ey = cx + facing * s * 0.95, cy - s * 0.35                       # elbow
    bx, by = cx + facing * s * 1.25, cy + s * 1.15                       # desk clamp
    c.line(cx, cy - s * 0.5, ex, ey, arm, lw, alpha)
    c.line(ex, ey, bx, by, arm, lw, alpha)
    c.circle(ex, ey, lw * 1.1, INK, alpha)
    c.fill_rrect(bx - s * 0.16, by, s * 0.32, s * 0.12, s * 0.03, INK, alpha)
    w = s * 0.42
    c.fill_rrect(cx - w * 0.38, cy + s * 0.32, w * 0.76, s * 0.22, s * 0.04, INK, alpha)          # neck / mount
    c.fill_rrect(cx - w * 0.56, cy + s * 0.22, w * 1.12, s * 0.09, s * 0.04, mix(INK, color, clamp(on)), alpha)
    c.fill_rrect(cx - w / 2, cy - s / 2, w, s * 0.78, w * 0.48, mix(INK, PAPER, 0.12), alpha)   # capsule
    for k in range(5):                                                   # grille
        gy = cy - s * 0.36 + k * s * 0.11
        c.line(cx - w * 0.3, gy, cx + w * 0.3, gy, mix(INK, PAPER, 0.42), max(1.5, s * 0.014), alpha)
    return (cx, cy - s * 0.1)


def slip(c, cx, cy, w, text="", rot=0.0, color=None, alpha=1.0, hole=True):
    """One request slip (w × 0.4 w) centred on (cx, cy): paper with a colored top edge and a mono line of text."""
    if alpha <= 0.002:
        return
    color = color or ORANGE
    h = w * 0.4
    with c.at(0, 0, 1.0, origin=(cx, cy), rot=rot):
        c.shadow(cx - w / 2, cy - h / 2, w, h, 6, 14, 6, 0.07 * alpha)
        c.fill_rrect(cx - w / 2, cy - h / 2, w, h, 6, (1, 1, 1, 1), alpha)
        c.fill_rrect(cx - w / 2, cy - h / 2, w, h * 0.16, 3, color, alpha)
        if text:
            size = max(17.0, min(h * 0.3, 26.0))
            tw = c.measure(text, F["mono_med"], size)[0]
            if tw > w * 0.86:
                size = max(17.0, size * w * 0.86 / tw)
            c.text(cx, cy + h * 0.24, text, F["mono_med"], size, INK, alpha, align="c")
        if hole:
            c.circle(cx, cy - h * 0.02 - (h * 0.18 if text else 0), max(2.5, w * 0.014), mix(INK, PAPER, 0.5), alpha)


def paku_nota(c, cx, base_y, s, slips=(), color=None, alpha=1.0):
    """Note spike (needle height s) standing on base_y with request slips impaled on it.
    slips = [dict(text, p 0..1 slides it down from above the needle, off 0..1 pulls it up and away, rot)], first =
    bottom of the pile. Each slip rests a little above the previous one."""
    if alpha <= 0.002:
        return
    color = color or ORANGE
    sw = s * 1.15
    gap = s * 0.085
    c.fill_rrect(cx - s * 0.36, base_y - s * 0.1, s * 0.72, s * 0.1, s * 0.05, INK, alpha)          # base
    c.line(cx, base_y - s * 0.1, cx, base_y - s, mix(INK, PAPER, 0.35), max(3.0, s * 0.022), alpha)
    top = base_y - s
    for i, d in enumerate(slips):
        p = clamp(d.get("p", 1.0))
        if p <= 0:
            continue
        rest = base_y - s * 0.2 - i * gap
        y = lerp(top - s * 0.45, rest, out_cubic(p))
        off = clamp(d.get("off", 0.0))
        y -= s * 1.6 * off * off
        a = alpha * clamp(p * 3) * (1 - off)
        slip(c, cx, y, sw, d.get("text", ""), d.get("rot", 0.0) * (1 - off), color, a, hole=False)
        if y > top:                                                       # the needle shows through the slip
            c.line(cx, y - sw * 0.2, cx, max(top, y - sw * 0.2 - 2), INK, max(3.0, s * 0.022), a)
    c.circle(cx, top, max(2.5, s * 0.016), INK, alpha)


def airwaves(c, cx, cy, p, r_max, color=None, n=3, a0=-0.5, a1=0.5, width=6, alpha=1.0):
    """Broadcast arcs leaving (cx, cy) toward angle range (a0, a1) radians (0 = right, π/2 = down); p 0..1 spreads
    them out and fades them."""
    if p <= 0 or p >= 1 or alpha <= 0.002:
        return
    color = color or ORANGE
    cx_ = c.ctx
    for k in range(n):
        pk = clamp((p - k * 0.16) / 0.68)
        if pk <= 0 or pk >= 1:
            continue
        r = lerp(18, r_max, out_cubic(pk))
        cx_.new_path()
        cx_.arc(cx, cy, r, a0, a1)
        c.src(color, alpha * (1 - pk))
        cx_.set_line_width(width * (1 - 0.5 * pk))
        cx_.stroke()


def data_center(c, x, y, w, h, t=0.0, lamp=0.0, color=None, alpha=1.0, label="DATA CENTER", roof=True):
    """Flat windowless data-center block (x, y, w, h) with rows of rack vents, a small ON AIR lamp on the roof
    (lamp 0..1, roof=False leaves it off) and a mono label. Returns the lamp centre."""
    if alpha <= 0.002:
        return (x + w / 2, y)
    c.shadow(x, y, w, h, 14, 26, 10, 0.08 * alpha)
    c.fill_rrect(x, y, w, h, 14, (1, 1, 1, 1), alpha)
    c.stroke_rrect(x, y, w, h, 14, mix(INK, PAPER, 0.75), 2, alpha)
    rows, cols = 5, 3
    pad = w * 0.1
    cw = (w - pad * (cols + 1)) / cols
    rh = (h * 0.62 - pad) / rows
    for r in range(rows):
        for k in range(cols):
            vx, vy = x + pad + k * (cw + pad), y + h * 0.3 + r * rh
            c.fill_rrect(vx, vy, cw, rh * 0.55, 4, mix(INK, PAPER, 0.88), alpha)
            led = 0.5 + 0.5 * math.sin(t * (2.1 + 0.37 * ((r * 3 + k) % 5)) + r * 1.7 + k)
            c.circle(vx + cw - 9, vy + rh * 0.275, 3.5, mix(mix(INK, PAPER, 0.6), C["reel_green"], led), alpha)
    c.text(x + w / 2, y + h * 0.2, label, F["mono_med"], max(17.0, min(22.0, w * 0.085)), mix(INK, PAPER, 0.3),
           alpha, 0.14, align="c")
    lx, ly = x + w / 2, y - w * 0.17
    if roof:
        on_air(c, lx, ly, w * 0.62, lamp, color=color, alpha=alpha, mount=False)
    return (lx, ly)
