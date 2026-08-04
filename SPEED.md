# Speed — what the published benchmarks actually say

**Researched 2026-08-03.** Asif: *"I'm really concerned about speed for the kids drills…
we really need to figure this out. Does khan academy or Kumon give insights on speed?"*

> ## The answer in three lines
>
> - **Kumon: yes, and it's the strongest of the three** — Standard Completion Time is a
>   *promotion gate*, not a metric. But the per-level chart is center-internal and not
>   published, so you can't use it from outside.
> - **Khan Academy: no.** Mastery-based and untimed by design. It publishes no speed norm.
> - **The one you actually want is neither**: Curriculum-Based Measurement, scored in
>   **digits correct per minute (DCPM)**, with free published grade norms.
>
> And the finding that matters more than any of them: **by the DCPM standard, our one
> real measurement is not "inside the benchmark" — it's below the floor.** This repo has
> been reasoning from a number it cannot source. See § The claim this repo got wrong.

## What each source gives you

| Source | Publishes a speed standard? | Usable from outside? |
|---|---|---|
| **Kumon** | **Yes — Standard Completion Time (SCT)**, per level, per worksheet. "SCT is the average number of minutes it should take students to complete one entire worksheet with a perfect score." It gates promotion: a student repeats a set until they hit SCT *with* accuracy, then advances | ❌ The chart is instructor material. Public copies are leaked uploads. What *is* published: **15–30 min per 2-page section** including the answer check, and ~30 min/day per subject — see [`KUMON.md`](KUMON.md) |
| **Khan Academy** | **No.** Mastery learning, self-paced, explicitly untimed — "students prove mastery of a topic and get to move on immediately." Its guidance is about *minutes of practice per week*, not speed per problem | ❌ Nothing to compare against |
| **CBM-Math** (VanDerHeyden & Burns, 2009) | **Yes — digits correct per minute, grades 2–5, with ±1 SD bands**, split by whether the material is new or already mastered | ✅ **Free, citable, and you can generate matching probes** |
| **Rocket Math** (2013) | **Yes — single-digit facts, problems per minute by grade** | ✅ Free PDF |

Kumon's idea is the right one and worth stealing even without their chart: **speed is a
gate, not a report card.** You don't advance until you're fast *and* accurate. That is
already this repo's rule — [`AGENTS.md`](AGENTS.md) § "When to move the pin again": zero
errors, under time, twice in a row. What was missing was a defensible "under time."

## The numbers

### Multi-digit computation — the one that applies to our drills

**CBM-Math Computation Fluency Norms, digits correct per minute.** 2-minute standardized
probes. Source: VanDerHeyden, A. M., & Burns, M. K. (2009), *Performance indicators in
math*, Journal of Behavioral Education, 18, 71–91; table reproduced by Jim Wright,
[interventioncentral.org](https://www.interventioncentral.org/curriculum-based-measurement-reading-math-assesment-tests).

| Grade | New material — median | New material — typical band | Mastered material — median | Mastered — typical band |
|---|---|---|---|---|
| 2 | 15 | 9–21 | 23 | 11–35 |
| 3 | 37 | 22–52 | 17 | 11–23 |
| 4 | 45 | 28–62 | 30 | 20–40 |
| 5 | 26 | 15–37 | 36 | 25–47 |

Two things to read carefully before using this table:

- **"New material" vs "mastered material" are different probes**, and our drills are the
  second kind — a drill is *supposed* to be a skill they already own. Grade 3 mastered =
  11–23; grade 4 mastered = 20–40.
- **The bands are ±1 SD — the typical range, not a pass mark.** Below the floor means
  "unusual", not "failing".

### Single-digit facts — the input to everything else

**Rocket Math Fact Fluency Benchmarks** (R&D Instructional Solutions, 2013),
[PDF](https://www.rocketmath.com/wp-content/uploads/2015/05/Rocket_Math_2013_Fact_Fluency_Benchmarks.pdf).
Problems per minute, single-digit facts only:

| Grade | Start of year | Mid year | End of year |
|---|---|---|---|
| 3 | addition 30/min | subtraction 30/min | **multiplication 30/min** |
| 4 | add/sub/mult 35/min | division 20/min | **all four 35/min** |
| 5 | all four 35/min | — | all four 35/min |

35/min is **1.7 seconds per fact**. That is the automaticity bar, and it is the number
that decides whether long division feels slow.

## The claim this repo got wrong

[`PRACTICE-PLAN-2026.md`](private/PRACTICE-PLAN-2026.md) § "Why this plan isn't fact
drills" says:

> "both kids did **49 problems of 3-digit-minus-3-digit subtraction with regrouping in 13
> minutes — ~16 sec/problem.** The fluency benchmark is 15–20 sec, so single-digit fact
> recall is already automatic; you cannot sustain that pace on 3-digit regrouping
> otherwise."

**Two problems with that.**

1. **The 15–20 second benchmark has no citation, and I could not source it.** No published
   fluency standard is expressed in seconds-per-multi-digit-problem. The field uses digits
   correct per minute, and single-digit automaticity is quoted at **~2 seconds per fact**,
   not 15–20.

2. **Converted to DCPM, that measurement lands below the floor**, not inside a band:

   ```
   49 problems × 3 answer digits ÷ 13 min = 11.3 DCPM
   ```

   | Compared against | Result |
   |---|---|
   | Grade 3, mastered material (11–23) | 11.3 — **at the very bottom** of the band |
   | Grade 3, new material (22–52) | **51% of the floor** |
   | Grade 4, mastered material (20–40) | **57% of the floor** |
   | Grade 4, new material (28–62) | **40% of the floor** |

   Run it yourself: `python3 speed_check.py --anchor --grade 4`

This matters because that paragraph is **load-bearing**. It is the stated reason the whole
plan skips fact drills — "Xtramath / Mad Minute style fact drills are NOT the bottleneck."
That conclusion was drawn from an uncited benchmark, and the sourced benchmark points the
other way.

### What would make this finding wrong

Stated plainly, because the confounds are real and at least one of them is likely:

- **Was the 13 minutes a stopwatch?** The note doesn't say. If it was elapsed session time
  with breaks, the DCPM number is meaningless and so is this entire section. **This is the
  most likely explanation and the cheapest to rule out.**
- **CBM probes are mixed-skill grade-level sheets.** They include easier items that lift
  DCPM. A pure 3-digit-regrouping sheet is harder per digit, so a lower score on it is
  expected — some of the gap is this, and it cuts in the kids' favour.
- **Digit counting.** 3 answer digits per problem is the generous end; at 2.5 it's 9.4
  DCPM, which is worse, not better. The direction of that error is safe.

So this is a **"go measure it properly"** finding, not a "your kids are behind" finding.
Nothing here says they're behind. It says the number we've been reassuring ourselves with
doesn't mean what the doc claims it means.

## The measurement to actually run

Twenty minutes, once, and it settles this. Two probes, because **they test different
things and only one of them is what we've been drilling.**

**1. Fact probe — 1 minute, single-digit multiplication and division.**
Is recall automatic? Target 35/min (1.7 s/fact) for both kids by the Rocket Math table.

```bash
python3 speed_check.py --facts --problems <correct> --minutes 1 --grade 4
```

**2. Computation probe — 2 minutes, at each kid's actual pin.**
Score **digits correct**, not problems. Long division: quotient digits *and* the remainder.

```bash
python3 speed_check.py --problems <correct> --minutes 2 --digits <answer digits> --grade 4
```

Rules that make it a measurement instead of a vibe:

- **Stopwatch, continuous.** Start on "go", stop at the buzzer. No breaks, no coaching.
- **More problems than they can finish.** A sheet they complete measures the sheet, not
  the kid.
- Score the digits that are *correct*. A wrong digit is worth zero; the ones after it in
  the same answer still count if they're right.
- Run it **twice on different days** before believing it. One probe is a mood.

Standardized probes, free: the [Intervention Central Math Worksheet
Generator](http://www.interventioncentral.org/teacher-resources/math-work-sheet-generator)
makes CBM-compatible single-skill and mixed-skill sheets with answer keys, timed or
untimed. `drill_gen.py --budget 120` gets close but is sized to *finish* in the window,
which is the opposite of what a probe needs — use the generator, or pass a bigger
`--problems` override.

### Then what

- **Facts slow (< 30/min) →** that's the bottleneck, and no amount of long-division
  drilling fixes it. The retired fact-drill range comes back for a few weeks. That
  reverses the current plan, which is exactly why it's worth measuring first.
- **Facts fine, computation slow →** it's the algorithm, not recall. Fewer problems, grid
  layout, and check whether steps are being skipped.
- **Both fine →** speed isn't the problem, and `drill_cost.py`'s `SEC_PER_MARK` needs
  recalibrating upward from a real observation instead of the May 2026 anchor.

In every branch, feed the result to `drill_cost.calibrate(observed_sec=…, marks=…)` and
update `SEC_PER_MARK`. That is the point of the whole model, and it has never been fed a
second data point.

## Confidence

**The benchmark numbers: high.** Both tables are quoted verbatim from primary sources —
the CBM norms from the VanDerHeyden & Burns table (PDF parsed locally after the fetcher
couldn't read it), the fact benchmarks from the Rocket Math PDF. Neither was rounded or
reconstructed from a search summary.

**The Kumon and Khan characterisations: high for Kumon, medium for Khan.** Kumon's SCT
definition and its role as a promotion gate are stated on Kumon-operated pages; the
15–30 min figure is verbatim from the official Educator's Guides ([`KUMON.md`](KUMON.md)).
Khan Academy's untimed/mastery stance is well documented, but I'm inferring "publishes no
speed norm" from its absence — an open-world absence, so treat it as "none found", not
"none exists".

**The DCPM conversion of our anchor: medium, and the confounds above are why.** The
arithmetic is exact. Whether the 13 minutes was stopwatch time is unknown and decides
everything.
