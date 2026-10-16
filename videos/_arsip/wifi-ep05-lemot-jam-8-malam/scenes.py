"""Bongkar WiFi Rumah EP 05 — Kenapa internet lemot tiap jam 8 malam? QUICK, classic + Apple craft, material flat (big hero).

Metaphor: one apartment block (rusun) on one water main. The riser pipe from the street = the ISP's shared bandwidth,
every tap = a home that is online. In the afternoon a few taps run hard (00); at 20.00 every window lights up, every
tap opens, and once more taps are open than the pipe was built for (oversubscription) the column thins toward the
top and your tap drips (01). Two tests and a log tell you whether it's the pipe or your WiFi (02). Recap closes the
series: five episodes as five chips next to the lit block (the 20.00 clock = bookend of the hook).
Craft: rack_cut (14.00 → 20.00) · draw_on (the shared route) · mark (circle on your dripping tap).
"""
from engine import Video, tokens as tk
from engine.ease import clamp, prog, lerp, curve
from engine.video import draw_background
from engine.components import (kicker, fade, pop_tag, check_badge, brand_intro, series_bumper, standard_outro, cover,
                               Rig, arrive, follow, rise, dolly, cut, push, ios_at, focus_pull, heads, draw_heads,
                               rack_cut, draw_on, mark, pts_bezier, rusun_air, rusun_geo, aliran, material as mat)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID, W = L["col_x"], L["col_w"], tk.W / 2, tk.W
PRE_ROLL = 2.05                     # long brand sting (version 2): the voice starts under its wipe
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · SATU PIPA", "01 · JAM RAME", "02 · YANG BISA KAMU LAKUIN", "RECAP", "OUTRO"]
LOOK = "flat"                       # EP 04 paper-big → flat-big
COL = tk.CHAPTER[4][0]              # teal: water, lit windows, the roof clock
SERIES = "BONGKAR WIFI RUMAH · EP 05"
RX, RY = MID, 1060                  # hero rest position (screen px)
HW, HH = 900, 1050                  # hero box, drawn around (0, 0)
G = rusun_geo(-HW / 2, -HH / 2, HW, HH)
YOU = len(G["units"]) - 1           # top floor, right
DAY = (2, 7)                        # taps already open in the afternoon
WAVE = (0, 1, 3, 4, 5, 6, 8)        # the rest open at 20.00
LIGHTS = (3, 0, 6, 9, 1, 4, 8, 2, 7, 5)
EPS = ("EP 01 · LAMPU LOS", "EP 02 · DARI ISP", "EP 03 · PAS HUJAN", "EP 04 · RESTART", "EP 05 · JAM 20.00")


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


def _open(t, t0, dur=0.4):
    return curve("apple_out")(prog(t, t0, dur))


class Cue:
    """Every time the hero reacts to, computed once from the voice — read this, not the draw code, to retime."""

    def __init__(self, T, b, bump1):
        self.b = b
        self.siang = T["L01"].start
        self.malam = _w(T, "L02", "malam", 0.3)                  # rack_cut 14.00 → 20.00
        self.dibagi = _w(T, "L03", "dibagi", 0.85)               # the band splits in ten
        self.t_in = max(arrive(_w(T, "L04", "rusun", 0.9), "hero"), bump1 - 0.25)
        self.keran = arrive(_w(T, "L05", "keran", 0.4))
        self.deres = arrive(_w(T, "L05", "deres", 0.9))
        self.isp = arrive(_w(T, "L06", "ISP", 0.45), "snappy")
        self.route = _w(T, "L06", "bareng", 0.7) - 0.3           # draw_on: street pipe → your tap
        self.lights = arrive(_w(T, "L07", "rumah", 0.9))         # signature: windows light up
        self.wave = arrive(_w(T, "L08", "barengan", 0.5))        # …and every tap opens
        self.cap = arrive(_w(T, "L09", "full", 0.75))            # the pipe was built for fewer: column thins
        self.over = arrive(_w(T, "L10", "oversubscription", 0.2), "snappy")
        self.netes = _w(T, "L11", "netes", 0.85)
        self.lan = arrive(_w(T, "L12", "LAN", 0.5))
        self.lemot = arrive(_w(T, "L13", "lemot", 0.3))
        self.wifi = _w(T, "L13", "WiFi", 0.85)
        self.ghz = arrive(_w(T, "L14", "GHz", 0.5))
        self.speed = arrive(_w(T, "L15", "speedtest", 0.5))
        self.komplain = _w(T, "L15", "komplain", 0.9)
        self.mana = arrive(_w(T, "L16", "mana", 0.9), "snappy")


def build(project):
    T = project.timing
    v = Video(duration=T["L20"].end + TAIL, bpm=88, beat_offset=0.0, series=SERIES)
    brand_intro(v, version=2)
    v.music = dict(style="lofi", key="A", mood="dreamy")      # EP 04 garage F warm, panggung marimba D bright
    v.sfx_kit = "glass"
    v.cover = lambda c: cover(c, "Lemot tiap\n*jam 8 malam*?", kicker=SERIES, color=COL, badge="EP 05",
                              tags=["peak hour", "bandwidth", "oversubscription"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    dib = _w(T, "L03", "dibagi", 0.85)
    bump0 = max(dib + 1.0, T["L03"].end + 0.1)
    bump1 = bump0 + 1.35
    b[1] = max(b[1], bump0 + 0.45)                           # chapter switch hidden under the bumper
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(3):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 5, "Lemot jam 8 malam", COL,
                                                   title=("BONGKAR", "WIFI RUMAH")), z=100)
    v.sfx("whoosh", bump0)
    v.stage = lambda c, t: (draw_background(c, v, t), mat.stage(c, LOOK, COL, 1 - v.dark_amount(t)))
    v.finish = lambda c, t: mat.finish(c, LOOK, 1 - v.dark_amount(t))
    Q = Cue(T, b, bump1)
    hero(v, T, Q)
    intro(v, T, Q, b[0], b[1])
    pipa(v, T, Q, b[1], b[2])
    rame(v, T, Q, b[2], b[3])
    lakuin(v, T, Q, b[3], b[4])
    recap(v, T, Q, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L20", COL,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="“Bongkar apa lagi?”",
                               sub="Seri berikutnya, kamu yang pilih."))
    v.cover_t = Q.netes + 1.0
    return v


# ── the rusun: one object from L04 to the recap ───────────────────────────────────────────────────────────────────
def state(t, Q):
    """rusun_air keyword values at t (taps, lights, night, clock, cap) — all from the Cue times."""
    taps = [0.0] * len(G["units"])
    for j, i in enumerate(DAY):
        taps[i] = _open(t, follow(Q.keran, j))
    taps[YOU] = _open(t, Q.deres)
    for j, i in enumerate(WAVE):
        taps[i] = _open(t, follow(Q.wave, j, 0.05))
    lights = [0.0] * len(G["units"])
    for j, i in enumerate(LIGHTS):
        lights[i] = _open(t, follow(Q.lights, j, 0.045))
    k = curve("apple_out")(prog(t, Q.lights - 0.3, 0.5))
    cap = lerp(10.0, 4.0, curve("apple_in_out")(prog(t, Q.cap, 0.9)))
    return dict(taps=taps, lights=lights, night=k, clock="14.00", clock_b="20.00", clock_p=k, cap=cap)


def _peak():
    return dict(taps=[1.0] * len(G["units"]), lights=[1.0] * len(G["units"]), night=1.0, clock="20.00", cap=4.0)


def _scr(rig, t, gx, gy):
    st = rig.state(t)
    return st["x"] + gx * st["s"], st["y"] + gy * st["s"]


def hero(v, T, Q):
    b = Q.b
    rig = Rig(x=RX, y=RY, s=2.4, a=0.0)
    rig.to(Q.t_in, preset="silk", s=1.0, a=1.0)              # full-bleed shrink → lands at rest on "rusun"
    rig.to(b[2] - 0.2, preset="silk", s=1.1, y=RY + 70)       # 01: closer, cropped at the street
    rig.to(b[4] + 0.1, preset="silk", s=0.5, x=730, y=1060)   # recap: small, right, windows still lit
    Q.rig = rig
    route = G["route"]

    def body(c, t):
        op = 1 - prog(t, b[5] - OUT, OUT)
        with c.group(op):
            with rig.place(c, t):
                rusun_air(c, -HW / 2, -HH / 2, HW, HH, t, look=LOOK, color=COL, **state(t, Q))
                draw_on(c, t, Q.route, route, C["accent"], width=8.0, dur=1.0, t_out=b[2] - OUT)

    def draw(c, t):
        focus_pull(c, t, b[3] + 0.1, b[4] - 0.3, (0, 380, W, 1540), lambda c: body(c, t))
    v.add(Q.t_in, b[5] + 0.05, draw, z=10, bleed=True)
    v.sfx("whoosh", Q.t_in, 0.5)
    for j in range(len(DAY)):
        v.sfx("pop", follow(Q.keran, j), 0.4)
    v.sfx("pop", Q.deres, 0.5)
    v.sfx("whoosh", Q.route, 0.3)
    for j in range(0, len(LIGHTS), 3):
        v.sfx("tick", follow(Q.lights, j, 0.045), 0.35)
    for j in range(0, len(WAVE), 2):
        v.sfx("pop", follow(Q.wave, j, 0.05), 0.35)
    v.sfx("thud", Q.cap + 0.3, 0.5)


def _cover_hero(c, box):
    x, y, w, h = box
    with c.at(x + w / 2, y + h / 2, min(w / HW, h / HH), origin=(0, 0)):
        rusun_air(c, -HW / 2, -HH / 2, HW, HH, 0.4, look=LOOK, color=COL, **_peak())


# ── INTRO: before/after on one clock; the water band stalls, then splits in ten ────────────────────────────────────
def intro(v, T, Q, s, e):
    hs = heads(T, [("Lancar\n*jaya*.", "L01"), ("Malamnya\n*nyangkut*.", "L02"), ("Satu pipa,\n*rame-rame*.", "L03")],
               e - OUT)
    t_out = e - OUT
    by = 1250

    def clock(text, sub):
        def d(c):
            c.text(X, 1020, text, F["display"], 280, C["ink"], ls=-0.05)
            c.text(X + 8, 1094, sub, F["mono_med"], 28, C["muted"], ls=0.2)
        return d

    def draw(c, t):
        kicker(c, t, T["L01"].start, t_out, SERIES, COL)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
        op = 1 - curve("apple_in")(prog(t, t_out, OUT))
        with c.group(op):
            rise(c, t, Q.siang, None, (X, 760, CW, 360),
                 lambda c: rack_cut(c, t, Q.malam, (X, 760, CW, 360), clock("14.00", "SIANG"), clock("20.00", "MALAM")))
            a = curve("apple_out")(prog(t, Q.siang + 0.3, 0.6))
            wd = lerp(56, 18, curve("apple_in_out")(prog(t, Q.malam, 0.8)))
            p = curve("apple_in_out")(prog(t, arrive(Q.dibagi), 0.9))
            if p <= 0:
                aliran(c, t, [(-60, by), (W + 60, by)], wd, COL, alpha=a)
            else:
                aliran(c, t, [(-60, by), (300, by)], wd, COL, alpha=a)
                for k in range(10):
                    ey = by + (k - 4.5) * 44 * p
                    aliran(c, t, pts_bezier((300, by), (520, by), (640, ey), (W + 60, ey), 32),
                           lerp(wd, 5, p), COL, alpha=a, speed=0.2 + 0.03 * k)
    v.add(s, e, draw, z=20, bleed=True)
    v.sfx("pop", Q.siang + 0.3, 0.4)
    v.sfx("thud", Q.malam, 0.6)
    v.sfx("pop", arrive(Q.dibagi) + 0.5, 0.5)


# ── 00: the block lands, three taps run hard, the shared route is traced ─────────────────────────────────────────
def pipa(v, T, Q, s, e):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("Rusun,\n*satu pipa*.", "L04"), ("Siang,\n*air deres*.", "L05"),
                   ("Bandwidth-nya\n*patungan*.", "L06")], e - OUT)
    ux, uy, uw, uh = G["units"][YOU]["box"]

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[1], col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
        fade(c, t, Q.deres, e - OUT, lambda c: pop_tag(c, t, Q.deres, X + CW - 30, RY + uy - 58, "KAMU", COL,
                                                         align="r"))
        fade(c, t, Q.isp, e - OUT, lambda c: pop_tag(c, t, Q.isp, X + 20, 1430, "bandwidth ISP", COL))
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", Q.isp, 0.4)
    dolly(v, Q.route + 1.0 + M["hold_min"], e - 0.2)


# ── 01: 20.00 — windows light, every tap opens, the column thins, your tap drips ─────────────────────────────────
def rame(v, T, Q, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("Jam 20.00,\n*semua pulang*.", "L07"), ("*Peak hour*.", "L08"),
                   ("Nggak buat\n*full barengan*.", "L09", "L10"), ("Sisanya\n*netes*.", "L11")], e - OUT)
    nx, ny = G["units"][YOU]["nozzle"]
    sx, sy = RX + nx * 1.1, RY + 70 + ny * 1.1
    t_push = arrive(Q.netes)
    t_mark = Q.netes + 0.35

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[2], col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
        fade(c, t, Q.over, e - OUT, lambda c: pop_tag(c, t, Q.over, X + 20, 1440, "oversubscription", COL))
        mark(c, t, t_mark, "circle", (sx - 62, sy - 34, 124, 112), C["accent"], width=5.0, t_out=e - OUT, seed=5)
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", Q.over, 0.4)
    push(v, t_push, (sx - 170, sy - 150, 340, 300), zoom=1.12)
    v.sfx("tick", Q.netes, 0.5)


# ── 02: three tests, one card per sentence; the block goes soft behind them (focus_pull) ─────────────────────────
def lakuin(v, T, Q, s, e):
    col = tk.CHAPTER[2][0]
    hs = heads(T, [("Colok\n*kabel* dulu.", "L12"), ("Kabel lemot?\nBukan *WiFi*.", "L13"),
                   ("Cari band\n*yang lega*.", "L14"), ("Catat. Bawa\n*bukti*.", "L15")], e - OUT)
    t_out = e - OUT
    ch, gap, y0 = 250, 30, 560
    boxes = [(X, y0 + i * (ch + gap), CW, ch) for i in range(3)]

    def bar(c, x, y, wmax, v_, color):
        c.fill_rrect(x, y, wmax, 28, 14, C["line"])
        if v_ > 0.005:
            c.fill_rrect(x, y, max(28, wmax * v_), 28, 14, color)

    def card_lan(c, t):
        x, y, w, h = boxes[0]
        c.card(x, y, w, h)
        c.text(x + 36, y + 58, "Tes kabel LAN", F["ui_semi"], 30, C["ink"])
        c.text(x + w - 36, y + 56, "SIANG · MALAM", F["mono_med"], 19, C["muted"], ls=0.14, align="r")
        siang = 0.9 * _open(t, follow(Q.lan, 1), 0.6)
        malam = 0.9 * _open(t, follow(Q.lan, 2), 0.6) - 0.62 * curve("apple_in_out")(prog(t, Q.lemot, 0.8))
        for k, (lab, val) in enumerate((("14.00", siang), ("20.00", malam))):
            yy = y + 112 + k * 70
            c.text(x + 36, yy + 22, lab, F["mono_med"], 22, C["ink2"])
            bar(c, x + 150, yy, w - 360, val, COL)
        fade(c, t, arrive(Q.wifi), None, lambda c: c.text(x + w - 36, y + 204, "jalurnya", F["serif"], 40,
                                                          C["accent"], align="r"))

    def card_ghz(c, t):
        x, y, w, h = boxes[1]
        c.card(x, y, w, h)
        c.text(x + 36, y + 58, "WiFi: pindah band", F["ui_semi"], 30, C["ink"])
        p = _open(t, follow(Q.ghz, 1), 0.6)
        c.text(x + 36, y + 134, "2,4 GHz", F["mono_med"], 22, C["ink2"])
        seg = (w - 360) / 9
        for k in range(9):
            c.fill_rrect(x + 190 + k * seg, y + 112, seg * 0.55 * p, 28, 8, C["faint"])
        c.text(x + 36, y + 204, "5 GHz", F["mono_med"], 22, C["ink2"])
        bar(c, x + 190, y + 182, w - 400, 0.9 * _open(t, follow(Q.ghz, 2), 0.6), COL)
        check_badge(c, x + w - 70, y + 196, 22, clamp(ios_at(t, follow(Q.ghz, 4), "snappy")))

    def card_log(c, t):
        x, y, w, h = boxes[2]
        c.card(x, y, w, h)
        c.text(x + 36, y + 58, "Catatan buat ISP", F["ui_semi"], 30, C["ink"])
        rows = ("20.00 — lemot, kabel juga", "20.30 — masih lemot", "14.00 — lancar")
        for k, r in enumerate(rows):
            a = _open(t, follow(Q.speed, k + 1), 0.45)
            c.text(x + 40, y + 120 + k * 46, r, F["serif"], 34, C["ink2"], alpha=a)
        check_badge(c, x + w - 70, y + 52, 24, clamp(ios_at(t, arrive(Q.komplain, "snappy"), "snappy")))

    def draw(c, t):
        kicker(c, t, s + 0.2, t_out, CH[3], col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
        for t0, box, fn in ((Q.lan, boxes[0], card_lan), (Q.ghz, boxes[1], card_ghz), (Q.speed, boxes[2], card_log)):
            rise(c, t, t0, t_out, box, lambda c, fn=fn: fn(c, t))
    v.add(s, e, draw, z=20)
    cut(v, s)
    for t0 in (Q.lan, Q.ghz, Q.speed):
        v.sfx("pop", t0, 0.5)
    v.sfx("whoosh", Q.lemot, 0.3)
    v.sfx("chime", follow(Q.ghz, 4), 0.4)
    v.sfx("chime", arrive(Q.komplain, "snappy"), 0.5)
    dolly(v, Q.komplain + 0.6, e - 0.2)


# ── RECAP (dark): the lit block shrinks right; five episodes as five chips; one opinion ───────────────────────────
def recap(v, T, Q, s, e):
    hs = heads(T, [("Cari dulu\n*di mana*.", "L16"), ("Jam rame,\n*server siap*.", "L17"),
                   ("Dibangun buat\n*rata-rata*.", "L18")], e - OUT, style="headline_dark")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP · SERI TAMAT", COL)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
        for i, lab in enumerate(EPS):
            t0 = follow(Q.mana, i, 0.1)
            fade(c, t, t0, e - OUT, lambda c, i=i, lab=lab, t0=t0: pop_tag(c, t, t0, X, 660 + i * 86, lab, COL))
    v.add(s, e, draw, z=20)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    for i in range(len(EPS)):
        v.sfx("pop", follow(Q.mana, i, 0.1), 0.35)
    dolly(v, T["L17"].start + 0.4, e - 0.2)
    cut(v, e)
