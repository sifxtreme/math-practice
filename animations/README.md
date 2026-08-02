# Drill-method animations

Four step-through animations of the **written methods** the daily drill sheets require —
one per kid per operation. Open [`index.html`](index.html) in a browser; it is
self-contained (inline CSS + JS, no dependencies, no network), same as the worksheets.

```bash
open -a "Google Chrome" ~/code/experiments/personal/math-worksheets/animations/index.html
```

**Chrome is the only target.** Confirmed by Asif 2026-08-01: *"we will always just use
chrome for this."* Every check here runs headless Chromium, which is therefore the real
browser and not a proxy for one — don't spend effort on Safari or Firefox quirks, and
don't caveat results with them.

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

## The rule this thing was built by

Asif found the same defect three times in one session, in three costumes:

| what was shown | what was missing |
|---|---|
| `2` and `4` appear in two places | the **42** they came out of |
| `6`, `2`, a carry, then `14` | the **12** and the **+ 2** |
| "how many 7s fit in 42? **Six**" | the **hunt** that found the six |

Each time the animation showed a step's *result* and skipped the object the kid actually
needs to hold in their head. Each time it looked fine until someone asked "but where did
that come from?"

**So: before adding any method here, list every number a solver holds mentally between one
written mark and the next. Each one of those has to exist on screen, and it has to linger
under a keypress you control — not on a timer.** That is the entire difference between an
animation that demonstrates an algorithm and one that teaches it.

The three methods the ladder still wants — 2-digit divisors, 3-digit × 3-digit, decimal
quotients — each have their own hidden object. The 2-digit divisor's is the estimate
("how many 23s in 147?" is a *guess* you then check), and it is the biggest one in the set.

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

## Two beats per digit: *what is it?* then *where does it go?*

Asked for by Asif 2026-08-01: *"when we multiply 7×6 that equals 42, we should linger a
bit there, and then show where the 2 goes and where the 4 goes."*

He was right, and the old version was hiding the most important object on the page. It
computed 42 and wrote the `2` and the `4` into two places **in the same instant** — so the
42 never existed. A kid watching it sees two digits appear from nowhere and has no reason
to believe they are halves of the same thing.

He came back to it the same day, pointing at `6 × 2` with a carry of 2 waiting on the
shelf: *"we are just showing 3 numbers then 14 — how did the 14 happen? that's necessary
for the kids to understand."* Same gap, one level down. The chip jumped straight to the
total, so the `12` never existed and neither did the `+ 2`.

So each digit of a multiplication is now **two steps — three when a carry is coming in**:

| beat | what happens |
|---|---|
| **`6 × 2`** | the product appears as a **whole number in a chip** beside the board, and stops there. Nothing else moves. You can talk about it, then press space. |
| **`+ THE CARRY`** *(only when there is one)* | the chip grows into a written expression, in order: `12` → `12 +` → the carry **flies down off the shelf** into the gap → `12 + 2` → `=` → `14`. Nothing appears out of sequence; the `= 14` waits until the carry has landed. |
| **`WHERE IT GOES`** | the chip's outline fades and the digits of the total **fly apart** — the `4` down-left into its column, the `1` up-left onto the shelf |

The chip is an expression, not a number, and only the cells of the **total** can fly out.
That is why `verify_animations.py` can assert the chip's own arithmetic is true: it reads
`12` and `2` and `14` straight off the cells and checks `12 + 2 == 14`, and separately
that the `2` it pulled in is the digit actually sitting on `cy1`.

Two details that matter:

- **The `4` is already orange inside the chip**, before it moves. It looks like a carry
  while it is still part of 42, so there is no colour jump when it lands — and you can
  point at it and say "that one's leaving" before it does.
- The directions are real. The chip sits to the **right** of the board precisely so the
  ones digit travels **down** and the carry travels **up**, matching what you say out loud.
  The board reserves a gutter for it and sits left of centre; without that the chip falls
  back to sitting *above* the board, and then the carry flies **down** to its shelf — the
  opposite of what you just said. On a phone there is genuinely no room, so it does sit
  above; the carry's travel there is 14px, which reads as sideways rather than down.
- One reserved width for the whole animation, so the chip appears in **the same spot every
  time** rather than hopping as the expression grows.

The `why` line under it does the place-value half: *"Split it by size: 42 = 2 + 40. The 2
fits in the ones column. The 40 does not — so it moves one column left, to where 40
belongs. **That is all a carry is.**"*

This doubles the step count on the multiplication tabs (kid1 5 → 10, kid2 11 → 17).
That is the point — the linger is under your thumb, not on a timer.

### Division has the same gap, and it is worse

*"did you do this for division and the other things too?"* — no, and checking rather than
guessing showed division had **zero** chips against multiplication's eight.

The hidden step in long division is not a carry, it is **the search**. When the narration
says *"how many 7s fit in 42? Six"* — where did the six come from? A kid does not know six.
They have to hunt for it, and that hunt is the thing they get wrong most often. It was
stated in words and never shown.

So every `D` now gets a **`TRY THEM`** beat first, with the candidates laid out and judged:

```
5 × 7 = 35    too small
6 × 7 = 42    fits          <- highlighted
7 × 7 = 49    too big
```

**"Too small" is the row that matters** and the one teaching usually skips. A digit is too
small when what is *left over* would still hold another divisor — you could have fitted one
more in. That is the `why` line, and it is the rule that stops a kid writing 5 and then
getting a leftover of 7.

Then the `D` beat **flies the chosen digit up** out of the winning row into the quotient, so
the answer has a visible source. The row keeps reading `6 × 7 = 42` with the 6 dimmed where
it left from — a clone flies, the original stays, or the row would read `× 7 = 42`.

Steps: kid1 ÷ 10 → 12, kid2 ÷ 15 → 18.

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

### Speed moves the motion, not just the pauses

Hafsa, 2026-08-01: *slowing down the animation when you move the numbers around would be
helpful.* She was pointing at a real flaw — the **Speed** control only stretched the gap
*between* steps. The digits still flew at exactly the same rate, so "Slow" did not slow
down the one thing you actually watch.

Every animated duration now goes through `dur()`, which scales by the Speed setting.
Measured, following the carry as it travels to its shelf:

| Speed | carry finishes travelling |
|---|---|
| Quick (×0.7) | 798 ms |
| Normal (×1) | 1140 ms |
| Slow (×1.6) | 1811 ms |

The **defaults for movement also got slower** — a split went 820 → 1250 ms, an arc
610 → 900 ms, the pen travels at 0.48 px/ms instead of 0.62. Marks *appearing* were left
alone; the note was about following a number as it moves, not about how fast ink lands.

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

## Type any problem — the numbers are not baked in

**The generator runs in the page.** Type `358 x 7` or `4231 / 23` into the box above the
tabs and it is animated on the spot — narration, chip, area model, you-try problems and
all. Nothing was baked in for it.

That is the whole reason [`engine.js`](engine.js) exists. `problems.json` made the problem
set *data*, but the data was still compiled into `index.html` at build time — to change a
number you rebuilt. A baked set can only ever answer problems someone chose in advance,
and **the one a kid just got wrong is never in it.**

Two rules the input enforces, both from real decisions rather than taste:

- **Never ÷ 1 or × 1.** Asif 2026-08-01: *"a waste of time for the kid."*
- **No `5 ÷ 90`** — a division with no whole part is not a long-division problem.

### engine.js is a port of specs.py, and that is deliberate

[`equiv-check.mjs`](equiv-check.mjs) runs **both implementations over hundreds of problems
and requires the emitted step data to be deep-equal**:

```
$ node equiv-check.mjs --n 40
14 shapes · 560 problems compared
engine.js and specs.py agree exactly
```

Python stops being the generator and becomes the **oracle** — a second implementation, in
another language, that has to agree. The independence `verify_animations.py` always
claimed is now structural instead of a discipline: **a bug has to be made twice, the same
way, in two languages, to survive.**

Four mutations confirmed it can fail, and one is the reason it exists: **Python's `round()`
breaks ties to even**, so `round(45, -1)` is `40` where `Math.round` says `50`. Swapping in
naive rounding is caught on `45 × 7` — *"45 is about 40"* vs *"about 50"*. A silently wrong
sentence in narration nobody diffs.

**If you change one, change the other, and let `equiv-check` tell you that you did.**

## Adding a permanent tab — or changing the shipped numbers

**Everything is in [`problems.json`](problems.json). One entry, then rebuild. No code.**

```json
{ "id": "kid1-mult-b", "kid": "kid1", "theme": "teal",
  "kind": "mult", "x": 358, "y": 7,
  "drill": { "category": "multiplication2", "slug": "multiplication_0301" },
  "standard": "4.NBT.B.5" }
```

`x` and `y` are the entire input. **Everything else is derived from their shape** by
[`describe.py`](describe.py): the title, the skill line, the rule card, the traps, the
area model, and three you-try problems that hit the *same traps* as the worked example
(same digit counts, and a carry / a remainder / an interior zero if the example has one).
Nothing is written per problem, because prose written per problem is what stops you adding
one.

Two constraints the picker enforces, both from real rules rather than taste:

- **Never divide by 1.** Asif 2026-08-01: *"a waste of time for the kid."* `DRILLS.md`
  measured 7 of 10 math-drills variants leaking divide-by-1 problems.
- **You-try problems must be the same kind of hard**, not just the same size. A you-try
  that comes out even when the worked example has a remainder is practising a different
  thing.

**`problems.json` is read by the builder AND the verifier, deliberately.** If the verifier
took the problem statement out of `index.html`, it would only ever prove the file is
self-consistent — a `247` corrupted to `248` would verify happily against its own corrupted
answer. Two sources, or no check.

## Is it actually generic? — [`sweep-check.py`](sweep-check.py)

Working for the four problems we ship says nothing about whether `247 × 6` works because
the code is right or because it is the number the code was tuned against. `sweep-check.py`
runs the **same verification over hundreds of problems nobody picked by hand**:

```
$ python3 sweep-check.py --n 60
2-digit x 1-digit    60 tried    8000 checks  ✓ all 60 pass
3-digit x 1-digit    60 tried   10490 checks  ✓ all 60 pass
4-digit x 1-digit    60 tried   13033 checks  ✓ all 60 pass
2-digit x 2-digit    60 tried   15389 checks  ✓ all 60 pass
3-digit x 2-digit    60 tried   20060 checks  ✓ all 60 pass
3-digit x 3-digit    60 tried   28444 checks  ✓ all 60 pass
2-digit / 1-digit    60 tried   11274 checks  ✓ all 60 pass
3-digit / 1-digit    60 tried   15907 checks  ✓ all 60 pass
4-digit / 1-digit    60 tried   20503 checks  ✓ all 60 pass
3-digit / 2-digit    60 tried   13244 checks  ✓ all 60 pass
4-digit / 2-digit    60 tried   18199 checks  ✓ all 60 pass

174,543 checks over 11 shapes
```

**Every shape on the drill ladder now works**, including the three that were "🆕 new
method" rungs in [`DRILLS.md`](../DRILLS.md). Turning one on is one entry in
`problems.json` — they are left off the shipped page on purpose, because the kids' current
rung is more variants of what they already have, not a harder slug.

### What the sweep caught that the four shipped problems never could

| problem | bug |
|---|---|
| `47 × 80` | multiplier ending in 0 wrote row 1 as `00` — one zero per column, not the number 0 |
| `803 × 407` | an **interior** zero in the multiplier: that row is its placeholders *plus* a zero product |

Both were correct-looking and permanently invisible to a fixed set of examples. That is
the whole argument for the sweep.

### How the two hard shapes were unblocked

- **Multi-digit divisor.** The gutter was one column wide because the divisor was one
  digit — `dcol = i + 2` everywhere. It is now `i + 1 + ndiv`, the divisor renders one
  token per digit, and the bracket and remainder label move with it. The `TOO SMALL` loop
  already handled taking more than one extra digit (`147 ÷ 23` needs two), so the
  algorithm itself did not change — only the layout did.
- **N-round multiplication.** `mult_two_by_two` now does one round per digit of the
  multiplier, each row starting with one more placeholder zero than the row above. The
  area model grows to N strips. `473 × 268` gives `3784 + 28380 + 94600 = 126764` with the
  zero staircase visible in the row it belongs to.


## Files

| File | What it is |
|---|---|
| `index.html` | **Generated.** The page. Do not hand-edit — `build_animations.py` overwrites it. |
| `problems.json` | **The problem set.** One entry per animation. Edit this, not code. |
| `describe.py` | Derives title / skill / rules / you-try from the shape of (kind, x, y). |
| `engine.js` | **The simulators, in the browser.** Inlined into the page; powers typed-in problems. |
| `equiv-check.mjs` | Requires `engine.js` and `specs.py` to agree exactly. Must exit 0. |
| `specs.py` | The Python **oracle** — the second implementation. Every digit comes from running the real algorithm. |
| `build_animations.py` | Problem choices + narration + the HTML/CSS/JS template. **Edit here.** |
| `verify_animations.py` | Independent re-derivation of the arithmetic, layout and model. Must exit 0. |
| `render-check.mjs` | Headless-Chromium assertions the data cannot make, incl. choreography. Must exit 0. |
| `perf-check.mjs` | Measures `apply()` cost, forced layouts, long tasks. Must exit 0. |
| `sweep-check.py` | Runs the checks over hundreds of unseen problems. Must exit 0. |
| `user-check.mjs` | Drives it the way a person does. Must exit 0. |

```bash
python3 build_animations.py && python3 verify_animations.py \
  && python3 sweep-check.py && node render-check.mjs && node perf-check.mjs \
  && node user-check.mjs
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
4. **The trial ladder** — every verdict re-derived from scratch (`big` if the product
   exceeds what you are dividing, `small` if the leftover would still hold another
   divisor, else `fits`). A wrong verdict here teaches the wrong *rule*, which is worse
   than a wrong answer. Plus: the row marked as fitting must carry the actual quotient
   digit, a `fits` row must not exist where the answer is 0, the chip must say it is
   dividing the number it is really dividing, and the digit that flies up must be the
   digit that lands.
5. **The product chip** — the sequence of chips must be the real running products,
   re-derived here; every chip digit must be accounted for by the split; and **the digit
   that flies must be the digit that lands** (chip digit vs. the text of the token it flies
   to). A chip that says 42 while a 3 lands on the board is the exact failure this catches.

It was **mutation-tested twice** — 9 corruptions against the board checks (flipped digits,
a deleted placeholder zero, a shifted quotient digit, a widened rule line, a misaligned
subtraction, narration that stops teaching the zero) and 7 against the model checks (a
wrong area cell, a band that isn't a place value, rowSums that stop matching the partial
products, a broken partial quotient, a broken leftover chain, a step that loses its `why`,
a model reference off the end) and 4 against the chip checks (a flying digit that does not
match the digit it lands on, a chip digit that goes nowhere, a chip showing the wrong
product, a split aimed at a mark that does not exist). All 20 were confirmed to fail it. A check that cannot fail
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
