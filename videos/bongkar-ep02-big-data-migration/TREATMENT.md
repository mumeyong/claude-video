# TREATMENT — Bongkar Arsitektur EP02: Pindahin big data ke cloud, tanpa satu byte hilang

> From IDENTITY.md: metaphor **library that's still open** · signature move **old/new pairs lock together (hash
> match → green click)** · signature color **green `#10A060`** · hook **myth struck out**.
> Tech terms English (GLOSSARY.md). No numbers (data size, duration) — none given.
> Cover (`v.cover_t`): L04 end — "zero data loss" punch on screen.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | two big **keycaps `Ctrl C` / `Ctrl V`** pressing → struck headline → **bookshelf, one book falls out** (red "1 record hilang") → `zero data loss` typographic punch → **green bumper** | centered object → shelf → pure type → full-bleed | punch on the falling book | keycaps drop away, shelf whips left, bumper wipes up |
| 00 MASALAH | **bookshelf** (library still open): books slide out & back (borrow/return), spines change color (UPDATE) → a frozen grey **copy** appears beside it, red diff marks where it fell behind | full-width shelf → split original/copy | push into the shelf; pull out on the split | shelf rises; copy slides in from right |
| 01 KEPUTUSAN | **sync_pipe**: `legacy` card top → `Alibaba Cloud` card bottom, lane 1 big crates (full copy), lane 2 steady dot stream (incremental sync); legacy keeps an **OPEN** badge | vertical two-node pipe | follows crates down, then holds wide | cards pop, crates flow |
| 02 DIAGRAM | series **arch_diagram** band (legacy → sync → Alibaba Cloud) + **twin_table**: legacy vs cloud rows slide together and **lock green** one by one; one row is off by **one character** → red → re-sync → green | band + two-column table | push on each locking row; tight on the bad character | rows slide in from the right |
| 03 HASIL | **cutover_switch**: app on top, track to legacy and to cloud, lever flips → traffic moves to cloud; old track turns dashed = **rollback plan** → `zero data loss.` punch | object → pure type | punch on the lever flip | switch pops in; type slams |
| RECAP (dark) | **gate with a padlock**: `row count ✓` + `checksum ✓` → lock opens → "boleh pindah"; opinion headline | centered object | push on the lock | checks pop, lock opens |
| OUTRO | logo + **EP03 teaser** + follow | centered | — | — |

## New components (engine/components/migrate.py)

| Component | What it does |
|---|---|
| `keycap` | 3D-ish keyboard key with a press animation |
| `bookshelf` | rows of book spines (seeded widths/colors); per-book pull-out, color change, falling book; `ghost` = frozen grey copy |
| `sync_pipe` | source + target cards, two lanes: crates (full copy) and a dot stream (incremental sync) |
| `twin_table` | legacy vs cloud rows: name · row count · checksum; slide-in, lock (green link + ✓), bad-char highlight + fix |
| `cutover_switch` | app → fork → legacy / cloud tracks, lever flip, packets on the active track, dashed rollback path |
| `padlock` | lock icon whose shackle opens |
| `series_bumper` | reusable "BONGKAR ARSITEKTUR · EP xx" full-bleed panel (episode color) |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `~Copy, paste, beres~?` | keycaps `Ctrl C` then `Ctrl V` press | click ×2 | "copy", "paste" |
| L02 | (strike) `Nggak segampang itu.` | strike draws; keycaps drop away | thud | "nggak" |
| L03 | `Satu record *hilang*.` | bookshelf; one book slides out and falls, red tag "1 record hilang" → "laporan salah" note | pop, thud | "hilang" |
| L04 | — | tags `legacy infra → Alibaba Cloud`; giant green `zero data loss` | whoosh, thud | "zero" |
| (gap) | — | **green bumper** `BONGKAR ARSITEKTUR · EP 02` | whoosh | chapter start |
| L05 | `Perpustakaan yang *masih buka*.` | bookshelf rises, OPEN sign | whoosh | "perpustakaan" |
| L06 | (same) | books slide out/in (borrow/return) | tick× | "pinjam" |
| L07 | `Datanya terus *berubah*.` | spines flash new colors + tiny UPDATE tags | tick× | "berubah" |
| L08 | (same) | grey frozen copy slides in beside it; red diff marks on changed books | pop×3 | "ketinggalan" |
| L09 | `*Dua* tahap.` | legacy + Alibaba Cloud cards pop, pipe draws | pop×2 | "dua" |
| L10 | (same) | lane 1: crates flow (full copy) | whoosh | "full" |
| L11 | (same) | lane 2: steady dots (incremental sync) | tick× | "incremental" |
| L12 | (same) | legacy badge "OPEN" stays green; note "tetap jalan" | pop | "buka" |
| L13 | `Disalin, lalu *dicek*.` | arch_diagram band builds | pop | "legacy" |
| L14 | (same) | packets ride the sync edge | tick | "sync" |
| L15 | (same) | twin_table rows slide in and lock green one by one | click per lock | "dicek", "checksum" |
| L16 | `Beda satu karakter? *Ketahuan*.` | last row: one char red, camera tight, re-sync → char flips → green lock | thud, chime | "karakter", "sync" |
| L17 | `Semua match → *cutover*.` | cutover_switch, lever flips, traffic to cloud | click, whoosh | "cutover" |
| L18 | (same) | old track dashed, label "rollback plan" | pop | "rollback" |
| L19 | — | giant `zero data loss.` + ✓ | thud, chime | "zero" |
| L20 | `Bukan soal *copy*.` | dark; padlock gate appears | whoosh_dark | "copy" |
| L21 | `Tapi soal *bukti*.` | `row count ✓` `checksum ✓` pop | pop×2 | "bukti" |
| L22 | `Belum terbukti? *Belum pindah*.` | padlock opens only after both checks | click, chime | "pindah" |
| L23 | — | logo + EP03 teaser card | pop | "serverless" |
| L24 | — | `+ Follow` click | click, chime | "follow" |
