import fs from 'fs';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';

// Playwright isn't a dependency of this folder — resolve it from wherever it already
// lives on this machine rather than adding a node_modules tree next to the worksheets.
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
    // playwright's entry is CJS; Node's named-export detection misses `chromium`,
    // so fall back to the default export rather than silently binding undefined.
    const m = await import(resolved);
    chromium = m.chromium ?? m.default?.chromium;
    if (chromium) break;
  } catch { /* try the next one */ }
}
if (!chromium) {
  console.error('playwright not found. Tried:\n  ' + CANDIDATES.join('\n  ') +
    '\nSet PLAYWRIGHT_PATH=/abs/path/to/node_modules/playwright');
  process.exit(2);
}

// Renders index.html in headless Chromium and asserts what JSON inspection cannot see.
// Run:  node render-check.mjs      (needs playwright on NODE_PATH, or `npm i playwright`)
// Exits non-zero on any failure. Screenshots land in ./shots/ (gitignored).
import path from 'path';
import { fileURLToPath } from 'url';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'shots');
fs.mkdirSync(OUT, { recursive: true });

const b = await chromium.launch();
const page = await b.newPage({ viewport: { width: 1180, height: 1000 }, deviceScaleFactor: 2 });

const errs = [];
const fails = [];
page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
page.on('pageerror', e => errs.push('pageerror: ' + e.message));

await page.goto('file://' + DIR + '/index.html');
await page.waitForTimeout(400);

const report = [];

for (let i = 0; i < 4; i++) {
  await page.keyboard.press(String(i + 1));
  await page.waitForTimeout(250);
  const nSteps = await page.evaluate(() => document.querySelectorAll('.dot').length);

  await page.screenshot({ path: `${OUT}/${i}-a-start.png`, fullPage: true });
  for (let s = 0; s < Math.floor(nSteps / 2); s++) await page.keyboard.press(' ');
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${OUT}/${i}-b-mid.png`, fullPage: true });
  for (let s = 0; s < nSteps; s++) await page.keyboard.press(' ');
  await page.waitForTimeout(700);
  await page.screenshot({ path: `${OUT}/${i}-c-final.png`, fullPage: true });

  const r = await page.evaluate((idx) => {
    const A = JSON.parse(document.getElementById('ANIM').textContent)[idx];
    // every key any step reveals must actually be on screen at the end
    const want = new Set(); A.steps.forEach(s => (s.show || []).forEach(k => want.add(k)));
    const invisible = [];
    const rows = {};
    document.querySelectorAll('.board .tok, .board .decor').forEach(el => {
      const k = el.dataset.k, cs = getComputedStyle(el);
      const box = el.getBoundingClientRect();
      const seen = parseFloat(cs.opacity) > 0.35 && box.width > 0 && box.height >= 0;
      if (want.has(k) && !seen) invisible.push({ k, opacity: cs.opacity, w: box.width, h: box.height });
      if (el.classList.contains('tok') && seen) {
        const rr = el.parentElement.style.gridRow;
        (rows[rr] ||= []).push({ t: el.textContent, x: box.x, struck: el.classList.contains('struck') });
      }
    });
    const board = {};
    for (const [rr, cells] of Object.entries(rows)) {
      cells.sort((a, b) => a.x - b.x);
      board[rr] = cells.map(c => c.struck ? `(${c.t})` : c.t).join(' ');
    }
    // no two marks may visually overlap
    const boxes = [...document.querySelectorAll('.board .tok')]
      .filter(e => parseFloat(getComputedStyle(e).opacity) > 0.35)
      .map(e => ({ k: e.dataset.k, b: e.getBoundingClientRect() }));
    const overlaps = [];
    for (let x = 0; x < boxes.length; x++) for (let y = x + 1; y < boxes.length; y++) {
      const p = boxes[x].b, q = boxes[y].b;
      const ox = Math.min(p.right, q.right) - Math.max(p.left, q.left);
      const oy = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
      if (ox > 3 && oy > 3) overlaps.push([boxes[x].k, boxes[y].k]);
    }
    // every digit on the board must render at the same size; a size outlier means a
    // page-level class outranked a token style (this is how the .sub collision hid)
    const sizes = {};
    document.querySelectorAll('.board .tok').forEach(el => {
      const grp = el.classList.contains('carry') ? 'carry'
                : el.classList.contains('rlab') ? 'rlab' : 'digit';
      (sizes[grp] ||= new Set()).add(getComputedStyle(el).fontSize);
    });
    const sizeSpread = Object.fromEntries(
      Object.entries(sizes).map(([k, v]) => [k, [...v]]));
    // the pen must be visible and parked ON the mark it just made — it was silently
    // drawn on top of the digit for a whole revision because nothing checked it
    const pen = document.getElementById('pen');
    const pcs = getComputedStyle(pen), pb = pen.getBoundingClientRect();
    const lastNew = (A.steps[A.steps.length - 1].show || [])[0];
    const penState = { up: pen.classList.contains('up'), opacity: pcs.opacity,
                       w: Math.round(pb.width), h: Math.round(pb.height) };
    return {
      id: A.id, nSteps: A.steps.length, invisible, overlaps, board, sizeSpread, penState,
      pageOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      boardClipped: (w => w.scrollWidth > w.clientWidth + 1)(document.querySelector('.boardwrap')),
    };
  }, i);

  for (const [grp, vals] of Object.entries(r.sizeSpread))
    if (vals.length > 1) fails.push(`${r.id}: ${grp} marks render at mixed sizes -> ${vals}`);
  if (r.penState.w < 10 || r.penState.h < 10)
    fails.push(`${r.id}: pen has no size -> ${JSON.stringify(r.penState)}`);
  if (r.invisible.length) fails.push(`${r.id}: revealed but INVISIBLE -> ${JSON.stringify(r.invisible)}`);
  if (r.overlaps.length) fails.push(`${r.id}: marks overlap -> ${JSON.stringify(r.overlaps)}`);
  if (r.pageOverflow) fails.push(`${r.id}: page scrolls horizontally at 1180px`);
  if (r.boardClipped) fails.push(`${r.id}: board clipped at 1180px`);
  if (r.nSteps !== nSteps) fails.push(`${r.id}: dot count ${nSteps} != step count ${r.nSteps}`);
  report.push(r);
}

// The pen must land ON the mark it just wrote, without covering it.
await page.setViewportSize({ width: 1180, height: 1000 });
await page.keyboard.press('3');
await page.waitForTimeout(200);
for (let s = 0; s < 5; s++) await page.keyboard.press(' ');
await page.waitForTimeout(700);
const penFit = await page.evaluate(() => {
  const A = JSON.parse(document.getElementById('ANIM').textContent);
  const idx = [...document.querySelectorAll('.tab')].findIndex(t => t.getAttribute('aria-selected') === 'true');
  const step = A[idx].steps[[...document.querySelectorAll('.dot')].findIndex(d => d.classList.contains('now'))];
  const last = (step.show || []).filter(k => document.querySelector(`.board [data-k="${k}"]`)).pop();
  const pen = document.getElementById('pen');
  const pb = pen.getBoundingClientRect();
  const mb = document.querySelector(`.board [data-k="${last}"]`).getBoundingClientRect();
  const ox = Math.min(pb.right, mb.right) - Math.max(pb.left, mb.left);
  const oy = Math.min(pb.bottom, mb.bottom) - Math.max(pb.top, mb.top);
  return { key: last, label: step.label,
           visible: parseFloat(getComputedStyle(pen).opacity) > .5,
           overlapArea: Math.max(0, ox) * Math.max(0, oy),
           markArea: mb.width * mb.height,
           nibDist: Math.hypot((pb.left + 2) - (mb.left + mb.width / 2), (pb.top + 2) - mb.bottom) };
});
if (!penFit.visible) fails.push('pen not visible on a step that writes a mark');
if (penFit.nibDist > 40) fails.push(`pen nib ${Math.round(penFit.nibDist)}px from '${penFit.key}', the last mark of step ${penFit.label}`);
if (penFit.overlapArea > penFit.markArea * 0.3)
  fails.push(`pen covers ${Math.round(100*penFit.overlapArea/penFit.markArea)}% of the mark`);

// CHOREOGRAPHY: the pen must ARRIVE before the mark appears, and marks inside a
// step must land one after another. That sequencing is the whole point of the
// motion rewrite and no data check can see it.
await page.keyboard.press('1');
await page.waitForTimeout(250);
await page.keyboard.press(' ');           // step 0 -> 1 (setup -> first written marks)
await page.waitForTimeout(1600);
const cho = await page.evaluate(async () => {
  const A = JSON.parse(document.getElementById('ANIM').textContent);
  const ti = [...document.querySelectorAll('.tab')].findIndex(t => t.getAttribute('aria-selected') === 'true');
  const now = [...document.querySelectorAll('.dot')].findIndex(d => d.classList.contains('now'));
  const next = A[ti].steps[now + 1];
  const q = k => document.querySelector(`.board [data-k="${k}"]`);
  const keys = (next.show || []).filter(q);
  const targets = keys.map(k => { const b = q(k).getBoundingClientRect();
                                  return { k, x: b.left + b.width / 2, y: b.bottom }; });
  window.dispatchEvent(new KeyboardEvent('keydown', { key: ' ' }));
  const samples = [], t0 = performance.now();
  await new Promise(res => (function tick() {
    const t = performance.now() - t0, pb = document.getElementById('pen').getBoundingClientRect();
    samples.push({ t, nib: [pb.left + 2, pb.top + 2],
                   op: keys.map(k => +getComputedStyle(q(k)).opacity) });
    if (t > 1500) res(); else requestAnimationFrame(tick);
  })());
  return { keys, targets, samples, flies: (next.fly || []).map(f => f.k) };
});

const inkAt = cho.keys.map((_, i) => {
  const s = cho.samples.find(s => s.op[i] > 0.5);
  return s ? s.t : null;
});
const nibGap = cho.keys.map((_, i) => {
  const s = cho.samples.find(s => s.op[i] > 0.5);
  if (!s) return null;
  return Math.hypot(s.nib[0] - cho.targets[i].x, s.nib[1] - cho.targets[i].y);
});
if (inkAt.some(v => v === null)) fails.push(`choreography: a mark never reached opacity>0.5`);
else {
  for (let i = 1; i < inkAt.length; i++)
    if (inkAt[i] <= inkAt[i - 1] + 30)
      fails.push(`choreography: marks ${cho.keys[i-1]}/${cho.keys[i]} land together ` +
                 `(${Math.round(inkAt[i-1])}ms vs ${Math.round(inkAt[i])}ms) — no stagger`);
  nibGap.forEach((g, i) => {
    if (cho.flies.includes(cho.keys[i])) return;   // carries loft in on their own
    if (g > 45) fails.push(`choreography: mark ${cho.keys[i]} inked while the pen was ` +
                           `${Math.round(g)}px away — pen is not leading`);
  });
}
const choReport = { keys: cho.keys, flies: cho.flies, inkAt: inkAt.map(v => v && Math.round(v)),
                    nibGap: nibGap.map(v => v && Math.round(v)) };

// Back button must actually un-write marks
await page.keyboard.press('1');
await page.waitForTimeout(200);
for (let s = 0; s < 9; s++) await page.keyboard.press(' ');
await page.waitForTimeout(400);
const atEnd = await page.evaluate(() => document.querySelectorAll('.board .tok.on').length);
for (let s = 0; s < 9; s++) await page.keyboard.press('ArrowLeft');
await page.waitForTimeout(400);
const atStart = await page.evaluate(() => document.querySelectorAll('.board .tok.on').length);
if (!(atStart < atEnd)) fails.push(`Back button does not un-write: ${atEnd} -> ${atStart}`);

// narrow viewport
await page.setViewportSize({ width: 390, height: 900 });
await page.keyboard.press('4');
await page.waitForTimeout(200);
for (let s = 0; s < 20; s++) await page.keyboard.press(' ');
await page.waitForTimeout(600);
await page.screenshot({ path: `${OUT}/narrow-final.png`, fullPage: true });
const narrow = await page.evaluate(() => ({
  overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
}));
if (narrow.overflow) fails.push('page scrolls horizontally at 390px');

// dark mode
const dark = await b.newPage({ viewport: { width: 1180, height: 1000 }, colorScheme: 'dark', deviceScaleFactor: 2 });
await dark.goto('file://' + DIR + '/index.html');
await dark.keyboard.press('3');
await dark.waitForTimeout(200);
for (let s = 0; s < 20; s++) await dark.keyboard.press(' ');
await dark.waitForTimeout(600);
await dark.screenshot({ path: `${OUT}/dark-final.png`, fullPage: true });

console.log(JSON.stringify({ errs, fails, narrow, choReport, report }, null, 1));
await b.close();
process.exit(fails.length || errs.length ? 1 : 0);
