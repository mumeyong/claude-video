# Autopilot prompt (dipakai `claude-video "Judul"` → engine/autopilot.py, Claude headless)
<!-- {{SLUG}} / {{TITLE}} diganti otomatis. Ubah teks ini buat ngubah perilaku autopilot. -->

Kamu jalan **headless** (nggak ada user yang bisa jawab). Bikin video MUMEYONG **"{{TITLE}}"** di
`videos/{{SLUG}}/` (folder + SCRIPT.md skeleton udah dibikin). Pakai skill `mumeyong-video` dan ikuti
CLAUDE.md — terutama rule 1 (JANGAN render apa pun), rule 2 (autopilot: semua gate otomatis "oke"), rule 14.
Jalankan engine pakai `.venv/bin/python -m engine <cmd>` — cuma `check`, `naskah`, `estimate`, `api`, `register`.

Urutan — kerjain semuanya sampai selesai, jangan berhenti buat nanya:

1. **Ide** — cek `ideas/` (nomor, judul, slug). Kalau udah ada file idenya: pakai brief/hook/bab di sana dan
   pastikan statusnya 🎬 + link `videos/{{SLUG}}/` (file + `ideas/README.md`). Kalau belum ada: bikin
   `ideas/NN-{{SLUG}}.md` (nomor berikutnya) dari `_TEMPLATE.md`, sesuai `ideas/STRATEGY.md` (lensa "tech di balik
   hal sehari-hari", pilih pilar + QUICK/FULL yang paling cocok), status 🎬, + baris di tabel pilar yang tepat di
   `ideas/README.md`.
2. **Brief** — nggak ada user: pakai default aman (QUICK 60–75 s kalau nggak jelas, CTA follow standar).
   Fakta yang ragu → jangan tampilkan angka spesifik; catat sebagai pertanyaan terbuka.
3. **SCRIPT.md** (+ hook A/B/C, pakai A) → `naskah {{SLUG}}` → `estimate {{SLUG}}`. Cek GLOSSARY.md.
4. **PLAN.md** — beda dari video sebelumnya (`ideas/REGISTRY.md`) → `register {{SLUG}}`.
   Isi baris **Look** (STYLE §6e): default **classic + Apple craft (STYLE §6f)** — boleh + 1–3 reel move sebagai aksen.
   Full reel look cuma buat brand teaser/trailer. Pengecualian §8 cuma berlaku buat reel look.
   **Motion = STYLE §6f, wajib baca sebelum nulis scenes.py**: satu leader, `arrive(T.word(..))`, hold ≥ 0,8 s,
   exit quiet, kontinuitas (`depth_swap`/`Morph`/`Rig`), kamera cuma `dolly`/`push`/`cut`. Contoh: `videos/_lab/apple-lab/scenes.py`.
5. **scenes.py** (+ komponen baru di `engine/components/` kalau perlu → `api`), cover, `hasil/{{SLUG}}/POST.md`,
   isi `REVIEW` dengan 4–6 line id yang paling berisiko.
6. `check {{SLUG}} --dry` → benerin sampai bersih (tanpa error), **termasuk tabel motion**: nggak ada `!`, tiap bab
   still ≥ 45 %, nggak ada `CROWD`/`STACK`. Wajib bersih sebelum selesai.

Jawaban terakhirmu (dicetak di terminal user, maks ± 12 baris, Bahasa Indonesia): hook yang dipakai, metafora,
durasi estimasi, komponen baru, hasil check, dan pertanyaan terbuka (fakta/angka yang perlu dicek user).
Jangan kasih command render — script-nya langsung lanjut render final sendiri (tanpa preview) — jadi **pertanyaan terbuka** di `out/autopilot.md` itu satu-satunya yang dicek user sebelum upload; tulis jelas.
