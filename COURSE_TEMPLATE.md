# Reusing this staging site for future math classes

The FinancialAlgebra GitHub repository now also hosts the **Grade 5 Math** curriculum outline, reusing the same classroom styling. The repository name still reflects its original Financial Algebra pilot, but its layout can host further development courses.

## Current development pages

- Financial Algebra: \`index.html\` · live pilot activities
- Grade 5 Math: \`grade5.html\` · **released reference implementation** with 11 teaching units, approved-bank manifest, games, generators, study guides, interactive tools, and projects; the original 13-unit pacing outline remains available
- Grade 1 Math: \`grade1.html\` · Illustrative Mathematics, sections and standards
- Grade 2 Math: \`grade2.html\` · Illustrative Mathematics, sections and standards
- Grade 3 Math: `grade3.html` · outline only, standards and guiding questions
- Grade 4 Math: \`grade4.html\` · outline only, with pacing and source objective categories
- All development source stays in this repository; the public Classroom site assembles **only released course files** into its Pages artifact.

## How to add another course

1. Convert the attached scope-and-sequence document into a single JSON file under \`course-outlines/<slug>.json\`. Preserve unit order, exact lesson boundaries, and any source standards. Note pages where the text continues or contains ambiguities.
2. Follow the \`course-outlines/grade5.json\` schema: \`schemaVersion\`, \`id\`, \`name\`, \`description\`, \`status\`, \`source\`, \`standards\` map, and \`units\` with \`id\`, \`name\`, \`status\`, \`skills\`, \`standards\`, and \`sourcePages\`.
3. Create a small course page (use \`grade5.html\` as the base) loading the common \`styles.css\`, \`site-overrides.css\`, and its own tiny bootstrap file (like \`src/grade5-site.js\`) calling \`mountOutline(course)\` from \`src/outline-template.js\`.
4. Add a link in the navigation for both development course pages. New course IDs must be unique and compatible with the eventual production course catalog.
5. Write tests matching the source document's unit and skill counts, topic order, standards references, page continuations and stable IDs.
6. Only after teacher review, begin adding authentic question families and activity integrations. Never show disabled tools as if they already work.

## Standard unit card — Geometry design (all present and future courses)

All course landing pages must use the Geometry-style `unit algebra-unit-card` pattern. This includes Grades 1–5, Financial Algebra, and every new class staged here and later published to Mr. K’s Classroom.

- Keep the three-column responsive `ul.units` grid, course-specific tint, dark outlined rounded cards, and shadow.
- Show `Unit N`, the unit title, up to four real curriculum lesson/skill names as bullet points, and an `Open unit →` link anchored at the bottom.
- With more than four lessons, include accessible `details.unit-lesson-details` and an expandable `Show all N lessons` / `Show fewer lessons` control. Never list fake lesson names.
- Do not put activity counts, thumbnail strips, games, resource inventories, or development badges inside the unit cards. These belong on the unit page or in page-level notices.
- Use `src/outline-template.js` for outline-only grades, the established Grade 5 renderer for ready Grade 5 content, and the shared Classroom renderer on production. When integrating, add accurate course-unit skill arrays to the Classroom catalog so cards never display blank lesson previews.
- Do not create per-course unit-card layouts or conditionals: future courses inherit the common format.

## Stable content contract

The skill ID for item index \`i\` (zero-based) in a unit is \`<unit-id>-skill-<two-digit-number>\`. Example: \`place-value-skill-01\`.

That ID pattern is intentionally consistent with the existing Classroom \`course-catalog.js\` convention. **Do not rename established IDs when Claude produces question banks**. Use each unit's \`id\` unchanged, and include the matching \`courseId\` (\`math5\`) on each question.

The staging site's outline renderer and CSS may be reused without copying any Financial Algebra-specific simulations. Avoid mixing financial content into other grade levels.

## Grade 5 release-quality checklist for Grades 1–4

Grade 5 is the reusable **implementation pattern**, not a blanket certification of each
question's editorial quality. The main site's publishing workflows validate the real
generated output (not only the source repository). Follow all of these gates for future grades:

1. **Curriculum integrity:** preserve the sourced pacing outline and standards. Keep stable unit and skill IDs, sensible age-appropriate level labels, and an explicit mapping between the original pacing sequence and the released teaching units.
2. **Question quality:** validate every answer independently; run difficulty, uniqueness, notation, diagrams/alt text, and worked-solution checks. Grade 5 contains 4,950 questions across three levels. Release after the existing automated checks pass; investigate reported issues as they arise. No exhaustive human-review gate is required.
3. **Activity coverage:** for each ready unit ensure real clickable games, lesson plan/worksheet/activity/assessment generators, flashcards, a cheat sheet, an age-appropriate understanding check, and at least one project. Include interactive manipulatives where they genuinely improve the lesson, not merely to fill a quota.
4. **Navigation:** every teacher resource needs usable home/course/unit return links; student links must preserve unit, level, and skills without exposing teacher-only notes. Keep compatibility redirects for old paths when renaming landing pages.
5. **Publishing:** build new grades here first. Do not show them on the public site until separately approved. Keep source files in their own repository; assemble only allowlisted course runtime, bank/manifest entries, diagrams, thumbnails, linked assets, and redirects into the public Pages artifact.
6. **Regression tests:** require the public release audit to find zero missing resource URLs, unloaded games, broken diagrams, orphan assets, missing banks, or dead internal navigation. Run real-browser checks for each game engine, course-page return flow, generator, study guide, interactive page, and project. Block releases on failures.
7. **Document exceptions:** list editorial review remaining, any untested device/browser combinations, or quality gaps explicitly. Source-code checks and static link checks do not replace a teacher play-through in a real classroom.

## Publishing into main Classroom

`akneller1/classroom` is the site assembly/deployment repository. It runs
`scripts/integrate-approved-courses.mjs` to incorporate released Grade 5 files from
this separate development repository; the source files **do not move** into Classroom.
The single canonical `Deploy site` workflow publishes the finished site.
The independent `Verify unified Mr. K's Classroom site` workflow is a validation-only gate
and must never race the deploy job. For Grade 4 and younger, keep development work
off the public site until approved for release and wired through the same QA gates.


## Preloaded resource engines (2026-11-12)

All Grade 1–4 outlines automatically inherit `src/elementary-resources.js` through
`src/outline-template.js`. Do not copy the Grade 5 engines or write per-grade game pages.
Each unit receives nine general games, the four teacher generators, six activity formats,
flashcards and a Readiness Check. Fraction Frenzy is reserved for fraction units.
Teacher generators include ordered mixed question groups, editable lesson sections,
difficulty/skill selection, spacing, versions, review, previews, and separate teacher keys.
There are no student-share controls in generators.

`worksheet-generator/elementary-resource.html` loads the selected outline and the actual
Grade 5 runtime. All requests use the outline's `math1`/`math2`/`math3`/`math4` ID, existing
unit IDs and `<unit-id>-skill-NN` IDs. Missing banks never fall back to Grade 5 questions.
The generator settings remain usable with an empty bank; handouts wait for real questions.

To activate a unit, add a schemaVersion 1 bank at
`question-banks/mathN/<unit-id>.json`, then register it in the root `manifest.json` with
`courseId`, `unitId`, `path`, and `approved:true` after automated verification. Preserve the
stable skill IDs and levels `cp2`, `cp1`, `honors` (Remedial, Standard, Advanced). The same
entry activates games, practice flashcards and checks. Include accessible image diagrams
and worked solutions; add optional misconception metadata at `mathN/meta/<unit-id>.meta.json`
for written error-analysis activities. New lesson vocabulary/objectives may be supplied
in the outline's unit `generatorContent` field; no Grade 5 instructional content is borrowed.

Run `npm test` and `node scripts/test-grade5.cjs` after changes. Curated vocabulary decks,
cheat sheets, projects and unit-specific manipulatives remain authored curriculum work.
Preloading does not promote unfinished grades into the main production website.
