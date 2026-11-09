# Grade 5 Math — Question-bank handoff notes

**Status: outline only.** Questions are NOT built or imported yet. This is preparation for a separate Claude authoring pass.

## Curriculum source of truth

\`course-outlines/grade5.json\`, derived from the attached \`Grade_5_Math_Scope_and_Sequence.pdf\` (4 pages).

- Course ID: \`math5\`
- Units: **13**, in exactly the supplied order
- Lessons / skill labels: **80**
- Each skill ID: \`<unit-id>-skill-01\`, \`-02\`, etc., 1-based and stable
- Every skill and unit is currently flagged as \`outline\` with no resources linked.

The PDF cites Pennsylvania-formatted standards and eligible-content codes. Preserve them in the outline, rather than silently substituting Massachusetts or national codes. Some source codes are abbreviated (e.g., Unit 8 \`A-F.2.1.3\`) and the Unit 3 standard narrative mentions two-digit divisors despite its one-digit divisor unit title. These details are deliberately retained from the document pending teacher review. **Unit 13 continues onto PDF page 4**, with ruler measurement and central tendencies (mean, median, range, and mode).

## Expected Claude outputs later

1. Read the JSON and existing Algebra 1/Grade 6 bank format from \`akneller1/classroom\` as compatibility examples.
2. Draft well-balanced, age-appropriate question families for all 80 skills, with numeric, fraction, decimal, word-problem, and diagram/table styles where appropriate.
3. Include unique question IDs, exact stable skill IDs, deterministic/verified answers, worked solutions, and the required original site's approved-bank formats. Do not generate just one template per skill and call it comprehensive.
4. Avoid overloading activities with inappropriate question types, e.g. do not force an open-ended explanation into a game demanding a single value.
5. Use Grade 5 mathematical scope, not Financial Algebra's single-level assumption by default; grade-level difficulty settings can be chosen when the banks are authored.
6. Deliver modular files or a ZIP and a clear integration manifest. Claude **cannot directly write to GitHub** in this workflow; ChatGPT will inspect and connect the files.
7. Keep unfinished content out of the student-facing manifest. Do not change any live production file until the bank is reviewed, validated, and approved.

## Initial testing requirements

Check Grade 5 arithmetic restrictions, decimal precision, whole-number / decimal division scope, equivalence, mixed numbers, graphs restricted to quadrant I, and exact rectangle/composite-volume rules as given in the source. Design automated checks for valid answers, distractors, balanced topical coverage, repeated near-duplicates, and age appropriateness. Curriculum decisions beyond the supplied PDF should be flagged as proposals rather than silently added.
