import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {GAMES,eligible,createDeck,gameItem} from '../financial/games/deck.mjs';
const root=new URL('../',import.meta.url);
const manifest=JSON.parse(fs.readFileSync(new URL('financial/resources.json',root)));
const ctx=vm.createContext({});vm.runInContext(fs.readFileSync(new URL('financial/games/vendor/rng.js',root),'utf8'),ctx);
vm.runInContext(fs.readFileSync(new URL('financial/lib/render.js',root),'utf8'),ctx);
const R=ctx.FA_RENDER;
for(const unit of manifest.units){
 const bank=JSON.parse(fs.readFileSync(new URL('financial/banks/'+unit.unitId+'.json',root)));
 test(unit.name+': all five games have playable questions and correct shuffled answers',()=>{
  const pool=eligible(bank);assert.ok(pool.length>=10);
  const draw=createDeck(bank,ctx.MKWS.rng.make('game-test-'+unit.unitId));
  const slots=bank.skills.flatMap(s=>Array.from({length:5},(_,i)=>({skill:s.id,col:s.id,row:i})));
  for(let round=0;round<3;round++){
   const deck=draw(slots);assert.equal(deck.length,slots.length);assert.equal(new Set(deck.map(q=>q.id)).size,slots.length);
   for(const q of deck){
    const original=pool.find(x=>x.id===q.id),it=gameItem(q,R);   // the playable form: as written, or with choices from its own work
    assert.equal(it.skill,q.slot.skill);assert.equal(it.q.prompt,original.prompt);
    assert.equal(it.options.filter(o=>o.ok).length,1);
    assert.equal(it.options.find(o=>o.ok).a,original.options.find(o=>o.correct).text);
    assert.deepEqual(it.options.map(o=>o.a).sort(),original.options.map(o=>o.text).sort());
    assert.equal(it.q.fig,original.scenario?R.scenario(original.scenario):null);
    assert.ok(it.steps.length);assert.ok(!it.typed);
   }
  }
  assert.equal(unit.resources.games.length,5);
  for(const game of GAMES){
   const link=unit.resources.games.find(g=>g.id===game.id);assert.ok(link);
   const url=new URL(link.path,'https://example.test/');assert.equal(url.searchParams.get('unit'),unit.unitId);
   assert.equal(url.searchParams.get('game'),game.id);
   assert.ok(fs.existsSync(new URL(url.pathname.slice(1),root)));
   assert.ok(fs.existsSync(new URL('thumbs/financial-algebra/'+unit.unitId+'-'+game.id+'.svg',root)));
  }
 });
}
test('Adapter excludes open responses, select-all, invalid choices and ineligible items',()=>{
 const q={id:'a',skillId:'one',gameEligible:true,format:'multiple-choice',options:[{text:'A',correct:true},{text:'B',correct:false}]};
 const bank={skills:[{id:'one'}],questions:[q,{...q,id:'b',gameEligible:false},{...q,id:'c',format:'select-all'},{...q,id:'d',options:[{text:'A',correct:true},{text:'a',correct:false}]},{...q,id:'e',options:[{text:'A',correct:true},{text:'B',correct:true}]}]};
 assert.deepEqual(eligible(bank).map(q=>q.id),['a']);
 assert.equal(createDeck(bank,ctx.MKWS.rng.make(1))([{skill:'one'},{skill:'one'},{skill:'other'}]).length,1);
});

import {slotLevel} from '../financial/games/deck.mjs';
test('game slots draw from the requested level; Mixed Showdown climbs Support → Advanced',()=>{
 assert.equal(slotLevel({level:'cp2'}),'support');assert.equal(slotLevel({level:'honors'}),'advanced');
 assert.deepEqual([0,1,2,3,4].map(row=>slotLevel({level:'mixed',row})),['support','support','standard','advanced','advanced']);
 assert.deepEqual([1,2,3].map(c=>slotLevel({c})),['support','standard','advanced']);assert.equal(slotLevel({}),'standard');
 for(const unit of manifest.units){
  const bank=JSON.parse(fs.readFileSync(new URL('financial/banks/'+unit.unitId+'.json',root)));
  for(const level of ['cp2','cp1','honors']){
   const draw=createDeck(bank,ctx.MKWS.rng.make('lv-'+unit.unitId+level)),slots=bank.skills.flatMap(s=>Array.from({length:3},(_,row)=>({skill:s.id,row,level})));
   const deck=draw(slots),want={cp2:'support',cp1:'standard',honors:'advanced'}[level];
   assert.equal(deck.length,slots.length,unit.unitId+' '+level);
   // every card is at the level unless that skill has run out of game cards there (then a neighbouring level fills in)
   const pool=eligible(bank);
   for(const s of bank.skills){const have=pool.filter(q=>q.skillId===s.id&&q.level===want).length,got=deck.filter(q=>q.skillId===s.id&&q.level===want).length;assert.equal(got,Math.min(3,have),unit.unitId+' '+s.id+' '+level);}
   const share=deck.filter(q=>q.level===want).length/deck.length;
   assert.ok(share>=0.75,unit.unitId+' '+level+' share at level '+share.toFixed(2));
  }
 }
});
