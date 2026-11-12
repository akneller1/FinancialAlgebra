import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {unitResources,GAMES,GENERATORS,ACTIVITIES} from '../src/elementary-resources.js';
const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
for(let grade=1;grade<=4;grade++) {
 const course=JSON.parse(read('course-outlines/grade'+grade+'.json'));
 test('Grade '+grade+': every unit has the shared engines and course-scoped links',()=>{
  for(const unit of course.units) {
   const resources=unitResources(course,unit);
   assert.equal(new Set(resources.map(r=>r.id)).size,resources.length);
   for(const [game] of GAMES) assert.ok(resources.some(r=>r.id===game));
   for(const [mode] of GENERATORS) assert.ok(resources.some(r=>r.id===mode));
   for(const [kind] of ACTIVITIES) assert.ok(resources.some(r=>r.id==='activity-'+kind));
   for(const id of ['flashcards','readiness']) assert.ok(resources.some(r=>r.id===id));
   for(const r of resources) {
    const url=new URL(r.path,'https://example.test/');
    assert.equal(url.searchParams.get('course'),course.id);
    assert.equal(url.searchParams.get('unit'),unit.id);
    assert.ok(fs.existsSync(new URL('../'+url.pathname.slice(1),import.meta.url)));
    assert.ok(fs.existsSync(new URL('../'+r.thumb,import.meta.url)),r.thumb);
   }
   assert.equal(resources.some(r=>r.id==='fraction-frenzy'),/fraction/i.test(unit.name));
  }
 });
 test('Grade '+grade+': runtime never requests another grade bank',async()=>{
  const unit=course.units[0]; const requests=[];
  const context={URLSearchParams,location:{search:'?course='+course.id+'&unit='+unit.id},document:{},
   MK_ELEMENTARY_COURSE:course,MK_BANK_LOADER:{async loadUnitFromSite(...args){requests.push(args);return []}}};
  context.window=context;
  vm.runInNewContext(read('worksheet-generator/grade5/g5-core.js'),context);
  await assert.rejects(context.G5.load(unit.id),/not published yet/);
  assert.equal(requests[0][0],course.id); assert.equal(requests[0][1],unit.id);
  const question={id:'test',skillId:unit.id+'-skill-01',answer:'4'};
  context.MK_BANK_LOADER.loadUnitFromSite=async()=>[course.id+'/'+unit.id];
  context.fetch=async path=>{assert.ok(path.startsWith('../'+course.id+'/meta/'));return {ok:false}};
  context.MK_QUESTION_BANKS={select(options){assert.equal(options.courseId,course.id);assert.equal(options.unitId,unit.id);return [question]}};
  assert.equal((await context.G5.load(unit.id))[0],question);
 });
}
test('Grade 5 entry points keep their original default bank',()=>{
 const c={URLSearchParams,location:{search:''},document:{}};c.window=c;
 vm.runInNewContext(read('worksheet-generator/grade5/g5-core.js'),c);
 assert.equal(c.G5.COURSE,'math5');assert.equal(c.G5.COURSE_NAME,'Grade 5');
});
test('Empty bank initializes real generator controls before generation',async()=>{
 const course=JSON.parse(read('course-outlines/grade1.json')),unit=course.units[0];
 const nodes=Object.fromEntries(['config','notice','output','previewTools','printRoot','questionEditor'].map(id=>[id,{innerHTML:'',textContent:'',querySelectorAll(){return []},replaceChildren(){this.innerHTML=''}}]));
 const c={URL,URLSearchParams,console,location:{href:'https://example.test/worksheet-generator/elementary-resource.html?course=math1&unit='+unit.id+'&tool=generators&mode=worksheet',search:'?unit='+unit.id+'&mode=worksheet'},
 MK_ELEMENTARY_COURSE:course,LIBRARY:{courses:[course]},history:{replaceState(){}},localStorage:{getItem(){return null},setItem(){}},addEventListener(){},
 document:{getElementById(id){return nodes[id]||null},querySelector(){return null},querySelectorAll(){return []},addEventListener(){}},
 MK_BANK_LOADER:{async loadUnitFromSite(courseId){assert.equal(courseId,'math1');return []}},
 MK_COURSE_CATALOG:{getSkillRecords(){return unit.skills.map((name,i)=>({name,id:unit.id+'-skill-'+String(i+1).padStart(2,'0')}))}},
 MK_QUESTION_BANKS:{select(){return []}}}; c.window=c;
 for(const file of ['generators-core.js','generators.js'])vm.runInNewContext(read('worksheet-generator/grade5/'+file),c);
 await new Promise(resolve=>setImmediate(resolve));
 assert.equal(c.G5_GENERATORS.state.unit.id,unit.id);
 assert.match(nodes.config.innerHTML,/Add question group/);
 assert.match(nodes.config.innerHTML,/Grade 1 Generators/);
 assert.match(nodes.notice.textContent,/Question bank coming soon/);
 assert.equal(c.G5_GENERATORS.state.plan,null);
 assert.doesNotMatch(nodes.config.innerHTML,/Copy student link/);
});
