import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {validateOutline,skillId} from '../src/outline-template.js';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const c=JSON.parse(read('course-outlines/grade2.json'));
const names=["Adding, Subtracting, and Working with Data","Adding and Subtracting within 100","Measuring Length","Addition and Subtraction on the Number Line","Numbers to 1,000","Geometry, Time, and Money","Adding and Subtracting within 1,000","Equal Groups","Putting It All Together"];
const pacing=[[14,18],[12,16],[14,18],[12,15],[11,14],[16,21],[14,18],[10,13],[13,13]];
test('Grade 2: units and original section headings are present',()=>{
 assert.equal(c.id,'math2');
 assert.equal(c.source.format,'HTML');
 assert.equal(c.source.url,'https://im.kendallhunt.com/k5/teachers/grade-2/course-guide/scope-and-sequence.html');
 assert.deepEqual(c.units.map(u=>u.name),names);
 assert.equal(c.units.length,9);
 assert.equal(c.units.reduce((n,u)=>n+u.sections.length,0),25);
 assert.equal(validateOutline(c).skills,89);
 assert.deepEqual(c.units.map(u=>[u.estimatedDays,u.estimatedDaysMax]),pacing);
});
test('Grade 2: each section has source alignment and stable original skill identifiers',()=>{
 for(const unit of c.units){
  assert.equal(unit.status,'outline');
  assert.equal(unit.resource,'Illustrative Mathematics (Kendall Hunt)');
  assert.ok(unit.sections.length>=2);
  assert.equal(unit.skills.length,new Set(unit.skills).size);
  assert.deepEqual(unit.skills,unit.sections.flatMap(section=>section.skills));
  assert.deepEqual(unit.objectiveGroups.map(group=>group.category),unit.sections.map(s=>'Section '+s.letter+': '+s.name));
  for(const [i,name] of unit.skills.entries()){
   assert.ok(name.length>=12);
   assert.equal(skillId(unit.id,i),unit.id+'-skill-'+String(i+1).padStart(2,'0'));
  }
  for(const section of unit.sections){
   assert.ok(section.standards.length>0);
   assert.ok(section.skills.length>0);
   for(const code of section.standards) assert.ok(c.standards[code]);
  }
 }
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
