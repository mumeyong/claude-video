# NASKAH — Bongkar Arsitektur EP04 — Monolith lama, dipecah jadi event-driven

> 27 kalimat · 224 kata · ± 1:23 kalau dibaca ± 160 kata/menit
> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.
> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.
> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.

## INTRO

<sub>L01</sub> Bagian terbaik dari aplikasi ini? Sebagian besar waktunya, dia **tidur**.  

<sub>L02</sub> Baru bangun pas ada **kejadian**. Selesai, tidur lagi.  ·  *(napas)*  

<sub>L03</sub> Dulu nggak gitu. Satu aplikasi gede, nyala terus, ngerjain **semuanya**.  

<sub>L04</sub> Project ini: monolith lama, dipecah jadi **event-driven**.  


*⏸ jeda ± 1 detik*

## 00 · MASALAH

<sub>L05</sub> Bayangin satu **rumah gede**, semua kerjaan ada di dalamnya.  

<sub>L06</sub> Terima order, proses bayar, kirim notifikasi, bikin laporan. **Satu atap**.  

<sub>L07</sub> Lampunya nyala dua puluh empat jam, walau yang kerja cuma **satu kamar**.  

<sub>L08</sub> Satu kamar **korslet**? Seluruh rumah ikut gelap.  

<sub>L09</sub> Mau benerin dapur doang? Satu aplikasi harus di-deploy **ulang**.  ·  *(napas)*  


*⏸ jeda ± 1 detik*

## 01 · KEPUTUSAN

<sub>L10</sub> Jadi rumahnya **dipecah**.  

<sub>L11</sub> Tiap kerjaan dapet rumah kecil sendiri. Satu **function**, satu tugas.  

<sub>L12</sub> Dan mereka nggak saling panggil. Mereka dengerin **kentongan**.  

<sub>L13</sub> Ada order masuk? Kentongan dipukul. Itu namanya **event**.  

<sub>L14</sub> Rumah yang berkepentingan nyala, kerja, terus **gelap lagi**.  ·  *(napas)*  


*⏸ jeda ± 1 detik*

## 02 · DIAGRAM

<sub>L15</sub> Order masuk lewat API, jadi satu **event**.  

<sub>L16</sub> Event itu didengar tiga function sekaligus: bayar, notifikasi, laporan. Jalan **barengan**.  

<sub>L17</sub> Function-nya jalan di **AWS Lambda** dan **Alibaba Function Compute**.  

<sub>L18</sub> Semuanya di dalam **private network**. Orang luar nggak bisa masuk.  

<sub>L19</sub> Mau keluar? Cuma lewat satu pintu: **NAT gateway**.  


*⏸ jeda ± 1 detik*

## 03 · HASIL

<sub>L20</sub> Hasilnya: compute overhead turun **drastis**.  

<sub>L21</sub> Satu function error? Yang lain tetap **jalan**.  

<sub>L22</sub> Mau update satu fitur? Deploy **satu function** aja.  


*⏸ jeda ± 1 detik*

## RECAP

<sub>L23</sub> Jadi event-driven itu bukan soal kodenya **dipecah**.  

<sub>L24</sub> Tapi soal yang mukul kentongan **nggak nunggu** siapa-siapa. Pukul, terus pergi.  

<sub>L25</sub> Dan jujur: nggak semua monolith harus dipecah. Kalau dia sehat, **biarin**.  


*⏸ jeda ± 1 detik*

## OUTRO

<sub>L26</sub> Episode depan: legacy dan container, hidup **berdampingan**.  

<sub>L27</sub> Follow, biar nggak ketinggalan.  

---

Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)
