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
            guided=["Arrows: ? &rarr; &times;4 &rarr; " + BLANK + " &rarr; &minus;7 &rarr; 29",
                    "Undo the LAST arrow first. 29 <b>+ 7</b> = " + BLANK,
                    "Now undo the first arrow. " + BLANK + " <b>&divide; 4</b> = " + BLANK,
                    "Check it forward: " + BLANK + " &times; 4 &minus; 7 = 29 ?"],
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
    ],
}

ALL = [DAY1]
