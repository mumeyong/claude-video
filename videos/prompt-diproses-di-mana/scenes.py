"""Kamu ngetik prompt — sebenernya diproses di mana? — QUICK, reel look (STYLE §6e). See PLAN.md.

Metaphor: sending a prompt = sending a request slip to a radio studio across the sea. The slip leaves the phone,
rides WiFi → tower → the submarine cable to the data center (the studio, ON AIR lamp on its roof), waits on the
announcer's note spike (the queue), the announcer is the GPU, and when it's your turn the ON AIR lamp lights and the
answer is broadcast back token by token (streaming). Signature: lamp on → waves leave the mic → a token lands.
Motion: reel moves (smear statements, float_chips, iris, one pixel_wipe, formula, end_card) + sheen/swap on the
phone screen · snappy pops · reel exits. Sound: garage A bright 128 + mech kit.
"""
import math

from engine import Video, tokens as tk
from engine.ease import clamp, prog, lerp, mix, out_back, out_cubic, in_out_cubic
from engine.components import (brand_intro, cover, follow_button, smear, smear_p, out_p, smear_words, viewfinder,
                               iris, pixel_wipe, highlight_phrase, float_chips, pop_card, formula, end_card, reel_sfx,
                               ink_on, phone, wifi_icon, gpu_card, token_line, note, pop_tag, ghost_trail, sheen, swap,
                               press, on_air, mic_studio, slip, paku_nota, airwaves, data_center,
                               RADIO_ORANGE as ORANGE, REEL_WORLDS as WORLDS)

C, F, L, M = tk.C, tk.F, tk.L, tk.M
PAPER, INK, GREEN, SEAL = C["brand_paper"], C["reel_ink"], C["reel_green"], C["brand_seal"]
MUTED = mix(INK, PAPER, 0.38)
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                             # long brand sting (version 2): voice starts under its wipe
LEAD = 0.3
TAIL = 2.4
OUT = M["reel_out"]
CH = ["INTRO", "00 · BERANGKAT", "01 · ANTRE", "02 · SIARAN LANGSUNG", "RECAP", "OUTRO"]
SECTIONS = ["00 — enter", "01 — berangkat", "02 — antre", "03 — siaran", "04 — pulang-pergi", "05 — follow"]
PROMPT = "kenapa langit itu biru?"
ANSWER = ["Lang", "it", " biru", " karena", " cahaya", " matahari", " dihambur", "kan", " udara", ",", " dan",
          " biru", " paling", " banyak", " dihambur", "kan", "."]
REQS = ["resep rendang", "PR fisika", "caption IG", "email ke bos", "lirik lagu", "kode Python", "ide kado"]


# ── small helpers ───────────────────────────────────────────────────────
def _fit(c, text, font, size, maxw, ls=-0.045):
    w = c.measure(text, font, size, ls)[0]
    return size if w <= maxw else size * maxw / w


def say(c, t, t0, t1, a, b, y=330, size=92, color=ORANGE, hl=None, t_hl=None):
    """Reel statement: a display line + a serif line in the signature color, centred, words smearing up."""
    sa = _fit(c, a, F["display"], size, CW)
    smear_words(c, t, t0, MID, y, a, F["display"], sa, INK, -0.045, "c", t_out=t1)
    if b:
        sb = _fit(c, b, F["serif"], size * tk.SERIF_SCALE, CW, 0.0)
        yb = y + sa * 1.08
        if hl and t_hl is not None:
            with c.group(1 - out_p(t, t1)):
                highlight_phrase(c, t, t_hl, MID, yb, b, hl, F["serif"], sb, align="c", color=mix(GREEN, PAPER, 0.5))
        smear_words(c, t, t0 + 0.25, MID, yb, b, F["serif"], sb, color, align="c", t_out=t1)


def says(c, t, items):
    for it in items:
        a, b, t0, t1 = it[:4]
        if t0 - 0.05 <= t < t1 + OUT + 0.05:
            say(c, t, t0, t1, a, b, **(it[4] if len(it) > 4 else {}))


def ent(c, t, t0, t_out, bbox, dy=80, dx=0):
    """Reel entrance (smear) + reel exit (scale-up blur) for a block drawn at rest."""
    return smear(c, smear_p(t, t0), bbox, dx=dx, dy=dy, out=out_p(t, t_out))


def chat_screen(prompt_n=1.0, sent=0.0, busy=0.0, answer=None):
    """Phone screen of a chat app: prompt typed in the input (prompt_n 0..1), sent bubble (sent 0..1), an optional
    'server sibuk' toast (busy 0..1) and an answer drawn by answer(c, x, y, w)."""
    def draw(c, sx, sy, sw, sh):
        c.fill_rrect(sx, sy, sw, sh, 0, PAPER)
        c.text(sx + sw / 2, sy + 70, "AI CHAT", F["mono_med"], 19, MUTED, 1, 0.16, align="c")
        c.line(sx + 24, sy + 96, sx + sw - 24, sy + 96, mix(INK, PAPER, 0.88), 2)
        iy = sy + sh - 110                                                       # input bar
        c.fill_rrect(sx + 20, iy, sw - 40, 76, 38, (1, 1, 1, 1))
        c.stroke_rrect(sx + 20, iy, sw - 40, 76, 38, mix(INK, PAPER, 0.8), 2)
        shown = PROMPT[:int(len(PROMPT) * clamp(prompt_n))] if sent < 0.05 else ""
        c.text(sx + 46, iy + 48, shown or "Tanya apa aja…", F["ui_reg"], 24, INK if shown else MUTED, 1)
        c.circle(sx + sw - 58, iy + 38, 26, ORANGE if shown else mix(INK, PAPER, 0.8))
        c.line(sx + sw - 58, iy + 50, sx + sw - 58, iy + 26, PAPER, 4)
        c.line(sx + sw - 68, iy + 36, sx + sw - 58, iy + 26, PAPER, 4)
        c.line(sx + sw - 48, iy + 36, sx + sw - 58, iy + 26, PAPER, 4)
        if sent > 0:                                                             # your bubble (right)
            bw = c.measure(PROMPT, F["ui"], 24)[0] + 44
            with c.group(clamp(sent * 2)):
                c.fill_rrect(sx + sw - 20 - bw, sy + 130, bw, 60, 24, mix(ORANGE, PAPER, 0.8))
                c.text(sx + sw - 20 - bw + 22, sy + 169, PROMPT, F["ui"], 24, INK, 1)
        if answer:
            answer(c, sx + 24, sy + 250, sw - 48)
        if busy > 0:
            with c.group(clamp(busy)):
                c.fill_rrect(sx + 20, sy + 220, sw - 40, 130, 20, INK)
                c.text(sx + 44, sy + 268, "Server sedang sibuk.", F["ui_semi"], 26, PAPER, 1)
                c.text(sx + 44, sy + 310, "Coba lagi sebentar.", F["ui_reg"], 22, mix(PAPER, INK, 0.3), 1)
    return draw


# ── build ───────────────────────────────────────────────────────────────
def build(project):
    T = project.timing
    v = Video(duration=T["L16"].end + TAIL, bpm=128, beat_offset=0.0)
    brand_intro(v, version=2)
    v.hud = False
    v.ground = PAPER
    v.music = dict(style="garage", key="A", mood="bright")   # ai-ngarang lofi Eb warm, interview marimba Bb bright
    v.sfx_kit = "mech"
    v.cover = lambda c: cover(c, "Prompt-mu\n*nyebrang laut*.", kicker="AI SEHARI-HARI · DI BALIK LAYAR",
                              color=ORANGE, tags=["data center", "antre GPU", "streaming"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    for i, n in enumerate(CH):
        v.chapter(i if 1 <= i <= 3 else None, n.split(" · ")[-1], b[i], b[i + 1])
    darks = [intro(v, T, b[0], b[1]), berangkat(v, T, b[1], b[2]), antre(v, T, b[2], b[3]),
             siaran(v, T, b[3], b[4]), recap(v, T, b[4], b[5])]
    outro(v, T, b[5], b[6])

    def hud(c, t):
        k = max([i for i in range(len(CH)) if b[i] <= t] or [0])
        viewfinder(c, t, SECTIONS[k], v.duration, dark=max([d(t) for d in darks if d] + [0.0]), tag="AI sehari-hari")
    v.add(0, v.duration, hud, z=110)
    v.cover_t = T["L13"].frac(0.7)
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w / 760, h / 620)
    with c.at(x + w / 2, y + h / 2, s, origin=(0, 0)):
        on_air(c, -140, -170, 300, 1.0)
        hx, hy = mic_studio(c, 220, -40, 230, on=1.0, facing=-1)
        airwaves(c, hx, hy - 60, 0.45, 260, a0=-2.4, a1=-0.75, width=8)
        slip(c, -150, 170, 240, PROMPT, rot=-0.06)


# ── INTRO: prompt typed → enter → the slip flies off → "bukan HP kamu" → radio ─
def intro(v, T, s, e):
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    t_enter = T.word("L01", "enter")
    t_type = t_enter - 1.0
    t_fly = t_enter + 0.12
    t_lamp = T.word("L03", "radio")
    t_iris = e - 0.75
    o_phone = L3.start - 0.2
    PX, PY, PW, PH = MID - 220, 640, 440, 860
    items = [("Belum sedetik,", "udah nyebrang laut.", T.word("L01", "Belum"), L2.start - 0.3),
             ("Yang mikir", "bukan HP kamu.", L2.start, L3.start - 0.3),
             ("Kirim request", "ke radio.", L3.start, t_iris - 0.1)]

    def screen(t):
        return chat_screen(prompt_n=prog(t, t_type, 0.85), sent=out_cubic(prog(t, t_fly, 0.3)))

    def draw(c, t):
        says(c, t, items)
        if t < o_phone + OUT:                                            # phone, greyed on "bukan HP kamu"
            g = clamp(prog(t, L2.start, 0.5))
            with ent(c, t, s, o_phone, (PX, PY, PW, PH), dy=120), c.at(0, 0, press(t, t_enter) * (1 - 0.06 * g),
                                                                        origin=(MID, PY + PH)):
                with c.group(1 - 0.45 * g):
                    phone(c, PX, PY, PW, PH, draw_screen=screen(t), dark=True, shadow=0.16)
            if g > 0:
                pop_tag(c, t, L2.start + 0.4, PX + 40, PY + PH + 30, "cuma kirim & terima", INK)

        def fly(c, tt):                                                  # the request slip leaves the phone
            p = clamp(prog(tt, t_fly, 0.9))
            if 0 < p < 1:
                y = lerp(PY + 180, -160, in_out_cubic(p))
                slip(c, MID + 60 * p, y, 260, PROMPT, rot=-0.15 * p, alpha=1 - clamp(prog(tt, t_fly + 0.75, 0.15)))
        ghost_trail(c, t, fly)
        if t >= L3.start - 0.1:                                          # the studio appears: lamp + mic
            ta = L3.start - 0.1
            with ent(c, t, ta, None, (180, 820, 720, 560), dy=100):
                on_air(c, MID - 130, 900, 360, clamp(prog(t, t_lamp, 0.12)))
                hx, hy = mic_studio(c, MID + 230, 1140, 230, on=clamp(prog(t, t_lamp, 0.12)), facing=-1)
                airwaves(c, hx, hy - 60, prog(t, t_lamp + 0.1, 1.1), 260, a0=-2.4, a1=-0.75, width=8)
    v.add(s, e, draw)
    v.add(s, e, lambda c, t: iris(c, t, t_iris, MID - 130, 900, ORANGE, "open"), z=100)
    v.camera.key(t_type - 0.2, zoom=1.12, y=PY + PH - 120, dur=0.9).key(t_fly + 0.2, zoom=1.0, dur=1.1)
    v.camera.key(L3.start, zoom=1.05, y=1000, dur=1.6)
    for k in range(len(PROMPT)):
        if PROMPT[k] != " ":
            v.sfx("key", t_type + 0.85 * k / len(PROMPT), 0.35)
    v.sfx("click", t_enter, 0.8)
    v.sfx("send", t_fly, 0.7)
    reel_sfx(v, "smear", T.word("L01", "Belum"))
    v.sfx("pop", L2.start + 0.4, 0.4)
    reel_sfx(v, "smear", L3.start - 0.1)
    v.sfx("click", t_lamp, 0.7)
    v.sfx("chime", t_lamp + 0.1, 0.4)
    reel_sfx(v, "iris", t_iris)
    dk = float(ink_on(ORANGE) == PAPER)
    return lambda t: dk * float(s <= t < e and prog(t, t_iris, 0.85) > 0.55)


# ── 00 · BERANGKAT: WiFi → tower → submarine cable → data center; the model doesn't fit a phone ─
RX, RY = X, 640                                    # route scene top-left
ROUTE = [(170, 1150), (170, 1010), (330, 880), (330, 1180), (400, 1290), (660, 1290), (720, 1180), (790, 1180)]


def _route_pt(f):
    n = len(ROUTE) - 1
    f = clamp(f) * n
    i = min(n - 1, int(f))
    u = f - i
    (x0, y0), (x1, y1) = ROUTE[i], ROUTE[i + 1]
    return lerp(x0, x1, u), lerp(y0, y1, u)


def _mini_screen(c, x, y, w, h):
    c.fill_rrect(x, y, w, h, 0, PAPER)
    c.fill_rrect(x + w * 0.35, y + h * 0.18, w * 0.55, h * 0.1, h * 0.05, mix(ORANGE, PAPER, 0.6))
    c.fill_rrect(x + w * 0.1, y + h * 0.82, w * 0.8, h * 0.08, h * 0.04, mix(INK, PAPER, 0.85))


def _tower(c, cx, base_y, h, alpha=1.0):
    col = mix(INK, PAPER, 0.3)
    c.line(cx - h * 0.18, base_y, cx, base_y - h, col, 5, alpha)
    c.line(cx + h * 0.18, base_y, cx, base_y - h, col, 5, alpha)
    for k in range(1, 5):
        yy = base_y - h * k / 5
        dx = h * 0.18 * (1 - k / 5)
        c.line(cx - dx, yy, cx + dx, yy, col, 3, alpha)
    c.circle(cx, base_y - h, 9, ORANGE, alpha)


def _sea(c, t, x0, x1, y, alpha=1.0):
    c.fill_rrect(x0, y, x1 - x0, 170, 18, mix(WORLDS[3], PAPER, 0.7), alpha)
    cx_ = c.ctx
    for row in range(3):
        cx_.new_path()
        yy = y + 30 + row * 42
        for k in range(41):
            xx = x0 + 16 + (x1 - x0 - 32) * k / 40
            yw = yy + 6 * math.sin(xx * 0.05 + t * 1.6 + row)
            (cx_.move_to if k == 0 else cx_.line_to)(xx, yw)
        c.src(mix(WORLDS[3], PAPER, 0.35), alpha * 0.7)
        cx_.set_line_width(3)
        cx_.stroke()


def berangkat(v, T, s, e):
    L4, L5, L6 = T["L04"], T["L05"], T["L06"]
    t_go = L4.start + 0.3
    t_arr = T.word("L05", "data")
    o_route = L6.start - 0.25
    o = e - 0.5
    items = [("Lewat WiFi,", "lalu kabel bawah laut.", s + 0.3, L5.start - 0.3, dict(size=84)),
             ("Tujuannya:", "data center.", L5.start, L6.start - 0.3),
             ("Model AI-nya", "nggak muat di HP.", L6.start, o)]
    chips = [("WiFi", WORLDS[1], 230, 960, -1), ("BTS", WORLDS[4], 360, 820, -1),
             ("kabel bawah laut", WORLDS[3], 400, 1490, -1), ("data center", ORANGE, 920, 840, 1)]

    def route(c, t):
        a = 1.0
        sea_x0, sea_x1 = 360, 700
        _sea(c, t, sea_x0, sea_x1, 1200, a)
        cx_ = c.ctx                                                       # the cable (dashed)
        cx_.new_path()
        for k, (x, y) in enumerate(ROUTE[3:7]):
            (cx_.move_to if k == 0 else cx_.line_to)(x, y)
        c.src(INK, 0.55)
        cx_.set_dash([10, 9])
        cx_.set_line_width(4)
        cx_.stroke()
        cx_.set_dash([])
        phone(c, 120, 1150, 100, 190, draw_screen=_mini_screen, dark=True, shadow=0.1)
        wifi_icon(c, 170, 1110, 46, bars=3.0, color=WORLDS[1])
        _tower(c, 330, 1180, 300)
        lamp = clamp(prog(t, t_arr, 0.12))
        lx, ly = data_center(c, 720, 860, 200, 420, t, lamp=lamp)
        airwaves(c, lx, ly, prog(t, t_arr + 0.05, 1.0), 150, a0=-2.8, a1=-0.35, width=6)

    def draw(c, t):
        says(c, t, items)
        if t < o_route + OUT:
            with ent(c, t, s + 0.1, o_route, (RX, 820, CW, 700), dy=90):
                route(c, t)

                def mover(c, tt):
                    f = prog(tt, t_go, t_arr - t_go)
                    if 0 < f < 1:
                        x, y = _route_pt(f)
                        slip(c, x, y - 20, 90, rot=-0.1, hole=False)
                ghost_trail(c, t, mover)
            float_chips(c, t, t_go + 0.2, chips, t_out=o_route)
        if t >= L6.start - 0.1:                                          # model block vs the phone
            tb = L6.start - 0.1
            with ent(c, t, tb, o, (130, 640, 820, 760), dy=-120):
                c.fill_rrect(230, 640, 650, 640, 40, INK)
                for k in range(7):
                    for j in range(6):
                        c.circle(300 + j * 102, 720 + k * 78, 9, mix(INK, ORANGE, 0.35 + 0.5 * ((k * 6 + j) % 3 == 0)))
                c.text(270, 1240, "MODEL AI", F["mono_med"], 26, PAPER, 1, 0.16)
            tp = T.word("L06", "HP")
            if t >= tp - 0.2:
                with ent(c, t, tp - 0.2, o, (110, 1100, 160, 300), dx=-120, dy=0):
                    c.stroke_rrect(130, 1110, 120, 230, 22, ORANGE, 4, dash=[10, 8])
                    c.text(190, 1390, "HP", F["mono_med"], 24, INK, 1, 0.16, align="c")
                note(c, 300, 1400, "nggak muat", clamp(prog(t, tp + 0.3, 0.6)), arrow_to=(250, 1330), color=ORANGE)
    v.add(s, e, draw)
    v.add(s, s + 0.7, lambda c, t: iris(c, t, s, MID - 130, 900, ORANGE, "close"), z=100)
    v.camera.key(T.word("L05", "data") - 0.4, zoom=1.12, x=820, y=1060, dur=1.0)
    v.camera.key(L6.start - 0.1, zoom=1.0, dur=0.8)
    v.camera.key(L6.start + 0.8, zoom=1.04, y=1000, dur=2.6)
    reel_sfx(v, "smear", s + 0.3)
    v.sfx("whoosh", t_go, 0.4)
    reel_sfx(v, "chips", t_go + 0.2, n=len(chips))
    v.sfx("click", t_arr, 0.7)
    v.sfx("chime", t_arr + 0.05, 0.4)
    reel_sfx(v, "smear", L5.start)
    v.sfx("thud", L6.start, 0.6)
    v.sfx("pop", T.word("L06", "HP") - 0.2, 0.5)
    return lambda t: float(s <= t < s + 0.3)


# ── 01 · ANTRE: thousands of slips on the spike, the announcer is the GPU, "server sibuk" ─
SPIKE = (300, 1340, 320)                           # cx, base_y, needle height
GPU = (500, 900, 400, 250)                         # behind the mic
MIC = (790, 1095, 210)                             # clamp (facing −1) lands on the desk at y 1340


def antre(v, T, s, e):
    L7, L8, L9, L10 = T["L07"], T["L08"], T["L09"], T["L10"]
    t_chips = L7.start + 0.4
    t_gpu = T.word("L08", "GPU")
    t_busy = T.word("L10", "server")
    o = e - 0.5
    o_say = [L8.start - 0.3, L9.start - 0.3, L10.start - 0.3, o]
    items = [("Ribuan request,", "di detik yang sama.", L7.start, o_say[0], dict(size=84)),
             ("Penyiarnya:", "GPU.", L8.start, o_say[1]),
             ("GPU idle?", "nggak ada yang mau.", L9.start, o_say[2], dict(size=88)),
             ("Server sibuk", "= antrean.", L10.start, o)]
    chips = [(REQS[i], (ORANGE, WORLDS[1], WORLDS[3], WORLDS[4], WORLDS[5], WORLDS[2])[i % 6],
              (110, 920)[i % 2], 560 + (i // 2) * 74, (-1, 1)[i % 2]) for i in range(6)]
    n_slips = 9
    t_s0, t_s1 = L7.start + 0.6, L8.start + 0.6
    rots = [-0.08, 0.06, -0.03, 0.1, -0.12, 0.04, -0.06, 0.09, -0.02]

    def slips(t):
        out = []
        for i in range(n_slips):
            ti = lerp(t_s0, t_s1, i / (n_slips - 1))
            out.append(dict(text=REQS[i % len(REQS)] if i == n_slips - 1 else "", p=prog(t, ti, 0.35), rot=rots[i]))
        return out

    def draw(c, t):
        says(c, t, items)
        with ent(c, t, s + 0.1, o, (X, 760, CW, 700), dy=90):
            c.fill_rrect(X + 90, 1340, CW - 180, 26, 13, mix(INK, PAPER, 0.82))  # desk (room for the exit scale-up)
            gx, gy, gw, gh = GPU
            g_on = clamp(prog(t, t_gpu, 0.4))
            gpu_card(c, gx, gy, gw, gh, t, on=g_on, label="GPU", color=ORANGE)
            mic_studio(c, MIC[0], MIC[1], MIC[2], on=g_on, facing=-1)
            paku_nota(c, SPIKE[0], SPIKE[1], SPIKE[2], slips(t))
            pop_tag(c, t, t_gpu + 0.2, gx, gy - 70, "penyiar = GPU", ORANGE)
            with c.group(1 - clamp(prog(t, L10.start - 0.3, 0.3))):
                note(c, 470, 1250, "aku pernah bangun ini", clamp(prog(t, L9.start + 0.3, 0.7)),
                     arrow_to=(gx + 60, gy + gh + 10), color=ORANGE, size=40)
        float_chips(c, t, t_chips, chips, t_out=L8.start - 0.2)
        if t >= t_busy - 0.25:                                           # small phone pops: server sibuk
            tb = t_busy - 0.25
            pw, ph = 380, 470
            px, py = X + CW - pw - 24, 1010
            _, busy = swap(t, t_busy - 0.15)                             # glue: a sheen hides the screen swap

            def scr(c, x, y, w, h):
                phone(c, x, y, w, h, draw_screen=chat_screen(1.0, 1.0, busy=busy), dark=True, shadow=0.1)
                sheen(c, t, t_busy - 0.15, (x, y, w, h), r=w * 0.13)
            pop_card(c, t, tb, px - 14, py - 14, pw + 28, ph + 28, draw=lambda c_, x, y, w, h: scr(c_, x + 14, y + 14,
                                                                                                  w - 28, h - 28),
                     label="ilustrasi", color=ORANGE, alpha=1 - out_p(t, o))
            tw = T.word("L10", "lemot")
            if t >= tw - 0.3:
                with c.group(1 - out_p(t, o)):
                    lab = "HP kamu lemot"
                    lw = c.measure(lab, F["ui"], tk.T["tag"][0], tk.T["tag"][1])[0] + 30
                    pop_tag(c, t, tw - 0.3, X + 30, 1440, lab, SEAL)
                    p = clamp(prog(t, tw + 0.1, 0.35))
                    if p > 0:
                        c.line(X + 22, 1440 + 22, X + 22 + (lw + 16) * out_cubic(p), 1440 + 22, SEAL, 6)
    v.add(s, e, draw)
    v.camera.key(L7.start + 0.4, zoom=1.12, x=SPIKE[0] + 120, y=1150, dur=1.2)
    v.camera.key(L8.start, zoom=1.0, dur=0.8)
    v.camera.focus(L9.start + 0.2, GPU, zoom=1.08, dur=1.0)
    v.camera.key(t_busy - 0.3, zoom=0.97, dur=0.35).key(t_busy + 0.1, zoom=1.0, dur=0.6)
    reel_sfx(v, "smear", L7.start)
    reel_sfx(v, "chips", t_chips, n=len(chips))
    for i in range(n_slips):
        v.sfx("tick", lerp(t_s0, t_s1, i / (n_slips - 1)) + 0.25, 0.35)
    v.sfx("click", t_gpu, 0.7)
    v.sfx("pop", t_gpu + 0.2, 0.5)
    v.sfx("pop", t_busy - 0.25, 0.6)
    v.sfx("thud", t_busy, 0.5)
    v.sfx("pop", T.word("L10", "lemot") - 0.3, 0.4)
    return None


# ── 02 · SIARAN LANGSUNG: lamp on → every wave carries one token to the phone ─
LAMP = (300, 660, 330)
SMIC = (770, 700, 180)
SPH = (MID - 260, 960, 520, 580)                    # phone (x, y, w, h)


def _token_times(T):
    t0 = T["L12"].start + 0.2
    out, t = [], t0
    for i in range(len(ANSWER)):
        out.append(t)
        t += 0.95 if i < 3 else 0.48
    return out


def siaran(v, T, s, e):
    L11, L12, L13, L14 = T["L11"], T["L12"], T["L13"], T["L14"]
    t_on = T.word("L11", "nyala")
    tts = _token_times(T)
    t_hl = T.word("L14", "baru")
    t_wipe = e - 0.55
    o = e - 0.45
    items = [("Giliran kamu.", None, L11.start, L12.start - 0.3, dict(size=110)),
             ("Satu token,", "satu tebakan.", L12.start, L13.start - 0.3),
             ("Jadi,", "langsung dikirim.", L13.start, L14.start - 0.3),
             ("Bukan efek.", "Baru dibikin.", L14.start, o, dict(hl="Baru dibikin", t_hl=t_hl))]
    fly = 0.32

    def n_at(t):
        n = 0.0
        for k, tk_ in enumerate(tts):
            if t >= tk_ + fly:
                n = k + 1
        return n

    def draw(c, t):
        says(c, t, items)
        lamp = clamp(prog(t, t_on, 0.12))
        with ent(c, t, s + 0.1, o, (X, 520, CW, 1000), dy=90):
            on_air(c, LAMP[0], LAMP[1], LAMP[2], lamp)
            hx, hy = mic_studio(c, SMIC[0], SMIC[1], SMIC[2], on=lamp, facing=-1)
            px, py, pw, ph = SPH

            def answer(c, x, y, w):
                n = n_at(t)
                car = token_line(c, x, y + 20, ANSWER, n, w, size=30, color=ORANGE, ink=INK, font=F["ui"],
                                 pills=clamp(prog(t, L12.start + 0.4, 0.4)) * (1 - clamp(prog(t, L13.start, 0.4))),
                                 tint=(ORANGE, mix(ORANGE, GREEN, 0.5)))
                if n < len(ANSWER) and t > tts[0] - 0.4:                     # caret while it's being made
                    c.fill_rrect(car[0] + 4, car[1] - 26, 4, 32, 2, ORANGE, 1.0 if int(t * 3) % 2 == 0 else 0.3)
            phone(c, px, py, pw, ph, draw_screen=chat_screen(1.0, 1.0, answer=answer), dark=True, shadow=0.14)
            for k, tk_ in enumerate(tts):                                    # signature: wave → token lands
                if tk_ - 0.05 <= t < tk_ + 1.0:
                    airwaves(c, hx, hy + 60, prog(t, tk_, 0.9), 220, a0=1.65, a1=2.35, width=6)

                    def tok(c, tt, tk_=tk_):
                        p = clamp(prog(tt, tk_, fly))
                        if 0 < p < 1:
                            x = lerp(hx - 40, px + pw * 0.5, in_out_cubic(p))
                            y = lerp(hy + 70, py + 300, in_out_cubic(p))
                            c.circle(x, y, 9, ORANGE)
                    ghost_trail(c, t, tok)
    v.add(s, e, draw)
    v.add(t_wipe, t_wipe + 1.6, lambda c, t: pixel_wipe(c, t, t_wipe, ORANGE), z=100)
    v.camera.key(s + 0.2, zoom=1.06, y=820, dur=1.2)
    v.camera.key(L12.start, zoom=1.0, dur=1.0)
    v.camera.focus(L14.start, SPH, zoom=1.08, dur=1.4)
    v.camera.key(t_wipe, zoom=1.0, dur=0.5)
    reel_sfx(v, "smear", L11.start)
    v.sfx("click", t_on, 0.8)
    v.sfx("chime", t_on + 0.08, 0.5)
    for k, tk_ in enumerate(tts):
        v.sfx("tick", tk_ + fly, 0.3 + 0.02 * (k % 5))
    reel_sfx(v, "highlight", t_hl)
    reel_sfx(v, "wipe", t_wipe)
    dk = float(ink_on(ORANGE) == PAPER)
    return lambda t: dk * float(0.3 < prog(t, t_wipe, 0.9) < 0.85)


# ── RECAP: nyebrang laut + antre + disiarin = beberapa detik ─────────────
def recap(v, T, s, e):
    L15 = T["L15"]
    t0 = L15.start + 0.1
    o = e - 0.45
    bw, bh = 560, 190
    boxes = [(MID - bw / 2 - 70 + i * 70, 520 + i * (bh + 60), bw, bh) for i in range(3)]
    cards = [("01 · berangkat", "Kabel laut", "HP → data center"), ("02 · antre", "GPU", "nunggu giliran"),
             ("03 · siaran", "Streaming", "token demi token")]
    target = (MID, 1340)
    t_res = t0 + 2.0
    t_res = max(t_res, T.word("L15", "beberapa") - 0.1)

    def draw(c, t):
        c.text(X, 300, "SATU PROMPT · TIGA STOP", F["mono"], 20, INK,
               0.55 * clamp(prog(t, s + 0.3, 0.35)) * (1 - out_p(t, o)), 0.18)
        smear_words(c, t, s + 0.35, X, 410, "Pulang-pergi.", F["display"], 84, INK, -0.045, t_out=o)
        formula(c, t, t0, boxes, cards, target, op="+", t_out=o)
        if t >= t_res:
            sz = _fit(c, "beberapa detik.", F["serif"], 110 * tk.SERIF_SCALE, CW, 0.0)
            smear_words(c, t, t_res, MID, target[1] + 110, "beberapa detik.", F["serif"], sz, ORANGE, align="c",
                        t_out=o)
            on_air(c, MID, target[1] - 40, 170, clamp(prog(t, t_res + 0.2, 0.12)), mount=False,
                   alpha=1 - out_p(t, o))
    v.add(s, e, draw)
    v.camera.key(s, zoom=1.06, dur=0.01).key(s + 0.1, zoom=1.0, dur=1.8)
    reel_sfx(v, "formula", t0, n=3)
    reel_sfx(v, "smear", t_res)
    v.sfx("click", t_res + 0.2, 0.6)
    return None


# ── OUTRO: end card + teaser + follow ────────────────────────────────────
def outro(v, T, s, e):
    L16 = T["L16"]
    t0 = L16.start - 0.2
    t_click = T.word("L16", "Follow") + 0.3

    def draw(c, t):
        end_card(c, t, t0, cy=760, r=140, name="mumeyong.dev", sub="berikutnya: AI yang jalan di HP kamu",
                 cta="follow biar nggak ketinggalan")
        if t >= t0 + 0.3:
            with ent(c, t, t0 + 0.3, None, (MID - 150, 1300, 300, 72), dy=40):
                follow_button(c, MID, 1300, t, t_click)
    v.add(s, e, draw, z=20)
    reel_sfx(v, "end", t0)
    v.sfx("pop", t0 + 0.3, 0.5)
    v.sfx("click", t_click, 0.8)
