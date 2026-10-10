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
    sig = d["signature"] + (f" · look {d['look']}" if d.get("look") else "")   # look (STYLE §6e) is optional
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
