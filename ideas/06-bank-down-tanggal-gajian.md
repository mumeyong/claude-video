# Kenapa app bank down pas tanggal gajian?

- **Status:** ✅ tayang — [`videos/kenapa-bank-down-gajian`](../videos/kenapa-bank-down-gajian/) · **Pilar:** B (broad) · **Format:** QUICK
- **Slug:** kenapa-bank-down-gajian
- **Seri:** —
- **Durasi target:** 60–70 s
- **Ditambahkan:** 2026-10-06

## Takeaway (1 kalimat)
Bukan servernya "lemah" — traffic tanggal 25 itu bentuknya beda, dan sistem yang nggak di-design buat lonjakan bakal tumbang.

## Hook (opsi)
- A: (pertanyaan spesifik) "Tanggal dua puluh lima, jam sembilan pagi. Kenapa app bank-mu *selalu* lemot pas ini?"
- B: (detektif) "Ada tiga tersangka. Cuma satu yang salah."

## Bab — struktur **detektif: 3 tersangka → pelakunya**
1. Tersangka 1: "servernya kurang" → setengah benar (kapasitas fixed)
2. Tersangka 2: "app-nya jelek" → bukan, app-nya sama tiap hari
3. Tersangka 3: database yang jadi satu pintu (bottleneck) → **pelaku utama**
4. Gimana bank yang nggak down ngatasinnya: auto-scaling, queue, cache, read replica (pilih 2, jangan semua)

## Identitas (draft)
| # | Pilihan | Untuk video ini |
|---|---|---|
| 1 | Metafora | **antrean kasir supermarket tanggal muda** — semua orang belanja di hari yang sama |
| 2 | Signature move | **kalender sobek**: lembar tanggal disobek cepat sampai "25" → kerumunan langsung muncul |
| 3 | Warna | merah `#F03B4F` |
| 4 | Hook | pertanyaan yang spesifik banget (tanggal + jam) |
| 5 | Struktur | detektif: 3 tersangka, papan bukti, satu dicap PELAKU |
| 6 | Komponen baru | `tear_calendar` · `suspect_board` (kartu tersangka + benang merah) |

Sentuhan manusia: opini "auto-scaling nggak nolong kalau database-nya cuma satu pintu"; pengalaman nahan 10.000
request barengan (EP01) jadi bukti — link ke EP01 di pinned comment.

## Catatan
- **Jangan sebut nama bank.** Generik "app bank". Fakta harus umum & benar.
- Anti-slop: hero = kalender + papan tersangka, bukan server biru.
