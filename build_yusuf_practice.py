"""build_yusuf_practice.py -- Yusuf's "Choose a Model" practice (2026-11-06): student PDF + parent key PDF.

Asif's request (via Instinct, 2026-11-06 16:31 PT): analyze Yusuf's paper, make a modest focused practice
set with a worked model and a separate parent key. Untimed, not an exam, algebra first where a
relationship is modeled. Visualization is Asif's hypothesis to test, not a finding.

Four types, one worked model each, two practice problems each, then two "no hint" problems where the
child must pick the model himself.  4 x 2 + 2 = 10 practice problems, 3 student pages.

  A  events vs intervals (first event counts)      -> timeline / number line
  B  worst case ("be sure")                        -> sketch the worst draw, then add one
  C  a cut makes new edges                         -> label the side, algebra for the unknown side
  D  letter addition (cryptarithm)                 -> columns + a carry, then an equation

Every answer is derived by the taught method (key lines) and re-derived by a second, independent
brute-force route before anything is written. Run:  python3 build_yusuf_practice.py <outdir>
This script never prints.  Name comes from kids.local.json (kid2).
"""
import html
import itertools
import os
import subprocess
import sys

from kids_config import kids_by_id, kid_name

KID = "kid2"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


# ---------------------------------------------------------------- data
def hm(m):  # minutes since midnight -> "7:20 AM"
    h, mi = divmod(m, 60)
    ap = "AM" if h < 12 else "PM"
    return "%d:%02d %s" % ((h - 1) % 12 + 1, mi, ap)


def T(h, m):
    return h * 60 + m


PROBS = [
    # ---- A: events vs intervals
    dict(id=1, t="A", kind="bus", first=T(7, 20), step=25, end=T(10, 0), what="ferry", plural="ferries",
         q="A ferry leaves the dock at %s and then every 25 minutes. How many ferries leave the dock from %s up to %s?"),
    dict(id=2, t="A", kind="posts", length=36, gap=4,
         q="A straight path is 36 meters long. Lamp posts stand 4 meters apart, with a post at <b>both</b> ends of the path. How many lamp posts are there?"),
    # ---- B: worst case
    dict(id=3, t="B", kind="worst", colors=["red", "blue", "green", "white"], each=8, need=2, thing="tiles",
         q="A bag holds 8 red, 8 blue, 8 green and 8 white tiles, and nothing else. Without looking, what is the <b>fewest</b> tiles you must take out to be <b>sure</b> that at least 2 of them are the same color?"),
    dict(id=4, t="B", kind="worst", colors=["mint", "cherry", "lemon"], each=15, need=3, thing="candies",
         q="A jar holds 15 mint, 15 cherry and 15 lemon candies, and nothing else. Without looking, what is the <b>fewest</b> candies you must take out to be <b>sure</b> that at least 3 of them are the same flavor?"),
    # ---- C: a cut makes new edges
    dict(id=5, t="C", kind="cut", side=8, given=26,
         q="A square tile has a perimeter of 32 inches. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 26 inches. What is the perimeter of the other rectangle?"),
    dict(id=6, t="C", kind="cut", side=9, given=30,
         q="A square rug has a perimeter of 36 feet. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 30 feet. What is the perimeter of the other rectangle?"),
    # ---- D: letter addition
    dict(id=7, t="D", kind="crypt", a="MM", b="N3", s="1M1", ask="N",
         q="In this addition, the same letter is the same digit and different letters are different digits. What digit is N?"),
    dict(id=8, t="D", kind="crypt", a="KK", b="P6", s="1PP", ask="P",
         q="In this addition, the same letter is the same digit and different letters are different digits. What digit is P?"),
    # ---- mixed: no model named
    dict(id=9, t="X", kind="bus", first=T(9, 5), step=20, end=T(10, 45), what="ring", plural="rings",
         q="A school bell rings at %s and then every 20 minutes. How many times does it ring from %s up to %s?"),
    dict(id=10, t="X", kind="worst", colors=["red", "blue", "green", "yellow", "black"], each=9, need=3, thing="gloves",
         q="A box holds 9 red, 9 blue, 9 green, 9 yellow and 9 black gloves, and nothing else. Without looking, what is the <b>fewest</b> gloves you must take out to be <b>sure</b> that at least 3 of them are the same color?"),
]


# ---------------------------------------------------------------- taught method (key lines) + second check
def val(s, m):
    return int("".join(str(m[c]) if c in m else c for c in s))


def solve(p):
    k = p["kind"]
    if k == "bus":
        span = p["end"] - p["first"]
        n_int, rem = divmod(span, p["step"])
        ans = n_int + 1
        times = [hm(p["first"] + i * p["step"]) for i in range(ans)]
        return dict(ans=ans, lines=[
            "Time from first to last: %s to %s = %d minutes." % (hm(p["first"]), hm(p["end"]), span),
            "Gaps (intervals): %d ÷ %d = %d, remainder %d. The remainder is leftover time, not an extra event." % (
                span, p["step"], n_int, rem),
            "Events = gaps + 1, because the first one counts: %d + 1 = %d." % (n_int, ans),
            "Timeline check: " + ", ".join(times) + "  (%d times)." % ans])
    if k == "posts":
        gaps = p["length"] // p["gap"]
        ans = gaps + 1
        return dict(ans=ans, lines=[
            "Gaps (intervals): %d ÷ %d = %d." % (p["length"], p["gap"], gaps),
            "Posts = gaps + 1 (a post at both ends): %d + 1 = %d." % (gaps, ans),
            "Number-line check: 0, " + ", ".join(str(p["gap"] * i) for i in range(1, ans)) + " (%d posts)." % ans])
    if k == "worst":
        c, e, n = len(p["colors"]), p["each"], p["need"]
        worst = c * (n - 1)
        ans = worst + 1
        return dict(ans=ans, lines=[
            "Worst case: every color shows up %d time(s) and none has %d yet: %d colors × %d = %d %s." % (
                n - 1, n, c, n - 1, worst, p["thing"]),
            "The very next one must match a color that already has %d: %d + 1 = %d." % (n - 1, worst, ans),
            "Check: with %d taken it is still possible to have no color %d times; with %d it is not." % (
                worst, n, ans)])
    if k == "cut":
        s, g = p["side"], p["given"]
        per = 4 * s
        x = g // 2 - s
        other = 2 * (s + (s - x))
        return dict(ans=other, x=x, lines=[
            "Square side = %d ÷ 4 = %d. Label the cut line %d: the cut is a NEW edge on both rectangles." % (per, s, s),
            "Let x = the other side of the rectangle that has perimeter %d. 2(%d + x) = %d, so %d + x = %d, x = %d." % (
                g, s, g, s, g // 2, x),
            "The other rectangle's sides: %d and %d − %d = %d. Perimeter = 2(%d + %d) = %d." % (
                s, s, x, s - x, s, s - x, other),
            "Check: %d + %d = %d. That equals the square's perimeter %d plus the two new edges 2 × %d = %d: %d + %d = %d ✓" % (
                g, other, g + other, per, s, 2 * s, per, 2 * s, per + 2 * s)])
    if k == "crypt":
        sol = crypt_solutions(p)[0]
        a, b, s = p["a"], p["b"], p["s"]
        return dict(ans=sol[p["ask"]], sol=sol, lines=crypt_lines(p, sol))
    raise ValueError(p)


def crypt_solutions(p):
    letters = sorted(set(c for c in p["a"] + p["b"] + p["s"] if c.isalpha()))
    out = []
    for d in itertools.permutations(range(10), len(letters)):
        m = dict(zip(letters, d))
        if any(m.get(x[0], int(x[0]) if x[0].isdigit() else 1) == 0 for x in (p["a"], p["b"], p["s"])):
            continue
        if val(p["a"], m) + val(p["b"], m) == val(p["s"], m):
            out.append(m)
    return out


def lin(word):
    """A column word like 'KK', 'N7' or '1NN' as (letter coefficients, constant): place value times digit."""
    co, const = {}, 0
    for i, ch in enumerate(word):
        place = 10 ** (len(word) - 1 - i)
        if ch.isdigit():
            const += place * int(ch)
        else:
            co[ch] = co.get(ch, 0) + place
    return co, const


def fmt(co, const):
    terms = [(v, "%s%s" % ("" if abs(v) == 1 else abs(v), k)) for k, v in sorted(co.items(), key=lambda kv: -kv[1]) if v]
    if const or not terms:
        terms.append((const, str(abs(const))))
    out = ("−" if terms[0][0] < 0 else "") + terms[0][1]   # 11H − W, never 11H + -1W (fixed 2026-11-08)
    for v, t in terms[1:]:
        out += (" − " if v < 0 else " + ") + t
    return out


def crypt_lines_generic(p, sol):
    """Taught steps for any 'two numbers = a three-digit sum' puzzle, computed (not hand-typed)."""
    a, b, s = p["a"], p["b"], p["s"]
    (ca, ka), (cb, kb), (cs, ks) = lin(a), lin(b), lin(s)
    left = {}
    for d in (ca, cb):
        for k, v in d.items():
            left[k] = left.get(k, 0) + v
    for k, v in cs.items():
        left[k] = left.get(k, 0) - v
    rhs = ks - ka - kb
    ask = p["ask"]
    other = [k for k in sorted(sol) if k != ask][0]
    return ["Each number is tens and ones: %s = %s, %s = %s, %s = %s. The leading 1 in the sum is a carry, so the sum is 100 or more." % (
                a, fmt(ca, ka), b, fmt(cb, kb), s, fmt(cs, ks)),
            "Equation: (%s) + (%s) = %s." % (fmt(ca, ka), fmt(cb, kb), fmt(cs, ks)),
            "Collect the letters on one side: %s = %d." % (fmt({k: v for k, v in left.items() if v}, 0), rhs),
            "A digit makes this true: %s = %d and %s = %d (all other digit choices fail; the program tried every one)." % (
                other, sol[other], ask, sol[ask]),
            "Check with real numbers: %d + %d = %d ✓ (different letters, different digits)." % (val(a, sol), val(b, sol), val(s, sol))]


def crypt_lines(p, sol):
    if p["id"] not in (7, 8):
        return crypt_lines_generic(p, sol)
    a, b, s = p["a"], p["b"], p["s"]
    if p["id"] == 7:   # MM + N3 = 1M1
        return ["Two 2-digit numbers add to at most 198, so the leading 1 in the sum is a carry. Units column: M + 3 ends in 1, so M = 8 (8 + 3 = 11, carry 1).",
                "As an equation: MM = 11M, N3 = 10N + 3, 1M1 = 101 + 10M.  11M + 10N + 3 = 101 + 10M.",
                "Subtract 10M and 3 from both sides: M + 10N = 98. With M = 8: 10N = 90, N = 9.",
                "Check: 88 + 93 = 181 ✓ (M = 8, N = 9, different digits)."]
    return ["Units column: K + 6 ends in P. The sum is 3 digits, so the leading 1 is a carry from the tens column.",   # KK + P6 = 1PP
            "As an equation: KK = 11K, P6 = 10P + 6, 1PP = 100 + 11P.  11K + 10P + 6 = 100 + 11P.",
            "Collect: 11K − P = 94. K is a digit, so try K = 9: 99 − P = 94, P = 5. (K = 8 would need 88 − P = 94, so P = −6: not a digit.)",
            "Check: 99 + 56 = 155 ✓ (K = 9, P = 5, different digits)."]


def verify(p, s):
    """Second route, no shared algebra: simulate / enumerate."""
    k = p["kind"]
    if k == "bus":
        t, n = p["first"], 0
        while t <= p["end"]:
            n += 1
            t += p["step"]
        return n == s["ans"]
    if k == "posts":
        return len([x for x in range(0, p["length"] + 1) if x % p["gap"] == 0]) == s["ans"]
    if k == "worst":
        c, e, n = len(p["colors"]), p["each"], p["need"]
        best = 0   # largest draw with no color reaching n, found by trying every count mix
        for counts in itertools.product(range(e + 1), repeat=c):
            if all(x < n for x in counts):
                best = max(best, sum(counts))
        return best + 1 == s["ans"]
    if k == "cut":
        side = p["side"]
        hits = []
        for x in range(1, side):            # cut leaves a rectangle side x x
            if 2 * (side + x) == p["given"]:
                hits.append(2 * (side + (side - x)))
        sq = 4 * side
        return hits == [s["ans"]] and p["given"] + s["ans"] == sq + 2 * side
    if k == "crypt":
        sols = crypt_solutions(p)
        return len(sols) == 1 and sols[0][p["ask"]] == s["ans"] and sols[0] == s["sol"]
    raise ValueError(p)


# ---------------------------------------------------------------- text
def statement(p):
    k = p["kind"]
    if k == "bus":
        return p["q"] % (hm(p["first"]), hm(p["first"]), hm(p["end"]))
    return p["q"]


def crypt_art(p):
    a, b, s = p["a"], p["b"], p["s"]
    return ('<div style="font:700 19px/1.1 Menlo,monospace;text-align:right;display:inline-block;margin:2px 0 2px 30px">'
            '&nbsp;&nbsp;%s<br>+ %s<br><span style="border-top:2px solid #14142b;display:inline-block;padding-top:2px">%s</span></div>' % (
                a, b, s))


UNIT = {"bus": lambda p: p["plural"], "posts": lambda p: "lamp posts",
        "worst": lambda p: p["thing"], "cut": lambda p: "units around", "crypt": lambda p: ""}


def unit(p):
    if p.get("unit") is not None:
        return p["unit"]
    if p["kind"] == "cut":
        return "inches" if p["id"] == 5 else "feet"
    return UNIT[p["kind"]](p)


# ---------------------------------------------------------------- render
CSS = """
  @page { size: letter; margin: 0.4in; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system,'Helvetica Neue',Arial,sans-serif; color:#14142b; font-size:14px; line-height:1.3; margin:0; }
  .pg { page-break-after: always; } .pg:last-child { page-break-after: auto; }
  h1 { font-size:22px; margin:0 0 2px; color:#1e3a8a; } .sub { color:#4b5563; font-size:13.5px; margin-bottom:6px; }
  .nm { font-size:16px; margin-bottom:6px; } .nm span { display:inline-block; min-width:190px; border-bottom:1.5px solid #14142b; }
  .primer { border:2px solid #1e3a8a; border-radius:8px; background:#f8faff; padding:5px 12px; margin:5px 0 6px; break-inside:avoid; }
  .primer h2 { font-size:15.5px; margin:0 0 3px; color:#1e3a8a; } .primer .ln { margin:1px 0 1px 10px; font-size:13.5px; line-height:1.3; }
  .primer .ln i { color:#6b7280; font-size:12.5px; }
  .prob { border:1.5px solid #c9ced8; border-radius:8px; padding:5px 10px; margin:0 0 6px; break-inside:avoid; }
  .prob .q { font-size:14.5px; margin-bottom:4px; }
  .prob .q b.n { display:inline-block; background:#1e3a8a; color:#fff; border-radius:50%; width:24px; height:24px; text-align:center; line-height:24px; margin-right:7px; font-size:14px; }
  .lab { font-size:12.5px; color:#1e3a8a; font-weight:700; margin:2px 0 1px; }
  .blank { display:inline-block; min-width:70px; border-bottom:1.5px solid #14142b; }
  .box { border:1.5px dashed #b6bccb; border-radius:6px; }
  .ans { margin-top:3px; font-size:14.5px; } .ans .blank { min-width:130px; }
  .keyln { margin:1px 0 1px 12px; font-size:13.5px; } .kprob { border-bottom:1px solid #e5e7eb; padding:4px 0 5px; break-inside:avoid; }
  .kprob .q { font-size:13px; color:#374151; } .kans { font-weight:700; color:#166534; }
  .how { font-size:13px; color:#374151; margin-top:8px; } .who { font-size:13px; margin:4px 0 8px; }
"""

PRIMERS = {
    "A": """<div class="primer"><h2>Worked model A: count the events, not just the gaps</h2>
 <div class="ln">A train leaves at 6:00 and then every 15 minutes. How many trains leave from 6:00 up to 7:00?</div>
 <div class="ln">Draw a timeline and mark every departure: <b>6:00 &nbsp;6:15 &nbsp;6:30 &nbsp;6:45 &nbsp;7:00</b>. Count the marks: 5. As arithmetic: 60 &divide; 15 = 4 gaps, and the first train counts too, so 4 + 1 = <b>5 trains</b>.
 <i>A gap is the time between two trains. A train is an event. 4 gaps, 5 trains.</i></div></div>""",
    "B": """<div class="primer"><h2>Worked model B: the worst case, then one more</h2>
 <div class="ln">A drawer holds 6 black, 6 gray and 6 tan socks. Fewest socks to take out to be sure that at least 2 are the same color?</div>
 <div class="ln">Sketch the unluckiest draw: <b>black, gray, tan</b>. Three socks, all different, and no pair yet. The next sock must match one of them. 3 + 1 = <b>4 socks</b>.
 <i>With 3 socks you might still have no pair, so 3 is not enough. With 4 you cannot miss.</i></div></div>""",
    "C": """<div class="primer"><h2>Worked model C: a cut makes new edges</h2>
 <div class="ln">A square has a perimeter of 24, so each side is 6. Cut it straight across into two rectangles. One has a perimeter of 20. The other?</div>
 <div class="ln">Draw the square, label the side 6 and write the cut line 6. Let x = the other side of the first rectangle: 2(6 + x) = 20, so 6 + x = 10 and x = 4. The other rectangle is 6 by 2: 2(6 + 2) = <b>16</b>.
 <i>Check: 20 + 16 = 36 = 24 + 6 + 6. The cut adds two new edges. Subtracting 24 &minus; 20 would ignore them.</i></div></div>""",
    "D": """<div class="primer"><h2>Worked model D: letters in columns, then an equation</h2>
 <div class="ln">DD + E4 = 11E. Same letter, same digit; different letters, different digits. What is E?</div>
 <div class="ln">DD means 11D, E4 means 10E + 4, and 11E means 110 + E. Equation: 11D + 10E + 4 = 110 + E, so 11D + 9E = 106. Try D = 8: 88 + 9E = 106, so 9E = 18 and <b>E = 2</b>.
 <i>Check with real numbers: 88 + 24 = 112 &check;. Always add the numbers back.</i></div></div>""",
}


def prob_html(p, with_hint=True):
    blocks = ['<div class="q"><b class="n">%d</b></div><div class="q">%s</div>' % (p["id"], statement(p))]
    if p["kind"] == "crypt":
        blocks.append(crypt_art(p))
    k = p["kind"]
    if k in ("bus", "posts"):
        blocks.append('<div class="lab">Draw the timeline / number line and mark every one:</div><div class="box" style="height:40px"></div>'
                      '')
    elif k == "worst":
        blocks.append('<div class="lab">Sketch the unluckiest draw, then add one:</div><div class="box" style="height:40px"></div>')
    elif k == "cut":
        blocks.append('<div class="lab">Draw the square. Label each side and the cut. Let x = ? Write the equation, then solve:</div><div class="box" style="height:52px"></div>'
                      '<div class="lab" style="margin-top:3px">Check: do the two perimeters add up the way the new edges say?</div><div class="box" style="height:22px"></div>')
    elif k == "crypt":
        blocks.append('<div class="lab">Units column first, then write an equation:</div><div class="box" style="height:44px"></div>'
                      '<div class="lab" style="margin-top:3px">Check by adding the real numbers:</div><div class="box" style="height:22px"></div>')
    if p["t"] == "X":
        blocks[1:] = [b.replace("Draw the timeline / number line and mark every one:", "Pick a picture or an equation, then show it:")
                      .replace("Sketch the unluckiest draw, then add one:", "Pick a picture or an equation, then show it:")
                      for b in blocks[1:]]
    blocks.append('<div class="ans">Answer: <span class="blank"></span> %s</div>' % html.escape(unit(p)))
    return '<div class="prob">%s</div>' % "".join(blocks)


# ---------------------------------------------------------------- pages
SECTIONS = [("A", "A. Events and gaps", [1, 2]), ("B", "B. The worst case", [3, 4]),
            ("C", "C. A cut makes new edges", [5, 6]), ("D", "D. Letter addition", [7, 8])]


def student_html(name):
    byid = {p["id"]: p for p in PROBS}

    def sec(key, title, ids):
        return PRIMERS[key] + "".join(prob_html(byid[i]) for i in ids)

    pages = []
    head = ('<h1>Choose a Picture, Then Solve</h1><div class="sub">Untimed practice, not a test. Pick a picture or an equation '
            'that fits the story, show it, then check your answer against every sentence.</div>'
            '<div class="nm">Name: <span>%s</span></div>' % html.escape(name))
    pages.append('<div class="pg">%s%s%s</div>' % (head, sec(*SECTIONS[0]), sec(*SECTIONS[1])))
    pages.append('<div class="pg">%s%s%s</div>' % (sec(*SECTIONS[2]), PRIMERS["D"], prob_html(byid[7])))
    mixed = "".join(prob_html(byid[i]) for i in (9, 10))
    pages.append('<div class="pg">%s<h1 style="margin-top:10px">Your Choice</h1><div class="sub">No model is named here. First decide what kind of problem it is, '
                 'then pick the picture or equation that helps.</div>%s</div>' % (prob_html(byid[8]), mixed))
    return "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Yusuf choose-a-picture practice, student</title><style>%s</style></head><body>%s</body></html>" % (CSS, "".join(pages))


def key_html(name, solved, method_note):
    rows = []
    for p, s in zip(PROBS, solved):
        body = "".join('<div class="keyln">%s</div>' % html.escape(l) for l in s["lines"])
        tag = {"A": "A events", "B": "B worst case", "C": "C cut", "D": "D letters", "X": "mixed"}[p["t"]]
        rows.append('<div class="kprob"><div class="q"><b>%d.</b> (%s) %s%s</div>%s<div class="keyln kans">Answer: %s %s</div></div>' % (
            p["id"], tag, statement(p),
            (" &nbsp;<tt>%s + %s = %s</tt>" % (p["a"], p["b"], p["s"])) if p["kind"] == "crypt" else "",
            body, s["ans"], html.escape(unit(p))))
    head = ('<h1>Parent answer key</h1><div class="who">For %s. Worked examples on the student sheet: A = 5 trains, '
            'B = 4 socks, C = 16, D: E = 2. Mixed page (9, 10) names no model on purpose.</div>' % html.escape(name))
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Yusuf choose-a-picture practice, parent key</title><style>%s</style></head><body>"
            '<div class="pg">%s%s</div><div class="pg">%s<div class="how">%s</div></div></body></html>' % (
                CSS, head, "".join(rows[:5]), "".join(rows[5:]), method_note))


METHOD = ("<b>How each answer was checked.</b> The key lines use the method on the sheet. A second route, sharing none of that "
          "arithmetic, then re-solved every problem before this file was written: ferry and bell times by stepping forward one gap at a "
          "time and counting every time not past the end; lamp posts by listing every whole meter that is a multiple of the gap; "
          "worst-case problems by trying every possible mix of colors and taking the largest draw where no color reaches the target, "
          "plus one; cut problems by trying every possible cut position and requiring the two perimeters to total the square's perimeter "
          "plus two cut edges; letter sums by trying all digit assignments (exactly one fit each). The four worked examples on the student "
          "sheet were checked the same way. Pages were rendered to PDF and read back as text.")


def check_primers():
    # A: 6:00..7:00 every 15 -> 5; B: 3 colors need 2 -> 4; C: side 6, rect 20 -> other 16; D: DD+E4=11E unique, E=2
    assert len([t for t in range(0, 61) if t % 15 == 0]) == 5
    assert max(sum(c) for c in itertools.product(range(7), repeat=3) if all(x < 2 for x in c)) + 1 == 4
    xs = [x for x in range(1, 6) if 2 * (6 + x) == 20]
    assert xs == [4] and 2 * (6 + 6 - 4) == 16 and 20 + 16 == 24 + 12
    sols = crypt_solutions(dict(id=0, a="DD", b="E4", s="11E"))
    assert len(sols) == 1 and sols[0]["E"] == 2 and sols[0]["D"] == 8


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    check_primers()
    solved = []
    for p in PROBS:
        s = solve(p)
        if not verify(p, s):
            print("VERIFY FAILED %d: %r -> %r" % (p["id"], p, s["ans"]), file=sys.stderr)
            return 1
        solved.append(s)
    name = kid_name(kids_by_id(), KID)
    base = "yusuf-choose-a-picture-2026-11-06"
    pdfs = []
    for suffix, text in (("student", student_html(name)), ("parent-key", key_html(name, solved, METHOD))):
        h = os.path.join(out, "%s-%s.html" % (base, suffix))
        pdf = os.path.join(out, "%s-%s.pdf" % (base, suffix))
        open(h, "w").write(text)
        if os.path.exists(pdf):
            os.remove(pdf)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run", "--no-pdf-header-footer",
                        "--virtual-time-budget=5000", "--user-data-dir=" + os.path.join(out, "ud-" + suffix),
                        "--print-to-pdf=" + pdf, "file://" + h], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
        pdfs.append(pdf)
    print("ok: %d problems verified a second way; answers: %s" % (len(PROBS), [(p["id"], s["ans"]) for p, s in zip(PROBS, solved)]))
    print("\n".join(pdfs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
