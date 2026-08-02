"""build_site.py — build the PUBLIC static site for math.sifxtreme.com.

    python3 build_site.py && python3 verify_public.py    # gate MUST pass
    # then deploy site/ to Cloudflare Pages

WHAT MAKES THIS "PUBLIC"
------------------------
The repo is a family's practice material. The SITE is a tool other parents can use.
Those are different artifacts and this script is the boundary between them:

  * every `Name:` field is BLANK — a printable worksheet should have a blank name
    line anyway, so this costs nothing and removes the only per-child field
  * the answer key's "Watch for:" boxes are DROPPED — they are observations about a
    specific child ("if he now answers 10 trays without being asked twice...")
  * nothing from `private/` is read, ever
  * `PRACTICE-PLAN-2026.md` and the docs are not published — they carry grades, a
    school name, and a term calendar

Nothing here is trusted on faith. `verify_public.py` re-reads everything this
writes and fails the build if a single forbidden string survives. Run it. The whole
point of a public/private split is that it is CHECKED, not intended.
"""

import html as _html
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")

# Worksheets worth publishing, with a human label. Deliberately an ALLOW-LIST: a new
# sheet is private until someone adds it here, which is the safe default.
SHEETS = [
    ("worksheet.html", "Space", "word problems"),
    ("worksheet-ocean.html", "Ocean & Reef", "word problems"),
    ("worksheet-dinosaur.html", "Fossil Dig", "word problems"),
    ("worksheet-volcano.html", "Volcanoes", "word problems"),
    ("worksheet-silkroad.html", "The Silk Road", "word problems"),
    ("worksheet-national-parks.html", "National Parks", "word problems"),
    ("worksheet-human-body-mixed.html", "The Human Body", "word problems"),
    ("worksheet-trains-teach2.html", "Trains", "word problems · teaching sheet"),
    ("worksheet-weather.html", "Weather", "word problems · teaching sheet"),
    ("worksheet-mars-rovers.html", "Mars Rovers", "word problems"),
    ("worksheet-honeybees.html", "Honeybees", "word problems"),
    ("worksheet-sailing-ships.html", "Sailing Ships", "word problems · timed"),
    ("worksheet-mountains-cumulative.html", "Mountains & Climbing", "word problems · review"),
    ("worksheet-teach-remainders-fractions.html", "Remainders & Fractions", "word problems · teaching sheet"),
    ("worksheet-egypt-logic.html", "Ancient Egypt", "logic puzzles"),
    ("worksheet-astronomy-logic.html", "Astronomy", "logic puzzles"),
    ("worksheet-bridges-logic.html", "Bridges", "logic puzzles"),
    ("worksheet-lighthouse-logic.html", "Lighthouses", "logic puzzles"),
    ("worksheet-falconry-logic.html", "Falconry", "logic puzzles"),
    ("worksheet-caravan-logic.html", "Deserts & Caravans", "logic puzzles"),
    ("worksheet-clocks-logic.html", "Clocks & Timekeeping", "logic puzzles"),
    ("worksheet-kites-logic-cumulative.html", "Kites & Flight", "logic puzzles · review"),
]

DRILL_SEEDS = [101, 202, 303, 404, 505]


def child_names():
    """Names to strip from structural markup. Read locally; never shipped."""
    import json
    p = os.path.join(HERE, "kids.local.json")
    if not os.path.exists(p):
        return []
    with open(p) as f:
        return [k["name"] for k in json.load(f)["kids"] if k.get("name")]


def scrub(doc, names=()):
    """Remove every place a sheet identifies WHOSE it is.

    Four structural carriers, each found the hard way when `verify_public.py`
    rejected the first build:

      1. the `Name:` header field
      2. `<div class="watch">` boxes — per-child observations for the adult
      3. answer-key section titles, which appear as BOTH "kid1 — 3rd Grade" and
         "3rd Grade — kid1" depending on the sheet's vintage
      4. HTML comments — invisible on screen, fully present in View Source

    Story characters inside problem text are deliberately left alone. A child in a
    falconry puzzle named kid2 is a name in a word problem, not a statement about
    anyone; stripping them would break the puzzles, whose answers reference them.
    """
    doc = re.sub(r'(Name:\s*<span>)(?:&nbsp;|\s)*[^<]*(</span>)', r'\1&nbsp;\2', doc)
    doc = re.sub(r'<div class="watch">.*?</div>', "", doc, flags=re.S)
    doc = re.sub(r'<!--.*?-->', "", doc, flags=re.S)          # View Source is public too
    for n in names:                                            # both title orders
        doc = re.sub(r'(<div class="section-title">)[^<]*?</div>',
                     lambda m, nm=n: re.sub(r'\s*[—-]\s*' + re.escape(nm) + r'|'
                                            + re.escape(nm) + r'\s*[—-]\s*|'
                                            + re.escape(nm),
                                            "", m.group(0)), doc)
    doc = re.sub(r'<div class="section-title">\s*</div>', "", doc)
    return doc



# --------------------------------------------------------------------------
# persistent nav
# --------------------------------------------------------------------------
# Injected into EVERY page. Two constraints drive the design:
#
#   1. **It must not print.** These pages exist to be printed; a nav bar across the
#      top of a worksheet ruins the sheet. Hence @media print { display: none }.
#   2. **It must not collide.** Every worksheet ships its own CSS with generic
#      selectors, so every class here is msnav-prefixed and every property it needs
#      is stated rather than inherited.
#
# Links are root-absolute because pages sit at three different depths.

NAV_CSS = """
<style>
.msnav{position:sticky;top:0;z-index:9999;display:flex;flex-wrap:wrap;align-items:center;
 gap:2px 4px;padding:8px 14px;background:#12131a;border-bottom:1px solid #2a2d38;
 font:14px/1.4 -apple-system,BlinkMacSystemFont,'Segoe UI',Inter,system-ui,sans-serif;}
.msnav a{color:#c9cde0;text-decoration:none;padding:5px 9px;border-radius:6px;
 white-space:nowrap;font-weight:500;}
.msnav a:hover{background:#232634;color:#fff;}
.msnav .msnav-home{font-weight:700;color:#fff;margin-right:6px;}
.msnav .msnav-sp{flex:1 1 auto;}
.msnav .msnav-out{color:#8fb8ff;}
@media print{.msnav{display:none !important;}}
</style>
"""

NAV_HTML = """
<nav class="msnav">
  <a class="msnav-home" href="/">Math worksheets</a>
  <a href="/#drills">Drills</a>
  <a href="/#word">Word problems</a>
  <a href="/#logic">Logic</a>
  <a href="/animations/">Animations</a>
  <span class="msnav-sp"></span>
  <a class="msnav-out" href="https://sifxtreme.com">&larr; sifxtreme.com</a>
</nav>
"""


def with_nav(doc):
    """Put the nav at the top of any of the three document shapes we emit.

    Worksheets are full documents with <body>; the animations page has no <body>
    tag at all (head + content, browser implies it). Handle both, and fall back to
    prepending rather than silently returning the page un-navigated.
    """
    block = NAV_CSS + NAV_HTML
    m = re.search(r'<body[^>]*>', doc)
    if m:
        return doc[:m.end()] + block + doc[m.end():]
    if "</head>" in doc:
        return doc.replace("</head>", "</head>" + block, 1)
    return block + doc

PAGE_CSS = """
:root { --ink:#12131a; --dim:#5a6070; --line:#e3e6ee; --bg:#fbfbfd; --accent:#8a1538; }
@media (prefers-color-scheme: dark) {
  :root { --ink:#e9eaf0; --dim:#9aa1b4; --line:#272a35; --bg:#101219; --accent:#f2789f; }
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,system-ui,sans-serif; }
.wrap { max-width:920px; margin:0 auto; padding:48px 22px 80px; }
h1 { font-size:clamp(28px,5vw,40px); line-height:1.15; margin:0 0 10px; letter-spacing:-.02em; }
h2 { font-size:20px; margin:44px 0 12px; letter-spacing:-.01em; }
.lede { color:var(--dim); font-size:18px; margin:0 0 8px; max-width:62ch; }
a { color:inherit; }
.grid { display:grid; gap:10px; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); margin:0; padding:0; list-style:none; }
.card { display:block; border:1px solid var(--line); border-radius:10px; padding:13px 15px;
  text-decoration:none; background:transparent; transition:border-color .15s, transform .15s; }
.card:hover { border-color:var(--accent); transform:translateY(-1px); }
.card b { display:block; font-weight:600; margin-bottom:2px; }
.card span { color:var(--dim); font-size:13px; }
table { border-collapse:collapse; width:100%; font-size:14.5px; margin:8px 0; }
th,td { text-align:left; padding:8px 10px; border-bottom:1px solid var(--line); }
th { color:var(--dim); font-weight:600; font-size:13px; }
code { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.9em;
  background:color-mix(in srgb, var(--line) 55%, transparent); padding:1px 5px; border-radius:4px; }
.card.hero { border-color:var(--accent); border-width:2px; padding:18px 20px; }
.card.hero b { font-size:18px; }
.note { border-left:3px solid var(--accent); padding:2px 0 2px 14px; color:var(--dim); margin:18px 0; }
footer { margin-top:56px; padding-top:18px; border-top:1px solid var(--line); color:var(--dim); font-size:13.5px; }
.scroll { overflow-x:auto; }
"""


def shell(title, body, depth=0):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_html.escape(title)}</title>
<style>{PAGE_CSS}</style></head>
<body>{NAV_CSS}{NAV_HTML}<div class="wrap">{body}
<footer>Free to print and use. Built by <a href="https://sifxtreme.com">Asif Ahmed</a>.
<a href="{up}index.html">All sheets</a></footer>
</div></body></html>
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "sheets"))
    os.makedirs(os.path.join(OUT, "drills"))

    # --- worksheets, scrubbed
    names = child_names()
    published = []
    for fname, label, kind in SHEETS:
        src = os.path.join(HERE, fname)
        if not os.path.exists(src):
            print(f"  skip (missing): {fname}", file=sys.stderr)
            continue
        with open(src) as f:
            doc = scrub(f.read(), names)
        with open(os.path.join(OUT, "sheets", fname), "w") as f:
            f.write(with_nav(doc))
        published.append((fname, label, kind))

    # --- drills, generated fresh at several seeds with NO kids config in play
    env = dict(os.environ, MATH_PUBLIC_BUILD="1")
    drills = []
    for skill, nice in (("div", "Long division"), ("mul", "Multiplication")):
        for seed in DRILL_SEEDS:
            out = os.path.join(OUT, "drills", f"{skill}-{seed}.html")
            subprocess.run(
                [sys.executable, os.path.join(HERE, "drill_gen.py"),
                 "--skill", skill, "--seed", str(seed), "--out", out],
                check=True, cwd=HERE, env=env,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(out) as f:
                doc = scrub(f.read(), names)
            with open(out, "w") as f:
                f.write(with_nav(doc))
            drills.append((f"{skill}-{seed}.html", nice, seed))

    # --- animations: the step-through of the written methods. Self-contained,
    # no external refs, so it drops in as one file.
    anim_src = os.path.join(HERE, "animations", "index.html")
    has_anim = os.path.exists(anim_src)
    if has_anim:
        os.makedirs(os.path.join(OUT, "animations"), exist_ok=True)
        with open(anim_src) as f:
            a = scrub(f.read(), names)
        # the internal tab labels are kid IDs, which read as nonsense in public
        a = re.sub(r"<title>[^<]*</title>",
                   "<title>How long division and multiplication actually work</title>", a)
        a = a.replace("kid1 &amp; kid2", "step by step").replace("kid1 & kid2", "step by step")
        # Strip the kid-ID prefix from tab labels and headings. Internally the tabs are
        # keyed per child; publicly "kid1 — Multiplying by one digit" is noise, and the
        # subtitle underneath already names the skill.
        # The visible tab labels are composed in JS from the per-child `kid` field,
        # so there is nothing in the static markup to rewrite — patch the two
        # templates instead. Internally the animations stay keyed per child; publicly
        # "kid1 — Multiplying by one digit" is noise and the skill line says it anyway.
        a = a.replace("`<b>${a.kid} \u2014 ${a.title}</b>${a.skill}`",
                      "`<b>${a.title}</b>${a.skill}`")
        a = a.replace("`${a.kid} \u00b7 ${a.title}`", "`${a.title}`")
        with open(os.path.join(OUT, "animations", "index.html"), "w") as f:
            f.write(with_nav(a))

    # --- index
    def cards(items, folder):
        return "\n".join(
            f'<li><a class="card" href="{folder}/{fn}"><b>{_html.escape(lbl)}</b>'
            f'<span>{_html.escape(sub)}</span></a></li>'
            for fn, lbl, sub in items)

    word = [(f, l, k) for f, l, k in published if "logic" not in k]
    logic = [(f, l, k) for f, l, k in published if "logic" in k]
    dr = [(f, f"{n} #{s}", "5-minute drill · answer key included") for f, n, s in drills]

    body = f"""
<h1>Printable math worksheets</h1>
<p class="lede">Word problems, logic puzzles, and arithmetic drills for roughly 3rd&ndash;5th grade.
Every sheet is one page per kid plus a worked answer key. Print them, no signup, no ads.</p>

<div class="note">Two things here are unusual. <b>Drills are sized to five minutes</b>, not
to fill a page &mdash; 20 long divisions is a sixteen-minute sheet, and most sites give you
20 regardless. And <b>the grid forces the work to be shown</b>: every step of the written
method has its own box, so you can see where it went wrong instead of just that it did.</div>

<h2>Watch the method first</h2>
<p class="lede">Four step-through animations of the <em>written</em> methods the drills
ask for &mdash; long division and multiplication, one pencil mark at a time, with the
trap called out at the exact step where it bites. Watch one, then do the paper.</p>
<ul class="grid"><li><a class="card hero" href="animations/index.html">
<b>How the methods actually work &rarr;</b>
<span>Long division &amp; multiplication, one mark at a time &middot; no signup</span>
</a></li></ul>

<h2 id="drills">Drills &mdash; five minutes, work shown</h2>
<p class="lede">Each is a different randomly generated set at the same difficulty. No
problem is ever &times;0, &times;1 or &divide;1 &mdash; those spend a slot teaching nothing.</p>
<ul class="grid">{cards(dr, "drills")}</ul>

<h2 id="word">Word problems</h2>
<p class="lede">Every problem is multi-step on purpose &mdash; choosing the operation is the
test, not the arithmetic. Each ends with a &ldquo;Did you know?&rdquo; tied to its story.</p>
<ul class="grid">{cards(word, "sheets")}</ul>

<h2 id="logic">Logic puzzles</h2>
<p class="lede">Reasoning rather than fluency. No arithmetic needed to start.</p>
<ul class="grid">{cards(logic, "sheets")}</ul>

<h2>How the five-minute number works</h2>
<p class="lede">A problem costs roughly what it costs to <em>write</em>. Count the marks the
standard method puts on paper, price them, and fill the time budget:</p>
<div class="scroll"><table>
<tr><th>Skill</th><th>Marks</th><th>Approx. seconds</th><th>Fits 5 min</th><th>Typical site ships</th></tr>
<tr><td>2-digit &times; 1-digit</td><td>2.7</td><td>10</td><td>28</td><td>25</td></tr>
<tr><td>2-digit &times; 2-digit</td><td>9.1</td><td>30</td><td>9</td><td>20</td></tr>
<tr><td>2-digit &divide; 1-digit</td><td>10.0</td><td>33</td><td>9</td><td>25</td></tr>
<tr><td>3-digit &divide; 1-digit</td><td>15.0</td><td>48</td><td>6</td><td>20</td></tr>
<tr><td>4-digit &divide; 1-digit</td><td>20.0</td><td>64</td><td>4</td><td>12</td></tr>
</table></div>
<p class="lede">Multiplication scales with the <em>product</em> of the digit counts, division
with the number of quotient digits. That&rsquo;s why a 2&times;2 costs three times a 2&times;1
while looking barely bigger on the page.</p>
<p class="lede"><b>Calibration, honestly:</b> the seconds come from one timed measurement
(49 subtraction problems in 13 minutes) extrapolated to the other operations. The mark
counts are exact; the seconds are an estimate. Time your own kid and the numbers move.</p>
"""
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(shell("Printable math worksheets", body))

    print(f"built {OUT}")
    print(f"  {len(published)} worksheets, {len(drills)} drill sheets")
    print("  NOW RUN: python3 verify_public.py   (the build is not trusted until it passes)")


if __name__ == "__main__":
    main()
