# 5th Grade Math: validation report (2026-11-11)

Everything below was actually run in this workspace against the repository with the Grade 5 changes applied. "Not tested" items are listed at the end.

## Content checks

| Check | Command | Result |
|---|---|---|
| Independent math verification of every answer, distractor and visible number | `python3 tools/grade5-authoring/verify.py` | **0 errors**, 11 warnings (some skill/levels draw from 3–4 question families instead of 5+; counts are still 30) |
| Notation lint through the site renderer (32,413 strings) | `node tools/grade5-authoring/tests/display-lint.cjs` | **0 issues** |
| Structure, counts, links, diagrams, thumbnails | `node scripts/test-grade5.cjs` | **PASS** — 4,950 questions (1,650 per level), 918 diagrams, every resource link and thumbnail resolves |
| Cheat-sheet examples and Try It answers evaluated in Node; page overflow | `python3 tools/grade5-authoring/build_content.py`, `node scripts/cheat-sheets/build.cjs …` | 66 checks passed, 11 sheets built, **0 overflow** |
| Standards coverage | `python3 tools/grade5-authoring/report.py` | **34 / 34** Grade 5 standards (100%), each at all three levels |

## Repository tests (Node)

All 53 `scripts/test-*.cjs` and `worksheet-generator/menu/*.test.cjs` files were run. 51 pass in one batch run. The other two:

- `scripts/test-course-parity-browser.cjs` timed out under load in the batch run. It **passes** run alone: "666 complete game and future-course parity scenarios".
- `scripts/test-escape-unit-ciphers.cjs` **fails on the unmodified baseline too** (no Escape Room themes for `discrete/*` and `statistics/*`). A math5-only copy of the test passes: 11 unique themes, and 660 unit-aligned cipher questions across 8 courses.

Grade 5 specific results from the shared suites:

- `MG_COURSE=math5 MG_PREFIX=m5- node scripts/test-grade-bank-integration.cjs`: 11 flashcard players, 11 vocabulary banks, **0 printable failures**, 165 lesson plans, 165 skill/level selections, 33 game decks, 231 printable builds.
- `scripts/test-tarsia-all-courses.cjs`: 306 passed, 0 failures (the line-plot unit needed four new short, diagram-free question families to fill an 18-piece Tarsia; added and re-verified).
- `scripts/test-standards.cjs`: 922 skills mapped, all checks passed (Grade 5 descriptions added).
- `scripts/test-public-site.cjs`, `scripts/test-dynamic-routing.cjs` (after `node scripts/build-site.mjs`): pass — 11 courses, 102 unit pages, 117 routed views, no broken rendered links.

## Browser tests (Playwright, Chromium)

`node tools/grade5-authoring/tests/browser-grade5.cjs` — **165 passed, 0 failed**:

- 10 games × every applicable unit (102 runs, including Math Quest in whole-class mode and Math Race with 4 teams): each launched, was played **to its end screen** by a bot that answers from the question shown, and no correct answer was marked wrong. Puzzle Masters was solved by matching every pair.
- Understanding Check, 11 units × 3 modes (one at a time with immediate feedback, one at a time with feedback at the end, all on one page): a fully correct run scores 8/8; blank runs score 0 and offer "Retry missed questions"; the teacher summary appears in teacher view.
- Flashcards, 11 units: flip (Space), next (→), Got it progress, shuffle, card-type filter, print layout with pictures.
- Interactive tools, 7: load, zoom and Fit controls, Student/Teacher view (teacher notes with worksheet and key links), every button clicked without errors.
- Unit pages, course page + 11 units: all local links resolve, all thumbnails load.

The repository's own browser tests (with a static server on port 8765) pass: `test-browser-smoke` (34 passed), `test-approved-browser`, `test-browse-activities-browser`, `test-course-parity-browser`, `test-legacy-review-browser`, `test-slope-golf-browser`, `test-unit-specific-arcade-browser`, `test-algebra2-integration-browser`, `test-algebra2-printable-browser`.

Generators opened in the browser for a Grade 5 unit with no console errors: Worksheet, Assessment, Understanding Check (printable), Lesson Planner, Printables (maze, Tarsia, stations), Millionaire, Vocabulary, Showdown.

## Fixed during validation

- Puzzle Masters: revealed text overflowed onto neighboring cards (now wraps inside the card).
- Math Soccer: with two strong teams the ball could go back and forth forever. A correct answer now keeps possession; a miss is a turnover.
- Site catalog rewrote Grade 5 flashcard, Connect 4 and Picture Reveal links (and one project link) into the generic player; Grade 5 items now keep their own links (`keepPath`), and team games are tagged "Team Games".
- Project hero images were rendered at the wrong size (artwork in one corner); cropped.

## Not tested

- Real printing on paper (PDF layout was checked on screen and by the cheat-sheet overflow check only).
- Screen-reader walkthroughs (ARIA labels, live regions and keyboard paths were written in but not tested with NVDA or VoiceOver).
- Phones and tablets on real devices (layouts include small-screen rules; tested at desktop size).
- Word and PowerPoint files for projects were not opened in Microsoft Office.
- A teacher's review of the mathematics for grade-level fit. Answers are machine-verified; wording and difficulty were spot-checked by sampling.
