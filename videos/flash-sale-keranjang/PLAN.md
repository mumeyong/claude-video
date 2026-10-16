# PLAN — Barang flash sale "habis" padahal udah di keranjang. Kok bisa?

<!-- registry
pilar: B
metafora: rak minimarket, sisa satu barang — keranjang = cuma nunjuk, checkout = tangan yang nyamber duluan; label stok kuning = papan skor (SISA 1 → HABIS → SISA -1 → HABIS → SISA 1 → PUNYAMU); race condition = dua kepalan narik satu barang jadi dua; lock = bingkai, yang lain nunggu di luar; ruang tunggu = antrean titik ke gerbang server; pesanan nggak dibayar → barang terbang balik ke rak
signature: tangan-tangan masuk frame nunjuk satu barang, satu kepalan nyamber, label stok di rak flip · look lit
look: lit
color: raspberry `#E0285A`
hook: layar HP checkout yang semua orang kenal — 11.59.57 → 12.00.00, Bayar, "Stok habis"
struktur: HP (hook) → barang terbang dari keranjang ke rak → nunjuk vs nyamber → replay race condition → replay lock → ruang tunggu + barang balik → recap gelap (tanganmu menang) + 2 hal disiapin
komponen: minimarket (rak, filler, produk, empty_spot, label_stok, tangan)
musik: garage D tense 132 · sfx glass
durasi: 84
-->

## Idenya
Semua orang pernah lihat layar itu: jam 12.00.00, tombol Bayar ditekan, lalu "Stok habis". Video mulai di layar HP
itu, terus barang di keranjang terbang keluar ke rak minimarket — sisa satu barang. Keranjang = jarimu nunjuk;
ribuan jari lain nunjuk barang yang sama; yang dapat itu kepalan yang nyamber duluan (checkout). Dua replay di
detik yang sama nunjukin race condition (satu barang ketarik jadi dua, label SISA -1) dan lock (bingkai, satu
masuk, sisanya nunggu). Label stok kuning di rak jadi papan skor sepanjang video. Di recap, tanganmu yang biru
akhirnya menang — label jadi PUNYAMU. Penonton pulang dengan satu kalimat: keranjang itu cuma "aku mau".
