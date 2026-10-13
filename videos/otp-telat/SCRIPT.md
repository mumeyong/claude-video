# Kenapa OTP suka telat datang? — format QUICK

> Pilar: B (broad) · target 60–75 s · ide: [ideas/24-otp-telat.md](../../ideas/24-otp-telat.md)
> Satu hero: amplop OTP yang lewat kantor-kantor sortir (rute pos dari server ke HP). Signature: amplop berhenti di
> antrean conveyor, timer "kirim ulang" di HP terus jalan.
> Yang cuma Mumeyong bilang: di log server status-nya udah *sent* dari detik pertama — padahal itu cuma artinya
> "udah diserahin ke gateway", bukan "udah sampai di HP". (Pengalaman engineer yang mantau log.)
> Fakta: alur A2P SMS = server app → SMS gateway/aggregator → operator (SMSC, store-and-forward) → BTS → HP.
> Nggak ada angka di layar selain timer UI "0:59" (contoh layar, bukan statistik).
>
> HOOK — A/B (A terpasang):
> A · Timer "kirim ulang 0:59" jalan, HP sepi — "kodenya udah dikirim, dia cuma lagi antre."
> B · "Kenapa OTP WhatsApp datang duluan dari OTP SMS?"

## INTRO
[L01] Kamu nunggu kode OTP, // timernya udah "kirim ulang dalam lima puluh sembilan detik", // dan HP-mu masih *sepi*.
[L02] Padahal kodenya *udah* dikirim. // Dia cuma lagi *antre*.

## 00 · JALANNYA
[L03] Kode OTP itu kayak *surat* yang lewat beberapa kantor pos.
[L04] Dari server aplikasi, // diserahin ke *SMS gateway*, // terus ke *operator*, // terus ke BTS dekat rumahmu.
[L05] Tiap kantor nerima, // nyortir, // baru *nerusin*.

## 01 · ANTREAN
[L06] Masalahnya, // tiap kantor punya *antrean*.
[L07] Pas jam rame, // tanggal gajian, // atau lagi ada promo, // semua aplikasi ngirim kode lewat jalur yang *sama*.
[L08] Kalau HP-mu lagi *nggak dapet sinyal*, // operator nyimpen dulu suratnya, // nunggu kamu nongol lagi.
[L09] Yang bikin aku gemes: // di log server, // status-nya udah *sent* dari detik pertama.
[L10] Padahal *sent* cuma artinya udah diserahin ke gateway, // *bukan* udah sampai di HP-mu.

## 02 · KIRIM ULANG
[L11] Makanya sekarang banyak aplikasi kirim kode lewat *WhatsApp* atau notifikasi, // jalannya internet, // bukan antrean SMS.
[L12] Dan satu lagi: // jangan pencet *kirim ulang* berkali-kali.
[L13] Di banyak aplikasi, // kode baru bikin kode lama *hangus*, // jadi yang akhirnya nyampe malah yang udah nggak berlaku.

## RECAP
[L14] OTP telat itu bukan HP-mu yang rusak. // Suratnya cuma lagi *antre* di jalan.

## OUTRO
[L15] Kamu pernah nunggu OTP paling lama berapa menit? // Tulis di komentar.
[L16] Follow, biar nggak ketinggalan.
