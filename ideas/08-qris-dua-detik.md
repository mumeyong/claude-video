# QRIS: apa yang terjadi dalam 2 detik setelah kamu scan?

- **Status:** ✅ tayang — [`videos/_arsip/qris-dua-detik`](../videos/_arsip/qris-dua-detik/) · **Pilar:** B (broad) · **Format:** QUICK
- **Slug:** qris-dua-detik
- **Seri:** —
- **Durasi target:** 60–70 s
- **Ditambahkan:** 2026-10-06

## Takeaway (1 kalimat)
Satu "beep" QRIS itu estafet beberapa sistem yang saling oper data — dan semuanya harus selesai sebelum kamu sempat kedip.

## Hook (opsi)
- A: (freeze-frame) "Tahan. Dua detik ini, uangmu lewat beberapa sistem." → layar beku di momen scan.
- B: "Kamu bayar es teh lima ribu. Di belakangnya, ada estafet."

## Bab — struktur **slow-motion replay** (jam detik diperlambat)
1. `0,0 s` scan — app-mu baca kode
2. `0,3 s` app → bank / e-wallet kamu (issuer): saldo cukup?
3. `0,8 s` lewat **switching** ke pihak merchant (acquirer)
4. `1,5 s` merchant dapet notifikasi
5. `2,0 s` beep — balik ke kecepatan normal

## Identitas (draft)
| # | Pilihan | Untuk video ini |
|---|---|---|
| 1 | Metafora | **lari estafet** — tongkat = transaksi |
| 2 | Signature move | **freeze-frame + slow-mo**: waktu melambat (timecode `0,3 s` jalan lambat), tongkat dioper |
| 3 | Warna | oranye `#E8861A` |
| 4 | Hook | freeze-frame ("Tahan.") |
| 5 | Struktur | replay slow-motion per milidetik |
| 6 | Komponen baru | `relay_track` (lintasan + pelari-node + tongkat) · `slowmo_clock` |

## Catatan
- ⚠️ **Fakta wajib dicek** sebelum naskah: urutan issuer → switching → acquirer, dan angka detiknya cuma ilustrasi
  (bilang "kira-kira" di naskah, atau pakai urutan tanpa angka).
- Jangan sebut nama bank/switching.
