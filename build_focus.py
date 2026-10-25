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
  .space { height: 285px; border-top: 1px dashed #bbb; position: relative; }
  .ladder-cols { display: flex; gap: 14px; }
  .ladder-cols > div { flex: 1; }
  .scaffold.two { display: grid; grid-template-columns: 1fr 1fr; column-gap: 14px; }
  .teach .rungs { font-size: 12.5px; margin: 1px 0 2px 6px; line-height: 1.3; }
  .teach .rungs i { color: #6b7280; font-size: 12px; }
  .walk { border: 2px solid #1e3a8a; border-radius: 8px; padding: 10px 14px; background: #f8faff; }
  .walk h2 { font-size: 19px; color: #1e3a8a; margin: 0 0 4px 0; }
  .wstep { margin: 14px 0 0 0; font-size: 15.5px; }
  .scaffold.walk-g { color: #14142b; font-size: 15px; }
  .wstep .n { display: inline-block; background: #1e3a8a; color: #fff; border-radius: 50%;
              width: 22px; height: 22px; text-align: center; line-height: 22px;
              font-weight: bold; margin-right: 6px; }
  .wpic { margin: 8px 0 0 30px; font-size: 15px; }
  .mbox { display: inline-block; min-width: 54px; height: 38px; border: 2px solid #1e3a8a;
          border-radius: 6px; text-align: center; line-height: 38px; font-weight: bold;
          font-size: 18px; background: #fff; vertical-align: middle; padding: 0 4px; }
  .arr { display: inline-block; text-align: center; margin: 0 5px; color: #1e3a8a;
         vertical-align: middle; font-size: 13px; line-height: 1.1; }
  .arr .op { display: inline-block; min-width: 34px; border-bottom: 1px solid #c7d2fe; font-weight: bold; }
  .back .mbox { border-color: #b45309; }
  .back .arr { color: #b45309; }
  .wmath { margin: 6px 0 0 30px; font-size: 15.5px; line-height: 2.0; }
  .wmath i { color: #6b7280; font-size: 12.5px; }
  .wtrap { margin-top: 10px; background: #fff7ed; border-left: 4px solid #b45309; padding: 6px 10px; font-size: 13.5px; }
  .drawbox { height: 90px; border: 1.5px dashed #c7d2fe; border-radius: 6px; margin: 4px 0 0 30px; }
  .bl { display: inline-block; min-width: 58px; border-bottom: 1.5px solid #1e3a8a; margin: 0 3px; }
  .grp { display: inline-block; border: 1.5px dashed #b45309; border-radius: 6px; padding: 1px 2px; margin: 0 2px; }
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


BL = '<span class="bl">&nbsp;</span>'


def _box(v):
    return '<span class="mbox">%s</span>' % v


def _arr(op):
    return '<span class="arr"><span class="op">%s</span><br>&#10230;</span>' % op


def _op(sym, n):
    return "%s%d" % (specs_focus.OPS[sym][3], n)


def _undo_op(sym, n):
    return "%s%d" % (specs_focus.UNDO_SYM[sym], n)


def _step(n, text):
    return '<div class="wstep"><span class="n">%d</span>%s</div>' % (n, text)


def _undo_walk(secret, ops, solved):
    """The 'undo the steps' method as five child-sized steps, picture AND math.
    solved=True fills every box (the worked example); False leaves blanks (guided #1)."""
    result = specs_focus.run_forward(secret, ops)
    mids, x = [], secret
    for sym, n in ops:
        x = specs_focus.OPS[sym][0](x, n)
        mids.append(x)
    trail = specs_focus.undo_trail(result, ops)
    v = (lambda val: str(val)) if solved else (lambda val: "&nbsp;")
    fwd = _box("?") + "".join(_arr(_op(sym, n)) + _box(result if i == len(ops) - 1 else v(mids[i]))
                              for i, (sym, n) in enumerate(ops))
    back = _box(result) + "".join(
        _arr(s if solved else "&nbsp;") + _box(v(b)) for (a, s, n, b) in
        [(a, "%s%d" % (s, n), n, b) for a, s, n, b in trail])
    out = [
        _step(1, "<b>Draw the number machine.</b> The secret number goes in. Each thing that "
                 "happens to it is an arrow."),
        '<div class="wpic">%s</div>' % fwd,
        _step(2, "<b>Turn around and walk back from the end.</b> Every arrow flips to its "
                 "opposite: <b>+ becomes &minus;</b>, <b>&minus; becomes +</b>, "
                 "<b>&times; becomes &divide;</b>, <b>&divide; becomes &times;</b>."),
        '<div class="wpic back">%s</div>' % back,
        _step(3, "<b>Write the math, ONE undo per line.</b> Copy the line, take off the LAST arrow."),
    ]
    lines = []
    for i, (line, why) in enumerate(undo_ladder(secret, ops)):
        if solved or i == 0:
            lines.append("%s &nbsp; <i>(%s)</i>" % (line, why))
        else:
            left = ops[:len(ops) - i]
            sym, n = ops[len(ops) - i]
            shown = (" &rarr; ".join(["?"] + [_op(s_, n_) for s_, n_ in left] + [BL])
                     if left else "? = " + BL)
            lines.append("%s &nbsp; <i>(undo %s: %s %s %d = %s)</i>"
                         % (shown, _op(sym, n), BL, specs_focus.UNDO_SYM[sym], n, BL))
    out.append('<div class="wmath">%s</div>' % "<br>".join(lines))
    chk = []
    x = secret
    for sym, n in ops:
        y = specs_focus.OPS[sym][0](x, n)
        chk.append("%s %s %d = %s" % (x if solved else BL, specs_focus.OPS[sym][3], n,
                                      y if solved else BL))
        x = y
    out += [_step(4, "<b>Check: put your answer in the machine, going forward.</b> Do you land "
                     "on %d?" % result),
            '<div class="wmath">%s %s</div>' % (", then ".join(chk), "&#10004;" if solved else "")]
    return "\n".join(out)


def _example_html(ex):
    secret, ops = ex["secret"], ex["ops"]
    result = specs_focus.run_forward(secret, ops)
    middle = specs_focus.undo_trail(result, ops)[0][3]
    return "\n".join([
        '  <div class="walk">',
        '    <h2>How to solve it: undo the steps</h2>',
        '    <div class="prompt"><i>%s thinks of a number. He multiplies it by 5, then adds 8. '
        'He gets %d. What was his number?</i></div>' % (ex["who"], result),
        _undo_walk(secret, ops, True),
        '    <div class="wtrap"><b>The trap:</b> after the first undo you have %d. That is the '
        '<b>middle</b> of the machine, not the start. Keep going until there are no arrows '
        'left. His number is %d.</div>' % (middle, secret),
        '  </div>', ''])


def _chip(text, fill):
    return ('<span style="display:inline-block;border:1.5px solid #1e3a8a;'
            'border-radius:4px;padding:0 6px;margin:0 1px;background:%s;'
            'font-size:12.5px">%s</span>' % (fill, text))


def _trade_walk(names, a, b, k, T, c, d, solved):
    a1, am, b1, bm = names
    n, m = a * k + b, c * k + d
    pb = T // n
    big = lambda: _chip(a1, "#fff")
    small = lambda: _chip(b1, "#fde68a")
    grp = lambda: '<span class="grp">%s</span>' % " ".join([small()] * k)
    v = (lambda val: str(val)) if solved else (lambda val: BL)
    pic = (lambda html: '<div class="wpic">%s</div>' % html) if solved else \
          (lambda html: '<div class="drawbox"></div>')
    out = [
        _step(1, "<b>Draw what you buy.</b>"),
        pic("%s &nbsp; %s &nbsp; = $%d" % (" ".join([big()] * a), " ".join([small()] * b), T)),
        _step(2, "<b>Trade every %s for %d %s.</b> Now there is only ONE kind of thing." % (a1, k, bm)),
        pic("%s &nbsp; %s &nbsp; = $%d" % (" ".join([grp()] * a), " ".join([small()] * b), T)),
        '<div class="wmath">%s %s + %s = $%d &nbsp; <i>(%d %s &times; %d = %s)</i></div>'
        % (v(a * k), bm, _plural(b, b1, bm), T, a, am if a != 1 else a1, k, v(a * k)),
        _step(3, "<b>Count them, then share the money.</b>"),
        '<div class="wmath">%s %s = $%d<br>1 %s = $%d &divide; %s = $%s</div>'
        % (v(n), bm, T, b1, T, v(n), v(pb)),
        _step(4, "<b>Answer the question the same way: trade, count, multiply.</b>"),
        '<div class="wmath">%s + %s<br>= %s %s + %s <i>(trade)</i><br>= %s %s<br>'
        '= %s &times; $%s = $%s</div>'
        % (_plural(c, a1, am), _plural(d, b1, bm), v(c * k), bm, _plural(d, b1, bm),
           v(m), bm, v(m), v(pb), v(m * pb)),
        _step(5, "<b>Check.</b> 1 %s = %d &times; $%s = $%s. Do the prices make $%d?"
              % (a1, k, v(pb), v(k * pb), T)),
        '<div class="wmath">%d &times; $%s + %d &times; $%s = $%d %s</div>'
        % (a, v(k * pb), b, v(pb), T, "&#10004;" if solved else ""),
    ]
    return "\n".join(out)


def _trade_example_html(ex):
    a, b, k, T, c, d = (ex[x] for x in "abkTcd")
    assert T % (a * k + b) == 0
    return "\n".join([
        '  <div class="walk">',
        '    <h2>How to solve it: trade it</h2>',
        '    <div class="prompt"><i>Sana buys %d jars of ink and %d quills for $%d. One jar costs '
        'the same as %d quills. How much do %d jars and %d quill cost?</i></div>' % (a, b, T, k, c, d),
        _trade_walk(("jar", "jars", "quill", "quills"), a, b, k, T, c, d, True),
        '    <div class="wtrap"><b>The trap:</b> do not split $%d over the %d things you see. '
        'A jar is not one quill. Trade first, then count.</div>' % (T, a + b),
        '  </div>', ''])


def _guided(i, p, kind):
    """Problem 1: the same steps as the worked example, with blanks to fill and space to draw."""
    if kind == "trade":
        walk = _trade_walk(p["names"], p["a_n"], p["b_n"], p["k"], p["T"], p["c_n"], p["d_n"], False)
    else:
        walk = _undo_walk(p["secret"], p["ops"], False)
    return "\n".join([
        '  <div class="problem guided">',
        '    <span class="qnum">%d.</span> <span class="tag">GUIDED &mdash; follow the steps</span>' % i,
        '    <div class="qtext">%s</div>' % p["q"],
        '    <div class="scaffold walk-g">%s</div>' % walk,
        '    <div class="answer">Answer:<span class="line"></span></div>',
        '    <div class="fact"><b>Did you know?</b> %s</div>' % p["fact"],
        '  </div>'])


def _problem(i, p, kind):
    """build_sheets._problem, with the work box swapped for a big OPEN space (no ruled lines:
    Asif 2026-10-25, lines make them write too small or too big). The step count is
    enforced in the key's rubric, not by the page."""
    if p.get("guided"):
        return _guided(i, p, kind)
    html = build_sheets._problem(i, p)
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
    title = spec["title"]
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
    """FOUR pages, one .sheet each (all carry the Name, so print-worksheet.sh --kid and its
    page-count check work): 1 = the worked example, drawn and in math, step by step;
    2 = guided #1, the same steps with blanks; 3 = #2-3; 4 = #4-5. Two problems per page
    so there is room to write every step (Asif, 2026-10-25)."""
    h = ['<!DOCTYPE html>', '<html lang="en">', "<head>", '<meta charset="UTF-8">',
         "<title>%s</title>" % spec["title_plain"], "<style>", build_sheets.CSS, LADDER_CSS,
         "</style>", "</head>", "<body>", ""]
    h += _sheet_head(spec, name, grade)
    h.append((_trade_example_html if spec.get("kind") == "trade" else _example_html)(
        spec["example"]))
    for i, p in enumerate(spec["problems"], 1):
        # page 1: the worked example; page 2: guided #1; then two problems per page
        if i in (1, 2, 4):
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
