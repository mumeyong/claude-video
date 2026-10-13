# PLAN — AI gratis itu — siapa yang bayar?

> Fase 1.5. Dua video terakhir di REGISTRY: wifi-ep03-lemot-pas-hujan (talang bocor · satu tetes · teal · pertanyaan
> spesifik · format seri · rise + Rig/sheet · lofi G dreamy/glass) dan ai-butuh-listrik (setrika · lampu klik + uap ·
> coral · angka dulu · rantai sebab-akibat · wipe + depth_swap · marimba F warm/soft). Pilihan 1–5 di bawah beda dari keduanya.

<!-- registry
pilar: B
metafora: struk kasir Rp0 — tiap jawaban AI satu baris "Rp0" di struk thermal; dibalik, di belakangnya ada tagihan asli (GPU · per jam · listrik) yang alamatnya bukan kamu: subscription, investor, iklan, data
signature: struk dibalik di sumbu tegak (yaw) — sisi depan "TOTAL Rp0" muter, sisi belakang penuh baris tagihan; tiap penanggung dicap stempel hijau miring
look: classic + paper-big
color: hijau `#10A060`
hook: mitos dicoret lewat benda (struk "TOTAL Rp0" → "struk ini ada baliknya")
struktur: satu struk, dua sisi: depan (Rp0) → biaya asli muncul samar → balik (4 penanggung) → saklar di kaki struk (bagianmu)
komponen: struk, saklar
musik: cinematic E tense 96 · sfx mech
durasi: 76
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **classic + Apple craft** — nggak ada reel moves |
| Material (STYLE §6g) | **paper, big** — struk thermal = kertas: `v.stage` paper ground (tint hijau), struk ngisi ± 40–55 % tinggi frame (s 1,0–1,3), masuk dari bawah frame (`bleed=True`); `v.finish` grain paper. Sebelumnya: flat-small (wifi-ep03) |
| Motion (STYLE §6d + §6f) | reveal `ink` (baris faint → kata nge-ink) · glue: struk = persistent hero (satu objek dari INTRO sampai RECAP, cuma ganti skala/posisi/sisi) + `focus_pull` (struk blur di belakang kartu saklar di 02) · exit quiet · spring `hero` buat struk, `smooth` buat tag, `snappy` cuma saklar — beda dari rise+Rig/sheet (wifi) dan wipe+depth_swap (listrik) |
| Apple craft (§6f) | leader: INTRO = struk ngeprint (feed) · 00 = kolom "biaya asli" nge-ink · 01 = flip, lalu stempel satu-satu · 02 = saklar · RECAP = struk balik ke depan + stempel. Hold terpanjang: L06 (dolly di baris GPU) dan L13. Tempo slow–slow–snap: snap di L08 (flip, thud) dan L17 (stempel "DITAGIH KE: ORANG LAIN"). Kontinuitas: struk nggak pernah keluar layar antar bab (INTRO→00→01 lewat transform-nya sendiri), 02 = kartu saklar naik di depan struk yang di-`focus_pull` |
| Metafora | struk Rp0: INTRO (struk Rp0 keprint), 00 (kolom biaya asli muncul samar di sebelah Rp0), 01 (struk dibalik: 4 penanggung), 02 (kaki struk: saklar "data buat training"), RECAP (struk balik ke depan, cap "ditagih ke orang lain") |
| Signature move | **struk dibalik**: yaw 0 → π (sisi depan menyempit, sisi belakang melebar) — INTRO (setengah putar, ngintip, balik lagi di L02), 01 (putar penuh di L08), RECAP (balik ke depan) |
| Color · hook · struktur | hijau `#10A060` (stempel, garis biaya, saklar nyala) · mitos dicoret lewat benda (Rp0 → "ada baliknya") · satu struk dua sisi |
| Suara (STYLE §7) | style `cinematic` · key E · mood tense · 96 BPM · sfx kit `mech` (printer kasir, stempel) — sebelumnya lofi/glass, marimba/soft |
| Komponen baru (QUICK) | `struk` (struk thermal: header toko, baris item, total, kaki sobekan zigzag; dua sisi + `flip` 0..1 lewat yaw; `feed` 0..1 = keluar dari printer; `look=` flat/paper) · `saklar` (toggle iOS, on 0..1, label) — dua-duanya di `components/kasir.py`. Reuse: `stamp`, `strike`, `note`, `pop_tag`, `focus_pull`, `standard_outro` |
| Sentuhan manusia | opini: "baris GPU yang bikin orang kaget" (L06) + "nggak ada baris yang nol" (L17) — dari kerjaan FinOps · kejutan: struk Rp0 ternyata punya belakang yang penuh (L08) · ketidaksempurnaan: stempel miring + hand note "ini kamu" (02) · artefak: — (screenshot setting privasi asli bisa masuk `assets/` nanti; sekarang digambar generik, tanpa merek) |

## Komposisi per bab (STYLE §6b)
| Bab | Hero (leader) | Layout | Kamera | Punch / transisi (kontinuitas) |
|---|---|---|---|---|
| INTRO | struk keluar dari printer (feed), baris "jawaban #01…#20 · Rp0", TOTAL Rp0 | centered hero besar (struk 70 % tinggi), headline di atas | dolly hold L01 | L02: struk ngintip setengah putar lalu balik (teaser); L03 "siapa?" hold |
| 00 · BIAYA ASLI | struk geser kiri + kolom kanan "biaya asli" nge-ink samar (GPU · per jam · listrik · data center) dengan "???" | object + annotation di samping (split) | push ke baris GPU (L06), dolly | Rp0 dicoret `strike` di L07 — "bukan *kamu*" |
| 01 · YANG NANGGUNG | struk dibalik penuh (yaw) — 4 baris penanggung, stempel hijau satu-satu | hero tengah, paling besar (s 1,3) | cut di flip (L08), dolly L13 | snap: flip + thud (L08); tag "campurannya beda" L13 |
| 02 · BAGIANMU | kartu `saklar` naik di depan struk (struk `focus_pull` blur di belakang) | kartu depan + latar blur | — (saklar yang gerak) | saklar mati di "mati" L15, tag "data kantor ✕" L16 |
| RECAP (dark) | struk balik ke sisi depan di gelap, TOTAL Rp0 → stempel "DITAGIH KE: ORANG LAIN" | hero tengah, gelap | cut masuk, dolly | stempel di "orang lain" (bookend hook) |
| OUTRO | `standard_outro` + save (L18) + follow (L19) | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01: nggak ada angka biaya di mana pun — kolom "biaya asli" pakai "???" (angka per jawaban beda tiap produk, nggak kita klaim).
- L09–L12: label penanggung generik (subscription · investor · iklan · data), tanpa merek; L12 "bisa", bukan "pasti".
- L15: saklar digambar generik ("Pakai obrolan buat training") — bukan screenshot produk tertentu.
