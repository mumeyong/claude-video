"""Kenapa app bank down pas tanggal gajian? — idea #06, pillar B, QUICK. See IDENTITY.md / TREATMENT.md.

Metaphor: the payday supermarket checkout + ONE ledger (buku kas). Signature move: a sheet gets torn off
(calendar pages, a cleared suspect card, ledger photocopies). Color: red. Hook: cold open mid-action.
Structure: detective — three suspects → the culprit → the fix.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp, lerp
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, note, stamp, follow_button,
                               phone, outline_text, word_pill, tear_calendar, suspect_card, red_string, cashier,
                               queue_dots, ledger, paper_sheet, cover, RED)
from engine.components.motion import bezier_point
from engine.components.infra import _draw_poly, _h

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · TERSANGKA", "01 · PELAKU", "02 · OBATNYA", "RECAP", "OUTRO"]
OK = C["ok"]
WHITE = (1, 1, 1, 1)


def build(project):
    T = project.timing
    v = Video(duration=T["L19"].end + TAIL, bpm=128, beat_offset=0.0, series="KASUS")
    v.cover_t = T.word("L12", "sama") + 0.8
    v.music = dict(key="E", mood="tense")             # generated score: detective tension
    v.cover = lambda c: cover(c, "Kenapa *down*\ntanggal 25?", kicker="APP BANK · TANGGAL GAJIAN", color=RED,
                              badge="KASUS", tags=["3 tersangka", "1 pelaku"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    intro(v, T, 0.0, b["00 · TERSANGKA"])
    board(v, T, T["L03"].start - 0.15, b["01 · PELAKU"])
    tersangka(v, T, b["00 · TERSANGKA"], b["01 · PELAKU"])
    pelaku(v, T, b["01 · PELAKU"], b["02 · OBATNYA"])
    obatnya(v, T, b["02 · OBATNYA"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


def _cover_hero(c, box):
    """Cover hero: the circled 25 next to the overheated ledger with the PELAKU stamp."""
    x, y, w, h = box
    cw = w * 0.4
    tear_calendar(c, x + 10, y + 40, cw, cw * 1.25, 0.0, 1.0, start=25, end=25, circle_p=1.0, sub="09.01", sub_p=1.0)
    lx, ly, ls = x + cw + (w - cw) / 2 + 10, y + h * 0.45, w - cw - 40
    ledger(c, lx, ly, ls, 0.0, filled=1.0, hot=1.0, title="database")
    stamp(c, lx, ly, "PELAKU", 1.0, color=RED, rot=-0.2, size=84)


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


def _ptag(c, t, t0, x, y, label, color=None, align="l", h=40):
    """Tag that pops in at t0; (x, y) = its left (or right) edge and top."""
    color = color or C["accent"]
    w = _tag_w(c, label)
    cx_ = x + w / 2 if align == "l" else x - w / 2
    _pop(c, t, t0, cx_, y + h / 2, lambda c: tag(c, x, y, label, color, align=align, h=h))


# ── INTRO: payday 09.01, the app spins → three suspects ────────────────
def _bank_screen(t, t_gaji, t_buka, t_muter):
    def screen(c, sx, sy, sw, sh):
        c.fill_rrect(sx, sy, sw, sh, 0, C["card"])
        ink2, muted, faint = C["ink2"], C["muted"], C["faint"]
        c.text(sx + 34, sy + 44, "09.01", F["mono_bold"], 19, C["ink"], 1, 0.04)
        c.fill_rrect(sx + 30, sy + 92, 44, 44, 12, ink2)
        c.text(sx + 88, sy + 123, "app bank", F["ui_semi"], 26, C["ink"], 1, -0.01)
        c.fill_rrect(sx + 30, sy + 170, sw - 60, 150, 20, C["bg"])
        c.text(sx + 54, sy + 214, "SALDO", F["mono_med"], 17, muted, 1, 0.14)
        c.text(sx + 54, sy + 284, "Rp ••••••", F["display"], 46, C["ink"], 1, -0.03)
        tw = (sw - 60 - 2 * 20) / 3
        for k in range(6):
            c.fill_rrect(sx + 30 + (k % 3) * (tw + 20), sy + 350 + (k // 3) * (tw + 20), tw, tw, 16, faint, 0.5)
        # loading: screen washes out, spinner keeps going (and grows on "muter")
        lp = out_expo(prog(t, t_buka, 0.5))
        if lp > 0:
            c.fill_rrect(sx, sy, sw, sh, 0, C["card"], 0.82 * lp)
            g = 1 + 0.35 * out_expo(prog(t, t_muter, 0.5))
            r = 40 * g
            mx, my = sx + sw / 2, sy + sh * 0.55
            a0 = t * 7.0
            sweep = 1.2 + 0.9 * math.sin(t * 2.3)
            c.ctx.new_path()
            c.ctx.arc(mx, my, r, 0, 2 * math.pi)
            c.src(C["faint"], lp)
            c.ctx.set_line_width(7 * g)
            c.ctx.stroke()
            c.ctx.new_path()
            c.ctx.arc(mx, my, r, a0, a0 + sweep)
            c.src(C["accent"], lp)
            c.ctx.set_line_width(7 * g)
            c.ctx.set_line_cap(1)
            c.ctx.stroke()
            c.text(mx, my + r + 54, "memuat…", F["ui"], 24, muted, lp, align="c")
        # notification drops in
        np_ = out_expo(prog(t, t_gaji, 0.6))
        if np_ > 0:
            ny = sy + 26 - 150 * (1 - np_)
            c.shadow(sx + 18, ny, sw - 36, 104, 22, 24, 8, 0.14 * np_)
            c.fill_rrect(sx + 18, ny, sw - 36, 104, 22, C["card"], np_)
            c.fill_rrect(sx + 36, ny + 30, 44, 44, 12, RED, np_)
            c.text(sx + 96, ny + 48, "Gaji masuk", F["ui_semi"], 26, C["ink"], np_, -0.01)
            c.text(sx + 96, ny + 80, "Rp ••••••• · baru saja", F["mono"], 17, muted, np_)
    return screen


def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    t_tear = T.word("L01", "dua")
    t_jam = T.word("L01", "sembilan")
    t_circle = T.word("L01", "satu")
    t_gaji = T.word("L02", "gaji")
    t_buka = T.word("L02", "buka")
    t_muter = T.word("L02", "muter")
    heads = [(Headline("Tanggal *25*, 09.01."), L1.start, L2.start - 0.15),
             (Headline("Gaji masuk. App *muter*."), L2.start, L3.start - 0.15)]
    cal = (X + 10, 650, 380, 480)
    ph = (X + 480, 590, 360, 720)
    step = 0.18

    cam = v.camera
    cam.key(0.0, zoom=1.06, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.focus(t_muter - 0.2, ph, zoom=1.08, dur=0.5)
    cam.reset(L3.start - 0.1, dur=0.4)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "KASUS · TANGGAL GAJIAN", RED)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        appear(c, t, L1.start - 0.1, L3.start - 0.15, cal,
               lambda c: tear_calendar(c, *cal, t, t_tear, step=step, circle_p=prog(t, t_circle, 0.7),
                                       sub="09.01", sub_p=prog(t, t_jam, 0.4)),
               enter="up", exit="left", rot=-0.035)
        appear(c, t, L1.start + 0.3, L3.start - 0.15, ph,
               lambda c: phone(c, *ph, draw_screen=_bank_screen(t, t_gaji, t_buka, t_muter)),
               enter="up", exit="left")
    v.add(s, e + 0.4, draw)
    for k in range(4):
        v.sfx("tick", t_tear + k * step, 0.5)
    v.sfx("pop", t_circle, 0.5)
    v.sfx("pop", t_gaji, 0.5)
    v.sfx("click", t_buka, 0.4)
    v.sfx("whoosh", t_muter - 0.2, 0.4)


# ── the suspect board (L03 → end of 00 · TERSANGKA) ────────────────────
BOARD = (X, 580, CW, 790)
CARD_W, CARD_H = 250, 380
CARDS = [(X + 8, 640, -0.04), (X + 299, 668, 0.025), (X + 590, 650, -0.02)]


def _icon_kasir(t):
    def icon(c, box):
        x, y, w, h = box
        for k in range(2):
            cashier(c, x + w / 2 + 6, y + h * (0.3 + 0.4 * k), w * 0.74, t, busy=1.0, seed=k + 1)
    return icon


def _icon_etalase(c, box):
    """Phone whose screen is a little shop: striped awning + product tiles."""
    x, y, w, h = box
    pw, ph_ = h * 0.5, h * 0.84
    px, py = x + w / 2 - pw / 2, y + h * 0.08
    c.stroke_rrect(px, py, pw, ph_, 14, C["ink2"], 4)
    n = 5
    sw = (pw - 16) / n
    for k in range(n):
        c.fill_rrect(px + 8 + k * sw, py + 22, sw, 26, 4, RED if k % 2 == 0 else C["card"])
    c.stroke_rrect(px + 8, py + 22, pw - 16, 26, 4, RED, 2)
    for k in range(4):
        c.fill_rrect(px + 16 + (k % 2) * (pw - 32) / 2, py + 64 + (k // 2) * 46, (pw - 40) / 2, 38, 6, C["faint"], 0.7)


def _traffic(c, x, y, w, h, p):
    """October traffic: flat days, a spike on the 1st and the 25th; dashed capacity line."""
    vals = []
    for d in range(1, 32):
        val = 0.22 + 0.08 * _h(d, 4)
        val += {1: 0.5, 2: 0.2, 25: 0.74, 26: 0.3}.get(d, 0.0)
        vals.append(val)
    pts = [(x + w * i / 30, y + h - h * vals[i]) for i in range(31)]
    c.text(x, y - 8, "TRAFFIC · OKTOBER", F["mono_bold"], 18, C["muted"], clamp(p * 3), 0.14)
    c.line(x, y + h, x + w, y + h, C["faint"], 2, clamp(p * 3))
    cap_y = y + h - h * 0.48
    c.ctx.set_dash([10, 8])
    c.line(x, cap_y, x + w, cap_y, C["ink2"], 2, 0.6 * clamp(p * 3))
    c.ctx.set_dash([])
    c.text(x + w, cap_y - 12, "kapasitas hari biasa", F["mono_med"], 17, C["ink2"], clamp(p * 3), 0.04, align="r")
    _draw_poly(c, pts, in_out_cubic(p), RED, 4)
    mp = clamp((p - 0.8) * 5)
    if mp > 0:
        px, py = pts[24]
        c.circle(px, py, 9, RED, mp)
        c.text(px, y + h + 30, "25", F["mono_bold"], 20, RED, mp, 0.04, align="c")


def board(v, T, s, e):
    L3, L4, L6 = T["L03"], T["L04"], T["L06"]
    t_tiga = T.word("L03", "tiga")
    t_satu = T.word("L03", "satu")
    t_r1 = T.word("L04", "pertama")
    t_half = T.word("L05", "setengah")
    t_r2 = T.word("L06", "kedua")
    t_bukan = T.word("L07", "bukan")
    t_traffic = T.word("L07", "traffic")
    head = Headline("Tiga tersangka. *Satu* pelaku.")
    pins = [(cx + CARD_W / 2, cy + 18) for cx, cy, _ in CARDS]

    def draw(c, t):
        head.draw(c, t, L3.start, L4.start - 0.15)

        def cork(c):
            c.card(*BOARD, r=26)
            bx, by, bw, bh = BOARD
            for i in range(1, 18):
                for j in range(1, 16):
                    c.circle(bx + i * bw / 18, by + j * bh / 16, 1.6, C["faint"], 0.6)
            red_string(c, pins, prog(t, t_tiga + 0.35, 0.8))
            specs = [
                dict(name="KASIR", label="server", icon=_icon_kasir(t), reveal=prog(t, t_r1, 0.6),
                     focus=out_expo(prog(t, t_r1, 0.4)) * (1 - prog(t, L6.start - 0.2, 0.3))),
                dict(name="ETALASE", label="app", icon=_icon_etalase, reveal=prog(t, t_r2, 0.6),
                     focus=out_expo(prog(t, t_r2, 0.4)), tear=prog(t, t_bukan, 0.9)),
                dict(name="???", label="?", icon=None, reveal=0.0,
                     focus=out_expo(prog(t, t_satu, 0.3)) * (1 - prog(t, L4.start - 0.3, 0.4))),
            ]
            for k, ((cx, cy, rot), sp) in enumerate(zip(CARDS, specs)):
                p_in = prog(t, t_tiga + k * 0.12, 0.45)
                if p_in <= 0:
                    continue
                sc = out_back(p_in, 1.7)
                with c.at(0, 0, max(0.01, sc), origin=(cx + CARD_W / 2, cy + CARD_H / 2)):
                    with c.group(clamp(p_in * 2)):
                        suspect_card(c, cx, cy, CARD_W, CARD_H, k + 1, sp["name"], sp["label"], sp["icon"],
                                     reveal=sp["reveal"], tear=sp.get("tear", 0.0), rot=rot, focus=sp["focus"])
            fade(c, t, t_half + 0.2, L6.start - 0.2,
                 lambda c: note(c, X + 300, 1120, "cukup buat hari biasa", prog(t, t_half + 0.2, 0.8),
                                arrow_to=(X + 150, 1050), size=36))
            if t >= t_traffic - 0.4:
                _traffic(c, X + 50, 1150, CW - 100, 170, prog(t, t_traffic - 0.4, 1.2))
        appear(c, t, s + 0.05, e - OUT, BOARD, cork, enter="right", blur=6)
    v.add(s, e, draw)
    v.sfx("whoosh", s + 0.05, 0.5)
    for k in range(3):
        v.sfx("pop", t_tiga + k * 0.12, 0.4)
    v.sfx("thud", t_satu, 0.5)
    v.sfx("pop", t_r1, 0.5)
    v.sfx("pop", t_r2, 0.5)
    v.sfx("whoosh", t_bukan, 0.6)
    v.sfx("tick", t_traffic + 0.4, 0.5)


# ── 00 · TERSANGKA: the board is the hero; this layer adds kicker, headlines, camera ──
def tersangka(v, T, s, e):
    ch = v.chapter(0, "TERSANGKA", s, e)
    L4, L5, L6, L7 = T["L04"], T["L05"], T["L06"], T["L07"]
    t_bukan = T.word("L07", "bukan")
    heads = [(Headline("Server *kurang*?"), L4.start, L5.start - 0.15),
             (Headline("Setengah *benar*."), L5.start, L6.start - 0.15),
             (Headline("App-nya *jelek*?"), L6.start, L7.start - 0.15),
             (Headline("Yang beda: *traffic*."), L7.start, e - OUT)]
    c1 = (CARDS[0][0], CARDS[0][1], CARD_W, CARD_H)
    c2 = (CARDS[1][0], CARDS[1][1], CARD_W, CARD_H)

    cam = v.camera
    cam.focus(L4.start - 0.2, c1, zoom=1.08, dur=0.6)
    cam.focus(L6.start - 0.2, c2, zoom=1.08, dur=0.6)
    cam.reset(t_bukan + 0.4, dur=0.7)

    def draw(c, t):
        kicker(c, t, L4.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
    v.add(s, e, draw)


# ── 01 · PELAKU: 2 cashiers → 20 → every lane ends at ONE ledger ───────
COLS, ROWS = 5, 4
CS = 128
LEDGER = (MID, 1300, 300)
FIRST = [(1, 1), (3, 1)]


def _counter_pos(i, j):
    cw = CW / COLS
    return X + cw * (i + 0.5), 660 + j * 118


def _envelope(c, x, y, a, rot=0.0):
    with c.at(0, 0, 1.0, origin=(x, y), rot=rot):
        c.fill_rrect(x - 24, y - 16, 48, 32, 4, C["card"], a)
        c.stroke_rrect(x - 24, y - 16, 48, 32, 4, RED, 2.5, a)
        c.ctx.new_path()
        c.ctx.move_to(x - 22, y - 14)
        c.ctx.line_to(x, y + 2)
        c.ctx.line_to(x + 22, y - 14)
        c.src(RED, a)
        c.ctx.set_line_width(2.5)
        c.ctx.stroke()


def pelaku(v, T, s, e):
    ch = v.chapter(1, "PELAKU", s, e)
    L8, L9, L10, L11, L12 = (T[k] for k in ("L08", "L09", "L10", "L11", "L12"))
    t_tambah = T.word("L09", "ditambah")
    t_auto = T.word("L09", "auto")
    t_satu = T.word("L10", "satu")
    t_db = T.word("L11", "database")
    t_antre = T.word("L11", "antre")
    t_gaji = T.word("L12", "gaji")
    t_sama = T.word("L12", "sama")
    heads = [(Headline("Kasir *tanggal muda*."), L8.start, L9.start - 0.15),
             (Headline("Tambah jadi *20*."), L9.start, L10.start - 0.15),
             (Headline("Buku kasnya *satu*."), L10.start, L11.start - 0.15),
             (Headline("Satu *pintu*."), L11.start, L12.start - 0.15),
             (Headline("Ini *pelakunya*."), L12.start, e - OUT)]
    lx, ly, ls = LEDGER
    cells = [(i, j) for j in range(ROWS) for i in range(COLS)]
    gx, gy = MID, _counter_pos(0, 1)[1] + 59

    def t_on(i, j):
        if (i, j) in FIRST:
            return L8.start - 0.1
        cx, cy = _counter_pos(i, j)
        return t_tambah + 0.04 * math.hypot(cx - gx, cy - gy) / 60

    cam = v.camera
    cam.key(s, zoom=1.25, x=gx, y=gy, dur=0.01)
    cam.key(t_tambah - 0.1, zoom=1.12, x=MID, y=850, dur=0.8)
    cam.key(t_satu - 0.1, zoom=1.0, dur=1.2, ease=out_cubic)
    cam.focus(t_db - 0.2, (lx - ls / 2, ly - 140, ls, 300), zoom=1.06, dur=0.6)
    cam.key(t_sama, zoom=0.97, dur=0.12)
    cam.key(t_sama + 0.12, zoom=1.0, dur=0.5)

    def draw(c, t):
        kicker(c, t, L8.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        jam = prog(t, t_antre, 1.2)
        hot = prog(t, t_gaji, 1.5)

        def floor(c):
            # lanes: every counter runs down to the one ledger (behind the counters)
            for k, (i, j) in enumerate(cells):
                cx, cy = _counter_pos(i, j)
                lane = [(cx, cy + 40), (lx + (cx - lx) * 0.12, ly - 115)]
                lp = prog(t, t_satu + 0.1 + k * 0.025, 0.6)
                if lp > 0:
                    c.ctx.set_dash([10, 8])
                    _draw_poly(c, lane, in_out_cubic(lp), RED, 2.5, 0.45)
                    c.ctx.set_dash([])
                    queue_dots(c, lane, t, n=2, speed=0.4, jam=jam, r=7, seed=k, color=RED, alpha=clamp(lp * 2 - 1))
            for k, (i, j) in enumerate(cells):
                ton = t_on(i, j)
                if t < ton:
                    continue
                cx, cy = _counter_pos(i, j)
                p = out_back(prog(t, ton, 0.4), 1.6)
                with c.at(0, 0, max(0.01, p), origin=(cx, cy)):
                    cashier(c, cx, cy, CS, t, busy=1.0, seed=k)
                    queue_dots(c, [(cx - CS * 0.36, cy - 64), (cx - CS * 0.36, cy - 34)], t, n=3, speed=0.3,
                               r=6, seed=k + 40, alpha=clamp(p))
            _ptag(c, t, t_auto, X + CW, 540, "auto-scaling", C["accent"], align="r")
            # the ledger
            if t >= t_satu - 0.1:
                lpop = out_back(prog(t, t_satu - 0.1, 0.5), 1.5)
                with c.at(0, 0, max(0.01, lpop), origin=(lx, ly)):
                    with c.group(clamp(lpop * 2)):
                        ledger(c, lx, ly, ls, t, filled=0.6 + 0.4 * hot, hot=hot, writing=1.0)
            _ptag(c, t, t_db, lx + ls / 2 + 30, ly - 20, "database", C["accent"])
            _ptag(c, t, t_gaji + 0.2, lx - ls / 2 - 30, ly - 20, "gaji ribuan kantor", RED, align="r")
            # payroll envelopes pour into the same ledger
            for k in range(14):
                t0 = t_gaji + k * 0.13
                p = prog(t, t0, 0.8)
                if 0 < p < 1:
                    src = (X + CW + 40 - 30 * (k % 3), 900 + 60 * (k % 4))
                    ex, ey = bezier_point(src, (X + CW - 40, 1200), (lx + 220, ly - 40), (lx + 40, ly), in_out_cubic(p))
                    _envelope(c, ex, ey, clamp(p * 5) * clamp((1 - p) * 5), rot=0.3 * (1 - p))
            stamp(c, lx, ly - 10, "PELAKU", prog(t, t_sama, 0.35), color=RED, rot=-0.2, size=92)
        appear(c, t, L8.start - 0.15, e - OUT, (X, 520, CW, 960), floor, blur=4, rise=12)
    v.add(s, e, draw)
    v.sfx("whoosh", L8.start - 0.15, 0.5)
    for k in range(6):
        v.sfx("pop", t_tambah + k * 0.1, 0.3)
    v.sfx("pop", t_auto, 0.5)
    v.sfx("whoosh", t_satu - 0.1, 0.6)
    v.sfx("pop", t_db, 0.5)
    for k in range(5):
        v.sfx("tick", t_gaji + k * 0.26, 0.35)
    v.sfx("thud", t_sama)


# ── 02 · OBATNYA: photocopies torn off the ledger serve the readers ────
def obatnya(v, T, s, e):
    ch = v.chapter(2, "OBATNYA", s, e)
    L13, L15 = T["L13"], T["L15"]
    t_baca = T.word("L13", "baca")
    t_read = T.word("L14", "read")
    t_rep = T.word("L14", "replica")
    t_w = [T.word("L15", "transfer"), T.word("L15", "bayar"), T.word("L15", "gaji")]
    head1 = Headline("Pisahin *baca* sama tulis.")
    head2 = Headline("Aslinya cuma buat *nulis*.")
    colw = (CW - 40) / 2
    lx, ly, ls = X + colw / 2, 820, 360
    rx = X + colw + 40
    sw, sh = 300, 150
    sx = rx + (colw - sw) / 2
    sy = [640, 815, 990]
    slot = (sx - 12, 626, sw + 24, 528)

    cam = v.camera
    cam.focus(t_read - 0.2, slot, zoom=1.05, dur=0.6)
    cam.focus(L15.start - 0.1, (X, 680, colw, 560), zoom=1.06, dur=0.6)
    cam.reset(e - 0.6, dur=0.5)

    def draw(c, t):
        kicker(c, t, L13.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L13.start, L15.start - 0.15)
        head2.draw(c, t, L15.start, e - OUT)
        cool = prog(t, L15.start, 1.2)
        moved = prog(t, t_read + 0.4, 0.8)

        def split(c):
            muted = C["muted"]
            c.text(X, 600, "TULIS", F["mono_bold"], 20, RED, 1, 0.18)
            c.text(rx, 600, "BACA", F["mono_bold"], 20, C["ink2"], out_expo(prog(t, t_baca, 0.4)), 0.18)
            sa = out_expo(prog(t, t_baca, 0.5)) * (1 - 0.7 * moved)
            c.stroke_rrect(*slot, 18, C["ink2"], 2.5, sa * 0.7, dash=[12, 10])
            # the jammed queue at the original: readers and writers mixed
            queue_dots(c, [(lx, 1330), (lx, 1010)], t, n=9, speed=0.25, jam=1.0 - moved, r=9, seed=3,
                       alpha=1 - moved)
            ledger(c, lx, ly, ls, t, filled=1.0, hot=1.0 - cool, writing=1.0)
            # three photocopies torn off the ledger fly to the read column (signature move)
            for k in range(3):
                t0 = t_read - 0.3 + k * 0.22
                p = prog(t, t0, 0.75)
                if p <= 0:
                    continue
                e_ = out_expo(p)
                x0, y0 = lx + ls * 0.05, ly - 110
                x1, y1 = sx, sy[k]
                fx = lerp(x0, x1, e_)
                fy = lerp(y0, y1, e_) - 120 * math.sin(math.pi * e_)
                with c.at(0, 0, 0.7 + 0.3 * e_, origin=(fx + sw / 2, fy + sh / 2), rot=0.35 * (1 - e_) * (1 if k % 2 else -1)):
                    paper_sheet(c, fx, fy, sw, sh, rows=4, filled=1.0)
            qa = prog(t, t_rep, 0.6)
            for k in range(3):
                queue_dots(c, [(sx + sw + 70, sy[k] + sh / 2 + 40), (sx + sw + 6, sy[k] + sh / 2)], t, n=3, speed=0.35,
                           r=8, seed=10 + k, alpha=qa)
            _ptag(c, t, t_rep, sx, 1180, "read replica", C["accent"])
            fade(c, t, t_rep + 0.3, e - OUT,
                 lambda c: c.text(sx + sw + 4, 1230, "cek saldo →", F["mono_med"], 18, muted, 1, 0.04, align="r"))
            for k, (lbl, tw_) in enumerate(zip(("transfer", "bayar", "gaji masuk"), t_w)):
                _ptag(c, t, tw_, X + 40, 1060 + k * 56, lbl, RED)

            def tick(c):
                mx, my = lx + ls / 2 - 6, ly - ls * 0.33 - 6
                c.circle(mx, my, 30, OK)
                icons.check(c, mx, my, 24, WHITE, 4)
            _pop(c, t, t_w[2] + 0.5, lx + ls / 2 - 6, ly - ls * 0.33 - 6, tick)
        appear(c, t, L13.start - 0.15, e - OUT, (X, 560, CW, 800), split, blur=4, rise=16)
    v.add(s, e, draw)
    v.sfx("whoosh", L13.start - 0.15, 0.5)
    for k in range(3):
        v.sfx("whoosh", t_read - 0.3 + k * 0.22, 0.35)
    v.sfx("pop", t_rep, 0.5)
    for tt in t_w:
        v.sfx("pop", tt, 0.45)
    v.sfx("chime", t_w[2] + 0.5)


# ── RECAP (dark): the 25th again + 10.000 → auto-scaling won't save one door ──
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L16, L17 = T["L16"], T["L17"]
    t_n = T.word("L16", "sepuluh")
    t_nggak = T.word("L17", "nggak")
    t_pintu = T.word("L17", "pintu")
    head1 = Headline("Bukan *teori*.", style="headline_dark")
    head2 = Headline("Masalahnya *satu pintu*.", style="headline_dark")
    cal = (X + 10, 640, 320, 400)
    nx = X + 380
    lx, ly, ls = MID, 1190, 260

    cam = v.camera
    cam.key(t_n + 0.6, zoom=0.97, dur=0.12)
    cam.key(t_n + 0.72, zoom=1.0, dur=0.5)
    cam.focus(t_pintu - 0.3, (lx - ls / 2, ly - 120, ls, 260), zoom=1.08, dur=0.5)
    cam.reset(e - 0.5, dur=0.4)

    def draw(c, t):
        head1.draw(c, t, L16.start, L17.start - 0.15)
        head2.draw(c, t, L17.start, e - OUT)
        appear(c, t, L16.start - 0.1, L17.start - 0.15, cal,
               lambda c: tear_calendar(c, *cal, t, 0.0, start=25, end=25, circle_p=1.0, sub="09.01", sub_p=1.0),
               enter="up", exit="left", rot=-0.04)

        def number(c):
            outline_text(c, nx, 880, "10.000", F["display"], 130, prog(t, t_n - 0.2, 0.7), prog(t, t_n + 0.5, 0.4),
                         color=RED)
            c.text(nx + 4, 940, "request barengan", F["ui_semi"], 32, C["d_ink"], out_expo(prog(t, t_n + 0.6, 0.4)), -0.01)
            c.text(nx + 4, 990, "BONGKAR ARSITEKTUR · EP01", F["mono_med"], 18, C["d_muted"],
                   out_expo(prog(t, t_n + 0.8, 0.4)), 0.12)
        appear(c, t, L16.start, L17.start - 0.15, (nx, 740, CW - 380, 280), number, enter="up", exit="left")

        def funnel(c):
            pw, _ = word_pill(c, X, 590, "auto-scaling", C["orange_pill"], size=56)
            sp = out_expo(prog(t, t_nggak, 0.5))
            if sp > 0:
                c.line(X - 10, 590 + 46, X - 10 + (pw + 20) * sp, 590 + 46, C["d_accent"], 7)
            cw = CW / COLS
            for k in range(10):
                i, j = k % COLS, k // COLS
                cx, cy = X + cw * (i + 0.5), 800 + j * 110
                lane = [(cx, cy + 34), (lx + (cx - lx) * 0.12, ly - 100)]
                c.ctx.set_dash([10, 8])
                _draw_poly(c, lane, 1.0, RED, 2.5, 0.5)
                c.ctx.set_dash([])
                queue_dots(c, lane, t, n=2, speed=0.4, jam=1.0, r=6, seed=k, color=RED)
                cashier(c, cx, cy, 104, t, busy=1.0, seed=k)
            ledger(c, lx, ly, ls, t, filled=1.0, hot=1.0, writing=1.0, title="database")
        appear(c, t, L17.start - 0.1, e - OUT, (X, 560, CW, 860), funnel, enter="right")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("thud", t_n + 0.5, 0.7)
    v.sfx("whoosh", L17.start - 0.1, 0.5)
    v.sfx("click", t_nggak, 0.7)
    v.sfx("thud", t_pintu)


# ── OUTRO: logo + next video (EP01) + follow ───────────────────────────
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
            c.fill_rrect(X, 830, 14, 220, 7, RED)
            c.text(X + 50, 892, "VIDEO BERIKUTNYA · BONGKAR EP01", F["mono_bold"], 20, RED, 1, 0.16)
            c.text(X + 50, 962, "10.000 request barengan", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "dan aplikasinya tetap jalan.", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L18.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L19.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "mumeyong.dev", F["mono_med"], 28,
                                                          C["d_muted"], 1, 0.06, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L19.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L18.start, 0.5)
    v.sfx("chime", t_click + 0.1)
