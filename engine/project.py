"""Locate and build a video project: videos/<slug>/{SCRIPT.md, timing.json, scenes.py, audio/, assets/}."""
import importlib.util
import pathlib
import sys

from .timing import Timing

ROOT = pathlib.Path(__file__).resolve().parent.parent


class Project:
    def __init__(self, slug):
        self.slug = slug
        self.dir = ROOT / "videos" / slug
        if not self.dir.is_dir():
            sys.exit(f"no such video: {self.dir}")
        self.out = self.dir / "out"
        self.audio = self.dir / "audio"
        self.assets = self.dir / "assets"
        self.timing_path = self.dir / "timing.json"
        self._timing = None

    @property
    def timing(self):
        if self._timing is None:
            if not self.timing_path.exists():
                sys.exit(f"{self.timing_path} missing — run: python -m engine estimate {self.slug}  "
                         f"(or align, once audio/voice.wav exists)")
            self._timing = Timing(self.timing_path)
        return self._timing

    def asset(self, name):
        p = self.assets / name
        if not p.exists():
            raise FileNotFoundError(p)
        return p

    def voice(self):
        p = self.audio / "voice.wav"
        return p if p.exists() else None

    def music(self):
        for ext in ("wav", "mp3", "m4a", "flac", "ogg", "aac"):
            p = self.audio / f"music.{ext}"
            if p.exists():
                return p
        return None

    def build(self):
        """Import scenes.py and call build(project) → Video."""
        path = self.dir / "scenes.py"
        if not path.exists():
            sys.exit(f"videos/{self.slug}/scenes.py belum ada — lanjutkan di Claude Code: \"kerjain video {self.slug}\"")
        spec = importlib.util.spec_from_file_location(f"video_{self.slug}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.build(self)
