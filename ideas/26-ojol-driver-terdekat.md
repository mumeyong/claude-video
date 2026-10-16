# Gimana ojol nemuin driver terdekat dalam 3 detik?

- **Status:** 🎬 produksi — [`videos/ojol-driver-terdekat/`](../videos/ojol-driver-terdekat/)
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** ojol-driver-terdekat
- **Seri:** —
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
App nggak ngecek semua driver se-kota — peta dibagi kotak-kotak kecil, dan cuma kotak di sekitarmu yang dicari dulu.

## Hook (opsi)
- A: titik kamu + ribuan titik motor — "Ada 20.000 driver di kota ini. App-nya cuma lihat 12."
- B: "Kenapa driver yang lebih jauh kadang yang dapat order-mu?"

## Bab
1. Peta dibagi grid (geohash / H3)
2. Cari dari kotakmu, melebar kalau kosong
3. Bukan cuma jarak: arah jalan, rating, rute, driver lagi selesai order
4. Kenapa tarif naik pas hujan (supply vs demand) — singkat

## Bukti / visual
Metafora: **cari teman di stadion lewat nomor tribun** — nggak teriak ke semua orang, langsung ke sektor. Signature: grid nyala sektor demi sektor melebar dari titikmu.

## Butuh komponen baru?
- `geo_grid` (kotak heksagon melebar) · `motor_dot` (titik driver + arah)

## Catatan
- Jelasin konsep umum, jangan klaim cara kerja internal Gojek/Grab.
- Mulai: `claude-video 26` atau `claude-video "Gimana ojol nemuin driver terdekat dalam 3 detik?"`
