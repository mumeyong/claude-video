---
name: mumeyong-video
description: Make a MUMEYONG vertical (9:16) animated explainer video in Python + ffmpeg, in the light-glass UI-keynote style — script, storyboard, voice-timed scenes, review loop. Use for any new video, scene, or change to a video in videos/<slug>/. Claude writes the code; the USER renders.
---

# MUMEYONG video workflow

Read `STYLE.md` (same folder) before writing a script or a scene. Read `CLAUDE.md` rules — especially
**rule 1: never render; hand the user the command.**

Each phase ends with a **gate**: stop, show the result, wait for the user's "ok/setuju". Don't skip ahead.

## Phase 0 — Brief
Ask (only what's missing): topic, audience, the ONE takeaway, target length (default 60–150 s),
CTA/contact for the outro, any visuals/footage the user owns (PNG screenshots go in `videos/<slug>/assets/`).
Then `python -m engine new <slug>` (user runs it, or Claude creates the files by hand).

## Phase 1 — SCRIPT.md (naskah)  → gate
- Format: `## CHAPTER` headings, one sentence per `[Lxx]` line. Chapters: `INTRO`, `00 · LABEL` … `06 · LABEL`, `RECAP`, `OUTRO`.
- Structure (from the reference, 152 s): hook 0–20 s (answer a comment / bold claim, show the result first) →
  4–7 numbered chapters of 8–28 s → dark recap tying back to the claim → outro CTA 10–12 s.
- Voice: casual Indonesian (aku/kamu, "nah", "terus", "udah"), 2–3 s per sentence, ~160 wpm → about
  **2.7 words per second of runtime**. 150 s ≈ 300 words, ~45 lines.
- Every line must "earn" a visual. Mark the key word you'll animate on with `{curly}` in a comment if needed.
- Offer 2–3 hook options as A/B/C (like the reference's option cards) and let the user pick.
- Read-aloud marks: `*kata*` = vocal stress (put it on the same words the visuals land on), ` //` at line
  end = breath. Write it to be SPOKEN: short clauses, no parentheses, numbers as words where they're said
  ("empat belas ribu dolar"), English terms only if you'd say them out loud.
- **After every SCRIPT.md write/change: run `python -m engine naskah <slug>` → NASKAH.md** and tell the
  user it's ready to read. Rerun it after every revision so it always matches.

## Phase 2 — TREATMENT.md (storyboard)  → gate
One row per line. Columns: `id · headline (punchline, with *accent*) · visual · motion · SFX · anchor word`.
Example:
```
L22 | Naskah dulu.   | 3 option cards A/B/C, cursor clicks "Setuju" on B | cards rise stagger .1s, click | pop×3, click | "naskahnya"
```
Check against STYLE.md: one change per sentence, ≤ 3 cards, one accent per headline, banned list.

## Phase 3 — Voice + timing
- Before the voice exists: `python -m engine estimate <slug>` (161 wpm estimate) so scenes can be built and previewed.
- User records `videos/<slug>/audio/voice.wav` reading **NASKAH.md** (48 kHz, quiet room, ONE take start→finish; on a mistake just
  repeat the sentence — the aligner keeps the last good take). Then `python -m engine align <slug>`.
  Lines scoring < 0.75 are flagged — check them in timing.json.
- Music: `videos/<slug>/audio/music.(mp3|wav)`, ~128 BPM. Set `beat_offset` in scenes.py to the first downbeat.

## Phase 4 — scenes.py (kode)
- `build(project) -> Video`. Get `T = project.timing`; every time comes from `T.line(..)`, `T.word(..)`,
  `T.after(..)`, chapter spans, or `video.beat`.
- Structure: one function per chapter (`def ch_naskah(v, T): ...`) that registers layers with
  `v.add(start, end, fn)`; `fn(c, t)` draws with components. End time of a layer must include its exit.
- Pattern per chapter: `v.chapter(n, LABEL, start, end)` → `kicker` + `Headline.draw(t, t_in, t_out)` →
  content via `appear(...)` → chat events → `v.sfx(...)` for each visible event.
- Each chapter's elements exit at the next chapter's start − 0.35 s (`out`).
- Use `wobble` for idle life, `select_box` / dim-and-outline for focus, `fmt_id` for numbers.
- After writing: Claude runs `python -m engine check <slug>` (no drawing) and fixes errors.
- Then hand the user the commands (see below). **Do not run them.**

## Phase 5 — Review loop (cek)  → gate per round
1. User runs `sheet` (one thumb per line) and/or `still` for specific lines, sends screenshots/notes.
2. User runs `preview` (half-res, with audio) for timing feel; `--from/--to` for one chapter.
3. Feedback must be specific: line id or timecode + what's wrong. If vague, ask which line.
4. Fix → new commands → repeat. Expect ~3 rounds (the reference took 3 versions).

## Phase 6 — Final render + commit
Hand over `python -m engine render <slug>`. When the user confirms it's good, suggest
`git add videos/<slug> && git commit -m "feat(<slug>): …"` — commit only if the user says so.

## Command block to hand over (fill in the slug and lines)
```bash
source .venv/bin/activate
python -m engine sheet <slug>                    # → videos/<slug>/out/sheet.png
python -m engine still <slug> L05 L12            # → videos/<slug>/out/stills/
python -m engine preview <slug> --from 20 --to 45
python -m engine render <slug>                   # final → videos/<slug>/out/final.mp4
```

## Engine cheat-sheet
```python
from engine import Video, tokens as tk
from engine.ease import prog, out_expo, in_cubic
from engine.components import (Headline, kicker, appear, fade, ChatTrack, window, chip, tag, word_pill,
    select_box, strike, stat, big_number, waveform, rec_bar, filmstrip, phone, comment, Cursor,
    step_row, rule_box, connector, segments, follow_button, contact_pill, fmt_id, wobble)

v = Video(duration=T.duration, bpm=128, beat_offset=0.0)
v.chapter(2, "NASKAH", start, end)            # numbered chapter → HUD + dot + bg tint
v.chapter(None, "LIMA ATURAN", s, e, dark=True)
v.add(start, end, lambda c, t: ..., z=0)       # draw fn, t = global seconds
v.sfx("whoosh", start)                          # sound cue
v.chat = ChatTrack(); v.chat.show(t); v.chat.type("…", at=t); v.chat.send(at=t2)
v.track(Cursor([(t0, x0, y0), (t1, x1, y1)], clicks=[t1]))

h = Headline("Naskah *dulu*.")                 # *accent*  _serif_  ~strike~  \n
h.draw(c, t, t_in, t_out, strike_at=None)
appear(c, t, t_in, t_out, (x, y, w, h), lambda c: window.frame(c, x, y, w, h, "CLAUDE.md", "aturan kerja"))
```
