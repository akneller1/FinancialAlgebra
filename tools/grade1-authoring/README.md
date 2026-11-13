# Grade 1 authoring tools (`math1`)

Source for the Grade 1 Mathematics question banks, diagrams and coverage report.
Reuses the Grade 5 (`math5`) schema, file layout and verification model; the content,
number ranges and difficulty ladder are built for first graders.

| File | Purpose |
|---|---|
| `outline.py` | Loads `course-outlines/grade1.json`: 8 units, 27 sections, 93 skills. Skill IDs are `<unit-id>-skill-NN` (stable). Standards per skill come from the section that lists it. |
| `g1lib.py` | Grade 5 problem toolkit unchanged: `Item`, `Diagram`, `EX`/`KEY`/`FN` checks, `fam`, derived extras. |
| `figs1.py` | Pillow diagram renderer (no SVG rasteriser in this environment): ten-frames, counters, number lines, base-ten, tally, picture and bar graphs, shapes and solids, partitions, analog clocks, rulers, place-value charts, number cards, arrays, sorting boxes. Fixed 720×480 canvas, colour-vision-safe palette. |
| `families.py` | Legacy question helpers. Every family is `f(r, L) -> Item` and carries a machine-checkable `check` built from the inputs (never from the answer). ~50 factories covering arithmetic, place value, stories, data, geometry, time and measurement. |
| `aligned.py` | Explicit target-specific source for all 93 skills. No domain-fact fallback. Levels vary number ranges, scaffolding, unknown positions, comparison closeness, and reasoning demands. |
| `aligned_extras.py` | Error analysis, true/false, select-all and multipart questions draw from the same selected target. Required diagrams are retained, with labelled panels for multipart items. Legacy `extras.py` is unused. |
| `gen_units.py` | Generates `units/uNN_*.py` from the skill → family mapping, so a skill name can never drift from the outline. |
| `units/uNN_*.py` | `SKILLS = {index: {"name": …, "fams": [source(unit, index)]}}` for each unit. |
| `build1.py` | Builds `question-banks/math1/<unit>.json`, `meta/<unit>.meta.json`, `assets/math1/<unit>/<qid>.png` and `out/<unit>.checks.json`. 30 questions per skill and level (12 short answer, 12 multiple choice, 3 error analysis, 1 true/false, 1 select-all, 1 open response/matching). |
| `verify1.py` | Independent verifier: re-derives every answer from the stored inputs with its own arithmetic and its own implementations of the named checks (no import of the families). Also validates options, distractor reasons, standards, counts, duplicates, and every diagram file (exists, 720×480, decodes, not blank, alt text, answer agrees with the picture where the picture is the ground truth). Must print `TOTAL ERRORS 0`. |
| `dupstats.py` | Measures cross-skill duplication: exact identity (prompt + options + answer + picture), picture-equivalent groups and digit-masked near-duplicates. Baseline figures are stored in `out/dup_before.json`. |
| `dedupe1.py` | Surgical deduplication: only items whose identity also appears in another skill are rewritten, one copy of every identity is kept, and the rest of the bank is untouched. Routes: fresh draw from the same family, fresh draw re-presented in another form (`forms.py`), or the same fact re-presented without its picture. |
| `forms.py` | Re-presentation templates per check kind (equation/story/place-value/clock/shape wording). The answer and check are never changed, so the verifier still proves the mathematics. |
| `report.py` | Writes `docs/math1/COVERAGE.md` including before/after duplication statistics and validation results. |
| `question-banks/math1/manifest.json` | Approved-bank manifest for the 8 units (not merged into the public site manifest). |

## Rebuild

```bash
cd tools/grade1-authoring
python3 gen_units.py        # regenerate unit modules from the mapping
G1_NEAR=4 python3 build1.py # all 8 units, deterministic (G1_NODRAW=1 skips diagrams)
python3 verify1.py          # must end with TOTAL ERRORS 0
python3 report.py           # docs/math1/COVERAGE.md
```

`G1_NEAR` (default 3) is how many times the same prompt shape/number set/answer may repeat
inside one skill and level; the verifier rejects anything above 6.

## Design rules

* **Numbers:** facts within 10 and 20, two-digit numbers to 99, sums within 100, lengths
  within 120, minutes to the half hour. No regrouping beyond Grade 1 (compose a ten when
  the skill says so), no multiplication, no fractions beyond halves and fourths.
* **Reading load:** one or two short sentences, familiar object and name vocabulary,
  numerals rather than number words where possible. The verifier warns on words longer than
  12 letters and prompts over 260 characters.
* **Checks, never stored answers:** every item stores the inputs (`a`, `b`, tally rows,
  clock hour/minute, shape kind …) and `verify1.py` recomputes the answer from them, so an
  authoring mistake cannot verify itself.
* **Uniqueness:** a skill/level set of 30 never repeats a prompt (text + options + picture).
  The same fact may appear in a different skill, which is normal practice material.
* **Diagrams:** the alt text is written from the same data that draws the picture, so the
  description cannot drift from the image; the verifier checks the file, its size, that it
  is not blank, and — for shape questions — that the answer matches the drawn shape.

## Approval status

`approved` is `false` for all eight banks in `question-banks/math1/manifest.json`. The manifest
records the two kinds of review separately:

* `review.mathematicalValidation` — passed: every answer re-derived from its inputs, 0 errors,
  0 diagram defects, 0 within-skill duplicates.
* `review.editorialApproval` — pending: no curriculum reviewer has signed off on wording,
  difficulty or grade-level fit.

Content being mathematically validated does **not** make it approved. Only a separate editorial
authorisation should flip `approved` to `true`.

## Not integrated

Grade 1 is intentionally **not** wired into the public Classroom site: no edits are made to
`data.js`, `app.js`, `course-catalog.js`, the root `question-banks/manifest.json` or any
student-facing page. `question-banks/math1/manifest.json` is the handoff point for a later,
separately approved integration.

## Staging handoff and limits

The rebuild preserves all 8,370 IDs, skill IDs, level quotas, standards and all editorial approval and bank access flags, checked against commit `21bdadb`. Each skill has 30 questions per level.
The bank is not registered with production games.

`staging-games.html` demonstrates the proposed Puzzle Masters compatibility change:
keep the selected skill/level, allow image questions and longer text, and match repeated
answer values interchangeably. `scripts/test-grade1-staging.cjs` checks every one of the
279 scopes. `scripts/test-grade1-puzzle-browser.cjs` clicks and solves each scope at a
390-pixel mobile viewport, checks image decoding and rejects horizontal overflow.
The shared engine now uses this behavior in the branch-only integrated development artifact.
The legacy shared game has restrictive text-only/short-answer eligibility; its count of
restricted skill/level combinations is a compatibility warning, not a request to add filler.

Run the branch-only `grade1-alignment-rebuild.yml` workflow to rebuild all PNGs, run
independent mathematics/semantic/structural/alignment checks and both Chromium suites,
then commit generated banks only if every check passes. No deploy or approval step exists.

The alignment pattern audit rejects obvious domain and addend-structure errors; it is
not an exhaustive proof of instructional effectiveness. Drawing and story-writing targets
use model answers for automatic games, so alternate valid constructed responses need
teacher judgment. Some narrow targets have only two valid answer categories. Cross-skill
repeated facts are permitted; duplicates within a selected skill/level are rejected.
Remedial/Standard/Advanced levels describe task demand, not calibrated student performance.

## Integrated development artifact

The `Grade 1 — integrated development artifact` workflow assembles the actual Classroom
shell and native generators, then adds an isolated Grade 1 staging loader. No Pages or
production deployment occurs. Its successful run provides the downloadable
`grade1-integrated-development-site` artifact and browser screenshots/results.

For local assembly on `grade1-question-bank`, set `GRADE1_STAGING=1` when running
`scripts/assemble-classroom-preview.mjs`. With no flag, the default build excludes Grade 1
banks exactly as before. Both source manifests and assembled production manifests retain
all bank approval flags. Staging banks are registered with `verified:false`; only the
explicitly packaged staging facade allows their use in development pages.

Native worksheet, assessment, lesson-plan and printable engines use the Grade 1 banks.
Games and study guides reuse the elementary engines. Puzzle Masters retains images and
longer prompts and accepts interchangeable answer cards with the same mathematical value.
The integration suite verifies all 279 single-skill/level puzzles, all four native question
formats and Error Analysis at every skill/level, plus representative game and guide routes.

Format-specific printables still need compatible arrangements: Partner Check requires
explicit paired items, while mazes and Tarsia require enough short, distinct answers.
The UI may offer fewer printable formats for narrow skills; unrelated filler is not added.

Grade 1 flashcards are bank-derived practice cards, rather than a separately authored
vocabulary deck. They include complete single-answer prompts and retain diagrams;
select-all and multipart items remain in the readiness check and generators.
