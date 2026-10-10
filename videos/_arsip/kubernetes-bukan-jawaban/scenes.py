"""Kubernetes bukan jawaban buat semua hal — QUICK opinion video. See PLAN.md.

Metaphor: Kubernetes is a container port (crane = scheduler, yard = node, box = container); a one-app job is one
parcel, and a courier (VM / serverless) carries it fine. Signature: the gantry crane slides, drops, lifts, sets down —
first containers, then (absurdly) one cardboard box.
Motion: snappy springs · blur headlines (+ track_line punches) · persistent crane (Rig) + bento · blur exits.
Sound: styled score garage E warm 130 + mech SFX kit.
"""
from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_back, in_cubic, in_out_cubic
from engine.components import (Headline, kicker, fade, pop_tag, check_badge, brand_intro, Rig, bento, track_line,
                               drifting, note, strike, word_pill, big_number, receipt, standard_outro, cover, crane,
                               peti_kemas, paket, kurir, PORT_GREEN as GREEN)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
OUTRO_TAIL = 3.0
PRE_ROLL = 2.05                            # long brand sting (version 2): voice starts under its wipe
RED = C["rec"]
CH = ["00 · PELABUHAN", "01 · SATU PAKET", "02 · BIAYA DIAM", "03 · TIGA PERTANYAAN", "RECAP", "OUTRO"]

# the crane is drawn around (0, 0) = centre of its ground line; geometry in crane-local px
CW_, CH_ = 560, 520                        # crane width / beam height
CX0 = -CW_ / 2                             # crane x (left leg)
BOX_W, BOX_H = 150, 80
SLOTS = {"A": -215, "B": -45, "C": 125}    # yard slots (left edges), between the legs
PICK = 0.0                                 # trolley at the cantilever tip = the quay
PARK = 0.5
GROUND = 1300


def _tr(cx):
    """Trolley value (0..1) that puts the spreader centre at crane-local x = cx."""
    b0, b1 = CX0 - CW_ * 0.12 + 40, CX0 + CW_ - 40
    return (cx - b0) / (b1 - b0)


def _hoist(top_y):
    """Hoist value that puts the spreader bottom (= the load's top) at crane-local y = top_y."""
    top, bottom = -CH_ + 40, -40
    return (top_y - 16 - top) / (bottom - top)


QUAY_X = CX0 - CW_ * 0.12 + 40             # spreader centre at trolley 0


class Cycle:
    """One pick-and-place: trolley to pick, drop, grab, lift, travel, drop, release, lift (snappy, keyed)."""

    def __init__(self, t0, pick, place, start=PARK):
        (pt, ph), (qt, qh) = pick, place
        self.keys = [(t0, start, 0.08), (t0 + 0.5, pt, 0.08), (t0 + 0.85, pt, ph), (t0 + 1.2, pt, 0.12),
                     (t0 + 1.9, qt, 0.12), (t0 + 2.25, qt, qh), (t0 + 2.6, qt, 0.08)]
        self.grab, self.drop = t0 + 0.85, t0 + 2.25

    def state(self, t):
        k = self.keys
        if t <= k[0][0]:
            return k[0][1], k[0][2]
        for (ta, ra, ha), (tb, rb, hb) in zip(k, k[1:]):
            if t < tb:
                u = in_out_cubic(prog(t, ta, tb - ta))
                return ra + (rb - ra) * u, ha + (hb - ha) * u
        return k[-1][1], k[-1][2]

    def carrying(self, t):
        return self.grab <= t < self.drop


def _box(color):
    return lambda c, cx, y: peti_kemas(c, cx - BOX_W / 2, y, BOX_W, BOX_H, color)


def build(project):
    T = project.timing
    v = Video(duration=T["L19"].end + OUTRO_TAIL, bpm=130, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="garage", key="E", mood="warm")      # EP 02 marimba A bright, EP 01 lofi F dreamy
    v.sfx_kit = "mech"
    v.cover = lambda c: cover(c, "Kubernetes?\n*Tergantung*.", kicker="OPINI ORANG CLOUD", color=GREEN,
                              tags=["pelabuhan", "kurir", "3 pertanyaan"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    hero = _crane_hero(v, T, b)
    intro(v, T, 0.0, b["00 · PELABUHAN"])
    pelabuhan(v, T, b["00 · PELABUHAN"], b["01 · SATU PAKET"], hero)
    satu_paket(v, T, b["01 · SATU PAKET"], b["02 · BIAYA DIAM"], hero)
    biaya(v, T, b["02 · BIAYA DIAM"], b["03 · TIGA PERTANYAAN"])
    tiga(v, T, b["03 · TIGA PERTANYAAN"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    standard_outro(v, T, b["OUTRO"], v.duration, "L19", GREEN,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="Tim pelabuhan, atau tim kurir?",
                               sub="Ceritain stack kamu."))
    v.cover_t = T["L09"].frac(0.6)
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(1.0, w / 760)
    with c.at(x + w / 2, y + h * 0.92, s):
        crane(c, CX0, 0, CW_, CH_, 0.0, trolley=_tr(0), hoist=_hoist(-150),
              load=lambda c, cx, y_: paket(c, cx, y_ + 50, 70))
        for name in ("A", "C"):
            peti_kemas(c, SLOTS[name], -BOX_H, BOX_W, BOX_H, GREEN if name == "A" else C["muted"])


def _heads(T, items, end, style="headline"):
    out = []
    for i, (text, lid) in enumerate(items):
        t_out = T[items[i + 1][1]].start - 0.15 if i + 1 < len(items) else end
        out.append((Headline(text, style=style), T[lid].start, t_out))
    return out


def _draw_heads(c, t, hs):
    for h, a, b_ in hs:
        h.draw(c, t, a, b_)


def _io(t, t_in, t_out, d_in=0.5):
    return out_expo(prog(t, t_in, d_in)) * (1 - in_cubic(prog(t, t_out, OUT)))


# ── the persistent hero: one crane from 00 to the end of 01 (+ small and dim behind the receipt in 02) ─────
def _crane_hero(v, T, b):
    s0, s1, s2, s3 = b["00 · PELABUHAN"], b["01 · SATU PAKET"], b["02 · BIAYA DIAM"], b["03 · TIGA PERTANYAAN"]
    t_kurir = T.word("L10", "kurir")
    rig = Rig(MID + 40, GROUND + 60, s=1.12, a=0.0)
    rig.to(s0 + 0.1, a=1.0, dur=0.4)
    rig.to(s0 + 0.1, y=GROUND, s=1.0, preset="snappy", dur=0.9)
    rig.to(t_kurir - 0.3, x=X + 250, s=0.62, preset="snappy", dur=0.8)
    rig.to(s2 + 0.2, x=X + CW - 170, y=1240, s=0.45, a=0.45, preset="snappy", dur=0.9)
    rig.to(s3 - 0.4, a=0.0, dur=0.4)

    c1 = Cycle(T.word("L06", "crane"), (PICK, _hoist(-BOX_H)), (_tr(SLOTS["B"] + BOX_W / 2), _hoist(-BOX_H)))
    c2 = Cycle(T.word("L07", "banyak") - 0.4, (PICK, _hoist(-BOX_H)),
               (_tr(SLOTS["C"] + BOX_W / 2), _hoist(-2 * BOX_H)), start=c1.keys[-1][1])
    t_box = T.word("L09", "paket") - 0.9
    c3 = Cycle(t_box, (PICK, _hoist(-50)), (PICK, 0.18), start=c2.keys[-1][1])     # lift the parcel, hold it up
    t_lone = T.word("L08", "satu")

    def draw(c, t):
        if t < s0 or t > s3:
            return
        cyc = c1 if t < c2.keys[0][0] else (c2 if t < c3.keys[0][0] else c3)
        tr, ho = cyc.state(t)
        dim = 1 - 0.7 * prog(t, t_lone, 0.5)
        load = None
        if cyc is c3 and t >= c3.grab and t < t_kurir:
            load = lambda c, cx, y: paket(c, cx, y + 50, 70)
        elif cyc is not c3 and cyc.carrying(t):
            load = _box(GREEN)
        with rig.place(c, t):
            with c.group(dim):
                peti_kemas(c, SLOTS["A"], -BOX_H, BOX_W, BOX_H, C["muted"])
                peti_kemas(c, SLOTS["A"], -2 * BOX_H, BOX_W, BOX_H, GREEN)
                peti_kemas(c, SLOTS["C"], -BOX_H, BOX_W, BOX_H, C["muted"])
                if t < c1.grab:
                    peti_kemas(c, QUAY_X - BOX_W / 2, -BOX_H, BOX_W, BOX_H, GREEN)
                if t >= c1.drop:
                    peti_kemas(c, SLOTS["B"], -BOX_H, BOX_W, BOX_H, GREEN)
                if c1.drop <= t < c2.grab:
                    peti_kemas(c, QUAY_X - BOX_W / 2, -BOX_H, BOX_W, BOX_H, GREEN)
                if t >= c2.drop:
                    peti_kemas(c, SLOTS["C"], -2 * BOX_H, BOX_W, BOX_H, GREEN)
            c.line(CX0 - CW_ * 0.25, 0, CX0 + CW_ + 30, 0, c.theme("faint", "d_line"), 5)
            if t_lone <= t < c3.grab:
                p = out_back(prog(t, t_lone, 0.4))
                with c.at(0, 0, max(0.01, p), origin=(QUAY_X, 0)):
                    paket(c, QUAY_X, 0, 70)
            crane(c, CX0, 0, CW_, CH_, t, trolley=tr, hoist=ho, load=load, lamp=prog(t, s2, 0.6))
    v.add(s0, s3, draw, z=5)
    for cyc in (c1, c2, c3):
        v.sfx("whoosh", cyc.keys[0][0], 0.35)
        v.sfx("click", cyc.grab, 0.7)
        if cyc is not c3:
            v.sfx("thud", cyc.drop, 0.6)
    v.sfx("pop", t_lone)
    return dict(rig=rig, c3=c3, t_kurir=t_kurir)


# ── INTRO: the myth struck out → "Tergantung." → the real 10.000 ─────────────
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3, L4 = T["L01"], T["L02"], T["L03"], T["L04"]
    t_tg = T.word("L02", "tergantung")
    t_num = T.word("L03", "sepuluh")
    myth = Headline("Pakai\n*Kubernetes* aja.")
    hs = _heads(T, [("Pernah aku\n*bangun*.", "L03"), ("Makanya tahu\nkapan *nggak*.", "L04")], e - OUT)

    def draw(c, t):
        kicker(c, t, L1.start, L3.start - 0.3, "SARAN YANG SERING KEDENGERAN", GREEN)
        myth.draw(c, t, L1.start, L3.start - 0.3, strike_at=L2.start)
        track_line(c, t, t_tg, L3.start - 0.3, X, 1000, "Tergantung.", "display", 150, c.theme("ink", "d_ink"))
        kicker(c, t, L3.start, e - OUT, "BONGKAR ARSITEKTUR · EP 01", GREEN)
        _draw_heads(c, t, hs)
        a = _io(t, t_num - 0.2, e - OUT)
        if a > 0.01:
            with c.group(a):
                big_number(c, X, 900, 10000, t, t_num, decimals=0, suffix="", caption="REQUEST BARENGAN",
                           sub="Kubernetes yang aku bangun", dur=1.0)
            fade(c, t, L4.start, e - OUT, lambda c: note(c, X + 20, 1320, "justru karena itu", 1.0, size=44))
    v.add(s, e, draw, z=20)
    v.camera.key(t_tg, zoom=0.97, dur=0.3).key(t_tg + 0.35, zoom=1.0, dur=0.5)
    v.sfx("click", L2.start, 0.7)
    v.sfx("thud", t_tg)
    v.sfx("whoosh", L3.start - 0.2, 0.6)
    for k in range(6):
        v.sfx("tick", t_num + k * 0.15, 0.4)
    v.sfx("pop", L4.start, 0.5)


# ── 00 · PELABUHAN: the crane stacks containers — scheduler / node / container ───
def pelabuhan(v, T, s, e, hero):
    ch = v.chapter(0, "PELABUHAN", s, e)
    L5, L6, L7 = T["L05"], T["L06"], T["L07"]
    hs = _heads(T, [("Kubernetes =\n*pelabuhan*.", "L05"), ("Ratusan *container*,\nsatu jadwal.", "L06"),
                    ("Rame? Dia *juara*.", "L07")], e - OUT)
    maps = [("crane", "crane → scheduler"), ("lapangan", "lapangan → node"), ("container", "peti → container")]
    t_juara = T.word("L07", "juara")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "00 · PELABUHAN", ch.color)
        _draw_heads(c, t, hs)
        for i, (w, label) in enumerate(maps):
            t0 = T.word("L06", w)
            fade(c, t, t0, L7.start + 0.4, lambda c, t0=t0, i=i, label=label:
                 pop_tag(c, t, t0, X + (0, 290, 0)[i], (1390, 1390, 1450)[i], label, GREEN))
        if t >= t_juara:
            check_badge(c, X + 60, 1420, 34, out_back(prog(t, t_juara, 0.4)) * (1 - prog(t, e - OUT, OUT)))
            fade(c, t, t_juara + 0.2, e - OUT, lambda c: c.text(X + 120, 1434, "banyak service, traffic naik turun",
                                                                F["ui_semi"], 32, C["ink2"]))
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.12, y=1100, dur=0.01).key(s + 0.1, zoom=1.0, y=960, dur=2.2)
    v.sfx("whoosh", s + 0.1, 0.6)
    for w, _ in maps:
        v.sfx("pop", T.word("L06", w), 0.6)
    v.sfx("chime", t_juara)


# ── 01 · SATU PAKET: one app → the giant crane lifts one parcel → the courier ──
def satu_paket(v, T, s, e, hero):
    ch = v.chapter(1, "SATU PAKET", s, e)
    L8, L9, L10 = T["L08"], T["L09"], T["L10"]
    rig, c3, t_kurir = hero["rig"], hero["c3"], hero["t_kurir"]
    t_vm, t_sl = T.word("L10", "VM"), T.word("L10", "serverless")
    hs = _heads(T, [("App-mu *satu*.", "L08"), ("Sewa pelabuhan\nbuat *satu paket*?", "L09"), ("Cukup *kurir*.", "L10")],
                e - OUT)
    KX, KS = X + CW - 360, 300

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "01 · SATU PAKET", ch.color)
        _draw_heads(c, t, hs)
        fade(c, t, L8.start + 0.5, L9.start, lambda c: pop_tag(c, t, L8.start + 0.5, X, 1420, "1 app · ratusan user",
                                                                GREEN))
        if L9.start <= t < t_kurir:
            note(c, X + 420, 1440, "sewa satu pelabuhan?", prog(t, c3.grab + 0.3, 0.5), size=42)
        k = _io(t, t_kurir - 0.3, e - OUT, d_in=0.8)
        if k > 0.01:
            dx = 420 * (1 - out_expo(prog(t, t_kurir - 0.3, 0.9)))
            kurir(c, KX + dx, GROUND, KS, t, ride=1 - prog(t, t_kurir + 0.5, 0.3), alpha=k)
            if t >= t_kurir + 0.4:                               # the parcel rides in the courier's box
                paket(c, KX + 60 + dx, GROUND - KS * 0.62, 56, alpha=k * prog(t, t_kurir + 0.4, 0.3))
            fade(c, t, t_vm, e - OUT, lambda c: pop_tag(c, t, t_vm, X + CW - 380, 1400, "VM", GREEN))
            fade(c, t, t_sl, e - OUT, lambda c: pop_tag(c, t, t_sl, X + CW - 270, 1400, "serverless", GREEN))
    v.add(s, e, draw, z=20)
    v.camera.focus(c3.grab - 0.2, (X + 20, 900, 420, 420), zoom=1.12, dur=0.9)
    v.camera.reset(t_kurir - 0.3, dur=0.8)
    v.sfx("whoosh", s + 0.1, 0.6)
    v.sfx("pop", L8.start + 0.5, 0.5)
    v.sfx("whoosh", t_kurir - 0.3, 0.7)
    v.sfx("pop", t_kurir + 0.4)
    v.sfx("pop", t_vm)
    v.sfx("pop", t_sl)


# ── 02 · BIAYA DIAM: the port costs money even when it's quiet ───────────────
def biaya(v, T, s, e):
    ch = v.chapter(2, "BIAYA DIAM", s, e)
    L11, L12, L13 = T["L11"], T["L12"], T["L13"]
    t_cp, t_mon, t_up = T.word("L12", "Control"), T.word("L12", "monitoring"), T.word("L12", "upgrade")
    t_ng, t_mahal = T.word("L13", "ngerti"), T.word("L13", "mahal")
    hs = _heads(T, [("Sepi pun\ntetap *bayar*.", "L11"), ("Jalan *terus*.", "L12"), ("Yang paling *mahal*.", "L13")],
                e - OUT)
    RX, RY, RW = X + 10, 640, 560

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · BIAYA YANG DIAM", ch.color)
        _draw_heads(c, t, hs)
        a = _io(t, L11.start + 0.3, e - OUT)
        if a <= 0.01:
            return
        lines = [("control plane", "tiap jam", prog(t, t_cp, 0.4), 0, None),
                 ("monitoring", "tiap hari", prog(t, t_mon, 0.4), 0, None),
                 ("upgrade versi", "tiap rilis", prog(t, t_up, 0.4), 0, None),
                 ("orang yang ngerti", "?", prog(t, t_ng, 0.4), 0, RED)]
        with c.group(a), c.at(0, 30 * (1 - a), 1, origin=(RX + RW / 2, RY), rot=-0.03):
            receipt(c, RX, RY, RW, lines, title="BIAYA PELABUHAN", sub="walau lagi sepi")
        if t >= t_mahal:
            fade(c, t, t_mahal, e - OUT, lambda c: pop_tag(c, t, t_mahal, X, 1330, "paling mahal", RED))
            note(c, X + 270, 1390, "bukan servernya", prog(t, t_mahal + 0.4, 0.5) * (1 - prog(t, e - OUT, OUT)),
                 size=40)
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.0, y=960, dur=0.01).key(t_ng, zoom=1.08, y=1120, dur=1.0)
    v.camera.reset(e - 0.6, dur=0.6)
    v.sfx("whoosh", s + 0.1, 0.6)
    for t0 in (t_cp, t_mon, t_up):
        v.sfx("tick", t0, 0.7)
    v.sfx("thud", t_ng)
    v.sfx("pop", t_mahal)


# ── 03 · TIGA PERTANYAAN: bento checklist (save-able) ──────────────────────
def tiga(v, T, s, e):
    ch = v.chapter(3, "TIGA PERTANYAAN", s, e)
    L14, L15, L16 = T["L14"], T["L15"], T["L16"]
    qs = [("Service-nya banyak?", "banyak"), ("Traffic naik turun ekstrem?", "ekstrem"), ("Ada tim yang siap jaga?", "jaga")]
    t_k = T.word("L16", "Kubernetes")
    hs = _heads(T, [("Jawab *tiga* ini.", "L14"), ("Tiga-tiganya *iya*?", "L16")], e - OUT)

    def tile(i):
        text, w = qs[i]
        t_yes = T.word("L15", w)

        def draw(c, x, y, w_, h, p):
            c.text(x + 40, y + h / 2 + 12, f"0{i + 1}", F["mono_bold"], 26, C["muted"], 1, 0.12)
            c.text(x + 110, y + h / 2 + 16, text, F["ui_semi"], 40, C["ink"], 1, -0.02)
            ok = out_back(prog(t_now[0], t_yes, 0.4))
            cx, cy = x + w_ - 70, y + h / 2
            c.circle(cx, cy, 30, C["faint"], 1 - ok)
            if ok > 0:
                check_badge(c, cx, cy, 30, ok)
        return (0, i, 1, 1, draw)
    t_now = [0.0]

    def draw(c, t):
        t_now[0] = t
        kicker(c, t, s + 0.2, e - OUT, "03 · SEBELUM PILIH", ch.color)
        _draw_heads(c, t, hs)
        bento(c, t, L14.start + 0.3, (X, 620, CW, 600), [tile(i) for i in range(3)], cols=1, rows=3, t_out=e - OUT)
        if t >= t_k:
            pa = out_back(prog(t, t_k, 0.4)) * (1 - prog(t, e - OUT, OUT))
            with c.at(0, 0, max(0.01, pa), origin=(X, 1330)):
                word_pill(c, X, 1280, "Kubernetes.", GREEN, size=96, alpha=min(1, pa))
            fade(c, t, t_k + 0.5, e - OUT, lambda c: c.text(X, 1480, "Kurang satu? Mulai dari kurir dulu.",
                                                             F["ui_semi"], 32, C["ink2"]))
    v.add(s, e, draw, z=20)
    for i, (_, w) in enumerate(qs):
        v.camera.key(T.word("L15", w) - 0.2, zoom=1.04, y=720 + i * 210, dur=0.6)
        v.sfx("chime", T.word("L15", w), 0.6)
    v.camera.reset(L16.start, dur=0.7)
    v.sfx("whoosh", s + 0.1, 0.6)
    v.sfx("pop", L14.start + 0.3, 0.6)
    v.sfx("thud", t_k)


# ── RECAP (dark): pick for the problem, not the trend — the courier rides off ─
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L17 = T["L17"]
    t_hebat, t_mas, t_tren = T.word("L17", "hebat"), T.word("L17", "masalahnya"), T.word("L17", "trennya")
    hs = _heads(T, [("Pilih buat\n*masalahnya*.", "L17")], e - OUT, style="headline_dark")

    def draw(c, t):
        _draw_heads(c, t, hs)
        a = _io(t, s + 0.2, e - OUT)
        if a <= 0.01:
            return
        with c.group(a), drifting(c, t, s, e, (MID, 1150)):
            with c.at(X + 230, 1150, 0.55):
                crane(c, CX0, 0, CW_, CH_, t, trolley=PARK, hoist=0.08, lamp=1.0)
                peti_kemas(c, SLOTS["A"], -BOX_H, BOX_W, BOX_H, GREEN)
                peti_kemas(c, SLOTS["C"], -BOX_H, BOX_W, BOX_H, GREEN)
            ride = prog(t, t_tren + 0.4, 1.4)
            kurir(c, X + CW - 330 + 260 * in_cubic(ride), 1150, 260, t, ride=1.0 if ride > 0 else 0.0,
                  alpha=1 - prog(ride, 0.6, 0.4))
            c.line(X + 24, 1150, X + CW - 24, 1150, C["d_line"], 4)
            fade(c, t, t_hebat, None, lambda c: c.text(X + 24, 1240, "alat yang hebat", F["mono_med"], 24, C["d_muted"]))
            fade(c, t, t_mas, None, lambda c: c.text(X + CW - 300, 1240, "alat yang pas", F["mono_med"], 24,
                                                       C["d_accent"]))
        if t >= t_tren:
            fade(c, t, t_tren, e - OUT, lambda c: c.text(X, 1400, "bukan buat trennya.", F["display"], 64, C["d_muted"],
                                                          1, -0.04))
            strike(c, t, t_tren + 0.3, X, X + 560, 1380, alpha=1 - prog(t, e - OUT, OUT))
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.04, y=1050, dur=3.0)
    v.sfx("whoosh_dark", s)
    v.sfx("pop", t_hebat, 0.5)
    v.sfx("chime", t_mas, 0.6)
    v.sfx("click", t_tren + 0.3, 0.6)
    v.sfx("whoosh", t_tren + 0.4, 0.5)
