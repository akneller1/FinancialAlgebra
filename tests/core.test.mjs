import test from 'node:test';
import assert from 'node:assert/strict';
import {course,getUnit,getSkillRecords} from '../src/course.js';

test('Financial Algebra has ten outline units and one level',()=>{
 assert.equal(course.id,'financial-algebra');
 assert.deepEqual(course.levels,['standard']);
 assert.equal(course.units.length,10);
 assert.ok(course.units.every(u=>u.status==='outline'));
 assert.equal(course.units.reduce((n,u)=>n+u.skills.length,0),40);
});
test('Financial Algebra IDs are unchanged and stable for future questions',()=>{
 assert.deepEqual(course.units.map(u=>u.id),[
 'income','budgeting','banking','credit','borrowing','investing','housing','insurance','college','retirement'
 ]);
 for(const u of course.units){
  assert.equal(getUnit(u.id),u);
  assert.equal(new Set(u.skills).size,u.skills.length);
  const skills=getSkillRecords(u.id);
  assert.equal(skills.length,u.skills.length);
  for(const [i,skill] of skills.entries()){
   assert.equal(skill.id,u.id+'-skill-'+String(i+1).padStart(2,'0'));
   assert.equal(skill.name,u.skills[i]);
  }
 }
});
