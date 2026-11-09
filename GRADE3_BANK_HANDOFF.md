# Grade 3 Mathematics — Question-bank handoff

**Status:** Curriculum outline only. Questions and interactive tools are not yet authored.

## Source and identifiers
- Source document: [3rd Grade Mathematics Scope & Sequence](https://resources.finalsite.net/images/v1652384560/carrollk12org/q67evpht5bth0b4vor14/3rdGradeMathematicsScopeandSequence.pdf) (14 pages).
- Curriculum data: `course-outlines/grade3.json`; course ID: `math3`.
- Eight units, preserving source order and approximate school-year months.
- Stable skill IDs: `<unit-id>-skill-01`, `-02`, etc.
- Source standards (e.g. `3.OA.1`, `3.NBT.2`, `3.NF.3`, `3.MD.7`) are retained in the course data and displayed.
- Learning-target labels and abbreviated guiding questions are editorial summaries of the source, not claims of publisher lesson names.

## Instructions for Claude
1. Read `course-outlines/grade3.json` and inspect `akneller1/classroom`'s current bank manifest, question schema, unit labels, and sample question families.
2. Author modular, **verified** Grade 3 question banks, covering all saved skill IDs without changing their order.
3. Use visual arrays, area models, number lines, basic fraction models, tables, scaled graphs, geometry diagrams, measurement tools, and word problems where appropriate.
4. Maintain source scope: multiplication/division within 100, 3-digit addition/subtraction within 1000, rounding to tens/hundreds, beginning fractions, unit squares, length measurements to halves/quarters of inches, and time to the minute.
5. Produce original problem contexts and deterministic answers with worked explanations. Check age appropriateness, invalid distractors, near-duplicates, and game compatibility.
6. Use the production site's normal difficulty system when authoring; the single-level policy belongs to Financial Algebra, not necessarily elementary classes.
7. Deliver a structured ZIP plus manifest and automated validators. Do not claim to write directly to GitHub; ChatGPT will review and integrate files.
8. Keep the main `akneller1/classroom` website untouched pending separate approval and regression tests.

**Important:** In the source, Unit 1 includes review material referenced as `2.G.2`; retain this rather than silently deleting it.
