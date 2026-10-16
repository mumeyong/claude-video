// Film glue: the page side of a MUMEYONG HTML film (videos/<slug>/film.html).
//
//   import { FILM, ready, T, cue, canvas, beats, SAFE } from '/web/lib/film.js';
//   await ready;                                   // FILM + fonts loaded
//   const hit = T.word('L03', 'gratis');           // voice is the clock: line/word times from timing.json
//   cue('pop', hit, 0.6);                          // SFX cue (names: engine/audio/sfx.py) — at setup, never in seek
//   canvas((g, t) => { ... });                     // or set window.seek = (t) => { ...DOM... } yourself
//
// Times are GLOBAL seconds of the final video: the brand sting (PRE_ROLL) is already added, so L01 starts at
// FILM.pre_roll. The page is drawn under the opening logo and fades out where the ending logo starts (FILM.end).
// FILM = { slug, W, H, fps, duration, start, end, pre_roll, lines, chapters, beats, safe, ui } — written by
// engine/web.py to videos/<slug>/out/.web/film.json every time the video is built.

export const FILM = {};
export const SAFE = { x0: 81, x1: 929, y0: 240, y1: 1560 };      // keep text + key subjects in here (house lint)
const base = document.createElement('style');
base.textContent = 'html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000}canvas{display:block}';
document.head.appendChild(base);

const norm = (w) => String(w).normalize('NFKD').toLowerCase().replace(/[^a-z0-9]/g, '');

export const ready = (async () => {
  const r = await fetch(new URL('out/.web/film.json', location.href), { cache: 'no-store' });
  if (!r.ok) throw new Error('out/.web/film.json missing — run: python -m engine check <slug>');
  Object.assign(FILM, await r.json());
  Object.assign(SAFE, FILM.safe || {});
  await document.fonts.ready;
})();
window.ready = ready;

// ── voice timing (same rules as engine/timing.py) ──────────────────────────────────────────────────
const lineOf = (id) => {
  const ln = FILM.lines.find((l) => l.id === id);
  if (!ln) throw new Error(`no line ${id} in timing.json`);
  return ln;
};
export const T = {
  line: lineOf,
  /** Time of the nth occurrence of word w in line id (fuzzy, accents/punctuation ignored). */
  word(id, w, nth = 0, edge = 'start') {
    const ln = lineOf(id), k = norm(w);
    let hits = ln.words.filter((x) => norm(x.w) === k);
    if (!hits.length) hits = ln.words.filter((x) => k && norm(x.w).includes(k));
    if (!hits.length) throw new Error(`word "${w}" not in ${id}: "${ln.text}"`);
    return hits[Math.min(nth, hits.length - 1)][edge];
  },
  /** Time at fraction f (0..1) through a line. */
  frac: (id, f) => { const ln = lineOf(id); return ln.start + (ln.end - ln.start) * f; },
  /** [start, end] of all lines of a chapter (the ## heading in SCRIPT.md). */
  chapter(name) {
    const ls = FILM.lines.filter((l) => l.chapter === name);
    if (!ls.length) throw new Error(`no chapter ${name}`);
    return [ls[0].start, ls[ls.length - 1].end];
  },
  /** The *stressed* words (SCRIPT.md marks) of one line, or of every line: [{ w, start, end, line }]. */
  stressed: (id = null) => FILM.lines.filter((l) => !id || l.id === id)
    .flatMap((l) => l.words.filter((w) => w.stress).map((w) => ({ ...w, line: l.id }))),
  /** Word currently being spoken at t (captions): { line, i, word } or null. */
  at(t) {
    for (const ln of FILM.lines) {
      if (t < ln.start || t >= ln.end + 0.25) continue;
      let i = -1;
      ln.words.forEach((w, j) => { if (w.start <= t) i = j; });
      return { line: ln, i, word: ln.words[i] || null };
    }
    return null;
  },
};

// ── beats: the score's grid (or a measured beats.json) ─────────────────────────────────────────────
/** Index of the last beat at or before t, and the time since it. */
export function beats(t) {
  const b = FILM.beats?.beats || [];
  let i = -1;
  for (let j = 0; j < b.length && b[j] <= t; j++) i = j;
  return { i, since: i < 0 ? t : t - b[i], bar: Math.floor(Math.max(0, i) / 4) };
}
/** Snap a time to the beat at or before it (cuts land on the beat). */
export const snap = (t) => { const { i } = beats(t + 0.02); return i < 0 ? t : FILM.beats.beats[i]; };

// ── SFX cues: collected once at setup, read by the engine (engine/audio/sfx.py names) ──────────────
window.CUES = [];
export function cue(name, t, gain = 1) { window.CUES.push({ name, t: +t, gain: +gain }); }

// ── canvas film: draw(g, t) paints one frame; nothing may carry over between frames ───────────────
export function canvas(draw) {
  const cv = document.querySelector('canvas') || document.body.appendChild(document.createElement('canvas'));
  cv.width = FILM.W; cv.height = FILM.H;
  const g = cv.getContext('2d');
  window.seek = (t) => { g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.filter = 'none'; g.clearRect(0, 0, FILM.W, FILM.H); draw(g, t); };
  return g;
}

// ── live preview in a normal browser (node web/run.mjs serve): ?t=3.5 freezes a frame ─────────────
if (!navigator.webdriver) {
  ready.then(() => {
    const q = new URLSearchParams(location.search);
    base.textContent += `html,body{width:auto;height:auto;overflow:auto;background:#111}
      canvas,body>.stage{transform-origin:0 0;transform:scale(${Math.min(innerWidth / 1080, innerHeight / 1920)})}`;
    const wait = () => (typeof window.seek === 'function' ? go() : setTimeout(wait, 50));
    const go = () => {
      if (q.has('t')) return window.seek(+q.get('t'));
      const t0 = performance.now() / 1000 - (+q.get('from') || 0);
      const tick = () => { window.seek(Math.min(FILM.end, performance.now() / 1000 - t0)); requestAnimationFrame(tick); };
      tick();
    };
    wait();
  });
}
