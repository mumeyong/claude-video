"""Post-office sorting components (first used in "otp-telat").

amplop · belt · loket · hp_otp · log_card · notif
Metaphor: an OTP code is a letter (amplop) passing several post offices (loket) on its way to the phone — server app →
SMS gateway → operator → BTS. Each office has a conveyor (belt) with a queue; the phone (hp_otp) shows the real
"Kirim ulang dalam 0:59" screen whose timer keeps running while the letter waits.
Signature: the letter stops in the queue on the belt while the timer on the phone keeps counting down.
Pure functions of their arguments (belt offset, timer value, progress) — frame = f(t). Colors from tokens.
"""
import math

from .. import tokens as tk
from ..ease import clamp, blink

GREEN = tk.CHAPTER[1][0]             # signature: our letter's stamp + postmarks
C, F = tk.C, tk.F
PW, PH = 600, 1220                   # hp_otp design size (drawn at scale s)


def amplop(c, cx, cy, w, color=None, code="", caps=0.0, alpha=1.0, mine=False):
    """Envelope centred on (cx, cy), width w (height 0.62 w). color = stamp (grey for other people's letters).
    caps = postmarks so far (2.4 → two full rings + a third at 40 %). mine adds a band in color along the left edge."""
    if alpha <= 0.01:
        return
    col = color or C["faint"]
    h = w * 0.62
    x, y = cx - w / 2, cy - h / 2
    r = w * 0.06
    with c.group(alpha):
        c.shadow(x, y, w, h, r, blur=w * 0.16, dy=w * 0.06, alpha=0.10)
        c.fill_rrect(x, y, w, h, r, C["card"])
        c.stroke_rrect(x, y, w, h, r, C["line"], 1.2)
        lw = max(1.2, w * 0.012)
        c.line(x + r, y + r * 0.6, cx, y + h * 0.56, C["faint"], lw)
        c.line(x + w - r, y + r * 0.6, cx, y + h * 0.56, C["faint"], lw)
        if mine:
            c.fill_rrect(x, y, w * 0.05, h, r * 0.5, col)
        sw, sh = w * 0.15, w * 0.18
        sx, sy = x + w - sw - w * 0.07, y + w * 0.07
        c.fill_rrect(sx, sy, sw, sh, w * 0.02, col)
        ctx = c.ctx
        for k in range(int(math.ceil(caps))):
            p = clamp(caps - k)
            if p <= 0:
                continue
            ox, oy = sx - w * (0.08 + 0.13 * k), sy + sh * 0.55 + w * 0.03 * (k % 2)
            c.src(col, 0.85 * min(1.0, p * 2))
            ctx.set_line_width(max(1.2, w * 0.013))
            ctx.new_path()
            ctx.arc(ox, oy, w * 0.085, -math.pi / 2, -math.pi / 2 + 2 * math.pi * p)
            ctx.stroke()
        if code and w * 0.115 >= 17:                         # the code only where it's readable (text ≥ 17 px)
            c.text(x + w * 0.11, y + h - w * 0.09, code, F["mono_bold"], w * 0.115, C["ink2"])


def belt(c, x, y, w, offset, h=44, legs=110, color=None, alpha=1.0):
    """Conveyor whose top surface spans (x, y)–(x + w, y + h); slats shift right with offset (px). Legs below."""
    col = color or C["ink2"]
    with c.group(alpha):
        if legs > 0:
            for lx in (x + w * 0.12, x + w * 0.88):
                c.line(lx, y + h, lx, y + h + legs, C["muted"], 8)
            c.fill_rrect(x + 20, y + h + legs - 6, w - 40, 12, 6, C["line"])
        c.fill_rrect(x, y, w, h, h / 2, col)
        step = 46
        with c.clip(x + h / 2, y, w - h, h):
            k0 = int(-offset // step) - 1
            for k in range(k0, k0 + int(w / step) + 3):
                sx = x + k * step + offset
                c.line(sx, y + 6, sx, y + h - 6, C["card"], 2.0, 0.22)
        for ex in (x + h / 2, x + w - h / 2):
            c.circle(ex, y + h / 2, h * 0.32, C["card"], 0.30)


def loket(c, x, y, w, h, label, sub="", color=None, alpha=1.0, lit=1.0):
    """Post-office counter card: a tinted mail-slot icon, mono label, muted sub line. lit 0..1 tints the icon."""
    col = color or GREEN
    if alpha <= 0.01:
        return
    with c.group(alpha):
        c.card(x, y, w, h, r=tk.L["radius_card"])
        s = min(64, h - 36)
        ix, iy = x + 24, y + (h - s) / 2
        c.fill_rrect(ix, iy, s, s, s * 0.26, C["bg"])
        c.fill_rrect(ix, iy, s, s, s * 0.26, col, 0.16 * lit)
        c.fill_rrect(ix + s * 0.2, iy + s * 0.44, s * 0.6, s * 0.12, s * 0.06, col, 0.35 + 0.65 * lit)
        tx = ix + s + 24
        c.text(tx, y + h / 2 - (4 if sub else -9), label, F["mono_bold"], 26, C["ink"])
        if sub:
            c.text(tx, y + h / 2 + 32, sub, F["ui_reg"], 24, C["muted"])


def _bars(c, x, y, n, color):
    for i in range(4):
        bh = 12 + i * 7
        c.fill_rrect(x + i * 13, y - bh, 9, bh, 3, color, 1.0 if i < n else 0.18)


def hp_otp(c, t, x, y, s, left=59.0, code="", filled=0.0, bars=4.0, detail=1.0, press=1.0, wrong=0.0,
           via="SMS", alpha=1.0):
    """Phone on the OTP screen, top-left (x, y), scale s of a 600 × 1220 design. left = seconds on the resend timer
    (≤ 0 → the blue 'Kirim ulang' link); code + filled (0..6) fill the six boxes; bars 0..4 = signal; detail 0..1
    fades the small print (use it when the phone is drawn small); press = scale of the resend link; wrong 0..1 shows
    the 'kode sudah tidak berlaku' error under the boxes."""
    if alpha <= 0.01:
        return
    with c.group(alpha):
        with c.at(x, y, s, origin=(0, 0)):
            c.shadow(0, 0, PW, PH, 84, blur=70, dy=34, alpha=0.20)
            c.fill_rrect(0, 0, PW, PH, 84, C["ink"])
            c.fill_rrect(16, 16, PW - 32, PH - 32, 70, C["card"])
            c.fill_rrect(PW / 2 - 80, 40, 160, 46, 23, C["ink"])
            nb = int(round(clamp(bars, 0, 4)))
            _bars(c, PW - 122, 86, nb, C["ink"] if nb else C["rec"])
            c.text(70, 82, "12.04", F["ui_semi"], 34, C["ink"], alpha=detail)
            c.text(PW / 2, 250, "Verifikasi", F["display"], 64, C["ink"], align="c")
            c.text(PW / 2, 318, f"Kode dikirim lewat {via} ke", F["ui_reg"], 32, C["muted"], align="c", alpha=detail)
            c.text(PW / 2, 360, "0812 •••• ••21", F["ui_reg"], 32, C["muted"], align="c", alpha=detail)
            bw, gap, by, bh = 72, 14, 430, 96
            bx0 = (PW - (6 * bw + 5 * gap)) / 2
            nf = int(clamp(filled, 0, 6))
            for i in range(6):
                bx = bx0 + i * (bw + gap)
                active = i == nf and wrong < 0.5
                err = wrong > 0 and i < nf
                c.fill_rrect(bx, by, bw, bh, 18, C["bg"])
                c.stroke_rrect(bx, by, bw, bh, 18, C["rec"] if err else (C["accent"] if active else C["faint"]),
                               4 if (active or err) else 2.5, alpha=wrong if err else 1.0)
                if i < nf and i < len(code):
                    c.text(bx + bw / 2, by + 70, code[i], F["display"], 58, C["ink"], align="c")
                if active and blink(t, 1.1):
                    c.fill_rrect(bx + bw / 2 - 2, by + 24, 4, bh - 48, 2, C["accent"])
            if wrong > 0:
                c.text(PW / 2, 596, "Kode sudah tidak berlaku", F["ui_semi"], 34, C["rec"], align="c", alpha=wrong)
            ry = 700
            if left > 0:
                sec = int(math.ceil(left))
                c.text(PW / 2, ry, f"Kirim ulang dalam 0:{sec:02d}", F["ui"], 46, C["muted"], align="c")
            else:
                with c.at(PW / 2, ry - 16, press, origin=(0, 0)):
                    c.text(0, 16, "Kirim ulang", F["ui_semi"], 50, C["accent"], align="c")
            kx0, ky0, kw, kh, kg = 52, 800, 152, 84, 18
            with c.group(detail):
                for r in range(4):
                    for k in range(3):
                        lab = "123456789 0 "[r * 3 + k]
                        if lab == " ":
                            continue
                        kx, ky = kx0 + k * (kw + kg), ky0 + r * (kh + kg)
                        c.fill_rrect(kx, ky, kw, kh, 18, C["bubble"], 0.7)
                        c.text(kx + kw / 2, ky + 58, lab, F["ui"], 42, C["ink"], align="c")
            c.fill_rrect(PW / 2 - 90, PH - 44, 180, 8, 4, C["ink"])


def hp_box(x, y, s):
    """Screen-space anchors of hp_otp at (x, y, s): dict(box, boxes (the 6-digit row), link (the resend line))."""
    return dict(box=(x, y, PW * s, PH * s), boxes=(x + 49 * s, y + 430 * s, 502 * s, 96 * s),
                link=(x + PW / 2 * s, y + 684 * s))


def log_card(c, x, y, w, rows, alpha=1.0, size=28, row_h=64):
    """Dark terminal card with mono rows [(left, right, color)] — server log lines. Returns the row baselines."""
    h = 70 + row_h * len(rows)
    ys = []
    with c.group(alpha):
        c.shadow(x, y, w, h, tk.L["radius_card"], blur=50, dy=24, alpha=0.22)
        c.fill_rrect(x, y, w, h, tk.L["radius_card"], C["d_card"])
        for i, col in enumerate((C["rec"], C["muted"], C["ok"])):
            c.circle(x + 34 + i * 26, y + 32, 7, col, 0.8)
        c.text(x + w - 30, y + 40, "server.log", F["mono"], 20, C["d_muted"], align="r")
        for i, (left, right, col) in enumerate(rows):
            by = y + 70 + row_h * i + row_h * 0.62
            ys.append(by)
            c.text(x + 34, by, left, F["mono"], size, C["d_muted"])
            c.text(x + 34 + w * 0.36, by, right, F["mono_bold"], size, col or C["d_ink"])
    return ys


def notif(c, x, y, w, app, body, color=None, alpha=1.0):
    """iOS-style notification banner (top-left x, y, width w, height 120): app square + name, one body line."""
    if alpha <= 0.01:
        return
    h = 120
    with c.group(alpha):
        c.shadow(x, y, w, h, 30, blur=40, dy=16, alpha=0.14)
        c.fill_rrect(x, y, w, h, 30, C["card"])
        c.fill_rrect(x + 22, y + 26, 68, 68, 18, color or C["wa"])
        c.fill_rrect(x + 40, y + 50, 32, 20, 6, C["card"], 0.9)
        c.text(x + 112, y + 50, app, F["ui_semi"], 26, C["ink"])
        c.text(x + 112, y + 90, body, F["ui_reg"], 26, C["ink2"])
