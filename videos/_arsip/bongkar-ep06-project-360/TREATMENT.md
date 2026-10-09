# TREATMENT — Bongkar Arsitektur EP06: Project 360

> From IDENTITY.md: metaphor **scattered files at many counters → one stopmap on the CS desk** · signature move
> **sheets fly in from different counters and slip into one stopmap, it shuts "klik"** · signature color
> **purple `#7558F0`** · hook **cold open mid-action**. Tech terms English (GLOSSARY.md). No numbers, no real customer
> data (names censored with a marker bar). Source colors (chapter palette): tabungan teal · asuransi green ·
> kredit orange · sekuritas blue.
> Cover (`v.cover`): "Satu nasabah,\n*satu layar*." + stopmap with sheets flying in.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **meja CS** (desk, monitor, CS left, nasabah right): app windows open one by one on the monitor (tabungan · asuransi · kredit), nasabah's `…` bubble, CS asks `NIK-nya berapa, Pak?` twice → windows fly into a **stopmap** (signature move) → giant purple `satu layar.` → **purple bumper** | centered hero, no card → pure type → full-bleed | push on the monitor; push on the bubble; punch on "satu layar" | desk rises; type slams; bumper wipes up |
| 00 MASALAH | **4 loket** card (2×2: BANK · ASURANSI · MULTIFINANCE · SEKURITAS), the same censored customer in each → CS walks counter to counter, photocopies stack in a tray → copies turn red, one sheet drifts out of the card: `celah bocor` | full-width card | push per counter; tight on the leaking sheet | card rises |
| 01 KEPUTUSAN | **stopmap** (no card): open → 4 sheets fly in from 4 corners (one hangs crooked first) → shuts "klik" → threads join the 4 tabs `nyambung` → map opens to a `profile_360` mini (`real-time` pulse) → 3 thin purple rings wrap it + tilted stamp `SENSITIF` | centered hero | punch on the "klik"; push on the profile; pull-out on the rings | map pops; sheets fly; rings draw |
| 02 DIAGRAM | **lapis** (concentric): core `ECS` box with 2 nodes × Docker containers → node-1 goes `down`, traffic shifts to node-2 → ring 1 `WAF` (red requests bounce) → ring 2 `VPN` (only the `kantor` tunnel connects) → ring 3 `IDaaS` (`id_card` taps the reader → green) | concentric diagram | push on the core; pull-out ring by ring | core pops; rings draw outward |
| 03 HASIL | **profile_360** full-width card: avatar ring fills per source (4 colors) → chips tabungan · asuransi · kredit · sekuritas → `LIVE` pulse + `diperbarui · baru saja` → 3 check tags `WAF · VPN · IDaaS` | full-width card | push on the ring; reset; punch on "aman" | card whips in from right |
| RECAP (dark) | **meja CS again** (bookend): CS opens one map → bubble `NIK-nya berapa, Pak?` appears… and is struck before it's said → nasabah ✓ → map with rings that grow thicker as sheets are added | centered object | pull-out 1.15 → 1.0 | desk rises; strike draws |
| OUTRO | logo + **EP07 teaser** (Azure AI Infrastructure, episode terakhir) + follow | centered | — | — |

Bookend: the cold open's repeated question returns in RECAP — struck out before it's asked.

## New components (engine/components/berkas.py)

| Component | What it does |
|---|---|
| `lembar` | paper sheet (center + rotation): colored source stripe, mono title, grey lines, dog-ear; `red` 0..1 tints it leaked |
| `stopmap` | snelhecter folder: back cover, colored page edges, fastener, front cover that swings open (`open_` 0..1), tab with label + hand note |
| `meja_cs` | CS desk scene: desk, monitor (screen = callback), CS behind the desk (left), customer on a chair (right) |
| `profile_360` | profile card: avatar with a 4-segment ring (one per source, each 0..1), censored name bar, product chips, LIVE dot |
| `lapis` | concentric security rings around a core box: each ring `p` 0..1 draws on, label pill on its top edge |
| `id_card` | employee ID card on a lanyard; `tap` 0..1 moves it to a reader, `ok` lights the reader green |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Buka aplikasi *satu-satu*.` | desk rises; app window 1 opens | whoosh, pop | "satu" |
| L02 | `Datanya *di mana-mana*.` | windows `tabungan` · `asuransi` · `kredit` stack on the monitor | pop×3 | "tabungan", "asuransi", "kredit" |
| L03 | `Ditanya *ulang*.` | nasabah `…` bubble; CS bubble `NIK-nya berapa, Pak?` ×2 | pop×2 | "sama" |
| L04 | — | windows fly into a stopmap (klik) → giant purple `satu layar.` | whoosh, thud | "layar" |
| (gap) | — | **purple bumper** `BONGKAR ARSITEKTUR · EP 06` | whoosh | chapter start |
| L05 | `Satu orang, *banyak* perusahaan.` | 2×2 counters pop, same censored customer in each | pop×4 | "banyak" |
| L06 | `Berkasnya *kesebar*.` | each counter gets its sheet stack (source colors) | tick×4 | "loket" |
| L07 | `Keliling, *fotokopi*.` | CS walks counter → counter, copies drop into a tray | whoosh, tick×4 | "fotokopi" |
| L08 | `Tiap fotokopi, *celah*.` | copies tint red, one drifts out; tag `celah bocor` | thud | "bocor" |
| L09 | `Kumpulin jadi *satu map*.` | stopmap opens; 4 sheets fly in, one hangs crooked, then klik | whoosh×4, thud | "map" |
| L10 | `Semua *nyambung*.` | threads join the 4 tabs | tick×3, chime | "nyambung" |
| L11 | `Ditarik *real-time*.` | map opens → mini profile, LIVE pulse | pop | "real-time" |
| L12 | `Penjagaan *berlapis*.` | 3 rings wrap the map; stamp `SENSITIF` | whoosh, thud | "berlapis" |
| L13 | `Docker di atas *ECS*.` | core box: node-1, node-2, each with Docker containers | pop×2 | "Docker", "ECS" |
| L14 | `Satu down, *yang lain jalan*.` | node-1 red `down`; dots shift to node-2 | thud, pop | "down", "ngelayanin" |
| L15 | `Lapis 1: *WAF*.` | outer ring draws; red requests bounce off | whoosh, tick×2 | "WAF" |
| L16 | `Lapis 2: *VPN*.` | middle ring; `kantor` tunnel connects, outsider can't | whoosh, pop | "VPN" |
| L17 | `Lapis 3: *IDaaS*.` | inner ring; id_card taps reader → green | whoosh, chime | "IDaaS" |
| L18 | `Satu nasabah, *satu layar*.` | profile_360 card whips in; ring fills per source | whoosh, pop×4 | "layar" |
| L19 | `Ditarik *real-time*.` | LIVE pulse, `diperbarui · baru saja`; sheet "fotokopi" struck | tick, pop | "real-time" |
| L20 | `Tetap *aman*.` | tags `WAF` · `VPN` · `IDaaS` with ✓ | pop×3, chime | "aman" |
| L21 | `Bukan soal *sebanyak-banyaknya*.` | dark: same CS desk, one map | whoosh_dark | "sebanyak" |
| L22 | `Nggak cerita *dua kali*.` | bubble `NIK-nya berapa, Pak?` appears and is struck; nasabah ✓ | tick, chime | "dua" |
| L23 | `Makin lengkap, makin *tebal*.` | map gains sheets, rings around it thicken | pop×3 | "tebal" |
| L24 | — | logo + EP07 teaser | pop | "AI" |
| L25 | — | `+ Follow` click | click, chime | "follow" |
