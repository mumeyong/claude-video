"""Reusable on-screen components. Import what you need in scenes.py:

    from engine.components import Headline, kicker, appear, window, ChatTrack, ...
"""
from .headline import Headline, kicker
from .motion import appear, fade, typed, type_end, type_cues, stagger, count, fmt_id, wobble, bezier_partial
from .pill import chip, tag, word_pill, size_label, select_box, strike
from .chat import ChatTrack
from .widgets import stat, big_number, waveform, rec_bar, filmstrip, phone, comment, Cursor
from .recap import step_row, rule_box, connector, segments, follow_button, contact_pill
from . import window, icons
