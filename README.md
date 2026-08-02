# Printable math worksheets, sized to a five-minute drill

**Free printable math practice for roughly 3rd–5th grade** — word problems, logic
puzzles, and arithmetic drills, each one page per kid plus a worked answer key.

### → **[math.sifxtreme.com](https://math.sifxtreme.com)** — print them, no signup, no ads

<p align="center">
  <img src="docs/multiplication.gif" alt="47 × 36 worked one written mark at a time" width="420">
</p>

The site also has step-through animations of the written methods — long division and
multiplication, one pencil mark at a time, with the trap called out at the step where it
actually bites. This repo is the generator behind it all: self-contained HTML, no
dependencies, `python3` and a browser.

Two things here are unusual and worth the thirty seconds:

- **Drills are sized to a clock, not a page.** Most worksheet sites give you 20 or 25
  problems whatever the skill. 20 long divisions is a sixteen-minute sheet. If you want
  five minutes, the count has to come from the work, and that's what `drill_cost.py`
  computes.
- **The grid forces the work to be shown.** Every step of the written method gets its own
  printed box, so a child can't jump to an answer. That rule exists because one of them
  did exactly that. It's optional — `--layout plain` gives the same problems with blank
  space, for when the method is solid and you want it the way a test would ask.

---

## Setting it up for your kids

**One step.** Copy the example config and put your own names in it:

```bash
cp kids.example.json kids.local.json
$EDITOR kids.local.json
```

```json
{
  "kids": [
    { "id": "kid1", "name": "Amira", "grade": 3 },
    { "id": "kid2", "name": "Idris", "grade": 4 }
  ]
}
```

That's it — generate a sheet and the names are on it.

**`kids.local.json` is gitignored. `kids.example.json` is not.** Committed code refers to
children by `id` (`kid1`, `kid2`) and never by name; the name is read at render time and
appears only in the printed `Name:` field. So you can share, fork, or publish the repo
without shipping your family with it.

If you skip this step nothing breaks — the generator falls back to the example file and
prints a loud notice. Sheets will say "Kid One". That's deliberate: a *silent* fallback
would hand you a stack of paper addressed to nobody.

### More or fewer than two kids

`id`s are the contract. The drill plans in `drill_gen.py` are keyed on `kid1` and `kid2`:

```python
PLANS = {
    "div": [("kid1", (2, 1), "2-digit ÷ 1-digit, with a remainder", "div_2d_1"),
            ("kid2", (3, 1), "3-digit ÷ 1-digit, with a remainder", "div_3d_1")],
    ...
}
```

Add a `kid3` to your config and a matching row there. The digit shapes `(2, 1)` mean
2-digit dividend ÷ 1-digit divisor; the last field picks the time model from
`drill_cost.py`.

### What is and isn't in this repo

Being straight about it, because a half-private repo is worse than a known-public one.
This repo **is public**, and it was scrubbed deliberately before it was published:

| | |
|---|---|
| ✅ All code | keyed on `kid1`/`kid2` ids, no names |
| ✅ `private/` and `kids.local.json` | gitignored — the practice plan, results log, and any per-child notes live there |
| ✅ Generated sheets | gitignored; rebuilt from a seed |
| ✅ Every `Name:` header field | blank — the child writes it |
| ✅ Git history and commit messages | rewritten with `git-filter-repo`; no names, no school, no per-child records |
| ℹ️ **Story characters** | The word problems and logic puzzles are cast with Muslim names — Idris, Hamza, Bilal, Amina, Zayd, Tariq and others. Those are **characters**, kept on purpose: the puzzle answers reference them by name. Nothing indicates whose repo it is. |

If you fork this for your own kids, `kids.local.json` is the only file that ever holds a
real name, and it is gitignored from the start.

---

## Daily use

A full day is **three sheets per kid**: word problems, logic, and a drill.

```bash
# drills — generated, sized to five minutes
python3 drill_gen.py --skill div --seed $(date +%Y%m%d)   # or --skill mul
python3 verify_drills.py                                  # must exit 0
./print-worksheet.sh worksheet-division-drill.html --dry-run

# word problems / logic — pick the day's sheet from PRACTICE-PLAN-2026.md
./print-worksheet.sh worksheet-sailing-ships.html --date today
```

`--budget 600` makes it a ten-minute sheet instead; the problem counts re-derive
themselves. `--seed` makes a sheet reproducible — same seed, same problems.

> ⚠️ **`print-worksheet.sh` and `print-drill.sh` refuse to print ahead, print a batch, or
> reprint a day that already exists.** That's `day-guard.sh`, and it is deliberate. A
> genuine replacement goes through `--override-day-guard`, which is loud and logged.

## The files

| File | What |
|---|---|
| `drill_gen.py` | generates division/multiplication drills, sized to a time budget |
| `drill_cost.py` | the time model — marks per problem → seconds → problems per sheet |
| `verify_drills.py` | audits the rendered HTML independently. Run before printing |
| `build_sheets.py` | generates the word-problem and logic sheets from `specs_*.py` |
| `verify_sheets.py` | re-derives every word-problem answer. Must exit 0 |
| `print-worksheet.sh` | render to a clean PDF and print |
| `print-drill.sh` | same, for an external drill PDF |
| `day-guard.sh` | the one-day-at-a-time print guard |
| `animations/` | step-through animations of the written methods |
| `AGENTS.md` | **the real documentation** — rules, difficulty pin, hard-won lessons |
| `DRILLS.md` | external drill sources (fallback) |
| `PRACTICE-PLAN-2026.md` | the day-by-day schedule |

**`AGENTS.md` is the file to read before changing anything.** It carries the rules that
have already decayed once and been reinstated — why drills are one day at a time, why the
work has to be shown, and why a doc that says "never" needs its date checked.

## The public site — [math.sifxtreme.com](https://math.sifxtreme.com)

A scrubbed subset of this repo is published as a free printable-worksheet site. It is a
**separate Cloudflare Pages project** (`sifxtreme-math`) from the blog, on purpose: a bad
math deploy can then never touch sifxtreme.com.

```bash
python3 build_site.py          # renders site/ from the SHEETS allow-list
python3 verify_public.py       # MUST exit 0 — refuses to publish if anything private survived
export CLOUDFLARE_API_TOKEN=$(grep ^CLOUDFLARE_API_TOKEN= ~/code/experiments/cloudflare-cli/.env | cut -d= -f2-)
npx wrangler pages deploy site --project-name sifxtreme-math --branch master
```

⚠️ **Verify by grepping the live page, never by status code** — Pages serves its fallback
with a `200`, so an unpublished URL still looks fine:

```bash
curl -sL https://math.sifxtreme.com/ | grep -o '<title>[^<]*</title>'
```

**What makes a sheet publishable:** the `SHEETS` allow-list in `build_site.py`. A new
worksheet is private until someone adds it — the safe default. `verify_public.py` is the
last line, not the only one, and it reads the terms it hunts from the gitignored
`private/forbidden-terms.txt` rather than hardcoding them.

## Calibrating the time model

Every problem count is currently a **prediction**. The model is anchored on one real
measurement (49 problems of 3-digit subtraction in 13 minutes) and extrapolated from
subtraction to division and multiplication.

To make it a measurement instead: time a real sheet, then

```python
import drill_cost
drill_cost.calibrate(observed_sec=41.0, marks=15.0)   # → the SEC_PER_MARK it implies
```

and update `SEC_PER_MARK`. **Don't hand-adjust the problem counts** — that breaks the
link between the model and reality, and then the numbers mean nothing.
