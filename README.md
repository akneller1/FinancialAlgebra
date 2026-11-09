# Financial Algebra — Independent Course Development

**Live classroom site:** https://mrksclassroom.com/ (unchanged)

**Financial Algebra development preview:** https://akneller1.github.io/FinancialAlgebra/

The independent project now uses the **actual Mr. K's Classroom course CSS and shared Interactive Math framework**, not a separately designed calculator dashboard. The new Financial Algebra course will ultimately be imported into the original site only after quality review and approval.

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
