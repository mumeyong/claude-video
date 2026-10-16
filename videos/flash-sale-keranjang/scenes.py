"""flash-sale-keranjang — "Barang flash sale 'habis' padahal udah di keranjang. Kok bisa?"

Hero: ONE minimarket rack with ONE flash-sale box left. Hands point at it (= keranjang), a fist grabs it (= checkout
yang menang). The yellow stock tag under it is the scoreboard: SISA 1 → HABIS → SISA -1 → HABIS → SISA 1 → PUNYAMU.
Intro is the phone screen everybody knows (12.00.00, Bayar, "Stok habis"); the box flies out of the cart onto the rack.
"""
import math
from contextlib import contextmanager

from engine import Video, tokens as tk
from engine.ease import clamp, prog, track, curve, lerp, mix
from engine.video import draw_background
from engine.components import (kicker, pop_tag, brand_intro, standard_outro, cover, arrive, follow, ios_at, dolly,
                               cut, heads, draw_heads, press, check_badge, strike, draw_on, pts_rrect, mark, wobble,
                               rak, rak_geo, filler, produk, empty_spot, label_stok, tangan, material as mat)
from engine.components.minimarket import SLEEVE, SKIN, PROD_W, PROD_H

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                     # long brand sting (version 2): the voice starts under its wipe
LEAD = 0.5                          # chapter visuals start this long before the chapter's first line
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · KERANJANG", "01 · CHECKOUT", "02 · ANTREAN", "RECAP", "OUTRO"]
LOOK = "lit"                        # studio light = a lit shop shelf (last two: flat-big, paper-big)

# palette
RED = tk.hexc("#E0285A")            # signature: flash-sale raspberry
YOU = C["accent"]                   # your sleeve, your dot in the queue
PHONE = tk.hexc("#16171C")
WAIT = C["orange_pill"]

# rack geometry (rack-local px, scale 1)
RACK_W, RACK_H, ROWS = 760, 880, (220, 330, 240)
SLOT_Y = rak_geo(RACK_W, RACK_H, ROWS)[1]      # the flash-sale row: product bottom
PC = (0.0, SLOT_Y - PROD_H / 2)               # product center
TAG_Y = SLOT_Y + 40                           # stock tag hangs under the lip
SPOT_DX = 235                                 # sold-out outlines left / right of the product
REACH = 520                                   # a hand slides in this far
PULL = 1000                                   # a fist carries the box this far out (off frame)
FLY = 0.9                                     # box flight phone/card → rack
RACK_KEYS = [(1090, 1.08), (860, 0.62), (990, 0.66)]  # (y, scale): 00–01 · 02 · recap
TAG_H, TAG_SIZE = 60, 30                      # tags readable at thumb size

# intro phone
PH = (270, 600, 540, 880)
SX, SY, SW, SH = PH[0] + 14, PH[1] + 14, PH[2] - 28, PH[3] - 28
THUMB = (SX + 150, SY + 560, 0.55)            # cart thumbnail: bottom-center + scale
TICK = 0.45                                   # clock seconds before 12.00.00
# bottom card in 02 (waiting room → unpaid order)
CARD = (X, 1190, CW, 240)
CARD_THUMB = (X + 100, 1395, 0.5)
Q_GAP, Q_STEP, Q_R = 46, 0.6, 13              # queue dots: spacing, step period, radius


def _w(T, lid, word, frac, nth=0):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words)."""
    try:
        return T.word(lid, word, nth)
    except Exception:
        return T[lid].frac(frac)


def _tag(c, t, t0, x, y, label, color, align="l"):
    """Solid pill tag, readable at thumb size (pop_tag's type is too small over a busy shelf)."""
    if t < t0:
        return
    w = c.measure(label, F["ui_semi"], TAG_SIZE)[0] + 44
    x = x - w if align == "r" else x
    p = ios_at(t, t0, "snappy")
    with c.group(clamp(prog(t, t0, 0.15))), c.at(0, 0, lerp(0.92, 1.0, p), origin=(x + w / 2, y + TAG_H / 2)):
        c.fill_rrect(x, y, w, TAG_H, TAG_H / 2, color)
        c.text(x + 22, y + TAG_H * 0.68, label, F["ui_semi"], TAG_SIZE, C["card"])


@contextmanager
def place(c, x, y, s):
    ctx = c.ctx
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    try:
        yield
    finally:
        ctx.restore()


class Hand:
    """One person's hand: slides in along its own direction to `tip` at t_in, leaves (or pulls the box) at t_out."""

    def __init__(self, kind, tip, ang, sleeve, skin, t_in, t_out=None, carry=None, travel=None, seed=0):
        self.kind, self.tip, self.ang, self.sleeve, self.skin = kind, tip, ang, sleeve, skin
        self.t_in, self.t_out, self.carry, self.seed = t_in, t_out, carry, seed
        self.travel = travel or (PULL if kind == "grab" else REACH)
        self.hold = travel is not None and kind == "grab"          # pulls a little and keeps it

    def out_p(self, t):
        if self.t_out is None or t < self.t_out:
            return 0.0
        if self.hold:
            return ios_at(t, self.t_out, "smooth")
        return curve("apple_in")(clamp(prog(t, self.t_out, 0.55)))

    def back(self, t):
        return REACH * (1 - ios_at(t, self.t_in, "snappy")) + self.travel * self.out_p(t)

    def live(self, t):
        return t >= self.t_in and (self.hold or self.out_p(t) < 1)

    def draw(self, c, t):
        dx, dy = math.cos(self.ang), math.sin(self.ang)
        b = self.back(t)
        idle = wobble(t, self.seed, 3) if self.kind == "point" else 0.0
        tangan(c, self.tip[0] - dx * b, self.tip[1] - dy * b + idle, self.ang, self.kind, self.sleeve, self.skin,
               alpha=clamp(prog(t, self.t_in, 0.12)))

    def draw_carry(self, c, t):
        if not self.carry or self.t_out is None or t < self.t_out:
            return
        dx, dy = math.cos(self.ang), math.sin(self.ang)
        b = self.travel * self.out_p(t)
        produk(c, PC[0] - dx * b, SLOT_Y - dy * b, RED, look=LOOK, ghost=self.carry == "ghost")


def _grab_tip(ang, inset=22):
    """Fist front touching the box side it comes from."""
    dx, dy = math.cos(ang), math.sin(ang)
    return (PC[0] - dx * (PROD_W / 2 - inset), PC[1] + 30 - dy * (PROD_H / 2 - inset) * abs(dy))


class Cue:
    """Every time the hero reacts to, computed once from the voice — read this, not the draw code, to retime."""

    def __init__(self, T, b):
        self.b = b
        self.t_in = T["L01"].start - 0.1
        self.tepat = _w(T, "L01", "tepat", 0.15)
        self.bayar = _w(T, "L01", "bayar", 0.7)
        self.habis = _w(T, "L01", "habis", 0.95)
        self.fly0 = b[1] - 0.1
        self.land0 = self.fly0 + FLY
        # 00 keranjang
        self.satu = _w(T, "L03", "satu", 0.7)
        self.nunjuk = _w(T, "L04", "nunjuk", 0.45)
        self.megang = _w(T, "L04", "megang", 0.9)
        self.kunci = _w(T, "L05", "dikunci", 0.3)
        self.ribuan = _w(T, "L05", "ribuan", 0.55)
        # 01 checkout
        self.check = _w(T, "L06", "checkout", 0.35)
        self.r7 = T["L07"].start - 0.15
        self.detik = _w(T, "L07", "detik", 0.25)
        self.dua = _w(T, "L07", "dua", 0.65, nth=1)
        self.race = _w(T, "L07", "race", 0.85)
        self.r8 = T["L08"].start - 0.15
        self.lock = _w(T, "L08", "lock", 0.2)
        self.satu8 = _w(T, "L08", "satu", 0.35)
        self.nunggu = _w(T, "L08", "nunggu", 0.6)
        self.habis8 = _w(T, "L08", "habis", 0.95)
        # 02 antrean
        self.l9 = T["L09"].start
        self.l10 = T["L10"].start - 0.15
        self.dibayar = _w(T, "L10", "dibayar", 0.6)
        self.balik = _w(T, "L10", "balik", 0.85)
        self.land2 = self.balik + FLY
        # recap
        self.mau = _w(T, "L11", "mau", 0.35)
        self.menang = _w(T, "L11", "menang", 0.92)
        self.alamat = _w(T, "L12", "alamat", 0.2)
        self.metode = _w(T, "L12", "metode", 0.3)
        self.sebelum = _w(T, "L12", "sebelum", 0.45)

        grab = self.check + 0.1
        split = arrive(self.dua, "snappy")
        take8 = self.satu8 + 0.05
        mine = self.menang + 0.05
        self.slot = [(self.land0, grab), (self.r7, split), (self.r8, take8), (self.land2, mine)]
        self.labels = [(self.land0, "SISA 1", C["ink"]), (grab + 0.35, "HABIS", RED),
                       (self.r7, "SISA 1", C["ink"]), (split + 0.3, "SISA -1", RED),
                       (self.r8, "SISA 1", C["ink"]), (take8 + 0.35, "HABIS", RED),
                       (self.land2, "SISA 1", C["ink"]), (mine + 0.4, "PUNYAMU", YOU)]

        # the hands (rack-local), in draw order
        e06 = T["L06"].end
        self.you = Hand("point", (-PROD_W / 2 - 16, PC[1] + 8), 0.0, YOU, SKIN[1],
                        arrive(self.nunjuk, "snappy"), grab + 0.9, seed=1)
        crowd = [(-0.45, 150), (math.pi + 0.45, 150), (-1.1, 165), (math.pi + 1.1, 165), (-math.pi / 2, 182),
                 (math.pi, 128)]
        self.crowd = []
        for i, (a, r) in enumerate(crowd):
            tip = (PC[0] - math.cos(a) * r, PC[1] - math.sin(a) * r)
            self.crowd.append(Hand("point", tip, a, SLEEVE[(i + 1) % len(SLEEVE)], SKIN[i % len(SKIN)],
                                   follow(arrive(self.ribuan, "snappy"), i), grab + 0.45 + 0.06 * i, seed=10 + i))
        win_a = math.pi + 0.18
        self.winner = Hand("grab", _grab_tip(win_a), win_a, SLEEVE[0], SKIN[2], grab - 0.35, grab, carry="prod")
        self.race_a = Hand("grab", _grab_tip(0.0), 0.0, SLEEVE[2], SKIN[0], arrive(self.detik, "snappy") - 0.1, split,
                           carry="prod")
        self.race_b = Hand("grab", _grab_tip(math.pi), math.pi, SLEEVE[4], SKIN[3],
                           arrive(self.detik, "snappy") - 0.1, split, carry="ghost")
        t8 = arrive(self.lock, "snappy") + 0.45
        self.lock_a = Hand("grab", _grab_tip(0.0), 0.0, SLEEVE[5], SKIN[1], t8, take8, carry="prod")
        self.lock_b = Hand("grab", (PROD_W / 2 + 44, PC[1] + 30), math.pi, SLEEVE[1], SKIN[2], t8, self.habis8 + 0.3)
        self.you2 = Hand("point", (-PROD_W / 2 - 16, PC[1] + 8), 0.0, YOU, SKIN[1], arrive(self.mau, "snappy"),
                         mine - 0.45, seed=2)
        self.you_fist = Hand("grab", _grab_tip(0.0), 0.0, YOU, SKIN[1], mine - 0.3, mine, carry="prod", travel=150)
        self.hands = [self.you] + self.crowd + [self.winner, self.race_a, self.race_b, self.lock_a, self.lock_b,
                                                self.you2, self.you_fist]
        self.e06 = e06


def rack_state(Q, t):
    b = Q.b
    keys = [b[1] - 0.2, b[3] - 0.25, b[4] + 0.1]
    y = track(t, [(k, v[0]) for k, v in zip(keys, RACK_KEYS)], "hero")
    s = track(t, [(k, v[1]) for k, v in zip(keys, RACK_KEYS)], "hero")
    return MID, y, s


def to_screen(Q, t, lx, ly):
    x, y, s = rack_state(Q, t)
    return x + lx * s, y + ly * s, s


def build(project):
    T = project.timing
    v = Video(duration=T["L14"].end + TAIL, bpm=132, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="garage", key="D", mood="tense")
    v.sfx_kit = "glass"
    v.cover = lambda c: cover(c, "Udah di keranjang,\nkok *habis*?", kicker="FLASH SALE", color=RED,
                              tags=["keranjang", "checkout", "race condition"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(3):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    v.stage = lambda c, t: (draw_background(c, v, t), mat.stage(c, LOOK, RED, 1 - v.dark_amount(t)))
    v.finish = lambda c, t: mat.finish(c, LOOK, 1 - v.dark_amount(t))
    Q = Cue(T, b)
    phone_intro(v, T, Q)
    hero(v, T, Q)
    intro(v, T, Q, b[0], b[1])
    bab0(v, T, Q, b[1], b[2])
    bab1(v, T, Q, b[2], b[3])
    bab2(v, T, Q, b[3], b[4])
    recap(v, T, Q, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L14", RED,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="“Kalah war barang apa?”",
                               sub="Barang yang lolos dari keranjangmu."))
    v.cover_t = Q.ribuan + 1.2
    return v


# ── the hero: the rack, the box, the stock tag, the hands (all in rack-local space) ─────────────────────────────────
def _label(Q, t):
    cur, te = Q.labels[0][1:], Q.labels[0][0]
    for tt, text, ink in Q.labels:
        if t >= tt:
            cur, te = (text, ink), tt
    flip = abs(1 - 2 * clamp((t - te + 0.12) / 0.24))
    if t < Q.labels[0][0]:
        flip = 1.0
    return cur[0], cur[1], flip


def _slot_alpha(Q, t):
    for a, z in Q.slot:
        if a <= t < z:
            return clamp(prog(t, a, 0.2)) if a not in (Q.land0, Q.land2) else 1.0
    return 0.0


def draw_rack(c, t, Q, label=True):
    def stock(c, i, x0, y, w):
        if i != 1:
            filler(c, i, x0, y, w, seed=i + 3)
            return
        for sx in (-SPOT_DX, SPOT_DX):
            empty_spot(c, sx, y)
        produk(c, PC[0], SLOT_Y, RED, look=LOOK, alpha=_slot_alpha(Q, t))
    rak(c, RACK_W, RACK_H, ROWS, LOOK, stock)
    if label:
        text, ink, flip = _label(Q, t)
        label_stok(c, 0, TAG_Y, text, ink, flip, alpha=clamp(prog(t, Q.land0 - 0.2, 0.3)))


def hero(v, T, Q):
    b = Q.b

    def draw(c, t):
        op = 1 - prog(t, b[5] - OUT, OUT)
        x, y, s = rack_state(Q, t)
        p_in = ios_at(t, b[1] + 0.05, "hero")                 # after the phone has left: no double exposure
        y += 140 * (1 - p_in) * s
        with c.group(op * clamp(prog(t, b[1] + 0.05, 0.3))):
            with place(c, x, y, s):
                draw_rack(c, t, Q, label=False)
                # L05: the dashed "not locked" frame · L08: the solid lock frame
                fx, fy, fw, fh = -PROD_W / 2 - 36, PC[1] - PROD_H / 2 - 36, PROD_W + 72, PROD_H + 72
                a5 = clamp(prog(t, arrive(Q.kunci, "smooth"), 0.3)) * (1 - prog(t, Q.ribuan + 0.6, 0.3))
                if a5 > 0:
                    c.stroke_rrect(fx, fy, fw, fh, 30, C["ink2"], 4, a5, dash=[16, 12])
                if Q.r8 <= t < T["L08"].end + 0.4:
                    draw_on(c, t, arrive(Q.lock, "snappy"), pts_rrect(fx, fy, fw, fh, 30), C["ink"], width=7,
                            t_out=T["L08"].end)
                for h in Q.hands:
                    h.draw_carry(c, t)
                for h in Q.hands:
                    if h.live(t):
                        h.draw(c, t)
                text, ink, flip = _label(Q, t)
                label_stok(c, 0, TAG_Y, text, ink, flip, alpha=clamp(prog(t, Q.land0 - 0.2, 0.3)))
                if Q.r7 <= t < T["L07"].end + 0.3:
                    mark(c, t, Q.dua + 0.5, "circle", (-150, TAG_Y - 16, 300, 98), RED, width=6,
                         t_out=T["L07"].end)
    v.add(b[1] - 0.3, b[5] + 0.05, draw, z=10, bleed=True)

    # the box flies out of the cart (intro) and out of the unpaid order card (02) onto the shelf
    def fly(c, t, t0, src, grey0):
        p = curve("apple_in_out")(clamp(prog(t, t0, FLY)))
        sx, sy, ss = to_screen(Q, t, PC[0], SLOT_Y)
        x = lerp(src[0], sx, p)
        y = lerp(src[1], sy, p) - 160 * math.sin(math.pi * p)
        produk(c, x, y, RED, s=lerp(src[2], ss, p), look=LOOK, grey=grey0 * (1 - p))

    v.add(Q.fly0, Q.land0, lambda c, t: fly(c, t, Q.fly0, THUMB, 1.0), z=14)
    v.add(Q.balik, Q.land2, lambda c, t: fly(c, t, Q.balik, CARD_THUMB, 0.0), z=14)
    v.sfx("send", Q.fly0, 0.5)
    v.sfx("pop", Q.land0, 0.5)
    for h in Q.hands:
        v.sfx("whoosh", h.t_in, 0.25 if h.kind == "point" else 0.45)
        if h.carry == "prod":
            v.sfx("thud", h.t_out, 0.4)
    for tt, text, _ in Q.labels[1:]:
        v.sfx("click", tt, 0.5)
    v.sfx("chime", Q.land2, 0.6)
    v.sfx("click", arrive(Q.lock, "snappy"), 0.6)


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w / 900, h / 1000)

    class _Q:                       # a frozen moment: the box on the shelf, three hands pointing at it
        land0, land2 = -1.0, 99.0
        slot = [(-1.0, 99.0)]
        labels = [(-1.0, "SISA 1", C["ink"])]
    with place(c, x + w / 2, y + h / 2, s):
        draw_rack(c, 5.0, _Q)
        for a, r, sl in ((0.0, 106, YOU), (math.pi + 0.45, 150, SLEEVE[1]), (-0.45, 150, SLEEVE[2])):
            tangan(c, PC[0] - math.cos(a) * r, PC[1] - math.sin(a) * r, a, "point", sl, SKIN[1])


# ── INTRO: the phone everyone knows — 11.59.57 → 12.00.00, Bayar, "Stok habis" ─────────────────────────────────────
def _clock(Q, t):
    n = int(clamp(math.ceil((Q.tepat - t) / TICK), 0, 3))
    return "12.00.00" if n == 0 else "11.59.%02d" % (60 - n)


def draw_phone(c, t, Q):
    x, y, w, h = PH
    p_in = ios_at(t, Q.t_in, "hero")
    e = curve("apple_in")(clamp(prog(t, Q.b[1] - 0.15, 0.4)))
    op = clamp(prog(t, Q.t_in, 0.25)) * (1 - e)
    if op <= 0:
        return
    sc = lerp(1.06, 1.0, p_in) * lerp(1.0, 0.94, e)
    habis = ios_at(t, Q.habis, "snappy")
    gone = t >= Q.habis
    with c.group(op), c.at(0, 70 * (1 - p_in), sc, origin=(x + w / 2, y + h / 2)):
        c.shadow(x, y, w, h, 72, blur=60, dy=30, alpha=0.22)
        c.fill_rrect(x, y, w, h, 72, PHONE)
        c.fill_rrect(SX, SY, SW, SH, 60, C["card"])
        c.fill_rrect(x + w / 2 - 60, y + 34, 120, 34, 17, PHONE)
        # flash-sale pill + the clock
        c.fill_rrect(MID - 110, SY + 92, 220, 44, 22, RED)
        c.text(MID, SY + 122, "FLASH SALE", F["mono_bold"], 22, C["card"], 1, 0.12, align="c")
        on = t >= Q.tepat
        c.text(MID, SY + 250, _clock(Q, t), F["mono_bold"], 92, RED if on else C["ink"], 1, -0.02, align="c")
        # the cart
        c.text(SX + 32, SY + 345, "Keranjang", F["ui_semi"], 36, C["ink"])
        ra = 1 - 0.5 * habis
        c.card(SX + 24, SY + 372, SW - 48, 210, r=26, alpha=ra)
        if gone:
            c.circle(SX + 64, SY + 477, 18, C["faint"])
        else:
            check_badge(c, SX + 64, SY + 477, 18, 1.0)
        if t < Q.fly0:
            tx, ty, ts = THUMB
            produk(c, tx, ty, RED, s=ts, look=LOOK, grey=habis)
        else:
            empty_spot(c, THUMB[0], THUMB[1], THUMB[2])
        c.text(SX + 225, SY + 458, "Barang flash sale", F["ui_semi"], 28, C["ink"], ra)
        c.text(SX + 225, SY + 498, "1 barang", F["ui_reg"], 24, C["muted"], ra)
        c.fill_rrect(SX + 225, SY + 522, 140, 22, 11, RED, 0.22 * ra)
        # the pay button: press → spinner → dead
        bx, by, bw, bh = SX + 24, SY + SH - 140, SW - 48, 100
        with c.at(0, 0, press(t, Q.bayar), origin=(bx + bw / 2, by + bh / 2)):
            c.fill_rrect(bx, by, bw, bh, 50, mix(RED, C["faint"], habis))
            if t < Q.bayar + 0.12:
                c.text(MID, by + 62, "Bayar sekarang", F["ui_bold"], 36, C["card"], align="c")
            elif not gone:
                ctx = c.ctx
                ctx.new_path()
                a0 = (t - Q.bayar) * 7
                ctx.arc(MID, by + bh / 2, 22, a0, a0 + 4.2)
                c.src(C["card"])
                ctx.set_line_width(6)
                ctx.stroke()
        # the sheet that ends it
        if gone:
            top = SY + SH - 330 + 120 * (1 - habis)
            with c.group(clamp(habis * 1.4)):
                c.card(SX + 16, top, SW - 32, 300, r=44)
                c.circle(SX + 84, top + 84, 32, RED)
                for sgn in (-1, 1):
                    c.line(SX + 72, top + 84 - 12 * sgn, SX + 96, top + 84 + 12 * sgn, C["card"], 6)
                c.text(SX + 136, top + 102, "Stok habis", F["display"], 52, C["ink"], 1, -0.03)
                c.text(SX + 52, top + 190, "Barang ini udah nggak tersedia.", F["ui_reg"], 26, C["muted"])
                c.fill_rrect(SX + 52, top + 222, SW - 136, 50, 25, C["bg"])
                c.text(MID, top + 255, "Oke", F["ui_semi"], 26, C["ink2"], align="c")


def phone_intro(v, T, Q):
    v.add(Q.t_in, Q.b[1] + 0.3, lambda c, t: draw_phone(c, t, Q), z=12)
    for k in (3, 2, 1):
        v.sfx("tick", Q.tepat - k * TICK, 0.5)
    v.sfx("pop", Q.tepat, 0.6)
    v.sfx("click", Q.bayar, 0.7)
    v.sfx("thud", Q.habis, 0.8)


def intro(v, T, Q, s, e):
    hs = heads(T, [("Udah di keranjang,\ntetap *habis*.", "L01"), ("Nggak pernah\njadi *milikmu*.", "L02")], e - OUT)

    def draw(c, t):
        kicker(c, t, T["L01"].start, e - OUT, "FLASH SALE", RED)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
    v.add(s, e, draw, z=20)
    dolly(v, Q.habis + 0.6, e - 0.2)


# ── 00: one box left · your finger · then everybody's ─────────────────────────────────────────────────────────────────
def bab0(v, T, Q, s, e):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("Sisa *satu*.", "L03"), ("Keranjang =\ncuma *nunjuk*.", "L04"),
                   ("Stock-nya nggak\n*dikunci*.", "L05")], e - OUT)
    t_kamu = Q.you.t_in + 0.35
    t_dik = arrive(Q.kunci, "smooth") + 0.15

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[1], col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        if t_kamu <= t < Q.ribuan:
            x, y, _ = to_screen(Q, t, -PROD_W / 2 - 300, PC[1] - 70)
            _tag(c, t,t_kamu, X + 10, y, "kamu", YOU)
        if t_dik <= t < Q.ribuan + 0.6:
            x, y, _ = to_screen(Q, t, -PROD_W / 2 - 36, PC[1] - PROD_H / 2 - 100)
            _tag(c, t,t_dik, x, y, "nggak dikunci", C["ink2"])
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", t_kamu, 0.4)
    v.sfx("pop", t_dik, 0.4)
    dolly(v, Q.land0 + 0.6, Q.you.t_in - 0.1, base=1.0)


# ── 01: checkout = who reaches the till first · the race · the lock ───────────────────────────────────────────────────
def bab1(v, T, Q, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("Yang nentuin:\ndetik *checkout*.", "L06"), ("Satu barang,\nkejual *dua kali*.", "L07"),
                   ("Satu-satu.\nSisanya *nunggu*.", "L08")], e - OUT)
    t_race = arrive(Q.race, "snappy")
    t_wait = arrive(Q.nunggu, "snappy")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[2], col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        for r0, r1 in ((Q.r7, T["L07"].end), (Q.r8, T["L08"].end)):
            if r0 <= t < r1:
                _tag(c, t,r0, X + CW, 575, "REPLAY · detik yang sama", C["ink2"], align="r")
        if t_race <= t < T["L07"].end:
            x, y, _ = to_screen(Q, t, 0, TAG_Y + 120)
            _tag(c, t,t_race, x - 110, y, "race condition", RED)
        if Q.r8 <= t < T["L08"].end:
            x, y, _ = to_screen(Q, t, -PROD_W / 2 - 36, PC[1] - PROD_H / 2 - 100)
            _tag(c, t,arrive(Q.lock, "snappy") + 0.2, x, y, "lock", C["ink"])
        if t_wait <= t < T["L08"].end:
            x, y, _ = to_screen(Q, t, PROD_W / 2 + 60, PC[1] + 120)
            _tag(c, t,t_wait, x, y, "nunggu…", WAIT)
    v.add(s, e, draw, z=20)
    cut(v, s)
    cut(v, Q.r7, zoom=1.04)
    cut(v, Q.r8, zoom=1.0)
    v.sfx("whoosh", Q.r7, 0.4)
    v.sfx("whoosh", Q.r8, 0.4)
    v.sfx("pop", t_race, 0.5)
    v.sfx("tick", t_wait, 0.5)


# ── 02: the waiting room is on purpose · unpaid orders put the box back ──────────────────────────────────────────────
def _queue(c, t, t0, x0, y, gate):
    """Dots walking to a gate one step at a time (pure function of t)."""
    k = max(0.0, (t - t0) / Q_STEP)
    n = int(k)
    move = n + ios_at(t, t0 + n * Q_STEP, "snappy")
    for j in range(22):
        qx = gate - 40 - j * Q_GAP + move * Q_GAP
        if qx < x0 - 20:
            continue
        a = clamp((qx - x0) / 60) * (1 - clamp((qx - gate) / 50))
        if a <= 0:
            continue
        c.circle(qx, y, Q_R + (3 if j == 9 else 0), YOU if j == 9 else SLEEVE[j % len(SLEEVE)], a)


def bab2(v, T, Q, s, e):
    col = tk.CHAPTER[2][0]
    hs = heads(T, [("Ruang tunggu itu\n*sengaja*.", "L09"), ("Habis, terus\n*muncul lagi*.", "L10")], e - OUT)
    cx, cy, cw, ch = CARD
    gate = cx + cw - 150
    t_strike = arrive(Q.dibayar, "snappy")

    def waiting(c, t):
        c.card(cx, cy, cw, ch, r=36)
        ctx = c.ctx
        ctx.new_path()
        a0 = t * 5
        ctx.arc(cx + 70, cy + 72, 28, a0, a0 + 4.4)
        c.src(RED)
        ctx.set_line_width(7)
        ctx.stroke()
        c.text(cx + 124, cy + 70, "Ruang tunggu", F["ui_semi"], 36, C["ink"])
        c.text(cx + 124, cy + 108, "Kamu lagi di antrean…", F["ui_reg"], 26, C["muted"])
        c.fill_rrect(cx + 30, cy + 178, gate - cx - 30, 6, 3, C["faint"])
        c.fill_rrect(gate - 4, cy + 146, 8, 70, 4, C["ink2"])
        c.fill_rrect(gate + 30, cy + 150, 100, 62, 14, C["ink"])
        c.text(gate + 80, cy + 189, "server", F["mono_med"], 20, C["card"], align="c")
        _queue(c, t, Q.l9, cx + 30, cy + 166, gate)

    def order(c, t):
        c.card(cx, cy, cw, ch, r=36)
        if t < Q.balik:
            produk(c, CARD_THUMB[0], CARD_THUMB[1], RED, s=CARD_THUMB[2], look=LOOK)
        else:
            empty_spot(c, CARD_THUMB[0], CARD_THUMB[1], CARD_THUMB[2])
        c.text(cx + 190, cy + 80, "Pesanan orang lain", F["ui_semi"], 34, C["ink"])
        lab = "Menunggu pembayaran"
        lw = c.measure(lab, F["ui_semi"], 26)[0] + 44
        c.fill_rrect(cx + 190, cy + 108, lw, 50, 25, WAIT, 0.14)
        c.text(cx + 212, cy + 142, lab, F["ui_semi"], 26, WAIT)
        strike(c, t, t_strike, cx + 200, cx + 180 + lw, cy + 133, width=6)
        _tag(c, t, t_strike + 0.35, cx + 190, cy + 176, "nggak dibayar → batal", RED)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[3], col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        p1 = ios_at(t, s + 0.2, "smooth")
        a1 = clamp(prog(t, s + 0.2, 0.3)) * (1 - prog(t, Q.l10 - 0.2, 0.3))
        if a1 > 0:
            with c.group(a1), c.at(0, 60 * (1 - p1)):
                waiting(c, t)
        p2 = ios_at(t, Q.l10, "smooth")
        a2 = clamp(prog(t, Q.l10, 0.3)) * (1 - prog(t, e - OUT, OUT))
        if a2 > 0:
            with c.group(a2), c.at(0, 60 * (1 - p2)):
                order(c, t)
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("whoosh", s + 0.2, 0.4)
    v.sfx("whoosh", Q.l10, 0.4)
    v.sfx("click", t_strike, 0.6)
    dolly(v, Q.l9 + 0.8, Q.l10 - 0.3, base=1.0)


# ── RECAP (dark): your finger again — and this time your fist wins · two things to prepare ──────────────────────────
def recap(v, T, Q, s, e):
    hs = heads(T, [("Keranjang =\n*aku mau*.", "L11"), ("Siapin *sebelum*\njamnya mulai.", "L12")], e - OUT,
               style="headline_dark")
    chips = [("alamat", Q.alamat, 0), ("metode bayar", Q.metode, 0), ("sebelum 12.00", Q.sebelum, 1)]

    def chip(c, t, t0, label, row, rowmates):
        f = F["ui_semi"]
        widths = [c.measure(lb, f, 28)[0] + 96 for lb, _, r in chips if r == row]
        total = sum(widths) + 20 * (len(widths) - 1)
        x = MID - total / 2 + sum(widths[:rowmates]) + 20 * rowmates
        w = widths[rowmates]
        y = 1330 + row * 84
        p = ios_at(t, t0, "snappy")
        with c.group(clamp(prog(t, t0, 0.2)) * (1 - prog(t, e - OUT, OUT))), c.at(0, 24 * (1 - p)):
            c.fill_rrect(x, y, w, 64, 32, C["d_card"])
            c.stroke_rrect(x, y, w, 64, 32, C["d_line"], 2)
            check_badge(c, x + 36, y + 32, 17, p)
            c.text(x + 66, y + 42, label, f, 28, C["d_ink"])

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", RED)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        for row in (0, 1):
            k = 0
            for label, t0, r in chips:
                if r != row:
                    continue
                if t >= t0:
                    chip(c, t, arrive(t0, "snappy"), label, row, k)
                k += 1
    v.add(s, e, draw, z=20)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    for _, t0, _ in chips:
        v.sfx("pop", arrive(t0, "snappy"), 0.5)
    dolly(v, Q.menang + 0.8, e - 0.2)
    cut(v, e)
