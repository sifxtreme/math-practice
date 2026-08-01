# Drill-method animations

Four step-through animations of the **written methods** the daily drill sheets require —
one per kid per operation. Open [`index.html`](index.html) in a browser; it is
self-contained (inline CSS + JS, no dependencies, no network), same as the worksheets.

```bash
open -a "Google Chrome" ~/code/experiments/personal/math-worksheets/animations/index.html
```

## Why this exists

The drills are bare arithmetic off math-drills.com, and a kid can get a 2-digit × 1-digit
right by holding it all in their head. That stops working at 3-digit × 1-digit, and it
never works for long division. **The method is the thing being taught, and the method is
"write it down."** Each animation reveals the problem one written mark at a time, so what
they see is the sequence of marks on the page — not a finished answer.

> ⚠️ **This is a deliberate exception to the paper-only rule.** [`AGENTS.md`](../AGENTS.md)
> § "Hard requirements" says *"Paper only. No Khan Academy, no app, no screen."* Asif asked
> for these animations on 2026-08-01 knowing that. They are a **teaching** aid for the
> 5-minute go-over-it slot in the daily session, not a replacement for the paper drill —
> watch one, then do the sheet. Don't take this as licence to move anything else on-screen.

## What's covered

| Tab | Kid | Method | Matching drill slug |
|---|---|---|---|
| 1 | kid1 | 3-digit × 1-digit, carrying (247 × 6) | `multiplication_0301` |
| 2 | kid1 | 2-digit ÷ 1-digit with remainder (67 ÷ 5) | `division_long_1dd2dd_r` |
| 3 | kid2 | 2-digit × 2-digit, two partial products (47 × 36) | `multiplication_0202` |
| 4 | kid2 | 4-digit ÷ 1-digit with remainder (4231 ÷ 7) | `division_long_1dd4dd_r` |

Slugs come from [`DRILLS.md`](../DRILLS.md) and match the current **STEP UP** pin.
The examples were chosen so the *facts* are easy and the *method* is the only load —
and so each one lands on its own trap:

- **kid1 ×** — multiply, **then** add the carry (adding first is the classic error)
- **kid1 ÷** — D·M·S·B in order; leftover must be smaller than the divisor
- **kid2 ×** — the **placeholder 0** in row 2, and crossing out the row-1 carries
- **kid2 ÷** — 4231 ÷ 7 = 604 R3, which hits *both* the "doesn't fit in the first digit"
  case and a **0 in the middle of the quotient**. Skip that 0 and 604 becomes 64.

Controls: `space` next · `←` back · `R` restart · `P` play/pause · `1`–`4` switch tab.
Play auto-advances with a per-step dwell; traps get a longer pause.

## Files

| File | What it is |
|---|---|
| `index.html` | **Generated.** The page. Do not hand-edit — `build_animations.py` overwrites it. |
| `specs.py` | The algorithm simulators. Every digit comes from running the real algorithm. |
| `build_animations.py` | Problem choices + narration + the HTML/CSS/JS template. **Edit here.** |
| `verify_animations.py` | Independent re-derivation. Must exit 0. |

```bash
python3 build_animations.py && python3 verify_animations.py
```

## Changing a worked example

Edit the `build=lambda: ...` line for that entry in `SPECS` (in `build_animations.py`),
rebuild, then **update the matching literals at the bottom of `verify_animations.py`** —
it asserts against numbers written there on purpose, so it can't be fooled by importing
the same wrong value it is checking.

## Verification

`verify_animations.py` runs **527 checks** and does not import the step builders. It pulls
the embedded JSON back out of `index.html` and checks it two ways:

1. **Arithmetic** — re-runs each algorithm from scratch and compares every carry,
   partial product, quotient digit, subtraction and leftover.
2. **Layout** — reads the digits back off the grid by row and column. A right answer in
   the wrong column is still wrong, and only this half catches it. Includes a
   **contiguity** check: digits of one number must occupy adjacent columns.

It was **mutation-tested** — 9 deliberate corruptions (flipped digits, a deleted
placeholder zero, a shifted quotient digit, a widened rule line, a misaligned subtraction,
narration that stops teaching the zero) were each confirmed to fail it. A check that
cannot fail isn't a check.

**The data checks are not sufficient on their own.** Two real bugs shipped past all 527 and
were caught only by rendering the page in headless Chromium:

- `.tok.carry2{opacity:.001}` — a stray rule that made kid2's **round-2 carry invisible**.
- The board's `sub` token class collided with the page's `.sub` subtitle class, which was
  declared later and won, rendering **every long-division subtraction row at 13px**.

Both were invisible to JSON inspection and obvious on screen. If you change the CSS,
re-render and look at it. The render harness asserts: no console errors, every revealed
mark actually visible, no two marks overlapping, uniform digit size, no horizontal
overflow at 1180px or 390px, and that Back really does un-write marks.
