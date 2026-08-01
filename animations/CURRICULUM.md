# 4th + 5th grade — the whole inventory, and what each topic needs to draw

Every Common Core standard for grades 4 and 5, mapped to **the drawing surface it
needs**. Written because "cover everything" is 45 standards, and the useful question is
not *how many* but *how few distinct surfaces they collapse into*.

**They collapse into six.** Two of them already exist.

| Surface | What it is | Status |
|---|---|---|
| **`grid`** | digit tokens at (row, col) — the column algorithms, exactly as on paper | ✅ **built** |
| **`parts`** | a rectangle cut into named parts — the area model | ✅ **built** (multiplication) |
| **`line`** | a number line with labelled ticks and a moving marker | ❌ |
| **`plane`** | first-quadrant coordinate grid | ❌ |
| **`figure`** | free-positioned shapes, angles, unit cubes | ❌ |
| **`tree`** | a nested expression that collapses inward-out | ❌ |

The two that exist are not small. `grid` covers every base-ten algorithm in both grades.
`parts` — built to explain why `47 × 36` has two rows — is **the same surface fraction
multiplication needs**, which is the single cheapest high-value extension on this page.

---

## Priority is not mine to invent

[`PRACTICE-PLAN-2026.md`](../PRACTICE-PLAN-2026.md) § Target board already names what
these two kids need, and says which two to protect if the plan slips:

> Protect these two: **remainder interpretation** (kid1) and **unlike denominators**
> (kid2). Both are genuinely new methods, not bigger numbers.

So the build order below is **led by the target board**, not by standard number. A topic
neither kid needs this summer is worth building only when it is nearly free.

| On the target board | Standard | Surface | Status |
|---|---|---|---|
| kid1 — multi-digit × then add/sub | 4.NBT.B.5 | `grid` | ✅ **done** |
| kid1 — **division with remainders, interpreting them** | 4.NBT.B.6 | `grid` | ⚠️ algorithm done, *interpretation* not |
| kid1 — two-step problems, four operations | 4.OA.A.3 | `tape` → `tree` | ❌ |
| kid1 — **equivalent / comparing fractions** | 4.NF.A.1, 4.NF.A.2 | `parts` + `line` | ❌ |
| kid1 — **area / perimeter, missing side** | 4.MD.A.3 | `figure` | ❌ |
| kid2 — 2-digit × 2-digit | 4.NBT.B.5 | `grid` | ✅ **done** |
| kid2 — long division w/ remainder | 4.NBT.B.6 / 5.NBT.B.6 | `grid` | ✅ **done** |
| kid2 — **fractions, unlike denominators** | 5.NF.A.1 | `parts` | ❌ |
| kid2 — **decimals, compare + add/sub** | 5.NBT.A.3, 5.NBT.B.7 | `grid` + `line` | ❌ |
| kid2 — multi-step rate problems | 5.NF.B.6 | `tape` | ❌ |

**Six of the ten are already-built surfaces or one surface away.**

---

## The full inventory

Legend — ✅ built · 🔜 same surface as something built · ❌ needs a new surface

### 4.OA — Operations & Algebraic Thinking

| Std | Topic | Surface | |
|---|---|---|---|
| 4.OA.A.1 | Multiplication as comparison (35 is 5 times as many as 7) | `tape` | ❌ |
| 4.OA.A.2 | Multiplicative-comparison word problems | `tape` | ❌ |
| 4.OA.A.3 | Multi-step problems, **interpreting remainders** | `tape` | ❌ |
| 4.OA.B.4 | Factors, multiples, prime/composite | `parts` (rectangles per factor pair) | 🔜 |
| 4.OA.C.5 | Generate a pattern from a rule | `line` | ❌ |

### 4.NBT — Base Ten

| Std | Topic | Surface | |
|---|---|---|---|
| 4.NBT.A.1 | A digit is 10× the place to its right | `grid` | 🔜 |
| 4.NBT.A.2 | Read / write / compare multi-digit | `grid` | 🔜 |
| 4.NBT.A.3 | **Rounding** to any place | `line` | ❌ |
| 4.NBT.B.4 | Add / subtract multi-digit (**regrouping**) | `grid` | 🔜 **cheapest real win** |
| 4.NBT.B.5 | Multiply | `grid` | ✅ |
| 4.NBT.B.6 | Divide w/ remainder | `grid` | ✅ |

### 4.NF — Fractions

| Std | Topic | Surface | |
|---|---|---|---|
| 4.NF.A.1 | **Equivalent fractions** — why (n×a)/(n×b) works | `parts` | 🔜 |
| 4.NF.A.2 | **Comparing** fractions | `parts` + `line` | 🔜 |
| 4.NF.B.3 | Add / subtract, like denominators; mixed numbers | `parts` | 🔜 |
| 4.NF.B.4 | Fraction × whole number | `parts` | 🔜 |
| 4.NF.C.5 | Tenths + hundredths | `parts` | 🔜 |
| 4.NF.C.6 | Decimal notation for fractions | `parts` + `grid` | 🔜 |
| 4.NF.C.7 | Compare decimals | `line` | ❌ |

### 4.MD — Measurement & Data

| Std | Topic | Surface | |
|---|---|---|---|
| 4.MD.A.1 | Unit conversion | `tape` | ❌ |
| 4.MD.A.2 | Measurement word problems | `tape` | ❌ |
| 4.MD.A.3 | **Area / perimeter, missing side** | `figure` | ❌ |
| 4.MD.B.4 | Line plots with fractions | `line` | ❌ |
| 4.MD.C.5 | Angles as a fraction of a circle | `figure` | ❌ |
| 4.MD.C.6 | Measure / sketch angles | `figure` | ❌ |
| 4.MD.C.7 | Adding angle measures | `figure` | ❌ |

### 4.G — Geometry

| Std | Topic | Surface | |
|---|---|---|---|
| 4.G.A.1 | Points, lines, rays, angles, parallel / perpendicular | `figure` | ❌ |
| 4.G.A.2 | Classify 2D figures | `figure` | ❌ |
| 4.G.A.3 | Line symmetry | `figure` | ❌ |

### 5.OA — Expressions & Patterns

| Std | Topic | Surface | |
|---|---|---|---|
| 5.OA.A.1 | **Parentheses / order of operations** | `tree` | ❌ |
| 5.OA.A.2 | Write and read expressions | `tree` | ❌ |
| 5.OA.B.3 | Two patterns → ordered pairs → graph | `plane` | ❌ |

### 5.NBT — Base Ten

| Std | Topic | Surface | |
|---|---|---|---|
| 5.NBT.A.1 | 10× and 1/10 across places | `grid` | 🔜 |
| 5.NBT.A.2 | Powers of 10 | `grid` | 🔜 |
| 5.NBT.A.3 | Read / compare decimals to thousandths | `grid` + `line` | 🔜 |
| 5.NBT.A.4 | Round decimals | `line` | ❌ |
| 5.NBT.B.5 | Multiply multi-digit | `grid` | ✅ |
| 5.NBT.B.6 | Divide, 2-digit divisor | `grid` | ✅ |
| 5.NBT.B.7 | **Decimal + − × ÷** | `grid` | 🔜 |

### 5.NF — Fractions

| Std | Topic | Surface | |
|---|---|---|---|
| 5.NF.A.1 | **Unlike denominators** ← protected | `parts` | 🔜 |
| 5.NF.A.2 | Estimating with benchmarks | `line` | ❌ |
| 5.NF.B.3 | a/b means a ÷ b | `parts` | 🔜 |
| 5.NF.B.4 | **Fraction × fraction** | `parts` | 🔜 ← *the same area model already built* |
| 5.NF.B.5 | Multiplication as scaling | `line` | ❌ |
| 5.NF.B.6 | Real-world fraction multiplication | `tape` | ❌ |
| 5.NF.B.7 | Dividing unit fractions | `parts` | 🔜 |

### 5.MD — Measurement & Data

| Std | Topic | Surface | |
|---|---|---|---|
| 5.MD.A.1 | Unit conversion | `tape` | ❌ |
| 5.MD.B.2 | Line plots + operations | `line` | ❌ |
| 5.MD.C.3 | Volume by unit cubes | `figure` | ❌ |
| 5.MD.C.4 | Measuring volume | `figure` | ❌ |
| 5.MD.C.5 | V = l × w × h, additive volume | `figure` | ❌ |

### 5.G — Geometry

| Std | Topic | Surface | |
|---|---|---|---|
| 5.G.A.1 | Coordinate plane | `plane` | ❌ |
| 5.G.A.2 | Graphing real-world problems | `plane` | ❌ |
| 5.G.B.3 | Attributes of 2D categories | `figure` | ❌ |
| 5.G.B.4 | Hierarchy of 2D figures | `figure` | ❌ |

---

## The count that matters

| | standards |
|---|---|
| ✅ Already animated | 4 |
| 🔜 Reachable on a **surface that already exists** | 18 |
| ❌ Need a new surface | 23 |

**22 of 45 need no new drawing surface.** That is the argument for extending `grid` and
`parts` before building anything new — and for building `line` third, since it alone
unlocks 8 more.
