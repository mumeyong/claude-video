"""Line icons drawn with cairo paths (no icon fonts). All centered at (x, y), size s."""
import math

import cairo


def _stroke(c, color, w, alpha=1.0):
    c.src(color, alpha)
    c.ctx.set_line_width(w)
    c.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    c.ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    c.ctx.stroke()


def plus(c, x, y, s, color, w=2.0, alpha=1.0):
    h = s / 2
    cx = c.ctx
    cx.new_path()
    cx.move_to(x - h, y); cx.line_to(x + h, y)
    cx.move_to(x, y - h); cx.line_to(x, y + h)
    _stroke(c, color, w, alpha)


def arrow_up(c, x, y, s, color, w=2.6, alpha=1.0):
    h = s / 2
    cx = c.ctx
    cx.new_path()
    cx.move_to(x, y + h); cx.line_to(x, y - h)
    cx.move_to(x - h * 0.75, y - h * 0.2); cx.line_to(x, y - h); cx.line_to(x + h * 0.75, y - h * 0.2)
    _stroke(c, color, w, alpha)


def check(c, x, y, s, color, w=2.6, alpha=1.0, p=1.0):
    """Checkmark; p (0..1) draws it progressively."""
    pts = [(x - s * 0.42, y + s * 0.02), (x - s * 0.12, y + s * 0.32), (x + s * 0.45, y - s * 0.3)]
    l1 = math.dist(pts[0], pts[1]); l2 = math.dist(pts[1], pts[2])
    d = (l1 + l2) * p
    cx = c.ctx
    cx.new_path()
    cx.move_to(*pts[0])
    if d <= l1:
        f = d / l1
        cx.line_to(pts[0][0] + (pts[1][0] - pts[0][0]) * f, pts[0][1] + (pts[1][1] - pts[0][1]) * f)
    else:
        cx.line_to(*pts[1])
        f = (d - l1) / l2
        cx.line_to(pts[1][0] + (pts[2][0] - pts[1][0]) * f, pts[1][1] + (pts[2][1] - pts[1][1]) * f)
    _stroke(c, color, w, alpha)


def paperclip(c, x, y, s, color, w=1.8, alpha=1.0):
    cx = c.ctx
    cx.save()
    cx.translate(x, y); cx.rotate(math.radians(40))
    r = s * 0.22
    cx.new_path()
    cx.move_to(r, -s * 0.15)
    cx.line_to(r, s * 0.3)
    cx.arc(0, s * 0.3, r, 0, math.pi)
    cx.line_to(-r, -s * 0.35)
    cx.arc(-r * 0.0, -s * 0.35, r, math.pi, 0)
    cx.line_to(r * 1.0, s * 0.1)
    cx.restore()
    _stroke(c, color, w, alpha)


def mic(c, x, y, s, color, w=1.8, alpha=1.0):
    cx = c.ctx
    cx.new_path()
    c.rrect(x - s * 0.18, y - s * 0.5, s * 0.36, s * 0.62, s * 0.18)
    _stroke(c, color, w, alpha)
    cx.new_path()
    cx.arc(x, y - s * 0.05, s * 0.32, 0.15, math.pi - 0.15)
    cx.move_to(x, y + s * 0.28); cx.line_to(x, y + s * 0.48)
    _stroke(c, color, w, alpha)


def globe(c, x, y, s, color, w=1.8, alpha=1.0):
    cx = c.ctx
    r = s * 0.46
    cx.new_path()
    cx.arc(x, y, r, 0, 2 * math.pi)
    _stroke(c, color, w, alpha)
    cx.new_path()
    cx.save(); cx.translate(x, y); cx.scale(0.45, 1); cx.arc(0, 0, r, 0, 2 * math.pi); cx.restore()
    cx.move_to(x - r, y); cx.line_to(x + r, y)
    _stroke(c, color, w, alpha)


def bulb(c, x, y, s, color, w=1.8, alpha=1.0):
    cx = c.ctx
    r = s * 0.3
    cx.new_path()
    cx.arc(x, y - s * 0.12, r, math.pi * 0.8, math.pi * 2.2)
    cx.line_to(x + r * 0.5, y + s * 0.3)
    cx.line_to(x - r * 0.5, y + s * 0.3)
    cx.close_path()
    cx.move_to(x - r * 0.45, y + s * 0.45); cx.line_to(x + r * 0.45, y + s * 0.45)
    _stroke(c, color, w, alpha)


def pointer(c, x, y, s=34, alpha=1.0):
    """macOS-style arrow cursor with tip at (x, y)."""
    pts = [(0, 0), (0, 1.0), (0.26, 0.76), (0.43, 1.12), (0.57, 1.06), (0.40, 0.70), (0.74, 0.70)]
    cx = c.ctx
    cx.new_path()
    for i, (px, py) in enumerate(pts):
        (cx.move_to if i == 0 else cx.line_to)(x + px * s, y + py * s)
    cx.close_path()
    c.src((0, 0, 0, 1), alpha)
    cx.fill_preserve()
    c.src((1, 1, 1, 1), alpha)
    cx.set_line_width(2.2)
    cx.set_line_join(cairo.LINE_JOIN_ROUND)
    cx.stroke()


def play_logo(c, x, y, r, color, w=None, p=1.0, alpha=1.0):
    """Circle-with-gap + play triangle (outro logo). p 0..1 draws the ring."""
    cx = c.ctx
    w = w or r * 0.2
    gap = 0.55
    a0 = -math.pi * 0.08 + gap / 2
    sweep = (2 * math.pi - gap) * p
    cx.new_path()
    cx.arc(x, y, r, a0, a0 + sweep)
    c.src(color, alpha)
    cx.set_line_width(w)
    cx.set_line_cap(cairo.LINE_CAP_BUTT)
    cx.stroke()
    if p > 0.6:
        a = min(1, (p - 0.6) / 0.4)
        cx.new_path()
        cx.move_to(x - r * 0.28, y - r * 0.5)
        cx.line_to(x + r * 0.52, y)
        cx.line_to(x - r * 0.28, y + r * 0.5)
        cx.line_to(x - r * 0.1, y)
        cx.close_path()
        c.src(color, alpha * a)
        cx.fill()


def wa(c, x, y, s, color, alpha=1.0):
    """Simple phone/chat glyph for WhatsApp pill."""
    cx = c.ctx
    cx.new_path()
    cx.arc(x, y, s * 0.42, 0, 2 * math.pi)
    _stroke(c, color, 1.8, alpha)
    cx.new_path()
    cx.move_to(x - s * 0.3, y + s * 0.32); cx.line_to(x - s * 0.42, y + s * 0.48); cx.line_to(x - s * 0.16, y + s * 0.4)
    _stroke(c, color, 1.8, alpha)
