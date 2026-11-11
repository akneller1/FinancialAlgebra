/* Validates every Financial Algebra bank, the Classroom export, labs, projects, and packaged files. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { course } from '../src/course.js';
import '../financial/lib/finance.js';
import '../financial/lib/render.js';
import '../financial/decision-lab/scenarios.js';
const root = new URL('../', import.meta.url), P = p => new URL(p, root).pathname;
const json = p => JSON.parse(readFileSync(P(p), 'utf8'));
const BAD = /\b(NaN|undefined|Infinity|null)\b|\[object Object\]/;
const FORMATS = ['multiple-choice', 'select-all', 'short-answer', 'open-response'];
const TYPES = ['vocabulary', 'concept', 'scenario', 'comparison', 'document', 'calculation', 'reasoning', 'claim'];

test('all ten units have extended banks with valid, unique, complete items', () => {
  const allIds = new Set();
  for (const u of course.units) {
    const b = json(`financial/banks/${u.id}.json`);
    assert.equal(b.schema, 'fa-bank-1'); assert.equal(b.unitId, u.id); assert.equal(b.level, 'standard');
    const skills = u.skills.map((_, i) => `${u.id}-skill-${String(i + 1).padStart(2, '0')}`);
    const counts = Object.fromEntries(skills.map(s => [s, 0])), prompts = new Set();
    for (const q of b.questions) {
      assert.ok(!allIds.has(q.id), 'duplicate id ' + q.id); allIds.add(q.id);
      assert.ok(skills.includes(q.skillId), q.id + ' bad skill'); counts[q.skillId]++;
      assert.ok(FORMATS.includes(q.format), q.id + ' format'); assert.ok(TYPES.includes(q.type), q.id + ' type ' + q.type);
      assert.equal(q.level, 'standard');
      assert.ok(q.prompt && q.prompt.length > 10, q.id + ' prompt');
      assert.ok(q.answer !== undefined && q.answer !== null && String(q.answer).length, q.id + ' answer');
      assert.ok(Array.isArray(q.solutionSteps) && q.solutionSteps.length, q.id + ' steps');
      const text = JSON.stringify([q.prompt, q.answer, q.solutionSteps, q.options, q.parts, q.scenario, q.modelResponse].filter(x => x !== undefined));
      assert.ok(!BAD.test(text), q.id + ' contains a bad token: ' + text.match(BAD)?.[0]);
      const strs = []; (function walk(x) { if (typeof x === 'string') strs.push(x); else if (x && typeof x === 'object') Object.values(x).forEach(walk); })([q.prompt, q.answer, q.solutionSteps, q.parts, q.scenario, q.modelResponse]);
      for (const t of strs) assert.equal((t.match(/\[\[/g) || []).length, (t.match(/\[\[[^\[\]]+\|\|[^\[\]]+\]\]/g) || []).length, q.id + ' fraction markup: ' + t);
      const key = q.prompt + JSON.stringify(q.scenario || '');
      assert.ok(!prompts.has(key), 'duplicate prompt ' + q.id); prompts.add(key);
      if (q.format === 'multiple-choice') { assert.equal(q.options.filter(o => o.correct).length, 1, q.id); assert.ok(q.options.length >= 3, q.id); assert.equal(q.options.find(o => o.correct).text, q.answer, q.id + ' answer matches option'); assert.equal(new Set(q.options.map(o => o.text)).size, q.options.length, q.id + ' distinct options'); }
      if (q.format === 'select-all') { assert.ok(q.options.filter(o => o.correct).length >= 2, q.id); assert.deepEqual(q.options.filter(o => o.correct).map(o => o.text).sort(), q.answer.slice().sort()); }
      if (q.format === 'open-response') { assert.ok(q.parts.length >= 4, q.id + ' parts'); assert.ok(q.rubric && q.rubric.length >= 4, q.id + ' rubric'); assert.ok(q.modelResponse, q.id + ' model response'); }
      if (q.numeric) { assert.ok(Number.isFinite(q.numeric.value), q.id + ' numeric'); if (q.numeric.unit === 'USD' && q.format === 'short-answer' && /^[−-]?\$[\d,]+\.\d\d$/.test(q.answer)) assert.equal(Number(q.answer.replace(/[$,]/g, '').replace('−', '-')), q.numeric.value, q.id + ' answer/numeric agree'); }
    }
    for (const s of skills) assert.ok(counts[s] >= 25, `${s} has only ${counts[s]} items`);
    assert.ok(b.lessons.length === 4 && b.lessons.every(l => l.objectives.length && l.examples.length && l.misconceptions.length), u.id + ' lessons');
    assert.ok(b.cheatSheet.sections.length >= 2 && b.cheatSheet.misconceptions.length, u.id + ' cheat sheet');
    assert.ok(b.vocab.length >= 14, u.id + ' vocab');
    for (const t of ['vocabulary', 'calculation', 'claim', 'document']) assert.ok(b.questions.some(q => q.type === t), `${u.id} lacks ${t}`);
    assert.ok(b.questions.some(q => q.type === 'comparison'), u.id + ' comparison');
  }
});

test('Classroom exports pass the unchanged production adapter (single level stored as cp1)', async () => {
  globalThis.MK_COURSE_CATALOG = { getSkillRecords: (c, u) => c === 'financial-algebra' ? (course.units.find(x => x.id === u)?.skills || []).map((s, i) => ({ id: `${u}-skill-${String(i + 1).padStart(2, '0')}`, name: s })) : [] };
  await import('./fixtures/question-bank-adapter.js');
  const A = globalThis.MK_QUESTION_BANKS;
  for (const u of course.units) {
    const b = json(`question-banks/financial-algebra/${u.id}.json`);
    const r = A.validate(b); assert.ok(r.ok, u.id + ': ' + r.errors.slice(0, 3).join('; '));
    assert.ok(b.questions.every(q => q.level === 'cp1'));
    assert.ok(A.register(b, { verified: true }).ok);
    const games = A.select({ courseId: 'financial-algebra', unitId: u.id, level: 'cp1', formats: ['multiple-choice', 'short-answer'] });
    assert.ok(games.length >= 60, u.id + ' game pool ' + games.length);
    assert.ok(games.every(q => q.prompt.length < 600), u.id + ' game prompts short enough');
  }
});

test('flashcard decks, resources manifest, and hub are consistent', () => {
  const src = readFileSync(P('financial/flashcards/decks.js'), 'utf8'); const decks = JSON.parse(src.slice(src.indexOf('=') + 1).trim().replace(/;$/, ''));
  const man = json('financial/resources.json'); assert.equal(man.units.length, 10);
  for (const u of man.units) {
    assert.ok(decks[u.unitId].cards.length >= 20, u.unitId + ' cards');
    assert.ok(decks[u.unitId].cards.some(c => c.kind), u.unitId + ' non-vocabulary cards');
    const r = u.resources;
    for (const p of [r.cheatSheet, r.classroomBank, r.extendedBank, ...r.projects.map(x => x.path)]) assert.ok(existsSync(P(p)), 'missing ' + p);
    assert.ok(r.decisionLab && r.projects.length >= 1, u.unitId + ' lab/projects');
  }
  assert.ok(man.units.reduce((n, u) => n + u.resources.projects.length, 0) >= 12);
});

test('decision labs compute finite results and checkable answers for every unit', () => {
  const L = globalThis.FA_LABS;
  for (const u of course.units) {
    const lab = L[u.id]; assert.ok(lab, 'lab for ' + u.id);
    assert.equal(lab.options.length, 3); assert.ok(lab.reflection.length >= 3 && lab.teacher.model && lab.objectives.length);
    for (const s of lab.skills) assert.ok(s.startsWith(u.id + '-skill-'));
    const v = Object.fromEntries(lab.vars.map(x => [x.id, x.value]));
    const out = lab.compute(v);
    for (const row of out.rows) for (const x of Object.values(row.values)) assert.ok(typeof x === 'string' || !Number.isNaN(x), `${u.id} ${row.label}`);
    for (const q of [...lab.questions, ...lab.challenges]) assert.ok(Number.isFinite(q.answer(v)), `${u.id}: ${typeof q.prompt === 'string' ? q.prompt.slice(0, 50) : ''}`);
    // vary each slider to its extremes without NaN
    for (const x of lab.vars.filter(x => x.type !== 'toggle')) for (const val of [x.min, x.max]) { const o = lab.compute({ ...v, [x.id]: val }); o.rows.forEach(r => Object.values(r.values).forEach(y => assert.ok(typeof y === 'string' || !Number.isNaN(y), `${u.id} ${x.id}=${val}`))); }
  }
});

test('projects are complete with 100-point rubrics and all formats', async () => {
  let n = 0;
  for (const u of course.units) {
    const f = P(`financial/content/projects/${u.id}.mjs`); assert.ok(existsSync(f), 'projects for ' + u.id);
    const list = (await import(new URL(`financial/content/projects/${u.id}.mjs`, root).href)).default;
    for (const p of list) {
      n++;
      assert.equal(p.rubric.reduce((s, r) => s + r.points, 0), 100, p.slug + ' rubric');
      assert.ok(p.rubric.every(r => r.levels.length === 4));
      for (const k of ['intro', 'scenario', 'goals', 'documents', 'tasks', 'reflection', 'checklist', 'slides']) assert.ok(p[k] && (p[k].length || typeof p[k] === 'string'), p.slug + ' ' + k);
      for (const k of ['materials', 'pacing', 'implementation', 'worked', 'samples', 'misconceptions', 'differentiation', 'extensions']) assert.ok(p.teacher[k], p.slug + ' teacher ' + k);
      assert.ok(!BAD.test(JSON.stringify(p)), p.slug + ' bad token');
      const dir = `artifacts/financial-algebra-project-${p.slug}/`;
      for (const s of ['-student.pdf', '-student.docx', '-teacher-guide.pdf', '-teacher-guide.docx', '-slides.pptx']) assert.ok(existsSync(P(dir + p.slug + s)), 'missing ' + dir + p.slug + s);
      assert.ok(existsSync(P(dir + 'index.html')) && existsSync(P(dir + 'hero.svg')));
    }
  }
  assert.ok(n >= 12);
});

test('shared renderer shows division as stacked fractions and escapes HTML', () => {
  const R = globalThis.FA_RENDER;
  assert.ok(R.rich('$1,240 × 26 ÷ 12').includes('fa-frac'));
  assert.ok(R.rich('[[price || quantity]]').includes('fa-num">price'));
  assert.ok(!R.rich('<script>').includes('<script>'));
  assert.equal(R.checkNumeric({ numeric: { value: -313.67, tolerance: 0.01 } }, '−$313.67'), true);
});

test('no files collide with the removed-pilot paths guarded by the existing site test', () => {
  for (const p of ['worksheet.html', 'practice.html', 'print.html', 'lab.html', 'src/finance-lab.js', 'src/questions.js', 'src/engine.js']) assert.equal(existsSync(P(p)), false, p);
});
