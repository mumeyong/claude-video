"""Paperwork components (first used in "bongkar-ep06-project-360").

lembar · stopmap · meja_cs · profile_360 · lapis · id_card
Signature move: sheets fly in from different counters and slip into one stopmap, which shuts "klik".
Pure functions of their progress values and t.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, out_expo, in_out_cubic

PURPLE = tk.CHAPTER[3][0]
WHITE = (1, 1, 1, 1)
# one color per data source (chapter palette, never the accent)
SOURCES = {"tabungan": tk.CHAPTER[4][0], "asuransi": tk.CHAPTER[1][0], "kredit": tk.CHAPTER[2][0],
           "sekuritas": tk.CHAPTER[0][0]}


def _person(c, x, base_y, s, color, alpha=1.0):
    """Seated/standing silhouette: head + shoulders, feet/seat at base_y, height s."""
    with c.group(alpha):
        c.fill_rrect(x - s * 0.24, base_y - s * 0.62, s * 0.48, s * 0.62, s * 0.2, color)
        c.circle(x, base_y - s * 0.8, s * 0.17, color)


# ── sheet ───────────────────────────────────────────────────────────────
def lembar(c, cx, cy, w, color, title="", rot=0.0, red=0.0, alpha=1.0, lines=4):
    """Paper sheet centered at (cx, cy), width w (A4-ish), colored stripe on top, rotated by rot."""
    h = w * 1.3
    x, y = cx - w / 2, cy - h / 2
    col = mix(color, tk.C["rec"], red)
    with c.at(0, 0, 1, origin=(cx, cy), rot=rot):
        with c.group(alpha):
            c.shadow(x, y, w, h, 6, 16, 6, 0.1)
            c.fill_rrect(x, y, w, h, 6, mix(c.theme("card", "d_card"), tk.C["rec"], 0.12 * red))
            c.fill_rrect(x, y, w, h * 0.13, 6, col)
            fs = max(17, w * 0.1)
            if title and c.measure(title.upper(), tk.F["mono_bold"], fs, 0.08)[0] < w * 0.84:   # only if it fits
                c.text(x + w * 0.1, y + h * 0.1, title.upper(), tk.F["mono_bold"], fs, WHITE, 1, 0.08)
            for k in range(lines):
                lw = w * (0.8 - 0.18 * ((k * 7) % 3) / 2)
                c.fill_rrect(x + w * 0.1, y + h * (0.27 + 0.13 * k), lw, max(4, h * 0.035), 3,
                             c.theme("faint", "d_line"))
            d = w * 0.18                                                     # dog-ear
            cxx = c.ctx
            cxx.new_path()
            cxx.move_to(x + w - d, y + h)
            cxx.line_to(x + w, y + h - d)
            cxx.line_to(x + w - d, y + h - d)
            cxx.close_path()
            c.src(c.theme("faint", "d_line"))
            cxx.fill()


# ── stopmap ─────────────────────────────────────────────────────────────
def stopmap(c, cx, cy, w, h, open_=0.0, pages=(), label="NASABAH", note_text=None, color=None, glow=0.0,
            alpha=1.0):
    """Snelhecter folder centered at (cx, cy). pages = list of colors (edges peek out on the right).
    open_ 0..1 swings the front cover to the left around the spine; glow 0..1 lights the tab."""
    color = color or PURPLE
    o = in_out_cubic(clamp(open_))
    x, y = cx - w / 2 + w * 0.5 * o, cy - h / 2          # slide right while opening: the open spread stays centred
    dark = mix(color, (0, 0, 0, 1), 0.18)
    with c.group(alpha):
        c.shadow(x, y, w, h, 12, 30, 12, 0.14, color)
        # tab
        tw = w * 0.42
        c.fill_rrect(x + w - tw - 10, y - 40, tw, 54, 10, mix(dark, WHITE, 0.25 * glow))
        c.text(x + w - tw / 2 - 10, y - 6, label, tk.F["mono_bold"], 18, WHITE, 1, 0.14, align="c")
        if glow > 0.01:
            c.stroke_rrect(x + w - tw - 14, y - 44, tw + 8, 62, 12, color, 3, glow)
        c.fill_rrect(x, y, w, h, 12, dark)                                   # back cover
        n = len(pages)
        for k, pc in enumerate(pages):                                       # page edges
            py = y + 26 + k * 10
            c.fill_rrect(x + 16, py, w - 22, h - 40 - k * 10, 6, c.theme("card", "d_card"))
            c.fill_rrect(x + w - 14, py + 20 + k * (h - 80) / max(1, n), 12, (h - 80) / max(1, n) - 6, 3, pc)
        # front cover: swings around the spine (left edge)
        sx = math.cos(o * math.pi)                                           # 1 → -1
        cw = w * abs(sx)
        fx = x if sx >= 0 else x - cw
        if cw > 2:
            front = color if sx >= 0 else mix(color, WHITE, 0.35)
            c.fill_rrect(fx, y, cw, h, 12, front)
            if sx > 0.3:
                c.fill_rrect(x + 18, y + h * 0.42, 12, h * 0.16, 4, mix(color, WHITE, 0.5))   # fastener
                c.fill_rrect(x + w * 0.22 * sx, y + h * 0.18, cw * 0.6, h * 0.16, 8, WHITE, 0.92)
                c.text(x + w * 0.22 * sx + 20, y + h * 0.18 + h * 0.11, "PROJECT 360", tk.F["mono_bold"],
                       max(17, w * 0.05), color, 1, 0.1)
        if note_text:
            c.text(x + w - 10, y + h + 52, note_text, tk.F["serif"], 36, c.theme("accent", "d_accent"), 1, align="r")


# ── CS desk ─────────────────────────────────────────────────────────────
def meja_cs(c, cx, base_y, w, t, screen=None, cs=True, customer=True, alpha=1.0):
    """CS desk scene, floor at base_y, width w. screen(c, sx, sy, sw, sh) draws the monitor contents."""
    ink2 = c.theme("ink2", "d_muted")
    dh = w * 0.06
    dy = base_y - w * 0.34
    mw, mh = w * 0.5, w * 0.34
    mx, my = cx - mw / 2, dy - mh - w * 0.07
    with c.group(alpha):
        if cs:
            _person(c, cx - w * 0.4, dy + 6, w * 0.26, ink2)
        # monitor
        c.fill_rrect(cx - 10, my + mh, 20, w * 0.07, 4, ink2)
        c.fill_rrect(cx - w * 0.07, dy - 10, w * 0.14, 10, 4, ink2)
        c.shadow(mx, my, mw, mh, 14, 28, 12, 0.12)
        c.fill_rrect(mx, my, mw, mh, 14, ink2)
        sx, sy, sw, sh = mx + 10, my + 10, mw - 20, mh - 20
        c.fill_rrect(sx, sy, sw, sh, 8, c.theme("bg", "d_bg"))
        if screen:
            with c.clip(sx, sy, sw, sh, 8):
                screen(c, sx, sy, sw, sh)
        # desk
        c.fill_rrect(cx - w / 2, dy, w, dh, 8, c.theme("card", "d_card"))
        c.stroke_rrect(cx - w / 2, dy, w, dh, 8, c.theme("line", "d_line"), 1.5)
        for lx in (cx - w * 0.44, cx + w * 0.4):
            c.fill_rrect(lx, dy + dh, w * 0.04, base_y - dy - dh, 4, c.theme("faint", "d_line"))
        if customer:
            px = cx + w * 0.42
            c.fill_rrect(px - w * 0.1, base_y - w * 0.2, w * 0.2, w * 0.03, 4, c.theme("faint", "d_line"))
            _person(c, px, base_y - w * 0.2, w * 0.26, c.theme("muted", "d_muted"))


def bubble(c, x, y, text, p=1.0, align="l", color=None, size=30):
    """Speech bubble with its tail at (x, y), body above it; p 0..1 pops it."""
    if p <= 0.01:
        return
    color = color or c.theme("card", "d_card")
    tw = c.measure(text, tk.F["ui_semi"], size, -0.01)[0]
    bw, bh = tw + 44, size * 1.9
    bx = x - 30 if align == "l" else x - bw + 30
    by = y - bh - 16
    with c.at(0, 0, 0.6 + 0.4 * out_expo(p), origin=(x, y)):
        with c.group(clamp(p * 2)):
            c.shadow(bx, by, bw, bh, bh / 2, 20, 8, 0.12)
            c.fill_rrect(bx, by, bw, bh, bh / 2, color)
            cxx = c.ctx
            cxx.new_path()
            cxx.move_to(x - 12, by + bh - 2)
            cxx.line_to(x, y)
            cxx.line_to(x + 12, by + bh - 2)
            cxx.close_path()
            c.src(color)
            cxx.fill()
            c.text(bx + 22, by + bh * 0.66, text, tk.F["ui_semi"], size, c.theme("ink", "d_ink"), 1, -0.01)
    return bx, by, bw, bh


# ── profile card ────────────────────────────────────────────────────────
def profile_360(c, x, y, w, h, t, ring=(1, 1, 1, 1), chips=None, live=0.0, name_bar=True, color=None,
                sources=("tabungan", "asuransi", "kredit", "sekuritas")):
    """Customer profile card: avatar with a 4-segment ring (one per source, each 0..1), censored name, chips."""
    color = color or PURPLE
    ink, muted = c.theme("ink", "d_ink"), c.theme("muted", "d_muted")
    c.card(x, y, w, h, r=26)
    r = min(h * 0.26, w * 0.13)
    ax, ay = x + 40 + r, y + 40 + r
    c.circle(ax, ay, r * 0.72, c.theme("faint", "d_line"))
    c.circle(ax, ay - r * 0.16, r * 0.24, c.theme("card", "d_card"))
    c.fill_rrect(ax - r * 0.38, ay + r * 0.12, r * 0.76, r * 0.4, r * 0.2, c.theme("card", "d_card"))
    cxx = c.ctx
    for k, src in enumerate(sources):
        p = clamp(ring[k] if k < len(ring) else 0)
        if p <= 0:
            continue
        a0 = -math.pi / 2 + k * math.pi / 2 + 0.06
        cxx.new_path()
        cxx.arc(ax, ay, r * 0.92, a0, a0 + (math.pi / 2 - 0.12) * p)
        c.src(SOURCES.get(src, color))
        cxx.set_line_width(r * 0.16)
        cxx.set_line_cap(1)
        cxx.stroke()
    tx = ax + r + 30
    c.text(tx, y + 62, "NASABAH", tk.F["mono_bold"], 18, muted, 1, 0.16)
    if name_bar:
        c.fill_rrect(tx, y + 80, min(260, x + w - tx - 30), 36, 6, ink)              # censored with a marker
    c.text(tx, y + 150, "360°", tk.F["display"], 44, color, 1, -0.03)
    if live > 0.01:
        pulse = 0.5 + 0.5 * math.sin(t * 6)
        lx = x + w - 120
        c.circle(lx, y + 56, 14 * (1 + 0.4 * pulse), tk.C["rec"], 0.2 * live)
        c.circle(lx, y + 56, 8, tk.C["rec"], live)
        c.text(lx + 20, y + 63, "LIVE", tk.F["mono_bold"], 18, tk.C["rec"], live, 0.14)
    if chips:
        cx_, cy_ = x + 40, ay + r + 36
        for lbl, a in chips:
            if a <= 0.01:
                continue
            col = SOURCES.get(lbl, color)
            cw = c.measure(lbl, tk.F["ui_semi"], 24, -0.01)[0] + 48
            if cx_ + cw > x + w - 30:
                cx_, cy_ = x + 40, cy_ + 62
            c.fill_rrect(cx_, cy_, cw, 48, 24, col, 0.14 * a)
            c.circle(cx_ + 20, cy_ + 24, 6, col, a)
            c.text(cx_ + 34, cy_ + 32, lbl, tk.F["ui_semi"], 24, col, a, -0.01)
            cx_ += cw + 12


# ── security rings ──────────────────────────────────────────────────────
def lapis(c, cx, cy, w, h, layers, gap=70, color=None):
    """Concentric rounded rings around a core box (w × h) at (cx, cy). layers (inner → outer):
    [{label, p (0..1 draw-on), thick (line width, default 4)}]."""
    color = color or PURPLE
    for k, ly in enumerate(layers):
        p = clamp(ly.get("p", 1.0))
        if p <= 0.01:
            continue
        pad = gap * (k + 1)
        x, y, ww, hh = cx - w / 2 - pad, cy - h / 2 - pad, w + 2 * pad, h + 2 * pad
        s = 0.94 + 0.06 * out_expo(p)
        with c.at(0, 0, s, origin=(cx, cy)):
            c.fill_rrect(x, y, ww, hh, 30 + pad * 0.3, (*color[:3], 0.035 * p))
            c.stroke_rrect(x, y, ww, hh, 30 + pad * 0.3, color, ly.get("thick", 4), p,
                           dash=None if ly.get("solid") else [18, 10])
            lbl = ly.get("label")
            if lbl:
                lw = c.measure(lbl, tk.F["mono_bold"], 18, 0.14)[0] + 28
                c.fill_rrect(x + 40, y - 17, lw, 34, 17, color, p)
                c.text(x + 54, y + 6, lbl, tk.F["mono_bold"], 18, WHITE, p, 0.14)


# ── employee card ───────────────────────────────────────────────────────
def id_card(c, cx, cy, s, tap=0.0, ok=0.0, name_bar=True, color=None, alpha=1.0):
    """Employee ID card (height s) on a lanyard, next to a reader on its right; tap 0..1 slides it onto the reader,
    ok 0..1 lights the reader green."""
    color = color or PURPLE
    w, h = s * 0.66, s
    rx = cx + s * 0.9
    p = in_out_cubic(clamp(tap))
    x = cx - w / 2 + (rx - cx - w * 0.1) * p
    y = cy - h / 2
    with c.group(alpha):
        # reader
        c.fill_rrect(rx - s * 0.06, cy - s * 0.45, s * 0.5, s * 0.9, 14, c.theme("ink2", "d_card"))
        led = mix(c.theme("faint", "d_line"), tk.C["ok"], clamp(ok))
        c.circle(rx + s * 0.19, cy - s * 0.3, s * 0.05, led)
        if ok > 0.01:
            c.circle(rx + s * 0.19, cy - s * 0.3, s * 0.12, tk.C["ok"], 0.25 * ok)
        # lanyard
        c.line(x + w / 2, y - s * 0.5, x + w / 2, y + 6, color, 6)
        # card
        c.shadow(x, y, w, h, 12, 18, 8, 0.14)
        c.fill_rrect(x, y, w, h, 12, c.theme("card", "d_card"))
        c.fill_rrect(x, y, w, h * 0.18, 12, color)
        c.fill_rrect(x + w * 0.42, y - 6, w * 0.16, 18, 6, mix(color, (0, 0, 0, 1), 0.3))
        c.fill_rrect(x + w * 0.25, y + h * 0.26, w * 0.5, h * 0.32, 8, c.theme("faint", "d_line"))
        c.circle(x + w / 2, y + h * 0.37, w * 0.1, c.theme("card", "d_card"))
        if name_bar:
            c.fill_rrect(x + w * 0.15, y + h * 0.68, w * 0.7, h * 0.07, 4, c.theme("ink", "d_ink"))
        c.text(x + w / 2, y + h * 0.88, "PEGAWAI", tk.F["mono_bold"], max(17, s * 0.07), color, 1, 0.12, align="c")
