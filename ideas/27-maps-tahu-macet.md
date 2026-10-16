# Google Maps tahu jalan macet dari mana?

- **Status:** 🎬 produksi — [`videos/maps-tahu-macet/`](../videos/maps-tahu-macet/)
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** maps-tahu-macet
- **Seri:** —
- **Durasi target:** 60–70 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Garis merah di Maps itu dari HP orang-orang di jalan yang sama — kecepatan mereka dirata-rata jadi warna.

## Hook (opsi)
- A: jalan merah di Maps — "Yang ngelaporin macet ini? Kamu. Dan semua orang di sebelahmu."
- B: "Ada orang yang narik 99 HP pakai gerobak — dan Maps percaya jalannya macet." (kejadian Berlin 2020)

## Bab
1. Tiap HP = sensor kecepatan anonim
2. Banyak titik lambat → merah; dirata-rata, bukan satu orang
3. Prediksi: data minggu lalu jam yang sama
4. Batasnya: jalan sepi, data sedikit, bisa dikelabui (99 HP)

## Bukti / visual
Metafora: **barisan semut** — tiap semut nggak tahu macet, tapi dilihat dari atas kelihatan. Signature: titik-titik HP melambat, jalan berubah warna di belakang mereka.

## Butuh komponen baru?
- `road_speed` (jalan yang warnanya ngikutin titik) · `phone_dot`

## Catatan
- ⚠️ cek fakta sumber publik (blog Google, eksperimen Simon Weckert 2020).
- Mulai: `claude-video 27` atau `claude-video "Google Maps tahu jalan macet dari mana?"`
