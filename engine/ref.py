"""Study a reference (from cheese `ref`): take its grammar — pace, palette, type, transitions — never its content.

    python -m engine ref <slug> <video|image> [--every 0.5]          (Claude may run: decode + PNG only, no encode)

A video → videos/<slug>/refs/<name>/: contact.png (one frame every `every` s, timestamped), cuts.json (detected cuts
+ shot lengths = the pacing), audio.wav (to measure its beat if wanted). An image → copied to refs/.
"""
import json
import re
import shutil
import subprocess
import sys

from .project import ROOT

FONT = ROOT / "assets" / "fonts" / "JetBrainsMono-Bold.ttf"
MAX_FRAMES = 120


def _probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    vid = next((s for s in d["streams"] if s["codec_type"] == "video"), {})
    return (float(d["format"].get("duration", 0)), vid.get("width", 0), vid.get("height", 0),
            any(s["codec_type"] == "audio" for s in d["streams"]))


def detect_cuts(path, low=0.09, ratio=5.0):
    """Adaptive cut detection: a frame is a cut when its scene score is a local peak, above `low` and `ratio`× the
    median of the surrounding second (a fixed threshold misses cuts in dark, minimal motion graphics)."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-i", str(path), "-vf",
                        "scale=270:-2,select='gte(scene,0)',metadata=print:key=lavfi.scene_score:file=-",
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    pts = [(float(a), float(b)) for a, b in re.findall(r"pts_time:([\d.]+)\s+lavfi\.scene_score=([\d.]+)", r.stdout)]
    cuts = []
    for i in range(1, len(pts)):
        t, sc = pts[i]
        prev = pts[i - 1][1]
        nxt = pts[i + 1][1] if i + 1 < len(pts) else 0
        if t < 0.1 or sc < low or sc < prev or sc < nxt:
            continue
        win = sorted(p[1] for j, p in enumerate(pts[max(0, i - 15):i + 16]) if j != min(i, 15))
        median = win[len(win) // 2] if win else 0
        if sc >= ratio * max(median, 0.004) and (not cuts or t - cuts[-1] > 0.2):
            cuts.append(round(t, 3))
    return cuts


def ref(project, src, every=0.5):
    import os
    from pathlib import Path
    src = (Path(os.environ.get("CV_CWD", ".")) / Path(src).expanduser()).resolve()   # vid cd's into the repo
    if not src.exists():
        sys.exit(f"not found: {src}")
    name = re.sub(r"[^\w-]+", "-", src.stem)
    refs = project.dir / "refs"
    if src.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
        refs.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, refs / f"{name}{src.suffix.lower()}")
        print(f"✓ {(refs / (name + src.suffix.lower())).relative_to(ROOT)}  — read it, take the look (palette, type, "
              "composition), never the content")
        return 0
    d = refs / name
    d.mkdir(parents=True, exist_ok=True)
    dur, w, h, has_audio = _probe(src)
    every = max(every, dur / MAX_FRAMES)
    n = int(dur / every)
    cols = 4 if w > h else 8
    rows = -(-n // cols)
    tile = 320 if w > h else 180
    label = (f"drawtext=fontfile={FONT}:text='%{{pts\\:hms}}':x=6:y=6:fontsize={tile // 12}:fontcolor=white:"
             "box=1:boxcolor=black@0.6:boxborderw=3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf",
                    f"fps=1/{every},scale={tile}:-2,{label},tile={cols}x{rows}:padding=4:margin=4",
                    "-frames:v", "1", "-update", "1", str(d / "contact.png")], check=True)
    cuts = detect_cuts(src)
    bounds = [0.0, *cuts, dur]
    shots = [round(b - a, 3) for a, b in zip(bounds, bounds[1:])]
    avg = sum(shots) / len(shots) if shots else dur
    (d / "cuts.json").write_text(json.dumps(dict(source=str(src), duration=round(dur, 3), width=w, height=h,
                                                 cuts=cuts, shots=shots, average_shot=round(avg, 3)), indent=1))
    if has_audio:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-ac", "2", "-ar", "48000",
                        str(d / "audio.wav")], check=True)
    rel = d.relative_to(ROOT)
    print(f"✓ {rel}/  {dur:.1f}s {w}×{h} · {len(cuts)} cuts · average shot {avg:.2f}s"
          + (" · audio.wav" if has_audio else ""))
    print(f"  read {rel}/contact.png → write the look into PLAN.md (palette hex, type, shot length, transitions, "
          "how text enters) — the grammar, never the content")
    return 0
