import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {skillId} from '../src/outline-template.js';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const c=JSON.parse(read('course-outlines/grade2.json'));
// The current Claude course replaced the former IM outline. Check the active
// 12-unit curriculum against the independently published curriculum map.
const map=JSON.parse(read('docs/math2/curriculum-map.json'));
const ids=['add-subtract-20','odd-even-arrays','place-value-1000','count-compare-1000','add-subtract-100','word-problems-100','add-subtract-1000','measuring-length','length-number-line','time-money','graphs-data','shapes-equal-shares'];
test('Grade 2: current twelve-unit course has 53 learning targets',()=>{
 assert.equal(c.id,'math2');
 assert.equal(c.status,'development');
 assert.ok(c.source.title.includes('Common Core'));
 assert.deepEqual(c.units.map(u=>u.id),ids);
 assert.equal(c.units.reduce((n,u)=>n+u.skills.length,0),53);
 assert.equal(Object.keys(c.standards).length,28);
 assert.deepEqual(map.units.map(u=>u.id),ids);
});
test('Grade 2: every target has stable IDs and complete standards coverage',()=>{
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
test('Grade 2: page, navigation, and source-based outline are wired',()=>{
 const page=read('grade2.html'),script=read('src/grade2-site.js');
 const renderer=read('src/outline-template.js');
 assert.ok(page.includes('styles.css')&&page.includes('site-overrides.css'));
 assert.ok(script.includes('course-outlines/grade2.json'));
 assert.ok(page.includes('src/grade2-site.js'));
 assert.ok(renderer.includes('Curriculum Sections &amp; Standards'));
 assert.ok(renderer.includes('estimatedDaysMax'));
 assert.ok(renderer.includes('resource templates ready'));
 for(const existing of ['grade1.html','grade3.html','grade4.html']){
  assert.ok(read(existing).includes('href="grade2.html"'));
 }
 assert.ok(!read('index.html').includes('href="grade2.html"'),'Unfinished Grade 2 must stay off the staging homepage');
 assert.ok(!read('grade5.html').includes('href="grade2.html"'),'Grade 5 picker should not advertise unfinished Grade 2');
 assert.ok(existsSync(new URL('../styles.css',import.meta.url)));
});
