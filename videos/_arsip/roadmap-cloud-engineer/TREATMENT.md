# TREATMENT — Roadmap jadi cloud engineer

> From IDENTITY.md: metaphor **jalur KRL** (skill = stasiun, sertifikat = tiket) · signature move **kereta meluncur ke
> stasiun berikutnya, stasiun yang dilewati nyala** · color **oranye `#E8861A`** · hook **mitos dicoret** ·
> structure **rute stasiun 1 → 5**. HUD `MUMEYONG · ROADMAP`. QUICK: one hero (the route) changing state.
> Cover (`v.cover_t`): L14, train at Kubernetes with every station lit.

## Composition per chapter (STYLE §6b)

| Chapter | Hero object | Layout | Camera | Transitions |
|---|---|---|---|---|
| INTRO | **10 certificate tickets** fanned in a stack → struck + dropped on "Jangan" → the **route** draws itself top→bottom, 5 stations pop, the train appears | stacked tilted cards → route strip | slow settle; pull-out as the route draws | stack drops down; route draws |
| 00 LINUX | train glides to station 1 (lights) · right: **terminal card** typing `ls -l` / `chmod` / `ps aux` on the spoken words · note "ini fondasinya" | route left + card right | push on station 1 + card | card whips in from the right |
| 01 NETWORKING | train → station 2 · right: **request path** kamu → DNS → IP → subnet, then the chain breaks ✕ between DNS and IP, "di sini" box | route + vertical chain | push on the break | whip |
| 02 SATU CLOUD | train → station 3 = **transit**: 4 branch lines fan out to 4 rows; row 1 "cloud pertama" fills deep, rows 2–4 appear and fill fast | route + branching rows | push on row 1 | whip |
| 03 IAC + K8S | train → station 4: **Terraform** code card + tags `diulang` · `di-review` · `nggak lupa` → train → station 5: **pods** pop · *surprise*: a ghost train jumps from 1 straight to 5, stations 2–4 go dead, "?" | route + code card → pods | push on code, then pull-out for the jump | whip, ghost arc |
| RECAP (dark) | **ticket vs train**: certificate ticket, then the big train slides in behind it → 5 station dots light 1 → 5 | centered object → horizontal route | push on the train | whip |
| OUTRO | logo + next video card (QRIS) + **Save** button + Follow | centered | — | — |

## New components (engine/components/transit.py)

| Component | What it does |
|---|---|
| `route_strip` | vertical commuter line: grey track draws on, colored up to `reach`, stations (ring → filled when lit, grey when dead, pulse when active), mono "STASIUN n" + name |
| `train` | KRL from the front: orange body, windscreen, white stripe, headlights; `ghost` = dashed outline |
| `cert_card` | certificate as a perforated ticket: color edge, SERTIFIKAT label, title, stub with seal |
| `save_button` | Save (outlined bookmark) → pressed → Tersimpan (filled) |
| `station_dots` | compact horizontal route for the recap bookend |

## Lines

| id | headline | visual | SFX | anchor |
|---|---|---|---|---|
| L01 | `~Sepuluh sertifikat~. *Jangan*.` | 10 cert tickets pop in a fan → strike + stack drops | pop×10, thud | "sepuluh", "jangan" |
| L02 | `Mulai dari *nol*.` | route draws, 5 stations pop, train appears at the top | whoosh, pop×5 | "rute", "lima" |
| L03 | `Mulai dari *Linux*.` | train glides to station 1, it lights | whoosh, chime | "linux" |
| L04 | (same) | terminal card types `ls -l` · `chmod +x` · `ps aux` | key×n | "terminal", "permission", "process" |
| L05 | `Ini *fondasinya*.` | note "semua stasiun nanti lewat sini" | — | "berat" |
| L06 | `*Networking*.` | train → station 2; tags IP · DNS · subnet | whoosh, pop×3 | "IP", "DNS", "subnet" |
| L07 | `Paling sering *nyangkut*.` | chain kamu → DNS → IP → subnet draws | tick | "nyangkut" |
| L08 | `Biasanya di *sini*.` | chain breaks ✕ between DNS and IP, red box "di sini" | thud | "sini" |
| L09 | `*Satu* cloud dulu.` | train → station 3; branch lines fan to 4 rows; row 1 lights, bar fills deep | whoosh, pop | "satu", "dalam" |
| L10 | (same) | rows 2–4 appear (empty) | pop×3 | "empat" |
| L11 | `Sisanya jadi *gampang*.` | rows 2–4 fill fast | tick×3 | "gampang" |
| L12 | `Infra jadi *kode*.` | train → station 4; Terraform card types | whoosh, key×n | "Terraform" |
| L13 | (same) | tags `diulang` · `di-review` · `nggak lupa` | pop×3 | "diulang", "review", "lupa" |
| L14 | `Baru *Kubernetes*.` | train → station 5; pods pop in a grid | whoosh, pop×6 | "Kubernetes" |
| L15 | `Jangan *loncat*.` | ghost train jumps 1 → 5; stations 2–4 go dead; "?" | whoosh, thud | "turun", "dilewatin" |
| L16 | `Tiket, bukan *kereta*.` | dark: certificate ticket → big train slides in | whoosh_dark, whoosh | "tiket", "keretanya" |
| L17 | `Yang penting *urutannya*.` | station dots 1 → 5 light in order | pop×5, chime | "urutannya" |
| L18 | — | logo + **Save** button clicked | click, chime | "save" |
| L19 | — | next video card: QRIS, 2 detik | pop | "berikutnya" |
| L20 | — | `+ Follow` click | click, chime | "follow" |
