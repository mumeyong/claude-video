"""Ticket-war / queue components (first used in "war-tiket-crash").

big_clock · print_slip · dispenser · loket · refresh_icon · refresh_storm
Signature move they share: a paper slip comes out of a slot (error slip, queue number).
Pure functions of their progress values and t; all variation is hash-seeded.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, glide, pop
from .infra import _h

GREEN = tk.CHAPTER[1][0]
WHITE = (1, 1, 1, 1)


# ── big clock ───────────────────────────────────────────────────────────
def big_clock(c, x, y, text, size, prev=None, jump=1.0, color=None, accent_from=None, align="l"):
    """Digital clock text 'HH:MM:SS' with baseline y. Characters that differ from `prev` drop in from above
    (jump 0..1) while the old ones fall out below — the 'second jumps' move. accent_from: index from which the
    characters take `color` (e.g. 6 = the seconds). Returns width."""
    font = tk.F["mono_bold"]
    ls = -0.02
    color = color or GREEN
    ink = c.theme("ink", "d_ink")
    cw = c.measure("0", font, size, ls)[0]
    total = cw * len(text)
    if align == "c":
        x -= total / 2
    elif align == "r":
        x -= total
    e = glide(clamp(jump))
    with c.clip(x - 10, y - size * 0.95, total + 20, size * 1.15):
        for i, ch in enumerate(text):
            col = color if accent_from is not None and i >= accent_from else ink
            cx = x + i * cw
            old = prev[i] if prev and i < len(prev) else ch
            if old != ch and e < 1:
                c.text(cx, y + size * 1.0 * e, old, font, size, col, 1 - e, ls)
                c.text(cx, y - size * 1.0 * (1 - e), ch, font, size, col, e, ls)
            else:
                c.text(cx, y, ch, font, size, col, 1, ls)
    return total


# ── paper slip out of a slot (signature move) ───────────────────────────
def print_slip(c, x, y, w, h, p, lines, color=None, rot=0.0, slot=True):
    """Slip feeding out of a slot whose top edge is at (x, y), width w; full length h at p=1.
    lines: [(text, font_key, size, color or None)] laid out top→bottom; they show as the paper passes the slot.
    Returns the visible paper rect."""
    color = color or GREEN
    if slot:
        c.fill_rrect(x - 14, y - 6, w + 28, 12, 6, c.theme("ink", "d_ink"), 0.85)
    if p <= 0:
        return (x, y, w, 0)
    L = h * glide(clamp(p))
    with c.at(0, 0, 1.0, origin=(x + w / 2, y), rot=rot * clamp(p)):
        with c.clip(x - 40, y, w + 80, L + 40):
            top = y + L - h          # the paper slides down: its own top is still inside the slot
            c.shadow(x, top, w, h, 4, 14, 6, 0.10)
            cx_ = c.ctx
            cx_.new_path()
            cx_.move_to(x, top)
            cx_.line_to(x + w, top)
            cx_.line_to(x + w, top + h - 10)
            n = 9
            for k in range(n):
                cx_.line_to(x + w - (k + 0.5) * w / n, top + h - 10 * (0.2 + 0.8 * _h(k, 2)))
                cx_.line_to(x + w - (k + 1) * w / n, top + h - 10)
            cx_.close_path()
            c.src(c.theme("card", "d_card"))
            cx_.fill()
            c.fill_rrect(x, top + 8, w, 6, 2, color, 0.9)
            ly = top + 30
            for text, fk, size, col in lines:
                ly += size * 1.1
                c.text(x + w / 2, ly, text, tk.F[fk], size, col or c.theme("ink", "d_ink"), 1, 0.02, align="c")
                ly += size * 0.35
    return (x, y, w, L)


# ── queue number machine ────────────────────────────────────────────────
def dispenser(c, cx, y, s, t, serving="", serving_prev=None, jump=1.0, called=0.0, press=0.0, color=None):
    """Queue-number machine (kantor pos), top center (cx, y), width s, height ≈ 1.45 s.
    Display 'SEKARANG MELAYANI' + LED number (digits drop in with jump), a big round button, and a ticket slot.
    called 0..1 lights the green 'DIPANGGIL' lamp. Returns the slot (x, y, w) for print_slip."""
    color = color or GREEN
    w, h = s, s * 1.45
    x = cx - w / 2
    ink = c.theme("ink", "d_ink")
    body = c.theme("card", "d_card")
    c.shadow(x, y, w, h, s * 0.1, 34, 14, 0.12)
    c.fill_rrect(x, y, w, h, s * 0.1, body)
    c.stroke_rrect(x, y, w, h, s * 0.1, c.theme("line", "d_line"), 1.5)
    c.fill_rrect(x, y, w, s * 0.1, s * 0.05, color)
    # display
    dx, dy, dw, dh = x + w * 0.08, y + s * 0.18, w * 0.84, s * 0.42
    c.fill_rrect(dx, dy, dw, dh, s * 0.04, mix(ink, (0, 0, 0, 1), 0.4))
    c.text(cx, dy + dh * 0.26, "SEKARANG MELAYANI", tk.F["mono_bold"], max(17, s * 0.045), mix(color, WHITE, 0.3), 0.9,
           0.14, align="c")
    if serving:
        big_clock(c, cx, dy + dh * 0.82, serving, s * 0.16, prev=serving_prev, jump=jump, color=color, accent_from=0,
                  align="c")
    # called lamp
    lx, ly = x + w * 0.88, y + s * 0.05
    if called > 0:
        c.shadow(lx - 22, ly - 22 + s * 0.05, 44, 44, 22, 26, 0, 0.5 * clamp(called), color)
    c.circle(lx, ly + s * 0.05, s * 0.035, mix(c.theme("faint", "d_line"), color, clamp(called)))
    # button
    bx, by, br = cx, y + s * 0.86, s * 0.14
    pr = clamp(press)
    c.circle(bx, by + 4, br, mix(color, (0, 0, 0, 1), 0.3))
    c.circle(bx, by + 4 * pr, br, color)
    c.text(bx, by + 4 * pr + s * 0.025, "AMBIL", tk.F["mono_bold"], max(17, s * 0.05), WHITE, 1, 0.1, align="c")
    c.text(cx, by + br + s * 0.1, "nomor antrean", tk.F["mono_med"], max(17, s * 0.04), c.theme("muted", "d_muted"), 1,
           0.08, align="c")
    sw = w * 0.56
    sy = y + h - s * 0.12
    return (cx - sw / 2, sy, sw)


# ── service window (loket) = server ─────────────────────────────────────
def loket(c, x, y, w, h, t, full=0.0, label="", seed=0, color=None, alpha=1.0, busy=1.0):
    """Counter window: frame, glass with a clerk, lamp on top (green → red when full), label plate, slip slot.
    full 0..1 turns the lamp red and shows a 'PENUH' plate. Returns the slot (x, y, w) for print_slip."""
    if alpha <= 0.002:
        return (x + w * 0.2, y + h, w * 0.6)
    color = color or GREEN
    red = tk.C["rec"]
    ink2 = c.theme("ink2", "d_muted")
    with c.group(alpha):
        c.shadow(x, y, w, h, 14, 24, 10, 0.10)
        c.fill_rrect(x, y, w, h, 14, c.theme("card", "d_card"))
        c.stroke_rrect(x, y, w, h, 14, c.theme("line", "d_line"), 1.5)
        gx, gy, gw, gh = x + w * 0.12, y + h * 0.22, w * 0.76, h * 0.5
        c.fill_rrect(gx, gy, gw, gh, 8, mix(c.theme("bg", "d_bg"), color, 0.08))
        # clerk (head + shoulders), works faster when busy
        bob = 3 * math.sin(t * (3 + 5 * busy) + seed)
        c.circle(gx + gw / 2, gy + gh * 0.45 + bob, gh * 0.16, ink2)
        c.fill_rrect(gx + gw * 0.28, gy + gh * 0.66 + bob, gw * 0.44, gh * 0.4, gh * 0.12, ink2)
        c.line(gx, gy + gh * 0.5, gx + gw, gy + gh * 0.5, WHITE, 2, 0.35)
        lamp = mix(color, red, clamp(full))
        lx, ly = x + w / 2, y + h * 0.1
        blink = 1.0 if full < 0.5 else 0.6 + 0.4 * (1 if (t * 3 + seed * 0.3) % 1 < 0.6 else 0)
        c.shadow(lx - 18, ly - 18, 36, 36, 18, 18, 0, 0.35 * blink, lamp)
        c.circle(lx, ly, max(8, w * 0.05), lamp, blink)
        if label:
            c.text(x + w / 2, y + h * 0.86, label, tk.F["mono_bold"], max(17, w * 0.085), ink2, 1, 0.1, align="c")
        if full > 0:
            pa = pop(clamp(full), 1.6)
            with c.at(0, 0, max(0.01, pa), origin=(gx + gw / 2, gy + gh / 2)):
                c.fill_rrect(gx + gw * 0.1, gy + gh * 0.32, gw * 0.8, gh * 0.36, 6, red, clamp(full * 2))
                c.text(gx + gw / 2, gy + gh * 0.58, "PENUH", tk.F["mono_bold"], max(17, gw * 0.15), WHITE,
                       clamp(full * 2), 0.12, align="c")
    return (x + w * 0.2, y + h, w * 0.6)


# ── refresh storm ───────────────────────────────────────────────────────
def refresh_icon(c, x, y, s, color, rot=0.0, alpha=1.0, width=None):
    """↻ : open circular arrow, centered (x, y), diameter s."""
    if alpha <= 0.002:
        return
    r = s / 2
    lw = width or max(2.0, s * 0.12)
    a0, a1 = rot + 0.5, rot + 0.5 + 2 * math.pi * 0.8
    cx_ = c.ctx
    cx_.new_path()
    cx_.arc(x, y, r, a0, a1)
    c.src(color, alpha)
    cx_.set_line_width(lw)
    cx_.set_line_cap(1)
    cx_.stroke()
    hx, hy = x + r * math.cos(a1), y + r * math.sin(a1)
    tang = a1 + math.pi / 2
    for da in (2.5, -2.5):
        cx_.new_path()
        cx_.move_to(hx, hy)
        cx_.line_to(hx + r * 0.6 * math.cos(tang + da), hy + r * 0.6 * math.sin(tang + da))
        cx_.stroke()


def refresh_storm(c, cx, cy, rx, ry, t, n=24, amount=1.0, speed=0.25, size=(26, 54), seed=1, color=None, alpha=1.0,
                  inward=0.0):
    """↻ icons swirling on an elliptical band around (cx, cy). amount 0..1 = share of the n icons present
    (each pops in at its own threshold — 'beranak'). inward 0..1 pulls them toward the center (the attack)."""
    color = color or tk.C["rec"]
    for i in range(n):
        thr = i / n
        a = clamp((amount - thr) * n * 0.6)
        if a <= 0:
            continue
        u = _h(i, seed)
        ang = 2 * math.pi * u + t * speed * (0.6 + 0.8 * _h(i, seed + 1)) * (1 if i % 2 else -1)
        k = (0.55 + 0.45 * _h(i, seed + 2)) * (1 - 0.45 * clamp(inward) * (0.5 + 0.5 * math.sin(t * 3 + i)))
        x, y = cx + rx * k * math.cos(ang), cy + ry * k * math.sin(ang)
        s = size[0] + (size[1] - size[0]) * _h(i, seed + 3)
        pk = pop(a, 1.8)
        refresh_icon(c, x, y, s * pk, color, rot=t * (2 + 3 * _h(i, seed + 4)), alpha=a * alpha * 0.9)
