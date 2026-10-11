"""Look lab — proof sheet for STYLE §6g (material layer) + the big-hero rule. Not for posting.

One scene, drawn four times: a drop leaves the rain, rides the drop cable down to the ODP box, slips through the gap
under its lifted lid and lands on the splice — the light in the fiber dims. 01 SEBELUM = how every video looked
(small hero, flat, empty frame) · 02 BESAR = the same drawing grows until it fills the frame and crops ·
03 CAHAYA = look "lit" · 04 KERTAS = look "paper". The hero never leaves: between chapters it dissolves to the next
take (shared element), and the look changes ON the spoken word. OUTRO = the three looks side by side.
Only look= and the scale change — that is the point. `check look-lab --dry` should be flag-free.
"""
import math

from engine import Video, tokens as tk
from engine.ease import clamp, curve, lerp, mix, prog
from engine.video import draw_background
from engine.components import (Headline, kicker, brand_intro, arrive, follow, presence, rise, dolly, cut, pop_tag,
                               land, squash, along, tetes, material as mat)

L, M, C, F = tk.L, tk.M, tk.C, tk.F
X, CW = L["col_x"], L["col_w"]
PRE_ROLL = 2.05
LEAD = 0.5                 # chapter visuals start this long before the chapter's first line
OUT = M["quiet_out"]
TAIL = 2.6
XF = 0.6                   # take-to-take dissolve at a chapter boundary
XL = 0.9                   # look change (flat → lit → paper), centred on the spoken word
NAMES = ("INTRO", "01 · SEBELUM", "02 · BESAR", "03 · CAHAYA", "04 · KERTAS", "OUTRO")
TEAL = tk.CHAPTER[4][0]    # signature: water + the light in the fiber
SMALL = (540, 760, 330)    # (cx, y0, w) of the box — the old small hero
BIG = (480, 545, 840)      # fills the frame, crops at the bottom and the right
RIDE, SLIP, FALL_IN, FALL = 0.8, 0.1, 0.35, 0.5


def build(project):
    T = project.timing
    v = Video(duration=T.line("L09").end + TAIL, bpm=84, beat_offset=0.0)
    v.series = "LOOK LAB"
    brand_intro(v, version=2)
    v.music = dict(style="ambient", key="D", mood="dreamy")
    v.sfx_kit = "glass"
    b = [max(0.0, T.chapter_span(n)[0] - LEAD) for n in NAMES] + [v.duration]
    b[0] = 0.0
    for i in range(6):
        v.chapter(i if 0 < i < 5 else None, NAMES[i].split(" · ")[-1], b[i], b[i + 1])
    lands = {1: T.word("L02", "ini", 1), 2: T.word("L03", "ngisi"), 3: T.word("L06", "tetesnya"),
             4: T.word("L07", "digunting")}
    sw = {3: T.word("L05", "cahaya") - XL / 2, 4: T.word("L07", "kertas") - XL / 2}
    S = Story(T, b, lands, sw)

    v.stage = lambda c, t: _stage(v, S, c, t)
    v.finish = lambda c, t: (mat.finish(c, "lit", S.amount("lit", t)), mat.finish(c, "paper", S.amount("paper", t)))
    intro(v, T, b[0], b[1])
    v.add(b[1], b[5], lambda c, t: S.draw(c, t), bleed=True)
    for i, (head, label) in enumerate((("Kecil,\n*jauh*.", "01 · SEBELUM · FLAT"),
                                       ("Sama, tapi *dekat*.", "02 · BESAR · FLAT"),
                                       ("Dikasih *cahaya*.", "03 · CAHAYA · LIT"),
                                       ("Digunting *kertas*.", "04 · KERTAS · PAPER")), start=1):
        _title(v, b[i], b[i + 1], head, label, tk.CHAPTER[i][0])
        cut(v, b[i])
        v.sfx("pop", lands[i])
        v.sfx("tick", S.hit(i))
        dolly(v, S.hit(i) + 0.9, b[i + 1] - 0.2)
    outro(v, T, S, b[5], v.duration)
    v.cover_t = S.hit(3) + 0.8
    return v


# ── the hero, one continuous object across chapters 01–04 ───────────────────────────────────────────────────────
def geo(cx, y0, w):
    """Box geometry (centre x, top y, width). Everything — cable, gap, splice — is relative, so it scales as one."""
    h = w * 1.3
    x0 = cx - w / 2
    ix, iy, iw, ih = x0 + w * 0.09, y0 + h * 0.13, w * 0.82, h * 0.66
    tx, ty, tw, th = ix + iw * 0.08, iy + ih * 0.1, iw * 0.84, ih * 0.62
    gap = (x0 + w * 0.93, y0 + h * 0.01)
    p0, n = (x0 + w * 1.3, y0 - w * 0.8), 14
    cable = [(p0[0] + (gap[0] - p0[0]) * k / n, p0[1] + (gap[1] - p0[1]) * k / n + w * 0.32 * (k / n) * (1 - k / n))
             for k in range(n + 1)]
    return dict(cx=cx, x0=x0, y0=y0, w=w, h=h, win=(ix, iy, iw, ih), tray=(tx, ty, tw, th),
                sx=[tx + tw * f for f in (0.3, 0.5, 0.7)], sy=ty + th * 0.5,
                cap=(cx - w * 0.54, y0 - h * 0.06, w * 1.08, h * 0.1), gap=gap, cable=cable,
                entry=(ix + iw * 0.86, iy + ih * 0.03),
                pole=(cx - w * 0.07, y0 - h * 0.2, w * 0.14, h * 1.2 + w * 0.9),
                outs=[[(cx + dx * w, y0 + h - 2), (cx + dx * w * 1.5, y0 + h + w * 0.55)] for dx in (-0.18, 0.0, 0.18)])


def _part(c, look, seed, box):
    """Paper look: each cut-out part is placed a touch off-square, by hand."""
    x, y, w, h = box
    return c.at(0, 0, 1, origin=(x + w / 2, y + h / 2), rot=mat.tilt(look, seed))


def odp_hero(c, t, look, g, wet=0.0, lum=1.0):
    """The ODP box close-up in a look: pole, cables out, body, cut-open window with the splice tray, fiber loops,
    sleeves, pooled water, the drop cable coming in, and the lid lifted at the right (the gap)."""
    w, h, x0, y0, cx = g["w"], g["h"], g["x0"], g["y0"], g["cx"]
    lw = max(2.5, w * 0.012)
    px, py, pw, ph = g["pole"]
    mat.body(c, look, mat.rrect_path(px, py, pw, ph, pw * 0.2), (px, py, pw, ph),
             mix(C["muted"], C["faint"], 0.4), form="cyl", shadow=False)
    for k, pts in enumerate(g["outs"]):
        mat.cable(c, look, pts, w * 0.026, TEAL if k == 1 else C["ink2"], 1.0 if k != 1 else 0.4 + 0.6 * lum)
    mat.body(c, look, mat.rrect_path(x0, y0, w, h, w * 0.06), (x0, y0, w, h), C["ink2"], r=w * 0.06)
    ix, iy, iw, ih = g["win"]
    win = mat.rrect_path(ix, iy, iw, ih, w * 0.035)
    with _part(c, look, 1, g["win"]):
        mat.body(c, look, win, g["win"], C["card"], shadow=False)
        mat.inset(c, look, win, g["win"])
        tx, ty, tw, th = g["tray"]
        tray = mat.rrect_path(tx, ty, tw, th, w * 0.03)
        mat.body(c, look, tray, g["tray"], C["bg"], shadow=look == "paper", lift=0.4)
        mat.inset(c, look, tray, g["tray"])
        for k in range(2):                                                                     # fiber loops
            m = w * (0.05 + 0.05 * k)
            col = mix(C["faint"], TEAL, 0.25 + 0.75 * lum)
            if look == "lit":
                c.stroke_rrect(tx + m, ty + m, tw - 2 * m, th - 2 * m, (th - 2 * m) * 0.45, TEAL, lw * 4, 0.12 * lum)
            elif look == "paper":
                c.stroke_rrect(tx + m, ty + m + lw * 0.8, tw - 2 * m, th - 2 * m, (th - 2 * m) * 0.45,
                               C["brand_ink"], lw, tk.LOOK["paper"]["stack_alpha"])
            c.stroke_rrect(tx + m, ty + m, tw - 2 * m, th - 2 * m, (th - 2 * m) * 0.45, col, lw, 0.9)
        sy = g["sy"]
        mat.spill(c, look, g["sx"][1], sy, w * 0.18, TEAL, lum)
        for k, x_ in enumerate(g["sx"]):                                                        # splice sleeves
            sb = (x_ - w * 0.055, sy - w * 0.022, w * 0.11, w * 0.044)
            mat.body(c, look, mat.rrect_path(*sb, w * 0.022), sb, TEAL if k == 1 else C["muted"],
                     0.35 + 0.65 * lum if k == 1 else 0.85, shadow=look != "flat", lift=0.3)
        if wet > 0.01:                                                                          # pooled water
            wh = ih * 0.22 * clamp(wet)
            amp = w * 0.008 * (1 - clamp(wet))
            pts = [(ix, iy + ih)] + [(ix + iw * k / 24, iy + ih - wh + amp * ((k * 7) % 5 - 2) / 2)
                                     for k in range(25)] + [(ix + iw, iy + ih)]
            with c.clip(ix, iy, iw, ih, w * 0.035):
                mat.body(c, look, mat.poly_path(pts), (ix, iy + ih - wh, iw, wh), TEAL,
                         0.32 if look == "flat" else 0.45, shadow=False)
            for k, (dx, dy) in enumerate(((-0.03, -0.035), (0.04, 0.03), (0.0, 0.045))):      # beads
                a = clamp(wet * 3 - k)
                if a > 0:
                    _drop(c, look, g["sx"][1] + w * dx, sy + w * dy, w * 0.05, 0.0, 0.0, a)
    with _part(c, look, 2, (cx - w * 0.2, y0 + h * 0.84, w * 0.4, h * 0.1)):
        c.text(cx, y0 + h * 0.9, "ODP", F["mono_bold"], max(17, w * 0.075), C["card"], 0.9, 0.2, align="c")
    mat.cable(c, look, g["cable"], w * 0.022, C["ink2"])                                       # drop cable in
    capx, capy, capw, caph = g["cap"]
    with c.at(0, 0, 1, origin=(capx, capy + caph), rot=-0.16 + mat.tilt(look, 3)):              # lid, lifted
        mat.body(c, look, mat.rrect_path(capx, capy, capw, caph, caph * 0.35), g["cap"], C["ink"],
                 r=caph * 0.35, lift=0.5)


def _drop(c, look, x, y, s, stretch, sq, alpha):
    """One drop in a look. flat = the component every video used (tetes); lit/paper = material body."""
    if alpha <= 0.002:
        return
    with squash(c, x, y + s * 0.34, sq):
        if look == "flat":
            tetes(c, x, y, s, TEAL, alpha, stretch)
        else:
            mat.body(c, look, mat.drop_path(x, y, s, stretch), mat.drop_box(x, y, s, stretch), TEAL, alpha,
                     form="drop", lift=0.35)


class Story:
    """Chapter takes of the one hero: geometry, look, drop phase, water and light — all pure functions of t."""

    def __init__(self, T, b, lands, sw):
        self.T, self.b, self.lands, self.sw = T, b, lands, sw

    def hit(self, i):
        return self.lands[i] + RIDE + SLIP + FALL_IN

    def amount(self, look, t):
        """How much of the frame is in `look` (stage, finish): lit from the switch in 03, paper from the one in 04."""
        k = curve("apple_in_out")
        if look == "lit":
            return k(prog(t, self.sw[3], XL)) * (1 - k(prog(t, self.sw[4], XL)))
        return k(prog(t, self.sw[4], XL)) * (1 - k(prog(t, self.b[5] - XF / 2, XF)))

    def geo(self, i, t):
        if i == 1:
            return geo(*SMALL)
        if i == 2:
            mv, _ = presence(t, arrive(self.T.word("L03", "dibesarin"), "hero"), None, "hero")
            return geo(*(lerp(a, z, mv) for a, z in zip(SMALL, BIG)))
        return geo(*BIG)

    def take(self, c, t, i):
        """Chapter i's take at time t, with its look change (03, 04) dissolving on the word."""
        g = self.geo(i, t)
        if i in self.sw:
            p = curve("apple_in_out")(prog(t, self.sw[i], XL))
            old, new = ("flat", "lit") if i == 3 else ("lit", "paper")
            if p < 1:
                self.render(c, t, i, g, old)
            if p > 0:
                with c.group(p):
                    self.render(c, t, i, g, new)
            return
        self.render(c, t, i, g, "flat")

    def render(self, c, t, i, g, look):
        t_land = self.lands[i]
        t_hit = self.hit(i)
        wet = curve("apple_out")(prog(t, t_hit, 1.0))
        flick = 0.5 + 0.5 * math.sin(t * 23.0) * math.sin(t * 7.3)
        lum = 1.0 - 0.55 * wet - 0.3 * flick * clamp(wet * 4) * (1 - prog(t, t_hit + 0.6, 0.6))
        odp_hero(c, t, look, g, wet, lum)
        w, s = g["w"], g["w"] * 0.1
        f0 = 0.55
        x0, y0, _ = along(g["cable"], f0)
        lift = s * 0.34 + w * 0.011
        if t_land - FALL <= t < t_land:                                                         # falling
            p = prog(t, t_land - FALL, FALL)
            _drop(c, look, x0, lerp(y0 - w * 0.7, y0, p * p) - lift, s, 0.6 * p, 0.0, clamp(p * 5))
        elif t_land <= t < t_land + RIDE + SLIP:                                                # riding the cable
            p = prog(t, t_land, RIDE)
            x, y, _ = along(g["cable"], f0 + (1 - f0) * p ** 1.7)
            a = 1 - prog(t, t_land + RIDE, SLIP)
            _drop(c, look, x, y - lift, s * (1 - 0.35 * (1 - a)), 0.0, land(t, t_land), a)
        elif t_land + RIDE + SLIP <= t < t_hit:                                                 # inside, falling
            p = prog(t, t_land + RIDE + SLIP, FALL_IN)
            ex, ey = g["entry"]
            _drop(c, look, lerp(ex, g["sx"][1], p), lerp(ey, g["sy"] - s * 0.4, p * p), s * 0.6, 0.5 * p, 0.0,
                  clamp(p * 6))
            mat.caustic(c, look, g["sx"][1], g["sy"], w * 0.08 * p, TEAL, p)

    def draw(self, c, t):
        b = self.b
        _, op = presence(t, b[1] + 0.1, b[5] - OUT, "hero")
        with c.group(op):
            for k in (2, 3, 4):                                                                 # take-to-take dissolve
                if b[k] - XF / 2 <= t < b[k] + XF / 2:
                    p = curve("apple_in_out")(prog(t, b[k] - XF / 2, XF))
                    self.take(c, t, k - 1)
                    with c.group(p):
                        self.take(c, t, k)
                    return
            i = max(k for k in (1, 2, 3, 4) if b[k] <= t) if t >= b[1] else 1
            self.take(c, t, i)


def _stage(v, S, c, t):
    """Default background, then the lit studio / paper ground as the look changes, and rain behind the hero."""
    draw_background(c, v, t)
    a_lit, a_paper = S.amount("lit", t), S.amount("paper", t)
    mat.stage(c, "lit", TEAL, a_lit)
    mat.stage(c, "paper", TEAL, a_paper)
    b = S.b
    d = curve("apple_out")(prog(t, b[1], 0.8)) * (1 - curve("apple_in")(prog(t, b[5] - OUT, 0.6)))
    box = (0, 0, tk.W, tk.H)
    mat.rain(c, t, "flat", box, mix(C["muted"], TEAL, 0.35), d, alpha=1 - a_lit - a_paper)
    mat.rain(c, t, "lit", box, TEAL, d, alpha=a_lit)
    mat.rain(c, t, "paper", box, TEAL, d, alpha=a_paper)


def _title(v, s, e, text, label, col):
    h = Headline(text)

    def draw(c, t):
        kicker(c, t, s + 0.15, e - OUT, label, col)
        h.draw(c, t, s + 0.25, e - OUT, reveal="rise", exit="quiet")
    v.add(s, e, draw)


# ── INTRO: type is the hero; one lit drop lands on the word ──────────────────────────────────────────────────────
def intro(v, T, s, e):
    h = Headline("Satu adegan.\nEmpat *cara*.", y=640, style="headline_lg")
    t_h = arrive(T["L01"].start + 0.25)
    t_land = T.word("L01", "sama", 1)
    cy, dx, s_ = 1010, X + CW * 0.42, 110

    def draw(c, t):
        kicker(c, t, s + 0.3, e - OUT, "LOOK LAB · STYLE §6g", TEAL)
        h.draw(c, t, t_h, e - OUT, reveal="rise", exit="quiet")
        mv, op = presence(t, arrive(T.word("L01", "tetes")), e - OUT)
        with c.group(op):
            mat.cable(c, "lit", [(X, cy + 18), (X + CW * 0.8, cy + 50)], 16, C["ink2"])
            if t >= t_land - FALL:
                p = prog(t, t_land - FALL, FALL)
                y = lerp(cy - 520, cy - s_ * 0.34 - 4 + 22, p * p)
                with squash(c, dx, y + s_ * 0.34, land(t, t_land)):
                    mat.body(c, "lit", mat.drop_path(dx, y, s_, 0.6 * (1 - prog(t, t_land, 0.2))),
                             mat.drop_box(dx, y, s_), TEAL, clamp(p * 5), form="drop", lift=0.3)
                mat.caustic(c, "lit", dx + 6, cy + 30, s_, TEAL, prog(t, t_land, 0.4))
    v.add(s, e, draw)
    v.sfx("pop", t_land)
    dolly(v, t_land + 0.9, e - 0.2)


# ── OUTRO: the three looks side by side, one leader + followers ──────────────────────────────────────────────────
def outro(v, T, S, s, e):
    L9 = T["L09"]
    h = Headline("Kamu pilih\n*yang mana*?")
    gap = 24
    tw, th, ty = (CW - 2 * gap) / 3, 560, 640
    t_lead = arrive(T.word("L09", "gambarnya"))
    looks = (("flat", "02", "BESAR"), ("lit", "03", "CAHAYA"), ("paper", "04", "KERTAS"))

    def tile(c, i, look, num, name):
        x = X + i * (tw + gap)
        c.shadow(x, ty, tw, th, L["radius_bento"], 34, 14, 0.08)
        with c.clip(x, ty, tw, th, L["radius_bento"]):
            c.fill_rrect(x, ty, tw, th, 0, C["card"])
            mat.stage(c, look, TEAL)
            g = geo(x + tw * 0.46, ty + 120, tw * 0.62)
            odp_hero(c, 0.0, look, g, 1.0, 0.45)
            mat.finish(c, look)
        c.stroke_rrect(x + 0.5, ty + 0.5, tw - 1, th - 1, L["radius_bento"], C["line"], 1)
        c.text(x + 4, ty + th + 64, num, F["display"], 54, C["ink"], 1, -0.04)
        c.text(x + 4, ty + th + 104, name, F["mono_med"], 22, C["ink2"], 1, 0.16)

    def draw(c, t):
        kicker(c, t, s + 0.15, e, "OUTRO · PILIH LOOK", TEAL)
        h.draw(c, t, L9.start - 0.1, None, reveal="rise")
        for i, (look, num, name) in enumerate(looks):
            ti = t_lead if i == 0 else follow(t_lead, i)
            dy = M["rise_dy"] * 2 * (1 if i == 0 else M["follow_amp"])
            rise(c, t, ti, None, (X + i * (tw + gap), ty, tw, th + 110),
                 lambda c, i=i, look=look, num=num, name=name: tile(c, i, look, num, name), dy=dy)
        pop_tag(c, t, follow(t_lead, 5), X, ty + th + 150, "tulis 02 / 03 / 04 di komentar", TEAL)
    v.add(s, e, draw)
    v.sfx("pop", T.word("L09", "gambarnya"))
    dolly(v, follow(t_lead, 8), e - 0.2)
