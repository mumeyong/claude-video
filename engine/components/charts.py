"""Data/explainer components: bill counter, cost chart, meters, seat grid, price bars, 24h timeline, block split.

All are drawn "at rest" from explicit progress values (0..1) the scene computes from time — no hidden state.
"""
import math

from .. import tokens as tk
from ..ease import clamp, lerp, mix, out_expo, in_out_cubic, glide, pop
from .motion import fmt_id


# ── bill counter ────────────────────────────────────────────────────────
def bill_counter(c, x, y, w, h, value, caption="", unit="/ bulan", prefix="$", sub="", sub_alpha=1.0,
                 size=150, card=True):
    """Big money number in a card: caption (mono) · '$14.000' + unit · optional sub line."""
    if card:
        c.card(x, y, w, h, r=28)
    pad = 44
    if caption:
        c.text(x + pad, y + 64, caption, tk.F["mono_med"], 19, c.theme("muted", "d_muted"), 1, 0.18)
    num = prefix + fmt_id(int(round(value)))
    base = y + 64 + size * 0.95
    nw = c.text(x + pad, base, num, tk.F["display"], size, c.theme("ink", "d_ink"), 1, -0.05)
    if unit:
        c.text(x + pad + nw + 18, base, unit, tk.F["ui"], 38, c.theme("muted", "d_muted"), 1, -0.01)
    if sub:
        c.text(x + pad, base + 74, sub, tk.F["display_semi"], 46, c.theme("accent", "d_accent"), sub_alpha, -0.03)


# ── cost chart ──────────────────────────────────────────────────────────
def _level(xf, drops, top=0.82):
    lv = top
    for (fx, amt, _label, p) in drops:
        s = clamp((xf - fx) / 0.035)
        lv -= amt * p * in_out_cubic(s)
    return lv


def cost_chart(c, x, y, w, h, t, draw=1.0, drops=(), leak=0.0, months=("Jan", "Apr", "Jul", "Okt"),
               caption="BIAYA CLOUD / BULAN", drip=10, line_w=6, labels_size=24):
    """Monthly cost line that steps down once per lever.

    drops: [(x_frac, amount_frac, label, p)] — p 0..1 animates each step down.
    draw: 0..1 how much of the line is drawn (left→right). leak: 0..1 strength of the red 'drip' dots.
    """
    c.card(x, y, w, h, r=24)
    px, py, pw, ph = x + 40, y + 80, w - 80, h - 140
    muted = c.theme("muted", "d_muted")
    c.text(x + 40, y + 52, caption, tk.F["mono_med"], 18, muted, 1, 0.18)
    for k in range(4):  # grid
        gy = py + ph * k / 3
        c.line(px, gy, px + pw, gy, c.theme("line", "d_line"), 1)
    for k, m in enumerate(months):
        c.text(px + pw * k / (len(months) - 1), y + h - 28, m, tk.F["mono"], 17, muted, 1, 0.05, align="c")
    if draw <= 0:
        return
    n = 140
    pts = []
    for i in range(int(n * draw) + 1):
        xf = i / n
        pts.append((px + pw * xf, py + ph * (1 - _level(xf, drops))))
    acc = c.theme("accent", "d_accent")
    cx = c.ctx
    # area
    cx.new_path()
    cx.move_to(pts[0][0], py + ph)
    for p in pts:
        cx.line_to(*p)
    cx.line_to(pts[-1][0], py + ph)
    cx.close_path()
    c.src(acc, 0.08)
    cx.fill()
    # line
    cx.new_path()
    for i, p in enumerate(pts):
        (cx.move_to if i == 0 else cx.line_to)(*p)
    c.src(acc)
    cx.set_line_width(line_w)
    cx.set_line_join(1)
    cx.stroke()
    c.circle(*pts[-1], 8, acc)
    # drop labels
    for (fx, amt, label, p) in drops:
        if p > 0.02 and label and fx <= draw:
            lx = px + pw * (fx + 0.02)
            ly = py + ph * (1 - _level(fx + 0.05, drops)) + 30
            c.text(lx, ly + 10 * (1 - p), label, tk.F["ui_semi"], labels_size, acc, p, -0.01)
    # leak drips
    if leak > 0:
        for k, fx in enumerate((0.22, 0.48, 0.74)):
            if fx > draw:
                continue
            ly = py + ph * (1 - _level(fx, drops))
            for j in range(2):
                ph_ = (t * 0.8 + k * 0.37 + j * 0.5) % 1.0
                c.circle(px + pw * fx, ly + 12 + ph_ * 200, drip * (1 - 0.35 * ph_), tk.C["rec"], leak * (1 - ph_))


# ── usage meter ─────────────────────────────────────────────────────────
def usage_meter(c, x, y, w, rows, row_h=110):
    """rows: [(label, fill 0..1, color, value_text, alpha)] — horizontal bars with big value on the right."""
    c.card(x, y, w, 60 + row_h * len(rows), r=24)
    for i, (label, fill, color, value, a) in enumerate(rows):
        if a <= 0.002:
            continue
        ry = y + 40 + i * row_h
        c.text(x + 40, ry + 26, label, tk.F["mono_med"], 20, c.theme("ink2", "d_muted"), a, 0.16)
        c.text(x + w - 40, ry + 34, value, tk.F["display"], 46, color, a, -0.04, align="r")
        bw = w - 80
        c.fill_rrect(x + 40, ry + 50, bw, 26, 13, c.theme("line", "d_line"), a)
        if fill > 0:
            c.fill_rrect(x + 40, ry + 50, max(26, bw * fill), 26, 13, color, a)


# ── seat grid (bus analogy) ─────────────────────────────────────────────
def seat_grid(c, x, y, cols, rows, t, p_in=1.0, filled=(0,), p_fill=1.0, keep=None, p_keep=0.0,
              seat=46, gap=14):
    """Bus: card with a windshield strip, seats popping in a wave. keep=k collapses to the first k seats."""
    n = cols * rows
    gw = cols * seat + (cols - 1) * gap
    gh = rows * seat + (rows - 1) * gap
    pad = 34
    # container shrinks with p_keep toward a k-seat 'car'
    if keep:
        kc = min(cols, keep)
        kr = math.ceil(keep / cols)
        kw = kc * seat + (kc - 1) * gap
        kh = kr * seat + (kr - 1) * gap
        gw_d, gh_d = lerp(gw, kw, p_keep), lerp(gh, kh, p_keep)
    else:
        gw_d, gh_d = gw, gh
    cw, ch = gw_d + 2 * pad, gh_d + 2 * pad + 30
    c.card(x, y, cw, ch, r=30)
    c.fill_rrect(x + pad, y + 18, gw_d, 16, 8, c.theme("accent_soft", "d_line"))  # windshield
    for wx in (x + cw * 0.22, x + cw * 0.78):
        c.circle(wx, y + ch + 2, 16, c.theme("ink2", "d_muted"))
    for i in range(n):
        r_, k_ = divmod(i, cols)
        wave = pop(clamp((p_in * (n + 10) - (r_ + k_) * 1.2) / 6))
        a = 1.0
        if keep and i >= keep:
            a *= 1 - p_keep
        if wave <= 0.01 or a <= 0.01:
            continue
        sx = x + pad + k_ * (seat + gap)
        sy = y + pad + 30 + r_ * (seat + gap)
        s = seat * wave
        col = c.theme("faint", "d_line")
        c.fill_rrect(sx + (seat - s) / 2, sy + (seat - s) / 2, s, s, 10, col, a)
        if i in filled and p_fill > 0:
            fs = s * pop(p_fill)
            c.fill_rrect(sx + (seat - fs) / 2, sy + (seat - fs) / 2, fs, fs, 10, c.theme("accent", "d_accent"), a)
    return cw, ch


# ── price bars ──────────────────────────────────────────────────────────
def price_bars(c, x, y, w, rows, bracket=0.0, bracket_label="beda jauh", row_h=124):
    """rows: [(label, length 0..1, color, tag, p)] — bars grow to length*p. bracket 0..1 draws a right bracket."""
    c.card(x, y, w, 40 + row_h * len(rows), r=24)
    bw = w - 80 - (150 if bracket > 0 else 0)
    for i, (label, length, color, tg, p) in enumerate(rows):
        if p <= 0.002:
            continue
        ry = y + 30 + i * row_h
        c.text(x + 40, ry + 34, label, tk.F["ui_semi"], 28, c.theme("ink", "d_ink"), glide(min(1, p * 2)), -0.02)
        c.fill_rrect(x + 40, ry + 54, bw, 40, 12, c.theme("line", "d_line"))
        L = bw * length * glide(p)
        if L > 2:
            c.fill_rrect(x + 40, ry + 54, max(24, L), 40, 12, color)
        if tg and p > 0.5:
            c.text(x + 40 + bw * length + 14 if length < 0.7 else x + 56, ry + 82, tg, tk.F["mono_med"], 18,
                   (1, 1, 1, 1) if length >= 0.7 else c.theme("muted", "d_muted"), (p - 0.5) * 2, 0.04)
    if bracket > 0:
        bx = x + w - 150
        y1, y2 = y + 30 + 54 + 20, y + 30 + (len(rows) - 1) * row_h + 54 + 20
        ym = lerp(y1, y2, 0.5)
        acc = c.theme("accent", "d_accent")
        p = glide(bracket)
        c.line(bx, ym - (ym - y1) * p, bx + 18, ym - (ym - y1) * p, acc, 3)
        c.line(bx + 18, ym - (ym - y1) * p, bx + 18, ym + (y2 - ym) * p, acc, 3)
        c.line(bx, ym + (y2 - ym) * p, bx + 18, ym + (y2 - ym) * p, acc, 3)
        c.text(bx + 34, ym + 8, bracket_label, tk.F["ui_semi"], 24, acc, p, -0.02)


# ── 24h timeline ────────────────────────────────────────────────────────
def day_timeline(c, x, y, w, rows, row_h=64, card=True):
    """rows: [(label, state(hour)->0..1, color)] — 24 cells per row, hour ticks below."""
    lab_w = 150
    h = 50 + row_h * len(rows) + 30
    if card:
        c.card(x, y, w, h, r=24)
    cw = (w - lab_w - 60) / 24
    for i, (label, state, color) in enumerate(rows):
        ry = y + 34 + i * row_h
        c.text(x + 34, ry + 30, label, tk.F["mono_med"], 18, c.theme("ink2", "d_muted"), 1, 0.12)
        for hr in range(24):
            s = clamp(state(hr))
            col = mix(c.theme("line", "d_line"), color, s)
            c.fill_rrect(x + lab_w + hr * cw + 1.5, ry + 6, cw - 3, row_h - 22, 5, col)
    for hr in (0, 6, 12, 18, 24):
        c.text(x + lab_w + hr * cw, y + h - 20, f"{hr:02d}", tk.F["mono"], 16, c.theme("muted", "d_muted"), 1,
               align="c")
    return h


# ── block split (monolith → services → serverless) ─────────────────────
def block_split(c, x, y, w, labels, p_split=0.0, moved=(), p_move=0.0, zone_label="serverless",
                big_label="monolith · 24/7", h=300, zone_h=150, glow=()):
    """One big block splits into a 2x3 grid; `moved` indices slide into a dashed zone below."""
    acc = c.theme("accent", "d_accent")
    soft = c.theme("accent_soft", "d_card")
    cols, rows_ = 3, 2
    gap = 22
    bw = (w - gap * (cols - 1)) / cols
    bh = (h - gap) / rows_
    zy = y + h + 50
    # dashed zone
    if moved:
        za = clamp(p_move * 3)
        c.stroke_rrect(x, zy, w, zone_h, 22, acc, 2, za, dash=[10, 8])
        c.text(x + 24, zy - 14, zone_label.upper(), tk.F["mono_med"], 18, acc, za, 0.18)
    # big block fades as it splits
    if p_split < 1:
        a = 1 - in_out_cubic(clamp(p_split * 1.4))
        c.card(x, y, w, h, r=26, color=soft, alpha=a)
        c.stroke_rrect(x, y, w, h, 26, acc, 2, a)
        c.text(x + w / 2, y + h / 2 + 16, big_label, tk.F["display_semi"], 48, acc, a, -0.03, align="c")
    if p_split <= 0:
        return
    zi = 0
    for i, label in enumerate(labels[: cols * rows_]):
        r_, k_ = divmod(i, cols)
        sx0, sy0 = x + k_ * (w / cols), y + r_ * (h / rows_)          # slice inside big block
        sw0, sh0 = w / cols, h / rows_
        sx1, sy1 = x + k_ * (bw + gap), y + r_ * (bh + gap)           # spaced grid
        sp = pop(clamp(p_split), 1.2)
        bx, by = lerp(sx0, sx1, sp), lerp(sy0, sy1, sp)
        bww, bhh = lerp(sw0, bw, sp), lerp(sh0, bh, sp)
        is_moved = i in moved
        if is_moved:
            mp = in_out_cubic(clamp(p_move))
            zw = (w - 48 - gap * 2) / 3
            tx, ty = x + 24 + zi * (zw + gap), zy + (zone_h - (zone_h - 40)) / 2
            bx, by = lerp(bx, tx, mp), lerp(by, ty, mp)
            bww, bhh = lerp(bww, zw, mp), lerp(bhh, zone_h - 40, mp)
            zi += 1
        a = clamp(p_split * 2)
        spin = ((i * 37) % 5 - 2) * 0.09 * math.sin(math.pi * clamp(p_split))  # tumble mid-flight, settle flat
        g = glow[zi - 1] if (is_moved and glow and zi - 1 < len(glow)) else 0.0
        with c.at(0, 0, 1 + 0.06 * g, origin=(bx + bww / 2, by + bhh / 2), rot=spin):
            if g > 0:
                c.shadow(bx, by, bww, bhh, 18, 26, 0, 0.55 * g, tk.C["ok"])
            c.card(bx, by, bww, bhh, r=18, shadow="card_tight", alpha=a)
            c.stroke_rrect(bx, by, bww, bhh, 18, tk.C["ok"] if g > 0.05 else acc, 1.5 + 1.5 * g,
                           a * max(g, 0.9 if is_moved and p_move > 0.5 else 0.35))
            c.text(bx + bww / 2, by + bhh / 2 + 9, label, tk.F["mono_med"], 26, c.theme("ink", "d_ink"), a, 0.02,
                   align="c")


# ── odometer (rolling digits) ───────────────────────────────────────────
def odometer(c, x, y, text, p, size, color, font=None, ls=-0.055, spins=2, stagger=0.09, align="l"):
    """Number whose digits roll up into place (rightmost first). y = baseline. p 0..1. Returns width."""
    font = font or tk.F["display"]
    total = c.measure(text, font, size, ls)[0]
    if align == "c":
        x -= total / 2
    elif align == "r":
        x -= total
    digits = [i for i, ch in enumerate(text) if ch.isdigit()]
    n = len(digits)
    line_h = size * 1.04
    for i, ch in enumerate(text):
        px = x + (c.measure(text[:i], font, size, ls)[0] if i else 0.0)
        if not ch.isdigit():
            c.text(px, y, ch, font, size, color, 1.0, ls)
            continue
        k = n - 1 - digits.index(i)  # 0 = rightmost
        pi = glide(clamp(p * (1 + stagger * n) - stagger * k))
        R = pi * (int(ch) + 10 * spins)
        d0, frac = int(R) % 10, R - int(R)
        cw = c.measure(ch, font, size, ls)[0] + size * 0.12
        with c.clip(px - size * 0.05, y - size * 0.98, cw, size * 1.22):
            c.text(px, y - frac * line_h, str(d0), font, size, color, 1.0, ls)
            if frac > 0.001:
                c.text(px, y + (1 - frac) * line_h, str((d0 + 1) % 10), font, size, color, 1.0, ls)
    return total


# ── 24h clock ring ──────────────────────────────────────────────────────
def clock24(c, cx, cy, r, state, color, width=56, marker=None, marker_p=0.0, center="", center_sub="",
            center_color=None, center_alpha=1.0):
    """Radial 24h ring (00 at top). state(hr)->0..1 lights each hour segment."""
    import cairo
    ctx = c.ctx
    gap = 0.018
    for hr in range(24):
        a0 = -math.pi / 2 + hr * 2 * math.pi / 24 + gap
        a1 = -math.pi / 2 + (hr + 1) * 2 * math.pi / 24 - gap
        col = mix(c.theme("line", "d_line"), color, clamp(state(hr)))
        ctx.new_path()
        ctx.arc(cx, cy, r, a0, a1)
        c.src(col)
        ctx.set_line_width(width)
        ctx.set_line_cap(cairo.LINE_CAP_BUTT)
        ctx.stroke()
    for hr in (0, 6, 12, 18):
        a = -math.pi / 2 + hr * 2 * math.pi / 24
        lx, ly = cx + math.cos(a) * (r + width / 2 + 34), cy + math.sin(a) * (r + width / 2 + 34)
        c.text(lx, ly + 8, f"{hr:02d}", tk.F["mono_med"], 22, c.theme("muted", "d_muted"), 1, 0.04, align="c")
    if marker is not None and marker_p > 0:
        a0 = -math.pi / 2 + marker * 2 * math.pi / 24
        a1 = a0 + 2 * math.pi / 24
        ctx.new_path()
        ctx.arc(cx, cy, r + width / 2 + 10, a0, a1)
        c.src(tk.C["rec"], marker_p)
        ctx.set_line_width(6)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        am = (a0 + a1) / 2
        moon(c, cx + math.cos(am) * (r + width / 2 + 54), cy + math.sin(am) * (r + width / 2 + 54), 16, marker_p)
    if center:
        c.text(cx, cy + 34, center, tk.F["display"], 120, center_color or c.theme("ink", "d_ink"), center_alpha,
               -0.05, align="c")
    if center_sub:
        c.text(cx, cy + 96, center_sub, tk.F["mono_med"], 24, c.theme("muted", "d_muted"), center_alpha, 0.12,
               align="c")


def moon(c, x, y, r, alpha=1.0):
    """Crescent glyph (no emoji)."""
    import cairo
    ctx = c.ctx
    ctx.save()
    ctx.push_group()
    c.circle(x, y, r, c.theme("ink2", "d_ink"))
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.new_path()
    ctx.arc(x + r * 0.55, y - r * 0.35, r * 0.85, 0, 2 * math.pi)
    ctx.fill()
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(alpha)
    ctx.restore()


# ── receipt ─────────────────────────────────────────────────────────────
def receipt(c, x, y, w, lines, title="TAGIHAN CLOUD", sub="per bulan", row_h=96):
    """Paper receipt that grows as lines print.

    lines: [(label, value, p_print 0..1, p_strike 0..1, value_color or None)]
    Returns the current paper height.
    """
    head_h, foot_h = 150, 70
    n = sum(clamp(ln[2]) for ln in lines)
    h = head_h + row_h * n + foot_h
    ctx = c.ctx
    # paper with zig-zag bottom
    c.shadow(x, y, w, h, 6, 30, 14, 0.10)
    ctx.new_path()
    ctx.move_to(x, y)
    ctx.line_to(x + w, y)
    ctx.line_to(x + w, y + h)
    teeth = int(w // 26)
    for k in range(teeth, -1, -1):
        tx = x + w * k / teeth
        ctx.line_to(tx, y + h - (12 if k % 2 else 0))
    ctx.close_path()
    c.src(c.theme("card", "d_card"))
    ctx.fill()
    ink = c.theme("ink", "d_ink")
    muted = c.theme("muted", "d_muted")
    c.text(x + w / 2, y + 62, title, tk.F["mono_bold"], 26, ink, 1, 0.2, align="c")
    c.text(x + w / 2, y + 98, sub, tk.F["mono"], 19, muted, 1, 0.1, align="c")
    _dash(c, x + 30, y + 128, x + w - 30, muted)
    yy = y + head_h
    for (label, value, pp, ps, vcol) in lines:
        pp = clamp(pp)
        if pp <= 0.01:
            continue
        a = glide(pp)
        base = yy + row_h * 0.55
        c.text(x + 36, base, label, tk.F["ui_semi"], 32, ink, a, -0.02)
        c.text(x + w - 36, base, value, tk.F["mono_bold"], 34, vcol or ink, a, 0.06, align="r")
        if ps > 0:
            sw = (w - 60) * glide(ps)
            c.line(x + 28, base - 11, x + 28 + sw, base - 11, tk.C["rec"], 5)
        yy += row_h * pp
    _dash(c, x + 30, y + h - foot_h + 14, x + w - 30, muted)
    return h


def _dash(c, x1, y, x2, color):
    c.ctx.new_path()
    c.ctx.move_to(x1, y)
    c.ctx.line_to(x2, y)
    c.src(color, 0.6)
    c.ctx.set_line_width(2)
    c.ctx.set_dash([8, 8])
    c.ctx.stroke()
    c.ctx.set_dash([])


def stamp(c, cx, cy, text, p, color=None, rot=-0.22, size=78):
    """Rubber stamp that slams in (scale 1.7→1) — 'HEMAT', '≈ Rp 200+ juta'."""
    if p <= 0:
        return
    color = color or c.theme("accent", "d_accent")
    s = 1 + 0.7 * (1 - out_expo(p))
    tw = c.measure(text, tk.F["display"], size, -0.03)[0]
    w, h = tw + 64, size * 1.25
    with c.at(0, 0, s, origin=(cx, cy), rot=rot):
        with c.group(clamp(p * 3) * 0.92):
            c.stroke_rrect(cx - w / 2, cy - h / 2, w, h, 16, color, 7)
            c.text(cx, cy + size * 0.36, text, tk.F["display"], size, color, 1, -0.03, align="c")


# ── hand note (serif italic annotation + arrow) ─────────────────────────
def note(c, x, y, text, p, arrow_to=None, color=None, size=None, align="l"):
    """Blue Instrument Serif italic note; optional curved arrow from the note toward arrow_to=(x, y)."""
    if p <= 0:
        return
    color = color or c.theme("accent", "d_accent")
    size = size or tk.T["note"][0]
    lines = text.split("\n")
    a = glide(clamp(p * 2))
    for i, ln in enumerate(lines):
        c.text(x, y + i * size * 1.05, ln, tk.F["serif"], size, color, a, 0.0, align=align)
    if arrow_to:
        from .motion import bezier_partial
        sx, sy = x - 12 if align == "l" else x + 12, y - size * 0.3
        tx, ty = arrow_to
        cp1 = (sx - 60 if align == "l" else sx + 60, sy - 20)
        cp2 = (tx + (40 if tx < sx else -40), ty - 50)
        pa = in_out_cubic(clamp((p - 0.2) / 0.8))
        if pa > 0:
            bezier_partial(c, (sx, sy), cp1, cp2, (tx, ty), pa)
            c.src(color, 0.9)
            c.ctx.set_line_width(3)
            c.ctx.set_line_cap(1)
            c.ctx.stroke()
            if pa > 0.95:
                from .motion import bezier_point
                bx, by = bezier_point((sx, sy), cp1, cp2, (tx, ty), 0.93)
                ang = math.atan2(ty - by, tx - bx)
                for da in (2.6, -2.6):
                    c.line(tx, ty, tx + 18 * math.cos(ang + da), ty + 18 * math.sin(ang + da), color, 3)


def chart_point(x, y, w, h, drops, xf):
    """Screen point on cost_chart's line at x fraction xf (same geometry as cost_chart)."""
    px, py, pw, ph = x + 40, y + 80, w - 80, h - 140
    return px + pw * xf, py + ph * (1 - _level(xf, drops))
