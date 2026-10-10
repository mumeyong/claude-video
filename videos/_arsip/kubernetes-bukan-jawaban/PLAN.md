# PLAN — Kubernetes bukan jawaban buat semua hal

> Fase 1.5. Cek `ideas/REGISTRY.md`: dua video terakhir = WiFi EP 01 (jalan cahaya fiber · ungu · cold open · diagnosa
> per lampu · lofi/glass) dan WiFi EP 02 (komplek + pos satpam · palang · oranye · klaim nyeleneh · perjalanan request ·
> marimba/wood). Pilihan 1–5 di bawah beda dari dua itu. Bukan episode seri — HUD biasa.

<!-- registry
pilar: C
metafora: pelabuhan peti kemas (Kubernetes: crane = scheduler, lapangan = node, peti = container) vs kurir motor bawa satu paket (VM / serverless)
signature: gantry crane turun-angkat-taruh (peti kemas → numpuk; lalu cuma satu kardus kecil — absurd)
color: hijau `#10A060`
hook: mitos dicoret ("Pakai Kubernetes aja" → "Tergantung.")
struktur: versus (pelabuhan vs kurir) → biaya diam → checklist 3 pertanyaan (save-able)
komponen: crane, peti_kemas, kurir
musik: garage E warm 130 · sfx mech
durasi: 74
-->

## Identitas
| | |
|---|---|
| Motion (STYLE §6d) | spring `snappy` · reveal `blur` (+ `track_line` cuma buat punch "Tergantung." / "Kubernetes.") · glue persistent hero `Rig` (crane) + `bento` (3 pertanyaan) · exit `blur` — beda set dari EP 02 (heavy · mask · lockup/sheen · mask) dan EP 01 (silk · ink · Morph/sheet · dim) |
| Metafora | pelabuhan: 00 (crane numpuk peti = scheduling ratusan container), 01 (crane ngangkat satu kardus → kurir lebih masuk akal), 02 (pelabuhan malam sepi, lampu + penjaga tetap nyala = biaya diam), RECAP (crane naruh kardus ke kurir) |
| Signature move | crane: trolley geser → spreader turun → angkat → taruh, snappy. 00 = peti kemas ke tumpukan; 01 = cuma kardus kecil (kamera push-in, absurd); RECAP = kardus diserahin ke kurir |
| Color · hook · struktur | hijau `#10A060` (peti + crane) · mitos dicoret · versus → biaya → checklist |
| Suara (STYLE §7) | style `garage` · key E · mood warm · 130 BPM · sfx kit `mech` (crane, mesin pelabuhan) — EP 02 marimba/wood, EP 01 lofi/glass |
| Komponen baru (QUICK) | `crane` (gantry: 2 kaki, balok atas, trolley, kabel + spreader, beban opsional) · `peti_kemas` (peti bergaris, label) · `kurir` (motor + box belakang) — reuse `receipt`, `bento` |
| Sentuhan manusia | artefak: "10.000 request barengan" (Bongkar EP 01, asli) + tag "Bongkar EP 01" · opini: "alat dipilih buat masalahnya, bukan trennya" · kejutan: crane raksasa ngangkat satu kardus · ketidaksempurnaan: strike miring di headline, hand note "sewa satu pelabuhan?" |

## Komposisi per bab (STYLE §6b)
| Bab | Hero | Layout | Kamera | Punch / transisi |
|---|---|---|---|---|
| INTRO | headline mitos dicoret → `track_line` "Tergantung." raksasa · L03 angka 10.000 + tag EP 01 | pure typography → big number | punch-out di "tergantung" | strike + thud · count-up 10.000 |
| 00 · PELABUHAN | crane (Rig) + tumpukan peti + label scheduler / node / container | centered hero, full width | pull-out 1,12 → 1 | crane numpuk 2 peti (signature) · ✓ "juara" |
| 01 · SATU PAKET | crane yang sama ngangkat 1 kardus → kurir masuk dari kanan | hero kiri + kurir kanan | push-in ke kardus (L09) | note "sewa satu pelabuhan?" · tag VM / serverless |
| 02 · BIAYA DIAM | `receipt` "BIAYA PELABUHAN · walau sepi" (crane kecil, redup, di belakang) | tilted receipt | drift + push-in ke baris terakhir | baris "orang yang ngerti" merah → "paling mahal" |
| 03 · TIGA PERTANYAAN | `bento` 3 tile pertanyaan, tiap tile dapat "iya" | bento grid | key per tile | word pill "Kubernetes." (L16) |
| RECAP (gelap) | crane naruh kardus ke kurir, peti tetap di pelabuhan | dark, left headline | drift | strike "trennya" vs accent "masalahnya" |
| OUTRO | `standard_outro` + kartu "Tim pelabuhan atau tim kurir?" (komentar) | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L03: 10.000 = angka asli dari Bongkar EP 01 (ICE Kubernetes). Tag "Bongkar EP 01" biar nyambung.
- L06: label English: `scheduler` (crane) · `node` (lapangan) · `container` (peti). Jangan diterjemahin.
- L10: tag `VM` · `serverless` — "bayarnya per request" cukup di narasi.
- L12: baris receipt tanpa angka (nilai = "tiap jam", "tiap hari", "tiap rilis") — nggak ada harga.
- Pertanyaan terbuka: kalau kamu punya cerita klien yang kamu saranin *nggak* pakai Kubernetes (asli), hook B bisa
  diganti jadi cerita itu.
