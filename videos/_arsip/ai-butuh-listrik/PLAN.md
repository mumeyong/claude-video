# PLAN — Kenapa AI butuh listrik segede satu kota?

> Fase 1.5. Dua video terakhir: prompt-diproses-di-mana (studio radio · lampu ON AIR + gelombang · oranye · cold open ·
> look reel · garage/mech) dan ai-ngarang-jawaban (bar saran keyboard · kata loncat · ungu · eksperimen + klaim ·
> classic+reel · lofi/glass). Video ini: **classic + Apple craft murni** (tanpa reel move) — beda dari dua-duanya.

<!-- registry
pilar: B
metafora: setrika rumah — satu GPU ≈ dua setrika yang nggak pernah dicabut; data center = gedung isi puluhan ribu setrika (= listrik kota kecil); panasnya harus dibuang (cooling ikut nyedot); gedungnya pindah nyari "colokan" (pembangkit + air)
signature: lampu indikator setrika nyala "klik" → uap panas naik bergelombang dari tapaknya — satu setrika, lalu satu grid, lalu satu gedung · look classic
look: classic
color: coral `#EB6A4A`
hook: angka dulu versi sehari-hari (1 GPU ≈ 2 setrika)
struktur: rantai sebab-akibat 3 mata rantai: nyala barengan → jadi panas → pindah ke colokan
komponen: setrika, uap_panas, pembangkit
musik: marimba F warm 104 · sfx soft
durasi: 74
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **classic + Apple craft (default)** — tanpa reel move (2 video terakhir reel / classic+reel) |
| Motion (STYLE §6d + §6f) | reveal **wipe** (headline) · glue **depth_swap** (GPU → setrika, grid → kota, setrika → gedung) + `focus_pull` (meteran listrik di depan setrika di bab 01) · exit quiet · spring smooth/hero (+ snappy buat tag) — beda dari prompt (smear · sheen/swap) dan ai-ngarang (ink · Rig) |
| Apple craft (§6f) | leader tiap bab: INTRO GPU → 2 setrika · 00 grid setrika (gelombang nyala satu leader dari kiri atas) · 01 setrika besar + uap → meter · 02 gedung data center yang geser ke pembangkit · RECAP satu setrika · hold terpanjang: L06 "kota kecil" (dolly) + L13 "colokannya" · tempo slow–slow–snap: snap di L06 (cut ke "kota kecil.") dan L13 (cut ke steker) · kontinuitas: setrika nggak pernah hilang — `depth_swap` antar ide |
| Metafora | setrika: INTRO (GPU = 2 setrika), 00 (puluhan ribu setrika = kota kecil), 01 (setrika panas → cooling), 02 (gedung setrika nyari colokan), RECAP (satu setrika buat kamu) |
| Signature move | lampu indikator setrika nyala "klik" → uap panas naik dari tapak — INTRO (2 setrika), 00 (gelombang lampu di grid), 01 (uap gede → throttle), RECAP (satu, gelap) |
| Color · hook · struktur | coral `#EB6A4A` (lampu setrika, uap, bar listrik) · angka dulu sehari-hari · rantai sebab-akibat 3 mata |
| Suara (STYLE §7) | style `marimba` · key F · mood warm · 104 BPM · sfx kit `soft` — prompt garage/mech, ai-ngarang lofi/glass |
| Komponen baru (QUICK) | `components/setrika.py`: `setrika` (setrika rumah, side view, lampu indikator + kabel) · `uap_panas` (garis uap bergelombang naik) · `pembangkit` (PLTU/PLTA kecil: cerobong/menara pendingin + uap) — reuse `gpu_card` (EP07) dan `data_center` (radio) di peran baru, `steker` (listrik) buat punch "colokannya" |
| Sentuhan manusia | artefak: perbandingan watt GPU vs setrika (di catatan, bukan di layar) · opini: "nanya boleh, tapi nggak gratis" · kejutan: data center pindah ke colokan, bukan ke kota · ketidaksempurnaan: hand note miring "panas, bukan pinter" + tag yang agak miring |

## Komposisi per bab (STYLE §6b)
| Bab | Hero (leader) | Layout | Kamera | Punch / transisi (kontinuitas) |
|---|---|---|---|---|
| INTRO | `gpu_card` mendarat di "GPU" (full-bleed shrink) → `depth_swap` ke 2 setrika di "setrika", lampu klik | centered hero (tanpa card) | dolly di L02 | headline "Segede *satu kota*?" di L02 |
| 00 · NYALA BARENGAN | grid 6×5 setrika kecil, lampunya nyala gelombang di "puluhan ribu" | full-width grid | dolly di L05 → cut di L06 | **cut** ke "kota kecil." (headline_lg) + garis kota dari jendela nyala |
| 01 · JADI PANAS | satu setrika besar, uap naik di "panas" → tag throttle → bar listrik (GPU + cooling) di depan (`focus_pull`) | object + hand note → focus sheet | push ke bar di L10 | bar cooling tumbuh di "nambah lagi" |
| 02 · PINDAH KE COLOKAN | `data_center` geser dari kota (kiri) ke `pembangkit` + garis air (kanan) di "pembangkit" | lanskap horizontal | — (hero yang gerak) → cut di L13 | **cut** ke `steker` besar + "colokannya." |
| RECAP (dark) | satu setrika, lampu nyala di "buat kamu" | centered hero gelap | dolly | headline "Jawabannya *nggak gratis*." |
| OUTRO | `standard_outro` (+ save) | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01: ⚠️ "dua setrika" = GPU kelas H100 ±700 W (TDP spec NVIDIA) vs setrika rumahan ±300–400 W. Nggak ada watt di layar.
- L04: ⚠️ "puluhan ribu GPU" — buat kampus AI terbesar (laporan publik 2024–2025 nyebut 100 rb+); di layar cuma kata, bukan angka.
- L06: ⚠️ "kota kecil" — puluhan ribu GPU + server + cooling ≈ ratusan megawatt (sumber: IEA Energy and AI 2025). Di layar tanpa angka.
- L08: throttle = GPU nurunin clock sendiri kalau suhunya lewat batas (thermal throttling).
- L10: cooling nambah listrik (PUE > 1) — tanpa angka persen.
- L11–12: contoh nyata ada (data center dekat pembangkit nuklir / PLTA, butuh air) — narasi nggak nyebut nama perusahaan.
