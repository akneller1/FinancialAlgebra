# Grade 5 authoring tools

Source for the 5th Grade Math (`math5`) banks, diagrams, flashcards, cheat sheets, tools and projects. Python 3 + Node; `rsvg-convert` and `pngquant`/Pillow for diagrams; Playwright for PDFs and browser tests.

| File | Purpose |
|---|---|
| `outline.py` → `outline.json` | Single source of truth: 11 units, 55 skills, standards per skill, the 34 Grade 5 standards. |
| `g5lib.py` | Problem toolkit: `Item`, number formatters, answer checks (`EX`, `KEY`, `FN`), distractor helpers, derived formats (error analysis, true/false, select-all, open response, matching). |
| `figs.py` | SVG diagram generators (fraction bars and circles, number lines, rulers, place-value charts, base-ten blocks, area models, arrays, coordinate planes, shapes, prisms, cubes, line plots, tables). |
| `units/u01…u11_*.py` | Question families per unit; `SKILLS` maps each skill to its families. |
| `build.py [module …]` | Builds `question-banks/math5/<unit>.json`, `meta/<unit>.meta.json`, diagrams in `question-banks/assets/math5/<unit>/`, and `out/<unit>.checks.json`. 30 questions per skill and level (12 short answer, 12 multiple choice, 3 error analysis, 1 true/false, 1 select-all, 1 open response or matching). Blocks exact and near duplicates across the course. `G5_NODRAW=1` skips diagram rendering. |
| `verify.py` | Independent verifier: re-reads the published text, recomputes every answer with its own math (about 70 checkers), checks that stored distractors are wrong, that numbers in a check appear in the problem, diagram files, duplicates and counts. Must print `TOTAL ERRORS 0`. |
| `tests/display-lint.cjs` | Renders every string through `worksheet-generator/core/math-display.js` and flags notation problems (stray italics, ASCII minus, broken fractions). |
| `tests/browser-grade5.cjs` | Playwright: plays every game to completion with a bot that answers correctly, runs the Understanding Check in each mode, flashcards, tools and unit pages, failing on console errors. `G5_ONLY=games|checks|cards|tools|units`, `G5_GAME=<id>`, `--quick`. |
| `content_g5.py`, `build_content.py` | Vocabulary, concept and visual flashcards, cheat-sheet content (with checked examples) and the MATH5 vocabulary block. |
| `interactive/` | Interactive Math tool pages and their worksheet/teacher-key PDFs. |
| `projects/` | Project content (`projects.py`) and builder (`build.py`) for PDF, Word, PowerPoint, teacher guide, page, hero and thumbnail. |
| `print/print.cjs` | Headless Chromium printer used by the builders. |
| `integration.cjs` | Applies every shared-file edit (data.js, app.js, catalog, manifest, planner, generators…) by anchor; safe to re-run. |
| `report.py` | Writes `docs/math5/COVERAGE.md` and `.csv` from the published bank. |
| `sample.py` | Prints random items for human review. |

Typical rebuild:

```bash
cd tools/grade5-authoring
python3 build.py                 # or: python3 build.py u05_fraction_add
python3 verify.py
node tests/display-lint.cjs
python3 build_content.py
node ../../scripts/cheat-sheets/build.cjs math5-place-value-number-sense   # one per unit, or "all"
python3 report.py
cd ../.. && node tools/grade5-authoring/integration.cjs && node scripts/test-grade5.cjs
```

Rendering conventions used in every string (the site renderer is strict): × and ÷ symbols, U+2212 minus, `a/b` fractions (stacked by the renderer), superscript exponents, U+2011 non-breaking hyphen inside words, measurement units spelled out (the renderer italicizes one- and two-letter words such as `kg`).
