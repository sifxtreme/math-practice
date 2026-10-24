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


def _example_html(ex):
    secret, ops = ex["secret"], ex["ops"]
    result = specs_focus.run_forward(secret, ops)
    trail = specs_focus.undo_trail(result, ops)
    fwd = " &rarr; ".join(["?"] + ["%s%d" % (specs_focus.OPS[s][3], n) for s, n in ops]
                          + [str(result)])
    (a1, s1, n1, b1), (a2, s2, n2, b2) = trail
    return "\n".join([
        '  <div class="teach">',
        '    <div class="teach-title">HOW IT WORKS</div>',
        '    <div class="prompt">%s thinks of a number. He multiplies it by 5, then adds 8. '
        'He gets %d. What was his number?</div>' % (ex["who"], result),
        '    <div class="step"><b>Step 1 &mdash; Draw the arrows, forward.</b> %s</div>' % fwd,
        '    <div class="step"><b>Step 2 &mdash; Undo them, LAST arrow first.</b> '
        'Each undo is the opposite: add 8 becomes <b>subtract 8</b>; multiply by 5 '
        'becomes <b>divide by 5</b>.</div>',
        '    <div class="step"><b>Step 3 &mdash; Do the undos.</b> %d %s %d = %d, then '
        '%d %s %d = <b>%d</b>.</div>' % (a1, s1, n1, b1, a2, s2, n2, b2),
        '    <div class="step"><b>Step 4 &mdash; Check forward.</b> %d &times; 5 = %d, '
        '%d + 8 = %d. It lands on %d.</div>' % (b2, a2, a2, result, result),
        '    <div class="punch"><b>The trap:</b> after the first undo you are '
        '<b>not at the start yet</b>. %d is only the middle. Keep undoing until every '
        'arrow is used up.</div>' % a2,
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
    pa = k * pb
    assert T % n == 0 and a * pa + b * pb == T
    jar, quill = _chip("jar", "#fff"), _chip("quill", "#fde68a")
    row = lambda items: " ".join(items)
    return "\n".join([
        '  <div class="teach">',
        '    <div class="teach-title">HOW IT WORKS</div>',
        '    <div class="prompt">Sana buys %d jars of ink and %d quills for $%d. One jar costs '
        'the same as %d quills. How much do %d jars and %d quill cost?</div>' % (a, b, T, k, c, d),
        '    <div class="step"><b>Step 1 &mdash; Draw it.</b> %s &nbsp;%s &nbsp;= $%d</div>'
        % (row([jar] * a), row([quill] * b), T),
        '    <div class="step"><b>Step 2 &mdash; Trade.</b> Every jar is worth %d quills: '
        '%s = %s. Swap them all.</div>' % (k, jar, row([quill] * k)),
        '    <div class="step"><b>Step 3 &mdash; One kind left.</b> %s &nbsp;= $%d. '
        '<b>One quill = $%d &divide; %d = $%d.</b></div>'
        % (_chip("%d quills" % n, "#fde68a"), T, T, n, pb),
        '    <div class="step"><b>Step 4 &mdash; Answer the question the same way.</b> '
        '%d jars + %d quill = %s &nbsp;= %d quills. %d &times; $%d = $%d.</div>'
        % (c, d, row([jar] * c + [quill] * d), c * k + d, c * k + d, pb, (c * k + d) * pb),
        '    <div class="punch"><b>The trap:</b> do not divide $%d by the %d items you can '
        'see. A jar is <b>not</b> one quill. Trade first, then count quills.</div>' % (T, a + b),
        '  </div>', ''])


def build_student(spec, name, grade):
    h = ['<!DOCTYPE html>', '<html lang="en">', "<head>", '<meta charset="UTF-8">',
         "<title>%s</title>" % spec["title_plain"], "<style>", build_sheets.CSS,
         "</style>", "</head>", "<body>", "",
         '<div class="sheet">',
         '  <div class="header">', "    <div>",
         "      <h1>%s</h1>" % spec["title"],
         '      <div class="sub">%s</div>' % spec["sub"],
         "    </div>", '    <div class="grade">%s</div>' % grade, "  </div>",
         '  <div class="meta">',
         "    <div>Name: <span>&nbsp;%s</span></div>" % name,
         "    <div>Date: <span>&nbsp;%s</span></div>" % spec["date"],
         "  </div>", "",
         (_trade_example_html if spec.get("kind") == "trade" else _example_html)(
             spec["example"])]
    for i, p in enumerate(spec["problems"], 1):
        h.append(build_sheets._problem(i, p))
        h.append("")
    h += ["</div>", "", "</body>", "</html>", ""]
    return "\n".join(h)


def build_key(spec, name, grade):
    h = ['<!DOCTYPE html>', '<html lang="en">', "<head>", '<meta charset="UTF-8">',
         "<title>%s - key</title>" % spec["title_plain"], "<style>", build_sheets.CSS,
         "</style>", "</head>", "<body>", "",
         '<div class="sheet key">',
         '  <div class="header">', "    <div>", "      <h1>&#128273; Answer Key</h1>",
         '      <div class="sub">%s &mdash; for the grown-ups, worked steps included</div>'
         % spec["title_plain"],
         "    </div>", '    <div class="grade">Coach</div>', "  </div>", ""]
    h.append('  <div class="section-title">%s &mdash; %s</div>' % (grade, name))
    for i, p in enumerate(spec["problems"], 1):
        h += ['  <div class="ans"><b>%d. %s</b>' % (i, p["a"]),
              '    <div class="steps">%s</div>' % p["steps"], "  </div>"]
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
