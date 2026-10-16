"""HTML films (the grak / cheese look, refs.pdf) inside a MUMEYONG video.

videos/<slug>/film.html is painted by headless Chrome (web/run.mjs) and laid UNDER the identity: the voice mix, the
opening logo (brand_intro) and the ending logo (standard_outro) stay this engine's. scenes.py stays tiny:

    v = Video(duration=T["L12"].end + TAIL, bpm=118); v.hud = False
    brand_intro(v, version=2)
    film(v, project, end=s_outro)                    # frame t of film.html, from 0 until the outro
    standard_outro(v, T, s_outro, v.duration, "L12", COLOR)

Frames are cached in out/.web/ and only rendered for the times something asks for: a render (every frame at
fps × subframes), critique / sheet / stills / cover (just those moments). Each cache carries a hash of the page,
its data and its assets, so an edit re-renders; `--fix A,B` re-renders only seconds A–B and keeps the rest.
"""
import hashlib
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys

from . import tokens as tk
from .ease import prog
from .project import ROOT

WEB = ROOT / "web"
SUB = {"final": 4, "preview": 1}          # browser subframes per frame (motion blur inside the film)
ALIAS = {"thump": "thud", "swoosh": "whoosh", "ding": "chime", "type": "key"}    # grak / cheese cue names
SAFE = dict(x0=tk.L["col_x"], x1=tk.L["col_x"] + tk.L["col_w"], y0=240, y1=1560)  # = lint.dry_check
UI = dict(top=220, bottom=440, left=90, right=190)                                 # platform UI, px from each edge
BANNED = [
    (r"Math\.random\s*\(", "Math.random — use rng(seed) from /web/lib/motion.js"),
    (r"Date\.now\s*\(|new Date\s*\(|performance\.now\s*\(", "wall-clock time — everything comes from t"),
    (r"setTimeout\s*\(|setInterval\s*\(|requestAnimationFrame\s*\(", "timers — seek(t) paints the frame"),
    (r"\btransition\s*:|@keyframes\b|\banimation\s*:", "CSS transition/animation — not seekable"),
    (r"<video\b|\.play\s*\(", "media playback — not seekable; use stills"),
]


def _node():
    for p in (shutil.which("node"), pathlib.Path.home() / ".local/opt/node22/bin/node"):
        if p and os.path.exists(p):
            return str(p)
    sys.exit("node (≥ 18) not found — HTML films need it")


def run(*args, capture=False):
    """node web/run.mjs <args> from the repo root."""
    if not (WEB / "node_modules" / "playwright").exists():
        sys.exit("web/node_modules missing — run once: (cd web && npm install)")
    return subprocess.run([_node(), str(WEB / "run.mjs"), *map(str, args)], cwd=ROOT, text=True,
                          capture_output=capture)


def _times(ts):
    return ",".join(f"{t:.4f}" for t in ts)


class Film:
    """One film.html laid over [start, end) of a video; draws the cached frame for t (nothing if not rendered)."""

    def __init__(self, v, project, page, start, end, fade_out):
        self.video, self.project = v, project
        self.page = project.dir / page
        if not self.page.exists():
            sys.exit(f"{self.page.relative_to(ROOT)} missing")
        self.url = self.page.relative_to(ROOT).as_posix()
        self.start, self.end, self.fade_out = start, end, fade_out
        self.dir = project.out / ".web"
        self._img, self._dirs = (None, None), None
        self.write_data()
        self.stamp = self._stamp()

    # ── data the page reads (out/.web/film.json) + the hash that keys every cache ───────────────────────
    def _beats(self):
        f = self.project.dir / "beats.json"
        if f.exists():                                   # measured from audio/music.* (python -m engine beats)
            return json.loads(f.read_text())
        v, step = self.video, 60.0 / self.video.bpm
        bs = [round(v.beat_offset + i * step, 4) for i in range(int((v.duration - v.beat_offset) / step) + 1)]
        return {"bpm": v.bpm, "source": "grid", "beats": bs, "downbeats": bs[::4]}

    def _stress(self):
        """{line id: {normalized word}} from the *kata* marks in SCRIPT.md — the words a visual lands on."""
        from .timing import norm
        f, out = self.project.dir / "SCRIPT.md", {}
        for m in re.finditer(r"^\[(L\d+)\](.*)$", f.read_text(encoding="utf-8") if f.exists() else "", re.M):
            out[m.group(1)] = {norm(w) for ph in re.findall(r"\*([^*]+)\*", m.group(2)) for w in ph.split()} - {""}
        return out

    def write_data(self):
        from .timing import norm
        T, stress = self.project.timing, self._stress()
        lines = [dict(id=ln.id, chapter=ln.chapter, text=ln.text, start=ln.start, end=ln.end,
                      words=[dict(w, stress=norm(w["w"]) in stress.get(ln.id, ())) for w in ln.words
                             if norm(w["w"])])                       # no breath marks (//) on screen
                 for ln in T.lines]
        data = dict(slug=self.project.slug, W=tk.W, H=tk.H, fps=tk.FPS, duration=self.video.duration,
                    start=self.start, end=self.end, pre_roll=self.project.pre_roll, lines=lines,
                    beats=self._beats(), safe=SAFE, ui=UI)
        txt = json.dumps(data, ensure_ascii=False, indent=1)
        f = self.dir / "film.json"
        if not f.exists() or f.read_text(encoding="utf-8") != txt:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(txt, encoding="utf-8")

    def _stamp(self):
        h = hashlib.sha1()
        for f in sorted(WEB.glob("lib/*")) + [WEB / "run.mjs", WEB / "package.json", self.page, self.dir / "film.json"]:
            h.update(f.name.encode() + f.read_bytes())
        for f in sorted(self.project.dir.rglob("*")):    # images/data the page may load (not out/, audio/, docs)
            rel = f.relative_to(self.project.dir).parts
            if f.is_file() and rel[0] not in ("out", "audio", "refs") and f.suffix not in (".md", ".py") \
                    and f.name not in ("timing.json", "REVIEW"):
                st = f.stat()
                h.update(f"{'/'.join(rel)}:{st.st_size}:{st.st_mtime_ns}".encode())
        return h.hexdigest()[:16]

    def _cache(self, name, keep=False):
        """out/.web/<name>/ for the current stamp (wiped when the stamp changed, unless keep)."""
        d = self.dir / name
        mark = d / "STAMP"
        if d.exists() and not keep and (not mark.exists() or mark.read_text() != self.stamp):
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
        mark.write_text(self.stamp)
        self._dirs = None
        return d

    # ── SFX the page computed from its own timings (window.CUES) ──────────────────────────────────────
    def cues(self):
        f = self.dir / "cues.json"
        data = json.loads(f.read_text()) if f.exists() else {}
        if data.get("stamp") != self.stamp:
            r = run("cues", "--page", self.url, capture=True)
            try:
                data = json.loads(r.stdout.strip().splitlines()[-1])
            except (ValueError, IndexError):
                data = {"cues": [], "errors": [(r.stderr or "no output").strip()[-400:]]}
            data["stamp"] = self.stamp
            f.write_text(json.dumps(data, ensure_ascii=False))
        for e in data.get("errors", []):
            print(f"  ! film.html: {e}")
        return [(ALIAS.get(c["name"], c["name"]), float(c["t"]), float(c.get("gain", 1))) for c in data["cues"]]

    # ── frames ──────────────────────────────────────────────────────────────────────────────────────
    def _frame_dirs(self):
        if self._dirs is None:
            ds = [d for d in self.dir.glob("f*x*") if (d / "STAMP").exists() and (d / "STAMP").read_text() == self.stamp]
            self._dirs = sorted(((int(d.name[1:].split("x")[0]), d) for d in ds), reverse=True)
            at = self.dir / "at"
            self._at = at if (at / "STAMP").exists() and (at / "STAMP").read_text() == self.stamp else None
        return self._dirs

    def frame_path(self, t):
        for fps, d in self._frame_dirs():
            p = d / f"{int(round(t * fps)):06d}.png"
            if p.exists():
                return p
        p = self._at / f"{t:.4f}.png" if self._at else None
        return p if p and p.exists() else None

    def draw(self, c, t):
        path = self.frame_path(t)
        if path is None:
            return
        if self._img[0] != path:
            import cairo
            self._img = (path, cairo.ImageSurface.create_from_png(str(path)))
        a = 1 - prog(t, self.end - self.fade_out, self.fade_out) if self.fade_out else 1.0
        c.ctx.set_source_surface(self._img[1], 0, 0)
        c.ctx.paint_with_alpha(a)

    def prepare_times(self, times):
        """Stills at exact times (critique, sheet, stills, cover) — seconds, no encode."""
        want = sorted({round(t, 4) for t in times if self.start <= t < self.end})
        d = self._cache("at")
        missing = [t for t in want if self.frame_path(t) is None]
        if missing:
            print(f"  web: {len(missing)} still(s) from {self.page.name}")
            if run("at", "--page", self.url, "--times", _times(missing), "--out", d).returncode:
                print("  ! film.html had page errors (see above)")

    def prepare_frames(self, fps, sub, f0, f1, fix=None):
        """Every frame in [f0, f1) at fps with `sub` browser subframes. fix=(a, b): re-render only seconds a–b and
        keep the other cached frames (even from an older version of the page)."""
        d = self._cache(f"f{fps}x{sub}", keep=fix is not None)
        if fix:
            for f in range(int(fix[0] * fps), int(math.ceil(fix[1] * fps))):
                (d / f"{f:06d}.png").unlink(missing_ok=True)
        fa, fb = max(f0, int(math.ceil(self.start * fps))), min(f1, int(math.ceil(self.end * fps)))
        have = {int(p.stem) for p in d.glob("[0-9]*.png")}
        runs, a = [], None
        for f in range(fa, fb + 1):
            gap = f < fb and f not in have
            if gap and a is None:
                a = f
            elif not gap and a is not None:
                runs.append((a, f))
                a = None
        for a, b in runs:
            print(f"  web: {self.page.name} frames {a}–{b - 1} @ {fps} fps" + (f", {sub} subframes" if sub > 1 else ""))
            if run("frames", "--page", self.url, "--fps", fps, "--sub", sub, "--from", a, "--to", b,
                   "--dur", self.video.duration, "--out", d).returncode:
                sys.exit("web frames failed — send this output to Claude")
        self._dirs = None

    # ── check --dry: page errors, determinism, banned patterns, cue names ─────────────────────────────
    def check(self):
        from .audio.sfx import SYNTH
        bad = 0
        print(f"{self.project.slug}: film check · {self.page.name} {self.start:.2f}–{self.end:.2f}s")
        for f in [self.page, *self.project.dir.glob("*.js")]:
            for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if re.match(r"\s*(//|\*|<!--)", ln):
                    continue
                for pat, why in BANNED:
                    if re.search(pat, ln):
                        bad += 1
                        print(f"  ✗ {f.name}:{i}  {why}")
        ts = [self.start + 0.5 * i for i in range(int((self.end - self.start) / 0.5))]
        r = run("check", "--page", self.url, "--times", _times(ts), capture=True)
        try:
            res = json.loads(r.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            res = {"errors": [(r.stderr or "page did not load").strip()[-600:]], "deterministic": True}
        for e in res["errors"]:
            bad += 1
            print(f"  ✗ ERROR  {e}")
        if not res["deterministic"]:
            bad += 1
            print(f"  ✗ frame {res['probe']:.2f}s differs between two seeks — state carried between frames, "
                  "wall-clock or randomness")
        if res.get("overflow"):
            print("  ! page is larger than 1080×1920 (scrollbars) — keep everything inside the stage")
        known = set(SYNTH) | {p.stem for p in (ROOT / "assets" / "sfx").glob("*.wav")}
        for name in sorted({n for n, _, _ in self.cues()} - known):
            bad += 1
            print(f"  ✗ cue '{name}' is not an SFX — use one of {', '.join(sorted(known))}")
        print(f"  {len(ts)} seeks · " + ("ok — no problems" if not bad else f"{bad} problem(s)"))
        return 1 if bad else 0


def film(v, project, start=0.0, end=None, page="film.html", fade_out=0.35, z=0):
    """Lay videos/<slug>/<page> over [start, end) of v (end default: the video's end) and add the SFX cues the page
    registered with cue(). The page fades out over fade_out s before end (into the ending logo). Returns the Film."""
    end = v.duration if end is None else end
    f = Film(v, project, page, start, end, fade_out)
    for name, t, gain in f.cues():
        v.sfx(name, t, gain)
    v.add(start, end, f.draw, z=z, bleed=True)
    v.web = f
    return f


def prepare(video, times):
    """Before drawing frames at `times` outside a render (sheet, stills, cover): make sure the film has them."""
    f = getattr(video, "web", None)
    if f is not None:
        f.prepare_times(times)
