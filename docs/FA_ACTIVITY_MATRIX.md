# Activity Compatibility Matrix

| Classroom activity | Decision | Financial Algebra implementation | Content it should use |
|---|---|---|---|
| Lesson Plan Generator | **Modify** | `financial/generators/?mode=lesson` — teacher plan or student guided notes, editable sections, document reading, guided scenario, practice, exit ticket, misconceptions, differentiation | Lesson data + bank items for the chosen skill |
| Worksheet Generator | **Modify** | `?mode=worksheet` — 8 formats (Case Study, Compare Two Options, Document Analysis, Budget & Data Analysis, Decision Challenge, Vocabulary & Concepts, Math Applications, Mixed), complexity, writing space, versions A–F, separate key | Extended bank |
| Assessment Generator | **Modify** | `?mode=assessment` — adjustable 20/20/30/30 blueprint, point values, scoring guide, rubrics, model responses | Extended bank |
| Practice Tests | **Modify** | `?mode=practice` — self-checking objective items with worked solutions | Objective items only |
| Flashcards | **Reuse workflow, new deck** | `financial/flashcards/` plus `mkvocab-financial-algebra.js` drop-in for the existing builder | Vocabulary + formula/principle/document cards |
| Cheat Sheets | **Reuse format** | `artifacts/financial-algebra-<unit>-cheat-sheet/cheat-sheet.pdf` | — |
| Showdown | **Reuse** | Existing engine via Classroom bank | Vocabulary, concepts, claims, short calculations |
| Connect 4 | **Reuse** | Existing engine via Classroom bank | Same |
| Tic Tac Toe | **Reuse** | Existing engine via Classroom bank | Same |
| Picture Reveal | **Reuse** | Existing engine via Classroom bank | Same |
| Detective / Whodunnit | **Reuse** | Existing `course-activity.js` (needs ≥10 MC items for selected skills — every unit has 60+) | MC only |
| Escape Room | **Reuse with limits** | Works for calculation-heavy skills (needs integer/numeric answers for locks); not recommended for vocabulary-only selections | Short numeric items |
| Activity Generator (stations, partner checks) | **Replace** | Decision Labs fill the "activity" role with guided decisions | — |
| Interactive Math (lab.js) | **Replace** | `financial/decision-lab/` — 7 steps: situation, options, prediction, investigation (auto-checked), variable changes with live table/chart, recommendation, reflection; teacher view with model answers, rubric, slider lock, printable summary | Lab scenarios |
| Unit Projects | **New, same packaging** | 12 projects (PDF + DOCX student packet, PPTX slides, PDF + DOCX teacher guide, landing page) | — |

**Not forced into games:** open responses, document analysis, and multi-table comparisons (`gameEligible: false`) are excluded from the Classroom export so game engines never show them.
