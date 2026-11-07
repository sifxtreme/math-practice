"""build_exam_practice_20.py -- Musa's ONE-DAY 20-problem practice sheet (2026-11-07): student PDF + parent key PDF.

Asif (2026-11-07): "we need to actually print 20 test problems for each child. 20."  Yesterday's set was 10 a day
over two days; this is all 20 on one sheet. Same topics and level as build_exam_practice.py (imports its solver,
independent verifier and wording), new numbers and stories, easier first.

    python3 build_exam_practice_20.py <outdir>

Writes <outdir>/musa-practice-2026-11-07-{student,parent-key}.pdf (Chrome headless). Never prints.
Every answer is computed by solve() and re-derived by verify() (brute force); the build fails on any mismatch,
and on any count other than 20 numbered problems.
"""
import html
import os
import subprocess
import sys

import build_exam_practice as bx
from kids_config import kids_by_id, kid_name

KID = "kid1"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = "musa-practice-2026-11-07"
bx.DATE_TAG = "2026-11-07"


def sub(a, b):
    return bx.arith_sub(a, b)


PROBLEMS = [
    # easier first: subtraction with add-back check
    sub(340, 70),
    sub(420, 180),
    sub(710, 365),
    dict(kind="arith", expr="5 × 6 + 4 × 3", op="mix1", vals=(5, 6, 4, 3)),
    dict(kind="arith", expr="3 × 5 + 4 × (10 − 6)", op="mix2", vals=(3, 5, 4, 10, 6)),
    # fewest / most in a group
    dict(kind="t19", n=18, g=11, k=9, club="coding club", half=True, ask="fewest"),
    dict(kind="t19", n=22, g=14, k=10, club="band", half=False, ask="fewest"),
    dict(kind="t19", n=20, g=13, k=12, club="hiking club", half=False, ask="fewest"),
    dict(kind="t19", n=24, g=9, k=12, club="robotics club", half=True, ask="most"),
    # two pair-totals and one known part
    dict(kind="t18", names=("Maryam", "Ismail", "Yara"), thing="stickers", verb="have", ab=140, cb=210, b=70),
    dict(kind="t18", names=("Tariq", "Dina", "Faisal"), thing="pages", verb="read", ab=260, cb=315, b=120),
    dict(kind="t18", names=("Hassan", "Layla", "Idris"), thing="grams of grapes", verb="ate", ab=180, cb=250, b=90),
    dict(kind="t18", names=("Salma", "Rami", "Nadia"), thing="cm of ribbon", verb="used", ab=95, cb=140, b=55),
    dict(kind="t18b", names=("Omar", "Sofia", "Bilal"), thing="apples", verb="picked", total3=380, ab=240, bc=210),
    # two prices, one count, one total
    dict(kind="t20", item_lo="pencils", item_hi="markers", lo=2, hi=3, n=7, total=17, buyer="Mina",
         ask="hi", noun="items", shop="A stationery stall"),
    dict(kind="t20", item_lo="red balloons", item_hi="gold balloons", lo=3, hi=5, n=10, total=38, buyer="Sami",
         ask="lo", noun="balloons", shop="A party shop"),
    dict(kind="t20", item_lo="postcards", item_hi="posters", lo=2, hi=5, n=8, total=28, buyer="Rayan",
         ask="hi", noun="prints", shop="A museum shop"),
    dict(kind="t20", item_lo="muffins", item_hi="pies", lo=4, hi=6, n=9, total=44, buyer="Leila",
         ask="lo", noun="treats", shop="A café"),
    dict(kind="t20", item_lo="small plants", item_hi="large plants", lo=3, hi=4, n=12, total=41, buyer="Jamal",
         ask="hi", noun="plants", shop="A garden stand"),
    dict(kind="t20", item_lo="ride tickets", item_hi="game tickets", lo=2, hi=5, n=10, total=32, buyer="Nura",
         ask="lo", noun="tickets", shop="A fair booth"),
]
assert len(PROBLEMS) == 20

CSS = bx.CSS + "\n  @page { @top-left { content: \"NAME - practice 2026-11-07\"; font-size: 10px; } @bottom-right { content: \"Page \" counter(page); font-size: 10px; } }\n  .prob .q b.n { background:#000; }  .primer { background:#fff; border-color:#000; }  h1,.primer h2,.lab { color:#000; }\n  .kans { color:#000; }\n  .prob .q.qt { margin-top:0; } .prob .q:first-child { margin-bottom:1px; }\n"


# Stacked full-width problems (no side-by-side rows) so the PDF text reads 1..20 in order.
_frame = bx.frame_for
bx.frame_for = lambda p: _frame(p).replace("height:92px", "height:72px").replace("height:62px", "height:50px")


def student_html(name):
    head = ('<h1>Practice: 20 problems</h1>'
            '<div class="sub">Untimed. This is practice, not a test: the goal is to show each step. '
            'Write what each letter means, write the equation, then one step per line. Problems go from easier to harder.</div>'
            '<div class="nm">Name: <span>%s</span></div>%s' % (html.escape(name), bx.primer_day1()))
    body = "".join(bx.student_problem(i, p) for i, p in enumerate(PROBLEMS, 1))
    return "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Practice 2026-11-07, student</title><style>%s</style></head><body>%s%s</body></html>" % (CSS.replace('NAME', html.escape(name)), head, body)


def key_html(name, solved):
    rows = []
    for i, (p, s) in enumerate(zip(PROBLEMS, solved), 1):
        body = "".join('<div class="keyln">%s</div>' % html.escape(l) for l in s["lines"])
        rows.append('<div class="kprob"><div class="q"><b>%d.</b> %s</div>%s<div class="keyln kans">Answer: %s %s</div></div>' % (
            i, bx.statement(p), body, s["ans"], html.escape(bx.unit_of(p))))
    head = ('<h1>Parent answer key</h1><div class="sub">For %s\'s 20-problem practice sheet, 2026-11-07. Every answer was '
            'computed by the program and re-solved a second way (counting up, repeated addition, trying every whole number, '
            'trying every possible number of girls) before this key was written.</div>' % html.escape(name))
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Practice 2026-11-07, key</title><style>%s</style></head><body>"
            '<div class="pg">%s%s</div><div class="pg">%s</div></body></html>' % (
                CSS.replace('NAME', html.escape(name)), head, "".join(rows[:8]), "".join(rows[8:])))


def to_pdf(text, out, suffix):
    h = os.path.join(out, "%s-%s.html" % (BASE, suffix))
    pdf = os.path.join(out, "%s-%s.pdf" % (BASE, suffix))
    open(h, "w").write(text)
    if os.path.exists(pdf):
        os.remove(pdf)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run", "--no-pdf-header-footer",
                    "--virtual-time-budget=5000", "--user-data-dir=" + os.path.join(out, "ud-" + suffix),
                    "--print-to-pdf=" + pdf, "file://" + h], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    return pdf


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    solved = []
    for i, p in enumerate(PROBLEMS, 1):
        s = bx.solve(p)
        if not bx.verify(p, s):
            print("VERIFY FAILED %d: %r -> %r" % (i, p, s["ans"]), file=sys.stderr)
            return 1
        solved.append(s)
    name = kid_name(kids_by_id(), KID)
    pdfs = [to_pdf(student_html(name), out, "student"), to_pdf(key_html(name, solved), out, "parent-key")]
    print("ok: %d problems verified a second way; answers: %s" % (len(PROBLEMS), [s["ans"] for s in solved]))
    print("\n".join(pdfs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
