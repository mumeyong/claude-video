"""EXPERIMENTAL — synthetic voice: SCRIPT.md → audio/voice_tts.wav + exact timing.json (source "tts").

Uses edge-tts (Microsoft Edge's online neural voices, free, needs internet — the script text is sent to Microsoft).
Each [Lxx] line is spoken separately; the word boundaries edge-tts returns become the word times, so scenes sync
without the whisper aligner. Lines are joined with natural pauses: line gap, longer after ' //' (breath),
longest at a chapter change.

A real recording always wins: as soon as audio/voice.wav exists, the pipeline aligns that instead.

Voice: "Mumeyong" — the channel's TTS voice (engine: edge-tts id-ID-ArdiNeural), one steady pace. Nothing to
configure. It mispronounces English tech terms, so a respelling lexicon is applied:
LEXICON below + optional videos/<slug>/audio/tts_lexicon.txt ("word = respelling", one per line).

Cartesia (opt-in, 2026-10-11, testing): put a `.cartesia` file in the repo root (git-ignored):
    key   = sk_car_...          # or env CARTESIA_API_KEY — play.cartesia.ai/keys
    voice = <voice id>          # `souffle voices` lists Indonesian voices
    only  = apple-lab           # optional: comma list of slugs that use Cartesia (omit = every video)
    skip  = slug-a, slug-b      # optional: slugs that keep the edge-tts voice (e.g. finished, frozen videos)
    # optional: model = sonic-3.6 · speed = 1.0 (0.6–1.5) · lexicon = off|on (respelling; default off)
Same contract as edge-tts: one request per [Lxx] line with word timestamps → exact timing.json, no aligner.
The script text is sent to Cartesia. Switching engine/voice regenerates the voice; the old file is kept as
audio/voice_tts.prev.wav for an A/B listen.
"""
import asyncio
import base64
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

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


CARTESIA_API = "https://api.cartesia.ai"
CARTESIA_VERSION = "2026-08-14"
CARTESIA_CFG = Path(__file__).resolve().parents[2] / ".cartesia"


def cartesia_config(slug=None):
    """Settings from .cartesia (+ env CARTESIA_API_KEY). With slug: None unless Cartesia applies to that video."""
    cfg = {}
    if CARTESIA_CFG.exists():
        for ln in CARTESIA_CFG.read_text(encoding="utf-8").splitlines():
            ln = ln.split("#", 1)[0]
            if "=" in ln:
                k, v = ln.split("=", 1)
                cfg[k.strip().lower()] = v.strip()
    if os.environ.get("CARTESIA_API_KEY"):
        cfg["key"] = os.environ["CARTESIA_API_KEY"]
    if slug is None:
        return cfg
    if not cfg.get("key") or not cfg.get("voice"):
        return None
    only = [x.strip() for x in cfg.get("only", "").split(",") if x.strip()]
    skip = [x.strip() for x in cfg.get("skip", "").split(",") if x.strip()]
    return cfg if (not only or slug in only) and slug not in skip else None


def version(project):
    """Tag stored in timing.json as "tts": a different value (engine/voice/speed changed) → the voice is regenerated."""
    cfg = cartesia_config(project.slug)
    if cfg is None:
        return VERSION
    return f"cartesia:{cfg.get('model', 'sonic-3.6')}:{cfg['voice']}:{cfg.get('speed', '1.0')}:{cfg.get('lexicon', 'off')}"


def _cartesia_req(cfg, path, body=None, timeout=60):
    req = urllib.request.Request(CARTESIA_API + path, data=None if body is None else json.dumps(body).encode(),
                                 method="GET" if body is None else "POST",
                                 headers={"Authorization": f"Bearer {cfg['key']}", "Cartesia-Version": CARTESIA_VERSION,
                                          "Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=timeout)


def _cartesia_line(cfg, text):
    """One line → (mono float64 @ SR, [(start, dur, word)]) via the SSE endpoint with word timestamps."""
    body = {"model_id": cfg.get("model", "sonic-3.6"), "transcript": text, "voice": {"id": cfg["voice"]},
            "language": "id", "add_timestamps": True,
            "output_format": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": SR}}
    if cfg.get("speed"):
        body["generation_config"] = {"speed": float(cfg["speed"])}
    for attempt in range(4):
        try:
            audio, words = bytearray(), []
            with _cartesia_req(cfg, "/tts/sse", body, timeout=120) as r:
                for raw in r:
                    ln = raw.decode("utf-8").strip()
                    if not ln.startswith("data:"):
                        continue
                    ev = json.loads(ln[5:].strip() or "{}")
                    kind = ev.get("type")
                    if kind == "chunk" and ev.get("data"):
                        audio += base64.b64decode(ev["data"])
                    elif kind == "timestamps" and ev.get("word_timestamps"):
                        wt = ev["word_timestamps"]
                        words += [(a, b - a, w) for w, a, b in zip(wt["words"], wt["start"], wt["end"])]
                    elif kind == "error":
                        raise RuntimeError(ev.get("error") or ev)
            return np.frombuffer(bytes(audio), np.float32).astype(np.float64), words
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:200]
            if e.code in (401, 402, 403) or attempt == 3:   # bad key / out of credits: retrying won't help
                raise SystemExit(f"cartesia {e.code} for {text[:40]!r}: {msg}")
        except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
            if attempt == 3:
                raise SystemExit(f"cartesia failed for {text[:40]!r}: {e}")
        import time
        time.sleep(1.5 * (attempt + 1))


def list_voices(lang="id"):
    """Print Cartesia voices for a language (needs the key in .cartesia or CARTESIA_API_KEY)."""
    cfg = cartesia_config()
    if not cfg.get("key"):
        raise SystemExit(f"no Cartesia key — put `key = sk_car_...` in {CARTESIA_CFG} (or env CARTESIA_API_KEY)")
    after, n = None, 0
    while True:
        q = f"/voices?limit=100&language={lang}" + (f"&starting_after={after}" if after else "")
        with _cartesia_req(cfg, q) as r:
            res = json.load(r)
        for v in res.get("data", []):
            n += 1
            print(f"{v['id']}  {v.get('gender') or '-':<14} {v['name']}" + (f" — {v['tagline']}" if v.get("tagline") else ""))
        if not res.get("has_more") or not res.get("next_page"):
            break
        after = res["next_page"]
    print(f"{n} voice(s) for language={lang}. Put one id in {CARTESIA_CFG.name}: voice = <id>")


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
    cfg = cartesia_config(project.slug)
    lex = _lexicon(project)
    script = project.dir / "SCRIPT.md"
    marked = parse_script(script, keep_marks=True)
    lines = parse_script(script)
    if cfg is None:
        spoken = [_respell(ln["text"], lex) for ln in lines]
        print(f"tts: {len(lines)} lines · suara {VOICE_NAME} (online, edge-tts)")
        results = [(_decode(mp3), b) for mp3, b in asyncio.run(_speak_all(spoken))]
        voice_id = VOICE
    else:
        spoken = [_respell(ln["text"], lex) if cfg.get("lexicon") == "on" else ln["text"] for ln in lines]
        print(f"tts: {len(lines)} lines · Cartesia {cfg.get('model', 'sonic-3.6')} · voice {cfg['voice']} (online)")
        with ThreadPoolExecutor(2) as ex:      # free plan: keep concurrency low
            results = list(ex.map(lambda tx: _cartesia_line(cfg, tx), spoken))
        voice_id = f"cartesia:{cfg['voice']}"

    parts, t, prev_ch = [np.zeros(int(LEAD_IN * SR))], LEAD_IN, None
    for i, (ln, (y, bounds)) in enumerate(zip(lines, results)):
        if prev_ch is not None and ln["chapter"] != prev_ch:
            gap = GAP_CHAPTER
        elif i > 0:
            gap = GAP_BREATH if marked[i - 1]["text"].rstrip().endswith("//") else GAP_LINE
        else:
            gap = 0.0
        parts.append(np.zeros(int(gap * SR)))
        t += gap
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
    tag = version(project)
    if voice_wav.exists() and project.timing_path.exists():   # engine/voice switch → keep the old take for A/B
        if json.load(open(project.timing_path)).get("tts") not in (None, tag):
            shutil.copy2(voice_wav, voice_wav.with_name("voice_tts.prev.wav"))
    y = np.concatenate(parts)
    y *= 0.89 / (np.max(np.abs(y)) or 1.0)
    from .sfx import write_wav
    write_wav(voice_wav, y)
    data = {"source": "tts", "voice": voice_id, "tts": tag, "duration": round(len(y) / SR, 3), "lines": lines}
    json.dump(data, open(project.timing_path, "w"), ensure_ascii=False, indent=1)
    mism = sum(1 for ln, (_, bd) in zip(lines, results) if len(bd) != len(ln["text"].split()))
    print(f"✓ {voice_wav}  ({data['duration']:.1f}s)")
    print(f"✓ {project.timing_path}  (source tts{f', {mism} lines spread by length' if mism else ''})")
    return data
