"""AI gratis itu — siapa yang bayar? QUICK, classic + Apple craft, material paper (big hero). See PLAN.md.

Metaphor: a cashier's thermal receipt. Twenty AI answers, every line Rp0, TOTAL Rp0 (INTRO) → the real cost lines
ink in faintly underneath: GPU, per hour, electricity, all "???" (00) → the receipt turns over: the back is full —
subscription, investor, iklan, data each get a green stamp, and "KAMU Rp0" (01) → the privacy switch sits in front of
the blurred receipt (02) → in the dark the receipt turns back and gets stamped "DITAGIH KE ORANG LAIN" (RECAP).
Signature: the receipt turns over on its vertical axis (peek in INTRO, full turn in 01, back in RECAP).
Motion: ink headlines · one persistent hero (Rig) + focus_pull · quiet exits · silk/hero springs, snappy only for
stamps and the switch · camera only dollies in holds + cuts.
Sound: styled score cinematic E tense 96 + mech SFX kit (wifi-ep03 lofi/glass, ai-butuh-listrik marimba/soft).
"""
from engine import Video, tokens as tk
from engine.ease import clamp, prog, curve
from engine.video import draw_background
from engine.components import (Headline, kicker, fade, pop_tag, note, brand_intro, standard_outro, cover, Rig, arrive, follow,
                               rise, focus_pull, dolly, cut, ios_at, heads, draw_heads, struk, stempel, saklar,
                               material as mat, KASIR_GREEN as GREEN)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                             # long brand sting (version 2): voice starts under its wipe
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · BIAYA ASLI", "01 · YANG NANGGUNG", "02 · BAGIANMU", "RECAP", "OUTRO"]
APPLE_OUT, APPLE_IN = curve("apple_out"), curve("apple_in")
LOOK = "paper"
SW = 600                                    # receipt width in its own px (the Rig scales it)
HERO_BOX = (60, 540, 960, 1060)             # screen box around the receipt (focus pull, layer bounds)
BACK_ROWS = (("01 subscription", "bulanan"), ("02 investor", "rugi dulu"), ("03 iklan", "tayang"),
             ("04 data", "training"))


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words oddly)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


def _ink(t, t0, dur=0.45):
    return APPLE_OUT(prog(t, t0, dur))


class Cue:
    """Every time the hero reacts to, computed once from the voice."""

    def __init__(self, T, b):
        self.b = b
        self.t_in = T["L01"].start - 0.1
        self.nol = arrive(_w(T, "L01", "nol", 0.75), "snappy")
        self.peek = arrive(_w(T, "L02", "baliknya", 0.8), "hero")
        self.unpeek = T["L03"].start + 0.1
        self.shrink = T["L04"].start - 0.2
        self.gpu = arrive(_w(T, "L04", "GPU", 0.65), "smooth")
        self.jam = arrive(_w(T, "L05", "jam", 0.45), "smooth")
        self.listrik = arrive(_w(T, "L05", "listriknya", 0.7), "smooth")
        self.kaget = arrive(_w(T, "L06", "kaget", 0.95), "smooth")
        self.strike = _w(T, "L07", "nol", 0.35)
        self.flip = arrive(_w(T, "L08", "balik", 0.2), "hero")
        self.rows = [arrive(_w(T, lid, w, 0.2), "smooth") for lid, w in
                     (("L09", "subscription"), ("L10", "investor"), ("L11", "iklan"), ("L12", "data"))]
        self.beda = arrive(_w(T, "L13", "beda", 0.8), "smooth")
        self.card = arrive(_w(T, "L14", "setting", 0.7), "smooth")
        self.mati = _w(T, "L15", "mati", 0.95)
        self.kantor = arrive(_w(T, "L16", "kantor", 0.5), "smooth")
        self.back = b[4] + 0.35
        self.tagih = arrive(_w(T, "L17", "orang", 0.85), "snappy")


def build(project):
    T = project.timing
    v = Video(duration=T["L19"].end + TAIL, bpm=96, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="cinematic", key="E", mood="tense")  # wifi-ep03 lofi G dreamy, ai-butuh-listrik marimba F
    v.sfx_kit = "mech"
    v.cover = lambda c: cover(c, "AI gratis,\n*siapa* bayar?", kicker="AI SEHARI-HARI", color=GREEN,
                              badge="Rp0", tags=["GPU", "subscription", "data"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(3):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    Q = Cue(T, b)
    v.stage = lambda c, t: (draw_background(c, v, t), mat.stage(c, LOOK, GREEN, 1 - v.dark_amount(t)))
    v.finish = lambda c, t: mat.finish(c, LOOK, 1 - v.dark_amount(t))
    hero(v, T, Q)
    intro(v, T, Q, b[0], b[1])
    biaya(v, T, Q, b[1], b[2])
    nanggung(v, T, Q, b[2], b[3])
    bagianmu(v, T, Q, b[3], b[4])
    recap(v, T, Q, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L19", GREEN, save_id="L18")
    v.cover_t = Q.flip + 1.2
    return v


# ── the receipt: one object from the first line to the recap ──────────────────────────────────────────────────────
def front_side(t, Q):
    grow = [_ink(t, Q.gpu - 0.25, 0.6), _ink(t, Q.gpu, 0.6), _ink(t, Q.jam, 0.6), _ink(t, Q.listrik, 0.6)]
    rows = [dict(l="jawaban #01", r="Rp0"), dict(l="jawaban #02", r="Rp0"), dict(l="   · · ·", r=""),
            dict(l="jawaban #20", r="Rp0")]
    for k, (l, r) in enumerate((("BIAYA ASLI", ""), ("GPU · data center", "???"), ("sewa per jam", "???"),
                                ("listrik nyala terus", "???"))):
        rows.append(dict(l=l, r=r, g=grow[k], a=_ink(t, (Q.gpu - 0.25, Q.gpu, Q.jam, Q.listrik)[k] + 0.2),
                         color=GREEN, kind="head" if k == 0 else None,
                         hi=_ink(t, Q.kaget, 0.6) if k == 1 else 0.0))
    total = dict(l="TOTAL", r="Rp0", a=_ink(t, Q.nol, 0.4), strike=APPLE_OUT(prog(t, Q.strike, 0.5)))
    return dict(title="WARUNG AI", sub="struk · hari ini", rows=rows, total=total, foot="terima kasih")


def back_side(t, Q):
    rows = []
    for k, (l, r) in enumerate(BACK_ROWS):
        dim = 0.7 * _ink(t, Q.beda, 0.6) if k in (1, 2) else 0.0
        rows.append(dict(l=l, r=r, a=_ink(t, Q.rows[k]) * (1 - dim), ph=f"0{k + 1}  · · · · · ·",
                         stamp=clamp(ios_at(t, follow(Q.rows[k], 2), "snappy")) * (1 - dim), stamp_text="LUNAS"))
    return dict(title="DIBAYAR OLEH", sub="biaya jawabanmu", rows=rows, total=dict(l="KAMU", r="Rp0"))


def flip_at(t, Q):
    return (0.22 * ios_at(t, Q.peek, "hero") - 0.22 * ios_at(t, Q.unpeek, "smooth")
            + ios_at(t, Q.flip, "hero") - ios_at(t, Q.back, "hero"))


def hero(v, T, Q):
    b = Q.b
    rig = Rig(x=MID, y=tk.H + 80, s=1.25)
    rig.to(Q.t_in, preset="silk", y=600)
    rig.to(Q.shrink, preset="silk", y=585, s=1.05)
    rig.to(Q.flip, preset="silk", y=600, s=1.3)
    rig.to(Q.back, preset="silk", y=650, s=1.0)

    def receipt(c, t):
        with rig.place(c, t):
            g = struk(c, -SW / 2, 0, SW, front_side(t, Q), back_side(t, Q), flip_at(t, Q), look=LOOK, color=GREEN)
            if g["total"] is not None and t > Q.back:
                stempel(c, 0, g["total"] - 6, "DITAGIH KE ORANG LAIN", ios_at(t, Q.tagih, "snappy"), GREEN, 34,
                        rot=-0.09)

    def draw(c, t):
        op = 1 - APPLE_IN(prog(t, b[5] - OUT, OUT))
        with c.group(op):
            focus_pull(c, t, Q.card - 0.15, b[4] - 0.7, HERO_BOX, lambda c: receipt(c, t))
    v.add(Q.t_in, b[5] + 0.05, draw, z=10, bleed=True)
    v.sfx("whoosh", Q.t_in, 0.5)
    v.sfx("tick", Q.nol, 0.6)
    v.sfx("whoosh", Q.peek, 0.4)
    for k, tt in enumerate((Q.gpu, Q.jam, Q.listrik)):
        v.sfx("tick", tt, 0.5)
    v.sfx("whoosh", Q.flip)
    v.sfx("thud", Q.flip + 0.35, 0.5)
    for tt in Q.rows:
        v.sfx("pop", follow(tt, 2) + 0.05, 0.6)
    v.sfx("whoosh", Q.back, 0.5)
    v.sfx("thud", Q.tagih + 0.1)


def _cover_hero(c, box):
    x, y, w, h = box
    Q = type("Q", (), {})()
    for k in ("nol", "gpu", "jam", "listrik", "strike"):
        setattr(Q, k, -10.0)
    Q.kaget = 1e9
    side = front_side(0.0, Q)
    s = min(w / SW, h / 900) * 0.92
    with c.at(x + w / 2, y, s, origin=(0, 0), rot=-0.04):
        g = struk(c, -SW / 2, 0, SW, side, flip=0.12, look=LOOK, color=GREEN)
        stempel(c, 0, g["total"] - 6, "DITAGIH KE ORANG LAIN", 1.0, GREEN, 34, rot=-0.09)


# ── INTRO: twenty answers, TOTAL Rp0 — the receipt peeks at its back ──────────────────────────────────────────────
def intro(v, T, Q, s, e):
    hs = heads(T, [("20 jawaban.\nTotal *Rp0*.", "L01"), ("Struk ini ada\n*baliknya*.", "L02"),
                   ("Yang bayar\n*siapa*?", "L03")], e - OUT)

    def draw(c, t):
        kicker(c, t, T["L01"].start, e - OUT, "AI GRATIS · HARI INI", GREEN)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
    v.add(s, e, draw, z=20)
    dolly(v, Q.nol + 0.9, Q.peek - 0.2)
    dolly(v, Q.unpeek + 1.2, e - 0.2, base=1.03)


# ── 00 · BIAYA ASLI: the real cost lines ink in under the Rp0 — GPU, per hour, electricity, all "???" ────────────────
def biaya(v, T, Q, s, e):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("Dihitung\ndi *GPU*.", "L04"), ("Disewa\nper *jam*.", "L05"), ("Baris yang bikin\n*kaget*.", "L06"),
                   ("Bukan nol.\nBukan *kamu*.", "L07")], e - OUT)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "00 · BIAYA ASLI", col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
    v.add(s, e, draw, z=20)
    cut(v, s)
    dolly(v, Q.kaget + 0.9, Q.strike - 0.2)
    dolly(v, Q.strike + 1.0, e - 0.2, base=1.03)


# ── 01 · YANG NANGGUNG: the receipt turns over — four payers get stamped, then the mix differs per product ─────────
def nanggung(v, T, Q, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("Dibalik:\n*empat* nama.", "L08"), ("Campurannya\n*beda*.", "L13")], e - OUT)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "01 · YANG NANGGUNG", col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
        fade(c, t, follow(Q.beda, 3), e - OUT, lambda c: pop_tag(c, t, follow(Q.beda, 3), X, 1450,
                                                                 "contoh · tiap produk beda", GREEN))
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", follow(Q.beda, 3), 0.4)
    dolly(v, follow(Q.beda, 3) + 0.9, e - 0.2)


# ── 02 · BAGIANMU: a privacy-setting card in front of the (soft) receipt — the switch is yours ──────────────────────
def bagianmu(v, T, Q, s, e):
    col = tk.CHAPTER[2][0]
    hs = heads(T, [("Buka\n*setting*-nya.", "L14"), ("Kamu yang\n*mutusin*.", "L15"), ("Data kantor?\n*Jangan*.", "L16")],
               e - OUT)
    box = (X + 20, 760, CW - 40, 400)
    t_off = arrive(Q.mati, "snappy")

    def card(c, t):
        x, y, w, h = box
        c.card(x, y, w, h, r=L["radius_bento"], shadow="chat")
        c.text(x + 50, y + 74, "SETTING · PRIVASI", F["mono_med"], 22, C["ink2"], 1, 0.16)
        c.line(x + 50, y + 112, x + w - 50, y + 112, C["line"], 2)
        c.text(x + 50, y + 200, "Pakai obrolanku", F["ui_semi"], 40, C["ink"], 1, -0.01)
        c.text(x + 50, y + 252, "buat training model", F["ui_semi"], 40, C["ink"], 1, -0.01)
        c.text(x + 50, y + 330, "bisa diubah kapan aja", F["ui"], 26, C["muted"], 1, 0.0)
        saklar(c, x + w - 50 - 150, y + 170, 150, 1 - clamp(ios_at(t, t_off, "snappy")), GREEN)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · BAGIANMU", col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
        rise(c, t, Q.card, e - OUT, box, lambda c: card(c, t), preset="smooth")
        fade(c, t, follow(t_off, 4), e - OUT, lambda c: note(c, X + 40, 1270, "saklarnya punya kamu", 1.0,
                                                             arrow_to=(box[0] + box[2] - 160, box[1] + box[3] + 10)))
        fade(c, t, Q.kantor, e - OUT, lambda c: pop_tag(c, t, Q.kantor, X + 20, 1400, "versi gratis · bukan buat data kantor",
                                                        C["orange_pill"]))
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", Q.card, 0.6)
    v.sfx("click", t_off + 0.1)
    v.sfx("pop", Q.kantor, 0.5)
    dolly(v, Q.kantor + 0.9, e - 0.2)


# ── RECAP (dark): the receipt turns back to Rp0 — and gets stamped "ditagih ke orang lain" ────────────────────────
def recap(v, T, Q, s, e):
    t_g = _w(T, "L17", "gratis", 0.45)                       # the headline turns mid-line, on "Gratis"
    hs = [(Headline("Nggak ada\nbaris *nol*.", style="headline_dark"), T["L17"].start, t_g - 0.15),
          (Headline("Ditagih ke\n*orang lain*.", style="headline_dark"), t_g, e - OUT)]

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", GREEN)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
    v.add(s, e, draw, z=20)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    dolly(v, Q.tagih + 0.9, e - 0.2)
    cut(v, e)
