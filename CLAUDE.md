# MUMEYONG — motion video studio (HTML films + Python + ffmpeg)

Vertical 1080×1920 / 60 fps animated explainers in **Bahasa Indonesia**. Every frame is code: `frame = f(t)`.
New videos are **HTML films** by default (`film.html`, the grak/cheese look — skill `WEB.md`) inside the Python engine,
which keeps the identity (voice, logos, mix). grak and cheese are merged here — one tool.
Workflow: skill `mumeyong-video` (`SKILL.md`). **Fixed: the voice + opening logo + ending logo (`IDENTITY.md`). Everything else is Claude's call.** User guide: `START.md`
(keep it in sync when commands change).

## Rules
1. **Claude never renders.** Never run `still`, `sheet`, `preview`, `render`, `mix`, `go`, `auto` or any ffmpeg encode.
   Claude may run only: `check [--dry]`, `critique` (¼-scale PNG review sheets, no encode — approved 2026-10-13),
   `estimate`, `naskah`, `api`, `recent`, `register`, `ref`, `capture`, `beats` (no encode), and read-only `npx hyperframes catalog|docs` lookups. Hand the user ONE copy-paste command and stop.
2. **Autopilot.** Every gate is pre-approved — make the call, write the file, keep going until the check is clean.
   Stop early only for a fact only the user knows; prefer a safe default and list the open question.
3. **Order:** SCRIPT.md (+ NASKAH.md) → PLAN.md with the Frame (+ `register`) → film.html + scenes.py (or scenes.py
   alone with `--py`) → `check --dry` → critique → user renders.
   Every SCRIPT.md change → `python -m engine naskah <slug>` (never hand-edit NASKAH.md; the user records from it).
4. **Never `git commit` / `git push` without asking.** Suggest the message.
5. **frame = f(t):** pure draw functions, seeded randomness only, no state between frames.
6. **Voice is the clock:** times come from `timing.json` (`T.line`, `T.word`), never typed seconds.
7. **Values have names:** use `engine/tokens.py`, or a video's own palette/sizes as named constants at the top of
   scenes.py — no magic numbers buried in draw code.
8. **Engine vs video:** reusable → `engine/components/` (add a parameter, don't fork); one-off → `videos/<slug>/scenes.py`.
9. **IDENTITY.md is law** (voice, opening logo, ending logo, no invented facts) — flag a conflict before doing it.
10. **Ideas** live in `ideas/` (strategy: `ideas/STRATEGY.md`). "Simpan ide" → `NN-slug.md` from `_TEMPLATE.md` + a row
    in `ideas/README.md`. Production → status 🎬 + link.
11. **Every video ships** a cover (`v.cover`) and `hasil/<slug>/POST.md` (`POST_TEMPLATE.md`). After posting: numbers into
    POST.md, then archive `videos/<slug>` → `videos/_arsip/`, `hasil/<slug>` → `hasil/_tayang/`.
12. **Free craft:** look, colors, fonts, metaphor, structure, layout, motion are Claude's call. Don't repeat the last video (`recent <slug>`,
    info only); the critique loop judges quality — add a rule only when the same mistake happens twice.
13. **Tech terms stay English** (`GLOSSARY.md`).
14. **HyperFrames skills are a library, not the workflow.** `mumeyong-video` owns every video here — never route
    through `hyperframes` / `faceless-explainer` / `general-video` etc., never `hyperframes init/render/preview/snapshot/tts`.
    Use `hyperframes-animation`, `-keyframes`, `-creative`, `-registry` for motion craft inside film.html (WEB.md § HyperFrames).

## Layout
```
engine/            tokens, draw, video, timing, components/, audio/, render, web (HTML films), ref, CLI   (API.md)
web/               film harness: run.mjs (Playwright frames/stills/cues/check/capture/serve), lib/ (motion, apple,
                   film, hf = GSAP/HyperFrames bridge, fonts.css) — needs `cd web && npm install` once
videos/<slug>/     in production: SCRIPT.md, NASKAH.md, PLAN.md, timing.json, scenes.py, REVIEW, CRITIQUE.md, audio/, out/
videos/_arsip/     finished (frozen) · videos/_lab/ proof sheets
hasil/<slug>/      final, not posted: mp4 + cover.png + POST.md · hasil/_tayang/ posted
ideas/             backlog + STRATEGY.md + REGISTRY.md
_archive/rules-v*/   older rule sets (history only — don't read)
```

## Commands (the user runs these)
```bash
claude-video <slug>              # naskah → voice (align voice.wav, else TTS) → check → final → hasil/<slug>/
claude-video <slug> preview      # optional 540p round
claude-video "Judul video"       # autopilot: Claude headless writes everything, then renders
claude-video "promo X" --url https://x.com --dur 20   # + facts + real screenshots from a page, ~20 s
claude-video "Judul" --ref clip.mp4 | --py           # study a reference look · draw in Python instead of HTML
claude-video <slug> --fix 12,15                      # HTML film: re-render only seconds 12–15 of the film
claude-video export <slug> · serve                   # per-platform files · live film preview in the browser
claude-video ideas | help
```

## Gotchas
- faster-whisper: pass audio as a numpy array (`align.py` does).
- Always `import engine` before `gi` (it points Pango at `assets/fonts`).
- Numbers on screen: Indonesian format via `fmt_id()`.
- HTML film frames are cached in `out/.web/` keyed by a hash of the page + data + assets (can be GBs at 60 fps).
- Wrapped text under a scaled canvas: Pango line spacing collapses — wrap in design units (see `obrolan._wrap`).

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
