# CRITIQUE — <slug>

Critique loop (STYLE §6). Each round: `python -m engine check <slug> --dry` clean → `python -m engine critique <slug>`
→ read `out/critique/hook.png`, `sheet.png`, `moves.png` → score → fix the 3 worst → next round.
Stop when every score is ≥ 8, or after 3 rounds (list what's still < 8 in the final message).

| Round | Hook 0–2 s | Readability | Layout | Motion | Variety | Brand | Sound sync | 3 worst problems → fix |
|------:|-----------:|------------:|-------:|-------:|--------:|------:|-----------:|------------------------|
| 1 |  |  |  |  |  |  |  | 1. … (L05 / 12.4 s) → … · 2. … · 3. … |

- **Hook:** something moving + a reason to stay before 2 s (hook.png frame 8 tells the story without sound)?
- **Readability:** every text legible at phone size in sheet.png (¼ scale ≈ thumb view); one idea per frame?
- **Layout:** in sheet.png, how many frames are the house frame (headline top-left + hero centre + empty bottom)?
  More than one → ≤ 4. Do the chapters look like different posters? Is type placed with intent?
- **Motion:** in moves.png each entrance starts at rest and flows into the next; no frozen frames (check DEAD), no
  stop-and-go (`track()`), one shape morphing rather than fade-out/fade-in.
- **Variety:** something new every 2–4 s; chapters don't repeat the same move.
- **Brand:** opening logo + ending logo + voice intact (IDENTITY.md); does it look like a deliberate choice, not a default?
- **Sound sync:** every visible arrival has a `v.sfx` on the arrival (not the start); gaps snap to `video.beat`.
