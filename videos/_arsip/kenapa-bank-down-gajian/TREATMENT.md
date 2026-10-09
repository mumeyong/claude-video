# TREATMENT — Kenapa app bank down pas tanggal gajian?

> From IDENTITY.md: metaphor **kasir supermarket tanggal muda + satu buku kas** · signature move **lembar disobek** ·
> color **merah `#F03B4F`** · hook **cold open di tengah kejadian** · structure **detektif: 3 tersangka → pelaku → obat**.
> HUD `MUMEYONG · KASUS`, no series bumper. Format QUICK (one hero world, changing state).
> Cover (`v.cover_t`): L12, the PELAKU stamp on the ledger.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **tear_calendar** (21→25 torn in a burst, 25 hand-circled, `09.01`) + **phone**: app bank spinner, "Gaji masuk" notification → whip to the **suspect board**: 3 blank cards `?` + red string | object pair (tilted calendar + phone), then board | push on the phone at "muter" | calendar/phone whip left, cards pop in stagger |
| 00 TERSANGKA | **suspect board** continues: card 1 reveals `KASIR · server` (+ hand note), card 2 reveals `ETALASE · app` → torn off the board (signature) → **traffic** line for October draws under the board, spike on 25 | stacked tilted cards | push on card 1, then card 2, reset for the traffic line | card tears and falls; traffic line draws |
| 01 PELAKU | **supermarket from above**: 2 cashiers → 20 cashiers (`auto-scaling`) → *surprise* pull-out: every lane runs into **one ledger** (`database`, `1 pintu`), queue jams → payroll envelopes pour in, ledger overheats → **PELAKU** stamp slams | centered hero, no card | tight on the cashiers (1.25) → pull-out 1.0 → punch-out on the stamp | board blurs out; stamp slam |
| 02 OBATNYA | **ledger + its photocopies**: three sheets torn off the ledger (signature) fly right → `read replica`; "cek saldo" queue walks to the copies; the original only gets `transfer` · `bayar` · `gaji masuk`, cools down ✓ | two columns (TULIS / BACA) | push on the replicas, then on the original | sheets tear & fly |
| RECAP (dark) | calendar returns, still on **25** (bookend) + outline **10.000** · then `auto-scaling` struck through above 20 mini cashiers that all funnel into one hot ledger | object + number → centered diagram | punch on 10.000; push on the ledger | whip |
| OUTRO | logo + **next video** card (Bongkar Arsitektur EP01 · 10.000 request) + follow | centered | — | — |

## New components (engine/components/payday.py)

| Component | What it does |
|---|---|
| `tear_calendar` | desk calendar (red band, rings, page stack); pages torn off one by one from t0 and fall (gravity + spin); hand-drawn marker loop around the date; mono sub line (`09.01`) |
| `suspect_card` + `pin` + `red_string` | polaroid suspect card: `#01`, photo (`?` until revealed → icon), name, tech-term tag; `tear` rips it off the board leaving a scrap under the pin; red string sags pin to pin |
| `cashier` | top-down checkout counter: belt with moving items, blinking register, cashier |
| `queue_dots` | people walking along a path; `jam` makes them slow and bunch at the end |
| `ledger` / `paper_sheet` | open ledger book (buku kas) with entries, a scribbling pen, `hot` overload glow; loose sheet = photocopy (read replica) |
| `torn_flight` | the shared "torn sheet falls away" motion (dx, dy, rot, alpha) |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Tanggal *25*, 09.01.` | calendar pages 21–24 torn in a burst → 25; marker loop; `09.01` | tick×4, pop | "dua", "sembilan" |
| L02 | `Gaji masuk. App *muter*.` | phone: "Gaji masuk" notification drops; balance hidden, spinner grows | pop, whoosh | "gaji", "muter" |
| L03 | `Tiga tersangka. *Satu* pelaku.` | whip → board: 3 `?` cards pop in, red string draws; card 3 framed red at "satu" | whoosh, pop×3, thud | "tiga", "satu" |
| L04 | `Server *kurang*?` | card 1 reveals: cashier counters · `KASIR` · `server` | pop | "pertama" |
| L05 | `Setengah *benar*.` | hand note "cukup buat hari biasa" → arrow to card 1 | — | "setengah" |
| L06 | `App-nya *jelek*?` | card 2 reveals: phone storefront · `ETALASE` · `app` | pop | "kedua" |
| L07 | `Yang beda: *traffic*.` | "Bukan." card 2 torn off & falls · October traffic line draws, spike at 25 | whoosh, tick | "bukan", "traffic" |
| L08 | `Kasir *tanggal muda*.` | tight on 2 cashiers with queues | whoosh | "kasir" |
| L09 | `Tambah jadi *20*.` | counters pop to a 5×4 grid; tag `auto-scaling` | pop×n | "ditambah", "auto" |
| L10 | `Buku kasnya *satu*.` | camera pulls out: all lanes run down to ONE ledger | whoosh | "satu" |
| L11 | `Satu *pintu*.` | tags `database` + `1 pintu`; queue jams at the ledger | pop, pop | "database", "pintu" |
| L12 | `Ini *pelakunya*.` | payroll envelopes pour in from the side; ledger overheats; stamp **PELAKU** | thud | "gaji", "sama" |
| L13 | `Pisahin *baca* sama tulis.` | ledger left (TULIS), empty dashed slot right (BACA) | whoosh | "baca" |
| L14 | (same) | three sheets torn off → fly to the right column; tag `read replica`; "cek saldo" queue moves to copies | whoosh×3, pop | "replica" |
| L15 | `Aslinya cuma buat *nulis*.` | original cools; tags `transfer` · `bayar` · `gaji masuk`; ✓ | pop×3, chime | "transfer", "bayar", "gaji" |
| L16 | `Pernah aku *tahan*.` | dark: calendar on 25 (bookend) + outline `10.000` fills, mono `request barengan` | whoosh_dark, thud | "sepuluh" |
| L17 | `Masalahnya *satu pintu*.` | pill `auto-scaling` struck through; 20 mini cashiers funnel into one hot ledger | click, thud | "nggak", "pintu" |
| L18 | — | logo + next-video card (EP01) | pop | "berikutnya" |
| L19 | — | `+ Follow` click | click, chime | "follow" |
