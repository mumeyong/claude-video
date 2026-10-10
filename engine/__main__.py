"""CLI.  python -m engine <command> <slug> [options]

  go       <slug> [preview]       ONE command: naskah → voice (align voice.wav, else TTS) → check → final render
                                  → hasil/<slug>/.  'preview' = review round instead: cover → sheet → stills
                                  (REVIEW) → 540p preview+music
  auto     "Judul video" | NN | <slug>  autopilot: scaffold (if new) → Claude headless writes idea, SCRIPT, NASKAH,
                                  PLAN, scenes.py, cover, POST.md until check --dry is clean → go (final render)
                                  (user runs — it starts Claude; Claude itself never runs this)
  new      "Judul video" | NN     scaffold videos/<slug> from a title or idea number; a matching ideas/NN-*.md
                                  (by number, title or slug) gives the slug + brief
  ideas                           list ideas that are not produced yet (number, pillar, title)
  ls                              list videos with stage + duration
  estimate <slug>                 timing.json from SCRIPT.md (no audio yet, 161 wpm)      (Claude may run)
  naskah   <slug>                 NASKAH.md — clean read-aloud script for recording      (Claude may run)
  align    <slug> [--model small] timing.json from audio/voice.wav via faster-whisper
  check    <slug> [--dry]         build only — validates structure; --dry also runs every draw fn off-screen
                                  (errors, safe column, tiny text; writes nothing)        (Claude may run)
  still    <slug> <t> [<t>...]    PNG frames at times (seconds) or line ids (L05)     (user runs)
  cover    <slug>                 TikTok cover → out/cover.png (v.cover, else frame at v.cover_t) (user runs)
  sheet    <slug>                 contact sheet, one thumbnail per script line          (user runs)
  preview  <slug> [--from s --to s]  540x960 30fps quick render with audio           (user runs)
  render   <slug> [--from s --to s]  1080x1920 60fps final                           (user runs)
  tts      <slug>                 Mumeyong voice → audio/voice_tts.wav + exact timing.json (edge-tts, online;
                                  automatic in go when there is no voice.wav; voice.wav always wins) (user runs)
  mix      <slug>                 audio only → out/mix.wav                              (user runs)
  music    <slug>                 generated score only → out/music_gen.wav (if no audio/music.*) (user runs)
  register <slug>                 index rows (ideas/REGISTRY.md, hasil/README.md) from PLAN.md   (Claude may run)
  api                             engine/API.md — one line per component (Claude reads this, not the sources)
  sfx                             export synth SFX (classic + kit strips) to .cache/sfx_preview to audition
  audition                        40 s demo per music style + SFX kit strips → .cache/audition/   (user runs)
"""
import argparse
import re
import shutil
import sys

from . import draw  # noqa: F401  (font setup first)
from .project import Project, ROOT, find


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
    ap.add_argument("--dry", action="store_true", help="check: also run every draw fn off-screen (nothing written)")
    a = ap.parse_args(argv)

    if a.cmd in ("ls", "list"):
        return list_videos()
    if a.cmd == "ideas":
        return list_ideas()
    if a.cmd == "api":
        from .apidoc import build_api
        build_api()
        return 0
    if a.cmd == "sfx":
        from .audio.sfx import export_library
        export_library(ROOT / ".cache" / "sfx_preview")
        return 0
    if a.cmd == "audition":
        from .audio.score import audition
        audition(ROOT / ".cache" / "audition")
        return 0
    if not a.slug:
        ap.error("slug required")

    if a.cmd == "new":
        return new_video(" ".join([a.slug] + a.rest))
    if a.cmd == "auto":
        return auto(a)

    p = Project(a.slug)
    if a.cmd == "go":
        return go(p, a)
    if a.cmd == "estimate":
        from .audio.align import estimate
        estimate(p.dir / "SCRIPT.md", p.timing_path)
    elif a.cmd == "register":
        from .registry import register
        register(a.slug)
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
        rc = check(a.slug)
        if a.dry:
            from .lint import dry_check, audio_dry, motion_check
            rc = max(rc, dry_check(a.slug), audio_dry(a.slug), motion_check(a.slug))
        return rc
    elif a.cmd == "still":
        from .render import render_stills
        times = []
        for x in a.rest:
            times.append(p.timing.line(x).frac(0.6) if x.upper().startswith("L") else float(x))
        render_stills(a.slug, times, a.scale)
    elif a.cmd == "cover":
        from .render import render_cover, _video
        render_cover(*_video(a.slug), p.out / "cover.png")
    elif a.cmd == "sheet":
        from .render import render_sheet
        render_sheet(a.slug)
    elif a.cmd in ("preview", "render"):
        from .render import render_video
        render_video(a.slug, "preview" if a.cmd == "preview" else "final", a.workers, a.t_from, a.t_to,
                     audio=not a.no_audio)
    elif a.cmd == "tts":
        from .audio.tts import synthesize
        synthesize(p)
    elif a.cmd == "music":
        from .audio.music import write_music
        out = write_music(p.build(), a.slug, p.out / "music_gen.wav")
        print(f"✓ {out}" if out else "music off (v.music = False)")
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


def _ideas():
    """[(num, title, slug, status, pillar, path)] from ideas/NN-*.md."""
    out = []
    for f in sorted((ROOT / "ideas").glob("[0-9][0-9]-*.md")):
        txt = f.read_text(encoding="utf-8")
        title = next((ln[2:].strip() for ln in txt.splitlines() if ln.startswith("# ")), f.stem)
        field = lambda k: (re.search(rf"\*\*{k}:\*\*\s*([^\n]*)", txt) or [None, ""])[1].strip()
        slug = re.sub(r"[`<].*", "", field("Slug")).strip() or f.stem[3:]
        out.append((f.name[:2], title, slug, field("Status"), field("Pilar").split(" · **")[0].strip(), f))
    return out


def find_idea(arg):
    key = arg.strip().lstrip("#")
    for idea in _ideas():
        num, title, slug, *_ = idea
        if key == num or key.zfill(2) == num or slugify(arg) in (slug, slugify(title)):
            return idea
    return None


def list_ideas():
    for num, title, slug, status, pillar, _ in _ideas():
        if not status.startswith(("💡", "⭐")) or "<" in slug or "format" in status:
            continue
        print(f"{num}  {pillar[:20]:20s} {title}")
    print('\n  claude-video <nomor>   atau   claude-video "Judul persis"   → bikin videos/<slug>/ dari ide itu')
    return 0


def new_video(title, hint=True):
    """Scaffold videos/<slug>/ from a title or idea number: SCRIPT.md skeleton (Claude fills it, then PLAN.md)."""
    import datetime
    title = title.strip().strip('"')
    idea = find_idea(title)
    if idea:
        _, title, slug, _, _, idea_path = idea
    elif title.lstrip("#").isdigit():
        sys.exit(f"nggak ada ide nomor {title} — lihat: claude-video ideas")
    else:
        slug = slugify(title)
    dst = ROOT / "videos" / slug
    if find("videos", slug).exists():
        sys.exit(f"sudah ada: {dst}")
    for d in ("audio", "assets", "out"):
        (dst / d).mkdir(parents=True)
    brief = f"\n> Ide: [ideas/{idea_path.name}](../../ideas/{idea_path.name}) — brief, hook, bab ada di sana" if idea else ""
    (dst / "SCRIPT.md").write_text(f"""# {title}

> Dibuat {datetime.date.today()} · status: brief — minta Claude: "kerjain video {slug}"{brief}
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
    (dst / "REVIEW").write_text("# Stills untuk putaran review (diisi Claude)\n")
    if idea:
        txt = idea_path.read_text(encoding="utf-8")
        txt = re.sub(r"(\*\*Status:\*\*\s*)[^\n]*", rf"\g<1>🎬 produksi — [`videos/{slug}/`](../videos/{slug}/)", txt, count=1)
        idea_path.write_text(txt, encoding="utf-8")
    print(f"✓ videos/{slug}/  —  \"{title}\"" + (f"  (dari ide {idea_path.name})" if idea else ""))
    if not hint:
        return 0
    print(f"  lanjut di Claude Code (folder {ROOT}):")
    print(f"    \"kerjain video {slug}\"   → brief, naskah + NASKAH.md, storyboard, kode (+ status di ideas/README.md)")
    print(f"  setelah ada scenes.py:  claude-video {slug}")
    return 0


def resolve(arg):
    """(slug, title) for an existing slug, an idea number/title, or a new title."""
    arg = arg.strip().strip('"')
    if find("videos", arg).exists():
        return arg, arg
    idea = find_idea(arg)
    if idea:
        return idea[2], idea[1]
    if arg.lstrip("#").isdigit():
        sys.exit(f"nggak ada ide nomor {arg} — lihat: claude-video ideas")
    return slugify(arg), arg


def auto(a):
    """Title/idea/slug → scaffold if new → Claude headless writes everything (if no scenes.py yet) → go."""
    slug, title = resolve(" ".join([a.slug] + [x for x in a.rest if x not in ("final", "preview")]))
    d = find("videos", slug)
    if not d.exists():
        new_video(title, hint=False)
    if not (find("videos", slug) / "scenes.py").exists():
        from .autopilot import autopilot
        if autopilot(slug, title):
            return 1
    return go(Project(slug), a)


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
        if (find("hasil", d.name) / f"{d.name}.mp4").exists():
            stage = "📦 final"
        elif (d / "out" / "preview.mp4").exists():
            stage = "🔁 review"
        elif (d / "scenes.py").exists():
            stage = "🎬 kode siap"
        elif (d / "PLAN.md").exists() or ((d / "TREATMENT.md").exists() and (d / "TREATMENT.md").stat().st_size > 200):
            stage = "🗒 storyboard"
        elif (d / "SCRIPT.md").exists() and "[L05]" in (d / "SCRIPT.md").read_text():
            stage = "✍️ naskah"
        else:
            stage = "💡 brief"
        voice = " 🎙" if (d / "audio" / "voice.wav").exists() else ""
        print(f"{d.name:28s} {stage + voice:22s} {dur:>7s}  {title}")
    for sub in sorted(x for x in (ROOT / "videos").iterdir() if x.is_dir() and x.name.startswith("_")):
        names = sorted(x.name for x in sub.iterdir() if x.is_dir() and not x.name.startswith((".", "_")))
        if names:
            print(f"  videos/{sub.name}/ ({len(names)}): {', '.join(names)}")
    print("\n  claude-video <video>        review   ·   claude-video <video> final   ·   claude-video \"Judul baru\"")
    return 0


def _newer(a, b):
    """True if file a exists and is newer than b (or b is missing)."""
    return a.exists() and (not b.exists() or a.stat().st_mtime > b.stat().st_mtime)


def go(p, a):
    """One command: naskah → voice (recording → align · none → TTS) → check → final render → hasil/<slug>/.
    'preview' in the args = review round instead: cover → sheet → stills → 540p preview with music.

    Only redoes what is out of date. Stills: line ids / seconds listed in videos/<slug>/REVIEW (one per line
    or space-separated; '#' comments) — Claude keeps that file updated with what to look at this round.
    """
    import json
    import time
    t0 = time.time()
    final = "preview" not in a.rest
    script, naskah, timing = p.dir / "SCRIPT.md", p.dir / "NASKAH.md", p.timing_path
    done = []

    def step(msg):
        print(f"\n━━ {msg}")

    if not (p.dir / "scenes.py").exists():   # still a brief: no script/voice/render work to do yet
        print(f"videos/{p.slug}/ masih brief (belum ada naskah + scenes.py).\n"
              f"  autopilot: claude-video auto {p.slug}   (atau di Claude Code: \"kerjain video {p.slug}\")")
        return 1

    if _newer(script, naskah):
        step("naskah (SCRIPT.md berubah)")
        from .naskah import build_naskah
        build_naskah(script, naskah)
        done.append(f"NASKAH.md   {naskah}")

    src = json.load(open(timing)).get("source") if timing.exists() else None
    real, synth = p.audio / "voice.wav", p.audio / "voice_tts.wav"
    if real.exists():
        if src != "whisper" or _newer(real, timing) or _newer(script, timing):
            step("align (voice.wav baru / berubah)")
            from .audio.align import align
            align(script, real, timing, model=a.model)
    else:
        # no recording → Mumeyong TTS voice. Redone only when the script changes (or an older TTS version is found).
        from .audio.tts import synthesize, VERSION
        prev = json.load(open(timing)) if timing.exists() else {}
        if src != "tts" or not synth.exists() or _newer(script, timing) or prev.get("tts") != VERSION:
            step("suara TTS (Mumeyong) — belum ada rekaman voice.wav")
            try:
                synthesize(p)
                done.append(f"voice_tts   {synth}")
            except (SystemExit, Exception) as e:   # offline / edge-tts missing → keep going without a voice
                print(f"  ! TTS gagal ({e}) — lanjut pakai timing estimasi (tanpa suara)")
                if src is None or _newer(script, timing):
                    from .audio.align import estimate
                    estimate(script, timing)

    step("check")
    from . import render
    if render.check(p.slug):
        sys.exit("check gagal — kirim output ini ke Claude")
    from .lint import dry_check
    if dry_check(p.slug):
        sys.exit("dry check: ada error di kode gambar — kirim output ini ke Claude")

    if not final:
        step("cover")
        pr, vd = render._video(p.slug)
        done.append(f"cover       {render.render_cover(pr, vd, p.out / 'cover.png')}")
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
    if final:
        from .project import find
        up = find("hasil", p.slug)
        print(f"\n▶ UPLOAD FILE INI (1080×1920 60fps): {up / (p.slug + '.mp4')}")
        print(f"  cover: {up / 'cover.png'} · caption: {up / 'POST.md'}")
        notes = p.out / "autopilot.md"
        if notes.exists() and "ertanyaan terbuka" in (txt := notes.read_text(encoding="utf-8")):
            print("\n⚠ CEK SEBELUM UPLOAD — pertanyaan terbuka dari autopilot (salah? bilang ke Claude, lalu ulang):")
            print(txt[txt.index("ertanyaan terbuka") - 1:].split("\n", 1)[-1].rstrip())
    else:
        print(f"\n  ⚠ preview = 540p, JANGAN di-upload. Buat upload: claude-video {p.slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
