"""Bongkar WiFi Rumah EP 02 — WiFi connected, tapi no internet. Kok bisa? See PLAN.md.

Metaphor: a komplek — your devices are houses, the router is the guard post at the gate, the boom barrier is the
link to the ISP, the guard's address book is DNS. Signature: the striped boom lifts (or doesn't) on a heavy spring,
and the orange "tes" envelope either bumps into it or gets out and back.
Motion: heavy springs · mask headlines · lockup + sheen/swap · mask exits. Sound: marimba A bright 108 + wood kit.
"""
from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_back, in_cubic, in_out_cubic, pulse
from engine.components import (Headline, kicker, fade, pop_tag, tag_center, check_badge, brand_intro, series_bumper,
                               Rig, lockup, sheen, swap, spring_at, drifting, note, strike, tag, word_pill, appear,
                               standard_outro, cover, rumah, gang, modem, ghost_trail, wifi_icon, pos_satpam,
                               buku_alamat, KOMPLEK_ORANGE as ORANGE)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
OUTRO_TAIL = 3.0
PRE_ROLL = 2.05                            # long brand sting (version 2): voice starts under its wipe
RED, OK = C["rec"], C["ok"]
CH = ["00 · DUA JALAN", "01 · GERBANG", "02 · BUKU ALAMAT", "RECAP", "OUTRO"]

# komplek scene (00 + RECAP): houses → road → guard post + boom → "jalan raya"
GROUND = 1200
HOUSES = [(X + 80, "HP"), (X + 215, "laptop"), (X + 350, "TV")]
HS = 118
POS_X, POS_S, ARM = X + 505, 150, 200
ICON = (X + 80, 1010, 56)                  # the HP's own WiFi icon above its roof
BOOK = (X, 640, CW, 600)
ROWS_OLD = [("youtube.com", "•••.•••.•.••"), ("google.com", "•••.•••.••.•"), ("instagram.com", "•••.••.•••.•")]
NET_L = dict(POWER="g", PON="g", LOS="", INTERNET="", WLAN="g")


def build(project):
    T = project.timing
    v = Video(duration=T["L21"].end + OUTRO_TAIL, bpm=108, beat_offset=0.0, series="BONGKAR WIFI RUMAH · EP 02")
    brand_intro(v, version=2)
    v.music = dict(style="marimba", key="A", mood="bright")     # EP 01 = lofi F dreamy
    v.sfx_kit = "wood"
    v.cover = lambda c: cover(c, "Sinyal *penuh*,\ninternet nol?", kicker="BONGKAR WIFI RUMAH · EP 02", color=ORANGE,
                              badge="EP 02", tags=["router", "ISP", "DNS"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    bump0 = T["L03"].end + 0.05
    bump1 = bump0 + 1.4
    b["00 · DUA JALAN"] = bump0 + 0.45                         # chapter switch hidden under the bumper
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 2, "Connected, no internet", ORANGE,
                                                    title=("BONGKAR", "WIFI RUMAH")), z=100)
    v.sfx("whoosh", bump0)
    intro(v, T, 0.0, b["00 · DUA JALAN"])
    dua_jalan(v, T, b["00 · DUA JALAN"], b["01 · GERBANG"])
    gerbang(v, T, b["01 · GERBANG"], b["02 · BUKU ALAMAT"])
    buku(v, T, b["02 · BUKU ALAMAT"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    standard_outro(v, T, b["OUTRO"], v.duration, "L21", ORANGE,
                   teaser=dict(kicker="BONGKAR WIFI RUMAH · EP 03", title="Lemot pas hujan.",
                               sub="Mitos, atau beneran?"))
    v.cover_t = T["L01"].frac(0.9)
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w, h) * 0.42
    wifi_icon(c, x + w / 2, y + h * 0.78, s, bars=3, bang=1.0)


# ── helpers ─────────────────────────────────────────────────────────────
def _heads(T, items, end, style="headline"):
    out = []
    for i, (text, lid) in enumerate(items):
        t_out = T[items[i + 1][1]].start - 0.15 if i + 1 < len(items) else end
        out.append((Headline(text, style=style), T[lid].start, t_out))
    return out


def _draw_heads(c, t, hs):
    for h, a, b_ in hs:
        h.draw(c, t, a, b_, reveal="mask", exit="mask")


def _io(t, t_in, t_out, d_in=0.5):
    """Presence 0..1: out_expo in, in_cubic out (mask exit = fade while rising, see _lift)."""
    return out_expo(prog(t, t_in, d_in)) * (1 - in_cubic(prog(t, t_out, OUT)))


def _lift(t, t_out):
    return -18 * in_cubic(prog(t, t_out, OUT))


def _amplop(c, x, y, a=1.0, label=True):
    """The orange 'tes' envelope centred on (x, y)."""
    w, h = 56, 38
    with c.group(a):
        c.fill_rrect(x - w / 2, y - h / 2, w, h, 6, ORANGE)
        c.line(x - w / 2 + 4, y - h / 2 + 4, x, y + 3, (1, 1, 1, 1), 3)
        c.line(x + w / 2 - 4, y - h / 2 + 4, x, y + 3, (1, 1, 1, 1), 3)
        if label:
            c.text(x, y - h / 2 - 12, "tes", F["mono_bold"], 20, ORANGE, 1, 0.1, align="c")


def _komplek(c, t, rise=1.0, t_rise=0.0, p_open=0.0, wifi=0.0, bang=0.0, conf=0.0, env=None, labels=1.0):
    """The whole komplek row. rise: houses pop in staggered from t_rise. wifi 0..1 draws the dotted WiFi road from
    the HP to the post. env = (x, alpha) of the test envelope (or None)."""
    ink2 = c.theme("ink2", "d_muted")
    gang(c, X + 24, GROUND, CW - 48)                           # inset: the scene drifts
    for i, (hx, name) in enumerate(HOUSES):
        p = out_back(prog(t, t_rise + i * 0.12, 0.5)) if rise else 1.0
        if p <= 0.01:
            continue
        with c.at(0, 0, p, origin=(hx, GROUND)):
            rumah(c, hx, GROUND, HS, t, light=1.0 if i == 0 else 0.4, color=ORANGE, seed=i)
        c.text(hx, GROUND + 92, name, F["mono_med"], 24, C["accent"] if i == 0 else ink2, labels * min(1, p), 0.04,
               align="c")
    pos_satpam(c, POS_X, GROUND, POS_S, t, p_open=p_open, arm=ARM, confused=conf)
    c.text(X + CW - 40, GROUND + 92, "JALAN RAYA →", F["mono_bold"], 20, ink2, labels, 0.14, align="r")
    c.text(X + CW - 40, GROUND + 124, "ke ISP · internet", F["mono"], 20, c.theme("muted", "d_muted"), labels,
           align="r")
    if wifi > 0.01:                                            # dotted signal road: HP roof → guard window
        x0, y0, x1, y1 = ICON[0], ICON[1] + 6, POS_X - 30, GROUND - 120
        n = 18
        for k in range(int(n * wifi) + 1):
            u = k / n
            px = x0 + (x1 - x0) * u
            py = y0 + (y1 - y0) * u - 210 * 4 * u * (1 - u)
            c.circle(px, py, 6, C["accent"], min(1, (wifi * n - k) + 0.2))
    ix, iy, isz = ICON
    wifi_icon(c, ix, iy, isz, bars=3, bang=bang)
    if env is not None and env[1] > 0.01:
        _amplop(c, env[0], GROUND - 63, env[1])


# ── INTRO: full bars × zero internet → the icon only measures half the road ──
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    t_full, t_nol = T.word("L01", "penuh"), T.word("L01", "nol")
    t_half = T.word("L03", "setengah")
    hs = _heads(T, [("Dua-duanya\n*bener*.", "L02"), ("Ikonnya cuma\nukur *setengah*.", "L03")], e - OUT)
    hero = Rig(MID, 1180, s=2.4, a=1.0)                        # full-bleed icon → its place under the headline
    hero.to(L2.start, y=1000, s=1.0, preset="heavy", dur=1.1)
    hero.to(e - OUT, a=0.0, dur=OUT)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "POJOK KANAN ATAS HP-MU", ORANGE)
        _draw_heads(c, t, hs)
        bars = 3 * in_out_cubic(prog(t, t_full - 0.4, 0.9))
        with hero.place(c, t):
            wifi_icon(c, 0, 0, 200, bars=bars, bang=prog(t, t_nol, 0.45))
        lockup(c, t, L2.start + 0.2, L3.start - 0.2, MID, 1290, "Penuh", "nol.", colors=(c.theme("ink", "d_ink"), RED))
        a = _io(t, L3.start, e - OUT)
        if a > 0.01:                                           # half the road: HP → router solid, router → internet ?
            y = 1250 + _lift(t, e - OUT)
            p1 = out_expo(prog(t, L3.start + 0.1, 0.6))
            p2 = out_expo(prog(t, t_half, 0.6))
            with c.group(a):
                for x_, lab in ((X + 40, "HP"), (MID, "router"), (X + CW - 40, "internet")):
                    tag_center(c, x_, y + 40, lab, ORANGE if lab == "router" else C["accent"])
                c.line(X + 40, y, X + 40 + (MID - X - 40) * p1, y, C["accent"], 8)
                for k in range(int(10 * p2)):
                    xx = MID + 20 + k * (X + CW - 60 - MID) / 10
                    c.line(xx, y, xx + 14, y, c.theme("faint", "d_line"), 8)
                if p2 > 0.5:
                    c.text((MID + X + CW) / 2, y - 26, "?", F["display"], 64, RED, out_back(prog(t, t_half + 0.2, 0.4)),
                           align="c")
                if p1 > 0.95:
                    check_badge(c, (X + 40 + MID) / 2, y - 44, 24, out_back(prog(t, L3.start + 0.6, 0.4)))
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.04, y=1100, dur=0.01).key(L2.start, zoom=1.0, y=960, dur=1.4)
    for k in range(3):
        v.sfx("tick", t_full - 0.3 + k * 0.3, 0.6)
    v.sfx("thud", t_nol)
    v.sfx("whoosh", L2.start + 0.2, 0.7)
    v.sfx("pop", L3.start + 0.6, 0.6)
    v.sfx("pop", t_half + 0.2)


# ── 00 · DUA JALAN: houses, the guard post, the bars only reach the post ─────
def dua_jalan(v, T, s, e):
    ch = v.chapter(0, "DUA JALAN", s, e)
    L4, L5, L6, L7, L8 = (T[k] for k in ("L04", "L05", "L06", "L07", "L08"))
    t_house, t_pos, t_mulus = T.word("L04", "rumah"), T.word("L05", "pos"), T.word("L06", "mulus")
    t_go, t_bang = T.word("L07", "keluar") - 0.2, T.word("L08", "tanda")
    px = POS_X + POS_S / 2 + POS_S * 0.16                      # the boom pivot (pos_satpam geometry)
    hs = _heads(T, [("HP-mu itu\nsatu *rumah*.", "L04"), ("Router =\n*pos satpam*.", "L05"),
                    ("Penuh cuma\nsampai *pos*.", "L06"), ("HP-mu *ngetes*\ndiam-diam.", "L07"),
                    ("Nggak dibalas?\n*Tanda seru*.", "L08")], e - OUT)

    def env(t):
        if t < t_go:
            return None
        u = in_out_cubic(prog(t, t_go, 1.1))
        x = ICON[0] + (px - 34 - ICON[0]) * u
        x -= 22 * pulse(t, t_go + 1.1, 0.35)                   # bump off the boom
        return x, 1 - prog(t, T.word("L08", "balasan"), 0.5)

    def trail(c, tt):
        q = env(tt)
        if q is not None:
            _amplop(c, q[0], GROUND - 63, q[1] * 0.5, label=False)

    def scene(c, t):
        a = _io(t, s + 0.1, e - OUT)
        if a <= 0.002:
            return
        with c.group(a), c.at(0, _lift(t, e - OUT)), drifting(c, t, s, e, (MID, GROUND)):
            e_ = env(t)
            if e_ is not None:
                ghost_trail(c, t, trail)
            _komplek(c, t, rise=1.0, t_rise=t_house - 0.2, p_open=0.0, wifi=in_out_cubic(prog(t, L6.start, 1.2)),
                     bang=prog(t, t_bang, 0.45), env=e_)
            fade(c, t, t_pos, None, lambda c: pop_tag(c, t, t_pos, POS_X, 860, "router", ORANGE, align="c"), d_in=0.2)
            if t >= t_mulus:
                check_badge(c, (ICON[0] + POS_X) / 2, 900, 28, out_back(prog(t, t_mulus, 0.4)))
                note(c, X + 40, 1420, "udah, itu doang", prog(t, t_mulus + 0.5, 0.5) * (1 - prog(t, L7.start, 0.3)), size=40)
        fade(c, t, L7.start + 0.4, e - OUT, lambda c: pop_tag(c, t, L7.start + 0.4, X, 1430, "tiap beberapa detik",
                                                               C["accent"]))
    v.add(s, e, scene)

    def head(c, t):
        kicker(c, t, s + 0.2, e - OUT, "00 · DUA JALAN", ch.color)
        _draw_heads(c, t, hs)
    v.add(s, e, head, z=20)
    v.camera.key(s, zoom=1.08, y=GROUND - 150, dur=0.01).key(s + 0.1, zoom=1.0, y=960, dur=2.0)
    v.camera.focus(t_go + 0.3, (POS_X - 260, 960, 520, 300), zoom=1.12, dur=0.9)
    v.camera.reset(T.word("L08", "balasan"), dur=0.8)
    for i in range(3):
        v.sfx("pop", t_house - 0.2 + i * 0.12, 0.6)
    v.sfx("pop", t_pos)
    v.sfx("tick", L6.start + 0.4, 0.5)
    v.sfx("chime", t_mulus, 0.6)
    v.sfx("whoosh", t_go, 0.5)
    v.sfx("thud", t_go + 1.1, 0.7)
    v.sfx("pop", L7.start + 0.4, 0.5)
    v.sfx("thud", t_bang)


# ── 01 · GERBANG: the boom won't lift → modem lamp (EP 01) → the whole street ──
def gerbang(v, T, s, e):
    ch = v.chapter(1, "GERBANG", s, e)
    L9, L10, L11, L12 = T["L09"], T["L10"], T["L11"], T["L12"]
    t_try, t_down = L9.start + 0.2, T.word("L09", "turun")
    t_putus, t_isp = T.word("L10", "putus"), T.word("L10", "down")
    t_ep, t_mass, t_no = T.word("L11", "satu"), T.word("L12", "massal"), T.word("L12", "ngefek")
    hs = _heads(T, [("Palangnya\n*turun*.", "L09"), ("Putus dari *ISP*.", "L10"), ("Lampu INTERNET\n*mati*?", "L11"),
                    ("Satu komplek?\n*Massal*.", "L12")], e - OUT)
    BS, BX, BY = 290, X + 175, 1260                            # close-up guard post
    street = [X + 75 + i * 165 for i in range(5)]

    def boom(t):                                               # tries to lift, gives up, drops on "turun"
        up = 0.34 * spring_at(t, t_try, "heavy")
        return up * (1 - spring_at(t, t_down - 0.15, "snappy"))

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "01 · PENYEBAB PERTAMA", ch.color)
        _draw_heads(c, t, hs)
        a = _io(t, s + 0.15, L11.start - 0.1)
        if a > 0.002:
            with c.group(a), c.at(-60 * in_cubic(prog(t, L11.start - 0.1, OUT)), 0):
                pos_satpam(c, BX, BY, BS, t, p_open=boom(t), arm=X + CW - 40 - (BX + BS * 0.66))
                c.line(X, BY, X + CW, BY, c.theme("faint", "d_line"), 5)
                if t >= t_down:                                # red flash on the boom
                    c.text(X + CW - 60, BY - 170, "×", F["display"], 90, RED, pulse(t, t_down, 0.5) * 0.9 + 0.1,
                           align="r")
                fade(c, t, t_putus, None, lambda c: pop_tag(c, t, t_putus, X, 1360, "kabel putus", RED), d_in=0.2)
                fade(c, t, t_isp, None, lambda c: pop_tag(c, t, t_isp, X + 240, 1360, "ISP down", RED), d_in=0.2)
        m = _io(t, L11.start, L12.start - 0.1)
        if m > 0.002:
            with c.group(m), c.at(60 * (1 - out_expo(prog(t, L11.start, 0.6))), _lift(t, L12.start - 0.1)):
                modem(c, MID, 960, 700, t, NET_L, focus="INTERNET", focus_p=prog(t, L11.start + 0.4, 0.5))
                fade(c, t, t_ep, None, lambda c: pop_tag(c, t, t_ep, X, 1240, "EP 01 · lampu modem", ORANGE),
                     d_in=0.2)
        h = _io(t, L12.start, e - OUT)
        if h > 0.002:
            with c.group(h), c.at(0, _lift(t, e - OUT)):
                gang(c, X, 1180, CW)
                for i, hx in enumerate(street):
                    p = out_back(prog(t, L12.start + i * 0.08, 0.45))
                    with c.at(0, 0, max(0.01, p), origin=(hx, 1180)):
                        rumah(c, hx, 1180, HS, t, light=0.3, color=ORANGE, seed=i + 3)
                    wifi_icon(c, hx, 1020, 46, bars=3, bang=prog(t, t_mass - 0.5 + i * 0.12, 0.4), alpha=min(1, p))
                fade(c, t, L12.start + 1.4, None, lambda c: tag(c, X, 1330, "restart · restart · restart", RED))
                strike(c, t, t_no, X + 8, X + 392, 1348)
    v.add(s, e, draw, z=20)
    v.camera.focus(t_try, (BX + 60, BY - 260, 520, 300), zoom=1.1, dur=0.9)
    v.camera.reset(L10.start + 0.4, dur=0.8)
    v.camera.key(L12.start, zoom=1.04, y=1100, dur=0.01).key(L12.start + 0.1, zoom=1.0, y=960, dur=1.6)
    v.sfx("whoosh", s + 0.1, 0.6)
    v.sfx("tick", t_try + 0.2, 0.5)
    v.sfx("thud", t_down)
    v.sfx("pop", t_putus)
    v.sfx("pop", t_isp)
    v.sfx("whoosh", L11.start, 0.6)
    v.sfx("pop", t_ep, 0.6)
    for i in range(5):
        v.sfx("pop", t_mass - 0.5 + i * 0.12, 0.5)
    v.sfx("click", t_no, 0.7)


# ── 02 · BUKU ALAMAT: gate open, guard confused → the address book is DNS ─────
def buku(v, T, s, e):
    ch = v.chapter(2, "BUKU ALAMAT", s, e)
    L13, L14, L15, L16, L17 = (T[k] for k in ("L13", "L14", "L15", "L16", "L17"))
    t_open, t_conf = T.word("L13", "kebuka"), T.word("L13", "bingung")
    t_num, t_err = T.word("L14", "nomornya"), T.word("L15", "error")
    t_new = T.word("L16", "ganti")
    t_g, t_cf = T.word("L16", "Google"), T.word("L16", "Cloudflare")
    t_ok, t_rusak = T.word("L17", "Kebuka"), T.word("L17", "rusak")
    hs = _heads(T, [("Gerbang buka,\nsatpam *bingung*.", "L13"), ("Nama → *nomor*.", "L14"), ("Namanya *DNS*.", "L15"),
                    ("Ganti\n*buku alamat*.", "L16"), ("Kebuka?\nBukunya *rusak*.", "L17")], e - OUT)
    PS, PX, PY = 240, X + 150, 1220

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "02 · PENYEBAB KEDUA", ch.color)
        _draw_heads(c, t, hs)
        a = _io(t, s + 0.15, L14.start - 0.1)
        if a > 0.002:
            with c.group(a), c.at(0, _lift(t, L14.start - 0.1)):
                pos_satpam(c, PX, PY, PS, t, p_open=spring_at(t, t_open, "heavy"), arm=300, confused=prog(t, t_conf, 0.4))
                c.line(X, PY, X + CW, PY, c.theme("faint", "d_line"), 5)
                note(c, X + 470, 1380, "jalan keluar kebuka", prog(t, t_open + 0.5, 0.5), size=38)
        bx, by, bw, bh = BOOK

        def book(c, rows, fail, found, chip, alpha=1.0):
            scan = (0, prog(t, t_num - 0.3, 0.6)) if t >= t_num - 0.3 else None
            buku_alamat(c, bx, by, bw, bh, rows, scan=scan, fail=fail, found=found, chip=chip, alpha=alpha)

        def content(c):
            old, new = swap(t, t_new)
            if old > 0.01:
                book(c, ROWS_OLD, prog(t, t_err, 0.6), 0.0, "DNS", old)
            if new > 0.01:
                book(c, ROWS_OLD, 0.0, prog(t, t_ok, 0.5), "DNS BARU", new)
            sheen(c, t, t_new, BOOK, r=24)
        appear(c, t, L14.start, e - OUT, BOOK, content, enter="up", exit="up")
        if t >= t_g:
            fade(c, t, t_g, e - OUT, lambda c: pop_tag(c, t, t_g, X, 1330, "8.8.8.8", C["accent"]))
            fade(c, t, t_cf, e - OUT, lambda c: pop_tag(c, t, t_cf, X + 200, 1330, "1.1.1.1", C["accent"]))
        if t >= t_ok:
            check_badge(c, X + 420, 1352, 34, out_back(prog(t, t_ok, 0.4)) * (1 - prog(t, e - OUT, OUT)))
            fade(c, t, t_rusak, e - OUT, lambda c: note(c, X + 480, 1440, "punya ISP-mu", 1.0, size=40))
    v.add(s, e, draw, z=20)
    v.camera.focus(t_conf - 0.2, (PX - 100, PY - 360, 420, 360), zoom=1.08, dur=0.9)
    v.camera.key(L14.start, zoom=1.06, y=960, dur=0.01).key(L14.start + 0.1, zoom=1.0, y=960, dur=1.6)
    v.sfx("whoosh", s + 0.1, 0.6)
    v.sfx("chime", t_open, 0.6)
    v.sfx("pop", t_conf)
    v.sfx("whoosh", L14.start, 0.6)
    v.sfx("tick", t_num, 0.6)
    v.sfx("thud", t_err + 0.3)
    v.sfx("whoosh", t_new, 0.5)
    v.sfx("pop", t_g)
    v.sfx("pop", t_cf)
    v.sfx("chime", t_ok)


# ── RECAP (dark): the envelope gets out and back → the big icon, no "!" ──────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L18, L19 = T["L18"], T["L19"]
    t_dns, t_hidup, t_alamat = T.word("L18", "DNS"), T.word("L19", "hidup"), T.word("L19", "alamat")
    hs = _heads(T, [("Yang aku cek\nduluan: *DNS*.", "L18"), ("Internetnya\n*hidup*.", "L19")], e - OUT,
                style="headline_dark")
    t_go = s + 0.6
    px = POS_X + POS_S / 2 + POS_S * 0.16

    def env(t):                                                # out through the open gate, and back home
        u = prog(t, t_go + 0.5, 2.6)
        if u <= 0 or u >= 1:
            return None
        far = X + CW - 30
        if u < 0.5:
            k = in_out_cubic(u * 2)
            return ICON[0] + (far - ICON[0]) * k, 1 - prog(u, 0.38, 0.12)
        k = in_out_cubic((u - 0.5) * 2)
        return far + (ICON[0] - far) * k, prog(u, 0.5, 0.12)

    def draw(c, t):
        _draw_heads(c, t, hs)
        a = _io(t, s + 0.2, L19.start - 0.2)
        if a > 0.002:
            with c.group(a), c.at(0, _lift(t, L19.start - 0.2)):
                _komplek(c, t, rise=0, p_open=spring_at(t, t_go, "heavy"), wifi=1.0,
                         bang=1 - prog(t, t_go + 3.2, 0.4), env=env(t), labels=0.0)
            if t >= t_dns:
                pa = out_back(prog(t, t_dns, 0.4)) * (1 - prog(t, L19.start - 0.2, OUT))
                with c.at(0, 0, max(0.01, pa), origin=(X, 1420)):
                    word_pill(c, X, 1370, "DNS.", ORANGE, size=96, alpha=min(1, pa))
                note(c, X + 330, 1440, "it's always DNS", prog(t, t_dns + 0.5, 0.5) * (1 - prog(t, L19.start - 0.2, OUT)),
                     size=40)
        m = _io(t, L19.start, e - OUT, d_in=0.6)
        if m > 0.002:
            with c.at(0, 30 * (1 - m) + _lift(t, e - OUT)):
                wifi_icon(c, MID, 1150, 230, bars=3, bang=0.0, alpha=m)
            fade(c, t, t_alamat, e - OUT, lambda c: c.text(X, 1360, "cuma nggak nemu alamat.", F["ui_semi"], 38,
                                                            C["d_muted"]))
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.04, y=1000, dur=3.0)
    v.camera.reset(L19.start, dur=0.8)
    v.sfx("whoosh_dark", s)
    v.sfx("chime", t_go, 0.5)
    v.sfx("whoosh", t_go + 0.5, 0.4)
    v.sfx("pop", t_go + 3.2, 0.6)
    v.sfx("thud", t_dns)
    v.sfx("chime", t_hidup, 0.6)
