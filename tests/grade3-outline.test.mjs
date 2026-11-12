import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {validateOutline,skillId} from '../src/outline-template.js';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const c=JSON.parse(read('course-outlines/grade3.json'));
test('Grade 3 outline retains eight units and source order',()=>{
 assert.equal(c.id,'math3');assert.equal(c.source.pages,14);assert.equal(validateOutline(c).units,8);
 assert.deepEqual(c.units.map(u=>u.name),[
 'Foundation of Multiplication, Division, and Area',
 'Addition and Subtraction / Measurement',
 'Equal Partitioning and Naming Fractions',
 'Multiplication and Division',
 'Equivalence and Comparing Fractions and Measurement / Data',
 'Multiplication, Division, and Area',
 'Geometry and Measurement',
 'Demonstrate Computational Fluency in Problem Solving']);
 assert.deepEqual(c.units.map(u=>u.sourceMonth),['September–October','October–November','November–December','January','February–March','March–April','April–May','May–June']);
});
test('Grade 3 standards, skills, and questions are integrated',()=>{
 assert.ok(c.units.every(u=>u.status==='outline'&&u.skills.length>=5&&u.standards.length>=3&&u.guidingQuestions.length>=2));
 assert.ok(c.units.every(u=>u.standards.every(code=>c.standards[code])));
 assert.ok(c.units.every(u=>u.skills.every((s,i)=>skillId(u.id,i)===u.id+'-skill-'+String(i+1).padStart(2,'0'))));
 assert.equal(c.units[0].standards.includes('2.G.2'),true);
 assert.equal(c.units[4].standards.includes('3.NF.3'),true);
});
test('New Grade 3 page and all other courses link to one another',()=>{
 const html=read('grade3.html'),boot=read('src/grade3-site.js'),renderer=read('src/outline-template.js');
 assert.ok(html.includes('src/grade3-site.js'));assert.ok(boot.includes('course-outlines/grade3.json'));
 assert.ok(renderer.includes('guidingQuestions'));assert.ok(renderer.includes('Questions coming soon'));
 for(const path of ['grade1.html','grade2.html','grade4.html'])assert.ok(read(path).includes('href="grade3.html"'));
 assert.ok(!read('index.html').includes('href="grade3.html"'),'Unfinished Grade 3 must stay off the staging homepage');
 assert.ok(!read('grade5.html').includes('href="grade3.html"'),'Grade 5 picker should not advertise unfinished Grade 3');
 assert.ok(existsSync(new URL('../styles.css',import.meta.url)));
});
