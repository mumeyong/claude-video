"""Bongkar Arsitektur EP06 — Project 360: satu nasabah, satu layar. See IDENTITY.md / TREATMENT.md.

Metaphor: files scattered across counters → one stopmap on the CS desk, guarded in layers. Signature move: sheets
fly in from different counters into one stopmap, which shuts "klik". Color: purple. Hook: cold open at the CS desk.
No numbers, no real customer data (names censored).
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp
from engine.components import (Headline, kicker, appear, fade, icons, note, stamp, strike, series_bumper, lembar,
                               stopmap, meja_cs, bubble, profile_360, lapis, id_card, visitor, walk_path,
                               fade_ends, cover, SOURCES, BERKAS_PURPLE as PURPLE, check_badge, pop_tag,
                               series_outro)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · MASALAH", "01 · KEPUTUSAN", "02 · DIAGRAM", "03 · HASIL", "RECAP", "OUTRO"]
OK = C["ok"]
RED = C["rec"]
SRC = ["tabungan", "asuransi", "kredit", "sekuritas"]
COL = [SOURCES[k] for k in SRC]
ASK = "NIK-nya berapa, Pak?"


def build(project):
    T = project.timing
    v = Video(duration=T["L25"].end + TAIL, bpm=128, beat_offset=0.0, series="BONGKAR ARSITEKTUR · EP 06")
    v.cover_t = T.word("L04", "layar") + 0.6
    v.music = dict(key="G", mood="tense")            # generated score: cold open, sensitive data
    v.cover = lambda c: cover(c, "Satu nasabah,\n*satu layar*.", kicker="BONGKAR ARSITEKTUR · EP 06", color=PURPLE,
                              badge="EP 06", tags=["Project 360", "real-time", "WAF · VPN · IDaaS"],
                              hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    b["00 · MASALAH"] = T["L04"].end + 0.1           # chapter + bumper start right after L04
    intro(v, T, 0.0, b["00 · MASALAH"])
    masalah(v, T, b["00 · MASALAH"], b["01 · KEPUTUSAN"])
    keputusan(v, T, b["01 · KEPUTUSAN"], b["02 · DIAGRAM"])
    diagram(v, T, b["02 · DIAGRAM"], b["03 · HASIL"])
    hasil(v, T, b["03 · HASIL"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


def _cover_hero(c, box):
    """Cover hero: one stopmap with four source sheets flying in from the corners."""
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2 + 20
    mh = min(h * 0.8, 420)
    mw = mh * 0.8
    stopmap(c, cx, cy, mw, mh, 0.0, pages=COL, glow=1.0)
    for k, (fx, fy) in enumerate(((0.12, 0.18), (0.88, 0.2), (0.1, 0.82), (0.9, 0.8))):
        lembar(c, x + w * fx, y + h * fy, 110, COL[k], SRC[k], rot=(-0.25, 0.2, 0.15, -0.18)[k])




def _fly(t, t0, src, dst, dur=0.55, hang=None):
    """Position + rotation of a sheet flying src → dst from t0 (optionally hanging crooked at 85% for `hang` s)."""
    if t < t0:
        return None
    u = (t - t0) / dur
    if hang:
        if u > 0.85:
            u = 0.85 + max(0.0, (t - t0 - dur * 0.85 - hang) / dur)
    u = clamp(u)
    e = out_cubic(u)
    x = src[0] + (dst[0] - src[0]) * e
    y = src[1] + (dst[1] - src[1]) * e - 120 * math.sin(math.pi * u)
    rot = (1 - e) * (0.6 if src[0] < dst[0] else -0.6) + (0.3 if hang and 0.84 < u < 0.86 else 0.0)
    return x, y, rot, u


# ── INTRO: cold open at the CS desk → windows into one map → punch → bumper ─
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3, L4, L5 = T["L01"], T["L02"], T["L03"], T["L04"], T["L05"]
    t_satu = T.word("L01", "satu")
    t_win = [T.word("L02", w) for w in ("tabungan", "asuransi", "kredit")]
    t_tunggu = T.word("L03", "nunggu")
    t_tanya = T.word("L03", "ditanya")
    t_sama = T.word("L03", "sama")
    t_c360 = T.word("L04", "360")
    t_layar = T.word("L04", "layar")
    headA = Headline("Buka aplikasi *satu-satu*.")
    headB = Headline("Datanya *di mana-mana*.")
    headC = Headline("Ditanya *ulang*.")
    base, dw = 1360, 760
    mon = (MID - 190, 791, 380, 258)
    cs_head = (MID - 304, 880)
    cu_head = (MID + 319, 990)
    map_c = (MID, 790)
    bump0, bump1 = e, max(e + 1.4, L5.start - 0.05)

    cam = v.camera
    cam.key(0.0, zoom=1.08, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.focus(L2.start, mon, zoom=1.08, dur=0.6)
    cam.reset(L3.start, dur=0.6)
    cam.key(t_layar, zoom=0.97, dur=0.12)
    cam.key(t_layar + 0.12, zoom=1.0, dur=0.4)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "PROJECT 360 · DATA NASABAH", PURPLE)
        headA.draw(c, t, L1.start, L2.start - 0.15)
        headB.draw(c, t, L2.start, L3.start - 0.15)
        headC.draw(c, t, L3.start, L4.start - 0.15)
        muted = c.theme("muted", "d_muted")

        def screen(c, sx, sy, sw, sh):
            la = out_expo(prog(t, t_satu, 0.3)) * (1 - prog(t, t_win[0], 0.2))
            c.text(sx + sw / 2, sy + sh / 2 + 8, "membuka aplikasi…", F["mono_med"], 18, muted, la, 0.04, align="c")
            for k, tw in enumerate(t_win):
                if t < tw:
                    continue
                p = out_back(prog(t, tw, 0.35), 1.4)
                wx, wy = sx + 20 + k * 40, sy + 18 + k * 34
                with c.at(0, 0, max(0.01, p), origin=(wx + 120, wy + 70)):
                    c.card(wx, wy, 240, 140, r=10, shadow="card_tight")
                    c.fill_rrect(wx, wy, 240, 30, 10, COL[k])
                    c.text(wx + 14, wy + 22, f"app {SRC[k]}", F["mono_bold"], 17, (1, 1, 1, 1), 1, 0.04)
                    for j in range(3):
                        c.fill_rrect(wx + 14, wy + 50 + j * 26, 160 - j * 30, 10, 4, c.theme("faint", "d_line"))

        def desk(c):
            meja_cs(c, MID, base, dw, t, screen=screen)
            bubble(c, cu_head[0], cu_head[1] - 40, "…", out_expo(prog(t, t_tunggu, 0.35)), align="r")
            bubble(c, cs_head[0], cs_head[1] - 150, ASK, out_expo(prog(t, t_tanya, 0.35)))
            bubble(c, cs_head[0] + 30, cs_head[1] - 240, ASK, out_expo(prog(t, t_sama - 0.1, 0.35)))
        appear(c, t, L1.start - 0.1, L4.start - 0.15, (X, 560, CW, 820), desk, enter="up")

        def punch(c):
            pages = [COL[k] for k in range(3) if t >= L4.start + 0.15 + k * 0.2 + 0.5]
            klik = prog(t, t_c360 - 0.1, 0.25)
            stopmap(c, map_c[0], map_c[1], 220, 270, 1 - klik, pages=pages or [COL[0]], glow=klik)
            for k in range(3):
                f = _fly(t, L4.start + 0.15 + k * 0.2, (X + 60 + k * 360, 1250), map_c, 0.5)
                if f and f[3] < 1:
                    lembar(c, f[0], f[1], 90, COL[k], SRC[k], rot=f[2])
            p = prog(t, t_layar, 0.35)
            size = min(150, 150 * CW / c.measure("satu layar.", F["display"], 150, -0.06)[0])
            with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, 1100)):
                c.text(MID, 1150, "satu layar.", F["display"], size, PURPLE, clamp(p * 3), -0.06, align="c")
        appear(c, t, L4.start, e - OUT, (X, 600, CW, 640), punch, enter="up", blur=4)
    v.add(s, e + 0.4, draw)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 6, "Project 360", PURPLE), z=100)
    v.sfx("whoosh", L1.start - 0.1, 0.5)
    v.sfx("pop", t_satu, 0.3)
    for tw in t_win:
        v.sfx("pop", tw, 0.45)
    v.sfx("pop", t_tunggu, 0.4)
    v.sfx("pop", t_tanya, 0.45)
    v.sfx("pop", t_sama - 0.1, 0.45)
    for k in range(3):
        v.sfx("whoosh", L4.start + 0.15 + k * 0.2, 0.3)
    v.sfx("thud", t_c360 - 0.1, 0.6)
    v.sfx("thud", t_layar)
    v.sfx("whoosh", bump0, 0.8)
    v.sfx("whoosh", bump1 - 0.35, 0.5)


# ── 00 · MASALAH: four counters, walk around, photocopies leak ─────────
def masalah(v, T, s, e):
    ch = v.chapter(0, "MASALAH", s, e)
    L5, L6, L7, L8 = T["L05"], T["L06"], T["L07"], T["L08"]
    t_banyak = T.word("L05", "banyak")
    t_loket = T.word("L06", "loket")
    t_kel = T.word("L07", "keliling")
    t_foto = T.word("L07", "fotokopi")
    t_lama = T.word("L08", "lama")
    t_bocor = T.word("L08", "bocor")
    heads = [(Headline("Satu orang, *banyak* perusahaan."), L5.start, L6.start - 0.15),
             (Headline("Berkasnya *kesebar*."), L6.start, L7.start - 0.15),
             (Headline("Keliling, *fotokopi*."), L7.start, L8.start - 0.15),
             (Headline("Tiap fotokopi, *celah*."), L8.start, e - OUT)]
    box = (X, 560, CW, 800)
    names = ["BANK", "ASURANSI", "MULTIFINANCE", "SEKURITAS"]
    LW, LH = (CW - 90) / 2, 250
    loc = [(X + 30 + (k % 2) * (LW + 30), 620 + (k // 2) * (LH + 30), LW, LH) for k in range(4)]
    t_loc = [L5.start + 0.3 + k * 0.15 for k in range(4)]
    t_stack = [t_loket - 0.3 + k * 0.15 for k in range(4)]
    tray = (MID - 210, 1200, 420, 90)
    t_visit = [t_kel + k * (max(0.6, L8.start - t_kel) / 4) for k in range(4)]
    stops = [(lx + lw * 0.7, ly + lh + 10) for lx, ly, lw, lh in loc]
    path_t0 = t_kel - 0.3

    cam = v.camera
    cam.focus(L5.start + 0.2, (X, 600, CW, 560), zoom=1.04, dur=0.8)
    cam.reset(L7.start, dur=0.6)
    cam.focus(t_bocor - 0.3, (MID - 50, 1150, 420, 300), zoom=1.1, dur=0.5)
    cam.reset(e - 0.8, dur=0.5)

    def draw(c, t):
        kicker(c, t, L5.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        muted, ink = c.theme("muted", "d_muted"), c.theme("ink", "d_ink")
        red = out_expo(prog(t, t_lama, 0.6))

        def counters(c):
            x, y, w, h = box
            c.card(x, y, w, h, r=30)
            for k, (lx, ly, lw, lh) in enumerate(loc):
                a = out_expo(prog(t, t_loc[k], 0.4))
                if a <= 0.01:
                    continue
                with c.group(a):
                    c.fill_rrect(lx, ly, lw, lh, 20, c.theme("bg", "d_bg"))
                    c.circle(lx + 26, ly + 34, 7, COL[k])
                    c.text(lx + 42, ly + 41, names[k], F["mono_bold"], 18, muted, 1, 0.14)
                    # the same (censored) customer at every counter
                    px, py = lx + 70, ly + lh - 30
                    c.circle(px, py - 120, 26, c.theme("ink2", "d_muted"))
                    c.fill_rrect(px - 40, py - 90, 80, 90, 30, c.theme("ink2", "d_muted"))
                    c.fill_rrect(px - 46, py - 132, 92, 16, 4, ink)              # marker bar over the face
                    if t >= t_stack[k]:
                        sa = out_expo(prog(t, t_stack[k], 0.4))
                        for j in range(3):
                            lembar(c, lx + lw * 0.68 + j * 6, ly + lh * 0.52 - j * 6, 92, COL[k], SRC[k],
                                   rot=0.04 * (j - 1), alpha=sa)
            # tray of photocopies
            ta = out_expo(prog(t, t_kel, 0.4))
            if ta > 0:
                tx, ty, tw, th = tray
                c.fill_rrect(tx, ty + th - 26, tw, 26, 8, c.theme("faint", "d_line"), ta)
                c.text(tx + tw / 2, ty + th + 30, "HASIL FOTOKOPI", F["mono_bold"], 17, muted, ta, 0.14, align="c")
            for k, tv in enumerate(t_visit):
                f = _fly(t, tv + 0.25, (stops[k][0], stops[k][1] - 150), (tray[0] + 70 + k * 92, tray[1] + 30),
                         0.6)
                if f:
                    leak = k == 2 and t >= t_bocor
                    if leak:
                        d = out_cubic(prog(t, t_bocor, 1.6))
                        lx, ly = f[0] + 180 * d, f[1] + 160 * d
                        lembar(c, lx, ly, 70, COL[k], "copy", rot=0.5 * d, red=1.0, alpha=1 - prog(t, t_bocor + 1.2, 0.4))
                    else:
                        lembar(c, f[0], f[1], 70, COL[k], "copy", rot=f[2] + 0.05 * (k - 1.5), red=red)
            # CS walking counter to counter
            if t >= path_t0:
                f = prog(t, path_t0, max(0.8, L8.start - path_t0))
                px, py = walk_path([(MID, 1340)] + stops, f)
                visitor(c, px, py, 70, t, PURPLE, walk=1 - prog(t, L8.start, 0.3), alpha=ta, seed=3)
            pop_tag(c, t, t_lama, x + 40, 1300, "lama", RED)
            pop_tag(c, t, t_bocor + 0.2, x + w - 40, 1300, "celah bocor", RED, align="r")
        appear(c, t, L5.start - 0.1, e - OUT, box, counters, enter="up")
    v.add(s, e, draw)
    v.sfx("whoosh", L5.start - 0.1, 0.6)
    for tt in t_loc:
        v.sfx("pop", tt, 0.35)
    for tt in t_stack:
        v.sfx("tick", tt, 0.35)
    v.sfx("whoosh", t_kel, 0.4)
    for tv in t_visit:
        v.sfx("tick", tv + 0.25, 0.4)
    v.sfx("pop", t_lama, 0.4)
    v.sfx("thud", t_bocor, 0.7)


# ── 01 · KEPUTUSAN: sheets into one map — klik — joined, real-time, guarded ─
def keputusan(v, T, s, e):
    ch = v.chapter(1, "KEPUTUSAN", s, e)
    L9, L10, L11, L12 = T["L09"], T["L10"], T["L11"], T["L12"]
    t_map = T.word("L09", "map")
    t_nyambung = T.word("L10", "nyambung")
    t_buka = T.word("L11", "map")
    t_rt = T.word("L11", "real-time")
    t_lapis = T.word("L12", "berlapis")
    heads = [(Headline("Kumpulin jadi *satu map*."), L9.start, L10.start - 0.15),
             (Headline("Semua *nyambung*."), L10.start, L11.start - 0.15),
             (Headline("Ditarik *real-time*."), L11.start, L12.start - 0.15),
             (Headline("Penjagaan *berlapis*."), L12.start, e - OUT)]
    mc = (MID, 960)
    mw, mh = 400, 500
    corners = [(X + 90, 640), (X + CW - 90, 640), (X + 90, 1320), (X + CW - 90, 1320)]
    t_in = [t_map - 0.3 + k * 0.28 for k in range(4)]
    t_klik = t_in[-1] + 0.75
    ring_r = 330

    cam = v.camera
    cam.key(t_klik, zoom=0.97, dur=0.12)
    cam.key(t_klik + 0.12, zoom=1.0, dur=0.4)
    cam.focus(t_buka, (MID - 220, 760, 440, 400), zoom=1.07, dur=0.6)
    cam.reset(L12.start, dur=0.5)
    cam.key(t_lapis - 0.1, zoom=0.96, dur=0.8)

    def draw(c, t):
        kicker(c, t, L9.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def folder(c):
            n_in = sum(1 for k, tt in enumerate(t_in) if t >= tt + (1.0 if k == 2 else 0.55))
            closed = prog(t, t_klik, 0.25)
            reopen = prog(t, t_buka, 0.5)
            stopmap(c, mc[0], mc[1], mw, mh, clamp(1 - closed + reopen), pages=COL[:max(1, n_in)], glow=closed,
                    note_text="jangan difotokopi" if t >= t_klik + 0.3 else None)
            for k, tt in enumerate(t_in):
                f = _fly(t, tt, corners[k], mc, 0.55, hang=0.45 if k == 2 else None)
                if f and f[3] < 1:
                    lembar(c, f[0], f[1], 120, COL[k], SRC[k], rot=f[2])
            # 360 ring: one arc per source joins up
            ra = 1 - prog(t, L12.start, 0.4)
            if t >= t_nyambung - 0.2 and ra > 0:
                cxx = c.ctx
                for k in range(4):
                    p = in_out_cubic(prog(t, t_nyambung - 0.2 + k * 0.15, 0.4))
                    if p <= 0:
                        continue
                    a0 = -math.pi / 2 + k * math.pi / 2 + 0.05
                    cxx.new_path()
                    cxx.arc(mc[0], mc[1], ring_r, a0, a0 + (math.pi / 2 - 0.1) * p)
                    c.src(COL[k], ra)
                    cxx.set_line_width(10)
                    cxx.set_line_cap(1)
                    cxx.stroke()
            # opened → a live profile on the pages
            pa = out_expo(prog(t, t_buka + 0.3, 0.4)) * (1 - prog(t, L12.start, 0.3))
            if pa > 0:
                with c.group(pa):
                    profile_360(c, mc[0] - 180, mc[1] - 150, 360, 300, t, live=out_expo(prog(t, t_rt, 0.3)))
            lp = [dict(p=out_expo(prog(t, t_lapis - 0.3 + k * 0.2, 0.5)), thick=3) for k in range(3)]
            lapis(c, mc[0], mc[1], mw, mh, lp, gap=36)
            stamp(c, mc[0] + 150, mc[1] + 300, "SENSITIF", prog(t, t_lapis + 0.4, 0.35), color=PURPLE, rot=-0.15,
                  size=60)
        appear(c, t, L9.start - 0.1, e - OUT, (X, 600, CW, 760), folder, enter="pop")
    v.add(s, e, draw)
    v.sfx("pop", L9.start - 0.1, 0.4)
    for tt in t_in:
        v.sfx("whoosh", tt, 0.35)
    v.sfx("thud", t_klik, 0.8)
    for k in range(3):
        v.sfx("tick", t_nyambung - 0.2 + k * 0.15, 0.35)
    v.sfx("chime", t_nyambung + 0.5, 0.6)
    v.sfx("pop", t_buka + 0.3, 0.5)
    v.sfx("whoosh", t_lapis - 0.3, 0.5)
    v.sfx("thud", t_lapis + 0.4, 0.7)


# ── 02 · DIAGRAM: Docker on ECS (HA) inside WAF · VPN · IDaaS ──────────
def diagram(v, T, s, e):
    ch = v.chapter(2, "DIAGRAM", s, e)
    L13, L14, L15, L16, L17 = T["L13"], T["L14"], T["L15"], T["L16"], T["L17"]
    t_docker = T.word("L13", "Docker")
    t_ecs = T.word("L13", "ECS")
    t_down = T.word("L14", "down")
    t_layan = T.word("L14", "ngelayanin")
    t_waf = T.word("L15", "WAF")
    t_vpn = T.word("L16", "VPN")
    t_kantor = T.word("L16", "kantor")
    t_idaas = T.word("L17", "IDaaS")
    t_login = T.word("L17", "login")
    heads = [(Headline("Docker di atas *ECS*."), L13.start, L14.start - 0.15),
             (Headline("Satu down, *yang lain jalan*."), L14.start, L15.start - 0.15),
             (Headline("Lapis 1: *WAF*."), L15.start, L16.start - 0.15),
             (Headline("Lapis 2: *VPN*."), L16.start, L17.start - 0.15),
             (Headline("Lapis 3: *IDaaS*."), L17.start, e - OUT)]
    cx, cy, cw, chh = MID, 1000, 340, 260
    gap = 70
    nodes = [(cx - 150, cy - 90, 140, 190), (cx + 10, cy - 90, 140, 190)]
    kantor = (MID - 150, 1420)
    card = (MID + 110, 1410)
    t0 = L13.start + 0.6

    cam = v.camera
    cam.focus(L13.start, (cx - 200, cy - 160, 400, 320), zoom=1.12, dur=0.7)
    cam.reset(L15.start - 0.1, dur=0.7)
    cam.focus(L16.start, (X, 1150, CW, 340), zoom=1.05, dur=0.6)
    cam.reset(e - 0.8, dur=0.5)

    def draw(c, t):
        kicker(c, t, L13.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        muted, ink = c.theme("muted", "d_muted"), c.theme("ink", "d_ink")
        down = out_expo(prog(t, t_down, 0.3))

        def core(c):
            x, y = cx - cw / 2, cy - chh / 2
            c.card(x, y, cw, chh, r=22)
            c.text(x + 20, y + 36, "ECS", F["mono_bold"], 19, PURPLE, out_expo(prog(t, t_ecs, 0.4)), 0.16)
            for k, (nx, ny, nw, nh) in enumerate(nodes):
                dead = down if k == 0 else 0.0
                c.stroke_rrect(nx, ny, nw, nh, 14, RED if dead > 0.5 else c.theme("faint", "d_line"), 2)
                c.text(nx + nw / 2, ny + 28, f"node-{k + 1}", F["mono_med"], 17, RED if dead > 0.5 else muted, 1,
                       0.06, align="c")
                for j in range(2):
                    da = out_back(prog(t, t_docker + 0.1 * (2 * k + j), 0.35), 1.5) if t >= t_docker else 0
                    if da <= 0.01:
                        continue
                    bx, by = nx + 14, ny + 48 + j * 66
                    with c.at(0, 0, max(0.01, da), origin=(bx + (nw - 28) / 2, by + 27)):
                        col = RED if dead > 0.5 else PURPLE
                        c.fill_rrect(bx, by, nw - 28, 54, 10, col, 0.15 + 0.15 * (1 - dead))
                        c.text(bx + (nw - 28) / 2, by + 34, "docker", F["mono_bold"], 17, col, 1, 0.04, align="c")
                if dead > 0.01:
                    c.text(nx + nw / 2, ny + nh + 34, "down", F["mono_bold"], 19, RED, dead, 0.1, align="c")
            # request dots into the nodes (after down: all to node-2)
            if t >= t0:
                for i in range(int((t - t0) / 0.35) + 1):
                    ts = t0 + i * 0.35
                    f = (t - ts) / 0.9
                    if not 0 <= f <= 1:
                        continue
                    k = 1 if (ts >= t_down or i % 2) else 0
                    nx, ny, nw, nh = nodes[k]
                    px, py = walk_path([(cx, 620), (cx, y - 6), (nx + nw / 2, ny + 10)], f)
                    c.circle(px, py, 7, C["accent"], fade_ends(f))
        appear(c, t, L13.start - 0.1, e - OUT, (cx - cw / 2, cy - chh / 2, cw, chh), core, enter="pop")
        pop_tag(c, t, t_layan, cx + cw / 2 + 20, cy - 22, "tetap ngelayanin", OK)

        layers = [dict(label="IDaaS", p=out_expo(prog(t, t_idaas - 0.2, 0.6))),
                  dict(label="VPN", p=out_expo(prog(t, t_vpn - 0.2, 0.6))),
                  dict(label="WAF", p=out_expo(prog(t, t_waf - 0.2, 0.6)))]
        lapis(c, cx, cy, cw, chh, layers, gap=gap)
        # WAF: bad requests bounce off the outer ring
        top = cy - chh / 2 - 3 * gap
        if t >= t_waf:
            for k in range(3):
                ts = t_waf + 0.2 + k * 0.45
                if t < ts:
                    continue
                f = prog(t, ts, 0.9)
                bx = cx - 260 + k * 260
                yy = 600 + (top - 600 - 10) * out_cubic(min(1, f * 1.6)) - 70 * clamp(f * 1.6 - 1)
                c.circle(bx, yy, 9, RED, 1 - prog(t, ts + 0.7, 0.2))
        # VPN: the office tunnel connects; an outsider stops at the VPN ring
        va = out_expo(prog(t, t_kantor - 0.2, 0.4))
        if va > 0:
            kx, ky = kantor
            c.fill_rrect(kx - 50, ky - 70, 100, 70, 8, c.theme("ink2", "d_muted"), va)
            for j in range(3):
                c.fill_rrect(kx - 36 + j * 28, ky - 56, 16, 16, 3, c.theme("card", "d_card"), va)
            c.text(kx, ky + 30, "kantor", F["mono_bold"], 18, c.theme("ink2", "d_muted"), va, 0.08, align="c")
            pl = in_out_cubic(prog(t, t_kantor, 0.6))
            c.line(kx, ky - 74, kx + (cx - 60 - kx) * pl, ky - 74 - (ky - 74 - cy - chh / 2 - 4) * pl, PURPLE, 10,
                   0.5 * va)
            ox = X + 40
            f = prog(t, t_kantor + 0.4, 0.8)
            c.circle(ox + (cx - cw / 2 - 2 * gap - ox - 10) * out_cubic(f), cy + 120, 9, RED,
                     va * (1 - prog(t, t_kantor + 1.4, 0.3)))
        # IDaaS: an employee card taps the reader
        ia = out_expo(prog(t, t_idaas - 0.1, 0.4))
        if ia > 0:
            id_card(c, card[0], card[1], 110, tap=prog(t, t_login - 0.2, 0.5), ok=prog(t, t_login + 0.3, 0.3),
                    alpha=ia)
    v.add(s, e, draw)
    v.sfx("pop", L13.start - 0.1, 0.4)
    v.sfx("pop", t_docker, 0.4)
    v.sfx("pop", t_ecs, 0.4)
    v.sfx("thud", t_down, 0.6)
    v.sfx("pop", t_layan, 0.4)
    v.sfx("whoosh", t_waf - 0.2, 0.5)
    for k in range(3):
        v.sfx("tick", t_waf + 0.2 + k * 0.45 + 0.55, 0.35)
    v.sfx("whoosh", t_vpn - 0.2, 0.5)
    v.sfx("pop", t_kantor, 0.4)
    v.sfx("whoosh", t_idaas - 0.2, 0.5)
    v.sfx("chime", t_login + 0.3, 0.7)


# ── 03 · HASIL: the full profile on one screen, live, guarded ──────────
def hasil(v, T, s, e):
    ch = v.chapter(3, "HASIL", s, e)
    L18, L19, L20 = T["L18"], T["L19"], T["L20"]
    t_layar = T.word("L18", "layar")
    t_rt = T.word("L19", "real-time")
    t_aman = T.word("L20", "aman")
    head1 = Headline("Satu nasabah, *satu layar*.")
    head2 = Headline("Ditarik *real-time*.")
    head3 = Headline("Tetap *aman*.")
    card = (X, 620, CW, 560)
    t_ring = [t_layar - 0.2 + k * 0.25 for k in range(4)]
    guards = ["WAF", "VPN", "IDaaS"]

    cam = v.camera
    cam.focus(L18.start + 0.2, (X, 620, 400, 300), zoom=1.06, dur=0.7)
    cam.reset(L19.start, dur=0.5)
    cam.key(t_aman, zoom=0.97, dur=0.12)
    cam.key(t_aman + 0.12, zoom=1.0, dur=0.4)

    def draw(c, t):
        kicker(c, t, L18.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L18.start, L19.start - 0.15)
        head2.draw(c, t, L19.start, L20.start - 0.15)
        head3.draw(c, t, L20.start, e - OUT)
        muted = c.theme("muted", "d_muted")

        def profile(c):
            x, y, w, h = card
            ring = [out_expo(prog(t, tt, 0.5)) for tt in t_ring]
            chips = [(SRC[k], out_expo(prog(t, t_ring[k] + 0.1, 0.3))) for k in range(4)]
            profile_360(c, x, y, w, h, t, ring=ring, chips=chips, live=out_expo(prog(t, t_rt, 0.3)))
            la = out_expo(prog(t, t_rt + 0.2, 0.4))
            c.text(x + 40, y + h - 40, "diperbarui · baru saja", F["mono_med"], 20, muted, la, 0.04)
            for k, g in enumerate(guards):
                gx = x + k * 220
                tt = t_aman - 0.3 + k * 0.2
                pop_tag(c, t, tt, gx + 60, y + h + 40, g, OK)
                check_badge(c, gx + 30, y + h + 62, 20, out_back(prog(t, tt, 0.4), 1.8) if t >= tt else 0)
        appear(c, t, L18.start - 0.1, e - OUT, card, profile, enter="right")
        fade(c, t, t_rt + 0.5, e - OUT,
             lambda c: note(c, X + CW - 30, card[1] + card[3] - 60, "tanpa fotokopi", prog(t, t_rt + 0.6, 0.9),
                            align="r", size=40))
    v.add(s, e, draw)
    v.sfx("whoosh", L18.start - 0.1, 0.5)
    for tt in t_ring:
        v.sfx("pop", tt, 0.35)
    v.sfx("tick", t_rt, 0.5)
    for k in range(3):
        v.sfx("pop", t_aman - 0.3 + k * 0.2, 0.4)
    v.sfx("chime", t_aman + 0.4, 0.7)


# ── RECAP (dark): same desk — the repeated question is struck before it's asked ─
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L21, L22, L23 = T["L21"], T["L22"], T["L23"]
    t_dua = T.word("L22", "dua")
    t_leng = T.word("L23", "lengkap")
    t_tebal = T.word("L23", "tebal")
    heads = [(Headline("Bukan soal *sebanyak-banyaknya*.", style="headline_dark"), L21.start, L22.start - 0.15),
             (Headline("Nggak cerita *dua kali*.", style="headline_dark"), L22.start, L23.start - 0.15),
             (Headline("Makin lengkap, makin *tebal*.", style="headline_dark"), L23.start, e - OUT)]
    base, dw = 1340, 700
    cs_head = (MID - 280, 900)
    cu_head = (MID + 294, 1000)
    t_ask = L22.start + 0.1

    cam = v.camera
    cam.key(s, zoom=1.15, y=1000, dur=0.01)
    cam.key(L22.start, zoom=1.0, dur=1.4)

    def draw(c, t):
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def screen(c, sx, sy, sw, sh):
            profile_360(c, sx + 10, sy + 10, sw - 20, sh - 20, t, live=1.0)

        def desk(c):
            meja_cs(c, MID, base, dw, t, screen=screen)
            r = bubble(c, cs_head[0], cs_head[1] - 150, ASK, out_expo(prog(t, t_ask, 0.35)))
            if r and t >= t_dua:
                bx, by, bw, bh = r
                strike(c, t, t_dua, bx + 10, bx + bw - 10, by + bh / 2, width=6)
            check_badge(c, cu_head[0], cu_head[1] - 80, 30, out_back(prog(t, t_dua + 0.4, 0.4), 1.8) if t >= t_dua + 0.4
                   else 0)
        appear(c, t, L21.start - 0.1, L23.start - 0.15, (X, 600, CW, 760), desk, enter="up", exit="up")

        def guarded(c):
            n = 2 + int(4 * clamp(prog(t, t_leng, 1.4)))
            thick = 3 + 9 * in_out_cubic(prog(t, t_tebal - 0.3, 0.8))
            cols = (COL * 2)[:n]
            stopmap(c, MID, 980, 300, 380, 0.0, pages=cols, glow=1.0)
            lapis(c, MID, 980, 300, 380, [dict(p=1.0, thick=thick, solid=True) for _ in range(3)], gap=44)
        appear(c, t, L23.start - 0.1, e - OUT, (MID - 300, 720, 600, 520), guarded, enter="pop")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("pop", t_ask, 0.45)
    v.sfx("tick", t_dua, 0.6)
    v.sfx("chime", t_dua + 0.4, 0.7)
    v.sfx("pop", L23.start - 0.1, 0.4)
    for k in range(3):
        v.sfx("pop", t_leng + k * 0.35, 0.3)


# ── OUTRO: logo + EP07 teaser + follow ─────────────────────────────────
def outro(v, T, s, e):
    series_outro(v, T, s, e, "L24", "L25", "EPISODE TERAKHIR · EP 07", "Azure AI Infrastructure",
                 "Fondasi buat training AI", PURPLE)
