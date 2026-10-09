"""Bongkar WiFi Rumah EP 01 — Lampu modem merah "LOS" itu artinya apa? See PLAN.md.

Metaphor: the light's road from the ISP office → pole (ODP box) → your house; every modem lamp points at one place on
that road. Signature: purple light pulses ride the fiber, die at the cut, and the modem lamp says where.
Motion: silk springs · ink headlines · persistent modem hero (Rig) + Morph + sheet · dim exits.
Sound: styled score lofi F dreamy 86 BPM + glass SFX kit.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_back, in_out_cubic
from engine.components import (Headline, kicker, fade, pop_tag, check_badge, brand_intro, series_bumper, curtain,
                               Rig, Morph, sheet, press, drifting, note, strike, tag, bubble, id_card, word_pill,
                               connector, standard_outro, cover, modem, modem_led, fiber_route, route_point,
                               patchcord, LEDS, ODP_F, WIFI_PURPLE as PURPLE)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT, DIM = M["out"], M["dim_out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
OUTRO_TAIL = 3.0
PRE_ROLL = 1.2
RED, OK = C["rec"], C["ok"]
MW = 760                                  # hero modem width at scale 1
CH = ["00 · LOS", "01 · PON", "02 · INTERNET", "RECAP", "OUTRO"]
ROUTE = (X + 24, 600, CW - 84, 800)       # street scene box: inset so the slow drift never leaves the column
CUT_AT = 0.8                              # where the drop cable breaks (arc fraction)

INTRO_L = dict(POWER="g", PON="", LOS="r", INTERNET="", WLAN="g")
PON_L = dict(POWER="g", PON="gb", LOS="", INTERNET="", WLAN="g")
NET_L = dict(POWER="g", PON="g", LOS="", INTERNET="", WLAN="g")
BOOT_L = dict(POWER="g", PON="gb", LOS="", INTERNET="", WLAN="g")
ALL_OK = dict(POWER="g", PON="g", LOS="", INTERNET="g", WLAN="g")


def build(project):
    T = project.timing
    v = Video(duration=T["L19"].end + OUTRO_TAIL, bpm=86, beat_offset=0.0, series="BONGKAR WIFI RUMAH · EP 01")
    brand_intro(v)
    v.music = dict(style="lofi", key="F", mood="dreamy")     # first styled score; all earlier videos = pulse 128
    v.sfx_kit = "glass"
    v.cover = lambda c: cover(c, "Lampu modem\n*merah*?", kicker="BONGKAR WIFI RUMAH · EP 01", color=PURPLE,
                              badge="EP 01", tags=["LOS", "PON", "INTERNET"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    bump0 = T["L03"].end + 0.05
    bump1 = bump0 + 1.4
    b["00 · LOS"] = bump0 + 0.45                              # chapter switch hidden under the bumper
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 1, "Lampu modem merah", PURPLE,
                                                    title=("BONGKAR", "WIFI RUMAH")), z=100)
    v.sfx("whoosh", bump0)
    t_rs = T.word("L14", "restart")
    _hero(v, T, b, t_rs)
    intro(v, T, 0.0, b["00 · LOS"])
    los(v, T, b["00 · LOS"], b["01 · PON"])
    pon(v, T, b["01 · PON"], b["02 · INTERNET"])
    internet(v, T, b["02 · INTERNET"], b["RECAP"], t_rs)
    recap(v, T, b["RECAP"], b["OUTRO"])
    standard_outro(v, T, b["OUTRO"], v.duration, "L19", PURPLE,
                   teaser=dict(kicker="BONGKAR WIFI RUMAH · EP 02", title="Connected, tapi no internet.",
                               sub="Kenapa bisa, dan cek apa dulu."))
    v.cover_t = T["L03"].frac(0.7)
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    mw = min(w * 0.9, 700)
    modem(c, x + w / 2, y + h * 0.62, mw, 0.0, INTRO_L, focus="LOS", focus_p=1.0)


def _heads(c, t, hs):
    for h, a, b_ in hs:
        h.draw(c, t, a, b_, reveal="ink", exit="dim")


def _ink(T, items, end, style="headline"):
    """[(text, line_id)] → headlines handing over line to line (ink in, dim out)."""
    out = []
    for i, (text, lid) in enumerate(items):
        t_out = T[items[i + 1][1]].start - 0.15 if i + 1 < len(items) else end
        out.append((Headline(text, style=style), T[lid].start, t_out))
    return out


def _alive(t, s, e, d_in=0.5):
    return out_expo(prog(t, s, d_in)) * (1 - in_out_cubic(prog(t, e - DIM, DIM)))


# ── the persistent hero: one modem from the cold open to the end of 02 ───
def _hero(v, T, b, t_rs):
    s1, s2, rc = b["01 · PON"], b["02 · INTERNET"], b["RECAP"]
    L2, L3 = T["L02"], T["L03"]
    t_ok = T.word("L14", "ngefek")
    lx, ly = modem_led(0, 0, MW, "LOS")
    hero = Rig(MID - lx * 2.4, 960 - ly * 2.4, s=2.4, a=1.0)          # close-up: the red LOS lamp mid-frame
    hero.to(L2.start + 0.1, x=MID, y=1000, s=1.0, preset="silk", dur=1.5)
    hero.to(b["00 · LOS"] - 0.5, a=0.0, dur=0.3)
    hero.to(s1 - 0.05, y=1120, s=0.84, dur=0.02)
    hero.to(s1 + 0.15, y=860, a=1.0, preset="silk", dur=1.1)
    hero.to(s2 + 0.05, y=760, s=0.6, preset="silk", dur=1.1)
    hero.to(rc - 0.45, a=0.0, dur=0.4)

    def lights(t):
        if t < s1:
            return INTRO_L
        if t < s2:
            return PON_L
        if t < t_rs + 0.15:
            return NET_L
        if t < t_rs + 0.95:
            return {}                                                  # restart: everything off
        return BOOT_L if t < t_ok else ALL_OK

    def focus(t):
        if t < s1:
            return "LOS", prog(t, L2.start + 0.6, 0.5) * (1 - prog(t, L3.start + 0.2, 0.4))
        if t < s2:
            return "PON", prog(t, T["L09"].start, 0.5) * (1 - prog(t, s2 - 0.6, 0.4))
        return "INTERNET", prog(t, T["L12"].start, 0.5) * (1 - prog(t, t_rs - 0.3, 0.3))

    def draw(c, t):
        if b["00 · LOS"] - 0.15 < t < s1 - 0.05:
            return
        name, fp = focus(t)
        with hero.place(c, t):
            modem(c, 0, 0, MW, t, lights(t), focus=name, focus_p=fp)
    v.add(0.0, rc, draw, z=5)
    v.sfx("click", t_rs + 0.1, 0.6)
    v.sfx("tick", t_rs + 0.95, 0.6)
    v.sfx("chime", t_ok)


# ── INTRO: cold open on the red lamp → pull back → every lamp = one place → bumper ─
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    v.add(s, L1.start + 1.2, lambda c, t: curtain(c, t, L1.start - 0.4), z=100)
    hs = _ink(T, [("Masalahnya\ndi *kabel*.", "L02"), ("Tiap lampu,\n*satu tempat*.", "L03")], e - DIM)
    hs[0] = (hs[0][0], T.word("L02", "kabel") - 0.35, hs[0][2])
    places = [("PON", "kantor ISP", "lampu"), ("LOS", "kabel", "tempat"), ("INTERNET", "akun", "baca")]

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "21:00 · DI RUMAH", PURPLE)
        _heads(c, t, hs)
        for name, label, word in places:
            t0 = T.word("L03", word)
            x, _ = modem_led(MID, 1000, MW, name)
            fade(c, t, t0, e - DIM, lambda c, x=x, label=label, t0=t0:
                 pop_tag(c, t, t0, x, 1250, label, PURPLE if name != "LOS" else RED, align="c"))
            if t >= t0:
                a = out_expo(prog(t, t0, 0.4)) * (1 - prog(t, e - DIM, DIM))
                c.line(x, 1176, x, 1176 + 40 * a, c.theme("faint", "d_line"), 3, a)
    v.add(s, e, draw, z=20)
    v.sfx("pop", L1.start + 0.2, 0.5)
    v.sfx("whoosh", L2.start + 0.1, 0.6)
    for w in ("lampu", "tempat", "baca"):
        v.sfx("pop", T.word("L03", w))


# ── 00 · LOS: the light's road, the cut, the cable behind the modem ───────
def los(v, T, s, e):
    ch = v.chapter(0, "LOS", s, e)
    L4, L5, L6, L7, L8 = (T[k] for k in ("L04", "L05", "L06", "L07", "L08"))
    t_flow = T.word("L04", "cahaya")
    t_pole = T.word("L05", "tiang")
    t_cut = T.word("L06", "nyampe") - 0.15
    t_mini = t_cut + 0.55
    t_kink = T.word("L07", "ketekuk") - 0.25
    t_safe = L8.start + 0.1
    t_no = T.word("L08", "ngefek")
    sheet_out = L8.start + 0.7
    hs = _ink(T, [("Internetmu itu\n*cahaya*.", "L04"), ("Cahayanya\n*nggak nyampe*.", "L06"),
                  ("Cek kabel\n*kecil* dulu.", "L07"), ("Putusnya\ndi *luar*.", "L08")], e - DIM)
    cx_, cy_ = route_point(ROUTE, CUT_AT)
    MX, MY = X + 185, 1330                                       # the mini modem that reports the cut

    def scene(c, t):
        a = _alive(t, s + 0.1, e)
        if a <= 0.002:
            return
        with c.group(a), drifting(c, t, s, e, (MID, 1000)):
            fiber_route(c, ROUTE, t, p_draw=in_out_cubic(prog(t, L4.start, 1.6)), flow=prog(t, t_flow, 0.6),
                        cut=out_expo(prog(t, t_cut, 0.3)), cut_at=CUT_AT, house_light=1.0,
                        labels=t >= L5.start, mark=prog(t, t_pole, 0.4) * (1 - prog(t, L6.start, 0.4)))
            if t >= t_mini:
                m = out_expo(prog(t, t_mini, 0.5))
                connector(c, cx_ - 10, cy_ + 20, MX + 120, MY - 70, prog(t, t_mini, 0.6), C["accent"], 3)
                with c.at(0, 30 * (1 - m)):
                    modem(c, MX, MY, 300, t, INTRO_L, alpha=m, antenna=False, labels=False)
                note(c, MX - 70, MY + 120, "LOS nyala", prog(t, t_mini + 0.3, 0.5), size=40)
        if t >= L8.start:
            fade(c, t, L8.start, e - DIM, lambda c: tag(c, X, 1470, "restart · restart · restart", RED))
            strike(c, t, t_no, X + 8, X + 392, 1488, alpha=1 - prog(t, e - DIM, DIM))
    v.add(s, e, scene)

    def cable(c, x, y, w, h):
        c.text(x + 44, y + 78, "DI BELAKANG MODEM", F["mono_bold"], 22, C["muted"], 1, 0.16)
        bend = in_out_cubic(prog(t_now[0], t_kink, 0.6)) * (1 - in_out_cubic(prog(t_now[0], t_safe, 0.4)))
        modem(c, x + w - 220, y + 250, 300, t_now[0], INTRO_L, antenna=False, labels=False)
        kx, ky = patchcord(c, x + 130, y + 280, x + w - 320, y + 330, bend=bend)
        c.text(x + 80, y + 380, "roset dinding", F["mono"], 20, C["ink2"], 1)
        note(c, x + 300, y + h - 60, "jangan sampai ketekuk", prog(t_now[0], t_kink + 0.3, 0.5),
             arrow_to=(kx - 10, ky + 20), size=40)
        ok = out_back(prog(t_now[0], t_safe + 0.2, 0.4))
        if ok > 0:
            check_badge(c, kx + 70, ky - 30, 30, ok)
    t_now = [0.0]

    def sheet_layer(c, t):
        t_now[0] = t
        sheet(c, t, L7.start - 0.1, sheet_out, (X, 820, CW, 560), cable)
    v.add(L7.start - 0.1, sheet_out + 0.6, sheet_layer, z=10)

    def head(c, t):
        kicker(c, t, s + 0.2, e - OUT, "00 · LAMPU LOS", ch.color)
        _heads(c, t, hs)
    v.add(s, e, head, z=20)
    v.camera.focus(t_cut - 0.3, (cx_ - 220, cy_ - 260, 440, 520), zoom=1.12, dur=0.9)
    v.camera.reset(L7.start - 0.35, dur=0.8)
    v.sfx("pop", L5.start, 0.5)
    v.sfx("pop", t_pole, 0.5)
    v.sfx("thud", t_cut)
    v.sfx("pop", t_mini)
    v.sfx("whoosh", L7.start - 0.1, 0.7)
    v.sfx("tick", t_kink + 0.3)
    v.sfx("chime", t_safe + 0.2, 0.6)
    v.sfx("pop", L8.start, 0.5)
    v.sfx("click", t_no, 0.7)


# ── 01 · PON: the light arrived — the modem is introducing itself ─────────
def pon(v, T, s, e):
    ch = v.chapter(1, "PON", s, e)
    L9, L10, L11 = T["L09"], T["L10"], T["L11"]
    t_hi, t_reg = T.word("L10", "kenalan"), T.word("L10", "didaftarin")
    hs = _ink(T, [("Udah *sampai*.", "L09"), ("Lagi *kenalan*.", "L10"), ("Tunggu, baru *lapor*.", "L11")], e - DIM)
    pill = Morph((X, 1050, 340, 68), r=34)
    pill.to(L11.start, (X, 1050, CW, 380), r=36)

    def content(c, box, k):
        x, y, w, h = box
        if k == 0:
            c.circle(x + 34, y + h / 2, 9, OK, 0.3 + 0.7 * (0.5 + 0.5 * math.cos(13.8 * t_now[0])))
            c.text(x + 58, y + h / 2 + 9, "PON · kedip", F["ui_semi"], 28, C["ink"])
            return
        c.text(x + 48, y + 86, "TUNGGU", F["mono_bold"], 22, C["muted"], 1, 0.18)
        c.text(x + 46, y + 186, "beberapa menit.", F["display"], 78, C["ink"], 1, -0.05)
        c.circle(x + 62, y + 286, 12, RED)
        c.text(x + 92, y + 296, "Kedip terus? Lapor ke ISP.", F["ui_semi"], 32, C["ink2"])
    t_now = [0.0]

    def draw(c, t):
        t_now[0] = t
        kicker(c, t, s + 0.2, e - OUT, "01 · LAMPU PON", ch.color)
        _heads(c, t, hs)
        a = _alive(t, L9.start + 0.3, e)
        if a > 0.002:
            pill.draw(c, t, C["card"], content=content, alpha=a)
        gone = 1 - prog(t, L11.start - 0.35, 0.3)
        bubble(c, MID + 330, 1300, "Halo, aku modem rumah.", out_back(prog(t, t_hi, 0.4)) * gone, align="r")
        bubble(c, X + 40, 1420, "Bentar, aku daftarin dulu.", out_back(prog(t, t_reg, 0.4)) * gone, color=PURPLE)
    v.add(s, e, draw, z=20)
    v.camera.focus(L9.start, (MID - 220, 760, 440, 200), zoom=1.06, dur=0.9)
    v.camera.reset(L10.start, dur=0.8)
    v.sfx("whoosh", s + 0.1, 0.6)
    v.sfx("pop", L9.start + 0.3)
    v.sfx("send", t_hi)
    v.sfx("send", t_reg)
    v.sfx("whoosh", L11.start, 0.6)


# ── 02 · INTERNET: cable fine, the door is the account → restart ──────────
def internet(v, T, s, e, t_rs):
    ch = v.chapter(2, "INTERNET", s, e)
    L12, L13, L14 = T["L12"], T["L13"], T["L14"]
    t_tap = T.word("L13", "akunmu")
    t_login, t_bill = T.word("L13", "login"), T.word("L13", "tagihan")
    t_ok = T.word("L14", "ngefek")
    hs = _ink(T, [("Kabelnya *aman*.", "L12"), ("Yang ketutup: *akunmu*.", "L13"),
                  ("Restart *kadang* ngefek.", "L14")], e - DIM)
    BX, BY, BW, BH = X, 1380, 280, 84

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · LAMPU INTERNET", ch.color)
        _heads(c, t, hs)
        a = _alive(t, L12.start + 0.4, e)
        if a > 0.002:
            id_card(c, X + 190, 1150, 300, tap=prog(t, t_tap - 0.4, 0.6), ok=prog(t, t_ok, 0.4), color=PURPLE,
                    alpha=a)
            gone = 1 - prog(t, L14.start - 0.3, 0.3)
            fade(c, t, t_login, None, lambda c: pop_tag(c, t, t_login, X, BY + 20, "login gagal", RED), d_in=0.2)
            fade(c, t, t_bill, None, lambda c: pop_tag(c, t, t_bill, X + 250, BY + 20, "tagihan telat", RED), d_in=0.2)
            if gone < 1:
                c.src(c.theme("bg", "d_bg"), (1 - gone) * a)
                c.ctx.rectangle(X, BY, CW, 100)
                c.ctx.fill()
            if t >= L14.start:
                b = out_expo(prog(t, L14.start, 0.4)) * a
                with c.at(0, 0, press(t, t_rs), origin=(BX + BW / 2, BY + BH / 2)):
                    c.fill_rrect(BX, BY, BW, BH, BH / 2, C["accent"], b)
                    c.text(BX + BW / 2, BY + 55, "Restart", F["ui_semi"], 34, C["card"], b, align="c")
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.08, y=960, dur=0.01).key(s + 0.1, zoom=1.0, y=960, dur=2.2)
    v.sfx("whoosh", s + 0.1, 0.6)
    v.sfx("click", t_tap + 0.2, 0.6)
    v.sfx("thud", t_login, 0.6)
    v.sfx("pop", t_bill)
    v.sfx("pop", L14.start, 0.5)


# ── RECAP (dark): check from the closest place outward → read the lamps → say "LOS merah" ─
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L15, L16, L17 = T["L15"], T["L16"], T["L17"]
    t0, t1 = T.word("L15", "cek"), T.word("L15", "dekat")
    t_read = T.word("L16", "baca")
    t_red = L17.start + 0.2
    t_pill = T.word("L17", "merah")
    hs = _ink(T, [("Cek dari yang\npaling *dekat*.", "L15"), ("Tinggal *baca*\nlampunya.", "L16"),
                  ("Lapor? Sebut\n*lampunya*.", "L17")], e - DIM, style="headline_dark")
    box = (X + 24, 620, CW - 84, 680)
    stops = [(0.985, "1"), (0.72, "2"), (ODP_F, "3"), (0.02, "4")]       # house → cable → ODP → ISP
    step = max(0.35, (t1 + 0.6 - t0) / len(stops))

    def draw(c, t):
        _heads(c, t, hs)
        a = out_expo(prog(t, s + 0.2, 0.5)) * (1 - in_out_cubic(prog(t, L16.start - 0.3, 0.4)))
        if a > 0.002:
            with c.group(a):
                fiber_route(c, box, t, flow=1.0, cut=1.0, cut_at=CUT_AT, house_light=1.0, labels=False)
                for i, (f, num) in enumerate(stops):
                    p = out_back(prog(t, t0 + i * step, 0.35))
                    if p > 0:
                        px, py = route_point(box, f)
                        py -= 52 if i == 0 else 0
                        with c.at(0, 0, p, origin=(px, py)):
                            c.circle(px, py, 26, C["d_accent"])
                            c.text(px, py + 10, num, F["mono_bold"], 26, C["d_ink"], 1, align="c")
        m = out_expo(prog(t, L16.start - 0.1, 0.6)) * (1 - in_out_cubic(prog(t, e - DIM, DIM)))
        if m > 0.002:
            hop = int(max(0.0, t - t_read) / 0.3)
            name = LEDS[hop] if 0 <= t - t_read and hop < len(LEDS) else None
            lights = ALL_OK if t < t_red else INTRO_L
            if t >= t_red:
                name = "LOS"
            with c.at(0, 40 * (1 - m)):
                modem(c, MID, 960, MW, t, lights, focus=name, focus_p=1.0 if name else 0.0, alpha=m)
            if t >= t_pill:
                pa = out_back(prog(t, t_pill, 0.4)) * (1 - prog(t, e - DIM, DIM))
                with c.at(0, 0, max(0.01, pa), origin=(X, 1290)):
                    pw, ph = word_pill(c, X, 1240, "LOS merah.", RED, size=96, alpha=min(1, pa))
                fade(c, t, t_pill + 0.5, e - DIM, lambda c: c.text(X, 1460, "= masalah kabel. Bukan settingan.",
                                                                   F["ui_semi"], 34, C["d_muted"]))
    v.add(s, e, draw, z=20)
    v.camera.key(L16.start, zoom=1.04, y=1000, dur=2.5)
    v.camera.reset(L17.start, dur=0.8)
    v.sfx("whoosh_dark", s)
    for i in range(len(stops)):
        v.sfx("tick", t0 + i * step)
    v.sfx("chime", t0 + len(stops) * step, 0.6)
    for k in range(len(LEDS)):
        v.sfx("tick", t_read + k * 0.3, 0.5)
    v.sfx("thud", t_pill)
