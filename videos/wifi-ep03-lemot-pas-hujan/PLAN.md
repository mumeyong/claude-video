# PLAN — WiFi lemot pas hujan: mitos atau beneran? (Bongkar WiFi Rumah EP 03)

> Fase 1.5. Cek `ideas/REGISTRY.md`: dua video terakhir = ai-butuh-listrik (setrika · lampu klik + uap · coral · angka dulu ·
> rantai sebab-akibat · wipe + depth_swap · marimba F warm/soft) dan prompt-diproses-di-mana (studio radio · ON AIR · oranye ·
> cold open · pulang-pergi 3 stop · look reel · garage A bright/mech). EP sebelumnya di seri: EP 02 (komplek · palang ·
> oranye · klaim nyeleneh · mask + lockup). Pilihan 1–5 di bawah beda dari semuanya. Seri: HUD `BONGKAR WIFI RUMAH · EP 03`,
> `series_bumper`, modem EP 01 + ikon WiFi EP 02 muncul sebagai rujukan, bukan hero.

<!-- registry
pilar: B
metafora: talang bocor — rumah dibelah waktu hujan: di dalam router + HP kering, di luar tiang + kotak ODP + kabel fiber nyusur atap kayak talang; masalahnya satu sambungan yang netes, bukan hujannya
signature: satu tetes air pisah dari hujan, jalan pelan nyusur kabel, nyelip ke celah tutup ODP → denyut cahaya di fiber meredup, lampu modem kedip
look: classic
color: teal `#0E9AAB`
hook: pertanyaan spesifik (hujan deras jam empat sore, video muter terus)
struktur: format seri lewat satu potongan rumah: mitos (dalam) → satu tetes (luar) → 3 langkah (sheet checklist)
komponen: hujan, odp_box, rumah_potong
musik: lofi G dreamy 84 · sfx glass
durasi: 74
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **classic + Apple craft** — nggak ada reel moves |
| Motion (STYLE §6d + §6f) | reveal `rise` (per baris) · glue `Rig` (satu potongan rumah = persistent hero, geser/zoom antar bab) + `sheet` (checklist 02) · exit quiet · spring `hero` buat Rig, `smooth` buat kartu/tag, `snappy` cuma buat tick checklist — beda dari wipe/depth_swap (listrik) dan mask/lockup (EP 02) |
| Apple craft (§6f) | leader: INTRO = spinner HP · 00 = tembok rumah (garis dalam/luar) · 01 = satu tetes · 02 = sheet · RECAP = tetes yang sama. Hold terpanjang: L12–L13 (denyut redup, dolly) · tempo slow–slow–snap: snap di L03 (hujan berhenti, cuma satu tetes) dan L13 (cut ke modem kedip) · kontinuitas: rumah yang sama dari INTRO sampai 01 lewat Rig, sheet naik nutupin rumah di 02 (rumah blur di belakang), RECAP balik ke tetes |
| Metafora | talang bocor: INTRO (satu tetes dari hujan), 00 (hujan di luar, dalam kering), 01 (sambungan ODP netes), 02 ("kena tetesan talang"), RECAP (celah yang udah ada) |
| Signature move | **satu tetes**: hujan jadi tipis/berhenti, satu tetes jatuh pelan, nempel di kabel, nyusur, nyelip ke celah — dipakai di INTRO (jatuh di atap, cut), 01 (masuk ODP, cahaya meredup), RECAP (tetes yang sama berhenti di celah, ditandai note) |
| Color · hook · struktur | teal `#0E9AAB` (air, tetes, kabel fiber yang nyala) · pertanyaan spesifik · format seri (lihat → kejadian → lakuin) lewat satu potongan rumah |
| Suara (STYLE §7) | style `lofi` · key G · mood dreamy · 84 BPM · sfx kit `glass` (tetes) — sebelumnya marimba/soft, garage/mech |
| Komponen baru (QUICK) | `hujan` (garis hujan seeded, density 0..1, frame = f(t)) + `tetes` (satu tetes + jejak) · `odp_box` (kotak ODP close-up: tutup bisa renggang, sambungan di dalam, air menggenang) · `rumah_potong` (rumah cutaway: atap, tembok, router + HP di dalam, tiang + kabel drop di luar) — reuse `modem`, `wifi_icon`, `note`, `pop_tag`, `sheet` |
| Sentuhan manusia | opini: "basahnya di mana?" (L18) · kejutan: hujan tiba-tiba berhenti, tinggal satu tetes (L03) · ketidaksempurnaan: tutup ODP miring/renggang + note tulisan tangan "celahnya di sini" (tanpa angka) · artefak: — (foto kotak ODP / kabel kendor depan rumah user kalau ada → assets/) |

## Komposisi per bab (STYLE §6b)
| Bab | Hero (leader) | Layout | Kamera | Punch / transisi (kontinuitas) |
|---|---|---|---|---|
| INTRO | HP dengan spinner (L01) → rumah potong di hujan (L02) → hujan berhenti, satu tetes (L03) | centered hero (HP) → full scene | cut L02, dolly hold L02 | snap L03: hujan stop, satu tetes jatuh + thud · bumper seri |
| 00 · MITOS | rumah potong (Rig zoom ke dalam): router → HP, ikon WiFi penuh, garis tembok "dalam / luar" | full-width scene, dalam vs luar | Rig push ke ruang dalam, dolly | tag "beberapa meter" (L06) · panah ke luar (L07) |
| 01 · SATU TETES | Rig geser ke tiang → `odp_box` close-up (depth via Rig scale), tetes nyelip celah, denyut cahaya redup | object + hand note | Rig ke tiang (L08), cut ke ODP close-up (L09), dolly hold L12 | snap L13: cut ke modem kecil, PON kedip / LOS kedip |
| 02 · YANG BISA KAMU LAKUIN | `sheet` checklist 3 baris, rumah blur di belakang | sheet over scene | — (sheet yang gerak) | tick per langkah, strike kecil "restart" (L17) |
| RECAP (gelap) | satu tetes besar di celah, note "basahnya di mana?" | dark, left headline, hero tengah | dolly | word pill "pemicu." → "celah." |
| OUTRO | `standard_outro` + teaser EP 04 (restart router) | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01: layar HP: video dengan spinner muter (lingkaran), jam status bar 16.00 — itu satu-satunya "angka" (jam, bukan data).
- L04: tag kecil "2,4 / 5 GHz" — **nggak**, terlalu teknis buat broad; cukup gelombang WiFi yang redup waktu lewat air (ilustrasi kecil).
- L06: tag "beberapa meter" di antara router dan HP; hujan cuma di luar garis tembok.
- L09: label ODP di kotak; kabel masuk dari bawah. L11: tags `tutup renggang` · `kabel retak`.
- L12: denyut cahaya teal di kabel, tiap lewat sambungan basah makin redup (alpha), di modem LED PON kedip.
- L15: baris checklist: "jam 16.04 · lemot" (contoh catatan tangan) + ikon kamera kecil (bukan emoji — gambar sendiri).
- Pertanyaan terbuka: foto kotak ODP / kabel drop asli (anonim) → `assets/` kalau ada.
