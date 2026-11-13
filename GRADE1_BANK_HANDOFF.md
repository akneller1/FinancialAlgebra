# Grade 1 Mathematics — Question Bank Development Handoff

**Status:** Shared Grade 5 game, generator, flashcard and readiness-check engines are preloaded for every unit in staging. Question banks have not been authored; these resources display a pending-bank state.

## Authoritative source

- [Illustrative Mathematics Grade 1: Scope and Sequence](https://im.kendallhunt.com/k5/teachers/grade-1/course-guide/scope-and-sequence.html)
- Source publisher: Illustrative Mathematics / Kendall Hunt; source text is presented under Creative Commons Attribution 4.0 (do not copy source illustrations without verifying their individual rights).
- Structured curriculum: `course-outlines/grade1.json` in repository `akneller1/FinancialAlgebra`.
- Stable course ID: **`math1`**; 8 units, 27 source-named sections, and 93 editorial learning targets.
- Original unit titles and section headings are preserved in source order, with standard alignment codes and estimated pacing ranges.
- The `skills` labels are **paraphrases for future item generation**; they are not copied textbook lesson titles. `sections[*].skills` maps directly to the flattened `units[*].skills`.
- A skill ID is `<unit-id>-skill-01` (one-based, two-digit index), e.g. `adding-subtracting-working-data-skill-01`. Do not rename these without a migration plan.

## Work for Claude

1. Inspect this JSON before generating any content; compare its IDs and sections with `akneller1/classroom` production course catalogs and a proven original question bank.
2. Author an ample range of age-appropriate, **original** item families for each skill. Use concrete contexts, story types, diagrams, models, number lines, and correctly labeled graphs. Prefer reusable generators with verified outputs to repeated near-identical questions.
3. Avoid overreaching into later grades. Follow source number ranges, units, measurement conventions, and fractions/arrays as appropriate to Grade 1.
4. Support multiple forms of assessment: objective answers, short numerical explanations, visual interpretation, and structured teacher rubrics for reasoning.
5. Include deterministic answer checking, solutions, test fixtures, uniqueness checks, and rendering guidance for diagrams and accessibility.
6. Verify compatibility with the approved question schema and all activities before marking a section usable. Do not force word-problem or open-response families into games requiring simple numeric answers.
7. Deliver complete modular bank files, a manifest, and automated validation results as a ZIP. **Claude cannot modify the GitHub repositories directly in this workflow.**
8. Keep all student-facing activities unavailable until the bank is reviewed and integrated in staging. Do not modify `akneller1/classroom` production until explicitly approved after regression testing.

## Implementation notes

The shared course outline component is `src/outline-template.js`; course entry page is `grade1.html`; bootstrap is `src/grade1-site.js`. Grade 1 is independent of Financial Algebra's one-level policy. No payment, third-party API, or AI inference at run time is required.


## Current integrated interface

Use Grade 5 on `mrksclassroom.com/#grade5` as the model. The development build
now uses the real main Classroom shell and native generators, assembled by
`scripts/assemble-classroom-preview.mjs`. Do not develop against the older
standalone Grade 5 generator UI. Source IDs stay `mathN`; the build adapts them
to `gradeN` for the native engines, using the same process as integrated Grade 5.
