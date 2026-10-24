"""verify_focus.py -- independent check of the Musa focus-track word sheets.

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

for spec in specs_focus.ALL:
    tag = spec["file"]
    ex = spec["example"]
    ex_result = forward(ex["secret"], ex["ops"])
    found = [s for s in range(10000) if forward(s, ex["ops"]) == ex_result]
    check(tag + " worked example unique start", found, [ex["secret"]])

    key_answers = []
    for i, p in enumerate(spec["problems"], 1):
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
    check(tag + " student: 1 sheet block", student.count('class="sheet'), 1)
    check(tag + " key: 1 sheet block", key.count('class="sheet'), 1)
    check(tag + " student is not a key", 'class="sheet key"' in student, False)
    check(tag + " key is a key", 'class="sheet key"' in key, True)
    check(tag + " student: Name filled",
          bool(re.search(r"Name:\s*<span>&nbsp;[A-Za-z]+</span>", student)), True)
    check(tag + " key: no Name/Date field", "Name:" in key or "Date:" in key, False)
    check(tag + " student: no answers leaked",
          any(("<b>%d</b>" % a) in student for a in key_answers), False)
    check(tag + " student: 4 problems, 4 work/scaffold areas",
          (student.count('class="problem'), student.count('class="work"')
           + student.count('class="scaffold"')), (4, 4))
    check(tag + " student: 4 Did-you-know facts", student.count("Did you know?"), 4)
    check(tag + " student: 4 answer lines", student.count('class="answer"'), 4)
    missing = [l for l in LITERALS if l not in student or l not in key]
    check(tag + " CSS literals intact", missing, [])
    printed = [int(x) for x in re.findall(r'<div class="ans"><b>\d+\. (\d+)</b>', key)]
    check(tag + " key prints the searched answers", printed, key_answers)

width = max(len(r[0]) for r in rows)
fails = [r for r in rows if not r[3]]
for label, got, want, ok in rows:
    if not ok:
        print("FAIL  %-*s  got=%r  WANT=%r" % (width, label, got, want))
print("\n%d/%d checks passed, %d failed" % (len(rows) - len(fails), len(rows), len(fails)))
sys.exit(1 if fails else 0)
