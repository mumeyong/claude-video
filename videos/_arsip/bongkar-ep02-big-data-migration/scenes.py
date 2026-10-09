"""Bongkar Arsitektur EP02 — Pindahin big data ke cloud, tanpa satu byte hilang. See IDENTITY.md / TREATMENT.md.

Metaphor: a library being moved while it's still open. Signature move: old/new pairs slide together and LOCK green
when the checksum matches. Signature color: green. Hook: myth struck out. No numbers (none given) — row counts masked.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, out_back, in_out_cubic, clamp, pulse
from engine.components import (Headline, kicker, appear, fade, Cursor, tag, icons, note, follow_button,
                               arch_diagram, keycap, bookshelf, shelf_books, sync_pipe, twin_table,
                               cutover_switch, padlock, series_bumper, GREEN)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
MID = tk.W / 2
LEAD = 0.6
TAIL = 3.0
CH = ["00 · MASALAH", "01 · KEPUTUSAN", "02 · DIAGRAM", "03 · HASIL", "RECAP", "OUTRO"]


def build(project):
    T = project.timing
    v = Video(duration=T["L24"].end + TAIL, bpm=128, beat_offset=0.0, series="BONGKAR ARSITEKTUR · EP 02")
    v.cover_t = T["L04"].end
    v.music = dict(key="F", mood="dreamy")           # generated score: calm library, careful
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


# ── INTRO: keycaps → struck myth → falling book → zero data loss → bumper ─
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L3, L4, L5 = T["L01"], T["L03"], T["L04"], T["L05"]
    t_c, t_v, t_beres = T.word("L01", "copy"), T.word("L01", "paste"), T.word("L01", "beres")
    t_no = T.word("L02", "nggak")
    t_lost = T.word("L03", "hilang")
    t_zero = T.word("L04", "zero")
    head1 = Headline("~Copy, paste, beres~?")
    head2 = Headline("Satu record *hilang*.")
    bump0, bump1 = e, max(e + 1.4, L5.start - 0.05)
    shelf = (X, 600, CW, 560)
    books = shelf_books(*shelf, rows=4, seed=3)
    fall_i = len(books) // 2 + 3

    cam = v.camera
    cam.key(0.0, zoom=1.1, dur=0.01)
    cam.key(L1.start, zoom=1.0, dur=1.6, ease=out_cubic)
    cam.focus(t_lost - 0.1, (books[fall_i][0] - 150, books[fall_i][1], 300, 500), zoom=1.12, dur=0.5)
    cam.reset(L4.start, dur=0.5)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "MIGRASI DATA · ALIBABA CLOUD", GREEN)
        head1.draw(c, t, L1.start, L3.start - 0.15, strike_at=t_no)
        head2.draw(c, t, L3.start, L4.start - 0.15)

        def keys(c):
            keycap(c, MID - 150, 900, "C", pulse(t, t_c, 0.25), 240, sub="Ctrl")
            keycap(c, MID + 150, 900, "V", pulse(t, t_v, 0.25), 240, sub="Ctrl")
            fade(c, t, t_beres, None, lambda c: c.text(MID, 1150, "beres?", F["serif"], 64,
                                                        c.theme("accent", "d_accent"), 1, align="c"))
        appear(c, t, L1.start, L3.start - 0.15, (MID - 300, 760, 600, 420), keys, enter="pop", exit="down")

        def lost(c):
            fp = prog(t, t_lost - 0.3, 0.9)
            bookshelf(c, *shelf, t, rows=4, seed=3, pulled={fall_i: min(0.5, fp * 2)} if fp < 0.25 else None,
                      falling=(fall_i, clamp((fp - 0.25) / 0.75)) if fp >= 0.25 else None)
            tp = out_expo(prog(t, t_lost + 0.4, 0.4))
            if tp > 0:
                tag(c, X, shelf[1] + shelf[3] + 30, "1 record hilang", C["rec"], tp, h=44)
                note(c, X + CW - 10, shelf[1] + shelf[3] + 120, "laporan salah,\nnggak ada yang sadar",
                     prog(t, T.word("L03", "laporan"), 0.9), align="r", size=38)
        appear(c, t, L3.start - 0.05, L4.start - 0.15, shelf, lost, exit="left")

        def zero(c):
            p = prog(t, t_zero, 0.35)
            c.text(MID, 820, "legacy infra  →  Alibaba Cloud", F["mono_med"], 28, c.theme("ink2", "d_muted"),
                   out_expo(prog(t, L4.start, 0.4)), 0.06, align="c")
            with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, 1000)):
                c.text(MID, 1010, "zero", F["display"], 230, GREEN, clamp(p * 3), -0.06, align="c")
                c.text(MID, 1190, "data loss.", F["display"], 150, c.theme("ink", "d_ink"), clamp(p * 3), -0.06,
                       align="c")
        appear(c, t, L4.start, e - OUT, (X, 740, CW, 500), zero, enter="up", blur=4)
    v.add(s, e + 0.4, draw)
    v.add(bump0, bump1, lambda c, t: series_bumper(c, t, bump0, bump1, 2, "Big data migration · Alibaba Cloud",
                                                    GREEN), z=100)
    v.sfx("click", t_c, 0.8)
    v.sfx("click", t_v, 0.8)
    v.sfx("thud", t_no, 0.7)
    v.sfx("pop", t_lost - 0.2, 0.4)
    v.sfx("thud", t_lost + 0.3)
    v.sfx("whoosh", L4.start - 0.1, 0.5)
    v.sfx("thud", t_zero)
    v.sfx("whoosh", bump0, 0.8)
    v.sfx("whoosh", bump1 - 0.35, 0.5)


# ── 00 · MASALAH: the library is still open ────────────────────────────
def masalah(v, T, s, e):
    ch = v.chapter(0, "MASALAH", s, e)
    L5, L7, L8 = T["L05"], T["L07"], T["L08"]
    t_pinjam = T.word("L06", "pinjam")
    t_ubah = T.word("L07", "berubah")
    t_late = T.word("L08", "ketinggalan")
    head1 = Headline("Perpustakaan yang *masih buka*.")
    head2 = Headline("Datanya terus *berubah*.")
    full = (X, 600, CW, 620)
    half_w = (CW - 24) / 2
    books = shelf_books(*full, rows=4, seed=7)
    n = len(books)
    borrow = [(int(n * f), k * 0.55) for k, f in enumerate((0.12, 0.47, 0.71, 0.3, 0.86, 0.58))]
    change = [int(n * f) for f in (0.2, 0.55, 0.8, 0.38)]

    cam = v.camera
    cam.key(t_pinjam - 0.2, zoom=1.06, y=full[1] + full[3] / 2, dur=1.4)
    cam.reset(L8.start, dur=0.6)

    def draw(c, t):
        kicker(c, t, L5.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L5.start, L7.start - 0.15)
        head2.draw(c, t, L7.start, e - OUT)
        split = in_out_cubic(prog(t, L8.start, 0.7))
        w_now = full[2] - (full[2] - half_w) * split
        pulled = {i: prog(t, t_pinjam + d, 0.9) for i, d in borrow}
        changed = {i: prog(t, t_ubah + k * 0.25, 0.6) for k, i in enumerate(change)}

        k_small = half_w / full[2]
        sc = 1 - (1 - k_small) * split                    # uniform scale → books keep their proportions
        y_off = (1 - sc) * full[3] / 2                     # keep the shelf vertically centred while shrinking

        def shelf(c):
            with c.at(0, y_off, sc, origin=(full[0], full[1])):
                bookshelf(c, *full, t, rows=4, seed=7, pulled=pulled, changed=changed)
                op = out_back(prog(t, L5.start + 0.4, 0.45)) if t >= L5.start + 0.4 else 0
                if op > 0:
                    with c.at(0, 0, max(0.01, op), origin=(full[0] + 70, full[1] - 10)):
                        c.fill_rrect(full[0] + 10, full[1] - 32, 120, 44, 22, GREEN)
                        c.text(full[0] + 70, full[1] - 3, "OPEN", F["mono_bold"], 20, (1, 1, 1, 1), 1, 0.12,
                               align="c")
        appear(c, t, L5.start, e - OUT, full, shelf, enter="up")

        def copy(c):
            cx_ = full[0] + half_w + 24
            yy = full[1] + (1 - k_small) * full[3] / 2
            c.text(cx_, yy - 14, "COPY · SEKALI", F["mono_bold"], 18, c.theme("muted", "d_muted"), 1, 0.14)
            with c.at(cx_ - full[0], yy - full[1], k_small, origin=(full[0], full[1])):
                bookshelf(c, *full, t, rows=4, seed=7, ghost=0.75, diff=set(change),
                          diff_p=out_expo(prog(t, t_late, 0.4)))
        appear(c, t, L8.start + 0.2, e - OUT, (full[0] + half_w + 24, full[1], half_w, full[3]), copy, enter="right")
        fade(c, t, t_late + 0.2, e - OUT, lambda c: tag(c, full[0] + half_w + 24,
                                                       full[1] + (1 + k_small) * full[3] / 2 + 30,
                                                       "ketinggalan perubahan", C["rec"], h=44))
    v.add(s, e, draw)
    v.sfx("whoosh", L5.start, 0.6)
    v.sfx("pop", L5.start + 0.4, 0.5)
    for i, d in borrow:
        v.sfx("tick", t_pinjam + d, 0.3)
    for k in range(len(change)):
        v.sfx("tick", t_ubah + k * 0.25, 0.4)
    v.sfx("whoosh", L8.start + 0.2, 0.5)
    for k in range(3):
        v.sfx("pop", t_late + k * 0.1, 0.4)


# ── 01 · KEPUTUSAN: two-stage sync pipe ─────────────────────────────────
def keputusan(v, T, s, e):
    ch = v.chapter(1, "KEPUTUSAN", s, e)
    L9, L12 = T["L09"], T["L12"]
    t_full = T.word("L10", "full")
    t_inc = T.word("L11", "incremental")
    t_open = T.word("L12", "buka")
    head = Headline("*Dua* tahap.")
    src = dict(x=MID - 260, y=600, w=520, h=130, kind="svc", label="legacy")
    dst = dict(x=MID - 260, y=1150, w=520, h=130, kind="svc", label="Alibaba Cloud")

    cam = v.camera
    cam.key(t_full, zoom=1.05, y=880, dur=1.0)
    cam.key(t_inc, zoom=1.05, y=1000, dur=1.0)
    cam.reset(L12.start, dur=0.8)

    def draw(c, t):
        kicker(c, t, L9.start - 0.2, e - OUT, ch.kicker, ch.color)
        head.draw(c, t, L9.start, e - OUT)
        a_src = out_expo(prog(t, L9.start + 0.2, 0.4))
        a_dst = out_expo(prog(t, L9.start + 0.4, 0.4))

        def pipe(c):
            sync_pipe(c, t, dict(src, a=a_src), dict(dst, a=a_dst), p_pipe=in_out_cubic(prog(t, L9.start + 0.5, 0.8)),
                      p_full=prog(t, t_full, max(1.0, t_inc - t_full)), p_inc=out_expo(prog(t, t_inc, 0.8)),
                      open_badge=prog(t, t_open, 0.45))
            for k, (lbl, tt) in enumerate((("1", t_full), ("2", t_inc))):
                p = out_back(prog(t, tt, 0.4)) if t >= tt else 0
                if p > 0:
                    bx = MID - 70 if k == 0 else MID + 70
                    with c.at(0, 0, max(0.01, p), origin=(bx, 760)):
                        c.circle(bx, 760, 26, GREEN)
                        c.text(bx, 770, lbl, F["mono_bold"], 26, (1, 1, 1, 1), 1, align="c")
        appear(c, t, L9.start + 0.1, e - OUT, (MID - 300, 600, 600, 700), pipe, blur=4, rise=20)
        note(c, X + CW - 10, 590, "tetap jalan", prog(t, t_open + 0.2, 0.8), arrow_to=(src["x"] + src["w"] - 30, 610),
             align="r", size=40)
    v.add(s, e, draw)
    v.sfx("pop", L9.start + 0.2, 0.5)
    v.sfx("pop", L9.start + 0.4, 0.5)
    v.sfx("whoosh", t_full, 0.6)
    for k in range(5):
        v.sfx("tick", t_inc + k * 0.3, 0.3)
    v.sfx("pop", t_open, 0.5)


# ── 02 · DIAGRAM: arch band + twin table locking ───────────────────────
ROWS = [  # name, legacy hash, cloud hash (cloud's last row is off by one char before re-sync)
    ("orders", "9f3a·c21e", "9f3a·c21e"),
    ("customers", "71bd·08fa", "71bd·08fa"),
    ("events", "e04c·5b93", "e04c·5b93"),
    ("inventory", "3a7e·d16f", "3a7e·d14f"),
]


def diagram(v, T, s, e):
    ch = v.chapter(2, "DIAGRAM", s, e)
    L13, L15, L16 = T["L13"], T["L15"], T["L16"]
    t_sync = T.word("L14", "sync")
    t_check = T.word("L15", "dicek")
    t_bad = T.word("L16", "karakter")
    t_fix = T.word("L16", "sync")
    head1 = Headline("Disalin, lalu *dicek*.")
    head2 = Headline("Beda satu karakter? *Ketahuan*.")
    ty = 860
    lock_t = [t_check + 0.2 + k * 0.45 for k in range(3)]
    row_h = 96

    cam = v.camera
    cam.focus(t_check, (X, ty, CW, 64 + row_h * 4), zoom=1.04, dur=0.8)
    cam.focus(t_bad, (X + CW / 2, ty + 64 + row_h * 3, CW / 2, row_h), zoom=1.22, dur=0.6)
    cam.reset(t_fix + 0.9, dur=0.6)

    def draw(c, t):
        kicker(c, t, L13.start - 0.2, e - OUT, ch.kicker, ch.color)
        head1.draw(c, t, L13.start, L16.start - 0.15)
        head2.draw(c, t, L16.start, e - OUT)

        def band(c):
            nodes = {
                "src": dict(x=X, y=560, w=300, h=96, kind="svc", label="legacy", a=out_expo(prog(t, L13.start, 0.4))),
                "dst": dict(x=X + CW - 300, y=560, w=300, h=96, kind="svc", label="Alibaba Cloud",
                            a=out_expo(prog(t, L13.start + 0.2, 0.4))),
            }
            arch_diagram(c, t, nodes, [])
            p = in_out_cubic(prog(t, L13.start + 0.4, 0.6))
            ax0, ax1, ay = X + 300, X + CW - 300, 608
            c.line(ax0 + 12, ay, ax0 + 12 + (ax1 - ax0 - 24) * p, ay, c.theme("faint", "d_line"), 6)
            c.text((ax0 + ax1) / 2, ay - 18, "SYNC", F["mono_bold"], 18, c.theme("muted", "d_muted"), p, 0.16, align="c")
            if t >= t_sync:
                for k in range(3):
                    f = (t * 0.7 + k / 3) % 1.0
                    c.circle(ax0 + 12 + (ax1 - ax0 - 24) * f, ay, 8, GREEN, min(1, f * 6, (1 - f) * 6))
        appear(c, t, L13.start - 0.1, e - OUT, (X, 560, CW, 96), band, blur=4, rise=20)

        def table(c):
            rows = []
            for k, (name, hl, hr) in enumerate(ROWS):
                slide = prog(t, t_check - 0.4 + k * 0.18, 0.5)
                if k < 3:
                    lock = prog(t, lock_t[k], 0.4)
                    rows.append(dict(name=name, count="•••.•••", h_left=hl, h_right=hr, slide=slide, lock=lock))
                else:
                    fix = prog(t, t_fix, 0.6)
                    rows.append(dict(name=name, count="•••.•••", h_left=hl, h_right=hr, slide=slide,
                                     bad=7, fix=fix, lock=prog(t, t_fix + 0.6, 0.4)))
            twin_table(c, X, ty, CW, rows, row_h=row_h)
        appear(c, t, t_check - 0.5, e - OUT, (X, ty, CW, 64 + row_h * 4 + 20), table, enter="up")
        note(c, X + CW - 10, ty + 64 + row_h * 4 + 110, "di-sync ulang", prog(t, t_fix + 0.2, 0.8),
             arrow_to=(X + CW - 120, ty + 64 + row_h * 3 + 70), align="r", size=40)
    v.add(s, e, draw)
    v.sfx("pop", L13.start, 0.5)
    v.sfx("pop", L13.start + 0.2, 0.5)
    v.sfx("tick", t_sync, 0.4)
    for tt in lock_t:
        v.sfx("click", tt + 0.1, 0.6)
    v.sfx("thud", t_bad, 0.6)
    v.sfx("whoosh", t_fix, 0.4)
    v.sfx("chime", t_fix + 0.65)


# ── 03 · HASIL: cutover switch → zero data loss ────────────────────────
def hasil(v, T, s, e):
    ch = v.chapter(3, "HASIL", s, e)
    L17, L19 = T["L17"], T["L19"]
    t_cut = T.word("L17", "cutover")
    t_rb = T.word("L18", "rollback")
    t_zero = T.word("L19", "zero")
    head = Headline("Semua match → *cutover*.")
    box = (X, 580, CW, 760)

    cam = v.camera
    cam.focus(t_cut - 0.1, (MID - 200, 700, 400, 300), zoom=1.08, dur=0.4)
    cam.key(t_cut + 0.4, zoom=1.0, dur=0.6)

    def draw(c, t):
        kicker(c, t, L17.start - 0.2, e - OUT, ch.kicker, ch.color)
        head.draw(c, t, L17.start, L19.start - 0.15)
        appear(c, t, L17.start, L19.start - 0.15, box,
               lambda c: cutover_switch(c, t, *box, p_flip=prog(t, t_cut, 0.6), p_rollback=prog(t, t_rb, 0.6)),
               enter="pop", exit="up")

        def punch(c):
            p = prog(t, t_zero, 0.35)
            with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, 980)):
                c.text(MID, 980, "zero", F["display"], 260, GREEN, clamp(p * 3), -0.06, align="c")
                c.text(MID, 1160, "data loss.", F["display"], 160, c.theme("ink", "d_ink"), clamp(p * 3), -0.06,
                       align="c")
            icons.check(c, MID, 1330, 60, GREEN, 8, p=out_expo(prog(t, t_zero + 0.4, 0.5)))
        appear(c, t, L19.start, e - OUT, (X, 760, CW, 620), punch, enter="up", blur=4)
    v.add(s, e, draw)
    v.sfx("pop", L17.start, 0.5)
    v.sfx("click", t_cut, 0.8)
    v.sfx("whoosh", t_cut + 0.1, 0.5)
    v.sfx("pop", t_rb, 0.5)
    v.sfx("thud", t_zero)
    v.sfx("chime", t_zero + 0.45)


# ── RECAP (dark): proof gate with a padlock ────────────────────────────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L20, L21, L22 = T["L20"], T["L21"], T["L22"]
    t_bukti = T.word("L21", "bukti")
    t_move = T.word("L22", "pindah")
    head1 = Headline("Bukan soal *copy*.", style="headline_dark")
    head2 = Headline("Tapi soal *bukti*.", style="headline_dark")
    head3 = Headline("Belum terbukti? *Belum pindah*.", style="headline_dark")
    checks = [("row count", t_bukti + 0.2), ("checksum", t_bukti + 0.6)]

    cam = v.camera
    cam.key(t_move - 0.2, zoom=1.1, y=1000, dur=0.5)
    cam.reset(t_move + 0.8, dur=0.6)

    def draw(c, t):
        head1.draw(c, t, L20.start, L21.start - 0.15)
        head2.draw(c, t, L21.start, L22.start - 0.15)
        head3.draw(c, t, L22.start, e - OUT)

        def gate(c):
            padlock(c, MID, 900, 200, p_open=prog(t, t_move, 0.6))
            for k, (lbl, tt) in enumerate(checks):
                p = out_expo(prog(t, tt, 0.4))
                y = 1200 + k * 90
                c.fill_rrect(MID - 220, y - 40, 440, 70, 35, C["d_card"], max(0.4, p))
                c.text(MID - 180, y + 8, lbl, F["mono_med"], 28, C["d_ink"], 0.5 + 0.5 * p, 0.04)
                if p > 0:
                    c.circle(MID + 170, y - 5, 22, GREEN, p)
                    icons.check(c, MID + 170, y - 5, 20, (1, 1, 1, 1), 3.5, p=p)
            op = out_expo(prog(t, t_move + 0.4, 0.4))
            if op > 0:
                c.text(MID, 1450, "boleh pindah", F["serif"], 54, GREEN, op, align="c")
        appear(c, t, L20.start + 0.2, e - OUT, (MID - 260, 700, 520, 800), gate, enter="pop")
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    for _, tt in checks:
        v.sfx("pop", tt, 0.5)
    v.sfx("click", t_move, 0.8)
    v.sfx("chime", t_move + 0.4)


# ── OUTRO: logo + EP03 teaser + follow ─────────────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    L23, L24 = T["L23"], T["L24"]
    t_click = T.word("L24", "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, GREEN)
            c.text(X + 50, 892, "EPISODE BERIKUTNYA · EP 03", F["mono_bold"], 20, GREEN, 1, 0.16)
            c.text(X + 50, 962, "Big data stack jadi serverless", F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, "Next-gen big data ecosystem", F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, L23.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, L24.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, "Seri Bongkar Arsitektur", F["ui"], 28,
                                                          C["d_muted"], 1, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(L24.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", L23.start, 0.5)
    v.sfx("chime", t_click + 0.1)
