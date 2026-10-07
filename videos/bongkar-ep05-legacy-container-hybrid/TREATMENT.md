# TREATMENT — Bongkar Arsitektur EP05: Legacy dan container, hidup berdampingan

> From IDENTITY.md: metaphor **lahan kuliner — ruko lama + kios kontainer, one front gate** · signature move
> **split-flap direction board flips, the visitor stream turns with it** · signature color **green `#10A060`** ·
> hook **specific question**. Tech terms English (GLOSSARY.md). No numbers.
> Cover (`v.cover`): "Lama & baru,\n*satu pintu*." + ruko + kios + flip board.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **ruko + kios side by side** (`legacy` / `Kubernetes` tags), a visitor walks in with a `?` → tags `belum bisa dimatiin` / `udah jalan` → giant green `berdampingan.` → **green bumper** | two objects, no card → pure type → full-bleed | pull-out 1.08 → 1.0; push on the visitor's `?`; punch on "berdampingan" | objects whip in from both sides; type rises; bumper wipes up |
| 00 MASALAH | **lahan kuliner** card: ruko left, kios right (one more drops in, one slides), three doors `A B C` on top → visitors pile into door A (red), B/C empty, ruko awning flickers red, `kebanjiran` · `lemot · error` | full-width card | push on ruko, then kios; tight on door A | card rises |
| 01 KEPUTUSAN | **one gapura** (satpam booth, two lane lamps) → visitors split alternately left/right (`SLB · load balancer`) → **flip_sign** drops in (`Nginx`) → rows flip `menu lama → RUKO`, `menu baru → KONTAINER`, visitors follow (signature move) → `satu pintu` | centered hero, vertical flow, no card | push on the gate; push on the board; pull-out 0.95 on "satu pintu" | gate pops; board drops in |
| 02 DIAGRAM | series **arch** stack: `users` → `SLB` → `nginx-1..3` → `legacy · monolith` box (ruko) + `Kubernetes` box (3 kios) with colored request dots → red request stopped at nginx (`access rule · ditolak`) → **flip_sign** row `/promo → LEGACY` flips to `KUBERNETES`, dots re-route | stacked diagram | focus SLB → nginx row → pull back → push on the board | nodes pop row by row; board rises |
| 03 HASIL | **door queues card**: 3 queue bars uneven (one red) → equal (green), `rata.` → a jittery red line goes calm green, `stabil.` stamp → **gapura** whips in with padlock tag `semua lewat sini` | full-width card → centered object | punch on "rata"; push on the line; reset | card rises; gate whips in from right |
| RECAP (dark) | ruko + kios under a big **flip_sign**: rows flip one at a time, not all (`nggak sekaligus`) → pull-out reveals one gapura framing everything → a visitor walks; the board flips mid-stride; she turns without stopping → ✓ `pesanannya sampai` | centered object | pull-out 1.15 → 1.0 across "pintunya satu" | board flips; gate draws on |
| OUTRO | logo + **EP06 teaser** (Customer 360, milidetik) + follow | centered | — | — |

Bookend: the hook's "tanpa user sadar" returns in RECAP — the board changes under the visitor's feet and she never notices.

## New components (engine/components/kuliner.py)

| Component | What it does |
|---|---|
| `ruko` | 2-storey shophouse: upper windows, signboard (serif, slight tilt), striped awning, rolling door (open 0..1), `hot` 0..1 flickers red (overloaded) |
| `kios` | container stall: corrugated ribs, serving hatch with awning flap, label; signature green |
| `flip_sign` | split-flap board: rows `label → destination`; destination chars flip one by one from `prev` to new at `t_flip` (flap squash); optional `stuck` char hangs half-flipped |
| `gapura` | the single front gate: two pillars, beam with label, satpam booth, two lane lamps (left/right) |
| `visitor` | tiny walking person (head + body), step bob, any color |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Lama & baru, *barengan*?` | ruko (left) + kios (right), tags `legacy` · `Kubernetes` | whoosh×2, pop×2 | "barengan" |
| L02 | `Tanpa user *sadar*.` | visitor walks in, `?` bubble, dashed arrows to both | pop | "mana" |
| L03 | `Yang baru udah *jalan*.` | tags `belum bisa dimatiin` (red) · `udah jalan` (green) | pop×2 | "dimatiin", "jalan" |
| L04 | — | `legacy + container` → giant green `berdampingan.` | whoosh, thud | "berdampingan" |
| (gap) | — | **green bumper** `BONGKAR ARSITEKTUR · EP 05` | whoosh | chapter start |
| L05 | `Satu *lahan kuliner*.` | card rises: empty lot, ground line | whoosh | "kuliner" |
| L06 | `Kiri: *ruko lama*.` | ruko pops; note "ini legacy-nya" | pop | "ruko" |
| L07 | `Kanan: *kios kontainer*.` | two kios pop; third drops in at "ditambah"; one slides at "dipindah" | pop×3, whoosh | "ditambah", "dipindah" |
| L08 | `Pintunya *beda-beda*.` | doors A/B/C appear on top | pop×3 | "beda" |
| L09 | `Satu *kebanjiran*.` | visitors pile into A (red), B/C empty; ruko flickers; `lemot · error` | tick×6, thud | "kebanjiran", "goyang" |
| L10 | `*Satu* pintu depan.` | gapura pops center | pop, thud | "satu" |
| L11 | `Satpam = *load balancer*.` | visitors split alternately left/right; lane lamps blink; tag `SLB` | tick×n, pop | "load" |
| L12 | `Papan arah = *Nginx*.` | flip_sign drops in under the gate | whoosh, pop | "Nginx" |
| L13 | `Lama ke ruko, baru ke *kontainer*.` | rows flip (one char sticks); grey visitors → ruko, green → kios | tick×chars, pop | "ruko", "kontainer" |
| L14 | `Kelihatannya *satu pintu*.` | pull-out; tag `user cuma lihat ini` on the gate | whoosh | "satu" |
| L15 | `Masuk lewat *SLB*.` | users → SLB | pop×2 | "SLB" |
| L16 | `Dibagi ke *Nginx*.` | nginx-1..3 pop; dots round-robin | pop×3 | "Nginx" |
| L17 | `Path lama, path *baru*.` | legacy box (ruko) + Kubernetes box (3 kios); grey dots left, green dots right | pop×2 | "legacy", "Kubernetes" |
| L18 | `Satpam *kedua*.` | red request stopped at nginx-2, ✗ + tag `access rule · ditolak` | thud | "mana" |
| L19 | `Ganti *papannya*.` | board row `/promo → LEGACY` flips to `KUBERNETES`; dots re-route | tick×chars, chime | "papannya" |
| L20 | `Kebagi *rata*.` | queue bars uneven → equal | whoosh, chime | "rata" |
| L21 | `Lebih *stabil*.` | red jitter line calms to green, stamp `STABIL` | thud | "stabil" |
| L22 | `Akses lebih *rapi*.` | gapura whips in, padlock tag `semua lewat sini` | whoosh, pop | "rapi" |
| L23 | `Nggak harus *sekaligus*.` | dark: ruko + kios under a 3-row board; row 1 flips, rows 2–3 stay | whoosh_dark, tick | "sekaligus" |
| L24 | `Pintunya *satu*.` | pull-out: one gapura frames everything | whoosh | "satu" |
| L25 | `Pesanannya *sampai*.` | visitor walks; board flips mid-stride; she turns, no stop; ✓ | tick, chime | "sampai" |
| L26 | — | logo + EP06 teaser card | pop | "milidetik" |
| L27 | — | `+ Follow` click | click, chime | "follow" |
