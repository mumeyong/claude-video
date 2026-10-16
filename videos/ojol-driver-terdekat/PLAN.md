# PLAN — Gimana ojol nemuin driver terdekat dalam 3 detik?

> Written BEFORE film.html (STYLE §2): the idea + how the frame is built. Then `python -m engine register <slug>`.

<!-- registry
pilar: B
metafora: peta kota kertas yang dipotong kotak (tribun stadion dibagi sektor) — titik kamu di tengah, driver = chevron
signature: kotak hexagon nyala cincin demi cincin melebar dari titikmu (intro sekilas, bab 01 penuh, recap seluruh kota)
look: paper — peta cetak krem, tinta navy, satu aksen
color: ultramarine `#4B2BFF`
hook: tombol Pesan dipencet → sekota penuh driver, kok bisa milih secepat itu?
struktur: satu peta + satu kamera dari awal sampai akhir: zoom-out kota → grid kotak (geohash) → hexagon (H3) → cincin melebar → street level balapan 2 driver → satu kotak kehujanan → seluruh kota nyala
komponen: — (semua di film.html: hex grid, driver chevron, route race, rain)
musik: marimba G bright 108 · sfx soft
durasi: ~66 s suara (+ sting + logo penutup)
-->

## Idenya
Satu peta kota dari atas, kayak peta cetak di kertas krem. Titik kamu (ultramarine) di tengah, chevron-chevron driver
di mana-mana. Kamera nggak pernah cut — cuma zoom dan geser di atas peta yang sama. Pertama kotanya kelihatan penuh
(masalahnya: ngitung ke semua itu lambat), lalu peta dipotong kotak kayak tribun stadion (label sektor A1, B2…),
kotaknya berubah jadi hexagon (H3), dan pencarian melebar cincin demi cincin dari kotakmu — itu signature-nya.
Terus turun ke level jalan: driver terdekat ngadep jalan satu arah yang salah, yang lebih jauh searah dan nyampe
duluan. Lalu hujan di satu kotak: pin pesanan numpuk, tarif naik, driver kotak sebelah ketarik masuk. Penutup: seluruh
kota nyala hexagon — "peta yang dipotong kotak." Rasanya di akhir: "oh, ternyata app-nya nyari kotak, bukan jarak."
Konsep umum spatial index — nggak ada klaim internal Gojek/Grab, nggak ada angka.

## Frame
- Type: **Bricolage Grotesque 800** (display, besar dan pendek) + **IBM Plex Mono 500** (label peta, chip, marginalia).
  Bukan Inter. Teks sebisa mungkin nempel di peta (label sektor, chip di driver, chip di kotak).
- Chrome: none — `v.hud = False`, nggak ada kicker bab. Kertas + grain halus.
- Per bab, komposisi beda (STYLE §2):
  - INTRO: UI as object — tombol pill "Pesan" besar di bawah, peta close-up; lalu macro → reveal ke seluruh kota,
    type "secepat / itu?" kiri atas.
  - 00: top-down diagram — garis jaring dari kamu ke semua driver + "satu-satu?" dicoret; lalu grid kotak menyapu
    keluar, type bawah "sektor."; label sektor tercetak di kotak + tag di tiap driver (text on object); "geohash" →
    "H3" di bawah sementara peta naik ke separuh atas dan kotak berubah jadi hexagon.
  - 01: macro di kotakmu, cincin nyala satu-satu, chip di peta ("kotakmu", "cincin 1 · kosong", "cincin 2");
    lalu bottom-anchored "langsung ke / sektornya." dengan "teriak ke semua" dicoret.
  - 02: street level full-bleed — jalan satu arah (panah), dua rute digambar, balapan, stempel DIPILIH, "duluan." besar
    di bawah; "terdekat ≠ dipilih." di atas.
  - 03: satu kotak memenuhi frame + hujan miring, pin pesanan numpuk, chip "tarif ↑", driver kotak sebelah meluncur masuk.
  - RECAP: seluruh kota, hexagon nyala melebar; type is the picture di tengah "peta yang / dipotong / kotak."
    (kertas terang, bukan recap gelap + serif).
  - OUTRO: rute muter-muter beraksen, "muter jauh?" di bawah → logo penutup.
