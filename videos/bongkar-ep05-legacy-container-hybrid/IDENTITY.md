# IDENTITY — Bongkar Arsitektur EP05: Legacy dan container, hidup berdampingan

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: bongkar-ep04-monolith-event-driven · sebelumnya lagi:
> qris-dua-detik).

## Identitas seri (tetap tiap episode)
HUD `MUMEYONG · BONGKAR ARSITEKTUR · EP 05` · bumper judul · struktur Masalah → Keputusan → Diagram → Hasil →
recap · komponen andalan `arch_node` · outro teaser episode berikutnya (EP06 Customer 360, milidetik).

| # | Pilihan | Untuk episode ini | Beda dari video sebelumnya? |
|---|---|---|---|
| 1 | **Metafora sentral** | **lahan kuliner: ruko lama + kios kontainer baru di satu lahan** — legacy = ruko lama (pelanggan setia, nggak bisa ditutup), container = kios kontainer (gampang ditambah/dipindah), SLB = satpam di satu-satunya pintu depan yang bagi rata pengunjung, Nginx = papan penunjuk arah, request = pengunjung | ✓ (kampung/kentongan · lari estafet) |
| 2 | **Signature move** | **papan arah split-flap berputar**: huruf-huruf tujuan flip satu-satu (`menu baru → KONTAINER`), dan aliran pengunjung langsung belok ikut papan | ✓ (kentongan + jendela nyala · freeze/slow-mo) |
| 3 | **Signature color** | hijau `#10A060` (tokens `CHAPTER[1]`) — papan arah kayak rambu, kios kontainer, panah rute | ✓ (teal · ungu); hijau terakhir war-tiket (4 video lalu) |
| 4 | **Format hook** | **pertanyaan spesifik**: "Gimana caranya aplikasi lama dan Kubernetes baru jalan barengan… tanpa user sadar?" — ruko & kontainer berdampingan, satu pengunjung jalan masuk dengan tanda tanya | ✓ (klaim nyeleneh · freeze-frame) |
| 5 | **Struktur** | format seri | (pengecualian seri) |
| 6 | **Komponen baru** (`engine/components/kuliner.py`) | `ruko` (ruko lama: rolling door, papan nama, kanopi garis) · `kios` (kios kontainer: rusuk bergelombang, jendela saji, kanopi) · `flip_sign` (papan arah split-flap: baris `rute → tujuan`, karakter flip berurutan) · `gapura` (satu pintu depan + pos satpam, lampu jalur kiri/kanan) · `visitor` (pengunjung kecil berjalan) | ✓ |
| 7 | **Musik** | C · dreamy (`v.music`) — beda dari EP04 (Eb warm) & qris (D bright) | ✓ |

Metafora dipakai di: INTRO (ruko + kontainer berdampingan, satu pengunjung bingung), MASALAH (lahan kuliner, tiga pintu,
satu kebanjiran), KEPUTUSAN (satu gapura + satpam = SLB, papan flip = Nginx), DIAGRAM (papan flip mini di node Nginx;
L19 papan diganti → rute pindah), HASIL (antrean rata di pintu, gapura dijaga), RECAP (papan flip terakhir, pengunjung
nggak sadar).

## Sentuhan manusia
- **Artefak asli:** stack asli project (SLB · Nginx · Kubernetes, legacy monolith tetap jalan). Angka **tidak ada →
  tidak ditampilkan**. Kalau ada potongan config Nginx (`location /…` dengan nama disamarkan) → bisa jadi bukti di L17
  — **opsional, tanya user**.
- **Opini:** "Migrasi itu nggak harus sekaligus. Yang lama boleh tetap hidup, asal pintunya satu." (L23–24)
- **Kejutan:** RECAP — papan flip berputar *sambil* pengunjung lagi jalan; dia belok ke kontainer tanpa berhenti
  sedikit pun. Kamera mundur: dari luar, cuma kelihatan satu gapura.
- **Ketidaksempurnaan:** satu huruf di papan flip nyangkut setengah sebelum jatuh; papan nama ruko tulisan tangan
  (Instrument Serif) dan sedikit miring.

## Bookend
Hook "tanpa user sadar dilayani yang mana" balik di RECAP: papan berganti di depan pengunjung, dan dia tetap jalan.

## Anti-generik checklist
- [x] 1–4 beda dari video sebelumnya (struktur = pengecualian seri)
- [x] ≥ 1 komponen baru (5)
- [ ] artefak asli — hanya nama stack asli; potongan config Nginx opsional (minta user)
- [x] opini di naskah (L23–24)
- [x] satu kejutan (papan berganti, pengunjung nggak sadar)
- [x] metafora kepakai di ≥ 3 bab (semua bab)
