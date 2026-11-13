import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {validateOutline,skillId} from '../src/outline-template.js';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const has=p=>existsSync(new URL('../'+p,import.meta.url));
// The 12-unit Math Expressions outline is a separate legacy source.
// The released Grade 4 bank uses the 10-unit CCSS authoring outline.
const authored=JSON.parse(read('tools/grade4-authoring/outline.json'));
const course={id:'math4',standards:authored.standards,units:authored.units.map(u=>({id:u.id,name:u.name,skills:u.skills.map(s=>s[0]),skillStandards:u.skills.map(s=>s[1]),standards:[...new Set(u.skills.flatMap(s=>s[1]))]}))};
const manifest=JSON.parse(read('manifest.json'));
const LEVELS=['cp2','cp1','honors'];

test('Grade 4 course: ten Common Core units, 49 skills, every Grade 4 standard mapped',()=>{
 assert.equal(course.id,'math4');
 assert.deepEqual(validateOutline(course),{units:10,skills:49});
 const covered=new Set(course.units.flatMap(u=>u.skillStandards.flat()));
 assert.equal(Object.keys(course.standards).length,35);
 for(const code of Object.keys(course.standards))assert.ok(covered.has(code),'uncovered '+code);
 for(const u of course.units){assert.equal(u.skills.length,u.skillStandards.length);assert.equal(new Set(u.skills).size,u.skills.length);}
});

test('Grade 4 banks: approved manifest entries, 30 questions per skill and level, valid records and diagrams',()=>{
 const entries=manifest.banks.filter(b=>b.courseId==='math4');
 assert.deepEqual(entries.map(b=>b.unitId),course.units.map(u=>u.id));
 const ids=new Set(),prompts=new Set();
 for(const [i,u] of course.units.entries()){
  const e=entries[i];assert.equal(e.approved,true);assert.equal(e.path,'question-banks/math4/'+u.id+'.json');
  const bank=JSON.parse(read(e.path));assert.equal(bank.schemaVersion,1);assert.equal(bank.courseId,'math4');assert.equal(bank.unitId,u.id);
  assert.ok(has('math4/meta/'+u.id+'.meta.json'),'meta '+u.id);
  const count={};
  for(const q of bank.questions){
   assert.ok(!ids.has(q.id),'duplicate id '+q.id);ids.add(q.id);
   const key=q.prompt+'|'+(q.options||[]).map(o=>o.text).sort().join('|')+'|'+(q.parts||[]).map(p=>p.prompt).join('|')+'|'+(q.diagram?.spec?.alt||'');
   assert.ok(!prompts.has(key),'duplicate question '+q.id);prompts.add(key);
   assert.match(q.skillId,new RegExp('^'+u.id+'-skill-\\d\\d$'));assert.ok(LEVELS.includes(q.level));
   assert.ok(['short-answer','multiple-choice','select-all','open-response'].includes(q.format));
   assert.ok(q.answer!==undefined&&q.answer!==''&&q.solutionSteps.length>0&&q.standards.length>0,q.id);
   if(q.format==='multiple-choice'){const ok=q.options.filter(o=>o.correct);assert.equal(ok.length,1,q.id);assert.equal(ok[0].text,q.answer,q.id);}
   if(q.diagram){assert.equal(q.diagram.type,'image');assert.ok(q.diagram.spec.alt.length>10,q.id);assert.ok(has(q.diagram.spec.src),q.diagram.spec.src);}
   count[q.skillId+'|'+q.level]=(count[q.skillId+'|'+q.level]||0)+1;
  }
  u.skills.forEach((_,k)=>LEVELS.forEach(l=>assert.equal(count[skillId(u.id,k)+'|'+l],30,skillId(u.id,k)+' '+l)));
 }
 assert.equal(ids.size,4410);
});

test('Grade 4 players, study guides, tools, projects and thumbnails are present',()=>{
 for(const f of ['worksheet-generator/grade4-games.html','worksheet-generator/grade4-flashcards.html','worksheet-generator/grade4-understanding-check.html',
  'worksheet-generator/grade4/config.js','worksheet-generator/elementary/el-core.js','worksheet-generator/elementary/el-games.js','tools/grade4-authoring/staging/assemble-grade4.mjs'])assert.ok(has(f),f);
 const tools=JSON.parse(read('tools/grade4-authoring/interactive/manifest.json')).tools;assert.equal(tools.length,9);
 for(const t of tools){assert.ok(has('artifacts/'+t.slug+'/index.html'),t.slug);assert.ok(has('thumbs/'+t.slug+'.svg'),t.slug);}
 const proj=JSON.parse(read('tools/grade4-authoring/projects/projects-registry.json'));
 for(const u of course.units){
  assert.ok(has('artifacts/math4-'+u.id+'-cheat-sheet/worksheet.pdf'),'cheat sheet '+u.id);
  assert.ok(has('worksheet-generator/grade4/flashcards/'+u.id+'.json'),'flashcards '+u.id);
  assert.ok((proj['math4-'+u.id]||[]).length>=1,'project '+u.id);
  for(const p of proj['math4-'+u.id])for(const f of ['index.html',p.slug+'-cp2.pdf',p.slug+'-cp1.pdf',p.slug+'-honors.pdf',p.slug+'-teacher-guide.pdf'])assert.ok(has('artifacts/'+p.folder+'/'+f),p.folder+'/'+f);
 }
 const games=JSON.parse(read('tools/grade4-authoring/games.json')).games;
 for(const g of games)assert.ok(has('thumbs/math4-game-'+g.thumb+'.svg'),g.id);
 assert.equal(new Set(games.map(g=>g.thumb)).size,games.length,'every game has its own thumbnail');
});
