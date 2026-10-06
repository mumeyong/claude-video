# TREATMENT — Kenalan: aku Mumeyong (video intro channel)

> From IDENTITY.md: metaphor **architect's floor plan** · signature move **lines draw first, then fill (become real)** ·
> color **teal `#0E9AAB`** · hook **specific question** · structure **intro → 3 numbers → channel map**.
> Numbers are real (CV / mumeyong.dev). HUD `MUMEYONG · KENALAN`, no series bumper.
> Cover (`v.cover_t`): L04 — giant "Mumeyong." filled.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **blueprint paper**: 3 phone wireframes (bank · ticket · QRIS) draw on → lines converge to a dashed `server ?` box → box fills teal: `cloud` + tag `cloud engineer` | full-width blueprint card | push on the `?` box at "kerjaanku" | card rises |
| 00 KENALAN | giant outline → filled **"Mumeyong."** → **bp_house** floor plan draws itself (one wall drawn wrong, crossed, redrawn) → annotations: server room · dashed route · bill meter + dimension → **then/now**: `2020 · jagain server` (rack) vs `sekarang · mutusin` (dashed server + ✓ / ✕) | pure type → plan card → two columns | push into the plan; push on ✓ | name blurs out up; plan whips left; columns rise |
| 01 TIGA ANGKA | three stacked **slots**: `4` cloud (+ 4 provider tags) · `10.000` request barengan ✓ · `$14.000` → "per bulan." — every number outline first, then filled | stacked typography | punch-out on "bulan" | slots pop stagger |
| 02 DI SINI | *surprise*: tight on a small house → pull out → **city_map** of the channel: blocks = upcoming videos, "kamu di sini" pin; blocks light up as named | map (full card) | pull-out 1.22 → 1.0 | map fades in under the house |
| RECAP (dark) | **classic blueprint** (light lines on dark): plan with one room missing → at "pas" the room slides into its slot, clicks, fills | centered object | push on the slot | plan draws on |
| OUTRO | logo + **next video** card (bank down pas gajian) + follow | centered | — | — |

## New components (engine/components/blueprint.py)

| Component | What it does |
|---|---|
| `bp_grid` | blueprint paper card: minor/major teal grid |
| `bp_house` | floor plan: walls draw progressively, doors/windows, rooms fill; `scribble` = wrong wall crossed out; `fit` = one room slides into its slot; returns room rects for annotations |
| `outline_text` | text whose outline draws left→right, then fills (signature move) |
| `dimension` | architect's dimension line: ticks + label |
| `phone_wire` | wireframe phone that draws on, with a bank-card / ticket / QR glyph |
| `city_map` | grid of blocks + streets; each block draws on, lights teal, label; optional "kamu di sini" pin |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Bank. Tiket. *QRIS*.` | blueprint card; phones draw on at each word | pop×3 | "bank", "tiket", "QRIS" |
| L02 | `Jalan *di mana*?` | lines from phones converge on dashed `server ?` box | whoosh | "mana" |
| L03 | `Itu *kerjaanku*.` | box fills teal → `cloud`; tag `cloud engineer` | thud, pop | "kerjaanku" |
| L04 | — (the name is the headline) | giant outline "Mumeyong." draws → fills; mono `cloud engineer · mumeyong.dev` | whoosh, thud | "Mumeyong" |
| L05 | `Aku gambar *denahnya*.` | plan draws itself; wrong wall crossed + redrawn; tags `developer → rumahnya` · `aku → denahnya` | tick×n, pop | "developer", "denahnya" |
| L06 | (same) | server box in a room · dashed route from the door · bill meter + dimension "$ / bulan" | pop×3 | "server", "jalannya", "tagihan" |
| L07 | `Sekarang aku yang *mutusin*.` | two columns: `2020` rack (LEDs) "jagain server" → `sekarang` dashed server + ✓ / ✕, ✓ lights | pop, click | "dulu", "sekarang", "perlu" |
| L08 | `Tiga *angka*.` | three dashed slots appear | pop×3 | "tiga" |
| L09 | (same) | `4` outline → fill; tags AWS · Azure · Google Cloud · Alibaba Cloud | pop×4 | "empat" |
| L10 | (same) | `10.000` outline → fill; "request barengan" + ✓ "tetap jalan" | thud, chime | "sepuluh", "jalan" |
| L11 | (same) | `$14.000` outline → fill; "biaya cloud turun" | thud | "empat" |
| L12 | (same) | "per bulan." serif slam, camera punch-out | thud | "bulan" |
| L13 | `Aku *bongkar* sistemnya.` | tight on the house → pull out → city map; pin "kamu di sini" | whoosh | "bongkar" |
| L14 | (same) | blocks `bank down · gajian` and `war tiket` light up | pop×2 | "gajian", "crash" |
| L15 | `Plus karier *cloud*.` | block `karier cloud` lights | pop | "beneran" |
| L16 | `Bukan yang paling *canggih*.` | dark blueprint plan draws on, one room missing (dashed slot) | whoosh_dark | "canggih" |
| L17 | `Tapi yang paling *pas*.` | missing room slides in, clicks, fills teal | click, chime | "pas" |
| L18 | — | logo + next-video card | pop | "berikutnya" |
| L19 | — | `+ Follow` click | click, chime | "follow" |
