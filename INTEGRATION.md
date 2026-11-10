# Integrating new courses into Mr. K's Classroom

This repository is a separate staging area. Production is akneller1/classroom, which must remain untouched while new courses are developed.

## Financial Algebra baseline

- Financial Algebra is **outline only**. All early pilot simulators, finance calculators, worksheet and assessment prototypes, practice tests, and printable materials have been removed from this staging repository.
- The ten unit IDs and forty proposed skill labels remain stable.
- Course ID: financial-algebra.
- One course level: standard. No CP2/CP1/Honors choices for this subject.
- Generators, Games, Study Guides, and Interactive Math are non-clickable Coming soon placeholders.
- See FINANCIAL_ALGEBRA_ACTIVITY_HANDOFF.md for Claude's activity-planning brief.

## Production interfaces to preserve

- data.js and app.js: course metadata, routing, activity cards and generators.
- course-catalog.js: skill ID convention, e.g. budgeting-skill-01.
- question-bank-adapter.js and question-bank-loader.js: approved question-bank schema and manifest.
- styles.css: Classroom visual framework.
- artifacts/interactive-math/lab.js and lab.css: interactive math framework **in the production repository**. Their previous copies were removed here with the pilots.

## Integration sequence

Plan course activities; prepare and test question families; implement and validate stage-only activities; adapt to the production schema; connect on a staging branch of production; run all existing course and student-view regression tests; request approval before merging to the live site.

The financial curriculum must make interest, payment timing, return assumptions, rounding, and uncertainty explicit. Do not collect real student financial data.

No production changes were made as part of this cleanup.
