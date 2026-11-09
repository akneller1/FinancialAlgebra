import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
test('standalone course and units reuse actual classroom course-page design',()=>{
 const shell=read('index.html'),site=read('src/site.js'),css=read('styles.css');
 for(const name of ['site-header','brand','band','algebra-unit-card','generator-banner','algebra-unit-section','grouped-cards','unit-pager']){
  assert.ok(site.includes(name)||shell.includes(name),'Missing classroom component '+name);
  assert.ok(css.includes(name),'Missing original classroom styling '+name);
 }
});
test('single-level worksheets, practice and labs are actually linked',()=>{
 const site=read('src/site.js'),course=read('src/course.js'),questions=read('src/questions.js');
 assert.ok(course.includes("levels: ['standard']"));
 assert.ok(!questions.includes('cp2')&&!questions.includes('cp1')&&!questions.includes('honors'));
 assert.ok(site.includes("worksheet.html?unit="));
 assert.ok(site.includes("practice.html?unit="));
 assert.ok(site.includes("interactiveUrl(u)"));
 assert.ok(!site.includes("lab.html#"));
 for(const file of ['practice.html','worksheet.html','print.html','lab.html',
  'src/practice.js','src/worksheet.js','src/print.js','src/finance-lab.js',
  'artifacts/interactive-math/lab.css','artifacts/interactive-math/lab.js',
  'artifacts/financial-algebra-budgeting-explorer/index.html',
  'artifacts/financial-algebra-credit-explorer/index.html',
  'artifacts/financial-algebra-investing-explorer/index.html'])
  assert.ok(existsSync(new URL('../'+file,import.meta.url)),'Missing '+file);
});
test('pilot math labs reuse actual Classroom Lab.layout and challenges framework',()=>{
 const core=read('artifacts/interactive-math/lab.js'),lab=read('src/finance-lab.js');
 assert.ok(core.includes('function layout('));
 assert.ok(core.includes('function challenges('));
 for(const name of ['L.layout','L.slider','L.challenges','L.table','L.graph'])assert.ok(lab.includes(name));
});
