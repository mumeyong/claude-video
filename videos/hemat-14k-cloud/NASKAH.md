# NASKAH — Gimana aku hemat $14.000/bulan biaya cloud

> 32 kalimat · 216 kata · ± 1:20 kalau dibaca ± 160 kata/menit
> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.
> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.
> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.

## INTRO

<sub>L01</sub> **Empat belas ribu dolar**.  ·  *(napas)*  

<sub>L02</sub> Segitu tagihan cloud yang aku potong, **tiap bulan**.  

<sub>L03</sub> Kalau dirupiahin, lebih dari **dua ratus juta**.  

<sub>L04</sub> Dan biasanya, masalahnya bukan cloud-nya yang mahal, tapi **bocor**.  

<sub>L05</sub> Ini empat langkah yang aku pakai, di Alibaba Cloud.  


*⏸ jeda ± 1 detik*

## 00 · BOCOR

<sub>L06</sub> Langkah pertama, **cari yang bocor** dulu.  

<sub>L07</sub> Server yang running, tapi **idle**, nggak ada yang pakai.  

<sub>L08</sub> Disk yang **unattached**, nggak nempel ke mana-mana.  

<sub>L09</sub> Snapshot lama, numpuk bertahun-tahun.  

<sub>L10</sub> Terus server development, ngapain nyala **jam dua pagi**?  

<sub>L11</sub> Pasang **auto-shutdown** di luar jam kerja. **Beres**.  


*⏸ jeda ± 1 detik*

## 01 · RIGHT-SIZING

<sub>L12</sub> Langkah kedua, **right-sizing**.  

<sub>L13</sub> Sering banget, CPU-nya kepakai cuma **sepuluh persen**.  

<sub>L14</sub> Tapi yang dibayar, **seratus persen**.  

<sub>L15</sub> Kayak sewa bus, buat nganter satu orang.  ·  *(napas)*  

<sub>L16</sub> Monitor dulu beberapa minggu, terus **downsize**.  


*⏸ jeda ± 1 detik*

## 02 · RESERVED & SPOT

<sub>L17</sub> Langkah ketiga, jangan semuanya **on-demand**.  

<sub>L18</sub> Yang nyala terus, pakai **reserved instance**, jauh lebih murah.  

<sub>L19</sub> Yang boleh mati sewaktu-waktu, pakai **spot instance**.  

<sub>L20</sub> Server sama, kerjaan sama, harganya **beda jauh**.  


*⏸ jeda ± 1 detik*

## 03 · ARSITEKTUR

<sub>L21</sub> Langkah terakhir, yang paling berat: **ubah arsitekturnya**.  

<sub>L22</sub> Monolith lama yang nyala dua puluh empat jam, dipecah.  

<sub>L23</sub> Bagian yang jarang dipakai, pindah ke **serverless**.  

<sub>L24</sub> Jadi bayarnya **pay-per-use**, cuma pas dipakai.  

<sub>L25</sub> Paling lama dikerjain, tapi efeknya paling panjang.  


*⏸ jeda ± 1 detik*

## RECAP

<sub>L26</sub> Jadi, empat langkahnya.  ·  *(napas)*  

<sub>L27</sub> Cari yang bocor, right-sizing, reserved dan spot, ubah arsitektur.  

<sub>L28</sub> Hasilnya, **empat belas ribu dolar**, tiap bulan.  

<sub>L29</sub> Dan ingat, hemat itu bukan berarti bikin sistemnya **lemot**.  


*⏸ jeda ± 1 detik*

## OUTRO

<sub>L30</sub> Mau dicek, biaya cloud-mu bocor di mana?  

<sub>L31</sub> Mampir ke **mumeyong dot dev**.  

<sub>L32</sub> Follow, buat bongkar arsitektur cloud lainnya.  

---

Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)
