import {budgetSummary,creditPayoff,futureValue,fmtMoney} from './engine.js';
const L=window.Lab;
const id=document.getElementById('app').dataset.unit;
const cfg={
 budgeting:{unit:'Budgeting & Spending',title:'Budget Builder',intro:'Make real tradeoffs with monthly income, essentials, transportation, housing, and savings. Observe how one spending decision changes the whole budget.'},
 credit:{unit:'Credit Cards & Debt',title:'Debt Repayment Explorer',intro:'How does a monthly payment affect the total interest paid on a credit card? Change the balance, APR, and payment, then compare the debt payoff curves.'},
 investing:{unit:'Investing & Compound Growth',title:'Compound Growth Explorer',intro:'Explore the relationship between starting capital, monthly deposits, time, and hypothetical investment returns. See what comes from contributions versus growth.'}
}[id];
if(!cfg) throw new Error('Unknown financial lab unit');
const p=L.layout({course:'Financial Algebra',unit:cfg.unit,title:cfg.title,intro:cfg.intro});
const s={
 budgeting:{income:3800,housing:1400,transport:400,essentials:1000,savings:600},
 credit:{balance:3000,apr:24,payment:150},
 investing:{principal:1000,monthly:150,annualRate:6,years:20}
}[id];
const initial={...s};
const fmt=v=>fmtMoney(v);
const panelRead=L.h('div',{class:'readout','aria-live':'polite'},p.panel);
const stageHeading=L.h('h2',{},p.stage,id==='budgeting'?'Where your monthly income goes':id==='credit'?'Credit-card balance over time':'Savings balance over time');
stageHeading.style.margin='6px 10px';
let chart;
if(id==='budgeting'){
 chart=L.s('svg',{viewBox:'0 0 640 380',role:'img','aria-label':'Monthly spending category comparison'},p.stage);
}else{
 chart=L.graph(p.stage,{xmin:0,xmax:24,ymin:0,ymax:4000,width:640,height:390,label:id==='credit'?'Credit card debt declining over time':'Investment account value rising over time'});
}
const legend=L.h('div',{class:'legend'},p.stage);
const table=L.table(p.stage);
L.h('h2',{},p.panel,'Adjust the assumptions');
const sliders=[];
function control(key,label,min,max,step,color,format=fmt){
 sliders.push({key,widget:L.slider(p.panel,{id:key,label,min,max,step,value:s[key],color,format,onInput(value){s[key]=value;redraw();}})});
}
if(id==='budgeting'){
 control('income','Monthly take-home pay',2000,7000,100,'blue');
 control('housing','Housing',700,3500,50,'purple');
 control('transport','Transportation',100,1600,50,'orange');
 control('essentials','Other essentials',300,2200,50,'red');
 control('savings','Savings allocation',0,2000,50,'green');
}else if(id==='credit'){
 control('balance','Initial card balance',1000,6000,100,'purple');
 control('apr','APR',12,30,1,'orange',v=>v+'%');
 control('payment','Monthly payment',100,500,10,'green');
}else{
 control('principal','Starting investment',0,10000,500,'purple');
 control('monthly','Monthly contribution',0,600,25,'blue');
 control('annualRate','Hypothetical annual return',0,10,1,'orange',v=>v+'%');
 control('years','Years invested',1,40,1,'green',v=>v+' years');
}
const controls=L.h('div',{class:'btn-row'},p.panel);
L.button(controls,'Reset',()=>{
 Object.assign(s,initial);
 sliders.forEach(({key,widget})=>widget.set(s[key],true));
 redraw();
},true);
const feedback=L.h('p',{class:'note','aria-live':'polite'},p.panel);
const seen={};
const challenges=id==='budgeting'?[
 {text:'Build a monthly budget with at least $1,000 left after all allocations.',check:()=>seen.surplus},
 {text:'Save at least 20% of take-home pay while staying within your budget.',check:()=>seen.savings20},
 {text:'Create a budget deficit. Which expense could you change first?',check:()=>seen.deficit},
 {text:'Keep housing at or below $1,000 and save at least $600.',check:()=>seen.housing},
 {text:'Make an affordable plan with at least $1,000 allocated to savings.',check:()=>seen.save1000}
]:id==='credit'?[
 {text:'Pay off the balance in 24 months or less.',check:()=>seen.fast},
 {text:'Save at least $300 in interest compared with paying $100 per month.',check:()=>seen.save300},
 {text:'Find a payment with less than $200 total interest.',check:()=>seen.lowinterest},
 {text:'Try an APR of 30%. What happens to interest when the payment stays the same?',check:()=>seen.highapr},
 {text:'Find a plan that pays off the balance within 12 months.',check:()=>seen.oneYear}
]:[
 {text:'Set the return to 0%. What happens to growth?',check:()=>seen.zero},
 {text:'Make investment growth exceed your own contributions.',check:()=>seen.growth},
 {text:'Find settings that produce an ending account value of at least $100,000.',check:()=>seen.large},
 {text:'Explore investing for at least 35 years. What changes compared with 10?',check:()=>seen.long},
 {text:'Keep the return at 5% or less and still reach at least $50,000.',check:()=>seen.conservative}
];
// Use a syntax-safe key for the six-figure challenge.
challenges[2].check= id==='investing'?()=>seen.large:challenges[2].check;
const tasks=L.challenges(p.panel,challenges);
const links=L.h('div',{class:'box'},p.below,
 '<h2 style="margin:0 0 8px">Explore &amp; Reflect</h2>'+
 '<p style="margin:0 0 12px;color:var(--ink-soft)">As on the other Interactive Math pages, use the printable reflection worksheet and its teacher guide while investigating the model.</p>'+
 '<div class="btn-row"><a class="btn" href="../../print.html?kind=explore&unit='+id+'">Printable exploration</a>'+
 '<a class="btn ghost" href="../../print.html?kind=explore-key&unit='+id+'">Teacher key</a>'+
 '<a class="btn ghost" href="../../index.html#financial-algebra.'+id+'">Back to unit</a></div>');
const details=L.h('details',{class:'box'},p.below);
L.h('summary',{style:'cursor:pointer;font-family:var(--display);font-weight:800'},details,'What should I notice?');
L.h('div',{},details,id==='budgeting'?
 '<p>Remaining money equals take-home pay minus every spending and saving allocation. A plan is balanced when the remainder is zero or greater. Saving is part of the budget, not an expense paid to someone else.</p><p>Look for tradeoffs: changing a housing cost by $100 changes the remainder by exactly $100, all else fixed.</p>':
 id==='credit'?
 '<p>More of each payment goes to principal as the balance shrinks. Paying more usually shortens payoff time and reduces total interest. The APR is annual, so the monthly rate in this simplified model is APR ÷ 12.</p><p>Real card issuers commonly calculate interest on daily balances; this is a teaching model with monthly compounding and month-end payments.</p>':
 '<p>Ending savings equals your contributions plus investment growth. Money deposited earlier has more time to compound. Monthly contributions occur at the end of each month in this model.</p><p>Constant returns are an assumption for isolating the mathematics, not a prediction. Market returns vary and can be negative.</p>');
function budgetChart(){
 const r=budgetSummary(s);
 chart.innerHTML='';
 const categories=[['Housing',s.housing,'purple'],['Transport',s.transport,'orange'],['Other essentials',s.essentials,'red'],['Savings',s.savings,'green'],['Unallocated',Math.max(0,r.remaining),'blue']];
 const total=Math.max(s.income,r.spent);
 const scale=total>0?510/total:1;
 L.s('text',{x:38,y:32,class:'g-label','font-size':17},chart).textContent='Total monthly income: '+fmt(s.income);
 let x=38;
 categories.forEach(([label,value,color])=>{
   if(!value)return;
   const w=value*scale;
   L.s('rect',{x,y:56,width:w,height:58,fill:'var(--'+color+')',opacity:.8,stroke:'var(--ink)','stroke-width':1},chart);
   x+=w;
 });
 L.s('rect',{x:38,y:56,width:510,height:58,fill:'none',stroke:'var(--ink)','stroke-width':2},chart);
 if(r.remaining<0){
  L.s('text',{x:38,y:145,fill:'var(--red)',class:'g-label'},chart).textContent='Deficit: '+fmt(-r.remaining)+' over your income';
 }
 categories.forEach(([label,value,color],i)=>{
  const y=185+i*37;
  L.s('rect',{x:38,y:y-15,width:22,height:18,fill:'var(--'+color+')',stroke:'var(--ink)','stroke-width':1},chart);
  L.s('text',{x:72,y,class:'g-label','font-size':15},chart).textContent=label+' — '+fmt(value);
 });
 table.set(['Allocation','Monthly amount','Share of income'],[
 ['Housing',fmt(s.housing),(100*s.housing/s.income).toFixed(1)+'%'],
 ['Transportation',fmt(s.transport),(100*s.transport/s.income).toFixed(1)+'%'],
 ['Essentials',fmt(s.essentials),(100*s.essentials/s.income).toFixed(1)+'%'],
 ['Savings',fmt(s.savings),(100*s.savings/s.income).toFixed(1)+'%']
 ]);
 panelRead.innerHTML='Remaining: <b>'+fmt(r.remaining)+'</b><div class="sub">Savings rate: '+(r.savingsRate*100).toFixed(1)+'%</div>';
 feedback.innerHTML=r.balanced?'✓ Your planned allocations fit your take-home income.':'⚠ Planned allocations exceed take-home income. Which expense could be adjusted?';
 if(r.remaining>=1000)seen.surplus=true;
 if(r.savingsRate>=.2&&r.balanced)seen.savings20=true;
 if(!r.balanced)seen.deficit=true;
 if(s.housing<=1000&&s.savings>=600)seen.housing=true;
 if(s.savings>=1000&&r.balanced)seen.save1000=true;
}
function creditChart(){
 const r=creditPayoff(s),baseline=creditPayoff({...s,payment:100});
 const history=[{month:0,balance:s.balance},...r.history];
 const maxX=Math.max(12,r.months||120);
 chart.clear();chart.setView({xmin:0,xmax:maxX,ymin:0,ymax:Math.max(1500,s.balance*1.08)});
 for(let k=1;k<history.length;k++) chart.line(history[k-1].month,history[k-1].balance,history[k].month,history[k].balance,{color:'purple',width:4});
 chart.dot(0,s.balance,{color:'purple',r:5});
 if(r.paidOff)chart.dot(r.months,0,{color:'green',r:7});
 legend.innerHTML='<span><i style="background:var(--purple)"></i>Remaining balance after each payment</span>';
 table.set(['Measure','Value'],[
 ['Payoff time',r.paidOff?r.months+' months':'Not paid off'],
 ['Total interest',r.paidOff?fmt(r.interest):'N/A'],
 ['Total paid',r.paidOff?fmt(r.totalPaid):'N/A'],
 ['Interest saved vs $100/month',(r.paidOff&&baseline.paidOff)?fmt(Math.max(0,baseline.interest-r.interest)):'N/A']
 ]);
 panelRead.innerHTML=r.paidOff?'<b>'+r.months+' months</b> to pay off<div class="sub">'+fmt(r.interest)+' total interest</div>':'The balance does not reach zero under these assumptions.';
 feedback.innerHTML='Monthly interest is '+s.apr+'% ÷ 12 = '+(s.apr/12).toFixed(2)+'% of the current balance before each payment.';
 if(r.paidOff&&r.months<=24)seen.fast=true;
 if(r.paidOff&&baseline.paidOff&&baseline.interest-r.interest>=300)seen.save300=true;
 if(r.paidOff&&r.interest<200)seen.lowinterest=true;
 if(s.apr===30)seen.highapr=true;
 if(r.paidOff&&r.months<=12)seen.oneYear=true;
}
function investChart(){
 const r=futureValue(s),h=r.history;
 chart.clear();chart.setView({xmin:0,xmax:Math.max(2,s.years),ymin:0,ymax:Math.max(1000,Math.ceil(r.value*1.1/1000)*1000)});
 let prev={month:0,value:s.principal},pc=s.principal;
 for(let k=1;k<h.length;k++){
  const p=h[k],a=prev.month/12,b=p.month/12;
  const contributionA=s.principal+s.monthly*prev.month,contributionB=s.principal+s.monthly*p.month;
  chart.line(a,prev.value,b,p.value,{color:'blue',width:4});
  chart.line(a,contributionA,b,contributionB,{color:'orange',width:2,dash:'6 5'});
  prev=p;pc=contributionB;
 }
 chart.dot(s.years,r.value,{color:'green',r:7});
 legend.innerHTML='<span><i style="background:var(--blue)"></i>Total account value</span><span><i style="background:var(--orange)"></i>Contributed money (dashed)</span>';
 table.set(['Measure','Value'],[
 ['Ending value',fmt(r.value)],['Total contributions',fmt(r.contributed)],['Investment growth',fmt(r.growth)],['Assumed annual return',s.annualRate+'% (hypothetical)']
 ]);
 panelRead.innerHTML='<b>'+fmt(r.value)+'</b><div class="sub">Growth: '+fmt(r.growth)+' · Contributions: '+fmt(r.contributed)+'</div>';
 feedback.innerHTML='This is a fixed-rate model, not a market forecast. It excludes investment fees, taxes, and inflation.';
 if(s.annualRate===0)seen.zero=true;
 if(r.growth>r.contributed)seen.growth=true;
 if(r.value>=100000)seen.large=true;
 if(s.years>=35)seen.long=true;
 if(s.annualRate<=5&&r.value>=50000)seen.conservative=true;
}
function redraw(){
 if(id==='budgeting')budgetChart();
 if(id==='credit')creditChart();
 if(id==='investing')investChart();
 tasks.update();
}
redraw();
