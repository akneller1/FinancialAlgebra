# 1st Grade Math (math1): validation report

Run on 2026-11-14 in a clean checkout layout (FinancialAlgebra `tools/grade2-authoring`, `grade3-authoring`, `grade5-authoring` from `main`, plus this kit). Every command exited 0. Raw output: `docs/math1/verification-output.txt`; full audit data: `docs/math1/audit.json`.

| Check | Tool | What it does | Result |
|---|---|---|---|
| Standards | `outline.py` | Every CCSS Grade 1 code (20 leaf standards + 1.NBT.B.2 and parts a, b, c) is mapped to at least one skill | **24/24** covered (`COVERAGE.md`) |
| Counts | `verify.py`, `audit1.py` | 12 units, 47 skills, 30 Remedial (cp2) + 30 Standard (cp1) + 30 Advanced (honors) per skill | **4,230** questions; every skill/level has exactly 30 |
| Answer correctness | `verify.py` + `checks1.py` (extends Grade 2 `checks2.py` → Grade 3 → Grade 5) | Re-derives every answer, MC option, select-all option, open-response part and true/false claim from stored check data with independent arithmetic and 47 new Grade 1 named checks (ten frames, tally, tens/ones, number names, comparisons, transitivity of length, unit measurement with gaps/overlaps, hour/half-hour clocks, data questions, shape attributes, composition, equal shares). Rejects any stored distractor that is actually correct. Numbers used by an expression check must be visible in the prompt or picture | **0 errors, 0 warnings** |
| Understanding Checks | `VERIFY_CHECKS=1 verify.py` | Same checks on the fixed check sets (2 per skill per level, never repeating a practice prompt) | **282** items, **0 errors** |
| Schema | site `question-bank-adapter.js` (both FA and classroom copies) run in Node with a catalog built from `course-outlines/grade1.json` | `validate()` + `register()` + `select()` on all 24 bank files | **4,512 questions, 0 failing** |
| Uniqueness and repetition | `build.py` gates + `audit1.py` | No repeated prompt+picture+options anywhere in the course; no repeated template-with-same-numbers-and-answer; ≤5 items share one digit-masked prompt template per skill/level (TMAX) | **0** exact duplicates, **0** same-number repeats, **0** templates over 6 |
| Multiple choice | `verify.py`, `audit1.py` | 4 distinct options, exactly one correct, answer equals the correct option; correct position balanced | **0** problems; positions A/B/C/D = 426/484/471/474 |
| Distractors | `audit1.py` | Every computed distractor carries a documented misconception reason (`meta.distractors`) | **100%** |
| Explanations | `audit1.py` | Final solution steps state the answer | **0** mismatches |
| Answer vs. question | checks with units + `audit1.py` | Word-problem answers must carry the unit the question asks about (e.g. “9 shells”); heuristic noun check | 1 heuristic flag, a false positive (“leaves”/“leaf”) |
| Grade 1 scope | `audit1.py` | Numbers in prompts/answers within unit range (≤10, ≤20, ≤99/≤120 as appropriate); no ×, ÷ or fraction notation; time only to the hour/half hour | **0** out of range |
| Reading load | `audit1.py` | Words per prompt (excluding error-analysis wrappers) | max **37**, mean 13.1 / 13.7 / 14.1 (R/S/A); 0 over 45 |
| Language lint | `verify.py` notation lints + build polish | ASCII minus, “1 times”, broken values, plural agreement after 1 (incl. “1 more X”), site-renderer italic traps (do/go/“of a”) | **0** issues |
| Assets | `verify.py`, `audit1.py` | Every diagram file exists, alt text present, diagram data stored for the verifier; no orphan files | **1,359** PNGs referenced (1,275 practice + 84 checks), **0 missing, 0 unused** |
| Rendered review | contact sheets viewed as images | Ten frames, crossed-out counters, number lines, base-ten blocks, 120/hundred charts, bars, tally charts, picture graphs, tables, length strips on unit squares, measuring with cubes/clips (gaps, overlaps, mixed sizes), analog/digital clocks, 2-D shapes (rotated, open figures), solids, composite pattern-block shapes, partitions | Defects found and fixed: length grids were not countable (now unit-square strips), compose drawings off-centre, “1 more blocks”, repeated names in one prompt, “6 groups of 10 and 0 more” |
| Determinism | rebuild in a second checkout | `build.py` regenerates byte-identical banks | identical |

## Difficulty progression
Across the 47 skills the mean largest number per item rises 14.7 → 23.1 → 30.1 (R → S → A) and 40/47 skills use larger numbers at Advanced. Advanced also adds unknowns in all positions, start-unknown stories, three-category comparisons, unaligned length comparison, elapsed/earlier time, rotated and less familiar shapes, and reasoning items (reasoning/explain share 0.30 → 0.35). Remedial uses more pictures (468 vs 377 diagrams). The numeric metric does not apply to three skills whose difficulty is conceptual (Time to the Half Hour, Matching and Using Clock Times, Naming 2-D and 3-D Shapes); their levels differ by content (o'clock vs half past vs mixed and elapsed time; 4 shapes vs 9 shapes and turned shapes).

## Known limitations (for the independent audit)
1. **400 items use an authored key** (conceptual MC such as “What makes a shape a triangle?”, “Who measured the right way?”, sorting categories). They are checked against the key and option uniqueness only, not re-derived.
2. **Six far-off distractors** are intentional place-value misconceptions (e.g. “one hundred thirteen is written 10013”). Remove them if the audit prefers tighter distractors (`docs/math1/audit.json → notes`).
3. **Open-response/matching extras** are built from the same skill's core families, so a few sets have repeated part answers (e.g. four “4”s in “How many fourths make a whole?”).
4. Some families serve two or three levels with different number ranges, so a Standard and an Advanced item can share wording. Teacher review of tone and pacing is still pending; no human has approved the banks (`approved:false`, `preview:true`).
5. Clocks use the shared Grade 3 renderer (hour hand placed exactly at h + m/60), so half-hour hands sit between numbers as intended.
6. Not authored in this package: flashcard decks, vocabulary patch, cheat sheets, projects, teaching notes, `worksheet-generator/grade1/config.js` and a staging assembler (see `INTEGRATION.md`).
