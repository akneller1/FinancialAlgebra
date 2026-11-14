# 1st Grade Math (math1): integration notes

Status: **development preview only.** Banks are registered `approved:false, preview:true`. Nothing here touches production (`akneller1/classroom`) or any shared runtime, game, generator or navigation file. All paths are repository-relative to **akneller1/FinancialAlgebra**, mirroring the Grade 2 package (`grade2-content-package-verified/`).

## 1. Contents

| Area | Files |
|---|---|
| Course outline | `course-outlines/grade1.json` — **replaces** the 8-unit/93-skill scope-and-sequence outline with the Grade 2-style standards outline: 12 units, 47 skills, `skillStandards`, `targets`, status `development`. Course ID stays **`math1`**. |
| Practice banks | `question-banks/math1/<unit>.json` (schemaVersion 1; 12 files, 4,230 questions). IDs `m1-<abbr>-sNN-<level>-NNN`; levels `cp2` Remedial, `cp1` Standard, `honors` Advanced; formats `short-answer`, `multiple-choice`, `select-all`, `open-response` |
| Metadata | `question-banks/math1/meta/<unit>.meta.json`: `questionType`, `tags`, `explanation`, `distractors` (answer → misconception), `misconception`, `diagram` kind, and **`game: {textMC, numeric}`** |
| Understanding Checks | `question-banks/math1/checks/<unit>.json` + `checks/meta/` — 282 fixed items (2 per skill per level), IDs `m1c-…`, `purpose: "understanding-check"`, per-skill feedback |
| Diagrams | `question-banks/assets/math1/<unit>/<qid>.png` (1,359 local PNGs; alt text in `diagram.spec.alt`) |
| Flashcards | `worksheet-generator/grade1/flashcards/<unit>.json` — 223 cards (91 vocabulary, 96 concept/fact/strategy/misconception/example, 36 visual with inline SVG), same shape as Grade 2 (`unit`, `unitName`, `number`, `cards[front, back, example?, kind, svg?]`) |
| Cheat sheets | source `scripts/cheat-sheets/content/math1-<unit>.cjs`; two-page PDFs `artifacts/math1-<unit>-cheat-sheet/worksheet.pdf`; thumbnails `thumbs/math1-<unit>-cheat-sheet.jpg` (built with the Classroom `scripts/cheat-sheets/build.cjs`) |
| Supporting content | `worksheet-generator/grade1/worked-examples.json` (47 skills), `tools/grade1-authoring/patches/vocabulary-math1.js` (91 terms, keys `math1-<unit>`), `tools/grade1-authoring/staging/teaching-notes.json`, `objectives.json` |
| Registration | `question-banks/math1/manifest.json` — 12 entries to merge into root `manifest.json` (`approved:false`, `preview:true`) |
| Reports | `docs/math1/VALIDATION_REPORT.md`, `COVERAGE.md`, `coverage.csv`, `curriculum-map.json` (unit → skill → standards → target → misconception → families → counts), `game-eligibility.json`, `audit.json`, `verification-output.txt` |
| Authoring kit | `tools/grade1-authoring/` (see its README). **Replace the existing directory**: the earlier Grade 5-model kit (`build1.py`, `verify1.py`, `families.py`, `forms.py`, `extras.py`, `dedupe1.py`, `dupstats.py`, `gen_units.py`, `report.py`, old `figs1.py`/`g1lib.py`/`outline.py`) never produced committed banks and targets the retired 93-skill outline. |

## 2. Unit and ID changes
Unit IDs differ from the old Illustrative Mathematics outline (no Grade 1 banks or production records used them). Mapping for any links: `adding-subtracting-working-data` → `add-subtract-10` + `data`; `addition-subtraction-story-problems` → `word-problems-20`; `adding-subtracting-within-20` → `add-subtract-20` + `equal-sign`; `numbers-to-99` → `count-120` + `tens-ones` + `compare-numbers`; `adding-within-100` → `add-subtract-100`; `length-measurement-120` → `measuring-length` (+ counting to 120 in `count-120`); `geometry-time` → `shapes-equal-shares` + `telling-time`; `putting-it-all-together` → review is covered by the fixed Understanding Checks.

## 3. Games and shared activities
- `meta[qid].game.textMC = true` (1,120 items): multiple choice, no picture, one line ≤140 characters, every choice ≤32 characters — safe for text-only multiple-choice play in the shared games. Lists per unit: `docs/math1/game-eligibility.json`.
- `meta[qid].game.numeric = true` (559 items): short answer that is a plain whole number with no picture — for games/card-match/Tarsia that need a simple numeric answer.
- Do not use items with diagrams, select-all, open-response, error-analysis (multi-line) or word answers (“half past 3”, “4 tens and 7 ones”) in text-only games.
- No multiplication, division or fraction notation is used, so no Grade 1 game needs to be removed for scope (Array Attack should stay off, as for Grade 2).
- Clock answers are written `h:mm` (checked by the shared `clock` check) or `“3 o'clock” / “half past 3”`. Comparison answers use `>`, `<`, `=` and were lint-checked with the site's math display rules (non-breaking hyphens, no italicized words).

## 4. Steps for the integrator
1. Copy the package into FinancialAlgebra at the same relative paths; replace `course-outlines/grade1.json` and `tools/grade1-authoring/`.
2. Merge `question-banks/math1/manifest.json` entries into the root `manifest.json` (preview only).
3. Rebuild and re-verify (requires Python 3 + Pillow, `rsvg-convert`; reuses `tools/grade2-authoring`, `grade3-authoring`, `grade5-authoring` unchanged):
   ```bash
   cd tools/grade1-authoring
   python3 outline.py --write && python3 build.py && python3 build_checks.py
   python3 verify.py && VERIFY_CHECKS=1 python3 verify.py && python3 audit1.py && python3 package1.py
   node tests/schema-adapter.cjs ../../question-bank-adapter.js ../..
   python3 build_content.py     # flashcards, vocabulary, cheat-sheet sources, worked examples, teaching notes
   # cheat sheets (in the Classroom repo, needs playwright): node scripts/cheat-sheets/build.cjs math1-count-120 … math1-shapes-equal-shares
   ```
4. For the preview shell, follow the Grade 2 pattern: add a `math1` branch beside `math2` in `scripts/assemble-classroom-preview.mjs` (line 137 already admits `math[1-4]` banks that are `approved`; extend the preview condition to `math1`), and create a `tools/grade1-authoring/staging/assemble-grade1.mjs` from `assemble-grade2.mjs`. That assembler also expects `worksheet-generator/grade1/config.js`, flashcards, vocabulary, teaching notes, projects and an interactive manifest, of which this package now includes flashcards, vocabulary, worked examples and teaching notes; `config.js`, projects and an interactive manifest are still to be added (empty projects/interactive lists are valid).
5. Run the Grade 2 browser suites against Grade 1 (`tests/browser-grade2.cjs` with a `G1_*` copy) before any approval. Do not add math1 to `integrate-approved-courses.mjs` until a person approves the banks.

## 5. Decisions
- Remedial/Standard/Advanced map to the existing `cp2`/`cp1`/`honors` level codes.
- Number ranges: facts within 10 (unit 2) and 20 (units 3–5); counting/reading to 120; two-digit place value and comparison to 99; adding within 100 with at most one new ten; lengths ≤20 units; time to the hour and half hour only.
- Repeated addition appears only as “2 towers like this” (doubling) in composing shapes; no × notation.
- Teen-number and place-value misconception distractors (e.g. 61 for sixteen, 1007 for one hundred seven) are deliberate and documented.
