"""EXPERIMENTAL — synthetic voice: SCRIPT.md → audio/voice_tts.wav + exact timing.json (source "tts").

Uses edge-tts (Microsoft Edge's online neural voices, free, needs internet — the script text is sent to Microsoft).
Each [Lxx] line is spoken separately; the word boundaries edge-tts returns become the word times, so scenes sync
without the whisper aligner. Lines are joined with natural pauses: line gap, longer after ' //' (breath),
longest at a chapter change.

A real recording always wins: as soon as audio/voice.wav exists, the pipeline aligns that instead.

Voice: "Mumeyong" — the channel's TTS voice (engine: edge-tts id-ID-ArdiNeural), one steady pace. Nothing to
configure. It mispronounces English tech terms, so a respelling lexicon is applied:
LEXICON below + optional videos/<slug>/audio/tts_lexicon.txt ("word = respelling", one per line).
"""
import asyncio
import json
import re
import subprocess

import numpy as np

from .align import parse_script, _spread_words

SR = 48000
VOICE = "id-ID-ArdiNeural"     # edge-tts voice id (must stay exact)
VOICE_NAME = "Mumeyong"        # what the CLI and docs call it
RATE = "+6%"           # casual pace, close to the 161 wpm reference
VERSION = "ardi"       # stored in timing.json; a different value → the voice is regenerated
LEAD_IN = 0.4
GAP_LINE = 0.32
GAP_BREATH = 0.6        # after a line ending in ' //'
GAP_CHAPTER = 1.0
TAIL = 0.8

# English tech term → how an Indonesian voice should say it (no spaces: one script word stays one spoken word)
LEXICON = {
    "cloud": "klaud", "serverless": "serverles", "node": "noud", "idle": "aidel", "legacy": "legasi", "pipeline": "paiplain", "streaming": "striming", "batch": "becc",
    "query": "kweri", "patch": "pecc", "restart": "ristart", "deploy": "diploi",
    "rollback": "rolbek", "cutover": "katover", "checksum": "ceksam", "sync": "sing", "real-time": "riltaim",
    "lake": "leik", "follow": "folo", "airflow": "erflo", "maxcompute": "makskompyut",
    "monolith": "monolit", "event-driven": "iven-driven",
    "kubernetes": "kubernetis", "cluster": "klaster", "traffic": "trafik", "request": "rikues",
    "auto-scaling": "oto-skeling", "load": "lod", "balancer": "belanser", "kitchen": "kicen",
    "full": "ful", "copy": "kopi", "incremental": "inkremental", "match": "mecc", "plan": "plen",
    "di-patch": "di-pecc", "di-restart": "di-ristart",
}


def _lexicon(project):
    lex = dict(LEXICON)
    f = project.audio / "tts_lexicon.txt"
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines():
            if "=" in ln and not ln.strip().startswith("#"):
                k, v = ln.split("=", 1)
                lex[k.strip().lower()] = v.strip()
    return lex


def _respell(text, lex):
    out = []
    for w in text.split():
        m = re.match(r"^([^\w]*)([\w\-]+?)([^\w]*)$", w)
        if not m:
            out.append(w)
            continue
        pre, core, post = m.groups()
        rep = lex.get(core.lower())
        if rep is None and "-" in core:
            rep = "-".join(lex.get(p.lower(), p) for p in core.split("-"))
        out.append(pre + (rep or core) + post)
    return " ".join(out)


async def _speak(text):
    import edge_tts
    for attempt in range(3):
        try:
            com = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary")
            audio, words = bytearray(), []
            async for ch in com.stream():
                if ch["type"] == "audio":
                    audio += ch["data"]
                elif ch["type"] == "WordBoundary":
                    words.append((ch["offset"] / 1e7, ch["duration"] / 1e7, ch["text"]))
            return bytes(audio), words
        except Exception as e:  # network hiccup → retry
            if attempt == 2:
                raise SystemExit(f"tts failed for {text[:40]!r}: {e}")
            await asyncio.sleep(1.5 * (attempt + 1))


async def _speak_all(texts, conc=4):
    sem = asyncio.Semaphore(conc)

    async def one(t):
        async with sem:
            return await _speak(t)
    res = await asyncio.gather(*(one(t) for t in texts), return_exceptions=True)
    for r in res:   # surface the first failure once, no "Task exception was never retrieved" noise
        if isinstance(r, BaseException):
            raise r
    return res


def _decode(mp3):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         input=mp3, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def _trim(y, thr=0.008):
    """Indices (a, b) of the voiced part, with a little air around it."""
    idx = np.flatnonzero(np.abs(y) > thr)
    if not len(idx):
        return 0, len(y)
    return max(0, idx[0] - int(0.03 * SR)), min(len(y), idx[-1] + int(0.08 * SR))


def synthesize(project):
    """Write audio/voice_tts.wav + timing.json (Mumeyong voice). Returns the timing dict."""
    lex = _lexicon(project)
    script = project.dir / "SCRIPT.md"
    marked = parse_script(script, keep_marks=True)
    lines = parse_script(script)
    spoken = [_respell(ln["text"], lex) for ln in lines]
    print(f"tts: {len(lines)} lines · suara {VOICE_NAME} (online, edge-tts)")
    results = asyncio.run(_speak_all(spoken))

    parts, t, prev_ch = [np.zeros(int(LEAD_IN * SR))], LEAD_IN, None
    for i, (ln, (mp3, bounds)) in enumerate(zip(lines, results)):
        if prev_ch is not None and ln["chapter"] != prev_ch:
            gap = GAP_CHAPTER
        elif i > 0:
            gap = GAP_BREATH if marked[i - 1]["text"].rstrip().endswith("//") else GAP_LINE
        else:
            gap = 0.0
        parts.append(np.zeros(int(gap * SR)))
        t += gap
        y = _decode(mp3)
        a, b = _trim(y)
        y = y[a:b]
        shift = a / SR
        words = ln["text"].split()
        if len(bounds) == len(words):
            ws = [{"w": w, "start": round(t + max(0.0, o - shift), 3), "end": round(t + max(0.0, o - shift + d), 3)}
                  for w, (o, d, _) in zip(words, bounds)]
        else:  # respelling split/merged a word → spread by length (still exact line edges)
            ws = _spread_words(ln["text"], t, t + len(y) / SR)
        ln["start"], ln["end"], ln["words"] = round(t, 3), round(t + len(y) / SR, 3), ws
        parts.append(y)
        t += len(y) / SR
        prev_ch = ln["chapter"]
    parts.append(np.zeros(int(TAIL * SR)))
    voice_wav = project.audio / "voice_tts.wav"
    voice_wav.parent.mkdir(parents=True, exist_ok=True)
    y = np.concatenate(parts)
    y *= 0.89 / (np.max(np.abs(y)) or 1.0)
    from .sfx import write_wav
    write_wav(voice_wav, y)
    data = {"source": "tts", "voice": VOICE, "tts": VERSION, "duration": round(len(y) / SR, 3), "lines": lines}
    json.dump(data, open(project.timing_path, "w"), ensure_ascii=False, indent=1)
    mism = sum(1 for ln, (_, bd) in zip(lines, results) if len(bd) != len(ln["text"].split()))
    print(f"✓ {voice_wav}  ({data['duration']:.1f}s)")
    print(f"✓ {project.timing_path}  (source tts{f', {mism} lines spread by length' if mism else ''})")
    return data
