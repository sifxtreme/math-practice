"""verify_fracmul.py -- independent check of the kid2 fraction packet (10 multiply + 10 add/subtract).

    python3 build_fracmul.py && python3 verify_fracmul.py     # MUST exit 0

Recomputes EVERY answer with fractions.Fraction from the raw numbers in specs_fracmul.py
(it does not import build_fracmul, so a builder bug cannot hide itself), then reads the
RENDERED key HTML back and parses each printed answer into a Fraction. Asserts:
  * exactly 20 problems: 10 multiply (7 bare + 3 word) and 10 add/subtract (7 bare + 3 word),
    numbered 1-20 in order on both the student sheet and the key
  * printed answer == recomputed answer, and is in simplest form (mixed number if improper)
  * the story text on the student sheet carries the same fractions as the raw numbers
  * multiply: no 0, no factor equal to 1, no fraction equal to 1, denominators 2-10
  * add/subtract: proper fractions only, denominators 2-12, no operand equal to 1 or 0,
    no negative or zero result, like/unlike groups really have equal/different bottoms
  * coverage (unit/proper/whole; simplifying and mixed-number answers; both + and -)
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


def degenerate_as(operands):
    """Add/subtract operands: proper fractions, denominators 2-12, never 0 or 1."""
    bad = []
    for n, d in operands:
        if n <= 0:
            bad.append("zero/negative %s/%s" % (n, d))
        if n >= d:
            bad.append("not a proper fraction: %s/%s" % (n, d))
        if not (2 <= d <= 12):
            bad.append("denominator out of 2-12: %s/%s" % (n, d))
    return bad


spec = specs_fracmul.SPEC
student = open(spec["file"]).read()
key = open(spec["key_file"]).read()
kids = kids_by_id()
MB, MW, AB, AW = spec["mul_bare"], spec["mul_word"], spec["as_bare"], spec["as_word"]

# ---- recompute from raw numbers ---------------------------------------------
want_mb = [frac(p["f"][0]) * frac(p["f"][1]) for p in MB]
want_ab = [frac(p["f"][0]) + frac(p["f"][1]) if p["op"] == "+" else frac(p["f"][0]) - frac(p["f"][1])
           for p in AB]


def word_answer(p):
    k = p["kind"]
    if k == "fof_left":
        return frac(p["p"]) - frac(p["p"]) * frac(p["q"])
    if k == "whole_chain":
        return Fraction(p["total"]) * frac(p["f1"]) * frac(p["f2"])
    if k == "area":
        return p["n"] * frac(p["l"]) * frac(p["w"])
    if k == "left_of_whole":
        return 1 - (frac(p["a"]) + frac(p["b"]))
    if k == "left_of_total":
        return frac(p["t"]) - frac(p["a"]) - frac(p["b"])
    if k == "add_then_sub":
        return frac(p["a"]) + frac(p["b"]) - frac(p["c"])
    raise ValueError(k)


want_mw = [word_answer(p) for p in MW]
want_aw = [word_answer(p) for p in AW]
# the packet order = problem numbers 1-20
want_all = want_mb + want_mw + want_ab + want_aw

# ---- counts: exactly 10 + 10 ------------------------------------------------
check("multiply problems", len(MB) + len(MW), 10)
check("add/subtract problems", len(AB) + len(AW), 10)
check("multiply: 7 bare + 3 word", (len(MB), len(MW)), (7, 3))
check("add/subtract: 7 bare + 3 word (2 like + 5 unlike bare)",
      (len(AB), len(AW), sum(p["group"] == "like" for p in AB), sum(p["group"] == "unlike" for p in AB)),
      (7, 3, 2, 5))

# ---- the key's printed answers, parsed back from the rendered HTML -----------
printed = re.findall(r'<div class="ans"><b>(\d+)\. <em class="answer-val">(.*?)</em>', key)
check("key: answers printed", len(printed), 20)
check("key: numbered 1-20 in order", [int(n) for n, _ in printed], list(range(1, 21)))
parsed = [parse_answer(markup) + (markup,) for _, markup in printed]
labels = (["M%02d" % i for i in range(1, len(MB) + 1)] + ["MW%d" % i for i in range(1, len(MW) + 1)]
          + ["S%02d" % i for i in range(1, len(AB) + 1)] + ["SW%d" % i for i in range(1, len(AW) + 1)])
for idx, want in enumerate(want_all):
    got, shape, _ = parsed[idx]
    check("#%d %s key == recomputed (%s)" % (idx + 1, labels[idx], want), got, want)
    check("#%d %s simplest form" % (idx + 1, labels[idx]), simplest_ok(got, shape), True)
for i, p in enumerate(MB, 1):
    check("M%02d degenerate factors" % i, degenerate(p["f"]), [])
for i, p in enumerate(AB, 1):
    check("S%02d degenerate operands" % i, degenerate_as(p["f"]), [])
    check("S%02d result > 0" % i, want_ab[i - 1] > 0, True)
    same = p["f"][0][1] == p["f"][1][1]
    check("S%02d group %s matches bottoms" % (i, p["group"]), same, p["group"] == "like")

# ---- word-problem factors: no degenerate, and the story carries the raw numbers
NAMES = ["Amina", "Omar", "Idris", "Zainab", "Hamza", "Kareem"]
for off, probs, deg, tag in ((len(MB) + 1, MW, degenerate, "MW"),
                             (len(MB) + len(MW) + len(AB) + 1, AW, degenerate_as, "SW")):
    for j, p in enumerate(probs):
        num = off + j
        raw = [v for k, v in p.items() if isinstance(v, tuple)]
        check("#%d %s degenerate factors" % (num, tag), deg(raw), [])
        story = re.search(r'<div class="problem">\s*<span class="qnum">%d\.</span>\s*'
                          r'<div class="qtext">(.*?)</div>' % num, student, re.S).group(1)
        in_story = sorted((int(a), int(b)) for a, b in re.findall(FR, story))
        check("#%d %s story fractions == raw numbers" % (num, tag), in_story, sorted(raw))
        for k in ("total", "n"):
            if k in p:
                check("#%d %s story mentions %s=%d" % (num, tag, k, p[k]),
                      bool(re.search(r"\b%d\b" % p[k], re.sub(r"<[^>]+>", " ", story))), True)
        check("#%d %s has a fact" % (num, tag), bool(p.get("fact")), True)
        check("#%d %s story names a character" % (num, tag),
              any(re.search(r"\b%s\b" % n, p["story"]) for n in NAMES), True)
check("add/subtract word results: intermediate steps positive (left_of_* kinds)",
      all(w > 0 for w in want_aw), True)

# ---- bare problems are rendered from the raw numbers, in order -----------------
cells = re.findall(r'<div class="q"><span class="qn">(\d+)\.</span>(.*?) =</div>', student)
check("student: 14 bare cells", len(cells), len(MB) + len(AB))
check("student: bare cells numbered 1-7 then 11-17",
      [int(n) for n, _ in cells], list(range(1, len(MB) + 1)) + list(range(11, 11 + len(AB))))


def operands(mk, sep):
    out = []
    for part in mk.split(sep):
        m = re.fullmatch(FR, part.strip())
        out.append((int(m.group(1)), int(m.group(2))) if m else (int(part.strip()), 1))
    return out


shown_m = [operands(mk, " &times; ") for _, mk in cells[:len(MB)]]
check("student: multiply factors == raw numbers", shown_m, [list(p["f"]) for p in MB])
shown_s = [(("+" if " + " in mk else "-"), operands(mk, " + " if " + " in mk else " &minus; "))
           for _, mk in cells[len(MB):]]
check("student: add/subtract operands and signs == raw numbers", shown_s,
      [(p["op"], list(p["f"])) for p in AB])

# ---- coverage ---------------------------------------------------------------
groups = {}
for p in MB:
    groups[p["group"]] = groups.get(p["group"], 0) + 1
check("multiply group counts (unit/proper/whole)", groups, {"unit": 2, "proper": 3, "whole": 2})
check("multiply unit problems really are 1/n x 1/m",
      all(p["f"][0][0] == 1 and p["f"][1][0] == 1 for p in MB if p["group"] == "unit"), True)
check("multiply whole problems have a whole factor",
      all(1 in (p["f"][0][1], p["f"][1][1]) for p in MB if p["group"] == "whole"), True)
check("multiply: >=2 proper products simplify",
      sum(1 for p in MB if p["group"] == "proper"
          and gcd(p["f"][0][0] * p["f"][1][0], p["f"][0][1] * p["f"][1][1]) > 1) >= 2, True)
check("multiply: >=2 whole x fraction answers are mixed numbers",
      sum(1 for p, x in zip(MB, want_mb) if p["group"] == "whole" and x > 1 and x.denominator > 1) >= 2,
      True)
check("add/subtract: both + and - used", sorted({p["op"] for p in AB}), ["+", "-"])
def as_reduces(p):
    """True when the sum/difference over the common denominator is not already in lowest terms."""
    (an, ad), (bn, bd) = p["f"]
    lcm = ad * bd // gcd(ad, bd)
    ra, rb = an * (lcm // ad), bn * (lcm // bd)
    return gcd(ra + rb if p["op"] == "+" else ra - rb, lcm) > 1


check("add/subtract: >=2 bare answers simplify (reduce)", sum(as_reduces(p) for p in AB) >= 2, True)
check("add/subtract: 1-2 bare sums are improper (mixed-number answers)",
      sum(1 for x in want_ab if x > 1) in (1, 2), True)

# ---- files -----------------------------------------------------------------
kid = spec.get("kid", "kid2")
check("student: 4 sheet blocks", student.count('class="sheet'), 4)
check("key: 4 sheet blocks", key.count('class="sheet'), 4)
check("student is not a key", 'class="sheet key"' in student, False)
check("key is a key", key.count('class="sheet key"'), 4)
check("student: Name is the mapped kid",
      re.findall(r"Name:\s*<span>&nbsp;([^<]+)</span>", student), [kid_name(kids, kid)] * 4)
check("key: no Name/Date field", "Name:" in key or "Date:" in key, False)
check("student: section headings Multiply + Add and subtract",
      (student.count("Multiply &mdash;"), student.count("Add and subtract &mdash;")), (2, 2))
check("student: no answer-val markup", 'class="answer-val"' in student, False)
# an answer must not appear as a standalone printed fraction in the student sheet's problem
# area (both worked examples are cut out first; they use different numbers)
body = re.sub(r'<div class="walk">.*?</div>\s*</div>\s*</div>', "", student, flags=re.S)
body_text = re.sub(r"\s+", " ", body)
# raw operands legitimately print on the sheet (e.g. 1/2 is an operand AND an answer), so compare
# COUNTS: a fraction answer may appear in the body only as often as the raw numbers put it there
raw_tuples = [t for p in MB + AB for t in p["f"]] + \
             [v for p in MW + AW for v in p.values() if isinstance(v, tuple)]
leaks = []
for _, _, mk in parsed:
    if mk.isdigit():
        continue
    m = re.fullmatch(r"\s*(\d+)?\s*" + FR + r"\s*", mk)
    whole, n, d = m.group(1), int(m.group(2)), int(m.group(3))
    expected = 0 if whole else raw_tuples.count((n, d))
    if body_text.count(mk.strip()) > expected:
        leaks.append(mk)
check("student: no fractional answer markup leaked", leaks, [])
check("student: both worked examples present", student.count('class="walk"'), 2)
missing = [l for l in LITERALS if l not in student or l not in key]
check("CSS literals intact", missing, [])
check("student: 6 word problems have boxed work areas + answer lines + facts",
      (student.count('class="space"'), student.count('class="answer"'),
       student.count("Did you know?")), (6, 6, 6))

# ---- table -----------------------------------------------------------------
width = max(len(r[0]) for r in rows)
for label, got, want, ok in rows:
    print("%s  %-*s  got=%s%s" % ("PASS" if ok else "FAIL", width, label, got,
                                  "" if ok else "  WANT=%s" % (want,)))
fails = [r for r in rows if not r[3]]
print("\n%d/%d checks passed, %d failed" % (len(rows) - len(fails), len(rows), len(fails)))
sys.exit(1 if fails else 0)
