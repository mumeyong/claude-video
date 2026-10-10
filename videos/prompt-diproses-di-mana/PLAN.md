# PLAN — Kamu ngetik prompt — sebenernya diproses di mana?

> Fase 1.5. Dua video terakhir: ai-ngarang-jawaban (bar saran keyboard · kata loncat · ungu · eksperimen + klaim ·
> classic+reel · lofi/glass) dan interview-cloud-5-pertanyaan (kartu kuis · flip snappy · teal · kuis ke penonton ·
> look reel · marimba/wood). Baris terakhir REGISTRY nggak ada `look reel` → video ini **look reel** (paper,
> viewfinder, smear, wipes; pengecualian §8 reel berlaku: statement di tengah, warna hijau + signature, hard cut).

<!-- registry
pilar: B
metafora: request ke studio radio — prompt = kertas request yang nyebrang laut ke studio (data center), antre di paku nota meja penyiar (GPU), jawaban disiarin langsung balik ke HP token demi token (streaming)
signature: lampu ON AIR nyala → gelombang siaran keluar dari mic, tiap gelombang bawa satu token yang mendarat di layar HP · look reel
look: reel
color: oranye `#E8861A`
hook: cold open di tengah aksi (tombol enter dipencet, kalimat terbang keluar layar "nyebrang laut")
struktur: perjalanan pulang-pergi 3 stop: berangkat (kabel laut) → antre (GPU) → siaran balik (streaming)
komponen: on_air, mic_studio, paku_nota
musik: garage A bright 128 · sfx mech
durasi: 77
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **reel**: paper ground, `viewfinder` (tag "AI sehari-hari"), `smear_words` statements di tengah, `float_chips` (request yang masuk), `iris` oranye ke bab 00, `pixel_wipe` ke RECAP, `formula` di RECAP, `end_card` outro. Satu `pixel_wipe`, tanpa `verb_slam`. |
| Motion (STYLE §6d) | reel moves + glue **`sheen` + `swap`** (layar HP: prompt → "server sibuk" → jawaban) · spring `snappy` buat pop kecil · exit reel (scale-up blur) — beda dari ai-ngarang (heavy · ink · Rig · mask) dan interview (snappy · smear · Rig deck) |
| Metafora | studio radio: INTRO (HP → "kirim request ke radio", lampu ON AIR muncul), 00 (studio = data center di seberang laut, lampunya kedip pas kertas nyampe), 01 (paku nota numpuk request, penyiar = GPU, "server sibuk"), 02 (ON AIR nyala → siaran token demi token), RECAP (formula pulang-pergi) |
| Signature move | lampu ON AIR nyala → gelombang siaran (`sound_rings` arc) keluar dari mic → satu token mendarat di HP — INTRO (kedip pertama), 00 (atap data center), 02 (×N token), RECAP |
| Color · hook · struktur | oranye `#E8861A` (lampu ON AIR, kertas request, gelombang) · cold open tombol enter · perjalanan pulang-pergi 3 stop |
| Suara (STYLE §7) | style `garage` · key A · mood bright · 128 BPM · sfx kit `mech` (tombol, saklar studio) — ai-ngarang lofi/glass, interview marimba/wood |
| Komponen baru (QUICK) | `components/radio.py`: `on_air` (lampu kotak ON AIR, nyala/kedip) · `mic_studio` (mic di boom arm) · `paku_nota` (paku nota dengan tumpukan kertas request) — reuse `gpu_card` (EP07) sebagai penyiar, `phone`, `sound_rings`, reel moves |
| Sentuhan manusia | artefak: request beneran sehari-hari di kertas (resep rendang, PR fisika, caption IG) · opini/pengalaman: "aku pernah bangun infra GPU — nggak ada yang mau GPU-nya idle" · kejutan: tulisan pelan-pelan itu bukan efek ketik · ketidaksempurnaan: kertas request miring + satu nyangkut di paku |

## Komposisi per bab (STYLE §6b)
| Bab | Hero | Layout | Kamera | Punch / transisi |
|---|---|---|---|---|
| INTRO | HP (prompt diketik, enter dipencet, kertas request terbang keluar atas) → lampu ON AIR + mic | centered hero (HP) → statement tengah | push-in ke tombol enter, pull-out | "nyebrang laut." smear besar · `iris` oranye dari lampu |
| 00 · BERANGKAT | rute: HP kiri bawah → WiFi/BTS → laut + kabel bawah laut → gedung data center + ON AIR di atap | full-width peta/rute | pan ikut kertas (key x), push-in ke data center | lampu atap kedip pas kertas nyampe · model vs HP (blok raksasa vs HP kecil) |
| 01 · ANTRE | meja penyiar: `paku_nota` numpuk + `gpu_card` di belakang `mic_studio`, chips request melayang masuk | object + hand note | push-in ke paku nota, punch-out di "server sibuk" | `float_chips` request · `pop_card` "server sibuk" di HP kecil · strike "HP lemot" |
| 02 · SIARAN LANGSUNG | ON AIR nyala → mic → gelombang → HP besar, jawaban muncul token demi token | stacked (studio atas, HP bawah) | drift pelan, push-in ke HP di L14 | `highlight_phrase` "baru dibikin" · `pixel_wipe` oranye ke RECAP |
| RECAP | `formula`: nyebrang laut + antre + disiarin = beberapa detik | centered typography | push-in pelan | count_pill-less (tanpa angka) |
| OUTRO | `end_card` + follow + teaser "AI yang jalan di HP" | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01: "belum sedetik" + "nyebrang laut" — ⚠️ cek: lokasi data center tiap layanan beda; teks layar nggak nyebut negara.
- L05: "biasanya di luar negeri" — ⚠️ cek user (bisa juga region lokal).
- L07: "ribuan" tanpa angka di layar — chips request ilustrasi.
- L09: pengalaman EP07 (infra GPU di Azure) — nggak sebut klien/angka.
- L10: tulisan "server sibuk" di layar = mock (tag "ilustrasi"), bukan screenshot app asli.
- L14: streaming bener (token dikirim sambil di-generate); beberapa app menghaluskan animasinya — narasi nggak bilang "persis".
