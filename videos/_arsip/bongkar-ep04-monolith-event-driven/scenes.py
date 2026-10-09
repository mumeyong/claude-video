"""Bongkar Arsitektur EP04 — Monolith lama, dipecah jadi event-driven. See IDENTITY.md / TREATMENT.md.

Metaphor: kampung + kentongan pos ronda (monolith = one big house, function = small house, event = kentongan).
Signature move: the kentongan is struck → rings run out → only the houses that listen light up, work, go dark again.
Signature color: teal. Hook: contrarian claim ("kebanyakan tidur"). No numbers (none given).
"""
from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_cubic, in_out_cubic, clamp
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, note, follow_button, arch_node,
                               series_bumper, kentongan, sound_rings, rumah, rumah_gede, gang, portal, ronda_man,
                               cover, KAMPUNG_TEAL as TEAL)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · MASALAH", "01 · KEPUTUSAN", "02 · DIAGRAM", "03 · HASIL", "RECAP", "OUTRO"]
OK = C["ok"]
RED = C["rec"]
ROOMS = ["order", "bayar", "notifikasi", "laporan"]
FNS = ["order()", "bayar()", "notif()", "laporan()"]


def build(project):
    T = project.timing
    v = Video(duration=T["L27"].end + TAIL, bpm=128, beat_offset=0.0, series="BONGKAR ARSITEKTUR · EP 04")
    v.cover_t = T.word("L04", "event") + 0.6
    v.music = dict(key="Eb", mood="warm")            # generated score: after D bright (qris) and A dreamy (roadmap)
    v.cover = lambda c: cover(c, "Aplikasinya\nkebanyakan *tidur*.", kicker="BONGKAR ARSITEKTUR · EP 04",
                              color=TEAL, badge="EP 04", tags=["event-driven", "serverless", "multi-cloud"],
                              hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    b["00 · MASALAH"] = T["L04"].end + 0.1           # chapter + bumper start right after L04
    intro(v, T, 0.0, b["00 · MASALAH"])
    masalah(v, T, b["00 · MASALAH"], b["01 · KEPUTUSAN"])
    keputusan(v, T, b["01 · KEPUTUSAN"], b["02 · DIAGRAM"])
    diagram(v, T, b["02 · DIAGRAM"], b["03 · HASIL"])
    hasil(v, T, b["03 · HASIL"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


def _cover_hero(c, box):
    """Cover hero: the gang at night-rest — kentongan rings, one window awake among sleeping houses."""
    x, y, w, h = box
    s = min(170, h * 0.42)
    base = y + h - 60
    kentongan(c, x + s * 0.75, base - s * 2.1, s * 0.95)
    sound_rings(c, x + s * 0.75, base - s * 1.4, 0.45, TEAL, r_max=w * 0.9, squash=0.55)
    for k in range(3):
        cx_ = x + w * (0.42 + 0.22 * k)
        rumah(c, cx_, base, s, 0.0, light=1.0 if k == 1 else 0.0, busy=1.0 if k == 1 else 0.0,
              sleep=0.0 if k == 1 else 1.0, seed=k)
    gang(c, x, base, w)


def _pop_tag(c, t, t0, x, y, label, color, h=44, align="l"):
    """Tag that pops in at t0 (scale overshoot)."""
    if t < t0:
        return
    p = out_back(prog(t, t0, 0.4), 1.6)
    with c.at(0, 0, max(0.01, p), origin=(x, y + h / 2)):
        tag(c, x, y, label, color, clamp(p * 2), align=align, h=h)


def _tag_c(c, cx, y, label, color, alpha=1.0, h=44):
    """Tag centered on cx."""
    w = c.measure(label, F["ui"], tk.T["tag"][0], tk.T["tag"][1])[0] + 30
    tag(c, cx - w / 2, y, label, color, alpha, h=h)


def _pulse(t, t_on, t_off, d_on=0.3, d_off=0.5):
    """0 → 1 at t_on, back to 0 at t_off (window light / busy envelope)."""
    if t < t_on:
        return 0.0
    return out_expo(prog(t, t_on, d_on)) * (1 - in_cubic(prog(t, t_off, d_off)))


def _flicker(t, t_on):
    """A lamp that blinks once before it stays on (deliberate imperfection)."""
    if t < t_on:
        return 0.0
    d = t - t_on
    if d < 0.08:
        return 1.0
    if d < 0.2:
        return 0.0
    return out_expo(prog(t, t_on + 0.2, 0.25))


def _room_centers(x, w, n=4):
    """Window centers of rumah_gede(x, w, mcb=True) — same geometry as the component."""
    rx0 = x + 86
    rw = (x + w - 20 - rx0) / n
    return [rx0 + rw * (k + 0.5) for k in range(n)], rw


# ── INTRO: the sleeping gang → one window wakes → the monolith → punch → bumper ─
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3, L4, L5 = T["L01"], T["L02"], T["L03"], T["L04"], T["L05"]
    t_tidur = T.word("L01", "tidur")
    t_hit = T.word("L02", "kejadian")
    t_done = T.word("L02", "selesai")
    t_terus = T.word("L03", "terus")
    t_semua = T.word("L03", "semuanya")
    t_ed = T.word("L04", "event")
    headA = Headline("Kebanyakan *tidur*.")
    headB = Headline("Bangun pas ada *kejadian*.")
    headC = Headline("Dulu: nyala *terus*.")
    kx, ktop, ks = X + 100, 720, 190
    base = ktop + ks * 2.1
    hx = [X + 330, X + 530, X + 730]
    scene = (X, 600, CW, 700)
    gede = (X, 1180, CW, 400)
    bump0, bump1 = e, max(e + 1.4, L5.start - 0.05)

    cam = v.camera
    cam.key(0.0, zoom=1.1, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.8, ease=out_cubic)
    cam.focus(t_hit + 0.3, (hx[1] - 120, base - 260, 240, 260), zoom=1.08, dur=0.6)
    cam.reset(t_done + 0.2, dur=0.6)
    cam.key(t_ed, zoom=0.97, dur=0.12)
    cam.key(t_ed + 0.12, zoom=1.0, dur=0.4)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "SERVERLESS · AWS + ALIBABA", TEAL)
        headA.draw(c, t, L1.start, L2.start - 0.15)
        headB.draw(c, t, L2.start, L3.start - 0.15)
        headC.draw(c, t, L3.start, L4.start - 0.15)

        def street(c):
            hit = prog(t, t_hit, 0.8) if t >= t_hit else 0.0
            kentongan(c, kx, ktop, ks, hit)
            sound_rings(c, kx, ktop + ks * 0.7, prog(t, t_hit + 0.05, 1.3), TEAL, r_max=760, squash=0.55)
            for k, cx_ in enumerate(hx):
                lt = _pulse(t, t_hit + 0.45, t_done + 0.1) if k == 1 else 0.0
                rumah(c, cx_, base, 170, t, light=lt, busy=lt, sleep=1 - lt, seed=k)
            gang(c, X, base, CW)
            fade(c, t, t_tidur, t_hit - 0.1,
                 lambda c: c.text(hx[2] + 90, ktop - 30, "zzz…", F["serif"], 52, c.theme("muted", "d_muted"),
                                  1, align="r"))
        appear(c, t, L1.start - 0.1, L3.start - 0.15, scene, street, enter="up", exit="left")

        def monolith(c):
            x, by, w, h = gede
            rumah_gede(c, x + 20, by, w - 40, 400, [dict(light=1.0, busy=0.4 if k == 3 else 0.0) for k in range(4)],
                       t, mcb=False)
            _pop_tag(c, t, t_terus, x + 20, by + 50, "nyala 24 jam", RED)
            _pop_tag(c, t, t_semua, x + w - 20, by + 50, "ngerjain semuanya", TEAL, align="r")
        appear(c, t, L3.start - 0.1, L4.start - 0.15, (X, 620, CW, 640), monolith, enter="right", exit="up")

        def punch(c):
            p = prog(t, t_ed, 0.35)
            a0 = out_expo(prog(t, L4.start, 0.4))
            c.text(MID, 840, "monolith lama", F["mono_med"], 32, c.theme("ink2", "d_muted"), a0, 0.06, align="c")
            c.line(MID, 880, MID, 880 + 70 * a0, c.theme("faint", "d_line"), 4)
            word = "event-driven."
            size = min(140, 140 * CW / c.measure(word, F["display"], 140, -0.06)[0])
            with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, 1060)):
                c.text(MID, 1100, word, F["display"], size, TEAL, clamp(p * 3), -0.06, align="c")
        appear(c, t, L4.start, e - OUT, (X, 780, CW, 400), punch, enter="up", blur=4)
    v.add(s, e + 0.4, draw)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 4, "BL-Revamp serverless", TEAL), z=100)
    v.sfx("whoosh", L1.start - 0.1, 0.5)
    v.sfx("thud", t_hit, 0.8)
    v.sfx("pop", t_hit + 0.45, 0.5)
    v.sfx("pop", t_done + 0.1, 0.3)
    v.sfx("whoosh", L3.start - 0.1, 0.5)
    v.sfx("pop", t_terus, 0.5)
    v.sfx("pop", t_semua, 0.5)
    v.sfx("whoosh", L4.start - 0.1, 0.5)
    v.sfx("thud", t_ed)
    v.sfx("whoosh", bump0, 0.8)
    v.sfx("whoosh", bump1 - 0.35, 0.5)


# ── 00 · MASALAH: one big house — all lit, one room working, one short circuit ─
def masalah(v, T, s, e):
    ch = v.chapter(0, "MASALAH", s, e)
    L5, L6, L7, L8, L9 = T["L05"], T["L06"], T["L07"], T["L08"], T["L09"]
    t_rumah = T.word("L05", "rumah")
    t_rooms = [T.word("L06", w) for w in ("order", "bayar", "notifikasi", "laporan")]
    t_atap = T.word("L06", "atap")
    t_satu = T.word("L07", "satu")
    t_kors = T.word("L08", "korslet")
    t_gelap = T.word("L08", "gelap")
    t_deploy = T.word("L09", "deploy")
    t_ulang = T.word("L09", "ulang")
    head1 = Headline("Satu *rumah gede*.")
    head2 = Headline("*Satu* atap.")
    head3 = Headline("Kerja cuma *satu kamar*.")
    head4 = Headline("Satu *korslet*?")
    head5 = Headline("Deploy *semuanya*.")
    box = (X, 560, CW, 780)
    hx, hb, hw, hh = X + 40, 560 + 600, CW - 80, 400
    centers, rw = _room_centers(hx, hw)
    tag_y = 560 + 670

    cam = v.camera
    cam.focus(L6.start, (X, 760, CW, 400), zoom=1.05, dur=0.9)
    cam.focus(t_kors - 0.1, (centers[3] - 140, 800, 280, 300), zoom=1.12, dur=0.35)
    cam.reset(t_gelap + 0.2, dur=0.6)
    cam.key(t_ulang, zoom=0.97, dur=0.12)
    cam.key(t_ulang + 0.12, zoom=1.0, dur=0.4)

    def draw(c, t):
        kicker(c, t, L5.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L5.start, L6.start - 0.15)
        head2.draw(c, t, L6.start, L7.start - 0.15)
        head3.draw(c, t, L7.start, L8.start - 0.15)
        head4.draw(c, t, L8.start, L9.start - 0.15)
        head5.draw(c, t, L9.start, e - OUT)
        trip = in_out_cubic(prog(t, t_gelap - 0.1, 0.25))
        broken = out_expo(prog(t, t_kors, 0.3))

        def house(c):
            x, y, w, h = box
            c.card(x, y, w, h, r=30)
            c.text(x + 30, y + 50, "APLIKASI LAMA · MONOLITH", F["mono_bold"], 19, c.theme("muted", "d_muted"), 1,
                   0.16)
            rooms = []
            for k in range(4):
                lt = out_expo(prog(t, t_rooms[k], 0.3))
                busy = out_expo(prog(t, L7.start, 0.4)) if k == 3 else 0.0
                rooms.append(dict(label=ROOMS[k], light=lt, busy=busy, broken=broken if k == 3 else 0.0))
            pl = sum(out_expo(prog(t, tt, 0.3)) for tt in t_rooms) / 4
            rumah_gede(c, hx, hb, hw, hh, rooms, t, trip=trip, closed=prog(t, t_ulang, 0.4), p_labels=pl)
            # one roof: a teal bracket over all rooms at "atap"
            pa = in_out_cubic(prog(t, t_atap, 0.5)) * (1 - prog(t, L7.start, 0.3))
            if pa > 0:
                y0 = hb - hh - hh * 0.38 - 24
                c.line(centers[0] - rw / 2, y0, centers[0] - rw / 2 + (centers[-1] - centers[0] + rw) * pa, y0,
                       TEAL, 6)
            # idle rooms: lit but nobody working
            ia = out_expo(prog(t, t_satu, 0.4)) * (1 - prog(t, L8.start, 0.3))
            if ia > 0:
                for k in range(3):
                    c.text(centers[k], hb - hh * 0.3, "idle", F["mono_bold"], 18, RED, ia, 0.1, align="c")
            with c.group(1 - prog(t, L8.start, 0.3)):
                _pop_tag(c, t, t_satu + 0.2, x + 40, tag_y, "idle · tetap nyala", RED)
            with c.group(1 - prog(t, L9.start, 0.3)):
                _pop_tag(c, t, t_gelap, x + 40, tag_y, "down semua", RED)
            _pop_tag(c, t, t_ulang + 0.15, x + 40, tag_y, "deploy ulang: semuanya", RED)
            if t >= t_deploy:
                _pop_tag(c, t, t_deploy, x + w - 40, tag_y, "cuma benerin laporan", C["accent"], align="r")
        appear(c, t, L5.start - 0.1, e - OUT, box, house, enter="up")
        fade(c, t, t_rumah + 0.3, L7.start - 0.1,
             lambda c: note(c, X + CW - 40, 690, "ini monolith-nya", prog(t, t_rumah + 0.4, 0.9),
                            arrow_to=(X + CW * 0.62, hb - hh - 40), align="r", size=40))
    v.add(s, e, draw)
    v.sfx("whoosh", L5.start - 0.1, 0.6)
    for tt in t_rooms:
        v.sfx("pop", tt, 0.4)
    v.sfx("tick", t_atap, 0.4)
    v.sfx("pop", t_satu + 0.2, 0.4)
    v.sfx("thud", t_kors, 0.6)
    v.sfx("whoosh", t_gelap - 0.1, 0.5)
    v.sfx("pop", t_deploy, 0.4)
    v.sfx("thud", t_ulang, 0.8)


# ── 01 · KEPUTUSAN: split into small houses, the kentongan, the signature move ─
def keputusan(v, T, s, e):
    ch = v.chapter(1, "KEPUTUSAN", s, e)
    L10, L11, L12, L13, L14 = T["L10"], T["L11"], T["L12"], T["L13"], T["L14"]
    t_split = T.word("L10", "dipecah")
    t_fn = T.word("L11", "function")
    t_tugas = T.word("L11", "tugas")
    t_call = T.word("L12", "panggil")
    t_kent = T.word("L12", "kentongan")
    t_order = T.word("L13", "order")
    t_hit = T.word("L13", "dipukul")
    t_event = T.word("L13", "event")
    t_nyala = T.word("L14", "nyala")
    t_kerja = T.word("L14", "kerja")
    t_gelap = T.word("L14", "gelap")
    heads = [(Headline("Rumahnya *dipecah*."), L10.start, L11.start - 0.15),
             (Headline("Satu function, *satu tugas*."), L11.start, L12.start - 0.15),
             (Headline("Nggak saling *panggil*."), L12.start, L13.start - 0.15),
             (Headline("Kentongan = *event*."), L13.start, L14.start - 0.15),
             (Headline("Nyala, kerja, *gelap lagi*."), L14.start, e - OUT)]
    hs, hb = 160, 1220
    hx = [X + CW * (0.125 + 0.25 * k) for k in range(4)]
    gx, gw = X + 20, CW - 40
    rc, rw = _room_centers(gx, gw)
    kx, ktop, ks = MID, 600, 140
    ring_y = ktop + ks * 0.7
    t_sleep = L12.start
    t_lbl = [t_fn + 0.1 + k * 0.18 for k in range(4)]
    # (house, on, busy) — house 0 (order) never listens to this event
    lit = {1: t_nyala - 0.1, 2: t_nyala + 0.15, 3: t_nyala + 0.05}

    cam = v.camera
    cam.key(t_split, zoom=0.97, dur=0.12)
    cam.key(t_split + 0.12, zoom=1.0, dur=0.4)
    cam.focus(t_kent - 0.1, (kx - 200, ktop - 60, 400, 380), zoom=1.07, dur=0.6)
    cam.reset(t_hit + 0.1, dur=0.7)

    def draw(c, t):
        kicker(c, t, L10.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        sp = in_out_cubic(prog(t, t_split, 0.7))

        def town(c):
            if sp < 1:
                with c.group(1 - clamp(sp * 3)):
                    rumah_gede(c, gx, hb, gw, 330, [dict(light=1.0) for _ in range(4)], t, mcb=True)
            if sp > 0:
                for k in range(4):
                    cx_ = rc[k] + (hx[k] - rc[k]) * sp
                    size = rw + (hs - rw) * sp
                    on = 1 - prog(t, t_sleep, 0.5)
                    if k in lit:
                        lamp = _flicker(t, lit[k]) if k == 2 else out_expo(prog(t, lit[k], 0.3)) if t >= lit[k] else 0
                        on = max(on, lamp * (1 - in_cubic(prog(t, t_gelap + 0.1 * k, 0.5))))
                    busy = on * prog(t, t_kerja, 0.3) * (1 - prog(t, t_gelap, 0.3)) if k in lit else 0.0
                    sleep = prog(t, t_sleep + 0.3, 0.6) * (1 - on)
                    lbl = FNS[k] if t >= t_lbl[k] else None
                    rumah(c, cx_, hb, size, t, light=on, busy=busy, sleep=sleep, label=lbl,
                          label_rot=0.07 if k == 2 else 0.0, label_color=TEAL, alpha=clamp(sp * 3), seed=k)
            gang(c, X, hb, CW, alpha=sp)
            # direct calls between houses → struck out
            wa = out_expo(prog(t, L12.start, 0.4)) * (1 - prog(t, t_kent, 0.4))
            if wa > 0:
                for k in range(3):
                    x0, x1 = hx[k] + 50, hx[k + 1] - 50
                    y0 = hb - 150
                    mx = (x0 + x1) / 2
                    c.line(x0, y0, x1, y0, c.theme("ink2", "d_muted"), 4, wa)
                    xp = out_back(prog(t, t_call + k * 0.12, 0.3), 1.6) if t >= t_call + k * 0.12 else 0
                    if xp > 0:
                        m = 16 * xp
                        c.line(mx - m, y0 - m, mx + m, y0 + m, RED, 6, wa)
                        c.line(mx - m, y0 + m, mx + m, y0 - m, RED, 6, wa)
        appear(c, t, L10.start - 0.1, e - OUT, (X, 820, CW, 500), town, enter="up")

        def pole(c):
            hit = prog(t, t_hit, 0.8) if t >= t_hit else 0.0
            kentongan(c, kx, ktop, ks, hit)
            sound_rings(c, kx, ring_y, prog(t, t_hit + 0.05, 1.4), TEAL, r_max=720, squash=0.7)
        appear(c, t, t_kent - 0.15, e - OUT, (kx - 160, ktop - 60, 320, ks * 2.4), pole, enter="down")
        if t >= t_order:
            with c.group(1 - prog(t, L14.start, 0.3)):
                _pop_tag(c, t, t_order, X, ktop + 40, "order masuk", C["accent"])
                _pop_tag(c, t, t_event, X + CW, ktop + 40, "event: order.created", TEAL, align="r")
        fade(c, t, t_kerja, e - 0.6,
             lambda c: note(c, X + 10, 1400, "order() tetap tidur", prog(t, t_kerja + 0.1, 0.9),
                            arrow_to=(hx[0] + 10, hb + 70), size=40))
    v.add(s, e, draw)
    v.sfx("pop", L10.start - 0.1, 0.4)
    v.sfx("thud", t_split, 0.7)
    v.sfx("whoosh", t_split + 0.1, 0.4)
    for tt in t_lbl:
        v.sfx("pop", tt, 0.35)
    for k in range(3):
        v.sfx("tick", t_call + k * 0.12, 0.45)
    v.sfx("whoosh", t_kent - 0.15, 0.5)
    v.sfx("pop", t_order, 0.4)
    v.sfx("thud", t_hit, 0.9)
    v.sfx("pop", t_event, 0.4)
    for tt in lit.values():
        v.sfx("pop", tt, 0.35)
    v.sfx("chime", t_gelap + 0.3, 0.6)


# ── 02 · DIAGRAM: API → event → 3 functions, inside a private network, out via NAT ─
def diagram(v, T, s, e):
    ch = v.chapter(2, "DIAGRAM", s, e)
    L15, L16, L17, L18, L19 = T["L15"], T["L16"], T["L17"], T["L18"], T["L19"]
    t_api = T.word("L15", "API")
    t_ev = T.word("L15", "event")
    t_bar = T.word("L16", "barengan")
    t_fns = [T.word("L16", w) for w in ("bayar", "notifikasi", "laporan")]
    t_aws = T.word("L17", "Lambda")
    t_ali = T.word("L17", "Alibaba")
    t_priv = T.word("L18", "private")
    t_luar = T.word("L18", "luar")
    t_nat = T.word("L19", "NAT")
    t_pintu = T.word("L19", "pintu")
    heads = [(Headline("API → *event*."), L15.start, L16.start - 0.15),
             (Headline("Didengar *barengan*."), L16.start, L17.start - 0.15),
             (Headline("Lambda + *Function Compute*."), L17.start, L18.start - 0.15),
             (Headline("Dalam *private network*."), L18.start, L19.start - 0.15),
             (Headline("Keluar lewat *NAT gateway*."), L19.start, e - OUT)]
    NW = 360
    users = (X, 560, NW, 86)
    api = (X + CW - NW, 560, NW, 86)
    evb = (MID - 230, 700, 460, 150)
    hs, hb = 150, 1050
    hx = [X + CW * f for f in (1 / 6, 3 / 6, 5 / 6)]
    PW = (CW - 24) / 2
    prov = [(X, 1120, PW, 70, "AWS Lambda", t_aws), (X + PW + 24, 1120, PW, 70, "Alibaba Function Compute", t_ali)]
    fence = (X, 603, CW, 1262 - 603)
    pb = 1330                               # portal base
    t_run = t_bar - 0.2

    cam = v.camera
    cam.focus(L15.start + 0.1, (X, 540, CW, 330), zoom=1.06, dur=0.7)
    cam.focus(L16.start, (X, 880, CW, 300), zoom=1.05, dur=0.7)
    cam.reset(L17.start, dur=0.6)
    cam.key(t_priv - 0.1, zoom=0.96, dur=0.8)
    cam.focus(L19.start, (MID - 300, 1150, 600, 300), zoom=1.08, dur=0.7)
    cam.reset(e - 1.0, dur=0.6)

    def draw(c, t):
        kicker(c, t, L15.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        muted, faint = c.theme("muted", "d_muted"), c.theme("faint", "d_line")

        def graph(c):
            # private network fence (draws on at L18)
            pf = in_out_cubic(prog(t, t_priv - 0.2, 0.9))
            if pf > 0:
                x, y, w, h = fence
                c.fill_rrect(x, y, w, h, 30, (*TEAL[:3], 0.04 * pf))
                c.stroke_rrect(x, y, w, h, 30, TEAL, 3, pf, dash=[16, 12])
                c.text(x + 30, y + h - 18, "PRIVATE NETWORK", F["mono_bold"], 18, TEAL, pf, 0.16)
            # row 1: order masuk → API
            a_u = out_expo(prog(t, L15.start + 0.05, 0.4))
            a_a = out_expo(prog(t, t_api, 0.4))
            arch_node(c, dict(x=users[0], y=users[1], w=NW, h=86, kind="users", label="order masuk", a=a_u))
            arch_node(c, dict(x=api[0], y=api[1], w=NW, h=86, kind="svc", label="API", a=a_a))
            pl = in_out_cubic(prog(t, t_api + 0.1, 0.4))
            ay = users[1] + 43
            c.line(X + NW + 10, ay, X + NW + 10 + (api[0] - X - NW - 20) * pl, ay, faint, 5)
            if t >= t_api + 0.5:
                f = ((t - t_api) * 0.9) % 1.0
                c.circle(X + NW + 10 + (api[0] - X - NW - 20) * f, ay, 7, C["accent"], min(1, f * 6, (1 - f) * 6))
            # API ↓ event (kentongan node)
            ex, ey, ew, eh = evb
            pe = in_out_cubic(prog(t, t_ev - 0.2, 0.4))
            acx = api[0] + NW / 2
            if pe > 0:
                c.line(acx, api[1] + 90, acx, api[1] + 90 + (ey + eh / 2 - api[1] - 90) * pe, faint, 5)
                c.line(acx, ey + eh / 2, acx - (acx - ex - ew) * clamp(pe * 2 - 1), ey + eh / 2, faint, 5)
            es = out_back(prog(t, t_ev, 0.45), 1.5) if t >= t_ev else 0
            if es > 0.01:
                with c.at(0, 0, max(0.01, es), origin=(ex + ew / 2, ey + eh / 2)):
                    c.card(ex, ey, ew, eh, r=24)
                    tick = (t - t_bar) % 2.0 if t >= t_bar else 9.0
                    kentongan(c, ex + 70, ey + 18, 56, prog(tick, 0, 0.8) if tick < 1 else 0.0)
                    c.text(ex + 150, ey + 74, "event", F["display_semi"], 44, c.theme("ink", "d_ink"), 1, -0.03)
                    c.text(ex + 150, ey + 112, "order.created", F["mono_med"], 19, TEAL, 1, 0.04)
            # fan-out ↓ to 3 functions
            pfan = in_out_cubic(prog(t, L16.start, 0.5))
            for k in range(3):
                x0, y0 = ex + ew / 2, ey + eh + 4
                x1, y1 = hx[k], hb - hs * 0.62 - hs * 0.36 - 14
                if pfan > 0:
                    c.line(x0, y0, x0 + (x1 - x0) * pfan, y0 + (y1 - y0) * pfan, faint, 4)
                if t >= t_run:
                    f = ((t - t_run) * 1.1) % 1.0
                    c.circle(x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, 7, TEAL, min(1, f * 6, (1 - f) * 6))
                a_h = out_expo(prog(t, t_fns[k], 0.4)) if t >= L16.start else 0.0
                on = out_expo(prog(t, t_run + 0.3, 0.3)) * (1 - 0.6 * prog(t, L18.start, 0.6))
                rumah(c, hx[k], hb, hs, t, light=on, busy=on, label=FNS[k + 1], label_color=TEAL, alpha=a_h,
                      seed=k + 4)
            # provider row
            for (px, py, pw, ph, lbl, tt) in prov:
                a = out_expo(prog(t, tt, 0.4))
                if a <= 0.01:
                    continue
                with c.group(a):
                    c.card(px, py, pw, ph, r=20, shadow="card_tight")
                    c.circle(px + 30, py + ph / 2, 8, TEAL)
                    c.text(px + 50, py + ph / 2 + 9, lbl, F["ui_semi"], 26 if len(lbl) < 14 else 23,
                           c.theme("ink", "d_ink"), 1, -0.01)
            # outsider tries to come in from below → bounced
            if t >= t_luar - 0.6:
                f = clamp((t - (t_luar - 0.6)) / 0.6)
                yb = fence[1] + fence[3]
                oy = 1450 - (1450 - yb - 14) * out_cubic(f) + 60 * in_cubic(prog(t, t_luar, 0.5))
                oa = 1 - prog(t, t_luar + 0.4, 0.3)
                ox = X + CW * 0.8
                c.circle(ox, oy, 10, RED, oa)
                if t >= t_luar:
                    m = 14 * out_back(prog(t, t_luar, 0.3), 1.6)
                    c.line(ox - m, yb - m, ox + m, yb + m, RED, 6, oa)
                    c.line(ox - m, yb + m, ox + m, yb - m, RED, 6, oa)
        appear(c, t, L15.start - 0.1, e - OUT, (X, 540, CW, 900), graph, blur=4, rise=20)

        def gate(c):
            p_open = _pulse(t, t_pintu, t_pintu + 1.4, 0.5, 0.5)
            portal(c, MID, pb, 240, p_open, "NAT gateway")
            # out ✓: a teal dot leaves through the gate
            if t >= t_pintu:
                f = prog(t, t_pintu + 0.3, 1.0)
                c.circle(MID, 1200 + 240 * in_out_cubic(f), 10, TEAL, 1 - prog(t, t_pintu + 1.2, 0.2))
                _pop_tag(c, t, t_pintu + 1.0, MID + 150, pb + 60, "keluar: boleh", OK)
            _pop_tag(c, t, t_nat + 0.2, MID - 150, pb + 60, "masuk: ditolak", RED, align="r")
        appear(c, t, L19.start - 0.1, e - OUT, (MID - 200, pb - 150, 400, 240), gate, enter="up")
    v.add(s, e, draw)
    v.sfx("pop", L15.start + 0.05, 0.4)
    v.sfx("pop", t_api, 0.4)
    v.sfx("pop", t_ev, 0.5)
    v.sfx("whoosh", L16.start, 0.4)
    for tt in t_fns:
        v.sfx("pop", tt, 0.35)
    v.sfx("thud", t_bar, 0.5)
    v.sfx("pop", t_aws, 0.45)
    v.sfx("pop", t_ali, 0.45)
    v.sfx("whoosh", t_priv - 0.2, 0.5)
    v.sfx("tick", t_luar, 0.6)
    v.sfx("pop", L19.start, 0.4)
    v.sfx("whoosh", t_pintu, 0.4)
    v.sfx("chime", t_pintu + 1.0, 0.6)


# ── 03 · HASIL: overhead down → one error, the rest keep going → deploy one ─
def hasil(v, T, s, e):
    ch = v.chapter(3, "HASIL", s, e)
    L20, L21, L22 = T["L20"], T["L21"], T["L22"]
    t_dras = T.word("L20", "drastis")
    t_err = T.word("L21", "error")
    t_jalan = T.word("L21", "jalan")
    t_satu = T.word("L22", "satu")
    head1 = Headline("Compute *overhead*:")
    head2 = Headline("Satu error, *yang lain jalan*.")
    head3 = Headline("Deploy *satu function*.")
    card = (X, 600, CW, 640)
    hs, hb = 160, 600 + 440
    hx = [X + CW * (0.125 + 0.25 * k) for k in range(4)]
    work = [(0.0, 1.6), (0.5, 1.9), (1.1, 1.5), (0.3, 2.1)]     # (phase, period) of each function's own rhythm

    cam = v.camera
    cam.key(t_dras, zoom=0.97, dur=0.12)
    cam.key(t_dras + 0.12, zoom=1.0, dur=0.4)
    cam.focus(t_err - 0.1, (hx[3] - 150, 800, 300, 340), zoom=1.08, dur=0.5)
    cam.reset(t_jalan + 0.2, dur=0.6)

    def draw(c, t):
        kicker(c, t, L20.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L20.start, L21.start - 0.15)
        head2.draw(c, t, L21.start, L22.start - 0.15)
        head3.draw(c, t, L22.start, e - OUT)
        ink, muted = c.theme("ink", "d_ink"), c.theme("muted", "d_muted")

        def punch(c):
            c.text(MID, 820, "turun", F["display"], 120, ink, out_expo(prog(t, L20.start + 0.3, 0.5)), -0.05,
                   align="c")
            p = prog(t, t_dras, 0.35)
            dy = -160 * (1 - out_expo(p))
            size = min(220, 220 * (CW - 40) / c.measure("drastis.", F["display"], 220, -0.06)[0])
            c.text(MID, 1040 + dy, "drastis.", F["display"], size, TEAL, clamp(p * 3), -0.06, align="c")
            # "lampu nyala" meter: monolith (always on) vs event-driven (only when there's an event)
            ma = out_expo(prog(t, t_dras + 0.3, 0.4))
            for k, (lbl, f) in enumerate((("monolith", 1.0), ("event-driven", 0.12))):
                y = 1140 + k * 70
                c.text(X + 40, y + 10, lbl, F["mono_med"], 20, muted, ma, 0.04)
                c.fill_rrect(X + 280, y - 8, CW - 320, 18, 9, c.theme("line", "d_line"), ma)
                fill = f if k == 0 else 1 - (1 - f) * in_out_cubic(prog(t, t_dras + 0.5, 1.0))
                c.fill_rrect(X + 280, y - 8, (CW - 320) * fill, 18, 9, RED if k == 0 else TEAL, ma)
            c.text(X + CW - 40, 1290, "lampu yang nyala", F["serif"], 36, muted, ma, align="r")
        appear(c, t, L20.start, L21.start - 0.15, (X, 700, CW, 620), punch, enter="up", exit="up", blur=4)

        def street(c):
            x, y, w, h = card
            c.card(x, y, w, h, r=30)
            c.text(x + 30, y + 50, "GANG FUNCTION", F["mono_bold"], 19, muted, 1, 0.16)
            fixed = out_expo(prog(t, t_satu + 0.6, 0.4))
            for k in range(4):
                ph, per = work[k]
                cyc = ((t + ph) % per) / per
                on = 1.0 if cyc < 0.55 else 0.25
                broken = out_expo(prog(t, t_err, 0.3)) * (1 - fixed) if k == 3 else 0.0
                rumah(c, hx[k], hb, hs, t, light=on if k != 3 or broken < 0.5 else 1.0, busy=on * (1 - broken),
                      broken=broken, label=FNS[k], label_color=RED if broken > 0.5 else TEAL, seed=k + 8)
            gang(c, x + 20, hb, w - 40)
            _pop_tag(c, t, t_err + 0.2, hx[3], y + h - 90, "error", RED, align="r")
            _pop_tag(c, t, t_jalan, x + 40, y + h - 90, "yang lain tetap jalan", OK)
            # deploy: one tag drops onto laporan() only
            if t >= t_satu:
                pd = out_cubic(prog(t, t_satu, 0.5))
                dy = -180 * (1 - pd)
                with c.group(clamp(pd * 3)):
                    _tag_c(c, hx[3], hb - hs * 1.2 + dy, "deploy", C["accent"])
                if fixed > 0.01:
                    with c.at(0, 0, max(0.01, out_back(fixed, 1.6)), origin=(hx[3] + 70, hb - hs * 0.9)):
                        c.circle(hx[3] + 70, hb - hs * 0.9, 20, OK)
                        icons.check(c, hx[3] + 70, hb - hs * 0.9, 17, (1, 1, 1, 1), 3.5)
            note(c, x + w - 30, y + h + 90, "yang lain nggak disentuh", prog(t, t_satu + 0.8, 0.9), align="r",
                 size=38)
        appear(c, t, L21.start - 0.1, e - OUT, card, street, enter="right")
    v.add(s, e, draw)
    v.sfx("pop", L20.start + 0.3, 0.4)
    v.sfx("whoosh", t_dras - 0.05, 0.4)
    v.sfx("thud", t_dras)
    v.sfx("tick", t_dras + 0.5, 0.4)
    v.sfx("whoosh", L21.start - 0.1, 0.5)
    v.sfx("thud", t_err, 0.6)
    v.sfx("pop", t_jalan, 0.5)
    v.sfx("pop", t_satu, 0.5)
    v.sfx("chime", t_satu + 0.6, 0.7)


# ── RECAP (dark): who strikes the kentongan never waits ─────────────────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L23, L24, L25 = T["L23"], T["L24"], T["L25"]
    t_mukul = T.word("L24", "mukul")
    t_nunggu = T.word("L24", "nunggu")
    t_pergi = T.word("L24", "pergi")
    t_biar = T.word("L25", "biarin")
    t_sehat = T.word("L25", "sehat")
    heads = [(Headline("Bukan soal *dipecah*.", style="headline_dark"), L23.start, L24.start - 0.15),
             (Headline("*Nggak nunggu* siapa-siapa.", style="headline_dark"), L24.start, L25.start - 0.15),
             (Headline("Sehat? *Biarin*.", style="headline_dark"), L25.start, e - OUT)]
    kx, ktop, ks = X + 110, 740, 170
    base = ktop + ks * 2.1
    hx = [X + 400, X + 580, X + 760]
    man0 = kx + 120
    t_walk = t_nunggu

    cam = v.camera
    cam.key(s, zoom=1.15, y=1000, dur=0.01)
    cam.key(t_mukul - 0.3, zoom=1.0, dur=1.6)

    def man_x(t):
        return man0 + 600 * in_out_cubic(prog(t, t_walk, 2.6)) if t >= t_walk else man0

    def draw(c, t):
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def night(c):
            hit = prog(t, t_mukul, 0.8) if t >= t_mukul else 0.0
            kentongan(c, kx, ktop, ks, hit)
            sound_rings(c, kx, ktop + ks * 0.7, prog(t, t_mukul + 0.05, 1.4), TEAL, r_max=760, squash=0.55)
            mx = man_x(t)
            for k, cx_ in enumerate(hx):
                t_on = t_mukul + 0.5 + 0.2 * k
                lt = _pulse(t, t_on, t_on + 2.4)
                rumah(c, cx_, base, 150, t, light=lt, busy=lt, sleep=1 - lt, seed=k + 20)
            gang(c, X, base, CW)
            arm = out_expo(prog(t, t_mukul - 0.25, 0.25)) * (1 - prog(t, t_mukul + 0.15, 0.3))
            walk = clamp((t - t_walk) * 3) * (1 - prog(t, t_walk + 2.4, 0.3)) if t >= t_walk else 0.0
            ronda_man(c, mx, base, 130, t, walk=walk, arm=arm, color=C["d_ink"],
                      alpha=1 - prog(t, t_walk + 1.8, 0.5))
            fa = out_expo(prog(t, t_pergi, 0.4))
            _tag_c(c, MID, base + 110, "fire-and-forget", TEAL, fa)
            c.text(man0 - 20, base + 200, "nggak nengok ke belakang", F["serif"], 38, C["d_muted"],
                   out_expo(prog(t, t_walk + 0.6, 0.6)) * (1 - fa))
        appear(c, t, L23.start - 0.1, L25.start - 0.15, (X, 640, CW, 640), night, enter="up", exit="down")

        def healthy(c):
            x, by, w = X + 104, 1160, CW - 208
            rumah_gede(c, x, by, w, 280, [dict(light=1.0, busy=0.6 if k % 2 else 0.0) for k in range(4)], t,
                       mcb=False)
            p = out_back(prog(t, t_sehat, 0.45), 1.8) if t >= t_sehat else 0
            if p > 0:
                with c.at(0, 0, max(0.01, p), origin=(x + w, by - 280)):
                    c.circle(x + w, by - 280, 34, OK)
                    icons.check(c, x + w, by - 280, 28, (1, 1, 1, 1), 4)
            _tag_c(c, MID, by + 60, "monolith sehat → biarin", OK, out_expo(prog(t, t_biar, 0.4)))
        appear(c, t, L25.start - 0.1, e - OUT, (X, 780, CW, 500), healthy, enter="pop")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("thud", t_mukul, 0.8)
    for k in range(3):
        v.sfx("pop", t_mukul + 0.5 + 0.2 * k, 0.3)
    v.sfx("whoosh", t_walk, 0.4)
    v.sfx("pop", t_pergi, 0.5)
    v.sfx("pop", L25.start - 0.1, 0.5)
    v.sfx("chime", t_biar)


# ── OUTRO: logo + EP05 teaser + follow ─────────────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L26, L27 = T["L26"], T["L27"]
    t_click = T.word("L27", "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, TEAL)
            c.text(X + 50, 892, "EPISODE BERIKUTNYA · EP 05", F["mono_bold"], 20, TEAL, 1, 0.16)
            c.text(X + 50, 962, "Legacy + container", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "Hidup berdampingan", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L26.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L27.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "Seri Bongkar Arsitektur", F["ui"], 28,
                                                          C["d_muted"], 1, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L27.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L26.start, 0.5)
    v.sfx("chime", t_click + 0.1)
