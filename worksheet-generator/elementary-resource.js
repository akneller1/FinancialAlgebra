/* Open an outline's resources with the established Grade 5 engines, never its banks. */
import {validateOutline} from '../src/outline-template.js?v=preload-20261112';
const params = new URLSearchParams(location.search);
const id = params.get('course'), tool = params.get('tool');
const tools = {
 games:['g5-core.js','g5-games.js'],
 flashcards:['g5-core.js','flashcards.js'],
 check:['g5-core.js','understanding-check.js'],
 generators:['generators-content.js','generators-core.js','generators-pagination.js','generators-render.js','generators.js']
};
function script(src) {
 return new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=src+'?v=elementary-preload-20261112';s.onload=resolve;s.onerror=()=>reject(Error('Could not load resource controls. Please refresh.'));document.body.append(s);});
}
async function boot() {
 if (!/^math[1-4]$/.test(id||'') || !tools[tool]) throw Error('Choose a course and resource from its unit page.');
 const response = await fetch('../course-outlines/grade'+id.slice(4)+'.json');
 if (!response.ok) throw Error('The course outline could not load.');
 const course = await response.json(); validateOutline(course);
 if (course.id !== id) throw Error('Course outline mismatch.');
 const unit = course.units.find(u=>u.id===params.get('unit'));
 if (!unit) throw Error('Choose a unit from this course.');
 window.MK_ELEMENTARY_COURSE = course;
 window.LIBRARY = {courses:[course]};
 window.MK_COURSE_CATALOG = {getSkillRecords(courseId,unitId) {
  if (courseId !== id) return [];
  const u=course.units.find(u=>u.id===unitId);
  return (u?.skills||[]).map((name,i)=>({id:unitId+'-skill-'+String(i+1).padStart(2,'0'),name,index:i+1}));
 }};
 const back='../grade'+id.slice(4)+'.html#'+id+'.'+unit.id;
 const home=document.querySelector('.g5-home');home.href=back;home.textContent='← '+course.shortName;
 document.title=course.shortName+' · '+unit.name;
 document.querySelector('.g5-title strong').textContent=course.shortName+' Resources';
 document.querySelectorAll('[data-tool]').forEach(a=>{
  const p=new URLSearchParams({course:id,unit:unit.id,tool:a.dataset.tool});a.href='elementary-resource.html?'+p;
 });
 document.querySelector('body > .g5-top').hidden=tool!=='generators';
 document.querySelector('.g5gen-skip').hidden=tool!=='generators';
 document.getElementById('app').hidden=tool==='generators';
 document.querySelector('.g5gen-app').hidden=tool!=='generators';
 // Scoped preference storage and content: never borrow a Grade 5 unit with the same slug.
 for (const src of ['../question-bank-adapter.js','../question-bank-loader.js','core/math-display.js',...(tool==='generators'?[]:['games/skill-setup.js'])]) await script(src);
 for (const file of tools[tool]) {
  await script('grade5/'+file);
  if (file==='generators-content.js') window.G5_GENERATOR_CONTENT.units={};
 }
}
boot().catch(error=>{
 document.querySelector('.g5gen-app').hidden=true;
 const main=document.getElementById('app');main.hidden=false;main.replaceChildren();
 const box=document.createElement('section');box.className='g5-panel';
 const h=document.createElement('h1');h.textContent='Resource unavailable';
 const p=document.createElement('p');p.textContent=error.message;box.append(h,p);main.append(box);
});
