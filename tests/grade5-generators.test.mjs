import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const read = p => fs.readFileSync(new URL(p, root), 'utf8');
const ctx = { console };
ctx.window = ctx;
vm.createContext(ctx);
for (const file of ['course-catalog.js', 'worksheet-generator/grade5/generators-content.js',
  'worksheet-generator/grade5/generators-core.js', 'worksheet-generator/grade5/generators-render.js']) {
  vm.runInContext(read(file), ctx, { filename: file });
}
const C = ctx.G5_GENERATORS_CORE, R = ctx.G5_GENERATORS_RENDER, Content = ctx.G5_GENERATOR_CONTENT;
const NAMES = {
  'place-value-number-sense': 'Place Value and Number Sense',
  'multi-digit-multiplication-division': 'Multi-Digit Multiplication and Division',
  'decimal-operations': 'Decimal Operations',
  'numerical-expressions-patterns': 'Numerical Expressions and Patterns',
  'fraction-addition-subtraction': 'Fraction Concepts and Operations',
  'fraction-multiplication-division': 'Fraction Multiplication and Division',
  'measurement-conversions': 'Measurement Conversions',
  'volume-three-dimensional-figures': 'Volume of Three-Dimensional Figures',
  'coordinate-plane-graphing': 'Coordinate Plane Graphing',
  'classifying-two-dimensional-figures': 'Geometry and Classifying Shapes',
  'data-line-plots-problem-solving': 'Data, Line Plots and Problem Solving'
};
const units = Object.keys(NAMES).map((id, i) => {
  const bank = JSON.parse(read(`math5/${id}.json`));
  const meta = JSON.parse(read(`math5/meta/${id}.meta.json`));
  return {
    id, name: NAMES[id], number: i + 1, bank, meta,
    skills: ctx.MK_COURSE_CATALOG.getSkillRecords('math5', id),
    questions: bank.questions,
    content: Content.units[id]
  };
});
const allSkills = u => u.skills.map(s => s.id);
const student = plan => R.render(plan, false);
const teacher = plan => R.render(plan, true);

test('all eleven Grade 5 units have lesson content and a complete approved bank', () => {
  assert.equal(units.length, 11);
  for (const u of units) {
    assert.ok(u.questions.length >= 360, u.id + ' bank size');
    assert.ok(u.content, u.id + ' lesson content');
    assert.ok(u.content.bigIdea.length > 20, u.id + ' big idea');
    assert.ok(u.content.vocabulary.length >= 6, u.id + ' vocabulary');
    assert.ok(u.content.objectives.length >= u.skills.length, u.id + ' objectives');
    assert.deepEqual(new Set(u.skills.map(s => s.id)), new Set(u.questions.map(q => q.skillId)), u.id + ' skills');
  }
});

test('lesson plans build for every unit and every level with matching keys', () => {
  for (const u of units) {
    for (const level of ['cp2', 'cp1', 'honors']) {
      const plan = C.buildLesson(u, C.options({ skills: allSkills(u), level }), 'A' + u.id + level);
      const s = student(plan), k = teacher(plan);
      assert.match(s, /STUDENT HANDOUT/);
      assert.match(k, /TEACHER KEY/);
      assert.match(s, /Name _/);
      assert.match(s, /Learning goals/);
      assert.match(s, /Key vocabulary/);
      assert.match(s, /Exit ticket/);
      assert.doesNotMatch(s, /undefined|NaN/);
      const qs = plan.sections.flatMap(x => x.blocks).filter(b => b.kind === 'question').map(b => b.q);
      assert.ok(qs.length >= 10, u.id + ' lesson questions');
      assert.equal(new Set(qs.map(q => q.id)).size, qs.length, u.id + ' duplicate lesson question');
      assert.ok(qs.every(q => q.level === level && allSkills(u).includes(q.skillId)), u.id + ' lesson level/skill');
      assert.doesNotMatch(s, /class="g5q-key"/, u.id + ' answers must not print on student copy');
      assert.match(k, /class="g5q-key"/);
    }
  }
});

test('notes, worked examples, section order and counts customize the lesson', () => {
  const u = units[0], o = C.options({ skills: allSkills(u), notes: 'blank' });
  o.sections = o.sections.filter(x => ['vocabulary', 'practice', 'teach'].includes(x.id)).reverse();
  o.sections.find(x => x.id === 'practice').count = 3;
  const plan = C.buildLesson(u, o, 'X'), s = student(plan);
  assert.doesNotMatch(s, /Learning goals|Exit ticket|Warm-up/);
  assert.ok(s.indexOf('Practice') < s.indexOf('Teach and model'));
  assert.equal(plan.sections.find(x => x.id === 'practice').blocks.length, 3);
  assert.match(s, /height:.42in/);
  const completed = C.buildLesson(u, C.options({ skills: allSkills(u), notes: 'completed' }), 'Y');
  assert.match(student(completed), /Completed/);
  const noWorked = C.buildLesson(u, C.options({ skills: allSkills(u), worked: false }), 'Z');
  assert.doesNotMatch(student(noWorked), /class="g5answer"/);
  assert.match(teacher(noWorked), /class="g5answer"/);
});

test('worksheets honor format, response, level and distinct-question rules', () => {
  for (const u of units) {
    for (const format of ['mixed', 'multiple-choice', 'short-answer', 'select-all', 'open-response', 'diagrams']) {
      const plan = C.buildPaper(u, C.options({ skills: allSkills(u), format, count: 10 }), 'worksheet', 'W' + u.id + format);
      const qs = plan.sections[0].blocks.map(b => b.q);
      assert.ok(qs.length > 0, u.id + ' ' + format);
      assert.equal(new Set(qs.map(q => q.id)).size, qs.length, u.id + ' duplicate worksheet question');
      if (format !== 'mixed') assert.ok(qs.every(q => format === 'diagrams' ? !!q.diagram : q.format === format), u.id + ' format ' + format);
      const s = student(plan), k = teacher(plan);
      assert.match(s, /Practice questions/);
      assert.match(k, /Scoring guide/);
      assert.doesNotMatch(s, /class="g5q-key"/);
      assert.doesNotMatch(s, /undefined|NaN/);
    }
  }
});

test('assessment points reconcile for every unit and total', () => {
  for (const u of units) {
    for (const total of [25, 40, 60, 100]) {
      const plan = C.buildPaper(u, C.options({ skills: allSkills(u), count: 12, total }), 'assessment', 'A' + u.id + total);
      const blocks = plan.sections[0].blocks;
      assert.equal(blocks.reduce((a, b) => a + b.points, 0), total, u.id + ' points ' + total);
      assert.ok(blocks.every(b => b.points >= 1));
      const s = student(plan), k = teacher(plan);
      assert.match(s, new RegExp(total + ' points'));
      assert.match(k, /Scoring guide/);
      assert.doesNotMatch(s, /class="g5q-key"/);
    }
  }
});

test('all six activity generators produce complete printable puzzles and keys', () => {
  for (const u of units) {
    for (const kind of Object.keys(C.ACTIVITIES)) {
      const plan = C.buildActivity(u, C.options({ skills: allSkills(u), activity: kind, count: 12 }), 'K' + u.id + kind);
      const s = student(plan), k = teacher(plan);
      assert.ok(plan.items.length >= (kind === 'error' ? 6 : 8), u.id + ' ' + kind + ' items ' + plan.items.length);
      assert.doesNotMatch(s, /undefined|NaN/);
      assert.ok(k.length > 300, u.id + ' ' + kind + ' teacher key');
      if (kind === 'maze') {
        assert.ok(plan.rooms.length >= 8);
        for (const room of plan.rooms) {
          assert.equal(room.doors.length, 3);
          assert.equal(room.doors.filter(d => d.correct).length, 1);
          const right = room.doors.find(d => d.correct).text;
          assert.equal(C.norm(right), C.norm(C.answerText(room.q)));
        }
        assert.match(k, /Correct route/);
      }
      if (kind === 'color') {
        assert.equal(plan.grid.length, 36);
        assert.ok(plan.grid.every(c => c.label), 'every colour cell has an answer');
        assert.match(k, /Color key/);
      }
      if (kind === 'matching') {
        assert.equal(new Set(plan.answers.map(C.norm)).size, plan.answers.length);
        assert.match(k, /Answer key/);
      }
      if (kind === 'stations') {
        assert.equal(plan.stations.length, 4);
        assert.match(s, /Recording sheet/);
      }
      if (kind === 'error') {
        assert.ok(plan.items.every(i => i.wrong && C.norm(i.wrong) !== C.norm(C.answerText(i.q))));
        assert.match(k, /Correct answer/);
      }
      if (kind === 'partner') {
        assert.ok(plan.pairs.length >= 4);
        assert.ok(plan.pairs.every(p => C.norm(C.answerText(p.a)) === C.norm(C.answerText(p.b))));
        assert.match(k, /Matched answers/);
      }
    }
  }
});

test('activity distractors are verified wrong answers, never the correct answer', () => {
  for (const u of units) {
    const plan = C.buildActivity(u, C.options({ skills: allSkills(u), activity: 'maze' }), 'D' + u.id);
    for (const room of plan.rooms) {
      for (const door of room.doors.filter(d => !d.correct)) {
        assert.notEqual(C.norm(door.text), C.norm(C.answerText(room.q)), u.id + ' distractor equals answer');
        const meta = u.meta[room.q.id] || {};
        const optionWrong = (room.q.options || []).filter(o => !o.correct).map(o => C.norm(o.text));
        const distractorWrong = Object.keys(meta.distractors || {}).map(C.norm);
        assert.ok(optionWrong.includes(C.norm(door.text)) || distractorWrong.includes(C.norm(door.text)), u.id + ' unverified distractor');
      }
    }
  }
});

test('generators are deterministic and every bank answer still matches its key', () => {
  const u = units[3];
  for (const mode of ['lesson', 'worksheet', 'assessment']) {
    const o = C.options({ skills: allSkills(u) });
    const a = C.build(u, o, mode, 'seed'), b = C.build(u, o, mode, 'seed');
    assert.equal(JSON.stringify(a), JSON.stringify(b), mode + ' deterministic');
  }
  const byId = new Map(u.questions.map(q => [q.id, q]));
  const plan = C.buildPaper(u, C.options({ skills: allSkills(u), count: 20 }), 'worksheet', 'Q');
  for (const block of plan.sections[0].blocks) {
    const original = byId.get(block.q.id);
    assert.ok(original, 'question exists in bank');
    assert.equal(C.answerText(block.q), C.answerText(original));
    assert.equal(JSON.stringify(block.q.solutionSteps), JSON.stringify(original.solutionSteps));
  }
});

test('page, scripts, styles and course links are wired for the Grade 5 generators', () => {
  const page = read('worksheet-generator/grade5-generators.html');
  for (const src of ['../data.js', '../course-catalog.js', '../question-bank-adapter.js', '../question-bank-loader.js',
    'core/math-display.js', 'grade5/generators-content.js', 'grade5/generators-core.js',
    'grade5/generators-pagination.js', 'grade5/generators-render.js', 'grade5/generators.js']) {
    assert.ok(page.includes(src), 'missing script ' + src);
  }
  for (const id of ['config', 'previewTools', 'notice', 'output', 'printRoot']) assert.ok(page.includes('id="' + id + '"'), 'missing #' + id);
  const css = read('worksheet-generator/grade5/generators.css');
  for (const sel of ['.pl-page', '@page', '#printRoot', '.g5maze', '.g5colorgrid', '.g5match', '.g5station', '.g5error', '.g5partners', 'print-color-adjust']) {
    assert.ok(css.includes(sel), 'missing style ' + sel);
  }
  const catalog = read('grade5-resource-catalog.js');
  for (const mode of ['lesson', 'worksheet', 'assessment', 'activity']) {
    assert.ok(catalog.includes('grade5-generators.html?unit=') || catalog.includes('mode=' + mode), 'catalog links ' + mode);
  }
});
