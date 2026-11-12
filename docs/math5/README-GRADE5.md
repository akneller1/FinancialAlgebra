# 5th Grade Math (`math5`): integration instructions

This package adds a complete Grade 5 course to Mr. K's Classroom. Every path in the ZIP is relative to the repository root, so integration is: unzip over a clean checkout of the same baseline, review the diff, run the checks below and commit.

Baseline: `akneller1/classroom` at the commit this work started from (`git log -1` in the repository at packaging time). If the target branch has moved, re-run the integration script instead of copying the modified shared files by hand (see "If the baseline has moved").

## What is included

| Area | Files |
|---|---|
| Question banks (4,950 questions: 1,650 per level, 30 per skill and level) | `question-banks/math5/*.json`, `question-banks/math5/meta/*.meta.json`, `question-banks/assets/math5/**` (918 PNG diagrams) |
| Course record, skills, manifest | `data.js`, `course-catalog.js`, `question-banks/manifest.json` (11 entries, `approved: true`) |
| Games (10 games, 6 engines, solo and whole-class modes) | `worksheet-generator/grade5-games.html`, `worksheet-generator/grade5/g5-games.js` |
| Understanding Check | `worksheet-generator/grade5-understanding-check.html`, `worksheet-generator/grade5/understanding-check.js`; printable version uses the existing `practice-test.html` (label changed to "Understanding Check" for math5) |
| Flashcards (226 cards with SVG pictures) | `worksheet-generator/grade5-flashcards.html`, `worksheet-generator/grade5/flashcards.js`, `worksheet-generator/grade5/flashcards/*.json` |
| Shared Grade 5 runtime and theme | `worksheet-generator/grade5/g5-core.js`, `worksheet-generator/grade5/g5.css` |
| Cheat sheets (11, elementary theme) | `scripts/cheat-sheets/content/math5-*.cjs`, `artifacts/math5-*-cheat-sheet/worksheet.pdf`, `scripts/cheat-sheets/style.cjs` (adds the `theme: "elementary"` style; other courses unchanged) |
| Interactive Math tools (7) | `artifacts/math5-{place-value-builder,area-model-explorer,fraction-explorer,expression-builder,measurement-converter,volume-builder,coordinate-explorer}/` (page, worksheet PDF, teacher key PDF), `worksheet-generator/grade5/{tool-shell.js,g5-figs.js,g5-tools.css}` |
| Projects (11, one per unit) | `artifacts/math5-project-*/` (Remedial/Standard/Advanced PDF, Word, PowerPoint; teacher guide PDF and Word with worked example, answer keys and rubric), registry entries in `worksheet-generator/menu/printables-projects.js` |
| Vocabulary (102 terms) | `worksheet-generator/vocabulary-data-middle-grades.js` (block between `MATH5-VOCAB-START` and `MATH5-VOCAB-END`) |
| Thumbnails | `thumbs/math5-*` |
| Escape Room themes and cipher problems | `worksheet-generator/games/escape-themes.json` (11 themes), `worksheet-generator/games/cipher-questions.js` (11 Grade 5 problem families) |
| Standards | `worksheet-generator/menu/standards.js` (Grade 5 descriptions), `worksheet-generator/menu/standards-map.js` (rebuilt), `massachusetts-framework-strands.js` |
| Authoring source, verifier and tests | `tools/grade5-authoring/**`, `scripts/test-grade5.cjs` |
| Reports | `docs/math5/COVERAGE.md`, `docs/math5/COVERAGE.csv`, `docs/math5/VALIDATION_REPORT.md` |

## Changes to existing shared files

All of these were applied by `tools/grade5-authoring/integration.cjs` (idempotent; anchors are checked) unless noted.

| File | Change |
|---|---|
| `data.js` | 5th Grade Math course record (color `sunshine`, art `fifth`, placed before 6th Grade) and one resource block (`/* 5th Grade Math (2026-11-11) ... */`) after the precalculus/calculus `planned=false` line. Grade 5 resources carry `keepPath: true`; games also carry `gameMode`. |
| `course-catalog.js` | `math5` skill catalog (11 units, 55 skills, standards per skill). |
| `question-banks/manifest.json` | 11 approved math5 entries. |
| `resource-standards.js` | One line: `if(a.keepPath)return null;` so Grade 5 links (flashcards, Connect 4, Picture Reveal, a project whose folder contains "showdown") are not rewritten into the generic course-game player. No effect on items without `keepPath`. |
| `app.js` | Course order, `fifth` art, math5 in the course lists, unit-card icon, a Projects resource group, Grade 5 level labels, and one line in `gameMode()`: `if (a.gameMode) return a.gameMode;`. |
| `styles.css` | `sunshine` course color. |
| `index.html`, `activity.html` | Cache-version strings. |
| `coverage.html`, `skills.html` | math5 added to course lists. |
| `resource-details.js` | Cheat-sheet details for the 11 units. |
| `massachusetts-framework-strands.js` | 11 grade-level strand records (5.NBT, 5.OA, 5.NF, 5.MD, 5.G). |
| `scripts/build-site.mjs` | SEO text for the new course. |
| `scripts/cheat-sheets/style.cjs` | `ECSS` elementary theme, applied only when `theme === 'elementary'`. (manual) |
| `worksheet-generator/algebra2-bank-native.js`, `menu/course-catalog-bridge.js`, `menu/match-game.js`, `games/course-activity.js`, `course-game.html`, `approved-flashcards.html`, `vocabulary-builder.js`, `practice/practice.js` | math5 added to course lists, Remedial/Standard/Advanced labels (`math[56]`), "Understanding Check" label for math5 in the practice test. |
| `worksheet-generator/planner/{course.js,planner-ui.js,scope-algebra2.js}` | Lesson planner scope for math5 (`MATH5`, prefix `M5`). |
| `worksheet-generator/menu/printables-projects.js` | 11 project registry entries. |
| `worksheet-generator/menu/standards.js`, `standards-map.js` | Grade 5 standard descriptions; map rebuilt with `node scripts/build_standards_map.cjs`. (manual) |
| `worksheet-generator/games/escape-themes.json`, `games/cipher-questions.js` | 11 Escape Room themes and Grade 5 cipher problem families (whole-number answers 1–25, no negatives). (manual) |
| `worksheet-generator/vocabulary-data-middle-grades.js` | MATH5 vocabulary block (written by `tools/grade5-authoring/build_content.py`). |

Test expectations updated because the catalog grew from 10 to 11 courses (91 → 102 units, 764 → 819 skills, 85 → 96 projects): `scripts/test-public-site.cjs`, `scripts/test-dynamic-routing.cjs`, `scripts/test-coverage-report.cjs`, `scripts/test-browser-smoke.cjs`, `scripts/test-approved-flashcards.cjs`, `worksheet-generator/menu/course-catalog-bridge.test.cjs` (also accepts grade-5 strand codes `5.XX`).

## Checks to run after integrating

```bash
node scripts/test-grade5.cjs                                   # math5 structure, links, diagrams, 30 per skill/level
python3 tools/grade5-authoring/verify.py                       # independent math re-check of every answer (expects TOTAL ERRORS 0)
node tools/grade5-authoring/tests/display-lint.cjs             # every string through the site math renderer (expects 0 issues)
MG_COURSE=math5 MG_PREFIX=m5- node scripts/test-grade-bank-integration.cjs
node scripts/test-published-question-banks.cjs
node scripts/test-tarsia-all-courses.cjs
node scripts/test-standards.cjs
node scripts/build-site.mjs && node scripts/test-public-site.cjs && node scripts/test-dynamic-routing.cjs
# browser (needs a static server on 127.0.0.1:8765 for the repo's own browser tests):
python3 -m http.server 8765 &
node tools/grade5-authoring/tests/browser-grade5.cjs          # plays every game to the end, Understanding Check, flashcards, tools, unit pages
node scripts/test-browser-smoke.cjs && node scripts/test-course-parity-browser.cjs && node scripts/test-browse-activities-browser.cjs
```

Note: `scripts/test-course-parity-browser.cjs` and `scripts/test-algebra2-integration-browser.cjs` rewrite `thumbs/previews/**` screenshots as a side effect. Discard those changes (`git checkout -- thumbs/previews`) unless you mean to refresh previews.

Known pre-existing failure, unchanged by this package: `scripts/test-escape-unit-ciphers.cjs` fails on the baseline because `discrete/*` and `statistics/*` units have no Escape Room themes. The math5 part of that test passes (checked with a math5-only copy of the test).

## If the baseline has moved

1. Copy the new (untracked) files from the ZIP.
2. Run `node tools/grade5-authoring/integration.cjs`. It re-applies every shared-file edit by anchor and stops with a clear message if an anchor is missing.
3. Re-apply the manual edits listed above (`style.cjs`, `standards.js` + `node scripts/build_standards_map.cjs`, `escape-themes.json`, `cipher-questions.js`, test expectations) by comparing with the ZIP copies.
4. Run the checks.

## Rebuilding content

See `tools/grade5-authoring/README.md`. In short: `python3 build.py` (banks and diagrams), `python3 verify.py`, `python3 build_content.py` (flashcards, vocabulary, cheat-sheet content), `node scripts/cheat-sheets/build.cjs math5-<unit>` (PDFs), `python3 report.py` (coverage report).

## Privacy and network

No student accounts and nothing is stored about students. The Grade 5 pages make no network requests beyond the site's own files; teacher summaries are shown on screen only (copy/print buttons). Only per-browser display zoom is kept in `localStorage`.
