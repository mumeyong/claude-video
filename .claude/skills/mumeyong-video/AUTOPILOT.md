# Autopilot prompt (`claude-video "Judul"` → engine/autopilot.py, Claude headless). {{SLUG}} / {{TITLE}} are filled in.

Kamu jalan headless — nggak ada user yang bisa ditanya. Bikin video MUMEYONG **"{{TITLE}}"** di `videos/{{SLUG}}/`.
Yang tetap cuma suara, logo pembuka, logo penutup (`IDENTITY.md`); look, warna, font, animasi, struktur terserah kamu. JANGAN render.
Engine: `.venv/bin/python -m engine <cmd>` — cuma `check`, `naskah`, `estimate`, `api`, `recent`, `register`, `critique`,
`ref`, `capture`, `beats`.
Mode: {{MODE}}

1. Baca sekali: `IDENTITY.md`, `STYLE.md`, `LESSONS.md`, `GLOSSARY.md`, file ide-nya di `ideas/` (kalau ada),
   `recent {{SLUG}}`, dan bahan mode-nya (`WEB.md` atau `api core` + `api index`). Film DOM/GSAP: boleh pakai skill `hyperframes-animation`,
   `hyperframes-keyframes`, `hyperframes-registry` sebagai referensi motion (WEB.md § HyperFrames) — bukan workflow/render-nya. Jangan buka video lain atau source komponen.
2. Kalau belum ada file ide: bikin dari `ideas/_TEMPLATE.md` + baris di `ideas/README.md`; status 🎬.
3. SCRIPT.md → `naskah` → `estimate` · PLAN.md dengan **Frame** (STYLE §2: bukan house frame, `v.hud = False`,
   komposisi beda tiap bab, font pairing sendiri) → `register` · gambarnya (lihat Mode) + cover + `hasil/{{SLUG}}/POST.md` + `REVIEW`.
4. `check {{SLUG}} --dry` sampai nggak ada `✗`, lalu critique loop (maks 3 ronde).
5. Fakta ragu → jangan tampilkan angka; tulis sebagai pertanyaan terbuka.

Jawaban terakhir (≤ 12 baris, Bahasa Indonesia): hook, idenya, durasi, komponen baru, hasil check, skor critique,
pertanyaan terbuka. Jangan kasih command render — script-nya lanjut render sendiri.
