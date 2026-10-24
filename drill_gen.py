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


# --- single-digit FACTS ----------------------------------------------------
# Added 2026-08-03. These are a different animal from the two above and the
# difference is the whole point:
#
#   A DRILL IS SIZED TO FINISH. A PROBE IS SIZED TO OVERFLOW.
#
# Everything else in this file packs problems until a 5-minute budget runs out,
# so a kid who works steadily completes the sheet. A fluency probe must NOT be
# completable — a sheet the kid finishes measures the sheet, not the kid (see
# SPEED.md § "The measurement to actually run"). So the count here is fixed and
# deliberately larger than the benchmark rate, and `--budget` does not apply.
#
# Why facts at all, when drill_cost.py says the kids are fine: they may not be.
# SPEED.md found the "fact recall is already automatic" conclusion in
# PRACTICE-PLAN-2026.md rests on an uncited benchmark, and converting the one
# real measurement to digits-correct-per-minute puts it below the floor of every
# grade 3/4 band. This sheet is how that gets settled.

FACT_MIN = 2         # x0 and x1 are not facts worth drilling -- same rule as the
FACT_MAX = 9         # multiplier constraint in make_multiplication().

# Rocket Math Fact Fluency Benchmarks (2013), grades 4-5: all four operations at
# 35 problems/min. That is 1.7 s/fact and it is the target this sheet is scored
# against -- NOT drill_cost.py, whose marks model has never been calibrated at
# the recall end and overestimates a fact by roughly 3x. See SPEED.md.
FACT_TARGET_PER_MIN = 35
FACT_PROBE_SEC = 60
# 60 problems against a 35/min target: a kid at benchmark finishes 58% of it, and
# even 1.0 s/fact -- faster than any published benchmark -- leaves 0 spare.
FACT_PROBE_COUNT = 60


def make_fact(rng, ops):
    """One single-digit fact, in an operation drawn from `ops`.

    Multiplication: both operands 2-9, so no row is spent on x0 or x1.
    Division: the INVERSE fact, built from its answer -- divisor and quotient are
    both 2-9, so the dividend is 4-81 and it always divides exactly. A remainder
    here would make it long division, which is a different skill and is already
    drilled by --skill div.
    """
    op = rng.choice(ops)
    a = rng.randint(FACT_MIN, FACT_MAX)
    b = rng.randint(FACT_MIN, FACT_MAX)
    if op == "mul":
        return ("mul", a, b)
    return ("div", a * b, b)          # a*b / b == a, exact by construction


def fact_space(ops):
    """How many DISTINCT facts exist for these operations. 8 values (2-9) each way.

    This is a hard ceiling, not a tuning knob, and it is small enough to matter:
    multiplication alone is 64. A 60-problem sheet is 94% of that space, so two
    different seeds give kid1 nearly the same problems in a different ORDER --
    measured 93-95% overlap on 2026-08-03.

    For a fact PROBE that is fine and arguably correct: you want the same
    instrument each time so the score is comparable week to week. But it is not
    what DRILLS.md's "unbounded -- it's a seed" claims about the multi-digit
    generators, and the difference should not be a surprise. Mixing in division
    (kid2) doubles the space to 128 and drops the overlap to ~45%.
    """
    per_op = (FACT_MAX - FACT_MIN + 1) ** 2
    return per_op * len(set(ops))


def problem_set_facts(rng, ops, count):
    """`count` distinct facts. Commuted pairs (7x8 and 8x7) count as DISTINCT.

    That is deliberate: recall is directional in practice -- a kid can be quick on
    7x8 and slow on 8x7 -- and collapsing them would also make a 60-problem sheet
    of 2-9 facts impossible to fill without repeats (there are only 36 unordered
    multiplication pairs).
    """
    space = fact_space(ops)
    if count > space:
        # Fail on the arithmetic, not by exhausting a loop. The old behaviour drew
        # count*200 random facts and then raised "could not build", which reads as
        # a transient failure when it is a hard ceiling that no seed can clear.
        raise SystemExit(
            f"--count {count} is impossible for {'+'.join(sorted(set(ops)))}: only "
            f"{space} distinct facts exist with operands {FACT_MIN}-{FACT_MAX}"
            + ("" if "div" in ops else
               " (add division to the plan to double the space to "
               f"{space * 2})"))
    seen, out = set(), []
    guard = 0
    while len(out) < count:
        guard += 1
        if guard > count * 200:
            raise RuntimeError(f"could not build {count} distinct facts from {ops}")
        p = make_fact(rng, ops)
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
    return out


def trace_fact(op, x, y):
    """Same (rows, cols, marks, rules, boxes) contract as the two tracers above,
    so render_problem() and verify_drills.py need no special geometry.

    One row: [x] [op] [y] [=] [box] [box]. Two answer cells on multiplication
    because a product of 2-9 facts is 4-81 -- one or two digits -- and a
    single-cell answer would tell the kid which. Division quotients are always
    one digit, so they get one cell.
    """
    sym = "×" if op == "mul" else "÷"
    ans = x * y if op == "mul" else x // y
    width = 2 if op == "mul" else 1

    marks = [(0, 0, str(x), "given"), (0, 1, sym, "given"),
             (0, 2, str(y), "given"), (0, 3, "=", "given")]

    # right-align the answer in its cells; the unused leading cell stays an empty
    # open box so a 1-digit product is not advertised as such.
    txt = str(ans).rjust(width)
    for i, ch in enumerate(txt):
        if ch != " ":
            marks.append((0, 4 + i, ch, "ans"))

    boxes = {(0, 4 + i) for i in range(width)}
    return 1, 4 + width, marks, set(), boxes


# --- TRAILING-ZERO products and quotients ---------------------------------
# Added 2026-10-24 for kid1's Noetic prep (a graded practice test missed
# "multiply/divide when there is a zero at the end"). Asif: "he should be able to do
# that really easily" -- so this is a fluency PROBE, not a method drill:
#
#   * Same shape as --skill facts: a fixed count sized to OVERFLOW the window, a
#     "Stopped at #" field, the score is how far the kid GOT and how many were right.
#   * There is no written method to force (the whole skill is "do the fact, then
#     move the zeros"), so there is no grid/plain split -- an answer box, like facts.
#   * One equation per problem: a OP b = c, with exactly one of the three numbers
#     missing. Stages 1-2 hide c. Stage 3 hides a or b (missing-factor forms).
#
# STAGES (one per school day; see private/PRACTICE-PLAN-2026.md "Musa focus track"):
#   1  ONE zero:  40 x 6 = 240   120 / 3 = 40   800 / 4 = 200   300 x 2 = 600
#   2  TWO zeros: 30 x 20 = 600  600 / 30 = 20  300 x 4 = 1200  2400 / 6 = 400
#   3  MISSING:   ? x 3 = 120    240 / ? = 60   ? / 4 = 80      (pool of stages 1-2)
#   mix           all three, for review
#
# Every operand is a single digit 2-9 or a multiple of 10 -- the same "no x0 / x1
# row" rule as make_multiplication(): x1 and x0 teach nothing here.

ZERO_STAGES = {
    # stage: (problems on sheet, answer-box width, seconds each at target)
    "1": (48, 3, 3),
    "2": (40, 4, 4),
    "3": (40, 4, 4),
    "mix": (40, 4, 4),
}
ZERO_PROBE_SEC = 120          # a 2-minute probe, like the CBM computation probe in SPEED.md
# Kept short: the sheet header is one flex row (title, Name, Date, Stopped at #).
ZERO_LABEL = {"1": "one zero", "2": "two zeros", "3": "missing number", "mix": "review"}


def _z_forms(stage):
    """[(weight, fn)] where fn(rng) -> (op, a, b, c): an equation a OP b = c."""
    D = range(2, 10)

    def f1a(r):                       # 40 x 6 = 240   (or 6 x 40)
        x, b = r.choice(D), r.choice(D)
        a = 10 * x
        return ("mul", *((a, b) if r.random() < .5 else (b, a)), a * b)

    def f1b(r):                       # 120 / 3 = 40
        x, b = r.choice(D), r.choice(D)
        return ("div", 10 * x * b, b, 10 * x)

    def f1c(r):                       # 800 / 4 = 200
        b = r.choice([2, 3, 4])
        q = r.choice(range(2, 9 // b + 1))
        return ("div", b * q * 100, b, q * 100)

    def f1d(r):                       # 300 x 2 = 600   (product stays under 1000)
        x, b = r.choice([(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (4, 2)])
        a = 100 * x
        return ("mul", *((a, b) if r.random() < .5 else (b, a)), a * b)

    def f2a(r):                       # 30 x 20 = 600  (zeros on BOTH factors)
        x, y = r.choice(D), r.choice(D)
        return ("mul", 10 * x, 10 * y, 100 * x * y)

    def f2b(r):                       # 300 x 4 = 1200
        while True:
            x, b = r.choice(D), r.choice(D)
            if x * b >= 10:
                a = 100 * x
                return ("mul", *((a, b) if r.random() < .5 else (b, a)), a * b)

    def f2c(r):                       # 600 / 30 = 20
        x, y = r.choice(D), r.choice(D)
        return ("div", 100 * x * y, 10 * y, 10 * x)

    def f2d(r):                       # 2400 / 6 = 400
        while True:
            x, b = r.choice(D), r.choice(D)
            if x * b >= 10:
                return ("div", 100 * x * b, b, 100 * x)

    s1 = [(.40, f1a), (.35, f1b), (.12, f1c), (.13, f1d)]
    s2 = [(.30, f2a), (.25, f2b), (.30, f2c), (.15, f2d)]
    return {"1": s1, "2": s2, "3": s1 + s2, "mix": s1 + s2}[stage]


def make_zero(rng, stage):
    """One trailing-zero equation: (op, a, b, c, hole), exactly one number hidden.

    Stage 3 hides a or b, never c: the missing-factor form is the new act. `mix`
    hides c two times in three and a/b one time in three.
    """
    forms = _z_forms(stage)
    fn = rng.choices([f for _, f in forms], weights=[w for w, _ in forms])[0]
    op, a, b, c = fn(rng)
    if stage == "3" or (stage == "mix" and rng.random() < 1 / 3):
        hole = rng.choice(["a", "b"])
    else:
        hole = "c"
    return (op, a, b, c, hole)


def problem_set_zeros(rng, stage, count):
    """`count` distinct equations. Commuted pairs (40 x 6, 6 x 40) are distinct."""
    seen, out, guard = set(), [], 0
    while len(out) < count:
        guard += 1
        if guard > count * 400:
            raise RuntimeError(f"could not build {count} distinct zeros problems "
                               f"for stage {stage}")
        p = make_zero(rng, stage)
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
    return out


def trace_zeros(op, a, b, c, hole, width):
    """One row: a OP b = c, the hidden number as `width` open boxes.

    Same (rows, cols, marks, rules, boxes) contract as the other tracers. The hidden
    number is right-aligned in a FIXED number of boxes, so the box count never tells
    the kid how many digits the answer has (same reason trace_fact uses 2 cells).
    """
    sym = "×" if op == "mul" else "÷"
    marks, boxes, col = [], set(), 0

    def number(val, hidden):
        nonlocal col
        if hidden:
            txt = str(val).rjust(width)
            for i, ch in enumerate(txt):
                if ch != " ":
                    marks.append((0, col + i, ch, "ans"))
                boxes.add((0, col + i))
            col += width
        else:
            for ch in str(val):
                marks.append((0, col, ch, "given"))
                col += 1

    def symbol(t):
        nonlocal col
        marks.append((0, col, t, "given"))
        col += 1

    number(a, hole == "a")
    symbol(sym)
    number(b, hole == "b")
    symbol("=")
    number(c, hole == "c")
    return 1, col, marks, set(), boxes


def verify_zeros(op, a, b, c, hole, marks):
    """Rebuild the equation from the MARKS (not from a/b/c) and check it."""
    toks, cur = [], []
    for (_r, _c, t, kind) in sorted(marks, key=lambda m: m[1]):
        if t in ("×", "÷", "="):
            toks.append(cur)
            toks.append(t)
            cur = []
        else:
            cur.append(t)
    toks.append(cur)
    if len(toks) != 5:
        return False, f"{len(toks)} tokens, want 5"
    na, sym, nb, eq, nc = ("".join(x) if isinstance(x, list) else x for x in toks)
    if not (na and nb and nc):
        return False, "an operand is empty"
    na, nb, nc = int(na), int(nb), int(nc)
    ok = (na * nb == nc) if sym == "×" else (nb != 0 and na == nb * nc)
    if not ok:
        return False, f"{na} {sym} {nb} != {nc}"
    for n in (na, nb, nc):
        if not (n % 10 == 0 or 2 <= n <= 9):
            return False, f"{n} is neither a multiple of 10 nor a digit 2-9"
    return True, f"{na} {sym} {nb} = {nc}"


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
        marks.append((row, C(i) - len(p), "−", "prompt"))  # scaffolding, not the problem
        for j, ch in enumerate(p):
            marks.append((row, C(i) - len(p) + 1 + j, ch, "fill"))
        row += 1

        r = str(st["rem"])                                      # difference, right-aligned at col i
        for j, ch in enumerate(r):
            marks.append((row, C(i) - len(r) + 1 + j, ch, "fill"))
        if last:
            marks.append((row, C(i) - 1, "R", "prompt"))
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
/* zeros probe: 40-48 one-row equations, two per row -- tighter than the grid sheets */
.grid-wrap.z { gap: 7px 30px; }
.z .prob { margin-bottom: 0; }
"""


def render_problem(idx, x, y, show_answers, shape="div", layout="grid", op=None):
    if shape == "div":
        rows, cols, marks, rules, boxes = trace_division(x, y)
    elif shape == "facts":
        rows, cols, marks, rules, boxes = trace_fact(op, x, y)
    elif shape == "zeros":
        rows, cols, marks, rules, boxes = trace_zeros(*x)    # x = (op,a,b,c,hole,width)
    else:
        rows, cols, marks, rules, boxes = trace_multiplication(x, y)

    # "plain" drops the boxes from the KID's sheet only — same geometry, so the
    # work space is unchanged, but nothing tells them how many digits go where.
    # A test will not hand them a grid; once the method is solid, take it away.
    #
    # Facts opt out: there is no written method to force or withhold, and the
    # answer box is the only place to write. `--layout plain` on a fact sheet
    # would produce a row of naked equals signs.
    boxed = (layout == "grid") or show_answers or shape in ("facts", "zeros")

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
                if kind in ("given", "prompt"):
                    # On a PLAIN sheet the minus signs and the R are removed, not just
                    # unboxed. Leaving them in tells the kid how many subtraction steps
                    # there are — i.e. how many digits the quotient has — which is most
                    # of what the exercise is asking them to work out.
                    if kind == "prompt" and not boxed:
                        txt = ""
                    classes.append("g")
                else:
                    if boxed:
                        classes.append("f")
                        if kind == "carry":
                            classes.append("cr")
                        elif r == 0 and shape == "div":
                            classes.append("q")
                    elif show_answers:
                        classes.append("f")
                        if kind == "carry":
                            classes.append("cr")
                        elif r == 0 and shape == "div":
                            classes.append("q")
                    if not show_answers:
                        txt = ""
            elif (r, c) in boxes and boxed:
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


def render_sheet(name, skill_label, probs, show_answers, budget_note, shape="div", layout="grid"):
    cls = "sheet key" if show_answers else "sheet"
    # Kept short for facts: the header is one flex row with a Name, a Date AND a
    # "Stopped at #" field, and a long title wraps it onto two lines.
    head = {"div": "Long Division", "mul": "Multiplication", "facts": "Facts",
            "zeros": "Zeros"}[shape]
    title = f"{head} — {skill_label}" + (" — ANSWERS" if show_answers else "")
    h = [f'<div class="{cls}">']
    h.append('<div class="head">')
    h.append(f'<h1>{html.escape(title)}</h1>')
    if show_answers:
        h.append('<div class="meta">for the grown-up</div>')
    else:
        meta = (f'Name: <span>&nbsp;{html.escape(name)}</span>'
                f'&nbsp;&nbsp;Date: <span>&nbsp;</span>')
        if shape in ("facts", "zeros"):
            # A probe is scored on how far they GOT, so the sheet has to carry the
            # stop point. Without it the number is unrecoverable an hour later.
            meta += '&nbsp;&nbsp;Stopped at #: <span>&nbsp;</span>'
        h.append(f'<div class="meta">{meta}</div>')
    h.append("</div>")
    if shape == "zeros":
        instr = ('<b>Two minutes. Work in order, left to right.</b> Write only the answer '
                 'in the boxes. Skip any you can\'t do fast; come back only if time is left.')
    elif shape == "facts":
        # "in order, left to right" and not "down the columns": the layout is
        # row-major and so is the numbering, and the score is HOW FAR THEY GOT —
        # which is only meaningful if they went in the printed order.
        instr = ('<b>One minute. Work in order, left to right.</b> Skip any you don\'t '
                 'know instantly — come back only if there is time left.')
    elif layout == "grid":
        instr = ('Work each one down the boxes. <b>Every box gets a digit</b> — the steps '
                 'are the answer.')
    else:
        instr = '<b>Show every step.</b> No boxes this time — line the columns up yourself.'
    h.append(f'<p class="instr">{instr}</p>')
    h.append('<div class="grid-wrap z">' if shape == "zeros" else '<div class="grid-wrap">')
    for i, p in enumerate(probs, 1):
        if shape == "zeros":
            h.append(render_problem(i, p, None, show_answers, shape, layout))
        elif shape == "facts":
            op, n, d = p
            h.append(render_problem(i, n, d, show_answers, shape, layout, op=op))
        else:
            n, d = p
            h.append(render_problem(i, n, d, show_answers, shape, layout))
    h.append("</div>")
    h.append(f'<div class="note">{html.escape(budget_note)}</div>')
    foot = {"div": "Divide → Multiply → Subtract → Bring down",
            "mul": "One row per digit · shift each row one column left · then add",
            "facts": ("Not meant to be finished — how far you get IS the measurement · "
                      f"target {FACT_TARGET_PER_MIN}/min"),
            "zeros": ("Not meant to be finished — how far you get IS the measurement · "
                      "do the fact, then move the zeros")}[shape]
    h.append(f'<div class="foot">{foot}</div>')
    h.append("</div>")
    return "".join(h)


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260801)
    ap.add_argument("--budget", type=int, default=drill_cost.DEFAULT_BUDGET_SEC,
                    help="seconds per sheet (default 300 = five minutes)")
    ap.add_argument("--skill", choices=["div", "mul", "facts", "zeros"], default="div",
                    help="which drill to build. One skill per kid per day — the "
                         "budget is five minutes TOTAL, not five minutes each. "
                         "'facts' is a 1-minute single-digit PROBE, not a drill: "
                         "fixed count, sized to overflow, --budget ignored. "
                         "'zeros' is the same kind of probe (2 minutes) for products and "
                         "quotients with trailing zeros; kid1 only; pick --stage.")
    ap.add_argument("--stage", choices=list(ZERO_STAGES), default="1",
                    help="zeros only: 1 = one zero (40 x 6, 120 / 3), 2 = two zeros "
                         "(30 x 20, 600 / 30), 3 = missing number (? x 3 = 120), "
                         "mix = all of them.")
    ap.add_argument("--count", type=int, default=None,
                    help="facts only: how many problems (default "
                         f"{FACT_PROBE_COUNT}). Must exceed what the kid can "
                         "finish in a minute or it stops being a measurement.")
    ap.add_argument("--layout", choices=["grid", "plain"], default="grid",
                    help="grid = every step gets a printed box (forces the work); "
                         "plain = the problem and blank space, the way a test gives it. "
                         "Start on grid, move to plain once the method is solid.")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    suffix = "" if args.layout == "grid" else "-plain"
    base = {"div": "division", "mul": "multiplication", "facts": "facts",
            "zeros": "zeros"}[args.skill]
    # A facts/zeros sheet has no layout variants, so it never takes the -plain suffix.
    out = args.out or (f"worksheet-{base}-drill"
                       f"{'' if args.skill in ('facts', 'zeros') else suffix}.html")
    rng = random.Random(args.seed)

    kids = kids_by_id()

    # Keyed on kid ID, never on a name — see load_kids(). Digit shapes come straight
    # from AGENTS.md "Difficulty pin".
    PLANS = {
        # Stepped up one notch 2026-08-20 on Asif's direct instruction ("make the
        # drills slightly harder"). One extra digit each — same method, one more
        # step — NOT a new act (Yusuf's flagged 2-digit-divisor rung is deliberately
        # skipped: that is a genuinely new skill, not "slightly"). Not evidence-gated
        # off RESULTS.md; this is the owner overriding the pin.
        "div": [("kid1", (3, 1), "3-digit ÷ 1-digit, with a remainder", "div_3d_1"),
                ("kid2", (4, 1), "4-digit ÷ 1-digit, with a remainder", "div_4d_1")],
        "mul": [("kid1", (4, 1), "4-digit × 1-digit", "mul_4x1"),
                ("kid2", (3, 2), "3-digit × 2-digit", "mul_3x2")],
        # Facts: the shape field carries the OPERATIONS, not digit counts, and
        # there is no drill_cost key because a probe is not sized to a budget.
        # kid1 gets multiplication only; kid2 gets both, because operation-
        # switching is itself part of what the grade 4-5 benchmark measures.
        # Labels stay short — the header is one flex row and "Facts — <label>"
        # plus three fields wraps if the label runs long.
        "facts": [("kid1", ("mul",), "×, 2–9", None),
                  ("kid2", ("mul", "div"), "× and ÷, 2–9", None)],
        # Zeros: kid1 ONLY (Noetic prep, 2026-10-24). kid2 is deliberately absent --
        # his plan is untouched. The label carries the stage.
        "zeros": [("kid1", None, ZERO_LABEL[args.stage], None)],
    }

    if args.count is not None and args.skill not in ("facts", "zeros"):
        raise SystemExit("--count applies to --skill facts/zeros only; the other skills "
                         "derive their count from --budget via drill_cost.py")

    sheets, keys, report = [], [], []
    for kid_id, shape_digits, label, cost_key in PLANS[args.skill]:
        name = kid_name(kids, kid_id)

        if args.skill == "zeros":
            n_default, width, sec_each = ZERO_STAGES[args.stage]
            count = args.count or n_default
            target = ZERO_PROBE_SEC // sec_each
            probs = [p + (width,) for p in problem_set_zeros(rng, args.stage, count)]
            for p in probs:                  # verify BEFORE anything is rendered
                _, _, marks, _, _ = trace_zeros(*p)
                ok, msg = verify_zeros(*p[:5], marks)
                if not ok:
                    raise SystemExit(f"VERIFY FAILED {name} {p[:5]}: {msg}")
            # Why 3 s: the grade 3 facts bar is 30/min (2 s, speed_check.py FACTS_PPM) plus
            # about a second to move the zeros. drill_cost's mark model would say
            # SEC_PER_MARK*3 + SEC_SETUP = 11 s for a 3-digit answer; SPEED.md shows that
            # model runs about 3x high for recall, so it is NOT used for this probe.
            note = (f"{count} problems, {ZERO_PROBE_SEC // 60} minutes. Target {target} "
                    f"correct ({sec_each}s each). Pass = target met with at most 2 wrong, "
                    f"twice in a row. Score: speed_check.py --facts --problems <correct> "
                    f"--minutes 2 --grade 3")
            report.append((name, label, count, float(sec_each), ZERO_PROBE_SEC, None))
            sheets.append(render_sheet(name, label, probs, False, note, "zeros", args.layout))
            keys.append((name, label, probs, note))
            continue

        if args.skill == "facts":
            count = args.count or FACT_PROBE_COUNT
            probs = problem_set_facts(rng, list(shape_digits), count)
            for op, x, y in probs:          # verify BEFORE anything is rendered
                if op == "mul":
                    ok = FACT_MIN <= x <= FACT_MAX and FACT_MIN <= y <= FACT_MAX
                    why = f"{x}×{y} outside {FACT_MIN}-{FACT_MAX}"
                else:
                    ok = (FACT_MIN <= y <= FACT_MAX and x % y == 0
                          and FACT_MIN <= x // y <= FACT_MAX)
                    why = f"{x}÷{y} not an exact 2-9 fact"
                if not ok:
                    raise SystemExit(f"VERIFY FAILED {name}: {why}")

            per = 60.0 / FACT_TARGET_PER_MIN
            note = (f"{count} problems in {FACT_PROBE_SEC}s. Target "
                    f"{FACT_TARGET_PER_MIN}/min ({per:.1f}s each) — Rocket Math "
                    f"grade 4–5. NOT meant to be finished: score how far they got, "
                    f"then `python3 speed_check.py --facts --problems N --minutes 1`.")
            space = fact_space(shape_digits)
            if count / space > 0.8:
                # Not an error — for a probe, a near-complete table is defensible.
                # But it must not be discovered later: at this ratio the seed only
                # reshuffles, it does not resample.
                print(f"note: {name}'s {count} problems are {count/space:.0%} of the "
                      f"{space} facts that exist for {'+'.join(sorted(set(shape_digits)))}"
                      f" — different seeds change the ORDER, not the problems")
            report.append((name, label, count, per, FACT_PROBE_SEC, None))
            sheets.append(render_sheet(name, label, probs, False, note, "facts", args.layout))
            keys.append((name, label, probs, note))
            continue

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
        sheets.append(render_sheet(name, label, probs, False, note, args.skill, args.layout))
        keys.append((name, label, probs, note))

    key_html = "\n".join(
        render_sheet(nm, lbl + f" — {nm}", pr, True, nt, args.skill, args.layout)
        for nm, lbl, pr, nt in keys)

    # One sheet per line. This started as a workaround: print-worksheet.sh counted
    # sheets with `grep -c`, which counts matching LINES, so a one-line document
    # reported 1 sheet against 4 real pages and warned the CSS had drifted. That bug
    # is FIXED at the source now (it counts occurrences), so this is no longer load-
    # bearing — kept because a sheet per line diffs and greps far better than a 50KB
    # single line.
    title = {"div": "Long Division", "mul": "Multiplication",
             "facts": "Fact fluency probe", "zeros": "Zeros probe"}[args.skill]
    # A real <head>: the sheets are served on the web as well as printed, and a
    # page with no <title> shows as a bare URL in a tab and in search results.
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
           f'<title>{title} — '
           f'{ {"facts": "1 minute", "zeros": "2 minutes"}.get(args.skill, "5 minutes") }</title>\n'
           f"<style>{CSS}</style>\n</head>\n<body>\n"
           + "\n".join(sheets) + "\n" + key_html + "\n</body>\n</html>\n")
    with open(out, "w") as f:
        f.write(doc)

    if args.skill == "zeros":
        print(f"seed {args.seed}   skill zeros   stage {args.stage}   probe "
              f"{ZERO_PROBE_SEC}s   (--budget and --layout do not apply)   -> {out}")
    elif args.skill == "facts":
        print(f"seed {args.seed}   skill facts   probe {FACT_PROBE_SEC}s   "
              f"(--budget and --layout do not apply)   -> {out}")
    else:
        print(f"seed {args.seed}   budget {args.budget}s   skill {args.skill}   "
              f"layout {args.layout}   -> {out}")
    print(f"{'kid':<8}{'skill':<34}{'n':>4}{'sec/ea':>8}{'est':>8}{'math-drills':>13}")
    print("-" * 75)
    for nm, lbl, n, per, est, md in report:
        print(f"{nm:<8}{lbl:<34}{n:>4}{per:>8.1f}{est/60:>7.1f}m"
              f"{(str(md) if md else 'n/a'):>13}")
    print(f"\nsheets: {len(sheets)} kid + {len(keys)} key = {len(sheets)+len(keys)} pages")
    if args.skill == "zeros":
        print("every equation rebuilt from its own marks and checked; every operand "
              "is a digit 2-9 or a multiple of 10")
        print("'est' is the PROBE WINDOW, not a prediction; 'sec/ea' is the TARGET")
    elif args.skill == "facts":
        print(f"every fact checked in range {FACT_MIN}-{FACT_MAX}; every division "
              f"fact checked exact")
        print(f"'est' is the PROBE WINDOW, not a prediction — the sheet is sized to "
              f"overflow it")
    else:
        print("every problem verified by independent re-derivation from its own marks")


if __name__ == "__main__":
    main()
