# Autopilot prompt (`claude-video "Judul"` → engine/autopilot.py, Claude headless). {{SLUG}} / {{TITLE}} are filled in.

Kamu jalan headless — nggak ada user yang bisa ditanya. Bikin video MUMEYONG **"{{TITLE}}"** di `videos/{{SLUG}}/`.
Ikuti skill `mumeyong-video` (SKILL.md → STYLE.md) dan CLAUDE.md. JANGAN render apa pun.
Engine: `.venv/bin/python -m engine <cmd>` — cuma `check`, `naskah`, `estimate`, `api`, `recent`, `register`, `critique`.

1. Baca sekali: `STYLE.md`, `LESSONS.md`, `GLOSSARY.md`, templates, file ide-nya di `ideas/` (kalau ada), `recent {{SLUG}}`,
   `api core` + `api index`. Jangan buka video lain, labs, atau source komponen.
2. Ide: kalau belum ada file di `ideas/`, bikin dari `_TEMPLATE.md` + baris di `ideas/README.md`; status 🎬.
3. SCRIPT.md → `naskah` → `estimate` · PLAN.md → `register` · scenes.py + cover + `hasil/{{SLUG}}/POST.md` + `REVIEW`.
   Tulis tiap file sekali utuh, lalu cuma edit kecil.
4. STYLE §8: `check {{SLUG}} --dry` sampai bersih, lalu critique loop (maks 3 ronde).
5. Fakta ragu → jangan tampilkan angka; tulis sebagai pertanyaan terbuka.

Jawaban terakhir (≤ 12 baris, Bahasa Indonesia): hook, metafora, durasi, komponen baru, hasil check, skor critique,
pertanyaan terbuka. Jangan kasih command render — script-nya lanjut render sendiri.
