# NASKAH — Bongkar Arsitektur EP02 — Pindahin big data ke cloud, tanpa satu byte hilang

> 24 kalimat · 196 kata · ± 1:13 kalau dibaca ± 160 kata/menit
> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.
> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.
> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.

## INTRO

<sub>L01</sub> Migrasi data ke cloud? Copy, paste, **beres**?  

<sub>L02</sub> **Nggak** segampang itu.  ·  *(napas)*  

<sub>L03</sub> Satu record aja hilang, laporan bisa salah, dan **nggak ada yang sadar**.  

<sub>L04</sub> Project ini: legacy infra ke Alibaba Cloud, dengan **zero data loss**.  


*⏸ jeda ± 1 detik*

## 00 · MASALAH

<sub>L05</sub> Bayangin mindahin satu **perpustakaan**, waktu masih **buka**.  

<sub>L06</sub> Bukunya jutaan, dan orang masih **pinjam dan balikin** tiap hari.  

<sub>L07</sub> Di dunia data, itu artinya data terus **berubah**, selama migrasi jalan.  

<sub>L08</sub> Kalau cuma di-copy sekali, perubahan di tengah jalan **ketinggalan**.  


*⏸ jeda ± 1 detik*

## 01 · KEPUTUSAN

<sub>L09</sub> Jadi migrasinya dipecah jadi **dua tahap**.  

<sub>L10</sub> Pertama, **full copy**: semua data lama dipindah sekaligus.  

<sub>L11</sub> Kedua, **incremental sync**: perubahan baru ikut dikirim, terus-terusan.  ·  *(napas)*  

<sub>L12</sub> Perpustakaan lama **tetap buka**, sampai yang baru bener-bener siap.  


*⏸ jeda ± 1 detik*

## 02 · DIAGRAM

<sub>L13</sub> Data di legacy disalin ke Alibaba Cloud.  

<sub>L14</sub> Tiap perubahan baru, ikut nyusul lewat **sync**.  

<sub>L15</sub> Terus tiap tabel **dicek**: jumlah row dan **checksum**-nya harus sama persis.  

<sub>L16</sub> Beda satu karakter aja? Ketahuan, dan **di-sync ulang**.  


*⏸ jeda ± 1 detik*

## 03 · HASIL

<sub>L17</sub> Begitu semua **match**, baru **cutover**: aplikasinya pindah ke cloud.  

<sub>L18</sub> Jalan balik ke sistem lama tetap disiapin. Namanya **rollback plan**.  

<sub>L19</sub> Hasilnya: pindah ke cloud, **zero data loss**.  


*⏸ jeda ± 1 detik*

## RECAP

<sub>L20</sub> Jadi, migrasi itu bukan soal **copy**.  

<sub>L21</sub> Tapi soal **bukti**: tiap data dicek, sebelum yang lama dimatiin.  

<sub>L22</sub> Kalau belum bisa dibuktiin sama, **belum boleh pindah**.  


*⏸ jeda ± 1 detik*

## OUTRO

<sub>L23</sub> Episode depan: stack big data yang dibikin **serverless**.  

<sub>L24</sub> Follow, biar nggak ketinggalan.  

---

Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)
