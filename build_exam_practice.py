"""build_exam_practice.py -- Musa's focused 20-problem practice set (2026-11-06), student sheet + parent key.

Asif's request (2026-11-06, via Instinct): 20 problems for two days, emphasis on three
types from a recent exam, plus arithmetic. Practice, not a test. Algebra first where a
relationship is modeled: define unknowns, write equations, solve line by line, check.

  T18  "two pair-totals + one known part"   (a+b, c+b, b given -> a+c)
  T19  "fewest / most in a group"           (n students, g girls, k in a club -> fewest girls)
  T20  "two prices, one count, one total"   (p*x + q*(n-x) = total)
  ARITH subtraction across tens/hundreds with an add-back check, and the bracket step 5 x (10 - 3)

Every problem here is NEW: no number, name or story is copied from the exam or from earlier
focus sheets. The exam is not named anywhere in the output.

    python3 build_exam_practice.py        # verifies every answer a second way, then writes
                                          #   worksheet-focus-2026-11-06-exam-practice.html      (student)
                                          #   worksheet-focus-2026-11-06-exam-practice-key.html  (parent key)

The student file holds Day 1 (pages 1-3) then Day 2 (pages 4-6). Paper rule (AGENTS.md): print ONE day,
by page range, and only when Asif says so. This script never prints.

The outputs carry the real name (from kids.local.json) and are gitignored by the focus-* glob.
"""
import html
import sys

from kids_config import kids_by_id, kid_name

KID = "kid1"
DATE_TAG = "2026-11-06"


# --------------------------------------------------------------------------------------
# The 20 problems. Data only; answers are DERIVED below and checked a second way.
# --------------------------------------------------------------------------------------
def arith_sub(a, b):
    return {"kind": "arith", "expr": "%d − %d" % (a, b), "a": a, "b": b, "op": "sub"}


PROBLEMS = [
    # ---------------- Day 1 ----------------
    dict(day=1, **arith_sub(280, 90)),
    dict(day=1, **arith_sub(350, 170)),
    dict(day=1, kind="t19", n=20, g=12, k=10, club="chess club", half=True, ask="fewest"),
    dict(day=1, kind="t19", n=24, g=15, k=8, club="choir", half=False, ask="fewest"),
    dict(day=1, kind="t18", names=("Laila", "Omar", "Zayd"), thing="grams of grapes", verb="ate",
         ab=150, cb=230, b=80),
    dict(day=1, kind="t18", names=("Hana", "Ibrahim", "Sara"), thing="stickers", verb="have",
         ab=130, cb=190, b=60),
    dict(day=1, kind="t18", names=("Kareem", "Sana", "Rashid"), thing="pages", verb="read",
         ab=345, cb=410, b=175),
    dict(day=1, kind="t20", item_lo="plain buns", item_hi="sesame buns", lo=3, hi=5, n=8, total=32,
         buyer="Samir", ask="hi", noun="buns"),
    dict(day=1, kind="t20", item_lo="gel pens", item_hi="ink pens", lo=2, hi=3, n=9, total=22,
         buyer="Fatima", ask="lo", noun="pens"),
    dict(day=1, kind="t20", item_lo="child tickets", item_hi="adult tickets", lo=3, hi=5, n=12, total=52,
         buyer=None, ask="lo", noun="tickets"),
    # ---------------- Day 2 ----------------
    dict(day=2, **arith_sub(600, 285)),
    dict(day=2, kind="arith", expr="4 \u00d7 7 + 5 \u00d7 3", op="mix1"),
    dict(day=2, kind="arith", expr="4 \u00d7 3 + 5 \u00d7 (10 \u2212 3)", op="mix2"),
    dict(day=2, kind="t18", names=("Yasmin", "Zara", "Noor"), thing="cm of ribbon", verb="used",
         ab=120, cb=165, b=45),
    dict(day=2, kind="t18b", names=("Aisha", "Bashir", "Dania"), thing="apples", verb="picked",
         total3=460, ab=290, bc=250),
    dict(day=2, kind="t19", n=30, g=21, k=15, club="art club", half=True, ask="fewest"),
    dict(day=2, kind="t19", n=26, g=15, k=13, club="drama club", half=True, ask="most"),
    dict(day=2, kind="t19", n=28, g=17, k=14, club="science club", half=True, ask="fewest"),
    dict(day=2, kind="t20", item_lo="small notebooks", item_hi="large notebooks", lo=3, hi=5, n=11, total=45,
         buyer="Zayn", ask="lo", noun="notebooks"),
    dict(day=2, kind="t20", item_lo="mangoes", item_hi="papayas", lo=2, hi=4, n=9, total=26,
         buyer="Hamza", ask="hi", noun="fruits"),
]
assert len(PROBLEMS) == 20


# --------------------------------------------------------------------------------------
# Solving. Each solve() returns the answer by the METHOD TAUGHT (key lines) ...
# --------------------------------------------------------------------------------------
def solve(p):
    k = p["kind"]
    if k == "arith":
        if p["op"] == "sub":
            ans = p["a"] - p["b"]
            return dict(ans=ans, lines=[
                "%d − %d = %d" % (p["a"], p["b"], ans),
                "Check by adding back: %d + %d = %d ✓" % (ans, p["b"], p["a"])])
        if p["op"] == "mix1":
            a, b, c, d = p.get("vals", (4, 7, 5, 3))
            return dict(ans=a * b + c * d, lines=["%d × %d = %d" % (a, b, a * b), "%d × %d = %d" % (c, d, c * d),
                                                   "%d + %d = %d" % (a * b, c * d, a * b + c * d)])
        if p["op"] == "mix2":
            a, b, c, d, e = p.get("vals", (4, 3, 5, 10, 3))
            return dict(ans=a * b + c * (d - e), lines=["Bracket first: %d − %d = %d" % (d, e, d - e),
                                                         "%d × %d = %d and %d × %d = %d" % (a, b, a * b, c, d - e, c * (d - e)),
                                                         "%d + %d = %d" % (a * b, c * (d - e), a * b + c * (d - e))])
    if k == "t18":
        a, b, c = p["names"]
        a_ = p["ab"] - p["b"]
        c_ = p["cb"] - p["b"]
        ans = a_ + c_
        x, y, z = a[0].upper(), b[0].upper(), c[0].upper()
        return dict(ans=ans, a=a_, c=c_, lines=[
            "Known: %s (%s) = %d" % (y, b, p["b"]),
            "%s + %s = %d, so %s = %d − %d = %d" % (x, y, p["ab"], x, p["ab"], p["b"], a_),
            "%s + %s = %d, so %s = %d − %d = %d" % (z, y, p["cb"], z, p["cb"], p["b"], c_),
            "%s + %s = %d + %d = %d" % (x, z, a_, c_, ans),
            "Check: %d + %d = %d ✓ and %d + %d = %d ✓" % (a_, p["b"], p["ab"], c_, p["b"], p["cb"])])
    if k == "t18b":
        a, b, c = p["names"]
        x, y, z = a[0].upper(), b[0].upper(), c[0].upper()
        a_ = p["total3"] - p["bc"]
        b_ = p["ab"] - a_
        c_ = p["bc"] - b_
        return dict(ans=a_, b=b_, c=c_, lines=[
            "a + b + c = %d and b + c = %d" % (p["total3"], p["bc"]),
            "a = %d − %d = %d" % (p["total3"], p["bc"], a_),
            "Check: a + b = %d, so b = %d − %d = %d; then c = %d − %d = %d" % (
                p["ab"], p["ab"], a_, b_, p["bc"], b_, c_),
            "Add all three: %d + %d + %d = %d ✓" % (a_, b_, c_, a_ + b_ + c_)])
    if k == "t20":
        lo, hi, n, tot = p["lo"], p["hi"], p["n"], p["total"]
        if p["ask"] == "hi":
            # let x = the dearer item; cheaper = n - x.   lo(n-x) + hi x = tot
            const = lo * n
            coef = hi - lo
            x = (tot - const) // coef
            assert const + coef * x == tot
            lines = ["Let x = number of %s. Then %s = %d − x." % (p["item_hi"], p["item_lo"], n),
                     "%d(%d − x) + %dx = %d" % (lo, n, hi, tot),
                     "%d×%d − %dx + %dx = %d   (the bracket: %d × %d, and %d × x)" % (
                         lo, n, lo, hi, tot, lo, n, lo),
                     ("%d + %dx = %d" % (const, coef, tot)).replace("1x", "x"),
                     "%dx = %d − %d = %d, so x = %d" % (coef, tot, const, tot - const, x),
                     "Check: %d %s = $%d and %d %s = $%d; $%d + $%d = $%d ✓" % (
                         x, p["item_hi"], hi * x, n - x, p["item_lo"], lo * (n - x),
                         hi * x, lo * (n - x), tot)]
            return dict(ans=x, other=n - x, lines=lines)
        # let x = the cheaper item; dearer = n - x.   lo x + hi (n-x) = tot
        const = hi * n
        coef = hi - lo
        x = (const - tot) // coef
        assert const - coef * x == tot
        lines = ["Let x = number of %s. Then %s = %d − x." % (p["item_lo"], p["item_hi"], n),
                 "%dx + %d(%d − x) = %d" % (lo, hi, n, tot),
                 "%dx + %d×%d − %dx = %d   (the bracket: %d × %d, and %d × x)" % (
                     lo, hi, n, hi, tot, hi, n, hi),
                 ("%d − %dx = %d" % (const, coef, tot)).replace("1x", "x"),
                 ("%dx = %d − %d = %d, so x = %d" % (coef, const, tot, const - tot, x)).replace("1x =", "x ="),
                 "Check: %d %s = $%d and %d %s = $%d; $%d + $%d = $%d ✓" % (
                     x, p["item_lo"], lo * x, n - x, p["item_hi"], hi * (n - x),
                     lo * x, hi * (n - x), tot)]
        return dict(ans=x, other=n - x, lines=lines)
    if k == "t19":
        n, g, kk = p["n"], p["g"], p["k"]
        boys = n - g
        if p["ask"] == "fewest":
            ans = max(0, kk - boys)
            if kk - boys > 0:
                lines = ["Boys in the class: %d − %d = %d" % (n, g, boys),
                         "The %s has %d seats%s." % (p["club"], kk,
                                                      " (half of %d)" % n if p["half"] else ""),
                         "Most boys that can fill seats: all %d. Seats left for girls: %d − %d = %d" % (
                             boys, kk, boys, ans),
                         "Check: %d boys + %d girls = %d seats ✓; with only %d girls we would need %d boys, "
                         "and there are just %d." % (boys, ans, kk, ans - 1, kk - (ans - 1), boys)]
                lines[-1] = lines[-1].replace("with only %d girls" % (ans - 1), "with only %d girl(s)" % (ans - 1))
            else:
                lines = ["Boys in the class: %d − %d = %d" % (n, g, boys),
                         "The %s has %d seats. There are %d boys, and %d ≥ %d, so boys can fill every seat." % (
                             p["club"], kk, boys, boys, kk),
                         "Girls needed: %d. The fewest is 0." % ans,
                         "Check: %d boys + 0 girls = %d seats ✓" % (kk, kk)]
            return dict(ans=ans, lines=lines)
        ans = min(kk, g)
        if g < kk:   # not every seat can be a girl: the girls run out first (fixed 2026-11-08)
            lines = ["The %s has %d seats%s. There are only %d girls in the class." % (
                        p["club"], kk, " (half of %d)" % n if p["half"] else "", g),
                     "Put every girl in the club: %d girls. Seats still empty: %d − %d = %d; boys fill them." % (
                         g, kk, g, kk - g),
                     "Boys in the class: %d − %d = %d, enough for %d seats. Most girls: %d" % (n, g, boys, kk - g, ans),
                     "Check: %d girls + %d boys = %d seats ✓; %d girls is impossible, there are only %d." % (
                         ans, kk - g, kk, ans + 1, g)]
            return dict(ans=ans, lines=lines)
        lines = ["The %s has %d seats%s. There are %d girls." % (
                    p["club"], kk, " (half of %d)" % n if p["half"] else "", g),
                 "Fill the seats with girls: %d girls are enough for %d seats, so all %d seats can be girls." % (
                     g, kk, kk),
                 "Most girls: %d" % ans,
                 "Check: %d girls + 0 boys = %d seats ✓ and %d ≤ %d girls ✓" % (ans, kk, ans, g)]
        return dict(ans=ans, lines=lines)
    raise ValueError(p)


# --------------------------------------------------------------------------------------
# ... and verify() finds the answer a SECOND way, with no shared algebra: brute force.
# --------------------------------------------------------------------------------------
def verify(p, s):
    k = p["kind"]
    if k == "arith":
        if p["op"] == "sub":
            # count up from the smaller number to the larger, one step at a time
            x, steps = p["b"], 0
            while x < p["a"]:
                x += 1
                steps += 1
            return steps == s["ans"]
        if p["op"] == "mix1":
            a, b, c, d = p.get("vals", (4, 7, 5, 3))
            return sum([a] * b) + sum([c] * d) == s["ans"]
        if p["op"] == "mix2":
            a, b, c, d, e = p.get("vals", (4, 3, 5, 10, 3))
            return sum([a] * b) + sum([c] * (d - e)) == s["ans"]
    if k == "t18":
        sols = [(a, c) for a in range(0, p["ab"] + 1) for c in range(0, p["cb"] + 1)
                if a + p["b"] == p["ab"] and c + p["b"] == p["cb"]]
        return len(sols) == 1 and sum(sols[0]) == s["ans"]
    if k == "t18b":
        sols = [(a, b, c) for a in range(p["total3"] + 1) for b in range(p["total3"] + 1 - a)
                for c in [p["total3"] - a - b]
                if a + b == p["ab"] and b + c == p["bc"]]
        return len(sols) == 1 and sols[0][0] == s["ans"]
    if k == "t20":
        hits = [x for x in range(0, p["n"] + 1)
                if (p["lo"] * x + p["hi"] * (p["n"] - x) == p["total"] if p["ask"] == "lo"
                    else p["lo"] * (p["n"] - x) + p["hi"] * x == p["total"])]
        return hits == [s["ans"]]
    if k == "t19":
        ok = []
        for x in range(0, p["g"] + 1):          # x girls in the club
            boys_in = p["k"] - x
            if 0 <= boys_in <= p["n"] - p["g"]:
                ok.append(x)
        want = min(ok) if p["ask"] == "fewest" else max(ok)
        return want == s["ans"]
    raise ValueError(p)


# --------------------------------------------------------------------------------------
# Text of each problem (written once, used by the student sheet and by the key).
# --------------------------------------------------------------------------------------
def money(n):
    return "$%d" % n


def statement(p):
    k = p["kind"]
    if k == "arith":
        return "Solve, then check: <b>%s = ?</b>" % html.escape(p["expr"])
    if k == "t18":
        a, b, c = p["names"]
        verb = p["verb"]
        who_pair = lambda u, v: "%s and %s" % (u, v)
        if verb == "ate":
            t1 = "%s and %s ate %d grams together." % (a, b, p["ab"])
            t2 = "%s and %s ate %d grams together." % (c, b, p["cb"])
            t3 = "%s ate %d grams." % (b, p["b"])
            q = "How many grams did %s and %s eat altogether?" % (a, c)
            lead = "%s, %s and %s shared some grapes." % (a, b, c)
        elif verb == "have":
            t1 = "%s and %s have %d stickers together." % (a, b, p["ab"])
            t2 = "%s and %s have %d stickers together." % (b, c, p["cb"])
            t3 = "%s has %d stickers." % (b, p["b"])
            q = "How many stickers do %s and %s have altogether?" % (a, c)
            lead = "%s, %s and %s collect stickers." % (a, b, c)
        elif verb == "read":
            t1 = "%s and %s read %d pages together." % (a, b, p["ab"])
            t2 = "%s and %s read %d pages together." % (c, b, p["cb"])
            t3 = "%s read %d pages." % (b, p["b"])
            q = "How many pages did %s and %s read altogether?" % (a, c)
            lead = "%s, %s and %s took part in a reading week." % (a, b, c)
        else:  # used (ribbon)
            t1 = "%s and %s used %d cm of ribbon together." % (a, b, p["ab"])
            t2 = "%s and %s used %d cm of ribbon together." % (c, b, p["cb"])
            t3 = "%s used %d cm of ribbon." % (b, p["b"])
            q = "How many cm of ribbon did %s and %s use altogether?" % (a, c)
            lead = "%s, %s and %s decorated cards for Eid." % (a, b, c)
        return " ".join([lead, t1, t2, t3, q])
    if k == "t18b":
        a, b, c = p["names"]
        return ("%s, %s and %s picked %d apples in all. %s and %s picked %d apples together. "
                "%s and %s picked %d apples together. How many apples did %s pick?" % (
                    a, b, c, p["total3"], a, b, p["ab"], b, c, p["bc"], a))
    if k == "t20":
        lo, hi, n, tot = p["lo"], p["hi"], p["n"], p["total"]
        if p["buyer"] is None:
            body = ("At the school play, %s cost %s each and %s cost %s each. The school sold %d tickets "
                    "and collected %s in all." % (p["item_lo"], money(lo), p["item_hi"], money(hi), n, money(tot)))
        else:
            body = ("%s sells %s for %s each and %s for %s each. %s buys %d %s and pays %s in all." % (
                p.get("shop") or {"plain buns": "A bakery", "gel pens": "A shop", "small notebooks": "A store",
                 "mangoes": "A fruit stand"}[p["item_lo"]],
                p["item_lo"], money(lo), p["item_hi"], money(hi), p["buyer"], n, p["noun"], money(tot)))
        which = p["item_hi"] if p["ask"] == "hi" else p["item_lo"]
        return "%s How many %s were bought?" % (body, which) if p["buyer"] is None else \
            "%s How many %s did %s buy?" % (body, which, p["buyer"])
    if k == "t19":
        n, g, kk = p["n"], p["g"], p["k"]
        if p["half"]:
            join = "Half of the students joined the %s." % p["club"]
        else:
            join = "%d of the students joined the %s." % (kk, p["club"])
        if p["ask"] == "fewest":
            q = "What is the <b>fewest</b> possible number of girls in the %s?" % p["club"]
        else:
            q = "What is the <b>most</b> possible number of girls in the %s?" % p["club"]
        return "There are %d students in a class, and %d of them are girls. %s %s" % (n, g, join, q)
    raise ValueError(p)


def unit_of(p):
    k = p["kind"]
    if k == "arith":
        return ""
    if k in ("t18",):
        return {"ate": "grams", "have": "stickers", "read": "pages", "used": "cm of ribbon"}[p["verb"]]
    if k == "t18b":
        return "apples"
    if k == "t20":
        return p["item_hi"] if p["ask"] == "hi" else p["item_lo"]
    return "girls"


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------
CSS = """
  @page { size: letter; margin: 0.5in; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; color: #14142b; font-size: 15px; line-height: 1.35; margin: 0; }
  .pg { page-break-after: always; }
  .pg:last-child { page-break-after: auto; }
  h1 { font-size: 22px; margin: 0 0 2px 0; color: #1e3a8a; }
  .sub { color: #4b5563; font-size: 13.5px; margin-bottom: 8px; }
  .nm { font-size: 16px; margin-bottom: 6px; }
  .nm span { display: inline-block; min-width: 190px; border-bottom: 1.5px solid #14142b; }
  .primer { border: 2px solid #1e3a8a; border-radius: 8px; background: #f8faff; padding: 6px 12px; margin: 6px 0 8px 0; }
  .primer h2 { font-size: 16px; margin: 0 0 3px 0; color: #1e3a8a; }
  .primer .ln { margin: 1px 0 1px 12px; font-size: 14px; line-height: 1.3; }
  .primer .ln i { color: #6b7280; font-size: 12.5px; }
  .prob { border: 1.5px solid #c9ced8; border-radius: 8px; padding: 6px 10px; margin: 0 0 7px 0; break-inside: avoid; }
  .prob .q { font-size: 15.5px; margin-bottom: 4px; }
  .prob .q b.n { display: inline-block; background: #1e3a8a; color: #fff; border-radius: 50%; width: 24px; height: 24px; text-align: center; line-height: 24px; margin-right: 7px; font-size: 14px; }
  .lab { font-size: 12.5px; color: #1e3a8a; font-weight: 700; margin: 2px 0 1px 0; }
  .row { display: flex; gap: 8px; } .row .prob { flex: 1; display: flex; flex-direction: column; } .row .prob .ans { margin-top: auto; padding-top: 4px; }
  .blank { display: inline-block; min-width: 70px; border-bottom: 1.5px solid #14142b; }
  .box { border: 1.5px dashed #b6bccb; border-radius: 6px; }
  .ans { margin-top: 4px; font-size: 15.5px; }
  .ans .blank { min-width: 130px; }
  .note { font-size: 13px; color: #374151; background: #fff7ed; border-left: 4px solid #b45309; padding: 4px 9px; margin: 6px 0; }
  .keyln { margin: 1px 0 1px 12px; font-size: 14px; }
  .kprob { border-bottom: 1px solid #e5e7eb; padding: 4px 0 5px 0; break-inside: avoid; }
  .kprob .q { font-size: 13.5px; color: #374151; }
  .kans { font-weight: 700; color: #166534; }
  .how { font-size: 13.5px; color: #374151; margin-top: 8px; }
"""


def frame_for(p):
    k = p["kind"]
    if k == "arith":
        return ('<div class="lab">Work:</div><div class="box" style="height:62px"></div>'
                '<div class="lab" style="margin-top:4px">Check by adding back: <span class="blank" style="min-width:150px"></span></div>')
    if k in ("t18", "t18b"):
        return ('<div class="lab">Unknowns (what does each letter stand for?):</div>'
                '<div style="margin:2px 0 0 4px">Let <span class="blank" style="min-width:34px"></span> = <span class="blank" style="min-width:110px"></span> '
                '&nbsp; <span class="blank" style="min-width:34px"></span> = <span class="blank" style="min-width:110px"></span> '
                '&nbsp; <span class="blank" style="min-width:34px"></span> = <span class="blank" style="min-width:110px"></span></div>'
                '<div class="lab">Equations, then solve one line at a time:</div><div class="box" style="height:92px"></div>'
                '<div class="lab" style="margin-top:5px">Check (put your answers back into the story):</div><div class="box" style="height:32px"></div>')
    if k == "t20":
        return ('<div class="lab">Unknown:</div>'
                '<div style="margin:2px 0 0 4px">Let <span class="blank"></span> = number of <span class="blank" style="min-width:170px"></span> '
                '&nbsp; so <span class="blank" style="min-width:170px"></span> = <span class="blank"></span></div>'
                '<div class="lab">Cost equation, then solve one line at a time:</div><div class="box" style="height:92px"></div>'
                '<div class="lab" style="margin-top:5px">Check (cost of each kind, then add):</div><div class="box" style="height:32px"></div>')
    if k == "t19":
        return ('<div class="lab">Boys in the class = <span class="blank"></span></div><div class="lab">Seats in the club = <span class="blank"></span></div>'
                '<div class="lab">Draw or write who can fill the seats. Show each step:</div><div class="box" style="height:62px"></div>'
                '<div class="lab" style="margin-top:5px">Check:</div><div class="box" style="height:30px"></div>')
    raise ValueError(k)


def student_problem(idx, p):
    unit = unit_of(p)
    return ('<div class="prob"><div class="q"><b class="n">%d</b></div><div class="q qt">%s</div>%s'
            '<div class="ans">Answer: <span class="blank"></span> %s</div></div>' % (
                idx, statement(p), frame_for(p), html.escape(unit)))


def primer_day1():
    return """
<div class="primer"><h2>Worked example A: the fewest in a group</h2>
 <div class="ln">12 kids in a class, 7 are girls. Six kids join the chess club. Fewest girls in the club?</div>
 <div class="ln">Boys: 12 &minus; 7 = 5. Seats: 6. Fill seats with all 5 boys; seats left: 6 &minus; 5 = 1. Those must be girls. <b>Answer: 1 girl.</b>
 <i>Check: 5 boys + 1 girl = 6 &check;; 0 girls would need 6 boys, and there are only 5. If boys can fill every seat, the answer is 0.</i></div></div>
<div class="primer"><h2>Worked example B: two pair-totals and one known part</h2>
 <div class="ln">Idris and Hana made 100 stars together. Zaid and Hana made 150 together. Hana made 40. Idris and Zaid altogether?</div>
 <div class="ln">i + h = 100 and z + h = 150, h = 40 &rarr; i = 100 &minus; 40 = 60 and z = 150 &minus; 40 = 110 &rarr; i + z = 170. <b>Answer: 170.</b>
 <i>Check each: 60 + 40 = 100 &check;, 110 + 40 = 150 &check;. Write each subtraction, then add back.</i></div></div>
<div class="primer"><h2>Worked example C: two prices, one count, one total</h2>
 <div class="ln">Rana buys 6 flags: small $2, big $3, total $15. How many big? Let b = big flags; small = 6 &minus; b.</div>
 <div class="ln">2 &times; (6 &minus; b) + 3 &times; b = 15. The bracket: 2 &times; 6 = 12 and 2 &times; b = 2b, so 12 &minus; 2b + 3b = 15 &rarr; 12 + b = 15 &rarr; b = 3. <b>Answer: 3 big flags.</b>
 <i>Check: 3 big = $9, 3 small = $6, $9 + $6 = $15 &check;</i></div></div>
"""


def primer_day2():
    return """
<div class="primer"><h2>Same three ideas as Day 1</h2>
 <div class="ln">Say what each letter means. Write the equation. One step per line. Check by putting your answer back into the story. Look back at the worked examples on Day 1 if you get stuck.</div></div>
"""


def student_html(name, probs):
    d1 = [(i + 1, p) for i, p in enumerate(PROBLEMS) if p["day"] == 1]
    d2 = [(i + 1, p) for i, p in enumerate(PROBLEMS) if p["day"] == 2]

    def day_block(day, items, primer):
        out = ['<div class="pg"><h1>Practice: Day %d of 2</h1>'
               '<div class="sub">Untimed. This is practice, not a test: the goal is to show each step. '
               'Write what each letter means, write the equation, then one step per line.</div>'
               '<div class="nm">Name: <span>%s</span></div>%s' % (day, html.escape(name), primer)]
        i = 0
        while i < len(items):
            kind = items[i][1]["kind"]
            width = {"arith": 3, "t19": 2}.get(kind, 1)
            j = i
            while j < len(items) and items[j][1]["kind"] == kind and j - i < width:
                j += 1
            if width > 1 and j - i > 1:
                out.append('<div class="row">%s</div>' % "".join(student_problem(a, b) for a, b in items[i:j]))
            else:
                out.append("".join(student_problem(a, b) for a, b in items[i:j]))
            i = j
        out.append("</div>")
        return "".join(out)

    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Practice set, student</title><style>%s</style></head><body>%s%s</body></html>" % (
        CSS, day_block(1, d1, primer_day1()), day_block(2, d2, primer_day2())))


def key_html(name, solved):
    rows = []
    for i, (p, s) in enumerate(zip(PROBLEMS, solved), 1):
        body = "".join('<div class="keyln">%s</div>' % html.escape(l) for l in s["lines"])
        unit = unit_of(p)
        rows.append('<div class="kprob"><div class="q"><b>%d.</b> (Day %d) %s</div>%s'
                    '<div class="keyln kans">Answer: %s %s</div></div>' % (
                        i, p["day"], statement(p), body, s["ans"], html.escape(unit)))
    head = ('<h1>Parent answer key</h1><div class="sub">For %s\'s two-day practice set. Every answer below was '
            'worked a second way (see the last note) before this key was written.</div>' % html.escape(name))
    note = ('<div class="how"><b>How each answer was checked:</b> the key lines use the method taught on the sheet. '
            'The program then re-solved every problem by a different route with no algebra: subtractions by counting '
            'up one at a time, sums of groups by repeated addition, the two-price and pair-total problems by trying every '
            'possible whole number and keeping only the ones that fit every sentence of the story, and the club problems by '
            'trying every possible number of girls in the club and taking the smallest or largest that works. The pair-total and '
            'two-price problems each had exactly one whole-number fit, equal to the key.</div>')
    half = 10
    pg1 = head + "".join(rows[:half])
    pg2 = "".join(rows[half:]) + note
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Practice set, parent key</title><style>%s</style></head><body>"
            '<div class="pg">%s</div><div class="pg">%s</div></body></html>' % (CSS, pg1, pg2))


def main():
    solved = []
    for i, p in enumerate(PROBLEMS, 1):
        s = solve(p)
        if not verify(p, s):
            print("VERIFY FAILED for problem %d: %r -> %r" % (i, p, s["ans"]), file=sys.stderr)
            return 1
        solved.append(s)
    kids = kids_by_id()
    name = kid_name(kids, KID)
    with open("worksheet-focus-%s-exam-practice.html" % DATE_TAG, "w") as f:
        f.write(student_html(name, PROBLEMS))
    with open("worksheet-focus-%s-exam-practice-key.html" % DATE_TAG, "w") as f:
        f.write(key_html(name, solved))
    print("ok: 20 problems verified a second way; answers:", [s["ans"] for s in solved])
    return 0


if __name__ == "__main__":
    sys.exit(main())
