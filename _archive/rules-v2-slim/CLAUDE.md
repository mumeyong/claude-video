# MUMEYONG — motion video studio (Python + ffmpeg)

Vertical 1080×1920 / 60 fps animated explainers in **Bahasa Indonesia**. Every frame is code: `frame = f(t)`.
Workflow: skill `mumeyong-video` (`.claude/skills/mumeyong-video/SKILL.md` → `STYLE.md`). User guide: `START.md`
(keep it in sync when commands change).

## Rules
1. **Claude never renders.** Never run `still`, `sheet`, `preview`, `render`, `mix`, `go`, `auto` or any ffmpeg encode.
   Claude may run only: `check [--dry]`, `critique` (¼-scale PNG review sheets, no encode — approved 2026-10-13),
   `estimate`, `naskah`, `api`, `recent`, `register`. Hand the user ONE copy-paste command and stop.
2. **Autopilot.** Every gate is pre-approved — make the call, write the file, keep going until the check is clean.
   Stop early only for a fact only the user knows; prefer a safe default and list the open question.
3. **Order:** SCRIPT.md (+ NASKAH.md) → PLAN.md (+ `register`) → scenes.py → `check --dry` → critique → user renders.
   Every SCRIPT.md change → `python -m engine naskah <slug>` (never hand-edit NASKAH.md; the user records from it).
4. **Never `git commit` / `git push` without asking.** Suggest the message.
5. **frame = f(t):** pure draw functions, seeded randomness only, no state between frames.
6. **Voice is the clock:** times come from `timing.json` (`T.line`, `T.word`), never typed seconds.
7. **Tokens only:** colors, sizes, fonts, durations from `engine/tokens.py`. New token → STYLE.md too.
8. **Engine vs video:** reusable → `engine/components/` (add a parameter, don't fork); one-off → `videos/<slug>/scenes.py`.
9. **STYLE.md's banned list is law** — if a request conflicts with it, say so before doing it.
10. **Ideas** live in `ideas/` (strategy: `ideas/STRATEGY.md`). "Simpan ide" → `NN-slug.md` from `_TEMPLATE.md` + a row
    in `ideas/README.md`. Production → status 🎬 + link.
11. **Every video ships** a cover (`v.cover`) and `hasil/<slug>/POST.md` (`POST_TEMPLATE.md`). After posting: numbers into
    POST.md, then archive `videos/<slug>` → `videos/_arsip/`, `hasil/<slug>` → `hasil/_tayang/`.
12. **Unique, never generic:** PLAN.md identity differs from the previous video (STYLE §3, `recent <slug>`).
13. **Tech terms stay English** (`GLOSSARY.md`).

## Layout
```
engine/            tokens, draw, video, timing, components/, audio/, render, CLI   (API.md = one line per function)
videos/<slug>/     in production: SCRIPT.md, NASKAH.md, PLAN.md, timing.json, scenes.py, REVIEW, CRITIQUE.md, audio/, out/
videos/_arsip/     finished (frozen) · videos/_lab/ proof sheets
hasil/<slug>/      final, not posted: mp4 + cover.png + POST.md · hasil/_tayang/ posted
ideas/             backlog + STRATEGY.md + REGISTRY.md
_archive/rules-v1/ the old long rules (history only — don't read)
```

## Commands (the user runs these)
```bash
claude-video <slug>              # naskah → voice (align voice.wav, else TTS) → check → final → hasil/<slug>/
claude-video <slug> preview      # optional 540p round
claude-video "Judul video"       # autopilot: Claude headless writes everything, then renders
claude-video ideas | help
```

## Gotchas
- faster-whisper: pass audio as a numpy array (`align.py` does).
- Always `import engine` before `gi` (it points Pango at `assets/fonts`).
- Numbers on screen: Indonesian format via `fmt_id()`.
- Wrapped text under a scaled canvas: Pango line spacing collapses — wrap in design units (see `obrolan._wrap`).

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
