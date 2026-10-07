# IDENTITY — Bongkar Arsitektur EP04: Monolith lama, dipecah jadi event-driven

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: qris-dua-detik · sebelumnya lagi: roadmap-cloud-engineer;
> episode seri sebelumnya: bongkar-ep03-serverless-big-data).

## Identitas seri (tetap tiap episode)
HUD `MUMEYONG · BONGKAR ARSITEKTUR · EP 04` · bumper judul · struktur Masalah → Keputusan → Diagram → Hasil →
recap · komponen andalan `arch_diagram`/`arch_node` · outro teaser episode berikutnya (EP05 legacy + container).

| # | Pilihan | Untuk episode ini | Beda dari video sebelumnya? |
|---|---|---|---|
| 1 | **Metafora sentral** | **kampung + kentongan pos ronda** — monolith = satu rumah gede (semua kerjaan satu atap, satu MCB); function = rumah kecil di satu gang; event = kentongan dipukul; private network = gang berpagar; NAT gateway = portal satu-satunya di ujung gang | ✓ (lari estafet · jalur KRL · dapur) |
| 2 | **Signature move** | **kentongan dipukul → gelombang bunyi menyebar sepanjang gang → jendela rumah yang "dengerin" nyala satu-satu, kerja, lalu gelap lagi.** Rumah yang nggak berkepentingan tetap gelap. | ✓ (freeze/slow-mo · kereta meluncur · kompor nyala-padam) |
| 3 | **Signature color** | teal `#0E9AAB` (tokens `CHAPTER[4]`) — lampu jendela, gelombang kentongan, portal | ✓ (ungu · oranye · oranye EP03); teal terakhir dipakai kenalan (6 video lalu) |
| 4 | **Format hook** | **klaim nyeleneh**: "Bagian terbaik dari aplikasi ini? Sebagian besar waktunya, dia tidur." — gang malam, semua jendela gelap, satu kentongan, *tok* → satu jendela nyala → gelap lagi | ✓ (freeze-frame · mitos dicoret · before/after) — format baru |
| 5 | **Struktur** | format seri (masalah → keputusan → diagram → hasil) | (pengecualian seri) |
| 6 | **Komponen baru** (`engine/components/kampung.py`) | `kentongan` (kentongan bambu digantung di tiang pos ronda, ayunan pukul) · `sound_rings` (gelombang bunyi menyebar) · `rumah` (rumah kecil: atap, jendela dengan lampu 0..1, papan nama, `zzz` kalau tidur) · `rumah_gede` (monolith: satu rumah, banyak kamar, satu MCB; bisa korslet → semua gelap, bisa "tutup renovasi") · `gang` (deretan rumah + jalan + pagar) · `portal` (NAT gateway: palang portal, panah keluar boleh / masuk ditolak) | ✓ |
| 7 | **Musik** | Eb · warm (`v.music`) — beda dari qris (D bright) & roadmap (A dreamy) | ✓ |

Metafora dipakai di: INTRO (gang malam, satu kentongan, satu jendela), MASALAH (rumah gede, lampu nyala semua, korslet →
gelap, renovasi dapur = tutup semua), KEPUTUSAN (rumah dipecah jadi gang rumah kecil, kentongan = event, signature move),
DIAGRAM (API → kentongan → 3 rumah function nyala barengan; dua gang AWS / Alibaba; pagar = private network; portal =
NAT gateway), HASIL (gang malam gelap = overhead turun; satu rumah korslet, tetangga tetap nyala), RECAP (pemukul
kentongan pergi tanpa nunggu).

## Sentuhan manusia
- **Artefak asli:** stack asli project (AWS Lambda · Alibaba Function Compute · private network · NAT gateway,
  multi-cloud). Angka **tidak ada → tidak ditampilkan**. Kalau ada screenshot daftar function / event rule
  (nama disamarkan) → bisa jadi bukti di L16–17 — **opsional, tanya user**.
- **Opini:** "Nggak semua monolith harus dipecah. Kalau dia sehat, biarin." (L25) — sikap yang berani di tengah hype
  microservices; nyambung ke ide #05.
- **Kejutan:** RECAP L24 — kamera ngikutin si pemukul kentongan: dia mukul, terus *jalan pergi* tanpa nengok, sementara
  di belakangnya rumah-rumah nyala sendiri (fire-and-forget).
- **Ketidaksempurnaan:** papan nama rumah tulisan tangan (Instrument Serif) & satu papan miring; hand note
  "ini monolith-nya" di rumah gede; satu lampu jendela kedip sekali sebelum nyala.

## Bookend
Hook (gang gelap, satu jendela nyala-mati) balik di RECAP: gang yang sama, tapi sekarang kita lihat siapa yang mukul
kentongan — dan dia nggak nunggu.

## Anti-generik checklist
- [x] 1–4 beda dari video sebelumnya (struktur = pengecualian seri)
- [x] ≥ 1 komponen baru (6)
- [ ] artefak asli — hanya nama stack asli; screenshot function list opsional (minta user)
- [x] opini di naskah (L25)
- [x] satu kejutan (pemukul kentongan pergi, L24)
- [x] metafora kepakai di ≥ 3 bab (semua bab)
