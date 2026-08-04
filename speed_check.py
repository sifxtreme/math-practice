"""speed_check.py — put a timed sheet against the published fluency norms.

WHY THIS EXISTS
---------------
Asif, 2026-08-03: *"I'm really concerned about speed for the kids drills ... we
really need to figure this out. Does khan academy or Kumon give insights on speed."*

Short answer: **Kumon yes, Khan Academy no, and neither is the one you want.**
The field standard is CURRICULUM-BASED MEASUREMENT, scored in DIGITS CORRECT PER
MINUTE (DCPM), and it has published grade norms. See SPEED.md for who says what.

This module converts a timed sheet into DCPM and places it in those norms, because
until 2026-08-03 this repo was measuring in SECONDS PER PROBLEM -- a unit no
published benchmark uses -- and comparing it to a 15-20 s "fluency benchmark" that
PRACTICE-PLAN-2026.md asserts without a citation and that I could not source.

    python3 speed_check.py --problems 49 --minutes 13 --digits 3 --grade 3
    python3 speed_check.py --facts --problems 42 --minutes 1 --grade 4

WHY DIGITS AND NOT PROBLEMS
---------------------------
CBM scores the digits in the ANSWER, not the problems. That is deliberate: it gives
partial credit for a long algorithm and makes a 3-digit subtraction comparable to a
single-digit fact. A kid who gets 2 of 3 digits right on every problem is doing real
work that a problems-correct score throws away entirely.

WHAT COUNTS AS A DIGIT
----------------------
Answer digits only, under standard CBM-Math scoring. For long division, the quotient
digits AND the remainder count. Work shown above the line does not. When in doubt use
the LOWER digit count -- it makes the result more conservative, not less.
"""

import argparse

# --- published norms, quoted, not derived ----------------------------------

# CBM-Math Computation Fluency Norms: Correct Digits Per Minute.
# Source: VanDerHeyden, A. M., & Burns, M. K. (2009). Performance indicators in
# math: Implications for brief experimental analysis of academic performance.
# Journal of Behavioral Education, 18, 71-91. Table as reproduced by Jim Wright,
# interventioncentral.org. Probes are 2-minute, group-administered, standardized.
#
# 'intervention' = probes at the student's CURRENT INSTRUCTIONAL LEVEL (new material).
# 'retention'    = probes on material the student has PREVIOUSLY MASTERED.
# Ranges are +/- 1 SD around the median -- the "typical" band, not a pass mark.
CBM_DCPM = {
    #        intervention          retention
    #        median  low  high     median  low  high
    2:      {"interv": (15,  9, 21), "reten": (23, 11, 35)},
    3:      {"interv": (37, 22, 52), "reten": (17, 11, 23)},
    4:      {"interv": (45, 28, 62), "reten": (30, 20, 40)},
    5:      {"interv": (26, 15, 37), "reten": (36, 25, 47)},
}

# Single-digit FACT fluency, in problems per minute.
# Source: Rocket Math Fact Fluency Benchmarks (R&D Instructional Solutions, 2013).
# These are facts only -- 7 x 8, not 47 x 36 -- and they are the input to every
# multi-digit algorithm. If facts are slow, long division cannot be fast.
FACTS_PPM = {
    3: {"start": ("addition", 30), "mid": ("subtraction", 30), "end": ("multiplication", 30)},
    4: {"start": ("add/sub/mult", 35), "mid": ("division", 20), "end": ("all four", 35)},
    5: {"start": ("all four", 35), "mid": ("all four", 35), "end": ("all four", 35)},
}

# The one measurement this repo actually has, for reference.
ANCHOR = {"problems": 49, "minutes": 13, "digits": 3.0,
          "label": "3-digit - 3-digit subtraction w/ regrouping, both kids, May 2026",
          "source": "PRACTICE-PLAN-2026.md 'Why this plan isn't fact drills'"}


def dcpm(problems: int, minutes: float, digits_per_problem: float) -> float:
    """Digits correct per minute. Assumes every answer was correct."""
    return problems * digits_per_problem / minutes


def place(value: float, band: tuple) -> str:
    """Where a score falls against a (median, low, high) norm band."""
    median, low, high = band
    if value >= high:
        return f"ABOVE the typical band (>{high})"
    if value >= median:
        return f"above median ({median}), inside the band"
    if value >= low:
        return f"below median ({median}) but inside the band ({low}-{high})"
    pct = value / low * 100
    return f"BELOW the band floor ({low}) — at {pct:.0f}% of it"


def report_computation(problems: int, minutes: float, digits: float, grade: int) -> None:
    score = dcpm(problems, minutes, digits)
    secs = minutes * 60 / problems
    print(f"{problems} problems in {minutes:g} min at {digits:g} answer digits each")
    print(f"  = {score:.1f} digits correct per minute   ({secs:.1f} s/problem)")
    print()
    if grade not in CBM_DCPM:
        print(f"  no CBM norms for grade {grade} (table covers 2-5)")
        return
    norms = CBM_DCPM[grade]
    print(f"  vs CBM-Math norms, grade {grade} (VanDerHeyden & Burns, 2009):")
    print(f"    new material (intervention): {place(score, norms['interv'])}")
    print(f"    mastered material (retention): {place(score, norms['reten'])}")
    print()
    print("  Which line applies depends on whether the skill is still being taught.")
    print("  A drill on a skill the kid supposedly OWNS is a retention probe.")


def report_facts(problems: int, minutes: float, grade: int) -> None:
    ppm = problems / minutes
    print(f"{problems} facts in {minutes:g} min = {ppm:.1f} problems per minute "
          f"({60/ppm:.1f} s/fact)")
    print()
    if grade not in FACTS_PPM:
        print(f"  no fact benchmarks for grade {grade} (table covers 3-5)")
        return
    print(f"  vs Rocket Math fact benchmarks, grade {grade}:")
    for when, (op, target) in FACTS_PPM[grade].items():
        verdict = "MET" if ppm >= target else f"short by {target - ppm:.1f}/min"
        print(f"    {when:<6} {op:<14} {target}/min  -> {verdict}")
    print()
    print("  Facts are the input to every multi-digit algorithm. Slow facts make")
    print("  long division slow for a reason that drilling long division won't fix.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--problems", type=int, help="problems completed correctly")
    ap.add_argument("--minutes", type=float, help="minutes of continuous timed work")
    ap.add_argument("--digits", type=float, default=3.0,
                    help="answer digits per problem (default 3; use the LOWER estimate)")
    ap.add_argument("--grade", type=int, required=True,
                    help="grade level to compare against (2-5)")
    ap.add_argument("--facts", action="store_true",
                    help="score as a single-digit FACT probe instead of computation")
    ap.add_argument("--anchor", action="store_true",
                    help="score this repo's May 2026 anchor measurement")
    args = ap.parse_args()

    if args.anchor:
        print(f"ANCHOR: {ANCHOR['label']}")
        print(f"source: {ANCHOR['source']}")
        print()
        report_computation(ANCHOR["problems"], ANCHOR["minutes"],
                           ANCHOR["digits"], args.grade)
        print()
        print("⚠ This is the measurement PRACTICE-PLAN-2026.md called 'inside the")
        print("  fluency benchmark'. In the unit the field actually uses, it is not.")
        print("  See SPEED.md § 'The claim this repo got wrong'.")
        return 0

    if args.problems is None or args.minutes is None:
        ap.error("--problems and --minutes are required (or use --anchor)")

    if args.facts:
        report_facts(args.problems, args.minutes, args.grade)
    else:
        report_computation(args.problems, args.minutes, args.digits, args.grade)

    print()
    print("⚠ Only valid if --minutes was a STOPWATCH on continuous work.")
    print("  Elapsed session time with breaks is not a fluency measurement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
