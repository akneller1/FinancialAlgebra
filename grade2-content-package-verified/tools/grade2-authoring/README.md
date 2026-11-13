# Grade 2 authoring kit (math2)

You need Python 3 (with Pillow, python-docx and python-pptx), `rsvg-convert`, Node 18+, and Playwright/Chromium.

The kit reuses the Grade 3 kit (`tools/grade3-authoring/g3lib.py`, `figs3.py`, `checks3.py`) and the Grade 5 kit (`g5lib.py`, `figs.py`)
by import. Do not copy them.

| File | Role |
|---|---|
| `outline.py` | Standards, units, skills, targets and misconceptions (single source of truth) |
| `g2lib.py`, `figs2.py` | Grade 2 helpers and diagram kinds (number lines with jumps, coins and bills, rulers, counters, solids, bar models, digital clocks, tally charts, counting charts, base-ten blocks, single-unit bar graphs, paired partitions) |
| `units/u01…u12_*.py` | Question families per skill (368 families) |
| `build.py` / `build_checks.py` | Practice banks / fixed Understanding Check sets |
| `verify.py`, `checks2.py` | Independent answer verifier |
| `audit.py`, `report.py`, `sample.py` | Content audit and curriculum map, coverage, sample listings |
| `content_g2.py`, `build_content.py` | Flashcards, vocabulary, cheat-sheet source, worked examples and teaching notes |
| `projects/` | Project content (`projects2.py`), builder and registry; `print/print.cjs` |
| `staging/assemble-grade2.mjs` | Preview assembler hook |
| `tests/` | Display lint, print overflow and browser suites |

## Rebuild order

```bash
cd tools/grade2-authoring
python3 outline.py --write
python3 build.py                 # clears and redraws question-banks/assets/math2/<unit>/
python3 build_checks.py          # must follow build.py
python3 verify.py && VERIFY_CHECKS=1 python3 verify.py
node tests/display-lint.cjs
python3 build_content.py
# cheat sheets: run the Classroom scripts/cheat-sheets/build.cjs (needs katex) on scripts/cheat-sheets/content/math2-*.cjs
python3 projects/build_projects.py /tmp/g2proj && node print/print.cjs /tmp/g2proj/jobs.json && python3 projects/build_projects.py /tmp/g2proj --svg-thumbs
node tests/print-overflow.cjs /tmp/g2proj
python3 report.py && python3 audit.py
# then the preview and browser tests in docs/math2/INTEGRATION.md
```

Environment settings: `G2_NODRAW=1` skips diagram drawing, and `G2_DEBUG=1` prints family attempts.
