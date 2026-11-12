#!/usr/bin/env node
/* 5th Grade Math (math5) integration check. Node only, no network.
   Banks: approved in the manifest, 30 questions per skill and level, schema-safe fields, standards on every item,
   one correct choice per multiple-choice item, stored distractors differ from the key, diagrams present with alt text,
   no duplicate ids or prompts. Content: flashcards, cheat sheets, tools, projects, escape themes, data.js links.
   Math is verified separately by tools/grade5-authoring/verify.py (independent re-computation of every answer). */
'use strict';
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm'), assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const read = f => fs.readFileSync(path.join(root, f), 'utf8');
const exists = f => fs.existsSync(path.join(root, f.split(/[?#]/)[0]));
const win = {}; win.window = win;
for (const f of ['data.js', 'course-catalog.js', 'grade5-resource-catalog.js']) vm.runInNewContext(read(f), win, { filename: f });
const course = win.LIBRARY.courses.find(c => c.id === 'math5');
assert.ok(course, 'math5 course record missing from data.js');
const units = course.units.map(u => u.id);
assert.equal(units.length, 11, 'eleven units');
const manifest = JSON.parse(read('manifest.json')).banks.filter(b => b.courseId === 'math5');
assert.equal(JSON.stringify(manifest.map(b => b.unitId).sort()), JSON.stringify(units.slice().sort()), 'every unit has a manifest entry');
assert.ok(manifest.every(b => b.approved === true), 'math5 manifest entries are approved');

const FORMATS = new Set(['short-answer', 'multiple-choice', 'select-all', 'open-response']);
const KEYS = new Set(['id', 'skillId', 'level', 'format', 'prompt', 'answer', 'solutionSteps', 'standards', 'sourceNotes', 'options', 'parts', 'diagram']);
const ids = new Set(), prompts = new Set();
let total = 0, diagrams = 0;
const byLevel = { cp2: 0, cp1: 0, honors: 0 };
for (const u of units) {
  const bank = JSON.parse(read(`math5/${u}.json`));
  const meta = JSON.parse(read(`math5/meta/${u}.meta.json`));
  const skills = win.MK_COURSE_CATALOG.getSkillRecords('math5', u).map(s => s.id);
  assert.equal(bank.courseId, 'math5'); assert.equal(bank.unitId, u);
  const count = {};
  for (const q of bank.questions) {
    total++; byLevel[q.level]++;
    for (const k of Object.keys(q)) assert.ok(KEYS.has(k), q.id + ': unexpected field ' + k);
    assert.ok(!ids.has(q.id), 'duplicate id ' + q.id); ids.add(q.id);
    const pk = q.prompt.replace(/\s+/g, ' ').trim().toLowerCase() + '|' + (q.diagram ? q.diagram.spec.alt : '') + '|' + (q.options || []).map(o => o.text).join('~') + '|' + (q.parts || []).map(p => p.prompt).join('~');
    assert.ok(!prompts.has(pk), 'duplicate prompt ' + q.id); prompts.add(pk);
    assert.ok(skills.includes(q.skillId), q.id + ': unknown skill');
    assert.ok(FORMATS.has(q.format), q.id + ': format');
    assert.ok(Array.isArray(q.standards) && q.standards.length && q.standards.every(s => /^5\.(OA|NBT|NF|MD|G)\.[A-C]\.\d+(\.[a-c])?$/.test(s)), q.id + ': standards');
    assert.ok(Array.isArray(q.solutionSteps) && q.solutionSteps.length, q.id + ': worked steps');
    assert.ok(meta[q.id] && meta[q.id].questionType, q.id + ': meta');
    if (q.format === 'multiple-choice') {
      assert.equal(q.options.filter(o => o.correct).length, 1, q.id + ': exactly one correct choice');
      assert.equal(new Set(q.options.map(o => o.text)).size, q.options.length, q.id + ': distinct choices');
    }
    if (q.format === 'select-all') assert.ok(q.options.some(o => o.correct) && q.options.some(o => !o.correct), q.id + ': select-all mix');
    if (q.format === 'open-response') assert.equal(q.parts.length, 4, q.id + ': four parts');
    for (const d of Object.keys((meta[q.id] || {}).distractors || {})) assert.notEqual(d.trim(), String(q.answer).trim(), q.id + ': stored distractor equals the key');
    if (q.diagram) {
      diagrams++;
      assert.equal(q.diagram.type, 'image'); assert.ok(q.diagram.spec.alt && q.diagram.spec.alt.length > 10, q.id + ': alt text');
      assert.ok(exists(q.diagram.spec.src), q.id + ': diagram file ' + q.diagram.spec.src);
    }
    const k = q.skillId + '|' + q.level; count[k] = (count[k] || 0) + 1;
  }
  for (const s of skills) for (const l of ['cp2', 'cp1', 'honors']) assert.equal(count[s + '|' + l], 30, `${u} ${s} ${l}: 30 questions`);

  const fc = JSON.parse(read(`worksheet-generator/grade5/flashcards/${u}.json`));
  assert.ok(fc.cards.length >= 15 && fc.cards.every(c => c.front && c.back), u + ': flashcards');
  assert.ok(exists(`math5-${u}-cheat-sheet/worksheet.pdf`) && exists(`scripts/cheat-sheets/content/math5-${u}.cjs`), u + ': cheat sheet');
  const res = course.units.find(x => x.id === u).artifacts;
  for (const a of res) assert.ok(exists(a.path), u + ': missing resource target ' + a.path);
  for (const a of res) if (a.thumb) assert.ok(exists(a.thumb), u + ': missing thumbnail ' + a.thumb);
  assert.ok(res.filter(a => /grade5-games\.html/.test(a.path)).length >= 9, u + ': games');
  assert.ok(res.some(a => /grade5-flashcards\.html/.test(a.path)) && res.some(a => /grade5-understanding-check\.html/.test(a.path)), u + ': flashcards and Understanding Check');
  assert.ok(res.some(a => a.type === 'Project'), u + ': project');
}
assert.equal(byLevel.cp2, byLevel.cp1); assert.equal(byLevel.cp1, byLevel.honors);
const themes = JSON.parse(read('worksheet-generator/games/escape-themes.json'));
assert.ok(units.every(u => themes['math5/' + u]), 'escape themes');
for (const f of ['grade5-games.html', 'grade5-flashcards.html', 'grade5-understanding-check.html', 'grade5/g5-core.js', 'grade5/g5-games.js', 'grade5/flashcards.js', 'grade5/understanding-check.js', 'grade5/g5.css'])
  assert.ok(exists('worksheet-generator/' + f), 'missing ' + f);
for (const f of ['grade5/g5-core.js', 'grade5/g5-games.js', 'grade5/flashcards.js', 'grade5/understanding-check.js', 'grade5/tool-shell.js']) new vm.Script(read('worksheet-generator/' + f), { filename: f });

// Verify all local assets referenced by seven interactive tool entry pages.
const models=['area-model-explorer','coordinate-explorer','expression-builder','fraction-explorer',
  'measurement-converter','place-value-builder','volume-builder'];
for(const slug of models){
  const base='math5-'+slug;
  const html=read(base+'/index.html');
  for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){
    const raw=match[1].split(/[?#]/)[0];
    if(!raw.startsWith('../'))continue;
    const local=path.posix.normalize(base+'/'+raw);
    assert.ok(!local.startsWith('..')&&exists(local),base+': missing local script or style '+raw);
  }
}
assert.ok(exists('grade5-resources.html')&&exists('grade5-resource-catalog.js'),'Grade 5 resource hub missing');

// Run the real browser-facing approved-bank loader against all 11 published banks.
// A successful file inventory alone cannot prove the runtime adapter accepts a bank.
win.fetch=async function(url){
  const local=String(url).replace(/^\.\.\//,'').split(/[?#]/)[0];
  return {ok:exists(local),json:async function(){return JSON.parse(read(local));}};
};
for(const mod of ['question-bank-adapter.js','question-bank-loader.js'])
  vm.runInNewContext(read(mod),win,{filename:mod});
Promise.all(units.map(u=>win.MK_BANK_LOADER.loadUnitFromSite('math5',u,null,'../'))).then(function(results){
  assert.equal(results.length,11);
  for(const u of units){
    assert.ok(win.MK_QUESTION_BANKS.available('math5',u),u+': adapter could not load approved questions');
  }
  console.log(`PASS math5: 11 approved units, ${total} questions (${byLevel.cp2} per level), ${diagrams} diagrams, 7 models, games, checks, projects, correct URLs and runtime bank loading`);
}).catch(function(e){console.error(e);process.exitCode=1;});

