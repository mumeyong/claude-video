"""Google Maps tahu jalan macet dari mana? — HTML film (WEB.md): the identity around videos/maps-tahu-macet/film.html.
The whole picture lives in film.html; this file places the opening logo, the film and the ending logo, and the sound.
"""
from engine import Video
from engine.components import brand_intro, standard_outro
from engine.web import film

PRE_ROLL = 2.05             # long brand sting (version 2): the voice starts under its wipe — film time includes it
TAIL = 3.0                  # the ending logo holds this long after the last word
TEASER = "L16"              # "Kamu pernah disuruh Maps lewat gang aneh?" — the ending logo + comment card start here
FOLLOW = "L17"              # "Follow, biar nggak ketinggalan."
BRAKE_RED = (0.949, 0.263, 0.227, 1)   # #F2433A — the film's accent (ending logo teaser card)


def build(project):
    T = project.timing
    v = Video(duration=T[FOLLOW].end + TAIL, bpm=84)
    v.hud = False
    v.music = dict(style="lofi", key="F", mood="dreamy")
    v.sfx_kit = "wood"
    brand_intro(v, version=2)
    s_out = T[TEASER].start - 0.3
    film(v, project, end=s_out)
    standard_outro(v, T, s_out, v.duration, FOLLOW, BRAKE_RED,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="“Gang paling aneh?”",
                               sub="Yang pernah disuruh Maps"))
    v.cover_t = T.word("L02", "merah") + 0.9                   # red road + "99 HP" painted on the asphalt
    return v
