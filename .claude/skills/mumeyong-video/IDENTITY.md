# MUMEYONG — IDENTITY.md (fixed — the only law)

Everything here is the same in every video; everything else is your call (`STYLE.md` is a craft guide, not rules).
Values live in `engine/tokens.py`.

## Format
- 1080×1920, 60 fps, −14 LUFS. Casual Indonesian (aku/kamu), short spoken sentences, in Mumeyong's voice.
- **Tech terms stay English** (`GLOSSARY.md`); Indonesian affixes are fine (*di-scale, pod-nya*).
- Safe column x 81–929; nothing that matters below y 1560 or above y 240 (except HUD). Text ≥ 17 px.

## Brand
- Open with the brand sting (`PRE_ROLL = 2.05` + `brand_intro(v, version=2)`); close with `standard_outro`.
- HUD (mono, top + bottom) and chapter dots (`v.chapter`). Cover (`v.cover`) + `hasil/<slug>/POST.md`.
- Accent blue `#1F5EFF` is the ONLY accent for words/UI. Other colors from tokens, for objects and tints.
- Type: Inter Display (headlines), Inter (UI, chat, cards), JetBrains Mono (HUD, labels); Instrument Serif italic
  only for a rare `_soft emphasis_`. Numbers in Indonesian format (`fmt_id`).
- Feel: calm and precise — an Apple keynote made by a motion designer. Springs that start from rest.

## Truth
- Never invent a number or a claim — no source, no number on screen. Anonymise clients AND projects.
- Every video says something only Mumeyong would say (an opinion, a real artefact, a lived detail).

## Banned
- Neon glow, glassmorphism, lens flares, stock gradients, 3D-extruded type, glitch/VHS, particle bursts, shake,
  spinning, zoom-punch transitions.
- Stock tech heroes: glowing servers, robot/brain, neon globe, padlock + shield, matrix code, cloud/gear/rocket icons.
- Emoji as decoration, clip-art, burned-in subtitles (the spoken sentence word for word on screen).
- Script clichés: "Di era digital ini", "Tahukah kamu", "Yuk simak", "game changer", vague "Pernah nggak sih…".
- Translated tech terms ("mesin" for node, "nganggur" for idle).
- In code: hard-coded seconds, hex/sizes typed into scenes, unseeded randomness, state between frames (frame = f(t)).
