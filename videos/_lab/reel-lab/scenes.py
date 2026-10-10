"""Reel lab — proof sheet for components/reel.py (STYLE §6e). Not for posting.

Every move of the claude.ai Motion film "Six Worlds, One Walk" (mumeyong.dev brand reel, 16:9), re-laid for 1080×1920,
one chapter per film scene, anchored to the (estimated) voice lines.
"""
from engine import Video, tokens as tk
from engine.ease import clamp, mix, prog
from engine.components import (smear_words, smear_p, out_p, viewfinder, dot_gather, orbit, iris, pixel_wipe,
                               highlight_phrase, float_chips, count_pill, formula, pop_card, tilt_plane, stat_panel,
                               verb_slam, end_card, reel_sfx, ink_on, REEL_WORLDS as W, fmt_id)

C, F, L = tk.C, tk.F, tk.L
PAPER, INK, GREEN = C["brand_paper"], C["reel_ink"], C["reel_green"]
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
LEAD = 0.3
TAIL = 1.4
NAMES = ("INTRO", "01 · LOGO", "02 · STACK", "03 · IDE", "04 · FORMULA", "05 · WORLDS", "06 · ANGKA", "07 · VERBS",
         "OUTRO")
SECTIONS = ("00 — reel lab", "01 — boot", "02 — the stack", "03 — the idea", "04 — formula", "05 — six worlds",
            "06 — numbers", "07 — six verbs", "08 — sign-off")


def build(project):
    T = project.timing
    v = Video(duration=T.line("L09").end + TAIL, bpm=112, beat_offset=0.0)
    v.hud = False
    v.music = dict(style="marimba", key="F", mood="bright")
    v.sfx_kit = "glass"
    b = [max(0.0, T.chapter_span(n)[0] - LEAD) for n in NAMES] + [v.duration]
    for i, n in enumerate(NAMES):
        v.chapter(i if 0 < i < 8 else None, n, b[i], b[i + 1])
    v.ground = PAPER
    darks = []
    for fn, i in ((intro, 0), (logo, 1), (stack, 2), (ide, 3), (rumus, 4), (worlds, 5), (angka, 6), (verbs, 7),
                  (outro, 8)):
        d = fn(v, T, b[i], b[i + 1])
        if d:
            darks.append(d)

    def hud(c, t):
        k = max([i for i in range(9) if b[i] <= t] or [0])
        viewfinder(c, t, SECTIONS[k], v.duration, dark=max([d(t) for d in darks] + [0.0]))
    v.add(0, v.duration, hud, z=110)   # full-screen overlays: z >= 100 (lint skips them)
    v.cover_t = T.line("L09").start + 2.6
    return v


def intro(v, T, s, e):
    L1 = T["L01"]

    def draw(c, t):
        o = e - 0.45
        smear_words(c, t, L1.start, MID, 900, "Reel lab.", F["display"], 150, INK, -0.045, "c", t_out=o)
        smear_words(c, t, L1.start + 0.4, MID, 1010, "versi vertikal.", F["serif"], 96 * tk.SERIF_SCALE, GREEN,
                    align="c", t_out=o)
    v.add(s, e, draw)
    reel_sfx(v, "smear", L1.start)


def logo(v, T, s, e):
    t0 = T["L02"].start - 0.2
    t_iris = e - 0.85

    def draw(c, t):
        dot_gather(c, t, t0, MID, 900, 150)
        orbit(c, t, MID, 900, 330, 90, alpha=clamp(prog(t, t0 + 1.05, 0.45)))
        c.text(MID, 1300, "~ BOOT SEQUENCE · MUMEYONG.DEV", F["mono"], 20, INK,
               0.55 * (1 - clamp(prog(t, t_iris - 0.3, 0.3))), 0.18, align="c")
    v.add(s, e, draw)
    v.add(s, e, lambda c, t: iris(c, t, t_iris, MID, 900, GREEN, "open"), z=100)
    reel_sfx(v, "gather", t0)
    reel_sfx(v, "iris", t_iris)
    return lambda t: float(s <= t < e and prog(t, t_iris, 0.85) > 0.55)


CHIPS = [("Kubernetes", W[1], 100, 430, -1), ("Terraform", W[4], 910, 380, 1), ("Alibaba Cloud", W[3], 110, 640, -1),
         ("ArgoCD", W[4], 900, 610, 1), ("Prometheus", W[5], 110, 1330, -1), ("WAF · zero-trust", W[2], 910, 1290, 1),
         ("AWS · Azure · GCP", W[3], 140, 1470, -1), ("Grafana", W[5], 900, 1480, 1)]


def stack(v, T, s, e):
    L3 = T["L03"]
    t_c = L3.start + 0.5
    o = e - 0.45

    def draw(c, t):
        smear_words(c, t, s + 0.35, MID, 960, "Multi-cloud", F["serif"], 150 * tk.SERIF_SCALE, INK, align="c", dy=60,
                    t_out=o)
        count_pill(c, t, t_c, MID, 1040, 1200, 10000, label="CONCURRENT REQ", suffix="+", t_out=o)
        float_chips(c, t, t_c + 0.2, CHIPS, t_out=o)
    v.add(s, e, draw)
    v.add(s, e, lambda c, t: iris(c, t, s, MID, 900, GREEN, "close"), z=100)
    reel_sfx(v, "count", t_c)
    reel_sfx(v, "chips", t_c + 0.2, n=len(CHIPS))
    return lambda t: float(s <= t < s + 0.25)


def ide(v, T, s, e):
    L4 = T["L04"]
    t_w = e - 1.0
    a, bb = "Cloud architecture", "you can walk through."

    def draw(c, t):
        sa = 92
        smear_words(c, t, L4.start - 0.1, MID, 880, a, F["display"], sa, INK, -0.045, "c")
        highlight_phrase(c, t, L4.start + 0.9, MID, 1010, bb, "walk through", F["serif"], sa * tk.SERIF_SCALE,
                         align="c")
        smear_words(c, t, L4.start + 0.3, MID, 1010, bb, F["serif"], sa * tk.SERIF_SCALE, INK, align="c")
    v.add(s, e, draw)
    v.add(s, e + 0.2, lambda c, t: pixel_wipe(c, t, t_w), z=100)
    reel_sfx(v, "highlight", L4.start + 0.9)
    reel_sfx(v, "wipe", t_w)
    return lambda t: float(s <= t < e + 0.2 and 0.3 < prog(t, t_w, 0.9) < 0.85)


def rumus(v, T, s, e):
    L5 = T["L05"]
    t0 = L5.start - 0.1
    cards = [("01 · FinOps", "Rightsizing", "capacity planning"), ("02 · IaC", "Automation", "−80% manual work"),
             ("03 · Signals", "Observability", "−50% RCA time")]
    bw, bh, gap = 600, 190, 70
    boxes = [(MID - bw / 2 - 60 + i * 60, 470 + i * (bh + gap), bw, bh) for i in range(3)]
    o = e - 0.4

    def draw(c, t):
        c.text(X, 330, "FORMULA · STRAIGHT FROM THE CV", F["mono"], 20, INK, 0.55 * clamp(prog(t, s, 0.35))
               * (1 - out_p(t, o)), 0.18)
        smear_words(c, t, s + 0.05, X, 420, "Savings, engineered.", F["display"], 76, INK, -0.045, t_out=o)
        t_res = formula(c, t, t0, boxes, cards, (MID, 1300), t_out=o)
        count_pill(c, t, t_res, MID, 1300, 7000, 14000, fmt=lambda x: "$" + fmt_id(round(x / 10) * 10),
                   label="/ BULAN", dur=1.0, t_out=o)
    v.add(s, e, draw)
    reel_sfx(v, "formula", t0, n=3)


SHOTS = [("Root", 0, 0, 560, 360), ("Platform", 590, 0, 310, 170), ("Security", 590, 190, 310, 170),
         ("Cloud", 0, 390, 280, 170), ("Automation", 310, 390, 280, 170), ("Observability", 620, 390, 280, 170)]
K = 0.78                                   # plane scale: the tilt pushes the corners out, keep it inside the column
PX, PY = MID - 900 * K / 2, 760


def worlds(v, T, s, e):
    L6 = T["L06"]
    o = e - 0.5

    def plane(c, t):
        for i, (name, x, y, w, h) in enumerate(SHOTS):
            def body(c, x, y, w, h, i=i):
                c.fill_rrect(x, y, w, h, 16, mix(W[i], PAPER, 0.82))
                for k in range(4):
                    c.fill_rrect(x + 28, y + 30 + k * 34, (w - 56) * (0.9 - k * 0.17), 14, 7, W[i], 0.5)
            pop_card(c, t, L6.start + 0.1 + i * tk.M["reel_card_stagger"], PX + x * K, PY + y * K, w * K, h * K,
                     draw=body,
                     label=name, color=W[i])

    def draw(c, t):
        smear_words(c, t, s + 0.05, X, 420, "Six worlds,", F["display"], 96, INK, -0.045, t_out=o)
        smear_words(c, t, s + 0.25, X, 530, "one walk.", F["serif"], 96 * tk.SERIF_SCALE, GREEN, t_out=o)
        tilt_plane(c, t, s, e, (PX, PY, 900 * K, 560 * K), plane, t_out=o)
    v.add(s, e, draw)
    reel_sfx(v, "cards", L6.start + 0.1, n=len(SHOTS))


def angka(v, T, s, e):
    each = (e - s) / 4
    S = [(3, 7, lambda x: f"{round(x)}+", "years in the cloud", None),
         (1, 4, lambda x: f"{round(x)}", "clouds · AWS · Azure · GCP · Alibaba", INK),
         (95, 99.99, lambda x: fmt_id(x, 2) + "%", "uptime, self-healing CI", None),
         (25, 50, lambda x: f"−{round(x)}%", "troubleshooting time", GREEN)]

    def draw(c, t):
        for i, (v0, v1, f, lab, bg) in enumerate(S):
            stat_panel(c, t, s + i * each, each, v0, v1, lab, f, bg, t_out=e - 0.3 if i == 3 else None)
    v.add(s, e, draw)
    reel_sfx(v, "stats", s, n=4, each=each)
    return lambda t: float(s + each <= t < s + 2 * each)


VERBS = ["BOOT", "CONNECT", "GUARD", "BUILD", "AUTOMATE", "MEASURE"]


def verbs(v, T, s, e):
    t0 = T["L08"].start - 0.1
    each = min(0.43, (e - t0) / 6)

    def draw(c, t):
        if t >= t0:
            verb_slam(c, t, t0, VERBS, each=each)
    v.add(s, e, draw, z=100)
    reel_sfx(v, "verbs", t0, n=6, each=each)

    def dark(t):
        if not (t0 <= t < e):
            return 0.0
        return float(ink_on(W[min(5, int((t - t0) / each))]) == PAPER)
    return dark


def outro(v, T, s, e):
    t0 = T["L09"].start - 0.2

    def draw(c, t):
        end_card(c, t, t0, cy=860, r=150, name="mumeyong.dev", sub="cloud & DevOps engineer",
                 cta="walk it at mumeyong.dev")
    v.add(s, e, draw)
    reel_sfx(v, "end", t0)
