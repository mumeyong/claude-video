# IDENTITY — Bongkar Arsitektur EP02: Pindahin big data ke cloud, tanpa satu byte hilang

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: bongkar-ep01-kubernetes-10k).

## Identitas seri (tetap tiap episode)
HUD `MUMEYONG · BONGKAR ARSITEKTUR · EP 02` · bumper judul · struktur Masalah → Keputusan → Diagram → Hasil →
recap · komponen andalan `arch_diagram` · outro teaser episode berikutnya.

| # | Pilihan | Untuk episode ini | Beda dari EP01? |
|---|---|---|---|
| 1 | **Metafora sentral** | **pindahan perpustakaan yang masih buka** — buku = record, peminjaman = data yang berubah, katalog = checksum | ✓ (gerbang tol) |
| 2 | **Signature move** | **pasangan mengunci**: baris lama & baris baru meluncur berdampingan, hash-nya cocok → *klik*, terkunci hijau ✓ | ✓ (gardu membelah) |
| 3 | **Signature color** | hijau `#10A060` (match / verified) | ✓ (ungu) |
| 4 | **Format hook** | **mitos dicoret**: `~Copy, paste, beres~.` → "Nggak segampang itu." | ✓ (cold open) |
| 5 | **Struktur** | format seri | (pengecualian seri) |
| 6 | **Komponen baru** | `twin_table` (lama vs baru, hash + lock) · `sync_pipe` (jalur full copy + aliran incremental) · `cutover_switch` (tuas pindah jalur + jalur rollback) · `bookshelf` (rak buku yang dikemas per kardus) | ✓ |

Metafora dipakai di: INTRO (kardus jatuh = record hilang), MASALAH (perpustakaan masih buka), KEPUTUSAN (dua tahap
pindahan), DIAGRAM (katalog dicocokkan), HASIL (gedung baru dibuka, jalan balik disiapin), RECAP.

## Sentuhan manusia
- **Artefak asli:** fakta portfolio (legacy → Alibaba Cloud, zero data loss). Ukuran data/durasi **tidak ada → tidak ditampilkan**.
- **Opini:** "Kalau belum bisa dibuktiin sama, belum boleh pindah." (L22)
- **Kejutan:** satu baris yang kelihatan cocok ternyata beda **satu karakter** di checksum → merah → di-sync ulang → hijau (L16)
- **Ketidaksempurnaan:** satu buku "nyelip" keluar dari kardus lalu ditangkap; hand note di checksum

## Anti-generik checklist
- [x] 1–4 beda dari video sebelumnya (struktur = pengecualian seri)
- [x] ≥ 1 komponen baru (4)
- [ ] artefak asli — hanya fakta portfolio; **minta user** angka/screenshot kalau ada di kemudian hari
- [x] opini di naskah (L22)
- [x] satu kejutan (L16)
- [x] metafora kepakai di ≥ 3 bab
