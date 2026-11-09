# Integration contract: Financial Algebra → Mr. K's Classroom

The pilot must be developed here first. Integration into \`akneller1/classroom\` should occur later through a separate, reviewed staging branch and regression tests; never edit the main site while experimenting.

## Existing classroom interfaces (inspected 2026-11-08)

- Course metadata: \`data.js\` stores \`window.LIBRARY.courses\` with \`id\`, \`name\`, \`color\`, \`art\`, \`units\`, \`artifacts\`.
- Course router: \`app.js\` includes a course order map and course handling.
- Skills: \`course-catalog.js\` maps course + unit IDs to skill strings, creating \`unitId-skill-01\`, etc.
- Question banks: \`question-bank-adapter.js\` expects \`schemaVersion:1\`, \`courseId\`, \`unitId\`, \`questions\`, and for each item \`id\`, \`skillId\`, \`level\` (cp2,cp1,honors), \`format\` (short-answer,multiple-choice,select-all,open-response), \`prompt\`, \`answer\`, \`solutionSteps\`.
- Bank loader: \`question-banks/manifest.json\` approves entries by course/unit for student-facing use.

## Stable identifiers

Use \`financial-algebra\` as the **course ID**, regardless of the repository's capitalization. Pilot unit IDs are \`budgeting\`, \`credit\`, and \`investing\`. Do not change these once content is authored.

## Future integration workflow

1. Confirm the curriculum and grade-level expectations with a teacher.
2. Expand and independently validate question families and nuanced financial assumptions; add written justification rubrics.
3. Produce a separate export tool converting verified parameterized items into the classroom bank schema, retaining skill IDs, answer explanations, and checked solutions.
4. Wrap each standalone simulation as an independently routable \`artifacts/financial-algebra-*/index.html\` tool with responsive styling and a worksheet + teacher key.
5. Add a course entry, course-catalog skill map, activity links, and the approved bank manifest on a **new staging branch** of \`akneller1/classroom\`.
6. Run site-wide regression tests for existing courses, generators, printable pages, games, student links, and deployment paths; merge only after explicit approval.

Do not merely rename prototype files and expect automatic compatibility. User-facing generators have their own constraints, including multi-part open responses and activity-specific rendering. Reuse math engines, authored content, and styles, while adapting the interfaces.

## Security and accuracy

- No secret teacher keys may be assumed private on a static public GitHub Pages site.
- Financial statements and investment returns are hypothetical unless verified otherwise.
- Use deterministic, independently tested calculations with explicit compounding, payment timing, tax, and rounding assumptions.
- Do not use student financial data in published examples.
