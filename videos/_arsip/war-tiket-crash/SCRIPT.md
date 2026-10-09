# Kenapa war tiket konser selalu crash?

> Ide #07 · pilar B (broad) · format QUICK · target 65–75 s (≈ 185 kata) · lihat ideas/STRATEGY.md
> Satu hero object yang berubah tiap bab: **jam besar 10:00:00** yang detiknya loncat → loket server → mesin nomor antrean.
> Satu hal yang cuma Mumeyong bisa bilang: opini "tombol refresh itu musuh terbesar server-nya sendiri".
> Fakta dijaga umum: TIDAK sebut promotor / platform tiket. Angka = ilustrasi, bukan data event tertentu.
> Tech terms English (GLOSSARY.md). Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — A/B/C (A terpasang):
> A · Angka dulu: "Ribuan kursi. Ratusan ribu jari. Satu detik."
> B · Cold open hitung mundur 09:59:57 → 10:00:00 → layar putih "503".
> C · Opini: "Tombol refresh itu musuh terbesar server-nya sendiri."
> (Video sebelumnya pakai cold open → B nggak dipakai; A dipasang.)

## INTRO
[L01] Ribuan kursi. Ratusan ribu jari. *Satu* detik.
[L02] Jam sepuluh tepat, kamu pencet beli, dan yang keluar cuma *error*. //
[L03] Ini yang kejadian, detik per *detik*.

## 00 · 10:00:00
[L04] Jam sepuluh tepat, semua orang klik di detik yang *sama*.
[L05] Grafik traffic-nya bukan naik pelan. Dia *tegak lurus*. //

## 01 · 10:00:01
[L06] Server-nya penuh. Yang kalah rebutan dapet *error*.
[L07] Terus kamu ngapain? *Refresh*.
[L08] Ratusan ribu orang refresh barengan. Traffic-nya jadi *dobel*. //

## 02 · 10:00:10
[L09] Ini namanya *retry storm*. Server belum sempat napas, udah diserbu lagi.
[L10] Nambah server doang nggak cukup. Badainya ikut *gede*. //

## 03 · ANTREAN
[L11] Yang nggak crash pakai *virtual waiting room*.
[L12] Kamu dapet nomor antrean, kayak ambil karcis di *kantor pos*.
[L13] Server cuma nerima segini per detik. Itu *rate limit*. Sisanya nunggu, bukan nembak.
[L14] Nomormu dua puluh sembilan ribu. Kedengeran jauh, tapi majunya *cepet*. //

## RECAP
[L15] Tombol refresh itu musuh terbesar server-nya *sendiri*.
[L16] Antrean yang jujur emang kerasa lambat. Tapi *nggak ada* yang crash.

## OUTRO
[L17] Video berikutnya: roadmap jadi cloud engineer, dari nol.
[L18] Follow, biar nggak ketinggalan.
