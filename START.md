# START — bikin video MUMEYONG

Panduan buat kamu (yang nge-render). Claude nulis naskah + kode, **kamu yang jalanin command render**.
Aturan lengkap: `CLAUDE.md` · gaya visual: `.claude/skills/mumeyong-video/STYLE.md`.

## Sekali aja (setup)

```bash
cd ~/aschente/claude-video
source .venv/bin/activate        # tiap buka terminal baru
```
Butuh: Python 3.13, ffmpeg, Pango (sudah ada). Font ada di `assets/fonts/`.

## Ide video

Backlog ada di `ideas/README.md`. Bilang "simpan ide: …" buat nambah, "kerjain ide #01" buat mulai.

## Alur kerja

```
 KAMU                                  CLAUDE
 ────                                  ──────
 1. "Bikin video tentang X"      ──►   tanya yang kurang (takeaway, durasi, CTA)
                                       bikin videos/<slug>/
 2. pilih hook, bilang "ok"      ◄──   SCRIPT.md — 2–3 opsi hook + naskah ([L01]…)
                                       + NASKAH.md — versi bersih buat dibaca
 3. bilang "ok"                  ◄──   TREATMENT.md — 1 baris per kalimat
                                       (headline · visual · gerak · SFX · kata kunci)
                                       estimate timing → tulis scenes.py → check
                                ◄──   kasih command
 4. jalanin sheet / still        ──►   kirim screenshot + catatan
    jalanin preview                    revisi → command baru (± 3 putaran)
 5. baca NASKAH.md → rekam
    voice.wav (1x jalan)
    taruh music.mp3
    jalanin align                ──►   kirim hasil skor → Claude benerin baris yang ditandai
 6. preview lagi                 ──►   tweak timing terakhir
 7. jalanin render                     final.mp4 → upload TikTok
 8. bilang "commit"              ──►   Claude commit (cuma kalau kamu minta)
```

Tiap langkah ada **gerbang**: Claude berhenti dan nunggu "ok" dari kamu sebelum lanjut.

## Command

| Kapan | Command | Hasil |
|---|---|---|
| Cek gaya per kalimat | `python -m engine sheet <slug>` | `videos/<slug>/out/sheet.png` |
| Cek frame tertentu | `python -m engine still <slug> L05 L12 33.5` | `out/stills/*.png` |
| Cek timing + suara | `python -m engine preview <slug>` | `out/preview.mp4` (540×960, 30fps) |
| Satu bagian aja | `python -m engine preview <slug> --from 20 --to 45` | `out/preview_20-45.mp4` |
| Naskah buat dibaca | `python -m engine naskah <slug>` | `NASKAH.md` (Claude biasanya udah bikinin) |
| Setelah rekam suara | `python -m engine align <slug>` | `timing.json` dari suaramu |
| Final | `python -m engine render <slug>` | `out/final.mp4` (1080×1920, 60fps) |
| Dengerin SFX | `python -m engine sfx` | `.cache/sfx_preview/*.wav` |

## Isi folder video

```
videos/<slug>/
├── SCRIPT.md        naskah, 1 kalimat per [Lxx], dikelompokkan per ## BAB (sumber utama)
├── NASKAH.md        versi baca dari SCRIPT.md — ini yang kamu baca waktu rekam (auto-generate)
├── TREATMENT.md     storyboard per kalimat
├── timing.json      waktu tiap kalimat & kata (estimate → align)
├── scenes.py        kode animasinya
├── audio/           voice.wav (kamu), music.mp3 (kamu)
├── assets/          screenshot / gambar PNG yang mau dipakai
└── out/             hasil render (nggak di-commit)
```

## Rekam suara

- Ruangan sepi, mic/HP ± 20 cm dari mulut, simpan sebagai `audio/voice.wav` (48 kHz).
- Buka **NASKAH.md** (di HP / layar kedua) dan baca seluruhnya **sekali jalan**, santai, ± 160 kata/menit.
- **Tebal** = kasih tekanan, *(napas)* = ambil napas, ⏸ = jeda ± 1 detik ganti bab.
- Mau ganti kata-kata? Bilang ke Claude → SCRIPT.md diubah → NASKAH.md di-generate ulang. Jangan edit NASKAH.md langsung.
- Salah ngomong? Diam sebentar, **ulangi kalimat itu**. Aligner otomatis ambil take terakhir yang bagus.
- Nggak perlu nunggu suara buat mulai: visual bisa dibangun & direview pakai timing estimasi dulu.

## Musik

- Royalty-free, ± 128 BPM (Pixabay, Uppbeat, YouTube Audio Library) → `audio/music.mp3`.
- Otomatis turun (ducking) waktu kamu ngomong, naik lagi di jeda antar bab.

## Kasih feedback yang spesifik

- ✅ "L14: kartu kodenya kegedean, headline ganti jadi *Cek sendiri.*"
- ✅ "00:00:42 — chat ngetiknya kecepetan"
- ❌ "kurang bagus" → Claude bakal nanya baris mana

## Kalau error

Copy-paste traceback-nya ke Claude, plus command yang kamu jalanin.
