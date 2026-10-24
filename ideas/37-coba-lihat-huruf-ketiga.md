# Coba lihat huruf ketiga

- **Status:** 🎬 produksi — [`videos/coba-lihat-huruf-ketiga/`](../videos/coba-lihat-huruf-ketiga/)
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** coba-lihat-huruf-ketiga
- **Seri:** —
- **Durasi target:** 60–70 s
- **Ditambahkan:** 2026-10-13

## Takeaway (1 kalimat)
Ada huruf yang kelihatan sama persis tapi beda karakter — link phishing bisa niru alamat asli sampai ke titiknya.

## Hook (opsi)
- A: "Link ini 100% kelihatan kayak tokopedia.com. // Coba zoom huruf ketiga."
- B: "Dua link ini beda. // Kamu bisa nemuin bedanya?" (dua URL identik, penonton ditantang)

## Bab
1. Dua URL yang kelihatan identik
2. Kaca pembesar: tiap huruf punya nomor identitas (Unicode) — "a" Latin vs "а" Cyrillic beda nomor
3. Topeng kebuka: alamatnya sebenernya `xn--…` (punycode)
4. Cara cek cepat sebelum login / bayar

## Bukti / visual
Murni tipografi: kamera makro nyelam ke huruf, loupe nge-rontgen huruf → kode di baliknya. Alamat "buka topeng" jadi punycode.

## Butuh komponen baru?
- `loupe` (lensa pembesar + x-ray huruf → code point) · `url_bar`

## Catatan
- ⚠️ cek fakta: browser mana sekarang nampilin punycode vs huruf mirip (aturannya berubah dari tahun ke tahun) — tes sendiri di Chrome / Safari / browser in-app.
- Jangan pakai domain phishing asli yang aktif; contoh dibikin sendiri / disamarkan. Nama brand di contoh → cek boleh atau pakai nama fiktif.
