# Grade 2 authoring tools (`math2`)

Source for the Grade 2 Mathematics question banks, diagrams and coverage report.
The Grade 1 toolchain is reused rather than forked: the same builder, verifier, deduplicator
and renderer run against `course-outlines/grade2.json`.

| File | Purpose |
|---|---|
| `outline2.py` | Loads `course-outlines/grade2.json` (9 units, 27 sections, 89 skills). Skill IDs are `<unit-id>-skill-NN`. Standards come from every section that lists the skill. |
| `fam2.py` | Grade 2 families: two-digit regrouping, three-digit place value, skip counting, number lines, line plots, metric and customary units, arrays, even/odd, money, time to five minutes, thirds, polygons, two-step problems. Reuses the Grade 1 families (`from families import *`) for fluency, tally/graph, base-ten, clock, ruler, shape and partition work that the Grade 2 outline re-teaches. |
| `figs2.py` | New diagram kinds registered into the shared renderer: `baseten3` (hundreds flats), `place3` (three-digit chart), `coins`, `lineplot`, `tape`, `polygon`. Everything else (ten-frames, counters, number lines, base-ten, tally, pictograph, bar graph, shapes, partitions, clocks, rulers, arrays) is the Grade 1 renderer. |
| `extras2.py` | Grade 2 derived formats (3 error analysis, 1 true/false, 1 select-all, 1 open response per skill and level) built from Grade 2 fact pools. |
| `gen_units2.py` | Generates `units/g2uNN_*.py` from the skill → family mapping, so skill names cannot drift from the outline. |
| `build2.py` | Builds `question-banks/math2/<unit>.json`, `meta/<unit>.meta.json`, `assets/math2/<unit>/<qid>.png` and `out/<unit>.checks.json` through the shared Grade 1 builder. 30 questions per skill and level: 12 short answer, 12 multiple choice, 3 error analysis, 1 true/false, 1 select-all, 1 open response. |
| `verify2.py` | Runs the shared independent verifier against math2 and registers the Grade 2 check kinds (`digit_value3`, `expanded3`, `skip_seq`, `round10`, `round_sum`, `money_cents`, `part_name`, `polygon_*`, `array_*`, `even_odd`, `longer_lbl`, `shorter_lbl`, `tape_diff`, `lineplot_*`, `repeat_add`, `fraction_shaded`, `clock_ampm`). |
| `dedupe2.py` | Cross-skill deduplication with the shared engine: one copy of every identity is kept, redundant copies are re-drawn, re-presented or re-worded. |
| `report2.py` | Writes `docs/math2/COVERAGE.md` (counts, formats, standards, before/after duplication, validation, approval). |

## Rebuild

```bash
cd tools/grade2-authoring
python3 gen_units2.py          # regenerate unit modules from the mapping
G1_NEAR=3 python3 build2.py    # all 9 units (G1_NODRAW=1 skips diagrams)
python3 verify2.py             # must end with TOTAL ERRORS 0
python3 dedupe2.py             # cross-skill duplicates (optional, idempotent)
python3 report2.py             # docs/math2/COVERAGE.md
```

## Content rules

* **Numbers:** fluency within 20, two-digit addition and subtraction within 100 including
  composing/decomposing a ten, three-digit numbers within 1,000, sums and differences within
  1,000, arrays up to 5 × 5, money to one dollar, time to five-minute intervals, lengths in
  centimeters, meters, inches and feet. No multiplication facts, no fractions beyond halves,
  thirds and fourths, no decimal notation for money.
* **Task forms:** equations in both orders, missing-part and missing-addend forms, stories with
  named children and objects, table/line-plot/tally reading, "choose the unit" and "explain the
  strategy" items, two-step problems, error analysis of a classmate's misconception, true/false
  with reasoning, select-all claims and multi-part open responses.
* **Checks, never stored answers:** each item stores its inputs (`a`, `b`, `rows`, `cols`,
  `cents`, `hour`, `minute`, `n`, `which` …); `verify2.py` recomputes the answer from them.
* **Diagrams:** alt text is generated from the same data that draws the picture; the verifier
  checks size (720×480), decodability, that the figure is not blank, and that shape answers
  match what is drawn.
* **Duplicates:** none inside a skill/level; across skills the residue is limited to closed
  fact sets (array sizes, polygon names, fraction words, true/false stems).

## Compatibility

The banks use the Grade 5 schema (`schemaVersion: 1`, `courseId`, `unitId`, `questions[]` with
`id`, `skillId`, `level`, `format`, `prompt`, `options`/`parts`, `answer`, `solutionSteps`,
`diagram`, `standards`, `sourceNotes`) plus the same meta sidecar, so the existing games,
generators, flashcard decks and understanding checks read them without changes.

## Approval status

`approved` is `false` for all nine banks. `question-banks/math2/manifest.json` records
mathematical validation (passed, 0 errors) separately from editorial approval (pending).

## Not integrated

Grade 2 is not wired into either site: no edits to `data.js`, `app.js`, the course catalog or the
root site manifest, and nothing is published.
