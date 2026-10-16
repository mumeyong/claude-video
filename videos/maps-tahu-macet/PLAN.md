# PLAN — Google Maps tahu jalan macet dari mana?

> Written BEFORE film.html (STYLE §2): the idea + how the frame is built. Then `python -m engine register maps-tahu-macet`.

<!-- registry
pilar: B
metafora: jalan aspal malam dilihat dari atas — tiap HP = satu titik cahaya; gerobak isi 99 titik (Berlin 2020)
signature: jalan dicat ulang DI BELAKANG titik-titiknya — titik lambat ninggalin jejak merah, titik cepat jejak hijau (cat jejak = warna Maps)
look: flat-big — aspal gelap, marka putih, warna lalu lintas datar (tanpa glow)
color: merah lampu rem `#F2433A` (+ hijau `#2FBF71`, kuning `#FFB020`)
hook: jalan kosong, gerobak 99 HP lewat pelan, jalannya jadi merah
struktur: gerobak (cold open) → macro satu titik → banyak titik dirata-rata → kalender minggu lalu → jalan sepi + gerobak balik → zoom-out kota = kita semua
komponen: — (film.html sendiri: roadPaint trail, cart, phone dot)
musik: lofi F dreamy 84 · sfx wood
durasi: 66
-->

## Idenya
Malam, dilihat dari atas: satu jalan aspal, sepi. Gerobak kecil isi titik-titik putih (HP) ditarik pelan — dan jalan di
belakangnya dicat merah, padahal nggak ada mobil. Itu kuncinya: **warna jalan = jejak kecepatan titik-titik**. Satu
titik dibesarin sampai jadi HP; titiknya kehilangan nama. Banyak titik melambat barengan → cat merah; satu titik
berhenti beli cilok → cat tetap hijau. Prediksi = empat lembar "jalan yang sama, jam yang sama" minggu lalu ditumpuk
jadi satu. Penutup: kamera mundur, seluruh kota ternyata digambar oleh titik — "itu kita". Rasa akhirnya: geli + sedikit
"oh, aku ikut bikin garis merah itu".

## Frame
- Type: **Archivo Black** (display, kapital, rapat, 150–260 px) + **IBM Plex Mono** (data kecil: label titik, jam,
  caption pojok). Tanpa Inter. Type duduk DI ATAS aspal seperti marka jalan (putih, kapital) atau di pojok sebagai
  caption mono — tidak ada headline melayang kiri-atas.
- Chrome: tanpa HUD. Satu tanda sendiri: pin kecil mono di pojok kanan-bawah "BAB 01 · MERAH" seperti label skala peta.
- Per bab, komposisi beda (STYLE §2):
  - INTRO: **full-bleed top-down** — jalan vertikal penuh frame, gerobak naik dari bawah, jejak merah di belakang.
    Type = marka jalan: "99 HP" dicat di aspal (seperti tulisan BUS/STOP), caption mono "BERLIN · 2020" kecil.
    L03: kamera dolly ke satu titik di gerobak.
  - 00 SENSOR: **macro → reveal** — satu titik raksasa di tengah = HP; label "posisi" berpindah, garis antar posisi
    = kecepatan; label nama dicoret jadi "titik". Type bottom-anchored mono + satu kata besar "TITIK".
  - 01 MERAH: **diagonal full-bleed** — jalan miring 3 lajur, banyak titik. Satu berhenti (balon kecil "cilok"),
    cat tetap hijau. Lalu semua melambat → segmen jadi merah. Kata "MERAH" dicat di aspal mengikuti miringnya jalan.
  - 02 PREDIKSI: **grid/bento** — 4 strip jalan horizontal bertumpuk (label mono "−4 MGG … −1 MGG", jam yang sama,
    tanpa angka kecepatan), lalu strip "SEKARANG" masuk, semua melebur jadi satu strip tebakan. Type kiri, rata kiri.
  - 03 CELAH: **split atas/bawah** — atas: jalan sepi, satu titik, cat putus-putus pucat ("datanya tipis"). Bawah:
    gerobak balik, jalan kosong merah. Kata "MACET" pakai tanda kutip besar.
  - RECAP: **zoom-out kota** — grid jalan seluruh frame, ribuan titik kecil, jalan-jalan berwarna; satu baris putih di
    tengah bawah "itu kita."
