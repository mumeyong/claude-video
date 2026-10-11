"""Kenapa AI butuh listrik segede satu kota? — QUICK, classic + Apple craft (STYLE §6f). See PLAN.md.

Metaphor: one data-center GPU ≈ two household irons that are never unplugged. The irons multiply into a grid
(tens of thousands → one building → a small town's worth of power), the heat has to be carried away (cooling eats
power too), so the building moves next to its "socket": a power plant with water nearby. Recap: one iron, on for you.
Signature: the iron's indicator lamp clicks on → heat lines rise from the soleplate (drawn once, then held).
Motion: wipe headlines · depth_swap glue (GPU → irons → grid → building) · focus_pull for the power bar · quiet exits ·
hero/smooth iOS springs · camera only dolly in holds + hard cuts on the two punches (L06, L13).
Sound: styled score marimba F warm 104 + soft SFX kit.
"""
from engine import Video, tokens as tk
from engine.ease import clamp, prog, mix, curve, lerp
from engine.components import (Headline, kicker, fade, pop_tag, note, brand_intro, standard_outro, cover, arrive,
                               follow, rise, presence, depth_swap, focus_pull, dolly, cut, heads, draw_heads, gpu_card,
                               data_center, steker, rumah, setrika, uap_panas, pembangkit, SETRIKA_CORAL as CORAL)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                             # long brand sting (version 2): voice starts under its wipe
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 2.6
CH = ["INTRO", "00 · NYALA BARENGAN", "01 · JADI PANAS", "02 · PINDAH KE COLOKAN", "RECAP", "OUTRO"]
APPLE_OUT = curve("apple_out")

# ── hero geometry ───────────────────────────────────────────────────────
GPU_BOX = (MID - 310, 760, 620, 330)
PAIR = [(352, 1120), (720, 1120)]          # two irons (cx, base_y), width PAIR_S
PAIR_S = 320
HERO_BOX = (X, 640, CW, 640)
GRID_S, GRID_COLS, GRID_ROWS = 96, 6, 4
GRID = [(X + 40 + (CW - 100) / GRID_COLS * (i + 0.5), 830 + r * 150) for r in range(GRID_ROWS) for i in range(GRID_COLS)]
DC_BOX = (MID - 230, 720, 460, 520)


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words oddly)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


def _lamp(t, t0):
    return clamp(prog(t, t0, 0.12))


def _steam(t, t0, dur=1.0):
    return APPLE_OUT(prog(t, t0, dur))


def build(project):
    T = project.timing
    v = Video(duration=T["L17"].end + TAIL, bpm=104, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="marimba", key="F", mood="warm")    # prompt garage A bright, ai-ngarang lofi Eb warm
    v.sfx_kit = "soft"
    v.cover = lambda c: cover(c, "1 GPU =\n*2 setrika*.", kicker="AI SEHARI-HARI · LISTRIK", color=CORAL,
                              tags=["data center", "cooling", "pembangkit"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    for i, n in enumerate(CH[:4]):
        v.chapter(i if i else None, n.split(" · ")[-1], b[i], b[i + 1])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    hero_intro_00(v, T, b)
    intro(v, T, b[0], b[1])
    nyala(v, T, b[1], b[2])
    panas(v, T, b[2], b[3])
    pindah(v, T, b[3], b[4])
    recap(v, T, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L17", CORAL, save_id="L16")
    v.cover_t = _w(T, "L01", "setrika", 0.6) + 1.6
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w * 0.62, h * 1.2)
    cx, base = x + w / 2 + 20, y + h * 0.86
    top = setrika(c, cx, base, s, lamp=1.0)
    uap_panas(c, top[0], top[1], s * 0.5, h * 0.42, 1.0)


# ── the hero across INTRO + 00: GPU → two irons → a grid of irons → one building → (cut) "kota kecil." ────────
def hero_intro_00(v, T, b):
    t_gpu_w = _w(T, "L01", "GPU", 0.1)
    t_gpu = arrive(t_gpu_w, "hero")
    t_set_w = _w(T, "L01", "setrika", 0.5)
    t_pair = arrive(t_set_w, "smooth", 0.5)
    t_lamps = [t_set_w + 0.25 + 0.12 * k for k in range(2)]
    t_grid_w = _w(T, "L04", "puluhan", 0.5)
    t_grid = arrive(t_grid_w, "smooth", 0.5)
    t_wave = t_grid_w + 0.35                                         # lamps light in a wave (color only)
    t_siang = _w(T, "L05", "siang", 0.5)
    t_gedung_w = _w(T, "L06", "gedung", 0.4)
    t_dc = arrive(t_gedung_w, "smooth", 0.5)
    t_kota = _w(T, "L06", "kota", 0.85)
    kota = Headline("Satu\n*kota kecil*.", y=780, style="headline_lg")
    end = b[2]

    def gpu(c, t, sc=1.0, op=1.0):
        gx, gy, gw, gh = GPU_BOX
        with c.at(0, 0, sc, origin=(gx + gw / 2, gy + gh / 2)), c.group(op):
            gpu_card(c, gx, gy, gw, gh, 0.0, on=1.0, label="GPU · DATA CENTER", color=CORAL)

    def pair(c, t):
        for k, (cx, base) in enumerate(PAIR):
            top = setrika(c, cx, base, PAIR_S, lamp=_lamp(t, t_lamps[k]))
            uap_panas(c, top[0], top[1], PAIR_S * 0.45, 300, _steam(t, t_lamps[k] + 0.1), seed=k)

    def grid(c, t):
        for k, (cx, base) in enumerate(GRID):
            col, row = k % GRID_COLS, k // GRID_COLS
            tl = t_wave + 0.05 * (col + row)
            top = setrika(c, cx, base, GRID_S, lamp=_lamp(t, tl))
            uap_panas(c, top[0], top[1], GRID_S * 0.5, 66, _steam(t, arrive(t_siang) + 0.03 * (col + row), 0.9),
                      n=2, width=3, seed=k)

    def gedung(c, t):
        x, y, w, h = DC_BOX
        uap_panas(c, x + w / 2, y - 10, w * 0.7, 190, 1.0, n=4, seed=3)
        data_center(c, x, y, w, h, 0.0, label="DATA CENTER", roof=False)

    def draw(c, t):
        if t >= t_kota:                                              # hard cut: no entrance, then a long hold
            op = 1 - prog(t, end - OUT, OUT)
            with c.group(op):
                kota.draw(c, 1e6, 0.0)
                c.text(X, 1170, "listrik satu gedung data center AI", F["mono_med"], 28, C["ink2"], 1, 0.04)
            return
        if t < t_pair:                                               # GPU lands from full-bleed on "GPU"
            mv, op = presence(t, t_gpu, None, "hero")
            if op > 0.002:
                gpu(c, t, 2.2 + (1.0 - 2.2) * mv, op)
            return
        if t < t_grid:
            depth_swap(c, t, t_pair, HERO_BOX, lambda c: gpu(c, t), lambda c: pair(c, t))
            return
        if t < t_dc:
            depth_swap(c, t, t_grid, HERO_BOX, lambda c: pair(c, t), lambda c: grid(c, t))
            return
        depth_swap(c, t, t_dc, HERO_BOX, lambda c: grid(c, t), lambda c: gedung(c, t))
    v.add(0.0, end, draw)
    v.sfx("thud", t_gpu_w, 0.6)
    v.sfx("whoosh", t_pair, 0.5)
    for tl in t_lamps:
        v.sfx("click", tl, 0.6)
    v.sfx("whoosh", t_grid, 0.5)
    v.sfx("tick", t_wave, 0.5)
    v.sfx("whoosh", t_dc, 0.5)
    v.sfx("thud", t_kota, 0.8)
    dolly(v, T["L02"].start, b[1] - 0.1)
    cut(v, b[1])
    dolly(v, arrive(t_siang) + 1.2, t_dc - 0.05, y=HERO_BOX[1] + HERO_BOX[3] / 2)
    cut(v, t_kota)
    dolly(v, t_kota + 0.05, end - 0.1, y=900)


# ── INTRO: headlines only (the hero lives in hero_intro_00) ─────────────
def intro(v, T, s, e):
    hs = heads(T, [("Satu GPU =\n*dua setrika*.", "L01"), ("Segede\n*satu kota*?", "L02")], e - OUT)

    def draw(c, t):
        kicker(c, t, 2.2, e - OUT, "AI SEHARI-HARI", CORAL)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
    v.add(s, e, draw)


# ── 00 · NYALA BARENGAN: headlines + the "24 jam" tag (hero = hero_intro_00) ─────────────────────────────────────
def nyala(v, T, s, e):
    col = tk.CHAPTER[1][0]
    t_kota = _w(T, "L06", "kota", 0.85)
    hs = heads(T, [("Dihitung\nsama *GPU*.", "L03"), ("*Puluhan ribu*\nGPU.", "L04"), ("Nyala\n*siang malam*.", "L05"),
                   ("Satu *gedung*.", "L06")], t_kota - 0.05)
    t_tag = follow(arrive(_w(T, "L05", "siang", 0.5)) + 1.0, 1)

    def draw(c, t):
        kicker(c, t, s + 0.2, t_kota - 0.05, "01 · NYALA BARENGAN", col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        fade(c, t, t_tag, T["L06"].start - 0.2, lambda c: pop_tag(c, t, t_tag, X + 40, 1340, "24 jam · 7 hari", CORAL))
    v.add(s, e, draw)
    v.sfx("pop", t_tag, 0.4)


# ── 01 · JADI PANAS: one big iron → heat → throttle → (rack focus) the power bar grows a cooling segment ─────────
def panas(v, T, s, e):
    col = tk.CHAPTER[2][0]
    S, CX, BASE = 600, MID + 30, 1180
    t_panas = _w(T, "L07", "panas", 0.85)
    t_lamp = t_panas - 0.3
    t_note = follow(t_panas + 1.0, 1)
    t_thr = _w(T, "L08", "throttle", 0.4)
    t_card_w = _w(T, "L09", "cooling", 0.3)
    t_card = arrive(t_card_w)
    t_nambah = _w(T, "L10", "nambah", 0.8)
    t_grow = arrive(t_nambah)
    hs = heads(T, [("Ujungnya:\n*panas*.", "L07"), ("Kepanasan?\n*Throttle*.", "L08"), ("Panasnya\n*dibuang*.", "L09"),
                   ("Cooling juga\n*nyedot*.", "L10")], e - OUT)
    area = (X, 600, CW, 700)
    card = (X, 820, CW, 420)

    def iron(c, t):
        top = setrika(c, CX, BASE, S, lamp=_lamp(t, t_lamp))
        uap_panas(c, top[0], top[1], S * 0.5, 360, _steam(t, arrive(t_panas), 1.1), seed=5)

    def bar(c, t):
        x, y, w, h = card
        c.card(x, y, w, h, r=L["radius_bento"], shadow="chat")
        c.text(x + 48, y + 74, "LISTRIK YANG MASUK DATA CENTER", F["mono_med"], 22, C["ink2"], 1, 0.12)
        bx, by, bw, bh = x + 48, y + 130, w - 96, 96
        c.fill_rrect(bx, by, bw, bh, 22, C["bg"])
        g = 0.64
        c.fill_rrect(bx, by, bw * g, bh, 22, CORAL)
        c.text(bx + 30, by + 62, "GPU", F["display"], 40, C["card"], 1, -0.02)
        k = APPLE_OUT(prog(t, t_grow, 0.9))
        if k > 0:
            cw_ = bw * 0.26 * k
            c.fill_rrect(bx + bw * g + 8, by, max(1.0, cw_ - 8), bh, 22, C["ink2"], clamp(k * 2))
            c.text(bx + bw * g + 30, by + 62, "cooling", F["display"], 40, C["card"], clamp(k * 3 - 1.5), -0.02)
        else:
            c.stroke_rrect(bx + bw * g + 8, by, bw * 0.26 - 8, bh, 22, C["faint"], 3, 1, dash=[10, 8])
        tx = x + 48
        for i, lbl in enumerate(("kipas", "AC", "air di pipa")):
            tw = c.measure(lbl, F["ui"], 26)[0] + 40
            a = APPLE_OUT(prog(t, follow(t_card + 0.6, i), 0.4))
            c.fill_rrect(tx, y + 290, tw, 54, 27, C["bg"], a)
            c.text(tx + 20, y + 326, lbl, F["ui"], 26, C["ink2"], a)
            tx += tw + 14
        c.text(x + w - 48, y + 326, "tanpa angka · ilustrasi", F["mono"], 18, C["muted"], 1, 0.04, align="r")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · JADI PANAS", col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        rise(c, t, s + 0.15, e - OUT, area, lambda c: focus_pull(c, t, t_card - 0.15, None, area,
                                                                 lambda c: iron(c, t)), preset="hero")
        fade(c, t, t_note, t_card - 0.4, lambda c: note(c, X + 30, 640, "hampir semua jadi panas", 1.0,
                                                        arrow_to=(CX - 120, 760)))
        fade(c, t, t_thr, t_card - 0.4, lambda c: pop_tag(c, t, t_thr, X, 1290, "suhu lewat batas → throttle", CORAL))
        rise(c, t, t_card, e - OUT, card, lambda c: bar(c, t))
    v.add(s, e, draw)
    v.sfx("click", t_lamp, 0.6)
    v.sfx("whoosh", arrive(t_panas), 0.4)
    v.sfx("pop", t_thr, 0.4)
    v.sfx("pop", t_card_w, 0.5)
    v.sfx("tick", t_nambah, 0.6)
    dolly(v, t_note + 0.6, t_card - 0.3, y=900)
    cut(v, t_card - 0.25)
    dolly(v, t_grow + 1.0, e - 0.1, y=card[1] + card[3] / 2)


# ── 02 · PINDAH KE COLOKAN: the building leaves the town for the power plant, water draws in, then a hard cut ────
def pindah(v, T, s, e):
    col = tk.CHAPTER[3][0]
    G = 1220                                         # ground line
    PB = (629, 260, 420)                             # power plant x, w, h
    DW, DH = 170, 240
    x_from, x_to = X + 185, PB[0] - DW - 36
    t_plant_w = _w(T, "L11", "pembangkit", 0.7)
    t_move = arrive(t_plant_w, "hero")
    t_cable = follow(t_plant_w + 0.2, 2)
    t_air = arrive(_w(T, "L12", "air", 0.3))
    t_kota = _w(T, "L13", "kota", 0.3)
    t_col = _w(T, "L13", "colokannya", 0.8)
    water = mix(tk.CHAPTER[4][0], C["bg"], 0.55)
    hs = heads(T, [("Pindah ke\n*pembangkit*.", "L11"), ("Deket *air*\njuga.", "L12"), ("Bukan deket\n*kota*.", "L13")],
               t_col - 0.05)
    punch = Headline("Deket\n*colokannya*.")
    scene = (X, 760, CW, 560)

    def land(c, t):
        c.line(X, G, X + CW - 40, G, C["faint"], 4)
        dim = clamp(prog(t, t_kota, 0.4))
        for k, hx in enumerate((X + 48, X + 132)):                              # the town (two houses)
            rumah(c, hx, G, 80, 0.0, light=1.0 - dim, color=CORAL, alpha=1.0 - 0.5 * dim, seed=k)
        sock = pembangkit(c, PB[0], G, PB[1], PB[2], steam=_steam(t, s + 0.6, 1.2))
        mv = presence(t, t_move, None, "hero")[0]
        dx = lerp(x_from, x_to, mv)
        uap_panas(c, dx + DW / 2, G - DH - 8, DW * 0.6, 110, 1.0, n=3, seed=2)
        data_center(c, dx, G - DH, DW, DH, 0.0, label="DATA CENTER", roof=False)
        pc = APPLE_OUT(prog(t, t_cable, 0.6))
        if pc > 0:
            x0, y0 = dx + DW, G - DH * 0.4
            c.line(x0, y0, lerp(x0, sock[0], pc), lerp(y0, sock[1], pc), CORAL, 6)
        pw = APPLE_OUT(prog(t, t_air, 0.9))                                     # water wipes in under the ground
        if pw > 0:
            c.fill_rrect(X + 230, G + 74, (CW - 270) * pw, 64, 32, water)
            c.text(X + 260, G + 117, "AIR · COOLING", F["mono_med"], 22, C["ink2"], clamp(pw * 2 - 1), 0.12)

    def plug(c, t):
        sx, sy = MID, 1060
        steker(c, sx, sy, 240, cable_to=(sx - 160, 560), sag=120)
        c.fill_rrect(sx - 150, sy + 70, 300, 200, 40, C["card"])
        c.stroke_rrect(sx - 150, sy + 70, 300, 200, 40, C["faint"], 3)
        for hx in (sx - 43, sx + 43):
            c.circle(hx, sy + 170, 16, C["ink2"])
        c.text(sx, sy + 330, "pembangkit + air", F["mono_med"], 26, C["ink2"], 1, 0.08, align="c")

    def draw(c, t):
        if t >= t_col:                                                          # hard cut: plug + punch headline
            op = 1 - prog(t, e - OUT, OUT)
            with c.group(op):
                punch.draw(c, 1e6, 0.0)
                plug(c, t)
            return
        kicker(c, t, s + 0.2, t_col - 0.05, "03 · PINDAH KE COLOKAN", col)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        rise(c, t, s + 0.15, None, scene, lambda c: land(c, t), preset="hero")
    v.add(s, e, draw)
    v.sfx("whoosh", t_move, 0.5)
    cut(v, s)
    v.sfx("click", t_cable + 0.5, 0.5)
    v.sfx("pop", t_air, 0.4)
    v.sfx("thud", t_col, 0.8)
    dolly(v, t_cable + 1.0, t_air - 0.05, y=1000)
    cut(v, t_col)
    dolly(v, t_col + 0.05, e - 0.1, y=1000)


# ── RECAP (dark): one iron, its lamp clicks on "buat kamu", then the opinion ─────────────────────────────────────
def recap(v, T, s, e):
    S, CX, BASE = 460, MID + 30, 1250
    t_kamu = _w(T, "L14", "kamu", 0.8)
    t_lamp = t_kamu - 0.1
    hs = heads(T, [("Satu setrika\n*buat kamu*.", "L14"), ("Jawabannya\n*nggak gratis*.", "L15")], e - OUT,
               style="headline_dark")
    area = (X, 760, CW, 560)

    def iron(c, t):
        top = setrika(c, CX, BASE, S, lamp=_lamp(t, t_lamp))
        uap_panas(c, top[0], top[1], S * 0.5, 280, _steam(t, t_lamp + 0.1), seed=9)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", CORAL)
        draw_heads(c, t, hs, reveal="wipe", exit="quiet")
        rise(c, t, s + 0.2, e - OUT, area, lambda c: iron(c, t), preset="hero")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    v.sfx("click", t_lamp, 0.7)
    dolly(v, follow(t_lamp + 1.1, 1), e - 0.1, y=1000)
