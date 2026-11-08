"""build_exam_practice_1108.py -- Musa's (kid1) ONE-DAY 20-problem contest-style sheet (2026-11-08): student PDF + parent key PDF.

Asif (2026-11-08): "Musa and Yusuf math sheets for today ... make sure today is medium-hard set of problems for
what they need to prep for."  And on 11-07's sheets: "easy enough for them, but ... ran out of time to do their last
4 problems."  So today is contest-shaped: 45 minutes, pace checkpoints at #5 / #10 / #15, no worked model, no type
labels, mixed order, medium first and hardest last, with one quick problem inside #17-20.

  12 problems from the recent-exam types, harder than 11-07 (3 each; solver, verifier and wording imported from
     build_exam_practice.py): ARITH, T18 pair-totals (3-digit, one with a distractor), T19 fewest/most (a "0" case and
     a "girls run out" case), T20 two prices (bigger counts).
   8 problems from the Noetic grade 3 strands (private/PRACTICE-PLAN-2026.md, Musa focus track): undo 3 arrows (x2),
     sum and difference (x2), balance / find one unit, heads and legs (guess-check), missing number, trailing zeros.

    python3 build_exam_practice_1108.py <outdir>

Writes <outdir>/musa-practice-2026-11-08-{student,parent-key}.pdf (Chrome headless). Never prints.
Every answer is computed by solve() and re-derived by an independent brute-force verify(); the build fails on any
mismatch, on a non-whole answer, or on any count other than 20.  The render helpers here are reused by
build_yusuf_practice_1108.py.
"""
import html
import os
import subprocess
import sys

import build_exam_practice as bx
from kids_config import kids_by_id, kid_name

KID = "kid1"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = "musa-practice-2026-11-08"
DATE = "2026-11-08"
OPS = {"×": lambda x, n: x * n, "+": lambda x, n: x + n, "−": lambda x, n: x - n, "÷": lambda x, n: x / n}
INV = {"×": "÷", "÷": "×", "+": "−", "−": "+"}


# ===================================================================== new kinds (Noetic strands)
# Each solve_new() returns dict(ans, lines) by the TAUGHT method; verify_new() finds the answer by brute force.

def forward(x, ops):
    for o, n in ops:
        x = OPS[o](x, n)
    return x


def undo_lines(result, ops):
    arrows = "? " + " ".join("→ %s%d" % (o, n) for o, n in ops) + " → %d" % result
    lines = ["Arrows: " + arrows]
    v = result
    for o, n in reversed(ops):
        u = INV[o]
        w = OPS[u](v, n)
        assert w == int(w), (result, ops)
        w = int(w)
        lines.append("Undo %s%d: %d %s %d = %d" % (o, n, v, u, n, w))
        v = w
    lines.append("Check forward from %d: " % v + ", ".join(str(int(forward(v, ops[:i + 1]))) for i in range(len(ops)))
                 + " ✓")
    return v, lines


def solve_new(p):
    k = p["kind"]
    if k == "undo":
        v, lines = undo_lines(p["result"], p["ops"])
        return dict(ans=v, lines=lines)
    if k == "missing":
        a, b, c = p["rhs"]
        r = a * b + c
        v, ul = undo_lines(r, p["ops"])
        return dict(ans=v, lines=["Right side first: %d × %d + %d = %d + %d = %d" % (a, b, c, a * b, c, r)] + ul[1:-1]
                    + ["Check: put %d in the box: left side = %d = right side ✓" % (v, forward(v, p["ops"]))])
    if k == "zeros":
        b, per, g = p["boxes"], p["per"], p["groups"]
        tot = b * per
        ans = tot // g
        assert ans * g == tot
        return dict(ans=ans, lines=[
            "All the %s: %d × %d. Fact %d × %d = %d, then add the %d zeros: %d" % (
                p["thing"], b, per, b // 10, per // 10, (b // 10) * (per // 10), 2, tot),
            "Share: %d ÷ %d. Fact %d ÷ %d = %d, then put the zeros back: %d" % (
                tot, g, tot // 100, g, (tot // 100) // g, ans),
            "Check: %d × %d = %d ✓" % (ans, g, tot)])
    if k == "sumdiff":
        T, d = p["total"], p["diff"]
        small = (T - d) // 2
        big = small + d
        assert small + big == T
        ans = big if p["ask"] == "big" else small
        return dict(ans=ans, lines=[
            "Two bars: the bigger bar is the smaller bar plus %d." % d,
            "Take the gap off: %d − %d = %d (now the two bars are equal)" % (T, d, T - d),
            "Split: %d ÷ 2 = %d, so %s = %d" % (T - d, small, p["small"], small),
            "%s = %d + %d = %d" % (p["big"], small, d, big),
            "Check: %d + %d = %d ✓ and %d − %d = %d ✓" % (big, small, T, big, small, d)])
    if k == "balance":
        na, nb, wb, ask = p["na"], p["nb"], p["wb"], p["ask_n"]
        both = nb * wb
        one = both // na
        assert one * na == both
        return dict(ans=ask * one, lines=[
            "%d %s balance %d %s: %d × %d = %d grams on each side" % (na, p["a"], nb, p["b"], nb, wb, both),
            "Find ONE %s first: %d ÷ %d = %d grams" % (p["a1"], both, na, one),
            "%d %s: %d × %d = %d grams" % (ask, p["a"], ask, one, ask * one),
            "Check: %d × %d = %d = %d × %d ✓" % (na, one, na * one, nb, wb)])
    if k == "legs":
        h, L, lo, hi = p["heads"], p["legs"], p["lo_legs"], p["hi_legs"]
        base = h * lo
        x = (L - base) // (hi - lo)
        assert base + x * (hi - lo) == L
        return dict(ans=x, lines=[
            "Guess: all %d are %s: %d × %d = %d legs. Too few by %d − %d = %d" % (h, p["lo"], h, lo, base, L, base, L - base),
            "Swap one %s for one %s: +%d legs each time" % (p["lo1"], p["hi1"], hi - lo),
            "Swaps needed: %d ÷ %d = %d, so %d %s" % (L - base, hi - lo, x, x, p["hi"]),
            "Check: %d × %d + %d × %d = %d + %d = %d legs ✓, %d + %d = %d heads ✓" % (
                x, hi, h - x, lo, x * hi, (h - x) * lo, L, x, h - x, h)])
    raise ValueError(k)


def verify_new(p, s):
    k = p["kind"]
    if k == "undo":
        hits = [x for x in range(0, 5001) if forward(x, p["ops"]) == p["result"]]
    elif k == "missing":
        a, b, c = p["rhs"]
        r = sum([a] * b) + c
        hits = [x for x in range(0, 1001) if forward(x, p["ops"]) == r]
    elif k == "zeros":
        tot = sum([p["per"]] * p["boxes"])
        hits = [q for q in range(0, tot + 1) if sum([q] * p["groups"]) == tot]
    elif k == "sumdiff":
        pairs = [(b, s_) for s_ in range(p["total"] + 1) for b in [p["total"] - s_] if b - s_ == p["diff"]]
        hits = [b if p["ask"] == "big" else s_ for b, s_ in pairs]
    elif k == "balance":
        hits = [p["ask_n"] * w for w in range(1, 5001) if p["na"] * w == p["nb"] * p["wb"]]
    elif k == "legs":
        hits = [x for x in range(p["heads"] + 1) if x * p["hi_legs"] + (p["heads"] - x) * p["lo_legs"] == p["legs"]]
    else:
        raise ValueError(k)
    return hits == [s["ans"]]


def text_new(p):
    k = p["kind"]
    if k in ("undo", "missing", "zeros", "sumdiff", "balance", "legs"):
        return p["q"]
    raise ValueError(k)


def box_expr(ops):
    """'(□ + 8) × 3' style left side, brackets wherever + or − comes before × or ÷."""
    s = "□"
    prev = None
    for o, n in ops:
        if o in "×÷" and prev in ("+", "−"):
            s = "(%s)" % s
        s = "%s %s %d" % (s, o, n)
        prev = o
    return s


# ===================================================================== the 20 problems
def sub(a, b):
    return bx.arith_sub(a, b)


def t18_distract(sentence, **kw):
    return dict(kind="t18", extra=sentence, **kw)


UNDO1_OPS = [("×", 4), ("−", 7), ("+", 15)]
UNDO2_OPS = [("−", 9), ("×", 2), ("−", 6)]
MISS_OPS = [("×", 8), ("−", 9)]

PROBLEMS = [
    # ---- medium (1-8)
    dict(sub(1000, 467), tier="medium", why="across three zeros at once"),
    dict(kind="zeros", boxes=40, per=60, groups=8, thing="crayons", unit="crayons", tier="medium",
         why="two zeros times, then a share; two steps",
         q="A school orders 40 boxes of crayons. Each box holds 60 crayons. The school shares all the crayons equally "
           "among 8 classes. How many crayons does each class get?"),
    dict(kind="t19", n=36, g=23, k=18, club="science fair team", half=True, ask="fewest", tier="medium",
         why="bigger class than 11-07; half of 36 first"),
    dict(kind="t18", names=("Zainab", "Mustafa", "Ruqayya"), thing="stickers", verb="have", ab=325, cb=412, b=168,
         tier="medium", why="3-digit subtractions with regrouping"),
    dict(kind="missing", ops=MISS_OPS, rhs=(6, 10, 3), unit="", tier="medium",
         why="work out the right side, then undo two steps",
         q="What number goes in the box?  <b>%s = 6 × 10 + 3</b>" % box_expr(MISS_OPS)),
    dict(kind="sumdiff", total=86, diff=14, big="Safiya", small="Rania", ask="big", unit="shells", tier="medium",
         why="asks for the BIGGER one; half of 86 is the trap",
         q="Safiya and Rania collected 86 shells at the beach together. Safiya collected 14 more shells than Rania. "
           "How many shells did Safiya collect?"),
    dict(kind="arith", expr="6 × 8 + 7 × (20 − 13)", op="mix2", vals=(6, 8, 7, 20, 13), tier="medium",
         why="bracket with a 2-digit subtraction, then two products"),
    dict(kind="t20", item_lo="small jars of honey", item_hi="large jars of honey", lo=3, hi=7, n=15, total=73,
         buyer="Sumayya", ask="hi", noun="jars", shop="A farm shop", tier="medium",
         why="15 items, a gap of $4 per swap"),
    # ---- medium-hard (9-15)
    dict(kind="undo", ops=UNDO1_OPS, result=52, unit="", tier="hard", why="three arrows; must undo all three",
         q="Amira thinks of a number. She multiplies it by 4, then subtracts 7, then adds 15. Her answer is 52. "
           "What number did she think of?"),
    t18_distract("The reading week lasted 7 days.", names=("Usman", "Maha", "Jibril"), thing="pages", verb="read",
                 ab=437, cb=506, b=219, tier="hard", why="a distractor number (7 days) and 3-digit regrouping"),
    dict(kind="balance", na=4, a="apples", a1="apple", nb=6, b="pears", wb=80, ask_n=3, unit="grams", tier="hard",
         why="find ONE apple first (not 3 × 80); three steps",
         q="On a balance scale, 4 apples weigh the same as 6 pears. Each pear weighs 80 grams. "
           "How much do 3 apples weigh?"),
    dict(kind="t19", n=30, g=13, k=15, club="football team", half=True, ask="fewest", tier="hard",
         why="the answer is 0: boys can fill every seat"),
    dict(kind="sumdiff", total=31, diff=9, big="Tasneem", small="Umar", ask="small", unit="years old", tier="hard",
         why="ages; odd total, so halving 31 fails at once",
         q="Tasneem is 9 years older than her brother Umar. Their ages add up to 31. How old is Umar?"),
    dict(kind="t20", item_lo="student tickets", item_hi="adult tickets", lo=4, hi=6, n=20, total=98,
         buyer=None, ask="lo", noun="tickets", tier="hard", why="20 tickets; the cheaper kind is asked"),
    dict(kind="t18b", names=("Amina", "Khalid", "Huda"), thing="apples", verb="picked", total3=615, ab=372, bc=408,
         tier="hard", why="three-person total; the right pair to take off is not the first one given"),
    # ---- hardest (16-20), one quick one at 18
    dict(kind="t19", n=32, g=12, k=16, club="art club", half=True, ask="most", tier="hard",
         why="the girls run out before the seats do: answer 12, not 16"),
    dict(kind="undo", ops=UNDO2_OPS, result=40, unit="marbles", tier="hard",
         why="a story with no arrows given; he must draw them, including the doubling",
         q="Bilal had some marbles. He gave 9 to his friend. Then his uncle gave him enough to double what he had left. "
           "Then he lost 6. Now he has 40 marbles. How many marbles did Bilal have at the start?"),
    dict(sub(4006, 1758), tier="quick", why="QUICK one placed late on purpose; four digits across two zeros"),
    dict(kind="t20", item_lo="paper kites", item_hi="cloth kites", lo=4, hi=9, n=14, total=86, buyer="Anas",
         ask="lo", noun="kites", shop="A kite stall", tier="hard", why="a $5 gap and the cheaper item is asked"),
    dict(kind="legs", heads=13, legs=38, lo="chickens", lo1="chicken", hi="goats", hi1="goat", lo_legs=2, hi_legs=4,
         unit="goats", tier="hard", why="two unknowns with no prices; guess, check, adjust by the gap",
         q="A farmyard has only chickens and goats. Together they have 13 heads and 38 legs. How many goats are there?"),
]
assert len(PROBLEMS) == 20

WATCH = {
    1: "Borrowing across all three zeros. A wrong answer like 643 or 633 means he subtracted the small digit from the big one in a column. The add-back line catches it.",
    2: "Moving the zeros: 40 × 60 is 2400, not 240. Two lines, not one answer.",
    3: "Half of 36 written as a line (18). Then boys 13. Writes 23 − 18 if he mixes up who fills the seats.",
    4: "Each subtraction on its own line. Adding all three numbers (325 + 412 + 168) is the wrong idea.",
    5: "Right side worked out FIRST (63), then undo − 9 BEFORE ÷ 8. Writing 63 ÷ 8 is undoing in the wrong order.",
    6: "His test miss (#9): halving the total (43). Look for the gap taken off first: 86 − 14.",
    7: "Bracket first. 7 × 20 − 13 = 127 means he skipped the bracket.",
    8: "The bracket step: 3 × 15 = 45, and 3 × x. Answer must pass the dollar check.",
    9: "His test miss (#12): undoing ONE step and stopping. Need three undo lines, last arrow first.",
    10: "The 7 days is a distractor. If 7 shows up in his work, he grabbed every number.",
    11: "His test miss (#16): 3 × 80 = 240 or 6 × 80 × 3. Look for '1 apple = 120' on its own line.",
    12: "Answer 0 is right. Writing 2 (15 − 13) means he used girls instead of boys.",
    13: "Halving 31 gives 15.5: if he writes 15 or 16, he skipped taking the gap off.",
    14: "Asked for STUDENT tickets (the cheaper ones). Answering 9 (the adult count) is a read-the-question slip.",
    15: "Total minus the pair that does NOT hold Amina (Khalid + Huda = 408). Taking 615 − 372 gives Huda, not Amina.",
    16: "Answer 12, not 16. The seats outnumber the girls; the check line should say only 12 girls exist.",
    17: "He must draw the three arrows himself (− 9, × 2, − 6). Undoing the doubling is ÷ 2; 40 + 6 = 46, 46 ÷ 2 = 23, 23 + 9 = 32.",
    18: "Quick one late on purpose. If it is blank, he ran out of time on 17, not this.",
    19: "Asked for PAPER kites (the cheaper ones). Bracket line: 9 × 14 = 126.",
    20: "Guess-check line: all chickens = 26 legs, 12 short, each goat adds 2. Answering 7 means he gave the chickens.",
}


# ===================================================================== solve / verify / text, dispatching
def solve(p):
    return solve_new(p) if p["kind"] in NEW_KINDS else bx.solve(p)


def verify(p, s):
    return verify_new(p, s) if p["kind"] in NEW_KINDS else bx.verify(p, s)


def statement(p):
    if p["kind"] in NEW_KINDS:
        return text_new(p)
    t = bx.statement(p)
    if p.get("extra"):
        i = t.rindex(" How many")
        t = t[:i] + " " + p["extra"] + t[i:]
    return t


def unit_of(p):
    return p["unit"] if "unit" in p else bx.unit_of(p)


NEW_KINDS = ("undo", "missing", "zeros", "sumdiff", "balance", "legs")


# ===================================================================== render (shared with build_yusuf_practice_1108.py)
CSS = """
  @page { size: letter; margin: 0.45in; @top-left { content: "TOPLEFT"; font-size: 10px; } @bottom-right { content: "Page " counter(page); font-size: 10px; } }
  * { box-sizing: border-box; }
  body { font-family: -apple-system,'Helvetica Neue',Arial,sans-serif; color:#000; font-size:15px; line-height:1.35; margin:0; }
  h1 { font-size:22px; margin:0 0 4px; }
  .nm { font-size:16px; margin:2px 0 4px; } .nm span, .blank { display:inline-block; min-width:90px; border-bottom:1.5px solid #000; }
  .nm span { min-width:200px; }
  .rules { border:2px solid #000; border-radius:6px; padding:5px 10px; margin:4px 0 8px; font-size:14.5px; }
  .rules div { margin:1px 0; }
  .prob { border:1.5px solid #888; border-radius:8px; padding:6px 10px; margin:0 0 7px; break-inside:avoid; display:flex; flex-direction:column; }
  .prob .q { font-size:15.5px; }
  .prob .q b.n { display:inline-block; background:#000; color:#fff; border-radius:50%; width:25px; height:25px; text-align:center; line-height:25px; margin-right:7px; font-size:14px; }
  .space { flex:1; }
  .ans { font-size:15.5px; text-align:right; } .ans .blank { min-width:140px; }
  .pace { border:2px dashed #000; border-radius:6px; padding:4px 10px; margin:0 0 7px; font-size:14.5px; font-weight:700; break-inside:avoid; }
  .art { font:700 20px/1.15 Menlo,monospace; text-align:right; display:inline-block; float:right; margin:0 30px 0 10px; }
  .keyhead { font-size:13.5px; margin-bottom:6px; }
  .pacebox { border:2px solid #000; border-radius:6px; padding:5px 10px; margin:4px 0 8px; font-size:13.5px; }
  .pacebox div { margin:3px 0; }
  .kprob { border-bottom:1px solid #bbb; padding:4px 0 5px; break-inside:avoid; }
  .kprob .q { font-size:12.5px; color:#333; }
  .keyln { margin:1px 0 1px 12px; font-size:13.5px; }
  .kans { font-weight:700; }
  .kmeta { margin:2px 0 0 12px; font-size:12.5px; } .watch { margin:2px 0 0 12px; font-size:12.5px; font-style:italic; }
  .how { font-size:12.5px; margin-top:8px; }
"""

SPACE = {"quick": 120, "medium": 165, "hard": 215}
CHECKPOINTS = {5: 11, 10: 22, 15: 34}


def rules_html():
    return ('<div class="rules">'
            '<div><b>45 minutes, like the contest.</b> &nbsp; Start: <span class="blank"></span> &nbsp; Finish: <span class="blank"></span></div>'
            '<div><b>Stuck more than 3 minutes? Circle it, move on, come back at the end.</b></div>'
            '<div><b>Show one step per line.</b> No calculator.</div></div>')


def pace_line(n):
    return ('<div class="pace">Pace check: you just finished #%d. You should be at about %d minutes. '
            'Clock now: <span class="blank"></span></div>' % (n, CHECKPOINTS[n]))


def student_doc(name, title, items, toplabel):
    """items: list of (number, statement_html, unit, tier, art_html)."""
    out = ['<h1>%s</h1><div class="nm">Name: <span>%s</span> &nbsp; Date: <span style="min-width:120px">%s</span></div>%s' % (
        html.escape(title), html.escape(name), DATE, rules_html())]
    for n, text, unit, tier, art in items:
        out.append('<div class="prob" style="min-height:%dpx"><div class="q">%s<b class="n">%d</b>%s</div>'
                   '<div class="space"></div><div class="ans">Answer: <span class="blank"></span> %s</div></div>' % (
                       SPACE[tier], art, n, text, html.escape(unit)))
        if n in CHECKPOINTS:
            out.append(pace_line(n))
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>%s, student</title><style>%s</style></head><body>%s</body></html>" % (
        html.escape(title), CSS.replace("TOPLEFT", toplabel), "".join(out)))


def pace_box_html():
    return ('<div class="pacebox"><b>Pace</b> (45 minutes; note the clock at each checkpoint)'
            '<div>Start: <span class="blank"></span> &nbsp; After #5 (target about 11 min): <span class="blank"></span> &nbsp; '
            'After #10 (about 22 min): <span class="blank"></span></div>'
            '<div>After #15 (about 34 min): <span class="blank"></span> &nbsp; Finish: <span class="blank"></span></div>'
            '<div>Attempted: <span class="blank" style="min-width:50px"></span> of 20 &nbsp; Finished with lines: '
            '<span class="blank" style="min-width:50px"></span> of 20 &nbsp; Circled and skipped: <span class="blank" style="min-width:160px"></span></div>'
            '<div>Grade the lines first: a right answer with no lines is UNSHOWN, not a pass.</div></div>')


def key_doc(name, title, rows, method, toplabel):
    """rows: list of (number, statement_html, lines, answer, unit, tier, why, watch)."""
    blocks = []
    for n, text, lines, ans, unit, tier, why, watch in rows:
        body = "".join('<div class="keyln">%s</div>' % html.escape(l) for l in lines)
        blocks.append('<div class="kprob"><div class="q"><b>%d.</b> %s</div>%s<div class="keyln kans">Answer: %s %s</div>'
                      '<div class="kmeta">Lines expected: %d (one per line above). Level: %s, %s.</div>'
                      '<div class="watch">Watch for: %s</div></div>' % (
                          n, text, body, ans, html.escape(unit), len(lines), tier, html.escape(why), html.escape(watch)))
    head = ('<h1>Parent answer key</h1><div class="keyhead">For %s, %s, %s. Not on the student sheet: no worked model and no type labels, on purpose.</div>%s' % (
        html.escape(name), html.escape(title), DATE, pace_box_html()))
    pages = [head + "".join(blocks)]   # one flow; .kprob never splits across pages
    pages[-1] += '<div class="how">%s</div>' % method
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>%s, key</title><style>%s .pg{page-break-after:always} .pg:last-child{page-break-after:auto}</style></head><body>%s</body></html>" % (
        html.escape(title), CSS.replace("TOPLEFT", toplabel), "".join('<div class="pg">%s</div>' % x for x in pages)))


def to_pdf(text, out, base, suffix):
    h = os.path.join(out, "%s-%s.html" % (base, suffix))
    pdf = os.path.join(out, "%s-%s.pdf" % (base, suffix))
    with open(h, "w") as f:
        f.write(text)
    if os.path.exists(pdf):
        os.remove(pdf)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run", "--no-pdf-header-footer",
                    "--virtual-time-budget=5000", "--user-data-dir=" + os.path.join(out, "ud-" + base + "-" + suffix),
                    "--print-to-pdf=" + pdf, "file://" + h], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    if not os.path.exists(pdf):
        raise SystemExit("Chrome wrote no PDF: " + pdf)
    return pdf


def check_whole(n, s):
    if not isinstance(s["ans"], int) or s["ans"] < 0:
        raise SystemExit("problem %d: answer %r is not a whole number" % (n, s["ans"]))


METHOD = ("<b>How each answer was checked.</b> The key lines use the taught method. A second route with no shared algebra then "
          "re-solved every problem before this file was written: subtractions by counting up one at a time; products by repeated "
          "addition; pair totals, two-price, sum-and-difference, heads-and-legs and balance problems by trying every whole number and "
          "keeping only the one that fits every sentence; club problems by trying every possible number of girls; undo and missing-number "
          "problems by running every start number 0 to 5000 forward. Each had exactly one fit, equal to the key.")


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    if len(PROBLEMS) != 20:
        raise SystemExit("need 20 problems, have %d" % len(PROBLEMS))
    solved = []
    for i, p in enumerate(PROBLEMS, 1):
        s = solve(p)
        if not verify(p, s):
            print("VERIFY FAILED %d: %r -> %r" % (i, p, s["ans"]), file=sys.stderr)
            return 1
        check_whole(i, s)
        solved.append(s)
    name = kid_name(kids_by_id(), KID)
    top = "%s - contest practice %s" % (name, DATE)
    items = [(i, statement(p), unit_of(p), p["tier"], "") for i, p in enumerate(PROBLEMS, 1)]
    rows = [(i, statement(p), s["lines"], s["ans"], unit_of(p), p["tier"], p["why"], WATCH[i])
            for i, (p, s) in enumerate(zip(PROBLEMS, solved), 1)]
    title = "Contest practice: 20 problems"
    pdfs = [to_pdf(student_doc(name, title, items, top), out, BASE, "student"),
            to_pdf(key_doc(name, title, rows, METHOD, top), out, BASE, "parent-key")]
    print("ok: %d problems verified a second way; answers: %s" % (len(PROBLEMS), [s["ans"] for s in solved]))
    print("\n".join(pdfs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
