"""Apple lab — proof sheet for STYLE §6f (Apple motion craft). Not for posting.

One rule per chapter, written the way every new video should be written: one leader, big moves that ARRIVE on the
stressed word (arrive), followers (follow), holds with a camera dolly, quiet exits, continuity (depth_swap → Morph),
rack focus, and a slow–slow–snap tempo ending on a hard cut. Chapter 01 first shows the OLD way (everything at once,
overshoot + blur) so the difference is visible. Run `check apple-lab --dry`: the motion table should be flag-free.
"""
from engine import Video, tokens as tk
from engine.ease import clamp, out_back, prog
from engine.components import (Headline, kicker, fade, pop_tag, brand_intro, Morph, arrive, follow, rise,
                               depth_swap, focus_pull, dolly, cut, presence)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW = L["col_x"], L["col_w"]
PRE_ROLL = 2.05
LEAD = 0.5                 # chapter visuals start this long before the chapter's first line
OUT = M["quiet_out"]
TAIL = 2.6
NAMES = ("INTRO", "01 · LEADER", "02 · MENDARAT", "03 · TEKS", "04 · KONTINUITAS", "05 · FOKUS", "06 · TEMPO",
         "OUTRO")
OLD = C["muted"]


def build(project):
    T = project.timing
    v = Video(duration=T.line("L12").end + TAIL, bpm=80, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="ambient", key="C", mood="dreamy")
    v.sfx_kit = "glass"
    b = [max(0.0, T.chapter_span(n)[0] - LEAD) for n in NAMES] + [v.duration]
    b[0] = 0.0
    for i, fn in enumerate((intro, leader, mendarat, teks, kontinuitas, fokus, tempo, outro)):
        v.chapter(i if 0 < i < 7 else None, NAMES[i].split(" · ")[-1], b[i], b[i + 1])
        fn(v, T, b[i], b[i + 1], tk.CHAPTER[i][0] if 0 < i < 7 else C["accent"])
        if i:
            cut(v, b[i])           # reset any dolly while the frame is empty (old content gone, new not in yet)
    v.cover_t = T.word("L04", "mendarat") + 1.0
    return v


def _tag(c, t, t_in, t_out, text, color, y=1330):
    fade(c, t, t_in, t_out, lambda c: pop_tag(c, t, t_in, X, y, text, color))


def _tile(c, x, y, w, h, n, color):
    c.card(x, y, w, h, r=L["radius_bento"])
    c.circle(x + 46, y + 50, 11, color)
    c.text(x + 34, y + h - 42, f"0{n}", F["mono_med"], 30, C["ink2"], 1, 0.04)


# ── INTRO: one headline arrives, then the whole line is a hold (camera dolly only) ──────────────────────────────
def intro(v, T, s, e, col):
    L1 = T["L01"]
    h = Headline("Tenang,\ntapi *presisi*.", y=720, style="headline_lg")
    t_h = arrive(L1.start + 0.25)

    def draw(c, t):
        kicker(c, t, s + 0.3, e - OUT, "APPLE LAB · STYLE §6f", col)
        h.draw(c, t, t_h, e - OUT, reveal="rise", exit="quiet")
        _tag(c, t, follow(T.word("L01", "presisi"), 2), e - OUT, "satu leader · lalu diam", col, y=1080)
    v.add(s, e, draw)
    dolly(v, T.word("L01", "presisi") + 0.4, e - 0.2)
    v.sfx("pop", T.word("L01", "presisi"))


# ── 01 · LEADER: OLD (all at once, overshoot + blur) → NEW (one leader, the rest follow with half the travel) ───
def leader(v, T, s, e, col):
    L2, L3 = T["L02"], T["L03"]
    gap = 24
    w, h, y = (CW - 2 * gap) / 3, 380, 760
    boxes = [(X + i * (w + gap), y, w, h) for i in range(3)]
    head = Headline("Siapa yang\n*mimpin*?")
    t_old, t_old_out = L2.start + 0.15, L3.start - 0.45
    t_lead = arrive(T.word("L03", "mimpin"))

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "01 · SATU LEADER", col)
        head.draw(c, t, L2.start - 0.1, e - OUT, reveal="rise", exit="quiet")
        # OLD: three tiles pop together — out_back overshoot, blur, tilt. This is the slop.
        if t < t_old_out + OUT:
            p = clamp(prog(t, t_old, 0.5))
            a, b = min(1.0, p * 2.5), prog(t, t_old_out, OUT)
            for i, (bx, by, bw, bh) in enumerate(boxes):
                k = out_back(p, 2.2)
                with c.at(0, 60 * (1 - k), 0.6 + 0.4 * k, origin=(bx + bw / 2, by + bh / 2), rot=(i - 1) * 0.12 * (1 - p)):
                    with c.layer((bx - 40, by - 40, bw + 80, bh + 80), a * (1 - b), 14 * (1 - p)):
                        _tile(c, bx, by, bw, bh, i + 1, OLD)
            _tag(c, t, t_old + 0.3, t_old_out, "LAMA · semua barengan", OLD)
        # NEW: tile 1 leads (full travel), tiles 2–3 follow 0.12 s apart with half the travel.
        for i, bx in enumerate(boxes):
            ti = t_lead if i == 0 else follow(t_lead, i)
            dy = M["rise_dy"] * 2 if i == 0 else M["rise_dy"] * 2 * M["follow_amp"]
            rise(c, t, ti, e - OUT, bx, lambda c, i=i, bx=bx: _tile(c, *bx, i + 1, col), dy=dy)
        _tag(c, t, follow(t_lead, 4), e - OUT, "BARU · leader + follow", col)
    v.add(s, e, draw)
    v.sfx("pop", t_old)
    v.sfx("pop", T.word("L03", "mimpin"))
    dolly(v, follow(t_lead, 6), e - 0.2)


# ── 02 · MENDARAT: the hero shrinks from full-bleed and LANDS on the stressed word, then holds ───────────────────
def mendarat(v, T, s, e, col):
    L4, L5 = T["L04"], T["L05"]
    head = Headline("Mendarat\npas *katanya*.")
    hw, hh = 560, 700
    hx, hy = X + (CW - hw) / 2, 600
    t_word = T.word("L04", "mendarat")
    t_hero = arrive(t_word, "hero")

    def hero(c, t):
        mv, op = presence(t, t_hero, e - OUT, "hero")
        if op <= 0.002:
            return
        sc = 2.4 + (1.0 - 2.4) * mv            # full-bleed → rest, on the heavy "hero" spring (no overshoot)
        with c.at(0, 0, sc, origin=(hx + hw / 2, hy + hh / 2)):
            with c.group(op):
                c.shadow(hx, hy, hw, hh, 48, 60, 24, 0.10)
                c.fill_rrect(hx, hy, hw, hh, 48, col)
                c.text(hx + 48, hy + hh - 70, "mendarat.", F["display"], 92, C["card"], 1, -0.05)
                c.text(hx + 50, hy + 80, "HERO · iOS SPRING", F["mono_med"], 24, C["card"], 0.8, 0.12)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · ARRIVE ON THE WORD", col)
        head.draw(c, t, L4.start - 0.15, e - OUT, reveal="rise", exit="quiet")
        hero(c, t)
        _tag(c, t, follow(L5.start, 1), e - OUT, "hold ≥ 0,8 s · cuma kamera dolly", col, y=1380)
    v.add(s, e, draw)
    v.sfx("thud", t_word)
    dolly(v, L5.start, e - 0.2, y=hy + hh / 2)


# ── 03 · TEKS: lines rise as one piece (opacity first) → a title opens with a soft wipe ──────────────────────────
def teks(v, T, s, e, col):
    L6, L7 = T["L06"], T["L07"]
    head = Headline("Naik\nper *baris*.")
    title = Headline("Lembut,\nbukan *heboh*.", y=900, style="headline_lg")
    t_cap = arrive(T.word("L06", "posisi"), "snappy")
    t_wipe = arrive(T.word("L07", "wipe"))

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "03 · TYPE MOVES AS TYPE", col)
        head.draw(c, t, L6.start - 0.1, e - OUT, reveal="rise", exit="quiet")
        rise(c, t, t_cap, L7.start - 0.3, (X, 640, CW, 60),
             lambda c: c.text(X, 690, "opacity  →  posisi", F["mono_med"], 40, C["ink2"], 1, 0.02))
        title.draw(c, t, t_wipe, e - OUT, reveal="wipe", exit="quiet")
    v.add(s, e, draw)
    v.sfx("pop", T.word("L06", "posisi"))
    v.sfx("whoosh", T.word("L07", "wipe"))


# ── 04 · KONTINUITAS: old card falls back while the new comes forward → it shrinks to a pill → grows into a card ─
def kontinuitas(v, T, s, e, col):
    L8, L9 = T["L08"], T["L09"]
    head = Headline("Nggak ada layar\n*kosong*.")
    box = (X, 620, CW, 560)
    pill = (X + CW / 2 - 150, 860, 300, 84)
    t_swap = arrive(T.word("L08", "maju"), "smooth", 0.5)
    t_pill = L9.start
    t_card = arrive(T.word("L09", "card"))
    morph = Morph(box, r=L["radius_bento"], preset="silk").to(t_pill, pill, r=42).to(t_card, (X, 560, CW, 720),
                                                                                      r=L["radius_bento"])

    def old(c):
        c.card(*box, r=L["radius_bento"])
        c.text(X + 56, box[1] + 110, "LAMA", F["mono_med"], 30, OLD, 1, 0.12)
        c.text(X + 56, box[1] + box[3] - 70, "mundur.", F["display"], 96, C["ink2"], 1, -0.05)

    def content(c, b, k):
        x, y, w, h = b
        if k == 0:
            c.text(x + 56, y + 110, "BARU", F["mono_med"], 30, C["card"], 0.85, 0.12)
            c.text(x + 56, y + h - 70, "maju.", F["display"], 96, C["card"], 1, -0.05)
        elif k == 1:
            c.text(x + w / 2, y + h / 2 + 14, "pill", F["display"], 40, C["card"], 1, -0.02, align="c")
        else:
            c.text(x + 56, y + 110, "CARD", F["mono_med"], 30, C["card"], 0.85, 0.12)
            c.text(x + 56, y + h - 70, "satu bentuk.", F["display"], 96, C["card"], 1, -0.05)

    def new(c):
        morph.draw(c, t_swap, col, content)        # = the Morph's base state, so the hand-over is seamless

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "04 · CONTINUITY", col)
        head.draw(c, t, L8.start - 0.1, e - OUT, reveal="rise", exit="quiet")
        _, op = presence(t, s + 0.3, e - OUT)
        with c.group(op):
            if t < t_pill:
                depth_swap(c, t, t_swap, box, old, new)
            else:
                morph.draw(c, t, col, content)
    v.add(s, e, draw)
    v.sfx("whoosh", t_swap)
    v.sfx("pop", t_card)


# ── 05 · FOKUS: the background goes soft (depth, not glass) while the number comes forward ───────────────────────
def fokus(v, T, s, e, col):
    L10 = T["L10"]
    head = Headline("Fokus ke\n*satu* hal.")
    t_num = arrive(T.word("L10", "muncul"))
    gap = 18
    tw, th = (CW - gap) / 2, 300
    tiles = [(X + (i % 2) * (tw + gap), 600 + (i // 2) * (th + gap), tw, th) for i in range(4)]
    area = (X, 600, CW, 2 * th + gap)
    nb = (X + 90, 700, CW - 180, 420)          # the number card, in front

    def back(c):
        for i, bx in enumerate(tiles):
            _tile(c, *bx, i + 1, OLD)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "05 · RACK FOCUS", col)
        head.draw(c, t, L10.start - 0.1, e - OUT, reveal="rise", exit="quiet")
        # background hard-cuts in with the chapter (no entrance) — only the headline and the number animate
        rise(c, t, s - 1.0, e - OUT, area, lambda c: focus_pull(c, t, t_num - 0.15, None, area, back))
        rise(c, t, t_num, e - OUT, nb, lambda c: (
            c.card(*nb, r=L["radius_bento"], shadow="chat"),
            c.text(nb[0] + 60, nb[1] + 100, "FRAME RATE", F["mono_med"], 28, C["ink2"], 1, 0.12),
            c.text(nb[0] + 56, nb[1] + 330, "60", F["display"], tk.T["mega"][0], col, 1, -0.06),
            c.text(nb[0] + 330, nb[1] + 330, "fps", F["serif"], 110, C["ink"], 1, 0.0)))
    v.add(s, e, draw)
    v.sfx("pop", T.word("L10", "muncul"))
    dolly(v, follow(t_num, 8), e - 0.2, y=nb[1] + nb[3] / 2)


# ── 06 · TEMPO: slow, slow… then a HARD cut to one word (contrast is what makes it feel designed) ────────────────
def tempo(v, T, s, e, col):
    t1, t2 = T.word("L11", "pelan", 0), T.word("L11", "pelan", 1)
    t_cut = T.word("L11", "cut")

    def word(c, t, t0, y, text):
        mv, op = presence(t, arrive(t0, "hero"), None, "hero")
        if t < t_cut and op > 0.002:
            with c.group(op):
                c.text(X, y + 40 * (1 - mv), text, F["display"], tk.T["headline_lg"][0], C["ink2"], 1, -0.06)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "06 · SLOW — SLOW — SNAP", col)   # chrome stays; only the content cuts
        if t < t_cut:
            word(c, t, t1, 760, "Pelan.")
            word(c, t, t2, 920, "Pelan.")
        else:                                    # the cut: no entrance animation at all, then a long hold
            op = 1 - prog(t, e - OUT, OUT)
            c.text(X - 6, 1180, "cut.", F["display"], tk.T["giga"][0], col, op, -0.065)
    v.add(s, e, draw)
    v.sfx("thud", t_cut)
    cut(v, t_cut, zoom=1.0)


# ── OUTRO: one line, then stillness ─────────────────────────────────────────────────────────────────────────────
def outro(v, T, s, e, col):
    L12 = T["L12"]
    h = Headline("Diam itu bagian\ndari *gerakan*.", y=760)

    def draw(c, t):
        h.draw(c, t, arrive(L12.start + 0.2), None, reveal="rise")
        fade(c, t, T.word("L12", "gerakan") + 0.6, None, lambda c: c.text(
            X, 1120, "mumeyong.dev", F["mono_med"], 30, C["ink2"], 1, 0.08))
    v.add(s, e, draw)
    dolly(v, T.word("L12", "gerakan"), e)
