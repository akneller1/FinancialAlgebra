# 2nd Grade Math (math2): integration README

Status: **development preview only.** The banks are registered as `approved:false, preview:true`. Nothing here is wired into
production; the production integrator (`scripts/integrate-approved-courses.mjs`) handles only math5 and ignores math2.

Branch: `grade2-content`, created from `grade3-content` (which is built on `grade4-framework-migration`, the current
config-driven elementary runtime). This branch therefore also contains the Grade 3 package. Every path below is
repository-relative (FinancialAlgebra repo).

## 1. What is in the package

| Area | Files |
|---|---|
| Curriculum map | `course-outlines/grade2.json` (replaced: 12 units, 53 skills, CCSS standards, targets, status `development`); `tools/grade2-authoring/outline.py` → `outline.json`; `docs/math2/curriculum-map.json` (unit → skill → target → standards → question families → resources → projects) |
| Practice banks | `question-banks/math2/<unit>.json`: 12 units and 4,770 questions (53 skills × 30 Remedial, 30 Standard and 30 Advanced). Metadata (question type, tags, distractor reasons) is in `question-banks/math2/meta/<unit>.meta.json` |
| Diagrams | `question-banks/assets/math2/<unit>/*.png` (local PNGs; alt text is in each item's `diagram.spec.alt`) |
| Understanding Checks | `question-banks/math2/checks/<unit>.json` + `checks/meta/`: 318 fixed items (2 per skill per level), IDs `m2c-…`, `purpose: "understanding-check"`, per-skill feedback. Kept separate from practice |
| Flashcards | `worksheet-generator/grade2/flashcards/<unit>.json` (233 cards) |
| Worked examples & misconceptions | `worksheet-generator/grade2/worked-examples.json` (all 53 skills); `tools/grade2-authoring/staging/teaching-notes.json`, `objectives.json` |
| Vocabulary | `tools/grade2-authoring/patches/vocabulary-math2.js` (104 terms, keys `math2-<unit>`) |
| Cheat sheets | source `scripts/cheat-sheets/content/math2-<unit>.cjs`; PDFs `artifacts/math2-<unit>-cheat-sheet/worksheet.pdf`; thumbnails `thumbs/math2-<unit>-cheat-sheet.jpg` |
| Projects (14) | `artifacts/math2-project-<slug>/`: student packets for Remedial, Standard and Advanced (PDF, DOCX and PPTX), teacher guide with solutions and rubric, supports, hero and index.html. Thumbnails `thumbs/math2-project-<slug>.{jpg,svg}`; registry `tools/grade2-authoring/projects/projects-registry.json` |
| Course runtime config | `worksheet-generator/grade2/config.js`, `grade2/g2.css`, `worksheet-generator/grade2-{games,flashcards,understanding-check}.html`; `tools/grade2-authoring/games.json`; `tools/grade2-authoring/interactive/manifest.json` (empty) |
| Thumbnails for shared activities | `thumbs/math2-{flashcards,understanding-check,game-*,generator-*}.svg` (course-neutral copies) |
| Assembler | `tools/grade2-authoring/staging/assemble-grade2.mjs` (same contract as Grades 3 and 4) |
| Registration | `manifest.json`: 12 `math2` entries (`approved:false`, `preview:true`) |
| Authoring and validation source | `tools/grade2-authoring/` (see its README) |
| Reports | `docs/math2/VALIDATION_REPORT.md`, `AUDIT.md`, `COVERAGE.md`, `coverage.csv` |
| Preview patch | `docs/math2/assemble-classroom-preview.patch` (adds both Grade 2 and Grade 3) |

No shared runtime, game, generator or navigation file was modified or forked.

## 2. Registration changes

1. **`manifest.json`** already contains the 12 math2 bank entries (preview only).
2. **`scripts/assemble-classroom-preview.mjs`** (dev preview): apply `docs/math2/assemble-classroom-preview.patch`.
   `git apply --check` confirms it applies to FA `main` e70c59f. It **supersedes the Grade 3 patch**, so apply this one instead of
   `docs/math3/assemble-classroom-preview.patch`. It (a) imports the Grade 2 and Grade 3 assemblers and (b) replaces the pending
   Grade 2 and Grade 3 course records with the assembled ones. It also (c) lets the native-bank adapter include math2 and math3
   banks marked `preview:true`.
3. **Prerequisites on the branch being assembled.** These are the same as for Grade 3:
   - `worksheet-generator/elementary/` must be present. On these branches it sits at root `elementary/`, so move it there; do not copy it.
   - `tools/grade4-authoring/` must be present.
   - The m5-*.png uploads must be where the main assembler expects them.
4. **Vocabulary.** The assembler appends `patches/vocabulary-math2.js` to the native vocabulary file (keys `grade2-<unit>`).
   For production, merge it the same way Grade 4's vocabulary was merged.

Nothing is registered for production. Do not add math2 to `integrate-approved-courses.mjs` until a person approves the banks.

## 3. Commands

```bash
# development preview (Classroom checkout next to FA, or CLASSROOM_SOURCE_DIR=...)
git apply docs/math2/assemble-classroom-preview.patch
node scripts/assemble-classroom-preview.mjs              # → ../classroom/_site, "grade2, grade3 with approved banks"
python3 -m http.server 8766 -d ../classroom/_site        # open /#grade2

# regression tests (Playwright/Chromium)
G2_SITE=../classroom/_site G2_PREFIX=grade2/ node tools/grade2-authoring/tests/browser-grade2.cjs
node tools/grade2-authoring/tests/browser-generators.cjs --all        # needs the http.server above
node tools/grade2-authoring/tests/display-lint.cjs
node tools/grade2-authoring/tests/print-overflow.cjs <project scratch dir>

# content validation
cd tools/grade2-authoring && python3 verify.py && VERIFY_CHECKS=1 python3 verify.py && python3 audit.py
```

The full rebuild order is in `tools/grade2-authoring/README.md`.

## 4. Production steps (when approved)

Follow the Grade 4 migration manifest pattern:
1. Set `approved:true` on the 12 math2 entries and drop `preview`.
2. Add a math2 branch to the production integrator mirroring math5: banks, meta, assets, checks, flashcards, artifacts, thumbnails, config and players.
3. Merge the vocabulary.
4. Run the browser suites against the production build.

## 5. Gaps and decisions (not finished, or needing the shared framework)

- **The shared player does not read the fixed Understanding Check sets yet.** This is the same gap as Grade 3:
  `el-understanding-check.js` draws from the practice pool. The proposed shared change is an optional `checkPath` in
  `MK_ELEMENTARY` pointing to `question-banks/math2/checks/`. I did not make it here, to avoid forking the framework.
- **No Grade 2 interactive tools.** `interactive/manifest.json` is empty.
- **Array Attack is removed** from the Grade 2 games. Its engine writes multiplication (×) equations, which belong to Grade 3.
  Grade 2 arrays use repeated addition (2.OA.C.4).
- **The graph unit has a small set of picture-free items.** The card-match game and the Tarsia activity use only items without a picture.
  So the Picture Graphs and Bar Graphs unit includes some items that give the data in words (“Data: apple 7, pear 12 …”). Its other items use the graph pictures.
- **AM and PM are written as "AM"/"PM", not "a.m."/"p.m.".** The site's math renderer italicizes the letters of "a.m." as
  variables, but it already treats AM and PM as words. The standard's wording (a.m., p.m.) appears in the outline text and the vocabulary.
- **Money:** amounts under a dollar use ¢ (45¢), whole dollars use $ ($13), and mixed amounts are written "$3 and 45¢".
  Decimal money notation is left for Grade 4.
- **Standards scope.** 2.NBT.A.1 has its own statement plus parts a and b, and all three are tracked (28 codes). The outline replaces the
  old 9-unit, 89-skill outline. Unit and skill IDs differ from the old handoff.
- **The printable Understanding Check page** (`practice-test.html`) is not part of the Grade 2 generator test (matching what was done for Grade 3).
  The interactive Understanding Check is tested.
- **The worksheet and assessment generator previews show only the Standard and Advanced level labels.** This is existing
  shared behavior; Remedial items exist and print.
- **Human review is pending.** The banks are machine-verified (see VALIDATION_REPORT) but no teacher has approved them.
  Conceptual multiple-choice items (best tool, estimates, shape facts) are checked against their rule or authored key only.
- **Division notation:** not used in Grade 2.
