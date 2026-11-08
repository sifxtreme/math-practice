"""build_yusuf_practice_1108.py -- Yusuf's (kid2) ONE-DAY 20-problem contest-style sheet (2026-11-08): student PDF + parent key PDF.

Asif (2026-11-08): "make sure today is medium-hard set of problems for what they need to prep for."  His Noetic sitting
is Wed 2026-11-11 (20 written problems, 45 min, no calculator, grade 4).  11-07's set was "easy enough" but he ran out
of time on the last 4, so the sheet carries the 45-minute frame and pace checkpoints (render helpers shared with
build_exam_practice_1108.py), no worked model, no type labels, mixed order, hardest last, one quick one inside #17-20.

  12 problems from the recent-exam types, harder than 11-07 (3 each; solver, verifier and wording imported from
     build_yusuf_practice.py): A events vs intervals (35/45-minute gaps, a remainder, crossing noon), B worst case
     (need 3/4/5 of a kind), C cut makes new edges (bigger squares), D letter addition (new shapes, one with a 0).
   8 problems from the Noetic grade 4 strands (private/PRACTICE-PLAN-2026.md, Yusuf focus track): trade it with
     "$d more" and with three items, averages (missing value; a newcomer, with a people-count trap), age at a later
     time and "years ago", working backwards, missing number.

    python3 build_yusuf_practice_1108.py <outdir>

Writes <outdir>/yusuf-practice-2026-11-08-{student,parent-key}.pdf (Chrome headless). Never prints.
Every answer is computed by solve() and re-derived by an independent brute-force verify(); the build fails on any
mismatch, a non-whole answer, or a count other than 20.
"""
import html
import os
import sys

import build_exam_practice_1108 as m   # shared render, pace checkpoints, undo/missing kinds
import build_yusuf_practice as by
from kids_config import kids_by_id, kid_name

KID = "kid2"
BASE = "yusuf-practice-2026-11-08"
T = by.T
SAME = "In this addition, the same letter is the same digit and different letters are different digits. What digit is %s?"


# ===================================================================== new kinds (Noetic grade 4 strands)
def solve_new(p):
    k = p["kind"]
    if k in ("undo", "missing"):
        return m.solve_new(p)
    if k == "trade_more":   # A = B + d;  ca*A + cb*B = T;  ask qa*A + qb*B
        A, B, d, ca, cb, Tt, qa, qb = p["A"], p["B"], p["d"], p["ca"], p["cb"], p["T"], p["qa"], p["qb"]
        b = (Tt - ca * d) // (ca + cb)
        a = b + d
        assert ca * a + cb * b == Tt
        ans = qa * a + qb * b
        return dict(ans=ans, lines=[
            "Let %s = price of one %s, %s = price of one %s. %s = %s + %d" % (A, p["an"], B, p["bn"], A, B, d),
            "%d%s + %d%s = %d" % (ca, A, cb, B, Tt),
            "Substitute: %d(%s + %d) + %d%s = %d" % (ca, B, d, cb, B, Tt),
            "%d%s + %d + %d%s = %d" % (ca, B, ca * d, cb, B, Tt),
            "%d%s + %d = %d, so %d%s = %d" % (ca + cb, B, ca * d, Tt, ca + cb, B, Tt - ca * d),
            "%s = %d ÷ %d = %d, and %s = %d + %d = %d" % (B, Tt - ca * d, ca + cb, b, A, b, d, a),
            "%d%s + %d%s = %d × %d + %d × %d = %d + %d = $%d" % (qa, A, qb, B, qa, a, qb, b, qa * a, qb * b, ans),
            "Check: %d × %d + %d × %d = %d + %d = $%d ✓" % (ca, a, cb, b, ca * a, cb * b, Tt)])
    if k == "trade3":       # J = r1 C, C = r2 S;  nj J + nc C + ns S = T;  ask qj J + qs S
        r1, r2, nj, nc, ns, Tt = p["r1"], p["r2"], p["nj"], p["nc"], p["ns"], p["T"]
        per_j, per_c = r1 * r2, r2
        units = nj * per_j + nc * per_c + ns
        s = Tt // units
        assert s * units == Tt
        c, j = r2 * s, r1 * r2 * s
        ans = p["qj"] * j + p["qs"] * s
        J, C, S = p["L"]
        return dict(ans=ans, lines=[
            "%s = %d%s and %s = %d%s, so %s = %d × %d%s = %d%s" % (J, r1, C, C, r2, S, J, r1, r2, S, per_j, S),
            "%d%s + %d%s + %d%s = %d" % (nj, J, nc, C, ns, S, Tt),
            "Trade everything for %s: %d × %d%s + %d × %d%s + %d%s = %d" % (S, nj, per_j, S, nc, per_c, S, ns, S, Tt),
            "%d%s + %d%s + %d%s = %d%s = %d" % (nj * per_j, S, nc * per_c, S, ns, S, units, S, Tt),
            "%s = %d ÷ %d = $%d; %s = %d × %d = $%d; %s = %d × %d = $%d" % (S, Tt, units, s, C, r2, s, c, J, r1, c, j),
            "%d%s + %d%s = %d + %d = $%d" % (p["qj"], J, p["qs"], S, p["qj"] * j, p["qs"] * s, ans),
            "Check: %d × %d + %d × %d + %d × %d = %d ✓" % (nj, j, nc, c, ns, s, nj * j + nc * c + ns * s)])
    if k == "avg_missing":
        n, avg, known = p["n"], p["avg"], p["known"]
        tot = n * avg
        ans = tot - sum(known)
        return dict(ans=ans, lines=[
            "Total of all %d = average × count = %d × %d = %d" % (n, avg, n, tot),
            "Known %d: %s = %d" % (len(known), " + ".join(map(str, known)), sum(known)),
            "Missing one: %d − %d = %d" % (tot, sum(known), ans),
            "Check: (%d + %d) ÷ %d = %d ÷ %d = %d ✓" % (sum(known), ans, n, tot, n, avg)])
    if k == "avg_add":
        n, avg, new = p["n"], p["avg"], p["new"]
        tot = n * avg
        ans = (tot + new) // (n + 1)
        assert ans * (n + 1) == tot + new
        return dict(ans=ans, lines=[
            "People at the start: %s = %d (count %s too)" % (p["who"], n, p["lead"]),
            "Total at the start: %d × %d = %d" % (n, avg, tot),
            "%s joins: total %d + %d = %d, people %d + 1 = %d" % (p["newname"], tot, new, tot + new, n, n + 1),
            "New average: %d ÷ %d = %d" % (tot + new, n + 1, ans),
            "Check: %d × %d = %d ✓" % (ans, n + 1, tot + new)])
    if k == "age_later":
        a, y, k_ = p["a"], p["y"], p["k"]
        later = (a + y) * k_
        ans = later - y
        return dict(ans=ans, lines=[
            "Draw the bars at the LATER time: in %d years %s is %d + %d = %d" % (y, p["kid"], a, y, a + y),
            "Then %s is %d × %d = %d" % (p["adult"], k_, a + y, later),
            "Now is %d years earlier: %d − %d = %d" % (y, later, y, ans),
            "Check: in %d years, %d + %d = %d and %d = %d × %d ✓" % (y, ans, y, later, later, k_, a + y)])
    if k == "age_ago":
        P, C, k_ = p["P"], p["C"], p["k"]
        y = (k_ * C - P) // (k_ - 1)
        assert P - y == k_ * (C - y)
        return dict(ans=y, lines=[
            "Let y = years ago. Then %s was %d − y and %s was %d − y." % (p["adult"], P, p["kid"], C),
            "%d − y = %d × (%d − y)" % (P, k_, C),
            "%d − y = %d − %dy" % (P, k_ * C, k_),
            "Add %dy to both sides: %d + %dy = %d, so %dy = %d − %d = %d" % (k_, P, k_ - 1, k_ * C, k_ - 1, k_ * C, P, k_ * C - P),
            "y = %d ÷ %d = %d" % (k_ * C - P, k_ - 1, y),
            "Check: %d years ago %s was %d and %s was %d; %d = %d × %d ✓" % (
                y, p["adult"], P - y, p["kid"], C - y, P - y, k_, C - y)])
    raise ValueError(k)


def verify_new(p, s):
    k = p["kind"]
    if k in ("undo", "missing"):
        return m.verify_new(p, s)
    if k == "trade_more":
        hits = [p["qa"] * (b + p["d"]) + p["qb"] * b for b in range(1, p["T"] + 1)
                if p["ca"] * (b + p["d"]) + p["cb"] * b == p["T"]]
    elif k == "trade3":
        hits = [p["qj"] * j + p["qs"] * sp for sp in range(1, p["T"] + 1) for c in range(1, p["T"] + 1)
                for j in range(1, p["T"] + 1)
                if c == p["r2"] * sp and j == p["r1"] * c and p["nj"] * j + p["nc"] * c + p["ns"] * sp == p["T"]]
    elif k == "avg_missing":
        hits = [x for x in range(0, 201) if sum(p["known"] + [x]) == sum([p["avg"]] * p["n"])]
    elif k == "avg_add":
        scores = [p["avg"]] * p["n"] + [p["new"]]          # any start list with that average has that total
        hits = [a for a in range(0, 1001) if sum([a] * len(scores)) == sum(scores)]
    elif k == "age_later":
        hits = [f for f in range(0, 121) if f + p["y"] == p["k"] * (p["a"] + p["y"])]
    elif k == "age_ago":
        hits = [y for y in range(0, p["C"] + 1) if p["P"] - y == p["k"] * (p["C"] - y)]
    else:
        raise ValueError(k)
    return hits == [s["ans"]]


NEW_KINDS = ("undo", "missing", "trade_more", "trade3", "avg_missing", "avg_add", "age_later", "age_ago")


# ===================================================================== the 20 problems
BUS_Q = "A %s leaves the %s at %%s and then every %d minutes. How many %s leave the %s from %%s up to %%s?"
BACK_OPS = [("÷", 2), ("−", 6), ("+", 10)]
MISS_OPS = [("+", 8), ("×", 3)]

PROBS = [
    # ---- medium (1-8)
    dict(kind="posts", length=84, gap=7, unit="lanterns", tier="medium", why="bigger numbers; posts = gaps + 1",
         q="A straight walkway is 84 meters long. Lanterns stand 7 meters apart, with a lantern at <b>both</b> ends of the walkway. How many lanterns are there?"),
    dict(kind="worst", colors=["red", "blue", "green", "yellow", "white", "purple"], each=8, need=3, thing="beads",
         unit="beads", tier="medium", why="six colors and need 3, not 2",
         q="A box holds 8 red, 8 blue, 8 green, 8 yellow, 8 white and 8 purple beads, and nothing else. Without looking, what is the <b>fewest</b> beads you must take out to be <b>sure</b> that at least 3 of them are the same color?"),
    dict(kind="missing", ops=MISS_OPS, rhs=(5, 12, 6), unit="", tier="medium", why="bracket on the left; undo in reverse",
         q="What number goes in the box?  <b>%s = 5 × 12 + 6</b>" % m.box_expr(MISS_OPS)),
    dict(kind="avg_missing", n=5, avg=88, known=[92, 79, 95, 84], unit="points", tier="medium",
         why="total = average × count, then take the known total off",
         q="Zubair took 5 quizzes. His average score was 88. Four of his scores were 92, 79, 95 and 84. What was his fifth score?"),
    dict(kind="cut", side=14, given=40, unit="inches", tier="medium", why="bigger square; the cut edge counts twice",
         q="A square tile has a perimeter of 56 inches. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 40 inches. What is the perimeter of the other rectangle?"),
    dict(kind="bus", first=T(6, 50), step=35, end=T(10, 30), what="boat", plural="boats", tier="medium",
         why="35-minute gaps and a remainder of 10 minutes that is NOT an extra boat",
         q=BUS_Q % ("boat", "pier", 35, "boats", "pier")),
    dict(kind="crypt", a="GB", b="B6", s="1GG", ask="G", unit="", tier="medium", why="new shape: the letters swap places",
         q=SAME % "G"),
    dict(kind="trade_more", A="n", B="p", an="notebook", bn="pen", d=4, ca=3, cb=2, T=37, qa=2, qb=5, unit="dollars",
         tier="medium", why="'$4 more' relation; asks a different total",
         q="At a school store, a notebook costs $4 more than a pen. 3 notebooks and 2 pens cost $37 in all. "
           "How much do 2 notebooks and 5 pens cost?"),
    # ---- medium-hard (9-15)
    dict(kind="worst", colors=["red", "blue", "green", "black", "white"], each=10, need=4, thing="caps",
         unit="caps", tier="hard", why="need 4 of a kind with 5 colors: 5 × 3 + 1",
         q="A bin holds 10 red, 10 blue, 10 green, 10 black and 10 white caps, and nothing else. Without looking, what is the <b>fewest</b> caps you must take out to be <b>sure</b> that at least 4 of them are the same color?"),
    dict(kind="age_later", a=8, y=4, k=3, kid="Ilyas", adult="his father", unit="years old", tier="hard",
         why="the 'times as old' is at the later time, then go back",
         q="Ilyas is 8 years old. In 4 years, his father will be 3 times as old as Ilyas will be then. How old is his father now?"),
    dict(kind="bus", first=T(11, 15), step=45, end=T(14, 45), what="ring", plural="rings", tier="hard",
         why="crosses noon; 45-minute gaps; a 30-minute remainder",
         q="A tower clock chimes at %s and then every 45 minutes. How many times does it chime from %s up to %s?", unit="chimes"),
    dict(kind="undo", ops=BACK_OPS, result=25, unit="dollars", tier="hard",
         why="working backwards through half, minus, plus; undo of 'half' is × 2",
         q="Hamid had some money. He spent half of it on a book. Then he spent $6 on lunch. Then his aunt gave him $10. "
           "Now he has $25. How much money did Hamid have at the start?"),
    dict(kind="cut", side=15, given=44, unit="centimeters", tier="hard", why="odd side; x = 22 − 15",
         q="A square card has a perimeter of 60 centimeters. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 44 centimeters. What is the perimeter of the other rectangle?"),
    dict(kind="crypt", a="H7", b="WH", s="1WW", ask="W", unit="", tier="hard", why="a letter in both the tens and the ones place",
         q=SAME % "W"),
    dict(kind="avg_add", n=4, avg=15, new=30, who="Maryam + 3 friends", lead="Maryam", newname="Noura", unit="stickers",
         tier="hard", why="'Maryam and her 3 friends' is 4 people; recompute the total, not the average",
         q="Maryam and her 3 friends have an average of 15 stickers each. Then Noura joins them with 30 stickers. "
           "What is the new average number of stickers per person?"),
    # ---- hardest (16-20), one quick one at 18
    dict(kind="trade3", r1=3, r2=2, nj=2, nc=4, ns=6, T=52, qj=1, qs=1, L=("j", "c", "s"), unit="dollars", tier="hard",
         why="three items, two trades in a chain",
         q="At a kitchen shop, 1 jug costs the same as 3 cups, and 1 cup costs the same as 2 spoons. "
           "2 jugs, 4 cups and 6 spoons cost $52 in all. How much do 1 jug and 1 spoon cost together?"),
    dict(kind="age_ago", P=34, C=10, k=4, adult="Rukhsana", kid="Safa", unit="years ago", tier="hard",
         why="'years ago' with 'times as old'; both ages move",
         q="Today Rukhsana is 34 years old and her daughter Safa is 10. How many years ago was Rukhsana exactly 4 times as old as Safa?"),
    dict(kind="worst", colors=["red", "blue", "green", "orange"], each=9, need=5, thing="balloons", unit="balloons",
         tier="quick", why="QUICK one placed late on purpose: 4 × 4 + 1",
         q="A bag holds 9 red, 9 blue, 9 green and 9 orange balloons, and nothing else. Without looking, what is the <b>fewest</b> balloons you must take out to be <b>sure</b> that at least 5 of them are the same color?"),
    dict(kind="cut", side=20, given=56, unit="inches", tier="hard", why="largest square; two-step algebra for x",
         q="A square poster has a perimeter of 80 inches. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 56 inches. What is the perimeter of the other rectangle?"),
    dict(kind="crypt", a="FF", b="6R", s="1RF", ask="F", unit="", tier="hard", why="one letter is 0; the carry decides it",
         q=SAME % "F"),
]
assert len(PROBS) == 20
for _i, _p in enumerate(PROBS, 1):
    _p["id"] = 100 + _i     # by.crypt_lines hand-writes ids 7 and 8 (11-06); keep clear of them
    _p.setdefault("t", "X")

WATCH = {
    1: "Answers 12 (84 ÷ 7, gaps only). Look for '+ 1 for the first lantern'.",
    2: "Worst case line written out: 6 colors × 2 each = 12, then + 1. Answer 7 means he used the 'need 2' rule.",
    3: "His known slip: skipping steps. Expect: right side 66, undo × 3 (22), undo + 8 (14). 66 − 8 first is the wrong order.",
    4: "Total line 5 × 88 = 440 must be on the page. Averaging the four known scores is the wrong idea.",
    5: "Answers 16 (56 − 40) if he forgets the two new cut edges. Look for x = 6 and the check line.",
    6: "Answers 6 (gaps only) or 8 (counts the leftover 10 minutes as a boat). The remainder is not an event.",
    7: "Must add the real numbers back: 59 + 96 = 155. An answer with no check is UNSHOWN.",
    8: "Asif's format: letters, substitute, one step per line. Skipping to 'p = 5' with no lines is UNSHOWN.",
    9: "5 × 3 + 1 = 16. Answer 21 (5 × 4 + 1) means he forgot the worst case stops one short.",
    10: "Answers 24 (3 × 8) or 36 if he applies 'times' now, or skips going back 4 years. (Same 'times as many' direction slip as Oct 12.)",
    11: "Times cross noon: 11:15 AM to 2:45 PM is 210 minutes. Answer 4 means he forgot the first chime.",
    12: "Undo order: + 10 first (25 − 10 = 15), then + 6 (21), then the half is undone by × 2 (42). Halving instead of doubling gives 10.5.",
    13: "x = 22 − 15 = 7. Answer 16 (60 − 44) skips the new edges.",
    14: "Units column: 7 + H ends in W, and tens H + W + carry = 1W. Check line 97 + 69 = 166.",
    15: "His Oct 12 miss (forgot Jackson): count 4 people, not 3. Dividing 75 by 4 or 90 by 4 is the people-count slip.",
    16: "Two trades in a chain: j = 3c = 6s. Look for everything written in spoons (26s = 52) before any price.",
    17: "Trying 34 ÷ 10 or 34 ÷ 4 = 8.5 is the wrong idea. Both ages go back by the same y. A table of y = 1, 2, 3 is fine as his lines.",
    18: "Quick one placed late on purpose. Blank here means time ran out on 16-17.",
    19: "x = 28 − 20 = 8, other rectangle 20 by 12. Answer 24 (80 − 56) skips the new edges.",
    20: "R = 0 is allowed (it is not a leading digit). Check line 44 + 60 = 104.",
}


def solve(p):
    return solve_new(p) if p["kind"] in NEW_KINDS else by.solve(p)


def verify(p, s):
    return verify_new(p, s) if p["kind"] in NEW_KINDS else by.verify(p, s)


def statement(p):
    return p["q"] if p["kind"] in NEW_KINDS else by.statement(p)


def unit(p):
    return p["unit"] if "unit" in p else by.unit(p)


def art(p):
    if p["kind"] != "crypt":
        return ""
    return '<div class="art">&nbsp;&nbsp;%s<br>+ %s<br><span style="border-top:2px solid #000">%s</span></div>' % (p["a"], p["b"], p["s"])


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    if len(PROBS) != 20:
        raise SystemExit("need 20 problems, have %d" % len(PROBS))
    solved = []
    for i, p in enumerate(PROBS, 1):
        s = solve(p)
        if not verify(p, s):
            print("VERIFY FAILED %d: %r -> %r" % (i, p, s["ans"]), file=sys.stderr)
            return 1
        m.check_whole(i, s)
        solved.append(s)
    name = kid_name(kids_by_id(), KID)
    top = "%s - contest practice %s" % (name, m.DATE)
    title = "Contest practice: 20 problems"
    items = [(i, statement(p), unit(p), p["tier"], art(p)) for i, p in enumerate(PROBS, 1)]
    rows = []
    for i, (p, s) in enumerate(zip(PROBS, solved), 1):
        text = statement(p) + ((" &nbsp;<tt>%s + %s = %s</tt>" % (p["a"], p["b"], p["s"])) if p["kind"] == "crypt" else "")
        rows.append((i, text, s["lines"], s["ans"], unit(p), p["tier"], p["why"], WATCH[i]))
    method = (m.METHOD.replace("club problems by trying every possible number of girls; ", "")
              + " Boat and chime counts were found by stepping forward one gap at a time; lanterns by listing every multiple of the gap; "
                "worst-case problems by trying every mix of colors; cut problems by trying every cut position; letter sums by trying "
                "every digit assignment (exactly one fit each); trade, average and age problems by trying every whole price, score or age.")
    pdfs = [m.to_pdf(m.student_doc(name, title, items, top), out, BASE, "student"),
            m.to_pdf(m.key_doc(name, title, rows, method, top), out, BASE, "parent-key")]
    print("ok: %d problems verified a second way; answers: %s" % (len(PROBS), [s["ans"] for s in solved]))
    print("\n".join(pdfs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
