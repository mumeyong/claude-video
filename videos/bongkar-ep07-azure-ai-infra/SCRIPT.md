# Bongkar Arsitektur EP07 — Fondasi buat training AI di Azure (episode terakhir)

> Seri Bongkar Arsitektur · target 75–90 s · klien disamarkan · Azure
> Fakta dari portfolio/CV (Azure AI Infrastructure): fondasi cloud architecture buat AI model training & inference di
> Azure — AKS + GPU compute; compute allocation yang scalable & high-performance; cross-cloud compatibility.
> TIDAK ada angka (jumlah GPU, ukuran model, biaya) — jangan ditambahin.
> Pembagian training pool (GPU, di-scale turun setelah selesai) vs inference pool (selalu siap) + "semuanya di container
> → bisa pindah cloud" = cara umum fondasi kayak gini dibangun; minta user konfirmasi cocok dengan yang dia kerjakan.
> Tech terms tetap English (GLOSSARY.md). Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — pilih satu (A sudah terpasang):
> A · Mitos dicoret:  "Mau bikin AI, harus beli GPU segudang, nyala terus? Nggak juga."
> B · Pertanyaan:     "GPU itu mahal. Jadi kapan dia harus nyala, dan kapan harus mati?"
> C · Analogi:        "Atlet juara nggak latihan dua puluh empat jam."

## INTRO
[L01] Mau bikin AI, harus beli GPU *segudang*, nyala terus?
[L02] *Nggak* juga. //
[L03] GPU itu mahal. Yang penting bukan banyaknya, tapi *kapan* dipakainya.
[L04] Project terakhir: fondasi buat training dan inference AI, di *Azure*.

## 00 · MASALAH
[L05] Bayangin model AI itu *atlet* bulu tangkis.
[L06] Masa *latihan*: pukulan yang sama, diulang ribuan kali, pakai lapangan dan alat paling berat.
[L07] Itu *training*: berat, tapi cuma sementara.
[L08] Pas *tanding*: satu pukulan, harus cepat, kapan aja lawan datang.
[L09] Itu *inference*. Kalau dua-duanya rebutan lapangan yang sama, dua-duanya *kalah*. //

## 01 · KEPUTUSAN
[L10] Jadi keputusannya: lapangannya *dipisah*.
[L11] Lapangan latihan pakai *GPU*, lampunya nyala pas ada jadwal latihan aja.
[L12] Lapangan tanding lebih kecil, tapi *selalu siap*.
[L13] Dan ada pelatih yang ngatur jadwalnya. Itu *Kubernetes*, AKS. //

## 02 · DIAGRAM
[L14] Data latihan masuk ke *GPU node pool*.
[L15] Selesai training, GPU-nya di-scale *turun* lagi.
[L16] Model yang udah jadi, di-deploy ke *inference* pool.
[L17] Semuanya di container. Jadi bisa dibawa ke cloud *lain*.

## 03 · HASIL
[L18] Hasilnya: compute-nya *scalable*. Nambah pas butuh, turun pas selesai.
[L19] GPU nggak *idle*, nungguin jadwal.
[L20] Dan fondasinya nggak *terkunci* di satu cloud.

## RECAP
[L21] Jadi, infrastruktur AI itu bukan soal punya GPU *paling banyak*.
[L22] Tapi soal tahu kapan *latihan*, dan kapan tanding.
[L23] Atlet juara nggak latihan dua puluh empat jam. Dia latihan *pas perlu*.

## OUTRO
[L24] Itu tujuh episode *Bongkar Arsitektur*. Mau lanjutan? Tulis di komentar.
[L25] Follow, biar nggak ketinggalan.
