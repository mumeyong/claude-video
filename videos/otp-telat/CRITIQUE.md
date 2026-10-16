# CRITIQUE — otp-telat

Critique loop (STYLE §5). Each round: `python -m engine check otp-telat --dry` clean → `python -m engine critique otp-telat`
→ read `out/critique/hook.png`, `sheet.png`, `moves.png` → score → fix the 3 worst → next round.

| Round | Hook 0–2 s | Readability | Motion | Variety | Brand | Sound sync | 3 worst problems → fix |
|------:|-----------:|------------:|-------:|--------:|------:|-----------:|------------------------|
| 1 | 8 | 7 | 8 | 8 | 8 | 8 | 1. L03 16,8 s "surat" punch too small (300 px, empty frame) → 540 px hero · 2. L08 44 s tray overlaps the piled rows, its sub line hidden under the letter → tray up to y 536, letter centred, text clear · 3. L11 63 s two lanes tiny + empty middle → bigger belt/letters (140 px), tags h 52, notif 760 px wide |
| 2 | 8 | 7 | 8 | 8 | 8 | 8 | 1. 00–02 the small phone's timer (the signature) only ~20 px → phone s 0,34 → 0,40 (timer ≈ 23 px), moved up to stay above y 1560 · 2. 01 belt legs touch the bigger phone → legs 56 · 3. L11 WhatsApp notif would collide with the bigger phone → 560 px wide, y 990 |
| 3 | 8 | 8 | 8 | 8 | 8 | 8 | all ≥ 8 — left as is: L09–L10 the log sheet covers the small phone for ~6 s (the timer pauses from view); L13 the two HANGUS stamps sit tight next to each other; 01 the belt's right roller sits close above the phone |
