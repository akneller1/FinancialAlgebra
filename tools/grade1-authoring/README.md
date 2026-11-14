# Grade 1 authoring kit (math1)

Built on the Grade 2 kit, which it imports unchanged (`tools/grade2-authoring/g2lib.py`, `figs2.py`, `checks2.py`), together with the Grade 3 and Grade 5 kits those import. Same family contract, schema, IDs and verifier as Grade 2. Needs Python 3 with Pillow, `rsvg-convert`, and Node 18+ for the schema test.

| File | Role |
|---|---|
| `outline.py` | Standards, units, skills, targets, misconceptions (single source of truth); `--write` → `outline.json` |
| `g1lib.py`, `figs1.py` | Grade 1 helpers and new diagram kinds: `tenframe`, `crossrow`, `lengths` (unit-square strips), `measure` (cubes/clips with gaps, overlaps, mixed sizes), `shapes1` (2-D shapes, turned, open figures), `compose` (pattern-block composites) |
| `units/u01…u12_*.py` | Question families per skill (`f(r, L)`, L = 0 Remedial/cp2, 1 Standard/cp1, 2 Advanced/honors) |
| `build.py` | Practice banks, meta (incl. game eligibility), diagrams, check data. Per skill/level: 12 short answer + 12 MC + 3 error analysis + 1 true/false + 1 select-all + 1 open/matching. Rejects exact and same-number repeats course-wide and caps a prompt template at 5 per skill/level (`G1_TMAX`) |
| `build_checks.py` | Fixed Understanding Check sets (run after `build.py`) |
| `verify.py`, `checks1.py` | Independent verifier (never imports families) |
| `audit1.py` | Scope, reading load, progression, duplicates, distractors, assets, game eligibility → `out/audit.json` |
| `package1.py` | `course-outlines/grade1.json`, `question-banks/math1/manifest.json`, `docs/math1/{curriculum-map.json, coverage.csv, game-eligibility.json}` |
| `sample1.py` | Print sample items: `python3 sample1.py <unit-id> [k]` |
| `tests/schema-adapter.cjs` | Runs the site's `question-bank-adapter.js` on every bank |

Rebuild order: `outline.py --write` → `build.py` → `build_checks.py` → `verify.py` → `VERIFY_CHECKS=1 verify.py` → `audit1.py` → `package1.py`. Builds are deterministic. `G1_NODRAW=1` skips drawing; `G1_ROOT` sets the repository root.
