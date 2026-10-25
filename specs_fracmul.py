"""specs_fracmul.py -- raw numbers for the simple-fraction MULTIPLICATION practice set (kid2).

Asif, 2026-10-25: "can we add a fraction set for kid2? He needs to practice multiplying
simple fractions." Khan 5th "Multiply fractions" / IM Grade 5.

This file holds ONLY raw numbers and prose templates. build_fracmul.py renders them;
verify_fracmul.py recomputes every answer from these numbers with fractions.Fraction.
A fraction is a (numerator, denominator) tuple; a whole number is (n, 1).

Rules the verifier enforces: denominators 2-10, no factor equal to 1 or 0, no fraction
equal to 1, and every printed answer in simplest form (mixed number when improper).
"""

SPEC = {
    "kid": "kid2",
    "file": "worksheet-focus-2026-10-25-fracmul.html",
    "key_file": "worksheet-focus-2026-10-25-fracmul-key.html",
    "date": "October 25, 2026",
    "title_plain": "Multiply Fractions",
    "title": "Multiply Fractions",
    "sub": "Glass &amp; mirrors: tops times tops, bottoms times bottoms, then simplify. One step per line.",
    # Worked example at the top of page 1 (numbers are NOT reused in Part A or B).
    "example": {"fraction": [(2, 5), (3, 4)], "whole": [(3, 1), (3, 4)]},
    # Part A: bare drill. "group" is only a label for the verifier's coverage check.
    "part_a": [
        {"group": "unit", "f": [(1, 2), (1, 3)]},
        {"group": "unit", "f": [(1, 4), (1, 5)]},
        {"group": "unit", "f": [(1, 5), (1, 3)]},
        {"group": "proper", "f": [(2, 3), (3, 4)]},
        {"group": "proper", "f": [(3, 5), (2, 7)]},
        {"group": "proper", "f": [(4, 9), (3, 8)]},
        {"group": "proper", "f": [(5, 6), (3, 10)]},
        {"group": "proper", "f": [(4, 7), (7, 8)]},
        {"group": "whole", "f": [(4, 1), (2, 3)]},
        {"group": "whole", "f": [(6, 1), (3, 4)]},
        {"group": "whole", "f": [(3, 10), (5, 1)]},
        {"group": "whole", "f": [(9, 1), (5, 6)]},
    ],
    # Part B: compound word problems. "kind" picks the formula in BOTH the builder
    # (for the key's worked lines) and the verifier (own copy, from these numbers).
    "part_b": [
        {"kind": "fof_left", "p": (3, 4), "q": (2, 3),
         "story": "Amina is a glassblower. Her furnace pot is {p} full of melted glass. She pours "
                  "{q} of the glass in the pot into a vase mold. What fraction of the WHOLE pot "
                  "is still left in the pot?",
         "unit": "of the pot",
         "fact": "A glass furnace can top 1,500 degrees Celsius, hot enough to melt sand. "
                 "Sand is what most glass is made from.",
         "watch": "Step 1 is fraction x fraction (the vase part). Step 2 is a subtraction from "
                  "the {p} she started with; that needs a common denominator. If she subtracts "
                  "{q} from {p} right away, she skipped the multiplying."},
        {"kind": "whole_chain", "total": 36, "f1": (2, 3), "f2": (3, 4),
         "story": "Omar sells mirrors. One crate holds {total} mirrors. {f1} of them have gold "
                  "frames. He hangs {f2} of the gold-framed mirrors in his shop window. How many "
                  "mirrors hang in the window?",
         "unit": "mirrors",
         "fact": "About 8,000 years ago, people in what is now Turkey polished black volcanic "
                 "glass, called obsidian, into the first mirrors.",
         "watch": "Step 2 must start from the gold-framed mirrors, not from all {total}. Answer "
                  "{total} x {f2} = 27 means he skipped the first fraction."},
        {"kind": "area", "l": (3, 4), "w": (2, 5), "n": 4,
         "story": "Idris cuts a rectangular pane of glass for a lamp. It is {l} meter long and "
                  "{w} meter wide. He cuts {n} panes the same size. How many square meters of "
                  "glass is that in all?",
         "unit": "square meters",
         "fact": "Ibn al-Haytham of Basra wrote his Book of Optics over 1,000 years ago. He "
                 "showed that we see because light bounces off things and into our eyes.",
         "watch": "Area = length x width (multiply, do not add). Then x {n}: the answer is "
                  "bigger than 1, so it should be a mixed number."},
    ],
}

ALL = [SPEC]
