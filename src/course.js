export const course = {
  id: 'financial-algebra',
  name: 'Financial Algebra',
  subtitle: 'Learn the mathematics behind real financial decisions.',
  levels: ['standard'],
  units: [
    {id:'income', name:'Careers & Income', status:'planned', skills:['Compare salary and hourly pay','Calculate gross and net income','Interpret pay stubs','Model income taxes']},
    {id:'budgeting', name:'Budgeting & Spending', status:'pilot', skills:['Calculate monthly cash flow','Analyze fixed and variable expenses','Model financial constraints','Compare spending decisions']},
    {id:'banking', name:'Banking & Saving', status:'planned', skills:['Understand account fees','Calculate simple interest','Compare savings products','Interpret bank statements']},
    {id:'credit', name:'Credit Cards & Debt', status:'pilot', skills:['Calculate monthly interest','Evaluate credit card repayment','Compare repayment strategies','Interpret credit costs']},
    {id:'borrowing', name:'Auto Loans & Borrowing', status:'planned', skills:['Model installment loans','Compare APR and loan term','Build amortization schedules','Analyze total borrowing cost']},
    {id:'investing', name:'Investing & Compound Growth', status:'pilot', skills:['Calculate compound growth','Model recurring contributions','Compare investment scenarios','Interpret investment risk']},
    {id:'housing', name:'Housing: Rent or Buy', status:'planned', skills:['Compare rental and ownership costs','Model a mortgage','Estimate ownership expenses','Analyze opportunity cost']},
    {id:'insurance', name:'Insurance & Risk', status:'planned', skills:['Compare premiums and deductibles','Model out-of-pocket costs','Calculate expected value','Evaluate financial risk']},
    {id:'college', name:'College & Career ROI', status:'planned', skills:['Estimate education costs','Model student loan payments','Compare career earnings','Analyze payback periods']},
    {id:'retirement', name:'Retirement & Inflation', status:'planned', skills:['Model inflation','Estimate retirement savings','Compare account contributions','Analyze purchasing power']}
  ]
};
export function getUnit(id){return course.units.find(unit=>unit.id===id);}
export function getSkillRecords(unitId){
  const unit=getUnit(unitId);
  return unit?unit.skills.map((name,i)=>({id:unitId+'-skill-'+String(i+1).padStart(2,'0'),name,index:i+1})):[];
}
