# PLAN — Kenapa AI lupa isi obrolan yang panjang?

> Fase 1.5 (identitas + komposisi, satu file). **v2 2026-10-13** (feedback user: bagian chat repetitif + mau font gaya Apple): INTRO + 00 = chat UI iOS di HP (`components/obrolan.py`, Inter semua, tanpa serif) + kartu "Model AI" di 00; papan mulai bab 01 (baris Inter). v1 = `out/scenes_v1_papan.py`.
> Beda dari wifi-ep05 (pipa PDAM, teal, before/after, lofi A dreamy,
> flat-big) dan wifi-ep04 (buku tamu, merah, kutipan CS, garage F warm, paper-big).

<!-- registry
pilar: B
metafora: chat HP beneran (intro + 00: tiap kirim, SELURUH thread terbang ke kartu AI, lalu kartu kosong lagi = stateless) → papan tulis kelas (01+) — tiap pesan satu baris; tiap pesan baru seluruh papan dibaca ulang (stateless); papan = context window; papan penuh → baris paling atas dihapus (namamu); obatnya: rangkum di kertas tempel, hapus papan, chat baru
signature: pita baca nyapu papan dari baris pertama sampai terakhir tiap pesan baru; papan penuh → penghapus ngangkat dari tray dan nyapu baris paling atas, tintanya nempel di busa penghapus
look: classic + paper-big
color: oranye `#E8861A`
hook: cold open di tengah kejadian (papan penuh, "nama kamu siapa?" ditulis di baris terakhir)
struktur: problem → turn → result lewat satu papan: baca ulang (stateless) → ukuran papan (context window + GPU memory) → dihapus (namamu) → rangkum + papan bersih
komponen: papan_tulis, penghapus, memori, chat_phone (obrolan.py, v2)
musik: marimba G bright 106 · sfx wood
durasi: 71
-->

## Identitas
| | |
|---|---|
| Look (STYLE §6e) | **classic + Apple craft (default)** — tanpa reel move |
| Material (STYLE §6g) | **paper-big** — papan tulis dari kertas potong (bingkai aluminium = kertas abu, busa penghapus bertekstur), papan ngisi kolom 848 px × ~700 px; video sebelumnya flat-big |
| Motion (STYLE §6d + §6f) | reveal **ink** (headline) · glue **rack_cut** (sekali: hook → "mundur dulu") + papan persisten (`Rig`) · exit quiet · spring smooth/hero (+ snappy buat tag) |
| Apple craft (§6f) | leader tiap bab = papan (baris ditulis / pita baca / penghapus) · hold terpanjang di L13 (dolly) · tempo slow–slow–snap: snap = penghapus nyapu di L10 · kontinuitas antar bab: papan nggak pernah keluar layar |
| Craft v2 (§6f+) | `mark` (lingkaran tangan di "aku Mumei." di hook + di busa penghapus di L11) · `track` (penghapus ganti target: tray → baris atas → bingkai → sapuan recap → tray, tanpa berhenti mati) · `rack_cut` (hook → rewind) |
| Metafora | papan tulis kelas (≥ 3 bab: semua bab + recap) |
| Signature move | pita baca oranye nyapu dari baris 1 sampai terakhir (00, 01, recap) + penghapus nyapu baris atas (intro time-lapse, 02, recap) |
| Color · hook · struktur | oranye `#E8861A` · cold open di tengah kejadian · problem → turn → result |
| Suara (STYLE §7) | style marimba · key G · mood bright · bpm 106 · sfx kit wood (kelas, papan, kapur) |
| Komponen baru (QUICK) | `papan_tulis` (papan + baris + pita baca + garis token), `penghapus`, `memori` (keping RAM GPU memory) — kit `papan.py` |
| Sentuhan manusia | artefak: obrolan liburan ke Bali (contoh, disamarkan) · opini: "chat baru itu bukan mulai dari nol" · kejutan: nama yang dihapus ternyata "Mumei" = *nameless* · ketidaksempurnaan: lingkaran tangan + kertas tempel miring |

## Komposisi per bab (STYLE §6b)
| Bab | Hero (leader) | Layout | Kamera | Punch / transisi (kontinuitas) |
|---|---|---|---|---|
| INTRO | papan penuh (full-bleed shrink), baris "Halo, aku Mumei." dilingkari → time-lapse 1 jam (baris naik & hilang) → "Maaf, nama kamu siapa?" ditulis | headline atas + papan besar | dolly di hold L02 | rack_cut ke 00 ("mundur" ke awal obrolan) |
| 00 · BACA ULANG | papan setengah isi; tiap pesan baru → pita baca nyapu semua baris; tag "dibaca ulang: N baris" | papan + tag kanan atas | cut + dolly | papan tetap, pita jadi signature |
| 01 · CONTEXT WINDOW | bingkai papan ditelusuri garis oranye (= batasnya); garis token di satu baris; papan "dibesarin" (slot 8 → 11, tulisan mengecil) + keping RAM `GPU memory` nyala per baris | papan + RAM di bawah | cut | punch: "Makin panjang, makin *mahal*." |
| 02 · DIHAPUS | papan penuh → penghapus ngangkat dari tray, nyapu baris atas, baris naik, pesan baru masuk; busa penghapus kebawa tinta "Halo, aku Mumei." | papan + catatan tangan | cut + dolly | snap: sapuan penghapus di "dihapus" |
| RECAP | papan di ruang gelap: kertas tempel "Ringkasan" miring nempel → penghapus nyapu semua baris → kertas tempel pindah ke baris 1 papan bersih | papan tengah, headline dark | cut + dolly | bookend: papan yang sama dari hook, kali ini dihapus sengaja |
| OUTRO | `standard_outro` + teaser OTP | — | — | — |

## Catatan baris
- L01: "nama kamu siapa?" mendarat di baris terakhir tepat di kata "nama" (arrive).
- L04/L05: pita baca mulai di "seluruh" / "semuanya" — sebab dan reaksi di frame yang sama.
- L08: angka per model sengaja nggak ditampilkan (nggak ada sumber) — cuma slot + RAM.
- L10: "baris paling atas yang dihapus duluan" = perilaku banyak aplikasi (truncation); ada juga yang ngerangkum otomatis — dicatat sebagai pertanyaan terbuka.
