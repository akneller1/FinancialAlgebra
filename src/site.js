import {course,getUnit} from './course.js';
import {resourceThumbnail,resourceHref} from '../financial/lib/resource-previews.mjs?v=student-work-1';

// Unit resources share one manifest with the library hub and content validation.
const response=await fetch(new URL('../financial/resources.json?v=student-work-1',import.meta.url));
if(!response.ok) throw new Error('Unable to load Financial Algebra resources');
const library=await response.json();
const resourcesFor=unit=>library.units.find(record=>record.unitId===unit.id).resources;
const main=document.getElementById('main');
const search=document.getElementById('q');
const back=document.getElementById('backBtn');
const courseId=course.id;
const esc=value=>String(value).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const titleFor=unit=>'Unit '+(course.units.indexOf(unit)+1)+': '+unit.name;
const linkFor=unit=>'#'+courseId+'.'+unit.id;

function artwork(){
 return '<svg class="finance-art" viewBox="0 0 230 195" xmlns="http://www.w3.org/2000/svg" fill="none" aria-hidden="true">'+
 '<rect x="30" y="53" width="176" height="115" rx="13" stroke="currentColor" stroke-width="5"/>'+
 '<rect x="46" y="72" width="76" height="14" rx="7" fill="currentColor" opacity=".24"/>'+
 '<path d="M49 143h123M49 124l30-22 24 13 29-31 30 12" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'+
 '<circle cx="179" cy="54" r="32" fill="#fff" stroke="currentColor" stroke-width="5"/>'+
 '<path d="M180 36v37M191 42c-16-11-26 2-20 10 6 8 25 5 22 15-4 13-23 11-30 2" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>'+
 '<circle cx="27" cy="164" r="19" fill="#fff" stroke="currentColor" stroke-width="4"/>'+
 '<path d="M18 164h19M27 155v18" stroke="currentColor" stroke-width="3"/>'+
 '</svg>';
}
function crumbs(items){
 return '<nav class="crumbs" aria-label="Breadcrumb"><ol>'+
 items.map((item,i)=>'<li>'+(i===items.length-1?'<span aria-current="page">'+esc(item[0])+'</span>':'<a href="'+esc(item[1])+'">'+esc(item[0])+'</a>')+'</li>').join('')+'</ol></nav>';
}
function band(content,withArtwork=false){
 return '<section class="band" data-color="purple" data-course="'+courseId+'"><div class="wrap">'+
 (withArtwork?'<div class="band-grid"><div>'+content+'</div><div class="band-art">'+artwork()+'</div></div>':content)+'</div></section>';
}
function skillList(unit){
 const list=items=>'<ul class="unit-skills">'+items.map(skill=>'<li class="unit-skill">'+esc(skill)+'</li>').join('')+'</ul>';
 const first=unit.skills.slice(0,4);
 const extra=unit.skills.slice(4);
 return list(first)+(extra.length?
  '<details class="unit-lesson-details"><summary>Show all '+unit.skills.length+' topics</summary>'+list(extra)+'</details>':'');
}
function unitCard(unit,index){
 return '<li><div class="unit algebra-unit-card" data-color="purple" data-course="'+courseId+'">'+
 '<h3><a class="unit-title-link" href="'+linkFor(unit)+'"><span class="unit-num">Unit '+(index+1)+'</span>'+esc(unit.name)+'</a></h3>'+
 '<div class="unit-meta" data-lesson-list="true">'+skillList(unit)+'</div>'+
 '<span class="unit-course-status">Generators · Games · Decision Lab · Study Guides · Projects</span>'+
 '<a class="unit-open-link" href="'+linkFor(unit)+'">Open unit →</a></div></li>';
}
const shortcuts=[
 ['Lesson Plan','▤','lessonPlan'],['Worksheet','≡','worksheet'],['Assessment','☑','assessment'],
 ['Decision Lab','⟡','decisionLab'],['Practice Test','✓','practiceTest'],['Flashcards','▤','flashcards'],['Cheat Sheet','▧','cheatSheet']
];
function shortcutBanner(unit){
 const resources=resourcesFor(unit);
 return '<section class="generator-banner compact"><div class="generator-banner-heading"><h2>Create Resources for This Unit</h2></div>'+
 '<ul class="generator-shortcuts">'+shortcuts.map(([name,icon,key])=>
 '<li><a class="generator-shortcut" href="'+esc(resourceHref(key==='decisionLab'?resources[key].path:resources[key]))+'">'+
 '<span class="generator-shortcut-icon" aria-hidden="true">'+icon+'</span>'+
 '<span class="generator-shortcut-copy"><strong>'+name+'</strong></span></a></li>').join('')+
 '</ul></section>';
}
function resourceCard(title,path,description,unit){
 const href=esc(resourceHref(path));
 const thumbnail=esc(resourceThumbnail(path,unit.id));
 const studentLink=/financial\/(games|decision-lab|flashcards|practice)\//.test(path)&&!/[?&]teacher=1/.test(path);
 return '<li class="finance-resource-item"><article class="finance-resource-card" data-course="'+esc(courseId)+'" data-color="purple">'+
  '<a class="finance-resource-image-link" href="'+href+'" aria-label="Open '+esc(title)+'"><img class="finance-resource-thumb" src="'+thumbnail+'" width="720" height="450" alt="" loading="lazy" decoding="async"></a>'+
  '<div class="finance-resource-body"><h3><a class="finance-resource-title" href="'+href+'">'+esc(title)+'</a></h3>'+
  '<p class="finance-resource-description">'+esc(description)+'</p>'+
  '<div class="finance-resource-actions"><a class="finance-resource-open" href="'+href+'">Open resource →</a>'+
  (studentLink?'<button type="button" class="finance-student-link" data-student-link="'+esc(path)+'">Generate student link</button>':'')+
  '</div></div></article></li>';
}
function resourceSections(unit){
 const r=resourcesFor(unit);
 return '<section class="algebra-unit-section"><h2>Generators</h2><ul class="finance-resource-grid">'+
 resourceCard('Lesson Plan',r.lessonPlan,'Build notes, examples, practice and an exit ticket.',unit)+
 resourceCard('Worksheet',r.worksheet,'Choose skills and create practice with an answer key.',unit)+
 resourceCard('Assessment',r.assessment,'Create a unit assessment with worked solutions.',unit)+'</ul></section>'+
 '<section class="algebra-unit-section" id="games"><h2>Games</h2><p>Play with financial vocabulary, concepts, calculations, and real-life choices. Standard level.</p><ul class="finance-resource-grid">'+
 r.games.map(g=>resourceCard(g.title,g.path,g.description,unit)).join('')+'</ul></section>'+
 '<section class="algebra-unit-section"><h2>Decision Lab</h2><p>Compare real-life choices, explore assumptions, and explain your decision.</p><ul class="finance-resource-grid">'+
 resourceCard(r.decisionLab.title,r.decisionLab.path,'A guided seven-step investigation with a printable summary.',unit)+
 resourceCard('Teacher guide',r.decisionLab.teacherPath,'Teaching prompts, model reasoning, and discussion guidance.',unit)+'</ul></section>'+
 '<section class="algebra-unit-section"><h2>Study Guides</h2><ul class="finance-resource-grid">'+
 resourceCard('Flashcards',r.flashcards,'Study financial vocabulary, formulas, and principles.',unit)+
 resourceCard('Cheat Sheet',r.cheatSheet,'A two-page printable reference.',unit)+
 resourceCard('Practice Test',r.practiceTest,'Check understanding with explanations and model responses.',unit)+'</ul></section>'+
 '<section class="algebra-unit-section"><h2>Projects</h2><ul class="finance-resource-grid">'+
 r.projects.map(p=>resourceCard(p.title,p.path,p.grouping+' · '+p.days+' · Student packet, slides, teacher guide, and rubric',unit)).join('')+'</ul></section>';
}
function pager(unit){
 const i=course.units.indexOf(unit);
 const link=(u,dir)=>u?'<a class="pager-link pager-'+dir+'" href="'+linkFor(u)+'" rel="'+dir+'">'+
 (dir==='prev'?'<span class="pager-arrow" aria-hidden="true">←</span>':'')+
 '<span class="pager-text"><span class="pager-dir">'+(dir==='prev'?'Previous unit':'Next unit')+
 '</span><span class="pager-name">'+esc(titleFor(u))+'</span></span>'+
 (dir==='next'?'<span class="pager-arrow" aria-hidden="true">→</span>':'')+'</a>':'<span class="pager-spot"></span>';
 return '<nav class="unit-pager" data-color="purple" data-course="'+courseId+'" aria-label="Unit navigation">'+
 link(course.units[i-1],'prev')+link(course.units[i+1],'next')+'</nav>';
}
function courseView(){
 const term=search.value.trim().toLocaleLowerCase();
 const shown=course.units.filter(unit=>!term||(unit.name+' '+unit.skills.join(' ')).toLocaleLowerCase().includes(term));
 const lead=crumbs([['Home','#'],[course.name,null]])+
 '<h1 tabindex="-1">'+esc(course.name)+'</h1>'+
 '<p class="band-blurb">Apply algebra to income, budgeting, banking, borrowing, investing, and everyday financial choices.</p>'+
 '<p class="band-meta">'+course.units.length+' units · 40 skills · one course level: Standard</p>';
 return band(lead,true)+'<section class="section"><div class="wrap">'+
 '<h2 class="course-units-title">Browse by unit</h2>'+
 '<p class="course-units-status">Explore lesson plans, worksheets, assessments, games, Decision Labs, study guides, and projects. All scenarios use fictional financial information and illustrative rates.</p>'+
 (shown.length?'<ul class="units">'+shown.map(unit=>unitCard(unit,course.units.indexOf(unit))).join('')+'</ul>':
 '<div class="empty"><h2>No matching units</h2><p>Try another financial topic.</p></div>')+
 '</div></section>';
}
function unitView(unit){
 const lead=crumbs([['Home','#'],[course.name,'#'],[titleFor(unit),null]])+
 '<h1 tabindex="-1">'+esc(titleFor(unit))+'</h1>'+
 '<p class="band-meta">Standard · financial concepts · real-life decisions</p>';
 const body=pager(unit)+shortcutBanner(unit)+
 '<section class="algebra-unit-section"><h2>Topics in this unit</h2>'+
 '<ul class="unit-skills">'+unit.skills.map(skill=>'<li class="unit-skill">'+esc(skill)+'</li>').join('')+'</ul>'+
 '</section>'+resourceSections(unit)+pager(unit);
 return band(lead)+'<section class="section"><div class="wrap algebra-unit-layout">'+body+'</div></section>';
}
function currentUnit(){
 const slug=decodeURIComponent(location.hash.slice(1));
 return slug.startsWith(courseId+'.')?getUnit(slug.slice(courseId.length+1)):null;
}
function render(){
 const unit=currentUnit();
 main.innerHTML=unit?unitView(unit):courseView();
 document.title=(unit?titleFor(unit)+' | ':'')+'Financial Algebra | Mr. K’s Classroom';
 back.style.visibility=unit?'visible':'hidden';
 search.style.visibility=unit?'hidden':'visible';
}
back.addEventListener('click',()=>{location.hash='';render();window.scrollTo(0,0);});
document.getElementById('skip').addEventListener('click',()=>main.focus());
document.getElementById('searchForm').addEventListener('submit',event=>{event.preventDefault();location.hash='';render();main.focus();});
search.addEventListener('input',()=>{if(!currentUnit())render();});
window.addEventListener('hashchange',()=>{render();window.scrollTo(0,0);});
render();


main.addEventListener('click',async event=>{
 const button=event.target.closest('[data-student-link]');if(!button)return;
 const url=new URL(button.dataset.studentLink,location.href);url.searchParams.delete('teacher');url.searchParams.delete('teacherShare');url.searchParams.set('student','1');
 try{await navigator.clipboard.writeText(url.href);button.textContent='Student link copied!';}catch{window.prompt('Copy student link:',url.href);}
});
