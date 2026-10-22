# Postmortem: malam waktu production mati

- **Status:** 🎬 produksi — [`videos/postmortem-production-mati/`](../videos/postmortem-production-mati/)
- **Pilar:** D · deep · **Format:** FULL
- **Slug:** postmortem-production-mati
- **Seri:** — (kandidat Season 2 Bongkar)
- **Durasi target:** 75–90 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Sistem pasti pernah jatuh — yang bikin tim jago adalah cara mereka bongkar kejadiannya tanpa nyalahin orang.

## Hook (opsi)
- A: "Jam 21.47, satu perubahan kecil bikin production mati 38 menit." (angka asli, disamarkan)
- B: "Bukan salah orangnya. Ini salah sistemnya."

## Bab
1. Kejadian: timeline menit per menit
2. Akar masalah (5 why)
3. Yang diubah setelahnya: guardrail, alert, runbook
4. Blameless postmortem — kenapa ini budaya, bukan dokumen

## Bukti / visual
Metafora: **kotak hitam pesawat** — setelah kejadian, rekamannya diputar ulang. Signature: kotak oranye kebuka, timeline diputar mundur-maju.

## Butuh komponen baru?
- `blackbox` (flight recorder oranye) · `incident_timeline` (menit per menit, rewind)

## Catatan
- ❓ butuh insiden asli dari user (klien disamarkan, angka asli). Tanpa itu jangan diproduksi.
- Mulai: `souffle 35` atau `souffle "Postmortem: malam waktu production mati"`
