"""QRIS: apa yang terjadi setelah kamu scan? — idea #08, pillar B, QUICK. See IDENTITY.md / TREATMENT.md.

Metaphor: a relay race — the baton is the transaction message, runners are your app → issuer → switching → acquirer.
Signature move: freeze → slow-motion replay (REPLAY 0,1× badge, crawling timecode, baton with a motion trail).
Color: purple. Hook: freeze-frame on an everyday moment. Structure: real speed → replay per runner → twist.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp, lerp, mix
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, follow_button, phone, fmt_id,
                               qr_code, qris_stand, es_teh, relay_track, slowmo_badge, mesh_hub, cover, PURPLE)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · APP KAMU", "01 · ISSUER", "02 · SWITCHING", "03 · ACQUIRER", "RECAP", "OUTRO"]
OK = C["ok"]
RED = C["rec"]
WHITE = (1, 1, 1, 1)

TRACK = (X, 1220, CW, 120)
XS = [X + 90, X + 310, X + 538, X + 758]
RUNNERS = ["app kamu", "issuer", "switching", "acquirer"]


def build(project):
    T = project.timing
    v = Video(duration=T["L19"].end + TAIL, bpm=128, beat_offset=0.0, series="REPLAY")
    v.cover_t = T.word("L11", "tol") + 0.9
    v.music = dict(key="D", mood="bright")            # generated score: light, after A dreamy (#12)
    v.cover = lambda c: cover(c, "Satu beep,\n*4 pelari*.", kicker="QRIS · SETELAH KAMU SCAN", color=PURPLE,
                              badge="REPLAY", tags=["issuer", "switching", "acquirer"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    arrive = [T["L05"].start, T["L07"].start, T["L09"].start, T["L12"].start]
    intro(v, T, 0.0, b["00 · APP KAMU"])
    track(v, T, T["L04"].start - 0.1, b["RECAP"], arrive)
    app(v, T, b["00 · APP KAMU"], b["01 · ISSUER"])
    issuer(v, T, b["01 · ISSUER"], b["02 · SWITCHING"])
    switching(v, T, b["02 · SWITCHING"], b["03 · ACQUIRER"])
    acquirer(v, T, b["03 · ACQUIRER"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


def _cover_hero(c, box):
    """Cover hero: the warung counter (standee + es teh) above the 4-runner track."""
    x, y, w, h = box
    base = y + h - 170
    qris_stand(c, x + w * 0.62, base, min(250, h * 0.45))
    es_teh(c, x + w * 0.2, base, min(220, h * 0.4))
    c.line(x, base, x + w, base, C["faint"], 4)
    relay_track(c, x, base + 40, w, 100, [x + w * f for f in (0.1, 0.36, 0.63, 0.9)], [], 0.0,
                baton_x=x + w * 0.45, lit=[1, 1, 1, 0], slow=1.0)


def _pop(c, t, t0, cx, cy, draw, d=0.4):
    if t < t0:
        return
    p = out_back(prog(t, t0, d), 1.7)
    with c.at(0, 0, max(0.01, p), origin=(cx, cy)):
        with c.group(clamp(p * 2)):
            draw(c)


def _ptag(c, t, t0, x, y, label, color=None, h=40, align="l"):
    color = color or C["accent"]
    w = c.measure(label, F["ui"], tk.T["tag"][0], tk.T["tag"][1])[0] + 30
    cx_ = x + w / 2 if align == "l" else x - w / 2
    _pop(c, t, t0, cx_, y + h / 2, lambda c: tag(c, x, y, label, color, align=align, h=h))


def _check_row(c, t, t0, x, y, text, color=None, size=30):
    """✓ circle + text, popping at t0."""
    color = color or OK
    a = out_expo(prog(t, t0, 0.4))
    if a <= 0:
        return
    s = out_back(prog(t, t0, 0.4), 1.8)
    with c.at(0, 0, max(0.01, s), origin=(x + 22, y - 10)):
        c.circle(x + 22, y - 10, 22, color, a)
        icons.check(c, x + 22, y - 10, 18, WHITE, 3.5, alpha=a)
    c.text(x + 60, y, text, F["ui_semi"], size, C["ink"], a, -0.01)


# ── INTRO: es teh, scan, PIN, beep — then freeze ───────────────────────
def _pay_screen(t, t_scan, t_pin, t_beep):
    def screen(c, sx, sy, sw, sh):
        c.fill_rrect(sx, sy, sw, sh, 0, C["card"])
        ok = prog(t, t_beep, 0.3)
        if ok < 1:
            with c.group(1 - ok):
                # camera view with the QR inside scan corners
                q = sw * 0.6
                qx, qy = sx + (sw - q) / 2, sy + 90
                c.fill_rrect(sx + 20, sy + 60, sw - 40, q + 60, 18, C["bg"])
                qr_code(c, qx, qy, q, 7)
                for (cx_, cy_, dx, dy) in ((qx - 10, qy - 10, 1, 1), (qx + q + 10, qy - 10, -1, 1),
                                           (qx - 10, qy + q + 10, 1, -1), (qx + q + 10, qy + q + 10, -1, -1)):
                    c.line(cx_, cy_, cx_ + 34 * dx, cy_, PURPLE, 6)
                    c.line(cx_, cy_, cx_, cy_ + 34 * dy, PURPLE, 6)
                sp = prog(t, t_scan, 0.6)
                if 0 < sp < 1:
                    ly = qy + q * in_out_cubic(sp)
                    c.line(qx - 6, ly, qx + q + 6, ly, PURPLE, 4, 0.9)
                c.text(sx + sw / 2, qy + q + 90, "Warung Es Teh", F["ui_semi"], 26, C["ink"], 1, -0.01, align="c")
                c.text(sx + sw / 2, qy + q + 140, "Rp5.000", F["display"], 50, C["ink"], 1, -0.03, align="c")
                # PIN dots
                pa = prog(t, t_pin - 0.1, 0.3)
                if pa > 0:
                    for k in range(6):
                        filled = prog(t, t_pin + k * 0.08, 0.1)
                        px = sx + sw / 2 + (k - 2.5) * 34
                        py = sy + sh - 90
                        c.circle(px, py, 11, C["faint"], pa)
                        c.circle(px, py, 11 * filled, PURPLE, pa)
        if ok > 0:
            s = out_back(ok, 1.8)
            cx_, cy_ = sx + sw / 2, sy + sh * 0.4
            with c.at(0, 0, max(0.01, s), origin=(cx_, cy_)):
                c.circle(cx_, cy_, 80, OK, ok)
                icons.check(c, cx_, cy_, 64, WHITE, 8, alpha=ok)
            c.text(cx_, cy_ + 150, "Berhasil", F["display_semi"], 44, C["ink"], ok, -0.02, align="c")
            c.text(cx_, cy_ + 200, "Rp5.000 · Warung Es Teh", F["mono_med"], 19, C["muted"], ok, 0.02, align="c")
    return screen


def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3, L4 = T["L01"], T["L02"], T["L03"], T["L04"]
    t_teh = T.word("L01", "teh")
    t_qris = T.word("L01", "qris")
    t_scan = T.word("L02", "scan")
    t_pin = T.word("L02", "pin")
    t_beep = T.word("L02", "beep")
    t_tahan = T.word("L03", "tahan")
    heads = [(Headline("Es teh *lima ribu*."), L1.start, L2.start - 0.15),
             (Headline("*Beep*. Kelar."), L2.start, L3.start - 0.15),
             (Headline("*Tahan*."), L3.start, L4.start - 0.15),
             (Headline("Estafet *empat* pelari."), L4.start, e - OUT)]
    counter = (X, 640, CW, 540)
    base = 1150
    ph = (MID - 175, 590, 350, 640)

    cam = v.camera
    cam.key(0.0, zoom=1.05, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.key(t_beep, zoom=0.97, dur=0.12)
    cam.key(t_beep + 0.12, zoom=1.0, dur=0.4)
    cam.key(t_tahan, zoom=1.04, dur=0.25)
    cam.reset(L4.start - 0.1, dur=0.5)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "QRIS · SETELAH KAMU SCAN", PURPLE)
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def warung(c):
            c.line(X, base, X + CW, base, C["faint"], 5)
            _pop(c, t, t_teh - 0.2, X + 200, base - 130, lambda c: es_teh(c, X + 200, base, 260, t))
            _pop(c, t, t_qris - 0.2, X + 580, base - 210, lambda c: qris_stand(c, X + 580, base, 300))
        appear(c, t, L1.start - 0.1, L2.start - 0.15, counter, warung, enter="up", exit="left")
        frozen = prog(t, t_tahan, 0.2)

        def pay(c):
            phone(c, *ph, draw_screen=_pay_screen(t, t_scan, t_pin, t_beep))
            if frozen > 0:
                x, y, w, h = ph
                c.fill_rrect(x, y, w, h, w * 0.13, WHITE, 0.45 * frozen)
                c.fill_rrect(MID - 40, y + h / 2 - 60, 28, 120, 8, C["ink"], frozen)
                c.fill_rrect(MID + 12, y + h / 2 - 60, 28, 120, 8, C["ink"], frozen)
        appear(c, t, L2.start - 0.15, L4.start - 0.15, ph, pay, enter="up", exit="left")
        fade(c, t, t_tahan, L4.start - 0.15, lambda c: slowmo_badge(c, X + CW, 1440, t, frozen=1.0, tc="0,00 s"))
    v.add(s, e + 0.4, draw)
    v.sfx("pop", t_teh - 0.2, 0.4)
    v.sfx("pop", t_qris - 0.2, 0.4)
    v.sfx("tick", t_scan, 0.5)
    for k in range(6):
        v.sfx("key", t_pin + k * 0.08, 0.35)
    v.sfx("chime", t_beep)
    v.sfx("thud", t_tahan, 0.8)


# ── the relay track (L04 → recap): the hero, changing state every chapter ──
def track(v, T, s, e, arrive):
    L4 = T["L04"]
    t_empat = T.word("L04", "empat")
    t_back = T.word("L14", "balik")

    def baton_x(t):
        x = XS[0] - 70
        for k, ta in enumerate(arrive):
            x = lerp(x, XS[k] + 30, in_out_cubic(prog(t, ta - 0.6, 0.9)))
        return x

    def moving(t):
        return max(math.sin(math.pi * prog(t, ta - 0.6, 0.9)) for ta in arrive)

    def draw(c, t):
        def lane(c):
            lit = [prog(t, ta + 0.3, 0.3) for ta in arrive]
            active = next((k for k in range(4) if arrive[k] <= t < (arrive[k + 1] if k < 3 else t_back)), None)
            relay_track(c, *TRACK, XS, RUNNERS, t, baton_x=baton_x(t) if t >= t_empat else None, lit=lit,
                        active=active, back=prog(t, t_back, 1.6), slow=moving(t), draw=prog(t, L4.start, 0.9))
            ok_ = out_back(prog(t, t_back + 1.6, 0.4), 1.8)
            if ok_ > 0:
                with c.at(0, 0, max(0.01, ok_), origin=(XS[0], TRACK[1] - 40)):
                    tag(c, XS[0] - 50, TRACK[1] - 60, "berhasil", OK, h=40)
        appear(c, t, s, e - OUT, (X, TRACK[1] - 80, CW, 260), lane, blur=4, rise=12)
        tc = max(0.0, t - L4.start) * 0.1
        fade(c, t, L4.start + 0.2, e - OUT,
             lambda c: slowmo_badge(c, X + CW, 1440, t, speed="0,1×", tc=fmt_id(tc, 2) + " s"))
    v.add(s, e, draw)
    v.sfx("whoosh", L4.start, 0.5)
    for k in range(4):
        v.sfx("pop", L4.start + 0.2 + k * 0.2, 0.35)
    for ta in arrive:
        v.sfx("whoosh", ta - 0.6, 0.4)
        v.sfx("click", ta + 0.3, 0.4)
    v.sfx("whoosh", t_back, 0.5)
    v.sfx("chime", t_back + 1.6, 0.6)


def _focus(v, t, box, zoom=1.05, dur=0.6):
    v.camera.focus(t, box, zoom=zoom, dur=dur)


# ── 00 · APP KAMU: the QR is data, not money ───────────────────────────
def app(v, T, s, e):
    ch = v.chapter(0, "APP KAMU", s, e)
    L5, L6 = T["L05"], T["L06"]
    t_baca = T.word("L05", "baca")
    t_uang = T.word("L06", "uang")
    t_rows = [T.word("L06", "warung"), T.word("L06", "siapa"), T.word("L06", "mana"), T.word("L06", "mana") + 0.5]
    head1 = Headline("App-mu *baca* kodenya.")
    head2 = Headline("Isinya cuma *data*.")
    q = 300
    qbox = (X, 640, q, q)
    fields = (X + 340, 600, CW - 340, 420)
    rows = [("merchant", "Warung Es Teh"), ("NMID", "ID1020••••••"), ("acquirer", "bank warung"),
            ("nominal", "kamu yang isi")]
    _focus(v, L6.start - 0.2, fields, zoom=1.05)
    v.camera.reset(e - 0.6, dur=0.5)

    def draw(c, t):
        kicker(c, t, L5.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L5.start, L6.start - 0.15)
        head2.draw(c, t, L6.start, e - OUT)

        def code(c):
            x, y, w, h = qbox
            qr_code(c, x, y, w, 7)
            sp = prog(t, t_baca, 0.7)
            if 0 < sp < 1:
                ly = y + h * in_out_cubic(sp)
                c.line(x - 10, ly, x + w + 10, ly, PURPLE, 5, 0.9)
            c.text(x, y + h + 60, "kode QR warung", F["mono_med"], 18, C["muted"], 1, 0.04)
        appear(c, t, L5.start - 0.1, e - OUT, qbox, code, enter="right", exit="left")

        def card(c):
            x, y, w, h = fields
            c.card(x, y, w, h, r=22)
            c.text(x + 30, y + 52, "ISI KODE QR", F["mono_bold"], 18, PURPLE, 1, 0.16)
            for k, ((key, val), tt) in enumerate(zip(rows, t_rows)):
                a = out_expo(prog(t, tt, 0.4))
                ry = y + 120 + k * 76
                c.line(x + 30, ry + 26, x + w - 30, ry + 26, C["line"], 1, a)
                c.text(x + 30, ry, key, F["mono_med"], 19, C["muted"], a, 0.04)
                c.text(x + w - 30, ry, val, F["ui_semi"], 26, C["ink"], a, -0.01, align="r")
            _ptag(c, t, t_uang, x + 30, y + h - 60, "bukan uang", C["orange_pill"])
        appear(c, t, L5.start + 0.2, e - OUT, fields, card, enter="right", exit="left")
    v.add(s, e, draw)
    v.sfx("tick", t_baca, 0.5)
    v.sfx("pop", t_uang, 0.5)
    for tt in t_rows:
        v.sfx("key", tt, 0.4)


# ── 01 · ISSUER: check PIN, check balance, hold the 5.000 ──────────────
def issuer(v, T, s, e):
    ch = v.chapter(1, "ISSUER", s, e)
    L7, L8 = T["L07"], T["L08"]
    t_iss = T.word("L07", "issuer")
    t_pin = T.word("L08", "pin")
    t_saldo = T.word("L08", "saldo")
    t_nahan = T.word("L08", "nahan")
    head1 = Headline("Bank kamu: *issuer*.")
    head2 = Headline("Cek, lalu *tahan*.")
    card = (X + 40, 600, CW - 80, 540)
    _focus(v, t_nahan - 0.2, (card[0], card[1] + 380, card[2], 140), zoom=1.06)
    v.camera.reset(e - 0.6, dur=0.5)

    def draw(c, t):
        kicker(c, t, L7.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L7.start, L8.start - 0.15)
        head2.draw(c, t, L8.start, e - OUT)

        def bank(c):
            x, y, w, h = card
            c.card(x, y, w, h, r=26)
            c.fill_rrect(x, y, 14, h, 7, PURPLE)
            c.text(x + 44, y + 58, "BANK / E-WALLET KAMU", F["mono_bold"], 18, C["muted"], 1, 0.16)
            _ptag(c, t, t_iss, x + w - 40, y + 30, "issuer", PURPLE, align="r")
            hp = prog(t, t_nahan + 0.2, 0.5)
            c.text(x + 44, y + 120, "SALDO", F["mono_med"], 17, C["muted"], 1, 0.14)
            val = "Rp82.500" if hp > 0.5 else "Rp87.500"
            jp = out_expo(prog(t, t_nahan + 0.45, 0.3)) if hp > 0.5 else 1.0
            c.text(x + 44, y + 200 + 20 * (1 - jp), val, F["display"], 78, C["ink"], jp, -0.04)
            _check_row(c, t, t_pin, x + 44, y + 300, "PIN cocok")
            _check_row(c, t, t_saldo, x + 44, y + 370, "saldo cukup")
            ha = out_expo(prog(t, t_nahan, 0.4))
            if ha > 0:
                c.fill_rrect(x + 30, y + 405, w - 60, 90, 18, PURPLE, 0.1 * ha)
                c.text(x + 60, y + 462, "Rp5.000 ditahan", F["ui_semi"], 32, PURPLE, ha, -0.01)
                c.text(x + w - 60, y + 460, "buat Warung Es Teh", F["mono_med"], 18, C["muted"], ha, 0.02, align="r")
        appear(c, t, L7.start - 0.1, e - OUT, card, bank, enter="right", exit="left")
    v.add(s, e, draw)
    v.sfx("pop", t_iss, 0.4)
    v.sfx("pop", t_pin, 0.45)
    v.sfx("pop", t_saldo, 0.45)
    v.sfx("tick", t_nahan, 0.6)


# ── 02 · SWITCHING: one-to-one mess vs one toll road ──────────────────
def switching(v, T, s, e):
    ch = v.chapter(2, "SWITCHING", s, e)
    L9, L10, L11 = T["L09"], T["L10"], T["L11"]
    t_sw = T.word("L09", "switching")
    t_satu = T.word("L10", "satu")
    t_tol = T.word("L11", "tol")
    heads = [(Headline("*Switching*."), L9.start, L10.start - 0.15),
             (Headline("Tanpa dia: *ruwet*."), L10.start, L11.start - 0.15),
             (Headline("Satu *jalan tol*."), L11.start, e - OUT)]
    cx, cy, r = MID, 880, 250
    cam = v.camera
    cam.key(L10.start, zoom=0.98, dur=1.2)
    cam.focus(t_tol - 0.2, (cx - 120, cy - 120, 240, 240), zoom=1.06, dur=0.6)
    cam.reset(e - 0.6, dur=0.5)

    def draw(c, t):
        kicker(c, t, L9.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def net(c):
            mesh_hub(c, cx, cy, r, t, n=6, p_mesh=prog(t, t_satu - 0.3, 1.6), p_hub=prog(t, t_tol - 0.3, 0.8))
            _ptag(c, t, t_sw, X, 600, "switching", PURPLE)
        appear(c, t, L9.start - 0.1, e - OUT, (cx - r - 60, cy - r - 60, 2 * r + 120, 2 * r + 120), net, enter="pop")
    v.add(s, e, draw)
    v.sfx("pop", L9.start, 0.4)
    for k in range(8):
        v.sfx("tick", t_satu - 0.3 + k * 0.2, 0.25)
    v.sfx("thud", t_tol - 0.1, 0.7)
    v.sfx("chime", t_tol + 0.4, 0.5)


# ── 03 · ACQUIRER: the seller's phone rings, the answer runs back ──────
def acquirer(v, T, s, e):
    ch = v.chapter(3, "ACQUIRER", s, e)
    L12, L13, L14 = T["L12"], T["L13"], T["L14"]
    t_acq = T.word("L12", "acquirer")
    t_oke = T.word("L13", "oke")
    t_bunyi = T.word("L13", "bunyi")
    t_back = T.word("L14", "balik")
    heads = [(Headline("Bank warung: *acquirer*."), L12.start, L13.start - 0.15),
             (Headline("HP penjual *bunyi*."), L13.start, L14.start - 0.15),
             (Headline("Jawabannya *balik*."), L14.start, e - OUT)]
    card = (X, 640, 380, 300)
    ph = (X + 470, 600, 330, 560)
    _focus(v, t_bunyi - 0.3, ph, zoom=1.05)
    v.camera.reset(t_back - 0.1, dur=0.6)

    def draw(c, t):
        kicker(c, t, L12.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def bank(c):
            x, y, w, h = card
            c.card(x, y, w, h, r=24)
            c.fill_rrect(x, y, 14, h, 7, PURPLE)
            c.text(x + 40, y + 56, "BANK WARUNG", F["mono_bold"], 18, C["muted"], 1, 0.16)
            _ptag(c, t, t_acq, x + 40, y + 84, "acquirer", PURPLE)
            ok = out_back(prog(t, t_oke, 0.4), 1.8)
            if ok > 0:
                with c.at(0, 0, max(0.01, ok), origin=(x + 80, y + 210)):
                    c.circle(x + 80, y + 210, 40, OK)
                    icons.check(c, x + 80, y + 210, 32, WHITE, 5)
                c.text(x + 140, y + 226, "OK", F["display"], 56, C["ink"], clamp(ok), -0.03)

        appear(c, t, L12.start - 0.1, e - OUT, card, bank, enter="right", exit="left")

        def seller(c):
            def screen(c, sx, sy, sw, sh):
                c.fill_rrect(sx, sy, sw, sh, 0, C["bg"])
                c.text(sx + 30, sy + 50, "HP penjual", F["mono_bold"], 18, C["muted"], 1, 0.08)
                np_ = out_expo(prog(t, t_bunyi - 0.1, 0.5))
                if np_ > 0:
                    ny = sy + 90 - 120 * (1 - np_)
                    c.shadow(sx + 16, ny, sw - 32, 130, 20, 22, 8, 0.12 * np_)
                    c.fill_rrect(sx + 16, ny, sw - 32, 130, 20, C["card"], np_)
                    c.fill_rrect(sx + 34, ny + 30, 44, 44, 12, PURPLE, np_)
                    c.text(sx + 94, ny + 50, "Pembayaran masuk", F["ui_semi"], 22, C["ink"], np_, -0.01)
                    c.text(sx + 94, ny + 88, "Rp5.000", F["display"], 34, C["ink"], np_, -0.02)
            phone(c, *ph, draw_screen=screen, dark=True)
            # sound arcs ("bunyi")
            for k in range(3):
                f = ((t - t_bunyi) * 1.2 + k / 3) % 1.0 if t >= t_bunyi else 0
                if t >= t_bunyi and t < t_back + 0.5:
                    ax, ay = ph[0] + ph[2] + 10, ph[1] + 120
                    c.ctx.new_path()
                    c.ctx.arc(ax, ay, 20 + 40 * f, -0.6, 0.6)
                    c.src(PURPLE, 0.8 * (1 - f))
                    c.ctx.set_line_width(4)
                    c.ctx.stroke()
        appear(c, t, L13.start - 0.3, e - OUT, ph, seller, enter="up", exit="left")
    v.add(s, e, draw)
    v.sfx("pop", t_acq, 0.4)
    v.sfx("pop", t_oke, 0.5)
    v.sfx("chime", t_bunyi, 0.8)


# ── RECAP (dark): it was only a message → settlement later → one slow runner ──
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L15, L16, L17 = T["L15"], T["L16"], T["L17"]
    t_pesan = T.word("L15", "pesan")
    t_set = T.word("L16", "settlement")
    t_lemot = T.word("L17", "lemot")
    heads = [(Headline("Cuma *pesan*.", style="headline_dark"), L15.start, L16.start - 0.15),
             (Headline("Uangnya *belakangan*.", style="headline_dark"), L16.start, L17.start - 0.15),
             (Headline("Satu lemot, *semua* nunggu.", style="headline_dark"), L17.start, e - OUT)]
    bx1, bx2, by = X + 120, X + CW - 120, 960

    cam = v.camera
    cam.key(t_pesan, zoom=1.05, dur=0.4)
    cam.reset(L16.start - 0.1, dur=0.4)

    def draw(c, t):
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def message(c):
            c.fill_rrect(MID - 240, 720, 480, 120, 60, PURPLE)
            c.fill_rrect(MID - 40, 720, 80, 120, 4, WHITE, 0.7)
            pa = out_expo(prog(t, t_pesan, 0.5))
            c.card(MID - 300, 900, 600, 170, r=22, alpha=pa)
            c.text(MID - 260, 960, "PESAN", F["mono_bold"], 18, PURPLE, pa, 0.16)
            c.text(MID - 260, 1020, "bayar Rp5.000 → Warung Es Teh", F["ui_semi"], 28, C["d_ink"], pa, -0.01)
        appear(c, t, L15.start - 0.1, L16.start - 0.15, (MID - 300, 700, 600, 380), message, enter="pop", exit="left")

        def settle(c):
            for bx, lbl in ((bx1, "bank kamu"), (bx2, "bank warung")):
                c.card(bx - 110, by - 90, 220, 180, r=22)
                c.text(bx, by + 10, lbl, F["ui_semi"], 28, C["d_ink"], 1, -0.01, align="c")
            c.ctx.set_dash([12, 10])
            c.line(bx1 + 120, by, bx2 - 120, by, C["d_muted"], 3)
            c.ctx.set_dash([])
            mp = clamp((t - t_set + 0.3) * 0.12)
            mx = lerp(bx1 + 140, bx2 - 140, mp)
            c.fill_rrect(mx - 50, by - 34, 100, 68, 12, OK)
            c.text(mx, by + 12, "Rp", F["display"], 34, WHITE, 1, -0.02, align="c")
            c.text(MID, by + 160, "settlement · belakangan", F["mono_bold"], 22, C["d_muted"],
                   out_expo(prog(t, t_set, 0.5)), 0.08, align="c")
        appear(c, t, L16.start - 0.1, L17.start - 0.15, (X, by - 120, CW, 320), settle, enter="right", exit="left")

        def slow(c):
            dim = [0, 0, out_expo(prog(t, t_lemot, 0.4)), 0]
            relay_track(c, X, 980, CW, 120, XS, RUNNERS, t, baton_x=XS[2] - 40, lit=[1, 1, 0, 0], dim=dim,
                        slow=1.0)
            el = max(0.0, t - L17.start) * 2.2
            c.text(MID, 1300, "00:" + f"{int(el):02d}", F["mono_bold"], 90, RED, out_expo(prog(t, t_lemot, 0.4)),
                   0.02, align="c")
            c.text(MID, 1360, "kamu, di depan kasir", F["mono_med"], 20, C["d_muted"], out_expo(prog(t, t_lemot, 0.4)),
                   0.04, align="c")
        appear(c, t, L17.start - 0.1, e - OUT, (X, 960, CW, 420), slow, enter="right")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("thud", t_pesan, 0.8)
    v.sfx("whoosh", L16.start - 0.1, 0.4)
    v.sfx("tick", t_set, 0.5)
    v.sfx("whoosh", L17.start - 0.1, 0.4)
    v.sfx("thud", t_lemot, 0.6)


# ── OUTRO: logo + next video (EP02) + follow ───────────────────────────
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
            c.fill_rrect(X, 830, 14, 220, 7, PURPLE)
            c.text(X + 50, 892, "VIDEO BERIKUTNYA · BONGKAR EP02", F["mono_bold"], 20, PURPLE, 1, 0.16)
            c.text(X + 50, 962, "Pindahin big data", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "tanpa satu byte hilang.", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L18.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L19.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "mumeyong.dev", F["mono_med"], 28,
                                                          C["d_muted"], 1, 0.06, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L19.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L18.start, 0.5)
    v.sfx("chime", t_click + 0.1)
