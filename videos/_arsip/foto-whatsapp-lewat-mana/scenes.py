"""Foto yang kamu kirim di WhatsApp, sebenernya lewat mana? — QUICK, reel look (STYLE §6e). See PLAN.md.

Metaphor: left-luggage lockers. Your phone locks the photo in a box with a brand-new key, the box waits in the
server's locker (#05), and the key never goes there — it rides inside the end-to-end chat message to your friend.
Signature: a locker door swinging on a heavy spring, swallowing / handing out the box; the key on its own green
dotted route. Motion: heavy springs · smear_words · persistent box (Rig) · reel exits. Sound: cinematic G dreamy 96
+ glass kit.
"""
import math

from engine import Video, tokens as tk
from engine.ease import clamp, prog, lerp, mix, out_back, out_cubic, in_cubic, in_out_cubic
from engine.components import (brand_intro, cover, phone, Rig, spring_at, ghost_trail, follow_button, smear, smear_p,
                               out_p, smear_words, viewfinder, iris, highlight_phrase, float_chips, reel_chip,
                               pop_card, verb_slam, end_card, reel_sfx, ink_on, loker, loker_cell, kotak, kunci,
                               centang, foto, LOKER_TERRA as TERRA)

C, F, L, M = tk.C, tk.F, tk.L, tk.M
PAPER, INK, GREEN, SEAL = C["brand_paper"], C["reel_ink"], C["reel_green"], C["brand_seal"]
MUTED = mix(INK, PAPER, 0.38)
BUBBLE = mix(GREEN, PAPER, 0.80)            # outgoing chat bubble
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05                             # long brand sting (version 2): voice starts under its wipe
LEAD = 0.3
TAIL = 2.6
OUT = M["reel_out"]
BOX = 300                                   # kotak width in rig-local px
CH = ["INTRO", "00 · DIKUNCI DI HP", "01 · DITITIP DI LOKER", "02 · JALAN LAIN", "03 · KALAU OFFLINE", "RECAP",
      "OUTRO"]
SECTIONS = ["00 — jam 21.04", "01 — dikunci di hp", "02 — dititip di loker", "03 — jalan lain", "04 — kalau offline",
            "05 — intinya", "06 — follow"]


# ── small helpers ───────────────────────────────────────────────────────
def _fit(c, text, font, size, maxw, ls=-0.045):
    w = c.measure(text, font, size, ls)[0]
    return size if w <= maxw else size * maxw / w


def say(c, t, t0, t1, a, b, y=330, size=92, color=TERRA):
    """Reel statement: a display line + a serif line in the signature color, centred, words smearing up."""
    sa = _fit(c, a, F["display"], size, CW)
    smear_words(c, t, t0, MID, y, a, F["display"], sa, INK, -0.045, "c", t_out=t1)
    if b:
        sb = _fit(c, b, F["serif"], size * tk.SERIF_SCALE, CW, 0.0)
        smear_words(c, t, t0 + 0.25, MID, y + sa * 1.08, b, F["serif"], sb, color, align="c", t_out=t1)


def heads(T, items, end):
    """[(a, b, line_id), …] → [(a, b, t_in, t_out)] handing over line to line."""
    out = []
    for i, (a, b, lid) in enumerate(items):
        t_out = T[items[i + 1][2]].start - 0.3 if i + 1 < len(items) else end
        out.append((a, b, T[lid].start - 0.1, t_out))
    return out


def draw_heads(c, t, hs, **kw):
    for a, b, t0, t1 in hs:
        if t0 - 0.05 <= t < t1 + OUT + 0.05:
            say(c, t, t0, t1, a, b, **kw)


def ent(c, t, t0, t_out, bbox, dy=80, dx=0):
    """Reel entrance (smear) + reel exit (scale-up blur) for a block drawn at rest."""
    return smear(c, smear_p(t, t0), bbox, dx=dx, dy=dy, out=out_p(t, t_out))


def door(t, t_open, t_close=None):
    """Locker door swing on the heavy spring: opens at t_open, closes at t_close."""
    o = spring_at(t, t_open, "heavy")
    return clamp(o - (spring_at(t, t_close, "heavy") if t_close is not None else 0.0))


def along(pts, f):
    """Point at fraction f (0..1, by distance) along polyline pts."""
    segs = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    left = sum(segs) * clamp(f)
    for (a, b), d in zip(zip(pts, pts[1:]), segs):
        if left <= d:
            u = left / d if d else 0
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
        left -= d
    return pts[-1]


def dotted(c, pts, p, color, gap=22, r=4.5, alpha=1.0):
    """Dotted route drawn to fraction p."""
    total = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    n = int(total / gap)
    for k in range(int(n * clamp(p)) + 1):
        x, y = along(pts, k / max(1, n))
        c.circle(x, y, r, color, alpha)


def dashed(c, pts, p, color, width=6, alpha=1.0):
    total = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    n = int(total / 34)
    for k in range(int(n * clamp(p))):
        x0, y0 = along(pts, k / n)
        x1, y1 = along(pts, (k + 0.55) / n)
        c.line(x0, y0, x1, y1, color, width, alpha)


def bubble(c, x, y, w, t, p1=1.0, p2=0.0, photo=1.0, time="21.04"):
    """Outgoing WhatsApp-style photo bubble (x, y = top-left, width w): photo, time, ticks. Returns its height."""
    ph = w * 0.62
    h = ph + 58
    c.fill_rrect(x, y, w, h, 18, BUBBLE)
    pad = 10
    if photo > 0:
        foto(c, x + pad, y + pad, w - 2 * pad, ph - pad, t, alpha=photo, r=12)
    else:
        c.fill_rrect(x + pad, y + pad, w - 2 * pad, ph - pad, 12, mix(BUBBLE, INK, 0.08))
    fs = max(17, w * 0.065)
    tw = c.text(x + w - 18 - fs * 1.6, y + h - 18, time, F["mono_med"], fs, MUTED, 1, 0.02, align="r")
    centang(c, x + w - 16 - fs * 1.45, y + h - 17, fs * 0.95, p1, p2, MUTED)
    return h


def chat_screen(t, p1=1.0, p2=0.0, photo=1.0, title="Temen"):
    def draw(c, sx, sy, sw, sh):
        c.fill_rrect(sx, sy, sw, sh, 0, mix(PAPER, GREEN, 0.06))
        hh = sw * 0.2
        c.fill_rrect(sx, sy, sw, hh, 0, PAPER)
        c.circle(sx + hh * 0.55, sy + hh * 0.58, hh * 0.26, mix(TERRA, PAPER, 0.4))
        c.text(sx + hh * 1.0, sy + hh * 0.7, title, F["ui_semi"], max(17, sw * 0.07), INK, 1, -0.01)
        bw = sw * 0.72
        bubble(c, sx + sw - bw - sw * 0.06, sy + sh * 0.34, bw, t, p1, p2, photo)
    return draw


# ── build ───────────────────────────────────────────────────────────────
def build(project):
    T = project.timing
    v = Video(duration=T["L19"].end + TAIL, bpm=96, beat_offset=0.0)
    brand_intro(v, version=2)
    v.hud = False
    v.ground = PAPER
    v.music = dict(style="cinematic", key="G", mood="dreamy")   # kubernetes garage E warm, EP 02 marimba A bright
    v.sfx_kit = "glass"
    v.cover = lambda c: cover(c, "Fotomu\nlewat *mana*?", kicker="WHATSAPP · DI BALIK LAYAR", color=TERRA,
                              tags=["loker", "key terpisah", "end-to-end"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    for i, n in enumerate(CH):
        num = i - 1 if 1 <= i <= 4 else None
        v.chapter(num, n.split(" · ")[-1], b[i], b[i + 1])
    rig = Rig(MID, 1220, s=0.8, a=0.0)                         # the box: phone → locker → friend's phone
    darks = [intro(v, T, b[0], b[1]), dikunci(v, T, b[1], b[2], rig), loker_bab(v, T, b[2], b[3], rig),
             jalan_lain(v, T, b[3], b[4], rig), offline(v, T, b[4], b[5], rig), recap(v, T, b[5], b[6])]
    outro(v, T, b[6], b[7])

    def hud(c, t):
        k = max([i for i in range(len(CH)) if b[i] <= t] or [0])
        viewfinder(c, t, SECTIONS[k], v.duration, dark=max([d(t) for d in darks if d] + [0.0]),
                   tag="tech sehari-hari")
    v.add(0, v.duration, hud, z=110)
    v.cover_t = T["L14"].frac(0.7)
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    lw, lh = min(w * 0.62, 520), min(h * 0.92, 600)
    lx, ly = x + 20, y + (h - lh) / 2
    loker(c, lx, ly, lw, lh, 0.0, doors={4: 0.85}, lit={4: 1.0},
          inside={4: lambda c, x_, y_, w_, h_: kotak(c, x_, y_ + h_ * 0.3, w_ * 0.7)})
    kunci(c, x + w - 150, y + h * 0.45, 190, -0.35)
    dotted(c, [(x + w - 150, y + h * 0.45 + 80), (x + w - 150, y + h - 30)], 1.0, GREEN)


def _iris_pair(v, s, e, cx, cy, color):
    """iris close (entrance) at s, iris open (exit) at e − 0.85. Returns the viewfinder dark function."""
    t_open = e - 0.85
    v.add(s, s + 0.7, lambda c, t: iris(c, t, s, cx, cy, color, "close"), z=100)
    v.add(t_open, e, lambda c, t: iris(c, t, t_open, cx, cy, color, "open"), z=100)
    reel_sfx(v, "iris", t_open)
    return lambda t: float((s <= t < s + 0.25) or (t_open + 0.47 <= t < e))


# ── INTRO: 21.04 → the photo leaves the phone and loops → "lewat server" ─
def intro(v, T, s, e):
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    t_kel = T.word("L02", "keliling")
    PX, PY, PW, PH = MID - 210, 660, 420, 780
    bw = (PW - 2 * PW * 0.035) * 0.72
    bx = PX + PW * 0.035 + (PW - 2 * PW * 0.035) * 0.22          # bubble geometry (same as chat_screen)
    by = PY + PW * 0.035 + (PH - 2 * PW * 0.035) * 0.34
    photo = (bx + 10, by + 10, bw - 20, bw * 0.62 - 10)
    loop = [(photo[0] + photo[2] / 2, photo[1] + photo[3] / 2), (MID + 80, 560), (X + CW - 60, 760),
            (X + CW - 80, 1260), (MID, 1500), (X + 40, 1200), (X - 260, 900)]
    t_fly, d_fly = t_kel - 0.5, 2.2
    o = e - 0.95

    def draw(c, t):
        smear_words(c, t, L1.start, MID, 560, "21.04", F["display"], 230, INK, -0.05, "c", t_out=L2.start - 0.2)
        c.text(MID, 330, "~ KIRIM KE: TEMEN", F["mono_med"], 22, MUTED,
               clamp(prog(t, L1.start, 0.4)) * (1 - out_p(t, L2.start - 0.2)), 0.18, align="c")
        say(c, t, L2.start, L3.start - 0.3, "Belum dua centang,", "udah keliling.")
        say(c, t, L3.start, o, "Lewat server.", None)
        if t >= L3.start + 0.3:
            hl = "isinya nggak kelihatan"
            sz = _fit(c, hl, F["serif"], 92 * tk.SERIF_SCALE, CW, 0.0)
            highlight_phrase(c, t, T.word("L03", "nggak") - 0.1, MID, 430, hl, "nggak kelihatan", F["serif"], sz,
                             align="c", color=mix(TERRA, PAPER, 0.55))
            smear_words(c, t, L3.start + 0.3, MID, 430, hl, F["serif"], sz, TERRA, align="c", t_out=o)
        with ent(c, t, L1.start + 0.5, o, (PX, PY, PW, PH), dy=120):
            gone = 1 - clamp(prog(t, t_fly, 0.15))
            phone(c, PX, PY, PW, PH, draw_screen=chat_screen(t, prog(t, L1.start + 1.6, 0.3), 0.0, gone),
                  dark=True, shadow=0.1)

        def flyer(c, tt):
            u = in_out_cubic(prog(tt, t_fly, d_fly))
            x, y = along(loop, u)
            k = 1 - 0.45 * u
            w, h = photo[2] * k, photo[3] * k
            foto(c, x - w / 2, y - h / 2, w, h, tt, r=12)
        if t_fly <= t < t_fly + d_fly:
            ghost_trail(c, t, flyer)
    v.add(s, e, draw, z=20)
    v.camera.key(L1.start + 1.5, zoom=1.0, dur=0.01).key(L2.start - 0.2, zoom=1.07, y=1000, dur=0.9)
    v.camera.reset(L3.start, dur=0.8)
    reel_sfx(v, "smear", L1.start)
    v.sfx("pop", L1.start + 0.5, 0.5)
    v.sfx("tick", L1.start + 1.6, 0.6)
    v.sfx("whoosh", t_fly, 0.7)
    reel_sfx(v, "highlight", T.word("L03", "nggak") - 0.1)
    return _iris_pair(v, -1.0, e, MID, 1050, TERRA)


# ── 00 · DIKUNCI DI HP: photo → a fresh key → into the box, lid shut, lock turns ─
def dikunci(v, T, s, e, rig):
    L4, L5, L6 = T["L04"], T["L05"], T["L06"]
    PX, PY, PW, PH = MID - 220, 600, 440, 820
    sx, sy, sw = PX + PW * 0.035, PY + PW * 0.035, PW - 2 * PW * 0.035
    ph = (sx + sw * 0.12, PY + 200, sw * 0.76, sw * 0.76 * 0.72)           # the photo on screen
    t_key = T.word("L05", "key") - 0.15
    t_box = L6.start - 0.1
    t_lid, t_in, t_lock, t_back = t_box + 0.75, t_box + 0.95, t_box + 1.35, t_box + 1.6
    t_lift = min(t_box + 2.1, e - 1.5)
    KEY_REST = (X + CW - 110, 760)
    RY, RS = 1220, 0.8                                                      # box on the screen (rig)
    keyhole = (MID, RY + RS * (-BOX * 0.5 + BOX * 0.5 * 0.26 + BOX * 0.5 * 0.52 * 0.42))
    o = e - 0.95
    hs = heads(T, [("Dikunci", "di HP-mu.", "L04"), ("Key baru,", "cuma buat foto ini.", "L05"),
                   ("Yang keluar:", "kotak terkunci.", "L06")], o)

    rig.to(t_box, a=1.0, dur=0.1)
    rig.to(t_lift, y=1080, s=1.0, preset="heavy")

    def key_pos(t):
        if t < t_in:
            return KEY_REST[0], KEY_REST[1], -0.35
        if t < t_back:
            u = in_out_cubic(prog(t, t_in, 0.4))
            return lerp(KEY_REST[0], keyhole[0] + 62, u), lerp(KEY_REST[1], keyhole[1], u), lerp(-0.35, math.pi, u)
        u = in_out_cubic(prog(t, t_back, 0.45))
        return lerp(keyhole[0] + 62, KEY_REST[0], u), lerp(keyhole[1], KEY_REST[1], u), lerp(math.pi, -0.35, u)

    def draw(c, t):
        draw_heads(c, t, hs)
        dim = 1 - 0.75 * prog(t, t_lift, 0.5)
        with ent(c, t, s + 0.1, o, (PX, PY, PW, PH), dy=120), c.group(dim):
            def screen(c, x, y, w, h):
                c.fill_rrect(x, y, w, h, 0, mix(PAPER, GREEN, 0.06))
                if t < t_box + 0.1:
                    foto(c, *ph, t, r=14)
                c.text(x + w / 2, y + 120, "FOTO · 21.04", F["mono_med"], 20, MUTED, 1, 0.18, align="c")
            phone(c, PX, PY, PW, PH, draw_screen=screen, dark=True, shadow=0.1)

    def key(c, t):                                                          # above the box (z 35)
        if t >= t_key:
            p = out_back(clamp(prog(t, t_key, 0.45)), 1.7)
            x, y, r = key_pos(t)
            a = 1 - out_p(t, o)
            with c.at(0, 0, max(0.01, p), origin=(x, y)), c.group(a):
                kunci(c, x, y, 130, r + math.sin(t * 1.3) * 0.04 * (t < t_in))
            if t < t_in + 0.2:
                with ent(c, t, t_key + 0.3, t_in - 0.2, (X + CW - 330, 830, 330, 56), dy=30):
                    reel_chip(c, X + CW - 330, 830, "sekali pakai", GREEN, 24)

    def box(c, t):
        if t < t_box or t >= e:
            return
        lid = 1 - in_cubic(prog(t, t_lid, 0.25))
        lock = out_back(prog(t, t_lock, 0.2), 2.0)

        def inside(c, top):
            u = in_cubic(prog(t, t_box + 0.1, 0.6))
            gx0, gy0 = ph[0] + ph[2] / 2, ph[1] + ph[3] / 2                 # photo centre, screen px → rig-local
            lx0, ly0 = (gx0 - MID) / RS, (gy0 - RY) / RS
            w, h = lerp(ph[2] / RS, BOX * 0.7, u), lerp(ph[3] / RS, BOX * 0.5, u)
            cy = lerp(ly0, top + h * 0.6, u)
            foto(c, lx0 * (1 - u) - w / 2, cy - h / 2, w, h, t, r=12)
        with rig.place(c, t), c.group(1 - out_p(t, o)):
            kotak(c, 0, 0, BOX, lid, lock, inside if t < t_lid + 0.2 else None)
    v.add(s, e, draw, z=20)
    v.add(s, e, box, z=30)
    v.add(s, e, key, z=35)
    v.camera.key(s, zoom=1.0, dur=0.01).key(t_key - 0.2, zoom=1.08, x=640, y=880, dur=0.8)
    v.camera.key(t_box, zoom=1.04, x=MID, y=1080, dur=0.8).reset(t_lift + 0.3, dur=0.8)
    reel_sfx(v, "smear", s + 0.1)
    v.sfx("pop", t_key, 0.8)
    v.sfx("pop", t_box, 0.5)
    v.sfx("thud", t_lid + 0.2, 0.6)
    v.sfx("click", t_lock, 0.9)
    v.sfx("whoosh", t_lift, 0.5)
    return _iris_pair(v, s, e, MID, 1000, TERRA)


# ── 01 · DITITIP DI LOKER: locker #05 swallows the box · holder has box, not key · data acak ─
LW = (X + 40, 560, CW - 80, 820)


def _cell_base(box, cols, rows, i, k=0.78):
    x, y, w, h = loker_cell(*box, cols, rows, i)
    return x + w / 2, y + h * k, w


def loker_bab(v, T, s, e, rig):
    L7, L8, L9 = T["L07"], T["L08"], T["L09"]
    t_fly = T.word("L07", "loker") - 0.6
    t_arrive, t_shut = t_fly + 0.95, t_fly + 1.35
    t_force, t_acak = L9.start, T.word("L09", "acak") - 0.35
    cbx, cby, cw_ = _cell_base(LW, 3, 3, 4)
    bs = cw_ * 0.72 / BOX
    o = e - 0.95
    hs = heads(T, [("Dititip di", "loker.", "L07"), ("Pegang kotak,", "bukan key-nya.", "L08"),
                   ("Dibuka paksa?", "cuma data acak.", "L09")], o)
    rig.to(s - 0.02, x=1320, y=900, s=bs, dur=0.01)
    rig.to(t_fly, x=cbx, y=cby, s=bs, preset="heavy", dur=1.0)
    chips = [("kotak: ada", TERRA, X, 1420, -1), ("key: nggak ada", INK, X + CW, 1420, 1)]
    card = (MID - 290, 760, 580, 420)

    def draw(c, t):
        draw_heads(c, t, hs)
        doors = {4: max(door(t, t_fly - 0.3, t_shut), door(t, t_force, o - 0.6))}
        lit = {4: clamp(prog(t, t_shut, 0.4))}
        inside = {4: lambda c, x_, y_, w_, h_: kotak(c, x_, y_ + h_ * 0.28, w_ * 0.72)} if t >= t_arrive else {}
        with ent(c, t, s + 0.15, o, LW, dy=140):
            loker(c, *LW, t, doors=doors, lit=lit, inside=inside, label="SERVER WHATSAPP · LOKER")
        if s <= t < t_arrive:
            with rig.place(c, t):
                kotak(c, 0, 0, BOX)
        float_chips(c, t, L8.start + 0.3, chips, t_out=L9.start)
        if t >= t_acak:
            def body(c, x, y, w, h):
                foto(c, x + 18, y + 18, w - 36, h - 36, t, scramble=1.0, seed=5)
            with c.group(1 - out_p(t, o)):
                pop_card(c, t, t_acak, *card, draw=body, label="yang kelihatan", color=TERRA)
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.0, dur=0.01).key(t_force - 0.2, zoom=1.12, x=cbx, y=cby - 60, dur=0.9)
    v.camera.reset(t_acak, dur=0.6)
    reel_sfx(v, "smear", s + 0.15)
    v.sfx("click", t_fly - 0.3, 0.7)
    v.sfx("whoosh", t_fly, 0.6)
    v.sfx("thud", t_shut + 0.1, 0.9)
    reel_sfx(v, "chips", L8.start + 0.3, n=2)
    v.sfx("click", t_force, 0.8)
    v.sfx("pop", t_acak, 0.9)
    v.sfx("thud", o - 0.6 + 0.4, 0.6)
    return _iris_pair(v, s, e, cbx, cby, GREEN)


# ── 02 · JALAN LAIN: box via the locker, key via the chat — they meet on your friend's phone ─
SP = (X, 560, 200, 360)                     # your phone
LK = (X + CW - 340, 570, 300, 320)          # locker (small)
RP = (X + CW - 240, 1100, 200, 360)         # friend's phone


def _scr(p):
    x, y, w, h = p
    b = w * 0.035
    return x + b, y + b, w - 2 * b, h - 2 * b


def jalan_lain(v, T, s, e, rig):
    L10, L11, L12, L13, L14 = T["L10"], T["L11"], T["L12"], T["L13"], T["L14"]
    t_lain = T.word("L11", "lain")
    t_c1, t_c2 = T.word("L13", "centang"), T.word("L13", "centang", nth=1)
    t_e2e = T.word("L12", "end")
    t_take, t_open, t_muncul = L14.start, T.word("L14", "buka"), T.word("L14", "muncul")
    cbx, cby, cw_ = _cell_base(LK, 3, 3, 4)
    rsx, rsy, rsw, rsh = _scr(RP)
    o = e - 0.95
    box_route = [(SP[0] + SP[2] + 10, 700), (LK[0] - 10, 700)]
    take_route = [(cbx, LK[1] + LK[3] + 10), (cbx, 1000), (rsx + rsw / 2, RP[1] - 14)]
    key_route = [(SP[0] + SP[2] / 2, SP[1] + SP[3] + 20), (SP[0] + SP[2] / 2, 1290), (RP[0] - 24, 1290)]
    node = (SP[0] + SP[2] / 2, 1110)
    hs = heads(T, [("Ini yang", "aku suka.", "L10"), ("Key-nya lewat", "jalan lain.", "L11"),
                   ("Nyelip di chat,", "end-to-end.", "L12"), ("Pesannya", "nyampe.", "L13"),
                   ("Kotak + key", "ketemu di sini.", "L14")], o)
    rig.to(s - 0.02, x=cbx, y=cby, s=cw_ * 0.7 / BOX, a=0.0, dur=0.01)
    rig.to(t_take + 0.3, a=1.0, dur=0.2)
    rig.to(t_take + 0.6, x=rsx + rsw / 2, y=rsy + rsh * 0.62, s=rsw * 0.62 / BOX, preset="heavy", dur=1.0)
    rig.to(t_muncul + 0.2, a=0.0, dur=0.4)
    f_c1 = 0.42                                   # node position along the key route (by distance)

    def key_f(t):
        if t < L12.start:
            return 0.0
        if t < t_c1:
            return f_c1 * in_out_cubic(prog(t, L12.start, t_c1 - L12.start))
        return lerp(f_c1, 1.0, in_out_cubic(prog(t, t_c1 + 0.2, max(0.3, t_c2 - t_c1 - 0.2))))

    def draw(c, t):
        if L10.start - 0.1 <= t < L11.start:                    # highlighter under "aku suka." (drawn first)
            sz = _fit(c, "aku suka.", F["serif"], 84 * tk.SERIF_SCALE, CW, 0.0)
            with c.group(1 - out_p(t, L11.start - 0.4)):
                highlight_phrase(c, t, L10.start + 0.4, MID, 330 + 84 * 1.08, "aku suka.", "aku suka", F["serif"],
                                 sz, align="c", color=mix(GREEN, PAPER, 0.55))
        draw_heads(c, t, hs, size=84)
        a = 1 - out_p(t, o)
        with c.group(a):
            with ent(c, t, s + 0.1, None, SP, dx=-200, dy=0):
                phone(c, *SP, draw_screen=lambda c, x, y, w, h: (c.fill_rrect(x, y, w, h, 0, mix(PAPER, GREEN, 0.06)),
                      foto(c, x + 16, y + 70, w - 32, (w - 32) * 0.7, t, r=10)), dark=True, shadow=0.1)
            c.text(SP[0] + SP[2] / 2, SP[1] + SP[3] + 50, "kamu", F["mono_med"], 22, MUTED,
                   clamp(prog(t, s + 0.3, 0.4)), 0.16, align="c")
            with ent(c, t, s + 0.25, None, LK, dx=200, dy=0):
                loker(c, *LK, t, doors={4: door(t, t_take - 0.2, t_take + 1.1)}, lit={4: 1.0},
                      inside={4: lambda c, x_, y_, w_, h_: kotak(c, x_, y_ + h_ * 0.28, w_ * 0.7)}
                      if t < t_take + 0.3 else {}, label="SERVER · LOKER")
            dashed(c, box_route, prog(t, s + 0.5, 0.6), TERRA)
            c.text(MID - 40, 680, "kotak", F["mono_med"], 22, TERRA, clamp(prog(t, s + 0.9, 0.4)), 0.16, align="c")
            with ent(c, t, s + 0.4, None, RP, dy=120):
                on = prog(t, t_muncul - 0.2, 0.4)

                def rscreen(c, x, y, w, h):
                    c.fill_rrect(x, y, w, h, 0, mix(PAPER, GREEN, 0.06))
                    if on > 0:
                        pw = (w - 32) * lerp(0.4, 1.0, out_back(on, 1.4))
                        foto(c, x + w / 2 - pw / 2, y + 70, pw, pw * 0.7, t, r=10, alpha=min(1, on * 2))
                phone(c, *RP, draw_screen=rscreen, dark=True, shadow=0.1)
            c.text(RP[0] + RP[2] / 2, RP[1] + RP[3] + 46, "temen", F["mono_med"], 22, MUTED,
                   clamp(prog(t, s + 0.6, 0.4)), 0.16, align="c")
            # the key route + the chat node
            dotted(c, key_route, prog(t, t_lain - 0.6, 1.2), GREEN)
            if t >= t_lain - 0.2:
                c.fill_rrect(node[0] - 92, node[1] - 26, 184, 52, 26, PAPER)
                c.stroke_rrect(node[0] - 92, node[1] - 26, 184, 52, 26, GREEN, 2.5, clamp(prog(t, t_lain - 0.2, 0.3)))
                c.text(node[0], node[1] + 8, "server · chat", F["mono_med"], 20, INK,
                       clamp(prog(t, t_lain - 0.2, 0.3)), 0.06, align="c")
            # the key (and then the chat bubble carrying key + #05)
            if t >= t_lain - 0.5:
                kx, ky = along(key_route, key_f(t))
                wrap = clamp(prog(t, L12.start - 0.4, 0.4))
                pk = out_back(clamp(prog(t, t_lain - 0.5, 0.4)), 1.7)
                bw, bh = lerp(110, 200, wrap), lerp(60, 74, wrap)
                if t < t_open + 0.4:
                    with c.at(0, 0, max(0.01, pk), origin=(kx, ky)):
                        c.fill_rrect(kx - bw / 2, ky - bh / 2, bw, bh, bh / 2, mix(PAPER, GREEN, 1 - 0.85 * wrap))
                        kunci(c, kx - bw / 2 + 52, ky, 70, 0.0, PAPER if wrap > 0.5 else GREEN)
                        c.text(kx + bw / 2 - 22, ky + 9, "#05", F["mono_bold"], 24, PAPER, wrap, 0.04, align="r")
                if L12.start <= t < t_open + 0.4:
                    with ent(c, t, t_e2e - 0.1, t_open, (kx - 90, ky - 98, 180, 50), dy=20):
                        reel_chip(c, kx - 90, ky - 98, "end-to-end", GREEN, 20)
            # ticks: one at the server node, two at the friend's phone
            if t >= t_c1 - 0.1:
                cx0, cy0 = X + 240, 1060
                centang(c, cx0, cy0, 120, prog(t, t_c1, 0.3), prog(t, t_c2, 0.3), INK, width=13)
                lab = "sampai server" if t < t_c2 else "sampai HP temen"
                c.text(cx0, cy0 + 56, lab.upper(), F["mono_med"], 20, MUTED, clamp(prog(t, t_c1, 0.3)), 0.16)
            dashed(c, take_route, prog(t, t_take, 0.6), TERRA)

    def box(c, t):
        if t < t_take or t >= t_muncul + 0.7:
            return
        with rig.place(c, t):
            kotak(c, 0, 0, BOX, lid=out_cubic(prog(t, t_open, 0.35)), lock=1 - prog(t, t_open - 0.2, 0.2))
    v.add(s, e, draw, z=20)
    v.add(s, e, box, z=30)
    v.camera.key(s, zoom=1.0, dur=0.01).key(t_lain - 0.4, zoom=1.06, x=420, y=1050, dur=1.0)
    v.camera.key(t_c2 - 0.3, zoom=1.06, x=640, y=1150, dur=0.8).reset(t_muncul + 0.2, dur=0.8)
    reel_sfx(v, "smear", s + 0.1)
    reel_sfx(v, "highlight", L10.start + 0.4)
    v.sfx("pop", t_lain - 0.5, 0.7)
    v.sfx("whoosh", L12.start, 0.5)
    v.sfx("pop", t_e2e - 0.1, 0.5)
    v.sfx("tick", t_c1, 0.8)
    v.sfx("chime", t_c2, 0.8)
    v.sfx("click", t_take - 0.2, 0.7)
    v.sfx("whoosh", t_take + 0.6, 0.5)
    v.sfx("click", t_open - 0.2, 0.8)
    v.sfx("chime", t_muncul, 0.9)
    return _iris_pair(v, s, e, RP[0] + RP[2] / 2, RP[1] + RP[3] / 2, TERRA)


# ── 03 · KALAU OFFLINE: one big locker door; the box waits until the phone is online ─
BIG = (X + 180, 600, 380, 780)              # hinge far enough right that the open door stays in the column
P3 = (X + CW - 240, 780, 220, 400)


def offline(v, T, s, e, rig):
    L15, L16 = T["L15"], T["L16"]
    t_nunggu = T.word("L15", "nunggu")
    t_on = T.word("L16", "online") - 0.3
    cbx, cby, cw_ = _cell_base(BIG, 1, 1, 0, 0.62)
    sx, sy, sw, sh = _scr(P3)
    bs = cw_ * 0.62 / BOX
    o = e - 0.95
    hs = heads(T, [("Lagi offline?", "kotaknya nunggu.", "L15"), ("Online lagi,", "baru diambil.", "L16")], o)
    rig.to(s - 0.02, x=cbx, y=cby, s=bs, a=1.0, dur=0.01)
    rig.to(t_on + 0.5, x=sx + sw / 2, y=sy + sh * 0.62, s=sw * 0.62 / BOX, preset="heavy", dur=1.0)

    def draw(c, t):
        draw_heads(c, t, hs)
        on = prog(t, t_on, 0.3)
        pulse = 0.5 + 0.5 * math.sin((t - s) * 3.0)
        with ent(c, t, s + 0.1, o, BIG, dy=140):
            loker(c, *BIG, t, cols=1, rows=1, first=5, doors={0: door(t, t_on)}, lit={0: lerp(pulse * 0.6, 1.0, on)},
                  inside={0: lambda c, x_, y_, w_, h_: kotak(c, x_, y_ + h_ * 0.12, w_ * 0.62)}
                  if t < t_on + 0.45 else {})
        with ent(c, t, s + 0.3, o, P3, dx=220, dy=0):
            def scr(c, x, y, w, h):
                c.fill_rrect(x, y, w, h, 0, mix(mix(INK, PAPER, 0.25), mix(PAPER, GREEN, 0.06), on))
                if t >= t_on + 1.4:
                    pw = (w - 32) * out_back(prog(t, t_on + 1.4, 0.4), 1.4)
                    foto(c, x + w / 2 - pw / 2, y + 90, pw, pw * 0.7, t, r=10)
            phone(c, *P3, draw_screen=scr, dark=True, shadow=0.1)
            c.text(P3[0] + P3[2] / 2, P3[1] - 30, "ONLINE" if on > 0.5 else "OFFLINE", F["mono_med"], 22,
                   GREEN if on > 0.5 else MUTED, 1, 0.18, align="c")
        if t >= t_nunggu:
            a = clamp(prog(t, t_nunggu, 0.4)) * (1 - clamp(prog(t, t_on, 0.3)))
            with c.at(0, 0, 1, origin=(BIG[0] + 30, 1450), rot=-0.05):
                c.text(BIG[0] + 30, 1450, "masih terkunci", F["serif"], 52 * tk.SERIF_SCALE, TERRA, a)

    def box(c, t):
        if t_on + 0.45 <= t < t_on + 1.7:
            with rig.place(c, t), c.group(1 - prog(t, t_on + 1.3, 0.4)):
                kotak(c, 0, 0, BOX)
    v.add(s, e, draw, z=20)
    v.add(s, e, box, z=30)
    v.camera.key(s, zoom=1.08, x=cbx, y=980, dur=0.01).key(s + 0.2, zoom=1.04, x=cbx + 40, y=980, dur=2.0)
    v.camera.reset(t_on, dur=1.0)
    reel_sfx(v, "smear", s + 0.1)
    v.sfx("pop", t_nunggu, 0.5)
    v.sfx("chime", t_on, 0.7)
    v.sfx("click", t_on + 0.05, 0.8)
    v.sfx("whoosh", t_on + 0.5, 0.5)
    v.sfx("pop", t_on + 1.4, 0.8)
    return _iris_pair(v, s, e, MID, 980, INK)


# ── RECAP: verb slam → the server is the locker keeper: box yes, key no → bookend bubble ✓✓ ─
VERBS = ["KUNCI.", "TITIP.", "AMBIL."]


def recap(v, T, s, e):
    L17 = T["L17"]
    t0 = L17.start - 0.1
    each = 0.43
    t_end = t0 + each * len(VERBS)
    o = e - 0.45
    ca, cb = (X, 760, 404, 400), (X + CW - 404, 760, 404, 400)

    def slam(c, t):
        verb_slam(c, t, t0, VERBS, colors=[TERRA, INK, GREEN], each=each, tile=False)
    v.add(t0, t_end, slam, z=100)

    def draw(c, t):
        if t < t_end - 0.05:
            return
        say(c, t, t_end, o, "Server =", "penjaga loker.")

        def box_card(c, x, y, w, h):
            kotak(c, x + w / 2, y + h * 0.62, w * 0.62)

        def key_card(c, x, y, w, h):
            kunci(c, x + w / 2, y + h * 0.45, w * 0.55, -0.2, mix(GREEN, PAPER, 0.35))
            sp = in_out_cubic(prog(t, t_end + 0.9, 0.35))
            if sp > 0:
                c.line(x + w * 0.2, y + h * 0.66, x + w * 0.2 + w * 0.6 * sp, y + h * 0.24, SEAL, 8)
        with c.group(1 - out_p(t, o)):
            pop_card(c, t, t_end + 0.2, *ca, draw=box_card, label="kotak · dipegang", color=TERRA)
            pop_card(c, t, t_end + 0.4, *cb, draw=key_card, label="key · nggak", color=GREEN)
        with ent(c, t, t_end + 0.8, o, (MID - 200, 1230, 400, 306), dy=60):
            bubble(c, MID - 200, 1230, 400, t, 1.0, 1.0)
    v.add(s, e, draw, z=20)
    v.camera.key(t_end, zoom=1.03, dur=0.01).key(t_end + 0.1, zoom=1.0, dur=2.5)
    reel_sfx(v, "verbs", t0, n=len(VERBS), each=each)
    reel_sfx(v, "smear", t_end)
    reel_sfx(v, "cards", t_end + 0.2, n=2, each=0.2)
    v.sfx("click", t_end + 0.9, 0.6)
    v.sfx("chime", t_end + 0.8, 0.5)

    def dark(t):
        if not (t0 <= t < t_end):
            return 0.0
        return float(ink_on([TERRA, INK, GREEN][min(2, int((t - t0) / each))]) == PAPER)
    return dark


# ── OUTRO: end card + follow ────────────────────────────────────────────
def outro(v, T, s, e):
    t0 = T["L18"].start - 0.2
    t_click = T.word("L19", "Follow") + 0.3

    def draw(c, t):
        end_card(c, t, t0, cy=760, r=140, name="mumeyong.dev", sub="app apa lagi yang mau dibongkar?",
                 cta="tulis di komentar")
        if t >= T["L19"].start - 0.4:
            with ent(c, t, T["L19"].start - 0.4, None, (MID - 150, 1300, 300, 72), dy=40):
                follow_button(c, MID, 1300, t, t_click)
    v.add(s, e, draw, z=20)
    reel_sfx(v, "end", t0)
    v.sfx("pop", T["L19"].start - 0.4, 0.5)
    v.sfx("click", t_click, 0.8)
