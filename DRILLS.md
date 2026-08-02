# Drill sheets

> ## ⚠️ We generate our own now — 2026-08-01
>
> **[`drill_gen.py`](drill_gen.py) is the default source for division and
> multiplication drills.** math-drills.com is the *fallback*, for skills the generator
> doesn't cover yet. Everything below still applies to that fallback, and the verified
> slug tables are still correct — but check the generator first.
>
> Why the switch, in one line each:
>
> | | math-drills.com | `drill_gen.py` |
> |---|---|---|
> | Sheet length | fills a page — 20 problems of 3-digit ÷ 1-digit is a **~16 min sheet** | derived from a **5-minute budget** |
> | Degenerate problems | ÷1 in **7 of 10** variants; ×0 and ×1 ship too | impossible by construction |
> | Showing the work | only the `_grid_..._prompts_` family | always, incl. a **carry row** for 1-digit multipliers |
> | Variants | 10 per slug, and we track which are spent | unbounded — it's a seed |
>
> `python3 drill_gen.py --skill mul && python3 verify_drills.py`

## The fallback bank — math-drills.com

The **drill** leg of the three-sheets-a-day rule (see [`AGENTS.md`](AGENTS.md) § "A full day = THREE sheets per child"). Drills are bare arithmetic on purpose — speed and fluency, not comprehension. Don't apply the word-problem rule to them.

Nothing here is generated. These are free printable PDFs off math-drills.com, picked to match the current **STEP UP** difficulty pin.

## How the URLs work

```
https://math-drills.com/<category>/<slug>_00N.php     ← N = 1..10, the A–J variants
```

Each page carries **two** PDF links. Take the one **without** `qp` in the filename:

| PDF | Pages | Use |
|---|---|---|
| `..._001.<digits>.pdf` | **2 — questions, then the answer key** | ✅ this one |
| `..._001qp.<digits>.pdf` | 1 — questions only | skip; you lose the key |

So one link = the kid's page *and* the grown-up's key, which is the same deal the generated sheets give you. Print page 1, keep page 2.

## Printing a drill

**Use [`print-drill.sh`](print-drill.sh), not a bare `lp`.**

```bash
./print-drill.sh ~/Downloads/multiplication_0301_001.pdf --for kid1 --date today
```

It routes the drill through the same **one-day-at-a-time guard** as the generated sheets ([`day-guard.sh`](day-guard.sh)): no future-dated paper, and no second target day once you've printed for one today. Drills were **half** the Jul 28 bulk run — 10 of its 20 jobs — and they went out via a bare `lp`, which no guard can see. That's the hole this closes. It also flags a PDF that isn't 2 pages, which is how you catch grabbing the `qp` link by mistake.

## The sheets — verified 2026-07-27

Every row below was checked live: page resolves, non-`qp` PDF exists and is 2 pages, 10 variants each. A deliberately-bogus slug was checked alongside them and failed, so the check could actually fail.

### kid1 (3rd → 4th)

| Skill | Category | Slug |
|---|---|---|
| 2-digit × 1-digit | `multiplication2` | `multiplication_0201` |
| 3-digit × 1-digit | `multiplication2` | `multiplication_0301` |
| **2-digit ÷ 1-digit with remainder** | `division` | `division_long_1dd2dd_r` |

### kid2 (4th → 5th)

| Skill | Category | Slug |
|---|---|---|
| **2-digit × 2-digit** | `multiplication2` | `multiplication_0202` |
| 3-digit ÷ 1-digit with remainder | `division` | `division_long_1dd3dd_r` |
| 4-digit ÷ 1-digit with remainder | `division` | `division_long_1dd4dd_r` |

Example, kid2's 2×2 multiplication, variant C:
`https://math-drills.com/multiplication2/multiplication_0202_003.php`

> ⚠️ **The `1dd*` division slugs leak divide-by-1 problems — check before you hand one
> over.** Set by Asif 2026-08-01: *"I really don't like it when we divide by 1 — it's a
> waste of time for the kid."* He's right, and it isn't rare. `1dd` means a 1-digit
> *divisor*, and math-drills draws that digit from **1–9**, so `1)598 = 598 R0` is a
> legal problem — the kid copies the number down and no long division happens.
>
> Measured across all ten variants of `division_long_1dd3dd_r` (parsed from the PDFs,
> 20 problems each):
>
> | Variant | A | B | C | **D** | E | **F** | G | H | I | J |
> |---|---|---|---|---|---|---|---|---|---|---|
> | ÷1 problems | 2 | 2 | 2 | **0** | 5 | **0** | 2 | 2 | 3 | 2 |
>
> **7 of 10 are contaminated**; only **D** and **F** are clean. kid2 got B on
> 2026-08-01. Assume the other `1dd*` slugs behave the same way and spot-check the
> variant before printing — or use a grid sheet below, which draws divisors 2–9.

### Slug decoder (division)

The division names are dense and easy to pick wrong:

- `1dd` = **1-digit divisor**
- `2dd` / `3dd` / `4dd` = 2- / 3- / 4-digit **dividend**
- `2dq` / `3dq` = 2- / 3-digit **quotient** — a *different* axis, don't confuse it with `dd`
- `_r` = **with remainders** · `_nr` = no remainders · `_d` = decimal quotients

`_d` (decimal quotients) is the natural next step for kid2's decimals target, but it isn't in the table above — introduce it on a TEACH sheet before drilling it.

## Sheets that force the work

**Added 2026-08-01.** The default math-drills layout gives a bare problem and blank
space underneath. Blank space is opt-*in*: a kid who wants to skip the written method
just writes an answer, and [`AGENTS.md`](AGENTS.md) § "Showing the work IS the
assignment" is why that ruins the sheet as a measurement.

The **`_grid_` + `_prompts_`** family solves it structurally. Every multiply → subtract
→ bring-down step gets its own printed box and the `R` box is pre-drawn, so the process
can't be skipped on the way to an answer.

```
division_long_grid_<N>digit_divisor_<M>digit_dividend_prompts_all_remainders_<001..010>
```

| Property | Value |
|---|---|
| Problems | **12** (vs 20 on a plain sheet — fewer, done properly) |
| Divisors drawn from | **2–9** — structurally no divide-by-1 |
| Remainders | `all_remainders` is literal: **every** problem lands on one |
| Pages | 2 — questions, then a key that shows **every intermediate step**, not just answers |

Also comes in `_no_remainders_` and plain `_remainders_` (mixed), and without `prompts_`
(grid, but no step boxes). The **`prompts_`** one is the point — take it.

> **Verify the sheet by rendering it, not by extracting text.** These PDFs are newer
> (v1.5, embedded CID fonts) and text extraction returns *nothing* — the trick that
> works on the older v1.3 sheets silently yields zero problems, which reads as "empty
> sheet" rather than "wrong tool." Render and look:
> ```bash
> pdftoppm -png -r 90 -f 1 -l 1 sheet.pdf out    # page 1; -f 2 -l 2 for the key
> ```
> `sips -s format png` also works but only ever renders page 1.

**Used so far:** kid2's 2026-08-01 redo —
`division_long_grid_1digit_divisor_3digit_dividend_prompts_all_remainders_001` (A).

## The next rung — verified 2026-08-01

Same live check as the table above (page resolves, non-`qp` PDF exists and is 2 pages,
10 variants each), with a deliberately-bogus slug checked alongside so the check could
actually fail. It did.

> ⚠️ **Before reaching for any of these, check the variants aren't the answer.**
> One slug is **ten sheets** (`_001`…`_010`). As of 2026-08-01 only variant **A** is
> spent on the current slugs, so there are **nine more sheets of the same shape** for
> each. If the goal is "get better at *this*", that is the work — a harder slug changes
> the skill instead of deepening it. Step up only on the existing rule in
> [`AGENTS.md`](AGENTS.md) § "When to move the pin again": **zero errors, under time,
> twice in a row.**

### kid1 (3rd → 4th)

| Order | Skill | Category / slug | Kind of step |
|---|---|---|---|
| 1 | 4-digit × 1-digit | `multiplication2` / `multiplication_0401` | size only — same method |
| 2 | 3-digit ÷ 1-digit, remainder | `division` / `division_long_1dd3dd_r` | size only — same method |
| 3 | **2-digit × 2-digit** | `multiplication2` / `multiplication_0202` | 🆕 **new method** — the placeholder zero |

### kid2 (4th → 5th)

| Order | Skill | Category / slug | Kind of step |
|---|---|---|---|
| 1 | 3-digit × 2-digit | `multiplication2` / `multiplication_0302` | size only — still two partial products |
| 2 | **2-digit divisor**, 3-digit dividend, remainder | `division` / `division_long_2dd3dd_r` | 🆕 **new method** — estimation |
| 3 | 2-digit divisor, 4-digit dividend | `division` / `division_long_2dd4dd_r` | size, once #2 lands |
| 4 | **3-digit × 3-digit** | `multiplication2` / `multiplication_0303` | 🆕 **new method** — three rows, `0` *and* `00` |
| 5 | 4-digit ÷ 1-digit, **decimal quotient** | `division` / `division_long_1dd4dd_d` | 🆕 **new method** — feeds the decimals target |

**The 🆕 rows need a TEACH sheet first — do not hand them over as a cold drill.** This
file already said it about `_d`; it is at least as true of a 2-digit divisor. "How many
23s go into 147?" is a genuinely different act from "how many 7s go into 42", and no
amount of long-division fluency with a 1-digit divisor prepares a kid for it. The
size-only rows need nothing — they are the same marks on a longer page.

Tabs 1 and 3 of [`animations/`](animations/README.md) already teach kid1's #3
(2-digit × 2-digit). Nothing yet covers the 2-digit divisor or the decimal quotient.

## Maintenance sheets

Below the pin, so not for daily use — but useful if a week goes badly and you want a confidence page. From the earlier plan bank:

| Use | Category / slug |
|---|---|
| 3-digit subtraction w/ regrouping | `subtraction` / `subtraction_multidigit_0303` |
| 4-digit − 4-digit | `subtraction` / `subtraction_multidigit_0404` |
| Mixed +/− 2-digit (operation-switching) | `multiop` / `addition_subtraction_2digit_100questions_sumsto099` |
| Multi-step word problems (easy) | `mathwordproblems` / `word_problems_multi-step_easy` |

## History — the retired forge job

Until 2026-07-27 a forge monitor (`forge-bot/src/chief-of-staff/monitors/math-worksheets.ts`, cron `30 15 * * *`) posted two random math-drills PDFs to personal Slack every afternoon. **Deleted 2026-07-27 at Asif's direction.** Its curated slug list is preserved here, but it is *not* what's in the tables above, and that's the point:

| | Retired forge list topped out at | The pin actually wants |
|---|---|---|
| Multiplication | facts to 144 (12×12 single-digit) | 2-digit × 2-digit |
| Division | **no division category at all** | long division with remainders |
| Add/sub | 3-digit ± 3-digit | (maintenance only) |

Its full retired list was: `multiplication_facts_to_144{,_zeros,_no01}`, `multiplication_facts_to_100{,_zeros}`, `multiplication_facts_to_81_zeros`, `multiplying_doubles_upto12`, `mixed_addition_subtraction_{2digit_2digit,3digit_3digit,3digit_2digit}_some_regrouping`, `addition_2digit_regrouping`, `addition_3digit_3digit`, `subtraction_0202_some_regrouping`, `subtraction_multidigit_0303`.

That whole range is the spread the **May 2026 measurement retired** — both kids ran 49 problems of 3-digit-minus-3-digit regrouping in 13 minutes (~16 s/problem, inside the 15–20 s fluency benchmark). It had also posted a single pair for *both* kids, so there was no kid1/kid2 split. See [`PRACTICE-PLAN-2026.md`](PRACTICE-PLAN-2026.md) § "Why this plan isn't fact drills".
