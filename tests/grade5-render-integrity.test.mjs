import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const ctx = {console}; ctx.window=ctx; vm.createContext(ctx);
for (const path of ['worksheet-generator/grade5/generators-content.js','worksheet-generator/grade5/generators-core.js','worksheet-generator/grade5/generators-render.js']) {
  vm.runInContext(fs.readFileSync(new URL('../'+path,import.meta.url),'utf8'),ctx,{filename:path});
}
const core=ctx.G5_GENERATORS_CORE, render=ctx.G5_GENERATORS_RENDER;
const base={mode:'activity',kind:'matching',unit:{name:'Sample',number:1},options:core.options(),items:[
  {id:'q1',prompt:'One?',answer:'1',solutionSteps:[]},{id:'q2',prompt:'Two?',answer:'2',solutionSteps:[]},
  {id:'q3',prompt:'Three?',answer:'3',solutionSteps:[]}
],answers:['3','1','2'],warnings:[]};
test('matching teacher answer letters refer to shuffled answer column',()=>{
  const html=render.render(base,true);
  assert.match(html,/<td>1<\/td><td>1<\/td><td>B<\/td>/);
  assert.match(html,/<td>2<\/td><td>2<\/td><td>C<\/td>/);
  assert.match(html,/<td>3<\/td><td>3<\/td><td>A<\/td>/);
});
test('station question labels extend past three questions',()=>{
  const plan={...base,kind:'stations',stations:[{n:1,items:Array.from({length:6},(_,i)=>({id:'s'+i,prompt:'Problem '+i,answer:String(i)}))}],items:[]};
  const html=render.render(plan,false);
  assert.match(html,/d\.<\/span>/);
  assert.doesNotMatch(html,/undefined\.<\/span>/);
});
