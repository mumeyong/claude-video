# IDENTITY — Bongkar Arsitektur EP06: Project 360

> Fase 1.5 · dicek ke `ideas/REGISTRY.md` (video sebelumnya: bongkar-ep05-legacy-container-hybrid · sebelumnya lagi:
> bongkar-ep04-monolith-event-driven).

## Identitas seri (tetap tiap episode)
HUD `MUMEYONG · BONGKAR ARSITEKTUR · EP 06` · bumper judul · struktur Masalah → Keputusan → Diagram → Hasil →
recap · komponen andalan `arch_node` · outro teaser episode terakhir (EP07 Azure AI Infrastructure).

| # | Pilihan | Untuk episode ini | Beda dari video sebelumnya? |
|---|---|---|---|
| 1 | **Metafora sentral** | **berkas di loket-loket + satu stopmap** — data nasabah = lembar berkas yang kesebar di loket tiap perusahaan (tabungan, asuransi, kredit, sekuritas); nyari gambaran utuh = keliling fotokopi; Project 360 = satu stopmap yang selalu siap di meja CS; keamanan = penjagaan berlapis di sekeliling map | ✓ (lahan kuliner · kampung) |
| 2 | **Signature move** | **lembar-lembar terbang dari loket berbeda dan nyelip ke satu stopmap — map menutup "klik"**, tab-nya nyala ungu | ✓ (papan flip · kentongan) |
| 3 | **Signature color** | ungu `#7558F0` (tokens `CHAPTER[3]`) — stopmap, cincin 360, lapisan keamanan | ✓ (hijau · teal); ungu terakhir qris (3 video lalu) |
| 4 | **Format hook** | **cold open di tengah aksi**: meja CS, nasabah duduk, monitor buka jendela aplikasi satu-satu, nasabah ditanya ulang | ✓ (pertanyaan spesifik · klaim nyeleneh) |
| 5 | **Struktur** | format seri | (pengecualian seri) |
| 6 | **Komponen baru** (`engine/components/berkas.py`) | `lembar` (lembar berkas: strip warna sumber, judul, garis isi, sudut terlipat) · `stopmap` (map snelhecter: buka/tutup, tab label, tepi lembar warna-warni) · `meja_cs` (meja CS + monitor + CS + nasabah, isi layar = callback) · `profile_360` (kartu profil: avatar + cincin 360 yang terisi per sumber, chip produk, titik LIVE) · `lapis` (lapisan keamanan konsentris, tiap lapis label) · `id_card` (kartu pegawai di-tap ke reader, LED hijau) | ✓ |
| 7 | **Musik** | G · tense (`v.music`) — cold open, data sensitif; beda dari EP05 (C dreamy) & EP04 (Eb warm) | ✓ |

Metafora dipakai di: INTRO (meja CS, jendela satu-satu → satu map), MASALAH (loket-loket, keliling fotokopi, lembar
bocor), KEPUTUSAN (lembar terbang ke stopmap — signature move; map dijaga berlapis), DIAGRAM (map di tengah, tiga lapis di
sekelilingnya), HASIL (map dibuka = profil 360 di satu layar), RECAP (meja CS lagi — pertanyaan ulang dicoret).

## Sentuhan manusia
- **Artefak asli:** stack asli project (Docker · ECS · WAF · VPN · IDaaS, high availability). Angka **tidak ada →
  tidak ditampilkan**. Screenshot dashboard Project 360 (data disamarkan total) → opsional, **tanya user** — hati-hati
  data nasabah; default: jangan.
- **Opini:** "Makin lengkap datanya, makin tebal juga penjaganya." (L23) + "bukan soal ngumpulin data sebanyak-banyaknya"
  (L21).
- **Kejutan:** RECAP — balik ke meja CS yang sama dari hook; gelembung "NIK-nya berapa, Pak?" muncul… lalu dicoret
  sebelum CS sempat ngomong.
- **Ketidaksempurnaan:** satu lembar nyangkut miring di mulut map sebelum masuk; tulisan tangan "jangan difotokopi" di
  tab map; nama nasabah disensor pakai spidol.

## Bookend
Cold open (nasabah nunggu, ditanya ulang) balik di RECAP: meja yang sama, pertanyaannya dicoret.

## Anti-generik checklist
- [x] 1–4 beda dari video sebelumnya (struktur = pengecualian seri)
- [x] ≥ 1 komponen baru (6)
- [ ] artefak asli — hanya nama stack asli (data nasabah sensitif → screenshot default tidak)
- [x] opini di naskah (L21, L23)
- [x] satu kejutan (pertanyaan dicoret, L22)
- [x] metafora kepakai di ≥ 3 bab (semua bab)
- [x] hero bukan gembok + perisai: keamanan = lapisan penjagaan di sekeliling map, bukan ikon gembok
