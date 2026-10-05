# Ide video — backlog

Satu file per ide (`NN-slug.md`, salin dari `_TEMPLATE.md`). Tabel ini indeksnya — update tiap status berubah.

**Status:** 💡 ide · ⭐ dipilih · 🎬 produksi (`videos/<slug>/`) · ✅ tayang · 🗑 batal

| # | Ide | Status | Durasi | Butuh komponen baru | Catatan |
|---|---|---|---|---|---|
| 01 | [Gimana aku hemat $14.000/bulan biaya cloud](01-hemat-14k-cloud.md) | 🎬 produksi | 90–120 s | cost chart, bar before/after | fase 5: review visual |
| 02 | [Seri: Bongkar Arsitektur (7 ep)](02-seri-bongkar-arsitektur.md) | 🎬 produksi — EP01 [`videos/bongkar-ep01-kubernetes-10k`](../videos/bongkar-ep01-kubernetes-10k/) fase 5: review visual | 60–90 s/ep | architecture diagram | cek NDA tiap project |
| 03 | [Cloud Architect itu ngapain sih?](03-cloud-architect-ngapain.md) | 💡 ide | 60–90 s | — | audiens luas, klien & recruiter |
| 04 | [5 tanda biaya cloud kamu bocor](04-tanda-biaya-cloud-bocor.md) | 💡 ide | 45–60 s | checklist | teaser sebelum #01 |
| 05 | [Kubernetes bukan jawaban buat semua hal](05-kubernetes-bukan-jawaban.md) | 💡 ide | 60–90 s | — | opini, mancing komentar |

## Urutan tayang yang disarankan
01 (cerita utama) → **02 EP01** (mulai seri) → 03 (siapa aku) → 04 (checklist, save-able) → 02 EP02 → 05 (opini)

## Cara pakai
- **Nambah ide:** bilang ke Claude "simpan ide: …" → dibuatin file + baris di tabel ini.
- **Mulai produksi:** "kerjain ide #01" → status 🎬, Claude bikin `videos/<slug>/` dan mulai dari SCRIPT.md.
- **Setelah tayang:** tulis link + catatan performa (views, komentar menarik) di file idenya → bahan ide berikutnya.
