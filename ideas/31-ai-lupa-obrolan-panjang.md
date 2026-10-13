# Kenapa AI lupa isi obrolan yang panjang?

- **Status:** 🎬 produksi — [`videos/ai-lupa-obrolan-panjang/`](../videos/ai-lupa-obrolan-panjang/)
- **Pilar:** B · AI sehari-hari · **Format:** QUICK
- **Slug:** ai-lupa-obrolan-panjang
- **Seri:** —
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
AI nggak punya ingatan — tiap kamu kirim pesan, seluruh obrolan dibaca ulang, dan mejanya cuma muat segini (context window).

## Hook (opsi)
- A: "Di awal aku udah bilang namaku. Di pesan ke-80, dia nanya lagi."
- B: "Tiap kamu ngetik 'oke', AI baca ulang seluruh obrolan dari awal."

## Bab
1. AI baca ulang seluruh obrolan tiap pesan (stateless)
2. Batas meja: context window (token)
3. Kepanjangan → yang awal kepotong / kurang diperhatiin
4. Sudut infra: makin panjang = makin mahal GPU memory; tips: rangkum, mulai chat baru

## Bukti / visual
Metafora: **papan tulis kelas** — guru nulis terus, papan penuh, tulisan paling atas dihapus biar muat. Signature: penghapus nyapu baris paling atas tiap pesan baru.

## Butuh komponen baru?
- `whiteboard` (baris tulisan + penghapus) · reuse `chat`

## Catatan
- Tetap pakai istilah English: context window, token, prompt. Jangan klaim angka context per model tanpa sumber.
- Mulai: `claude-video 31` atau `claude-video "Kenapa AI lupa isi obrolan yang panjang?"`
