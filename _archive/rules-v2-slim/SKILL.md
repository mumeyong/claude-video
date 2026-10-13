---
name: mumeyong-video
description: Make a MUMEYONG vertical (9:16) animated explainer video in Python + ffmpeg — script, plan, voice-timed scenes, self-check. Use for any new video, scene, or change to a video in videos/<slug>/. Claude writes the code; the USER renders.
---

# MUMEYONG video workflow

Read `STYLE.md` + `LESSONS.md` first. Never render (CLAUDE.md rule 1); don't stop at gates (rule 2) — run straight
through to a clean check, then hand over ONE command. Open questions (real numbers, facts) go in the final message.

## 1. SCRIPT.md (+ NASKAH.md)
- From `templates/SCRIPT_QUICK.md` (default, 60–75 s, ~14–20 lines) or `templates/SCRIPT.md` (FULL, 90–150 s).
  `## INTRO` · `## 00 · LABEL` … · `## RECAP` · `## OUTRO`, one spoken sentence per `[Lxx]` line, ~2.7 words/s.
- Hook options A/B/C at the top (use A). Every line must earn a visual. `*kata*` = stress (the visual lands there),
  ` //` = breath. Numbers as spoken words. Check every line against `GLOSSARY.md`.
- Then `python -m engine naskah <slug>` (→ NASKAH.md, never hand-edit) + `python -m engine estimate <slug>`.

## 2. PLAN.md
- From `templates/PLAN.md`: the registry block + identity table (STYLE §3, all different from `recent <slug>`) +
  one composition row per chapter (STYLE §4). Then `python -m engine register <slug>`.

## 3. scenes.py
- Start from `templates/scenes.py`. Look up names with `python -m engine api core` / `api index` / `api <module>` —
  don't read old videos, labs or component sources.
- `build(project) -> Video`; all times from `T = project.timing` (`T.line`, `T.word`, `arrive(...)`) — never typed seconds.
- One function per chapter registering `v.add(start, end, fn)`; `v.sfx(...)` for every visible event.
- Reusable parts go in `engine/components/` (then `python -m engine api`); one-off code stays in scenes.py.
- Cover: `v.cover = lambda c: cover(c, "<hook title with one *accent*>", ...)`. Post: `hasil/<slug>/POST.md` from
  `POST_TEMPLATE.md`. `REVIEW`: 4–6 risky line ids.
- Then STYLE §8: `check --dry` clean → critique loop.

## 4. Hand over
```bash
claude-video <slug>              # naskah, voice (align voice.wav or TTS), check, final render → hasil/<slug>/
claude-video <slug> preview      # optional 540p round (sheet, REVIEW stills)
```
Feedback must name a line id or timecode. Add each review note to `LESSONS.md` (what was wrong → the rule).
After it's posted: link + numbers in POST.md, archive `videos/<slug>` → `videos/_arsip/`, `hasil/<slug>` → `hasil/_tayang/`.
Suggest a commit message; commit only when the user says so.

## Engine in five lines
```python
v = Video(duration=T["L15"].end + TAIL, bpm=106); brand_intro(v, version=2)
v.chapter(1, "LABEL", s, e)                     # HUD + dot + tint; dark=True for the recap
v.add(s, e, lambda c, t: ..., z=10)             # draw fn: c = Canvas, t = global seconds
v.sfx("pop", t0, 0.4)                           # sound on the event's frame
x = track(t, [(t0, 120), (t1, 480)], "snappy")  # 2+ targets → summed springs (STYLE §5)
```
