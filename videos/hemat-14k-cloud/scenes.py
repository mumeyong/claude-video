"""Gimana aku hemat $14.000/bulan biaya cloud — v2 (see TREATMENT.md).

v2: every chapter has its own composition + hero object, a camera move, and its own transition.
  INTRO       giant odometer number (centered, camera pull-out) → stamp → leaking chart → 2×2 lever tiles
  BOCOR       big terminal, flagged rows pop out as tilted leak cards → whip → 24h clock ring
  UKURAN      typographic battle 10% vs 100% (camera punch) → bus, cursor drag-resizes it
  LANGGANAN   receipt printing line by line + hand notes + HEMAT stamp (camera follows the paper)
  ARSITEKTUR  monolith shatters, pieces tumble into the serverless zone, glow when used
  RECAP       full-width staircase chart, a ball rolls down per lever → bookend odometer
All times come from timing.json (T). Layers with z >= 80 ignore the camera (chips row).
"""
from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp, lerp
from engine.components import (Headline, kicker, appear, fade, Cursor, window, chip, tag, icons, select_box,
                               follow_button, contact_pill, type_cues, cost_chart, seat_grid, day_timeline,
                               block_split, odometer, clock24, receipt, stamp, note, chart_point)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CHIPS_Y = 1490
LEVERS = ["Bocor", "Right-sizing", "Reserved & spot", "Arsitektur"]
CHAPTERS = ["00 · BOCOR", "01 · RIGHT-SIZING", "02 · RESERVED & SPOT", "03 · ARSITEKTUR"]


def build(project):
    T = project.timing
    v = Video(duration=T["L32"].end + TAIL, bpm=128, beat_offset=0.0)
    v.cover_t = T["L02"].end + 0.3
    v.music = dict(key="C", mood="bright")           # generated score: money saved, upbeat
    b = {name: T.chapter_span(name)[0] - LEAD for name in CHAPTERS + ["RECAP", "OUTRO"]}
    intro(v, T, 0.0, b["00 · BOCOR"])
    bocor(v, T, b["00 · BOCOR"], b["01 · RIGHT-SIZING"])
    ukuran(v, T, b["01 · RIGHT-SIZING"], b["02 · RESERVED & SPOT"])
    langganan(v, T, b["02 · RESERVED & SPOT"], b["03 · ARSITEKTUR"])
    arsitektur(v, T, b["03 · ARSITEKTUR"], b["RECAP"])
    lever_map(v, T, [b[c] for c in CHAPTERS], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


def count_ticks(v, t0, dur, step=0.07, gain=0.22):
    for k in range(int(dur / step)):
        v.sfx("tick", t0 + k * step, gain)


# ── sticky 4-lever chip map (screen-fixed, z=90) ────────────────────────
def lever_map(v, T, starts, end):
    t_in = starts[0] - 0.1

    def draw(c, t):
        def row(c):
            x = X
            active = max((i for i, s in enumerate(starts) if t >= s), default=0)
            for i, name in enumerate(LEVERS):
                p = out_expo(prog(t, t_in + i * 0.08, 0.45))
                if p <= 0.002:
                    continue
                on = active == i
                w = chip(c, x, CHIPS_Y + 14 * (1 - p), f"{i + 1} · {name}",
                         tk.CHAPTER[i][0] if on else C["faint"], p * (1.0 if on else 0.5))
                x += w + 12
        fade(c, t, t_in, end - OUT, row)
    v.add(t_in, end, draw, z=90)


# ── INTRO ───────────────────────────────────────────────────────────────
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L4, L5 = T["L01"], T["L02"], T["L04"], T["L05"]
    t_count = L1.start + 0.05
    d_count = max(0.9, T.word("L01", "dolar", edge="end") - t_count + 0.2)
    t_rp = T.word("L03", "dua")
    t_bocor = T.word("L04", "bocor")
    t_four = T.word("L05", "empat")
    head1 = Headline("Dipotong. *Tiap bulan*.")
    head2 = Headline("Bukan ~mahal~. *Bocor*.")
    num_y = 1000

    cam = v.camera
    cam.key(0.0, zoom=1.22, y=num_y - 80, dur=0.01)
    cam.key(t_count, zoom=1.0, dur=d_count + 0.8, ease=out_cubic)
    cam.key(L4.start + 0.2, zoom=1.04, y=900, dur=2.5)
    cam.reset(L5.start, dur=0.6)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "FINOPS · ALIBABA CLOUD", C["accent"])
        head1.draw(c, t, T.word("L02", "tiap") - 0.1, L4.start - 0.15)
        head2.draw(c, t, L4.start, L5.start - 0.1, strike_at=t_bocor)

        def number(c):
            odometer(c, MID, num_y, "$14.000", prog(t, t_count, d_count), 210, c.theme("ink", "d_ink"),
                     align="c")
            c.text(MID, num_y + 78, "/ bulan", F["ui"], 44, c.theme("muted", "d_muted"),
                   out_expo(prog(t, T.word("L02", "bulan"), 0.4)), -0.01, align="c")
            stamp(c, MID + 150, num_y + 230, "≈ Rp 200+ juta", prog(t, t_rp, 0.35), size=58, rot=-0.1)
        appear(c, t, L1.start, L4.start - 0.15, (X, num_y - 220, CW, 520), number, exit="down", blur=6)

        ch_y, ch_h = 560, 720
        appear(c, t, L4.start + 0.1, L5.start - 0.1, (X, ch_y, CW, ch_h),
               lambda c: cost_chart(c, X, ch_y, CW, ch_h, t, draw=in_out_cubic(prog(t, L4.start + 0.15, 1.1)),
                                    leak=out_expo(prog(t, t_bocor, 0.5)), drip=13),
               exit="left")

        # 2×2 lever tiles (whip in from the right), drop toward the chip row at chapter end
        tw, th, gap = (CW - 24) / 2, 300, 24
        for i, name in enumerate(LEVERS):
            r_, k_ = divmod(i, 2)
            tx, ty = X + k_ * (tw + gap), 560 + r_ * (th + gap)

            def tile(c, i=i, name=name, tx=tx, ty=ty):
                c.card(tx, ty, tw, th, r=28)
                c.text(tx + 36, ty + 150, str(i + 1), F["display"], 150, tk.CHAPTER[i][0], 1, -0.05)
                c.text(tx + 36, ty + 240, name, F["display_semi"], 48, c.theme("ink", "d_ink"), 1, -0.03)
            appear(c, t, t_four + i * 0.09, e - OUT, (tx, ty, tw, th), tile, enter="right", exit="down")
        fade(c, t, T.word("L05", "alibaba"), e - OUT,
             lambda c: tag(c, X, 560 + 2 * th + gap + 40, "Alibaba Cloud", h=42))
    v.add(s, e, draw)
    count_ticks(v, t_count, d_count)
    v.sfx("thud", t_count + d_count)
    v.sfx("whoosh", T.word("L02", "tiap") - 0.1, 0.6)
    v.sfx("thud", t_rp, 0.7)
    v.sfx("pop", t_bocor)
    v.sfx("whoosh", L5.start - 0.1, 0.6)
    for i in range(4):
        v.sfx("pop", t_four + i * 0.09, 0.45)


# ── 00 · BOCOR ──────────────────────────────────────────────────────────
TERM_ROWS = [  # name, status, flag (None = healthy), anchor (line, word)
    ("ecs-api-prod", "CPU 61% · RUNNING", None, None),
    ("ecs-web-old", "CPU 0% · RUNNING", "idle", ("L07", "pakai")),
    ("rds-main", "CPU 44% · RUNNING", None, None),
    ("disk-7f3a", "500 GB · UNATTACHED", "unattached", ("L08", "disk")),
    ("snap-2023-*", "×148 · 3 tahun", "stale", ("L09", "snapshot")),
]


def bocor(v, T, s, e):
    ch = v.chapter(0, "BOCOR", s, e)
    L6, L10, L11 = T["L06"], T["L10"], T["L11"]
    head1 = Headline("Cari yang *bocor*.")
    head2 = Headline("Nyala jam _dua_ pagi?")
    cmd = "./audit-biaya.sh --region jakarta"
    t_cmd = L6.start + 0.4
    t_rows = t_cmd + len(cmd) / 40 + 0.2
    anchors = [T.word(*a) if a else None for (_, _, _, a) in TERM_ROWS]
    flagged = [(i, a) for i, a in enumerate(anchors) if a is not None]
    t_auto = T.word("L11", "shutdown")
    t_beres = T.word("L11", "beres")
    night = list(range(18, 24)) + list(range(0, 8))
    ty, th = 540, 560
    row_y = lambda i: ty + 66 + 18 + 96 + i * 70  # noqa: E731  (baseline of row i inside the terminal)
    clock_c = (MID, 1010)

    cam = v.camera
    cam.focus(flagged[0][1] - 0.2, (X, ty + 120, CW, 360), zoom=1.07, dur=1.2)
    cam.reset(L10.start - 0.2, dur=0.5)
    cam.key(L10.start + 0.3, zoom=1.06, x=clock_c[0], y=clock_c[1] - 40, dur=3.0)
    cam.reset(L11.end, dur=0.8)

    def dev(t):
        def st(hr):
            if hr in night:
                return 1 - in_out_cubic(prog(t, t_auto + night.index(hr) * 0.05, 0.25))
            return 1.0
        return st

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L6.start, L10.start - 0.15)
        head2.draw(c, t, L10.start, e - OUT)

        def term(c):
            bx, by = window.frame(c, X, ty, CW, th, "Terminal", "aliyun cli")
            window.terminal_line(c, bx, by + 34, cmd, t, t_cmd, cps=40, caret=t < t_rows)
            first = flagged[0][1]
            for i, (name, status, flag, _a) in enumerate(TERM_ROWS):
                a = out_expo(prog(t, t_rows + i * 0.08, 0.3))
                if a <= 0.002:
                    continue
                ry = row_y(i)
                popped = flag and t >= anchors[i]
                dim = 1 - 0.65 * in_out_cubic(prog(t, first, 0.4)) if not flag else (0.3 if popped else 1.0)
                c.text(bx, ry, name, F["mono_med"], 25, c.theme("ink", "d_ink"), a * dim)
                c.text(bx + 280, ry, status, F["mono"], 23, c.theme("muted", "d_muted"), a * dim)
                if popped:
                    c.line(bx, ry - 9, bx + CW - 64, ry - 9, C["rec"], 3, 0.6 * out_expo(prog(t, anchors[i], 0.3)))
        appear(c, t, L6.start + 0.05, L10.start - 0.15, (X, ty, CW, th), term, exit="left")

        # flagged rows pop out as tilted leak cards, stacking under the terminal
        for k, (i, anc) in enumerate(flagged):
            name, status, flag, _ = TERM_ROWS[i]
            cw_, chh = 470, 150
            cx_, cy_ = X + 40 + k * 170, ty + th + 40 + k * 18
            rot = (-0.05, 0.035, -0.02)[k]

            def leak_card(c, name=name, status=status, flag=flag, cx_=cx_, cy_=cy_):
                c.card(cx_, cy_, cw_, chh, r=22)
                c.circle(cx_ + 34, cy_ + 44, 9, C["rec"])
                c.text(cx_ + 56, cy_ + 54, flag.upper(), F["mono_bold"], 24, C["rec"], 1, 0.14)
                c.text(cx_ + 30, cy_ + 104, name, F["mono_med"], 30, c.theme("ink", "d_ink"), 1)
                c.text(cx_ + 30, cy_ + 134, status, F["mono"], 20, c.theme("muted", "d_muted"), 1)
            appear(c, t, anc, L10.start - 0.15, (cx_, cy_, cw_, chh), leak_card, enter="pop", exit="left", rot=rot)

        def ring(c):
            auto = in_out_cubic(prog(t, t_auto, 0.6))
            clock24(c, clock_c[0], clock_c[1], 280, dev(t), C["accent"], width=60,
                    marker=2, marker_p=out_expo(prog(t, L10.start + 0.4, 0.4)) * (1 - auto),
                    center="02:00" if auto < 0.5 else "OFF",
                    center_sub="dev · running" if auto < 0.5 else "auto-shutdown · 18:00 – 08:00",
                    center_color=c.theme("ink", "d_ink") if auto < 0.5 else C["ok"],
                    center_alpha=abs(1 - 2 * auto) if 0.3 < auto < 0.7 else 1.0)
            bp = out_expo(prog(t, t_beres, 0.4))
            if bp > 0:
                icons.check(c, clock_c[0], clock_c[1] + 400, 50, C["ok"], 6, p=bp)
        appear(c, t, L10.start, e - OUT, (clock_c[0] - 380, clock_c[1] - 380, 760, 760), ring, enter="right")
    v.add(s, e, draw)
    v.sfx("whoosh", s)
    for name, t_k, gain in type_cues(cmd, t_cmd, 40, gain=0.35):
        v.sfx(name, t_k, gain)
    for k in range(len(TERM_ROWS)):
        v.sfx("tick", t_rows + k * 0.08, 0.25)
    for _, a in flagged:
        v.sfx("pop", a, 0.6)
    v.sfx("whoosh", L10.start - 0.15, 0.7)
    v.sfx("pop", L10.start + 0.4)
    v.sfx("chime", t_beres)


# ── 01 · UKURAN ─────────────────────────────────────────────────────────
def ukuran(v, T, s, e):
    ch = v.chapter(1, "RIGHT-SIZING", s, e)
    L12, L15, L16 = T["L12"], T["L15"], T["L16"]
    head = Headline("*Right-size* dulu.")
    t10, t100 = T.word("L13", "sepuluh"), T.word("L14", "seratus")
    t_one, t_down = T.word("L15", "satu"), T.word("L16", "downsize")
    bus_y, seat, gap, cols, rows = 600, 62, 16, 8, 5
    full = (cols * seat + (cols - 1) * gap + 68, rows * seat + (rows - 1) * gap + 68 + 30)
    kept = (4 * seat + 3 * gap + 68, seat + 68 + 30)
    drag0, drag1 = t_down - 0.15, t_down + 0.75

    cam = v.camera
    cam.key(t10 - 0.2, zoom=1.08, y=780, dur=0.6)
    cam.key(t100, zoom=0.97, y=960, dur=0.35, ease=out_expo)  # punch out on "seratus"
    cam.reset(t100 + 0.5, dur=0.5)
    cam.focus(L15.start + 0.4, (X, bus_y, full[0], full[1]), zoom=1.05, dur=1.2)
    cam.reset(drag1 + 0.3, dur=0.8)

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, ch.kicker, ch.color)
        head.draw(c, t, L12.start, e - OUT)

        def battle(c):
            p10, p100 = prog(t, t10, 0.8), prog(t, t100, 0.7)
            c.text(X, 640, "CPU USAGE", F["mono_med"], 26, c.theme("ink2", "d_muted"), 1, 0.18)
            odometer(c, X - 6, 880, "10%", p10, 230, C["accent"], spins=1)
            if p100 > 0:
                c.text(X, 1000, "BILLED", F["mono_med"], 26, c.theme("ink2", "d_muted"), clamp(p100 * 3), 0.18)
                with c.at(0, 0, 1 + 0.25 * (1 - out_back(p100, 2.2)), origin=(X + 300, 1180)):
                    odometer(c, X - 10, 1290, "100%", p100, 300, C["orange_pill"], spins=1)
        appear(c, t, t10 - 0.3, L15.start - 0.15, (X, 580, CW, 760), battle, exit="up", blur=4)

        def bus(c):
            pk = in_out_cubic(prog(t, drag0, drag1 - drag0))
            cw_, chh = seat_grid(c, X, bus_y, cols, rows, t, p_in=prog(t, L15.start, 0.9), filled=(2,),
                                 p_fill=prog(t, t_one, 0.4), keep=4, p_keep=pk, seat=seat, gap=gap)
            if t >= drag0 - 0.4:
                select_box(c, t, drag0 - 0.4, X, bus_y, cw_, chh + 18, f"{int(cw_)} × {int(chh)}")
        appear(c, t, L15.start, e - OUT, (X, bus_y, full[0], full[1]), bus, enter="up")
        note(c, X + 420, bus_y + kept[1] + 140, "monitor dulu,\nbaru downsize", prog(t, L16.start, 0.9),
             arrow_to=(X + kept[0] - 20, bus_y + kept[1] + 40))
    v.add(s, e, draw)
    v.track(Cursor([(drag0 - 0.5, X + full[0] + 160, bus_y + full[1] + 160),
                    (drag0, X + full[0] + 6, bus_y + full[1] + 24),
                    (drag1, X + kept[0] + 6, bus_y + kept[1] + 24)],
                   clicks=[drag0], hide=drag1 + 0.6))
    v.sfx("whoosh", s)
    count_ticks(v, t10, 0.6, 0.1)
    v.sfx("thud", t100 + 0.1)
    v.sfx("whoosh", L15.start - 0.15, 0.6)
    v.sfx("pop", t_one)
    v.sfx("whoosh", drag0 + 0.1, 0.4)


# ── 02 · LANGGANAN ──────────────────────────────────────────────────────
def langganan(v, T, s, e):
    ch = v.chapter(2, "RESERVED & SPOT", s, e)
    L17 = T["L17"]
    head = Headline("Jangan semua *on-demand*.")
    t_e, t_l = T.word("L17", "demand"), T.word("L18", "reserved")
    t_s, t_b = T.word("L19", "spot"), T.word("L20", "beda")
    rx, ry, rw = X + 10, 560, 560

    cam = v.camera
    cam.key(L17.start + 0.3, zoom=1.05, x=rx + rw / 2 + 120, y=760, dur=1.0)
    cam.key(t_s - 0.2, zoom=1.05, x=rx + rw / 2 + 120, y=960, dur=1.0)
    cam.reset(t_b, dur=0.5, ease=out_expo)

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, ch.kicker, ch.color)
        head.draw(c, t, L17.start, e - OUT)

        def paper(c):
            receipt(c, rx, ry, rw, [
                ("On-demand", "$$$$$", prog(t, t_e - 0.1, 0.4), prog(t, t_l, 0.5), C["orange_pill"]),
                ("Reserved instance", "$$$", prog(t, t_l, 0.4), 0.0, C["accent"]),
                ("Spot instance", "$", prog(t, t_s, 0.4), 0.0, C["ok"]),
            ], title="TAGIHAN CLOUD", sub="server yang sama · per bulan")
            stamp(c, rx + rw / 2 + 40, ry + 400, "HEMAT", prog(t, t_b, 0.35), color=C["accent"], size=96)
        appear(c, t, L17.start + 0.1, e - OUT, (rx, ry, rw, 640), paper, rot=-0.025, exit="right")
        row = lambda k: ry + 150 + 96 * k + 50  # noqa: E731
        note(c, rx + rw + 40, row(1) - 40, "yang nyala\nterus", prog(t, t_l + 0.3, 0.9),
             arrow_to=(rx + rw - 10, row(1) - 10))
        note(c, rx + rw + 40, row(2) + 40, "boleh\ndi-interrupt", prog(t, t_s + 0.3, 0.9),
             arrow_to=(rx + rw - 10, row(2) - 10), size=36)
        fade(c, t, t_e + 0.6, e - OUT,
             lambda c: c.text(X, 1420, "*jumlah $ = ilustrasi, bukan harga asli", F["mono"], 17,
                              c.theme("muted", "d_muted"), 1, 0.02))
    v.add(s, e, draw)
    v.sfx("whoosh", s)
    for tt in (t_e, t_l, t_s):
        v.sfx("pop", tt)
    v.sfx("tick", t_l + 0.05, 0.5)
    v.sfx("thud", t_b)
    v.sfx("chime", t_b + 0.15)


# ── 03 · ARSITEKTUR ─────────────────────────────────────────────────────
def arsitektur(v, T, s, e):
    ch = v.chapter(3, "ARSITEKTUR", s, e)
    L21, L24, L25 = T["L21"], T["L24"], T["L25"]
    head = Headline("Ubah *arsitekturnya*.")
    t_big = T.word("L21", "arsitekturnya")
    t_split, t_move = T.word("L22", "dipecah"), T.word("L23", "serverless")
    t_pas = T.word("L24", "pas")
    by, bh, zh = 580, 380, 160

    cam = v.camera
    cam.focus(t_big, (X, by, CW, bh), zoom=1.07, dur=0.8)
    cam.key(t_split, zoom=0.96, y=930, dur=0.4, ease=out_expo)
    cam.key(t_split + 0.5, zoom=1.0, y=1000, dur=1.5)
    cam.reset(L25.end, dur=0.6)

    def glow(t):
        return [out_expo(prog(t, t_pas + k * 0.22, 0.15)) * (1 - prog(t, t_pas + k * 0.22 + 0.3, 0.5))
                for k in range(3)]

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, ch.kicker, ch.color)
        head.draw(c, t, L21.start, e - OUT)
        appear(c, t, t_big - 0.1, e - OUT, (X, by, CW, bh + 50 + zh),
               lambda c: block_split(c, X, by, CW, ["web", "api", "auth", "laporan", "export", "notif"],
                                     p_split=prog(t, t_split, 0.9), moved=(3, 4, 5),
                                     p_move=prog(t, t_move, 0.9), h=bh, zone_h=zh, glow=glow(t)),
               enter="pop", exit="down")
        note(c, X + CW - 10, by + bh + 50 + zh + 90, "pay-per-use", prog(t, t_pas, 0.9),
             align="r", size=44)

        def arrow(c):
            ay = 1400
            c.text(X, ay, "PALING LAMA  ·  EFEK PALING PANJANG", F["mono_med"], 21, c.theme("ink2", "d_muted"), 1, 0.14)
            p = in_out_cubic(prog(t, T.word("L25", "panjang"), 0.6))
            if p > 0:
                ex = X + CW * p
                acc = c.theme("accent", "d_accent")
                c.line(X, ay + 28, ex, ay + 28, acc, 4)
                c.line(ex - 14, ay + 18, ex, ay + 28, acc, 4)
                c.line(ex - 14, ay + 38, ex, ay + 28, acc, 4)
        fade(c, t, L25.start, e - OUT, arrow)
    v.add(s, e, draw)
    v.sfx("whoosh", s)
    v.sfx("thud", t_big)
    v.sfx("whoosh", t_split, 0.7)
    for k in range(3):
        v.sfx("pop", t_move + 0.12 * k, 0.45)
        v.sfx("tick", t_pas + k * 0.22, 0.45)


# ── RECAP (dark) ────────────────────────────────────────────────────────
def recap(v, T, s, e):
    v.chapter(None, "EMPAT LANGKAH", s, e, dark=True)
    L26, L28, L29 = T["L26"], T["L28"], T["L29"]
    head1 = Headline("Empat langkah.", style="headline_dark")
    head2 = Headline("Hasilnya:", style="headline_dark")
    head3 = Headline("Hemat ≠ *lemot*.", style="headline_dark")
    words = ["bocor", "sizing", "reserved", "arsitektur"]
    t_lv = [T.word("L27", w) for w in words]
    t_cnt = L28.start + 0.1
    d_cnt = max(0.9, T.word("L28", "dolar", edge="end") - t_cnt + 0.2)
    t_lemot = T.word("L29", "lemot")
    cy, chh = 560, 700
    fx = [0.14 + 0.22 * i for i in range(4)]
    num_y = 1000

    def drops(t):
        return [(fx[i], 0.15, LEVERS[i], out_expo(prog(t, t_lv[i], 0.5))) for i in range(4)]

    def ball_x(t):
        xf = 0.03
        for i in range(4):
            xf = lerp(xf, fx[i] + 0.1, in_out_cubic(prog(t, t_lv[i], 0.5)))
        return xf

    cam = v.camera
    cam.key(t_lv[0] - 0.3, zoom=1.06, x=X + CW * 0.3, y=cy + chh * 0.45, dur=0.6)
    cam.key(t_lv[3], zoom=1.06, x=X + CW * 0.7, y=cy + chh * 0.6, dur=1.2)
    cam.key(t_cnt - 0.05, zoom=1.2, y=num_y - 80, dur=0.01)
    cam.key(t_cnt, zoom=1.0, dur=d_cnt + 0.6, ease=out_cubic)

    def draw(c, t):
        head1.draw(c, t, L26.start, L28.start - 0.15)
        head2.draw(c, t, L28.start, L29.start - 0.15)
        head3.draw(c, t, L29.start, e - OUT)

        def stairs(c):
            ds = drops(t)
            cost_chart(c, X, cy, CW, chh, t, draw=1.0, drops=ds, months=("", "", "", ""),
                       caption="BIAYA CLOUD / BULAN", line_w=7, labels_size=30)
            bx_, by_ = chart_point(X, cy, CW, chh, ds, ball_x(t))
            c.circle(bx_, by_ - 16, 16, C["d_ink"])
        appear(c, t, L26.start + 0.2, L28.start - 0.15, (X, cy, CW, chh), stairs, exit="down")

        def number(c):
            odometer(c, MID, num_y, "$14.000", prog(t, t_cnt, d_cnt), 210, C["d_ink"], align="c")
            c.text(MID, num_y + 78, "/ bulan", F["ui"], 44, C["d_muted"], 1, -0.01, align="c")
            p = in_out_cubic(prog(t, t_lemot, 0.7))
            if p > 0:
                yy = num_y + 210
                c.text(MID, yy, "BUKAN POTONG PERFORMA", F["mono_med"], 22, C["d_muted"], 1, 0.18, align="c")
                c.line(MID - 300, yy + 44, MID - 300 + 600 * p, yy + 44, C["ok"], 5)
                icons.check(c, MID, yy + 120, 40, C["ok"], 5, p=out_expo(prog(t, t_lemot + 0.7, 0.4)))
        appear(c, t, L28.start, e - OUT, (X, num_y - 220, CW, 560), number, enter="pop", blur=4)
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    for tt in t_lv:
        v.sfx("pop", tt, 0.55)
    count_ticks(v, t_cnt, d_cnt)
    v.sfx("thud", t_cnt + d_cnt)
    v.sfx("chime", t_lemot + 0.7)


# ── OUTRO (dark, centered) ──────────────────────────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L30 = T["L30"]
    t_site = T.word("L31", "mumeyong")
    t_click = T.word("L32", "follow") + 0.4
    cx = MID

    def draw(c, t):
        icons.play_logo(c, cx, 640, 110, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.1)))
        fade(c, t, s + 0.6, None,
             lambda c: c.text(cx, 860, tk.BRAND_NAME, F["display"], 92, C["d_ink"], 1, -0.05, align="c"))
        fade(c, t, L30.start, None,
             lambda c: c.text(cx, 930, "Biaya cloud-mu bocor di mana?", F["ui"], 34, C["d_ink"], 0.85, -0.02,
                              align="c"))
        sp = out_back(prog(t, t_site, 0.45)) if t >= t_site else 0.0
        if sp > 0:
            with c.at(0, 0, 0.9 + 0.1 * sp, origin=(cx, 1012)):
                contact_pill(c, cx, 980, tk.CONTACT["site"], "SITUS", alpha=clamp(sp))
        fade(c, t, T["L32"].start, None, lambda c: follow_button(c, cx, 1110, t, t_click))
        fade(c, t, t_click + 0.5, None,
             lambda c: c.text(cx, 1250, "Bongkar arsitektur cloud lainnya.", F["ui"], 28, C["d_muted"], 1,
                              align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(t_site - 0.2, 860, 1400), (t_site + 0.4, cx + 120, 1020), (t_click, cx + 40, 1150)],
                   clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", t_site)
    v.sfx("chime", t_click + 0.1)
