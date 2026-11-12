import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const ctx={console};ctx.window=ctx;vm.createContext(ctx);
for(const file of ['worksheet-generator/grade5/generators-content.js','worksheet-generator/grade5/generators-core.js'])
 vm.runInContext(fs.readFileSync(new URL('../'+file,import.meta.url),'utf8'),ctx);
test('color by number has six used colors and no ambiguous duplicate answers',()=>{
 const C=ctx.G5_GENERATORS_CORE;
 const q=Array.from({length:24},(_,i)=>({id:'q'+i,skillId:'s',level:'cp1',format:'short-answer',prompt:'Find value '+i,answer:String(i),solutionSteps:[]}));
 const unit={name:'Sample',id:'sample',skills:[{id:'s',name:'Numbers'}],questions:q,meta:{}};
 const plan=C.buildActivity(unit,C.options({skills:['s'],level:'cp1',activity:'color',count:12}),'fixed');
 assert.equal(new Set(plan.grid.map(x=>x.color)).size,6);
 assert.equal(new Set(plan.items.map(x=>C.norm(C.answerText(x)))).size,plan.items.length);
 assert.ok(plan.grid.every(x=>x.label));
 assert.ok(plan.items.every(q=>plan.grid.some(cell=>C.norm(cell.label)===C.norm(C.answerText(q)))));
});
