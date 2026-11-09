import {creditPayoff,futureValue,roundMoney,fmtMoney} from './engine.js';
import {getUnit} from './course.js';

// One common Financial Algebra level. These families vary context and reasoning, not grade tier.
// All numeric answers are calculated from the same deterministic math as the simulations.
export function makeQuestion(unitId,index=0) {
  const unit=getUnit(unitId);
  if(!unit||unit.status!=='pilot') throw new RangeError('Unit has no pilot questions');
  if(!Number.isInteger(index)||index<0) throw new RangeError('Question index must be nonnegative integer');
  const family=index%3, variant=Math.floor(index/3)%30, cycle=Math.floor(index/90);
  const n=variant+cycle*7;
  let prompt,answer,solution,skill;
  const dollars=fmtMoney;
  if(unitId==='budgeting'){
    if(family===0){
      const income=3000+120*n, rent=1050+15*n, transport=280+5*n, essentials=850+10*n;
      answer=roundMoney(income-rent-transport-essentials);
      prompt='You earn '+dollars(income)+' in monthly take-home pay. Your rent is '+dollars(rent)+', transportation costs '+dollars(transport)+', and food, utilities, and other essentials total '+dollars(essentials)+'. How much money remains for savings or discretionary spending this month?';
      solution='Remaining money = income − rent − transportation − essentials = '+dollars(income)+' − '+dollars(rent)+' − '+dollars(transport)+' − '+dollars(essentials)+' = '+dollars(answer)+'.';
      skill=1;
    }else if(family===1){
      const income=3600+100*n, savingsPct=15+(n%4)*5;
      answer=roundMoney(income*savingsPct/100);
      prompt='Your monthly take-home pay is '+dollars(income)+'. You decide to save '+savingsPct+'% of that amount before paying for optional purchases. How much should you set aside for savings each month?';
      solution='Monthly savings = '+dollars(income)+' × '+savingsPct+'% = '+dollars(answer)+'. A savings target is an allocation, not an additional income source.';
      skill=2;
    }else{
      const income=3950+100*n, fixed=2150+20*n, variable=920+5*n, emergency=150+15*(n%6);
      answer=roundMoney(income-fixed-variable-emergency);
      prompt='Your take-home pay is '+dollars(income)+'. Fixed expenses are '+dollars(fixed)+', variable expenses are '+dollars(variable)+', and an unexpected repair costs '+dollars(emergency)+'. How much remains after all three expenses this month?';
      solution='Net cash flow = '+dollars(income)+' − '+dollars(fixed)+' − '+dollars(variable)+' − '+dollars(emergency)+' = '+dollars(answer)+'.';
      skill=3;
    }
  }else if(unitId==='credit'){
    const balance=900+70*n, apr=18+2*(n%6);
    if(family===0){
      answer=roundMoney(balance*apr/1200);
      prompt='A credit-card account has a balance of '+dollars(balance)+' at '+apr+'% APR. In this simplified model, interest is charged once each month at APR ÷ 12, with no new purchases. How much interest accrues in the first month?';
      solution='Monthly interest = '+dollars(balance)+' × ('+apr+'% ÷ 12) = '+dollars(answer)+'. Real cards often use daily balance methods.';
      skill=1;
    }else if(family===1){
      const payment=110+10*(n%7);
      const r=creditPayoff({balance,apr,payment});
      if(!r.paidOff) throw new Error('Unpayable scenario');
      answer=r.interest;
      prompt='You owe '+dollars(balance)+' at '+apr+'% APR, compounded monthly. There are no new purchases. You pay '+dollars(payment)+' at the end of each month, with a smaller final payment if needed. What is the total interest paid before the balance reaches zero?';
      solution='For each month, calculate interest on the current balance at '+apr+'% ÷ 12, then subtract the payment. The debt is paid in '+r.months+' months. Sum of monthly interest = '+dollars(answer)+'.';
      skill=2;
    }else{
      const slow=95+10*(n%5),fast=slow+75;
      const s=creditPayoff({balance,apr,payment:slow}),f=creditPayoff({balance,apr,payment:fast});
      if(!s.paidOff||!f.paidOff) throw new Error('Unpayable comparison');
      answer=roundMoney(s.interest-f.interest);
      prompt='A '+dollars(balance)+' balance has '+apr+'% APR compounded monthly, with no new purchases. Compare paying '+dollars(slow)+' per month with '+dollars(fast)+' per month. How much interest would the higher-payment strategy save over the full payoff period?';
      solution='Interest with '+dollars(slow)+' payments: '+dollars(s.interest)+'. Interest with '+dollars(fast)+' payments: '+dollars(f.interest)+'. Savings = '+dollars(answer)+'.';
      skill=3;
    }
  }else if(unitId==='investing'){
    const principal=1000+200*(n%16),rate=4+(n%6),years=6+(n%10);
    if(family===0){
      const r=futureValue({principal,monthly:0,annualRate:rate,years});
      answer=r.value;
      prompt='You invest '+dollars(principal)+' for '+years+' years. Assume, only for this exercise, a constant '+rate+'% annual return compounded monthly and no additional contributions. What is the ending balance? Round to the nearest cent.';
      solution='Future value = '+dollars(principal)+' × (1 + '+rate+'% ÷ 12)^('+years+' × 12) = '+dollars(answer)+'. Actual returns vary and are not guaranteed.';
      skill=1;
    }else if(family===1){
      const monthly=100+25*(n%7),r=futureValue({principal,monthly,annualRate:rate,years});
      answer=r.growth;
      prompt='You begin with '+dollars(principal)+' and add '+dollars(monthly)+' at each month-end for '+years+' years. Assume a hypothetical constant '+rate+'% annual return compounded monthly. How much of the ending account value comes from investment growth, rather than your own contributions?';
      solution='Ending value = '+dollars(r.value)+'. Contributions = '+dollars(r.contributed)+'. Growth = ending value − contributions = '+dollars(answer)+'.';
      skill=2;
    }else{
      const baseMonthly=100+20*(n%6),a=futureValue({principal,monthly:baseMonthly,annualRate:rate,years});
      const b=futureValue({principal,monthly:baseMonthly+50,annualRate:rate,years});
      answer=roundMoney(b.value-a.value);
      prompt='Two savers both start with '+dollars(principal)+' and invest for '+years+' years at a hypothetical constant '+rate+'% annual return compounded monthly. One contributes '+dollars(baseMonthly)+' at each month-end; the other contributes '+dollars(baseMonthly+50)+'. How much larger is the second saver’s ending balance?';
      solution='First plan ends at '+dollars(a.value)+'. Second plan ends at '+dollars(b.value)+'. Difference = '+dollars(answer)+'. More contributions and their growth explain the difference.';
      skill=3;
    }
  }
  if(!Number.isFinite(answer)) throw new Error('Invalid generated answer');
  return {id:'fa-'+unitId+'-'+index,courseId:'financial-algebra',unitId,skillId:unitId+'-skill-'+String(skill).padStart(2,'0'),format:'short-answer',prompt,answer,solutionSteps:[solution],tolerance:.02,answerType:'money'};
}
export function gradeQuestion(question,response){
  if(response==null||String(response).trim()==='') return {valid:false,correct:false};
  const n=Number(response);
  return Number.isFinite(n)?{valid:true,correct:Math.abs(n-question.answer)<=question.tolerance}:{valid:false,correct:false};
}
export function createWorksheet(unitId,count=6,start=0){
  if(!Number.isInteger(count)||count<1||count>30) throw new RangeError('Question count must be 1–30');
  if(!Number.isInteger(start)||start<0) throw new RangeError('Invalid starting question');
  return Array.from({length:count},(_,i)=>makeQuestion(unitId,start+i));
}
