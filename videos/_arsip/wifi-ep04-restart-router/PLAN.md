# PLAN — Restart router beneran ngefek? (Bongkar WiFi Rumah EP 04)

> Fase 1.5. Dua video terakhir di REGISTRY: ai-butuh-cloud-engineer (panggung hajatan · lampu sorot nyisir · ungu ·
> pengalaman sendiri · satu panggung atas → bawah · wipe + Rig · marimba D bright/wood · flat-big) dan ai-gratis-siapa-bayar
> (struk Rp0 · struk dibalik · hijau · mitos dicoret lewat benda · ink + Rig/focus_pull · cinematic E tense/mech · paper-big).
> EP sebelumnya di seri: EP 03 (talang bocor · satu tetes · teal · pertanyaan spesifik · rise + Rig/sheet · lofi G/glass).
> Pilihan 1–5 + material + musik beda dari dua video terakhir. Seri: HUD/kicker `BONGKAR WIFI RUMAH · EP 04`,
> `series_bumper`, format lihat → kejadian → lakuin; pos satpam EP 02 jadi rumah buku tamunya, modem EP 01 balik di bab 02.

<!-- registry
pilar: B
metafora: buku tamu pos satpam — router = satpam yang nyatet tiap koneksi satu baris (NAT table); halaman penuh → tamu baru nunggu; restart = halamannya disobek, buku bersih; masalah di jalan (kabel, ISP, sambungan basah) nggak ikut kesobek
signature: baris-baris buku tamu keisi cepat sampai penuh → halaman kanan disobek dari jilidan dan jatuh → kertas bersih; tiap restart ninggalin sobekan di jilidan (sobekan numpuk = gejala)
look: classic + paper-big
color: merah `#F03B4F`
hook: kutipan sehari-hari ("Udah dicoba restart, Kak?" — kata CS) → "kadang sembuh, kadang buang waktu"
struktur: format seri lewat satu buku: isi buku (kenapa restart nolong) → di luar buku (kapan percuma, 3 episode) → sekali vs tiap hari (sobekan numpuk)
komponen: buku_tamu
musik: garage F warm 128 · sfx soft
durasi: 75
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **classic + Apple craft** — nggak ada reel moves |
| Material (STYLE §6g) | **paper, big** — buku tamu = kertas + sampul karton merah: `v.stage` paper ground (tint merah), buku ngisi ± 85 % lebar × 38 % tinggi frame (s 1,0–1,15), masuk full-bleed dari bawah (`bleed=True`); `v.finish` grain paper. Sebelumnya: flat-big (ai-butuh-cloud-engineer). paper-big terakhir 2 video lalu, nggak berturut-turut |
| Motion (STYLE §6d + §6f) | reveal `rise` (headline per baris) · glue: buku = persistent hero `Rig` + `depth_swap` (bab 01: buku mundur kecil, tiga kartu episode maju; bab 02: kartu mundur, modem maju) · exit quiet · spring `hero` buat buku, `smooth` buat kartu/tag, `snappy` cuma stempel + centang — beda dari wipe + Rig (panggung) dan ink + focus_pull (struk) |
| Apple craft (§6f) | leader: INTRO = kartu chat CS → buku · 00 = baris buku (lalu sobekan) · 01 = kartu episode satu per satu · 02 = modem (lampu mati → nyala) lalu sobekan di jilidan · RECAP = buku + stempel. Hold terpanjang: L06 (NAT table, dolly) + L20 (gejala, dolly) · tempo slow–slow–snap: snap di L09 (halaman disobek, thud) dan L14 (sobek lagi, jalannya tetap rusak) · kontinuitas: buku nggak pernah keluar frame dari L03 sampai RECAP (Rig), cuma mundur di belakang kartu/modem |
| Metafora | buku tamu satpam: INTRO (buku muncul di L03), 00 (baris, penuh, sobek), 01 (buku diganti, jalan tetap rusak), 02 (sobekan numpuk di jilidan), RECAP (jilidan penuh sobekan = gejala) |
| Signature move | **halaman disobek**: halaman kanan keangkat dari jilidan, miring, jatuh keluar frame (torn_flight), kertas bersih di bawahnya — L09, L14, L15 (restart sekali), L17 (cepat berulang → sobekan numpuk) |
| Color · hook · struktur | merah `#F03B4F` (sampul buku, stempel PENUH/GEJALA, sobekan) · kutipan sehari-hari · format seri lewat satu buku |
| Suara (STYLE §7) | style `garage` · key F · mood warm · 128 BPM · sfx kit `soft` (kertas, pensil) — sebelumnya marimba/wood, cinematic/mech |
| Komponen baru (1, QUICK) | `buku_tamu` (buku tamu terbuka: sampul karton, halaman kiri = judul + meter memory, halaman kanan = baris tamu yang nge-ink; `tear` nyobek halaman kanan, `stubs` = sobekan numpuk di jilidan, `full`/`wait` = baris antre) — reuse `modem` (EP 01), `stempel` (kasir), `series_bumper`, `pop_tag`, `note`, `check_badge` |
| Sentuhan manusia | opini/pengakuan: server production juga "sembuh" abis restart → kalau rutin itu gejala (L19–L20) · kejutan: halaman disobek di L09 · ketidaksempurnaan: stempel PENUH miring, tulisan tangan di buku, sobekan yang nggak rapi · artefak: — (opsional: foto modem/router rumah user → assets/) |

## Komposisi per bab (STYLE §6b)
| Bab | Hero (leader) | Layout | Kamera | Punch / transisi (kontinuitas) |
|---|---|---|---|---|
| INTRO | kartu chat CS "Udah dicoba restart, Kak?" (L01) → buku tamu full-bleed shrink (L03) | object + hand note → centered hero | dolly hold L02 | buku naik di "tamu" · bumper seri nutupin ganti bab |
| 00 · BUKU TAMU | buku tamu besar, baris nge-ink satu per satu → penuh cepat, stempel PENUH, baris antre "nunggu" | full-width hero (buku) + tag | dolly L06, cut L09 | snap L09: halaman disobek, thud, kertas bersih |
| 01 · KAPAN PERCUMA | tiga kartu episode miring (LOS · ISP · basah) maju di depan buku yang mundur (depth_swap), tiap kartu dicap "DI LUAR" | stacked/tilted cards | dolly hold L13 | L14: buku di belakang sobek lagi, kartu tetap dicap |
| 02 · YANG BISA KAMU LAKUIN | modem (lampu mati → nyala, L15) → centang (L16) → buku balik, sobekan numpuk di jilidan (L17) | centered hero (modem) → hero buku + tag | cut L15, dolly L18 | sobekan numpuk cepat di L17 (tiap hari) |
| RECAP | buku tamu di gelap, jilidan penuh sobekan, stempel GEJALA (L20) | hero + headline | dolly L20 | stempel GEJALA |
| OUTRO | `standard_outro` + teaser EP 05 (jam 8 malam) | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L05: isi baris generik (HP · video, laptop · meeting, TV · streaming) — nggak ada merek app, nggak ada jumlah baris yang "resmi".
- L07: meter MEMORY di halaman kiri = gambar tangan, tanpa angka/persen.
- L15: "tunggu sebentar" — sengaja tanpa detik (lama nyala ulang beda tiap modem).
- L18: dua tag — "update firmware" · "minta ganti modem ke ISP".
