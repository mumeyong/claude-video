"""Craft lab — proof sheet for STYLE §6f "craft v2" (components/craft.py). Not for posting.

One new move per chapter, each used the way a video should use it: draw_on + mark (a connector that draws itself
between two real cards, then a hand ring), split_rise (mask rise per word from the centre, then per char for one
punch word), count_up (two tabular numbers as one chord), morph_path (circle → drop → card, one continuous shape),
path_at + shutter (a packet follows its route; only the fast whip gets motion blur), carry + rack_cut (the two seams).
Run `check craft-lab --dry`: the motion table should be flag-free.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, curve, lerp
from engine.components import (Headline, kicker, fade, pop_tag, brand_intro, arrive, follow, rise, dolly, cut,
                               presence, draw_on, mark, split_rise, count_up, morph_path, path_at, shutter, carry,
                               rack_cut, pts_bezier, pts_circle, pts_rrect, stroke_partial)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 2.6
NAMES = ("INTRO", "01 · GARIS", "02 · TEKS", "03 · ANGKA", "04 · BENTUK", "05 · JALUR", "06 · SAMBUNGAN", "OUTRO")
D = F["display"]


def _w(T, lid, word, frac):
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


def build(project):
    T = project.timing
    v = Video(duration=T["L14"].end + TAIL, bpm=84, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="lofi", key="A", mood="dreamy")
    v.sfx_kit = "glass"
    b = [max(0.0, T.chapter_span(n)[0] - LEAD) for n in NAMES] + [v.duration]
    b[0] = 0.0
    fns = (intro, garis, teks, angka, bentuk, jalur, sambungan, outro)
    for i, fn in enumerate(fns):
        v.chapter(i if 0 < i < 7 else None, NAMES[i].split(" · ")[-1], b[i], b[i + 1])
        fn(v, T, b[i], b[i + 1], tk.CHAPTER[i][0] if 0 < i < 7 else C["accent"])
        if i:
            cut(v, b[i])
    v.cover_t = _w(T, "L09", "kartu", 0.7) + 1.0
    return v


def _tag(c, t, t_in, t_out, x, y, text, col):
    fade(c, t, t_in, t_out, lambda c: pop_tag(c, t, t_in, x, y, text, col))


# ── INTRO: split_rise by line + a hand underline that draws itself under the accent word ─────────────────────────
def intro(v, T, s, e, col):
    t_in = arrive(T["L01"].start + 0.2)
    t_mark = _w(T, "L01", "desainer", 0.85)
    size = tk.T["headline_lg"][0]

    def draw(c, t):
        kicker(c, t, s + 0.3, e - OUT, "CRAFT LAB · STYLE §6f v2", col)
        split_rise(c, t, t_in, e - OUT, X, 820, "Gerak kayak\n*desainer*.", D, size, C["ink"], by="line",
                   accent=col, ls=-0.06, line_h=0.98)
        w = c.measure("desainer.", D, size, -0.06)[0]
        mark(c, t, t_mark, "underline", (X, 820 + size * 0.98 - size * 0.72, w, size * 0.72), col, 7,
             t_out=e - OUT, seed=2)
    v.add(s, e, draw)
    v.sfx("pop", t_mark)
    dolly(v, t_mark + 0.9, e - 0.2)


# ── 01 · GARIS: two real cards, a connector draws between them, then a hand ring around the target ─────────────────
def garis(v, T, s, e, col):
    head = Headline("Garis yang\n*ngegambar*.")
    a = (X, 760, 330, 210)
    bx = (X + CW - 330 - 40, 1180, 330, 210)
    t_cards = T["L02"].start
    t_draw = arrive(_w(T, "L02", "ngegambar", 0.4), "smooth", 0.5)
    t_ring = _w(T, "L03", "dilingkarin", 0.8)
    path = pts_bezier((a[0] + a[2] * 0.5, a[1] + a[3]), (a[0] + a[2] * 0.5, 1120),
                      (bx[0] + bx[2] * 0.5, 1000), (bx[0] + bx[2] * 0.5, bx[1]), 60)

    def card(c, box, label):
        c.card(*box, r=L["radius_bento"])
        c.text(box[0] + 34, box[1] + box[3] - 40, label, D, 52, C["ink"], 1, -0.04)
        c.text(box[0] + 36, box[1] + 56, "NODE", F["mono_med"], 24, C["ink2"], 1, 0.12)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "01 · DRAW ON", col)
        head.draw(c, t, T["L02"].start - 0.1, e - OUT, reveal="rise", exit="quiet")
        rise(c, t, t_cards, e - OUT, a, lambda c: card(c, a, "titik A"))
        rise(c, t, follow(t_cards, 1), e - OUT, bx, lambda c: card(c, bx, "titik B"))
        draw_on(c, t, t_draw, path, col, 6, dur=0.8, t_out=e - OUT)
        mark(c, t, t_ring, "circle", bx, col, 6, dur=0.7, t_out=e - OUT, seed=5)
    v.add(s, e, draw)
    v.sfx("whoosh", t_draw, 0.4)
    v.sfx("pop", t_ring + 0.5)
    dolly(v, t_draw + 1.0, T["L03"].start - 0.1)
    dolly(v, t_ring + 0.9, e - 0.2)


# ── 02 · TEKS: per word from the centre, then ONE punch word per char ────────────────────────────────────────────
def teks(v, T, s, e, col):
    t1 = arrive(_w(T, "L04", "mask", 0.5), "smooth", 0.3)
    t1_out = T["L05"].start - 0.35
    t2 = arrive(_w(T, "L05", "huruf", 0.85), "smooth", 0.2)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · SPLIT TEXT", col)
        split_rise(c, t, t1, t1_out, X, 820, "Naik dari\nbalik *mask*.", D, 112, C["ink"], by="word",
                   order="center", accent=col, ls=-0.055)
        split_rise(c, t, t2, e - OUT, X, 1060, "huruf.", D, tk.T["giga"][0], col, by="char", ls=-0.065)
    v.add(s, e, draw)
    v.sfx("pop", t1 + 0.3)
    v.sfx("thud", t2 + 0.25)
    dolly(v, t1 + 1.0, t1_out - 0.2)
    dolly(v, t2 + 1.0, e - 0.2)


# ── 03 · ANGKA: two tabular counts on one beat (a chord), suffix after the land ─────────────────────────────────────
def angka(v, T, s, e, col):
    head = Headline("Ngitung,\nnggak *goyang*.")
    t0 = arrive(_w(T, "L06", "ngitung", 0.3), "smooth", 0.3)
    t_tag = _w(T, "L07", "ketukan", 0.8)
    boxes = [(X, 760, CW, 300), (X, 1100, CW, 300)]

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "03 · COUNT UP", col)
        head.draw(c, t, T["L06"].start - 0.1, e - OUT, reveal="rise", exit="quiet")
        for i, (bx, (v1, dec, suf, lab)) in enumerate(zip(boxes, ((2951, 0, "user", "USER BARENGAN"),
                                                                  (44.4, 1, "s", "WAKTU VIDEO")))):
            rise(c, t, follow(t0 - 0.4, i), e - OUT, bx, lambda c, bx=bx, lab=lab: (
                c.card(*bx, r=L["radius_bento"]),
                c.text(bx[0] + 50, bx[1] + 70, lab, F["mono_med"], 26, C["ink2"], 1, 0.12)))
            _, op = presence(t, follow(t0 - 0.4, i), e - OUT)
            with c.group(op):
                count_up(c, t, t0, bx[0] + 46, bx[1] + 240, 0, v1, D, 150, C["ink"], decimals=dec, suffix=suf,
                         suffix_color=col)
        _tag(c, t, t_tag, e - OUT, X, 1470, "satu ketukan · satu kurva", col)
    v.add(s, e, draw)
    v.sfx("tick", t0)
    v.sfx("pop", t_tag)
    dolly(v, t0 + M["count_dur"] + 0.3, e - 0.2)


# ── 04 · BENTUK: circle → drop → card, one continuous shape ─────────────────────────────────────────────────────────
def _drop(cx, cy, r, n=128):
    return [(cx + r * 0.95 * math.sin(a) * math.sin(a / 2), cy - r * 1.1 * math.cos(a)) for a in
            (2 * math.pi * i / n for i in range(n + 1))]


def bentuk(v, T, s, e, col):
    head = Headline("Satu bentuk,\n*berubah*.")
    cx, cy = MID, 1080
    circle = pts_circle(cx, cy, 230, 128)
    drop = _drop(cx, cy, 260)
    card = pts_rrect(X, cy - 260, CW, 520, L["radius_bento"])
    t_in = T["L08"].start
    t_drop = arrive(_w(T, "L08", "berubah", 0.3), "smooth", 0.5)
    t_card = arrive(_w(T, "L09", "kartu", 0.4), "smooth", 0.5)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "04 · MORPH", col)
        head.draw(c, t, T["L08"].start - 0.1, e - OUT, reveal="rise", exit="quiet")
        op = 1 - curve("apple_in")(prog(t, e - OUT, OUT))     # the shape hard-cuts in with the chapter
        if t < t_card:
            morph_path(c, t, t_drop, circle, drop, col, dur=0.75, alpha=op)
        else:
            morph_path(c, t, t_card, drop, card, col, dur=0.75, alpha=op)
        fade(c, t, t_card + 0.55, e - OUT, lambda c: c.text(
            X + 60, cy + 200, "kartu.", D, 96, C["card"], 1, -0.05))
    v.add(s, e, draw)
    v.sfx("whoosh", t_drop, 0.4)
    v.sfx("whoosh", t_card, 0.4)
    dolly(v, t_card + 1.2, e - 0.2, y=cy)


# ── 05 · JALUR: the packet follows its route (trail draws behind it); only the fast whip gets real motion blur ─────
def jalur(v, T, s, e, col):
    head = Headline("Ikut\n*jalurnya*.")
    route = pts_bezier((X + 40, 1500), (X + 120, 820), (X + CW - 120, 1500), (X + CW - 40, 800), 80)
    t_go = arrive(_w(T, "L10", "jalurnya", 0.6), "smooth", 0.3)
    go_dur = 1.15
    t_whip = _w(T, "L11", "blur", 0.85) - 0.2
    whip = 0.38

    def packet(c):
        c.fill_rrect(-34, -22, 68, 44, 12, col)
        c.circle(20, 0, 6, C["card"])

    def chip_at(c, tt):
        u = curve("apple_in_out")(prog(tt, t_whip, whip))
        c.fill_rrect(lerp(X, X + CW - 200, u), 640, 200, 64, 32, C["ink"])

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "05 · MOTION PATH", col)
        head.draw(c, t, T["L10"].start - 0.1, e - OUT, reveal="rise", exit="quiet")
        op = 1 - curve("apple_in")(prog(t, e - OUT, OUT))     # the route hard-cuts in; only the packet moves
        with c.group(op):
            stroke_partial(c, route, 1.0, C["line"], 4)
            path_at(c, t, t_go, go_dur, route, packet, rotate=True, trail=True, trail_color=col, width=5)
        if t >= t_whip - 0.3:
            u0 = prog(t, t_whip, whip)
            speed = (CW - 120) * 3.2 / whip * (1 - abs(2 * u0 - 1)) if 0 < u0 < 1 else 0.0
            wop = 1 - curve("apple_in")(prog(t, e - OUT, OUT))
            with c.group(wop):
                shutter(c, t, chip_at, speed=speed)
    v.add(s, e, draw)
    v.sfx("whoosh", t_go, 0.4)
    v.sfx("whoosh", t_whip, 0.6)


# ── 06 · SAMBUNGAN: carry (one direction, cut mid-motion) then the one rack_cut ────────────────────────────────────
def sambungan(v, T, s, e, col):
    box = (X, 700, CW, 600)
    t_carry = _w(T, "L12", "kosong", 0.5)
    t_rack = _w(T, "L13", "dipotong", 0.8)

    def scene(label, sub, fill):
        def draw(c):
            c.card(*box, r=L["radius_bento"], color=fill)
            c.text(X + 60, box[1] + 90, sub, F["mono_med"], 26, C["card"] if fill != C["card"] else C["ink2"],
                   0.9, 0.12)
            c.text(X + 56, box[1] + box[3] - 70, label, D, 104, C["card"] if fill != C["card"] else C["ink"], 1,
                   -0.05)
        return draw
    a = scene("adegan 1.", "SEBELUM", C["card"])
    b = scene("adegan 2.", "SESUDAH · ARAH SAMA", col)
    cc = scene("fokus.", "RACK CUT", C["ink"])

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "06 · SEAMS", col)
        _, op = presence(t, s + 0.2, e - OUT)
        with c.group(op):
            if t < t_rack - M["rack_in"]:
                carry(c, t, t_carry, box, a, b)
            else:
                rack_cut(c, t, t_rack, box, b, cc)
    v.add(s, e, draw)
    v.sfx("whoosh", t_carry - 0.15, 0.5)
    v.sfx("thud", t_rack, 0.6)
    dolly(v, t_carry + M["carry_in"] + 0.3, t_rack - M["rack_in"] - 0.3)


# ── OUTRO: one line, then stillness ─────────────────────────────────────────────────────────────────────────────────
def outro(v, T, s, e, col):
    t_in = arrive(T["L14"].start + 0.2)
    t_mark = _w(T, "L14", "tepat", 0.8)

    def draw(c, t):
        split_rise(c, t, t_in, None, X, 820, "Sedikit gerakan,\ntapi *tepat*.", D, 112, C["ink"], by="line",
                   accent=C["accent"], ls=-0.055)
        w = c.measure("tapi tepat.", D, 112, -0.055)[0]
        mark(c, t, t_mark, "underline", (X, 820 + 112 - 80, w, 80), C["accent"], 6, seed=7)
        fade(c, t, t_mark + 0.6, None, lambda c: c.text(X, 1120, "mumeyong.dev", F["mono_med"], 30, C["ink2"], 1,
                                                        0.08))
    v.add(s, e, draw)
    dolly(v, t_mark + 0.6, e)
