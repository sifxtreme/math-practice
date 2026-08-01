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

**It was never a performance problem.** `perf-check.mjs` measured the first version at
`apply()` p95 of 0.8–1.4ms against an 8.3ms frame budget, zero long tasks, zero forced
reflows. Nothing was dropping frames. Throwing `will-change` and GPU hints at it would
have changed nothing anybody could see. What was wrong was **choreography**:

| defect | fix |
|---|---|
| The pen and the ink moved **at the same time**, so the mark appeared before the pen got there — the pen read as decoration floating near a digit, not the thing that made it | the pen **arrives first**, the mark appears under the nib second |
| Every mark in a step landed in **the same instant** | marks are **chained** — one after another, travel time scaled by distance |
| `transition: all` on tabs, dots, beats and area cells | explicit property lists; only `transform`/`opacity` on the board, so it stays on the compositor |
| A carry **faded in** where it landed | it **arcs** up from the digit that produced it, lofting through a raised mid-point |
| The pen travelled to carries too | carries loft in on their own; the pen only visits marks a hand actually makes |
| `.on` landed in the write phase but the animation was created later on a timer, so each mark was **painted at full opacity for ~95ms and then restarted from zero** — a double-take on every step | newly-revealed marks are held at `opacity:0` until their animation exists |

The state class `.on` is now **state only, with no transition** — all motion is driven
through the Web Animations API so each mark can be sequenced independently. Timings live
in one `T` table so the whole page shares a feel. Reads and writes are separated into
distinct phases inside `apply()`, so no write-then-read pair can force a synchronous layout.

Also: **brought-down digits drop** from the dividend, **D · M · S · B lights up** so the
four moves have a beat, the pen stays away during SET UP (that is the problem being *placed*,
not written), going **Back** un-inks quickly with no pen (undoing is not writing), and the
attention pulse waits until the ink has landed so the two do not compete.

All of it respects `prefers-reduced-motion` — the pen hides and the flights are skipped.
Window resize is rAF-throttled to one re-layout per frame.

Controls: `space` next · `←` back · `R` restart · `P` play/pause · `1`–`4` switch tab.
Play auto-advances with a per-step dwell; traps and `why` steps get a longer pause.

## Using it like a person

`user-check.mjs` exists because everything above can pass while the page is still
unusable. It mashes Next 25 times faster than key-repeat, mashes Back the same way,
switches tabs mid-draw, jumps around with the progress dots, lets autoplay run to the
end, and then does the whole thing again on a 390 x 844 phone.

**What it caught that nothing else could:** on a phone the board started **589px** down
and Next/Play sat at **1128px** — so you could not see the problem and advance it at the
same time, which is the entire interaction. Four stacked tabs alone ate 600px. Fixed with
a horizontally-scrolling tab strip and a control bar pinned to the bottom of the viewport:
board now starts at **322px**, controls at **732px**, both on screen at once.

It also found two things that were **not** bugs, which is worth recording so nobody
"fixes" them again:

- Sampling the board 260ms after a step change shows marks still at `opacity:0`. That is
  the chain working — they are queued behind the pen. At 1.5s every one is correct.
- "An animation was still running when the next step began" fires on every correct run,
  because `apply()` itself starts the next step's animations. The meaningful check is
  whether the autoplay gap exceeds the ~700ms drawing time. It does, by 3.5s+.

One finding is deliberately left alone: the math-drills link is 35px tall. It is an inline
link inside a sentence, not a button, and padding it to 44px would look wrong.

## Files

| File | What it is |
|---|---|
| `index.html` | **Generated.** The page. Do not hand-edit — `build_animations.py` overwrites it. |
| `specs.py` | The algorithm simulators. Every digit comes from running the real algorithm. |
| `build_animations.py` | Problem choices + narration + the HTML/CSS/JS template. **Edit here.** |
| `verify_animations.py` | Independent re-derivation of the arithmetic, layout and model. Must exit 0. |
| `render-check.mjs` | Headless-Chromium assertions the data cannot make, incl. choreography. Must exit 0. |
| `perf-check.mjs` | Measures `apply()` cost, forced layouts, long tasks. Must exit 0. |
| `user-check.mjs` | Drives it the way a person does. Must exit 0. |

```bash
python3 build_animations.py && python3 verify_animations.py \
  && node render-check.mjs && node perf-check.mjs && node user-check.mjs
```

All four must exit 0. `perf-check.mjs` enforces a budget: `apply()` p95 under 8.3ms (one
frame at 120Hz), max under 16.7ms, zero long tasks, zero forced-reflow violations. Treat
its absolute frame numbers as soft — headless timing is synthetic — and the before/after
delta as the real signal.

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

**Choreography is asserted, not eyeballed.** `render-check.mjs` steps the animation, samples
pen position and per-mark opacity every frame for 1.5s, and requires that (a) marks land at
least 30ms apart — no simultaneous reveal — and (b) each mark is inked while the pen is
within 45px of it, skipping carries because those arrive by themselves. Currently the first
mark inks at ~123ms with the pen 10px away and the carry lofts in ~150ms later.

Those assertions were mutation-tested too: firing the ink before the pen arrives, collapsing
the chain so marks land together, and restoring the flash-of-final-state bug were each
confirmed to fail the check.
