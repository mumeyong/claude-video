# PLAN — Kenapa ChatGPT kadang ngarang jawaban?

> Fase 1.5. Dua video terakhir: interview-cloud-5-pertanyaan (kartu kuis · flip snappy · teal · kuis ke penonton ·
> **look reel** · marimba/wood) dan jalur-karier-cloud (skill tree · cabang + ring charge · merah · before/after ·
> classic+reel · ambient/soft). Baris terakhir REGISTRY = `look reel` → video ini **classic + reel moves**
> (STYLE §6e, tanpa pengecualian §8: kiri, satu aksen biru, nggak ada hard cut warna).

<!-- registry
pilar: B
metafora: bar saran keyboard HP (tiga kata tebakan di atas keyboard) — AI = versi raksasanya; nggak ada tombol "nggak tahu"
signature: kata teratas di bar saran loncat ke kalimat (bar peluangnya penuh, dua lainnya kempes) — token demi token
look: classic+reel
color: ungu `#7558F0`
hook: eksperimen + klaim nyeleneh (buku yang nggak pernah ada → "Dia nggak bohong. Dia nebak.")
struktur: mekanisme → kenapa kedengeran yakin → 3 kebiasaan (tombol "nggak tahu" dipasang)
komponen: keyboard_hp, suggest_bar, token_line
musik: lofi Eb warm 88 · sfx glass
durasi: 74
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **classic + 3 reel moves**: `count_pill` (hitungan token yang ketebak, bab 00) · `pixel_wipe` ungu masuk bab 02 (satu-satunya) · `pop_card` (3 kartu kebiasaan, bab 02). Warna dikasih signature color; §8 penuh. Beda dari jalur-karier (iris · float_chips · highlight_phrase). |
| Motion (STYLE §6d) | spring `heavy` (keyboard = hero besar, `Rig`) · reveal `ink` · glue persistent hero `Rig` (keyboard pindah/scale antar bab, nggak exit) · exit `mask` — beda dari jalur (silk · mask · Morph · dim) dan interview (snappy · smear · deck persisten · reel) |
| Metafora | keyboard HP yang nebak kata: INTRO (jawaban AI = deretan tebakan), 00 (nanti aku… → pulang), 01 (bar saran tanpa tombol "nggak tahu", data kosong tetap ada tebakan), 02 (tombol "nggak tahu" dipasang + context/sumber), RECAP (bar saran: cepet · ngebantu · di-review) |
| Signature move | kata teratas di `suggest_bar` loncat ke baris teks (`token_line`) — dipakai di INTRO, 00, 01, RECAP |
| Color · hook · struktur | ungu `#7558F0` (bar peluang, slot terpilih, token) · eksperimen buku fiktif · mekanisme → kenapa yakin → 3 kebiasaan |
| Suara (STYLE §7) | style `lofi` · key Eb · mood warm · 88 BPM · sfx kit `glass` (UI HP) — interview marimba/wood, jalur ambient/soft |
| Komponen baru | `components/tebak.py`: `keyboard_hp` · `suggest_bar` · `token_line` — reuse `Rig`, `bubble`, `note`, `word_pill`, `strike`, `pop_tag`, reel moves |
| Sentuhan manusia | artefak: chat ilustrasi buku fiktif (label "ilustrasi") · opini: "AI itu kayak junior yang pede — tetap aku review" · kejutan: tombol "nggak tahu" nggak ada di keyboard, lalu dipasang · ketidaksempurnaan: hand note miring "bukunya nggak ada" + slot kosong bergaris putus |

## Komposisi per bab (STYLE §6b)
| Bab | Hero | Layout | Kamera | Punch / transisi |
|---|---|---|---|---|
| INTRO | kartu chat: pertanyaan buku → jawaban AI ngetik lancar → kata-katanya jadi pill "tebakan" | full-width card | push-in ke jawaban, reset | note "bukunya nggak ada" · headline "Dia *nebak*." |
| 00 · NEBAK KATA | keyboard HP (Rig masuk dari bawah, `heavy`) + baris teks "nanti aku" + bar saran 3 kata → "pulang" loncat | centered hero (no card) | focus bar saran → pull-out pas "raksasanya" (keyboard mengecil ke bawah, token_line panjang di atas) | `count_pill` token · signature move ×4 |
| 01 · KENAPA YAKIN | bar saran besar di tengah, slot ke-4 bergaris putus "nggak tahu" dicoret; bar peluang rata-rata pendek tetap ada pemenang | stacked typography + bar | push-in ke slot kosong, punch-out 0.97 di "hallucination." | keys runtuh → close-up bar · note "hampir rata" · word_pill coral "hallucination." |
| 02 · BIAR NGGAK NGARANG | `pixel_wipe` ungu → 3 `pop_card` kebiasaan miring (context · sumber · izin) + keyboard kecil yang akhirnya punya tombol "nggak tahu" | stacked/tilted cards | drift + focus tiap kartu | tombol "nggak tahu" pop (bookend kejutan) |
| RECAP | bar saran dark: cepet · ngebantu · tetap di-review → "review" loncat ke kalimat | centered hero (dark) | push-in pelan | bookend signature move |
| OUTRO | `standard_outro` + teaser "Kenapa AI bisa lupa obrolan panjang?" | — | — | — |

## Catatan baris (cuma yang nggak kelihatan dari kode)
- L01–L03: buku "Senja di Kota Awan" = judul karangan; jawaban AI ilustrasi (tag "ilustrasi"), tanpa nama penulis.
- L05: pulang · telat · kabarin — tebakan contoh, bukan data keyboard asli. Bar peluang tanpa angka persen.
- L08: count_pill cuma ngitung token di layar (bukan klaim jumlah token asli).
- L12: "hallucination" tetap English (GLOSSARY).
- L16: opini user — ⚠️ cek user setuju.
