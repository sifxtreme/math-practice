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
NUMWORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


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


# ------------------------------------------------- N digits x M digits

def mult_two_by_two(top, bot):
    """Standard algorithm for ANY multi-digit multiplier: one round per digit of `bot`,
    each row starting with one more placeholder zero than the row above it, then a final
    addition. The name is historical -- it does 3x3 and beyond. Keep it, `problems.json`
    and the sweep both reach it through `generate()`."""
    assert bot >= 10, "use mult_by_one_digit for a single-digit multiplier"
    tdig = _digits(top)
    bdig = _digits(bot)                       # left to right
    N = len(bdig)
    rounds = list(reversed(bdig))             # ones first, the order you work in
    partials = [top * m * 10 ** k for k, m in enumerate(rounds)]
    product = top * bot
    W = len(str(product))
    col = lambda j: W + 1 - j
    R_CARRY, R_TOP, R_BOT, R_RULE1 = 1, 2, 3, 4
    R_P = [5 + k for k in range(N)]           # one written row per round
    R_RULE2, R_ANS = 5 + N, 6 + N

    toks, steps = [], []
    for j, d in enumerate(reversed(tdig)):
        toks.append({"k": f"t{j}", "r": R_TOP, "c": col(j), "t": str(d), "cls": "d"})
    toks.append({"k": "op", "r": R_BOT, "c": 1, "t": "×", "cls": "op"})
    bot_keys = []
    for k, m in enumerate(rounds):
        toks.append({"k": f"b{k}", "r": R_BOT, "c": col(k), "t": str(m),
                     "cls": "d hot" if k == 0 else "d hot2"})
        bot_keys.append(f"b{k}")
    for k in range(1, N):
        toks.append({"k": f"plus{k}", "r": R_P[k], "c": 1, "t": "+", "cls": "op"})

    decor = [
        {"kind": "rule", "k": "rule1", "r": R_RULE1, "c0": 1, "c1": W + 1},
        {"kind": "rule", "k": "rule2", "r": R_RULE2, "c0": 1, "c1": W + 1},
    ]

    # --- area model: one strip per digit of the multiplier, biggest place on top
    tcols = []
    for j, d in enumerate(reversed(tdig)):
        if d or j == 0:
            tcols.append(d * 10 ** j)
    tcols.reverse()
    model_rows = [{"v": rounds[k] * 10 ** k, "maps": f"p{k + 1}"}
                  for k in reversed(range(N))]
    cells = [{"r": ri, "c": ci, "v": r["v"] * cv}
             for ri, r in enumerate(model_rows) for ci, cv in enumerate(tcols)]
    model = {
        "kind": "area", "h": bot, "rows": model_rows,
        "cols": [{"v": v} for v in tcols], "cells": cells,
        "rowSums": [r["v"] * top for r in model_rows], "total": product,
        "caption": f"{top} × {bot} as a rectangle, one strip per digit of {bot}. "
                   + " ".join(f"The {r['v']} strip is written row {N - ri}, "
                              f"<b>{r['v'] * top}</b>." for ri, r in enumerate(model_rows)),
    }

    setup = ([f"t{j}" for j in range(len(tdig))] + ["op"] + bot_keys + ["rule1"])
    steps.append({
        "label": "SET UP", "beat": None,
        "say": f"{NUMWORD[N].capitalize()} digits on the bottom means <b>{NUMWORD[N]} "
               f"rounds</b>, so {NUMWORD[N]} answer rows, and then you add them all up.",
        "why": "Each digit on the bottom is a different size. The "
               + ", ".join(f"<b>{m}</b> is really <b>{m * 10 ** k}</b>"
                           for k, m in enumerate(rounds) if k) +
               ". That is where each row's zeros come from.",
        "show": setup, "flash": bot_keys, "dwell": 5.0, "modelRow": None,
    })

    def digit_beats(mult, d, carry, j, last, slot, ans_row, ans_pre, carry_pre,
                    hot_key, mrow, tens_scale):
        """Beats for one digit of a round: the multiplication, then (if a carry is
        coming in) the carry joining it, then where each half of the total goes."""
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
            "show": [], "flash": [hot_key, f"t{j}"],
            "bubble": {"cells": chip_first, "reserveW": reserve},
            "modelRow": mrow, "dwell": 3.6,
        })
        if carry:
            steps.append({
                "label": "+ THE CARRY", "beat": None,
                "say": f"Now bring in the carry: <b>{raw} + {carry} = {total}</b>.",
                "why": f"The carry came from the column on the right, where it did not "
                       f"fit. This is the column it belongs in.",
                "show": [], "flash": [f"{carry_pre}{j-1}"],
                "bubble": {"cells": chip_full, "grewFrom": len(chip_first),
                           "reserveW": reserve},
                "trap": (f"<b>Multiply first, then add the carry.</b> Not "
                         f"{d} + {carry} = {d+carry}, then × {mult} = {(d+carry)*mult}."),
                "modelRow": mrow, "dwell": 4.8,
            })

        show, split = [], []
        if last:
            for i, ch in enumerate(reversed(digits)):
                k = f"{ans_pre}{slot+i}"
                toks.append({"k": k, "r": ans_row, "c": col(slot + i), "t": ch,
                             "cls": "d p1"})
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
                         "cls": "d p1"})
            toks.append({"k": k_car, "r": R_CARRY, "c": col(j + 1), "t": str(tens),
                         "cls": "carry" + ("" if carry_pre == "c0" else " carry2")})
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
                         "cls": "d p1"})
            show.append(k_ans)
            split = [{"part": 0, "to": k_ans}]
            say2 = f"<b>{total}</b> is one digit — it drops straight down."
            why2 = "Nothing needs to move left."

        steps.append({
            "label": "WHERE IT GOES", "beat": None, "say": say2, "why": why2,
            "show": show, "flash": [], "bubble": {"cells": chip_full, "reserveW": reserve},
            "split": split, "modelRow": mrow, "dwell": 4.2,
        })
        return 0 if last else total // 10

    # --- one round per digit of the multiplier
    for k, m in enumerate(rounds):
        mrow = N - 1 - k                       # model rows run biggest-place first
        pre, cpre = f"p{k}_", f"c{k}_"

        if k:
            # the placeholder zeros: k of them, and they are the whole reason this row
            # is ten (or a hundred) times the last one
            zk = []
            for z in range(k):
                key = f"z{k}_{z}"
                toks.append({"k": key, "r": R_P[k], "c": col(z), "t": "0",
                             "cls": "d p2 zero"})
                zk.append(key)
            steps.append({
                "label": "THE ZERO" + ("S" if k > 1 else ""), "beat": None,
                "say": f"Round {k+1} uses the <b>{m}</b> — but it is <b>not {m}</b>. It "
                       f"sits {NUMWORD[k]} place{'s' if k > 1 else ''} to the left, so it "
                       f"is really <b>{m * 10 ** k}</b>. Before you multiply anything, put "
                       f"<b>{NUMWORD[k]} 0{'s' if k > 1 else ''}</b> at the end of this row.",
                "why": f"This row is <b>{m * 10 ** k} × {top} = {partials[k]}</b>. Every "
                       f"multiple of {m * 10 ** k} ends in {NUMWORD[k]} "
                       f"zero{'s' if k > 1 else ''}, so this row <i>has</i> to. You are not "
                       f"adding magic zeros — you are writing down where the number is.",
                "show": zk + [f"plus{k}"], "flash": [f"b{k}"] + zk, "dwell": 5.6,
                "modelRow": mrow,
                "trap": f"<b>This is the most common way to get a multi-digit multiply "
                        f"wrong.</b> Miss the zeros and you add {partials[k] // 10 ** k} "
                        f"instead of {partials[k]}.",
            })
            prev = [t["k"] for t in toks if t["k"].startswith(f"c{k-1}_")]
            if prev:
                steps.append({
                    "label": "CROSS OUT", "beat": None,
                    "say": "Cross out the carries from the last round. They belong to that "
                           "row and nothing else.",
                    "why": "They were amounts borrowed inside the previous row's "
                           "calculation. This is a different calculation.",
                    "show": [], "flash": [], "strike": prev, "dwell": 3.8,
                    "modelRow": mrow,
                    "trap": "Leaving them there adds them a second time, and the answer "
                            "comes out wrong with no obvious sign of why.",
                })

        if m == 0:
            # a whole round of zeros: one beat, one mark -- walking it digit by digit
            # writes one 0 per column, which is not the number 0
            key = f"{pre}{k}"
            toks.append({"k": key, "r": R_P[k], "c": col(k), "t": "0", "cls": "d p1"})
            steps.append({
                "label": f"× {m}", "beat": None,
                "say": f"Round {k+1} multiplies by <b>0</b>. Anything times 0 is 0, so the "
                       f"whole row is just <b>0</b> — no carrying, nothing to line up.",
                "why": f"<b>{top} × 0 = 0.</b> The row still matters: its zeros are holding "
                       f"the columns open for the rounds after it.",
                "show": [key], "flash": [f"b{k}"],
                "bubble": {"cells": [{"t": "0", "part": 0}], "reserveW": 62},
                "split": [{"part": 0, "to": key}], "modelRow": mrow, "dwell": 4.0,
            })
        else:
            carry = 0
            for j, d in enumerate(reversed(tdig)):
                carry = digit_beats(m, d, carry, j, j == len(tdig) - 1, j + k,
                                    R_P[k], pre, cpre, f"b{k}", mrow, 10 ** k)

        steps.append({
            "label": f"ROW {k+1} DONE", "beat": None,
            "say": f"Row {k+1} is <b>{partials[k]}</b> — that is <b>{m * 10 ** k} × {top}</b>.",
            "why": f"On the rectangle that is the <b>{m * 10 ** k}</b> strip, area "
                   f"<b>{partials[k]}</b>.",
            "show": [], "flash": [], "dwell": 3.4, "modelRow": mrow,
        })

    ans_keys = []
    for i, ch in enumerate(reversed(str(product))):
        toks.append({"k": f"a{i}", "r": R_ANS, "c": col(i), "t": ch, "cls": "d ans"})
        ans_keys.append(f"a{i}")
    steps.append({
        "label": "ADD", "beat": None,
        "say": f"Last move: <b>add all {NUMWORD[N]} rows</b>. "
               f"{' + '.join(str(p) for p in partials)} = <b>{product}</b>.",
        "why": f"Which is the whole rectangle: <b>{product}</b>.",
        "show": ans_keys + ["rule2"], "flash": ans_keys, "dwell": 4.0, "modelRow": "all",
    })

    r_top = round(top, -1)
    steps.append({
        "label": "CHECK", "beat": None,
        "say": f"Sense-check: {top} is about {r_top}, so the answer should land near "
               f"{r_top} × {bot} = {r_top * bot}. We got <b>{product}</b>. ✓",
        "why": f"All the little areas add to <b>{product}</b>.",
        "show": [], "flash": ans_keys, "dwell": 5.4, "modelRow": "all",
    })

    _mx = max((st["bubble"]["reserveW"] for st in steps if st.get("bubble")), default=0)
    for st in steps:
        if st.get("bubble"):
            st["bubble"]["reserveW"] = _mx

    return {"cols": W + 1, "rows": R_ANS, "toks": toks, "decor": decor, "steps": steps,
            "model": model, "answer": product}


# ------------------------------------------------- long division

def long_division(dividend, divisor):
    """Long division with a remainder: D-M-S-B, one written mark at a time."""
    # Asif 2026-08-01: never divide by 1 — the kid copies the number down and no
    # long division happens. See DRILLS.md, which measured how often it leaks in.
    assert divisor >= 2, "dividing by 1 is not a drill"
    assert dividend >= divisor, "the quotient would be zero; not a drill shape"
    ddig = _digits(dividend)
    W = len(ddig)
    ndiv = len(str(divisor))                       # the gutter is as wide as the divisor
    dcol = lambda i: i + 1 + ndiv                  # i-th dividend digit (0 = leftmost)
    pv = lambda i: 10 ** (W - 1 - i)               # place value of quotient digit at i
    R_Q, R_DIV = 1, 2

    toks, steps, decor = [], [], []
    for i, d in enumerate(ddig):
        toks.append({"k": f"n{i}", "r": R_DIV, "c": dcol(i), "t": str(d), "cls": "d"})
    dv_keys = []
    for i, ch in enumerate(str(divisor)):
        toks.append({"k": f"dv{i}", "r": R_DIV, "c": i + 1, "t": ch, "cls": "d hot"})
        dv_keys.append(f"dv{i}")
    decor.append({"kind": "bracket", "k": "brk", "r": R_DIV,
                  "c0": ndiv + 1, "c1": ndiv + W})

    quotient, remainder = divmod(dividend, divisor)

    setup = dv_keys + ["brk"] + [f"n{i}" for i in range(W)]
    steps.append({
        "label": "SET UP", "beat": None,
        "say": f"<b>{dividend}</b> goes inside the house, <b>{divisor}</b> stands outside. "
               f"Then you repeat four moves, in this order, forever: "
               f"<b>Divide → Multiply → Subtract → Bring down.</b>",
        "why": f"The real question underneath all of it: <b>how many {divisor}s fit inside "
               f"{dividend}?</b> You chip away at it a place value at a time — hundreds first, "
               f"then tens, then ones — instead of counting {divisor}s one by one.",
        "show": setup, "flash": dv_keys, "dwell": 5.0, "modelRow": None,
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
            "show": [], "flash": dv_keys + cur_keys,
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
                  "flash": [f"q{i}"] + dv_keys + cur_keys, "trap": trap, "bubble": dict(chip),
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
            toks.append({"k": "rlab", "r": R_Q, "c": ndiv + W + 1, "t": f"R{rem}",
                         "cls": "rlab"})
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

    return {"cols": ndiv + W + 1, "rows": row + 2, "toks": toks, "decor": decor,
            "steps": steps,
            "model": model, "answer": f"{quotient} R{remainder}"}
