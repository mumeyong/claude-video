"""Kenapa war tiket konser selalu crash? — idea #07, pillar B, QUICK. See IDENTITY.md / TREATMENT.md.

Metaphor: the post-office queue-number machine (server = loket). Signature move: a paper slip feeds out of a slot
(ERROR 503, the queue ticket) + the big clock's seconds jump. Color: green. Hook: number first.
Structure: timeline per second — 10:00:00 → 10:00:01 → 10:00:10 → the queue.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp, lerp
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, note, follow_button, phone, fmt_id,
                               queue_dots, big_clock, print_slip, dispenser, loket, refresh_icon, refresh_storm, cover,
                               GREEN)
from engine.components.infra import _draw_poly, _h

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · 10:00:00", "01 · 10:00:01", "02 · 10:00:10", "03 · ANTREAN", "RECAP", "OUTRO"]
RED = C["rec"]
OK = C["ok"]
WHITE = (1, 1, 1, 1)


def build(project):
    T = project.timing
    v = Video(duration=T["L18"].end + TAIL, bpm=128, beat_offset=0.0, series="DETIK PER DETIK")
    v.cover_t = T.word("L14", "cepet") + 0.9
    v.music = dict(key="Bb", mood="warm")             # generated score: warm, after E tense (#06)
    v.cover = lambda c: cover(c, "Kenapa *crash*\njam 10.00?", kicker="WAR TIKET KONSER", color=GREEN,
                              badge="DETIK PER DETIK", tags=["retry storm", "waiting room"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    intro(v, T, 0.0, b["00 · 10:00:00"])
    detik00(v, T, b["00 · 10:00:00"], b["01 · 10:00:01"])
    detik01(v, T, b["01 · 10:00:01"], b["02 · 10:00:10"])
    detik10(v, T, b["02 · 10:00:10"], b["03 · ANTREAN"])
    antrean(v, T, b["03 · ANTREAN"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


def _cover_hero(c, box):
    """Cover hero: a full loket feeding out a 503 slip, next to the queue machine feeding out 29.481."""
    x, y, w, h = box
    lh = h * 0.6
    lw = lh / 1.3
    slot = loket(c, x + 20, y + 10, lw, lh, 0.0, full=1.0, label="server")
    print_slip(c, *slot, h * 0.36, 1.0, [("ERROR", "mono_bold", 20, None), ("503", "display", 56, RED)], color=RED,
               rot=-0.05)
    ds = h * 0.66 / 1.45
    slot = dispenser(c, x + w - ds / 2 - 20, y, ds, 0.0, serving="29.481", called=1.0)
    print_slip(c, *slot, h * 0.3, 1.0, [("NOMOR", "mono_bold", 17, None), ("29.481", "display", 40, GREEN)], rot=0.05)


def _pop(c, t, t0, cx, cy, draw, d=0.4):
    if t < t0:
        return
    p = out_back(prog(t, t0, d), 1.7)
    with c.at(0, 0, max(0.01, p), origin=(cx, cy)):
        with c.group(clamp(p * 2)):
            draw(c)


def _ptag(c, t, t0, x, y, label, color=None, align="l", h=40):
    color = color or C["accent"]
    w = c.measure(label, F["ui"], tk.T["tag"][0], tk.T["tag"][1])[0] + 30
    cx_ = x + w / 2 if align == "l" else x - w / 2
    _pop(c, t, t0, cx_, y + h / 2, lambda c: tag(c, x, y, label, color, align=align, h=h))


def _ripples(c, t, t0, x, y, w, h, n, seed=0, color=None):
    """Taps: rings expanding at hash-seeded spots, each repeating every ~0.9 s after t0."""
    color = color or C["accent"]
    if t < t0:
        return
    for i in range(n):
        ph = (t - t0) / 0.9 + _h(i, seed)
        if (t - t0) < _h(i, seed) * 0.9:
            continue
        f = ph % 1.0
        px, py = x + w * _h(i, seed + 1), y + h * _h(i, seed + 2)
        c.ctx.new_path()
        c.ctx.arc(px, py, 6 + 28 * out_expo(f), 0, 2 * math.pi)
        c.src(color, 0.6 * (1 - f))
        c.ctx.set_line_width(3)
        c.ctx.stroke()
        c.circle(px, py, 5, color, 0.8 * (1 - f))


# ── INTRO: thousands of seats, hundreds of thousands of fingers, one second ──
def _ticket_screen(t, t_tap, t_err):
    def screen(c, sx, sy, sw, sh):
        err = prog(t, t_err, 0.15)
        c.fill_rrect(sx, sy, sw, sh, 0, C["card"])
        if err < 1:
            with c.group(1 - err):
                c.text(sx + 34, sy + 50, "09:59:59", F["mono_bold"], 19, C["ink"], 1, 0.04)
                c.text(sx + 34, sy + 120, "TIKET KONSER", F["mono_bold"], 18, C["muted"], 1, 0.16)
                c.text(sx + 34, sy + 170, "Kategori", F["display_semi"], 40, C["ink"], 1, -0.03)
                for k, lbl in enumerate(("FESTIVAL", "TRIBUN A", "TRIBUN B")):
                    ry = sy + 210 + k * 96
                    c.fill_rrect(sx + 30, ry, sw - 60, 80, 16, C["bg"])
                    c.text(sx + 54, ry + 50, lbl, F["mono_bold"], 19, C["ink2"], 1, 0.1)
                    c.fill_rrect(sx + sw - 90, ry + 24, 34, 34, 17, GREEN if k == 0 else C["faint"])
                bp = 1 - 0.06 * math.sin(math.pi * prog(t, t_tap, 0.2))
                bx, by, bw, bh = sx + 30, sy + sh - 130, sw - 60, 90
                with c.at(0, 0, bp, origin=(bx + bw / 2, by + bh / 2)):
                    c.fill_rrect(bx, by, bw, bh, 45, GREEN)
                    c.text(bx + bw / 2, by + 58, "Beli", F["display_semi"], 40, WHITE, 1, -0.02, align="c")
        if err > 0:
            c.text(sx + sw / 2, sy + sh * 0.5, "503", F["display"], 130, C["ink"], err, -0.05, align="c")
            c.text(sx + sw / 2, sy + sh * 0.5 + 60, "Service Unavailable", F["mono_med"], 19, C["muted"], err, 0.04,
                   align="c")
    return screen


def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    t_kursi = T.word("L01", "kursi")
    t_jari = T.word("L01", "jari")
    t_det = T.word("L01", "detik")
    t_tap = T.word("L02", "pencet")
    t_err = T.word("L02", "error")
    t_d = [T.word("L03", "detik", 0), T.word("L03", "per"), T.word("L03", "detik", 1)]
    heads = [(Headline("Semua di *satu detik*."), L1.start, L2.start - 0.15),
             (Headline("Yang keluar: *error*."), L2.start, L3.start - 0.15),
             (Headline("Detik per *detik*."), L3.start, e - OUT)]
    card = (X, 560, CW, 380)
    cols, rows, ss = 22, 8, 37
    gx0 = X + (CW - cols * ss) / 2 + 4
    ph = (MID - 180, 560, 360, 700)
    slot = (MID - 120, 1300, 240)

    cam = v.camera
    cam.key(0.0, zoom=1.05, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.4, ease=out_cubic)
    cam.focus(t_err - 0.15, (ph[0], ph[1] + 200, ph[2], 600), zoom=1.07, dur=0.4)
    cam.reset(L3.start - 0.1, dur=0.4)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "WAR TIKET · JAM 10.00", GREEN)
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def seats(c):
            c.card(*card, r=26)
            c.text(X + 30, 600, "PANGGUNG", F["mono_bold"], 18, C["muted"], 1, 0.2)
            for j in range(rows):
                for i in range(cols):
                    d = math.hypot(i - cols / 2, j) / cols
                    a = out_expo(prog(t, t_kursi - 0.3 + d * 0.6, 0.4))
                    if a > 0:
                        c.fill_rrect(gx0 + i * ss, 630 + j * ss, ss - 9, ss - 9, 6, GREEN, 0.18 + 0.5 * a)
            _ripples(c, t, t_jari - 0.1, gx0, 630, cols * ss, rows * ss, 26, seed=4)
        appear(c, t, L1.start - 0.1, L2.start - 0.15, card, seats, enter="up", exit="left")

        def clock(c):
            jp = prog(t, t_det, 0.35)
            big_clock(c, MID, 1160, "10:00:00" if jp > 0 else "09:59:59", 150, prev="09:59:59", jump=jp,
                      accent_from=6, align="c")
        appear(c, t, T.word("L01", "satu") - 0.2, L2.start - 0.15, (MID - 380, 1020, 760, 170), clock,
               enter="up", exit="left", blur=6)
        appear(c, t, L2.start - 0.1, L3.start - 0.15, ph,
               lambda c: phone(c, *ph, draw_screen=_ticket_screen(t, t_tap, t_err)), enter="right", exit="left")
        fade(c, t, t_err, L3.start - 0.15,
             lambda c: print_slip(c, *slot, 210, prog(t, t_err + 0.1, 0.9),
                                  [("ERROR", "mono_bold", 20, None), ("503", "display", 64, RED),
                                   ("coba lagi", "mono_med", 18, C["muted"])], color=RED, rot=-0.04))

        def ruler(c):
            big_clock(c, MID, 900, "10:00:00", 170, accent_from=6, align="c")
            x0, x1, ry = X + 60, X + CW - 60, 1080
            c.line(x0, ry, x1, ry, C["faint"], 3)
            for k, (lbl, f) in enumerate(((":00", 0.0), (":01", 0.1), (":10", 1.0))):
                px = lerp(x0, x1, f)
                lit = out_expo(prog(t, t_d[k], 0.3))
                c.circle(px, ry, 10 + 4 * lit, GREEN if lit > 0 else C["faint"])
                c.text(px, ry + 54, lbl, F["mono_bold"], 26, GREEN if lit > 0.5 else C["muted"], 1, 0.04, align="c")
        appear(c, t, L3.start - 0.1, e - OUT, (X, 740, CW, 400), ruler, enter="up")
    v.add(s, e + 0.4, draw)
    v.track(Cursor([(L2.start + 0.2, 860, 1500), (t_tap, MID + 60, ph[1] + ph[3] - 90)], clicks=[t_tap],
                   hide=t_err + 0.3))
    v.sfx("pop", t_kursi - 0.2, 0.5)
    for k in range(4):
        v.sfx("tick", t_jari + k * 0.2, 0.35)
    v.sfx("thud", t_det, 0.7)
    v.sfx("thud", t_err)
    for tt in t_d:
        v.sfx("tick", tt, 0.5)


# ── 00 · 10:00:00: the line doesn't climb, it goes vertical ────────────
def detik00(v, T, s, e):
    ch = v.chapter(0, "10:00:00", s, e)
    L4, L5 = T["L04"], T["L05"]
    t_klik = T.word("L04", "klik")
    t_sama = T.word("L04", "sama")
    t_pelan = T.word("L05", "pelan")
    t_tegak = T.word("L05", "tegak")
    head1 = Headline("Semua klik *barengan*.")
    head2 = Headline("Grafiknya *tegak lurus*.")
    card = (X, 590, CW, 780)
    px, py, pw, ph = X + 60, 720, CW - 120, 520
    base = py + ph - ph * 0.06
    xm = px + pw * 0.5

    cam = v.camera
    cam.focus(L4.start, card, zoom=1.03, dur=1.0)
    cam.key(t_tegak + 0.15, zoom=0.97, dur=0.12)
    cam.key(t_tegak + 0.27, zoom=1.0, dur=0.5)

    def draw(c, t):
        kicker(c, t, L4.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L4.start, L5.start - 0.15)
        head2.draw(c, t, L5.start, e - OUT)

        def graph(c):
            c.card(*card, r=26)
            c.text(X + 40, 645, "TRAFFIC · PER DETIK", F["mono_bold"], 18, C["muted"], 1, 0.16)
            c.text(X + CW - 40, 645, "ilustrasi", F["serif"], 30, C["muted"], 1, align="r")
            big_clock(c, X + CW - 40, 700, "10:00:00", 30, accent_from=6, align="r")
            c.line(px, py + ph, px + pw, py + ph, C["faint"], 2)
            for f, lbl in ((0.0, "09:59:50"), (0.5, "10:00:00"), (1.0, "10:00:10")):
                c.text(px + pw * f, py + ph + 44, lbl, F["mono_med"], 18, C["ink2"] if f == 0.5 else C["muted"], 1,
                       0.04, align="c")
            # flat line up to 10:00:00
            fp = in_out_cubic(prog(t, L4.start + 0.1, max(0.4, t_sama - L4.start - 0.1)))
            pts = [(px + pw * 0.5 * k / 20, base - 6 * math.sin(k * 1.7)) for k in range(21)]
            _draw_poly(c, pts, fp, GREEN, 4)
            # what people imagine: a slow climb (ghost, dashed)
            gp = prog(t, t_pelan - 0.2, 0.8)
            if gp > 0:
                ghost = [(xm + pw * 0.5 * k / 20, base - ph * 0.45 * (k / 20) ** 2) for k in range(21)]
                c.ctx.set_dash([10, 10])
                _draw_poly(c, ghost, gp, C["ink2"], 3, 0.45 * (1 - 0.5 * prog(t, t_tegak, 0.4)))
                c.ctx.set_dash([])
                c.text(xm + pw * 0.36, base - ph * 0.3, "naik pelan?", F["serif"], 34, C["ink2"],
                       out_expo(gp) * (1 - 0.6 * prog(t, t_tegak, 0.4)))
            # the real thing: straight up
            vp = out_expo(prog(t, t_tegak - 0.05, 0.35))
            if vp > 0:
                top = lerp(base, py - 40, vp)
                c.line(xm, base, xm, top, RED, 6)
                for da in (-0.6, 0.6):
                    c.line(xm, top, xm + 22 * math.sin(da), top + 22 * math.cos(da), RED, 6)
                c.text(xm + 24, py + 30, "semua, detik ini", F["mono_bold"], 20, RED, clamp(vp * 2 - 1), 0.04)
            _ripples(c, t, t_klik - 0.1, xm - 60, base - 60, 120, 60, 10, seed=7, color=GREEN)
        appear(c, t, L4.start - 0.15, e - OUT, card, graph, enter="up")
    v.add(s, e, draw)
    v.sfx("whoosh", L4.start - 0.15, 0.5)
    v.sfx("pop", t_klik, 0.5)
    v.sfx("whoosh", t_pelan - 0.2, 0.3)
    v.sfx("thud", t_tegak)


# ── 01 · 10:00:01: the lokets fill up, the losers get 503 → refresh ──
NL = 4
LW, LH = 190, 260


def _loket_x(k, n=NL, w=LW):
    gap = (CW - n * w) / (n - 1)
    return X + k * (w + gap)


def detik01(v, T, s, e):
    ch = v.chapter(1, "10:00:01", s, e)
    L6, L7, L8 = T["L06"], T["L07"], T["L08"]
    t_penuh = T.word("L06", "penuh")
    t_err = T.word("L06", "error")
    t_ref = T.word("L07", "refresh")
    t_ref2 = T.word("L08", "refresh")
    t_dobel = T.word("L08", "dobel")
    heads = [(Headline("Loketnya *penuh*."), L6.start, L7.start - 0.15),
             (Headline("Terus: *refresh*."), L7.start, L8.start - 0.15),
             (Headline("Traffic-nya *dobel*."), L8.start, e - OUT)]
    ly = 600

    cam = v.camera
    cam.focus(t_err - 0.2, (X, ly + 150, CW, 400), zoom=1.06, dur=0.5)
    cam.reset(t_ref - 0.1, dur=0.3)
    cam.key(t_ref + 0.05, zoom=0.97, dur=0.12)
    cam.key(t_ref + 0.17, zoom=1.0, dur=0.5)

    def draw(c, t):
        kicker(c, t, L6.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        full = prog(t, t_penuh, 0.4)

        def row(c):
            for k in range(NL):
                x = _loket_x(k)
                lane = [(x + LW / 2 + (k - 1.5) * 40, 1340), (x + LW / 2, ly + LH + 30)]
                queue_dots(c, lane, t, n=9, speed=0.5, jam=full, r=9, seed=k)
            storm = prog(t, t_ref2 - 0.2, max(0.5, t_dobel - t_ref2 + 0.2))
            refresh_storm(c, MID, ly + LH / 2 + 60, 470, 330, t, n=40, amount=0.5 * storm, seed=3)
            for k in range(NL):
                x = _loket_x(k)
                slot = loket(c, x, ly, LW, LH, t, full=prog(t, t_penuh + k * 0.08, 0.4), label=f"server {k + 1}",
                             seed=k)
                print_slip(c, *slot, 170, prog(t, t_err + k * 0.15, 0.8),
                           [("ERROR", "mono_bold", 17, None), ("503", "display", 44, RED)], color=RED,
                           rot=(-0.06, 0.05, -0.03, 0.07)[k])
        appear(c, t, L6.start - 0.15, e - OUT, (X, ly, CW, 760), row, enter="up", blur=6)

        def big_refresh(c):
            refresh_icon(c, MID, 1200, 210, RED, rot=t * 2.5, width=26)
        appear(c, t, t_ref - 0.05, L8.start + 0.4, (MID - 130, 1070, 260, 260), big_refresh, enter="pop", exit="pop")

        def meter(c):
            bp = prog(t, t_dobel - 0.3, 0.6)
            c.text(X, 1360, "TRAFFIC", F["mono_bold"], 18, C["muted"], 1, 0.16)
            c.fill_rrect(X, 1380, CW, 26, 13, C["faint"], 0.5)
            c.fill_rrect(X, 1380, CW * (0.45 + 0.45 * out_expo(bp)), 26, 13, RED)
            c.text(X + CW, 1360, "×2" if bp > 0.5 else "×1", F["mono_bold"], 22, RED, 1, 0.04, align="r")
        appear(c, t, L8.start, e - OUT, (X, 1330, CW, 90), meter, enter="up", rise=16)
    v.add(s, e, draw)
    v.sfx("whoosh", L6.start - 0.15, 0.5)
    for k in range(NL):
        v.sfx("pop", t_penuh + k * 0.08, 0.35)
        v.sfx("tick", t_err + k * 0.15, 0.35)
    v.sfx("thud", t_ref)
    for k in range(6):
        v.sfx("tick", t_ref2 + k * 0.18, 0.3)
    v.sfx("thud", t_dobel, 0.6)


# ── 02 · 10:00:10: retry storm — more lokets, bigger storm ─────────────
def detik10(v, T, s, e):
    ch = v.chapter(2, "10:00:10", s, e)
    L9, L10 = T["L09"], T["L10"]
    t_retry = T.word("L09", "retry")
    t_tambah = T.word("L10", "nambah")
    t_gede = T.word("L10", "gede")
    head1 = Headline("*Retry storm*.")
    head2 = Headline("Badainya ikut *gede*.")
    w, h = 170, 230
    rows_y = [760, 1030]
    cy = 1010

    cam = v.camera
    cam.key(L9.start, zoom=1.0, dur=0.01)
    cam.key(L9.start + 0.1, zoom=1.08, x=MID, y=cy, dur=2.4)
    cam.key(t_tambah, zoom=1.0, dur=1.2, ease=out_cubic)

    def draw(c, t):
        kicker(c, t, L9.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L9.start, L10.start - 0.15)
        head2.draw(c, t, L10.start, e - OUT)
        amount = lerp(0.25, 0.5, prog(t, L9.start, 2.0)) + 0.5 * prog(t, t_tambah + 0.3, max(0.6, t_gede - t_tambah))

        def storm(c):
            rx = lerp(470, 520, prog(t, t_tambah, 1.0))
            refresh_storm(c, MID, cy, rx, 470, t, n=56, amount=amount, inward=prog(t, t_retry, 0.8), seed=5,
                          size=(24, 50))
            for r, ry in enumerate(rows_y):
                for k in range(NL):
                    x = _loket_x(k, w=w)
                    if r == 0:
                        loket(c, x, ry, w, h, t, full=1.0, label=f"server {k + 1}", seed=k)
                    else:
                        t0 = t_tambah + k * 0.1
                        if t >= t0:
                            p = out_back(prog(t, t0, 0.4), 1.6)
                            with c.at(0, 0, max(0.01, p), origin=(x + w / 2, ry + h / 2)):
                                loket(c, x, ry, w, h, t, full=prog(t, t0 + 0.6, 0.4), label=f"server {k + 5}",
                                      seed=k + 4)
            _ptag(c, t, t_retry, X, 600, "retry storm", RED)
        appear(c, t, L9.start - 0.15, e - OUT, (X, 560, CW, 900), storm, blur=4, rise=12)
    v.add(s, e, draw)
    v.sfx("whoosh", L9.start - 0.15, 0.6)
    v.sfx("pop", t_retry, 0.5)
    for k in range(NL):
        v.sfx("pop", t_tambah + k * 0.1, 0.35)
    v.sfx("whoosh", t_gede - 0.2, 0.5)


# ── 03 · ANTREAN: take a number; the server only takes so many per second ──
def _serving(t, t_slow, t_fast, t_end):
    """(current, previous, jump) of the 'SEKARANG MELAYANI' display: slow steps, then a fast run to 29.481."""
    steps = [(t_slow + k * 0.6, 28120 + 37 * (k + 1)) for k in range(int(max(0.0, t_fast - t_slow) / 0.6))]
    last = steps[-1][1] if steps else 28120
    for k in range(10):
        steps.append((t_fast + (t_end - t_fast) * (k + 1) / 10, int(lerp(last, 29481, (k + 1) / 10))))
    cur, prev, t0 = 28120, None, -1.0
    for st, val in steps:
        if t < st:
            break
        prev, cur, t0 = cur, val, st
    return fmt_id(cur), (fmt_id(prev) if prev is not None else None), prog(t, t0, 0.25)


def antrean(v, T, s, e):
    ch = v.chapter(3, "ANTREAN", s, e)
    L11, L12, L13, L14 = T["L11"], T["L12"], T["L13"], T["L14"]
    t_vwr = T.word("L11", "virtual")
    t_karcis = T.word("L12", "karcis")
    t_rate = T.word("L13", "rate")
    t_nunggu = T.word("L13", "nunggu")
    t_tapi = T.word("L14", "tapi")
    t_cepet = T.word("L14", "cepet")
    heads = [(Headline("Virtual *waiting room*."), L11.start, L12.start - 0.15),
             (Headline("Ambil *karcis*."), L12.start, L13.start - 0.15),
             (Headline("Masuk *segini* per detik."), L13.start, L14.start - 0.15),
             (Headline("Majunya *cepet*."), L14.start, e - OUT)]
    dcx, dy, ds = X + 190, 600, 340
    lw, lh = 190, 250
    lx = [X + 438, X + 658]
    ly = 620
    gate_x = X + 400

    cam = v.camera
    cam.focus(t_karcis - 0.2, (dcx - 170, dy + 380, 340, 420), zoom=1.08, dur=0.5)
    cam.reset(L13.start - 0.1, dur=0.5)
    cam.focus(t_tapi - 0.2, (dcx - 170, dy, 340, 300), zoom=1.1, dur=0.5)
    cam.reset(t_cepet + 0.8, dur=0.6)

    def draw(c, t):
        kicker(c, t, L11.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        cur, prev, jp = _serving(t, L12.start, t_tapi, t_cepet + 0.1)
        called = prog(t, t_cepet + 0.1, 0.3)

        def scene(c):
            # the rest wait in a long, calm line (bottom)
            wa = prog(t, t_nunggu - 0.3, 0.6)
            queue_dots(c, [(X + CW, 1470), (X, 1470)], t, n=16, speed=0.03, r=9, seed=9, alpha=wa)
            fade(c, t, t_nunggu, e - OUT,
                 lambda c: c.text(X, 1430, "sisanya nunggu", F["mono_med"], 18, C["muted"], 1, 0.04))
            # orderly flow: machine → rate limit gate → green lokets
            fa = prog(t, t_rate - 0.3, 0.6)
            for k in range(2):
                path = [(dcx + ds / 2 - 10, 1000), (gate_x, 1000), (lx[k] + lw / 2, 1000), (lx[k] + lw / 2, ly + lh + 20)]
                c.ctx.set_dash([8, 8])
                _draw_poly(c, path, fa, GREEN, 2.5, 0.5)
                c.ctx.set_dash([])
                queue_dots(c, path, t, n=4, speed=0.18, r=8, seed=20 + k, color=GREEN, alpha=fa)
            if fa > 0:
                c.fill_rrect(gate_x - 6, 950, 12, 100, 6, C["ink2"], fa)
            _ptag(c, t, t_rate, gate_x - 30, 1070, "rate limit", C["accent"])
            for k in range(2):
                loket(c, lx[k], ly, lw, lh, t, full=0.0, label=f"server {k + 1}", seed=k,
                      alpha=out_expo(prog(t, L11.start + 0.3 + k * 0.1, 0.5)))
            slot = dispenser(c, dcx, dy, ds, t, serving=cur, serving_prev=prev, jump=jp, called=called,
                             press=math.sin(math.pi * prog(t, t_karcis - 0.25, 0.25)))
            print_slip(c, *slot, 270, prog(t, t_karcis, 1.0),
                       [("NOMOR ANTREAN", "mono_bold", 18, None), ("29.481", "display", 56, GREEN),
                        ("tunggu dipanggil", "mono_med", 17, C["muted"])], rot=0.04)
            _ptag(c, t, t_vwr, lx[0], 566, "virtual waiting room", GREEN)
        appear(c, t, L11.start - 0.15, e - OUT, (X, 560, CW, 940), scene, enter="up", blur=6)
        fade(c, t, t_cepet + 0.3, e - OUT,
             lambda c: note(c, X + 420, 1290, "itu kamu", prog(t, t_cepet + 0.3, 0.8), arrow_to=(X + 300, 1165),
                            color=GREEN, size=40))
    v.add(s, e, draw)
    v.sfx("whoosh", L11.start - 0.15, 0.5)
    v.sfx("pop", t_vwr, 0.5)
    v.sfx("click", t_karcis - 0.2, 0.7)
    for k in range(5):
        v.sfx("tick", t_karcis + k * 0.12, 0.25)
    v.sfx("pop", t_rate, 0.5)
    for k in range(10):
        v.sfx("tick", t_tapi + (t_cepet + 0.1 - t_tapi) * (k + 1) / 10, 0.3)
    v.sfx("chime", t_cepet + 0.1)


# ── RECAP (dark): the refresh button crossed out → calm green lokets ───
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L15, L16 = T["L15"], T["L16"]
    t_sendiri = T.word("L15", "sendiri")
    t_crash = T.word("L16", "crash")
    head1 = Headline("Musuhnya: tombol *refresh*.", style="headline_dark")
    head2 = Headline("Lambat, tapi *nggak crash*.", style="headline_dark")
    bx, by, br = MID, 960, 230
    ly, lw, lh = 640, 190, 250

    cam = v.camera
    cam.focus(t_sendiri - 0.3, (bx - br, by - br, 2 * br, 2 * br), zoom=1.06, dur=0.5)
    cam.reset(L16.start - 0.1, dur=0.4)
    cam.focus(t_crash - 0.3, (MID - 200, ly + lh, 400, 320), zoom=1.08, dur=0.5)
    cam.reset(e - 0.5, dur=0.4)

    def draw(c, t):
        head1.draw(c, t, L15.start, L16.start - 0.15)
        head2.draw(c, t, L16.start, e - OUT)

        def button(c):
            c.shadow(bx - br, by - br, 2 * br, 2 * br, br, 40, 16, 0.3)
            c.circle(bx, by, br, C["d_card"])
            c.circle(bx, by, br, C["d_line"])
            refresh_icon(c, bx, by, br * 1.0, C["d_ink"], rot=t * 1.5, width=24)
            xp = out_expo(prog(t, t_sendiri, 0.4))
            if xp > 0:
                d = br * 0.8
                c.line(bx - d, by - d, bx - d + 2 * d * xp, by - d + 2 * d * xp, RED, 18)
                xp2 = out_expo(prog(t, t_sendiri + 0.15, 0.4))
                if xp2 > 0:
                    c.line(bx + d, by - d, bx + d - 2 * d * xp2, by - d + 2 * d * xp2, RED, 18)
        appear(c, t, L15.start - 0.1, L16.start - 0.15, (bx - br, by - br, 2 * br, 2 * br), button, enter="pop",
               exit="left")

        def calm(c):
            for k in range(NL):
                x = _loket_x(k)
                lane = [(x + LW / 2, 1300), (x + LW / 2, ly + lh + 20)]
                queue_dots(c, lane, t, n=4, speed=0.2, r=8, seed=k, color=GREEN)
                slot = loket(c, x, ly, LW, lh, t, full=0.0, label=f"server {k + 1}", seed=k, busy=0.4)
                if k == 1:
                    print_slip(c, *slot, 200, prog(t, t_crash - 0.2, 0.9),
                               [("giliranmu", "mono_bold", 18, None), ("dipanggil", "display", 36, GREEN)], rot=-0.04)
        appear(c, t, L16.start - 0.1, e - OUT, (X, ly, CW, 700), calm, enter="right")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("thud", t_sendiri)
    v.sfx("whoosh", L16.start - 0.1, 0.5)
    v.sfx("pop", t_crash - 0.2, 0.5)
    v.sfx("chime", t_crash + 0.3)


# ── OUTRO: logo + next video (roadmap) + follow ────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L17, L18 = T["L17"], T["L18"]
    t_click = T.word("L18", "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, GREEN)
            c.text(X + 50, 892, "VIDEO BERIKUTNYA", F["mono_bold"], 20, GREEN, 1, 0.16)
            c.text(X + 50, 962, "Roadmap jadi cloud engineer", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "mulai dari nol.", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L17.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L18.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "mumeyong.dev", F["mono_med"], 28,
                                                          C["d_muted"], 1, 0.06, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L18.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L17.start, 0.5)
    v.sfx("chime", t_click + 0.1)
