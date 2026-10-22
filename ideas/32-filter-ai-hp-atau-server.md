# Filter AI di kamera HP: diproses di HP atau di server?

- **Status:** 🎬 produksi — [`videos/filter-ai-hp-atau-server/`](../videos/filter-ai-hp-atau-server/)
- **Pilar:** B · AI sehari-hari · **Format:** QUICK
- **Slug:** filter-ai-hp-atau-server
- **Seri:** —
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Filter yang ngikutin wajah real-time diproses di chip HP-mu sendiri; yang "ubah fotomu jadi anime" dikirim ke GPU di data center.

## Hook (opsi)
- A: wajah + filter real-time vs loading "Generating…" 8 detik — "Yang satu di sakumu. Yang satu di gedung lain."
- B: "Kenapa filter tertentu cuma jalan di HP baru?"

## Bab
1. On-device: chip khusus (NPU), cepat, privat, tapi kecil
2. Cloud: model gede di GPU, butuh upload + antre
3. Kenapa ada yang gratis/berbayar (biaya GPU — link #18)
4. Privasi: fotomu ke mana?

## Bukti / visual
Metafora: **printer rumah vs percetakan** — print biasa langsung di rumah, banner gede harus ke percetakan. Signature: foto keluar dari HP kecil vs dikirim jauh dan balik.

## Butuh komponen baru?
- `chip_npu` (chip kecil di dalam HP) · reuse `gpu_card`, `phone`

## Catatan
- ✗ visual robot/otak. Sudut infra, bukan review app.
- Mulai: `souffle 32` atau `souffle "Filter AI di kamera HP: diproses di HP atau di server?"`
