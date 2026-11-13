const fs=require('fs'),vm=require('vm'),path=require('path');
const assert=require('node:assert/strict');
const root=process.cwd(),site=path.resolve(process.env.GRADE1_SITE||'../classroom/_site');
const G=require(path.resolve('../classroom/worksheet-generator/menu/tests/load.cjs'))(['games/bank.js','menu/printables.js','menu/printables-scenes.js','menu/printables-cases.js']);
vm.runInContext(fs.readFileSync(path.join(site,'worksheet-generator/menu/printables.js'),'utf8'),G);
const outline=JSON.parse(fs.readFileSync('course-outlines/grade1.json'));outline.id='grade1';G.LIBRARY={courses:[outline]};
G.MK_COURSE_CATALOG={getSkillRecords(c,u){const x=outline.units.find(x=>x.id===u);return c==='grade1'&&x?x.skills.map((name,i)=>({name,id:u+'-skill-'+String(i+1).padStart(2,'0')})):[]}};
vm.runInContext(fs.readFileSync(path.join(site,'question-bank-adapter.js'),'utf8'),G);
const all=new Map();for(const u of outline.units){const b=JSON.parse(fs.readFileSync('question-banks/math1/'+u.id+'.json'));b.courseId='grade1';G.MK_QUESTION_BANKS.register(b,{verified:false});b.questions.forEach(q=>all.set(q.id,q));}
const A=G.MK_QUESTION_BANKS,sel=A.select,avail=A.available;A.select=o=>sel({...o,includeUnverified:true});A.available=(c,u)=>avail(c,u,{includeUnverified:true});
G.MK_BANK_LOADER={loadFromSite(){return Promise.resolve([])}};
vm.runInContext(fs.readFileSync(path.join(site,'worksheet-generator/algebra2-bank-native.js'),'utf8'),G);
(async()=>{
await G.MK_COURSE_BANKS_READY;G.MK_GRADE1_STAGING={content:JSON.parse(fs.readFileSync(path.join(site,'grade1-staging/content-index.json')))};vm.runInContext(fs.readFileSync(path.join(site,'grade1-staging/printables.js'),'utf8'),G);const PR=G.MKMENU.printables;const results=[];
function mystery(B){if(!B.grade1Who)return;assert.equal(B.cards.length,10);const cleared={p:new Set(),l:new Set(),m:new Set()};for(const c of B.cards){const q=all.get(c.item.p.sourceId);assert.equal(q.format,'multiple-choice');assert.deepEqual([...c.opts.map(o=>o.a)].sort(),q.options.map(o=>o.text).sort());assert.equal(c.opts.filter(o=>o.ok).length,1);assert(c.opts[c.pos].ok);assert.equal(c.opts[c.pos].a,q.answer);assert.equal(c.opts[c.pos].clue,c.truth.text);for(const k of ['p','l','m'])if(c.truth[k]!==undefined)cleared[k].add(c.truth[k]);}for(const k of ['p','l','m']){assert.equal(cleared[k].size,5);assert(!cleared[k].has(B.culprit[k]));}}
function walk(x,out=new Set()){if(!x||typeof x!=='object')return out;if(x.sourceId)out.add(x.sourceId);for(const value of Object.values(x))if(value&&typeof value==='object')walk(value,out);return out;}
for(const u of outline.units)for(const level of ['cp2','cp1','honors'])for(const kind of ['maze','color','tarsia','stations','error','who']){
 const cfg=PR.defaultConfig('grade1-'+u.id,kind);cfg.level=level;cfg.seed='full-activity-audit';const start=Date.now(),B=PR.build(cfg,0);
 mystery(B);const qs=[...walk(B)].map(id=>all.get(id));const borrowed=qs.filter(q=>q&&q.level!==level);assert.equal(borrowed.length,0,kind+' borrowed another level');assert(qs.every(q=>q&&q.skillId.startsWith(u.id+'-skill-')));
 if(B.grade1Color){assert.equal(new Set(B.code.map(c=>G.MK_GRADE1_PRINTABLES.key(c.answer))).size,B.code.length);assert.equal(B.code.length,B.items.length);assert(B.groupNum.every(n=>n>=1&&n<=B.items.length));}
 results.push({unit:u.id,level,kind,success:!B.error,error:B.error||null,items:qs.length,borrowed:borrowed.length,ms:Date.now()-start});
 if(results.length%15===0)console.log('Audited '+results.length+' unit/activity selections');
}
let scopes=0;const singles={stations:0,error:0,color:0,tarsia:0,who:0};
for(const u of outline.units)for(const skill of G.MK_COURSE_CATALOG.getSkillRecords('grade1',u.id))for(const level of ['cp2','cp1','honors']){
 for(const kind of ['stations','error','color','tarsia','who']){
  const cfg=PR.defaultConfig('grade1-'+u.id,kind);Object.assign(cfg,{skills:{[skill.id]:true},level,seed:'single-skill-audit'});const B=PR.build(cfg,0);
  if(['stations','error'].includes(kind))assert(!B.error,kind+' '+skill.id+'/'+level);
  if(!B.error){mystery(B);singles[kind]++;for(const id of walk(B)){const q=all.get(id);assert(q);assert.equal(q.level,level);assert.equal(q.skillId,skill.id);}}
 }scopes++;
}
assert.equal(scopes,279);assert.equal(singles.stations,279);assert.equal(singles.error,279);
const summary={passed:true,unitActivitySelections:results.length,successful:results.filter(x=>x.success).length,wrongLevel:results.filter(x=>x.borrowed).length,singleSkillScopes:scopes,singles,unavailable:results.filter(x=>!x.success),results};
fs.mkdirSync('grade1-integration-results',{recursive:true});fs.writeFileSync('grade1-integration-results/activities.json',JSON.stringify(summary,null,2));console.log(JSON.stringify({...summary,results:undefined}));
})().catch(e=>{console.error(e);process.exit(1)});
