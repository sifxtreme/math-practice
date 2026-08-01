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

Every step carries three things, and the middle one is the whole point of the second pass:

| | |
|---|---|
| **say** | what to do — the instruction, the mark you make |
| **why** | what that mark *means* in place value. **That carry is not a 4, it is 40. That 6 in the quotient is not a 6, it is 600. The 42 you write under 4231 is really 4200.** |
| **trap** | the specific wrong answer waiting at this step |

A kid who can run the algorithm but cannot say the **why** sentences is executing, not
understanding — and that is exactly the kid who falls apart when the numbers get bigger.

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

## The model — the same sum drawn a second way

Under the board, every animation shows the calculation again **without the shorthand**,
highlighted in sync with the current step:

- **Multiplication → an area rectangle**, sliced by place value. For 47 × 36 the top strip
  is `30 × 47 = 1410` and the bottom is `6 × 47 = 282` — which *are* the two written rows.
  This is what gives the placeholder zero a reason: every multiple of 30 ends in 0, so row
  2 has to. You are not adding a magic zero, you are writing where the number actually is.
- **Division → a partial-quotients ladder.** `4231 − 4200 (600×7) → 31 − 0 (0×7) → 31 − 28
  (4×7) → 3`, totalling `600 + 0 + 4 = 604`. This is the clearest statement of why the
  middle zero matters: without it you are claiming `60 + 4`.

Common Core **4.NBT.B.5** asks for exactly this — *"illustrate and explain the calculation
by using ... rectangular arrays and/or area models"* — and v1 had none of it.

## The motion

- **A pen leads every mark.** It travels to the spot *before* the digit appears, so writing
  *order* is visible, not just the result. Its nib lands on the mark; the body hangs
  down-right so it never covers what it just wrote.
- **Carries fly.** A carry does not fade in where it lands — it travels from the digit that
  produced it up to its shelf. That is the one bit of motion that carries real meaning.
- **Brought-down digits drop** from the dividend.
- **D · M · S · B lights up** on the division animations so the four moves have a beat.

All of it respects `prefers-reduced-motion` — the pen hides and the flights are skipped.

Controls: `space` next · `←` back · `R` restart · `P` play/pause · `1`–`4` switch tab.
Play auto-advances with a per-step dwell; traps and `why` steps get a longer pause.

## Files

| File | What it is |
|---|---|
| `index.html` | **Generated.** The page. Do not hand-edit — `build_animations.py` overwrites it. |
| `specs.py` | The algorithm simulators. Every digit comes from running the real algorithm. |
| `build_animations.py` | Problem choices + narration + the HTML/CSS/JS template. **Edit here.** |
| `verify_animations.py` | Independent re-derivation of the arithmetic, layout and model. Must exit 0. |
| `render-check.mjs` | Headless-Chromium assertions the data cannot make. Must exit 0. |

```bash
python3 build_animations.py && python3 verify_animations.py
```

## Changing a worked example

Edit the `build=lambda: ...` line for that entry in `SPECS` (in `build_animations.py`),
rebuild, then **update the matching literals at the bottom of `verify_animations.py`** —
it asserts against numbers written there on purpose, so it can't be fooled by importing
the same wrong value it is checking.

## Verification

`verify_animations.py` runs **655 checks** and does not import the step builders. It pulls
the embedded JSON back out of `index.html` and checks it three ways:

1. **Arithmetic** — re-runs each algorithm from scratch and compares every carry,
   partial product, quotient digit, subtraction and leftover.
2. **Layout** — reads the digits back off the grid by row and column. A right answer in
   the wrong column is still wrong, and only this half catches it. Includes a
   **contiguity** check: digits of one number must occupy adjacent columns.
3. **The model** — checked against the two input numbers directly, *never* against the
   board it exists to corroborate. Area columns must sum to the top number and rows to the
   bottom; every band must be a clean place value (`200`, `40`, `7` — never `47`); every
   cell must be its row × its column; the strips must *be* the two written partial
   products. For the ladder: every partial quotient a clean place value, each product
   `q × divisor`, the leftover chain intact, and the partial quotients summing to the
   real quotient. Plus: every step must have a `why`, and every model reference in range.

It was **mutation-tested twice** — 9 corruptions against the board checks (flipped digits,
a deleted placeholder zero, a shifted quotient digit, a widened rule line, a misaligned
subtraction, narration that stops teaching the zero) and 7 against the model checks (a
wrong area cell, a band that isn't a place value, rowSums that stop matching the partial
products, a broken partial quotient, a broken leftover chain, a step that loses its `why`,
a model reference off the end). All 16 were confirmed to fail it. A check that cannot fail
isn't a check.

**The data checks are not sufficient on their own.** Three real bugs passed every one of
them and were caught only by rendering the page in headless Chromium:

- `.tok.carry2{opacity:.001}` — a stray rule that made kid2's **round-2 carry invisible**.
- The board's `sub` token class collided with the page's `.sub` subtitle class, which was
  declared later and won, rendering **every long-division subtraction row at 13px**.
- (v2) The pen was drawn **on top of the digit it was pointing at** — present, correct
  position, and useless. Nothing in the data could have told you.

All three were invisible to JSON inspection and obvious on screen. If you change the CSS,
re-render and look at it. `render-check.mjs` now asserts: no console errors, every revealed
mark actually visible, no two marks overlapping, uniform digit size, no horizontal overflow
at 1180px or 390px, that Back really does un-write marks, and that **the pen is visible,
its nib within 40px of the mark it just wrote, and covering less than 30% of it**. Those
pen assertions were mutation-tested too.
