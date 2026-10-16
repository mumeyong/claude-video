# Gimana ojol nemuin driver terdekat dalam 3 detik? — format QUICK

> Dibuat 2026-10-15 · Pilar: B (broad) · target 60–75 s · ide: [ideas/26-ojol-driver-terdekat.md](../../ideas/26-ojol-driver-terdekat.md)
> Satu hero object: peta kota yang dipotong kotak hexagon — titik kamu di tengah, cincin nyala melebar.
> Satu hal yang cuma Mumeyong bisa bilang: yang paling dekat belum tentu yang dipilih — app nyari *kotak*, bukan jarak.
> Konsep umum (spatial index), bukan klaim cara kerja internal Gojek/Grab. Tanpa angka yang nggak ada sumbernya.
> Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — A/B (A terpasang):
> A · Pencet Pesan → beberapa detik → driver udah jalan; padahal sekota banyak banget driver.
> B · "Kenapa yang dapet order-mu kadang driver yang lebih jauh?"

## INTRO
[L01] Kamu pencet *Pesan*, // beberapa detik kemudian, satu driver udah jalan ke kamu.
[L02] Padahal sekota ada *banyak banget* driver online. // Gimana app-nya milih secepat itu?

## 00 · PETA DIPOTONG
[L03] Kalau app-nya ngitung jarak ke *semua* driver, satu-satu, // itu lambat.
[L04] Jadi petanya dipotong jadi kotak-kotak kecil, // kayak tribun stadion yang dibagi *sektor*.
[L05] Tiap driver tinggal nyatet, // dia lagi di kotak *mana*.
[L06] Caranya macem-macem: *geohash*, // atau *H3*, grid hexagon yang di-open-source Uber.

## 01 · CARI DARI KOTAKMU
[L07] Pas kamu pesan, app ngecek kotak tempat kamu *berdiri* dulu.
[L08] Kosong? // Dia melebar satu *cincin*, // terus satu cincin lagi.
[L09] Kayak nyari teman di stadion: // nggak teriak ke semua orang, // langsung ke *sektornya*.

## 02 · BUKAN CUMA JARAK
[L10] Nah, yang paling dekat belum tentu yang *dipilih*.
[L11] Bisa jadi dia lagi ngadep arah *sebaliknya*, // atau kepotong jalan satu arah.
[L12] Yang lebih jauh, // tapi searah dan baru kelar order, // bisa nyampe *duluan*.

## 03 · PAS HUJAN
[L13] Pas hujan, // yang pesan di satu kotak tiba-tiba *numpuk*, // driver-nya tetap segitu.
[L14] Makanya tarif bisa naik: // salah satu tujuannya, narik driver dari kotak *sebelah*.

## RECAP
[L15] Jadi rahasianya bukan komputer super, // tapi peta yang dipotong *kotak*.

## OUTRO
[L16] Pernah dapet driver yang malah muter jauh? // Ceritain di komentar.
[L17] Follow, biar nggak ketinggalan.
