"""5 pertanyaan interview cloud yang selalu aku tanya — QUICK, reel look (STYLE §6e). See PLAN.md.

Metaphor: a stack of flashcards on the interview desk. Each question is one card; a 3-2-1 ring drains, the card flips
over its top edge and the back shows what I'm really listening for — not the textbook answer. Done cards pile up,
tilted, bottom-left; the deck shrinks bottom-right. In the recap the five cards fan out and merge into one question.
Motion: snappy springs · smear_words · persistent cards (Rig: deck → centre → pile → fan) · reel exits.
Sound: marimba Bb bright 112 + wood kit.
"""
import math

from engine import Video, tokens as tk
from engine.ease import clamp, prog, lerp, mix, out_back, in_out_cubic
from engine.components import (brand_intro, cover, Rig, spring_at, press, follow_button, smear, smear_p, out_p,
                               smear_words, viewfinder, iris, pixel_wipe, highlight, highlight_phrase, float_chips,
                               count_pill, pop_card, end_card, reel_sfx, ink_on, queue_dots, flip_card,
                               countdown_ring, KUIS_TEAL as TEAL, REEL_WORLDS as WORLDS)

C, F, L, M = tk.C, tk.F, tk.L, tk.M
PAPER, INK, GREEN, SEAL = C["brand_paper"], C["reel_ink"], C["reel_green"], C["brand_seal"]
MUTED = mix(INK, PAPER, 0.38)
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                             # long brand sting (version 2): voice starts under its wipe
LEAD = 0.3
TAIL = 2.6
OUT = M["reel_out"]
W0, H0 = 680, 450                          # card size at s = 1 (rig-local)
RING = (W0 / 2 - 70, -H0 / 2, 58)           # timer sticker on the card's top edge (rig-local)
DECK, PILE, DS = (770, 1440), (250, 1440), 0.26
SMALL = 0.62                                # below this scale a card shows only its big number
CH = ["INTRO", "01 · LEMOT", "02 · SCALE", "03 · TAGIHAN", "04 · JAM DUA", "05 · KUBERNETES", "RECAP", "OUTRO"]
SECTIONS = ["00 — 3 detik", "01 — lemot", "02 — scale", "03 — tagihan", "04 — jam 02.00", "05 — kubernetes",
            "06 — intinya", "07 — follow"]
QS = [("01", "Server-mu tiba-tiba lemot. Cek apa duluan?", ["sejak kapan?", "apa yang berubah?"]),
      ("02", "Bedanya scale up sama scale out?", ["kapan scale out", "nggak nolong?"]),
      ("03", "Tagihan naik dua kali lipat. Mulai dari mana?", ["cost report dulu,", "cari yang berubah."]),
      ("04", "Deploy gagal jam 02.00. Rollback atau fix forward?", ["user aman dulu,", "debug besok pagi."]),
      ("05", "Kapan kamu nggak pakai Kubernetes?", ["bisa jawab", "dengan yakin?"])]


# ── small helpers ───────────────────────────────────────────────────────
def _fit(c, text, font, size, maxw, ls=-0.045):
    w = c.measure(text, font, size, ls)[0]
    return size if w <= maxw else size * maxw / w


def say(c, t, t0, t1, a, b, y=330, size=92, color=TEAL, hl=None, t_hl=None):
    """Reel statement: a display line + a serif line in the signature color, centred, words smearing up.
    hl = phrase of the serif line to sweep with the highlighter at t_hl."""
    sa = _fit(c, a, F["display"], size, CW)
    smear_words(c, t, t0, MID, y, a, F["display"], sa, INK, -0.045, "c", t_out=t1)
    if b:
        sb = _fit(c, b, F["serif"], size * tk.SERIF_SCALE, CW, 0.0)
        yb = y + sa * 1.08
        if hl and t_hl is not None:
            with c.group(1 - out_p(t, t1)):
                highlight_phrase(c, t, t_hl, MID, yb, b, hl, F["serif"], sb, align="c", color=mix(GREEN, PAPER, 0.5))
        smear_words(c, t, t0 + 0.25, MID, yb, b, F["serif"], sb, color, align="c", t_out=t1)


def says(c, t, items):
    for it in items:
        a, b, t0, t1 = it[:4]
        if t0 - 0.05 <= t < t1 + OUT + 0.05:
            say(c, t, t0, t1, a, b, **(it[4] if len(it) > 4 else {}))


def ent(c, t, t0, t_out, bbox, dy=80, dx=0):
    """Reel entrance (smear) + reel exit (scale-up blur) for a block drawn at rest."""
    return smear(c, smear_p(t, t0), bbox, dx=dx, dy=dy, out=out_p(t, t_out))


def _small_front(c, x, y, w, h):
    c.fill_rrect(x, y, w, h * 0.06, 0, TEAL)
    for k in range(1, 4):
        c.line(x + w * 0.1, y + h * (0.35 + k * 0.17), x + w * 0.9, y + h * (0.35 + k * 0.17), mix(TEAL, PAPER, 0.8),
               4)


def _small_back(num):
    def draw(c, x, y, w, h):
        c.fill_rrect(x, y + h * 0.94, w, h * 0.06, 0, TEAL)
        c.text(x + w / 2, y + h * 0.66, num, F["mono_bold"], h * 0.42, TEAL, align="c")
    return draw


class Card:
    """One quiz card over the whole video: rig (deck → centre → pile → fan), ring window, flip time."""

    def __init__(self, i, rig):
        self.i, self.rig = i, rig
        self.num, self.q, self.a = QS[i]
        self.t_in = self.t_ring = self.t_ring_end = self.t_flip = None
        self.t_gone = 1e9

    def flip(self, t):
        return spring_at(t, self.t_flip, "snappy") if self.t_flip is not None else 0.0

    def draw(self, c, t):
        if self.t_in is None or t < self.t_in or t >= self.t_gone:
            return
        with self.rig.place(c, t) as st:
            small = st["s"] < SMALL
            write = clamp(prog(t, self.t_flip + 0.3, 1.2)) if self.t_flip is not None else 0.0
            flip_card(c, 0, 0, W0, H0, self.flip(t), self.num, self.q, self.a, write,
                      front=_small_front if small else None, back=_small_back(self.num) if small else None)
            if self.t_ring is not None and not small:
                ra = clamp(prog(t, self.t_in + 0.25, 0.3)) * (1 - clamp(prog(t, self.t_flip - 0.05, 0.25)))
                if ra > 0:
                    rp = clamp(prog(t, self.t_ring, self.t_ring_end - self.t_ring))
                    sc = out_back(clamp(prog(t, self.t_in + 0.25, 0.35)), 2.0)
                    with c.at(0, 0, max(0.01, sc), origin=RING[:2]):
                        countdown_ring(c, RING[0], RING[1], RING[2], rp, alpha=ra)

    def cues(self, v):
        v.sfx("pop", self.t_in, 0.6)
        if self.t_ring is not None:
            span = self.t_ring_end - self.t_ring
            for k in range(3):
                v.sfx("tick", self.t_ring + span * k / 3, 0.6 + 0.1 * k)
            v.sfx("chime", self.t_ring_end, 0.45)
        if self.t_flip is not None:
            v.sfx("whoosh", self.t_flip, 0.4)
            v.sfx("click", self.t_flip + 0.22, 0.7)


def to_pile(card, t):
    j = card.i
    card.rig.to(t, x=PILE[0] + (j % 2) * 14 - 7, y=PILE[1] - j * 7, s=DS, rot=(-0.09, 0.05, -0.03, 0.1, -0.06)[j],
                preset="snappy")


# ── build ───────────────────────────────────────────────────────────────
def build(project):
    T = project.timing
    v = Video(duration=T["L17"].end + TAIL, bpm=112, beat_offset=0.0)
    brand_intro(v, version=2)
    v.hud = False
    v.ground = PAPER
    v.music = dict(style="marimba", key="Bb", mood="bright")   # jalur-karier ambient D warm, foto-WA cinematic G dreamy
    v.sfx_kit = "wood"
    v.cover = lambda c: cover(c, "Jawab dalam\n*3 detik*.", kicker="INTERVIEW CLOUD · 5 PERTANYAAN", color=TEAL,
                              tags=["5 kartu", "bukan textbook", "rollback?"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    for i, n in enumerate(CH):
        v.chapter(i if 1 <= i <= 5 else None, n.split(" · ")[-1], b[i], b[i + 1])
    cards = [Card(0, Rig(MID, 1320, s=0.6, rot=0.08, a=0.0))] + \
            [Card(i, Rig(DECK[0], DECK[1], s=DS, rot=0.04, a=0.0)) for i in range(1, 5)]
    t_wipe = b[6] - 0.55
    darks = [intro(v, T, b[0], b[1], cards[0]), lemot(v, T, b[1], b[2], cards[0]),
             scale(v, T, b[2], b[3], cards[1]), tagihan(v, T, b[3], b[4], cards[2]),
             jam_dua(v, T, b[4], b[5], cards[3]), kubernetes(v, T, b[5], b[6], cards[4]),
             recap(v, T, b[6], b[7], cards, t_wipe)]
    outro(v, T, b[7], b[8])
    for k in cards:
        k.cues(v)

    t_deck = T["L02"].start + 0.3

    def desk(c, t):                                                     # deck (cards not dealt yet) + all cards
        if t_deck <= t < t_wipe + 0.5:
            left = [k for k in cards[1:] if t < k.t_in]
            for j, k in enumerate(reversed(left)):
                p = out_back(clamp(prog(t, t_deck + 0.08 * (4 - k.i), 0.4)), 1.6)
                with c.at(DECK[0] - j * 5, DECK[1] - j * 7 + 60 * (1 - p), DS * max(0.01, p), origin=(0, 0),
                          rot=0.04):
                    with c.group(clamp(p)):
                        flip_card(c, 0, 0, W0, H0, 0.0, front=_small_front)
        for k in cards:                                                 # pile (lower) first, active card on top
            k.draw(c, t)
    v.add(0, b[7], desk, z=30)
    reel_sfx(v, "cards", t_deck, n=4, each=0.08)

    def hud(c, t):
        k = max([i for i in range(len(CH)) if b[i] <= t] or [0])
        viewfinder(c, t, SECTIONS[k], v.duration, dark=max([d(t) for d in darks if d] + [0.0]), tag="karier cloud")
    v.add(0, v.duration, hud, z=110)
    v.cover_t = T["L05"].frac(0.8)
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    cw = min(w * 0.9, h * 1.3, 700)
    s = cw / W0
    with c.at(x + w / 2, y + h / 2, s, origin=(0, 0), rot=-0.03):
        flip_card(c, 0, 0, W0, H0, 0.0, "01", QS[0][1])
        countdown_ring(c, RING[0], RING[1], RING[2], 0.4)


# ── INTRO: card 01 lands, the ring runs 3-2-1 → five cards → "not the textbook" ─
def intro(v, T, s, e, card):
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    o = e - 0.95
    card.t_in = L1.start - 0.15
    card.t_ring = T.word("L01", "duluan", edge="end")
    card.t_ring_end = card.t_ring + 3.0                 # the literal 3-second timer from the question
    card.rig.to(card.t_in, a=1.0, dur=0.2).to(card.t_in, x=MID, y=930, s=1.0, rot=0.0, preset="snappy")
    card.rig.to(L2.start, y=900, s=0.92, preset="snappy")
    items = [("3 detik.", None, L1.start, L2.start - 0.3, dict(size=150, y=400)),
             ("Lima pertanyaan,", "tiap interview.", L2.start, L3.start - 0.3),
             ("Yang aku cari:", "bukan textbook.", L3.start, o, dict(hl="bukan", t_hl=T.word("L03", "bukan")))]

    def draw(c, t):
        says(c, t, items)
    v.add(s, e, draw, z=20)
    rx, ry = MID + RING[0], 930 + RING[1]
    v.camera.key(card.t_ring - 0.4, zoom=1.0, dur=0.01).key(card.t_ring - 0.3, zoom=1.08, x=rx - 120, y=ry + 160,
                                                             dur=0.7)
    v.camera.reset(L2.start + 0.1, dur=0.9)
    reel_sfx(v, "smear", L1.start)
    reel_sfx(v, "highlight", T.word("L03", "bukan"))
    t_open = e - 0.85
    v.add(t_open, e, lambda c, t: iris(c, t, t_open, MID, 900, TEAL, "open"), z=100)
    reel_sfx(v, "iris", t_open)
    dk = float(ink_on(TEAL) == PAPER)
    return lambda t: dk * float(t_open + 0.47 <= t < e)


# ── 01 · LEMOT: tool names fly in and fade · the card flips: "sejak kapan? apa yang berubah?" ─
TOOLS = [("Grafana", WORLDS[5], X + 10, 520, -1), ("CloudWatch", WORLDS[3], X + CW - 10, 560, 1),
         ("htop", WORLDS[4], X + 30, 1230, -1), ("Datadog", WORLDS[1], X + CW - 30, 1270, 1)]


def lemot(v, T, s, e, card):
    L4, L5 = T["L04"], T["L05"]
    o = e - 0.45
    card.t_flip = L5.start - 0.1
    card.rig.to(s + 0.1, y=920, s=1.0, preset="snappy")
    to_pile(card, e - 0.55)
    t_c = T.word("L04", "tool") - 0.5
    v.add(s, s + 0.7, lambda c, t: iris(c, t, s, MID, 900, TEAL, "close"), z=100)
    items = [("Bukan nama", "tool-nya.", L4.start - 0.1, L5.start - 0.3),
             ("Dia", "nanya balik.", L5.start, o)]

    def draw(c, t):
        says(c, t, items)
        if t >= t_c:
            with c.group(1 - 0.75 * clamp(prog(t, L5.start - 0.2, 0.5))):
                float_chips(c, t, t_c, TOOLS, t_out=L5.start + 0.6)
    v.add(s, e, draw, z=20)
    v.camera.key(card.t_flip, zoom=1.0, dur=0.01).key(card.t_flip + 0.2, zoom=1.06, y=980, dur=0.8)
    v.camera.reset(o, dur=0.6)
    reel_sfx(v, "chips", t_c, n=len(TOOLS))
    reel_sfx(v, "smear", L5.start)
    v.sfx("pop", e - 0.55, 0.3)
    dk = float(ink_on(TEAL) == PAPER)
    return lambda t: dk * float(s <= t < s + 0.25)


# ── 02 · SCALE: up (one tall box) vs out (four boxes) → all of them queue at one database ─
def _server(c, x, y, w, h, color, alpha=1.0):
    c.fill_rrect(x, y, w, h, 14, mix(color, PAPER, 0.7), alpha)
    c.stroke_rrect(x + 1, y + 1, w - 2, h - 2, 14, color, 3, alpha)
    for k in range(int(h // 40)):
        c.circle(x + 20, y + 22 + k * 40, 5, color, alpha)


def _db(c, cx, top, w, h, color, alpha=1.0):
    e = w * 0.16
    c.fill_rrect(cx - w / 2, top, w, h, 4, mix(color, PAPER, 0.55), alpha)
    cx_ = c.ctx
    for yy, fill in ((top + h, True), (top, True)):
        cx_.save()
        cx_.translate(cx, yy)
        cx_.scale(w / 2, e)
        cx_.new_path()
        cx_.arc(0, 0, 1, 0, 2 * math.pi)
        cx_.restore()
        c.src(mix(color, PAPER, 0.3 if yy == top else 0.55), alpha)
        cx_.fill()
    c.text(cx, top + h * 0.62, "database", F["mono_bold"], 22, INK, alpha, 0.04, align="c")


def scale(v, T, s, e, card):
    L6, L7, L8 = T["L06"], T["L07"], T["L08"]
    o = e - 0.45
    card.t_in = s + 0.1
    card.t_ring, card.t_flip = L6.start + 0.3, T.word("L07", "tanya") - 0.1
    card.t_ring_end = card.t_flip - 0.15
    card.rig.to(card.t_in, a=1.0, dur=0.15).to(card.t_in, x=MID, y=760, s=0.78, rot=0.0, preset="snappy")
    to_pile(card, e - 0.55)
    t_up, t_out = T.word("L06", "up"), T.word("L06", "out")
    t_db = T.word("L08", "database")
    DB = (MID, 1385, 190, 110)
    up_box = (X + 70, 990)
    outs = [(X + CW - 330 + (i % 2) * 150, 1010 + (i // 2) * 150) for i in range(4)]
    items = [("Up", "atau out?", L6.start - 0.1, L7.start - 0.3),
             ("Definisi?", "semua hafal.", L7.start, L8.start - 0.3),
             ("Bottleneck-nya", "di database.", L8.start, o, dict(hl="database", t_hl=t_db))]

    def draw(c, t):
        says(c, t, items)
        with ent(c, t, L6.start + 0.2, o, (X + 40, 990, CW - 80, 520), dy=90):
            grow = out_back(clamp(prog(t, t_up, 0.5)), 1.4)
            hh = lerp(120, 300, grow)
            _server(c, up_box[0], up_box[1] + 300 - hh, 170, hh, TEAL)
            c.text(up_box[0], 1335, "scale up", F["mono_med"], 22, MUTED, clamp(prog(t, t_up, 0.3)), 0.12)
            for i, (bx, by) in enumerate(outs):
                p = out_back(clamp(prog(t, t_out + 0.1 * i, 0.4)), 1.7)
                if p > 0:
                    with c.at(0, 0, max(0.01, p), origin=(bx + 60, by + 60)):
                        _server(c, bx, by, 120, 120, TEAL)
            c.text(X + CW - 70, 1325, "scale out", F["mono_med"], 22, MUTED, clamp(prog(t, t_out, 0.3)), 0.12,
                   align="r")
            pd = clamp(prog(t, t_db - 0.4, 0.4))
            if pd > 0:
                _db(c, DB[0], DB[1], DB[2], DB[3], INK, pd)
                srcs = [(up_box[0] + 85, 1290)] + [(bx + 60, by + 120) for bx, by in outs]
                for j, (sx, sy) in enumerate(srcs):
                    pts = [(sx, sy), (lerp(sx, DB[0], 0.5), lerp(sy, DB[1], 0.6)), (DB[0] + (j - 2) * 14, DB[1])]
                    c.line(pts[0][0], pts[0][1], pts[2][0], pts[2][1], mix(TEAL, PAPER, 0.6), 3, pd)
                    queue_dots(c, pts, t, n=4, speed=0.3, jam=clamp(prog(t, t_db, 1.2)), r=7, seed=j, color=TEAL,
                               alpha=pd)
    v.add(s, e, draw, z=20)
    v.camera.key(t_db - 0.3, zoom=1.0, dur=0.01).key(t_db - 0.2, zoom=1.05, y=1250, dur=0.8)
    v.camera.reset(o, dur=0.6)
    reel_sfx(v, "smear", L6.start + 0.2)
    v.sfx("pop", t_up, 0.5)
    reel_sfx(v, "chips", t_out, n=4, each=0.1)
    reel_sfx(v, "highlight", t_db)
    v.sfx("thud", t_db, 0.4)


# ── 03 · TAGIHAN: 2× pill · tilted card + cost report, the new row gets the highlighter ─
ROWS = [("compute", 0.74, False), ("storage", 0.42, False), ("NAT gateway", 0.58, True)]


def tagihan(v, T, s, e, card):
    L9, L10 = T["L09"], T["L10"]
    o = e - 0.45
    card.t_in = s + 0.1
    card.t_ring, card.t_flip = L9.start + 0.3, L10.start - 0.1
    card.t_ring_end = card.t_flip - 0.15
    card.rig.to(card.t_in, a=1.0, dur=0.15).to(card.t_in, x=395, y=770, s=0.72, rot=-0.05, preset="snappy")
    to_pile(card, e - 0.55)
    t_2x = T.word("L09", "dua") - 0.1
    t_rep = L9.start + 1.2
    t_hl = T.word("L10", "berubah") - 0.1
    RX, RY, RW, RH = X + CW - 40 - 520, 1000, 520, 360
    items = [("Tagihan", "meledak.", L9.start - 0.1, L10.start - 0.3),
             ("Data dulu,", "baru tindakan.", L10.start, o)]

    def report(c, t, x, y, w, h):
        c.text(x + 34, y + 58, "COST REPORT · BULAN INI", F["mono_med"], 20, MUTED, 1, 0.16)
        for i, (name, f, new) in enumerate(ROWS):
            ry = y + 112 + i * 76
            if new:
                highlight(c, t, t_hl, x + 24, ry - 2, w - 48, 58, color=mix(GREEN, PAPER, 0.55))
            c.text(x + 34, ry + 36, name, F["ui_semi"], 26, INK, 1, -0.01)
            bx = x + 240
            c.fill_rrect(bx, ry + 16, (w - 290) * f * clamp(prog(t, t_rep + 0.3 + 0.12 * i, 0.5)), 22, 11,
                         SEAL if new else mix(TEAL, PAPER, 0.35))
            if new and t >= t_hl + 0.2:
                pa = out_back(clamp(prog(t, t_hl + 0.2, 0.35)), 1.8)
                with c.at(0, 0, max(0.01, pa), origin=(x + w - 70, ry - 8)):
                    c.fill_rrect(x + w - 128, ry - 26, 116, 38, 19, SEAL)
                    c.text(x + w - 70, ry, "baru", F["ui_semi"], 22, PAPER, 1, align="c")

    def draw(c, t):
        says(c, t, items)
        count_pill(c, t, t_2x, 740, 505, 1, 2, label="TAGIHAN",
                   fmt=lambda x: f"{round(x * 10) / 10:g}".replace(".", ",") + "×", dur=0.8, t_out=o)
        with c.group(1 - out_p(t, o)):
            pop_card(c, t, t_rep, RX, RY, RW, RH, draw=lambda c_, *bx: report(c_, t, *bx))
    v.add(s, e, draw, z=40)
    v.camera.key(t_hl - 0.3, zoom=1.0, dur=0.01).key(t_hl - 0.2, zoom=1.06, x=RX + RW / 2, y=RY + 260, dur=0.8)
    v.camera.reset(o, dur=0.6)
    reel_sfx(v, "count", t_2x)
    reel_sfx(v, "cards", t_rep, n=1)
    reel_sfx(v, "highlight", t_hl)
    v.sfx("pop", t_hl + 0.2, 0.6)


# ── 04 · JAM DUA: giant 02.00 → card + two buttons, "Rollback" gets pressed ─
def _button(c, cx, y, w, h, label, filled, alpha=1.0):
    if filled:
        c.fill_rrect(cx - w / 2, y, w, h, h / 2, TEAL, alpha)
    else:
        c.fill_rrect(cx - w / 2, y, w, h, h / 2, PAPER, alpha)
        c.stroke_rrect(cx - w / 2 + 1.5, y + 1.5, w - 3, h - 3, h / 2, mix(INK, PAPER, 0.6), 3, alpha)
    c.text(cx, y + h * 0.63, label, F["ui_semi"], 30, PAPER if filled else INK, alpha, -0.01, align="c")


def jam_dua(v, T, s, e, card):
    L11, L12 = T["L11"], T["L12"]
    o = e - 0.45
    card.t_in = L11.start + 0.5
    card.t_ring, card.t_flip = L11.start + 0.9, L12.start - 0.1
    card.t_ring_end = card.t_flip - 0.15
    card.rig.to(card.t_in, a=1.0, dur=0.15).to(card.t_in, x=MID, y=1000, s=0.8, rot=0.0, preset="snappy")
    to_pile(card, e - 0.55)
    t_rb = T.word("L12", "rollback")
    BY, BW, BH = 1240, 300, 84
    rb, ff = (MID - 170, BY), (MID + 170, BY)

    def draw(c, t):
        a_clock = 1 - out_p(t, L12.start - 0.35)
        if a_clock > 0:
            c.text(MID, 400, "● DEPLOY · FAILED", F["mono_med"], 24, SEAL, clamp(prog(t, L11.start, 0.3)) * a_clock,
                   0.18, align="c")
            smear_words(c, t, L11.start - 0.05, MID, 650, "02.00", F["display"], 250, INK, -0.05, "c",
                        t_out=L12.start - 0.35)
        says(c, t, [("Favoritku:", "rollback.", L12.start, o)])
        with ent(c, t, L11.start + 1.0, o, (rb[0] - BW / 2, BY, ff[0] - rb[0] + BW, BH), dy=50):
            with c.at(0, 0, press(t, t_rb), origin=(rb[0], BY + BH / 2)):
                _button(c, rb[0], BY, BW, BH, "Rollback", True)
            _button(c, ff[0], BY, BW, BH, "fix forward", False, 1 - 0.55 * clamp(prog(t, t_rb, 0.3)))
            pk = out_back(clamp(prog(t, t_rb + 0.15, 0.35)), 2.0)
            if pk > 0:
                with c.at(0, 0, max(0.01, pk), origin=(rb[0] + BW / 2 - 14, BY + 6)):
                    c.circle(rb[0] + BW / 2 - 14, BY + 6, 26, PAPER)
                    countdown_ring(c, rb[0] + BW / 2 - 14, BY + 6, 22, 1.0, width=6)
    v.add(s, e, draw, z=20)
    v.camera.key(t_rb, zoom=1.0, dur=0.01).key(t_rb + 0.02, zoom=0.97, dur=0.33).key(t_rb + 0.4, zoom=1.0, dur=0.6)
    reel_sfx(v, "smear", L11.start - 0.05)
    v.sfx("thud", L11.start + 0.2, 0.5)
    reel_sfx(v, "smear", L11.start + 1.0)
    v.sfx("click", t_rb, 0.9)
    v.sfx("chime", t_rb + 0.15, 0.5)


# ── 05 · KUBERNETES: card right, interview notes left — the pen writes, I note the name ─
def _scribble(c, x, y, w, p, color, width=4):
    pts = []
    n = 60
    for i in range(int(n * clamp(p)) + 1):
        u = i / n
        pts.append((x + w * u, y + math.sin(u * 31.0) * 9 + math.sin(u * 13.0 + 1.3) * 5 - u * 6))
    if len(pts) < 2:
        return
    cx_ = c.ctx
    cx_.new_path()
    cx_.move_to(*pts[0])
    for q in pts[1:]:
        cx_.line_to(*q)
    c.src(color)
    cx_.set_line_width(width)
    cx_.stroke()


def kubernetes(v, T, s, e, card):
    L13, L14 = T["L13"], T["L14"]
    o = e - 0.45
    card.t_in = s + 0.1
    card.t_ring, card.t_flip = L13.start + 0.3, L14.start - 0.1
    card.t_ring_end = card.t_flip - 0.15
    card.rig.to(card.t_in, a=1.0, dur=0.15).to(card.t_in, x=MID + 90, y=800, s=0.72, rot=0.04, preset="snappy")
    t_cat = T.word("L14", "catat")
    NX, NY, NW, NH = X + 50, 990, 400, 330
    items = [("Kapan nggak", "pakai Kubernetes?", L13.start - 0.1, L14.start - 0.3),
             ("Yang yakin,", "aku catat.", L14.start, o)]

    def notes(c, t):
        with c.at(0, 0, 1.0, origin=(NX + NW / 2, NY + NH / 2), rot=-0.05):
            c.card(NX, NY, NW, NH, 10, color=C["card"])
            c.text(NX + 30, NY + 54, "CATATAN INTERVIEW", F["mono_med"], 19, MUTED, 1, 0.16)
            for k in range(3):
                ly = NY + 150 + k * 66
                c.line(NX + 30, ly, NX + NW - 30, ly, mix(TEAL, PAPER, 0.8), 2)
            c.text(NX + 30, NY + 138, "kandidat:", F["serif"], 36, INK, 1)
            _scribble(c, NX + 180, NY + 122, NW - 230, prog(t, t_cat, 0.7), INK)
            ck = clamp(prog(t, t_cat + 0.7, 0.3))
            if ck > 0:
                countdown_ring(c, NX + NW - 60, NY + 236, 30, 1.0, width=7, alpha=ck)

    def draw(c, t):
        says(c, t, items)
        with ent(c, t, L13.start + 0.6, o, (NX - 20, NY - 20, NW + 40, NH + 40), dy=70, dx=-60):
            notes(c, t)
    v.add(s, e, draw, z=20)
    v.camera.key(s + 0.2, zoom=1.0, dur=0.01).key(L14.start, zoom=1.05, x=NX + NW / 2 + 60, y=NY + 120, dur=1.2)
    v.camera.reset(o, dur=0.6)
    reel_sfx(v, "smear", L13.start + 0.6)
    v.sfx("key", t_cat, 0.5)
    v.sfx("key", t_cat + 0.3, 0.4)
    v.sfx("chime", t_cat + 0.7, 0.5)


# ── RECAP: pixel wipe → five cards fan out → merge into one question ────
MERGED = ("01–05", "Ada yang rusak. Langkah pertamamu?")


def recap(v, T, s, e, cards, t_wipe):
    L15 = T["L15"]
    o = e - 0.45
    t_fan = s + 0.1
    t_m = T.word("L15", "satu") - 0.15
    for k in cards:
        j = k.i - 2
        k.rig.to(t_fan + 0.05 * k.i, x=MID + j * 110, y=1060 + abs(j) * 30, s=0.34, rot=j * 0.09, preset="snappy")
        k.rig.to(t_m + 0.04 * k.i, x=MID, y=1000, s=0.86, rot=0.0, preset="snappy")
        k.rig.to(t_m + 0.3, a=0.0, dur=0.2)
        k.t_gone = t_m + 0.55
    merged = Rig(MID, 1000, s=0.86, a=0.0)
    merged.to(t_m + 0.3, a=1.0, dur=0.15).to(t_m + 0.6, s=1.0, preset="snappy")
    t_mf = t_m + 0.55

    def draw(c, t):
        says(c, t, [("Lima kartu,", "satu pertanyaan.", L15.start - 0.1, o)])
        if t >= t_m + 0.3:
            with merged.place(c, t), c.group(1 - out_p(t, o)):
                flip_card(c, 0, 0, W0, H0, 1 - spring_at(t, t_mf, "snappy"), MERGED[0], MERGED[1],
                          back=lambda c_, x, y, w, h: None)
    v.add(s, e, draw, z=35)
    v.add(t_wipe, t_wipe + 1.6, lambda c, t: pixel_wipe(c, t, t_wipe, TEAL), z=100)
    v.camera.key(s, zoom=1.08, dur=0.01).key(s + 0.1, zoom=1.0, dur=1.6)
    reel_sfx(v, "wipe", t_wipe)
    reel_sfx(v, "cards", t_fan, n=5, each=0.05)
    reel_sfx(v, "smear", L15.start - 0.1)
    v.sfx("thud", t_m + 0.3, 0.5)
    v.sfx("whoosh", t_mf, 0.4)
    dk = float(ink_on(TEAL) == PAPER)
    return lambda t: dk * float(0.3 < prog(t, t_wipe, 0.9) < 0.85)


# ── OUTRO: end card + "kamu jawab apa?" + follow ────────────────────────
def outro(v, T, s, e):
    t0 = T["L16"].start - 0.2
    t_click = T.word("L17", "Follow") + 0.3

    def draw(c, t):
        end_card(c, t, t0, cy=760, r=140, name="mumeyong.dev", sub="pertanyaan 01 — kamu jawab apa?",
                 cta="tulis di komentar")
        if t >= T["L17"].start - 0.4:
            with ent(c, t, T["L17"].start - 0.4, None, (MID - 150, 1300, 300, 72), dy=40):
                follow_button(c, MID, 1300, t, t_click)
    v.add(s, e, draw, z=20)
    reel_sfx(v, "end", t0)
    v.sfx("pop", T["L17"].start - 0.4, 0.5)
    v.sfx("click", t_click, 0.8)
