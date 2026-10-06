# IDENTITY — Bongkar Arsitektur EP03: Ganti stack big data jadi serverless

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: bongkar-ep02-big-data-migration, sebelumnya lagi:
> bongkar-ep01-kubernetes-10k).

## Identitas seri (tetap tiap episode)
HUD `MUMEYONG · BONGKAR ARSITEKTUR · EP 03` · bumper judul · struktur Masalah → Keputusan → Diagram → Hasil →
recap · komponen andalan `arch_diagram` · outro teaser episode berikutnya (EP04 monolith → event-driven).

| # | Pilihan | Untuk episode ini | Beda dari EP02 / EP01? |
|---|---|---|---|
| 1 | **Metafora sentral** | **dapur sendiri vs cloud kitchen** — node legacy = dapur sendiri (kompor dirawat, gas dibeli walau sepi), serverless = cloud kitchen (kompor nyala pas ada pesanan), job = tiket pesanan, data = bahan, Paimon = pantry bersama, Airflow = rel tiket / urutan masak | ✓ (perpustakaan / gerbang tol) |
| 2 | **Signature move** | **kompor nyala-padam ikut pesanan**: tiket jatuh ke kompor → api *fwoosh* nyala; masakan selesai → api mengecil sampai hilang total (nggak ada pilot light). Di dapur lama apinya nyala terus, walau kosong. | ✓ (hash lock / gardu membelah) |
| 3 | **Signature color** | oranye api `#E8861A` (tokens `CHAPTER[2]` / `CHIP["orange"]`) | ✓ (hijau / ungu); beda jelas dari coral `#EB6A4A` (hemat-14k, 3 video lalu) — oranye ini lebih kuning |
| 4 | **Format hook** | **before/after**: layar terbelah — kiri `Dulu` node + kunci pas + jam berdetak, kanan `Sekarang` kosong bersih → "Sama sekali." | ✓ (mitos dicoret / cold open) |
| 5 | **Struktur** | format seri | (pengecualian seri) |
| 6 | **Komponen baru** | `flame` + `burner` (kompor + api dengan intensitas 0–1, nyala/padam) · `oven` (batch) · `server_rack` (LED kedip, pensiun = abu-abu) · `order_ticket` + `ticket_rail` (tiket pesanan = job, digantung di rel, bisa tulisan tangan) · `dag_flow` (Airflow DAG: kotak task nyala berurutan + panah) · `lake_pantry` (rak/tabel Paimon di tengah, diambil dua jalur: streaming & batch) | ✓ |

Metafora dipakai di: INTRO (before/after: dapur berantakan vs kosong), MASALAH (dapur sendiri, api nyala terus, tiket
numpuk pas membludak), KEPUTUSAN (lepas dapur → cloud kitchen, kompor nyala pas ada tiket), DIAGRAM (Flink = kompor
cepat streaming, MaxCompute = oven batch besar, Paimon = pantry bersama, Airflow = rel tiket), HASIL (dapur sepi
tengah malam, nggak ada yang jaga), RECAP (kejutan: dinding dapur dibuka → server tetap ada).

## Sentuhan manusia
- **Artefak asli:** nama stack asli dari project (Flink · MaxCompute · Paimon · Airflow, Alibaba Cloud). Angka
  **tidak ada → tidak ditampilkan**. Kalau ada screenshot Airflow DAG (nama task disamarkan), bisa jadi
  bukti di L16 — **opsional, tanya user**.
- **Opini:** "Server-nya tetap ada. Cuma, bukan kamu yang ngurus." (L21) + "kamu urus resepnya, bukan mesinnya" (L11)
- **Kejutan:** RECAP L20–21 — kamera mundur dari cloud kitchen, dinding belakang kebuka → ternyata ada rak server
  raksasa di baliknya. Server-nya tetap ada, punya orang lain.
- **Ketidaksempurnaan:** tiket pesanan tulisan tangan (Instrument Serif), satu tiket miring & nyangkut sebentar di
  rel sebelum jatuh; hand note "ini node legacy →" di dapur lama.

## Bookend
Hook before/after (kiri dijagain / kanan kosong) balik di RECAP: sisi kanan yang "kosong" dibuka → server di baliknya.

## Anti-generik checklist
- [x] 1–4 beda dari video sebelumnya (struktur = pengecualian seri)
- [x] ≥ 1 komponen baru (4)
- [ ] artefak asli — hanya nama stack asli; screenshot Airflow DAG opsional (minta user)
- [x] opini di naskah (L11, L21)
- [x] satu kejutan (server di balik dinding, L20–21)
- [x] metafora kepakai di ≥ 3 bab (semua bab)
