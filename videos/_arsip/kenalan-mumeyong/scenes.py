"""Kenalan: aku Mumeyong — the channel intro (pinned). See IDENTITY.md / TREATMENT.md.

Metaphor: the architect's floor plan. Signature move: lines draw first, then fill (become real). Color: teal.
Hook: a specific question. Structure: intro → three real numbers → the channel as a city map (surprise pull-out).
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, note, follow_button,
                               server_rack, bp_grid, bp_house, house_rooms, outline_text, dimension, phone_wire,
                               city_map, cover, TEAL)
from engine.components.infra import _draw_poly, _along

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · KENALAN", "01 · TIGA ANGKA", "02 · DI SINI", "RECAP", "OUTRO"]
OK = C["ok"]
WHITE = (1, 1, 1, 1)


def build(project):
    T = project.timing
    v = Video(duration=T["L19"].end + TAIL, bpm=128, beat_offset=0.0, series="KENALAN")
    v.cover_t = T.word("L04", "Mumeyong") + 1.0
    v.music = dict(key="G", mood="bright")            # generated score: optimistic introduction
    v.cover = lambda c: cover(c, "Kenalan: aku *Mumeyong*.", kicker="CLOUD ENGINEER", color=TEAL, badge="KENALAN",
                              tags=["4 cloud", "10.000 request", "$14.000/bln"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    intro(v, T, 0.0, b["00 · KENALAN"])
    kenalan(v, T, b["00 · KENALAN"], b["01 · TIGA ANGKA"])
    angka(v, T, b["01 · TIGA ANGKA"], b["02 · DI SINI"])
    disini(v, T, b["02 · DI SINI"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


def _cover_hero(c, box):
    """Cover hero: the finished floor plan on blueprint paper, server room lit, bill dimension."""
    x, y, w, h = box
    bp_grid(c, x, y, w, h)
    hx, hy, hw, hh = x + 70, y + 60, w - 140, h - 150
    rooms = bp_house(c, hx, hy, hw, hh, 1.0, p_fill=1.0)
    sx, sy, sw, sh = rooms[1]
    for k in range(3):
        c.fill_rrect(sx + sw / 2 - 60, sy + sh / 2 - 50 + k * 36, 120, 28, 6, TEAL)
    dimension(c, hx, hy + hh + 50, hx + hw, hy + hh + 50, "$ / bulan", 1.0)


def _pop(c, t, t0, cx, cy, draw, d=0.4):
    """Small element popping in at t0 (overshoot), drawn around (cx, cy)."""
    if t < t0:
        return
    p = out_back(prog(t, t0, d), 1.7)
    with c.at(0, 0, max(0.01, p), origin=(cx, cy)):
        with c.group(clamp(p * 2)):
            draw(c)


def _tag_w(c, label):
    return c.measure(label, F["ui"], tk.T["tag"][0], tk.T["tag"][1])[0] + 30


# ── INTRO: three apps → "who decides where they run?" → that's my job ──
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    t_app = [T.word("L01", "bank"), T.word("L01", "tiket"), T.word("L01", "QRIS")]
    t_mana = T.word("L02", "mana")
    t_job = T.word("L03", "kerjaanku")
    t_eng = T.word("L03", "cloud")
    heads = [(Headline("Bank. Tiket. *QRIS*."), L1.start, L2.start - 0.15),
             (Headline("Jalan *di mana*?"), L2.start, L3.start - 0.15),
             (Headline("Itu *kerjaanku*."), L3.start, e - OUT)]
    card = (X, 560, CW, 760)
    px = [X + CW * f for f in (0.2, 0.5, 0.8)]
    py, ps = 770, 260
    kinds = [("bank", "bank"), ("ticket", "tiket"), ("qris", "QRIS")]
    box = (MID - 170, 1110, 340, 130)
    routes = [[(x_, py + ps / 2 + 60), (x_, 1040), (MID, 1040), (MID, box[1])] for x_ in px]

    cam = v.camera
    cam.key(0.0, zoom=1.06, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.focus(t_job - 0.2, (box[0], box[1] - 200, box[2], box[3] + 240), zoom=1.08, dur=0.5)
    cam.reset(L3.end, dur=0.5)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "CLOUD ENGINEER", TEAL)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        fill = out_expo(prog(t, t_job, 0.5))

        def paper(c):
            bp_grid(c, *card)
            for k, (kind, lbl) in enumerate(kinds):
                phone_wire(c, px[k], py, ps, prog(t, t_app[k] - 0.15, 0.7), kind, lbl, fill=fill)
            pr = in_out_cubic(prog(t, t_mana - 0.5, 0.8))
            for k, r in enumerate(routes):
                _draw_poly(c, r, clamp(pr * 1.2 - k * 0.1), TEAL, 3, 0.8)
            if pr > 0:
                bx, by, bw, bh = box
                c.stroke_rrect(bx, by, bw, bh, 18, TEAL, 3, clamp(pr * 2) * (1 - fill), dash=[12, 10])
                c.text(bx + bw / 2, by + bh / 2 + 10, "server ?", F["mono_bold"], 30, TEAL, clamp(pr * 2) * (1 - fill),
                       0.04, align="c")
                if fill > 0:
                    c.fill_rrect(bx, by, bw, bh, 18, TEAL, fill)
                    c.text(bx + bw / 2, by + bh / 2 + 14, "cloud", F["display_semi"], 48, WHITE, fill, -0.03, align="c")
                    for k, r in enumerate(routes):
                        f = (t * 0.5 + k / 3) % 1.0
                        dx, dy = _along(r, f)
                        c.circle(dx, dy, 7, TEAL, fill * min(1, f * 6, (1 - f) * 6))
            w = _tag_w(c, "cloud engineer")
            _pop(c, t, t_eng, MID, 1280, lambda c: tag(c, MID - w / 2, 1262, "cloud engineer", TEAL, h=40))
        appear(c, t, L1.start - 0.1, e - OUT, card, paper, enter="up")
    v.add(s, e + 0.4, draw)
    for tt in t_app:
        v.sfx("pop", tt, 0.45)
    v.sfx("whoosh", t_mana - 0.5, 0.5)
    v.sfx("thud", t_job, 0.7)
    v.sfx("pop", t_eng, 0.4)


# ── 00 · KENALAN: name → floor plan → then/now ─────────────────────────
def kenalan(v, T, s, e):
    ch = v.chapter(0, "KENALAN", s, e)
    L4, L5, L7 = T["L04"], T["L05"], T["L07"]
    t_name = T.word("L04", "Mumeyong")
    t_dev = T.word("L05", "developer")
    t_denah = T.word("L05", "denahnya")
    t_srv = T.word("L06", "server-nya")
    t_jalan = T.word("L06", "jalannya")
    t_bill = T.word("L06", "tagihan")
    t_dulu = T.word("L07", "dulu")
    t_now = T.word("L07", "sekarang")
    t_perlu = T.word("L07", "perlu")
    head1 = Headline("Aku gambar *denahnya*.")
    head2 = Headline("Sekarang aku yang *mutusin*.")
    card = (X, 590, CW, 740)
    hx, hy, hw, hh = X + 100, 690, CW - 200, 470
    rooms = house_rooms(hx, hy, hw, hh)
    colw = (CW - 48) / 2
    left = (X, 620, colw, 600)
    right = (X + colw + 48, 620, colw, 600)

    cam = v.camera
    cam.focus(L5.start + 0.2, card, zoom=1.04, dur=1.0)
    cam.reset(L7.start - 0.3, dur=0.5)
    cam.focus(t_perlu - 0.3, right, zoom=1.06, dur=0.5)
    cam.reset(e - 0.6, dur=0.5)

    def draw(c, t):
        kicker(c, t, L4.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L5.start, L7.start - 0.15)
        head2.draw(c, t, L7.start, e - OUT)

        def name(c):
            outline_text(c, MID, 1010, "Mumeyong.", F["display"], 160, prog(t, L4.start - 0.1, 0.8),
                         prog(t, t_name + 0.3, 0.5), align="c", width=3)
            c.text(MID, 1090, "cloud engineer · mumeyong.dev", F["mono_med"], 26, c.theme("ink2", "d_muted"),
                   out_expo(prog(t, t_name + 0.5, 0.5)), 0.08, align="c")
        appear(c, t, L4.start - 0.2, L5.start - 0.15, (X, 860, CW, 260), name, enter="up", blur=4)

        def plan(c):
            bp_grid(c, *card)
            bp_house(c, hx, hy, hw, hh, prog(t, L5.start + 0.1, 1.6), p_fill=prog(t, t_denah, 0.6),
                     scribble=prog(t, L5.start + 0.5, 1.4))
            # annotations: server room · route from the door · electricity bill
            sx, sy, sw, sh = rooms[1]
            sp = out_back(prog(t, t_srv, 0.4), 1.6) if t >= t_srv else 0
            if sp > 0:
                cx_, cy_ = sx + sw / 2, sy + sh / 2
                with c.at(0, 0, max(0.01, sp), origin=(cx_, cy_)):
                    for k in range(3):
                        c.fill_rrect(cx_ - 60, cy_ - 50 + k * 36, 120, 28, 6, TEAL)
                        c.circle(cx_ + 40, cy_ - 36 + k * 36, 5, WHITE)
                c.text(cx_, sy + sh - 24, "server", F["mono_bold"], 20, TEAL, clamp(sp), 0.1, align="c")
            rp = in_out_cubic(prog(t, t_jalan - 0.1, 0.8))
            if rp > 0:
                door_y = hy + hh * 0.36
                route = [(hx - 60, door_y), (hx + hw * 0.3, door_y), (hx + hw * 0.3, sy + sh * 0.72),
                         (sx + sw / 2 - 70, sy + sh * 0.72)]
                c.ctx.set_dash([12, 10])
                _draw_poly(c, route, rp, C["accent"], 4)
                c.ctx.set_dash([])
                c.text(hx + hw * 0.3 - 16, door_y - 18, "jalur", F["mono_bold"], 20, C["accent"], clamp(rp * 2), 0.1,
                       align="r")
            bx, by, bw, bh = rooms[2]
            bp = prog(t, t_bill, 0.6)
            if bp > 0:
                mx, my = bx + bw * 0.75, by + bh / 2
                c.stroke_rrect(mx - 50, my - 50, 100, 100, 50, TEAL, 3, clamp(bp * 3))
                ang = -2.4 + 3.4 * out_expo(bp)
                c.line(mx, my, mx + 38 * math.cos(ang), my + 38 * math.sin(ang), C["rec"], 4, clamp(bp * 3))
                c.text(mx, my + 82, "tagihan listrik", F["mono_bold"], 18, TEAL, clamp(bp * 3), 0.08, align="c")
            dimension(c, hx, hy + hh + 50, hx + hw, hy + hh + 50, "$ / bulan", prog(t, t_bill + 0.3, 0.7))
            if t >= t_dev:
                _pop(c, t, t_dev, X + 40, 1290, lambda c: tag(c, X + 40, 1270, "developer → rumahnya", C["accent"], h=40))
            w = _tag_w(c, "aku → denahnya")
            _pop(c, t, t_denah, X + CW - 40 - w / 2,
                 1290, lambda c: tag(c, X + CW - 40, 1270, "aku → denahnya", TEAL, align="r", h=40))
        appear(c, t, L5.start - 0.1, L7.start - 0.15, card, plan, enter="up", exit="left")

        def then(c):
            x, y, w, h = left
            c.card(x, y, w, h, r=26)
            outline_text(c, x + 32, y + 120, "2020", F["display"], 100, prog(t, t_dulu - 0.1, 0.6),
                         prog(t, t_dulu + 0.4, 0.4))
            server_rack(c, x + 32, y + 170, w - 64, 300, t, units=4, seed=3)
            c.text(x + 32, y + h - 40, "jagain server", F["serif"], 44, c.theme("ink2", "d_muted"),
                   out_expo(prog(t, t_dulu + 0.3, 0.4)))
        appear(c, t, L7.start - 0.1, e - OUT, left, then, enter="up")

        def now(c):
            x, y, w, h = right
            c.card(x, y, w, h, r=26)
            outline_text(c, x + 32, y + 110, "sekarang", F["display"], 72, prog(t, t_now - 0.1, 0.6),
                         prog(t, t_now + 0.4, 0.4), fill=TEAL)
            server_rack(c, x + 32, y + 170, w - 64, 220, t, dashed=True)
            c.text(x + w / 2, y + 290, "perlu?", F["display_semi"], 44, TEAL, out_expo(prog(t, t_now + 0.3, 0.4)),
                   -0.02, align="c")
            pk = prog(t, t_perlu, 0.4)
            for k, (col, cx_) in enumerate(((OK, x + w / 2 - 70), (C["rec"], x + w / 2 + 70))):
                cy_ = y + 450
                hl = pk if k == 0 else 0
                c.circle(cx_, cy_, 36 + 6 * out_back(hl, 2) * (hl > 0), col, 0.25 + 0.75 * (hl if k == 0 else 0.3))
                if k == 0:
                    icons.check(c, cx_, cy_, 28, WHITE, 4)
                else:
                    c.line(cx_ - 12, cy_ - 12, cx_ + 12, cy_ + 12, WHITE, 4)
                    c.line(cx_ - 12, cy_ + 12, cx_ + 12, cy_ - 12, WHITE, 4)
            c.text(x + 32, y + h - 40, "mutusin", F["serif"], 44, TEAL, out_expo(prog(t, t_perlu + 0.2, 0.4)))
        appear(c, t, t_now - 0.2, e - OUT, right, now, enter="up")
        fade(c, t, t_dulu + 0.6, e - OUT,
             lambda c: note(c, MID, 1300, "ini aku, dulu", prog(t, t_dulu + 0.6, 0.8),
                            arrow_to=(left[0] + left[2] / 2, left[1] + left[3] + 10), size=36))
    v.add(s, e, draw)
    v.sfx("whoosh", L4.start - 0.1, 0.5)
    v.sfx("thud", t_name + 0.3, 0.6)
    for k in range(6):
        v.sfx("tick", L5.start + 0.1 + k * 0.27, 0.3)
    v.sfx("pop", t_dev, 0.4)
    v.sfx("pop", t_denah, 0.5)
    v.sfx("pop", t_srv, 0.4)
    v.sfx("whoosh", t_jalan - 0.1, 0.3)
    v.sfx("pop", t_bill, 0.4)
    v.sfx("whoosh", L7.start - 0.15, 0.5)
    v.sfx("pop", t_now, 0.4)
    v.sfx("click", t_perlu, 0.7)


# ── 01 · TIGA ANGKA: three real numbers, each drawn then filled ────────
def angka(v, T, s, e):
    ch = v.chapter(1, "TIGA ANGKA", s, e)
    L8 = T["L08"]
    t_tiga = T.word("L08", "tiga")
    t_n = [T.word("L09", "empat"), T.word("L10", "sepuluh"), T.word("L11", "empat")]
    t_prov = [T.word("L09", "AWS"), T.word("L09", "Azure"), T.word("L09", "Google"), T.word("L09", "Alibaba")]
    t_jalan = T.word("L10", "jalan")
    t_bulan = T.word("L12", "bulan")
    head = Headline("Tiga *angka*.")
    sy = [560, 800, 1040]
    SH = 220
    provs = ["AWS", "Azure", "Google Cloud", "Alibaba Cloud"]

    cam = v.camera
    for k in range(3):
        cam.focus(t_n[k] - 0.2, (X, sy[k], CW, SH), zoom=1.04, dur=0.6)
    cam.key(t_bulan, zoom=0.97, dur=0.12)
    cam.key(t_bulan + 0.12, zoom=1.0, dur=0.5)

    def draw(c, t):
        kicker(c, t, L8.start - 0.2, e - OUT, ch.kicker, ch.color)
        head.draw(c, t, L8.start, e - OUT)
        ink2 = c.theme("ink2", "d_muted")

        def slots(c):
            for k in range(3):
                a = out_expo(prog(t, t_tiga + k * 0.12, 0.4))
                filled = prog(t, t_n[k] + 0.5, 0.5)
                c.stroke_rrect(X, sy[k], CW, SH, 26, TEAL, 2.5, a * (1 - 0.7 * filled), dash=[12, 10])
                if filled > 0:
                    c.card(X, sy[k], CW, SH, r=26, alpha=filled)
                c.text(X + CW - 30, sy[k] + 40, f"0{k + 1}", F["mono_bold"], 18, TEAL, a, 0.14, align="r")
            # 1 · four clouds
            outline_text(c, X + 40, sy[0] + 178, "4", F["display"], 190, prog(t, t_n[0] - 0.2, 0.6),
                         prog(t, t_n[0] + 0.4, 0.4), fill=TEAL)
            c.text(X + 200, sy[0] + 96, "cloud", F["display_semi"], 60, c.theme("ink", "d_ink"),
                   out_expo(prog(t, t_n[0] + 0.3, 0.4)), -0.03)
            tx = X + 200
            for k, (lbl, tt) in enumerate(zip(provs, t_prov)):
                w = _tag_w(c, lbl)
                _pop(c, t, tt, tx + w / 2, sy[0] + 150, lambda c, tx=tx, lbl=lbl: tag(c, tx, sy[0] + 130, lbl, TEAL, h=40))
                tx += w + 10
            # 2 · 10.000 concurrent requests
            outline_text(c, X + 40, sy[1] + 150, "10.000", F["display"], 140, prog(t, t_n[1] - 0.2, 0.7),
                         prog(t, t_n[1] + 0.5, 0.4))
            c.text(X + 42, sy[1] + 198, "request barengan", F["ui_semi"], 30, ink2, out_expo(prog(t, t_n[1] + 0.6, 0.4)),
                   -0.01)
            w = _tag_w(c, "tetap jalan")
            _pop(c, t, t_jalan, X + CW - 40 - w / 2, sy[1] + 120,
                 lambda c: tag(c, X + CW - 40, sy[1] + 100, "tetap jalan", OK, align="r", h=44))
            # 3 · $14.000 saved — per month
            outline_text(c, X + 40, sy[2] + 150, "$14.000", F["display"], 140, prog(t, t_n[2] - 0.2, 0.8),
                         prog(t, t_n[2] + 0.6, 0.4), fill=TEAL)
            c.text(X + 42, sy[2] + 198, "biaya cloud turun", F["ui_semi"], 30, ink2,
                   out_expo(prog(t, t_n[2] + 0.7, 0.4)), -0.01)
            bp = prog(t, t_bulan - 0.05, 0.3)
            if bp > 0:
                with c.at(0, 0, 1 + 0.6 * (1 - out_expo(bp)), origin=(X + CW - 40, sy[2] + 120)):
                    c.text(X + CW - 40, sy[2] + 140, "/ bulan", F["serif"], 76, TEAL, clamp(bp * 3), align="r")
        appear(c, t, L8.start, e - OUT, (X, sy[0], CW, sy[2] + SH - sy[0]), slots, blur=4, rise=20)
    v.add(s, e, draw)
    for k in range(3):
        v.sfx("pop", t_tiga + k * 0.12, 0.35)
    for tt in t_prov:
        v.sfx("pop", tt, 0.35)
    v.sfx("thud", t_n[0] + 0.4, 0.5)
    v.sfx("thud", t_n[1] + 0.5, 0.5)
    v.sfx("chime", t_jalan, 0.6)
    v.sfx("thud", t_n[2] + 0.6, 0.6)
    v.sfx("thud", t_bulan)


# ── 02 · DI SINI: pull out from the house → the channel's city map ─────
BLOCKS = [  # col, row, label, sub, key word that lights it
    (0, 0, "bank down\npas gajian", "BROAD", ("L14", "gajian")),
    (1, 0, "war tiket\nkonser", "BROAD", ("L14", "crash")),
    (2, 0, "QRIS\n2 detik", "BROAD", ("L13", "tiap")),
    (0, 1, "Bongkar\nArsitektur", "EP01–EP07", ("L13", "bongkar")),
    (2, 1, "biaya cloud\nbocor", "BROAD", ("L13", "hari")),
    (0, 2, "karier\ncloud", "KARIER", ("L15", "karier")),
    (1, 2, "roadmap", "KARIER", ("L15", "beneran")),
    (2, 2, "interview\ncloud", "KARIER", ("L15", "jalanin")),
]


def disini(v, T, s, e):
    ch = v.chapter(2, "DI SINI", s, e)
    L13, L15 = T["L13"], T["L15"]
    head1 = Headline("Aku *bongkar* sistemnya.")
    head2 = Headline("Plus karier *cloud*.")
    mp = (X, 560, CW, 800)
    pad, street = 30, 34
    bw = (CW - 2 * pad - street * 2) / 3
    bh = (mp[3] - 2 * pad - street * 2) / 3
    center = (X + pad + bw + street, mp[1] + pad + bh + street, bw, bh)
    t_out = L13.start + 0.2

    cam = v.camera
    cam.focus(s, center, zoom=1.22, dur=0.01)
    cam.key(t_out, zoom=1.0, dur=1.8)

    def draw(c, t):
        kicker(c, t, L13.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L13.start, L15.start - 0.15)
        head2.draw(c, t, L15.start, e - OUT)

        def city(c):
            blocks = [dict(col=1, row=1, draw=1.0, lit=0.0)]
            for k, (col, row, lbl, sub, (lid, word)) in enumerate(BLOCKS):
                blocks.append(dict(col=col, row=row, label=lbl, sub=sub, draw=prog(t, t_out + 0.3 + k * 0.08, 0.6),
                                   lit=out_expo(prog(t, T.word(lid, word), 0.4))))
            city_map(c, *mp, blocks, pin=(1, 1), pin_p=prog(t, t_out + 1.4, 0.4))
            cx_, cy_, cw_, chh = center
            bp_house(c, cx_ + 24, cy_ + 34, cw_ - 48, chh - 68, 1.0, p_fill=1.0, width=3)
        appear(c, t, s + 0.1, e - OUT, mp, city, enter="up", blur=4, rise=10)
        fade(c, t, t_out + 1.6, e - OUT, lambda c: note(c, center[0] + center[2] / 2, center[1] + center[3] + 26,
                                                         "kamu di sini", prog(t, t_out + 1.6, 0.8), size=34,
                                                         align="l"))
    v.add(s, e, draw)
    v.sfx("whoosh", t_out, 0.7)
    v.sfx("pop", t_out + 1.4, 0.5)
    for (_, _, _, _, (lid, word)) in BLOCKS:
        v.sfx("pop", T.word(lid, word), 0.3)


# ── RECAP (dark): classic blueprint, the missing room slides in ────────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L16, L17 = T["L16"], T["L17"]
    t_pas = T.word("L17", "pas")
    head1 = Headline("Bukan yang paling *canggih*.", style="headline_dark")
    head2 = Headline("Tapi yang paling *pas*.", style="headline_dark")
    card = (X, 620, CW, 760)
    hx, hy, hw, hh = X + 110, 720, CW - 220, 520

    cam = v.camera
    cam.focus(t_pas - 0.4, house_rooms(hx, hy, hw, hh)[1], zoom=1.1, dur=0.5)
    cam.reset(t_pas + 0.9, dur=0.6)

    def draw(c, t):
        head1.draw(c, t, L16.start, L17.start - 0.15)
        head2.draw(c, t, L17.start, e - OUT)

        def plan(c):
            bp_grid(c, *card)
            bp_house(c, hx, hy, hw, hh, prog(t, L16.start, 1.4), p_fill=prog(t, L16.start + 1.2, 0.6),
                     fit=(1, prog(t, t_pas - 0.3, 0.6)))
            rx, ry, rw, rh = house_rooms(hx, hy, hw, hh)[1]
            mx, my = rx + rw / 2, ry + rh / 2

            def tick(c):
                c.circle(mx, my, 30, OK)
                icons.check(c, mx, my, 24, WHITE, 4)
            _pop(c, t, t_pas + 0.3, mx, my, tick)
        appear(c, t, L16.start - 0.1, e - OUT, card, plan, enter="up")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("click", t_pas + 0.3, 0.8)
    v.sfx("chime", t_pas + 0.35)


# ── OUTRO: logo + next video + follow ──────────────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L18, L19 = T["L18"], T["L19"]
    t_click = T.word("L19", "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, TEAL)
            c.text(X + 50, 892, "VIDEO BERIKUTNYA", F["mono_bold"], 20, TEAL, 1, 0.16)
            c.text(X + 50, 962, "Kenapa app bank down", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "pas tanggal gajian?", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L18.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L19.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "mumeyong.dev", F["mono_med"], 28,
                                                          C["d_muted"], 1, 0.06, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L19.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L18.start, 0.5)
    v.sfx("chime", t_click + 0.1)
