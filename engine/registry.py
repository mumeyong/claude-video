"""`python -m engine register <slug>` — update the index tables from the <!-- registry … --> block in PLAN.md.

Upserts: the video's row in ideas/REGISTRY.md (+ its music and new components) and its row in the right pillar
section of hasil/README.md. Text only — Claude may run it. Saves hand-editing big markdown tables.
"""
import re

from .project import ROOT, find

KEYS = ("pilar", "metafora", "signature", "color", "hook", "struktur", "komponen", "musik", "durasi")
SECTION = {"B": "## B · Broad", "C": "## C · Karier", "D": "## D · Seri Bongkar Arsitektur"}


def read_block(slug):
    path = find("videos", slug) / "PLAN.md"
    m = re.search(r"<!--\s*registry(.*?)-->", path.read_text(), re.S) if path.exists() else None
    if not m:
        raise SystemExit(f"{path}: no <!-- registry … --> block")
    d = {}
    for ln in m.group(1).strip().splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            d[k.strip().lower()] = v.strip()
    miss = [k for k in KEYS if not d.get(k)]
    if miss:
        raise SystemExit(f"registry block missing: {', '.join(miss)}")
    return d


def _upsert_row(lines, start, end, key, row):
    """Replace the table row containing `key` within lines[start:end], else insert after the last table row."""
    last = None
    for i in range(start, end):
        if lines[i].startswith("|"):
            if key in lines[i]:
                lines[i] = row
                return "updated"
            last = i
    if last is None:
        raise SystemExit("no table found in section")
    lines.insert(last + 1, row)
    return "added"


def register(slug):
    d = read_block(slug)
    # ── ideas/REGISTRY.md ────────────────────────────────────────────────
    p = ROOT / "ideas" / "REGISTRY.md"
    lines = p.read_text().split("\n")
    end = next(i for i, ln in enumerate(lines) if ln.startswith("## Musik"))
    sig = d["signature"] + (f" · look {d['look']}" if d.get("look") else "")   # look (STYLE §1) is optional
    row = (f"| [{slug}](../{find('videos', slug).relative_to(ROOT).as_posix()}/PLAN.md) | {d['metafora']} | {sig} | {d['color']} | {d['hook']} | "
           f"{d['struktur']} | {d['komponen']} | — |")
    r1 = _upsert_row(lines, 0, end, f"[{slug}](", row)
    text = "\n".join(lines)
    music = f"{slug} {d['musik']}"
    if slug not in text.split("## Musik", 1)[1].split("##", 1)[0]:
        text = re.sub(r"(## Musik[^\n]*\n[^\n]*?)(\. Video berikutnya)", lambda m: f"{m.group(1)} · {music}{m.group(2)}",
                      text, count=1)
    comps = [x.strip() for x in d["komponen"].split(",") if x.strip()]
    sect = text.split("## Komponen yang sudah ada", 1)
    if len(sect) == 2:
        new = [c for c in comps if not re.search(rf"(^|[ ·]){re.escape(c)}( |$|·)", sect[1], re.M)]
        if new:
            text = text.rstrip("\n") + " ·\n" + " · ".join(new) + "\n"
    p.write_text(text)
    # ── hasil/README.md ──────────────────────────────────────────────────
    p = ROOT / "hasil" / "README.md"
    lines = p.read_text().split("\n")
    head = SECTION.get(d["pilar"].upper()[:1], "## Lainnya")
    try:
        s = next(i for i, ln in enumerate(lines) if ln.startswith(head))
    except StopIteration:
        raise SystemExit(f"hasil/README.md: section '{head}' not found")
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ") or lines[i].startswith("**Status")),
             len(lines))
    hd = find("hasil", slug)
    has_post = (hd / "POST.md").exists()
    has_mp4 = (hd / f"{slug}.mp4").exists()
    status = "📦 final — mp4 + cover + POST.md" if has_mp4 else ("🎬 produksi — POST.md siap" if has_post else "🎬 produksi")
    row = f"| — | [{slug}]({hd.relative_to(ROOT / 'hasil').as_posix()}/) | ± {d['durasi']} s | — | {status} |"
    r2 = _upsert_row(lines, s, e, f"[{slug}](", row)
    p.write_text("\n".join(lines))
    print(f"✓ ideas/REGISTRY.md row {r1} · hasil/README.md ({head[3:]}) row {r2} · status: {status}")


def _plan_rows(path, keys=("Look", "Material", "Suara")):
    """'| Look (STYLE §1) | … |' style identity rows of a PLAN.md, shortened."""
    out = []
    for ln in path.read_text().splitlines() if path.exists() else []:
        cells = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(cells) >= 2 and any(cells[0].startswith(k) for k in keys):
            out.append(f"{cells[0].split(' (')[0]}: {cells[1][:160]}")
    return out


def recent(slug, n=3):
    """`python -m engine recent <slug>` — everything the new video must differ from, in one short print, so nobody
    opens old scenes.py / SCRIPT.md / the whole REGISTRY: the last n REGISTRY rows, their look/material/sound rows,
    the music rotation, and (series) the previous episode's identity + spoken lines for continuity."""
    reg = (ROOT / "ideas" / "REGISTRY.md").read_text()
    table = reg.split("## Musik", 1)[0]
    rows = []
    for ln in table.splitlines():
        m = re.match(r"\|\s*\[([^\]]+)\]", ln)
        if m and m.group(1) != slug:
            rows.append((m.group(1), [x.strip() for x in ln.strip().strip("|").split("|")]))
    print(f"## last {n} videos (REGISTRY) — info only: don't repeat yourself, everything else is free")
    for s, cells in rows[-n:]:
        print(f"- {s}: " + " · ".join(c[:150] for c in cells[1:6]))
        for r in _plan_rows(find("videos", s) / "PLAN.md"):
            print(f"    {r}")
    mus = reg.split("## Musik", 1)[1].split("\n", 2)[1]
    print(f"\n## music rotation (latest last)\n{' · '.join(mus.split(' · ')[-5:])[:400]}")
    m = re.match(r"(.+-ep)(\d+)-", slug)
    if m:
        prev = f"{m.group(1)}{int(m.group(2)) - 1:02d}-"
        hits = sorted(p for p in (ROOT / "videos").glob(f"**/{prev}*") if p.is_dir() and (p / "SCRIPT.md").exists())
        if hits:
            d = hits[0]
            print(f"\n## previous episode: {d.name} (continuity — callbacks only, do not copy)")
            try:
                b = read_block(d.name)
                print(f"metafora: {b['metafora'][:220]}\nsignature: {b['signature'][:200]}")
            except SystemExit:
                pass
            lines = re.findall(r"^\[L\d+\]\s*(.+)$", (d / "SCRIPT.md").read_text(), re.M)
            print("lines: " + " ".join(re.sub(r"[*/]|\s{2,}", "", x).strip() for x in lines)[:1400])
    return 0
