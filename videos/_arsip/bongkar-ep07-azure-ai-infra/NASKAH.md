# NASKAH — Bongkar Arsitektur EP07 — Fondasi buat training AI di Azure (episode terakhir)

> 25 kalimat · 204 kata · ± 1:16 kalau dibaca ± 160 kata/menit
> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.
> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.
> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.

## INTRO

<sub>L01</sub> Mau bikin AI, harus beli GPU **segudang**, nyala terus?  

<sub>L02</sub> **Nggak** juga.  ·  *(napas)*  

<sub>L03</sub> GPU itu mahal. Yang penting bukan banyaknya, tapi **kapan** dipakainya.  

<sub>L04</sub> Project terakhir: fondasi buat training dan inference AI, di **Azure**.  


*⏸ jeda ± 1 detik*

## 00 · MASALAH

<sub>L05</sub> Bayangin model AI itu **atlet** bulu tangkis.  

<sub>L06</sub> Masa **latihan**: pukulan yang sama, diulang ribuan kali, pakai lapangan dan alat paling berat.  

<sub>L07</sub> Itu **training**: berat, tapi cuma sementara.  

<sub>L08</sub> Pas **tanding**: satu pukulan, harus cepat, kapan aja lawan datang.  

<sub>L09</sub> Itu **inference**. Kalau dua-duanya rebutan lapangan yang sama, dua-duanya **kalah**.  ·  *(napas)*  


*⏸ jeda ± 1 detik*

## 01 · KEPUTUSAN

<sub>L10</sub> Jadi keputusannya: lapangannya **dipisah**.  

<sub>L11</sub> Lapangan latihan pakai **GPU**, lampunya nyala pas ada jadwal latihan aja.  

<sub>L12</sub> Lapangan tanding lebih kecil, tapi **selalu siap**.  

<sub>L13</sub> Dan ada pelatih yang ngatur jadwalnya. Itu **Kubernetes**, AKS.  ·  *(napas)*  


*⏸ jeda ± 1 detik*

## 02 · DIAGRAM

<sub>L14</sub> Data latihan masuk ke **GPU node pool**.  

<sub>L15</sub> Selesai training, GPU-nya di-scale **turun** lagi.  

<sub>L16</sub> Model yang udah jadi, di-deploy ke **inference** pool.  

<sub>L17</sub> Semuanya di container. Jadi bisa dibawa ke cloud **lain**.  


*⏸ jeda ± 1 detik*

## 03 · HASIL

<sub>L18</sub> Hasilnya: compute-nya **scalable**. Nambah pas butuh, turun pas selesai.  

<sub>L19</sub> GPU nggak **idle**, nungguin jadwal.  

<sub>L20</sub> Dan fondasinya nggak **terkunci** di satu cloud.  


*⏸ jeda ± 1 detik*

## RECAP

<sub>L21</sub> Jadi, infrastruktur AI itu bukan soal punya GPU **paling banyak**.  

<sub>L22</sub> Tapi soal tahu kapan **latihan**, dan kapan tanding.  

<sub>L23</sub> Atlet juara nggak latihan dua puluh empat jam. Dia latihan **pas perlu**.  


*⏸ jeda ± 1 detik*

## OUTRO

<sub>L24</sub> Itu tujuh episode **Bongkar Arsitektur**. Mau lanjutan? Tulis di komentar.  

<sub>L25</sub> Follow, biar nggak ketinggalan.  

---

Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)
