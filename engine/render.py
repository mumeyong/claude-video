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
from .draw import new_frame
from .project import Project

PRESETS = {
    #           scale  fps  x264 preset  crf
    "preview": (0.5, 30, "veryfast", 24),
    "final": (1.0, 60, "slow", 14),
}
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


def _render_chunk(args):
    slug, f0, f1, fps, scale, preset, crf, threads, out = args
    _, video = _video(slug)
    w, h = int(round(tk.W * scale)), int(round(tk.H * scale))
    proc = subprocess.Popen(_ffmpeg_cmd(out, w, h, fps, preset, crf, threads), stdin=subprocess.PIPE)
    for f in range(f0, f1):
        _, data = frame_bytes(video, f / fps, scale)
        proc.stdin.write(data)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed on chunk {out}")
    return f1 - f0


def render_video(slug, mode="preview", workers=None, t_from=0.0, t_to=None, audio=True):
    scale, fps, preset, crf = PRESETS[mode]
    project, video = _video(slug)
    t_to = min(video.duration, t_to if t_to is not None else video.duration)
    f_start, f_end = int(t_from * fps), int(round(t_to * fps))
    total = f_end - f_start
    workers = workers or _auto_workers(mode)
    threads = max(1, (os.cpu_count() or 4) // workers)  # x264 default = 1.5×cores per encoder
    chunk = max(fps, -(-total // workers))  # ceil
    tmp = project.out / f".{mode}_chunks"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    jobs, f = [], f_start
    while f < f_end:
        g = min(f_end, f + chunk)
        jobs.append((slug, f, g, fps, scale, preset, crf, threads, tmp / f"c{len(jobs):04d}.mp4"))
        f = g
    print(f"[{mode}] {slug}: {total} frames @ {fps}fps, scale {scale}, {len(jobs)} chunks, {workers} workers")
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
    lst.write_text("".join(f"file '{j[-1].name}'\n" for j in jobs))
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
    from .project import ROOT
    d = ROOT / "hasil" / project.slug
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final_mp4, d / f"{project.slug}.mp4")
    render_cover(project, video, d / "cover.png")
    print(f"✓ {d}/  ({project.slug}.mp4 + cover.png)")
    if not (d / "POST.md").exists():
        print("  → minta Claude: \"bikinin POST.md buat " + project.slug + "\"")


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
        surf, _ = frame_bytes(video, cover_t, 1.0)
        surf.write_to_png(str(path))
    print(f"✓ {path}")
    return path


def render_stills(slug, times, scale=1.0):
    project, video = _video(slug)
    d = project.out / "stills"
    d.mkdir(parents=True, exist_ok=True)
    paths = []
    for t in times:
        surf, _ = frame_bytes(video, t, scale)
        p = d / f"t{t:07.2f}.png"
        surf.write_to_png(str(p))
        paths.append(p)
        print(f"✓ {p}")
    return paths


def render_sheet(slug, times=None, cols=6, scale=0.25):
    """Contact sheet: one thumbnail per script line (at 60% through it) with time + line id."""
    import cairo
    from .draw import Canvas
    project, video = _video(slug)
    labels = []
    if times is None:
        times = []
        for ln in project.timing.lines:
            times.append(ln.frac(0.6))
            labels.append(ln.id)
    labels += [""] * (len(times) - len(labels))
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
        lab.text(x, y + th + 24, f"{lb}  {t:6.2f}s", tk.F["mono"], 16, (1, 1, 1, 0.8))
    p = project.out / "sheet.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    sheet.write_to_png(str(p))
    print(f"✓ {p}")
    return p


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
