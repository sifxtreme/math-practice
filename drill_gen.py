"""drill_gen.py — generate long-division drill sheets sized to a time budget.

Asif, 2026-08-01: "the goal is for the kids to do this in 5 minutes ... let's create
our math generator for drills."

WHAT THIS DOES DIFFERENTLY FROM math-drills.com
-----------------------------------------------
1. **Sized by clock, not by page.** The count comes from `drill_cost.py`, which prices
   a problem by how many marks the written method requires. math-drills ships 20
   problems of 3-digit / 1-digit; that is a ~16 minute sheet against a 5 minute target.
2. **No degenerate problems.** Divisors are 2-9. A divide-by-1 is a copy, not a
   division -- Asif, 2026-08-01, after 7 of 10 math-drills variants were measured
   leaking them (see DRILLS.md).
3. **The grid forces the work.** Every mark the method requires gets its own printed
   box, so the steps cannot be skipped on the way to an answer. See AGENTS.md
   "Showing the work IS the assignment".

The layout is derived by SIMULATING the algorithm, which is the only way to know how
many working rows a given problem needs -- 347/4 needs fewer rows than 913/7, and a
fixed-size grid would be wrong for one of them.

Output is one sheet per kid plus an answer key each, matching what
`print-worksheet.sh` already expects, so the existing print path works unchanged.

Names come from `kids.local.json` (gitignored) at render time — this file keys on
`kid1` / `kid2` and never hardcodes a name. See README.md "Setting it up for your
kids".

    python3 drill_gen.py --skill div --seed 20260801
    python3 verify_drills.py
    ./print-worksheet.sh worksheet-division-drill.html --dry-run
"""

import argparse
import html
import json
import os
import random
import sys

import drill_cost
from kids_config import kids_by_id, kid_name

# --------------------------------------------------------------------------
# problem generation
# --------------------------------------------------------------------------

MIN_DIVISOR = 2      # 1 is a copy, 0 is undefined. Never generate either.
MAX_DIVISOR = 9


def make_division(rng, dividend_digits, want_remainder=True, tries=500):
    """One long-division problem with the degenerate cases excluded.

    want_remainder: math-drills' `_all_remainders_` behaviour. The remainder IS the
    skill being drilled, so a problem that divides evenly spends a slot without
    exercising it.
    """
    lo = 10 ** (dividend_digits - 1)
    hi = 10 ** dividend_digits - 1
    for _ in range(tries):
        d = rng.randint(MIN_DIVISOR, MAX_DIVISOR)
        n = rng.randint(lo, hi)
        if want_remainder and n % d == 0:
            continue
        if n < d:                       # quotient would be 0 -- not a drill shape
            continue
        return n, d
    raise RuntimeError(f"could not build a {dividend_digits}-digit problem")


def problem_set(rng, dividend_digits, count, want_remainder=True):
    """`count` distinct problems, no repeats within a sheet."""
    seen, out = set(), []
    while len(out) < count:
        n, d = make_division(rng, dividend_digits, want_remainder)
        if (n, d) in seen:
            continue
        seen.add((n, d))
        out.append((n, d))
    return out


def make_multiplication(rng, a_digits, b_digits, tries=500):
    """One standard-algorithm multiplication, degenerate cases excluded.

    THE MULTIPLIER'S DIGITS ARE ALL 2-9, and that constraint is not the same as the
    one on division. A 0 or 1 digit in the MULTIPLIER produces a partial-product row
    of all zeros or a bare copy of the multiplicand -- Asif's "multiplying by 0 or 1
    is generally stupid", one whole row of the sheet spent on nothing. math-drills
    ships them (`48 x 80` was on the sheet measured 2026-08-01).

    THE MULTIPLICAND KEEPS ITS 0s AND 1s. `105 x 7` is a good problem: the interior
    zero is exactly where place value gets tested. Only the multiplier is constrained.

    Note this is NOT about the placeholder zero. That comes from the PLACE -- the
    second partial row is shifted a column left whatever its digits are -- so
    constraining the multiplier costs nothing pedagogically.
    """
    a_lo, a_hi = 10 ** (a_digits - 1), 10 ** a_digits - 1
    for _ in range(tries):
        a = rng.randint(a_lo, a_hi)
        b_digits_list = [rng.randint(2, 9) for _ in range(b_digits)]
        b = int("".join(str(x) for x in b_digits_list))
        if len(str(b)) != b_digits:
            continue
        return a, b
    raise RuntimeError(f"could not build a {a_digits}x{b_digits} problem")


def problem_set_mul(rng, a_digits, b_digits, count):
    seen, out = set(), []
    while len(out) < count:
        a, b = make_multiplication(rng, a_digits, b_digits)
        if (a, b) in seen:
            continue
        seen.add((a, b))
        out.append((a, b))
    return out


# --------------------------------------------------------------------------
# the algorithm, simulated one written mark at a time
# --------------------------------------------------------------------------

def trace_division(dividend, divisor):
    """Return (rows, marks) laying out the standard school method on a grid.

    Grid columns: 0 = divisor, 1 = bracket, 2..2+W-1 = the dividend's digits.
    Grid rows:    0 = quotient, 1 = dividend, then two rows per productive step
                  (the product being subtracted, then the difference).

    A mark is (row, col, text, kind) where kind is 'given' (pre-printed) or
    'fill' (an empty box on the worksheet, a digit on the key).
    """
    ds = str(dividend)
    W = len(ds)
    C = lambda i: 2 + i                      # grid col of dividend digit i

    marks = [(1, 0, str(divisor), "given")]
    for i, ch in enumerate(ds):
        marks.append((1, C(i), ch, "given"))

    # which steps actually produce a quotient digit
    steps = []
    rem, started = 0, False
    for i, ch in enumerate(ds):
        cur = rem * 10 + int(ch)
        q = cur // divisor
        if q == 0 and not started:
            rem = cur
            continue
        started = True
        prod = q * divisor
        rem = cur - prod
        steps.append({"i": i, "q": q, "prod": prod, "rem": rem})

    row = 2
    for k, st in enumerate(steps):
        i, last = st["i"], (k == len(steps) - 1)
        marks.append((0, C(i), str(st["q"]), "fill"))          # quotient digit

        p = str(st["prod"])                                     # product, right-aligned at col i
        marks.append((row, C(i) - len(p), "−", "given"))   # the minus sign is a prompt
        for j, ch in enumerate(p):
            marks.append((row, C(i) - len(p) + 1 + j, ch, "fill"))
        row += 1

        r = str(st["rem"])                                      # difference, right-aligned at col i
        for j, ch in enumerate(r):
            marks.append((row, C(i) - len(r) + 1 + j, ch, "fill"))
        if last:
            marks.append((row, C(i) - 1, "R", "given"))
            # the remainder is the answer -- restate it in the R slot
        else:
            marks.append((row, C(i + 1), ds[i + 1], "fill"))    # bring down
        row += 1

    cols = 2 + W
    # Boxes: the quotient line, and the working area under the bracket. Columns 0
    # and 1 are the divisor and the bracket wall — never boxes.
    boxes = {(0, c) for c in range(2, cols)}
    boxes |= {(r, c) for r in range(2, row) for c in range(2, cols)}
    return row, cols, marks, rules_div(), boxes


def rules_div():
    """Division draws its rule as the bracket roof, not as a row rule."""
    return set()


def carries_for(a, digit):
    """The carry digits a single-digit multiplication writes, by grid column offset.

    Returns {slots_from_right: carry}. A carry generated while multiplying the digit
    j places from the right is written ABOVE the digit at j+1 — that is where the
    child has to read it back. The final carry off the left end is not a carry mark
    at all; it becomes the leading digit of the product.
    """
    A = str(a)
    out, carry = {}, 0
    for j, ch in enumerate(reversed(A)):
        v = int(ch) * digit + carry
        carry = v // 10
        if carry and j + 1 < len(A):
            out[j + 1] = carry
    return out


def trace_multiplication(a, b, carry_row=True):
    """Standard algorithm on a grid: one partial-product row per multiplier digit.

    Rows: an optional carry row, then the multiplicand, then the x and the multiplier,
    then one row per partial product, then the final sum when there is more than one
    partial to add. `rules` holds the rows needing a horizontal line drawn above.

    THE CARRY ROW EXISTS ONLY FOR A SINGLE-DIGIT MULTIPLIER, and that is deliberate.
    A 1-digit multiplier produces exactly ONE partial product -- the answer itself --
    so without carry boxes the sheet has one row to fill and forces no work at all
    (AGENTS.md "Showing the work IS the assignment"). The carries ARE the method
    there. With a 2+ digit multiplier the partial rows already carry the method, and
    a shared carry row would be wrong anyway: each partial generates its own carries
    over the same columns, which is why children erase them between rows.

    Everything is right-aligned to the last column, as it is written by hand; the
    shift that produces the placeholder zero falls out of that alignment.
    """
    A, B = str(a), str(b)
    partials = [a * int(ch) * (10 ** j) for j, ch in enumerate(reversed(B))]
    product = a * b
    width = max(len(str(product)), max(len(str(p)) for p in partials), len(A), len(B))
    cols = width + 1                      # +1 for the x sign
    R = lambda s, row, kind: [(row, cols - len(s) + k, ch, kind)
                              for k, ch in enumerate(s)]

    show_carry = carry_row and len(B) == 1
    off = 1 if show_carry else 0
    marks, rules, boxes = [], set(), set()

    if show_carry:
        for slot, c in carries_for(a, int(B)).items():
            marks.append((0, cols - 1 - slot, str(c), "carry"))
        # Box every multiplicand column except the ones place -- a carry can never
        # land there, and an empty box the child must leave blank teaches nothing.
        for k in range(1, len(A)):
            boxes.add((0, cols - 1 - k))

    marks += R(A, off, "given")
    marks.append((1 + off, cols - len(B) - 1, "×", "given"))
    marks += R(B, 1 + off, "given")
    rules.add(2 + off)                     # rule under the multiplier

    row = 2 + off
    for p in partials:
        marks += R(str(p), row, "fill")
        boxes.update((row, c) for c in range(cols))
        row += 1
    if len(partials) > 1:
        rules.add(row)                     # rule under the partials
        marks += R(str(product), row, "fill")
        boxes.update((row, c) for c in range(cols))
        row += 1

    return row, cols, marks, rules, boxes


def verify_mul(a, b, marks, rules):
    """Re-derive the product from the MARKS, not from `a * b`.

    Reads each partial-product row back off the grid and the final row, then checks
    the partials sum to the final row AND that the final row equals a*b. A shift bug
    — the placeholder zero landing in the wrong column — fails the first check.
    Carry marks are checked separately against a fresh computation.
    """
    carry_marks = {}
    for (r, c, t, kind) in marks:
        if kind == "carry":
            carry_marks[c] = t
    if carry_marks:
        cols = max(c for (_, c, _, _) in marks) + 1
        want = {cols - 1 - slot: str(v) for slot, v in carries_for(a, int(str(b))).items()}
        if carry_marks != want:
            return False, f"carries {carry_marks} != {want}"

    by_row = {}
    for (r, c, t, kind) in marks:
        if kind == "fill":
            by_row.setdefault(r, []).append((c, t))
    if not by_row:
        return False, "no fill marks"
    rows = sorted(by_row)
    vals = [int("".join(t for _, t in sorted(by_row[r]))) for r in rows]
    nb = len(str(b))
    if nb > 1:
        *partials, total = vals
        if sum(partials) != total:
            return False, f"partials {partials} sum to {sum(partials)}, row says {total}"
    else:
        total = vals[-1]
    if total != a * b:
        return False, f"{a}*{b} = {a*b}, grid says {total}"
    return True, f"{a}*{b} = {total}"


def verify(dividend, divisor, marks):
    """Re-derive the answer from the MARKS, independently of how they were built.

    Reads the quotient digits back off row 0 and the remainder off the R row, then
    checks q * divisor + r == dividend. A layout bug that drops or misplaces a digit
    fails here rather than reaching paper.
    """
    q_cells = sorted([m for m in marks if m[0] == 0], key=lambda m: m[1])
    q = int("".join(c[2] for c in q_cells)) if q_cells else 0
    r_rows = [m[0] for m in marks if m[2] == "R"]
    if not r_rows:
        return False, "no R mark"
    rr = max(r_rows)
    r_cells = sorted([m for m in marks if m[0] == rr and m[3] == "fill"], key=lambda m: m[1])
    r = int("".join(c[2] for c in r_cells)) if r_cells else 0
    if q * divisor + r != dividend:
        return False, f"{q}*{divisor}+{r} != {dividend}"
    if not (0 <= r < divisor):
        return False, f"remainder {r} out of range for divisor {divisor}"
    return True, f"{dividend}/{divisor} = {q} R{r}"


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

CSS = """
* { box-sizing: border-box; }
body { font-family: Georgia, 'Times New Roman', serif; margin: 0; color: #111; }
.sheet { width: 7.7in; min-height: 10in; padding: 0.30in 0.35in; page-break-after: always; }
.sheet:last-child { page-break-after: auto; }
.head { display:flex; justify-content:space-between; align-items:baseline;
        border:1.5px solid #111; padding:7px 12px; margin-bottom:10px; }
.head h1 { font-size: 17px; margin: 0; letter-spacing: .2px; }
.meta { font-size: 12px; }
.meta span { display:inline-block; min-width:96px; border-bottom:1px solid #111; }
.instr { text-align:center; font-size:12.5px; margin: 0 0 12px; }
.grid-wrap { display:flex; flex-wrap:wrap; gap: 16px 8px; }
.prob { display:grid; grid-auto-flow:row; justify-content:start; align-content:start;
        margin-bottom: 4px; }
.n  { font-size:10px; color:#777; grid-row:1; grid-column:1; align-self:center; }
.c  { width:23px; height:23px; font-size:15px; line-height:21px; text-align:center; }
/* a box the kid fills -- this is the whole point of the sheet */
.f  { border:1px solid #c9c9c9; background:#fff; }
.g  { font-weight:600; }
/* the division bracket: left wall + roof over the dividend */
.dv { border-right:2px solid #111; }
.rf { border-top:2px solid #111; }
/* the two rules of a written multiplication. Declared after .f so it wins the
   top border on a cell that is also a fill box. */
.rl { border-top:2px solid #111; }
/* carry boxes: deliberately small and set high, the way a carry is actually
   written — a cramped mark above the column, not a full digit in the row. */
.c.cr { height:13px; line-height:11px; font-size:10px; align-self:end;
        border-style:dashed; color:#8a1538; }
.key .f { border-color:#e6e6e6; }
/* .key .f is (0,2,0) and would otherwise repaint the multiplication rules and the
   division roof light grey — they are (0,1,0) and lose. The lines then disappear
   from the KEY only, which no data check can see. Caught by rendering, 2026-08-01. */
.key .rl, .key .rf { border-top-color:#111; }
.key .dv { border-right-color:#111; }
.key .f.q { color:#8a1538; font-weight:700; }
.foot { margin-top:14px; border:1.5px solid #111; padding:5px; text-align:center;
        font-size:11px; }
.note { font-size:11px; color:#555; margin-top:8px; }
"""


def render_problem(idx, x, y, show_answers, shape="div"):
    if shape == "div":
        rows, cols, marks, rules, boxes = trace_division(x, y)
    else:
        rows, cols, marks, rules, boxes = trace_multiplication(x, y)

    grid = {}
    for (r, c, t, kind) in marks:
        grid[(r, c)] = (t, kind)

    out = [f'<div class="prob" style="grid-template-columns:repeat({cols + 1},23px)">']
    out.append(f'<span class="n" style="grid-row:1;grid-column:1">{idx}.</span>')
    for r in range(rows):
        for c in range(cols):
            cell = grid.get((r, c))
            classes = ["c"]
            style = f"grid-row:{r + 1};grid-column:{c + 2}"
            txt = ""
            if cell:
                t, kind = cell
                txt = html.escape(t)
                if kind == "given":
                    classes.append("g")
                else:
                    classes.append("f")
                    if kind == "carry":
                        classes.append("cr")
                    elif r == 0 and shape == "div":
                        classes.append("q")
                    if not show_answers:
                        txt = ""
            elif (r, c) in boxes:
                # an open box the kid fills, so the sheet never reveals how many
                # digits the answer has
                classes.append("f")
                if r == 0 and shape == "mul":
                    classes.append("cr")
            if shape == "div":
                # bracket furniture
                if r == 1 and c == 1:
                    classes.append("dv")
                if r == 1 and c >= 2:
                    classes.append("rf")
            if r in rules:
                classes.append("rl")       # horizontal rule above this row
            out.append(f'<div class="{" ".join(sorted(set(classes)))}" style="{style}">{txt}</div>')
    out.append("</div>")
    return "".join(out)


def render_sheet(name, skill_label, probs, show_answers, budget_note, shape="div"):
    cls = "sheet key" if show_answers else "sheet"
    head = "Long Division" if shape == "div" else "Multiplication"
    title = f"{head} — {skill_label}" + (" — ANSWERS" if show_answers else "")
    h = [f'<div class="{cls}">']
    h.append('<div class="head">')
    h.append(f'<h1>{html.escape(title)}</h1>')
    if show_answers:
        h.append('<div class="meta">for the grown-up</div>')
    else:
        h.append(f'<div class="meta">Name: <span>&nbsp;{html.escape(name)}</span>'
                 f'&nbsp;&nbsp;Date: <span>&nbsp;</span></div>')
    h.append("</div>")
    h.append('<p class="instr">Work each one down the boxes. '
             '<b>Every box gets a digit</b> — the steps are the answer.</p>')
    h.append('<div class="grid-wrap">')
    for i, (n, d) in enumerate(probs, 1):
        h.append(render_problem(i, n, d, show_answers, shape))
    h.append("</div>")
    h.append(f'<div class="note">{html.escape(budget_note)}</div>')
    foot = ("Divide → Multiply → Subtract → Bring down" if shape == "div"
            else "One row per digit · shift each row one column left · then add")
    h.append(f'<div class="foot">{foot}</div>')
    h.append("</div>")
    return "".join(h)


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260801)
    ap.add_argument("--budget", type=int, default=drill_cost.DEFAULT_BUDGET_SEC,
                    help="seconds per sheet (default 300 = five minutes)")
    ap.add_argument("--skill", choices=["div", "mul"], default="div",
                    help="which drill to build. One skill per kid per day — the "
                         "budget is five minutes TOTAL, not five minutes each.")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    out = args.out or f"worksheet-{'division' if args.skill == 'div' else 'multiplication'}-drill.html"
    rng = random.Random(args.seed)

    kids = kids_by_id()

    # Keyed on kid ID, never on a name — see load_kids(). Digit shapes come straight
    # from AGENTS.md "Difficulty pin".
    PLANS = {
        "div": [("kid1", (2, 1), "2-digit ÷ 1-digit, with a remainder", "div_2d_1"),
                ("kid2", (3, 1), "3-digit ÷ 1-digit, with a remainder", "div_3d_1")],
        "mul": [("kid1", (3, 1), "3-digit × 1-digit", "mul_3x1"),
                ("kid2", (2, 2), "2-digit × 2-digit", "mul_2x2")],
    }

    sheets, keys, report = [], [], []
    for kid_id, shape_digits, label, cost_key in PLANS[args.skill]:
        name = kid_name(kids, kid_id)
        skill = next(s for s in drill_cost.SKILLS if s.key == cost_key)
        count = skill.count_for(args.budget)

        if args.skill == "div":
            probs = problem_set(rng, shape_digits[0], count)
            for n, d in probs:                  # verify BEFORE anything is rendered
                _, _, marks, _, _ = trace_division(n, d)
                ok, msg = verify(n, d, marks)
                if not ok:
                    raise SystemExit(f"VERIFY FAILED {name} {n}/{d}: {msg}")
        else:
            probs = problem_set_mul(rng, shape_digits[0], shape_digits[1], count)
            for a, b in probs:
                _, _, marks, rules, _ = trace_multiplication(a, b)
                ok, msg = verify_mul(a, b, marks, rules)
                if not ok:
                    raise SystemExit(f"VERIFY FAILED {name} {a}x{b}: {msg}")

        est = count * skill.seconds()
        md = drill_cost.MATH_DRILLS_COUNT.get(cost_key)
        note = (f"{count} problems · about {est/60:.1f} min at "
                f"{skill.seconds():.0f}s each (target {args.budget/60:.0f}:00)."
                + (f" math-drills ships {md} for this skill." if md else ""))
        report.append((name, label, count, skill.seconds(), est, md))
        sheets.append(render_sheet(name, label, probs, False, note, args.skill))
        keys.append((name, label, probs, note))

    key_html = "\n".join(
        render_sheet(nm, lbl + f" — {nm}", pr, True, nt, args.skill)
        for nm, lbl, pr, nt in keys)

    # One sheet per line. This started as a workaround: print-worksheet.sh counted
    # sheets with `grep -c`, which counts matching LINES, so a one-line document
    # reported 1 sheet against 4 real pages and warned the CSS had drifted. That bug
    # is FIXED at the source now (it counts occurrences), so this is no longer load-
    # bearing — kept because a sheet per line diffs and greps far better than a 50KB
    # single line.
    title = ("Long Division" if args.skill == "div" else "Multiplication")
    # A real <head>: the sheets are served on the web as well as printed, and a
    # page with no <title> shows as a bare URL in a tab and in search results.
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
           f'<title>{title} drill — 5 minutes</title>\n'
           f"<style>{CSS}</style>\n</head>\n<body>\n"
           + "\n".join(sheets) + "\n" + key_html + "\n</body>\n</html>\n")
    with open(out, "w") as f:
        f.write(doc)

    print(f"seed {args.seed}   budget {args.budget}s   skill {args.skill}   -> {out}")
    print(f"{'kid':<8}{'skill':<34}{'n':>4}{'sec/ea':>8}{'est':>8}{'math-drills':>13}")
    print("-" * 75)
    for nm, lbl, n, per, est, md in report:
        print(f"{nm:<8}{lbl:<34}{n:>4}{per:>8.0f}{est/60:>7.1f}m{str(md):>13}")
    print(f"\nsheets: {len(sheets)} kid + {len(keys)} key = {len(sheets)+len(keys)} pages")
    print("every problem verified by independent re-derivation from its own marks")


if __name__ == "__main__":
    main()
