import {course,getUnit} from './course.js';
import {makeQuestion} from './questions.js';
import {fmtMoney} from './engine.js';
const params=new URLSearchParams(location.search);
const ids=course.units.filter(u=>u.status==='pilot').map(u=>u.id);
let id=ids.includes(params.get('unit'))?params.get('unit'):'budgeting';
let count=6,start=0,selected=[1,2,3],step='setup',tab='student';
const el=document.getElementById('generator'),sum=document.getElementById('summary'),back=document.getElementById('backToUnit');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function questions(){
 const result=[];
 for(let i=start;i<start+300&&result.length<count;i++){
  const q=makeQuestion(id,i);
  const which=Number(q.skillId.split('-').at(-1));
  if(selected.includes(which))result.push(q);
 }
 if(result.length!==count)throw new Error('Insufficient questions for selected skills');
 return result;
}
function renderPaper(mode){
 const data=questions(),title=getUnit(id).name;
 return '<section class="fa-paper"><div class="fa-paper-head"><span>MR. K’S CLASSROOM · FINANCIAL ALGEBRA</span><h2>'+esc(title)+'</h2>'+
 '<p>'+ (mode==='student'?'Name: __________________________________ &nbsp; Date: ______________':'Teacher answer key') +'</p></div>'+
 data.map((q,i)=>'<article class="fa-paper-item"><strong>'+String(i+1)+'.</strong> '+esc(q.prompt)+
 (mode==='teacher'?'<div class="fa-paper-solution"><strong>Answer: '+esc(fmtMoney(q.answer))+'</strong><p>'+esc(q.solutionSteps.join(' '))+'</p></div>':
 '<div class="fa-answer-lines"><i></i><i></i><i></i></div>')+'</article>').join('')+
 '<p class="fa-paper-foot">Show your work. Financial calculations follow the assumptions stated in each problem.</p></section>';
}
function render(){
 const u=getUnit(id);
 back.href='index.html#financial-algebra.'+id;
 document.querySelectorAll('[data-step]').forEach(b=>b.classList.toggle('on',b.dataset.step===step));
 sum.innerHTML='<span><b>'+esc(u.name)+'</b></span><span>'+count+' questions</span><span>Financial Algebra · One level</span>';
 if(step==='setup'){
  el.innerHTML='<div class="mm-view-setup"><div class="card mm-card"><h2><span class="step">1</span> Choose a unit</h2><div class="field"><label class="lbl" for="unit">Unit</label><select id="unit">'+ids.map(x=>
   '<option value="'+x+'" '+(id===x?'selected':'')+'>'+esc(getUnit(x).name)+'</option>').join('')+'</select></div>'+
   '<div class="field"><label class="lbl" for="count">Number of questions</label><select id="count">'+[4,6,8,10,12].map(x=>
   '<option value="'+x+'" '+(count===x?'selected':'')+'>'+x+'</option>').join('')+'</select></div>'+
   '<p class="hint">The course has one common level. There are no CP2, CP1 or Honors selections.</p></div>'+
   '<div class="card mm-card"><h2><span class="step">2</span> Select skills</h2><p class="hint">Choose the concepts to practice.</p>'+
   u.skills.slice(0,3).map((skill,i)=>'<label class="lrow"><input type="checkbox" data-skill="'+(i+1)+'" '+(selected.includes(i+1)?'checked':'')+'><span class="ltitle">'+esc(skill)+'</span></label>').join('')+
   '<div class="bulk"><button type="button" id="all" class="btn ghost sm">Select all</button></div></div>'+
   '<div class="card mm-card" style="grid-column:1/-1"><h2><span class="step">3</span> Create</h2>'+
   '<p class="hint">Generate a student worksheet and a separate worked teacher key.</p><button type="button" class="btn" id="create">Generate worksheet →</button></div></div>';
 } else {
  el.innerHTML='<div class="ptool"><div class="grp"><button class="tab" type="button" data-tab="student" aria-pressed="'+(tab==='student')+'">Student</button>'+
  '<button class="tab" type="button" data-tab="teacher" aria-pressed="'+(tab==='teacher')+'">Teacher key</button></div><span class="sp"></span>'+
  '<button class="btn ghost sm" id="regenerate" type="button">Regenerate</button><button class="btn" id="print" type="button">Print / Save PDF</button></div>'+
  '<div id="pagesWrap"><div id="pages">'+renderPaper(tab)+'</div></div>'+
  '<div class="fa-footer-actions"><button type="button" class="btn ghost" id="edit">← Edit settings</button></div>';
 }
}
document.getElementById('mmMain').addEventListener('change',e=>{
 if(e.target.id==='unit'){id=e.target.value;selected=[1,2,3];start=0;render();}
 if(e.target.id==='count'){count=Number(e.target.value);render();}
 if(e.target.dataset.skill){const n=Number(e.target.dataset.skill);selected=e.target.checked?[...selected.filter(v=>v!==n),n].sort():selected.filter(v=>v!==n);}
});
document.getElementById('mmMain').addEventListener('click',e=>{
 const s=e.target.closest('[data-step]')?.dataset.step;
 if(s){if(s==='setup'||selected.length){step=s;render();}return;}
 const t=e.target.dataset.tab;
 if(t){tab=t;render();return;}
 if(e.target.id==='all'){selected=[1,2,3];render();}
 if(e.target.id==='create'){if(!selected.length){alert('Select at least one skill.');return;}step='preview';render();}
 if(e.target.id==='regenerate'){start+=count*3;render();}
 if(e.target.id==='edit'){step='setup';render();}
 if(e.target.id==='print'){window.print();}
});
render();
