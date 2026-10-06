# Ide video — backlog

Satu file per ide (`NN-slug.md`, salin dari `_TEMPLATE.md`). Tabel ini indeksnya — update tiap status berubah.

**Status:** 💡 ide · ⭐ dipilih · 🎬 produksi (`videos/<slug>/`) · ✅ tayang · 🗑 batal

| # | Ide | Status | Durasi | Butuh komponen baru | Catatan |
|---|---|---|---|---|---|
| 01 | [Gimana aku hemat $14.000/bulan biaya cloud](01-hemat-14k-cloud.md) | 🎬 produksi | 90–120 s | cost chart, bar before/after | fase 5: review visual |
| 02 | [Seri: Bongkar Arsitektur (7 ep)](02-seri-bongkar-arsitektur.md) | 🎬 produksi — EP01 [`videos/bongkar-ep01-kubernetes-10k`](../videos/bongkar-ep01-kubernetes-10k/) fase 5 · EP02 [`videos/bongkar-ep02-big-data-migration`](../videos/bongkar-ep02-big-data-migration/) fase 5: review visual · EP03 [`videos/bongkar-ep03-serverless-big-data`](../videos/bongkar-ep03-serverless-big-data/) fase 5: review visual | 60–90 s/ep | architecture diagram | cek NDA tiap project |
| 03 | [Cloud Architect itu ngapain sih?](03-cloud-architect-ngapain.md) | 💡 ide | 60–90 s | — | audiens luas, klien & recruiter |
| 04 | [5 tanda biaya cloud kamu bocor](04-tanda-biaya-cloud-bocor.md) | 💡 ide | 45–60 s | checklist | teaser sebelum #01 |
| 05 | [Kubernetes bukan jawaban buat semua hal](05-kubernetes-bukan-jawaban.md) | 💡 ide | 60–90 s | — | opini, mancing komentar |
| 06 | [Kenapa app bank down pas tanggal gajian?](06-bank-down-tanggal-gajian.md) | 💡 ide | 60–70 s | tear_calendar, suspect_board | **B** · QUICK · detektif 3 tersangka |
| 07 | [Kenapa war tiket konser selalu crash?](07-war-tiket-konser-crash.md) | 💡 ide | 60–75 s | queue_dispenser, big_clock, refresh_storm | **B** · QUICK · timeline per detik |
| 08 | [QRIS: 2 detik setelah kamu scan](08-qris-dua-detik.md) | 💡 ide | 60–70 s | relay_track, slowmo_clock | **B** · QUICK · ⚠️ cek fakta alur |
| 09 | [Slot berita: Bongkar Kejadian](09-slot-bongkar-kejadian.md) | 💡 format | 60–75 s | pakai ulang | **B** · reaktif ≤ 48 jam |
| 10 | [Foto WhatsApp sebenernya lewat mana?](10-foto-whatsapp-ke-mana.md) | 💡 ide | 60–70 s | parcel, tracking_log, double_tick | **B** · QUICK · ⚠️ cek fakta |
| 11 | [Dari System Engineer ke Senior — jalur aku](11-jenjang-karier-cloud.md) | 💡 ide | 75–90 s | skill_tree, name_card | **C** · FULL · artefak = CV asli |
| 12 | [Roadmap jadi cloud engineer](12-roadmap-cloud-engineer.md) | 💡 ide | 60–75 s | transit_map, train | **C** · QUICK · save-able |
| 13 | [5 pertanyaan interview cloud](13-pertanyaan-interview-cloud.md) | 💡 ide | 60–75 s | flip_card, countdown_ring | **C** · QUICK · kuis |

## Strategi & urutan tayang
Lihat **[STRATEGY.md](STRATEGY.md)** — tujuan creator income, rasio pilar **3 B (broad) : 1 C (karier) : 1 D (deep)**,
format FULL vs QUICK, aturan anti-slop, dan urutan tayang yang disarankan.

## Cara pakai
- **Nambah ide:** bilang ke Claude "simpan ide: …" → dibuatin file + baris di tabel ini.
- **Mulai produksi:** "kerjain ide #01" → status 🎬, Claude bikin `videos/<slug>/` dan mulai dari SCRIPT.md.
- **Setelah tayang:** tulis link + catatan performa (views, komentar menarik) di file idenya → bahan ide berikutnya.
