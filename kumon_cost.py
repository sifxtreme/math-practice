"""kumon_cost.py — how long a Kumon sample page is supposed to take.

WHY THIS EXISTS
---------------
Asif, 2026-08-03, on being handed the Kumon Grades 3-5 sample packet: *"I'm
concerned about speed. How long is it supposed to take."*

Fair question, and there are TWO answers that do not agree. Both belong here,
because picking one and hiding the other is how a number stops meaning anything.

  1. KUMON'S OWN ANSWER — from the official Educator's Guides on kumonbooks.com
     (`G4DivGuide.pdf`, `G3DivisionGuide-1.pdf`, both fetched 2026-08-03):

         "We recommend having your child complete about one section (2 pages) a
          day. This should include the answer check."
         "Each daily session is about 15 to 30 minutes. If your child is learning
          the skill for the first time, the learning session will be closer to 30
          minutes."

     So Kumon's unit is a 2-PAGE SECTION at 15-30 min => 7.5-15 min PER PAGE,
     and that window explicitly INCLUDES checking the answers.

  2. THIS REPO'S ANSWER — `drill_cost.py` prices a problem by the written marks
     its method requires, calibrated on the one real measurement we have (49
     problems of 3-digit subtraction in 13 min). Applied to the actual problem
     counts on each sample page, it predicts 3-4 min per page.

THE GAP IS REAL AND IT IS NOT A BUG
-----------------------------------
The model is 2-4x faster than Kumon's guidance, and the reasons are all visible:

  - Kumon's window includes the answer check. The model prices pen-moving only.
  - Kumon's 30-min end is for a child meeting the skill FOR THE FIRST TIME.
    Neither of ours is: both are past this material.
  - Kumon is describing a comfortable daily session for a child working at their
    own placed level. `drill_cost.py` is describing a TIMED fluency drill.

Use them for different things. **Kumon's 7.5-15 min/page is the "is my kid
struggling" line; the model's 3-4 min is the "is this still worth printing"
line.** A page that the model prices at 3 min and takes 12 is a real signal. A
page that the model prices at 3 min and takes 4 is fine, and is also telling you
the page is below the pin.

CONFIDENCE
----------
The Kumon numbers are quoted verbatim from official PDFs and are not estimates.
The model numbers inherit every caveat in `drill_cost.py` -- one data point, one
skill, extrapolated -- PLUS a new one: the mark counts below for recall facts
(`2 x 7 =`) and fraction rewrites are NOT drawn from a multi-digit written
algorithm, which is the only thing the anchor ever measured. At ~1.3 marks the
fixed SEC_SETUP term is a third of the total and has never been calibrated at
that end. Treat the recall rows as the softest numbers in this file.

Run `python3 kumon_cost.py` for the table.
"""

from dataclasses import dataclass, field

import drill_cost

# --- Kumon's published guidance, quoted, not derived -----------------------
# Source: Kumon Publishing North America, "Kumon Grade 4 Division Workbook
# Educator's Guide" and the Grade 3 equivalent, section "Important Steps >
# Timing". Fetched 2026-08-03 from kumonbooks.com/wp-content/uploads/2023/10/.
KUMON_SECTION_PAGES = 2
KUMON_SECTION_MIN = (15, 30)          # per 2-page section, INCLUDING answer check
KUMON_PER_PAGE_MIN = (KUMON_SECTION_MIN[0] / KUMON_SECTION_PAGES,
                      KUMON_SECTION_MIN[1] / KUMON_SECTION_PAGES)


# --- mark counts for the problem shapes on the sample pages ----------------
# Same rule as drill_cost.py: a mark is one digit committed to paper. These are
# derived from what the page actually asks for, counted off RENDERED pages --
# never off pdftotext, which returns nothing on these files (CID fonts; the trap
# DRILLS.md documents).

MARKS_RECALL_FACT = 1.3        # `2 x 7 =` -> one or two digits, no method
MARKS_FILL_SENTENCE = 3.0      # `[] x [] = []` copied from a prompt sentence
MARKS_DECIMAL_ADD = drill_cost.marks_subtraction(3)   # 4.5 -- same shape as the anchor
MARKS_IMPROPER_TO_MIXED = 3.0  # divide, then write whole + numerator + denominator


@dataclass
class Section:
    """One numbered exercise block on a page."""
    label: str
    count: int
    marks: float

    def seconds(self) -> float:
        return self.count * (drill_cost.SEC_PER_MARK * self.marks + drill_cost.SEC_SETUP)


@dataclass
class Page:
    n: int
    book: str
    topic: str
    sections: list = field(default_factory=list)
    outside_model: str = ""       # set when the marks model does not apply

    def seconds(self) -> float:
        return sum(s.seconds() for s in self.sections)

    def minutes(self) -> float:
        return self.seconds() / 60


# The 12 worksheet pages of Bookstore-Packet-3_5.pdf, in packet order (that is
# source pages 5-16; 1-4 are marketing and 17 is a catalog page).
# Counts were read off 110-dpi renders on 2026-08-03.
PAGES = [
    Page(1, "Grade 3 Multiplication", "2x table: fill-in + trace", [
        Section("fill missing numbers in sequence", 20, MARKS_RECALL_FACT),
        Section("trace while reading", 9, MARKS_RECALL_FACT),
    ]),
    Page(2, "Grade 3 Multiplication", "2x table", [
        Section("fill in the boxes", 10, MARKS_FILL_SENTENCE),
        Section("multiply", 17, MARKS_RECALL_FACT),
    ]),
    Page(3, "Grade 3 Multiplication", "2x table", [
        Section("fill in the boxes", 10, MARKS_FILL_SENTENCE),
        Section("multiply", 20, MARKS_RECALL_FACT),
    ]),
    Page(4, "Grade 3 Multiplication", "2x table", [
        Section("fill in the boxes", 10, MARKS_FILL_SENTENCE),
        Section("multiply", 20, MARKS_RECALL_FACT),
    ]),
    Page(5, "Grade 4 Decimals and Fractions", "addition of decimals", [
        Section("add", 12, MARKS_DECIMAL_ADD),
    ]),
    Page(6, "Grade 4 Decimals and Fractions", "addition of decimals", [
        Section("add", 13, MARKS_DECIMAL_ADD),
    ]),
    Page(7, "Grade 4 Decimals and Fractions", "improper -> mixed numbers", [
        Section("rewrite", 20, MARKS_IMPROPER_TO_MIXED),
    ]),
    Page(8, "Grade 4 Decimals and Fractions", "improper -> mixed numbers", [
        Section("rewrite", 20, MARKS_IMPROPER_TO_MIXED),
    ]),
    Page(9, "Grade 4 Word Problems", "review: mixed units, time, grouping",
         outside_model="reading + operation choice, not written marks"),
    Page(10, "Grade 4 Word Problems", "review: money, grouping, comparison",
         outside_model="reading + operation choice, not written marks"),
    Page(11, "Grade 5 Geometry and Measurement", "quadrilaterals / trapezoids",
         outside_model="identification + compass and protractor work"),
    Page(12, "Grade 5 Geometry and Measurement", "drawing trapezoids",
         outside_model="identification + compass and protractor work"),
]


def main() -> int:
    print(__doc__.strip().split("\n")[0])
    print()
    print(f"Kumon's own guidance: {KUMON_SECTION_MIN[0]}-{KUMON_SECTION_MIN[1]} min per "
          f"{KUMON_SECTION_PAGES}-page section, answer check included")
    print(f"  => {KUMON_PER_PAGE_MIN[0]:.1f}-{KUMON_PER_PAGE_MIN[1]:.1f} min per page")
    print(f"This repo's model: SEC_PER_MARK={drill_cost.SEC_PER_MARK}, "
          f"SEC_SETUP={drill_cost.SEC_SETUP} (drill_cost.py)")
    print()

    hdr = (f"{'p':>2}  {'book':<34}{'topic':<36}{'probs':>6}{'model':>9}"
           f"{'vs Kumon':>14}")
    print(hdr)
    print("-" * len(hdr))

    modelled_sec = 0.0
    for pg in PAGES:
        if pg.outside_model:
            print(f"{pg.n:>2}  {pg.book:<34}{pg.topic:<36}{'-':>6}{'-':>9}"
                  f"{'not modelled':>14}")
            continue
        n = sum(s.count for s in pg.sections)
        mins = pg.minutes()
        modelled_sec += pg.seconds()
        ratio = KUMON_PER_PAGE_MIN[0] / mins
        print(f"{pg.n:>2}  {pg.book:<34}{pg.topic:<36}{n:>6}{mins:>8.1f}m"
              f"{ratio:>13.1f}x")

    modelled = [p for p in PAGES if not p.outside_model]
    print()
    print(f"{len(modelled)} modelled pages total {modelled_sec/60:.0f} min by the model; "
          f"Kumon would budget {len(modelled)*KUMON_PER_PAGE_MIN[0]:.0f}-"
          f"{len(modelled)*KUMON_PER_PAGE_MIN[1]:.0f} min for the same pages.")
    print(f"All 12 pages at Kumon's pacing = {len(PAGES)//KUMON_SECTION_PAGES} daily "
          f"sessions = {len(PAGES)//KUMON_SECTION_PAGES*KUMON_SECTION_MIN[0]}-"
          f"{len(PAGES)//KUMON_SECTION_PAGES*KUMON_SECTION_MIN[1]} min of work.")
    print()
    print("'vs Kumon' = how many times faster the model is than Kumon's LOWER bound.")
    print("The model prices pen-moving; Kumon's window includes the answer check.")
    print("Neither is a stopwatch. Time a real page, then drill_cost.calibrate().")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
