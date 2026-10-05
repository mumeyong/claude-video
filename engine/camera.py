"""Virtual camera over the content layers (z < 80). HUD, chips row (z >= 80) and background stay put.

    cam = v.camera
    cam.key(t, zoom=1.15, x=540, y=950, dur=0.01)   # cut in tight
    cam.key(t + 0.1, zoom=1.0, dur=1.6)              # slow pull-out to neutral
    cam.focus(t, (x, y, w, h), zoom=1.06)            # push toward a box

State = (zoom, fx, fy): design point (fx, fy) is placed at screen center, scaled by zoom.
Neutral = (1.0, 540, 960). Each key eases from the previous state over `dur`.
"""
from . import tokens as tk
from .ease import in_out_cubic, lerp, prog

NEUTRAL = (1.0, tk.W / 2, tk.H / 2)


class Camera:
    def __init__(self):
        self.keys = []  # (t, dur, zoom, fx, fy, ease)

    def key(self, t, zoom=1.0, x=None, y=None, dur=0.8, ease=in_out_cubic):
        x = tk.W / 2 if x is None else x
        y = tk.H / 2 if y is None else y
        self.keys.append((float(t), float(dur), zoom, x, y, ease))
        self.keys.sort(key=lambda k: k[0])
        return self

    def focus(self, t, box, zoom=1.06, dur=0.8, ease=in_out_cubic):
        x, y, w, h = box
        return self.key(t, zoom, x + w / 2, y + h / 2, dur, ease)

    def reset(self, t, dur=0.8, ease=in_out_cubic):
        return self.key(t, 1.0, None, None, dur, ease)

    def state(self, t):
        z, fx, fy = NEUTRAL
        for (kt, d, kz, kx, ky, e) in self.keys:
            if t < kt:
                break
            p = e(prog(t, kt, d))
            z, fx, fy = lerp(z, kz, p), lerp(fx, kx, p), lerp(fy, ky, p)
        return z, fx, fy

    def apply(self, ctx, t):
        z, fx, fy = self.state(t)
        if abs(z - 1) < 1e-4 and abs(fx - NEUTRAL[1]) < 0.05 and abs(fy - NEUTRAL[2]) < 0.05:
            return
        ctx.translate(tk.W / 2, tk.H / 2)
        ctx.scale(z, z)
        ctx.translate(-fx, -fy)
