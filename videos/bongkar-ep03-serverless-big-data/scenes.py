"""Bongkar Arsitektur EP03 — Ganti stack big data jadi serverless. See IDENTITY.md / TREATMENT.md.

Metaphor: own kitchen vs cloud kitchen. Signature move: a burner ignites when a ticket (job) lands and dies to nothing
when the job is done. Signature color: orange. Hook: before/after split. No numbers (none given).
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_cubic, in_out_cubic, clamp, mix
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, note, stamp, strike, moon,
                               follow_button, arch_node, series_bumper, burner, oven, ticket_rail, dag_flow,
                               dag_state, lake_pantry, server_rack, ORANGE)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · MASALAH", "01 · KEPUTUSAN", "02 · DIAGRAM", "03 · HASIL", "RECAP", "OUTRO"]
OK = C["ok"]


def build(project):
    T = project.timing
    v = Video(duration=T["L24"].end + TAIL, bpm=128, beat_offset=0.0, series="BONGKAR ARSITEKTUR · EP 03")
    v.cover_t = T.word("L04", "serverless") + 0.6
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


# ── INTRO: before/after split → serverless punch → bumper ──────────────
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3, L4, L5 = T["L01"], T["L02"], T["L03"], T["L04"], T["L05"]
    t_jaga = T.word("L01", "dijagain")
    t_now = T.word("L02", "sekarang")
    t_sama = T.word("L02", "sama")
    t_siapa = T.word("L03", "siapa")
    t_srv = T.word("L04", "serverless")
    headA = Headline("Dulu: *dijagain* tiap hari.")
    headB = Headline("Sekarang: *nggak ada* yang diurus.")
    headC = Headline("Yang beda: *siapa yang ngurus*.")
    PW = (CW - 24) / 2
    left = (X, 600, PW, 760)
    right = (X + PW + 24, 600, PW, 760)
    chores = [("patch", t_jaga - 0.1), ("restart", t_jaga + 0.15), ("monitoring", t_jaga + 0.4)]
    bump0, bump1 = e, max(e + 1.4, L5.start - 0.05)

    cam = v.camera
    cam.key(0.0, zoom=1.08, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.focus(t_sama - 0.1, right, zoom=1.06, dur=0.5)
    cam.reset(L3.start, dur=0.6)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "BIG DATA · ALIBABA CLOUD", ORANGE)
        headA.draw(c, t, L1.start, L2.start - 0.15)
        headB.draw(c, t, L2.start, L3.start - 0.15)
        headC.draw(c, t, L3.start, L4.start - 0.15)

        def same_row(c, x, y):
            a = out_expo(prog(t, L3.start, 0.4))
            tag(c, x, y, "data", C["accent"], a, h=40)
            tag(c, x + 92, y, "job", C["accent"], a, h=40)

        def dulu(c):
            x, y, w, h = left
            c.card(x, y, w, h, r=28)
            c.text(x + 28, y + 52, "DULU", F["mono_bold"], 20, c.theme("muted", "d_muted"), 1, 0.18)
            server_rack(c, x + 28, y + 84, w - 56, 330, t, units=5, seed=2)
            for k, (lbl, tt) in enumerate(chores):
                _pop_tag(c, t, tt, x + 28, y + 440 + k * 56, lbl, ORANGE, h=40)
            same_row(c, x + 28, y + 628)
            _pop_tag(c, t, t_siapa, x + 28, y + 690, "kamu yang ngurus", C["rec"])

        def now(c):
            x, y, w, h = right
            c.card(x, y, w, h, r=28)
            c.text(x + 28, y + 52, "SEKARANG", F["mono_bold"], 20, c.theme("muted", "d_muted"), 1, 0.18)
            server_rack(c, x + 28, y + 84, w - 56, 330, t, dashed=True)
            c.text(x + w / 2, y + 268, "kosong.", F["display"], 64, c.theme("ink", "d_ink"),
                   out_expo(prog(t, t_now + 0.3, 0.5)), -0.04, align="c")
            p = out_back(prog(t, t_sama, 0.45), 1.8) if t >= t_sama else 0
            if p > 0:
                with c.at(0, 0, max(0.01, p), origin=(x + w / 2, y + 340)):
                    c.circle(x + w / 2, y + 340, 26, OK)
                    icons.check(c, x + w / 2, y + 340, 22, (1, 1, 1, 1), 3.5)
            same_row(c, x + 28, y + 628)
            _pop_tag(c, t, t_siapa + 0.3, x + 28, y + 690, "cloud yang ngurus", OK)

        appear(c, t, L1.start + 0.1, L4.start - 0.15, left, dulu, enter="left", exit="left")
        appear(c, t, t_now - 0.1, L4.start - 0.15, right, now, enter="right", exit="right")

        def punch(c):
            p = prog(t, t_srv, 0.35)
            a0 = out_expo(prog(t, L4.start, 0.4))
            c.text(MID, 840, "stack big data legacy", F["mono_med"], 30, c.theme("ink2", "d_muted"), a0, 0.06,
                   align="c")
            c.line(MID, 880, MID, 880 + 70 * a0, c.theme("faint", "d_line"), 4)
            with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, 1060)):
                c.text(MID, 1100, "serverless.", F["display"], 140, ORANGE, clamp(p * 3), -0.06, align="c")
        appear(c, t, L4.start, e - OUT, (X, 780, CW, 400), punch, enter="up", blur=4)
    v.add(s, e + 0.4, draw)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 3, "Next-gen big data ecosystem",
                                                    ORANGE), z=100)
    v.sfx("whoosh", L1.start + 0.1, 0.5)
    for _, tt in chores:
        v.sfx("pop", tt, 0.4)
    v.sfx("whoosh", t_now - 0.1, 0.5)
    v.sfx("thud", t_sama, 0.6)
    v.sfx("pop", L3.start, 0.4)
    v.sfx("pop", t_siapa, 0.5)
    v.sfx("pop", t_siapa + 0.3, 0.5)
    v.sfx("whoosh", L4.start - 0.1, 0.5)
    v.sfx("thud", t_srv)
    v.sfx("whoosh", bump0, 0.8)
    v.sfx("whoosh", bump1 - 0.35, 0.5)


# ── 00 · MASALAH: own kitchen, burning nonstop ─────────────────────────
JOBS = ["laporan", "dashboard", "rekap", "query", "export", "join", "agregasi"]


def masalah(v, T, s, e):
    ch = v.chapter(0, "MASALAH", s, e)
    L5, L7, L8 = T["L05"], T["L07"], T["L08"]
    t_rawat = T.word("L06", "dirawat")
    t_gas = T.word("L06", "gasnya")
    t_walau = T.word("L06", "walau")
    t_legacy = T.word("L07", "legacy")
    t_idle = T.word("L07", "idle")
    t_pes = T.word("L08", "pesanan")
    t_blu = T.word("L08", "membludak")
    t_kew = T.word("L08", "kewalahan")
    t_nambah = T.word("L08", "nambah")
    head1 = Headline("Bayangin *dapur sendiri*.")
    head2 = Headline("Itu node *legacy*.")
    head3 = Headline("Pesanan *membludak*?")
    box = (X, 560, CW, 780)
    rail_y = 650
    sx = [X + CW * f for f in (0.2, 0.5, 0.8)]
    sy, ss = 1060, 220
    ign = [L5.start + 0.5 + k * 0.25 for k in range(3)]
    flood = [(X + 80 + k * 108, t_pes + k * 0.16, 0.26 if k == 4 else (((k * 37) % 7) / 7 - 0.5) * 0.12)
             for k in range(7)]

    cam = v.camera
    cam.focus(L5.start + 0.4, (X, 900, CW, 300), zoom=1.05, dur=1.2)
    cam.focus(t_blu, (X, 640, CW, 240), zoom=1.08, dur=0.5)
    cam.reset(t_nambah, dur=0.6)

    def draw(c, t):
        kicker(c, t, L5.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L5.start, L7.start - 0.15)
        head2.draw(c, t, L7.start, L8.start - 0.15)
        head3.draw(c, t, L8.start, e - OUT)
        hot = in_out_cubic(prog(t, t_kew - 0.3, 0.6))
        relabel = out_expo(prog(t, t_legacy, 0.5))
        muted = c.theme("muted", "d_muted")

        def kitchen(c):
            x, y, w, h = box
            c.card(x, y, w, h, r=30)
            c.text(x + 30, y + 50, "DAPUR SENDIRI", F["mono_bold"], 19, muted, 1, 0.16)
            tickets = [dict(x=tx, title=f"job-{k + 1:02d}", lines=(JOBS[k],), p=prog(t, tt, 0.4), rot=rot)
                       for k, (tx, tt, rot) in enumerate(flood)]
            ticket_rail(c, x + 30, rail_y, w - 60, tickets, tw=130, th=180)
            a_empty = out_expo(prog(t, t_walau, 0.4)) * (1 - prog(t, t_pes - 0.2, 0.2))
            c.text(x + w / 2, rail_y + 70, "nggak ada pesanan", F["serif"], 40, muted, a_empty, align="c")
            for k in range(3):
                fire = out_back(prog(t, ign[k], 0.4), 1.4) if t >= ign[k] else 0
                burner(c, sx[k], sy, ss, fire, t, seed=k, hot=hot)
                ly = sy + ss * 0.34 + 36
                c.text(sx[k], ly, f"kompor {k + 1}", F["mono_med"], 19, muted, 1 - relabel, 0.08, align="c")
                c.text(sx[k], ly, f"node-{k + 1}", F["mono_bold"], 19, ORANGE, relabel, 0.08, align="c")
            # gas gauge (L05–L07) → '+ node baru' crawl (L08)
            gy = 1200
            ga = 1 - prog(t, L8.start, 0.3)
            if ga > 0:
                lvl = 1 - 0.6 * in_out_cubic(prog(t, t_gas, 2.5))
                c.text(x + 40, gy + 8, "GAS", F["mono_bold"], 18, muted, ga, 0.14)
                c.fill_rrect(x + 110, gy - 6, w - 150, 14, 7, c.theme("line", "d_line"), ga)
                c.fill_rrect(x + 110, gy - 6, (w - 150) * lvl, 14, 7, ORANGE, ga)
            na = out_expo(prog(t, t_nambah, 0.4))
            if na > 0:
                crawl = 0.06 + 0.1 * prog(t, t_nambah, 2.5)
                c.text(x + 40, gy + 8, "+ NODE BARU", F["mono_bold"], 18, C["rec"], na, 0.14)
                c.fill_rrect(x + 210, gy - 6, w - 250, 14, 7, c.theme("line", "d_line"), na)
                c.fill_rrect(x + 210, gy - 6, (w - 250) * crawl, 14, 7, C["rec"], na)
                c.text(x + w - 40, gy + 64, "nunggu…", F["serif"], 38, muted, na, align="r")
            ta = 1 - prog(t, L7.start, 0.3)
            if ta > 0:
                with c.group(ta):
                    _pop_tag(c, t, t_rawat, x + 40, 1240, "servis kompor", ORANGE)
                    _pop_tag(c, t, t_gas, x + 250, 1240, "beli gas", ORANGE)
            ia = 1 - prog(t, L8.start, 0.3)
            if ia > 0:
                with c.group(ia):
                    _pop_tag(c, t, t_idle, x + 40, 1240, "idle · tetap dibayar", C["rec"])
        appear(c, t, L5.start - 0.1, e - OUT, box, kitchen, enter="up")
        fade(c, t, t_legacy, L8.start - 0.1,
             lambda c: note(c, X + CW - 40, 790, "ini node legacy", prog(t, t_legacy + 0.2, 0.9),
                            arrow_to=(sx[2] + 30, 930), align="r", size=40))
    v.add(s, e, draw)
    v.sfx("whoosh", L5.start - 0.1, 0.6)
    for tt in ign:
        v.sfx("pop", tt, 0.4)
    v.sfx("tick", t_rawat, 0.4)
    v.sfx("tick", t_gas, 0.4)
    v.sfx("pop", t_legacy, 0.4)
    v.sfx("thud", t_idle, 0.5)
    for _, tt, _ in flood:
        v.sfx("tick", tt, 0.35)
    v.sfx("thud", t_kew, 0.6)


# ── 01 · KEPUTUSAN: cloud kitchen — ignite on a ticket, die when done ──
def keputusan(v, T, s, e):
    ch = v.chapter(1, "KEPUTUSAN", s, e)
    L9, L11, L12 = T["L09"], T["L11"], T["L12"]
    t_lepas = T.word("L09", "lepas")
    t_nyala = T.word("L10", "nyala")
    t_mati = T.word("L10", "mati")
    t_resep = T.word("L11", "resepnya")
    t_mesin = T.word("L11", "mesinnya")
    t_pensiun = T.word("L12", "pensiun")
    head1 = Headline("*Lepas* dapurnya.")
    head2 = Headline("Kamu urus *resepnya*.")
    head3 = Headline("Node legacy-nya *pensiun*.")
    sx = [X + CW * f for f in (0.2, 0.5, 0.8)]
    sy, ss = 1060, 220
    rail_y = 660
    t_cloud = t_lepas + 0.45
    # (burner, ticket lands, job done) — the signature move
    jobs = [(0, t_nyala - 0.1, t_mati - 0.2), (2, t_nyala + 0.45, t_mati + 0.1), (1, t_resep - 0.3, t_mesin + 0.4)]
    jobs = [(k, tl, max(td, tl + 0.8)) for k, tl, td in jobs]
    racks = [(MID - 375 + k * 260, 800, 230, 300) for k in range(3)]

    cam = v.camera
    cam.focus(t_nyala - 0.3, (sx[0] - 150, 800, 300, 400), zoom=1.06, dur=0.5)
    cam.reset(t_mati, dur=0.7)
    cam.key(t_pensiun, zoom=0.97, dur=0.12)
    cam.key(t_pensiun + 0.12, zoom=1.0, dur=0.4)

    def fire_of(t, k):
        f = 0.0
        for kk, tl, td in jobs:
            if kk == k and t >= tl:
                f = max(f, out_back(prog(t, tl, 0.35), 1.6) * (1 - in_cubic(prog(t, td, 0.6))))
        return f

    def draw(c, t):
        kicker(c, t, L9.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L9.start, L11.start - 0.15)
        head2.draw(c, t, L11.start, L12.start - 0.15)
        head3.draw(c, t, L12.start, e - OUT)
        muted = c.theme("muted", "d_muted")

        def old(c):
            for k in range(3):
                burner(c, sx[k], sy, ss, 1.0, t, seed=k)
            c.text(MID, 820, "DAPUR SENDIRI", F["mono_bold"], 19, muted, 1, 0.16, align="c")
        appear(c, t, L9.start - 0.1, t_lepas + 0.25, (X, 800, CW, 380), old, enter="up", exit="left")

        def cloud(c):
            c.text(MID, 600, "CLOUD KITCHEN", F["mono_bold"], 20, ORANGE, 1, 0.18, align="c")
            tickets = []
            for k, tl, td in jobs:
                drop = in_cubic(prog(t, tl - 0.35, 0.35))
                tickets.append(dict(x=sx[k], title=f"job-{k + 1:02d}", lines=(JOBS[k],), p=prog(t, tl - 1.1, 0.4),
                                    drop=((sy - 120 - rail_y) * drop, prog(t, tl - 0.12, 0.12))))
            ticket_rail(c, X + 30, rail_y, CW - 60, tickets, tw=150, th=180)
            for k in range(3):
                f = fire_of(t, k)
                burner(c, sx[k], sy, ss, f, t, seed=k + 3, cold=1 - clamp(f * 3))
            for k, tl, td in jobs:
                da = out_expo(prog(t, td, 0.3)) * (1 - prog(t, td + 1.0, 0.3))
                if da > 0:
                    _tag_c(c, sx[k], sy + ss * 0.34 + 18, "done", OK, da, h=40)
            _pop_tag(c, t, t_resep, X + 40, 1250, "kamu: job / query", C["accent"])
            _pop_tag(c, t, t_mesin, X + CW - 40, 1250, "cloud: mesinnya", OK, align="r")
        appear(c, t, t_cloud, L12.start - 0.15, (X, 560, CW, 760), cloud, enter="right", exit="up")

        def retire(c):
            for k, (rx, ry, rw, rh) in enumerate(racks):
                server_rack(c, rx, ry, rw, rh, t, units=4, on=1 - prog(t, L12.start + 0.3 + k * 0.15, 0.6),
                            seed=k + 5)
                c.text(rx + rw / 2, ry + rh + 44, f"node-{k + 1}", F["mono_med"], 19, muted, 1, 0.08, align="c")
            stamp(c, MID, 960, "PENSIUN", prog(t, t_pensiun, 0.35), color=ORANGE, rot=-0.12, size=96)
        appear(c, t, L12.start - 0.1, e - OUT, (MID - 390, 800, 780, 360), retire, enter="pop")
    v.add(s, e, draw)
    v.sfx("pop", L9.start - 0.1, 0.4)
    v.sfx("whoosh", t_lepas + 0.25, 0.6)
    for k, tl, td in jobs:
        v.sfx("tick", tl - 1.1, 0.3)
        v.sfx("whoosh", tl, 0.45)
        v.sfx("pop", td, 0.3)
    v.sfx("pop", t_resep, 0.5)
    v.sfx("pop", t_mesin, 0.5)
    v.sfx("pop", L12.start, 0.4)
    v.sfx("thud", t_pensiun, 0.8)


# ── 02 · DIAGRAM: Flink + MaxCompute → Paimon, ordered by Airflow ──────
TASKS = ["ingest", "flink", "maxcompute", "report"]


def diagram(v, T, s, e):
    ch = v.chapter(2, "DIAGRAM", s, e)
    L13, L14, L15, L16 = T["L13"], T["L14"], T["L15"], T["L16"]
    t_stream = T.word("L13", "streaming")
    t_batch = T.word("L14", "batch")
    t_paimon = T.word("L15", "Paimon")
    t_air = T.word("L16", "Airflow")
    heads = [(Headline("Streaming → *Flink*."), L13.start, L14.start - 0.15),
             (Headline("Batch → *MaxCompute*."), L14.start, L15.start - 0.15),
             (Headline("Satu pantry: *Paimon*."), L15.start, L16.start - 0.15),
             (Headline("Urutannya: *Airflow*."), L16.start, e - OUT)]
    EW = (CW - 48) / 2
    src = [(X, 560, EW, 86, "events"), (X + EW + 48, 560, EW, 86, "data harian")]
    eng = [(X, 730, EW, 170), (X + EW + 48, 730, EW, 170)]
    pantry = (X, 980, CW, 280)
    dag_y = 1282
    t_in = [L13.start + 0.1, L14.start + 0.1]
    t_run = t_air + 0.2

    cam = v.camera
    cam.focus(L13.start + 0.2, (X, 560, EW, 340), zoom=1.06, dur=0.7)
    cam.focus(L14.start, (X + EW + 48, 560, EW, 340), zoom=1.06, dur=0.7)
    cam.reset(L15.start, dur=0.8)
    cam.focus(L16.start + 0.1, (X, dag_y, CW, 164), zoom=1.05, dur=0.7)
    cam.reset(e - 1.0, dur=0.6)

    def draw(c, t):
        kicker(c, t, L13.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        muted, ink, faint = c.theme("muted", "d_muted"), c.theme("ink", "d_ink"), c.theme("faint", "d_line")

        def graph(c):
            for i in range(2):
                a = out_expo(prog(t, t_in[i], 0.4))
                if a <= 0.01:
                    continue
                x, y, w, h, lbl = src[i]
                arch_node(c, dict(x=x, y=y, w=w, h=h, kind="svc", label=lbl, a=a))
                ex, ey, ew, eh = eng[i]
                cx_ = ex + ew / 2
                pl = in_out_cubic(prog(t, t_in[i] + 0.2, 0.4))
                c.line(cx_, y + h + 4, cx_, y + h + 4 + (ey - y - h - 8) * pl, faint, 5)
                es = out_back(prog(t, t_in[i] + 0.3, 0.45), 1.5) if t >= t_in[i] + 0.3 else 0
                if es <= 0.01:
                    continue
                with c.at(0, 0, max(0.01, es), origin=(cx_, ey + eh / 2)):
                    c.card(ex, ey, ew, eh, r=24)
                    if i == 0:
                        burner(c, ex + 80, ey + 118, 110, out_back(prog(t, t_stream, 0.35), 1.6) if t >= t_stream
                               else 0, t, seed=9)
                        name, sub = "Flink", "STREAMING"
                    else:
                        oven(c, ex + 80, ey + 88, 104, out_expo(prog(t, t_batch, 0.6)), t, seed=4)
                        name, sub = "MaxCompute", "BATCH"
                    c.text(ex + 160, ey + 84, name, F["display_semi"], 42 if i == 0 else 36, ink, 1, -0.03)
                    c.text(ex + 160, ey + 122, sub, F["mono_med"], 17, muted, 1, 0.16)
            # streaming: fast small dots · batch: a crate every ~1.2 s
            if t >= t_stream:
                x, y, w, h, _ = src[0]
                cx_, y0, y1 = x + w / 2, y + h + 6, eng[0][1] - 6
                for k in range(6):
                    f = (t * 1.6 + k / 6) % 1.0
                    c.circle(cx_, y0 + (y1 - y0) * f, 6, ORANGE, min(1, f * 6, (1 - f) * 6))
            if t >= t_batch:
                x, y, w, h, _ = src[1]
                cx_, y0, y1 = x + w / 2, y + h + 6, eng[1][1] - 6
                f = ((t - t_batch) / 1.2) % 1.0
                fe = in_out_cubic(f)
                c.fill_rrect(cx_ - 20, y0 + (y1 - y0 - 30) * fe, 40, 30, 6, ORANGE, min(1, f * 8, (1 - f) * 8))
            # both engines read from and write to the same Paimon tables
            pl = in_out_cubic(prog(t, L15.start + 0.2, 0.5))
            if pl > 0:
                for i in range(2):
                    ex, ey, ew, eh = eng[i]
                    y0, y1 = ey + eh + 6, pantry[1] - 6
                    for dx, up in ((-40, False), (40, True)):
                        lx = ex + ew / 2 + dx
                        c.line(lx, y0, lx, y0 + (y1 - y0) * pl, faint, 4)
                        if t >= t_paimon:
                            for k in range(2):
                                f = (t * 0.9 + k / 2 + i * 0.25) % 1.0
                                py = y1 - (y1 - y0) * f if up else y0 + (y1 - y0) * f
                                c.circle(lx, py, 6, OK if up else ORANGE, min(1, f * 6, (1 - f) * 6))
                ra = out_expo(prog(t, t_paimon + 0.3, 0.4))
                c.text(X + CW / 2, pantry[1] - 30, "write ↓   ↑ read", F["mono_med"], 17, muted, ra, 0.1, align="c")
        appear(c, t, L13.start - 0.1, e - OUT, (X, 560, CW, 360), graph, blur=4, rise=20)
        appear(c, t, L15.start, e - OUT, pantry,
               lambda c: lake_pantry(c, *pantry, t, tables=("orders", "events", "customers"),
                                     p_tables=prog(t, t_paimon, 1.0)), enter="up")

        def band(c):
            st = dag_state(t, t_run, len(TASKS), 0.5)
            dag_flow(c, X, dag_y, CW, [dict(label=lb, run=r, done=d) for lb, (r, d) in zip(TASKS, st)],
                     p=out_expo(prog(t, L16.start, 0.8)))
        appear(c, t, L16.start - 0.05, e - OUT, (X, dag_y, CW, 164), band, enter="up")
    v.add(s, e, draw)
    for tt in t_in:
        v.sfx("pop", tt, 0.4)
        v.sfx("pop", tt + 0.3, 0.5)
    v.sfx("whoosh", t_stream, 0.4)
    v.sfx("whoosh", t_batch, 0.5)
    v.sfx("whoosh", L15.start, 0.5)
    v.sfx("pop", t_paimon, 0.4)
    v.sfx("pop", L16.start, 0.4)
    for k in range(len(TASKS)):
        v.sfx("tick", t_run + k * 0.5 + 0.4, 0.4)
    v.sfx("chime", t_run + len(TASKS) * 0.5 + 0.1, 0.8)


# ── 03 · HASIL: faster → nothing to babysit → pipeline runs itself ─────
def hasil(v, T, s, e):
    ch = v.chapter(3, "HASIL", s, e)
    L17, L18, L19 = T["L17"], T["L18"], T["L19"]
    t_cepat = T.word("L17", "cepat")
    chores = [("patch", T.word("L18", "di-patch")), ("restart", T.word("L18", "di-restart")),
              ("jaga tengah malam", T.word("L18", "dijagain"))]
    t_sendiri = T.word("L19", "sendiri")
    head1 = Headline("Hasilnya:")
    head2 = Headline("Nggak ada yang *dijagain*.")
    head3 = Headline("Pipeline jalan *sendiri*.")
    card = (X, 620, CW, 540)
    band_y = 860
    cycle = 2.6

    cam = v.camera
    cam.key(t_cepat, zoom=0.97, dur=0.12)
    cam.key(t_cepat + 0.12, zoom=1.0, dur=0.4)
    cam.focus(chores[0][1] - 0.2, card, zoom=1.05, dur=0.8)
    cam.reset(L19.start, dur=0.6)

    def draw(c, t):
        kicker(c, t, L17.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L17.start, L18.start - 0.15)
        head2.draw(c, t, L18.start, L19.start - 0.15)
        head3.draw(c, t, L19.start, e - OUT)
        ink, muted = c.theme("ink", "d_ink"), c.theme("muted", "d_muted")

        def punch(c):
            a0 = out_expo(prog(t, L17.start + 0.1, 0.4))
            c.text(MID, 760, "data processing", F["mono_med"], 32, c.theme("ink2", "d_muted"), a0, 0.06, align="c")
            c.text(MID, 950, "lebih", F["display"], 120, ink, out_expo(prog(t, L17.start + 0.3, 0.5)), -0.05,
                   align="c")
            p = prog(t, t_cepat, 0.35)
            dx = 260 * (1 - out_expo(p))
            c.text(MID + dx, 1200, "cepat.", F["display"], 250, ORANGE, clamp(p * 3), -0.06, align="c")
            streak = 1 - out_expo(prog(t, t_cepat, 0.7))
            if 0 < p and streak > 0.01:
                for k in range(4):
                    yk = 1060 + k * 36
                    c.line(MID + 390 + dx, yk, MID + 390 + dx + 300 * streak, yk, ORANGE, 6, 0.6 * streak)
        appear(c, t, L17.start, L18.start - 0.15, (X, 700, CW, 560), punch, enter="up", exit="up", blur=4)

        def chore_list(c):
            x, y, w, h = card
            c.card(x, y, w, h, r=28)
            c.text(x + 36, y + 56, "TUGAS NODE LEGACY", F["mono_bold"], 19, muted, 1, 0.16)
            moon(c, x + w - 70, y + 56, 30)
            for k, (lbl, tt) in enumerate(chores):
                ry = y + 170 + k * 130
                a = out_expo(prog(t, tt - 0.3, 0.4))
                c.text(x + 36, ry, lbl, F["display_semi"], 58, ink, a * (1 - 0.5 * prog(t, tt + 0.35, 0.4)), -0.03)
                tw = c.measure(lbl, F["display_semi"], 58, -0.03)[0]
                strike(c, t, tt + 0.35, x + 28, x + 44 + tw, ry - 20, width=7)
        appear(c, t, L18.start - 0.1, L19.start - 0.15, card, chore_list, enter="right", exit="left")

        def band(c):
            t0 = L19.start + 0.2
            tl = t0 + ((t - t0) % cycle) if t >= t0 else t
            st = dag_state(tl, t0, len(TASKS), 0.5)
            dag_flow(c, X, band_y, CW, [dict(label=lb, run=r, done=d) for lb, (r, d) in zip(TASKS, st)])
            tag(c, X, band_y + 200, "data masuk", C["accent"], h=44)
            tag(c, X + CW, band_y + 200, "siap dipakai", OK, align="r", h=44)
            note(c, X + CW - 10, band_y + 360, "nggak ada yang\nnekan tombol", prog(t, t_sendiri + 0.2, 0.9),
                 align="r", size=40)
        appear(c, t, L19.start - 0.05, e - OUT, (X, band_y, CW, 420), band, enter="right")
    v.add(s, e, draw)
    v.sfx("pop", L17.start + 0.1, 0.4)
    v.sfx("thud", t_cepat)
    v.sfx("whoosh", t_cepat - 0.05, 0.4)
    v.sfx("whoosh", L18.start - 0.1, 0.5)
    for _, tt in chores:
        v.sfx("tick", tt + 0.35, 0.5)
    v.sfx("whoosh", L19.start - 0.05, 0.5)
    for k in range(len(TASKS)):
        v.sfx("tick", L19.start + 0.2 + k * 0.5 + 0.4, 0.35)
    v.sfx("chime", t_sendiri + 0.1, 0.7)


# ── RECAP (dark): the wall lifts — the servers were there all along ────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L20, L21, L22 = T["L20"], T["L21"], T["L22"]
    t_tetap = T.word("L21", "tetap")
    t_bukan = T.word("L21", "bukan")
    t_data = T.word("L22", "datanya")
    heads = [(Headline("Bukan soal *nggak ada server*.", style="headline_dark"), L20.start, L21.start - 0.15),
             (Headline("Server-nya *tetap ada*.", style="headline_dark"), L21.start, t_bukan - 0.15),
             (Headline("*Bukan kamu* yang ngurus.", style="headline_dark"), t_bukan, L22.start - 0.15),
             (Headline("Balik ke *datanya*.", style="headline_dark"), L22.start, e - OUT)]
    room = (X, 600, CW, 580)
    sx = [X + CW * f for f in (0.2, 0.5, 0.8)]
    sy, ss = 1250, 200
    t_job = L20.start + 0.6

    cam = v.camera
    cam.key(s, zoom=1.12, y=1150, dur=0.01)
    cam.key(t_tetap - 0.2, zoom=1.0, dur=1.4)

    def draw(c, t):
        for h, a, b in heads:
            h.draw(c, t, a, b)
        dim = in_out_cubic(prog(t, t_data - 0.3, 0.6))
        lift = in_out_cubic(prog(t, t_tetap - 0.1, 0.9))

        def scene(c):
            x, y, w, h = room
            with c.group(1 - 0.75 * dim):
                with c.clip(x, y, w, h, 28):
                    for k in range(3):
                        server_rack(c, x + 20 + k * (w - 40) / 3 + 8, y + 30, (w - 40) / 3 - 16, h - 60, t, units=7,
                                    seed=k + 11)
                    wy = y - (h + 40) * lift
                    c.fill_rrect(x, wy, w, h, 28, mix(C["d_card"], (1, 1, 1, 1), 0.05))
                    c.stroke_rrect(x, wy, w, h, 28, C["d_line"], 1.5)
                    c.text(x + w / 2, wy + h / 2 - 10, "CLOUD KITCHEN", F["mono_bold"], 30, ORANGE, 1, 0.2,
                           align="c")
                    c.text(x + w / 2, wy + h / 2 + 50, "buka pas ada pesanan", F["serif"], 40, C["d_muted"], 1,
                           align="c")
                for k in range(3):
                    f = 0.0
                    if k == 1 and t >= t_job:
                        f = out_back(prog(t, t_job, 0.35), 1.6) * (1 - in_cubic(prog(t, t_job + 2.2, 0.6)))
                    burner(c, sx[k], sy, ss, f, t, seed=k + 20, cold=1 - clamp(f * 3))
                ta = out_expo(prog(t, t_bukan, 0.4))
                _tag_c(c, MID, y + h + 210, "dikelola cloud provider", OK, ta)
            if dim > 0.01:
                cx_, cy_ = MID, y + h / 2
                for k in range(24):
                    ang = k / 24 * 2 * math.pi + t * 0.5
                    r = 220 + 14 * math.sin(t * 2 + k)
                    c.circle(cx_ + r * math.cos(ang), cy_ + r * math.sin(ang) * 0.8, 7, ORANGE, dim * 0.9)
                c.text(cx_, cy_ + 30, "datanya.", F["serif"], 120, ORANGE, dim, align="c")
        appear(c, t, L20.start - 0.1, e - OUT, (X, 600, CW, 860), scene, enter="up")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("whoosh", t_job, 0.3)
    v.sfx("whoosh", t_tetap - 0.1, 0.7)
    v.sfx("pop", t_bukan, 0.5)
    v.sfx("chime", t_data)


# ── OUTRO: logo + EP04 teaser + follow ─────────────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L23, L24 = T["L23"], T["L24"]
    t_click = T.word("L24", "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, ORANGE)
            c.text(X + 50, 892, "EPISODE BERIKUTNYA · EP 04", F["mono_bold"], 20, ORANGE, 1, 0.16)
            c.text(X + 50, 962, "Monolith → event-driven", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "Monolith lama, dipecah", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L23.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L24.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "Seri Bongkar Arsitektur", F["ui"], 28,
                                                          C["d_muted"], 1, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L24.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L23.start, 0.5)
    v.sfx("chime", t_click + 0.1)
