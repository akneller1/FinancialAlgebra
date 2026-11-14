# Grade 1 integration review — 2026-11-14

Status: locally assembled development preview; not deployed or approved for production.

- 12 units, 47 skills, 4,230 practice items and 282 fixed Understanding Check items.
- Reran practice and check verifiers: zero errors and warnings.
- Reran semantic/scope/duplicate/assets audit: zero blockers, no missing/unused images; 24/24 mapped standards.
- Site adapter: 24 files, 4,512 items, zero failures.
- Inspected a diagram sample from every unit (counters, ten frames, blocks, comparison table, tally chart, equality bars, lengths, triangle, clock and story subtraction).
- Repository tests: 94/94 pass. Updated retired Grade 1 outline expectations and stale Grade 5 tests for the already-requested removal of unit-view project cards.
- Integrated preview structural/native registration test: 45 elementary units pass. Complete Classroom development build succeeds.
- Browser gameplay and generator UI regression tests have NOT run. Do not treat structural tests as evidence of complete interactive behavior.
- 421 authored-key checks (399 practice, 22 Understanding Checks) require additional content review; automated arithmetic verification is not proof of all conceptual answers. Three conceptual difficulty flags, six deliberate place-value distractors, and one leaf/leaves heuristic flag remain documented by the supplied audit.

## Integration

Registered all math1 banks as approved:false, preview:true. Added the development-only Grade 1 assembler, player config and game/check entry pages. Native generators receive adapted grade1 bank IDs. Shared runtime code and the production Classroom repository are unchanged.

Flashcards, cheat sheets, vocabulary, projects and teaching notes were not supplied; their resource cards are omitted. No new Asteroid Blaster placements were added. The development preview reuses nine Grade 2 game modes and the verified separate Understanding Check sets.

The source change replaces the retired Grade 1 authoring directory and outline. Old-to-new unit mapping is in INTEGRATION.md. The package patch handles removed source files.

## Publication

GitHub push from this checkout could not authenticate (no username/credentials). No remote branch, PR, deployment or public Grade 1 release was created. Apply the enclosed patch to FinancialAlgebra, run checks/build, complete browser review, and publish staging before considering production.
