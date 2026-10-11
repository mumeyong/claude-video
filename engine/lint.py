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
import math
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
            for hook in ("stage", "finish"):           # Video.stage / Video.finish (material looks): exceptions only
                fn = getattr(video, hook, None)
                if fn is None or hook in errors:
                    continue
                surf, c = new_frame(SCALE)
                c.dark = video.dark_amount(t)
                try:
                    fn(c, t)
                except Exception as ex:  # noqa: BLE001
                    f = traceback.extract_tb(ex.__traceback__)[-1]
                    errors[hook] = (t, f"{type(ex).__name__}: {ex}", f"{f.filename.split('claude-video/')[-1]}:{f.lineno}")
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
                if ly.bleed:
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


# ── motion check (STYLE §6f, 2026-10-11): measure how the video MOVES, without rendering anything ──────────
# The content layers (z < 100: content + screen-fixed UI; no camera, background, HUD or full-screen overlays) are composited off-screen every M_STEP s; consecutive
# alpha masks are diffed on a coarse grid. A grid cell "moves" when enough of its ink changed; neighbouring moving
# cells form one "mover". The camera is measured separately from v.camera.state(t).
M_STEP = 1 / 15
M_DIFF = 48            # alpha change (0-255) that counts as motion
M_CELL = (6, 10)       # grid: 6 columns × 10 rows (~180 px cells)
M_CELL_MIN = 0.012     # fraction of a cell's pixels that must change
CAM_ZOOM_V, CAM_PAN_V = 0.035, 70     # camera faster than this (zoom/s, px/s) = a real move (a dolly stays below)
REST_MIN, REST_BAD = 0.45, 0.30       # share of a chapter that should be still (holds) / clearly too busy
BUSY_MAX, BUSY_BAD = 2.5, 4.0         # longest stretch without a single still moment (s)
CROWD_N, CROWD_T = 3, 0.5             # ≥ 3 movers at once for ≥ 0.5 s = no clear leader


def _movers(cells):
    """Count 4-connected groups of True in a small 2-D bool grid."""
    rows, cols = cells.shape
    seen = np.zeros_like(cells)
    n = 0
    for r in range(rows):
        for c_ in range(cols):
            if cells[r, c_] and not seen[r, c_]:
                n += 1
                stack = [(r, c_)]
                seen[r, c_] = True
                while stack:
                    y, x = stack.pop()
                    for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= yy < rows and 0 <= xx < cols and cells[yy, xx] and not seen[yy, xx]:
                            seen[yy, xx] = True
                            stack.append((yy, xx))
    return n


def _spans(flags, ts, min_len):
    out, s0 = [], None
    for f, t in zip(flags + [False], ts + [ts[-1] + M_STEP if ts else 0]):
        if f and s0 is None:
            s0 = t
        elif not f and s0 is not None:
            if t - s0 >= min_len:
                out.append((s0, t))
            s0 = None
    return out


def motion_profile(video):
    """[(t, movers, ink_moving_fraction, camera_moving)] sampled every M_STEP s."""
    cols, rows = M_CELL
    prev, out = None, []
    n = int(video.duration / M_STEP) + 1
    for i in range(n):
        t = i * M_STEP
        surf, c = new_frame(SCALE)
        c.dark = video.dark_amount(t)
        for ly in sorted((l for l in video.layers if l.start <= t < l.end and l.z < 100), key=lambda l: l.z):
            try:
                c.ctx.save()
                ly.fn(c, t)
                c.ctx.restore()
            except Exception:  # noqa: BLE001 — dry_check reports exceptions; here they just don't count
                c.ctx.restore()
        a = _alpha(surf).astype(np.int16)[:, :int(tk.W * SCALE)]
        z0, x0, y0 = video.camera.state(max(0.0, t - M_STEP))
        z1, x1, y1 = video.camera.state(t)
        cam = abs(z1 - z0) / M_STEP > CAM_ZOOM_V or math.hypot(x1 - x0, y1 - y0) / M_STEP > CAM_PAN_V
        if prev is None:
            out.append((t, 0, 0.0, cam))
        else:
            d = np.abs(a - prev) > M_DIFF
            h, w = d.shape
            ch, cw = h // rows, w // cols
            grid = d[:ch * rows, :cw * cols].reshape(rows, ch, cols, cw).mean(axis=(1, 3)) > M_CELL_MIN
            ink = max(1, int((a > 90).sum()))
            out.append((t, _movers(grid), float(d.sum()) / ink, cam))
        prev = a
    return out


def motion_check(slug):
    """Per chapter: how much is still (holds), the longest stretch without rest, crowd moments (no single leader),
    camera moves stacked on content moves. Advisory — fix every `!` before handing over a render command."""
    project, video = _video(slug)
    prof = motion_profile(video)
    chs = video.chapters or []
    spans = [(ch.label, ch.start, ch.end) for ch in chs] or [("video", 0.0, video.duration)]
    print(f"{slug}: motion check · {len(prof)} samples every {M_STEP:.3f}s · nothing written")
    print(f"  {'chapter':<22}{'still':>7}{'longest busy':>14}{'peak movers':>13}")
    flags = 0
    for label, s, e in spans:
        rows = [p for p in prof if s <= p[0] < e]
        if not rows:
            continue
        still = [p[1] == 0 and not p[3] for p in rows]
        ts = [p[0] for p in rows]
        share = sum(still) / len(rows)
        busy = max([b - a for a, b in _spans([not x for x in still], ts, 0.0)] or [0.0])
        peak = max(p[1] for p in rows)
        mark = "!" if share < REST_BAD or busy > BUSY_BAD else ("~" if share < REST_MIN or busy > BUSY_MAX else " ")
        print(f"{mark} {label[:22]:<22}{share * 100:>6.0f}%{busy:>12.1f} s{peak:>13}")
        if mark == "!":
            flags += 1
        crowd = _spans([p[1] >= CROWD_N for p in rows], ts, CROWD_T)
        for a, b in crowd:
            flags += 1
            print(f"    ! CROWD {a:.2f}–{b:.2f}s  {CROWD_N}+ things move at once — pick one leader, delay the rest "
                  f"(follow()) or hold them still")
        stack = _spans([p[3] and p[1] >= 2 for p in rows], ts, 0.3)
        for a, b in stack:
            flags += 1
            print(f"    ! STACK {a:.2f}–{b:.2f}s  camera move on top of 2+ content moves — move the camera in a hold")
    tot = sum(p[1] == 0 and not p[3] for p in prof) / max(1, len(prof))
    print(f"  overall still {tot * 100:.0f}% (aim ≥ {REST_MIN * 100:.0f}% per chapter) · "
          + ("ok — no motion flags" if not flags else f"{flags} motion flag(s)"))
    return 0
