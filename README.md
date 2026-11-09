# Financial Algebra — standalone development site

An independent Financial Algebra course for eventual integration into [Mr. K's Classroom](https://mrksclassroom.com/).

**Status: early pilot, not a complete course.** We copied the live Classroom course-page stylesheet and adapted its actual course overview, unit cards, lesson details, generator shortcuts, activity groups, and unit navigation. The working simulations and question generators live behind their corresponding resource cards, not on a different-looking dashboard.

## Open the preview

Enable GitHub Pages for main / (root), then visit:
- [Financial Algebra course page](https://akneller1.github.io/FinancialAlgebra/)
- [Budgeting unit](https://akneller1.github.io/FinancialAlgebra/#financial-algebra.budgeting)
- [Budgeting interactive lab](https://akneller1.github.io/FinancialAlgebra/lab.html#budgeting)

The separate development repository is [akneller1/FinancialAlgebra](https://github.com/akneller1/FinancialAlgebra). The live \`akneller1/classroom\` repository has **not** been modified.

## What currently works

- Ten-unit course overview with classroom-style unit cards, unit banners, lesson lists, next/previous navigation.
- Budgeting, Credit Cards, and Investing pilot units with interactive simulations and deterministic questions at CP2/CP1/Honors levels.
- Interactive practice, six-item printed student worksheets, and teacher keys.
- Financial math validation through GitHub Actions \`npm test\`.
- Same visual design system as the live site in \`styles.css\` (copied source), with minimal project-specific changes in \`site-overrides.css\`.

## What is explicitly still under development

Lesson Planner, Activity Generator, Assessment Generator, Games, complete Study Guides, all other seven units, curriculum validation, and full question coverage. The course pages show disabled “Coming soon” shortcuts rather than sending users to broken tools. Prototype keys are public and cannot be treated as access-controlled assessments.

## Project structure

- \`index.html\` + \`src/site.js\`: Classroom-style course/unit navigation.
- \`styles.css\`: copied live Classroom design CSS; \`site-overrides.css\` adds a unique course hue.
- \`lab.html\`, \`lab.css\`, \`src/app.js\`: original working financial calculators and practice.
- \`src/engine.js\`: deterministic models; \`src/questions.js\`: parametric question/answer generator.
- \`src/course.js\`: curriculum metadata and stable unit/skill identifiers.
- \`tests/\`: arithmetic, question, and parity assertions.
- \`INTEGRATION.md\`: future reviewed integration plan.

## Validation and accuracy

Run \`npm test\` on Node.js 20+. Current models simplify interest timing, tax withholding, and investment returns for teaching, and clearly state their assumptions. No real student financial data or external financial accounts are used. Runtime AI is not required.
