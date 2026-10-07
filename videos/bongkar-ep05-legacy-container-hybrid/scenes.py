"""Bongkar Arsitektur EP05 — Legacy dan container, hidup berdampingan. See IDENTITY.md / TREATMENT.md.

Metaphor: one food lot — ruko lama (legacy) + kios kontainer (container) behind ONE front gate (SLB) and a direction
board (Nginx). Signature move: the split-flap board flips and the visitor stream turns with it. Color: green.
Hook: specific question. No numbers (none given).
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp, mix
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, note, stamp, follow_button,
                               arch_node, series_bumper, ruko, kios, flip_sign, flip_cues, gapura, visitor, walk_path,
                               fade_ends, cover, KULINER_GREEN as GREEN)
from engine.components.infra import _h

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · MASALAH", "01 · KEPUTUSAN", "02 · DIAGRAM", "03 · HASIL", "RECAP", "OUTRO"]
OK = C["ok"]
RED = C["rec"]


def build(project):
    T = project.timing
    v = Video(duration=T["L27"].end + TAIL, bpm=128, beat_offset=0.0, series="BONGKAR ARSITEKTUR · EP 05")
    v.cover_t = T.word("L04", "berdampingan") + 0.6
    v.music = dict(key="C", mood="dreamy")           # generated score: after Eb warm (EP04) and D bright (qris)
    v.cover = lambda c: cover(c, "Lama & baru,\n*satu pintu*.", kicker="BONGKAR ARSITEKTUR · EP 05", color=GREEN,
                              badge="EP 05", tags=["legacy", "Kubernetes", "Nginx + SLB"], hero=_cover_hero)
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
    """Cover hero: the lot — ruko + stacked kios under the green direction board."""
    x, y, w, h = box
    base = y + h - 20
    ruko(c, x + 10, base, w * 0.38, min(330, h * 0.62), 0.0)
    kw = w * 0.26
    kios(c, x + w * 0.46, base, kw, kw * 0.75, 0.0, label="k8s")
    kios(c, x + w * 0.46 + kw + 16, base, kw, kw * 0.75, 0.0)
    kios(c, x + w * 0.46 + kw * 0.5, base - kw * 0.75, kw, kw * 0.75, 0.0)
    flip_sign(c, x + w * 0.3, y + 10, w * 0.7, [dict(label="lama", dest="ruko"), dict(label="baru", dest="kontainer")],
              0.0, row_h=60)


def _pop_tag(c, t, t0, x, y, label, color, h=44, align="l"):
    """Tag that pops in at t0 (scale overshoot)."""
    if t < t0:
        return
    p = out_back(prog(t, t0, 0.4), 1.6)
    with c.at(0, 0, max(0.01, p), origin=(x, y + h / 2)):
        tag(c, x, y, label, color, clamp(p * 2), align=align, h=h)


def _tag_c(c, cx, y, label, color, alpha=1.0, h=44):
    """Tag centered on cx."""
    w = c.measure(label, F["ui"], tk.T["tag"][0], tk.T["tag"][1])[0] + 30
    tag(c, cx - w / 2, y, label, color, alpha, h=h)


def _fit(c, word, size, width):
    return min(size, size * width / c.measure(word, F["display"], size, -0.06)[0])


# ── INTRO: ruko + kios side by side → one visitor, which one? → punch → bumper ─
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3, L4, L5 = T["L01"], T["L02"], T["L03"], T["L04"], T["L05"]
    t_mana = T.word("L02", "mana")
    t_mati = T.word("L03", "dimatiin")
    t_jalan = T.word("L03", "jalan")
    t_bd = T.word("L04", "berdampingan")
    headA = Headline("Lama & baru, *barengan*?")
    headB = Headline("Tanpa user *sadar*.")
    headC = Headline("Yang baru udah *jalan*.")
    base = 1180
    left = (X, 760, 380, 440)
    right = (X + 420, 760, CW - 420, 440)
    kw, kh = 210, 170
    kx = X + 440
    bump0, bump1 = e, max(e + 1.4, L5.start - 0.05)

    cam = v.camera
    cam.key(0.0, zoom=1.08, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.focus(t_mana - 0.2, (MID - 200, 1100, 400, 360), zoom=1.07, dur=0.5)
    cam.reset(L3.start, dur=0.6)
    cam.key(t_bd, zoom=0.97, dur=0.12)
    cam.key(t_bd + 0.12, zoom=1.0, dur=0.4)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "HYBRID · NGINX + SLB", GREEN)
        headA.draw(c, t, L1.start, L2.start - 0.15)
        headB.draw(c, t, L2.start, L3.start - 0.15)
        headC.draw(c, t, L3.start, L4.start - 0.15)

        def old(c):
            ruko(c, X + 20, base, 340, 400, t, label="Toko Lama")
            _pop_tag(c, t, L1.start + 0.4, X + 20, base + 30, "legacy", c.theme("ink2", "d_muted"))
            _pop_tag(c, t, t_mati, X + 20, base + 90, "belum bisa dimatiin", RED)
        appear(c, t, L1.start, L4.start - 0.15, left, old, enter="left", exit="left")

        def new(c):
            kios(c, kx, base, kw, kh, t, label="k8s")
            kios(c, kx + kw + 18, base, kw, kh, t)
            kios(c, kx + kw * 0.5 + 9, base - kh, kw, kh, t, seed=2)
            _pop_tag(c, t, L1.start + 0.6, X + CW, base + 30, "Kubernetes", GREEN, align="r")
            _pop_tag(c, t, t_jalan, X + CW, base + 90, "udah jalan", OK, align="r")
        appear(c, t, L1.start + 0.2, L4.start - 0.15, right, new, enter="right", exit="right")

        def who(c):
            f = out_cubic(prog(t, L2.start, 1.0))
            vy = 1470 - 140 * f
            visitor(c, MID, vy, 110, t, walk=1 - prog(t, L2.start + 0.9, 0.3), seed=1)
            qa = out_back(prog(t, t_mana, 0.4), 1.8) if t >= t_mana else 0
            if qa > 0:
                with c.at(0, 0, max(0.01, qa), origin=(MID, vy - 150)):
                    c.text(MID, vy - 130, "?", F["display"], 90, C["accent"], 1, align="c")
                c.text(MID - 90, vy - 60, "←", F["ui_semi"], 50, c.theme("muted", "d_muted"), qa, align="c")
                c.text(MID + 90, vy - 60, "→", F["ui_semi"], 50, c.theme("muted", "d_muted"), qa, align="c")
        fade(c, t, L2.start, L3.start - 0.15, who)

        def punch(c):
            p = prog(t, t_bd, 0.35)
            a0 = out_expo(prog(t, L4.start, 0.4))
            c.text(MID, 840, "legacy + container", F["mono_med"], 32, c.theme("ink2", "d_muted"), a0, 0.06, align="c")
            c.line(MID, 880, MID, 880 + 70 * a0, c.theme("faint", "d_line"), 4)
            size = _fit(c, "berdampingan.", 140, CW)
            with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, 1060)):
                c.text(MID, 1100, "berdampingan.", F["display"], size, GREEN, clamp(p * 3), -0.06, align="c")
        appear(c, t, L4.start, e - OUT, (X, 780, CW, 400), punch, enter="up", blur=4)
    v.add(s, e + 0.4, draw)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 5, "Conglomeration hybrid infra", GREEN),
          z=100)
    v.sfx("whoosh", L1.start, 0.5)
    v.sfx("whoosh", L1.start + 0.2, 0.4)
    v.sfx("pop", L1.start + 0.4, 0.4)
    v.sfx("pop", L1.start + 0.6, 0.4)
    v.sfx("pop", t_mana, 0.5)
    v.sfx("pop", t_mati, 0.5)
    v.sfx("pop", t_jalan, 0.5)
    v.sfx("whoosh", L4.start - 0.1, 0.5)
    v.sfx("thud", t_bd)
    v.sfx("whoosh", bump0, 0.8)
    v.sfx("whoosh", bump1 - 0.35, 0.5)


# ── 00 · MASALAH: one lot, three doors, one flooded ────────────────────
def masalah(v, T, s, e):
    ch = v.chapter(0, "MASALAH", s, e)
    L5, L6, L7, L8, L9 = T["L05"], T["L06"], T["L07"], T["L08"], T["L09"]
    t_ruko = T.word("L06", "ruko")
    t_kios = T.word("L07", "kios")
    t_tambah = T.word("L07", "ditambah")
    t_pindah = T.word("L07", "dipindah")
    t_beda = T.word("L08", "beda")
    t_banjir = T.word("L09", "kebanjiran")
    t_goyang = T.word("L09", "goyang")
    heads = [(Headline("Satu *lahan kuliner*."), L5.start, L6.start - 0.15),
             (Headline("Kiri: *ruko lama*."), L6.start, L7.start - 0.15),
             (Headline("Kanan: *kios kontainer*."), L7.start, L8.start - 0.15),
             (Headline("Pintunya *beda-beda*."), L8.start, L9.start - 0.15),
             (Headline("Satu *kebanjiran*."), L9.start, e - OUT)]
    box = (X, 560, CW, 800)
    gnd = 1250
    kw, kh = 190, 150
    doors = [X + 150, MID, X + CW - 150]
    t_door = [t_beda + k * 0.15 for k in range(3)]
    crowd = [(doors[0] + (_h(k, 3) - 0.5) * 200, 880 + _h(k, 4) * 20, t_banjir - 0.6 + k * 0.12) for k in range(11)]

    cam = v.camera
    cam.focus(t_ruko - 0.1, (X, 880, 380, 380), zoom=1.06, dur=0.6)
    cam.focus(t_kios - 0.1, (X + 380, 900, CW - 380, 360), zoom=1.05, dur=0.6)
    cam.reset(L8.start, dur=0.6)
    cam.focus(t_banjir - 0.2, (X, 620, 420, 300), zoom=1.1, dur=0.5)
    cam.reset(t_goyang + 0.2, dur=0.6)

    def draw(c, t):
        kicker(c, t, L5.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        muted = c.theme("muted", "d_muted")

        def lot(c):
            x, y, w, h = box
            c.card(x, y, w, h, r=30)
            c.text(x + 30, y + 50, "LAHAN KULINER", F["mono_bold"], 19, muted, 1, 0.16)
            c.line(x + 30, gnd, x + w - 30, gnd, c.theme("faint", "d_line"), 5)
            ra = out_expo(prog(t, t_ruko, 0.5))
            hot = clamp(prog(t, t_goyang - 0.2, 0.3))
            if ra > 0:
                with c.at(0, 30 * (1 - ra), 1, origin=(0, 0)):
                    ruko(c, x + 40, gnd, 300, 340, t, door=0.7, hot=hot, alpha=ra)
            for k, (kx0, tt) in enumerate(((x + 400, t_kios), (x + 610, t_kios + 0.15))):
                a = out_expo(prog(t, tt, 0.4))
                if a > 0:
                    kios(c, kx0, gnd, kw, kh, t, label="k8s" if k == 0 else None, alpha=a, seed=k)
            if t >= t_tambah:
                drop = out_cubic(prog(t, t_tambah, 0.45))
                slide = in_out_cubic(prog(t, t_pindah, 0.6))
                kx0 = x + 400 + 210 * slide
                kios(c, kx0, gnd - kh - 260 * (1 - drop), kw, kh, t, alpha=clamp(drop * 3), seed=5)
            # three doors on top, the crowd at door A
            for k, dx in enumerate(doors):
                if t >= t_door[k]:
                    a = out_back(prog(t, t_door[k], 0.4), 1.5)
                    with c.at(0, 0, max(0.01, a), origin=(dx, 800)):
                        gapura(c, dx, 800, 150, 90, t, label=f"PINTU {'ABC'[k]}", booth=False,
                               color=RED if (k == 0 and t >= t_banjir) else GREEN)
            for k, (cx_, cy_, tt) in enumerate(crowd):
                if t >= tt:
                    visitor(c, cx_, cy_, 50, t, RED, walk=0.4, alpha=out_expo(prog(t, tt, 0.3)), seed=k)
            if t >= t_banjir:
                for k in (1, 2):
                    visitor(c, doors[k] + 30, 880, 50, t, muted, walk=0.0, alpha=out_expo(prog(t, t_banjir, 0.4)),
                            seed=k + 20)
            _pop_tag(c, t, t_banjir + 0.2, x + 40, 1280, "pintu A: kebanjiran", RED)
            _pop_tag(c, t, t_goyang, x + w - 40, 1280, "lemot · error", RED, align="r")
        appear(c, t, L5.start - 0.1, e - OUT, box, lot, enter="up")
        fade(c, t, t_ruko + 0.3, L8.start - 0.1,
             lambda c: note(c, X + CW - 40, 760, "ini legacy-nya", prog(t, t_ruko + 0.4, 0.9),
                            arrow_to=(X + 300, 920), align="r", size=40))
    v.add(s, e, draw)
    v.sfx("whoosh", L5.start - 0.1, 0.6)
    v.sfx("pop", t_ruko, 0.5)
    v.sfx("pop", t_kios, 0.4)
    v.sfx("pop", t_kios + 0.15, 0.4)
    v.sfx("pop", t_tambah, 0.4)
    v.sfx("whoosh", t_pindah, 0.4)
    for tt in t_door:
        v.sfx("pop", tt, 0.35)
    for _, _, tt in crowd[::2]:
        v.sfx("tick", tt, 0.3)
    v.sfx("thud", t_goyang, 0.7)


# ── 01 · KEPUTUSAN: one gate (SLB) + a direction board (Nginx) ─────────
def keputusan(v, T, s, e):
    ch = v.chapter(1, "KEPUTUSAN", s, e)
    L10, L11, L12, L13, L14 = T["L10"], T["L11"], T["L12"], T["L13"], T["L14"]
    t_satu = T.word("L10", "satu")
    t_satpam = T.word("L11", "satpam")
    t_load = T.word("L11", "load")
    t_papan = T.word("L12", "papan")
    t_nginx = T.word("L12", "Nginx")
    t_ruko = T.word("L13", "ruko")
    t_kont = T.word("L13", "kontainer")
    t_one = T.word("L14", "satu")
    heads = [(Headline("*Satu* pintu depan."), L10.start, L11.start - 0.15),
             (Headline("Satpam = *load balancer*."), L11.start, L12.start - 0.15),
             (Headline("Papan arah = *Nginx*."), L12.start, L13.start - 0.15),
             (Headline("Lama ke ruko, baru ke *kontainer*."), L13.start, L14.start - 0.15),
             (Headline("Kelihatannya *satu pintu*."), L14.start, e - OUT)]
    gb, gw, gh = 760, 360, 150
    sign = (MID - 260, 800, 520)
    rows = [dict(label="menu lama", dest="ruko", prev=" ", t_flip=t_ruko - 0.3),
            dict(label="menu baru", dest="kontainer", prev=" ", t_flip=t_kont - 0.3, stuck=4)]
    t_route = t_ruko - 0.3
    rb, kb = 1340, 1340
    dest = {0: (X + 170, rb), 1: (X + CW - 200, kb)}
    side = {0: MID - 300, 1: MID + 300}
    gap, dur = 0.42, 3.0
    t0 = t_satpam
    n = int(max(0, (e - t0)) / gap) + 1
    walkers = []
    for i in range(n):
        ts = t0 + i * gap
        lane = i % 2
        new = _h(i, 11) > 0.5
        go = (1 if new else 0) if ts >= t_route - 1.2 else lane
        walkers.append((ts, lane, go, new and ts >= t_route - 1.2))

    cam = v.camera
    cam.focus(L10.start, (MID - 260, 560, 520, 260), zoom=1.06, dur=0.7)
    cam.reset(t_load + 0.3, dur=0.7)
    cam.focus(t_papan - 0.1, (sign[0], sign[1], sign[2], 220), zoom=1.07, dur=0.6)
    cam.reset(t_kont + 0.3, dur=0.6)
    cam.key(t_one - 0.1, zoom=0.95, dur=0.8)
    cam.reset(e - 0.6, dur=0.5)

    def draw(c, t):
        kicker(c, t, L10.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        dim = 1 - 0.6 * in_out_cubic(prog(t, t_one, 0.5))
        muted = c.theme("muted", "d_muted")

        def lot(c):
            with c.group(dim):
                ruko(c, X + 20, rb, 300, 300, t, label="Toko Lama")
                kios(c, X + CW - 400, kb, 180, 150, t, label="k8s")
                kios(c, X + CW - 200, kb, 180, 150, t, seed=3)
                for ts, lane, go, new in walkers:
                    f = (t - ts) / dur
                    if not 0 <= f <= 1:
                        continue
                    lx = MID + (-80 if lane == 0 else 80)
                    pts = [(lx, gb - 40), (lx, gb + 30), (side[go], gb + 30), (side[go], 1100), dest[go]]
                    px, py = walk_path(pts, f)
                    visitor(c, px, py, 56, t, GREEN if new else muted, alpha=fade_ends(f), seed=int(ts * 10))
        appear(c, t, L10.start + 0.2, e - OUT, (X, 900, CW, 460), lot, enter="up")

        def gate(c):
            cur = [w for w in walkers if 0 <= t - w[0] < 0.4]
            lane = cur[-1][1] if cur and t >= t_satpam else None
            gapura(c, MID, gb, gw, gh, t, label="PINTU DEPAN", lane=lane)
        appear(c, t, L10.start - 0.1, e - OUT, (MID - 320, gb - gh - 80, 640, gh + 80), gate, enter="pop")
        _pop_tag(c, t, t_load, X + CW, gb - 60, "SLB", GREEN, align="r")

        def board(c):
            with c.group(dim):
                flip_sign(c, sign[0], sign[1], sign[2], rows, t, row_h=64, title="NGINX")
        appear(c, t, t_papan - 0.1, e - OUT, (sign[0], sign[1], sign[2], 200), board, enter="down")
        _pop_tag(c, t, t_one, X + CW, gb - gh - 10, "user cuma lihat ini", C["accent"], align="r")
    v.add(s, e, draw)
    v.sfx("pop", L10.start - 0.1, 0.5)
    v.sfx("thud", t_satu, 0.6)
    for ts, *_ in walkers[:10]:
        v.sfx("tick", ts, 0.25)
    v.sfx("pop", t_load, 0.5)
    v.sfx("whoosh", t_papan - 0.1, 0.5)
    v.sfx("pop", t_nginx, 0.4)
    for r in rows:
        for tt in flip_cues(r):
            v.sfx("tick", tt, 0.3)
    v.sfx("whoosh", t_one - 0.1, 0.5)


# ── 02 · DIAGRAM: users → SLB → nginx ×3 → legacy | Kubernetes ─────────
def diagram(v, T, s, e):
    ch = v.chapter(2, "DIAGRAM", s, e)
    L15, L16, L17, L18, L19 = T["L15"], T["L16"], T["L17"], T["L18"], T["L19"]
    t_slb = T.word("L15", "SLB")
    t_ngx = T.word("L16", "Nginx")
    t_leg = T.word("L17", "legacy")
    t_k8s = T.word("L17", "Kubernetes")
    t_mana = T.word("L18", "mana")
    t_papan = T.word("L19", "papannya")
    heads = [(Headline("Masuk lewat *SLB*."), L15.start, L16.start - 0.15),
             (Headline("Dibagi ke *Nginx*."), L16.start, L17.start - 0.15),
             (Headline("Path lama, path *baru*."), L17.start, L18.start - 0.15),
             (Headline("Satpam *kedua*."), L18.start, L19.start - 0.15),
             (Headline("Ganti *papannya*."), L19.start, e - OUT)]
    users = (MID - 200, 560, 400, 86)
    slb = (MID - 200, 690, 400, 86)
    NW = (CW - 48) / 3
    ngx = [(X + k * (NW + 24), 830, NW, 96) for k in range(3)]
    EW = (CW - 24) / 2
    leg = (X, 1000, EW, 250)
    k8s = (X + EW + 24, 1000, EW, 250)
    board = (X, 1290, CW)
    row = dict(label="/promo", dest="kubernetes", prev="legacy", t_flip=t_papan - 0.2)
    t_ngx_in = [t_ngx - 0.1 + k * 0.15 for k in range(3)]
    gap, dur = 0.34, 1.6
    t0 = L15.start + 0.3

    cam = v.camera
    cam.focus(L15.start + 0.1, (MID - 220, 560, 440, 230), zoom=1.07, dur=0.6)
    cam.focus(L16.start, (X, 690, CW, 240), zoom=1.05, dur=0.6)
    cam.reset(L17.start, dur=0.6)
    cam.focus(t_mana - 0.4, (ngx[1][0] - 60, 800, NW + 120, 200), zoom=1.08, dur=0.5)
    cam.focus(L19.start, (X, 1150, CW, 260), zoom=1.06, dur=0.6)
    cam.reset(e - 0.9, dur=0.5)

    def request(t, i):
        """(x, y, color, alpha) of request i at time t, or None."""
        ts = t0 + i * gap
        f = (t - ts) / dur
        if not 0 <= f <= 1:
            return None
        promo = i % 4 == 0
        new = _h(i, 7) > 0.55 or (promo and ts >= t_papan - 0.6)
        k = i % 3
        nx = ngx[k][0] + NW / 2
        bx = (k8s if new else leg)
        pts = [(MID, users[1] + 90), (MID, slb[1] + 43)]
        if ts >= t_ngx - 0.6:
            pts += [(nx, ngx[k][1] + 48)]
            if ts >= t_leg - 0.6:
                pts += [(bx[0] + bx[2] / 2, bx[1] + 40)]
        x, y = walk_path(pts, f)
        col = GREEN if new else C["muted"]
        return x, y, col, fade_ends(f)

    def draw(c, t):
        kicker(c, t, L15.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        faint, muted, ink = c.theme("faint", "d_line"), c.theme("muted", "d_muted"), c.theme("ink", "d_ink")

        def graph(c):
            arch_node(c, dict(x=users[0], y=users[1], w=400, h=86, kind="users", label="users",
                              a=out_expo(prog(t, L15.start, 0.4))))
            a_s = out_expo(prog(t, t_slb, 0.4))
            if a_s > 0:
                c.line(MID, users[1] + 88, MID, slb[1] - 2, faint, 5, a_s)
            arch_node(c, dict(x=slb[0], y=slb[1], w=400, h=86, kind="lb", label="SLB", a=a_s))
            for k, (nx, ny, nw, nh) in enumerate(ngx):
                a = out_expo(prog(t, t_ngx_in[k], 0.4))
                if a <= 0.01:
                    continue
                c.line(MID, slb[1] + 88, nx + nw / 2, ny - 2, faint, 4, a)
                hit = k == 1 and t >= t_mana - 0.3
                arch_node(c, dict(x=nx, y=ny, w=nw, h=nh, kind="svc", label=f"nginx-{k + 1}", a=a))
                if hit:
                    m = 16 * out_back(prog(t, t_mana, 0.3), 1.6) if t >= t_mana else 0
                    c.line(nx + nw - 34 - m, ny + 30 - m, nx + nw - 34 + m, ny + 30 + m, RED, 6)
                    c.line(nx + nw - 34 - m, ny + 30 + m, nx + nw - 34 + m, ny + 30 - m, RED, 6)
            for (bx, by, bw, bh), tt, name, sub in ((leg, t_leg, "LEGACY", "monolith"),
                                                    (k8s, t_k8s, "KUBERNETES", "container")):
                a = out_expo(prog(t, tt - 0.1, 0.45))
                if a <= 0.01:
                    continue
                with c.group(a):
                    for k in range(3):
                        c.line(ngx[k][0] + NW / 2, ngx[k][1] + 98, bx + bw / 2, by - 2, faint, 3, 0.6)
                    c.card(bx, by, bw, bh, r=24)
                    c.text(bx + 24, by + 42, name, F["mono_bold"], 19, GREEN if name == "KUBERNETES" else muted, 1,
                           0.16)
                    c.text(bx + 24, by + 72, sub, F["mono"], 17, muted, 1, 0.04)
                    if name == "LEGACY":
                        ruko(c, bx + bw - 190, by + bh - 16, 160, 170, t, label="lama")
                    else:
                        for j in range(3):
                            kios(c, bx + 24 + j * ((bw - 48) / 3), by + bh - 16, (bw - 48) / 3 - 10, 100, t,
                                 seed=j + 7)
            # request dots
            i0 = max(0, int((t - t0 - dur) / gap))
            for i in range(i0, int((t - t0) / gap) + 1):
                r = request(t, i)
                if r:
                    c.circle(r[0], r[1], 8, r[2], r[3])
            # the rejected one
            if t >= t_mana - 1.0:
                f = clamp((t - (t_mana - 1.0)) / 0.8)
                x, y = walk_path([(MID, users[1] + 90), (MID, slb[1] + 43), (ngx[1][0] + NW / 2, ngx[1][1] + 10)], f)
                c.circle(x, y, 10, RED, 1 - prog(t, t_mana + 0.5, 0.3))
            _pop_tag(c, t, t_mana + 0.1, X + CW, 945, "access rule · ditolak", RED, align="r")
        appear(c, t, L15.start - 0.1, e - OUT, (X, 540, CW, 720), graph, blur=4, rise=20)
        appear(c, t, L19.start - 0.1, e - OUT, (board[0], board[1], board[2], 100),
               lambda c: flip_sign(c, board[0], board[1], board[2], [row], t, row_h=76), enter="up")
    v.add(s, e, draw)
    v.sfx("pop", L15.start, 0.4)
    v.sfx("pop", t_slb, 0.5)
    for tt in t_ngx_in:
        v.sfx("pop", tt, 0.35)
    v.sfx("pop", t_leg - 0.1, 0.45)
    v.sfx("pop", t_k8s - 0.1, 0.45)
    v.sfx("thud", t_mana, 0.6)
    v.sfx("whoosh", L19.start - 0.1, 0.4)
    for tt in flip_cues(row):
        v.sfx("tick", tt, 0.3)
    v.sfx("chime", t_papan + 0.6, 0.6)


# ── 03 · HASIL: queues even out → line calms → one guarded gate ────────
def hasil(v, T, s, e):
    ch = v.chapter(3, "HASIL", s, e)
    L20, L21, L22 = T["L20"], T["L21"], T["L22"]
    t_rata = T.word("L20", "rata")
    t_stabil = T.word("L21", "stabil")
    t_rapi = T.word("L22", "rapi")
    head1 = Headline("Kebagi *rata*.")
    head2 = Headline("Lebih *stabil*.")
    head3 = Headline("Akses lebih *rapi*.")
    card = (X, 600, CW, 680)
    before = (0.95, 0.18, 0.1)
    bx = [X + CW * f for f in (0.2, 0.5, 0.8)]
    bbase, bmax = 1000, 300
    chart = (X + 40, 1070, CW - 80, 150)

    cam = v.camera
    cam.key(t_rata, zoom=0.97, dur=0.12)
    cam.key(t_rata + 0.12, zoom=1.0, dur=0.4)
    cam.focus(L21.start, chart, zoom=1.06, dur=0.6)
    cam.reset(L22.start - 0.1, dur=0.5)

    def draw(c, t):
        kicker(c, t, L20.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L20.start, L21.start - 0.15)
        head2.draw(c, t, L21.start, L22.start - 0.15)
        head3.draw(c, t, L22.start, e - OUT)
        muted = c.theme("muted", "d_muted")

        def queues(c):
            x, y, w, h = card
            c.card(x, y, w, h, r=30)
            c.text(x + 30, y + 50, "ANTREAN TIAP PINTU", F["mono_bold"], 19, muted, 1, 0.16)
            ev = in_out_cubic(prog(t, t_rata - 0.2, 0.8))
            for k in range(3):
                hgt = bmax * (before[k] + (0.42 - before[k]) * ev)
                col = mix(RED, GREEN, ev) if k == 0 else GREEN
                c.fill_rrect(bx[k] - 60, bbase - hgt, 120, hgt, 14, col, 0.85)
                c.text(bx[k], bbase + 40, f"PINTU {'ABC'[k]}", F["mono_bold"], 19, muted, 1, 0.1, align="c")
            # jittery line calms down
            cx_, cy_, cw_, ch_ = chart
            c.text(cx_, cy_ - 12, "response time", F["mono_med"], 18, muted, 1, 0.06)
            calm = in_out_cubic(prog(t, t_stabil - 0.4, 1.0))
            col = mix(RED, GREEN, calm)
            ctx = c.ctx
            ctx.new_path()
            n = 60
            for j in range(n + 1):
                u = j / n
                amp = (1 - 0.9 * calm) * ch_ * 0.4
                yy = cy_ + ch_ / 2 + amp * math.sin(u * 37 + t * 3) * (0.4 + 0.6 * abs(math.sin(u * 11)))
                (ctx.move_to if j == 0 else ctx.line_to)(cx_ + cw_ * u, yy)
            c.src(col)
            ctx.set_line_width(5)
            ctx.stroke()
            stamp(c, cx_ + cw_ - 150, cy_ + ch_ / 2, "STABIL", prog(t, t_stabil, 0.35), color=GREEN, rot=-0.1, size=64)
        appear(c, t, L20.start - 0.1, L22.start - 0.15, card, queues, enter="up", exit="left")

        def gate(c):
            gapura(c, MID, 1150, 440, 230, t, label="SATU PINTU", lane=int(t * 2.5) % 2)
            _tag_c(c, MID, 1200, "semua lewat sini · access rule", GREEN, out_expo(prog(t, t_rapi, 0.4)))
        appear(c, t, L22.start - 0.1, e - OUT, (MID - 340, 760, 680, 500), gate, enter="right")
    v.add(s, e, draw)
    v.sfx("whoosh", L20.start - 0.1, 0.5)
    v.sfx("whoosh", t_rata - 0.2, 0.4)
    v.sfx("chime", t_rata + 0.5, 0.6)
    v.sfx("thud", t_stabil)
    v.sfx("whoosh", L22.start - 0.1, 0.5)
    v.sfx("pop", t_rapi, 0.5)


# ── RECAP (dark): not all at once · one gate · the board flips mid-stride ─
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L23, L24, L25 = T["L23"], T["L24"], T["L25"]
    t_seka = T.word("L23", "sekaligus")
    t_satu = T.word("L24", "satu")
    t_peduli = T.word("L25", "peduli")
    t_sampai = T.word("L25", "sampai")
    heads = [(Headline("Nggak harus *sekaligus*.", style="headline_dark"), L23.start, L24.start - 0.15),
             (Headline("Pintunya *satu*.", style="headline_dark"), L24.start, L25.start - 0.15),
             (Headline("Pesanannya *sampai*.", style="headline_dark"), L25.start, e - OUT)]
    sign = (X + 130, 700, CW - 260)
    t_mid = t_peduli + 0.3
    rows = [dict(label="/promo", dest="kontainer", prev="ruko", t_flip=t_seka - 0.1),
            dict(label="/akun", dest="kontainer", prev="ruko", t_flip=t_mid),
            dict(label="/laporan", dest="ruko")]
    base = 1250
    walk0 = L25.start - 0.2
    path = [(MID, 1450), (MID, 1330), (X + CW - 250, 1300)]

    cam = v.camera
    cam.key(s, zoom=1.15, y=1000, dur=0.01)
    cam.key(L24.start, zoom=1.0, dur=1.4)

    def draw(c, t):
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def lot(c):
            ruko(c, X + 130, base, 260, 280, t, label="Toko Lama")
            kios(c, X + CW - 400, base, 160, 140, t, label="k8s")
            kios(c, X + CW - 215, base, 160, 140, t, seed=2)
            flip_sign(c, sign[0], sign[1], sign[2], rows, t, row_h=64, title="NGINX")
            ga = out_expo(prog(t, t_satu - 0.2, 0.6))
            if ga > 0:
                gapura(c, MID, base + 30, CW - 80, 660, t, label="PINTU DEPAN", booth=False, alpha=ga)
            if t >= walk0:
                f = prog(t, walk0, 2.6)
                px, py = walk_path(path, f)
                visitor(c, px, py, 90, t, C["d_ink"], walk=1 - prog(t, walk0 + 2.5, 0.2), seed=4)
            if t >= t_sampai:
                p = out_back(prog(t, t_sampai, 0.4), 1.8)
                ox, oy = X + CW - 250, 1160
                with c.at(0, 0, max(0.01, p), origin=(ox, oy)):
                    c.circle(ox, oy, 30, OK)
                    icons.check(c, ox, oy, 25, (1, 1, 1, 1), 4)
            c.text(X + 130, 1420, "dia nggak berhenti", F["serif"], 38, C["d_muted"],
                   out_expo(prog(t, t_mid + 0.6, 0.5)))
        appear(c, t, L23.start - 0.1, e - OUT, (X, 560, CW, 900), lot, enter="up")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    for r in rows:
        for tt in flip_cues(r):
            v.sfx("tick", tt, 0.3)
    v.sfx("whoosh", t_satu - 0.2, 0.6)
    v.sfx("chime", t_sampai)


# ── OUTRO: logo + EP06 teaser + follow ─────────────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L26, L27 = T["L26"], T["L27"]
    t_click = T.word("L27", "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, GREEN)
            c.text(X + 50, 892, "EPISODE BERIKUTNYA · EP 06", F["mono_bold"], 20, GREEN, 1, 0.16)
            c.text(X + 50, 962, "Customer 360", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "Data pelanggan dalam milidetik", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L26.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L27.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "Seri Bongkar Arsitektur", F["ui"], 28,
                                                          C["d_muted"], 1, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L27.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L26.start, 0.5)
    v.sfx("chime", t_click + 0.1)
