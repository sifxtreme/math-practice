"""Everything except the worked example itself, derived from the shape of (kind, x, y).

`problems.json` says `{"kind": "mult", "x": 247, "y": 6}` and this file produces the
title, the skill line, the short rule card, and three you-try problems that hit the
same traps. Nothing here is written per problem, which is the point: adding an
animation must not require writing prose, or the prose is what stops you adding one.

The you-try picker is deterministic — same inputs, same three problems, every build.
A random picker would make the page churn on every rebuild and make the verifier's
job impossible.
"""

ORD = ["ones", "tens", "hundreds", "thousands", "ten-thousands"]
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def ndig(n):
    return len(str(abs(n)))


# ------------------------------------------------------------------ traits
# What makes a problem the SAME KIND OF HARD as the worked example. You-try
# problems that miss these are the same arithmetic and a different lesson.

def mult_traits(x, y):
    t = {"nx": ndig(x), "ny": ndig(y)}
    carry, tdig = 0, [int(c) for c in str(x)]
    carries = 0
    for m in ([y] if y < 10 else [int(c) for c in str(y)][::-1]):
        carry = 0
        for j, d in enumerate(reversed(tdig)):
            tot = m * d + carry
            if j < len(tdig) - 1 and tot >= 10:
                carries += 1
            carry = 0 if j == len(tdig) - 1 else tot // 10
    t["carries"] = carries
    t["zero_in_top"] = "0" in str(x)
    return t


def div_traits(x, y):
    q, r = divmod(x, y)
    qs = str(q)
    return {"nx": ndig(x), "ny": ndig(y), "nq": len(qs),
            "remainder": r != 0,
            "inner_zero": "0" in qs[1:-1] if len(qs) > 2 else False,
            "skips_first": int(str(x)[0]) < y}


def _ok_mult(a, b, want):
    if b < 2 or a < 10:
        return False
    t = mult_traits(a, b)
    if (t["nx"], t["ny"]) != (want["nx"], want["ny"]):
        return False
    if want["carries"] and not t["carries"]:
        return False
    if want["zero_in_top"] and not t["zero_in_top"]:
        return False
    return ndig(a * b) == want["nprod"]


def _ok_div(a, b, want):
    # never divide by 1 — Asif, 2026-08-01: "a waste of time for the kid"
    if b < 2 or a < b:
        return False
    t = div_traits(a, b)
    if (t["nx"], t["ny"], t["nq"]) != (want["nx"], want["ny"], want["nq"]):
        return False
    if want["remainder"] and not t["remainder"]:
        return False
    if want["inner_zero"] and not t["inner_zero"]:
        return False
    return True


def pick_try(kind, x, y, n=3):
    """Three problems of the same shape that land on the same traps. Deterministic:
    the sweep is offset by (x, y) so different worked examples get different picks,
    but the same worked example always gets the same three."""
    lox, hix = 10 ** (ndig(x) - 1), 10 ** ndig(x) - 1
    loy, hiy = 10 ** (ndig(y) - 1), 10 ** ndig(y) - 1
    if ndig(y) == 1:
        loy = 2                                    # never 1, never 0
    span_a, span_b = hix - lox + 1, hiy - loy + 1

    if kind == "mult":
        want = mult_traits(x, y)
        want["nprod"] = ndig(x * y)
        ok = _ok_mult
    else:
        want = div_traits(x, y)
        ok = _ok_div

    # walk BOTH numbers on every step, with different strides, or you get three
    # problems that share a first number and feel like one problem three times
    out = []
    for k in range(1, span_a * 4 + 400):
        a = lox + (k * 37 + x) % span_a
        b = loy + (k * 13 + y) % span_b
        if (a, b) == (x, y) or (a, b) in out:
            continue
        if ok(a, b, want):
            out.append((a, b))
            if len(out) == n:
                return out
    return out


# ------------------------------------------------------------------ prose

def describe(kind, x, y):
    if kind == "mult":
        return _describe_mult(x, y)
    return _describe_div(x, y)


def _describe_mult(x, y):
    nx, ny = ndig(x), ndig(y)
    t = mult_traits(x, y)
    if ny == 1:
        return {
            "title": "Multiplying by one digit",
            "skill": f"{nx}-digit × 1-digit, with carrying",
            "why": "The bottom number visits every digit on top, one at a time, right to "
                   "left. Anything too big for its box gets parked on the shelf above the "
                   "next column.",
            "rules": [
                "Line up the <b>ones</b> column. Always.",
                "Work <b>right to left</b> — " + ", then ".join(ORD[:nx]) + ".",
                "<b>Multiply first, then add the carry.</b> Never the other way round.",
                "A carry gets <b>written above</b>, not remembered.",
            ],
            "tryNote": ("Every one of these has a carry in it — that is the thing being "
                        "practised, not the times tables."
                        + (" One has a <b>0</b> in the middle on purpose: × 0 is still 0, "
                           "but a carry coming in still has to be added."
                           if t["zero_in_top"] else "")),
        }
    rounds = NUM.get(ny, str(ny))
    return {
        "title": f"{'Two' if ny == 2 else NUM.get(ny, ny).capitalize()} digits times "
                 f"{NUM.get(nx, nx)} digits",
        "skill": f"{nx}-digit × {ny}-digit, {rounds} partial products",
        "why": f"{rounds.capitalize()} digits on the bottom means <b>{rounds} rounds</b>, so "
               f"{rounds} answer rows, then you add them. Each round after the first is "
               f"multiplying by a bigger place, which is why each row starts with one more "
               f"<b>0</b> than the row above it.",
        "rules": [
            "One round per digit on the bottom, <b>right to left</b>.",
            "<b>Row 2 starts with one 0. Row 3 starts with two.</b> Write the zeros "
            "before you multiply anything."
            if ny > 2 else
            "<b>Row 2 starts with a 0 in the ones column.</b> Write the 0 before you "
            "multiply anything.",
            "<b>Cross out the carries</b> before starting the next round.",
            "Add all the rows at the end — that is the answer, not the last row on its own.",
        ],
        "tryNote": "Before you add the rows, point at each row's zeros and count them. "
                   "Every time.",
    }


def _describe_div(x, y):
    nx, ny = ndig(x), ndig(y)
    t = div_traits(x, y)
    big = nx >= 4 or t["inner_zero"]
    rules = [
        "<b>D</b>ivide → <b>M</b>ultiply → <b>S</b>ubtract → <b>B</b>ring down. Repeat.",
        "The answer digit goes <b>directly above</b> the digit you just used.",
        "After subtracting, the leftover must be <b>smaller than the divisor</b>. "
        "If it isn't, your digit was too small.",
    ]
    if t["skips_first"]:
        rules.append("Doesn't fit in the first digit? Take <b>one more</b>, and write "
                     "nothing above the first.")
    if t["inner_zero"]:
        rules.append("Doesn't fit after a bring-down? <b>Write a 0 up top</b> and keep "
                     "going. A zero at the <b>front</b> you skip; a zero in the "
                     "<b>middle</b> you must write.")
    if t["remainder"]:
        rules.append("Nothing left to bring down? Whatever is left is the <b>remainder</b>.")

    why = ("Four moves, in the same order, over and over until you run out of digits: "
           "<b>Divide, Multiply, Subtract, Bring down.</b> Never skip one, never reorder them.")
    if big:
        why = ("Same four moves as always — but with more digits you hit the traps that eat "
               "long division: the divisor not fitting in the first digit, and a "
               "<b>0 landing in the middle of the answer</b>.")
    if ny > 1:
        why += (f" And with a <b>{ny}-digit divisor</b> you can no longer recall the answer "
                f"— every digit is an <b>estimate you then check</b>.")

    note = "Say the four moves out loud on every single one. Out loud is the point."
    if t["inner_zero"]:
        note = ("All three of these have a <b>0 in the answer</b>. That is not a "
                "coincidence — it is the thing being practised.")
    return {
        "title": (f"Long division, {ny}-digit divisor" if ny > 1 else
                  "Long division, big numbers" if big else
                  "Long division with a remainder"),
        "skill": f"{nx}-digit ÷ {ny}-digit"
                 + (", remainder" if t["remainder"] else ", no remainder")
                 + (" — and a zero in the answer" if t["inner_zero"] else ""),
        "why": why,
        "rules": rules,
        "tryNote": note,
    }
