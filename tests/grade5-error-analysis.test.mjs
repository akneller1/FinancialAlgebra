import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const read = p => fs.readFileSync(new URL(p, root), 'utf8');
const context = { console };
context.window = context;
vm.createContext(context);
vm.runInContext(read('worksheet-generator/grade5/generators-core.js'), context);
const engine = context.G5_GENERATORS_CORE;
const ids = [
  'place-value-number-sense','multi-digit-multiplication-division',
  'decimal-operations','numerical-expressions-patterns',
  'fraction-addition-subtraction','fraction-multiplication-division',
  'measurement-conversions','volume-three-dimensional-figures',
  'coordinate-plane-graphing','classifying-two-dimensional-figures',
  'data-line-plots-problem-solving'
];

test('Error Analysis has verified questions at every Grade 5 unit and level', () => {
  for (const id of ids) {
    const bank = JSON.parse(read('math5/' + id + '.json'));
    const meta = JSON.parse(read('math5/meta/' + id + '.meta.json'));
    const skills = [...new Set(bank.questions.map(q => q.skillId))].map(skillId => ({ id: skillId }));
    const unit = { id, name: id, skills, questions: bank.questions, meta };
    for (const level of ['cp2','cp1','honors']) {
      const options = engine.options({ activity: 'error', level, count: 8, skills: skills.map(s => s.id) });
      const result = engine.buildActivity(unit, options, 'error-analysis-' + id + '-' + level);
      assert.equal(result.kind, 'error');
      assert.ok(result.items.length >= 6, id + ' ' + level + ': insufficient items');
      for (const item of result.items) {
        const wrong = engine.norm(item.wrong);
        assert.notEqual(wrong, engine.norm(engine.answerText(item.q)), item.q.id);
        const verified = [
          ...(item.q.options || []).filter(x => !x.correct).map(x => engine.norm(x.text)),
          ...Object.keys((meta[item.q.id] || {}).distractors || {}).map(engine.norm)
        ];
        assert.ok(verified.includes(wrong), item.q.id + ': unverified error');
      }
    }
  }
});
