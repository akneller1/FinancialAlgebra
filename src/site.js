import {course,getUnit} from './course.js';

const main=document.getElementById('main');
const search=document.getElementById('q');
const back=document.getElementById('backBtn');
const courseId=course.id;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const titleFor=(unit)=>'Unit '+(course.units.indexOf(unit)+1)+': '+unit.name;
const linkFor=(unit)=>'#'+courseId+'.'+unit.id;
const isPilot=(u)=>u.status==='pilot';
function art(){
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
 return '<nav class="crumbs" aria-label="Breadcrumb"><ol>'+items.map((item,i)=>
 '<li>'+(i===items.length-1?'<span aria-current="page">'+esc(item[0])+'</span>':'<a href="'+item[1]+'">'+esc(item[0])+'</a>')+'</li>').join('')+'</ol></nav>';
}
function band(inner,withArt=false){
 return '<section class="band" data-color="purple" data-course="'+courseId+'"><div class="wrap">'+
 (withArt?'<div class="band-grid"><div>'+inner+'</div><div class="band-art">'+art()+'</div></div>':inner)+
 '</div></section>';
}
function skillList(u){
 const n=4;
 const list=x=>'<ul class="unit-skills">'+x.map(s=>'<li class="unit-skill">'+esc(s)+'</li>').join('')+'</ul>';
 return list(u.skills.slice(0,n))+(u.skills.length>n?
 '<details class="unit-lesson-details"><summary><span>Show all '+u.skills.length+' lessons</span></summary>'+list(u.skills.slice(n))+'</details>':'');
}
function unitCard(u,i){
 return '<li><div class="unit algebra-unit-card" data-color="purple" data-course="'+courseId+'"><h3>'+
 '<a class="unit-title-link" href="'+linkFor(u)+'"><span class="unit-num">Unit '+(i+1)+'</span>'+esc(u.name)+'</a></h3>'+
 '<div class="unit-meta" data-lesson-list="true">'+skillList(u)+'</div>'+
 '<span class="unit-course-status">'+(isPilot(u)?'Interactive pilot available':'Development planned')+'</span>'+
 '<a class="unit-open-link" href="'+linkFor(u)+'">Open unit →</a></div></li>';
}
function filteredUnits(){
 const q=search.value.trim().toLocaleLowerCase();
 return course.units.filter(u=>!q||(u.name+' '+u.skills.join(' ')).toLocaleLowerCase().includes(q));
}
function courseView(){
 const filtered=filteredUnits();
 const lead=crumbs([['Home','#'],[course.name,null]])+
 '<h1 tabindex="-1">'+esc(course.name)+'</h1>'+
 '<p class="band-blurb">Apply algebra to income, budgeting, banking, borrowing, investing, and everyday financial choices.</p>'+
 '<p class="band-meta">10 units with lessons, financial scenarios, generators, games, and interactive investigations planned · 3 units in pilot development</p>';
 const intro=band(lead,true);
 const cards=filtered.map(u=>unitCard(u,course.units.indexOf(u))).join('');
 return intro+
 '<section class="section"><div class="wrap">'+
 '<h2 class="course-units-title">Browse by unit</h2>'+
 '<p class="course-units-status">Same unit cards and expandable lesson lists as Mr. K’s Classroom. Units marked as planned do not yet have functional resources.</p>'+
 (cards?'<ul class="units">'+cards+'</ul>':
 '<div class="empty"><h2>No matching units</h2><p>Try searching a different financial topic.</p></div>')+
 '</div></section>';
}
const options=[
 {label:'Lesson Plan',icon:'▤',status:'planned'},
 {label:'Worksheet',icon:'≡',status:'live',url:'lab'},
 {label:'Activity',icon:'✦',status:'planned'},
 {label:'Assessment',icon:'☑',status:'planned'},
 {label:'Games',icon:'◈',status:'planned'},
 {label:'Study Guides',icon:'▤',status:'live',url:'lab'},
 {label:'Interactive Math',icon:'⟡',status:'live',url:'lab'}
];
function shortcutBanner(u){
 return '<div class="generator-banner compact"><div class="generator-banner-heading"><h2>Create Resources for This Unit</h2></div>'+
 '<ul class="generator-shortcuts">'+options.map(o=>{
   const active=isPilot(u)&&o.status==='live';
   const tag=active?'a':'span',attr=active?'href="lab.html#'+u.id+'"':'aria-disabled="true" title="Not built yet"';
   const subtitle=active?'':'<small class="build-badge">Coming soon</small>';
   return '<li><'+tag+' class="generator-shortcut'+(o.url==='lab'?' resource-shortcut':'')+'" '+attr+'>'+
   '<span class="generator-shortcut-icon" aria-hidden="true">'+o.icon+'</span>'+
   '<span class="generator-shortcut-copy"><strong>'+o.label+'</strong>'+subtitle+'</span></'+tag+'></li>';
 }).join('')+'</ul></div>';
}
function thumb(kind){
 const shapes={
  budget:'<rect x="24" y="28" width="106" height="13" rx="6" fill="#5d7bc2"/><rect x="24" y="53" width="162" height="12" rx="6" fill="#68ad9f"/><rect x="24" y="76" width="82" height="12" rx="6" fill="#d89f75"/><rect x="24" y="101" width="139" height="12" rx="6" fill="#ab92d4"/>',
  credit:'<path d="M18 30h175v94H18z" rx="12" fill="#f7fafc" stroke="#6474a2" stroke-width="3"/><path d="M37 49h130M37 68h110" stroke="#bfcee5" stroke-width="9" stroke-linecap="round"/><path d="M40 104l38-12 29 5 38-24 26 3" stroke="#a27cc7" stroke-width="5" stroke-linecap="round" fill="none"/>',
  investing:'<path d="M24 112h159M24 30v82" stroke="#7185a2" stroke-width="4"/><path d="M34 104l28-16 24 5 26-30 26 10 39-46" stroke="#319a89" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 104l28-16 24 5 26-30 26 10 39-46v79H34z" fill="#80cdb9" opacity=".23"/>'
 };
 return '<svg class="lab-thumb" viewBox="0 0 210 138" role="img" aria-label="Financial data illustration" xmlns="http://www.w3.org/2000/svg">'+
 '<rect width="210" height="138" rx="12" fill="#f0f4ff"/>'+
 (shapes[kind]||shapes.budget)+'</svg>';
}
function resourceCard(u,{title,desc,kind,url,button='Open activity'}){
 return '<li class="card lab-card" data-color="purple" data-course="'+courseId+'">'+
 '<a class="thumb" href="'+esc(url)+'" tabindex="-1" aria-hidden="true">'+thumb(kind)+'</a>'+
 '<div class="card-body"><p class="development-pill">Working pilot</p>'+
 '<h3><a href="'+esc(url)+'">'+esc(title)+'</a></h3>'+
 '<p class="desc">'+esc(desc)+'</p>'+
 '<div class="actions"><a class="btn btn-open" href="'+esc(url)+'">'+esc(button)+'</a></div></div></li>';
}
function cardSection(title,cards){
 return '<section class="algebra-unit-section"><h2>'+esc(title)+'</h2><ul class="cards grouped-cards">'+cards.join('')+'</ul></section>';
}
function pager(u){
 const i=course.units.indexOf(u);
 const item=(unit,dir)=>unit?'<a class="pager-link pager-'+dir+'" href="'+linkFor(unit)+'" rel="'+dir+'">'+
 (dir==='prev'?'<span class="pager-arrow" aria-hidden="true">←</span>':'')+
 '<span class="pager-text"><span class="pager-dir">'+(dir==='prev'?'Previous unit':'Next unit')+'</span><span class="pager-name">'+esc(titleFor(unit))+'</span></span>'+
 (dir==='next'?'<span class="pager-arrow" aria-hidden="true">→</span>':'')+'</a>':'<span class="pager-spot"></span>';
 return '<nav class="unit-pager" data-color="purple" data-course="'+courseId+'" aria-label="Unit navigation">'+item(course.units[i-1],'prev')+item(course.units[i+1],'next')+'</nav>';
}
function unitView(u){
 const lead=crumbs([['Home','#'],[course.name,'#'],[titleFor(u),null]])+
 '<h1 tabindex="-1">'+esc(titleFor(u))+'</h1>'+
 '<p class="band-meta">'+(isPilot(u)?'Create custom practice resources or explore interactive financial mathematics for this unit.':'Course outline · Activities coming soon')+'</p>';
 let body=pager(u);
 if(isPilot(u)){
   const url='lab.html#'+u.id,worksheet='lab.html?print=worksheet&unit='+u.id+'&level=cp1';
   const key='lab.html?print=key&unit='+u.id+'&level=cp1';
   body+=shortcutBanner(u);
   body+=cardSection('Study Guides',[resourceCard(u,{
      title:'Financial Math Practice',kind:u.id==='budgeting'?'budget':u.id==='credit'?'credit':'investing',
      desc:'Generated CP2, CP1, and Honors questions with worked solutions and immediate feedback.',
      url,button:'Practice'} )]);
   body+=cardSection('Interactive Math',[resourceCard(u,{
      title:(u.id==='budgeting'?'Budget Builder':u.id==='credit'?'Debt Repayment Explorer':'Compound Growth Explorer'),kind:u.id==='budgeting'?'budget':u.id==='credit'?'credit':'investing',
      desc:'Adjust realistic financial assumptions to observe their mathematical consequences.',
      url,button:'Explore'} )]);
   body+=cardSection('Practice Activities',[resourceCard(u,{
      title:'Printable Financial Algebra Worksheet',kind:u.id==='budgeting'?'budget':u.id==='credit'?'credit':'investing',
      desc:'Six parameterized practice questions, with a separate teacher key. Opens the CP1 worksheet; the lab supports all difficulty levels.',
      url:worksheet,button:'Open printable'} )]);
   body+='<p class="unit-notes"><a href="'+key+'">Open the CP1 teacher answer key →</a> · Games, full lesson plans, activity generators, and assessments are not yet implemented.</p>';
 }else{
   body+='<section class="algebra-unit-section"><h2>Topics in this unit</h2>'+
   '<ul class="unit-skills">'+u.skills.map(s=>'<li class="unit-skill">'+esc(s)+'</li>').join('')+'</ul>'+
   '<div class="empty"><h2>Activities coming soon</h2><p>These lessons, games, and practice resources have not yet been built. Try one of the three working pilot units.</p></div></section>';
 }
 body+=pager(u);
 return band(lead) + '<section class="section"><div class="wrap algebra-unit-layout">'+body+'</div></section>';
}
function routeUnit(){
 const slug=decodeURIComponent(location.hash.slice(1));
 const prefix=courseId+'.';
 return slug.startsWith(prefix)?getUnit(slug.slice(prefix.length)):null;
}
function render(){
 const u=routeUnit();
 main.innerHTML=u?unitView(u):courseView();
 const heading=main.querySelector('h1');
 document.title=(u?titleFor(u)+' | ':'')+'Financial Algebra | Mr. K’s Classroom';
 back.style.visibility=u?'visible':'hidden';
 search.style.visibility=u?'hidden':'visible';
 if(heading) heading.setAttribute('tabindex','-1');
}
document.getElementById('backBtn').addEventListener('click',()=>{location.hash='';render();window.scrollTo(0,0)});
document.getElementById('skip').addEventListener('click',()=>main.focus());
document.getElementById('searchForm').addEventListener('submit',e=>{e.preventDefault();location.hash='';render();main.focus();});
search.addEventListener('input',()=>{if(!routeUnit())render();});
window.addEventListener('hashchange',()=>{render();window.scrollTo(0,0)});
render();
