'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const stage=path.resolve(__dirname,'..'),base=path.resolve(process.env.CLASSROOM_SOURCE_DIR||path.join(stage,'../classroom')),site=path.join(base,'_site');
const read=p=>fs.readFileSync(path.join(site,p),'utf8');
// The active generator UI/engine files are byte-for-byte the main Classroom source.
for(const file of ['worksheet-generator/menu/app.js','worksheet-generator/menu/menu.css','worksheet-generator/menu/engine.js','worksheet-generator/planner/planner-ui.js','styles.css'])assert.equal(read(file),fs.readFileSync(path.join(base,file),'utf8'),file+' drifted from Classroom');
assert.equal((read('index.html').match(/src="elementary-preload-catalog/g)||[]).length,1);
const context={window:{}};context.globalThis=context.window;
for(const file of ['data.js','course-integrations.js','course-catalog.js','grade5/grade5-main-catalog.js','elementary-preload-catalog.js'])vm.runInNewContext(read(file),context,{filename:file});
const G=context.window,grades=G.LIBRARY.courses.filter(c=>/^grade[1-4]$/.test(c.id));
assert.equal(grades.length,4);assert.equal(grades.reduce((n,c)=>n+c.units.length,0),37);
for(const c of grades)for(const u of c.units){
 assert.equal(G.MK_COURSE_CATALOG.getSkills(c.id,u.id).length,G.MK_COURSE_CATALOG.getSkillRecords(c.id,u.id).length);
 for(const [format,page] of [['lesson-planner','lesson-planner.html'],['worksheet-generator','worksheet.html'],['assessment-generator','menu-assessment.html'],['printable-generator','printables.html']]){
  const a=u.artifacts.find(a=>a.bankFormat===format);assert.ok(a,c.id+' '+u.id+' '+format);
  assert.equal(a.path,'worksheet-generator/'+page+'#unit='+c.id+'-'+u.id);
 }
 for(const a of u.artifacts){
  assert.ok(fs.existsSync(path.join(site,a.path.split(/[?#]/)[0])),a.path);
  assert.ok(fs.existsSync(path.join(site,a.thumb)),a.thumb);
  assert.doesNotMatch(a.path,/grade5-generators\.html|tool=generators/);
 }
 assert.ok(u.artifacts.some(a=>a.title==='Flashcards'));assert.ok(u.artifacts.some(a=>a.title==='Readiness Check'));
}
for(const page of ['worksheet.html','menu-assessment.html','lesson-planner.html','printables.html']){
 const text=read('worksheet-generator/'+page);
 assert.ok(text.includes('elementary-preload-catalog.js'),page+' catalog');
 assert.ok(text.includes('elementary-preload-runtime.js'),page+' pending runtime');
 assert.ok(text.includes('grade5-main-catalog.js'),page+' integrated Grade 5');
}
assert.match(read('app.js'),/if \(c.preloaded\) return algebraUnitView\(c, u\)/);
assert.match(read('index.html'),/elementary-preload-catalog/);
assert.match(read('elementary/worksheet-generator/elementary-resource.html'),/location.replace\('\.\.\/\.\.\/worksheet-generator\//);
for(let grade=1;grade<=4;grade++)assert.match(read('grade'+grade+'.html'),new RegExp('#grade'+grade));
// Run the actual native registration against an empty set of future banks.
const native=require(path.join(base,'worksheet-generator/menu/tests/load.cjs'))(['games/bank.js','menu/render.js']);
native.LIBRARY=G.LIBRARY;native.MK_COURSE_CATALOG=G.MK_COURSE_CATALOG;native.MK_ELEMENTARY_PRELOAD=G.MK_ELEMENTARY_PRELOAD;
native.MK_QUESTION_BANKS={available(){return false}};native.MK_COURSE_BANKS_READY=Promise.resolve();
vm.runInContext(read('worksheet-generator/elementary-preload-runtime.js'),native);
(async()=>{
 await native.MK_COURSE_BANKS_READY;
 assert.equal(Object.keys(native.MK_PRELOADED_UNITS).length,37);
 for(const c of grades)for(const u of c.units){
  const id=c.id+'-'+u.id,set=native.MKMENU.skillSets[id];assert.ok(set);
  assert.equal(native.MK_PRELOADED_PLANNER_UNIT(c.id,'u'+(c.units.indexOf(u)+1)),id);
  assert.equal(set.skills.length,G.MK_COURSE_CATALOG.getSkills(c.id,u.id).length);
  const cfg=native.MKMENU.defaultConfig(id,'worksheet');assert.equal(cfg.unitId,id);
  assert.equal(native.MKMENU.generateProblem(id,set.skills[0].id,4,{level:'cp1'},'pending').failed,true);
 }
 console.log('PASS integrated Classroom preview: 37 units; actual native generators, production course/unit renderer, games, guides and scoped pending banks.');
})().catch(e=>{console.error(e);process.exitCode=1});
