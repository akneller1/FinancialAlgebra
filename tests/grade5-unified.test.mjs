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
  const win={document,location:{hash},addEventListener(name,fn){listeners[name]=fn;},scrollTo(){},
    fetch:async()=>({ok:true,json:async()=>JSON.parse(read('course-outlines/grade5.json'))})};
  win.window=win;
  const context=vm.createContext({window:win,document,console,location:win.location,URLSearchParams});
  for(const file of ['data.js','course-catalog.js','grade5-resource-catalog.js','src/grade5-site.js']){
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
  assert.ok(gameChrome.includes('../grade5.html#math5'));
  assert.equal(gameChrome.includes('../index.html#math5'),false);
  for(const slug of Object.values(runPage().win.MK_GRADE5_RESOURCES.projects)){
    const p=read('math5-project-'+slug+'/index.html');
    assert.ok(p.includes('href="../grade5.html#math5.'),slug+' return to unit');
    assert.equal(p.includes('grade5-resources.html'),false,slug+' legacy return');
  }
});
