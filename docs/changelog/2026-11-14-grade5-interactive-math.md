# 2026-11-14 — Grade 5 Interactive Math for the three units that had none (FinancialAlgebra repo)

| Unit | Tool |
|---|---|
| Decimal Operations | Decimal Place-Value Builder (existing tool, now also listed here: decimals, × 10 and ÷ 10) |
| Geometry and Classifying Shapes | **Quadrilateral Family** (new): change the sides, height and slant; a live checklist shows which of trapezoid, parallelogram, rectangle, rhombus and square fit, and why. Uses the inclusive trapezoid definition and says so in the teacher notes. 5.G.B.3–4 |
| Data, Line Plots, and Problem Solving | **Line Plot Fair Share** (new): build a line plot in eighths of a liter, find the total and the fair share (total ÷ number of jars), and see what one new jar does to it. 5.MD.B.2 |

- The new tools use the same page shell and `TOOL` challenge API as the other `math5-*` tools. Each has five challenges (none is ticked when the page opens), teacher notes, a 2-page worksheet and key, and a thumbnail.
- Source: `tools/grade5-authoring/interactive/tools_20261114.py`, which writes `math5-<slug>/index.html` and the print jobs. It reuses the worksheet layout from `worksheets.py`. Print with `node tools/grade5-authoring/print/print.cjs /tmp/g5new/jobs.json`.
- `grade5-resource-catalog.js`: `tools` map entries added for the three units.
- Checks:
  - All 10 challenges were played in Chrome: both tools reach 5 of 5, with no page errors.
  - The Classroom production build with these files passes `audit-grade5-release` (12 interactive resources, 0 defects) and `test-grade5-deployment`.
- **Not done:** Grade 4 "Data, Line Plots, and Multi-Step Word Problems" still has no tool. Production Grade 4 is built from a pinned older commit. Once the pin moves, list `math5-line-plot-fair-share` there or build a Grade 4 tool.
