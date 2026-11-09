# Reusing this staging site for future math classes

The FinancialAlgebra GitHub repository now also hosts the **Grade 5 Math** curriculum outline, reusing the same classroom styling. The repository name still reflects its original Financial Algebra pilot, but its layout can host further development courses.

## Current development pages

- Financial Algebra: \`index.html\` · live pilot activities
- Grade 5 Math: \`grade5.html\` · outline only
- Grade 1 Math: \`grade1.html\` · Illustrative Mathematics, sections and standards
- Grade 2 Math: \`grade2.html\` · Illustrative Mathematics, sections and standards
- Grade 3 Math: `grade3.html` · outline only, standards and guiding questions
- Grade 4 Math: \`grade4.html\` · outline only, with pacing and source objective categories
- Both are independent from the production \`akneller1/classroom\` repository.

## How to add another course

1. Convert the attached scope-and-sequence document into a single JSON file under \`course-outlines/<slug>.json\`. Preserve unit order, exact lesson boundaries, and any source standards. Note pages where the text continues or contains ambiguities.
2. Follow the \`course-outlines/grade5.json\` schema: \`schemaVersion\`, \`id\`, \`name\`, \`description\`, \`status\`, \`source\`, \`standards\` map, and \`units\` with \`id\`, \`name\`, \`status\`, \`skills\`, \`standards\`, and \`sourcePages\`.
3. Create a small course page (use \`grade5.html\` as the base) loading the common \`styles.css\`, \`site-overrides.css\`, and its own tiny bootstrap file (like \`src/grade5-site.js\`) calling \`mountOutline(course)\` from \`src/outline-template.js\`.
4. Add a link in the navigation for both development course pages. New course IDs must be unique and compatible with the eventual production course catalog.
5. Write tests matching the source document's unit and skill counts, topic order, standards references, page continuations and stable IDs.
6. Only after teacher review, begin adding authentic question families and activity integrations. Never show disabled tools as if they already work.

## Stable content contract

The skill ID for item index \`i\` (zero-based) in a unit is \`<unit-id>-skill-<two-digit-number>\`. Example: \`place-value-skill-01\`.

That ID pattern is intentionally consistent with the existing Classroom \`course-catalog.js\` convention. **Do not rename established IDs when Claude produces question banks**. Use each unit's \`id\` unchanged, and include the matching \`courseId\` (\`math5\`) on each question.

The staging site's outline renderer and CSS may be reused without copying any Financial Algebra-specific simulations. Avoid mixing financial content into other grade levels.

## Future import into main Classroom

Do not push changes to \`akneller1/classroom\` while authoring in this staging repository. Import the finished course later into a staging branch of the production repository, adapt the question-bank manifest, integrate generators and activities, and run full regression checks. Production changes require a separate review.
