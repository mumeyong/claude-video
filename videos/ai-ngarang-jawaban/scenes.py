"""Kenapa ChatGPT kadang ngarang jawaban? (pilar B, AI sehari-hari, QUICK). See PLAN.md.

Metaphor: the phone keyboard that guesses your next word — an AI like ChatGPT is its giant version. Hero: the
keyboard + its suggestion bar (one persistent Rig): "nanti aku…" → pulang (00), the giant version writing a fake
book summary token by token (00), a bar with no "nggak tahu" key that still picks a winner from near-equal bars
(01), and the "nggak tahu" slot finally installed (02). Signature: the top word in the bar jumps into the sentence.
Look: classic + reel moves (count_pill in 00, one pixel_wipe into 02, pop_card habit cards in 02).
Motion: heavy springs (Rig) · ink headlines · persistent hero glue · mask exits.
Sound: styled score lofi Eb warm 88 + glass SFX kit.
"""
from engine import Video, tokens as tk
from engine.ease import prog, clamp, out_back, out_cubic, in_cubic, in_out_cubic
from engine.components import (Headline, kicker, appear, fade, note, word_pill, pop_tag, check_badge, brand_intro,
                               standard_outro, cover, Rig, count_pill, pixel_wipe, pop_card, reel_sfx, type_cues,
                               keyboard_hp, suggest_bar, token_line, KB_RATIO, TEBAK_PURPLE as PURPLE)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT = M["out"]
X, CW = L["col_x"], L["col_w"]
CXc = X + CW / 2
LEAD = 0.6
OUTRO_TAIL = 3.0
PRE_ROLL = 2.05                            # long brand sting (version 2): voice starts under its wipe
CH = ["00 · NEBAK KATA", "01 · KENAPA YAKIN", "02 · BIAR NGGAK NGARANG", "RECAP", "OUTRO"]
CORAL = C["orange_pill"]

# the hero, drawn around (0, 0) inside the Rig: text field · suggestion bar · keyboard
KW = 820
KH = KW * KB_RATIO
BAR = (-KW / 2, -116, KW, 96)
FIELD = (-KW / 2, -250, KW, 104)
HERO_BOX = (-KW / 2 - 20, -270, KW + 40, KH + 290)

# the fake book answer (illustration) — cut into tokens; each step's bar = (picked, two alternatives)
ANSWER = ["Novel", " ini", " ter", "bit", " tahun", " 2009", ",", " cerita", "nya", " tentang", " anak", " nelayan",
          " yang", " …"]
ALTS = [("Buku", "Kisah"), (" itu", " karya"), (" di", " pertama"), ("bitan", "kenal"), (" lalu", " baru"),
        (" 2011", " 1998"), (" dan", "."), (" kisah", " isinya"), (" ini", " pun"), (" soal", " anak"),
        (" gadis", " keluarga"), (" muda", " pesisir"), (" hidup", ","), (" .", " dan")]


def _w(T, lid, word, frac, nth=0):
    """Time of a word, falling back to a fraction of the line."""
    try:
        return T.word(lid, word, nth)
    except Exception:
        return T[lid].frac(frac)


def _heads(T, items, end, style="headline"):
    out = []
    for i, (text, lid) in enumerate(items):
        t_out = T[items[i + 1][1]].start - 0.4 if i + 1 < len(items) else end
        out.append((Headline(text, style=style), T[lid].start, t_out))
    return out


def _draw_heads(c, t, hs):
    for h, a, b in hs:
        h.draw(c, t, a, b, reveal="ink", exit="mask")


def _cam(v, t, y, zoom, dur=0.9):
    """Gentle push: the camera only travels a third of the way to y, so the headline stays on screen."""
    v.camera.key(t, zoom=zoom, x=tk.W / 2, y=tk.H / 2 + (y - tk.H / 2) * 0.3, dur=dur, ease=in_out_cubic)


def _field(c, tokens, n, src=None, alpha=1.0, size=44):
    x, y, w, h = FIELD
    c.card(x, y, w, h, r=26, alpha=alpha)
    with c.group(alpha):
        cx, cy = token_line(c, x + 34, y + h / 2 + size * 0.36, tokens, n, w - 90, size=size, src=src)
        if alpha > 0.5:
            c.fill_rrect(cx + 6, cy - size * 0.8, 4, size * 0.95, 2, C["accent"], 0.9)


def build(project):
    T = project.timing
    v = Video(duration=T["L17"].end + OUTRO_TAIL, bpm=88, beat_offset=0.0)
    brand_intro(v, version=2)
    v.series = "AI"
    v.music = dict(style="lofi", key="Eb", mood="warm")       # interview marimba Bb bright, jalur ambient D warm
    v.sfx_kit = "glass"
    v.cover = lambda c: cover(c, "ChatGPT\ncuma *nebak*?", kicker="KENAPA AI NGARANG", color=PURPLE,
                              tags=["keyboard HP", "token", "hallucination"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    rig = Rig(x=CXc, y=2350, s=0.9)
    intro(v, T, 0.0, b[CH[0]])
    hero(v, T, b, rig)
    nebak(v, T, b[CH[0]], b[CH[1]], rig)
    yakin(v, T, b[CH[1]], b[CH[2]], rig)
    cara(v, T, b[CH[2]], b["RECAP"], rig)
    recap(v, T, b["RECAP"], b["OUTRO"])
    standard_outro(v, T, b["OUTRO"], v.duration, "L17", PURPLE,
                   teaser=dict(kicker="BERIKUTNYA", title="Kenapa AI bisa lupa?", sub="obrolan panjang & context window"))
    v.cover_t = T["L06"].end
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w / (KW + 40), h / (KH + 300))
    with c.at(x + w / 2, y + h / 2 - (KH - 250) / 2 * s + 10, s, origin=(0, 0)):
        _field(c, list("nanti aku") + [" pulang"], 10)
        suggest_bar(c, *BAR[:3],["pulang", "telat", "kabarin"], probs=(0.82, 0.46, 0.3), pick=0, pick_p=1.0)
        keyboard_hp(c, -KW / 2, 0, KW)


# ── INTRO: a chat about a book that doesn't exist → a fluent answer → every word is a guess ──────────────────
def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    box = (X, 560, CW, 560)
    t_card = L1.start - 0.2
    t_a0, t_a1 = L2.start + 0.1, L2.end - 0.1
    t_pills = _w(T, "L03", "nebak", 0.8) - 0.1
    hs = _heads(T, [("Buku yang\n*nggak ada*.", "L01"), ("Jawabannya\n*lengkap*.", "L02"), ("Dia *nebak*.", "L03")],
                e - OUT)
    ask = "Ringkasin buku Senja di Kota Awan dong."

    def card(c):
        x, y, w, h = box
        c.card(x, y, w, h, r=28)
        c.circle(x + 40, y + 50, 7, PURPLE)
        c.text(x + 58, y + 58, "AI · CHAT", F["mono_med"], 20, C["muted"], 1, 0.16)
        c.fill_rrect(x + w - 150, y + 30, 120, 38, 19, C["faint"], 0.5)
        c.text(x + w - 90, y + 56, "ilustrasi", F["ui"], 20, C["ink2"], 1, align="c")
        bw = c.measure(ask, F["ui"], 32, -0.01)[0] + 56
        c.fill_rrect(x + w - 34 - bw, y + 100, bw, 74, 30, C["accent_soft"])
        c.text(x + w - 34 - bw + 28, y + 148, ask, F["ui"], 32, C["ink"], 1, -0.01)

    def draw(c, t):
        kicker(c, t, L1.start, e - OUT, "EKSPERIMEN KECIL", PURPLE)
        _draw_heads(c, t, hs)

        def body(c):
            card(c)
            n = len(ANSWER) * clamp(prog(t, t_a0, t_a1 - t_a0))
            c.circle(X + 50, 818 - 14, 12, PURPLE, 0.9 if n > 0 else 0.0)
            token_line(c, X + 80, 818, ANSWER, n, CW - 120, size=42, pills=out_cubic(prog(t, t_pills, 0.5)))
            if t > t_pills:
                pop_tag(c, t, t_pills + 0.25, X + 80, 1040, "tiap potongan = tebakan", PURPLE)
        appear(c, t, t_card, e - OUT, box, body)
        p = prog(t, L1.end - 0.6, 0.6) * (1 - prog(t, e - OUT, 0.3))
        if p > 0:
            with c.at(0, 0, 1, origin=(X + 40, 1260), rot=-0.035):
                note(c, X + 40, 1260, "bukunya nggak ada", p, arrow_to=(X + 420, 1150), size=42)
    v.add(s, e + 0.4, draw, z=20)
    _cam(v, t_a0, 860, 1.05)
    _cam(v, L3.end - 0.3, 960, 1.0, dur=0.8)
    v.sfx("pop", t_card + 0.1, 0.6)
    for i in range(len(ANSWER)):
        v.sfx("key", t_a0 + i * (t_a1 - t_a0) / len(ANSWER), 0.35)
    v.sfx("pop", L1.end - 0.5, 0.4)
    v.sfx("chime", t_pills, 0.6)


# ── the persistent hero: keyboard rises in 00, sinks for the giant version, close-up in 01, small in 02 ─────────
def hero(v, T, b, rig):
    s0, s1, s2, s3 = b[CH[0]], b[CH[1]], b[CH[2]], b["RECAP"]
    rig.to(s0 + 0.1, preset="heavy", y=1090)
    rig.to(T["L07"].start, preset="heavy", y=1275, s=0.6)
    rig.to(s1 + 0.05, preset="heavy", y=1190, s=1.0)
    rig.to(s2 - 0.1, preset="heavy", y=1290, s=0.55)
    v.sfx("whoosh", s0 + 0.1, 0.5)
    v.sfx("whoosh", s1 + 0.05, 0.4)


def _keys(t, s1, s2):
    """Keyboard keys: on in 00, collapse for the 01 close-up, back in 02."""
    return (1 - out_cubic(prog(t, s1, 0.5))) + out_cubic(prog(t, s2, 0.5))


def _src(rig, t, centre):
    st = rig.state(t)
    return st["x"] + centre[0] * st["s"], st["y"] + centre[1] * st["s"]


# ── 00 · NEBAK KATA: "nanti aku" → pulang · telat · kabarin → pulang jumps · the giant version, token by token ─
def nebak(v, T, s, e, rig):
    ch = v.chapter(0, "NEBAK KATA", s, e)
    L4, L5, L6, L7, L8 = (T[k] for k in ("L04", "L05", "L06", "L07", "L08"))
    typed = list("nanti aku")
    t_ty0 = _w(T, "L04", "nanti", 0.7)
    t_ty1 = max(t_ty0 + 0.6, L4.end)
    t_words = [_w(T, "L05", "pulang", 0.55), _w(T, "L05", "telat", 0.75), _w(T, "L05", "kabarin", 0.9)]
    t_probs = _w(T, "L06", "paling", 0.7)
    t_pick = max(t_probs + 0.7, L6.end - 0.5)
    t_g0, t_g1 = L8.start + 0.1, L8.end - 0.2
    t_tok = _w(T, "L08", "token", 0.3)
    hs = _heads(T, [("Keyboard-mu\n*nebak*.", "L04"), ("Bukan ngerti:\n*paling sering*.", "L06"),
                    ("Versi *raksasa*.", "L07"), ("Satu *token*,\nlalu lagi.", "L08")], e - OUT)

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, "00 · KEYBOARD HP KAMU", ch.color)
        _draw_heads(c, t, hs)
        out = 1 - in_cubic(prog(t, e - OUT, OUT))
        st_keys = _keys(t, e, 1e9)
        giant = t >= L7.start
        hero_on = t < e                                       # 01 carries the same hero on from e
        with rig.place(c, t, bbox=HERO_BOX):
            if not hero_on:
                pass
            elif not giant or t < t_g0:
                k = clamp(prog(t, t_ty0, t_ty1 - t_ty0)) * len(typed)
                fly = out_cubic(prog(t, t_pick + 0.15, 0.45))
                fa = 1 - out_cubic(prog(t, L7.start, 0.4))
                _field(c, typed + [" pulang"], k + fly if fly > 0 else k, src=(BAR[0] + KW / 6, BAR[1] + 48),
                       alpha=fa)
                words, probs = ["pulang", "telat", "kabarin"], (0.82, 0.46, 0.3)
                wa = [out_cubic(prog(t, tw, 0.3)) for tw in t_words]
                if fly > 0:
                    wa[0] *= 1 - fly
                suggest_bar(c, *BAR[:3],words, probs=probs, bars=out_cubic(prog(t, t_probs, 0.7)), pick=0,
                            pick_p=prog(t, t_pick, 0.2) * (1 - prog(t, L7.start, 0.3)), word_a=wa)
                ci = min(len(typed) - 1, int(k))
                press_p = (k % 1.0) * 2 if t < t_ty1 else 0.0
                keyboard_hp(c, -KW / 2, 0, KW, press=typed[ci].strip() or None, press_p=clamp(press_p),
                            keys=st_keys)
            else:
                n = len(ANSWER) * clamp(prog(t, t_g0, t_g1 - t_g0))
                k = min(len(ANSWER) - 1, int(n))
                alt = ALTS[k]
                f = n - int(n)
                suggest_bar(c, *BAR[:3],[ANSWER[k].strip(), alt[0].strip(), alt[1].strip()], probs=(0.74, 0.4, 0.22),
                            pick=0, pick_p=1.0 if n < len(ANSWER) else 0.0, word_a=[1 - f, 1, 1])
                keyboard_hp(c, -KW / 2, 0, KW, keys=st_keys)
        if t >= t_g0:
            n = len(ANSWER) * clamp(prog(t, t_g0, t_g1 - t_g0))
            k = min(len(ANSWER) - 1, int(n))
            with c.group(out):
                token_line(c, X, 640, ANSWER, n, CW, size=56, pills=0.6,
                           src=_src(rig, t, (BAR[0] + KW / 6, BAR[1] + 48)) if n < len(ANSWER) else None)
                count_pill(c, t, t_tok, X + 130, 860, 0, len(ANSWER), label="TOKEN", dur=t_g1 - t_tok,
                           t_out=e - OUT)
    v.add(s, e + 0.3, draw, z=20)
    _cam(v, t_words[0] - 0.3, 1000, 1.06)
    _cam(v, L7.start, 960, 1.0, dur=1.0)
    for i, ch_ in enumerate(typed):
        if ch_ != " ":
            v.sfx("key", t_ty0 + (i + 0.5) * (t_ty1 - t_ty0) / len(typed), 0.45)
    for tw in t_words:
        v.sfx("pop", tw, 0.5)
    v.sfx("tick", t_probs, 0.5)
    v.sfx("click", t_pick + 0.15, 0.7)
    for i in range(len(ANSWER)):
        v.sfx("key", t_g0 + i * (t_g1 - t_g0) / len(ANSWER), 0.4)
    reel_sfx(v, "count", t_tok, each=t_g1 - t_tok)


# ── 01 · KENAPA YAKIN: no "nggak tahu" key · near-equal bars still crown a winner · hallucination. ─────────────
def yakin(v, T, s, e, rig):
    ch = v.chapter(1, "KENAPA YAKIN", s, e)
    L9, L10, L11, L12 = (T[k] for k in ("L09", "L10", "L11", "L12"))
    t_miss = _w(T, "L09", "tahu", 0.8) - 0.2
    t_bars = _w(T, "L10", "kosong", 0.35)
    t_pick = _w(T, "L10", "mungkin", 0.85)
    t_hal = _w(T, "L12", "hallucination", 0.3)
    hs = _heads(T, [("Nggak ada tombol\n*nggak tahu*.", "L09"), ("Kosong pun\ntetap *nebak*.", "L10"),
                    ("Mungkin ≠ *bener*.", "L11"), ("Lancar, tapi\n*ngarang*.", "L12")], e - OUT)
    base = ["…", " Kota", " Awan", " terbit", " tahun"]

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, "01 · KENAPA KEDENGERAN YAKIN", ch.color)
        _draw_heads(c, t, hs)
        out = 1 - in_cubic(prog(t, e - OUT, OUT))
        fly = out_cubic(prog(t, t_pick + 0.15, 0.45))
        ha = 1 - prog(t, e - 0.35, 0.3)                       # hands over to 02's hero under the wipe
        with c.group(ha), rig.place(c, t, bbox=HERO_BOX):
            _field(c, base + [" 2009"], len(base) + fly if fly > 0 else len(base), src=(BAR[0] + 0.73 * KW / 6,
                   BAR[1] + 48), alpha=out_cubic(prog(t, s + 0.2, 0.4)))
            cen = suggest_bar(c, *BAR[:3],["2009", "2011", "1998"], probs=(0.36, 0.33, 0.31),
                              bars=out_cubic(prog(t, t_bars, 0.7)), pick=0, pick_p=prog(t, t_pick, 0.2),
                              missing="nggak tahu", missing_p=prog(t, t_miss, 0.35), word_a=[1 - fly, 1, 1])
            kk = 1 - out_cubic(prog(t, s, 0.3))                # keys + panel fold away for the bar close-up
            keyboard_hp(c, -KW / 2, 0, KW, keys=kk, alpha=kk)
            if t > t_miss + 0.4:
                mx = cen[-1][0]
                c.line(mx - 100, BAR[1] + 52, mx + 100, BAR[1] + 44, CORAL, 5, clamp(prog(t, t_miss + 0.4, 0.3)))
                pop_tag(c, t, t_miss + 0.5, mx + 110, BAR[1] + 112, "nggak ada", CORAL, align="r")
        p = prog(t, t_bars + 0.5, 0.6) * out * (1 - prog(t, L11.start, 0.4))
        if p > 0:
            with c.at(0, 0, 1, origin=(X + 20, 1380), rot=0.03):
                note(c, X + 20, 1380, "hampir rata — tetap ada juaranya", p, arrow_to=(X + 160, 1180), size=40)
        if t >= t_hal:
            pa = out_back(prog(t, t_hal, 0.45))
            with c.at(0, 0, max(0.01, pa), origin=(X, 640)):
                word_pill(c, X, 580, "hallucination.", CORAL, size=100, alpha=min(1.0, pa) * out)
    v.add(s, e + 0.3, draw, z=20)
    _cam(v, t_miss - 0.2, 1080, 1.06)
    _cam(v, t_bars, 1100, 1.03, dur=0.7)
    v.camera.key(t_hal, zoom=0.97, dur=0.3).key(t_hal + 0.35, zoom=1.0, dur=0.5)
    v.sfx("pop", t_miss, 0.5)
    v.sfx("click", t_miss + 0.45, 0.5)
    v.sfx("tick", t_bars, 0.5)
    v.sfx("click", t_pick + 0.15, 0.7)
    v.sfx("pop", t_bars + 0.5, 0.35)
    v.sfx("thud", t_hal)


# ── 02 · BIAR NGGAK NGARANG: pixel wipe → three habit cards · the "nggak tahu" slot is finally installed ─────────
CARDS = [("01 · CONTEXT", "PDF · catatan · data", "> ingatan AI"),
         ("02 · SUMBER", "link → buka sendiri", "baca, jangan cuma percaya"),
         ("03 · IZIN", "“Kalau ragu,", "jawab: nggak tahu.”")]


def cara(v, T, s, e, rig):
    ch = v.chapter(2, "BIAR NGGAK NGARANG", s, e)
    L13, L14, L15 = T["L13"], T["L14"], T["L15"]
    t_wipe = s - 0.35
    t_cards = [L13.start + 0.1, L14.start + 0.05, L15.start + 0.05]
    t_slot = _w(T, "L15", "nggak", 0.75, nth=0)
    t_pick = t_slot + 0.5
    hs = _heads(T, [("Kasih *context*.", "L13"), ("Minta *sumber*.", "L14"), ("Izinin\n*nggak tahu*.", "L15")],
                e - OUT)
    boxes = [(X, 560, 760, 170, -0.02), (X + 70, 755, 760, 170, 0.015), (X + 20, 950, 760, 170, -0.012)]

    def wipe(c, t):
        pixel_wipe(c, t, t_wipe, PURPLE, after=None)
    v.add(t_wipe, t_wipe + 1.0, wipe, z=100)

    def card_draw(i):
        kk, title, sub = CARDS[i]

        def d(c, x, y, w, h):
            c.text(x + 34, y + 50, kk, F["mono_bold"], 21, PURPLE, 1, 0.16)
            c.text(x + 34, y + 108, title, F["display_semi"], 46, C["ink"], 1, -0.03)
            c.text(x + 34, y + 148, sub, F["mono"], 24, C["ink2"], 1)
        return d

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, "02 · TIGA KEBIASAAN", ch.color)
        _draw_heads(c, t, hs)
        out = 1 - in_cubic(prog(t, e - OUT, OUT))
        with c.group(out):
            for i, (x, y, w, h, rot) in enumerate(boxes):
                with c.at(0, 0, 1, origin=(x + w / 2, y + h / 2), rot=rot):
                    pop_card(c, t, t_cards[i], x, y, w, h, draw=card_draw(i))
        fly = out_cubic(prog(t, t_pick + 0.1, 0.45))
        slot = out_back(prog(t, t_slot, 0.4))
        ha = out * out_cubic(prog(t, s - 0.1, 0.3))            # takes over from 01's hero under the wipe
        with c.group(ha), rig.place(c, t, bbox=HERO_BOX):
            _field(c, ["Jawabannya:", " nggak", " tahu."], 1 + 2 * fly, alpha=1.0)
            third = "nggak tahu" if t >= t_slot else "1998"
            with c.at(0, 0, 1 + 0.08 * (1 - clamp(slot)) if t >= t_slot else 1, origin=(KW / 3, BAR[1] + 48)):
                suggest_bar(c, *BAR[:3],["2009", "2011", third], probs=(0.36, 0.33, 0.31 if t < t_slot else 0.9),
                            pick=2, pick_p=prog(t, t_pick, 0.2) if t >= t_slot else 0.0,
                            missing=None if t >= t_slot else "nggak tahu", missing_p=1.0, word_a=[1, 1, 1 - fly])
            keyboard_hp(c, -KW / 2, 0, KW, keys=out_cubic(prog(t, s - 0.1, 0.5)))
        if t > t_pick + 0.4:
            st = rig.state(t)
            check_badge(c, st["x"] + (KW / 2 - 30) * st["s"], st["y"] + (BAR[1] + 4) * st["s"], 22,
                        out_back(prog(t, t_pick + 0.4, 0.4)) * out)
    v.add(s - 0.4, e + 0.3, draw, z=20)
    _cam(v, t_cards[0], 700, 1.04)
    _cam(v, t_cards[2], 1000, 1.03)
    _cam(v, t_slot - 0.2, 1240, 1.06, dur=0.7)
    _cam(v, e - 0.8, 960, 1.0, dur=0.6)
    reel_sfx(v, "wipe", t_wipe)
    for tc in t_cards:
        reel_sfx(v, "cards", tc)
    v.sfx("pop", t_slot, 0.7)
    v.sfx("click", t_pick + 0.1, 0.6)
    v.sfx("chime", t_pick + 0.4)


# ── RECAP (dark): the bar one last time — cepet · ngebantu · di-review → review wins ────────────────────────────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L16 = T["L16"]
    t_w = [_w(T, "L16", "cepet", 0.55), _w(T, "L16", "ngebantu", 0.7), _w(T, "L16", "review", 0.92)]
    t_pick = t_w[2] + 0.15
    h1 = Headline("Junior yang\n*pede*.", style="headline_dark")
    h2 = Headline("Tetap aku\n*review*.", style="headline_dark")
    bw, by = KW, 900

    def draw(c, t):
        h1.draw(c, t, L16.start, t_w[2] - 0.45, reveal="ink", exit="mask")
        h2.draw(c, t, t_w[2] - 0.2, e - OUT, reveal="ink", exit="mask")
        a = out_cubic(prog(t, s + 0.2, 0.6)) * (1 - in_cubic(prog(t, e - OUT, OUT)))
        if a <= 0.002:
            return
        with c.group(a):
            cen = suggest_bar(c, CXc - bw / 2, by, bw, ["cepet", "ngebantu", "di-review"], dark=True, h=110, size=38,
                              pick=2, pick_p=prog(t, t_pick, 0.25), word_a=[out_cubic(prog(t, tw, 0.3)) for tw in t_w])
            keyboard_hp(c, CXc - bw / 2, by + 130, bw, dark=True)
            check_badge(c, cen[2][0] + 120, by + 8, 22, out_back(prog(t, t_pick + 0.3, 0.4)))
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.0, dur=0.01).key(s + 0.1, zoom=1.04, y=1000, dur=max(1.0, e - s - 0.6))
    v.sfx("whoosh_dark", s)
    for tw in t_w:
        v.sfx("pop", tw, 0.45)
    v.sfx("chime", t_pick + 0.3)
