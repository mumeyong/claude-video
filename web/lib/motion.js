// Motion primitives for HTML films (cheese + grak, refs.pdf). Everything is a pure function of time,
// so window.seek(t) can paint any frame without simulating the ones before it.
//
//   import { spring, track, trackObj, stagger, pulse, rng, noise1, cursor, SNAPPY } from '/web/lib/motion.js';

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, p) => a + (b - a) * p;
export const mix = (a, b, p) => a + (b - a) * clamp(p);
export const mapRange = (x, a, b, c = 0, d = 1) => lerp(c, d, clamp((x - a) / (b - a)));

// Spring presets: stiffness k, damping d (unit mass). spring(t, 'snappy') or spring(t, ...SNAPPY).
export const SPRINGS = {
  snappy: { k: 320, d: 30 },  // buttons, toggles, leading edges — hair of overshoot
  default: { k: 170, d: 26 }, // cards, containers, camera
  heavy: { k: 90, d: 20 },    // big type, logo lockups — no visible overshoot
  playful: { k: 260, d: 14 }, // mascots, stickers — visible overshoot
};
export const SNAPPY = [320, 30], DEFAULT = [170, 26], HEAVY = [90, 20], PLAYFUL = [260, 14];
const preset = (k, d) => (typeof k === 'string' ? SPRINGS[k] : { k, d });

// Closed-form damped spring from 0 to 1, starting at t = 0 at rest.
export function spring(t, k = 170, d = 26) {
  if (typeof k === 'string') ({ k, d } = SPRINGS[k]);
  if (t <= 0) return 0;
  const w0 = Math.sqrt(k), z = d / (2 * w0);
  if (z < 1) {
    const wd = w0 * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + ((z * w0) / wd) * Math.sin(wd * t));
  }
  if (z === 1) return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
  const s = w0 * Math.sqrt(z * z - 1), r1 = -z * w0 + s, r2 = -z * w0 - s;
  return 1 - (r2 * Math.exp(r1 * t) - r1 * Math.exp(r2 * t)) / (r2 - r1);
}

// Time until the spring stays within `eps` of 1 (sampled, cached) — budget holds with it.
const settleCache = new Map();
export function settleTime(k = 170, d = 26, eps = 0.002) {
  ({ k, d } = preset(k, d));
  const key = `${k}|${d}|${eps}`;
  if (settleCache.has(key)) return settleCache.get(key);
  let last = 0;
  for (let t = 0; t < 10; t += 1 / 240) if (Math.abs(1 - spring(t, k, d)) > eps) last = t;
  const T = Math.ceil((last + 1 / 240) * 240) / 240;
  settleCache.set(key, T);
  return T;
}

// A value that changes target many times. keys: [[time, value], ...] sorted by time.
// One spring per change, summed — continuous motion, still a pure function of t.
export function track(t, keys, k = 170, d = 26) {
  ({ k, d } = preset(k, d));
  let v = keys[0][1];
  for (let i = 1; i < keys.length; i++) v += (keys[i][1] - keys[i - 1][1]) * spring(t - keys[i][0], k, d);
  return v;
}

// Multi-dimensional track: keys [[time, {x, y, w, ...}], ...]
export function trackObj(t, keys, k, d) {
  const out = {};
  for (const prop of Object.keys(keys[0][1])) out[prop] = track(t, keys.map(([kt, v]) => [kt, v[prop]]), k, d);
  return out;
}

// Tab indicator that stretches: leading edge stiffer than trailing edge.
export function indicator(t, stops, width = 120) {
  const lead = track(t, stops, 320, 30), trail = track(t, stops, 140, 22);
  return { left: Math.min(lead, trail), right: Math.max(lead, trail) + width };
}

// Text inside a morphing container: in after the morph starts, out before it ends.
export function swapAlpha(t, tIn, tOut, fade = 0.12) {
  return Math.min(clamp((t - tIn - 0.08) / fade), clamp((tOut - 0.1 - t) / fade));
}

// Staggered spring for item i of a group.
export const stagger = (t, i, gap = 0.04, k, d) => spring(t - i * gap, k, d);

// Seamless loop time.
export const loopT = (t, dur) => ((t % dur) + dur) % dur;

// Seeded noise (mulberry32). Never Math.random: the render must be identical every run.
export function rng(seed = 1) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Smooth 1D value noise, deterministic in (x, seed) — slow drifts, hand wobble.
export function noise1(x, seed = 0) {
  const h = (n) => { const r = rng((n * 374761393 + seed * 668265263) | 0); return r() * 2 - 1; };
  const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f);
  return lerp(h(i), h(i + 1), u);
}

// 1 on each time in `times`, decaying to 0 — pulses that hit with the music (FILM.beats).
export function pulse(t, times, decay = 8) {
  let v = 0;
  for (const b of times) if (t >= b) v = Math.max(v, Math.exp(-(t - b) * decay));
  return v;
}

// Cursor that drives a UI: moves between waypoints on springs with a slight arc, presses on each click
// and leaves a ripple. path: [[t, x, y], ...] · clicks: [t, ...] (add a 'click' cue at each).
// Returns { x, y, scale, ripples: [{ x, y, r, alpha }] } for the hotspot (arrow tip).
export function cursor(t, path, clicks = [], preset = 'snappy') {
  const { x, y } = trackObj(t, path.map(([kt, px, py]) => [kt, { x: px, y: py }]), preset);
  let ax = 0, ay = 0;
  for (let i = 1; i < path.length; i++) {
    const dx = path[i][1] - path[i - 1][1], dy = path[i][2] - path[i - 1][2], len = Math.hypot(dx, dy);
    if (!len) continue;
    const bow = Math.sin(Math.PI * clamp(spring(t - path[i][0], preset))) ** 2 * Math.min(0.12 * len, 90);
    ax += (-dy / len) * bow; ay += (dx / len) * bow;
  }
  let scale = 1;
  const ripples = [];
  for (const tc of clicks) {
    if (t >= tc - 0.06 && t < tc) scale = Math.min(scale, 1 - 0.2 * ((t - tc + 0.06) / 0.06));
    else if (t >= tc) scale = Math.min(scale, 0.8 + 0.2 * spring(t - tc, 'playful'));
    if (t >= tc && t < tc + 0.5) {
      const p = (t - tc) / 0.5, at = cursor(tc, path, [], preset);
      ripples.push({ x: at.x, y: at.y, r: 18 + 70 * (1 - (1 - p) ** 3), alpha: (1 - p) ** 2 });
    }
  }
  return { x: x + ax, y: y + ay, scale, ripples };
}

// Arrow pointer, tip at (0, 0), 28×42 box: g.fill(new Path2D(CURSOR_PATH)).
export const CURSOR_PATH = 'M1 1 L1 33 L9.5 25.5 L15 38.5 L21 36 L15.5 23.5 L26.5 23.5 Z';
