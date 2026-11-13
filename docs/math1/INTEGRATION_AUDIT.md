# Grade 1 — independent integration-readiness audit

**Branch:** grade1-question-bank  
**Current decision:** DO NOT RELEASE OR ENABLE STUDENT GAMES.  
**Mathematical verifier:** Passed (TOTAL ERRORS 0), but it does not check English question semantics.  
**Shared Classroom schema adapter:** Passed across all 8 banks while they remain unapproved.  
**Independent semantic QA:** FAILED (193 high-confidence findings).  
**Editorial approval:** Pending for all banks. Public Pages and production code remain untouched.

## Verified inventory

- 8 Grade 1 units, 93 stable skill IDs, 8,370 questions (30 per skill per level).
- 3,405 PNG diagrams, all with expected 720 × 480 file headers.
- 8,370 metadata records; the shared question-bank adapter accepts the banks without registering them as verified for students.
- The existing independent mathematical verifier finds no errors against stored calculation inputs.
- Questions remain in the separate question-banks/math1/ folder and are absent from the public root manifest.
- Branch-only GitHub Actions runs the independent Python arithmetic/image verifier, full-bank adapter audit, and semantic audit. It cannot deploy the website.

## High-confidence release blockers

Counts are findings per category, not necessarily unique question IDs (categories may overlap). The rules are intentionally narrow, so these are a minimum, not an exhaustive review.

| Category | Findings | Example |
|---|---:|---|
| Start-unknown addition stories | 96 | Receives 3 more and finishes with 8; answer claims the starting amount is 8 instead of 5 |
| Parts count vs. fraction name | 34 | Asks what equal parts are called, answers 2 or 4 instead of halves/fourths |
| Answer absent from pictured shapes | 33 | Asks for a circle while the picture shows no circle |
| Counting sides vs. shape name | 14 | Asks how many sides, answers hexagon instead of 6 |
| Tens count vs. ones-place question | 9 | Stored check answers number of tens when question asks for ones |
| Two triangles / hexagon | 6 | Joins two triangles along one side and incorrectly claims hexagon |
| Longer/shorter reversed | 1 | Comparison asked in question differs from stored answer |
| **Total high-confidence findings** | **193** | |

These issues occur in both the original family generator and the later deduplication rewording layer. Fix the source and resulting banks, not just a superficial display label.

## Editorial and integration issues

| Finding | Count | Needed |
|---|---:|---|
| 1 tens / 1 ones grammar | 125 | Use 1 ten and 1 one; repair prompts, choices, solutions, alt text and generator source |
| Ambiguous ones wording | 65 | Say ones digit or loose ones rather than ambiguous count of ones |
| **Total wording findings** | **190** | |

Additional coverage gaps:

- **Puzzle Masters:** 86 of the 279 skill × level combinations contain fewer than four distinct eligible text-only short-answer pairs. A teacher may select one valid skill and still be unable to launch the game. The engine needs a safe visual-card fallback or suitable questions, without silently changing the teacher's skill selection.
- **Skill alignment:** Sampled items include 6 + 0 under a skill specifically about adding a one-digit number to a two-digit number, and an unrelated tally-graph question under a make-ten addition skill. Correct arithmetic is not proof that the question assesses its declared learning target.
- **Difficulty calibration:** Thirty problems at each label does not prove Remedial/Standard/Advanced appropriately differ in cognitive demand.
- **Provenance:** All 8,370 source notes say Original Claude-authored. Verify attribution or replace the claim.
- **Visual inspection:** PNGs were machine-validated, but systematic human visual review of all 3,405 pictures was not done.
- **Duplication:** Original report says 390 cross-skill duplicated items (4.7%). Branch audit uses a different normalization and is not directly comparable.

## Required remediation order

1. Read the full GitHub Actions artifact grade1-semantic-report.json for every flagged question and failure category.
2. Fix the original question families and re-presentation templates so the same bugs cannot recur.
3. Surgically repair every affected question, preserving stable IDs and intended skill. A start-unknown story must remain start-unknown: changing the story into an easier result-unknown problem merely to retain its wrong answer is not acceptable.
4. Keep stored check inputs, answer, choices, correct flags, distractor metadata, solution steps, PNGs and alt text synchronized.
5. Re-run these three commands and require zero errors in all of them:
   - python tools/grade1-authoring/verify1.py
   - node scripts/audit-grade1-bank.cjs
   - node scripts/audit-grade1-semantics.cjs
6. Independently check **skill alignment** for all 93 skills, compare level demand, and spot-check real rendered diagrams and activities in a browser.
7. Keep every bank **approved:false, teacherUse:false**. Editorial approval and public release remain separate decisions.

## Review-only image and question viewer

From the repository root after checking out the branch, run:

python3 -m http.server 8000

Then open http://localhost:8000/tools/grade1-authoring/preview.html

The standalone page shows actual questions, pictures and solutions by unit, skill, level and format. It is **not** a published game or a release to students.

## Files and safeguards

- Branch-only workflow: .github/workflows/grade1-branch-qa.yml
- Full-bank adapter audit: scripts/audit-grade1-bank.cjs
- Semantic audit: scripts/audit-grade1-semantics.cjs
- Independent math/image verifier: tools/grade1-authoring/verify1.py
- Bank source: question-banks/math1/
- Authoring source: tools/grade1-authoring/
- Curriculum: course-outlines/grade1.json

**No production course catalog, homepage, root manifest, or Pages deployment was changed.**
