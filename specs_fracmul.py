"""specs_fracmul.py -- raw numbers for the kid2 fraction packet: 10 multiply + 10 add/subtract.

Asif, 2026-10-25: "can we add a fraction set for kid2? He needs to practice multiplying
simple fractions", then "print out practice combining 10 fraction multiplication And 10
different addition and subtraction." ONE packet of exactly 20 problems, numbered 1-20.
Khan 5th "Multiply fractions" / IM Grade 5; add/subtract is unlike-denominator review.

This file holds ONLY raw numbers and prose templates. build_fracmul.py renders them;
verify_fracmul.py recomputes every answer from these numbers with fractions.Fraction.
A fraction is a (numerator, denominator) tuple; a whole number is (n, 1).

Rules the verifier enforces: multiply denominators 2-10, add/subtract denominators 2-12,
no factor equal to 0 or 1, no fraction equal to 1, add/subtract results > 0, and every
printed answer in simplest form (mixed number when improper).
"""

SPEC = {
    "kid": "kid2",
    "file": "worksheet-focus-2026-10-25-fractions.html",
    "key_file": "worksheet-focus-2026-10-25-fractions-key.html",
    "date": "October 25, 2026",
    "title_plain": "Fraction Practice",
    "title": "Fraction Practice",
    "sub": "Glass &amp; mirrors: multiply, then add and subtract. One step per line.",
    # Worked examples (numbers are NOT reused in the problems).
    "mul_example": {"fraction": [(2, 5), (3, 4)], "whole": [(3, 1), (3, 4)]},
    "as_example": {"add": [(2, 3), (3, 4)], "sub": [(7, 10), (1, 6)]},
    # Multiply, problems 1-7. "group" is only a label for the verifier's coverage check.
    "mul_bare": [
        {"group": "unit", "f": [(1, 2), (1, 3)]},
        {"group": "unit", "f": [(1, 4), (1, 5)]},
        {"group": "proper", "f": [(2, 3), (3, 4)]},
        {"group": "proper", "f": [(3, 5), (2, 7)]},
        {"group": "proper", "f": [(4, 9), (3, 8)]},
        {"group": "whole", "f": [(4, 1), (2, 3)]},
        {"group": "whole", "f": [(9, 1), (5, 6)]},
    ],
    # Multiply word problems, 8-10. "kind" picks the formula in BOTH the builder
    # (for the key's worked lines) and the verifier (own copy, from these numbers).
    "mul_word": [
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
    # Add and subtract, problems 11-17. "op" is "+" or "-".
    "as_bare": [
        {"group": "like", "op": "+", "f": [(5, 8), (7, 8)]},
        {"group": "like", "op": "-", "f": [(11, 12), (5, 12)]},
        {"group": "unlike", "op": "+", "f": [(2, 5), (1, 3)]},
        {"group": "unlike", "op": "-", "f": [(5, 6), (3, 8)]},
        {"group": "unlike", "op": "+", "f": [(3, 4), (5, 6)]},
        {"group": "unlike", "op": "-", "f": [(7, 10), (1, 4)]},
        {"group": "unlike", "op": "+", "f": [(3, 10), (1, 6)]},
    ],
    # Add/subtract word problems, 18-20. "kind" picks the formula (builder + verifier).
    "as_word": [
        {"kind": "left_of_whole", "a": (1, 3), "b": (1, 4),
         "story": "Zainab paints a wooden mirror frame. On Monday she paints {a} of the frame. "
                  "On Tuesday she paints {b} more of the frame. What fraction of the frame is "
                  "still not painted?",
         "unit": "of the frame",
         "fact": "Glass can be melted down and made into new glass again and again. "
                 "That is why glass is easy to recycle.",
         "watch": "Step 1 is an addition with unlike bottoms. Step 2 subtracts from the WHOLE "
                  "frame, which is 1 = 12/12. An answer of {a} + {b} = 7/12 stops after step 1."},
        {"kind": "left_of_total", "t": (11, 12), "a": (1, 4), "b": (1, 6),
         "story": "Hamza has {t} of a meter of silver trim. He uses {a} of a meter on one mirror "
                  "and {b} of a meter on another mirror. How much trim is left?",
         "unit": "of a meter",
         "fact": "A mirror is a sheet of glass with a thin shiny layer of metal on the back. "
                 "The metal is what bounces the light back to your eyes.",
         "watch": "Find how much he used in all first ({a} + {b}), then subtract that from {t}. "
                  "The answer 6/12 must be simplified."},
        {"kind": "add_then_sub", "a": (7, 8), "b": (2, 3), "c": (1, 2),
         "story": "Kareem mixes {a} liter of blue glaze with {b} liter of green glaze in a bowl. "
                  "He pours {c} liter of the mix onto a glass vase. How much glaze is left in "
                  "the bowl?",
         "unit": "liters",
         "fact": "Hot glass is soft and gooey, so a glassblower can blow into a tube "
                 "and stretch it into a bubble, like a balloon.",
         "watch": "Step 1 gives an improper fraction, 37/24 (more than 1 liter). Subtract {c} "
                  "from it, then write the answer as a mixed number."},
    ],
}

ALL = [SPEC]
