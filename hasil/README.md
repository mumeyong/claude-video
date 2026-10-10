# Hasil — video yang sudah final

`claude-video <slug> final` otomatis menyalin hasil final ke `hasil/<slug>/`. **Folder di `hasil/` = antrean upload.**
Setelah tayang → pindah ke `hasil/_tayang/<slug>/` (dan `videos/<slug>` → `videos/_arsip/`). Di git cuma POST.md;
mp4 + cover.png di-ignore (cover bisa dibikin ulang dari scenes.py).

```
hasil/<slug>/
├── <slug>.mp4    video final 1080×1920 60fps (TIDAK di-commit — simpan/backup sendiri, mis. Google Drive)
├── cover.png     (nggak di-commit) cover TikTok yang didesain (`v.cover` di scenes.py; preview tiap review: out/cover.png)
└── POST.md       caption, deskripsi, hashtag, komentar pin, checklist upload, performa (ditulis Claude waktu produksi)
```

## Pembuka

| Tanggal tayang | Video | Durasi | TikTok | Status |
|---|---|---|---|---|
| ≤ 2026-10-08 (PERTAMA, pin) | [kenalan-mumeyong](_tayang/kenalan-mumeyong/) | ± 70 s | — | ✅ tayang |

## B · Broad

| Tanggal tayang | Video | Durasi | TikTok | Status |
|---|---|---|---|---|
| ≤ 2026-10-08 | [kenapa-bank-down-gajian](_tayang/kenapa-bank-down-gajian/) | ± 72 s | — | ✅ tayang |
| — (#3) | [war-tiket-crash](_tayang/war-tiket-crash/) | ± 70 s | — | ✅ tayang |
| — (#5) | [qris-dua-detik](_tayang/qris-dua-detik/) | ± 72 s | — | ✅ tayang |
| — | [biaya-cloud-bocor](_tayang/biaya-cloud-bocor/) | ± 70 s | — | ✅ tayang |
| — | [wifi-ep01-lampu-los](_tayang/wifi-ep01-lampu-los/) | ± 72 s | — | ✅ tayang |
| — | [wifi-ep02-connected-no-internet](_tayang/wifi-ep02-connected-no-internet/) | ± 74 s | — | ✅ tayang |
| — | [foto-whatsapp-lewat-mana](_tayang/foto-whatsapp-lewat-mana/) | ± 74 s | — | ✅ tayang |
| — | [ai-ngarang-jawaban](ai-ngarang-jawaban/) | ± 74 s | — | 🎬 produksi |
| — | [prompt-diproses-di-mana](prompt-diproses-di-mana/) | ± 77 s | — | 🎬 produksi |

## C · Karier

| Tanggal tayang | Video | Durasi | TikTok | Status |
|---|---|---|---|---|
| — (#4) | [roadmap-cloud-engineer](_tayang/roadmap-cloud-engineer/) | ± 73 s | — | ✅ tayang |
| — | [kubernetes-bukan-jawaban](_tayang/kubernetes-bukan-jawaban/) | ± 74 s | — | ✅ tayang |
| — | [jalur-karier-cloud](jalur-karier-cloud/) | ± 78 s | — | 🎬 produksi |
| — | [interview-cloud-5-pertanyaan](interview-cloud-5-pertanyaan/) | ± 78 s | — | 🎬 produksi |

## D · Seri Bongkar Arsitektur

| Tanggal tayang | Video | Durasi | TikTok | Status |
|---|---|---|---|---|
| ≤ 2026-10-08 | [bongkar-ep01-kubernetes-10k](_tayang/bongkar-ep01-kubernetes-10k/) | — | — | ✅ tayang · POST.md nggak ada |
| ≤ 2026-10-08 | [bongkar-ep02-big-data-migration](_tayang/bongkar-ep02-big-data-migration/) | — | — | ✅ tayang · POST.md nggak ada |
| ≤ 2026-10-08 | [bongkar-ep03-serverless-big-data](_tayang/bongkar-ep03-serverless-big-data/) | — | — | ✅ tayang · POST.md nggak ada |
| ≤ 2026-10-08 | [bongkar-ep04-monolith-event-driven](_tayang/bongkar-ep04-monolith-event-driven/) | ± 85 s | — | ✅ tayang |
| — | [bongkar-ep05-legacy-container-hybrid](_tayang/bongkar-ep05-legacy-container-hybrid/) | ± 80 s | — | ✅ tayang |
| — | [bongkar-ep06-project-360](_tayang/bongkar-ep06-project-360/) | ± 80 s | — | ✅ tayang |
| — | [bongkar-ep07-azure-ai-infra](_tayang/bongkar-ep07-azure-ai-infra/) | ± 80 s | — | ✅ tayang |

## Lainnya

| Tanggal tayang | Video | Durasi | TikTok | Status |
|---|---|---|---|---|
| — | hemat-14k-cloud | ± 100 s | — | 🎬 produksi (belum final) |
| — | contoh | 34 s | — | demo, nggak diupload |

**Status:** 🎬 produksi · 📦 final (siap upload) · ✅ tayang
