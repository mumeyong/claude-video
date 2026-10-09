# IDENTITY — Bongkar Arsitektur EP07: Fondasi buat training AI di Azure (episode terakhir)

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: bongkar-ep06-project-360 · sebelumnya lagi:
> bongkar-ep05-legacy-container-hybrid).

## Identitas seri (tetap tiap episode)
HUD `MUMEYONG · BONGKAR ARSITEKTUR · EP 07` · bumper judul · struktur Masalah → Keputusan → Diagram → Hasil →
recap · komponen andalan `arch_node` · **outro = penutup seri** (7 episode dicentang + ajakan komentar buat lanjutan).

| # | Pilihan | Untuk episode ini | Beda dari video sebelumnya? |
|---|---|---|---|
| 1 | **Metafora sentral** | **atlet bulu tangkis: pelatnas vs pertandingan** — model AI = atlet; training = latihan (pukulan diulang, mesin pelontar, alat berat = GPU, cuma sementara); inference = tanding (satu pukulan, cepat, kapan aja); AKS = pelatih yang ngatur jadwal lapangan; cross-cloud = bisa tanding di GOR mana aja | ✓ (stopmap · lahan kuliner) |
| 2 | **Signature move** | **kok melengkung lewat net — tiap kali mendarat, satu titik repetisi nyala** (training); di tanding: satu smash, langsung poin | ✓ (lembar → map · papan flip) |
| 3 | **Signature color** | oranye `#E8861A` (tokens `CHAPTER[2]`) — lampu lapangan, GPU nyala, kok | ✓ (ungu · hijau); oranye terakhir EP03 (4 video lalu) |
| 4 | **Format hook** | **mitos dicoret**: gudang GPU nyala semua → "Nggak juga." dicoret | ✓ (cold open · pertanyaan spesifik) |
| 5 | **Struktur** | format seri | (pengecualian seri) |
| 6 | **Komponen baru** (`engine/components/badminton.py`) | `gpu_card` (kartu GPU: kipas berputar, nyala/mati) · `lapangan` (lapangan side-view: garis, net, lampu sorot di atas) · `pemain` (atlet + raket, ayunan) · `shuttle` + `shuttle_arc` (kok + lintasan melengkung) · `pelontar` (mesin pelontar kok, latihan drill) · `rep_dots` (titik repetisi) · `jadwal` (papan jadwal pelatih: blok latihan / tanding di timeline, playhead) · `gor` (gedung GOR = cloud) | ✓ |
| 7 | **Musik** | E · bright (`v.music`) — sporty, finale; beda dari EP06 (G tense) & EP05 (C dreamy) | ✓ |

Metafora dipakai di: MASALAH (latihan vs tanding, rebutan satu lapangan), KEPUTUSAN (dua lapangan + pelatih/jadwal),
DIAGRAM (GPU pool = lapangan latihan, inference pool = lapangan tanding, GOR = cloud), HASIL (lampu lapangan latihan cuma
nyala pas jadwal), RECAP (atlet juara latihan pas perlu). Hook pakai gudang GPU (bookend di recap).

## Sentuhan manusia
- **Artefak asli:** stack asli project (Azure · AKS · GPU compute, training + inference, cross-cloud). Angka **tidak ada
  → tidak ditampilkan**. Screenshot node pool AKS (nama disamarkan) → opsional, **tanya user**.
- **Opini:** "Atlet juara nggak latihan dua puluh empat jam. Dia latihan pas perlu." (L23) + "bukan soal punya GPU paling
  banyak" (L21).
- **Kejutan:** RECAP — gudang GPU dari hook muncul lagi, semua nyala… lalu padam satu-satu sampai tinggal yang lagi
  latihan; lampu lapangan tanding tetap nyala kecil.
- **Ketidaksempurnaan:** satu kok nyangkut di net sebelum jatuh; jadwal pelatih tulisan tangan (Instrument Serif) dengan
  satu jadwal dicoret.

## Bookend
Hook "GPU segudang, nyala terus" balik di RECAP: gudang yang sama, padam sampai tinggal yang perlu.

## Penutup seri
Outro: kartu "SERI BONGKAR ARSITEKTUR · SELESAI" dengan EP 01–07 dicentang satu-satu + "Mau lanjutan? Tulis di komentar".

## Anti-generik checklist
- [x] 1–4 beda dari video sebelumnya (struktur = pengecualian seri)
- [x] ≥ 1 komponen baru (8)
- [ ] artefak asli — hanya nama stack asli; screenshot node pool opsional (minta user)
- [x] opini di naskah (L21, L23)
- [x] satu kejutan (gudang GPU padam)
- [x] metafora kepakai di ≥ 3 bab (semua bab)
- [x] hero bukan otak/robot AI: AI = atlet bulu tangkis, GPU = alat latihan
