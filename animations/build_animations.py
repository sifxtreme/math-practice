#!/usr/bin/env python3
"""Build `index.html` — the drill-method animations for kid1 and kid2.

Run:  python3 build_animations.py
Then: python3 verify_animations.py      <- must exit 0 before you show it to anyone

Every digit on screen comes out of `specs.py`, which runs the real algorithm.
Nothing here is hand-typed arithmetic. Edit the SPECS block below to change a
worked example; do NOT hand-edit index.html, it is overwritten on every build.
"""

import json
import pathlib

from specs import mult_by_one_digit, mult_two_by_two, long_division

HERE = pathlib.Path(__file__).parent
DRILL = "https://math-drills.com"

# --------------------------------------------------------------- the four

SPECS = [
    dict(
        id="kid1-mult", kid="kid1", grade="3rd → 4th", theme="teal",
        title="Multiplying by one digit",
        skill="3-digit × 1-digit, with carrying",
        drill_slug="multiplication_0301",
        drill_url=f"{DRILL}/multiplication2/multiplication_0301_001.php",
        why="The bottom number visits every digit on top, one at a time, right to left. "
            "Anything too big for its box gets parked on the shelf above the next column.",
        build=lambda: mult_by_one_digit(247, 6),
        rules=[
            "Line up the <b>ones</b> column. Always.",
            "Work <b>right to left</b> — ones, then tens, then hundreds.",
            "<b>Multiply first, then add the carry.</b> Never the other way round.",
            "A carry gets <b>written above</b>, not remembered.",
        ],
        try_kind="m1", try_items=[(138, 4), (306, 7), (429, 8)],
        try_note="The middle one has a <b>0</b> in it on purpose — 7 × 0 is still 0, "
                 "but the carry coming in still has to be added.",
    ),
    dict(
        id="kid1-div", kid="kid1", grade="3rd → 4th", theme="teal",
        title="Long division with a remainder",
        skill="2-digit ÷ 1-digit, remainder left over",
        drill_slug="division_long_1dd2dd_r",
        drill_url=f"{DRILL}/division/division_long_1dd2dd_r_001.php",
        why="Four moves, in the same order, over and over until you run out of digits: "
            "<b>Divide, Multiply, Subtract, Bring down.</b> Never skip one, never reorder them.",
        build=lambda: long_division(67, 5),
        rules=[
            "<b>D</b>ivide → <b>M</b>ultiply → <b>S</b>ubtract → <b>B</b>ring down. Repeat.",
            "The answer digit goes <b>directly above</b> the digit you just used.",
            "After subtracting, the leftover must be <b>smaller than the divisor</b>. "
            "If it isn't, your digit was too small.",
            "When there is nothing left to bring down, whatever is left is the <b>remainder</b>.",
        ],
        try_kind="dv", try_items=[(83, 6), (59, 4), (74, 8)],
        try_note="Say the four moves out loud on every single one. Out loud is the point.",
    ),
    dict(
        id="kid2-mult", kid="kid2", grade="4th → 5th", theme="violet",
        title="Two digits times two digits",
        skill="2-digit × 2-digit, two partial products",
        drill_slug="multiplication_0202",
        drill_url=f"{DRILL}/multiplication2/multiplication_0202_001.php",
        why="Two digits on the bottom means two rounds, so two answer rows, then you add them. "
            "Round 2 is multiplying by a <b>tens</b> digit, which is why it starts with a 0.",
        build=lambda: mult_two_by_two(47, 36),
        rules=[
            "Round 1 = the <b>ones</b> digit. Round 2 = the <b>tens</b> digit.",
            "<b>Row 2 starts with a 0 in the ones column.</b> Write the 0 before you multiply anything.",
            "<b>Cross out the row-1 carries</b> before starting row 2.",
            "Add the two rows at the end — that is the answer, not row 2 on its own.",
        ],
        try_kind="m2", try_items=[(58, 24), (73, 46), (89, 37)],
        try_note="Before you add the two rows, point at the 0 and check it is there. Every time.",
    ),
    dict(
        id="kid2-div", kid="kid2", grade="4th → 5th", theme="violet",
        title="Long division, big numbers",
        skill="4-digit ÷ 1-digit, remainder — and a zero in the answer",
        drill_slug="division_long_1dd4dd_r",
        drill_url=f"{DRILL}/division/division_long_1dd4dd_r_001.php",
        why="Same four moves as always — but with more digits you hit the two traps that eat "
            "long division: the divisor not fitting in the first digit, and a <b>0 landing in the "
            "middle of the answer</b>.",
        build=lambda: long_division(4231, 7),
        rules=[
            "<b>D</b>ivide → <b>M</b>ultiply → <b>S</b>ubtract → <b>B</b>ring down. Repeat.",
            "Doesn't fit in the first digit? Take <b>two</b> digits, and write nothing above the first.",
            "Doesn't fit after a bring-down? <b>Write a 0 up top</b> and keep going.",
            "A zero at the <b>front</b> you skip. A zero in the <b>middle</b> you must write.",
        ],
        try_kind="dv", try_items=[(3025, 6), (5138, 9), (2417, 4)],
        try_note="All three of these have a <b>0 in the answer</b>. That is not a coincidence — "
                 "it is the thing being practised.",
    ),
]


# --------------------------------------------------------------- assemble

def try_block(kind, items):
    out = []
    for a, b in items:
        if kind in ("m1", "m2"):
            out.append({"q": f"{a} × {b}", "a": f"{a * b}"})
        else:
            out.append({"q": f"{a} ÷ {b}", "a": f"{a // b} R{a % b}"})
    return out


def build():
    anims = []
    for s in SPECS:
        core = s["build"]()
        traps = [st["trap"] for st in core["steps"] if st.get("trap")]
        anims.append({
            "id": s["id"], "kid": s["kid"], "grade": s["grade"], "theme": s["theme"],
            "title": s["title"], "skill": s["skill"], "why": s["why"],
            "drillSlug": s["drill_slug"], "drillUrl": s["drill_url"],
            "rules": s["rules"], "traps": traps,
            "youTry": try_block(s["try_kind"], s["try_items"]),
            "tryNote": s["try_note"],
            "cols": core["cols"], "rows": core["rows"],
            "toks": core["toks"], "decor": core["decor"], "steps": core["steps"],
            "model": core["model"],
            "answer": str(core["answer"]),
        })
    return anims


HTML = r"""<meta charset="utf-8">
<title>How to do the drills — kid1 &amp; kid2</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{
  --bg:#f7f5fb; --card:#ffffff; --ink:#14142b; --mute:#6b6480; --line:#e3ddf0;
  --accent:#6d28d9; --accent-soft:#f3eeff; --warn:#b4530a; --warn-bg:#fff5e9;
  --warn-line:#f3c893; --ok:#0f766e; --why:#1d4ed8; --why-bg:#eef3ff; --why-line:#c3d4fb;
  --shadow:0 1px 2px rgba(20,20,43,.05),0 8px 28px rgba(20,20,43,.07);
}
[data-theme="teal"]{ --accent:#0e7490; --accent-soft:#e8f6fa; }
[data-theme="violet"]{ --accent:#6d28d9; --accent-soft:#f3eeff; }
@media (prefers-color-scheme:dark){
  :root{ --bg:#131120; --card:#1c1930; --ink:#f0edf8; --mute:#a49bbd; --line:#2f2a47;
         --accent-soft:#241f3d; --warn:#f0a860; --warn-bg:#2c2113; --warn-line:#5b4322;
         --why:#8fb4ff; --why-bg:#151d33; --why-line:#2b3d63;
         --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px rgba(0,0,0,.35); }
  [data-theme="teal"]{ --accent:#38bcd8; --accent-soft:#16303a; }
  [data-theme="violet"]{ --accent:#b190ff; --accent-soft:#282047; }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font-family:Georgia,"Iowan Old Style","Times New Roman",serif;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:22px 18px 70px}

header h1{font-size:26px;margin:0 0 4px;letter-spacing:-.2px}
header .thesis{font-size:15.5px;color:var(--mute);margin:0 0 18px;max-width:64ch}
header .thesis b{color:var(--ink)}

.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.tab{font:inherit;font-size:14px;cursor:pointer;background:var(--card);color:var(--mute);
     border:1.5px solid var(--line);border-radius:10px;padding:8px 14px;text-align:left;
     transition:background-color .16s ease,border-color .16s ease,color .16s ease;line-height:1.25}
.tab b{display:block;font-size:15px;color:var(--ink)}
.tab:hover{border-color:var(--accent)}
.tab[aria-selected=true]{background:var(--accent);border-color:var(--accent);color:#fff;
     box-shadow:var(--shadow)}
.tab[aria-selected=true] b{color:#fff}

.stage{display:grid;grid-template-columns:minmax(0,1.28fr) minmax(300px,.72fr);gap:16px;align-items:start}
@media(max-width:920px){.stage{grid-template-columns:1fr}}

.card{background:var(--card);border:1.5px solid var(--line);border-radius:14px;
      padding:16px 18px;box-shadow:var(--shadow);margin-bottom:16px}
.card:last-child{margin-bottom:0}
.card h2{font-size:11px;letter-spacing:1.3px;text-transform:uppercase;color:var(--accent);
         margin:0 0 10px;font-weight:700}
.boardsub{font-size:13.5px;color:var(--mute);margin:-4px 0 12px}

/* ---------- the board ---------- */
.boardwrap{position:relative;display:flex;justify-content:center;padding:24px 6px 12px;overflow-x:auto}
.board{display:grid;justify-items:center;align-items:center;
       grid-template-columns:repeat(var(--cols),var(--cw));
       grid-template-rows:repeat(var(--rows),minmax(6px,auto));
       column-gap:2px;row-gap:5px;
       font-family:"SF Mono",ui-monospace,"Menlo","DejaVu Sans Mono",monospace;
       --cw:clamp(38px,8.4vw,58px)}
.board .cell{display:flex;align-items:flex-end;justify-content:center;gap:3px;min-height:1px}
.board .tok{font-size:clamp(28px,6.4vw,44px);font-weight:600;line-height:1.06;
     opacity:0;position:relative}
/* `.on` is STATE, not motion. The appearing is driven by the Web Animations API
   so each mark can be sequenced behind the pen instead of all landing at once. */
.board .tok.on{opacity:1}
.board .tok.op{color:var(--mute);font-weight:400}
.board .tok.hot,.board .tok.hot2{color:var(--accent)}
.board .tok.ans,.board .tok.quo{color:var(--accent)}
.board .tok.subtrahend{color:var(--mute)}
.board .tok.carry{font-size:clamp(15px,3.1vw,21px);font-weight:700;color:var(--warn)}
.board .tok.carry2{color:var(--accent)}
.board .tok.zero{color:var(--warn)}
.board .tok.rlab{font-size:clamp(18px,3.6vw,26px);font-weight:700;color:var(--accent);
          align-self:center;padding-left:4px}
.board .tok.flash::before{content:"";position:absolute;inset:-6px -7px;border-radius:8px;
     border:2.5px solid var(--accent);animation:ring 1.15s ease-in-out infinite}
@keyframes ring{0%,100%{opacity:.28;transform:scale(.97)}50%{opacity:1;transform:scale(1.03)}}
.board .tok.struck{color:var(--mute);opacity:.55}
.board .tok.struck::after{content:"";position:absolute;left:-14%;right:-14%;top:52%;height:2.5px;
     background:currentColor;transform:rotate(-16deg) scaleX(0);transform-origin:left center;
     animation:strike .3s ease-out forwards}
@keyframes strike{to{transform:rotate(-16deg) scaleX(1)}}

.decor{width:100%;opacity:0;transition:opacity .22s ease}
.decor.on{opacity:1}
.decor.rule{border-top:3px solid var(--ink);height:0;align-self:center}
.decor.bracket{border-top:3.5px solid var(--ink);border-left:3.5px solid var(--ink);
     border-top-left-radius:14px;height:100%;align-self:stretch;opacity:1;
     margin-left:-6px;width:calc(100% + 6px)}

/* The product exists as a NUMBER before it is split. Without this the 2 and the 4
   just appear in two places at once and the kid never sees the 42 they came out of. */
.bubble{position:absolute;left:0;top:0;display:none;align-items:center;gap:1px;
  padding:5px 13px;z-index:4;pointer-events:none;
  font-family:"SF Mono",ui-monospace,"Menlo",monospace}
.bubble .shell{position:absolute;inset:0;border-radius:13px;background:var(--card);
  border:2.5px solid var(--accent);box-shadow:0 7px 22px rgba(20,20,43,.14)}
@media (prefers-color-scheme:dark){.bubble .shell{box-shadow:0 7px 22px rgba(0,0,0,.5)}}
.bubble.up{display:flex;animation:bubblePop .34s cubic-bezier(.2,.9,.3,1.45)}
@keyframes bubblePop{from{opacity:0;transform:scale(.62)}to{opacity:1;transform:none}}
.bubble .bd{position:relative;font-size:clamp(25px,5.4vw,40px);font-weight:700;
  color:var(--accent);line-height:1.06;display:block}
/* a digit bound for the shelf already looks like a carry while it flies, so there
   is no colour jump at the handoff */
.bubble .bd.to-carry{color:var(--warn)}
/* the D-step chip is a stack of candidates, not an inline expression */
.bubble.trial{flex-direction:column;align-items:stretch;gap:1px;padding:8px 10px}
.bubble.trial .trow{display:flex;align-items:center;gap:2px;padding:3px 5px;
  border-radius:7px;opacity:.48;position:relative}
.bubble.trial .trow.fits{opacity:1;background:var(--accent-soft)}
.bubble.trial .bd{font-size:clamp(16px,3vw,22px)}
.bubble.trial .bop{font-size:clamp(12px,2.4vw,16px);padding:0 2px}
.bubble.trial .tag{margin-left:7px;font-size:10px;letter-spacing:.7px;font-weight:700;
  text-transform:uppercase;font-family:ui-monospace,monospace;white-space:nowrap}
.bubble.trial .trow.small .tag,.bubble.trial .trow.big .tag{color:var(--warn)}
.bubble.trial .trow.fits .tag{color:var(--accent)}
.bubble .bop{position:relative;font-size:clamp(17px,3.4vw,25px);font-weight:600;
  color:var(--mute);padding:0 4px;line-height:1.06;display:block}

/* the pen goes to the spot BEFORE the mark appears, so writing order is visible */
.pen{position:absolute;left:0;top:0;pointer-events:none;z-index:5;opacity:0;
     will-change:transform,opacity}
.pen.up{opacity:1}
.pen .body{fill:var(--accent)}
.pen .nib{fill:var(--ink)}

/* ---------- D-M-S-B beat ---------- */
.beats{display:flex;gap:6px;justify-content:center;margin-top:4px}
.beat{font-family:ui-monospace,monospace;font-size:11px;font-weight:700;letter-spacing:.6px;
      border:1.5px solid var(--line);color:var(--mute);border-radius:7px;padding:4px 11px;
      transition:background-color .2s ease,border-color .2s ease,color .2s ease,transform .2s
        cubic-bezier(.2,.9,.3,1.4)}
.beat.now{background:var(--accent);border-color:var(--accent);color:#fff;transform:scale(1.09)}

/* ---------- narration, right under the board ---------- */
.stepbadge{display:inline-block;font-family:ui-monospace,monospace;font-size:11px;font-weight:700;
     letter-spacing:1.4px;background:var(--accent);color:#fff;padding:3px 9px;border-radius:5px;
     margin-bottom:9px}
.say{font-size:18px;min-height:3.2em;margin:0}
.say b{color:var(--accent)}
.whybox{margin-top:12px;background:var(--why-bg);border:1.5px solid var(--why-line);
        border-left:5px solid var(--why);border-radius:9px;padding:11px 14px;font-size:15px}
.whybox .lbl{display:block;font-size:10.5px;letter-spacing:1.3px;text-transform:uppercase;
        font-weight:700;color:var(--why);margin-bottom:4px;font-family:ui-monospace,monospace}
.whybox b{color:var(--why)}
.trap{margin-top:10px;background:var(--warn-bg);border:1.5px solid var(--warn-line);
      border-left:5px solid var(--warn);border-radius:9px;padding:10px 13px;font-size:14.5px}
.trap .lbl{display:block;font-size:10.5px;letter-spacing:1.3px;text-transform:uppercase;
      font-weight:700;color:var(--warn);margin-bottom:3px;font-family:ui-monospace,monospace}
.trap b{color:var(--warn)}

/* ---------- the model: same sum drawn a second way ---------- */
.modelwrap{display:flex;justify-content:center;padding:6px 0 2px;overflow-x:auto}
.area{display:grid;gap:0;font-family:ui-monospace,monospace;max-width:560px}
.acell{position:relative;background:var(--accent-soft);border:1.5px solid var(--line);
       margin:-0.75px;min-height:52px;padding:6px 4px;display:flex;flex-direction:column;
       align-items:center;justify-content:center;opacity:.45;
       transition:opacity .28s ease,background-color .28s ease,outline-color .28s ease}
/* the slices share edges — it is ONE rectangle cut up, not four tiles */
.acell.lit{opacity:1;background:var(--card);z-index:2;
       outline:2.5px solid var(--accent);outline-offset:-2.5px}
.acell .mul{font-size:11px;color:var(--mute);white-space:nowrap}
.acell .val{font-size:19px;font-weight:700;color:var(--ink)}
.ahead{font-family:ui-monospace,monospace;font-size:13px;font-weight:700;color:var(--accent);
       display:flex;align-items:center;justify-content:center;padding:2px}
.asum{font-family:ui-monospace,monospace;font-size:13px;color:var(--mute);
      display:flex;align-items:center;padding-left:8px;white-space:nowrap;opacity:.45;
      transition:opacity .28s ease,color .28s ease}
.asum.lit{opacity:1;color:var(--accent);font-weight:700}

.ladder{font-family:ui-monospace,monospace;font-size:16px;line-height:1.65;
        border-collapse:collapse}
.ladder td{padding:2px 10px;text-align:right;transition:color .25s ease}
.ladder tr{opacity:.42;transition:opacity .25s ease}
.ladder tr.lit{opacity:1}
.ladder tr.lit td.note{color:var(--accent);font-weight:700}
.ladder td.note{text-align:left;font-size:12.5px;color:var(--mute);white-space:nowrap}
.ladder td.num{border-bottom:0}
.ladder tr.sub td.num{color:var(--mute)}
.ladder tr.line td.num{border-top:2.5px solid var(--ink)}
.ladder tr.line td{padding:0;height:0}
.ladder tfoot td{padding-top:9px;font-weight:700;color:var(--accent)}
.mcap{font-size:13px;color:var(--mute);margin:12px 0 0;text-align:center;max-width:62ch;
      margin-left:auto;margin-right:auto}
.mcap b{color:var(--ink)}

/* ---------- controls ---------- */
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:14px}
button.ctl{font:inherit;font-size:14.5px;cursor:pointer;border-radius:9px;padding:9px 15px;
     border:1.5px solid var(--line);background:var(--card);color:var(--ink);
     transition:border-color .14s ease,color .14s ease,opacity .14s ease}
button.ctl:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
button.ctl:disabled{opacity:.35;cursor:default}
button.ctl.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700;
     min-width:118px}
button.ctl.primary:hover{opacity:.9;color:#fff}
.spd{margin-left:auto;font-size:13px;color:var(--mute);display:flex;align-items:center;gap:6px}
.spd select{font:inherit;font-size:13px;padding:4px 6px;border-radius:7px;
     border:1.5px solid var(--line);background:var(--card);color:var(--ink)}
.dots{display:flex;flex-wrap:wrap;gap:5px;margin-top:12px}
.dot{flex:1 1 12px;min-width:10px;height:7px;border-radius:4px;background:var(--line);
     border:0;padding:0;cursor:pointer;
     transition:background-color .18s ease,opacity .18s ease,transform .18s ease}
.dot.done{background:var(--accent);opacity:.42}
.dot.now{background:var(--accent);opacity:1;transform:scaleY(1.6)}
.hint{font-size:12.5px;color:var(--mute);margin-top:9px}
kbd{font-family:ui-monospace,monospace;font-size:11.5px;background:var(--accent-soft);
    border:1px solid var(--line);border-radius:4px;padding:1px 5px}

/* ---------- side cards ---------- */
ul.rules{margin:0;padding-left:19px;font-size:14.5px}
ul.rules li{margin-bottom:7px}
ul.rules b{color:var(--accent)}
.why{font-size:14.5px;margin:0 0 10px}
.why b{color:var(--accent)}
.drill{font-size:13px;color:var(--mute);margin-top:11px;padding-top:10px;border-top:1px solid var(--line)}
.drill a{color:var(--accent)}
.drill code{font-family:ui-monospace,monospace;font-size:12px;background:var(--accent-soft);
     padding:1px 5px;border-radius:4px}
.tryrow{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px dashed var(--line);
     font-size:17px}
.tryrow:last-child{border-bottom:0}
.tryq{font-family:ui-monospace,monospace;font-weight:600;min-width:9ch}
.tryrow button{font:inherit;font-size:12.5px;cursor:pointer;background:var(--accent-soft);
     border:1px solid var(--line);color:var(--accent);border-radius:7px;padding:6px 12px}
.trya{font-family:ui-monospace,monospace;font-weight:700;color:var(--ok);visibility:hidden}
.trya.shown{visibility:visible}
.trynote{font-size:13.5px;color:var(--mute);margin:11px 0 0}
.watch ol{margin:0;padding-left:19px;font-size:14px;color:var(--mute)}
.watch li{margin-bottom:8px}
.watch b{color:var(--ink)}
footer{margin-top:26px;font-size:12.5px;color:var(--mute);text-align:center}

/* ---------- phone / iPad portrait ----------
   Measured on a 390px viewport: the board started 589px down and Next/Play sat at
   1128px, so you could not see the problem and advance it at the same time — which
   is the entire interaction. Four stacked tabs alone ate 600px. */
@media (max-width:700px){
  header .thesis{font-size:13.5px;margin-bottom:12px}
  header h1{font-size:22px}
  .wrap{padding:16px 14px 104px}
  .tabs{flex-wrap:nowrap;overflow-x:auto;gap:6px;padding-bottom:4px;
        scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .tabs::-webkit-scrollbar{display:none}
  .tab{flex:0 0 auto;padding:9px 13px;font-size:0;min-height:44px;display:flex;align-items:center}
  .tab b{font-size:13.5px;white-space:nowrap}
  /* the controls follow you down the page — nothing else about this works without it */
  .controls{position:fixed;left:0;right:0;bottom:0;z-index:40;margin:0;gap:7px;
            padding:9px 12px calc(9px + env(safe-area-inset-bottom,0px));
            background:var(--card);border-top:1.5px solid var(--line);
            box-shadow:0 -6px 22px rgba(20,20,43,.13)}
  button.ctl{padding:11px 14px;min-height:44px}
  button.ctl.primary{min-width:96px}
  .spd select{min-height:40px}
  .hint{display:none}
  .say{font-size:16.5px;min-height:0}
  .tryrow button{min-height:40px;padding:8px 14px}
  .beat{padding:5px 0;flex:1;text-align:center;font-size:12px}
  .beat .word{display:none}
  .beats{gap:5px}
}
@media (prefers-color-scheme:dark) and (max-width:700px){
  .controls{box-shadow:0 -6px 22px rgba(0,0,0,.5)}
}

@media (prefers-reduced-motion:reduce){
  .board .tok,.decor,.pen,.acell,.ladder tr{transition:none}
  .board .tok.flash::before,.board .tok.struck::after{animation:none}
  .board .tok.struck::after{transform:rotate(-16deg) scaleX(1)}
  .board .tok.flash::before{opacity:1}
  .pen{display:none}
  .bubble.up{animation:none}
}
@media print{
  body{background:#fff}
  .tabs,.controls,.dots,.hint,footer,.trap,.say,.stepbadge,.pen,.beats,
  .bubble{display:none!important}
  .board .tok,.decor{opacity:1!important;transform:none!important}
  .acell,.ladder tr{opacity:1!important}
  .card{break-inside:avoid;box-shadow:none}
}
</style>

<div class="wrap">
  <header>
    <h1>How to do the drills</h1>
    <p class="thesis">One method per drill sheet, one written mark at a time.
      The whole point of these methods is that <b>you don't hold anything in your head</b> —
      every number you think of goes down on the paper. And every mark <b>means</b> something:
      that carry isn't a 4, it's 40. Watch it once, then do the sheet.</p>
  </header>

  <div class="tabs" role="tablist" id="tabs"></div>

  <div class="stage">
    <div>
      <div class="card">
        <h2 id="bTitle">—</h2>
        <p class="boardsub" id="bSkill">—</p>
        <div class="boardwrap" id="boardwrap">
          <div class="board" id="board"></div>
          <div class="bubble" id="bubble" aria-hidden="true"></div>
          <svg class="pen" id="pen" width="38" height="46" viewBox="0 0 38 46" aria-hidden="true">
            <path class="body" d="M6.5 9.5 L10.5 5.8 L34 34.5 A4.4 4.4 0 0 1 27.5 40.5 Z"/>
            <path class="nib" d="M2 2 L11 6.4 L7.2 10.2 Z"/>
          </svg>
        </div>
        <div class="beats" id="beats"></div>
        <div class="dots" id="dots"></div>
      </div>

      <div class="card">
        <span class="stepbadge" id="badge">SET UP</span>
        <p class="say" id="say"></p>
        <div id="whyBox"></div>
        <div id="trapBox"></div>
        <div class="controls">
          <button class="ctl" id="back">◀ Back</button>
          <button class="ctl primary" id="play">▶ Play</button>
          <button class="ctl" id="next">Next ▶</button>
          <button class="ctl" id="restart">↺</button>
          <span class="spd"><label for="speed">Speed</label>
            <select id="speed">
              <option value="1.5">Slow</option>
              <option value="1" selected>Normal</option>
              <option value="0.65">Quick</option>
            </select></span>
        </div>
        <p class="hint"><kbd>space</kbd> next · <kbd>←</kbd> back · <kbd>R</kbd> restart ·
           <kbd>P</kbd> play · <kbd>1</kbd>–<kbd>4</kbd> switch sheet</p>
      </div>

      <div class="card">
        <h2 id="mTitle">The same sum, drawn</h2>
        <div class="modelwrap"><div id="model"></div></div>
        <p class="mcap" id="mcap"></p>
      </div>
    </div>

    <div>
      <div class="card">
        <h2>The rule, short version</h2>
        <p class="why" id="whyShort"></p>
        <ul class="rules" id="rules"></ul>
        <p class="drill" id="drill"></p>
      </div>

      <div class="card">
        <h2>Now you try — same shape, on paper</h2>
        <div id="tryRows"></div>
        <p class="trynote" id="tryNote"></p>
      </div>

      <div class="card watch">
        <h2>Watch for — for the grown-up</h2>
        <ol id="watch"></ol>
      </div>
    </div>
  </div>

  <footer>Built from <code>build_animations.py</code> · every digit derived by running the
    algorithm, checked by <code>verify_animations.py</code></footer>
</div>

<script id="ANIM" type="application/json">__DATA__</script>
<script>
const A = JSON.parse(document.getElementById('ANIM').textContent);
const $ = id => document.getElementById(id);
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
let ai = 0, si = 0, timer = null, playing = false;

A.forEach((a, i) => {
  const b = document.createElement('button');
  b.className = 'tab'; b.setAttribute('role', 'tab');
  b.innerHTML = `<b>${a.kid} — ${a.title}</b>${a.skill}`;
  b.onclick = () => pick(i);
  $('tabs').appendChild(b);
});

function pick(i){
  stop(); ai = i; si = 0;
  const a = A[i];
  document.documentElement.setAttribute('data-theme', a.theme);
  [...$('tabs').children].forEach((t, k) => {
    t.setAttribute('aria-selected', k === i);
    if (k === i) t.scrollIntoView({ inline: 'nearest', block: 'nearest', behavior: 'smooth' });
  });
  $('bTitle').textContent = `${a.kid} · ${a.title}`;
  $('bSkill').textContent = `${a.skill} — worked example, one mark at a time`;
  $('whyShort').innerHTML = a.why;
  $('rules').innerHTML = a.rules.map(r => `<li>${r}</li>`).join('');
  $('drill').innerHTML = `Matching drill sheet: <code>${a.drillSlug}</code> —
    <a href="${a.drillUrl}" target="_blank" rel="noopener">open on math-drills.com</a>
    (variants <code>_001</code>…<code>_010</code>)`;
  $('watch').innerHTML = a.traps.map(t => `<li>${t}</li>`).join('');
  $('tryNote').innerHTML = a.tryNote;
  $('mTitle').textContent = a.model.kind === 'area'
    ? 'The same sum, drawn as a rectangle' : 'The same division, without the shorthand';
  $('mcap').innerHTML = a.model.caption;
  $('tryRows').innerHTML = '';
  a.youTry.forEach((t, k) => {
    const row = document.createElement('div');
    row.className = 'tryrow';
    row.innerHTML = `<span class="tryq">${t.q} =</span>
      <button type="button">show</button><span class="trya" id="ta${k}">${t.a}</span>`;
    row.querySelector('button').onclick = e => {
      const el = $('ta' + k); el.classList.toggle('shown');
      e.target.textContent = el.classList.contains('shown') ? 'hide' : 'show';
    };
    $('tryRows').appendChild(row);
  });
  penXY = null; prevSi = 0;
  buildBoard(a); buildBeats(a); buildModel(a); buildDots(a);
  reserveChipGutter(a);
  apply(true);
}

function buildBoard(a){
  const b = $('board');
  b.innerHTML = '';
  b.style.setProperty('--cols', a.cols);
  b.style.setProperty('--rows', a.rows);
  a.decor.forEach(d => {
    const el = document.createElement('div');
    el.className = 'decor ' + d.kind;
    el.dataset.k = d.k;
    el.style.gridRow = d.r;
    el.style.gridColumn = `${d.c0} / ${d.c1 + 1}`;
    b.appendChild(el);
  });
  const cells = new Map();
  a.toks.forEach(t => {
    const key = t.r + ':' + t.c;
    if (!cells.has(key)) {
      const c = document.createElement('div');
      c.className = 'cell';
      c.style.gridRow = t.r; c.style.gridColumn = t.c;
      cells.set(key, c); b.appendChild(c);
    }
    const s = document.createElement('span');
    s.className = 'tok ' + t.cls; s.dataset.k = t.k; s.textContent = t.t;
    cells.get(key).appendChild(s);
  });
}

function reserveChipGutter(a){
  const wrapEl = $('boardwrap');
  wrapEl.style.paddingRight = '';
  const need = Math.max(0, ...a.steps.map(s => (s.bubble && s.bubble.reserveW) || 0));
  if (!need) return;
  // only steal the space if what's left still comfortably holds the board
  const avail = wrapEl.clientWidth, board = $('board').getBoundingClientRect().width;
  if (avail - need - 26 > board + 30) wrapEl.style.paddingRight = (need + 26) + 'px';
}

function buildBeats(a){
  const has = a.steps.some(s => s.beat);
  $('beats').innerHTML = has
    ? ['D','M','S','B'].map((x, i) =>
        `<span class="beat" data-beat="${x}">${x}<span class="word"> · ${['Divide','Multiply','Subtract','Bring down'][i]}</span></span>`
      ).join('') : '';
}

function buildModel(a){
  const m = a.model, host = $('model');
  host.innerHTML = '';
  if (m.kind === 'area') {
    // compressed weights: raw place values are far too lopsided to draw to scale
    const w = v => Math.max(1, Math.pow(v, 0.45));
    const el = document.createElement('div');
    el.className = 'area';
    el.style.gridTemplateColumns =
      `auto ${m.cols.map(c => w(c.v).toFixed(2) + 'fr').join(' ')} auto`;
    el.style.gridTemplateRows = `auto ${m.rows.map(r => w(r.v).toFixed(2) + 'fr').join(' ')}`;
    el.appendChild(Object.assign(document.createElement('div'), { className: 'ahead' }));
    m.cols.forEach(c => {
      const h = document.createElement('div'); h.className = 'ahead'; h.textContent = c.v;
      el.appendChild(h);
    });
    el.appendChild(Object.assign(document.createElement('div'), { className: 'ahead' }));
    m.rows.forEach((r, ri) => {
      const h = document.createElement('div'); h.className = 'ahead'; h.textContent = '× ' + r.v;
      el.appendChild(h);
      m.cols.forEach((c, ci) => {
        const cell = m.cells.find(x => x.r === ri && x.c === ci);
        const d = document.createElement('div');
        d.className = 'acell'; d.dataset.r = ri; d.dataset.c = ci;
        d.innerHTML = `<span class="mul">${r.v} × ${c.v}</span><span class="val">${cell.v}</span>`;
        el.appendChild(d);
      });
      const s = document.createElement('div');
      s.className = 'asum'; s.dataset.r = ri;
      s.textContent = m.rowSums ? '= ' + m.rowSums[ri] : '';
      el.appendChild(s);
    });
    host.appendChild(el);
  } else {
    const t = document.createElement('table');
    t.className = 'ladder';
    let html = `<tr class="lit"><td class="num">${m.start}</td><td class="note"></td></tr>`;
    m.rows.forEach((r, i) => {
      html += `<tr class="sub" data-r="${i}"><td class="num">− ${r.prod}</td>` +
              `<td class="note">${r.q} × ${m.divisor} = ${r.prod}</td></tr>`;
      html += `<tr class="line" data-r="${i}"><td class="num"></td><td></td></tr>`;
      html += `<tr data-r="${i}"><td class="num">${r.left}</td><td class="note">` +
              (i === m.rows.length - 1 ? 'remainder' : 'still to divide') + `</td></tr>`;
    });
    t.innerHTML = html +
      `<tfoot><tr class="lit"><td class="num">${m.rows.map(r => r.q).join(' + ')} = ${m.quotient}</td>` +
      `<td class="note">groups of ${m.divisor}, R${m.remainder}</td></tr></tfoot>`;
    host.appendChild(t);
  }
}

function buildDots(a){
  $('dots').innerHTML = '';
  a.steps.forEach((s, i) => {
    const d = document.createElement('button');
    d.className = 'dot'; d.title = s.label;
    d.onclick = () => { stop(); si = i; apply(); };
    $('dots').appendChild(d);
  });
}

/* ---------------- motion system ----------------
   One timing table so the whole page shares a feel. Everything animated below is
   transform/opacity only, so it stays on the compositor thread.

   The rule that makes it read as WRITING rather than as fading boxes: the pen
   arrives FIRST, the mark appears under the nib SECOND. v1 ran both at once,
   which is why the pen looked like decoration floating near a digit instead of
   the thing that made it. Marks within a step are also chained, not simultaneous —
   a hand writes one thing at a time. */
const T = {
  ink: 165, inkOut: 95, drop: 450, arc: 610, split: 820,
  travelMin: 95, travelMax: 330, pxPerMs: 0.62,
  chain: 0.5,     // how much the next mark overlaps the previous one settling
  sweep: 50,      // stagger when a step PLACES many marks (setup) rather than writing them
  ease: {
    travel: 'cubic-bezier(.45,.05,.2,1)',
    ink:    'cubic-bezier(.2,.9,.3,1)',
    arc:    'cubic-bezier(.4,.02,.2,1)',
    out:    'cubic-bezier(.4,0,1,1)',
  },
};
let running = [], timers = [], pending = [], penXY = null, prevSi = 0;

function haltMotion(){
  timers.forEach(clearTimeout); timers = [];
  // finish (not cancel) so a fast Next lands everything on its final state
  running.forEach(an => { try { an.finish(); } catch (e) {} });
  running = [];
  // anything still waiting its turn must not stay hidden
  pending.forEach(n => { n.style.opacity = ''; });
  pending = [];
}
/* `.on` lands in the write phase but the animation is created later, on a timer.
   Without this the mark is painted at full opacity in the gap and then restarts
   from zero — a visible double-take on every single step. */
function holdHidden(node){ if (node) { node.style.opacity = '0'; pending.push(node); } }
function release(node){
  if (!node) return;
  node.style.opacity = '';
  pending = pending.filter(n => n !== node);
}
function play(el, frames, opts){
  const an = el.animate(frames, opts);
  running.push(an);
  an.finished.catch(() => {}).then(() => { running = running.filter(x => x !== an); });
  return an;
}
function after(ms, fn){ timers.push(setTimeout(fn, ms)); }

function inkIn(node, fromBox, myBox){
  if (!node) return;
  release(node);
  if (fromBox && myBox) {                       // a carry: it ARCS in from the digit that made it
    const dx = fromBox.left - myBox.left, dy = fromBox.top - myBox.top;
    return play(node, [
      { transform: `translate(${dx}px,${dy}px) scale(1.45)`, opacity: 0, offset: 0 },
      { transform: `translate(${dx}px,${dy}px) scale(1.45)`, opacity: 1, offset: .14 },
      { transform: `translate(${dx * .45}px,${dy * .55 - 22}px) scale(1.18)`, opacity: 1, offset: .58 },
      { transform: 'none', opacity: 1, offset: 1 },
    ], { duration: T.arc, easing: T.ease.arc, fill: 'backwards' });
  }
  if (node.classList.contains('drop'))
    return play(node, [{ transform: 'translateY(-54px) scale(.72)', opacity: 0 },
                       { transform: 'none', opacity: 1 }],
                { duration: T.drop, easing: T.ease.ink, fill: 'backwards' });
  if (node.classList.contains('zero'))
    return play(node, [{ transform: 'scale(.2)', opacity: 0, offset: 0 },
                       { transform: 'scale(1.3)', opacity: 1, offset: .62 },
                       { transform: 'none', opacity: 1, offset: 1 }],
                { duration: T.arc * .8, easing: T.ease.ink, fill: 'backwards' });
  return play(node, [{ transform: 'translateY(-8px) scale(.86)', opacity: 0 },
                     { transform: 'none', opacity: 1 }],
              { duration: T.ink, easing: T.ease.ink, fill: 'backwards' });
}

/* Positioned to the RIGHT of the board so the split reads correctly: the ones digit
   travels down-left to the answer row, the carry travels up-left to the shelf. Both
   directions match what you tell the kid. Falls back to above the board when there
   is no room to the right, which is the case on a phone. */
function chipKey(b){
  if (!b) return '';
  return b.trials ? 'T' + b.divisor + ':' + b.cur + ':' + b.trials.map(t => t.n).join(',')
                  : b.cells.map(c => c.t).join('');
}
const VERDICT = { small: 'too small', fits: 'fits', big: 'too big' };
function trialHTML(b){
  return '<div class="trials">' + b.trials.map(t => {
    const part = t.part !== undefined ? ` data-part="${t.part}"` : '';
    const prod = String(t.prod).split('').map(ch => `<span class="bd">${ch}</span>`).join('');
    return `<div class="trow ${t.v}"><span class="bd"${part}>${t.n}</span>` +
           `<span class="bop">×</span><span class="bd">${b.divisor}</span>` +
           `<span class="bop">=</span>${prod}<span class="tag">${VERDICT[t.v]}</span></div>`;
  }).join('') + '</div>';
}
function showBubble(b, wrap, boardRect){
  const bub = $('bubble'), key = chipKey(b);
  const fresh = bub.dataset.key !== key;
  if (fresh) { bub.dataset.key = key;
    bub.classList.toggle('trial', !!b.trials);
    bub.style.position = 'absolute';
    bub.innerHTML = '<span class="shell"></span>' + (b.trials ? trialHTML(b)
      : b.cells.map((c, i) => c.op
        ? `<span class="bop" data-i="${i}">${c.t}</span>`
        : `<span class="bd" data-i="${i}"${c.part !== undefined ? ` data-part="${c.part}"` : ''}>${c.t}</span>`
        ).join('')); }
  const estW = b.reserveW || (b.cells || []).reduce((n, c) => n + (c.op ? 22 : 30), 32);
  const wrapW = $('boardwrap').clientWidth;
  const rightX = boardRect.right - wrap.left + 20;
  const fits = rightX + estW <= wrapW - 4;
  bub.style.left = (fits ? rightX : Math.max(4, (wrapW - estW) / 2)) + 'px';
  bub.style.top  = (fits ? boardRect.top - wrap.top + 6 : 0) + 'px';
  bub.classList.add('up');
  return fresh;
}
/* The carry does not teleport into the sum. It comes down off the shelf and lands in
   the expression, which is the whole answer to "how did the 14 happen". */
function growBubble(cells, grewFrom, boxes){
  const bub = $('bubble');
  let at = 0;
  [...bub.querySelectorAll('[data-i]')].filter(n => +n.dataset.i >= grewFrom)
    .forEach(n => {
      const cell = cells[+n.dataset.i];
      const src = cell.arrive && boxes[cell.arrive];
      if (src) {
        const to = n.getBoundingClientRect();
        const dx = (src.left + src.width / 2) - (to.left + to.width / 2);
        const dy = (src.top + src.height / 2) - (to.top + to.height / 2);
        play(n, [
          { transform: `translate(${dx}px,${dy}px) scale(.6)`, opacity: 0, offset: 0 },
          { transform: `translate(${dx}px,${dy}px) scale(.6)`, opacity: 1, offset: .13 },
          { transform: `translate(${dx * .4}px,${dy * .4 + 16}px) scale(.82)`, opacity: 1, offset: .6 },
          { transform: 'none', opacity: 1, offset: 1 },
        ], { duration: 680, delay: at, easing: T.ease.arc, fill: 'backwards' });
        // nothing after the carry may appear until the carry has actually landed —
        // otherwise the chip reads "12 + = 14" for a beat, which is nonsense
        at += 620;
      } else {
        play(n, [{ opacity: 0, transform: 'translateX(-10px) scale(.78)' },
                 { opacity: 1, transform: 'none' }],
             { duration: 260, delay: at, easing: T.ease.ink, fill: 'backwards' });
        at += 110;
      }
    });
}
function splitBubble(split, partBoxes, el, box, keep, bubBox){
  const bub = $('bubble'), shell = bub.querySelector('.shell');
  // when the chip is kept (the D step keeps its trial rows on screen) the shell stays
  if (shell && !keep) play(shell, [{ opacity: 1 }, { opacity: 0 }],
                           { duration: 260, easing: T.ease.out, fill: 'forwards' });
  split.forEach(sp => {
    const span = bub.querySelector(`.bd[data-part="${sp.part}"]`);
    const from = partBoxes[sp.part], to = box[sp.to];
    if (!span || !from || !to) return;
    span.classList.toggle('to-carry', /carry/.test(el[sp.to].className));
    // On a kept chip the row has to keep reading true, so fly a CLONE and leave the
    // original behind, dimmed. Otherwise "6 x 7 = 42" becomes "x 7 = 42".
    let mover = span;
    if (keep && bubBox) {
      mover = span.cloneNode(true);
      mover.removeAttribute('data-part');
      Object.assign(mover.style, { position: 'absolute', margin: '0',
        left: (from.left - bubBox.left) + 'px', top: (from.top - bubBox.top) + 'px' });
      bub.appendChild(mover);
      span.style.opacity = '.4';
      after(T.split + 40, () => mover.remove());
    }
    const dx = (to.left + to.width / 2) - (from.left + from.width / 2);
    const dy = (to.top + to.height / 2) - (from.top + from.height / 2);
    const sc = to.height / from.height;
    play(mover, [
      { transform: 'none', opacity: 1, offset: 0 },
      { transform: `translate(${dx * .5}px,${dy * .5 - 14}px) scale(${(1 + sc) / 2})`,
        opacity: 1, offset: .55 },
      { transform: `translate(${dx}px,${dy}px) scale(${sc})`, opacity: 1, offset: .88 },
      { transform: `translate(${dx}px,${dy}px) scale(${sc})`, opacity: 0, offset: 1 },
    ], { duration: T.split, easing: T.ease.arc, fill: 'forwards' });
    // the real mark takes over exactly as the flying digit lands on it
    after(T.split * .86, () => {
      release(el[sp.to]);
      play(el[sp.to], [{ opacity: 0 }, { opacity: 1 }], { duration: 130, easing: T.ease.ink });
    });
  });
  if (!keep) after(T.split + 30, () => {
    $('bubble').classList.remove('up'); $('bubble').dataset.key = ''; });
}

function penTarget(b, wrap){
  return { x: b.left - wrap.left + b.width / 2 + 7, y: b.top - wrap.top + b.height - 7 };
}
function parkPen(pt, show){
  const pen = $('pen');
  if (!show || !pt) { pen.classList.remove('up'); return; }
  pen.style.transform = `translate(${pt.x - 2}px, ${pt.y - 2}px)`;
  pen.classList.add('up');
  penXY = pt;
}

function apply(instant){
  haltMotion();
  const a = A[ai], cur = a.steps[si];
  const back = si < prevSi;
  const board = $('board'), pen = $('pen');

  const show = new Set(), struck = new Set();
  a.steps.slice(0, si + 1).forEach(s => {
    (s.show || []).forEach(k => show.add(k));
    (s.strike || []).forEach(k => struck.add(k));
  });
  const flash = new Set(cur.flash || []);

  /* ---------- READ PHASE ----------
     Every measurement happens before any write. Interleaving them is what forces
     a synchronous layout, and it is invisible to every data check we have. */
  const el = {};
  board.querySelectorAll('[data-k]').forEach(n => { el[n.dataset.k] = n; });
  const wasOn = {};
  for (const k in el) wasOn[k] = el[k].classList.contains('on');
  const newly  = (cur.show || []).filter(k => el[k] && !wasOn[k]);
  const leaving = Object.keys(el).filter(k => wasOn[k] && !show.has(k));

  const flyFrom = {};
  (cur.fly || []).forEach(f => { flyFrom[f.k] = f.from; });
  const wrap = $('boardwrap').getBoundingClientRect();
  const boardRect = board.getBoundingClientRect();
  const box = {};
  const arriving = ((cur.bubble && cur.bubble.cells) || []).filter(c => c.arrive).map(c => c.arrive);
  new Set([...newly, ...Object.values(flyFrom), ...arriving]).forEach(k => {
    if (el[k]) box[k] = el[k].getBoundingClientRect();
  });
  // The bubble is already on screen from the compute beat, so its parts can be
  // measured here in the read phase. If it is NOT up (someone jumped straight to
  // this step), there is nothing to fly and the marks simply appear.
  const bub = $('bubble');
  const bubKey = chipKey(cur.bubble);
  const canSplit = !!(cur.split && !instant && !back && !REDUCED
                      && bub.classList.contains('up') && bub.dataset.key === bubKey);
  const partBoxes = {};
  let bubBox = null;
  if (canSplit) {
    bubBox = bub.getBoundingClientRect();
    bub.querySelectorAll('.bd[data-part]').forEach(n => {
      partBoxes[+n.dataset.part] = n.getBoundingClientRect(); });
  }

  /* ---------- WRITE PHASE ---------- */
  for (const k in el) {
    el[k].classList.toggle('on', show.has(k));
    el[k].classList.toggle('struck', struck.has(k));
    el[k].classList.remove('flash');
  }

  if (!REDUCED && !instant && !back) newly.forEach(k => holdHidden(el[k]));

  if (cur.bubble && !canSplit) {
    const fresh = showBubble(cur.bubble, wrap, boardRect);
    if (fresh && cur.bubble.grewFrom != null && !instant && !back && !REDUCED)
      growBubble(cur.bubble.cells, cur.bubble.grewFrom, box);
  } else if (!cur.bubble) { bub.classList.remove('up'); bub.dataset.key = ''; }

  const litFlash = () => flash.forEach(k => {
    if (el[k] && el[k].classList.contains('on')) el[k].classList.add('flash');
  });

  if (canSplit) {
    pen.classList.remove('up');
    splitBubble(cur.split, partBoxes, el, box, cur.keepChip, bubBox);
    after(T.split + 90, litFlash);
  } else if (REDUCED || instant) {
    litFlash();
    parkPen(newly.length ? penTarget(box[newly[0]], wrap) : penXY,
            !REDUCED && newly.length > 0 && si > 0);
  } else if (back) {
    // undoing is not writing — no pen, and the marks lift off quickly
    leaving.forEach(k => play(el[k], [{ opacity: 1, transform: 'none' },
                                      { opacity: 0, transform: 'scale(.88)' }],
                              { duration: T.inkOut, easing: T.ease.out }));
    litFlash();
    pen.classList.remove('up');
  } else if (!newly.length) {
    litFlash();
    pen.classList.remove('up');
  } else if (newly.length > 3 || si === 0) {
    // the problem being PLACED on the page, not written by hand — a quick sweep
    pen.classList.remove('up');
    newly.forEach((k, i) => after(i * T.sweep, () =>
      inkIn(el[k], box[flyFrom[k]], box[k])));
    after(newly.length * T.sweep + T.ink + 60, litFlash);
    penXY = null;
  } else {
    let cursor = penXY, t = 0;
    newly.forEach(k => {
      if (flyFrom[k]) {                 // arcs up from the digit that made it — no pen
        const at = t;
        after(at, () => inkIn(el[k], box[flyFrom[k]], box[k]));
        t = at + T.ink * T.chain;
        return;
      }
      const pt = penTarget(box[k], wrap);
      const from = cursor;
      const dist = from ? Math.hypot(pt.x - from.x, pt.y - from.y) : 0;
      const dur = from ? Math.min(T.travelMax, Math.max(T.travelMin, dist / T.pxPerMs))
                       : T.travelMin;
      const at = t;
      after(at, () => {
        pen.classList.add('up');
        play(pen, [
          { transform: `translate(${(from ? from.x : pt.x) - 2}px, ${(from ? from.y : pt.y) - 2}px)`,
            opacity: from ? 1 : 0 },
          { transform: `translate(${pt.x - 2}px, ${pt.y - 2}px)`, opacity: 1 },
        ], { duration: dur, easing: T.ease.travel, fill: 'forwards' });
      });
      // the mark lands only once the nib is there
      after(at + dur, () => inkIn(el[k], box[flyFrom[k]], box[k]));
      cursor = pt;
      t = at + dur + T.ink * T.chain;
    });
    penXY = cursor;
    after(t + 60, litFlash);
  }
  prevSi = si;

  $('badge').textContent = cur.label;
  $('say').innerHTML = cur.say;
  $('whyBox').innerHTML = cur.why
    ? `<div class="whybox"><span class="lbl">what it really means</span>${cur.why}</div>` : '';
  $('trapBox').innerHTML = cur.trap
    ? `<div class="trap"><span class="lbl">the trap</span>${cur.trap}</div>` : '';

  $('beats').querySelectorAll('.beat').forEach(b =>
    b.classList.toggle('now', b.dataset.beat === cur.beat));

  const mr = cur.modelRow, mc = cur.modelCell;
  $('model').querySelectorAll('.acell,.asum').forEach(node => {
    const lit = mr === 'all' || mc === 'all'
      || (mr !== undefined && mr !== null && +node.dataset.r === mr)
      || (mc !== undefined && mc !== null && node.classList.contains('acell') && +node.dataset.c === mc);
    node.classList.toggle('lit', !!lit);
  });
  $('model').querySelectorAll('tr[data-r]').forEach(tr =>
    tr.classList.toggle('lit', mr === 'all' || +tr.dataset.r === mr));

  [...$('dots').children].forEach((d, i) => {
    d.classList.toggle('done', i < si);
    d.classList.toggle('now', i === si);
  });
  $('back').disabled = si === 0;
  $('next').disabled = si === a.steps.length - 1;
  if (playing && si === a.steps.length - 1) stop();
}

function step(n){
  const a = A[ai];
  si = Math.max(0, Math.min(a.steps.length - 1, si + n));
  apply();
}
function tick(){
  const a = A[ai], mult = parseFloat($('speed').value);
  timer = setTimeout(() => {
    if (si >= a.steps.length - 1) { stop(); return; }
    si++; apply();
    if (playing) tick();
  }, (a.steps[si].dwell || 3) * 1000 * mult);
}
function start(){
  const a = A[ai];
  if (si >= a.steps.length - 1) si = 0;
  playing = true; $('play').textContent = '❚❚ Pause'; apply(); tick();
}
function stop(){
  playing = false; clearTimeout(timer); timer = null;
  $('play').textContent = '▶ Play';
}

$('play').onclick = () => playing ? stop() : start();
$('next').onclick = () => { stop(); step(1); };
$('back').onclick = () => { stop(); step(-1); };
$('restart').onclick = () => { stop(); si = 0; apply(); };
$('speed').onchange = () => { if (playing) { clearTimeout(timer); tick(); } };
let rAF = 0;
addEventListener('resize', () => {
  if (rAF) return;
  rAF = requestAnimationFrame(() => { rAF = 0; penXY = null; apply(true); });
});

addEventListener('keydown', e => {
  if (e.target.tagName === 'SELECT') return;
  if (e.key === ' ' || e.key === 'ArrowRight') { e.preventDefault(); stop(); step(1); }
  else if (e.key === 'ArrowLeft') { e.preventDefault(); stop(); step(-1); }
  else if (e.key.toLowerCase() === 'r') { stop(); si = 0; apply(); }
  else if (e.key.toLowerCase() === 'p') { playing ? stop() : start(); }
  else if ('1234'.includes(e.key)) pick(Math.min(A.length - 1, +e.key - 1));
});

pick(0);
</script>
"""


def main():
    anims = build()
    out = HTML.replace("__DATA__", json.dumps(anims, ensure_ascii=False))
    path = HERE / "index.html"
    path.write_text(out, encoding="utf-8")

    print(f"wrote {path}  ({len(out):,} bytes)")
    for a in anims:
        print(f"  {a['id']:<12} {a['kid']:<6} {len(a['steps']):>2} steps  "
              f"{a['cols']}×{a['rows']} grid  model={a['model']['kind']:<6} answer={a['answer']}")


if __name__ == "__main__":
    main()
