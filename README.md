# Financial Algebra — standalone development

A separate, browser-only Financial Algebra course prototype for eventual integration into [Mr. K's Classroom](https://mrksclassroom.com/).

**Status: Phase 1 pilot.** The site contains a 10-unit course outline. Budgeting, Credit Cards, and Investing are the only functional pilot units. Other units are clearly marked as planned.

## Current functionality

- Matching 10-unit outline and CP2 / CP1 / Honors difficulty levels.
- Three configurable, deterministic simulations: monthly budgeting, credit-card repayment, compound investing.
- Parametric short-answer practice across each pilot unit and level; student checks reveal worked solutions only after submitting.
- Print-friendly six-question student worksheets and matching teacher answer keys.
- No runtime AI, login, external API, database, paid hosting, or third-party JavaScript dependency.
- Built-in automated financial mathematics and question generation tests.

## View the site

Publish this repo as a **GitHub Pages** site:
1. Open repository **Settings → Pages**.
2. In **Build and deployment**, choose **Deploy from a branch**.
3. Set Branch to **main**, directory to **/(root)**, then **Save**.
4. Use the URL GitHub displays under Pages. Typical project URL format: \`https://akneller1.github.io/FinancialAlgebra/\`.

To work locally, serve the repo from any basic local HTTP server, e.g. \`python -m http.server 8000\`, and visit \`http://localhost:8000\`. Opening \`index.html\` directly with \`file://\` is not supported because browser ES modules require HTTP(S).

## Testing

Requires Node.js 20+: \`npm test\`.

## Architecture

- \`src/course.js\` — course and stable unit/skill IDs.
- \`src/engine.js\` — pure reusable financial formulas; no UI dependency.
- \`src/questions.js\` — reproducible scenarios, answer keys, feedback, worksheets.
- \`src/app.js\` — standalone interface and print views.
- \`style.css\` — responsive visual design.
- \`tests/\` — automated calculations, syllabus, and question checks.
- \`INTEGRATION.md\` — eventual integration plan for Mr. K's Classroom.

## Important limitations

This is **not yet a complete course**. There are no lesson-plan or activity generators, standards mappings, long-form written responses, games, full question banks, or interactive tools for the other seven units yet. Keys are public in this prototype and are not secure for controlled student assessments. Models are simplified, educational illustrations: credit interest is calculated monthly (real credit card interest usually uses daily balances), investing assumes constant hypothetical returns, and budgeting withholding is not a tax calculation.

**Production isolation:** This repository is independent of \`akneller1/classroom\`. No code was changed in the production classroom repo for this pilot.
