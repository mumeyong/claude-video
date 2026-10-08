"""Motion lab — proof sheet for components/kinetic.py (STYLE §6d). Not for posting.

Each chapter shows the old move first (LAMA tag), then the new one (BARU tag), so the difference is visible
side by side in time. Reference: @davianmotion (persistent hero, type that arrives, light swaps, dim exits).
"""
from engine import Video, tokens as tk
from engine.ease import prog, in_out_cubic
from engine.components import (Headline, kicker, appear, fade, phone, pop_tag, wobble, brand_intro, check_badge,
                               Rig, drifting, parallax, track_line, sheen, swap, lockup, curtain, spring_at)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
LEAD = 0.6
OUTRO_TAIL = 2.5
PRE_ROLL = 1.2
OLD, NEW = C["muted"], C["accent"]
PW, PH = 300, 620          # hero phone size (drawn around 0, 0)
NOTIF = (-118, -40, 236, 120)  # notification card on the phone screen, local coords


def build(project):
    T = project.timing
    v = Video(duration=T.line("L12").end + OUTRO_TAIL, bpm=128, beat_offset=0.0)
    brand_intro(v)
    v.music = dict(key="D", mood="dreamy")
    b = {n: T.chapter_span(n)[0] - LEAD for n in ("00 · TEKS", "01 · HERO", "02 · KAMERA", "OUTRO")}
    intro(v, T, 0.0, b["00 · TEKS"])
    teks(v, T, b["00 · TEKS"], b["01 · HERO"])
    hero(v, T, b["01 · HERO"], b["02 · KAMERA"])
    kamera(v, T, b["02 · KAMERA"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    v.cover_t = T.word("L07", "pindah") + 1.2
    return v


def _label(c, t, t_in, t_out, text, color, y=1500):
    fade(c, t, t_in, t_out, lambda c: pop_tag(c, t, t_in, X, y, text, color))


# ── INTRO: cold open out of darkness → LAMA × BARU lockup ───────────────
def intro(v, T, s, e):
    v.chapter(None, "MOTION LAB", s, e)
    L1, L2 = T["L01"], T["L02"]
    t_lock = T.word("L01", "lama")
    v.add(s, L1.start + 1.2, lambda c, t: curtain(c, t, L1.start - 0.4), z=100)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "MOTION LAB · KINETIC.PY", C["accent"])
        lockup(c, t, t_lock, e - M["dim_out"], tk.W / 2, 930, "LAMA", "BARU", style="headline_lg")
        track_line(c, t, L2.start + 0.1, e - M["dim_out"], X, 1180, "PILIH SATU.", "display", 88, C["ink"])
    v.add(s, e, draw)
    v.sfx("thud", t_lock + 0.45)
    v.sfx("whoosh", t_lock)
    v.sfx("pop", L2.start + 0.1)


# ── 00 · TEKS: blur-rise (old) → mask (new) → tracking collapse (new) ───
def teks(v, T, s, e):
    v.chapter(0, "TEKS", s, e)
    L3, L4, L5 = T["L03"], T["L04"], T["L05"]
    old = Headline("Semua video\n*sama* gerakannya.", y=640)
    new = Headline("Muncul dari\n*balik* garis.", y=640)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "00 · HEADLINE REVEAL", tk.CHAPTER[0][0])
        old.draw(c, t, L3.start + 0.1, L4.start - 0.3)
        _label(c, t, L3.start + 0.3, L4.start - 0.3, "LAMA · blur + rise", OLD)
        new.draw(c, t, L4.start + 0.1, L5.start - 0.3, reveal="mask", exit="mask")
        _label(c, t, L4.start + 0.3, L5.start - 0.3, "BARU · mask + spring", NEW)
        track_line(c, t, L5.start + 0.05, e - M["dim_out"], X, 800, "HURUF DEMI", "display", 104, C["ink"])
        track_line(c, t, T.word("L05", "tracking"), e - M["dim_out"], X, 910, "HURUF.", "display", 104,
                   C["accent"])
        _label(c, t, L5.start + 0.3, e - OUT, "BARU · tracking collapse · exit dim", NEW)
    v.add(s, e, draw)
    for t0 in (L3.start, L4.start, L5.start):
        v.sfx("whoosh", t0)


# ── 01 · HERO: exit+enter reset (old) → persistent Rig hero + sheen swap + dim (new) ─
def _screen(t, t_swap):
    def draw(c, sx, sy, sw, sh):
        c.fill_rrect(sx, sy, sw, sh, 0, C["d_bg"])
        c.text(sx + sw / 2, sy + 120, "9:41", F["display"], 64, C["d_ink"], 1, align="c")
        c.text(sx + sw / 2, sy + 150, "Senin, 8 Oktober", F["ui"], 18, C["d_muted"], 1, align="c")
        a_old, a_new = (1.0, 0.0) if t_swap is None else swap(t, t_swap)
        x, y, w, h = NOTIF
        x, y = x + sx + sw / 2, y + sy + sh / 2
        c.fill_rrect(x, y, w, h, 22, C["d_card"])
        c.stroke_rrect(x + 0.5, y + 0.5, w - 1, h - 1, 22, C["d_line"], 1.0)
        if a_old > 0.01:
            c.text(x + 22, y + 48, "PESANAN MASUK", F["mono_bold"], 18, C["d_accent"], a_old)
            c.text(x + 22, y + 84, "Order #2951", F["ui_semi"], 24, C["d_ink"], a_old)
        if a_new > 0.01:
            check_badge(c, x + 44, y + h / 2, 22, spring_at(t, t_swap + M["sheen_dur"] * 0.4, "snappy"))
            c.text(x + 80, y + 54, "TERKONFIRMASI", F["mono_bold"], 18, C["ok"], a_new)
            c.text(x + 80, y + 86, "Order #2951", F["ui_semi"], 24, C["d_ink"], a_new)
    return draw


def hero(v, T, s, e):
    v.chapter(1, "HERO", s, e)
    L6, L7, L8, L9 = T["L06"], T["L07"], T["L08"], T["L09"]
    t_reset = T.word("L06", "baru")
    t_move = T.word("L07", "pindah")
    t_side = L8.start
    t_swap = T.word("L08", "sapuan")
    t_dim = T.word("L09", "abu")

    # old: the same phone exits and a "new scene" re-enters from zero
    def old(c, t):
        box = (tk.W / 2 - PW / 2, 1000 - PH / 2, PW, PH)
        for t_in, t_out in ((L6.start, t_reset - 0.1), (t_reset + 0.25, L7.start - 0.35)):
            appear(c, t, t_in, t_out, box, lambda c: phone(c, *box, draw_screen=_screen(t, None)))
        _label(c, t, L6.start + 0.3, L7.start - 0.35, "LAMA · exit → enter from zero", OLD)
    v.add(s, L7.start, old)

    # new: one Rig hero for the rest of the chapter
    rig = Rig(tk.W / 2, 1000, s=0.9, a=0.0)
    rig.to(L7.start, a=1.0, s=1.0, preset="heavy")
    rig.to(t_move, x=X + PW / 2 + 20, rot=-0.035, preset="heavy", anticip=0.06)
    rig.to(t_side, x=X + CW - PW / 2 - 40, rot=0.03, preset="heavy", anticip=0.06)
    rig.to(t_dim, a=0.0, s=0.94, dur=M["dim_out"] * 2)

    def new(c, t):
        with drifting(c, t, L7.start, e, origin=(rig.state(t)["x"], 1000)):
            with rig.place(c, t, bbox=(-PW / 2 - 40, -PH / 2 - 40, PW + 80, PH + 80)):
                phone(c, -PW / 2, -PH / 2 + wobble(t, 2, 3), PW, PH, draw_screen=_screen(t, t_swap))
                x, y, w, h = NOTIF
                sheen(c, t, t_swap, (x + 0, y + wobble(t, 2, 3), w, h), r=22)
        # text sits on the side the phone left free (the phone swaps sides, like the reference)
        track_line(c, t, t_move + 0.25, t_side - 0.2, 520, 980, "NGGAK", "display", 96, C["ink"])
        track_line(c, t, t_move + 0.4, t_side - 0.2, 520, 1080, "PERGI.", "display", 96, C["accent"])
        track_line(c, t, t_side + 0.3, t_dim, X, 980, "GANTI", "display", 96, C["ink"])
        track_line(c, t, t_side + 0.45, t_dim, X, 1080, "ISI.", "display", 96, C["accent"])
        _label(c, t, L7.start + 0.3, t_side - 0.2, "BARU · Rig + anticip + heavy spring", NEW)
        _label(c, t, t_side + 0.3, t_dim, "BARU · sheen + swap", NEW)
        _label(c, t, t_dim, e - OUT, "BARU · exit dim", NEW)
    v.add(L7.start - 0.1, e, new)
    for t0 in (t_move, t_side):
        v.sfx("whoosh", t0)
    v.sfx("pop", t_swap + M["sheen_dur"] * 0.45)
    v.camera.key(L7.start, zoom=1.04, y=1000, dur=2.0).reset(t_dim, dur=1.0)


# ── 02 · KAMERA: flat zoom (old) → three parallax depths (new) ──────────
def _scene(c, t, v, layered):
    far, mid, near = (0.45, 1.0, 1.45) if layered else (1.0, 1.0, 1.0)
    with parallax(c, v, t, far):
        for i in range(7):
            for j in range(9):
                c.circle(X + 40 + i * 128, 620 + j * 110, 5, C["faint"])
    with parallax(c, v, t, mid):
        for k, (x, y, label) in enumerate(((X + 60, 760, "load balancer"), (X + 300, 980, "pod"),
                                           (X + 120, 1200, "node"))):
            c.card(x, y + wobble(t, k, 3), 420, 150)
            c.text(x + 34, y + 92 + wobble(t, k, 3), label, F["display_semi"], 44, C["ink"])
    with parallax(c, v, t, near):
        c.fill_rrect(X + 480, 700, 220, 64, 32, tk.CHAPTER[2][0])
        c.text(X + 590, 742, "depth 1,45", F["ui_semi"], 24, C["card"], align="c")


def kamera(v, T, s, e):
    v.chapter(2, "KAMERA", s, e)
    L10, L11 = T["L10"], T["L11"]

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · DEPTH", tk.CHAPTER[2][0])
        layered = t >= L11.start - 0.2
        a = 1 - in_out_cubic(prog(t, L11.start - 0.5, 0.3)) + in_out_cubic(prog(t, L11.start - 0.2, 0.3))
        a *= 1 - in_out_cubic(prog(t, e - OUT, OUT))
        with c.group(min(1.0, a)):
            _scene(c, t, v, layered)
        _label(c, t, L10.start + 0.3, L11.start - 0.4, "LAMA · semua ikut zoom", OLD)
        _label(c, t, L11.start + 0.1, e - OUT, "BARU · parallax 0,45 / 1 / 1,45", NEW)
    v.add(s, e, draw)
    cam = v.camera
    cam.key(L10.start, zoom=1.12, x=420, y=980, dur=2.2).reset(L10.end - 0.6, dur=0.6)
    cam.key(L11.start, zoom=1.14, x=420, y=980, dur=2.4).reset(e - 0.6, dur=0.6)
    v.sfx("whoosh", L11.start - 0.2)


# ── OUTRO: dark, mask headline + bookend lockup ─────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L12 = T["L12"]
    head = Headline("Mana yang\npaling *kerasa*?", y=620, style="headline_dark")

    def draw(c, t):
        head.draw(c, t, L12.start, e - M["dim_out"], reveal="mask", exit="dim")
        lockup(c, t, T.word("L12", "kabarin"), e - M["dim_out"], tk.W / 2, 1150, "LAMA", "BARU",
               style="headline_lg")
    v.add(s, e, draw)
    v.sfx("thud", T.word("L12", "kabarin") + 0.45)
