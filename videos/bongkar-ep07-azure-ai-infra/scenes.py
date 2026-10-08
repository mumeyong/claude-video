"""Bongkar Arsitektur EP07 — Fondasi buat training AI di Azure (series finale). See IDENTITY.md / TREATMENT.md.

Metaphor: a badminton athlete — training camp (training) vs the match (inference); GPU = the heavy training court,
AKS = the coach with the schedule, clouds = sports halls. Signature move: a shuttle arcs over the net, each landing
lights one rep dot. Color: orange. Hook: myth struck out. No numbers. No AI brain/robot imagery.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_cubic, in_out_cubic, clamp
from engine.components import (Headline, kicker, appear, fade, Cursor, icons, note, strike, stamp, follow_button,
                               arch_node, series_bumper, gpu_card, lapangan, pemain, shuttle, shuttle_arc,
                               pelontar, rep_dots, jadwal, gor, cover, BADMINTON_ORANGE as ORANGE, check_badge,
                               pop_tag)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · MASALAH", "01 · KEPUTUSAN", "02 · DIAGRAM", "03 · HASIL", "RECAP", "OUTRO"]
OK = C["ok"]
RED = C["rec"]
GW, GH, GG = 180, 120, 22                          # GPU grid card size + gap
GX0 = MID - (4 * GW + 3 * GG) / 2
KEEP = (1, 6, 10)                                  # the cards that stay on ("pas perlu")


def build(project):
    T = project.timing
    v = Video(duration=T["L25"].end + TAIL, bpm=128, beat_offset=0.0, series="BONGKAR ARSITEKTUR · EP 07")
    v.cover_t = T.word("L04", "Azure") + 0.6
    v.music = dict(key="E", mood="bright")           # generated score: sporty finale, after G tense (EP06)
    v.cover = lambda c: cover(c, "GPU nyala\n*pas perlu*.", kicker="BONGKAR ARSITEKTUR · EP 07", color=ORANGE,
                              badge="EP 07 · FINAL", tags=["training", "inference", "AKS"], hero=_cover_hero)
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
    """Cover hero: a lit court with a shuttle mid-arc, and a row of GPU cards with only one on."""
    x, y, w, h = box
    base = y + h - 40
    lapangan(c, x, base, w, 0.0, lights=1.0, lamp_h=min(260, h * 0.55))
    pemain(c, x + w * 0.18, base, 170, 0.0, swing=0.7)
    sx, sy, ang = shuttle_arc(x + w * 0.2, base - 150, x + w * 0.85, base - 40, 160, 0.45)
    shuttle(c, sx, sy, 26, ang)
    for k in range(4):
        gpu_card(c, x + k * (w / 4) + 10, y + 10, w / 4 - 20, 80, 0.0, on=1.0 if k == 1 else 0.0, label=None)




def _grid(c, t, y0, on_of):
    """The GPU 'gudang': 4×3 gpu_cards; on_of(k) → 0..1."""
    for k in range(12):
        gx = GX0 + (k % 4) * (GW + GG)
        gy = y0 + (k // 4) * (GH + GG)
        gpu_card(c, gx, gy, GW, GH, t, on=on_of(k), label=f"GPU {k + 1:02d}", seed=k)


# ── INTRO: the GPU warehouse myth → struck → it's about *when* → Azure → bumper ─
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3, L4, L5 = T["L01"], T["L02"], T["L03"], T["L04"], T["L05"]
    t_gudang = T.word("L01", "segudang")
    t_terus = T.word("L01", "terus")
    t_nggak = T.word("L02", "nggak")
    t_mahal = T.word("L03", "mahal")
    t_kapan = T.word("L03", "kapan")
    t_az = T.word("L04", "Azure")
    headA = Headline("GPU *segudang*?")
    headB = Headline("*Nggak* juga.")
    headC = Headline("Soal *kapan*.")
    gy0 = 640
    cap = "beli GPU segudang, nyala terus"
    bump0, bump1 = e, max(e + 1.4, L5.start - 0.05)

    cam = v.camera
    cam.key(0.0, zoom=1.1, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.key(t_nggak, zoom=0.97, dur=0.12)
    cam.key(t_nggak + 0.12, zoom=1.0, dur=0.4)
    cam.key(t_az, zoom=0.97, dur=0.12)
    cam.key(t_az + 0.12, zoom=1.0, dur=0.4)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "AI INFRA · AZURE", ORANGE)
        headA.draw(c, t, L1.start, L2.start - 0.15)
        headB.draw(c, t, L2.start, L3.start - 0.15)
        headC.draw(c, t, L3.start, L4.start - 0.15)

        def warehouse(c):
            def on(k):
                a = out_expo(prog(t, L1.start + 0.2 + k * 0.06, 0.3))
                if k not in KEEP:
                    a *= 1 - in_out_cubic(prog(t, t_kapan - 0.2 + (k % 4) * 0.05, 0.4))
                return a
            _grid(c, t, gy0, on)
            ca = out_expo(prog(t, t_gudang, 0.4))
            w = c.measure(cap, F["mono_med"], 30, 0.02)[0]
            c.text(MID, 1130, cap, F["mono_med"], 30, c.theme("ink2", "d_muted"), ca, 0.02, align="c")
            strike(c, t, t_nggak, MID - w / 2 - 10, MID + w / 2 + 10, 1120, width=8)
            pop_tag(c, t, t_terus, X + CW, 590, "nyala terus", ORANGE, align="r")
            pop_tag(c, t, t_mahal, X, 1180, "GPU = mahal", RED)
        appear(c, t, L1.start - 0.1, L4.start - 0.15, (X, 580, CW, 660), warehouse, enter="up")

        def punch(c):
            p = prog(t, t_az, 0.35)
            a0 = out_expo(prog(t, L4.start, 0.4))
            c.text(MID, 840, "training + inference", F["mono_med"], 32, c.theme("ink2", "d_muted"), a0, 0.06,
                   align="c")
            c.line(MID, 880, MID, 880 + 70 * a0, c.theme("faint", "d_line"), 4)
            with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, 1060)):
                c.text(MID, 1130, "Azure.", F["display"], 230, ORANGE, clamp(p * 3), -0.06, align="c")
        appear(c, t, L4.start, e - OUT, (X, 780, CW, 420), punch, enter="up", blur=4)
    v.add(s, e + 0.4, draw)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 7, "Azure AI infrastructure", ORANGE), z=100)
    v.sfx("whoosh", L1.start - 0.1, 0.5)
    for k in range(0, 12, 3):
        v.sfx("tick", L1.start + 0.2 + k * 0.06, 0.3)
    v.sfx("pop", t_terus, 0.45)
    v.sfx("thud", t_nggak, 0.8)
    v.sfx("pop", t_mahal, 0.45)
    v.sfx("tick", t_kapan, 0.5)
    v.sfx("whoosh", L4.start - 0.1, 0.5)
    v.sfx("thud", t_az)
    v.sfx("whoosh", bump0, 0.8)
    v.sfx("whoosh", bump1 - 0.35, 0.5)


# ── 00 · MASALAH: training drill vs match on one court ─────────────────
def masalah(v, T, s, e):
    ch = v.chapter(0, "MASALAH", s, e)
    L5, L6, L7, L8, L9 = T["L05"], T["L06"], T["L07"], T["L08"], T["L09"]
    t_atlet = T.word("L05", "atlet")
    t_lat = T.word("L06", "latihan")
    t_train = T.word("L07", "training")
    t_sem = T.word("L07", "sementara")
    t_tand = T.word("L08", "tanding")
    t_inf = T.word("L09", "inference")
    t_reb = T.word("L09", "rebutan")
    t_kalah = T.word("L09", "kalah")
    heads = [(Headline("Model = *atlet*."), L5.start, L6.start - 0.15),
             (Headline("Masa *latihan*."), L6.start, L7.start - 0.15),
             (Headline("Itu *training*."), L7.start, L8.start - 0.15),
             (Headline("Pas *tanding*."), L8.start, L9.start - 0.15),
             (Headline("Rebutan, *kalah* dua-duanya."), L9.start, e - OUT)]
    box = (X, 560, CW, 800)
    base = 1150
    px, py = X + 200, base - 140                    # player's racket point
    lx = X + CW - 150                               # launcher
    mouth = (lx - 70, base - 130)
    t_shots = []
    tt = L6.start + 0.2
    while tt < L8.start - 0.6:
        t_shots.append(tt)
        tt += 0.55
    FL = 0.6                                        # flight time
    t_smash = t_tand + 0.5
    t_clash = t_reb - 0.4

    cam = v.camera
    cam.focus(L6.start + 1.0, (X, 1150, CW, 140), zoom=1.05, dur=0.8)
    cam.reset(L8.start, dur=0.5)
    cam.key(t_smash + 0.3, zoom=0.97, dur=0.12)
    cam.key(t_smash + 0.42, zoom=1.0, dur=0.4)
    cam.focus(t_clash, (MID - 200, 760, 400, 300), zoom=1.08, dur=0.4)
    cam.reset(t_kalah + 0.3, dur=0.6)

    def draw(c, t):
        kicker(c, t, L5.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        muted = c.theme("muted", "d_muted")
        out_l = prog(t, L8.start - 0.2, 0.4)                    # launcher leaves for the match
        back = prog(t, L9.start, 0.4)                           # …and comes back onto the same court
        la = max(1 - out_l, back)
        opp = out_expo(prog(t, L8.start, 0.4))

        def court(c):
            x, y, w, h = box
            c.card(x, y, w, h, r=30)
            c.text(x + 30, y + 50, "SATU LAPANGAN", F["mono_bold"], 19, muted, 1, 0.16)
            lapangan(c, x + 40, base, w - 80, t, lights=1.0)
            # player swings when a shuttle arrives (and on the smash)
            sw = 0.0
            for ts in t_shots + [t_smash - FL]:
                d = t - (ts + FL)
                if -0.15 < d < 0.25:
                    sw = max(sw, 1 - abs(d - 0.05) / 0.2)
            pemain(c, x + 170, base, 200, t, swing=clamp(sw), facing=1)
            fire = max([clamp(1 - abs(t - ts) / 0.12) for ts in t_shots] + [0.0])
            pelontar(c, lx + 260 * (1 - la), base, 190, t, fire=fire, alpha=la)
            pemain(c, x + w - 170, base, 200, t, swing=0.3, facing=-1, alpha=opp * (1 - back))
            # training drill: arcs over the net → rep dots (one shuttle gets stuck on the net)
            n_on = 0.0
            for k, ts in enumerate(t_shots):
                u = (t - ts) / FL
                if k == 3:
                    if 0 <= u <= 1.8:
                        su = min(u, 0.55)
                        sx, sy, ang = shuttle_arc(mouth[0], mouth[1], px, py, 170, su)
                        drop = 80 * in_cubic(clamp((u - 0.9) / 0.9))
                        shuttle(c, sx, sy + drop, 22, ang if u < 0.55 else 1.4, alpha=1 - clamp((u - 1.6) / 0.2))
                    continue
                if 0 <= u <= 1:
                    sx, sy, ang = shuttle_arc(mouth[0], mouth[1], px, py, 170, u)
                    shuttle(c, sx, sy, 22, ang)
                if u > 1:
                    n_on += min(1.0, (u - 1) * 4)
            rep_dots(c, x + 60, 1235, 16, n_on, gap=46, alpha=out_expo(prog(t, L6.start, 0.4)))
            c.text(x + 60, 1205, "REPETISI", F["mono_bold"], 17, muted, out_expo(prog(t, L6.start, 0.4)), 0.14)
            # the match: one smash, one point
            if t >= t_smash - FL * 0.5:
                u = (t - (t_smash - 0.05)) / 0.35
                if 0 <= u <= 1:
                    sx, sy, ang = shuttle_arc(px + 20, py - 30, x + w - 300, base - 6, 20, u)
                    shuttle(c, sx, sy, 22, ang)
                stamp(c, x + w - 260, 820, "POIN", prog(t, t_smash + 0.3, 0.35) * (1 - back), color=ORANGE,
                      rot=-0.12, size=64)
            # both on one court: a drill shuttle and a match shuttle collide over the net
            if t >= t_clash - 0.4:
                u = clamp((t - (t_clash - 0.4)) / 0.4)
                a = 1 - prog(t, t_clash + 0.3, 0.3)
                sx1, sy1, a1 = shuttle_arc(mouth[0], mouth[1], MID + 10, 860, 60, u)
                sx2, sy2, a2 = shuttle_arc(px, py, MID - 10, 860, 60, u)
                shuttle(c, sx1, sy1, 22, a1, alpha=a)
                shuttle(c, sx2, sy2, 22, a2, alpha=a)
                if t >= t_clash:
                    p = out_expo(prog(t, t_clash, 0.4))
                    for j in range(8):
                        ang = j / 8 * 2 * math.pi
                        c.line(MID + 20 * p * math.cos(ang), 860 + 20 * p * math.sin(ang),
                               MID + 60 * p * math.cos(ang), 860 + 60 * p * math.sin(ang), RED, 5,
                               1 - prog(t, t_clash + 0.4, 0.4))
            with c.group(1 - prog(t, L8.start, 0.3)):
                pop_tag(c, t, t_train, x + 40, 1280, "training · berat", ORANGE)
                pop_tag(c, t, t_sem, x + w - 40, 1280, "cuma sementara", muted, align="r")
            with c.group(1 - prog(t, L9.start + 0.3, 0.3)):
                pop_tag(c, t, t_smash + 0.3, x + 40, 1280, "inference · cepat", ORANGE)
            pop_tag(c, t, t_reb, x + 40, 1280, "rebutan satu lapangan", RED)
        appear(c, t, L5.start - 0.1, e - OUT, box, court, enter="up")
        fade(c, t, t_atlet + 0.3, L6.start + 1.5,
             lambda c: note(c, X + CW - 40, 700, "ini model AI-nya", prog(t, t_atlet + 0.4, 0.9),
                            arrow_to=(X + 250, base - 230), align="r", size=40))
    v.add(s, e, draw)
    v.sfx("whoosh", L5.start - 0.1, 0.6)
    for ts in t_shots:
        v.sfx("pop", ts, 0.25)
    v.sfx("pop", t_train, 0.4)
    v.sfx("pop", t_sem, 0.4)
    v.sfx("whoosh", L8.start - 0.2, 0.4)
    v.sfx("thud", t_smash + 0.3, 0.8)
    v.sfx("pop", t_inf, 0.3)
    v.sfx("thud", t_clash, 0.7)
    v.sfx("pop", t_reb, 0.45)


# ── 01 · KEPUTUSAN: split courts + the coach's schedule (AKS) ──────────
def keputusan(v, T, s, e):
    ch = v.chapter(1, "KEPUTUSAN", s, e)
    L10, L11, L12, L13 = T["L10"], T["L11"], T["L12"], T["L13"]
    t_pisah = T.word("L10", "dipisah")
    t_gpu = T.word("L11", "GPU")
    t_jad = T.word("L11", "jadwal")
    t_siap = T.word("L12", "siap")
    t_k8s = T.word("L13", "Kubernetes")
    heads = [(Headline("Lapangannya *dipisah*."), L10.start, L11.start - 0.15),
             (Headline("Latihan pakai *GPU*."), L11.start, L12.start - 0.15),
             (Headline("Tanding: *selalu siap*."), L12.start, L13.start - 0.15),
             (Headline("Pelatihnya: *AKS*."), L13.start, e - OUT)]
    top_b, bot_b = 900, 1190
    BLOCKS = [(0.05, 0.3), (0.55, 0.78)]
    board_y = 1270
    t_board = L13.start - 0.1

    def playhead(t):
        return ((t - t_board) * 0.22) % 1.0 if t >= t_board else None

    def lights_top(t):
        ph = playhead(t)
        if ph is not None:
            return max(clamp(1 - max(f0 - ph, 0.0, ph - f1) * 12) for f0, f1 in BLOCKS)
        return _win(t, t_jad - 0.2, L12.start - 0.1)

    cam = v.camera
    cam.key(t_pisah, zoom=0.97, dur=0.12)
    cam.key(t_pisah + 0.12, zoom=1.0, dur=0.4)
    cam.focus(L11.start, (X, 620, CW, 340), zoom=1.05, dur=0.6)
    cam.focus(L12.start, (MID - 320, 1000, 640, 260), zoom=1.06, dur=0.6)
    cam.reset(L13.start, dur=0.6)

    def draw(c, t):
        kicker(c, t, L10.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        sp = in_out_cubic(prog(t, t_pisah, 0.7))
        muted = c.theme("muted", "d_muted")

        def courts(c):
            lt = lights_top(t)
            # top: training court (GPU) — follows the schedule
            yb = 1050 + (top_b - 1050) * sp
            lapangan(c, X, yb, CW, t, lights=lt if sp > 0.5 else 1.0,
                     label="LAPANGAN LATIHAN · GPU" if sp > 0.5 else None, lamp_h=240)
            pemain(c, X + 150, yb, 170, t, swing=0.5 + 0.5 * math.sin(t * 6) * lt if sp > 0.5 else 0.3)
            pelontar(c, X + CW - 140, yb, 160, t, alpha=1.0)
            if sp > 0.5 and lt > 0.5:
                u = (t * 1.6) % 1.0
                sx, sy, ang = shuttle_arc(X + CW - 210, yb - 110, X + 190, yb - 130, 120, u)
                shuttle(c, sx, sy, 20, ang)
            if sp > 0.5:
                for k in range(3):
                    gpu_card(c, X + CW - 3 * 108 + k * 108, yb + 70, 96, 64, t, on=lt, label=None, seed=k)
            # bottom: match court — small, always ready
            if sp > 0.01:
                w2 = 600
                with c.group(sp):
                    lapangan(c, MID - w2 / 2, bot_b, w2, t, lights=0.6, label="LAPANGAN TANDING", lamp_h=150)
                    pemain(c, MID - w2 / 2 + 90, bot_b, 130, t, swing=0.3)
                    pemain(c, MID + w2 / 2 - 90, bot_b, 130, t, swing=0.3, facing=-1)
            pop_tag(c, t, t_gpu, X + CW, top_b + 34, "GPU", ORANGE, align="r")
            pop_tag(c, t, t_siap, MID + 310, bot_b + 34, "selalu siap", OK, align="r")
        appear(c, t, L10.start - 0.1, e - OUT, (X, 600, CW, 680), courts, enter="up")

        def board(c):
            rows = [dict(label="latihan · GPU", blocks=BLOCKS, struck=(0.84, 0.96)),
                    dict(label="tanding", blocks=[(0.0, 1.0)], color=OK)]
            jadwal(c, X, board_y, CW, rows, t, playhead=playhead(t), row_h=56)
        appear(c, t, t_board, e - OUT, (X, board_y, CW, 202), board, enter="left")
        pop_tag(c, t, t_k8s, X + CW, board_y - 54, "Kubernetes · AKS", C["accent"], align="r")
    v.add(s, e, draw)
    v.sfx("pop", L10.start - 0.1, 0.4)
    v.sfx("thud", t_pisah, 0.7)
    v.sfx("whoosh", t_pisah + 0.1, 0.4)
    v.sfx("pop", t_gpu, 0.45)
    v.sfx("pop", t_jad, 0.35)
    v.sfx("pop", t_siap, 0.45)
    v.sfx("whoosh", t_board, 0.5)
    v.sfx("pop", t_k8s, 0.45)


def _win(t, a, b, d=0.25):
    """1 inside [a, b] with soft edges."""
    return out_expo(prog(t, a, d)) * (1 - in_cubic(prog(t, b, d)))


# ── 02 · DIAGRAM: AKS — GPU pool trains & scales down, inference pool serves ─
def diagram(v, T, s, e):
    ch = v.chapter(2, "DIAGRAM", s, e)
    L14, L15, L16, L17 = T["L14"], T["L15"], T["L16"], T["L17"]
    t_gpu = T.word("L14", "GPU")
    t_turun = T.word("L15", "turun")
    t_inf = T.word("L16", "inference")
    t_cont = T.word("L17", "container")
    t_lain = T.word("L17", "lain")
    heads = [(Headline("Masuk ke *GPU pool*."), L14.start, L15.start - 0.15),
             (Headline("Selesai, *scale turun*."), L15.start, L16.start - 0.15),
             (Headline("Deploy ke *inference*."), L16.start, L17.start - 0.15),
             (Headline("Bisa pindah *cloud*."), L17.start, e - OUT)]
    data = (X, 560, 360, 80)
    users = (X + CW - 360, 560, 360, 80)
    aks = (X, 690, CW, 520)
    PW = 380
    gpool = (X + 30, 750, PW, 300)
    ipool = (X + CW - 30 - PW, 750, PW, 300)
    gors = [(X, 1250, 400, 180), (X + CW - 400, 1250, 400, 180)]
    t_on = [t_gpu + 0.2 + k * 0.15 for k in range(3)]
    t_off = [t_turun + k * 0.25 for k in range(3)]

    cam = v.camera
    cam.focus(L14.start, (gpool[0], 560, PW, 500), zoom=1.06, dur=0.6)
    cam.focus(L16.start, (ipool[0], 560, PW, 500), zoom=1.06, dur=0.6)
    cam.reset(L17.start, dur=0.6)
    cam.focus(t_cont, (X, 1200, CW, 260), zoom=1.05, dur=0.6)
    cam.reset(e - 0.8, dur=0.5)

    def draw(c, t):
        kicker(c, t, L14.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        muted, faint, ink = c.theme("muted", "d_muted"), c.theme("faint", "d_line"), c.theme("ink", "d_ink")

        def graph(c):
            arch_node(c, dict(x=data[0], y=data[1], w=360, h=80, kind="svc", label="data latihan",
                              a=out_expo(prog(t, L14.start, 0.4))))
            arch_node(c, dict(x=users[0], y=users[1], w=360, h=80, kind="users", label="users",
                              a=out_expo(prog(t, t_inf, 0.4))))
            x, y, w, h = aks
            c.stroke_rrect(x, y, w, h, 28, C["accent"], 2.5, 0.8, dash=[14, 10])
            c.text(x + 24, y + 36, "AKS CLUSTER · AZURE", F["mono_bold"], 18, C["accent"], 1, 0.16)
            # GPU node pool
            gx, gy, gw, gh = gpool
            c.card(gx, gy, gw, gh, r=22)
            c.text(gx + 22, gy + 40, "GPU NODE POOL", F["mono_bold"], 18, ORANGE, 1, 0.14)
            c.text(gx + 22, gy + 66, "training", F["mono"], 17, muted, 1, 0.04)
            for k in range(3):
                on = _win(t, t_on[k], t_off[k], 0.3)
                gpu_card(c, gx + 22 + k * 118, gy + 110, 106, 120, t, on=on, label=None, seed=k)
            # data → GPU while training
            if L14.start + 0.4 <= t < t_off[-1]:
                for j in range(3):
                    f = ((t - L14.start) * 1.2 + j / 3) % 1.0
                    c.circle(data[0] + 180, data[1] + 84 + (gy - data[1] - 88) * f, 7, ORANGE, min(1, f * 6, (1 - f) * 6))
            # inference pool: always on
            ia = out_expo(prog(t, t_inf - 0.3, 0.4))
            if ia > 0.01:
                with c.group(ia):
                    ix, iy, iw, ih = ipool
                    c.card(ix, iy, iw, ih, r=22)
                    c.text(ix + 22, iy + 40, "INFERENCE POOL", F["mono_bold"], 18, OK, 1, 0.14)
                    c.text(ix + 22, iy + 66, "selalu siap", F["mono"], 17, muted, 1, 0.04)
                    for k in range(2):
                        arch_node(c, dict(x=ix + 22 + k * 176, y=iy + 120, w=160, h=90, kind="pod", label="model"))
                    for j in range(3):
                        f = ((t - t_inf) * 1.4 + j / 3) % 1.0
                        c.circle(users[0] + 180, iy - 4 - (iy - users[1] - 88) * f, 7, OK, min(1, f * 6, (1 - f) * 6))
            # model hops GPU pool → inference pool
            if t >= t_inf - 0.6:
                f = in_out_cubic(prog(t, t_inf - 0.6, 0.7))
                mx = gx + gw + (ipool[0] - gx - gw) * f
                ma = 1 - prog(t, t_inf + 0.2, 0.3)
                c.fill_rrect(mx - 50, gy + gh / 2 - 22, 100, 44, 22, ORANGE, ma)
                c.text(mx, gy + gh / 2 + 7, "model", F["mono_bold"], 18, (1, 1, 1, 1), ma, 0.04, align="c")
        appear(c, t, L14.start - 0.1, e - OUT, (X, 540, CW, 680), graph, blur=4, rise=20)

        def clouds(c):
            for k, (gx, gy, gw, gh) in enumerate(gors):
                gor(c, gx, gy, gw, gh, "Azure" if k == 0 else "cloud lain", "GOR " + ("kandang" if k == 0 else
                                                                                    "tandang"),
                    ok=out_back(prog(t, t_lain + 0.5, 0.4), 1.8) if (k == 1 and t >= t_lain + 0.5) else 0.0)
            u = in_out_cubic(prog(t, t_cont, 1.0))
            sx, sy, _ = shuttle_arc(gors[0][0] + 200, gors[0][1] + 60, gors[1][0] + 200, gors[1][1] + 60, 90, u)
            c.fill_rrect(sx - 70, sy - 26, 140, 52, 10, ORANGE)
            c.text(sx, sy + 7, "container", F["mono_bold"], 18, (1, 1, 1, 1), 1, 0.04, align="c")
        appear(c, t, L17.start - 0.1, e - OUT, (X, 1250, CW, 180), clouds, enter="up")
    v.add(s, e, draw)
    v.sfx("pop", L14.start, 0.4)
    for tt in t_on:
        v.sfx("pop", tt, 0.35)
    for tt in t_off:
        v.sfx("tick", tt, 0.4)
    v.sfx("whoosh", t_inf - 0.6, 0.4)
    v.sfx("pop", t_inf, 0.45)
    v.sfx("whoosh", t_cont, 0.5)
    v.sfx("chime", t_lain + 0.5, 0.6)


# ── 03 · HASIL: scalable → never idle → not locked in ──────────────────
def hasil(v, T, s, e):
    ch = v.chapter(3, "HASIL", s, e)
    L18, L19, L20 = T["L18"], T["L19"], T["L20"]
    t_sc = T.word("L18", "scalable")
    t_idle = T.word("L19", "idle")
    t_kunci = T.word("L20", "terkunci")
    head1 = Headline("Compute-nya *scalable*.")
    head2 = Headline("GPU nggak *idle*.")
    head3 = Headline("Nggak *terkunci*.")
    bw = CW - 160

    cam = v.camera
    cam.key(t_sc, zoom=0.97, dur=0.12)
    cam.key(t_sc + 0.12, zoom=1.0, dur=0.4)
    cam.focus(L19.start, (X, 600, CW, 360), zoom=1.05, dur=0.6)
    cam.reset(L20.start, dur=0.6)

    def draw(c, t):
        kicker(c, t, L18.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L18.start, L19.start - 0.15)
        head2.draw(c, t, L19.start, L20.start - 0.15)
        head3.draw(c, t, L20.start, e - OUT)
        muted = c.theme("muted", "d_muted")

        def punch(c):
            c.text(MID, 800, "compute", F["mono_med"], 32, c.theme("ink2", "d_muted"),
                   out_expo(prog(t, L18.start + 0.1, 0.4)), 0.06, align="c")
            p = prog(t, t_sc, 0.35)
            size = min(220, 220 * CW / c.measure("scalable.", F["display"], 220, -0.06)[0])
            with c.at(0, 0, 1 + 0.4 * (1 - out_expo(p)), origin=(MID, 960)):
                c.text(MID, 1010, "scalable.", F["display"], size, ORANGE, clamp(p * 3), -0.06, align="c")
            # GPU usage bar: up when training, down when done
            u = prog(t, t_sc + 0.2, 2.2)
            lvl = in_out_cubic(clamp(u * 2.2)) * (1 - in_out_cubic(clamp((u - 0.55) * 2.6)))
            c.text(X + 80, 1150, "GPU", F["mono_bold"], 19, muted, 1, 0.14)
            c.fill_rrect(X + 160, 1132, bw - 80, 22, 11, c.theme("line", "d_line"))
            c.fill_rrect(X + 160, 1132, (bw - 80) * max(0.02, lvl), 22, 11, ORANGE)
            c.text(X + 160, 1200, "nambah", F["serif"], 36, muted, clamp(u * 4) * (1 - clamp((u - 0.5) * 4)))
            c.text(X + CW - 80, 1200, "turun lagi", F["serif"], 36, muted, clamp((u - 0.6) * 4), align="r")
        appear(c, t, L18.start, L19.start - 0.15, (X, 740, CW, 500), punch, enter="up", exit="up", blur=4)

        def strip(c):
            rows = [dict(label="GPU", blocks=[(0.08, 0.3), (0.55, 0.74)], p=prog(t, L19.start, 1.2))]
            jadwal(c, X, 620, CW, rows, t, title="pemakaian GPU", playhead=prog(t, L19.start, 1.2))
            w = c.measure("idle", F["display"], 120, -0.05)[0]
            c.text(X + 40, 960, "idle", F["display"], 120, c.theme("ink", "d_ink"),
                   out_expo(prog(t, t_idle - 0.2, 0.4)) * (1 - 0.6 * prog(t, t_idle + 0.4, 0.3)), -0.05)
            strike(c, t, t_idle + 0.3, X + 30, X + 50 + w, 925, width=9)
            c.text(X + 80 + w, 950, "nggak ada GPU nyala\nnungguin jadwal", F["serif"], 36, muted,
                   out_expo(prog(t, t_idle + 0.6, 0.5)))
        appear(c, t, L19.start - 0.1, e - OUT, (X, 620, CW, 380), strip, enter="right")

        def halls(c):
            for k, lbl in enumerate(("Azure", "cloud lain")):
                gx = X + k * (CW / 2 + 12)
                tt = t_kunci - 0.2 + k * 0.25
                gor(c, gx, 1060, CW / 2 - 12, 220, lbl, ok=out_back(prog(t, tt, 0.4), 1.8) if t >= tt else 0.0)
        appear(c, t, L20.start - 0.1, e - OUT, (X, 1060, CW, 220), halls, enter="up")
    v.add(s, e, draw)
    v.sfx("pop", L18.start + 0.1, 0.4)
    v.sfx("thud", t_sc)
    v.sfx("tick", t_sc + 0.8, 0.4)
    v.sfx("whoosh", L19.start - 0.1, 0.5)
    v.sfx("tick", t_idle + 0.3, 0.6)
    v.sfx("pop", L20.start - 0.1, 0.4)
    v.sfx("pop", t_kunci - 0.2, 0.4)
    v.sfx("chime", t_kunci + 0.1, 0.6)


# ── RECAP (dark): the warehouse again → dark down to what's needed → night court ─
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L21, L22, L23 = T["L21"], T["L22"], T["L23"]
    t_lat = T.word("L22", "latihan")
    t_perlu = T.word("L23", "perlu")
    heads = [(Headline("Bukan soal *paling banyak*.", style="headline_dark"), L21.start, L22.start - 0.15),
             (Headline("Tahu *kapan*.", style="headline_dark"), L22.start, L23.start - 0.15),
             (Headline("Latihan *pas perlu*.", style="headline_dark"), L23.start, e - OUT)]
    base = 1250
    t_drill = t_perlu - 0.6

    cam = v.camera
    cam.key(s, zoom=1.15, y=900, dur=0.01)
    cam.key(L22.start, zoom=1.0, dur=1.4)

    def draw(c, t):
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def warehouse(c):
            def on(k):
                a = out_expo(prog(t, L21.start + k * 0.05, 0.3))
                if k not in KEEP:
                    a *= 1 - in_out_cubic(prog(t, t_lat - 0.6 + k * 0.08, 0.35))
                return a
            _grid(c, t, 640, on)
        appear(c, t, L21.start - 0.1, L23.start - 0.15, (X, 620, CW, 440), warehouse, enter="up", exit="up")

        def night(c):
            lt = _win(t, t_drill, t_drill + 2.0, 0.2)
            lapangan(c, X + 40, base, CW - 80, t, lights=lt, lamp_h=220)
            pemain(c, X + 190, base, 190, t, swing=0.5 + 0.5 * math.sin(t * 7) * lt)
            pelontar(c, X + CW - 170, base, 170, t)
            if lt > 0.5:
                u = (t * 1.8) % 1.0
                sx, sy, ang = shuttle_arc(X + CW - 240, base - 120, X + 220, base - 140, 120, u)
                shuttle(c, sx, sy, 22, ang)
            c.text(MID, base + 150, "pas perlu.", F["serif"], 110, ORANGE, out_expo(prog(t, t_perlu, 0.6)),
                   align="c")
        appear(c, t, L23.start - 0.1, e - OUT, (X, 820, CW, 600), night, enter="up")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    for k in range(0, 12, 2):
        v.sfx("tick", t_lat - 0.6 + k * 0.08, 0.25)
    v.sfx("pop", t_drill, 0.4)
    v.sfx("chime", t_perlu)


# ── OUTRO: series finale — 7 episodes ticked + follow ──────────────────
EPS = ["Kubernetes 10k", "Big data migration", "Serverless big data", "Event-driven", "Legacy + container",
       "Project 360", "Azure AI"]


def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L24, L25 = T["L24"], T["L25"]
    t_click = T.word("L25", "follow") + 0.4
    t_tick = [L24.start + 0.3 + k * 0.18 for k in range(7)]

    def draw(c, t):
        icons.play_logo(c, MID, 480, 70, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.4, None,
             lambda c: c.text(MID, 620, tk.BRAND_NAME, F["display"], 72, C["d_ink"], 1, -0.05, align="c"))

        def finale(c):
            y0 = 680
            c.card(X, y0, CW, 400, r=28)
            c.fill_rrect(X, y0, 14, 400, 7, ORANGE)
            c.text(X + 50, y0 + 56, "SERI BONGKAR ARSITEKTUR · SELESAI", F["mono_bold"], 20, ORANGE, 1, 0.14)
            for k, name in enumerate(EPS):
                col, row = k % 2, k // 2
                ex, ey = X + 50 + col * (CW / 2 - 20), y0 + 110 + row * 70
                p = out_back(prog(t, t_tick[k], 0.35), 1.8) if t >= t_tick[k] else 0
                c.circle(ex + 14, ey, 14, C["d_line"])
                check_badge(c, ex + 14, ey, 14, p)
                c.text(ex + 42, ey + 7, f"EP {k + 1:02d}", F["mono_bold"], 18, C["d_muted"], 1, 0.1)
                c.text(ex + 112, ey + 8, name, F["ui"], 24, C["d_ink"], 0.5 + 0.5 * clamp(p), -0.01)
            c.text(X + 50, y0 + 370, "Mau lanjutan? Tulis di komentar.", F["serif"], 34, C["d_accent"],
                   out_expo(prog(t, t_tick[-1] + 0.4, 0.5)))
        appear(c, t, L24.start, None, (X, 680, CW, 400), finale)
        fade(c, t, L25.start, None, lambda c: follow_button(c, MID, 1180, t, t_click))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L25.start - 0.2, 860, 1450), (t_click, MID + 40, 1220)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L24.start, 0.5)
    for tt in t_tick:
        v.sfx("tick", tt, 0.35)
    v.sfx("chime", t_tick[-1] + 0.2, 0.6)
    v.sfx("chime", t_click + 0.1)
