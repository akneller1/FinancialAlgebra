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
   const deck=draw(slots);assert.equal(deck.length,20);assert.equal(new Set(deck.map(q=>q.id)).size,20);
   for(const q of deck){
    const original=bank.questions.find(x=>x.id===q.id),it=gameItem(q,R);
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
