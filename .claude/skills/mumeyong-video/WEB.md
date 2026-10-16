# WEB.md — HTML films (the grak / cheese look, refs.pdf)

The default for new videos. The picture is `videos/<slug>/film.html`, painted by headless Chrome; `scenes.py`
(`templates/scenes_web.py`) only places the identity around it: opening logo → film → ending logo, plus the voice,
score and SFX. Start from `templates/film.html` (canvas) or `templates/film_hf.html` (GSAP DOM, HyperFrames way — both work with any script) and replace the look with this video's idea.

## Contract
- `import { FILM, ready, T, cue, canvas, beats, snap, SAFE } from '/web/lib/film.js'` → `await ready`.
- `canvas((g, t) => …)` paints frame t (or set `window.seek = t => …` for a DOM film). **Pure function of t**: no
  timers, `Math.random`, `Date`, CSS transitions/animations, `<video>`; no state carried between frames
  (`check --dry` catches these and renders one frame twice).
- Times are global seconds with the brand sting included: L01 starts at `FILM.pre_roll`. The film runs under the
  opening logo from 0 and fades out at `FILM.end` (the ending logo). Every time from the voice: `T.word('L03',
  'gratis')`, `T.line(id)`, `T.frac(id, .5)`, `T.chapter('INTRO')`, `T.stressed()` (the `*kata*` marks), `T.at(t)`
  (captions) — computed once at setup, never typed seconds.
- Sound: `cue('pop', t, 0.5)` at setup (names: click pop send whoosh whoosh_dark chime tick rec thud key). Cuts land
  on `FILM.beats` (the score's grid, or `beats.json` from `python -m engine beats <slug>` for a supplied song).
- Motion: `/web/lib/motion.js` (spring, track, trackObj, stagger, pulse, noise1, rng, cursor) and `/web/lib/apple.js`
  (iosAt, arrive, follow, presence, rise, wipe, depthSwap, focusPull, sheet, bento, morphBox, press, countUp,
  fmtID, drawOn, dolly, push, applyCam). 2+ targets → `track`/`morphBox`. No bounce on text or big things.
- Type: `<link rel="stylesheet" href="/web/lib/fonts.css">` = the repo fonts (Inter Display, Inter, JetBrains Mono,
  Fraunces, Instrument Serif, Syne, Unbounded, Space Grotesk, Archivo Black, Bricolage Grotesque, DM Serif Display,
  Caveat, IBM Plex Mono); `await document.fonts.load(…)` before measuring text.
- Images live in `videos/<slug>/assets/` (`../assets/x.png` from the page). Real UI only: `python -m engine capture
  <slug> <url>` → `assets/site/`. A reference look: `python -m engine ref <slug> <video|image>` → `refs/`.

## HyperFrames (GSAP DOM films)
The `hyperframes-*` skills (installed from heygen-com/hyperframes, `skills-lock.json`) are the motion library for DOM
films: `hyperframes-animation` (motion rules, scene blueprints, transitions, 24 text effects, GSAP adapter),
`hyperframes-keyframes` (punch-in, camera, masks, SVG draw), `hyperframes-creative` (palettes, type, beat planning),
`hyperframes-registry` (blocks: charts, terminals, maps, glitch, grain… — read the block's HTML/GSAP and adapt it).
- Start from `templates/film_hf.html`: `import { gsap, clip, timeline } from '/web/lib/hf.js'` → one
  `gsap.timeline({ paused: true })`, `clip(el, start, end)` = HyperFrames clip visibility, `timeline(tl)` last.
  Ported code that sets `window.__timelines['main'] = tl` works with a bare `timeline()`.
- Their contract carries over (single paused timeline, `fromTo` not CSS transforms, no clocks/random). Ours wins on
  the clock: every tween position and clip time from `T` / `FILM`, never a typed `data-start="3.2"`.
- Not used here: their project scaffold (`init`, `index.html`, sub-compositions), `render` / `preview` / `snapshot`
  (rule 1 — our harness renders), and `media-use` voice/TTS/BGM (IDENTITY.md: voice and sound are the engine's).

## Craft (shorts)
- Hook right after the sting: the first frame after `pre_roll` already shows something bold.
- Something new every 1–2 s; one leader per beat, followers `follow()` later; nothing ever freezes.
- Type huge and short (100–200 px, ≤ 6 words on screen), high contrast, readable muted at 360 px wide.
- Keep text and key subjects inside `SAFE` (x 81–929, y 240–1560): the green box on the critique sheets.
- One persistent hero that changes form beats a slideshow; hand over with a shared element, never a blank frame.
- Never invent a product screen or a number (IDENTITY.md).

## Look at it
`check <slug> --dry` (fix every ✗) → `critique <slug>` → read `out/critique/{sheet,hook,moves}.png` → fix the 3
worst (text outside the box, unreadable, dead or crowded moments) → repeat, ≤ 3 rounds. Live preview for the user:
`claude-video serve` → `http://localhost:5173/videos/<slug>/film.html?t=4.2`.
