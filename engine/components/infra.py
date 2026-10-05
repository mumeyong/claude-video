"""Infrastructure explainer components (first used in Bongkar Arsitektur EP01).

particle_flow · toll_plaza (+ booth, car) · arch_diagram · load_graph · stack_layers
All pure: drawn from explicit progress values / time; randomness is hash-seeded.
"""
import math

from .. import tokens as tk
from ..ease import clamp, lerp, mix, out_expo, out_back, in_out_cubic
from .motion import bezier_point

PURPLE = tk.CHAPTER[3][0]


def _h(i, seed=0):
    x = math.sin(i * 12.9898 + seed * 78.233) * 43758.5453
    return x - math.floor(x)


# ── particle flow ───────────────────────────────────────────────────────
def particle_flow(c, t, target, n=300, density=1.0, speed=0.35, jam=0.0, red=0.0, seed=1,
                  spawn=(-80, -120, tk.W + 160, 360), color=None, size=(5, 10), spread=40):
    """Request dots streaming from `spawn` (rect) toward `target` (x, y).

    jam 0..1: particles slow down and pile up short of the target. red 0..1: tint toward failure red.
    """
    color = mix(color or c.theme("accent", "d_accent"), tk.C["rec"], red)
    tx, ty = target
    sx0, sy0, sw, sh = spawn
    m = int(n * clamp(density))
    stop = 1 - 0.38 * jam
    for i in range(m):
        u = _h(i, seed)
        sp = speed * (0.6 + 0.8 * _h(i, seed + 3)) * (1 - 0.75 * jam)
        ph = (t * sp + u) % 1.0
        ph_e = min(ph, stop) ** 1.6
        start = (sx0 + sw * _h(i, seed + 1), sy0 + sh * _h(i, seed + 2))
        if _h(i, seed + 9) < 0.35:  # some come from the sides / bottom
            side = _h(i, seed + 10)
            start = (-60 if side < 0.5 else tk.W + 60, tk.H * (0.2 + 0.7 * _h(i, seed + 4)))
        end = (tx + (_h(i, seed + 5) - 0.5) * spread * (1 + 3 * jam), ty + (_h(i, seed + 6) - 0.5) * spread * (1 + 3 * jam))
        mid = ((start[0] + end[0]) / 2 + (_h(i, seed + 7) - 0.5) * 300, (start[1] + end[1]) / 2)
        x, y = bezier_point(start, mid, mid, end, ph_e)
        a = clamp(ph / 0.08) * (1 - clamp((ph - 0.9) / 0.1) if jam < 0.5 else 1.0)
        r = lerp(size[0], size[1], _h(i, seed + 8))
        c.circle(x, y, r, color, 0.85 * a)


# ── toll plaza (top-down) ───────────────────────────────────────────────
def car(c, cx, cy, color=None, alpha=1.0, rot=0.0, w=34, h=52):
    color = color or c.theme("ink2", "d_muted")
    with c.at(0, 0, 1.0, origin=(cx, cy), rot=rot):
        c.fill_rrect(cx - w / 2, cy - h / 2, w, h, 9, color, alpha)
        c.fill_rrect(cx - w / 2 + 5, cy - h / 2 + 9, w - 10, 12, 4, (1, 1, 1, 1), 0.55 * alpha)


def booth(c, cx, cy, w=70, h=46, open_p=1.0, color=None, state="ok", alpha=1.0):
    """Top-down toll booth: purple box + barrier arm (raised when open). state: ok / idle / red."""
    color = {"ok": color or PURPLE, "idle": c.theme("faint", "d_line"), "red": tk.C["rec"]}[state]
    s = out_back(clamp(open_p), 1.6) if open_p < 1 else 1.0
    with c.at(0, 0, max(0.01, s), origin=(cx, cy)):
        c.shadow(cx - w / 2, cy - h / 2, w, h, 10, 14, 6, 0.12 * alpha)
        c.fill_rrect(cx - w / 2, cy - h / 2, w, h, 10, color, alpha)
        c.fill_rrect(cx - w / 2 + 8, cy - 5, w - 16, 10, 5, (1, 1, 1, 1), 0.5 * alpha)
        arm = -0.9 * clamp(open_p) if state != "idle" else 0.0
        ax, ay = cx + w / 2 + 4, cy + h / 2 + 6
        c.ctx.save()
        c.ctx.translate(ax, ay)
        c.ctx.rotate(arm)
        c.line(0, 0, 54, 0, tk.C["rec"] if state != "ok" else c.theme("ink2", "d_muted"), 5, alpha)
        c.ctx.restore()


def toll_plaza(c, x, y, w, h, t, booths, flow=1.0, queue=0.0, uturns=0.0, uturn_n=3, seed=2, booth_line=0.6):
    """Top-down plaza. booths: [(x_frac, open_p, state)]. queue 0..1 stacks cars before the booths.

    uturns 0..1: the last cars of the queue swing out and drive back up (red). Returns booth line y.
    """
    c.card(x, y, w, h, r=30)
    yb = y + h * booth_line
    road = c.theme("line", "d_line")
    c.fill_rrect(x + 24, y + 24, w - 48, h - 48, 22, road, 0.5)
    n = len(booths)
    # lane dashes
    for i, (fx, op, st) in enumerate(booths):
        lx = x + w * fx
        for k in range(int((h - 60) / 44)):
            yy = y + 36 + k * 44 + (t * 120 * flow) % 44
            if abs(yy - yb) > 40:
                c.line(lx, yy, lx, yy + 18, (1, 1, 1, 1), 3, 0.7)
    spacing = w / max(1, n)
    bw = min(70, spacing * 0.62)
    qlen = queue * (yb - y - 80)
    lane_open = [op > 0.5 and st == "ok" for (_, op, st) in booths]
    for i, (fx, op, st) in enumerate(booths):
        lx = x + w * fx
        # queued cars (static stack with tiny breathing)
        nq = int(qlen / 58)
        for j in range(nq):
            cy = yb - 50 - j * 58 + math.sin(t * 3 + j + i) * 1.5
            car(c, lx, cy, c.theme("ink2", "d_muted"), 0.85)
        # flowing cars above the queue
        m = 4
        top, bot = y + 40, yb - 50 - nq * 58
        for k in range(m):
            ph = (t * 0.45 * flow + k / m + _h(i, seed) * 0.5) % 1.0
            cy = top + (bot - top) * ph
            if bot - top > 40 and flow > 0.01:
                car(c, lx, cy, c.theme("muted", "d_muted"), clamp(ph / 0.15) * clamp(flow * 2))
        # cars leaving below an open booth
        if lane_open[i] and flow > 0.01:
            for k in range(2):
                ph = (t * 0.6 * flow + k / 2 + _h(i, seed + 5)) % 1.0
                cy = yb + 50 + (y + h - 60 - yb - 50) * ph
                car(c, lx, cy, c.theme("muted", "d_muted"), (1 - ph) * clamp(flow * 2))
        booth(c, lx, yb, bw, 46, op, state=st)
    # U-turning cars (red), from the tail of the queue of the middle lanes
    if uturns > 0:
        for k in range(uturn_n):
            i = (k * 2 + 1) % n
            lx = x + w * booths[i][0]
            yq = yb - 50 - max(1, int(qlen / 58)) * 58
            p = clamp((uturns - k * 0.18) / 0.6)
            if p <= 0:
                continue
            side = 1 if lx < x + w * 0.8 else -1
            p0, p1, p2, p3 = (lx, yq), (lx + side * 90, yq + 30), (lx + side * 150, yq - 120), (lx + side * 110, y + 60)
            pe = in_out_cubic(p)
            bx, by = bezier_point(p0, p1, p2, p3, pe)
            bx2, by2 = bezier_point(p0, p1, p2, p3, min(1, pe + 0.02))
            rot = math.atan2(by2 - by, bx2 - bx) - math.pi / 2
            c.ctx.save()
            from .motion import bezier_partial
            bezier_partial(c, p0, p1, p2, p3, pe)
            c.src(tk.C["rec"], 0.35)
            c.ctx.set_line_width(3)
            c.ctx.set_dash([8, 8])
            c.ctx.stroke()
            c.ctx.set_dash([])
            c.ctx.restore()
            car(c, bx, by, tk.C["rec"], 1.0, rot)
    return yb


# ── architecture diagram ────────────────────────────────────────────────
def _elbow(a, b):
    ax, ay = a
    bx, by = b
    my = (ay + by) / 2
    return [(ax, ay), (ax, my), (bx, my), (bx, by)]


def _along(pts, f):
    segs = [math.dist(p, q) for p, q in zip(pts, pts[1:])]
    total = sum(segs) or 1
    d = total * clamp(f)
    for (p, q), L in zip(zip(pts, pts[1:]), segs):
        if d <= L:
            u = d / L if L else 0
            return p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u
        d -= L
    return pts[-1]


def _draw_poly(c, pts, f, color, width=3, alpha=1.0):
    if f <= 0:
        return
    segs = [math.dist(p, q) for p, q in zip(pts, pts[1:])]
    total = sum(segs) or 1
    d = total * clamp(f)
    cx = c.ctx
    cx.new_path()
    cx.move_to(*pts[0])
    for (p, q), L in zip(zip(pts, pts[1:]), segs):
        if d >= L:
            cx.line_to(*q)
            d -= L
        else:
            u = d / L if L else 0
            cx.line_to(p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)
            break
    c.src(color, alpha)
    cx.set_line_width(width)
    cx.set_line_join(1)
    cx.stroke()


def arch_node(c, nd):
    """Draw one node dict: {x, y, w, h, kind, label, a, s, state, sub}."""
    a, s = nd.get("a", 1.0), nd.get("s", 1.0)
    if a <= 0.002:
        return
    x, y, w, h = nd["x"], nd["y"], nd["w"], nd["h"]
    kind, label = nd["kind"], nd.get("label", "")
    state = nd.get("state", "ok")
    ink, muted = c.theme("ink", "d_ink"), c.theme("muted", "d_muted")
    with c.at(0, 0, s, origin=(x + w / 2, y + h / 2)):
        with c.group(a):
            if kind == "node":
                c.fill_rrect(x, y, w, h, 24, (*PURPLE[:3], 0.05))
                c.stroke_rrect(x, y, w, h, 24, PURPLE, 2, 0.7, dash=[10, 8])
                c.text(x + 22, y + 36, label.upper(), tk.F["mono_med"], 18, PURPLE, 1, 0.16)
                if nd.get("sub"):
                    c.text(x + w - 22, y + 36, nd["sub"], tk.F["mono"], 16, muted, 1, 0.04, align="r")
            elif kind == "pod":
                col = tk.C["rec"] if state == "dead" else PURPLE
                c.shadow(x, y, w, h, 16, 18, 8, 0.18, col)
                c.fill_rrect(x, y, w, h, 16, col)
                c.text(x + w / 2, y + h / 2 + 8, label or "pod", tk.F["mono_bold"], 22, (1, 1, 1, 1), 1, 0.06, align="c")
                if state == "dead":
                    cx_, cy_ = x + w - 22, y + 22
                    c.line(cx_ - 9, cy_ - 9, cx_ + 9, cy_ + 9, (1, 1, 1, 1), 4)
                    c.line(cx_ - 9, cy_ + 9, cx_ + 9, cy_ - 9, (1, 1, 1, 1), 4)
            else:  # users / lb / generic service card
                c.card(x, y, w, h, r=20)
                if kind == "users":
                    for k in range(3):
                        px = x + 40 + k * 26
                        c.circle(px, y + h / 2 - 8, 10, c.theme("ink2", "d_ink"))
                        c.fill_rrect(px - 14, y + h / 2 + 6, 28, 16, 8, c.theme("ink2", "d_ink"))
                    c.text(x + 130, y + h / 2 + 9, label, tk.F["ui_semi"], 28, ink, 1, -0.02)
                elif kind == "lb":
                    mx, my = x + 46, y + h / 2
                    acc = c.theme("accent", "d_accent")
                    c.line(mx - 18, my, mx, my, acc, 4)
                    for dy in (-16, 0, 16):
                        c.line(mx, my, mx + 18, my + dy, acc, 4)
                    c.text(x + 86, y + h / 2 + 9, label, tk.F["ui_semi"], 28, ink, 1, -0.02)
                else:
                    c.text(x + w / 2, y + h / 2 + 9, label, tk.F["ui_semi"], 28, ink, 1, -0.02, align="c")


def arch_diagram(c, t, nodes, edges, speed=0.6, packets=3):
    """nodes: {id: node dict}; edges: [(from_id, to_id, draw_p, flow 0..1)]. Packets ride the edges."""
    acc = c.theme("accent", "d_accent")
    for (a, b, p, flow) in edges:
        na, nb = nodes[a], nodes[b]
        if min(na.get("a", 1), nb.get("a", 1)) <= 0.01:
            continue
        pa = (na["x"] + na["w"] / 2, na["y"] + na["h"])
        pb = (nb["x"] + nb["w"] / 2, nb["y"])
        pts = _elbow(pa, pb)
        _draw_poly(c, pts, p, c.theme("faint", "d_line"), 3, min(na.get("a", 1), nb.get("a", 1)))
        if flow > 0 and p >= 1:
            for k in range(packets):
                f = (t * speed + k / packets + (sum(map(ord, f"{a}>{b}")) % 100) / 100) % 1.0
                px, py = _along(pts, f)
                c.circle(px, py, 7, acc, flow * min(1, f * 6, (1 - f) * 6))
    order = sorted(nodes.values(), key=lambda n: 0 if n["kind"] == "node" else 1)
    for nd in order:
        arch_node(c, nd)


# ── load graph (24h) ────────────────────────────────────────────────────
def load_graph(c, x, y, w, h, traffic, capacity, draw=1.0, cursor=None, hours=(6, 12, 18, 0, 6),
               peak_label=None, peak_p=0.0, cursor_label=None, band_color=None, caption="TRAFFIC · 24 JAM"):
    """traffic(xf), capacity(xf) -> 0..1. x axis = one day starting at hours[0]."""
    band_color = band_color or PURPLE
    c.card(x, y, w, h, r=26)
    px, py, pw, ph = x + 40, y + 80, w - 80, h - 150
    muted = c.theme("muted", "d_muted")
    c.text(x + 40, y + 52, caption, tk.F["mono_med"], 18, muted, 1, 0.18)
    for k, hr in enumerate(hours):
        c.text(px + pw * k / (len(hours) - 1), y + h - 34, f"{hr:02d}:00", tk.F["mono"], 17, muted, 1, 0.04, align="c")
    c.line(px, py + ph, px + pw, py + ph, c.theme("line", "d_line"), 2)
    n = 160
    m = int(n * clamp(draw))
    if m < 2:
        return
    cx = c.ctx
    # capacity band
    cx.new_path()
    cx.move_to(px, py + ph)
    for i in range(m + 1):
        f = i / n
        cx.line_to(px + pw * f, py + ph * (1 - capacity(f)))
    cx.line_to(px + pw * m / n, py + ph)
    cx.close_path()
    c.src(band_color, 0.18)
    cx.fill()
    # traffic line
    cx.new_path()
    for i in range(m + 1):
        f = i / n
        (cx.move_to if i == 0 else cx.line_to)(px + pw * f, py + ph * (1 - traffic(f)))
    c.src(c.theme("ink", "d_ink"))
    cx.set_line_width(5)
    cx.set_line_join(1)
    cx.stroke()
    if peak_label and peak_p > 0:
        fpk = max((i / n for i in range(m + 1)), key=traffic)
        kx, ky = px + pw * fpk, py + ph * (1 - traffic(fpk))
        c.circle(kx, ky, 9, c.theme("ink", "d_ink"), peak_p)
        tw = c.measure(peak_label, tk.F["ui_semi"], 26, -0.01)[0] + 36
        c.fill_rrect(kx - tw / 2, ky - 74, tw, 48, 24, c.theme("card", "d_card"), peak_p)
        c.stroke_rrect(kx - tw / 2, ky - 74, tw, 48, 24, tk.C["ok"], 2, peak_p)
        c.text(kx, ky - 42, peak_label, tk.F["ui_semi"], 26, tk.C["ok"], peak_p, -0.01, align="c")
    if cursor is not None:
        cxp = px + pw * cursor
        c.line(cxp, py - 10, cxp, py + ph, c.theme("accent", "d_accent"), 3)
        if cursor_label:
            from .pill import size_label
            size_label(c, cxp, py - 46, cursor_label)


# ── stacked slabs ───────────────────────────────────────────────────────
def stack_layers(c, x, y_bottom, w, layers, slab_h=120, depth=22, gap=18, ghost=1.0):
    """3D-ish slabs stacked bottom→top. layers: [(label, sub, color, p)] bottom first.

    ghost 0..1 shows dashed outlines of empty slots so dropping slabs never float.
    """
    for k, (label, sub, color, p) in enumerate(layers):
        sy = y_bottom - (k + 1) * (slab_h + depth + gap) + gap
        if ghost > 0 and p < 1:
            c.stroke_rrect(x, sy, w, slab_h + depth, 22, c.theme("faint", "d_line"), 2, ghost * (1 - clamp(p * 2)),
                           dash=[10, 8])
        if p <= 0:
            continue
        dy = -340 * (1 - out_back(clamp(p), 1.3))
        a = clamp(p * 4)
        with c.group(a):
            c.shadow(x, sy + dy, w, slab_h + depth, 22, 26, 14, 0.12)
            c.fill_rrect(x, sy + dy + depth, w, slab_h, 22, mix(color, (0, 0, 0, 1), 0.25))   # side
            c.fill_rrect(x, sy + dy, w, slab_h, 22, c.theme("card", "d_card"))               # top face
            c.stroke_rrect(x, sy + dy, w, slab_h, 22, color, 2.5)
            c.fill_rrect(x + 22, sy + dy + 28, 14, slab_h - 56, 7, color)
            c.text(x + 58, sy + dy + slab_h / 2 + 4, label, tk.F["display_semi"], 46, c.theme("ink", "d_ink"), 1, -0.03)
            if sub:
                c.text(x + w - 30, sy + dy + slab_h / 2 + 2, sub, tk.F["mono_med"], 20, c.theme("muted", "d_muted"),
                       1, 0.08, align="r")


def slab_y(y_bottom, k, slab_h=120, depth=22, gap=18):
    """Top y of slab k (0 = bottom) — for attaching badges/notes."""
    return y_bottom - (k + 1) * (slab_h + depth + gap) + gap
