"""SCRIPT.md + voice.wav → timing.json.

SCRIPT.md format:
    # Judul video
    ## INTRO
    [L01] Ada yang minta tutorialnya, oke, aku bongkar semua.
    [L02] ...
    ## 00 · SIAPKAN
    [L05] ...
Lines without an [Lxx] tag (notes, > quotes, blank) are ignored.
"""
import json
import re
import subprocess
from difflib import SequenceMatcher

import numpy as np

from ..timing import norm

WPS = 2.68          # words/second while speaking (reference: 161 wpm)
GAP_LINE = 0.38     # pause between lines
GAP_CHAPTER = 1.3   # pause at chapter change (transition breathing room)
LEAD_IN = 0.4


def parse_script(path, keep_marks=False):
    """keep_marks=False strips read-aloud marks (*stress*, trailing //) — timing never sees them."""
    lines, chapter = [], ""
    for raw in open(path, encoding="utf-8"):
        raw = raw.strip()
        m = re.match(r"^##\s+(.+)$", raw)
        if m:
            chapter = m.group(1).strip()
            continue
        m = re.match(r"^\[(L\d+[a-z]?)\]\s+(.+)$", raw)
        if m:
            text = m.group(2).strip()
            if not keep_marks:
                text = re.sub(r"\s*//\s*$", "", text).replace("*", "").strip()
            lines.append({"id": m.group(1), "chapter": chapter, "text": text})
    ids = [ln["id"] for ln in lines]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise SystemExit(f"duplicate line ids in SCRIPT.md: {sorted(dup)}")
    return lines


def _spread_words(text, start, end):
    """Distribute words over [start, end] by character length."""
    ws = text.split()
    lens = [len(w) + 1 for w in ws]
    tot = sum(lens)
    out, t = [], start
    for w, L in zip(ws, lens):
        d = (end - start) * L / tot
        out.append({"w": w, "start": round(t, 3), "end": round(t + d * 0.92, 3)})
        t += d
    return out


def estimate(script_path, out_path):
    lines = parse_script(script_path)
    t, prev_ch = LEAD_IN, None
    for ln in lines:
        if prev_ch is not None and ln["chapter"] != prev_ch:
            t += GAP_CHAPTER - GAP_LINE
        n = len(ln["text"].split())
        dur = max(1.0, n / WPS)
        ln["start"], ln["end"] = round(t, 3), round(t + dur, 3)
        ln["words"] = _spread_words(ln["text"], t, t + dur)
        t += dur + GAP_LINE
        prev_ch = ln["chapter"]
    data = {"source": "estimate", "duration": round(t + 0.6, 3), "lines": lines}
    json.dump(data, open(out_path, "w"), ensure_ascii=False, indent=1)
    print(f"✓ {out_path}  (estimate, {len(lines)} lines, {data['duration']:.1f}s)")
    return data


def _load_audio(path, sr=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def _duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def transcribe(voice, model="small", lang="id"):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(_load_audio(voice), language=lang, word_timestamps=True, vad_filter=False,
                           condition_on_previous_text=False)
    words = []
    for s in segs:
        for w in s.words:
            words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
    return words


def _score(a, b):
    return SequenceMatcher(None, " ".join(a), " ".join(b), autojunk=False).ratio()


def align(script_path, voice, out_path, model="small", lang="id", hints=None):
    """Match each script line to the transcript in order. Retakes: the LAST good take wins."""
    lines = parse_script(script_path)
    tw = transcribe(voice, model, lang)
    tn = [norm(w["w"]) for w in tw]
    if hints:  # e.g. {"cloud": "claude"} for words whisper keeps mishearing
        tn = [hints.get(x, x) for x in tn]
    pos, report = 0, []
    for ln in lines:
        sw = [norm(w) for w in ln["text"].split()]
        sw = [w for w in sw if w]
        k = len(sw)
        cands = []
        for s in range(pos, min(len(tn), pos + 80 + 6 * k)):
            best = (0, 0)
            for L in range(max(1, k - 3), k + 4):
                sc = _score(sw, tn[s:s + L])
                if sc > best[0]:
                    best = (sc, L)
            if best[0] >= 0.62:
                cands.append((s, best[1], best[0]))
        if not cands:
            ln["start"] = ln["end"] = None
            report.append((ln["id"], 0.0, "NOT FOUND"))
            continue
        # cluster of retakes = candidates starting before the first one's end + slack; take the last strong one
        first = cands[0]
        horizon = first[0] + first[1] * 3 + 12
        cluster = [c for c in cands if c[0] <= horizon]
        top = max(c[2] for c in cluster)
        # non-max suppression: among overlapping windows keep the best; then pick the last take
        takes = []
        for c in cluster:
            if c[2] >= top - 0.12:
                if takes and c[0] < takes[-1][0] + takes[-1][1]:
                    if c[2] > takes[-1][2]:
                        takes[-1] = c
                else:
                    takes.append(c)
        s, L, sc = takes[-1]
        win = tw[s:s + L]
        # map script words → transcript word times
        sm = SequenceMatcher(None, sw, tn[s:s + L], autojunk=False)
        times = [None] * k
        for a, b, size in sm.get_matching_blocks():
            for i in range(size):
                times[a + i] = (win[b + i]["start"], win[b + i]["end"])
        st, en = win[0]["start"], win[-1]["end"]
        known = [(i, tt) for i, tt in enumerate(times) if tt]
        words_out = []
        orig = [w for w in ln["text"].split() if norm(w)]
        for i, w in enumerate(orig):
            if times[i]:
                ws, we = times[i]
            else:  # interpolate between neighbours
                before = [tt for j, tt in known if j < i]
                after = [tt for j, tt in known if j > i]
                ws = before[-1][1] if before else st
                we = after[0][0] if after else en
            words_out.append({"w": w, "start": ws, "end": we})
        ln["start"], ln["end"], ln["words"] = st, en, words_out
        report.append((ln["id"], sc, f"take {len(takes)}/{len(takes)}" if len(takes) > 1 else ""))
        pos = s + L
    # fill lines that were not found by estimating between neighbours
    for i, ln in enumerate(lines):
        if ln["start"] is None:
            prev_end = next((lines[j]["end"] for j in range(i - 1, -1, -1) if lines[j]["start"] is not None), 0.0)
            nxt = next((lines[j]["start"] for j in range(i + 1, len(lines)) if lines[j]["start"] is not None),
                       prev_end + len(ln["text"].split()) / WPS + 0.5)
            ln["start"], ln["end"] = prev_end + 0.2, max(prev_end + 0.4, nxt - 0.2)
            ln["words"] = _spread_words(ln["text"], ln["start"], ln["end"])
    data = {"source": "whisper", "duration": round(_duration(voice), 3), "lines": lines,
            "transcript": " ".join(w["w"] for w in tw)}
    json.dump(data, open(out_path, "w"), ensure_ascii=False, indent=1)
    for lid, sc, note in report:
        flag = "  ← check" if sc < 0.75 else ""
        print(f"  {lid:5s} {sc:4.2f} {note}{flag}")
    print(f"✓ {out_path}  (whisper, {len(lines)} lines, {data['duration']:.1f}s)")
    return data
