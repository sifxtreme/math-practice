#!/usr/bin/env python3
"""make-sheet.py — build a 3-page worksheet HTML from a spec dict.

Why this exists: every sheet is the same layout with different problems. Hand-
copying the HTML per sheet is how CSS drifts, and the print pipeline is picky —
print-worksheet.sh tightens the page by rewriting EXACT literal CSS strings
(`height: 78px;`, `padding: 9px 12px;`, `margin-bottom: 4px;`, `line-height: 1.4;`,
`margin: 4px 0 7px 0;`, `margin-top: 7px;`, `padding: 4px 8px;`). If a sheet's CSS
drifts from those, the sheet silently overflows to 5 pages. This emits them
verbatim, every time.

Usage:
    from make_sheet import build
    open('out.html','w').write(build(spec))

Spec shape — see build-block1.py for worked examples.
    title, sub, color{main,muted,border,factbg,factbar,keyborder}
    pages[]: {name, grade, work_label, teach{prompt,steps[],punch}, problems[]}
      problems[]: {text, fact, scaffold[]}   # scaffold => GUIDED, replaces .work
    key[]: {section, watch, answers[{a, steps}]}

Rules enforced elsewhere (AGENTS.md): 5 problems on a PRACTICE page, 4 on a
TEACH page (the worked-example box costs one problem's worth of height).
"""
import html as _html


def _problem(p, i, work_label):
    guided = bool(p.get('scaffold'))
    cls = 'problem guided' if guided else 'problem'
    tag = '<span class="tag">GUIDED</span>' if guided else ''
    out = [f'  <div class="{cls}">']
    out.append(f'    <span class="qnum">{i}.</span>{tag}')
    out.append(f'    <div class="qtext">{p["text"]}</div>')
    if guided:
        out.append('    <div class="scaffold">')
        for line in p['scaffold']:
            out.append(f'      <div>{line}</div>')
        out.append('    </div>')
    else:
        out.append(f'    <div class="work"><span class="work-label">{work_label}</span></div>')
    out.append('    <div class="answer">Answer:<span class="line"></span></div>')
    if p.get('fact'):
        out.append(f'    <div class="fact"><b>Did you know?</b> {p["fact"]}</div>')
    out.append('  </div>')
    return '\n'.join(out)


def _teach(t):
    out = ['  <div class="teach">', '    <div class="teach-title">HOW IT WORKS</div>',
           f'    <div class="prompt">{t["prompt"]}</div>']
    for s in t['steps']:
        out.append(f'    <div class="step">{s}</div>')
    out.append(f'    <div class="punch"><b>The trap:</b> {t["punch"]}</div>')
    out.append('  </div>')
    return '\n'.join(out)


def build(spec):
    c = spec['color']
    css = f"""  @page {{ margin: 0.55in; }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: "Georgia", "Times New Roman", serif;
    color: #14142b;
    margin: 0;
    line-height: 1.4;
  }}
  .sheet {{ page-break-after: always; padding: 6px 4px; }}
  .sheet:last-child {{ page-break-after: auto; }}
  .header {{
    display: flex; justify-content: space-between; align-items: flex-end;
    border-bottom: 3px solid {c['main']}; padding-bottom: 8px; margin-bottom: 6px;
  }}
  .header h1 {{ font-size: 22px; margin: 0; color: {c['main']}; }}
  .header .sub {{ font-size: 12px; color: {c['muted']}; font-style: italic; }}
  .grade {{
    font-size: 13px; font-weight: bold; background: {c['main']};
    color: #fff; padding: 3px 10px; border-radius: 4px;
  }}
  .meta {{ display: flex; gap: 30px; font-size: 13px; margin-bottom: 12px; color: #444; }}
  .meta span {{ border-bottom: 1px solid #999; min-width: 140px; display: inline-block; }}

  /* TEACH box — padding/margin MUST stay these literals so print-worksheet.sh
     shrinks them along with everything else. Don't "tidy" them. */
  .teach {{
    border: 2px solid {c['main']}; border-radius: 6px;
    padding: 9px 12px; margin-bottom: 4px;
    background: {c['factbg']}; page-break-inside: avoid;
  }}
  .teach .teach-title {{
    font-size: 12px; font-weight: bold; letter-spacing: 1px;
    color: #fff; background: {c['main']};
    display: inline-block; padding: 2px 9px; border-radius: 3px; margin-bottom: 5px;
  }}
  .teach .prompt {{ font-size: 13.5px; font-style: italic; margin-bottom: 5px; }}
  .teach .step {{
    font-size: 13.5px; margin: 3px 0 3px 4px;
    padding-left: 8px; border-left: 3px solid {c['border']};
  }}
  .teach .step b {{ color: {c['main']}; }}
  .teach .punch {{
    margin-top: 6px; font-size: 13px;
    background: {c['factbg']}; border-radius: 4px; padding: 5px 9px;
  }}
  .teach .punch b {{ color: {c['main']}; }}

  .problem {{
    margin-bottom: 4px;
    padding: 9px 12px;
    border: 1.5px solid {c['border']};
    border-radius: 6px;
    page-break-inside: avoid;
  }}
  .problem.guided {{ border-color: {c['main']}; border-style: dashed; }}
  .qnum {{ font-weight: bold; font-size: 15px; color: {c['main']}; }}
  .tag {{
    font-size: 9.5px; font-weight: bold; letter-spacing: 0.5px;
    background: {c['main']}; color: #fff; padding: 1px 6px;
    border-radius: 3px; margin-left: 5px; vertical-align: 2px;
  }}
  .qtext {{ font-size: 14.5px; margin: 4px 0 7px 0; }}
  .work {{ height: 78px; border-top: 1px dashed #bbb; position: relative; }}
  .work-label {{
    position: absolute; top: 3px; left: 0;
    font-size: 10px; color: #999; font-style: italic; letter-spacing: 0.5px;
  }}
  /* Guided steps sit in normal flow and ARE the work area — a .work box shrinks
     to 40px on print, which an absolute scaffold would overflow onto the answer line. */
  .scaffold {{ font-size: 12.5px; color: {c['muted']}; border-top: 1px dashed #bbb; padding-top: 4px; }}
  .scaffold div {{ margin-bottom: 3px; }}
  .scaffold .blank {{
    display: inline-block; border-bottom: 1px solid {c['border']};
    width: 90px; margin: 0 3px;
  }}
  .answer {{ margin-top: 5px; font-size: 13px; }}
  .answer .line {{
    display: inline-block; border-bottom: 2px solid #14142b;
    width: 150px; margin-left: 6px;
  }}
  .fact {{
    margin-top: 7px;
    font-size: 11.5px; color: #444;
    background: {c['factbg']};
    border-left: 3px solid {c['factbar']};
    padding: 4px 8px;
    border-radius: 0 4px 4px 0;
  }}
  .fact b {{ color: {c['main']}; }}

  .key h1 {{ color: {c['main']}; }}
  .key .ans {{
    margin-bottom: 11px; padding: 8px 12px;
    border: 1px solid {c['keyborder']}; border-radius: 5px;
    page-break-inside: avoid; font-size: 13.5px;
  }}
  .key .ans b {{ color: {c['main']}; }}
  .key .ans .steps {{ color: #555; font-size: 12.5px; margin-top: 2px; }}
  .key .section-title {{
    font-size: 15px; font-weight: bold; color: #fff;
    background: {c['main']}; padding: 4px 10px; border-radius: 4px;
    margin: 14px 0 8px 0;
  }}
  .key .watch {{
    font-size: 12.5px; background: #fef3c7; border-left: 3px solid #d97706;
    padding: 5px 9px; border-radius: 0 4px 4px 0; margin: 8px 0 4px 0;
  }}
  .key .watch b {{ color: #92400e; }}"""

    body = []
    for page in spec['pages']:
        wl = page.get('work_label', 'SHOW YOUR WORK')
        body.append(f'<!-- ==== {page["name"].upper()} ==== -->')
        body.append('<div class="sheet">')
        body.append('  <div class="header">')
        body.append(f'    <div>\n      <h1>{spec["title"]}</h1>\n'
                    f'      <div class="sub">{spec["sub"]}</div>\n    </div>')
        body.append(f'    <div class="grade">{page["grade"]}</div>')
        body.append('  </div>')
        body.append(f'  <div class="meta">\n    <div>Name: <span>&nbsp;{page["name"]}</span></div>'
                    f'\n    <div>Date: <span></span></div>\n  </div>\n')
        if page.get('teach'):
            body.append(_teach(page['teach']) + '\n')
        for i, p in enumerate(page['problems'], 1):
            body.append(_problem(p, i, wl) + '\n')
        body.append('</div>\n')

    body.append('<!-- ==== ANSWER KEY ==== -->')
    body.append('<div class="sheet key">')
    body.append('  <div class="header">\n    <div>\n      <h1>🔑 Answer Key</h1>')
    body.append(f'      <div class="sub">{spec.get("key_sub", "For the grown-ups — worked steps included")}</div>')
    body.append('    </div>\n    <div class="grade">Coach</div>\n  </div>\n')
    for sec in spec['key']:
        body.append(f'  <div class="section-title">{sec["section"]}</div>\n')
        if sec.get('watch'):
            body.append(f'  <div class="watch"><b>Watch for:</b> {sec["watch"]}</div>\n')
        for i, a in enumerate(sec['answers'], 1):
            body.append(f'  <div class="ans"><b>{i}. {a["a"]}</b>\n'
                        f'    <div class="steps">{a["steps"]}</div>\n  </div>')
        body.append('')
    body.append('</div>')

    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            f'<title>{_html.escape(spec["doc_title"])}</title>\n<style>\n{css}\n</style>\n'
            f'</head>\n<body>\n\n' + '\n'.join(body) + '\n\n</body>\n</html>\n')
