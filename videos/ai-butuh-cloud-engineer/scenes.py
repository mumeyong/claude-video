"""AI nggak gantiin cloud engineer — AI butuh cloud engineer. QUICK, pilar C, classic + Apple craft, flat-big. See PLAN.md.

Metaphor: a hajatan stage. AI = the singer everyone sees under the lamps (INTRO) → under the stage, in the dark, the
follow spot finds the generator (GPU), the cable drum (network), the road case (storage), the rental slip (cost) (00)
→ the spot climbs to the dark wing: the sound crew at the mixer = the cloud engineer; generator on for training, then
scaled down, inference always ready, everything packed in containers (01) → the stage becomes one of three (02) →
in the dark the singer is swapped, the crew stays (RECAP).
Signature: the follow-spot pool searching the dark parts — whatever it touches lights up and stays lit.
Motion: wipe headlines · one persistent hero (Rig: full-bleed shrink → rest → one of three → back) · quiet exits ·
silk spring for the stage, smooth for the spot + tags · camera only dollies in holds + cuts at chapter changes.
Sound: styled score marimba D bright 110 + wood SFX kit (ai-gratis cinematic/mech, wifi-ep03 lofi/glass).
"""
from engine import Video, tokens as tk
from engine.ease import clamp, lerp, prog, curve
from engine.components import (Headline, kicker, fade, pop_tag, tag_center, note, brand_intro, standard_outro, cover,
                               Rig, arrive, follow, rise, dolly, cut, heads, draw_heads, panggung, panggung_geo,
                               PANGGUNG_PURPLE as PURPLE)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                             # long brand sting (version 2): voice starts under its wipe
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · KOLONG PANGGUNG", "01 · KRU SOUND", "02 · SKILL-NYA", "RECAP", "OUTRO"]
LOOK = "flat"
HB = (-550, -500, 1100, 1000)               # the stage in its own px, around the Rig origin
G = panggung_geo(*HB)
RX, RY = MID, 1040                          # Rig rest position (stage spans y 540–1540 at s = 1)
INOUT = curve("apple_in_out")
SPOT_MOVE = 0.75
SPOT_R = 190


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words oddly)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


def _centre(name):
    x, y, w, h = G["items"][name]
    return x + w / 2, y + h / 2


def scr(lx, ly):
    """Stage px → screen px while the stage rests at s = 1 (INTRO … 01)."""
    return RX + lx, RY + ly


class Cue:
    """Every time the stage reacts to, computed once from the voice."""

    def __init__(self, T, b):
        self.b = b
        self.t_in = T["L01"].start - 0.1
        self.training = _w(T, "L01", "training", 0.55)
        self.bukan = _w(T, "L02", "bukan", 0.6)
        self.gantiin = _w(T, "L03", "gantiin", 0.25)
        self.butuh = _w(T, "L03", "butuh", 0.7)
        self.biduan = _w(T, "L04", "biduan", 0.45)
        self.genset = _w(T, "L06", "genset", 0.5)
        self.network = _w(T, "L07", "network", 0.3)
        self.storage = _w(T, "L07", "storage", 0.85)
        self.jam = _w(T, "L08", "jam", 0.9)
        self.kru = _w(T, "L09", "kru", 0.75)
        self.train = _w(T, "L10", "training", 0.45)
        self.selesai = _w(T, "L10", "selesai", 0.92)
        self.siap = _w(T, "L11", "siap", 0.3)
        self.container = _w(T, "L12", "container", 0.2)
        self.sendiri = _w(T, "L13", "sendiri", 0.9)
        self.panggung = _w(T, "L14", "panggung", 0.85)
        self.skills = [_w(T, "L15", w, f) for w, f in (("GPU", 0.55), ("network", 0.72), ("biaya", 0.9))]
        self.hilang = _w(T, "L16", "hilang", 0.85)
        self.ganti = _w(T, "L17", "ganti", 0.2)
        self.orang = _w(T, "L17", "orang", 0.9)
        # the follow spot: (start of the move, target, amount) — lands just before its word
        sp = lambda tw: tw - SPOT_MOVE * 0.8
        self.spot = [(self.t_in, _centre("genset"), 0.0),
                     (sp(self.bukan), _centre("genset"), 1.0), (T["L03"].start, _centre("genset"), 0.0),
                     (sp(self.genset), _centre("genset"), 1.0), (sp(self.network), _centre("kabel"), 1.0),
                     (sp(self.storage), _centre("peti"), 1.0), (sp(self.jam), _centre("nota"), 1.0),
                     (sp(self.kru), _centre("kru"), 1.0), (b[3] - 0.2, _centre("kru"), 0.0),
                     (b[4] + 0.4, _centre("kru"), 1.0)]
        self.lit_at = dict(genset=self.genset, kabel=self.network, peti=self.storage, nota=self.jam, kru=self.kru)


def spot_at(t, keys):
    """(x, y, amount) of the follow spot at t: each key glides from the previous state on apple_in_out."""
    x, y = keys[0][1]
    a = keys[0][2]
    for t0, (tx, ty), ta in keys[1:]:
        if t < t0:
            break
        p = INOUT(clamp(prog(t, t0, SPOT_MOVE)))
        x, y, a = lerp(x, tx, p), lerp(y, ty, p), lerp(a, ta, p)
    return x, y, a


def lit_at(t, Q, spot):
    """Each prop lights when the spot first lands on it and stays lit; before that only the spot itself lights it."""
    sx, sy, sa = spot
    out = {}
    for name, tl in Q.lit_at.items():
        cx, cy = _centre(name)
        near = clamp(1.3 - ((cx - sx) ** 2 + (cy - sy) ** 2) ** 0.5 / SPOT_R) * sa
        out[name] = max(near, clamp(prog(t, tl - 0.15, 0.4)))
    return out


def build(project):
    T = project.timing
    v = Video(duration=T["L19"].end + TAIL, bpm=110, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="marimba", key="D", mood="bright")   # ai-gratis cinematic E tense, wifi-ep03 lofi G dreamy
    v.sfx_kit = "wood"
    v.cover = lambda c: cover(c, "Yang jagain\nAI-nya *siapa*?", kicker="KARIER CLOUD", color=PURPLE,
                              badge="kru sound", tags=["GPU", "network", "biaya"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(3):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    Q = Cue(T, b)
    hero(v, T, Q)
    intro(v, T, Q, b[0], b[1])
    kolong(v, T, Q, b[1], b[2])
    kru(v, T, Q, b[2], b[3])
    skill(v, T, Q, b[3], b[4])
    recap(v, T, Q, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L19", PURPLE,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="“panggung”", sub="mulai jadi kru-nya"))
    v.cover_t = Q.kru + 1.2
    return v


# ── the stage: one object from the first line to the recap ───────────────────────────────────────────────────────
def stage_state(t, Q):
    sp = spot_at(t, Q.spot)
    run = (clamp(prog(t, Q.genset - 0.2, 0.5)) - 0.75 * clamp(prog(t, Q.selesai, 0.8))
           + 0.75 * clamp(prog(t, Q.b[4], 0.8)))
    pack = {k: clamp(prog(t, follow(Q.container, i), 0.45)) * (1 - clamp(prog(t, Q.b[3] - OUT, OUT)))
            for i, k in enumerate(("genset", "kabel", "peti", "nota"))}
    return dict(lit=lit_at(t, Q, sp), spot=(sp[0], sp[1], SPOT_R, sp[2]), run=run, pack=pack,
                swap=clamp(prog(t, arrive(Q.ganti), 0.7)), show=clamp(prog(t, Q.t_in + 0.4, 0.8)))


def hero(v, T, Q):
    b = Q.b
    rig = Rig(x=RX, y=RY, s=2.2, a=0.0)
    rig.to(Q.t_in, preset="silk", s=1.0, a=1.0)                       # full-bleed shrink, lands on "training"
    rig.to(arrive(Q.panggung) - 0.4, preset="silk", s=0.45, y=820)     # becomes the big one of three
    rig.to(b[4] + 0.2, preset="silk", s=0.82, y=1060)                  # back for the recap
    t_copy = follow(arrive(Q.panggung), 2)
    copies = [(230, 1180), (780, 1180)]

    def small(c, t, i, cx, cy):
        s = 0.27
        box = (cx - 550 * s, cy - 500 * s, 1100 * s, 1000 * s)

        def draw(c):
            with c.at(cx, cy, s, origin=(0, 0)):
                panggung(c, *HB, t, lit={k: 1.0 for k in G["items"]}, run=1.0, swap=float(i == 0), look=LOOK,
                         color=PURPLE)
        rise(c, t, follow(t_copy, i), b[4] - OUT, box, draw)

    def draw(c, t):
        op = 1 - prog(t, b[5] - OUT, OUT)
        st = stage_state(t, Q)
        with c.group(op):
            with rig.place(c, t):
                panggung(c, *HB, t, look=LOOK, color=PURPLE, **st)
            for i, (cx, cy) in enumerate(copies):
                small(c, t, i, cx, cy)
    v.add(Q.t_in, b[5] + 0.05, draw, z=10, bleed=True)
    v.sfx("whoosh", Q.t_in, 0.5)
    v.sfx("tick", Q.bukan, 0.5)
    for tt in (Q.genset, Q.network, Q.storage, Q.jam):
        v.sfx("tick", tt, 0.6)
    v.sfx("chime", Q.kru, 0.6)
    for i in range(4):
        v.sfx("pop", follow(Q.container, i), 0.35)
    v.sfx("whoosh", arrive(Q.panggung) - 0.4, 0.5)
    v.sfx("pop", t_copy, 0.4)
    v.sfx("pop", follow(t_copy, 1), 0.4)
    v.sfx("whoosh", b[4] + 0.2, 0.4)
    v.sfx("pop", arrive(Q.ganti), 0.5)


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w / 1100, h / 1000) * 1.02
    with c.at(x + w / 2, y + h / 2, s, origin=(0, 0)):
        kx, ky = _centre("kru")
        panggung(c, *HB, 0.0, lit={k: 1.0 for k in G["items"]}, spot=(kx, ky, SPOT_R, 1.0), run=1.0, look=LOOK,
                 color=PURPLE)


def _tag(c, t, t_in, t_out, x, y, label, color=PURPLE, align="l"):
    fade(c, t, t_in, t_out, lambda c: pop_tag(c, t, t_in, x, y, label, color, align=align))


# ── INTRO: the stage lands from full-bleed; the spot peeks under the deck on "bukan" ─────────────────────────────────
def intro(v, T, Q, s, e):
    hs = [(Headline("Fondasi buat\n*training* AI."), T["L01"].start, T["L02"].start - 0.15),
          (Headline("Yang ngurus?\n*Bukan* AI."), T["L02"].start, T["L03"].start - 0.15)]
    h3 = Headline("AI ~gantiin~.\nAI *butuh*.")

    def draw(c, t):
        kicker(c, t, T["L01"].start, e - OUT, "PENGALAMAN SENDIRI", PURPLE)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        h3.draw(c, t, T["L03"].start, e - OUT, strike_at=Q.gantiin + 0.25, reveal="wipe", exit="quiet")
    v.add(s, e, draw, z=20)
    v.sfx("thud", Q.butuh, 0.8)
    dolly(v, Q.training + 0.9, Q.bukan - SPOT_MOVE - 0.1)
    dolly(v, Q.butuh + 0.6, e - 0.2, base=1.03)


# ── 00 · KOLONG PANGGUNG: the spot finds generator (GPU), cable (network), road case (storage), slip (cost) ──────────
def kolong(v, T, Q, s, e):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("Biduan\n*hajatan*.", "L04"), ("Yang kamu\n*lihat*.", "L05"), ("Di kolongnya:\n*GPU*.", "L06"),
                   ("Kabel, peti:\n*network*.", "L07"), ("Nota sewa\nper *jam*.", "L08")], e - OUT)
    t_ai = arrive(Q.biduan, "snappy")
    sx, sy = scr(G["singer"][0], G["singer"][1] - G["singer"][2])
    it = {k: scr(*G["items"][k][:2]) for k in G["items"]}

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "00 · KOLONG PANGGUNG", col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        _tag(c, t, t_ai, b_end(Q, 2), sx - 30, sy - 70, "AI")
        _tag(c, t, Q.genset, b_end(Q, 2), X + 20, it["genset"][1] - 60, "GPU")
        _tag(c, t, Q.network, b_end(Q, 2), it["kabel"][0] - 10, it["kabel"][1] - 60, "network")
        _tag(c, t, Q.storage, b_end(Q, 2), it["peti"][0] - 10, it["peti"][1] - 60, "storage")
        _tag(c, t, Q.jam, b_end(Q, 2), X + CW, it["nota"][1] - 56, "biaya · per jam", align="r")
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", t_ai, 0.5)
    dolly(v, t_ai + 0.9, Q.genset - SPOT_MOVE - 0.1)
    dolly(v, Q.jam + 0.9, e - 0.2, base=1.03)


def b_end(Q, n):
    return Q.b[n] - OUT


# ── 01 · KRU SOUND: the spot climbs to the wing — the crew; generator on → scaled down; inference ready; containers ──
def kru(v, T, Q, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("Yang jagain:\n*kru sound*.", "L09"), ("GPU nyala,\nlalu *turun*.", "L10"),
                   ("Inference\nselalu *siap*.", "L11"), ("Semua di\n*container*.", "L12"),
                   ("Nggak bisa\n*sendiri*.", "L13")], e - OUT)
    kx, ky = scr(*G["items"]["kru"][:2])
    gx, gy = scr(*G["items"]["genset"][:2])
    sx, sy = scr(G["singer"][0], G["singer"][1] - G["singer"][2])
    t_kru = arrive(Q.kru, "snappy")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "01 · KRU SOUND", col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        _tag(c, t, follow(t_kru, 1), e - OUT, X + CW, ky - 60, "cloud engineer", align="r")
        fade(c, t, follow(t_kru, 3), Q.train - 0.2, lambda c: note(c, X + 470, 720, "ini kamu", 1.0,
                                                                  arrow_to=(kx + 60, ky + 10)))
        _tag(c, t, Q.train, Q.selesai - 0.1, X + 20, gy - 60, "training · nyala")
        _tag(c, t, Q.selesai, e - OUT, X + 20, gy - 60, "selesai · di-scale turun")
        _tag(c, t, Q.siap, e - OUT, sx - 120, sy - 70, "inference · selalu siap")
        _tag(c, t, follow(Q.container, 4), e - OUT, X + 20, 1110, "container · bisa pindah cloud")
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", follow(t_kru, 1), 0.5)
    v.sfx("pop", Q.train, 0.4)
    v.sfx("tick", Q.selesai, 0.5)
    v.sfx("pop", Q.siap, 0.5)
    v.sfx("pop", follow(Q.container, 4), 0.4)
    dolly(v, follow(t_kru, 3) + 0.9, Q.train - 0.2, x=kx, y=ky + 100)
    dolly(v, Q.sendiri - 0.6, e - 0.2, base=1.03)


# ── 02 · SKILL-NYA: the stage shrinks into the big one of three; three skill pills; "Berubah. Bukan ~hilang~." ───────
def skill(v, T, Q, s, e):
    col = tk.CHAPTER[2][0]
    hs = [(Headline("Makin banyak\n*panggung*."), T["L14"].start, T["L15"].start - 0.15),
          (Headline("Yang ngerti\n*panggungnya*."), T["L15"].start, T["L16"].start - 0.15)]
    h3 = Headline("*Berubah*.\nBukan ~hilang~.")
    pills = [(230, "GPU"), (505, "network"), (780, "biaya")]

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · SKILL-NYA", col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        h3.draw(c, t, T["L16"].start, e - OUT, strike_at=Q.hilang, reveal="wipe", exit="quiet")
        for (cx, label), tw in zip(pills, Q.skills):
            t0 = arrive(tw, "snappy")
            rise(c, t, t0, e - OUT, (cx - 120, 1370, 240, 60),
                 lambda c, cx=cx, label=label: tag_center(c, cx, 1380, label, PURPLE, h=52))
    v.add(s, e, draw, z=20)
    cut(v, s)
    for tw in Q.skills:
        v.sfx("pop", arrive(tw, "snappy"), 0.5)
    v.sfx("thud", Q.hilang + 0.1, 0.8)
    dolly(v, arrive(Q.skills[-1], "snappy") + 0.9, Q.hilang - 0.3)
    dolly(v, Q.hilang + 0.9, e - 0.2, base=1.03)


# ── RECAP (dark): the stage comes back; the singer is swapped, the spot stays on the crew ─────────────────────────────
def recap(v, T, Q, s, e):
    t_p = _w(T, "L17", "panggungnya", 0.55)
    hs = [(Headline("Biduannya\nboleh *ganti*.", style="headline_dark"), T["L17"].start, t_p - 0.15),
          (Headline("Panggungnya butuh\n*orang*.", style="headline_dark"), t_p, e - OUT)]

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", PURPLE)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
    v.add(s, e, draw, z=20)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    dolly(v, Q.orang + 0.3, e - 0.2)
    cut(v, e)
