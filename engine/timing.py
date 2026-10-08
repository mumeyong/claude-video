"""Voice-driven timing. Scenes ask for times by script line / word, never raw seconds.

timing.json (written by `python -m engine align`):
{
  "source": "whisper" | "estimate",
  "duration": 152.4,                       # length of voice.wav (or estimate)
  "lines": [{"id": "L01", "chapter": "INTRO", "text": "...", "start": 0.0, "end": 4.36,
             "words": [{"w": "Ada", "start": 0.0, "end": 0.21}, ...]}, ...]
}
"""
import json
import re
import unicodedata


def norm(word):
    w = unicodedata.normalize("NFKD", word.lower())
    return re.sub(r"[^a-z0-9]", "", w)


class Line:
    def __init__(self, d):
        self.id = d["id"]
        self.chapter = d.get("chapter", "")
        self.text = d["text"]
        self.start = float(d["start"])
        self.end = float(d["end"])
        self.words = d.get("words", [])

    @property
    def dur(self):
        return self.end - self.start

    def word(self, w, nth=0, edge="start"):
        """Time of the nth occurrence of word w in this line (fuzzy-normalized)."""
        target = norm(w)
        hits = [x for x in self.words if norm(x["w"]) == target]
        if not hits:
            hits = [x for x in self.words if target and target in norm(x["w"])]
        if not hits:
            raise KeyError(f"word {w!r} not in line {self.id}: {self.text!r}")
        return float(hits[min(nth, len(hits) - 1)][edge])

    def frac(self, f):
        """Time at fraction f (0..1) through the line."""
        return self.start + self.dur * f


class Timing:
    def __init__(self, path, offset=0.0):
        """offset (s): pre-roll before the voice (brand sting) — every line/word time and the duration shift by it."""
        with open(path) as fh:
            d = json.load(fh)
        if offset:
            d["duration"] = float(d["duration"]) + offset
            for ln in d["lines"]:
                ln["start"], ln["end"] = float(ln["start"]) + offset, float(ln["end"]) + offset
                for w in ln.get("words", []):
                    w["start"], w["end"] = float(w["start"]) + offset, float(w["end"]) + offset
        self.source = d.get("source", "?")
        self.duration = float(d["duration"])
        self.lines = [Line(x) for x in d["lines"]]
        self._by_id = {ln.id: ln for ln in self.lines}

    def __getitem__(self, line_id):
        return self._by_id[line_id]

    def line(self, line_id):
        return self._by_id[line_id]

    def word(self, line_id, w, nth=0, edge="start"):
        return self._by_id[line_id].word(w, nth, edge)

    def chapter_span(self, chapter):
        """(start, end) of all lines belonging to a chapter label."""
        ls = [ln for ln in self.lines if ln.chapter == chapter]
        if not ls:
            raise KeyError(chapter)
        return ls[0].start, ls[-1].end

    def after(self, line_id):
        """Start of the line after line_id (or end of timeline)."""
        i = self.lines.index(self._by_id[line_id])
        return self.lines[i + 1].start if i + 1 < len(self.lines) else self.duration


class Beat:
    """Music grid. offset = time of beat 0 in seconds (measure it from the track)."""

    def __init__(self, bpm=128, offset=0.0):
        self.bpm = bpm
        self.offset = offset
        self.spb = 60.0 / bpm

    def __call__(self, n):
        return self.offset + n * self.spb

    def snap(self, t, div=1):
        step = self.spb / div
        return self.offset + round((t - self.offset) / step) * step

    def next(self, t, div=1):
        import math
        step = self.spb / div
        return self.offset + math.ceil((t - self.offset) / step - 1e-6) * step
