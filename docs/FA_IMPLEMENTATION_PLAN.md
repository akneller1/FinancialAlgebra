# Financial Algebra — Implementation Plan & Decisions

## Curriculum coverage
The ten units and forty skill IDs in `src/course.js` are unchanged (`<unit>-skill-01…04`, course `financial-algebra`, one level `standard`). Essential concepts that the skill names do not state explicitly are taught **inside** the closest existing skill rather than by adding skills:

| Concept added | Where it lives |
|---|---|
| Emergency funds, sinking funds, 50/30/20, needs vs. wants | Budgeting skills 1–3; Banking skill 3 |
| Pay frequencies, overtime, commission, benefits / total compensation | Income skills 1–2 |
| Overdrafts, ATM fees, FDIC/NCUA insurance, liquidity, CDs | Banking skills 1, 3 |
| Credit scores, utilization, cash advances, balance transfers, avalanche/snowball | Credit skills 3–4 |
| Leasing (money factor, residual), Truth in Lending disclosures, negative equity | Borrowing skills 2, 4 |
| Fees/expense ratios, diversification, volatility, real return | Investing skills 3–4 |
| 28/36 affordability, PMI, closing/selling costs, equity | Housing skills 1, 3, 4 |
| Liability limits, auto coverages, self-insuring, HSAs | Insurance skills 1, 4 |
| FAFSA, aid offers, subsidized vs. unsubsidized, completion risk | College skills 1, 2, 4 |
| Employer match, vesting, Roth vs. traditional, CPI | Retirement skills 1, 3 |

**Recommendation (optional, not implemented):** if the course ever adds skills, the strongest candidates are *Taxes & filing (W-2/1040 basics)* in Unit 1 and *Identity theft & fraud protection* in Unit 3.

## Architecture
```
financial/
  lib/finance.js        deterministic finance engine (FA_MATH) — browser + Node
  lib/render.js         shared renderers (FA_RENDER): questions, tables, fictional documents, rubrics, stacked fractions
  lib/fa.css            components on top of Classroom styles.css tokens
  content/<unit>.mjs    authored source: vocabulary, concept items, claims, parameterized families, lessons, cheat sheet, extra flashcards
  content/projects/     unit projects (+ capstone) as data
  banks/<unit>.json     extended bank (schema fa-bank-1) used by FA generators
  generators/           Lesson Plan · Worksheet (8 formats) · Assessment (20/20/30/30) · Practice Test
  decision-lab/         reusable 7-step Decision Lab engine + 10 unit scenarios
  flashcards/           flip-card app + decks.js + MKVOCAB drop-in
  resources.json        integration manifest (every resource path by unit)
  index.html            staging hub listing all resources
question-banks/financial-algebra/<unit>.json   Classroom schemaVersion 1 export
artifacts/financial-algebra-*                   cheat sheets (PDF/HTML) and projects (PDF, DOCX, PPTX, landing page)
scripts/                build-banks.mjs · build-print.mjs · build_office.py · build-hub.mjs
tests/                  fa-finance.test.mjs · fa-content.test.mjs · fa-browser.cjs (+ fixtures/ production adapter copy)
```

### Question-bank design
- **Source of truth is code, not hand-typed items.** Each family is a seeded generator (`rng(unit:family:k)`), so builds are reproducible and every number is computed by `finance.js`. Variation comes from different people, employers, products, documents, and situations, not only numbers.
- **Extended schema (`fa-bank-1`)** per item: `id, unitId, skillId, level, type (vocabulary|concept|scenario|comparison|document|calculation|reasoning|claim), format, prompt, scenario {title,text,table,document}, options, answer, numeric {value,tolerance,unit}, solutionSteps, parts, modelResponse, rubric, misconceptions, activityTypes, gameEligible, family`.
- **Classroom export** (schemaVersion 1) passes the **unchanged** production `question-bank-adapter.js`. Decision: the single Financial Algebra level is stored as `level: "cp1"` because the production schema only allows cp2/cp1/honors and the site already labels cp1 as "Standard" for Math 6/Pre-Algebra. Only short, game-suitable MC/short-answer items, select-all items, and ≥4-part open responses are exported; long document items stay in the extended bank.
- **Fictional documents**: pay stubs, bank/credit statements, aid offers, Truth in Lending boxes, loan schedules, Loan Estimates, Summaries of Benefits, investment and 401(k) statements — all rendered by one generic, accessible renderer.
- **Stated assumptions**: Course Tax Table (illustrative), 7.65% FICA, 5% flat state tax, 6.25% sales tax, card interest = balance × APR ÷ 12, minimum = 1% + interest (≥ $25), hypothetical returns. Every page carries a fictional/illustrative notice.

### Grading philosophy
Numeric answers are verified deterministically (tolerance per item). Written reasoning is never auto-graded: every open response ships a model response and a 4-criterion rubric that explicitly accepts alternative defensible conclusions.

### Display convention
Division is shown as a stacked fraction (`[[a || b]]` markup and `a ÷ b` patterns render as numerator over a bar over denominator). Word/PowerPoint exports fall back to "÷", never "/".

## Development record
1. Inspected both repos (course.js, site.js, production adapter/loader/schema, games bridge, artifact folder conventions, project packaging).
2. Built finance engine, kit, render layer; built **Budgeting & Spending** as the reference unit (bank, lessons, cheat sheet, lab, two projects) and validated it in a browser.
3. Scaled to the other nine units with the same structure; added one project per unit and a capstone.
4. Automated validation (Node + Playwright), then packaged.
