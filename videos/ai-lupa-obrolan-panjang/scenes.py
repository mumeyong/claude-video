"""Kenapa AI lupa isi obrolan yang panjang? — chat on a phone → papan tulis kelas (PLAN.md, v2 2026-10-13).

v2 (user feedback: the chat part was repetitive + wanted Apple-style type): the conversation is a REAL chat UI
(engine/components/obrolan.py, iOS Messages look, Inter only). INTRO: your first message, an hour of chat glides
past, the AI asks your name. 00: the phone steps aside, an "AI" card appears — every send flies the WHOLE thread
over to it (5 messages, then 7) and after the reply the card is empty again (stateless). 01 on: the whiteboard is
the metaphor for the context window (clean Inter rows now, no handwriting): it fills, the eraser wipes the top row
where your name was; recap: summary note, board wiped on purpose. Look: classic + Apple craft · paper-big.
v1 (whiteboard-only) is kept in out/scenes_v1_papan.py.
"""
import math

from engine import Video, tokens as tk
from engine.ease import clamp, lerp, prog, track, curve, glide
from engine.video import draw_background
from engine.components import (kicker, fade, pop_tag, brand_intro, standard_outro, cover, Rig, arrive, follow,
                               dolly, cut, heads, draw_heads, mark, draw_on, pts_rrect, rack_cut,
                               papan_tulis, papan_geo, penghapus, memori, chat_phone, material as mat)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW, MID = L["col_x"], L["col_w"], tk.W / 2
PRE_ROLL = 2.05
LEAD = 0.5
OUT = M["quiet_out"]
TAIL = 3.0
CH = ["INTRO", "00 · BACA ULANG", "01 · CONTEXT WINDOW", "02 · DIHAPUS", "RECAP", "OUTRO"]
LOOK = "paper"
COL = tk.CHAPTER[2][0]              # signature orange: AI avatar, read outline, board ink, eraser, memory cells
ROW_FONT = F["ui"]                  # board rows: Inter (Apple-style), no handwriting
BW, BH = CW, 800                    # the board fills the column
BCY = 600 + BH / 2                  # board centre (screen y) → board top at y 600
PW, PH = 620, 1000                  # phone (drawn around 0, 0 inside its Rig)
PCY = 552 + PH / 2                  # phone centre in INTRO
PS2 = 0.76                          # phone scale in 00 (steps aside for the AI card)
PX2 = X + PW * PS2 / 2              # phone centre x in 00
CARD = (X + PW * PS2 + 34, 690, CW - PW * PS2 - 34, 640)   # the AI card in 00 (screen)

KAMU, AI, TYPING, STAMP = "kamu", "ai", "typing", "stamp"
INTRO_ROWS = [
    ("Halo, aku Mumei.", KAMU), ("Halo Mumei! Mau dibantu apa?", AI), ("Bantu rencanain liburan ke Bali.", KAMU),
    ("Siap! Berapa hari?", AI), ("4 hari, budget hemat.", KAMU), ("Hari 1: Ubud, sawah, kopi.", AI),
    ("oke", KAMU), ("Hari 2: pantai Sanur.", AI), ("Hotelnya ganti dong.", KAMU), ("Ini 3 pilihan hotel.", AI),
    ("Yang paling murah?", KAMU), ("Yang dekat Kuta.", AI), ("oke, booking ya", KAMU), ("Siap! Nama kamu siapa?", AI),
]
# the story (00 → recap): the same chat from its first message; '|' = token cuts shown on the board in 01
STORY_ROWS = [
    ("Halo, aku Mumei.", KAMU), ("Halo Mumei! Mau dibantu apa?", AI),
    ("Bantu |rencan|ain |liburan |ke |Bali.", KAMU), ("Siap! Berapa hari?", AI), ("4 hari, budget hemat.", KAMU),
    ("Hari 1: Ubud, sawah, kopi.", AI), ("oke", KAMU), ("Hari 2: pantai Sanur.", AI), ("Hotelnya ganti dong.", KAMU),
]
ON_BOARD = 7                        # rows 0-6 are on the board when it appears (the chat so far)


def _w(T, lid, word, frac, nth=0):
    """Time of a word, falling back to a fraction of the line (estimate timings normalise some words)."""
    try:
        return T.word(lid, word, nth)
    except Exception:
        return T[lid].frac(frac)


class Cue:
    """Every time the picture reacts to, computed once from the voice — read this, not the draw code, to retime."""

    def __init__(self, T, b):
        self.b = b
        # INTRO — the chat
        self.t_in = T["L01"].start - 0.15                                # phone arrives
        self.m0 = T["L01"].start + 0.15                                  # "Halo, aku Mumei."
        self.m1 = _w(T, "L01", "bilang", 0.3)                            # AI greets back
        self.mark = arrive(_w(T, "L01", "namaku", 0.4), "snappy")        # circle round your name
        self.lapse = _w(T, "L01", "satu", 0.5)                           # one hour glides past
        self.lapse_step = 0.1
        self.typing0 = self.lapse + 11 * self.lapse_step + 0.05
        self.ask = _w(T, "L01", "nama", 0.85) - 0.2                      # "Siap! Nama kamu siapa?"
        self.forget = _w(T, "L02", "punya", 0.7) - 0.1                   # no memory: the rest of the thread dims
        # 00 — the phone steps aside, the AI card
        self.rack = b[1] + 0.25                                          # rewind to the chat's first messages
        self.aside = b[1] + 0.35
        self.card = arrive(_w(T, "L03", "obrolan", 0.4), "smooth")        # the AI card: empty
        self.type1 = _w(T, "L04", "tiap", 0.05)                          # you type …
        self.send1 = _w(T, "L04", "kirim", 0.2)                          # … and send
        self.stream1 = arrive(_w(T, "L04", "seluruh", 0.6), "smooth")    # the whole thread flies over
        self.typing1 = self.stream1 + 5 * 0.07 + 0.55
        self.reply1 = _w(T, "L04", "pertama", 0.95) - 0.1
        self.clear1 = self.reply1 + 0.55                                 # the card forgets
        self.type2 = _w(T, "L05", "ngetik", 0.15) - 0.05
        self.send2 = _w(T, "L05", "oke", 0.35) + 0.25
        self.stream2 = arrive(_w(T, "L05", "semuanya", 0.85), "smooth")
        # 01 — the board
        self.swap = b[2] + 0.05                                          # phone recedes, board comes forward
        self.rows = b[2] + 0.35                                          # the chat so far is written on it
        self.scan = arrive(_w(T, "L06", "baca", 0.6), "smooth")          # what is read = what must fit
        self.frame = arrive(_w(T, "L06", "muat", 0.75), "smooth")        # the board edge is traced = the limit
        self.label = arrive(_w(T, "L07", "context", 0.3), "snappy")
        self.tok = arrive(_w(T, "L07", "token", 0.8), "smooth")
        self.grow = arrive(_w(T, "L08", "gede", 0.25), "hero")
        self.mem = arrive(_w(T, "L08", "gpu", 0.55), "smooth")
        self.mahal = _w(T, "L08", "mahal", 0.95)
        self.shrink = b[3] + 0.1
        # 02 — erased
        self.w7 = _w(T, "L09", "penuh", 0.8) - 0.25                      # the board is full
        self.lift = arrive(_w(T, "L10", "baru", 0.25), "smooth")         # eraser lifts off the tray
        self.wipe = _w(T, "L10", "dihapus", 0.7) - 0.15                  # the top row goes
        self.scroll1 = self.wipe + 0.75
        self.w8 = self.scroll1 + 0.45
        self.name = arrive(_w(T, "L11", "namamu", 0.2), "snappy")       # "namamu" is on the eraser
        # recap
        self.sum = arrive(_w(T, "L12", "rangkum", 0.35), "smooth")       # summary note
        self.clean = _w(T, "L12", "baru", 0.85) - 0.2                    # the board is wiped on purpose
        self.settle = self.clean + 1.35                                  # the note moves onto the clean board
        self.home = T["L13"].start + 0.6                                 # eraser back on the tray


# ── the phone (INTRO + 00) ──────────────────────────────────────────────────────────────────────────────────────────
def _typed(text, t, t0, dur):
    """Draft text typed between t0 and t0 + dur (chars appear evenly)."""
    if t < t0:
        return ""
    return text[:int(len(text) * clamp((t - t0) / dur) + 0.999)]


def _intro_msgs(t, Q):
    dim = clamp(prog(t, Q.forget, 0.5))
    msgs = [dict(text=INTRO_ROWS[0][0], who=KAMU, t_in=Q.m0), dict(text=INTRO_ROWS[1][0], who=AI, t_in=Q.m1),
            dict(text="1 jam kemudian", who=STAMP, t_in=Q.lapse)]
    for i in range(2, 13):
        msgs.append(dict(text=INTRO_ROWS[i][0], who=INTRO_ROWS[i][1], t_in=Q.lapse + (i - 1) * Q.lapse_step))
    msgs.append(dict(text=None, who=TYPING, t_in=Q.typing0, t_out=Q.ask))
    msgs.append(dict(text=INTRO_ROWS[13][0], who=AI, t_in=Q.ask))
    for m in msgs[:-1]:
        m["dim"] = dim
    return msgs


def _story_msgs(t, Q):
    msgs = [dict(text=STORY_ROWS[i][0].replace("|", ""), who=STORY_ROWS[i][1], t_in=None) for i in range(4)]
    msgs += [dict(text=STORY_ROWS[4][0], who=KAMU, t_in=Q.send1 + 0.08),
             dict(text=None, who=TYPING, t_in=Q.typing1, t_out=Q.reply1),
             dict(text=STORY_ROWS[5][0], who=AI, t_in=Q.reply1),
             dict(text=STORY_ROWS[6][0], who=KAMU, t_in=Q.send2 + 0.08)]
    for ts, n in ((Q.stream1, 5), (Q.stream2, 7)):          # outline = "this one is sent again"
        live = [m for m in msgs if m["who"] != TYPING]
        for i, m in enumerate(live[:n]):
            t0 = ts + i * 0.07
            m["hl"] = max(m.get("hl", 0.0), clamp(prog(t, t0, 0.12)) * (1 - prog(t, t0 + 0.45, 0.35)))
    return msgs


def _draft(t, Q):
    if Q.type1 <= t < Q.send1:
        return _typed(STORY_ROWS[4][0], t, Q.type1, Q.send1 - Q.type1 - 0.15), Q.send1
    if Q.type2 <= t < Q.send2:
        return _typed("oke", t, Q.type2, 0.3), Q.send2
    return "", (Q.send1 if t < Q.type2 else Q.send2)


def phone_rig(Q):
    rig = Rig(x=MID, y=PCY + 60, s=0.96, a=0.0)
    rig.to(Q.t_in, preset="silk", y=PCY, s=1.0, a=1.0)                      # rises into place
    rig.to(Q.aside, preset="silk", x=PX2, y=CARD[1] + CARD[3] / 2, s=PS2)  # steps aside for the AI card
    rig.to(Q.swap, dur=0.45, preset="silk", s=PS2 * 0.9, a=0.0)            # recedes fast as the board comes forward
    return rig


def phone(v, T, Q, rig):
    b = Q.b
    box = (-PW / 2, -PH / 2, PW, PH)
    held = {}

    def intro_phone(c, t):
        g = chat_phone(c, t, *box, _intro_msgs(t, Q), scroll_preset="snappy")
        held["g"] = g
        x0, y0, w0, h0 = g["boxes"][0] or (0, 0, 0, 0)
        mark(c, t, Q.mark, "circle", (x0 - 14, y0 - 10, w0 + 28, h0 + 20), COL, width=5, t_out=Q.lapse, seed=3)

    def story_phone(c, t):
        draft, send = _draft(t, Q)
        held["g"] = chat_phone(c, t, *box, _story_msgs(t, Q), draft=draft, caret=bool(draft), send=send)

    def draw(c, t):
        with rig.place(c, t) as st:
            held["st"] = st
            if t < Q.rack + 0.5:
                rack_cut(c, t, Q.rack, (box[0] - 30, box[1] - 30, box[2] + 60, box[3] + 60),
                         lambda c: intro_phone(c, t), lambda c: story_phone(c, t))
            else:
                story_phone(c, t)
        if t >= Q.card - 0.1:
            ai_card(c, t, Q, held)
    v.add(Q.t_in, b[2] + 1.2, draw, z=10, bleed=True)
    v.sfx("whoosh", Q.t_in, 0.45)


def ai_card(c, t, Q, held):
    """The AI's side: empty until the whole thread arrives, read, answered — then empty again."""
    x, y, w, h = CARD
    op = clamp(prog(t, Q.card, 0.35)) * (1 - clamp(prog(t, Q.swap, 0.3)))
    if op <= 0.002:
        return
    rise_ = (1 - glide(prog(t, Q.card, 0.6))) * 30
    streams = ((Q.stream1, 5, Q.clear1), (Q.stream2, 7, Q.swap))
    with c.group(op), c.at(0, rise_):
        c.card(x, y, w, h, r=L["radius_bento"])
        c.circle(x + 52, y + 62, 24, COL)
        c.text(x + 52, y + 71, "AI", F["ui_bold"], 20, C["card"], align="c")
        c.text(x + 90, y + 72, "Model AI", F["ui_semi"], 30, C["ink"])
        c.line(x + 28, y + 112, x + w - 28, y + 112, C["faint"], 1.5)
        n_now, gone = 0, 1.0
        for ts, n, clear in streams:
            if t >= ts:
                n_now, gone = n, clamp(prog(t, clear, 0.35))
        empty = 1.0 if n_now == 0 else gone
        c.text(x + w / 2, y + h / 2 + 10, "ingatan: kosong", F["ui_reg"], 28, C["muted"], empty * 0.9, align="c")
        got = sum(1 for i in range(n_now) if t >= _stream_t(Q, n_now) + i * 0.07 + 0.5) if n_now else 0
        if got and gone < 1:
            c.text(x + 28, y + h - 40, f"dibaca ulang: {got} pesan", F["ui_semi"], 26, COL, 1 - gone)
    _minis(c, t, Q, held, streams, rise_)


def _stream_t(Q, n):
    return Q.stream1 if n == 5 else Q.stream2


def _minis(c, t, Q, held, streams, dy):
    """Every message flies from its bubble on the phone to a row in the AI card (cause → reaction, same frame)."""
    g, st = held.get("g"), held.get("st")
    if not g or not st:
        return
    x, y, w, h = CARD
    for ts, n, clear in streams:
        if t < ts or t > clear + 0.4:
            continue
        fade_ = 1 - clamp(prog(t, clear, 0.35))
        pairs = [(bx, m["who"]) for bx, m in zip(g["boxes"], _story_msgs(t, Q)) if m["who"] != TYPING][:n]
        for i, (bx, who) in enumerate(pairs):
            t0 = ts + i * 0.07
            p = glide(prog(t, t0, 0.5))
            if p <= 0 or bx is None:
                continue
            sx = st["x"] + st["s"] * (bx[0] + bx[2] / 2)
            sy = st["y"] + st["s"] * (bx[1] + bx[3] / 2)
            ex = x + 28 + (w - 56) / 2
            ey = y + 140 + i * 44 + 14 + dy
            px, py = lerp(sx, ex, p), lerp(sy, ey, p) - 70 * math.sin(math.pi * p)
            ww = lerp(st["s"] * bx[2], w - 56, p)
            hh = lerp(st["s"] * bx[3], 28, p)
            fill = C["accent"] if who == KAMU else C["bubble"]
            c.fill_rrect(px - ww / 2, py - hh / 2, ww, hh, hh / 2, fill, fade_ * (0.55 + 0.45 * p))


# ── the board (01 → recap) ──────────────────────────────────────────────────────────────────────────────────────────
def _scan_pos(t, t0, n, dur):
    """Reading band: slot position + alpha for a sweep over rows 0..n-1 starting at t0."""
    if t < t0 or t > t0 + dur + 0.3:
        return None, 0.0
    pos = lerp(-0.6, n - 0.4, curve("apple_in_out")(prog(t, t0, dur)))       # one pan, rest → rest
    a = clamp(prog(t, t0, 0.15)) * (1 - prog(t, t0 + dur, 0.3))
    return pos, a


def _story_state(t, Q):
    b = Q.b
    rows = []
    for i, (text, who) in enumerate(STORY_ROWS):
        if i < ON_BOARD:
            wr = glide(prog(t, Q.rows + i * 0.09, 0.4))
        else:
            wr = glide(prog(t, (Q.w7, Q.w8)[i - ON_BOARD], 0.55))
        gone = 0.0
        if i == 0:
            gone = _wipe_gone(t, Q)
        elif t >= Q.clean:
            gone = clamp(prog(t, Q.clean + (i - 1) * 0.1, 0.4))
        dim = 1 - 0.65 * clamp(prog(t, Q.sum, 0.4)) if i >= 1 else 1.0     # the summary takes focus
        rows.append(dict(text=text, who=who, slot=i, write=wr, gone=gone, a=dim))
    scroll = track(t, [(0.0, 0.0), (Q.scroll1, 1.0)], "smooth")
    slots = track(t, [(0.0, 8.0), (Q.grow, 11.0), (Q.shrink, 8.0)], "hero")
    scan, scan_a = _scan_pos(t, Q.scan, ON_BOARD, 1.3)
    tok = clamp(prog(t, Q.tok, 0.9)) * (1 - prog(t, b[3] - OUT, OUT))
    return dict(rows=rows, scroll=scroll, slots=slots, scan=scan, scan_a=scan_a, tok=tok)


def _row_span(c, g, text):
    """(x0, x1) of a row's text in board space."""
    w = c.measure(text.replace("|", ""), ROW_FONT, g["size"])[0]
    return g["text_x"], g["text_x"] + w


# eraser path (board space): rest on the tray → left of the top row → swept across it → parked on the top rim
def _eraser_frames(Q):
    g = papan_geo(-BW / 2, -BH / 2, BW, BH, 8, 0.0)
    rest = g["rest"]
    by, bh = g["band"](0)
    yrow = by + bh * 0.42
    x0 = g["text_x"] - 40
    park = (BW / 2 - 150, -BH / 2 - 26)
    top1 = (g["text_x"] + 40, yrow)
    low = (BW / 2 - 170, -BH / 2 + BH - 120)
    return rest, [(0.0, rest), (Q.lift, (x0, yrow)), (Q.wipe, (x0 + SWEEP, yrow)), (Q.wipe + 0.6, park),
                  (Q.clean - 0.35, top1), (Q.clean + 0.1, low), (Q.home, rest)], yrow


SWEEP, NAME_W = 600, 330            # eraser travel across the top row · approx. width of "Halo, aku Mumei." (Inter)


def _sweep(t, Q):
    return curve("apple_in_out")(prog(t, Q.wipe, 0.55))


def _wipe_gone(t, Q):
    """The top row disappears exactly where the eraser's leading edge has passed (cause and reaction, same frame):
    the eraser starts 40 px left of the text and is 200 px wide → its right edge sits 60 px into the row."""
    return clamp((60 + SWEEP * _sweep(t, Q)) / NAME_W) if t >= Q.wipe else 0.0


def _eraser_at(t, Q):
    rest, frames, _ = _eraser_frames(Q)
    if t < Q.lift or t > Q.home + 1.2:
        return None
    if Q.wipe <= t < Q.wipe + 0.55:
        x0, y0 = frames[1][1]
        return x0 + SWEEP * _sweep(t, Q), y0
    return track(t, frames, "smooth")


def draw_board(c, t, Q, st):
    smudge = _wipe_gone(t, Q)
    pos = _eraser_at(t, Q)
    papan_tulis(c, -BW / 2, -BH / 2, BW, BH, rows=st["rows"], scroll=st["scroll"], slots=st["slots"],
                scan=st["scan"], scan_a=st["scan_a"], tok=st["tok"], eraser=0.0 if pos else 1.0, look=LOOK,
                color=COL, font=ROW_FONT)
    if pos:
        penghapus(c, pos[0], pos[1], 1.0, look=LOOK, color=COL, smudge=smudge)


def board(v, T, Q):
    b = Q.b
    rig = Rig(x=MID, y=BCY, s=1.06, a=0.0)
    rig.to(Q.swap, preset="silk", s=1.0, a=1.0)                  # comes forward as the phone recedes

    def draw(c, t):
        op = 1 - prog(t, b[5] - OUT, OUT)
        with c.group(op):
            with rig.place(c, t):
                draw_board(c, t, Q, _story_state(t, Q))
                overlays(c, t, Q)
    v.add(Q.swap, b[5] + 0.05, draw, z=10, bleed=True)


def overlays(c, t, Q):
    """Board-space followers: the edge trace, tags on the rim, the circle on the eraser, the summary note."""
    b = Q.b
    g0 = papan_geo(-BW / 2, -BH / 2, BW, BH, 8, 0.0)
    _tag(c, t, Q.scan + 1.3, Q.label - 0.1, BW / 2 - 18, -BH / 2 - 58, f"DIBACA · {ON_BOARD} BARIS", align="r")
    sx, sy, sw, sh = g0["surface"]
    a_frame = 1 - prog(t, b[4] - OUT, OUT)
    draw_on(c, t, Q.frame, pts_rrect(sx, sy, sw, sh, 6), COL, width=6, dur=0.8, alpha=a_frame)
    _tag(c, t, Q.label, b[3] - OUT, -BW / 2 + 18, -BH / 2 - 58, "CONTEXT WINDOW")
    _tag(c, t, Q.w7 + 0.3, Q.lift - 0.1, BW / 2 - 18, -BH / 2 - 58, "PENUH · 8 / 8", align="r")
    _, frames, _ = _eraser_frames(Q)
    px, py = frames[3][1]
    mark(c, t, Q.name, "circle", (px - 120, py - 46, 240, 92), C["accent"], width=5, t_out=b[4] - OUT, seed=7)
    _tag(c, t, Q.name + 0.2, b[4] - OUT, px - 140, py - 20, "NAMAMU IKUT TERHAPUS", align="r")
    sticky(c, t, Q)


def sticky(c, t, Q):
    if t < Q.sum:
        return
    g = papan_geo(-BW / 2, -BH / 2, BW, BH, 8, 1.0)
    w, h = 470, 196
    a0 = (BW / 2 - w / 2 - 40, -BH / 2 + 150)
    by, bh = g["band"](1)
    a1 = (g["text_x"] - 30 + w / 2, by + h / 2 - 4)
    cx, cy = track(t, [(Q.sum, a0), (Q.settle, a1)], "smooth")
    rot = track(t, [(Q.sum, 0.05), (Q.settle, 0.025)], "smooth")
    op = clamp(prog(t, Q.sum, 0.3)) * (1 - prog(t, Q.b[5] - OUT, OUT))
    dy = (1 - glide(prog(t, Q.sum, 0.7))) * 24

    def body(c):
        mat.body(c, LOOK, mat.rrect_path(-w / 2, -h / 2, w, h, 6), (-w / 2, -h / 2, w, h), COL, r=6)
        c.text(-w / 2 + 30, -h / 2 + 46, "RINGKASAN", F["mono_med"], 19, C["brand_ink"], 0.8, ls=0.16)
        c.text(-w / 2 + 30, -h / 2 + 100, "Mumei · Bali 4 hari", F["ui_semi"], 36, C["brand_ink"])
        c.text(-w / 2 + 30, -h / 2 + 150, "budget hemat", F["ui_reg"], 34, C["brand_ink"])
    with c.group(op), c.at(cx, cy + dy, 1.0, rot=rot):
        body(c)


def _tag(c, t, t_in, t_out, x, y, label, align="l"):
    fade(c, t, t_in, t_out, lambda c: pop_tag(c, t, t_in, x, y, label, COL, align=align))


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w / (BW + 40), h / (BH + 80))
    st = dict(rows=[dict(text=tx, who=wh, slot=i, write=1.0, gone=0.55 if i == 0 else 0.0)
                    for i, (tx, wh) in enumerate(STORY_ROWS[:8])], scroll=0.0, slots=8, scan=2.6, scan_a=1.0,
              tok=0.0)
    with c.at(x + w / 2, y + h / 2, s, origin=(0, 0)):
        papan_tulis(c, -BW / 2, -BH / 2, BW, BH, eraser=0.0, look=LOOK, color=COL, font=ROW_FONT, **st)
        g = papan_geo(-BW / 2, -BH / 2, BW, BH, 8, 0.0)
        by, bh = g["band"](0)
        penghapus(c, g["text_x"] + 300, by + bh * 0.42, 1.0, look=LOOK, color=COL, smudge=0.6)


def build(project):
    T = project.timing
    v = Video(duration=T["L15"].end + TAIL, bpm=106, beat_offset=0.0)
    brand_intro(v, version=2)
    v.music = dict(style="marimba", key="G", mood="bright")
    v.sfx_kit = "wood"
    v.cover = lambda c: cover(c, "AI lupa\n*namamu*?", kicker="AI SEHARI-HARI", color=COL, badge="CONTEXT WINDOW",
                              tags=["chat", "token"], hero=_cover_hero)
    b = [0.0] + [T.chapter_span(n)[0] - LEAD for n in CH[1:]] + [v.duration]
    v.chapter(None, "INTRO", b[0], b[1])
    for n in range(3):
        v.chapter(n, CH[n + 1].split(" · ")[-1], b[n + 1], b[n + 2])
    v.chapter(None, "RECAP", b[4], b[5], dark=True)
    v.stage = lambda c, t: (draw_background(c, v, t), mat.stage(c, LOOK, COL, 1 - v.dark_amount(t)))
    v.finish = lambda c, t: mat.finish(c, LOOK, 1 - v.dark_amount(t))
    Q = Cue(T, b)
    phone(v, T, Q, phone_rig(Q))
    board(v, T, Q)
    intro(v, T, Q, b[0], b[1])
    bab0(v, T, Q, b[1], b[2])
    bab1(v, T, Q, b[2], b[3])
    bab2(v, T, Q, b[3], b[4])
    recap(v, T, Q, b[4], b[5])
    standard_outro(v, T, b[5], v.duration, "L15", COL,
                   teaser=dict(kicker="VIDEO BERIKUTNYA", title="“Kenapa OTP suka telat?”",
                               sub="SMS-nya mampir ke mana dulu"))
    v.cover_t = Q.wipe + 0.3
    return v


# ── INTRO: your first message → an hour of chat glides past → the AI asks your name ────────────────────────────────
def intro(v, T, Q, s, e):
    hs = heads(T, [("Dia lupa\n*namaku*.", "L01"), ("Nggak punya\n*ingatan*.", "L02")], e - OUT)

    def draw(c, t):
        kicker(c, t, T["L01"].start, e - OUT, "AI SEHARI-HARI", COL)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
    v.add(s, e, draw, z=20)
    v.sfx("send", Q.m0, 0.4)
    v.sfx("pop", Q.m1, 0.3)
    v.sfx("pop", Q.mark + 0.2, 0.35)
    v.sfx("whoosh", Q.lapse, 0.35)
    for i in range(0, 11, 2):
        v.sfx("tick", Q.lapse + (i + 1) * Q.lapse_step, 0.18)
    v.sfx("pop", Q.ask, 0.5)
    dolly(v, T["L02"].start + 0.3, e - 0.2)


# ── 00 · BACA ULANG: rewind → the phone steps aside → every send carries the whole thread → the AI forgets ─────────
def bab0(v, T, Q, s, e):
    col = tk.CHAPTER[0][0]
    hs = heads(T, [("Dibaca ulang,\n*semua*.", "L03", "L04"), ("Cuma *oke*,\ntetap dari awal.", "L05")], e - OUT)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[1], col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("whoosh", Q.rack - 0.1, 0.4)
    v.sfx("pop", Q.card, 0.35)
    for t0, t1, txt in ((Q.type1, Q.send1, STORY_ROWS[4][0]), (Q.type2, Q.send2, "oke")):
        n = len(txt.replace(" ", ""))
        for i in range(0, n, 2):
            v.sfx("key", t0 + (t1 - t0 - 0.15) * i / max(1, n), 0.3)
        v.sfx("send", t1, 0.45)
    for ts, n in ((Q.stream1, 5), (Q.stream2, 7)):
        v.sfx("whoosh", ts, 0.4)
        for i in range(n):
            v.sfx("tick", ts + i * 0.07 + 0.5, 0.22)
    v.sfx("pop", Q.reply1, 0.35)
    v.sfx("whoosh", Q.clear1, 0.25)


# ── 01 · CONTEXT WINDOW: the board comes forward with the chat on it; read band, edge, name, tokens, size, memory ───
def bab1(v, T, Q, s, e):
    col = tk.CHAPTER[1][0]
    hs = heads(T, [("Papannya\n*segini*.", "L06"), ("Namanya\n*context window*.", "L07"),
                   ("Makin panjang,\nmakin *mahal*.", "L08")], e - OUT)
    mem_box = (X + 124, 1462, 480, 96)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[2], col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
        lit = 7 * glide(prog(t, Q.mem + 0.2, 1.0))
        a = clamp(prog(t, Q.mem, 0.35)) * (1 - prog(t, e - OUT, OUT))
        dy = (1 - glide(prog(t, Q.mem, 0.6))) * 30
        with c.group(a), c.at(0, dy):
            memori(c, mem_box[0], mem_box[1], mem_box[2], cells=11, lit=lit, look=LOOK, color=COL)
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("whoosh", Q.swap, 0.45)
    for i in range(0, ON_BOARD, 2):
        v.sfx("key", Q.rows + i * 0.09, 0.25)
    v.sfx("tick", Q.scan, 0.35)
    v.sfx("tick", Q.frame, 0.35)
    v.sfx("pop", Q.label, 0.45)
    v.sfx("tick", Q.tok, 0.35)
    v.sfx("whoosh", Q.grow, 0.35)
    for i in range(7):
        v.sfx("tick", Q.mem + 0.2 + 0.07 * i, 0.25)
    v.sfx("thud", Q.mahal, 0.6)


# ── 02 · DIHAPUS: full → the eraser lifts, wipes the top row, the board rolls up; your name is on the felt ───────────
def bab2(v, T, Q, s, e):
    col = tk.CHAPTER[2][0]
    hs = heads(T, [("Papannya\n*penuh*.", "L09"), ("Yang atas\n*dihapus*.", "L10"), ("Termasuk\n*namamu*.", "L11")],
               e - OUT)

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, CH[3], col)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
    v.add(s, e, draw, z=20)
    cut(v, s)
    v.sfx("key", Q.w7, 0.4)
    v.sfx("pop", Q.w7 + 0.3, 0.35)
    v.sfx("click", Q.lift, 0.4)
    v.sfx("whoosh", Q.wipe, 0.55)
    v.sfx("key", Q.w8, 0.35)
    v.sfx("pop", Q.name, 0.4)
    dolly(v, Q.name + 0.9, e - 0.2)


# ── RECAP (dark): summary note → the board is wiped on purpose → the note on the clean board ───────────────────────
def recap(v, T, Q, s, e):
    hs = heads(T, [("*Rangkum*,\nlalu chat baru.", "L12"), ("Hapus papan,\n*sengaja*.", "L13")], e - OUT,
               style="headline_dark")

    def draw(c, t):
        kicker(c, t, s + 0.2, e - OUT, "RECAP", COL)
        draw_heads(c, t, hs, reveal="ink", exit="quiet")
    v.add(s, e, draw, z=20)
    v.sfx("whoosh_dark", s, 0.6)
    cut(v, s)
    v.sfx("pop", Q.sum, 0.5)
    v.sfx("whoosh", Q.clean, 0.6)
    v.sfx("tick", Q.settle, 0.4)
    v.sfx("click", Q.home + 0.6, 0.3)
    dolly(v, Q.home + 1.0, e - 0.2)
    cut(v, e)
