import {getUnit} from './course.js';
import {makeQuestion,gradeQuestion} from './questions.js';
import {fmtMoney} from './engine.js';
const params=new URLSearchParams(location.search);
const id=getUnit(params.get('unit'))?.status==='pilot'?params.get('unit'):'budgeting';
const unit=getUnit(id);
document.getElementById('backToUnit').href='index.html#financial-algebra.'+id;
const root=document.getElementById('practice');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const N=8;
let start=0,screen='intro',responses=Array(N).fill(''),result=null;
function questions(){return Array.from({length:N},(_,i)=>makeQuestion(id,start+i));}
function render(){
 const q=questions();
 if(screen==='intro'){
  root.innerHTML='<section class="pt-card"><div class="pt-eyebrow">Financial Algebra · '+esc(unit.name)+'</div>'+
  '<h1>Assessment Readiness Check</h1>'+
  '<p>Answer '+N+' financial-math questions. Review your score and worked solutions at the end. This course has one standard level—there is no difficulty selector.</p>'+
  '<p class="pt-muted">The financial models are educational approximations and state their assumptions in each question.</p>'+
  '<div class="pt-actions"><button id="start" type="button">Start practice test</button>'+
  '<a class="btn ghost" href="worksheet.html?unit='+id+'">Create a printable worksheet</a></div></section>';
  return;
 }
 const answered=responses.filter(x=>String(x).trim()!=='').length;
 const header='<div class="pt-header"><div><div class="pt-eyebrow">'+esc(unit.name)+'</div><h1>Assessment Readiness Check</h1></div><div class="pt-muted">'+answered+' of '+N+' responses</div></div>'+
 '<div class="pt-progress"><div style="width:'+(100*answered/N)+'%"></div></div>';
 if(screen==='test'){
  root.innerHTML=header+'<div class="pt-nav" role="navigation" aria-label="Question navigation">'+q.map((v,i)=>
   '<button class="'+(responses[i]!==''?'answered':'')+'" type="button" data-question="'+i+'">'+(i+1)+'</button>').join('')+'</div>'+
   q.map((v,i)=>'<section class="pt-test-question" id="question-'+i+'"><div class="pt-card">'+
    '<div class="pt-top"><span class="pt-eyebrow">Question '+(i+1)+' of '+N+'</span><span class="pt-muted">'+esc(unit.skills[Number(v.skillId.split('-').at(-1))-1]||'Financial mathematics')+'</span></div>'+
    '<div class="pt-problem">'+esc(v.prompt)+'</div>'+
    '<label class="pt-response" for="response-'+i+'">Your answer ($)<input type="number" inputmode="decimal" step="0.01" id="response-'+i+'" data-response="'+i+'" value="'+esc(responses[i])+'" placeholder="Amount in dollars"></label>'+
    '</div></section>').join('')+
   '<div class="pt-card"><p class="pt-muted">Review your answers before grading; unanswered questions count as incorrect.</p>'+
   '<div class="pt-actions"><button type="button" id="grade">Grade assessment</button><button type="button" class="pt-secondary" id="restart">New assessment</button></div></div>';
   return;
 }
 if(screen==='results'){
  let num=0;
  q.forEach((question,i)=>{if(gradeQuestion(question,responses[i]).correct)num++;});
  root.innerHTML='<section class="pt-card"><div class="pt-eyebrow">Financial Algebra · '+esc(unit.name)+'</div><h1>Your results</h1><p class="pt-score">'+num+' / '+N+'</p>'+
   '<p class="pt-muted">Review each solution below, then try a new version to practice the same financial ideas.</p><div class="pt-actions">'+
   '<button id="restart" type="button">New assessment</button>'+
   '<a href="worksheet.html?unit='+id+'" class="btn ghost">Worksheet generator</a></div></section>'+
   q.map((question,i)=>{const g=gradeQuestion(question,responses[i]);return '<details class="pt-card pt-review" '+(!g.correct?'open':'')+'>'+
    '<summary>Question '+(i+1)+' · <span class="'+(g.correct?'pt-good':'pt-bad')+'">'+(g.correct?'Correct':'Needs review')+'</span></summary>'+
    '<div class="pt-problem">'+esc(question.prompt)+'</div><p><strong>Your answer:</strong> '+(responses[i]===''?'Not answered':esc(responses[i]))+'</p>'+
    '<div class="pt-explain"><strong>Correct answer: '+esc(fmtMoney(question.answer))+'</strong><p>'+esc(question.solutionSteps.join(' '))+'</p></div></details>';}).join('');
 }
}
root.addEventListener('input',e=>{if(e.target.dataset.response!==undefined)responses[Number(e.target.dataset.response)]=e.target.value;});
root.addEventListener('click',e=>{
 const n=e.target.dataset.question;
 if(n!==undefined){document.getElementById('question-'+n)?.scrollIntoView({behavior:'smooth'});return;}
 if(e.target.id==='start'){screen='test';render();return;}
 if(e.target.id==='grade'){screen='results';render();window.scrollTo(0,0);return;}
 if(e.target.id==='restart'){start+=N;responses=Array(N).fill('');screen='test';render();window.scrollTo(0,0);}
});
render();
