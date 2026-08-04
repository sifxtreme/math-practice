# Kumon sample packets — and how long a page is supposed to take

**Researched 2026-08-03.** Asif asked for Kumon packets, then: *"I'm concerned about
speed. How long is it supposed to take."* This file is the answer to both, and the second
question is the one that turned out to matter.

> ## ⏱ The number, up front
>
> **A Kumon page is a 7.5–15 minute unit. A drill from this repo is a 5 minute page.**
>
> Kumon's own guidance, quoted from the official Educator's Guides:
>
> > "We recommend having your child complete about one section (**2 pages**) a day. This
> > should include the answer check."
> > "Each daily session is about **15 to 30 minutes**. If your child is learning the skill
> > for the first time, the learning session will be closer to 30 minutes."
>
> — *Kumon Grade 4 Division Workbook Educator's Guide*, § Important Steps → Timing
> ([PDF](https://kumonbooks.com/wp-content/uploads/2023/10/G4DivGuide.pdf)); identical
> wording in the [Grade 3 guide](https://kumonbooks.com/wp-content/uploads/2023/10/G3DivisionGuide-1.pdf).
>
> So the whole 12-page packet, at Kumon's own pacing, is **6 daily sessions = 90–180
> minutes of work.** It is not a stack you hand over in one sitting.

## Two answers that disagree, and why you want both

`python3 kumon_cost.py` prices every page in the packet with the same marks model
[`drill_cost.py`](drill_cost.py) uses for generated drills, then puts it next to Kumon's
number:

```
 p  book                              topic                                probs    model      vs Kumon
-------------------------------------------------------------------------------------------------------
 1  Grade 3 Multiplication            2x table: fill-in + trace               29     2.9m          2.6x
 2  Grade 3 Multiplication            2x table                                27     3.6m          2.1x
 3  Grade 3 Multiplication            2x table                                30     3.9m          1.9x
 4  Grade 3 Multiplication            2x table                                30     3.9m          1.9x
 5  Grade 4 Decimals and Fractions    addition of decimals                    12     3.2m          2.4x
 6  Grade 4 Decimals and Fractions    addition of decimals                    13     3.5m          2.2x
 7  Grade 4 Decimals and Fractions    improper -> mixed numbers               20     3.8m          2.0x
 8  Grade 4 Decimals and Fractions    improper -> mixed numbers               20     3.8m          2.0x
 9  Grade 4 Word Problems             review: mixed units, time, grouping      -        -  not modelled
10  Grade 4 Word Problems             review: money, grouping, comparison      -        -  not modelled
11  Grade 5 Geometry and Measurement  quadrilaterals / trapezoids              -        -  not modelled
12  Grade 5 Geometry and Measurement  drawing trapezoids                       -        -  not modelled
```

The model is **2–2.6× faster** than Kumon's *lower* bound. That gap is not a defect in
either number — they are measuring different things:

| | Kumon's 7.5–15 min | `drill_cost.py`'s 3–4 min |
|---|---|---|
| Includes the answer check | **yes**, stated explicitly | no |
| Assumes first exposure to the skill | yes, at the 30-min end | no |
| What it's describing | a comfortable daily session at the child's placed level | a **timed** fluency drill |
| What it prices | sitting down, reading, working, checking | written marks only |

**Use them for different things.** Kumon's 7.5–15 min/page is the *"is my kid
struggling"* line. The model's 3–4 min is the *"is this page still worth printing"* line.
A page priced at 3 min that takes 12 is a real signal. A page priced at 3 min that takes
4 is fine — and is also telling you the page is below the pin.

### Applied to our two

Both kids are past the anchor measurement (49 problems of 3-digit subtraction in 13 min
= 15.9 s/problem, May 2026, inside the 15–20 s fluency benchmark). Neither is meeting
this material for the first time, so **the 30-minute end of Kumon's range does not apply
to them.** Expect the 15-minute end at worst, and the model's 3–4 min if the skill is
actually solid.

If a Grade 3 Multiplication page here takes kid1 anywhere near 7.5 minutes, that is not
a speed problem — it is the wrong page. See below.

## What's actually in the packet

[Bookstore Sample Packet Grades 3-5](https://kumonbooks.com/wp-content/uploads/2022/08/Bookstore-Packet-3_5.pdf)
— 17 pages, of which **12 are worksheets**; pages 1–4 are marketing and 17 is a catalog.
The stripped 12-page version is at `private/kumon/kumon-gr3-5-worksheets-only.pdf`.

| Pages | Book | Content | Verdict against the pin |
|---|---|---|---|
| 1–4 | Grade 3 Multiplication ©2008 | **2× times table only** | ❌ **Below kid1's pin.** He is on 2-digit × 1-digit and long division with remainders. This is the fact-drill range the May 2026 measurement retired — see [`DRILLS.md`](DRILLS.md) § History |
| 5–8 | Grade 4 Decimals and Fractions ©2009 | decimal column addition; improper → mixed | ✅ **The useful ones.** [`DRILLS.md`](DRILLS.md) names decimals as kid2's next target and says nothing covers it yet |
| 9–10 | Grade 4 Word Problems ©2009 | 11 multi-step problems — mixed units, time, grouping | ✅ usable for either kid |
| 11–12 | Grade 5 Geometry and Measurement ©2009 | trapezoids, parallel lines, protractor drawing | ➖ off-curriculum for the current pin |

> ⚠️ **No answer keys. Not one page, in any of the sample packets.** This is the material
> difference from both existing sources: `drill_gen.py` always emits a key, and
> [`DRILLS.md`](DRILLS.md) picks the non-`qp` math-drills PDF *specifically* to get the
> 2-page question+key pair. Every Kumon page here is graded by hand.

> ⚠️ **These will not go through `print-worksheet.sh` or `print-drill.sh`.**
> `print-drill.sh` rejects any PDF that isn't 2 pages — exactly the question+key shape
> these lack — and `print-worksheet.sh` self-checks 3 `.sheet` blocks. Printing them
> means a bare `lp`, which [`day-guard.sh`](day-guard.sh) cannot see. That is the hole
> [`DRILLS.md`](DRILLS.md) § "Printing a drill" says was half the Jul 28 bulk run. If
> these become regular use, they need a guard path.

## The Kumon page is a 2-page unit worth 100 points

Worth knowing before splitting pages up. Each Kumon sheet carries a **Score /100** box and
a printed **points per question** value, and the points only sum to 100 across the
**pair**: page 2 of the first sheet is 2 pts × 10 + 3 pts × 17 = 71, with the other 29 on
its facing page. Kumon's "one section a day" *is* that pair. Hand over half a sheet and
the score box is meaningless.

## What is NOT available, and why

The real Kumon packets — Levels A through O, the thing people mean by "Kumon worksheets" —
**are not distributed free anywhere legitimate.** They go to enrolled students through the
center or the My Kumon / Kumon Connect apps. The Level C/D/E PDFs that dominate search
results are unauthorized uploads of copyrighted workbooks on Scribd and pdfcoffee; they
are not linked here and were not downloaded.

Checked and ruled out:

| Source | Result |
|---|---|
| [kumon.sg/downloads](https://kumon.sg/downloads/) | Level charts, reading lists, parent magazines. **Zero worksheets** |
| [kumon.com official sample](https://www.kumon.com/assets/us-en/pdfs/math_english_sample_worksheet.pdf) | 2 A5 pages, **Level 2A** (`1+1`, `3+1`) — kindergarten |
| Kumon UK / Canada regional sites | no free worksheet downloads found |
| Scribd / pdfcoffee "Level C/D/E" | pirated copyrighted workbooks — not used |

The three publisher sample packets are the entire legitimate free surface:

| Packet | Pages | Contents |
|---|---|---|
| [Grades 3-5](https://kumonbooks.com/wp-content/uploads/2022/08/Bookstore-Packet-3_5.pdf) | 17 (12 worksheets) | the table above |
| [K–Gr.2](https://kumonbooks.com/wp-content/uploads/2022/08/Bookstore-Packet-K2.pdf) | 24 | numbers 1–120, simple addition, simple subtraction, easy phonics, rhyming words |
| [Pre-K & Up](https://kumonbooks.com/wp-content/uploads/2022/08/Bookstore-Packet-Pre-K.pdf) | 24 | pre-K skills |

Local copies: `private/kumon/` — **gitignored on purpose.** This repo is public
(`github.com/sifxtreme/math-practice`); copyrighted Kumon PDFs must never be committed.
`.gitignore` catches them twice, via `*.pdf` and via `private/`.

## Verification notes

- Every link above was fetched: HTTP 200, `application/pdf`, page counts from `pdfinfo`.
- **Problem counts were read off rendered pages, never `pdftotext`.** These PDFs return
  *nothing* from text extraction — the same CID-font trap [`DRILLS.md`](DRILLS.md)
  documents for the newer math-drills sheets. A count taken from extracted text would
  have been zero, and would have read as "empty page" rather than "wrong tool."
  ```bash
  pdftoppm -png -r 110 -f 2 -l 2 kumon-gr3-5-worksheets-only.pdf p
  ```
- The 12-page extract was rebuilt with `pdfseparate`/`pdfunite` and then re-read off disk
  (`pdfinfo` → 12 pages; per-book composition re-derived) rather than trusted from the
  command's exit code.
- Kumon's timing numbers are **quoted verbatim** from the official guides. They are not
  estimates and were not rounded.
- The model's numbers inherit every caveat in [`drill_cost.py`](drill_cost.py) — one data
  point, one skill, extrapolated — **plus one new one**: the mark counts for recall facts
  (`2 × 7 =`) and fraction rewrites do not come from a multi-digit written algorithm,
  which is the only thing the anchor ever measured. At ~1.3 marks the fixed `SEC_SETUP`
  term is a third of the total and has never been calibrated at that end. The recall rows
  are the softest numbers in this repo.
