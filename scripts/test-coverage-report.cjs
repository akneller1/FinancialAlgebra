#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),ctx={window:{}};
for(const f of ['data.js','course-catalog.js','question-bank-adapter.js','coverage-report.js']){
vm.runInNewContext(fs.readFileSync(path.join(root,f),'utf8'),ctx,{filename:f});
}
const c=ctx.window.MK_COVERAGE_REPORT,lib=ctx.window.LIBRARY;
let report=c.report(lib);
assert.equal(report.length,11);
assert.equal(report.reduce((n,r)=>n+r.unitCount,0),102);
assert.equal(report.reduce((n,r)=>n+r.skillCount,0),819);
assert.equal(report.reduce((n,r)=>n+r.approvedQuestions,0),0);
const only=c.report(lib,'algebra2');assert.equal(only.length,1);assert.equal(only[0].unitCount,11);
const s=ctx.window.MK_COURSE_CATALOG.getSkillRecords('algebra2','conic-sections')[0].id;
const bank={schemaVersion:1,courseId:'algebra2',unitId:'conic-sections',questions:[
{ id:'fixture',skillId:s,level:'cp2',format:'short-answer',prompt:'Fixture only',answer:'1',solutionSteps:['Fixture']}]};
assert.equal(ctx.window.MK_QUESTION_BANKS.register(bank,{verified:true}).ok,true);
report=c.report(lib,'algebra2');
assert.equal(report[0].approvedQuestions,1);
assert.equal(report[0].units.find(u=>u.id==='conic-sections').skills[0].counts.cp2,1);
assert.equal(report[0].fullyCovered,0,'One difficulty is not complete');
console.log('PASS eleven-course coverage reporting and level-by-level approved question counts');
