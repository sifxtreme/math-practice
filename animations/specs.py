"""Step-by-step algorithm simulators for the drill animations.

Every number on screen is produced HERE, by running the actual algorithm --
nothing is typed by hand. `verify_animations.py` re-derives the same values a
second, independent way and asserts they match.

Grid model (1-based, matches CSS grid):
    column 1        = the operator / divisor gutter
    columns 2..W+1  = digit places, left to right (W = width of the widest number)
Helper `col(j)` maps "j places from the right" to a grid column, so j=0 is always
the ones column.

A "token" is one written mark: {k: key, r: row, c: col, t: text, cls: style}.
Steps reveal tokens by key. Reveal is cumulative and recomputed from scratch on
every step change, which is what makes the Back button work.
"""

# ---------------------------------------------------------------- helpers

def _digits(n):
    return [int(ch) for ch in str(n)]


def _spell(n):
    return {0: "no", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}.get(n, str(n))


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

    setup_keys = [f"t{j}" for j in range(len(tdig))] + ["op", "b0", "rule1"]
    steps.append({
        "label": "SET UP",
        "say": f"Stack them so the <b>ones line up</b>. The {bot} on the bottom is going to "
               f"visit every digit on top, one at a time, <b>starting from the right</b>.",
        "show": setup_keys, "flash": ["b0"], "dwell": 3.4,
    })

    carry = 0
    for j, d in enumerate(reversed(tdig)):
        raw = bot * d
        total = raw + carry
        last = (j == len(tdig) - 1)
        place = ["ones", "tens", "hundreds", "thousands", "ten-thousands"][j]

        show, flash = [], ["b0", f"t{j}"]
        if carry:
            flash.append(f"cy{j-1}")

        if carry == 0:
            say = f"<b>{bot} × {d} = {raw}.</b>"
        else:
            say = (f"<b>{bot} × {d} = {raw}</b>, and <i>now</i> add the carry: "
                   f"<b>{raw} + {carry} = {total}</b>.")

        trap = None
        if last:
            if total >= 10:
                for i, ch in enumerate(reversed(str(total))):
                    toks.append({"k": f"a{j+i}", "r": R_ANS, "c": col(j + i), "t": ch, "cls": "d ans"})
                    show.append(f"a{j+i}")
                say += (f" Nothing left to multiply, so the whole <b>{total}</b> goes down.")
            else:
                toks.append({"k": f"a{j}", "r": R_ANS, "c": col(j), "t": str(total), "cls": "d ans"})
                show.append(f"a{j}")
                say += f" Write the <b>{total}</b>."
        elif total >= 10:
            ones, tens = total % 10, total // 10
            toks.append({"k": f"a{j}", "r": R_ANS, "c": col(j), "t": str(ones), "cls": "d ans"})
            toks.append({"k": f"cy{j}", "r": R_CARRY, "c": col(j + 1), "t": str(tens), "cls": "carry"})
            show += [f"a{j}", f"cy{j}"]
            say += (f" That's too big for one box — the <b>{ones}</b> goes down in the {place} "
                    f"column, and the <b>{tens}</b> goes <b>up on the shelf</b> above the next column.")
            if j == 0:
                trap = ("The carry lives <b>on the paper</b>, not in your head. Write it up top "
                        "every single time — that is the whole reason this method exists.")
        else:
            toks.append({"k": f"a{j}", "r": R_ANS, "c": col(j), "t": str(total), "cls": "d ans"})
            show.append(f"a{j}")
            say += f" Write the <b>{total}</b>."

        if carry and trap is None:
            wrong = (d + carry) * bot
            trap = (f"<b>Multiply first, then add.</b> Doing it backwards — "
                    f"{d} + {carry} = {d+carry}, then {d+carry} × {bot} = {wrong} — "
                    f"is the mistake almost everybody makes here.")

        steps.append({"label": f"× {d}", "say": say, "show": show,
                      "flash": flash, "trap": trap, "dwell": 4.2 if trap else 3.2})

        carry = 0 if last else total // 10

    rough = round(top, -1)
    steps.append({
        "label": "CHECK",
        "say": f"<b>{top} × {bot} = {product}.</b> Now check it's sensible: {top} is about "
               f"{rough}, and {rough} × {bot} = {rough*bot}. {product} is right next to it. ✓",
        "show": [], "flash": [f"a{j}" for j in range(W)], "dwell": 5.0,
    })

    return {"cols": W + 1, "rows": 5, "toks": toks, "decor": decor, "steps": steps,
            "answer": product}


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

    setup = [f"t{j}" for j in range(len(tdig))] + ["op", "bo", "bt", "rule1"]
    steps.append({
        "label": "SET UP",
        "say": f"Two digits on the bottom means <b>two rounds</b>, so you get <b>two answer rows</b> "
               f"and then you add them. Round 1 uses the <b>{b_ones}</b>. Round 2 uses the "
               f"<b>{b_tens}</b> — and that one has a catch.",
        "show": setup, "flash": ["bo", "bt"], "dwell": 4.6,
    })

    # ---- round 1: the ones digit
    carry = 0
    for j, d in enumerate(reversed(tdig)):
        raw = b_ones * d
        total = raw + carry
        last = (j == len(tdig) - 1)
        show, flash = [], ["bo", f"t{j}"]
        if carry:
            flash.append(f"cA{j-1}")
        say = (f"<b>{b_ones} × {d} = {raw}.</b>" if carry == 0 else
               f"<b>{b_ones} × {d} = {raw}</b>, then add the carry: <b>{raw} + {carry} = {total}</b>.")
        trap = None
        if last:
            for i, ch in enumerate(reversed(str(total))):
                toks.append({"k": f"p1_{j+i}", "r": R_P1, "c": col(j + i), "t": ch, "cls": "d p1"})
                show.append(f"p1_{j+i}")
            say += f" Nothing left on top, so all of <b>{total}</b> goes down."
        else:
            toks.append({"k": f"p1_{j}", "r": R_P1, "c": col(j), "t": str(total % 10), "cls": "d p1"})
            show.append(f"p1_{j}")
            if total >= 10:
                toks.append({"k": f"cA{j}", "r": R_CARRY, "c": col(j + 1), "t": str(total // 10), "cls": "carry"})
                show.append(f"cA{j}")
                say += f" Write <b>{total % 10}</b>, carry the <b>{total // 10}</b>."
            else:
                say += f" Write <b>{total}</b>."
        if carry and trap is None:
            wrong = (d + carry) * b_ones
            trap = (f"<b>Multiply first, then add the carry.</b> Not "
                    f"{d} + {carry} = {d+carry}, then × {b_ones} = {wrong}.")
        steps.append({"label": f"× {b_ones}", "say": say, "show": show, "flash": flash,
                      "trap": trap, "dwell": 4.0 if trap else 3.0})
        carry = 0 if last else total // 10

    carriesA = [t["k"] for t in toks if t["k"].startswith("cA")]
    steps.append({
        "label": "ROW 1 DONE",
        "say": f"Row 1 is finished: <b>{p1}</b>. That is <b>{b_ones} × {top}</b>.",
        "show": [], "flash": [f"p1_{i}" for i in range(len(str(p1)))], "dwell": 3.0,
    })
    if carriesA:
        steps.append({
            "label": "CROSS OUT",
            "say": "Before round 2, <b>cross out the carries</b> from round 1. They belong to that "
                   "row and nothing else.",
            "show": [], "flash": [], "strike": carriesA, "dwell": 3.6,
            "trap": "Leaving them there is a quiet disaster — you add them a second time in "
                    "round 2 and the answer comes out wrong with no obvious sign of why.",
        })

    # ---- round 2: the tens digit, starting with the placeholder zero
    toks.append({"k": "zero", "r": R_P2, "c": col(0), "t": "0", "cls": "d p2 zero"})
    steps.append({
        "label": "THE ZERO",
        "say": f"Round 2 uses the <b>{b_tens}</b> — but it is <b>not {b_tens}</b>. It sits in the "
               f"tens column, so it is really <b>{b_tens*10}</b>. Before you multiply anything, "
               f"<b>put a 0 in the ones column</b> of row 2.",
        "show": ["zero", "plus"], "flash": ["bt", "zero"], "dwell": 5.4,
        "trap": f"<b>This is the single most common way to get a 2-digit × 2-digit wrong.</b> "
                f"Skip the 0 and you add {p1} + {p2//10} = {p1 + p2//10} instead of "
                f"{p1} + {p2} = {product}.",
    })

    carry = 0
    for j, d in enumerate(reversed(tdig)):
        raw = b_tens * d
        total = raw + carry
        last = (j == len(tdig) - 1)
        slot = j + 1                                    # shifted one left by the placeholder
        show, flash = [], ["bt", f"t{j}"]
        if carry:
            flash.append(f"cB{j-1}")
        say = (f"<b>{b_tens} × {d} = {raw}.</b>" if carry == 0 else
               f"<b>{b_tens} × {d} = {raw}</b>, then add the carry: <b>{raw} + {carry} = {total}</b>.")
        if last:
            for i, ch in enumerate(reversed(str(total))):
                toks.append({"k": f"p2_{slot+i}", "r": R_P2, "c": col(slot + i), "t": ch, "cls": "d p2"})
                show.append(f"p2_{slot+i}")
            say += f" All of <b>{total}</b> goes down."
        else:
            toks.append({"k": f"p2_{slot}", "r": R_P2, "c": col(slot), "t": str(total % 10), "cls": "d p2"})
            show.append(f"p2_{slot}")
            if total >= 10:
                toks.append({"k": f"cB{j}", "r": R_CARRY, "c": col(j + 1), "t": str(total // 10), "cls": "carry carry2"})
                show.append(f"cB{j}")
                say += f" Write <b>{total % 10}</b>, carry the <b>{total // 10}</b>."
            else:
                say += f" Write <b>{total}</b>."
        steps.append({"label": f"× {b_tens}", "say": say, "show": show, "flash": flash, "dwell": 3.0})
        carry = 0 if last else total // 10

    steps.append({
        "label": "ROW 2 DONE",
        "say": f"Row 2 is <b>{p2}</b>, which is <b>{b_tens*10} × {top}</b>. See how the 0 made it "
               f"ten times bigger than {p2//10}? That is what the 0 is for.",
        "show": ["rule2"], "flash": [], "dwell": 4.4,
    })

    ans_keys = []
    for i, ch in enumerate(reversed(str(product))):
        toks.append({"k": f"a{i}", "r": R_ANS, "c": col(i), "t": ch, "cls": "d ans"})
        ans_keys.append(f"a{i}")
    steps.append({
        "label": "ADD",
        "say": f"Last move: <b>add the two rows</b>. {p1} + {p2} = <b>{product}</b>.",
        "show": ans_keys, "flash": ans_keys, "dwell": 3.6,
    })

    r_top = round(top, -1)
    steps.append({
        "label": "CHECK",
        "say": f"Sense-check: {top} is about {r_top}, so the answer should land near "
               f"{r_top} × {bot} = {r_top*bot}. We got <b>{product}</b>. ✓",
        "show": [], "flash": ans_keys, "dwell": 5.0,
    })

    return {"cols": W + 1, "rows": 8, "toks": toks, "decor": decor, "steps": steps,
            "answer": product}


# ------------------------------------------------- long division

def long_division(dividend, divisor):
    """Long division with a remainder: D-M-S-B, one written mark at a time."""
    assert 0 < divisor < 10, "this layout is for a single-digit divisor"
    assert dividend >= divisor, "the quotient would be zero; not a drill shape"
    ddig = _digits(dividend)
    W = len(ddig)
    col = lambda j: W + 1 - j                      # j places from the right
    dcol = lambda i: i + 2                         # i-th dividend digit (0 = leftmost)
    R_Q, R_DIV = 1, 2

    toks, steps, decor = [], [], []
    for i, d in enumerate(ddig):
        toks.append({"k": f"n{i}", "r": R_DIV, "c": dcol(i), "t": str(d), "cls": "d"})
    toks.append({"k": "dv", "r": R_DIV, "c": 1, "t": str(divisor), "cls": "d hot"})
    decor.append({"kind": "bracket", "k": "brk", "r": R_DIV, "c0": 2, "c1": W + 1})

    setup = ["dv", "brk"] + [f"n{i}" for i in range(W)]
    steps.append({
        "label": "SET UP",
        "say": f"<b>{dividend}</b> goes inside the house, <b>{divisor}</b> stands outside. "
               f"Then you repeat four moves, in this order, forever: "
               f"<b>Divide → Multiply → Subtract → Bring down.</b>",
        "show": setup, "flash": ["dv"], "dwell": 4.6,
    })

    row = 3
    cur, cur_start = 0, 2          # value being divided, and its leftmost grid column
    cur_keys = []                  # the marks on the page that spell out `cur`
    started = False
    q_written = []

    for i, d in enumerate(ddig):
        if i == 0:
            cur, cur_start, cur_keys = d, dcol(0), ["n0"]
        # (subsequent digits are brought down at the end of the previous iteration)

        if not started and cur < divisor:
            steps.append({
                "label": "TOO SMALL",
                "say": f"How many <b>{divisor}</b>s fit in <b>{cur}</b>? <b>None</b> — {divisor} is "
                       f"bigger than {cur}. So you write <i>nothing</i> above the {cur} and take one "
                       f"more digit: look at <b>{cur*10 + ddig[i+1]}</b> instead.",
                "show": [], "flash": [f"n{i}", f"n{i+1}"], "dwell": 5.0,
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

        # --- D: divide
        toks.append({"k": f"q{i}", "r": R_Q, "c": qcol, "t": str(q), "cls": "d quo"})
        q_written.append(f"q{i}")
        if q == 0:
            say = (f"<b>D — Divide.</b> How many <b>{divisor}</b>s fit in <b>{cur}</b>? "
                   f"<b>None.</b> So write a <b>0</b> up top, right above the {ddig[i]}.")
            trap = (f"<b>Write the 0. Do not skip it.</b> Skipping it here shifts every digit after "
                    f"it and the answer comes out about ten times too small.")
        else:
            nxt = (q + 1) * divisor
            say = (f"<b>D — Divide.</b> How many <b>{divisor}</b>s fit in <b>{cur}</b>? "
                   f"<b>{_spell(q).capitalize()}</b> — because {q} × {divisor} = {prod}, "
                   f"and {q+1} × {divisor} = {nxt}, which is too big.")
            trap = ("The digit goes <b>directly above the digit you just used</b>, not off to the side. "
                    "The column is what keeps the place value honest.") if len(q_written) == 1 else None
        steps.append({"label": "D", "say": say, "show": [f"q{i}"],
                      "flash": [f"q{i}", "dv"] + cur_keys,
                      "trap": trap, "dwell": 4.4 if trap else 3.4})

        # --- M: multiply
        sub_txt = str(prod)
        sub_start = qcol - (len(sub_txt) - 1)
        sub_keys = []
        for t_i, ch in enumerate(sub_txt):
            k = f"s{i}_{t_i}"
            toks.append({"k": k, "r": row, "c": sub_start + t_i, "t": ch, "cls": "d sub"})
            sub_keys.append(k)
        toks.append({"k": f"m{i}", "r": row, "c": sub_start - 1, "t": "−", "cls": "op"})
        steps.append({
            "label": "M",
            "say": f"<b>M — Multiply.</b> {q} × {divisor} = <b>{prod}</b>. "
                   f"Write it <b>underneath</b>, lined up under the {cur}.",
            "show": sub_keys + [f"m{i}"], "flash": sub_keys, "dwell": 3.2,
        })

        # --- S: subtract
        # The rule sits under the minus sign and every digit of both numbers, so it
        # starts at whichever is further left: the minus, or the leading digit of `cur`.
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
            "label": "S",
            "say": f"<b>S — Subtract.</b> {cur} − {prod} = <b>{rem}</b>.",
            "show": [f"r{i}"] + rem_keys, "flash": rem_keys, "trap": s_trap,
            "dwell": 4.4 if s_trap else 3.0,
        })

        # --- B: bring down (or finish)
        if i + 1 < W:
            nxt_d = ddig[i + 1]
            k = f"bd{i}"
            toks.append({"k": k, "r": row + 2, "c": dcol(i + 1), "t": str(nxt_d), "cls": "d drop"})
            new_cur = rem * 10 + nxt_d
            steps.append({
                "label": "B",
                "say": f"<b>B — Bring down.</b> Pull the <b>{nxt_d}</b> straight down next to the "
                       f"{rem}. Now you are dividing <b>{new_cur}</b>, and the four moves start again.",
                "show": [k], "flash": [f"n{i+1}", k], "dwell": 3.6,
            })
            cur, cur_start, cur_keys = new_cur, rem_start, rem_keys + [k]
            row += 3
        else:
            quotient = dividend // divisor
            toks.append({"k": "rlab", "r": R_Q, "c": W + 2, "t": f"R{rem}", "cls": "rlab"})
            steps.append({
                "label": "REMAINDER",
                "say": f"Nothing left to bring down. The <b>{rem}</b> that will not split is the "
                       f"<b>remainder</b>. Answer: <b>{quotient} R{rem}</b>.",
                "show": ["rlab"], "flash": ["rlab"] + rem_keys, "dwell": 4.4,
            })
            steps.append({
                "label": "CHECK",
                "say": f"Check it by going backwards: <b>{quotient} × {divisor} = "
                       f"{quotient*divisor}</b>, plus the remainder <b>{rem}</b> "
                       f"= <b>{quotient*divisor + rem}</b>. That is the number you started with. ✓",
                "show": [], "flash": q_written + ["rlab"], "dwell": 5.4,
            })

    return {"cols": W + 2, "rows": row + 2, "toks": toks, "decor": decor, "steps": steps,
            "answer": f"{dividend // divisor} R{dividend % divisor}"}
