"""Measure the beat grid of a supplied song (from cheese `beats`) → videos/<slug>/beats.json.

    python -m engine beats <slug> [--phase 0-3]

HTML films read it as FILM.beats (beats = state changes, downbeats = big moments, hits = SFX). Without beats.json a
film gets the generated score's own grid (v.bpm). Needs librosa: in the venv, or fetched on the fly with `uv`.

Run as a script it prints the JSON for one file:  python engine/audio/beats.py song.wav [phase]
"""
import json
import subprocess
import sys
from pathlib import Path


def measure(path, phase=None):
    import warnings
    import librosa
    import numpy as np
    warnings.filterwarnings("ignore", category=UserWarning)
    y, sr = librosa.load(str(path), sr=None, mono=True)
    tempo, frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
    beats = librosa.frames_to_time(frames, sr=sr).round(3).tolist()
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    peaks = librosa.util.peak_pick(onset, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=10)
    if phase is None:
        # downbeats: the phase (0-3) whose beats carry the most low-band (kick/bass) energy — full-band energy tends
        # to lock onto snares on 2 and 4. Four-on-the-floor stays ambiguous → --phase N.
        low = librosa.onset.onset_strength(y=y, sr=sr, fmax=200, n_mels=32)
        strength = low[np.minimum(frames, len(low) - 1)] if len(frames) else np.array([])
        phase = int(np.argmax([strength[p::4].sum() for p in range(4)])) if len(strength) >= 4 else 0
    return {"bpm": round(float(np.atleast_1d(tempo)[0]), 2), "source": "librosa", "duration": round(len(y) / sr, 3),
            "beats": beats, "downbeats": beats[phase::4],
            "hits": librosa.frames_to_time(peaks, sr=sr).round(3).tolist()}


def write_beats(project, phase=None):
    music = project.music()
    if not music:
        sys.exit(f"no song: put it at videos/{project.slug}/audio/music.mp3 (or .wav/.m4a)")
    try:
        data = measure(music, phase)
    except ImportError:
        args = ["uv", "run", "-q", "--with", "librosa", "--with", "numpy", "python", "-I", __file__, str(music)]
        r = subprocess.run(args + ([str(phase)] if phase is not None else []), capture_output=True, text=True)
        if r.returncode:
            sys.exit("librosa missing — .venv/bin/pip install librosa  (or install uv)\n" + r.stderr[-400:])
        data = json.loads(r.stdout)
    out = project.dir / "beats.json"
    out.write_text(json.dumps(data, indent=1))
    print(f"✓ {out}  {data['bpm']} BPM · {len(data['beats'])} beats · "
          f"{len(data['hits'])} hits")
    return out


if __name__ == "__main__":
    print(json.dumps(measure(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None), indent=1))
