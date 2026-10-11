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
    # reel layer (opt-in, 2026-10-10, components/reel.py — brand teasers only, STYLE §6e): paper = brand_paper
    "reel_green": hexc("#608A70"),  # the reel's main color: iris, orbit satellite, highlighter, dotted lines
    "reel_ink": hexc("#22231F"),    # reel type, chips border, dark pills, pixel wipe
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

# Reel "six worlds" (mumeyong.dev site sections) — chip squares, card labels, verb-slam grounds. Reel layer only.
REEL_WORLDS = [hexc("#608A70"), hexc("#52D6CE"), hexc("#D6785C"),   # root · platform · security
               hexc("#8A96FF"), hexc("#D6AA48"), hexc("#B078C4")]   # cloud · automation · observability

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
    "radius_bento": 36,   # keynote bento tiles / floating sheets
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
    # kinetic.py (opt-in, 2026-10-08 — motion signature per video, STYLE §6d)
    "mask_in": 0.75,           # word rises from behind its baseline mask
    "track_in": 0.9,           # tracking-collapse line: letters arrive + spacing closes
    "track_spread": 0.32,      # extra tracking at the start (em)
    "dim_out": 0.6,            # exit: drain to grey, then fade
    "sheen_dur": 0.7,          # light band sweeping across a card (content swaps at its middle)
    "drift_zoom": 0.035,       # slow push over a whole scene (+3.5%)
    "drift_rot": 0.012,        # ± rotation over that push (radians, ~0.7°)
    "mblur_k": 0.006,          # px of blur per px/s above 300 px/s
    "mblur_max": 16,
    "curtain": 0.9,            # cold-open fade out of darkness
    # keynote.py (opt-in, 2026-10-08 — Apple / iOS feel)
    "bento_gap": 18, "bento_in": 0.9, "bento_stagger": 0.09,
    "turn_from": 0.9,          # product yaw before it turns to face the camera (radians, ~52°)
    "press_dip": 0.06,         # button press scale dip
    "sheet_dim": 0.18,         # backdrop dim behind a floating sheet
    "ink_stagger": 0.11,       # Headline reveal="ink": per-word ink-in
    "ink_in": 0.55,
    # reel.py (opt-in, 2026-10-10 — brand teasers, STYLE §6e)
    "reel_smear_in": 0.45,     # smear entrance: offset + horizontal stretch + blur 16 → 0
    "reel_smear_blur": 16,
    "reel_out": 0.4,           # reel exit: scale +30%, blur 18, fade
    "reel_out_blur": 18,
    "reel_gather": 1.35,       # dots gather onto the ensō (logo build)
    "reel_iris": 0.6,          # iris close / circle swell
    "reel_block": 72,          # pixel-wipe block size (15 × 27 on 1080 × 1920)
    "reel_block_sweep": 0.55,  # time for the wipe front to cross the frame
    "reel_block_hold": 0.34,   # how long each block stays ink before turning paper
    "reel_hl": 0.4,            # highlighter swipe
    "reel_chip_stagger": 0.11,
    "reel_count": 1.75,        # count-up inside a pill
    "reel_card_stagger": 0.16,
    "reel_slam": 0.2,          # verb slam whip-in
    "reel_type": 0.6,          # wordmark clip-type
}

# Spring personalities: (damping, frequency, settle seconds). PLAN.md picks one as the video's default.
SPRING = {
    "snappy": (0.62, 2.0, 0.55),   # UI, tags, words — quick, one small overshoot
    "heavy":  (0.80, 1.05, 0.95),  # big hero objects, lockups — slow, weighty, barely overshoots
    "floaty": (0.55, 1.8, 1.25),   # soft / playful worlds — ~12% overshoot, small objects only
    "silk":   (0.93, 0.9, 1.15),   # Apple keynote — long, smooth, no visible overshoot (morphs, sheets, heroes)
}

# ── Apple motion craft (STYLE §6f, 2026-10-11 — default for every new video) ──────────────────────
# Named cubic-bezier curves (ease.curve(name)). Entrances decelerate long, exits accelerate short.
EASE = {
    "apple":        (0.28, 0.11, 0.32, 1.0),   # apple.com standard transition
    "apple_out":    (0.16, 1.0, 0.3, 1.0),     # entrances: decisive start, long glide to rest
    "apple_in":     (0.4, 0.0, 0.9, 0.55),     # exits: quiet start, leaves quickly
    "apple_in_out": (0.65, 0.0, 0.35, 1.0),    # push / pan between two focus points
    "apple_dolly":  (0.42, 0.0, 0.58, 1.0),    # slow camera dolly over a hold
}

# SwiftUI springs by real time: (response s, dampingFraction). ease.ios_spring(dt, *IOS[name]).
IOS = {
    "smooth":  (0.5, 1.0),    # iOS .smooth — no overshoot (default for text + cards)
    "snappy":  (0.5, 0.85),   # iOS .snappy — ~1% overshoot (UI pops, chips, buttons)
    "bouncy":  (0.5, 0.7),    # iOS .bouncy — small objects only, max once per chapter
    "default": (0.55, 0.825), # iOS .spring() default
    "hero":    (0.85, 1.0),   # big hero objects / full-bleed shrink — heavy, no overshoot
}

M.update({
    "rise_dy": 34,            # fade-up travel (px) for text/cards; distance-scaled for bigger objects
    "rise_scale": 0.985,      # fade-up start scale
    "rise_line_stagger": 0.08,   # Headline reveal="rise": per line
    "op_lead": 0.45,          # opacity is done at 45 % of the move — opacity leads, position follows
    "wipe_in": 0.95,          # soft-edged mask wipe (titles, images)
    "wipe_soft": 0.22,        # feather of the wipe edge (fraction of the box)
    "quiet_out": 0.32,        # exit: fade + scale 0.98, apple_in — exits are faster and quieter than entrances
    "quiet_scale": 0.98,
    "swap_dur": 0.85,         # depth_swap: old goes back, new comes forward
    "swap_back": 0.92, "swap_front": 1.06,
    "focus_blur": 9,          # focus_pull: background depth-of-field blur (px) — depth, never a glass panel
    "focus_scale": 0.965, "focus_dim": 0.35,
    "dolly_zoom": 0.03,       # camera dolly over a hold (+3 %)
    "follow_gap": 0.12,       # follower starts this long after the leader
    "follow_amp": 0.5,        # follower moves ≤ half the leader's distance
    "hold_min": 0.8,          # stillness after an arrival before the next move
})

# ── material / look (STYLE §6g, 2026-10-12 — components/material.py) ──────────────────────────────
# The look = how objects are SHADED. "flat" = plain fills (before 2026-10-12). Volume comes from light, never extrusion.
LOOK = {
    "lit": dict(                 # soft studio light from the top-left (Apple product film)
        hi=0.30, lo=0.30,        # body gradient: lighten the lit side / darken the far side
        ao=0.24,                 # ambient occlusion at the edges (volume)
        rim=0.55, rim_w=3.0,     # bright top edge = light catching the material
        sheen=0.10,              # soft diagonal reflection band
        shadow_blur=46, shadow_dy=30, shadow_alpha=0.16,   # cast shadow at 600 px object size (scales with size)
        contact_alpha=0.20,      # tight dark shadow where the object touches its surface
        spill=0.30,              # light of a glowing part falling on what's around it
        grain=0.06, vignette=0.12,
    ),
    "paper": dict(               # cut paper, layers lying on each other
        stack_dy=9, stack_alpha=0.17,                      # short hard shadow of the layer below
        soft_blur=20, soft_dy=14, soft_alpha=0.10,
        fibre=0.30,              # paper fibre texture (soft light)
        edge=0.45,               # cut edge catching light (thin top highlight)
        tilt=0.012,              # hand-placed: each part a touch off-square (radians)
        grain=0.05, vignette=0.06,
    ),
}
C.update({
    "paper_ground": hexc("#EEE8DC"),   # paper look: the ground the cut-outs lie on
    "studio_floor": hexc("#DDE2E9"),   # lit look: floor of the studio sweep (tinted by the video color)
})

# ── shadow ──────────────────────────────────────────────────────────────
SHADOW = {
    "card": dict(blur=34, dy=14, alpha=0.075),
    "card_tight": dict(blur=8, dy=2, alpha=0.05),
    "chat": dict(blur=40, dy=16, alpha=0.09),
    "pill": dict(blur=22, dy=10, alpha=0.28),  # colored pills use their own color
}
