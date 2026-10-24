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
    ("worksheet-facts-drill.html", "facts"),
    ("worksheet-zeros-drill.html", "zeros"),
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

            if shape == "zeros":
                # One row: a OP b = c with exactly one number hidden in open boxes.
                # Split the row at the OPERATOR/= cells, rebuild each number (a hidden
                # one from the KEY's fill digits) and re-derive the equation here with
                # plain arithmetic -- never by importing drill_gen.
                row = sorted([c for c in cs if c["t"]], key=lambda c: c["c"])
                toks, cur = [], []
                for c in row:
                    if c["t"] in ("×", "÷", "="):
                        toks += [cur, c["t"]]
                        cur = []
                    else:
                        cur.append(c)
                toks.append(cur)
                check(len(toks) == 5 and toks[1] in ("×", "÷") and toks[3] == "=",
                      f"{tag}: row is not 'a OP b = c' ({[t if isinstance(t, str) else '..' for t in toks]})")
                if len(toks) != 5:
                    continue
                hidden = [i for i in (0, 2, 4) if any("f" in c["cls"] for c in toks[i])]
                check(len(hidden) == 1, f"{tag}: {len(hidden)} hidden numbers, want exactly 1")
                vals = [int("".join(c["t"] for c in toks[i])) if toks[i] else None
                        for i in (0, 2, 4)]
                check(None not in vals, f"{tag}: a number is missing from the key")
                if None in vals:
                    continue
                a, b, cc = vals
                if toks[1] == "×":
                    check(a * b == cc, f"{tag}: {a}×{b} != {cc}")
                else:
                    check(b != 0 and a == b * cc, f"{tag}: {a}÷{b} != {cc} (or not exact)")
                for n in vals:
                    check(n % 10 == 0 or 2 <= n <= 9,
                          f"{tag}: {n} is neither a multiple of 10 nor a digit 2-9")
                # the skill under test: at least one number carries a trailing zero
                check(any(n % 10 == 0 for n in vals), f"{tag}: no trailing zero in {vals}")
            elif shape == "facts":
                # One row: [x] [op] [y] [=] [ans...]. Operands are the 'g' cells,
                # the answer is whatever is in the fill boxes. Re-derived here with
                # plain arithmetic, never by importing drill_gen.
                given = sorted([c for c in cs if "g" in c["cls"] and c["t"]],
                               key=lambda c: c["c"])
                check(len(given) == 4, f"{tag}: {len(given)} given cells, want 4")
                if len(given) != 4:
                    continue
                x, sym, y, eq = (given[0]["t"], given[1]["t"],
                                 given[2]["t"], given[3]["t"])
                check(eq == "=", f"{tag}: no = sign")
                check(sym in ("×", "÷"), f"{tag}: operator {sym!r} not × or ÷")
                x, y = int(x), int(y)
                ans = num([c for c in cs if "f" in c["cls"]])
                check(ans is not None, f"{tag}: key has no answer")
                if ans is None:
                    continue
                if sym == "×":
                    check(2 <= x <= 9 and 2 <= y <= 9,
                          f"{tag}: {x}×{y} has an operand outside 2-9")
                    check(ans == x * y, f"{tag}: {x}×{y} != {ans}")
                else:
                    check(2 <= y <= 9, f"{tag}: divisor {y} outside 2-9")
                    check(x % y == 0, f"{tag}: {x}÷{y} is not exact — that's long "
                                      f"division, not a fact")
                    check(2 <= x // y <= 9, f"{tag}: quotient {x//y} outside 2-9")
                    check(ans == x // y, f"{tag}: {x}÷{y} != {ans}")
            elif shape == "div":
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

# --- the KEY must describe the sheet the kid is actually holding ---------------
#
# Added 2026-08-03 after a mutation that swapped two problems on a kid sheet and
# left the key untouched passed all 1416 checks clean. Everything above audits the
# keys' arithmetic and the kid sheets' leak-freedom, and NOTHING tied the two
# together — so a key could be internally perfect and still grade the wrong sheet.
#
# That was always a hole; --skill facts made it load-bearing, because the fact
# probe's key IS the grading instrument for a measurement the week's plan turns on.
#
# Compares the GIVEN cells (class "g") positionally. On a `plain` layout the kid's
# prompt cells are deliberately blanked while the key's are not, so the kid's
# givens must be a SUBSET of the key's, not equal to them.
for path, shape in TARGETS:
    groups = list(sheets(path))
    kid_sheets = [(t, p) for t, k, p in groups if not k]
    key_sheets = [(t, p) for t, k, p in groups if k]
    check(len(kid_sheets) == len(key_sheets),
          f"{path}: {len(kid_sheets)} kid sheets but {len(key_sheets)} keys")
    for (kt, kprobs), (yt, yprobs) in zip(kid_sheets, key_sheets):
        check(len(kprobs) == len(yprobs),
              f"{path}:{kt[:30]}: {len(kprobs)} problems but key has {len(yprobs)}")
        for pi, (kp, yp) in enumerate(zip(kprobs, yprobs), 1):
            kg = {(c["r"], c["c"], c["t"]) for c in cells(kp)
                  if "g" in c["cls"] and c["t"]}
            yg = {(c["r"], c["c"], c["t"]) for c in cells(yp)
                  if "g" in c["cls"] and c["t"]}
            check(kg <= yg,
                  f"{path}:{kt[:30]}#{pi}: key does not match the kid's problem "
                  f"(kid-only givens: {sorted(kg - yg)[:4]})")

# duplicate-problem check per sheet
for path, shape in TARGETS:
    for title, is_key, probs in sheets(path):
        if not is_key:
            continue
        sigs = []
        for prob in probs:
            cs = cells(prob)
            if shape == "zeros":
                # givens + WHERE the hole is, so '40 x ? = 240' and '? x 6 = 240' differ
                g = sorted([c for c in cs if "g" in c["cls"] and c["t"]],
                           key=lambda c: c["c"])
                sigs.append(tuple((c["c"], c["t"]) for c in g))
            elif shape == "facts":
                g = sorted([c for c in cs if "g" in c["cls"] and c["t"]],
                           key=lambda c: c["c"])
                sigs.append(tuple(c["t"] for c in g) if len(g) == 4 else ("?",))
            elif shape == "div":
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
