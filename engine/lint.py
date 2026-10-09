"""Dry check: run every draw function off-screen and report problems — no image, no video, nothing written.

    python -m engine check <slug> --dry

Each active layer is drawn on its own tiny throw-away surface (scale 0.25, layout space, no camera) every `step`
seconds. Reports:
  · exceptions (first time + traceback line per layer)
  · ink outside the safe column x 81–929 (± tolerance) that lasts longer than a whip transition
    (`!` = more than 40 px over — real problem; `·` = a few px, usually a card edge/shadow — judge by eye)
  · ink above the kicker (y < 240) or below the content floor (y > 1560)
  · text smaller than 17 px
Full-screen overlays (z >= 100, e.g. the series bumper) are skipped. Shadows/glows are ignored (alpha threshold).
"""
import traceback

import numpy as np

from . import tokens as tk
from .draw import new_frame, Canvas
from .render import _video

SCALE = 0.25
ALPHA = 0.35          # ink below this alpha (soft shadows, glows) doesn't count
TOL = 8               # px of slack around the safe column
PERSIST = 0.75        # seconds an out-of-bounds layer must stay out to be reported (whips are shorter)
MIN_TEXT = 17
HEAD_Y, HEAD_EXTRA = 520, 60   # above y 520 the TikTok rail is absent; Headline wraps at col_w + 60


def _name(fn):
    code = getattr(fn, "__code__", None)
    q = getattr(fn, "__qualname__", repr(fn)).replace(".<locals>", "")
    return f"{q}:{code.co_firstlineno}" if code else q


def _alpha(surf):
    surf.flush()
    return np.frombuffer(surf.get_data(), np.uint8).reshape(surf.get_height(), surf.get_stride() // 4, 4)[..., 3]


def _outside(a, x_lo, x_hi, y_lo, y_hi):
    """Ink outside the safe box → (side, overshoot px, (x0, x1, y0, y1) of the offending ink) per side, design px."""
    ink = a > ALPHA * 255
    out = []
    xl, xh, yl, yh = (int(v * SCALE) for v in (x_lo, x_hi, y_lo, y_hi))
    left, right = ink[:, :max(0, xl)], ink[:, xh:].copy()
    hz, extra = int(HEAD_Y * SCALE), int(HEAD_EXTRA * SCALE)      # headline zone may use col_w + 60 (Headline width)
    right[:hz, :extra] = False
    if left.any() or right.any():
        ys = np.nonzero(left.any(1) | right.any(1))[0]
        xs_l = np.nonzero(left.any(0))[0]
        xs_r = np.nonzero(right.any(0))[0] + xh
        over = max((xl - xs_l.min()) if len(xs_l) else 0, (xs_r.max() + 1 - xh) if len(xs_r) else 0) / SCALE
        x0 = xs_l.min() if len(xs_l) else xh
        x1 = xs_r.max() + 1 if len(xs_r) else xl
        out.append(("X", over, (x0 / SCALE, x1 / SCALE, ys.min() / SCALE, (ys.max() + 1) / SCALE)))
    top, bot = ink[:max(0, yl), :], ink[yh:, :]
    if top.any() or bot.any():
        xs = np.nonzero(top.any(0) | bot.any(0))[0]
        ys_t = np.nonzero(top.any(1))[0]
        ys_b = np.nonzero(bot.any(1))[0] + yh
        over = max((yl - ys_t.min()) if len(ys_t) else 0, (ys_b.max() + 1 - yh) if len(ys_b) else 0) / SCALE
        out.append(("Y", over, (xs.min() / SCALE, (xs.max() + 1) / SCALE,
                                (ys_t.min() if len(ys_t) else yh) / SCALE, (ys_b.max() + 1 if len(ys_b) else yl) / SCALE)))
    return out


def _ranges(ts, step):
    """[t, t, …] → [(t0, t1), …] merged where consecutive."""
    out = []
    for t in ts:
        if out and t - out[-1][1] <= step * 1.5:
            out[-1][1] = t
        else:
            out.append([t, t])
    return out


def dry_check(slug, step=0.25):
    project, video = _video(slug)
    x_lo, x_hi = tk.L["col_x"] - TOL, tk.L["col_x"] + tk.L["col_w"] + TOL
    y_lo, y_hi = 240, 1560
    errors, small = {}, {}
    out_x, out_y = {}, {}

    orig_text = Canvas.text
    cur = {"layer": None, "t": 0.0}

    def text_spy(self, x, y, text, font, size, *a, **kw):
        if size < MIN_TEXT - 0.01 and text and cur["layer"]:
            small.setdefault(cur["layer"], (cur["t"], size, text))
        return orig_text(self, x, y, text, font, size, *a, **kw)

    Canvas.text = text_spy
    n = int(video.duration / step) + 1
    try:
        for i in range(n):
            t = i * step
            for ly in video.layers:
                if not (ly.start <= t < ly.end) or ly.z >= 100:
                    continue
                name = _name(ly.fn)
                cur["layer"], cur["t"] = name, t
                surf, c = new_frame(SCALE)
                c.dark = video.dark_amount(t)
                try:
                    c.ctx.save()
                    ly.fn(c, t)
                    c.ctx.restore()
                except Exception as ex:  # noqa: BLE001 — report everything
                    if name not in errors:
                        tb = traceback.extract_tb(ex.__traceback__)
                        here = [f for f in tb if "videos/" in f.filename or "components/" in f.filename] or tb
                        f = here[-1]
                        errors[name] = (t, f"{type(ex).__name__}: {ex}",
                                        f"{f.filename.split('claude-video/')[-1]}:{f.lineno}")
                    continue
                for side, over, box in _outside(_alpha(surf), x_lo, x_hi, y_lo, y_hi):
                    (out_x if side == "X" else out_y).setdefault(name, []).append((t, over, box))
    finally:
        Canvas.text = orig_text

    print(f"{slug}: dry check · {n} samples every {step}s · nothing written")
    bad = 0
    for name, (t, msg, where) in errors.items():
        bad += 1
        print(f"  ✗ ERROR   {name}  t={t:.2f}s  {where}\n            {msg}")
    for label, found, side in (("X", out_x, "outside x 81–929"), ("Y", out_y, "outside y 240–1560")):
        for name, hits in found.items():
            for t0, t1 in _ranges([h[0] for h in hits], step):
                if t1 - t0 < PERSIST:
                    continue
                hs = [h for h in hits if t0 <= h[0] <= t1]
                over = max(h[1] for h in hs)
                worst = max(hs, key=lambda h: h[1])
                x0, x1, y0, y1 = worst[2]
                bad += 1
                sev = "!" if over > 40 else "·"
                print(f"  {sev} SAFE-{label}  {name}  {t0:.2f}–{t1:.2f}s  {side} by {over:.0f}px "
                      f"(worst t={worst[0]:.2f}: offending ink x {x0:.0f}–{x1:.0f}, y {y0:.0f}–{y1:.0f})")
    for name, (t, size, text) in small.items():
        bad += 1
        print(f"  ! TEXT    {name}  t={t:.2f}s  {size:.1f}px < {MIN_TEXT}: {text[:40]!r}")
    print("  ok — no problems" if not bad else f"  {bad} problem(s)")
    return 1 if errors else 0


def audio_dry(slug):
    """Compose the generated score + SFX track in memory (nothing written): exceptions, NaN, clipping, length."""
    import time
    from .audio import music, sfx
    project, video = _video(slug)
    t0 = time.time()
    problems = []
    try:
        y = music.compose(video, slug)
        if y is not None:
            if not np.isfinite(y).all():
                problems.append("music: NaN/inf in the score")
            if abs(len(y) / music.SR - video.duration) > 0.05:
                problems.append(f"music: length {len(y) / music.SR:.2f}s ≠ video {video.duration:.2f}s")
            desc = f"music {music.style_of(video)} {'stereo' if y.ndim == 2 else 'mono'} peak {np.abs(y).max():.2f}"
        else:
            desc = "music off"
        kit = getattr(video, "sfx_kit", None)
        cfg = music.config(video, slug)
        fx = sfx.track(video.all_cues(), video.duration, kit, cfg[0] if cfg else "C", bool(cfg) and cfg[1] == "tense")
        if not np.isfinite(fx).all():
            problems.append("sfx: NaN/inf")
        desc += f" · sfx {kit or 'classic'} {len(video.all_cues())} cues peak {np.abs(fx).max():.2f}"
    except Exception as e:  # noqa: BLE001 — report, don't crash the check
        tb = traceback.extract_tb(e.__traceback__)[-1]
        problems.append(f"✗ ERROR {type(e).__name__}: {e}  ({tb.filename.split('/')[-1]}:{tb.lineno})")
        desc = "audio"
    print(f"{slug}: audio dry · {desc} · {time.time() - t0:.1f}s · nothing written")
    for pr in problems:
        print(f"  {pr}")
    print("  ok — no problems" if not problems else f"  {len(problems)} problem(s)")
    return 1 if problems else 0
