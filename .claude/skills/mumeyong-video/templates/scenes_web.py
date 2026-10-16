"""HTML film video (WEB.md): the identity around videos/<slug>/film.html. Copy, set every REPLACE, and put the whole
picture in film.html — this file only places the opening logo, the film and the ending logo, and picks the sound.
"""
from engine import Video
from engine.components import brand_intro, standard_outro
from engine.web import film

PRE_ROLL = 2.05             # long brand sting (version 2): the voice starts under its wipe — film time includes it
TAIL = 3.0                  # the ending logo holds this long after the last word
FOLLOW = "L10"              # REPLACE: the last line ("Follow …") — the ending logo starts on it
ACCENT = (1.0, 0.29, 0.11, 1)   # REPLACE: the film's accent as RGBA 0–1 (the ending logo's teaser card)


def build(project):
    T = project.timing
    v = Video(duration=T[FOLLOW].end + TAIL, bpm=128)        # REPLACE bpm (inside the style's range): the film's
    v.hud = False                                              # FILM.beats grid = the score's beat
    v.music = dict(style="garage", key="D", mood="bright")    # REPLACE: lofi · marimba · ambient · garage · cinematic
    v.sfx_kit = "glass"                                        # REPLACE: glass · wood · soft · mech (or None)
    brand_intro(v, version=2)
    s_out = T[FOLLOW].start - 0.3
    film(v, project, end=s_out)                               # + every cue() the page registered
    standard_outro(v, T, s_out, v.duration, FOLLOW, ACCENT,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="“REPLACE”", sub="REPLACE"))
    v.cover_t = T["L01"].end                                  # REPLACE: the film frame that works as the cover
    return v
