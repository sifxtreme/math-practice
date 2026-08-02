"""drill_cost.py — how many problems fit in a five-minute drill.

WHY THIS EXISTS
---------------
Asif, 2026-08-01: "the goal is for the kids to do this in 5 minutes ... 2 digits vs
3 digit vs 1 digit makes it different right?"

Yes, and by a lot more than math-drills.com assumes. Their sheets are sized to fill a
page, not to fit a clock: 25 problems of 2-digit x 1-digit and 20 of 2-digit x 2-digit,
when the second is roughly four times the work of the first. A count that isn't derived
from a time budget is a guess.

So a sheet here is built to a TIME budget, not a problem count. You say "five minutes",
the generator packs problems until the estimated seconds run out, and the count falls
out of the arithmetic. Change the skill and the count changes by itself.

THE MODEL
---------
Time per problem is driven by the number of elementary WRITTEN MARKS the standard
algorithm requires -- not by how "hard" the skill feels. A mark is one digit committed
to paper: a product digit, a carry, a difference digit, a brought-down digit.

    seconds = SEC_PER_MARK * marks + SEC_SETUP

CALIBRATION (the one real measurement we have)
----------------------------------------------
PRACTICE-PLAN-2026.md, "Why this plan isn't fact drills" -- May 2026, both kids:
**49 problems of 3-digit minus 3-digit subtraction with regrouping in 13 minutes**
= 15.9 s/problem. That single point sets SEC_PER_MARK; everything else is the mark
count, which is derived, not guessed.

    3-digit - 3-digit w/ regrouping ~ 3 difference digits + ~1.5 regroup marks = 4.5
    15.9 s = SEC_PER_MARK * 4.5 + SEC_SETUP

CONFIDENCE, STATED PLAINLY
--------------------------
One data point, one skill, three months old. The MARK COUNTS are exact -- they come from
the algorithms. The SECONDS PER MARK is an extrapolation from subtraction to division and
multiplication, and it is the number most likely to be wrong. Treat every count below as
a STARTING POINT to be corrected by `calibrate()` once real sheets get timed. That is why
observed times are a first-class input here and not a comment.

Run `python3 drill_cost.py` for the table and the self-check.
"""

from dataclasses import dataclass

# --- calibration constants -------------------------------------------------
# Split between per-mark cost and a fixed per-problem cost (read the problem,
# orient on the page, write the answer down). SEC_SETUP is small on purpose:
# with the anchor being a 4.5-mark problem, a large setup term would leave the
# per-mark cost too small to separate a 2x1 from a 2x2 multiply.
SEC_PER_MARK = 3.1
SEC_SETUP = 2.0

ANCHOR = {
    "label": "3-digit - 3-digit subtraction w/ regrouping",
    "marks": 4.5,
    "observed_sec": 15.9,   # 49 problems / 13 min, both kids, May 2026
    "source": "PRACTICE-PLAN-2026.md 'Why this plan isn't fact drills'",
}

DEFAULT_BUDGET_SEC = 300     # five minutes


# --- mark counts, derived from the written algorithms ----------------------

def marks_multiplication(a_digits: int, b_digits: int) -> float:
    """Standard algorithm: a partial product per multiplier digit, then add them.

    Per multiplier digit you write a_digits product digits plus roughly a_digits-1
    carries. With more than one multiplier digit you also write the placeholder
    zero(s) and then add the partial rows -- an addition about (a_digits+b_digits)
    columns wide, with carries.
    """
    per_row = a_digits + max(0, a_digits - 1) * 0.7     # product digits + carries
    rows = b_digits
    total = per_row * rows
    if b_digits > 1:
        total += (b_digits - 1) * 0.5                   # placeholder zeros
        total += (a_digits + b_digits) * 0.8            # final addition + carries
    return total


def marks_long_division(dividend_digits: int, divisor_digits: int = 1) -> float:
    """D-M-S-B, once per quotient digit.

    Each cycle writes: the quotient digit, the product under the current chunk
    (about divisor_digits+1 digits), the difference, and the brought-down digit.
    A 1-digit divisor is a recall; a 2-digit divisor adds an ESTIMATE step, which
    is the expensive part and the reason DRILLS.md wants a TEACH sheet first.
    """
    q_digits = max(1, dividend_digits - divisor_digits + 1)
    per_cycle = 1 + (divisor_digits + 1) + 1 + 1        # q, product, difference, bring-down
    if divisor_digits > 1:
        per_cycle += 1.5                                 # estimate / adjust
    return q_digits * per_cycle


def marks_subtraction(digits: int) -> float:
    return digits + (digits - 1) * 0.75                  # differences + regroups


@dataclass
class Skill:
    key: str
    label: str
    kid: str
    marks: float

    def seconds(self) -> float:
        return SEC_PER_MARK * self.marks + SEC_SETUP

    def count_for(self, budget_sec: int = DEFAULT_BUDGET_SEC) -> int:
        return max(1, int(budget_sec / self.seconds()))


# The skills actually on the pin (AGENTS.md "Difficulty pin"), plus the anchor.
# The `kid` field is an ID, never a name — see README.md "Setting it up for your
# kids". A "+" suffix means the next rung up for that child, not yet on the pin.
SKILLS = [
    Skill("sub_3x3", "3-digit - 3-digit, regrouping (ANCHOR)", "both", marks_subtraction(3)),
    Skill("mul_2x1", "2-digit x 1-digit", "kid1", marks_multiplication(2, 1)),
    Skill("mul_3x1", "3-digit x 1-digit", "kid1", marks_multiplication(3, 1)),
    Skill("mul_4x1", "4-digit x 1-digit", "kid1+", marks_multiplication(4, 1)),
    Skill("mul_2x2", "2-digit x 2-digit", "kid2", marks_multiplication(2, 2)),
    Skill("mul_3x2", "3-digit x 2-digit", "kid2+", marks_multiplication(3, 2)),
    Skill("div_2d_1", "2-digit / 1-digit, remainder", "kid1", marks_long_division(2, 1)),
    Skill("div_3d_1", "3-digit / 1-digit, remainder", "kid2", marks_long_division(3, 1)),
    Skill("div_4d_1", "4-digit / 1-digit, remainder", "kid2", marks_long_division(4, 1)),
    Skill("div_3d_2", "3-digit / 2-digit, remainder", "kid2+", marks_long_division(3, 2)),
]

# What math-drills.com actually ships, counted off the rendered PDFs 2026-08-01.
MATH_DRILLS_COUNT = {
    "mul_2x1": 25, "mul_2x2": 20,
    "div_2d_1": 25, "div_3d_1": 20, "div_4d_1": 12,
}


def calibrate(observed_sec: float, marks: float) -> float:
    """Re-derive SEC_PER_MARK from a timed sheet. Feed it a real observation.

    Time a kid on a real sheet, pass the seconds-per-problem and that skill's mark
    count, and this returns the SEC_PER_MARK the observation implies. If it drifts
    far from the constant above, change the constant -- do not adjust the counts by
    hand, or the model stops meaning anything.
    """
    return (observed_sec - SEC_SETUP) / marks


def _self_check() -> bool:
    """The model must reproduce the one measurement we actually have."""
    predicted = SEC_PER_MARK * ANCHOR["marks"] + SEC_SETUP
    err = abs(predicted - ANCHOR["observed_sec"])
    ok = err < 0.5
    print(f"self-check: anchor = {ANCHOR['label']}")
    print(f"  observed {ANCHOR['observed_sec']:.1f}s   predicted {predicted:.1f}s   "
          f"error {err:.2f}s   {'PASS' if ok else 'FAIL'}")
    print(f"  source: {ANCHOR['source']}")
    return ok


def main() -> int:
    print(__doc__.strip().split("\n")[0])
    print()
    ok = _self_check()
    print()
    hdr = f"{'skill':<38}{'kid':<8}{'marks':>6}{'sec':>7}{'5-min':>7}{'M-D':>6}{'verdict':>22}"
    print(hdr)
    print("-" * len(hdr))
    for s in SKILLS:
        n = s.count_for()
        md = MATH_DRILLS_COUNT.get(s.key)
        if md is None:
            verdict = ""
        else:
            ratio = md / n
            mins = md * s.seconds() / 60
            verdict = f"{ratio:.1f}x over -> {mins:.0f} min"
        md_s = str(md) if md else "-"
        print(f"{s.label:<38}{s.kid:<8}{s.marks:>6.1f}{s.seconds():>7.1f}{n:>7}{md_s:>6}{verdict:>22}")
    print()
    print("'5-min' = problems that fit 300s. 'M-D' = what math-drills.com ships.")
    print("Counts are a starting point: time a real sheet, then call calibrate().")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
