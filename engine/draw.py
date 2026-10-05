"""Canvas: thin wrapper over cairo + Pango with the primitives scenes need.

All coordinates are in 1080x1920 design space; the canvas may be scaled
(preview = 0.5) and everything still lines up.
"""
import math
import os
import pathlib
from contextlib import contextmanager
from functools import lru_cache

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"


def _setup_fonts():
    """Point fontconfig at assets/fonts before Pango loads."""
    cache = ROOT / ".cache"
    cache.mkdir(exist_ok=True)
    conf = cache / "fonts.conf"
    conf.write_text(
        '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n<fontconfig>\n'
        '  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>\n'
        f"  <dir>{FONT_DIR}</dir>\n  <cachedir>{cache / 'fontconfig'}</cachedir>\n</fontconfig>\n")
    os.environ["FONTCONFIG_FILE"] = str(conf)


_setup_fonts()

import cairo  # noqa: E402
import gi  # noqa: E402

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
gi.require_foreign("cairo")
from gi.repository import Pango, PangoCairo  # noqa: E402

from . import tokens as tk  # noqa: E402

_FO = cairo.FontOptions()
_FO.set_hint_style(cairo.HINT_STYLE_NONE)
_FO.set_hint_metrics(cairo.HINT_METRICS_OFF)  # smooth sub-pixel motion
_FO.set_antialias(cairo.ANTIALIAS_GRAY)


# ── blur ────────────────────────────────────────────────────────────────
def _box(a, r, axis):
    if r < 1:
        return a
    n = a.shape[axis]
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    cs = np.cumsum(np.pad(a, pad), axis=axis, dtype=np.float32)
    hi = [slice(None)] * a.ndim
    lo = [slice(None)] * a.ndim
    hi[axis] = slice(2 * r + 1, 2 * r + 1 + n)
    lo[axis] = slice(0, n)
    return (cs[tuple(hi)] - cs[tuple(lo)]) / (2 * r + 1)


def gaussian(arr, sigma):
    """Approximate gaussian blur (3 box passes) on an HxWx4 premultiplied array."""
    if sigma < 0.5:
        return arr
    w = math.sqrt(12 * sigma * sigma / 3 + 1)
    r = max(1, int(round((w - 1) / 2)))
    a = arr.astype(np.float32)
    for _ in range(3):
        a = _box(a, r, 0)
        a = _box(a, r, 1)
    return np.clip(a, 0, 255).astype(np.uint8)


def surface_to_array(surf):
    surf.flush()
    h, w, stride = surf.get_height(), surf.get_width(), surf.get_stride()
    return np.frombuffer(surf.get_data(), np.uint8).reshape(h, stride)[:, : w * 4].reshape(h, w, 4)


def array_to_surface(arr):
    arr = np.ascontiguousarray(arr)
    h, w = arr.shape[:2]
    buf = bytearray(arr.tobytes())
    surf = cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_ARGB32, w, h, w * 4)
    # pycairo holds a reference to buf for the surface lifetime
    return surf


@lru_cache(maxsize=256)
def _shadow_mask(w, h, r, blur, s):
    """Blurred rounded-rect alpha mask at device scale s. Returns (surface, pad)."""
    pad = int(blur * 3) + 2
    W, H = int((w + 2 * pad) * s) + 1, int((h + 2 * pad) * s) + 1
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cx = cairo.Context(surf)
    cx.scale(s, s)
    _rrect_path(cx, pad, pad, w, h, r)
    cx.set_source_rgba(0, 0, 0, 1)
    cx.fill()
    return array_to_surface(gaussian(surface_to_array(surf), blur * s / 2)), pad


@lru_cache(maxsize=128)
def load_png(path):
    return cairo.ImageSurface.create_from_png(str(path))


def _rrect_path(cx, x, y, w, h, r):
    r = max(0.0, min(r, w / 2, h / 2))
    cx.new_sub_path()
    cx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cx.close_path()


# ── canvas ──────────────────────────────────────────────────────────────
class Canvas:
    def __init__(self, ctx, scale=1.0, dark=0.0):
        self.ctx = ctx
        self.s = scale
        self.dark = dark  # 0 light → 1 dark; components may read it to pick colors

    # color ----------------------------------------------------------------
    def src(self, color, alpha=1.0):
        r, g, b = color[:3]
        a = color[3] if len(color) > 3 else 1.0
        self.ctx.set_source_rgba(r, g, b, a * alpha)

    def theme(self, light_key, dark_key):
        """Pick a token color blended by the current dark amount."""
        a, b = tk.C[light_key], tk.C[dark_key]
        return tuple(x + (y - x) * self.dark for x, y in zip(a, b))

    # shapes ---------------------------------------------------------------
    def rrect(self, x, y, w, h, r):
        _rrect_path(self.ctx, x, y, w, h, r)

    def fill_rrect(self, x, y, w, h, r, color, alpha=1.0):
        self.ctx.new_path()
        self.rrect(x, y, w, h, r)
        self.src(color, alpha)
        self.ctx.fill()

    def stroke_rrect(self, x, y, w, h, r, color, width=1.0, alpha=1.0, dash=None):
        self.ctx.new_path()
        self.rrect(x, y, w, h, r)
        self.src(color, alpha)
        self.ctx.set_line_width(width)
        self.ctx.set_dash(dash or [])
        self.ctx.stroke()
        self.ctx.set_dash([])

    def circle(self, x, y, r, color, alpha=1.0):
        self.ctx.new_path()
        self.ctx.arc(x, y, r, 0, 2 * math.pi)
        self.src(color, alpha)
        self.ctx.fill()

    def line(self, x1, y1, x2, y2, color, width=1.0, alpha=1.0, cap=cairo.LINE_CAP_ROUND):
        self.ctx.new_path()
        self.ctx.move_to(x1, y1)
        self.ctx.line_to(x2, y2)
        self.src(color, alpha)
        self.ctx.set_line_width(width)
        self.ctx.set_line_cap(cap)
        self.ctx.stroke()

    def shadow(self, x, y, w, h, r, blur=30, dy=10, alpha=0.08, color=(0, 0, 0, 1)):
        if alpha <= 0.002:
            return
        dev = self.ctx.get_matrix().xx  # current device scale (includes element scale)
        s = round(max(0.1, abs(dev)), 2)
        mask, pad = _shadow_mask(int(w), int(h), int(r), int(blur), s)
        cx = self.ctx
        cx.save()
        cx.translate(x - pad, y - pad + dy)
        cx.scale(1 / s, 1 / s)
        self.src(color, alpha)
        cx.mask_surface(mask, 0, 0)
        cx.restore()

    def card(self, x, y, w, h, r=None, shadow="card", color=None, border=True, alpha=1.0):
        """White rounded card with the reference soft shadow + hairline border."""
        r = tk.L["radius_card"] if r is None else r
        if shadow:
            sh = tk.SHADOW[shadow]
            self.shadow(x, y, w, h, r, sh["blur"], sh["dy"], sh["alpha"] * alpha * (1 - 0.6 * self.dark))
        self.fill_rrect(x, y, w, h, r, color or self.theme("card", "d_card"), alpha)
        if border:
            self.stroke_rrect(x + 0.5, y + 0.5, w - 1, h - 1, r, self.theme("line", "d_line"), 1.0, alpha)

    def image(self, path, x, y, w, h, r=0, alpha=1.0, fit="cover"):
        img = load_png(path)
        iw, ih = img.get_width(), img.get_height()
        sc = max(w / iw, h / ih) if fit == "cover" else min(w / iw, h / ih)
        cx = self.ctx
        cx.save()
        cx.new_path()
        self.rrect(x, y, w, h, r)
        cx.clip()
        cx.translate(x + (w - iw * sc) / 2, y + (h - ih * sc) / 2)
        cx.scale(sc, sc)
        cx.set_source_surface(img, 0, 0)
        cx.get_source().set_filter(cairo.FILTER_GOOD)
        cx.paint_with_alpha(alpha)
        cx.restore()

    # text -----------------------------------------------------------------
    def layout(self, text, font, size, ls=0.0, markup=False, width=None, align="l", line_h=None):
        pctx = PangoCairo.create_context(self.ctx)
        PangoCairo.context_set_font_options(pctx, _FO)
        try:
            pctx.set_round_glyph_positions(False)
        except AttributeError:
            pass
        lay = Pango.Layout.new(pctx)
        desc = Pango.FontDescription.from_string(font)
        desc.set_absolute_size(size * Pango.SCALE)
        lay.set_font_description(desc)
        if markup:
            lay.set_markup(text, -1)
        else:
            lay.set_text(text, -1)
        if ls:
            attrs = lay.get_attributes() or Pango.AttrList()
            attrs.insert(Pango.attr_letter_spacing_new(int(ls * size * Pango.SCALE)))
            lay.set_attributes(attrs)
        if width:
            lay.set_width(int(width * Pango.SCALE))
            lay.set_wrap(Pango.WrapMode.WORD)
        if line_h:
            lay.set_line_spacing(line_h)
        lay.set_alignment({"l": Pango.Alignment.LEFT, "c": Pango.Alignment.CENTER,
                           "r": Pango.Alignment.RIGHT}[align])
        return lay

    @staticmethod
    def extents(lay):
        _, log = lay.get_extents()
        return log.width / Pango.SCALE, log.height / Pango.SCALE, lay.get_baseline() / Pango.SCALE

    def measure(self, text, font, size, ls=0.0, markup=False):
        """(width, height, baseline) of a single-line string."""
        w, h, b = self.extents(self.layout(text, font, size, ls, markup))
        return w - (ls * size if ls > 0 else 0), h, b

    def text(self, x, y, text, font, size, color, alpha=1.0, ls=0.0, align="l",
             markup=False, width=None, line_h=None):
        """Draw text with its first baseline at y. align l/c/r is relative to x. Returns width."""
        if alpha <= 0.002 or not text:
            return 0.0
        lay = self.layout(text, font, size, ls, markup, width, "l" if width is None else align, line_h)
        w, h, base = self.extents(lay)
        if width is None and ls > 0:
            w -= ls * size  # trailing tracking
        dx = 0 if (align == "l" or width is not None) else (-w / 2 if align == "c" else -w)
        cx = self.ctx
        cx.move_to(x + dx, y - base)
        self.src(color, alpha)
        PangoCairo.show_layout(cx, lay)
        cx.new_path()
        return w

    def style_text(self, x, y, text, style, font, color, alpha=1.0, align="l", **kw):
        """Text using a T token: style_text(x, y, 'hi', 'kicker', tk.F['mono'], color)."""
        size, ls, _ = tk.T[style]
        return self.text(x, y, text, font, size, color, alpha, ls, align, **kw)

    # compositing ----------------------------------------------------------
    @contextmanager
    def group(self, opacity=1.0):
        """Draw the body as one unit with group opacity."""
        cx = self.ctx
        cx.push_group()
        try:
            yield self
        finally:
            cx.pop_group_to_source()
            if opacity > 0.002:
                cx.paint_with_alpha(min(1.0, opacity))

    @contextmanager
    def layer(self, bbox, opacity=1.0, blur=0.0):
        """Offscreen layer with group opacity and gaussian blur (design-space px).

        bbox = (x, y, w, h) in current user space; content outside it (plus blur pad) is clipped.
        """
        if blur < 0.4:
            with self.group(opacity):
                yield self
            return
        cx = self.ctx
        m = cx.get_matrix()
        sc = math.hypot(m.xx, m.yx)
        pad = blur * 3
        x, y, w, h = bbox
        pts = [cx.user_to_device(px, py) for px, py in
               ((x - pad, y - pad), (x + w + pad, y - pad), (x - pad, y + h + pad), (x + w + pad, y + h + pad))]
        tw, th = cx.get_target().get_width(), cx.get_target().get_height()
        dx0 = max(0, int(min(p[0] for p in pts)))
        dy0 = max(0, int(min(p[1] for p in pts)))
        dx1 = min(tw, int(math.ceil(max(p[0] for p in pts))))
        dy1 = min(th, int(math.ceil(max(p[1] for p in pts))))
        if dx1 <= dx0 or dy1 <= dy0 or opacity <= 0.002:
            with self.group(0.0):
                yield self
            return
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, dx1 - dx0, dy1 - dy0)
        cx2 = cairo.Context(surf)
        cx2.translate(-dx0, -dy0)
        cx2.transform(m)
        prev = self.ctx
        self.ctx = cx2
        try:
            yield self
        finally:
            self.ctx = prev
            out = array_to_surface(gaussian(surface_to_array(surf), blur * sc / 2))
            cx.save()
            cx.identity_matrix()
            cx.set_source_surface(out, dx0, dy0)
            cx.paint_with_alpha(min(1.0, opacity))
            cx.restore()

    @contextmanager
    def at(self, tx=0.0, ty=0.0, scale=1.0, origin=(0.0, 0.0), rot=0.0):
        """Translate/scale/rotate around origin for the body."""
        cx = self.ctx
        cx.save()
        cx.translate(tx + origin[0], ty + origin[1])
        if rot:
            cx.rotate(rot)
        if scale != 1.0:
            cx.scale(scale, scale)
        cx.translate(-origin[0], -origin[1])
        try:
            yield self
        finally:
            cx.restore()

    @contextmanager
    def clip(self, x, y, w, h, r=0):
        cx = self.ctx
        cx.save()
        cx.new_path()
        self.rrect(x, y, w, h, r)
        cx.clip()
        try:
            yield self
        finally:
            cx.restore()


def new_frame(scale=1.0):
    """Fresh ARGB surface + Canvas at design size x scale."""
    w, h = int(round(tk.W * scale)), int(round(tk.H * scale))
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    cx = cairo.Context(surf)
    cx.scale(scale, scale)
    return surf, Canvas(cx, scale)
