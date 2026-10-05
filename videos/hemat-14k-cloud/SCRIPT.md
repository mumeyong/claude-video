# Gimana aku hemat $14.000/bulan biaya cloud

> Target 90–120 s · audiens: TikTok umum (bahasa awam, satu "bukti" teknis per bab) · Alibaba Cloud
> Tech terms tetap English (GLOSSARY.md).
> Read-aloud marks: *kata* = tekanan, ' //' = napas. Fakta yang dipakai: $14k/bulan (portfolio). Contoh di
> tiap bab = pola umum ("biasanya"), bukan klaim soal klien tertentu.
>
> HOOK — pilih satu (A sudah terpasang di INTRO di bawah):
> A · Angka dulu:   "Empat belas ribu dolar. Segitu tagihan cloud yang aku potong, tiap bulan."
> B · Pertanyaan:   "Bayar cloud itu emang semahal itu? Biasanya bukan mahal. Tapi bocor."
> C · Analogi:      "Bayangin bayar listrik rumah kosong, tiap bulan. Banyak perusahaan gitu, sama cloud-nya."

## INTRO
[L01] *Empat belas ribu dolar*. //
[L02] Segitu tagihan cloud yang aku potong, *tiap bulan*.
[L03] Kalau dirupiahin, lebih dari *dua ratus juta*.
[L04] Dan biasanya, masalahnya bukan cloud-nya yang mahal, tapi *bocor*.
[L05] Ini empat langkah yang aku pakai, di Alibaba Cloud.

## 00 · BOCOR
[L06] Langkah pertama, *cari yang bocor* dulu.
[L07] Server yang running, tapi *idle*, nggak ada yang pakai.
[L08] Disk yang *unattached*, nggak nempel ke mana-mana.
[L09] Snapshot lama, numpuk bertahun-tahun.
[L10] Terus server development, ngapain nyala *jam dua pagi*?
[L11] Pasang *auto-shutdown* di luar jam kerja. *Beres*.

## 01 · RIGHT-SIZING
[L12] Langkah kedua, *right-sizing*.
[L13] Sering banget, CPU-nya kepakai cuma *sepuluh persen*.
[L14] Tapi yang dibayar, *seratus persen*.
[L15] Kayak sewa bus, buat nganter satu orang. //
[L16] Monitor dulu beberapa minggu, terus *downsize*.

## 02 · RESERVED & SPOT
[L17] Langkah ketiga, jangan semuanya *on-demand*.
[L18] Yang nyala terus, pakai *reserved instance*, jauh lebih murah.
[L19] Yang boleh mati sewaktu-waktu, pakai *spot instance*.
[L20] Server sama, kerjaan sama, harganya *beda jauh*.

## 03 · ARSITEKTUR
[L21] Langkah terakhir, yang paling berat: *ubah arsitekturnya*.
[L22] Monolith lama yang nyala dua puluh empat jam, dipecah.
[L23] Bagian yang jarang dipakai, pindah ke *serverless*.
[L24] Jadi bayarnya *pay-per-use*, cuma pas dipakai.
[L25] Paling lama dikerjain, tapi efeknya paling panjang.

## RECAP
[L26] Jadi, empat langkahnya. //
[L27] Cari yang bocor, right-sizing, reserved dan spot, ubah arsitektur.
[L28] Hasilnya, *empat belas ribu dolar*, tiap bulan.
[L29] Dan ingat, hemat itu bukan berarti bikin sistemnya *lemot*.

## OUTRO
[L30] Mau dicek, biaya cloud-mu bocor di mana?
[L31] Mampir ke *mumeyong dot dev*.
[L32] Follow, buat bongkar arsitektur cloud lainnya.
