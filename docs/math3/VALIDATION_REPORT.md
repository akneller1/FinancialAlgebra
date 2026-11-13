# 3rd Grade Math (math3) — validation report

Run on 2026-11-13 against branch `grade3-content`. Every command below exited 0 unless noted.

| Check | Tool | What it does | Result |
|---|---|---|---|
| Standards | Learning Commons (CCSS Multi-State) | Statement of every Grade 3 leaf standard looked up; outline maps all of them | 33/33 covered (`COVERAGE.md`) |
| Answer correctness | `verify.py` | Schema; quotas (30/30/30 per skill); independent re-computation of every answer from the item's own check data (`checks3.py`, ~90 named checks: arithmetic, rounding, unknowns, fractions/number lines, clocks/elapsed time, scales, pictographs/bars, rulers, area by shoelace, perimeter, shape classification, partitions); each distractor re-checked as wrong; numbers in the answer must appear in the prompt/diagram; duplicates/near-duplicates; lint (ASCII minus, "1 times", etc.) | 4,770 questions, **0 errors**, 79 warnings (mostly "only 3–4 families" at Remedial) |
| Understanding Checks | `VERIFY_CHECKS=1 verify.py` | Same checks on the fixed sets | 317 items, **0 errors** |
| Content audit | `audit.py` | Family template audit with parameter ranges per level; scope limits (products/quotients ≤ 100 in 3.OA units, givens ≤ 1,000, denominators 2/3/4/6/8); progression; reading demand; distractor reasons; check/practice separation | **0 blocking**; ~330 families; 99% of distractors carry a documented misconception reason; 7 prompts over 45 words (max 52); checks: 0 exact repeats of practice, 11 same template with same numbers; 1 progression flag (`properties-fact-strategies-skill-02`, metric artifact — Advanced adds missing-factor reasoning) |
| Display | `tests/display-lint.cjs` | Runs every prompt/option/step through the site's `math-display.js` and flags unwanted italics, unstacked fractions, stray symbols | 31,013 strings, **0 issues** |
| Rendered review | `sample.py` + visual inspection | Sample sheets of every unit/level with diagrams viewed as images; diagram labels drawn to scale (polygons, rulers, number lines, clocks, scales, graphs) | Issues found were fixed (label clipping, scale pointer at 0, off-scale polygons, unlabeled number lines) |
| Cheat sheets | classroom `build.cjs` + overflow check | 11 PDFs built with the current elementary theme | 66 checks, **0 overflow** |
| Projects | `print/print.cjs`, `tests/print-overflow.cjs` | 13 projects × (3 student levels + teacher guide + supports) | 293 pages, **0 overflow**; numbers in each project re-checked by hand-written solutions |
| Integrated preview | `assemble-classroom-preview.mjs` + patch | Assembled real Classroom shell with Grade 3 | 11 units, 214 resource cards |
| Browser | `tests/browser-grade3.cjs` | Unit pages, every game/flashcard/Understanding Check per unit, levels, cheat sheets/projects links, no console errors, no student links on generators | **151 passed, 0 failed** |
| Generators | `tests/browser-generators.cjs --all` | Native lesson/worksheet/activity/assessment generators for every unit, PDFs, levels, no student-link controls | **77 passed, 0 failed** |

## Limitations

- Conceptual multiple-choice items (definitions, "which strategy", shape attributes) are verified against their authored key and
  the shape classifier, not independently derived from first principles.
- Reading level is measured by word counts only; no formal readability score.
- The shared Understanding Check player does not yet read the fixed check sets (see INTEGRATION.md §5).
- No teacher review has occurred; banks stay `approved:false`.
