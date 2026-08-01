#!/usr/bin/env python3
"""Independently verify the generated animations. Must exit 0 before anyone sees them.

This does NOT import specs.py's step builders. It reads `index.html`, pulls the
embedded JSON back out, and checks it two ways:

  1. ARITHMETIC — re-runs each algorithm from scratch, here, and compares.
  2. LAYOUT — reads the digits back off the grid by row and column and asserts
     they spell the right numbers in the right columns. A correct answer written
     in the wrong column is still a wrong worksheet, and only this half catches it.

Plus structural checks: no duplicate keys, no token that never appears, no step
referring to a key that doesn't exist, nothing outside the declared grid.
"""

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
FAILS = []
CHECKS = [0]


def check(cond, label, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILS.append(f"{label}" + (f" — {detail}" if detail else ""))
    return cond


def load():
    html = (HERE / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<script id="ANIM" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        print("FATAL: no embedded ANIM json in index.html — run build_animations.py")
        sys.exit(1)
    return json.loads(m.group(1)), html


# ------------------------------------------------------------ board reader

def _digit_toks(toks, r, skip=()):
    """Marks on row r that are digits — the operator gutter (×, −, the divisor) and
    the R-label are furniture, not part of the number the row spells."""
    return [t for t in toks if t["r"] == r
            and "op" not in t["cls"].split()
            and "rlab" not in t["cls"].split()
            and t["k"] not in skip]


def row_text(toks, r, skip=()):
    """The digits on row r, read left to right, as written."""
    items = sorted(_digit_toks(toks, r, skip), key=lambda t: t["c"])
    return "".join(t["t"] for t in items)


def row_cols(toks, r, skip=()):
    return sorted(t["c"] for t in _digit_toks(toks, r, skip))


def contiguous(a, r, skip=(), label=""):
    """The digits of a written number must sit in adjacent columns. Reading a row
    left-to-right gives the right string even if a digit drifted into the wrong
    column, so the text check alone cannot catch a misalignment. This can."""
    cols = row_cols(a["toks"], r, skip)
    ok = not cols or cols == list(range(min(cols), min(cols) + len(cols)))
    check(ok, f"[{a['id']}] row {r} {label} digits not in adjacent columns", str(cols))


def plain(s):
    """Narration with the markup stripped, so text checks aren't defeated by a <b>."""
    return re.sub(r"<[^>]+>", "", s or "")


def ones_col(a):
    """Grid column of the ones place: last digit column."""
    return a["cols"] - 1 if a["id"].endswith("div") else a["cols"]


# ------------------------------------------------------------ the model

def verify_model(a, x, y, kind):
    """The model is a SECOND derivation of the same calculation, so it is worth
    exactly as much as it can be independently falsified. Check it against x and y
    directly, never against the board it is meant to corroborate."""
    m = a["model"]

    if m["kind"] == "area":
        top, bot = x, y
        check(sum(c["v"] for c in m["cols"]) == top,
              f"[{a['id']}] area columns sum to {sum(c['v'] for c in m['cols'])}, want {top}")
        check(sum(r["v"] for r in m["rows"]) == bot,
              f"[{a['id']}] area rows sum to {sum(r['v'] for r in m['rows'])}, want {bot}")
        # every column and row is a single place value: 200, 40, 7 — never 47
        for c in m["cols"] + m["rows"]:
            d = str(c["v"])
            check(d == d[0] + "0" * (len(d) - 1),
                  f"[{a['id']}] model band {c['v']} is not a single place value")
        seen = set()
        for cell in m["cells"]:
            want = m["rows"][cell["r"]]["v"] * m["cols"][cell["c"]]["v"]
            check(cell["v"] == want,
                  f"[{a['id']}] area cell r{cell['r']}c{cell['c']} = {cell['v']}, want {want}")
            seen.add((cell["r"], cell["c"]))
        check(len(seen) == len(m["rows"]) * len(m["cols"]),
              f"[{a['id']}] area grid has holes", f"{len(seen)} cells for "
              f"{len(m['rows'])}×{len(m['cols'])}")
        check(sum(c["v"] for c in m["cells"]) == top * bot,
              f"[{a['id']}] area cells sum to {sum(c['v'] for c in m['cells'])}, want {top*bot}")
        check(m["total"] == top * bot, f"[{a['id']}] model total", str(m["total"]))

        if "rowSums" in m:
            for ri, rs in enumerate(m["rowSums"]):
                want = sum(c["v"] for c in m["cells"] if c["r"] == ri)
                check(rs == want, f"[{a['id']}] rowSum {ri} = {rs}, want {want}")
            # and the two strips must BE the two written partial products
            p1, p2 = top * (bot % 10), top * (bot // 10) * 10
            check(sorted(m["rowSums"]) == sorted([p1, p2]),
                  f"[{a['id']}] rowSums {m['rowSums']} are not the partial products {[p1, p2]}")
            check(set(r.get("maps") for r in m["rows"]) == {"p1", "p2"},
                  f"[{a['id']}] area rows don't map to the two written rows")

    else:
        dividend, divisor = x, y
        q, rem = divmod(dividend, divisor)
        check(m["start"] == dividend, f"[{a['id']}] ladder start", str(m["start"]))
        check(m["divisor"] == divisor, f"[{a['id']}] ladder divisor", str(m["divisor"]))
        check(sum(r["q"] for r in m["rows"]) == q,
              f"[{a['id']}] partial quotients sum to {sum(r['q'] for r in m['rows'])}, want {q}")
        left = dividend
        for i, r in enumerate(m["rows"]):
            check(r["prod"] == r["q"] * divisor,
                  f"[{a['id']}] ladder row {i}: {r['q']} × {divisor} != {r['prod']}")
            # each partial quotient is a clean place value (600, 0, 4 — never 604)
            d = str(r["q"])
            check(r["q"] == 0 or d == d[0] + "0" * (len(d) - 1),
                  f"[{a['id']}] partial quotient {r['q']} is not a single place value")
            left -= r["prod"]
            check(r["left"] == left,
                  f"[{a['id']}] ladder row {i} leftover {r['left']}, want {left}")
        check(m["remainder"] == rem == left, f"[{a['id']}] ladder remainder", str(m["remainder"]))
        check(rem < divisor, f"[{a['id']}] remainder {rem} not smaller than divisor {divisor}")
        check(m["quotient"] == q, f"[{a['id']}] ladder quotient", str(m["quotient"]))

    # every step must point at a real part of the model, and explain itself
    n_rows = len(m["rows"])
    n_cols = len(m.get("cols", []))
    for i, st in enumerate(a["steps"]):
        check(bool(st.get("why")), f"[{a['id']}] step {i} ({st['label']}) has no `why`")
        for field, limit in (("modelRow", n_rows), ("modelCell", n_cols)):
            v = st.get(field)
            if v is None or v == "all":
                continue
            check(isinstance(v, int) and 0 <= v < limit,
                  f"[{a['id']}] step {i} {field}={v} outside 0..{limit-1}")


def verify_bubbles(a, top, bot):
    """The product bubble is the number the algorithm normally hides. Two things must
    hold or it teaches a lie: the sequence of bubbles must be the real running products,
    and the digit that flies out of the bubble must be the digit that lands on the board."""
    toks = {t["k"]: t for t in a["toks"]}

    # --- every bubble digit must physically land where the split says it does
    for i, st in enumerate(a["steps"]):
        if st.get("split"):
            check(bool(st.get("bubble")), f"[{a['id']}] step {i} splits with no bubble to split")
            digits = (st.get("bubble") or {}).get("digits", [])
            seen = set()
            for sp in st["split"]:
                check(0 <= sp["part"] < len(digits),
                      f"[{a['id']}] step {i} flies part {sp['part']} of a {len(digits)}-digit bubble")
                check(sp["to"] in toks, f"[{a['id']}] step {i} flies to unknown mark {sp['to']}")
                if 0 <= sp["part"] < len(digits) and sp["to"] in toks:
                    check(digits[sp["part"]] == toks[sp["to"]]["t"],
                          f"[{a['id']}] step {i}: bubble digit {digits[sp['part']]!r} flies to "
                          f"{sp['to']} which reads {toks[sp['to']]['t']!r}")
                seen.add(sp["part"])
                check(sp["to"] in st.get("show", []),
                      f"[{a['id']}] step {i} flies to {sp['to']} but never reveals it")
            check(seen == set(range(len(digits))),
                  f"[{a['id']}] step {i} leaves bubble digits unaccounted for", str(sorted(seen)))

    # --- the bubbles, in order, must be the real running products
    got = [int("".join(st["bubble"]["digits"]))
           for st in a["steps"] if st.get("bubble") and not st.get("split")]
    want, tdig = [], [int(c) for c in str(top)]
    rounds = [bot] if bot < 10 else [bot % 10, bot // 10]
    for m in rounds:
        carry = 0
        for j, d in enumerate(reversed(tdig)):
            total = m * d + carry
            want.append(total)
            carry = 0 if j == len(tdig) - 1 else total // 10
    check(got == want, f"[{a['id']}] bubble sequence", f"got {got}, want {want}")


# ------------------------------------------------------------ structural

def structural(a):
    keys = [t["k"] for t in a["toks"]] + [d["k"] for d in a["decor"]]
    check(len(keys) == len(set(keys)), f"[{a['id']}] duplicate keys",
          str([k for k in keys if keys.count(k) > 1]))

    known = set(keys)
    shown = set()
    for i, s in enumerate(a["steps"]):
        for field in ("show", "flash", "strike"):
            for k in s.get(field, []):
                check(k in known, f"[{a['id']}] step {i} {field} -> unknown key {k}")
        shown |= set(s.get("show", []))
    never = known - shown
    check(not never, f"[{a['id']}] token never revealed by any step", str(sorted(never)))

    for t in a["toks"]:
        check(1 <= t["r"] <= a["rows"], f"[{a['id']}] token {t['k']} row {t['r']} outside 1..{a['rows']}")
        check(1 <= t["c"] <= a["cols"], f"[{a['id']}] token {t['k']} col {t['c']} outside 1..{a['cols']}")
    for d in a["decor"]:
        check(1 <= d["c0"] <= d["c1"] <= a["cols"],
              f"[{a['id']}] decor {d['k']} spans {d['c0']}..{d['c1']} outside 1..{a['cols']}")
        check(1 <= d["r"] <= a["rows"],
              f"[{a['id']}] decor {d['k']} row {d['r']} outside 1..{a['rows']}")

    check(len(a["steps"]) >= 4, f"[{a['id']}] suspiciously few steps", str(len(a["steps"])))
    for i, s in enumerate(a["steps"]):
        check(bool(s.get("say")), f"[{a['id']}] step {i} has no narration")
        check(bool(s.get("label")), f"[{a['id']}] step {i} has no label")


# ------------------------------------------------------------ multiplication

def verify_mult1(a, top, bot):
    toks = a["toks"]
    product = top * bot
    check(a["answer"] == str(product), f"[{a['id']}] declared answer", a["answer"])
    check(row_text(toks, 2) == str(top), f"[{a['id']}] top row reads {row_text(toks,2)!r}, want {top}")
    check(row_text(toks, 3) == str(bot), f"[{a['id']}] bottom row reads {row_text(toks,3)!r}, want {bot}")
    check(row_text(toks, 5) == str(product),
          f"[{a['id']}] answer row reads {row_text(toks,5)!r}, want {product}")

    # ones columns must all line up on the right edge
    W = a["cols"] - 1
    for r, want in ((2, top), (3, bot), (5, product)):
        cols = row_cols(toks, r)
        check(max(cols) == W + 1, f"[{a['id']}] row {r} ones digit in col {max(cols)}, want {W+1}")

    for r, lbl in ((2, "top"), (3, "bottom"), (5, "answer")):
        contiguous(a, r, label=lbl)

    # carries, re-derived here
    carry, expected = 0, {}
    tdig = [int(c) for c in str(top)]
    for j, d in enumerate(reversed(tdig)):
        total = bot * d + carry
        last = j == len(tdig) - 1
        carry = 0 if last else total // 10
        if carry:
            expected[W + 1 - (j + 1)] = str(carry)      # written above the NEXT column
    got = {t["c"]: t["t"] for t in toks if "carry" in t["cls"].split()}
    check(got == expected, f"[{a['id']}] carry row", f"got {got}, want {expected}")


def verify_mult2(a, top, bot):
    toks = a["toks"]
    p1, p2, product = top * (bot % 10), top * (bot // 10) * 10, top * bot
    check(a["answer"] == str(product), f"[{a['id']}] declared answer", a["answer"])
    check(row_text(toks, 2) == str(top), f"[{a['id']}] top row {row_text(toks,2)!r} want {top}")
    check(row_text(toks, 3) == str(bot), f"[{a['id']}] bottom row {row_text(toks,3)!r} want {bot}")
    check(row_text(toks, 5) == str(p1), f"[{a['id']}] partial 1 {row_text(toks,5)!r} want {p1}")
    check(row_text(toks, 6) == str(p2), f"[{a['id']}] partial 2 {row_text(toks,6)!r} want {p2}")
    check(row_text(toks, 8) == str(product), f"[{a['id']}] answer {row_text(toks,8)!r} want {product}")

    # the placeholder zero: partial 2 must physically end in a 0 in the ones column
    W = a["cols"] - 1
    zeros = [t for t in toks if t["r"] == 6 and t["c"] == W + 1]
    check(len(zeros) == 1 and zeros[0]["t"] == "0",
          f"[{a['id']}] no placeholder 0 in the ones column of row 2", str(zeros))
    for r, lbl in ((2, "top"), (3, "bottom"), (5, "partial 1"), (6, "partial 2"), (8, "answer")):
        contiguous(a, r, label=lbl)
    check(p1 + p2 == product, f"[{a['id']}] partials don't sum to the answer")
    # and it must be taught, not just drawn
    check(any("0 in the ones column" in plain(s.get("say")) for s in a["steps"]),
          f"[{a['id']}] the placeholder zero is never explained in narration")

    # both carry sets, re-derived
    for tag, mult in (("cA", bot % 10), ("cB", bot // 10)):
        carry, expected = 0, {}
        tdig = [int(c) for c in str(top)]
        for j, d in enumerate(reversed(tdig)):
            total = mult * d + carry
            last = j == len(tdig) - 1
            carry = 0 if last else total // 10
            if carry:
                expected[W + 1 - (j + 1)] = str(carry)
        got = {t["c"]: t["t"] for t in toks if t["k"].startswith(tag)}
        check(got == expected, f"[{a['id']}] carry set {tag}", f"got {got}, want {expected}")


# ------------------------------------------------------------ long division

def verify_div(a, dividend, divisor):
    toks = a["toks"]
    quotient, remainder = divmod(dividend, divisor)
    check(a["answer"] == f"{quotient} R{remainder}", f"[{a['id']}] declared answer", a["answer"])

    check(row_text(toks, 2, skip={"dv"}) == str(dividend),
          f"[{a['id']}] dividend row {row_text(toks,2,skip={'dv'})!r} want {dividend}")
    dv = [t for t in toks if t["k"] == "dv"]
    check(len(dv) == 1 and dv[0]["t"] == str(divisor) and dv[0]["c"] == 1,
          f"[{a['id']}] divisor not in the gutter column", str(dv))
    check(row_text(toks, 1) == str(quotient),
          f"[{a['id']}] quotient row {row_text(toks,1)!r} want {quotient}")
    rlab = [t for t in toks if "rlab" in t["cls"].split()]
    check(len(rlab) == 1 and rlab[0]["t"] == f"R{remainder}",
          f"[{a['id']}] remainder label", str(rlab))

    contiguous(a, 2, skip={"dv"}, label="dividend")
    contiguous(a, 1, label="quotient")

    # --- re-run long division here, independently
    ddig = [int(c) for c in str(dividend)]
    cur, started, trace = 0, False, []
    for i, d in enumerate(ddig):
        cur = cur * 10 + d
        if not started and cur < divisor:
            continue
        started = True
        q, prod = cur // divisor, (cur // divisor) * divisor
        rem = cur - prod
        trace.append({"i": i, "q": q, "prod": prod, "rem": rem, "cur": cur})
        cur = rem

    check("".join(str(t["q"]) for t in trace) == str(quotient),
          f"[{a['id']}] traced quotient digits disagree with {quotient}")
    check(trace[-1]["rem"] == remainder, f"[{a['id']}] traced remainder disagrees")

    # --- each quotient digit sits directly above the dividend digit it consumed
    qtoks = {t["c"]: t["t"] for t in toks if "quo" in t["cls"].split()}
    want_q = {t["i"] + 2: str(t["q"]) for t in trace}
    check(qtoks == want_q, f"[{a['id']}] quotient column alignment", f"got {qtoks}, want {want_q}")

    # --- each subtraction row, and each leftover row
    for k, t in enumerate(trace):
        sub_r, rem_r = 3 + 3 * k, 5 + 3 * k
        check(row_text(toks, sub_r) == str(t["prod"]),
              f"[{a['id']}] subtraction row {sub_r} reads {row_text(toks,sub_r)!r}, want {t['prod']}")
        check(max(row_cols(toks, sub_r)) == t["i"] + 2,
              f"[{a['id']}] subtraction row {sub_r} not right-aligned under col {t['i']+2}")
        check(t["rem"] < divisor,
              f"[{a['id']}] leftover {t['rem']} is not smaller than the divisor {divisor}")

        contiguous(a, sub_r, label="subtraction")
        contiguous(a, rem_r, label="leftover")
        rules = [d for d in a["decor"] if d["kind"] == "rule" and d["r"] == sub_r + 1]
        check(len(rules) == 1, f"[{a['id']}] no subtraction rule line under row {sub_r}")
        if rules:
            check(rules[0]["c1"] == t["i"] + 2,
                  f"[{a['id']}] rule under row {sub_r} ends at col {rules[0]['c1']}, want {t['i']+2}")

        text = row_text(toks, rem_r)
        if k + 1 < len(trace):
            check(int(text) == trace[k + 1]["cur"],
                  f"[{a['id']}] row {rem_r} reads {text!r}; next round divides {trace[k+1]['cur']}")
        else:
            check(int(text) == remainder,
                  f"[{a['id']}] final leftover row reads {text!r}, want {remainder}")

    check(a["rows"] == 2 + 3 * len(trace),
          f"[{a['id']}] row count {a['rows']}, want {2 + 3*len(trace)}")

    # --- the two traps this drill exists for
    if any(t["q"] == 0 for t in trace):
        check(any("0 up top" in plain(s.get("say")) or "Write the 0" in plain(s.get("trap"))
                  for s in a["steps"]),
              f"[{a['id']}] has a zero in the quotient but never teaches writing it")
    check(any(s["label"] in ("D", "M", "S", "B") for s in a["steps"]),
          f"[{a['id']}] steps aren't labelled with the D-M-S-B moves")


# ------------------------------------------------------------ you-try

def verify_try(a, kind, items):
    got = [(t["q"], t["a"]) for t in a["youTry"]]
    want = []
    for x, y in items:
        if kind == "mul":
            want.append((f"{x} × {y}", str(x * y)))
        else:
            want.append((f"{x} ÷ {y}", f"{x // y} R{x % y}"))
    check(got == want, f"[{a['id']}] you-try answers", f"got {got}, want {want}")
    check(len({q for q, _ in got}) == len(got), f"[{a['id']}] duplicate you-try problem")


# ------------------------------------------------------------ page-level

def page_checks(html, anims):
    check("<script src=" not in html and "<link rel=\"stylesheet\"" not in html,
          "page is not self-contained (external script or stylesheet)")
    check("prefers-reduced-motion" in html, "no reduced-motion fallback")
    check("@media print" in html, "no print stylesheet")
    ids = [a["id"] for a in anims]
    check(len(ids) == len(set(ids)), "duplicate animation ids")
    for a in anims:
        check(a["kid"] in ("kid1", "kid2"), f"[{a['id']}] unexpected kid name {a['kid']!r}")
        check(a["drillSlug"] in html, f"[{a['id']}] drill slug missing from page")


def main():
    anims, html = load()
    by_id = {a["id"]: a for a in anims}
    check(set(by_id) == {"kid1-mult", "kid1-div", "kid2-mult", "kid2-div"},
          "unexpected set of animations", str(sorted(by_id)))

    for a in anims:
        structural(a)

    if "kid1-mult" in by_id:
        verify_mult1(by_id["kid1-mult"], 247, 6)
        verify_model(by_id["kid1-mult"], 247, 6, "area")
        verify_bubbles(by_id["kid1-mult"], 247, 6)
        verify_try(by_id["kid1-mult"], "mul", [(138, 4), (306, 7), (429, 8)])
    if "kid1-div" in by_id:
        verify_div(by_id["kid1-div"], 67, 5)
        verify_model(by_id["kid1-div"], 67, 5, "ladder")
        verify_try(by_id["kid1-div"], "div", [(83, 6), (59, 4), (74, 8)])
    if "kid2-mult" in by_id:
        verify_mult2(by_id["kid2-mult"], 47, 36)
        verify_model(by_id["kid2-mult"], 47, 36, "area")
        verify_bubbles(by_id["kid2-mult"], 47, 36)
        verify_try(by_id["kid2-mult"], "mul", [(58, 24), (73, 46), (89, 37)])
    if "kid2-div" in by_id:
        verify_div(by_id["kid2-div"], 4231, 7)
        verify_model(by_id["kid2-div"], 4231, 7, "ladder")
        verify_try(by_id["kid2-div"], "div", [(3025, 6), (5138, 9), (2417, 4)])

    page_checks(html, anims)

    print(f"{CHECKS[0]} checks run")
    if FAILS:
        print(f"\n{len(FAILS)} FAILED:")
        for f in FAILS:
            print("  ✗ " + f)
        sys.exit(1)

    for a in anims:
        print(f"  ✓ {a['id']:<12} {len(a['steps']):>2} steps · grid {a['cols']}×{a['rows']} · "
              f"answer {a['answer']}")
    print("\nALL PASS")


if __name__ == "__main__":
    main()
