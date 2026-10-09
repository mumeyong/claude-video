# IDENTITY — Kenapa app bank down pas tanggal gajian?

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: kenalan-mumeyong, sebelumnya lagi:
> bongkar-ep03-serverless-big-data). Bukan bagian seri → HUD `MUMEYONG · KASUS`, tanpa bumper seri.
> Pilar B · format QUICK.

| # | Pilihan | Untuk video ini | Beda dari kenalan / EP03? |
|---|---|---|---|
| 1 | **Metafora sentral** | **kasir supermarket tanggal muda**. Kasir = server (bisa ditambah), **buku kas** = database (cuma satu), fotokopian buku kas = read replica. Tersangkanya juga benda supermarket: KASIR, ETALASE, BUKU KAS | ✓ (denah / dapur) |
| 2 | **Signature move** | **lembar disobek**: kalender disobek cepat 21 → 25 (hook) · kartu tersangka yang lolos disobek dari papan (00) · lembar fotokopi disobek dari buku kas jadi read replica (02) · kalender 25 balik di recap | ✓ (garis-lalu-isi / kompor nyala-padam) |
| 3 | **Signature color** | merah `#F03B4F` (`CHAPTER[5]`): kalender, pin + benang merah, stempel PELAKU, buku kas yang kepanasan | ✓ (teal / oranye) |
| 4 | **Format hook** | **cold open di tengah kejadian**: tanggal 25, jam 09.01, gaji masuk, app muter terus | ✓ (pertanyaan spesifik / before-after) |
| 5 | **Struktur** | **detektif**: 3 tersangka → 2 lolos → pelakunya → obatnya | ✓ (kenalan→3 angka→peta / format seri) |
| 6 | **Komponen baru** | `tear_calendar` (kalender meja, lembar disobek + tanggal dilingkari tangan) · `suspect_card` + `red_string` (papan tersangka) · `cashier` (meja kasir top-down) · `ledger` (buku kas: baris ketulis, kepanasan, lembar fotokopi) · `queue_dots` (antrean orang di sepanjang jalur, bisa macet) | ✓ |
| 7 | **Musik** | E · tense (`v.music`) — suasana detektif | ✓ (G bright / D warm) |

Metafora dipakai di: INTRO (kalender tanggal muda + 3 kartu tersangka kosong), TERSANGKA (kartu KASIR dan ETALASE),
PELAKU (supermarket: 20 kasir → semua garis antre ke satu buku kas), OBATNYA (fotokopian buku kas), RECAP (kalender 25
balik + satu buku kas).

## Sentuhan manusia
- **Artefak asli:** angka dari CV: nahan 10.000 request barengan (L16) → nyambung ke EP01 (outro + pinned comment).
- **Opini:** "Auto-scaling nggak nolong, kalau database-nya cuma satu pintu." (L17)
- **Kejutan:** L10 — kamera mundur dari 20 kasir yang sibuk → ternyata semua jalurnya nyambung ke **satu** buku kas
  kecil di bawah. Yang kelihatan "kurang" (kasir) ternyata bukan masalahnya.
- **Ketidaksempurnaan:** tanggal 25 dilingkari tangan (spidol merah, nggak rapi) · stempel PELAKU miring ·
  hand note "setengah benar" di kartu tersangka pertama.

## Anti-generik checklist
- [x] 1–5 beda dari video sebelumnya (dan dari 2 sebelumnya)
- [x] ≥ 1 komponen baru (5)
- [x] artefak asli (10.000 request, CV)
- [x] opini (L17)
- [x] satu kejutan (pull-out ke satu buku kas, L10)
- [x] metafora kepakai di ≥ 3 bab (semua)
- [x] anti-slop: tanpa server biru, tanpa nama bank; hero = kalender, papan tersangka, buku kas
