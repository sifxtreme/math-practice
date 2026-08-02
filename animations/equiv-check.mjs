/* equiv-check.mjs — the JS engine and the Python oracle must agree, exactly.
 *
 * engine.js is a port of specs.py. A port is only safe if something proves it is
 * still a port, so this runs BOTH over hundreds of problems and requires the emitted
 * step data to be deep-equal.
 *
 * This is not redundant with the other checks. verify_animations.py proves the data is
 * mathematically right; this proves two independent implementations, in two languages,
 * produce the same data. Together they mean a bug has to be made twice, the same way,
 * in two languages, to survive.
 *
 * Run:  node equiv-check.mjs [--n 60]
 * Exits non-zero on the first disagreement, printing the exact path that differs.
 */
import { execFileSync } from 'child_process';
import { createRequire } from 'module';
import path from 'path';
import { fileURLToPath } from 'url';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const E = require(path.join(DIR, 'engine.js'));

const N = (() => {
  const i = process.argv.indexOf('--n');
  return i > -1 ? parseInt(process.argv[i + 1], 10) : 60;
})();

// Which generator each shape goes through, on both sides.
const SHAPES = [
  { label: '2-digit x 1-digit', js: 'multByOneDigit', py: 'mult_by_one_digit', nx: 2, ny: 1 },
  { label: '3-digit x 1-digit', js: 'multByOneDigit', py: 'mult_by_one_digit', nx: 3, ny: 1 },
  { label: '4-digit x 1-digit', js: 'multByOneDigit', py: 'mult_by_one_digit', nx: 4, ny: 1 },
  { label: '5-digit x 1-digit', js: 'multByOneDigit', py: 'mult_by_one_digit', nx: 5, ny: 1 },
  { label: '2-digit x 2-digit', js: 'multMulti', py: 'mult_two_by_two', nx: 2, ny: 2 },
  { label: '3-digit x 2-digit', js: 'multMulti', py: 'mult_two_by_two', nx: 3, ny: 2 },
  { label: '3-digit x 3-digit', js: 'multMulti', py: 'mult_two_by_two', nx: 3, ny: 3 },
  { label: '4-digit x 4-digit', js: 'multMulti', py: 'mult_two_by_two', nx: 4, ny: 4 },
  { label: '2-digit / 1-digit', js: 'longDivision', py: 'long_division', nx: 2, ny: 1 },
  { label: '3-digit / 1-digit', js: 'longDivision', py: 'long_division', nx: 3, ny: 1 },
  { label: '4-digit / 1-digit', js: 'longDivision', py: 'long_division', nx: 4, ny: 1 },
  { label: '3-digit / 2-digit', js: 'longDivision', py: 'long_division', nx: 3, ny: 2 },
  { label: '4-digit / 2-digit', js: 'longDivision', py: 'long_division', nx: 4, ny: 2 },
  { label: '6-digit / 3-digit', js: 'longDivision', py: 'long_division', nx: 6, ny: 3 },
];

/* Same deterministic spread the Python sweep uses, so a failure here is reproducible
   and lines up with a failure there. */
function cases(nx, ny, n) {
  const lox = Math.pow(10, nx - 1), hix = Math.pow(10, nx) - 1;
  let loy = Math.pow(10, ny - 1);
  const hiy = Math.pow(10, ny) - 1;
  if (ny === 1) loy = 2;
  const out = [];
  for (let k = 1; out.length < n && k < 40000; k++) {
    const x = lox + (k * 313) % (hix - lox + 1);
    const y = loy + (k * 97) % (hiy - loy + 1);
    if (x < y) continue;
    if (!out.some(p => p[0] === x && p[1] === y)) out.push([x, y]);
  }
  return out;
}

/* Key order is a rendering detail, not data. Sort recursively so the comparison is
   about VALUES — otherwise the port would be pinned to Python's dict insertion order
   for no mathematical reason. */
function canon(v) {
  if (Array.isArray(v)) return v.map(canon);
  if (v && typeof v === 'object') {
    const out = {};
    for (const k of Object.keys(v).sort()) out[k] = canon(v[k]);
    return out;
  }
  if (typeof v === 'number' && Number.isInteger(v)) return v;
  return v;
}

function firstDiff(a, b, p = '') {
  if (JSON.stringify(a) === JSON.stringify(b)) return null;
  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return `${p}: length ${a.length} (js) vs ${b.length} (py)`;
    for (let i = 0; i < a.length; i++) {
      const d = firstDiff(a[i], b[i], `${p}[${i}]`);
      if (d) return d;
    }
    return null;
  }
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    const ks = [...new Set([...Object.keys(a), ...Object.keys(b)])].sort();
    for (const k of ks) {
      if (!(k in a)) return `${p}.${k}: missing in js`;
      if (!(k in b)) return `${p}.${k}: missing in py (js has ${JSON.stringify(a[k])})`;
      const d = firstDiff(a[k], b[k], `${p}.${k}`);
      if (d) return d;
    }
    return null;
  }
  return `${p}: js=${JSON.stringify(a)}  py=${JSON.stringify(b)}`;
}

// Ask Python for every case in one process — spawning per problem is what made an
// earlier version of this take minutes instead of seconds.
function pythonBatch(fn, pairs) {
  const src = `
import json, sys
import specs
pairs = json.loads(sys.stdin.read())
out = [specs.${fn}(x, y) for x, y in pairs]
print(json.dumps(out, ensure_ascii=False))
`;
  const raw = execFileSync('python3', ['-c', src], {
    cwd: DIR, input: JSON.stringify(pairs), maxBuffer: 1 << 28, encoding: 'utf8',
  });
  return JSON.parse(raw);
}

let total = 0, bad = 0;
console.log(`${'shape'.padEnd(20)}${'pairs'.padStart(6)}  result`);
for (const sh of SHAPES) {
  const pairs = cases(sh.nx, sh.ny, N);
  const pys = pythonBatch(sh.py, pairs);
  let firstBad = null;
  pairs.forEach(([x, y], i) => {
    total++;
    const js = canon(E[sh.js](x, y));
    const py = canon(pys[i]);
    const d = firstDiff(js, py);
    if (d) { bad++; if (!firstBad) firstBad = { x, y, d }; }
  });
  console.log(`${sh.label.padEnd(20)}${String(pairs.length).padStart(6)}  ` +
    (firstBad ? `✗ ${firstBad.x},${firstBad.y} → ${firstBad.d}` : `✓ identical`));
}

console.log(`\n${total} problems compared across ${SHAPES.length} shapes`);
if (bad) console.log(`${bad} DISAGREEMENT(S) — engine.js has drifted from specs.py`);
else console.log('engine.js and specs.py agree exactly');
process.exit(bad ? 1 : 0);
