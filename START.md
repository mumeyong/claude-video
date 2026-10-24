# START — bikin video MUMEYONG

**Claude** nulis naskah, rencana, dan kode animasinya. **Kamu** yang render, rekam suara (opsional), dan upload.
Aturan lengkap: `CLAUDE.md` · yang dikunci: `.claude/skills/mumeyong-video/IDENTITY.md` · ide gaya (opsional): `STYLE.md`.
Yang tetap cuma **suaramu dan logo penutup** (logo pembuka dihapus sejak 23-10-2026 — hook langsung di detik 0) — look, warna, font, animasi, struktur bebas dipilih Claude.

## Alurnya: satu command

```
1. PILIH      souffle ideas      lihat ide yang belum dibikin (nomor + judul)
2. BIKIN      souffle 24         Claude nulis semuanya → langsung render FINAL → hasil/<slug>/
                                      (mp4 + cover.png + POST.md). Tinggal tunggu, nggak perlu buka `claude`.
3. CEK        baca "⚠ CEK SEBELUM UPLOAD" di akhir output — fakta/opini yang cuma kamu yang tahu
4. UPLOAD     hasil/<slug>/<slug>.mp4 + caption dari POST.md
```

Ada yang mau diubah? Buka `claude` → "video 24: L14 kegedean" → jalanin `souffle 24` lagi.
Mau lihat dulu versi cepat 480p? `souffle 24 preview` (opsional).

Setelah upload: kirim link (+ views) ke Claude → dicatat, foldernya dipindah ke `_tayang/` / `_arsip/`.
Mau simpan ke git? Bilang "commit" — Claude nggak pernah commit sendiri.

## Mulai dari mana: nomor ide atau judul?

| Kamu ketik | Artinya |
|---|---|
| `souffle 24` | **Dari ide di backlog** (`ideas/24-*.md`). Brief + hook-nya dipakai, status ide → 🎬. **Paling aman.** |
| `souffle "Judul baru"` | **Video baru** tanpa ide. Claude bikin idenya sendiri dari judul itu. |
| `souffle "promo X" --url https://x.com --dur 20` | Sama, plus Claude baca halaman itu buat fakta asli (`--url`) dan naskahnya pas ± 20 detik (`--dur`). |
| `souffle <slug>` atau nomornya | **Video yang sudah ada** → render final lagi (setelah revisi). |

⚠ Judul cuma dianggap ide yang sudah ada kalau **persis sama**. Beda dikit → jadi video baru (dobel). Pakai nomor.

## Ide

- Daftar semua ide: `ideas/README.md` · status: 💡 ide → ⭐ dipilih → 🎬 produksi → ✅ tayang (🗑 batal)
- Urutan tayang yang disarankan: `ideas/STRATEGY.md` §7 · antrean upload: `hasil/README.md`
- **Nambah ide:** bilang ke Claude "simpan ide: …"
- Biar nggak generik: kasih Claude **satu angka / screenshot asli** per video.

## Folder

```
ideas/              backlog ide
videos/<slug>/      video yang lagi dikerjain (SCRIPT.md, NASKAH.md, PLAN.md, scenes.py, audio/, out/)
hasil/<slug>/       siap upload: <slug>.mp4 + cover.png + POST.md (caption tiap platform)
videos/_arsip/  hasil/_tayang/    sudah selesai / sudah tayang
```

Yang di-upload **selalu** `hasil/<slug>/<slug>.mp4` (1080×1920 60fps). `out/preview.mp4` (kalau pakai `preview`) cuma 540p.
mp4/png/wav nggak masuk git — backup sendiri.

## Suara

- **Nggak rekam?** Suara AI "Mumeyong" dibikin otomatis (butuh internet). Tayang pakai ini → nyalain label
  "AI-generated content" di TikTok/YouTube. Salah ucap → tambahin di `audio/tts_lexicon.txt` (`airflow = erflo`).
- **Rekam sendiri:** baca `videos/<slug>/NASKAH.md` sekali jalan, simpan `videos/<slug>/audio/voice.wav` →
  `souffle <slug>` lagi (align otomatis, rekaman asli selalu menang, final dirender ulang). Salah ngomong? Diam sebentar, ulangi kalimatnya.
- **Coba suara Cartesia** (lebih natural, ada emosi; free plan cukup buat tes, nggak boleh komersial): daftar di
  play.cartesia.ai → API key → `cp .cartesia.example .cartesia`, isi `key` → `souffle voices` (daftar suara
  Indonesia) → isi `voice` → `souffle apple-lab`. Semua video pakai Cartesia, kecuali yang ada di `skip =`; suara lama
  disimpan di `audio/voice_tts.prev.wav` buat dibandingin. Mau diposting → wajib plan Pro ($5/bln). Teks naskah dikirim ke Cartesia.
- Musik + SFX dibikin otomatis. Mau lagu sendiri: `audio/music.mp3`. Dengerin pilihan: `souffle audition`.

## Feedback yang enak buat Claude

✅ "L14: angkanya kegedean" · ✅ "00:42 zoom-nya kecepetan" · ❌ "kurang bagus"

**Gerakan = mengalir, nggak pernah beku** (STYLE §3, dari refs.pdf): satu yang gerak duluan, mendarat pas kata yang
ditekan, lalu langsung nyambung ke gerakan berikutnya — satu bentuk yang berubah wujud, bukan hilang-muncul.
Render final otomatis pakai **motion blur** (4 subframe per frame), jadi gerakan cepat kelihatan halus, bukan
patah-patah (render final jadi sedikit lebih lama). Claude ngecek frame beku (DEAD) di `check --dry` (tanpa render).
Mau lihat contohnya: `souffle apple-lab` (proof sheet ± 45 s, nggak buat diposting).

**Sejak 2026-10-13 semua gerakan pakai spring** (STYLE §3, dari refs.pdf): mulai dari diam, nggak
"nyentak" di frame pertama, dan yang pindah target berkali-kali (kursor, indikator) belok halus pakai `track()`.
Claude juga **ngeliat frame-nya sendiri**: `python -m engine critique <slug>` bikin PNG review (hook 2 detik pertama,
satu frame per baris, tiap awal bab 6 frame) — tanpa encode video/audio — terus dinilai di `videos/<slug>/CRITIQUE.md`
sampai semua skor ≥ 8. Bandingin gerakan lama vs baru: `souffle spring-lab`.

## Animasi HTML (look grak / cheese) — default sejak 2026-10-15

Video baru sekarang digambar sebagai **film HTML** (`videos/<slug>/film.html`, browser) — gaya grak/cheese yang kamu
suka — tapi tetap **suaramu dan logo penutup** dari engine Python. Mau cara lama (gambar di Python)?
Tambah `--py`: `souffle "Judul" --py`.

Animasinya bisa pakai **HyperFrames** (GSAP): cuma 4 skill referensi yang dipasang — `hyperframes-animation`,
`-keyframes`, `-creative`, `-registry` — Claude ambil motion rules, blueprint scene, dan block registry-nya (chart,
terminal, map, glitch…) untuk `film.html`. Tetap suaramu, logomu, dan render-nya tetap `souffle <slug>`. Mau minta?
Tulis aja "pakai HyperFrames" di judul/brief. Update skill-nya: `npx skills update -p` (jangan `npx skills add
heygen-com/hyperframes` — itu masang lagi semua skill workflow-nya).

| Kapan | Command |
|---|---|
| Lihat filmnya live di browser | `souffle serve` → buka `http://localhost:5173/videos/<slug>/film.html` |
| Benerin cuma detik 12–15 (sisanya nggak dirender ulang) | `souffle <slug> --fix 12,15` |
| Gaya dari video/gambar referensi | `souffle "Judul" --ref ~/Downloads/contoh.mp4` |
| Pakai lagu sendiri, potongan pas ketukan | taruh `audio/music.mp3` → `souffle beats <slug>` |
| File khusus TikTok / Shorts / Reels | `souffle export <slug>` → `hasil/<slug>/upload/` |

Contoh bukti: `souffle web-lab` (± 30 s, nggak buat diposting). Render pertama film HTML lebih lama (browser
gambar tiap frame); frame disimpan di `out/.web/`, jadi render ulang tanpa perubahan cepat.

## Command lain

| Kapan | Command |
|---|---|
| Daftar video + tahapnya | `souffle` |
| Preview 480p 30fps (opsional) | `souffle <slug> preview` · sebagian: `… preview --from 20 --to 45` |
| Cuma bikin folder (tanpa Claude) | `souffle new "Judul"` |
| Buka folder video | `souffle open <slug>` |
| Review PNG (Claude juga boleh) | `python -m engine critique <slug>` → `out/critique/` |
| Semua command satuan | `souffle help` |

Error? Copy-paste output-nya + command-nya ke Claude. Autopilot gagal di tengah? `claude` → "lanjutin video <slug>".

## Setup di komputer baru

```bash
git clone git@github.com:mumeyong/claude-video.git ~/aschente/souffle
cd ~/aschente/souffle
python3 -m venv --system-site-packages .venv && .venv/bin/pip install faster-whisper edge-tts
(cd web && npm install)            # film HTML: Playwright (pakai Google Chrome yang sudah terpasang) + GSAP
ln -s ~/aschente/souffle/vid ~/.local/bin/souffle   # ~/.local/bin harus ada di PATH
```
Butuh: Python 3.13, Node ≥ 18 + Google Chrome (film HTML), ffmpeg, Pango + PyGObject (`gir1.2-pango-1.0`, `python3-gi`, `python3-cairo`). Font ikut di repo.
