# Restart router beneran ngefek?

- **Status:** 🎬 produksi — [`videos/wifi-ep04-restart-router/`](../videos/wifi-ep04-restart-router/)
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** wifi-ep04-restart-router
- **Seri:** #14 Bongkar WiFi Rumah — EP 04
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Restart kadang beneran nyembuhin (memori penuh, tabel koneksi kepenuhan, IP baru) — tapi kalau masalahnya di kabel atau di ISP, restart cuma bikin kamu nunggu 3 menit.

## Hook (opsi)
- A: kutipan: "disuruh restart tapi percuma" — "Kadang percuma. Kadang ajaib. Ini bedanya."
- B: jam pasir 3 menit modem nyala ulang — "3 menit ini sebenernya ngapain?"

## Bab
1. Kenapa restart bisa nolong: memori bocor, tabel koneksi (NAT) penuh, minta IP baru
2. Kapan percuma: LOS merah (EP01), gangguan di ISP (EP02), kabel basah (EP03)
3. Pengakuan orang infra: di production pun restart sering jadi "obat" — dan itu tanda ada yang belum ketahuan
4. Teaser EP05: jam 8 malam

## Bukti / visual
Metafora: **buku tamu satpam yang penuh** — tiap koneksi dicatat, halaman habis, tamu baru ditolak; restart = buku baru. Signature: halaman buku tamu terisi cepat → disobek → halaman bersih.

## Butuh komponen baru?
- `guestbook` (buku tamu, baris keisi) · `boot_timer` (urutan lampu modem nyala ulang)

## Catatan
- Sudut "cuma Mumeyong": cerita restart server production yang nutupin bug asli (disamarkan).
- Mulai: `souffle 22` atau `souffle "Restart router beneran ngefek?"`
