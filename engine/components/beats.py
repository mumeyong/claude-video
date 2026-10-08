"""Small recurring beats every video uses — import these instead of re-defining them in scenes.py.

pop_tag · tag_center · check_badge · series_outro
"""
from .. import tokens as tk
from ..ease import prog, out_back, out_cubic, clamp
from .pill import tag
from .motion import appear, fade
from .recap import follow_button
from .widgets import Cursor
from . import icons


def pop_tag(c, t, t0, x, y, label, color, h=44, align="l"):
    """Tag that pops in at t0 (scale overshoot). align='r' anchors its right edge at x."""
    if t < t0:
        return
    p = out_back(prog(t, t0, 0.4), 1.6)
    with c.at(0, 0, max(0.01, p), origin=(x, y + h / 2)):
        tag(c, x, y, label, color, clamp(p * 2), align=align, h=h)


def tag_center(c, cx, y, label, color, alpha=1.0, h=44):
    """Tag centered on cx."""
    w = c.measure(label, tk.F["ui"], tk.T["tag"][0], tk.T["tag"][1])[0] + 30
    tag(c, cx - w / 2, y, label, color, alpha, h=h)


def check_badge(c, x, y, r, p):
    """Green ✓ disc at (x, y), radius r, scaled by p (0..1, use out_back for a pop)."""
    if p <= 0.01:
        return
    with c.at(0, 0, max(0.01, p), origin=(x, y)):
        c.circle(x, y, r, tk.C["ok"])
        icons.check(c, x, y, r * 0.85, (1, 1, 1, 1), 3.5)


def series_outro(v, T, s, e, teaser_id, follow_id, kicker, title, sub, color, series="Seri Bongkar Arsitektur"):
    """Dark outro for a series episode: logo + brand, 'next episode' teaser card at teaser_id, + Follow click at the
    word 'follow' in follow_id, series name under the button."""
    X, CW, MID, C, F = tk.L["col_x"], tk.L["col_w"], tk.W / 2, tk.C, tk.F
    v.chapter(None, "OUTRO", s, e, dark=True)
    Lt, Lf = T[teaser_id], T[follow_id]
    t_click = T.word(follow_id, "follow") + 0.4

    def draw(c, t):
        icons.play_logo(c, MID, 560, 90, C["d_ink"], p=out_cubic(prog(t, s + 0.1, 1.0)))
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 740, tk.BRAND_NAME, F["display"], 80, C["d_ink"], 1, -0.05, align="c"))

        def teaser(c):
            c.card(X, 830, CW, 220, r=28)
            c.fill_rrect(X, 830, 14, 220, 7, color)
            c.text(X + 50, 892, kicker, F["mono_bold"], 20, color, 1, 0.16)
            c.text(X + 50, 962, title, F["display_semi"], 50, C["d_ink"], 1, -0.03)
            c.text(X + 50, 1016, sub, F["ui"], 34, C["d_muted"], 1, -0.01)
        appear(c, t, Lt.start, None, (X, 830, CW, 220), teaser)
        fade(c, t, Lf.start, None, lambda c: follow_button(c, MID, 1120, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, 1260, series, F["ui"], 28, C["d_muted"], 1, align="c"))
    v.add(s, e + 1, draw)
    v.track(Cursor([(Lf.start - 0.2, 860, 1450), (t_click, MID + 40, 1160)], clicks=[t_click], hide=t_click + 1.0))
    v.sfx("pop", Lt.start, 0.5)
    v.sfx("chime", t_click + 0.1)


# ── added 2026-10-08: less boilerplate per video (new videos only) ──────
def heads(T, items, end, style="headline"):
    """Headlines that hand over line to line. items = [("Teks *aksen*.", "L04"), ("Lagi.", "L05", "L06"), …]:
    each starts at its line and ends just before the next item's line (or at `end` for the last one).
    Returns [(Headline, t_in, t_out)] for draw_heads()."""
    from .headline import Headline
    out = []
    for i, it in enumerate(items):
        text, a = it[0], it[1]
        if len(it) > 2 and it[2]:
            t_out = T[it[2]].start - 0.15
        elif i + 1 < len(items):
            t_out = T[items[i + 1][1]].start - 0.15
        else:
            t_out = end
        out.append((Headline(text, style=style), T[a].start, t_out))
    return out


def draw_heads(c, t, hs):
    for h, a, b in hs:
        h.draw(c, t, a, b)


def punch_word(c, t, t_in, t_word, word, color, caption=None, y=1100, size=150):
    """Intro punch: a small mono caption at t_in, then one giant word slams in at t_word (auto-fits the column)."""
    X, CW, MID, F = tk.L["col_x"], tk.L["col_w"], tk.W / 2, tk.F
    from ..ease import out_expo
    if caption:
        a0 = out_expo(prog(t, t_in, 0.4))
        c.text(MID, y - 260, caption, F["mono_med"], 32, c.theme("ink2", "d_muted"), a0, 0.06, align="c")
        c.line(MID, y - 220, MID, y - 220 + 70 * a0, c.theme("faint", "d_line"), 4)
    p = prog(t, t_word, 0.35)
    size = min(size, size * CW / c.measure(word, F["display"], size, -0.06)[0])
    with c.at(0, 0, 1 + 0.5 * (1 - out_expo(p)), origin=(MID, y - 40)):
        c.text(MID, y, word, F["display"], size, color, clamp(p * 3), -0.06, align="c")


def standard_outro(v, T, s, e, follow_id, color, teaser=None, save_id=None, contact="mumeyong.dev"):
    """Dark outro: brushed mumei mark + brand → optional teaser card {kicker, title, sub} → optional Save click (at
    the word 'save' in save_id) → Follow click (word 'follow' in follow_id) → contact line."""
    from .brand import mumei_mark
    from .transit import save_button
    X, CW, MID, C, F = tk.L["col_x"], tk.L["col_w"], tk.W / 2, tk.C, tk.F
    v.chapter(None, "OUTRO", s, e, dark=True)
    Lf = T[follow_id]
    t_click = T.word(follow_id, "follow") + 0.4
    t_save = T.word(save_id, "save") + 0.3 if save_id else None
    y_btn = 1170 if save_id else 1120

    def draw(c, t):
        mumei_mark(c, MID - 14, 500, 72, p_enso=out_cubic(prog(t, s + 0.1, 0.9)), p_seal=prog(t, s + 0.9, 0.25),
                   flecks=prog(t, s + 0.8, 0.2), ink=C["d_ink"], paper=C["d_bg"])
        fade(c, t, s + 0.5, None,
             lambda c: c.text(MID, 690, tk.BRAND_NAME, F["display"], 76, C["d_ink"], 1, -0.05, align="c"))
        if teaser:
            def card(c):
                c.card(X, 780, CW, 220, r=28)
                c.fill_rrect(X, 780, 14, 220, 7, color)
                c.text(X + 50, 842, teaser["kicker"], F["mono_bold"], 20, color, 1, 0.16)
                c.text(X + 50, 912, teaser["title"], F["display_semi"], 50, C["d_ink"], 1, -0.03)
                c.text(X + 50, 966, teaser.get("sub", ""), F["ui"], 32, C["d_muted"], 1, -0.01)
            appear(c, t, s + 0.3, None, (X, 780, CW, 220), card)
        if save_id:
            fade(c, t, T[save_id].start, None, lambda c: save_button(c, MID, 1060, t, t_save, color=color))
        fade(c, t, Lf.start, None, lambda c: follow_button(c, MID, y_btn, t, t_click))
        fade(c, t, t_click + 0.5, None, lambda c: c.text(MID, y_btn + 140, contact, F["mono_med"], 28, C["d_muted"],
                                                          1, 0.06, align="c"))
    v.add(s, e + 1, draw)
    pts = [((T[save_id] if save_id else Lf).start - 0.2, 860, 1450)]
    clicks = [t_click]
    if save_id:
        pts.append((t_save, MID + 40, 1096))
        clicks.insert(0, t_save)
    pts += [(Lf.start, MID + 70, y_btn + 110), (t_click, MID + 40, y_btn + 36)]
    v.track(Cursor(pts, clicks=clicks, hide=t_click + 1.0))
    if teaser:
        v.sfx("pop", s + 0.3, 0.4)
    if save_id:
        v.sfx("click", t_save, 0.7)
        v.sfx("chime", t_save + 0.1, 0.6)
    v.sfx("chime", t_click + 0.1)
