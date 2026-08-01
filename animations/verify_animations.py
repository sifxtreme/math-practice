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
            # the strips must BE the written partial products, one per multiplier digit
            rounds = [int(c) for c in str(bot)][::-1]
            parts = sorted(top * mm * 10 ** k for k, mm in enumerate(rounds))
            check(sorted(m["rowSums"]) == parts,
                  f"[{a['id']}] rowSums {sorted(m['rowSums'])} are not the partial "
                  f"products {parts}")
            check(set(r.get("maps") for r in m["rows"])
                  == {f"p{k+1}" for k in range(len(rounds))},
                  f"[{a['id']}] area rows don't map one-to-one onto the written rows")

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
    """The chip is a little expression, and it is the only place the intermediate
    numbers are ever visible. Three things have to hold or it teaches a lie:
      - the arithmetic written in the chip is TRUE  (raw + carry == total)
      - the carry it pulls in is the digit actually sitting on the shelf
      - the digit that flies out of the chip is the digit that lands on the board
    """
    toks = {t["k"]: t for t in a["toks"]}

    def cells(st):
        return (st.get("bubble") or {}).get("cells") or []

    for i, st in enumerate(a["steps"]):
        cs = cells(st)
        if not cs:
            check(not st.get("split"), f"[{a['id']}] step {i} splits with no chip to split")
            continue

        # --- the chip's own arithmetic, read straight off the cells
        parts = [c for c in cs if "part" in c]
        if parts:
            idx = [c["part"] for c in parts]
            check(idx == list(range(len(parts))),
                  f"[{a['id']}] step {i} chip parts are not 0..n", str(idx))
            total = int("".join(c["t"] for c in parts))
            ops = [k for k, c in enumerate(cs) if c.get("op")]
            if ops:
                lhs = int("".join(c["t"] for c in cs[:ops[0]]))
                mid = [c for c in cs if c.get("arrive")]
                check(len(mid) == 1, f"[{a['id']}] step {i} chip has an operator but nothing arriving")
                if mid:
                    check(lhs + int(mid[0]["t"]) == total,
                          f"[{a['id']}] step {i} chip claims {lhs} + {mid[0]['t']} = {total}")
                    src = mid[0]["arrive"]
                    check(src in toks, f"[{a['id']}] step {i} carry arrives from unknown mark {src}")
                    if src in toks:
                        check(toks[src]["t"] == mid[0]["t"],
                              f"[{a['id']}] step {i} pulls a {mid[0]['t']} off the shelf, "
                              f"but {src} reads {toks[src]['t']!r}")
                check(st.get("bubble", {}).get("grewFrom") is None
                      or st["bubble"]["grewFrom"] == ops[0],
                      f"[{a['id']}] step {i} grows from the wrong cell")

        # --- every flying digit must be the digit that lands
        if st.get("split"):
            seen = set()
            for sp in st["split"]:
                match = [c for c in cs if c.get("part") == sp["part"]]
                check(len(match) == 1,
                      f"[{a['id']}] step {i} flies part {sp['part']}, which the chip has "
                      f"{len(match)} of")
                check(sp["to"] in toks, f"[{a['id']}] step {i} flies to unknown mark {sp['to']}")
                if match and sp["to"] in toks:
                    check(match[0]["t"] == toks[sp["to"]]["t"],
                          f"[{a['id']}] step {i}: chip digit {match[0]['t']!r} flies to "
                          f"{sp['to']} which reads {toks[sp['to']]['t']!r}")
                check(sp["to"] in st.get("show", []),
                      f"[{a['id']}] step {i} flies to {sp['to']} but never reveals it")
                seen.add(sp["part"])
            check(seen == {c["part"] for c in cs if "part" in c},
                  f"[{a['id']}] step {i} leaves chip digits unaccounted for", str(sorted(seen)))

    # --- the sequence of totals must be the real running products
    got = [int("".join(c["t"] for c in cells(st) if "part" in c))
           for st in a["steps"] if st.get("split")]
    want, tdig = [], [int(c) for c in str(top)]
    rounds = [bot] if bot < 10 else [int(c) for c in str(bot)][::-1]
    for m in rounds:
        if m == 0:
            want.append(0)      # a whole round of zeros collapses to ONE mark, not N
            continue
        carry = 0
        for j, d in enumerate(reversed(tdig)):
            t = m * d + carry
            want.append(t)
            carry = 0 if j == len(tdig) - 1 else t // 10
    check(got == want, f"[{a['id']}] chip totals in order", f"got {got}, want {want}")

    # --- every multiplication that takes a carry must SHOW the addition happening
    n_add = sum(1 for st in a["steps"]
                if (st.get("bubble") or {}).get("grewFrom") is not None)
    n_need = 0
    for m in rounds:
        if m == 0:
            continue
        carry = 0
        for j, d in enumerate(reversed(tdig)):
            t = m * d + carry
            if carry:
                n_need += 1
            carry = 0 if j == len(tdig) - 1 else t // 10
    check(n_add == n_need,
          f"[{a['id']}] {n_need} carries get added in, but only {n_add} chips show it")


def verify_trials(a, dividend, divisor):
    """The D-step chip shows the candidates a kid weighs. A wrong verdict here is worse
    than a wrong answer -- it teaches the wrong RULE. So re-derive every verdict from
    scratch, and check that the digit marked as fitting is the digit that lands up top."""
    toks = {t["k"]: t for t in a["toks"]}

    # re-run the division to know what `cur` and `q` really are at each D step
    ddig = [int(c) for c in str(dividend)]
    cur, started, trace = 0, False, []
    for i, d in enumerate(ddig):
        cur = cur * 10 + d
        if not started and cur < divisor:
            trace.append({"kind": "skip", "cur": cur, "q": 0})
            continue
        started = True
        q = cur // divisor
        trace.append({"kind": "d", "cur": cur, "q": q, "i": i})
        cur -= q * divisor

    chips = [st for st in a["steps"] if (st.get("bubble") or {}).get("trials")]
    # a TRY THEM chip is carried through D and M, so count distinct label groups
    tries = [st for st in a["steps"] if st["label"] in ("TRY THEM", "TOO SMALL")
             and (st.get("bubble") or {}).get("trials")]
    check(len(tries) == len(trace),
          f"[{a['id']}] {len(trace)} decisions to make, {len(tries)} trial chips")

    for st, tr in zip(tries, trace):
        b = st["bubble"]
        check(b["cur"] == tr["cur"],
              f"[{a['id']}] trial chip says it is dividing {b['cur']}, really {tr['cur']}")
        check(b["divisor"] == divisor, f"[{a['id']}] trial chip divisor", str(b["divisor"]))
        for row in b["trials"]:
            check(row["prod"] == row["n"] * divisor,
                  f"[{a['id']}] trial {row['n']} × {divisor} != {row['prod']}")
            want = ("big" if row["prod"] > tr["cur"]
                    else "small" if tr["cur"] - row["prod"] >= divisor else "fits")
            check(row["v"] == want,
                  f"[{a['id']}] trial {row['n']} × {divisor} = {row['prod']} against "
                  f"{tr['cur']} is labelled {row['v']!r}, should be {want!r}")
        winners = [r for r in b["trials"] if "part" in r]
        if tr["q"]:
            check(len(winners) == 1 and winners[0]["n"] == tr["q"],
                  f"[{a['id']}] the row marked as fitting is {winners}, quotient digit is {tr['q']}")
        else:
            check(not winners, f"[{a['id']}] a 'fits' row exists where the answer is 0")

    # the chosen digit must be the digit that lands in the quotient
    for st in a["steps"]:
        b = st.get("bubble") or {}
        if st.get("split") and b.get("trials"):
            for sp in st["split"]:
                win = [r for r in b["trials"] if r.get("part") == sp["part"]]
                check(len(win) == 1, f"[{a['id']}] D step flies part {sp['part']}, no such row")
                check(sp["to"] in toks, f"[{a['id']}] D step flies to unknown {sp['to']}")
                if win and sp["to"] in toks:
                    check(str(win[0]["n"]) == toks[sp["to"]]["t"],
                          f"[{a['id']}] trial picked {win[0]['n']} but {sp['to']} reads "
                          f"{toks[sp['to']]['t']!r}")
            check(st.get("keepChip"), f"[{a['id']}] D step splits the chip but does not keep it")

    # every decision must be SHOWN, not just narrated
    check(all(any(r["v"] == "small" for r in st["bubble"]["trials"])
              or st["bubble"]["trials"][0]["n"] == 1
              for st in tries),
          f"[{a['id']}] a trial chip offers no 'too small' candidate and does not start at 1")


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
    """Any multi-digit multiplier: one written row per digit, each with one more
    trailing zero than the row above, then the sum. Re-derived here from (top, bot),
    never read off the board it is checking."""
    toks = a["toks"]
    rounds = [int(c) for c in str(bot)][::-1]          # ones first, the order you work in
    N = len(rounds)
    partials = [top * m * 10 ** k for k, m in enumerate(rounds)]
    product = top * bot
    W = a["cols"] - 1
    R_TOP, R_BOT = 2, 3
    R_P = [5 + k for k in range(N)]
    R_ANS = 6 + N

    check(a["answer"] == str(product), f"[{a['id']}] declared answer", a["answer"])
    check(a["rows"] == R_ANS, f"[{a['id']}] {a['rows']} grid rows, want {R_ANS} for "
                              f"{N} rounds")
    check(row_text(toks, R_TOP) == str(top),
          f"[{a['id']}] top row {row_text(toks, R_TOP)!r} want {top}")
    check(row_text(toks, R_BOT) == str(bot),
          f"[{a['id']}] bottom row {row_text(toks, R_BOT)!r} want {bot}")
    check(row_text(toks, R_ANS) == str(product),
          f"[{a['id']}] answer {row_text(toks, R_ANS)!r} want {product}")
    check(sum(partials) == product, f"[{a['id']}] partials don't sum to the answer")
    contiguous(a, R_TOP, label="top")
    contiguous(a, R_BOT, label="bottom")
    contiguous(a, R_ANS, label="answer")

    for k in range(N):
        txt = row_text(toks, R_P[k])
        # a round whose multiplier is 0 is a row of zeros: its k placeholders plus one
        # more for the product. That is 0 written with leading zeros, which is what a
        # kid writes, so match the marks rather than the value.
        want_txt = "0" * (k + 1) if rounds[k] == 0 else str(partials[k])
        check(txt == want_txt,
              f"[{a['id']}] row {k+1} reads {txt!r}, want {want_txt}")
        contiguous(a, R_P[k], label=f"partial {k+1}")
        # row k must physically end in k zeros — this is the placeholder, and it is
        # the single most common way to get a multi-digit multiply wrong
        if k:
            check(txt.endswith("0" * k),
                  f"[{a['id']}] row {k+1} is {txt!r}; it must end in {k} placeholder "
                  f"zero(s) because it is multiplying by {rounds[k] * 10 ** k}")
            zeros = [t for t in toks if t["r"] == R_P[k] and t["c"] > W + 1 - k]
            check(len(zeros) == k,
                  f"[{a['id']}] row {k+1} has {len(zeros)} marks in its last {k} column(s)")

    # every round after the first must have a step that TEACHES its zeros
    zsteps = [st for st in a["steps"] if st["label"].startswith("THE ZERO")]
    check(len(zsteps) == N - 1,
          f"[{a['id']}] {N-1} rounds need placeholder zeros, {len(zsteps)} steps teach them")

    # carries, re-derived per round
    tdig = [int(c) for c in str(top)]
    for k, m in enumerate(rounds):
        got = {t["c"]: t["t"] for t in toks if t["k"].startswith(f"c{k}_")}
        if m == 0:
            check(not got, f"[{a['id']}] round {k+1} multiplies by 0 but carries {got}")
            continue
        carry, expected = 0, {}
        for j, d in enumerate(reversed(tdig)):
            total = m * d + carry
            carry = 0 if j == len(tdig) - 1 else total // 10
            if carry:
                expected[W + 1 - (j + 1)] = str(carry)
        check(got == expected, f"[{a['id']}] round {k+1} carries", f"got {got}, want {expected}")


def verify_div(a, dividend, divisor):
    toks = a["toks"]
    quotient, remainder = divmod(dividend, divisor)
    check(a["answer"] == f"{quotient} R{remainder}", f"[{a['id']}] declared answer", a["answer"])

    # the gutter is as wide as the divisor, so a 2-digit divisor shifts every column
    ndiv = len(str(divisor))
    gut = {f"dv{i}" for i in range(ndiv)}
    check(row_text(toks, 2, skip=gut) == str(dividend),
          f"[{a['id']}] dividend row {row_text(toks, 2, skip=gut)!r} want {dividend}")
    dv = sorted([t for t in toks if t["k"].startswith("dv")], key=lambda t: t["c"])
    check("".join(t["t"] for t in dv) == str(divisor),
          f"[{a['id']}] gutter spells {''.join(t['t'] for t in dv)!r}, want {divisor}")
    check([t["c"] for t in dv] == list(range(1, ndiv + 1)),
          f"[{a['id']}] divisor not laid out across the gutter columns", str(dv))
    check(row_text(toks, 1) == str(quotient),
          f"[{a['id']}] quotient row {row_text(toks,1)!r} want {quotient}")
    rlab = [t for t in toks if "rlab" in t["cls"].split()]
    check(len(rlab) == 1 and rlab[0]["t"] == f"R{remainder}",
          f"[{a['id']}] remainder label", str(rlab))

    contiguous(a, 2, skip=gut, label="dividend")
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
    want_q = {t["i"] + 1 + ndiv: str(t["q"]) for t in trace}
    check(qtoks == want_q, f"[{a['id']}] quotient column alignment", f"got {qtoks}, want {want_q}")

    # --- each subtraction row, and each leftover row
    for k, t in enumerate(trace):
        sub_r, rem_r = 3 + 3 * k, 5 + 3 * k
        check(row_text(toks, sub_r) == str(t["prod"]),
              f"[{a['id']}] subtraction row {sub_r} reads {row_text(toks,sub_r)!r}, want {t['prod']}")
        check(max(row_cols(toks, sub_r)) == t["i"] + 1 + ndiv,
              f"[{a['id']}] subtraction row {sub_r} not right-aligned under col "
              f"{t['i'] + 1 + ndiv}")
        check(t["rem"] < divisor,
              f"[{a['id']}] leftover {t['rem']} is not smaller than the divisor {divisor}")

        contiguous(a, sub_r, label="subtraction")
        contiguous(a, rem_r, label="leftover")
        rules = [d for d in a["decor"] if d["kind"] == "rule" and d["r"] == sub_r + 1]
        check(len(rules) == 1, f"[{a['id']}] no subtraction rule line under row {sub_r}")
        if rules:
            check(rules[0]["c1"] == t["i"] + 1 + ndiv,
                  f"[{a['id']}] rule under row {sub_r} ends at col {rules[0]['c1']}, "
                  f"want {t['i'] + 1 + ndiv}")

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

def verify_try(a, kind, x, y):
    """Re-derive what a you-try problem has to satisfy, rather than compare against a
    list copied from the producer. Comparing lists only proves two files agree; this
    proves each problem is arithmetically right AND the same kind of hard as the
    worked example, which is the thing that actually matters."""
    items = a["youTry"]
    check(len(items) == 3, f"[{a['id']}] {len(items)} you-try problems, want 3")
    want_shape = (len(str(x)), len(str(y)))
    seen = set()
    for it in items:
        m = re.match(r"^(\d+) ([×÷]) (\d+)$", it["q"])
        if not check(bool(m), f"[{a['id']}] unparseable you-try {it['q']!r}"):
            continue
        u, op, v = int(m.group(1)), m.group(2), int(m.group(3))
        check((op == "×") == (kind == "mult"),
              f"[{a['id']}] you-try {it['q']} uses the wrong operator for this method")
        if kind == "mult":
            check(it["a"] == str(u * v), f"[{a['id']}] {it['q']} = {it['a']!r}, really {u * v}")
        else:
            # Asif 2026-08-01: dividing by 1 is a waste of the kid's time
            check(v >= 2, f"[{a['id']}] you-try {it['q']} divides by {v}")
            check(it["a"] == f"{u // v} R{u % v}",
                  f"[{a['id']}] {it['q']} = {it['a']!r}, really {u // v} R{u % v}")
            if x % y:
                check(u % v != 0,
                      f"[{a['id']}] you-try {it['q']} comes out even; the worked example "
                      f"has a remainder, so this practises a different thing")
            if len(str(x // y)) > 2 and "0" in str(x // y)[1:-1]:
                check("0" in str(u // v)[1:-1],
                      f"[{a['id']}] worked example has a zero inside the quotient, "
                      f"{it['q']} does not")
        check((len(str(u)), len(str(v))) == want_shape,
              f"[{a['id']}] you-try {it['q']} is {len(str(u))}x{len(str(v))} digits, "
              f"worked example is {want_shape[0]}x{want_shape[1]}")
        check((u, v) != (x, y), f"[{a['id']}] you-try repeats the worked example")
        check((u, v) not in seen, f"[{a['id']}] duplicate you-try {it['q']}")
        seen.add((u, v))


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

    # The problem set comes from problems.json, NOT from the artifact. Reading it out of
    # index.html would only prove the file is self-consistent: a 247 corrupted to 248
    # would verify happily against its own corrupted answer. Two sources, or no check.
    declared = json.loads((HERE / "problems.json").read_text(encoding="utf-8"))["animations"]
    check(set(by_id) == {p["id"] for p in declared},
          "index.html and problems.json disagree about which animations exist",
          f"built {sorted(by_id)} vs declared {sorted(p['id'] for p in declared)}")

    for spec in declared:
        a = by_id.get(spec["id"])
        if not check(a is not None, f"[{spec['id']}] declared but not built"):
            continue
        kind, x, y = spec["kind"], spec["x"], spec["y"]
        check((a.get("kind"), a.get("x"), a.get("y")) == (kind, x, y),
              f"[{spec['id']}] built {a.get('x')} {a.get('kind')} {a.get('y')}, "
              f"declared {x} {kind} {y}")
        check(a.get("kid") == spec["kid"], f"[{spec['id']}] wrong kid")

        structural(a)
        if kind == "mult":
            (verify_mult1 if len(str(y)) == 1 else verify_mult2)(a, x, y)
            verify_model(a, x, y, "area")
            verify_bubbles(a, x, y)
        else:
            check(y >= 2, f"[{spec['id']}] worked example divides by {y} — never by 1")
            verify_div(a, x, y)
            verify_model(a, x, y, "ladder")
            verify_trials(a, x, y)
        verify_try(a, kind, x, y)

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
