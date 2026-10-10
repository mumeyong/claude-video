# PLAN — Foto yang kamu kirim di WhatsApp, sebenernya lewat mana?

> Fase 1.5. Dua video terakhir: kubernetes-bukan-jawaban (pelabuhan + kurir/paket · crane · hijau · mitos dicoret ·
> versus → checklist · garage/mech) dan WiFi EP 02 (komplek + pos satpam · palang · oranye · klaim nyeleneh ·
> perjalanan request · marimba/wood). Draft ide (ekspedisi + paket) dibuang: kurir + paket baru aja dipakai.
> Baris terakhir REGISTRY nggak ada `look reel` → video ini **full reel look** (STYLE §6e).

<!-- registry
pilar: B
metafora: loker penitipan — foto = kotak yang dikunci di HP-mu, server = dinding loker + penjaganya, key nggak ikut ke loker (lewat pesan chat end-to-end)
signature: pintu loker mengayun (heavy) nelen / ngeluarin kotak, sementara key jalan sendiri di garis titik-titik hijau — dua jalur yang ketemu di HP temenmu
look: reel
color: terracotta `#D6785C`
hook: timestamp spesifik (jam 21.04, "sebelum centang dua")
struktur: dua jalur: kotak lewat loker · key lewat chat → ketemu di HP penerima (+ kasus offline)
komponen: loker, kotak, kunci, centang, foto
musik: cinematic G dreamy 96 · sfx glass
durasi: 74
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **reel**: `v.ground` paper, `v.hud = False` + `viewfinder` (tag "tech sehari-hari"), `smear_words` statements, `iris` antar bab, `float_chips`, `highlight_phrase`, `count_pill`-free (nggak ada angka), satu `verb_slam` (recap), `end_card` + follow click. Pengecualian §8 reel berlaku (center, hijau/world colors, hard cut). |
| Motion (STYLE §6d) | spring `heavy` (pintu loker, kotak) · reveal `smear_words` (reel) · glue persistent hero `Rig` (kotak: HP → loker → HP temen) · exit reel (scale +30% blur) — beda set dari kubernetes (snappy · blur · Rig+bento · blur) |
| Metafora | loker penitipan: 00 (kotak dikunci di HP), 01 (kotak masuk loker #05, penjaga pegang kotak bukan key), 02 (key lewat jalan lain, kotak diambil dari loker), 03 (kotak nunggu di loker pas offline), RECAP (penjaga loker) |
| Signature move | pintu loker mengayun pakai `heavy` spring: nelen kotak (01), dibuka paksa → data acak (01), ngeluarin kotak (02, 03). Key = garis titik-titik hijau yang nggak pernah lewat loker |
| Color · hook · struktur | terracotta `#D6785C` (REEL_WORLDS security: kotak, loker, rute kotak) + `reel_green` (rute key, iris) · timestamp spesifik · dua jalur |
| Suara (STYLE §7) | style `cinematic` · key G · mood dreamy · 96 BPM · sfx kit `glass` (app/UI) — kubernetes garage/mech, EP 02 marimba/wood |
| Komponen baru (QUICK) | `components/loker.py`: `loker` (dinding loker + pintu ayun + nomor), `kotak` (kotak terkunci, tutup + lubang key), `kunci` (key), `centang` (✓ / ✓✓ digambar), `foto` (foto contoh + mode data acak) — reuse `phone`, reel.py |
| Sentuhan manusia | artefak: urutan nyata dari WhatsApp Security Whitepaper (key sekali pakai, pointer, centang) · opini: "ini bagian yang aku suka" (L10) · kejutan: key nggak ikut ke loker · ketidaksempurnaan: hand note miring "nggak bisa dibuka" + kotak sedikit miring di loker |

## Komposisi per bab (STYLE §6b)
| Bab | Hero | Layout | Kamera | Punch / transisi |
|---|---|---|---|---|
| INTRO | HP dengan bubble foto "21.04 ✓" → foto keluar dan muter (keliling) | timestamp raksasa smear → HP center | push-in ke bubble di L02 | "21.04" smear · `highlight_phrase` "nggak bisa lihat" · `iris` open terracotta |
| 00 · DIKUNCI DI HP | HP besar: foto → key muncul → masuk kotak, tutup, key muter, kotak (Rig) lepas | centered hero | push-in ke key (L05) | `iris` close · key pop · lock click |
| 01 · DITITIP DI LOKER | dinding loker 3 × 3 full width, kotak terbang masuk #05 (tengah) | full-width grid | push-in ke #05 (L09) | pintu heavy · chips "kotak ✓ / key ✗" · data acak (punch) |
| 02 · JALAN LAIN | peta dua jalur: HP-mu → loker → HP temen (terracotta) vs key lewat bubble chat (hijau titik-titik) | diagram dua jalur | key route follow → reset | `highlight_phrase` "aku suka" · ✓ lalu ✓✓ besar · foto muncul |
| 03 · KALAU OFFLINE | satu pintu loker close-up + HP temen redup "offline" → "online" | object + side phone | pull-out pas online | pintu kebuka, kotak meluncur ke HP |
| RECAP | `verb_slam` KUNCI · TITIP · AMBIL → dua kartu: kotak ✓ / key ✗ + bubble hook balik dengan ✓✓ | pure typography → kartu | drift | verb slam (sekali per video) |
| OUTRO | `end_card` + follow click (brand) | centered | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01 / RECAP: bookend — bubble "21.04" yang sama, awalnya ✓, di recap ✓✓.
- L05: label `key` (English), chip "sekali pakai". Jangan tulis "kunci" di layar.
- L09: data acak = grid karakter mono seeded (bukan matrix code hijau — banned) di dalam kotak.
- L12: chip "end-to-end" di bubble yang bawa key + "#05".
- L13: ✓ pas bubble sampai node server, ✓✓ pas sampai HP temen (abu-abu, bukan biru — biru = dibaca).
- Pertanyaan terbuka: berapa lama kotak boleh nunggu di loker kalau penerima offline terus? (sengaja nggak disebut).
