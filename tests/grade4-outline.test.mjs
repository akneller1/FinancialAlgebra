import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {validateOutline,skillId} from '../src/outline-template.js';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const course=JSON.parse(read('course-outlines/grade4.json'));
test('Grade 4 source curriculum contains all twelve units in source order',()=>{
 assert.equal(course.id,'math4');
 assert.equal(course.source.pages,15);
 assert.equal(course.units.length,12);
 assert.deepEqual(course.units.map(x=>x.name),[
  'Solve Multiplication and Division Word Problems','Quadrilaterals',
  'Place Value and Multi-Digit Addition & Subtraction','Angles & Polygons',
  'Multi-Digit Multiplication','The Metric Measurement System',
  'Multi-Digit Division','Patterns, Functions, and Graphs',
  'Fractions','Three-Dimensional Figures','Decimal Numbers','The U.S. Customary System'
 ]);
 assert.deepEqual(course.units.map(u=>u.sourcePages),[[1],[2],[3,4],[5],[6],[7],[8],[10],[11,12],[13],[14],[15]]);
});
test('Grade 4 pacing and source resource notes are retained',()=>{
 assert.deepEqual(course.units.map(u=>u.estimatedDays),[12,10,28,9,26,8,21,8,27,5,15,8]);
 assert.deepEqual(course.units.map(u=>u.reportedLessons),[9,6,20,7,17,5,14,5,22,3,15,5]);
 assert.equal(course.units.reduce((n,u)=>n+u.estimatedDays,0),177);
 assert.equal(course.units.reduce((n,u)=>n+u.reportedLessons,0),128);
 assert.ok(course.units[2].resourceNote.includes('3.2'));
 assert.ok(course.units[7].resourceNote.includes('8.5'));
 assert.ok(course.units[7].resourceNote.includes('x/y'));
});
test('all 107 editorial learning targets and source categories have stable identifiers',()=>{
 const stats=validateOutline(course);
 assert.deepEqual(stats,{units:12,skills:107});
 for(const u of course.units){
  assert.equal(u.status,'outline');
  assert.equal(u.standards.length,0);
  assert.ok(u.skills.length>=5);
  assert.equal(new Set(u.skills).size,u.skills.length);
  assert.ok(u.objectiveGroups.length>=2);
  assert.ok(u.objectiveGroups.every(g=>g.category&&g.items.length&&g.items.every(t=>t.length>20)));
  assert.equal(skillId(u.id,0),u.id+'-skill-01');
  assert.equal(skillId(u.id,u.skills.length-1),u.id+'-skill-'+String(u.skills.length).padStart(2,'0'));
 }
});
test('Grade 4 preserves meaningful source qualifications',()=>{
 const joined=JSON.stringify(course).toLocaleLowerCase();
 for(const term of ['12 × 12','prime and composite','six digits','quarter','twelfths','hundredths','x/y','1–50']){
  assert.ok(joined.includes(term.toLocaleLowerCase()),'Missing '+term);
 }
 assert.ok(joined.includes('the source repeats these two objectives'));
 assert.ok(course.units[8].sourcePages.includes(12));
});
test('Grade 4 page reuses the existing generic outline renderer and does not advertise finished activities',()=>{
 const page=read('grade4.html'),js=read('src/grade4-site.js'),template=read('src/outline-template.js');
 assert.ok(page.includes('styles.css'));
 assert.ok(page.includes('site-overrides.css'));
 assert.ok(page.includes('src/grade4-site.js'));
 assert.ok(js.includes('course-outlines/grade4.json'));
 assert.ok(read('index.html').includes('grade4.html'));
 assert.ok(read('grade5.html').includes('grade4.html'));
 assert.ok(template.includes('objectiveGroups'));
 assert.ok(template.includes('Source Objectives by Category'));
 assert.ok(template.includes('Coming soon'));
 assert.ok(template.includes('aria-disabled="true"'));
 assert.ok(existsSync(new URL('../styles.css',import.meta.url)));
});
