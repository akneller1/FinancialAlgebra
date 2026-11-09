# Financial Algebra — Independent Course Development

**Live classroom site:** https://mrksclassroom.com/ (unchanged)

**Financial Algebra development preview:** https://akneller1.github.io/FinancialAlgebra/

The independent project now uses the **actual Mr. K's Classroom course CSS and shared Interactive Math framework**, not a separately designed calculator dashboard. The new Financial Algebra course will ultimately be imported into the original site only after quality review and approval.

## New: Grade 3 Mathematics (outline-only staging)

**[Open Grade 3](https://akneller1.github.io/FinancialAlgebra/grade3.html)**

Eight units in source order, covering multiplication/division, multi-digit addition/subtraction, fractions, measurement, area, geometry, and computational fluency. Standards, guiding questions, unit dates and learning targets are included. No live question banks or activities yet; see `GRADE3_BANK_HANDOFF.md`.

## New: Grade 4 Mathematics (outline-only staging)

**[Open the Grade 4 course outline](https://akneller1.github.io/FinancialAlgebra/grade4.html)**

- Based on the user's supplied 15-page \`Grade4ScopeandSequence.pdf\` (\`Math Expressions Grade 4 – Scope and Sequence\`).
- Preserves all **12 units in sequence** plus each unit's estimated instructional days and reported textbook lesson count.
- Summarizes the source learning objectives as **107 source-based learning targets**; the attached document does **not** provide individual lesson titles, so these targets must not be mistaken for the book's numbered lessons.
- Each unit includes categorized source objectives and page references. Original notes to skip lessons **3.2** and **8.5** are preserved.
- Uses the shared classroom design/renderer, with games and generators clearly marked Coming soon.
- JSON data: \`course-outlines/grade4.json\`. Claude handoff: \`GRADE4_BANK_HANDOFF.md\`.

## New: Grade 5 Mathematics (outline-only staging)

**[Open the Grade 5 course outline](https://akneller1.github.io/FinancialAlgebra/grade5.html)**

- Based on the user's attached four-page \`Grade_5_Math_Scope_and_Sequence.pdf\`, retaining **all 13 units and all 80 listed skills** in their instructional order.
- Reuses the original Classroom course cards, expandable unit skills, unit headers, next/previous navigation, and generator shortcut visuals.
- Standards and eligible-content codes are available inside each unit, alongside source page references.
- Activities, question banks, lesson plans, and generators are **not yet built** and therefore are clearly marked Coming soon rather than linked to unrelated tools.
- JSON source of truth: \`course-outlines/grade5.json\`. The reusable outline renderer is \`src/outline-template.js\`.
- See \`COURSE_TEMPLATE.md\` to add more future classes and \`GRADE5_BANK_HANDOFF.md\` for later Claude question-bank development.

Financial Algebra remains fully available at \`index.html\`; the live \`akneller1/classroom\` production site is unchanged.

## What's built (pilot)

- Course overview and 10 unit outlines in the same visual design as the production site.
- **One Financial Algebra level for all learners** (no CP2/CP1/Honors options).
- Pilot units: Budgeting, Credit Cards, and Investing.
- For each pilot:
  - One Interactive Math activity with live graphs, adjustable sliders, reset, five "Try this" challenges, and a collapsible "What should I notice?" explanation.
  - Matching printable **Explore & Reflect** worksheet and teacher guide (HTML print or Save as PDF).
  - A Worksheet Generator with unit/skill selection, question count, preview, student/teacher versions, regenerate, and printing.
  - An Assessment Readiness Check with numbered questions, input and scoring, and worked solutions.
- Deterministic offline financial calculations and question scenarios; no AI, data feed, student account, or external service is needed at runtime.
- GitHub Actions tests run on every push.

## Layout and reusable pieces

- \`index.html\`, \`src/site.js\`, \`styles.css\`: Classroom course/unit navigation and copied design system.
- \`artifacts/interactive-math/lab.css\` and \`lab.js\`: Shared Interactive Math components copied from the main site.
- \`artifacts/financial-algebra-*-explorer/index.html\`: Unit-specific Interactive Math pages.
- \`src/finance-lab.js\`: Shared financial interactive behavior.
- \`src/engine.js\`: Deterministic budgets, installment payoff, and investing models.
- \`src/questions.js\`: Parameterized scenarios with one common level and checked math.
- \`worksheet.html\`, \`src/worksheet.js\`: Classroom-style worksheet generator.
- \`practice.html\`, \`src/practice.js\`: Classroom-style Assessment Readiness Check.
- \`print.html\`, \`src/print.js\`: Printable student and teacher reflection materials.
- \`shared/*\`: Original worksheet/practice design CSS copied from main Classroom.
- \`INTEGRATION.md\`: Future compatibility and migration plan.

## Development limits

This is still an early pilot, **not a finished course**. Lesson Planner, Activity Generator, Assessment Generator, Games, full Study Guides, and seven units are still incomplete, so their links are explicitly disabled. The working readiness check is separate from a configurable Assessment Generator. Numerical questions are currently short-answer only; rich decision scenarios and rubrics are future work.

All financial data are hypothetical. Credit uses a monthly rather than daily interest model; investing assumes a constant illustrative return and no taxes or fees. Teacher keys on a static public Pages site are not access-controlled.

## Testing

Use Node.js 20+ and run \`npm test\`. Github Actions checks calculations, generated answers, site components, and shared assets.

GitHub Pages requires Settings → Pages → Deploy from a branch → \`main\` / \`(root)\`.
