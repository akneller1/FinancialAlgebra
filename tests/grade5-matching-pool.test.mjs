import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const context = {console}; context.window = context;
vm.createContext(context);
for (const file of ['worksheet-generator/grade5/generators-content.js',
                    'worksheet-generator/grade5/generators-core.js']) {
  vm.runInContext(fs.readFileSync(new URL('../' + file, import.meta.url), 'utf8'), context);
}
const core = context.G5_GENERATORS_CORE;

test('matching fills requested count when distinct answers exist despite duplicates', () => {
  const questions = [];
  for (let i = 0; i < 50; i++) {
    questions.push({id:'duplicate-'+i,skillId:'s',level:'cp1',
      format:'short-answer',prompt:'Find another equivalent form '+i,answer:'1',solutionSteps:[]});
  }
  for (let i = 0; i < 10; i++) {
    questions.push({id:'distinct-'+i,skillId:'s',level:'cp1',
      format:'short-answer',prompt:'Find value '+i,answer:String(i+2),solutionSteps:[]});
  }
  const unit = {id:'sample',name:'Sample',number:1,
    skills:[{id:'s',name:'Answers'}],questions,meta:{}};
  const opts = core.options({skills:['s'],level:'cp1',count:10,activity:'matching'});
  for (let i = 0; i < 20; i++) {
    const plan = core.buildActivity(unit,opts,'seed-'+i);
    assert.equal(plan.items.length,10);
    assert.equal(new Set(plan.items.map(q=>core.norm(core.answerText(q)))).size,10);
    assert.equal(plan.answers.length,10);
  }
});
