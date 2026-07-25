# Kids' Math Word Problems

Printable, themed math word problems for the kids. Every sheet is 3 pages (kid1, kid2, answer key) and self-contained — open in a browser, Cmd+P → Save as PDF or print, or use `./print-worksheet.sh`.

## Files

| File | Theme | Type |
|------|-------|------|
| `worksheet.html` | Space (original template) | Math |
| `worksheet-worldcup.html` | 2026 World Cup | Math |
| `worksheet-worldcup-final.html` | World Cup, final week | Math |
| `worksheet-ocean.html` | Ocean / reef / research ship | Math |
| `worksheet-dinosaur.html` | Fossil dig | Math |
| `worksheet-worldcup-logic.html` | World Cup | Logic |
| `worksheet-egypt-logic.html` | Ancient Egypt | Logic |

## Layout (3 pages)

| Page | For | Grade | Content |
|------|-----|-------|---------|
| 1 | kid1 | 3rd grade | 5 word problems |
| 2 | kid2 | 4th grade | 5 word problems |
| 3 | (grown-ups) | Answer key | Worked steps for all 10 |

Names are pre-filled in the header. Each problem is a **compound / multi-step** problem (2+ operations) with a boxed work area, an answer line, and a "Did you know?" fact tied to its story.

## Skill levels

- **3rd grade (kid1):** multiply-then-subtract, multi-step grouping/division, add+subtract chains, elapsed time, division with remainder.
- **4th grade (kid2):** multi-step mult/div, multi-week savings, area + division, fractions (part eaten / part left), large multiplication + subtraction.

## Printing

**One command:** `./print-worksheet.sh <file.html>` — renders a clean 3-page PDF and prints the kids' sheets to the Brother. Add `--dry-run` to preview, `--both` to also print the answer key, `--printer NAME` for a different printer. (Chrome headless ignores the page margins and would otherwise overflow to 5 pages; the script renders a lightly-tightened, same-font copy that fits — your `.html` is untouched.)

**Manual (full-size layout):** open the `.html`, Cmd+P → **"Headers and footers" OFF**, **100% scale** → 3 pages.

## Editing

Everything is in one self-contained `worksheet.html` (inline CSS, no dependencies).

- Change a name: edit the `Name:` span in each sheet's `.meta` block, and the names inside the `.qtext` problems.
- Swap difficulty: edit the numbers in `.qtext` and the matching `.ans` steps on the answer-key page.
- Re-theme: replace the `.fact` blurbs and story wording; the math stays the same.
