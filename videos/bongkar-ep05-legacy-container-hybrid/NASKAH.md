# NASKAH — Bongkar Arsitektur EP05 — Legacy dan container, hidup berdampingan

> 27 kalimat · 210 kata · ± 1:18 kalau dibaca ± 160 kata/menit
> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.
> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.
> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.

## INTRO

<sub>L01</sub> Gimana caranya aplikasi lama dan Kubernetes baru jalan **barengan**?  

<sub>L02</sub> Tanpa user sadar, mereka lagi dilayani yang **mana**.  ·  *(napas)*  

<sub>L03</sub> Yang lama belum bisa dimatiin. Yang baru udah **jalan**.  

<sub>L04</sub> Project ini: legacy dan container, hidup **berdampingan**.  


*⏸ jeda ± 1 detik*

## 00 · MASALAH

<sub>L05</sub> Bayangin satu lahan **kuliner**.  

<sub>L06</sub> Di kiri, **ruko lama**: udah lama buka, pelanggannya setia.  

<sub>L07</sub> Di kanan, deretan **kios kontainer**: gampang ditambah, gampang dipindah.  

<sub>L08</sub> Masalahnya: pintu masuknya **beda-beda**.  

<sub>L09</sub> Satu pintu kebanjiran, yang lain sepi. Aplikasinya ikut **goyang**.  ·  *(napas)*  


*⏸ jeda ± 1 detik*

## 01 · KEPUTUSAN

<sub>L10</sub> Jadi keputusannya: **satu pintu depan**.  

<sub>L11</sub> Di situ ada satpam yang bagi rata pengunjung. Itu **load balancer**, SLB.  

<sub>L12</sub> Habis itu, ada papan penunjuk arah. Itu **Nginx**.  

<sub>L13</sub> Cari menu lama? Ke ruko. Menu baru? Ke **kontainer**.  

<sub>L14</sub> Pengunjung cuma lihat **satu pintu**.  ·  *(napas)*  


*⏸ jeda ± 1 detik*

## 02 · DIAGRAM

<sub>L15</sub> Request masuk ke **SLB** dulu.  

<sub>L16</sub> SLB bagi rata ke beberapa **Nginx**, biar nggak ada yang kewalahan.  

<sub>L17</sub> Nginx baca alamatnya: path lama ke **legacy**, path baru ke **Kubernetes**.  

<sub>L18</sub> Sekalian jadi satpam kedua: siapa boleh masuk ke **mana**.  

<sub>L19</sub> Mau pindahin satu fitur ke container? Cukup ganti **papannya**.  


*⏸ jeda ± 1 detik*

## 03 · HASIL

<sub>L20</sub> Hasilnya: traffic kebagi **rata**, nggak ada pintu yang kebanjiran.  

<sub>L21</sub> Aplikasinya jadi lebih **stabil**.  

<sub>L22</sub> Dan aksesnya lebih **rapi**: semua lewat satu pintu yang dijaga.  


*⏸ jeda ± 1 detik*

## RECAP

<sub>L23</sub> Jadi, migrasi itu nggak harus **sekaligus**.  

<sub>L24</sub> Yang lama boleh tetap hidup, asal pintunya **satu**.  

<sub>L25</sub> Pengunjung nggak peduli ruko atau kontainer. Yang penting, pesanannya **sampai**.  


*⏸ jeda ± 1 detik*

## OUTRO

<sub>L26</sub> Episode depan: data nasabah, satu layar, **real-time**.  

<sub>L27</sub> Follow, biar nggak ketinggalan.  

---

Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)
