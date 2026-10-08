# NASKAH — Bongkar Arsitektur EP06 — Project 360: satu nasabah, satu layar

> 25 kalimat · 206 kata · ± 1:16 kalau dibaca ± 160 kata/menit
> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.
> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.
> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.

## INTRO

<sub>L01</sub> Nasabah udah duduk di depan CS. CS-nya buka aplikasi, **satu-satu**.  

<sub>L02</sub> Data tabungan di sini, asuransi di sana, kredit di tempat lain.  ·  *(napas)*  

<sub>L03</sub> Nasabahnya nunggu. Terus ditanya ulang data yang **sama**.  

<sub>L04</sub> Namanya: Project 360. Satu nasabah, **satu layar**.  


*⏸ jeda ± 1 detik*

## 00 · MASALAH

<sub>L05</sub> Di grup konglomerasi, satu orang bisa jadi nasabah di **banyak** perusahaan.  

<sub>L06</sub> Datanya kesebar, kayak berkas di **loket** yang beda-beda.  

<sub>L07</sub> Mau lihat gambaran utuh? Harus keliling, **fotokopi** satu-satu.  

<sub>L08</sub> Lama. Dan tiap fotokopi, itu satu celah buat data **bocor**.  ·  *(napas)*  


*⏸ jeda ± 1 detik*

## 01 · KEPUTUSAN

<sub>L09</sub> Jadi keputusannya: kumpulin jadi **satu map**.  

<sub>L10</sub> Satu tempat, semua data nasabah **nyambung**.  

<sub>L11</sub> CS tinggal buka satu map, datanya ditarik **real-time**.  

<sub>L12</sub> Tapi isi map ini sensitif. Jadi penjagaannya **berlapis**.  ·  *(napas)*  


*⏸ jeda ± 1 detik*

## 02 · DIAGRAM

<sub>L13</sub> Aplikasinya jalan di container **Docker**, di atas **ECS**.  

<sub>L14</sub> Server-nya lebih dari satu. Satu down, yang lain tetap **ngelayanin**.  

<sub>L15</sub> Lapis pertama: **WAF**, nyaring request jahat sebelum masuk.  

<sub>L16</sub> Lapis kedua: **VPN**, cuma jaringan kantor yang bisa nyambung.  

<sub>L17</sub> Lapis ketiga: **IDaaS**, tiap pegawai login pakai akunnya sendiri.  


*⏸ jeda ± 1 detik*

## 03 · HASIL

<sub>L18</sub> Hasilnya: CS lihat gambaran utuh nasabah, di **satu layar**.  

<sub>L19</sub> Datanya ditarik **real-time**, nggak nunggu fotokopi.  

<sub>L20</sub> Dan tetap **aman**: tiga lapis, sebelum satu lembar pun kebuka.  


*⏸ jeda ± 1 detik*

## RECAP

<sub>L21</sub> Jadi, Project 360 bukan soal ngumpulin data **sebanyak-banyaknya**.  

<sub>L22</sub> Tapi soal nasabah nggak perlu cerita **dua kali**.  

<sub>L23</sub> Dan makin lengkap datanya, makin **tebal** juga penjaganya.  


*⏸ jeda ± 1 detik*

## OUTRO

<sub>L24</sub> Episode terakhir: fondasi buat training **AI** di Azure.  

<sub>L25</sub> Follow, biar nggak ketinggalan.  

---

Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)
