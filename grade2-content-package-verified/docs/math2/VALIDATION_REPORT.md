# 2nd Grade Math (math2): validation report

Run on 2026-11-13 against branch `grade2-content`. Every command below exited 0 unless noted.

| Check | Tool | What it does | Result |
|---|---|---|---|
| Standards | Published CCSSM Grade 2 text (Washington OSPI copy) | Checked the statement of every Grade 2 standard. The outline maps all of them, including 2.NBT.A.1 and its parts a and b | 28/28 covered (`COVERAGE.md`) |
| Answer correctness | `verify.py` + `checks2.py` | Checks the schema and the quotas (30/30/30 per skill). Re-computes every answer independently from the item's own check data, using ~130 named Grade 2 checks plus the Grade 3 and 5 checks: facts and missing numbers, parity, doubles, arrays, place value, number names, comparing, skip counting, ± 10/100, regrouping, story equations, rulers, tools, unit size, estimates, line plots, number-line jumps, clocks, AM/PM, coins (values from coin names), bills, graphs, polygon corners, solids and equal shares. Also re-checks that each distractor is wrong and that numbers used in a check are shown to the student. Looks for duplicates and near-duplicates and lints notation (plurals after 1, ASCII minus, broken values) | 4,770 questions, **0 errors, 0 warnings** |
| Understanding Checks | `VERIFY_CHECKS=1 verify.py` | Runs the same checks on the fixed sets | 318 items (2 per skill per level), **0 errors** |
| Content audit | `audit.py` | Family template audit with number ranges per level. Grade 2 scope limits: givens ≤ 20 in the fluency unit, ≤ 100 in the within-100 units, ≤ 1,000 elsewhere, arrays ≤ 5 × 5, no fraction notation. Also checks progression, reading demand, distractor reasons, and separation of checks from practice | **0 blocking**. 373 families. 99% of distractors carry a documented misconception reason. 0 prompts over 45 words. Checks repeat practice exactly 0 times, and use the same template with the same numbers 7 times. Every skill's Advanced level is more demanding than Remedial |
| Display | `tests/display-lint.cjs` | Runs every prompt, option and step through the site's `math-display.js` and flags words turned into italic variables, unstacked slashes and stray symbols | 31,149 strings, **0 issues** |
| Rendered review | Contact sheets of random diagrams per unit, viewed as images | Number lines with jumps, base-ten blocks, rulers, coins and bills, clocks, graphs, tally charts, arrays, partitions, solids and shapes on dot paper | Issues found were fixed (money layout width, “of one …” phrasing, articles such as “an eraser”, plurals) |
| Cheat sheets | Classroom `build.cjs` + overflow check | 12 two-page PDFs in the current elementary theme | 72 example checks, **0 overflow** |
| Projects | `print/print.cjs`, `tests/print-overflow.cjs` | 14 projects. Each has 3 student levels (PDF, DOCX, PPTX), a teacher guide with solutions and rubric, supports, a hero and thumbnails | 70 documents, 317 pages, **0 overflow**. Every answer is computed in `projects2.py` |
| Integrated preview | `assemble-classroom-preview.mjs` + patch | Builds the real Classroom shell with Grades 2 and 3 | 41 preloaded units (Grade 2: 12) |
| Browser | `tests/browser-grade2.cjs` | Unit pages, every game for every unit (including Monster Match on every unit), flashcards, Understanding Check in all views, student links and levels, with no console errors | **161 passed, 0 failed** |
| Generators | `tests/browser-generators.cjs --all` | Lesson planner, worksheet, assessment, maze, Tarsia, vocabulary and stations for all 12 units: preview content, levels, answer key, PDF export, and no student-link controls | **84 passed, 0 failed** |

## Limitations

- Conceptual items are checked against a stated rule, not derived from first principles. These are the best measuring tool (by benchmark length), estimates (within 35% of a benchmark), AM/PM for events (by event hour range), and fixed-text explanations.
- Reading level is measured by word count only; there is no formal readability score.
- The shared Understanding Check player does not read the fixed check sets yet (see INTEGRATION.md §5).
- The printable Understanding Check page (`practice-test.html`) was not exercised for Grade 2.
- No teacher review has taken place yet; the banks stay `approved:false`.
