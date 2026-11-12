import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';

const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
const exists=path=>existsSync(new URL('../'+path,import.meta.url));

test('Financial Algebra connects the complete resource library with the Classroom design',()=>{
 const site=read('src/site.js'),index=read('index.html'),css=read('styles.css');
 for(const className of ['site-header','band','algebra-unit-card','generator-banner','algebra-unit-section','unit-pager']){
  assert.ok(index.includes(className)||site.includes(className),'Missing course style '+className);
  assert.ok(css.includes(className),'Original style missing '+className);
 }
 assert.ok(site.includes('resourcesFor(unit)'));
 assert.ok(site.includes('resourceSections(unit)'));
 assert.ok(site.includes('financial/resources.json'));
 assert.equal(site.includes('aria-disabled="true"'),false);
 assert.equal(site.includes('Activities coming soon'),false);
 for(const forbidden of ['Interactive pilot available','href="lab.html','worksheet.html?unit=','practice.html?unit=','financial-algebra-budgeting-explorer']){
  assert.equal(site.includes(forbidden),false,'Unwanted activity link remains: '+forbidden);
 }
 for(const path of ['worksheet.html','practice.html','print.html','lab.html',
 'src/finance-lab.js','src/questions.js','src/engine.js',
 'artifacts/financial-algebra-budgeting-explorer/index.html',
 'artifacts/financial-algebra-credit-explorer/index.html',
 'artifacts/financial-algebra-investing-explorer/index.html']){
  assert.equal(exists(path),false,'Unused pilot file remains: '+path);
 }
});
test('All Grades 1–5 have their own SVG icons and nav references',()=>{
 const renderer=read('src/outline-template.js');
 // Grades 1–4 remain development outlines: their own pages retain the
 // icon navigation, while the Financial Algebra and finished Grade 5
 // navigation deliberately does not advertise unfinished courses.
 const navPages=Array.from({length:4},(_,i)=>'grade'+(i+1)+'.html');
 assert.ok(read('index.html').includes('href="grade5.html"'));
 for(const page of ['index.html','grade5.html']){
  for(let n=1;n<=4;n++){
   assert.ok(!read(page).includes('href="grade'+n+'.html"'),page+' publicly advertises unfinished Grade '+n);
  }
 }
 const iconContents=[];
 for(let n=1;n<=5;n++){
  const iconPath='assets/course-icons/grade'+n+'.svg';
  assert.ok(exists(iconPath));
  const icon=read(iconPath);
  assert.match(icon,/^<svg/);
  assert.ok(icon.includes('Grade '+n));
  assert.ok(icon.includes('viewBox="0 0 230 195"'));
  iconContents.push(icon);
  for(const page of navPages){
   assert.ok(read(page).includes('src="./assets/course-icons/grade'+n+'.svg"'),page+' missing icon '+n);
  }
 }
 assert.equal(new Set(iconContents).size,5);
 assert.ok(renderer.includes('function artwork()'));
 assert.ok(renderer.includes('assets/course-icons/grade'));
 assert.ok(renderer.includes("return band(lead,true,'course')"));
 assert.ok(renderer.includes('unit-band'), 'Outline unit pages should retain compact unit headers');
 assert.ok(renderer.includes('course-band'), 'Course overviews should use matching compact headers');
});
