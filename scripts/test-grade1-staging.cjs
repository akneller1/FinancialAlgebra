#!/usr/bin/env node
// Development-only integration contract. Never registers or approves banks.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),cp=require('node:child_process');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const manifest=read('question-banks/math1/manifest.json');
assert.deepEqual(manifest,JSON.parse(cp.execFileSync('git',['show',process.env.G1_BASE_REF||'21bdadb:question-banks/math1/manifest.json'],{encoding:'utf8'})),'Approval manifest changed');
const context={};vm.createContext(context);vm.runInContext(fs.readFileSync('tools/grade1-authoring/staging-puzzle.js','utf8'),context);
let scopes=0,visual=0,restricted=0;
for(const {unitId} of manifest.banks){
 const file='question-banks/math1/'+unitId+'.json';
 const bank=read(file),before=JSON.parse(cp.execFileSync('git',['show','21bdadb:'+file],{encoding:'utf8',maxBuffer:20*1024*1024}));
 const identity=q=>({id:q.id,skillId:q.skillId,level:q.level,standards:q.standards});
 assert.deepEqual(bank.questions.map(identity).sort((a,b)=>a.id.localeCompare(b.id)),before.questions.map(identity).sort((a,b)=>a.id.localeCompare(b.id)),'IDs, levels, skills, or standards changed');
 const checks=read('tools/grade1-authoring/out/'+unitId+'.checks.json');
 for(const q of bank.questions){
  assert.equal(Boolean(q.diagram),Boolean(checks[q.id].diagram),'Diagram/check inventory mismatch '+q.id);
  assert(!/facts_(oa|nbt|md|g)/.test(checks[q.id].family),'Generic filler '+q.id);
 }
 for(const skill of new Set(bank.questions.map(q=>q.skillId)))for(const level of ['cp2','cp1','honors']){
  const model=context.G1StagingPuzzle.prepare(bank.questions,skill,level);
  assert(model.pairs>=4);assert.equal(model.cards.length,model.pairs*2);
  const questions=model.cards.filter(c=>c.kind==='question'),answers=model.cards.filter(c=>c.kind==='answer');
  for(const q of questions){assert(answers.some(a=>a.value===q.value));assert(bank.questions.some(x=>x.id===q.questionId&&x.skillId===skill&&x.level===level));}
  // Matching uses answer values: every equivalence class has equally many Q and A cards.
  for(const value of new Set(model.cards.map(c=>c.value)))assert.equal(questions.filter(c=>c.value===value).length,answers.filter(c=>c.value===value).length);
  visual+=questions.some(c=>c.image)?1:0;restricted+=model.distinctAnswers<4?1:0;scopes++;
 }
}
assert.equal(scopes,279);
console.log(JSON.stringify({passed:true,scopes,scopesUsingImages:visual,scopesWithFewerThanFourAnswerValues:restricted,preserved:'all IDs, skill IDs, levels, standards and complete approval manifest'},null,2));
