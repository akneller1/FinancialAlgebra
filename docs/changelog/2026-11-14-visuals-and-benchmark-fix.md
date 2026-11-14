# 2026-11-14 — Pictures for text-described items and Grade 5 benchmark fix (FinancialAlgebra repo)

## Pictures added (70 items)
Each picture is drawn only from numbers in the item's own prompt. The prompt, answer and check data are unchanged.

| Bank | Family | Items | Picture |
|---|---|---|---|
| `question-banks/math2/graphs-data.json` | `sp_text_*` ("A bar graph shows soccer 9, tennis 7, swim 5…") | 23 | the bar graph or picture graph |
| `question-banks/math3/graphs-measurement-data.json` | `pg_half` | 4 | a picture-graph key: one whole star = n, half a star = ? |
| `math4/fractions-equivalent-fractions.json` | `ue_split_parts*` | 30 | the rectangle in equal parts, shaded, before the second cut |
| `math4/geometry-angles-symmetry.json` | `sy_fold_measure*` | 13 | a symmetric figure with a dashed line of symmetry and the shaded half's area |

PNG files are in `question-banks/assets/<course>/<unit>/<id>.png`.

**Deliberately left as text.** Items that ask students to *make* a graph (`mk_text_pics`, `mk_symbols*`) have no picture, because a finished graph would show the answer.

## Grade 5 benchmark estimation (14 items)
Several "Use benchmarks (0, 1/2, or 1) to estimate…" items used fractions far from any benchmark. For example, 1/3 − 2/9 was keyed 1/2, but the exact answer is 1/9.

New rule:
- each fraction is within 1/6 of its benchmark;
- the estimate is within 1/4 of the exact answer.

**What changed in each repaired item.** The ids and keyed estimates stay the same. The two fractions are replaced, and these are rewritten from the new numbers:
- prompt
- steps
- the "exact answer" distractor, student answer or "answer shown"
- check data

**Covered so future builds follow the rule:**
- Families `b_sum`, `b_sum_error` and `b_sum_tf`.
- Generator guard added in `tools/grade5-authoring/units/u05_fraction_add.py` (`b_sum`).
- `tools/grade5-authoring/verify.py`: TOTAL ERRORS 0.

## Production note
- Production builds **Grades 1–3** from FinancialAlgebra commit 0e3c25f and **Grade 4** from 9f29d62. Grade 4 reads `question-banks/math4/<unit>.json`; that folder no longer exists on `main`, where the banks are in `math4/`.
- These fixes reach the live site only after the pins in `classroom/.github/workflows/deploy-site.yml` move to the new commit, and after Grade 4's source path is updated to `math4/`.
- **Grade 5** follows `main` and picks the changes up automatically, until it is pinned.
