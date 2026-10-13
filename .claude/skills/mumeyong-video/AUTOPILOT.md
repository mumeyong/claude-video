# Autopilot prompt (`claude-video "Judul"` → engine/autopilot.py, Claude headless). {{SLUG}} / {{TITLE}} are filled in.

Kamu jalan headless — nggak ada user yang bisa ditanya. Bikin video MUMEYONG **"{{TITLE}}"** di `videos/{{SLUG}}/`.
Identitas tetap (`IDENTITY.md`); sisanya bebas — metafora, struktur, layout, motion terserah kamu. JANGAN render.
Engine: `.venv/bin/python -m engine <cmd>` — cuma `check`, `naskah`, `estimate`, `api`, `recent`, `register`, `critique`.

1. Baca sekali: `IDENTITY.md`, `STYLE.md`, `LESSONS.md`, `GLOSSARY.md`, file ide-nya di `ideas/` (kalau ada),
   `recent {{SLUG}}`, `api core` + `api index`. Jangan buka video lain atau source komponen.
2. Kalau belum ada file ide: bikin dari `ideas/_TEMPLATE.md` + baris di `ideas/README.md`; status 🎬.
3. SCRIPT.md → `naskah` → `estimate` · scenes.py + cover + `hasil/{{SLUG}}/POST.md` + `REVIEW` · PLAN.md → `register`.
4. `check {{SLUG}} --dry` sampai nggak ada `✗`, lalu critique loop (maks 3 ronde).
5. Fakta ragu → jangan tampilkan angka; tulis sebagai pertanyaan terbuka.

Jawaban terakhir (≤ 12 baris, Bahasa Indonesia): hook, idenya, durasi, komponen baru, hasil check, skor critique,
pertanyaan terbuka. Jangan kasih command render — script-nya lanjut render sendiri.
