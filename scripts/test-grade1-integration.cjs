#!/usr/bin/env node
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=path.resolve(__dirname,'..'),site=path.resolve(process.env.GRADE1_SITE||path.join(source,'../classroom/_site'));
const read=p=>JSON.parse(fs.readFileSync(path.join(site,p)));
const staging=read('grade1-staging/manifest.json');assert.equal(staging.staging,true);assert.equal(staging.banks.length,8);assert(staging.banks.every(b=>b.approved===false));
assert(!read('question-banks/manifest.json').banks.some(b=>['math1','grade1'].includes(b.courseId)));
assert(!read('elementary/manifest.json').banks.some(b=>['math1','grade1'].includes(b.courseId)));
assert.equal(JSON.parse(fs.readFileSync(path.join(source,'question-banks/math1/manifest.json'))).review.editorialApproval.approved,false);
const context={window:{}};context.globalThis=context.window;
for(const file of ['data.js','course-integrations.js','course-catalog.js','grade5/grade5-main-catalog.js','elementary-preload-catalog.js'])vm.runInNewContext(fs.readFileSync(path.join(site,file),'utf8'),context);
const c=context.window.LIBRARY.courses.find(c=>c.id==='grade1');assert(c.staging);assert.equal(c.units.length,8);
let questions=0,images=0;
for(const b of staging.banks){const bank=read('grade1-staging/'+b.path);questions+=bank.questions.length;
 for(const q of bank.questions)if(q.diagram){images++;for(const prefix of ['', 'elementary/'])assert(fs.existsSync(path.join(site,prefix,q.diagram.spec.src)));}
}
assert.equal(questions,8370);assert.equal(images,2820);
for(const page of ['worksheet.html','menu-assessment.html','lesson-planner.html','printables.html']){
 const text=fs.readFileSync(path.join(site,'worksheet-generator',page),'utf8');assert.equal((text.match(/src="\.\.\/grade1-staging\/runtime.js"/g)||[]).length,1);
 assert(text.indexOf('../grade1-staging/runtime.js')<text.indexOf('algebra2-bank-native.js'));
}
console.log(JSON.stringify({passed:true,units:8,questions,images,productionGrade1Entries:0}));
(async()=>{
 const G=context.window;
 G.document={currentScript:{src:'https://staging.test/grade1-staging/runtime.js'},readyState:'loading',addEventListener(){}};
 G.fetch=async url=>{const p=new URL(url,'https://staging.test/').pathname.slice(1);return {ok:true,json:async()=>read(p)}};
 context.URL=URL;context.Promise=Promise;
 for(const file of ['question-bank-adapter.js','question-bank-loader.js','grade1-staging/runtime.js'])vm.runInNewContext(fs.readFileSync(path.join(site,file),'utf8'),context);
 await G.MK_GRADE1_STAGING.ready();
 for(const b of staging.banks)for(const id of ['grade1','math1']){
  assert.equal(G.MK_GRADE1_STAGING.originalAvailable(id,b.unitId),false);
  assert.equal(G.MK_QUESTION_BANKS.available(id,b.unitId),true);
  assert(G.MK_QUESTION_BANKS.select({courseId:id,unitId:b.unitId}).length>0);
  assert(G.MK_QUESTION_BANKS.coverage(id,b.unitId).every(s=>s.verified===false));
 }
 assert.equal(G.MK_QUESTION_BANKS.available('grade2',staging.banks[0].unitId),false);
 console.log('PASS scoped runtime: native and elementary banks available only through the staging facade; every stored bank remains unverified.');
})().catch(e=>{console.error(e);process.exitCode=1});
