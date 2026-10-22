# Kenapa video YouTube langsung main, padahal servernya jauh?

- **Status:** 🎬 produksi — [`videos/youtube-langsung-main/`](../videos/youtube-langsung-main/)
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** youtube-langsung-main
- **Seri:** —
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Video yang lagi rame udah "dititipin" di server dekat kotamu — kadang malah di gedung ISP-mu sendiri.

## Hook (opsi)
- A: tap video, langsung main — "Video ini nggak datang dari Amerika. Dia udah nunggu di dekat rumahmu."
- B: "Kenapa video viral lancar, tapi video lama kadang buffering?"

## Bab
1. Kalau semua dari satu server pusat: jauh + macet
2. CDN: salinan di dekat penonton (edge / cache di ISP)
3. Video viral = udah ada di rak dekat; video lama = harus diambil dari gudang
4. Sudut infra: ini juga yang aku pasang buat app klien

## Bukti / visual
Metafora: **warung titip stok** — pabrik di Jawa Barat, tapi Indomie udah ada di warung depan gang. Signature: truk dari gudang pusat cuma datang sekali, warung-warung ngelayanin ribuan pembeli.

## Butuh komponen baru?
- `warung_cache` (warung + rak stok) · `supply_truck`

## Catatan
- ⚠️ cek fakta Google Global Cache / Netflix Open Connect di ISP Indonesia sebelum disebut.
- Mulai: `souffle 28` atau `souffle "Kenapa video YouTube langsung main, padahal servernya jauh?"`
