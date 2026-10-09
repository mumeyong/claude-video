# Kenapa war tiket konser selalu crash?

- **Status:** ✅ tayang — [`videos/_arsip/war-tiket-crash`](../videos/_arsip/war-tiket-crash/) · **Pilar:** B (broad) · **Format:** QUICK
- **Slug:** war-tiket-crash
- **Seri:** —
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-06

## Takeaway (1 kalimat)
Jam 10:00:00 itu bukan "banyak orang" — itu semua orang di detik yang sama; solusinya ngatur antrean, bukan nambah server doang.

## Hook (opsi)
- A: (cold open) countdown `09:59:57… 58… 59…` → `10:00:00` → layar putih "503". Baru narasi masuk.
- B: "Satu kursi. Lima puluh ribu jari. Satu detik."

## Bab — struktur **timeline per detik**
1. `10:00:00` — semua klik barengan (spike vertikal, bukan naik pelan)
2. `10:00:01` — server penuh, yang kalah dapet error, terus **refresh** → traffic dobel
3. `10:00:10` — kenapa refresh bikin makin parah (retry storm)
4. Solusinya: **virtual waiting room** — kamu dapet nomor antrean, server cuma nerima segini per detik
5. Twist: antrean yang jujur itu kerasa lambat, tapi **nggak ada yang crash**

## Identitas (draft)
| # | Pilihan | Untuk video ini |
|---|---|---|
| 1 | Metafora | **mesin nomor antrean di bank/kantor pos** — ambil karcis, tunggu dipanggil |
| 2 | Signature move | **karcis nomor keluar dari mesin** dan digit display "SEKARANG MELAYANI" bergulir |
| 3 | Warna | hijau `#10A060` (lampu "dipanggil") |
| 4 | Hook | cold open hitung mundur |
| 5 | Struktur | timeline per detik (timecode besar di tiap bab) |
| 6 | Komponen baru | `queue_dispenser` · `big_clock` (HH:MM:SS dengan detik loncat) · `refresh_storm` (ikon ↻ beranak) |

Sentuhan manusia: opini "tombol refresh itu musuh terbesar server-mu sendiri"; kejutan: angka antrean kamu ternyata
29.481 → tapi maju cepat.

## Catatan
- Jangan sebut promotor/platform tiket tertentu.
- Istilah tetap English: retry, traffic, rate limit, virtual waiting room, error 503.
