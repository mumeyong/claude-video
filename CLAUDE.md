# MUMEYONG — motion video studio (Python + ffmpeg)

Vertical 1080×1920 / 60fps animated explainer videos in **Bahasa Indonesia**, in the light-glass
"UI keynote" style (see `.claude/skills/mumeyong-video/STYLE.md`). Every frame is code: `frame = f(t)`.
User-facing workflow guide: `START.md` — keep it in sync when commands or phases change.

## Aturan tetap (non-negotiable)

1. **Claude TIDAK PERNAH me-render.** Never run `still`, `sheet`, `preview`, `render`, `mix`, or any
   ffmpeg encode — not even "just one frame to check". Finish the code, then give the user the exact
   command(s) in a copy-paste block. The user renders on their own machine and reports back
   (screenshots, timecodes, errors). The only engine commands Claude may run are
   `python -m engine check <slug>` and `python -m engine estimate <slug>` (no image/audio output).
2. **Review dulu, kerjakan kemudian.** For every new video or big change: propose a plan, wait for "ok".
3. **Urutan wajib:** SCRIPT.md → (approved) → TREATMENT.md → (approved) → scenes.py → user renders
   stills/preview → feedback → final. Never write scenes.py before the treatment is approved.
4. **Jangan pernah `git commit` / `git push` tanpa nanya.** Suggest a commit message; the user decides.
5. **Every new video uses the skill** `mumeyong-video` (`.claude/skills/mumeyong-video/SKILL.md`).
6. **frame = f(t).** Draw functions are pure: no state carried between frames, no unseeded randomness,
   no wall-clock. Seeking to any second must produce the same picture as playing to it.
7. **Voice is the clock.** Times come from `timing.json` (`T.line("L07").start`, `T.word("L07", "kode")`),
   never hard-coded seconds. Only gaps/transitions may snap to `video.beat`.
8. **Tokens only.** Colors, sizes, fonts, easing, durations come from `engine/tokens.py` (mirror of
   STYLE.md). No magic hex values in scenes. New token → add it to both files.
9. **Banned list in STYLE.md is law.** If a request conflicts with it, say so before doing it.
10. **Engine vs video.** Reusable things go in `engine/components/`; one-off scene code stays in
    `videos/<slug>/scenes.py`. Don't fork a component for a one-time tweak — add a parameter.

## Layout

```
engine/            reusable engine (tokens, draw, video, timing, components/, audio/, render, CLI)
assets/fonts/      Inter, Inter Display, Instrument Serif Italic, JetBrains Mono
assets/sfx/        optional real SFX samples (<name>.wav overrides the synth)
videos/<slug>/     SCRIPT.md, TREATMENT.md, timing.json, scenes.py, audio/, assets/, out/
.claude/skills/mumeyong-video/   SKILL.md (workflow), STYLE.md (design system), templates/
```

## Commands (the user runs these — Claude only hands them over)

```bash
source .venv/bin/activate                          # venv uses system Pango/cairo (--system-site-packages)
python -m engine new <slug>                        # scaffold
python -m engine estimate <slug>                   # timing from script, before voice exists (Claude may run)
python -m engine align <slug>                      # timing from audio/voice.wav (whisper)
python -m engine check <slug>                      # structure check, no drawing (Claude may run)
python -m engine still <slug> L05 L12 33.5         # PNG stills → out/stills/
python -m engine sheet <slug>                      # contact sheet → out/sheet.png
python -m engine preview <slug> [--from 20 --to 40]  # 540x960 30fps + audio → out/preview.mp4
python -m engine render <slug>                     # 1080x1920 60fps final → out/final.mp4
```

## Gotchas

- faster-whisper: pass audio as a numpy array (PyAV here rejects `metadata_errors`). `align.py` already does.
- Pango must load fonts from `assets/fonts` — always `import engine` (it sets FONTCONFIG_FILE) before `gi`.
- Numbers on screen use Indonesian format: `2.951`, `44,4 s` → `fmt_id()`.
