# Kubernetes bukan jawaban buat semua hal — format QUICK

> Pilar: C (karier/opini) · target 60–75 s (≈ 185 kata) · ide: [ideas/05-kubernetes-bukan-jawaban.md](../../ideas/05-kubernetes-bukan-jawaban.md)
> Hero: pelabuhan peti kemas (Kubernetes) — crane = scheduler, lapangan = node, peti = container — vs kurir motor
> bawa satu paket (VM biasa / serverless). Bab 03 = checklist 3 pertanyaan (save-able).
> Satu hal yang cuma Mumeyong bisa bilang: dia pernah bangun Kubernetes yang nahan 10.000 request barengan (Bongkar
> Arsitektur EP 01, asli) — justru karena itu dia tahu kapan Kubernetes *nggak* perlu (L03–L04). Opini, mancing komentar.
> Fakta (aman, umum): control plane, monitoring, upgrade versi rutin (Kubernetes rilis beberapa kali setahun),
> skill tim = biaya tersembunyi. Nggak ada angka harga.
> Anti-slop: tanpa "Di era digital", "Tahukah kamu", "Yuk simak". Tech terms English (GLOSSARY.md).
> Read-aloud marks: *kata* = tekanan, ' //' = napas.
>
> HOOK — A/B/C (A terpasang):
> A · Mitos dicoret: "Bikin app baru? Pakai Kubernetes aja." → dicoret → "Tergantung."
> B · Pengalaman: "Aku pernah bangun Kubernetes buat sepuluh ribu request barengan. Kebanyakan app nggak butuh itu."
> C · Pertanyaan spesifik: "App kamu cuma satu, usernya ratusan. Kenapa harus Kubernetes?"

## INTRO
[L01] Bikin app baru? Pakai *Kubernetes* aja.
[L02] Jawaban jujur orang cloud: *tergantung*. //
[L03] Aku pernah bangun Kubernetes yang nahan *sepuluh ribu* request barengan.
[L04] Justru karena itu, aku tahu kapan dia *nggak* perlu.

## 00 · PELABUHAN
[L05] Kubernetes itu kayak *pelabuhan* peti kemas.
[L06] Ada crane, ada lapangan, ada jadwal yang ngatur ratusan *container* tiap hari.
[L07] Kapalnya banyak, muatannya naik turun? Pelabuhan itu *juara*. //

## 01 · SATU PAKET
[L08] Tapi app kamu cuma satu, *user*-nya masih ratusan.
[L09] Itu kayak kirim *satu paket*, tapi sewa pelabuhan lengkap.
[L10] Cukup *kurir*: VM biasa, atau serverless yang bayarnya per request. //

## 02 · BIAYA DIAM
[L11] Yang jarang dibahas: pelabuhan harus *dijaga*, walau lagi sepi.
[L12] Control plane, monitoring, upgrade versi tiap *beberapa bulan*.
[L13] Dan orang yang *ngerti* ngurusnya. Itu yang paling *mahal*. //

## 03 · TIGA PERTANYAAN
[L14] Sebelum pilih, jawab *tiga* ini.
[L15] Service-nya *banyak*? Traffic-nya naik turun *ekstrem*? Ada tim yang siap *jaga*?
[L16] Tiga-tiganya iya? Baru *Kubernetes*. //

## RECAP
[L17] Kubernetes itu alat yang hebat. Tapi alat dipilih buat *masalahnya*, bukan buat *trennya*.

## OUTRO
[L18] Kamu tim pelabuhan, atau tim kurir? Tulis di *komentar*.
[L19] Follow, biar nggak ketinggalan.
