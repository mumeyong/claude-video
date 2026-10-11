"""Dari System Engineer ke Senior Cloud Engineer — jalur aku (pilar C, karier). See PLAN.md.

Metaphor: a career as a game skill tree growing bottom → top. LV 1 (2020, System Engineer) opens tool branches,
LV 2 (2021, Cloud Engineer, project bank) adds a branch that is a question ("kenapa pilih ini?"), LV 3 (Senior)
— and the top tier unlocks into questions, not tools. Signature: a branch creeps up with a bright tip, the tile's
ring charges round, the tile unlocks (red border + ✓, small pop).
Look: classic + reel moves (iris into 02, float_chips + highlight_phrase in 03).
Motion: silk springs · mask headlines · Morph glue (name card → root node) + persistent tree · dim exits.
Sound: styled score ambient D warm 80 + soft SFX kit.
"""
import math

from engine import Video, tokens as tk
from engine.ease import prog, out_back, out_cubic, in_cubic, in_out_cubic, mix
from engine.components import (Headline, kicker, fade, pop_tag, note, bubble, word_pill, brand_intro, standard_outro,
                               cover, Morph, yaw, spring_at, iris, float_chips, highlight_phrase, reel_sfx, branch,
                               skill_tree, name_card, TREE_RED as RED)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
OUT, DOUT = M["out"], M["dim_out"]
X, CW = L["col_x"], L["col_w"]
CXc = X + CW / 2                           # tree axis = centre of the safe column
LEAD = 0.6
OUTRO_TAIL = 3.0
PRE_ROLL = 2.05                            # long brand sting (version 2): voice starts under its wipe
CH = ["00 · SYSTEM ENGINEER", "01 · CLOUD ENGINEER", "02 · SENIOR", "03 · SALAH KAPRAH", "RECAP", "OUTRO"]

# ── the tree (screen coordinates): root at the bottom, LV 1 → LV 3, the question tier on top ─────────────
TW, TH, QW, DX = 250, 92, 390, 284
GEO = {
    "root": (CXc, 1470, 84, 84, "2020", None, "root"),
    "a0": (CXc - DX, 1280, TW, TH, "CI/CD", "pipeline", "tool"),
    "a1": (CXc, 1280, TW, TH, "monitoring", "observability", "tool"),
    "a2": (CXc + DX, 1280, TW, TH, "serverless", "deploy pertama", "tool"),
    "b0": (CXc - DX, 1080, TW, TH, "Kubernetes", None, "tool"),
    "b1": (CXc, 1080, TW, TH, "multi-AZ", None, "tool"),
    "b2": (CXc + DX, 1080, TW, TH, "biaya cloud ↓", None, "tool"),
    "c0": (CXc - DX, 880, TW, TH, "migrasi big data", None, "tool"),
    "c1": (CXc, 880, TW, TH, "serverless stack", None, "tool"),
    "c2": (CXc + DX, 880, TW, TH, "mentoring", "junior", "tool"),
    "q0": (CXc - 210, 680, QW, TH, "Perlu Kubernetes?", None, "question"),
    "q1": (CXc + 210, 680, QW, TH, "Kalau salah, berapa?", None, "question"),
}
EDGES = [("root", "a0"), ("root", "a1"), ("root", "a2"), ("a0", "b0"), ("a1", "b1"), ("a2", "b2"),
         ("b0", "c0"), ("b1", "c1"), ("b2", "c2"), ("c0", "q0"), ("c1", "q1"), ("c2", "q1")]
ROOT_BOX = (CXc - 42, 1470 - 42, 84, 84)
CARD = (X + 30, 640, CW - 60, 520)


def _nodes(t, sched, alpha=None):
    """Node dicts at t. sched = {id: unlock time}: ring charges over the 0.35 s before it, the tile unlocks after."""
    out = {}
    for k, (x, y, w, h, label, sub, kind) in GEO.items():
        tu = sched.get(k)
        charge = 0.0 if tu is None else out_cubic(prog(t, tu - 0.35, 0.35))
        unlock = 0.0 if tu is None else prog(t, tu, 0.35)
        out[k] = dict(x=x, y=y, w=w, h=h, label=label, sub=sub, kind=kind, charge=charge, unlock=unlock,
                      a=(alpha or {}).get(k, 1.0))
    return out


def _edges(t, sched):
    return [(a, b, 0.0 if sched.get(b) is None else in_out_cubic(prog(t, sched[b] - 0.7, 0.55)), 1.0)
            for a, b in EDGES]


def _w(T, lid, word, frac):
    """Time of a word, falling back to a fraction of the line (terms like CI/CD / multi-AZ normalise oddly)."""
    try:
        return T.word(lid, word)
    except Exception:
        return T[lid].frac(frac)


def _heads(T, items, end, style="headline"):
    out = []
    for i, (text, lid) in enumerate(items):
        t_out = T[items[i + 1][1]].start - 0.45 if i + 1 < len(items) else end
        out.append((Headline(text, style=style), T[lid].start, t_out))
    return out


def _draw_heads(c, t, hs):
    for h, a, b in hs:
        h.draw(c, t, a, b, reveal="mask", exit="dim")


def _cam(v, t, y, zoom, dur=0.9):
    """Gentle push: the camera only travels a third of the way to y, so the headline stays on screen."""
    v.camera.key(t, zoom=zoom, x=tk.W / 2, y=tk.H / 2 + (y - tk.H / 2) * 0.3, dur=dur, ease=in_out_cubic)


def build(project):
    T = project.timing
    v = Video(duration=T["L20"].end + OUTRO_TAIL, bpm=80, beat_offset=0.0)
    brand_intro(v, version=2)
    v.series = "KARIER"
    v.music = dict(style="ambient", key="D", mood="warm")      # foto-WA cinematic G dreamy, kubernetes garage E warm
    v.sfx_kit = "soft"
    v.cover = lambda c: cover(c, "Naik level\nbukan *tools*.", kicker="JALUR KARIER CLOUD", color=RED,
                              tags=["LV 1 → LV 3", "dari CV asli", "2020 → sekarang"], hero=_cover_hero)
    b = {name: T.chapter_span(name)[0] - LEAD for name in CH}
    sched = {
        "a0": _w(T, "L05", "CI/CD", 0.18), "a1": _w(T, "L05", "monitoring", 0.42),
        "a2": _w(T, "L05", "serverless", 0.62),
        "b0": _w(T, "L09", "Kubernetes", 0.08), "b1": _w(T, "L09", "multi-AZ", 0.32),
        "b2": _w(T, "L09", "turun", 0.85),
        "c0": _w(T, "L13", "Migrasi", 0.04) + 0.2, "c1": _w(T, "L13", "serverless", 0.5),
        "c2": _w(T, "L13", "mentoring", 0.78),
        "q0": _w(T, "L15", "Kubernetes", 0.45), "q1": _w(T, "L15", "biayanya", 0.75),
    }
    t_land = intro(v, T, 0.0, b[CH[0]])
    sched["root"] = t_land - 0.4
    tree(v, T, t_land, b, sched)
    lv1(v, T, b[CH[0]], b[CH[1]], sched)
    lv2(v, T, b[CH[1]], b[CH[2]], sched)
    lv3(v, T, b[CH[2]], b[CH[3]], sched)
    salah(v, T, b[CH[3]], b["RECAP"])
    recap(v, T, b["RECAP"], b["OUTRO"])
    standard_outro(v, T, b["OUTRO"], v.duration, "L20", RED,
                   teaser=dict(kicker="TULIS DI KOMENTAR", title="Kamu lagi di cabang mana?",
                               sub="LV 1, LV 2, atau udah mutusin?"))
    v.cover_t = T["L15"].frac(0.9)
    return v


def _cover_hero(c, box):
    x, y, w, h = box
    s = min(w / 860, h / 900)
    full = {k: -10.0 for k in GEO}
    with c.at(x + w / 2 - CXc, y + h / 2 - 1073, s, origin=(CXc, 1073)):
        skill_tree(c, _nodes(0.0, full), _edges(0.0, full))


# ── INTRO: name card 2020 → flipped to 'sekarang' → Morphs into the tree's root ──────────────────────────────
OLD = dict(role="System\nEngineer", task="jalanin yang disuruh", year="2020", level="LV 1")
NEW = dict(role="Senior Cloud\nEngineer", task="mutusin apa yang perlu dibikin", year="SEKARANG", level="LV 3")


def intro(v, T, s, e):
    v.chapter(None, "INTRO", s, e)
    L1, L2, L3 = T["L01"], T["L02"], T["L03"]
    t_in = L1.start - 0.3
    t_flip = _w(T, "L02", "Sekarang", 0.0) - 0.05
    t_m = L3.start + 0.4
    t_land = t_m + tk.SPRING["silk"][2]
    hs = _heads(T, [("Dulu: *jalanin*.", "L01"), ("Sekarang:\n*mutusin*.", "L02"), ("Ini *jalurnya*.", "L03")],
                e - DOUT)
    mo = Morph(CARD, r=28).to(t_m, ROOT_BOX, r=42)
    ccx, ccy = CARD[0] + CARD[2] / 2, CARD[1] + CARD[3] / 2

    def face(c, box, k):
        if k == 0:
            name_card(c, *box, color=RED, **NEW)
        else:
            x, y, w, h = box
            c.fill_rrect(x, y, w, h, min(w, h) / 2, RED)
            c.text(x + w / 2, y + h / 2 + 8, "2020", F["mono_bold"], 22, C["card"], 1, 0.06, align="c")

    def draw(c, t):
        kicker(c, t, L1.start, e - DOUT, "DULU → SEKARANG", RED)
        _draw_heads(c, t, hs)
        if t < t_m:
            k = spring_at(t, t_in, "silk")
            ang = math.pi * spring_at(t, t_flip, "silk")
            with c.group(min(1.0, k)), c.at(0, 90 * (1 - k)):
                with yaw(c, ccx, ccy, ang if ang < math.pi / 2 else ang - math.pi):
                    name_card(c, *CARD, color=RED, **(OLD if ang < math.pi / 2 else NEW))
        else:
            mo.draw(c, t, C["card"], face, shadow="card")
    v.add(s, t_land + 0.1, draw, z=20)
    _cam(v, t_flip - 0.2, ccy, 1.04)
    _cam(v, t_m, 1300, 1.0, dur=1.1)
    v.sfx("pop", t_in + 0.2, 0.5)
    v.sfx("whoosh", t_flip + 0.1, 0.6)
    v.sfx("whoosh", t_m, 0.5)
    v.sfx("pop", t_land - 0.2, 0.7)
    return t_land


# ── the persistent tree: ghost from the landing, tiers unlock on their words, dims out before 03 ─────────────
def tree(v, T, t_land, b, sched):
    s3 = b[CH[3]]
    t_dim0, t_dim1 = T["L10"].start, b[CH[2]] - 0.2           # LV 3 ghosts step back for the 'kenapa?' bubble

    def draw(c, t):
        a = out_cubic(prog(t, t_land - 0.2, 0.6)) * (1 - in_cubic(prog(t, s3 - 0.5, 0.6)))
        if a <= 0.002:
            return
        back = 1 - 0.75 * prog(t, t_dim0, 0.4) * (1 - prog(t, t_dim1, 0.4))
        skill_tree(c, _nodes(t, sched, {k: back for k in ("c0", "c1", "c2")}), _edges(t, sched), alpha=a)
    v.add(t_land - 0.2, s3 + 0.2, draw, z=5)
    for k, tu in sched.items():
        if k == "root":
            continue
        v.sfx("tick", tu - 0.35, 0.45)
        v.sfx("chime" if k.startswith("q") else "pop", tu, 0.7)


# ── 00 · SYSTEM ENGINEER (LV 1): tools unlock · LEVEL UP · decisions belong to someone else ─────────────────────
def lv1(v, T, s, e, sched):
    ch = v.chapter(0, "SYSTEM ENGINEER", s, e)
    L5, L7 = T["L05"], T["L07"]
    t_lv = _w(T, "L06", "naik", 0.6)
    t_ol = _w(T, "L07", "orang", 0.7)
    hs = _heads(T, [("Isinya *tools*.", "L04"), ("Rasanya\n*naik level*.", "L06"), ("Yang mutusin?\n*Orang lain*.", "L07")],
                e - DOUT)

    def draw(c, t):
        kicker(c, t, s + 0.15, e - DOUT, "LV 1 · 2020 · SYSTEM ENGINEER", ch.color)
        _draw_heads(c, t, hs)
        fade(c, t, t_lv, e - DOUT, lambda c: pop_tag(c, t, t_lv, CXc + 66, 1450, "LEVEL UP", RED))
        p = prog(t, t_ol, 0.6) * (1 - prog(t, e - DOUT, 0.4))
        if p > 0:
            with c.at(0, 0, 1, origin=(560, 800), rot=-0.035):
                note(c, 560, 800, "keputusan: orang lain", p, arrow_to=(CXc + 2, 738), size=40)
    v.add(s, e + 0.3, draw, z=20)
    _cam(v, L5.start - 0.2, 1280, 1.05)
    _cam(v, L7.start, 760, 1.02, dur=1.0)
    v.sfx("whoosh", s + 0.1, 0.6)
    v.sfx("pop", t_lv, 0.6)
    v.sfx("pop", t_ol, 0.4)


# ── 01 · CLOUD ENGINEER (LV 2): Kubernetes · multi-AZ · biaya ↓ — then a branch that is a question ─────────────
def lv2(v, T, s, e, sched):
    ch = v.chapter(1, "CLOUD ENGINEER", s, e)
    L9, L10 = T["L09"], T["L10"]
    t_k = _w(T, "L11", "kenapa", 0.5)
    hs = _heads(T, [("Masuk project\n*bank*.", "L08"), ("Cabangnya\n*beda*.", "L10"), ("Ditanya *kenapa*.", "L11")],
                e - DOUT)
    tail = (CXc + 15, 958)

    def draw(c, t):
        kicker(c, t, s + 0.15, e - DOUT, "LV 2 · 2021 · CLOUD ENGINEER", ch.color)
        _draw_heads(c, t, hs)
        out = 1 - in_cubic(prog(t, e - DOUT, 0.4))
        p = in_out_cubic(prog(t, L10.start + 0.2, 0.9))
        if p > 0 and out > 0:
            branch(c, CXc, 1080 - TH / 2, tail[0], tail[1] + 4, p, ghost=0.0, alpha=out)
        q = prog(t, t_k - 0.15, 0.4) * out
        bubble(c, tail[0], tail[1], "kenapa pilih ini?", q)
    v.add(s, e + 0.3, draw, z=20)
    _cam(v, L9.start - 0.2, 1080, 1.05)
    _cam(v, t_k - 0.3, 960, 1.07, dur=0.8)
    _cam(v, e - 0.7, 960, 1.0, dur=0.6)
    v.sfx("whoosh", s + 0.1, 0.6)
    v.sfx("tick", L10.start + 0.2, 0.5)
    v.sfx("pop", t_k - 0.15)


# ── 02 · SENIOR (LV 3): iris in · migrasi / serverless stack / mentoring · the top tier = questions ────────────
def lv3(v, T, s, e, sched):
    ch = v.chapter(2, "SENIOR", s, e)
    L13, L14 = T["L13"], T["L14"]
    t_open, t_close = s - 0.8, s + 0.05
    hs = _heads(T, [("Naik jadi\n*Senior*.", "L12"), ("Paling atas:\n*bukan tools*.", "L14"),
                    ("Isinya\n*pertanyaan*.", "L15")], e - DOUT)

    def wipe(c, t):
        if t < t_close:
            iris(c, t, t_open, CXc, 1080, RED, "open")
        else:
            iris(c, t, t_close, CXc, 880, RED, "close")
    v.add(t_open, t_close + 1.0, wipe, z=100)

    def draw(c, t):
        kicker(c, t, s + 0.3, e - DOUT, "LV 3 · SENIOR CLOUD ENGINEER", ch.color)
        _draw_heads(c, t, hs)
        pulse = prog(t, L14.start, 0.3) * (1 - prog(t, sched["q0"] - 0.3, 0.3))
        if pulse > 0:
            k = 0.5 + 0.5 * math.sin((t - L14.start) * 2 * math.pi * 1.6)
            for q in ("q0", "q1"):
                x, y, w, h = GEO[q][:4]
                c.stroke_rrect(x - w / 2 - 8, y - h / 2 - 8, w + 16, h + 16, 26, RED, 3, pulse * (0.3 + 0.5 * k),
                               dash=[10, 8])
    v.add(s, e + 0.3, draw, z=20)
    _cam(v, L13.start - 0.2, 880, 1.04)
    _cam(v, L14.start, 680, 1.07, dur=1.0)
    _cam(v, sched["q1"] + 0.5, 960, 1.0, dur=1.3)             # pull-out: the whole tree, topped by questions
    reel_sfx(v, "iris", t_open)
    v.sfx("whoosh", L14.start, 0.5)


# ── 03 · SALAH KAPRAH: certificates + tools fly in → struck → 'keputusan.' + highlighted 'dipercayain' ────────
def salah(v, T, s, e):
    ch = v.chapter(3, "SALAH KAPRAH", s, e)
    L16, L17 = T["L16"], T["L17"]
    t_c = _w(T, "L16", "sertifikat", 0.5) - 0.2
    t_kp = _w(T, "L17", "keputusan", 0.45)
    t_d = _w(T, "L17", "dipercayain", 0.65)
    t_h2 = max(L17.start + 1.0, t_kp - 0.1)
    h1 = Headline("Dulu aku kira:\n*tools* = level.")
    h2 = Headline("Ternyata:\n*dipercaya*.")
    soft = mix(RED, C["card"], 0.72)
    chips = [("sertifikat", RED, X, 640, -1), ("tools baru", ch.color, X + CW, 740, 1),
             ("sertifikat lagi", RED, X + 30, 860, -1), ("tools lagi", ch.color, X + CW - 20, 980, 1),
             ("+1 sertifikat", RED, X + 10, 1100, -1)]
    line = "yang dipercayain ke kamu."

    def draw(c, t):
        kicker(c, t, s + 0.15, e - DOUT, "03 · YANG DULU AKU SALAH", ch.color)
        h1.draw(c, t, L16.start, t_h2 - 0.5, strike_at=L17.start, reveal="mask", exit="dim")
        h2.draw(c, t, t_h2, e - DOUT, reveal="mask", exit="dim")
        float_chips(c, t, t_c, chips, t_out=L17.start + 0.1)
        out = 1 - in_cubic(prog(t, e - DOUT, 0.45))
        if t >= t_kp and out > 0:
            pa = out_back(prog(t, t_kp, 0.45))
            with c.at(0, 0, max(0.01, pa), origin=(X, 840)):
                word_pill(c, X, 770, "keputusan.", C["accent"], size=120, alpha=min(1.0, pa) * out)
            a = out_cubic(prog(t, t_kp + 0.3, 0.5)) * out
            if a > 0:
                with c.group(a):
                    highlight_phrase(c, t, t_d, X, 1060, line, "dipercayain", F["display"], 64, -0.04, color=soft)
                    c.text(X, 1060, line, F["display"], 64, C["ink"], 1, -0.04)
            p = prog(t, t_d + 0.6, 0.6) * out
            if p > 0:
                with c.at(0, 0, 1, origin=(X + 40, 1230), rot=-0.03):
                    note(c, X + 40, 1230, "bukan jumlah sertifikatnya", p, size=42)
    v.add(s, e + 0.3, draw, z=20)
    v.camera.key(t_kp, zoom=0.97, dur=0.3).key(t_kp + 0.35, zoom=1.0, dur=0.5)
    v.sfx("whoosh", s + 0.1, 0.6)
    reel_sfx(v, "chips", t_c, n=len(chips))
    v.sfx("click", L17.start, 0.7)
    v.sfx("thud", t_kp)
    reel_sfx(v, "highlight", t_d)


# ── RECAP (dark): mini tree — 'kamu di sini?' on LV 1, then the branches race up to the questions ───────────
def recap(v, T, s, e):
    v.chapter(None, "INTINYA", s, e, dark=True)
    L18 = T["L18"]
    t_m = _w(T, "L19", "mutusin", 0.85)
    hs = _heads(T, [("Masih di\n*cabang pertama*.", "L18"), ("Jalanin dulu.\nNanti *mutusin*.", "L19")], e - OUT,
                style="headline_dark")
    sched = {"root": s - 1, "a0": s - 1, "a1": s - 1, "a2": s - 1}
    for i, tier in enumerate(("b", "c", "q")):
        for k in GEO:
            if k.startswith(tier):
                sched[k] = t_m + 0.15 + 0.3 * i
    S, OY = 0.72, 1100

    def draw(c, t):
        _draw_heads(c, t, hs)
        a = out_cubic(prog(t, s + 0.2, 0.6)) * (1 - in_cubic(prog(t, e - OUT, OUT)))
        if a <= 0.002:
            return
        with c.group(a), c.at(0, 0, S, origin=(CXc, OY)):
            skill_tree(c, _nodes(t, sched), _edges(t, sched))
        p = prog(t, L18.start + 0.6, 0.6) * (1 - prog(t, t_m, 0.4))
        if p > 0:
            note(c, X + 20, 1480, "kamu di sini?", p * a, arrow_to=(CXc - DX * S, OY + 180 * S + 40), size=42)
    v.add(s, e, draw, z=20)
    v.camera.key(s, zoom=1.0, dur=0.01).key(s + 0.1, zoom=1.04, y=1000, dur=max(1.0, e - s - 0.6))
    v.sfx("whoosh_dark", s)
    v.sfx("pop", L18.start + 0.6, 0.5)
    for i in range(3):
        v.sfx("tick", t_m + 0.15 + 0.3 * i - 0.35, 0.5)
    v.sfx("chime", t_m + 0.75)
