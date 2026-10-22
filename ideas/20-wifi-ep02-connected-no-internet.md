# WiFi connected, tapi no internet. Kok bisa?

- **Status:** ✅ tayang → [`videos/_arsip/wifi-ep02-connected-no-internet/`](../videos/_arsip/wifi-ep02-connected-no-internet/)
- **Pilar:** B · broad · **Format:** QUICK
- **Slug:** wifi-ep02-connected-no-internet
- **Seri:** #14 Bongkar WiFi Rumah — EP 02
- **Durasi target:** 60–75 s
- **Ditambahkan:** 2026-10-09

## Takeaway (1 kalimat)
Ikon WiFi penuh cuma berarti HP-mu nyambung ke router — jalan dari router ke internet itu cerita lain, dan kamu bisa ngecek bagian mana yang putus.

## Hook (opsi)
- A: ikon WiFi full + tanda seru kecil — "Sinyalnya penuh. Internetnya nol. Dua-duanya bener."
- B: (gangguan massal) "Kemarin jutaan orang lihat ikon ini. Ini yang sebenernya kejadian."

## Bab
1. Yang kamu lihat: ikon penuh, tanda seru, app nggak mau loading
2. Yang sebenernya kejadian: HP → router (lancar) · router → ISP (putus / DNS / IP nggak dapet)
3. Cek dari layer paling dekat: buka 192.168.1.1, cek lampu modem (link ke EP01), coba DNS lain
4. Teaser EP03: lemot pas hujan

## Bukti / visual
Metafora: **intercom apartemen** — kamu nyambung ke resepsionis lobby (router), tapi telepon keluar dari lobby lagi mati. Signature: sinyal jalan sampai lobby, lalu mantul balik.

## Butuh komponen baru?
- `intercom` (lobby + kabel keluar) · `wifi_icon` (bars + tanda seru) — reuse `modem` dari EP01

## Catatan
- Bisa dinaikin duluan kalau ada gangguan massal (slot berita #09). Jangan nyalahin merek ISP.
- Mulai: `souffle 20` atau `souffle "WiFi connected, tapi no internet. Kok bisa?"`
