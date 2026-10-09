# Bongkar Arsitektur EP03 — Ganti stack big data jadi serverless

> Seri Bongkar Arsitektur · target 75–90 s · klien disamarkan ("stack big data legacy", tanpa industri) · Alibaba Cloud
> Fakta dari portfolio/CV: legacy processing nodes diganti serverless stack — Flink, MaxCompute, Paimon — dengan
> workflow otomatis Airflow; data lake management lebih ringkas; data processing lebih cepat. TIDAK ada angka
> (berapa node, berapa persen lebih cepat) — jangan ditambahin tanpa angka asli.
> Pembagian peran (Flink = streaming, MaxCompute = batch, Paimon = tabel data lake bersama, Airflow = jadwal/urutan)
> = cara umum stack ini dipakai; minta user konfirmasi cocok dengan yang dia kerjakan.
> Tech terms tetap English (GLOSSARY.md). Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — pilih satu (A sudah terpasang):
> A · Before/after:   "Dulu: node big data yang harus dijagain tiap hari. Sekarang: nggak ada server yang perlu diurus."
> B · Pertanyaan:     "Kenapa bayar dapur yang kompornya nyala dua puluh empat jam, kalau masaknya cuma pas ada pesanan?"
> C · Klaim nyeleneh: "Server terbaik buat big data? Yang nggak usah kamu urus."

## INTRO
[L01] Dulu: node big data yang harus *dijagain*, tiap hari.
[L02] Sekarang: nggak ada server yang perlu diurus. *Sama sekali*. //
[L03] Datanya sama, job-nya sama. Yang beda: *siapa yang ngurus mesinnya*.
[L04] Project ini: stack big data legacy, diganti jadi *serverless*.

## 00 · MASALAH
[L05] Bayangin punya *dapur sendiri*.
[L06] Kompornya harus dirawat, gasnya harus dibeli, *walau nggak ada pesanan*.
[L07] Itu node legacy: nyala terus, *idle* pun tetap dibayar.
[L08] Pas pesanan *membludak*? Dapurnya kewalahan, dan nambah kompor itu *nggak cepat*.

## 01 · KEPUTUSAN
[L09] Jadi keputusannya: *lepas dapurnya*.
[L10] Pindah ke *cloud kitchen*: kompornya nyala pas ada pesanan, mati pas sepi.
[L11] Itu intinya *serverless*: kamu urus resepnya, bukan mesinnya. //
[L12] Node legacy-nya *pensiun*.

## 02 · DIAGRAM
[L13] Data yang masuk detik itu juga, itu *streaming*, dimasak *Flink*.
[L14] Data gede yang diolah sekaligus, itu *batch*, masuk *MaxCompute*.
[L15] Dua-duanya ambil bahan dari tempat yang sama: tabel *Paimon* di data lake.
[L16] Dan yang ngatur urutan masaknya? *Airflow*, otomatis, sesuai jadwal.

## 03 · HASIL
[L17] Hasilnya: data processing jadi *lebih cepat*.
[L18] Nggak ada node yang perlu di-patch, di-restart, atau dijagain *tengah malam*.
[L19] Pipeline-nya jalan *sendiri*, dari data masuk sampai siap dipakai.

## RECAP
[L20] Jadi, serverless itu bukan soal *nggak ada server*.
[L21] Server-nya tetap ada. Cuma, *bukan kamu* yang ngurus.
[L22] Waktu kamu balik ke yang penting: *datanya*.

## OUTRO
[L23] Episode depan: *monolith* lama, dipecah jadi *event-driven*.
[L24] Follow, biar nggak ketinggalan.
