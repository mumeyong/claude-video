# START — bikin video MUMEYONG

Panduan buat kamu. **Claude** nulis naskah, storyboard, dan kode animasinya.
**Kamu** yang jalanin render (Claude nggak pernah nge-render sendiri), rekam suara, dan upload.
Aturan lengkap: `CLAUDE.md` · gaya visual: `.claude/skills/mumeyong-video/STYLE.md`.

## Satu command: `claude-video` (dari folder mana pun)

```bash
claude-video                              # daftar semua video + tahapnya
claude-video "Judul video baru"           # bikin video baru dari judul (folder & slug otomatis)
claude-video <video>                      # satu putaran review (Claude bilang kapan)
claude-video <video> final                # render final → hasil/<video>/
```

`claude-video <video>` otomatis ngerjain yang perlu aja, berurutan, lalu nge-print file apa yang dikirim ke Claude:

1. **naskah** — generate ulang `NASKAH.md` kalau `SCRIPT.md` berubah
2. **suara + timing** — ada rekamanmu (`audio/voice.wav`)? → **align otomatis**. Belum ada? → **suara TTS otomatis**
   (Ardi; butuh internet). Dibikin ulang cuma kalau naskah berubah. Offline → timing estimasi tanpa suara.
3. **check** — cek struktur; kalau gagal dia berhenti
4. **cover** — `out/cover.png` (cover TikTok yang didesain)
5. **sheet** — satu thumbnail per kalimat
6. **stills** — frame penuh untuk baris di file `REVIEW` (diisi Claude tiap putaran)
7. **preview** — 540×960 30fps + suara + musik otomatis

`claude-video <video> final` = sama, tapi render final → `hasil/<video>/` (mp4 + cover.png; POST.md udah ada).

## Mulai video baru (contoh: EP02) — langkah demi langkah

**Versi singkat:** `cd` ke repo → `claude` → "kerjain EP02 seri Bongkar Arsitektur" → jawab pertanyaan →
"ok" tiap gerbang → `claude-video <video>` → rekam → `claude-video <video> final`.

**1. Buka Claude di folder repo** (wajib di sini — biar `CLAUDE.md`, skill, glossary, dan memory ke-load otomatis)
```bash
cd ~/aschente/claude-video
claude
```

**2. Bilang satu kalimat** — mis. *"kerjain EP02 seri Bongkar Arsitektur"* atau *"kerjain ide #03"*.
(Opsional: bikin foldernya dulu pakai `claude-video "Bongkar EP02 Big Data Migration"`.)
Mau cepat? Bilang *"kerjain ide #06 format quick"* → 60–75 s, satu hero object, tetap unik (aturan anti-slop di `ideas/STRATEGY.md`).

**3. Jawab brief** — Claude cuma nanya yang kurang: nama samaran klien, angka asli, apa yang sebenarnya terjadi.
💡 Siapin 1–2 fakta/angka asli atau screenshot yang disamarkan — itu yang paling bikin videonya unik.

**4. Autopilot** — Claude jalan terus tanpa nanya "ok" tiap tahap (naskah → identitas → storyboard → kode),
lalu berhenti dengan satu ringkasan + perintah render. Mau koreksi? Bilang aja kapan pun, Claude revisi:

| Tahap | Kamu dapat | Kamu ngapain |
|---|---|---|
| Naskah | `SCRIPT.md` + 2–3 opsi hook + `NASKAH.md` | cek fakta, ganti hook kalau mau |
| Identitas | `IDENTITY.md` — metafora, gerakan, warna, hook baru (beda dari video sebelumnya) | "ok" |
| Storyboard | `TREATMENT.md` — komposisi beda tiap bab | "ok" |
| Kode | `scenes.py` + komponen baru + `REVIEW` terisi | tunggu aja |

**5. Putaran review (± 3×)** — `claude-video <video>` → kirim sheet/stills/preview + catatan per baris → Claude
revisi → jalanin lagi.

**6. Rekam suara** — baca `NASKAH.md`, simpan `videos/<video>/audio/voice.wav` (musik dibikin otomatis) →
jalanin `claude-video <video>` lagi (align otomatis).

**7. Final** — `claude-video <video> final` → bilang "final ok" → Claude bikin `POST.md` (caption + hashtag) dan
update `hasil/`, `ideas/`, registry → upload ke TikTok → kirim link ke Claude → bilang "commit" kalau mau disimpan
ke git.

## Alur kerja

```
 KAMU                                     CLAUDE
 ────                                     ──────
 1. claude-video "Judul"           ──►    (atau langsung bilang "bikin video tentang X")
    "kerjain video <video>"               tanya yang kurang: takeaway, durasi, CTA

 2. pilih hook, bilang "ok"        ◄──    SCRIPT.md (2–3 opsi hook + naskah)
                                          + NASKAH.md (versi bersih buat dibaca)

 2b. bilang "ok"                   ◄──    IDENTITY.md: metafora, gerakan khas, warna, format hook,
                                          struktur, komponen baru — beda dari video sebelumnya

 3. bilang "ok"                    ◄──    TREATMENT.md: komposisi tiap bab + storyboard per kalimat
                                          → tulis scenes.py → check → isi REVIEW

 4. claude-video <video>           ──►    kirim sheet / stills / preview + catatan
    (± 3 putaran)                  ◄──    revisi → "jalanin claude-video <video> lagi"

 5. baca NASKAH.md, rekam voice.wav
    claude-video <video>           ──►    align otomatis → kirim hasil skor
                                   ◄──    benerin baris yang ditandai, tweak timing

 6. claude-video <video> final     ──►    "final ok"
                                   ◄──    POST.md (caption + hashtag), update hasil/ & ideas/

 7. upload TikTok, kirim link      ──►    catat link + performa → bahan ide berikutnya
 8. bilang "commit"                ──►    Claude commit (cuma kalau kamu minta)
```

Tiap langkah ada **gerbang**: Claude berhenti dan nunggu "ok" dari kamu sebelum lanjut.

## Isi repo

```
claude-video/
├── START.md         ← kamu di sini
├── ideas/           backlog ide (README.md) + REGISTRY.md (identitas tiap video, biar nggak ngulang)
├── videos/<video>/  satu folder per video (lihat di bawah)
├── hasil/           video final: <video>.mp4 + cover.png + POST.md (README.md = daftar tayang)
├── engine/          mesin animasinya (Claude yang urus)
└── vid              script di balik `claude-video`
```

## Isi folder video

```
videos/<video>/
├── SCRIPT.md        naskah, 1 kalimat per [Lxx], per ## BAB (sumber utama — yang diubah cuma ini)
├── NASKAH.md        versi baca dari SCRIPT.md, buat rekam (auto-generate, jangan diedit)
├── IDENTITY.md      identitas unik video ini (metafora, gerakan khas, warna, hook, struktur)
├── TREATMENT.md     storyboard: komposisi tiap bab + visual per kalimat
├── REVIEW           baris yang dicek sebagai still putaran ini (diisi Claude)
├── timing.json      waktu tiap kalimat & kata (estimasi → align dari suaramu)
├── scenes.py        kode animasinya
├── audio/           voice.wav (kamu) · music.mp3 opsional (kalau kosong → musik digenerate)
├── assets/          screenshot / gambar PNG yang mau dipakai
└── out/             hasil render sementara (nggak di-commit)
```

## Ide video

Daftar di `ideas/README.md`. Status: 💡 ide → ⭐ dipilih → 🎬 produksi → ✅ tayang (🗑 batal).

- **Nambah ide:** bilang ke Claude "simpan ide: …"
- **Mulai:** "kerjain ide #04" → Claude bikin folder videonya dan mulai dari naskah
- **Setelah tayang:** kirim link + views → dicatat, buat bahan ide berikutnya

## Biar tiap video unik

Yang **selalu sama** (biar orang langsung kenal "ini Mumeyong"): HUD, font, biru aksen, rasa geraknya, outro.
Yang **beda tiap video** (dicatat di `IDENTITY.md`, dicek ke `ideas/REGISTRY.md`): metafora, gerakan khas,
warna khas, format hook, struktur, dan minimal satu komponen visual baru. Plus sentuhan manusia: artefak asli
(screenshot/angka yang disamarkan), opinimu, satu kejutan. **Bantu Claude dengan satu angka/screenshot asli
tiap video** — itu yang paling bikin nggak generik.

## Rekam suara

- Ruangan sepi, mic/HP ± 20 cm dari mulut, simpan sebagai `videos/<video>/audio/voice.wav` (48 kHz).
- Buka **NASKAH.md** (di HP / layar kedua), baca seluruhnya **sekali jalan**, santai, ± 160 kata/menit.
- **Tebal** = kasih tekanan · *(napas)* = ambil napas · ⏸ = jeda ± 1 detik ganti bab.
- Salah ngomong? Diam sebentar, **ulangi kalimat itu**. Aligner otomatis ambil take terakhir yang bagus.
- Mau ganti kata-kata? Bilang ke Claude → SCRIPT.md diubah → NASKAH.md ikut ke-generate. Jangan edit NASKAH.md langsung.
- Nggak perlu nunggu suara buat mulai: visual bisa dibangun & direview pakai timing estimasi dulu.

### Suara sintetis (otomatis kalau belum ada rekaman)
```bash
claude-video <video>                      # belum ada voice.wav → suara Ardi dibikin otomatis
claude-video tts <video>                  # cuma bikin suaranya aja
```
- Pakai **edge-tts** (suara neural Microsoft, gratis, **butuh internet — teks naskah dikirim ke Microsoft**).
- Satu suara aja: **Ardi**, tempo santai. Nggak ada opsi yang perlu diatur.
- Timing per kata langsung dari TTS → nggak perlu aligner. Tanda *tekanan* nggak kebaca, napas `//` = jeda lebih panjang.
- Istilah English dibaca pakai ejaan Indonesia (`serverless` → "serverles"). Ada yang salah ucap? Tambahin di
  `audio/tts_lexicon.txt`: `airflow = erflo` (satu per baris).
- **Rekaman asli selalu menang:** begitu ada `audio/voice.wav`, itu yang dipakai (align otomatis).
- Tayang pakai suara sintetis? Nyalain label **"AI-generated content"** di TikTok/YouTube — dan jujur ke penonton.

## Musik

- **Kamu cukup rekam suara.** Kalau `audio/music.*` kosong, musik **digenerate otomatis** waktu render
  (`engine/audio/music.py`): disusun dari bab-bab videonya sendiri — intro ringan, tiap bab groove penuh dengan pola
  arp sendiri, recap gelap tanpa drum, outro resolve. Pergantian bab jatuh pas di beat, ada riser + impact.
- Tiap video punya karakter sendiri (key + mood: warm · tense · bright · dreamy), diatur di IDENTITY.md /
  `v.music = dict(key="D", mood="warm")`. `claude-video check <video>` nampilin rencana musiknya.
- Dengerin musiknya aja: `claude-video music <video>` → `out/music_gen.wav`.
- Mau pakai lagu sendiri? Taruh royalty-free ± 128 BPM di `audio/music.mp3` — itu yang dipakai.
- Otomatis turun (ducking) waktu kamu ngomong, naik lagi di jeda antar bab.

## Hasil final

> **Yang di-upload selalu `hasil/<video>/<video>.mp4`** (1080×1920 60fps). `out/preview.mp4` cuma 540p buat review.

`claude-video <video> final` nyalin hasil ke `hasil/<video>/`:
`<video>.mp4` (1080×1920 60fps) dan `cover.png` (cover TikTok yang didesain). `POST.md` (caption, deskripsi buat
search, hashtag, komentar pin, checklist upload) udah ditulis Claude dari waktu produksi — tinggal copy-paste.
Cover juga muncul tiap putaran review di `out/cover.png` (atau `claude-video cover <video>`).
File mp4 **nggak masuk git** — backup sendiri (mis. Google Drive).

## Kasih feedback yang spesifik

- ✅ "L14: angkanya kegedean, headline ganti jadi *Cek sendiri.*"
- ✅ "00:00:42 — kameranya kecepetan zoom-nya"
- ✅ "Bab UKURAN masih kerasa kayak template"
- ❌ "kurang bagus" → Claude bakal nanya baris mana

## Command lain (jarang perlu)

| Kapan | Command |
|---|---|
| Preview satu bagian aja | `claude-video <video> --from 20 --to 45` |
| Buka folder video | `claude-video open <video>` |
| Dengerin semua SFX | `claude-video sfx` |
| Command satuan (still, sheet, preview, align, mix, …) | `claude-video help` |

## Setup di komputer baru

```bash
git clone git@github.com:mumeyong/claude-video.git ~/aschente/claude-video
cd ~/aschente/claude-video
python3 -m venv --system-site-packages .venv && .venv/bin/pip install faster-whisper edge-tts
ln -s ~/aschente/claude-video/vid ~/.local/bin/claude-video   # ~/.local/bin harus ada di PATH
```
Butuh: Python 3.13, ffmpeg, Pango + PyGObject (`gir1.2-pango-1.0`, `python3-gi`, `python3-cairo`).
Font sudah ikut di repo (`assets/fonts/`).

## Kalau error

Copy-paste output-nya ke Claude, plus command yang kamu jalanin.
