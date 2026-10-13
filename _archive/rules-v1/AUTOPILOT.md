# Autopilot prompt (dipakai `claude-video "Judul"` → engine/autopilot.py, Claude headless)
<!-- {{SLUG}} / {{TITLE}} diganti otomatis. Ubah teks ini buat ngubah perilaku autopilot. -->

Kamu jalan **headless** (nggak ada user yang bisa jawab). Bikin video MUMEYONG **"{{TITLE}}"** di
`videos/{{SLUG}}/` (folder + SCRIPT.md skeleton udah dibikin). Pakai skill `mumeyong-video` dan ikuti
CLAUDE.md — terutama rule 1 (JANGAN render apa pun), rule 2 (autopilot: semua gate otomatis "oke"), rule 14.
Jalankan engine pakai `.venv/bin/python -m engine <cmd>` — cuma `check`, `naskah`, `estimate`, `api`, `recent`, `register`, `critique`.

Urutan — kerjain semuanya sampai selesai, jangan berhenti buat nanya:

0. **Konteks — tiga bacaan, sekali aja** (hemat token: tiap panggilan ngirim ulang semua yang udah kebaca; output Bash
   kepotong di ± 30k karakter, makanya dibagi tiga):
   a. `Read .claude/skills/mumeyong-video/STYLE.md`
   b. `S=.claude/skills/mumeyong-video; cat $S/GLOSSARY.md $S/LESSONS.md $S/templates/PLAN.md $S/templates/SCRIPT_QUICK.md $S/templates/scenes.py ideas/STRATEGY.md; .venv/bin/python -m engine recent {{SLUG}}`
   c. `.venv/bin/python -m engine api core && .venv/bin/python -m engine api index`
   + file ide-nya (kalau ada). Itu SEMUA yang kamu butuh. **Jangan** buka scenes.py / SCRIPT.md video lain, `videos/_lab/*`,
   `engine/API.md` utuh, `ideas/REGISTRY.md` utuh, atau source komponen — `recent` = yang harus beda + episode sebelumnya,
   `templates/scenes.py` = grammar terkini, `api <modul>` = signature satu kit (cuma kalau kit itu dipakai).
   Kualitas nggak turun: aturan unik (§6c), Apple craft (§6f), material (§6g) tetap wajib — yang dihemat cuma bacaan ganda.

1. **Ide** — cek `ideas/` (nomor, judul, slug). Kalau udah ada file idenya: pakai brief/hook/bab di sana dan
   pastikan statusnya 🎬 + link `videos/{{SLUG}}/` (file + `ideas/README.md`). Kalau belum ada: bikin
   `ideas/NN-{{SLUG}}.md` (nomor berikutnya) dari `_TEMPLATE.md`, sesuai `ideas/STRATEGY.md` (lensa "tech di balik
   hal sehari-hari", pilih pilar + QUICK/FULL yang paling cocok), status 🎬, + baris di tabel pilar yang tepat di
   `ideas/README.md`.
2. **Brief** — nggak ada user: pakai default aman (QUICK 60–75 s kalau nggak jelas, CTA follow standar).
   Fakta yang ragu → jangan tampilkan angka spesifik; catat sebagai pertanyaan terbuka.
3. **SCRIPT.md** (+ hook A/B/C, pakai A) → `naskah {{SLUG}}` → `estimate {{SLUG}}`. Cek GLOSSARY.md.
4. **PLAN.md** — beda dari video sebelumnya (output `recent` di langkah 0) → `register {{SLUG}}`.
   Isi baris **Look** (STYLE §6e): default **classic + Apple craft (STYLE §6f)** — boleh + 1–3 reel move sebagai aksen.
   Full reel look cuma buat brand teaser/trailer. Pengecualian §8 cuma berlaku buat reel look.
   **Motion = STYLE §6f, wajib baca sebelum nulis scenes.py**: satu leader, `arrive(T.word(..))`, hold ≥ 0,8 s,
   exit quiet, kontinuitas (`depth_swap`/`Morph`/`Rig`), kamera cuma `dolly`/`push`/`cut`. Contoh: `templates/scenes.py` (udah kebaca di langkah 0).
   **Craft v2 (STYLE §6f+)**: pilih 1–3 gerakan `craft` yang *melayani metaforanya* (mis. `draw_on` buat rute/kabel,
   `count_up` buat angka, `morph_path` buat hero yang berubah bentuk, `carry` sebagai seam) — beda dari video
   sebelumnya kalau bisa; jangan semua dipakai sekaligus. Tulis pilihannya di baris Motion PLAN.md.
5. **scenes.py** (+ komponen baru di `engine/components/` kalau perlu → `api`), cover, `hasil/{{SLUG}}/POST.md`,
   isi `REVIEW` dengan 4–6 line id yang paling berisiko.
   Tulis scenes.py **sekali, utuh** (Write), komponen baru juga — lalu cuma `Edit` kecil. Jangan `Read` ulang file yang
   barusan kamu tulis. Gabung command yang nggak saling nunggu dalam satu Bash (`naskah` + `estimate`; `api` + `check`).
6. `check {{SLUG}} --dry` → benerin sampai bersih (tanpa error), **termasuk tabel motion**: nggak ada `!`, tiap bab
   still ≥ 45 %, nggak ada `CROWD`/`STACK`. Wajib bersih sebelum selesai. **Easing check** juga: `out_expo`/`out_back`
   → `glide`/`pop`, nilai dengan 2+ target → `track()` (STYLE §6h).
7. **Critique loop (STYLE §6h)** — `critique {{SLUG}}` lalu `Read` `videos/{{SLUG}}/out/critique/hook.png`, `sheet.png`,
   `moves.png`. Skor 1–10 (hook 0–2 s · readability · motion · variety · brand · sound sync) di
   `videos/{{SLUG}}/CRITIQUE.md` (template `templates/CRITIQUE.md`), benerin 3 masalah terburuk, `check --dry` +
   `critique` lagi. Ulang sampai semua ≥ 8 atau 3 ronde; yang masih < 8 masuk pertanyaan terbuka.

Jawaban terakhirmu (dicetak di terminal user, maks ± 12 baris, Bahasa Indonesia): hook yang dipakai, metafora,
durasi estimasi, komponen baru, hasil check, skor critique terakhir, dan pertanyaan terbuka (fakta/angka yang perlu dicek user).
Jangan kasih command render — script-nya langsung lanjut render final sendiri (tanpa preview) — jadi **pertanyaan terbuka** di `out/autopilot.md` itu satu-satunya yang dicek user sebelum upload; tulis jelas.
