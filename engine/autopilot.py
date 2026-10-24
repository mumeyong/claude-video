"""Autopilot: run Claude Code headless to write a whole video (idea → SCRIPT → NASKAH → scenes.py → PLAN →
cover + POST.md → check --dry clean → critique loop), so `souffle "Judul"` can go straight on to the final render.

The user runs this (it spawns `claude -p`). The headless Claude only writes text files and may run the
text-only engine commands (check / naskah / estimate / api / register) plus `critique` (PNG review sheets it
reads back — STYLE §6); it can never render video or audio — those Bash commands are simply not allowed. Progress is streamed as one line per tool call.
"""
import json
import shutil
import subprocess
import sys

from .project import ROOT

PROMPT = ROOT / ".claude" / "skills" / "mumeyong-video" / "AUTOPILOT.md"
PY = ".venv/bin/python -m engine"
ALLOWED = ["Read", "Write", "Edit", "Glob", "Grep", "Skill", "TodoWrite",
           *(f"Bash({PY} {c}:*)" for c in ("check", "naskah", "estimate", "api", "register", "ideas", "ls", "critique",
                                            "recent", "ref", "capture", "beats")),
           *(f"Bash(python -m engine {c}:*)" for c in ("check", "naskah", "estimate", "api", "register", "critique",
                                                       "recent", "ref", "capture", "beats")),
           "Bash(ls:*)", "WebFetch"]   # WebFetch: read the --url page for real facts


def _short(tool, inp):
    if tool in ("Write", "Edit", "Read"):
        return str(inp.get("file_path", "")).replace(str(ROOT) + "/", "")
    if tool == "Bash":
        return inp.get("command", "")[:90]
    if tool in ("Glob", "Grep"):
        return inp.get("pattern", "")
    if tool == "Skill":
        return inp.get("skill", "")
    return ""


MODE = {
    "web": "**HTML film** (default): gambarnya `videos/{{SLUG}}/film.html` — look grak/cheese, baca `WEB.md`. "
           "`scenes.py` cuma bungkus identitas (film dari detik 0 + logo penutup, TANPA logo pembuka) dari `templates/scenes_web.py`.",
    "py": "**Python**: semua digambar di `scenes.py` (`api core` + `api index`, contoh `templates/scenes.py`).",
}


def autopilot(slug, title, note="", mode="web"):
    """Write videos/<slug>/ with Claude headless. Returns 0 when scenes.py exists afterwards."""
    if not shutil.which("claude"):
        sys.exit("`claude` (Claude Code CLI) nggak ketemu di PATH")
    prompt = PROMPT.read_text(encoding="utf-8").replace("{{MODE}}", MODE[mode])
    prompt = prompt.replace("{{SLUG}}", slug).replace("{{TITLE}}", title)
    if note:
        prompt += f"\n\n## Catatan tambahan dari user\n{note}\n"
    # videos/ and hasil/ may be symlinks to another drive: grant their real paths, or every Write is refused
    extra = sorted({str(p.resolve()) for p in (ROOT / "videos", ROOT / "hasil") if p.resolve() != p.absolute()})
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", *(["--add-dir", *extra] if extra else []),
           "--allowedTools", *ALLOWED]
    print(f"━━ autopilot: Claude nulis videos/{slug}/ (naskah → plan → scenes.py → check). ± 10–25 menit…")
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, text=True)
    result = None
    for raw in proc.stdout:
        try:
            ev = json.loads(raw)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for b in ev.get("message", {}).get("content", []):
                if b.get("type") == "tool_use":
                    print(f"  · {b['name']:6s} {_short(b['name'], b.get('input', {}))}", flush=True)
        elif ev.get("type") == "result":
            result = ev
    proc.wait()
    log = ROOT / "videos" / slug / "out" / "autopilot.md"
    if result:
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(result.get("result") or "", encoding="utf-8")
        print(f"\n{result.get('result', '').strip()}\n")
        cost = result.get("total_cost_usd")
        print(f"  (ringkasan: {log.relative_to(ROOT)}" + (f" · ${cost:.2f}" if cost else "") + ")")
    if proc.returncode or not (ROOT / "videos" / slug / "scenes.py").exists():
        print(f"✗ autopilot belum selesai — buka `claude` di {ROOT} dan bilang: \"lanjutin video {slug}\"")
        return 1
    return 0
