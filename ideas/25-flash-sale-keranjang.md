# Barang flash sale "habis" padahal udah di keranjang. Kok bisa?

- **Status:** 💡 ide
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** flash-sale-keranjang
- **Seri:** —
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Keranjang itu cuma catatan "aku mau" — stok baru jadi milikmu waktu bayar, dan ribuan orang lagi rebutan detik yang sama.

## Hook (opsi)
- A: notif "Stok habis" pas jari udah di tombol bayar — "Barangnya nggak pernah jadi milikmu."
- B: jam 12.12.00 — "Satu barang. 40.000 jari."

## Bab
1. Keranjang ≠ beli: stok nggak dikunci di keranjang
2. Detik checkout: siapa duluan ngunci stok (race condition, oversell)
3. Kenapa app sengaja bikin antrean / ruang tunggu
4. Tips: bayar pakai metode yang paling cepat, jangan buka 3 tab

## Bukti / visual
Metafora: **rak minimarket barang terakhir** — banyak tangan nyamber satu barang, yang sampai kasir duluan yang dapat. Signature: tangan-tangan masuk frame, barang pindah ke satu kantong, label rak jadi 0.

## Butuh komponen baru?
- `shelf_stock` (rak + label stok) · `grab_hands` (tangan berebut, seeded)

## Catatan
- Bedain dari war-tiket-crash (itu soal server crash, ini soal stok). Hero & warna beda.
- Mulai: `claude-video 25` atau `claude-video "Barang flash sale "habis" padahal udah di keranjang. Kok bisa?"`
