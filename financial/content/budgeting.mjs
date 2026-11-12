import { sheets } from './cheat-sheets.mjs';
/* Unit 2 — Budgeting & Spending (reference unit). */
import { M, money, $, $0, pct, person, TOWNS, JOBS, mc, selectAll, numeric, table, an } from './kit.mjs';

const SALES_TAX = 0.0625; // fictional state sales tax used throughout the course (matches the MA rate)
const EXP = {
  rent: [[750, 'Rent (shared apartment)'], [1150, 'Rent (studio)'], [1325, 'Rent (1-bedroom)'], [1480, 'Rent (1-bedroom)']],
  util: [95, 120, 145], phone: [45, 60, 80], carPay: [0, 285, 340, 395], carIns: [115, 145, 180], gas: [120, 150, 185],
  groc: [290, 340, 395], dining: [90, 160, 240], subs: [28, 42, 61], loan: [0, 190, 245, 310], fun: [60, 110, 160]
};
function budgetFor(r, net) {
  const rent = r.pick(EXP.rent), carPay = r.pick(EXP.carPay);
  const rows = [[rent[1], rent[0]], ['Utilities & internet', r.pick(EXP.util)], ['Phone', r.pick(EXP.phone)]];
  if (carPay) rows.push(['Car payment', carPay], ['Car insurance', r.pick(EXP.carIns)], ['Gas', r.pick(EXP.gas)]);
  else rows.push(['Transit pass', 90]);
  rows.push(['Groceries', r.pick(EXP.groc)], ['Dining out', r.pick(EXP.dining)], ['Streaming & apps', r.pick(EXP.subs)]);
  const loan = r.pick(EXP.loan); if (loan) rows.push(['Student loan', loan]);
  rows.push(['Entertainment', r.pick(EXP.fun)]);
  return rows;
}
const total = rows => rows.reduce((s, x) => s + x[1], 0);

export default {
  id: 'budgeting',
  vocab: [
    { term: 'Budget', skill: 1, def: 'A plan that assigns expected income to spending, saving, and debt payments for a period of time', example: 'Ana plans $1,200 for rent, $350 for groceries, and $200 for savings from her $2,600 monthly take-home pay.', mis: 'A budget is a restriction rather than a plan you control.' },
    { term: 'Cash flow', skill: 1, def: 'Money coming in minus money going out during a period', example: 'Income of $2,900 and expenses of $3,050 produce a −$150 monthly result.' },
    { term: 'Surplus', skill: 1, def: 'The amount left over when income is greater than expenses', example: 'After every bill is paid, Theo has $240 left this month.' },
    { term: 'Deficit', skill: 1, def: 'The shortfall when expenses are greater than income', example: 'Expenses of $2,480 against income of $2,300 leave a $180 gap covered by a credit card.' },
    { term: 'Net income (take-home pay)', skill: 1, def: 'Pay remaining after taxes and other deductions; the amount a budget should be built on', example: 'A $1,650 biweekly gross check becomes a $1,282 deposit after withholding.', mis: 'Students often budget with gross pay, overstating what they can spend.' },
    { term: 'Sinking fund', skill: 1, def: 'Money set aside each month for a known, irregular future expense', example: 'Saving $90 a month so a $1,080 annual car-insurance bill is already covered when it arrives.' },
    { term: 'Fixed expense', skill: 2, def: 'A cost that stays the same amount each period', example: 'A $1,325 rent payment that is identical every month under a lease.' },
    { term: 'Variable expense', skill: 2, def: 'A cost whose amount changes from period to period', example: 'Grocery spending of $312, $367, and $341 in three consecutive months.' },
    { term: 'Discretionary expense', skill: 2, def: 'Spending on wants that could be reduced or eliminated without affecting basic needs', example: 'Concert tickets, takeout meals, and a second streaming service.' },
    { term: 'Essential expense (need)', skill: 2, def: 'Spending required for basic living or to keep earning income', example: 'Rent, basic groceries, utilities, and transportation to work.' },
    { term: '50/30/20 guideline', skill: 2, def: 'A starting-point plan that directs about 50% of take-home pay to needs, 30% to wants, and 20% to savings and extra debt payments', example: 'With $3,000 take-home pay: about $1,500 needs, $900 wants, $600 savings.', mis: 'It is a rule everyone must follow; in high-cost areas needs often exceed 50%.' },
    { term: 'Emergency fund', skill: 3, def: 'Savings reserved for unexpected expenses or income loss, often targeted at 3–6 months of essential expenses', example: 'Keeping $6,600 in savings when essential expenses are $2,200 per month (3 months).' },
    { term: 'Financial constraint', skill: 3, def: 'A limit, such as income or a savings target, that restricts which spending choices are possible', example: 'Rent must be at most 30% of gross income: r ≤ 0.30 × 4,000.' },
    { term: 'Savings goal', skill: 3, def: 'A specific amount of money to accumulate by a target date', example: '$2,400 for a used-car down payment within 12 months requires $200 per month.' },
    { term: 'Opportunity cost', skill: 4, def: 'The value of the next-best alternative given up when making a choice', example: 'Spending $1,200 a year on takeout lunches means not putting that $1,200 toward an emergency fund.', mis: 'Opportunity cost is only money; it can also be time or flexibility.' },
    { term: 'Unit price', skill: 4, def: 'The cost per single unit (ounce, item, load) used to compare package sizes fairly', example: '$8.99 for 24 oz is about $0.375 per ounce.' },
    { term: 'Impulse purchase', skill: 4, def: 'An unplanned purchase made on the spot, often influenced by marketing or emotion', example: 'Buying a $45 gadget near the checkout that was not on the list.' },
    { term: 'Buy now, pay later (BNPL)', skill: 4, def: 'A short-term financing plan that splits a purchase into installments, sometimes with late fees or interest', example: 'A $240 jacket paid in four $60 installments every two weeks.', mis: 'BNPL is “free money”; missed payments can add fees and stack up across several plans.' },
    { term: 'Sales tax', skill: 4, def: 'A percent of the purchase price collected by the state at the time of sale', example: 'A $40 item with 6.25% sales tax costs $42.50.' }
  ],
  concepts: [
    { skill: 1, q: 'Why should a monthly budget be built on net income instead of gross income?', a: 'Net income is the money actually deposited and available to spend', d: ['Gross income is always smaller than net income', 'Taxes are paid only once a year, so they can be ignored', 'Net income includes employer benefits that can be spent'], why: 'Withholding (taxes, benefits) is removed before you receive your pay. Budgeting with gross pay overstates spendable money.' },
    { skill: 1, q: 'A worker is paid biweekly. How many paychecks does the worker receive in a year?', a: '26', d: ['24', '52', '12'], why: 'Biweekly means every two weeks: 52 ÷ 2 = 26 paychecks. Semimonthly (twice a month) gives 24.', mis: 'Confusing biweekly with semimonthly.' },
    { skill: 1, q: 'Which choice best explains why “two paychecks per month” underestimates the income of a biweekly worker?', a: 'Two months each year contain a third paycheck, so the monthly average is 26 ÷ 12 ≈ 2.17 paychecks', d: ['Biweekly workers are paid more in December', 'Taxes are lower in some months', 'Biweekly pay is the same as semimonthly pay'], why: '26 paychecks ÷ 12 months ≈ 2.17 paychecks per month on average.' },
    { skill: 1, q: 'Which situation describes a negative monthly cash flow?', a: 'Spending $2,640 when take-home pay is $2,480', d: ['Saving $200 from $2,480 of take-home pay', 'Spending exactly $2,480 of $2,480 take-home pay', 'Earning $2,480 and spending $2,300'], why: '$2,480 − $2,640 = −$160, a deficit.' },
    { skill: 2, q: 'Which expense is variable for most households?', a: 'Electricity bill', d: ['Monthly rent under a one-year lease', 'Car loan payment', 'Fixed-price phone plan'], why: 'Electric usage changes with weather and habits, so the bill changes month to month.' },
    { skill: 2, q: 'Select ALL expenses that are usually fixed.', all: ['Rent under a lease', 'Car loan payment', 'Gym membership with a contract'], wrong: ['Groceries', 'Gasoline', 'Dining out'], why: 'Fixed expenses are set by agreement; groceries, gas, and dining vary with behavior and prices.' },
    { skill: 2, q: 'Why do budget planners often average three or more months of a variable expense?', a: 'One month may be unusually high or low, so an average gives a more realistic planning amount', d: ['Variable expenses always increase every month', 'Banks require a three-month average', 'Averages remove the expense from the budget'], why: 'Averaging smooths out month-to-month swings; many planners add a small buffer on top.' },
    { skill: 3, q: 'Kai wants rent to be no more than 30% of a $3,800 gross monthly income. Which inequality models the rent r?', a: 'r ≤ 0.30(3,800)', d: ['r ≥ 0.30(3,800)', 'r = 3,800 − 0.30', '0.30r ≤ 3,800'], why: '“No more than” means ≤. 30% of 3,800 is $1,140, the maximum rent.' },
    { skill: 3, q: 'An emergency fund target is usually based on which amount?', a: 'Several months of essential expenses', d: ['One year of gross salary', 'The balance on all credit cards', 'The price of the most expensive item a person owns'], why: 'The fund must cover necessities if income stops or a surprise bill arrives; 3–6 months of essential expenses is a common guideline.' },
    { skill: 4, q: 'A 32-ounce jar costs $6.40 and a 20-ounce jar of the same product costs $4.20. Which statement is correct?', a: 'The 32-ounce jar has the lower unit price ($0.20 vs $0.21 per ounce)', d: ['The 20-ounce jar is cheaper because its price is lower', 'The two jars have the same unit price', 'The 32-ounce jar costs $0.25 per ounce'], why: '6.40 ÷ 32 = $0.20/oz; 4.20 ÷ 20 = $0.21/oz.' },
    { skill: 4, q: 'Which question best helps decide whether a bulk purchase is actually a good deal?', a: 'Will I use all of it before it spoils or I lose interest?', d: ['Is the package bigger than the regular size?', 'Is the store having a sale this week?', 'Is the total price above $20?'], why: 'A lower unit price only saves money if the extra quantity is actually used.' },
    { skill: 4, q: 'Select ALL possible costs of a buy-now-pay-later plan.', all: ['Late fees for missed installments', 'Overdraft fees if automatic payments hit an empty account', 'Less money available for future months'], wrong: ['A guaranteed lower item price', 'An automatic boost to a credit score'], why: 'BNPL shifts payments to future budgets and can trigger fees; it does not lower the price.' }
  ],
  claims: [
    { skill: 1, claim: 'If I have money left in my checking account at the end of the month, my budget is working.', verdict: 1, model: 'Sometimes. A positive balance can hide irregular bills (annual insurance, car repairs) that have not arrived yet, or credit-card charges not yet paid. A budget works when planned income covers all expenses — including set-asides for irregular costs — and savings goals.', example: 'Ending with $300 looks fine, but a $1,080 annual insurance bill next month creates a $780 shortfall if no sinking fund exists.' },
    { skill: 2, claim: 'Fixed expenses can never be reduced.', verdict: 2, model: 'Never true. Fixed expenses are stable per period, but they can be changed at decision points: getting a roommate, refinancing, switching phone plans, or choosing cheaper housing at lease renewal.', example: 'Moving from $1,325 rent to a $750 shared apartment saves $575 per month ($6,900 per year).' },
    { skill: 2, claim: 'Everyone should follow the 50/30/20 rule exactly.', verdict: 2, model: 'Never true as stated. 50/30/20 is a starting guideline. In high-cost areas needs may exceed 50%; someone paying off high-interest debt may put more than 20% toward debt. The goal is a plan where needs are covered and savings are intentional.', other: 'A person with low rent might reasonably save 35% instead.' },
    { skill: 3, claim: 'Saving a little each month is pointless; you should wait until you can save a large amount.', verdict: 2, model: 'Never true. Small regular amounts accumulate and build the habit. $25 per week is $1,300 per year — enough to cover many common emergencies — before any interest.', example: '$25 × 52 = $1,300.' },
    { skill: 4, claim: 'A sale always saves money.', verdict: 1, model: 'Sometimes. A sale saves money only if you planned to buy the item anyway. Buying something unneeded because it is 40% off spends 60% of the price that could have gone elsewhere — that is an opportunity cost, not a savings.', example: 'A $150 jacket at 40% off costs $90 + tax. If it was not needed, $95.63 left the budget.' },
    { skill: 4, claim: 'Small daily purchases do not really affect a budget.', verdict: 2, model: 'Never true as a general statement. Small recurring costs scale up: $6.50 five days a week is about $1,690 per year. Whether that spending is worth it is a personal choice, but its yearly cost should be known.', example: '$6.50 × 5 × 52 = $1,690.' }
  ],
  families: [
    { id: 'cf-monthly', skill: 1, type: 'calculation', count: 8, gen(r) {
      const p = person(r), net = r.step(1080, 1640, 20), rows = budgetFor(r);
      const monthly = M.round2(net * 26 / 12), exp = total(rows), cf = M.round2(monthly - exp);
      return { prompt: `${p.name} receives a biweekly take-home paycheck of ${$(net)}. ${p.Pos} monthly expenses are listed in the table. Find ${p.pos} average monthly cash flow (use 26 paychecks per year). Is it a surplus or a deficit?`,
        scenario: { title: `${p.name}'s monthly plan`, table: table(['Expense', 'Monthly amount'], rows.map(x => [x[0], $(x[1])]), 'Monthly expenses') },
        ...numeric(cf), solutionSteps: [`Average monthly income = ${$(net)} × 26 ÷ 12 = ${money(monthly)}.`, `Total expenses = ${money(exp)}.`, `Cash flow = ${money(monthly)} − ${money(exp)} = ${money(cf)}, a ${cf >= 0 ? 'surplus' : 'deficit'}.`],
        misconceptions: ['Using 2 paychecks per month (' + money(net * 2) + ') understates income.'] };
    } },
    { id: 'cf-mc', skill: 1, type: 'scenario', count: 7, gen(r) {
      const p = person(r), job = r.pick(JOBS), gross = M.round2(job[1] / 12), net = M.round2(gross * r.pick([0.76, 0.78, 0.8])), rows = budgetFor(r), exp = total(rows);
      const cf = M.round2(net - exp);
      return { prompt: `${p.name}, ${an(job[0])} in ${r.pick(TOWNS)}, earns ${$0(job[1])} per year. After taxes and deductions, ${p.pos} monthly take-home pay is ${money(net)}. ${p.Pos} planned monthly expenses total ${money(exp)}. What is ${p.pos} monthly cash flow?`,
        ...mc(r, money(cf), [money(gross - exp), money(exp - net), money(net + exp), money(cf + 100)]), solutionSteps: [`Use take-home pay, not gross pay: ${money(net)} − ${money(exp)} = ${money(cf)}.`, cf < 0 ? 'Negative cash flow means a deficit: spending must drop, income must rise, or debt/savings will cover the gap.' : 'Positive cash flow is a surplus that can be directed to savings goals.'],
        misconceptions: ['Subtracting expenses from gross monthly pay (' + money(gross) + ').'] };
    } },
    { id: 'cf-sinking', skill: 1, type: 'calculation', count: 7, gen(r) {
      const p = person(r);
      const pool = [['Car insurance (paid every 6 months)', r.step(540, 900, 30), 6], ['Renters insurance (annual)', r.step(144, 228, 12), 12], ['Car registration & inspection (annual)', r.step(96, 180, 12), 12], ['Holiday gifts (December)', r.step(240, 600, 60), 12], ['Car maintenance (estimated per year)', r.step(480, 960, 60), 12], ['Amazon Prime-style membership (annual)', 144, 12], ['Back-to-school supplies (annual)', r.step(180, 360, 30), 12]];
      const items = r.sample(pool, 3), monthly = items.reduce((s, x) => s + x[1] / x[2], 0);
      return { prompt: `${p.name} wants a sinking fund so that irregular bills never surprise ${p.obj}. How much should ${p.sub} set aside each month to cover all three expenses below?`,
        scenario: { table: table(['Irregular expense', 'Amount', 'Every'], items.map(x => [x[0], $(x[1]), x[2] + ' months'])) },
        ...numeric(M.round2(monthly)), solutionSteps: items.map(x => `${x[0]}: ${$(x[1])} ÷ ${x[2]} = ${money(x[1] / x[2])} per month`).concat(`Total monthly set-aside = ${money(monthly)}.`) };
    } },
    { id: 'cf-statement', skill: 1, type: 'document', count: 6, game: false, gen(r) {
      const p = person(r), n1 = r.step(1120, 1480, 20), n2 = n1, side = r.step(120, 340, 20);
      const tx = [['03/01', 'Rent — Elm St Properties', -r.pick([950, 1150, 1225])], ['03/03', 'Payroll deposit', n1], ['03/05', 'FreshMart Groceries', -r.step(82, 140, 1)], ['03/08', 'Riverton Electric', -r.step(64, 118, 1)], ['03/11', 'Cell phone autopay', -r.pick([45, 60, 75])], ['03/14', 'Pet-sitting (side job)', side], ['03/17', 'Payroll deposit', n2], ['03/19', 'FreshMart Groceries', -r.step(70, 130, 1)], ['03/22', 'Streamly subscription', -15.99], ['03/24', 'Gas — QuickFuel', -r.step(38, 62, 1)], ['03/27', 'Takeout — Noodle Bar', -r.step(24, 58, 1)], ['03/29', 'Transfer to savings', -r.pick([100, 150, 200])]];
      const inflow = tx.filter(t => t[2] > 0).reduce((s, t) => s + t[2], 0), outflow = -tx.filter(t => t[2] < 0).reduce((s, t) => s + t[2], 0);
      const ask = r.pick(['net', 'out', 'save']);
      const save = -tx[11][2], netcf = M.round2(inflow - outflow);
      const ansVal = ask === 'net' ? netcf : ask === 'out' ? outflow : M.round2(netcf + save);
      const ask_t = { net: 'What was the net cash flow for March (total deposits minus total withdrawals, including the transfer to savings)?', out: 'What was the total of all money that left the account in March?', save: 'The transfer to savings is not really “spent.” What was March cash flow if you treat the savings transfer as money kept rather than an expense?' }[ask];
      return { prompt: `Review ${p.name}'s fictional March checking-account activity. ${ask_t}`,
        scenario: { document: { kind: 'bank-statement', title: 'Harbor Community Credit Union — Checking Activity', meta: [['Account holder', p.name], ['Statement period', 'March 1–31'], ['Account', '••••4417 (fictional)']], table: table(['Date', 'Description', 'Amount'], tx.map(t => [t[0], t[1], money(t[2])])) } },
        ...numeric(ansVal), solutionSteps: [`Deposits: ${tx.filter(t => t[2] > 0).map(t => money(t[2])).join(' + ')} = ${money(inflow)}.`, `Withdrawals total ${money(outflow)}.`, ask === 'out' ? `Total out = ${money(outflow)}.` : ask === 'net' ? `Net = ${money(inflow)} − ${money(outflow)} = ${money(netcf)}.` : `Net excluding the ${money(save)} savings transfer = ${money(netcf)} + ${money(save)} = ${money(ansVal)}.`] };
    } },
    { id: 'cf-plan-or', skill: 1, type: 'scenario', count: 5, gen(r) {
      const p = person(r), job = r.pick(JOBS.filter(j => j[1] < 50000)), net = M.round2(job[1] * 0.78 / 12), rows = budgetFor(r);
      let exp = total(rows); while (exp < net + 60) { rows.push(['Credit card minimum', 75]); exp = total(rows); }
      const cf = M.round2(net - exp);
      return { format: 'open-response', prompt: `${p.name} works as ${an(job[0])} and takes home ${money(net)} per month. ${p.Sub} ${p.has} started putting the shortfall on a credit card. Analyze ${p.pos} budget.`,
        scenario: { title: `${p.name}'s current monthly plan`, table: table(['Expense', 'Monthly'], rows.map(x => [x[0], $(x[1])])) },
        parts: [{ prompt: 'Calculate the monthly cash flow.', answer: money(cf) }, { prompt: 'Classify each expense as a need or a want and identify the two expenses you would change first.', answer: 'Answers vary; dining out, entertainment, and subscriptions are discretionary; housing and transportation are larger but slower to change.' }, { prompt: 'Propose specific changes and show that the new plan has cash flow of at least $0 and saves at least $100 per month.', answer: `Changes must total at least ${money(-cf + 100)}.` }, { prompt: `Explain one tradeoff of your plan and what happens to ${p.pos} credit-card balance if nothing changes for a year.`, answer: `Without changes the card grows by about ${money(-cf * 12)} plus interest in a year.` }],
        answer: `Cash flow ${money(cf)}; reductions of at least ${money(-cf + 100)} required.`, solutionSteps: [`Total expenses ${money(exp)}; ${money(net)} − ${money(exp)} = ${money(cf)}.`, `To reach +$100, cut or earn ${money(-cf + 100)} per month.`, 'Sample: cut dining out by half, drop one subscription, reduce entertainment, and pick up 4 extra work hours per month.', 'Tradeoff: fewer social meals; benefit: debt stops growing, savings begin.'],
        modelResponse: `${p.name} spends ${money(exp)} but brings home ${money(net)}, a ${money(cf)} monthly deficit. In a year that adds about ${money(-cf * 12)} to the credit card before interest. I would first reduce discretionary spending (dining, entertainment, subscriptions) because those can change this month, then consider a roommate or cheaper transportation at the next renewal. My plan reduces spending by ${money(-cf + 100)}, producing a $100 surplus for an emergency fund. The tradeoff is less flexibility for social activities, but avoiding high-interest debt protects future months.`,
        rubric: undefined };
    } },
    { id: 'fv-classify', skill: 2, type: 'concept', count: 6, gen(r) {
      const fixed = ['Rent under a 12-month lease', 'Car loan payment', 'Student-loan payment on a standard plan', 'Fixed-price phone plan', 'Gym contract membership', 'Renters insurance premium', 'Streaming subscription'];
      const variable = ['Groceries', 'Gasoline', 'Electric bill', 'Dining out', 'Clothing', 'Rideshare trips', 'Heating oil', 'Gifts'];
      const askFixed = r.next() < 0.5, c = r.sample(askFixed ? fixed : variable, 3), w = r.sample(askFixed ? variable : fixed, 3);
      return { prompt: `Select ALL of the expenses that are typically ${askFixed ? 'fixed' : 'variable'} from month to month.`, ...selectAll(r, c, w), solutionSteps: [askFixed ? 'Fixed expenses are set by a contract or price agreement and repeat at the same amount.' : 'Variable expenses change with usage, prices, and choices.', `Correct: ${c.join('; ')}.`] };
    } },
    { id: 'fv-average', skill: 2, type: 'calculation', count: 7, gen(r) {
      const p = person(r), cat = r.pick([['groceries', 280, 420], ['gasoline', 110, 210], ['electricity', 60, 160], ['dining out', 70, 260]]);
      const vals = [0, 1, 2, 3].map(() => r.step(cat[1], cat[2], 1)), avg = M.round2(vals.reduce((a, b) => a + b, 0) / 4), buf = r.pick([0.05, 0.10]);
      const plan = M.round2(avg * (1 + buf));
      return { prompt: `${p.name} spent these amounts on ${cat[0]} over four months: ${vals.map(v => $(v)).join(', ')}. ${p.Sub} decides to budget the four-month average plus a ${pct(buf, 0)} buffer. What monthly amount should ${p.sub} budget?`,
        ...numeric(plan), solutionSteps: [`Average = (${vals.join(' + ')}) ÷ 4 = ${money(avg)}.`, `Add ${pct(buf, 0)}: ${money(avg)} × ${1 + buf} = ${money(plan)}.`, 'The buffer protects against a higher-than-usual month.'] };
    } },
    { id: 'fv-503020', skill: 2, type: 'comparison', count: 7, gen(r) {
      const p = person(r), net = r.step(2400, 4200, 100);
      const needs = M.round2(net * r.pick([0.52, 0.58, 0.61, 0.47, 0.55])), wants = M.round2(net * r.pick([0.24, 0.29, 0.33, 0.21])), save = M.round2(net - needs - wants);
      const g = M.rule503020(net), which = r.pick(['needs', 'wants', 'savings']);
      const actual = { needs, wants, savings: save }[which], diff = M.round2(actual - g[which]);
      return { prompt: `${p.name} takes home ${$(net)} per month and spends ${money(needs)} on needs and ${money(wants)} on wants; the rest goes to savings. Compared with the 50/30/20 guideline, how many dollars above (+) or below (−) the guideline is ${p.pos} ${which} amount?`,
        ...numeric(diff), solutionSteps: [`Savings = ${$(net)} − ${money(needs)} − ${money(wants)} = ${money(save)}.`, `Guideline ${which}: ${which === 'needs' ? '50%' : which === 'wants' ? '30%' : '20%'} × ${$(net)} = ${money(g[which])}.`, `Difference = ${money(actual)} − ${money(g[which])} = ${money(diff)}.`, 'The guideline is a reference point, not a requirement; explain whether the difference is reasonable.'] };
    } },
    { id: 'fv-tracker-or', skill: 2, type: 'document', count: 4, gen(r) {
      const p = person(r), net = r.step(2600, 3600, 100);
      const rows = [['Rent', 'Fixed', 'Need', r.pick([1150, 1225, 1325])], ['Car payment', 'Fixed', 'Need', r.pick([285, 340])], ['Car insurance', 'Fixed', 'Need', r.pick([125, 160])], ['Groceries', 'Variable', 'Need', r.step(300, 400, 5)], ['Gas', 'Variable', 'Need', r.step(120, 180, 5)], ['Utilities', 'Variable', 'Need', r.step(90, 150, 5)], ['Dining & takeout', 'Variable', 'Want', r.step(180, 320, 5)], ['Subscriptions (4)', 'Fixed', 'Want', r.pick([48, 56, 63])], ['Shopping', 'Variable', 'Want', r.step(120, 260, 5)], ['Savings transfer', 'Fixed', 'Savings', r.pick([50, 100])]];
      const n = rows.filter(x => x[2] === 'Need').reduce((s, x) => s + x[3], 0), w = rows.filter(x => x[2] === 'Want').reduce((s, x) => s + x[3], 0), s = rows.filter(x => x[2] === 'Savings').reduce((s2, x) => s2 + x[3], 0);
      return { format: 'open-response', prompt: `${p.name} tracked one month of spending (take-home pay ${$(net)}). Analyze the tracker and make a recommendation.`,
        scenario: { document: { kind: 'spending-tracker', title: `${p.name}'s Spending Tracker — October`, meta: [['Take-home pay', $(net)]], table: table(['Category', 'Fixed/Variable', 'Need/Want/Savings', 'Amount'], rows.map(x => [x[0], x[1], x[2], $(x[3])])) } },
        parts: [{ prompt: 'Find the totals and percents of take-home pay for needs, wants, and savings.', answer: `Needs ${$(n)} (${pct(n / net)}), wants ${$(w)} (${pct(w / net)}), savings ${$(s)} (${pct(s / net)}); unspent ${$(net - n - w - s)}.` }, { prompt: 'Which variable expense would be easiest to reduce next month? Why?', answer: 'Dining & takeout or shopping — they are variable wants that change with daily choices.' }, { prompt: 'Which fixed expense might be worth reconsidering at its next decision point?', answer: 'Subscriptions (cancel any unused) or insurance (shop rates); rent at lease renewal.' }, { prompt: 'Write a revised plan that reaches at least 15% savings and explain the tradeoffs.', answer: `Savings of at least ${$(Math.ceil(net * 0.15))} per month.` }],
        answer: `Needs ${pct(n / net)}, wants ${pct(w / net)}, savings ${pct(s / net)}.`, solutionSteps: [`Needs total ${$(n)}; wants ${$(w)}; savings ${$(s)}.`, `Percents of ${$(net)}: ${pct(n / net)}, ${pct(w / net)}, ${pct(s / net)}.`, `15% savings target = ${money(net * 0.15)}.`],
        modelResponse: `Needs use ${pct(n / net)} and wants ${pct(w / net)} of take-home pay, while savings is only ${pct(s / net)}. Dining and shopping are variable wants that can change immediately. I would cut takeout by about half and set a shopping limit, and cancel unused subscriptions, moving that money into savings until savings reach ${money(net * 0.15)} per month. The tradeoff is fewer convenience meals, but it builds an emergency fund.` };
    } },
    { id: 'con-rent', skill: 3, type: 'calculation', count: 7, gen(r) {
      const p = person(r), job = r.pick(JOBS), gm = M.round2(job[1] / 12), pctR = r.pick([0.25, 0.28, 0.30]);
      return { prompt: `${p.name} earns ${$0(job[1])} per year as ${an(job[0])}. ${p.Sub} wants rent to be at most ${pct(pctR, 0)} of gross monthly income. What is the maximum monthly rent?`, ...numeric(M.round2(gm * pctR)), solutionSteps: [`Gross monthly = ${$0(job[1])} ÷ 12 = ${money(gm)}.`, `r ≤ ${pctR} × ${money(gm)} = ${money(gm * pctR)}.`] };
    } },
    { id: 'con-hours', skill: 3, type: 'calculation', count: 7, gen(r) {
      const p = person(r), wage = r.pick([15.5, 16, 16.75, 17.25, 18, 19.5]), takeRate = r.pick([0.88, 0.9, 0.92]), item = r.pick([['a used laptop', 640], ['a prom outfit and tickets', 420], ['a used e-bike', 980], ['concert trip costs', 515], ['car insurance down payment', 760]]);
      const have = r.step(0, 200, 25), costT = item[1] * (1 + SALES_TAX), per = wage * takeRate, h = Math.ceil((costT - have) / per - 1e-9);
      return { prompt: `${p.name} earns ${$(wage)} per hour at a part-time job and keeps about ${pct(takeRate, 0)} after payroll taxes. ${p.Sub} already ${p.has} ${$(have)} saved and wants ${item[0]} costing ${$(item[1])} plus ${pct(SALES_TAX, 2)} sales tax. What is the minimum whole number of hours ${p.sub} must work?`,
        ...numeric(h, { unit: 'count' }), solutionSteps: [`Total cost = ${$(item[1])} × 1.0625 = ${money(costT)}.`, `Still needed = ${money(costT)} − ${$(have)} = ${money(costT - have)}.`, `Take-home per hour = ${$(wage)} × ${takeRate} = ${money(per)}.`, `Solve ${money(per)}h ≥ ${money(costT - have)}: h ≥ ${(Math.round((costT - have) / per * 100) / 100)} → ${h} hours (round up).`] };
    } },
    { id: 'con-goal', skill: 3, type: 'calculation', count: 7, gen(r) {
      const p = person(r), goal = r.pick([['an emergency fund', r.step(2400, 6000, 300)], ['a car down payment', r.step(1500, 4000, 250)], ['a security deposit and first month’s rent', r.step(2200, 3200, 100)], ['a summer trip', r.step(900, 1800, 100)]]), months = r.pick([6, 8, 10, 12, 15, 18]), start = r.step(0, 600, 50);
      const needed = M.round2((goal[1] - start) / months);
      return { prompt: `${p.name} wants ${$(goal[1])} for ${goal[0]} in ${months} months and already has ${$(start)}. Ignoring interest, what is the least amount ${p.sub} must save each month?`,
        ...numeric(Math.ceil(needed * 100) / 100), solutionSteps: [`Remaining = ${$(goal[1])} − ${$(start)} = ${$(goal[1] - start)}.`, `${months}m ≥ ${$(goal[1] - start)} → m ≥ ${money(needed)} per month.`, 'Round up to the cent so the goal is actually reached.'] };
    } },
    { id: 'con-model', skill: 3, type: 'concept', count: 6, gen(r) {
      const p = person(r), inc = r.step(2400, 3400, 100), fixed = r.step(1400, 2000, 50), save = r.step(150, 400, 50);
      const correct = `${fixed} + v + ${save} ≤ ${inc}`;
      return { prompt: `${p.name} takes home ${$(inc)} monthly, has ${$(fixed)} in fixed expenses, and wants to save at least ${$(save)}. Let v be the monthly amount for variable spending. Which inequality models the constraint, and what is the maximum v?`,
        ...mc(r, `${correct}; v ≤ ${$(inc - fixed - save)}`, [`${fixed} + v + ${save} ≥ ${inc}; v ≥ ${$(inc - fixed - save)}`, `${fixed} + v ≤ ${inc}; v ≤ ${$(inc - fixed)}`, `v + ${save} ≤ ${inc}; v ≤ ${$(inc - save)}`]), solutionSteps: [`Spending + saving cannot exceed income: ${correct}.`, `v ≤ ${inc} − ${fixed} − ${save} = ${$(inc - fixed - save)}.`] };
    } },
    { id: 'con-emergency', skill: 3, type: 'scenario', count: 5, gen(r) {
      const p = person(r), ess = r.step(1800, 2900, 50), months = r.pick([3, 4, 6]), have = r.step(500, 2500, 250), sv = r.step(150, 400, 25);
      const target = ess * months, m2 = Math.ceil((target - have) / sv - 1e-9);
      return { prompt: `${p.name}'s essential expenses are ${$(ess)} per month. ${p.Sub} wants an emergency fund covering ${months} months, has ${$(have)} saved, and can save ${$(sv)} per month. How many months will it take to reach the target?`,
        ...numeric(m2, { unit: 'count' }), solutionSteps: [`Target = ${months} × ${$(ess)} = ${$(target)}.`, `Remaining = ${$(target - have)}.`, `${$(target - have)} ÷ ${$(sv)} ≈ ${Math.round((target - have) / sv * 100) / 100} → ${m2} months.`] };
    } },
    { id: 'sp-gym', skill: 4, type: 'comparison', count: 7, gen(r) {
      const p = person(r), fee = r.pick([[29, 'Club FitLine'], [35, 'PowerHouse Gym'], [42, 'Riverside Athletic']]), visit = r.pick([6, 7, 8, 9]), join = r.pick([0, 25, 49]);
      const visits = r.int(3, 8), monthCost = fee[0], pay = visit * visits;
      const be = Math.ceil(fee[0] / visit - 1e-9);
      return { prompt: `${fee[1]} charges ${$(fee[0])} per month (plus a one-time ${$(join)} joining fee). The community center charges ${$(visit)} per visit. ${p.name} expects to go ${visits} times per month. (a) Which option costs less per month, ignoring the joining fee? (b) What is the minimum number of monthly visits for the membership to be cheaper?`,
        format: 'short-answer', answer: `(a) ${pay < monthCost ? 'Pay per visit (' + $(pay) + ' vs ' + $(monthCost) + ')' : pay > monthCost ? 'Membership (' + $(monthCost) + ' vs ' + $(pay) + ')' : 'They tie at ' + $(pay)} (b) ${be} visits`, numeric: { value: be, tolerance: 0, unit: 'count' },
        solutionSteps: [`Pay per visit: ${visits} × ${$(visit)} = ${$(pay)}.`, `Membership: ${$(monthCost)}.`, `Break-even: ${$(fee[0])} ÷ ${$(visit)} ≈ ${(fee[0] / visit).toFixed(2)}, so ${be} or more visits make the membership cheaper${fee[0] % visit === 0 ? ' (at exactly ' + fee[0] / visit + ' they tie)' : ''}.`, join ? `The ${$(join)} joining fee spread over 12 months adds ${money(join / 12)} per month.` : 'No joining fee applies.'],
        misconceptions: ['Choosing the membership because “unlimited” sounds cheaper without counting realistic visits.'], game: false };
    } },
    { id: 'sp-habit', skill: 4, type: 'calculation', count: 7, gen(r) {
      const p = person(r), h = r.pick([['iced coffee', 5.75, 5], ['energy drink', 3.49, 6], ['lunch from a café', 11.5, 5], ['smoothie', 7.25, 3], ['convenience-store snack', 4.1, 5], ['rideshare to work', 13.8, 2]]);
      const annual = M.round2(h[1] * h[2] * 52);
      return { prompt: `${p.name} buys ${an(h[0])} for ${$(h[1])} about ${h[2]} times per week. What is the annual cost of this habit (52 weeks)?`, ...numeric(annual), solutionSteps: [`${$(h[1])} × ${h[2]} × 52 = ${money(annual)} per year.`, `Opportunity cost: that ${money(annual)} could fund ${Math.floor(annual / 100) * 100 >= 1000 ? 'a large share of a starter emergency fund' : 'a sinking fund for an annual bill'}.`] };
    } },
    { id: 'sp-unit', skill: 4, type: 'comparison', count: 7, gen(r) {
      const it = r.pick([['laundry detergent', 'loads', [[64, 13.99], [150, 27.49]]], ['coffee', 'ounces', [[12, 9.49], [32, 22.99]]], ['paper towels', 'sheets', [[6 * 102, 8.99], [12 * 140, 21.99]]], ['cereal', 'ounces', [[18, 4.79], [40, 9.29]]], ['shampoo', 'ounces', [[13.5, 6.49], [33.8, 13.99]]]]);
      const [a, b] = it[2], ua = a[1] / a[0], ub = b[1] / b[0], better = ua < ub ? 'smaller' : 'larger';
      const fmt = u => '$' + u.toFixed(3);
      return { prompt: `A store sells ${it[0]} in two sizes: ${a[0]} ${it[1]} for ${$(a[1])} or ${b[0]} ${it[1]} for ${$(b[1])}. Which size has the lower unit price, and by about how much per ${it[1].replace(/s$/, '')}?`,
        ...mc(r, `The ${better} size, by about ${fmt(Math.abs(ua - ub))} per ${it[1].replace(/s$/, '')}`, [`The ${better === 'smaller' ? 'larger' : 'smaller'} size, by about ${fmt(Math.abs(ua - ub))} per ${it[1].replace(/s$/, '')}`, `The ${better === 'smaller' ? 'larger' : 'smaller'} size, because its total price is ${better === 'smaller' ? 'higher' : 'lower'}`, 'They have the same unit price']),
        solutionSteps: [`Small: ${$(a[1])} ÷ ${a[0]} ≈ ${fmt(ua)} per unit.`, `Large: ${$(b[1])} ÷ ${b[0]} ≈ ${fmt(ub)} per unit.`, 'Lower unit price is a better deal only if you will use the whole package and can afford the up-front cost.'] };
    } },
    { id: 'sp-sale', skill: 4, type: 'calculation', count: 7, gen(r) {
      const p = person(r), item = r.pick([['pair of running shoes', 129.99], ['winter jacket', 189], ['wireless headphones', 249.99], ['desk chair', 164.5], ['video game console bundle', 449.99], ['set of tires', 520]]), off = r.pick([0.15, 0.2, 0.25, 0.3, 0.4]);
      const sale = M.round2(item[1] * (1 - off)), tax = M.round2(sale * SALES_TAX), tot = M.round2(sale + tax);
      return { prompt: `A ${item[0]} regularly priced at ${$(item[1])} is ${pct(off, 0)} off. Sales tax is ${pct(SALES_TAX, 2)} and is applied to the sale price. What is the total cost?`, ...numeric(tot), solutionSteps: [`Sale price = ${$(item[1])} × ${1 - off} = ${money(sale)}.`, `Tax = ${money(sale)} × 0.0625 = ${money(tax)}.`, `Total = ${money(tot)}.`, 'Ask: was this purchase planned? Savings only matter if you intended to buy it.'] };
    } },
    { id: 'sp-bnpl', skill: 4, type: 'comparison', count: 6, game: false, gen(r) {
      const p = person(r), price = r.step(180, 600, 20), apr = r.pick([0.2299, 0.2499, 0.2799]), months = r.pick([3, 4, 6]), fee = r.pick([7, 10, 15]), missed = r.int(0, 2);
      const bnpl = M.round2(price + missed * fee), card = M.amortize(price, apr, months), cardTot = card.totalPaid;
      return { prompt: `${p.name} wants a ${$(price)} purchase. Option A: buy now, pay later in 4 equal interest-free installments with a ${$(fee)} fee for each late payment. Option B: put it on a credit card at ${pct(apr, 2)} APR and pay it off in ${months} equal monthly payments. Option C: save for ${months} months, then pay cash. If ${p.name} misses ${missed} installment${missed === 1 ? '' : 's'} with Option A, rank the options from lowest to highest total cost.`,
        ...(() => { const o = [['A', bnpl], ['B', cardTot], ['C', price]]; const rank = arr => arr.slice().sort((x, y) => x[1] - y[1] || x[0].localeCompare(y[0])).map(x => `${x[0]} (${money(x[1])})`).join(' ≤ ');
          return mc(r, rank(o), [rank([['A', price / 4], ['B', cardTot], ['C', price]]), o.slice().sort((x, y) => y[1] - x[1]).map(x => `${x[0]} (${money(x[1])})`).join(' ≤ '), rank([['A', bnpl], ['B', price], ['C', cardTot]])]); })(),
        solutionSteps: [`A: ${$(price)} + ${missed} × ${$(fee)} = ${money(bnpl)}.`, `B: payment ${money(card.payment)} × ${months} ≈ ${money(cardTot)} (interest ${money(card.totalInterest)}).`, `C: ${$(price)}, but the item arrives ${months} months later.`, 'Non-numeric tradeoffs: waiting vs. immediate need; BNPL and card payments reduce future budgets.'] };
    } },
    { id: 'sp-phone-or', skill: 4, type: 'comparison', count: 4, gen(r) {
      const p = person(r), a = { name: 'Plan A — FlexTalk', base: r.pick([35, 40]), perGB: r.pick([10, 12]), incl: 5, device: 0 }, b = { name: 'Plan B — UnlimitedPlus', base: r.pick([65, 70, 75]), perGB: 0, incl: Infinity, device: r.pick([0, 15]) };
      const gbs = [r.int(3, 6), r.int(8, 12), r.int(14, 18)];
      const cost = (pl, g) => pl.base + pl.device + (pl.incl === Infinity ? 0 : Math.max(0, g - pl.incl) * pl.perGB);
      const be = a.incl + Math.ceil((b.base + b.device - a.base) / a.perGB - 1e-9);
      return { format: 'open-response', prompt: `${p.name} is choosing a phone plan for the next two years. Compare the plans.`,
        scenario: { table: table(['Feature', a.name, b.name], [['Monthly base price', $(a.base), $(b.base)], ['Data included', '5 GB', 'Unlimited'], ['Extra data', $(a.perGB) + ' per GB over 5 GB', '—'], ['Device installment', '$0 (bring own phone)', $(b.device) + '/month']]) },
        parts: [{ prompt: `Find the monthly cost of each plan if ${p.name} uses ${gbs[0]}, ${gbs[1]}, and ${gbs[2]} GB.`, answer: gbs.map(g => `${g} GB: A ${$(cost(a, g))}, B ${$(cost(b, g))}`).join('; ') }, { prompt: 'Write a cost function for Plan A when data use is above 5 GB.', answer: `C(g) = ${a.base} + ${a.perGB}(g − 5)` }, { prompt: 'At what whole-GB usage does Plan B become cheaper?', answer: `${be} GB or more` }, { prompt: 'Make a recommendation and identify information you still need (actual usage history, coverage, contract terms).', answer: 'Answers vary; must reference typical usage.' }],
        answer: `Plan B is cheaper at ${be}+ GB.`, solutionSteps: gbs.map(g => `${g} GB → A ${$(cost(a, g))}, B ${$(cost(b, g))}`).concat(`Break-even: ${a.base} + ${a.perGB}(g − 5) > ${b.base + b.device} → g > ${(5 + (b.base + b.device - a.base) / a.perGB).toFixed(2)}.`),
        modelResponse: `Plan A is cheaper for light users, but each GB over 5 costs ${$(a.perGB)}. Plan B costs ${$(b.base + b.device)} regardless of use and becomes cheaper at ${be} GB. I would check ${p.name}'s last three months of data use; if usage is usually above ${be - 1} GB, choose Plan B for predictability; otherwise choose Plan A and use Wi-Fi.` };
    } }
  ],
  flashExtras: [
    { skill: 1, kind: 'formula', front: 'Biweekly pay → monthly', back: 'Multiply the paycheck by 26, then divide by 12.', example: '$1,240 × 26 ÷ 12 = $2,686.67', watch: 'Not × 2 — that misses two paychecks a year.' },
    { skill: 1, kind: 'principle', front: 'Pay yourself first', back: 'Move savings out on payday before spending, so saving is a planned expense rather than leftovers.' },
    { skill: 1, kind: 'document', front: 'Bank statement: what to scan first', back: 'Total deposits, total withdrawals, ending balance, recurring charges, and fees.' },
    { skill: 2, kind: 'relationship', front: 'Fixed vs. variable vs. need vs. want', back: 'Two separate questions: does the amount change? Is it required? A subscription is a fixed want; groceries are a variable need.' },
    { skill: 3, kind: 'principle', front: 'Rounding in the safe direction', back: 'Round hours and months UP; round maximum spending DOWN.', example: '72.6 hours → 73 hours' },
    { skill: 4, kind: 'formula', front: 'Break-even uses', back: 'Fixed cost ÷ savings per use, rounded up.', example: '$35 membership ÷ $8 per visit → 5 visits' },
    { skill: 4, kind: 'principle', front: 'Total cost beats monthly payment', back: 'Compare what you pay in total, including fees and interest — not the size of each payment.' }
  ],
  lessons: [
    { skill: 1, title: 'Where Does the Money Go? Monthly Cash Flow', minutes: 55,
      objectives: ['Convert pay from any pay frequency to an average monthly amount.', 'Calculate monthly cash flow and interpret a surplus or deficit.', 'Build a sinking fund for irregular expenses.'],
      vocab: ['Budget', 'Cash flow', 'Surplus', 'Deficit', 'Net income (take-home pay)', 'Sinking fund'],
      hook: 'Show two fictional friends who each earn $3,000 per month. One ends every month stressed; the other has $250 left. Ask: “What could be different besides income?”',
      notes: [
        { h: 'Cash flow', body: 'Cash flow = money in − money out for a period. Positive = surplus; negative = deficit. Use take-home (net) pay, because withholding never reaches your account.' },
        { h: 'Converting pay frequencies', body: 'Weekly × 52 ÷ 12; biweekly × 26 ÷ 12; semimonthly × 2; annual ÷ 12. Biweekly workers get 26 checks, so “two checks a month” undercounts by about 2 checks per year.' },
        { h: 'Irregular expenses', body: 'Annual or semiannual bills (insurance, registration, gifts) are real monthly costs. Divide each by the number of months it covers and set that amount aside every month — a sinking fund.' }
      ],
      examples: [
        { problem: 'Lena’s biweekly take-home pay is $1,240. Her monthly expenses total $2,610. Find her monthly cash flow.', steps: ['Monthly income = 1,240 × 26 ÷ 12 = $2,686.67', 'Cash flow = 2,686.67 − 2,610 = $76.67', 'Surplus, but small — one surprise bill could erase it.'], answer: '$76.67 surplus' },
        { problem: 'Lena also pays $720 for car insurance every 6 months and $132 for renters insurance each year. What is her monthly sinking-fund amount, and what is her true cash flow?', steps: ['720 ÷ 6 = $120 per month', '132 ÷ 12 = $11 per month', 'Sinking fund = $131 per month', 'True cash flow = 76.67 − 131 = −$54.33'], answer: 'Lena actually runs a $54.33 monthly deficit.' }
      ],
      document: 'bank-statement',
      discussion: ['Why might someone feel “broke” even when their paycheck is larger than their monthly bills?', 'What is the difference between saving money and having a surplus?', 'Which expenses are hardest to remember when building a budget?'],
      misconceptions: [['Budgeting with gross pay.', 'Ask students to find the deposit amount on a pay stub; that is the budget number.'], ['Assuming biweekly = twice a month.', 'Count paydays on a printed calendar to show 26.'], ['Ignoring annual bills.', 'Have students list every bill they know of that is not monthly.']],
      reflection: ['Which irregular expenses would show up in your future budget?', 'How would you know whether your budget is working after three months?'],
      extension: 'Research two irregular costs for a car owner in your area and build a sinking-fund plan.',
      differentiation: { support: ['Provide a conversion table for pay frequencies.', 'Use a pre-sorted expense list.'], extend: ['Have students model a month with three paychecks.', 'Ask students to write a rule for when a biweekly worker’s surplus is real.'] },
      realWorld: 'Many banks and budgeting apps categorize transactions automatically; students should still check the totals against their own plan.' },
    { skill: 2, title: 'Fixed vs. Variable, Needs vs. Wants', minutes: 55,
      objectives: ['Classify expenses as fixed or variable and as needs or wants.', 'Use averages to plan for variable expenses.', 'Compare a spending pattern with the 50/30/20 guideline and judge whether differences are reasonable.'],
      vocab: ['Fixed expense', 'Variable expense', 'Discretionary expense', 'Essential expense (need)', '50/30/20 guideline'],
      hook: 'Card sort: 16 expense cards. Pairs sort them two ways (fixed/variable, need/want) and defend tough cases like a phone plan or a car.',
      notes: [{ h: 'Two different questions', body: 'Fixed/variable asks “does the amount change?” Need/want asks “is it required for basic living or earning income?” A streaming subscription is fixed but a want; groceries are variable but a need.' }, { h: 'Planning for variable costs', body: 'Average several months, then add a 5–10% buffer. Track actual spending to adjust.' }, { h: '50/30/20 as a reference point', body: 'Needs about 50%, wants about 30%, savings/extra debt payments about 20% of take-home pay. Use it to start a conversation, not as a law.' }],
      examples: [{ problem: 'Groceries were $318, $356, $341, $305. Budget the average plus 10%.', steps: ['Average = 1,320 ÷ 4 = $330', '330 × 1.10 = $363'], answer: '$363 per month' }, { problem: 'Take-home pay $3,200; needs $1,890; wants $910. Compare to 50/30/20.', steps: ['Savings = 3,200 − 1,890 − 910 = $400 (12.5%)', 'Needs 59.1% vs 50%; wants 28.4% vs 30%; savings 12.5% vs 20%'], answer: 'Needs are high; savings are $240 below the 20% reference ($640).' }],
      document: 'spending-tracker',
      discussion: ['Is a car a need or a want? What information decides it?', 'Why might someone in an expensive city reasonably exceed 50% for needs?', 'Which is easier to change quickly: fixed or variable expenses?'],
      misconceptions: [['Fixed means “necessary.”', 'Show fixed wants (subscriptions) and variable needs (groceries).'], ['50/30/20 is a requirement.', 'Compare three fictional people with different rents and goals.']],
      reflection: ['Which of your current spending categories are variable wants?', 'What percent of a future paycheck would you want to save, and why?'],
      extension: 'Students design an alternative guideline (e.g., 60/20/20) for a high-cost city and justify it.',
      differentiation: { support: ['Color-code categories.', 'Provide a percent calculation template.'], extend: ['Compute the dollar change needed to reach 20% savings and propose two plans.'] },
      realWorld: 'Credit-card and bank apps often label categories; their labels do not decide what is a need.' },
    { skill: 3, title: 'Living Within Limits: Modeling Financial Constraints', minutes: 55,
      objectives: ['Write and solve inequalities that model budget constraints.', 'Determine time or hours needed to reach a savings goal.', 'Set and justify an emergency-fund target.'],
      vocab: ['Financial constraint', 'Savings goal', 'Emergency fund'],
      hook: '“Your dream apartment is $1,450. Can you afford it?” Students list what they would need to know.',
      notes: [{ h: 'Constraints as inequalities', body: 'Spending + saving ≤ income. “At most” → ≤; “at least” → ≥. Solve for the unknown and interpret the boundary.' }, { h: 'Round in the safe direction', body: 'Hours worked and months saved round UP; maximum spending amounts round DOWN to the cent.' }, { h: 'Emergency funds', body: 'Commonly 3–6 months of essential expenses. Start with a smaller first target (e.g., $1,000) to build momentum.' }],
      examples: [{ problem: 'Gross pay $4,200/month. Rent must be ≤ 30% of gross. Max rent?', steps: ['r ≤ 0.30 × 4,200', 'r ≤ $1,260'], answer: '$1,260' }, { problem: 'Take-home $2,900; fixed $1,760; save at least $250. Max variable spending v?', steps: ['1,760 + v + 250 ≤ 2,900', 'v ≤ $890'], answer: 'v ≤ $890' }, { problem: 'Need $1,150 more; earn $15.84 after taxes per hour. Hours?', steps: ['15.84h ≥ 1,150', 'h ≥ 72.6', 'Round up: 73 hours'], answer: '73 hours' }],
      discussion: ['Why might two lenders or landlords use different affordability rules?', 'What happens to the constraint if income is irregular (tips, gig work)?'],
      misconceptions: [['Rounding hours down.', 'Test the rounded answer: does 72 hours reach the goal?'], ['Flipping the inequality.', 'Translate the words first: “at most” means the value can equal or be below.']],
      reflection: ['What constraint matters most in your life right now?', 'How large should your first emergency fund be, and why?'],
      extension: 'Model irregular gig income with a minimum and maximum month; find a budget that works for the minimum.',
      differentiation: { support: ['Inequality phrase bank.', 'Number line visual for ≤/≥.'], extend: ['System of constraints: rent ≤ 30% of gross AND total housing ≤ 40% of take-home.'] },
      realWorld: 'Landlords often require gross income of 2.5–3× the rent; this is the same inequality from the landlord’s side.' },
    { skill: 4, title: 'Is It Worth It? Comparing Spending Decisions', minutes: 55,
      objectives: ['Compare options using unit price, break-even analysis, and annualized cost.', 'Identify opportunity costs, including non-monetary ones.', 'Evaluate sales, BNPL offers, and subscriptions critically.'],
      vocab: ['Opportunity cost', 'Unit price', 'Impulse purchase', 'Buy now, pay later (BNPL)', 'Sales tax'],
      hook: 'Show a fictional ad: “Save $60! Today only!” Ask: “When does buying this save money, and when does it cost money?”',
      notes: [{ h: 'Annualize small costs', body: 'Price × times per week × 52. Seeing the yearly number makes the opportunity cost visible.' }, { h: 'Break-even', body: 'Fixed cost ÷ savings per use = uses needed before the fixed option is cheaper.' }, { h: 'Unit price', body: 'Price ÷ quantity. Only a deal if you will use it all and can afford the larger up-front cost.' }, { h: 'Total cost of financing', body: 'Compare the total paid (including fees and interest), not just the per-payment amount.' }],
      examples: [{ problem: 'Gym: $35/month vs $8/visit. Break-even?', steps: ['35 ÷ 8 = 4.375', '5 visits or more per month'], answer: '5+ visits favors membership' }, { problem: '$5.75 coffee 5 days a week. Annual cost?', steps: ['5.75 × 5 × 52 = $1,495'], answer: '$1,495 per year' }],
      discussion: ['Is spending $1,495 a year on coffee a bad decision? Who gets to decide?', 'Why do stores place items near checkout?', 'What is the opportunity cost of time spent comparison shopping?'],
      misconceptions: [['A lower payment means a lower price.', 'Compute the total of all payments.'], ['Sales always save money.', 'Ask whether the purchase was planned.']],
      reflection: ['Name one recurring purchase you make. What is its annual cost?', 'Describe a time a “deal” cost you more than expected.'],
      extension: 'Research a real store’s BNPL terms (late fees, autopay) and summarize the risks.',
      differentiation: { support: ['Unit-price calculation organizer.', 'Calculator allowed.'], extend: ['Include time value: compare saving the money at 4% APY for 5 years.'] },
      realWorld: 'Many states require shelf tags to show unit prices; students can check them on their next store trip.' }
  ],
  cheatSheet: { title: 'Budgeting & Spending', ...sheets.budgeting }
};
