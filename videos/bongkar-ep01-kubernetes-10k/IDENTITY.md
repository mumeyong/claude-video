# IDENTITY — Bongkar Arsitektur EP01: Kubernetes yang nahan 10.000 request barengan

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: hemat-14k-cloud).

## Identitas seri (tetap tiap episode)
HUD `MUMEYONG · BONGKAR ARSITEKTUR · EP 01` · bumper judul 1,5 s · struktur Masalah → Keputusan → Diagram →
Hasil → recap · komponen andalan `arch_diagram` · outro teaser episode berikutnya.

| # | Pilihan | Untuk episode ini | Beda dari #01? |
|---|---|---|---|
| 1 | **Metafora sentral** | gerbang tol waktu mudik — request = mobil, pod = gardu, Kubernetes = petugas tol | ✓ (tagihan bocor) |
| 2 | **Signature move** | gardu **membelah jadi dua** saat antrean naik, **menutup** saat sepi | ✓ (odometer) |
| 3 | **Signature color** | ungu `#7558F0` | ✓ (coral) |
| 4 | **Format hook** | cold open di tengah aksi + banjir titik request | ✓ (angka dulu) |
| 5 | **Struktur** | format seri | ✓ (4 langkah) |
| 6 | **Komponen baru** | `particle_flow`, `toll_plaza`, `arch_diagram`, `load_graph`, `stack_layers` | ✓ |

Metafora dipakai di: INTRO (banjir mobil/titik), MASALAH (antrean & putar balik), KEPUTUSAN (petugas tol),
DIAGRAM (gardu dibuka/diganti), HASIL (gardu nutup jam 2 pagi), RECAP.

## Sentuhan manusia
- **Artefak asli:** angka 10.000+ request barengan; bentuk alur LB → pod → node. (Node/pod count tidak ada → tidak ditampilkan.)
- **Opini:** "Kubernetes bukan gaya-gayaan. Emang butuh."
- **Kejutan:** jam 2 pagi gardu nutup sendiri satu-satu → nyambung ke biaya (#01)
- **Ketidaksempurnaan:** satu mobil nyelonong pindah jalur; hand note di diagram

## Anti-generik checklist
- [x] 1–5 beda dari video sebelumnya
- [x] ≥ 1 komponen baru
- [x] artefak asli (10.000+), node count sengaja nggak dikarang
- [x] opini di naskah (L24)
- [x] satu kejutan (L20)
- [x] metafora kepakai di ≥ 3 bab
