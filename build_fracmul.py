"""build_fracmul.py -- render the simple-fraction MULTIPLICATION practice set (one kid).

    python3 build_fracmul.py          # writes worksheet-focus-<date>-fracmul.html + -key.html
    python3 verify_fracmul.py         # MUST exit 0 before anything is rendered or printed
    ./print-worksheet.sh worksheet-focus-2026-10-25-fracmul.html --dry-run   # page check

Same pattern as build_focus.py: one kid per spec, student sheet and key as two separate
files, build_sheets.CSS reused byte-for-byte (print-worksheet.sh rewrites its literals),
child name from kids.local.json via kids_config. Outputs match the gitignored
worksheet-focus-*.html glob because they carry a real name. Not folded into build_focus.py
because that builder is hard-wired to its two methods (undo / trade) and four-page layout.

Student file = 2 pages (one .sheet each, both carry Name:): 1 = worked example + Part A
(12 bare problems), 2 = Part B (3 compound word problems). Key file = 2 pages too, so
each stays one printed page.

ONE STEP PER LINE (Asif, 2026-10-25): every worked line and key line changes one thing.
"""
import sys
from fractions import Fraction
from math import gcd

import build_sheets
import specs_fracmul
from kids_config import kids_by_id, kid_name, grade_label

KID = "kid2"

CSS_EXTRA = """
  .fr { display: inline-block; vertical-align: middle; text-align: center; line-height: 1.15;
        margin: 0 3px; }
  .fr > span { display: block; padding: 0 3px; }
  .fr > span:first-child { border-bottom: 1.6px solid #14142b; }
  .walk { border: 2px solid #1e3a8a; border-radius: 8px; padding: 8px 14px; background: #f8faff; }
  .walk h2 { font-size: 17px; color: #1e3a8a; margin: 0 0 3px 0; }
  .cols { display: flex; gap: 18px; }
  .cols > div { flex: 1; }
  .ex { font-size: 14.5px; line-height: 1.85; }
  .ex i { color: #6b7280; font-size: 12px; }
  .ex .big { font-size: 16px; }
  .tip { margin-top: 5px; font-size: 12.5px; background: #fff7ed; border-left: 4px solid #b45309;
         padding: 4px 9px; }
  .parta { font-size: 15px; font-weight: bold; color: #fff; background: #1e3a8a;
           padding: 3px 10px; border-radius: 4px; margin: 10px 0 6px 0; }
  .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
  .cell { border: 1.5px solid #c7d2fe; border-radius: 6px; padding: 6px 10px; height: 126px;
          position: relative; }
  .cell .q { font-size: 18px; }
  .cell .qn { font-weight: bold; color: #1e3a8a; font-size: 14px; margin-right: 6px; }
  .cell .hint { position: absolute; left: 10px; top: 50px; font-size: 10px; color: #999;
                font-style: italic; }
  .cell .ans-line { position: absolute; left: 10px; bottom: 7px; font-size: 13px; }
  .cell .ans-line span { display: inline-block; border-bottom: 2px solid #14142b; width: 78px;
                         margin-left: 5px; }
  .space { height: 112px; border: 1.5px dashed #c7d2fe; border-radius: 6px; position: relative;
           margin-top: 5px; }
  .ln { font-size: 14px; }
  .answer-val { font-style: normal; }
  .key .ex { font-size: 11.5px; line-height: 1.5; }
  .key .ex .fr { margin: 0 2px; }
  .key .cols { gap: 8px; }
  .kgrid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0 8px; }
  .key .ans { margin-bottom: 6px; padding: 5px 8px; }
"""


def fr(f):
    """HTML for a fraction (n, d) tuple; a whole number (n, 1) prints as a plain number."""
    n, d = f
    if d == 1:
        return str(n)
    return '<span class="fr"><span>%d</span><span>%d</span></span>' % (n, d)


def mixed(x):
    """Fraction -> HTML in simplest form, mixed number when improper."""
    if x.denominator == 1:
        return str(x.numerator)
    whole, rem = divmod(x.numerator, x.denominator)
    f = fr((rem, x.denominator))
    return ("%d " % whole + f) if whole else f


def improper(x):
    return fr((x.numerator, x.denominator))


def ladder_mul(factors):
    """Key lines for a product of fractions, ONE change per line. Returns (lines, result)."""
    (an, ad), (bn, bd) = factors
    x = Fraction(an, ad) * Fraction(bn, bd)
    lines = [(" &times; ".join(fr(f) for f in factors), "")]
    if ad == 1 or bd == 1:
        # a whole number is a fraction over 1: show that as its own line
        over1 = lambda n, d: '<span class="fr"><span>%d</span><span>%d</span></span>' % (n, d)
        lines.append((" &times; ".join(over1(n, d) for n, d in factors), "a whole number is over 1"))
    lines.append(("= %s" % ('<span class="fr"><span>%d &times; %d</span><span>%d &times; %d</span></span>'
                            % (an, bn, ad, bd)), "tops, then bottoms"))
    pn, pd = an * bn, ad * bd
    lines.append(("= %s" % fr((pn, pd)), "multiply"))
    g = gcd(pn, pd)
    if g > 1:
        lines.append(("= %s" % fr((pn // g, pd // g)), "&divide;%d top and bottom" % g))
    if x.denominator > 1 and x.numerator > x.denominator:
        lines.append(("= %s" % mixed(x), "%d &divide; %d = %d remainder %d"
                      % (x.numerator, x.denominator, x.numerator // x.denominator,
                         x.numerator % x.denominator)))
    return lines, x


def _lines_html(lines):
    return "<br>".join("%s%s" % (l, (" &nbsp; <i>(%s)</i>" % why) if why else "")
                       for l, why in lines)


def _example(ex):
    f_lines, _ = ladder_mul(ex["fraction"])
    w_lines, _ = ladder_mul(ex["whole"])
    return "\n".join([
        '  <div class="walk">',
        "    <h2>How to multiply fractions: one step on each line</h2>",
        '    <div class="cols">',
        '      <div class="ex"><b>Fraction &times; fraction</b><br>%s</div>' % _lines_html(f_lines),
        '      <div class="ex"><b>Whole number &times; fraction</b><br>%s</div>' % _lines_html(w_lines),
        "    </div>",
        '    <div class="tip"><b>Remember:</b> multiply the TOPS, multiply the BOTTOMS, then '
        "simplify. A whole number is a fraction over 1. If the top is bigger than the bottom, "
        "write a mixed number.</div>",
        "  </div>", ""])


def _cell(i, p):
    return "\n".join([
        '    <div class="cell">',
        '      <div class="q"><span class="qn">%d.</span>%s =</div>'
        % (i, " &times; ".join(fr(f) for f in p["f"])),
        '      <div class="hint">tops &middot; bottoms &middot; simplify</div>',
        '      <div class="ans-line">Answer:<span></span></div>',
        "    </div>"])


def _story(p):
    vals = {k: (fr(v) if isinstance(v, tuple) else v) for k, v in p.items()}
    return p["story"].format(**vals)


def _wlines(p):
    """Key for a word problem as (groups, answer): groups = [(heading, lines)], one per step,
    each line changing ONE thing, built from the raw numbers."""
    k = p["kind"]
    if k == "fof_left":
        used_lines, used = ladder_mul([p["p"], p["q"]])
        pp = Fraction(*p["p"])
        left = pp - used
        lcm = pp.denominator * used.denominator // gcd(pp.denominator, used.denominator)
        a, b = pp * lcm, used * lcm
        sub = [("%s &minus; %s" % (fr(p["p"]), improper(used)), "had &minus; poured"),
               ("= %s &minus; %s" % (fr((int(a), lcm)), fr((int(b), lcm))), "common denominator %d" % lcm),
               ("= %s" % improper(left), "subtract the tops")]
        return [("Step 1: how much of the whole pot did she pour?", used_lines),
                ("Step 2: how much is left?", sub)], left
    if k == "whole_chain":
        l1, x1 = ladder_mul([(p["total"], 1), p["f1"]])
        l2, x2 = ladder_mul([(x1.numerator, 1), p["f2"]])
        return [("Step 1: how many have gold frames?", l1),
                ("Step 2: how many of those hang in the window?", l2)], x2
    if k == "area":
        l1, x1 = ladder_mul([p["l"], p["w"]])
        l2, x2 = ladder_mul([(p["n"], 1), (x1.numerator, x1.denominator)])
        return [("Step 1: area of one pane = length &times; width", l1),
                ("Step 2: %d panes" % p["n"], l2)], x2
    raise ValueError(k)


def _problem_b(i, p):
    return "\n".join([
        '  <div class="problem">',
        '    <span class="qnum">%d.</span>' % i,
        '    <div class="qtext">%s</div>' % _story(p),
        '    <div class="space"><span class="work-label">One step per line. Multiply, then '
        "simplify. Write what each line is for.</span></div>",
        '    <div class="answer">Answer:<span class="line"></span> %s</div>' % p["unit"],
        '    <div class="fact"><b>Did you know?</b> %s</div>' % p["fact"],
        "  </div>"])


def _head(spec, name, grade):
    return ['<div class="sheet">', '  <div class="header">', "    <div>",
            "      <h1>%s</h1>" % spec["title"],
            '      <div class="sub">%s</div>' % spec["sub"],
            "    </div>", '    <div class="grade">%s</div>' % grade, "  </div>",
            '  <div class="meta">',
            "    <div>Name: <span>&nbsp;%s</span></div>" % name,
            "    <div>Date: <span>&nbsp;%s</span></div>" % spec["date"],
            "  </div>", ""]


def _doc_open(title):
    return ['<!DOCTYPE html>', '<html lang="en">', "<head>", '<meta charset="UTF-8">',
            "<title>%s</title>" % title, "<style>", build_sheets.CSS, CSS_EXTRA, "</style>",
            "</head>", "<body>", ""]


def build_student(spec, name, grade):
    h = _doc_open(spec["title_plain"]) + _head(spec, name, grade)
    h.append(_example(spec["example"]))
    h.append('  <div class="parta">Part A &mdash; Multiply. Show every step. '
             "Answers in simplest form.</div>")
    h.append('  <div class="grid">')
    h += [_cell(i, p) for i, p in enumerate(spec["part_a"], 1)]
    h += ["  </div>", "</div>", ""]
    h += _head(spec, name, grade)
    h.append('  <div class="parta">Part B &mdash; Glass &amp; mirrors. Two steps each.</div>')
    for i, p in enumerate(spec["part_b"], 1):
        h += [_problem_b(i, p), ""]
    h += ["</div>", "", "</body>", "</html>", ""]
    return "\n".join(h)


def build_key(spec, name, grade):
    def key_head(sub):
        return ['<div class="sheet key">', '  <div class="header">', "    <div>",
                "      <h1>&#128273; Answer Key</h1>",
                '      <div class="sub">%s &mdash; %s</div>' % (spec["title_plain"], sub),
                "    </div>", '    <div class="grade">Coach</div>', "  </div>", ""]

    h = _doc_open(spec["title_plain"] + " - key") + key_head("Part A, worked steps")
    h.append('  <div class="section-title">%s &mdash; %s</div>' % (grade, name))
    h.append('  <div class="kgrid">')
    for i, p in enumerate(spec["part_a"], 1):
        lines, x = ladder_mul(p["f"])
        h += ['    <div class="ans"><b>%d. <em class="answer-val">%s</em></b>' % (i, mixed(x)),
              '      <div class="steps ex">%s</div>' % _lines_html(lines), "    </div>"]
    h += ["  </div>",
          '  <div class="watch"><b>Grade the LINES first, the answer second.</b> Tops, bottoms, '
          "simplify, each on its own line. A right answer with no lines is UNSHOWN, not a pass. "
          "Watch for: adding tops and bottoms; leaving 6/12 unsimplified; forgetting to turn an "
          "improper fraction into a mixed number.</div>",
          "</div>", ""]
    h += key_head("Part B, worked steps")
    for i, p in enumerate(spec["part_b"], 1):
        groups, x = _wlines(p)
        h += ['  <div class="ans"><b>%d. <em class="answer-val">%s</em> %s</b>'
              % (i, mixed(x), p["unit"]), '    <div class="cols">']
        for head, lines in groups:
            h.append('      <div class="steps ex"><b>%s</b><br>%s</div>' % (head, _lines_html(lines)))
        h += ["    </div>", "  </div>"]
    vals = lambda p: {k: (fr(v) if isinstance(v, tuple) else v) for k, v in p.items()}
    h.append('  <div class="watch"><b>Watch for:</b><br>%s</div>' % "<br>".join(
        "<b>#%d</b> %s" % (i, p["watch"].format(**vals(p))) for i, p in enumerate(spec["part_b"], 1)))
    h += ["", "</div>", "", "</body>", "</html>", ""]
    return "\n".join(h)


def main():
    kids = kids_by_id()
    for spec in specs_fracmul.ALL:
        kid = spec.get("kid", KID)
        name = kid_name(kids, kid)
        grade = grade_label(kids[kid])
        for fname, text in ((spec["file"], build_student(spec, name, grade)),
                            (spec["key_file"], build_key(spec, name, grade))):
            with open(fname, "w") as f:
                f.write(text)
            print("  wrote", fname)
    return 0


if __name__ == "__main__":
    sys.exit(main())
