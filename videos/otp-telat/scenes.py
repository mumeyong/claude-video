"""Kenapa OTP suka telat datang? — the OTP code is a letter passing post offices (kantorpos.py).

Hero = the phone on the OTP screen, alive from the first line to the recap: its "Kirim ulang dalam 0:59" timer runs on
the voice clock (it hits 0:00 exactly when L12 says "kirim ulang"). Our letter (green stamp) is the second shared
element: queue in the intro → "surat" in 00 → stuck on the conveyor in 01 → back on the belt in the recap.
Signature: the letter stops in the queue while the timer on the phone keeps counting.
"""
from engine import Video, tokens as tk
from engine.ease import clamp, prog, track
from engine.video import draw_background
from engine.components import (kicker, fade, pop_tag, brand_intro, standard_outro, cover, arrive, follow, dolly, cut,
                               heads, draw_heads, sheet, mark, stamp, press, draw_on, ios_at, material as mat,
                               amplop, belt, loket, hp_otp, hp_box, log_card, notif, POS_GREEN)
from engine.components.kantorpos import PW, PH

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · JALANNYA", "01 · ANTREAN", "02 · KIRIM ULANG", "RECAP", "OUTRO"]
LOOK = "flat"
COL = POS_GREEN
CODES = ("482193", "773041", "190657")

# 00 — the route: four counters stacked on a vertical line, phone at the bottom right
RX = X + 60                                   # route line x
ST_X, ST_W, ST_H = X + 120, 470, 116
ST_Y = (580, 760, 940, 1120)
STATIONS = (("server app", "yang bikin kode"), ("SMS gateway", "nerusin ke operator"),
            ("operator", "SMSC · pusat SMS"), ("BTS", "menara dekat rumahmu"))
# 01 — one office: the conveyor and the queue
BY, BH = 980, 44                              # belt top / height
EW = 124                                      # envelope width on the belt
EH = EW * 0.62
TRAY = (640, 536, 289, 176)                   # "disimpan" tray (store-and-forward), above the piled rows


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


class Cue:
    """Every time the video reacts to, computed once from the voice — read this, not the draw code, to retime."""

    def __init__(self, T, b):
        self.b = b
        self.t_in = T["L01"].start - 0.1
        self.tim = _w(T, "L01", "timernya", 0.25)           # timer starts
        self.sepi = _w(T, "L01", "sepi", 0.95)
        self.antre = _w(T, "L02", "antre", 0.85)            # intro queue slides in
        self.surat = _w(T, "L03", "surat", 0.35)            # our letter becomes the hero
        self.st = [_w(T, "L04", w, f) for w, f in (("server", 0.1), ("gateway", 0.35),
                                                    ("operator", 0.6), ("BTS", 0.85))]
        self.verbs = [_w(T, "L05", w, f) for w, f in (("nerima", 0.2), ("nyortir", 0.5), ("nerusin", 0.85))]
        self.antrean = _w(T, "L06", "antrean", 0.8)
        self.rame = [_w(T, "L07", w, f) for w, f in (("rame", 0.15), ("gajian", 0.35), ("promo", 0.55))]
        self.sama = _w(T, "L07", "sama", 0.95)
        self.nosig = _w(T, "L08", "sinyal", 0.3)            # bars drop, letter goes to the tray
        self.back = _w(T, "L08", "nongol", 0.85)            # bars back, letter back on the belt
        self.hops = [self.antrean + 1.6, self.sama + 0.5, self.back + 1.2]   # the queue steps forward
        self.log = T["L09"].start
        self.sent = _w(T, "L09", "sent", 0.75)
        self.bukan = _w(T, "L10", "bukan", 0.7)
        self.wa = _w(T, "L11", "WhatsApp", 0.3)
        self.inet = _w(T, "L11", "internet", 0.75)
        self.resend = _w(T, "L12", "kirim", 0.6)            # the timer reaches 0:00 here → press
        self.again = _w(T, "L12", "berkali", 0.85)
        self.hangus = _w(T, "L13", "hangus", 0.4)
        self.nyampe = _w(T, "L13", "nyampe", 0.65)
        self.berlaku = _w(T, "L13", "berlaku", 0.95)
        self.antre2 = _w(T, "L14", "antre", 0.8)


def timer_left(t, Q):
    """Seconds on the resend timer: 59 → 0 on the voice clock (lands on L12 'kirim'), then a fresh 59 after the press."""
    if t < Q.resend + 0.2:                    # reaches 0:00 1,2 s early so the blue link is seen before the press
        return 59.0 * (1 - clamp((t - Q.tim) / (Q.resend - 1.2 - Q.tim)))
    return max(0.0, 59.0 - (t - Q.resend - 0.2))


def build(project):
    T = project.timing
    v = Video(duration=T["L16"].end + TAIL, bpm=80, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="ambient", key="F", mood="warm")
    v.sfx_kit = "mech"
    v.cover = lambda c: cover(c, "Kenapa OTP\nsuka *telat*?", kicker="BONGKAR SEHARI-HARI", color=COL,
                              badge="SMS", tags=["SMS gateway", "antrean"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(3):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    v.stage = lambda c, t: (draw_background(c, v, t), mat.stage(c, LOOK, COL, 1 - v.dark_amount(t)))
    v.finish = lambda c, t: mat.finish(c, LOOK, 1 - v.dark_amount(t))
    Q = Cue(T, b)
    phone(v, T, Q)
    intro(v, T, Q, b[0], b[1])
    bab0(v, T, Q, b[1], b[2])
    bab1(v, T, Q, b[2], b[3])
    bab2(v, T, Q, b[3], b[4])
    recap(v, T, Q, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L16", COL,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="“Paling lama berapa menit?”",
                               sub="nunggu OTP yang nggak dateng-dateng"))
    v.cover_t = Q.sepi + 0.8
    return v


# ── the hero: the phone on the OTP screen, from L01 to the end of the recap ─────────────────────────────────────────
def phone_state(t, Q):
    """(cx, cy, s) of the phone — one track per axis so every move bends, never stop-and-go."""
    b = Q.b
    big = Q.resend - 2.2                      # 02: grows back to centre just before the timer runs out
    cx = track(t, [(0, MID), (b[1], 800), (big, MID)], "hero")
    cy = track(t, [(0, 1100), (b[1], 1310), (big, 1130), (b[4], 1190)], "hero")
    s = track(t, [(0, 0.76), (Q.t_in, 0.72), (b[1], 0.40), (big, 0.62), (b[4], 0.5)], "hero")
    return cx, cy, s


def phone(v, T, Q):
    b = Q.b

    def draw(c, t):
        cx, cy, s = phone_state(t, Q)
        a = clamp(prog(t, Q.t_in, 0.45)) * (1 - prog(t, b[5] - OUT, OUT))
        bars = 0 if Q.nosig + 0.2 <= t < Q.back else 4
        recap = t >= b[4]
        filled = 0 if recap else 6 * clamp(prog(t, Q.nyampe + 0.35, 0.7))
        wrong = 0 if recap else clamp(prog(t, arrive(Q.berlaku, "snappy"), 0.3))
        hp_otp(c, t, cx - PW * s / 2, cy - PH * s / 2, s, left=timer_left(t, Q), code=CODES[0], filled=filled,
               bars=bars, detail=clamp((s - 0.45) / 0.15), press=press(t, Q.resend), wrong=wrong, alpha=a)
    v.add(Q.t_in, b[5] + 0.05, draw, z=12, bleed=True)
    v.sfx("whoosh", Q.t_in, 0.4)
    for k in range(3):
        v.sfx("tick", Q.tim + k, 0.35)
    v.sfx("thud", Q.nosig + 0.2, 0.4)
    v.sfx("click", Q.resend, 0.6)
    v.sfx("rec", arrive(Q.berlaku, "snappy"), 0.5)


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w / (PW + 260), h / (PH + 40))
    ox = x + (w - (PW + 260) * s) / 2
    hp_otp(c, 0.3, ox, y + (h - PH * s) / 2, s, left=42, bars=4)
    amplop(c, ox + (PW + 120) * s, y + h * 0.42, 300 * s, COL, code=CODES[0], caps=2, mine=True)


# ── INTRO: the screen everyone knows; on "antre" the queue slides in above it ───────────────────────────────────────
def intro(v, T, Q, s, e):
    hs = heads(T, [("HP-mu masih\n*sepi*.", "L01"), ("Kodenya udah dikirim.\nLagi *antre*.", "L02")], e - OUT)
    xs = [820, 670, 520, 370]
    t0 = arrive(Q.antre, "snappy")

    def draw(c, t):
        kicker(c, t, T["L01"].start, e - OUT, "OTP · KIRIM ULANG", COL)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        for i, x in enumerate(xs):                           # other people's letters, ahead of ours
            ti = follow(t0, i)
            p = clamp(track(t, [(0, 0.0), (ti, 1.0)], "snappy"))
            a = clamp(prog(t, ti, 0.25)) * (1 - prog(t, Q.surat - 0.3, 0.3))
            amplop(c, x - 120 * (1 - p), 600, 130, code="", alpha=a)
    v.add(s, Q.surat + 0.1, draw, z=20)
    for i in range(len(xs)):
        v.sfx("pop", follow(t0, i), 0.35)
    dolly(v, Q.sepi + 0.4, Q.antre - 0.3)


# ── our letter: intro queue → "surat" punch → station by station → the belt → the tray → recap ────────────────────
def belt_off(t, Q):
    """The 01 queue doesn't crawl — it steps one slot forward a few times (a letter leaves), then holds."""
    return sum((EW + 18) * ios_at(t, th, "smooth") for th in Q.hops)


def slot_x(i, t, Q):
    """x of queue slot i on the 01 belt (0 = front, near the exit on the right)."""
    return 860 - i * (EW + 18) + belt_off(t, Q)


def edge_alpha(x, w):
    """Letters fade at the ends of the belt so no ink leaves the safe column."""
    return clamp((x - w / 2 - X) / 50) * clamp((X + CW - x - w / 2) / 40)


def letter(v, T, Q):
    b = Q.b
    t_belt = b[2] + 0.2
    cy_belt = BY - EH / 2 - 2
    tray = (TRAY[0] + TRAY[2] / 2, TRAY[1] + 94)
    # intro + 00: fixed targets (queue → "surat" punch → each counter on the route)
    xs = [(0, 220), (Q.surat - 0.25, MID), (arrive(Q.st[0], "snappy"), RX)]
    ys = [(0, 600), (Q.surat - 0.25, 860)] + [(arrive(t0, "snappy"), y + ST_H / 2) for t0, y in zip(Q.st, ST_Y)]
    ws = [(0, 130), (Q.surat - 0.25, 540), (arrive(Q.st[0], "snappy"), 100)]

    def draw(c, t):
        x, y, w = track(t, xs, "smooth"), track(t, ys, "smooth"), track(t, ws, "smooth")
        # 01: onto the belt (keeps its slot as the belt crawls) ↔ the "disimpan" tray while there's no signal
        k_tray = clamp(track(t, [(0, 0.0), (Q.nosig, 1.0), (Q.back, 0.0)], "smooth"))
        bx = slot_x(4, t, Q) + (tray[0] - slot_x(4, t, Q)) * k_tray
        by = cy_belt + (tray[1] - cy_belt) * k_tray
        k1 = clamp(track(t, [(0, 0.0), (t_belt, 1.0)], "smooth"))
        x, y, w = x + (bx - x) * k1, y + (by - y) * k1, w + (EW - w) * k1
        # recap: back in a queue on the dark belt, slot 3, crawling with it
        k4 = clamp(track(t, [(0, 0.0), (b[4] + 0.2, 1.0)], "smooth"))
        rx, ry = 840 - 3 * 160, 760 - 150 * 0.31 - 2
        x, y, w = x + (rx - x) * k4, y + (ry - y) * k4, w + (150 - w) * k4
        caps = sum(clamp(prog(t, arrive(t0, "snappy"), 0.35)) for t0 in Q.st)
        a = clamp(prog(t, arrive(Q.antre, "snappy") - 0.2, 0.3))
        a *= 1 - prog(t, b[3] - OUT, OUT) + prog(t, b[4], 0.4)
        a *= 1 - prog(t, b[5] - OUT, OUT)
        amplop(c, x, y, w, COL, code=CODES[0], caps=caps, mine=True, alpha=clamp(a))
    v.add(Q.antre - 0.5, b[5] + 0.05, draw, z=16, bleed=True)
    v.sfx("whoosh", Q.surat - 0.25, 0.4)
    for t0 in Q.st:
        v.sfx("pop", arrive(t0, "snappy"), 0.5)


# ── 00: four counters drawn on one route; the letter collects a postmark at each ─────────────────────────────────────
def bab0(v, T, Q, s, e):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("Kode OTP itu\n*surat*.", "L03"), ("Lewat beberapa\n*kantor pos*.", "L04", "L05")], e - OUT)
    route = [(RX, ST_Y[0] + ST_H / 2), (RX, 1400), (670, 1400)]
    tags = ["nerima", "nyortir", "nerusin"]
    letter(v, T, Q)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[1], col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        out = 1 - prog(t, e - OUT, OUT)
        with c.group(out):
            draw_on(c, t, arrive(Q.st[0], "smooth") - 0.3, route, C["faint"], width=6, dur=1.6)
            for k, (y, (lab, sub)) in enumerate(zip(ST_Y, STATIONS)):
                tk_ = arrive(Q.st[k], "snappy") - 0.15
                p = clamp(track(t, [(0, 0.0), (tk_, 1.0)], "snappy"))
                lit = clamp(prog(t, tk_ + 0.2, 0.4))
                with c.at(0, 24 * (1 - p)):
                    loket(c, ST_X, y, ST_W, ST_H, lab, sub, COL, alpha=clamp(prog(t, tk_, 0.25)), lit=lit)
                c.circle(RX, y + ST_H / 2, 12, COL, clamp(prog(t, tk_, 0.25)))
            for i, lab in enumerate(tags):
                ti = arrive(Q.verbs[i], "snappy")
                fade(c, t, ti, e - OUT, lambda c, i=i, lab=lab, ti=ti:
                     pop_tag(c, t, ti, ST_X + 110 + i * 175, ST_Y[3] + ST_H + 64, lab, COL))
    v.add(s, e, draw, z=14)
    cut(v, s)
    for t0 in Q.verbs:
        v.sfx("tick", arrive(t0, "snappy"), 0.4)
    dolly(v, arrive(Q.verbs[2], "snappy") + 0.9, e - 0.2, base=1.0)


# ── 01: one office up close — the conveyor, the queue, the tray, the server log ─────────────────────────────────────
def bab1(v, T, Q, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("Tiap kantor punya\n*antrean*.", "L06"), ("Semua lewat jalur\nyang *sama*.", "L07"),
                   ("Nggak ada sinyal?\nSuratnya *ditahan*.", "L08"), ("Log bilang\n*sent*.", "L09"),
                   ("Sent ≠\n*sampai*.", "L10")], e - OUT)
    t_q = arrive(Q.antrean, "snappy")
    layers = [arrive(t0, "snappy") for t0 in Q.rame]         # each busy moment adds a row on top
    rows = [("12.04.01", "otp.send → gateway", None), ("status", "sent ✓", C["ok"]),
            ("delivered", "— belum ada", C["d_muted"])]
    box = (X, 1050, CW, 70 + 64 * len(rows))

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[2], col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        out = 1 - prog(t, e - OUT, OUT)
        p_in = clamp(track(t, [(0, 0.0), (s + 0.1, 1.0)], "hero"))
        with c.group(out * clamp(prog(t, s, 0.4))):
            with c.at(0, 60 * (1 - p_in)):
                belt(c, X, BY, CW, belt_off(t, Q), h=BH, legs=56)
            loket(c, X, 590, 520, 116, "operator", "SMSC · antrean SMS", COL)
            ta = arrive(Q.nosig, "smooth") - 0.3
            tray_a = clamp(prog(t, ta, 0.35)) * (1 - prog(t, Q.back + 0.8, OUT))
            if tray_a > 0:
                tx, ty, tw, th = TRAY
                c.fill_rrect(tx, ty, tw, th, L["radius_card"], C["card"], tray_a)
                c.stroke_rrect(tx, ty, tw, th, L["radius_card"], COL, 2.5, alpha=tray_a, dash=[10, 8])
                c.text(tx + 22, ty + 36, "DISIMPAN", F["mono_bold"], 22, COL, alpha=tray_a)
                c.text(tx + 22, ty + th - 14, "nunggu HP online", F["ui_reg"], 22, C["muted"], alpha=tray_a)
            for i in range(12):                              # bottom row; slot 4 is ours (drawn by letter())
                if i == 4:
                    continue
                x = slot_x(i, t, Q)
                ti = follow(t_q, min(i, 6))
                a = clamp(prog(t, ti, 0.25)) * edge_alpha(x, EW)
                dy = 40 * (1 - clamp(track(t, [(0, 0.0), (ti, 1.0)], "snappy")))
                amplop(c, x, BY - EH / 2 - 2 - dy, EW, alpha=a)
            for r, tl in enumerate(layers):                  # rows piling up on top
                for i in range(9):
                    x = slot_x(i, t, Q) - (r % 2) * (EW + 18) / 2 - 10
                    ti = follow(tl, i % 5)
                    a = clamp(prog(t, ti, 0.25)) * edge_alpha(x, EW)
                    lift = (r + 1) * (EH * 0.55)
                    dy = 50 * (1 - clamp(track(t, [(0, 0.0), (ti, 1.0)], "snappy")))
                    if r == 2 and i % 2:
                        continue
                    amplop(c, x, BY - EH / 2 - 2 - lift - dy, EW, alpha=a)
        sheet(c, t, Q.log - 0.1, e - OUT, box, lambda c, *bx: _log(c, t, Q, bx, rows))
    v.add(s, e, draw, z=14)
    cut(v, s)
    v.sfx("whoosh", s + 0.1, 0.4)
    for i in range(6):
        v.sfx("pop", follow(t_q, i), 0.3)
    for tl in layers:
        v.sfx("pop", tl, 0.45)
    v.sfx("send", arrive(Q.nosig, "smooth"), 0.4)
    v.sfx("send", Q.back, 0.4)
    v.sfx("whoosh", Q.log - 0.1, 0.4)
    v.sfx("click", arrive(Q.sent, "snappy"), 0.5)
    v.sfx("click", arrive(Q.bukan, "snappy"), 0.5)


def _log(c, t, Q, box, rows):
    x, y, w, h = box
    ys = log_card(c, x, y, w, rows)
    rx = x + 34 + w * 0.36
    mark(c, t, arrive(Q.sent, "snappy"), "underline", (rx, ys[1] - 26, 140, 36), C["ok"], width=5)
    mark(c, t, arrive(Q.bukan, "snappy"), "circle", (rx - 16, ys[2] - 40, 270, 60), C["d_accent"], width=5)


# ── 02: two lanes (SMS queue vs internet), then the resend trap ──────────────────────────────────────────────────────
def bab2(v, T, Q, s, e):
    col = tk.CHAPTER[2][0]
    hs = heads(T, [("Lewat *internet*,\nbukan antrean.", "L11"), ("Jangan spam\n*kirim ulang*.", "L12"),
                   ("Kode lama\n*hangus*.", "L13")], e - OUT)
    lanes_out = Q.resend - 2.4
    t_wa = arrive(Q.wa, "smooth")
    t_n = arrive(Q.inet, "smooth")
    presses = [Q.resend - 2.0, arrive(Q.resend, "snappy"), arrive(Q.again, "snappy")]
    ex = [760, 560, 360]
    by2, ew2 = 650, 150
    eh2 = ew2 * 0.62
    t_h = arrive(Q.hangus, "snappy")
    t_ny = arrive(Q.nyampe, "smooth")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[3], col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        out = 1 - prog(t, e - OUT, OUT)
        la = clamp(prog(t, s, 0.4)) * (1 - prog(t, lanes_out, OUT))
        if la > 0:
            with c.group(la):
                pop_tag(c, t, s + 0.2, X, 600, "SMS · antre di tiap kantor", COL, h=52)
                belt(c, X, 800, CW, 12 * (t - s), h=40, legs=50)
                for i in range(7):
                    x = 830 - i * 160 + 12 * (t - s)
                    amplop(c, x, 800 - 45, 140, alpha=edge_alpha(x, 140))
                fade(c, t, t_wa - 0.2, lanes_out, lambda c: pop_tag(c, t, t_wa - 0.2, X, 910,
                                                                    "WhatsApp / notifikasi · internet", C["wa"], h=52))
                p = clamp(track(t, [(0, 0.0), (t_n - 0.4, 1.0)], "snappy"))
                notif(c, X + 20 - 120 * (1 - p), 990, 560, "WhatsApp", "Kode verifikasi kamu: 190657",
                      alpha=clamp(prog(t, t_n - 0.4, 0.2)))
        ea = clamp(prog(t, lanes_out + 0.2, 0.4)) * out
        if ea > 0:
            with c.group(ea):
                belt(c, X, by2, CW, 0.0, h=36, legs=0)
                for i, (x0, code) in enumerate(zip(ex, CODES)):
                    ti = presses[i]
                    a = clamp(prog(t, ti, 0.25))
                    dy = 50 * (1 - clamp(track(t, [(0, 0.0), (ti, 1.0)], "snappy")))
                    x, y, w = x0, by2 - eh2 / 2 - 2 - dy, ew2
                    if i == 0:                               # the oldest one is the one that arrives
                        cx, cy, sp = phone_state(t, Q)
                        bx, by_, bw, bh = hp_box(cx - PW * sp / 2, cy - PH * sp / 2, sp)["boxes"]
                        k = clamp(track(t, [(0, 0.0), (t_ny, 1.0)], "smooth"))
                        x, y, w = x + (bx + bw / 2 - x) * k, y + (by_ + bh / 2 - y) * k, w * (1 - 0.5 * k)
                        a *= 1 - prog(t, t_ny + 0.5, 0.3)
                    amplop(c, x, y, w, C["muted"], code=code, alpha=a)
                    if i < 2:
                        stamp(c, x, y, "HANGUS", clamp(prog(t, follow(t_h, i), 0.35)), color=C["rec"], size=34)
                lx, ly = hp_box(*_phone_tl(t, Q))["link"]
                ta = presses[2]
                fade(c, t, ta, e - OUT, lambda c: pop_tag(c, t, ta, lx + 150, ly - 60, "×3", C["rec"]))
    v.add(s, e, draw, z=14)
    cut(v, s)
    v.sfx("chime", t_n, 0.5)
    for ti in presses:
        v.sfx("pop", ti, 0.4)
    for i in range(2):
        v.sfx("thud", follow(t_h, i), 0.5)
    v.sfx("send", t_ny, 0.4)


def _phone_tl(t, Q):
    cx, cy, s = phone_state(t, Q)
    return cx - PW * s / 2, cy - PH * s / 2, s


# ── RECAP (dark): the letter is back on the belt, the timer runs again — one line only Mumeyong says ────────────────
def recap(v, T, Q, s, e):
    hs = heads(T, [("Bukan HP-mu yang rusak.\nSuratnya lagi *antre*.", "L14")], e - OUT, style="headline_dark")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", COL)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        a = clamp(prog(t, s + 0.2, 0.5)) * (1 - prog(t, e - OUT, OUT))
        with c.group(a):
            belt(c, X, 760, CW, 0.0, h=36, legs=0, color=C["d_muted"])
            for i in range(5):                               # slot 3 = our letter (letter())
                if i != 3:
                    amplop(c, 840 - i * 160, 760 - 150 * 0.31 - 2, 150, alpha=0.85)
    v.add(s, e, draw, z=14)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    dolly(v, T["L14"].start + 0.8, e - 0.2)
    cut(v, e)
