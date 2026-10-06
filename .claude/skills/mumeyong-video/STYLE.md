# MUMEYONG — STYLE.md (buku panduan gaya)

Measured from the reference (beyondstudioid "Tutorial membuat animasi dengan Claude Code", 2026).
Code mirror: `engine/tokens.py`. If you change a value here, change it there too.

## 1. WAJIB (always)

| Thing | Value |
|---|---|
| Canvas | 1080×1920, 60 fps, H.264 yuv420p, AAC 192k, −14 LUFS |
| Language | Bahasa Indonesia, casual "aku/kamu", short punchy sentences |
| Brand | HUD top-left `MUMEYONG · TUTORIAL` (series word can change per video) |
| Ending | dark recap → logo + "Follow" click → contact pills |
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
- Headline: words enter one by one — blur 18→0, rise 26→0, opacity 0→1, 0.55 s, stagger 0.06 s.
- Cards: rise 48, scale .965→1, blur 12→0, 0.6 s. Stagger sibling cards 0.08–0.12 s.
- Exit (scene change): blur → 14, fade, drift up 14–18 px, 0.35 s. Everything leaves together.
- Chapter change: headline/cards exit, HUD label crossfades, dot fills with chapter color, bg tint crossfades 0.6 s, kicker slides in from −14 px. A `whoosh` SFX lands on it.
- Focus: dim the rest to 30%, outline the focused line in blue; or a selection box.
- Typing: 34 cps (chat), ~120 cps (code). Every typed char = `key` SFX.
- Resting elements may idle-float 2–4 px (`wobble`). Never bounce big things; `out_back` only for small pops (chips, check marks).
- One visual change per spoken sentence (~every 2.5 s). If a line is > 4 s, add a second beat inside it (highlight, count-up, cursor).

## 6b. Composition — NOT a template

The skeleton (HUD, kicker, headline, chapter dots) stays constant; **what's under it must change every chapter.**

- **Hero object per chapter**, filling ≥ 50% of the content area (y 520–1450). A small card floating in empty
  space is a bug. Hero vocabulary: giant odometer number · 24h clock ring · receipt · terminal with pop-out
  cards · seat grid + drag-resize · shattering block · staircase chart · typographic battle (10% vs 100%).
- **No two consecutive chapters share a layout.** Rotate between: full-width card · centered hero (no card) ·
  stacked/tilted cards · pure typography · object + hand note.
- **At least one camera move per chapter** (`v.camera`): push-in on the detail being spoken, punch-out (zoom
  0.97, 0.35 s) on a big number, pull-out (1.2 → 1.0) on a reveal. Never more than ±22% zoom.
- **Vary transitions inside and between chapters** — `appear(enter=, exit=)`: whip left/right, drop down,
  pop, blur. Mid-chapter scene changes use a whip; chapter changes keep the blur/HUD crossfade.
- **One "punch" moment every ~15–20 s**: giant number or word (`mega`/`giga` tokens) or a stamp slam.
- **Headline may change mid-chapter** when the visual changes (`Cari yang *bocor*.` → `Nyala jam _dua_ pagi?`).
- **Hand notes** (`note()`, Instrument Serif italic blue + arrow) are allowed as annotations — max 2 on screen.
- **Bookends**: the hook's hero object returns in the recap (same number, new meaning).
- Slight tilt (±2–3°) is allowed for stacked cards, receipts and stamps — never for terminals, charts or text.

## 6c. Brand DNA vs identity — unique, never generic

**Brand DNA (fixed in every video, ~40%)** — HUD, fonts, accent blue `#1F5EFF`, chapter dots, motion feel
(blur-in, easing, transition rhythm), outro/logo/CTA, SFX palette. Never changes per video.

**Identity (chosen per video, ~60%)** — written in `videos/<slug>/IDENTITY.md` (phase 1.5) from
`IDENTITY_TEMPLATE.md`, checked against `ideas/REGISTRY.md`:
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

## 7. Sound

- Voice on top (recorded by the user, one take). Music bed side-chain ducked under voice (own track −19 dB,
  generated score −13 dB).
- **Generated score** (`engine/audio/music.py`) when no track is given: tempo = `v.bpm`, arrangement follows the chapters
  (intro light · chapters full groove, own arp pattern each · dark recap no drums + bells · outro resolves),
  section changes on the beat with riser + impact. Key + mood (warm · tense · bright · dreamy) are part of the
  video's identity — not the same as the previous video.
- SFX (synth, `engine/audio/sfx.py`): `key` typing · `pop` chip/card/tag in · `click` cursor/button ·
  `send` chat send · `whoosh` chapter change · `whoosh_dark` into dark section · `chime` success/✓ ·
  `tick` count-up · `rec` recording starts · `thud` big punch word.
- Rule: every visible "event" (card in, click, check) has a sound; ambient motion has none.

## 8. LARANGAN (banned — biar nggak keliatan generik)

- ✗ Stock gradients (purple→pink), neon glow, glassmorphism blur panels, lens flares, 3D extrusions.
- ✗ Emoji as decoration, clip-art icons, drop shadows darker than 12% in light mode.
- ✗ More than one accent color in a frame (chapter dots excepted), any accent other than `#1F5EFF`.
- ✗ Centered body text in light chapters (everything is left-aligned on the column; outro is the only centered screen).
- ✗ Linear motion, bounce on large elements, spinning, zoom-punch transitions, shake.
- ✗ Words on screen that duplicate the narration verbatim (headline = punchline, cards = evidence).
- ✗ Subtitles/captions burned in (TikTok auto-captions exist; the headline does that job).
- ✗ Text smaller than 17px, more than ~12 lines of code visible, more than 3 cards at once.
- ✗ The same headline-top + one-card layout two chapters in a row; a chapter with no camera move; > 40% empty content area.
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

