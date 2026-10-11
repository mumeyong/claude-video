# PLAN — 5 pertanyaan interview cloud yang selalu aku tanya

> Fase 1.5. Dua video terakhir: jalur-karier-cloud (skill tree · cabang menjalar + ring charge · merah · before/after
> kartu nama · kronologis · classic+reel · ambient/soft) dan foto-whatsapp-lewat-mana (loker penitipan · pintu loker
> heavy · terracotta · timestamp spesifik · dua jalur · **look reel** · cinematic/glass).
> Baris terakhir REGISTRY = `look classic+reel` (bukan `look reel`) → video ini **full reel look** (STYLE §6e).
> Draft identitas di ideas/13 dipakai (kartu kuis · teal · kuis langsung · 5 kartu). Flip-nya beda dari kartu nama
> jalur-karier (itu putar samping, sekali, di hook): di sini kartu dibalik **ke atas** (sumbu horizontal) setelah
> ring 3 detik habis — dan itu signature yang balik di tiap bab.

<!-- registry
pilar: C
metafora: tumpukan kartu kuis (flashcard) di meja interview — tiap pertanyaan satu kartu, di baliknya "yang aku cari", bukan jawaban textbook
signature: ring hitung mundur 3 · 2 · 1 habis → kartu dibalik ke atas (snappy), tulisan tangan teal muncul di baliknya; kartu selesai ditumpuk miring di kiri
look: reel
color: teal `#0E9AAB`
hook: kuis langsung ke penonton ("jawab dalam tiga detik")
struktur: kuis 5 kartu (pertanyaan → timer → balik kartu) → satu pertanyaan di balik semuanya
komponen: flip_card, countdown_ring
musik: marimba Bb bright 112 · sfx wood
durasi: 78
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **reel**: `v.ground` paper, `v.hud = False` + `viewfinder` (tag "karier cloud"), `smear_words` statements (center), `iris` teal masuk/keluar INTRO, `float_chips` (nama tool, bab 01), `highlight_phrase` (bab 02, 03), `count_pill` ("2×", bab 03), satu `pixel_wipe` (masuk RECAP), `end_card` + follow. Pengecualian §8 reel berlaku. Nggak pakai `verb_slam` (foto-WA baru pakai). |
| Motion (STYLE §6d) | spring `snappy` (flip kartu, timer pop) · reveal `smear_words` (reel) · glue persistent hero: kartu aktif datang dari deck kanan-bawah, pergi ke tumpukan "selesai" kiri-bawah (deck + pile persisten 01–05) · exit reel (scale +30% blur) — beda set dari jalur-karier (silk · mask · Morph · dim) |
| Metafora | kartu kuis: INTRO (kartu 01 + timer), 01–05 (satu kartu per bab, dibalik), RECAP (lima kartu jajar → jadi satu kartu), OUTRO (kartu 01 balik: "kamu jawab apa?") |
| Signature move | `countdown_ring` habis → `flip_card` dibalik ke atas (snappy, sedikit overshoot = kartu "nendang" pas mendarat) → tulisan tangan ditulis kiri→kanan. Di 01, 02, 03, 04, 05 + versi cepat di RECAP |
| Color · hook · struktur | teal `#0E9AAB` (ring, band kartu, balik kartu) + `reel_green` (iris, highlighter) · kuis langsung · kuis 5 kartu |
| Suara (STYLE §7) | style `marimba` · key Bb · mood bright · 112 BPM · sfx kit `wood` (kartu di meja kayu) — jalur-karier ambient/soft, foto-WA cinematic/glass |
| Komponen baru (QUICK) | `components/kuis.py`: `flip_card` (kartu kuis 2 muka, flip sumbu horizontal, tulisan tangan), `countdown_ring` (ring 3·2·1 + ✓) |
| Sentuhan manusia | artefak: — (tanpa screenshot; pertanyaan asli dari interview) · opini: "jawaban favoritku: rollback dulu" (L12), "aku catat namanya" (L14) · kejutan: lima kartu ternyata satu pertanyaan (RECAP) · ketidaksempurnaan: kartu selesai ditumpuk miring + coretan "nama: ____" yang ditulis tangan |

## Komposisi per bab (STYLE §6b)
| Bab | Hero | Layout | Kamera | Punch / transisi |
|---|---|---|---|---|
| INTRO | kartu 01 besar (pertanyaan lemot) + ring 3·2·1 jalan | centered hero, statement di atas | push-in ke ring (L01) → pull-out pas deck 5 kartu nongol (L02) | smear "3 detik." · ring tick tiap detik · "textbook" dicoret highlight (L03) · `iris` open teal |
| 01 · LEMOT | kartu 01 dibalik: "sejak kapan? / apa yang berubah?" | kartu tengah + `float_chips` nama tool yang dateng lalu redup | push-in ke tulisan tangan (L05) | chips tool (L04) → pudar · flip (signature) |
| 02 · SCALE | kartu 02 kecil di atas + diagram: up (satu box tinggi) vs out (4 box) → semua antre ke satu database | kartu atas + diagram bawah | follow ke database (L08) | `highlight_phrase` "nggak nolong" · antrean titik numpuk |
| 03 · TAGIHAN | kartu 03 miring kiri + cost report (3 baris, satu "baru bulan ini") | stacked/tilted (kartu + report) | push-in ke baris baru | `count_pill` 1× → 2× (punch) · highlight baris · flip |
| 04 · JAM DUA | "02.00" raksasa (typography) → kartu 04 dengan dua tombol: Rollback / fix forward | pure typography → kartu | punch-out pas Rollback dipencet | press "Rollback" + ✓ · flip |
| 05 · KUBERNETES | kartu 05 + notes kecil "nama: ____" yang ditulis | kartu kanan + notes kiri (tilted) | drift | pen scribble + ✓ teal |
| RECAP | `pixel_wipe` → lima kartu (balik) berjajar kipas → nyatu jadi satu kartu: "pas rusak, mikir gimana?" | fan → satu kartu | pull-out | pixel wipe (sekali per video) |
| OUTRO | `end_card` + kartu 01 mini "kamu jawab apa?" + follow click | centered | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01: ring mulai di "duluan" dan habis pas L02 jalan — kartu 01 baru dibalik di L04 (penonton sempat mikir).
- L04: chips tool = Grafana, CloudWatch, htop, Datadog — nama tool, bukan logo.
- L08: label "database" English, antrean = titik-titik numpuk di depan satu cylinder.
- L10: cost report baris generik (compute · storage · "NAT gateway — baru"), tanpa angka rupiah/dolar.
- L12: tombol "Rollback" ditekan (press) — opini, bukan aturan mutlak.
- Pertanyaan terbuka: framing "aku tanya" butuh pengalaman nge-interview/mentoring beneran.
