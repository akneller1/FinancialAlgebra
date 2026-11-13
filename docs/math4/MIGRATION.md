# 4th Grade Math: production migration manifest

**Do not run this until Grade 4 is approved for the public site.** Until then production (`akneller1/classroom`) keeps
its "4th Grade Math · Coming soon" placeholder and no Grade 4 files.

Production releases elementary grades the way it released Grade 5 (`docs/grade5-elementary-release-model.md` in the
Classroom repository): the course stays in this repository, and the Classroom Pages workflow checks out the approved
files and assembles them into `_site/` with a release adapter. Grade 4 is built for that model. The development preview
already assembles Grade 4 into the real Classroom shell with `tools/grade4-authoring/staging/assemble-grade4.mjs`; the
production adapter should do the same things with production paths.

## Source of truth (this repository)

| What | Path |
|---|---|
| Course outline (10 units, 49 skills, 35 standards) | `course-outlines/grade4.json` (generated from `tools/grade4-authoring/outline.py`) |
| Approved banks | `manifest.json` entries `courseId: "math4"`, files `question-banks/math4/<unit>.json` |
| Question metadata (types, distractor reasons) | `question-banks/math4/meta/` and `math4/meta/` (identical) |
| Diagrams (762) | `question-banks/assets/math4/<unit>/<id>.png` |
| Players | `worksheet-generator/grade4-{games,flashcards,understanding-check}.html`, `worksheet-generator/grade4/`, `worksheet-generator/elementary/` |
| Cheat sheets, tools, projects | `artifacts/math4-*` |
| Thumbnails | `thumbs/math4-*` |
| Planner teaching notes | `tools/grade4-authoring/staging/teaching-notes.json` (from `build-teaching-notes.py`) |
| Unit vocabulary | `tools/grade4-authoring/patches/vocabulary-math4.js` |
| Resource list per unit | built by `assembleGrade4()` from `outline.json`, `games.json`, `interactive/manifest.json`, `projects/projects-registry.json` |

## Steps for ChatGPT (production, once approved)

1. **Release adapter.** In `scripts/integrate-approved-courses.mjs`, add a Grade 4 section beside Grade 5 (or call
   `assembleGrade4({source, out})` from this repository's `tools/grade4-authoring/staging/assemble-grade4.mjs`, which
   already does all of the following):
   - copy the Grade 4 players, `artifacts/math4-*`, `thumbs/math4-*`, banks, metadata and diagrams to `_site/grade4/`,
     and write `_site/grade4/data.js`, `course-catalog.js`, `question-banks/manifest.json` and an `index.html` alias
     that redirects to `/#grade4`;
   - adapt each approved `math4` bank to `courseId: "grade4"` at `question-banks/grade4/<unit>.json` and add it to the
     native manifest (exactly as Grade 5 is adapted to `grade5`);
   - write the course catalog (`grade4-main-catalog.js`, like `grade5-main-catalog.js`) with the card list
     `assembleGrade4()` returns, changing relative `grade4/…` paths to absolute `/grade4/…`;
   - write `grade4-native-notes.js` (`MKPLAN_TEACH.grade4`) and `grade4-native-resources.js` (vocabulary under
     `grade4-<unit>` and the project registry) and load them in `lesson-planner.html` and `printables.html`, the way
     the Grade 5 files are loaded.
2. **Shared files that name the released elementary course** (each currently names only `grade5`):
   - `worksheet-generator/planner/planner-ui.js`: add `'grade4'` to the approved-bank course list (`PA8`) and to the two
     course regular expressions near lines 199–200 and 721. Without it the planner can draw the first day before the
     banks load (the preview works around this with a small redraw script; production should fix it at the source).
   - `app.js`: show the Projects section for `grade4` (`c.id === 'grade5'` → `['grade4','grade5'].indexOf(c.id) >= 0`);
     remove the `{ id: 'grade4', … comingSoon: true, homePlaceholder: true }` placeholder.
   - Course landing page `courses/grade4.html`, sitemap entry and the course picker, as for Grade 5.
3. **Workflow.** In `.github/workflows/deploy-site.yml`, the existing checkout of this repository already provides the
   files; run the Grade 4 step after Grade 5 and add a Grade 4 audit like `scripts/audit-grade5-release.cjs`
   (units, banks, links, thumbnails, diagrams resolve inside `_site/`).
4. **Tests.** Production tests that count courses, units, skills or projects move by +1 course, +10 units, +49 skills,
   +10 projects, +11 public pages. Update their expectations.
5. **Verify** on the assembled `_site/`: `node scripts/test-public-site.cjs`, the Grade 4 audit, and the browser
   tests in `tools/grade4-authoring/tests/` (`browser-preview.cjs`, `browser-grade4.cjs` with `G4_PREFIX=grade4/`,
   `browser-tools.cjs`, `browser-generators.cjs --all` with `G4_SET=grade4`).

## Shared dependencies

The Grade 4 players use these Classroom files (copied into `_site/grade4/` by the adapter, never changed):
`question-bank-adapter.js`, `question-bank-loader.js`, `worksheet-generator/core/math-display.{js,css}`,
`worksheet-generator/games/skill-setup.js`, `assets/favicon.svg`. The native generators are used unchanged.
`worksheet-generator/elementary/` is a configuration-driven version of the Grade 5 runtime: a later grade needs only
its own `config.js` and three thin pages.

## Not used any more

`tools/grade4-authoring/integration.cjs` patched production's shared files directly (tested against production
`c98a4ed` on 2026-11-12, before the Grade 5 release adapter existed). It is kept only as a record of each shared-file
change; do not run it on the current production repository.
