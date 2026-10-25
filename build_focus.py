"""build_focus.py -- render the Noetic-prep focus-track word sheets (one kid per spec).

A spec names its child with spec["kid"] (default kid1) and its method with
spec["kind"] ("undo", default, or "trade"). kid1 = "undo the steps"; kid2 = "trade it".

    python3 build_focus.py            # writes worksheet-focus-<date>-<topic>.html + -key.html
    python3 verify_focus.py           # MUST exit 0 before anything is rendered or printed
    ./print-worksheet.sh worksheet-focus-2026-10-25-undo.html --dry-run   # render check

WHY TWO FILES, NOT ONE: the brief for this track is "student sheet and key as
SEPARATE PDFs". The student file has one .sheet block, the key file has one, so
print-worksheet.sh's page-count self-check (one page per .sheet) works on each.

WHY NOT build_sheets.build(): that builder is hard-wired to BOTH kids plus a key in
one file. This track is one kid. It reuses build_sheets.CSS and build_sheets._problem
so the print-worksheet.sh CSS literals stay byte-identical (verify_focus.py asserts
them), and takes the child's name from kids.local.json like every other generator.

The outputs carry a real name in the Name: field, so they are GITIGNORED
(worksheet-focus-*.html). The spec and this builder carry no name.
"""
import os
import sys

import build_sheets
import specs_focus
from kids_config import kids_by_id, kid_name, grade_label

KID = "kid1"   # default when a spec names no kid


# ONE STEP PER LINE (Asif, 2026-10-25): "we want to see one step simplified at each
# expression ... they're thinking too much in their head because they don't like
# writing." Every worked example, guided problem, work area and key line is a LADDER:
# each line copies the one above with exactly ONE thing changed, and the arithmetic
# that made the change sits beside it as "work". The ladder lines are the deliverable.
LADDER_CSS = """
  .space { height: 150px; border-top: 1px dashed #bbb; position: relative; }
  .ladder-cols { display: flex; gap: 14px; }
  .ladder-cols > div { flex: 1; }
  .scaffold.two { display: grid; grid-template-columns: 1fr 1fr; column-gap: 14px; }
  .teach .rungs { font-size: 12.5px; margin: 1px 0 2px 6px; line-height: 1.3; }
  .teach .rungs i { color: #6b7280; font-size: 12px; }
"""


def _plural(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


def _arrows(ops, value):
    """'? -> x4 -> -7 -> 29'; with no ops left it is '? = value'."""
    if not ops:
        return "? = <b>%d</b>" % value
    return " &rarr; ".join(["?"] + ["%s%d" % (specs_focus.OPS[s][3], n) for s, n in ops]
                           + [str(value)])


def undo_ladder(secret, ops):
    """Rungs for 'undo the steps': drop the LAST arrow each line, one undo per line."""
    result = specs_focus.run_forward(secret, ops)
    rungs = [(_arrows(ops, result), "the whole story")]
    for i, (a, s, n, b) in enumerate(specs_focus.undo_trail(result, ops)):
        left = ops[:len(ops) - 1 - i]
        rungs.append((_arrows(left, b), "undo %s%d: %d %s %d = %d"
                      % (specs_focus.OPS[ops[len(ops) - 1 - i][0]][3],
                         ops[len(ops) - 1 - i][1], a, s, n, b)))
    return rungs


def trade_ladders(names, a, b, k, T, c, d):
    """Two ladders: find ONE unit, then answer the question. One change per line."""
    a1, am, b1, bm = names
    n, m = a * k + b, c * k + d
    pb = T // n
    unit = [("%s + %s = $%d" % (_plural(a, a1, am), _plural(b, b1, bm), T), "the story"),
            ("%s + %s = $%d" % (_plural(a * k, b1, bm), _plural(b, b1, bm), T),
             "trade: 1 %s = %s" % (a1, _plural(k, b1, bm))),
            ("%s = $%d" % (_plural(n, b1, bm), T), "%d + %d = %d" % (a * k, b, n)),
            ("1 %s = $%d" % (b1, pb), "$%d &divide; %d = $%d" % (T, n, pb))]
    asked = [("%s + %s" % (_plural(c, a1, am), _plural(d, b1, bm)), "the question"),
             ("= %s + %s" % (_plural(c * k, b1, bm), _plural(d, b1, bm)), "trade"),
             ("= %s" % _plural(m, b1, bm), "%d + %d = %d" % (c * k, d, m)),
             ("= $%d" % (m * pb), "%d &times; $%d = $%d" % (m, pb, m * pb))]
    return unit, asked


def _rungs_html(rungs):
    return "<br>".join("%s &nbsp; <i>(%s)</i>" % (line, why) for line, why in rungs)


def _example_html(ex):
    secret, ops = ex["secret"], ex["ops"]
    result = specs_focus.run_forward(secret, ops)
    rungs = undo_ladder(secret, ops)
    a2 = specs_focus.undo_trail(result, ops)[0][3]
    return "\n".join([
        '  <div class="teach">',
        '    <div class="teach-title">HOW IT WORKS &mdash; ONE STEP PER LINE</div>',
        '    <div class="prompt">%s thinks of a number. He multiplies it by 5, then adds 8. '
        'He gets %d. What was his number?</div>' % (ex["who"], result),
        '    <div class="rungs">%s</div>' % _rungs_html(rungs),
        '    <div class="punch"><b>The rule:</b> copy the line, undo <b>ONE</b> arrow (the last one). '
        'Stop only when no arrows are left: %d is the middle, not the answer. '
        'Check: %d &times; 5 + 8 = %d.</div>' % (a2, secret, result),
        '  </div>', ''])


def _chip(text, fill):
    return ('<span style="display:inline-block;border:1.5px solid #1e3a8a;'
            'border-radius:4px;padding:0 6px;margin:0 1px;background:%s;'
            'font-size:12px">%s</span>' % (fill, text))


def _trade_example_html(ex):
    """Worked example, every number computed from the same (a,b,k,T,c,d) the problems use."""
    a, b, k, T, c, d = (ex[x] for x in "abkTcd")
    n = a * k + b
    pb = T // n
    assert T % n == 0 and a * k * pb + b * pb == T
    jar, quill = _chip("jar", "#fff"), _chip("quill", "#fde68a")
    unit, asked = trade_ladders(("jar", "jars", "quill", "quills"), a, b, k, T, c, d)
    return "\n".join([
        '  <div class="teach">',
        '    <div class="teach-title">HOW IT WORKS &mdash; ONE STEP PER LINE</div>',
        '    <div class="prompt">Sana buys %d jars of ink and %d quills for $%d. One jar costs '
        'the same as %d quills. How much do %d jars and %d quill cost?</div>' % (a, b, T, k, c, d),
        '    <div class="step">The trade: %s = %s</div>' % (jar, " ".join([quill] * k)),
        '    <div class="ladder-cols"><div class="rungs"><b>Find one quill</b><br>%s</div>'
        '<div class="rungs"><b>Answer the question</b><br>%s</div></div>'
        % (_rungs_html(unit), _rungs_html(asked)),
        '    <div class="punch"><b>The rule:</b> copy the line and change <b>ONE</b> thing. '
        'Do not divide $%d by the %d items you can see: a jar is not one quill.</div>' % (T, a + b),
        '  </div>', ''])


def _problem(i, p, kind):
    """build_sheets._problem, with the work box swapped for a big OPEN space (no ruled lines:
    Asif 2026-10-25, lines make them write too small or too big). The step count is
    enforced in the key's rubric, not by the page."""
    html = build_sheets._problem(i, p)
    if p.get("guided"):
        if kind == "trade":
            html = html.replace('<div class="scaffold">', '<div class="scaffold two">')
        return html
    label = ("Find ONE first, then answer the question. One step per line."
             if kind == "trade" else "Line 1: the story as arrows. Then ONE undo per line.")
    old = '<div class="work"><span class="work-label">SHOW YOUR THINKING</span></div>'
    assert old in html
    return html.replace(old, '<div class="space"><span class="work-label">%s</span></div>' % label)


def _key_steps(p, kind):
    if kind == "trade":
        unit, asked = trade_ladders(p["names"], p["a_n"], p["b_n"], p["k"], p["T"],
                                    p["c_n"], p["d_n"])
        flat = lambda rungs: " &nbsp;|&nbsp; ".join(line for line, _ in rungs)
        return "<b>Find one:</b> %s<br><b>Question:</b> %s" % (flat(unit), flat(asked))
    return _rungs_html(undo_ladder(p["secret"], p["ops"]))


def _sheet_head(spec, name, grade, cont=False):
    title = spec["title"] + (" &mdash; page 2" if cont else "")
    return ['<div class="sheet">',
            '  <div class="header">', "    <div>",
            "      <h1>%s</h1>" % title,
            '      <div class="sub">%s</div>' % spec["sub"],
            "    </div>", '    <div class="grade">%s</div>' % grade, "  </div>",
            '  <div class="meta">',
            "    <div>Name: <span>&nbsp;%s</span></div>" % name,
            "    <div>Date: <span>&nbsp;%s</span></div>" % spec["date"],
            "  </div>", ""]


def build_student(spec, name, grade):
    """TWO pages, one .sheet each (both carry the Name, so print-worksheet.sh --kid and its
    page-count check work): page 1 = worked example + problems 1-2, page 2 = problems 3-4.
    One page could not hold four ladders at a height a child can write on (2026-10-25)."""
    h = ['<!DOCTYPE html>', '<html lang="en">', "<head>", '<meta charset="UTF-8">',
         "<title>%s</title>" % spec["title_plain"], "<style>", build_sheets.CSS, LADDER_CSS,
         "</style>", "</head>", "<body>", ""]
    h += _sheet_head(spec, name, grade)
    h.append((_trade_example_html if spec.get("kind") == "trade" else _example_html)(
        spec["example"]))
    for i, p in enumerate(spec["problems"], 1):
        if i == 3:  # page 1: example + 1-2; page 2: 3-5
            h += ["</div>", ""] + _sheet_head(spec, name, grade, cont=True)
        h.append(_problem(i, p, spec.get("kind")))
        h.append("")
    h += ["</div>", "", "</body>", "</html>", ""]
    return "\n".join(h)


def build_key(spec, name, grade):
    h = ['<!DOCTYPE html>', '<html lang="en">', "<head>", '<meta charset="UTF-8">',
         "<title>%s - key</title>" % spec["title_plain"], "<style>", build_sheets.CSS, LADDER_CSS,
         "</style>", "</head>", "<body>", "",
         '<div class="sheet key">',
         '  <div class="header">', "    <div>", "      <h1>&#128273; Answer Key</h1>",
         '      <div class="sub">%s &mdash; for the grown-ups, worked steps included</div>'
         % spec["title_plain"],
         "    </div>", '    <div class="grade">Coach</div>', "  </div>", ""]
    h.append('  <div class="section-title">%s &mdash; %s</div>' % (grade, name))
    for i, p in enumerate(spec["problems"], 1):
        h += ['  <div class="ans"><b>%d. %s</b>' % (i, p["a"]),
              '    <div class="steps">%s</div>' % _key_steps(p, spec.get("kind")), "  </div>"]
    rows = []
    for i, p in enumerate(spec["problems"], 1):
        n = 8 if spec.get("kind") == "trade" else len(p["ops"]) + 1
        rows.append("<tr><td>#%d</td><td>%d lines</td><td>&#9744;</td><td>&#9744;</td></tr>" % (i, n))
    h.append('  <div class="watch"><b>Grade the LINES first, the answer second.</b> One step per line: '
             'each line copies the one above with ONE thing changed. A right answer without its lines '
             'is <b>UNSHOWN</b>, not a pass; send it back to write the lines.'
             '<table class="rubric"><tr><th>Problem</th><th>Lines expected</th><th>Lines there</th>'
             '<th>Answer right</th></tr>%s</table></div>' % "".join(rows))
    h.append('  <div class="watch"><b>Watch for:</b><br>%s</div>' % "<br>".join(
        "<b>#%d</b> %s" % (i, p["watch"]) for i, p in enumerate(spec["problems"], 1)))
    h += ["", "</div>", "", "</body>", "</html>", ""]
    return "\n".join(h)


def main():
    kids = kids_by_id()
    for spec in specs_focus.ALL:
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
