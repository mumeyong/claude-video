# POST — <judul>

- **File:** `<slug>.mp4` · **cover:** `cover.png` (didesain: `v.cover` di scenes.py)
- **Durasi:** — · **Final:** YYYY-MM-DD · **Pilar:** B / C / D
- **Suara:** rekaman asli / sintetis (TTS) — kalau sintetis: nyalain label AI di semua platform
- **Tayang:** TikTok — · YouTube Shorts — · Instagram — · Facebook —

<!-- Aturan nulis (Claude):
  · Judul = hook rasa penasaran, bukan judul video mentah; ≤ 60 karakter biar nggak kepotong di feed Shorts (maks 100).
    Kata kunci yang orang ketik di search ada di judul (mis. "WiFi", "biaya cloud", "ChatGPT").
  · Baris pertama tiap caption = yang kelihatan tanpa "lainnya" (TikTok ± 150, Instagram ± 125 karakter).
  · Deskripsi = 2–3 kalimat bahasa ngomong + kata kunci search, bukan daftar keyword.
  · Hashtag 3–5 (Instagram maks 5): 1 topik besar + 1–2 spesifik + 1 komunitas. Tech terms tetap English.
  · Tanpa klise (STYLE §8b): "Di era digital", "Tahukah kamu", "Yuk simak", "wajib tahu", emoji berderet. -->

## Judul (dipakai di semua platform)
<≤ 60 karakter>

## TikTok — tempel satu blok ini
```
<judul>
<1–2 kalimat deskripsi + kata kunci search>
#… #… #…
```

## YouTube Shorts
**Title** (≤ 100, ideal ≤ 60):
```
<judul>
```
**Description** (2 baris pertama kelihatan; 3 hashtag pertama muncul di atas judul):
```
<1–2 kalimat: apa yang penonton dapet>
<1 kalimat konteks / pengalaman Mumeyong>

#… #… #…
```
**Tags** (Studio → Show more → Tags, dipisah koma):
```
<kata kunci 1>, <kata kunci 2>, … (8–12, campur Indonesia + istilah English)
```

## Meta — Instagram Reels + Facebook Reels (blok yang sama)
```
<judul>

<2–3 kalimat deskripsi, baris pertama paling kuat>

#… #… #…
```
**Alt text** (Instagram → Advanced settings → Accessibility; dibaca search):
```
<1 kalimat: apa yang kelihatan di video>
```

## Komentar pertama (pin — semua platform)
…

## Checklist upload
- [ ] File: `hasil/<slug>/<slug>.mp4` (1080×1920 60fps) — **bukan** `out/preview.mp4` (540p)
- [ ] Cover: `cover.png` — TikTok Studio → Edit cover → Upload · YouTube Shorts: pilih frame di app YouTube (kalau ada opsi upload gambar, pakai cover.png) · Instagram → Edit cover → Add from camera roll
- [ ] Judul + deskripsi + hashtag per platform (blok di atas)
- [ ] Label AI kalau suaranya TTS (TikTok "AI-generated content" · YouTube "Altered or synthetic content" · Instagram "Add AI label")
- [ ] Pin komentar pertama
- [ ] Facebook: share dari Instagram ("Also share to Facebook") atau upload ulang dengan blok Meta
- [ ] LinkedIn (opsional): judul + deskripsi Meta, tanpa hashtag berlebih
- [ ] Setelah upload: pindahin `hasil/<slug>` → `hasil/_tayang/` dan `videos/<slug>` → `videos/_arsip/`

## Setelah tayang
| | TikTok | YT Shorts | Instagram | Facebook |
|---|---|---|---|---|
| Views 24 jam / 7 hari | | | | |
| Tahan 3 dtk / completion | | | | |
| Share · save · follow | | | | |
- Komentar menarik (bahan video berikutnya → ideas/):
