# Kenapa app bank down pas tanggal gajian?

> Ide #06 · pilar B (broad) · format QUICK · target 65–75 s (≈ 180 kata) · lihat ideas/STRATEGY.md
> Satu hero object yang berubah tiap bab: **papan tersangka** → **kasir tanggal muda + satu buku kas** → buku kas + fotokopiannya.
> Satu hal yang cuma Mumeyong bisa bilang: angka asli dari CV (10.000 request barengan) + opini
> "auto-scaling nggak nolong kalau database-nya cuma satu pintu".
> Fakta dijaga umum: TIDAK sebut nama bank. Tech terms English (GLOSSARY.md).
> Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — A/B/C (A terpasang):
> A · Cold open di tengah kejadian: "Tanggal dua puluh lima, jam sembilan lewat satu. Gaji udah masuk, app bank-mu muter terus."
> B · Detektif: "Ada tiga tersangka. Cuma satu yang salah."
> C · Angka dulu: "Jutaan orang buka app yang sama, di menit yang sama."
> (Hook "pertanyaan spesifik" dipakai video sebelumnya → A diubah jadi cold open, B jadi kalimat ketiga.)

## INTRO
[L01] Tanggal dua puluh lima, jam sembilan lewat satu.
[L02] Gaji udah masuk, kamu buka app bank, dan dia *muter terus*. //
[L03] Ada tiga tersangka. Cuma *satu* pelakunya.

## 00 · TERSANGKA
[L04] Tersangka pertama: server-nya *kurang*.
[L05] Setengah benar. Server-nya disiapin buat hari biasa, bukan buat *tanggal muda*. //
[L06] Tersangka kedua: app-nya *jelek*.
[L07] Bukan. App-nya sama persis tiap hari. Yang beda cuma *traffic*-nya. //

## 01 · PELAKU
[L08] Bayangin kasir supermarket pas tanggal muda.
[L09] Kasirnya bisa ditambah jadi dua puluh. Itu *auto-scaling*.
[L10] Tapi semua transaksi harus dicatat di *satu* buku kas yang sama.
[L11] Itu *database*-nya. Semua antre di satu pintu. //
[L12] Dan tanggal dua puluh lima, gaji ribuan kantor juga masuk ke buku yang *sama*.

## 02 · OBATNYA
[L13] Sistem yang tahan biasanya misahin dua hal: *baca* sama tulis.
[L14] Yang cuma mau cek saldo, baca dari *read replica*. Fotokopian buku kasnya. //
[L15] Buku aslinya cuma buat yang *nulis*: transfer, bayar, gaji masuk.

## RECAP
[L16] Aku pernah nahan *sepuluh ribu* request barengan.
[L17] Auto-scaling nggak nolong, kalau database-nya cuma *satu pintu*.

## OUTRO
[L18] Video berikutnya: gimana sepuluh ribu request itu tetap *jalan*.
[L19] Follow, biar nggak ketinggalan.
