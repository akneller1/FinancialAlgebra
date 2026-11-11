# Financial Algebra Resource Library — Integration Manifest (Batch 1, complete course)

**For:** ChatGPT (integration into `akneller1/FinancialAlgebra`) · **Course:** `financial-algebra` · **Level:** standard (stored as `cp1` in Classroom-schema banks)

## Install
Unzip at the **repository root**. All paths are new; nothing existing is overwritten (`src/`, `index.html`, `styles.css`, `package.json` untouched). Pages reference `../../styles.css` / `../styles.css` from the repo root.

## What is included
| Area | Count | Path |
|---|---|---|
| Question items (extended bank) | 1,445 (27–58 per skill; all 40 skills) | `financial/banks/<unit>.json` |
| Classroom-schema export (validated with unchanged production adapter) | 1,274 | `question-banks/financial-algebra/<unit>.json` |
| Generators: Lesson Plan, Worksheet (8 formats), Assessment, Practice Test | 1 app, all units | `financial/generators/index.html?unit=<id>&mode=lesson\|worksheet\|assessment\|practice` |
| Decision Labs (7-step guided, teacher view) | 10 (one per unit) | `financial/decision-lab/index.html?lab=<unitId>[&teacher=1]` |
| Flashcards | 228 cards | `financial/flashcards/index.html?unit=<id>`; drop-in `mkvocab-financial-algebra.js` |
| Cheat sheets (2-page PDF + HTML) | 10 | `artifacts/financial-algebra-<unit>-cheat-sheet/` |
| Projects (student PDF/DOCX, slides PPTX, teacher guide PDF/DOCX, landing page, 100-pt rubric) | 12 (2 for Budgeting, 1 per other unit, + capstone) | `artifacts/financial-algebra-project-<slug>/` |
| Resource manifest + staging hub | — | `financial/resources.json`, `financial/index.html` |
| Docs | — | `docs/FA_IMPLEMENTATION_PLAN.md`, `docs/FA_ACTIVITY_MATRIX.md` |

Projects: survive-on-your-salary, twelve-month-goal-plan (U2) · job-offer-showdown (U1) · emergency-fund-plan (U3) · escape-the-debt-trap (U4) · your-first-car (U5) · investment-plan (U6) · rent-or-buy (U7) · protect-a-household (U8) · compare-education-pathways (U9) · retirement-strategy + build-your-financial-future capstone (U10).

## Integration tasks for ChatGPT
1. **Unit pages:** in `src/site.js`, replace the disabled “Coming soon” shortcuts with links from `financial/resources.json` (`resources.lessonPlan`, `worksheet`, `assessment`, `practiceTest`, `flashcards`, `cheatSheet`, `decisionLab.path`, `projects[]`). Update `tests/site.test.mjs` assertions that currently require “Activities coming soon”/`aria-disabled` (the forbidden pilot file list is still respected — no collisions).
2. **Classroom games:** add manifest entries `{courseId:'financial-algebra', unitId, path:'question-banks/financial-algebra/<unit>.json', approved:true}` after review, and add `financial-algebra` to `course-catalog.js` with the existing skill IDs. Show the level selector as a single “Standard” (`cp1`) option for this course. Recommended games: Showdown, Connect 4, Tic Tac Toe, Picture Reveal, Detective; Escape Room only for calculation-heavy skills.
3. Optional: load `financial/flashcards/mkvocab-financial-algebra.js` where the Classroom vocabulary builder is used.

## Rebuild
```
node scripts/build-banks.mjs && node scripts/build-print.mjs && python3 scripts/build_office.py && node scripts/build-hub.mjs
```
(Playwright + Chromium for PDFs; python-docx and python-pptx for Office files.) Suggested `package.json` script: `"build:fa": "<the line above>"`.

## Test results (this build)
- `npm test` on the dev repo with this ZIP overlaid: **35/35 pass** (22 existing + 13 new).
- `tests/fa-finance.test.mjs`: interest, APY, annuities, loans/amortization reconcile to the cent, lease, card payoff, avalanche ≤ snowball, course tax table, insurance, housing, inflation, retirement.
- `tests/fa-content.test.mjs`: every item complete; unique IDs/prompts; one correct MC answer; numeric answer = stored value; open responses have ≥4 parts, rubric, and model response; ≥25 items per skill; Classroom export passes the production adapter; labs finite at default and extreme slider values; projects have 100-point rubrics and all five files.
- `tests/fa-browser.cjs` (Playwright, not in `npm test`): **124 page checks, 0 failures** — every generator mode and worksheet format for every unit, every lesson, flashcards, every lab (teacher and mobile), cheat sheets, project link integrity, hub, no console errors, no horizontal overflow at 390 px.

## Known limitations
- Lesson Plan/Worksheet/Assessment are Financial-Algebra-native pages styled like the Classroom generators, not modifications of the production generator code (which is math-skill-specific).
- Tax figures use an explicit illustrative Course Tax Table, not current IRS values; returns and rates are hypothetical and labeled as such.
- Skills with the fewest items: income-skill-03 and college-skill-03/04 (27). All others ≥ 28.
- The capstone and project PDFs use system fonts when Google Fonts are unavailable at build time.
- Student Decision Lab responses are stored only in the browser (best effort) and in the printable summary; no data leaves the device.
