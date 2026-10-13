# PLAN — AI nggak gantiin cloud engineer — AI butuh cloud engineer

> Fase 1.5. Dua video terakhir di REGISTRY: ai-gratis-siapa-bayar (struk Rp0 · struk dibalik · hijau · mitos dicoret
> lewat benda · satu struk dua sisi · ink + Rig/focus_pull · cinematic E tense/mech · paper-big) dan wifi-ep03-lemot-pas-hujan
> (talang bocor · satu tetes · teal · pertanyaan spesifik · format seri · rise + Rig/sheet · lofi G dreamy/glass · flat-small).
> Pilihan 1–5 + look + musik di bawah beda dari keduanya.

<!-- registry
pilar: C
metafora: panggung hajatan — AI = biduan yang kelihatan; kolong panggung yang gelap = infra (genset = GPU, gulungan kabel = network, peti alat = storage, nota sewa = biaya); kru sound di sayap panggung = cloud engineer
signature: lingkaran lampu sorot nyisir bagian gelap panggung — tiap alat yang kena sorot nyala dan tetap terang; terakhir sorotnya mendarat di kru sound
look: classic + flat-big
color: ungu `#7558F0`
hook: pengalaman sendiri ("aku pernah bangun fondasi buat training AI — yang ngurus bukan AI-nya") + ~gantiin~ → butuh
struktur: satu panggung dari atas ke bawah: biduan (yang kelihatan) → kolong (alatnya) → kru (orangnya) → panggungnya jadi banyak (skill)
komponen: panggung, sorot
musik: marimba D bright 110 · sfx wood
durasi: 74
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **classic + Apple craft** — nggak ada reel moves |
| Material (STYLE §6g) | **flat-big** — panggung ngisi ± 100 % lebar × 52 % tinggi frame (y 540–1540, kepotong tipis di kiri-kanan, `bleed=True`); plain fills, kontras dari terang (panggung) vs gelap (kolong + sayap). Sebelumnya: paper-big (ai-gratis), flat-small (wifi-ep03) |
| Motion (STYLE §6d + §6f) | reveal `wipe` (headline dibuka mask lembut per baris) · glue: panggung = persistent hero `Rig` (full-bleed shrink di INTRO → diam → mengecil jadi satu dari tiga panggung di 02 → balik di RECAP) · exit quiet · spring `hero` buat panggung, `smooth` buat sorot + tag, `snappy` cuma tag kecil — beda dari ink + Rig/focus_pull (ai-gratis) dan rise + sheet (wifi-ep03) |
| Apple craft (§6f) | leader: INTRO = panggung mendarat (full-bleed → 1) · 00 = lingkaran sorot (pindah alat ke alat, satu per kata) · 01 = sorot ke kru, lalu genset (nyala → turun), lalu kotak container satu-satu (follow) · 02 = panggung jadi tiga (yang tengah = hero, dua lainnya follow) · RECAP = sorot ke kru. Hold terpanjang: L05 (cuma biduan, dolly) dan L13. Tempo slow–slow–snap: snap di L03 (~gantiin~ dicoret) dan L16 (~hilang~ dicoret). Kontinuitas: panggung nggak pernah keluar layar dari INTRO sampai RECAP |
| Metafora | panggung hajatan: INTRO (biduan di bawah lampu), 00 (kolong: genset/kabel/peti/nota), 01 (kru sound di sayap), 02 (tiga panggung), RECAP (biduan ganti, kru tetap) |
| Signature move | **lingkaran sorot nyisir yang gelap** — INTRO (ngintip ke kolong di "bukan", balik ke biduan), 00 (empat alat satu-satu), 01 (mendarat di kru), RECAP (balik ke kru waktu biduan ganti) |
| Color · hook · struktur | ungu `#7558F0` (baju biduan, lampu, sorot, tag) · pengalaman sendiri + coretan "gantiin → butuh" · atas → bawah → orangnya → kali tiga |
| Suara (STYLE §7) | style `marimba` · key D · mood bright · 110 BPM · sfx kit `wood` (panggung kayu, rame hajatan) — sebelumnya cinematic/mech, lofi/glass |
| Komponen baru (QUICK) | `panggung` (+ `panggung_geo`): panggung hajatan potongan samping — rangka truss + 2 lampu, backdrop, speaker, biduan + stand mic, sayap gelap kanan dengan meja mixer + kru sound (headset), dek, kolong gelap dengan scaffolding + genset (`run`: lampu + asap) · gulungan kabel · peti alat · nota sewa; `lit` per alat, `pack` (kotak container putus-putus) per alat, `swap` (biduan ganti) · `sorot`: kolam cahaya lembut di permukaan gelap (cahaya, bukan neon). Di `components/panggung.py` |
| Sentuhan manusia | artefak: project training AI di Azure (EP07, CV) — L01, L10–L12 · opini: "biduannya boleh ganti tiap bulan, panggungnya tetap butuh orang" (L17) · kejutan: kolong yang gelap ternyata penuh alat (L06) · ketidaksempurnaan: nota sewa ditempel miring, hand note "ini kamu" di kru |

## Komposisi per bab (STYLE §6b)
| Bab | Hero (leader) | Layout | Kamera | Punch / transisi (kontinuitas) |
|---|---|---|---|---|
| INTRO | panggung mendarat dari full-bleed (s 2,2 → 1) di "training"; lampu ke biduan | hero besar, headline di atas | dolly hold L01, cut | L02 sorot ngintip kolong; snap L03: ~Gantiin~ dicoret → *butuh* |
| 00 · KOLONG PANGGUNG | sorot pindah: genset → kabel → peti → nota; tag English nempel di tiap alat | hero besar, fokus di setengah bawah | dolly di L05 (hold biduan) + L08 | kejutan: kolong gelap penuh alat (L06) |
| 01 · KRU SOUND | sorot naik ke sayap: kru sound nyala; genset nyala → turun; kotak container | hero besar, fokus di sayap kanan | dolly ke kru (L09), dolly L13 | hand note "ini kamu" (L09) |
| 02 · SKILL-NYA | panggung mengecil jadi yang tengah dari tiga (Rig), dua lainnya follow; 3 pill skill | tiga objek kecil berjajar + typografi | cut masuk, dolly L15 | snap L16: *Berubah*. Bukan ~hilang~. |
| RECAP (dark) | panggung balik besar; biduan ganti (swap), sorot tetap di kru | hero tengah, gelap | cut masuk, dolly | bookend INTRO: lampu, biduan, kru |
| OUTRO | `standard_outro` + teaser card ("tulis *panggung*") + follow (L19) | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01/L10–L12: sama persis dengan EP07 (AKS + GPU, training pool di-scale turun, inference selalu siap, container → bisa pindah cloud). Nggak ada angka.
- L15: "yang aku lihat dicari" = opini/pengamatan, bukan data lowongan — di layar cuma tiga pill skill, tanpa angka.
- Biduan = siluet orang (bukan robot), tag "AI" di atasnya. Banned list: nggak ada server biru / otak / robot.
