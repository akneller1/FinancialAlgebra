# 2026-11-14 — Grade 4: Line Plot Builder and 43 question pictures

**Base:** commit 9f29d62. This is the commit `deploy-site.yml` pins for Grade 4. It is not on `main`, so this update goes on a branch made from it (see "How to publish").

## New Interactive Math tool: Line Plot Builder (`artifacts/math4-line-plot-builder/`)
Unit: Data, Line Plots and Word Problems (`data-line-plots-word-problems`). Standard: 4.MD.B.4. This was the only Grade 4 unit without a tool.
- Students make a line plot of measurements to the nearest 1/2, 1/4 or 1/8 inch. They add an X by tapping a mark, or by moving the arrow and pressing Add X.
- Three data sets are included: ribbon lengths, bean sprout heights and weekly rainfall. Students can also start a blank plot.
- The readout shows the least and greatest values, greatest − least, the most common value(s) and the total of all measurements, all as fractions or mixed numbers.
- Five "Try this" challenges. None is checked when the page opens.
- Teacher notes and a "What should I notice?" panel.
- Source: `tools/grade4-authoring/interactive/tools.py` (tool 10). The tool is in `interactive/manifest.json`, so `assemble-grade4.mjs` adds its card to the unit automatically.
- Thumbnail: `thumbs/math4-line-plot-builder.svg`, made by `tools/grade4-authoring/thumbs.py`.
- Test: `tools/grade4-authoring/tests/browser-tools.cjs` now covers it. All 10 tools pass at 1280×800, 1920×1080, 1024×600 and 390×780. Set `CHROME=/path/to/chrome` to choose a browser.

## Pictures for 43 questions
The same pictures as the FinancialAlgebra `main` update of 2026-11-14 (`math4/`), now in the banks production actually reads:
- `question-banks/math4/fractions-equivalent-fractions.json`: 30 "split into equal parts" items.
- `question-banks/math4/geometry-angles-symmetry.json`: 13 "fold and measure" items.
- The PNGs are in `question-banks/assets/math4/<unit>/`.
- Only the `diagram` field changed; every other field is unchanged.

## How to publish
1. On GitHub, create a branch named `grade4-release` from commit 9f29d62. The ChatGPT structural prompt, section 4b, has the steps.
2. Upload this ZIP to that branch.
3. Point the Grade 4 checkout in `deploy-site.yml` to the new commit.

Checked with the classroom deploy pipeline, with Grade 4 assembled from this tree: the Grade 4 release structure check, test-public-site, test-elementary-generators, test-shared-course-catalogs and test-elementary-asteroid all pass.
