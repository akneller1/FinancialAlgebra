# Integrating new courses into Mr. K's Classroom

This repository is a separate staging area. Production is akneller1/classroom, which must remain untouched while new courses are developed.

## Financial Algebra resources

The complete resource library is integrated into the ten unit pages. Each unit links to native generators, a Decision Lab and teacher view, study guides, and project packets. The single visible course level is Standard. Exported Classroom banks use `cp1` solely for schema compatibility; they are not connected to production games.

See `FA_INTEGRATION_MANIFEST.md` and `financial/resources.json` for resource paths and rebuild instructions. Grades 1–5 remain independent outlines. The removed pilot files remain absent.

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
