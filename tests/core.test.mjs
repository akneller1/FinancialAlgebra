import test from 'node:test';
import assert from 'node:assert/strict';
import {budgetSummary,creditPayoff,futureValue} from '../src/engine.js';
import {course,getSkillRecords} from '../src/course.js';
import {makeQuestion,createWorksheet,gradeQuestion} from '../src/questions.js';
test('curriculum has one common level and stable identifiers',()=>{
  assert.equal(course.units.length,10);
  assert.equal(course.levels.length,1);
  assert.deepEqual(course.levels,['standard']);
  assert.equal(getSkillRecords('budgeting')[0].id,'budgeting-skill-01');
  assert.deepEqual(course.units.filter(u=>u.status==='pilot').map(u=>u.id),['budgeting','credit','investing']);
});
test('budget and overdraft',()=>{
  assert.equal(budgetSummary({income:3500,housing:1200,transport:400,essentials:800,savings:500}).remaining,600);
  assert.equal(budgetSummary({income:100,housing:200,transport:0,essentials:0,savings:0}).balanced,false);
});
test('credit payoff with zero APR and partial final payment',()=>{
  const a=creditPayoff({balance:1000,apr:0,payment:100});
  assert.equal(a.months,10);assert.equal(a.interest,0);
  const b=creditPayoff({balance:1000,apr:24,payment:100});
  assert.equal(b.paidOff,true);assert.ok(b.interest>0);
  assert.equal(b.history.at(-1).balance,0);
  assert.equal(creditPayoff({balance:1000,apr:24,payment:20}).paidOff,false);
});
test('compounding: zero and positive returns',()=>{
  const a=futureValue({principal:1000,monthly:100,annualRate:0,years:1});
  assert.equal(a.value,2200);assert.equal(a.growth,0);
  const b=futureValue({principal:1000,monthly:100,annualRate:6,years:1});
  assert.ok(b.growth>0);
});
test('single-level parametric questions have valid keys, grading and skill mappings',()=>{
 for(const unit of ['budgeting','credit','investing']){
  const sheet=createWorksheet(unit,15);
  assert.equal(sheet.length,15);
  for(let i=0;i<90;i++){
    const q=makeQuestion(unit,i);
    assert.equal(q.unitId,unit);
    assert.ok(q.prompt.length>95);
    assert.ok(Number.isFinite(q.answer));
    assert.equal(q.skillId.slice(0,unit.length),unit);
    assert.ok(q.solutionSteps.length);
    assert.equal(gradeQuestion(q,String(q.answer)).correct,true);
    assert.equal(gradeQuestion(q,'').valid,false);
    assert.equal('level' in q,false);
  }
 }
});
