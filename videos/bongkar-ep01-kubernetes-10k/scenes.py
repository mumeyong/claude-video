"""Bongkar Arsitektur EP01 — Kubernetes yang nahan 10.000 request barengan. See IDENTITY.md / TREATMENT.md.

Metaphor: toll gates at mudik (request = car, pod = booth, Kubernetes = toll officer).
Signature move: a booth/pod SPLITS in two when the queue rises and CLOSES when it's quiet. Signature color: purple.
All times come from timing.json (T). No chat input, no chip row.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, in_cubic, clamp, lerp
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, word_pill, note,
                               follow_button, fmt_id, particle_flow, toll_plaza, booth, arch_diagram,
                               load_graph, stack_layers, slab_y, PURPLE)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
SERIES = "BONGKAR ARSITEKTUR · EP 01"
CH = ["00 · MASALAH", "01 · KEPUTUSAN", "02 · DIAGRAM", "03 · HASIL", "RECAP", "OUTRO"]


def build(project):
    T = project.timing
    v = Video(duration=T["L26"].end + TAIL, bpm=128, beat_offset=0.0, series=SERIES)
    v.cover_t = T["L02"].end
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    b["00 · MASALAH"] = T["L04"].end + 0.1           # chapter (and bumper) starts right after L04
    intro(v, T, 0.0, b["00 · MASALAH"])
    masalah(v, T, b["00 · MASALAH"], b["01 · KEPUTUSAN"])
    keputusan(v, T, b["01 · KEPUTUSAN"], b["02 · DIAGRAM"])
    diagram(v, T, b["02 · DIAGRAM"], b["03 · HASIL"])
    hasil(v, T, b["03 · HASIL"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


# ── INTRO: particle flood → crash → bumper ─────────────────────────────
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L4, L5 = T["L01"], T["L02"], T["L04"], T["L05"]
    t_10k = T.word("L02", "sepuluh")
    t_fin = T.word("L03", "keuangan")
    t_slow, t_down = T.word("L04", "lemot"), T.word("L04", "down")
    target = (MID, 980)
    head1 = Headline("*10.000+* barengan.")
    head2 = Headline("Lemot. Lalu *down*.")
    bump0, bump1 = e, max(e + 1.4, L5.start - 0.05)  # bumper window (z=100, over the chapter change)

    cam = v.camera
    cam.key(0.0, zoom=1.15, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=L2.end - L1.start, ease=out_cubic)
    cam.key(t_down, zoom=1.08, y=target[1], dur=0.25, ease=out_expo)  # punch on "tumbang"
    cam.reset(e, dur=0.4)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "PEAK HOUR · TIAP HARI", C["accent"])
        head1.draw(c, t, L2.start, L4.start - 0.15)
        head2.draw(c, t, L4.start, e - OUT)
        dens = out_cubic(prog(t, L1.start - 0.2, max(0.5, t_10k - L1.start + 0.6)))
        jam = in_out_cubic(prog(t, t_slow, 1.2))
        red = in_out_cubic(prog(t, t_down, 0.4))
        fade_out = 1 - prog(t, e - 0.2, 0.4)
        with c.group(fade_out):
            particle_flow(c, t, target, n=420, density=dens, jam=jam, red=red, speed=0.32)
            # the app the requests hit
            r = 46 + 8 * math.sin(t * 6) * (1 - jam)
            c.circle(target[0], target[1], r + 16, lerp_col(PURPLE, C["rec"], red), 0.18)
            c.circle(target[0], target[1], r, lerp_col(PURPLE, C["rec"], red))
            c.text(target[0], target[1] + 9, "app", F["mono_bold"], 24, (1, 1, 1, 1), 1, 0.06, align="c")
            cnt = 10000 * out_cubic(prog(t, t_10k - 0.3, 1.2))
            fade(c, t, t_10k - 0.3, None, lambda c: c.text(
                target[0], target[1] + 130, f"{fmt_id(int(cnt))}+ request barengan", F["mono_med"], 28,
                c.theme("ink2", "d_muted"), 1, 0.04, align="c"))
            fade(c, t, t_fin, None, lambda c: tag(c, target[0] - 110, target[1] + 160, "layanan keuangan", h=42))
            if t >= t_down:
                p = prog(t, t_down, 0.35)
                with c.at(0, 0, 1 + 0.6 * (1 - out_expo(p)), origin=target, rot=-0.06):
                    word_pill(c, target[0] - 150, target[1] - 260, "503", C["rec"], size=120, alpha=clamp(p * 3))
                fade(c, t, t_down + 0.25, None, lambda c: c.text(
                    target[0], target[1] - 290, "SERVICE UNAVAILABLE", F["mono_bold"], 22, C["rec"], 1, 0.16,
                    align="c"))
    v.add(s, e + 0.4, draw)

    def bumper(c, t):  # purple full-bleed panel wipes up, holds, wipes out
        pin = out_expo(prog(t, bump0, 0.4))
        pout = in_cubic(prog(t, bump1 - 0.35, 0.35))
        top = tk.H * (1 - pin) - tk.H * pout
        c.src(PURPLE)
        c.ctx.rectangle(0, top, tk.W, tk.H)
        c.ctx.fill()
        a = out_expo(prog(t, bump0 + 0.15, 0.4)) * (1 - pout)
        with c.layer((0, 0, tk.W, tk.H), a, 10 * (1 - out_expo(prog(t, bump0 + 0.15, 0.4)))):
            c.text(X, 760, "BONGKAR", F["display"], 150, (1, 1, 1, 1), 1, -0.06)
            c.text(X, 900, "ARSITEKTUR", F["display"], 150, (1, 1, 1, 1), 1, -0.06)
            c.text(X, 1010, "EP 01", F["mono_bold"], 40, (1, 1, 1, 1), 0.85, 0.2)
            c.text(X, 1090, "Layanan keuangan · Kubernetes · Alibaba Cloud", F["ui"], 34, (1, 1, 1, 1), 0.8, -0.01)
    v.add(bump0, bump1, bumper, z=100)

    v.sfx("whoosh", L1.start, 0.5)
    v.sfx("thud", t_10k)
    v.sfx("pop", t_fin, 0.4)
    v.sfx("thud", t_down)
    v.sfx("whoosh", bump0, 0.8)
    v.sfx("whoosh", bump1 - 0.35, 0.5)


def lerp_col(a, b, p):
    return tuple(x + (y - x) * p for x, y in zip(a, b))


# ── 00 · MASALAH: toll plaza jam ───────────────────────────────────────
def masalah(v, T, s, e):
    ch = v.chapter(0, "MASALAH", s, e)
    L5, L8 = T["L05"], T["L08"]
    t_q = T.word("L06", "segitu")
    t_u = T.word("L07", "putar")
    t_g = T.word("L08", "gagal")
    head1 = Headline("Bayangin *gerbang tol*.")
    head2 = Headline("Transaksi *gagal*.")
    py, ph = 560, 820

    cam = v.camera
    cam.focus(t_q, (X, py + 60, CW, 420), zoom=1.07, dur=1.5)
    cam.reset(L8.start, dur=0.6)

    def draw(c, t):
        kicker(c, t, L5.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L5.start, L8.start - 0.15)
        head2.draw(c, t, L8.start, e - OUT)
        q = in_out_cubic(prog(t, t_q, 2.2))
        flow = 0.6 + 0.8 * q

        def plaza(c):
            toll_plaza(c, X, py, CW, ph, t, [(0.25, 1, "ok"), (0.5, 1, "ok"), (0.75, 1, "ok")],
                       flow=flow, queue=0.15 + 0.6 * q, uturns=prog(t, t_u, 1.6), uturn_n=3)
            gp = out_expo(prog(t, t_g, 0.4))
            if gp > 0:
                for k in range(3):
                    tag(c, X + 40 + k * 270, py + 40 + (k % 2) * 30, "FAILED", C["rec"],
                        clamp(gp * 3 - k * 0.6), h=40)
        appear(c, t, L5.start, e - OUT, (X, py, CW, ph), plaza, enter="right")
    v.add(s, e, draw)
    v.sfx("whoosh", L5.start, 0.6)
    for k in range(4):
        v.sfx("tick", t_q + k * 0.3, 0.3)
    for k in range(3):
        v.sfx("pop", t_u + k * 0.18, 0.4)
    v.sfx("thud", t_g, 0.7)


# ── 01 · KEPUTUSAN: idle grid → split → stacked slabs ──────────────────
def keputusan(v, T, s, e):
    ch = v.chapter(1, "KEPUTUSAN", s, e)
    L9, L11, L12 = T["L09"], T["L11"], T["L12"]
    t_idle = T.word("L10", "idle")
    t_self = T.word("L11", "sendiri")
    t_layers = [T.word("L12", "container"), T.word("L12", "kubernetes"), T.word("L12", "alibaba")]
    t_pet = T.word("L13", "petugas")
    head1 = Headline("~Gardu sebanyak-banyaknya~?")
    head2 = Headline("Gardu yang *nambah sendiri*.")
    gy, gh = 560, 640
    sx, sy_bot, sw = X + 30, 1360, CW - 60

    cam = v.camera
    cam.key(T["L10"].start, zoom=1.05, y=gy + gh / 2, dur=1.6)
    cam.reset(L11.start, dur=0.5)
    cam.key(t_layers[0] - 0.2, zoom=1.04, y=1000, dur=0.6)
    cam.reset(t_layers[2] + 0.4, dur=1.0)

    def draw(c, t):
        kicker(c, t, L9.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L9.start, L11.start - 0.15, strike_at=t_idle + 0.3)
        head2.draw(c, t, L11.start, e - OUT)

        def grid(c):
            night = in_out_cubic(prog(t, T["L10"].start, 0.8))
            booths = [((k + 0.5) / 12, 1, "idle" if night > 0.5 else "ok") for k in range(12)]
            toll_plaza(c, X, gy, CW, gh, t, booths, flow=1 - night, queue=0, booth_line=0.55)
            if night > 0:
                c.fill_rrect(X, gy, CW, gh, 30, (0.05, 0.06, 0.12, 1), 0.35 * night)
                from engine.components import moon
                moon(c, X + CW - 90, gy + 80, 26, night)
                tag(c, X + 30, gy + gh - 70, "mahal · idle tiap malam", C["rec"], night, h=44)
        appear(c, t, L9.start, L11.start - 0.15, (X, gy, CW, gh), grid, exit="down")

        def split(c):
            p = in_out_cubic(prog(t, t_self, 0.6))
            for side in (-1, 1):
                bx = MID + side * 130 * p
                booth(c, bx, 860, 170, 110, 1.0 if side < 0 or p > 0.05 else 0.0)
            note(c, MID + 210, 1040, "auto-scaling", prog(t, t_self + 0.3, 0.8), arrow_to=(MID + 150, 920),
                 size=38)
        appear(c, t, L11.start - 0.05, t_layers[0] - 0.25, (X, 700, CW, 360), split, enter="pop", exit="up")

        def stack(c):
            # bottom → top: Alibaba Cloud, Kubernetes, container — each drops when its word is spoken
            layers = [("Alibaba Cloud", "infra", tk.CHAPTER[0][0], prog(t, t_layers[2], 0.55)),
                      ("Kubernetes", "petugas tol", PURPLE, prog(t, t_layers[1], 0.55)),
                      ("container", "app", tk.CHAPTER[4][0], prog(t, t_layers[0], 0.55))]
            stack_layers(c, sx, sy_bot, sw, layers, ghost=out_expo(prog(t, t_layers[0] - 0.3, 0.3)))
            bp = out_back(prog(t, t_pet, 0.45)) if t >= t_pet else 0.0
            if bp > 0:
                ky = slab_y(sy_bot, 1)
                with c.at(0, 0, max(0.01, bp), origin=(sx + sw - 40, ky)):
                    c.circle(sx + sw - 40, ky, 44, PURPLE)
                    icons.check(c, sx + sw - 40, ky, 34, (1, 1, 1, 1), 5)
            note(c, sx + 10, slab_y(sy_bot, 2) - 60, "Kubernetes = petugas tol-nya", prog(t, t_pet + 0.2, 0.8),
                 size=36)
        appear(c, t, t_layers[0] - 0.3, e - OUT, (sx, sy_bot - 520, sw, 520), stack, blur=4, rise=0)
    v.add(s, e, draw)
    v.sfx("pop", L9.start, 0.5)
    v.sfx("tick", t_idle, 0.5)
    v.sfx("pop", t_self)
    for tt in t_layers:
        v.sfx("thud", tt + 0.3, 0.6)
    v.sfx("pop", t_pet)


# ── 02 · DIAGRAM: arch diagram with splitting pods ──────────────────────
def diagram(v, T, s, e):
    ch = v.chapter(2, "DIAGRAM", s, e)
    L14, L15, L17 = T["L14"], T["L15"], T["L17"]
    t_lb = T.word("L14", "load")
    t_split = T.word("L15", "nambah")
    t_node = T.word("L16", "ditambah")
    t_dead, t_new = T.word("L17", "crash"), T.word("L17", "diganti")
    head1 = Headline("Dibagi *rata*.")
    head2 = Headline("Traffic naik? *Scale up*.")
    head3 = Headline("Pod crash? *Diganti*.")
    nw, nh = 410, 380
    n1 = (X, 940)
    n2 = (X + CW - nw, 940)
    pw_, ph_ = 160, 110

    def slot(node, k):
        nx, ny = node
        return nx + 30 + (k % 2) * (pw_ + 30), ny + 80 + (k // 2) * (ph_ + 30)

    cam = v.camera
    cam.focus(t_lb, (X, 560, CW, 320), zoom=1.05, dur=0.8)
    cam.focus(t_split, (X, 900, nw, nh), zoom=1.08, dur=0.8)
    cam.focus(t_node, (X + CW - nw, 900, nw, nh), zoom=1.06, dur=0.9)
    cam.focus(t_dead, (X, 900, nw, nh), zoom=1.1, dur=0.6)
    cam.reset(e - 0.8, dur=0.6)

    def draw(c, t):
        kicker(c, t, L14.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L14.start, L15.start - 0.15)
        head2.draw(c, t, L15.start, L17.start - 0.15)
        head3.draw(c, t, L17.start, e - OUT)

        def dia(c):
            a_users = out_expo(prog(t, L14.start, 0.4))
            a_lb = out_expo(prog(t, t_lb, 0.4))
            a_n1 = out_expo(prog(t, t_lb + 0.3, 0.4))
            n2p = out_expo(prog(t, t_node, 0.6))
            nodes = {
                "users": dict(x=MID - 190, y=560, w=380, h=110, kind="users", label="users", a=a_users),
                "lb": dict(x=MID - 190, y=740, w=380, h=100, kind="lb", label="load balancer", a=a_lb),
                "n1": dict(x=n1[0], y=n1[1], w=nw, h=nh, kind="node", label="node 1", a=a_n1),
                "n2": dict(x=n2[0] + 120 * (1 - n2p), y=n2[1], w=nw, h=nh, kind="node", label="node 2", a=n2p),
            }
            # pods: (id, node, slot, parent (node, slot) it splits from, t_born)
            pods = [("p0", n1, 0, None, t_lb + 0.5), ("p1", n1, 1, None, t_lb + 0.6),
                    ("p2", n1, 2, (n1, 0), t_split), ("p3", n1, 3, (n1, 1), t_split + 0.12),
                    ("p4", n2, 0, (n1, 2), t_node + 0.4), ("p5", n2, 1, (n1, 3), t_node + 0.52)]
            edges = [("users", "lb", out_expo(prog(t, t_lb, 0.5)), 1.0)]
            for pid, node, k, parent, tb in pods:
                p = prog(t, tb, 0.55)
                if p <= 0:
                    continue
                tx, ty = slot(node, k)
                if node is n2:
                    tx += 120 * (1 - n2p)
                if parent:
                    fx, fy = slot(*parent)
                    sp = out_back(p, 1.4)
                    x_, y_ = lerp(fx, tx, sp), lerp(fy, ty, sp)
                else:
                    x_, y_ = tx, ty
                state, a = "ok", clamp(p * 3)
                if pid == "p1":  # the pod that breaks and gets replaced
                    if t >= t_dead:
                        state = "dead"
                        a *= 1 - prog(t, t_dead + 0.5, 0.4)
                nodes[pid] = dict(x=x_, y=y_, w=pw_, h=ph_, kind="pod", label="pod", a=a, state=state)
                edges.append(("lb", pid, prog(t, tb, 0.4), 0.0 if state == "dead" else 1.0))
            if t >= t_new:  # replacement pod pops into p1's slot
                p = prog(t, t_new, 0.45)
                x_, y_ = slot(n1, 1)
                nodes["p1b"] = dict(x=x_, y=y_, w=pw_, h=ph_, kind="pod", label="pod", a=clamp(p * 3),
                                    s=out_back(p, 1.8) if p < 1 else 1.0)
                edges.append(("lb", "p1b", prog(t, t_new + 0.2, 0.4), 1.0))
            arch_diagram(c, t, nodes, edges, speed=0.55)
        appear(c, t, L14.start - 0.1, e - OUT, (X, 560, CW, 760), dia, blur=4, rise=20)
        note(c, X + CW - 30, 1395, "auto-scaling", prog(t, t_split + 0.4, 0.8), arrow_to=(X + 380, 1260), align="r",
             size=40)
    v.add(s, e, draw)
    v.sfx("pop", L14.start, 0.4)
    v.sfx("pop", t_lb, 0.5)
    v.sfx("pop", t_split, 0.6)
    v.sfx("pop", t_split + 0.12, 0.5)
    v.sfx("whoosh", t_node, 0.6)
    v.sfx("thud", t_dead, 0.6)
    v.sfx("pop", t_new, 0.6)


# ── 03 · HASIL: 24h load graph + closing booths ────────────────────────
def traffic(f):
    """Illustrative daily curve, x from 06:00 → 06:00 (no real data — shape only)."""
    day = 0.15 + 0.75 * math.exp(-((f - 0.22) / 0.13) ** 2) + 0.35 * math.exp(-((f - 0.55) / 0.12) ** 2)
    return clamp(day, 0.05, 0.95) * (1 - 0.6 * clamp((f - 0.7) / 0.12)) + 0.04  # quiet after midnight


def capacity(f):
    return min(1.0, math.ceil(traffic(f) * 8) / 8 + 0.06)


def hasil(v, T, s, e):
    ch = v.chapter(3, "HASIL", s, e)
    L18, L20, L21 = T["L18"], T["L20"], T["L21"]
    t_aman = T.word("L19", "aman")
    t_close = T.word("L20", "scale")
    head1 = Headline("Peak hour, *aman*.")
    head2 = Headline("Bayar pas *rame*.")
    gy, gh = 560, 560
    strip_y = 1240
    f_night = 20 / 24  # 02:00 on a 06:00-start axis

    cam = v.camera
    cam.key(L18.start + 0.2, zoom=1.04, x=X + CW * 0.35, y=gy + gh / 2, dur=1.2)
    cam.key(T["L20"].start, zoom=1.05, x=X + CW * 0.75, y=900, dur=1.4)
    cam.reset(L21.end, dur=0.8)

    def cursor_at(t):
        f = lerp(0.0, 0.42, in_out_cubic(prog(t, L18.start, max(0.6, t_aman - L18.start))))
        return lerp(f, f_night, in_out_cubic(prog(t, t_close - 0.3, 1.6)))

    def draw(c, t):
        kicker(c, t, L18.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L18.start, L21.start - 0.15)
        head2.draw(c, t, L21.start, e - OUT)
        cur = cursor_at(t)
        hh = int(6 + cur * 24) % 24
        appear(c, t, L18.start - 0.1, e - OUT, (X, gy, CW, gh),
               lambda c: load_graph(c, X, gy, CW, gh, traffic, capacity, draw=max(cur, 0.02), cursor=cur,
                                    cursor_label=f"{hh:02d}:00", peak_label="10.000+ · aman",
                                    peak_p=out_expo(prog(t, t_aman, 0.4))))

        def strip(c):
            c.card(X, strip_y, CW, 150, r=24)
            c.text(X + 30, strip_y + 40, "PODS", F["mono_med"], 18, c.theme("muted", "d_muted"), 1, 0.16)
            open_n = capacity(cur) * 8
            for k in range(8):
                op = clamp(open_n - k)
                booth(c, X + 90 + k * 95, strip_y + 95, 64, 44, 1.0, state="ok" if op > 0.5 else "idle")
        appear(c, t, L18.start + 0.3, e - OUT, (X, strip_y, CW, 150), strip, enter="up")
        note(c, X + CW - 20, gy - 20, "bayar cuma segini — pay-per-use", prog(t, L21.start + 0.2, 0.8),
             arrow_to=(X + 40 + (CW - 80) * f_night, gy + 80 + (gh - 150) * (1 - capacity(f_night)) + 20),
             align="r", size=38)
    v.add(s, e, draw)
    v.sfx("whoosh", L18.start, 0.5)
    v.sfx("chime", t_aman)
    for k in range(5):
        v.sfx("tick", t_close + k * 0.28, 0.4)
    v.sfx("pop", L21.start + 0.2, 0.4)


# ── RECAP (dark): fixed vs breathing booths → opinion slam ─────────────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L22, L23, L24 = T["L22"], T["L23"], T["L24"]
    t_butuh = T.word("L24", "butuh")
    head1 = Headline("Jangan sizing buat *peak*.", style="headline_dark")
    head2 = Headline("Bukan *gaya-gayaan*.", style="headline_dark")
    cy, chh, cw2 = 620, 620, (CW - 24) / 2

    cam = v.camera
    cam.key(t_butuh, zoom=1.1, y=1050, dur=0.01)
    cam.key(t_butuh + 0.02, zoom=1.0, dur=0.7, ease=out_cubic)

    def draw(c, t):
        head1.draw(c, t, L22.start, L24.start - 0.15)
        head2.draw(c, t, L24.start, e - OUT)

        def side(c, x, title, sub, breathing, struck):
            c.card(x, cy, cw2, chh, r=26)
            c.text(x + 30, cy + 56, title, F["mono_bold"], 20, C["d_muted"], 1, 0.16)
            for k in range(6):
                r_, k_ = divmod(k, 2)
                bx, by = x + cw2 * (0.3 + 0.4 * k_), cy + 170 + r_ * 130
                if breathing:
                    open_n = 2 + 4 * (0.5 + 0.5 * math.sin((t - L23.start) * 2.4))
                    st = "ok" if open_n > k else "idle"
                else:
                    st = "ok"
                booth(c, bx, by, 90, 56, 1.0, state=st)
            c.text(x + 30, cy + chh - 40, sub, F["ui_semi"], 28, C["d_ink"], 1, -0.02)
            if struck > 0:
                c.line(x + 20, cy + chh / 2, x + 20 + (cw2 - 40) * out_expo(struck), cy + chh / 2, C["rec"], 6)
        appear(c, t, L22.start + 0.1, L24.start - 0.15,
               (X, cy, cw2, chh), lambda c: side(c, X, "SIZED FOR PEAK", "mahal tiap hari", False,
                                                 prog(t, T.word("L22", "rame"), 0.5)), exit="left")
        appear(c, t, L22.start + 0.25, L24.start - 0.15,
               (X + cw2 + 24, cy, cw2, chh), lambda c: side(c, X + cw2 + 24, "AUTO-SCALING", "scale up & down sendiri",
                                                            t >= L23.start, 0), exit="right")
        if t >= t_butuh - 0.05:
            p = prog(t, t_butuh, 0.3)
            with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, 1050)):
                c.text(MID, 1100, "Emang butuh.", F["display"], 150, C["d_ink"], clamp(p * 3), -0.06, align="c")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("pop", T.word("L22", "rame"), 0.5)
    for k in range(4):
        v.sfx("tick", L23.start + 0.3 + k * 0.65, 0.35)
    v.sfx("thud", t_butuh)


# ── OUTRO: logo + EP02 teaser + follow ─────────────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L25, L26 = T["L25"], T["L26"]
    t_click = T.word("L26", "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, PURPLE)
            c.text(X + 50, 892, "EPISODE BERIKUTNYA · EP 02", F["mono_bold"], 20, PURPLE, 1, 0.16)
            c.text(X + 50, 962, "Big data migration ke cloud", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "zero data loss", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L25.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L26.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "Seri Bongkar Arsitektur", F["ui"], 28,
                                                          C["d_muted"], 1, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L26.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L25.start, 0.5)
    v.sfx("chime", t_click + 0.1)
