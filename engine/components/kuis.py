"""Quiz-card components (first used in "interview-cloud-5-pertanyaan", reel look).

flip_card · countdown_ring
Metaphor: a stack of flashcards on an interview desk — one question per card. Signature: a 3-second ring drains
around the card's number, then the card flips over its horizontal axis (top edge toward the camera) and the back
shows what the interviewer is really listening for, in handwriting — not the textbook answer.
Pure functions of their progress values (frame = f(t)); colors from tokens.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, pop

TEAL = tk.CHAPTER[4][0]             # signature: ring, card band, the back of the card
F, C = tk.F, tk.C
PAPER, INK = C["brand_paper"], C["reel_ink"]


def countdown_ring(c, cx, cy, r, p, color=None, n=3, width=None, alpha=1.0, ground=None):
    """Timer ring centred on (cx, cy): the colored arc drains clockwise from 12 o'clock as p goes 0 → 1, the
    digit counts n … 1 (pops on every change) and turns into a ✓ at p = 1. ground = disc fill (default paper)."""
    if alpha <= 0.002:
        return
    color = color or TEAL
    p = clamp(p)
    width = width or max(6.0, r * 0.16)
    cx_ = c.ctx
    c.circle(cx, cy, r + width * 0.5, ground or PAPER, alpha)
    cx_.new_path()
    cx_.arc(cx, cy, r - width * 0.5, 0, 2 * math.pi)
    c.src(mix(color, PAPER, 0.8), alpha)
    cx_.set_line_width(width)
    cx_.stroke()
    if p < 1:
        a0 = -math.pi / 2 + 2 * math.pi * p
        cx_.new_path()
        cx_.arc(cx, cy, r - width * 0.5, a0, 3 * math.pi / 2)
        c.src(color, alpha)
        cx_.stroke()
        for k in range(1, n):                                   # segment ticks
            a = -math.pi / 2 + 2 * math.pi * k / n
            c.circle(cx + math.cos(a) * (r - width * 0.5), cy + math.sin(a) * (r - width * 0.5), width * 0.22,
                     PAPER, alpha)
        d = min(n, int(n * (1 - p)) + 1)
        local = (n * p) % 1.0
        s = pop(clamp(local / 0.35), 2.2) * 0.25 + 0.75 if p > 0 else 1.0
        size = r * 0.95
        with c.at(0, 0, s, origin=(cx, cy)):
            c.text(cx, cy + size * 0.36, str(d), F["mono_bold"], size, INK, alpha, align="c")
    else:
        cx_.new_path()
        cx_.move_to(cx - r * 0.36, cy + r * 0.02)
        cx_.line_to(cx - r * 0.08, cy + r * 0.3)
        cx_.line_to(cx + r * 0.4, cy - r * 0.3)
        c.src(color, alpha)
        cx_.set_line_width(width * 0.9)
        cx_.stroke()


def _wrap_lines(c, text, font, size, maxw, ls=0.0):
    out = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            nxt = (cur + " " + w).strip()
            if cur and c.measure(nxt, font, size, ls)[0] > maxw:
                out.append(cur)
                cur = w
            else:
                cur = nxt
        out.append(cur)
    return out


def _front(c, x, y, w, h, num, question, color, tag, q_size):
    pad = w * 0.08
    c.fill_rrect(x, y, w, h * 0.035, 0, color)                              # index-card band
    for k in range(1, 6):                                                   # faint ruled lines
        ly = y + h * (0.42 + k * 0.1)
        c.line(x + pad, ly, x + w - pad, ly, mix(color, PAPER, 0.85), 2)
    c.text(x + pad, y + h * 0.16, f"{tag} {num}", F["mono_med"], max(18, w * 0.04), mix(INK, PAPER, 0.4), 1, 0.18)
    qs = q_size or h * 0.105
    lines = _wrap_lines(c, question, F["display"], qs, w - 2 * pad, -0.04)
    while len(lines) > 4 and qs > 24:
        qs *= 0.9
        lines = _wrap_lines(c, question, F["display"], qs, w - 2 * pad, -0.04)
    for i, ln in enumerate(lines):
        c.text(x + pad, y + h * 0.3 + qs * (0.8 + i * 1.02), ln, F["display"], qs, INK, 1, -0.04)


def _back(c, x, y, w, h, num, answer, color, tag, a_size, write):
    pad = w * 0.08
    c.fill_rrect(x, y + h - h * 0.035, w, h * 0.035, 0, color)
    c.text(x + pad, y + h * 0.16, f"{tag} · {num}", F["mono_med"], max(18, w * 0.04), color, 1, 0.18)
    s = a_size or h * 0.11
    n = max(1, len(answer))
    yy = y + h * 0.3 + s * 0.8
    for i, ln in enumerate(answer):
        k = clamp(write * n - i)
        if k <= 0:
            break
        size = s
        while size > 22 and c.measure(ln, F["serif"], size)[0] > w - 2 * pad:
            size *= 0.94
        with c.clip(x + pad - 10, yy - size * 1.1, (w - 2 * pad + 20) * k, size * 1.6):
            c.text(x + pad, yy, ln, F["serif"], size, INK, 1)
        yy += s * 1.12


def flip_card(c, cx, cy, w, h, flip=0.0, num="01", question="", answer=(), write=1.0, color=None, tilt=0.0,
              tag="PERTANYAAN", back_tag="YANG AKU CARI", q_size=None, a_size=None, alpha=1.0, front=None,
              back=None):
    """Flashcard centred on (cx, cy), w × h. flip 0 → 1 turns it over its horizontal axis (may overshoot a little on
    a spring — it squashes, never mirrors): front = 'PERTANYAAN 01' + the question (display type on ruled lines),
    back = a tinted face with `answer` lines in serif 'handwriting', revealed left → right by write 0..1.
    front / back(c, x, y, w, h) replace the default faces. tilt = rotation (radians), small values only."""
    if alpha <= 0.002:
        return
    color = color or TEAL
    ang = math.pi * clamp(flip, 0.0, 1.08)
    k = math.cos(ang)
    sy = max(0.02, abs(k))
    lift = 1 + 0.07 * math.sin(min(math.pi, ang))
    x, y = cx - w / 2, cy - h / 2
    r = min(w, h) * 0.05
    cx_ = c.ctx
    with c.group(alpha):
        up = (lift - 1) / 0.07                                              # 0 on the desk … 1 mid-flip
        c.shadow(x + w * 0.04, y + h * (0.5 - 0.5 * sy), w * 0.92, h * sy, r, 34 + 20 * up, 14 + 26 * up,
                 0.08 * (1 - 0.35 * up))
        cx_.save()
        cx_.translate(cx, cy)
        if tilt:
            cx_.rotate(tilt)
        cx_.scale(lift, lift * sy)
        cx_.translate(-cx, -cy)
        is_front = k >= 0
        face = C["card"] if is_front else mix(color, PAPER, 0.86)
        c.fill_rrect(x, y, w, h, r, face)
        c.stroke_rrect(x + 0.5, y + 0.5, w - 1, h - 1, r, C["line"], 1.0)
        if sy > 0.35:                                                       # no squashed type mid-flip
            with c.clip(x, y, w, h, r):
                if is_front:
                    (front or (lambda c_, *b: _front(c_, *b, num, question, color, tag, q_size)))(c, x, y, w, h)
                else:
                    (back or (lambda c_, *b: _back(c_, *b, num, answer, color, back_tag, a_size, write)))(
                        c, x, y, w, h)
        cx_.restore()
