# 4th Grade Math: QA report (2026-11-13)

Everything below was run in this workspace on the development repository at `4bf5ca3` with this package applied, and on
the integrated preview assembled from production Classroom `e6ce580` by `scripts/assemble-classroom-preview.mjs`.
Automated checks and browser tests are listed separately. Items that were not tested are listed at the end.

## Curriculum

- 10 units, 49 skills, 35 Grade 4 standards (the 34 Common Core Grade 4 codes plus Massachusetts 4.OA.A.3.a). **35 of 35
  covered**, each at all three levels (`docs/math4/COVERAGE.md`, `.csv`).
- Explicitly covered: multiplicative comparison, multistep problems with remainders, factors and multiples, prime and
  composite, number and shape patterns, decimal fractions (tenths and hundredths), unit conversions, elapsed time, money,
  area and perimeter, angle measure (protractor, one-degree turns, additive angles), line plots with fractions, and
  classification of two-dimensional figures and symmetry.
- No Grade 5 content is presented as a Grade 4 requirement. Outline objectives from other grades (3-D figures,
  mean/median/mode, probability, coordinate graphing, decimal multiplication) are listed in `docs/math4/CROSSWALK.md`.

## Question banks — automated

| Check | Result |
|---|---|
| Independent verifier (`tools/grade4-authoring/verify.py`): recomputes every answer, every multiple-choice and select-all option, every open-response part and every true/false claim from stored check data with its own arithmetic; confirms stored distractors are wrong; numbers used by a check appear in the problem; diagrams exist with alt text | **4,410 questions, 0 errors, 0 warnings** |
| Notation lint (`tests/display-lint.cjs`): every student-facing string through the site's math renderer | **29,132 strings, 0 issues** |
| Schema and counts (`tests/grade4-course.test.mjs`) | unique IDs, valid skill IDs and levels, single correct option equals the key, solutions and standards present, 762 diagram files resolve, **exactly 30 per skill per level**, no exact duplicate questions |
| Formats | short answer 2,143 · multiple choice 2,001 · open response / matching 140 · select all 126 |
| Question types (metadata) | conceptual 1,050 · procedural 631 · visual 567 · multi-step 442 · error analysis 429 · word problem 334 · fill in the blank 283 · explain 228 · real-world 220 · true/false with reasons 127 · ordering 55 · compare strategies 33 · matching 11 |

Distractors carry the misconception they model (for example "added the denominators", "read the protractor from the
wrong end", "left out the zero in the quotient"), stored in the question metadata.

## Repository tests — automated

| Command | Result |
|---|---|
| `npm test` | **96 passed, 0 failed** (3 new Grade 4 tests; Grade 1–3, Grade 5, Financial Algebra and site tests unchanged and passing) |
| `scripts/assemble-classroom-preview.mjs` then `scripts/test-classroom-preview.cjs` | **PASS**: 35 units (Grade 4 approved, 25 Grades 1–3 units pending); Grade 4 native banks, games, guides, projects, vocabulary and planner teaching notes present; production generator and renderer files byte-identical to Classroom |

## Browser tests (Playwright, Chromium) on the assembled preview

| Test | Result |
|---|---|
| `browser-preview.cjs`: `/#grade4`, all 10 unit pages, every local link on every card, thumbnails, `grade4.html` redirect, Grade 5 and Financial Algebra still open | **14 passed, 0 failed** (no broken image, no 4xx) |
| `browser-grade4.cjs` with `G4_PREFIX=grade4/`: every game on every unit it is listed for, played **to its end screen** by a bot answering the shown question (no correct answer marked wrong); whole-class, team and partner modes; Understanding Check in each view and feedback mode on all units (scores, retry missed, printable results, teacher summary); flashcards on all units (flip, next, Got it, filter, shuffle); student links for a game and a check open straight into the configured level and skills | **140 passed, 0 failed** |
| `browser-tools.cjs`: 9 interactive tools at 1280×800, 1920×1080, 1024×600 and 390×780; real controls, readouts, challenges and reset; zoom and Fit scale the whole workspace; Present keeps picture **and** controls inside the window; student view hides teacher controls | **36 passed, 0 failed** |
| `browser-generators.cjs --all` with `G4_SET=grade4`: native Lesson Plan, Worksheet, Assessment and Activity (maze, Tarsia, vocabulary/crossword, stations) for all 10 units; preview holds this unit's questions; answer key; Remedial / Standard / Advanced labels; PDF export | **70 passed, 0 failed** |
| Unit-page "Copy student link" on a Grade 4 game | link copied; opens directly in the game in student view |

## Fixed during this pass

- Production renders projects only for Grade 5 and drops unknown card formats: Grade 4 team games and projects now use
  the formats the renderer lists, and the preview shows Projects for approved courses.
- The native lesson planner waits for course banks only for courses in its own list (Grade 5, not Grade 4), so the first
  day could be drawn before the banks loaded. Preview: a small redraw script. Production: one-line fix listed in
  `MIGRATION.md`.
- Planner objectives now read as sentences ("Students will be able to add multi-digit whole numbers with the standard
  algorithm"), from `tools/grade4-authoring/staging/objectives.json`.
- Browser test hook could miss the first question of a fast-starting game (a test race, not a game defect).

## Not tested

- Real printing on paper (PDF layout checked on screen and by page counts only).
- Screen readers (labels and live regions are present but not tested with NVDA or VoiceOver).
- Real phones, tablets and smartboards (tools tested at phone and projector sizes in Chromium; unit pages at desktop size).
- Word and PowerPoint project files were not opened in Microsoft Office.
- Production migration (not performed, by design).
- A teacher's review of every question for wording and grade-level fit. Answers are machine-verified; wording was
  spot-checked by sampling.
