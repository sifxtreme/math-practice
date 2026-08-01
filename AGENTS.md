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
| **Drill** | *not generated —* [`DRILLS.md`](DRILLS.md) | **Short, bare problems.** Speed and fluency, not comprehension. Timed | a math-drills.com PDF per kid |
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
> school Prep week and an end-of-summer taper — and both were removed on 2026-07-28
> because Asif never asked for them.
>
> Before printing, count: did each kid get word problems, logic, AND a drill?

> ⚠️ **The "word problems, not bare arithmetic" rule below applies to the MATH
> sheet only.** A drill sheet is *supposed* to be bare arithmetic — that's the
> point of it. Don't apply requirement 1 to a drill sheet.

**Status:** logic sheets exist (`-egypt-logic`, `-worldcup-logic`,
`-astronomy-logic`, `-bridges-logic`). **Drills are NOT generated and never were** — don't write a
`-drill.html`. They come off math-drills.com, one verified PDF per kid per skill,
listed in [`DRILLS.md`](DRILLS.md); each PDF is 2 pages, questions then answer key.
(This line used to read "no drill sheet exists yet, that type still needs
building." It was wrong: a forge monitor had been posting math-drills PDFs to
Slack daily since well before that was written. The two files just never learned
about each other. That monitor was deleted 2026-07-27 — it drilled below the
difficulty pin — and `DRILLS.md` replaced it with per-kid sheets at the pin.)

> Worth knowing: `PRACTICE-PLAN-2026.md` § "Why this plan isn't fact drills" concluded from a May 2026 timing
> analysis that fact-fluency drills are *not* the bottleneck. Drills were added
> anyway on 2026-07-26 at Asif's direction — they buy speed, which is a separate
> goal from understanding. Not a contradiction, just don't expect them to move
> comprehension.

## Drill-method animations — [`animations/`](animations/README.md)

Added 2026-08-01 at Asif's request. Four step-through animations of the **written
methods** the drill sheets require — kid1 × and ÷, kid2 × and ÷ — each revealing a
worked example one written mark at a time, with the trap for that method called out
where it happens. Self-contained `index.html`, no dependencies.

```bash
open -a "Google Chrome" ~/code/experiments/personal/math-worksheets/animations/index.html
```

⚠️ **This is a deliberate, narrow exception to "Paper only. No screen." in the Hard
requirements above.** Asif asked for it knowing the rule. It is a teaching aid for the
5-minute go-over-it slot in the daily session — *watch one, then do the paper drill*.
It replaces nothing. **Do not generalize it** into moving worksheets, logic sheets, or
anything else on-screen; that rule still stands everywhere else.

Same discipline as the sheets: content is generated (`build_animations.py` + `specs.py`),
`index.html` is overwritten on every build, and `verify_animations.py` re-derives every
digit independently and must exit 0. **It is mutation-tested** — 9 deliberate corruptions
were each confirmed to fail it.

> **Data checks are not enough here — render it.** Two real bugs passed all 527 data
> checks and were caught only in headless Chromium: a stray `opacity:.001` that made a
> carry digit invisible, and a CSS class collision (`.sub` as both a board token class and
> a page subtitle class) that shrank every long-division subtraction row to 13px. If you
> touch the CSS, re-render and look at it.

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

Step up when a kid finishes a sheet **under time with zero errors twice in a row**. Step back down a notch if either kid gets 2+ wrong on the same skill across two sheets — that's the skill, not carelessness.

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
- `print-worksheet.sh` — render a worksheet to a clean 3-page PDF and print it to the Brother.
- `print-drill.sh` — print a math-drills.com PDF through the same day guard.
- `day-guard.sh` — sourced by both print scripts. The one-day-at-a-time enforcement (guards A, B, C).
- `print-ledger.tsv` — tracked record of what paper exists, per target day. Guard C reads it.
- `test-day-guard.sh` — 17 regression cases for the guard. Run after any change to it.
- `animations/` — drill-method animations (one written mark at a time). See [`animations/README.md`](animations/README.md).
- `README.md` — human-facing overview.
- `AGENTS.md` — this file.
