// Measure how smooth the animations actually are, rather than guessing.
// Run:  node perf-check.mjs [--json]
//
// What it measures, and why each one:
//
//   applyMs        time inside apply() — the JS that runs on every step change.
//                  This is the budget. At 120Hz a frame is 8.3ms; anything over
//                  that here guarantees a dropped frame at the moment the kid
//                  presses space, which is exactly when they are looking.
//   layoutReads    getBoundingClientRect / offsetWidth calls inside apply().
//                  Each one that FOLLOWS a DOM write forces a synchronous
//                  layout. Read-write-read-write interleaving is the classic
//                  jank source and it does not show up in any data check.
//   violations     Chrome's own "[Violation] Forced reflow ..." console lines.
//                  The browser telling you directly.
//   longTasks      PerformanceObserver longtask entries (>50ms main thread).
//   frame p95/max  rAF deltas during autoplay. Headless timing is synthetic, so
//                  treat the ABSOLUTE numbers as soft and the before/after
//                  DELTA as the real signal.
//
// Prints a table per animation. Exits non-zero if a budget is blown.

import { createRequire } from 'module';
import { pathToFileURL } from 'url';
import path from 'path';
import { fileURLToPath } from 'url';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const CANDIDATES = [
  process.env.PLAYWRIGHT_PATH,
  `${process.env.HOME}/code/e2e/node_modules/playwright`,
  'playwright',
].filter(Boolean);
let chromium;
for (const c of CANDIDATES) {
  try {
    const req = createRequire(import.meta.url);
    const resolved = c === 'playwright' ? 'playwright' : pathToFileURL(req.resolve(c)).href;
    const m = await import(resolved);
    chromium = m.chromium ?? m.default?.chromium;
    if (chromium) break;
  } catch { /* next */ }
}
if (!chromium) { console.error('playwright not found'); process.exit(2); }

// Budgets. applyMs is the one that matters: it is synchronous work sitting
// between the keypress and the first painted frame of the transition.
const BUDGET = { applyP95: 8.3, applyMax: 16.7, longTasks: 0, violations: 0 };

const b = await chromium.launch();
const page = await b.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });

const violations = [];
page.on('console', m => {
  const t = m.text();
  if (/Forced reflow|Violation/i.test(t)) violations.push(t);
});

await page.goto('file://' + DIR + '/index.html');
await page.waitForTimeout(300);

// Instrument: count layout reads and time apply(), without editing the page source.
await page.addInitScript(() => {});
await page.evaluate(() => {
  window.__perf = { reads: 0, applies: [], longTasks: [], frames: [] };

  const rect = Element.prototype.getBoundingClientRect;
  Element.prototype.getBoundingClientRect = function (...a) {
    window.__perf.reads++;
    return rect.apply(this, a);
  };
  const ow = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetWidth');
  Object.defineProperty(HTMLElement.prototype, 'offsetWidth', {
    get() { window.__perf.reads++; return ow.get.call(this); }, configurable: true,
  });

  try {
    new PerformanceObserver(l => l.getEntries().forEach(e =>
      window.__perf.longTasks.push(Math.round(e.duration)))).observe({ entryTypes: ['longtask'] });
  } catch {}

  let last = performance.now();
  (function tick(t) { window.__perf.frames.push(t - last); last = t; requestAnimationFrame(tick); })(last);

  // wrap the page's own apply()
  const orig = window.apply;
  window.apply = function (...a) {
    const r0 = window.__perf.reads, t0 = performance.now();
    const out = orig.apply(this, a);
    window.__perf.applies.push({ ms: performance.now() - t0, reads: window.__perf.reads - r0 });
    return out;
  };
});

const pct = (arr, p) => {
  if (!arr.length) return 0;
  const s = [...arr].sort((x, y) => x - y);
  return s[Math.min(s.length - 1, Math.floor(s.length * p))];
};

const report = [];
for (let i = 0; i < 4; i++) {
  await page.evaluate(() => { window.__perf.applies = []; window.__perf.frames = []; });
  await page.keyboard.press(String(i + 1));
  await page.waitForTimeout(250);

  const n = await page.evaluate(() => document.querySelectorAll('.dot').length);
  for (let s = 0; s < n; s++) { await page.keyboard.press(' '); await page.waitForTimeout(220); }
  // and back, which re-runs apply() with removals
  for (let s = 0; s < n; s++) { await page.keyboard.press('ArrowLeft'); await page.waitForTimeout(120); }

  const d = await page.evaluate(() => ({
    id: JSON.parse(document.getElementById('ANIM').textContent)[
      [...document.querySelectorAll('.tab')].findIndex(t => t.getAttribute('aria-selected') === 'true')].id,
    applies: window.__perf.applies,
    frames: window.__perf.frames.filter(f => f > 0 && f < 500),
    longTasks: window.__perf.longTasks,
    tokens: document.querySelectorAll('.board .tok').length,
  }));

  const ms = d.applies.map(a => a.ms), reads = d.applies.map(a => a.reads);
  report.push({
    id: d.id, tokens: d.tokens, steps: n, calls: d.applies.length,
    applyP50: +pct(ms, .5).toFixed(2), applyP95: +pct(ms, .95).toFixed(2),
    applyMax: +Math.max(...ms, 0).toFixed(2),
    readsMax: Math.max(...reads, 0), readsTotal: reads.reduce((a, c) => a + c, 0),
    frameP95: +pct(d.frames, .95).toFixed(1), frameMax: +Math.max(...d.frames, 0).toFixed(1),
    longTasks: d.longTasks.length,
  });
}

const fails = [];
for (const r of report) {
  if (r.applyP95 > BUDGET.applyP95) fails.push(`${r.id}: apply p95 ${r.applyP95}ms > ${BUDGET.applyP95}ms`);
  if (r.applyMax > BUDGET.applyMax) fails.push(`${r.id}: apply max ${r.applyMax}ms > ${BUDGET.applyMax}ms`);
  if (r.longTasks > BUDGET.longTasks) fails.push(`${r.id}: ${r.longTasks} long task(s)`);
}
if (violations.length > BUDGET.violations)
  fails.push(`${violations.length} forced-reflow violation(s): ${violations[0]}`);

if (process.argv.includes('--json')) {
  console.log(JSON.stringify({ report, fails, violations }, null, 1));
} else {
  const pad = (s, n) => String(s).padEnd(n);
  console.log(pad('animation', 13) + pad('tok', 5) + pad('apply p50', 11) +
              pad('p95', 8) + pad('max', 8) + pad('reads/step', 12) +
              pad('frame p95', 11) + 'longTasks');
  for (const r of report)
    console.log(pad(r.id, 13) + pad(r.tokens, 5) + pad(r.applyP50 + 'ms', 11) +
                pad(r.applyP95 + 'ms', 8) + pad(r.applyMax + 'ms', 8) +
                pad(r.readsMax, 12) + pad(r.frameP95 + 'ms', 11) + r.longTasks);
  console.log('\nforced-reflow violations: ' + violations.length);
  if (fails.length) { console.log('\nOVER BUDGET:'); fails.forEach(f => console.log('  ✗ ' + f)); }
  else console.log('\nall within budget');
}

await b.close();
process.exit(fails.length ? 1 : 0);
