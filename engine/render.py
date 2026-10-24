"""Rendering: stills, contact sheet, preview, final. Frames pipe straight into ffmpeg (no PNG dump).

Run by the USER, never by Claude (see CLAUDE.md rule 1).
"""
import multiprocessing as mp
import os
import shutil
import subprocess
import sys
import time

from . import tokens as tk
from .draw import frame_size, new_frame
from .project import Project
from .web import prepare

PRESETS = {
    #           scale  fps  x264 preset  crf
    "preview": (4 / 9, 30, "veryfast", 24),   # 480×854
    "final": (1.0, 60, "slow", 14),
}
# Motion blur (2026-10-13, refs.pdf §04: "60 fps, 4 subframes per frame, blended"): the final render averages
# SUBFRAMES draws spread over SHUTTER of the frame interval (1.0 = 360°), centred on t so arrivals stay on their word.
# A video can override with v.subframes / v.shutter. Frames where nothing moves are drawn once (no extra cost).
SUBFRAMES = {"preview": 1, "final": 4}
SHUTTER = 1.0
# Rough peak RAM per worker (python + its x264 encoder), GB. Full-res "slow" x264 keeps a deep
# lookahead + ref frames; 20 of those at once got the desktop OOM-killed.
_WORKER_GB = {"preview": 0.5, "final": 1.5}


def _mem_available_gb():
    try:
        for line in open("/proc/meminfo"):
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) / 1024 / 1024
    except OSError:
        pass
    return None


def _auto_workers(mode):
    n = max(1, (os.cpu_count() or 4) - 2)
    gb = _mem_available_gb()
    if gb is not None:
        n = min(n, max(1, int(gb * 0.7 / _WORKER_GB[mode])))  # keep 30% for the desktop
    return n

_W = {}  # per-process cache: slug → (project, video)


def _video(slug):
    if slug not in _W:
        p = Project(slug)
        _W[slug] = (p, p.build())
    return _W[slug]


def frame_bytes(video, t, scale):
    surf, c = new_frame(scale)
    video.draw(c, t)
    surf.flush()
    return surf, bytes(surf.get_data())


def _ffmpeg_cmd(out, w, h, fps, preset, crf, threads):
    return ["ffmpeg", "-v", "error", "-y", "-threads", str(threads),
            "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
            "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-threads", str(threads),
            "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-x264-params", "keyint=120", str(out)]


def blurred_bytes(video, t, fps, scale, n, shutter):
    """Frame at t with motion blur: mean of n subframes over shutter/fps seconds centred on t. If the first and last
    subframe are identical (a still frame), that one draw is returned as is."""
    if n <= 1:
        return frame_bytes(video, t, scale)[1]
    span = shutter / fps
    ts = [max(0.0, min(video.duration - 1e-6, t + span * ((k + 0.5) / n - 0.5))) for k in range(n)]
    first = frame_bytes(video, ts[0], scale)[1]
    last = frame_bytes(video, ts[-1], scale)[1]
    if first == last:
        return first
    import numpy as np
    acc = np.frombuffer(first, np.uint8).astype(np.uint32) + np.frombuffer(last, np.uint8)
    for tt in ts[1:-1]:
        acc += np.frombuffer(frame_bytes(video, tt, scale)[1], np.uint8)
    return ((acc + n // 2) // n).astype(np.uint8).tobytes()


def _render_chunk(args):
    slug, f0, f1, fps, scale, preset, crf, threads, out, mode = args
    _, video = _video(slug)
    w, h = frame_size(scale)
    n = getattr(video, "subframes", None) or SUBFRAMES[mode]
    shutter = getattr(video, "shutter", None) or SHUTTER
    proc = subprocess.Popen(_ffmpeg_cmd(out, w, h, fps, preset, crf, threads), stdin=subprocess.PIPE)
    for f in range(f0, f1):
        proc.stdin.write(blurred_bytes(video, f / fps, fps, scale, n, shutter))
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed on chunk {out}")
    return f1 - f0


def render_video(slug, mode="preview", workers=None, t_from=0.0, t_to=None, audio=True, fix=None):
    """fix=(a, b): HTML film only — re-render the film's frames for seconds a–b, reuse every other cached frame."""
    scale, fps, preset, crf = PRESETS[mode]
    project, video = _video(slug)
    t_to = min(video.duration, t_to if t_to is not None else video.duration)
    f_start, f_end = int(t_from * fps), int(round(t_to * fps))
    total = f_end - f_start
    if getattr(video, "web", None) is not None:          # HTML film: browser frames first (cached in out/.web/)
        from .web import SUB as WEB_SUB
        video.web.prepare_frames(fps, WEB_SUB[mode], f_start, f_end, fix)
    workers = workers or _auto_workers(mode)
    threads = max(1, (os.cpu_count() or 4) // workers)  # x264 default = 1.5×cores per encoder
    chunk = max(fps, -(-total // workers))  # ceil
    tmp = project.out / f".{mode}_chunks"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    jobs, f = [], f_start
    while f < f_end:
        g = min(f_end, f + chunk)
        jobs.append((slug, f, g, fps, scale, preset, crf, threads, tmp / f"c{len(jobs):04d}.mp4", mode))
        f = g
    sub = getattr(video, "subframes", None) or SUBFRAMES[mode]
    print(f"[{mode}] {slug}: {total} frames @ {fps}fps, scale {scale}, {len(jobs)} chunks, {workers} workers"
          + (f", motion blur {sub} subframes" if sub > 1 else ""))
    t0 = time.time()
    done = 0
    with mp.get_context("spawn").Pool(workers) as pool:
        for n in pool.imap_unordered(_render_chunk, jobs):
            done += n
            el = time.time() - t0
            print(f"\r  {done}/{total} frames  {done / el:5.1f} fps  eta {el / done * (total - done):5.0f}s",
                  end="", flush=True)
    print()
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{j[-2].name}'\n" for j in jobs))
    silent = tmp / "video.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(silent)], check=True)
    suffix = "" if (t_from == 0 and t_to >= video.duration) else f"_{t_from:g}-{t_to:g}"
    out = project.out / f"{mode}{suffix}.mp4"
    if audio:
        from .audio.mix import build_mix
        wav = build_mix(project, video, project.out / "mix.wav")
        if wav:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-ss", str(t_from),
                            "-t", str(t_to - t_from), "-i", str(wav), "-map", "0:v", "-map", "1:a",
                            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                            "-movflags", "+faststart", str(out)], check=True)
        else:
            shutil.move(silent, out)
    else:
        shutil.move(silent, out)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"✓ {out}  ({time.time() - t0:.0f}s)")
    if mode == "final" and not suffix:
        publish(project, video, out)
    return out


def publish(project, video, final_mp4):
    """Copy a full final render to hasil/<slug>/ with a cover frame. POST.md is written by Claude."""
    from .project import find
    d = find("hasil", project.slug)
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final_mp4, d / f"{project.slug}.mp4")
    render_cover(project, video, d / "cover.png")
    print(f"✓ {d}/  ({project.slug}.mp4 + cover.png)")
    if not (d / "POST.md").exists():
        print("  → minta Claude: \"bikinin POST.md buat " + project.slug + "\"")


# Upload targets (from cheese, unofficial, Oct 2026): length limit, warning, bitrate cap for a platform-safe encode.
PLATFORMS = {
    "tiktok": ("TikTok", 600, None, "12M"),
    "shorts": ("YouTube Shorts", 180, None, "16M"),
    "reels": ("Instagram/Facebook Reels", None, 90, "12M"),
}


def export(slug, targets=None):
    """hasil/<slug>/<slug>.mp4 → hasil/<slug>/upload/<slug>.<platform>.mp4: H.264 High 4.2, capped bitrate,
    2 s GOP, faststart — same picture, encodes each app accepts without crushing it again."""
    from .project import find
    d = find("hasil", slug)
    src = d / f"{slug}.mp4"
    if not src.exists():
        sys.exit(f"{src} missing — render first: souffle {slug}")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(src)], capture_output=True, text=True, check=True).stdout)
    up = d / "upload"
    up.mkdir(exist_ok=True)
    for key in targets or PLATFORMS:
        label, limit, warn, rate = PLATFORMS[key]
        if limit and dur > limit:
            print(f"  ! {label}: {dur:.0f}s > {limit}s — skipped")
            continue
        if warn and dur > warn:
            print(f"  ! {label}: over {warn}s may not be distributed as a reel")
        out = up / f"{slug}.{key}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-c:v", "libx264", "-preset", "slow",
                        "-profile:v", "high", "-level", "4.2", "-crf", "17", "-maxrate", rate,
                        "-bufsize", f"{int(rate[:-1]) * 2}M", "-pix_fmt", "yuv420p", "-g", str(2 * tk.FPS),
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-c:a", "copy", "-movflags", "+faststart", str(out)], check=True)
        print(f"✓ {label:26s} {out}")
    return up


def render_cover(project, video, path):
    """Designed cover (v.cover = fn(c)) if the video has one, else the frame at v.cover_t."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fn = getattr(video, "cover", None)
    if fn is not None:
        surf, c = new_frame(1.0)
        fn(c)
        surf.write_to_png(str(path))
    else:
        cover_t = getattr(video, "cover_t", None)
        if cover_t is None:
            cover_t = project.timing.lines[0].end if project.timing.lines else 1.5
        prepare(video, [cover_t])
        surf, _ = frame_bytes(video, cover_t, 1.0)
        surf.write_to_png(str(path))
    print(f"✓ {path}")
    return path


def render_stills(slug, times, scale=1.0):
    project, video = _video(slug)
    d = project.out / "stills"
    d.mkdir(parents=True, exist_ok=True)
    prepare(video, times)
    paths = []
    for t in times:
        surf, _ = frame_bytes(video, t, scale)
        p = d / f"t{t:07.2f}.png"
        surf.write_to_png(str(p))
        paths.append(p)
        print(f"✓ {p}")
    return paths


def render_sheet(slug, times=None, cols=6, scale=0.25, path=None, labels=None):
    """Contact sheet: one thumbnail per script line (at 60% through it) with time + line id."""
    import cairo
    from .draw import Canvas
    project, video = _video(slug)
    labels = list(labels or [])
    if times is None:
        times = []
        for ln in project.timing.lines:
            times.append(ln.frac(0.6))
            labels.append(ln.id)
    labels += [""] * (len(times) - len(labels))
    prepare(video, times)
    tw, th = int(tk.W * scale), int(tk.H * scale)
    rows = -(-len(times) // cols)
    sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * (tw + 8) + 8, rows * (th + 36) + 8)
    cx = cairo.Context(sheet)
    cx.set_source_rgb(0.1, 0.1, 0.12)
    cx.paint()
    lab = Canvas(cx)
    for i, (t, lb) in enumerate(zip(times, labels)):
        surf, _ = frame_bytes(video, t, scale)
        x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 36)
        cx.set_source_surface(surf, x, y)
        cx.paint()
        if getattr(video, "web", None) is not None:      # HTML film: the dry check can't see inside it — show the box
            from .web import SAFE
            cx.set_source_rgba(0.4, 1.0, 0.3, 0.7)
            cx.set_line_width(2)
            cx.rectangle(x + SAFE["x0"] * scale, y + SAFE["y0"] * scale, (SAFE["x1"] - SAFE["x0"]) * scale,
                         (SAFE["y1"] - SAFE["y0"]) * scale)
            cx.stroke()
        lab.text(x, y + th + 24, f"{lb}  {t:6.2f}s", tk.F["mono"], 16, (1, 1, 1, 0.8))
    p = path or project.out / "sheet.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    sheet.write_to_png(str(p))
    print(f"✓ {p}")
    return p


def render_critique(slug):
    """Review sheets for the critique loop (STYLE §6, refs.pdf §11) — PNG only at 1/4 scale, no encode, no audio,
    so Claude may run it and LOOK at the result:
      out/critique/sheet.png   one frame per script line (60 % through it) — readability, variety, brand
      out/critique/hook.png    8 frames over the first 2 s — is there a hook before the thumb scrolls on?
      out/critique/moves.png   each chapter's entrance as 6 frames 0.1 s apart — does the motion start at rest,
                               lead with one thing, and settle (no pop, no stop-and-go)?"""
    project, video = _video(slug)
    d = project.out / "critique"
    out = [render_sheet(slug, path=d / "sheet.png")]
    hook = [i * 2.0 / 7 for i in range(8)]
    out.append(render_sheet(slug, hook, cols=8, path=d / "hook.png", labels=["hook"] * 8))
    times, labels = [], []
    for ch in video.chapters:
        for k in range(6):
            times.append(min(video.duration - 0.01, ch.start + 0.1 * k))
            labels.append(f"{ch.label[:10]} +{0.1 * k:.1f}" if k else ch.label[:14])
    if times:
        out.append(render_sheet(slug, times, cols=6, path=d / "moves.png", labels=labels))
    return out


def check(slug):
    """Build the video WITHOUT drawing anything: validates timing refs, prints the structure."""
    project, video = _video(slug)
    tm = project.timing
    print(f"{slug}: {video.duration:.2f}s  timing={tm.source}  lines={len(tm.lines)}  bpm={video.bpm}")
    for ch in video.chapters:
        print(f"  {ch.start:7.2f}–{ch.end:7.2f}  {'■' if ch.dark else '□'} {ch.hud}")
    print(f"  layers={len(video.layers)}  sfx cues={len(video.all_cues())}")
    if project.music():
        print(f"  music: {project.music().name} (own track)")
    else:
        from .audio.music import plan
        for ln in plan(video, project.slug):
            print("  " + ln)
    bad = [ly for ly in video.layers if ly.end <= ly.start]
    if bad:
        print(f"  ! {len(bad)} layers with end <= start")
    late = [ly for ly in video.layers if ly.start >= video.duration]
    if late:
        print(f"  ! {len(late)} layers start after the end")
    print("  ok (nothing rendered)")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit("use: python -m engine <command> ...")
