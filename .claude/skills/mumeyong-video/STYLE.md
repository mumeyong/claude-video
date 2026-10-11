# MUMEYONG — STYLE.md (buku panduan gaya)

Measured from the reference (beyondstudioid "Tutorial membuat animasi dengan Claude Code", 2026).
Code mirror: `engine/tokens.py`. If you change a value here, change it there too.

## 1. WAJIB (always)

| Thing | Value |
|---|---|
| Canvas | 1080×1920, 60 fps, H.264 yuv420p, AAC 192k, −14 LUFS |
| Language | Bahasa Indonesia, casual "aku/kamu", short punchy sentences |
| Brand | HUD top-left `MUMEYONG · TUTORIAL` (series word can change per video) |
| Opening | **brand sting v2** (new videos from 2026-10-09) 2,45 s on paper: ink drop blooms → ensō brushed in (wet tip, slow push-in) → flecks → seal stamps (shadow, press ring) → MUMEYONG letter by letter + brushed vermilion underline + url → brushy wipe reveals the video as the mark flies into the HUD corner; `PRE_ROLL = 2.05` + `brand_intro(v, version=2)`. (2026-10-08 videos: v1, 1,5 s, `PRE_ROLL = 1.2`.) |
| Ending | dark recap → logo (new videos: `mumei_mark`) + "Follow" click → contact pills |
| Safe zone | content column x 81→929 (keeps clear of TikTok's right rail), nothing important below y 1560 except HUD |

## 2. Frame anatomy (top → bottom)

```
y 66    MUMEYONG · TUTORIAL                         02 — NASKAH      ← HUD mono 19px, muted, tracking .18em
y 100                                                ● ● ● ○ ○ ○ ○    ← chapter progress dots (current = chapter color)
y 290   ● 02 · NASKAH                                                 ← kicker: mono-med 24px, tracking .2em, chapter dot
y 318   Naskah dulu.                                                  ← HEADLINE Inter Display Bold 96px, −0.055em, lh .98
y 520   ┌──────────── content: cards / mockups / numbers ───────────┐
        │                                                            │
y 1330  └────────────────────────────────────────────────────────────┘
y 1338  (● CLAUDE.md) (● skill)                                       ← context chips
y 1400  ┌ Tanya Claude Code...                                    (↑) ┐ ← persistent chat input, r 32
y 1552  └ +  📎  🎙  🌐  💡                                          ┘
y 1855  00:01:04:04 ● 128 BPM                      1080×1920 · 60FPS  ← HUD bottom (timecode HH:MM:SS:FF)
```

## 3. Color

Light section (most of the video)
- Canvas `#F2F3F6`; two soft radial glows of the **chapter tint** (top-right, bottom-left) + constant warm `#F6ECE8` bottom-right. Glows drift slowly (±40px).
- Ink `#0B0B0F` · body `#3A3F47` · muted `#8A8F98` · faint `#C9CDD4` · hairline `rgba(0,0,0,.06)`
- **Accent blue `#1F5EFF`** — the ONLY accent for words, buttons, highlights, selection boxes.
- Negative pill (the "wrong" thing): coral `#EB6A4A`.

Chapter identity (dot color / bg tint):
| # | dot | tint | | # | dot | tint |
|---|---|---|---|---|---|---|
| 00 | `#2364FF` | `#EAEDFA` | | 04 | `#0E9AAB` | `#EAF3F8` |
| 01 | `#10A060` | `#ECF3F2` | | 05 | `#F03B4F` | `#F6ECEF` |
| 02 | `#E8861A` | `#F8F1EA` | | 06 | `#2364FF` | `#EAEDFA` |
| 03 | `#7558F0` | `#EFEBFA` | | intro | — | `#EEEBF8` |

Brand mark (from mumeyong.dev — the "mumei" 無名 emblem: an ensō left open at the upper right + a blank vermilion
hanko seal, tilted 4°): paper `#FAF9F5`, ink `#2B2C29`, seal `#C44834`. Used ONLY by the brand sting at the very
start (`components/brand.py`, opt-in `PRE_ROLL` in scenes.py, from 2026-10-08 on) and the outro mark — never as a
content accent.

Dark section (recap + outro): bg `#0C0C12`, navy glow `#13265A` rising from bottom, ink `#F5F6F8`,
muted `#7C8494`, cards `#161925`, accent `#4F8BFF`.

## 4. Type

| Role | Font | Size | Tracking |
|---|---|---|---|
| Headline | Inter Display Bold | 96 (punch: 128) | −0.055em, line-height .98 |
| Emphasis word | **accent blue** same font — `*kata*` | | |
| Soft emphasis | Instrument Serif Italic, blue, ×1.10 — `_kata_` (max 1 per video section) | | |
| Kicker / HUD | JetBrains Mono (Medium for kicker) | 24 / 19 | +0.18–0.20em, UPPERCASE |
| Card title | Inter SemiBold | 27 | −0.01em |
| Card body | JetBrains Mono | 21, line-height 1.85 | 0 |
| Chat text | Inter Regular | 30 | |
| Chips | Inter SemiBold | 22 | |
| Numbers | Inter Display Bold, Indonesian format `2.951` / `44,4 s` | 60–64 | −0.04em |

Headline rules: ≤ 4 words per line, ≤ 2 lines, ends with a period. Exactly one accent (`*…*`) per
headline. The headline is the **punchline**, not the narration ("Habis itu minta storyboard, detail banget" → `Tulis _tiap_ detiknya.`).

## 4b. Language — tech terms stay English

Narration and on-screen text are casual Indonesian, but **every technical term stays English** — node, pod,
load balancer, auto-scaling, request, idle, right-sizing, reserved instance, on-demand, serverless, monolith…
Indonesian affixes on them are natural (*di-scale, pod-nya*). Metaphors may introduce a term, never replace it.
Full list + do/don't: `GLOSSARY.md`.

## 5. Components (engine/components)

- **Window card** — white, r 22, hairline border, soft shadow (blur 34, y 14, 7.5%). Header 66px: three grey dots, title, mono meta right. Kinds: markdown (`CLAUDE.md`), code (`film.py`, line numbers + light syntax), terminal (`›` prompt, typing, progress bar).
- **Chat input** — always present from the first chapter on; typing at 34 cps with the next letter fading in blue + blue caret; send = press + ripple; chips above show current context.
- **Selection box** — design-tool blue frame + 4 square handles + size label pill (`398 × 71`). Use to point at one thing.
- **Word pill** — big colored pill with white headline text (`keyframe.` coral = wrong, `kode.` blue = right).
- **Strike** — blue line drawn through a phrase (`~satu prompt~`).
- **Stat tile / big number** — count-up, Indonesian format.
- **Option cards** — A/B/C small cards with "Setuju" buttons, slightly rotated (±2°).
- **Filmstrip** — thumbnails in a card + blue playhead + time pill.
- **Waveform / REC bar** — red recording pill; waveform colored per segment with S1/S2 markers.
- **Cursor** — macOS pointer, arcs between points, click ripple.
- **Recap (dark)** — left: chapter rows; right: rule slots filled one by one, joined by blue S-curves; `━━ ━━ ── 02 / 05`.
- **Outro** — ring logo draws on, brand name, tagline, `+ Follow` → click → `✓ Following`, contact pills.

## 6. Motion

- **Everything eases out**: entrances `out_expo`, exits `in_cubic`. Never linear (except progress bars/timers).
- Headline: words enter one by one — blur 18→0, rise 26→0, opacity 0→1, 0.55 s, stagger 0.06 s. (= the classic
  `blur` reveal — one of several motion signatures, §6d).
- Cards: rise 48, scale .965→1, blur 12→0, 0.6 s. Stagger sibling cards 0.08–0.12 s.
- Exit (scene change): blur → 14, fade, drift up 14–18 px, 0.35 s. Everything leaves together.
- Chapter change: headline/cards exit, HUD label crossfades, dot fills with chapter color, bg tint crossfades 0.6 s, kicker slides in from −14 px. A `whoosh` SFX lands on it.
- Focus: dim the rest to 30%, outline the focused line in blue; or a selection box.
- Typing: 34 cps (chat), ~120 cps (code). Every typed char = `key` SFX.
- Resting elements: **still** (Apple) — the hero alone may idle-float 2–4 px (`wobble`) or ride a dolly. Never bounce big
  things; `out_back` only for small pops (chips, check marks). From 2026-10-11 §6f overrides this section where they differ.
- One *idea* per spoken sentence (~every 2.5 s) — a change can be a word highlight or a number ticking, not a new
  move. A line > 4 s gets a second beat **or a hold with a camera dolly** (§6f). Stillness is allowed; busyness isn't.
- **Physical layer (`components/fx.py`, from 2026-10-08 on — new videos only):** small pops and camera stops may
  `settle` (spring, ~6% overshoot, 0.7 s — never on big cards/text); objects that drop onto a floor get a
  `contact_shadow` and a `land` squash (12%, 0.35 s); fast small movers (shuttle, flying sheet, dot) get a
  `ghost_trail` (4 samples over 0.05 s) instead of strobing at 60 fps. Tokens: `M["settle"]`, `M["land_*"]`, `M["trail_*"]`.

## 6b. Composition — NOT a template

The skeleton (HUD, kicker, headline, chapter dots) stays constant; **what's under it must change every chapter.**

- **Hero object per chapter**, filling ≥ 50% of the content area (y 520–1450). A small card floating in empty
  space is a bug. Hero vocabulary: giant odometer number · 24h clock ring · receipt · terminal with pop-out
  cards · seat grid + drag-resize · shattering block · staircase chart · typographic battle (10% vs 100%).
- **No two consecutive chapters share a layout.** Rotate between: full-width card · centered hero (no card) ·
  stacked/tilted cards · pure typography · object + hand note.
- **Camera is motivated, never decorative** (§6f): a `dolly` during a hold, a `push` to the next focus timed with
  `arrive()`, or a `cut` on the beat. Never while 2+ things are moving. A chapter may have none if the hero moves.
  Never more than ±22% zoom.
- **Vary transitions inside and between chapters** — `appear(enter=, exit=)`: whip left/right, drop down,
  pop, blur. Mid-chapter scene changes use a whip; chapter changes keep the blur/HUD crossfade.
- **One "punch" moment every ~15–20 s**: giant number or word (`mega`/`giga` tokens), a full-bleed hero, or a hard cut
  to a single word — then hold it.
- **Headline may change mid-chapter** when the visual changes (`Cari yang *bocor*.` → `Nyala jam _dua_ pagi?`).
- **Hand notes** (`note()`, Instrument Serif italic blue + arrow) are allowed as annotations — max 2 on screen.
- **Bookends**: the hook's hero object returns in the recap (same number, new meaning).
- Slight tilt (±2–3°) is allowed for stacked cards, receipts and stamps — never for terminals, charts or text.

## 6c. Brand DNA vs identity — unique, never generic

**Brand DNA (fixed in every video, ~40%)** — HUD, fonts, accent blue `#1F5EFF`, chapter dots, "everything eases
out / nothing linear", outro/logo/CTA, SFX palette. Never changes per video.
*(Until 2026-10-08 the whole motion feel — blur-in headlines, `out_expo`, blur-out exits — was DNA too. That made
every video move identically; it is now the per-video **motion signature**, §6d.)*

**Identity (chosen per video, ~60%)** — written in `videos/<slug>/PLAN.md` (phase 1.5) from
`templates/PLAN.md`, checked against `ideas/REGISTRY.md`:
0. **Look + motion signature** — Look: classic (§1–§6d) · classic + reel moves · reel (§6e). Then spring preset ·
   headline reveal · scene-to-scene glue · exit. The set differs from the previous video.
1. **Central metaphor** — one "world" used in ≥ 3 chapters, not only the hook.
2. **Signature move** — one motion the video owns (rolling digits, lights switching off, snapping grid…).
3. **Signature color** — one chapter-palette color that owns the hero objects. Accent blue stays for words/UI.
4. **Hook format** — rotate: number first · viewer comment (only if real) · myth struck out · relatable
   question · cold open mid-action · before/after.
5. **Structure** — rotate: N steps · countdown · problem → turn → result · myth vs fact · before/after · story.
6. **≥ 1 new component** — the engine grows with every video.

**No repeats:** choices 1–5 must differ from the previous video (ideally the previous two). **Series exception:**
episodes of one series share the series structure, HUD series label, bumper and signature series component;
metaphor, signature move, color and hook still rotate. A component may
not be the *hero* of two consecutive videos.

**Human touch (at least 3 of 4):** a real artefact (anonymised screenshot/output/number) · an opinion only
you would say · one surprise moment · deliberate imperfection (hand note, tilted stamp, hesitant cursor).

## 6d. Motion signature — kinetic + keynote layers (`components/kinetic.py`, `keynote.py`, new videos from 2026-10-08)

Studied from @davianmotion + Apple keynotes / iOS: one hero that never leaves, type that *arrives*, swaps hidden by light, a camera
that never sits still, exits that fade to grey instead of blurring away. Each video picks **one choice per row** in
PLAN.md (“Motion”) and keeps it for the whole video; the previous video's choices may not be repeated as a set.

| | Options |
|---|---|
| Spring (`tk.SPRING`) | `snappy` (UI, quick ~11%) · `heavy` (weighty, ~3%) · `floaty` (soft, ~15%, small objects only) · `silk` (Apple keynote, no visible overshoot) |
| Headline reveal | `blur` (classic) · `ink` (Apple: line fades in faint, words ink in one by one) · `mask` (words spring up from behind the baseline) · `track_line` (letters arrive, tracking collapses — 1–3 words, punch lines) |
| Scene glue | **persistent hero** `Rig` (the hero moves/scales to its next spot instead of exit+enter, `anticip=` wind-up) · `sheen` + `swap` (light band hides a content change) · `lockup` (A × B fly in from both edges) · `Morph` (pill grows into a card — Dynamic Island / App Store expand) · `bento` (tiles assemble) · `sheet` (floating sheet slides up) |
| Exit | `blur` (classic) · `dim` (drain to grey, then fade) · `mask` (leave up through the baseline) |
| Hero entrance | full-bleed shrink into place (`Rig` s 2–2,6 → 1, `silk`) · `yaw` + `turn_at` (product turns to face camera) · `press` on any button that gets tapped |
| Alive during holds | `dolly` (camera, preferred) or `drifting` on the hero only — never both, never under a big move · `parallax` for background props (depth 0.4–0.7) |

Rules: a persistent hero = **max one** `Rig` hero per chapter, and it moves at most once per spoken line.
Big objects use `heavy`, never `floaty`. `anticip` ≤ 0.08. `track_line` only for ≤ 3 words in `headline`/`headline_lg`/`mega`.
`sheen` is a soft highlight on a card, not a lens flare — never on text alone, max once per ~10 s.
`curtain` (fade from darkness) is allowed for a cold-open hook only. Neon glow / bloom and frosted-glass blur stay banned (§8).
A keynote-style video (`silk` + `ink` + `bento`/`Morph`) keeps the left-aligned column — no centered statement text.
Proof sheet for every move: `videos/motion-lab`.

## 6e. Reel layer — the brand-reel editing style (`components/reel.py`, new videos from 2026-10-10)

Ported from the claude.ai Motion film **"Six Worlds, One Walk"** (the mumeyong.dev brand reel, 16:9) and re-laid for
1080×1920. Proof sheet: `videos/_lab/reel-lab` (one chapter per film scene). Every future video picks one of two
ways to use it in PLAN.md (row "Look"):

- **Look: reel** — the whole video wears the reel style (table below): paper ground, viewfinder HUD, green + world
  colors, smear entrances, wipes, slams. Default for brand teasers/trailers; an explainer uses it only when the PLAN
  argues why (from 2026-10-11 the default explainer look is classic + Apple craft, §6f). To stay unique, never two reel-look videos
  in a row (except teaser/trailer pairs). `look:` in the PLAN registry block, so `register` writes it into REGISTRY's Signature column. The motion signature (§6d) row then becomes reel moves + one §6d glue.
- **Look: classic + reel moves** — the light-glass video borrows 2–4 reel moves as its signature (e.g. `smear_words`
  headlines, `highlight_phrase`, `float_chips`, `count_pill`, `iris`/`pixel_wipe` chapter changes, `stat_panel`,
  `verb_slam` as the hook). Pass the chapter / accent color into the color parameters. §8 stays fully in force.

| Thing | Reel value |
|---|---|
| Ground | flat paper `#FAF9F5` (`v.ground = C["brand_paper"]`), no glows · ink `#22231F` (`reel_ink`) |
| Main color | green `#608A70` (`reel_green`): iris, orbit satellite, highlighter, dotted lines · seal `#C44834` dots |
| Six worlds | `REEL_WORLDS` (root · platform · security · cloud · automation · observability): chip squares, card labels, verb grounds |
| HUD | `viewfinder` (with `v.hud = False`, z ≥ 100): corner brackets, **mumeyong.dev** / tag, running TC, section, progress bar |
| Type | Inter Display 800 against Instrument Serif italic; mono labels tracked .16–.18em, uppercase |
| Entrance | `smear` / `smear_words`: offset + horizontal stretch (+25%) + blur 16 → 0, opacity 1.6× faster |
| Exit | reel exit: scale +30%, blur 18, fade (0.4 s), or a wipe (`iris`, `pixel_wipe`) |
| Logo | `dot_gather` (dots on an orbit gather onto the ensō, seal stamps) → `orbit` → `iris` open in green |
| Moves | `float_chips` · `count_pill` · `highlight_phrase` · `formula` · `tilt_plane` + `pop_card` · `stat_panel` (hard cuts) · `verb_slam` · `end_card` · `type_clip` |
| Sound | `reel_sfx(v, move, t0, …)` registers the matching SFX for every move |

Rules: everything is still voice-timed (`T.line(...)`) and frame = f(t). Full-screen pieces (`iris`, `pixel_wipe`,
`verb_slam`, `viewfinder`) go at z ≥ 100. Numbers use Indonesian format (`fmt_id`). Chips that fly in and the logo
dots may cross the safe column while they move, but nothing may rest outside it. Max one `pixel_wipe` and one
`verb_slam` run per video (no more than 3 flashes per second).
**Deliberate exceptions to §8, "Look: reel" only:** the reel centres its statements, uses the green + world colors
instead of accent blue, and has hard color cuts (verb slam) plus a scale-up blur exit. A classic-look video that
borrows reel moves gets none of these exceptions.

## 6f. Apple motion craft — the DEFAULT for every new video (2026-10-11)

The user wants the motion to feel like an Apple keynote / product film made by a professional motion designer —
never "AI slop" (everything moving, all the time, all the same way). §6d/§6e choose the *vocabulary*; this section is
the *craft* that every video follows on top of whatever Look it picks. Code: `components/keynote.py` (Apple craft
block), `ease.curve()` / `ease.ios_spring()`, `tk.EASE`, `tk.IOS`. Proof sheet: `videos/_lab/apple-lab`.

**The ten rules**

1. **One leader.** At any moment ONE thing makes the main move. Others wait or follow: `follow(t_lead, i)` (+0.12 s
   each) with ≤ half the travel. The camera never moves while 2+ things move (`check --dry` flags `STACK`/`CROWD`).
2. **Arrive on the word.** Big moves *land* on the stressed word, they don't start on the line:
   `t0 = arrive(T.word("L07", "kode"))`. Put the SFX on the arrival, not the start.
3. **Hold.** After an arrival leave ≥ 0.8 s (`M["hold_min"]`) of stillness so the eye reads it. Only a `dolly` may
   move during a hold. Every chapter is ≥ 45 % still (`check --dry` measures it; < 30 % = `!`).
4. **Opacity leads, position follows.** Opacity is done at 45 % of the move; position glides on (`presence`, `rise`).
5. **Real curves only.** iOS springs by real time (`ios_at(t, t0, "smooth")`; presets `tk.IOS`: smooth · snappy ·
   bouncy · default · hero) or Apple béziers (`curve("apple_out")` in · `"apple_in"` out · `"apple_in_out"` pans ·
   `"apple_dolly"` holds). No `out_back`/`out_expo` on anything big. `bouncy` ≤ once per chapter, small objects only.
6. **Size sets duration.** Small (≤ 100 px: chips, ticks) 0.35–0.45 s · cards / lines 0.6–0.8 s · hero / full-bleed
   0.9–1.2 s (`"hero"` spring). Travel ≤ 40 px for text, ~5 % of the object's height for big objects. Scale in from
   0.96–0.985 (or full-bleed shrink 2–2.6 → 1), **never from 0**.
7. **Exits are quiet and faster** (0.3–0.4 s, fade + scale .98, `exit="quiet"`). No flourish on the way out.
8. **Continuity over exit-then-enter.** Between ideas, keep something on screen: shared element (`Morph`, `Rig`),
   `depth_swap` (old falls back, new comes forward), `focus_pull` (background goes soft behind a sheet/number), or a
   hard `cut` on the beat for contrast. Never a blank frame between two scenes.
9. **One effect per element.** Opacity + ONE transform (rise, or scale, or wipe). No blur + scale + rotate + spring on
   the same thing. Blur only as motion blur or depth (`focus_pull` ≤ 9 px) — never decoration.
10. **Type moves as type.** Headlines reveal per line (`reveal="rise"` or `"wipe"`) or ink in (`"ink"`); word-by-word
    `blur`/`mask` max once per chapter; `track_line` only for a 1–3 word punch. Big type, tight tracking, lots of air.

**Tempo:** a video breathes slow–slow–snap: two calm arrivals then one fast cut or punch. Contrast is what makes it
feel designed. **Camera:** `dolly(v, hold_start, hold_end)` (+3 %), `push(v, arrive(t_word), box)` to the next focus,
`cut(v, t_beat, zoom, x, y)` for a new framing. **Composition:** one hero, big, with negative space around it — a
keynote frame has 1 idea, not 4 cards.

**Lab-proven defaults** (use unless the PLAN says otherwise): headlines `reveal="rise", exit="quiet"` · cards `rise`
· hero entrance full-bleed shrink on `"hero"` · scene glue `depth_swap` or `Morph` · camera `dolly` in holds.
The motion *signature* (§6d) still rotates per video inside this grammar: reveal (rise · wipe · ink · mask) ·
glue (Morph · Rig · depth_swap · focus_pull · bento · sheet) · the video's own signature move.

**Self-check before handing over:** `check --dry` motion table has no `!`, every chapter's `still` ≥ 45 %, no `CROWD`,
no `STACK`. Then the 3-frame test (§8b) — and a motion test: "would an Apple motion designer remove anything?" If yes, remove it.

## 6g. Material layer — the look is how things are LIT (2026-10-12, `components/material.py`, proof: `videos/_lab/look-lab`)

Viewers said the videos look "cheap / copied from Claude". Diagnosis from the contact sheets: every video changed its
metaphor, but every frame was drawn the same way — flat shapes, one color, no light, a small icon in the middle of an
empty frame, headline top-left. Motion craft (§6f) can't fix that: the problem is *what* moves, not how.

**1. Look = material (PLAN.md picks one; rotate like the metaphor — not the same as the previous video):**
| Look | Feel | Code |
|---|---|---|
| `flat` | the old look — plain fills | `look="flat"` |
| `lit` | Apple product film: soft studio light from the top-left, gradient body, edges a touch darker (AO), bright top rim (light catching the material), sheen, cast shadow that grows with the object, studio sweep ground, grain + vignette | `look="lit"` |
| `paper` | cut paper: flat color + fibre texture, short stacked shadow, paper ground, parts placed a touch off-square | `look="paper"` |

Primitives (all take `look=`): `material.body` (any shape via `rrect_path` / `poly_path` / `circle_path` /
`drop_path`; `form="box" | "cyl" | "drop"`), `material.cable`, `material.inset` (recesses), `material.spill` (light
falling on things around a glowing part), `material.caustic`, `material.rain`. Frame: `v.stage = …material.stage(…)`
(replaces the background) and `v.finish = …material.finish(…)` (grain + vignette, under the HUD). Tokens: `tk.LOOK`.
New hero components take a `look=` parameter and draw with these — never a second, private shading recipe.

**2. Big hero.** The hero fills 60–80 % of the frame and may crop at the frame edge (`v.add(…, bleed=True)` — art only,
never text; `check` skips the safe-zone test for bleed layers). One hero, one idea per frame. A small object floating in
empty space is the #1 "AI slop" tell. Text stays in the safe column.

**3. Continuity.** The hero stays on screen between chapters (shared element): it grows, dissolves to the next take, or
changes look ON the spoken word — never exit-then-enter.

**4. Volume from light, never extrusion.** §8's "3D extrusions" ban (extruded WordArt type/logos, bevel-and-emboss)
still stands. `lit` gets depth from gradients, shadows and rim light only. `spill` is light falling on a surface — not
a neon glow. Bigger objects get deeper, softer shadows (apple-design skill: bigger surfaces read thicker).

**5. Brand DNA is unchanged** in every look: HUD, fonts, accent blue for words/UI, chapter dots, outro, voice.

## 7. Sound

- Voice on top (recorded by the user, one take). Music bed side-chain ducked under voice (own track −19 dB,
  generated score −13 dB).
- **Generated score** (`engine/audio/music.py`) when no track is given: tempo = `v.bpm`, arrangement follows the chapters
  (intro light · chapters full groove, own arp pattern each · dark recap no drums + bells · outro resolves),
  section changes on the beat with riser + impact. Key + mood (warm · tense · bright · dreamy) are part of the
  video's identity — not the same as the previous video.
- **Styled score (new videos from 2026-10-09, `engine/audio/score.py`)** — `v.music = dict(style=.., key=.., mood=..)`.
  Each style is its own band, groove and tempo; pick one per video, never the same as the previous video:

  | style | BPM | band | for |
  |---|---|---|---|
  | `lofi` | 76–94 | boom-bap + rim, Rhodes, sub, vinyl, swing | santai, ngobrol, everyday tech |
  | `marimba` | 100–116 | mallet ostinato, clap, shaker, pluck bass | main-main, keynote, explainer ringan |
  | `ambient` | 70–90 | felt piano broken chords, wide pad, no drums | tenang, deep, cerita personal |
  | `garage` | 126–136 | 2-step shuffle, chord stabs, sidechain | cepat, urban, hitung mundur |
  | `cinematic` | 88–110 | string ostinato, taiko, bells | tegang, berita, outage |

  Every styled score also has a seeded **motif** (the video's own melody, from chapter 2), two progressions per mood
  (chapters alternate), an arrangement that builds (intro sparse → chapter 1 + bass/drums → later + motif), a fill
  every 8th bar, a style-specific transition (reverse swell · mallet gliss · riser · taiko roll — not one stock
  riser), humanised timing and stereo space. `pulse` = the original score (all videos before 2026-10-09).
  Audition: `claude-video audition` → `.cache/audition/` (music_<style>.wav + kit_<kit>.wav).
- **SFX kit** — `v.sfx_kit = "glass" | "wood" | "soft" | "mech"`: the material of every UI sound, pitched to the
  score's key (pop/tick runs climb the scale, chime = the key's triad, thud = tonic), whooshes rotate 4 shapes.
  Match the metaphor (wood = kampung/kentongan/dapur · glass = UI/app · soft = calm/personal · mech = mesin/loket).
  No kit = the classic set (old videos).
- SFX (synth, `engine/audio/sfx.py`): `key` typing · `pop` chip/card/tag in · `click` cursor/button ·
  `send` chat send · `whoosh` chapter change · `whoosh_dark` into dark section · `chime` success/✓ ·
  `tick` count-up · `rec` recording starts · `thud` big punch word.
- Rule: every visible "event" (card in, click, check) has a sound; ambient motion has none.

## 8. LARANGAN (banned — biar nggak keliatan generik)

- ✗ Stock gradients (purple→pink), neon glow, glassmorphism blur panels, lens flares, 3D extrusions (extruded type/logos —
  volume by light in the `lit` look, §6g, is fine).
- ✗ Emoji as decoration, clip-art icons, drop shadows darker than 12% in light mode.
- ✗ More than one accent color in a frame (chapter dots excepted), any accent other than `#1F5EFF`.
- ✗ Centered body text in light chapters (everything is left-aligned on the column; outro is the only centered screen).
- ✗ Linear motion, bounce on large elements, spinning, zoom-punch transitions, shake.
- ✗ Words on screen that duplicate the narration verbatim (headline = punchline, cards = evidence).
- ✗ Subtitles/captions burned in (TikTok auto-captions exist; the headline does that job).
- ✗ Text smaller than 17px, more than ~12 lines of code visible, more than 3 cards at once.
- ✗ The same headline-top + one-card layout two chapters in a row; > 40% empty content area *by accident* (negative space
  around ONE hero is the Apple look — empty space with nothing in focus is the bug).
- ✗ Hard-coded seconds in scenes, unseeded randomness, content outside the safe column.
- ✗ Translating tech terms into Indonesian ("mesin" for node, "langganan" for reserved instance, "nganggur" for idle) —
  see `GLOSSARY.md`. Everyday UI words may be Indonesian ("Setuju"), tech terms never.

## 8b. Anti-slop (biar nggak kelihatan kayak AI generik)

- ✗ Script clichés: "Di era digital ini", "Tahukah kamu", "Yuk simak", "game changer", "rahasia yang jarang orang tahu",
  vague "Pernah nggak sih…" (a question is fine only if it's specific: a date, a time, a real moment).
- ✗ A video with nothing only Mumeyong could say — every video needs one real experience, number (anonymised), mistake
  or opinion.
- ✗ Stock tech imagery as hero: glowing blue servers, robot/brain, globe with neon lines, padlock+shield, matrix code,
  cloud/gear/rocket icons. The hero is the object of the video's own metaphor.
- ✓ Metaphors from Indonesian daily life; a signature move reused across chapters; one surprise; one deliberate
  imperfection (hand note, tilted stamp, stuck ticket).
- Final test: hide the title, look at 3 random frames — can you tell it's Mumeyong, and *which* video? If not, it's generic.

