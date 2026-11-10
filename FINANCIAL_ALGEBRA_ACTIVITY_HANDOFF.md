# Financial Algebra — Activity Planning Brief for Claude

## Baseline

Read the ten-unit, forty-skill curriculum in src/course.js of the independent repository akneller1/FinancialAlgebra.

**All previous Financial Algebra pilot activities have been deliberately removed.** No old simulations, calculators, worksheet/practice prototypes, or Interactive Math pilots need to be preserved.

Course ID: financial-algebra. Difficulty: **ONE level** (standard). Do not add CP2, CP1, or Honors selectors.

Production website: https://mrksclassroom.com/  
Staging website: https://akneller1.github.io/FinancialAlgebra/

Claude supplies plans and files but does not write directly to GitHub in this workflow.

## Planning requirements

1. Review every unit and its learning goals, including real-life financial reasoning and tradeoffs.
2. Design worthwhile experiences that serve the learning goal: scenario-based decisions, math modeling, interpreting bills and statements, comparing loans, budgeting, debt payoff, investing, taxes, risk, college ROI and retirement.
3. Prioritize educational quality. Do not force a simulation or game into a unit where it does not add learning value.
4. Match the main Mr. K's Classroom design and activity workflow, including teacher controls, student links, printables, answer keys, navigation, mobile usability, and accessibility.
5. Distinguish numerical questions that can be graded deterministically in JavaScript from explanations that require worked reasoning or rubrics. Avoid runtime AI and paid external APIs.
6. For each proposed activity provide the target skills, scenario, user interactions, sample question, underlying math, feedback or rubric, student mode, teacher controls, and validation tests.
7. Explicitly model money rounding, APR conventions, compounding timing, market uncertainty, taxes, and inflation. Label hypothetical values and avoid misleading certainty.
8. Do not collect real student bank-account data or other private financial information.
9. Outline dependencies, suggested build order, expected code modules, testing strategy, and future integration adapter.
10. Keep incomplete activities unlinked until verified. Do not modify the production akneller1/classroom repository.

## Deliverable

Begin with a comprehensive **activity architecture and implementation plan** and several representative fully specified activities, not a bulk unreviewed code drop. After review, supply modular files, automated checks, and a ZIP suitable for inspection and staging integration.
