# Bongkar Arsitektur EP02 — Pindahin big data ke cloud, tanpa satu byte hilang

> Seri Bongkar Arsitektur · target 70–90 s · klien disamarkan ("infra legacy", tanpa industri) · Alibaba Cloud
> Fakta dari portfolio: legacy infra → Alibaba Cloud, zero data loss. TIDAK ada angka (ukuran data, durasi) —
> jangan ditambahin tanpa angka asli. Metode (full copy → incremental sync → verifikasi → cutover + rollback plan)
> = praktik standar; minta user konfirmasi cocok dengan yang dia kerjakan.
> Tech terms tetap English (GLOSSARY.md). Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — pilih satu (A sudah terpasang):
> A · Mitos dicoret: "Migrasi data ke cloud? Copy, paste, beres? Nggak segampang itu."
> B · Taruhan:       "Satu record hilang waktu migrasi. Nggak ada yang sadar... sampai laporannya salah."
> C · Analogi:       "Bayangin mindahin satu perpustakaan, waktu perpustakaannya masih buka."

## INTRO
[L01] Migrasi data ke cloud? Copy, paste, *beres*?
[L02] *Nggak* segampang itu. //
[L03] Satu record aja hilang, laporan bisa salah, dan *nggak ada yang sadar*.
[L04] Project ini: legacy infra ke Alibaba Cloud, dengan *zero data loss*.

## 00 · MASALAH
[L05] Bayangin mindahin satu *perpustakaan*, waktu masih *buka*.
[L06] Bukunya jutaan, dan orang masih *pinjam dan balikin* tiap hari.
[L07] Di dunia data, itu artinya data terus *berubah*, selama migrasi jalan.
[L08] Kalau cuma di-copy sekali, perubahan di tengah jalan *ketinggalan*.

## 01 · KEPUTUSAN
[L09] Jadi migrasinya dipecah jadi *dua tahap*.
[L10] Pertama, *full copy*: semua data lama dipindah sekaligus.
[L11] Kedua, *incremental sync*: perubahan baru ikut dikirim, terus-terusan. //
[L12] Perpustakaan lama *tetap buka*, sampai yang baru bener-bener siap.

## 02 · DIAGRAM
[L13] Data di legacy disalin ke Alibaba Cloud.
[L14] Tiap perubahan baru, ikut nyusul lewat *sync*.
[L15] Terus tiap tabel *dicek*: jumlah row dan *checksum*-nya harus sama persis.
[L16] Beda satu karakter aja? Ketahuan, dan *di-sync ulang*.

## 03 · HASIL
[L17] Begitu semua *match*, baru *cutover*: aplikasinya pindah ke cloud.
[L18] Jalan balik ke sistem lama tetap disiapin. Namanya *rollback plan*.
[L19] Hasilnya: pindah ke cloud, *zero data loss*.

## RECAP
[L20] Jadi, migrasi itu bukan soal *copy*.
[L21] Tapi soal *bukti*: tiap data dicek, sebelum yang lama dimatiin.
[L22] Kalau belum bisa dibuktiin sama, *belum boleh pindah*.

## OUTRO
[L23] Episode depan: stack big data yang dibikin *serverless*.
[L24] Follow, biar nggak ketinggalan.
