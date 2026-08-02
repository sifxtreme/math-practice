// capture_animation.mjs — screenshot every step of an animation, for making a GIF.
//
//   # 1. start a headless Chrome with a debug port
//   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
//     --headless=new --disable-gpu --no-sandbox --no-first-run \
//     --remote-debugging-port=9333 --user-data-dir=/tmp/ud --window-size=1200,1250 \
//     about:blank &
//
//   # 2. drive it: <url> <tabIndex> <outDir> [clip "x,y,w,h"]
//   node capture_animation.mjs "file://$PWD/site/animations/index.html" 2 /tmp/frames "91,474,350,354"
//
//   # 3. assemble (drop the tail frames where only the pencil moves)
//   magick -delay 45 /tmp/frames/f0[01][0-9].png -delay 260 /tmp/frames/f020.png \
//          -loop 0 -layers Optimize multiplication.gif
//
// WHY CDP AND NOT PLAYWRIGHT: nothing to install. Node 22 ships a global WebSocket,
// and Chrome's DevTools Protocol is enough to call the page's own pick()/step()
// between screenshots. We launch the browser ourselves, so we are never attaching to
// a Chrome someone else owns.
//
// The board is a FIXED size — it reserves space for every row up front — so one clip
// works for all frames. Get it with:
//   document.querySelector('.board').getBoundingClientRect()
//
// This file lives in the repo because the first version lived in a temp dir and was
// gone after a reboot, with the GIF already published and no way to remake it.

import { writeFileSync, mkdirSync, rmSync } from 'node:fs';

const PORT = Number(process.env.PORT || 9333);
const [URL_, TAB_S, OUT, CLIP] = process.argv.slice(2);
const TAB = Number(TAB_S ?? 0);

if (!URL_ || !OUT) {
  console.error('usage: node capture_animation.mjs <url> <tabIndex> <outDir> [x,y,w,h]');
  process.exit(1);
}

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

const targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
const page = targets.find((t) => t.type === 'page');
if (!page) throw new Error(`no page target on :${PORT} — is Chrome running with --remote-debugging-port?`);

const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));

let id = 0;
const pending = new Map();
ws.onmessage = (m) => {
  const msg = JSON.parse(m.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
};
const send = (method, params = {}) =>
  new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const evalJs = async (expr) =>
  (await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }))
    .result?.result?.value;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

await send('Page.enable');
await send('Runtime.enable');
await send('Page.navigate', { url: URL_ });
await sleep(2500);

await evalJs(`pick(${TAB})`);
await sleep(700);

const clip = CLIP
  ? (([x, y, w, h]) => ({ x, y, width: w, height: h, scale: 2 }))(CLIP.split(',').map(Number))
  : undefined;

let n = 0;
const shoot = async () => {
  const r = await send('Page.captureScreenshot', clip ? { format: 'png', clip } : { format: 'png' });
  const b64 = r.result?.data;
  if (!b64) return;
  writeFileSync(`${OUT}/f${String(n).padStart(3, '0')}.png`, Buffer.from(b64, 'base64'));
  n++;
};

await shoot();                                  // opening state
for (let i = 0; i < 30; i++) {
  await evalJs('typeof step === "function" ? step(1) : null');
  await sleep(650);                             // let the CSS transition land
  await shoot();
}

// The animation keeps nudging the pencil after the maths is done, so trailing frames
// are never byte-identical — you cannot auto-trim on a checksum. Eyeball the last few
// and cut where the answer completes.
console.log(`  captured ${n} frames -> ${OUT}`);
console.log('  NOTE: trim the tail by hand; late frames differ only by pencil position.');
ws.close();
process.exit(0);
