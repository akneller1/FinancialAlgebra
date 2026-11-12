import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {validateOutline,skillId} from '../src/outline-template.js';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const c=JSON.parse(read('course-outlines/grade1.json'));
const names=["Adding, Subtracting, and Working with Data","Addition and Subtraction Story Problems","Adding and Subtracting within 20","Numbers to 99","Adding Within 100","Length Measurements Within 120 Units","Geometry and Time","Putting It All Together"];
const pacing=[[14,15],[21,22],[27,28],[21,23],[13,14],[16,17],[17,17],[10,10]];
test('Grade 1: units and original section headings are present',()=>{
 assert.equal(c.id,'math1');
 assert.equal(c.source.format,'HTML');
 assert.equal(c.source.url,'https://im.kendallhunt.com/k5/teachers/grade-1/course-guide/scope-and-sequence.html');
 assert.deepEqual(c.units.map(u=>u.name),names);
 assert.equal(c.units.length,8);
 assert.equal(c.units.reduce((n,u)=>n+u.sections.length,0),27);
 assert.equal(validateOutline(c).skills,93);
 assert.deepEqual(c.units.map(u=>[u.estimatedDays,u.estimatedDaysMax]),pacing);
});
test('Grade 1: each section has source alignment and stable original skill identifiers',()=>{
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
