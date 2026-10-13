"""Spring lab — proof sheet for STYLE §6h (springs, refs.pdf §08). Not for posting.

Split screen, the same move twice: left = the OLD easing (out_expo · out_back · keys()), right = the NEW one
(glide · pop · track() · indicator()). Under each panel a small plot of the curve with a dot riding it, so the
first-frame jolt of out_expo/out_back and the stop-and-go of keys() are visible even in a still.
The easing check in `check --dry` flags the LAMA side on purpose — that's the point of the lab.
"""
import math

from engine import Video, tokens as tk
from engine.ease import clamp, prog, out_expo, out_back, keys, glide, pop, track, indicator
from engine.components import Headline, kicker, fade, brand_intro, check_badge, arrive, dolly, cut

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW = L["col_x"], L["col_w"]
PRE_ROLL = 2.05
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 2.4
NAMES = ("INTRO", "01 · MASUK", "02 · POP", "03 · PINDAH", "04 · INDIKATOR", "OUTRO")
GAP = 20
PW = (CW - GAP) // 2                    # panel width (414)
PX = (X, X + PW + GAP)                  # left = LAMA, right = BARU
PY, PH = 560, 860                       # panel box
PLOT_Y, PLOT_H = PY + PH - 190, 130     # curve plot inside the panel


def build(project):
    T = project.timing
    v = Video(duration=T.line("L10").end + TAIL, bpm=90, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="ambient", key="D", mood="dreamy")
    v.sfx_kit = "glass"
    b = [max(0.0, T.chapter_span(n)[0] - LEAD) for n in NAMES] + [v.duration]
    b[0] = 0.0
    for i, fn in enumerate((intro, masuk, pop_ch, pindah, indikator, outro)):
        v.chapter(i if 0 < i < 5 else None, NAMES[i].split(" · ")[-1], b[i], b[i + 1])
        fn(v, T, b[i], b[i + 1], tk.CHAPTER[i][0] if 0 < i < 5 else C["accent"])
        if i:
            cut(v, b[i])
    v.cover_t = T["L03"].start + 1.0
    return v


# ── shared: two panels + a curve plot ─────────────────────────────────────────────────────────────────────────
def panels(c, t, t_in, t_out, old_name, new_name, col):
    """Both panel cards with their labels. Returns the panels' opacity (for the content inside)."""
    a = clamp((t - t_in) / 0.4) * (1 - clamp((t - t_out) / OUT))
    for k, (name, ink) in enumerate(((f"LAMA · {old_name}", C["muted"]), (f"BARU · {new_name}", col))):
        x = PX[k]
        c.card(x, PY, PW, PH, r=L["radius_bento"], alpha=a)
        c.text(x + 28, PY + 52, name, F["mono_med"], 22, ink, a, 0.04)
    return a


def plot(c, k, fn, p, a, col, lo=0.0, hi=1.15, dur=None, label=None):
    """Curve fn over 0..1 in panel k, with a dot at the current progress p. dur = window length (s) → footer shows
    how much of the move happens in the very first frame (the jolt)."""
    x0, w = PX[k] + 28, PW - 56
    y_of = lambda v: PLOT_Y + PLOT_H - (v - lo) / (hi - lo) * PLOT_H
    c.line(x0, y_of(1.0), x0 + w, y_of(1.0), C["ink2"], 1.5, a * 0.25)
    c.line(x0, y_of(0.0), x0 + w, y_of(0.0), C["ink2"], 1.5, a * 0.25)
    n = 60
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        c.line(x0 + u0 * w, y_of(fn(u0)), x0 + u1 * w, y_of(fn(u1)), col, 3, a * 0.8)
    pc = clamp(p)
    c.circle(x0 + pc * w, y_of(fn(pc)), 9, col, a)
    if dur:
        c.text(x0, PLOT_Y + PLOT_H + 40, "jalan di frame 1", F["mono_med"], 20, C["ink2"], a * 0.8, 0.04)
        c.text(x0 + w, PLOT_Y + PLOT_H + 40, f"{(fn(1 / 60 / dur) - fn(0)) * 100:.1f} %", F["mono_med"], 20, col, a,
               0.04, align="r")
    elif label:
        c.text(x0, PLOT_Y + PLOT_H + 40, label, F["mono_med"], 20, C["ink2"], a * 0.8, 0.04)


def head(text, y=330):
    return Headline(text, y=y, style="headline")


# ── INTRO ─────────────────────────────────────────────────────────────────────────────────────────────────────
def intro(v, T, s, e, col):
    L1 = T["L01"]
    h = Headline("Mulai dari\n*diam*.", y=720, style="headline_lg")

    def draw(c, t):
        kicker(c, t, s + 0.3, e - OUT, "SPRING LAB · STYLE §6h", col)
        h.draw(c, t, arrive(L1.start + 0.2), e - OUT, reveal="rise", exit="quiet")
        fade(c, t, T.word("L01", "kanan"), e - OUT, lambda c: c.text(
            X, 1080, "kiri = lama · kanan = baru", F["mono_med"], 28, C["ink2"], 1, 0.06))
    v.add(s, e, draw)
    dolly(v, T.word("L01", "baru"), e)


# ── 01 MASUK: three cards rise in, every 2.2 s — out_expo vs glide ────────────────────────────────────────────
def masuk(v, T, s, e, col):
    h = head("Masuk dari *diam*.")
    t0, P, D = T["L02"].start, 2.2, 0.7

    def card_stack(c, k, ease_fn, tl, a):
        for i in range(3):
            p = ease_fn(prog(tl, i * 0.1, D))
            y = PY + 110 + i * 150 + 90 * (1 - p)
            fade_out = 1 - clamp((tl - (P - 0.3)) / 0.3)
            al = a * min(1.0, p * 2.0) * fade_out
            c.card(PX[k] + 28, y, PW - 56, 120, r=L["radius_card"], alpha=al)
            c.fill_rrect(PX[k] + 52, y + 44, 120, 14, 7, C["ink2"], al * 0.5)
            c.fill_rrect(PX[k] + 52, y + 70, 200, 14, 7, C["ink2"], al * 0.3)

    def draw(c, t):
        kicker(c, t, s + 0.3, e - OUT, "01 · MASUK", col)
        h.draw(c, t, s + 0.4, e - OUT, reveal="rise", exit="quiet")
        a = panels(c, t, s + 0.5, e - OUT, "out_expo", "glide", col)
        if t >= t0:
            tl = (t - t0) % P
            for k, fn in enumerate((out_expo, glide)):
                card_stack(c, k, fn, tl, a)
                plot(c, k, fn, prog(tl, 0, D), a, (C["muted"], col)[k], dur=D)
    v.add(s, e, draw)
    t = t0
    while t < e - 0.5:
        v.sfx("tick", t, 0.25)
        t += P


# ── 02 POP: a check badge pops, every 1.8 s — out_back(1.8) vs pop(1.8) ───────────────────────────────────────
def pop_ch(v, T, s, e, col):
    h = head("Overshoot sama,\n*tanpa loncat*.")
    t0, P, D = T["L04"].start, 1.8, 0.6

    def draw(c, t):
        kicker(c, t, s + 0.3, e - OUT, "02 · POP", col)
        h.draw(c, t, s + 0.4, e - OUT, reveal="rise", exit="quiet")
        a = panels(c, t, s + 0.5, e - OUT, "out_back", "pop", col)
        if t >= t0:
            tl = (t - t0) % P
            fade_out = 1 - clamp((tl - (P - 0.25)) / 0.25)
            for k, fn in enumerate((lambda p: out_back(p, 1.8), lambda p: pop(p, 1.8))):
                p = prog(tl, 0, D)
                check_badge(c, PX[k] + PW / 2, PY + 330, 110, max(0.0, fn(p)) * fade_out * a)
                plot(c, k, fn, p, a, (C["muted"], col)[k], lo=0.0, hi=1.25, dur=D)
    v.add(s, e, draw)
    t = t0
    while t < e - 0.5:
        v.sfx("pop", t, 0.35)
        t += P


# ── 03 PINDAH: a dot visits 4 targets and comes home, every 3.6 s — keys() vs track() ─────────────────────────
def pindah(v, T, s, e, col):
    h = head("Pindah target,\n*tanpa berhenti*.")
    t0, P = T["L06"].start, 3.6
    pts = [(0.22, 0.25), (0.78, 0.30), (0.70, 0.75), (0.25, 0.65), (0.22, 0.25)]   # fractions of the stage box
    ts = [0.0, 0.55, 1.1, 1.65, 2.2]

    def at_old(tl):
        return keys(tl, [(tc, p) for tc, p in zip(ts, pts)])

    def at_new(tl):   # target changes at ts[i - 1]: the spring heads for pts[i] while keys() is still on its way
        return track(tl, [(-1.0, pts[0])] + [(tc, p) for tc, p in zip(ts[:-1], pts[1:])], "smooth")

    def stage(c, k, pos_at, tl, a, ink):
        x0, y0, w, hh = PX[k] + 28, PY + 100, PW - 56, 520
        for p in pts[:-1]:
            c.circle(x0 + p[0] * w, y0 + p[1] * hh, 14, C["ink2"], a * 0.18)
        n = 24
        for j in range(n, 0, -1):          # trail: the last 0.4 s of the path (spacing = speed)
            tt = tl - j * 0.4 / n
            if tt < 0:
                continue
            px, py = pos_at(tt)
            c.circle(x0 + px * w, y0 + py * hh, 4, ink, a * 0.5 * (1 - j / n))
        px, py = pos_at(tl)
        c.circle(x0 + px * w, y0 + py * hh, 18, ink, a)

    def draw(c, t):
        kicker(c, t, s + 0.3, e - OUT, "03 · PINDAH", col)
        h.draw(c, t, s + 0.4, e - OUT, reveal="rise", exit="quiet")
        a = panels(c, t, s + 0.5, e - OUT, "keys()", "track()", col)
        if t >= t0:
            tl = (t - t0) % P
            for k, pos_at in enumerate((at_old, at_new)):
                stage(c, k, pos_at, tl, a, (C["muted"], col)[k])
            def spd(f):   # 2-D speed over the first 2.6 s of the cycle, ~1 = fastest stretch
                return lambda u: min(1.15, math.hypot(*(q - r for q, r in zip(f(u * 2.6 + 0.01), f(u * 2.6)))) * 40)
            plot(c, 0, spd(at_old), tl / 2.6, a, C["muted"], label="kecepatan: 0 di tiap titik")
            plot(c, 1, spd(at_new), tl / 2.6, a, col, label="kecepatan: nggak pernah 0")
    v.add(s, e, draw)


# ── 04 INDIKATOR: a tab indicator visits tabs 0 → 2 → 1 → 3 → 0, every 4 s — keys() vs indicator() ──────────
def indikator(v, T, s, e, col):
    h = head("Ujung depan duluan,\nlalu *melar*.")
    t0, P = T["L08"].start, 4.0
    order, ts = (0, 2, 1, 3, 0), (0.0, 0.6, 1.4, 2.2, 3.0)

    def draw(c, t):
        kicker(c, t, s + 0.3, e - OUT, "04 · INDIKATOR", col)
        h.draw(c, t, s + 0.4, e - OUT, reveal="rise", exit="quiet")
        a = panels(c, t, s + 0.5, e - OUT, "keys()", "indicator()", col)
        if t < t0:
            return
        tl = (t - t0) % P
        for k in range(2):
            x0, w = PX[k] + 28, PW - 56
            tw = w / 4
            y = PY + 200
            c.fill_rrect(x0, y, w, 72, 36, C["ink2"], a * 0.08)
            left, right = spans(k, tl)
            ink = (C["muted"], col)[k]
            c.fill_rrect(left + 4, y + 6, right - left - 8, 60, 30, ink, a)
            for i in range(4):
                c.text(x0 + i * tw + tw / 2, y + 48, f"{i + 1}", F["mono_med"], 24, C["ink"], a * 0.8, 0.0, align="c")
            c.text(x0, y + 140, f"lebar {right - left:.0f} px", F["mono_med"], 22, ink, a, 0.04)
            wd = lambda u, k=k: (lambda lr: (lr[1] - lr[0]) / tw)(spans(k, u * 3.4))
            plot(c, k, wd, tl / 3.4, a, ink, lo=0.6, hi=2.2,
                 label=("lebar: tetap", "lebar: melar pas jalan")[k])
    v.add(s, e, draw)

    def spans(k, tl):
        x0, w = PX[k] + 28, PW - 56
        tw = w / 4
        xs = [x0 + i * tw for i in order]
        if k == 0:
            left = keys(tl, frames_old(xs))
            return left, left + tw
        return indicator(tl, [(-1.0, xs[0])] + list(zip(ts[1:], xs[1:])), tw)

    def frames_old(xs):
        fr = [(ts[0], xs[0])]
        for i in range(1, len(ts)):            # hold on the old tab until ts[i], move there in 0.45 s
            fr += [(ts[i], xs[i - 1]), (ts[i] + 0.45, xs[i])]
        return fr


# ── OUTRO ─────────────────────────────────────────────────────────────────────────────────────────────────────
def outro(v, T, s, e, col):
    L10 = T["L10"]
    h = Headline("Jangan pernah\n*nyentak*.", y=760)

    def draw(c, t):
        h.draw(c, t, arrive(L10.start + 0.2), None, reveal="rise")
        fade(c, t, T.word("L10", "nyentak") + 0.6, None, lambda c: c.text(
            X, 1120, "mumeyong.dev", F["mono_med"], 30, C["ink2"], 1, 0.08))
    v.add(s, e, draw)
    dolly(v, T.word("L10", "nyentak"), e)
