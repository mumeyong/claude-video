# PLAN — WiFi connected, tapi no internet. Kok bisa? (Bongkar WiFi Rumah EP 02)

> Fase 1.5. Cek `ideas/REGISTRY.md`: dua video terakhir = biaya-cloud-bocor (meteran token · LED pulsa · teal · angka
> dulu · hitung mundur) dan WiFi EP 01 (jalan cahaya fiber · denyut putus · ungu · cold open · diagnosa per lampu).
> Pilihan 1–5 di bawah beda dari dua itu. Seri: HUD `BONGKAR WIFI RUMAH · EP 02`, `series_bumper` seri, modem EP 01 muncul
> sekali sebagai rujukan (L11) — bukan hero.

<!-- registry
pilar: B
metafora: komplek perumahan — HP = rumah, router = pos satpam di gerbang, palang = sambungan ke ISP, buku alamat satpam = DNS
signature: palang portal komplek naik/turun (heavy spring); amplop "tes" mentok di palang / lolos dan balik
color: oranye `#E8861A`
hook: klaim nyeleneh (penuh × nol — dua-duanya bener)
struktur: satu perjalanan request: rumah → pos → gerbang → buku alamat (penyebab 1, penyebab 2)
komponen: wifi_icon, pos_satpam, buku_alamat
musik: marimba A bright 108 · sfx wood
durasi: 74
-->

## Identitas
| | |
|---|---|
| Motion (STYLE §6d) | spring `heavy` · reveal `mask` · glue `lockup` (PENUH × NOL) + `sheen`/`swap` (buku alamat ganti DNS) + hero entrance full-bleed shrink (ikon WiFi) · exit `mask` — beda set dari EP 01 (silk · ink · Rig/Morph/sheet · dim) |
| Metafora | komplek: 00 (rumah + pos + jalan WiFi), 01 (palang turun = ISP putus), 02 (palang naik, satpam bingung = DNS), RECAP (amplop lolos + balik) |
| Signature move | palang portal: di 00 amplop tes mentok palang → ikon dapat "!" · di 01 palang coba naik, ketahan, turun lagi · di 02 palang naik mulus, amplop berhenti di satpam yang bingung · di RECAP palang naik, amplop keluar dan balik, "!" hilang |
| Color · hook · struktur | oranye `#E8861A` (palang + amplop) · klaim nyeleneh · perjalanan satu request (2 penyebab) |
| Suara (STYLE §7) | style `marimba` · key A · mood bright · 108 BPM · sfx kit `wood` (pos satpam, palang kayu) — EP 01 lofi/glass |
| Komponen baru (QUICK) | `wifi_icon` (kipas 3 bar + titik, bar nyala satu-satu, badge "!") · `pos_satpam` (pos jaga + jendela + satpam + palang dengan pivot, p_open, confused "?") · `buku_alamat` (buku alamat: nama → nomor, scan baris, gagal "?", nomor muncul) — reuse `rumah`, `gang`, `modem` |
| Sentuhan manusia | opini: "yang pertama aku cek itu DNS" (L18) + hand note *it's always DNS* (lelucon orang infra) · kejutan: HP diam-diam ngetes satu alamat (L07) · ketidaksempurnaan: palang yang ketahan setengah naik, note tulisan tangan · artefak: — (screenshot ikon WiFi + "!" dari HP user kalau ada → assets/) |

## Komposisi per bab (STYLE §6b)
| Bab | Hero | Layout | Kamera | Punch / transisi |
|---|---|---|---|---|
| INTRO | `wifi_icon` raksasa full-bleed → mengecil | centered hero, tanpa kartu | hero s 2,3 → 1 (heavy) | bar nyala "penuh" → "!" thud "nol" · `lockup` PENUH × NOL (L02) · garis setengah jalan (L03) → bumper |
| 00 · DUA JALAN | komplek samping: 3 rumah (HP/laptop/TV) + gang + pos satpam + palang + "jalan raya" | full-width scene | pull-out 1,1 → 1, push-in ke palang (L07) | gelombang WiFi rumah → pos · amplop mentok palang · "!" pop di atas rumah HP |
| 01 · GERBANG | pos satpam close-up (palang besar) → modem kecil EP 01 → deret rumah tetangga | centered hero → stacked | push-in ke palang, reset | palang ketahan setengah (heavy) · tag "EP 01 · lampu LOS" · semua rumah dapat "!" satu-satu (massal) · strike "restart" |
| 02 · BUKU ALAMAT | palang naik + satpam "?" → `buku_alamat` full-width | object + hand note → full-width card | pull-out pas buku muncul | scan baris → "?" error stamp · `sheen` + `swap` ke DNS baru, nomor muncul + ✓ |
| RECAP (gelap) | komplek gelap: amplop lewat palang terbuka, ke buku, balik → ikon WiFi besar tanpa "!" (bookend intro) | dark, left headline | drift | word pill "DNS." + note *it's always DNS* |
| OUTRO | `standard_outro` + teaser EP 03 (hujan) | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L03: "setengah jalan" = garis HP → router nyala, router → internet putus-putus "?" — itu janji videonya.
- L07–L08: alamat tes = connectivity check (Android/iPhone) — label amplop cuma "tes", jangan tulis domain.
- L10: tags `kabel putus` · `ISP down` (bukan merek). L11: modem EP 01 dengan INTERNET mati + tag "EP 01".
- L14: baris buku: youtube.com · google.com · instagram.com; nomor disensor (`•••.•••.•.••`), jangan IP asli.
- L16: tags `1.1.1.1` · `8.8.8.8` (di layar aja, nggak dibaca). "buku alamatnya rusak" = DNS server ISP — cukup metafora.
- Pertanyaan terbuka: screenshot ikon WiFi + tanda seru dari HP user (opsional) → `assets/`.
