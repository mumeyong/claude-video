# MUMEYONG — STYLE.md (craft ideas — all optional)

Only `IDENTITY.md` is fixed (voice, opening logo, ending logo). This file is a toolbox of things that have looked
good before — use, bend or ignore any of it. The critique loop (§6) is the judge. Older rule sets: `_archive/`.

## 1. Ideas worth reaching for
- **A metaphor from Indonesian daily life** often carries a whole video (rusun water pipe, guest book at the
  security post, a warung's order slips). The hero is that object, not a tech icon. A real chat UI, a terminal, or
  pure type is fine too when the subject is literally that.
- A **signature move** the video owns, reused later. A hook that moves before 2 s: number first, myth struck out, a
  specific question, cold open mid-action, before/after, a real viewer comment — or something new.
- Look: `flat` small or big hero, `paper`, `lit`; reel smears for teasers. Build new components when it helps.
- Repeating yourself is the real risk. Glance at `python -m engine recent <slug>` and do something you haven't done.

## 2. Layout — design the frame before the motion
The **house frame** (HUD bar on top, kicker + headline top-left at y 318, hero in the middle, bottom 40 % empty) is
what every old video looks like. Don't use it by default: start with `v.hud = False` and decide per video where type
lives, which fonts, and what holds the frame. Every chapter gets a **different composition**, for example:
- **Type is the picture** — one giant word fills the frame (`tk.F["poster"]`, 200–400 px), the object sits in/behind it.
- **Text on the object** — the words are printed on the sign, screen, receipt, label (no floating headline at all).
- **Full-bleed object** cropped by the frame edges; text small in a corner like a caption.
- **Bottom-anchored** — picture up top, type stacked from the bottom; or the reverse.
- **Split** (top/bottom or left/right) for before/after or versus; **grid/bento** for many small things.
- **Macro → reveal** — so close it's abstract, then pull out. **Top-down map / diagram** across the whole frame.
- **UI as the frame** — the phone or terminal IS the screen, edge to edge. **Marginalia** — hand notes (`tk.F["hand"]`)
  around the object. **One word, centre, nothing else** for the punch.
Type palette (`tk.F`): `display` (Inter), `serif_display` / `serif_italic` (Fraunces), `classic` (DM Serif),
`grotesk`, `poster` (Archivo Black), `quirky` (Bricolage), `wide` (Syne), `round` (Unbounded), `plex_mono`, `hand`.
Pick one pairing per video (display + text); `Headline(text, x, y, font=, size=, align=)` takes any of them.
Keep one idea per frame and something on screen across chapter changes.

## 3. Motion — fluid, never frozen (refs.pdf)
- **Never a frozen frame.** Something is always alive: the camera drifts, the hero breathes, the next element starts
  arriving while the last one settles (overlap, don't queue). A "hold" is slow motion, not a pause. `check` flags
  DEAD stretches > 1.2 s and chapters > 65 % still.
- **One shape, never cut.** Prefer one element that morphs size, radius, colour, content from state to state
  (`Morph`, `morph_path`, `Rig`, `track`) over fade-out → fade-in. Text inside a morphing box enters after the morph
  starts and leaves before it ends (`swap_alpha`). Scenes hand over through a shared element, not a blank.
- **Handoff patterns** (the last object of a chapter becomes the first of the next — pick a different one each time):
  colour **spills** out of a tap/click point (`clip-path: circle(r at x y)`) and shrinks back to a point that the next
  thing bursts from · a chip/box **blooms** into the next card (rect + radius + colour together) · things **collapse**
  to one dot that becomes the next hero · a **mosaic** floods from the edges · a **stair wipe** · a bar **closes to a
  line** that opens into the next scene · a **scan line** reveals the next layer. Measure the anchor point from the page
  (`getBoundingClientRect` in setup), never type it in. Overlap the two chapters by 0.1–0.3 s.
- **One protagonist for the film** when the story allows: one object (a packet, a dot, a coin) that changes form
  chapter to chapter reads as one film; a new hero per chapter reads as slides.
- **Snap, then drift:** moves take 0.35–0.6 s (expo-out / snappy spring), then a 0.4–0.8 s slow drift before the next
  beat — fast in, calm hold. Long sine-eased glides read as floaty.
- **Stepped vs smooth:** counters, pixels, typing and HUD readouts step at 12 per second (`floor(t*12)/12`), camera
  and cards stay smooth at 60 fps — the contrast reads as digital.
- Words split into spans need `margin: 0 .12em` (or a real space) — tight tracking glues them together.
- **Springs from rest:** `ios_at`, `glide`, `pop`, `curve("apple_out")`; 2+ targets → `track(t, frames, preset)` —
  it bends to the new target instead of stop-and-go. Snappy for UI, smooth for cards/camera, heavy for big type.
- **One leader at a time** (others `follow()` with less travel) — fluid is one thing always moving, not ten at once.
  Land on the stressed word (`arrive(T.word(...))`), SFX on the arrival.
- **Beat grid:** something happens on every beat or two (`video.beat`); no dead beat.
- Motion blur is automatic in the final render (4 subframes) — fast moves read as smooth, not as steps.
- Toolbox (`api core` / `api index`): `Morph`, `morph_path`, `Rig`, `track`, `indicator`, `swap_alpha`, `carry`,
  `rack_cut`, `depth_swap`, `draw_on`, `mark`, `count_up`, `chat_phone`, `bento`, `dolly`, `push`. Invent the rest.

## 4. Color and taste
- Each video picks its own palette (named constants at the top of scenes.py); house accent blue `#1F5EFF` is optional.
  New fonts: drop OFL files in `assets/fonts` and add a `tk.F` name.
- Things that usually look cheap: neon glow, glassmorphism, lens flares, glitch/VHS, shake, stock tech icons
  (glowing servers, robot brain, padlock + shield), emoji as decoration, the spoken sentence as on-screen subtitle,
  clichés ("Di era digital ini", "Tahukah kamu", "Yuk simak").

## 5. Sound
- Voice on top, music ducked. `v.music = dict(style=, key=, mood=)` with `Video(bpm=)`: `lofi` 76–94 · `marimba`
  100–116 · `ambient` 70–90 · `garage` 126–136 · `cinematic` 88–110. `v.sfx_kit = "glass"|"wood"|"soft"|"mech"`.
- A sound on every visible event's frame: `key` `pop` `click` `send` `whoosh` `whoosh_dark` `chime` `tick` `rec` `thud`.

## 6. Look at your frames (the one required step)
1. `python -m engine check <slug> --dry` — fix every `✗`. `!` notes (safe zone, tiny text, still %, CROWD, easing)
   are hints: fix them or know why not.
2. `python -m engine critique <slug>` → read `out/critique/hook.png`, `sheet.png`, `moves.png` like a viewer would.
   Score in `CRITIQUE.md`, fix the 3 worst, repeat until all ≥ 8 or 3 rounds.
3. Hide the title, look at 3 random frames: is it clearly *this* video — and would you stop scrolling for it?
