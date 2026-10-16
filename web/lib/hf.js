// HyperFrames bridge: a DOM film written the HyperFrames way (one paused GSAP timeline + timed clips), driven by
// the MUMEYONG harness. The hyperframes-* skills (animation rules, blueprints, keyframes, registry blocks) apply
// as written — only the clock differs: times come from the voice (T), never typed seconds.
//
//   import { FILM, ready, T, cue } from '/web/lib/film.js';
//   import { gsap, clip, timeline } from '/web/lib/hf.js';
//   await ready;
//   const tl = gsap.timeline({ paused: true });
//   clip('#hook', FILM.pre_roll, T.line('L02').start);       // visible only inside [start, end) — like data-start
//   tl.fromTo('#hook h1', { yPercent: 40, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .5, ease: 'expo.out' },
//             T.word('L01', 'kenapa'));
//   timeline(tl);                                              // window.seek(t) = clip visibility + tl.seek(t)
//
// Ported HyperFrames code that registers window.__timelines['main'] = tl works too: call timeline() with no
// argument. Clips may also carry data-start / data-duration set from T in script (global seconds, sting included).
import { gsap } from '/web/node_modules/gsap/index.js';

export { gsap };
gsap.globalTimeline.pause();         // nothing plays on its own: a stray gsap.to() can't run on the wall clock
gsap.ticker.lagSmoothing(0);
window.__timelines = window.__timelines || {};

const CLIPS = [];

/** Show el (element or selector) only inside [start, end) — HyperFrames clip semantics, times from T. */
export function clip(el, start, end = Infinity) {
  for (const e of typeof el === 'string' ? document.querySelectorAll(el) : [el]) CLIPS.push({ el: e, s: +start, e: +end });
}

/** Drive tl (default: the first timeline in window.__timelines) from window.seek(t). Call once, after setup. */
export function timeline(tl = Object.values(window.__timelines)[0]) {
  if (!tl) throw new Error('timeline(): no GSAP timeline passed and none in window.__timelines');
  for (const el of document.querySelectorAll('[data-start]')) {
    const s = +el.dataset.start, d = el.dataset.duration;
    clip(el, s, d == null ? Infinity : s + +d);
  }
  tl.pause();
  window.seek = (t) => {
    for (const c of CLIPS) c.el.style.visibility = t >= c.s && t < c.e ? '' : 'hidden';
    tl.seek(t, true);                 // suppressEvents: callbacks would be state carried between frames
  };
  return tl;
}
