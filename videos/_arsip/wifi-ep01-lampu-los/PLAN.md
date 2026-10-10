# PLAN — Lampu modem merah "LOS" itu artinya apa? (Bongkar WiFi Rumah EP 01)

> Fase 1.5. Cek `ideas/REGISTRY.md`: dua video terakhir = EP07 (atlet bulu tangkis · kok melengkung · oranye · mitos
> dicoret · format seri) dan biaya-cloud-bocor (meteran token · LED pulsa · teal · angka dulu · hitung mundur).
> Semua pilihan 1–5 di bawah beda dari dua itu. Seri baru: HUD `MUMEYONG · BONGKAR WIFI RUMAH · EP 01`, bumper seri.

<!-- registry
pilar: B
metafora: jalan cahaya dari kantor ISP → tiang (ODP) → rumah; lampu modem = penunjuk tempat rusaknya
signature: denyut cahaya jalan di kabel fiber, berhenti di titik putus, kamera balik ke lampu modem yang ngasih tahu
color: ungu `#7558F0`
hook: cold open di tengah kejadian (jam 21.00, lampu merah)
struktur: diagnosa per lampu (lampu → tempat → yang bisa kamu lakuin)
komponen: modem, fiber_route, patchcord
musik: lofi F dreamy 86 · sfx glass
durasi: 72
-->

## Identitas
| | |
|---|---|
| Motion (STYLE §6d) | spring `silk` · reveal `ink` · glue persistent hero `Rig` (modem) + `Morph` (pill → kartu) + `sheet` (close-up kabel) · exit `dim` |
| Metafora | jalan cahaya ISP → tiang → rumah: INTRO (lampu = penunjuk), 00 LOS (kabel putus), 01 PON (cahaya sampai, kenalan), 02 INTERNET (kabel aman, pintu akun), RECAP (cek dari yang paling dekat, jalur yang sama dari bawah ke atas) |
| Signature move | denyut cahaya ungu jalan di kabel → mati di titik putus → kamera balik ke lampu modem (00, RECAP); di 01 denyut sampai rumah + modem "kenalan"; di 02 denyut sampai tapi berhenti di pintu akun |
| Color · hook · struktur | ungu `#7558F0` (cahaya di fiber) · cold open 21.00 lampu merah · diagnosa per lampu |
| Suara (STYLE §7) | style `lofi` · key F · mood dreamy · 86 BPM · sfx kit `glass` (pertama kali styled score; sebelumnya semua `pulse` 128) |
| Komponen baru (QUICK) | `modem` (5 lampu, state per lampu, focus ring) · `fiber_route` (kantor ISP → tiang + ODP → rumah, denyut, putus) · `patchcord` (kabel kecil di belakang modem, bisa ketekuk) |
| Sentuhan manusia | opini: "aku nggak nebak, aku cek dari yang paling dekat" (L15) · kejutan: internet = cahaya (L04) · ketidaksempurnaan: hand note "jangan ketekuk" + kabel kuning yang ketekuk · artefak: — (foto modem asli user kalau dikasih → assets/) |

## Komposisi per bab (STYLE §6b)
| Bab | Hero | Layout | Kamera | Punch / transisi |
|---|---|---|---|---|
| INTRO | modem (Rig) close-up full-bleed di lampu LOS merah → mundur jadi 5 lampu | centered hero, curtain dari gelap | Rig s 2,3 → 1 (silk) | headline ink "Masalahnya di *kabel*." → bumper seri |
| 00 · LOS | `fiber_route` penuh (ISP → tiang → rumah) | full-width scene, tanpa kartu | push-in ke titik putus (L06) → reset | kabel putus + denyut mati · `sheet` close-up patchcord (L07) · strike "restart" (L08) |
| 01 · PON | modem (Rig balik) + 2 bubble kenalan | hero atas + dialog | push-in ke lampu PON | `Morph` pill "PON · kedip" → kartu "lagi registrasi" |
| 02 · INTERNET | modem kecil di atas + `id_card` login ke pintu ISP | stacked: modem → kartu akun | pull-out 1,08 → 1 | tag merah "login gagal / tagihan telat" · `press` tombol restart → INTERNET hijau + chime |
| RECAP (gelap) | jalur yang sama, dicek dari rumah ke atas (1 → 2 → 3) → modem 5 lampu jadi checklist | dark, left headline | drift | word pill "LOS merah." (L17) |
| OUTRO | `standard_outro` + teaser EP 02 ("WiFi connected, tapi no internet") | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L02: headline bukan narasi — "Masalahnya di *kabel*." (bukan "Tulisannya LOS").
- L07–L08: patchcord di rumah = satu-satunya penyebab LOS yang bisa dicek sendiri; sisanya lapor (L17).
- L13: "akun" = sesi login ISP (PPPoE) — nggak usah sebut PPPoE di layar; tag `login gagal` · `tagihan telat`.
- L14: "kadang" penting — jangan janji restart pasti beres.
- Pertanyaan terbuka: foto lampu modem asli user (opsional) → `assets/modem.jpg`, bisa gantiin kartu di RECAP.
