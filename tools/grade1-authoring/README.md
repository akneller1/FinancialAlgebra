# Grade 1 authoring tools (`math1`)

Source for the Grade 1 Mathematics question banks, diagrams and coverage report.
Reuses the Grade 5 (`math5`) schema, file layout and verification model; the content,
number ranges and difficulty ladder are built for first graders.

| File | Purpose |
|---|---|
| `outline.py` | Loads `course-outlines/grade1.json`: 8 units, 27 sections, 93 skills. Skill IDs are `<unit-id>-skill-NN` (stable). Standards per skill come from the section that lists it. |
| `g1lib.py` | Grade 5 problem toolkit unchanged: `Item`, `Diagram`, `EX`/`KEY`/`FN` checks, `fam`, derived extras. |
| `figs1.py` | Pillow diagram renderer (no SVG rasteriser in this environment): ten-frames, counters, number lines, base-ten, tally, picture and bar graphs, shapes and solids, partitions, analog clocks, rulers, place-value charts, number cards, arrays, sorting boxes. Fixed 720×480 canvas, colour-vision-safe palette. |
| `families.py` | Question families. Every family is `f(r, L) -> Item` and carries a machine-checkable `check` built from the inputs (never from the answer). ~50 factories covering arithmetic, place value, stories, data, geometry, time and measurement. |
| `extras.py` | Grade 1 derived formats: 3 error-analysis, 1 true/false, 1 select-all and 1 open-response per skill and level, generated from a domain fact factory so picture-heavy skills still get them. |
| `gen_units.py` | Generates `units/uNN_*.py` from the skill → family mapping, so a skill name can never drift from the outline. |
| `units/uNN_*.py` | `SKILLS = {index: {"name": …, "fams": […], "domain": …}}` for each unit. |
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
