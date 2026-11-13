// NOTE (2026-11-13): SUPERSEDED for production. Production now releases elementary grades from this repository through its
// own release adapter (akneller1/classroom scripts/integrate-approved-courses.mjs, the Grade 5 model). Use
// docs/math4/MIGRATION.md. This script patched production's shared files directly; it was tested against production
// commit c98a4ed (2026-11-12 morning) and is kept only as a record of every shared-file change Grade 4 needs.
// Grade 4 (math4) site integration. Idempotent: safe to run again (each edit is skipped if already applied).
// Usage (repository root):  node tools/grade4-authoring/integration.cjs [--production-release]
//
// It works on both layouts it was tested on:
//   * the production Classroom repository (akneller1/classroom), with or without the Grade 5 package;
//   * the development repository (akneller1/FinancialAlgebra), where the Grade 5 package is already applied.
// What it does:
//   0. course record (data.js), skill catalog (course-catalog.js), bank manifest(s)
//   1. one resource block in data.js (games, flashcards, Understanding Checks, cheat sheets, vocabulary and printable
//      generators, Interactive Math, projects)
//   2. adds 'math4' next to 'math6' in the shared course lists (app, planner, generators, level labels)
//   3. course color, unit icons, framework strands, standards descriptions, resource details, SEO text, cipher problems
// --production-release also hides the "4th Grade Math · Coming soon" home placeholder once the real course exists.
// Do NOT pass it until Grade 4 is approved for the public site.
const fs = require('fs'), path = require('path');
const ROOT = process.env.G4_ROOT || path.resolve(__dirname, '../..');
const RELEASE = process.argv.includes('--production-release');
const O = require('./outline.json');
const opt = f => { try { return require(f); } catch (e) { return null; } };
const TOOLS = (opt('./interactive/manifest.json') || { tools: [] }).tools;
const PROJ = opt('./projects/projects-registry.json') || {};
const GAMES = require('./games.json');
const ADDED = '2026-11-12', LV = ['Remedial', 'Standard', 'Advanced'], C = 'math4';
const has = f => fs.existsSync(path.join(ROOT, f));
const read = f => fs.readFileSync(path.join(ROOT, f), 'utf8'), write = (f, s) => fs.writeFileSync(path.join(ROOT, f), s);
let applied = 0, skipped = 0; const notes = [];
function edit(file, find, repl, o = {}) {
  if (!has(file)) { if (o.optional) { notes.push('skipped (file not in this repository): ' + file); return; } throw Error('missing file ' + file); }
  let s = read(file);
  if (o.done ? s.includes(o.done) : s.includes(repl)) { skipped++; return; }
  if (!s.includes(find)) { if (o.optional) { notes.push('anchor not found (left unchanged): ' + file + ' :: ' + find.slice(0, 60)); return; } throw Error(file + ': anchor not found: ' + find.slice(0, 90)); }
  write(file, o.all ? s.split(find).join(repl) : s.replace(find, repl)); applied++;
}
const exists = p => { if (!has(p)) throw Error('missing ' + p); return p; };

/* "Treat math4 the way math6 is treated": every shared list, test and label that names math6 also names math4. */
function alongside(file, o = {}) {
  if (!has(file)) { if (o.optional !== false) { notes.push('skipped (file not in this repository): ' + file); return; } throw Error('missing file ' + file); }
  let s = read(file);
  if (/math4|math\[4/.test(s)) { skipped++; return; }
  const before = s;
  s = s.replace(/\[(['"])math5\1, (['"])5th Grade Math\2\], \[(['"])math6\3, /g, "['math4', '4th Grade Math'], ['math5', '5th Grade Math'], ['math6', ");
  s = s.replace(/\[(['"])math6\1, (['"])6th Grade Math\2\]/g, m => /4th Grade Math/.test(s) ? m : "['math4', '4th Grade Math'], " + m);
  s = s.replace(/(^|[\[,(]\s*)(['"])math6\2(?=\s*[,\]])/gm, (m, pre, q) => pre + q + 'math4' + q + ',' + (/\s$/.test(pre) || /, /.test(m + ' ') ? ' ' : '') + q + 'math6' + q);
  s = s.replace(/math\[56\]/g, 'math[456]').replace(/\|math6\)/g, '|math[46])').replace(/\|math6\|/g, '|math6|math4|').replace(/\^math6-/g, '^math[46]-');
  s = s.replace(/math6:'MATH6'/g, "math4:'MATH4',math6:'MATH6'").replace(/math6:'M6'/g, "math4:'M4',math6:'M6'");
  s = s.replace(/c\.id === 'math6'/g, "c.id === 'math4' || c.id === 'math6'").replace(/c\.id !== 'math6'/g, "c.id !== 'math4' && c.id !== 'math6'");
  if (s === before) { if (o.must) throw Error(file + ': no math6 list found'); notes.push('no math6 list found in ' + file); return; }
  write(file, s); applied++;
}

/* ---------------- 0. course record, skill catalog, bank manifest ---------------- */
{
  let d = read('data.js');
  if (!d.includes('"id": "math4"')) {
    const rec = { id: C, name: O.name, color: 'meadow', art: 'fourth', blurb: O.blurb, units: O.units.map(u => ({ id: u.id, name: u.name, artifacts: [] })), comingSoon: false };
    const a5 = '{\n  "id": "math5",', a6 = '{\n  "id": "math6",', anchor = d.includes(a5) ? a5 : a6;
    if (!d.includes(anchor)) throw Error('math5/math6 anchor not found in data.js');
    write('data.js', d.replace(anchor, JSON.stringify(rec, null, 2) + ',\n' + anchor)); applied++;
  } else skipped++;
  let c = read('course-catalog.js');
  if (!c.includes('"math4": {')) {
    const body = {}; O.units.forEach(u => body[u.id] = u.skills.map(s => s[0]));
    const a5 = '  "math5": {', a6 = '  "math6": {', anchor = c.includes(a5) ? a5 : a6;
    if (!c.includes(anchor)) throw Error('math5/math6 anchor not found in course-catalog.js');
    write('course-catalog.js', c.replace(anchor, '  "math4": ' + JSON.stringify(body, null, 2).replace(/\n/g, '\n  ') + ',\n' + anchor)); applied++;
  } else skipped++;
  // The development repository keeps its manifest at the repository root; production keeps it in question-banks/.
  ['question-banks/manifest.json', 'manifest.json'].filter(has).forEach(mfile => {
    const mf = JSON.parse(read(mfile));
    if (!Array.isArray(mf.banks)) return;
    let added = 0;
    O.units.forEach(u => { if (!mf.banks.some(b => b.courseId === C && b.unitId === u.id)) { exists(`question-banks/${C}/${u.id}.json`); mf.banks.push({ courseId: C, unitId: u.id, path: `question-banks/${C}/${u.id}.json`, approved: true }); added++; } });
    if (added) { write(mfile, JSON.stringify(mf, null, 2) + '\n'); applied++; } else skipped++;
  });
}

/* ---------------- 1. data.js resource block ---------------- */
const units = {};
O.units.forEach((u, i) => {
  const A = units[u.id] = [];
  GAMES.games.forEach(g => {
    if (g.units && !g.units.includes(u.id)) return;
    A.push({ title: g.title + ': ' + u.name, path: `worksheet-generator/grade4-games.html?game=${g.id}&unit=${u.id}`, bankFormat: 'topic-games', keepPath: true, gameMode: g.team ? 'Team Games' : 'Individual Review', type: 'Game',
      thumb: exists(`thumbs/math4-game-${g.thumb}.svg`), description: g.description + (g.generated ? '' : ' Remedial, Standard and Advanced questions from the Grade 4 bank.'), level: LV, topics: [u.name, 'Grade 4 game'], added: ADDED });
  });
  A.push({ title: 'Flashcards: ' + u.name, path: `worksheet-generator/grade4-flashcards.html?unit=${u.id}`, bankFormat: 'flashcards', keepPath: true, type: 'Study Guide', thumb: exists('thumbs/math4-flashcards.svg'),
    description: 'Colorful flashcards for vocabulary, key facts, pictures, big ideas, examples and common mistakes.', topics: [u.name], added: ADDED });
  A.push({ title: 'Understanding Check', path: `worksheet-generator/grade4-understanding-check.html?unit=${u.id}`, bankFormat: 'interactive-practice-test', keepPath: true, type: 'Study Guide', thumb: exists('thumbs/math4-understanding-check.svg'),
    description: 'A friendly check of learning: one question at a time or all on one page, hints, worked solutions, retry of missed questions, a printable results page and a teacher summary.', level: LV, topics: [u.name], added: ADDED });
  A.push({ title: 'Understanding Check (Printable Version)', path: `worksheet-generator/practice-test.html#unit=math4-${u.id}`, bankFormat: 'interactive-practice-test', type: 'Study Guide', thumb: 'thumbs/practice-test.svg',
    description: 'Build a printable Understanding Check from the Grade 4 bank, with an answer key and a targeted follow-up.', level: LV, topics: [u.name], added: ADDED });
  const cs = `artifacts/math4-${u.id}-cheat-sheet/worksheet.pdf`;
  A.push({ title: u.name + ' Cheat Sheet', path: exists(cs), thumb: exists(`thumbs/math4-${u.id}-cheat-sheet.jpg`), type: 'Printable',
    description: 'Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It!', topics: ['Cheat sheet', 'Reference', u.name, 'Unit ' + (i + 1)], added: ADDED });
  A.push({ title: 'Vocabulary Activities and Crosswords', path: `worksheet-generator/printables.html#unit=math4-${u.id}&kind=vocabulary`, type: 'Printable', thumb: 'thumbs/vocabulary-prealgebra.svg',
    description: 'Matching, fill-in-the-blank, examples, and crosswords using the Grade 4 unit vocabulary.', level: LV, topics: [u.name], added: ADDED });
  [['error', 'Error Analysis', 'error-generator-foundations.svg', 'Find, explain, and correct mistakes. Includes teacher solutions.'], ['tarsia', 'Tarsia Puzzle', 'tarsia-generator-foundations.svg', 'Match problems and answers to assemble a triangle puzzle.'],
   ['maze', 'Maze', 'maze-generator-foundations.svg', 'Follow a route of correctly answered questions through a maze.'], ['color', 'Color by Number', 'geometry-color-generator-basics-reasoning.svg', 'Solve problems to reveal a color-coded picture.'],
   ['partner', 'Partner Check', 'partner-generator-foundations.svg', 'Solve and compare matched-answer problems in pairs.'], ['stations', 'Station Work', 'stations-generator-foundations.svg', 'Rotate through stations with mixed problem types.'],
   ['who', 'Whodunnit', 'foundations-algebra-whodunnit.jpg', 'Solve clues and narrow down the mystery.']].forEach(k => {
    A.push({ title: k[1] + ' Generator', path: `worksheet-generator/printables.html#unit=math4-${u.id}&kind=${k[0]}`, bankFormat: 'printable-generator', type: 'Printable', thumb: 'thumbs/' + k[2],
      description: k[3] + ' Uses Grade 4 questions and a teacher key.', level: LV, topics: [u.name], added: ADDED });
  });
  TOOLS.filter(t => t.units.includes(u.id)).forEach(t => A.push({ title: t.title, path: exists(`artifacts/${t.slug}/index.html`), bankFormat: 'interactive-math', type: 'Interactive', thumb: exists(`thumbs/${t.slug}.svg`),
    description: t.description, topics: t.topics, added: ADDED }));
  (PROJ['math4-' + u.id] || []).forEach(p => A.push({ title: 'Project: ' + p.title, path: exists(`artifacts/${p.folder}/index.html`), bankFormat: 'projects', keepPath: true, type: 'Project', thumb: exists(`thumbs/${p.folder}.svg`),
    description: p.description, level: LV, topics: [u.name, 'Project', p.theme], added: ADDED }));
});
const block = `/* 4th Grade Math (${ADDED}): Grade 4 game collection, flashcards, Understanding Checks, elementary cheat sheets,
   vocabulary and printable generators from the approved bank, Interactive Math and unit projects (built by tools/grade4-authoring/). */
(function(G){
 var c=G.LIBRARY.courses.find(function(x){return x.id==='math4';});if(!c)return;
 var R=${JSON.stringify(units)};
 c.units.forEach(function(u){(R[u.id]||[]).forEach(function(a){if(!u.artifacts.some(function(x){return x.path===a.path;}))u.artifacts.push(a);});});
 c.planned=false;
})(window);
`;
{
  let d = read('data.js');
  d = d.replace(/\/\* 4th Grade Math \(\d{4}-\d\d-\d\d\)[\s\S]*?\n\}\)\(window\);\n+/, '');
  const anchor = '(function(G){ G.LIBRARY.courses.filter(c=>["precalculus","calculus"].includes(c.id)).forEach(c=>{c.planned=false;}); })(window);\n';
  const at = d.indexOf(anchor);
  if (at < 0) throw Error('data.js anchor not found');
  // exactly one blank line before and after the block, so running this again leaves data.js byte-for-byte the same
  write('data.js', d.slice(0, at + anchor.length) + '\n' + block + '\n' + d.slice(at + anchor.length).replace(/^\n+/, ''));
  fs.mkdirSync(path.join(__dirname, 'patches'), { recursive: true }); fs.writeFileSync(path.join(__dirname, 'patches', 'data.math4-block.js'), block);
}

/* ---------------- 2. shared behavior ---------------- */
// Elementary pages keep their own links (same two generic hooks the Grade 5 package uses; added only if missing).
edit('resource-standards.js', "function kind(a){\n const p=a.path||'';", "function kind(a){\n if(a.keepPath)return null;\n const p=a.path||'';");
edit('app.js', "  function gameMode(a) {\n    var f = activityFormat(a);", "  function gameMode(a) {\n    if (a.gameMode) return a.gameMode;\n    var f = activityFormat(a);");
edit('app.js', "    { id: 'practice', name: 'Practice Activities', formats: ['proofs'] },", "    { id: 'practice', name: 'Practice Activities', formats: ['proofs'] },\n    { id: 'projects', name: 'Projects', formats: ['projects'] },", { done: "{ id: 'projects', name: 'Projects'" });
edit('app.js', "        category('practice', 'Practice Activities', practiceFormats) +", "        category('practice', 'Practice Activities', practiceFormats) +\n        category('projects', 'Projects', ['projects']) +", { done: "category('projects', 'Projects'" });
// app.js: math4 behaves like math6 (unit pages with generators, games and study guides)
{
  let s = read('app.js');
  if (!/math4/.test(s)) {
    const b = s;
    s = s.replace(/math6: (-?\d+)/, (m, n) => 'math4: ' + (Number(n) - 1.5) + ', ' + m);                       // course order: before Grade 5 and Grade 6
    s = s.replace("math6: 'sixth'", "math4: 'fourth', math6: 'sixth'");
    s = s.replace(/(^|[\[,]\s*)'math6'(?=\s*[,\]])/gm, (m, pre) => pre + "'math4', 'math6'");
    s = s.replace(/c\.id === 'math6'/g, "c.id === 'math4' || c.id === 'math6'").replace(/c\.id !== 'math6'/g, "c.id !== 'math4' && c.id !== 'math6'");
    s = s.replace(/^(\s*)math6: 'Ratios, rational numbers & expressions\.',/m, "$1math4: 'Factors, fractions & geometry.',\n$1math6: 'Ratios, rational numbers & expressions.',");
    if (s === b) throw Error('app.js: no math6 references found');
    write('app.js', s); applied++;
  } else skipped++;
}
// unit illustration on every Grade 4 unit card (only where app.js still has the per-course card branch)
edit('app.js', "            return '<li><div class=\"unit algebra-unit-card\" data-color=\"' + esc(c.color || '') + '\" data-course=\"' + esc(c.id) + '\">' +\n",
  "            return '<li><div class=\"unit algebra-unit-card\" data-color=\"' + esc(c.color || '') + '\" data-course=\"' + esc(c.id) + '\">' +\n              (c.id === 'math4' ? '<img class=\"el-unit-icon\" src=\"thumbs/math4-unit-' + esc(u.id) + '.svg\" alt=\"\" width=\"160\" height=\"120\" loading=\"lazy\">' : '') +\n", { done: 'thumbs/math4-unit-', optional: true });   // newer app.js draws one shared unit card for every course
// the 'fourth' course art exists in production; older copies (the development repository) need it
{
  let s = read('app.js');
  if (!/\n    fourth:\n/.test(s)) {
    const art = "    fourth:\n      '<svg class=\"art\" viewBox=\"0 0 200 160\" aria-hidden=\"true\" focusable=\"false\">' +\n      '<rect class=\"f-soft\" x=\"24\" y=\"26\" width=\"152\" height=\"108\" rx=\"10\"/>' +\n" +
      "      '<rect class=\"f\" x=\"40\" y=\"44\" width=\"60\" height=\"24\"/><rect class=\"s-thin\" x=\"40\" y=\"44\" width=\"120\" height=\"24\" fill=\"none\"/><path class=\"s-thin\" d=\"M70 44 V68 M100 44 V68 M130 44 V68\"/>' +\n" +
      "      '<circle class=\"f\" cx=\"52\" cy=\"100\" r=\"8\"/><circle class=\"f\" cx=\"76\" cy=\"100\" r=\"8\"/><circle class=\"f\" cx=\"100\" cy=\"100\" r=\"8\"/><circle class=\"f\" cx=\"52\" cy=\"122\" r=\"8\"/><circle class=\"f\" cx=\"76\" cy=\"122\" r=\"8\"/><circle class=\"f\" cx=\"100\" cy=\"122\" r=\"8\"/>' +\n" +
      "      '<path class=\"s\" d=\"M126 126 L160 126 M126 126 L154 96\" fill=\"none\"/>' +\n      '</svg>',\n";
    if (!s.includes('    sixth:\n')) throw Error('app.js: course art anchor not found');
    write('app.js', s.replace('    sixth:\n', art + '    sixth:\n')); applied++;
  } else skipped++;
}
// Production only, and only on request: the real course replaces the "Coming soon" home placeholder.
if (RELEASE) {
  const ph = "    { id: 'grade4', name: '4th Grade Math', color: 'green', art: 'fourth', units: [], comingSoon: true, homePlaceholder: true },\n";
  const s0 = read('app.js');
  if (s0.includes(ph)) { write('app.js', s0.replace(ph, '')); applied++; } else skipped++;
}
else if (has('app.js') && read('app.js').includes("{ id: 'grade4', name: '4th Grade Math'")) notes.push("production placeholder '4th Grade Math · Coming soon' left in place (pass --production-release to replace it with the real course)");

// level labels and course lists in the shared generators
['worksheet-generator/course-game.html', 'worksheet-generator/games/course-activity.js', 'worksheet-generator/approved-flashcards.html', 'worksheet-generator/vocabulary-builder.js',
 'worksheet-generator/menu/match-game.js', 'worksheet-generator/algebra2-bank-native.js', 'worksheet-generator/menu/course-catalog-bridge.js', 'coverage.html', 'skills.html',
 'worksheet-generator/practice/practice.js', 'worksheet-generator/planner/scope-algebra2.js', 'worksheet-generator/planner/course.js', 'worksheet-generator/planner/planner-ui.js'].forEach(f => alongside(f));
// "Understanding Check" wording in the printable practice page (never "Assessment Readiness" or "Test Prep" for Grade 4)
{
  const f = 'worksheet-generator/practice/practice.js';
  if (has(f)) {
    let s = read(f);
    if (!s.includes("'GRADE '+config.unit.charAt(4)+' · UNDERSTANDING CHECK'")) {
      const g5 = "(/^math5-/.test(config.unit)?'GRADE 5 · UNDERSTANDING CHECK':'ASSESSMENT READINESS · VERSION 2')+'</span><h1>'+(/^math5-/.test(config.unit)?'Understanding Check':'Assessment Readiness Check')+'</h1>";
      const base = "function controls(){return '<section class=\"pt-card\"><span class=\"pt-eyebrow\">ASSESSMENT READINESS · VERSION 2</span><h1>Assessment Readiness Check</h1>";
      const repl = "(/^math[45]-/.test(config.unit)?'GRADE '+config.unit.charAt(4)+' · UNDERSTANDING CHECK':'ASSESSMENT READINESS · VERSION 2')+'</span><h1>'+(/^math[45]-/.test(config.unit)?'Understanding Check':'Assessment Readiness Check')+'</h1>";
      if (s.includes(g5)) s = s.replace(g5, repl);
      else if (s.includes(base)) s = s.replace(base, "function controls(){return '<section class=\"pt-card\"><span class=\"pt-eyebrow\">'+" + repl);
      else throw Error(f + ': Understanding Check heading anchor not found');
      write(f, s); applied++;
    } else skipped++;
  }
}

// projects registry for the Activity Builder (Printable Generator, kind=project)
{
  const f = 'worksheet-generator/menu/printables-projects.js';
  if (!has(f)) notes.push('skipped (file not in this repository): ' + f);
  else if (Object.keys(PROJ).length) {
    let s = read(f);
    if (!s.includes('"math4-' + O.units[0].id + '"')) {
      const anchor = '  PR.PROJECTS = {\n';
      if (!s.includes(anchor)) throw Error(f + ': anchor not found');
      const body = Object.entries(PROJ).map(([k, v]) => '  ' + JSON.stringify(k) + ': ' + JSON.stringify(v, null, 2).replace(/\n/g, '\n  ')).join(',\n') + ',\n';
      s = s.replace(anchor, anchor + body).replace(/(Courses: Algebra 1, Geometry, Algebra 2,)( 5th Grade,)?/, '$1 4th Grade,$2');
      write(f, s); applied++;
    } else skipped++;
  }
}

/* ---------------- 3. look, standards, details ---------------- */
edit('styles.css', "[data-color=\"teal\"] { --c-bg: var(--teal-bg); --c-fg: var(--teal-fg); --c-tint: var(--teal-tint); --c-text: var(--teal-text); }",
  "[data-color=\"teal\"] { --c-bg: var(--teal-bg); --c-fg: var(--teal-fg); --c-tint: var(--teal-tint); --c-text: var(--teal-text); }\n/* 4th Grade Math: fresh meadow-green palette and a unit illustration on every unit card. */\n:root { --meadow-bg: #2fbf71; --meadow-fg: #06281a; --meadow-tint: #e2f8ea; --meadow-text: #0d6b3c; }\n[data-color=\"meadow\"] { --c-bg: var(--meadow-bg); --c-fg: var(--meadow-fg); --c-tint: var(--meadow-tint); --c-text: var(--meadow-text); }\n.el-unit-icon { display:block; width:100%; max-width:160px; height:auto; margin:0 0 .4rem; border-radius:14px; }", { done: '--meadow-bg' });
{ // framework strands (one record per unit)
  let s = read('massachusetts-framework-strands.js');
  if (!s.includes('"courseId": "math4"')) {
    const recs = O.units.map(u => '  ' + JSON.stringify({ courseId: C, unitId: u.id, strand: u.strand, relationship: 'grade-level' }, null, 2).replace(/\n/g, '\n  ')).join(',\n') + ',\n';
    const anchor = ' var records=[\n';
    if (!s.includes(anchor)) throw Error('strands anchor');
    write('massachusetts-framework-strands.js', s.replace(anchor, anchor + recs)); applied++;
  } else skipped++;
}
{ // short standard descriptions shown next to skills (only codes that are not already described)
  const f = 'worksheet-generator/menu/standards.js';
  if (has(f)) {
    let s = read(f); const SHORT = require('./standards-short.json'); const add = [];
    // the site's normalizer writes sub-standards without the last dot (4.NF.B.3a)
    Object.entries(SHORT).forEach(([k0, v]) => { const k = k0.replace(/\.([a-z])$/, '$1'); if (!s.includes("'" + k + "':")) add.push("    '" + k + "': '" + v.replace(/'/g, "\\'") + "',"); });
    if (add.length) {
      const anchor = "    /* Grade 4–5 */\n";
      if (s.includes(anchor)) s = s.replace(anchor, anchor + add.join('\n') + '\n');
      else { const a2 = "    '6.RP.A.1':"; if (!s.includes(a2)) throw Error(f + ': anchor not found'); s = s.replace(a2, add.join('\n') + '\n' + a2); }
      write(f, s); applied++;
    } else skipped++;
  } else notes.push('skipped (file not in this repository): ' + f);
}
{ // resource details for cheat sheets (2 pages, reference sheet)
  let r = read('resource-details.js'); const add = [];
  O.units.forEach(u => { const k = `artifacts/math4-${u.id}-cheat-sheet/worksheet.pdf`; if (!r.includes(JSON.stringify(k) + ':')) add.push('  ' + JSON.stringify(k) + ': ' + JSON.stringify({ pages: 2, referenceSheet: true })); });
  if (add.length) { write('resource-details.js', r.replace(/\n\};\s*$/, ',\n' + add.join(',\n') + '\n};\n')); applied++; } else skipped++;
}
edit('scripts/build-site.mjs', "  math6: {\n    title: \"Free 6th Grade Math Worksheets & Games\",", "  math4: {\n    title: \"Free 4th Grade Math Worksheets, Games & Activities\",\n    description: \"Free 4th grade math games, worksheets, flashcards, cheat sheets, projects and interactive tools for place value, multiplication, division, fractions, decimals, measurement, angles and more.\"\n  },\n  math6: {\n    title: \"Free 6th Grade Math Worksheets & Games\",", { optional: true, done: 'Free 4th Grade Math Worksheets' });
{ // Escape Room cipher problems: one Grade 4 family per unit (whole-number answers 1–25)
  const f = 'worksheet-generator/games/cipher-questions.js';
  if (has(f)) {
    let s = read(f);
    if (!s.includes("case 'g4-place-value'")) {
      const P = fs.readFileSync(path.join(__dirname, 'patches', 'cipher-math4.js'), 'utf8').split('/*---SPLIT---*/');
      if (!s.includes(' math6:{') || !s.includes(' default: return null;')) throw Error(f + ': anchors not found');
      s = s.replace(' math6:{', P[0].trim().replace(/^/, ' ') + '\n math6:{').replace(' default: return null;', P[1].replace(/^\n+|\s+$/g, '') + '\n default: return null;');
      write(f, s); applied++;
    } else skipped++;
  } else notes.push('skipped (file not in this repository): ' + f);
}
{ // Escape Room themes (one per unit)
  const f = 'worksheet-generator/games/escape-themes.json';
  if (has(f)) {
    const T = JSON.parse(read(f)), mine = require('./patches/escape-themes-math4.json'); let n = 0;
    Object.entries(mine).forEach(([k, v]) => { if (!T[k]) { T[k] = v; n++; } });
    if (n) { write(f, JSON.stringify(T, null, 1) + '\n'); applied++; } else skipped++;
  } else notes.push('skipped (file not in this repository): ' + f);
}
{ // vocabulary block for the Vocabulary Activities generator
  const f = 'worksheet-generator/vocabulary-data-middle-grades.js';
  if (has(f)) {
    let s = read(f); const blk = fs.readFileSync(path.join(__dirname, 'patches', 'vocabulary-math4.js'), 'utf8').trim();
    const re = /\/\* MATH4-VOCAB-START[\s\S]*?MATH4-VOCAB-END \*\//;
    const n = re.test(s) ? s.replace(re, () => blk) : s.replace(/\s*$/, '\n' + blk + '\n');
    if (n !== s) { write(f, n); applied++; } else skipped++;
  } else notes.push('skipped (file not in this repository): ' + f);
}
// cache strings so browsers pick up the new catalog
['index.html', 'activity.html'].filter(has).forEach(f => { let s = read(f), n = s.replace(/(data|resource-details|course-catalog)\.js\?v=[a-z0-9-]+/g, '$1.js?v=grade4-20261112').replace(/app\.js\?v=[a-z0-9-]+/g, 'app.js?v=grade4-20261112'); if (n !== s) { write(f, n); applied++; } else skipped++; });
console.log('math4 integration: data.js block (' + Object.values(units).reduce((a, x) => a + x.length, 0) + ' resources), ' + applied + ' edits applied, ' + skipped + ' already present');
notes.forEach(n => console.log('  note: ' + n));
