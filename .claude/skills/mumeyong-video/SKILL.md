---
name: mumeyong-video
description: Make a MUMEYONG vertical (9:16) animated explainer video in Python + ffmpeg — script, voice-timed scenes, self-critique from frames. Use for any new video, scene, or change to a video in videos/<slug>/. Claude writes the code; the USER renders.
---

# MUMEYONG video workflow

**Fixed:** `IDENTITY.md` (format, brand, truth, banned). **Free:** everything else — metaphor, structure, layout,
motion, sound are your call; `STYLE.md` is a craft guide, `LESSONS.md` is what went wrong before. Read those three,
then make something you'd be proud of. Never render (CLAUDE.md rule 1); don't stop to ask — finish, then hand over.

## 1. SCRIPT.md (+ NASKAH.md)
- `templates/SCRIPT_QUICK.md` (60–75 s) or `templates/SCRIPT.md` (90–150 s): `## INTRO` · `## 00 · LABEL` … ·
  `## OUTRO` (a recap chapter is optional), one spoken sentence per `[Lxx]` line, ~2.7 words/s.
- `*kata*` = stress (a visual lands there), ` //` = breath, numbers as spoken words, terms per `GLOSSARY.md`.
- Then `python -m engine naskah <slug>` (never hand-edit NASKAH.md) + `python -m engine estimate <slug>`.

## 2. scenes.py
- Look up names with `python -m engine api core` / `api index` / `api <module>`. `templates/scenes.py` shows the
  grammar if you want a start — don't read old videos.
- `build(project) -> Video`; all times from `T = project.timing` (`T.line`, `T.word`, `arrive(...)`).
- Reusable parts → `engine/components/` (then `python -m engine api`); one-off code stays in scenes.py.
- Cover: `v.cover = lambda c: cover(c, "<hook with one *accent*>", ...)`. `hasil/<slug>/POST.md` from
  `POST_TEMPLATE.md`. `REVIEW`: 4–6 risky line ids.
- `PLAN.md` (`templates/PLAN.md`: registry block + one paragraph) → `python -m engine register <slug>`.

## 3. Look at it (STYLE §5)
`check --dry` (fix every `✗`) → `critique` → read the PNGs → fix the 3 worst → repeat (≤ 3 rounds).

## 4. Hand over
```bash
claude-video <slug>              # naskah, voice (align voice.wav or TTS), check, final render → hasil/<slug>/
claude-video <slug> preview      # optional 540p round
```
Feedback names a line id or timecode; turn it into one line in `LESSONS.md`. After posting: numbers in POST.md,
archive `videos/<slug>` → `videos/_arsip/`, `hasil/<slug>` → `hasil/_tayang/`. Commit only when the user says so.

## Engine in five lines
```python
v = Video(duration=T["L15"].end + TAIL, bpm=106); brand_intro(v, version=2)
v.chapter(1, "LABEL", s, e)                     # HUD + dot + tint; dark=True for a dark section
v.add(s, e, lambda c, t: ..., z=10)             # draw fn: c = Canvas, t = global seconds
v.sfx("pop", t0, 0.4)                           # sound on the event's frame
x = track(t, [(t0, 120), (t1, 480)], "snappy")  # 2+ targets → summed springs (STYLE §3)
```
