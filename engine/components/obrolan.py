"""iOS-Messages-style chat on a phone (first used in "ai-lupa-obrolan-panjang", 2026-10-13).

chat_phone · chat_geo
A real chat UI instead of a list of lines: header (avatar + name), a thread of bubbles (kamu = right, accent;
AI = left, light grey), a typing indicator, and the input bar with a draft being typed. Apple type: Inter (the open
SF Pro stand-in) for everything, no serif. The thread scrolls by itself with summed springs (track) so a burst of
messages (a time-lapse) glides instead of jumping. Pure function of t (frame = f(t)).
"""
import math

from .. import tokens as tk
from ..ease import clamp, glide, pop, prog, track

C, F = tk.C, tk.F
BASE_W = 620          # design width — everything scales with w / BASE_W
KAMU, AI, TYPING, STAMP = "kamu", "ai", "typing", "stamp"


def chat_geo(x, y, w, h):
    """Geometry of chat_phone drawn with the same box: f, screen, header, thread (view box), input bar, send button."""
    f = w / BASE_W
    b = 18 * f
    sx, sy, sw, sh = x + b, y + b, w - 2 * b, h - 2 * b
    head_h, input_h = 150 * f, 120 * f
    return dict(f=f, r=72 * f, screen=(sx, sy, sw, sh), head=(sx, sy, sw, head_h),
                view=(sx, sy + head_h, sw, sh - head_h - input_h), input=(sx, sy + sh - input_h, sw, input_h),
                send=(sx + sw - 62 * f, sy + sh - input_h / 2), size=34 * f, pad=(28 * f, 18 * f),
                max_w=sw * 0.72, gap=14 * f, margin=26 * f)


_WRAP = {}
LINE_H = 1.22


def _wrap(text, size, width):
    """Lines of text wrapped at width, measured ONCE on an unscaled surface (design units) and cached: the wrap
    never changes with the canvas scale (preview, a scaled phone, a scale animation → no reflow flicker), and lines
    are drawn one by one (Pango line spacing collapses under a scaled CTM). Returns (lines, widest line)."""
    key = (text, round(size, 2), round(width, 1))
    if key not in _WRAP:
        import cairo
        from ..draw import Canvas
        cv = Canvas(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)))
        lay = cv.layout(text, F["ui_reg"], size, width=width)
        raw = text.encode()
        lines = []
        for ln in lay.get_lines_readonly():
            lines.append(raw[ln.start_index:ln.start_index + ln.length].decode().strip())
        widest = max(cv.measure(ln, F["ui_reg"], size)[0] for ln in lines)
        _WRAP[key] = (lines, widest)
    return _WRAP[key]


def _bubble_box(c, g, m):
    """(w, h) of one message bubble (wrapped text)."""
    f, size = g["f"], g["size"]
    if m["who"] == TYPING:
        return 118 * f, 70 * f
    if m["who"] == STAMP:
        return g["view"][2], 54 * f
    px, py = g["pad"]
    lines, tw = _wrap(m["text"], size, g["max_w"] - 2 * px)
    return tw + 2 * px, size * (1.2 + LINE_H * (len(lines) - 1)) + 2 * py


def _layout(c, g, msgs):
    """Thread y (top of each bubble, thread space) + its size. Typing bubbles only take space while shown."""
    ys, sizes, y = [], [], g["gap"]
    for m in msgs:
        w, h = _bubble_box(c, g, m)
        ys.append(y)
        sizes.append((w, h))
        y += h + g["gap"]
    return ys, sizes


def _scroll(c, t, g, msgs, base=0.0, preset="smooth"):
    """Auto-scroll: whenever a message enters, glide (summed springs) so its bottom sits at the bottom of the view.
    A typing bubble with a t_out only borrows its slot — the reply after it takes the same slot."""
    view_h = g["view"][3] - g["gap"]
    frames, y = [(-1e3, base)], g["gap"]
    for m in msgs:
        h = _bubble_box(c, g, m)[1]
        if m.get("t_in") is not None:
            frames.append((m["t_in"], max(base, y + h - view_h)))
        if not (m["who"] == TYPING and m.get("t_out") is not None):
            y += h + g["gap"]
    frames.sort(key=lambda fr: fr[0])
    return track(t, frames, preset)


def chat_phone(c, t, x, y, w, h, msgs, title="Asisten AI", sub="online", draft="", caret=False, send=None,
               base_scroll=0.0, scroll_preset="smooth", color=None, alpha=1.0):
    """Phone with a chat thread, top-left (x, y), size w × h.
    msgs: dicts {text, who ('kamu' | 'ai' | 'typing' | 'stamp'), t_in (None = already there), t_out (typing: when
    the reply replaces it; others: fades out), a (alpha), hl 0..1 (accent outline — 'this one is read'),
    dim 0..1}. Messages are laid out in order; typing bubbles keep their slot only while shown, so put the reply
    right after its typing bubble with the same slot (who='ai', t_in = typing's t_out).
    draft: text in the input bar (caret blinks if caret); send: time the send button is pressed (None = idle).
    base_scroll: px already scrolled before the first t_in (a thread that starts mid-conversation).
    Returns geo + 'boxes' = [(x, y, w, h) screen box of each message, or None if not on screen]."""
    g = chat_geo(x, y, w, h)
    if alpha <= 0.002:
        return g
    f = g["f"]
    col = C["accent"] if color is None else color
    sx, sy, sw, sh = g["screen"]
    # typing bubbles that have been replaced give their slot to the reply
    vis = [m for m in msgs if not (m["who"] == TYPING and m.get("t_out") is not None and t >= m["t_out"])]
    ys, sizes = _layout(c, g, vis)
    scroll = _scroll(c, t, g, msgs, base_scroll, scroll_preset)
    boxes = []
    with c.group(alpha):
        # body + screen
        c.shadow(x, y, w, h, g["r"], 50 * f, 24 * f, 0.18)
        c.fill_rrect(x, y, w, h, g["r"], C["ink"])
        c.fill_rrect(sx, sy, sw, sh, g["r"] - 18 * f, C["card"])
        with c.clip(sx, sy, sw, sh, g["r"] - 18 * f):
            vx, vy, vw, vh = g["view"]
            with c.clip(vx, vy, vw, vh):
                drawn = {}
                for m, ty, (bw, bh) in zip(vis, ys, sizes):
                    drawn[id(m)] = _bubble(c, t, g, m, vx, vy + ty - scroll, bw, bh, col)
                boxes = [drawn.get(id(m)) for m in msgs]          # aligned with msgs (None = not on screen)
            _header(c, g, title, sub, col)
            _input(c, t, g, draft, caret, send, col)
            c.fill_rrect(sx + sw / 2 - 66 * f, sy + 14 * f, 132 * f, 34 * f, 17 * f, C["ink"])   # dynamic island
    g["boxes"] = boxes
    g["scroll"] = scroll
    return g


def _bubble(c, t, g, m, vx, top, bw, bh, col):
    f, size = g["f"], g["size"]
    t_in = m.get("t_in")
    p = 1.0 if t_in is None else prog(t, t_in, 0.45)
    if p <= 0:
        return None
    a = m.get("a", 1.0) * min(1.0, glide(p) * 1.6)
    if m.get("t_out") is not None and m["who"] != TYPING:
        a *= 1 - clamp((t - m["t_out"]) / 0.35)
    if a <= 0.002:
        return None
    dim = m.get("dim", 0.0)
    right = m["who"] == KAMU
    bx = vx + g["view"][2] - g["margin"] - bw if right else vx + g["margin"]
    if m["who"] == STAMP:
        c.text(vx + g["view"][2] / 2, top + bh * 0.62, m["text"], F["ui_semi"], 22 * f, C["muted"], a, 0.02,
               align="c")
        return (bx, top, bw, bh)
    s = 0.9 + 0.1 * pop(p, 1.3)                     # grows out of its tail corner, starts at rest
    ox = bx + (bw if right else 0)
    oy = top + bh
    rise = (1 - glide(p)) * 16 * f
    fill = col if right else tk.C["bubble"]
    ink = C["card"] if right else C["ink"]
    with c.at(0, rise, s, origin=(ox, oy)), c.group(a * (1 - 0.6 * dim)):
        r = min(bh / 2, 36 * f)
        c.fill_rrect(bx, top, bw, bh, r, fill)
        ctx = c.ctx                                 # tail
        tx = bx + bw if right else bx
        d = 1 if right else -1
        ctx.move_to(tx - d * 18 * f, oy - 30 * f)
        ctx.curve_to(tx - d * 4 * f, oy - 6 * f, tx + d * 6 * f, oy, tx + d * 14 * f, oy)
        ctx.curve_to(tx, oy - 6 * f, tx - d * 4 * f, oy - 12 * f, tx - d * 4 * f, oy - 20 * f)
        ctx.close_path()
        c.src(fill)
        ctx.fill()
        hl = m.get("hl", 0.0)
        if hl > 0.002:
            c.stroke_rrect(bx - 5 * f, top - 5 * f, bw + 10 * f, bh + 10 * f, r + 5 * f, tk.CHAPTER[2][0], 4 * f, hl)
        if m["who"] == TYPING:
            for i in range(3):                      # dots breathe in turn (pure in t)
                k = 0.35 + 0.65 * max(0.0, math.sin(2 * math.pi * (t * 1.6 - i * 0.22)))
                c.circle(bx + 36 * f + i * 23 * f, top + bh / 2, 8 * f, C["muted"], k)
        else:
            px, py = g["pad"]
            for i, ln in enumerate(_wrap(m["text"], size, g["max_w"] - 2 * px)[0]):
                c.text(bx + px, top + py + size * 0.93 + i * size * LINE_H, ln, F["ui_reg"], size, ink)
    return (bx, top, bw, bh)


def _header(c, g, title, sub, col):
    f = g["f"]
    hx, hy, hw, hh = g["head"]
    c.fill_rrect(hx, hy, hw, hh, 0, C["card"], 0.96)
    c.line(hx, hy + hh, hx + hw, hy + hh, C["faint"], 1.5 * f, 0.8)
    cx, cy = hx + hw / 2, hy + 84 * f
    c.circle(cx - 128 * f, cy, 26 * f, tk.CHAPTER[2][0])
    c.text(cx - 128 * f, cy + 9 * f, "AI", F["ui_bold"], 22 * f, C["card"], align="c")
    c.text(cx - 88 * f, cy - 4 * f, title, F["ui_semi"], 30 * f, C["ink"])
    c.text(cx - 88 * f, cy + 28 * f, sub, F["ui_reg"], 22 * f, C["muted"])
    c.text(hx + 34 * f, hy + 44 * f, "20.41", F["ui_semi"], 22 * f, C["ink"])


def _input(c, t, g, draft, caret, send, col):
    f = g["f"]
    ix, iy, iw, ih = g["input"]
    c.line(ix, iy, ix + iw, iy, C["faint"], 1.5 * f, 0.8)
    fx, fy, fw, fh = ix + 26 * f, iy + 24 * f, iw - 120 * f, 64 * f
    c.stroke_rrect(fx, fy, fw, fh, fh / 2, C["faint"], 2 * f)
    if draft:
        w = c.text(fx + 26 * f, fy + fh * 0.66, draft, F["ui_reg"], 30 * f, C["ink"])
        if caret and (t * 2) % 1 < 0.5:
            c.line(fx + 30 * f + w, fy + 16 * f, fx + 30 * f + w, fy + fh - 16 * f, col, 3 * f)
    else:
        c.text(fx + 26 * f, fy + fh * 0.66, "Ketik pesan", F["ui_reg"], 30 * f, C["muted"])
    bx, by = g["send"]
    press = 0.0 if send is None else math.sin(math.pi * clamp((t - send) / 0.24))
    on = 1.0 if draft else 0.35
    c.circle(bx, by, 30 * f * (1 - 0.12 * press), col, on)
    c.line(bx, by + 12 * f, bx, by - 12 * f, C["card"], 4 * f, on)
    c.line(bx - 10 * f, by - 2 * f, bx, by - 12 * f, C["card"], 4 * f, on)
    c.line(bx + 10 * f, by - 2 * f, bx, by - 12 * f, C["card"], 4 * f, on)
