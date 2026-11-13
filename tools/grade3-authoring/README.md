# Grade 3 authoring kit (math3)

Python 3 (+ Pillow, `rsvg-convert`), Node 18+, Playwright/Chromium. Reuses the Grade 5 kit (`tools/grade5-authoring/g5lib.py`,
`figs.py`) by import — do not copy it.

| File | Role |
|---|---|
| `outline.py` | Standards, units, skills, targets, misconceptions (single source of truth) |
| `g3lib.py`, `figs3.py` | Grade 3 helpers and diagram kinds |
| `units/u01…u11_*.py` | Question families per skill |
| `build.py` / `build_checks.py` | Practice banks / fixed Understanding Check sets |
| `verify.py`, `checks3.py` | Independent answer verifier |
| `audit.py`, `report.py`, `sample.py` | Content audit + curriculum map, coverage, sample sheets |
| `content_g3.py`, `build_content.py` | Flashcards, vocabulary, cheat-sheet source, worked examples, teaching notes |
| `projects/` | Project content (`projects3.py`), builder, registry; `print/print.cjs` |
| `staging/assemble-grade3.mjs` | Preview assembler hook |
| `tests/` | display lint, print overflow, browser suites |

## Rebuild order

```bash
cd tools/grade3-authoring
python3 outline.py --write
python3 build.py                 # clears and redraws question-banks/assets/math3/<unit>/
python3 build_checks.py          # must follow build.py
python3 verify.py && VERIFY_CHECKS=1 python3 verify.py
node tests/display-lint.cjs
python3 build_content.py
# cheat sheets: run the Classroom scripts/cheat-sheets/build.cjs (needs katex) on scripts/cheat-sheets/content/math3-*.cjs
python3 projects/build_projects.py && node print/print.cjs && python3 projects/build_projects.py --svg-thumbs
node tests/print-overflow.cjs
python3 report.py && python3 audit.py
# then the preview + browser tests in docs/math3/INTEGRATION.md
```

Environment: `G3_NODRAW=1` skips diagram drawing, `G3_DEBUG=1` prints family attempts.
