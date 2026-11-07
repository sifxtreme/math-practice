"""build_yusuf_practice_20.py -- Yusuf's ONE-DAY 20-problem "choose a picture" sheet (2026-11-07): student PDF + parent key PDF.

Asif (2026-11-07): "we need to actually print 20 test problems for each child. 20."  Yesterday's set was 10 problems.
Same four types and worked models as build_yusuf_practice.py (imports its solver, independent brute-force verifier,
wording and primers), new numbers and stories: A events/gaps x4, B worst case x4, C cut makes new edges x4,
D letter addition x4, then 4 mixed problems with no model named.  Easier first inside each section.

    python3 build_yusuf_practice_20.py <outdir>

Writes <outdir>/yusuf-choose-a-picture-2026-11-07-{student,parent-key}.pdf (Chrome headless). Never prints.
The build fails if any answer disagrees with its second route, or if the count is not 20.
"""
import html
import os
import re
import subprocess
import sys

import build_yusuf_practice as by
from kids_config import kids_by_id, kid_name

KID = "kid2"
BASE = "yusuf-choose-a-picture-2026-11-07"
T = by.T

BUS_Q = "A %s leaves the %s at %%s and then every %d minutes. How many %s leave the %s from %%s up to %%s?"

PROBS = [
    # ---- A: events vs intervals
    dict(id=1, t="A", kind="bus", first=T(6, 40), step=20, end=T(9, 0), what="bus", plural="buses",
         q=BUS_Q % ("bus", "station", 20, "buses", "station")),
    dict(id=2, t="A", kind="posts", length=30, gap=5, unit="fence posts",
         q="A straight fence is 30 meters long. Fence posts stand 5 meters apart, with a post at <b>both</b> ends of the fence. How many fence posts are there?"),
    dict(id=3, t="A", kind="bus", first=T(7, 45), step=25, end=T(10, 0), what="tram", plural="trams",
         q=BUS_Q % ("tram", "stop", 25, "trams", "stop")),
    dict(id=4, t="A", kind="posts", length=52, gap=4, unit="benches",
         q="A straight garden path is 52 meters long. Benches stand 4 meters apart, with a bench at <b>both</b> ends of the path. How many benches are there?"),
    # ---- B: worst case
    dict(id=5, t="B", kind="worst", colors=["black", "white", "gray"], each=10, need=2, thing="buttons",
         q="A bag holds 10 black, 10 white and 10 gray buttons, and nothing else. Without looking, what is the <b>fewest</b> buttons you must take out to be <b>sure</b> that at least 2 of them are the same color?"),
    dict(id=6, t="B", kind="worst", colors=["red", "blue", "green", "yellow"], each=12, need=2, thing="marbles",
         q="A box holds 12 red, 12 blue, 12 green and 12 yellow marbles, and nothing else. Without looking, what is the <b>fewest</b> marbles you must take out to be <b>sure</b> that at least 2 of them are the same color?"),
    dict(id=7, t="B", kind="worst", colors=["plain", "cheese", "seeded"], each=14, need=3, thing="crackers",
         q="A tin holds 14 plain, 14 cheese and 14 seeded crackers, and nothing else. Without looking, what is the <b>fewest</b> crackers you must take out to be <b>sure</b> that at least 3 of them are the same kind?"),
    dict(id=8, t="B", kind="worst", colors=["red", "blue", "green", "orange"], each=12, need=3, thing="pencils",
         q="A pouch holds 12 red, 12 blue, 12 green and 12 orange pencils, and nothing else. Without looking, what is the <b>fewest</b> pencils you must take out to be <b>sure</b> that at least 3 of them are the same color?"),
    # ---- C: a cut makes new edges
    dict(id=9, t="C", kind="cut", side=10, given=34, unit="centimeters",
         q="A square board has a perimeter of 40 centimeters. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 34 centimeters. What is the perimeter of the other rectangle?"),
    dict(id=10, t="C", kind="cut", side=6, given=16, unit="feet",
         q="A square mat has a perimeter of 24 feet. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 16 feet. What is the perimeter of the other rectangle?"),
    dict(id=11, t="C", kind="cut", side=7, given=24, unit="inches",
         q="A square card has a perimeter of 28 inches. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 24 inches. What is the perimeter of the other rectangle?"),
    dict(id=12, t="C", kind="cut", side=12, given=40, unit="inches",
         q="A square banner has a perimeter of 48 inches. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 40 inches. What is the perimeter of the other rectangle?"),
    # ---- D: letter addition
    dict(id=13, t="D", kind="crypt", a="SS", b="Z4", s="1ZZ", ask="Z",
         q="In this addition, the same letter is the same digit and different letters are different digits. What digit is Z?"),
    dict(id=14, t="D", kind="crypt", a="KK", b="N7", s="1NN", ask="N",
         q="In this addition, the same letter is the same digit and different letters are different digits. What digit is N?"),
    dict(id=15, t="D", kind="crypt", a="TT", b="R7", s="1T1", ask="T",
         q="In this addition, the same letter is the same digit and different letters are different digits. What digit is T?"),
    dict(id=16, t="D", kind="crypt", a="MM", b="P5", s="1M1", ask="M",
         q="In this addition, the same letter is the same digit and different letters are different digits. What digit is M?"),
    # ---- mixed: no model named
    dict(id=17, t="X", kind="bus", first=T(9, 10), step=15, end=T(10, 40), what="ring", plural="rings",
         q="A school bell rings at %s and then every 15 minutes. How many times does it ring from %s up to %s?"),
    dict(id=18, t="X", kind="worst", colors=["red", "blue", "green", "white", "black", "pink"], each=7, need=2, thing="socks",
         q="A drawer holds 7 red, 7 blue, 7 green, 7 white, 7 black and 7 pink socks, and nothing else. Without looking, what is the <b>fewest</b> socks you must take out to be <b>sure</b> that at least 2 of them are the same color?"),
    dict(id=19, t="X", kind="cut", side=9, given=28, unit="inches",
         q="A square sheet of paper has a perimeter of 36 inches. It is cut straight across into 2 rectangles. One rectangle has a perimeter of 28 inches. What is the perimeter of the other rectangle?"),
    dict(id=20, t="X", kind="posts", length=42, gap=6, unit="flag poles",
         q="A straight road is 42 meters long. Flag poles stand 6 meters apart, with a pole at <b>both</b> ends of the road. How many flag poles are there?"),
]
assert len(PROBS) == 20 and [p["id"] for p in PROBS] == list(range(1, 21))

# Black and white only: swap the blue/colored accents of the shared CSS for black and gray.
CSS = (by.CSS + "\n  @page { @top-left { content: \"NAME - choose a picture, 2026-11-07\"; font-size: 10px; } @bottom-right { content: \"Page \" counter(page); font-size: 10px; } }"
       "\n  h1,.primer h2,.lab { color:#000; } .prob .q b.n { background:#000; } .primer { background:#fff; border-color:#000; } .kans { color:#000; }\n")

_ph = by.prob_html


def prob_html(p, with_hint=True):
    h = _ph(p, with_hint)
    if p["kind"] == "crypt":   # float the sum to the right of the question so four letter sums share one page, work boxes stay full size
        art = re.search(r'<div style="font:700.*?</div>', h, re.S).group(0)
        h = h.replace(art, "")
        art = art.replace("display:inline-block;margin:2px 0 2px 30px", "display:inline-block;margin:0 40px 0 10px;float:right")
        h = h.replace('</div><div class="q">', '</div>' + art + '<div class="q">', 1)
    if p["kind"] == "cut":
        h = h.replace("height:52px", "height:42px").replace("height:22px", "height:16px")
    return h


by.prob_html = prob_html

HEADS = {"A": "A. Events and gaps", "B": "B. The worst case", "C": "C. A cut makes new edges", "D": "D. Letter addition"}


def student_html(name):
    byt = {}
    for p in PROBS:
        byt.setdefault(p["t"], []).append(p)
    pages = []
    head = ('<h1>Choose a Picture, Then Solve</h1><div class="sub">Untimed practice, not a test. 20 problems. Pick a picture or an equation '
            'that fits the story, show it, then check your answer against every sentence.</div>'
            '<div class="nm">Name: <span>%s</span></div>' % html.escape(name))
    for i, key in enumerate("ABCD"):
        pages.append('<div class="pg">%s%s%s</div>' % (head if i == 0 else "", by.PRIMERS[key], "".join(by.prob_html(p) for p in byt[key])))
    pages.append('<div class="pg"><h1>Your Choice</h1><div class="sub">No model is named here. First decide what kind of problem it is, '
                 'then pick the picture or equation that helps.</div>%s</div>' % "".join(by.prob_html(p) for p in byt["X"]))
    return "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Choose a picture 2026-11-07, student</title><style>%s</style></head><body>%s</body></html>" % (
        CSS.replace("NAME", html.escape(name)), "".join(pages))


def key_html(name, solved):
    rows = []
    for p, s in zip(PROBS, solved):
        body = "".join('<div class="keyln">%s</div>' % html.escape(l) for l in s["lines"])
        tag = {"A": "A events", "B": "B worst case", "C": "C cut", "D": "D letters", "X": "mixed"}[p["t"]]
        rows.append('<div class="kprob"><div class="q"><b>%d.</b> (%s) %s%s</div>%s<div class="keyln kans">Answer: %s %s</div></div>' % (
            p["id"], tag, by.statement(p),
            (" &nbsp;<tt>%s + %s = %s</tt>" % (p["a"], p["b"], p["s"])) if p["kind"] == "crypt" else "",
            body, s["ans"], html.escape(by.unit(p))))
    head = ('<h1>Parent answer key</h1><div class="who">For %s, 20-problem sheet, 2026-11-07. Worked examples on the student sheet: '
            'A = 5 trains, B = 4 socks, C = 16, D: E = 2 (they do not count toward the 20). Problems 17 to 20 name no model on purpose.</div>' % html.escape(name))
    pages = [head + "".join(rows[:5]), "".join(rows[5:10]), "".join(rows[10:15]), "".join(rows[15:]) + '<div class="how">%s</div>' % by.METHOD]
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Choose a picture 2026-11-07, key</title><style>%s</style></head><body>%s</body></html>" % (
        CSS.replace("NAME", html.escape(name)), "".join('<div class="pg">%s</div>' % x for x in pages)))


def to_pdf(text, out, suffix):
    h = os.path.join(out, "%s-%s.html" % (BASE, suffix))
    pdf = os.path.join(out, "%s-%s.pdf" % (BASE, suffix))
    open(h, "w").write(text)
    if os.path.exists(pdf):
        os.remove(pdf)
    subprocess.run([by.CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run", "--no-pdf-header-footer",
                    "--virtual-time-budget=5000", "--user-data-dir=" + os.path.join(out, "ud-" + suffix),
                    "--print-to-pdf=" + pdf, "file://" + h], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    return pdf


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    by.check_primers()
    solved = []
    for p in PROBS:
        s = by.solve(p)
        if not by.verify(p, s):
            print("VERIFY FAILED %d: %r -> %r" % (p["id"], p, s["ans"]), file=sys.stderr)
            return 1
        solved.append(s)
    name = kid_name(kids_by_id(), KID)
    pdfs = [to_pdf(student_html(name), out, "student"), to_pdf(key_html(name, solved), out, "parent-key")]
    print("ok: %d problems verified a second way; answers: %s" % (len(PROBS), [(p["id"], s["ans"]) for p, s in zip(PROBS, solved)]))
    print("\n".join(pdfs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
