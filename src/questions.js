import {budgetSummary,creditPayoff,futureValue,roundMoney,fmtMoney} from './engine.js';
import {getUnit} from './course.js';
// Repeatable item variants for independent practice, worksheets, and test fixtures.
export function makeQuestion(unitId,level='cp1',index=0) {
  const unit=getUnit(unitId);
  if(!unit || unit.status!=='pilot') throw new RangeError('Unit has no pilot question bank');
  if(!['cp2','cp1','honors'].includes(level)) throw new RangeError('Unknown difficulty');
  if(!Number.isInteger(index)||index<0) throw new RangeError('Invalid item index');
  const n=index%12, t=Math.floor(index/12);
  let prompt, answer, solution, skill=0, type='money';
  const lift=(n*37+t*19);
  if(unitId==='budgeting') {
    if(level==='cp2') {
      const income=2600+100*lift, rent=850+20*n, transport=180+10*n, essentials=620+5*n;
      answer=roundMoney(income-rent-transport-essentials);
      prompt='Your monthly take-home pay is '+fmtMoney(income)+'. Rent is '+fmtMoney(rent)+', transportation is '+fmtMoney(transport)+', and other essentials cost '+fmtMoney(essentials)+'. How much remains for savings and optional spending?';
      solution='Take-home pay minus monthly expenses: '+fmtMoney(income)+' − '+fmtMoney(rent)+' − '+fmtMoney(transport)+' − '+fmtMoney(essentials)+' = '+fmtMoney(answer)+'.';
      skill=1;
    } else if(level==='cp1') {
      const gross=3700+100*lift, withholding=.18, rent=1150+15*n, other=1050+10*n;
      const net=roundMoney(gross*(1-withholding));
      answer=roundMoney(net-rent-other);
      prompt='Monthly gross earnings are '+fmtMoney(gross)+'. Assume a flat 18% combined withholding (a simplified model). Rent is '+fmtMoney(rent)+' and all other expenses total '+fmtMoney(other)+'. What is the monthly amount left after withholding and expenses?';
      solution='Estimated net pay = '+fmtMoney(gross)+' × 0.82 = '+fmtMoney(net)+'. Remaining = '+fmtMoney(net)+' − '+fmtMoney(rent)+' − '+fmtMoney(other)+' = '+fmtMoney(answer)+'.';
      skill=2;
    } else {
      const income=4600+100*lift, housing=1850+20*n, other=1550+15*n, savingsRate=.2;
      const target=roundMoney(income*savingsRate);
      answer=roundMoney(income-housing-other-target);
      prompt='You take home '+fmtMoney(income)+' monthly and want to save 20% of that amount. Housing is '+fmtMoney(housing)+' and essential expenses total '+fmtMoney(other)+'. What is the maximum additional discretionary spending per month while meeting your savings target?';
      solution='Savings target = 20% × '+fmtMoney(income)+' = '+fmtMoney(target)+'. Max discretionary spending = '+fmtMoney(income)+' − '+fmtMoney(housing)+' − '+fmtMoney(other)+' − '+fmtMoney(target)+' = '+fmtMoney(answer)+'.';
      skill=3;
    }
  } else if(unitId==='credit') {
    const balance=800+100*lift, apr=18+(n%4)*2;
    if(level==='cp2') {
      answer=roundMoney(balance*apr/1200);
      prompt='A card carries a '+fmtMoney(balance)+' balance at '+apr+'% APR. Assuming monthly interest equals balance × APR ÷ 12 and no other transactions, how much interest accrues in one month?';
      solution=fmtMoney(balance)+' × '+apr+'% ÷ 12 = '+fmtMoney(answer)+'. This is a simplified monthly-interest model; real cards commonly use daily balance methods.';
      skill=1;
    } else if(level==='cp1') {
      const payment=80+10*(n%5), result=creditPayoff({balance,apr,payment});
      answer=result.interest;
      prompt='You owe '+fmtMoney(balance)+' at '+apr+'% APR, compounded monthly. You pay '+fmtMoney(payment)+' at each month-end with no new purchases. What is the total interest paid until the balance reaches zero? Round to cents.';
      solution='Apply monthly interest (APR ÷ 12) to the remaining balance, then subtract the payment each month. The balance reaches zero after '+result.months+' payments. Total interest = '+fmtMoney(result.interest)+'.';
      skill=2;
    } else {
      const slow=75+10*(n%4), fast=slow+60;
      const a=creditPayoff({balance,apr,payment:slow}), b=creditPayoff({balance,apr,payment:fast});
      answer=roundMoney(a.interest-b.interest);
      prompt='You owe '+fmtMoney(balance)+' at '+apr+'% APR with monthly compounding and no new purchases. Compare paying '+fmtMoney(slow)+'/month with '+fmtMoney(fast)+'/month. How much total interest is saved by choosing the larger payment?';
      solution='The smaller payment produces '+fmtMoney(a.interest)+' interest over '+a.months+' months. The larger payment produces '+fmtMoney(b.interest)+' over '+b.months+' months. Savings = '+fmtMoney(answer)+'.';
      skill=3;
    }
  } else if(unitId==='investing') {
    const principal=1000+200*n, annualRate=4+(n%5), years=5+(n%6);
    if(level==='cp2') {
      const result=futureValue({principal,monthly:0,annualRate,years});
      answer=result.value;
      prompt='You invest '+fmtMoney(principal)+' for '+years+' years, assuming a constant '+annualRate+'% annual return compounded monthly. With no new contributions, what is the final balance?';
      solution='Use '+fmtMoney(principal)+' × (1 + '+annualRate+'% ÷ 12)^('+12*years+') = '+fmtMoney(answer)+'. Returns are hypothetical, not guaranteed.';
      skill=1;
    } else if(level==='cp1') {
      const monthly=75+10*(n%7);
      const result=futureValue({principal,monthly,annualRate,years});
      answer=result.growth;
      prompt='You start with '+fmtMoney(principal)+' and contribute '+fmtMoney(monthly)+' at every month-end for '+years+' years. Assume a constant '+annualRate+'% annual return compounded monthly. How much of your ending balance is investment growth rather than your own contributions?';
      solution='Future balance = '+fmtMoney(result.value)+'. Contributions = '+fmtMoney(result.contributed)+'. Growth = '+fmtMoney(result.value)+' − '+fmtMoney(result.contributed)+' = '+fmtMoney(answer)+'.';
      skill=2;
    } else {
      const monthly=100+20*(n%5);
      const regular=futureValue({principal,monthly,annualRate,years});
      const delayed=futureValue({principal,monthly,annualRate,years:Math.max(years-2,1)});
      const postponed=futureValue({principal:delayed.value,monthly:0,annualRate,years:2});
      answer=roundMoney(regular.value-postponed.value);
      prompt='You have '+fmtMoney(principal)+' invested. Plan A adds '+fmtMoney(monthly)+' at each month-end for '+years+' years. Plan B adds the same monthly amount for the first '+(years-2)+' years, then makes no further contributions for the final 2 years. Both assume '+annualRate+'% annual return compounded monthly. How much larger is Plan A’s final balance?';
      solution='Plan A ends at '+fmtMoney(regular.value)+'. Plan B ends at approximately '+fmtMoney(postponed.value)+'. Difference = '+fmtMoney(answer)+'. Small rounding differences may occur when modeling intermediate balances.';
      skill=3;
    }
  }
  if(!Number.isFinite(answer)) throw new Error('Invalid generated answer');
  return {id:'fa-'+unitId+'-'+level+'-'+index,courseId:'financial-algebra',unitId,level,skillId:unitId+'-skill-'+String(skill).padStart(2,'0'),format:'short-answer',prompt,answer,solutionSteps:[solution],tolerance:.02,answerType:type};
}
export function gradeQuestion(question,response) {
  const n=Number(response);
  if(String(response).trim()==='' || !Number.isFinite(n)) return {valid:false,correct:false};
  return {valid:true,correct:Math.abs(n-question.answer)<=question.tolerance};
}
export function createWorksheet(unitId,level,count=6) {
  if(!Number.isInteger(count)||count<1||count>30) throw new RangeError('Worksheet count must be 1–30');
  return Array.from({length:count},(_,i)=>makeQuestion(unitId,level,i));
}
