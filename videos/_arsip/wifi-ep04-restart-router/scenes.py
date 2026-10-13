"""Bongkar WiFi Rumah EP 04 — Restart router beneran ngefek? QUICK, classic + Apple craft, material paper (big hero).
See PLAN.md.

Metaphor: the guard's guestbook. The router (the guard at the gate, EP 02) writes every connection into a book, one
row each — the NAT table. The page fills, new guests wait; a restart tears the page out and the book is clean (00).
Problems outside the book — a cut cable, the ISP, a wet splice (EP 01–03) — don't tear with it (01). Restart once is
fine; a binding full of torn stubs is a symptom (02, RECAP).
Signature: the right page rips off the binding and falls away, a clean page underneath; every tear leaves a stub.
Motion: rise headlines · one persistent hero (Rig) + depth_swap-style fall-backs behind the episode cards / the modem ·
quiet exits · silk springs for the book, smooth for cards/tags, snappy only for stamps and the check · camera only
dollies in holds + cuts.
Sound: styled score garage F warm 128 + soft SFX kit (ai-butuh-cloud-engineer marimba/wood, ai-gratis cinematic/mech).
"""
from engine import Video, tokens as tk
from engine.ease import clamp, prog, lerp, curve
from engine.video import draw_background
from engine.components import (Headline, kicker, fade, pop_tag, note, check_badge, brand_intro, series_bumper,
                               standard_outro, cover, Rig, arrive, follow, rise, dolly, cut, ios_at, heads, draw_heads,
                               modem, stempel, buku_tamu, material as mat, BUKU_RED as RED)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                             # long brand sting (version 2): voice starts under its wipe
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · BUKU TAMU", "01 · KAPAN PERCUMA", "02 · YANG BISA KAMU LAKUIN", "RECAP", "OUTRO"]
APPLE_OUT, APPLE_IN = curve("apple_out"), curve("apple_in")
LOOK = "paper"
BW = 900                                    # book width in its own px (the Rig scales it); height 0.64 BW
BH = BW * 0.64
TEAR = 0.8                                  # one page falling away
ROWS = [dict(jam="19.02", tamu="HP", ke="video"), dict(jam="19.02", tamu="HP", ke="chat"),
        dict(jam="19.03", tamu="laptop", ke="meeting"), dict(jam="19.05", tamu="TV", ke="streaming"),
        dict(jam="19.05", tamu="HP 2", ke="game"), dict(jam="19.06", tamu="tablet", ke="update"),
        dict(jam="19.06", tamu="laptop", ke="backup"), dict(jam="19.07", tamu="HP", ke="musik")]
CARDS = (("EP 01 · LAMPU LOS", "Kabel putus"), ("EP 02 · DARI ISP", "Gangguan ISP"),
         ("EP 03 · PAS HUJAN", "Sambungan basah"))
CARD_H, CARD_GAP, CARD_Y = 176, 34, 600
MODEM_C, MODEM_W = (MID, 870), 560


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words oddly)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


class Cue:
    """Every time the hero reacts to, computed once from the voice."""

    def __init__(self, T, b):
        self.b = b
        self.chat = T["L01"].start - 0.15
        self.tamu = _w(T, "L03", "tamu", 0.85)
        self.book = self.tamu - 0.75
        # 00 — rows ink in, the page fills, the queue waits, the page is torn out
        r1 = arrive(_w(T, "L04", "nyatet", 0.75))
        r2 = [arrive(_w(T, "L05", w, f)) for w, f in (("app", 0.2), ("internet", 0.5), ("baris", 0.9))]
        self.nat = arrive(_w(T, "L06", "NAT", 0.2))
        self.penuh = arrive(_w(T, "L07", "penuh", 0.45))
        self.memory = follow(self.penuh, 2)
        self.rows = [r1] + r2 + [self.penuh - 0.42 + 0.1 * k for k in range(4)]
        self.nunggu = arrive(_w(T, "L08", "nunggu", 0.35))
        self.sobek = arrive(_w(T, "L09", "nyobek", 0.35), "snappy")
        # 01 — three episode cards in front of the book, then the book tears twice behind them
        self.cards = [arrive(_w(T, lid, w, f)) for lid, w, f in (("L11", "putus", 0.55), ("L12", "luar", 0.6),
                                                                  ("L13", "tiga", 0.9))]
        self.back = T["L14"].start - 0.1
        t14 = [_w(T, "L14", "diganti", 0.3), _w(T, "L14", "berkali-kali", 0.5)]
        self.rusak = arrive(_w(T, "L14", "rusak", 0.95))
        # 02 — modem off/on, check; then a tear every day; tags
        self.modem = b[3] + 0.15
        self.cabut = _w(T, "L15", "cabut", 0.45)
        self.colok = _w(T, "L15", "colok", 0.85)
        self.lancar = arrive(_w(T, "L16", "penuh", 0.85), "snappy")
        self.hari = T["L17"].start + 0.1
        t17 = [arrive(_w(T, "L17", "tiap", 0.4)) + 0.38 * k for k in range(4)]
        self.kewalahan = arrive(_w(T, "L17", "kewalahan", 0.9))
        self.tags = [arrive(_w(T, "L18", "firmware", 0.35)), arrive(_w(T, "L18", "ISP", 0.75))]
        # RECAP — one more tear, then the stamp
        t19 = arrive(_w(T, "L19", "restart", 0.9), "snappy")
        self.gejala = arrive(_w(T, "L20", "gejala", 0.95), "snappy")
        tears = [self.sobek] + t14 + [self.colok - 0.55] + t17 + [t19]
        for i in range(1, len(tears)):                           # strictly in order, ≥ 0.3 s apart
            tears[i] = max(tears[i], tears[i - 1] + 0.3)
        self.tears = tears
        # a page flies for TEAR s, or until the next tear starts (the L17 "page a day" run flicks faster)
        self.tear_durs = [min(TEAR, tears[i + 1] - tears[i]) for i in range(len(tears) - 1)] + [TEAR]


def build(project):
    T = project.timing
    v = Video(duration=T["L22"].end + TAIL, bpm=128, beat_offset=0.0, series="BONGKAR WIFI RUMAH · EP 04")
    brand_intro(v, version=2)
    v.music = dict(style="garage", key="F", mood="warm")    # ai-butuh-cloud-engineer marimba D, ai-gratis cinematic E
    v.sfx_kit = "soft"
    v.cover = lambda c: cover(c, "Restart router,\n*ngefek*?", kicker="BONGKAR WIFI RUMAH · EP 04", color=RED,
                              badge="EP 04", tags=["NAT table", "memory", "kapan percuma"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    Q0 = _w(T, "L03", "tamu", 0.85)
    bump0 = max(Q0 + 1.0, T["L03"].end + 0.1)
    bump1 = bump0 + 1.35
    b[1] = max(b[1], bump0 + 0.45)                           # chapter switch hidden under the bumper
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(3):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 4, "Restart router", RED,
                                                   title=("BONGKAR", "WIFI RUMAH")), z=100)
    v.sfx("whoosh", bump0)
    Q = Cue(T, b)
    Q.bump1 = bump1
    v.stage = lambda c, t: (draw_background(c, v, t), mat.stage(c, LOOK, RED, 1 - v.dark_amount(t)))
    v.finish = lambda c, t: mat.finish(c, LOOK, 1 - v.dark_amount(t))
    hero(v, T, Q)
    intro(v, T, Q, b[0], b[1])
    buku(v, T, Q, b[1], b[2])
    percuma(v, T, Q, b[2], b[3])
    lakuin(v, T, Q, b[3], b[4])
    recap(v, T, Q, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L22", RED,
                   teaser=dict(kicker="BONGKAR WIFI RUMAH · EP 05", title="Lemot jam 8 malam.",
                               sub="Episode terakhir: internetmu lagi dibagi."))
    v.cover_t = Q.penuh + 1.0
    return v


# ── the guestbook: one object from L03 to the recap ───────────────────────────────────────────────────────────────
def page(k, t, Q):
    """(rows, fill, stamp, stamp_p) of page k (0 = the first page; page k is on top after tear k − 1)."""
    if k == 0:
        fill = sum(clamp(prog(t, tr, 0.35)) for tr in Q.rows) / len(ROWS)
        return ROWS, fill, "PENUH", clamp(ios_at(t, follow(Q.penuh, 1), "snappy"))
    if 4 <= k <= 7:                                          # L17: a page a day — they fill up again as it starts
        return ROWS[:3], APPLE_OUT(prog(t, Q.hari + 0.3, 0.4)), None, 0.0
    if k >= 8:                                               # recap: filling up again
        return ROWS[:3], 1.0, "GEJALA", clamp(ios_at(t, Q.gejala, "snappy"))
    return (), 0.0, None, 0.0


def book_args(t, Q):
    k = sum(1 for tt, d in zip(Q.tears, Q.tear_durs) if t >= tt + d)   # pages fully gone
    top = page(k, t, Q)
    under = page(k + 1, t, Q)
    tear = clamp(prog(t, Q.tears[k], Q.tear_durs[k])) if k < len(Q.tears) else 0.0
    stubs = sum(clamp(prog(t, tt + 0.2, 0.3)) for tt in Q.tears)
    mem = 0.15 + 0.4 * page(0, t, Q)[1] + 0.35 * APPLE_OUT(prog(t, Q.memory, 0.6))
    mem = lerp(mem, 0.12, APPLE_OUT(prog(t, Q.sobek + 0.3, 0.6)))           # the tear empties memory too
    mem = lerp(mem, 0.95, APPLE_OUT(prog(t, Q.kewalahan, 0.7)))
    return dict(rows=top[0], fill=top[1], stamp=top[2], stamp_p=top[3], under=under[0], under_fill=under[1],
                tear=tear, stubs=stubs, mem=mem)


def hero(v, T, Q):
    b = Q.b
    rig = Rig(x=MID, y=930, s=2.4, a=0.0)
    rig.to(Q.book, preset="silk", s=1.0, a=1.0)
    rig.to(b[2] + 0.1, preset="silk", y=1010, s=0.86)
    rig.to(Q.back, preset="silk", y=950, s=0.95)
    rig.to(b[3] + 0.05, preset="silk", y=1280, s=0.8)
    rig.to(Q.hari, preset="silk", y=930, s=1.0)
    rig.to(b[4] + 0.1, preset="silk", y=980, s=0.98)

    def draw(c, t):
        op = 1 - APPLE_IN(prog(t, b[5] - OUT, OUT))
        with c.group(op):
            with rig.place(c, t):
                buku_tamu(c, -BW / 2, -BH / 2, BW, look=LOOK, color=RED, **book_args(t, Q))
    v.add(Q.book, b[5] + 0.05, draw, z=10, bleed=True)
    v.sfx("whoosh", Q.book, 0.5)
    for tt in Q.rows[:4]:
        v.sfx("tick", tt + 0.1, 0.4)
    v.sfx("tick", Q.penuh, 0.5)
    v.sfx("thud", follow(Q.penuh, 1) + 0.08, 0.5)
    for k, tt in enumerate(Q.tears):
        v.sfx("whoosh", tt, 0.7 if k == 0 else 0.35)
    v.sfx("thud", Q.gejala + 0.08)


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w / BW, h / BH) * 0.95
    with c.at(x + w / 2, y + h / 2, s, origin=(0, 0), rot=-0.03):
        buku_tamu(c, -BW / 2, -BH / 2, BW, rows=ROWS, fill=1.0, stamp="PENUH", stamp_p=1.0, stubs=2, mem=0.92,
                  look=LOOK, color=RED)


# ── INTRO: the CS line — then the guestbook arrives on "tamu" ────────────────────────────────────────────────────────
def intro(v, T, Q, s, e):
    hs = [(Headline("Sembuh, atau\n*buang waktu*?"), T["L02"].start, T["L03"].start - 0.15),
          (Headline("Bedanya di\nbuku *tamu*."), T["L03"].start, e - OUT)]
    box = (X + 20, 760, CW - 40, 300)

    def chat(c):
        x, y, w, h = box
        mat.body(c, LOOK, mat.rrect_path(x, y, w, h, L["radius_bento"]), box, C["card"], r=L["radius_bento"])
        c.circle(x + 70, y + 72, 26, RED)
        c.text(x + 70, y + 81, "CS", F["mono_bold"], 20, C["card"], 1, 0.06, align="c")
        c.text(x + 116, y + 66, "CS · INTERNET RUMAH", F["mono_med"], 22, C["ink2"], 1, 0.16)
        c.text(x + 116, y + 98, "barusan", F["mono"], 20, C["muted"], 1, 0.06)
        c.fill_rrect(x + 44, y + 140, w - 88, 112, 56, C["bg"])
        c.text(x + 84, y + 212, "“Udah dicoba restart, Kak?”", F["ui_semi"], 44, C["ink"], 1, -0.01)

    def draw(c, t):
        kicker(c, t, T["L01"].start, e - OUT, "BONGKAR WIFI RUMAH · EP 04", RED)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
        rise(c, t, Q.chat, Q.book, box, chat, preset="smooth")
    v.add(s, e, draw, z=20)
    v.sfx("pop", Q.chat + 0.1, 0.6)
    dolly(v, Q.chat + 1.0, Q.book - 0.2)


# ── 00 · BUKU TAMU: a row per connection — full — wait — torn out ───────────────────────────────────────────────────
def buku(v, T, Q, s, e):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("Satu koneksi,\nsatu *baris*.", "L04"), ("Halamannya\n*terbatas*.", "L06"),
                   ("Penuh, tamu\n*nunggu*.", "L07"), ("Restart, buku\n*bersih*.", "L09")], e - OUT)
    y_tag = 1250

    def draw(c, t):
        kicker(c, t, max(s + 0.2, Q.bump1 - 0.3), e - OUT, "00 · BUKU TAMU", col)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
        fade(c, t, Q.nat, Q.sobek, lambda c: pop_tag(c, t, Q.nat, X + CW - 20, y_tag, "NAT table", col, align="r"))
        fade(c, t, Q.nunggu, Q.sobek, lambda c: pop_tag(c, t, Q.nunggu, X + 20, y_tag, "tamu baru · nunggu",
                                                        C["orange_pill"]))
    v.add(s, e, draw, z=20)
    v.sfx("pop", Q.nat, 0.5)
    v.sfx("pop", Q.nunggu, 0.5)
    dolly(v, Q.nat + 0.9, Q.penuh - 0.5)
    dolly(v, Q.sobek + TEAR + 0.3, e - 0.2, base=1.02)


# ── 01 · KAPAN PERCUMA: three episode cards in front of the book — the book tears, the road stays broken ────────────
def percuma(v, T, Q, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("Cuma yang di\n*dalam* router.", "L10"), ("Jalannya tetap\n*rusak*.", "L14")], e - OUT)
    rots = (-0.025, 0.02, -0.015)

    def card(c, i, t):
        x, y, w, h = X + 30, CARD_Y + i * (CARD_H + CARD_GAP), CW - 60, CARD_H
        kick, title = CARDS[i]
        mat.body(c, LOOK, mat.rrect_path(x, y, w, h, 28), (x, y, w, h), C["card"], r=28)
        c.text(x + 44, y + 62, kick, F["mono_med"], 22, C["ink2"], 1, 0.16)
        c.text(x + 44, y + 136, title, F["display"], 58, C["ink"], 1, -0.04)
        stempel(c, x + w - 130, y + h / 2 + 6, "DI LUAR", clamp(ios_at(t, follow(Q.cards[i], 3), "snappy")), RED, 30,
                rot=-0.14 + 0.08 * i)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "01 · KAPAN PERCUMA", col)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
        back = APPLE_OUT(prog(t, Q.back, 0.6))                   # the cards fall back, the book comes forward
        for i in range(3):
            y = CARD_Y + i * (CARD_H + CARD_GAP)
            bb = (X + 30, y, CW - 60, CARD_H)
            with c.at(0, 0, lerp(1.0, 0.94, back), origin=(MID, y + CARD_H / 2), rot=rots[i]):
                with c.group(lerp(1.0, 0.18, back)):
                    rise(c, t, Q.cards[i], e - OUT, bb, lambda c, i=i: card(c, i, t), preset="smooth")
    v.add(s, e, draw, z=20)
    cut(v, s)
    for i, tt in enumerate(Q.cards):
        v.sfx("pop", tt + 0.1, 0.55)
        v.sfx("thud", follow(tt, 3) + 0.1, 0.35)
    dolly(v, follow(Q.cards[2], 3) + 0.5, Q.back - 0.1)
    dolly(v, Q.rusak + 0.5, e - 0.2, base=1.02)


# ── 02 · YANG BISA KAMU LAKUIN: unplug once — a page a day is a different story ─────────────────────────────────────
def lakuin(v, T, Q, s, e):
    col = tk.CHAPTER[2][0]
    hs = heads(T, [("Restart\n*sekali*.", "L15"), ("Tiap hari?\nItu *kewalahan*.", "L17")], e - OUT)
    mbox = (MODEM_C[0] - MODEM_W / 2, MODEM_C[1] - 330, MODEM_W, 450)

    def lights(t):
        if t < Q.cabut:
            return dict(POWER="g", PON="g", LOS="", INTERNET="g", WLAN="g")
        on = [n for k, n in enumerate(("POWER", "PON", "INTERNET", "WLAN")) if t >= Q.colok + 0.25 * k]
        return {n: ("g" if n in on else "") for n in ("POWER", "PON", "LOS", "INTERNET", "WLAN")}

    def draw_modem(c, t):
        modem(c, MODEM_C[0], MODEM_C[1], MODEM_W, t, lights(t))
        p = clamp(ios_at(t, Q.lancar, "snappy"))
        if p > 0.002:
            check_badge(c, MODEM_C[0] + MODEM_W / 2 - 10, MODEM_C[1] - 120, 34, p)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · YANG BISA KAMU LAKUIN", col)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
        rise(c, t, Q.modem, Q.hari, mbox, lambda c: draw_modem(c, t), preset="smooth")
        fade(c, t, follow(Q.lancar, 2), Q.hari, lambda c: note(c, X + 40, 1022, "bukunya yang penuh", 1.0,
                                                                 arrow_to=(MID + 120, 1060)))
        fade(c, t, Q.tags[0], e - OUT, lambda c: pop_tag(c, t, Q.tags[0], X + 20, 1260, "update firmware", col))
        fade(c, t, Q.tags[1], e - OUT, lambda c: pop_tag(c, t, Q.tags[1], X + 20, 1330, "minta ISP ganti modem",
                                                         col))
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("pop", Q.modem + 0.1, 0.5)
    v.sfx("click", Q.cabut, 0.7)
    v.sfx("click", Q.colok, 0.7)
    v.sfx("chime", Q.lancar + 0.1, 0.6)
    for tt in Q.tags:
        v.sfx("pop", tt + 0.05, 0.5)
    dolly(v, Q.tags[1] + 0.9, e - 0.2)


# ── RECAP (dark): the same book, a binding full of stubs — stamped GEJALA ───────────────────────────────────────────
def recap(v, T, Q, s, e):
    hs = heads(T, [("Server juga\n*sembuh*.", "L19"), ("Bukan obat.\nItu *gejala*.", "L20")], e - OUT,
               style="headline_dark")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", RED)
        draw_heads(c, t, hs, reveal="rise", exit="quiet")
    v.add(s, e, draw, z=20)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    dolly(v, Q.gejala + 0.9, e - 0.2)
    cut(v, e)
