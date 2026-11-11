import { M, money, $ } from '../kit.mjs';

const CAREERS = [['Pharmacy technician', 39000], ['Electrician apprentice', 44000], ['Paralegal', 50000], ['HVAC technician', 52000], ['Graphic designer', 54000], ['Registered nurse', 82000]];
const careerRows = CAREERS.map(([j, g]) => { const n = M.netPay(g, { retirementPct: 0.03, healthPremium: 1200 }); return [j, $(g), money(g / 12), money(n.net / 12)]; });
const ex = M.netPay(50000, { retirementPct: 0.03, healthPremium: 1200 });
const exNet = M.round2(ex.net / 12);
const COST = [['Housing', 'Room in shared house $725 · Studio $1,150 · 1-bedroom $1,425 · 2-bedroom (split) $910'], ['Utilities & internet', 'Shared $70 · Own place $135'], ['Transportation', 'Bus/transit pass $90 · Used car: payment $265 + insurance $150 + gas $140 · Bike + rideshare $55'], ['Groceries', 'Thrifty $260 · Moderate $350 · Generous $450'], ['Phone', 'Prepaid $35 · Standard $65 · Premium unlimited $90'], ['Health premium', 'Already deducted from pay (see career card)'], ['Entertainment & dining', 'Your choice; minimum $50'], ['Clothing & personal', 'Minimum $60'], ['Savings', 'At least 10% of take-home pay'], ['Student loan (if your career needs one)', 'Nurse $310 · Paralegal $185 · Designer $240 · Others $0']];
const exBudget = [['Studio', 1150], ['Utilities', 135], ['Used car (payment + insurance + gas)', 555], ['Groceries (moderate)', 350], ['Phone (standard)', 65], ['Entertainment & dining', 150], ['Clothing & personal', 80], ['Student loan', 185], ['Savings (10%)', Math.ceil(exNet * 0.1)]];
const exTotal = exBudget.reduce((s, x) => s + x[1], 0);

export default [
  {
    slug: 'survive-on-your-salary', title: 'Survive on Your Salary', unit: 'budgeting', unitNum: 2,
    tagline: 'Draw a career, build a realistic monthly budget, and survive what life throws at you.',
    grouping: 'Individual (best) or pairs', days: '3–4 class periods', skills: ['budgeting-skill-01', 'budgeting-skill-02', 'budgeting-skill-03', 'budgeting-skill-04'],
    intro: 'Your first full-time paycheck is coming. Before the excitement wears off, rent, a car, groceries, and a dozen small bills will compete for every dollar. In this project you will receive a fictional career, figure out what you actually take home, build a budget for life in the fictional city of Riverton, and then respond to the surprises that real life brings.',
    scenario: 'You have just moved to Riverton for a new job. You have $1,500 in savings, no furniture, and big plans. Your employer withholds taxes, a 3% retirement contribution, and a $100 monthly health premium from every paycheck.',
    goals: ['Convert an annual salary to monthly take-home pay and explain each deduction.', 'Build a balanced monthly budget using realistic local costs.', 'Classify expenses as fixed/variable and needs/wants and compare with the 50/30/20 guideline.', 'Model savings goals and constraints with inequalities.', 'Adjust a budget in response to unexpected events and defend your choices.'],
    documents: [
      { title: 'Career Cards (fictional employers; Course Tax Table)', table: { headers: ['Career', 'Annual salary', 'Gross monthly', 'Est. take-home monthly*'], rows: careerRows }, note: '*After federal tax (Course Tax Table), 7.65% FICA, 5% state tax, 3% retirement, and a $100/month health premium.' },
      { title: 'Riverton Cost Guide (monthly)', table: { headers: ['Category', 'Choices'], rows: COST } },
      { title: 'Life Happens Event Cards (teacher deals three)', table: { headers: ['#', 'Event'], rows: [['1', 'Your car needs new brakes: $640 (if no car: phone screen repair $180).'], ['2', 'Your hours are cut: take-home pay drops 10% for 3 months.'], ['3', 'Your rent increases 6% at lease renewal.'], ['4', 'A friend’s wedding: $350 for travel and a gift in 2 months.'], ['5', 'Medical bill after urgent care: $275.'], ['6', 'You earn a $1,200 bonus (before taxes; keep 72%).'], ['7', 'Your roommate moves out — you must cover their $725 share for 1 month or find a new roommate.'], ['8', 'Annual car registration and inspection: $165 due next month.']] } }
    ],
    tasks: [
      { title: 'Know your paycheck', steps: ['Record your career, annual salary, and gross monthly pay.', 'Using the career card, record your monthly take-home pay.', 'Explain in two sentences why take-home pay is less than gross pay. Name at least three deductions.', 'Rent guideline check: what is 30% of your gross monthly pay? Write and solve the inequality r ≤ 0.30 × (gross monthly).'], deliverable: 'Paycheck summary with the rent inequality.' },
      { title: 'Build your budget', steps: ['Choose one option in every category of the Riverton Cost Guide.', 'Complete a budget table with columns: Category, Amount, Fixed/Variable, Need/Want/Savings.', 'Find total expenses and monthly cash flow (take-home − expenses). Your cash flow must be ≥ $0.', 'Compute the percent of take-home pay for needs, wants, and savings, and compare with 50/30/20.'], deliverable: 'Completed budget table with totals, cash flow, and percents.' },
      { title: 'Plan for the irregular', steps: ['List at least three irregular costs you expect in a year (gifts, car registration, renters insurance, etc.) with estimated amounts.', 'Calculate the monthly sinking-fund amount and add it to your budget.', 'Set an emergency-fund goal of 3 months of essential expenses. Starting from $1,500, how many months will it take at your savings rate? Show the inequality.'], deliverable: 'Sinking-fund table and emergency-fund timeline.' },
      { title: 'Life happens', steps: ['Your teacher will deal you three Life Happens cards.', 'For each event, calculate its effect on your cash flow or savings.', 'Revise your budget to absorb the events. Describe every change and its tradeoff.', 'Compare your original and revised budgets in a side-by-side table.'], deliverable: 'Event calculations and revised budget.' },
      { title: 'Compare two spending decisions', steps: ['Pick two choices you made (for example, car vs. transit, studio vs. shared house).', 'Calculate the annual cost difference of each choice.', 'Describe the opportunity cost: what else could that money do in a year?', 'Decide whether you would keep each choice and explain why.'], deliverable: 'Comparison table with annual costs and opportunity costs.' },
      { title: 'Present your plan', steps: ['Create a one-page budget summary or 4-slide mini presentation: career, budget breakdown chart, events and adjustments, final advice.', 'Write a 150–200 word reflection: What surprised you? What will you do differently when you start your career?'], deliverable: 'Summary or slides + reflection.' }
    ],
    reflection: ['What surprised you most about the cost of living on your own?', 'Which expense would you be most willing to cut, and which would you protect? Why?', 'How did the Life Happens events change your thinking about emergency funds?', 'What advice would you give a friend starting their first job?'],
    checklist: ['Paycheck summary and rent inequality', 'Budget table with all categories classified', 'Cash flow ≥ $0 and percent breakdown', 'Sinking fund and emergency-fund timeline', 'Three event calculations and revised budget', 'Two spending comparisons with opportunity costs', 'Summary page or slides', 'Reflection (150–200 words)'],
    teacher: {
      materials: ['Student packet (one per student)', 'Life Happens cards (cut apart) or random number generator 1–8', 'Calculators or spreadsheet software', 'Optional: chart paper or slide software for presentations'],
      pacing: [['Day 1', 'Tasks 1–2: paycheck and initial budget'], ['Day 2', 'Task 3 and deal Life Happens cards; begin Task 4'], ['Day 3', 'Finish Task 4; Task 5 comparisons'], ['Day 4 (optional)', 'Presentations / gallery walk and reflections']],
      implementation: ['Assign careers randomly so students experience a range of incomes, including tight budgets.', 'Model one full example (below) before students start Task 2.', 'Deal events after budgets are “locked” so students must genuinely adjust.', 'The higher-income nurse card includes a larger loan payment — use it to discuss that income is not the only factor.'],
      worked: [
        { task: 'Task 1 (Paralegal)', work: [`Gross monthly = 50,000 ÷ 12 = ${money(50000 / 12)}.`, `Annual deductions: federal ${money(ex.federal)}, Social Security ${money(ex.socialSecurity)}, Medicare ${money(ex.medicare)}, state ${money(ex.state)}, retirement ${money(ex.retirement)}, health ${money(ex.health)}.`, `Take-home = ${money(ex.net)} per year ÷ 12 = ${money(exNet)} per month.`, `Rent guideline: r ≤ 0.30 × ${money(50000 / 12)} = ${money(M.round2(50000 / 12 * 0.3))}.`] },
        { task: 'Task 2 (sample budget)', work: exBudget.map(x => `${x[0]}: ${$(x[1])}`).concat(`Total = ${$(exTotal)}; cash flow = ${money(exNet)} − ${$(exTotal)} = ${money(exNet - exTotal)}.`) },
        { task: 'Task 3 (emergency fund)', work: [`Essential expenses ≈ ${$(1150 + 135 + 555 + 350 + 65 + 185)} per month; 3 months = ${$(3 * (1150 + 135 + 555 + 350 + 65 + 185))}.`, `Needed beyond $1,500: ${$(3 * 2440 - 1500)}. At ${$(exBudget[8][1])} + surplus per month, months m ≥ ${$(3 * 2440 - 1500)} ÷ (monthly savings).`] },
        { task: 'Task 4 (event example)', work: ['Brakes $640: if cash flow is $40/month, the event equals 16 months of surplus — it must come from the emergency fund, then be rebuilt.', 'Hours cut 10%: take-home drops by 10%; students must reduce variable wants first.'] }
      ],
      samples: ['“Even though I chose the studio, the hours cut forced me to drop dining out from $150 to $60 and switch to the prepaid phone. I kept the car because I need it for job sites, but if the cut lasted longer I would look for a roommate.”', '“Choosing transit instead of a car saves $465 per month, or $5,580 per year — that alone would fund my emergency fund in under a year.”'],
      misconceptions: ['Budgeting from gross pay — insist on take-home.', 'Leaving savings for “whatever is left.” Savings is a line item.', 'Treating irregular costs as surprises rather than predictable expenses.', 'Assuming higher salary means an easier budget (the nurse’s loan and lifestyle choices matter).'],
      differentiation: { support: ['Provide a partially completed budget template.', 'Limit to two events.', 'Allow a calculator-based percent tool.'], extend: ['Build the budget in a spreadsheet with formulas.', 'Add a second year with a 3% raise and 4% rent increase.', 'Research actual rents in a real town and compare with Riverton.'] },
      extensions: ['Compare your budget to a classmate with a different career and write a joint memo on what made each work.', 'Research one local assistance program or employer benefit that could change your budget.']
    },
    rubric: [
      { category: 'Financial understanding', points: 20, levels: ['Correctly explains deductions, fixed/variable and need/want classifications, sinking funds, and emergency funds with precise vocabulary.', 'Mostly correct explanations with minor vocabulary errors.', 'Partial understanding; several classifications or explanations incorrect.', 'Little evidence of understanding.'] },
      { category: 'Mathematical accuracy', points: 25, levels: ['All totals, cash flow, percents, inequalities, and event calculations correct and labeled.', '1–2 minor errors that do not change conclusions.', 'Several errors or missing calculations.', 'Calculations largely missing or incorrect.'] },
      { category: 'Analysis of events & comparisons', points: 20, levels: ['Accurately quantifies every event and comparison, including annual costs and opportunity costs.', 'Analyzes most events/comparisons with minor gaps.', 'Analysis superficial or incomplete.', 'Little analysis.'] },
      { category: 'Justification of decisions', points: 15, levels: ['Every adjustment is justified with numbers and a tradeoff; considers non-financial factors.', 'Most adjustments justified.', 'Some justification, mostly opinion.', 'No justification.'] },
      { category: 'Communication & presentation', points: 10, levels: ['Organized, clear, well-labeled tables and visuals; reflection is thoughtful.', 'Clear with minor organization issues.', 'Hard to follow in places.', 'Disorganized.'] },
      { category: 'Completion', points: 10, levels: ['Every checklist item complete.', 'One item missing or incomplete.', 'Two or three items missing.', 'Most items missing.'] }
    ],
    slides: [
      { title: 'Survive on Your Salary', bullets: ['Unit 2: Budgeting & Spending', 'Draw a career · Build a budget · Survive surprises'] },
      { title: 'The situation', bullets: ['New job in Riverton', '$1,500 in savings', 'Withholding: taxes, 3% retirement, $100 health premium', 'Your job: make the money last — and grow'] },
      { title: 'Gross vs. take-home', bullets: ['Gross monthly = salary ÷ 12', 'Take-home = gross − taxes − deductions', 'Budget with take-home only', `Example: $50,000 salary → about ${money(exNet)} per month`] },
      { title: 'Build the budget', bullets: ['Pick every category from the Cost Guide', 'Classify: fixed/variable and need/want/savings', 'Cash flow must be ≥ $0', 'Compare with 50/30/20'] },
      { title: 'Plan for the irregular', bullets: ['Sinking funds: annual cost ÷ 12', 'Emergency fund: 3 months of essentials', 'Inequality: 1,500 + s·m ≥ goal'] },
      { title: 'Life happens', bullets: ['Three event cards per student', 'Quantify each event', 'Revise and explain every tradeoff'] },
      { title: 'Deliverables', bullets: ['Budget tables + calculations', 'Two spending comparisons', 'Summary page or 4 slides', 'Reflection (150–200 words)'] },
      { title: 'How you will be scored (100 pts)', bullets: ['Financial understanding 20', 'Math accuracy 25', 'Analysis 20 · Justification 15', 'Communication 10 · Completion 10'] }
    ]
  },
  {
    slug: 'twelve-month-goal-plan', title: 'The 12-Month Goal Plan', unit: 'budgeting', unitNum: 2,
    tagline: 'Help a teen reach a big savings goal in one year — with an uneven paycheck and a busy calendar.',
    grouping: 'Pairs', days: '2–3 class periods', skills: ['budgeting-skill-01', 'budgeting-skill-03', 'budgeting-skill-04'],
    intro: 'Big goals — a first car, a security deposit, a semester abroad — are reached one month at a time. In this project you and a partner act as financial coaches for Jaylen, a high school senior with a part-time job, a goal, and a calendar full of things that cost money.',
    scenario: 'Jaylen, 17, works at the Maple Falls Rec Center for $16.50 per hour and keeps about 92% after payroll taxes. Hours change with the season. Jaylen has $650 saved and wants $3,600 by next August for a used-car down payment, insurance deposit, and registration.',
    goals: ['Model income that varies month to month.', 'Plan for known irregular expenses with sinking funds.', 'Use inequalities to test whether a savings goal is reachable.', 'Compare spending choices and quantify opportunity costs.', 'Recommend and defend a realistic plan.'],
    documents: [
      { title: 'Jaylen’s expected work hours', table: { headers: ['Month', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'], rows: [['Hours', '40', '44', '40', '56', '36', '36', '40', '44', '48', '80', '96', '80']] } },
      { title: 'Jaylen’s regular monthly spending', table: { headers: ['Item', 'Monthly'], rows: [['Phone (share of family plan)', '$30'], ['Food & snacks out', '$85'], ['Streaming & games', '$24'], ['Gas money to friends', '$20'], ['Clothes', '$40']] } },
      { title: 'Known irregular expenses', table: { headers: ['Month', 'Expense', 'Cost'], rows: [['Oct', 'Homecoming', '$140'], ['Dec', 'Holiday gifts', '$220'], ['Feb', 'School trip', '$180'], ['Apr', 'Prom', '$310'], ['Jun', 'Graduation photos & party contribution', '$150'], ['Jul', 'Birthday trip with friends', '$200']] } },
      { title: 'Two spending decisions Jaylen is considering', table: { headers: ['Decision', 'Option 1', 'Option 2'], rows: [['Phone', 'Keep family plan share $30/mo', 'Own unlimited plan $65/mo'], ['Lunch', 'Buy lunch 3×/week at $9.50', 'Pack lunch, about $3 each']] } }
    ],
    tasks: [
      { title: 'Model the income', steps: ['For each month, compute take-home pay = hours × $16.50 × 0.92 (round to cents).', 'Find total take-home pay for the year and the average per month.', 'Identify Jaylen’s three lowest-income months.'], deliverable: '12-month income table.' },
      { title: 'Build the monthly cash-flow table', steps: ['For each month: take-home − regular spending − irregular expenses = amount available to save.', 'Track a running savings balance starting at $650.', 'Mark any month with negative cash flow.'], deliverable: 'Cash-flow table with running balance.' },
      { title: 'Test the goal', steps: ['Does the balance reach $3,600 by the end of August? By how much is Jaylen over or short?', 'Write and solve an inequality for the extra average amount per month (x) needed: final balance + 12x ≥ 3,600.', 'Use sinking funds: how much should Jaylen set aside each month starting in September to cover all irregular expenses evenly?'], deliverable: 'Goal analysis with inequality and sinking-fund amount.' },
      { title: 'Compare spending decisions', steps: ['Compute the yearly cost difference for the phone decision and the lunch decision (36 school weeks for lunch).', 'Explain the opportunity cost of each in terms of the goal.', 'Recommend which changes Jaylen should make and show the new year-end balance.'], deliverable: 'Comparison table and recommendation.' },
      { title: 'Coach’s memo', steps: ['Write a one-page memo to Jaylen: the plan, the monthly savings targets, the riskiest months, and a backup plan if hours are cut.', 'Include at least one chart (running balance by month).'], deliverable: 'Memo with chart.' }
    ],
    reflection: ['Why is a goal with uneven income harder to plan for?', 'Which change had the biggest impact for the least sacrifice?', 'How could you use this method for one of your own goals?'],
    checklist: ['Income table (12 months)', 'Cash-flow table with running balance', 'Goal test and inequality', 'Sinking-fund calculation', 'Two spending comparisons', 'Coach’s memo with chart', 'Reflection'],
    teacher: {
      materials: ['Student packet', 'Calculators or spreadsheet', 'Graph paper or charting tool'],
      pacing: [['Day 1', 'Tasks 1–2'], ['Day 2', 'Tasks 3–4'], ['Day 3 (optional)', 'Memo and peer review']],
      implementation: ['Encourage a spreadsheet: the running balance is a natural formula exercise.', 'Pairs should divide months, then check each other’s work.', 'Discuss why summer months carry the plan.'],
      worked: (() => {
        const hrs = [40, 44, 40, 56, 36, 36, 40, 44, 48, 80, 96, 80], reg = 199, irr = [0, 140, 0, 220, 0, 180, 0, 310, 0, 150, 200, 0];
        let bal = 650; const lines = []; const mo = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'];
        let totInc = 0;
        hrs.forEach((h, i) => { const inc = M.round2(h * 16.5 * 0.92); totInc += inc; const cf = M.round2(inc - reg - irr[i]); bal = M.round2(bal + cf); lines.push(`${mo[i]}: ${h} h → ${money(inc)}; − $199 − ${$(irr[i])} = ${money(cf)}; balance ${money(bal)}`); });
        const short = M.round2(3600 - bal);
        return [{ task: 'Tasks 1–2', work: lines.concat(`Total take-home ${money(totInc)}; average ${money(totInc / 12)}/month.`) },
          { task: 'Task 3', work: [short > 0 ? `Year-end balance ${money(bal)} is ${money(short)} short of $3,600.` : `Year-end balance ${money(bal)} exceeds $3,600 by ${money(-short)}.`, short > 0 ? `${money(bal)} + 12x ≥ 3,600 → x ≥ ${money(short / 12)} per month.` : 'No extra savings needed, but the margin is thin.', 'Irregular total $1,200 ÷ 12 = $100 per month sinking fund.'] },
          { task: 'Task 4', work: ['Phone: ($65 − $30) × 12 = $420 more per year for the unlimited plan.', 'Lunch: (9.50 − 3.00) × 3 × 36 = $702 per year saved by packing.', 'Packing lunch alone covers most of any shortfall.'] }];
      })(),
      samples: ['“Jaylen should keep the family phone plan and pack lunch at least three days a week. Those two choices save $1,122 a year and turn a shortfall into a cushion. The riskiest months are December and April, when expenses spike; the sinking fund smooths them out.”'],
      misconceptions: ['Using gross pay (forgetting the 92%).', 'Treating the average month as typical — summer income is not available in December.', 'Forgetting to carry the running balance forward.'],
      differentiation: { support: ['Provide the income column precomputed for the first three months.', 'Use a fill-in running-balance template.'], extend: ['Add a 4.00% APY savings account (monthly interest).', 'Model a 20% cut in summer hours and design a backup plan.'] },
      extensions: ['Students create a 12-month plan for a goal of their own using fictional numbers.']
    },
    rubric: [
      { category: 'Financial understanding', points: 20, levels: ['Explains variable income, sinking funds, and opportunity cost accurately.', 'Minor gaps.', 'Partial understanding.', 'Little understanding.'] },
      { category: 'Mathematical accuracy', points: 25, levels: ['Income, cash flow, running balance, and inequality all correct.', '1–2 minor errors.', 'Several errors.', 'Mostly incorrect.'] },
      { category: 'Analysis', points: 20, levels: ['Identifies risky months, quantifies both decisions, tests the goal precisely.', 'Most analysis complete.', 'Superficial.', 'Missing.'] },
      { category: 'Justification', points: 15, levels: ['Recommendation backed by numbers and realistic tradeoffs; includes a backup plan.', 'Mostly justified.', 'Weak justification.', 'None.'] },
      { category: 'Communication', points: 10, levels: ['Clear memo and labeled chart.', 'Minor issues.', 'Hard to follow.', 'Disorganized.'] },
      { category: 'Completion & collaboration', points: 10, levels: ['All items complete; both partners contributed.', 'One item missing.', 'Several missing.', 'Mostly missing.'] }
    ],
    slides: [
      { title: 'The 12-Month Goal Plan', bullets: ['Unit 2: Budgeting & Spending', 'Coach Jaylen to a $3,600 goal'] },
      { title: 'Meet Jaylen', bullets: ['$16.50/hour, keeps 92%', 'Hours change by season', '$650 saved', 'Goal: $3,600 by August'] },
      { title: 'The plan in four steps', bullets: ['Model the income', 'Track monthly cash flow', 'Test the goal with an inequality', 'Compare spending choices'] },
      { title: 'Key math', bullets: ['Take-home = hours × 16.50 × 0.92', 'Balance(next) = balance + cash flow', 'Sinking fund = total irregular ÷ 12', 'final + 12x ≥ 3,600'] },
      { title: 'Deliverables', bullets: ['Income and cash-flow tables', 'Goal test and comparisons', 'Coach’s memo with chart'] },
      { title: 'Scoring (100 pts)', bullets: ['Understanding 20 · Accuracy 25', 'Analysis 20 · Justification 15', 'Communication 10 · Completion 10'] }
    ]
  }
];
