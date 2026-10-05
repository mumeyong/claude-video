"""The persistent 'Tanya Claude Code...' input at the bottom + context chips.

Usage (in build):
    chat = ChatTrack()
    chat.show(2.0)
    chat.chips([("CLAUDE.md", "green"), ("skill", "purple")], at=30.0)
    chat.type("bikinin video kayak kemarin", at=t0)
    chat.send(at=t1)               # press + ripple, text clears
    chat.dim(at=118, amount=0.6)   # fade back while cards take focus
    video.chat = chat
"""
from gi.repository import Pango

from .. import tokens as tk
from ..ease import out_expo, in_cubic, prog, pulse, in_out_cubic
from . import icons
from .motion import typed, type_cues
from .pill import chip, chip_width


class ChatTrack:
    def __init__(self, placeholder=tk.CHAT_PLACEHOLDER):
        self.placeholder = placeholder
        self.ev = []  # (t, kind, payload)

    # events ----------------------------------------------------------------
    def _add(self, t, kind, payload=None):
        self.ev.append((float(t), kind, payload))
        self.ev.sort(key=lambda e: e[0])
        return self

    def show(self, at): return self._add(at, "show")
    def hide(self, at): return self._add(at, "hide")
    def send(self, at): return self._add(at, "send")
    def clear(self, at): return self._add(at, "clear")
    def dim(self, at, amount=0.6): return self._add(at, "dim", amount)
    def chips(self, items, at): return self._add(at, "chips", list(items))

    def type(self, text, at, cps=None):
        return self._add(at, "type", (text, cps or tk.M["type_cps"]))

    def cues(self):
        out = []
        for t, kind, pl in self.ev:
            if kind == "type":
                out += type_cues(pl[0], t, pl[1])
            elif kind == "send":
                out += [("click", t, 0.8), ("send", t + 0.03, 0.6)]
            elif kind == "chips" and pl:
                out += [("pop", t + i * 0.08, 0.4) for i in range(len(pl))]
        return out

    def send_point(self):
        """Center of the send button (for cursor paths)."""
        L = tk.L
        return L["col_x"] + L["col_w"] - 52, L["chat_y"] + L["chat_h"] - 46

    # state -----------------------------------------------------------------
    def _last(self, t, kinds):
        best = None
        for e in self.ev:
            if e[0] > t:
                break
            if e[1] in kinds:
                best = e
        return best

    def _visible(self, t):
        e = self._last(t, ("show", "hide"))
        if e is None:
            return 0.0
        prev = [x for x in self.ev if x[1] in ("show", "hide") and x[0] < e[0]]
        if e[1] == "show":
            return out_expo(prog(t, e[0], 0.6))
        was = 1.0 if prev and prev[-1][1] == "show" else 0.0
        return was * (1 - in_cubic(prog(t, e[0], 0.4)))

    def _text_state(self, t):
        """(text, partial, partial_alpha, clearing 0..1, typing?)"""
        e = self._last(t, ("type", "send", "clear"))
        if e is None or e[1] != "type":
            if e is not None:
                # just sent/cleared: fade out the previous text
                prev = self._last(e[0] - 1e-6, ("type",))
                if prev and t - e[0] < 0.35:
                    txt = prev[2][0]
                    return txt, "", 0.0, prog(t, e[0], 0.35), False
            return "", "", 0.0, 0.0, False
        text, cps = e[2]
        full, part, pa, done = typed(text, t, e[0], cps)
        return full, part, pa, 0.0, not done

    # draw ------------------------------------------------------------------
    def draw(self, c, t):
        vis = self._visible(t)
        if vis <= 0.002:
            return
        d = self._last(t, ("dim",))
        dim = 1.0
        if d:
            prev_dim = [x for x in self.ev if x[1] == "dim" and x[0] < d[0]]
            a0 = 1 - (prev_dim[-1][2] if prev_dim else 0.0)
            dim = a0 + ((1 - d[2]) - a0) * in_out_cubic(prog(t, d[0], 0.5))
        L, F = tk.L, tk.F
        x, w = L["col_x"], L["col_w"]
        y0, h0 = L["chat_y"], L["chat_h"]
        rise = 40 * (1 - vis)
        text, part, pa, clearing, typing = self._text_state(t)
        size, ls, lh = tk.T["chat"]
        # height grows upward with multi-line text (smoothed by sampling the past)
        hs = []
        for k in range(4):
            tt, pp, _, _, _ = self._text_state(t - k * 0.04)
            hh = c.extents(c.layout(tt + pp or " ", F["ui_reg"], size, ls, width=w - 60))[1]
            hs.append(max(h0, hh + 104))
        h = sum(hs) / len(hs)
        y = y0 + h0 - h

        with c.group(vis * dim):
            with c.at(0, rise):
                # chips row
                ce = self._last(t, ("chips",))
                if ce and ce[2]:
                    cx = x + 6
                    for i, (label, col) in enumerate(ce[2]):
                        p = out_expo(prog(t, ce[0] + i * 0.08, 0.45))
                        cw = chip_width(c, label)
                        if p > 0.002:
                            with c.at(0, 14 * (1 - p), 0.9 + 0.1 * p, origin=(cx + cw / 2, y - 42)):
                                chip(c, cx, y - 62, label, tk.CHIP.get(col, col), p)
                        cx += cw + 12
                sh = tk.SHADOW["chat"]
                c.shadow(x, y, w, h, L["radius_chat"], sh["blur"], sh["dy"], sh["alpha"])
                c.fill_rrect(x, y, w, h, L["radius_chat"], c.theme("card", "d_card"))
                c.stroke_rrect(x + 0.5, y + 0.5, w - 1, h - 1, L["radius_chat"], c.theme("line", "d_line"))
                # text or placeholder
                tx, ty = x + 32, y + 50
                if text or part:
                    a = 1 - clearing
                    lay_w = w - 60
                    c.text(tx, ty + 6 - 10 * clearing, text, F["ui_reg"], size, c.theme("ink", "d_ink"), a, ls, width=lay_w)
                    # caret + fading-in next char, measured on the last line
                    lay = c.layout(text or " ", F["ui_reg"], size, ls, width=lay_w)
                    line = lay.get_line_count() - 1
                    xpos = lay.get_line(line).index_to_x(len(text.encode()), False) / Pango.SCALE if text else 0
                    _, line_h, _ = c.extents(c.layout("Ag", F["ui_reg"], size, ls))
                    cy = ty + 6 + line * line_h
                    if part:
                        c.text(tx + xpos, cy, part, F["ui_reg"], size, c.theme("accent", "d_accent"), pa * a, ls)
                    if typing or (t * 1.6) % 1 < 0.5:
                        c.fill_rrect(tx + xpos + 2, cy - size * 0.82, 2.5, size * 1.0, 1, c.theme("accent", "d_accent"), a)
                else:
                    c.text(tx, ty + 6, self.placeholder, F["ui_reg"], size, c.theme("muted", "d_muted"), 1, ls)
                # tool icons
                iy = y + h - 46
                muted = c.theme("muted", "d_muted")
                c.circle(x + 40, iy, 17, c.theme("bg", "d_bg"))
                icons.plus(c, x + 40, iy, 15, c.theme("ink2", "d_ink"), 2)
                icons.paperclip(c, x + 88, iy, 22, muted)
                icons.mic(c, x + 132, iy, 22, muted)
                icons.globe(c, x + 176, iy, 22, muted)
                icons.bulb(c, x + 218, iy, 24, muted)
                # send button: idle soft, active solid, press pulse on send
                bx, by = x + w - 52, iy
                se = self._last(t, ("send",))
                press = pulse(t, se[0], 0.25) if se else 0.0
                active = 1.0 if (text or part) and clearing == 0 else 0.0
                r = 25 * (1 - 0.12 * press)
                c.circle(bx, by, r, c.theme("accent_soft", "d_card"), 1 - active)
                c.circle(bx, by, r, c.theme("accent", "d_accent"), active)
                icons.arrow_up(c, bx, by, 18, (1, 1, 1, 1) if active else c.theme("accent", "d_accent"), 2.6)
                if se:
                    rp = prog(t, se[0], 0.6)
                    if 0 < rp < 1:
                        c.ctx.new_path()
                        c.ctx.arc(bx, by, 25 + 40 * out_expo(rp), 0, 6.2832)
                        c.src(c.theme("accent", "d_accent"), 0.5 * (1 - rp))
                        c.ctx.set_line_width(3)
                        c.ctx.stroke()
