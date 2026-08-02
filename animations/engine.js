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

  // ------------------------------------------- N digits x M digits

  function multMulti(top, bot) {
    if (!(bot >= 10)) throw new Error('use multByOneDigit for a single-digit multiplier');
    const tdig = digitsOf(top);
    const bdig = digitsOf(bot);
    const N = bdig.length;
    const rounds = bdig.slice().reverse();
    const partials = rounds.map((m, k) => top * m * Math.pow(10, k));
    const product = top * bot;
    const W = String(product).length;
    const col = j => W + 1 - j;
    const R_CARRY = 1, R_TOP = 2, R_BOT = 3, R_RULE1 = 4;
    const R_P = Array.from({ length: N }, (_, k) => 5 + k);
    const R_RULE2 = 5 + N, R_ANS = 6 + N;

    const toks = [], steps = [];
    const trev = tdig.slice().reverse();
    trev.forEach((d, j) => toks.push({ k: `t${j}`, r: R_TOP, c: col(j), t: String(d), cls: 'd' }));
    toks.push({ k: 'op', r: R_BOT, c: 1, t: '×', cls: 'op' });
    const botKeys = [];
    rounds.forEach((m, k) => {
      toks.push({ k: `b${k}`, r: R_BOT, c: col(k), t: String(m),
                  cls: k === 0 ? 'd hot' : 'd hot2' });
      botKeys.push(`b${k}`);
    });
    for (let k = 1; k < N; k++) toks.push({ k: `plus${k}`, r: R_P[k], c: 1, t: '+', cls: 'op' });

    const decor = [
      { kind: 'rule', k: 'rule1', r: R_RULE1, c0: 1, c1: W + 1 },
      { kind: 'rule', k: 'rule2', r: R_RULE2, c0: 1, c1: W + 1 },
    ];

    const tcols = [];
    trev.forEach((d, j) => { if (d || j === 0) tcols.push(d * Math.pow(10, j)); });
    tcols.reverse();
    const modelRows = [];
    for (let k = N - 1; k >= 0; k--) {
      modelRows.push({ v: rounds[k] * Math.pow(10, k), maps: `p${k + 1}` });
    }
    const cells = [];
    modelRows.forEach((r, ri) => tcols.forEach((cv, ci) => cells.push({ r: ri, c: ci, v: r.v * cv })));
    const model = {
      kind: 'area', h: bot, rows: modelRows,
      cols: tcols.map(v => ({ v })), cells,
      rowSums: modelRows.map(r => r.v * top), total: product,
      caption: `${top} × ${bot} as a rectangle, one strip per digit of ${bot}. `
        + modelRows.map((r, ri) =>
            `The ${r.v} strip is written row ${N - ri}, <b>${r.v * top}</b>.`).join(' '),
    };

    const setup = tdig.map((_, j) => `t${j}`).concat(['op'], botKeys, ['rule1']);
    steps.push({
      label: 'SET UP', beat: null,
      say: `${cap(NUMWORD[N])} digits on the bottom means <b>${NUMWORD[N]} `
         + `rounds</b>, so ${NUMWORD[N]} answer rows, and then you add them all up.`,
      why: 'Each digit on the bottom is a different size. The '
         + rounds.map((m, k) => (k ? `<b>${m}</b> is really <b>${m * Math.pow(10, k)}</b>` : null))
             .filter(Boolean).join(', ')
         + ". That is where each row's zeros come from.",
      show: setup, flash: botKeys, dwell: 5.0, modelRow: null,
    });

    function digitBeats(mult, d, carry, j, last, slot, ansRow, ansPre, carryPre,
                        hotKey, mrow, tensScale) {
      const raw = mult * d;
      const total = raw + carry;
      const digits = String(total).split('');
      const totcells = digits.map((ch, i) => ({ t: ch, part: i }));
      let chipFirst, chipFull;
      if (carry) {
        chipFirst = String(raw).split('').map(ch => ({ t: ch }));
        chipFull = String(raw).split('').map(ch => ({ t: ch }))
          .concat([{ t: '+', op: true },
                   { t: String(carry), arrive: `${carryPre}${j - 1}` },
                   { t: '=', op: true }], totcells);
      } else { chipFirst = totcells; chipFull = totcells; }
      const reserve = chipFull.reduce((n, c) => n + (c.op ? 22 : 30), 0) + 32;

      steps.push({
        label: `${mult} × ${d}`, beat: null,
        say: `<b>${mult} × ${d} = ${raw}.</b>`,
        why: (j === 0 && tensScale === 1 && raw >= 10)
          ? `<b>${raw}</b> — and a column holds one digit, so watch where each half of it goes.`
          : `Really <b>${mult * tensScale} × ${d * Math.pow(10, j)} = `
            + `${raw * Math.pow(10, j) * tensScale}</b>.`,
        show: [], flash: [hotKey, `t${j}`],
        bubble: { cells: chipFirst, reserveW: reserve },
        modelRow: mrow, dwell: 3.6,
      });
      if (carry) {
        steps.push({
          label: '+ THE CARRY', beat: null,
          say: `Now bring in the carry: <b>${raw} + ${carry} = ${total}</b>.`,
          why: 'The carry came from the column on the right, where it did not '
             + 'fit. This is the column it belongs in.',
          show: [], flash: [`${carryPre}${j - 1}`],
          bubble: { cells: chipFull, grewFrom: chipFirst.length, reserveW: reserve },
          trap: `<b>Multiply first, then add the carry.</b> Not `
              + `${d} + ${carry} = ${d + carry}, then × ${mult} = ${(d + carry) * mult}.`,
          modelRow: mrow, dwell: 4.8,
        });
      }

      const show = [];
      let split = [], say2, why2;
      if (last) {
        digits.slice().reverse().forEach((ch, i) => {
          const key = `${ansPre}${slot + i}`;
          toks.push({ k: key, r: ansRow, c: col(slot + i), t: ch, cls: 'd p1' });
          show.push(key);
          split.push({ part: digits.length - 1 - i, to: key });
        });
        say2 = digits.length > 1
          ? 'Nothing left on top, so <b>both digits go down</b>.'
          : `Write the <b>${total}</b>.`;
        why2 = digits.length > 1
          ? `<b>${total}</b> lands across two columns because that is where its two place values belong.`
          : 'One digit, one column.';
      } else if (total >= 10) {
        const ones = total % 10, tens = idiv(total, 10);
        const kAns = `${ansPre}${slot}`, kCar = `${carryPre}${j}`;
        toks.push({ k: kAns, r: ansRow, c: col(slot), t: String(ones), cls: 'd p1' });
        toks.push({ k: kCar, r: R_CARRY, c: col(j + 1), t: String(tens),
                    cls: 'carry' + (carryPre === 'c0' ? '' : ' carry2') });
        show.push(kAns, kCar);
        split = [{ part: 1, to: kAns }, { part: 0, to: kCar }];
        say2 = `<b>${total}</b> is two digits and only one fits in a box. The `
             + `<b>${ones}</b> drops <b>down</b>; the <b>${tens}</b> flies <b>up</b> `
             + `to the shelf above the next column.`;
        why2 = 'The part that does not fit moves one column left, which is the only '
             + 'thing a carry ever is.';
      } else {
        const kAns = `${ansPre}${slot}`;
        toks.push({ k: kAns, r: ansRow, c: col(slot), t: String(total), cls: 'd p1' });
        show.push(kAns);
        split = [{ part: 0, to: kAns }];
        say2 = `<b>${total}</b> is one digit — it drops straight down.`;
        why2 = 'Nothing needs to move left.';
      }

      steps.push({
        label: 'WHERE IT GOES', beat: null, say: say2, why: why2,
        show, flash: [], bubble: { cells: chipFull, reserveW: reserve },
        split, modelRow: mrow, dwell: 4.2,
      });
      return last ? 0 : idiv(total, 10);
    }

    rounds.forEach((m, k) => {
      const mrow = N - 1 - k;
      const pre = `p${k}_`, cpre = `c${k}_`;

      if (k) {
        const zk = [];
        for (let z = 0; z < k; z++) {
          const key = `z${k}_${z}`;
          toks.push({ k: key, r: R_P[k], c: col(z), t: '0', cls: 'd p2 zero' });
          zk.push(key);
        }
        steps.push({
          label: 'THE ZERO' + (k > 1 ? 'S' : ''), beat: null,
          say: `Round ${k + 1} uses the <b>${m}</b> — but it is <b>not ${m}</b>. It `
             + `sits ${NUMWORD[k]} place${k > 1 ? 's' : ''} to the left, so it `
             + `is really <b>${m * Math.pow(10, k)}</b>. Before you multiply anything, put `
             + `<b>${NUMWORD[k]} 0${k > 1 ? 's' : ''}</b> at the end of this row.`,
          why: `This row is <b>${m * Math.pow(10, k)} × ${top} = ${partials[k]}</b>. Every `
             + `multiple of ${m * Math.pow(10, k)} ends in ${NUMWORD[k]} `
             + `zero${k > 1 ? 's' : ''}, so this row <i>has</i> to. You are not `
             + `adding magic zeros — you are writing down where the number is.`,
          show: zk.concat([`plus${k}`]), flash: [`b${k}`].concat(zk), dwell: 5.6,
          modelRow: mrow,
          trap: `<b>This is the most common way to get a multi-digit multiply `
              + `wrong.</b> Miss the zeros and you add ${idiv(partials[k], Math.pow(10, k))} `
              + `instead of ${partials[k]}.`,
        });
        const prev = toks.filter(t => t.k.startsWith(`c${k - 1}_`)).map(t => t.k);
        if (prev.length) {
          steps.push({
            label: 'CROSS OUT', beat: null,
            say: 'Cross out the carries from the last round. They belong to that '
               + 'row and nothing else.',
            why: "They were amounts borrowed inside the previous row's "
               + 'calculation. This is a different calculation.',
            show: [], flash: [], strike: prev, dwell: 3.8,
            modelRow: mrow,
            trap: 'Leaving them there adds them a second time, and the answer '
                + 'comes out wrong with no obvious sign of why.',
          });
        }
      }

      if (m === 0) {
        const key = `${pre}${k}`;
        toks.push({ k: key, r: R_P[k], c: col(k), t: '0', cls: 'd p1' });
        steps.push({
          label: `× ${m}`, beat: null,
          say: `Round ${k + 1} multiplies by <b>0</b>. Anything times 0 is 0, so the `
             + `whole row is just <b>0</b> — no carrying, nothing to line up.`,
          why: `<b>${top} × 0 = 0.</b> The row still matters: its zeros are holding `
             + `the columns open for the rounds after it.`,
          show: [key], flash: [`b${k}`],
          bubble: { cells: [{ t: '0', part: 0 }], reserveW: 62 },
          split: [{ part: 0, to: key }], modelRow: mrow, dwell: 4.0,
        });
      } else {
        let carry = 0;
        trev.forEach((d, j) => {
          carry = digitBeats(m, d, carry, j, j === tdig.length - 1, j + k,
                             R_P[k], pre, cpre, `b${k}`, mrow, Math.pow(10, k));
        });
      }

      steps.push({
        label: `ROW ${k + 1} DONE`, beat: null,
        say: `Row ${k + 1} is <b>${partials[k]}</b> — that is <b>${m * Math.pow(10, k)} × ${top}</b>.`,
        why: `On the rectangle that is the <b>${m * Math.pow(10, k)}</b> strip, area `
           + `<b>${partials[k]}</b>.`,
        show: [], flash: [], dwell: 3.4, modelRow: mrow,
      });
    });

    const ansKeys = [];
    String(product).split('').reverse().forEach((ch, i) => {
      toks.push({ k: `a${i}`, r: R_ANS, c: col(i), t: ch, cls: 'd ans' });
      ansKeys.push(`a${i}`);
    });
    steps.push({
      label: 'ADD', beat: null,
      say: `Last move: <b>add all ${NUMWORD[N]} rows</b>. `
         + `${partials.join(' + ')} = <b>${product}</b>.`,
      why: `Which is the whole rectangle: <b>${product}</b>.`,
      show: ansKeys.concat(['rule2']), flash: ansKeys, dwell: 4.0, modelRow: 'all',
    });

    const rTop = roundHalfEven(top, -1);
    steps.push({
      label: 'CHECK', beat: null,
      say: `Sense-check: ${top} is about ${rTop}, so the answer should land near `
         + `${rTop} × ${bot} = ${rTop * bot}. We got <b>${product}</b>. ✓`,
      why: `All the little areas add to <b>${product}</b>.`,
      show: [], flash: ansKeys, dwell: 5.4, modelRow: 'all',
    });

    const mx = steps.reduce((m2, st) => (st.bubble ? Math.max(m2, st.bubble.reserveW) : m2), 0);
    steps.forEach(st => { if (st.bubble) st.bubble.reserveW = mx; });

    return { cols: W + 1, rows: R_ANS, toks, decor, steps, model, answer: product };
  }

  // ------------------------------------------- long division

  function longDivision(dividend, divisor) {
    // Asif 2026-08-01: never divide by 1 — the kid copies the number down and no
    // long division happens.
    if (!(divisor >= 2)) throw new Error('dividing by 1 is not a drill');
    if (!(dividend >= divisor)) throw new Error('the quotient would be zero; not a drill shape');
    const ddig = digitsOf(dividend);
    const W = ddig.length;
    const ndiv = String(divisor).length;
    const dcol = i => i + 1 + ndiv;
    const pv = i => Math.pow(10, W - 1 - i);
    const R_Q = 1, R_DIV = 2;

    const toks = [], steps = [], decor = [];
    ddig.forEach((d, i) => toks.push({ k: `n${i}`, r: R_DIV, c: dcol(i), t: String(d), cls: 'd' }));
    const dvKeys = [];
    String(divisor).split('').forEach((ch, i) => {
      toks.push({ k: `dv${i}`, r: R_DIV, c: i + 1, t: ch, cls: 'd hot' });
      dvKeys.push(`dv${i}`);
    });
    decor.push({ kind: 'bracket', k: 'brk', r: R_DIV, c0: ndiv + 1, c1: ndiv + W });

    const quotient = idiv(dividend, divisor), remainder = dividend % divisor;

    const setup = dvKeys.concat(['brk'], ddig.map((_, i) => `n${i}`));
    steps.push({
      label: 'SET UP', beat: null,
      say: `<b>${dividend}</b> goes inside the house, <b>${divisor}</b> stands outside. `
         + `Then you repeat four moves, in this order, forever: `
         + `<b>Divide → Multiply → Subtract → Bring down.</b>`,
      why: `The real question underneath all of it: <b>how many ${divisor}s fit inside `
         + `${dividend}?</b> You chip away at it a place value at a time — hundreds first, `
         + `then tens, then ones — instead of counting ${divisor}s one by one.`,
      show: setup, flash: dvKeys, dwell: 5.0, modelRow: null,
    });

    let row = 3;
    let cur = 0, curStart = 2, curKeys = [];
    let started = false;
    const qWritten = [];
    const ladder = [];
    let kIndex = 0;

    for (let i = 0; i < W; i++) {
      if (i === 0) { cur = ddig[0]; curStart = dcol(0); curKeys = ['n0']; }

      if (!started && cur < divisor) {
        steps.push({
          label: 'TOO SMALL', beat: null,
          say: `How many <b>${divisor}</b>s fit in <b>${cur}</b>? <b>None</b> — ${divisor} is `
             + `bigger than ${cur}. So you write <i>nothing</i> above the ${cur} and take one `
             + `more digit: look at <b>${cur * 10 + ddig[i + 1]}</b> instead.`,
          why: `Asked properly: are there any <b>${pv(i)}</b>-sized groups of ${divisor} in `
             + `${dividend}? ${divisor} × ${pv(i)} = ${divisor * pv(i)}, which is more than `
             + `${dividend}. So the answer has no ${PLACE(W - 1 - i)} digit at all — and a `
             + `leading zero would just be writing 'none' where nothing needs writing.`,
          show: [], flash: [`n${i}`, `n${i + 1}`], dwell: 5.6, modelRow: null,
          bubble: { trials: trials(cur, divisor, 0), cur, divisor, reserveW: 232 },
          trap: 'A zero at the <b>front</b> of the answer is the one zero you skip. A zero in '
              + 'the <b>middle</b> you must write. Those are different, and mixing them up is '
              + 'how a 604 turns into a 64.',
        });
        cur = cur * 10 + ddig[i + 1];
        curKeys = curKeys.concat([`n${i + 1}`]);
        continue;
      }

      started = true;
      const q = idiv(cur, divisor);
      const prod = q * divisor;
      const rem = cur - prod;
      const qcol = dcol(i);
      const p = pv(i);
      ladder.push({ q: q * p, prod: prod * p, left: null });

      const tr = trials(cur, divisor, q);
      const chip = { trials: tr, cur, divisor, reserveW: 232 };
      if (q) chip.winPart = 0;
      steps.push({
        label: 'TRY THEM', beat: 'D',
        say: `How many <b>${divisor}</b>s fit inside <b>${cur}</b>? Nobody just `
           + `<i>knows</i> this — you <b>try them</b>, and you keep the biggest one `
           + `that still fits.`,
        why: '<b>Too small</b> is the one people skip. A digit is too small when '
           + 'what is <i>left over</i> would still hold another ' + String(divisor)
           + ' — you could have fitted one more in.',
        show: [], flash: dvKeys.concat(curKeys),
        bubble: chip, modelRow: kIndex, dwell: 5.6,
      });

      toks.push({ k: `q${i}`, r: R_Q, c: qcol, t: String(q), cls: 'd quo' });
      qWritten.push(`q${i}`);
      let say, why, trap;
      if (q === 0) {
        say = `<b>D — Divide.</b> How many <b>${divisor}</b>s fit in <b>${cur}</b>? `
            + `<b>None.</b> So write a <b>0</b> up top, right above the ${ddig[i]}.`;
        why = `It means there are <b>no ${PLACE(W - 1 - i)}</b> in the answer — no groups of `
            + `${divisor * p}. That is a real fact about the answer and it needs a real digit, `
            + `because the digits after it depend on sitting in the right column.`;
        trap = `<b>Write the 0. Do not skip it.</b> Skipping it here shifts every digit after `
             + `it and the answer comes out about ten times too small.`;
      } else {
        const nxt = (q + 1) * divisor;
        say = `<b>D — Divide.</b> How many <b>${divisor}</b>s fit in <b>${cur}</b>? `
            + `<b>${cap(spell(q))}</b> — because ${q} × ${divisor} = ${prod}, `
            + `and ${q + 1} × ${divisor} = ${nxt}, which is too big.`;
        why = `That ${q} sits in the ${PLACE(W - 1 - i)} column, so it is really <b>${q * p}</b>. `
            + `You just found <b>${q * p} groups of ${divisor}</b> inside ${dividend}.`;
        trap = qWritten.length === 1
          ? 'The digit goes <b>directly above the digit you just used</b>, not off to the side. '
            + 'The column is what turns a 6 into a 600.'
          : null;
      }
      const dStep = {
        label: 'D', beat: 'D', say, why, show: [`q${i}`],
        flash: [`q${i}`].concat(dvKeys, curKeys), trap,
        bubble: JSON.parse(JSON.stringify(chip)),
        modelRow: kIndex, dwell: trap ? 4.8 : 3.6,
      };
      if (q) { dStep.split = [{ part: 0, to: `q${i}` }]; dStep.keepChip = true; }
      steps.push(dStep);

      const subTxt = String(prod);
      const subStart = qcol - (subTxt.length - 1);
      const subKeys = [];
      subTxt.split('').forEach((ch, ti) => {
        const key = `s${i}_${ti}`;
        toks.push({ k: key, r: row, c: subStart + ti, t: ch, cls: 'd subtrahend' });
        subKeys.push(key);
      });
      toks.push({ k: `m${i}`, r: row, c: subStart - 1, t: '−', cls: 'op' });
      steps.push({
        label: 'M', beat: 'M',
        say: `<b>M — Multiply.</b> ${q} × ${divisor} = <b>${prod}</b>. `
           + `Write it <b>underneath</b>, lined up under the ${cur}.`,
        why: `On paper it looks like ${prod}, but it is really <b>${prod * p}</b> — that is `
           + `${q * p} groups of ${divisor}, and it is the chunk of ${dividend} you have now `
           + `accounted for.`,
        show: subKeys.concat([`m${i}`]), flash: subKeys, dwell: 3.6, modelRow: kIndex,
        bubble: JSON.parse(JSON.stringify(chip)),
      });

      const ruleStart = Math.min(subStart - 1, curStart);
      decor.push({ kind: 'rule', k: `r${i}`, r: row + 1, c0: ruleStart, c1: qcol });
      const remTxt = String(rem);
      const remStart = qcol - (remTxt.length - 1);
      const remKeys = [];
      remTxt.split('').forEach((ch, ti) => {
        const key = `e${i}_${ti}`;
        toks.push({ k: key, r: row + 2, c: remStart + ti, t: ch, cls: 'd rem' });
        remKeys.push(key);
      });
      const sTrap = qWritten.length === 1
        ? `Check the leftover: <b>${rem} is smaller than ${divisor}</b>. It always must be. `
          + `If your leftover is ever <i>bigger</i> than ${divisor}, your digit up top was `
          + `too small — back up and make it bigger.`
        : null;
      steps.push({
        label: 'S', beat: 'S',
        say: `<b>S — Subtract.</b> ${cur} − ${prod} = <b>${rem}</b>.`,
        why: `Really <b>${cur * p} − ${prod * p} = ${rem * p}</b>. That ${rem * p} is what is still `
           + `un-divided, and it is too small to make another group of ${divisor * p}.`,
        show: [`r${i}`].concat(remKeys), flash: remKeys, trap: sTrap,
        dwell: sTrap ? 4.8 : 3.4, modelRow: kIndex,
      });

      if (i + 1 < W) {
        const nxtD = ddig[i + 1];
        const key = `bd${i}`;
        toks.push({ k: key, r: row + 2, c: dcol(i + 1), t: String(nxtD), cls: 'd drop' });
        const newCur = rem * 10 + nxtD;
        steps.push({
          label: 'B', beat: 'B',
          say: `<b>B — Bring down.</b> Pull the <b>${nxtD}</b> straight down next to the `
             + `${rem}. Now you are dividing <b>${newCur}</b>, and the four moves start again.`,
          why: `You are moving down one place value: from ${PLACE(W - 1 - i)} to `
             + `${PLACE(W - 2 - i)}. The ${rem * p} left over plus the ${nxtD * pv(i + 1)} you just `
             + `pulled down make <b>${newCur * pv(i + 1)}</b> still to divide.`,
          show: [key], flash: [`n${i + 1}`, key], dwell: 4.0, modelRow: kIndex,
        });
        cur = newCur; curStart = remStart; curKeys = remKeys.concat([key]);
        row += 3;
      } else {
        toks.push({ k: 'rlab', r: R_Q, c: ndiv + W + 1, t: `R${rem}`, cls: 'rlab' });
        steps.push({
          label: 'REMAINDER', beat: null,
          say: `Nothing left to bring down. The <b>${rem}</b> that will not split is the `
             + `<b>remainder</b>. Answer: <b>${quotient} R${rem}</b>.`,
          why: `${rem} is smaller than ${divisor}, so it cannot make even one more group. `
             + `On a word problem this is the number that decides the answer — `
             + `${rem} left over means you still need one more of whatever you are counting.`,
          show: ['rlab'], flash: ['rlab'].concat(remKeys), dwell: 4.8, modelRow: kIndex,
        });
        steps.push({
          label: 'CHECK', beat: null,
          say: `Check it by going backwards: <b>${quotient} × ${divisor} = `
             + `${quotient * divisor}</b>, plus the remainder <b>${rem}</b> `
             + `= <b>${quotient * divisor + rem}</b>. That is the number you started with. ✓`,
          why: `And the ladder adds up: `
             + `${ladder.map(l => l.q).join(' + ')} = <b>${quotient}</b>. Those are `
             + `the real sizes of the digits you wrote on top.`,
          show: [], flash: qWritten.concat(['rlab']), dwell: 5.8, modelRow: 'all',
        });
      }
      kIndex += 1;
    }

    let left = dividend;
    ladder.forEach(l => { left -= l.prod; l.left = left; });
    const model = {
      kind: 'ladder', start: dividend, divisor,
      rows: ladder, quotient, remainder,
      caption: `The same division without the shorthand. Each written digit is really a `
             + `whole chunk: ${ladder.map(l => l.q).join(' + ')} = <b>${quotient}</b> `
             + `groups of ${divisor}, with <b>${remainder}</b> left over.`,
    };

    return { cols: ndiv + W + 1, rows: row + 2, toks, decor, steps, model,
             answer: `${quotient} R${remainder}` };
  }

  // ----------------------------------- derived prose (port of describe.py)

  const ORD = ['ones', 'tens', 'hundreds', 'thousands', 'ten-thousands'];
  const ndig = n => String(Math.abs(n)).length;

  function multTraits(x, y) {
    const t = { nx: ndig(x), ny: ndig(y) };
    const tdig = digitsOf(x);
    let carries = 0;
    const ms = y < 10 ? [y] : digitsOf(y).slice().reverse();
    for (const m of ms) {
      let carry = 0;
      tdig.slice().reverse().forEach((d, j) => {
        const tot = m * d + carry;
        if (j < tdig.length - 1 && tot >= 10) carries += 1;
        carry = (j === tdig.length - 1) ? 0 : idiv(tot, 10);
      });
    }
    t.carries = carries;
    t.zero_in_top = String(x).includes('0');
    return t;
  }

  function divTraits(x, y) {
    const q = idiv(x, y), r = x % y;
    const qs = String(q);
    return {
      nx: ndig(x), ny: ndig(y), nq: qs.length,
      remainder: r !== 0,
      inner_zero: qs.length > 2 ? qs.slice(1, -1).includes('0') : false,
      skips_first: Number(String(x)[0]) < y,
    };
  }

  function okMult(a, b, want) {
    if (b < 2 || a < 10) return false;
    const t = multTraits(a, b);
    if (t.nx !== want.nx || t.ny !== want.ny) return false;
    if (want.carries && !t.carries) return false;
    if (want.zero_in_top && !t.zero_in_top) return false;
    return ndig(a * b) === want.nprod;
  }

  function okDiv(a, b, want) {
    if (b < 2 || a < b) return false;              // never divide by 1
    const t = divTraits(a, b);
    if (t.nx !== want.nx || t.ny !== want.ny || t.nq !== want.nq) return false;
    if (want.remainder && !t.remainder) return false;
    if (want.inner_zero && !t.inner_zero) return false;
    return true;
  }

  function pickTry(kind, x, y, n) {
    n = n || 3;
    const lox = Math.pow(10, ndig(x) - 1), hix = Math.pow(10, ndig(x)) - 1;
    let loy = Math.pow(10, ndig(y) - 1);
    const hiy = Math.pow(10, ndig(y)) - 1;
    if (ndig(y) === 1) loy = 2;
    const spanA = hix - lox + 1, spanB = hiy - loy + 1;
    let want, ok;
    if (kind === 'mult') { want = multTraits(x, y); want.nprod = ndig(x * y); ok = okMult; }
    else { want = divTraits(x, y); ok = okDiv; }
    const out = [];
    for (let k = 1; k < spanA * 4 + 400; k++) {
      const a = lox + (k * 37 + x) % spanA;
      const b = loy + (k * 13 + y) % spanB;
      if ((a === x && b === y) || out.some(p => p[0] === a && p[1] === b)) continue;
      if (ok(a, b, want)) { out.push([a, b]); if (out.length === n) return out; }
    }
    return out;
  }

  function describe(kind, x, y) {
    return kind === 'mult' ? describeMult(x, y) : describeDiv(x, y);
  }

  function describeMult(x, y) {
    const nx = ndig(x), ny = ndig(y);
    const t = multTraits(x, y);
    if (ny === 1) {
      return {
        title: 'Multiplying by one digit',
        skill: `${nx}-digit × 1-digit, with carrying`,
        why: 'The bottom number visits every digit on top, one at a time, right to '
           + 'left. Anything too big for its box gets parked on the shelf above the '
           + 'next column.',
        rules: [
          'Line up the <b>ones</b> column. Always.',
          'Work <b>right to left</b> — ' + ORD.slice(0, nx).join(', then ') + '.',
          '<b>Multiply first, then add the carry.</b> Never the other way round.',
          'A carry gets <b>written above</b>, not remembered.',
        ],
        tryNote: 'Every one of these has a carry in it — that is the thing being '
               + 'practised, not the times tables.'
               + (t.zero_in_top
                   ? ' One has a <b>0</b> in the middle on purpose: × 0 is still 0, '
                     + 'but a carry coming in still has to be added.' : ''),
      };
    }
    const rounds = NUMWORD[ny] || String(ny);
    return {
      title: `${ny === 2 ? 'Two' : cap(NUMWORD[ny] || String(ny))} digits times `
           + `${NUMWORD[nx] || nx} digits`,
      skill: `${nx}-digit × ${ny}-digit, ${rounds} partial products`,
      why: `${cap(rounds)} digits on the bottom means <b>${rounds} rounds</b>, so `
         + `${rounds} answer rows, then you add them. Each round after the first is `
         + `multiplying by a bigger place, which is why each row starts with one more `
         + `<b>0</b> than the row above it.`,
      rules: [
        'One round per digit on the bottom, <b>right to left</b>.',
        ny > 2
          ? '<b>Row 2 starts with one 0. Row 3 starts with two.</b> Write the zeros '
            + 'before you multiply anything.'
          : '<b>Row 2 starts with a 0 in the ones column.</b> Write the 0 before you '
            + 'multiply anything.',
        '<b>Cross out the carries</b> before starting the next round.',
        'Add all the rows at the end — that is the answer, not the last row on its own.',
      ],
      tryNote: "Before you add the rows, point at each row's zeros and count them. "
             + 'Every time.',
    };
  }

  function describeDiv(x, y) {
    const nx = ndig(x), ny = ndig(y);
    const t = divTraits(x, y);
    const big = nx >= 4 || t.inner_zero;
    const rules = [
      '<b>D</b>ivide → <b>M</b>ultiply → <b>S</b>ubtract → <b>B</b>ring down. Repeat.',
      'The answer digit goes <b>directly above</b> the digit you just used.',
      'After subtracting, the leftover must be <b>smaller than the divisor</b>. '
      + "If it isn't, your digit was too small.",
    ];
    if (t.skips_first) {
      rules.push("Doesn't fit in the first digit? Take <b>one more</b>, and write "
               + 'nothing above the first.');
    }
    if (t.inner_zero) {
      rules.push("Doesn't fit after a bring-down? <b>Write a 0 up top</b> and keep "
               + 'going. A zero at the <b>front</b> you skip; a zero in the '
               + '<b>middle</b> you must write.');
    }
    if (t.remainder) {
      rules.push('Nothing left to bring down? Whatever is left is the <b>remainder</b>.');
    }
    let why = 'Four moves, in the same order, over and over until you run out of digits: '
            + '<b>Divide, Multiply, Subtract, Bring down.</b> Never skip one, never reorder them.';
    if (big) {
      why = 'Same four moves as always — but with more digits you hit the traps that eat '
          + 'long division: the divisor not fitting in the first digit, and a '
          + '<b>0 landing in the middle of the answer</b>.';
    }
    if (ny > 1) {
      why += ` And with a <b>${ny}-digit divisor</b> you can no longer recall the answer `
           + `— every digit is an <b>estimate you then check</b>.`;
    }
    let note = 'Say the four moves out loud on every single one. Out loud is the point.';
    if (t.inner_zero) {
      note = 'All three of these have a <b>0 in the answer</b>. That is not a '
           + 'coincidence — it is the thing being practised.';
    }
    return {
      title: ny > 1 ? `Long division, ${ny}-digit divisor`
           : big ? 'Long division, big numbers' : 'Long division with a remainder',
      skill: `${nx}-digit ÷ ${ny}-digit`
           + (t.remainder ? ', remainder' : ', no remainder')
           + (t.inner_zero ? ' — and a zero in the answer' : ''),
      why, rules, tryNote: note,
    };
  }

  // one entry point: shape in, whole animation out
  function generate(kind, x, y) {
    const core = kind === 'div' ? longDivision(x, y)
               : (String(y).length === 1 ? multByOneDigit(x, y) : multMulti(x, y));
    const d = describe(kind, x, y);
    const op = kind === 'mult' ? '×' : '÷';
    return Object.assign({
      kind, x, y,
      title: d.title, skill: d.skill, why: d.why, rules: d.rules,
      traps: core.steps.filter(st => st.trap).map(st => st.trap),
      youTry: pickTry(kind, x, y).map(([a, b]) => ({
        q: `${a} ${op} ${b}`,
        a: kind === 'mult' ? String(a * b) : `${idiv(a, b)} R${a % b}`,
      })),
      tryNote: d.tryNote,
    }, {
      cols: core.cols, rows: core.rows, toks: core.toks, decor: core.decor,
      steps: core.steps, model: core.model, answer: String(core.answer),
    });
  }

  const API = { multByOneDigit, multMulti, longDivision, describe, pickTry, generate, trials, PLACE, NUMWORD, roundHalfEven, spell, cap, idiv, digitsOf };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else root.MathEngine = API;
})(typeof globalThis !== 'undefined' ? globalThis : this);
