// HTML film harness (grak core + cheese extras). Called by engine/web.py — you rarely run it by hand.
//
//   node web/run.mjs frames  --page videos/x/film.html --fps 60 --sub 4 --from 0 --to 3600 --out DIR [--jobs N]
//   node web/run.mjs at      --page videos/x/film.html --times 0.5,1.2 --out DIR      stills, no encode
//   node web/run.mjs cues    --page videos/x/film.html                                window.CUES → stdout
//   node web/run.mjs check   --page videos/x/film.html --times 0.5,1.2                page errors + determinism
//   node web/run.mjs capture --url https://x.com --out DIR                            screenshots + site.json
//   node web/run.mjs serve   [--port 5173]                                            live preview in a browser
//
// A film paints frame t when the harness calls window.seek(t) (film.js sets it up). Pages are served from the
// repo root, so /web/lib/*.js and /assets/fonts/* resolve. Frames are PNG; --sub N averages N subframes spread
// over the frame interval, centred on t (the same shutter as engine/render.py).
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { cpus } from 'node:os';
import { extname, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('..', import.meta.url)));
const W = 1080, H = 1920;
const cmd = process.argv[2];
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const times = () => String(arg('times', '')).split(',').filter(Boolean).map(Number);

// ── static server for the repo root (ES modules and fetch() don't work from file://) ─────────────
const TYPES = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml',
  '.webp': 'image/webp', '.gif': 'image/gif', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.otf': 'font/otf',
  '.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.mp4': 'video/mp4',
};
function serve(port = 0) {
  const server = createServer(async (req, res) => {
    const path = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname));
    const file = join(ROOT, path.endsWith('/') ? path + 'index.html' : path);
    if (!file.startsWith(ROOT)) { res.writeHead(403).end(); return; }
    try {
      const body = await readFile(file);
      res.writeHead(200, { 'content-type': TYPES[extname(file)] || 'application/octet-stream', 'cache-control': 'no-store' });
      res.end(body);
    } catch { res.writeHead(404).end('not found'); }
  });
  return new Promise((r) => server.listen(port, '127.0.0.1', () => r({ server, port: server.address().port })));
}

// Playwright's Chromium if installed, else the system Chrome (no download needed).
async function launch() {
  try { return await chromium.launch(); } catch {}
  for (const p of ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'])
    if (existsSync(p)) return chromium.launch({ executablePath: p });
  throw new Error('No browser: install Chrome or run `npx playwright install chromium` in web/');
}

async function open(browser, port, errors) {
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !m.text().startsWith('Failed to load resource')) errors.push(m.text()); });
  page.on('response', (r) => { if (r.status() >= 400 && !r.url().endsWith('/favicon.ico')) errors.push(`${r.status()} ${new URL(r.url()).pathname}`); });
  await page.goto(`http://127.0.0.1:${port}/${arg('page')}`);
  await page.waitForFunction(() => typeof window.seek === 'function', null, { timeout: 30000 });
  await page.evaluate(async () => { await window.ready; await document.fonts.ready; });
  return page;
}
const shot = async (page, t) => { await page.evaluate((t) => window.seek(t), t); return page.screenshot({ type: 'png' }); };

// ── frames: [from, to) frame indexes → DIR/000123.png, split over --jobs pages ─────────────────────
async function frames(browser, port) {
  const fps = +arg('fps', 60), sub = +arg('sub', 1), out = arg('out'), dur = +arg('dur', 1e9);
  const f0 = +arg('from', 0), f1 = +arg('to');
  const jobs = Math.max(1, Math.min(+arg('jobs', Math.max(1, Math.min(6, Math.floor(cpus().length / 3)))), f1 - f0));
  mkdirSync(out, { recursive: true });
  const size = Math.ceil((f1 - f0) / jobs), t0 = Date.now();
  let done = 0;
  const errors = [];
  await Promise.all(Array.from({ length: jobs }, async (_, j) => {
    const a = f0 + j * size, b = Math.min(f1, a + size);
    if (a >= b) return;
    const page = await open(browser, port, errors);
    // tmix averages each group of `sub` subframes; select keeps the last of each group.
    const vf = sub > 1 ? `tmix=frames=${sub},select='eq(mod(n\\,${sub})\\,${sub - 1})'` : 'null';
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps * sub), '-i', '-',
      '-vf', vf, '-fps_mode', 'passthrough', '-start_number', String(a), join(out, '%06d.png')], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = a; f < b; f++) {
      for (let k = 0; k < sub; k++) {
        const t = Math.min(dur - 1e-4, Math.max(0, (f + (k + 0.5) / sub - 0.5) / fps));
        const png = await shot(page, sub > 1 ? t : f / fps);
        if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
      }
      if (++done % fps === 0) {
        const el = (Date.now() - t0) / 1000;
        process.stdout.write(`\r  web frames ${done}/${f1 - f0}  ${(done / el).toFixed(1)} fps  eta ${((f1 - f0 - done) * el / done).toFixed(0)}s `);
      }
    }
    ff.stdin.end();
    const code = await new Promise((r) => ff.on('close', r));
    if (code) throw new Error(`ffmpeg exited ${code}`);
    await page.close();
  }));
  console.log(`\r  web frames ${f1 - f0} in ${((Date.now() - t0) / 1000).toFixed(0)}s (${jobs} pages${sub > 1 ? `, ${sub} subframes` : ''})          `);
  if (errors.length) { console.error('page errors:\n  ' + [...new Set(errors)].join('\n  ')); process.exitCode = 1; }
}

// ── at: exact stills (critique, cover, sheet) → DIR/<t>.png ─────────────────────────────────────────
async function at(browser, port) {
  const out = arg('out'), errors = [];
  mkdirSync(out, { recursive: true });
  const page = await open(browser, port, errors);
  for (const t of times()) writeFileSync(join(out, `${t.toFixed(4)}.png`), await shot(page, t));
  if (errors.length) { console.error('page errors:\n  ' + [...new Set(errors)].join('\n  ')); process.exitCode = 1; }
}

// ── cues: the SFX cue sheet the film computed from its own timings (window.CUES) ─────────────────────
async function cues(browser, port) {
  const errors = [], page = await open(browser, port, errors);
  console.log(JSON.stringify({ cues: await page.evaluate(() => window.CUES || []), errors }));
}

// ── check: loads, seeks every sample, reports page errors; renders one moment twice (determinism) ───
async function check(browser, port) {
  const errors = [], page = await open(browser, port, errors), ts = times();
  for (const t of ts) await page.evaluate((t) => window.seek(t), t);
  const probe = ts[Math.floor(ts.length * 0.37)] ?? 1;
  const a = await shot(page, probe);
  await shot(page, ts[ts.length - 1] ?? 0);
  const b = await shot(page, probe);
  const blank = await page.evaluate(() => document.body.scrollWidth > innerWidth || document.body.scrollHeight > innerHeight);
  console.log(JSON.stringify({ errors: [...new Set(errors)], deterministic: a.equals(b), probe, overflow: blank }));
}

// ── capture: real screenshots + brand facts from a site (mobile + desktop) ───────────────────────────
async function capture(browser) {
  const url = arg('url'), out = arg('out');
  mkdirSync(out, { recursive: true });
  const site = { url, shots: [] };
  for (const [name, vp, dpr] of [['mobile', { width: 390, height: 844 }, 3], ['desktop', { width: 1440, height: 900 }, 1.5]]) {
    const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: dpr, isMobile: name === 'mobile' });
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
    await page.waitForTimeout(1200);
    await page.screenshot({ path: join(out, `${name}.png`) });
    await page.screenshot({ path: join(out, `${name}_full.png`), fullPage: true }).catch(() => {});
    site.shots.push(`${name}.png`, `${name}_full.png`);
    if (name === 'mobile') Object.assign(site, await page.evaluate(() => {
      const meta = (n) => document.querySelector(`meta[name="${n}"],meta[property="${n}"]`)?.content || null;
      const css = getComputedStyle(document.body);
      const fonts = [...new Set([...document.querySelectorAll('h1,h2,p,a,button')].slice(0, 40).map((e) => getComputedStyle(e).fontFamily))];
      const colors = {};
      for (const e of [...document.querySelectorAll('a,button,h1,h2,[class*=btn],[class*=button]')].slice(0, 200)) {
        for (const c of [getComputedStyle(e).color, getComputedStyle(e).backgroundColor])
          if (c && !/rgba\(0, 0, 0, 0\)|transparent/.test(c)) colors[c] = (colors[c] || 0) + 1;
      }
      return {
        title: document.title, description: meta('description') || meta('og:description'), themeColor: meta('theme-color'),
        ogImage: meta('og:image'), icon: document.querySelector('link[rel~="icon"]')?.href || null,
        background: css.backgroundColor, text: css.color, fonts,
        colors: Object.entries(colors).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([c]) => c),
        headings: [...document.querySelectorAll('h1,h2')].slice(0, 8).map((e) => e.innerText.trim()).filter(Boolean),
      };
    }));
    await ctx.close();
  }
  writeFileSync(join(out, 'site.json'), JSON.stringify(site, null, 1) + '\n');
  console.log(`capture: ${url} → ${out}/ (${site.shots.join(', ')}, site.json)`);
}

if (cmd === 'serve') {
  const { port } = await serve(+arg('port', 5173));
  console.log(`preview: http://localhost:${port}/videos/<slug>/film.html   (?t=3.5 freezes a frame)`);
} else if (['frames', 'at', 'cues', 'check', 'capture'].includes(cmd)) {
  const { server, port } = await serve(0);
  const browser = await launch();
  try { await { frames, at, cues, check, capture }[cmd](browser, port); }
  finally { await browser.close(); server.close(); }
} else {
  console.log('usage: node web/run.mjs frames|at|cues|check|capture|serve …  (see the header of this file)');
  process.exitCode = 1;
}
