# TREATMENT — Bongkar Arsitektur EP03: Ganti stack big data jadi serverless

> From IDENTITY.md: metaphor **own kitchen vs cloud kitchen** · signature move **burner ignites when a ticket lands,
> dies to nothing when the job is done** · signature color **orange `#E8861A`** · hook **before/after split**.
> Tech terms English (GLOSSARY.md). No numbers (node count, % faster) — none given.
> Cover (`v.cover_t`): L04 — giant orange `serverless.` on screen.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **before/after split**: left `DULU` = server_rack with blinking LEDs + chores (patch · restart · monitoring); right `SEKARANG` = empty dashed rack, "kosong." → owner tags (kamu / cloud) → giant orange `serverless.` → **orange bumper** | two columns → pure type → full-bleed | pull-out 1.08 → 1.0 on L01, push on the empty side at "sama sekali" | left whips in, right whips in, type rises, bumper wipes up |
| 00 MASALAH | **own kitchen** card: ticket rail (empty) + 3 burners burning nonstop, gas gauge draining → burners relabel `node-1..3`, red `idle · tetap dibayar` → tickets flood the rail, flames turn red, `+ node baru` progress bar crawls | full-width card | push into the burners; tight on the flooded rail | card rises |
| 01 KEPUTUSAN | **cloud kitchen** (no card): old burners whip out → 3 cold burners; tickets drop from the rail into a burner → *fwoosh* → done → flame dies (signature move) → owner tags `kamu: job / query` · `cloud: mesinnya` → 3 grey racks + tilted **PENSIUN** stamp | centered hero, no card | punch on the first ignition; punch-out on the stamp | old kitchen whips left, racks pop |
| 02 DIAGRAM | series **arch** stack: sources → `Flink` (burner, streaming dots) + `MaxCompute` (oven, batch crates) → **lake_pantry** `Paimon · data lake` (both read & write) → **dag_flow** `Airflow` band, tasks light in order | stacked diagram + band | focus Flink → MaxCompute → pull out to pantry → push on the DAG | nodes pop row by row |
| 03 HASIL | `lebih *cepat*.` typographic punch with speed lines → chore list struck through (patch · restart · jaga tengah malam) + moon → DAG band running by itself | pure type → list card → band | punch-out on "cepat"; push on the list | type slams; list whips in; band whips in from right |
| RECAP (dark) | **cloud kitchen at night** → *surprise*: the back wall slides up → giant server racks behind it, "dikelola cloud provider" → racks dim, an orange data glow: `datanya.` | centered object | pull-out 1.15 → 1.0 across the reveal | wall lifts; racks dim |
| OUTRO | logo + **EP04 teaser** (monolith → event-driven) + follow | centered | — | — |

Bookend: hook's right panel ("kosong.") comes back in RECAP — the "empty" side opens to show the servers behind it.

## New components (engine/components/kitchen.py)

| Component | What it does |
|---|---|
| `flame` | flickering 3-tongue flame (deterministic in t), size 0..1, `hot` tints toward red |
| `burner` | stove (side view): body + knob that turns with the fire + burner head + flame; optional label |
| `oven` | oven box whose window glows with `heat` (batch) |
| `order_ticket` / `ticket_rail` | paper ticket (mono title + serif "handwritten" lines, zigzag bottom, done ✓); rail holds tickets that drop in, tilt, fall |
| `dag_flow` | Airflow DAG band: task boxes + arrows; waiting → running (orange bar) → done (green ✓) |
| `lake_pantry` | Paimon data-lake card: animated water + table jars (orders, events, customers) |
| `server_rack` | rack of 1U units with seeded blinking LEDs; `on=0` = retired grey |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Dulu: *dijagain* tiap hari.` | left DULU panel: rack, LEDs blink; chores pop (patch · restart · monitoring) | whoosh, pop×3 | "dijagain" |
| L02 | `Sekarang: *nggak ada* yang diurus.` | right SEKARANG panel: dashed empty rack, "kosong." | whoosh, thud | "sama" |
| L03 | `Yang beda: *siapa yang ngurus*.` | both panels get `data · job` tags (same); then `kamu yang ngurus` (red) / `cloud yang ngurus` (green) | pop×2 | "siapa" |
| L04 | — | `stack big data legacy` → giant orange `serverless.` | whoosh, thud | "serverless" |
| (gap) | — | **orange bumper** `BONGKAR ARSITEKTUR · EP 03` | whoosh | chapter start |
| L05 | `Bayangin *dapur sendiri*.` | kitchen card rises, 3 burners ignite one by one | whoosh, pop×3 | "dapur" |
| L06 | (same) | rail shows "nggak ada pesanan"; tags `servis kompor`, `beli gas`; gas gauge drains | tick×2 | "dirawat", "gasnya" |
| L07 | `Itu node *legacy*.` | burner labels → `node-1..3`; red tag `idle · tetap dibayar`; note "ini node legacy" | pop, thud | "idle" |
| L08 | `Pesanan *membludak*?` | 7 tickets flood the rail (one hangs crooked), flames turn red; `+ node baru` bar crawls | tick×7, thud | "membludak", "nambah" |
| L09 | `*Lepas* dapurnya.` | old burners whip out left | whoosh | "lepas" |
| L10 | (same) | cloud kitchen: 3 cold burners; tickets drop in → fwoosh → done → flame dies | pop, whoosh×2 | "nyala", "mati" |
| L11 | `Kamu urus *resepnya*.` | one more ticket cycle; tags `kamu: job / query` · `cloud: mesinnya` | pop×2 | "resepnya", "mesinnya" |
| L12 | `Node legacy-nya *pensiun*.` | 3 grey racks, LEDs off, stamp **PENSIUN** (tilted) | pop, thud | "pensiun" |
| L13 | `Streaming → *Flink*.` | `events` source + Flink node (burner lit), fast dots | pop, tick | "streaming" |
| L14 | `Batch → *MaxCompute*.` | `data harian` source + MaxCompute node (oven glows), crates | pop, whoosh | "batch" |
| L15 | `Satu pantry: *Paimon*.` | lake_pantry under both; dots down (write) and up (read) | whoosh | "Paimon" |
| L16 | `Urutannya: *Airflow*.` | dag_flow band: ingest → flink → maxcompute → report, lit in order | tick×4, chime | "Airflow" |
| L17 | `Hasilnya:` | `data processing` → giant `lebih cepat.` with speed lines | thud | "cepat" |
| L18 | `Nggak ada yang *dijagain*.` | card: patch / restart / jaga tengah malam, each struck; moon | tick×3 | "di-patch", "di-restart", "dijagain" |
| L19 | `Pipeline jalan *sendiri*.` | dag_flow loops by itself; `data masuk` → `siap dipakai` | tick×4, chime | "sendiri" |
| L20 | `Bukan soal *nggak ada server*.` | dark: cloud kitchen at night (wall + 3 burners) | whoosh_dark | "server" |
| L21 | `Server-nya *tetap ada*.` → `*Bukan kamu* yang ngurus.` | wall lifts → server racks behind; tag `dikelola cloud provider` | whoosh, pop | "tetap", "bukan" |
| L22 | `Balik ke *datanya*.` | racks dim; orange data glow + serif "datanya." | chime | "datanya" |
| L23 | — | logo + EP04 teaser card | pop | "monolith" |
| L24 | — | `+ Follow` click | click, chime | "follow" |
