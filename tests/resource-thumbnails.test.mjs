import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import vm from 'node:vm';
import {course,getUnit} from '../src/course.js';
import {resourceThumbnail,resourceHref} from '../financial/lib/resource-previews.mjs';
const root=new URL('../',import.meta.url);
const read=p=>readFileSync(new URL(p,root),'utf8');
const manifest=JSON.parse(read('financial/resources.json'));

test('all ten unit views show a local thumbnail on every resource card',async()=>{
 for(const unit of course.units){
  const main={innerHTML:'',focus(){}};
  const elements={main,q:{value:'',style:{},addEventListener(){}},backBtn:{style:{},addEventListener(){}},skip:{addEventListener(){}},searchForm:{addEventListener(){}}};
  const document={getElementById:id=>elements[id]};
  const location={hash:'#financial-algebra.'+unit.id};
  const context=vm.createContext({course,getUnit,resourceThumbnail,resourceHref,URL,document,location,fetch:async()=>({ok:true,json:async()=>manifest}),window:{addEventListener(){},scrollTo(){}}});
  const source=read('src/site.js').replace(/^import .*;\n/gm,'').replaceAll('import.meta.url',JSON.stringify(new URL('src/site.js',root).href));
  await vm.runInContext('(async()=>{'+source+'})()',context);
  const cards=[...main.innerHTML.matchAll(/<a class="finance-resource-card"[^>]*>[\s\S]*?<\/a>/g)].map(m=>m[0]);
  const resources=manifest.units.find(u=>u.unitId===unit.id).resources;
  assert.equal(cards.length,8+resources.projects.length,unit.id+' resource count');
  for(const card of cards){
   assert.match(card,/<img class="finance-resource-thumb"/);
   for(const match of card.matchAll(/(?:href|src)="([^"]+)"/g)){
    const path=match[1].replace(/&amp;/g,'&').split(/[?#]/)[0];
    assert.ok(existsSync(new URL(path,root)),unit.id+': '+path);
   }
  }
 }
});
