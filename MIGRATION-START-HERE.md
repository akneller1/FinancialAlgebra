# Grade 4 migration into current elementary Classroom framework

Source: uploaded staging package. Production has NOT been changed.

## Verified package inventory
- 10 Grade 4 unit bank JSON files, diagram assets, metadata and curriculum outline.
- Grade 4 games, flashcards, Understanding Check player and shared elementary runtime.
- Interactive activities, cheat sheets, projects and thumbnails.
- Preview assembly and QA documentation.

## Integration contract
Use the CURRENT Grade 5 production release adapter as model. Keep source in FinancialAlgebra; build Grade 4 into the assembled Classroom site with math4 -> grade4 adaptation. Reuse native Algebra 1/Grade 5 teacher generators, never create student links in generators. Use student skill-selection links for games and Understanding Checks. Keep Remedial, Standard and Advanced. Retain bank IDs and diagrams. Do not run legacy tools/grade4-authoring/integration.cjs. Ensure no second independent course navigation or duplicated player engine is exposed.

Before public release, rerun tests against current production main and manually sample diagrams, skill alignment, PDF pagination, phone and smartboard views. The source QA report documents historical tests, not a new run against the latest live code.

See docs/math4/MIGRATION.md and docs/math4/VALIDATION_REPORT.md.
