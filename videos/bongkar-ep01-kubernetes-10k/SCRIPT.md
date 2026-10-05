# Bongkar Arsitektur EP01 — Kubernetes yang nahan 10.000 request barengan

> Seri Bongkar Arsitektur · target 70–90 s · layanan keuangan (disamarkan) · Alibaba Cloud (ACK)
> Fakta: 10.000+ request barengan (portfolio) · peak tiap hari · dulu lemot lalu down · pakai auto-scaling.
> Tech terms tetap English (GLOSSARY.md).
> Jumlah node/pod TIDAK disebut (nggak ada angka asli) — visual cuma nunjukin "nambah", tanpa angka.
> Read-aloud marks: *kata* = tekanan, ' //' = napas. Bumper "BONGKAR ARSITEKTUR · EP 01" = visual di jeda INTRO → 00.
>
> HOOK — pilih satu (A sudah terpasang):
> A · Cold open:   "Tiap hari, pas peak hour. Lebih dari sepuluh ribu request masuk, barengan."
> B · Relatable:   "Pernah mau transfer, terus aplikasinya muter-muter doang? Di belakang layar, ini yang terjadi."
> C · Mitos:       "Aplikasi lemot? Tambahin server aja. ... Bukan itu jawabannya."

## INTRO
[L01] Tiap hari, pas peak hour. //
[L02] Lebih dari *sepuluh ribu* request masuk, *barengan*.
[L03] Ke satu aplikasi layanan keuangan.
[L04] Dulu, di jam segini, app-nya *lemot*, terus *down*.

## 00 · MASALAH
[L05] Bayangin gerbang tol, waktu mudik.
[L06] Mobilnya ribuan, tapi gardunya *segitu-segitu aja*.
[L07] Antrean numpuk, ada yang nyerah, putar balik.
[L08] Di aplikasi, itu artinya transaksi *gagal*.

## 01 · KEPUTUSAN
[L09] Solusinya bukan bikin gardu sebanyak-banyaknya.
[L10] Itu mahal, dan malam-malam *idle*.
[L11] Solusinya: gardu yang bisa *nambah sendiri*.
[L12] Aplikasinya jalan di container, di atas Kubernetes, di Alibaba Cloud. //
[L13] Kubernetes ini kayak *petugas tol*-nya.

## 02 · DIAGRAM
[L14] Request masuk lewat load balancer, dibagi rata.
[L15] Begitu traffic naik, auto-scaling *nambah pod* baru, otomatis.
[L16] Kalau node-nya penuh, node baru juga ikut *ditambah*.
[L17] Satu pod crash? Langsung *diganti*, traffic-nya dialihin.

## 03 · HASIL
[L18] Sekarang, peak hour lewat *tanpa down*.
[L19] Lebih dari sepuluh ribu request barengan, *aman*.
[L20] Dan jam dua pagi, pod-nya *scale down* sendiri, satu-satu.
[L21] Jadi bayarnya cuma *pas rame*.

## RECAP
[L22] Jadi, jangan siapin server buat hari paling rame.
[L23] Siapin sistem yang bisa *scale up* dan *scale down* sendiri.
[L24] Buat beban kayak gini, Kubernetes bukan *gaya-gayaan*. Emang *butuh*.

## OUTRO
[L25] Episode depan: big data migration ke cloud, dengan *zero data loss*.
[L26] Follow, biar nggak ketinggalan.
