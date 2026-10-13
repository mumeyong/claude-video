"""Payment-relay components (first used in "qris-dua-detik").

qr_code · qris_stand · es_teh · relay_track · slowmo_badge · mesh_hub
Signature move: freeze → slow-motion replay, the baton (the transaction message) handed from runner to runner.
Pure functions of their progress values and t; QR modules and jitter are hash-seeded.
"""
import math

from .. import tokens as tk
from ..ease import clamp, mix, out_expo, in_out_cubic, glide, pop
from .infra import _h

PURPLE = tk.CHAPTER[3][0]
OK_COLOR = tk.C["ok"]
WHITE = (1, 1, 1, 1)


# ── QR code + warung standee ────────────────────────────────────────────
def qr_code(c, x, y, s, seed=1, color=None, alpha=1.0, n=25, reveal=1.0):
    """Square QR-looking code at (x, y), size s: 3 finder patterns + hash-seeded modules. reveal 0..1 fills top→bottom."""
    color = color or c.theme("ink", "d_ink")
    m = s / n
    with c.group(alpha):
        c.fill_rrect(x - m, y - m, s + 2 * m, s + 2 * m, m, c.theme("card", "d_card"))
        rows = int(n * clamp(reveal) + 0.999)
        finders = ((0, 0), (n - 7, 0), (0, n - 7))
        for j in range(rows):
            for i in range(n):
                if any(fx <= i < fx + 7 and fy <= j < fy + 7 for fx, fy in finders):
                    continue
                if _h(i * 31 + j, seed) > 0.52:
                    c.fill_rrect(x + i * m, y + j * m, m * 0.92, m * 0.92, m * 0.15, color)
        for fx, fy in finders:
            if fy >= rows:
                continue
            c.fill_rrect(x + fx * m, y + fy * m, 7 * m, 7 * m, m * 0.8, color)
            c.fill_rrect(x + (fx + 1) * m, y + (fy + 1) * m, 5 * m, 5 * m, m * 0.5, c.theme("card", "d_card"))
            c.fill_rrect(x + (fx + 2) * m, y + (fy + 2) * m, 3 * m, 3 * m, m * 0.4, color)


def qris_stand(c, cx, base_y, s, seed=1, color=None, name="Warung Es Teh", alpha=1.0):
    """Acrylic QR standee on a counter: card (width s) with a header band, merchant name and the QR, on a foot."""
    color = color or PURPLE
    w, h = s, s * 1.42
    x, y = cx - w / 2, base_y - h - s * 0.08
    with c.group(alpha):
        c.fill_rrect(cx - w * 0.36, base_y - s * 0.1, w * 0.72, s * 0.1, s * 0.03, c.theme("faint", "d_line"))
        c.shadow(x, y, w, h, s * 0.06, 30, 12, 0.12)
        c.fill_rrect(x, y, w, h, s * 0.06, c.theme("card", "d_card"))
        c.fill_rrect(x, y, w, h * 0.16, s * 0.06, color)
        c.fill_rrect(x, y + h * 0.1, w, h * 0.06, 0, color)
        c.text(cx, y + h * 0.11, "QRIS", tk.F["display"], s * 0.13, WHITE, 1, -0.02, align="c")
        c.text(cx, y + h * 0.25, name, tk.F["ui_semi"], max(17, s * 0.075), c.theme("ink", "d_ink"), 1, -0.01,
               align="c")
        q = w * 0.7
        qr_code(c, cx - q / 2, y + h * 0.31, q, seed)
        c.text(cx, y + h * 0.95, "NMID · ID1020••••••", tk.F["mono_med"], max(17, s * 0.05),
               c.theme("muted", "d_muted"), 1, 0.04, align="c")
        # acrylic sheen
        c.line(x + w * 0.08, y + h * 0.2, x + w * 0.2, y + h * 0.08, WHITE, 3, 0.5)


def es_teh(c, cx, base_y, s, t=0.0, alpha=1.0):
    """Plastic cup of iced tea (height s) standing on base_y: amber tea, ice cubes, straw, condensation drops."""
    tea = mix(tk.CHAPTER[2][0], (0.45, 0.2, 0.05, 1), 0.25)
    w_top, w_bot, h = s * 0.62, s * 0.48, s
    xt, xb = cx - w_top / 2, cx - w_bot / 2
    top = base_y - h
    cx_ = c.ctx
    with c.group(alpha):
        c.line(cx + s * 0.1, top - s * 0.25, cx - s * 0.04, top + h * 0.7, mix(PURPLE, WHITE, 0.2), s * 0.06)
        lvl = top + h * 0.18
        cx_.new_path()
        cx_.move_to(xt + (w_top - w_bot) / 2 * 0.18, lvl)
        cx_.line_to(xt + w_top - (w_top - w_bot) / 2 * 0.18, lvl)
        cx_.line_to(xb + w_bot, base_y)
        cx_.line_to(xb, base_y)
        cx_.close_path()
        c.src(tea, 0.9)
        cx_.fill()
        for k in range(3):
            ix = cx - s * 0.18 + k * s * 0.13
            iy = lvl + s * 0.06 + (k % 2) * s * 0.1 + 2 * math.sin(t * 1.3 + k)
            c.fill_rrect(ix, iy, s * 0.14, s * 0.14, s * 0.03, WHITE, 0.55)
        cx_.new_path()
        cx_.move_to(xt, top)
        cx_.line_to(xt + w_top, top)
        cx_.line_to(xb + w_bot, base_y)
        cx_.line_to(xb, base_y)
        cx_.close_path()
        c.src(c.theme("ink2", "d_muted"), 0.5)
        cx_.set_line_width(3)
        cx_.stroke()
        for k in range(4):
            c.circle(xt + w_top * (0.2 + 0.2 * k), top + h * (0.35 + 0.15 * _h(k, 3)), s * 0.015, WHITE, 0.8)


# ── relay track ─────────────────────────────────────────────────────────
def relay_track(c, x, y, w, h, xs, labels, t, baton_x=None, lit=(), active=None, back=0.0, slow=0.0, color=None,
                draw=1.0, dim=()):
    """Horizontal running track (band x, y, w, h) with runner tokens at xs (numbered), labels under them.
    baton_x: where the baton is; lit[k] 0..1 = runner k has had the baton; back 0..1 = the reply pulse running
    right→left along the top lane; slow 0..1 adds motion-trail ghosts behind the baton (slow-motion);
    dim[k] 0..1 turns a runner red/slow (the lagging runner)."""
    color = color or PURPLE
    e = in_out_cubic(clamp(draw))
    with c.clip(x - 4, y - 200, (w + 8) * e, h + 400):
        c.fill_rrect(x, y, w, h, h / 2, mix(c.theme("bg", "d_bg"), color, 0.1))
        for k in (1, 2):
            ly = y + h * k / 3
            c.ctx.set_dash([18, 14])
            c.line(x + h / 2, ly, x + w - h / 2, ly, c.theme("card", "d_card"), 3, 0.9)
            c.ctx.set_dash([])
        # reply pulse along the upper lane, right → left
        if 0 < back < 1:
            bx = x + w - (w - h) * in_out_cubic(back) - h / 2
            for k in range(6):
                c.circle(bx + k * 22, y + h / 3, 9 - k, OK_COLOR, 0.9 - k * 0.14)
        r = h * 0.36
        for k, px in enumerate(xs):
            lk = clamp(lit[k]) if k < len(lit) else 0.0
            dk = clamp(dim[k]) if k < len(dim) else 0.0
            col = mix(mix(c.theme("faint", "d_line"), color, lk), tk.C["rec"], dk)
            if active == k:
                ph = (t * 0.9) % 1.0
                c.ctx.new_path()
                c.ctx.arc(px, y + h / 2, r + 4 + 22 * out_expo(ph), 0, 2 * math.pi)
                c.src(color, 0.5 * (1 - ph))
                c.ctx.set_line_width(3)
                c.ctx.stroke()
            c.shadow(px - r, y + h / 2 - r, 2 * r, 2 * r, r, 14, 6, 0.12)
            c.circle(px, y + h / 2, r, c.theme("card", "d_card"))
            c.circle(px, y + h / 2, r - 6, col)
            c.text(px, y + h / 2 + r * 0.32, str(k + 1), tk.F["display"], r * 0.9, WHITE, 1, -0.02, align="c")
            if k < len(labels):
                c.text(px, y + h + 40, labels[k], tk.F["mono_bold"], 18,
                       mix(c.theme("muted", "d_muted"), c.theme("ink", "d_ink"), lk), 1, 0.08, align="c")
        if baton_x is not None:
            by = y + h * 0.66
            for k in range(1, 4):
                if slow > 0:
                    _baton(c, baton_x - k * 26, by, h * 0.42, color, 0.25 * slow / k)
            _baton(c, baton_x, by, h * 0.42, color, 1.0)



def _baton(c, cx, cy, s, color, alpha):
    w, h = s * 1.5, s * 0.42
    c.fill_rrect(cx - w / 2, cy - h / 2, w, h, h / 2, color, alpha)
    c.fill_rrect(cx - w * 0.12, cy - h / 2, w * 0.24, h, 2, WHITE, 0.7 * alpha)


def slowmo_badge(c, x, y, t, speed="0,1×", tc="", frozen=0.0, alpha=1.0, align="r"):
    """Replay badge: '▶ 0,1×' (or '❚❚ TAHAN' when frozen) + a mono timecode. (x, y) = its right (or left) top."""
    if alpha <= 0.002:
        return
    label = "TAHAN" if frozen > 0.5 else f"REPLAY  {speed}"
    tw = c.measure(label, tk.F["mono_bold"], 20, 0.12)[0]
    cw = c.measure(tc, tk.F["mono_med"], 20, 0.02)[0] if tc else 0
    w = tw + cw + (110 if tc else 80)
    h = 52
    x0 = x - w if align == "r" else x
    with c.group(alpha):
        c.fill_rrect(x0, y, w, h, h / 2, (0.08, 0.09, 0.13, 1))
        ix, iy = x0 + 30, y + h / 2
        if frozen > 0.5:
            c.fill_rrect(ix - 9, iy - 10, 6, 20, 2, WHITE)
            c.fill_rrect(ix + 3, iy - 10, 6, 20, 2, WHITE)
        else:
            cx_ = c.ctx
            cx_.new_path()
            cx_.move_to(ix - 7, iy - 10)
            cx_.line_to(ix + 9, iy)
            cx_.line_to(ix - 7, iy + 10)
            cx_.close_path()
            c.src(tk.C["rec"])
            cx_.fill()
        c.text(ix + 26, y + h / 2 + 7, label, tk.F["mono_bold"], 20, WHITE, 1, 0.12)
        if tc:
            c.text(x0 + w - 24, y + h / 2 + 7, tc, tk.F["mono_med"], 20, mix(WHITE, PURPLE, 0.3), 1, 0.02, align="r")


# ── mesh vs hub (why switching exists) ──────────────────────────────────
def mesh_hub(c, cx, cy, r, t, n=6, p_mesh=1.0, p_hub=0.0, color=None, hub_label="switching", node_label="bank"):
    """n bank nodes on a circle. p_mesh draws every node-to-node line (the mess); p_hub fades the mesh out and
    grows spokes to a central hub with packets running on them."""
    color = color or PURPLE
    pts = [(cx + r * math.cos(-math.pi / 2 + 2 * math.pi * k / n), cy + r * math.sin(-math.pi / 2 + 2 * math.pi * k / n))
           for k in range(n)]
    mesh_a = clamp(p_mesh) * (1 - 0.85 * clamp(p_hub))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for q, (i, j) in enumerate(pairs):
        f = clamp((p_mesh * (len(pairs) + 3) - q) / 3)
        if f <= 0 or mesh_a <= 0:
            continue
        (ax, ay), (bx, by) = pts[i], pts[j]
        c.line(ax, ay, ax + (bx - ax) * f, ay + (by - ay) * f, c.theme("ink2", "d_muted"), 2, 0.55 * mesh_a)
    hp = glide(clamp(p_hub))
    if hp > 0:
        for k, (px, py) in enumerate(pts):
            c.line(cx, cy, cx + (px - cx) * hp, cy + (py - cy) * hp, color, 5)
            f = (t * 0.6 + k / n) % 1.0
            c.circle(cx + (px - cx) * f, cy + (py - cy) * f, 7, WHITE, hp * 0.9)
        hr = r * 0.32 * pop(clamp(p_hub), 1.6)
        c.shadow(cx - hr, cy - hr, 2 * hr, 2 * hr, hr, 24, 8, 0.25 * hp, color)
        c.circle(cx, cy, hr, color)
        c.text(cx, cy + 8, hub_label, tk.F["mono_bold"], max(17, r * 0.085), WHITE, hp, 0.04, align="c")
    for k, (px, py) in enumerate(pts):
        c.circle(px, py, r * 0.15, c.theme("card", "d_card"))
        c.stroke_rrect(px - r * 0.15, py - r * 0.15, r * 0.3, r * 0.3, r * 0.15, c.theme("ink2", "d_muted"), 3)
        c.text(px, py + 7, f"{node_label} {chr(65 + k)}", tk.F["mono_bold"], max(17, r * 0.06),
               c.theme("ink2", "d_muted"), 1, 0.02, align="c")
