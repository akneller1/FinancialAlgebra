/* Reusable course-outline renderer for new classes.
   Data is supplied as JSON; no questions, activities, or unsupported links are fabricated. */
export function skillId(unitId,index){return unitId+'-skill-'+String(index+1).padStart(2,'0');}
export function outlineStats(course){
 return {units:course.units.length,skills:course.units.reduce((n,u)=>n+u.skills.length,0)};
}
export function validateOutline(course){
 if(!course || typeof course.id!=='string' || !Array.isArray(course.units)) throw Error('Invalid course outline');
 const seen=new Set();
 for(const u of course.units){
  if(!u.id||seen.has(u.id)||!Array.isArray(u.skills)||!Array.isArray(u.standards))throw Error('Invalid or duplicate unit '+u.id);
  seen.add(u.id);
  for(const code of u.standards)if(!course.standards?.[code])throw Error('Unmapped standard '+code);
 }
 return outlineStats(course);
}
export function mountOutline(course,{page='grade5.html'}={}){
 const stats=validateOutline(course);
 const hasObjectives=Boolean(course.units.some(u=>Array.isArray(u.objectiveGroups)&&u.objectiveGroups.length));
 const targetLabel=hasObjectives?'learning targets':'lessons';
 const hasPacing=course.units.some(u=>Number.isFinite(u.estimatedDays));
 const pacingLow=course.units.reduce((n,u)=>n+(u.estimatedDays||0),0);
 const pacingHigh=course.units.reduce((n,u)=>n+(u.estimatedDaysMax||u.estimatedDays||0),0);
 const paceLabel=(low,high)=>String(low)+(high&&high!==low?'–'+high:'');
 const main=document.getElementById('main');
 const search=document.getElementById('q');
 const back=document.getElementById('backBtn');
 if(!main||!search||!back)throw Error('Missing classroom page shell');
 const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const num=u=>course.units.indexOf(u)+1;
 const title=u=>'Unit '+num(u)+': '+u.name;
 const href=u=>'#'+course.id+'.'+u.id;
 const anchor=(text,link)=>link?'<a href="'+link+'">'+esc(text)+'</a>':'<span aria-current="page">'+esc(text)+'</span>';
 const crumb=links=>'<nav class="crumbs" aria-label="Breadcrumb"><ol>'+
 links.map(([text,link])=>'<li>'+anchor(text,link)+'</li>').join('')+'</ol></nav>';
 function artwork(){
  const match=/^math([1-5])$/.exec(course.id);
  if(!match)return '';
  const grade=match[1];
  const motifs={'1':'counting beads','2':'base-ten blocks','3':'multiplication array','4':'geometric shapes','5':'fraction circle'};
  return '<img class="outline-art" src="./assets/course-icons/grade'+grade+'.svg" alt="Grade '+grade+' '+motifs[grade]+' icon" width="230" height="195">';
 }
 function band(contents,art=false){
  return '<section class="band" data-course="'+course.id+'" data-color="purple"><div class="wrap">'+
   (art?'<div class="band-grid"><div>'+contents+'</div><div class="band-art">'+artwork()+'</div></div>':contents)+'</div></section>';
 }
 function skillsCompact(u){
  function list(xs){return '<ul class="unit-skills">'+xs.map(s=>'<li class="unit-skill">'+esc(s)+'</li>').join('')+'</ul>';}
  return list(u.skills.slice(0,4))+(u.skills.length>4?'<details class="unit-lesson-details"><summary>'+
  '<span class="show-label">Show all '+u.skills.length+' '+targetLabel+'</span><span class="hide-label">Show fewer '+targetLabel+'</span>'+
  '</summary>'+list(u.skills.slice(4))+'</details>':'');
 }
 function card(u){
  return '<li><div class="unit algebra-unit-card" data-color="purple" data-course="'+course.id+'">'+
   '<h3><a class="unit-title-link" href="'+href(u)+'"><span class="unit-num">Unit '+num(u)+'</span>'+esc(u.name)+'</a></h3>'+
   '<div class="unit-meta" data-lesson-list="true">'+skillsCompact(u)+'</div>'+
   '<span class="unit-course-status">Question banks coming soon</span>'+
   '<a class="unit-open-link" href="'+href(u)+'">Open unit →</a></div></li>';
 }
 const actions=[
  ['Lesson Plan','▤'],['Worksheet','≡'],['Activity','✦'],['Assessment','☑'],
  ['Games','◈'],['Study Guides','▤'],['Interactive Math','⟡']
 ];
 function shortcuts(){
  return '<section class="generator-banner compact"><div class="generator-banner-heading"><h2>Create Resources for This Unit</h2></div>'+
   '<ul class="generator-shortcuts">'+actions.map(([name,icon])=>
   '<li><span class="generator-shortcut" aria-disabled="true" title="Question banks and activities have not been added">'+
   '<span class="generator-shortcut-icon" aria-hidden="true">'+icon+'</span>'+
   '<span class="generator-shortcut-copy"><strong>'+name+'</strong><small class="build-badge">Coming soon</small></span></span></li>').join('')+'</ul></section>';
 }
 function unitPager(u){
  const idx=course.units.indexOf(u);
  function link(v,d){
   if(!v)return '<span class="pager-spot"></span>';
   return '<a class="pager-link pager-'+d+'" href="'+href(v)+'" rel="'+d+'">'+
    (d==='prev'?'<span class="pager-arrow" aria-hidden="true">←</span>':'')+
    '<span class="pager-text"><span class="pager-dir">'+(d==='prev'?'Previous unit':'Next unit')+
    '</span><span class="pager-name">'+esc(title(v))+'</span></span>'+
    (d==='next'?'<span class="pager-arrow" aria-hidden="true">→</span>':'')+'</a>';
  }
  return '<nav class="unit-pager" data-color="purple" data-course="'+course.id+'" aria-label="Unit navigation">'+
   link(course.units[idx-1],'prev')+link(course.units[idx+1],'next')+'</nav>';
 }
 function standards(u){
  if(Array.isArray(u.sections)&&u.sections.length){
   return '<section class="algebra-unit-section outline-standards"><h2>Curriculum Sections &amp; Standards</h2>'+
   '<p class="course-skill-hint">Section headings and standard codes come from the cited scope and sequence. Skills within each section are paraphrased learning targets.</p>'+
   u.sections.map(sec=>'<details class="outline-standards-detail im-section"><summary><strong>Section '+esc(sec.letter)+': '+esc(sec.name)+'</strong> · '+sec.skills.length+' targets</summary>'+
   '<ul>'+sec.skills.map(skill=>'<li>'+esc(skill)+'</li>').join('')+'</ul>'+
   '<p class="outline-standard-codes"><strong>Standards:</strong> '+sec.standards.map(esc).join(', ')+'</p></details>').join('')+
   '<p class="outline-source">Source: <a target="_blank" rel="noopener" href="'+esc(course.source.url)+'">'+esc(course.source.title)+'</a> · Illustrative Mathematics, CC BY 4.0</p></section>';
  }
  if(Array.isArray(u.objectiveGroups)&&u.objectiveGroups.length){
   const n=u.objectiveGroups.reduce((total,g)=>total+g.items.length,0);
   return '<section class="algebra-unit-section outline-standards"><h2>Source Objectives by Category</h2>'+
   '<p class="course-skill-hint">The target labels above condense the source objectives; the original document does not give individual textbook lesson titles.</p>'+
   '<details class="outline-standards-detail"><summary>Show '+n+' source-based statements in '+u.objectiveGroups.length+' categories</summary>'+
   u.objectiveGroups.map(g=>'<section class="outline-objective-group"><h3>'+esc(g.category)+'</h3><ul>'+
   g.items.map(t=>'<li>'+esc(t)+'</li>').join('')+'</ul></section>').join('')+'</details>'+
   '<p class="outline-source">Source: '+esc(course.source.filename)+' · PDF page'+(u.sourcePages.length>1?'s ':' ')+u.sourcePages.join(', ')+'</p></section>';
  }
  return '<section class="algebra-unit-section outline-standards"><h2>Standards &amp; Eligible Content</h2>'+
   '<p class="course-skill-hint">References transcribed from the attached Grade 5 scope and sequence, not independently revised or remapped.</p>'+
   '<details class="outline-standards-detail"><summary>Show '+u.standards.length+' source references</summary>'+
   '<ul>'+u.standards.map(code=>'<li><strong>'+esc(code)+'</strong> — '+esc(course.standards[code])+'</li>').join('')+'</ul></details>'+
   '<p class="outline-source">Source: '+esc(course.source.filename)+' · page'+(u.sourcePages.length>1?'s ':' ')+u.sourcePages.join('–')+'</p></section>';
 }
 function unitPage(u){
  const lead=crumb([[course.name,page],[title(u),null]])+'<h1 tabindex="-1">'+esc(title(u))+'</h1>'+
   '<p class="band-meta">'+u.skills.length+' '+targetLabel+(Number.isFinite(u.estimatedDays)?' · '+paceLabel(u.estimatedDays,u.estimatedDaysMax)+' estimated instructional days':'')+(u.sourceMonth?' · '+esc(u.sourceMonth):'')+(u.reportedLessons?' · '+u.reportedLessons+' reported textbook lessons':'')+' · resources coming soon</p>';
  const lessonItems=u.skills.map((s,i)=>'<li class="outline-lesson" data-skill-id="'+skillId(u.id,i)+'">'+
   '<span class="outline-lesson-number">'+String(i+1).padStart(2,'0')+'</span><span>'+esc(s)+'</span></li>').join('');
  return band(lead,true)+'<section class="section"><div class="wrap algebra-unit-layout">'+
   unitPager(u)+shortcuts()+
   '<section class="algebra-unit-section"><h2>'+(hasObjectives?'Learning Targets & Subskills':'Lessons and Subskills')+'</h2>'+
   '<p class="course-skill-hint">'+(hasObjectives?'Source-based learning targets are editorial groupings; Individual lesson titles are not listed in the source; sections and learning targets are shown here.':'The lesson sequence follows the supplied curriculum.')+' Stable skill IDs are reserved for later question banks.</p>'+
   '<ol class="outline-lesson-list" data-course-id="'+course.id+'" data-unit-id="'+u.id+'">'+lessonItems+'</ol>'+
   (u.resourceNote?'<p class="outline-curriculum-note"><strong>Source resource note:</strong> '+esc(u.resourceNote)+'</p>':'')+'</section>'+
   standards(u)+
   (u.guidingQuestions?.length?'<section class="algebra-unit-section outline-guiding"><h2>Essential &amp; Guiding Questions</h2><ul>'+u.guidingQuestions.map(q=>'<li>'+esc(q)+'</li>').join('')+'</ul></section>':'')+
   '<section class="algebra-unit-section"><h2>Games, Study Guides &amp; Interactive Math</h2>'+
   '<div class="empty"><h2>Coming soon</h2><p>The outline is ready. Question banks, generators, and activities will be created separately and tested before being linked here.</p></div>'+
   '</section>'+unitPager(u)+'</div></section>';
 }
 function overview(){
  const q=search.value.trim().toLocaleLowerCase();
  const matching=course.units.filter(u=>!q||(u.name+' '+u.skills.join(' ')+' '+u.standards.join(' ')).toLocaleLowerCase().includes(q));
  const lead=crumb([[course.name,null]])+'<h1 tabindex="-1">'+esc(course.name)+'</h1>'+
   '<p class="band-blurb">'+esc(course.description)+'</p>'+
   '<p class="band-meta">'+stats.units+' units · '+stats.skills+' '+targetLabel+(hasPacing?' · '+paceLabel(pacingLow,pacingHigh)+' estimated instructional days':'')+' · question banks and activities coming later</p>';
  return band(lead,true)+'<section class="section"><div class="wrap">'+
   '<h2 class="course-units-title">Browse by unit</h2>'+
   '<p class="course-units-status">'+(hasObjectives?'Unit sequence and available pacing come from the source curriculum. Target labels summarize the stated goals; open a unit for the original section headings and standards when provided.':'Unit names and lesson order reflect the attached scope and sequence. Expand the lesson lists or open a unit to see its standards.')+'</p>'+
   (matching.length?'<ul class="units">'+matching.map(card).join('')+'</ul>':
   '<div class="empty"><h2>No matching units</h2><p>Try another topic or learning target.</p></div>')+'</div></section>';
 }
 function current(){
  const slug=decodeURIComponent(location.hash.replace(/^#/,''));
  const prefix=course.id+'.';
  return slug.startsWith(prefix)?course.units.find(u=>u.id===slug.slice(prefix.length)):undefined;
 }
 function render(){
  const u=current();
  main.innerHTML=u?unitPage(u):overview();
  back.style.visibility=u?'visible':'hidden';
  search.style.visibility=u?'hidden':'visible';
  document.title=(u?title(u)+' | ':'')+course.name+' | Mr. K’s Classroom';
 }
 document.getElementById('skip')?.addEventListener('click',()=>main.focus());
 back.addEventListener('click',()=>{location.hash='';render();window.scrollTo(0,0);});
 document.getElementById('searchForm').addEventListener('submit',e=>{e.preventDefault();location.hash='';render();});
 search.addEventListener('input',()=>{if(!current())render();});
 window.addEventListener('hashchange',()=>{render();window.scrollTo(0,0);});
 render();
}
