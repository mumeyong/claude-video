# NASKAH — Bongkar Arsitektur EP03 — Ganti stack big data jadi serverless

> 24 kalimat · 198 kata · ± 1:13 kalau dibaca ± 160 kata/menit
> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.
> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.
> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.

## INTRO

<sub>L01</sub> Dulu: node big data yang harus **dijagain**, tiap hari.  

<sub>L02</sub> Sekarang: nggak ada server yang perlu diurus. **Sama sekali**.  ·  *(napas)*  

<sub>L03</sub> Datanya sama, job-nya sama. Yang beda: **siapa yang ngurus mesinnya**.  

<sub>L04</sub> Project ini: stack big data legacy, diganti jadi **serverless**.  


*⏸ jeda ± 1 detik*

## 00 · MASALAH

<sub>L05</sub> Bayangin punya **dapur sendiri**.  

<sub>L06</sub> Kompornya harus dirawat, gasnya harus dibeli, **walau nggak ada pesanan**.  

<sub>L07</sub> Itu node legacy: nyala terus, **idle** pun tetap dibayar.  

<sub>L08</sub> Pas pesanan **membludak**? Dapurnya kewalahan, dan nambah kompor itu **nggak cepat**.  


*⏸ jeda ± 1 detik*

## 01 · KEPUTUSAN

<sub>L09</sub> Jadi keputusannya: **lepas dapurnya**.  

<sub>L10</sub> Pindah ke **cloud kitchen**: kompornya nyala pas ada pesanan, mati pas sepi.  

<sub>L11</sub> Itu intinya **serverless**: kamu urus resepnya, bukan mesinnya.  ·  *(napas)*  

<sub>L12</sub> Node legacy-nya **pensiun**.  


*⏸ jeda ± 1 detik*

## 02 · DIAGRAM

<sub>L13</sub> Data yang masuk detik itu juga, itu **streaming**, dimasak **Flink**.  

<sub>L14</sub> Data gede yang diolah sekaligus, itu **batch**, masuk **MaxCompute**.  

<sub>L15</sub> Dua-duanya ambil bahan dari tempat yang sama: tabel **Paimon** di data lake.  

<sub>L16</sub> Dan yang ngatur urutan masaknya? **Airflow**, otomatis, sesuai jadwal.  


*⏸ jeda ± 1 detik*

## 03 · HASIL

<sub>L17</sub> Hasilnya: data processing jadi **lebih cepat**.  

<sub>L18</sub> Nggak ada node yang perlu di-patch, di-restart, atau dijagain **tengah malam**.  

<sub>L19</sub> Pipeline-nya jalan **sendiri**, dari data masuk sampai siap dipakai.  


*⏸ jeda ± 1 detik*

## RECAP

<sub>L20</sub> Jadi, serverless itu bukan soal **nggak ada server**.  

<sub>L21</sub> Server-nya tetap ada. Cuma, **bukan kamu** yang ngurus.  

<sub>L22</sub> Waktu kamu balik ke yang penting: **datanya**.  


*⏸ jeda ± 1 detik*

## OUTRO

<sub>L23</sub> Episode depan: **monolith** lama, dipecah jadi **event-driven**.  

<sub>L24</sub> Follow, biar nggak ketinggalan.  

---

Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)
