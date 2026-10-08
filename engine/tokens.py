"""Design tokens — the code mirror of .claude/skills/mumeyong-video/STYLE.md.

Every color, size and duration a scene uses must come from here.
Values were measured from the reference video (720x1280 source, scaled x1.5).
"""

# ── canvas ──────────────────────────────────────────────────────────────
W, H, FPS = 1080, 1920, 60

BRAND = "MUMEYONG"          # HUD (uppercase)
BRAND_NAME = "Mumeyong"     # outro wordmark
TAGLINE = "Follow, biar nggak cuma vibe coding."
CONTACT = {"site": "mumeyong.dev", "wa": ""}  # WhatsApp: not provided yet
SERIES = "TUTORIAL"
CHAT_PLACEHOLDER = "Tanya Claude Code..."


def hexc(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def hexs(color):
    """RGBA tuple → '#RRGGBB' (for Pango markup spans)."""
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in color[:3])


# ── color ───────────────────────────────────────────────────────────────
C = {
    "bg": hexc("#F2F3F6"),          # base canvas
    "bg_warm": hexc("#F6ECE8"),     # constant warm glow, bottom-right
    "ink": hexc("#0B0B0F"),         # headline black
    "ink2": hexc("#3A3F47"),        # kicker / body text
    "muted": hexc("#8A8F98"),       # HUD, placeholders, meta
    "faint": hexc("#C9CDD4"),       # future progress dots, dividers
    "line": hexc("#000000", 0.06),  # hairlines, card borders
    "card": hexc("#FFFFFF"),
    "accent": hexc("#1F5EFF"),      # THE blue: accent word, send button, links
    "accent_soft": hexc("#E3EBFF"),  # idle send button, blue tag bg
    "orange_pill": hexc("#EB6A4A"),  # "keyframe." style negative pill
    "ok": hexc("#16A34A"),
    "rec": hexc("#E5484D"),
    "wa": hexc("#25D366"),
    # dark section (recap / outro)
    "d_bg": hexc("#0C0C12"),
    "d_glow": hexc("#13265A"),
    "d_ink": hexc("#F5F6F8"),
    "d_muted": hexc("#7C8494"),
    "d_card": hexc("#161925"),
    "d_line": hexc("#FFFFFF", 0.08),
    "d_accent": hexc("#4F8BFF"),
    # brand mark (mumeyong.dev "mumei" emblem: ensō + blank vermilion hanko) — brand sting & outro mark only
    "brand_paper": hexc("#FAF9F5"),
    "brand_ink": hexc("#2B2C29"),
    "brand_seal": hexc("#C44834"),
    # code syntax
    "code_kw": hexc("#7C3AED"),
    "code_str": hexc("#0E9F6E"),
    "code_cmt": hexc("#9AA0AA"),
    "code_txt": hexc("#2A2F37"),
}

# Chapter identity: (dot color, background tint). Index = chapter number.
CHAPTER = [
    (hexc("#2364FF"), hexc("#EAEDFA")),  # 00 blue
    (hexc("#10A060"), hexc("#ECF3F2")),  # 01 green
    (hexc("#E8861A"), hexc("#F8F1EA")),  # 02 orange
    (hexc("#7558F0"), hexc("#EFEBFA")),  # 03 purple
    (hexc("#0E9AAB"), hexc("#EAF3F8")),  # 04 teal
    (hexc("#F03B4F"), hexc("#F6ECEF")),  # 05 red
    (hexc("#2364FF"), hexc("#EAEDFA")),  # 06 blue
    (hexc("#10A060"), hexc("#ECF3F2")),  # 07+ cycle
    (hexc("#E8861A"), hexc("#F8F1EA")),
]
INTRO_TINT = hexc("#EEEBF8")

# Chip dot colors (context chips above the chat input)
CHIP = {"green": hexc("#10A060"), "purple": hexc("#7558F0"),
        "blue": hexc("#2364FF"), "orange": hexc("#E8861A"), "red": hexc("#E5484D")}

# ── type ────────────────────────────────────────────────────────────────
# Pango font descriptions (family + weight). Fonts live in assets/fonts.
F = {
    "display": "Inter Display Bold",     # headlines
    "display_semi": "Inter Display SemiBold",
    "serif": "Instrument Serif Italic",  # italic emphasis word (_tiap_)
    "ui": "Inter Medium",
    "ui_reg": "Inter Regular",
    "ui_semi": "Inter SemiBold",
    "ui_bold": "Inter Bold",
    "mono": "JetBrains Mono Regular",
    "mono_med": "JetBrains Mono Medium",
    "mono_bold": "JetBrains Mono Bold",
}

T = {  # (size px, letter-spacing em, line-height x size)
    "headline": (96, -0.055, 0.98),
    "headline_lg": (128, -0.06, 0.95),   # single-word/number punches ("100%")
    "headline_dark": (78, -0.05, 1.0),   # recap/outro headlines
    "kicker": (24, 0.20, 1.0),           # "● 02 · NASKAH"
    "hud": (19, 0.18, 1.0),
    "card_title": (27, -0.01, 1.0),
    "card_meta": (19, 0.02, 1.0),
    "body_mono": (21, 0.0, 1.85),        # lines inside cards
    "chat": (30, -0.005, 1.25),
    "chip": (22, -0.005, 1.0),
    "tag": (19, 0.0, 1.0),
    "stat": (60, -0.04, 1.0),
    "label": (17, 0.06, 1.0),            # size-label pills, tiny mono
    "comment": (40, -0.02, 1.15),
    "mega": (210, -0.06, 0.9),           # hero numbers ("$14.000"), centered punch moments
    "giga": (300, -0.065, 0.9),          # one-word slams ("100%")
    "note": (40, 0.0, 1.05),             # serif italic hand-note annotations
}
SERIF_SCALE = 1.10  # serif italic sits optically smaller than Inter, scale it up

# ── layout (1080x1920) ──────────────────────────────────────────────────
L = {
    "hud_x": 60, "hud_top": 66, "hud_bottom": 1855, "hud_right": 1020,
    "dots_y": 100, "dot_r": 3.6, "dot_gap": 19,
    "col_x": 81,          # content column left
    "col_w": 848,         # content column width (right edge 929 keeps clear of TikTok buttons)
    "kicker_y": 290,      # kicker baseline-center
    "headline_y": 318,    # headline top
    "content_y": 520,     # first card top
    "content_bottom": 1330,
    "chips_y": 1338,      # chip row top
    "chat_y": 1400, "chat_h": 152,
    "radius_card": 22, "radius_chat": 32, "radius_pill": 999,
}

# ── motion (seconds) ────────────────────────────────────────────────────
M = {
    "word_in": 0.55, "word_stagger": 0.06, "word_blur": 18, "word_rise": 26,
    "out": 0.35, "out_blur": 14,
    "card_in": 0.6, "card_rise": 48, "card_scale": 0.965, "card_blur": 12,
    "type_cps": 34,            # typing speed, chars per second
    "chapter_fade": 0.6,       # background tint crossfade
    "beat_bpm": 128,
    # fx.py (opt-in upgrades, 2026-10-08)
    "settle": 0.7,             # spring settle duration (pops, camera stops)
    "land_dur": 0.35,          # squash-and-stretch after a landing
    "land_squash": 0.12,       # max squash (12% wider / shorter)
    "trail_n": 4,              # ghost-trail samples behind fast movers
    "trail_span": 0.05,        # seconds the trail reaches back
}

# ── shadow ──────────────────────────────────────────────────────────────
SHADOW = {
    "card": dict(blur=34, dy=14, alpha=0.075),
    "card_tight": dict(blur=8, dy=2, alpha=0.05),
    "chat": dict(blur=40, dy=16, alpha=0.09),
    "pill": dict(blur=22, dy=10, alpha=0.28),  # colored pills use their own color
}
