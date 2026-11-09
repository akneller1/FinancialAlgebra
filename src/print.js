import {getUnit} from './course.js';
import {createWorksheet} from './questions.js';
import {creditPayoff,futureValue,fmtMoney} from './engine.js';
const p=new URLSearchParams(location.search);
const unit=getUnit(p.get('unit'))?.status==='pilot'?getUnit(p.get('unit')):getUnit('budgeting');
const kind=p.get('kind')||'explore';
document.getElementById('back').href='index.html#financial-algebra.'+unit.id;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const m=fmtMoney;
const interest=3000*.24/12;
const pay150=creditPayoff({balance:3000,apr:24,payment:150}),pay250=creditPayoff({balance:3000,apr:24,payment:250});
const inv=futureValue({principal:1000,monthly:150,annualRate:6,years:20}),inv10=futureValue({principal:1000,monthly:150,annualRate:6,years:10});
const labs={
 budgeting:{
   title:'Budget Builder',
   questions:[
    'Begin with the default settings. Record monthly income, housing, transportation, essentials, savings, and the unallocated amount. Show the subtraction that produces the unallocated amount.',
    'Increase transportation by $100 without changing anything else. Predict and record the new unallocated amount. Why does the change happen?',
    'A person earning $3,800 take-home wants to save 20%. How much should they set aside? At the default expenses, would that leave a balanced budget?',
    'Make the monthly budget unbalanced, then explain two realistic adjustments that could make it balanced again.',
    'Create a balanced monthly budget with at least $1,000 in savings. Record the amounts you chose and explain one tradeoff you made.'
   ],
   answers:[
    'Default allocations: '+m(3800)+' − '+m(1400)+' − '+m(400)+' − '+m(1000)+' − '+m(600)+' = '+m(400)+' unallocated.',
    'Increasing transportation to $500 leaves '+m(300)+' unallocated, a $100 decrease because income and every other category are unchanged.',
    '20% of $3,800 is $760. Increasing savings from $600 to $760 reduces the $400 remainder to $240, so the default budget remains balanced.',
    'Answers vary. Example: lower housing costs, reduce discretionary spending, reduce transportation costs, or increase income. Any plan must produce a nonnegative remainder.',
    'Answers vary. Verify that income − all four allocations is nonnegative and savings ≥ $1,000; reasoning should explicitly identify a tradeoff.'
   ]
 },
 credit:{
   title:'Debt Repayment Explorer',
   questions:[
    'Use the default settings: a $3,000 card balance, 24% APR, and $150 monthly payment. Calculate the first month’s interest using APR ÷ 12.',
    'At these default settings, how much of the first $150 payment goes toward principal? What is the balance after that payment?',
    'Record the number of months and the total interest paid at the default payment. Then increase the payment to $250. Record both results.',
    'Explain why increasing a monthly payment can save more interest than the difference between the two payments alone would suggest.',
    'Create a repayment plan that finishes in 24 months or less. State your balance, APR, payment, payoff time, and the limitations of the model.'
   ],
   answers:[
    'APR ÷ 12 = 2% per month, so first-month interest is '+m(interest)+'.',
    'Principal reduction = $150 − $60 = $90. New balance = $3,000 − $90 = $2,910.',
    'At $150/month: '+pay150.months+' months and '+m(pay150.interest)+' interest. At $250/month: '+pay250.months+' months and '+m(pay250.interest)+' interest.',
    'Paying additional principal early shrinks the balance on which future interest is charged, so the benefit compounds across future payment periods.',
    'Answers vary. Verify that the payment retires the balance within 24 months under the stated monthly-interest and payment-timing assumptions. Actual cards commonly calculate interest daily.'
   ]
 },
 investing:{
   title:'Compound Growth Explorer',
   questions:[
    'Using the default settings ($1,000 to start, $150 at every month-end, 6% annual return, 20 years), calculate the total dollars you contributed.',
    'Record the simulated ending value after 20 years. How much is investment growth rather than money you contributed?',
    'Change only the years invested from 20 to 10. Record the new ending value. Explain why the difference is more than just 10 years of contributions.',
    'Set the annual return assumption to 0%. Explain what happens to the growth portion of the ending balance.',
    'Create two different contribution/return scenarios with similar ending values. Explain why neither is a prediction of real investment returns.'
   ],
   answers:[
    'Contributions: $1,000 + $150 × (20 × 12) = '+m(inv.contributed)+'.',
    'Ending value: '+m(inv.value)+'. Investment growth: '+m(inv.growth)+'.',
    'At 10 years, ending value: '+m(inv10.value)+'. Earlier deposits in the 20-year plan have more time to earn hypothetical compounded returns.',
    'At 0%, account value equals all contributions; modeled investment growth is zero.',
    'Answers vary. Compare total contributions, duration, and assumed returns. Clearly state that constant annual returns are hypothetical and exclude taxes/fees.'
   ]
 }
};
let html='<section class="fa-paper"><div class="fa-paper-head"><span>MR. K’S CLASSROOM · FINANCIAL ALGEBRA</span><h2>'+esc(unit.name)+'</h2>';
if(kind==='worksheet'||kind==='key'){
 const teacher=kind==='key',data=createWorksheet(unit.id,6);
 html+='<p>'+(teacher?'Teacher key':'Student worksheet · Name: _______________________________ &nbsp; Date: __________')+'</p></div>'+
 data.map((q,i)=>'<article class="fa-paper-item"><strong>'+(i+1)+'. </strong>'+esc(q.prompt)+
 (teacher?'<div class="fa-paper-solution"><strong>Answer: '+esc(m(q.answer))+'</strong><p>'+esc(q.solutionSteps[0])+'</p></div>':
 '<div class="fa-answer-lines"><i></i><i></i></div>')+'</article>').join('');
}else{
 const key=kind==='explore-key';
 const data=labs[unit.id];
 html+='<p>'+esc(data.title)+' · '+(key?'Teacher guide':'Explore & Reflect worksheet')+'</p>'+
 (key?'':'<p>Name: _______________________________ &nbsp; Date: __________</p>')+'</div>'+
 '<p class="fa-paper-foot">Use the matching interactive financial lab. Show calculations, explain relationships, and write conclusions in your own words.</p>'+
 data.questions.map((q,i)=>'<article class="fa-paper-item"><strong>'+(i+1)+'. </strong>'+esc(q)+
 (key?'<div class="fa-paper-solution">'+esc(data.answers[i])+'</div>':'<div class="fa-answer-lines"><i></i><i></i><i></i></div>')+'</article>').join('');
}
html+='<p class="fa-paper-foot">Financial models are simplified for learning. Assumptions about APR, contributions, growth, and payment timing are stated in the activities.</p></section>';
document.getElementById('printRoot').innerHTML=html;
document.title=(kind.includes('key')?'Teacher Key':kind==='worksheet'?'Worksheet':'Explore & Reflect')+' · '+unit.name+' · Financial Algebra';
