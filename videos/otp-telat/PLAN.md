# PLAN — Kenapa OTP suka telat datang?

<!-- registry
pilar: B
metafora: kantor pos sortir — kode OTP = surat (amplop cap hijau) yang lewat server app → SMS gateway → operator (SMSC) → BTS → HP; tiap kantor punya conveyor + antrean; nggak ada sinyal = surat disimpan di baki; status `sent` di log = baru diserahin ke gateway
signature: amplop kita diem di antrean conveyor sementara timer "Kirim ulang dalam 0:59" di HP terus jalan (timer jalan di jam suara, nyentuh 0:00 pas "kirim ulang") · look flat-big
look: flat-big
color: hijau `#10A060`
hook: layar OTP yang semua orang kenal ("kirim ulang dalam 0:59", HP sepi) → "kodenya udah dikirim, lagi antre"
struktur: satu HP + satu amplop dari awal sampai recap: jalannya (4 loket di satu rute) → antrean (conveyor, numpuk, baki, log server) → kirim ulang (internet vs SMS, kode lama hangus) → recap gelap
komponen: kantorpos (amplop, belt, loket, hp_otp, log_card, notif)
musik: ambient F warm 80 · sfx mech
durasi: ~72
-->

## Idenya
Semua orang pernah natap layar "Kirim ulang dalam 0:59" — jadi layar itu hero-nya, dari detik pertama sampai recap,
dan timer-nya beneran jalan di jam suara: dia nyentuh 0:00 tepat pas narasi bilang "kirim ulang". Di atasnya, kode
OTP jadi surat ber-cap hijau yang lewat empat loket di satu rute, lalu macet di conveyor operator yang makin numpuk
pas jam rame, dipindah ke baki "disimpan" pas HP nggak dapet sinyal, dan balik lagi pas sinyal nongol. Momen
Mumeyong: kartu `server.log` — `status: sent ✓` dari detik pertama, tapi `delivered` masih kosong. Penutupnya praktis:
jalur internet (WhatsApp/notifikasi) nggak lewat antrean SMS, dan spam "kirim ulang" bikin kode yang nyampe duluan
justru yang udah hangus. Penonton pulang dengan satu gambar: suratnya nggak hilang, dia lagi antre.
