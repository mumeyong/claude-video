# Bongkar Arsitektur EP04 — Monolith lama, dipecah jadi event-driven

> Seri Bongkar Arsitektur · target 75–90 s · klien disamarkan ("aplikasi monolith lama", tanpa industri)
> Fakta dari portfolio/CV (BL-Revamp Serverless): monolith lama di-redesign jadi event-driven serverless —
> AWS Lambda + Alibaba Function Compute; data diisolasi ketat lewat private network + NAT gateway;
> compute overhead turun drastis, bottleneck operasional berkurang. TIDAK ada angka — jangan ditambahin.
> Contoh function (bayar · notifikasi · laporan) = ilustrasi umum, bukan nama asli; minta user konfirmasi/ganti.
> Tech terms tetap English (GLOSSARY.md). Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — pilih satu (A sudah terpasang):
> A · Klaim nyeleneh:      "Bagian terbaik dari aplikasi ini? Sebagian besar waktunya, dia tidur."
> B · Pertanyaan spesifik: "Kenapa bug di fitur laporan bisa bikin fitur bayar ikut down?"
> C · Analogi:             "Kampung yang baik itu tidur semua, sampai kentongan bunyi."

## INTRO
[L01] Bagian terbaik dari aplikasi ini? Sebagian besar waktunya, dia *tidur*.
[L02] Baru bangun pas ada *kejadian*. Selesai, tidur lagi. //
[L03] Dulu nggak gitu. Satu aplikasi gede, nyala terus, ngerjain *semuanya*.
[L04] Project ini: monolith lama, dipecah jadi *event-driven*.

## 00 · MASALAH
[L05] Bayangin satu *rumah gede*, semua kerjaan ada di dalamnya.
[L06] Terima order, proses bayar, kirim notifikasi, bikin laporan. *Satu atap*.
[L07] Lampunya nyala dua puluh empat jam, walau yang kerja cuma *satu kamar*.
[L08] Satu kamar *korslet*? Seluruh rumah ikut gelap.
[L09] Mau benerin dapur doang? Satu aplikasi harus di-deploy *ulang*. //

## 01 · KEPUTUSAN
[L10] Jadi rumahnya *dipecah*.
[L11] Tiap kerjaan dapet rumah kecil sendiri. Satu *function*, satu tugas.
[L12] Dan mereka nggak saling panggil. Mereka dengerin *kentongan*.
[L13] Ada order masuk? Kentongan dipukul. Itu namanya *event*.
[L14] Rumah yang berkepentingan nyala, kerja, terus *gelap lagi*. //

## 02 · DIAGRAM
[L15] Order masuk lewat API, jadi satu *event*.
[L16] Event itu didengar tiga function sekaligus: bayar, notifikasi, laporan. Jalan *barengan*.
[L17] Function-nya jalan di *AWS Lambda* dan *Alibaba Function Compute*.
[L18] Semuanya di dalam *private network*. Orang luar nggak bisa masuk.
[L19] Mau keluar? Cuma lewat satu pintu: *NAT gateway*.

## 03 · HASIL
[L20] Hasilnya: compute overhead turun *drastis*.
[L21] Satu function error? Yang lain tetap *jalan*.
[L22] Mau update satu fitur? Deploy *satu function* aja.

## RECAP
[L23] Jadi event-driven itu bukan soal kodenya *dipecah*.
[L24] Tapi soal yang mukul kentongan *nggak nunggu* siapa-siapa. Pukul, terus pergi.
[L25] Dan jujur: nggak semua monolith harus dipecah. Kalau dia sehat, *biarin*.

## OUTRO
[L26] Episode depan: legacy dan container, hidup *berdampingan*.
[L27] Follow, biar nggak ketinggalan.
