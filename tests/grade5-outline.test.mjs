import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {outlineStats,skillId,validateOutline} from '../src/outline-template.js';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const c=JSON.parse(read('course-outlines/grade5.json'));
test('grade 5 outline matches the supplied 13-unit, 80-skill sequence',()=>{
 const totals=validateOutline(c);
 assert.deepEqual(totals,{units:13,skills:80});
 assert.equal(c.id,'math5');
 assert.equal(c.status,'outline');
 assert.ok(c.units.every(u=>u.status==='outline'));
 assert.deepEqual(c.units.map(u=>u.name),[
  'Place Value','Multiply Whole Numbers','Divide by a One-Digit Divisor','Divide by a Two-Digit Divisor',
  'Add and Subtract Decimals','Multiply and Divide Decimals','Expressions and Patterns','Fractions and Decimals',
  'Add and Subtract Fractions','Multiply and Divide Fractions','Measurement','Geometry','Bridging to 6th Grade']);
 assert.deepEqual(c.units.map(u=>u.skills.length),[7,7,7,4,5,9,5,6,9,6,5,5,5]);
});
test('grade 5 keeps the source continuation on PDF page 4 in Unit 13',()=>{
 const last=c.units.at(-1);
 assert.deepEqual(last.sourcePages,[3,4]);
 assert.ok(last.skills.includes('Measure with a Ruler'));
 assert.ok(last.skills.some(s=>s.includes('Mean, Median, Range, and Mode')));
 assert.ok(last.standards.includes('CC.2.4.6.B.1'));
});
test('unit and skill IDs are deterministic and standards are source-mapped',()=>{
 const ids=new Set();
 for(const u of c.units){
  assert.match(u.id,/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
  assert.equal(ids.has(u.id),false);
  ids.add(u.id);
  assert.equal(u.skills.length,new Set(u.skills).size,'Duplicate skill within '+u.id);
  for(const [i,name]of u.skills.entries()){
   assert.ok(name.length>3);
   assert.equal(skillId(u.id,i),u.id+'-skill-'+String(i+1).padStart(2,'0'));
  }
  for(const code of u.standards){
   assert.ok(typeof c.standards[code]==='string'&&c.standards[code].length>10);
  }
 }
 // The uploaded PDF's abbreviated Unit 8 code and Unit 3 standards are retained as supplied.
 assert.ok(c.units[7].standards.includes('A-F.2.1.3'));
 assert.ok(c.units[2].standards.includes('M05.A-T.2.1.2'));
});
test('Grade 5 keeps the original source sequence within one Classroom-style class page',()=>{
 const page=read('grade5.html'),site=read('src/grade5-site.js');
 const catalog=read('grade5-resource-catalog.js'),legacy=read('grade5-resources.html');
 assert.ok(page.includes('styles.css')&&page.includes('site-overrides.css'));
 assert.ok(page.includes('src/grade5-site.js'));
 assert.ok(page.includes('grade5-resource-catalog.js'));
 assert.ok(!page.includes('href="grade5-resources.html"'));
 assert.ok(read('index.html').includes('href="grade5.html"'));
 assert.ok(site.includes('course-outlines/grade5.json'));
 assert.ok(site.includes('Original curriculum sequence (13 pacing units)'));
 assert.ok(site.includes('cards grouped-cards'));
 assert.ok(site.includes('generator-banner compact'));
 for(const section of ['Games','Study Guides','Interactive Math','Projects']){
  assert.ok(site.includes('title:\''+section+'\''),section+' section');
 }
 assert.ok(catalog.includes('worksheet-generator/grade5-games.html'));
 assert.ok(catalog.includes('worksheet-generator/grade5-understanding-check.html'));
 assert.ok(legacy.includes('location.replace'));
 assert.ok(existsSync(new URL('../styles.css',import.meta.url)));
});
