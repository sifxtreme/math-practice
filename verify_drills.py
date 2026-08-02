"""verify_drills.py — independent audit of the generated drill sheets.

Run it after `drill_gen.py`, before anything is printed:

    python3 drill_gen.py --skill mul && python3 verify_drills.py

WHY A SECOND VERIFIER
---------------------
`drill_gen.py` already checks itself, but it checks its own MARKS — the in-memory
structure it just built. That cannot catch a fault anywhere downstream of the marks:
a render bug, a CSS collision, an escaping problem, a shifted column. This file reads
the RENDERED HTML — the artifact that actually reaches the printer — reconstructs each
problem from its grid cells, and re-derives every answer with plain arithmetic.

**It deliberately does not import drill_gen.** Same discipline as
`animations/verify_animations.py`, and for the same reason: a verifier that takes its
problem statement from the artifact it is checking only proves the artifact is
self-consistent. A corrupted 4002 would verify happily against its own corrupted key.

WHAT IT CHECKS
--------------
- every divisor is 2-9 and every remainder is non-zero (the forced-remainder rule)
- quotient x divisor + remainder == dividend, re-derived off the grid
- every multiplier digit is 2-9 (no wasted x0 / x1 row)
- each partial product equals a x digit x 10^j **for its position** — this is what
  catches a placeholder zero in the wrong column, which a correct total would hide
- the partials sum to the total row, and the total equals a x b
- carry digits match a fresh run of the algorithm; a 2+ digit multiplier has none
- **no blank sheet contains a single answer digit**
- no duplicate problems on one sheet

IT IS MUTATION-TESTED — a check that cannot fail is not a check. Four deliberate
corruptions were each confirmed to fail it on 2026-08-01: a flipped digit in a key, a
digit leaked onto a blank sheet, a flipped carry, and a deleted carry box. The first
version of this file also had a real bug of its own (it reversed the partial-product
order and reported 18 false failures) — which is the other reason the checks are
positional and not just "does the total come out right".
"""
import re, sys

CELL = re.compile(
    r'<div class="([^"]*)" style="grid-row:(\d+);grid-column:(\d+)">([^<]*)</div>')

def sheets(path):
    doc = open(path).read()
    parts = doc.split('<div class="sheet')
    for p in parts[1:]:
        is_key = p.startswith(' key')
        title = re.search(r'<h1>([^<]*)</h1>', p)
        probs = p.split('<div class="prob"')[1:]
        yield (title.group(1) if title else "?"), is_key, probs

def cells(prob):
    out = []
    for m in CELL.finditer(prob):
        cls, gr, gc, txt = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        out.append({"cls": set(cls.split()), "r": gr - 1, "c": gc - 2,
                    "t": txt.strip()})
    return out

def num(cs):
    cs = [c for c in cs if c["t"]]
    if not cs:
        return None
    return int("".join(c["t"] for c in sorted(cs, key=lambda x: x["c"])))

fails, checks = [], 0

def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)

# Both layouts. `plain` drops the boxes from the kid's sheet but the KEY is identical,
# so every arithmetic check below applies unchanged — and the blank-sheet leak check
# still has to pass, which is the one that matters most.
import os as _os
TARGETS = [(p, sh) for p, sh in [
    ("worksheet-division-drill.html", "div"),
    ("worksheet-division-drill-plain.html", "div"),
    ("worksheet-multiplication-drill.html", "mul"),
    ("worksheet-multiplication-drill-plain.html", "mul"),
] if _os.path.exists(p)]

for path, shape in TARGETS:
    for title, is_key, probs in sheets(path):
        for pi, prob in enumerate(probs, 1):
            cs = cells(prob)
            fill = [c for c in cs if "f" in c["cls"] and c["t"]]
            tag = f"{path}:{title[:38]}#{pi}"

            if not is_key:
                # A blank sheet must not contain a single answer digit anywhere.
                check(not fill, f"{tag}: BLANK SHEET LEAKS {len(fill)} digits")
                continue

            if shape == "div":
                divisor = num([c for c in cs if c["r"] == 1 and c["c"] == 0])
                dividend = num([c for c in cs if c["r"] == 1 and c["c"] >= 2])
                quotient = num([c for c in cs if c["r"] == 0])
                rrow = [c for c in cs if c["t"] == "R"]
                check(bool(rrow), f"{tag}: no R mark")
                if not rrow:
                    continue
                rr = max(c["r"] for c in rrow)
                rem = num([c for c in cs if c["r"] == rr and "f" in c["cls"]]) or 0
                check(divisor is not None and 2 <= divisor <= 9,
                      f"{tag}: divisor {divisor} outside 2-9")
                check(quotient * divisor + rem == dividend,
                      f"{tag}: {quotient}*{divisor}+{rem} != {dividend}")
                check(0 < rem < divisor,
                      f"{tag}: remainder {rem} not in 1..{divisor-1} (forced-remainder rule)")
            else:
                # a carry row shifts the operands down one; find them by content
                grows = sorted({c["r"] for c in cs if "g" in c["cls"] and c["t"]})
                a = num([c for c in cs if c["r"] == grows[0]])
                b = num([c for c in cs if c["r"] == grows[1] and c["t"] != "×"])

                # carries are fill cells too — exclude them from the partial rows,
                # then check them against a fresh computation of the algorithm.
                carry = {c["c"]: c["t"] for c in cs if "cr" in c["cls"] and c["t"]}
                if len(str(b)) == 1:
                    ncols = max(c["c"] for c in cs) + 1
                    want, k = {}, 0
                    for j, ch in enumerate(str(a)[::-1]):
                        v = int(ch) * int(str(b)) + k
                        k = v // 10
                        if k and j + 1 < len(str(a)):
                            want[ncols - 1 - (j + 1)] = str(k)
                    check(carry == want, f"{tag}: carries {carry} != {want}")
                else:
                    check(not carry,
                          f"{tag}: carry row on a {len(str(b))}-digit multiplier")

                body = [c for c in cs if "f" in c["cls"] and "cr" not in c["cls"]]
                rows = sorted({c["r"] for c in body if c["t"]})
                vals = [num([c for c in body if c["r"] == r]) for r in rows]
                check(a is not None and b is not None, f"{tag}: missing operands")
                if a is None or b is None:
                    continue
                check(all(d in "23456789" for d in str(b)),
                      f"{tag}: multiplier {b} has a 0 or 1 digit")
                if len(str(b)) > 1:
                    *partials, total = vals
                    check(len(partials) == len(str(b)),
                          f"{tag}: {len(partials)} partial rows for a {len(str(b))}-digit multiplier")
                    # partial rows are written ones-digit FIRST, top to bottom, which
                    # already matches str(b) reversed. Do not reverse them again.
                    for j, (p, d) in enumerate(zip(partials, str(b)[::-1])):
                        check(p == a * int(d) * (10 ** j),
                              f"{tag}: partial {p} != {a}*{d}*10^{j}")
                    check(sum(partials) == total,
                          f"{tag}: partials sum {sum(partials)} != total row {total}")
                else:
                    total = vals[-1]
                check(total == a * b, f"{tag}: total {total} != {a}*{b}={a*b}")

# duplicate-problem check per sheet
for path, shape in TARGETS:
    for title, is_key, probs in sheets(path):
        if not is_key:
            continue
        sigs = []
        for prob in probs:
            cs = cells(prob)
            if shape == "div":
                sigs.append((num([c for c in cs if c["r"] == 1 and c["c"] == 0]),
                             num([c for c in cs if c["r"] == 1 and c["c"] >= 2])))
            else:
                sigs.append((num([c for c in cs if c["r"] == 0]),
                             num([c for c in cs if c["r"] == 1 and c["t"] != "×"])))
        check(len(sigs) == len(set(sigs)),
              f"{path}:{title[:30]}: duplicate problems on one sheet")

print(f"{checks} checks run")
if fails:
    print(f"\n{len(fails)} FAILED:")
    for f in fails[:25]:
        print("  ✗", f)
    sys.exit(1)
print("all passed")
