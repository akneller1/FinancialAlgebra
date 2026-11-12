import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import vm from 'node:vm';

const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
function runPage(hash=''){
  const listeners={};
  const elements={
    main:{innerHTML:'',focus(){},addEventListener(name,fn){listeners['main:'+name]=fn;}},
    q:{value:'',style:{},addEventListener(name,fn){listeners['q:'+name]=fn;}},
    backBtn:{style:{},addEventListener(name,fn){listeners['back:'+name]=fn;}},
    skip:{addEventListener(name,fn){listeners['skip:'+name]=fn;}},
    searchForm:{addEventListener(name,fn){listeners['search:'+name]=fn;}}
  };
  const document={title:'',getElementById(name){return elements[name]||null;}};
  const win={document,location:{hash,href:'https://akneller1.github.io/FinancialAlgebra/grade5.html'},addEventListener(name,fn){listeners[name]=fn;},scrollTo(){},
    fetch:async()=>({ok:true,json:async()=>JSON.parse(read('course-outlines/grade5.json'))})};
  win.window=win;
  const context=vm.createContext({window:win,document,console,location:win.location,URL,URLSearchParams});
  for(const file of ['data.js','course-catalog.js','grade5-resource-catalog.js','src/grade5-student-links.js','src/grade5-site.js']){
    vm.runInContext(read(file),context,{filename:file});
  }
  return {html:elements.main.innerHTML,elements,win,listeners};
}

test('Grade 5 class is one page, not separate outline and resource library',()=>{
  const page=read('grade5.html');
  const home=read('index.html');
  for(const html of [page,home]){
    assert.ok(html.includes('href="grade5.html"'));
    assert.equal(html.includes('href="grade5-resources.html"'),false,'duplicate course/library navigation');
  }
  for(const src of ['data.js','course-catalog.js','grade5-resource-catalog.js','src/grade5-site.js']){
    assert.ok(page.includes(src),'Grade 5 page missing '+src);
  }
  const alias=read('grade5-resources.html');
  assert.ok(alias.includes("location.replace('./grade5.html'+hash)"),'old library URL must redirect to unified page');
  const result=runPage();
  assert.ok(result.html.includes('Browse by unit'));
  assert.ok(result.html.includes('Original curriculum sequence (13 pacing units)'));
  assert.equal((result.html.match(/class="unit algebra-unit-card"/g)||[]).length,11);
  assert.ok(result.html.includes('href="#math5.place-value-number-sense"'));
  assert.ok(result.html.includes('Grade 5 Math')||result.html.includes('5th Grade Math'));
});

test('All 11 units use the Classroom unit banner, section order and resource cards',()=>{
  const {win}=runPage();
  for(const unit of win.MK_GRADE5_RESOURCES.course.units){
    const page=runPage('#math5.'+unit.id);
    const html=page.html;
    assert.ok(html.includes('algebra-unit-layout'),unit.id+' layout');
    assert.ok(html.includes('unit-pager'),unit.id+' pager');
    assert.ok(html.includes('generator-banner compact'),unit.id+' shortcuts');
    const sections=['g5-games','g5-study-guides','g5-interactive','g5-projects'];
    let before=-1;
    for(const name of sections){
      const idx=html.indexOf('id="'+name+'"');
      if(idx<0){
        assert.equal(name,'g5-interactive',unit.id+' missing '+name);
        continue;
      }
      assert.ok(idx>before,unit.id+' activity order: '+name);
      before=idx;
    }
    assert.ok(html.includes('cards grouped-cards'),unit.id+' resource cards');
    assert.ok(html.includes('Skills in this unit'),unit.id+' skills');
    assert.equal(html.includes('grade5-resources.html'),false,unit.id+' has orphan library link');
    const cards=[...html.matchAll(/<li class="card g5-resource-card"[^>]*>/g)];
    assert.equal(cards.length,unit.artifacts.length,unit.id+' resource counts');
    const shortcuts=html.match(/data-g5-scroll="g5-games"/g)||[];
    assert.equal(shortcuts.length,1,unit.id+' game shortcut');
    for(const resource of unit.artifacts){
      assert.ok(html.includes('href="'+resource.path.replaceAll('&','&amp;')+'"'),unit.id+' missing link '+resource.path);
      assert.ok(existsSync(new URL('../'+resource.path.split(/[?#]/)[0],import.meta.url)),resource.path+' target');
    }
  }
});

test('All return links stay inside the unified Grade 5 class',()=>{
  const shell=read('worksheet-generator/grade5/tool-shell.js');
  const gameChrome=read('worksheet-generator/grade5/g5-core.js');
  assert.ok(shell.includes('../grade5.html'));
  assert.ok(gameChrome.includes("home.href = 'https://mrksclassroom.com/'"), 'Grade 5 game header should return to public Classroom homepage');
  assert.equal(gameChrome.includes("home.href = '../grade5.html"),false,'Removed Grade 5 alias must not be the game homepage');
  for(const slug of Object.values(runPage().win.MK_GRADE5_RESOURCES.projects)){
    const p=read('math5-project-'+slug+'/index.html');
    assert.ok(p.includes('href="../grade5.html#math5.'),slug+' return to unit');
    assert.equal(p.includes('grade5-resources.html'),false,slug+' legacy return');
  }
});

test('Open resource is a real anchor and only games and study guides have student link controls',()=>{
 const {win}=runPage();
 const css=read('site-overrides.css');
 assert.ok(css.includes('.g5-resource-card h3 a::after{content:none!important'), 'Main card overlay must not block the action controls');
 for(const u of win.MK_GRADE5_RESOURCES.course.units){
  const page=runPage('#math5.'+u.id).html;
  const openLinks=[...page.matchAll(/<a class="btn btn-open" href="([^"]+)">Open resource →<\/a>/g)];
  const copyControls=[...page.matchAll(/<button type="button" class="g5-student-copy"[^>]*>Copy student link<\/button>/g)];
  const explicitThumbLinks=[...page.matchAll(/<a class="thumb g5-resource-image-link" href="([^"]+)"/g)];
  assert.equal(openLinks.length,u.artifacts.length,'Open resource links: '+u.id);
  assert.equal(copyControls.length,u.artifacts.filter(a=>['Game','Study Guide'].includes(a.type)).length,'Student share controls: '+u.id);
  assert.equal(explicitThumbLinks.length,u.artifacts.length,'Clickable thumbnails: '+u.id);
  assert.ok(page.includes('<option value="cp1" selected>Standard</option>'),u.id+' has a level selector');
 }
 const page=read('grade5.html');
 assert.ok(page.includes('src/grade5-student-links.js'),'Shared Grade 5 URL builder loaded');
 assert.ok(page.indexOf('src/grade5-student-links.js')<page.indexOf('src/grade5-site.js'),'URL builder loads first');
});

test('Student links preserve unit and game, set level, and never point to project teacher guides',()=>{
 const {win}=runPage();
 const {destination,hasLevel}=win.MK_GRADE5_STUDENT_LINKS;
 const base='https://akneller1.github.io/FinancialAlgebra/grade5.html';
 const grade5=win.MK_GRADE5_RESOURCES.course;
 let tested=0;
 for(const unit of grade5.units)for(const resource of unit.artifacts){
  const level=hasLevel(resource)?'honors':'cp1';
  const absolute=destination(resource,level,base);
  const u=new URL(absolute);
  assert.equal(u.origin,'https://akneller1.github.io');
  assert.ok(u.pathname.startsWith('/FinancialAlgebra/'));
  const rootPath=u.pathname.replace(/^\/FinancialAlgebra\//,'');
  assert.ok(existsSync(new URL('../'+rootPath,import.meta.url)),unit.id+' missing student destination '+rootPath);
  if(resource.type==='Project'){
   assert.match(rootPath,/math5-project-[a-z0-9-]+\/[a-z0-9-]+-honors\.pdf$/);
   assert.ok(!u.href.includes('teacher-guide'));
  }else if(resource.type==='Game'){
   assert.equal(u.searchParams.get('unit'),unit.id);
   assert.ok(u.searchParams.has('game'));
   assert.equal(u.searchParams.get('student'),'1');
   assert.equal(u.searchParams.get('level'),'honors');
  }else if(resource.type==='Study Guide'&&resource.title==='Cheat Sheet'){
   assert.match(rootPath,/worksheet\.pdf$/);
   assert.ok(!u.searchParams.has('student'));
  }else{
   assert.equal(u.searchParams.get('student'),'1');
  }
  assert.notEqual(u.searchParams.get('mode'),'teacher');
  tested++;
 }
 assert.ok(tested>100,'every unit has many student resources');
 const project=grade5.units.flatMap(u=>u.artifacts).find(a=>a.type==='Project');
 for(const grade of ['cp2','cp1','honors']){
  const uri=new URL(destination(project,grade,base));
  assert.ok(uri.pathname.endsWith('-'+grade+'.pdf'));
  assert.ok(existsSync(new URL('../'+uri.pathname.replace(/^\/FinancialAlgebra\//,''),import.meta.url)));
 }
});

test('Student interactive mode hides teacher-view button and excludes the teacher-notes section',()=>{
 const tool=read('worksheet-generator/grade5/tool-shell.js');
 assert.ok(tool.includes("if (!studentMode) {"));
 assert.ok(tool.includes("studentMode ? '' : '<button type="));
 assert.ok(tool.includes("if (studentMode) return;"));
 assert.ok(!tool.includes('Copy student link'),'Student sharing is limited to games and study guides');
 const core=read('worksheet-generator/grade5/g5-core.js');
 assert.ok(core.includes('Copy student link'),'Games and study activities have an in-app student sharing button');
 assert.ok(core.includes("url.searchParams.set('student','1')"),'Games and checks share student view');
 for(const page of ['grade5-games.html','grade5-flashcards.html','grade5-understanding-check.html']){
   assert.ok(read('worksheet-generator/'+page).includes('g5-core.js?v=grade5-home-link-20261112'),page+' needs updated activity chrome');
 }
 for(const slug of ['area-model-explorer','coordinate-explorer','expression-builder','fraction-explorer',
   'measurement-converter','place-value-builder','volume-builder']){
  const html=read('math5-'+slug+'/index.html');
  assert.ok(html.includes('tool-shell.js?v=games-guides-only-20261112'),slug+' needs updated student-mode tool shell');
 }
});
