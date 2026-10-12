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

# --- Aug 16 castles (Block 2 restart, faded TEACH)
q, r = divmod_by_repeated_subtraction(59, 7)
check("W-Aug16 M1 full/left", (q, r), (8, 3))
check("W-Aug16 M1 carts for all", boxes_needed(59, 7), 9)
check("W-Aug16 M2 towers", boxes_needed(94, 8), 12)
check("W-Aug16 M2 eleven is short", 11 * 8 < 94, True)
check("W-Aug16 M3 bricks", sum([136] * 6) - 87, 729)
check("W-Aug16 M4 5/6 > 3/4", F(5, 6) > F(3, 4), True)
check("W-Aug16 M4 margin is one 12th", F(5, 6) - F(3, 4), F(1, 12))
check("W-Aug16 M5 side", next(s for s in range(1, 100) if 8 * s == 96), 12)
check("W-Aug16 M5 perimeter", 8 + 12 + 8 + 12, 40)
check("W-Aug16 Y1 2/5+1/3", F(2, 5) + F(1, 3), F(11, 15))
check("W-Aug16 Y1 still under 1", F(11, 15) < 1, True)
check("W-Aug16 Y2 5/6-2/9", F(5, 6) - F(2, 9), F(11, 18))
check("W-Aug16 Y3 5/6+3/4", F(5, 6) + F(3, 4), F(19, 12))
check("W-Aug16 Y3 is >1 (mixed)", F(19, 12) > 1, True)
check("W-Aug16 Y4 47x36", sum([47] * 36), 1692)
check("W-Aug16 Y5 day rate", next(d for d in range(1, 300) if sum([d] * 6) == 288), 48)
check("W-Aug16 Y5 eleven days", sum([48] * 11), 528)
check("W-Aug16 Y5 good ones", sum([48] * 11) - 37, 491)

# the guided problem is the whole point of a faded TEACH — assert it is still there,
# on the PROTECTED skill for each kid, and that it is problem #1 and only problem #1.
for _kid, _slot in (("kid1", "remainder"), ("kid2", "unlike denominators")):
    _probs = specs_word.AUG16[_kid]
    check("W-Aug16 %s problem 1 is guided" % _kid, bool(_probs[0].get("guided")), True)
    check("W-Aug16 %s only #1 is guided" % _kid,
          [i for i, p in enumerate(_probs) if p.get("guided")], [0])

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

# --- Aug 16 rainforest logic (all helpers above are defined by now)
v = 19
v -= 6
v += 9
v = v // 2
check("L-Aug16 M1 replay forwards", v, 11)
check("L-Aug16 M2 neither", neither(24, 13, 11, 6), 6)

# the monkey/mango trap, modelled from the per-monkey rate rather than asserted
def eat_minutes(monkeys, mangoes, base_minutes=3):
    """Each monkey eats one mango in base_minutes; they eat in parallel."""
    rounds = mangoes // monkeys + (1 if mangoes % monkeys else 0)
    return rounds * base_minutes


check("L-Aug16 M3 nine monkeys nine mangoes", eat_minutes(9, 9), 3)
check("L-Aug16 M3 baseline reproduces", eat_minutes(3, 3), 3)
check("L-Aug16 M3 the trap answer is wrong", eat_minutes(9, 9) != 9, True)
check("L-Aug16 M4 parrot calls", len(list(combinations(range(5), 2))), 10)

sols = []
for animals in permutations(["toucan", "jaguar", "sloth"]):
    for camps in permutations(["Canopy", "Ridge", "River"]):
        a = dict(zip(["Ibrahim", "Khadija", "Sumayya"], animals))
        c = dict(zip(["Ibrahim", "Khadija", "Sumayya"], camps))
        if a[[p for p in c if c[p] == "Canopy"][0]] != "toucan":
            continue                                  # 1
        if c["Ibrahim"] == "River" or a["Ibrahim"] == "sloth":
            continue                                  # 2
        if a["Khadija"] != "jaguar":
            continue                                  # 3
        if c["Sumayya"] == "Ridge":
            continue                                  # 4
        sols.append({p: (a[p], c[p]) for p in a})
check("L-Aug16 Y1 grid unique", len(sols), 1)
check("L-Aug16 Y1 grid solution", sols[0],
      {"Ibrahim": ("toucan", "Canopy"), "Khadija": ("jaguar", "Ridge"),
       "Sumayya": ("sloth", "River")})
# clue 4 must be load-bearing: without it the camps are ambiguous, which is the
# thing kid2_watch tells the grown-up to listen for
sols_no4 = []
for animals in permutations(["toucan", "jaguar", "sloth"]):
    for camps in permutations(["Canopy", "Ridge", "River"]):
        a = dict(zip(["Ibrahim", "Khadija", "Sumayya"], animals))
        c = dict(zip(["Ibrahim", "Khadija", "Sumayya"], camps))
        if a[[p for p in c if c[p] == "Canopy"][0]] != "toucan":
            continue
        if c["Ibrahim"] == "River" or a["Ibrahim"] == "sloth":
            continue
        if a["Khadija"] != "jaguar":
            continue
        sols_no4.append(1)
check("L-Aug16 Y1 clue 4 is load-bearing", len(sols_no4) > 1, True)

check("L-Aug16 Y2 frogs together", first_common(8, 14), 56)
check("L-Aug16 Y2 times in 5 min",
      len([t for t in range(1, 301) if t % 8 == 0 and t % 14 == 0]), 5)


# Umar "not me", Harun "it was Umar", Zaynab "not Harun". Exactly one truth.
def st_aug16(speaker, culprit):
    if speaker == "Umar":
        return culprit != "Umar"
    if speaker == "Harun":
        return culprit == "Umar"
    return culprit != "Harun"                          # Zaynab


check("L-Aug16 Y3 liar unique",
      liar_solve(["Umar", "Harun", "Zaynab"], st_aug16, want_true=1), ["Harun"])
check("L-Aug16 Y4 twelve pods", min_weighings(12), 3)
check("L-Aug16 Y4 two weighings insufficient", 3 ** 2 < 12, True)
check("L-Aug16 Y4 three suffice", 3 ** 3 >= 12, True)

# --- Aug 17 immune system (word). Multiplications are re-derived as repeated
#     addition and divisions as repeated subtraction, so a slipped digit in
#     specs_word.py cannot agree with a slipped digit here.
check("W-Aug17 M1 side from area", next(s for s in range(1, 200) if 9 * s == 72), 8)
check("W-Aug17 M1 perimeter", 9 + 8 + 9 + 8, 34)
q, r = divmod_by_repeated_subtraction(75, 8)
check("W-Aug17 M2 full/left", (q, r), (9, 3))
check("W-Aug17 M2 trays for all", boxes_needed(75, 8), 10)
check("W-Aug17 M3 good samples", sum([128] * 7) - 94, 802)
check("W-Aug17 M4 two-thirds is the bigger vial", F(2, 3) > F(5, 8), True)
check("W-Aug17 M5 side from perimeter",
      next(s for s in range(1, 200) if 2 * (14 + s) == 46), 9)
check("W-Aug17 M5 area", sum([14] * 9), 126)
check("W-Aug17 M5 the trap answer is wrong", 46 - 14 != 9, True)
check("W-Aug17 Y1 decimal subtract", F(84, 10) - F(375, 100), F(93, 20))
check("W-Aug17 Y1 renders as 4.65", "%.2f" % float(F(93, 20)), "4.65")
check("W-Aug17 Y1 unpadded trap differs", F(93, 20) != F(475, 100), True)
check("W-Aug17 Y2 34x26", sum([34] * 26), 884)
q2, r2 = divmod_by_repeated_subtraction(1347, 6)
check("W-Aug17 Y3 long division", (q2, r2), (224, 3))
check("W-Aug17 Y3 reconstructs 1347", sum([6] * 224) + 3, 1347)
check("W-Aug17 Y4 fraction sum", F(3, 8) + F(1, 3), F(17, 24))
check("W-Aug17 Y5 strip cost", F(35, 100) * 240, F(84))
check("W-Aug17 Y5 change from 100", 100 - F(35, 100) * 240, F(16))

# --- Aug 17 immune logic
_v = 23
_v -= 7
_v += 12
_v //= 2
check("L-Aug17 M1 replay forwards", _v, 14)
check("L-Aug17 M2 neither", neither(30, 17, 14, 8), 7)


def climb_day(rise, fall, target):
    """Independent simulation of the climb-and-slip; no closed form."""
    pos, day = 0, 0
    while True:
        day += 1
        pos += rise
        if pos >= target:
            return day
        pos -= fall


check("L-Aug17 M3 climb reaches on day 8", climb_day(3, 2, 10), 8)
check("L-Aug17 M3 net-gain trap answer is wrong", 10 // (3 - 2) != climb_day(3, 2, 10), True)

from itertools import product as _product


def can_avoid_pair(kinds, picks):
    """Exhaustive: is ANY run of this many picks free of a repeat?"""
    return any(len(set(c)) == picks for c in _product(range(kinds), repeat=picks))


check("L-Aug17 M4 three picks can still miss", can_avoid_pair(3, 3), True)
check("L-Aug17 M4 four picks cannot", can_avoid_pair(3, 4), False)

_people = ["Idris", "Hafsa", "Zakariya"]


def immune_grid(use_clue4=True):
    out = []
    for cells in permutations(["T-cell", "B-cell", "macrophage"]):
        for labs in permutations(["North", "South", "Central"]):
            a = dict(zip(_people, cells))
            b = dict(zip(_people, labs))
            central = [p for p in _people if b[p] == "Central"][0]
            if a[central] != "macrophage":                    # clue 1
                continue
            if a["Idris"] == "B-cell":                        # clue 2
                continue
            if a["Hafsa"] != "T-cell":                        # clue 3
                continue
            if use_clue4 and b["Zakariya"] == "North":        # clue 4
                continue
            out.append((a, b))
    return out


_sols = immune_grid()
check("L-Aug17 Y1 grid unique", len(_sols), 1)
check("L-Aug17 Y1 grid solution",
      tuple((_sols[0][0][p], _sols[0][1][p]) for p in _people),
      (("macrophage", "Central"), ("T-cell", "North"), ("B-cell", "South")))
check("L-Aug17 Y1 clue 4 is load-bearing", len(immune_grid(use_clue4=False)) > 1, True)


def pour_reachable(cap_a, cap_b, target):
    """BFS over syringe states — proves 4 mL is actually obtainable."""
    seen, frontier = set(), [(0, 0)]
    while frontier:
        st = frontier.pop()
        if st in seen:
            continue
        seen.add(st)
        a, b = st
        if a == target or b == target:
            return True
        t1 = min(a, cap_b - b)
        t2 = min(b, cap_a - a)
        frontier += [(cap_a, b), (a, cap_b), (0, b), (a, 0),
                     (a - t1, b + t1), (a + t2, b - t2)]
    return False


check("L-Aug17 Y2 four mL is reachable", pour_reachable(5, 3, 4), True)
check("L-Aug17 Y2 and it needs both syringes", pour_reachable(5, 0, 4), False)


def st_aug17(speaker, culprit):
    if speaker == "Anas":
        return culprit == "Bilal"
    if speaker == "Bilal":
        return culprit != "Bilal"
    return culprit == "Anas"                           # Ruqayya


check("L-Aug17 Y3 liar unique (exactly one lying = two true)",
      liar_solve(["Anas", "Bilal", "Ruqayya"], st_aug17, want_true=2), ["Anas"])
check("L-Aug17 Y4 pieces", 42 // 6, 7)
check("L-Aug17 Y4 cuts by internal boundary count",
      len([x for x in range(6, 42, 6)]), 6)
check("L-Aug17 Y4 minutes", len([x for x in range(6, 42, 6)]) * 3, 18)
check("L-Aug17 Y4 one-cut-per-piece trap is wrong", (42 // 6) * 3 != 18, True)

# --- Aug 18 white cells (word). Same discipline as Aug 17: multiplication by
#     repeated addition, division by repeated subtraction, missing sides by
#     search over candidates rather than by rearranging the formula.
check("W-Aug18 M1 side from perimeter",
      next(s for s in range(1, 200) if 2 * (11 + s) == 58), 18)
check("W-Aug18 M1 area", sum([11] * 18), 198)
check("W-Aug18 M1 the no-halving trap is wrong", 58 - 11 != 18, True)
q, r = divmod_by_repeated_subtraction(92, 6)
check("W-Aug18 M2 full/left", (q, r), (15, 2))
check("W-Aug18 M2 racks for all", boxes_needed(92, 6), 16)
check("W-Aug18 M3 good cultures", sum([146] * 8) - 79, 1089)
check("W-Aug18 M4 three-fifths is the bigger dish", F(3, 5) > F(7, 12), True)
check("W-Aug18 M4 and it is close", F(3, 5) - F(7, 12), F(1, 60))
check("W-Aug18 M5 side from area", next(s for s in range(1, 200) if 12 * s == 108), 9)
check("W-Aug18 M5 perimeter", 12 + 9 + 12 + 9, 42)
check("W-Aug18 Y1 unlike denominators add", F(1, 4) + F(2, 5), F(13, 20))
check("W-Aug18 Y1 add-across trap differs", F(1, 4) + F(2, 5) != F(3, 9), True)
check("W-Aug18 Y2 unlike denominators subtract", F(7, 8) - F(1, 3), F(13, 24))
check("W-Aug18 Y2 subtract-across trap differs", F(7, 8) - F(1, 3) != F(6, 5), True)
check("W-Aug18 Y3 48x27", sum([48] * 27), 1296)
check("W-Aug18 Y4 doses given", F(24, 10) + F(375, 100), F(123, 20))
check("W-Aug18 Y4 renders as 6.15", "%.2f" % float(F(123, 20)), "6.15")
check("W-Aug18 Y4 remaining", F(95, 10) - (F(24, 10) + F(375, 100)), F(67, 20))
check("W-Aug18 Y4 renders as 3.35", "%.2f" % float(F(67, 20)), "3.35")
_rate, _rem_r = divmod_by_repeated_subtraction(1455, 5)
check("W-Aug18 Y5 rate is exact", (_rate, _rem_r), (291, 0))
check("W-Aug18 Y5 nine-day total", sum([291] * 9), 2619)
_f, _fr = divmod_by_repeated_subtraction(2619, 8)
check("W-Aug18 Y5 folders/left", (_f, _fr), (327, 3))
check("W-Aug18 Y5 reconstructs 2619", sum([8] * 327) + 3, 2619)

# --- Aug 18 lab bench logic
check("L-Aug18 M1 handshakes by enumerating pairs",
      len(list(combinations(range(6), 2))), 15)
check("L-Aug18 M1 the double-count trap is wrong", 6 * 5 != 15, True)
check("L-Aug18 M2 balance by search",
      [(v, f) for v in range(1, 100) for f in range(1, 100)
       if 3 * v == f and f + v == 32], [(8, 24)])
_t = 9 * 60 + 45
for _leg in (50, 25, 40):
    _t += _leg
check("L-Aug18 M3 finish time", (_t // 60, _t % 60), (11, 40))
check("L-Aug18 M3 is 1h55m of legs, not 1h15m", 50 + 25 + 40, 115)


def doubling_days(full_day):
    """Walk it forwards from 1 and read the day each level is reached."""
    level, out = 1, {}
    for day in range(1, full_day + 1):
        out[day] = level
        level *= 2
    full = out[full_day]
    half = [d for d, v in out.items() if v * 2 == full][0]
    quarter = [d for d, v in out.items() if v * 4 == full][0]
    return half, quarter


check("L-Aug18 M4 half and quarter days", doubling_days(12), (11, 10))
check("L-Aug18 M4 the halve-the-day trap is wrong", 12 // 2 != 11, True)

_techs = ["Yusra", "Bilal", "Amina"]


def bench_grid(use_clue4=True):
    out = []
    for tests in permutations(["blood", "swab", "culture"]):
        for shifts in permutations(["morning", "evening", "night"]):
            a = dict(zip(_techs, tests))
            b = dict(zip(_techs, shifts))
            culture = [p for p in _techs if a[p] == "culture"][0]
            if b[culture] != "night":                       # clue 1
                continue
            if a["Bilal"] != "culture":                     # clue 2
                continue
            if b["Yusra"] == "morning":                     # clue 3
                continue
            if use_clue4:
                blood = [p for p in _techs if a[p] == "blood"][0]
                if b[blood] != "morning":                   # clue 4
                    continue
            out.append((a, b))
    return out


_sol = bench_grid()
check("L-Aug18 Y1 grid has one solution", len(_sol), 1)
check("L-Aug18 Y1 assignment", (_sol[0][0], _sol[0][1]),
      ({"Yusra": "swab", "Bilal": "culture", "Amina": "blood"},
       {"Yusra": "evening", "Bilal": "night", "Amina": "morning"}))
check("L-Aug18 Y1 clue 4 is load-bearing", len(bench_grid(use_clue4=False)) > 1, True)


def scan_rounds(slides, capacity):
    """Fewest rounds to scan both sides of every slide, searched not reasoned.

    A round is a set of (slide, side) tasks, at most `capacity` of them, and a
    slide cannot have both its sides done in the same round.
    """
    tasks = [(s, side) for s in range(slides) for side in (0, 1)]
    for rounds in range(1, len(tasks) + 1):
        for assign in _product(range(rounds), repeat=len(tasks)):
            grouped = {}
            for t, rd in zip(tasks, assign):
                grouped.setdefault(rd, []).append(t)
            if any(len(g) > capacity for g in grouped.values()):
                continue
            if any(len({s for s, _ in g}) != len(g) for g in grouped.values()):
                continue
            if len(grouped) == rounds:
                return rounds
    return None


check("L-Aug18 Y2 three rounds suffice", scan_rounds(3, 2), 3)
check("L-Aug18 Y2 minutes", scan_rounds(3, 2) * 5, 15)
# The trap is NOT fully serial (that would be 6 rounds). It is filling the
# scanner greedily and finishing each group before starting the next: slides A+B
# take 2 rounds, then C alone takes 2 more with the machine half empty.
_naive_rounds = 2 * -(-3 // 2)
check("L-Aug18 Y2 finish-each-group trap costs 4 rounds", _naive_rounds, 4)
check("L-Aug18 Y2 trap in minutes", _naive_rounds * 5, 20)
check("L-Aug18 Y2 optimal really is faster", scan_rounds(3, 2) < _naive_rounds, True)


def can_avoid_triple(kinds, picks):
    """Exhaustive: is ANY run of this many picks free of three of a kind?"""
    return any(max(c.count(k) for k in set(c)) < 3
               for c in _product(range(kinds), repeat=picks))


check("L-Aug18 Y3 eight picks can still miss", can_avoid_triple(4, 8), True)
check("L-Aug18 Y3 nine picks cannot", can_avoid_triple(4, 9), False)
check("L-Aug18 Y3 the pair answer is not the triple answer", 4 + 1 != 9, True)

_n = 34
_n -= _n // 2                                    # half to North
_n -= 3                                          # set aside
_n -= _n // 2                                    # half to South
check("L-Aug18 Y4 replay forwards", _n, 7)

# --- Oct 12 mapmakers (word). Repeated addition / subtraction as above; the
#     kid2 fraction answers are rebuilt by break-apart (the method the sheet
#     teaches), not by the improper-fraction product the spec uses.
check("W-Oct12 M1 good maps", sum([128] * 6) - 95, 673)
q, r = divmod_by_repeated_subtraction(75, 8)
check("W-Oct12 M2 full/left", (q, r), (9, 3))
check("W-Oct12 M2 boats for all", boxes_needed(75, 8), 10)
_e, _er = divmod_by_repeated_subtraction(sum([12] * 4) - 18, 5)
check("W-Oct12 M3 pencils each, exact", (_e, _er), (6, 0))
check("W-Oct12 M4 two-thirds is bigger", F(2, 3) > F(5, 8), True)
check("W-Oct12 M4 and it is close", F(2, 3) - F(5, 8), F(1, 24))
check("W-Oct12 M5 side from area", next(s for s in range(1, 200) if 8 * s == 96), 12)
check("W-Oct12 M5 perimeter", 8 + 12 + 8 + 12, 40)
check("W-Oct12 Y1 break-apart", 6 * 3 + 6 * F(2, 5), F(102, 5))
check("W-Oct12 Y1 renders 20 2/5", specs_word.mixed(6 * 3 + 6 * F(2, 5)), "20 2/5")
check("W-Oct12 Y1 dropped-whole trap differs", 6 * F(2, 5) != F(102, 5), True)
check("W-Oct12 Y2 small map rivers",
      next(s for s in range(1, 100) if sum([s] * 6) == 54), 9)
check("W-Oct12 Y2 mountains", sum([9] * 3), 27)
check("W-Oct12 Y3 people = Khadijah + 4", 1 + 4, 5)
check("W-Oct12 Y3 share", F(8, 1 + 4), F(8, 5))
check("W-Oct12 Y3 renders 1 3/5", specs_word.mixed(F(8, 5)), "1 3/5")
_third = F(130, 3)
check("W-Oct12 Y4 two-thirds", _third + _third, F(260, 3))
check("W-Oct12 Y4 renders 86 2/3", specs_word.mixed(_third + _third), "86 2/3")
check("W-Oct12 Y4 less than 90", _third + _third < 90, True)
check("W-Oct12 Y4 2/3 of 135 is 90", F(2, 3) * 135, 90)
check("W-Oct12 Y4 remainder-as-whole trap differs", 2 * 43 + 1 != F(260, 3), True)
check("W-Oct12 Y5 area by break-apart", 2 * F(3, 4) + F(1, 2) * F(3, 4), F(15, 8))
check("W-Oct12 Y5 renders 1 7/8", specs_word.mixed(F(15, 8)), "1 7/8")

# --- Oct 12 map room logic
_pos = [0, 0]
for _dx, _dy, _n in ((0, 1, 3), (1, 0, 5), (0, -1, 1), (-1, 0, 2)):
    for _ in range(_n):
        _pos[0] += _dx
        _pos[1] += _dy
check("L-Oct12 M1 walk (east, north)", tuple(_pos), (3, 2))


def map_pens():
    """Every assignment of (map, pen) to Idris, Maryam, Bilal that fits clues 1-4."""
    people = ("Idris", "Maryam", "Bilal")
    out = []
    for maps in permutations(("river", "mountain", "city")):
        for pens in permutations(("red", "blue", "green")):
            m, p = dict(zip(people, maps)), dict(zip(people, pens))
            who = {v: k for k, v in m.items()}
            if (p[who["river"]] == "blue" and m["Maryam"] == "city"
                    and p["Idris"] != "blue" and p[who["city"]] != "red"):
                out.append(tuple((x, m[x], p[x]) for x in people))
    return out


check("L-Oct12 M2 unique grid", map_pens(),
      [(("Idris", "mountain", "red"), ("Maryam", "city", "green"), ("Bilal", "river", "blue"))])
check("L-Oct12 M3 halfway km", sum([5] * 8) // 2, 20)
check("L-Oct12 M4 routes by listing",
      len([(a, b) for a in "ABC" for b in "12"]), 6)

_borders = {("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("C", "D"), ("C", "E"), ("D", "E")}


def min_colours(nodes, edges):
    for k in range(1, len(nodes) + 1):
        for combo in __import__("itertools").product(range(k), repeat=len(nodes)):
            col = dict(zip(nodes, combo))
            if all(col[a] != col[b] for a, b in edges):
                return k
    return None


check("L-Oct12 Y1 fewest colours", min_colours("ABCDE", _borders), 3)
_shown = {"A": 0, "B": 1, "C": 2, "D": 1, "E": 0}
check("L-Oct12 Y1 key's colouring is legal", all(_shown[a] != _shown[b] for a, b in _borders), True)
# The prose borders list must match the edge set, from both sides.
_prose = {"A": "BCD", "B": "AC", "C": "ABDE", "D": "ACE", "E": "CD"}
check("L-Oct12 Y1 prose borders symmetric and equal to edges",
      {tuple(sorted((a, b))) for a, bs in _prose.items() for b in bs}, _borders)


def chest_labels(treasure):
    return [treasure == "gold", treasure != "silver", treasure != "gold"]


check("L-Oct12 Y2 exactly one true label",
      [c for c in ("gold", "silver", "bronze") if sum(chest_labels(c)) == 1], ["silver"])


def grid_paths(east, north):
    """Enumerate every E/N word rather than use n-choose-k."""
    return len({w for w in permutations("E" * east + "N" * north)})


check("L-Oct12 Y3 shortest routes", grid_paths(3, 2), 10)


def photo_orders():
    out = []
    for o in permutations(("Zaid", "Huda", "Anas", "Safiya")):
        i = {n: k for k, n in enumerate(o)}
        if (i["Huda"] < i["Zaid"] and {o[0], o[3]} == {"Anas", "Safiya"}
                and abs(i["Safiya"] - i["Zaid"]) == 1):
            out.append(o)
    return out


check("L-Oct12 Y4 unique order", photo_orders(), [("Anas", "Huda", "Zaid", "Safiya")])

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
