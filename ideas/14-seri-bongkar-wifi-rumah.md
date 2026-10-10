# Seri: Bongkar WiFi Rumah (5 episode)

- **Status:** 🎬 seri jalan — EP01 ✅ tayang → [`videos/_arsip/wifi-ep01-lampu-los/`](../videos/_arsip/wifi-ep01-lampu-los/)
- **Pilar:** B (broad) · **Format:** QUICK
- **Slug:** wifi-ep<NN>-<nama-episode>
- **Seri:** Bongkar WiFi Rumah — pengganti slot seri setelah Bongkar Arsitektur tamat
- **Durasi target:** 60–75 s per episode (lewat 1 menit buat payout)
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Tiap episode: satu hal yang kamu lihat sendiri di WiFi rumah → apa yang sebenernya kejadian di baliknya → apa yang bisa kamu lakuin.

## Kenapa seri ini
Keluhan internet rumah paling ramai di 2026: gangguan massal IndiHome 22 Jan 2026 (Downdetector 4.319 laporan, ~82% "nggak bisa
akses internet", gejala: WiFi tersambung tapi nggak bisa dipakai), surat pembaca soal **lampu LOS merah** + mati 24–36 jam
(Apr–Mei 2026), dan "lemot pas hujan / disuruh restart tapi percuma". Sumber: Kompas, Liputan6, Media Konsumen, Mojok.

## Episode
| EP | Judul | Hook (draft) | Catatan |
|---|---|---|---|
| 01 | **Lampu modem merah "LOS" itu artinya apa?** | foto lampu modem: PON kedip, LOS merah — "Lampu ini ngasih tahu rusaknya di rumahmu atau di jalan." | ⭐ mulai di sini · save-able |
| 02 | **WiFi connected, tapi no internet. Kok bisa?** | ikon WiFi penuh + tanda seru | router ↔ ISP; bisa dinaikin cepat waktu ada gangguan massal (slot berita #09) |
| 03 | **WiFi lemot pas hujan: mitos atau beneran?** | "Tiap hujan, internetmu ikut lemot?" | ⚠️ cek fakta — biasanya air masuk kabel drop / ODP / listrik, bukan hujannya |
| 04 | **Restart router beneran ngefek?** | kutipan asli: "disuruh restart tapi percuma" | restart di production juga sering "obat", kenapa itu bukan solusi |
| 05 | **Kenapa internet lemot tiap jam 8 malam?** | jam 20.00, semua rumah nyala | peak hour + oversubscription; metafora tekanan air PDAM |

## Format tetap tiap episode
Hook (gejala yang penonton kenal) → **Yang kamu lihat** → **Yang sebenernya kejadian** → **Yang bisa kamu lakuin** → outro teaser EP berikutnya

## Identitas SERI (tetap di semua episode)
- HUD: `MUMEYONG · BONGKAR WIFI RUMAH` + `EP 01` di kanan atas
- Bumper pakai `series_bumper` (judul seri + nomor EP)
- Sudut "cuma Mumeyong": cara orang infra nge-debug network — **cek dari layer paling dekat dulu** (HP → router → kabel → ISP)
- Tiap episode: motion signature beda (STYLE §6d). EP01 usul: `silk` + `ink` + `Morph`

## Identitas EP 01 (draft)
- Metafora: **dashboard mobil** — tiap lampu = peringatan satu bagian perjalanan dari jalan ke HP-mu
- Signature move: satu lampu mati → kamera ngikutin kabel mundur sampai titik putusnya
- Komponen baru (calon): `modem` (lampu PON/LOS/INTERNET/WLAN) · `fiber_path` (rumah → tiang → ODP → STO)

## Catatan
- Jangan sebut ISP secara negatif/menjelekkan — jelasin mekanismenya, bukan nyalahin merek.
- ⚠️ Cek fakta arti lampu per merek modem (ZTE/Huawei/FiberHome beda label).
