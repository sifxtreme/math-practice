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

ALL = [DAY1, TRADE_DAY1, DAY1_B, TRADE_DAY1_B]
