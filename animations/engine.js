/* engine.js — the algorithm simulators, in the browser.
 *
 * WHY THIS EXISTS. The generators used to be Python that ran at build time, which
 * meant every number was baked into index.html. "Data-driven" but not dynamic: to
 * change 247 x 6 you had to rebuild. Running the generator in the page means any
 * problem can be animated on demand — including the one a kid just got wrong.
 *
 * THIS IS A PORT OF specs.py, AND THAT IS DELIBERATE, NOT DEBT.
 * `equiv-check.mjs` runs both implementations over hundreds of problems and requires
 * the emitted step data to be deep-equal. Python stops being the generator and becomes
 * the ORACLE — a second implementation, in another language, that has to agree. The
 * independence the verifier always claimed is now structural instead of a discipline.
 *
 * If you change one, change the other, and let equiv-check tell you that you did.
 *
 * Traps this port has to honour (each one caught by equiv-check when I got it wrong):
 *   - Python round() is banker's rounding: round(45, -1) is 40, not 50.
 *   - Python // floors toward negative infinity; JS / truncates toward zero.
 *   - Python's `or 0` / truthiness on 0 differs from JS on empty string.
 */
(function (root) {
  'use strict';

  const _PLACE = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands',
                  'hundred-thousands', 'millions', 'ten-millions', 'hundred-millions'];
  const PLACE = i => (i < _PLACE.length ? _PLACE[i] : `10^${i}`);
  const NUMWORD = { 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six' };

  const digitsOf = n => String(n).split('').map(Number);
  const idiv = (a, b) => Math.floor(a / b);

  /* Python's round() breaks ties to EVEN, so round(45, -1) is 40 and round(35, -1)
     is also 40. Math.round would give 50 and 40. This is the single most likely
     place for a port to drift, because it only shows up on exact .5 cases. */
  function roundHalfEven(value, ndigits) {
    const f = Math.pow(10, -ndigits);
    const scaled = value / f;
    const fl = Math.floor(scaled);
    const diff = scaled - fl;
    let r;
    if (diff > 0.5) r = fl + 1;
    else if (diff < 0.5) r = fl;
    else r = (fl % 2 === 0) ? fl : fl + 1;
    return r * f;
  }

  const SPELL = { 0: 'no', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
                  6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten' };
  const spell = n => (n in SPELL ? SPELL[n] : String(n));
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);

  // ------------------------------------------------------------- trials

  function trials(cur, divisor, q) {
    let lo, hi;
    if (q === 0) { lo = 1; hi = 1; }
    else { lo = Math.max(1, q - 1); hi = Math.min(9, q + 1); }
    const rows = [];
    for (let n = lo; n <= hi; n++) {
      const prod = n * divisor;
      const v = prod > cur ? 'big' : (cur - prod >= divisor ? 'small' : 'fits');
      const row = { n, prod, v };
      if (v === 'fits') row.part = 0;
      rows.push(row);
    }
    return rows;
  }

  // ------------------------------------------- multi-digit x 1 digit

  function multByOneDigit(top, bot) {
    if (!(bot > 0 && bot < 10)) throw new Error('this layout is for a single-digit multiplier');
    const tdig = digitsOf(top);
    const product = top * bot;
    const W = String(product).length;
    const col = j => W + 1 - j;
    const R_CARRY = 1, R_TOP = 2, R_BOT = 3, R_RULE = 4, R_ANS = 5;

    const toks = [], steps = [];
    const rev = tdig.slice().reverse();
    rev.forEach((d, j) => toks.push({ k: `t${j}`, r: R_TOP, c: col(j), t: String(d), cls: 'd' }));
    toks.push({ k: 'op', r: R_BOT, c: 1, t: '×', cls: 'op' });
    toks.push({ k: 'b0', r: R_BOT, c: col(0), t: String(bot), cls: 'd hot' });

    const decor = [{ kind: 'rule', k: 'rule1', r: R_RULE, c0: 1, c1: W + 1 }];

    const strips = [];
    rev.forEach((d, j) => {
      if (d || j === 0) strips.push({ w: d * Math.pow(10, j), area: bot * d * Math.pow(10, j), j });
    });
    strips.reverse();
    const model = {
      kind: 'area', h: bot,
      rows: [{ v: bot, maps: null }],
      cols: strips.map(s => ({ v: s.w })),
      cells: strips.map((s, i) => ({ r: 0, c: i, v: s.area, j: s.j })),
      total: product,
      caption: `${top} × ${bot} — a rectangle ${bot} tall, sliced by place value. `
             + `The slices are ${strips.map(s => s.area).join(' + ')} = ${product}, `
             + `and the algorithm is just those slices folded into columns.`,
    };

    const setupKeys = tdig.map((_, j) => `t${j}`).concat(['op', 'b0', 'rule1']);
    steps.push({
      label: 'SET UP', beat: null,
      say: `Stack them so the <b>ones line up</b>. The ${bot} on the bottom is going to `
         + `visit every digit on top, one at a time, <b>starting from the right</b>.`,
      why: `Lining up the ones column is not neatness — it is what keeps each digit `
         + `standing for the right amount. In ${top} the ${tdig[0]} is not a ${tdig[0]}, `
         + `it is <b>${tdig[0] * Math.pow(10, tdig.length - 1)}</b>.`,
      show: setupKeys, flash: ['b0'], dwell: 3.6, modelCell: null,
    });

    let carry = 0;
    const stripIndex = {};
    strips.forEach((s, i) => { stripIndex[s.j] = i; });

    rev.forEach((d, j) => {
      const raw = bot * d;
      const total = raw + carry;
      const last = j === tdig.length - 1;
      const realD = d * Math.pow(10, j);
      const digits = String(total).split('');

      const totcells = digits.map((ch, i) => ({ t: ch, part: i }));
      let chipFirst, chipFull;
      if (carry) {
        chipFirst = String(raw).split('').map(ch => ({ t: ch }));
        chipFull = String(raw).split('').map(ch => ({ t: ch }))
          .concat([{ t: '+', op: true },
                   { t: String(carry), arrive: `cy${j - 1}` },
                   { t: '=', op: true }], totcells);
      } else {
        chipFirst = totcells; chipFull = totcells;
      }
      const reserve = chipFull.reduce((n, c) => n + (c.op ? 22 : 30), 0) + 32;

      steps.push({
        label: `${bot} × ${d}`, beat: null,
        say: `<b>${bot} × ${d} = ${raw}.</b>`,
        why: j === 0
          ? (raw >= 10
              ? `<b>${raw} ones.</b> But a column only holds <i>one</i> digit — `
                + `${raw} cannot all stay here. Watch where each half goes next.`
              : `<b>${raw} ones</b>, and that fits in a single column.`)
          : `That ${d} is really <b>${realD}</b>, so this move is really `
            + `<b>${bot} × ${realD} = ${raw * Math.pow(10, j)}</b>.`,
        show: [], flash: ['b0', `t${j}`], bubble: { cells: chipFirst, reserveW: reserve },
        modelCell: (j in stripIndex) ? stripIndex[j] : null, dwell: 3.8,
      });

      if (carry) {
        steps.push({
          label: '+ THE CARRY', beat: null,
          say: `Now bring in the carry from the last column: `
             + `<b>${raw} + ${carry} = ${total}</b>.`,
          why: `That carry is not a ${carry} — it is <b>${carry * Math.pow(10, j)}</b>. `
             + `It came from the column on the right, where it did not fit, and `
             + `this is the column where it belongs.`,
          show: [], flash: [`cy${j - 1}`],
          bubble: { cells: chipFull, grewFrom: chipFirst.length, reserveW: reserve },
          trap: `<b>Multiply first, then add.</b> Doing it backwards — `
              + `${d} + ${carry} = ${d + carry}, then ${d + carry} × ${bot} = `
              + `${(d + carry) * bot} — is the mistake almost everybody makes here.`,
          modelCell: (j in stripIndex) ? stripIndex[j] : null, dwell: 5.0,
        });
      }

      const show = [];
      let split = [], say2, why2;
      if (last) {
        digits.slice().reverse().forEach((ch, i) => {
          toks.push({ k: `a${j + i}`, r: R_ANS, c: col(j + i), t: ch, cls: 'd ans' });
          show.push(`a${j + i}`);
          split.push({ part: digits.length - 1 - i, to: `a${j + i}` });
        });
        if (digits.length > 1) {
          say2 = `Nothing left to multiply, so <b>both digits go down</b> — the `
               + `<b>${digits[0]}</b> into the ${PLACE(j + 1)} column and the `
               + `<b>${digits[1]}</b> into the ${PLACE(j)} column.`;
          why2 = `<b>${total * Math.pow(10, j)}</b> = ${Number(digits[0]) * Math.pow(10, j + 1)} + `
               + `${Number(digits[1]) * Math.pow(10, j)}. Each digit sits in the column that `
               + `gives it the right size.`;
        } else {
          say2 = `Write the <b>${total}</b> in the ${PLACE(j)} column.`;
          why2 = `That ${total} is really <b>${total * Math.pow(10, j)}</b>.`;
        }
      } else if (total >= 10) {
        const ones = total % 10, tens = idiv(total, 10);
        toks.push({ k: `a${j}`, r: R_ANS, c: col(j), t: String(ones), cls: 'd ans' });
        toks.push({ k: `cy${j}`, r: R_CARRY, c: col(j + 1), t: String(tens), cls: 'carry' });
        show.push(`a${j}`, `cy${j}`);
        split = [{ part: 1, to: `a${j}` }, { part: 0, to: `cy${j}` }];
        say2 = `<b>${total}</b> is two digits and only one fits in a box. `
             + `The <b>${ones}</b> drops <b>down</b> into the ${PLACE(j)} column. `
             + `The <b>${tens}</b> flies <b>up</b> to the shelf above the next column.`;
        why2 = `Split it by size: <b>${total * Math.pow(10, j)} = ${ones * Math.pow(10, j)} + `
             + `${tens * Math.pow(10, j + 1)}</b>. The ${ones * Math.pow(10, j)} fits in the ${PLACE(j)} `
             + `column. The ${tens * Math.pow(10, j + 1)} does not — so it moves one column left, `
             + `to where ${tens * Math.pow(10, j + 1)} belongs. That is all a carry is.`;
      } else {
        toks.push({ k: `a${j}`, r: R_ANS, c: col(j), t: String(total), cls: 'd ans' });
        show.push(`a${j}`);
        split = [{ part: 0, to: `a${j}` }];
        say2 = `<b>${total}</b> is one digit, so it drops straight down into the ${PLACE(j)} column.`;
        why2 = `That ${total} is really <b>${total * Math.pow(10, j)}</b>, and nothing needs to move left.`;
      }

      steps.push({
        label: 'WHERE IT GOES', beat: null, say: say2, why: why2,
        show, flash: [], bubble: { cells: chipFull, reserveW: reserve }, split,
        modelCell: (j in stripIndex) ? stripIndex[j] : null, dwell: 4.4,
      });
      carry = last ? 0 : idiv(total, 10);
    });

    const mx = steps.reduce((m, st) => (st.bubble ? Math.max(m, st.bubble.reserveW) : m), 0);
    steps.forEach(st => { if (st.bubble) st.bubble.reserveW = mx; });

    const rough = roundHalfEven(top, -1);
    steps.push({
      label: 'CHECK', beat: null,
      say: `<b>${top} × ${bot} = ${product}.</b> Now check it's sensible: ${top} is about `
         + `${rough}, and ${rough} × ${bot} = ${rough * bot}. ${product} is right next to it. ✓`,
      why: `And the slices agree: ${strips.map(s => s.area).join(' + ')} = `
         + `<b>${product}</b>. The columns and the rectangle are the same calculation.`,
      show: [], flash: Array.from({ length: W }, (_, j) => `a${j}`), dwell: 5.4, modelCell: 'all',
    });

    return { cols: W + 1, rows: 5, toks, decor, steps, model, answer: product };
  }

  const API = { multByOneDigit, trials, PLACE, NUMWORD, roundHalfEven, spell, cap, idiv, digitsOf };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else root.MathEngine = API;
})(typeof globalThis !== 'undefined' ? globalThis : this);
