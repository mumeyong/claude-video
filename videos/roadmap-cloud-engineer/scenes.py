"""Roadmap jadi cloud engineer — idea #12, pillar C, QUICK. See IDENTITY.md / TREATMENT.md.

Metaphor: a commuter line (KRL) — skills are stations, the certificate is just the ticket. Signature move: the train
glides to the next station and every station it passed lights up. Color: orange. Hook: myth struck out.
Structure: the route, station 1 → 5.
"""
from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp, lerp
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, note, follow_button,
                               route_strip, train, cert_card, save_button, station_dots, cover, ORANGE)
from engine.components.motion import bezier_point
from engine.components.infra import _draw_poly

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · LINUX", "01 · NETWORKING", "02 · SATU CLOUD", "03 · IAC + KUBERNETES", "RECAP", "OUTRO"]
RED = C["rec"]
OK = C["ok"]
WHITE = (1, 1, 1, 1)

LX = X + 60                               # the line
YS = [640, 810, 980, 1150, 1320]          # stations
Y0, Y1 = YS[0] - 60, YS[-1] + 60
NAMES = ["Linux", "Networking", "Satu cloud", "Terraform", "Kubernetes"]
SUBS = [f"STASIUN {k + 1}" for k in range(5)]
DX, DW = X + 360, CW - 360                # detail cards, right of the labels


def build(project):
    T = project.timing
    v = Video(duration=T["L20"].end + TAIL, bpm=128, beat_offset=0.0, series="ROADMAP")
    v.cover_t = T.word("L14", "kubernetes") + 1.2
    v.music = dict(key="A", mood="dreamy")            # generated score: aspirational, after Bb warm (#07)
    v.cover = lambda c: cover(c, "Mulai dari\n*Linux*.", kicker="ROADMAP CLOUD ENGINEER", color=ORANGE,
                              badge="SAVE", tags=["5 stasiun", "urut, jangan loncat"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    arrive = [T["L03"].start, T["L06"].start, T["L09"].start, T["L12"].start, T["L14"].start]
    intro(v, T, 0.0, b["00 · LINUX"])
    route(v, T, T["L02"].start - 0.1, b["RECAP"], arrive)
    linux(v, T, b["00 · LINUX"], b["01 · NETWORKING"])
    networking(v, T, b["01 · NETWORKING"], b["02 · SATU CLOUD"])
    satu_cloud(v, T, b["02 · SATU CLOUD"], b["03 · IAC + KUBERNETES"])
    iac_k8s(v, T, b["03 · IAC + KUBERNETES"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


def _cover_hero(c, box):
    """Cover hero: the whole route lit, train arriving at Kubernetes."""
    x, y, w, h = box
    sp = (h - 100) / 4
    ys = [y + 50 + k * sp for k in range(5)]
    route_strip(c, x + 70, ys, 0.0, p_draw=1.0, reach=1.0, lit=[1] * 5, names=NAMES, subs=SUBS)
    train(c, x + 70, ys[3] + sp * 0.55, 120)
    cert_card(c, x + w - 330, y + 40, 320, 130, "Sertifikat", "≠ keretanya", rot=0.05)


def _pop(c, t, t0, cx, cy, draw, d=0.4):
    if t < t0:
        return
    p = out_back(prog(t, t0, d), 1.7)
    with c.at(0, 0, max(0.01, p), origin=(cx, cy)):
        with c.group(clamp(p * 2)):
            draw(c)


def _ptag(c, t, t0, x, y, label, color=None, h=40):
    color = color or C["accent"]
    w = c.measure(label, F["ui"], tk.T["tag"][0], tk.T["tag"][1])[0] + 30
    _pop(c, t, t0, x + w / 2, y + h / 2, lambda c: tag(c, x, y, label, color, h=h))
    return w + 10


def _typed_lines(c, t, x, y, lines, cps=48, size=21, lh=40):
    """Mono lines typed from their own start time: [(text, t0, color)]."""
    for i, (text, t0, col) in enumerate(lines):
        n = int(max(0.0, t - t0) * cps)
        if n <= 0:
            continue
        c.text(x, y + i * lh, text[:n], F["mono"], size, col, 1, 0.0)
        if n < len(text):
            w = c.measure(text[:n], F["mono"], size)[0]
            c.fill_rrect(x + w + 2, y + i * lh - size * 0.8, 3, size, 1, C["accent"])


# ── INTRO: ten certificates? no. → the route ───────────────────────────
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2 = T["L01"], T["L02"]
    t_sep = T.word("L01", "sepuluh")
    t_jangan = T.word("L01", "jangan")
    head1 = Headline("~Sepuluh sertifikat~. *Jangan*.")
    head2 = Headline("Mulai dari *nol*.")

    cam = v.camera
    cam.key(0.0, zoom=1.04, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "ROADMAP · DARI NOL", ORANGE)
        head1.draw(c, t, L1.start, L2.start - 0.15, strike_at=t_jangan)
        head2.draw(c, t, L2.start, e - OUT)

        def stack(c):
            for k in range(10):
                p = prog(t, t_sep - 0.2 + k * 0.07, 0.35)
                if p <= 0:
                    continue
                x, y = X + 70 + k * 12, 600 + k * 30
                rot = (0.03 if k % 2 else -0.025) + (0.06 if k == 6 else 0.0)
                sc = out_back(p, 1.6)
                with c.at(0, 0, max(0.01, sc), origin=(x + 280, y + 85)):
                    cert_card(c, x, y, 560, 170, f"Sertifikasi #{k + 1:02d}", "cloud · level ?", alpha=clamp(p * 2),
                              rot=rot)
        appear(c, t, t_sep - 0.3, t_jangan + 0.25, (X + 60, 580, 700, 480), stack, exit="down", blur=4, rise=10)
    v.add(s, e + 0.4, draw)
    for k in range(10):
        v.sfx("pop", t_sep - 0.2 + k * 0.07, 0.25)
    v.sfx("thud", t_jangan)


# ── the route (L02 → recap): the hero, changing state every chapter ────
def route(v, T, s, e, arrive):
    t_rute = T.word("L02", "rute")
    t_lima = T.word("L02", "lima")
    t_urut = T.word("L02", "urut")
    t_turun = T.word("L15", "turun")
    t_dil = T.word("L15", "dilewatin")
    t_bingung = T.word("L15", "bingung")
    L15 = T["L15"]

    def train_y(t):
        y = Y0
        for k, ta in enumerate(arrive):
            y = lerp(y, YS[k], in_out_cubic(prog(t, ta - 0.5, 0.9)))
        return y

    def draw(c, t):
        def strip(c):
            ty = train_y(t)
            lit = [prog(t, ta + 0.35, 0.3) for ta in arrive]
            dead = [0.0] + [prog(t, t_dil, 0.3) * (1 - prog(t, e - 0.8, 0.3))] * 3 + [0.0]
            active = next((k for k in range(5) if arrive[k] <= t < (arrive[k + 1] if k < 4 else e)), None)
            route_strip(c, LX, YS, t, p_draw=prog(t, t_rute - 0.2, 1.4), reach=(ty - Y0) / (Y1 - Y0), lit=lit,
                        names=NAMES, subs=SUBS, label_a=out_expo(prog(t, t_lima, 0.6)), dead=dead, active=active)
            ta = out_expo(prog(t, t_urut, 0.4))
            train(c, LX, ty, 92, alpha=ta, t=t)
            # L15: a ghost train jumps from station 1 straight to station 5
            gp = prog(t, t_turun - 0.3, 1.0)
            if 0 < gp:
                ga = clamp(gp * 4) * (1 - prog(t, e - 0.8, 0.3))
                gx, gy = bezier_point((LX, YS[0]), (LX + 300, YS[1]), (LX + 300, YS[3]), (LX, YS[4]), in_out_cubic(gp))
                if gp < 1:
                    train(c, gx, gy, 92, ghost=True, alpha=ga)
                for k in range(3):
                    qp = out_back(prog(t, t_bingung + k * 0.12, 0.4), 2.0)
                    if qp > 0:
                        c.text(LX + 60 + k * 44, YS[4] - 46 - 12 * (k % 2), "?", F["serif"], 50 * qp, ORANGE,
                               clamp(qp) * ga, align="c")
        appear(c, t, s, e - OUT, (X, Y0 - 30, 340, Y1 - Y0 + 60), strip, blur=4, rise=10)
    v.add(s, e, draw)
    v.sfx("whoosh", t_rute - 0.2, 0.5)
    for k in range(5):
        v.sfx("pop", t_rute + k * 0.25, 0.3)
    v.sfx("pop", t_urut, 0.4)
    for ta in arrive:
        v.sfx("whoosh", ta - 0.5, 0.45)
        v.sfx("chime", ta + 0.35, 0.35)
    v.sfx("whoosh", t_turun - 0.3, 0.5)
    v.sfx("thud", t_dil, 0.6)


def _focus(v, t, k, zoom=1.05):
    v.camera.focus(t, (X, YS[k] - 230, CW, 460), zoom=zoom, dur=0.8)


# ── 00 · LINUX ──────────────────────────────────────────────────────────
def linux(v, T, s, e):
    ch = v.chapter(0, "LINUX", s, e)
    L3, L5 = T["L03"], T["L05"]
    t_term = T.word("L04", "terminal")
    t_perm = T.word("L04", "permission")
    t_proc = T.word("L04", "process")
    t_berat = T.word("L05", "berat")
    head1 = Headline("Mulai dari *Linux*.")
    head2 = Headline("Ini *fondasinya*.")
    card = (DX, 560, DW, 320)
    _focus(v, L3.start - 0.5, 0)

    def draw(c, t):
        kicker(c, t, L3.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L3.start, L5.start - 0.15)
        head2.draw(c, t, L5.start, e - OUT)

        def term(c):
            x, y, w, h = card
            c.card(x, y, w, h, r=22)
            for k in range(3):
                c.circle(x + 30 + k * 22, y + 32, 6, C["faint"])
            c.text(x + w - 24, y + 39, "terminal", F["mono_med"], 18, C["muted"], 1, 0.04, align="r")
            ink, mut = C["code_txt"], C["muted"]
            _typed_lines(c, t, x + 30, y + 100, [
                ("$ ls -l", t_term, ink), ("-rwxr-x--- deploy.sh", t_term + 0.35, mut),
                ("$ chmod +x deploy.sh", t_perm, ink), ("$ ps aux | grep nginx", t_proc, ink),
                ("root  812  nginx: master", t_proc + 0.5, mut)])
        appear(c, t, L3.start + 0.2, e - OUT, card, term, enter="right", exit="left")
        fade(c, t, t_berat - 0.2, e - OUT,
             lambda c: note(c, DX, 980, "semua stasiun\nnanti lewat sini", prog(t, t_berat - 0.2, 0.8),
                            arrow_to=(LX + 36, YS[0] + 20), color=ORANGE, size=38))
    v.add(s, e, draw)
    for tt in (t_term, t_perm, t_proc):
        for k in range(6):
            v.sfx("key", tt + k / 48 * 3, 0.3)


# ── 01 · NETWORKING ─────────────────────────────────────────────────────
def networking(v, T, s, e):
    ch = v.chapter(1, "NETWORKING", s, e)
    L6, L7, L8 = T["L06"], T["L07"], T["L08"]
    t_ip = T.word("L06", "ip")
    t_dns = T.word("L06", "dns")
    t_sub = T.word("L06", "subnet")
    t_nyangkut = T.word("L07", "nyangkut")
    t_akses = T.word("L08", "diakses")
    t_sini = T.word("L08", "sini")
    heads = [(Headline("*Networking*."), L6.start, L7.start - 0.15),
             (Headline("Paling sering *nyangkut*."), L7.start, L8.start - 0.15),
             (Headline("Biasanya di *sini*."), L8.start, e - OUT)]
    card = (DX, 690, DW, 540)
    nodes = [("kamu", "app-nya mana?", L6.start + 0.2), ("DNS", "nama → alamat", t_dns),
             ("IP", "10.0.1.24", t_ip), ("subnet", "10.0.1.0/24", t_sub)]
    bx, bw, bh = DX + 36, DW - 72, 76
    by = [card[1] + 40 + k * 124 for k in range(4)]
    _focus(v, L6.start - 0.5, 1)
    v.camera.focus(t_akses - 0.2, (DX, by[1], DW, by[2] - by[1] + bh), zoom=1.08, dur=0.5)

    def draw(c, t):
        kicker(c, t, L6.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)
        brk = out_expo(prog(t, t_akses, 0.4))

        def chain(c):
            x, y, w, h = card
            c.card(x, y, w, h, r=22)
            for k in range(3):
                lp = prog(t, t_nyangkut - 0.3 + k * 0.2, 0.4)
                ya, yb = by[k] + bh, by[k + 1]
                col = RED if (k == 1 and brk > 0) else C["ink2"]
                if lp > 0:
                    c.line(bx + bw / 2, ya, bx + bw / 2, lerp(ya, yb, out_expo(lp)), col, 3)
                if k == 1 and brk > 0:
                    mx, my = bx + bw / 2, (ya + yb) / 2
                    d = 14 * brk
                    c.circle(mx, my, 22, C["card"])
                    c.line(mx - d, my - d, mx + d, my + d, RED, 5)
                    c.line(mx - d, my + d, mx + d, my - d, RED, 5)
            for k, (name, sub, t0) in enumerate(nodes):
                def node(c, k=k, name=name, sub=sub):
                    c.fill_rrect(bx, by[k], bw, bh, 16, C["bg"])
                    c.text(bx + 24, by[k] + 48, name, F["display_semi"], 32, C["ink"], 1, -0.02)
                    c.text(bx + bw - 22, by[k] + 46, sub, F["mono_med"], 18, C["muted"], 1, 0.02, align="r")
                _pop(c, t, t0, bx + bw / 2, by[k] + bh / 2, node)
            sp = out_expo(prog(t, t_sini, 0.4))
            if sp > 0:
                c.stroke_rrect(bx - 12, by[1] - 12, bw + 24, by[2] + bh - by[1] + 24, 20, RED, 4, sp)
        appear(c, t, L6.start - 0.1, e - OUT, card, chain, enter="right", exit="left")
        fade(c, t, t_nyangkut, e - OUT,
             lambda c: note(c, DX, 1300, "pemula nyangkut\ndi sini", prog(t, t_nyangkut, 0.8),
                            arrow_to=(LX + 36, YS[1] + 24), color=ORANGE, size=36))
    v.add(s, e, draw)
    for tt in (L6.start + 0.2, t_dns, t_ip, t_sub):
        v.sfx("pop", tt, 0.4)
    v.sfx("tick", t_nyangkut, 0.5)
    v.sfx("thud", t_akses, 0.7)
    v.sfx("pop", t_sini, 0.5)


# ── 02 · SATU CLOUD: the transit station — one deep, the rest easy ─────
def satu_cloud(v, T, s, e):
    ch = v.chapter(2, "SATU CLOUD", s, e)
    L9, L10, L11 = T["L09"], T["L10"], T["L11"]
    t_satu = T.word("L09", "satu")
    t_dalam = T.word("L09", "dalam")
    t_empat = T.word("L10", "empat")
    t_gampang = T.word("L11", "gampang")
    head1 = Headline("*Satu* cloud dulu.")
    head2 = Headline("Sisanya jadi *gampang*.")
    card = (DX, 800, DW, 440)
    rows = ["cloud pertama", "cloud kedua", "cloud ketiga", "cloud keempat"]
    ry = [card[1] + 40 + k * 96 for k in range(4)]
    rh = 76
    _focus(v, L9.start - 0.5, 2)
    v.camera.focus(t_dalam - 0.2, (DX, ry[0] - 20, DW, rh + 40), zoom=1.07, dur=0.5)
    v.camera.focus(t_gampang - 0.4, card, zoom=1.03, dur=0.6)

    def draw(c, t):
        kicker(c, t, L9.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L9.start, L11.start - 0.15)
        head2.draw(c, t, L11.start, e - OUT)

        def branches(c):
            for k in range(4):
                bp = prog(t, t_satu - 0.2 + k * 0.1, 0.6)
                vis = 1.0 if k == 0 else out_expo(prog(t, t_empat, 0.5))
                col = ORANGE if k == 0 else C["faint"]
                pts = [(LX + 28, YS[2] + 44), (DX - 40, YS[2] + 44), (DX - 40, ry[k] + rh / 2), (DX, ry[k] + rh / 2)]
                _draw_poly(c, pts, bp, col, 6 if k == 0 else 4, 0.25 + 0.75 * vis)
            x, y, w, h = card
            c.card(x, y, w, h, r=22)
            for k, lbl in enumerate(rows):
                vis = 1.0 if k == 0 else out_expo(prog(t, t_empat + 0.1 * k, 0.5))
                if vis <= 0:
                    continue
                with c.group(vis):
                    c.text(x + 30, ry[k] + 34, lbl, F["ui_semi"], 26, C["ink"] if k == 0 else C["ink2"], 1, -0.01)
                    bxx, bww = x + 30, w - 60
                    c.fill_rrect(bxx, ry[k] + 50, bww, 14, 7, C["faint"], 0.6)
                    if k == 0:
                        f = out_expo(prog(t, t_dalam, 1.0))
                    else:
                        f = 0.82 * out_expo(prog(t, t_gampang + 0.15 * (k - 1), 0.45))
                    if f > 0:
                        c.fill_rrect(bxx, ry[k] + 50, bww * f, 14, 7, ORANGE if k == 0 else mix_soft(ORANGE))
                    if k == 0 and f > 0.6:
                        c.text(x + w - 30, ry[k] + 34, "dalam-dalam", F["serif"], 32, ORANGE, clamp((f - 0.6) * 3),
                               align="r")
        appear(c, t, L9.start - 0.1, e - OUT, (X, 760, CW, 500), branches, enter="right", exit="left")
    v.add(s, e, draw)
    v.sfx("pop", t_satu, 0.5)
    v.sfx("tick", t_dalam, 0.5)
    for k in range(3):
        v.sfx("pop", t_empat + 0.1 * (k + 1), 0.35)
        v.sfx("tick", t_gampang + 0.15 * k, 0.4)


def mix_soft(col):
    return (*col[:3], 0.55)


# ── 03 · IAC + KUBERNETES: code, then pods — and the ghost who jumped ──
def iac_k8s(v, T, s, e):
    ch = v.chapter(3, "IAC + KUBERNETES", s, e)
    L12, L13, L14, L15 = T["L12"], T["L13"], T["L14"], T["L15"]
    t_tf = T.word("L12", "terraform")
    t_tags = [T.word("L13", "diulang"), T.word("L13", "review"), T.word("L13", "lupa")]
    t_k8s = T.word("L14", "kubernetes")
    heads = [(Headline("Infra jadi *kode*."), L12.start, L14.start - 0.15),
             (Headline("Baru *Kubernetes*."), L14.start, L15.start - 0.15),
             (Headline("Jangan *loncat*."), L15.start, e - OUT)]
    code = (DX, 960, DW, 250)
    pods = (DX, 1180, DW, 260)
    _focus(v, L12.start - 0.5, 3)
    _focus(v, L14.start - 0.5, 4)
    v.camera.reset(L15.start - 0.1, dur=0.8)

    def draw(c, t):
        kicker(c, t, L12.start - 0.2, e - OUT, ch.kicker, ch.color)
        for h, a, b in heads:
            h.draw(c, t, a, b)

        def tf(c):
            x, y, w, h = code
            c.card(x, y, w, h, r=22)
            c.text(x + 30, y + 44, "main.tf", F["mono_bold"], 18, C["muted"], 1, 0.06)
            kw, st, ink = C["code_kw"], C["code_str"], C["code_txt"]
            t0 = t_tf + 0.2
            _typed_lines(c, t, x + 30, y + 96, [
                ('resource "aws_instance" "web" {', t0, kw), ('  instance_type = "t3.small"', t0 + 0.7, st),
                ("  count         = 3", t0 + 1.3, ink), ("}", t0 + 1.7, kw)], cps=55, size=19, lh=36)
        appear(c, t, L12.start + 0.1, L14.start - 0.15, code, tf, enter="right", exit="left")
        if L13.start - 0.2 <= t:
            def tags(c):
                tx = DX
                for lbl, tt in zip(("diulang", "di-review", "nggak lupa"), t_tags):
                    tx += _ptag(c, t, tt, tx, 1236, lbl, ORANGE)
            fade(c, t, L13.start - 0.2, L14.start - 0.15, tags)

        def k8s(c):
            x, y, w, h = pods
            c.card(x, y, w, h, r=22)
            c.text(x + 30, y + 44, "cluster", F["mono_bold"], 18, C["muted"], 1, 0.06)
            pw, ph = (w - 60 - 2 * 16) / 3, 74
            for k in range(6):
                px, py = x + 30 + (k % 3) * (pw + 16), y + 70 + (k // 3) * (ph + 16)

                def pod(c, px=px, py=py):
                    c.fill_rrect(px, py, pw, ph, 14, ORANGE, 0.14)
                    c.stroke_rrect(px, py, pw, ph, 14, ORANGE, 2)
                    c.text(px + pw / 2, py + ph / 2 + 8, "pod", F["mono_bold"], 22, ORANGE, 1, 0.04, align="c")
                _pop(c, t, t_k8s + 0.1 + k * 0.08, px + pw / 2, py + ph / 2, pod)
        appear(c, t, L14.start - 0.1, e - OUT, pods, k8s, enter="right")
        fade(c, t, T.word("L15", "dilewatin"), e - OUT,
             lambda c: note(c, DX, 1000, "3 stasiun\ndilewatin", prog(t, T.word("L15", "dilewatin"), 0.8),
                            arrow_to=(LX + 60, YS[2]), color=ORANGE, size=38))
    v.add(s, e, draw)
    for k in range(4):
        v.sfx("key", t_tf + 0.2 + k * 0.5, 0.35)
    for tt in t_tags:
        v.sfx("pop", tt, 0.4)
    for k in range(6):
        v.sfx("pop", t_k8s + 0.1 + k * 0.08, 0.25)


# ── RECAP (dark): the ticket is not the train → order ──────────────────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L16, L17 = T["L16"], T["L17"]
    t_tiket = T.word("L16", "tiket")
    t_kereta = T.word("L16", "keretanya")
    head1 = Headline("Tiket, bukan *kereta*.", style="headline_dark")
    head2 = Headline("Yang penting *urutannya*.", style="headline_dark")
    cert = (X + 124, 620, 600, 220)

    cam = v.camera
    cam.focus(t_kereta, (MID - 200, 900, 400, 420), zoom=1.06, dur=0.6)
    cam.reset(L17.start - 0.1, dur=0.4)

    def draw(c, t):
        head1.draw(c, t, L16.start, L17.start - 0.15)
        head2.draw(c, t, L17.start, e - OUT)

        def ticket(c):
            cert_card(c, *cert, "Sertifikat cloud", "tiket masuk", rot=-0.03)
            tp = out_expo(prog(t, t_kereta - 0.2, 0.8))
            if tp > 0:
                train(c, lerp(MID + 700, MID, tp), 1120, 400, t=t)
        appear(c, t, t_tiket - 0.3, L17.start - 0.15, (X, 600, CW, 760), ticket, enter="up", exit="left")

        def order(c):
            lit = [prog(t, L17.start + 0.3 + k * 0.3, 0.3) for k in range(5)]
            station_dots(c, X + 60, X + CW - 60, 1000, 5, lit)
            for k, n in enumerate(NAMES):
                px = X + 60 + (CW - 120) * k / 4
                c.text(px, 940, n, F["mono_med"], 17, C["d_muted"], out_expo(lit[k]), 0.02, align="c")
        appear(c, t, L17.start - 0.1, e - OUT, (X, 900, CW, 180), order, enter="right")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("pop", t_tiket, 0.5)
    v.sfx("whoosh", t_kereta - 0.2, 0.6)
    v.sfx("whoosh", L17.start - 0.1, 0.4)
    for k in range(5):
        v.sfx("pop", L17.start + 0.3 + k * 0.3, 0.3)
    v.sfx("chime", L17.start + 1.6, 0.6)


# ── OUTRO: save + next video (QRIS) + follow ───────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L18, L19, L20 = T["L18"], T["L19"], T["L20"]
    t_save = T.word("L18", "save") + 0.3
    t_click = T.word("L20", "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, ORANGE)
            c.text(X + 50, 892, "VIDEO BERIKUTNYA", F["mono_bold"], 20, ORANGE, 1, 0.16)
            c.text(X + 50, 962, "QRIS: 2 detik", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "setelah kamu scan.", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L19.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L18.start, None, lambda c: save_button(c, MID, 1090, t, t_save))
        fade(c, t, L20.start, None, lambda c: follow_button(c, MID, 1190, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1330, "mumeyong.dev", F["mono_med"], 28,
                                                          C["d_muted"], 1, 0.06, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L18.start - 0.2, 860, 1450), (t_save, MID + 40, 1126), (L20.start, MID + 70, 1300),
                    (t_click, MID + 40, 1226)], clicks=[t_save, t_click], hide=t_click + 1.0))
    v.sfx("click", t_save, 0.7)
    v.sfx("chime", t_save + 0.1, 0.6)
    v.sfx("pop", L19.start, 0.5)
    v.sfx("chime", t_click + 0.1)
