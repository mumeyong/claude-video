# Kenapa transfer antar bank kadang "sedang diproses"?

- **Status:** 💡 ide
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** transfer-antar-bank
- **Seri:** —
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Transfer antar bank lewat jalur yang beda-beda — ada yang langsung (BI-FAST), ada yang dikumpulin dulu lalu diberangkatin barengan.

## Hook (opsi)
- A: status "Sedang diproses" jam 23.40 — "Uangnya nggak hilang. Dia lagi nunggu bus."
- B: "Kenapa transfer 2.500 bisa langsung, tapi yang gede nunggu?"

## Bab
1. Jalur langsung vs jalur batch (dikumpulin per jadwal)
2. Kenapa ada limit / jam operasional
3. Kalau "diproses" lama: uang di mana? (tertahan, bukan hilang)
4. Yang bisa kamu lakuin: simpan bukti, cek jalur yang dipilih

## Bukti / visual
Metafora: **ojek vs bus antar kota** — ojek berangkat langsung, bus nunggu penuh/jadwal. Signature: uang naik bus yang belum berangkat, jam terminal jalan.

## Butuh komponen baru?
- `bus_terminal` (jadwal keberangkatan) · reuse `cashier`/`ledger` beda fungsi

## Catatan
- ⚠️ cek fakta WAJIB: BI-FAST, SKN, RTGS — limit, jam, biaya 2026. Beda dari bank-down (itu soal app crash).
- Mulai: `claude-video 29` atau `claude-video "Kenapa transfer antar bank kadang "sedang diproses"?"`
