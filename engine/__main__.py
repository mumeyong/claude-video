"""CLI.  python -m engine <command> <slug> [options]

  new      <slug>                 scaffold videos/<slug> from the skill templates
  estimate <slug>                 timing.json from SCRIPT.md (no audio yet, 161 wpm)      (Claude may run)
  naskah   <slug>                 NASKAH.md — clean read-aloud script for recording      (Claude may run)
  align    <slug> [--model small] timing.json from audio/voice.wav via faster-whisper
  check    <slug>                 build only, draws nothing — validates structure      (Claude may run)
  still    <slug> <t> [<t>...]    PNG frames at times (seconds) or line ids (L05)     (user runs)
  sheet    <slug>                 contact sheet, one thumbnail per script line          (user runs)
  preview  <slug> [--from s --to s]  540x960 30fps quick render with audio           (user runs)
  render   <slug> [--from s --to s]  1080x1920 60fps final                           (user runs)
  mix      <slug>                 audio only → out/mix.wav                              (user runs)
  sfx                             export synth SFX to .cache/sfx_preview to audition
"""
import argparse
import shutil
import sys

from . import draw  # noqa: F401  (font setup first)
from .project import Project, ROOT


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m engine", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd")
    ap.add_argument("slug", nargs="?")
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--model", default="small")
    ap.add_argument("--from", dest="t_from", type=float, default=0.0)
    ap.add_argument("--to", dest="t_to", type=float, default=None)
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--no-audio", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "sfx":
        from .audio.sfx import export_library
        export_library(ROOT / ".cache" / "sfx_preview")
        return 0
    if not a.slug:
        ap.error("slug required")

    if a.cmd == "new":
        dst = ROOT / "videos" / a.slug
        if dst.exists():
            sys.exit(f"{dst} already exists")
        shutil.copytree(ROOT / ".claude" / "skills" / "mumeyong-video" / "templates", dst)
        for d in ("audio", "assets", "out"):
            (dst / d).mkdir(exist_ok=True)
        print(f"✓ {dst}\n  next: write SCRIPT.md, then python -m engine estimate {a.slug}")
        return 0

    p = Project(a.slug)
    if a.cmd == "estimate":
        from .audio.align import estimate
        estimate(p.dir / "SCRIPT.md", p.timing_path)
    elif a.cmd == "naskah":
        from .naskah import build_naskah
        build_naskah(p.dir / "SCRIPT.md", p.dir / "NASKAH.md")
    elif a.cmd == "align":
        from .audio.align import align
        if not p.voice():
            sys.exit(f"missing {p.audio / 'voice.wav'}")
        align(p.dir / "SCRIPT.md", p.voice(), p.timing_path, model=a.model)
    elif a.cmd == "check":
        from .render import check
        return check(a.slug)
    elif a.cmd == "still":
        from .render import render_stills
        times = []
        for x in a.rest:
            times.append(p.timing.line(x).frac(0.6) if x.upper().startswith("L") else float(x))
        render_stills(a.slug, times, a.scale)
    elif a.cmd == "sheet":
        from .render import render_sheet
        render_sheet(a.slug)
    elif a.cmd in ("preview", "render"):
        from .render import render_video
        render_video(a.slug, "preview" if a.cmd == "preview" else "final", a.workers, a.t_from, a.t_to,
                     audio=not a.no_audio)
    elif a.cmd == "mix":
        from .audio.mix import build_mix
        build_mix(p, p.build(), p.out / "mix.wav")
    else:
        ap.error(f"unknown command {a.cmd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
