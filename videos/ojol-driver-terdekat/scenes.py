"""ojol-driver-terdekat — HTML film (WEB.md): the identity around film.html. The whole picture (one printed city map
sliced into sectors) lives in film.html; this file only places the opening logo, the film and the ending logo, and
picks the sound.
"""
from engine import Video
from engine.components import brand_intro, standard_outro
from engine.web import film

PRE_ROLL = 2.05             # long brand sting (version 2): the voice starts under its wipe — film time includes it
TAIL = 3.0                  # the ending logo holds this long after the last word
FOLLOW = "L17"              # the last line ("Follow …") — the ending logo starts on it
ACCENT = (0.294, 0.169, 1.0, 1)   # ultramarine #4B2BFF (the ending logo's teaser card)


def build(project):
    T = project.timing
    v = Video(duration=T[FOLLOW].end + TAIL, bpm=108)        # marimba range 100–116: FILM.beats grid
    v.hud = False
    v.music = dict(style="marimba", key="G", mood="bright")
    v.sfx_kit = "soft"
    brand_intro(v, version=2)
    s_out = T[FOLLOW].start - 0.3
    film(v, project, end=s_out)                               # + every cue() the page registered
    standard_outro(v, T, s_out, v.duration, FOLLOW, ACCENT,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="“Driver-mu muter jauh?”",
                               sub="ceritain di komentar"))
    v.cover_t = T["L02"].end                                  # "secepat itu?" over the whole city
    return v
