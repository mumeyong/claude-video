# Google Maps tahu jalan macet dari mana? — format QUICK

> Dibuat 2026-10-16 · Pilar: B (broad) · target 60–70 s · ide: [ideas/27-maps-tahu-macet.md](../../ideas/27-maps-tahu-macet.md)
> Satu hero object: titik-titik HP di jalan — jalan berubah warna di belakang mereka. Yang cuma Mumeyong bilang:
> garis merah itu bukan satelit, itu kita yang kejebak bareng.
> Anti-slop: tanpa "Di era digital", "Tahukah kamu", "Yuk simak". Tech terms English (GLOSSARY.md).
> Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> Sumber: Simon Weckert, "Google Maps Hacks" (Berlin, Februari 2020 — 99 HP di gerobak) · Google Maps blog
> "Google Maps 101: How AI helps predict traffic and determine routes" (2020 — data lokasi anonim yang dikumpulin +
> pola lalu lintas historis).
>
> HOOK — A/B (B terpasang):
> A · jalan merah di Maps — "Yang ngelaporin macet ini? Kamu. Dan semua orang di sebelahmu."
> B · 99 HP di gerobak → jalan kosong jadi merah.

## INTRO
[L01] Tahun dua ribu dua puluh, ada orang di Berlin narik *sembilan puluh sembilan* HP pakai gerobak.
[L02] Jalannya kosong, // tapi di Google Maps, jalan itu langsung *merah*.
[L03] Soalnya Maps nggak ngelihat jalan. // Dia ngelihat *HP* kita.

## 00 · SENSOR
[L04] Tiap HP yang location-nya nyala, ikut ngirim posisinya ke Google.
[L05] Dari posisi ke posisi, kelihatan seberapa *cepat* dia gerak.
[L06] Tanpa nama — // buat Maps, kamu cuma satu *titik*.

## 01 · MERAH
[L07] Satu titik berhenti? // Bisa aja dia lagi beli *cilok*.
[L08] Tapi kalau banyak titik di jalan yang sama *barengan* melambat,
[L09] kecepatannya dirata-rata, // dan jalannya jadi *merah*.

## 02 · PREDIKSI
[L10] Terus tebakan "sampai jam berapa"? // Itu dari *masa lalu*.
[L11] Maps inget jalan ini biasanya kayak gimana, di jam yang sama, minggu-minggu sebelumnya,
[L12] terus dicampur kondisi *sekarang*.

## 03 · CELAH
[L13] Makanya di jalan yang sepi, tebakannya suka meleset: // datanya *tipis*.
[L14] Dan sembilan puluh sembilan HP yang jalan pelan? // Buat Maps, itu *macet*.

## RECAP
[L15] Jadi garis merah itu bukan satelit yang ngintip dari atas. // Itu kita, yang lagi kejebak *bareng*.

## OUTRO
[L16] Kamu pernah disuruh Maps lewat gang aneh? // Cerita di komentar.
[L17] Follow, biar nggak ketinggalan.
