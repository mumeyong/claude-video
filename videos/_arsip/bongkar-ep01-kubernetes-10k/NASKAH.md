# NASKAH — Bongkar Arsitektur EP01 — Kubernetes yang nahan 10.000 request barengan

> 26 kalimat · 179 kata · ± 1:06 kalau dibaca ± 160 kata/menit
> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.
> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.
> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.

## INTRO

<sub>L01</sub> Tiap hari, pas peak hour.  ·  *(napas)*  

<sub>L02</sub> Lebih dari **sepuluh ribu** request masuk, **barengan**.  

<sub>L03</sub> Ke satu aplikasi layanan keuangan.  

<sub>L04</sub> Dulu, di jam segini, app-nya **lemot**, terus **down**.  


*⏸ jeda ± 1 detik*

## 00 · MASALAH

<sub>L05</sub> Bayangin gerbang tol, waktu mudik.  

<sub>L06</sub> Mobilnya ribuan, tapi gardunya **segitu-segitu aja**.  

<sub>L07</sub> Antrean numpuk, ada yang nyerah, putar balik.  

<sub>L08</sub> Di aplikasi, itu artinya transaksi **gagal**.  


*⏸ jeda ± 1 detik*

## 01 · KEPUTUSAN

<sub>L09</sub> Solusinya bukan bikin gardu sebanyak-banyaknya.  

<sub>L10</sub> Itu mahal, dan malam-malam **idle**.  

<sub>L11</sub> Solusinya: gardu yang bisa **nambah sendiri**.  

<sub>L12</sub> Aplikasinya jalan di container, di atas Kubernetes, di Alibaba Cloud.  ·  *(napas)*  

<sub>L13</sub> Kubernetes ini kayak **petugas tol**-nya.  


*⏸ jeda ± 1 detik*

## 02 · DIAGRAM

<sub>L14</sub> Request masuk lewat load balancer, dibagi rata.  

<sub>L15</sub> Begitu traffic naik, auto-scaling **nambah pod** baru, otomatis.  

<sub>L16</sub> Kalau node-nya penuh, node baru juga ikut **ditambah**.  

<sub>L17</sub> Satu pod crash? Langsung **diganti**, traffic-nya dialihin.  


*⏸ jeda ± 1 detik*

## 03 · HASIL

<sub>L18</sub> Sekarang, peak hour lewat **tanpa down**.  

<sub>L19</sub> Lebih dari sepuluh ribu request barengan, **aman**.  

<sub>L20</sub> Dan jam dua pagi, pod-nya **scale down** sendiri, satu-satu.  

<sub>L21</sub> Jadi bayarnya cuma **pas rame**.  


*⏸ jeda ± 1 detik*

## RECAP

<sub>L22</sub> Jadi, jangan siapin server buat hari paling rame.  

<sub>L23</sub> Siapin sistem yang bisa **scale up** dan **scale down** sendiri.  

<sub>L24</sub> Buat beban kayak gini, Kubernetes bukan **gaya-gayaan**. Emang **butuh**.  


*⏸ jeda ± 1 detik*

## OUTRO

<sub>L25</sub> Episode depan: big data migration ke cloud, dengan **zero data loss**.  

<sub>L26</sub> Follow, biar nggak ketinggalan.  

---

Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)
