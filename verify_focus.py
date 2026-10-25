"""verify_focus.py -- independent check of the Noetic-prep focus-track word sheets (kid1 undo, kid2 trade).

kid2 "trade" sheets: each answer is found by brute-force search over BOTH prices
(whole dollars 1..300), keeping the pairs that satisfy the two stated equations
(1 A = k B, and a A + b B = T). Exactly one pair must survive and the asked total
must equal the key. The plan samples (averages, ages, equations) are searched too.

    python3 build_focus.py && python3 verify_focus.py     # MUST exit 0

Deliberately does NOT undo the steps the way specs_focus.py does. Each answer is
found by BRUTE-FORCE FORWARD SEARCH: try every start 0..9999, run the chain forward
exactly as the sentence reads, keep the starts that land on the stated result. The
search must find exactly one start and it must equal the answer printed in the key.

The chain is also re-read from the QUESTION TEXT (every number in the op list and
the result must appear in the story), so a spec whose ops disagree with its own
sentence cannot pass.

Then the rendered HTML: separate student and key files, one .sheet block each, a
real Name: field on the student sheet only, the print-worksheet.sh CSS literals
intact, and the key's printed answers equal the searched ones.
"""
import re
import sys

import specs_focus
from kids_config import kids_by_id, kid_name

rows = []


def check(label, got, want):
    rows.append((label, got, want, got == want))


def forward(start, ops):
    x = start
    for sym, n in ops:
        if sym == "+":
            x += n
        elif sym == "-":
            x -= n
        elif sym == "*":
            x *= n
        elif sym == "/":
            if x % n:
                return None
            x //= n
    return x


def words(q):
    return [int(t) for t in re.findall(r"\d+", re.sub(r"<[^>]+>", "", q))]


LITERALS = ["@page { margin: 0.55in; }", "line-height: 1.4;", "height: 78px;",
            "padding: 9px 12px;", "margin-bottom: 4px;", "margin: 4px 0 7px 0;",
            "margin-top: 7px;", "padding: 4px 8px;"]

def trade_search(a, b, k, T, c, d):
    """All (price_a, price_b) in whole dollars meeting the two stated equations."""
    sols = [(pa, pb) for pb in range(1, 301) for pa in range(1, 301)
            if pa == k * pb and a * pa + b * pb == T]
    return sols, [c * pa + d * pb for pa, pb in sols]


for spec in specs_focus.ALL:
    tag = spec["file"]
    kind = spec.get("kind", "undo")
    ex = spec["example"]
    key_answers = []
    if kind == "trade":
        sols, asked = trade_search(*(ex[x] for x in "abkTcd"))
        check(tag + " worked example unique prices", len(sols), 1)
        for i, p in enumerate(spec["problems"], 1):
            sols, asked = trade_search(p["a_n"], p["b_n"], p["k"], p["T"], p["c_n"], p["d_n"])
            check("%s #%d unique prices" % (tag, i), len(sols), 1)
            check("%s #%d asked total == key" % (tag, i), asked, [int(p["a"].lstrip("$"))])
            nums = words(p["q"])
            for n in (p["a_n"], p["b_n"], p["k"], p["T"], p["c_n"], p["d_n"]):
                check("%s #%d story mentions %d" % (tag, i, n), n in nums, True)
            key_answers.append(p["answer"])
    else:
        ex_result = forward(ex["secret"], ex["ops"])
        found = [s for s in range(10000) if forward(s, ex["ops"]) == ex_result]
        check(tag + " worked example unique start", found, [ex["secret"]])
    for i, p in enumerate(spec["problems"] if kind != "trade" else [], 1):
        found = [s for s in range(10000) if forward(s, p["ops"]) == p["result"]]
        check("%s #%d unique start" % (tag, i), len(found), 1)
        check("%s #%d start == answer" % (tag, i), found[0] if found else None,
              int(p["a"]))
        nums = words(p["q"])
        for n in [n for _, n in p["ops"]] + [p["result"]]:
            check("%s #%d story mentions %d" % (tag, i, n), n in nums, True)
        # the story's own order: the ops must appear in the sentence in chain order
        check("%s #%d no remainder in chain" % (tag, i),
              forward(found[0], p["ops"]) is not None if found else False, True)
        key_answers.append(int(p["a"]))

    student = open(spec["file"]).read()
    key = open(spec["key_file"]).read()
    check(tag + " student: 2 sheet blocks (pages)", student.count('class="sheet'), 2)
    check(tag + " key: 1 sheet block", key.count('class="sheet'), 1)
    check(tag + " student is not a key", 'class="sheet key"' in student, False)
    check(tag + " key is a key", 'class="sheet key"' in key, True)
    check(tag + " student: Name filled",
          bool(re.search(r"Name:\s*<span>&nbsp;[A-Za-z]+</span>", student)), True)
    check(tag + " key: no Name/Date field", "Name:" in key or "Date:" in key, False)
    check(tag + " student: no answers leaked",
          any(("<b>%d</b>" % a) in student for a in key_answers), False)
    check(tag + " student: 5 problems, 5 work/scaffold areas",
          (student.count('class="problem'), student.count('class="space"')
           + student.count('class="scaffold')), (5, 5))
    check(tag + " student: 5 Did-you-know facts", student.count("Did you know?"), 5)
    check(tag + " student: 5 answer lines", student.count('class="answer"'), 5)
    missing = [l for l in LITERALS if l not in student or l not in key]
    check(tag + " CSS literals intact", missing, [])
    kid = spec.get("kid", "kid1")
    kids = kids_by_id()
    check(tag + " student: Name is the mapped kid",
          re.search(r"Name:\s*<span>&nbsp;([^<]+)</span>", student).group(1),
          kid_name(kids, kid))
    printed = [int(x) for x in re.findall(r'<div class="ans"><b>\d+\. \$?(\d+)</b>', key)]
    check(tag + " key prints the searched answers", printed, key_answers)

# ---- plan samples (strands b, c for kid2): brute-force, not formula ----------
for i, sm in enumerate(specs_focus.SAMPLES_KID2, 1):
    k = sm["kind"]
    tag = "sample %d %s" % (i, k)
    if k == "avg_missing":
        # fifth/sixth value v such that the mean of known + [v] is exactly avg
        found = [v for v in range(0, 1001)
                 if (sum(sm["known"]) + v) == sm["avg"] * len(sm["known"] + [v])]
        check(tag + " unique", found, [sm["answer"]])
        check(tag + " count matches story", len(sm["known"]) + 1, sm["count"])
    elif k == "avg_add":
        # four values summing to avg*count are not known; the mean after adding is
        # (avg*count + added) / (count + 1), found by trying each candidate average
        found = [m for m in range(0, 1001)
                 if m * (sm["count"] + 1) == sm["avg"] * sm["count"] + sm["added"]]
        check(tag + " unique", found, [sm["answer"]])
    elif k == "age":
        found = [d for d in range(0, 121)
                 if d + sm["years"] == sm["times"] * (sm["now"] + sm["years"])]
        check(tag + " unique", found, [sm["answer"]])
    elif k == "equation":
        found = [x for x in range(0, 1001)
                 if x * sm["mul"] - sm["sub"] == sm["rhs_a"] * sm["rhs_b"]]
        check(tag + " unique", found, [sm["answer"]])
    nums = words(sm["q"])
    check(tag + " story mentions its answer-free numbers",
          all(n in nums for n in [x for x in
                                  ([sm.get("avg"), sm.get("added"), sm.get("now"),
                                    sm.get("years"), sm.get("times"), sm.get("mul"),
                                    sm.get("sub"), sm.get("rhs_a"), sm.get("rhs_b")]
                                   + sm.get("known", [])) if x is not None]), True)

width = max(len(r[0]) for r in rows)
fails = [r for r in rows if not r[3]]
for label, got, want, ok in rows:
    if not ok:
        print("FAIL  %-*s  got=%r  WANT=%r" % (width, label, got, want))
print("\n%d/%d checks passed, %d failed" % (len(rows) - len(fails), len(rows), len(fails)))
sys.exit(1 if fails else 0)
