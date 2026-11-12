# Mr. K's Classroom — Independent Course Development

**Staging website:** https://akneller1.github.io/FinancialAlgebra/  
**Live production website:** https://mrksclassroom.com/ (not modified)

This repository is a separate development space for creating new math classes using the Mr. K's Classroom design, before importing finished courses into production.

## Courses

| Class | Staging page | Curriculum status |
| --- | --- | --- |
| Financial Algebra | [Course outline](https://akneller1.github.io/FinancialAlgebra/) | 10 units, 40 skills; complete Financial Algebra resource library |
| Grade 5 | [Grade 5](https://akneller1.github.io/FinancialAlgebra/grade5.html) | 13 units, 80 skills, sourced from the uploaded sequence |
| Grade 4 | [Grade 4](https://akneller1.github.io/FinancialAlgebra/grade4.html) | 12 units, 107 editorial learning targets, pacing and objectives |
| Grade 3 | [Grade 3](https://akneller1.github.io/FinancialAlgebra/grade3.html) | 8 units, standard-aligned goals and guiding questions |
| Grade 2 | [Grade 2](https://akneller1.github.io/FinancialAlgebra/grade2.html) | 9 Illustrative Mathematics units, 25 source-named sections |
| Grade 1 | [Grade 1](https://akneller1.github.io/FinancialAlgebra/grade1.html) | 8 Illustrative Mathematics units, 27 source-named sections |

Financial Algebra unit pages link to lesson plans, eight worksheet formats, assessments, practice tests, ten Decision Labs, 228 flashcards, ten cheat sheets, and twelve projects. The 1,445-item extended bank powers the native resources; 1,274 compatible questions are also exported for future Classroom games integration. Games are not published here. Grades 1–5 remain course outlines with Coming soon shortcuts.

## Design and icons

The staging pages use the main Classroom visual system from styles.css, with narrowly scoped overrides in site-overrides.css.

Grades 1–5 have distinct vector icons in assets/course-icons, visible in the course navigation and on the course/unit banners:
- **Grade 1:** blue counting beads
- **Grade 2:** gold base-ten rods and unit blocks
- **Grade 3:** teal multiplication array
- **Grade 4:** coral geometric shapes
- **Grade 5:** pink fraction circle

The reusable outline renderer is src/outline-template.js. The Financial Algebra outline page is src/site.js and uses a finance-specific banner illustration.

## Content-development handoffs

- Financial Algebra activity planning: [FINANCIAL_ALGEBRA_ACTIVITY_HANDOFF.md](FINANCIAL_ALGEBRA_ACTIVITY_HANDOFF.md).
- Grade-level question banks: GRADE1_BANK_HANDOFF.md through GRADE5_BANK_HANDOFF.md.
- Stable course IDs: financial-algebra, math1, math2, math3, math4, math5.
- Preserve all unit IDs and unit-id-skill-XX identifiers. The Financial Algebra course uses **one level** (standard); do not extrapolate this constraint to elementary grades.
- Claude may author plans and supply modular ZIP files; ChatGPT reviews and integrates finished files into this staging repository. The production site stays untouched until the user approves integration.

## Validation

Run npm test on Node.js 20+ (the GitHub workflow runs it and checks JavaScript syntax). Pages deploys from main at repository root.

## Elementary generators

Use the full Algebra 1 teacher engines for every new grade, as documented in [the elementary generator standard](docs/ELEMENTARY_GENERATORS.md). Grade 5 production routes all four teacher generators to the shared Classroom engines; the local Grade 5 generator remains a development fallback. Do not add student links to teacher generators.
