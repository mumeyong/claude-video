# PLAN — Dari System Engineer ke Senior Cloud Engineer — jalur aku

> Fase 1.5. Dua video terakhir: foto-whatsapp-lewat-mana (loker penitipan · pintu loker heavy · terracotta · timestamp
> spesifik · dua jalur · **look reel** · cinematic/glass) dan kubernetes-bukan-jawaban (pelabuhan + kurir · crane ·
> hijau · mitos dicoret · versus → checklist · garage/mech). Baris terakhir REGISTRY = `look reel` → video ini
> **classic + reel moves** (STYLE §6e, tanpa pengecualian §8).
> Draft identitas di ideas/11 dipakai (skill tree · merah · before/after · kronologis) — tanpa gembok (kunci/loker baru
> aja dipakai di video sebelumnya): node "terbuka" = ring yang ke-charge lalu tile-nya nyala.

<!-- registry
pilar: C
metafora: skill tree game — tiap level karier buka cabang baru (tools), cabang paling atas ternyata pertanyaan (= keputusan)
signature: cabang menjalar dari tile induk dengan ujung terang → ring status nge-charge → tile kebuka (border merah + ✓, pop kecil)
look: classic+reel
color: merah `#F03B4F`
hook: before/after (kartu nama 2020 "jalanin" → sekarang "mutusin", kartu dibalik)
struktur: cerita kronologis: LV 1 → LV 2 → LV 3 → salah kaprah → "kamu di cabang mana"
komponen: branch, skill_tile, skill_tree, name_card
musik: ambient D warm 80 · sfx soft
durasi: 78
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **classic + 3 reel moves**: `iris` (close, merah) masuk bab 02 SENIOR · `float_chips` (sertifikat/tools beterbangan di bab 03) · `highlight_phrase` ("dipercayain" di bab 03). Warna dikasih chapter/signature color; §8 tetap penuh (kiri, satu aksen biru). |
| Motion (STYLE §6d) | spring `silk` (Morph kartu → node root, kamera) · reveal `mask` · glue `Morph` (kartu nama menyusut jadi root tree) + tree persisten (bukan `Rig`) · exit `dim` — beda set dari foto-WA (heavy · smear · Rig · reel exit) dan kubernetes (snappy · blur · Rig+bento · blur) |
| Metafora | skill tree: INTRO (kartu nama → root), 00 (LV 1 tools kebuka), 01 (LV 2 + cabang "kenapa?"), 02 (LV 3 + cabang paling atas = pertanyaan), RECAP (tree mini: "kamu di sini") |
| Signature move | cabang menjalar + ring charge + tile kebuka — dipakai di 00, 01, 02, dan versi cepat di RECAP |
| Color · hook · struktur | merah `#F03B4F` (branch, ring, tile) · before/after kartu nama · kronologis per level |
| Suara (STYLE §7) | style `ambient` · key D · mood warm · 80 BPM · sfx kit `soft` (cerita personal) — foto-WA cinematic/glass, kubernetes garage/mech |
| Komponen baru | `components/skilltree.py`: `branch` · `skill_tile` · `skill_tree` · `name_card` — reuse `Morph`, `yaw`, `bubble`, `note`, `word_pill`, `strike`, reel moves |
| Sentuhan manusia | artefak: jalur asli dari CV (2020 System Engineer → 2021 Cloud Engineer di project bank → Senior) · opini: yang bikin naik = keputusan yang dipercayain · kejutan: tier paling atas kebuka isinya pertanyaan, bukan tools · ketidaksempurnaan: hand note miring "keputusan: orang lain" + bubble "kenapa pilih ini?" |

## Komposisi per bab (STYLE §6b)
| Bab | Hero | Layout | Kamera | Punch / transisi |
|---|---|---|---|---|
| INTRO | kartu nama 2020 (LV 1) → dibalik (yaw) → "sekarang" (LV 3) → Morph menyusut jadi root tree | centered card | push-in pas kartu dibalik, reset | flip kartu · Morph ke root · tree hantu muncul |
| 00 · SYSTEM ENGINEER | skill tree: LV 1 (CI/CD · monitoring · serverless) kebuka | full tree, tier bawah aktif | focus tier 1 → reset ke atas (note) | tag "LEVEL UP" · hand note ke tier atas "keputusan: orang lain" |
| 01 · CLOUD ENGINEER | tree: LV 2 (Kubernetes · multi-AZ · biaya ↓) + cabang pendek ke bubble "kenapa pilih ini?" | tree + bubble | focus tier 2 → push ke bubble | bubble pop (punch kecil) |
| 02 · SENIOR | tree: LV 3 (migrasi big data · serverless stack · mentoring) → tier paling atas kebuka = 2 pertanyaan | tree penuh | `iris` close masuk, focus tier 3 → focus atas → pull-out (kejutan) | tile pertanyaan solid merah |
| 03 · SALAH KAPRAH | typography: chips sertifikat/tools beterbangan → dicoret → pill "keputusan." + "yang dipercayain ke kamu" | pure typography | punch-out 0.97 di pill | `float_chips` · strike · `highlight_phrase` |
| RECAP | tree mini (dark): root nyala + note "kamu di sini?" → cabang lari cepat ke atas | centered hero (dark) | drift push | bookend "jalanin → mutusin" |
| OUTRO | `standard_outro` + teaser "Kamu lagi di cabang mana?" | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01/L02: kartu nama = bookend kata "jalanin" / "mutusin" (balik lagi di L19).
- L05: label tile pakai istilah English (CI/CD, monitoring, serverless). Nggak ada nama tools/vendor yang nggak ada di CV.
- L08: "project bank" — nama bank/perusahaan nggak disebut.
- L12: tahun naik Senior nggak ditampilkan (belum dicek) — kicker cuma "LV 3 · SENIOR".
- L16: chips "sertifikat", "tools" generik — bukan nama sertifikat asli.
- Pertanyaan terbuka: tahun jadi Senior · apakah 2021 = pindah perusahaan atau naik jabatan · kelas/mentoring udah siap (CTA)?
