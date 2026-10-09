# TREATMENT — QRIS: apa yang terjadi setelah kamu scan?

> From IDENTITY.md: metaphor **lari estafet** (tongkat = pesan transaksi) · signature move **freeze → slow-motion
> replay** (badge `REPLAY 0,1×`, crawling timecode, baton with motion trail) · color **ungu `#7558F0`** · hook
> **freeze-frame momen sehari-hari** · structure **replay: asli → pelan per pelari → twist**. HUD `MUMEYONG · REPLAY`.
> Facts kept general (no bank/switching names, no millisecond claims; the timecode is illustrative).
> Cover (`v.cover_t`): L11, the switching hub.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **warung counter**: QRIS standee + es teh → phone: scan → PIN → ✓ beep (real speed) → **freeze** "TAHAN" → the **relay track** draws in with 4 runners | object pair → phone → track | push on the standee; punch on beep; hold on freeze | phone rises; whip; track draws |
| 00 APP KAMU | baton → runner 1 (slow-mo) · **QR + decoded fields** (merchant, NMID, acquirer, nominal) + tag "bukan uang" | QR left + fields card right, track below | push on the fields | whip |
| 01 ISSUER | baton → runner 2 · **bank card**: balance, ✓ PIN, ✓ saldo, Rp5.000 ditahan (balance drops) | full-width card | push on the hold row | whip |
| 02 SWITCHING | baton → runner 3 · **mesh vs hub**: 6 banks wired one-to-one (mess) → one hub "switching" with spokes | centered object, no card | pull-out on the mesh, push on the hub | pop |
| 03 ACQUIRER | baton → runner 4 · bank warung "OK ✓" + **seller's phone** rings "Pembayaran masuk" · reply pulse runs back along the track → "berhasil ✓" at runner 1 | card + phone, track below | push on the phone, pull-out for the reply | whip |
| RECAP (dark) | big **baton = pesan** → two banks, a money bundle crawling between them: `settlement · belakangan` → track with runner 3 red, baton stuck, timer counting | centered object → diagram → track | push on the bundle | whip |
| OUTRO | logo + next video (EP02 big data migration) + follow | centered | — | — |

## New components (engine/components/relay.py)

| Component | What it does |
|---|---|
| `qr_code` | QR-looking square: 3 finder patterns + hash-seeded modules, reveal top→bottom |
| `qris_stand` | acrylic QRIS standee on a counter: purple header, merchant name, QR, NMID |
| `es_teh` | plastic cup of iced tea: amber tea, ice, straw, condensation |
| `relay_track` | running track with numbered runner tokens + labels, baton (with slow-mo trail), reply pulse right→left, lagging runner in red |
| `slowmo_badge` | dark pill: ▶ `REPLAY 0,1×` + timecode, or ❚❚ `TAHAN` when frozen |
| `mesh_hub` | n banks: every-to-every lines (mess) → one hub with spokes and packets |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Es teh *lima ribu*.` | counter: standee + es teh | pop×2 | "teh", "QRIS" |
| L02 | `*Beep*. Kelar.` | phone: scan line → PIN dots → ✓ Rp5.000 | tick, key×6, chime | "scan", "PIN", "beep" |
| L03 | `*Tahan*.` | freeze: dim, pause bars, badge TAHAN | thud | "tahan" |
| L04 | `Estafet *empat* pelari.` | track draws, 4 runners pop; badge REPLAY 0,1× | whoosh, pop×4 | "estafet", "empat" |
| L05 | `App-mu *baca* kodenya.` | baton → 1 · QR with scan beam | whoosh | "baca" |
| L06 | `Isinya cuma *data*.` | fields typed: merchant · NMID · acquirer · nominal; tag "bukan uang" | key, pop | "uang", "warung", "mana" |
| L07 | `Bank kamu: *issuer*.` | baton → 2 · issuer card | whoosh | "issuer" |
| L08 | `Cek, lalu *tahan*.` | ✓ PIN · ✓ saldo · Rp5.000 ditahan, balance drops | pop×2, tick | "PIN", "saldo", "nahan" |
| L09 | `*Switching*.` | baton → 3 · 6 bank nodes | whoosh | "switching" |
| L10 | `Tanpa dia: *ruwet*.` | every-to-every lines draw | tick×n | "satu" |
| L11 | `Satu *jalan tol*.` | mesh fades, hub + spokes + packets | thud, chime | "tol" |
| L12 | `Bank warung: *acquirer*.` | baton → 4 · acquirer card "OK" | whoosh | "acquirer" |
| L13 | `HP penjual *bunyi*.` | seller phone notification + sound arcs | chime | "bunyi" |
| L14 | `Jawabannya *balik*.` | reply pulse runs back → "berhasil ✓" at runner 1 | whoosh, chime | "balik" |
| L15 | `Cuma *pesan*.` | dark: big baton tagged "pesan" | whoosh_dark, thud | "pesan" |
| L16 | `Uangnya *belakangan*.` | two banks, money bundle crawls: settlement | tick | "settlement" |
| L17 | `Satu lemot, *semua* nunggu.` | track: runner 3 red, baton stuck, timer counts | thud | "lemot" |
| L18 | — | logo + next-video card (EP02) | pop | "berikutnya" |
| L19 | — | `+ Follow` click | click, chime | "follow" |
