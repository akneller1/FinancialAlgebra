# 3rd Grade Math (math3) — integration README

Status: **development preview only.** Banks are registered `approved:false, preview:true`. Nothing here is wired into
production; the production integrator (`scripts/integrate-approved-courses.mjs`) only handles math5 and will ignore math3.

Branch: `grade3-content`, created from `grade4-framework-migration` (the current config-driven elementary runtime).
Paths below are repository-relative (FinancialAlgebra repo).

## 1. What is in the package

| Area | Files |
|---|---|
| Curriculum map | `course-outlines/grade3.json` (replaced: 11 units, 53 skills, CCSS standards, targets, status `development`); `tools/grade3-authoring/outline.py` → `outline.json`; `docs/math3/curriculum-map.json` (unit → skill → target → standards → question families → resources → projects) |
| Practice banks | `question-banks/math3/<unit>.json` (11 units, 4,770 questions = 53 skills × 30 Remedial/30 Standard/30 Advanced); `question-banks/math3/meta/<unit>.meta.json` (question type, tags, distractor reasons) |
| Diagrams | `question-banks/assets/math3/<unit>/*.png` (local PNGs, alt text in each item's `diagram.spec.alt`) |
| Understanding Checks | `question-banks/math3/checks/<unit>.json` + `checks/meta/` (317 fixed items, IDs `m3c-…`, `purpose: "understanding-check"`, per-skill feedback) — separate from practice |
| Flashcards | `worksheet-generator/grade3/flashcards/<unit>.json` (224 cards) |
| Worked examples & misconceptions | `worksheet-generator/grade3/worked-examples.json` (all 53 skills); `tools/grade3-authoring/staging/teaching-notes.json`, `objectives.json` |
| Vocabulary | `tools/grade3-authoring/patches/vocabulary-math3.js` (101 terms, keys `math3-<unit>`) |
| Cheat sheets | source `scripts/cheat-sheets/content/math3-<unit>.cjs`; PDFs `artifacts/math3-<unit>-cheat-sheet/worksheet.pdf`; thumbs `thumbs/math3-<unit>-cheat-sheet.jpg` |
| Projects (13) | `artifacts/math3-project-<slug>/` (student packets R/S/A as PDF/DOCX/PPTX, teacher guide, solutions, rubric, supports, hero, index.html); `thumbs/math3-project-<slug>.{jpg,svg}`; registry `tools/grade3-authoring/projects/projects-registry.json` |
| Course runtime config | `worksheet-generator/grade3/config.js`, `grade3/g3.css`, `worksheet-generator/grade3-{games,flashcards,understanding-check}.html`; `tools/grade3-authoring/games.json`; `tools/grade3-authoring/interactive/manifest.json` (empty) |
| Thumbs for shared activities | `thumbs/math3-{flashcards,understanding-check,game-*,generator-*}.svg` |
| Assembler | `tools/grade3-authoring/staging/assemble-grade3.mjs` (same contract as Grade 4's) |
| Registration | `manifest.json`: 11 `math3` entries (`approved:false`, `preview:true`) |
| Authoring + validation source | `tools/grade3-authoring/` (see its README) |
| Reports | `docs/math3/VALIDATION_REPORT.md`, `AUDIT.md`, `COVERAGE.md`, `coverage.csv` |
| Preview patch | `docs/math3/assemble-classroom-preview.patch` |

No shared runtime, game, generator or navigation file was modified or forked.

## 2. Registration changes

1. **`manifest.json`** — already contains the 11 math3 bank entries (preview only).
2. **`scripts/assemble-classroom-preview.mjs`** (dev preview) — apply `docs/math3/assemble-classroom-preview.patch`
   (verified with `git apply --check` against FA `main` e70c59f). It (a) imports `assembleGrade3/grade3Ready`,
   (b) replaces the pending Grade 3 course record with the assembled one before the Grade 4 hook, and
   (c) lets the native-bank adapter include math3 banks marked `preview:true`.
3. **Prerequisites on the branch being assembled:** `worksheet-generator/elementary/` (the shared runtime; on the
   `grade4-framework-migration` branch it currently sits flattened at root `elementary/` — move it, do not copy a
   Grade-3 version) and `tools/grade4-authoring/` (Grade 4 hook). The m5-*.png uploads at repo root must be where the
   main assembler expects them, as for Grade 5.
4. **Vocabulary:** merge `tools/grade3-authoring/patches/vocabulary-math3.js` into the Classroom vocabulary file the
   same way Grade 4's `vocabulary-math4.js` was merged.

Nothing is registered for production. Do not add math3 to `integrate-approved-courses.mjs` until a person approves the banks.

## 3. Commands

```bash
# development preview (Classroom checkout next to FA, or CLASSROOM_SOURCE_DIR=...)
git apply docs/math3/assemble-classroom-preview.patch
node scripts/assemble-classroom-preview.mjs        # → ../classroom/_site, "grade3 with approved banks"
python3 -m http.server 8766 -d ../classroom/_site  # open /#grade3

# regression tests (Playwright/Chromium)
node tools/grade3-authoring/tests/browser-grade3.cjs        # 151 checks
node tools/grade3-authoring/tests/browser-generators.cjs --all   # 77 checks
node tools/grade3-authoring/tests/display-lint.cjs
node tools/grade3-authoring/tests/print-overflow.cjs

# content validation
cd tools/grade3-authoring && python3 verify.py && VERIFY_CHECKS=1 python3 verify.py && python3 audit.py
```

Full rebuild order: `tools/grade3-authoring/README.md`.

## 4. Production steps (when approved)

Follow the Grade 4 migration manifest pattern: set `approved:true` on the 11 math3 entries (drop `preview`), add a
math3 branch to the production integrator mirroring math5 (banks, meta, assets, checks, flashcards, artifacts, thumbs,
config, players), merge vocabulary, then run the browser suites against the production build.

## 5. Gaps and decisions (not finished / need the shared framework)

- **Fixed Understanding Check sets are not yet read by the shared player.** `el-understanding-check.js` draws from the
  practice pool. Proposed shared change (not made here, to avoid forking): an optional `checkPath` in `MK_ELEMENTARY`
  config pointing to `question-banks/math3/checks/`; until then the Grade 3 Understanding Check page works but uses practice items.
- **No Grade 3 interactive tools** (`interactive/manifest.json` is empty).
- **Fraction Match-Up removed from the Grade 3 game list** — its engine generates denominators 5/10/12 and simplest-form
  answers, outside 3.NF. Re-enable only if the engine gets a denominator whitelist.
- **Worksheet generator preview shows only Standard/Advanced labels** (existing shared behavior); Remedial items exist and print.
- **Understanding Check, `equivalent-comparing-fractions-skill-03` Remedial:** 1 item instead of 2 (the practice bank already
  uses every distinct item of that small family set).
- **Standards scope:** the old handoff kept a `2.G.2` review strand in Unit 1; per the request not to label prerequisite
  content as Grade 3, the outline now covers only the 33 CCSS Grade 3 leaf standards. Units/IDs differ from the old 8-unit outline.
- **Human review pending:** banks are machine-verified (see VALIDATION_REPORT) but not teacher-approved; conceptual MC items
  are checked against their authored key only.
- **Division notation:** banks use the site's `÷` convention; the stacked-fraction display preference applies only where the renderer supports it.
