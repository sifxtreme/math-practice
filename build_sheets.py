"""Shared builder for the daily sheets.

Why this exists: ten hand-copied HTML files drift. print-worksheet.sh rewrites
EXACT literal CSS strings ('height: 78px;', 'padding: 9px 12px;', ...) to tighten
a sheet onto 3 pages, and a single retyped value silently breaks that for one
file. The CSS below is copied once from worksheet-bridges-logic.html and every
generated sheet shares it byte-for-byte.

Answers are COMPUTED here and interpolated into the key, so the key cannot
disagree with the arithmetic. See verify_sheets.py for the assertions.
"""

CSS = """  @page { margin: 0.55in; }
  * { box-sizing: border-box; }
  body {
    font-family: "Georgia", "Times New Roman", serif;
    color: #14142b;
    margin: 0;
    line-height: 1.4;
  }
  .sheet { page-break-after: always; padding: 6px 4px; }
  .sheet:last-child { page-break-after: auto; }
  .header {
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 3px solid #1e3a8a; padding-bottom: 8px; margin-bottom: 6px;
  }
  .header h1 { font-size: 22px; margin: 0; color: #1e3a8a; }
  .header .sub { font-size: 12px; color: #7d8bb0; font-style: italic; }
  .grade {
    font-size: 13px; font-weight: bold; background: #1e3a8a;
    color: #fff; padding: 3px 10px; border-radius: 4px;
  }
  .meta { display: flex; gap: 30px; font-size: 13px; margin-bottom: 12px; color: #444; }
  .meta span { border-bottom: 1px solid #999; min-width: 140px; display: inline-block; }

  /* TEACH box — padding/margin MUST stay these literals so print-worksheet.sh
     shrinks them along with everything else. Don't "tidy" them. */
  .teach {
    border: 2px solid #1e3a8a; border-radius: 6px;
    padding: 9px 12px; margin-bottom: 4px;
    background: #eef2ff; page-break-inside: avoid;
  }
  .teach .teach-title {
    font-size: 12px; font-weight: bold; letter-spacing: 1px;
    color: #fff; background: #1e3a8a;
    display: inline-block; padding: 2px 9px; border-radius: 3px; margin-bottom: 5px;
  }
  .teach .prompt { font-size: 13.5px; font-style: italic; margin-bottom: 5px; }
  .teach .step {
    font-size: 13.5px; margin: 3px 0 3px 4px;
    padding-left: 8px; border-left: 3px solid #c7d2fe;
  }
  .teach .step b { color: #1e3a8a; }
  .teach .punch {
    margin-top: 6px; font-size: 13px;
    background: #eef2ff; border-radius: 4px; padding: 5px 9px;
  }
  .teach .punch b { color: #1e3a8a; }

  .problem {
    margin-bottom: 4px;
    padding: 9px 12px;
    border: 1.5px solid #c7d2fe;
    border-radius: 6px;
    page-break-inside: avoid;
  }
  .problem.guided { border-color: #1e3a8a; border-style: dashed; }
  .qnum { font-weight: bold; font-size: 15px; color: #1e3a8a; }
  .tag {
    font-size: 9.5px; font-weight: bold; letter-spacing: 0.5px;
    background: #1e3a8a; color: #fff; padding: 1px 6px;
    border-radius: 3px; margin-left: 5px; vertical-align: 2px;
  }
  .qtext { font-size: 14.5px; margin: 4px 0 7px 0; }
  .work { height: 78px; border-top: 1px dashed #bbb; position: relative; }
  .work-label {
    position: absolute; top: 3px; left: 0;
    font-size: 10px; color: #999; font-style: italic; letter-spacing: 0.5px;
  }
  /* Guided steps sit in normal flow and ARE the work area — a .work box shrinks
     to 40px on print, which an absolute scaffold would overflow onto the answer line. */
  .scaffold { font-size: 12.5px; color: #7d8bb0; border-top: 1px dashed #bbb; padding-top: 4px; }
  .scaffold div { margin-bottom: 3px; }
  .scaffold .blank {
    display: inline-block; border-bottom: 1px solid #c7d2fe;
    width: 90px; margin: 0 3px;
  }
  .answer { margin-top: 5px; font-size: 13px; }
  .answer .line {
    display: inline-block; border-bottom: 2px solid #14142b;
    width: 150px; margin-left: 6px;
  }
  .fact {
    margin-top: 7px;
    font-size: 11.5px; color: #444;
    background: #eef2ff;
    border-left: 3px solid #4f46e5;
    padding: 4px 8px;
    border-radius: 0 4px 4px 0;
  }
  .fact b { color: #1e3a8a; }

  .key h1 { color: #1e3a8a; }
  .key .ans {
    margin-bottom: 11px; padding: 8px 12px;
    border: 1px solid #d5dcf7; border-radius: 5px;
    page-break-inside: avoid; font-size: 13.5px;
  }
  .key .ans b { color: #1e3a8a; }
  .key .ans .steps { color: #555; font-size: 12.5px; margin-top: 2px; }
  .key .section-title {
    font-size: 15px; font-weight: bold; color: #fff;
    background: #1e3a8a; padding: 4px 10px; border-radius: 4px;
    margin: 14px 0 8px 0;
  }
  .key .watch {
    font-size: 12.5px; background: #fef3c7; border-left: 3px solid #d97706;
    padding: 5px 9px; border-radius: 0 4px 4px 0; margin: 8px 0 4px 0;
  }
  .key .watch b { color: #92400e; }"""

# (id, display name, grade label). The id is the spec dict key; the NAME comes from
# the gitignored kids.local.json and reaches paper only in the Name: field.
# See README.md "Setting it up for your kids".
from kids_config import load_kids, grade_label

KIDS = [(k["id"], k["name"], grade_label(k)) for k in load_kids()]


def _problem(i, p):
    """One numbered problem. A 'guided' problem gets a scaffold instead of a work box."""
    cls = "problem guided" if p.get("guided") else "problem"
    tag = ' <span class="tag">GUIDED</span>' if p.get("guided") else ""
    out = ['  <div class="%s">' % cls,
           '    <span class="qnum">%d.</span>%s' % (i, tag),
           '    <div class="qtext">%s</div>' % p["q"]]
    if p.get("guided"):
        out.append('    <div class="scaffold">')
        for line in p["guided"]:
            out.append("      <div>%s</div>" % line)
        out.append("    </div>")
    else:
        out.append('    <div class="work"><span class="work-label">SHOW YOUR THINKING</span></div>')
    out.append('    <div class="answer">Answer:<span class="line"></span></div>')
    out.append('    <div class="fact"><b>Did you know?</b> %s</div>' % p["fact"])
    out.append("  </div>")
    return "\n".join(out)


def build(spec):
    h = ['<!DOCTYPE html>', '<html lang="en">', "<head>", '<meta charset="UTF-8">',
         "<title>%s</title>" % spec["title_plain"], "<style>", CSS, "</style>", "</head>",
         "<body>", ""]

    for kid_id, kid, grade in KIDS:
        probs = spec[kid_id]
        h += ["<!-- ==== %s ==== -->" % kid.upper(),
              '<div class="sheet">',
              '  <div class="header">', "    <div>",
              "      <h1>%s</h1>" % spec["title"],
              '      <div class="sub">%s</div>' % spec["sub"],
              "    </div>",
              '    <div class="grade">%s</div>' % grade,
              "  </div>",
              '  <div class="meta">',
              "    <div>Name: <span>&nbsp;%s</span></div>" % kid,
              "    <div>Date: <span>&nbsp;</span></div>",
              "  </div>", ""]
        for i, p in enumerate(probs, 1):
            h.append(_problem(i, p))
            h.append("")
        h += ["</div>", ""]

    h += ["<!-- ==== ANSWER KEY ==== -->", '<div class="sheet key">',
          '  <div class="header">', "    <div>", "      <h1>🔑 Answer Key</h1>",
          '      <div class="sub">For the grown-ups — worked steps included</div>',
          "    </div>", '    <div class="grade">Coach</div>', "  </div>", ""]
    for kid_id, kid, grade in KIDS:
        h.append('  <div class="section-title">%s — %s</div>' % (grade, kid))
        for i, p in enumerate(spec[kid_id], 1):
            h += ['  <div class="ans"><b>%d. %s</b>' % (i, p["a"]),
                  '    <div class="steps">%s</div>' % p["steps"], "  </div>"]
        w = spec.get(kid_id + "_watch")
        if w:
            h.append('  <div class="watch"><b>Watch for:</b> %s</div>' % w)
        h.append("")
    h += ["</div>", "", "</body>", "</html>", ""]
    return "\n".join(h)


def write(spec, outdir="."):
    import os
    path = os.path.join(outdir, spec["file"])
    with open(path, "w") as f:
        f.write(build(spec))
    return path
