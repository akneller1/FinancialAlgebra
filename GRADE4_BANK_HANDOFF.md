# Grade 4 Math — question-bank development handoff

**Status: outline only. No question banks, games, generators, or interactive activities have been built for Grade 4.**

## Source and curriculum contract

- Original upload: \`Grade4ScopeandSequence.pdf\`, 15 pages, headed \`Math Expressions Grade 4 – Scope and Sequence\`.
- Staging data: \`course-outlines/grade4.json\` in the independent \`akneller1/FinancialAlgebra\` repository.
- Course ID: **\`math4\`**
- **12 units**, all in the PDF's order.
- **107 learning targets**: concise editorial groupings of the PDF's objectives, **not** the actual textbook lesson names.
- **177 estimated instructional days** and **128 reported textbook lessons** summed from source headings. The latter figures are not a count of learning targets. Unit 11 reports 15 days for 15 lessons plus an assessment; do not silently alter it.
- Individual units have \`sourcePages\`, \`estimatedDays\`, \`reportedLessons\`, \`skills\`, \`objectiveGroups\`, and \`resourceNote\`.
- Unlike the Grade 5 PDF, this Grade 4 file does **not** list specific standard or eligible-content codes. The \`standards\` arrays are intentionally empty; do not invent codes.
- Resource: \`Math Expressions\`; **Unit 3 excludes lesson 3.2** and **Unit 8 excludes lesson 8.5**, which the original source describes as having switched x/y tables. Those exact notes are stored in \`resourceNote\`.
- Unit 3's objectives carry onto PDF page 4; Unit 9's carry onto page 12. PDF page 9 is a blank header page between Units 7 and 8.
- One source title spells 'MEASURMENT'; the UI normalizes it to 'Measurement'. The objectives include source category labels 'Calculus' and 'Trigonometry' for comparisons and angles; the JSON explicitly identifies these source labels, without promoting these topics to advanced coursework.
- The source repeats some decimal-modeling objectives in Unit 11. The outline groups repeated items rather than creating misleading duplicate skill identifiers.

## Authoring rules for Claude

1. **Read** the JSON and the attached PDF if available, and inspect the production \`akneller1/classroom\` bank format to match its current approved schema.
2. Work unit-by-unit, preserving exact course and unit IDs. A skill's ID is \`<unit-id>-skill-01\`, \`-02\`, etc., using the current order in \`skills\`.
3. Generate a broad age-appropriate set of unique, parameterized question families for each topic. Check numerical ranges and no-dependency requirements. Include genuine word problems, visual fraction models, numerical expressions, grids, data tables, graphs, measurement prompts, and geometric diagrams where relevant.
4. Preserve the PDF's constraints: factors/multiples up to 100, primes/composites up to 50, numbers through six digits, standard division of two-/three-digit by one-digit, decimal places through hundredths, fractions through twelfths on the described number-line tasks, and elapsed-time questions within two adjacent hours.
5. Include question IDs, stable skill IDs, correct answer keys, worked solutions, math-formatting and diagram metadata, and independent deterministic verification. Ensure that questions are valid for the specific activities they will serve.
6. Preserve the source's Math Expressions lesson exclusions, even if developing more adaptable original tasks.
7. Grade 4 is **not** Financial Algebra. Do not inherit Financial Algebra's one-level requirement without a separate decision. The final question-bank format should be compatible with the site's normal difficulty mechanisms, but the UI can keep difficulty options hidden until that decision is made.
8. Clearly mark unbuilt activities Coming soon. Do not claim teacher-only keys can be secured on public GitHub Pages.
9. Claude cannot directly modify GitHub in the user's workflow. Have Claude deliver the completed modular bank files or ZIP for ChatGPT to inspect, validate, and integrate into the staging repository.
10. Do not modify the production \`akneller1/classroom\` site until approved after regression testing.

## Pilot sequence for future development

Prioritize Units 1, 3, 5, 7, 9, and 11 for robust question generation and printable activities, then complete the remaining units. Focus early interactive-tool experimentation on quadrilaterals, angles and polygons, number patterns, fractions, measurement, and data representations.
