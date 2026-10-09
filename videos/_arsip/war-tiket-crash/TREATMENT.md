# TREATMENT — Kenapa war tiket konser selalu crash?

> From IDENTITY.md: metaphor **mesin nomor antrean kantor pos** (server = loket) · signature move **karcis keluar dari
> slot** (+ the big clock's seconds jumping) · color **hijau `#10A060`** · hook **angka dulu** · structure
> **timeline per detik** (chapter label = timecode). HUD `MUMEYONG · DETIK PER DETIK`, no series bumper. QUICK.
> Numbers on the graph are an illustration (labelled "ilustrasi"). Cover (`v.cover_t`): L14, ticket 29.481 + display.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **seat grid** (ribuan kursi) → tap ripples (jari) → **big_clock** 09:59:59 → 10:00:00 · phone "Beli" tapped → white **503**, slip `ERROR 503` feeds out under the phone · clock + ruler `:00 · :01 · :10` | full card + big type → centered phone → centered clock | push on the phone at "error" | whip left, slip feeds |
| 00 · 10:00:00 | **traffic graph** (per second): flat line → ghost "naik pelan" curve → the line goes **vertical** | full-width card | punch-out on "tegak" | card rises |
| 01 · 10:00:01 | **4 loket** (servers): crowd rushes in → lamps red **PENUH** → each loket feeds out a `503` slip → giant **↻** → storm starts, traffic bar ×1 → ×2 | centered row, no card | push on the slips; punch on ↻ | slips feed, ↻ pops |
| 02 · 10:00:10 | **refresh_storm** swirling around the lokets (retry storm) → 4 more lokets pop in, the storm doubles too | centered object + storm | slow push → pull-out | lokets pop |
| 03 · ANTREAN | **dispenser** (queue machine) left: button pressed, ticket **29.481** feeds out · right: green lokets, orderly line through `rate limit`, the rest wait in a long line · display SEKARANG MELAYANI jumps fast → lamp **DIPANGGIL** | object + side scene + hand note | push on the slot, then on the display | machine rises |
| RECAP (dark) | giant **refresh button** crossed out → green lokets, orderly line, slip `giliranmu ✓` | centered | push on the slip | whip |
| OUTRO | logo + next video (roadmap cloud engineer) + follow | centered | — | — |

## New components (engine/components/tickets.py)

| Component | What it does |
|---|---|
| `big_clock` | mono HH:MM:SS; characters that changed drop in from above while the old ones fall out (second jump) |
| `print_slip` | paper slip feeding out of a slot (signature move): colored band, centered lines, zigzag tear, slight tilt |
| `dispenser` | queue-number machine: green top, LED display "SEKARANG MELAYANI" (digits jump), AMBIL button (press), called lamp, ticket slot |
| `loket` | service window = server: clerk behind glass, lamp green → red, "PENUH" plate, label, slip slot |
| `refresh_icon` / `refresh_storm` | ↻ glyph; many ↻ swirling on an ellipse, multiplying with `amount`, pulsing inward |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Semua di *satu detik*.` | seats fill · tap ripples · clock 09:59:59 → 10:00:00 | pop, tick, thud | "kursi", "jari", "detik" |
| L02 | `Yang keluar: *error*.` | phone ticket page, cursor taps **Beli** → white 503 → slip `ERROR 503` feeds out | click, thud | "pencet", "error" |
| L03 | `Detik per *detik*.` | big clock 10:00:00 + ruler ticks :00 · :01 · :10 light up | tick×3 | "detik" |
| L04 | `Semua klik *barengan*.` | graph: flat line drawn up to 10:00:00, tap ripples on the point | pop | "klik", "sama" |
| L05 | `Grafiknya *tegak lurus*.` | ghost curve "naik pelan" (dashed) → real line shoots vertical | whoosh, thud | "pelan", "tegak" |
| L06 | `Loketnya *penuh*.` | crowd rushes 4 lokets → PENUH → 503 slips feed out | pop×4 | "penuh", "error" |
| L07 | `Terus: *refresh*.` | giant ↻ | thud | "refresh" |
| L08 | `Traffic-nya *dobel*.` | storm of ↻ starts · bar ×1 → ×2 | tick×n | "refresh", "dobel" |
| L09 | `*Retry storm*.` | storm thickens, pulses inward on the lokets; tag `retry storm` | whoosh | "retry" |
| L10 | `Badainya ikut *gede*.` | 4 more lokets pop in · storm doubles · pull-out | pop×4 | "nambah", "gede" |
| L11 | `Virtual *waiting room*.` | dispenser rises; tag `virtual waiting room` | whoosh | "virtual" |
| L12 | `Ambil *karcis*.` | button pressed → ticket 29.481 feeds out | click, pop | "karcis" |
| L13 | `Masuk *segini* per detik.` | orderly dots pass the `rate limit` gate to green lokets; the rest wait in line | pop | "rate" |
| L14 | `Majunya *cepet*.` | display jumps fast → 29.481, lamp DIPANGGIL; note "itu kamu" | tick×n, chime | "jauh", "cepet" |
| L15 | `Musuhnya: tombol *refresh*.` | dark: giant refresh button, crossed out on "sendiri" | whoosh_dark, thud | "refresh", "sendiri" |
| L16 | `Lambat, tapi *nggak crash*.` | 4 green lokets, orderly line, slip `giliranmu ✓` | pop, chime | "lambat", "crash" |
| L17 | — | logo + next-video card (roadmap) | pop | "berikutnya" |
| L18 | — | `+ Follow` click | click, chime | "follow" |
