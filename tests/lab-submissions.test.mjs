import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
function engine(query,data=new Map()){
 const nodes=new Map(),node=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',events:{},addEventListener(k,f){this.events[k]=f;}});return nodes.get(id);};
 const document={getElementById:node,title:''};let current;
 const win={document,location:new URL('https://school.test/financial/decision-lab/index.html?'+query),URLSearchParams,console,localStorage:{getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v)},addEventListener(){},scrollTo(){},FA_SUBMISSIONS:{attach:c=>current=c}};win.window=win;
 vm.createContext(win);for(const p of ['financial/lib/finance.js','financial/lib/render.js','financial/decision-lab/scenarios.js','financial/decision-lab/lab.js'])vm.runInContext(source(p),win);
 return {win,data,get current(){return current;},node,input(key,value){node('app').events.input({target:{value,getAttribute:k=>k==='data-resp'?key:null}});}};
}
test('all ten lab reports include full prompts, settings, partial work, and separate teacher keys',()=>{
 const first=engine('lab=income');
 for(const id of Object.keys(first.win.FA_LABS)){
  const e=engine('lab='+id),c=e.current; c.resp.studentName='<script>student</script>';c.resp.q0='123';
  e.win.document.querySelector=()=>({after(){}});e.win.document.createElement=()=>({setAttribute(){},querySelector(){}});
  vm.runInContext(source('financial/decision-lab/submissions.js'),e.win);e.win.FA_SUBMISSIONS.attach(c);
  const student=e.win.FA_SUBMISSIONS.report(false),teacher=e.win.FA_SUBMISSIONS.report(true);
  assert.match(student,/&lt;script&gt;student&lt;\/script&gt;/);assert.match(student,/Not answered/);assert.match(student,/123/);assert.match(student,/Current setting/);assert.match(student,/student’s current settings/);
  assert(!student.includes('Sample recommendation'));assert.match(teacher,/Sample recommendation/);assert.match(teacher,/Rubric/);
  for(const q of [...c.lab.questions,...c.lab.challenges])assert(teacher.includes(c.fmt(q.answer(c.defaults),q.fmt)),id);
 }
});
test('answers and slider settings survive reload; assignment links isolate work',()=>{
 const e=engine('lab=income');e.input('q0','1700');const v=e.current.lab.vars.find(v=>v.type!=='toggle');e.current.vars[v.id]=v.max;e.current.save();
 const reload=engine('lab=income',e.data);assert.equal(reload.current.resp.q0,'1700');assert.equal(reload.current.vars[v.id],v.max);
 const assigned=engine('lab=income&student=1&assignment=new&settings='+encodeURIComponent(JSON.stringify({[v.id]:v.min})),e.data);assert.equal(assigned.current.resp.q0,undefined);assert.equal(assigned.current.vars[v.id],v.min);assert(!assigned.node('app').innerHTML.includes('Teacher view'));
});
