# IDENTITY — 5 tanda biaya cloud kamu bocor

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: bongkar-ep07-azure-ai-infra · sebelumnya lagi:
> bongkar-ep06-project-360). Draft lama di ideas/04 (rumah + teal + lampu mati) diganti: rumah/kampung baru dipakai EP04.

| # | Pilihan | Untuk video ini | Beda dari video sebelumnya? |
|---|---|---|---|
| 1 | **Metafora sentral** | **meteran token listrik prabayar + satu colokan T**: akun cloud = meteran yang kedip-kedip; tiap tanda = satu barang yang nyolok dan nyedot diam-diam (colokan T beranak = tanpa tag, kulkas penuh basi = snapshot, AC 2 PK di kamar kos = instance kegedean, charger tanpa HP = unattached disk, lampu teras siang bolong = VM 24 jam) | ✓ (atlet bulu tangkis · stopmap) |
| 2 | **Signature move** | **lampu pulsa meteran (LED imp/kWh) kedip cepat → tiap kebocoran diberesin, kedipnya melambat** + barangnya dicabut / dimatiin (colokan lepas, jatuh ke lantai) | ✓ (kok melengkung · lembar ke map) |
| 3 | **Signature color** | teal `#0E9AAB` (tokens `CHAPTER[4]`) — layar LCD meteran, LED "normal", tag beres | ✓ (oranye · ungu); teal terakhir EP04 (4 video lalu) |
| 4 | **Format hook** | **angka dulu** — angka asli: "$5.000 / bulan" (CV) count-up | ✓ (mitos dicoret · cold open); terakhir war-tiket (7 video lalu) |
| 5 | **Struktur** | **hitung mundur 5 → 1** (paling sering di nomor 1) | ✓ — struktur baru di channel |
| 6 | **Komponen baru** (`engine/components/listrik.py`) | `token_meter` (meteran prabayar: LCD, keypad, LED pulsa dengan laju berubah tapi tetap frame = f(t)) · `stop_kontak` (colokan T panjang + steker + kabel) · `alat` (5 barang: colokan T beranak, kulkas, AC, charger, lampu teras) · `pulse_led` (fase kedip dari laju piecewise) | ✓ |
| 7 | **Musik** | C · warm (`v.music`) — beda dari EP07 (E bright) & EP06 (G tense) | ✓ |
| 8 | **Upgrade gerak (pertama kali)** | `fx.py`: steker dicabut → `ghost_trail` waktu terbang, `land` + `squash` + `contact_shadow` waktu jatuh ke lantai; check badge & tag `settle` | baru |

Metafora dipakai di: INTRO (meteran kedip cepat), 00–02 (tiap tanda = satu barang di colokan T), RECAP (kejutan: dinding
meteran rusun — semua kedip cepat, punya kita pelan).

## Sentuhan manusia
- **Artefak asli:** "$5.000 / bulan" — angka asli dari CV (FinOps automation, rightsizing, usage monitoring).
- **Opini:** "Kebocoran cloud itu jarang yang gede. Yang bikin mahal: yang kecil, tapi dibiarin." (L15)
- **Kejutan:** RECAP — kamera mundur: meteran kita ternyata satu dari puluhan meteran di dinding rusun (akun lain),
  semuanya masih kedip cepat.
- **Ketidaksempurnaan:** colokan T beranak miring, satu steker setengah nyolok; label tag tulisan tangan.

## Anti-generik checklist
- [x] 1–5 beda dari video sebelumnya (REGISTRY)
- [x] ≥ 1 komponen baru (4)
- [x] artefak asli ($5.000/bulan dari CV)
- [x] opini di naskah (L15)
- [x] satu kejutan (dinding meteran rusun)
- [x] metafora kepakai di ≥ 3 bab (semua bab)
- [x] hero = objek metafora (meteran + colokan T), bukan server/awan
