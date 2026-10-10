# START — bikin video MUMEYONG

**Claude** nulis naskah, rencana, dan kode animasinya. **Kamu** yang render, rekam suara (opsional), dan upload.
Aturan lengkap: `CLAUDE.md` · gaya visual: `.claude/skills/mumeyong-video/STYLE.md`.

## Alurnya: satu command

```
1. PILIH      claude-video ideas      lihat ide yang belum dibikin (nomor + judul)
2. BIKIN      claude-video 24         Claude nulis semuanya → langsung render FINAL → hasil/<slug>/
                                      (mp4 + cover.png + POST.md). Tinggal tunggu, nggak perlu buka `claude`.
3. CEK        baca "⚠ CEK SEBELUM UPLOAD" di akhir output — fakta/opini yang cuma kamu yang tahu
4. UPLOAD     hasil/<slug>/<slug>.mp4 + caption dari POST.md
```

Ada yang mau diubah? Buka `claude` → "video 24: L14 kegedean" → jalanin `claude-video 24` lagi.
Mau lihat dulu versi cepat 540p? `claude-video 24 preview` (opsional).

Setelah upload: kirim link (+ views) ke Claude → dicatat, foldernya dipindah ke `_tayang/` / `_arsip/`.
Mau simpan ke git? Bilang "commit" — Claude nggak pernah commit sendiri.

## Mulai dari mana: nomor ide atau judul?

| Kamu ketik | Artinya |
|---|---|
| `claude-video 24` | **Dari ide di backlog** (`ideas/24-*.md`). Brief + hook-nya dipakai, status ide → 🎬. **Paling aman.** |
| `claude-video "Judul baru"` | **Video baru** tanpa ide. Claude bikin idenya sendiri dari judul itu. |
| `claude-video <slug>` atau nomornya | **Video yang sudah ada** → render final lagi (setelah revisi). |

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
  `claude-video <slug>` lagi (align otomatis, rekaman asli selalu menang, final dirender ulang). Salah ngomong? Diam sebentar, ulangi kalimatnya.
- Musik + SFX dibikin otomatis. Mau lagu sendiri: `audio/music.mp3`. Dengerin pilihan: `claude-video audition`.

## Feedback yang enak buat Claude

✅ "L14: angkanya kegedean" · ✅ "00:42 zoom-nya kecepetan" · ❌ "kurang bagus"

**Gerakan = gaya Apple keynote** (STYLE §6f, sejak 2026-10-11): satu yang gerak duluan, mendarat pas kata yang
ditekan, terus diam sebentar. Claude ngecek ini sendiri lewat tabel *motion* di `check --dry` (tanpa render).
Mau lihat contohnya: `claude-video apple-lab` (proof sheet ± 45 s, nggak buat diposting).

## Command lain

| Kapan | Command |
|---|---|
| Daftar video + tahapnya | `claude-video` |
| Preview 540p (opsional) | `claude-video <slug> preview` · sebagian: `… preview --from 20 --to 45` |
| Cuma bikin folder (tanpa Claude) | `claude-video new "Judul"` |
| Buka folder video | `claude-video open <slug>` |
| Semua command satuan | `claude-video help` |

Error? Copy-paste output-nya + command-nya ke Claude. Autopilot gagal di tengah? `claude` → "lanjutin video <slug>".

## Setup di komputer baru

```bash
git clone git@github.com:mumeyong/claude-video.git ~/aschente/claude-video
cd ~/aschente/claude-video
python3 -m venv --system-site-packages .venv && .venv/bin/pip install faster-whisper edge-tts
ln -s ~/aschente/claude-video/vid ~/.local/bin/claude-video   # ~/.local/bin harus ada di PATH
```
Butuh: Python 3.13, ffmpeg, Pango + PyGObject (`gir1.2-pango-1.0`, `python3-gi`, `python3-cairo`). Font ikut di repo.
