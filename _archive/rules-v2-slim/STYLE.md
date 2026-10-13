# MUMEYONG — STYLE.md

One rule per line; values live in `engine/tokens.py` (change both together). v1 (13k words of layered sections) is in
`_archive/rules-v1/` — history only, don't read it.

## 1. Format + brand DNA (same in every video)
- 1080×1920, 60 fps, −14 LUFS. Casual Indonesian (aku/kamu), short spoken sentences. **Tech terms stay English**
  (`GLOSSARY.md`); Indonesian affixes are fine (*di-scale, pod-nya*).
- Safe column x 81–929; nothing that matters below y 1560 or above y 240 (except HUD). Text ≥ 17 px.
- Frame: HUD (mono, top + bottom) · chapter dots · kicker (`● 02 · LABEL`) · headline at y 318 · content y 520–1450.
- Open with the brand sting (`PRE_ROLL = 2.05` + `brand_intro(v, version=2)`); close with a dark recap →
  `standard_outro` (mumei mark + Follow). Accent blue `#1F5EFF` is the ONLY accent for words/UI; chapter colors
  (`tk.CHAPTER`) only for dots, tints and hero objects. Dark section = recap + outro.
- Tokens only: no hex, sizes or durations typed into scenes.

## 2. Type
- Inter Display Bold headline 96 px (punch 128), Inter for UI/chat/cards, JetBrains Mono for HUD/kicker/labels.
  Instrument Serif italic only for `_soft emphasis_` (max once per section). Numbers in Indonesian format (`fmt_id`).
- Headline = the **punchline, not the narration**: ≤ 4 words per line, ≤ 2 lines, ends with a period, exactly one
  `*accent*` word. It may change mid-chapter when the picture changes.
- No burned-in subtitles; never put the spoken sentence on screen word for word.

## 3. Identity — what changes per video (PLAN.md)
Pick each and make it **different from the previous video** (`python -m engine recent <slug>`):
1. **Metaphor** — one object/place from Indonesian daily life that carries ≥ 3 chapters (rusun water pipe, guest
   book at the security post, classroom whiteboard). The hero is that object — never a stock tech icon.
2. **Signature move** — one motion the video owns, reused in a later chapter (not only the hook).
3. **Signature color** — one chapter color owns the hero.
4. **Hook format** — number first · myth struck out · specific question · cold open mid-action · before/after ·
   real viewer comment.
5. **Structure** — N steps · countdown · problem → turn → result · myth vs fact · story.
6. **Material** — `flat` small hero · `flat` big hero (60–80 % of the frame, may bleed) · `paper`; `lit` only on
   request. Never the same as the previous video.
7. **≥ 1 new component**, or an old one in a clearly new role.
8. **Human touch** (3 of 4): a real artefact (anonymised) · an opinion only Mumeyong would say · one surprise ·
   one deliberate imperfection (hand mark, tilted stamp).
Series episodes share structure + series label; metaphor, signature, color and hook still rotate.
Reel look (`components/reel.py`: paper ground, smear entrances, verb slams) = brand teasers only.

## 4. Composition
- **One hero, big**, with air around it — one idea per frame. A small card floating in empty space is a bug.
- No two consecutive chapters with the same layout (full card · centred hero · stacked/tilted cards · pure type ·
  object + hand mark). ≤ 3 cards at once.
- The hero stays on screen between chapters (shared element) — never a blank frame between scenes.
- One punch every ~15–20 s (giant number/word or full-bleed hero), then hold it.
- Bookend: the hook's object returns in the recap with a new meaning.

## 5. Motion (the only motion section)
Goal: an Apple keynote made by a motion designer — calm, precise, nothing moves without a reason.
1. **Start from rest.** Springs only: `ios_at(t, t0, "smooth"|"snappy"|"hero")`, window springs `glide(p)` / `pop(p, s)`,
   Apple curves `curve("apple_out"|"apple_in"|"apple_in_out")`. Anything with 2+ targets uses `track(t, frames, preset)`
   (it bends to the new target instead of stop-and-go). `out_expo` only for impacts (ripple ring, slam-down scale).
   Never linear (except progress bars), never scale from 0, no bounce on big things.
2. **One leader.** One thing makes the main move; others `follow()` 0.12 s later with ≤ half the travel.
3. **Arrive on the word.** Big moves land on the stressed word: `t0 = arrive(T.word("L07", "kode"))`; the SFX goes on
   the arrival. Cause and reaction on the same frame.
4. **Hold.** ≥ 0.8 s stillness after an arrival; every chapter ≥ 45 % still. 0.3–0.75 s of stillness before a payoff.
5. **Size sets duration.** Small (chips, ticks) 0.35–0.45 s · cards/lines 0.6–0.8 s · hero 0.9–1.2 s. Text travels
   ≤ 40 px. Opacity leads (done at ~45 %), position follows (`rise`, `presence`).
6. **Exits are quiet and faster** (0.3–0.4 s, fade + scale .98).
7. **One effect per element**: opacity + ONE transform. Blur only as motion blur or depth.
8. **Continuity:** hand over with a shared element (`Rig`, `Morph`), `depth_swap`, `focus_pull`, or one `rack_cut`
   per ~8 s. Use 2–3 seam types per video, one main direction (up).
9. **Camera:** `dolly` during a hold, `push` to the next focus, `cut` on a beat — never while 2+ things move, ≤ ±22 % zoom.
10. **Tempo:** slow–slow–snap. Headlines reveal per line (`rise`/`wipe`/`ink`); word-by-word max once per chapter.
Toolbox (`python -m engine api core` / `api index`): `draw_on`, `mark`, `split_rise`, `count_up`, `morph_path`,
`path_at`, `carry`, `rack_cut`, `shutter`, `indicator`, `chat_phone`, `Rig`, `Morph`, `bento`, `sheet`. Pick 1–3 that
serve the metaphor — never all.

## 6. Sound
- Voice on top; music ducked under it. Generated score: `v.music = dict(style=, key=, mood=)` with `Video(bpm=)` in
  the style's range — `lofi` 76–94 · `marimba` 100–116 · `ambient` 70–90 · `garage` 126–136 · `cinematic` 88–110.
  `v.sfx_kit = "glass" | "wood" | "soft" | "mech"` to match the metaphor's material. Style and kit ≠ previous video.
- Every visible event (card in, click, check, send) has a sound on its frame; ambient motion has none.
  SFX: `key` · `pop` · `click` · `send` · `whoosh` · `whoosh_dark` · `chime` · `tick` · `rec` · `thud`.

## 7. Banned
- Neon glow, glassmorphism panels, lens flares, stock gradients, 3D-extruded type, glitch/VHS, particle bursts, shake,
  spinning, zoom-punch transitions.
- Stock tech heroes: glowing servers, robot/brain, neon globe, padlock + shield, matrix code, cloud/gear/rocket icons.
- Emoji as decoration, clip-art, centred body text in light chapters (outro excepted), more than one accent color.
- Script clichés: "Di era digital ini", "Tahukah kamu", "Yuk simak", "game changer", vague "Pernah nggak sih…".
- A video with nothing only Mumeyong could say. An invented number — no source, no number on screen.
- Translated tech terms ("mesin" for node, "nganggur" for idle).
- Hard-coded seconds, unseeded randomness, state carried between frames (frame = f(t)).

## 8. Before handing over (Claude)
1. `python -m engine check <slug> --dry` — fix every `✗`, every `!` (safe zone, tiny text, motion table: still %,
   CROWD, STACK) and the easing notes.
2. `python -m engine critique <slug>` → read `out/critique/hook.png`, `sheet.png`, `moves.png`. Score hook (0–2 s) ·
   readability at phone size · motion · variety · brand · sound sync 1–10 in `CRITIQUE.md`; fix the 3 worst; repeat
   until all ≥ 8 or 3 rounds.
3. Final test: hide the title, look at 3 random frames — is it clearly Mumeyong, and clearly *this* video?
