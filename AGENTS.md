# AGENTS.md — Kids' Math Worksheets

Recurring task: generate printable math word-problem worksheets for Asif's kids.

**Active plan: [`PRACTICE-PLAN-2026.md`](PRACTICE-PLAN-2026.md)** — daily practice Jul 25 → Aug 30, 2026 (school starts Aug 31). Check it for which sheet is due before generating a new one.

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

## Two sheet types

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
2. Pick a new **theme** (and matching "Did you know?" facts).
3. Write 5 fresh compound problems per grade, using the skill spread in **Difficulty pin** below (that section is the live setting — read it, don't use the baseline unless it says to).
4. Regenerate the **answer key** page with worked steps — verify every answer by hand.
5. Pre-fill each sheet's `Name:` field (kid1 / kid2).
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

**Easy path (one command) — `./print-worksheet.sh <file.html>`.** Renders the sheet to a clean 3-page PDF and prints the kids' sheets to the Brother (`Brother_HL_L2305_series`). Flags: `--dry-run` (render only), `--both` (also print the answer-key page — skipped by default), `--printer NAME`.

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
- `print-worksheet.sh` — render a worksheet to a clean 3-page PDF and print it to the Brother.
- `README.md` — human-facing overview.
- `AGENTS.md` — this file.
