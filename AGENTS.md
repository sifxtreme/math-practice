# AGENTS.md — Kids' Math Worksheets

Recurring task: generate printable math word-problem worksheets for Asif's kids.

**Active plan: [`PRACTICE-PLAN-2026.md`](PRACTICE-PLAN-2026.md)** — daily practice Jul 25 → Aug 30, 2026 (school starts Aug 31). Check it for which sheet is due before generating a new one.

## 🔒 ONE DAY'S WORTH OF PAPER AT A TIME

**Set by Asif 2026-07-31. This one is enforced in code, not prose.**

> *"I'll only ask you for one day at a time. I will never ask you for more.
> Make sure you don't print out more than one day worth at a time — it's really bad."*

**Never print ahead. Never print a batch.** One day = word problems + logic + drills,
for **that day only**. That is the maximum, every time, with no exceptions to infer.

Asif will never ask for more than one day, so **a request for a batch is a
misreading of the request** — go back and re-read it.

[`day-guard.sh`](day-guard.sh) enforces it at the point where paper is actually
committed. Both print scripts source it, and it **refuses (exit 2) before `lp` is
reached**:

| Guard | Refuses |
|---|---|
| **A — never ahead** | Any sheet dated later than today |
| **B — one target day per calendar day** | A second, different day once you've printed for one today |
| **C — never a second copy** | A day whose paper already exists (printed on an earlier date) |

Several *files* on the same day are fine — that's what a full day is (word + logic +
two drills = four jobs), and Guard C only looks at paper printed on an *earlier* day,
so it never blocks file #2 of this morning's own set.

**Guard C is the one that matters most, and it was nearly missed.** A and B alone
would not have stopped either duplicate morning: Jul 29 and Jul 30 each printed a
single day, on that day, one day at a time — clean under both. Asif caught it
straight away (*"we already printed aug 1 and aug 2 i guess"*), which is exactly
right: the Jul 28 bulk run put paper on the shelf through Aug 2, so the next two
mornings were lined up to repeat the mistake. **"One day at a time" and "don't print
what already exists" are two different rules.** You need both.

The escape hatch is `--override-day-guard`, deliberately verbose, warns loudly, and
records the override in the ledger. A genuine replacement — a lost or ruined sheet —
goes through it, and should: that's a deliberate act, not a default.

`print-ledger.tsv` is the record of what paper exists, **tracked in git** (a
gitignored ledger starts empty on a fresh clone, and an empty ledger answers "no
paper exists" for every day — the wrong answer, silently). Rows before 2026-07-31 are
reconstructed from CUPS jobs 120–159; everything after is recorded live at print time.

**Run [`test-day-guard.sh`](test-day-guard.sh) after touching `day-guard.sh`** — 17
cases, no printer involved, real ledger untouched.

**Why code and not another paragraph:** this exact rule has now decayed three times
by living only in a doc — twice as the three-sheets-a-day rule (written here, silently
contradicted by the schedule table, and the table won), and once on 2026-07-28, when
a session printed all of Block 1 in a single run — **20 jobs, 10 days of sheets**
(CUPS jobs 132–151) — while this file already said one day at a time. Two mornings
then reprinted days that were already sitting in that stack. A doc cannot refuse. The
guard can.

**Generating ahead is still fine** — building a week of sheets costs nothing but
tokens and lets themes be planned. It is only *printing* ahead that is banned. Keep
the two verbs separate: `build_sheets.py` may run for a batch; `print-worksheet.sh`
runs for one day.

## The kids

| Name | Grade |
|------|-------|
| kid1 | 3rd |
| kid2 | 4th |

## Hard requirements (Asif's preferences — don't re-derive)

1. **Word problems**, not bare arithmetic. Every problem must be **compound / multi-step** (2+ operations) so it tests understanding.
2. **Muslim names** for the characters in the stories.
3. **Themed** for incidental learning. Each problem ends with a short **"Did you know?"** fact tied to its story. (First run = space.)
4. **HTML, self-contained** (inline CSS, no dependencies) so it prints cleanly and has **room to do the work** on the page — every problem needs a boxed work area + an answer line.
5. **3 pages, in this order:** page 1 = kid1 (3rd), page 2 = kid2 (4th), page 3 = **separate answer key** with worked steps for the grown-up.
6. **5 problems per kid** on a PRACTICE sheet — **4** on a TEACH sheet (the worked example eats one problem's worth of page; 5 overflows to a 2nd page).
7. **Paper only.** No Khan Academy, no app, no screen. The sheet has to carry the teaching itself — see **Two sheet types** below.

## A full day = THREE sheets per child

**Set 2026-07-26. Re-confirmed by Asif 2026-07-28 and made binding.** One sheet per
kid is not the unit of work. A complete day is **three sheets each**, and they
exercise different things:

| Type | File suffix | What it is | Format |
|---|---|---|---|
| **Math** | `worksheet-<theme>.html` | Compound word problems — the operation choice is the test | 5 per kid (4 on a TEACH sheet) |
| **Drill** | `worksheet-<op>-drill.html` — [`drill_gen.py`](drill_gen.py) | **Short, bare problems.** Speed and fluency, not comprehension. Timed | **built to a 5-minute budget**, count derived per skill |
| **Logic** | `worksheet-<theme>-logic.html` | Puzzles / reasoning — no arithmetic fluency required to start | 4–5 per kid |

Keep them as **three separate files, each still 3 pages** (kid1 · kid2 · key).
Do NOT merge into one 7-page file — `print-worksheet.sh` self-checks page count
against `.sheet` blocks and expects 3.

> ⚠️ **All three run EVERY day, and logic is the one that keeps getting dropped.**
> Twice now this rule has decayed the same way: it was written here, the schedule
> table in `PRACTICE-PLAN-2026.md` quietly disagreed with a `—`, and the schedule won
> — because the schedule is what gets read each morning. **A dash in that table is a
> bug.** The count drops for exactly one reason: **a break Asif designates** (right
> now, Aug 3–9 — nothing else). Every other day until school starts is a full three-
> sheet day. **Do not invent light days.** The plan invented two — a 15-minute
> test-prep week and an end-of-summer taper — and both were removed on 2026-07-28
> because Asif never asked for them.
>
> Before printing, count: did each kid get word problems, logic, AND a drill?

> ⚠️ **The "word problems, not bare arithmetic" rule below applies to the MATH
> sheet only.** A drill sheet is *supposed* to be bare arithmetic — that's the
> point of it. Don't apply requirement 1 to a drill sheet.

**Status:** logic sheets exist (`-egypt-logic`, `-worldcup-logic`,
`-astronomy-logic`, `-bridges-logic`). **Drills ARE generated, as of 2026-08-01** —
see [Generated drills](#generated-drills-drill_genpy) below. math-drills.com is now the
*fallback*, not the default, and [`DRILLS.md`](DRILLS.md) keeps its verified slugs for
skills the generator doesn't cover yet.

> This paragraph has been wrong twice, in opposite directions, and both times the fix
> was measurement. It first read "no drill sheet exists yet" while a forge monitor had
> been posting math-drills PDFs to Slack daily. It was then corrected to "drills are NOT
> generated and never were — don't write a `-drill.html`", which held until Asif asked
> for a generator on 2026-08-01. **If you are about to trust a "never" in this file,
> check the date on it.**

### Generated drills — [`drill_gen.py`](drill_gen.py)

```bash
python3 drill_gen.py --skill div --seed 20260801     # or --skill mul
python3 verify_drills.py                             # MUST exit 0 before printing
./print-worksheet.sh worksheet-division-drill.html --dry-run
```

Three things it does that a math-drills PDF does not:

1. **Sized to the clock, not the page.** [`drill_cost.py`](drill_cost.py) prices a
   problem by the number of written marks its method requires, and the count is
   whatever fits 5 minutes. math-drills ships 20 problems of 3-digit ÷ 1-digit; that
   is a **~16 minute sheet**, and kid2 was handed one on 2026-08-01. `--budget 600`
   for a ten-minute sheet; the counts re-derive themselves.
2. **No degenerate problems, by construction.** Divisors are 2–9. Multiplier digits
   are 2–9 — a 0 or 1 there spends a whole partial-product row on nothing. The
   *multiplicand* keeps its 0s and 1s, where they test place value. (These are two
   different rules; see `make_multiplication`'s docstring for why.)
3. **The grid forces the work**, including a **carry row** for single-digit
   multipliers — without it that sheet has one row to fill and forces nothing.

⚠️ **The time model rests on ONE measurement** — 49 problems of 3-digit subtraction in
13 minutes, May 2026, from `PRACTICE-PLAN-2026.md`. The mark counts are exact; the
seconds-per-mark is extrapolated from subtraction to division and multiplication.
**Time one real sheet and call `drill_cost.calibrate()`** — do not hand-adjust the
counts, or the model stops meaning anything. Until then, every count is a prediction.

> Worth knowing: `PRACTICE-PLAN-2026.md` § "Why this plan isn't fact drills" concluded from a May 2026 timing
> analysis that fact-fluency drills are *not* the bottleneck. Drills were added
> anyway on 2026-07-26 at Asif's direction — they buy speed, which is a separate
> goal from understanding. Not a contradiction, just don't expect them to move
> comprehension.

## Showing the work IS the assignment

**Set by Asif 2026-08-01, after kid2's division sheet came back with answers and no
written work at all.** His words: *"kid2 didn't show any of the work. This is something
we need to be more aware of."*

**The written work is the deliverable. The answer is a by-product.**

The reason is not neatness and not "so we can check it." It's that **a sheet with no
work is not a measurement.** With the steps missing:

- a right answer and a lucky guess are indistinguishable;
- a wrong answer doesn't say whether the *method* broke or a single subtraction slipped
  — which are opposite problems with opposite fixes;
- the sheet cannot feed the [pin rule](#when-to-move-the-pin-again), because "zero
  errors" is a claim the paper no longer supports.

An answer with no work is a **self-report**. The work is the state you read back.
Grade the method; a correct answer with nothing shown is not a pass on these sheets.

### What this changes when you pick or build a sheet

1. **Prefer a format that makes the work non-optional** for any method-critical skill —
   long division, multi-digit multiplication, anything with carries or bring-downs.
   Blank space is opt-*in*; a printed grid is opt-*out*. math-drills' **`..._grid_..._prompts_...`**
   family gives every multiply → subtract → bring-down step its own box and prints the
   `R` box at the bottom, so the process can't be skipped on the way to an answer. That
   is what kid2's 2026-08-01 redo used. See [`DRILLS.md`](DRILLS.md) § "Sheets that force the work".
2. **On a generated worksheet, the `.work` box is the same idea** and already exists —
   but a box can be left empty. If a skill keeps coming back unshown, move it to a
   grid sheet rather than asking again.
3. **A scaffolded format is not a step down.** The arithmetic is unchanged; only the
   written support differs. Don't treat it as a pin regression or "going easier" —
   it's the same skill, made legible.

> ⚠️ **This is a different failure from getting it wrong, and it is invisible in a
> score.** kid2's sheet could have been 20/20 and it would still have been a bad sheet.
> Check for *presence of work* before checking correctness — if the work isn't there,
> stop, because nothing downstream of that is trustworthy.

The [`animations/`](animations/README.md) **kid2 ÷** tab exists for exactly this gap:
it steps through the written method one mark at a time. Watch it, then do the paper.

## Method animations — [`animations/`](animations/README.md)

Built 2026-08-01 at Asif's request. **Multiplication and division are DONE** — the written
methods, revealed one mark at a time, with the trap for each called out where it happens.
Ready for the August block.

```bash
open -a "Google Chrome" ~/code/experiments/personal/math-worksheets/animations/index.html
```

**Type any problem into the box.** `358 x 7`, `4231 / 23` — it is generated in the page,
not baked in, so the problem a kid just got wrong can be animated on the spot. Four
worked tabs ship by default; every whole-number shape through 5th grade works
(N-digit × M-digit, multi-digit divisors). Decimals do **not** — `150 ÷ 4` gives `37 R2`,
not `37.5`, and that is a genuinely new method, not a bigger number.

⚠️ **A deliberate, narrow exception to "Paper only. No screen." above.** Asif asked for it
knowing the rule. It is a teaching aid for the 5-minute go-over-it slot — *watch one, then
do the paper drill.* It replaces nothing. **Do not generalize it** to worksheets or logic
sheets; that rule stands everywhere else.

### Before you claim a change works

Five commands, all must exit 0. Skipping any one of them has already let a real bug ship.

```bash
cd animations
python3 build_animations.py && python3 verify_animations.py \
  && python3 sweep-check.py && node equiv-check.mjs \
  && node render-check.mjs && node perf-check.mjs && node user-check.mjs
```

| check | what only it can catch |
|---|---|
| `verify_animations.py` | the maths, re-derived independently — never imports the generators |
| `sweep-check.py` | ~660 problems nobody picked. Caught `47 × 80` writing `00`, and `803 × 407` |
| `equiv-check.mjs` | `engine.js` (browser) vs `specs.py` (oracle) must agree **exactly** |
| `render-check.mjs` | it drew correctly. Caught an invisible carry and a 13px row |
| `user-check.mjs` | it is **usable**. Caught the phone layout putting Next 1128px below the board |

**`engine.js` and `specs.py` are the same algorithms in two languages, on purpose.**
Python is no longer the generator — it is the oracle. Change one, change the other, and
let `equiv-check` prove you did. It catches things nobody would ever diff: Python's
`round()` breaks ties to even, so `round(45,-1)` is 40 where `Math.round` says 50, which
silently changes a sentence in the narration.

> **Data checks are not enough — render it and look.** Three real bugs passed every data
> check and died only in headless Chromium: a stray `opacity:.001` hiding a carry, a CSS
> class collision shrinking every subtraction row to 13px, and the pen drawn *on top of*
> the digit it pointed at. If you touch the CSS, re-render.

### What to build next — and the trap

[`animations/CURRICULUM.md`](animations/CURRICULUM.md) maps all 45 fourth- and fifth-grade
standards onto the six drawing surfaces they need. Two exist; **22 of 45 need no new one**.

**Read the target board in [`PRACTICE-PLAN-2026.md`](PRACTICE-PLAN-2026.md) before
picking.** *Reachable on an existing surface* is an engineering fact, not a reason.
Add/subtract with regrouping is the cheapest thing on the list **and worthless here** —
both kids already run it at ~16 sec/problem, inside the fluency benchmark. Cheapness is
exactly what makes the wrong thing tempting.

### The rule the whole thing was built by

Asif found the same defect three times in one session, in three costumes: the `2` and `4`
appearing without the **42** they came from; a `14` with no visible **12 + 2**; a quotient
digit with no visible **hunt** that found it.

> **Before adding a method: list every number a solver holds mentally between one written
> mark and the next. Each one has to exist on screen, and linger under a keypress you
> control — not on a timer.**

That is the difference between an animation that demonstrates an algorithm and one that
teaches it. Every remaining topic has its own hidden object; the 2-digit divisor's is the
estimate, and it is the biggest one left.

## Two sheet types (applies to the MATH sheet)

The kids are not doing Khan or any app, so a sheet introducing a brand-new skill has to *teach* it, not just test it. Which type you write depends on whether the skill is new.

### TEACH sheet — first exposure to a skill

Opens with a **worked example**: one problem solved completely, every step labeled. Then the practice fades the scaffolding:

| # | Scaffolding |
|---|---|
| — | `HOW IT WORKS` box: worked example, all steps shown, ending in a **"The trap:"** line naming the mistake they're about to make |
| 1 | **Guided** — same problem shape, steps pre-labeled, kid fills the blanks |
| 2–3 | Independent |
| 4 | Independent, slightly harder |

Fade across the week: **day 1** = full worked example + guided problem · **day 2** = guided problem, no example · **day 3+** = plain PRACTICE sheet.

Do NOT write an explanation paragraph. Kids skip prose on a worksheet; they read a solved example. Show, don't tell.

The answer key on a TEACH sheet gets a **`Watch for:`** box per grade — the specific wrong answer to expect, and what to do when it shows up. That's for the adult, and it's the most useful part of the page.

`worksheet-teach-remainders-fractions.html` is the reference implementation. Two layout constraints it encodes, both learned the hard way (first render came out 5 pages):

- The `.teach` box uses `padding: 9px 12px;` and `margin-bottom: 4px;` **verbatim**, because those are the exact literal strings `print-worksheet.sh` rewrites when it tightens the page. Any other value and the box won't shrink with everything else.
- The guided problem has **no `.work` box** — its `.scaffold` steps sit in normal flow and *are* the work area. A `.work` box shrinks to 40px on print, which an absolutely-positioned scaffold would overflow, landing on top of the answer line.

### PRACTICE sheet — skill already introduced

Straight to 5 compound word problems, no example box. This is the original format (`worksheet.html` and every themed sheet).

## How to make a new set

1. Copy the closest existing sheet — `worksheet.html` for PRACTICE, `worksheet-teach-remainders-fractions.html` for TEACH. The layout/CSS is already dialed in.
2. Pick a new **theme** (and matching "Did you know?" facts). **Themes already used — do not repeat:** space · World Cup (×3) · ocean · dinosaur · Ancient Egypt · astronomy · human body · national parks · trains · volcano · Silk Road · bridges · weather · Mars rovers · honeybees · sailing ships · mountains & climbing · lighthouses · falconry · deserts & caravans · clocks & timekeeping · kites & flight. **Append yours here when you add a sheet.**

⚠️ **Theme supply is the binding constraint now**, not build time — three sheets a day burns two themes a day. Unspent ideas: rainforest · the Olympics · castles · animal migration · rivers · caves · bridges of the world *(distinct from `bridges`)* · printing & books · glass & mirrors · wells and water · silk & dye · maps and mapmaking.
3. Write 5 fresh compound problems per grade, using the skill spread in **Difficulty pin** below (that section is the live setting — read it, don't use the baseline unless it says to).
4. Regenerate the **answer key** page with worked steps, then **verify every answer programmatically** — a throwaway Python block asserting each expected value (`fractions.Fraction` for the fraction problems). Hand-checking is exactly where a tired adult repeats the very error the key exists to catch. Print the pass/fail table before you print paper.
5. Pre-fill each sheet's `Name:` field (kid1 / kid2). For the `Date:` field, **prefer `./print-worksheet.sh <file> --date "July 28, 2026"`** (or `--date today`) — it stamps the render only, leaves your source alone, and overrides a stale baked-in date, so **reprinting an old sheet never needs a hand-edit**. A blank date makes the sheet unfilable the moment it leaves the printer: you can't tell later which day it was for or whether it was done. The answer key has no `Date:` field and stays undated — don't add one. Baking the date into the HTML still works for a sheet written for one specific day.
6. Render it before handing it over: `./print-worksheet.sh <file> --dry-run` must report **3 pages**.

## Difficulty pin

**Current pin: STEP UP — set 2026-07-25.** Both kids cleared the baseline spread without trouble, so the next sheets move each of them one Khan Academy notch up. kid1 jumps the 3rd→4th boundary; kid2 jumps the 4th→5th boundary. Write to *this* list, not the baseline.

### kid1 (3rd) — pin to late-3rd / early-4th Khan

| # | Skill | Khan unit |
|---|-------|-----------|
| 1 | 2-digit and 3-digit **× 1-digit**, then subtract/add (no more single-digit multipliers) | [4th: Multiplication and division](https://www.khanacademy.org/math/cc-fourth-grade-math/cc-4th-mult-div-topic) |
| 2 | **2-digit ÷ 1-digit with a remainder** — and the problem must force him to *interpret* the remainder ("how many vans do they actually need?") | [4th: Division → remainders](https://www.khanacademy.org/math/cc-fourth-grade-math/division) |
| 3 | **Two-step word problems mixing all four operations** (the operation choice is the test) | [3rd: Arithmetic patterns and problem solving](https://www.khanacademy.org/math/cc-third-grade-math/arithmetic-patterns-and-problem-solving) |
| 4 | **Equivalent / comparing fractions** (½ vs 3/6, which is bigger) — new territory for him | [3rd: Equivalent fractions and comparing fractions](https://www.khanacademy.org/math/cc-third-grade-math/equivalent-fractions-and-comparing-fractions) |
| 5 | **Area or perimeter with a missing side** (given area + one side, find the other) | [3rd: Perimeter](https://www.khanacademy.org/math/cc-third-grade-math/3rd-perimeter) |

### kid2 (4th) — pin to late-4th / early-5th Khan

| # | Skill | Khan unit |
|---|-------|-----------|
| 1 | **2-digit × 2-digit** standard algorithm (not 2-digit × 1-digit) | [4th: Multiply by 2-digit numbers](https://www.khanacademy.org/math/cc-fourth-grade-math/multiplying-by-2-digit-numbers) |
| 2 | **Long division, 3–4 digit ÷ 1-digit, with remainder** | [4th: Division](https://www.khanacademy.org/math/cc-fourth-grade-math/division) |
| 3 | **Add/subtract fractions with UNLIKE denominators** — the real jump; needs a common denominator | [5th: Add and subtract fractions](https://www.khanacademy.org/math/cc-fifth-grade-math/imp-fractions-3) |
| 4 | **Decimals** — compare, and add/subtract tenths & hundredths (money is the natural story) | [4th: Decimals](https://www.khanacademy.org/math/cc-fourth-grade-math/imp-decimals) → [5th: Decimal place value](https://www.khanacademy.org/math/cc-fifth-grade-math/imp-place-value-and-decimals) |
| 5 | **Multi-step with a rate**: unit price or per-day rate → total → remainder/leftover | [5th: Multi-digit multiplication and division](https://www.khanacademy.org/math/cc-fifth-grade-math/multi-digit-multiplication-and-division) |

### When to move the pin again

Step up when a kid finishes a sheet **under time with zero errors twice in a row —
with the work shown**. Step back down a notch if either kid gets 2+ wrong on the same
skill across two sheets — that's the skill, not carelessness.

⚠️ **The "with the work shown" clause is load-bearing, added 2026-08-01.** Without it
this rule promotes a kid who never demonstrated the method — see
[Showing the work IS the assignment](#showing-the-work-is-the-assignment). A sheet with
no work is not a passing sheet and not a failing one; it is **no reading at all**, and
it cannot satisfy a criterion about errors. The next rung for kid2 is a **2-digit
divisor**, which [`DRILLS.md`](DRILLS.md) flags as a genuinely new act that 1-digit
fluency does not prepare him for. Promoting him there on unshown work is how that
lands badly.

### Baseline (the easier spread — only if the pin is too hot)

- **3rd (kid1):** multiply-then-subtract, multi-step grouping/division, add+subtract chains, elapsed time, division with remainder.
- **4th (kid2):** multi-step mult/div, multi-week money, area + division, fractions (part/whole), large multiplication + subtraction.

Sheets written to the baseline: `worksheet.html`, `worksheet-worldcup*.html`, `worksheet-ocean.html`, `worksheet-dinosaur.html`, `worksheet-egypt-logic.html`.

## Printing

> ⚠️ **"The plan says it's printed" is not evidence that it printed.** Block 1 was
> bulk-printed on 2026-07-28, and the schedule logged all ten days as ✅ — including
> days that hadn't happened. Two mornings then reprinted sheets that were already in
> the stack. `PRACTICE-PLAN-2026.md` now separates **📦 stack** (paper exists, printed
> ahead) from **✅ \<date\>** (that day's set actually went out that morning); a ✅ on a
> future row is a bug. To settle it, read the printer, not the plan:
> `grep "$(date +%d/%b/%Y)" /var/log/cups/access_log | grep -c Send-Document` — 0 means
> nothing went out today. And `lp` returning a request id only means CUPS *queued* it:
> confirm with `lpstat -o` (blank = drained) and check `Alerts:` in
> `lpstat -l -p Brother_HL_L2305_series` — an empty paper tray shows as
> `media-needed-error` and holds the job silently.

> 🔒 **Before any print, re-read [ONE DAY'S WORTH OF PAPER AT A TIME](#-one-days-worth-of-paper-at-a-time) above.** The scripts will refuse a batch or a future day on their own, but the guard is a backstop, not the plan.

**Easy path (one command) — `./print-worksheet.sh <file.html>`.** Renders the sheet to a clean 3-page PDF and prints it to the Brother (`Brother_HL_L2305_series`), **answer key included by default** since 2026-07-26. Flags: `--dry-run` (render only), `--date "July 28, 2026"` / `--date today` (stamp the Date field at print time), `--no-key` (kids' sheets only), `--key-only` (just the key), `--printer NAME`, `--override-day-guard` (break the one-day rule; loud, logged).

**Drills — `./print-drill.sh <drill.pdf> --for kid1 --date today`.** Drills are half the day's paper, and a bare `lp` bypasses every guard, so they get their own guarded entry point. Same flags for `--date`, `--printer`, `--dry-run`, `--override-day-guard`. It also checks the PDF is 2 pages, which catches the `qp` (questions-only, no key) link named in [`DRILLS.md`](DRILLS.md).

- `--dry-run` deliberately does **not** consult the day guard — nothing is printed, so nothing is spent. Use it freely to check page counts on any sheet, any date.

- ⚠️ **Don't "simplify" the `${RANGE_ARGS[@]+...}` guards near the bottom.** macOS ships bash 3.2, where `set -u` treats an *empty* array expansion as unbound and kills the script. That is the default path (no `--key-only`/`--no-key` ⇒ no page range ⇒ empty array), so a plain print died right before `lp` ran — after printing a reassuring `Rendered: 3 pages`. Fixed 2026-07-27.

- Why the script exists: Chrome's `--headless --print-to-pdf` **ignores `@page` margins** and forces ~1in margins, which overflows each sheet's last problem to a 2nd page (3 pages → 5). The script renders a lightly-tightened copy (smaller work boxes + spacing, **fonts unchanged**) that fits 3 pages at those margins. Your source `.html` is left untouched.
- It self-checks the page count against the number of `.sheet` blocks and WARNS if they don't match (a sign the worksheet's CSS drifted from this template — keep the `height: 78px` / `line-height: 1.4` / `padding: 9px 12px` values so the tighten-transform still matches).

**Manual path (full-size layout):** open the `.html`, Cmd+P → turn **"Headers and footers" OFF**, **100% scale** → 3 pages. Use this when you want the full 78px work boxes.

## Files

- `worksheet.html` — space theme (the original template).
- `worksheet-worldcup.html` — World Cup word problems.
- `worksheet-worldcup-final.html` — World Cup, final week.
- `worksheet-ocean.html` — ocean / reef word problems.
- `worksheet-dinosaur.html` — fossil dig word problems.
- `worksheet-worldcup-logic.html` — World Cup logic/puzzles.
- `worksheet-egypt-logic.html` — Ancient Egypt logic/puzzles.
- `worksheet-bridges-logic.html` — bridge logic/puzzles; kid2's #5 is the classic lantern crossing (answer 17, not 19).

**Generated by `build_sheets.py` (Jul 29 – Aug 2 batch, built 2026-07-28).** Content
lives in `specs_word.py` / `specs_logic.py`; `verify_sheets.py` re-derives every
answer independently and must exit 0 before any of them is printed.

| File | Day | Type |
|---|---|---|
| `worksheet-weather.html` | Jul 29 | word problems — teach, faded (guided #1, no example) |
| `worksheet-lighthouse-logic.html` | Jul 29 | logic |
| `worksheet-mars-rovers.html` | Jul 30 | word problems — practice |
| `worksheet-falconry-logic.html` | Jul 30 | logic |
| `worksheet-honeybees.html` | Jul 31 | word problems — practice |
| `worksheet-caravan-logic.html` | Jul 31 | logic — incl. the goat/grain/jackal crossing |
| `worksheet-sailing-ships.html` | Aug 1 | word problems — practice, **timed** |
| `worksheet-clocks-logic.html` | Aug 1 | logic — incl. the 4/7 hourglass |
| `worksheet-mountains-cumulative.html` | Aug 2 | word problems — **cumulative** |
| `worksheet-kites-logic-cumulative.html` | Aug 2 | logic — **cumulative** |

> **Editing one of these? Edit the spec, not the HTML.** Regenerating overwrites the
> `.html`. Re-run `python3 verify_sheets.py` after any change — it also asserts the
> CSS literals `print-worksheet.sh` rewrites are still present in every file, which
> is the failure a hand-edit causes and a page-count check catches only sometimes.
- `drill_gen.py` — generate division/multiplication drill sheets sized to a time budget.
- `drill_cost.py` — the time model: marks per problem → seconds → problems per sheet.
- `verify_drills.py` — audits the generated HTML independently of the generator. Mutation-tested.
- `private/RESULTS.md` — what came back marked, tagged SKILL / CARE / UNSHOWN. Feeds the
  pin rule. **Gitignored** — it is a per-child record of mistakes, the most sensitive
  thing here. See [`README.md`](README.md) § "Setting it up for your kids".
- `kids.example.json` — the names template. Copy to `kids.local.json` (gitignored).
- `print-worksheet.sh` — render a worksheet to a clean 3-page PDF and print it to the Brother.
- `print-drill.sh` — print a math-drills.com PDF through the same day guard.
- `day-guard.sh` — sourced by both print scripts. The one-day-at-a-time enforcement (guards A, B, C).
- `print-ledger.tsv` — tracked record of what paper exists, per target day. Guard C reads it.
- `test-day-guard.sh` — 17 regression cases for the guard. Run after any change to it.
- `animations/` — drill-method animations (one written mark at a time). See [`animations/README.md`](animations/README.md).
- `README.md` — human-facing overview.
- `AGENTS.md` — this file.
