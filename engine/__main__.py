"""CLI.  python -m engine <command> <slug> [options]

  go       <slug> [final]         ONE command per review round: naskah → estimate/align → check →
                                  sheet → stills (from REVIEW file) → preview  ('final' = final render)
  new      "Judul video"          scaffold videos/<slug> from a title (slug auto)
  ls                              list videos with stage + duration
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

    if a.cmd in ("ls", "list"):
        return list_videos()
    if a.cmd == "sfx":
        from .audio.sfx import export_library
        export_library(ROOT / ".cache" / "sfx_preview")
        return 0
    if not a.slug:
        ap.error("slug required")

    if a.cmd == "new":
        return new_video(" ".join([a.slug] + a.rest))

    p = Project(a.slug)
    if a.cmd == "go":
        return go(p, a)
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


def slugify(title):
    import re
    import unicodedata
    s = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:48].rstrip("-") or "video"


def new_video(title):
    """Scaffold videos/<slug>/ from a title: SCRIPT.md + TREATMENT.md skeletons (Claude fills them)."""
    import datetime
    title = title.strip().strip('"')
    slug = slugify(title)
    dst = ROOT / "videos" / slug
    if dst.exists():
        sys.exit(f"sudah ada: {dst}")
    for d in ("audio", "assets", "out"):
        (dst / d).mkdir(parents=True)
    (dst / "SCRIPT.md").write_text(f"""# {title}

> Dibuat {datetime.date.today()} · status: brief — minta Claude: "kerjain video {slug}"
> Satu kalimat per [Lxx]. Tanda baca-keras: *kata* = tekanan, ' //' = napas.

## INTRO
[L01] (hook)

## 00 · BAB PERTAMA
[L02] …

## RECAP
[L03] …

## OUTRO
[L04] Follow, …
""")
    (dst / "TREATMENT.md").write_text(f"# TREATMENT — {title}\n\n> Diisi setelah SCRIPT.md di-approve (fase 2).\n")
    (dst / "REVIEW").write_text("# Stills untuk putaran review (diisi Claude)\n")
    print(f"✓ videos/{slug}/  —  \"{title}\"")
    print(f"  lanjut di Claude Code (folder {ROOT}):")
    print(f"    \"kerjain video {slug}\"   → brief, naskah + NASKAH.md, storyboard, kode")
    print(f"  setelah ada scenes.py:  claude-video {slug}")
    return 0


def list_videos():
    import json
    vids = sorted(d for d in (ROOT / "videos").iterdir() if d.is_dir() and not d.name.startswith((".", "_")))
    print(f"{'video':28s} {'tahap':22s} {'durasi':>7s}  judul")
    for d in vids:
        title = next((ln[2:].strip() for ln in open(d / "SCRIPT.md", encoding="utf-8") if ln.startswith("# ")),
                     "") if (d / "SCRIPT.md").exists() else ""
        dur = ""
        if (d / "timing.json").exists():
            tj = json.load(open(d / "timing.json"))
            dur = f"{tj['duration']:.0f}s" + ("" if tj.get("source") == "whisper" else "~")
        if (ROOT / "hasil" / d.name / f"{d.name}.mp4").exists():
            stage = "📦 final"
        elif (d / "out" / "preview.mp4").exists():
            stage = "🔁 review"
        elif (d / "scenes.py").exists():
            stage = "🎬 kode siap"
        elif (d / "TREATMENT.md").exists() and (d / "TREATMENT.md").stat().st_size > 200:
            stage = "🗒 storyboard"
        elif (d / "SCRIPT.md").exists() and "[L05]" in (d / "SCRIPT.md").read_text():
            stage = "✍️ naskah"
        else:
            stage = "💡 brief"
        voice = " 🎙" if (d / "audio" / "voice.wav").exists() else ""
        print(f"{d.name:28s} {stage + voice:22s} {dur:>7s}  {title}")
    print("\n  claude-video <video>        review   ·   claude-video <video> final   ·   claude-video \"Judul baru\"")
    return 0


def _newer(a, b):
    """True if file a exists and is newer than b (or b is missing)."""
    return a.exists() and (not b.exists() or a.stat().st_mtime > b.stat().st_mtime)


def go(p, a):
    """One command for a review round: naskah → timing → check → sheet → stills → preview (or final).

    Only redoes what is out of date. Stills: line ids / seconds listed in videos/<slug>/REVIEW (one per line
    or space-separated; '#' comments) — Claude keeps that file updated with what to look at this round.
    """
    import json
    import time
    t0 = time.time()
    final = "final" in a.rest
    script, naskah, timing = p.dir / "SCRIPT.md", p.dir / "NASKAH.md", p.timing_path
    done = []

    def step(msg):
        print(f"\n━━ {msg}")

    if _newer(script, naskah):
        step("naskah (SCRIPT.md berubah)")
        from .naskah import build_naskah
        build_naskah(script, naskah)
        done.append(f"NASKAH.md   {naskah}")

    src = json.load(open(timing)).get("source") if timing.exists() else None
    voice = p.voice()
    if voice and (src != "whisper" or _newer(voice, timing) or _newer(script, timing)):
        step("align (voice.wav baru / berubah)")
        from .audio.align import align
        align(script, voice, timing, model=a.model)
    elif not voice and (src is None or _newer(script, timing)):
        step("estimate (belum ada voice.wav)")
        from .audio.align import estimate
        estimate(script, timing)

    step("check")
    from . import render
    if render.check(p.slug):
        sys.exit("check gagal — kirim output ini ke Claude")

    if not final:
        step("sheet")
        done.append(f"sheet       {render.render_sheet(p.slug)}")
        rv = p.dir / "REVIEW"
        if rv.exists():
            ids = [w for ln in rv.read_text().splitlines() for w in ln.split("#")[0].split()]
            if ids:
                step(f"stills ({len(ids)})")
                tm = p.timing
                times = [tm.line(x).frac(0.6) if x.upper().startswith("L") else float(x) for x in ids]
                render.render_stills(p.slug, times, a.scale)
                done.append(f"stills      {p.out / 'stills'}/")

    step("render final 1080×1920 60fps" if final else "preview 540×960 30fps")
    out = render.render_video(p.slug, "final" if final else "preview", a.workers, a.t_from, a.t_to,
                              audio=not a.no_audio)
    done.append(f"{'final' if final else 'preview':11s} {out}")

    print(f"\n✓ selesai dalam {time.time() - t0:.0f}s — kirim ke Claude:")
    for d in done:
        print(f"  {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
