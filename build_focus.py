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
  .eqrow { margin: 3px 0 0 30px; display: flex; align-items: baseline; }
  .eqrow .eq { display: inline-block; min-width: 300px; font-size: 19px; font-weight: 600; color: #14142b; }
  .eqrow i { color: #6b7280; font-size: 13px; }
  .letdef { margin: 4px 0 0 30px; font-size: 17px; font-weight: 600; color: #1e3a8a; }
  .space .letdef { margin-left: 4px; margin-top: 18px; }
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


_OP_WORDS = {"+": "adds %d", "-": "takes away %d", "*": "multiplies it by %d",
             "/": "divides it by %d"}


def _example_story(ex):
    result = specs_focus.run_forward(ex["secret"], ex["ops"])
    parts = [_OP_WORDS[s_] % n_ for s_, n_ in ex["ops"]]
    chain = ", ".join(parts[:-1]) + ", then " + parts[-1] if len(parts) > 1 else parts[0]
    return "%s thinks of a number. He %s. He gets %d. What was his number?" % (
        ex["who"], chain, result), result


def _example_html(ex):
    secret, ops = ex["secret"], ex["ops"]
    story, result = _example_story(ex)
    middle = specs_focus.undo_trail(result, ops)[0][3]
    return "\n".join([
        '  <div class="walk">',
        '    <h2>How to solve it: undo the steps</h2>',
        '    <div class="prompt"><i>%s</i></div>' % story,
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


# ---------------------------------------------------------------------------
# kind "eq" (kid2, Day 2+): letter equations with substitution, ONE step per line
# (Asif, 2026-10-25: his own worked photo). mask=None gives the full lines; a mask
# function turns every DERIVED number into a blank (guided problem), while the givens
# (counts, total, the trade) stay printed.
# ---------------------------------------------------------------------------
def _eq_args(src):
    """Normalise an eq worked example or problem dict into one tuple of raw numbers."""
    if "a" in src and "rel" in src and "pb" in src and "a_n" not in src:   # worked example
        a, b, r, pb, c, d = (src[x] for x in ("a", "b", "r", "pb", "c", "d"))
        rel, names = src["rel"], src["names"]
    else:
        a, b, r, pb, c, d = (src[x] for x in ("a_n", "b_n", "r", "pb", "c_n", "d_n"))
        rel, names = src["rel"], src["names"]
    pa = r * pb if rel == "k" else pb + r
    return names, rel, a, b, r, pa, pb, c, d, a * pa + b * pb


def eq_lines(src, mask=None):
    """[(step, equation, note)] for the whole problem, then the check as (5, eq, note)."""
    names, rel, a, b, r, pa, pb, c, d, T = _eq_args(src)
    a1, am, b1, bm = names
    la, lb = a1[0], b1[0]
    N = mask or (lambda x: x)
    n, m = a + b, c + d
    L = []
    if rel == "k":
        ak, ck = a * r, c * r
        nn, mm = ak + b, ck + d
        L = [(1, "%d%s + %d%s = %d" % (a, la, b, lb, T), "the story"),
             (1, "1%s = %d%s" % (la, r, lb), "the trade: 1 %s costs the same as %d %s" % (a1, r, bm)),
             (2, "%s%s + %d%s = %d" % (N(ak), lb, b, lb, T),
              "substitute: %d%s = %d &times; %d%s = %s%s" % (a, la, a, r, lb, N(ak), lb)),
             (2, "%s%s = %d" % (N(nn), lb, T), "%s + %d = %s" % (N(ak), b, N(nn))),
             (3, "%s = %s" % (lb, N(pb)), "%d &divide; %s = %s" % (T, N(nn), N(pb))),
             (3, "%s = %s" % (la, N(pa)), "%d &times; %s = %s" % (r, N(pb), N(pa))),
             (4, "%d%s + %d%s" % (c, la, d, lb), "the question"),
             (4, "= %s%s + %d%s" % (N(ck), lb, d, lb),
              "substitute: %d%s = %d &times; %d%s = %s%s" % (c, la, c, r, lb, N(ck), lb)),
             (4, "= %s%s" % (N(mm), lb), "%s + %d = %s" % (N(ck), d, N(mm))),
             (4, "= %s &times; %s = $%s" % (N(mm), N(pb), N(mm * pb)),
              "put in %s = %s" % (lb, N(pb)))]
    else:
        e = r
        ae, ce = a * e, c * e
        L = [(1, "%d%s + %d%s = %d" % (a, la, b, lb, T), "the story"),
             (1, "1%s = 1%s + %d" % (la, lb, e), "the trade: 1 %s costs $%d more than 1 %s" % (a1, e, b1)),
             (2, "%d(1%s + %d) + %d%s = %d" % (a, lb, e, b, lb, T),
              "substitute: %s is 1%s + %d" % (la, lb, e)),
             (2, "%d%s + %s + %d%s = %d" % (a, lb, N(ae), b, lb, T),
              "%d &times; %d = %s" % (a, e, N(ae))),
             (2, "%s%s + %s = %d" % (N(n), lb, N(ae), T), "%d + %d = %s" % (a, b, N(n))),
             (2, "%s%s = %s" % (N(n), lb, N(T - ae)), "%d &minus; %s = %s" % (T, N(ae), N(T - ae))),
             (3, "%s = %s" % (lb, N(pb)), "%s &divide; %s = %s" % (N(T - ae), N(n), N(pb))),
             (3, "%s = %s" % (la, N(pa)), "%s + %d = %s" % (N(pb), e, N(pa))),
             (4, "%d%s + %d%s" % (c, la, d, lb), "the question"),
             (4, "= %d(1%s + %d) + %d%s" % (c, lb, e, d, lb), "substitute: %s is 1%s + %d" % (la, lb, e)),
             (4, "= %d%s + %s + %d%s" % (c, lb, N(ce), d, lb), "%d &times; %d = %s" % (c, e, N(ce))),
             (4, "= %s%s + %s" % (N(m), lb, N(ce)), "%d + %d = %s" % (c, d, N(m))),
             (4, "= %s &times; %s + %s" % (N(m), N(pb), N(ce)), "put in %s = %s" % (lb, N(pb))),
             (4, "= $%s" % N(m * pb + ce), "%s + %s = %s" % (N(m * pb), N(ce), N(m * pb + ce)))]
    L.append((5, "%d &times; %s + %d &times; %s = %d" % (a, N(pa), b, N(pb), T), "does it make $%d?" % T))
    return L


EQ_STEPS = {1: "<b>Write what you know as equations.</b> One letter for each price.",
            2: "<b>Substitute</b> for the letter that has a trade. Then combine, until ONE letter is left.",
            3: "<b>Solve</b> for the one price, then the other.",
            4: "<b>Answer the question the same way:</b> write it, substitute, combine, put in the price.",
            5: "<b>Check.</b> Put both prices back in the first equation."}


def _eq_row(eq, note, tick=""):
    return '<div class="eqrow"><span class="eq">%s %s</span><i>(%s)</i></div>' % (eq, tick, note)


def _letdef(names):
    a1, am, b1, bm = names
    return "Let %s = the price of 1 %s. &nbsp; Let %s = the price of 1 %s." % (a1[0], a1, b1[0], b1)


def _eq_walk(src, solved):
    names = _eq_args(src)[0]
    lines = eq_lines(src, None if solved else (lambda x: BL))
    out, last = [], 0
    for step, eq, note in lines:
        if step != last:
            out.append(_step(step, EQ_STEPS[step]))
            if step == 1:
                out.append('<div class="letdef">%s</div>' % _letdef(names))
            last = step
        out.append(_eq_row(eq, note, "&#10004;" if (solved and step == 5) else ""))
    return "\n".join(out)


def _eq_example_html(ex):
    names, rel, a, b, r, pa, pb, c, d, T = _eq_args(ex)
    assert rel == "k"
    a1, am, b1, bm = names
    pic = ("%s &nbsp; %s &nbsp; = $%d &nbsp;&nbsp; <i style=\"font-size:12px;color:#6b7280\">"
           "(a picture, just to help)</i>" % (
               " ".join([_chip(a1, "#fff")] * a), " ".join([_chip(b1, "#fde68a")] * b), T))
    body = _eq_walk(ex, True)
    marker = _step(2, EQ_STEPS[2])
    body = body.replace(marker, '<div class="wpic">%s</div>\n%s' % (pic, marker), 1)
    return "\n".join([
        '  <div class="walk">',
        '    <h2>How to solve it: letters and substitution</h2>',
        '    <div class="prompt"><i>Sana buys %d %s and %d %s for $%d. One %s costs the same as %d '
        '%s. How much do %d %s and %d %s cost?</i></div>' % (
            a, am, b, bm, T, a1, r, bm, c, am, d, b1 if d == 1 else bm),
        body,
        '    <div class="wtrap"><b>The trap:</b> do not split $%d over the %d things you see. '
        'A %s is not one %s. Substitute first, then solve. Keep every step on its own line.</div>'
        % (T, a + b, a1, b1),
        '  </div>', ''])


def _guided(i, p, kind):
    """Problem 1: the same steps as the worked example, with blanks to fill and space to draw."""
    if kind == "eq":
        walk = _eq_walk(p, False)
    elif kind == "trade":
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
    extra = ""
    if kind == "eq":
        label = "Letters first. Substitute. ONE step per line. Check at the end."
        extra = '<div class="letdef">%s</div>' % _letdef(p["names"])
    old = '<div class="work"><span class="work-label">SHOW YOUR THINKING</span></div>'
    assert old in html
    return html.replace(old, '<div class="space"><span class="work-label">%s</span>%s</div>'
                        % (label, extra))


def _key_steps(p, kind):
    if kind == "eq":
        lines = eq_lines(p)
        return "<b>%s</b><br>%s" % (_letdef(p["names"]), " &nbsp;|&nbsp; ".join(
            ("<b>%s</b>" % eq) if st != 5 else eq for st, eq, _ in lines))
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
    h.append({"trade": _trade_example_html, "eq": _eq_example_html}.get(
        spec.get("kind"), _example_html)(spec["example"]))
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
        n = (8 if spec.get("kind") == "trade" else
             len(eq_lines(p)) if spec.get("kind") == "eq" else len(p["ops"]) + 1)
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
