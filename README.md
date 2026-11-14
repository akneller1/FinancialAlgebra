# Mr. K's Classroom — Independent Course Development

**Staging website:** https://akneller1.github.io/FinancialAlgebra/  
**Live production website:** https://mrksclassroom.com/

This repository is a separate development space for creating new math classes using the Mr. K's Classroom design, before importing finished courses into production.

## Courses

| Class | Staging page | Curriculum status |
| --- | --- | --- |
| Financial Algebra | [Staging](https://akneller1.github.io/FinancialAlgebra/) | 10 units; question banks and resources available |
| Grade 5 | [Staging](https://akneller1.github.io/FinancialAlgebra/grade5.html) | 11 published units; question banks available |
| Grade 4 | [Staging](https://akneller1.github.io/FinancialAlgebra/grade4.html) | 10 published units; question banks available |
| Grade 3 | [Staging](https://akneller1.github.io/FinancialAlgebra/grade3.html) | 11 published units; question banks available (original 8-unit outline retained for reference) |
| Grade 2 | [Staging](https://akneller1.github.io/FinancialAlgebra/grade2.html) | 12 published units; question banks available |
| Grade 1 | [Staging](https://akneller1.github.io/FinancialAlgebra/grade1.html) | 12 published units; question banks available |

Production imports reviewed commit pins through `classroom/.github/workflows/deploy-site.yml`. Staging changes do not update those pins automatically. Original curriculum outlines can have different unit counts from the published bank catalogs. Grade 5 retains its original 13-unit outline for reference.

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
