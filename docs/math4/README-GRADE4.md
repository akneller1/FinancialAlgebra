# 4th Grade Math (`math4`): integration README

Package for the development repository **akneller1/FinancialAlgebra**, built against commit `4bf5ca3`
("Preload native printable settings…", 2026-11-12 19:13). Production (**akneller1/classroom**) is not changed.

## Integrate (ChatGPT)

1. Unzip at the repository root of a clean checkout. Every path in the ZIP is repository-relative. No script needs to run:
   the files are already in their final state.
2. Review the diff. Seven existing files change (table below); everything else is new.
3. Run `npm test` (96 tests; 3 are new Grade 4 tests).
4. Build and check the integrated preview exactly as the deploy workflow does:
   ```bash
   git clone --depth 1 https://github.com/akneller1/classroom ../classroom
   CLASSROOM_SOURCE_DIR=../classroom node scripts/assemble-classroom-preview.mjs
   CLASSROOM_SOURCE_DIR=../classroom node scripts/test-classroom-preview.cjs
   ```
5. Optional browser checks (Playwright; serve `../classroom/_site` with `python3 -m http.server 8771`):
   ```bash
   G4_BASE=http://127.0.0.1:8771/ node tools/grade4-authoring/tests/browser-preview.cjs           # course + unit pages, links, thumbnails
   G4_SITE=../classroom/_site G4_PREFIX=grade4/ node tools/grade4-authoring/tests/browser-grade4.cjs   # every game played to the end, checks, flashcards, student links
   BASE=http://127.0.0.1:8771/grade4/ node tools/grade4-authoring/tests/browser-tools.cjs           # 9 tools at 4 screen sizes, zoom / Fit / Present
   G4_BASE=http://127.0.0.1:8771/ G4_SET=grade4 node tools/grade4-authoring/tests/browser-generators.cjs --all   # native generators, PDF export
   ```
6. Commit and push. The existing "Deploy integrated Classroom development site" workflow publishes it.

If the repository has moved on since `4bf5ca3`, copy the new files as they are, and re-apply the edits below by hand: each
is small and described exactly.

### Existing files changed

| File | Change |
|---|---|
| `course-outlines/grade4.json` | Now the ten-unit Common Core course (49 skills, 35 standards, `skillStandards` per skill). The previous file is unchanged as `course-outlines/grade4-math-expressions.json` (new). |
| `manifest.json` | 10 entries `{"courseId":"math4","path":"question-banks/math4/<unit>.json","approved":true}`. The assembler adapts them to `grade4` for the native generators. |
| `scripts/assemble-classroom-preview.mjs` | Imports `tools/grade4-authoring/staging/assemble-grade4.mjs` and, when Grade 4 banks are approved, replaces the preloaded Grade 4 card list with the real one and builds `_site/grade4/`. Also: relative `grade1–5/` card paths are kept (was `grade5/` only); the Projects section shows for approved courses (was Grade 5 only); the course band and preview banner name the approved grade; the study-guide card is titled **Understanding Check** (was "Readiness Check") for every grade. |
| `scripts/test-classroom-preview.cjs` | Unit count read from the outlines (35) instead of the fixed 37; approved Grade 4 checked for native banks, games, guides, projects and vocabulary; pending-bank checks run only on Grades 1–3; "Understanding Check" title. |
| `tests/grade4-outline.test.mjs` | Source-outline tests read `grade4-math-expressions.json`; the last test no longer requires "Questions coming soon" wording. |
| `grade4.html` | Description and footer text only. |
| `README.md`, `GRADE4_BANK_HANDOFF.md` | Grade 4 row and status note. |

### New files

| Area | Files |
|---|---|
| Question banks (4,410 questions: 30 per skill and level) | `question-banks/math4/*.json`, `question-banks/math4/meta/*.meta.json`, `math4/meta/*.meta.json` (same metadata at the path the shared players read), `question-banks/assets/math4/**` (762 PNG diagrams) |
| Course players | `worksheet-generator/grade4-games.html`, `grade4-flashcards.html`, `grade4-understanding-check.html`; `worksheet-generator/grade4/` (settings, theme, 10 flashcard decks with 261 cards); `worksheet-generator/elementary/` (shared, configuration-driven elementary runtime: games, flashcards, Understanding Check, tool shell) |
| Cheat sheets (10, two pages each) | `artifacts/math4-<unit>-cheat-sheet/worksheet.pdf`, sources `scripts/cheat-sheets/content/math4-*.cjs` |
| Interactive Math (9) | `artifacts/math4-{place-value-blocks,array-area-models,division-groups,equivalent-fractions,fraction-number-line,decimal-grids,angle-explorer,area-perimeter,symmetry-shapes}/index.html` |
| Projects (10, one per unit) | `artifacts/math4-project-*/` (Remedial / Standard / Advanced packets as PDF, Word and PowerPoint; teacher guide PDF and Word; page) |
| Thumbnails (66) | `thumbs/math4-*` (every game, tool, project, cheat sheet, unit and generator has its own) |
| Authoring source and tests | `tools/grade4-authoring/**`, `tests/grade4-course.test.mjs` |
| Docs | `docs/math4/README-GRADE4.md`, `VALIDATION_REPORT.md`, `MIGRATION.md`, `COVERAGE.md`, `COVERAGE.csv`, `CROSSWALK.md` |

## How Grade 4 appears on the development site

The development site is the production Classroom shell assembled by `scripts/assemble-classroom-preview.mjs`. Grade 4
follows the released Grade 5 model: its own players and files in one folder, `_site/grade4/`, and its unit cards in
the shared course page (`/#grade4`, `/#grade4.<unit>`; `grade4.html` redirects there).

Each unit page lists:

- **Create Resources** — the four native Classroom generators (Lesson Plan, Worksheet, Activity, Assessment), the same
  engines Algebra 1 uses, opened with `#unit=grade4-<unit>`. Error Analysis and Vocabulary Activities and Crosswords
  open the native Activity generator directly.
- **Games** — 9 games for every unit plus a model-drawing game where it fits (Fraction Match-Up in Units 6–7, Array Attack in
  Units 3–5): Treasure Quest, Space Rescue, Puzzle Island, Castle Conquest, Math Detective, Monster Match (play alone or
  as a class), and Rocket Race, Math Soccer, Four in a Row (team games). They keep the Grade 5 mechanics with Grade 4
  themes. Every game has Remedial / Standard / Advanced, skill selection, retries and hints, no timers, and a
  student link that opens straight into the configured game.
- **Study Guides** — Flashcards, Understanding Check (one at a time or all on one page, immediate or end feedback,
  worked solutions, progress, summary, retry of missed questions, printable results page, teacher summary), Cheat Sheet.
- **Interactive Math** and **Projects**.

No accounts, no server storage, no external services. Only display zoom is kept in the browser.

## Levels

Remedial (`cp2`), Standard (`cp1`), Advanced (`honors`), the site's existing elementary convention. Advanced adds
reasoning and multi-step work (error analysis, true/false with reasons, select-all, open response, two- and three-step
problems), not only larger numbers.

## Rebuilding content

```bash
cd tools/grade4-authoring
python3 outline.py            # outline.json from outline.py (the single source of units, skills and standards)
python3 build.py              # banks, metadata and diagrams (deterministic); needs rsvg-convert and Pillow
python3 verify.py             # independent re-derivation of every answer; must print TOTAL ERRORS 0
node tests/display-lint.cjs   # every string through the site's math renderer; must print 0 issues
python3 report.py             # docs/math4/COVERAGE.md and .csv
python3 build_content.py      # flashcards, vocabulary, cheat-sheet content
node build-config.cjs         # worksheet-generator/grade4/config.js from games.json
```
After `build.py`, copy `question-banks/math4/meta/*.json` to `math4/meta/`. Cheat-sheet PDFs, tool worksheets and
project files are built with the production repository's `scripts/cheat-sheets/build.cjs` and print helper
(`tools/grade4-authoring/print/print.cjs`, `projects/build.py`), which need Playwright.
