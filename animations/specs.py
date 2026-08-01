"""Step-by-step algorithm simulators for the drill animations.

Every number on screen is produced HERE, by running the actual algorithm --
nothing is typed by hand. `verify_animations.py` re-derives the same values a
second, independent way and asserts they match.

Each step carries THREE things:

  say   -- what to do: the instruction, the mark you make
  why   -- what the mark actually MEANS in place value. This is the part the
           standard algorithm hides. That carry is not a 4, it is 40. That 6 in
           the quotient is not a 6, it is 600. The 42 you write under 4231 is
           really 4200. A kid who can run the algorithm but cannot say these
           sentences is executing, not understanding.
  trap  -- the specific wrong answer waiting at this step

and each animation carries a `model`: the same calculation drawn a second way
(an area rectangle for multiplication, a partial-quotients ladder for division)
that the steps highlight in sync. Common Core 4.NBT.B.5 asks for exactly this --
"illustrate and explain the calculation by using ... rectangular arrays and/or
area models" -- and it is what makes the placeholder zero have a reason.

Grid model (1-based, matches CSS grid):
    column 1        = the operator / divisor gutter
    columns 2..W+1  = digit places, left to right (W = width of the widest number)
Helper `col(j)` maps "j places from the right" to a grid column, so j=0 is always
the ones column.

A "token" is one written mark: {k: key, r: row, c: col, t: text, cls: style}.
Steps reveal tokens by key. Reveal is cumulative and recomputed from scratch on
every step change, which is what makes the Back button work.
"""

PLACE = ["ones", "tens", "hundreds", "thousands", "ten-thousands"]


def _digits(n):
    return [int(ch) for ch in str(n)]


def _spell(n):
    return {0: "no", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}.get(n, str(n))


def _trials(cur, divisor, q):
    """The candidates a kid actually has to weigh at the D step, with the verdict on
    each. "Too small" is the one that gets skipped in teaching and it is the one that
    matters: a digit is too small when the LEFTOVER would still hold another divisor."""
    lo, hi = (1, 1) if q == 0 else (max(1, q - 1), min(9, q + 1))
    rows = []
    for n in range(lo, hi + 1):
        prod = n * divisor
        v = "big" if prod > cur else ("small" if cur - prod >= divisor else "fits")
        row = {"n": n, "prod": prod, "v": v}
        if v == "fits":
            row["part"] = 0        # the digit that flies up to the quotient
        rows.append(row)
    return rows


# ------------------------------------------------- multi-digit x 1 digit

def mult_by_one_digit(top, bot):
    """Standard algorithm, e.g. 247 x 6. Carries are written on the shelf row."""
    assert 0 < bot < 10, "this layout is for a single-digit multiplier"
    tdig = _digits(top)
    product = top * bot
    W = len(str(product))
    col = lambda j: W + 1 - j          # j places from the right -> grid column
    R_CARRY, R_TOP, R_BOT, R_RULE, R_ANS = 1, 2, 3, 4, 5

    toks, steps = [], []
    for j, d in enumerate(reversed(tdig)):
        toks.append({"k": f"t{j}", "r": R_TOP, "c": col(j), "t": str(d), "cls": "d"})
    toks.append({"k": "op", "r": R_BOT, "c": 1, "t": "×", "cls": "op"})
    toks.append({"k": "b0", "r": R_BOT, "c": col(0), "t": str(bot), "cls": "d hot"})

    decor = [{"kind": "rule", "k": "rule1", "r": R_RULE, "c0": 1, "c1": W + 1}]

    # --- the area model: one strip per digit of the top number
    strips = []
    for j, d in enumerate(reversed(tdig)):
        if d or j == 0:
            strips.append({"w": d * 10 ** j, "area": bot * d * 10 ** j, "j": j})
    strips.reverse()                    # draw biggest place first, left to right
    model = {
        "kind": "area", "h": bot,
        "rows": [{"v": bot, "maps": None}],
        "cols": [{"v": s["w"]} for s in strips],
        "cells": [{"r": 0, "c": i, "v": s["area"], "j": s["j"]}
                  for i, s in enumerate(strips)],
        "total": product,
        "caption": f"{top} × {bot} — a rectangle {bot} tall, sliced by place value. "
                   f"The slices are {' + '.join(str(s['area']) for s in strips)} = {product}, "
                   f"and the algorithm is just those slices folded into columns.",
    }

    setup_keys = [f"t{j}" for j in range(len(tdig))] + ["op", "b0", "rule1"]
    steps.append({
        "label": "SET UP", "beat": None,
        "say": f"Stack them so the <b>ones line up</b>. The {bot} on the bottom is going to "
               f"visit every digit on top, one at a time, <b>starting from the right</b>.",
        "why": f"Lining up the ones column is not neatness — it is what keeps each digit "
               f"standing for the right amount. In {top} the {tdig[0]} is not a {tdig[0]}, "
               f"it is <b>{tdig[0] * 10 ** (len(tdig)-1)}</b>.",
        "show": setup_keys, "flash": ["b0"], "dwell": 3.6, "modelCell": None,
    })

    carry = 0
    strip_index = {s["j"]: i for i, s in enumerate(strips)}
    for j, d in enumerate(reversed(tdig)):
        raw = bot * d
        total = raw + carry
        last = (j == len(tdig) - 1)
        real_d = d * 10 ** j
        digits = list(str(total))

        # The chip is a little expression, not just an answer. When a carry is coming
        # in it has to show `12 + 2 = 14`, because otherwise the 14 arrives out of
        # nowhere -- the kid sees a 6, a 2 and a carry, and then a number that has no
        # visible parentage. Only the cells of the TOTAL carry a `part`; those are the
        # ones that fly out when it splits.
        totcells = [{"t": ch, "part": i} for i, ch in enumerate(digits)]
        if carry:
            chip_first = [{"t": ch} for ch in str(raw)]
            chip_full = ([{"t": ch} for ch in str(raw)]
                         + [{"t": "+", "op": True},
                            {"t": str(carry), "arrive": f"cy{j-1}"},
                            {"t": "=", "op": True}] + totcells)
        else:
            chip_first = chip_full = totcells
        # width of the widest state this chip will reach, so all three beats sit in
        # the same place instead of the chip hopping when the expression grows
        reserve = sum(22 if c.get("op") else 30 for c in chip_full) + 32

        # ---------- beat 1: the multiplication, on its own
        steps.append({
            "label": f"{bot} × {d}", "beat": None,
            "say": f"<b>{bot} × {d} = {raw}.</b>",
            "why": ((f"<b>{raw} ones.</b> But a column only holds <i>one</i> digit — "
                     f"{raw} cannot all stay here. Watch where each half goes next."
                     if raw >= 10 else
                     f"<b>{raw} ones</b>, and that fits in a single column.")
                    if j == 0 else
                    f"That {d} is really <b>{real_d}</b>, so this move is really "
                    f"<b>{bot} × {real_d} = {raw * 10 ** j}</b>."),
            "show": [], "flash": ["b0", f"t{j}"], "bubble": {"cells": chip_first, "reserveW": reserve},
            "modelCell": strip_index.get(j), "dwell": 3.8,
        })

        # ---------- beat 2 (only when there IS one): the carry comes down and joins in
        if carry:
            steps.append({
                "label": "+ THE CARRY", "beat": None,
                "say": f"Now bring in the carry from the last column: "
                       f"<b>{raw} + {carry} = {total}</b>.",
                "why": f"That carry is not a {carry} — it is <b>{carry * 10 ** j}</b>. "
                       f"It came from the column on the right, where it did not fit, and "
                       f"this is the column where it belongs.",
                "show": [], "flash": [f"cy{j-1}"],
                "bubble": {"cells": chip_full, "grewFrom": len(chip_first), "reserveW": reserve},
                "trap": (f"<b>Multiply first, then add.</b> Doing it backwards — "
                         f"{d} + {carry} = {d+carry}, then {d+carry} × {bot} = "
                         f"{(d+carry)*bot} — is the mistake almost everybody makes here."),
                "modelCell": strip_index.get(j), "dwell": 5.0,
            })

        # ---------- beat 3: where each digit of the total goes
        show, split = [], []
        if last:
            for i, ch in enumerate(reversed(digits)):
                toks.append({"k": f"a{j+i}", "r": R_ANS, "c": col(j + i), "t": ch, "cls": "d ans"})
                show.append(f"a{j+i}")
                split.append({"part": len(digits) - 1 - i, "to": f"a{j+i}"})
            if len(digits) > 1:
                say2 = (f"Nothing left to multiply, so <b>both digits go down</b> — the "
                        f"<b>{digits[0]}</b> into the {PLACE[j+1]} column and the "
                        f"<b>{digits[1]}</b> into the {PLACE[j]} column.")
                why2 = (f"<b>{total * 10 ** j}</b> = {int(digits[0]) * 10 ** (j+1)} + "
                        f"{int(digits[1]) * 10 ** j}. Each digit sits in the column that "
                        f"gives it the right size.")
            else:
                say2 = f"Write the <b>{total}</b> in the {PLACE[j]} column."
                why2 = f"That {total} is really <b>{total * 10 ** j}</b>."
        elif total >= 10:
            ones, tens = total % 10, total // 10
            toks.append({"k": f"a{j}", "r": R_ANS, "c": col(j), "t": str(ones), "cls": "d ans"})
            toks.append({"k": f"cy{j}", "r": R_CARRY, "c": col(j + 1), "t": str(tens), "cls": "carry"})
            show += [f"a{j}", f"cy{j}"]
            split = [{"part": 1, "to": f"a{j}"}, {"part": 0, "to": f"cy{j}"}]
            say2 = (f"<b>{total}</b> is two digits and only one fits in a box. "
                    f"The <b>{ones}</b> drops <b>down</b> into the {PLACE[j]} column. "
                    f"The <b>{tens}</b> flies <b>up</b> to the shelf above the next column.")
            why2 = (f"Split it by size: <b>{total * 10 ** j} = {ones * 10 ** j} + "
                    f"{tens * 10 ** (j+1)}</b>. The {ones * 10 ** j} fits in the {PLACE[j]} "
                    f"column. The {tens * 10 ** (j+1)} does not — so it moves one column left, "
                    f"to where {tens * 10 ** (j+1)} belongs. That is all a carry is.")
        else:
            toks.append({"k": f"a{j}", "r": R_ANS, "c": col(j), "t": str(total), "cls": "d ans"})
            show.append(f"a{j}")
            split = [{"part": 0, "to": f"a{j}"}]
            say2 = f"<b>{total}</b> is one digit, so it drops straight down into the {PLACE[j]} column."
            why2 = f"That {total} is really <b>{total * 10 ** j}</b>, and nothing needs to move left."

        steps.append({
            "label": "WHERE IT GOES", "beat": None, "say": say2, "why": why2,
            "show": show, "flash": [], "bubble": {"cells": chip_full, "reserveW": reserve}, "split": split,
            "modelCell": strip_index.get(j), "dwell": 4.4,
        })
        carry = 0 if last else total // 10

    # One reserved width for the whole animation, so the chip appears in the same
    # spot every time instead of moving between digit groups.
    _mx = max((st["bubble"]["reserveW"] for st in steps if st.get("bubble")), default=0)
    for st in steps:
        if st.get("bubble"):
            st["bubble"]["reserveW"] = _mx

    rough = round(top, -1)
    steps.append({
        "label": "CHECK", "beat": None,
        "say": f"<b>{top} × {bot} = {product}.</b> Now check it's sensible: {top} is about "
               f"{rough}, and {rough} × {bot} = {rough*bot}. {product} is right next to it. ✓",
        "why": f"And the slices agree: {' + '.join(str(s['area']) for s in strips)} = "
               f"<b>{product}</b>. The columns and the rectangle are the same calculation.",
        "show": [], "flash": [f"a{j}" for j in range(W)], "dwell": 5.4, "modelCell": "all",
    })

    return {"cols": W + 1, "rows": 5, "toks": toks, "decor": decor, "steps": steps,
            "model": model, "answer": product}


# ------------------------------------------------- 2 digit x 2 digit

def mult_two_by_two(top, bot):
    """Standard algorithm with two partial products and the placeholder zero."""
    assert 10 <= bot < 100, "this layout is for a two-digit multiplier"
    tdig = _digits(top)
    b_ones, b_tens = bot % 10, bot // 10
    p1 = top * b_ones
    p2 = top * b_tens * 10
    product = top * bot
    W = len(str(product))
    col = lambda j: W + 1 - j
    R_CARRY, R_TOP, R_BOT, R_RULE1, R_P1, R_P2, R_RULE2, R_ANS = 1, 2, 3, 4, 5, 6, 7, 8

    toks, steps = [], []
    for j, d in enumerate(reversed(tdig)):
        toks.append({"k": f"t{j}", "r": R_TOP, "c": col(j), "t": str(d), "cls": "d"})
    toks.append({"k": "op", "r": R_BOT, "c": 1, "t": "×", "cls": "op"})
    toks.append({"k": "bo", "r": R_BOT, "c": col(0), "t": str(b_ones), "cls": "d hot"})
    toks.append({"k": "bt", "r": R_BOT, "c": col(1), "t": str(b_tens), "cls": "d hot2"})
    toks.append({"k": "plus", "r": R_P2, "c": 1, "t": "+", "cls": "op"})

    decor = [
        {"kind": "rule", "k": "rule1", "r": R_RULE1, "c0": 1, "c1": W + 1},
        {"kind": "rule", "k": "rule2", "r": R_RULE2, "c0": 1, "c1": W + 1},
    ]

    # --- the area model: a 2x2 grid whose ROWS are the two written answer rows
    tcols = []
    for j, d in enumerate(reversed(tdig)):
        if d or j == 0:
            tcols.append(d * 10 ** j)
    tcols.reverse()
    cells, model_rows = [], [{"v": b_tens * 10, "maps": "p2"}, {"v": b_ones, "maps": "p1"}]
    for ri, r in enumerate(model_rows):
        for ci, cv in enumerate(tcols):
            cells.append({"r": ri, "c": ci, "v": r["v"] * cv})
    model = {
        "kind": "area", "h": bot,
        "rows": model_rows, "cols": [{"v": v} for v in tcols], "cells": cells,
        "rowSums": [p2, p1], "total": product,
        "caption": f"{top} × {bot} as a rectangle. The bottom strip is the <b>{b_ones}</b> — "
                   f"that is written row 1, {p1}. The top strip is the <b>{b_tens*10}</b>, not the "
                   f"{b_tens} — that is written row 2, <b>{p2}</b>. It ends in 0 because every "
                   f"multiple of {b_tens*10} does.",
    }

    setup = [f"t{j}" for j in range(len(tdig))] + ["op", "bo", "bt", "rule1"]
    steps.append({
        "label": "SET UP", "beat": None,
        "say": f"Two digits on the bottom means <b>two rounds</b>, so you get <b>two answer rows</b> "
               f"and then you add them. Round 1 uses the <b>{b_ones}</b>. Round 2 uses the "
               f"<b>{b_tens}</b> — and that one has a catch.",
        "why": f"The catch, up front: in {bot} the {b_tens} is not a {b_tens}. It sits in the tens "
               f"column, so it is <b>{b_tens*10}</b>. Round 2 is really <b>{b_tens*10} × {top}</b>, "
               f"and that is where the 0 comes from.",
        "show": setup, "flash": ["bo", "bt"], "dwell": 5.0, "modelRow": None,
    })

    def digit_beats(mult, d, carry, j, last, slot, ans_row, ans_pre, carry_pre,
                    hot_key, mrow, tens_scale):
        """Beats for one digit of a round: the multiplication, then (if a carry is
        coming in) the carry joining it, then where each half of the total goes. The
        chip has to show `12 + 2 = 14` or the 14 has no visible parentage."""
        raw = mult * d
        total = raw + carry
        digits = list(str(total))
        totcells = [{"t": ch, "part": i} for i, ch in enumerate(digits)]
        if carry:
            chip_first = [{"t": ch} for ch in str(raw)]
            chip_full = ([{"t": ch} for ch in str(raw)]
                         + [{"t": "+", "op": True},
                            {"t": str(carry), "arrive": f"{carry_pre}{j-1}"},
                            {"t": "=", "op": True}] + totcells)
        else:
            chip_first = chip_full = totcells
        reserve = sum(22 if c.get("op") else 30 for c in chip_full) + 32

        steps.append({
            "label": f"{mult} × {d}", "beat": None,
            "say": f"<b>{mult} × {d} = {raw}.</b>",
            "why": (f"<b>{raw}</b> — and a column holds one digit, so watch where each "
                    f"half of it goes."
                    if (j == 0 and tens_scale == 1 and raw >= 10) else
                    f"Really <b>{mult * tens_scale} × {d * 10 ** j} = "
                    f"{raw * 10 ** j * tens_scale}</b>."),
            "show": [], "flash": [hot_key, f"t{j}"], "bubble": {"cells": chip_first, "reserveW": reserve},
            "modelRow": mrow, "dwell": 3.6,
        })

        if carry:
            steps.append({
                "label": "+ THE CARRY", "beat": None,
                "say": f"Now bring in the carry: <b>{raw} + {carry} = {total}</b>.",
                "why": f"The carry came from the column on the right, where it did not "
                       f"fit. This is the column it belongs in.",
                "show": [], "flash": [f"{carry_pre}{j-1}"],
                "bubble": {"cells": chip_full, "grewFrom": len(chip_first), "reserveW": reserve},
                "trap": (f"<b>Multiply first, then add the carry.</b> Not "
                         f"{d} + {carry} = {d+carry}, then × {mult} = {(d+carry)*mult}."),
                "modelRow": mrow, "dwell": 4.8,
            })

        show, split = [], []
        if last:
            for i, ch in enumerate(reversed(digits)):
                k = f"{ans_pre}{slot+i}"
                toks.append({"k": k, "r": ans_row, "c": col(slot + i), "t": ch,
                             "cls": f"d {ans_pre[:2]}"})
                show.append(k)
                split.append({"part": len(digits) - 1 - i, "to": k})
            say2 = (f"Nothing left on top, so <b>both digits go down</b>."
                    if len(digits) > 1 else f"Write the <b>{total}</b>.")
            why2 = (f"<b>{total}</b> lands across two columns because that is where its "
                    f"two place values belong.") if len(digits) > 1 else "One digit, one column."
        elif total >= 10:
            ones, tens = total % 10, total // 10
            k_ans, k_car = f"{ans_pre}{slot}", f"{carry_pre}{j}"
            toks.append({"k": k_ans, "r": ans_row, "c": col(slot), "t": str(ones),
                         "cls": f"d {ans_pre[:2]}"})
            toks.append({"k": k_car, "r": R_CARRY, "c": col(j + 1), "t": str(tens),
                         "cls": "carry" + (" carry2" if carry_pre == "cB" else "")})
            show += [k_ans, k_car]
            split = [{"part": 1, "to": k_ans}, {"part": 0, "to": k_car}]
            say2 = (f"<b>{total}</b> is two digits and only one fits in a box. The "
                    f"<b>{ones}</b> drops <b>down</b>; the <b>{tens}</b> flies <b>up</b> "
                    f"to the shelf above the next column.")
            why2 = (f"The part that does not fit moves one column left, which is the only "
                    f"thing a carry ever is.")
        else:
            k_ans = f"{ans_pre}{slot}"
            toks.append({"k": k_ans, "r": ans_row, "c": col(slot), "t": str(total),
                         "cls": f"d {ans_pre[:2]}"})
            show.append(k_ans)
            split = [{"part": 0, "to": k_ans}]
            say2 = f"<b>{total}</b> is one digit — it drops straight down."
            why2 = "Nothing needs to move left."

        steps.append({
            "label": "WHERE IT GOES", "beat": None, "say": say2, "why": why2,
            "show": show, "flash": [], "bubble": {"cells": chip_full, "reserveW": reserve}, "split": split,
            "modelRow": mrow, "dwell": 4.2,
        })
        return 0 if last else total // 10

    # ---- round 1: the ones digit
    carry = 0
    for j, d in enumerate(reversed(tdig)):
        carry = digit_beats(b_ones, d, carry, j, j == len(tdig) - 1, j,
                            R_P1, "p1_", "cA", "bo", 1, 1)

    carriesA = [t["k"] for t in toks if t["k"].startswith("cA")]
    steps.append({
        "label": "ROW 1 DONE", "beat": None,
        "say": f"Row 1 is finished: <b>{p1}</b>. That is <b>{b_ones} × {top}</b>.",
        "why": f"On the rectangle that is the <b>bottom strip</b> — {b_ones} tall, {top} wide, "
               f"area <b>{p1}</b>.",
        "show": [], "flash": [f"p1_{i}" for i in range(len(str(p1)))], "dwell": 3.4, "modelRow": 1,
    })
    if carriesA:
        steps.append({
            "label": "CROSS OUT", "beat": None,
            "say": "Before round 2, <b>cross out the carries</b> from round 1. They belong to that "
                   "row and nothing else.",
            "why": "They were tens and hundreds borrowed inside round 1's calculation. Round 2 is "
                   "a different calculation; those amounts are already spent.",
            "show": [], "flash": [], "strike": carriesA, "dwell": 3.8, "modelRow": 1,
            "trap": "Leaving them there is a quiet disaster — you add them a second time in "
                    "round 2 and the answer comes out wrong with no obvious sign of why.",
        })

    # ---- round 2: the tens digit, starting with the placeholder zero
    toks.append({"k": "zero", "r": R_P2, "c": col(0), "t": "0", "cls": "d p2 zero"})
    steps.append({
        "label": "THE ZERO", "beat": None,
        "say": f"Round 2 uses the <b>{b_tens}</b> — but it is <b>not {b_tens}</b>. It sits in the "
               f"tens column, so it is really <b>{b_tens*10}</b>. Before you multiply anything, "
               f"<b>put a 0 in the ones column</b> of row 2.",
        "why": f"Look at the rectangle: the top strip is <b>{b_tens*10} × {top} = {p2}</b>. Every "
               f"multiple of {b_tens*10} ends in 0, so row 2 <i>has</i> to end in 0. You are not "
               f"adding a magic zero — you are writing down where the number actually is.",
        "show": ["plus", "zero"], "flash": ["bt", "zero"], "dwell": 6.0, "modelRow": 0,
        "trap": f"<b>This is the single most common way to get a 2-digit × 2-digit wrong.</b> "
                f"Skip the 0 and you add {p1} + {p2//10} = {p1 + p2//10} instead of "
                f"{p1} + {p2} = {product}.",
    })

    carry = 0
    for j, d in enumerate(reversed(tdig)):
        carry = digit_beats(b_tens, d, carry, j, j == len(tdig) - 1, j + 1,
                            R_P2, "p2_", "cB", "bt", 0, 10)

    steps.append({
        "label": "ROW 2 DONE", "beat": None,
        "say": f"Row 2 is <b>{p2}</b>, which is <b>{b_tens*10} × {top}</b>. See how the 0 made it "
               f"ten times bigger than {p2//10}? That is what the 0 is for.",
        "why": f"Top strip of the rectangle: <b>{p2}</b>. Bottom strip: <b>{p1}</b>. Two strips, "
               f"two written rows — same thing drawn two ways.",
        "show": ["rule2"], "flash": [], "dwell": 4.8, "modelRow": 0,
    })

    ans_keys = []
    for i, ch in enumerate(reversed(str(product))):
        toks.append({"k": f"a{i}", "r": R_ANS, "c": col(i), "t": ch, "cls": "d ans"})
        ans_keys.append(f"a{i}")
    steps.append({
        "label": "ADD", "beat": None,
        "say": f"Last move: <b>add the two rows</b>. {p1} + {p2} = <b>{product}</b>.",
        "why": f"Which is the whole rectangle: <b>{p2} + {p1} = {product}</b>.",
        "show": ans_keys, "flash": ans_keys, "dwell": 3.8, "modelRow": "all",
    })

    # One reserved width for the whole animation, so the chip appears in the same
    # spot every time instead of moving between digit groups.
    _mx = max((st["bubble"]["reserveW"] for st in steps if st.get("bubble")), default=0)
    for st in steps:
        if st.get("bubble"):
            st["bubble"]["reserveW"] = _mx

    r_top = round(top, -1)
    steps.append({
        "label": "CHECK", "beat": None,
        "say": f"Sense-check: {top} is about {r_top}, so the answer should land near "
               f"{r_top} × {bot} = {r_top*bot}. We got <b>{product}</b>. ✓",
        "why": f"All four little areas: "
               f"{' + '.join(str(c['v']) for c in cells)} = <b>{product}</b>.",
        "show": [], "flash": ans_keys, "dwell": 5.4, "modelRow": "all",
    })

    return {"cols": W + 1, "rows": 8, "toks": toks, "decor": decor, "steps": steps,
            "model": model, "answer": product}


# ------------------------------------------------- long division

def long_division(dividend, divisor):
    """Long division with a remainder: D-M-S-B, one written mark at a time."""
    assert 0 < divisor < 10, "this layout is for a single-digit divisor"
    assert dividend >= divisor, "the quotient would be zero; not a drill shape"
    ddig = _digits(dividend)
    W = len(ddig)
    col = lambda j: W + 1 - j                      # j places from the right
    dcol = lambda i: i + 2                         # i-th dividend digit (0 = leftmost)
    pv = lambda i: 10 ** (W - 1 - i)               # place value of quotient digit at i
    R_Q, R_DIV = 1, 2

    toks, steps, decor = [], [], []
    for i, d in enumerate(ddig):
        toks.append({"k": f"n{i}", "r": R_DIV, "c": dcol(i), "t": str(d), "cls": "d"})
    toks.append({"k": "dv", "r": R_DIV, "c": 1, "t": str(divisor), "cls": "d hot"})
    decor.append({"kind": "bracket", "k": "brk", "r": R_DIV, "c0": 2, "c1": W + 1})

    quotient, remainder = divmod(dividend, divisor)

    setup = ["dv", "brk"] + [f"n{i}" for i in range(W)]
    steps.append({
        "label": "SET UP", "beat": None,
        "say": f"<b>{dividend}</b> goes inside the house, <b>{divisor}</b> stands outside. "
               f"Then you repeat four moves, in this order, forever: "
               f"<b>Divide → Multiply → Subtract → Bring down.</b>",
        "why": f"The real question underneath all of it: <b>how many {divisor}s fit inside "
               f"{dividend}?</b> You chip away at it a place value at a time — hundreds first, "
               f"then tens, then ones — instead of counting {divisor}s one by one.",
        "show": setup, "flash": ["dv"], "dwell": 5.0, "modelRow": None,
    })

    row = 3
    cur, cur_start = 0, 2
    cur_keys = []
    started = False
    q_written = []
    ladder, k_index = [], 0

    for i, d in enumerate(ddig):
        if i == 0:
            cur, cur_start, cur_keys = d, dcol(0), ["n0"]

        if not started and cur < divisor:
            steps.append({
                "label": "TOO SMALL", "beat": None,
                "say": f"How many <b>{divisor}</b>s fit in <b>{cur}</b>? <b>None</b> — {divisor} is "
                       f"bigger than {cur}. So you write <i>nothing</i> above the {cur} and take one "
                       f"more digit: look at <b>{cur*10 + ddig[i+1]}</b> instead.",
                "why": f"Asked properly: are there any <b>{pv(i)}</b>-sized groups of {divisor} in "
                       f"{dividend}? {divisor} × {pv(i)} = {divisor * pv(i)}, which is more than "
                       f"{dividend}. So the answer has no {PLACE[W-1-i]} digit at all — and a "
                       f"leading zero would just be writing 'none' where nothing needs writing.",
                "show": [], "flash": [f"n{i}", f"n{i+1}"], "dwell": 5.6, "modelRow": None,
                "bubble": {"trials": _trials(cur, divisor, 0), "cur": cur,
                           "divisor": divisor, "reserveW": 232},
                "trap": "A zero at the <b>front</b> of the answer is the one zero you skip. A zero in "
                        "the <b>middle</b> you must write. Those are different, and mixing them up is "
                        "how a 604 turns into a 64.",
            })
            cur = cur * 10 + ddig[i + 1]
            cur_keys = cur_keys + [f"n{i+1}"]
            continue

        started = True
        q = cur // divisor
        prod = q * divisor
        rem = cur - prod
        qcol = dcol(i)
        p = pv(i)
        ladder.append({"q": q * p, "prod": prod * p, "left": None})   # `left` filled below

        # --- the search itself. "How many 7s fit in 42?" is a hunt, and the hunt is
        # --- the part kids get wrong. Show the candidates and let it sit there.
        trials = _trials(cur, divisor, q)
        chip = {"trials": trials, "cur": cur, "divisor": divisor, "reserveW": 232}
        if q:
            chip["winPart"] = 0
        steps.append({
            "label": "TRY THEM", "beat": "D",
            "say": (f"How many <b>{divisor}</b>s fit inside <b>{cur}</b>? Nobody just "
                    f"<i>knows</i> this — you <b>try them</b>, and you keep the biggest one "
                    f"that still fits."),
            "why": ("<b>Too small</b> is the one people skip. A digit is too small when "
                    "what is <i>left over</i> would still hold another " + str(divisor) +
                    " — you could have fitted one more in."),
            "show": [], "flash": ["dv"] + cur_keys,
            "bubble": chip, "modelRow": k_index, "dwell": 5.6,
        })

        # --- D: divide
        toks.append({"k": f"q{i}", "r": R_Q, "c": qcol, "t": str(q), "cls": "d quo"})
        q_written.append(f"q{i}")
        if q == 0:
            say = (f"<b>D — Divide.</b> How many <b>{divisor}</b>s fit in <b>{cur}</b>? "
                   f"<b>None.</b> So write a <b>0</b> up top, right above the {ddig[i]}.")
            why = (f"It means there are <b>no {PLACE[W-1-i]}</b> in the answer — no groups of "
                   f"{divisor * p}. That is a real fact about the answer and it needs a real digit, "
                   f"because the digits after it depend on sitting in the right column.")
            trap = (f"<b>Write the 0. Do not skip it.</b> Skipping it here shifts every digit after "
                    f"it and the answer comes out about ten times too small.")
        else:
            nxt = (q + 1) * divisor
            say = (f"<b>D — Divide.</b> How many <b>{divisor}</b>s fit in <b>{cur}</b>? "
                   f"<b>{_spell(q).capitalize()}</b> — because {q} × {divisor} = {prod}, "
                   f"and {q+1} × {divisor} = {nxt}, which is too big.")
            why = (f"That {q} sits in the {PLACE[W-1-i]} column, so it is really <b>{q*p}</b>. "
                   f"You just found <b>{q*p} groups of {divisor}</b> inside {dividend}.")
            trap = ("The digit goes <b>directly above the digit you just used</b>, not off to the side. "
                    "The column is what turns a 6 into a 600.") if len(q_written) == 1 else None
        d_step = {"label": "D", "beat": "D", "say": say, "why": why, "show": [f"q{i}"],
                  "flash": [f"q{i}", "dv"] + cur_keys, "trap": trap, "bubble": dict(chip),
                  "modelRow": k_index, "dwell": 4.8 if trap else 3.6}
        if q:
            # the digit you picked in the trial is the digit that goes up top -- it
            # flies out of the winning row, so the answer has a visible source
            d_step["split"] = [{"part": 0, "to": f"q{i}"}]
            d_step["keepChip"] = True
        steps.append(d_step)

        # --- M: multiply
        sub_txt = str(prod)
        sub_start = qcol - (len(sub_txt) - 1)
        sub_keys = []
        for t_i, ch in enumerate(sub_txt):
            k = f"s{i}_{t_i}"
            toks.append({"k": k, "r": row, "c": sub_start + t_i, "t": ch, "cls": "d subtrahend"})
            sub_keys.append(k)
        toks.append({"k": f"m{i}", "r": row, "c": sub_start - 1, "t": "−", "cls": "op"})
        steps.append({
            "label": "M", "beat": "M",
            "say": f"<b>M — Multiply.</b> {q} × {divisor} = <b>{prod}</b>. "
                   f"Write it <b>underneath</b>, lined up under the {cur}.",
            "why": f"On paper it looks like {prod}, but it is really <b>{prod*p}</b> — that is "
                   f"{q*p} groups of {divisor}, and it is the chunk of {dividend} you have now "
                   f"accounted for.",
            "show": sub_keys + [f"m{i}"], "flash": sub_keys, "dwell": 3.6, "modelRow": k_index,
            "bubble": dict(chip),
        })

        # --- S: subtract
        rule_start = min(sub_start - 1, cur_start)
        decor.append({"kind": "rule", "k": f"r{i}", "r": row + 1, "c0": rule_start, "c1": qcol})
        rem_txt = str(rem)
        rem_start = qcol - (len(rem_txt) - 1)
        rem_keys = []
        for t_i, ch in enumerate(rem_txt):
            k = f"e{i}_{t_i}"
            toks.append({"k": k, "r": row + 2, "c": rem_start + t_i, "t": ch, "cls": "d rem"})
            rem_keys.append(k)
        s_trap = None
        if len(q_written) == 1:
            s_trap = (f"Check the leftover: <b>{rem} is smaller than {divisor}</b>. It always must be. "
                      f"If your leftover is ever <i>bigger</i> than {divisor}, your digit up top was "
                      f"too small — back up and make it bigger.")
        steps.append({
            "label": "S", "beat": "S",
            "say": f"<b>S — Subtract.</b> {cur} − {prod} = <b>{rem}</b>.",
            "why": f"Really <b>{cur*p} − {prod*p} = {rem*p}</b>. That {rem*p} is what is still "
                   f"un-divided, and it is too small to make another group of {divisor*p}.",
            "show": [f"r{i}"] + rem_keys, "flash": rem_keys, "trap": s_trap,
            "dwell": 4.8 if s_trap else 3.4, "modelRow": k_index,
        })

        # --- B: bring down (or finish)
        if i + 1 < W:
            nxt_d = ddig[i + 1]
            k = f"bd{i}"
            toks.append({"k": k, "r": row + 2, "c": dcol(i + 1), "t": str(nxt_d), "cls": "d drop"})
            new_cur = rem * 10 + nxt_d
            steps.append({
                "label": "B", "beat": "B",
                "say": f"<b>B — Bring down.</b> Pull the <b>{nxt_d}</b> straight down next to the "
                       f"{rem}. Now you are dividing <b>{new_cur}</b>, and the four moves start again.",
                "why": f"You are moving down one place value: from {PLACE[W-1-i]} to "
                       f"{PLACE[W-2-i]}. The {rem*p} left over plus the {nxt_d*pv(i+1)} you just "
                       f"pulled down make <b>{new_cur*pv(i+1)}</b> still to divide.",
                "show": [k], "flash": [f"n{i+1}", k], "dwell": 4.0, "modelRow": k_index,
            })
            cur, cur_start, cur_keys = new_cur, rem_start, rem_keys + [k]
            row += 3
        else:
            toks.append({"k": "rlab", "r": R_Q, "c": W + 2, "t": f"R{rem}", "cls": "rlab"})
            steps.append({
                "label": "REMAINDER", "beat": None,
                "say": f"Nothing left to bring down. The <b>{rem}</b> that will not split is the "
                       f"<b>remainder</b>. Answer: <b>{quotient} R{rem}</b>.",
                "why": f"{rem} is smaller than {divisor}, so it cannot make even one more group. "
                       f"On a word problem this is the number that decides the answer — "
                       f"{rem} left over means you still need one more of whatever you are counting.",
                "show": ["rlab"], "flash": ["rlab"] + rem_keys, "dwell": 4.8, "modelRow": k_index,
            })
            steps.append({
                "label": "CHECK", "beat": None,
                "say": f"Check it by going backwards: <b>{quotient} × {divisor} = "
                       f"{quotient*divisor}</b>, plus the remainder <b>{rem}</b> "
                       f"= <b>{quotient*divisor + rem}</b>. That is the number you started with. ✓",
                "why": f"And the ladder adds up: "
                       f"{' + '.join(str(l['q']) for l in ladder)} = <b>{quotient}</b>. Those are "
                       f"the real sizes of the digits you wrote on top.",
                "show": [], "flash": q_written + ["rlab"], "dwell": 5.8, "modelRow": "all",
            })
        k_index += 1

    # fill in the ladder's running leftovers
    left = dividend
    for l in ladder:
        left -= l["prod"]
        l["left"] = left
    model = {
        "kind": "ladder", "start": dividend, "divisor": divisor,
        "rows": ladder, "quotient": quotient, "remainder": remainder,
        "caption": f"The same division without the shorthand. Each written digit is really a "
                   f"whole chunk: {' + '.join(str(l['q']) for l in ladder)} = <b>{quotient}</b> "
                   f"groups of {divisor}, with <b>{remainder}</b> left over.",
    }

    return {"cols": W + 2, "rows": row + 2, "toks": toks, "decor": decor, "steps": steps,
            "model": model, "answer": f"{quotient} R{remainder}"}
