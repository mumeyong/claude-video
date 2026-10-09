# Bongkar Arsitektur EP06 — Project 360: satu nasabah, satu layar

> Seri Bongkar Arsitektur · target 75–90 s · klien disamarkan ("grup konglomerasi", tanpa nama)
> Fakta dari portfolio/CV (Project 360): data nasabah dipusatkan di environment container yang high-performance &
> highly available — Docker di atas ECS; data retrieval real-time & aman lewat WAF, VPN, dan IDaaS.
> TIDAK ada angka (latency, jumlah nasabah/perusahaan) — jangan ditambahin. "Milidetik" sengaja nggak dipakai.
> Adegan CS (buka aplikasi satu-satu, ditanya ulang) + contoh produk (tabungan · asuransi · kredit · sekuritas) +
> peran tiap lapis keamanan = ilustrasi umum; minta user konfirmasi cocok dengan yang dia kerjakan.
> Tech terms tetap English (GLOSSARY.md). Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — pilih satu (A sudah terpasang):
> A · Cold open:       "Nasabah udah duduk di depan CS. CS-nya buka aplikasi, satu-satu."
> B · Pertanyaan:      "Kenapa CS selalu nanya ulang data kamu, padahal kamu udah nasabah lama?"
> C · Before/after:    "Dulu: keliling loket, fotokopi satu-satu. Sekarang: satu map, satu layar."

## INTRO
[L01] Nasabah udah duduk di depan CS. CS-nya buka aplikasi, *satu-satu*.
[L02] Data tabungan di sini, asuransi di sana, kredit di tempat lain. //
[L03] Nasabahnya nunggu. Terus ditanya ulang data yang *sama*.
[L04] Namanya: Project 360. Satu nasabah, *satu layar*.

## 00 · MASALAH
[L05] Di grup konglomerasi, satu orang bisa jadi nasabah di *banyak* perusahaan.
[L06] Datanya kesebar, kayak berkas di *loket* yang beda-beda.
[L07] Mau lihat gambaran utuh? Harus keliling, *fotokopi* satu-satu.
[L08] Lama. Dan tiap fotokopi, itu satu celah buat data *bocor*. //

## 01 · KEPUTUSAN
[L09] Jadi keputusannya: kumpulin jadi *satu map*.
[L10] Satu tempat, semua data nasabah *nyambung*.
[L11] CS tinggal buka satu map, datanya ditarik *real-time*.
[L12] Tapi isi map ini sensitif. Jadi penjagaannya *berlapis*. //

## 02 · DIAGRAM
[L13] Aplikasinya jalan di container *Docker*, di atas *ECS*.
[L14] Server-nya lebih dari satu. Satu down, yang lain tetap *ngelayanin*.
[L15] Lapis pertama: *WAF*, nyaring request jahat sebelum masuk.
[L16] Lapis kedua: *VPN*, cuma jaringan kantor yang bisa nyambung.
[L17] Lapis ketiga: *IDaaS*, tiap pegawai login pakai akunnya sendiri.

## 03 · HASIL
[L18] Hasilnya: CS lihat gambaran utuh nasabah, di *satu layar*.
[L19] Datanya ditarik *real-time*, nggak nunggu fotokopi.
[L20] Dan tetap *aman*: tiga lapis, sebelum satu lembar pun kebuka.

## RECAP
[L21] Jadi, Project 360 bukan soal ngumpulin data *sebanyak-banyaknya*.
[L22] Tapi soal nasabah nggak perlu cerita *dua kali*.
[L23] Dan makin lengkap datanya, makin *tebal* juga penjaganya.

## OUTRO
[L24] Episode terakhir: fondasi buat training *AI* di Azure.
[L25] Follow, biar nggak ketinggalan.
