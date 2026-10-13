# Kenapa OTP suka telat datang?

- **Status:** 🎬 produksi — [`videos/otp-telat/`](../videos/otp-telat/)
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** otp-telat
- **Seri:** —
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Kode OTP lewat beberapa "kantor pos" sebelum sampai ke HP-mu — dan antrean di salah satunya yang bikin kamu nunggu 2 menit.

## Hook (opsi)
- A: layar "Kirim ulang kode (0:59)" — "Kodenya udah dikirim. Dia lagi antre."
- B: "Kenapa OTP WhatsApp datang duluan dari OTP SMS?"

## Bab
1. Jalan OTP: app → SMS gateway → operator → BTS → HP
2. Kenapa telat: antrean pas promo/tanggal gajian, sinyal, nomor pindah operator
3. Kenapa sekarang banyak lewat WhatsApp/push: jalannya internet, bukan SMS
4. Yang bisa kamu lakuin: jangan spam "kirim ulang" (kode lama hangus)

## Bukti / visual
Metafora: **kantor pos sortir** — amplop OTP lewat conveyor, cap pos tiap kantor. Signature: amplop berhenti di conveyor yang macet, timer di HP terus jalan.

## Butuh komponen baru?
- `sorting_belt` (conveyor + amplop) · `otp_timer` (hitung mundur kirim ulang)

## Catatan
- ⚠️ cek fakta alur SMS A2P di Indonesia (aggregator, SMSC). Jangan sebut merek bank/app negatif.
- Mulai: `claude-video 24` atau `claude-video "Kenapa OTP suka telat datang?"`
