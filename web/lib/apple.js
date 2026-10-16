// Apple motion craft — the iOS / Apple-keynote layer on top of motion.js (same values as the Python engine's
// engine/tokens.py IOS + EASE + keynote.py). Everything is a pure function of time: seek(t) stays deterministic.
//
//   import { iosAt, arrive, follow, presence, rise, wipe, depthSwap, focusPull, sheet, bento, morphBox,
//            press, countUp, drawOn, dolly, push, applyCam, curve, ease } from '/web/lib/apple.js';
//
// Grammar: one leader per beat (others follow() 0.12 s later with less travel) · big moves land ON the stressed
// word (arrive) · opacity leads, position follows · exits are quieter and faster than entrances (apple_in, 0.32 s,
// scale .98) · springs without visible bounce on text and big things · hand over scenes with a shared element,
// depthSwap or focusPull — never a blank frame.
import { clamp, spring, track } from './motion.js';

// ── SwiftUI springs by real time: [response s, dampingFraction] ─────────────────────────────────
export const IOS = {
  smooth: [0.5, 1.0],     // .smooth — no overshoot (default for text + cards)
  snappy: [0.5, 0.85],    // .snappy — ~1 % overshoot (chips, buttons, UI pops)
  bouncy: [0.5, 0.7],     // .bouncy — small objects only, max once per scene
  default: [0.55, 0.825], // .spring() default
  hero: [0.85, 1.0],      // big hero objects / full-bleed shrink — heavy, no overshoot
  lead: [0.35, 0.84],     // indicator leading edge
  trail: [0.53, 0.93],    // indicator trailing edge
};

/** iOS preset → [stiffness, damping] for motion.js spring()/track() (unit mass). */
export function iosKD(name = 'smooth') {
  const [response, z] = Array.isArray(name) ? name : IOS[name] || IOS.smooth;
  const w = (2 * Math.PI) / response;
  return [w * w, 2 * z * w];
}

/** 0 → 1 (may overshoot for snappy/bouncy) for a move that starts at t0. 0 before t0. */
export const iosAt = (t, t0, name = 'smooth') => spring(t - t0, ...iosKD(name));

/** track() with an iOS preset: a value with several [time, value] targets bends between them. */
export const iosTrack = (t, keys, name = 'smooth') => track(t, keys, ...iosKD(name));

const _dur = {};
/** Seconds until the preset is within 0.5 % of rest — use it to budget holds. */
export function iosDur(name = 'smooth') {
  const key = String(name);
  if (_dur[key] != null) return _dur[key];
  let last = 0;
  for (let dt = 0; dt < 4; dt += 1 / 240) if (Math.abs(1 - spring(dt, ...iosKD(name))) > 0.005) last = dt;
  return (_dur[key] = last);
}

/** Start time so the move is `frac` of the way there exactly at tHit — land ON the stressed word. */
export function arrive(tHit, name = 'smooth', frac = 0.9) {
  for (let dt = 0; dt < 3; dt += 1 / 480) if (spring(dt, ...iosKD(name)) >= frac) return tHit - dt;
  return tHit;
}

/** Start of the i-th follower: one leader moves, the rest follow `gap` s apart (with ≤ half the travel). */
export const follow = (tLead, i = 1, gap = 0.12) => tLead + i * gap;

// ── Apple cubic-bezier curves ─────────────────────────────────────────────────────────────────
export const EASE = {
  apple: [0.28, 0.11, 0.32, 1.0],        // apple.com standard transition
  apple_out: [0.16, 1.0, 0.3, 1.0],      // entrances: decisive start, long glide to rest
  apple_in: [0.4, 0.0, 0.9, 0.55],       // exits: quiet start, leaves quickly
  apple_in_out: [0.65, 0.0, 0.35, 1.0],  // push / pan between two focus points
  apple_dolly: [0.42, 0.0, 0.58, 1.0],   // slow camera dolly over a hold
};
const _bez = {};
/** Named easing p → eased p (0..1). */
export function curve(name = 'apple') {
  if (_bez[name]) return _bez[name];
  const [x1, y1, x2, y2] = EASE[name] || EASE.apple;
  const bx = (s) => 3 * x1 * s * (1 - s) ** 2 + 3 * x2 * s * s * (1 - s) + s ** 3;
  const by = (s) => 3 * y1 * s * (1 - s) ** 2 + 3 * y2 * s * s * (1 - s) + s ** 3;
  const fn = (p) => {
    if (p <= 0) return 0;
    if (p >= 1) return 1;
    let lo = 0, hi = 1, s = p;
    for (let i = 0; i < 24; i++) { s = (lo + hi) / 2; if (bx(s) < p) lo = s; else hi = s; }
    return by(s);
  };
  return (_bez[name] = fn);
}
/** curve(name) over [t0, t0 + dur]. */
export const ease = (t, t0, dur, name = 'apple') => curve(name)((t - t0) / dur);

// ── presence: how every element enters and leaves ─────────────────────────────────────────────
const OP_LEAD = 0.45, QUIET_OUT = 0.32, QUIET_SCALE = 0.98;
/** { move, alpha, out } — move = iOS spring 0→1 from tIn; alpha is done at 45 % of the move (opacity leads);
 *  out = 0→1 quiet exit from tOut (apple_in, 0.32 s). */
export function presence(t, tIn, tOut = null, name = 'smooth') {
  const move = iosAt(t, tIn, name);
  const out = tOut == null ? 0 : ease(t, tOut, QUIET_OUT, 'apple_in');
  const alpha = clamp(Math.min(1, move / OP_LEAD)) * (1 - out);
  return { move, alpha, out };
}

/** Apple fade-up: draw(g) at rest; arrives from dy below and a touch small, leaves quietly.
 *  box = [x, y, w, h] (scale origin). */
export function rise(g, t, tIn, tOut, box, draw, { dy = 34, scale = 0.985, name = 'smooth' } = {}) {
  const { move, alpha, out } = presence(t, tIn, tOut, name);
  if (alpha <= 0.001) return;
  const [x, y, w, h] = box, cx = x + w / 2, cy = y + h / 2;
  const s = (scale + (1 - scale) * Math.min(1, move)) * (1 - (1 - QUIET_SCALE) * out);
  g.save();
  g.globalAlpha *= alpha;
  g.translate(cx, cy + dy * (1 - move));
  g.scale(s, s);
  g.translate(-cx, -cy);
  draw(g);
  g.restore();
}

// ── offscreen helper (masks, blur) ──────────────────────────────────────────────────────────────
const _off = new Map();
function layer(w, h, key) {
  const k = `${key}:${Math.ceil(w)}x${Math.ceil(h)}`;
  let c = _off.get(k);
  if (!c) { c = new OffscreenCanvas(Math.max(1, Math.ceil(w)), Math.max(1, Math.ceil(h))); _off.set(k, c); }
  const x = c.getContext('2d');
  x.setTransform(1, 0, 0, 1, 0, 0);
  x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; x.filter = 'none';
  x.clearRect(0, 0, c.width, c.height);
  return [c, x];
}

/** Soft-edged mask wipe (keynote title / product reveal): a feathered edge sweeps across box on apple_out.
 *  direction: right | left | up | down. Leaves with a quiet fade from tOut. */
export function wipe(g, t, t0, box, draw, { dur = 0.95, soft = 0.22, direction = 'right', tOut = null } = {}) {
  const p = ease(t, t0, dur, 'apple_out');
  const a = tOut == null ? 1 : 1 - ease(t, tOut, QUIET_OUT, 'apple_in');
  if (p <= 0 || a <= 0) return;
  const [x, y, w, h] = box;
  if (p >= 1) { g.save(); g.globalAlpha *= a; draw(g); g.restore(); return; }
  const [c, o] = layer(w, h, 'wipe');
  o.translate(-x, -y); draw(o); o.setTransform(1, 0, 0, 1, 0, 0);
  const horiz = direction === 'right' || direction === 'left';
  const len = horiz ? w : h, edge = p * len * (1 + soft);
  let grad;
  if (direction === 'right') grad = o.createLinearGradient(edge - soft * len, 0, edge, 0);
  else if (direction === 'left') grad = o.createLinearGradient(w - edge + soft * len, 0, w - edge, 0);
  else if (direction === 'down') grad = o.createLinearGradient(0, edge - soft * len, 0, edge);
  else grad = o.createLinearGradient(0, h - edge + soft * len, 0, h - edge);
  grad.addColorStop(0, 'rgba(0,0,0,1)'); grad.addColorStop(1, 'rgba(0,0,0,0)');
  o.globalCompositeOperation = 'destination-in';
  o.fillStyle = grad; o.fillRect(0, 0, w, h);
  g.save(); g.globalAlpha *= a; g.drawImage(c, x, y); g.restore();
}

/** Keynote push-through: old content falls back (→ .92, fades fast) while new comes forward from 1.06.
 *  Both drawn around box's centre. Before tSwap only old is drawn; after the swap only new. */
export function depthSwap(g, t, tSwap, box, oldDraw, newDraw, { dur = 0.85 } = {}) {
  const p = ease(t, tSwap, dur, 'apple_in_out');
  const [x, y, w, h] = box, cx = x + w / 2, cy = y + h / 2;
  const at = (s, a, fn) => {
    if (a <= 0.001) return;
    g.save(); g.globalAlpha *= a; g.translate(cx, cy); g.scale(s, s); g.translate(-cx, -cy); fn(g); g.restore();
  };
  at(1 - 0.08 * p, 1 - clamp(p / 0.5), oldDraw);
  at(1.06 - 0.06 * p, clamp((p - 0.3) / 0.5), newDraw);
}

/** Rack focus: while a foreground is up (t0..t1) the background goes soft — blur + scale .965 + dim.
 *  Call it to draw the BACKGROUND; then draw the foreground yourself. Depth, never a frosted-glass panel. */
export function focusPull(g, t, t0, t1, box, draw, { blur = 9, scale = 0.965, dim = 0.35 } = {}) {
  const k = iosAt(t, t0, 'smooth') - iosAt(t, t1, 'smooth');
  if (k <= 0.002) { draw(g); return; }
  const [x, y, w, h] = box, cx = x + w / 2, cy = y + h / 2, s = 1 - (1 - scale) * k;
  g.save();
  g.translate(cx, cy); g.scale(s, s); g.translate(-cx, -cy);
  g.filter = `blur(${(blur * k).toFixed(2)}px)`;
  g.globalAlpha *= 1 - dim * k;
  draw(g);
  g.restore();
}

/** Floating sheet: slides up from below the frame on a smooth spring and dims what's behind it.
 *  H = frame height. box = [x, y, w, h] at rest. */
export function sheet(g, t, tIn, tOut, box, draw, { H = 1920, dim = 0.35, r = 44, fill = '#fff' } = {}) {
  const { move, out } = presence(t, tIn, tOut, 'smooth');
  const vis = Math.min(1, move) * (1 - out);
  if (vis <= 0.001) return;
  const [x, y, w, h] = box, dy = (H - y) * (1 - Math.min(1, move)) + 80 * out;
  g.save();
  g.fillStyle = `rgba(0,0,0,${(dim * vis).toFixed(3)})`;
  g.fillRect(-1e4, -1e4, 2e4, 2e4);
  g.translate(0, dy);
  g.globalAlpha *= 1 - out;
  roundRect(g, x, y, w, h, r); g.fillStyle = fill; g.fill();
  g.save(); roundRect(g, x, y, w, h, r); g.clip(); draw(g, [x, y, w, h]); g.restore();
  g.restore();
}

/** Tiles assemble into a grid: each rises + scales from .94 + fades, staggered outward from the first tile.
 *  area = [x, y, w, h]; tiles = [drawFn(g, box), …]; cols/rows; returns the tile boxes. */
export function bento(g, t, t0, area, tiles, { cols = 2, rows = 2, gap = 24, step = 0.07, tOut = null } = {}) {
  const [x, y, w, h] = area, tw = (w - gap * (cols - 1)) / cols, th = (h - gap * (rows - 1)) / rows;
  const boxes = [];
  tiles.forEach((fn, i) => {
    const cx = i % cols, cy = Math.floor(i / cols), box = [x + cx * (tw + gap), y + cy * (th + gap), tw, th];
    boxes.push(box);
    const d = Math.hypot(cx, cy);
    const { move, alpha, out } = presence(t, t0 + d * step, tOut, 'smooth');
    if (alpha <= 0.001) return;
    const s = (0.94 + 0.06 * Math.min(1, move)) * (1 - 0.02 * out);
    const bx = box[0] + tw / 2, by = box[1] + th / 2 + 40 * (1 - move);
    g.save(); g.globalAlpha *= alpha; g.translate(bx, by); g.scale(s, s); g.translate(-tw / 2, -th / 2);
    fn(g, [0, 0, tw, th]);
    g.restore();
  });
  return boxes;
}

/** A rounded rect whose box + radius spring between keys — ONE shape that never cuts.
 *  keys = [[time, {x, y, w, h, r}], …] → {x, y, w, h, r, k} where k = index of the last key started. */
export function morphBox(t, keys, name = 'smooth') {
  const out = {};
  for (const f of ['x', 'y', 'w', 'h', 'r']) out[f] = iosTrack(t, keys.map(([tk, b]) => [tk, b[f] ?? 0]), name);
  out.k = keys.reduce((k, [tk], i) => (t >= tk ? i : k), 0);
  return out;
}

/** Button press scale: 1 → .94 in 0.12 s, then springs back (snappy). g.scale(press(t, tTap)). */
export function press(t, t0) {
  if (t < t0) return 1;
  if (t < t0 + 0.12) return 1 - 0.06 * curve('apple_out')((t - t0) / 0.12);
  return 0.94 + 0.06 * iosAt(t, t0 + 0.12, 'snappy');
}

/** Count v0 → v1 on apple_out over dur (1.2–2.5 s). Round/format it yourself (tabular figures avoid jitter). */
export const countUp = (t, t0, dur, v0, v1) => v0 + (v1 - v0) * ease(t, t0, dur, 'apple_out');

/** Indonesian number format: 2951 → "2.951", 44.4 → "44,4". */
export function fmtID(v, decimals = 0) {
  const [i, d] = Math.abs(v).toFixed(decimals).split('.');
  return (v < 0 ? '−' : '') + i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + (d ? ',' + d : '');
}

/** Stroke draw-on: path (Path2D) of known length draws 0 → full on apple_out in dur, then optional quiet exit. */
export function drawOn(g, t, t0, path, length, { dur = 0.8, color = '#fff', width = 6, tOut = null } = {}) {
  const p = ease(t, t0, dur, 'apple_out');
  const a = tOut == null ? 1 : 1 - ease(t, tOut, QUIET_OUT, 'apple_in');
  if (p <= 0 || a <= 0) return;
  g.save();
  g.globalAlpha *= a; g.strokeStyle = color; g.lineWidth = width; g.lineCap = 'round'; g.lineJoin = 'round';
  g.setLineDash([length, length]); g.lineDashOffset = length * (1 - p);
  g.stroke(path);
  g.restore();
}

// ── camera ────────────────────────────────────────────────────────────────────────────────────
/** Slow push over a HOLD (the only motion while content rests): scale base → base + zoom on apple_dolly. */
export const dolly = (t, t0, t1, zoom = 0.03, base = 1) => base + zoom * ease(t, t0, Math.max(0.01, t1 - t0), 'apple_dolly');

/** Motivated push to the next focus: {s, x, y} from `from` to `to` ({s, x, y}) on apple_in_out. */
export function push(t, t0, from, to, dur = 0.9) {
  const p = ease(t, t0, dur, 'apple_in_out');
  return { s: from.s + (to.s - from.s) * p, x: from.x + (to.x - from.x) * p, y: from.y + (to.y - from.y) * p };
}

/** Apply a camera {s, x, y} (x, y = focus point in stage px) to the context. Call between save()/restore(). */
export function applyCam(g, cam, W, H) {
  g.translate(W / 2, H / 2); g.scale(cam.s, cam.s); g.translate(-cam.x, -cam.y);
}

// ── small helpers ─────────────────────────────────────────────────────────────────────────────
export function roundRect(g, x, y, w, h, r) {
  r = Math.max(0, Math.min(r, w / 2, h / 2));
  g.beginPath();
  g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r);
  g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
}
