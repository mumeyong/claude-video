# Slot berita: Bongkar Kejadian (reaktif)

- **Status:** 💡 ide (format berulang) · **Pilar:** B (broad) · **Format:** QUICK, tayang ≤ 48 jam
- **Slug:** bongkar-kejadian-<nama>
- **Seri:** Bongkar Kejadian
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-06

## Takeaway (1 kalimat)
Tiap outage / kebocoran besar di Indonesia: apa yang (kemungkinan) terjadi, kenapa, dan pelajaran arsitekturnya.

## Struktur tetap
Kronologi publik (3 titik waktu) → "kemungkinan kenapa" (1–2 penyebab, dari info publik) → pelajaran arsitektur yang
bisa dipakai penonton → recap 1 kalimat.

## Aturan (wajib)
- **Cuma info publik.** Sebut sumber di caption. Kalau belum ada penjelasan resmi, bilang "kemungkinan", jangan nebak
  seolah fakta.
- **Jangan nyalahin orang/tim.** Bahas sistemnya, bukan engineer-nya.
- Siapin komponen yang bisa langsung dipakai: `arch_diagram`, `particle_flow`, `load_graph`, `big_clock` (#07).
- Identitas tetap harus beda dari video sebelumnya (REGISTRY) — metafora diambil dari kejadiannya sendiri.

## Catatan
Kalau ada kejadian: bilang "bongkar kejadian <X>" → Claude bikin naskah dari sumber publik yang kamu kasih.
