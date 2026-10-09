# Bongkar Arsitektur EP05 — Legacy dan container, hidup berdampingan

> Seri Bongkar Arsitektur · target 75–90 s · klien disamarkan ("konglomerasi", tanpa nama/industri)
> Fakta dari portfolio/CV (Conglomeration Hybrid Infra): traffic distribution di-re-architect pakai Nginx + SLB
> buat bagi beban antara legacy monolith dan workload container (Kubernetes) yang baru; aplikasi lebih stabil,
> access management lebih rapi. TIDAK ada angka — jangan ditambahin.
> "Pindahin satu fitur = cukup ganti routing di Nginx" (L19) + rute contoh (menu lama / menu baru) = praktik umum &
> ilustrasi; minta user konfirmasi cocok dengan yang dia kerjakan.
> Tech terms tetap English (GLOSSARY.md). "kontainer" (ejaan Indonesia) HANYA buat kios kontainer di metafora;
> objek tech-nya tetap "container". Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — pilih satu (A sudah terpasang):
> A · Pertanyaan spesifik: "Gimana caranya aplikasi lama dan Kubernetes baru jalan barengan, tanpa user sadar?"
> B · Before/after:        "Dulu: tiga pintu, satu kebanjiran. Sekarang: satu pintu, semua kebagian."
> C · Mitos dicoret:       "Pindah ke Kubernetes harus matiin yang lama? Nggak juga."

## INTRO
[L01] Gimana caranya aplikasi lama dan Kubernetes baru jalan *barengan*?
[L02] Tanpa user sadar, mereka lagi dilayani yang *mana*. //
[L03] Yang lama belum bisa dimatiin. Yang baru udah *jalan*.
[L04] Project ini: legacy dan container, hidup *berdampingan*.

## 00 · MASALAH
[L05] Bayangin satu lahan *kuliner*.
[L06] Di kiri, *ruko lama*: udah lama buka, pelanggannya setia.
[L07] Di kanan, deretan *kios kontainer*: gampang ditambah, gampang dipindah.
[L08] Masalahnya: pintu masuknya *beda-beda*.
[L09] Satu pintu kebanjiran, yang lain sepi. Aplikasinya ikut *goyang*. //

## 01 · KEPUTUSAN
[L10] Jadi keputusannya: *satu pintu depan*.
[L11] Di situ ada satpam yang bagi rata pengunjung. Itu *load balancer*, SLB.
[L12] Habis itu, ada papan penunjuk arah. Itu *Nginx*.
[L13] Cari menu lama? Ke ruko. Menu baru? Ke *kontainer*.
[L14] Pengunjung cuma lihat *satu pintu*. //

## 02 · DIAGRAM
[L15] Request masuk ke *SLB* dulu.
[L16] SLB bagi rata ke beberapa *Nginx*, biar nggak ada yang kewalahan.
[L17] Nginx baca alamatnya: path lama ke *legacy*, path baru ke *Kubernetes*.
[L18] Sekalian jadi satpam kedua: siapa boleh masuk ke *mana*.
[L19] Mau pindahin satu fitur ke container? Cukup ganti *papannya*.

## 03 · HASIL
[L20] Hasilnya: traffic kebagi *rata*, nggak ada pintu yang kebanjiran.
[L21] Aplikasinya jadi lebih *stabil*.
[L22] Dan aksesnya lebih *rapi*: semua lewat satu pintu yang dijaga.

## RECAP
[L23] Jadi, migrasi itu nggak harus *sekaligus*.
[L24] Yang lama boleh tetap hidup, asal pintunya *satu*.
[L25] Pengunjung nggak peduli ruko atau kontainer. Yang penting, pesanannya *sampai*.

## OUTRO
[L26] Episode depan: data nasabah, satu layar, *real-time*.
[L27] Follow, biar nggak ketinggalan.
