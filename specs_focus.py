"""Musa focus track (Noetic prep, from 2026-10-25): algebraic-thinking word sheets.

Why this exists: a graded Grade 3 practice test (2026-10-24) showed one weak
strand besides the zeros fluency (see drill_gen.py --skill zeros). The algebraic
strand misses were: working backwards (#12), sum and difference (#9), two
unknowns (#15), balance/proportion (#16). The plan is in
private/PRACTICE-PLAN-2026.md "Musa focus track: Noetic prep".

One sheet per school day, ONE method per sheet. DAY1 teaches "undo the steps".

Kid1 only. The spec carries no name -- build_focus.py reads it from
kids.local.json at render time, same as every other generator here.

Every answer is COMPUTED: each problem is a secret start plus a chain of ops,
the result is produced by running the chain FORWARD, and the key undoes it. So
the numbers on the page cannot disagree with the arithmetic. verify_focus.py
re-derives each answer a different way (brute-force search, not undoing).
"""

# op symbol -> (forward, inverse, words used in the key, symbol shown on the page)
OPS = {
    "+": (lambda x, n: x + n, lambda x, n: x - n, "add", "+"),
    "-": (lambda x, n: x - n, lambda x, n: x + n, "subtract", "&minus;"),
    "*": (lambda x, n: x * n, lambda x, n: x // n, "multiply by", "&times;"),
    "/": (lambda x, n: x // n, lambda x, n: x * n, "divide by", "&divide;"),
}
UNDO_SYM = {"+": "&minus;", "-": "+", "*": "&divide;", "/": "&times;"}


def run_forward(start, ops):
    """Apply ops in order. Raises if a division is not exact (no remainders here)."""
    x = start
    for sym, n in ops:
        if sym == "/" and x % n:
            raise ValueError("inexact division %d / %d" % (x, n))
        x = OPS[sym][0](x, n)
    return x


def undo_trail(result, ops):
    """[(value_before_undo, symbol, n, value_after_undo)] walking the chain backwards."""
    trail, x = [], result
    for sym, n in reversed(ops):
        y = OPS[sym][1](x, n)
        trail.append((x, UNDO_SYM[sym], n, y))
        x = y
    return trail


def problem(secret, ops, q, fact, guided=None, watch=""):
    result = run_forward(secret, ops)
    trail = undo_trail(result, ops)
    answer = trail[-1][3]
    assert answer == secret, "undo did not return the secret"
    steps = " &nbsp;then&nbsp; ".join(
        "%d %s %d = <b>%d</b>" % (a, s, n, b) for a, s, n, b in trail)
    fwd = " &rarr; ".join(["?"] + ["%s%d" % (OPS[s][3], n) for s, n in ops]
                          + [str(result)])
    check_x, chk = secret, []
    for sym, n in ops:
        nxt = OPS[sym][0](check_x, n)
        chk.append("%d %s %d = %d" % (check_x, OPS[sym][3], n, nxt))
        check_x = nxt
    if watch == "auto":
        stops = ", ".join(str(t[3]) for t in trail[:-1])
        watch = ("Right answer %d. Expect %s if he stops early (middle values). An undo "
                 "that does not come out even means the wrong order." % (answer, stops))
    d = {"secret": secret, "ops": ops, "result": result, "answer": answer,
         "q": q, "fact": fact, "a": "%d" % answer,
         "steps": "Arrows: %s. Undo from the LAST arrow: %s. Check: %s." % (
             fwd, steps, "; ".join(chk)),
         "watch": watch}
    if guided:
        d["guided"] = guided
    return d


BLANK = "<span class='blank'></span>"

DAY1 = {
    "file": "worksheet-focus-2026-10-25-undo.html",
    "key_file": "worksheet-focus-2026-10-25-undo-key.html",
    "date": "October 25, 2026",
    "title_plain": "Undo the Steps",
    "title": "&#128294; Undo the Steps",
    "sub": "Cave explorers work backwards — start at the answer, undo the arrows",
    # worked example, all numbers computed from the same chain machinery
    "example": {"who": "Hamza", "secret": 11, "ops": [("*", 5), ("+", 8)]},
    "problems": [
        problem(
            9, [("*", 4), ("-", 7)],
            "Layla is a cave guide. She thinks of a secret number of lanterns. She "
            "multiplies it by 4, then subtracts 7. She ends with 29. What was her "
            "secret number?",
            "A deep cave stays almost the same temperature all year, close to the "
            "average yearly temperature of the land above it.",
            guided=True,
            watch="Expect 36. He undoes the last arrow, then stops (the same slip as "
                  "42 on practice-test #12). Ask: is 36 the start, or only the middle?"),
        problem(
            24, [("/", 3), ("+", 12)],
            "Omar is a park ranger. He picks a secret number, divides it by 3, then "
            "adds 12. He gets 20. What was his secret number?",
            "Mammoth Cave in Kentucky is the longest known cave system in the world. "
            "More than 400 miles of its passages have been mapped.",
            watch="Expect 8 (stopped after one undo) or 20 &divide; 3 (undoing in the "
                  "wrong order: it does not come out even, which is the clue)."),
        problem(
            9, [("+", 6), ("*", 3), ("-", 5)],
            "Aisha is mapping a cave with a rope. She picks a number of rope-lengths, "
            "adds 6, multiplies by 3, then subtracts 5. She gets 40. How many "
            "rope-lengths did she start with?",
            "Some stalactites grow only about 1 centimeter in 100 years, so a long one "
            "can be thousands of years old.",
            watch="Three arrows, so three undos. Expect 45 or 15 (stopped early). "
                  "If he writes 40 &divide; 3, the order is wrong: 40 does not divide "
                  "by 3."),
        problem(
            39, [("-", 15), ("/", 4)],
            "At sunset the bats leave Khadija's cave. First 15 bats fly out. The bats "
            "that are left split into 4 equal groups of 6. How many bats were in the "
            "cave at the start?",
            "Bracken Cave in Texas is home to about 15 million Mexican free-tailed "
            "bats, the biggest bat colony known.",
            watch="No arrows are given: he must draw them. Expect 24 (stopped early) or "
                  "9 (24 &minus; 15, the wrong way). Ask him to draw the two arrows "
                  "before any arithmetic."),
        problem(
            8, [("*", 6), ("-", 9)],
            "Yusra collects crystals in a cave. She multiplies her number of crystals by "
            "6, then gives away 9. She has 39 left. How many crystals did she start with?",
            "Some caves hold giant crystals: the Cave of the Crystals in Mexico has "
            "crystals longer than a school bus.",
            watch="Expect 48 (one undo, then stopped) or 5 (39 &divide; 6 first, which "
                  "leaves a remainder: the clue the order is wrong)."),
    ],
}

# ---------------------------------------------------------------------------
# kid2 focus track (Noetic prep, from 2026-10-25): substitution / "trade it".
#
# Why: a Noetic-style Grade 4 practice test (2026-10-24) missed #2 (two unknowns
# with a relation), #5 (averages) and #4 (age problem). The plan is in
# private/PRACTICE-PLAN-2026.md "kid2 focus track". Day 1 is strand (a), the main
# focus: "one A costs the same as k B's" -- trade every A for k B's, then there is
# ONE unknown item, and a single division finds its price.
#
# A problem is: a A's and b B's cost T dollars; 1 A = k B's; how much do c A's and
# d B's cost? Every number on the page and in the key is computed from
# (a, b, k, T, c, d), and trade_problem() refuses a spec where the prices are not
# whole dollars. verify_focus.py re-derives each answer by brute-force search over
# both prices, not by trading.
# ---------------------------------------------------------------------------


def trade_problem(names, tmpl, a, b, k, price_b, c, d, fact, guided=None, who=""):
    """names = (A_one, A_many, B_one, B_many). Total T is computed from price_b."""
    a1, am, b1, bm = names
    pb = price_b
    pa = k * pb
    T = a * pa + b * pb
    n = a * k + b
    m = c * k + d
    assert T % n == 0 and T // n == pb, "prices must come out whole"
    ans = c * pa + d * pb
    assert ans == m * pb
    q = tmpl.format(a=a, b=b, k=k, T=T, c=c, d=d)
    steps = (
        "Trade every %s for %d %s: %d %s = %d %s. Now %d + %d = <b>%d</b> %s cost $%d, "
        "so 1 %s = $%d &divide; %d = <b>$%d</b> (and 1 %s = %d &times; $%d = $%d). "
        "Asked: %d %s and %d %s = %d + %d = %d %s = %d &times; $%d = <b>$%d</b>. "
        "Check: %d &times; $%d + %d &times; $%d = $%d."
    ) % (a1, k, bm, a, am if a != 1 else a1, a * k, bm, a * k, b, n, bm, T,
         b1, T, n, pb, a1, k, pb, pa,
         c, am if c != 1 else a1, d, bm if d != 1 else b1, c * k, d, m, bm, m, pb, ans,
         a, pa, b, pb, T)
    # the two slips this sheet is built to catch, with their numbers computed
    slip_untraded = (c + d) * pb       # priced the asked items as if each cost one B
    watch = (
        "Right answer $%d. Expect $%d if he forgets to trade the asked %s too "
        "(%d items at $%d). Expect '$%d &divide; %d = ?' (splitting $%d over the %d items "
        "as if every item cost the same): that is the sign he skipped the trade. "
        "Ask for the trade line first: '%d %s = ___ %s'."
    ) % (ans, slip_untraded, am, c + d, pb, T, a + b, T, a + b, 1, a1, bm)
    d_ = {"names": names, "a_n": a, "b_n": b, "k": k, "T": T, "c_n": c, "d_n": d,
          "q": q, "fact": fact, "answer": ans, "a": "$%d" % ans,
          "steps": steps, "watch": watch, "who": who}
    if guided:
        d_["guided"] = guided
    return d_


TRADE_DAY1 = {
    "kid": "kid2",
    "kind": "trade",
    "file": "worksheet-focus-2026-10-25-trade.html",
    "key_file": "worksheet-focus-2026-10-25-trade-key.html",
    "pdf_stem": "focus-2026-10-25-trade-word",
    "date": "October 25, 2026",
    "title_plain": "Trade It",
    "title": "&#128214; Trade It",
    "sub": "The book fair: swap one thing for what it is worth. Write the trade line first, every time.",
    # worked example: 2 jars + 2 quills = $18; 1 jar = 2 quills; ask 3 jars + 1 quill
    "example": {"a": 2, "b": 2, "k": 2, "T": 18, "c": 3, "d": 1},
    "problems": [
        trade_problem(
            ("notebook", "notebooks", "pen", "pens"),
            "Bilal is at the book fair. He buys {a} notebooks and {b} pens for ${T}. "
            "One notebook costs the same as {k} pens. How much do 1 notebook and "
            "{d} pens cost?",
            2, 3, 2, 3, 1, 4,
            "Johannes Gutenberg's printing press (about 1450) let one shop make "
            "hundreds of identical books, when each one had been copied by hand.",
            guided=True),
        trade_problem(
            ("bookmark", "bookmarks", "sticker", "stickers"),
            "Zainab helps at the paper stall. {a} bookmarks and {b} stickers cost "
            "${T}. One bookmark costs the same as {k} stickers. How much do {c} "
            "bookmarks and {d} stickers cost?",
            3, 4, 2, 2, 5, 2,
            "Baghdad had paper mills by about the year 800, and the city's House of "
            "Wisdom collected and translated books from many languages."),
        trade_problem(
            ("atlas", "atlases", "map", "maps"),
            "Idris sells maps at the fair. {a} atlases and {b} maps cost ${T}. One "
            "atlas costs the same as {k} maps. How much do {c} atlases and {d} map "
            "cost?",
            2, 6, 4, 2, 3, 1,
            "The al-Qarawiyyin library in Fez, Morocco, was founded in 859 by "
            "Fatima al-Fihri. It is one of the oldest libraries in the world still open."),
        trade_problem(
            ("poster", "posters", "flyer", "flyers"),
            "Maryam runs the print shop. {a} posters and {b} flyers cost ${T}. One "
            "poster costs the same as {k} flyers. How much do {c} posters and {d} "
            "flyers cost?",
            7, 4, 3, 2, 4, 9,
            "Printers fold big sheets into groups of pages called signatures, "
            "usually 8, 16 or 32 pages, then sew the signatures into a book."),
        trade_problem(
            ("dictionary", "dictionaries", "comic", "comics"),
            "Hasan buys {a} dictionaries and {b} comics for ${T}. One dictionary costs "
            "the same as {k} comics. How much do {c} dictionaries and {d} comics cost?",
            3, 5, 3, 2, 2, 3,
            "The first big English dictionary by one author, Samuel Johnson's, came out "
            "in 1755 and took him about nine years to write."),
    ],
}

# Plan samples for strands (b) averages and (c) general algebraic thinking.
# Each is re-derived by brute force in verify_focus.py. (kind, data..., answer)
SAMPLES_KID2 = [
    {"kind": "avg_missing", "avg": 85, "count": 6, "known": [80, 90, 88, 76, 92],
     "answer": 84,
     "q": "Hamza's 6 test scores have an average of 85. Five of them are 80, 90, 88, "
          "76 and 92. What is the sixth score?"},
    {"kind": "avg_add", "avg": 12, "count": 4, "added": 27, "answer": 15,
     "q": "Four friends have an average of 12 marbles each. Salma joins them with 27 "
          "marbles. What is the new average?"},
    {"kind": "age", "now": 7, "years": 5, "times": 3, "answer": 31,
     "q": "Omar is 7. In 5 years his mother will be 3 times as old as Omar will be "
          "then. How old is his mother now?"},
    {"kind": "equation", "mul": 4, "sub": 6, "rhs_a": 3, "rhs_b": 6, "answer": 6,
     "q": "? &times; 4 &minus; 6 = 3 &times; 6. What number goes in the box?"},
]

# ---------------------------------------------------------------------------
# BATCH B (Asif 2026-10-25: "have a second batch ready in case the first batch doesn't
# go well, and I want them to practice more"). Same method, same layout, new numbers
# and theme. Built now, printed only when he asks (one day's paper rule still holds:
# it is the same target day).
# ---------------------------------------------------------------------------
DAY1_B = {
    "file": "worksheet-focus-2026-10-25-undo-b.html",
    "key_file": "worksheet-focus-2026-10-25-undo-b-key.html",
    "date": "October 25, 2026",
    "title_plain": "Undo the Steps (B)",
    "title": "&#127793; Undo the Steps (B)",
    "sub": "In the garden: start at the answer and undo the arrows, one per line",
    "example": {"who": "Hamza", "secret": 11, "ops": [("*", 5), ("+", 8)]},
    "problems": [
        problem(
            7, [("*", 3), ("+", 5)],
            "Bilal plants seeds. He thinks of a secret number, multiplies it by 3, then "
            "adds 5. He gets 26. What was his secret number?",
            "Young sunflowers turn to follow the sun across the sky during the day.",
            guided=True,
            watch="Expect 21 (one undo, then stopped). Ask: are there arrows left?"),
        problem(
            6, [("*", 5), ("-", 8)],
            "Sara picks a number of flower pots. She multiplies it by 5, then subtracts "
            "8. She ends with 22. How many pots did she pick?",
            "A strawberry carries its seeds on the outside, about 200 of them.",
            watch="Expect 30 (stopped after one undo) or 14 (subtracted instead of adding back)."),
        problem(
            32, [("/", 4), ("+", 9)],
            "Yahya has a secret number of carrots. He divides it by 4, then adds 9. He "
            "gets 17. How many carrots did he start with?",
            "Pumpkins are a fruit, because they grow from a flower and hold seeds.",
            watch="Expect 8 (stopped after one undo) or 2 (divided by 4 again instead of multiplying)."),
        problem(
            4, [("+", 5), ("*", 4), ("-", 6)],
            "Noor picks a number. She adds 5, multiplies by 4, then subtracts 6. She "
            "gets 30. What number did she pick?",
            "Earthworms help a garden: their tunnels let air and water reach the roots.",
            watch="Three arrows, three undos. Expect 36 or 9 (stopped early)."),
        problem(
            50, [("-", 14), ("/", 6)],
            "Musa's family picks tomatoes. They eat 14 of them. The rest are split into "
            "6 baskets with 6 tomatoes in each. How many tomatoes did they pick?",
            "Some kinds of bamboo can grow more than 2 feet in a single day.",
            watch="No arrows given: he draws them. Expect 36 (stopped early) or 22 (36 &minus; 14)."),
    ],
}

TRADE_DAY1_B = {
    "kid": "kid2",
    "kind": "trade",
    "file": "worksheet-focus-2026-10-25-trade-b.html",
    "key_file": "worksheet-focus-2026-10-25-trade-b-key.html",
    "pdf_stem": "focus-2026-10-25-trade-b-word",
    "date": "October 25, 2026",
    "title_plain": "Trade It (B)",
    "title": "&#129473; Trade It (B)",
    "sub": "The bakery: swap one thing for what it is worth, one step per line.",
    "example": {"a": 2, "b": 2, "k": 2, "T": 18, "c": 3, "d": 1},
    "problems": [
        trade_problem(
            ("muffin", "muffins", "cookie", "cookies"),
            "Amina buys {a} muffins and {b} cookies for ${T}. One muffin costs the same "
            "as {k} cookies. How much do {c} muffins and {d} cookies cost?",
            3, 2, 3, 2, 2, 4,
            "Baking soda makes bubbles when it meets something sour, like buttermilk. "
            "The bubbles make muffins rise.",
            guided=True),
        trade_problem(
            ("croissant", "croissants", "bagel", "bagels"),
            "Ilyas buys {a} croissants and {b} bagels for ${T}. One croissant costs the "
            "same as {k} bagels. How much do {c} croissants and {d} bagel cost?",
            2, 5, 2, 3, 3, 1,
            "Bagels are boiled in water before they are baked. That gives them their "
            "chewy crust."),
        trade_problem(
            ("cake", "cakes", "cupcake", "cupcakes"),
            "Fatima buys {a} cake and {b} cupcakes for ${T}. One cake costs the same as "
            "{k} cupcakes. How much do {c} cakes and {d} cupcakes cost?",
            1, 6, 5, 2, 2, 3,
            "Bread rises because yeast eats sugar and lets out a gas that makes "
            "bubbles in the dough."),
        trade_problem(
            ("pie", "pies", "tart", "tarts"),
            "Khalid buys {a} pies and {b} tarts for ${T}. One pie costs the same as {k} "
            "tarts. How much do {c} pies and {d} tarts cost?",
            3, 4, 4, 1, 2, 5,
            "Bakers often weigh flour instead of measuring it in cups, because a cup "
            "of flour can hold more or less depending on how it is packed."),
        trade_problem(
            ("loaf", "loaves", "roll", "rolls"),
            "Hana buys {a} loaves and {b} rolls for ${T}. One loaf costs the same as {k} "
            "rolls. How much do {c} loaves and {d} rolls cost?",
            2, 7, 6, 1, 3, 2,
            "Most bread needs only four things: flour, water, salt and yeast."),
    ],
}

# ---------------------------------------------------------------------------
# DAY 2 (2026-10-26).
#
# kid1 (Musa): "undo the steps" with THREE arrows; the story never says "arrow", he draws
# them. Same walk-through format as Day 1, so it reuses problem() and the undo ladder.
#
# kid2 (Yusuf): kind "eq". Asif, 2026-10-25 13:53 (AGENTS.md "kid2 format direction"):
# explicit letter equations with substitution, ONE step per line, like his own worked
# photo (2n + 3p = 21, n = 2p -> 4p + 3p = 21 -> 7p = 21 -> p = 3 -> 6p -> 18). A small
# chip picture is only a side aid. The plan's Day 2 also asks for one "$e more"
# relation (rel "more"); the rest are "k times" (rel "k").
#
# eq_problem() stores only the raw numbers plus the relation; build_focus.eq_lines()
# derives every equation line from them, and verify_focus.py re-derives the prices by
# brute-force search over both prices (not by the substitution the sheet teaches).
# ---------------------------------------------------------------------------


def eq_problem(names, tmpl, rel, a, b, r, price_b, c, d, fact, guided=None):
    """rel 'k': 1 A = r B's.  rel 'more': 1 A = 1 B + r.  Prices come out whole dollars."""
    a1, am, b1, bm = names
    la, lb = a1[0], b1[0]
    assert la != lb, "letters must differ"
    pb = price_b
    pa = r * pb if rel == "k" else pb + r
    T = a * pa + b * pb
    ans = c * pa + d * pb
    q = tmpl.format(a=a, b=b, k=r, e=r, T=T, c=c, d=d)
    if rel == "k":
        slip = (c + d) * pb
        slip_txt = ("Expect $%d if he forgets to swap the asked %s too (%d items at $%d)."
                    % (slip, am, c + d, pb))
    else:
        # distribution slip: a(B + e) written as aB + e  ->  (a+b)B + e = T
        num = T - r
        slip_txt = ("Expect the distribution slip: %d(%s + %d) written as %d%s + %d, which "
                    "gives %s = %s, not a whole price." % (
                        a, lb, r, a, lb, r, lb,
                        ("$%d" % (num // (a + b))) if num % (a + b) == 0
                        else "%d/%d" % (num, a + b)))
    watch = ("Right answer $%d. %s Also expect the right idea with LINES SKIPPED (jumps from "
             "the story to '%s = %d'): send it back for the substitute line." % (ans, slip_txt, lb, pb))
    d_ = {"names": names, "letters": (la, lb), "rel": rel, "r": r, "a_n": a, "b_n": b,
          "T": T, "c_n": c, "d_n": d, "pa": pa, "pb": pb, "q": q, "fact": fact,
          "answer": ans, "a": "$%d" % ans, "watch": watch}
    if guided:
        d_["guided"] = True
    return d_


UNDO_DAY2 = {
    "file": "worksheet-focus-2026-10-26-undo.html",
    "key_file": "worksheet-focus-2026-10-26-undo-key.html",
    "pdf_stem": "focus-2026-10-26-undo-word",
    "date": "October 26, 2026",
    "title_plain": "Undo the Steps 2",
    "title": "&#128167; Undo the Steps 2",
    "sub": "Wells and water: three things happen to the number. Draw them, then undo them, one per line",
    "example": {"who": "Tariq", "secret": 7, "ops": [("+", 4), ("*", 3), ("-", 5)]},
    "problems": [
        problem(
            6, [("*", 3), ("+", 4), ("*", 2)],
            "Layla draws water from a village well. She picks a secret number of buckets, "
            "multiplies it by 3, adds 4, then multiplies by 2. She gets 44. What was her "
            "secret number?",
            "Rain soaks down through soil and rock into an underground layer called an "
            "aquifer. A well is a hole that reaches down into it.",
            guided=True,
            watch="auto"),
        problem(
            5, [("+", 7), ("*", 4), ("-", 10)],
            "Omar fills water jugs at a well. He starts with a secret number of jugs, adds "
            "7, multiplies by 4, then takes away 10. He ends with 38. What was his secret "
            "number?",
            "Qanats are underground channels in Iran that carry water from the hills to "
            "villages without any pump. Some are more than 2,000 years old.",
            watch="auto"),
        problem(
            28, [("/", 4), ("+", 9), ("*", 3)],
            "Aisha measures the water in a cistern. She divides her secret number of liters "
            "by 4, adds 9, then multiplies by 3. She gets 48. What was her secret number?",
            "A pulley over a well lets you pull DOWN on the rope to lift the bucket up, "
            "which is easier than lifting straight up.",
            watch="auto"),
        problem(
            9, [("*", 5), ("-", 12), ("/", 3)],
            "Idris carries water jugs to the market. Each jug he starts with is swapped for "
            "5 small cups. Then 12 cups break. The rest are shared equally among 3 families, "
            "and each family gets 11 cups. How many jugs did he start with?",
            "The Chand Baori stepwell in India has about 3,500 narrow steps that lead down "
            "to the water.",
            watch="auto"),
        problem(
            20, [("-", 8), ("*", 6), ("+", 9)],
            "Yusra fills a water tank. She takes 8 away from her secret number of liters, "
            "multiplies by 6, then adds 9. She gets 81. What was her secret number?",
            "Most adults need about 2 liters of fluid a day, and more when it is hot.",
            watch="auto"),
    ],
}

UNDO_DAY2_B = {
    "file": "worksheet-focus-2026-10-26-undo-b.html",
    "key_file": "worksheet-focus-2026-10-26-undo-b-key.html",
    "pdf_stem": "focus-2026-10-26-undo-b-word",
    "date": "October 26, 2026",
    "title_plain": "Undo the Steps 2 (B)",
    "title": "&#129526; Undo the Steps 2 (B)",
    "sub": "Silk and dye: three things happen to the number. Draw them, then undo them, one per line",
    "example": {"who": "Tariq", "secret": 7, "ops": [("+", 4), ("*", 3), ("-", 5)]},
    "problems": [
        problem(
            5, [("*", 4), ("-", 6), ("+", 9)],
            "Hana raises silkworms. She picks a secret number of leaves, multiplies it by 4, "
            "takes away 6, then adds 9. She gets 23. What was her secret number?",
            "Silkworms eat mulberry leaves, and one cocoon is a single thread that can be "
            "hundreds of meters long.",
            guided=True,
            watch="auto"),
        problem(
            12, [("+", 8), ("/", 2), ("*", 5)],
            "Bilal has a secret number of spools of thread. He adds 8, divides by 2, then "
            "multiplies by 5. He gets 50. What was his secret number?",
            "Indigo, a deep blue dye, is made from the leaves of the indigo plant.",
            watch="auto"),
        problem(
            4, [("*", 3), ("+", 7), ("*", 2)],
            "Sara dyes cloth. She multiplies her secret number of meters by 3, adds 7, then "
            "multiplies by 2. She gets 38. What was her secret number?",
            "Tyrian purple was made from sea snails. It took thousands of snails to dye "
            "one robe, so only the very rich could buy it.",
            watch="auto"),
        problem(
            24, [("-", 6), ("*", 3), ("/", 9)],
            "Noor has a number of silk cocoons. She uses 6 of them, and each of the rest "
            "is spun into 3 skeins of thread. She packs the skeins into boxes of 9 and "
            "fills exactly 6 boxes. How many cocoons did she start with?",
            "Saffron, a bright yellow-orange dye and spice, comes from the threads inside a "
            "crocus flower.",
            watch="auto"),
        problem(
            35, [("/", 5), ("+", 13), ("*", 4)],
            "Yahya divides his secret number of silk threads by 5, adds 13, then multiplies "
            "by 4. He gets 80. What was his secret number?",
            "Madder root gives a red dye and has been used for cloth for thousands of years.",
            watch="auto"),
    ],
}

TRADE_DAY2 = {
    "kid": "kid2",
    "kind": "eq",
    "file": "worksheet-focus-2026-10-26-trade.html",
    "key_file": "worksheet-focus-2026-10-26-trade-key.html",
    "pdf_stem": "focus-2026-10-26-trade-word",
    "date": "October 26, 2026",
    "title_plain": "Trade It with Letters",
    "title": "&#129351; Trade It with Letters",
    "sub": "The Olympic shop: write each step as an equation, one step per line, like a mathematician",
    # worked example: 2 jars + 2 quills = $18; 1 jar = 2 quills; ask 3 jars + 1 quill
    "example": {"names": ("jar", "jars", "quill", "quills"), "rel": "k",
                "a": 2, "b": 2, "r": 2, "pb": 3, "c": 3, "d": 1},
    "problems": [
        eq_problem(
            ("ticket", "tickets", "badge", "badges"),
            "Sumaya buys {a} tickets and {b} badges at the Olympic shop for ${T}. One ticket "
            "costs the same as {k} badges. How much do {c} ticket and {d} badges cost?",
            "k", 3, 2, 2, 2, 1, 3,
            "The Olympic Games began in Olympia, Greece, more than 2,700 years ago. The "
            "modern Games started in Athens in 1896.",
            guided=True),
        eq_problem(
            ("flag", "flags", "pin", "pins"),
            "Hamza buys {a} flags and {b} pins for ${T}. One flag costs the same as {k} pins. "
            "How much do {c} flags and {d} pins cost?",
            "k", 2, 4, 3, 2, 3, 2,
            "The five Olympic rings link five parts of the world: the Americas, Africa, Asia, "
            "Europe and Oceania."),
        eq_problem(
            ("jersey", "jerseys", "cap", "caps"),
            "Zaid buys {a} jersey and {b} caps for ${T}. One jersey costs the same as {k} "
            "caps. How much do {c} jerseys and {d} caps cost?",
            "k", 1, 3, 4, 2, 2, 5,
            "The torch for each Games is lit in Olympia with a curved mirror that focuses "
            "the sun's rays."),
        eq_problem(
            ("scarf", "scarves", "button", "buttons"),
            "Maryam buys {a} scarves and {b} buttons for ${T}. One scarf costs the same as "
            "{k} buttons. How much do {c} scarves and {d} buttons cost?",
            "k", 4, 3, 2, 3, 5, 2,
            "The marathon is 42.195 kilometers (26.2 miles) long. It is named for a "
            "famous run from Marathon to Athens."),
        eq_problem(
            ("towel", "towels", "bottle", "bottles"),
            "Khadija buys {a} towels and {b} bottles for ${T}. One towel costs ${e} more than "
            "one bottle. How much do {c} towels and {d} bottles cost?",
            "more", 3, 2, 4, 3, 2, 4,
            "Gold medals today are mostly silver with a thin coat of gold on the outside."),
    ],
}

TRADE_DAY2_B = {
    "kid": "kid2",
    "kind": "eq",
    "file": "worksheet-focus-2026-10-26-trade-b.html",
    "key_file": "worksheet-focus-2026-10-26-trade-b-key.html",
    "pdf_stem": "focus-2026-10-26-trade-b-word",
    "date": "October 26, 2026",
    "title_plain": "Trade It with Letters (B)",
    "title": "&#127753; Trade It with Letters (B)",
    "sub": "The bridge gift shop: write each step as an equation, one step per line",
    "example": {"names": ("jar", "jars", "quill", "quills"), "rel": "k",
                "a": 2, "b": 2, "r": 2, "pb": 3, "c": 3, "d": 1},
    "problems": [
        eq_problem(
            ("book", "books", "magnet", "magnets"),
            "Ilyas buys {a} books and {b} magnet at the bridge gift shop for ${T}. One book "
            "costs the same as {k} magnets. How much do {c} books and {d} magnets cost?",
            "k", 3, 1, 2, 4, 4, 1,
            "The Brooklyn Bridge in New York opened in 1883. It was the longest suspension "
            "bridge in the world at the time.",
            guided=True),
        eq_problem(
            ("mug", "mugs", "sticker", "stickers"),
            "Amina buys {a} mugs and {b} stickers for ${T}. One mug costs the same as {k} "
            "stickers. How much do {c} mug and {d} stickers cost?",
            "k", 2, 3, 3, 3, 1, 4,
            "Some Roman arch bridges are still standing after almost 2,000 years."),
        eq_problem(
            ("model", "models", "postcard", "postcards"),
            "Yusra buys {a} models and {b} postcards for ${T}. One model costs the same as "
            "{k} postcards. How much do {c} models and {d} postcards cost?",
            "k", 2, 3, 5, 2, 3, 2,
            "The Ponte Vecchio in Florence, Italy, was rebuilt in 1345. It still has shops "
            "built along both sides of the bridge."),
        eq_problem(
            ("puzzle", "puzzles", "ticket", "tickets"),
            "Idris buys {a} puzzles and {b} tickets for ${T}. One puzzle costs the same as "
            "{k} tickets. How much do {c} puzzles and {d} tickets cost?",
            "k", 5, 2, 2, 3, 2, 6,
            "The Millau Viaduct in France is taller than the Eiffel Tower at its highest "
            "tower."),
        eq_problem(
            ("toy", "toys", "cap", "caps"),
            "Layla buys {a} toys and {b} caps for ${T}. One toy costs ${e} more than one cap. "
            "How much do {c} toys and {d} cap cost?",
            "more", 2, 4, 3, 4, 3, 1,
            "The Akashi Kaikyo Bridge in Japan has the longest central span of any "
            "suspension bridge, about 2 kilometers."),
    ],
}

ALL = [DAY1, TRADE_DAY1, DAY1_B, TRADE_DAY1_B,
       UNDO_DAY2, TRADE_DAY2, UNDO_DAY2_B, TRADE_DAY2_B]
