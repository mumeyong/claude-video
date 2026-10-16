# CRITIQUE — ai-lupa-obrolan-panjang

Critique loop (STYLE §6h). Each round: `python -m engine check <slug> --dry` clean → `python -m engine critique <slug>`
→ read `out/critique/hook.png`, `sheet.png`, `moves.png` → score → fix the 3 worst → next round.

| Round | Hook 0–2 s | Readability | Motion | Variety | Brand | Sound sync | 3 worst problems → fix |
|------:|-----------:|------------:|-------:|--------:|------:|-----------:|------------------------|
| 1 | 7 | 6 | 8 | 7 | 8 | 8 | 1. L12: kertas tempel numpuk di atas baris, dua-duanya nggak kebaca → baris lain diredupin (35 %) pas ringkasan masuk · 2. papan 700 px, sepertiga bawah frame kosong, tulisan kecil di ukuran HP → papan 800 px, huruf sampai 50 px, RAM pindah ke bawah tray · 3. lingkaran di penghapus masih nempel di L12 (recap) → keluar di akhir bab 02 |
| 2 | 7 | 8 | 8 | 8 | 8 | 8 | 1. baris "Halo Mumei! Ada yang bisa dibantu?" mepet tepi kanan papan (huruf 50 px) → "Halo Mumei! Mau dibantu apa?" · 2. catatan "namamu." baru nongol di akhir L11 (±1 s) → mulai di kata "namamu" · 3. — |
| 3 | 7 | 8 | 8 | 8 | 8 | 8 | sisa < 8: hook 0–2 s = brand sting v2 (brand DNA, sengaja nggak diubah); papan + headline baru masuk setelah wipe |

## v2 — chat UI + board (2026-10-13, user feedback: chat part repetitive, wants Apple-style type)

| Round | Hook 0–2 s | Readability | Motion | Variety | Brand | Sound sync | 3 worst problems → fix |
|------:|-----------:|------------:|-------:|--------:|------:|-----------:|------------------------|
| 1 | 7 | 5 | 8 | 8 | 8 | 8 | 1. wrapped bubbles overlap under canvas scale (Pango line spacing collapses) → wrap once in design units, draw line by line (obrolan.py) · 2. board rows in Inter run off the right edge → papan_tulis fits the widest row · 3. "NAMAMU IKUT TERHAPUS" tag hits the L11 headline → next to the parked eraser; + card showed "0 pesan" mid-flight, phone 0.7 → 0.76 |
| 2 | 7 | 8 | 7 | 8 | 8 | 8 | 1. phone fades ~1 s and sits on top of the incoming board (22.6–22.8 s) → phone recedes in 0.45 s |
| 3 | 7 | 8 | 8 | 8 | 8 | 8 | sisa < 8: hook 0–2 s = brand sting v2 (brand DNA). Lower ~25 % of the frame is empty in 00 (phone + card end ≈ y 1390). |
