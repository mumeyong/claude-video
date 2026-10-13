"""TEMPLATE — the current scenes.py grammar (STYLE §4 composition + §5 motion). Copy, then replace every
`REPLACE` with this video's own metaphor. Do NOT open other videos' scenes.py: this file + `api core` + the kit you
build is everything. Structure only — the hero, signature move, colors and copy must come from PLAN.md.

Shape: one persistent hero (Rig) from the first line to the recap · one function per chapter that draws headlines,
tags and small followers over it · every time from the voice (T) · camera = dolly in holds + cut at chapter changes.
"""
from engine import Video, tokens as tk
from engine.ease import clamp, prog
from engine.video import draw_background
from engine.components import (Headline, kicker, fade, pop_tag, brand_intro, standard_outro, cover, Rig, arrive,
                               follow, rise, dolly, cut, heads, draw_heads, material as mat)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                     # long brand sting (version 2): the voice starts under its wipe
LEAD = 0.5                          # chapter visuals start this long before the chapter's first line
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · REPLACE", "01 · REPLACE", "RECAP", "OUTRO"]   # = the ## headings in SCRIPT.md
LOOK = "flat"                       # flat | paper | lit — rotate vs the last video (`recent`)
COL = tk.CHAPTER[0][0]              # REPLACE with the PLAN signature color (a token, never a hex)
RX, RY = MID, 1020                  # hero rest position (screen px)


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


class Cue:
    """Every time the hero reacts to, computed once from the voice — read this, not the draw code, to retime."""

    def __init__(self, T, b):
        self.b = b
        self.t_in = T["L01"].start - 0.1
        self.hit = _w(T, "L02", "REPLACE", 0.6)       # the signature move lands on this stressed word
        self.again = _w(T, "L05", "REPLACE", 0.5)     # …and comes back in a later chapter (STYLE §3: reuse it)


def build(project):
    T = project.timing
    v = Video(duration=T["L10"].end + TAIL, bpm=88, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="lofi", key="C", mood="warm")          # REPLACE: rotate style/key/mood vs `recent`
    v.sfx_kit = "soft"                                         # REPLACE: rotate vs `recent`
    v.cover = lambda c: cover(c, "Judul\n*REPLACE*?", kicker="REPLACE", color=COL, badge="REPLACE",
                              tags=["REPLACE", "REPLACE"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(2):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[3], b[4], dark=True)
    v.stage = lambda c, t: (draw_background(c, v, t), mat.stage(c, LOOK, COL, 1 - v.dark_amount(t)))
    v.finish = lambda c, t: mat.finish(c, LOOK, 1 - v.dark_amount(t))
    Q = Cue(T, b)
    hero(v, T, Q)
    intro(v, T, Q, b[0], b[1])
    bab0(v, T, Q, b[1], b[2])
    bab1(v, T, Q, b[2], b[3])
    recap(v, T, Q, b[3], b[4])
    standard_outro(v, T, b[4], v.duration, "L10", COL,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="“REPLACE”", sub="REPLACE"))
    v.cover_t = Q.hit + 1.0
    return v


# ── the hero: ONE object over the whole video (big — STYLE §4), drawn around (0, 0) ───────────────────────────────────────
def draw_hero(c, t, Q, hit=0.0):
    """REPLACE with this video's kit component (engine/components/<kit>.py), e.g. kit(c, -w/2, -h/2, w, h, t, …)."""
    w, h = 820, 900
    c.card(-w / 2, -h / 2, w, h, r=L["radius_bento"])
    c.fill_rrect(-w / 2 + 60, -h / 2 + 60, (w - 120) * hit, 40, 20, COL)


def hero(v, T, Q):
    b = Q.b
    rig = Rig(x=RX, y=RY, s=2.2, a=0.0)
    rig.to(Q.t_in, preset="silk", s=1.0, a=1.0)              # full-bleed shrink → lands at rest
    rig.to(b[2] - 0.3, preset="silk", s=0.7, y=1180)          # makes room in 01 (continuity, never an empty frame)
    rig.to(b[3] + 0.2, preset="silk", s=0.85, y=1040)         # back for the recap

    def draw(c, t):
        op = 1 - prog(t, b[4] - OUT, OUT)
        hit = clamp(prog(t, arrive(Q.hit, "hero"), 0.6))
        with c.group(op):
            with rig.place(c, t):
                draw_hero(c, t, Q, hit)
    v.add(Q.t_in, b[4] + 0.05, draw, z=10, bleed=True)
    v.sfx("whoosh", Q.t_in, 0.5)
    v.sfx("thud", Q.hit, 0.7)


def _cover_hero(c, box):
    x, y, w, h = box
    with c.at(x + w / 2, y + h / 2, min(w / 820, h / 900), origin=(0, 0)):
        draw_hero(c, 0.0, None, 1.0)


def _tag(c, t, t_in, t_out, x, y, label, align="l"):
    fade(c, t, t_in, t_out, lambda c: pop_tag(c, t, t_in, x, y, label, COL, align=align))


# ── INTRO: hook headline arrives on its word; the hero lands; hold = dolly only ─────────────────────────────────────
def intro(v, T, Q, s, e):
    hs = heads(T, [("Hook\n*REPLACE*.", "L01"), ("Lalu\n*REPLACE*.", "L02")], e - OUT)

    def draw(c, t):
        kicker(c, t, T["L01"].start, e - OUT, "REPLACE", COL)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
    v.add(s, e, draw, z=20)
    dolly(v, Q.hit + 0.9, e - 0.2)


# ── 00: one leader per beat (tag/label follows the hero), holds ≥ 0,8 s ─────────────────────────────────────────────
def bab0(v, T, Q, s, e):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("REPLACE\n*satu*.", "L03"), ("REPLACE\n*dua*.", "L04")], e - OUT)
    t_tag = arrive(_w(T, "L03", "REPLACE", 0.5), "snappy")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[1], col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        _tag(c, t, t_tag, e - OUT, X + 20, RY - 520, "REPLACE")
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", t_tag, 0.5)
    dolly(v, t_tag + 0.9, e - 0.2, base=1.03)


# ── 01: the signature move comes back (Q.again); followers enter with follow(), never all at once ─────────────────
def bab1(v, T, Q, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("REPLACE\n*tiga*.", "L05"), ("REPLACE\n*empat*.", "L06", "L07")], e - OUT)
    t0 = arrive(Q.again, "snappy")
    chips = ["REPLACE", "REPLACE", "REPLACE"]

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[2], col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        for i, label in enumerate(chips):
            rise(c, t, follow(t0, i), e - OUT, (X, 640 + i * 80, CW, 60),
                 lambda c, i=i, label=label: pop_tag(c, t, follow(t0, i), X, 650 + i * 80, label, col))
    v.add(s, e, draw, z=20)
    cut(v, s)
    for i in range(len(chips)):
        v.sfx("pop", follow(t0, i), 0.4)
    dolly(v, follow(t0, 4) + 0.9, e - 0.2)


# ── RECAP (dark): the hero comes back; one line that only Mumeyong can say ───────────────────────────────────────────
def recap(v, T, Q, s, e):
    hs = heads(T, [("REPLACE\n*recap*.", "L08"), ("REPLACE\n*opini*.", "L09")], e - OUT, style="headline_dark")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", COL)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
    v.add(s, e, draw, z=20)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    dolly(v, T["L09"].start + 0.6, e - 0.2)
    cut(v, e)
