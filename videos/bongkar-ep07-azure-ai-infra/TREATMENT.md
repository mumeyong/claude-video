# TREATMENT — Bongkar Arsitektur EP07: Fondasi buat training AI di Azure (episode terakhir)

> From IDENTITY.md: metaphor **badminton athlete — pelatnas (training) vs match (inference)** · signature move
> **shuttle arcs over the net, each landing lights one rep dot** · signature color **orange `#E8861A`** · hook
> **myth struck out**. Tech terms English (GLOSSARY.md). No numbers. No AI brain/robot imagery.
> Cover (`v.cover`): "GPU nyala\n*pas perlu*." + court with a shuttle arc + a row of GPU cards (most dark).

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **gudang GPU**: grid of gpu_cards all lit, tag `nyala terus` → `Nggak juga.` with a strike over the myth → cards go dark except a few (`kapan`) → `training + inference` → giant orange `Azure.` → **orange bumper** | grid → pure type → full-bleed | pull-out 1.10 → 1.0; punch on "Nggak"; punch on "Azure" | grid rises; strike draws; type slams |
| 00 MASALAH | **one court** card (side view): player + shuttle launcher → arcs over the net, rep dots fill (`training · berat · sementara`) → launcher out, opponent in → one smash, `poin` (`inference · cepat`) → launcher back on the same court, shuttles collide, red `rebutan` | full-width card | push on the rep dots; punch on the smash | card rises; launcher whips |
| 01 KEPUTUSAN | **two courts** (no card): the court splits — top `LAPANGAN LATIHAN · GPU` (lights only during a scheduled block), bottom `LAPANGAN TANDING` (small, lamp always on, `selalu siap`) → coach's **jadwal** board whips in at the left: `AKS` | stacked hero, no card | push on each court; pull-out on the board | courts split vertically; board whips in |
| 02 DIAGRAM | series **arch** stack inside a dashed `AKS cluster`: `data latihan` → `GPU node pool` (3 gpu_cards light, train, then scale down to dark) → `model` → `inference pool` (2 pods, always on) → `users`; then a container box hops from `GOR Azure` to `GOR cloud lain` | stacked diagram | focus GPU pool → inference → pull out to the GORs | nodes pop row by row; container hops |
| 03 HASIL | `scalable.` typographic punch with a GPU bar rising and falling → **jadwal** strip: GPU blocks only when training, `idle` struck → two GOR cards both ✓ `nggak terkunci` | pure type → card → two cards | punch-out on "scalable"; push on the strip | type slams; strip whips in; GORs pop |
| RECAP (dark) | **gudang GPU** again (bookend): all lit → fade out one by one until only the training ones stay → night court: lamp off, then on for a short drill → serif `pas perlu.` | centered object | pull-out 1.15 → 1.0 | cards dim in a wave |
| OUTRO | **series finale**: logo + card `SERI BONGKAR ARSITEKTUR · SELESAI` with EP 01–07 ticked one by one + `Mau lanjutan? Tulis di komentar` + follow | centered | — | — |

Bookend: the hook's "GPU segudang, nyala terus" returns in RECAP and goes dark down to what's needed.

## New components (engine/components/badminton.py)

| Component | What it does |
|---|---|
| `gpu_card` | GPU board: two fans (spin when on), heatsink fins, label; `on` 0..1 lights it orange |
| `lapangan` | side-view court: floor + lines, net in the middle, two overhead lamps (`lights` 0..1), optional label |
| `pemain` | player silhouette with racket; `swing` 0..1 rotates the racket arm; `facing` ±1 |
| `shuttle` / `shuttle_arc` | shuttlecock (cork + feather skirt) · point on a parabola between two points at u |
| `pelontar` | shuttle launcher on a tripod, tube of shuttles, recoil on `fire` |
| `rep_dots` | row of repetition dots, `n_on` filled (fractional = last one fading in) |
| `jadwal` | coach's schedule board: rows with blocks on a timeline (`(f0, f1)`), playhead, hand-written title, struck block |
| `gor` | sports-hall card (arched roof) with a label = one cloud; `ok` shows a check |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `GPU *segudang*?` | 4×3 GPU grid, all lit, fans spinning; tag `nyala terus` | whoosh, tick×n | "segudang" |
| L02 | `*Nggak* juga.` | strike across the grid caption `beli GPU segudang` | thud | "Nggak" |
| L03 | `Soal *kapan*.` | grid dims to 3 lit cards; tag `mahal` | tick, pop | "kapan" |
| L04 | — | `training + inference` → giant orange `Azure.` | whoosh, thud | "Azure" |
| (gap) | — | **orange bumper** `BONGKAR ARSITEKTUR · EP 07` | whoosh | chapter start |
| L05 | `Model = *atlet*.` | court card rises, player | whoosh | "atlet" |
| L06 | `Masa *latihan*.` | launcher fires; arcs over the net; rep dots fill (one shuttle stuck on the net) | pop×n | "latihan" |
| L07 | `Itu *training*.` | tags `berat` · `sementara` | pop×2 | "training" |
| L08 | `Pas *tanding*.` | launcher whips out, opponent in; one smash; `poin` | whoosh, thud | "tanding" |
| L09 | `Rebutan, *kalah* dua-duanya.` | launcher back on the same court; collision; red `rebutan` | thud | "kalah" |
| L10 | `Lapangannya *dipisah*.` | court splits into two | whoosh, thud | "dipisah" |
| L11 | `Latihan pakai *GPU*.` | top court: GPU tag; lights on during a block | pop | "GPU", "jadwal" |
| L12 | `Tanding: *selalu siap*.` | bottom court: small lamp steady; tag `selalu siap` | pop | "siap" |
| L13 | `Pelatihnya: *AKS*.` | jadwal board whips in; tag `Kubernetes · AKS` | whoosh, pop | "Kubernetes" |
| L14 | `Masuk ke *GPU pool*.` | data → GPU node pool, cards light | pop×3 | "GPU" |
| L15 | `Selesai, *scale turun*.` | GPU cards go dark one by one | tick×3 | "turun" |
| L16 | `Deploy ke *inference*.` | model → inference pool → users | pop×2 | "inference" |
| L17 | `Bisa pindah *cloud*.` | container hops GOR Azure → GOR cloud lain | whoosh, chime | "lain" |
| L18 | `Compute-nya *scalable*.` | giant `scalable.`, GPU bar rises then falls | thud | "scalable" |
| L19 | `Nggak *idle*.` | jadwal strip: GPU only in blocks; `idle` struck | tick, pop | "idle" |
| L20 | `Nggak *terkunci*.` | two GOR cards ✓ | pop×2, chime | "terkunci" |
| L21 | `Bukan soal *paling banyak*.` | dark: GPU grid all lit | whoosh_dark | "banyak" |
| L22 | `Tahu *kapan*.` | cards fade in a wave until 3 remain | tick×n | "latihan" |
| L23 | `Latihan *pas perlu*.` | night court, one short drill, serif `pas perlu.` | chime | "perlu" |
| L24 | — | finale card: EP 01–07 ticked | tick×7, chime | "Bongkar" |
| L25 | — | `+ Follow` click | click, chime | "follow" |
