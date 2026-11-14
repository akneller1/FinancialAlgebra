import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {skillId} from '../src/outline-template.js';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const c=JSON.parse(read('course-outlines/grade1.json'));
// The current Claude course replaced the former IM outline. Check the active
// 12-unit curriculum against the independently published curriculum map.
const map=JSON.parse(read('docs/math1/curriculum-map.json'));
const ids=["count-120", "add-subtract-10", "add-subtract-20", "equal-sign", "word-problems-20", "tens-ones", "compare-numbers", "add-subtract-100", "measuring-length", "telling-time", "data", "shapes-equal-shares"];
test('Grade 1: current twelve-unit course has 47 learning targets',()=>{
 assert.equal(c.id,'math1');
 assert.equal(c.status,'development');
 assert.ok(c.source.title.includes('Common Core'));
 assert.deepEqual(c.units.map(u=>u.id),ids);
 assert.equal(c.units.reduce((n,u)=>n+u.skills.length,0),47);
 assert.equal(Object.keys(c.standards).length,24);
 assert.deepEqual(map.units.map(u=>u.id),ids);
});
test('Grade 1: every target has stable IDs and complete standards coverage',()=>{
 const covered=new Set();
 for(const [ui,unit] of c.units.entries()){
  assert.equal(unit.status,'development');
  assert.equal(unit.skills.length,new Set(unit.skills).size);
  assert.equal(unit.skills.length,unit.targets.length);
  assert.equal(unit.skills.length,unit.skillStandards.length);
  assert.equal(unit.skills.length,map.units[ui].skills.length);
  for(const [i,name] of unit.skills.entries()){
   const mapped=map.units[ui].skills[i];
   assert.equal(mapped.id,skillId(unit.id,i));
   assert.equal(mapped.name,name);
   assert.equal(mapped.target,unit.targets[i]);
   assert.deepEqual(mapped.standards,unit.skillStandards[i]);
   assert.ok(name.trim().length>0);
   assert.ok(unit.targets[i].startsWith('I can '));
   assert.ok(unit.skillStandards[i].length>0);
   for(const code of unit.skillStandards[i]){
    assert.ok(c.standards[code],'Unmapped standard '+code);
    covered.add(code);
   }
  }
 }
 assert.deepEqual([...covered].sort(),Object.keys(c.standards).sort());
});
test('Grade 1: page, navigation, and source-based outline are wired',()=>{
 const page=read('grade1.html'),script=read('src/grade1-site.js');
 const renderer=read('src/outline-template.js');
 assert.ok(page.includes('styles.css')&&page.includes('site-overrides.css'));
 assert.ok(script.includes('course-outlines/grade1.json'));
 assert.ok(page.includes('src/grade1-site.js'));
 assert.ok(renderer.includes('Curriculum Sections &amp; Standards'));
 assert.ok(renderer.includes('estimatedDaysMax'));
 assert.ok(renderer.includes('resource templates ready'));
 for(const existing of ['grade2.html','grade3.html','grade4.html']){
  assert.ok(read(existing).includes('href="grade1.html"'));
 }
 assert.ok(!read('index.html').includes('href="grade1.html"'),'Unfinished Grade 1 must stay off the staging homepage');
 assert.ok(!read('grade5.html').includes('href="grade1.html"'),'Grade 5 picker should not advertise unfinished Grade 1');
 assert.ok(existsSync(new URL('../styles.css',import.meta.url)));
});
