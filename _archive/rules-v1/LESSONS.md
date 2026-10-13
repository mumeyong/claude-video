# LESSONS — read before every new video (phase 1), add after every review round

Concrete things learned from finished videos. One line each: what went wrong / what worked → the rule now.
Finished videos (final in `hasil/`) are frozen — lessons apply to the NEXT video, never patch old ones.

## Layout (from `check --dry` over all 13 videos, 2026-10-08)
- Objects placed against the right edge overflow (EP05 2nd kios +30 px, EP06 corner sheets) → keep wide objects
  ≥ 40 px inside the column; compute the right edge in code (`x + w <= X + CW - 40`), don't eyeball.
- Effects that spread (sound rings, particles, folders opening) leave the column → point them INTO the frame
  (`sound_rings(arc=...)`, limit `r_max` to the column) and keep opening/sliding objects centred while they move.
- Overhangs count: roofs, parapets, awnings stick out 4–8 % beyond the body width.
- Text under 17 px slipped into 2 older videos (outro pills, chips) → `check --dry` flags it; fix before handing over.
- Headlines may use col_w + 60 (top-right has no TikTok rail) — but nothing else may.

## Facts & naming
- Never invent a number or claim the CV doesn't have ("milidetik" for EP06 was wrong → "real-time").
- Real project names can be confidential: "Customer 360" had to become "Project 360". Ask/anonymise project names
  the same way as client names.

## Composition patterns getting repetitive (vary them next)
- Giant punch word in every intro (`serverless.`, `event-driven.`, `berdampingan.`, `satu layar.`, `Azure.`).
- Every recap: dark + serif closing word. Every outro: identical layout.
- Every chapter: headline top → hero → tags at y ≈ 1280.

## Motion (new, opt-in from 2026-10-08 — `components/fx.py`)
- Fast small movers strobe at 60 fps → `ghost_trail`. Drops feel weightless → `contact_shadow` + `land`/`squash`.
- Small pops & camera stops → `settle` (spring ~6 %). Never on big cards or headline text.

## Motion signature (2026-10-08 — `components/kinetic.py`, STYLE §6d)
- All 14 videos moved identically (out_expo + blur-rise headlines + blur-out exits, ~6 camera keys) → the user
  found them generic. Motion is now chosen per video in PLAN.md: spring · reveal · glue · exit. Proof: videos/motion-lab.

## Apple motion craft (2026-10-11 — STYLE §6f)
- User: "all out like professional motion graphic… especially Apple animation" — videos still read as AI slop. Cause:
  every rule ADDED motion (camera per chapter, always-alive drift, beat every 2.5 s, 2–4 reel moves, punches), nothing
  asked for stillness, and Claude never sees a frame. → §6f: one leader · arrive on the word · holds ≥ 0,8 s · quiet
  exits · continuity · real iOS springs / Apple curves. `check --dry` now prints a motion table (still % per chapter,
  CROWD, STACK) — Claude's eyes. Baseline 2026-10-11: war-tiket-crash 3–5 % still in its busy chapters (flagged),
  prompt-diproses 3× camera on top of content moves (STACK), jalur-karier clean.

## Process
- Token budget (user asked 2026-10-08): one fresh session per video; read `engine/API.md` (not sources / old
  scenes.py); PLAN.md instead of IDENTITY + TREATMENT; `register` for index tables; beats helpers; 1–2 new components.
- `check --dry` before every render command; fix every `✗` and `!`.
- After each review round, add the user's notes here (line id + what was wrong + the rule).

## User review notes
- 2026-10-09 (brand sting, all videos): "logo di awal terlalu cepat dan animasinya jelek — itu hook pertama, all out"
  → v1 (1,5 s, ensō in 0,7 s) replaced for new videos by `brand_intro(v, version=2)` (2,45 s: drop → ensō → seal →
  wordmark → brushy wipe) + `PRE_ROLL = 2.05`. Watch 3-second hold on the first v2 video; shorten with `dur=` if it drops.
