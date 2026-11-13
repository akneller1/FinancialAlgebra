#!/usr/bin/env node
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const site=path.resolve(process.env.GRADE1_SITE||'../classroom/_site');
const manifest=JSON.parse(fs.readFileSync('question-banks/math1/manifest.json'));
const content=JSON.parse(fs.readFileSync(path.join(site,'grade1-staging/content-index.json')));
const banks=new Map(),questions=new Map(),skillSets={};
for(const entry of manifest.banks){const b=JSON.parse(fs.readFileSync('question-banks/'+entry.path));banks.set(entry.unitId,b.questions);b.questions.forEach(q=>questions.set(q.id,q));skillSets['grade1-'+entry.unitId]={unitName:entry.unitId};}
const original=JSON.stringify([...banks]);
const PR={MODES:{partner:{}},KINDS:[],capable(){return 'original-capability'},build(){return 'original-build'}};
const N={printables:PR,skillSets,courseLevelName(id,l){return l},grade1StagingQuestion(id,qid){const q=questions.get(qid);return {sourceId:q.id,prompt:q.prompt,skill:q.skillId,c:4,steps:q.solutionSteps.map(t=>({t})),fig:q.diagram?{src:q.diagram.spec.src,alt:q.diagram.spec.alt}:null};}};
const G={MKMENU:N,MK_GRADE1_STAGING:{content},MK_QUESTION_BANKS:{select(o){return banks.get(o.unitId).filter(q=>q.level===o.level&&o.formats.includes(q.format));}}};
vm.runInNewContext(fs.readFileSync(path.join(site,'grade1-staging/printables.js'),'utf8'),{window:G,Set,Map,Math});
let scopes=0,partnerAvailable=0,partnerUnavailable=0,partnerRows=0,matchingItems=0;const unavailable=[];
for(const [unit,qs] of banks)for(const skill of new Set(qs.map(q=>q.skillId)))for(const level of ['cp2','cp1','honors']){
 const cfg={unitId:'grade1-'+unit,skills:{[skill]:true},level,seed:'verified-printables',count:8};
 const match=PR.build({...cfg,kind:'answer-match'},0);
 assert(!match.error);assert(match.items.length>0);assert.equal(match.items.length,new Set(match.items.map(it=>it.p.sourceId)).size);
 assert.equal(new Set(match.answers.map(a=>G.MK_GRADE1_PRINTABLES.key(a.value))).size,match.answers.length);
 assert.equal(JSON.stringify(match),JSON.stringify(PR.build({...cfg,kind:'answer-match'},0)));
 for(const it of match.items){const q=questions.get(it.p.sourceId);assert.equal(q.skillId,skill);assert.equal(q.level,level);assert.equal(it.p.prompt,q.prompt);assert.equal(it.key,String(q.answer));assert.equal(G.MK_GRADE1_PRINTABLES.key(match.answers.find(a=>a.letter===it.letter).value),G.MK_GRADE1_PRINTABLES.key(q.answer));assert.equal(!!it.p.fig,!!q.diagram);}
 matchingItems+=match.items.length;
 const partner=PR.build({...cfg,kind:'partner'},0);
 if(partner.error){partnerUnavailable++;unavailable.push({skill,level});}
 else{
  partnerAvailable++;partnerRows+=partner.rows.length;const answerValues=new Set();
  for(const row of partner.rows){const a=questions.get(row.A.p.sourceId),b=questions.get(row.B.p.sourceId);assert.notEqual(a.id,b.id);assert.equal(a.skillId,skill);assert.equal(b.skillId,skill);assert.equal(a.level,level);assert.equal(b.level,level);assert.notEqual(content[a.id],content[b.id]);assert.equal(G.MK_GRADE1_PRINTABLES.key(a.answer),G.MK_GRADE1_PRINTABLES.key(b.answer));assert(!answerValues.has(G.MK_GRADE1_PRINTABLES.key(a.answer)));answerValues.add(G.MK_GRADE1_PRINTABLES.key(a.answer));}
  assert.equal(JSON.stringify(partner),JSON.stringify(PR.build({...cfg,kind:'partner'},0)));
 }
 scopes++;
}
assert.equal(scopes,279);assert.equal(JSON.stringify([...banks]),original,'Bank mutated');
assert.equal(PR.build({unitId:'grade5-test',kind:'partner'}),'original-build');assert.equal(PR.capable('grade5-test','skill','answer-match'),false);
const result={passed:true,scopes,matchingItems,partnerAvailable,partnerUnavailable,partnerRows,unavailable};
fs.mkdirSync('grade1-integration-results',{recursive:true});fs.writeFileSync('grade1-integration-results/printables.json',JSON.stringify(result,null,2));console.log(JSON.stringify({...result,unavailable:unavailable.length}));
