# TREATMENT — Gimana aku hemat $14.000/bulan biaya cloud

> One row per script line. headline = punchline (not narration). anchor = spoken word the main event lands on.
> ≤ 3 cards on screen · one accent per headline · numbers in Indonesian format (`$14.000`, `10%`).
> Cover frame (`v.cover_t`): end of L02 — `$14.000` + "tiap bulan" fully on screen.

> **v2.1 — tech terms English (GLOSSARY.md):** chapters `01 · RIGHT-SIZING`, `02 · RESERVED & SPOT`; tags idle /
> unattached / stale; CPU USAGE / BILLED; receipt On-demand / Reserved instance / Spot instance; monolith · 24/7;
> pay-per-use. Headlines `*Right-size* dulu.`, `Jangan semua *on-demand*.` (older rows below still show v1 wording).

## v2 composition (STYLE §6b) — replaces the v1 "headline + card" layout everywhere

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | rolling odometer `$14.000` (210px, no card) + stamp `≈ Rp 200+ juta` → leaking chart → 2×2 lever tiles | centered hero → full-width chart → tile grid | cut-in 1.22 → pull-out; slow push on chart | number drops down, chart whips left, tiles whip in |
| 00 BOCOR | big terminal; flagged rows pop out as tilted leak cards → 24h clock ring | card + stacked cards → centered ring | push to flagged rows; push to clock | whip left → ring whips in from right |
| 01 UKURAN | typographic battle `10%` vs `100%` (300px) → bus, cursor drag-resizes it (live size label) + hand note | pure typography → object + note | push on 10%, **punch-out on "seratus"**, push on bus | battle drifts up, bus rises |
| 02 LANGGANAN | receipt printing line by line, eceran struck, **HEMAT stamp** + 2 hand notes | tilted paper + notes | camera follows the paper down, snaps back on stamp | receipt whips out right |
| 03 ARSITEKTUR | monolith shatters (pieces tumble), 3 fly into serverless zone and glow when used | centered object | push on monolith, punch-out on split | pop in, drop out |
| RECAP | full-width staircase chart, ball rolls down a step per lever → **bookend odometer** `$14.000` | full-width chart → centered hero | follows the ball → cut-in 1.2 → pull-out | chart drops, number pops |

## New components (engine/components/charts.py)

| Component | Used in | Description |
|---|---|---|
| `bill_counter` | INTRO, RECAP | big `$` number counting up/down in a card, with a "/ bulan" label and mono caption |
| `cost_chart` | INTRO, RECAP | line chart (12 months) that drops in steps, one step per lever, labels on each drop |
| `usage_meter` | 01 | horizontal bar: "terpakai 10%" vs "dibayar 100%" |
| `seat_grid` | 01 | 4×10 grid of bus seats (rounded squares), one filled blue |
| `price_bars` | 02 | 3 horizontal bars: Eceran / Langganan / Spot, each shrinking to its relative price |
| `day_timeline` | 00, 03 | 24-hour strip: always-on vs active only during working hours / only during spikes |
| `block_split` | 03 | one big "monolith" block splits into small service blocks, some fade to "serverless" |

Relative prices in `price_bars` and the shape of `cost_chart` are **illustrative** (no per-lever breakdown
given); on screen they carry no rupiah/dollar figures except the confirmed $14.000 total.

## INTRO (light, intro tint)

| id | headline | visual | motion | SFX | anchor |
|---|---|---|---|---|---|
| L01 | — | `bill_counter` card, centered on the column: counts `$0 → $14.000` | number counts up 1.2 s, card blur-rises | tick (during count), thud at end | "dolar" |
| L02 | `Tiap *bulan*.` | counter stays; headline lands above it; mono caption "HEMAT BIAYA CLOUD · PER BULAN" | words blur-rise | whoosh soft | "bulan" |
| L03 | (same) | second line under counter: `≈ Rp 200+ juta` counts up | count 0.8 s | tick | "dua ratus" |
| L04 | `Bukan mahal. *Bocor*.` | counter exits; `cost_chart` flat-high line, a "leak" drip of red dots dripping from the line | line draws left→right, drips loop 2× | pop on "bocor" | "bocor" |
| L05 | (same) | 4 numbered chips appear in a row: `Bocor · Ukuran · Langganan · Arsitektur`; tag "Alibaba Cloud" | chips pop stagger 0.1 s | pop×4 | "empat" |

## 00 · BOCOR (green)

| id | headline | visual | motion | SFX | anchor |
|---|---|---|---|---|---|
| L06 | `Cari yang *bocor*.` | terminal card `aliyun ecs` listing resources, typing | terminal types command | key ticks | "bocor" |
| L07 | (same) | row 1 highlights: `ecs-web-old · CPU 0% · RUNNING` + red tag "nganggur" | dim others, outline row | tick | "nggak ada" |
| L08 | (same) | row 2: `disk-7f3a · 500 GB · UNATTACHED` + tag "yatim" | same | tick | "disk" |
| L09 | (same) | row 3: `snap-2023-… · ×148` + tag "numpuk" | same | tick | "snapshot" |
| L10 | (same) | terminal exits; `day_timeline` 00–24 h fully "ON", clock chip `02:00` with a moon, blinking | strip fills, clock pops | pop | "dua pagi" |
| L11 | (same) | timeline animates: night hours switch OFF (grey), only 08–18 stay blue; green ✓ "otomatis" | segments flip right→left | chime | "beres" |

## 01 · UKURAN (orange)

| id | headline | visual | motion | SFX | anchor |
|---|---|---|---|---|---|
| L12 | `Ukuran yang *pas*.` | `usage_meter` card, empty | card rises | pop | "pas" |
| L13 | (same) | bar fills to **10%** "terpakai" | fill eases 0.6 s, count 0→10% | tick | "sepuluh" |
| L14 | (same) | second bar fills to **100%** "dibayar" in coral | fill, count to 100% | thud | "seratus" |
| L15 | (same) | meter shrinks up; `seat_grid` bus (40 seats), one seat fills blue | seats pop in wave, one fills | pop | "satu orang" |
| L16 | (same) | grid compresses to 4 seats ("ukuran pas"), mono caption "pantau 2–4 minggu → turunin" | grid morph, caption fades | whoosh soft | "turunin" |

## 02 · LANGGANAN (purple)

| id | headline | visual | motion | SFX | anchor |
|---|---|---|---|---|---|
| L17 | `Jangan bayar *eceran*.` | `price_bars`: only "Eceran" bar, full width | bar draws | pop | "eceran" |
| L18 | (same) | "Langganan tahunan" bar appears, shorter; tag "yang nyala terus" | bar grows to its length | pop | "langganan" |
| L19 | (same) | "Spot instance" bar, shortest; tag "boleh mati sewaktu-waktu" | bar grows | pop | "spot" |
| L20 | (same) | all three bars side by side; same server icon on each row; bracket "beda jauh" | bracket draws | chime | "beda jauh" |

## 03 · ARSITEKTUR (teal)

| id | headline | visual | motion | SFX | anchor |
|---|---|---|---|---|---|
| L21 | `Ubah *arsitekturnya*.` | `block_split`: one big block "aplikasi lama · 24 jam" | block rises | thud | "arsitekturnya" |
| L22 | (same) | block cracks and splits into 6 small blocks | split with spring | whoosh | "dipecah" |
| L23 | (same) | 3 rarely used blocks slide into a dashed zone labeled "serverless" | slide + dashed zone draws | pop×3 | "serverless" |
| L24 | (same) | `day_timeline` under it: serverless row only lights up in short spikes | spikes flash in sequence | tick×3 | "pas dipakai" |
| L25 | (same) | caption "paling lama · efek paling panjang" with a long arrow → | arrow draws | — | "panjang" |

## RECAP (dark)

| id | headline | visual | motion | SFX | anchor |
|---|---|---|---|---|---|
| L26 | `Empat langkah.` | left: rows `00 BOCOR … 03 ARSITEKTUR` (step_row) | rows stagger in | whoosh_dark | "empat" |
| L27 | (same) | each row activates as its name is spoken; `cost_chart` on the right steps DOWN once per lever | row lights + chart drop per lever | pop×4 | each lever name |
| L28 | `*$14.000* / bulan.` | chart done; `bill_counter` re-appears big: `$14.000` | count up | thud | "dolar" |
| L29 | `Hemat ≠ *lemot*.` | small uptime-style line stays flat & green under the counter, label "performa tetap" | line draws | chime | "lemot" |

## OUTRO (dark, centered)

| id | headline | visual | motion | SFX | anchor |
|---|---|---|---|---|---|
| L30 | — | ring logo draws, "Mumeyong", line "Biaya cloud-mu bocor di mana?" | logo 1 s, text fade | — | — |
| L31 | — | contact pill `mumeyong.dev · SITUS` pops, cursor hovers it | pill pop + cursor | pop | "dev" |
| L32 | — | `+ Follow` → click → `✓ Following`; tagline "Bongkar arsitektur cloud lainnya" | click | click, chime | "Follow" |

## Notes
- Terminal rows in 00 (`ecs-web-old`, `500 GB`, `×148`) are **illustrative examples** of common leaks,
  not data from a client — fine since the narration says "biasanya". Replace with real (anonymised) values if you have them.
- Chat input: **not used** in this video (it's not a Claude workflow video) → frees the bottom area; content
  column can extend to y ≈ 1450. Context chips are replaced by the 4-lever chip row from L05 (sticky, dimmed,
  current lever highlighted) — acts as a progress map through the chapters.
- Outro tagline changes to "Follow, buat bongkar arsitektur cloud lainnya." (matches the spoken line).
