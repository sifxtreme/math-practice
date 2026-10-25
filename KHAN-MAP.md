# KHAN-MAP: where Khan Academy teaches and assesses the algebraic-thinking skills

**Verified 2026-10-25** by rendering each Khan course page and each Common Core standards page in headless
Chromium (no login). Raw renders were read in full; links come from the rendered `href`s. Anything not read on a
Khan page is marked **UNVERIFIED**. Do not check Khan links with curl (see the note in `AGENTS.md`, Difficulty pin).

**What "assessed" means here.** Khan places a `Quiz N` after a group of exercises and a `Unit test` at the end of
each unit. Each course ends with a `Course challenge`. This file names the quiz that follows the exercise on the
course page. **UNVERIFIED for all rows: the questions inside each quiz or test were not opened** (they need a
login to attempt). Quiz position is a fact; quiz content is an inference from the exercise it follows.

Base URL: `https://www.khanacademy.org`. Links below start with `/math/...`.

## Answer table

| # | Skill | Earliest Khan teaching (course, unit, exercise) | Assessed in | CCSS | 
|---|-------|--------------------------------------------------|-------------|------|
| 1 | Work backwards / undo the steps | **Formal only.** 7th, Unit 6: [Two-step equations](https://www.khanacademy.org/math/cc-seventh-grade-math/cc-7th-variables-expressions/cc-7th-2-step-equations-intro/e/linear_equations_2), [Two-step equations word problems](https://www.khanacademy.org/math/cc-seventh-grade-math/cc-7th-variables-expressions/cc-7th-linear-eq-word-probs/e/linear-equation-world-problems-2). Closest in 3rd-4th: 3rd U8 [2-step word problems](https://www.khanacademy.org/math/cc-third-grade-math/arithmetic-patterns-and-problem-solving/imp-one-and-two-step-word-problems/e/two-step-word-problems-with-addition--subtraction--multiplication--and-division), 4th U5 [Multi-step word problems](https://www.khanacademy.org/math/cc-fourth-grade-math/division/multi-step-word-problems/e/multi-step-word-problems-with-whole-numbers). No 3rd-5th exercise is named for "undo" or "work backwards". | 7th U6 Quiz 2 + Unit test; 3rd U8 Quiz 1; 4th U5 Quiz 4 | 7.EE.B.4.a; 3.OA.D.8; 4.OA.A.3 | 
| 2 | Substitution, two unknowns with a relation | **Formal only.** 8th, Unit 4: [Systems of equations with substitution](https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-with-substitution/e/systems_of_equations_with_substitution). Algebra 1, Unit 6, same name. **No arithmetic "trade it" version in 3rd-5th** (searched every exercise name). | 8th U4 Quiz 1 + Unit test; Algebra 1 U6 Quiz 2 + Unit test | 8.EE.C.8.b | 
| 3 | Age problems | 8th, Unit 4: [Age word problems](https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-word-problems/e/age_word_problems). Also Algebra 1 U6, IM Grade 8 U4. Nothing earlier. | 8th U4 Quiz 2 + Unit test; Algebra 1 U6 Quiz 3 + Unit test | 8.EE.C.8.c | 
| 4 | Sum and difference ("3 older, sum 25") | **No exercise found** in any course by name. Nearest: 8th U2 [Sums of consecutive integers](https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-solving-equations/linear-equations-word-problems/e/integer_sums); 8th U4 [Systems of equations word problems](https://www.khanacademy.org/math/cc-eighth-grade-math/cc-8th-systems-topic/cc-8th-systems-word-problems/e/understanding-systems-of-equations-word-problems). Whether those contain a sum-and-difference item: **UNVERIFIED**. | 8th U4 Quiz 2 + Unit test (inference) | 8.EE.C.8.c | 
| 5 | Average / missing value from a mean | **6th, Unit 11**: [Calculating the mean](https://www.khanacademy.org/math/cc-sixth-grade-math/cc-6th-data-statistics), then [Missing value given the mean](https://www.khanacademy.org/math/cc-sixth-grade-math/cc-6th-data-statistics/cc-6th-mean-median-challenge/e/find-a-missing-value-given-the-mean). No "mean" or "average" exercise in the 3rd, 4th or 5th grade courses. | 6th U11 Quiz 2 + Unit test; IM Grade 6 U8 | 6.SP.B.5.c | 
| 6 | Missing numbers in equations; equal sign | 3rd: U7 [Find missing factors](https://www.khanacademy.org/math/cc-third-grade-math/imp-multiplication-and-division/imp-more-with-1-digit-multiplication-and-division/e/finding-missing-factors--1-digit-multiplication-), [Find missing divisors and dividends](https://www.khanacademy.org/math/cc-third-grade-math/imp-multiplication-and-division); U3 [Find the missing number (add and subtract within 1000)](https://www.khanacademy.org/math/cc-third-grade-math/imp-addition-and-subtraction/imp-addition-and-subtraction-missing-value-problems/e/find-the-missing-number--addition-and-subtraction-within-1000-). Balance picture: 6th U7 [hanger diagrams](https://www.khanacademy.org/math/cc-sixth-grade-math/cc-6th-equations-and-inequalities/cc-6th-solving-equations/e/identify-equations-from-visual-models). Equal-sign meaning in K-2: **UNVERIFIED** (not read). | 3rd U7 Quiz 1 + Unit test; 3rd U3 Unit test; 6th U7 Quiz 1 + Unit test | 3.OA.A.4; 6.EE.B.7 | 
| 7 | Patterns / "what rule" | 3rd U8 [Math patterns](https://www.khanacademy.org/math/cc-third-grade-math/arithmetic-patterns-and-problem-solving/imp-patterns-in-arithmetic/e/patterns); 4th U6 [Patterns with numbers](https://www.khanacademy.org/math/cc-fourth-grade-math/imp-factors-multiples-and-patterns/imp-math-patterns/e/math-patterns); 5th U13 [Rules that relate 2 variables](https://www.khanacademy.org/math/cc-fifth-grade-math/imp-algebraic-thinking/imp-number-patterns/e/write-a-2-variable-relationship) | 3rd U8 Quiz 2 + Unit test; 4th U6 Quiz 3 + Unit test; 5th U13 Quiz 2 + Unit test | 3.OA.D.9; 4.OA.C.5 (Khan: MOSTLY COVERED); 5.OA.B.3 | 

**Course challenge** (all courses, one each): 3rd `/math/cc-third-grade-math/test/x95ab04602940c446:course-challenge`,
4th `.../cc-fourth-grade-math/test/x0b5b2e23e6febb9a:course-challenge`,
5th `.../cc-fifth-grade-math/test/xe33ac28b798af866:course-challenge`,
6th `.../cc-sixth-grade-math/test/x0267d782:course-challenge`,
7th `.../cc-seventh-grade-math/test/x6b17ba59:course-challenge`,
8th `.../cc-eighth-grade-math/test/x7c7044d7:course-challenge`,
Algebra 1 `/math/algebra/test/x2f8bb11595b61c86:course-challenge`.
Which skills each challenge samples: **UNVERIFIED**.

**Main finding.** Khan teaches rows 2, 3, 4 and 1 (as equations) only in grades 7-8 and Algebra 1, as formal algebra.
The grade 3-5 courses have no arithmetic or bar-model version of "trade it", age, or sum-and-difference. Row 5 starts
in 6th grade. Only rows 6 and 7 (and a weak form of row 1) are taught on grade for a 3rd/4th grader. So for rows 1-5
the sheets in this repo teach the method; Khan is the "where does this go in the formal course" reference.

## Per kid: on grade vs above grade

**Musa (3rd grade, works 4th-grade math).**
- On grade (3rd): row 7 patterns (3.OA.D.9), row 6 missing factors/dividends (3.OA.A.4), 2-step word problems
  (3.OA.D.8, the nearest Khan skill to row 1).
- Next grade (4th, Khan has it): multi-step word problems with equations (4.OA.A.3), patterns with a rule (4.OA.C.5).
- Above grade, Noetic asks early: row 1 chained operations with unknown start (Khan: 7th), row 2 (8th),
  row 3 (8th), row 4 (no exercise), row 5 (6th).

**Yusuf (4th grade homeroom, IM Grade 5 at school).**
- On grade (4th): multi-step word problems (4.OA.A.3), patterns (4.OA.C.5). On his IM Grade 5 track: Khan's
  5th-grade course Unit 13 "Algebraic thinking" (expressions with parentheses, rules that relate 2 variables).
  The IM Grade 5 Khan course has no algebraic-thinking unit; its patterns exercises sit in Unit 7 (see below).
- Above grade, Noetic asks early: row 5 averages (6th), row 2 trade-it (8th formal), row 3 age (8th), row 1 (7th).
  His Noetic misses #2 (row 2), #4 (row 3) and #5 (row 5) are all above grade on Khan.

## Per-course detail

Each unit lists the relevant exercises in order. `Q` = quiz, `UT` = unit test. Exercise names are copied from the course page.

### 3rd grade (cc-third-grade-math) 14 units, 142 skills
`/math/cc-third-grade-math` (also an IM version, below).
- **U3 Addition, subtraction, and estimation** (`/imp-addition-and-subtraction`): Find the missing number (add and
  subtract within 1000); Missing number for 3-digit addition / subtraction within 1000; UT.
- **U7 More with multiplication and division** (`/imp-multiplication-and-division`): Find missing factors (1-digit
  multiplication); Find missing divisors and dividends (1-digit division); Multiplication and division word problems
  (within 100); Q1; ...; UT. (CCSS 3.OA.A.3, 3.OA.A.4.)
- **U8 Arithmetic patterns and problem solving** (`/arithmetic-patterns-and-problem-solving`): Solve 2-step
  expressions; 2-step estimation word problems; Represent 2-step word problems with equations; 2-step word problems;
  **Q1**; Math patterns; Patterns with even and odd; Patterns in hundreds chart; Patterns in multiplication tables;
  **Q2**; UT. (3.OA.D.8, 3.OA.D.9.)
- U10 Area has "Find a missing side length when given area"; U11 Perimeter has missing-side items. Geometry, not these skills.

### 3rd grade, IM aligned (3rd-grade-illustrative-mathematics) 7 units
`/math/3rd-grade-illustrative-mathematics`. Same exercises, regrouped.
- U1 Introducing multiplication: Find missing factors (1-digit multiplication).
- U3 Wrapping up addition and subtraction within 1,000: Find the missing number; Two-step add and subtract word
  problems; Represent 2-step word problems with equations; 2-step word problems; Q6; UT.
- U4 Relating multiplication to division: Find missing divisors and dividends; Solve 2-step expressions; UT.

### 4th grade (cc-fourth-grade-math) 14 units
`/math/cc-fourth-grade-math`.
- **U3 Multiply by 1-digit numbers**: Compare with multiplication; Compare with multiplication word problems
  ("times as many", 4.OA.A.1-2). Q1, UT.
- **U5 Division** (`/division`): Multiplication and division word problems; 2-step estimation word problems;
  **Represent multi-step word problems using equations**; **Multi-step word problems with whole numbers**; **Q4**; UT.
  (4.OA.A.3.)
- **U6 Factors, multiples and patterns**: Patterns with numbers; Patterns with shapes; **Q3**; UT. (4.OA.C.5.)
- No missing-number or average exercise in 4th grade.

### 4th grade, IM aligned (4th-grade-illustrative-mathematics) 8 units
`/math/4th-grade-illustrative-mathematics`. U6 "Multiplying and dividing multi-digit numbers" holds Patterns
with numbers, Represent multi-step word problems using equations, Multi-step word problems with whole numbers
(Q9), and the UT. U5 "Multiplicative comparison and measurement" holds Compare with multiplication word problems.

### 5th grade (cc-fifth-grade-math) 16 units
`/math/cc-fifth-grade-math`.
- **U13 Algebraic thinking** (`/imp-algebraic-thinking`): Evaluate expressions with parentheses; Translate
  expressions with parentheses; Create expressions with parentheses; **Q1**; Rules that relate 2 variables; Tables
  from rules that relate 2 variables; Graphs of rules that relate 2 variables; Extend patterns; Relationships
  between 2 patterns; **Q2**; UT. (5.OA.A.1-2, 5.OA.B.3.)
- No missing-value, age, or mean exercise in 5th grade. U4 and U5 are the fraction and multi-digit units
  already pinned in `AGENTS.md`.

### 5th grade, IM aligned (5th-grade-illustrative-mathematics) 7 units
`/math/5th-grade-illustrative-mathematics`. This is Yusuf's school course. **No algebraic-thinking unit.**
The patterns and rules exercises (Rules that relate 2 variables, Extend patterns, Relationships between 2
patterns) sit in **U7 Shapes on the coordinate grid**. Course challenge: `.../test/xe7a2395079b692f7:course-challenge`.
Existing note on this course: bifrost `research/khan-academy-im-math-practice-2026-10-12.md`.

### 6th grade (cc-sixth-grade-math) 12 units; IM version: 6th-grade-illustrative-math
- **U6 Variables & expressions**: Evaluating expressions with variables word problems; Writing expressions with
  variables; Q1-Q3; UT.
- **U7 Equations & inequalities** (`/cc-6th-equations-and-inequalities`): Testing solutions to equations;
  Identify equations from visual models (tape diagrams); (hanger diagrams = balance picture); Solve equations from
  visual models; One-step addition & subtraction equations; One-step multiplication & division equations; **Q1**;
  Find the mistake in one-step equations; Translate one-step equations and solve; Model with one-step equations
  and solve; **Q2**; UT. (6.EE.B.7.)
- **U11 Data and statistics** (`/cc-6th-data-statistics`): Calculating the mean; Calculating the median;
  **Missing value given the mean**; Effects of shifting, adding, & removing a data point; **Q2**; UT. (6.SP.B.5.c.)
- IM version: the same "Missing value given the mean" sits in its U8 "Data sets and distribution" (UT there).

### 7th grade (cc-seventh-grade-math) 9 units; IM version: 7th-grade-illustrative-math
- **U6 Expressions, equations, & inequalities** (`/cc-7th-variables-expressions`): Writing expressions word
  problems; Q1; **Two-step equations**; Two-step equations with decimals and fractions; Find the mistake: two-step
  equations; Interpret two-step equation word problems; **Two-step equations word problems**; **Q2**; one- and
  two-step inequalities; Q3; UT. (7.EE.B.4.a: the standard text says to compare an algebraic solution with an
  arithmetic one and name the sequence of operations. This is the "undo the steps" idea in formal dress.)

### 8th grade (cc-eighth-grade-math) 7 units; IM version: 8th-grade-illustrative-math
- **U2 Solving equations with one unknown**: Equations with variables on both sides; Equations with parentheses;
  Number of solutions; Sums of consecutive integers; Q1, Q2, UT. (8.EE.C.7.)
- **U4 Systems of equations** (`/cc-8th-systems-topic`): Solutions of systems; Systems with graphing; **Systems of
  equations with substitution**; **Q1**; Number of solutions (graphically, algebraically); **Age word problems**;
  **Systems of equations word problems**; **Q2**; UT. (8.EE.C.8.b-c.) The standards page lists "Systems of
  equations with substitution: potato chips" and "Setting up a system... (pet weights)" under 8.EE.C.8.
- IM Grade 8: same exercises in Unit 4 "Linear equations and linear systems" (Age word problems under lesson 9,
  substitution under lessons 13-14, systems word problems before Q4 and the UT).

### Algebra 1 (algebra) 17 units; IM version: algebra-1-illustrative-math (8 units)
- **U2 Solving equations & inequalities**: Reasoning with linear equations; Linear equations with unknown coefficients.
- **U6 Systems of equations** (`/x2f8bb11595b61c86:systems-of-equations`): Creating systems in context; **Q1**;
  Systems of equations with substitution; Combining equations; Elimination strategies; Systems with elimination;
  Reasoning with systems of equations; **Q2**; Age word problems; Systems of equations word problems; **Q3**; UT.
- IM Algebra 1: U2 "Linear equations and systems" holds Creating systems in context, substitution, elimination.
  It has no Age word problems exercise.
- U9 Sequences (arithmetic and geometric) covers "what rule" in formal form.

## Standards pages read (what each says Khan covers)
`/standards/CCSS.Math/` + `3.OA`, `4.OA`, `5.OA`, `6.EE`, `7.EE`, `8.EE`, `6.SP` (also `3.MD`, `4.NBT`, not used).
Coverage labels as Khan shows them: 3.OA.A.4, 3.OA.D.8, 3.OA.D.9, 4.OA.A.3, 5.OA.B.3, 6.EE.B.7, 7.EE.B.4.a,
8.EE.C.8.b-c, 6.SP.B.5.c all FULLY COVERED. 4.OA.C.5 (generate a pattern from a rule) is **MOSTLY COVERED**.
8.EE.C.8.c (age, systems word problems) is where the age exercise maps.

## Not covered or UNVERIFIED
- Row 4 (sum and difference): no named exercise anywhere. Treat as taught by this repo only.
- Rows 1-5 in grades 3-5: Khan has no exercise. Verified by reading every exercise name in the six 3rd-5th course
  pages (standard and IM). A name-only search can miss an item inside a differently named exercise; the contents
  of exercises and quizzes were not opened.
- Quiz and test contents, course-challenge coverage, and K-2 equal-sign lessons: UNVERIFIED.
- Khan courses change. Re-render before citing a link older than a school year.
