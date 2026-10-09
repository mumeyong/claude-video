# Seri: Bongkar Arsitektur (7 episode)

- **Status:** ✅ tayang EP01–07 (tamat) — EP01 → [`videos/_arsip/bongkar-ep01-kubernetes-10k/`](../videos/_arsip/bongkar-ep01-kubernetes-10k/) · ✅ tayang · EP02 → [`videos/_arsip/bongkar-ep02-big-data-migration/`](../videos/_arsip/bongkar-ep02-big-data-migration/) · ✅ tayang · EP03 → [`videos/_arsip/bongkar-ep03-serverless-big-data/`](../videos/_arsip/bongkar-ep03-serverless-big-data/) · ✅ tayang · EP04 → [`videos/_arsip/bongkar-ep04-monolith-event-driven/`](../videos/_arsip/bongkar-ep04-monolith-event-driven/) · ✅ tayang · EP05 → [`videos/_arsip/bongkar-ep05-legacy-container-hybrid/`](../videos/_arsip/bongkar-ep05-legacy-container-hybrid/) · ✅ tayang · EP06 → [`videos/_arsip/bongkar-ep06-project-360/`](../videos/_arsip/bongkar-ep06-project-360/) · ✅ tayang · EP07 → [`videos/_arsip/bongkar-ep07-azure-ai-infra/`](../videos/_arsip/bongkar-ep07-azure-ai-infra/) · ✅ tayang
- **Slug:** bongkar-<nama-episode>
- **Seri:** Bongkar Arsitektur
- **Durasi target:** 60–90 s per episode
- **Ditambahkan:** 2026-10-05

## Takeaway (1 kalimat)
Tiap episode: satu masalah nyata → satu keputusan arsitektur → hasilnya.

## Episode (dari project di mumeyong.dev)
1. Kubernetes yang nahan 10.000 request barengan — ICE ACK Platform
2. Pindahin big data ke cloud tanpa satu byte hilang — Big Data Cloud Migration
3. Ganti stack big data jadi serverless — Next-Gen Big Data Ecosystem
4. Monolith lama dipecah jadi event-driven — BL-Revamp Serverless
5. Legacy + container hidup berdampingan — Conglomeration Hybrid Infra
6. Narik data pelanggan dalam milidetik — Project 360
7. Fondasi buat training AI di Azure — Azure AI Infrastructure

## Format tetap tiap episode
Hook (masalah) → **Kondisi awal** → **Keputusan** → **Diagram** → **Hasil (angka)** → recap → outro

## Butuh komponen baru?
- ⚠️ **Architecture diagram** (node + panah + traffic mengalir)
- Badge provider (AWS/Azure/GCP/Alibaba) sebagai teks, bukan logo

## Catatan
- Cek NDA tiap project — nama klien disamarkan.
- Komponen dari ide #01 (cost chart) dipakai ulang di sini.

## Identitas SERI (tetap di semua episode)
- HUD: `MUMEYONG · BONGKAR ARSITEKTUR` + `EP 01` di kanan atas (gantiin "TUTORIAL")
- **Bumper** 1,5 s di awal setelah hook: kartu judul "BONGKAR ARSITEKTUR · EP 01" + nama project (disamarkan)
- **Struktur tetap:** Masalah → Kondisi awal → Keputusan → Diagram → Hasil (angka) → recap → outro
- **Komponen andalan seri:** `arch_diagram` (node + garis + paket data mengalir) — muncul di tiap episode
- Outro: teaser "Episode berikutnya: …"

## Identitas EP 01 (draft — fase 1.5): "Kubernetes yang nahan 10.000 request barengan"

| # | Pilihan | Untuk episode ini | Kenapa cocok |
|---|---|---|---|
| 1 | **Metafora sentral** | **gerbang tol waktu mudik** — request = mobil, pod = gardu tol, auto-scaling = gardu tambahan dibuka | relate banget buat orang Indonesia; beda dari klise "pelabuhan kontainer" |
| 2 | **Signature move** | gardu/pod **membelah jadi dua** (kayak sel) waktu antrean naik, nutup lagi waktu sepi | auto-scaling jadi kelihatan |
| 3 | **Signature color** | ungu `#7558F0` | beda dari coral (#01) |
| 4 | **Format hook** | **cold open di tengah aksi**: "Jam delapan malam. Sepuluh ribu orang buka aplikasi yang sama. Barengan." + banjir titik request | beda dari "angka dulu" (#01) |
| 5 | **Struktur** | format seri (masalah → keputusan → hasil) | beda dari "4 langkah" (#01) |
| 6 | **Komponen baru** | `particle_flow` (aliran titik request) · `toll_lanes` (gardu + antrean + membelah) · `arch_diagram` · `load_graph` (lonjakan traffic + pita auto-scale) | belum ada |

Sentuhan manusia:
- **Artefak asli:** bentuk arsitektur/angka asli yang disamarkan — puncak request, jumlah node/pod, region (tanya user)
- **Opini:** "Kubernetes di sini bukan buat gaya-gayaan — beban kayak gini emang butuh" (nyambung ke ide #05)
- **Kejutan:** jam 2 pagi gardunya nutup sendiri satu-satu → biayanya ikut turun (nyambung ke #01)
- **Ketidaksempurnaan:** hand note di diagram, satu mobil "nyelonong" pindah jalur
