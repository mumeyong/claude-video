# CRITIQUE — <slug>

Critique loop (STYLE §6h). Each round: `python -m engine check <slug> --dry` clean → `python -m engine critique <slug>`
→ read `out/critique/hook.png`, `sheet.png`, `moves.png` → score → fix the 3 worst → next round.
Stop when every score is ≥ 8, or after 3 rounds (list what's still < 8 in the final message).

| Round | Hook 0–2 s | Readability | Motion | Variety | Brand | Sound sync | 3 worst problems → fix |
|------:|-----------:|------------:|-------:|--------:|------:|-----------:|------------------------|
| 1 |  |  |  |  |  |  | 1. … (L05 / 12.4 s) → … · 2. … · 3. … |

- **Hook:** something moving + a reason to stay before 2 s (hook.png frame 8 tells the story without sound)?
- **Readability:** every text legible at phone size in sheet.png (¼ scale ≈ thumb view); one idea per frame?
- **Motion:** in moves.png each entrance starts at rest, one leader, settles; no pop, no stop-and-go (`track()`).
- **Variety:** something new every 2–4 s; chapters don't repeat the same move.
- **Brand:** STYLE banned list (§8, §8b), tokens only, accent blue, HUD, one hero per frame.
- **Sound sync:** every visible arrival has a `v.sfx` on the arrival (not the start); gaps snap to `video.beat`.
