# MUMEYONG — STYLE.md (craft guide — freedom inside IDENTITY.md)

`IDENTITY.md` is fixed. This file is taste: defaults that usually look good. Break any of them when the idea is
better for it — the critique loop (§5) is the judge, not this list. Older rule sets: `_archive/` (don't read).

## 1. Ideas worth reaching for
- **A metaphor from Indonesian daily life** often carries a whole video (rusun water pipe, guest book at the
  security post, a warung's order slips). The hero is that object, not a tech icon. A real chat UI, a terminal, or
  pure type is fine too when the subject is literally that.
- A **signature move** the video owns, reused later. A hook that moves before 2 s: number first, myth struck out, a
  specific question, cold open mid-action, before/after, a real viewer comment — or something new.
- Look: `flat` small or big hero, `paper`, `lit`; reel smears for teasers. Build new components when it helps.
- Repeating yourself is the real risk. Glance at `python -m engine recent <slug>` and do something you haven't done.

## 2. Composition
- One idea per frame, a hero with air around it; a small card floating in empty space usually reads as a bug.
- Keep something on screen across chapter changes (shared element) — avoid blank frames.
- Change the layout between chapters; give the viewer a punch (giant number/word, full-bleed hero) now and then.
- Headline = the punchline, not the narration: short, one `*accent*` word.

## 3. Motion — what makes it feel smooth
- **Start from rest:** `ios_at`, `glide(p)`, `pop(p, s)`, `curve("apple_out")`; 2+ targets → `track(t, frames, preset)`
  so it bends instead of stop-and-go. `out_expo` for impacts only. Never scale from 0.
- **One leader**, the rest `follow()` a beat later with less travel. **Land on the stressed word**
  (`arrive(T.word(...))`), SFX on the arrival.
- **Hold** after arrivals — stillness is what makes the moves read. Exits quieter and faster than entrances.
- Bigger things move slower. Opacity + one transform per element. Camera moves during holds, not over busy frames.
- Toolbox (`python -m engine api core` / `api index`): `draw_on`, `mark`, `split_rise`, `count_up`, `morph_path`,
  `carry`, `rack_cut`, `shutter`, `indicator`, `chat_phone`, `Rig`, `Morph`, `bento`, `papan_tulis`. Use what the
  idea needs; invent the rest in scenes.py.

## 4. Sound
- Voice on top, music ducked. `v.music = dict(style=, key=, mood=)` with `Video(bpm=)`: `lofi` 76–94 · `marimba`
  100–116 · `ambient` 70–90 · `garage` 126–136 · `cinematic` 88–110. `v.sfx_kit = "glass"|"wood"|"soft"|"mech"`.
- A sound on every visible event's frame: `key` `pop` `click` `send` `whoosh` `whoosh_dark` `chime` `tick` `rec` `thud`.

## 5. Look at your frames (the one required step)
1. `python -m engine check <slug> --dry` — fix every `✗`. `!` notes (safe zone, tiny text, still %, CROWD, easing)
   are hints: fix them or know why not.
2. `python -m engine critique <slug>` → read `out/critique/hook.png`, `sheet.png`, `moves.png` like a viewer would.
   Score in `CRITIQUE.md`, fix the 3 worst, repeat until all ≥ 8 or 3 rounds.
3. Hide the title, look at 3 random frames: clearly Mumeyong (IDENTITY.md), and clearly *this* video?
