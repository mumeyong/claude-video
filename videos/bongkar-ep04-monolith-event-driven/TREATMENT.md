# TREATMENT — Bongkar Arsitektur EP04: Monolith lama, dipecah jadi event-driven

> From IDENTITY.md: metaphor **kampung + kentongan pos ronda** · signature move **kentongan struck → sound rings run
> down the gang → only the houses that listen light up, work, go dark again** · signature color **teal `#0E9AAB`** ·
> hook **contrarian claim** ("sebagian besar waktunya, dia tidur"). Tech terms English (GLOSSARY.md). No numbers.
> Cover (`v.cover`): "Aplikasinya\nkebanyakan *tidur*." + gang with one lit window + kentongan.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **gang at rest**: kentongan on its pole + 4 dark houses with `z z` → *tok* → rings → one window lights, works, goes dark → whip to **rumah gede** with every window lit `24 jam` → giant teal `event-driven.` → **teal bumper** | centered hero → centered hero → pure type → full-bleed | pull-out 1.10 → 1.0 on L01; push on the lit window; punch on "event-driven" | gang rises, big house whips in from right, type slams, bumper wipes up |
| 00 MASALAH | **rumah gede** card: 4 rooms (order · bayar · notifikasi · laporan) under one roof, one MCB → all lit, only `laporan` busy → `korslet` spark → MCB trips → whole house dark, red `down semua` → `TUTUP · RENOVASI` board + `deploy ulang: semuanya` | full-width card | push on the rooms; punch-in on the spark; reset on the board | card rises |
| 01 KEPUTUSAN | **gang** (no card): house splits into 4 small houses sliding apart (`order()` `bayar()` `notif()` `laporan()`) → call-wires between houses struck → kentongan pole slides in → *tok* → rings → bayar/notif/laporan light, work, dark again (signature move) · `order()` stays dark | centered hero, no card | punch on the split; push on the kentongan; pull back on the rings | house splits; kentongan whips in from left |
| 02 DIAGRAM | series **arch** stack: `API` → **kentongan node** `event: order.created` → 3 function houses → provider row `AWS Lambda` · `Alibaba Function Compute` → dashed teal fence `private network` (outside dot bounces off) → **portal** `NAT gateway` at the bottom (dot out ✓, dot in ✗) | stacked diagram | focus API → functions → pull out to fence → push on the portal | nodes pop row by row; fence draws on; portal rises |
| 03 HASIL | `compute overhead` → giant teal `turun drastis.` with a "lampu nyala" meter dropping from full (monolith) to a sliver → gang: `laporan()` sparks red, neighbours keep working (`tetap jalan`) → `deploy` tag lands on one house only | pure type → gang card | punch-out on "drastis"; push on the broken house | type slams; gang card whips in from right |
| RECAP (dark) | **gang at night**, a small figure at the kentongan: *tok* → he walks off right without turning, houses light up behind him (surprise, fire-and-forget) → small **rumah gede** returns, green ✓ `sehat → biarin` | centered object | pull-out 1.15 → 1.0 across the walk | figure walks; house pops |
| OUTRO | logo + **EP05 teaser** (legacy + container berdampingan) + follow | centered | — | — |

Bookend: hook's dark gang with one window comes back in RECAP — now we see who struck the kentongan, and he never waits.

## New components (engine/components/kampung.py)

| Component | What it does |
|---|---|
| `kentongan` | bamboo slit drum hanging from a pos-ronda pole; `hit` 0..1 swings it, mallet strikes |
| `sound_rings` | 3 concentric arcs expanding from a point after a hit (teal), fade with distance |
| `rumah` | small house: roof, door, window whose lamp glows with `light` 0..1, work dots when `busy`, `z z` when asleep, red X + spark when `broken`, signboard (serif, optional tilt) |
| `rumah_gede` | the monolith: one wide house, N rooms in a row under one roof, one MCB box; per-room light/busy, `trip` 0..1 blacks everything out, `closed` 0..1 nails a "TUTUP · RENOVASI" board across |
| `gang` | street line + kerb under a row of houses (helper: x positions) |
| `portal` | kampung portal gate (NAT gateway): two posts + striped boom; label; arrow out ✓ / in ✗ |
| `ronda_man` | tiny figure (head + body + legs) that walks with a step cycle — recap surprise |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Kebanyakan *tidur*.` | gang: kentongan + 4 dark houses, `z z` floats | whoosh | "tidur" |
| L02 | `Bangun pas ada *kejadian*.` | *tok* → rings → house 3 lights, works, dark again | thud, pop | "kejadian", "selesai" |
| L03 | `Dulu: nyala *terus*.` | rumah gede whips in, every window lit, tag `24 jam` · `semuanya` | whoosh, pop | "semuanya" |
| L04 | — | `monolith lama` → giant teal `event-driven.` | whoosh, thud | "event-driven" |
| (gap) | — | **teal bumper** `BONGKAR ARSITEKTUR · EP 04` | whoosh | chapter start |
| L05 | `Satu *rumah gede*.` | rumah gede card rises, MCB box, note "ini monolith-nya" | whoosh | "rumah" |
| L06 | `*Satu* atap.` | rooms label one by one: order · bayar · notifikasi · laporan | pop×4 | the four words |
| L07 | `Kerja cuma *satu kamar*.` | all lit; only laporan busy; red tag `idle · tetap nyala` | tick, pop | "satu" |
| L08 | `Satu *korslet*?` | spark in laporan → MCB trips → all dark; `down semua` | thud, whoosh | "korslet", "gelap" |
| L09 | `Deploy *semuanya*.` | board `TUTUP · RENOVASI` nails across; tag `deploy ulang: semuanya` | thud, pop | "ulang" |
| L10 | `Rumahnya *dipecah*.` | house splits into 4 small houses, slide apart | thud, whoosh | "dipecah" |
| L11 | `Satu function, *satu tugas*.` | signs: `order()` `bayar()` `notif()` `laporan()` | pop×4 | "function" |
| L12 | `Nggak saling *panggil*.` | wires between houses → struck; kentongan whips in | tick×3, whoosh | "panggil", "kentongan" |
| L13 | `Kentongan = *event*.` | `order masuk` tag → *tok* → rings; tag `event: order.created` | thud, pop | "dipukul", "event" |
| L14 | `Nyala, kerja, *gelap lagi*.` | bayar/notif/laporan light (one flickers first), busy, dark; order dark | pop×3, chime | "nyala", "gelap" |
| L15 | `API → *event*.` | `API` node + `order masuk` → kentongan node | pop×2 | "event" |
| L16 | `Didengar *barengan*.` | 3 function houses light together, dots from kentongan | pop×3 | "barengan" |
| L17 | `Lambda + *Function Compute*.` | provider row: `AWS Lambda` · `Alibaba Function Compute` under houses | pop×2 | "Lambda", "Function" |
| L18 | `Dalam *private network*.` | dashed teal fence draws around; outside dot bounces off, ✗ | whoosh, tick | "private" |
| L19 | `Keluar lewat *NAT gateway*.` | portal at bottom; dot goes out ✓ (in ✗) | pop, chime | "NAT" |
| L20 | `Compute overhead:` | giant teal `turun drastis.`; "lampu nyala" meter monolith full → event-driven sliver | thud, whoosh | "drastis" |
| L21 | `Satu error, *yang lain jalan*.` | gang card: laporan() broken red, others keep working | thud, pop | "error", "jalan" |
| L22 | `Deploy *satu function*.` | `deploy` tag drops on one house only, ✓ | pop, chime | "satu" |
| L23 | `Bukan soal *dipecah*.` | dark gang at night, figure at kentongan | whoosh_dark | "dipecah" |
| L24 | `*Nggak nunggu* siapa-siapa.` | *tok* → figure walks off right; houses light behind him | thud, whoosh | "nunggu", "pergi" |
| L25 | `Sehat? *Biarin*.` | small rumah gede pops with green ✓ `sehat → biarin` | pop, chime | "biarin" |
| L26 | — | logo + EP05 teaser card | pop | "berdampingan" |
| L27 | — | `+ Follow` click | click, chime | "follow" |
