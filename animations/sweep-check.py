#!/usr/bin/env python3
"""Prove the generators are generic instead of claiming it.

`verify_animations.py` checks the four problems we ship. That says nothing about
whether 247 x 6 works because the code is right or because it is the number we
happened to tune against. This runs the SAME verification over hundreds of problems
nobody picked by hand, straight out of the generators, without touching index.html.

Run:  python3 sweep-check.py [--n 40]
Exits non-zero if any problem produces an animation that fails its own checks.

Every shape here is one the drill ladder in ../DRILLS.md actually wants. A shape
that raises is reported as UNSUPPORTED rather than crashing the sweep, so this
doubles as the honest inventory of what the generators cannot yet draw.
"""

import argparse
import sys
import traceback

import verify_animations as V
from describe import describe, pick_try
from specs import mult_by_one_digit, mult_two_by_two, long_division

# (label, kind, digits of x, digits of y) — the shapes on the ladder
SHAPES = [
    ("2-digit x 1-digit", "mult", 2, 1),
    ("3-digit x 1-digit", "mult", 3, 1),
    ("4-digit x 1-digit", "mult", 4, 1),
    ("2-digit x 2-digit", "mult", 2, 2),
    ("3-digit x 2-digit", "mult", 3, 2),
    ("3-digit x 3-digit", "mult", 3, 3),
    ("2-digit / 1-digit",  "div", 2, 1),
    ("3-digit / 1-digit",  "div", 3, 1),
    ("4-digit / 1-digit",  "div", 4, 1),
    ("3-digit / 2-digit",  "div", 3, 2),
    ("4-digit / 2-digit",  "div", 4, 2),
]


def cases(kind, nx, ny, n):
    """A deterministic spread across the shape — no randomness, so a failure found
    here is reproducible by re-running, not by luck."""
    lox, hix = 10 ** (nx - 1), 10 ** nx - 1
    loy, hiy = 10 ** (ny - 1), 10 ** ny - 1
    if ny == 1:
        loy = 2                                  # never divide or multiply by 1
    out, k = [], 1
    while len(out) < n and k < 40000:
        x = lox + (k * 313) % (hix - lox + 1)
        y = loy + (k * 97) % (hiy - loy + 1)
        k += 1
        if kind == "div" and x < y:
            continue
        if (x, y) not in out:
            out.append((x, y))
    return out


def generate(kind, x, y):
    if kind == "div":
        return long_division(x, y)
    return (mult_by_one_digit if len(str(y)) == 1 else mult_two_by_two)(x, y)


def build_one(kind, x, y):
    core = generate(kind, x, y)
    d = describe(kind, x, y)
    tries = pick_try(kind, x, y)
    return {
        "id": f"{kind}-{x}-{y}", "kid": "kid1", "theme": "teal",
        "kind": kind, "x": x, "y": y,
        "title": d["title"], "skill": d["skill"], "why": d["why"], "rules": d["rules"],
        "drillSlug": "sweep", "drillUrl": "", "traps": [],
        "youTry": [{"q": f"{a} × {b}", "a": str(a * b)} if kind == "mult"
                   else {"q": f"{a} ÷ {b}", "a": f"{a // b} R{a % b}"} for a, b in tries],
        "tryNote": d["tryNote"],
        "cols": core["cols"], "rows": core["rows"], "toks": core["toks"],
        "decor": core["decor"], "steps": core["steps"], "model": core["model"],
        "answer": str(core["answer"]),
    }


def verify_one(a, kind, x, y):
    """Run the shipped checks against one generated animation, isolated so one bad
    problem cannot contaminate the next."""
    V.FAILS.clear()
    before = V.CHECKS[0]
    V.structural(a)
    if kind == "mult":
        (V.verify_mult1 if len(str(y)) == 1 else V.verify_mult2)(a, x, y)
        V.verify_model(a, x, y, "area")
        V.verify_bubbles(a, x, y)
    else:
        V.verify_div(a, x, y)
        V.verify_model(a, x, y, "ladder")
        V.verify_trials(a, x, y)
    V.verify_try(a, kind, x, y)
    return list(V.FAILS), V.CHECKS[0] - before


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40, help="problems per shape")
    args = ap.parse_args()

    total_checks = 0
    bad, unsupported = [], []
    print(f"{'shape':<20} {'tried':>6} {'checks':>8}  result")
    for label, kind, nx, ny in SHAPES:
        tried = ok = 0
        checks = 0
        first_err = None
        for x, y in cases(kind, nx, ny, args.n):
            tried += 1
            try:
                a = build_one(kind, x, y)
            except AssertionError as e:
                first_err = f"UNSUPPORTED — {e}"
                break
            except Exception:
                first_err = "CRASH — " + traceback.format_exc(limit=1).strip().splitlines()[-1]
                break
            fails, n = verify_one(a, kind, x, y)
            checks += n
            if fails:
                bad.append((label, x, y, fails[:2]))
                if first_err is None:
                    first_err = fails[0]
            else:
                ok += 1
        total_checks += checks
        if first_err and ok == 0:
            unsupported.append((label, first_err))
            print(f"{label:<20} {tried:>6} {checks:>8}  ✗ {first_err[:64]}")
        elif ok < tried:
            print(f"{label:<20} {tried:>6} {checks:>8}  ✗ {tried - ok} of {tried} failed")
        else:
            print(f"{label:<20} {tried:>6} {checks:>8}  ✓ all {tried} pass")

    print(f"\n{total_checks:,} checks over {len(SHAPES)} shapes")
    if unsupported:
        print("\nSHAPES THE GENERATORS CANNOT DRAW YET:")
        for label, err in unsupported:
            print(f"  · {label:<20} {err[:90]}")
    if bad:
        print(f"\n{len(bad)} PROBLEM(S) FAILED VERIFICATION:")
        for label, x, y, fails in bad[:10]:
            print(f"  ✗ {label} {x},{y}")
            for f in fails:
                print(f"      {f}")
    # a shape we cannot draw is a known gap, not a regression; a generated problem
    # that fails its own checks is a real bug
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
