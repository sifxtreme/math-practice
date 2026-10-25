"""verify_fracmul.py -- independent check of the fraction-multiplication set (kid2).

    python3 build_fracmul.py && python3 verify_fracmul.py     # MUST exit 0

Recomputes EVERY answer with fractions.Fraction from the raw numbers in specs_fracmul.py
(it does not import build_fracmul, so a builder bug cannot hide itself), then reads the
RENDERED key HTML back and parses each printed answer into a Fraction. Asserts:
  * printed answer == recomputed answer, and is in simplest form (mixed number if improper)
  * the story text on the student sheet carries the same fractions as the raw numbers
  * no degenerate factors: no 0, no factor equal to 1, no fraction equal to 1, denominators 2-10
  * Part A covers unit x unit, proper x proper, whole x fraction, and some products simplify
  * student sheet: Name from kids.local.json, no answers leaked, print-worksheet.sh CSS literals
Prints a pass/fail table; exits nonzero on any failure.
"""
import re
import sys
from fractions import Fraction
from math import gcd

import specs_fracmul
from kids_config import kids_by_id, kid_name

rows = []


def check(label, got, want):
    rows.append((label, got, want, got == want))


LITERALS = ["@page { margin: 0.55in; }", "line-height: 1.4;", "height: 78px;",
            "padding: 9px 12px;", "margin-bottom: 4px;", "margin: 4px 0 7px 0;",
            "margin-top: 7px;", "padding: 4px 8px;"]

FR = r'<span class="fr"><span>(\d+)</span><span>(\d+)</span></span>'


def parse_answer(markup):
    """'2 <fr 2/3>' | '<fr 1/4>' | '18' -> (Fraction, shape). Reads the rendered markup."""
    m = re.fullmatch(r"\s*(?:(\d+)\s*)?(?:" + FR + r")?\s*", markup)
    if not m or not (m.group(1) or m.group(2)):
        raise ValueError("unparseable answer markup: %r" % markup)
    whole = int(m.group(1) or 0)
    if m.group(2):
        n, d = int(m.group(2)), int(m.group(3))
        return whole + Fraction(n, d), (whole > 0, n, d)
    return Fraction(whole), (False, whole, 1)


def simplest_ok(x, shape):
    """Simplest form: fraction part lowest terms and proper; no leftover improper fraction."""
    _, n, d = shape
    return gcd(n, d) == 1 and (d == 1 or n < d)


def frac(t):
    return Fraction(t[0], t[1])


def degenerate(factors):
    bad = []
    for n, d in factors:
        if n <= 0:
            bad.append("zero/negative %s/%s" % (n, d))
        if n == d:
            bad.append("equals 1: %s/%s" % (n, d))
        if d != 1 and not (2 <= d <= 10):
            bad.append("denominator out of 2-10: %s/%s" % (n, d))
        if d == 1 and n < 2:
            bad.append("whole factor %s" % n)
    return bad


spec = specs_fracmul.SPEC
student = open(spec["file"]).read()
key = open(spec["key_file"]).read()
kids = kids_by_id()

# ---- recompute from raw numbers ---------------------------------------------
want_a = [frac(p["f"][0]) * frac(p["f"][1]) for p in spec["part_a"]]


def word_answer(p):
    k = p["kind"]
    if k == "fof_left":
        return frac(p["p"]) - frac(p["p"]) * frac(p["q"])
    if k == "whole_chain":
        return Fraction(p["total"]) * frac(p["f1"]) * frac(p["f2"])
    if k == "area":
        return p["n"] * frac(p["l"]) * frac(p["w"])
    raise ValueError(k)


want_b = [word_answer(p) for p in spec["part_b"]]

# ---- the key's printed answers, parsed back from the rendered HTML -----------
printed = re.findall(r'<div class="ans"><b>(\d+)\. <em class="answer-val">(.*?)</em>', key)
check("key: answers printed (12 A + 3 B)", len(printed), len(want_a) + len(want_b))
parsed = []
for num, markup in printed:
    parsed.append(parse_answer(markup) + (markup,))
for i, want in enumerate(want_a, 1):
    got, shape, _ = parsed[i - 1]
    check("A%02d key == recomputed (%s)" % (i, want), got, want)
    check("A%02d simplest form" % i, simplest_ok(got, shape), True)
    check("A%02d degenerate factors" % i, degenerate(spec["part_a"][i - 1]["f"]), [])
for i, want in enumerate(want_b, 1):
    got, shape, _ = parsed[len(want_a) + i - 1]
    check("B%d key == recomputed (%s)" % (i, want), got, want)
    check("B%d simplest form" % i, simplest_ok(got, shape), True)

# ---- word-problem factors: no degenerate, and the story carries the raw numbers
for i, p in enumerate(spec["part_b"], 1):
    raw = [v for k, v in p.items() if isinstance(v, tuple)]
    check("B%d degenerate factors" % i, degenerate(raw), [])
    story = re.search(r'<div class="problem">\s*<span class="qnum">%d\.</span>\s*'
                      r'<div class="qtext">(.*?)</div>' % i, student, re.S).group(1)
    in_story = sorted((int(a), int(b)) for a, b in re.findall(FR, story))
    check("B%d story fractions == raw numbers" % i, in_story, sorted(raw))
    for k in ("total", "n"):
        if k in p:
            check("B%d story mentions %s=%d" % (i, k, p[k]),
                  bool(re.search(r"\b%d\b" % p[k], re.sub(r"<[^>]+>", " ", story))), True)
    # 2+ steps, themed: each story ends in a Did-you-know fact, and uses a Muslim name
    check("B%d has a fact" % i, bool(p.get("fact")), True)
check("B names (Muslim, not child's)", [re.match(r".*?\b(Amina|Omar|Idris)\b", p["story"]) is not None
                                        for p in spec["part_b"]], [True] * 3)

# ---- Part A is rendered from the raw numbers, in order, and covers the groups -
cells = re.findall(r'<div class="q"><span class="qn">(\d+)\.</span>(.*?) =</div>', student)
check("student: 12 Part A cells", len(cells), 12)
shown = []
for _, mk in cells:
    parts = mk.split(" &times; ")
    pair = []
    for part in parts:
        m = re.fullmatch(FR, part.strip())
        pair.append((int(m.group(1)), int(m.group(2))) if m else (int(part.strip()), 1))
    shown.append(pair)
check("student: Part A factors == raw numbers", shown, [list(p["f"]) for p in spec["part_a"]])
groups = {}
for p in spec["part_a"]:
    groups[p["group"]] = groups.get(p["group"], 0) + 1
check("Part A has unit/proper/whole problems", sorted(groups), ["proper", "unit", "whole"])
check("Part A unit problems really are 1/n x 1/m",
      all(p["f"][0][0] == 1 and p["f"][1][0] == 1 for p in spec["part_a"] if p["group"] == "unit"), True)
check("Part A whole problems have a whole factor",
      all(1 in (p["f"][0][1], p["f"][1][1]) for p in spec["part_a"] if p["group"] == "whole"), True)
check("Part A: >=3 products simplify (reduce)",
      sum(1 for p in spec["part_a"]
          if gcd(p["f"][0][0] * p["f"][1][0], p["f"][0][1] * p["f"][1][1]) > 1
          and p["group"] == "proper") >= 3, True)
check("Part A: >=3 mixed-number answers", sum(1 for x in want_a if x > 1 and x.denominator > 1) >= 3, True)

# ---- files -----------------------------------------------------------------
kid = spec.get("kid", "kid2")
check("student: 2 sheet blocks", student.count('class="sheet'), 2)
check("key: 2 sheet blocks", key.count('class="sheet'), 2)
check("student is not a key", 'class="sheet key"' in student, False)
check("key is a key", key.count('class="sheet key"'), 2)
check("student: Name is the mapped kid",
      re.findall(r"Name:\s*<span>&nbsp;([^<]+)</span>", student), [kid_name(kids, kid)] * 2)
check("key: no Name/Date field", "Name:" in key or "Date:" in key, False)
check("student: no answer-val markup", 'class="answer-val"' in student, False)
# an answer must not appear as a standalone printed number/fraction in the student sheet's
# problem area (the worked example is cut out first; it uses different numbers)
body = re.sub(r'<div class="walk">.*?</div>\s*</div>\s*</div>', "", student, flags=re.S)
body_text = re.sub(r"\s+", " ", body)
leaks = [mk for _, _, mk in parsed
         if re.search(r"(?<![\d>])" + re.escape(mk) + r"(?![\d<])", body_text)
         and not mk.isdigit()]
check("student: no fractional answer markup leaked", leaks, [])
missing = [l for l in LITERALS if l not in student or l not in key]
check("CSS literals intact", missing, [])
check("student: Part B has 3 boxed work areas + 3 answer lines + 3 facts",
      (student.count('class="space"'), student.count('class="answer"'),
       student.count("Did you know?")), (3, 3, 3))

# ---- table -----------------------------------------------------------------
width = max(len(r[0]) for r in rows)
for label, got, want, ok in rows:
    print("%s  %-*s  got=%s%s" % ("PASS" if ok else "FAIL", width, label, got,
                                  "" if ok else "  WANT=%s" % (want,)))
fails = [r for r in rows if not r[3]]
print("\n%d/%d checks passed, %d failed" % (len(rows) - len(fails), len(rows), len(fails)))
sys.exit(1 if fails else 0)
