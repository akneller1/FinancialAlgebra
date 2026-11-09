import {course,getUnit} from './course.js';
import {budgetSummary,creditPayoff,futureValue,fmtMoney} from './engine.js';
import {makeQuestion,gradeQuestion,createWorksheet} from './questions.js';

const root=document.getElementById('app');
const pilotIds=course.units.filter(u=>u.status==='pilot').map(u=>u.id);
const hashUnit=decodeURIComponent(location.hash.replace(/^#/,''));
const state={
  unitId:pilotIds.includes(hashUnit)?hashUnit:'budgeting',
  level:'cp1',index:0,result:null,lastAnswer:'',
  budget:{income:3800,housing:1400,transport:400,essentials:1000,savings:600},
  credit:{balance:3000,apr:24,payment:150},
  investing:{principal:1000,monthly:150,annualRate:6,years:20}
};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function range(key,label,min,max,step,value,display){
  return '<label class="slider-row"><span class="slider-label"><span>'+esc(label)+'</span><strong>'+esc(display(value))+'</strong></span><input data-slider="'+esc(key)+'" aria-label="'+esc(label)+'" type="range" min="'+min+'" max="'+max+'" step="'+step+'" value="'+value+'"></label>';
}
const money=v=>fmtMoney(v);
const percent=v=>v+'%';
function stat(label,value,extra=''){
  return '<div class="stat '+extra+'"><span>'+esc(label)+'</span><strong>'+esc(value)+'</strong></div>';
}
function simulator(){
  if(state.unitId==='budgeting') {
    const b=state.budget,r=budgetSummary(b);
    return '<div class="lab-grid"><div class="sliders">'+
      range('income','Monthly take-home pay',2000,7000,100,b.income,money)+
      range('housing','Housing',700,3500,50,b.housing,money)+
      range('transport','Transportation',100,1600,50,b.transport,money)+
      range('essentials','Other essentials',300,2200,50,b.essentials,money)+
      range('savings','Savings goal',0,2000,50,b.savings,money)+
      '</div><div class="result-grid">'+stat('Monthly income',money(r.income))+stat('Allocated',money(r.spent))+stat('Unallocated money',money(r.remaining),'wide '+(r.balanced?'positive':'negative'))+stat('Savings rate',Math.round(r.savingsRate*100)+'%','wide')+'</div></div><p class="note">Try reducing an expense or increasing savings. A negative remainder means this monthly plan is not affordable.</p>';
  }
  if(state.unitId==='credit') {
    const c=state.credit,r=creditPayoff(c);
    const baseline=creditPayoff({...c,payment:100});
    return '<div class="lab-grid"><div class="sliders">'+
      range('balance','Starting debt',1000,6000,100,c.balance,money)+
      range('apr','Credit card APR',12,30,1,c.apr,percent)+
      range('payment','Monthly payment',100,500,10,c.payment,money)+
      '</div><div class="result-grid">'+stat('Months until paid off',r.paidOff?String(r.months):'Not paid off')+
      stat('Total interest',r.paidOff?money(r.interest):'N/A')+
      stat('Total payments',r.paidOff?money(r.totalPaid):'N/A','wide')+
      stat('Interest saved vs. $100/month',(r.paidOff&&baseline.paidOff)?money(Math.max(0,baseline.interest-r.interest)):'N/A','wide positive')+
      '</div></div><p class="note">Assumes one fixed APR, monthly interest (APR ÷ 12), month-end payments, and no new purchases. Actual credit cards generally compute interest daily.</p>';
  }
  if(state.unitId==='investing') {
    const i=state.investing,r=futureValue(i);
    return '<div class="lab-grid"><div class="sliders">'+
      range('principal','Starting savings',0,10000,500,i.principal,money)+
      range('monthly','Monthly contribution',0,600,25,i.monthly,money)+
      range('annualRate','Hypothetical annual return',0,10,1,i.annualRate,percent)+
      range('years','Years invested',1,40,1,i.years,v=>v+' years')+
      '</div><div class="result-grid">'+stat('Ending account value',money(r.value),'wide positive')+
      stat('Your contributions',money(r.contributed))+stat('Investment growth',money(r.growth))+
      '</div></div><p class="note">Illustrative fixed-rate model with monthly compounding and contributions at month-end. Real investment returns vary, can be negative, and are not guaranteed; taxes and fees are excluded.</p>';
  }
  return '';
}
function renderUnitButtons(){
  return course.units.map((u,i)=>
    '<button class="unit-btn '+(state.unitId===u.id?'selected':'')+'" data-unit="'+esc(u.id)+'" aria-current="'+(state.unitId===u.id?'true':'false')+'">'+
    '<span class="unit-index">'+String(i+1).padStart(2,'0')+'</span><span class="unit-name">'+esc(u.name)+'</span>'+
    '<span class="tiny-tag '+(u.status==='planned'?'planned':'')+'">'+(u.status==='pilot'?'PILOT':'SOON')+'</span></button>').join('');
}
function practice(){
  const q=makeQuestion(state.unitId,state.level,state.index);
  let feedback='';
  if(state.result){
    const correct=state.result.correct;
    feedback='<div class="feedback '+(correct?'':'incorrect')+'" role="status">'+
      '<strong>'+(correct?'Correct — well done.':'Not quite. Review the solution.')+'</strong>'+
      '<p>Correct answer: <strong>'+esc(money(q.answer))+'</strong></p><p>'+esc(q.solutionSteps.join(' '))+'</p></div>';
  }
  return '<section class="card" aria-labelledby="practice-heading"><div class="title-row"><div><span class="small-heading">Practice generator</span><h3 id="practice-heading">Apply the math</h3></div><label>Difficulty <select class="level-control" id="level">'+
    [['cp2','CP2'],['cp1','CP1'],['honors','Honors']].map(([v,label])=>'<option value="'+v+'" '+(state.level===v?'selected':'')+'>'+label+'</option>').join('')+
    '</select></label></div><p class="subtext">Each new question uses different financial data. Work it out before revealing the key.</p>'+
    '<div class="question"><span class="small-heading">Question '+(state.index+1)+'</span><p>'+esc(q.prompt)+'</p>'+
    '<form id="answer-form" class="form-row"><label for="answer">Your answer ($)</label><input id="answer" name="answer" aria-label="Answer in dollars" type="number" step="0.01" inputmode="decimal" required value="'+esc(state.lastAnswer)+'" '+(state.result?'disabled':'')+'>'+
    '<button type="submit" class="primary" '+(state.result?'disabled':'')+'>Check answer</button></form>'+
    feedback+'</div><div class="button-row"><button class="secondary" data-action="next">New question</button>'+
    '<button class="secondary" data-action="worksheet">Print worksheet</button>'+
    '<button class="secondary" data-action="key">Teacher key</button></div>'+
    '<p class="note">Teacher keys are publicly accessible in this prototype. Student-facing access controls will be addressed before integration.</p></section>';
}
function render(){
  const unit=getUnit(state.unitId);
  const active=unit.status==='pilot';
  root.innerHTML='<header class="topbar"><div class="top-inner"><a class="brand" href="./">MR. K’S <em>CLASSROOM</em></a><div class="top-actions"><span class="pill">Standalone development</span><a href="https://mrksclassroom.com/" target="_blank" rel="noopener">Main website</a></div></div></header>'+
    '<div class="container"><div class="hero"><div><span class="small-heading" style="color:#a5e5eb">FINANCIAL ALGEBRA LAB</span><h1>Real money. Real math. Better decisions.</h1><p>Learn to budget, understand borrowing, and model investing with adjustable simulations and differentiated practice.</p></div>'+
    '<div class="hero-count"><strong>10</strong><span>Curriculum units</span><hr style="opacity:.2"><strong>3</strong><span>Interactive pilots</span></div></div>'+
    '<div class="layout"><aside class="sidebar" aria-label="Course units"><span class="small-heading">Course outline</span><h2>Explore the units</h2><div class="units">'+renderUnitButtons()+'</div></aside>'+
    '<main id="main" class="main-panel"><section class="card"><span class="small-heading">Unit '+(course.units.indexOf(unit)+1)+'</span><h2 class="unit-title">'+esc(unit.name)+'</h2>'+
    '<p class="subtext">'+(active?'Try the simulator, then practice the underlying mathematics.':'This unit is part of the planned course sequence; activities are not yet available.')+'</p>'+
    '<div class="meta-row"><span class="chip">'+(active?'Working pilot':'Planned')+'</span><span class="chip">CP2 · CP1 · Honors</span></div>'+
    '<div class="skills-list">'+unit.skills.map(s=>'<span class="chip">'+esc(s)+'</span>').join('')+'</div></section>'+
    (active?'<section class="card"><span class="small-heading">Interactive math lab</span><h3>Explore the financial model</h3><p class="subtext">Change the assumptions and observe the consequences.</p>'+simulator()+'</section>'+practice():
    '<section class="card"><div class="planned-card"><h3>Coming later in development</h3><p class="subtext">We will develop questions, simulations, printables, and games for this unit after the three pilot units have been reviewed.</p><button class="primary" data-unit="budgeting">Explore the budgeting pilot</button></div></section>')+
    '</main></div><footer class="footer">Independent Financial Algebra prototype. The live Mr. K’s Classroom repository is not modified.</footer></div>';
}
function printView(mode,unitId,level){
  const unit=getUnit(unitId),q=createWorksheet(unitId,level,6);
  document.title=(mode==='key'?'Teacher Key':'Worksheet')+' — '+unit.name;
  root.innerHTML='<main class="print-sheet"><button class="primary print-button" onclick="window.print()">Print / Save as PDF</button>'+
    '<h1>Financial Algebra — '+esc(unit.name)+'</h1><div class="muted">'+(mode==='key'?'Teacher answer key':'Student worksheet')+' · '+level.toUpperCase()+'</div>'+
    (mode==='key'?'':'<div class="print-name">Name: _________________________________ &nbsp; Date: __________</div>')+
    q.map((item,i)=>'<div class="print-question"><strong>'+String(i+1)+'.</strong> '+esc(item.prompt)+
      (mode==='key'?'<div class="print-key"><strong>Answer: '+esc(money(item.answer))+'</strong><div>'+esc(item.solutionSteps[0])+'</div></div>':
      '<div class="print-line"></div><div class="print-line"></div>')+'</div>').join('')+
    '<p class="note">Calculations use simplified financial models; see the question assumptions.</p></main>';
}
const params=new URLSearchParams(location.search);
if(['worksheet','key'].includes(params.get('print')) && pilotIds.includes(params.get('unit')) && course.levels.includes(params.get('level'))) {
  printView(params.get('print'),params.get('unit'),params.get('level'));
} else {
  render();
  root.addEventListener('click',e=>{
    const unitButton=e.target.closest('[data-unit]');
    if(unitButton){
      const id=unitButton.dataset.unit;
      if(getUnit(id)){state.unitId=id;state.index=0;state.result=null;state.lastAnswer='';location.hash=id;render();}
      return;
    }
    const action=e.target.closest('[data-action]')?.dataset.action;
    if(action==='next'){state.index++;state.result=null;state.lastAnswer='';render();}
    if(action==='worksheet'||action==='key'){
      const url=new URL(location.href);url.hash='';url.search='';
      url.searchParams.set('print',action);url.searchParams.set('unit',state.unitId);url.searchParams.set('level',state.level);
      window.open(url.toString(),'_blank','noopener');
    }
  });
  root.addEventListener('change',e=>{
    if(e.target.id==='level'){state.level=e.target.value;state.index=0;state.result=null;state.lastAnswer='';render();return;}
    const key=e.target.dataset.slider;
    if(key){const group=state[state.unitId];group[key]=Number(e.target.value);render();}
  });
  root.addEventListener('submit',e=>{
    if(e.target.id==='answer-form'){
      e.preventDefault();
      state.lastAnswer=e.target.elements.answer.value;
      state.result=gradeQuestion(makeQuestion(state.unitId,state.level,state.index),state.lastAnswer);
      render();
    }
  });
  window.addEventListener('hashchange',()=>{
    const target=decodeURIComponent(location.hash.slice(1));
    if(getUnit(target)&&target!==state.unitId){state.unitId=target;state.index=0;state.result=null;state.lastAnswer='';render();}
  });
}
