// Pure, deterministic financial math; no live financial feeds or AI calls.
export function roundMoney(value) {
  if (!Number.isFinite(value)) throw new RangeError('Expected finite amount');
  return Math.round((value + Number.EPSILON) * 100) / 100;
}
function nonnegative(value,label) {
  if (!Number.isFinite(value) || value < 0) throw new RangeError(label+' must be a nonnegative finite number');
}
export function budgetSummary({income,housing,transport,essentials,savings}) {
  for(const [key,val] of Object.entries({income,housing,transport,essentials,savings})) nonnegative(val,key);
  const spent=roundMoney(housing+transport+essentials+savings);
  const remaining=roundMoney(income-spent);
  return {income,spent,remaining,savingsRate:income ? savings/income : 0,balanced:remaining>=0};
}
export function creditPayoff({balance,apr,payment,maxMonths=1200}) {
  nonnegative(balance,'balance'); nonnegative(apr,'APR'); nonnegative(payment,'payment');
  if (!Number.isInteger(maxMonths)||maxMonths<1) throw new RangeError('Invalid maximum months');
  if(balance===0) return {paidOff:true,months:0,interest:0,totalPaid:0,history:[]};
  const rate=apr/1200;
  const history=[];
  let debt=roundMoney(balance), totalInterest=0, totalPaid=0;
  if(payment<=roundMoney(debt*rate)) return {paidOff:false,months:null,interest:null,totalPaid:null,history:[]};
  for(let month=1;month<=maxMonths;month++){
    const interest=roundMoney(debt*rate);
    const due=roundMoney(debt+interest);
    const paid=roundMoney(Math.min(payment,due));
    debt=roundMoney(due-paid);
    totalInterest=roundMoney(totalInterest+interest);
    totalPaid=roundMoney(totalPaid+paid);
    history.push({month,interest,payment:paid,balance:debt});
    if(debt===0) return {paidOff:true,months:month,interest:totalInterest,totalPaid,history};
  }
  return {paidOff:false,months:null,interest:null,totalPaid:null,history};
}
export function futureValue({principal,monthly,annualRate,years}) {
  nonnegative(principal,'principal'); nonnegative(monthly,'monthly');
  nonnegative(annualRate,'annualRate'); nonnegative(years,'years');
  if (!Number.isInteger(years*12)||years>80) throw new RangeError('Years must be whole months and at most 80');
  const months=Math.round(years*12), monthlyRate=annualRate/1200;
  let balance=principal;
  const history=[{month:0,value:roundMoney(principal)}];
  // Monthly contribution occurs at each month-end, after growth.
  for(let month=1;month<=months;month++) {
    balance=balance*(1+monthlyRate)+monthly;
    if(month%12===0 || month===months) history.push({month,value:roundMoney(balance)});
  }
  const contributed=roundMoney(principal+monthly*months);
  const value=roundMoney(balance);
  return {value,contributed,growth:roundMoney(value-contributed),history};
}
export function fmtMoney(value) {
  return new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:2}).format(value);
}
