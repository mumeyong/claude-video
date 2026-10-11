"""Bongkar WiFi Rumah EP 03 — WiFi lemot pas hujan: mitos atau beneran? QUICK, classic + Apple craft. See PLAN.md.

Metaphor: a leaking gutter (talang bocor). One cut-away house in the rain lives in a viewport card: inside, the
router and the phone stay dry; outside, the drop cable hangs from the ODP box on the pole and runs along the eave
like a gutter. The rain is never the problem — one joint that drips is.
Signature: the rain stops, ONE drop falls (INTRO) → slides under the ODP lid and drips onto the splice, the light in
the fiber goes weak (01) → falls into the gap (RECAP).
Motion: rise headlines · Rig persistent scene (the "camera" inside the card) + depth_swap into the ODP + sheet for
the checklist · quiet exits · hero/silk springs · global camera only dollies in holds + cuts.
Sound: styled score lofi G dreamy 84 + glass SFX kit (EP 02 marimba/wood, ai-butuh-listrik marimba/soft).
"""
import math

from engine import Video, tokens as tk
from engine.ease import clamp, prog, mix, curve
from engine.components import (kicker, fade, pop_tag, tag_center, check_badge, note, strike, brand_intro,
                               series_bumper, standard_outro, cover, Rig, arrive, follow, rise, depth_swap, sheet,
                               dolly, cut, ios_at, heads, draw_heads, dimension, airwaves, modem, hujan, tetes,
                               odp_box, rumah_potong, rumah_geo, along, HUJAN_TEAL as TEAL)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                             # long brand sting (version 2): voice starts under its wipe
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · MITOS", "01 · SATU TETES", "02 · YANG BISA KAMU LAKUIN", "RECAP", "OUTRO"]
APPLE_OUT, APPLE_IO = curve("apple_out"), curve("apple_in_out")

# ── the viewport card + the rainy scene inside it (world px, framed by a Rig) ──────────────────────────────────────
VP = (X, 600, CW, 860)
VR = L["radius_bento"]
VC = (MID, VP[1] + VP[3] / 2)
SC = (X + 30, 1400, CW - 60, 700)           # rumah_potong(x, base_y, w, h)
G = rumah_geo(*SC)
SKY = mix(C["bg"], C["muted"], 0.22)
P_PHONE = (236, 1226)                       # back window + phone on the sofa
P_ALL = (SC[0] + SC[2] / 2, SC[1] - SC[3] / 2)
P_IN = (470, 1220)                          # the room: phone ← router | wall | rain
P_OUT = (690, 1010)                         # eave, drop cable, pole, ODP
P_DROP = along(G["cable"][:13], 0.72)[:2]   # where the INTRO drop lands on the hanging cable
ODP_C, ODP_W = (MID, 1010), 360             # the ODP close-up


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words oddly)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


def _frame(P, s):
    """Rig state that puts world point P at the card centre at scale s."""
    return dict(x=VC[0] - s * (P[0] - VC[0]), y=VC[1] - s * (P[1] - VC[1]), s=s)


def _screen(st, P):
    return st["x"] + st["s"] * (P[0] - VC[0]), st["y"] + st["s"] * (P[1] - VC[1])


def _fall(u):
    """Gravity: distance fraction after time fraction u."""
    return clamp(u) ** 2


def build(project):
    T = project.timing
    v = Video(duration=T["L21"].end + TAIL, bpm=84, beat_offset=0.0, series="BONGKAR WIFI RUMAH · EP 03")
    brand_intro(v, version=2)
    v.music = dict(style="lofi", key="G", mood="dreamy")     # EP 02 marimba A bright, ai-butuh-listrik marimba F warm
    v.sfx_kit = "glass"
    v.cover = lambda c: cover(c, "WiFi *takut*\nhujan?", kicker="BONGKAR WIFI RUMAH · EP 03", color=TEAL,
                              badge="EP 03", tags=["ODP", "fiber", "satu tetes"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    t_tetes = _w(T, "L03", "tetes", 0.9)
    bump0 = max(t_tetes + 0.9, T["L03"].end + 0.1)
    bump1 = bump0 + 1.35
    b[1] = max(b[1], bump0 + 0.45)                           # chapter switch hidden under the bumper
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(3):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 3, "Lemot pas hujan", TEAL,
                                                   title=("BONGKAR", "WIFI RUMAH")), z=100)
    v.sfx("whoosh", bump0)
    scene(v, T, b, bump0, bump1)
    intro(v, T, b[0], b[1])
    mitos(v, T, b[1], b[2], bump1)
    satu_tetes(v, T, b[2], b[3])
    lakuin(v, T, b[3], b[4])
    recap(v, T, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L21", TEAL,
                   teaser=dict(kicker="BONGKAR WIFI RUMAH · EP 04", title="Restart router.",
                               sub="Beneran ngefek, atau cuma kebiasaan?"))
    v.cover_t = t_tetes + 0.6
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w * 0.42, h / 1.9)
    g = odp_box(c, x + w / 2, y + h * 0.5, s, 0.0, lid=0.7, wet=0.6, glow=0.5)
    tetes(c, g["gap"][0], g["gap"][1] + s * 0.12, s * 0.16)


def _phone_screen(t):
    """The video that keeps buffering: dark screen, a frame, a spinner (world px, tiny phone)."""
    def draw(c, sx, sy, sw, sh):
        c.fill_rrect(sx, sy, sw, sh, 0, C["ink"])
        c.fill_rrect(sx, sy + sh * 0.3, sw, sh * 0.34, 0, C["ink2"])
        cx, cy, r = sx + sw / 2, sy + sh * 0.47, sw * 0.17
        ctx = c.ctx
        ctx.new_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        c.src(C["muted"], 0.6)
        ctx.set_line_width(sw * 0.05)
        ctx.stroke()
        a = t * 5.5
        ctx.new_path()
        ctx.arc(cx, cy, r, a, a + 1.7)
        c.src(C["card"])
        ctx.set_line_cap(1)
        ctx.stroke()
    return draw


# ── the viewport: rainy house (INTRO → 00 → 01), ODP close-up (01), modem (L13), held under the sheet (02) ────────
def scene(v, T, b, bump0, bump1):
    L1s = T["L01"].start
    t_takut = arrive(_w(T, "L02", "takut", 0.6), "hero")
    t_stop = _w(T, "L03", "yang", 0.45) - 0.45
    t_land = _w(T, "L03", "tetes", 0.9) + 0.05
    t_in00 = bump0 + 0.45
    t_diredam = _w(T, "L04", "diredam", 0.6)
    t_waves = (T["L04"].start + 0.1, arrive(t_diredam))
    t_dalam, t_luar5 = _w(T, "L05", "dalam", 0.4), _w(T, "L05", "luar", 0.9)
    t_meter = _w(T, "L06", "meter", 0.4)
    t_out = arrive(_w(T, "L07", "luar", 0.85), "hero")
    t_fiber = _w(T, "L08", "fiber", 0.5)
    t_odp = _w(T, "L09", "ODP", 0.7) - 0.55                      # depth_swap lands on "ODP"
    t_netes, t_samb = _w(T, "L10", "netes", 0.7), _w(T, "L10", "sambungan", 0.9)
    t_reng, t_retak = _w(T, "L11", "renggang", 0.3), _w(T, "L11", "retak", 0.6)
    t_masuk = _w(T, "L11", "masuk", 0.9)
    t_lemah = _w(T, "L12", "lemah", 0.6)
    t_modem = _w(T, "L13", "modem", 0.02)
    t_putus = _w(T, "L13", "putus-nyambung", 0.7)
    end = b[4]

    rig = Rig(a=0.0, **_frame(P_PHONE, 4.2))                     # full-bleed shrink onto the phone
    rig.to(L1s - 0.25, preset="silk", a=1.0, **_frame(P_PHONE, 3.0))
    rig.to(t_takut, preset="silk", **_frame(P_ALL, 1.0))
    rig.to(t_in00, preset="silk", dur=0.55, **_frame(P_IN, 1.5))  # under the bumper
    rig.to(t_out, preset="silk", **_frame(P_OUT, 1.5))

    def rain(t):
        if t < bump0:
            return 1.0 - APPLE_OUT(prog(t, t_stop, 0.6))
        return 0.75

    def light(t):
        return APPLE_OUT(prog(t, t_fiber - 0.2, 0.8))

    def world(c, t):
        rumah_potong(c, *SC, t, light=light(t), screen=_phone_screen(t), rain=rain(t))
        if t_land - 0.8 < t < bump0 + 0.4:                       # the one drop (INTRO)
            u = prog(t, t_land - 0.55, 0.55)
            y0 = VC[1] + (VP[1] - 40 - rig.state(t)["y"]) / rig.state(t)["s"]
            y = y0 + (P_DROP[1] + 9 - y0) * _fall(u)
            tetes(c, P_DROP[0], y, 26, stretch=0.6 * (1 - prog(t, t_land, 0.15)) if u > 0 else 0,
                  alpha=clamp(prog(t, t_land - 0.75, 0.2)))
        r = G["router"]
        for k, tw in enumerate(t_waves):                         # WiFi bursts: strong inside, damped outside
            p = prog(t, tw, 1.6)
            if 0 < p < 1:
                with c.clip(SC[0], SC[1] - SC[3], G["wall_x"] - SC[0], SC[3]):
                    airwaves(c, r[0] - 20, r[1] - 10, p, 270, C["accent"], a0=math.pi - 0.45, a1=math.pi + 0.45)
                    airwaves(c, r[0] + 20, r[1] - 10, p, 250, C["accent"], a0=-0.45, a1=0.45)
                with c.clip(G["wall_x"], SC[1] - SC[3], SC[2], SC[3]):
                    airwaves(c, r[0] + 20, r[1] - 10, p, 250, C["accent"], a0=-0.45, a1=0.45,
                             alpha=0.22 if k else 0.5)

    def rig_world(c, t):
        with rig.place(c, t):
            with c.at(-VC[0], -VC[1]):
                world(c, t)

    def lid(t):
        return clamp(ios_at(t, arrive(t_reng), "smooth"))

    def wet(t):
        return APPLE_OUT(prog(t, t_masuk + 0.35, 2.2))

    def glow(t):
        return 1.0 - 0.7 * APPLE_OUT(prog(t, arrive(t_lemah), 0.9))

    def odp_view(c, t):
        hujan(c, VP, t, 0.55, n=70, length=70, width=3.5, seed=3)
        g = odp_box(c, ODP_C[0], ODP_C[1], ODP_W, t, lid=lid(t), wet=wet(t), glow=glow(t), alpha=1.0)
        cx0, cy0, cw_, ch_ = g["cap"]
        gx, gy = g["gap"]
        if t_netes - 0.3 < t < t_masuk + 0.6:                    # the drop: along the lid edge → gap → splice
            ts = arrive(t_samb, "smooth", 0.95)
            u = APPLE_IO(prog(t, ts - 0.9, 1.0))
            x = cx0 + cw_ * 0.18 + (gx - cx0 - cw_ * 0.18) * u
            y = cy0 + ch_ + 16 + (gy + 16 - cy0 - ch_ - 16) * u
            fu = prog(t, t_masuk - 0.15, 0.5)
            sy = g["splice"][1] - 18
            y += (sy - y) * _fall(fu)
            a = clamp(prog(t, t_netes - 0.3, 0.3)) * (1 - prog(t, t_masuk + 0.3, 0.2))
            tetes(c, x, y, 30, stretch=0.6 if 0 < fu < 1 else 0.0, alpha=a)
        return g

    def modem_view(c, t):
        modem(c, MID, 1010, 660, t, dict(POWER="g", PON="gb", LOS="", INTERNET="gb", WLAN="g"))
        fade(c, t, follow(t_putus, 1), None,
             lambda c: tag_center(c, MID, 1290, "PON + INTERNET kedip", TEAL))

    def draw(c, t):
        a = rig.state(t)["a"] if t < t_odp else 1.0
        a *= 1 - prog(t, end - OUT, OUT)
        if a <= 0.002:
            return
        with c.group(a):
            c.card(*VP, r=VR)
            with c.clip(*VP, VR):
                c.fill_rrect(*VP, VR, SKY)
                hujan(c, VP, t, rain(t) if t < t_odp else 0.0)
                if t < t_odp:
                    rig_world(c, t)
                elif t < t_modem:
                    depth_swap(c, t, t_odp, VP, lambda c: rig_world(c, t), lambda c: odp_view(c, t))
                else:
                    modem_view(c, t)
    v.add(0.0, end, draw, z=10)
    v.sfx("whoosh", L1s - 0.25, 0.4)
    v.sfx("whoosh", t_takut, 0.5)
    v.sfx("pop", t_land, 0.8)
    v.sfx("whoosh", t_out, 0.5)
    v.sfx("tick", t_fiber, 0.4)
    v.sfx("whoosh", t_odp, 0.5)
    v.sfx("pop", t_samb, 0.6)
    v.sfx("click", arrive(t_reng), 0.6)
    v.sfx("pop", t_masuk + 0.35, 0.7)
    v.sfx("tick", t_lemah, 0.5)
    v.sfx("click", t_modem, 0.7)
    dolly(v, T["L02"].end + 0.1, t_stop - 0.1, y=VC[1])
    cut(v, t_stop)
    dolly(v, arrive(t_meter) + 1.0, t_out - 0.1, y=VC[1])
    cut(v, t_out)
    dolly(v, arrive(t_lemah) + 1.0, t_modem - 0.05, y=VC[1])
    cut(v, t_modem)
    return dict(rig=rig, t_dalam=t_dalam, t_luar5=t_luar5, t_meter=t_meter, t_out=t_out)


# ── INTRO: buffering phone → the house in the rain → the rain stops, one drop ────────────────────────────────────
def intro(v, T, s, e):
    hs = heads(T, [("Video *muter*\nterus.", "L01"), ("WiFi takut\n*hujan*?", "L02"),
                   ("Bukan hujannya.\nSatu *tetes*.", "L03")], e - OUT)

    def draw(c, t):
        kicker(c, t, T["L01"].start, e - OUT, "JAM 16.00 · HUJAN DERAS", TEAL)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
    v.add(s, e, draw, z=20)


# ── 00 · MITOS: inside dry, outside wet — WiFi is damped by water, but the rain isn't in the room ─────────────────
def mitos(v, T, s, e, bump1):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("WiFi bisa\n*diredam* air.", "L04"), ("Router di *dalam*.\nHujan di luar.", "L05"),
                   ("Cuma *beberapa*\nmeter.", "L06"), ("Cari di *luar*.", "L07")], e - OUT)
    h0, a0, b0 = hs[0]
    hs[0] = (h0, max(a0, bump1 - 0.25), b0)                      # first headline appears as the bumper leaves
    t_dalam = arrive(_w(T, "L05", "dalam", 0.4), "snappy")
    t_luar = arrive(_w(T, "L05", "luar", 0.9), "snappy")
    t_meter = arrive(_w(T, "L06", "meter", 0.4))
    t_off = arrive(_w(T, "L07", "luar", 0.85), "hero") - 0.05
    s_in = 1.5
    ph = (VC[0] - s_in * (P_IN[0] - G["phone"][0]), VC[1])
    ro = (VC[0] - s_in * (P_IN[0] - G["router"][0]), VC[1])
    y_dim = VC[1] + s_in * (SC[1] + 30 - P_IN[1])          # under the floor line

    def draw(c, t):
        kicker(c, t, max(s + 0.2, bump1 - 0.3), e - OUT, "00 · MITOS", col)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
        fade(c, t, t_dalam, t_off, lambda c: pop_tag(c, t, t_dalam, X + 70, 790, "dalam · kering", TEAL))
        fade(c, t, t_luar, t_off, lambda c: pop_tag(c, t, t_luar, X + CW - 30, 790, "luar · hujan", TEAL, align="r"))
        fade(c, t, t_meter, t_off, lambda c: dimension(c, ph[0], y_dim, ro[0], y_dim, "beberapa meter",
                                                        APPLE_OUT(prog(t, t_meter, 0.7)), color=TEAL))
    v.add(s, e, draw, z=20)
    v.sfx("pop", t_dalam, 0.5)
    v.sfx("pop", t_luar, 0.5)
    v.sfx("tick", t_meter, 0.5)


# ── 01 · SATU TETES: fiber from the pole → the ODP close-up → the drop gets in → weak light → the modem blinks ────
def satu_tetes(v, T, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("Masuk lewat\n*fiber*.", "L08"), ("Kotak kecil:\n*ODP*.", "L09"), ("Kayak talang\n*bocor*.", "L10"),
                   ("Ada *celah*,\nair masuk.", "L11"), ("Cahayanya\n*melemah*.", "L12"),
                   ("Nyala, tapi\n*putus-nyambung*.", "L13")], e - OUT)
    t_note = follow(_w(T, "L10", "bocor", 0.3) + 0.4, 1)
    t_reng = arrive(_w(T, "L11", "renggang", 0.3), "snappy")
    t_retak = arrive(_w(T, "L11", "retak", 0.6), "snappy")
    t_lemah = arrive(_w(T, "L12", "lemah", 0.6))
    t_note2 = follow(t_lemah + 0.9, 1)
    t_modem = _w(T, "L13", "modem", 0.02)
    sp = (ODP_C[0], ODP_C[1] - ODP_W * 0.65 + ODP_W * 1.3 * 0.13 + 0.66 * ODP_W * 1.3 * (0.1 + 0.31))

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "01 · SATU TETES", col)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
        fade(c, t, t_note, t_reng - 0.2,
             lambda c: note(c, X + 40, 690, "talang bocor", 1.0, arrow_to=(ODP_C[0] + 120, ODP_C[1] - 220)))
        fade(c, t, t_reng, T["L12"].start - 0.1, lambda c: pop_tag(c, t, t_reng, X + 40, 760, "tutup renggang", TEAL))
        fade(c, t, t_retak, T["L12"].start - 0.1, lambda c: pop_tag(c, t, t_retak, X + 40, 1340, "kabel retak", TEAL))
        fade(c, t, t_note2, t_modem - 0.05,
             lambda c: note(c, X + 40, 1360, "sambungan basah", 1.0, arrow_to=(sp[0] - 70, sp[1] + 20)))
    v.add(s, e, draw, z=20)
    v.sfx("pop", t_reng, 0.4)
    v.sfx("pop", t_retak, 0.4)


# ── 02 · YANG BISA KAMU LAKUIN: a sheet with three rows, each ticks on its line ────────────────────────────────────
def lakuin(v, T, s, e):
    col = tk.CHAPTER[2][0]
    hs = heads(T, [("Cek *kabelnya*.", "L14"), ("*Catat* jamnya.", "L15"), ("Bilang\n*tiap hujan*.", "L16"),
                   ("Biar dicek\ndi *luar*.", "L17")], e - OUT)
    SH = (X, 640, CW, 800)
    t_sheet = s + 0.15
    rows = [("1", "Kabel tiang → rumah", "kendor? kena tetesan talang?", arrive(_w(T, "L14", "kabel", 0.2)),
             _w(T, "L14", "talang", 0.95) + 0.3),
            ("2", "Catat jam + foto lampu", None, arrive(_w(T, "L15", "catat", 0.3)),
             _w(T, "L15", "modemnya", 0.95) + 0.2),
            ("3", "Lapor ke ISP", "“lemot tiap hujan”", arrive(_w(T, "L16", "lapor", 0.25)),
             _w(T, "L16", "hujan", 0.95) + 0.2)]
    t_luar = arrive(_w(T, "L17", "luar", 0.55))
    t_restart = _w(T, "L17", "restart", 0.9)

    def content(c, t, x, y, w, h):
        c.text(x + 56, y + 84, "CEK SENDIRI · 3 LANGKAH", F["mono_med"], 22, C["muted"], 1, 0.16)
        for i, (num, title, sub, t_in, t_tick) in enumerate(rows):
            ry = y + 120 + i * 205

            def row(c, ry=ry, num=num, title=title, sub=sub, i=i, t_tick=t_tick):
                c.circle(x + 86, ry + 62, 30, TEAL)
                c.text(x + 86, ry + 74, num, F["display"], 32, C["card"], 1, align="c")
                c.text(x + 142, ry + 76, title, F["ui_semi"], 42, C["ink"], 1, -0.01)
                if sub:
                    c.text(x + 142, ry + 128, sub, F["mono"], 25, C["ink2"], 1)
                else:
                    c.text(x + 142, ry + 132, "16.04 · lemot lagi", F["serif"], 40, C["accent"], 1)
                check_badge(c, x + w - 76, ry + 62, 26, clamp(ios_at(t, t_tick, "snappy")))
                if i < 2:
                    c.line(x + 56, ry + 182, x + w - 56, ry + 182, C["line"], 2)
            rise(c, t, t_in, None, (x, ry, w, 190), row)
        ry = y + 120 + 2 * 205
        fade(c, t, t_luar, None, lambda c: c.text(x + 142, ry + 180, "→ teknisi cek di luar", F["ui_semi"], 30, TEAL))
        fade(c, t, t_luar, None, lambda c: c.text(x + w - 56, ry + 180, "restart router", F["mono"], 24, C["muted"],
                                                   align="r"))
        rw = c.measure("restart router", F["mono"], 24)[0]
        strike(c, t, t_restart, x + w - 56 - rw - 6, x + w - 50, ry + 172, width=4)

    def draw(c, t):
        sheet(c, t, t_sheet, e - OUT, SH, lambda c, x, y, w, h: content(c, t, x, y, w, h))
        kicker(c, t, s + 0.2, e - OUT, "02 · YANG BISA KAMU LAKUIN", col)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
    v.add(s, e, draw, z=30)
    v.sfx("whoosh", t_sheet, 0.5)
    for _, _, _, t_in, t_tick in rows:
        v.sfx("pop", t_in, 0.4)
        v.sfx("chime", t_tick, 0.5)
    v.sfx("tick", t_restart, 0.5)


# ── RECAP (dark): the same drop, held over a seam — "basahnya di mana?" — then it falls into the gap ──────────────
def recap(v, T, s, e):
    hs = heads(T, [("*Basahnya*\ndi mana?", "L18"), ("Hujan cuma\n*pemicu*.", "L19")], e - OUT, style="headline_dark")
    Y0, YG, GAP = 960, 1250, 34
    t_pemicu = _w(T, "L19", "pemicu", 0.4)
    t_fall = t_pemicu - 0.4
    t_celah = follow(_w(T, "L19", "celahnya", 0.6), 1)

    def drop(c, t):
        u = prog(t, t_fall, 0.5)
        y = Y0 + (YG - 20 - Y0) * _fall(u)
        tetes(c, MID, y, 200, stretch=0.5 if 0 < u < 1 else 0.0, alpha=1 - prog(t, t_fall + 0.42, 0.12))

    def seam(c, t):
        for x0, x1 in ((X + 60, MID - GAP / 2), (MID + GAP / 2, X + CW - 60)):
            c.fill_rrect(x0, YG, x1 - x0, 44, 12, C["d_card"])
            c.stroke_rrect(x0, YG, x1 - x0, 44, 12, C["d_line"], 2)
        rp = prog(t, t_fall + 0.5, 0.7)
        if 0 < rp < 1:
            ctx = c.ctx
            ctx.new_path()
            ctx.save()
            ctx.translate(MID, YG + 4)
            ctx.scale(1.0, 0.3)
            ctx.arc(0, 0, 30 + 170 * APPLE_OUT(rp), 0, 2 * math.pi)
            ctx.restore()
            c.src(TEAL, 0.8 * (1 - rp))
            ctx.set_line_width(4)
            ctx.stroke()
        hl = APPLE_OUT(prog(t, t_celah, 0.6))
        if hl > 0:
            c.fill_rrect(MID - GAP / 2 - 6, YG + 54, GAP + 12, 8, 4, TEAL, hl)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", TEAL)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
        rise(c, t, s + 0.25, e - OUT, (X, YG, CW, 60), lambda c: seam(c, t))
        rise(c, t, follow(s + 0.25, 1), e - OUT, (MID - 120, Y0 - 160, 240, 260), lambda c: drop(c, t), preset="hero")
        fade(c, t, t_celah, e - OUT, lambda c: note(c, X + 40, 1440, "celahnya di sini", 1.0,
                                                     arrow_to=(MID - 30, YG + 70), color=C["d_accent"]))
    v.add(s, e, draw, z=20)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    v.sfx("pop", t_fall + 0.5, 0.7)
    dolly(v, follow(s + 0.25, 1) + 1.4, t_fall - 0.1, y=1100)
    cut(v, e)
