"""SCRIPT.md → NASKAH.md: a clean read-aloud script for recording voice.wav.

Generated, never hand-edited — SCRIPT.md stays the single source of truth, so what you read is
exactly what align.py matches against and what the scenes are timed to.

SCRIPT.md extras understood here (stripped everywhere else):
    *kata*          vocal stress → **bold** in NASKAH.md
    [L05] ... //    '//' at the end = take a breath / short pause after this line
"""
import re

from .audio.align import WPS, parse_script

PAUSE_CHAPTER = "⏸ jeda ± 1 detik"


def _clean_words(text):
    return re.sub(r"[*/]", "", text).split()


def build_naskah(script_path, out_path, title=None):
    lines = parse_script(script_path, keep_marks=True)
    if title is None:
        for raw in open(script_path, encoding="utf-8"):
            if raw.startswith("# "):
                title = raw[2:].strip()
                break
    words = sum(len(_clean_words(ln["text"])) for ln in lines)
    secs = words / WPS
    out = [
        f"# NASKAH — {title or 'video'}",
        "",
        f"> {len(lines)} kalimat · {words} kata · ± {int(secs // 60)}:{int(secs % 60):02d} kalau dibaca ± 160 kata/menit",
        "> **Cara rekam:** baca dari atas sampai bawah **sekali jalan**. Salah? Diam 1 detik, ulangi kalimat itu aja.",
        "> **Tebal** = kasih tekanan. ⏸ = jeda ganti bab. Nomor kecil [Lxx] cuma buat referensi, nggak dibaca.",
        "> Generated dari SCRIPT.md — jangan edit file ini, edit SCRIPT.md lalu generate ulang.",
        "",
    ]
    chapter = None
    for ln in lines:
        if ln["chapter"] != chapter:
            if chapter is not None:
                out += ["", f"*{PAUSE_CHAPTER}*", ""]
            chapter = ln["chapter"]
            out += [f"## {chapter}", ""]
        text = ln["text"].rstrip()
        breath = text.endswith("//")
        text = text[:-2].rstrip() if breath else text
        text = re.sub(r"\*([^*]+)\*", r"**\1**", text)
        out.append(f"<sub>{ln['id']}</sub> {text}{'  ·  *(napas)*' if breath else ''}  ")
        out.append("")
    out += ["---", "", "Selesai. Simpan sebagai `audio/voice.wav` → jalanin `claude-video <slug>` (align otomatis)", ""]
    open(out_path, "w", encoding="utf-8").write("\n".join(out))
    print(f"✓ {out_path}  ({len(lines)} kalimat, {words} kata, ± {secs:.0f} s)")
    return out_path
