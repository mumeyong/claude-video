"""Window cards: markdown file, code file, terminal. White card + grey dots + title bar."""
import html
import re

from .. import tokens as tk
from ..ease import prog, in_out_cubic, glide
from .motion import typed

HEADER_H = 66
PAD_X = 32


def frame(c, x, y, w, h, title, meta="", title_mono=False):
    """Card chrome. Returns (body_x, body_y) where content starts."""
    c.card(x, y, w, h)
    for i in range(3):
        c.circle(x + 26 + i * 18, y + HEADER_H / 2, 5.5, c.theme("faint", "d_line"))
    size, ls, _ = tk.T["card_title"]
    font = tk.F["mono_med"] if title_mono else tk.F["ui_semi"]
    c.text(x + 92, y + HEADER_H / 2 + 9, title, font, size if not title_mono else size - 3,
           c.theme("ink", "d_ink"), 1, ls)
    if meta:
        ms, mls, _ = tk.T["card_meta"]
        c.text(x + w - PAD_X, y + HEADER_H / 2 + 7, meta, tk.F["mono"], ms, c.theme("muted", "d_muted"), 1, mls, align="r")
    c.line(x + 1, y + HEADER_H, x + w - 1, y + HEADER_H, c.theme("line", "d_line"), 1)
    return x + PAD_X, y + HEADER_H + 18


# ── markdown ────────────────────────────────────────────────────────────
def md_markup(line, code_bg="#EEF0F3"):
    """Tiny markdown → Pango markup: # / ## / - bullets, **bold**, `code`."""
    s = html.escape(line, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", rf'<span background="{code_bg}"> \1 </span>', s)
    return s


def md_lines(c, x, y, lines, t, reveal=None, focus=None, focus_t=None, width=780):
    """Draw markdown lines.

    reveal: list of times each line appears (None = all visible).
    focus: index of a line to spotlight from focus_t (others dim to 30%, blue outline on it).
    Returns list of (line_top, line_h) for annotations.
    """
    size, _, lh = tk.T["body_mono"]
    step = size * lh
    ink = c.theme("ink2", "d_ink")
    rows = []
    fp = in_out_cubic(prog(t, focus_t, 0.4)) if focus is not None and focus_t is not None else 0.0
    for i, raw in enumerate(lines):
        top = y + i * step
        rows.append((top, step))
        a = 1.0 if reveal is None else glide(prog(t, reveal[i], 0.35))
        if a <= 0.002:
            continue
        dim = 1.0 - (0.7 * fp if (focus is not None and i != focus) else 0.0)
        font = tk.F["mono"]
        text, col, xx = raw, ink, x
        if raw.startswith("## "):
            text, col = raw, c.theme("muted", "d_muted")
        elif raw.startswith("# "):
            font = tk.F["mono_bold"]
            col = c.theme("ink", "d_ink")
        elif raw.startswith("- "):
            c.circle(x + 6, top + step / 2 - 2, 3.5, c.theme("accent", "d_accent"), a * dim)
            text, xx = raw[2:], x + 22
        dx = 10 * (1 - a)
        c.text(xx + dx, top + step / 2 + size * 0.36, md_markup(text), font, size, col, a * dim,
               markup=True, width=width - (xx - x))
        if focus == i and fp > 0:
            c.stroke_rrect(x - 12, top + 4, width + 20, step - 4, 4, c.theme("accent", "d_accent"), 2, fp)
    return rows


# ── code ────────────────────────────────────────────────────────────────
_KW = r"\b(import|from|def|return|const|let|var|function|class|if|else|elif|for|in|while|export|async|await|with|as|new)\b"


def code_markup(line):
    C = tk.C

    def hx(col):
        return "#%02x%02x%02x" % tuple(int(v * 255) for v in col[:3])

    out, i = [], 0
    pat = re.compile(r"(//.*$|#.*$)|('[^']*'|\"[^\"]*\")|" + _KW)
    for m in pat.finditer(line):
        out.append(html.escape(line[i:m.start()], quote=False))
        tok = html.escape(m.group(0), quote=False)
        if m.group(1):
            out.append(f'<span foreground="{hx(C["code_cmt"])}">{tok}</span>')
        elif m.group(2):
            out.append(f'<span foreground="{hx(C["code_str"])}">{tok}</span>')
        else:
            out.append(f'<span foreground="{hx(C["code_kw"])}">{tok}</span>')
        i = m.end()
    out.append(html.escape(line[i:], quote=False))
    return "".join(out)


def code_lines(c, x, y, lines, t, t0=None, cps=None, line_numbers=True, size=None, clip_w=None):
    """Code with line numbers + light syntax colors. t0/cps = type it out line by line."""
    size = size or tk.T["body_mono"][0] - 2
    step = size * 1.62
    total = 0
    for i, ln in enumerate(lines):
        top = y + i * step
        base = top + size
        if t0 is not None:
            vis_text, _, _, _ = typed(ln, t, t0 + total / (cps or 120), cps or 120)
            total += len(ln) + 4
            if not vis_text and ln:
                continue
        else:
            vis_text = ln
        if line_numbers:
            c.text(x, base, str(i + 1), tk.F["mono"], size, c.theme("faint", "d_muted"), 1)
        c.text(x + (44 if line_numbers else 0), base, code_markup(vis_text), tk.F["mono"], size,
               c.theme("code_txt", "d_ink"), 1, markup=True)
    return y + len(lines) * step


# ── terminal ────────────────────────────────────────────────────────────
def terminal_line(c, x, y, cmd, t, t0, cps=None, caret=True):
    """'› cmd' typed from t0. Returns True once fully typed."""
    size = tk.T["body_mono"][0] + 3
    c.text(x, y, "›", tk.F["mono_bold"], size + 2, c.theme("accent", "d_accent"), 1)
    full, part, pa, done = typed(cmd, t, t0, cps)
    w = c.text(x + 28, y, full, tk.F["mono"], size, c.theme("ink", "d_ink"), 1) if full else 0
    if part:
        w += c.text(x + 28 + w, y, part, tk.F["mono"], size, c.theme("accent", "d_accent"), pa)
    if caret and t >= t0 - 0.5 and (not done or (t * 1.6) % 1 < 0.5):
        c.fill_rrect(x + 30 + w, y - size * 0.8, 2.5, size * 0.95, 1, c.theme("ink", "d_ink"))
    return done


def progress_bar(c, x, y, w, p, h=10):
    c.fill_rrect(x, y, w, h, h / 2, c.theme("line", "d_line"))
    if p > 0:
        c.fill_rrect(x, y, max(h, w * p), h, h / 2, c.theme("accent", "d_accent"))
