# MUMEYONG — motion video studio (Python + ffmpeg)

Vertical 1080×1920 / 60fps animated explainer videos in **Bahasa Indonesia**, in the light-glass
"UI keynote" style (see `.claude/skills/mumeyong-video/STYLE.md`). Every frame is code: `frame = f(t)`.
User-facing workflow guide: `START.md` — keep it in sync when commands or phases change.

## Aturan tetap (non-negotiable)

1. **Claude TIDAK PERNAH me-render.** Never run `still`, `sheet`, `preview`, `render`, `mix`, or any
   ffmpeg encode — not even "just one frame to check". Finish the code, then give the user the exact
   command(s) in a copy-paste block. The user renders on their own machine and reports back
   (screenshots, timecodes, errors). The only engine commands Claude may run are
   `check`, `estimate` and `naskah` (text/JSON only, no image/audio output).
2. **Autopilot — jangan berhenti di gate.** The user approves every gate by default ("oke" to everything).
   Don't stop to ask for ok between phases: make the best call yourself, write each phase's file, then move on.
   Run straight through to scenes.py + `check`, then stop and hand over the render command (rule 1).
   Only stop early if blocked on a fact only the user knows (real numbers, NDA, what actually happened) — and
   even then prefer a safe default (no number shown) and list the open question in the final message.
3. **Urutan wajib:** SCRIPT.md (+ NASKAH.md) → IDENTITY.md → TREATMENT.md → scenes.py → `check` → user renders
   stills/preview → feedback → final. The order stays; the waiting between steps doesn't (rule 2).
3b. **Every video ships a read-aloud script.** Whenever SCRIPT.md is written or changed, regenerate
   `NASKAH.md` with `python -m engine naskah <slug>` and tell the user. Never hand-edit NASKAH.md and
   never let it drift from SCRIPT.md — the user records voice.wav from it.
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
11. **Ideas live in `ideas/`** (strategy: `ideas/STRATEGY.md` — creator income, 3 broad : 1 career : 1 deep, QUICK vs FULL format). "Simpan ide" → new `NN-slug.md` from `_TEMPLATE.md` + a row in
    `ideas/README.md`. Starting production → status 🎬 and link `videos/<slug>/`. Keep the index in sync.
12. **Finished videos go to `hasil/`.** A full `render` auto-copies mp4 + cover.png there. When the user
    approves the final, write `hasil/<slug>/POST.md` from `.claude/skills/mumeyong-video/POST_TEMPLATE.md`
    (caption, hashtags, pinned comment) and update `hasil/README.md` + the idea's status.
13. **Unique, never generic.** Every video gets `IDENTITY.md` (phase 1.5) — metaphor, signature move/color,
    hook format, structure, new component — different from the previous video per `ideas/REGISTRY.md`
    (STYLE §6c). Brand DNA (HUD, type, accent blue, motion feel, outro) never changes.
14. **Tech terms stay English.** Never translate technical terms into Indonesian — in scripts, NASKAH, headlines,
    labels, tags. Indonesian is the glue; affixes are fine (di-scale, pod-nya). Check every script against
    `.claude/skills/mumeyong-video/GLOSSARY.md` before showing it.

## Layout

```
engine/            reusable engine (tokens, draw, video, timing, components/, audio/ (sfx, generated music, mix), render, CLI)
assets/fonts/      Inter, Inter Display, Instrument Serif Italic, JetBrains Mono
assets/sfx/        optional real SFX samples (<name>.wav overrides the synth)
videos/<slug>/     SCRIPT.md, TREATMENT.md, timing.json, scenes.py, audio/, assets/, out/
hasil/             finished videos: <slug>/<slug>.mp4 (git-ignored) + cover.png + POST.md; README.md index
ideas/             video idea backlog: README.md (index + status) + one NN-slug.md per idea
.claude/skills/mumeyong-video/   SKILL.md (workflow), STYLE.md (design system), templates/
```

## Commands (the user runs these — Claude only hands them over)

**Hand over ONE command per round:** `claude-video <slug>` (global command = `vid` symlinked into
~/.local/bin; works from any folder; `./vid` inside the repo is identical) (review) or `claude-video <slug> final`. Before handing it over,
update `videos/<slug>/REVIEW` with the line ids/seconds the user should look at as stills this round.

```bash
claude-video <slug>                      # review round: naskah → estimate/align (auto) → check → sheet → stills(REVIEW) → preview
claude-video <slug> final                # final 1080x1920 60fps → out/final.mp4 + hasil/<slug>/
claude-video <slug> --from 20 --to 45    # same, preview only that range
claude-video "Judul video"             # new video from a title (slug auto); `claude-video` alone = list
claude-video check <slug>                # structure check, no drawing (Claude may run; also estimate, naskah)
claude-video help                        # all low-level commands (still, sheet, preview, render, align, mix, sfx)
```

## Gotchas

- faster-whisper: pass audio as a numpy array (PyAV here rejects `metadata_errors`). `align.py` already does.
- Pango must load fonts from `assets/fonts` — always `import engine` (it sets FONTCONFIG_FILE) before `gi`.
- Numbers on screen use Indonesian format: `2.951`, `44,4 s` → `fmt_id()`.
