// Drive the page the way a person does: mash the buttons, let autoplay run, switch
// tabs mid-animation, then do the whole thing on a phone. Correctness checks live in
// render-check.mjs; this one is for the things that are technically fine and still
// unusable — it is what caught Next/Play sitting 1128px below the board on a phone.
// Run: node user-check.mjs
import { createRequire } from 'module'; import { pathToFileURL } from 'url'; import fs from 'fs';
const req = createRequire(import.meta.url);
let chromium;
for (const c of [process.env.PLAYWRIGHT_PATH, `${process.env.HOME}/code/e2e/node_modules/playwright`, 'playwright'].filter(Boolean)) {
  try { const m = await import(c === 'playwright' ? c : pathToFileURL(req.resolve(c)).href);
        chromium = m.chromium ?? m.default?.chromium; if (chromium) break; } catch {}
}
if (!chromium) { console.error('playwright not found'); process.exit(2); }

import path from 'path';
import { fileURLToPath } from 'url';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const URL = 'file://' + DIR + '/index.html';
const OUT = path.join(DIR, 'shots-user');
fs.mkdirSync(OUT, { recursive: true });

const found = [];
const note = (sev, s) => { found.push(`[${sev}] ${s}`); };

const b = await chromium.launch();
const page = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
const errs = [];
page.on('pageerror', e => errs.push('pageerror: ' + e.message));
page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
await page.goto(URL);
await page.waitForTimeout(400);

const state = () => page.evaluate(() => {
  const A = JSON.parse(document.getElementById('ANIM').textContent);
  const ti = [...document.querySelectorAll('.tab')].findIndex(t => t.getAttribute('aria-selected') === 'true');
  const si = [...document.querySelectorAll('.dot')].findIndex(d => d.classList.contains('now'));
  const a = A[ti];
  const shouldShow = new Set();
  a.steps.slice(0, si + 1).forEach(s => (s.show || []).forEach(k => shouldShow.add(k)));
  const wrong = [];
  document.querySelectorAll('.board [data-k]').forEach(el => {
    const k = el.dataset.k, op = +getComputedStyle(el).opacity;
    const want = shouldShow.has(k);
    if (want && op < 0.5) wrong.push({ k, op, inline: el.style.opacity, expected: 'visible' });
    if (!want && op > 0.5) wrong.push({ k, op, expected: 'hidden' });
  });
  return { tab: ti, step: si, steps: a.steps.length, wrong,
           playing: document.getElementById('play').textContent.includes('Pause'),
           penUp: document.getElementById('pen').classList.contains('up'),
           say: document.getElementById('say').textContent.slice(0, 45) };
});

// ---------- 1. A kid mashes Next as fast as the key repeats -------------
await page.keyboard.press('4');                       // the longest one, 15 steps
await page.waitForTimeout(300);
for (let i = 0; i < 25; i++) { await page.keyboard.down(' '); await page.keyboard.up(' '); }
await page.waitForTimeout(120);                       // barely any settle time
let s = await state();
if (s.wrong.length) note('BUG', `mashing Next left ${s.wrong.length} mark(s) in the wrong state: ` +
  JSON.stringify(s.wrong.slice(0, 4)));
if (s.step !== s.steps - 1) note('BUG', `mashing Next stopped at step ${s.step} of ${s.steps - 1}`);
await page.screenshot({ path: `${OUT}/1-mashed-next.png`, fullPage: true });

// ---------- 2. ...then mashes Back just as fast -------------------------
for (let i = 0; i < 25; i++) { await page.keyboard.press('ArrowLeft'); }
await page.waitForTimeout(150);
s = await state();
if (s.wrong.length) note('BUG', `mashing Back left ${s.wrong.length} mark(s) wrong: ` +
  JSON.stringify(s.wrong.slice(0, 4)));
if (s.step !== 0) note('BUG', `mashing Back stopped at step ${s.step}, not 0`);
if (s.penUp) note('POLISH', 'pen still showing after rewinding to the setup step');

// ---------- 3. Autoplay: does the narration outrun the drawing? ---------
await page.keyboard.press('1');
await page.waitForTimeout(250);
const race = await page.evaluate(async () => {
  const out = [];
  document.getElementById('play').click();
  const t0 = performance.now();
  let lastStep = -1;
  await new Promise(res => {
    const iv = setInterval(() => {
      const si = [...document.querySelectorAll('.dot')].findIndex(d => d.classList.contains('now'));
      if (si !== lastStep) { out.push({ si, t: Math.round(performance.now() - t0),
        running: document.getAnimations().filter(a => a.playState === 'running'
          && a.effect?.getTiming?.().iterations !== Infinity).length }); lastStep = si; }
      if (!document.getElementById('play').textContent.includes('Pause')) { clearInterval(iv); res(); }
    }, 40);
  });
  return out;
});
for (let i = 1; i < race.length; i++) {
  const gap = race[i].t - race[i - 1].t;
  if (gap < 900) note('PACING', `autoplay advanced step ${race[i-1].si}→${race[i].si} after only ${gap}ms`);
}
// (a check for "animations still running at the step boundary" was removed: apply()
//  starts the next step's animations, so it fired on every correct run. The gap check
//  above is the real test — autoplay dwell must exceed the ~700ms drawing time.)

// ---------- 4. Switching tabs mid-animation ----------------------------
await page.keyboard.press('3');
await page.waitForTimeout(120);
await page.keyboard.press(' ');
await page.waitForTimeout(60);                        // interrupt mid-draw
await page.keyboard.press('2');
await page.waitForTimeout(900);
s = await state();
if (s.wrong.length) note('BUG', `switching tabs mid-draw left ${s.wrong.length} mark(s) wrong: ` +
  JSON.stringify(s.wrong.slice(0, 3)));
if (s.playing) note('BUG', 'still in Play mode after switching tabs');

// ---------- 5. Jump around with the progress dots ----------------------
const dots = await page.locator('.dot').count();
for (const idx of [dots - 1, 2, dots - 3, 0, Math.floor(dots / 2)]) {
  await page.locator('.dot').nth(idx).click();
  await page.waitForTimeout(1400);   // let the chain finish; mid-sequence is not a state
  const st = await state();
  if (st.wrong.length) note('BUG', `jumping to dot ${idx} left ${st.wrong.length} mark(s) wrong`);
}

// ---------- 6. Space while the speed dropdown has focus ----------------
await page.locator('#speed').focus();
const beforeSel = (await state()).step;
await page.keyboard.press(' ');
await page.waitForTimeout(200);
if ((await state()).step !== beforeSel) note('BUG', 'space advanced the step while the speed select had focus');
await page.locator('body').click({ position: { x: 5, y: 5 } });

// ---------- 7. The you-try reveal buttons ------------------------------
await page.keyboard.press('1');
await page.waitForTimeout(200);
const tb = page.locator('.tryrow button').first();
await tb.click(); await page.waitForTimeout(120);
const shown = await page.locator('.trya').first().evaluate(e => getComputedStyle(e).visibility);
if (shown !== 'visible') note('BUG', 'you-try "show" did not reveal the answer');
await tb.click(); await page.waitForTimeout(120);
if (await page.locator('.trya').first().evaluate(e => getComputedStyle(e).visibility) !== 'hidden')
  note('BUG', 'you-try "show" did not toggle back');

// ---------- 8. Phone. Tap targets, reachability, no sideways scroll ----
const phone = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3,
                                isMobile: true, hasTouch: true });
await phone.goto(URL);
await phone.waitForTimeout(500);
const touch = await phone.evaluate(() => {
  const small = [];
  document.querySelectorAll('button, select, a').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && r.height < 40 && !el.classList.contains('dot'))
      small.push({ what: (el.textContent || el.tagName).trim().slice(0, 22), h: Math.round(r.height) });
  });
  const board = document.querySelector('.boardwrap');
  return { small, sideways: document.documentElement.scrollWidth > innerWidth + 1,
           boardScrolls: board.scrollWidth > board.clientWidth + 1,
           boardTop: Math.round(board.getBoundingClientRect().top),
           controlsTop: Math.round(document.querySelector('.controls').getBoundingClientRect().top),
           pageH: document.documentElement.scrollHeight };
});
if (touch.sideways) note('BUG', 'page scrolls sideways on a 390px phone');
if (touch.boardScrolls) note('POLISH', 'board itself scrolls sideways on a phone');
if (touch.small.length) note('POLISH', `${touch.small.length} tap target(s) under 40px tall: ` +
  JSON.stringify(touch.small.slice(0, 5)));
if (touch.controlsTop > 844 || touch.controlsTop < 0) note('UX', `Next/Play are ${touch.controlsTop}px down — off-screen on a ` +
  `phone, so you must scroll away from the board to advance it`);
await phone.screenshot({ path: `${OUT}/8-phone.png`, fullPage: false });
await phone.evaluate(() => document.querySelector('.controls').scrollIntoView({ block: 'center' }));
await phone.screenshot({ path: `${OUT}/8-phone-controls.png`, fullPage: false });

console.log(JSON.stringify({ errs, touchSummary: touch, race, findings: found }, null, 1));
await b.close();

process.exit(found.some(f => f.startsWith('[BUG]') || f.startsWith('[UX]')) || errs.length ? 1 : 0);
