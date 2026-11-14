# Grade 1–3 Interactive Math

25 hands-on tools for 1st, 2nd and 3rd Grade Math, modeled on the Grade 5 Interactive Math tools (`math5-*`). Every unit in
Grades 1–3 lists at least one tool under **Interactive Math**.

Each tool has:
- a live model with large + / − controls (mouse, touch and keyboard);
- six **Try this** challenges that tick off as students reach them (none is done on load);
- a closed **What should I notice?** panel;
- **Teacher view** with teaching notes, standards and links to a two-page **Explore & Reflect worksheet** and **teacher key**
  (`worksheet.pdf`, `teacher-key.pdf` in the tool folder);
- zoom, **Fit**, **Present** and **Reset** from the shared elementary shell (`worksheet-generator/elementary/el-tool-shell.js`);
- a thumbnail (`thumbs/<slug>.svg`). No network calls; nothing is saved except the display zoom.

## Files

| File | Role |
|---|---|
| `tools_g1.py`, `tools_g2.py`, `tools_g3.py` | Tool definitions: controls, script, challenges, notices, teacher notes, standards, worksheet Q&A |
| `build.py` | Writes `artifacts/math{1,2,3}-*/index.html` and `tools/grade{1,2,3}-authoring/interactive/manifest.json`; `--print` also makes the PDFs and thumbnails |
| `tests/browser-tools.cjs` | Loads every tool, plays all six challenges with the on-screen controls, fuzzes every button, checks Teacher view, Fit and Reset |
| `worksheet-generator/elementary/el-tool-kit.js` | Shared helpers plus the clock, graph and equal-shares engines used by several tools |

The grade assemblers (`tools/grade{1,2,3}-authoring/staging/assemble-grade{N}.mjs`) read the manifests and list each tool as an
`Interactive` card (`bankFormat: interactive-math`) in every unit named in its `units`.

## Rebuild

```bash
python3 tools/elementary-interactive/build.py --print     # pages, manifests, PDFs and thumbnails
node tools/elementary-interactive/tests/browser-tools.cjs # must print PASS
```

## Tools

| Grade | Tool | Units |
|---|---|---|
| 1 | Ten-Frame Builder | add-subtract-10, add-subtract-20, word-problems-20 |
| 1 | Tens and Ones Builder (with Compare) | tens-ones, count-120, compare-numbers |
| 1 | Equal Sign Balance | equal-sign, add-subtract-20 |
| 1 | Hundred Chart Hopper (1–120) | count-120, add-subtract-100 |
| 1 | Clock Explorer (hour, half hour) | telling-time |
| 1 | Measure with Cubes (gaps and overlaps) | measuring-length |
| 1 | Tally and Picture Graph Builder | data |
| 1 | Equal Shares (halves, fourths) | shapes-equal-shares |
| 2 | Place-Value Blocks to 1,000 | place-value-1000, count-compare-1000, add-subtract-1000 |
| 2 | Number Line Jumps | add-subtract-100, add-subtract-1000, length-number-line, count-compare-1000 |
| 2 | Arrays and Odd or Even | odd-even-arrays |
| 2 | Bar Model Builder | word-problems-100, add-subtract-20, add-subtract-100 |
| 2 | Clock to Five Minutes (a.m./p.m.) | time-money |
| 2 | Coin and Bill Counter | time-money |
| 2 | Ruler and Line Plot | measuring-length, graphs-data |
| 2 | Picture and Bar Graph Builder | graphs-data |
| 2 | Equal Shares and Square Grids | shapes-equal-shares |
| 3 | Equal Groups Explorer (multiply, share, group) | multiplication-meaning, division-meaning, patterns-unknowns-two-step |
| 3 | Break-Apart Arrays | properties-fact-strategies, area |
| 3 | Multiplication Table Patterns | patterns-unknowns-two-step, properties-fact-strategies, multiplication-meaning |
| 3 | Rounding Number Line (with Estimate) | addition-subtraction-1000 |
| 3 | Fraction Bars and Number Lines (with Compare) | understanding-fractions, equivalent-comparing-fractions |
| 3 | Clocks and Elapsed Time | time-volume-mass |
| 3 | Scaled Graph Builder | graphs-measurement-data |
| 3 | Area and Perimeter Grid (rectangles and painted shapes) | area, perimeter-shapes |

## Production

The Classroom deploy (`akneller1/classroom`, `.github/workflows/deploy-site.yml`) checks out Grades 1, 2 and 3 from this
repository at pinned commits. After this branch is merged, update the three `ref:` values for Grade 3, Grade 2 and Grade 1
to the merge commit so the tools are published. No Classroom script needs to change: the existing `integrate-grade{1,2,3}.mjs`
scripts already copy `artifacts/math{N}-*` and `thumbs/math{N}-*` and use the cards the assemblers produce.
