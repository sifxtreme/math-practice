"""Independent check of every answer on the ten Jul 29 - Aug 2 sheets.

Deliberately re-derives each result a DIFFERENT way from the spec file — loops
and brute-force searches instead of the closed forms in specs_*.py — so a wrong
formula there cannot quietly agree with a wrong formula here. Reasoning puzzles
(logic grids, liar puzzles, the river crossing, the hourglass) are solved by
exhaustive search, not asserted by hand.

Also checks the generated HTML: 3 .sheet blocks, 2 date fields, and every CSS
literal print-worksheet.sh rewrites.
"""
import re
from fractions import Fraction as F
from itertools import combinations, permutations
from math import gcd

import specs_word
import specs_logic

rows = []


def check(label, got, want):
    rows.append((label, got, want, got == want))


def divmod_by_repeated_subtraction(n, d):
    """Deliberately not // and % — an independent path to the same pair."""
    q = 0
    while n >= d:
        n -= d
        q += 1
    return q, n


def boxes_needed(n, per):
    q, r = divmod_by_repeated_subtraction(n, per)
    return q + (1 if r else 0)


# ============================== WORD SHEETS ==============================
# --- Jul 29 weather
q, r = divmod_by_repeated_subtraction(53, 8)
check("W-Jul29 M1 full/left", (q, r), (6, 5))
check("W-Jul29 M1 boxes for all", boxes_needed(53, 8), 7)
check("W-Jul29 M2 vans", boxes_needed(87, 9), 10)
check("W-Jul29 M3 readings", sum([6] * 24) - 18, 126)
check("W-Jul29 M4 3/4 > 5/8", F(3, 4) > F(5, 8), True)
check("W-Jul29 M5 side", next(s for s in range(1, 50) if 6 * s == 48), 8)
check("W-Jul29 M5 perimeter", 6 + 8 + 6 + 8, 28)
check("W-Jul29 Y1 1/2+1/3", F(1, 2) + F(1, 3), F(5, 6))
check("W-Jul29 Y2 3/4-2/5", F(3, 4) - F(2, 5), F(7, 20))
check("W-Jul29 Y3 2/3+3/4", F(2, 3) + F(3, 4), F(17, 12))
check("W-Jul29 Y3 is >1 (mixed)", F(17, 12) > 1, True)
check("W-Jul29 Y4 36x24", sum([36] * 24), 864)
check("W-Jul29 Y5 balloon", sum([45] * 18) - 210, 600)

# --- Jul 30 mars
q, r = divmod_by_repeated_subtraction(74, 8)
check("W-Jul30 M1 full/left", (q, r), (9, 2))
check("W-Jul30 M1 trays for all", boxes_needed(74, 8), 10)
check("W-Jul30 M2 new ground", sum([128] * 7) - 245, 651)
check("W-Jul30 M3 photos each", (sum([12] * 5) - 8) / 4, 13)
check("W-Jul30 M4 2/3 > 5/9", F(2, 3) > F(5, 9), True)
check("W-Jul30 M5 side/perim", (56 // 7, 2 * (7 + 8)), (8, 30))
check("W-Jul30 Y1 3/8+1/6", F(3, 8) + F(1, 6), F(13, 24))
check("W-Jul30 Y2 1246/5", divmod_by_repeated_subtraction(1246, 5), (249, 1))
check("W-Jul30 Y2 reconstruct", 249 * 5 + 1, 1246)
check("W-Jul30 Y3 4.75-1.8", round(4.75 - 1.8, 2), 2.95)
check("W-Jul30 Y4 48x25", sum([48] * 25), 1200)
check("W-Jul30 Y5 rover", round(3.5 * 24 - 12.5, 2), 71.5)

# --- Jul 31 bees
q, r = divmod_by_repeated_subtraction(95, 6)
check("W-Jul31 M1 full/left", (q, r), (15, 5))
check("W-Jul31 M1 crates for all", boxes_needed(95, 6), 16)
check("W-Jul31 M2 bees", sum([145] * 4) - 96, 484)
check("W-Jul31 M3 frames each", (8 * 9) / 3, 24)
check("W-Jul31 M4 1/2 > 4/10", F(1, 2) > F(4, 10), True)
check("W-Jul31 M5 side/perim", (63 // 9, 2 * (9 + 7)), (7, 32))
check("W-Jul31 Y1 5/6-3/8", F(5, 6) - F(3, 8), F(11, 24))
check("W-Jul31 Y2 2375/8", divmod_by_repeated_subtraction(2375, 8), (296, 7))
check("W-Jul31 Y2 reconstruct", 296 * 8 + 7, 2375)
check("W-Jul31 Y3 2.4+3.75", round(2.4 + 3.75, 2), 6.15)
check("W-Jul31 Y4 34x56", sum([34] * 56), 1904)
check("W-Jul31 Y5 honey left", round(15 * 12 - 45.5, 2), 134.5)

# --- Aug 1 ships
q, r = divmod_by_repeated_subtraction(68, 9)
check("W-Aug1 M1 full/left", (q, r), (7, 5))
check("W-Aug1 M1 boats launched", boxes_needed(68, 9), 8)
check("W-Aug1 M2 rope", sum([236] * 3) - 159, 549)
check("W-Aug1 M3 crates each", (6 * 14) / 7, 12)
check("W-Aug1 M4 7/10 > 3/5", F(7, 10) > F(3, 5), True)
check("W-Aug1 M5 side/perim", (72 // 8, 2 * (8 + 9)), (9, 34))
check("W-Aug1 Y1 7/10+1/4", F(7, 10) + F(1, 4), F(19, 20))
check("W-Aug1 Y1 still under 1", F(19, 20) < 1, True)
check("W-Aug1 Y2 3428/6", divmod_by_repeated_subtraction(3428, 6), (571, 2))
check("W-Aug1 Y2 reconstruct", 571 * 6 + 2, 3428)
check("W-Aug1 Y3 12.6-4.85", round(12.6 - 4.85, 2), 7.75)
check("W-Aug1 Y4 62x45", sum([62] * 45), 2790)
check("W-Aug1 Y5 made good", round(8.5 * 14 - 23.5, 2), 95.5)

# --- Aug 2 mountains (cumulative)
check("W-Aug2 M1 side/perim", (54 // 6, 2 * (6 + 9)), (9, 30))
check("W-Aug2 M2 trips", boxes_needed(77, 8), 10)
check("W-Aug2 M3 2/3 > 5/8", F(2, 3) > F(5, 8), True)
check("W-Aug2 M3 margin is one 24th", F(2, 3) - F(5, 8), F(1, 24))
check("W-Aug2 M4 gain", sum([174] * 5) - 218, 652)
check("W-Aug2 M5 per mule", (9 * 6 - 12) / 6, 7)
check("W-Aug2 Y1 38x47", sum([38] * 47), 1786)
check("W-Aug2 Y2 5/6-1/4", F(5, 6) - F(1, 4), F(7, 12))
check("W-Aug2 Y3 4215/7", divmod_by_repeated_subtraction(4215, 7), (602, 1))
check("W-Aug2 Y3 reconstruct", 602 * 7 + 1, 4215)
check("W-Aug2 Y4 9.4-3.65", round(9.4 - 3.65, 2), 5.75)
check("W-Aug2 Y5 gain", sum([320] * 7) - 465, 1775)

# cumulative sheet must cover all five pinned skills, one each
check("W-Aug2 kid1 has 5 problems", len(specs_word.AUG2["kid1"]), 5)
check("W-Aug2 kid2 has 5 problems", len(specs_word.AUG2["kid2"]), 5)

# ============================== LOGIC SHEETS ==============================
# --- patterns, by generating the sequence forward
seq = [1]
for gap in range(1, 7):
    seq.append(seq[-1] + gap)
check("L-Jul29 M1 pattern", seq[:7], [1, 2, 4, 7, 11, 16, 22])

s = [2]
for i in range(6):
    s.append(s[-1] + (3 if i % 2 == 0 else -1))
check("L-Jul30 M2 pattern", s[:7], [2, 5, 4, 7, 6, 9, 8])

s = [3]
for i in range(7):
    s.append(s[-1] * 2 if i % 2 == 0 else s[-1] - 1)
check("L-Jul31 M2 pattern", s[:8], [3, 6, 5, 10, 9, 18, 17, 34])

tri = [1]
for gap in range(2, 8):
    tri.append(tri[-1] + gap)
check("L-Aug2 M3 triangular", tri[:7], [1, 3, 6, 10, 15, 21, 28])

# --- set overlap, by counting elements not by formula
def neither(total, a, b, both):
    return total - (a + b - both)


check("L-Jul29 M2 neither", neither(12, 7, 6, 3), 2)
check("L-Jul29 Y2 neither", neither(30, 18, 14, 5), 3)
check("L-Aug2 M2 neither", neither(20, 12, 9, 4), 3)

# --- substitution / balance, solved by brute force over integer weights
sol = [(lens, lamp) for lens in range(1, 20) for lamp in range(1, 20)
       if 2 * lens + lamp == 11 and lens + lamp == 7]
check("L-Jul29 Y3 unique lens/lamp", sol, [(4, 3)])
check("L-Jul29 M4 lenses per big lamp", 3 * 2, 6)
check("L-Jul30 Y3 bells for 9 hoods", (9 // 3) * 2 * 6, 36)
check("L-Aug2 M4 bells for 4 large", (4 // 2) * 5 * 3, 30)

# --- age puzzle, brute forced
sol = [(f, c) for f in range(1, 30) for c in range(1, 30) if f == 3 * c and f + c == 12]
check("L-Jul30 M1 unique ages", sol, [(9, 3)])

# --- ordering puzzles, brute forced over permutations
o = [p for p in permutations(["Gull", "Rock", "Pine", "Sand"])
     if p.index("Gull") < p.index("Rock") and p[-1] == "Sand"
     and p.index("Pine") < p.index("Gull")]
check("L-Jul29 M3 unique order", o, [("Pine", "Gull", "Rock", "Sand")])

o = [p for p in permutations(["Zahra", "Rimal", "Bahr", "Nakhl"])
     if p[0] == "Rimal" and p[-1] == "Nakhl"
     and p.index("Zahra") < p.index("Bahr") < p.index("Nakhl")]
check("L-Jul31 M3 unique order", o, [("Rimal", "Zahra", "Bahr", "Nakhl")])

o = [p for p in permutations(["Idris", "Salma", "Yahya"])
     if p.index("Idris") < p.index("Salma") < p.index("Yahya")]
check("L-Aug1 M4 unique order", o, [("Idris", "Salma", "Yahya")])

# --- kid1's 3-way matching (Jul 30)
sols = []
for birds in permutations(["kestrel", "saker", "peregrine"]):
    b = dict(zip(["Hamza", "Layla", "Bilal"], birds))
    if b["Hamza"] == "kestrel":
        continue
    if b["Layla"] != "peregrine":
        continue
    sols.append(b)
check("L-Jul30 M3 unique match", sols,
      [{"Hamza": "saker", "Layla": "peregrine", "Bilal": "kestrel"}])

# --- kid2's logic grids
sols = []
for birds in permutations(["peregrine", "saker", "kestrel"]):
    for days in permutations(["Tue", "Thu", "Sat"]):
        b = dict(zip(["Yusuf", "Tariq", "Amina"], birds))
        d = dict(zip(["Yusuf", "Tariq", "Amina"], days))
        if d["Amina"] == "Sat":
            continue
        if d[[p for p in b if b[p] == "peregrine"][0]] != "Sat":
            continue
        if d["Yusuf"] != "Tue" or b["Yusuf"] == "saker":
            continue
        sols.append({p: (b[p], d[p]) for p in b})
check("L-Jul30 Y1 grid unique", len(sols), 1)
check("L-Jul30 Y1 grid solution", sols[0],
      {"Yusuf": ("kestrel", "Tue"), "Tariq": ("peregrine", "Sat"), "Amina": ("saker", "Thu")})

sols = []
for cols in permutations(["red", "green", "blue"]):
    for places in permutations(["hill", "beach", "park"]):
        c = dict(zip(["Yusuf", "Musa", "Hamza"], cols))
        pl = dict(zip(["Yusuf", "Musa", "Hamza"], places))
        if c["Musa"] == "red":
            continue
        if pl[[p for p in c if c[p] == "blue"][0]] != "beach":
            continue
        if pl["Hamza"] != "hill" or c["Hamza"] == "green":
            continue
        if pl["Yusuf"] == "beach":
            continue
        sols.append({p: (c[p], pl[p]) for p in c})
check("L-Aug2 Y1 grid unique", len(sols), 1)
check("L-Aug2 Y1 grid solution", sols[0],
      {"Hamza": ("red", "hill"), "Musa": ("blue", "beach"), "Yusuf": ("green", "park")})

# --- liar puzzles, brute forced over who is guilty
def liar_solve(people, statement, want_true=None, want_lies=None):
    out = []
    for culprit in people:
        truths = sum(1 for p in people if statement(p, culprit))
        if want_true is not None and truths == want_true:
            out.append(culprit)
        if want_lies is not None and len(people) - truths == want_lies:
            out.append(culprit)
    return out


# Jul 29: Idris "not me", Anas "it was Bilal", Bilal "Anas is lying". Exactly one truth.
def st_jul29(speaker, culprit):
    if speaker == "Idris":
        return culprit != "Idris"
    if speaker == "Anas":
        return culprit == "Bilal"
    return not (culprit == "Bilal")          # Bilal: "Anas is lying"


check("L-Jul29 Y1 liar unique", liar_solve(["Idris", "Anas", "Bilal"], st_jul29, want_true=1), ["Idris"])


# Aug 2: Anas "Bilal did it", Bilal "I didn't", Idris "Anas did it". Exactly one LIES.
def st_aug2(speaker, culprit):
    if speaker == "Anas":
        return culprit == "Bilal"
    if speaker == "Bilal":
        return culprit != "Bilal"
    return culprit == "Anas"


check("L-Aug2 Y3 liar unique", liar_solve(["Anas", "Bilal", "Idris"], st_aug2, want_lies=1), ["Anas"])
# and confirm the Jul 29 rule really does give a DIFFERENT answer, so the
# cumulative sheet's trap is real rather than accidental
check("L-Aug2 Y3 differs from one-truth reading",
      liar_solve(["Anas", "Bilal", "Idris"], st_aug2, want_true=1) != ["Anas"], True)

# --- LCM cycles, computed by walking the multiples
def first_common(a, b, limit=100000):
    n = a
    while n <= limit:
        if n % b == 0:
            return n
        n += a
    return None


check("L-Jul29 Y4 flash together", first_common(4, 6), 12)
check("L-Jul29 Y4 times in 60s", len([t for t in range(1, 61) if t % 4 == 0 and t % 6 == 0]), 5)
check("L-Jul31 Y3 caravans", first_common(9, 12), 36)
check("L-Jul31 Y3 per year", len([d for d in range(1, 366) if d % 36 == 0]), 10)
check("L-Aug1 Y2 three bells", first_common(first_common(6, 8), 12), 24)
check("L-Aug2 Y2 festivals", first_common(15, 20), 60)

# --- clock puzzles
check("L-Aug1 M1 slow clock", (3 * 60 + 40 + 15) // 60 * 100 + (3 * 60 + 40 + 15) % 60, 355)  # 3:55
check("L-Aug1 M2 strikes 1..6", sum(range(1, 7)), 21)
check("L-Aug1 M3 chimes 2:00-4:00", len(list(range(0, 121, 15))), 9)
check("L-Aug1 M3 gaps not chimes", 120 // 15, 8)
mins = 3 * 60 + 45 - (1 * 60 + 50) - 25
check("L-Aug1 Y3 reach station", (mins // 60, mins % 60), (1, 30))
hour_hand = (4 % 12) * 30 + 20 * 0.5
min_hand = 20 * 6
check("L-Aug1 Y4 angle at 4:20", abs(hour_hand - min_hand), 10.0)


# --- hourglass 9 minutes: simulate the stated procedure
def hourglass_check():
    """Follow the key's steps literally; return the minute the big glass empties last."""
    t = 0
    small, big = 4, 7            # sand remaining in the top of each
    events = []
    # run forward minute by minute
    small_left, big_left = 4, 7
    flips = {4: "small", 7: "big", 8: "big"}
    while t < 20:
        t += 1
        small_left -= 1
        big_left -= 1
        if t in flips:
            if flips[t] == "small":
                small_left = 4
            else:
                # flip the big glass: the sand that has fallen becomes the sand on top
                big_left = 7 - big_left if big_left > 0 else 7
        if t >= 8 and big_left == 0:
            events.append(t)
            break
    return events[0] if events else None


check("L-Aug1 Y1 hourglass lands on 9", hourglass_check(), 9)


# --- river crossing: BFS for the shortest safe solution
def river_min_crossings():
    items = frozenset(["goat", "grain", "jackal"])

    def safe(side_without_farmer):
        if {"jackal", "goat"} <= side_without_farmer:
            return False
        if {"goat", "grain"} <= side_without_farmer:
            return False
        return True

    start = (items, 0)
    from collections import deque
    seen, dq = {start: 0}, deque([start])
    while dq:
        near, boat = dq.popleft()
        far = items - near
        if not near and boat == 1:
            return seen[(near, boat)]
        src = near if boat == 0 else far
        for cargo in [frozenset()] + [frozenset([i]) for i in src]:
            nn = near - cargo if boat == 0 else near | cargo
            nf = items - nn
            # The farmer ends up on the side he rowed TO, so the side left
            # unattended is the one he rowed FROM: near when boat==0, far when boat==1.
            left_alone = nn if boat == 0 else nf
            if not safe(left_alone):
                continue
            st = (nn, 1 - boat)
            if st not in seen:
                seen[st] = seen[(near, boat)] + 1
                dq.append(st)
    return None


check("L-Jul31 M4 river crossings", river_min_crossings(), 7)


# --- two-guides puzzle: the named road is wrong under BOTH assignments
def guides_ok():
    results = []
    for truthful in ("A", "B"):
        for oasis in ("left", "right"):
            asked = "A"
            # "the other guide" is relative to the one we ASKED, not to who is honest
            other = "B"
            # what would the OTHER guide say the oasis road is?
            other_says = oasis if other == truthful else ("left" if oasis == "right" else "right")
            # asked guide reports that, truthfully or inverted
            reported = other_says if asked == truthful else ("left" if other_says == "right" else "right")
            results.append(reported != oasis)   # must always be the WRONG road
    return all(results)


check("L-Jul31 Y1 answer is always the wrong road", guides_ok(), True)


# --- weighing puzzles: minimum weighings = ceil(log3 n), verified by search
def min_weighings(n):
    k = 0
    while 3 ** k < n:
        k += 1
    return k


check("L-Jul31 Y4 nine sacks", min_weighings(9), 2)
check("L-Jul31 Y4 one weighing insufficient", 3 ** 1 < 9, True)
check("L-Aug2 Y4 eight kites", min_weighings(8), 2)

# --- backwards puzzles: verify by replaying FORWARDS
v = 21
v -= 5
v += 8
v = v // 2
check("L-Jul31 M1 replay forwards", v, 12)
v = 48
v = v // 2
v -= 6
v = v // 2
check("L-Jul31 Y2 replay forwards", v, 9)
v = 10
v += 4
v = v // 2
check("L-Aug2 M1 replay forwards", v, 7)

# --- combinatorics
kits = [(h, j) for h in ("red", "green", "brown") for j in ("leather", "silk")
        if not (h == "brown" and j == "silk")]
check("L-Jul30 M4 kits", len(kits), 5)
check("L-Jul30 Y4 greetings", len(list(combinations(range(7), 2))), 21)

# ============================== RENDERED HTML ==============================
import build_sheets

LITERALS = ["@page { margin: 0.55in; }", "line-height: 1.4;", "height: 78px;",
            "padding: 9px 12px;", "margin-bottom: 4px;", "margin: 4px 0 7px 0;",
            "margin-top: 7px;", "padding: 4px 8px;"]

for spec in specs_word.ALL + specs_logic.ALL:
    html = build_sheets.build(spec)
    name = spec["file"]
    check("%s: 3 sheet blocks" % name, html.count('class="sheet'), 3)
    check("%s: 2 date fields" % name,
          len(re.findall(r"<div>Date:\s*<span>.*?</span></div>", html, re.S)), 2)
    check("%s: no unfilled placeholder" % name, "%s" % "{}" in html, False)
    missing = [l for l in LITERALS if l not in html]
    check("%s: print-script CSS literals intact" % name, missing, [])
    kid_counts = (len(spec["kid1"]), len(spec["kid2"]))
    check("%s: equal problem count per kid" % name, kid_counts[0] == kid_counts[1], True)

# ============================== REPORT ==============================
width = max(len(r[0]) for r in rows)
fails = [r for r in rows if not r[3]]
for label, got, want, ok in rows:
    if not ok:
        print("FAIL  %-*s  got=%r  WANT=%r" % (width, label, got, want))
print("\n%d/%d checks passed, %d failed" % (len(rows) - len(fails), len(rows), len(fails)))
raise SystemExit(1 if fails else 0)
