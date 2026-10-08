# TREATMENT — 5 tanda biaya cloud kamu bocor (QUICK)

> From IDENTITY.md: metaphor **prepaid token meter + one power strip** · signature move **meter LED blinks fast →
> slows after each fix; the plug is pulled and drops** · color **teal** · hook **number first ($5.000/bulan, real)** ·
> structure **countdown 5 → 1**. First video with `fx.py` (ghost_trail · land/squash · contact_shadow · settle).
> Cover (`v.cover`): "Meteran cloud\nkamu *bocor*?" + token meter + power strip.

## Composition (QUICK: one hero object changing state; camera move per chapter; punch every ~15 s)

| Chapter | Hero state | Layout | Camera | Punch |
|---|---|---|---|---|
| INTRO | `$5.000` odometer count-up + `/ bulan · dipotong` → token meter whips in, LED frantic, LCD `LAJU: boros` → 5 countdown dots | pure type → object | pull-out 1.08 → 1.0; push on the LED | `$5.000` |
| 00 TANDA 5 & 4 | **wall card**: meter top-left, giant numeral top-right, 5 appliance tiles + power strip at the bottom. `5` slams → colokan T beranak tile (tangled adapters, `?` tags) → handwritten tag `tim: payment` pinned ✓, LED slows · `4` slams → kulkas tile stuffed with old boxes → boxes slide out, ✓, LED slows | full-width card | focus tile 5 → tile 4; small punch on each numeral | numerals |
| 01 TANDA 3 & 2 | same wall: `3` → AC tile labelled `2 PK`, CPU bar barely moving → label swaps to `½ PK` (`right-sizing`), ✓ · `2` → charger tile glowing, no phone → **plug pulled, flies (ghost trail), drops on the floor (squash + contact shadow)**, ✓ | full-width card | push on AC; follow the plug down | numerals + plug drop |
| 02 NOMOR 1 | `1` slams bigger → lamp tile in sunlight (sun icon) → `schedule` strip: lamp on only `jam kerja`, off nights/weekend → LED almost calm, LCD `LAJU: normal` | full-width card → strip | punch-in on `1`; pull-out | `1` |
| RECAP (dark) | **wall of meters** (rusun panel 4×3): all blinking fast, ours (center, teal) slow → serif `dibiarin.` | grid, centered | pull-out 1.25 → 1.0 from our meter | surprise |
| OUTRO | logo + **Save** button (teal) click + Follow | centered | — | — |

## New components (engine/components/listrik.py)

| Component | What it does |
|---|---|
| `pulse_led` | LED on/off from a piecewise blink rate — phase = ∫ rate dt, so any t renders the same (frame = f(t)) |
| `token_meter` | prepaid meter: body, LCD (label + rate bar + `boros`/`normal`), keypad, the pulse LED |
| `stop_kontak` | long power strip with n sockets; each socket has a plug (`out` 0..1 lifts it) + cable up to its tile |
| `alat` | the five appliances as line drawings in a tile: `colokan_t`, `kulkas`, `ac`, `charger`, `lampu`; per-kind state (fixed 0..1) |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `Dipotong *sebulan*.` | `$5.000` odometer + `/ bulan` | tick×n, thud | "potong" |
| L02 | `Dari yang *kecil*.` | meter whips in, LED frantic, LCD `boros` | whoosh | "kecil" |
| L03 | `Hitung *mundur*.` | 5 dots `5 4 3 2 1`, `1` marked `paling sering` | pop×5 | "satu" |
| L04 | `#5 · Tanpa *tag*.` | wall card; `5` slams; colokan T tile highlighted | thud | "tag" |
| L05 | `Punya *siapa*?` | `?` tags over the tangle → handwritten `tag: tim-payment` pins ✓, LED slows | pop, chime | "siapa" |
| L06 | `#4 · Snapshot *numpuk*.` | `4` slams; kulkas tile | thud | "numpuk" |
| L07 | `Dibayar *tiap bulan*.` | old boxes `2024`… slide out, ✓, LED slows | whoosh, chime | "basi" |
| L08 | `#3 · Instance *kegedean*.` | `3` slams; AC `2 PK` tile | thud | "kegedean" |
| L09 | `CPU kepakai *sedikit*.` | tiny CPU bar barely moving | tick | "sedikit" |
| L10 | `Obatnya: *right-sizing*.` | `2 PK` → `½ PK`, ✓, LED slows | pop, chime | "right-sizing" |
| L11 | `#2 · Disk *lepas*.` | `2` slams; charger tile glowing | thud | "apa-apa" |
| L12 | `Tetap *nyedot*.` | plug pulled → flies → lands on floor (squash + shadow), ✓, LED slows | whoosh, thud, chime | "nyedot" |
| L13 | `#1 · Nyala *24 jam*.` | big `1`; lamp tile in the sun | thud | "jam kerja" |
| L14 | `Matiin pakai *schedule*.` | schedule strip (on in work hours only), lamp off, LCD `normal` | tick×3, chime | "matiin" |
| L15 | `Yang kecil, *dibiarin*.` | dark: wall of meters, ours calm | whoosh_dark | "dibiarin" |
| L16 | `Bulan depan *beda*.` | our meter's LCD bar drops | chime | "beda" |
| L17 | — | Save button click | click, chime | "save" |
| L18 | — | Follow click | click, chime | "follow" |
