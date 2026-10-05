# TREATMENT — Bongkar Arsitektur EP01: Kubernetes yang nahan 10.000 request barengan

> Built from IDENTITY.md: metaphor **toll gates at mudik** · signature move **booth splits in two / closes** ·
> signature color **purple `#7558F0`** (pods, booths, capacity) · accent blue stays for words/UI · red = failure.
> Cover (`v.cover_t`): L02 end — flood of dots + "10.000+" on screen.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **particle flood** → traffic spike graph with "10.000+" pinned at the peak → crash (red `503` pill, line flatlines) → **purple full-bleed bumper** | full-bleed particles (no card) → centered graph → full-bleed color panel | dolly through the flood; punch on 503 | particles converge; graph drops down; bumper wipes up |
| 00 MASALAH | **toll plaza top-down**: 3 booths, cars queue, some U-turn (red), "gagal" tags pop | full-width top-down object | push into the queue | whip in from right |
| 01 KEPUTUSAN | 12 idle booths under a moon (struck) → **stacked slabs** `container → Kubernetes → Alibaba Cloud` drop onto each other + purple "petugas" badge | object grid → tilted 3D-ish stack | push on idle booths; pull out as the stack lands | grid drops, slabs drop in with overshoot |
| 02 DIAGRAM | **arch_diagram** (series signature): users → load balancer → pods inside nodes, packets flowing; pods **split**; a node slides in; a pod dies and is replaced | full-width vertical diagram | follows the action: LB → pods → new node → dead pod | diagram builds node by node |
| 03 HASIL | **load_graph 24h**: traffic curve + purple capacity band hugging it; at 02:00 the band shrinks; mini toll strip below closes booths one by one | graph + strip | slow track left→right along the day | graph draws in; strip pops |
| RECAP (dark) | fixed 12 booths (struck) vs **breathing booths** (open/close loop) → opinion slam `Bukan *gaya-gayaan*.` → `Emang butuh.` (giga) | split comparison → pure typography | push between the two; punch on "butuh" | split slides apart; type slams |
| OUTRO | logo + **EP02 teaser card** + follow | centered | — | — |

## New components (engine/components/infra.py)

| Component | What it does |
|---|---|
| `particle_flow` | deterministic stream of request dots from a spawn area toward a target (density, speed, jam) |
| `toll_plaza` | top-down road: lanes, booths (each with open-progress → split animation), queued + flowing cars, U-turning cars |
| `arch_diagram` | nodes (users / lb / pod / node box) + edges + packets flowing along edges; per-node alpha/scale/state |
| `load_graph` | 24h traffic line + capacity step band + time cursor |
| `stack_layers` | thick 3D-ish slabs that drop and stack (label + sub-label) |

## Lines

| id | headline | visual | motion | SFX | anchor |
|---|---|---|---|---|---|
| L01 | — | dark-ish particle field, dots start streaming toward one point at center | particles accelerate, camera dolly in | whoosh low | "sibuk" |
| L02 | `*10.000+* barengan.` | flood thickens; traffic line spikes, label `10.000+` pinned at peak | spike draws, label pops | thud | "sepuluh" |
| L03 | (same) | tag "layanan keuangan" under graph | tag pop | pop | "keuangan" |
| L04 | `Lemot. Lalu *down*.` | particles jam (slow, turn red); red pill `503` slams; line flatlines | slam + camera punch | thud, glitch-free | "down" |
| (gap) | — | **bumper**: purple panel wipes up, `BONGKAR ARSITEKTUR` + `EP 01` + "Layanan keuangan · Kubernetes" | wipe 0.4 s, text blur-in, wipe out | whoosh | chapter start |
| L05 | `Bayangin *gerbang tol*.` | toll plaza top-down, 3 booths, cars flowing | plaza whips in | whoosh | "tol" |
| L06 | (same) | car flow increases; queue grows behind booths | queue stacks up | tick× | "segitu" |
| L07 | (same) | 3 cars U-turn (red arc) | arcs draw | pop×3 | "putar" |
| L08 | `Transaksi *gagal*.` | red "FAILED" tags pop over U-turners; count chip `gagal ×3…` | pop | pop, thud | "gagal" |
| L09 | `~Gardu sebanyak-banyaknya~.` | 12 booths in a grid, all open | grid pops in | pop | "sebanyak" |
| L10 | (same) | night: moon, booths go dim/idle; tag "mahal · nganggur" | dim sweep | — | "nganggur" |
| L11 | `Gardu yang *nambah sendiri*.` | grid drops; one booth splits into two (signature move preview) | split | pop | "sendiri" |
| L12 | (same) | slabs drop: `container` → `Kubernetes` → `Alibaba Cloud` | drop + overshoot, stagger on each word | thud×3 | "container", "kubernetes", "alibaba" |
| L13 | (same) | purple badge "petugas tol" on the Kubernetes slab + hand note | badge pop, note writes | pop | "petugas" |
| L14 | `Dibagi *rata*.` | diagram: users → LB → 2 pods (in node box); packets split evenly | build + packets | pop | "load" |
| L15 | `Traffic naik? *Scale up*.` | queue meter rises; pods split 2 → 4 | split ×2 | pop×2 | "dibuka" |
| L16 | (same) | node box full → second node box slides in; pods split into it | slide | whoosh | "ditambah" |
| L17 | `Pod crash? *Diganti*.` | one pod turns red ✕, fades; new pod pops; packets reroute | ✕ + pop | thud, pop | "diganti" |
| L18 | `Peak hour, *aman*.` | load_graph: traffic curve over 24h, capacity band follows | draw left→right | whoosh | "tanpa" |
| L19 | (same) | peak label `10.000+ · aman ✓` | pop + check | chime | "aman" |
| L20 | (same) | cursor reaches 02:00: band shrinks; toll strip below closes booths one by one | close one by one | tick× | "nutup" |
| L21 | `Bayar pas *rame*.` | band hugging the curve highlighted; note "bayar cuma segini" pointing at band | note writes | pop | "rame" |
| L22 | `Jangan sizing buat *peak*.` | left: 12 fixed booths struck; right: breathing booths | split in, strike | pop | "rame" |
| L23 | (same) | right side loops open/close (signature move) | loop | tick× | "nutup" |
| L24 | `Bukan *gaya-gayaan*.` → `Emang butuh.` | opinion slam, giga type on "butuh" | slam + punch | thud | "butuh" |
| L25 | — | logo + EP02 teaser card: "EP 02 · Big data pindah ke cloud — 0 byte hilang" | card rises | pop | "hilang" |
| L26 | — | `+ Follow` click → `✓ Following` | click | click, chime | "Follow" |

## Notes
- Tech terms stay English (GLOSSARY.md): users, node, pod, load balancer, auto-scaling, idle, peak hour, down, crash, FAILED.
- No pod/node counts anywhere (no real numbers) — booths/pods are shown without numbers.
- No chat input (not a Claude workflow video); no lever chips — the series bumper + chapter HUD carry navigation.
- HUD series label: `BONGKAR ARSITEKTUR · EP 01`.
