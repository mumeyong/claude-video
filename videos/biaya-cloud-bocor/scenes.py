"""5 tanda biaya cloud kamu bocor (QUICK, pillar B). See IDENTITY.md / TREATMENT.md.

Metaphor: a prepaid token meter + one power strip; each leak is an appliance quietly drawing power.
Signature move: the meter's pulse LED blinks fast and slows down with every fixed leak; the charger plug is pulled and
drops. Color: teal. Hook: number first ($5.000/bulan — real, from the CV). Structure: countdown 5 → 1.
First video with fx.py: ghost_trail (flying plug), land/squash + contact_shadow (plug hits the floor), settle (✓ pops).
"""
from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, clamp
from engine.components import (Headline, kicker, appear, fade, Cursor, note, odometer, follow_button,
                               save_button, jadwal, cover, token_meter, stop_kontak, steker, alat, tag_center,
                               ghost_trail, land, squash, contact_shadow, settle, mumei_mark, brand_intro,
                               LISTRIK_TEAL as TEAL)

PRE_ROLL = 1.2          # brand sting first (engine shifts the voice + every T time by this) — see components/brand.py

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · TANDA 5 & 4", "01 · TANDA 3 & 2", "02 · NOMOR 1", "RECAP", "OUTRO"]
OK = C["ok"]
RED = C["rec"]

# tiles, left → right = sign 1 … 5 (the countdown sweeps right → left)
KINDS = ["lampu", "charger", "ac", "kulkas", "colokan_t"]
LABELS = ["lampu teras", "charger", "AC", "kulkas", "colokan T"]
TECH = ["VM 24 jam", "unattached disk", "instance gede", "snapshot lama", "tanpa tag"]
TITLE = {5: ("Resource tanpa tag", "colokan T beranak"), 4: ("Snapshot numpuk", "kulkas penuh basi"),
         3: ("Instance kegedean", "AC 2 PK, kamar kos"), 2: ("Disk nggak nempel", "charger tanpa HP"),
         1: ("Nyala 24 jam", "lampu teras siang bolong")}
TW, TH, TY = 144, 170, 1000
TX = [X + 40 + i * 156 for i in range(5)]
STRIP_Y = 1215
FLOOR = 1305
METER = (X + 40, 600, 260, 360)


def build(project):
    T = project.timing
    v = Video(duration=T["L18"].end + TAIL, bpm=128, beat_offset=0.0, series="5 TANDA")
    v.cover_t = T.word("L05", "siapa") + 0.6
    v.music = dict(key="C", mood="warm")             # after E bright (EP07) and G tense (EP06)
    v.cover = lambda c: cover(c, "Cloud kamu\n*bocor*?", kicker="5 TANDA · FINOPS", color=TEAL, badge="SAVE",
                              tags=["$5.000 / bulan", "hitung mundur"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    fixes = {5: T.word("L05", "siapa") + 0.3, 4: T.word("L07", "basi") + 0.2, 3: T.word("L10", "right-sizing"),
             2: T.word("L12", "nyedot"), 1: T.word("L14", "matiin")}
    slams = {5: T["L04"].start, 4: T["L06"].start, 3: T["L08"].start, 2: T["L11"].start, 1: T["L13"].start}
    brand_intro(v)                                   # opening sting: ensō + seal → into the HUD corner
    led = [(0.0, 4.0)] + [(fixes[n], hz) for n, hz in ((5, 3.0), (4, 2.2), (3, 1.6), (2, 1.1), (1, 0.5))]
    intro(v, T, 0.0, b[CH[0]], led)
    wall(v, T, b[CH[0]], b["RECAP"], led, fixes, slams)
    recap(v, T, b["RECAP"], b["OUTRO"], led)
    outro(v, T, b["OUTRO"], v.duration)
    return v


def _cover_hero(c, box):
    """Cover hero: the meter (frantic) next to the power strip with two leaking appliances."""
    x, y, w, h = box
    token_meter(c, x + 10, y + 10, 250, min(340, h - 20), 0.0, [(0, 4.0)], bar=0.95)
    for k, kind in enumerate(("charger", "colokan_t")):
        alat(c, kind, x + 300 + k * 270, y + 20, 240, 230, 0.0, label=LABELS[1 if k == 0 else 4], seed=k)
    stop_kontak(c, x + 300, y + 280, w - 300, 2)


def _calm(t, fixes):
    return sum(out_expo(prog(t, tt, 0.6)) for tt in fixes.values()) / 5


# ── INTRO: $5.000 → the frantic meter → countdown ──────────────────────
def intro(v, T, s, e, led):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    t_pot = T.word("L01", "potong")
    t_kecil = T.word("L02", "kecil")
    t_satu = T.word("L03", "satu")
    headA = Headline("Dipotong *sebulan*.")
    headB = Headline("Dari yang *kecil*.")
    headC = Headline("Hitung *mundur*.")
    mbox = (MID - 160, 620, 320, 440)
    t_dots = [L3.start + 0.2 + k * 0.16 for k in range(5)]

    cam = v.camera
    cam.key(0.0, zoom=1.08, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.key(t_pot, zoom=0.97, dur=0.12)
    cam.key(t_pot + 0.12, zoom=1.0, dur=0.4)
    cam.focus(t_kecil - 0.2, (mbox[0], mbox[1] - 20, mbox[2], 160), zoom=1.08, dur=0.6)
    cam.reset(L3.start, dur=0.6)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "FINOPS · 5 TANDA", TEAL)
        headA.draw(c, t, L1.start, L2.start - 0.15)
        headB.draw(c, t, L2.start, L3.start - 0.15)
        headC.draw(c, t, L3.start, e - OUT)

        def number(c):
            odometer(c, MID, 1050, "$5.000", prog(t, L1.start + 0.2, 1.3), 210, TEAL, align="c")
            c.text(MID, 1150, "per bulan", F["mono_med"], 32, c.theme("ink2", "d_muted"),
                   out_expo(prog(t, L1.start + 0.8, 0.4)), 0.08, align="c")
            if t >= t_pot:
                s_ = settle(t, t_pot)
                with c.at(0, 0, max(0.01, s_), origin=(MID, 1240)):
                    tag_center(c, MID, 1218, "dipotong · tagihan cloud asli", OK)
        appear(c, t, L1.start, L2.start - 0.15, (X, 820, CW, 460), number, enter="up", exit="up", blur=4)

        def meter(c):
            token_meter(c, *mbox, t, led, calm=0.0, bar=0.95)
        appear(c, t, L2.start - 0.1, e - OUT, mbox, meter, enter="right")
        if t >= t_kecil:
            note(c, X + 10, 760, "kedipnya kecepetan", prog(t, t_kecil + 0.1, 0.9), arrow_to=(mbox[0] + 260, 650),
                 size=40)

        def dots(c):
            for k in range(5):
                n = 5 - k
                if t < t_dots[k]:
                    continue
                p = settle(t, t_dots[k])
                cx = MID - 260 + k * 130
                with c.at(0, 0, max(0.01, p), origin=(cx, 1180)):
                    hi = n == 1
                    c.circle(cx, 1180, 46, TEAL if hi else c.theme("card", "d_card"))
                    c.stroke_rrect(cx - 46, 1134, 92, 92, 46, TEAL, 3)
                    c.text(cx, 1200, str(n), F["display"], 54, (1, 1, 1, 1) if hi else TEAL, 1, -0.03, align="c")
            if t >= t_satu:
                note(c, MID + 300, 1300, "paling sering", prog(t, t_satu, 0.9), arrow_to=(MID + 270, 1236),
                     align="r", size=38)
        fade(c, t, L3.start, e - OUT, dots)
    v.add(s, e + 0.4, draw)
    for k in range(4):
        v.sfx("tick", L1.start + 0.3 + k * 0.22, 0.4)
    v.sfx("thud", t_pot, 0.8)
    v.sfx("whoosh", L2.start - 0.1, 0.5)
    for tt in t_dots:
        v.sfx("pop", tt, 0.35)


# ── 00–02: the wall — countdown 5 → 1, each leak fixed, the LED slows ──
def wall(v, T, s, e, led, fixes, slams):
    b1 = T.chapter_span(CH[1])[0] - LEAD
    b2 = T.chapter_span(CH[2])[0] - LEAD
    ch0 = v.chapter(0, "TANDA 5 & 4", s, b1)
    ch1 = v.chapter(1, "TANDA 3 & 2", b1, b2)
    ch2 = v.chapter(2, "NOMOR 1", b2, e)
    heads = [("#5 · Tanpa *tag*.", "L04", "L05"), ("Punya *siapa*?", "L05", "L06"),
             ("#4 · Snapshot *numpuk*.", "L06", "L07"), ("Dibayar *tiap bulan*.", "L07", "L08"),
             ("#3 · Instance *kegedean*.", "L08", "L09"), ("CPU kepakai *sedikit*.", "L09", "L10"),
             ("Obatnya: *right-sizing*.", "L10", "L11"), ("#2 · Disk *lepas*.", "L11", "L12"),
             ("Tetap *nyedot*.", "L12", "L13"), ("#1 · Nyala *24 jam*.", "L13", "L14"),
             ("Matiin pakai *schedule*.", "L14", None)]
    heads = [(Headline(txt), T[a].start, (T[b].start - 0.15) if b else e - OUT) for txt, a, b in heads]
    box = (X, 560, CW, 780)
    t_pull = fixes[2] - 0.75
    t_land = t_pull + 0.7
    plug_land = (TX[1] + TW / 2 + 130, FLOOR)

    cam = v.camera
    for n in (5, 4, 3, 2):
        i = n - 1
        cam.key(slams[n], zoom=0.98, dur=0.1)
        cam.focus(slams[n] + 0.12, (TX[i] - 40, TY - 20, TW + 80, TH + 140), zoom=1.07, dur=0.6)
        cam.reset(fixes[n] + 0.4, dur=0.6)
    cam.focus(t_pull, (TX[1] - 40, TY, TW + 260, 340), zoom=1.08, dur=0.5)
    cam.reset(t_land + 0.6, dur=0.6)
    cam.key(slams[1], zoom=0.96, dur=0.12)
    cam.key(slams[1] + 0.12, zoom=1.0, dur=0.4)
    cam.key(fixes[1] + 0.3, zoom=0.96, dur=1.2)

    def plug_pos(t, sx):
        """Charger plug: in the socket → lifted → flies in an arc → on the floor."""
        if t < t_pull:
            return sx, STRIP_Y + 8, 0.0
        u = (t - t_pull) / 0.25
        if u <= 1:
            return sx, STRIP_Y + 8 - 70 * out_cubic(u), 0.0
        f = clamp((t - t_pull - 0.25) / 0.45)
        x0, y0 = sx, STRIP_Y - 62
        x1, y1 = plug_land
        x = x0 + (x1 - x0) * f
        y = y0 + (y1 - y0) * f * f - 90 * f * (1 - f)
        return x, y, 1.6 * f

    def draw(c, t):
        n_now = 5 if t < slams[4] else 4 if t < slams[3] else 3 if t < slams[2] else 2 if t < slams[1] else 1
        ch = ch0 if t < b1 else ch1 if t < b2 else ch2
        kicker(c, t, ch.start - 0.2 if ch is ch0 else ch.start, e - OUT, ch.kicker, ch.color)
        for h, a, b_ in heads:
            h.draw(c, t, a, b_)
        calm = _calm(t, fixes)
        muted = c.theme("muted", "d_muted")

        def room(c):
            x, y, w, h = box
            c.card(x, y, w, h, r=30)
            token_meter(c, *METER, t, led, calm=calm)
            c.line(x + 30, FLOOR + 6, x + w - 30, FLOOR + 6, c.theme("faint", "d_line"), 3)
            # giant countdown numeral + titles (top-right)
            ts = slams[n_now]
            p = prog(t, ts, 0.3)
            nx, ny = X + 420, 900
            with c.at(0, 0, 1 + 0.35 * (1 - out_expo(p)), origin=(nx, ny - 100)):
                c.text(nx, ny, str(n_now), F["display"], 300 if n_now > 1 else 330, TEAL, clamp(p * 3), -0.06,
                       align="c")
            ta = out_expo(prog(t, ts + 0.15, 0.4))
            sched = n_now == 1 and t >= T["L14"].start - 0.1
            if not sched:
                title, meta = TITLE[n_now]
                c.text(X + 540, 760, title, F["display_semi"], 40, c.theme("ink", "d_ink"), ta, -0.03,
                       width=CW - 580, line_h=1.0)
                c.text(X + 540, 880, meta, F["serif"], 36, muted, ta, width=CW - 580)
            else:
                rows = [dict(label="server", blocks=[(0.34, 0.72)], p=prog(t, T["L14"].start, 1.0))]
                jadwal(c, X + 330, 640, CW - 370, rows, t, title="schedule", color=TEAL,
                       playhead=(t * 0.18) % 1.0, row_h=62)
                c.text(X + 460, 900, "jam kerja aja", F["serif"], 34, muted, out_expo(prog(t, fixes[1], 0.5)))
            # tiles
            sockets = stop_kontak(c, X + 40, STRIP_Y, 5 * 156 - 12, 5)
            for i in range(5):
                n = i + 1
                fx = clamp((t - fixes[n]) / 0.5) if t >= fixes[n] else 0.0
                hi = out_expo(prog(t, slams[n], 0.3)) * (1 - prog(t, fixes[n] + 0.8, 0.4))
                alat(c, KINDS[i], TX[i], TY, TW, TH, t, fixed=fx, hi=hi, label=LABELS[i],
                     sub=TECH[i] if t >= slams[n] else "", seed=i)
                sx, sy = sockets[i]
                cable = (TX[i] + TW / 2, TY + TH)
                if n != 2:
                    steker(c, sx, STRIP_Y + 8, 34, cable_to=cable, sag=20)
            # the charger plug: pulled, flies (ghost trail), lands (squash + contact shadow)
            sx2 = sockets[1][0]
            px, py, _ = plug_pos(t, sx2)
            contact_shadow(c, px, FLOOR, 60, lift=max(0.0, FLOOR - py), alpha=1.0 if t >= t_pull + 0.25 else 0.0)
            with squash(c, px, FLOOR, land(t, t_land)):
                if t_pull + 0.25 <= t < t_land:
                    ghost_trail(c, t, lambda c, tt: steker(c, *plug_pos(tt, sx2)[:2], 34, rot=plug_pos(tt, sx2)[2]))
                    steker(c, px, py, 34, rot=plug_pos(t, sx2)[2], cable_to=(TX[1] + TW / 2, TY + TH), sag=10)
                else:
                    rot = 1.6 if t >= t_land else 0.0
                    steker(c, px, py if t < t_land else FLOOR - 6, 34, rot=rot,
                           cable_to=(TX[1] + TW / 2, TY + TH), sag=10 if t < t_pull else 0)
            # leak counter: how many fixed
            nf = sum(1 for tt in fixes.values() if t >= tt)
            c.text(METER[0], METER[1] + METER[3] + 40, f"beres: {nf} / 5", F["mono_bold"], 20,
                   TEAL if nf else muted, 1, 0.1)
        appear(c, t, s - 0.1, e - OUT, box, room, enter="up")
    v.add(s, e, draw)
    v.sfx("whoosh", s - 0.1, 0.6)
    for n in (5, 4, 3, 2, 1):
        v.sfx("thud", slams[n], 0.6 if n > 1 else 0.9)
        v.sfx("pop", fixes[n], 0.45)
        v.sfx("chime", fixes[n] + 0.15, 0.5)
    v.sfx("tick", T.word("L09", "sedikit"), 0.4)
    v.sfx("whoosh", t_pull + 0.25, 0.45)
    v.sfx("thud", t_land, 0.5)
    for k in range(3):
        v.sfx("tick", T["L14"].start + 0.3 + k * 0.3, 0.3)


# ── RECAP (dark): our meter is one of many on the rusun wall ───────────
def recap(v, T, s, e, led):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L15, L16 = T["L15"], T["L16"]
    t_biar = T.word("L15", "dibiarin")
    t_beda = T.word("L16", "beda")
    head1 = Headline("Yang kecil, *dibiarin*.", style="headline_dark")
    head2 = Headline("Bulan depan *beda*.", style="headline_dark")
    MW, MH, G = 170, 230, 22
    x0, y0 = MID - (4 * MW + 3 * G) / 2, 620
    ours = 5                                          # row 1, col 1
    ox, oy = x0 + (ours % 4) * (MW + G), y0 + (ours // 4) * (MH + G)

    cam = v.camera
    cam.key(s, zoom=1.25, x=ox + MW / 2, y=oy + MH / 2, dur=0.01)
    cam.key(L15.start + 0.6, zoom=1.0, dur=1.8)

    def draw(c, t):
        head1.draw(c, t, L15.start, L16.start - 0.15)
        head2.draw(c, t, L16.start, e - OUT)

        def panel(c):
            for k in range(12):
                mx, my = x0 + (k % 4) * (MW + G), y0 + (k // 4) * (MH + G)
                if k == ours:
                    bar = 0.15 - 0.08 * out_expo(prog(t, t_beda, 0.8))
                    token_meter(c, mx, my, MW, MH, t, [(0.0, 0.5)], calm=1.0, bar=bar, label="KAMU")
                    c.stroke_rrect(mx - 6, my - 6, MW + 12, MH + 12, 26, TEAL, 4)
                else:
                    token_meter(c, mx, my, MW, MH, t + k * 0.13, [(0.0, 3.0 + (k % 3) * 0.7)], bar=0.9,
                                label=f"UNIT {k + 1:02d}", alpha=0.75)
            c.text(MID, y0 + 3 * (MH + G) + 90, "dibiarin.", F["serif"], 100, TEAL, out_expo(prog(t, t_biar, 0.6)),
                   align="c")
        appear(c, t, L15.start - 0.1, e - OUT, (x0, y0, 4 * MW + 3 * G, 3 * MH + 2 * G), panel, enter="up")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("pop", t_biar, 0.5)
    v.sfx("chime", t_beda)


# ── OUTRO: save + follow (+ the full story next) ───────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L17, L18 = T["L17"], T["L18"]
    t_save = T.word("L17", "save") + 0.3
    t_click = T.word("L18", "follow") + 0.4

    def draw(c, t):
        mumei_mark(c, MID - 14, 500, 72, p_enso=out_cubic(prog(t, s + 0.1, 0.9)), p_seal=prog(t, s + 0.9, 0.25),
                   flecks=prog(t, s + 0.8, 0.2), ink=C["d_ink"], paper=C["d_bg"])
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 690, tk.BRAND_NAME, F["display"], 76, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 780, CW, 220, r=28)
            c.fill_rrect(X, 780, 14, 220, 7, TEAL)
            c.text(X + 50, 842, "CERITA LENGKAPNYA", F["mono_bold"], 20, TEAL, 1, 0.16)
            c.text(X + 50, 912, "Hemat $14.000 / bulan", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 966, "gimana caranya, langkah demi langkah", F["ui"], 32, C["d_muted"], 1, -0.01)
        appear(c, t, s + 0.3, None, (X, 780, CW, 220), teaser)
        fade(c, t, L17.start, None, lambda c: save_button(c, MID, 1060, t, t_save, color=TEAL))
        fade(c, t, L18.start, None, lambda c: follow_button(c, MID, 1170, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1310, "mumeyong.dev", F["mono_med"], 28,
                                                          C["d_muted"], 1, 0.06, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L17.start - 0.2, 860, 1450), (t_save, MID + 40, 1096), (L18.start, MID + 70, 1280),
                    (t_click, MID + 40, 1206)], clicks=[t_save, t_click], hide=t_click + 1.0))
    v.sfx("pop", s + 0.3, 0.4)
    v.sfx("click", t_save, 0.7)
    v.sfx("chime", t_save + 0.1, 0.6)
    v.sfx("chime", t_click + 0.1)
