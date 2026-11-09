# Financial Algebra integration plan

The Financial Algebra repository is the separate build-and-test environment for a future new course at [Mr. K's Classroom](https://mrksclassroom.com/). The production \`akneller1/classroom\` repository must remain untouched while this course is in development.

## Current production interfaces examined

- \`data.js\`: \`window.LIBRARY.courses\` contains courses, units, artifacts, and paths.
- \`app.js\`: Routes course/unit pages, generator cards, Games/Study Guides/Interactive Math groups.
- \`course-catalog.js\`: Stable skills generated as \`unitId-skill-01\`, etc.
- \`question-bank-adapter.js\`: Schema v1 of approved question banks with cp2/cp1/honors internal levels.
- \`question-bank-loader.js\`: Loads approved banks from a manifest.
- \`styles.css\`: Course/unit styling (copied into this standalone project).
- \`artifacts/interactive-math/lab.js\` and \`lab.css\`: Interactive Math shell, controls, charts, and challenges. Copies included here.
- Worksheet Generator and Assessment Readiness Check CSS copied from \`worksheet-generator/\`.

## Stable standalone IDs

Course ID: \`financial-algebra\`.
Pilot unit IDs: \`budgeting\`, \`credit\`, \`investing\`.

**One difficulty only:** All Financial Algebra question APIs are a single standard level. Do not reintroduce CP2/CP1/Honors controls. Production adapters currently require one of the legacy level names in bank JSON, so a later import adapter may have to write an internal compatibility tag while hiding differentiation from students and teachers, or extend the adapter's schema safely. Do not change other courses' levels.

## Later integration

1. Review pilot activities with a teacher. Confirm finance facts, accessibility, print layout, and assumptions.
2. Expand scenario banks and decision-based tasks, including rubrics and explanations.
3. Preserve skill IDs. Build an adapter to export approved questions in the production schema without converting one public level into three.
4. Wrap each interactive tool with its local worksheet and teacher guide in separate \`artifacts/financial-algebra-*/\` folders.
5. Add the course on a **staging branch** of the production repository; run full site tests and inspect generators, navigation, assets, answer keys, and student links.
6. Integrate only after explicit approval.

No production code was changed during this standalone development.
