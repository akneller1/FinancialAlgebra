// Grade 5 (math5) site integration. Idempotent: safe to run again (each edit is skipped if already applied).
// Usage (repository root): node tools/grade5-authoring/integration.cjs
// 1. Inserts the Grade 5 resource block into data.js (games, flashcards, Understanding Check, cheat sheets,
//    vocabulary and printable generators, Interactive Math, projects).
// 2. Adds 'math5' next to 'math6' in the shared course lists (app, planner, generators, level labels), the
//    elementary color, projects registry, framework strands, resource details and site SEO.
// Every edit names its exact anchor text and stops with an error if the anchor is missing.
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const O = require('./outline.json');
const TOOLS = require('./interactive/manifest.json').tools;
const PROJ = require('./projects/projects-registry.json');
const ADDED = '2026-11-11', LV = ['Remedial', 'Standard', 'Advanced'];
const read = f => fs.readFileSync(path.join(ROOT, f), 'utf8'), write = (f, s) => fs.writeFileSync(path.join(ROOT, f), s);
let applied = 0, skipped = 0;
function edit(file, find, repl, opt = {}) {
  let s = read(file);
  if (opt.done ? s.includes(opt.done) : s.includes(repl)) { skipped++; return; }
  if (!s.includes(find)) throw Error(file + ': anchor not found: ' + find.slice(0, 90));
  s = opt.all ? s.split(find).join(repl) : s.replace(find, repl);
  write(file, s); applied++;
}
const exists = p => { if (!fs.existsSync(path.join(ROOT, p))) throw Error('missing ' + p); return p; };

/* ---------------- 0. course record, skill catalog, bank manifest ---------------- */
{
  let d = read('data.js');
  if (!d.includes('"id": "math5"')) {
    const rec = { id: 'math5', name: O.name, color: 'sunshine', art: 'fifth', blurb: O.blurb, units: O.units.map(u => ({ id: u.id, name: u.name, artifacts: [] })), comingSoon: false };
    const anchor = '{\n  "id": "math6",';
    if (!d.includes(anchor)) throw Error('math6 anchor not found in data.js');
    d = d.replace(anchor, JSON.stringify(rec, null, 2) + ',\n' + anchor); write('data.js', d); applied++;
  } else skipped++;
  let c = read('course-catalog.js');
  if (!c.includes('"math5": {')) {
    const body = {}; O.units.forEach(u => body[u.id] = u.skills.map(s => s[0]));
    const anchor = '  "math6": {';
    if (!c.includes(anchor)) throw Error('math6 anchor not found in course-catalog.js');
    c = c.replace(anchor, '  "math5": ' + JSON.stringify(body, null, 2).replace(/\n/g, '\n  ') + ',\n' + anchor); write('course-catalog.js', c); applied++;
  } else skipped++;
  const mf = JSON.parse(read('question-banks/manifest.json'));
  let added = 0;
  O.units.forEach(u => { if (!mf.banks.some(b => b.courseId === 'math5' && b.unitId === u.id)) { exists(`question-banks/math5/${u.id}.json`); mf.banks.push({ courseId: 'math5', unitId: u.id, path: `question-banks/math5/${u.id}.json`, approved: true }); added++; } });
  if (added) { write('question-banks/manifest.json', JSON.stringify(mf, null, 2) + '\n'); applied++; } else skipped++;
}

/* ---------------- 1. data.js block ---------------- */
const GAMES = [['math-quest', 'Math Quest', 'quest'], ['treasure-trail', 'Treasure Trail', 'treasure'], ['space-explorer', 'Space Explorer', 'space'], ['math-builders', 'Math Builders', 'builders'],
  ['picture-reveal', 'Picture Reveal', 'reveal'], ['math-race', 'Math Race', 'race'], ['math-soccer', 'Math Soccer', 'soccer'], ['connect-four', 'Connect 4', 'connect4'],
  ['puzzle-masters', 'Puzzle Masters', 'puzzle'], ['fraction-frenzy', 'Fraction Frenzy', 'frenzy']];
const GAME_DESC = { 'math-quest': 'Unlock six lands on an adventure map by answering correctly. Play alone or as a class.', 'treasure-trail': 'Follow the treasure map stone by stone and collect gems.',
  'space-explorer': 'Earn fuel cells to fly from planet to planet.', 'math-builders': 'Earn a building for your town with every correct answer.',
  'picture-reveal': 'Uncover tiles to reveal a hidden picture.', 'math-race': 'Two to four teams race; a correct answer moves the team car one space.',
  'math-soccer': 'Two teams kick the ball toward the goal with correct answers.', 'connect-four': 'Two teams answer to earn discs. Four in a row wins.',
  'puzzle-masters': 'Flip cards and match each problem to its answer, alone or with a partner.', 'fraction-frenzy': 'Match fraction models to fractions, including equivalent fractions and simplest form.' };
const units = {};
const TEAM = ['math-race', 'math-soccer', 'connect-four'];   // whole-class team games; the others are played alone or as a class
O.units.forEach((u, i) => {
  const A = units[u.id] = [];
  GAMES.forEach(([g, t, th]) => {
    if (g === 'fraction-frenzy' && !/^fraction-/.test(u.id)) return;
    A.push({ title: t + ': ' + u.name, path: `worksheet-generator/grade5-games.html?game=${g}&unit=${u.id}`, bankFormat: 'topic-games', keepPath: true, gameMode: TEAM.includes(g) ? 'Team Games' : 'Individual Review', type: 'Game', thumb: exists(`thumbs/math5-game-${th}.svg`),
      description: GAME_DESC[g] + (g === 'fraction-frenzy' ? ' Fraction models are drawn exactly from the chosen numbers.' : ' Remedial, Standard and Advanced questions from the Grade 5 bank.'), level: LV, topics: [u.name, 'Grade 5 game'], added: ADDED });
  });
  A.push({ title: 'Flashcards: ' + u.name, path: `worksheet-generator/grade5-flashcards.html?unit=${u.id}`, bankFormat: 'flashcards', keepPath: true, type: 'Study Guide', thumb: exists('thumbs/math5-flashcards.svg'),
    description: 'Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.', topics: [u.name], added: ADDED });
  A.push({ title: 'Understanding Check', path: `worksheet-generator/grade5-understanding-check.html?unit=${u.id}`, bankFormat: 'interactive-practice-test', keepPath: true, type: 'Study Guide', thumb: exists('thumbs/math5-understanding-check.svg'),
    description: 'A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.', level: LV, topics: [u.name], added: ADDED });
  A.push({ title: 'Understanding Check (Printable Version)', path: `worksheet-generator/practice-test.html#unit=math5-${u.id}`, bankFormat: 'interactive-practice-test', type: 'Study Guide', thumb: 'thumbs/practice-test.svg',
    description: 'Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.', level: LV, topics: [u.name], added: ADDED });
  const cs = `artifacts/math5-${u.id}-cheat-sheet/worksheet.pdf`;
  A.push({ title: u.name + ' Cheat Sheet', path: exists(cs), thumb: exists(`thumbs/math5-${u.id}-cheat-sheet.jpg`), type: 'Printable',
    description: `Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for ${u.focus || u.name}.`.replace(' for ' + undefined, ''), topics: ['Cheat sheet', 'Reference', u.name, 'Unit ' + (i + 1)], added: ADDED });
  A.push({ title: 'Vocabulary Activities and Crosswords', path: `worksheet-generator/printables.html#unit=math5-${u.id}&kind=vocabulary`, type: 'Printable', thumb: 'thumbs/vocabulary-prealgebra.svg',
    description: 'Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.', level: LV, topics: [u.name], added: ADDED });
  [['error', 'Error Analysis', 'error-generator-foundations.svg', 'Find, explain, and correct mistakes. Includes teacher solutions.'], ['tarsia', 'Tarsia Puzzle', 'tarsia-generator-foundations.svg', 'Match problems and answers to assemble a triangle puzzle.'],
   ['maze', 'Maze', 'maze-generator-foundations.svg', 'Follow a route of correctly answered questions through a maze.'], ['color', 'Color by Number', 'geometry-color-generator-basics-reasoning.svg', 'Solve problems to reveal a color-coded picture.'],
   ['partner', 'Partner Check', 'partner-generator-foundations.svg', 'Solve and compare matched-answer problems in pairs.'], ['stations', 'Station Work', 'stations-generator-foundations.svg', 'Rotate through stations with mixed problem types.'],
   ['who', 'Whodunnit', 'foundations-algebra-whodunnit.jpg', 'Solve clues and narrow down the mystery.']].forEach(k => {
    A.push({ title: k[1] + ' Generator', path: `worksheet-generator/printables.html#unit=math5-${u.id}&kind=${k[0]}`, bankFormat: 'printable-generator', type: 'Printable', thumb: 'thumbs/' + k[2],
      description: k[3] + ' Uses Grade 5 questions and a teacher key.', level: LV, topics: [u.name], added: ADDED });
  });
  TOOLS.filter(t => t.unit === u.id).forEach(t => A.push({ title: t.title, path: exists(`artifacts/${t.slug}/index.html`), bankFormat: 'interactive-math', type: 'Interactive', thumb: exists(`thumbs/${t.slug}.jpg`),
    description: t.description, topics: t.topics, worksheet: exists(`artifacts/${t.slug}/worksheet.pdf`), answerKey: exists(`artifacts/${t.slug}/teacher-key.pdf`), added: ADDED }));
  (PROJ['math5-' + u.id] || []).forEach(p => A.push({ title: 'Project: ' + p.title, path: exists(`artifacts/${p.folder}/index.html`), bankFormat: 'projects', keepPath: true, type: 'Project', thumb: exists(`thumbs/${p.folder}.jpg`),
    description: p.description, level: LV, topics: [u.name, 'Project', p.theme], added: ADDED }));
});
// The Fraction Explorer and Area Model Explorer also serve Unit 6 (fractions × ÷); the Place-Value Builder also serves Unit 3 (decimals).
[['fraction-multiplication-division', 'math5-area-model-explorer'], ['fraction-multiplication-division', 'math5-fraction-explorer'], ['decimal-operations', 'math5-place-value-builder']].forEach(([unit, slug]) => {
  const t = TOOLS.find(x => x.slug === slug); units[unit].push({ title: t.title, path: `artifacts/${slug}/index.html`, bankFormat: 'interactive-math', type: 'Interactive', thumb: `thumbs/${slug}.jpg`,
    description: t.description, topics: t.topics, worksheet: `artifacts/${slug}/worksheet.pdf`, answerKey: `artifacts/${slug}/teacher-key.pdf`, added: ADDED });
});
const block = `/* 5th Grade Math (2026-11-11): Grade 5 game collection, flashcards, Understanding Checks, elementary cheat sheets,
   vocabulary and printable generators from the approved bank, Interactive Math and unit projects (built by tools/grade5-authoring/). */
(function(G){
 var c=G.LIBRARY.courses.find(function(x){return x.id==='math5';});if(!c)return;
 var R=${JSON.stringify(units)};
 c.units.forEach(function(u){(R[u.id]||[]).forEach(function(a){if(!u.artifacts.some(function(x){return x.path===a.path;}))u.artifacts.push(a);});});
 c.planned=false;
})(window);
`;
{
  let d = read('data.js');
  d = d.replace(/\/\* 5th Grade Math \(2026-11-11\)[\s\S]*?\n\}\)\(window\);\n\n/, '');
  const anchor = '(function(G){ G.LIBRARY.courses.filter(c=>["precalculus","calculus"].includes(c.id)).forEach(c=>{c.planned=false;}); })(window);\n';
  if (!d.includes(anchor)) throw Error('data.js anchor not found');
  d = d.replace(anchor, anchor + '\n' + block + '\n');
  write('data.js', d); fs.mkdirSync(path.join(__dirname, 'patches'), { recursive: true }); fs.writeFileSync(path.join(__dirname, 'patches', 'data.math5-block.js'), block);
}

/* ---------------- 2. shared lists ---------------- */
// Grade 5 pages keep their own links: resource-standards.js would otherwise rewrite any path containing
// flashcards / connect-four / picture-reveal / showdown into the generic course-game player.
edit('resource-standards.js', "function kind(a){\n const p=a.path||'';", "function kind(a){\n if(a.keepPath)return null;\n const p=a.path||'';");
edit('app.js', "  function gameMode(a) {\n    var f = activityFormat(a);", "  function gameMode(a) {\n    if (a.gameMode) return a.gameMode;\n    var f = activityFormat(a);");
// app.js
edit('app.js', "var courseOrder = { math6: 0,", "var courseOrder = { math5: -1, math6: 0,");
edit('app.js', "var byCourse = { math6: 'sixth',", "var byCourse = { math5: 'fifth', math6: 'sixth',");
edit('app.js', "    sixth:\n", "    fifth:\n      '<svg class=\"art\" viewBox=\"0 0 200 160\" aria-hidden=\"true\" focusable=\"false\">' +\n      '<rect class=\"f-soft\" x=\"24\" y=\"26\" width=\"152\" height=\"108\" rx=\"10\"/>' +\n      '<path class=\"f\" d=\"M 70 80 L 70 40 A 40 40 0 0 1 110 80 Z\"/><circle class=\"s\" cx=\"70\" cy=\"80\" r=\"40\" fill=\"none\"/>' +\n      '<path class=\"s-thin\" d=\"M 30 80 H 110 M 70 40 V 120\"/>' +\n      '<rect class=\"f\" x=\"126\" y=\"94\" width=\"14\" height=\"14\"/><rect class=\"f\" x=\"140\" y=\"94\" width=\"14\" height=\"14\"/><rect class=\"f\" x=\"126\" y=\"80\" width=\"14\" height=\"14\"/><rect class=\"s-thin\" x=\"126\" y=\"66\" width=\"28\" height=\"42\" fill=\"none\"/>' +\n      '</svg>',\n    sixth:\n");
edit('app.js', "['algebra', 'geometry', 'algebra2', 'prealgebra', 'prealgebra7', 'math6', 'precalculus', 'calculus', 'statistics', 'discrete'].indexOf(c.id) >= 0 ? '' : '<span class=\"course-wip-label\">Coming Soon</span>'",
  "['algebra', 'geometry', 'algebra2', 'prealgebra', 'prealgebra7', 'math6', 'math5', 'precalculus', 'calculus', 'statistics', 'discrete'].indexOf(c.id) >= 0 ? '' : '<span class=\"course-wip-label\">Coming Soon</span>'");
edit('app.js', "(c.id === 'math6' || c.id === 'prealgebra7' || c.id === 'prealgebra') ? units(c.units.length) + ' with ' + lessonCount(c)", "(c.id === 'math5' || c.id === 'math6' || c.id === 'prealgebra7' || c.id === 'prealgebra') ? units(c.units.length) + ' with ' + lessonCount(c)");
edit('app.js', "c.id !== 'prealgebra7' && c.id !== 'math6') {", "c.id !== 'prealgebra7' && c.id !== 'math6' && c.id !== 'math5') {");
edit('app.js', "c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6') {\n            return '<li><div class=\"unit algebra-unit-card\" data-color=\"' + esc(c.color || '') + '\" data-course=\"' + esc(c.id) + '\">' +\n              '<h3>",
  "c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6' || c.id === 'math5') {\n            return '<li><div class=\"unit algebra-unit-card\" data-color=\"' + esc(c.color || '') + '\" data-course=\"' + esc(c.id) + '\">' +\n              (c.id === 'math5' ? '<img class=\"g5-unit-icon\" src=\"thumbs/math5-unit-' + esc(u.id) + '.svg\" alt=\"\" width=\"160\" height=\"120\" loading=\"lazy\">' : '') +\n              '<h3>");
edit('app.js', "['algebra2', 'prealgebra', 'prealgebra7', 'math6', 'precalculus', 'calculus', 'statistics', 'discrete'].indexOf(c.id) >= 0) {\n          var selectedUnit", "['algebra2', 'prealgebra', 'prealgebra7', 'math6', 'math5', 'precalculus', 'calculus', 'statistics', 'discrete'].indexOf(c.id) >= 0) {\n          var selectedUnit");
edit('app.js', "c.id === 'prealgebra7' || c.id === 'math6' || c.id === 'algebra2'; });", "c.id === 'prealgebra7' || c.id === 'math6' || c.id === 'math5' || c.id === 'algebra2'; });");
edit('app.js', "if (c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6' || c.id === 'precalculus'", "if (c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6' || c.id === 'math5' || c.id === 'precalculus'");
edit('app.js', "    { id: 'practice', name: 'Practice Activities', formats: ['proofs'] },", "    { id: 'practice', name: 'Practice Activities', formats: ['proofs'] },\n    { id: 'projects', name: 'Projects', formats: ['projects'] },");
edit('app.js', "        category('practice', 'Practice Activities', practiceFormats) +", "        category('practice', 'Practice Activities', practiceFormats) +\n        category('projects', 'Projects', ['projects']) +");
// level labels and course lists in generators
edit('worksheet-generator/course-game.html', "if(['math6','prealgebra7','prealgebra'].includes(source.courseId))", "if(['math5','math6','prealgebra7','prealgebra'].includes(source.courseId))");
edit('worksheet-generator/games/course-activity.js', "['math6','prealgebra7','prealgebra'].includes(source.courseId)", "['math5','math6','prealgebra7','prealgebra'].includes(source.courseId)");
edit('worksheet-generator/approved-flashcards.html', "if(['math6','prealgebra7','prealgebra'].indexOf(c)<0)return;", "if(['math5','math6','prealgebra7','prealgebra'].indexOf(c)<0)return;");
edit('worksheet-generator/vocabulary-builder.js', "const middle=/^(prealgebra7?|math6)-/.test($('unit').value);", "const middle=/^(prealgebra7?|math[56])-/.test($('unit').value);");
edit('worksheet-generator/menu/match-game.js', "function levelName(unit,id){return /^(prealgebra7?|math6)-/.test(unit)", "function levelName(unit,id){return /^(prealgebra7?|math[56])-/.test(unit)");
edit('worksheet-generator/algebra2-bank-native.js', "NS.courseLevelName=function(id,level){return /^(prealgebra(?:7)?|math6)-/.test(id)", "NS.courseLevelName=function(id,level){return /^(prealgebra(?:7)?|math[56])-/.test(id)");
edit('worksheet-generator/menu/course-catalog-bridge.js', "var courseIds = ['math6', 'prealgebra7',", "var courseIds = ['math5', 'math6', 'prealgebra7',");
edit('coverage.html', "function isMiddleSchool(id){return ['math6','prealgebra7','prealgebra'].indexOf(id)>=0}", "function isMiddleSchool(id){return ['math5','math6','prealgebra7','prealgebra'].indexOf(id)>=0}");
edit('skills.html', "var order=['math6',", "var order=['math5','math6',");
// Understanding Check wording + labels in the printable practice page
edit('worksheet-generator/practice/practice.js', "(/^prealgebra(?:7)?-|^math6-/.test(config.unit)?", "(/^prealgebra(?:7)?-|^math[56]-/.test(config.unit)?");
edit('worksheet-generator/practice/practice.js', "function controls(){return '<section class=\"pt-card\"><span class=\"pt-eyebrow\">ASSESSMENT READINESS · VERSION 2</span><h1>Assessment Readiness Check</h1>",
  "function controls(){return '<section class=\"pt-card\"><span class=\"pt-eyebrow\">'+(/^math5-/.test(config.unit)?'GRADE 5 · UNDERSTANDING CHECK':'ASSESSMENT READINESS · VERSION 2')+'</span><h1>'+(/^math5-/.test(config.unit)?'Understanding Check':'Assessment Readiness Check')+'</h1>");
// lesson planner
edit('worksheet-generator/planner/scope-algebra2.js', "['algebra2','prealgebra','prealgebra7','math6','precalculus'", "['algebra2','prealgebra','prealgebra7','math6','math5','precalculus'");
edit('worksheet-generator/planner/scope-algebra2.js', "math6:'MATH6',precalculus:'PRECALCULUS'", "math6:'MATH6',math5:'MATH5',precalculus:'PRECALCULUS'");
edit('worksheet-generator/planner/scope-algebra2.js', "math6:'M6',precalculus:'PC'", "math6:'M6',math5:'M5',precalculus:'PC'");
edit('worksheet-generator/planner/course.js', "var mid = ['prealgebra', 'prealgebra7', 'math6']", "var mid = ['prealgebra', 'prealgebra7', 'math6', 'math5']");
edit('worksheet-generator/planner/planner-ui.js', "PA8 = ['prealgebra', 'prealgebra7', 'math6', 'prec", "PA8 = ['prealgebra', 'prealgebra7', 'math6', 'math5', 'prec");
edit('worksheet-generator/planner/planner-ui.js', "/^(algebra1|geometry|algebra2|prealgebra7|prealgebra|math6|precalculus|calculus|statistics|discrete)-/", "/^(algebra1|geometry|algebra2|prealgebra7|prealgebra|math6|math5|precalculus|calculus|statistics|discrete)-/");
edit('worksheet-generator/planner/planner-ui.js', "/^(algebra1|geometry|algebra2|prealgebra|prealgebra7|math6|precalculus|calculus|statistics|discrete)$/", "/^(algebra1|geometry|algebra2|prealgebra|prealgebra7|math6|math5|precalculus|calculus|statistics|discrete)$/", { all: true });
edit('worksheet-generator/planner/planner-ui.js', "[['math6', '6th Grade Math'], ['prealgebra7',", "[['math5', '5th Grade Math'], ['math6', '6th Grade Math'], ['prealgebra7',");
{ // hashchange regex (third occurrence family)
  let s = read('worksheet-generator/planner/planner-ui.js');
  const re = /\/\^\(algebra1\|geometry\|algebra2\|prealgebra\|prealgebra7\|math6\|precalcu/g;
  if (re.test(s)) { s = s.replace(re, '/^(algebra1|geometry|algebra2|prealgebra|prealgebra7|math6|math5|precalcu'); write('worksheet-generator/planner/planner-ui.js', s); applied++; } else skipped++;
}
// elementary color + unit icon on unit cards
edit('styles.css', "[data-color=\"teal\"] { --c-bg: var(--teal-bg); --c-fg: var(--teal-fg); --c-tint: var(--teal-tint); --c-text: var(--teal-text); }",
  "[data-color=\"teal\"] { --c-bg: var(--teal-bg); --c-fg: var(--teal-fg); --c-tint: var(--teal-tint); --c-text: var(--teal-text); }\n/* 5th Grade Math: bright sunshine palette and a unit illustration on every unit card. */\n:root { --sunshine-bg: #f5b301; --sunshine-fg: #2b1d00; --sunshine-tint: #fff4cc; --sunshine-text: #8a5a00; }\n[data-color=\"sunshine\"] { --c-bg: var(--sunshine-bg); --c-fg: var(--sunshine-fg); --c-tint: var(--sunshine-tint); --c-text: var(--sunshine-text); }\n.g5-unit-icon { display:block; width:100%; max-width:160px; height:auto; margin:0 0 .4rem; border-radius:14px; }");
// vocabulary script tag already includes vocabulary-data-middle-grades.js on printables/vocabulary pages (content.py appends MATH5 block)
// projects registry for the Printable Generator (kind=project)
{
  let s = read('worksheet-generator/menu/printables-projects.js');
  if (!s.includes('"math5-place-value-number-sense"')) {
    const anchor = '  PR.PROJECTS = {\n';
    if (!s.includes(anchor)) throw Error('printables-projects.js anchor not found');
    const body = Object.entries(PROJ).map(([k, v]) => '  ' + JSON.stringify(k) + ': ' + JSON.stringify(v, null, 2).replace(/\n/g, '\n  ')).join(',\n') + ',\n';
    s = s.replace(anchor, anchor + body).replace('Courses: Algebra 1, Geometry, Algebra 2, 6th Grade,', 'Courses: Algebra 1, Geometry, Algebra 2, 5th Grade, 6th Grade,');
    write('worksheet-generator/menu/printables-projects.js', s); applied++;
  } else skipped++;
}
// framework strands (one record per unit)
{
  let s = read('massachusetts-framework-strands.js');
  if (!s.includes('"courseId": "math5"')) {
    const strand = { 'place-value-number-sense': '5.NBT', 'multi-digit-multiplication-division': '5.NBT', 'decimal-operations': '5.NBT', 'numerical-expressions-patterns': '5.OA',
      'fraction-addition-subtraction': '5.NF', 'fraction-multiplication-division': '5.NF', 'measurement-conversions': '5.MD', 'volume-three-dimensional-figures': '5.MD',
      'coordinate-plane-graphing': '5.G', 'classifying-two-dimensional-figures': '5.G', 'data-line-plots-problem-solving': '5.MD' };
    const recs = O.units.map(u => '  ' + JSON.stringify({ courseId: 'math5', unitId: u.id, strand: strand[u.id], relationship: 'grade-level' }, null, 2).replace(/\n/g, '\n  ')).join(',\n') + ',\n';
    const anchor = ' var records=[\n';
    if (!s.includes(anchor)) throw Error('strands anchor');
    s = s.replace(anchor, anchor + recs); write('massachusetts-framework-strands.js', s); applied++;
  } else skipped++;
}
// resource details for cheat sheets (2 pages, reference sheet) and tools
{
  let r = read('resource-details.js'); const add = [];
  O.units.forEach(u => { const k = `artifacts/math5-${u.id}-cheat-sheet/worksheet.pdf`; if (!r.includes(JSON.stringify(k) + ':')) add.push('  ' + JSON.stringify(k) + ': ' + JSON.stringify({ pages: 2, referenceSheet: true })); });
  if (add.length) { r = r.replace(/\n\};\s*$/, ',\n' + add.join(',\n') + '\n};\n'); write('resource-details.js', r); applied++; } else skipped++;
}
// public site SEO
edit('scripts/build-site.mjs', "  math6: {\n    title: \"Free 6th Grade Math Worksheets & Games\",", "  math5: {\n    title: \"Free 5th Grade Math Worksheets, Games & Activities\",\n    description: \"Free 5th grade math games, worksheets, flashcards, cheat sheets, projects and interactive tools for place value, decimals, fractions, volume, the coordinate plane and more.\"\n  },\n  math6: {\n    title: \"Free 6th Grade Math Worksheets & Games\",");
// cache strings so browsers pick up the new catalog
['index.html', 'activity.html'].forEach(f => { let s = read(f), n = s.replace(/(data|resource-details)\.js\?v=[a-z0-9-]+/g, '$1.js?v=grade5-20261111').replace(/app\.js\?v=[a-z0-9-]+/g, 'app.js?v=grade5-20261111'); if (n !== s) { write(f, n); applied++; } else skipped++; });
console.log('math5 integration: data.js block (' + Object.values(units).reduce((a, x) => a + x.length, 0) + ' resources), ' + applied + ' edits applied, ' + skipped + ' already present');
