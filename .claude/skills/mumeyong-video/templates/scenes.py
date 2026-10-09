"""Demo video — the reference grammar in 8 lines. Copy the patterns, replace the content.

Every time below comes from timing.json (T). Chapters start LEAD seconds before their first line so the
transition happens in the pause, and everything in a chapter exits at (chapter end - OUT).
"""
from engine import Video, tokens as tk
from engine.ease import prog, out_expo, out_cubic, in_out_cubic, in_cubic
from engine.components import (Headline, kicker, appear, fade, ChatTrack, Cursor, window, tag, word_pill,
                               select_box, big_number, filmstrip, comment, step_row, rule_box, connector,
                               segments, follow_button, contact_pill, icons, type_end, fmt_id, mumei_mark,
                               brand_intro)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
LEAD = 0.6          # chapter starts this long before its first line
OUTRO_TAIL = 3.5    # seconds after the last line
PRE_ROLL = 2.05     # brand sting (version 2) first: the engine starts the voice + every T time this much later


def build(project):
    T = project.timing
    v = Video(duration=T.line("L08").end + OUTRO_TAIL, bpm=128, beat_offset=0.0)
    brand_intro(v, version=2)  # opening sting: ink drop → ensō → seal → MUMEYONG → brushy wipe into the video
    v.chat = ChatTrack()
    b = {name: T.chapter_span(name)[0] - LEAD for name in ("00 · ATURAN", "01 · KODE", "RECAP", "OUTRO")}
    intro(v, T, 0.0, b["00 · ATURAN"])
    aturan(v, T, b["00 · ATURAN"], b["01 · KODE"])
    kode(v, T, b["01 · KODE"], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    outro(v, T, b["OUTRO"], v.duration)
    return v


# ── INTRO ───────────────────────────────────────────────────────────────
CODE = [
    "# scenes.py — frame = f(t)",
    "from engine import Video",
    "",
    "def build(project):",
    "    T = project.timing",
    "    v = Video(duration=T.duration)",
    "    v.add(T['L03'].start, end, aturan)",
    "    return v",
]


def _pill(c, t, t_in, t_out, y, word, color):
    def draw(c):
        w, h = word_pill(c, X, y, word, color)
        select_box(c, t, t_in + 0.25, X, y, w, h, f"{int(w)} × {int(h)}")
    appear(c, t, t_in, t_out, (X, y, 620, 150), draw, rise=30, scale=0.9)


def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1 = T["L01"]
    t_nol, t_key = T.word("L02", "nol"), T.word("L02", "keyframe")
    t_100, t_kode = T.word("L02", "seratus"), T.word("L02", "kode")
    lift = t_nol - 0.35  # black hook card lifts just before "nol"

    def hook(c, t):  # z=100 → drawn above the HUD
        a = 1 - in_out_cubic(prog(t, lift, 0.5))
        c.src((0, 0, 0, 1), a)
        c.ctx.rectangle(0, 0, tk.W, tk.H)
        c.ctx.fill()
        appear(c, t, L1.start + 0.05, lift - 0.1, (100, 760, 780, 210),
               lambda c: comment(c, 100, 760, 780, "mumeyong_fan", "video ini bikinnya\npakai apa bang?",
                                 highlight="pakai apa"))
    v.add(s, lift + 0.6, hook, z=100)

    nol = Headline("Nol", style="headline_lg")
    cent = Headline("100%", style="headline_lg")

    def punch(c, t):
        kicker(c, t, lift + 0.2, e - OUT, "VIDEO INI · 30 DETIK", C["accent"])
        nol.draw(c, t, t_nol, t_100 - 0.15)
        cent.draw(c, t, t_100, e - OUT)
        py = nol.bottom(c) + 16
        _pill(c, t, t_key, t_100 - 0.15, py, "keyframe.", C["orange_pill"])
        _pill(c, t, t_kode, e - OUT, py, "kode.", C["accent"])
        cy, ch = py + 210, 400

        def card(c):
            bx, by = window.frame(c, X, cy, CW, ch, "scenes.py", "mumeyong/videos", title_mono=True)
            window.code_lines(c, bx, by, CODE, t, t0=t_kode + 0.4, cps=140)
        appear(c, t, t_kode + 0.2, e - OUT, (X, cy, CW, ch), card)
    v.add(lift, e, punch)
    v.sfx("pop", L1.start + 0.05)
    v.sfx("thud", t_nol)
    v.sfx("whoosh", t_100 - 0.1)
    v.sfx("pop", t_kode)


# ── 00 · ATURAN ─────────────────────────────────────────────────────────
RULES_MD = [
    "# Mumeyong — aturan kerja",
    "## Aturan tetap",
    "- **Rencana dulu**, kerjakan kemudian.",
    "- **Jangan render sendiri.** Kasih command.",
    "- Jangan `git commit` tanpa nanya.",
    "## Video baru",
    "Wajib pakai skill `mumeyong-video`.",
]


def aturan(v, T, s, e):
    ch = v.chapter(0, "ATURAN", s, e)
    L3 = T["L03"]
    prompt = "bikin CLAUDE.md, aturan kerja"
    t_type = L3.start + 0.1
    t_send = type_end(prompt, t_type) + 0.15
    t_card = t_send + 0.25
    t_focus = T.word("L04", "render")
    v.chat.show(s + 0.1)
    v.chat.chips([("CLAUDE.md", "green")], at=L3.start)
    v.chat.type(prompt, at=t_type)
    v.chat.send(at=t_send)
    head = Headline("Kasih *aturan* main.")

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, ch.kicker, ch.color)
        head.draw(c, t, L3.start, e - OUT)
        y, h = L["content_y"], 400

        def card(c):
            bx, by = window.frame(c, X, y, CW, h, "CLAUDE.md", "aturan kerja · root repo")
            reveal = [t_card + 0.25 + i * 0.1 for i in range(len(RULES_MD))]
            window.md_lines(c, bx, by, RULES_MD, t, reveal=reveal, focus=3, focus_t=t_focus, width=CW - 64)
        appear(c, t, t_card, e - OUT, (X, y, CW, h), card)
    v.add(s, e, draw)
    v.sfx("whoosh", s)
    v.sfx("pop", t_card)
    v.sfx("tick", t_focus)


# ── 01 · KODE ───────────────────────────────────────────────────────────
def kode(v, T, s, e):
    ch = v.chapter(1, "KODE", s, e)
    L5, L6 = T["L05"], T["L06"]
    t_frame, t_same = T.word("L05", "frame"), T.word("L06", "sama")
    prompt = "Setiap frame adalah fungsi dari waktu t."
    v.chat.chips([("CLAUDE.md", "green"), ("skill", "purple")], at=s + 0.2)
    v.chat.type(prompt, at=L5.start + 0.2)
    v.chat.send(at=type_end(prompt, L5.start + 0.2) + 0.1)
    head = Headline("Satu kalimat *kunci*.")
    formula = f'frame = <span foreground="{tk.hexs(C["accent"])}">f(t)</span>'
    thumbs = [(*tk.CHAPTER[i % 7][0][:3], 0.28) for i in range(8)]
    fy = L["content_y"] + 10
    sy = fy + 220
    ny = sy + 330

    def scrub(t):  # playhead position 0..1 while L06 is spoken
        return 0.15 + 0.7 * in_out_cubic(prog(t, L6.start, max(0.5, L6.dur)))

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, ch.kicker, ch.color)
        head.draw(c, t, L5.start, e - OUT)

        def eq(c):
            w = c.text(X + 16, fy + 70, formula, F["mono_med"], 68, c.theme("ink", "d_ink"), markup=True)
            select_box(c, t, t_frame + 0.3, X + 16, fy + 10, w, 78, "398 × 71")
        appear(c, t, t_frame, e - OUT, (X, fy, 600, 110), eq, rise=20)

        secs = 30 * scrub(t)
        appear(c, t, L6.start - 0.2, e - OUT, (X, sy, CW, 150),
               lambda c: filmstrip(c, X, sy, CW, 150, None, t, head=scrub(t),
                                   head_label=f"{fmt_id(secs, 1)} s", colors=thumbs))
        appear(c, t, L6.start, e - OUT, (X, ny - 90, 420, 150),
               lambda c: big_number(c, X + 10, ny, secs, t, t - 1, 1, " s", "WAKTU VIDEO",
                                    f"frame {fmt_id(int(secs * tk.FPS))}"))

        def ok(c):
            w = tag(c, X + 470, ny - 50, "diff 0 px · identik", C["ok"], h=44)
            icons.check(c, X + 470 + w + 26, ny - 28, 22, C["ok"], 3, p=out_expo(prog(t, t_same + 0.1, 0.4)))
        fade(c, t, t_same, e - OUT, ok)
    v.add(s, e, draw)
    v.sfx("whoosh", s)
    v.sfx("pop", t_frame)
    v.sfx("chime", t_same)


# ── RECAP (dark) ────────────────────────────────────────────────────────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    t_k, t_c = T.word("L07", "konteks"), T.word("L07", "cek")
    v.chat.hide(s)
    head = Headline("Intinya cuma *dua*.", style="headline_dark")
    rows = [(0, "ATURAN"), (1, "KODE")]
    rules = [("Kasih konteks", t_k, tk.CHAPTER[0][0], 0), ("Cek sendiri", t_c, tk.CHAPTER[4][0], 1)]
    y0, lw, rx, rw = 760, 330, X + 480, 368

    def draw(c, t):
        head.draw(c, t, s + 0.3, e - OUT)
        k = sum(1 for r in rules if t >= r[1])
        sy = head.bottom(c) + 34
        fade(c, t, s + 0.5, e - OUT, lambda c: segments(c, X, sy, len(rules), k))
        for i, (n, label) in enumerate(rows):
            act = max((out_expo(prog(t, r[1], 0.4)) for r in rules if r[3] == i), default=0.0)
            y = y0 + i * 90
            appear(c, t, s + 0.4 + i * 0.1, e - OUT, (X, y, lw, 62),
                   lambda c: step_row(c, X, y, lw, n, label, act))
        vis = 1 - in_cubic(prog(t, e - OUT, OUT))
        for j, (label, tr, col, ri) in enumerate(rules):
            y = y0 + j * 90
            fill = out_expo(prog(t, tr, 0.45))
            appear(c, t, s + 0.6 + j * 0.1, e - OUT, (rx, y, rw, 62),
                   lambda c: rule_box(c, rx, y, rw, j + 1, label, col, fill))
            p = in_out_cubic(prog(t, tr - 0.1, 0.5))
            if p > 0 and vis > 0:
                with c.group(vis):
                    connector(c, X + lw, y0 + ri * 90 + 31, rx, y + 31, p)
    v.add(s, e, draw)
    v.sfx("whoosh_dark", s)
    v.sfx("pop", t_k)
    v.sfx("pop", t_c)


# ── OUTRO (dark, centered) ──────────────────────────────────────────────
def outro(v, T, s, e):
    v.chapter(None, "OUTRO", s, e, dark=True)
    t_click = T.word("L08", "follow") + 0.5
    cx = tk.W / 2

    def draw(c, t):
        mumei_mark(c, cx - 20, 700, 110, p_enso=out_cubic(prog(t, s + 0.1, 1.0)), p_seal=prog(t, s + 1.0, 0.25),
                   flecks=prog(t, s + 0.9, 0.2), ink=C["d_ink"], paper=C["d_bg"])
        fade(c, t, s + 0.7, None,
             lambda c: c.text(cx, 950, tk.BRAND_NAME, F["display"], 92, C["d_ink"], 1, -0.05, align="c"))
        fade(c, t, s + 0.9, None,
             lambda c: c.text(cx, 1020, tk.TAGLINE, F["ui"], 34, C["d_ink"], 0.85, -0.02, align="c"))
        fade(c, t, s + 1.1, None, lambda c: follow_button(c, cx, 1070, t, t_click))

        def contact(c):
            c.text(cx, 1240, "Mau dibikinin video kayak gini?", F["ui"], 28, C["d_muted"], 1, align="c")
            contact_pill(c, cx, 1268, tk.CONTACT["site"], "SITUS")
        fade(c, t, t_click + 0.6, None, contact)
    v.add(s, e + 1, draw)
    v.track(Cursor([(s + 1.2, 900, 1500), (t_click, cx + 40, 1110)], clicks=[t_click], hide=t_click + 0.9))
    v.sfx("chime", t_click + 0.1)
