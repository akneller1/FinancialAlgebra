/* Four new skills added 2026-11-16 (one per unit), so the course covers topics most personal finance
 * standards include: credit scores and reports, the full cost of owning a car, renting, and scams/identity theft.
 * Each entry is merged into its unit by scripts/build-banks.mjs and adds skill 5 to src/course.js.
 * Numeric answers are recomputed independently in tests/fa-new-skills.test.mjs. Legal limits cited
 * (Regulation E, Fair Credit Billing Act) are federal rules, current as of November 2026. */
import { M, money, $, $0, pct, person, mc, numeric, table } from './kit.mjs';
const r2 = M.round2;
const pick = (list, k) => list[k % list.length];

/* ---------- Credit Cards & Debt · skill 5: credit scores and reports ---------- */
const credit = {
  skillName: 'Understand credit scores and reports',
  vocab: [
    { term: 'Credit bureau', skill: 5, def: 'A company (Equifax, Experian or TransUnion) that collects credit history and sells credit reports', example: 'Each of the three bureaus may hold slightly different information about you.' },
    { term: 'Payment history', skill: 5, def: 'The record of whether bills were paid on time; the largest factor in most credit scores', example: 'A payment 30 or more days late can stay on a report for seven years.' },
    { term: 'Hard inquiry', skill: 5, def: 'A lender’s check of your credit when you apply for new credit; it can lower a score slightly for a while', example: 'Applying for a car loan creates a hard inquiry.' },
    { term: 'Soft inquiry', skill: 5, def: 'A credit check that does not affect your score, such as checking your own report or a pre-approval offer', example: 'Looking at your own credit report is a soft inquiry.' },
    { term: 'Length of credit history', skill: 5, def: 'How long your credit accounts have been open, including the average age of accounts', example: 'Closing your oldest card can shorten your average account age.' },
    { term: 'Credit dispute', skill: 5, def: 'A request to a credit bureau to investigate and correct wrong information on your report', example: 'A late payment you never made can be disputed online with the bureau.' }
  ],
  concepts: [
    { skill: 5, q: 'Which factor usually has the biggest effect on a credit score?', a: 'Payment history', d: ['Income', 'Number of bank accounts', 'Age of the borrower'], why: 'On-time payments matter most; income is not part of a credit score.' },
    { skill: 5, q: 'Where can you get free copies of your credit reports from all three bureaus?', a: 'AnnualCreditReport.com', d: ['Any site that advertises a free score', 'Your employer', 'The IRS'], why: 'AnnualCreditReport.com is the official free source set up under federal law.' },
    { skill: 5, q: 'Select ALL items that appear on a credit report.', all: ['Credit card accounts and balances', 'Late payments', 'Loan accounts'], wrong: ['Your salary', 'Your bank account balance'], why: 'Credit reports show credit accounts and payment history, not income or savings balances.' },
    { skill: 5, q: 'Your report lists a credit card you never opened. What is the best first step?', a: 'Dispute it with the credit bureau and check for identity theft', d: ['Ignore it; it will fall off soon', 'Pay the balance to protect your score', 'Close your other cards'], why: 'An unknown account can be fraud: dispute it, and consider a fraud alert or credit freeze.' },
    { skill: 5, q: 'Checking your own credit report does what to your score?', a: 'Nothing; it is a soft inquiry', d: ['Lowers it a little', 'Raises it a little', 'Lowers it until the next statement'], why: 'Only hard inquiries from applications can affect a score.' }
  ],
  claims: [
    { skill: 5, claim: 'Checking your own credit score lowers it.', verdict: 2, model: 'Never true. Checking your own report or score is a soft inquiry and does not affect the score.', example: 'You can check your reports free at AnnualCreditReport.com without any effect.' },
    { skill: 5, claim: 'A higher credit score saves money on a loan.', verdict: 0, model: 'Always true for the same loan: a higher score generally qualifies for a lower APR, which lowers the payment and total interest.', example: '$20,000 for 60 months at 6% vs 11% APR differs by about $2,900 in interest.' }
  ],
  families: [
    { id: 'cs-score-cost', skill: 5, type: 'comparison', count: 8, gen(r) {
      const p = person(r), P = r.step(12000, 32000, 500), n = r.pick([48, 60]), good = r.pick([0.055, 0.06, 0.065]), fair = r2(good + r.pick([0.04, 0.05, 0.06]));
      const a = r2(M.loanPayment(P, good, n)), b = r2(M.loanPayment(P, fair, n)), d = r2(b * n - a * n);
      return { prompt: `With a good credit score, ${p.name} qualifies for a ${$0(P)} car loan at ${pct(good)} APR for ${n} months (${money(a)}/month). With a fair score the rate would be ${pct(fair)} (${money(b)}/month). How much more would the fair-score loan cost in total?`,
        ...numeric(d, { tolerance: 0.05 }), solutionSteps: [`Good score: ${money(a)} × ${n} = ${money(a * n)}.`, `Fair score: ${money(b)} × ${n} = ${money(b * n)}.`, `Difference = ${money(d)}. A better score is worth real money.`] }; } },
    { id: 'cs-overall-util', skill: 5, type: 'calculation', count: 7, gen(r) {
      const p = person(r), lims = [r.step(1000, 4000, 500), r.step(1500, 6000, 500)], bals = lims.map(l => r.step(0, Math.floor(l * 0.7), 10)), u = r2((bals[0] + bals[1]) / (lims[0] + lims[1]) * 100);
      return { prompt: `${p.name} has two credit cards: ${$0(bals[0])} owed on a ${$0(lims[0])} limit and ${$0(bals[1])} owed on a ${$0(lims[1])} limit. What is ${p.pos} overall credit utilization, to the nearest tenth of a percent?`,
        ...numeric(u, { unit: '%', d: 1, tolerance: 0.05 }), solutionSteps: [`Total balances = ${$0(bals[0] + bals[1])}; total limits = ${$0(lims[0] + lims[1])}.`, `Utilization = ${$0(bals[0] + bals[1])} ÷ ${$0(lims[0] + lims[1])} = ${(u / 100).toFixed(4)}.`, `≈ ${u.toFixed(1)}%. Many lenders like to see under 30%.`] }; } },
    { id: 'cs-avg-age', skill: 5, type: 'calculation', count: 6, gen(r) {
      const p = person(r), ages = [r.int(6, 12), r.int(2, 5), r.int(0, 2)], avg = r2((ages[0] + ages[1] + ages[2]) / 3), after = r2((ages[1] + ages[2]) / 2);
      return { prompt: `${p.name} has three credit accounts that are ${ages[0]}, ${ages[1]} and ${ages[2]} years old. If ${p.sub} closes the ${ages[0]}-year-old account, what will the average age of the remaining accounts be, in years?`,
        ...numeric(after, { unit: 'count', display: String(after), tolerance: 0.01 }), solutionSteps: [`Average now = (${ages.join(' + ')}) ÷ 3 = ${avg}.`, `After closing: (${ages[1]} + ${ages[2]}) ÷ 2 = ${after}.`, 'Closing the oldest account shortens credit history, which can lower a score.'] }; } },
    { id: 'cs-report-action', skill: 5, type: 'scenario', count: 6, gen(r, k) {
      const p = person(r), s = pick([
        ['a 30-day late payment on a card ' + 'that was actually paid on time', 'File a dispute with the credit bureau and include proof of the payment'],
        ['a store card that ' + 'they never applied for', 'Dispute the account and place a fraud alert or credit freeze'],
        ['a hard inquiry from a lender ' + 'they never contacted', 'Dispute the inquiry and check for other signs of identity theft'],
        ['an old address and a correct, paid-off car loan', 'Nothing urgent: accurate paid accounts and old addresses are normal'],
        ['the same collection debt listed twice', 'Dispute the duplicate entry with the bureau'],
        ['a balance that is ' + '$400 higher than the latest statement', 'Compare with the statement date; dispute only if the balance was reported wrong']
      ], k);
      const others = ['Pay whatever the report says to avoid trouble', 'Close all credit cards right away', 'Wait seven years for it to disappear', 'Apply for a new card to raise the score'];
      return { prompt: `${p.name} checks ${p.pos} free credit report and finds ${s[0]}. What should ${p.sub} do?`, ...mc(r, s[1], r.sample(others, 3)), solutionSteps: [s[1] + '.', 'Disputes are free; bureaus must investigate, usually within 30 days.', 'Check all three bureaus, since each report can differ.'] }; } }
  ],
  lesson: { skill: 5, title: 'Credit Scores and Credit Reports', minutes: 50,
    objectives: ['Name the factors that drive a credit score and their relative weight.', 'Read a credit report and spot errors or signs of fraud.', 'Calculate how a credit score changes the cost of a loan.'],
    vocab: ['Credit bureau', 'Payment history', 'Hard inquiry', 'Soft inquiry', 'Length of credit history', 'Credit dispute'],
    hook: 'Same car, same price, same income: one buyer pays almost $2,900 more in interest. Why?',
    notes: [{ h: 'What a score measures', body: 'Payment history (largest), amounts owed and utilization, length of history, new credit, credit mix. Income and savings are not included.' }, { h: 'Reports vs scores', body: 'A report is the record; a score is a number calculated from it. Free reports from all three bureaus at AnnualCreditReport.com.' }, { h: 'Fixing errors', body: 'Dispute wrong items with the bureau; it must investigate. Unknown accounts may mean identity theft.' }],
    examples: [{ problem: '$20,000 car loan, 60 months: 6% APR vs 11% APR.', steps: ['6%: payment ≈ $386.66, total ≈ $23,199.60', '11%: payment ≈ $434.85, total ≈ $26,091.00'], answer: 'The lower score costs about $2,891 more.' }],
    discussion: ['Why might a landlord or insurer look at credit history?'],
    misconceptions: [['Checking my own score lowers it.', 'Checking your own report or score is a soft inquiry with no effect.'], ['Income is part of a credit score.', 'Scores use credit history, not income.']],
    reflection: ['Which two habits would most protect your future credit score?'],
    extension: 'Compare the loan-cost difference for three score tiers on a $250,000 mortgage.',
    differentiation: { support: ['Give a labeled sample report with the five score factors color-coded.'], extend: ['Model how one late payment changes a year of costs on a credit card and a car loan.'] },
    realWorld: 'Lenders, landlords, some employers and insurers can use credit information.' }
};

/* ---------- Auto Loans & Borrowing · skill 5: total cost of car ownership ---------- */
const borrowing = {
  skillName: 'Calculate the total cost of car ownership',
  vocab: [
    { term: 'Liability insurance', skill: 5, def: 'Car insurance that pays for injuries and damage you cause to others; required by law in most states', example: 'It pays for the other driver’s car, not yours.' },
    { term: 'Collision coverage', skill: 5, def: 'Car insurance that pays to repair your own car after a crash, minus the deductible', example: 'A $500 deductible on a $3,200 repair pays $2,700.' },
    { term: 'Comprehensive coverage', skill: 5, def: 'Car insurance for non-crash damage such as theft, hail, fire or hitting a deer', example: 'A cracked windshield from hail.' },
    { term: 'Fuel economy (MPG)', skill: 5, def: 'Miles a car travels per gallon of fuel', example: '12,000 miles at 30 MPG uses 400 gallons.' },
    { term: 'Cost per mile', skill: 5, def: 'Total yearly cost of owning a car divided by the miles driven', example: '$7,200 ÷ 12,000 miles = $0.60 per mile.' }
  ],
  concepts: [
    { skill: 5, q: 'Select ALL costs that are part of owning a car besides the loan payment.', all: ['Insurance', 'Fuel', 'Maintenance and repairs', 'Registration and fees'], wrong: ['The sticker price paid again each year', 'Sales tax every month'], why: 'Total cost of ownership adds insurance, fuel, upkeep, fees and depreciation to financing.' },
    { skill: 5, q: 'Which kind of car insurance pays for damage you cause to someone else?', a: 'Liability', d: ['Collision', 'Comprehensive', 'Gap'], why: 'Liability covers others; collision and comprehensive cover your own car.' },
    { skill: 5, q: 'Why does a new car usually lose value fastest in its first few years?', a: 'Depreciation is steepest early in a car’s life', d: ['Insurance stops covering it', 'The loan rate rises', 'Fuel economy falls by half'], why: 'Cars commonly lose a large share of value in the first years.' }
  ],
  claims: [
    { skill: 5, claim: 'The car with the lower price is cheaper to own.', verdict: 1, model: 'Sometimes. Fuel, insurance, repairs and depreciation can make a cheaper car cost more over several years.', example: 'A $2,000 cheaper car that gets 22 MPG instead of 35 MPG spends about $700 more on fuel per year at 12,000 miles and $3.50/gal.' }
  ],
  families: [
    { id: 'tco-annual', skill: 5, type: 'calculation', count: 8, gen(r) {
      const p = person(r), pay = r.step(240, 520, 0.01), ins = r.step(90, 220, 1), miles = r.step(8000, 15000, 500), mpg = r.pick([24, 28, 30, 32, 36]), gas = r.pick([3.1, 3.25, 3.4, 3.6]), maint = r.step(500, 1400, 50);
      const fuel = r2(miles / mpg * gas), tot = r2(pay * 12 + ins * 12 + fuel + maint);
      return { prompt: `${p.name}'s car costs ${money(pay)}/month for the loan and ${$(ins)}/month for insurance. ${p.Sub} drives ${miles.toLocaleString('en-US')} miles a year at ${mpg} MPG with gas at ${money(gas)}/gallon, and budgets ${$0(maint)} a year for maintenance. What is the total yearly cost?`,
        ...numeric(tot, { tolerance: 0.02 }), solutionSteps: [`Loan + insurance = (${money(pay)} + ${$(ins)}) × 12 = ${money((pay + ins) * 12)}.`, `Fuel = ${miles.toLocaleString('en-US')} ÷ ${mpg} × ${money(gas)} = ${money(fuel)}.`, `Total = ${money((pay + ins) * 12)} + ${money(fuel)} + ${$0(maint)} = ${money(tot)}.`] }; } },
    { id: 'fuel-compare', skill: 5, type: 'comparison', count: 7, gen(r) {
      const p = person(r), miles = r.step(9000, 16000, 500), a = r.pick([22, 24, 26]), b = r.pick([34, 38, 42, 48]), gas = r.pick([3.2, 3.45, 3.75]), d = r2(miles / a * gas - miles / b * gas);
      return { prompt: `${p.name} drives ${miles.toLocaleString('en-US')} miles a year. Car A gets ${a} MPG and Car B gets ${b} MPG. With gas at ${money(gas)}/gallon, how much less does Car B spend on fuel per year?`,
        ...numeric(d, { tolerance: 0.02 }), solutionSteps: [`Car A: ${miles.toLocaleString('en-US')} ÷ ${a} × ${money(gas)} = ${money(miles / a * gas)}.`, `Car B: ${miles.toLocaleString('en-US')} ÷ ${b} × ${money(gas)} = ${money(miles / b * gas)}.`, `Savings = ${money(d)} per year.`] }; } },
    { id: 'car-depreciate', skill: 5, type: 'calculation', count: 6, gen(r) {
      const price = r.step(18000, 42000, 500), rate = r.pick([0.12, 0.15, 0.18, 0.2]), y = r.pick([3, 4, 5]), v = r2(price * (1 - rate) ** y);
      return { prompt: `A new car costs ${$0(price)} and loses ${pct(rate, 0)} of its value each year. What is it worth after ${y} years?`,
        ...numeric(v), solutionSteps: [`Value = ${$0(price)} × (1 − ${rate})^${y}.`, `= ${$0(price)} × ${((1 - rate) ** y).toFixed(4)} = ${money(v)}.`, `Depreciation over ${y} years = ${money(price - v)}, a real cost of ownership.`] }; } },
    { id: 'cost-mile', skill: 5, type: 'calculation', count: 6, gen(r) {
      const p = person(r), tot = r.step(5400, 11000, 50), miles = r.step(8000, 16000, 500), cpm = r2(tot / miles);
      return { prompt: `Owning ${p.pos} car costs ${p.name} ${$0(tot)} a year in total, and ${p.sub} drives ${miles.toLocaleString('en-US')} miles. What is the cost per mile?`,
        ...numeric(cpm), solutionSteps: [`Cost per mile = ${$0(tot)} ÷ ${miles.toLocaleString('en-US')}.`, `= ${money(cpm)} per mile.`, 'Use cost per mile to compare driving with transit or rideshare.'] }; } }
  ],
  lesson: { skill: 5, title: 'What a Car Really Costs', minutes: 55,
    objectives: ['List the costs of owning a car beyond the payment.', 'Calculate yearly fuel, insurance and maintenance costs and cost per mile.', 'Compare two cars by total cost of ownership.'],
    vocab: ['Liability insurance', 'Collision coverage', 'Comprehensive coverage', 'Fuel economy (MPG)', 'Cost per mile'],
    hook: 'The ad says “Only $299 a month!” Ask: what will this car really cost you each year?',
    notes: [{ h: 'Total cost of ownership', body: 'Payment + insurance + fuel + maintenance + registration/fees + depreciation.' }, { h: 'Fuel', body: 'Gallons = miles ÷ MPG; fuel cost = gallons × price per gallon.' }, { h: 'Insurance types', body: 'Liability covers others (required in most states); collision and comprehensive cover your car, minus a deductible.' }],
    examples: [{ problem: '$350/month loan, $140/month insurance, 12,000 miles at 30 MPG and $3.40/gal, $900 maintenance.', steps: ['(350 + 140) × 12 = $5,880', '12,000 ÷ 30 × 3.40 = $1,360', '5,880 + 1,360 + 900 = $8,140'], answer: '$8,140 per year, about $0.68 per mile.' }],
    discussion: ['When might a more expensive car be the better deal?'],
    misconceptions: [['The monthly payment is the cost of the car.', 'Insurance, fuel, upkeep and depreciation often add thousands per year.']],
    reflection: ['What monthly amount would you set aside for car costs besides the payment?'],
    extension: 'Compare total five-year cost of a new and a three-year-old used version of the same model.',
    differentiation: { support: ['Provide a cost table with each category labeled.'], extend: ['Add depreciation and compare cost per mile for two cars over five years.'] },
    realWorld: 'Transportation is the second-largest expense for many households.' }
};

/* ---------- Housing · skill 5: renting ---------- */
const housing = {
  skillName: 'Plan the costs of renting',
  vocab: [
    { term: 'Rent-to-income ratio', skill: 5, def: 'Monthly rent divided by gross monthly income; a common guideline is 30% or less', example: '$1,200 ÷ $4,000 = 30%.' },
    { term: 'Prorated rent', skill: 5, def: 'Rent charged only for the days you live in a unit during a partial month', example: 'Moving in on the 21st of a 30-day month: 10 of 30 days.' },
    { term: 'Move-in costs', skill: 5, def: 'Money due before moving in, such as first month’s rent, a security deposit and fees', example: 'Rent + deposit + application fee + moving truck.' },
    { term: 'Normal wear and tear', skill: 5, def: 'Expected aging of a rental from ordinary use, which cannot be deducted from a security deposit', example: 'Faded paint is wear and tear; a hole in the wall is damage.' },
    { term: 'Roommate agreement', skill: 5, def: 'A written plan for how roommates split rent, utilities and responsibilities', example: 'Larger bedroom pays 55% of rent.' }
  ],
  concepts: [
    { skill: 5, q: 'What does renters insurance usually cover?', a: 'Your belongings and your liability, not the building', d: ['The building’s roof and walls', 'Late rent payments', 'Your security deposit'], why: 'The landlord insures the building; renters insurance covers your stuff and liability.' },
    { skill: 5, q: 'Which charge can a landlord usually deduct from a security deposit?', a: 'Repairing a hole punched in a wall', d: ['Repainting faded walls after five years', 'Replacing carpet worn by normal use', 'Cleaning normal dust'], why: 'Deposits can cover damage beyond normal wear and tear.' },
    { skill: 5, q: 'Select ALL items to check before signing a lease.', all: ['Length of the lease', 'Which utilities are included', 'Rules on pets and guests', 'Penalty for breaking the lease'], wrong: ['The landlord’s credit score', 'Your future employer'], why: 'A lease is a contract; read terms, costs and penalties first.' }
  ],
  claims: [
    { skill: 5, claim: 'Renting is just throwing money away.', verdict: 1, model: 'Sometimes. Rent buys housing with low upfront cost and flexibility; owning builds equity but adds taxes, upkeep and closing costs. Which is better depends on time horizon and costs.', example: 'Moving after two years, closing costs and fees can exceed the equity built.' }
  ],
  families: [
    { id: 'rent-30', skill: 5, type: 'calculation', count: 7, gen(r) {
      const p = person(r), hourly = r.pick([16, 17.5, 19, 21, 24, 26.5]), mo = r2(hourly * 40 * 52 / 12), cap = r2(mo * 0.3);
      return { prompt: `${p.name} earns ${money(hourly)} per hour, 40 hours a week, 52 weeks a year. Using the guideline that rent should be at most 30% of gross monthly income, what is the most ${p.sub} should pay in rent?`,
        ...numeric(cap), solutionSteps: [`Gross yearly = ${money(hourly)} × 40 × 52 = ${money(hourly * 40 * 52)}.`, `Monthly = ÷ 12 = ${money(mo)}.`, `30% × ${money(mo)} = ${money(cap)}.`] }; } },
    { id: 'move-in', skill: 5, type: 'calculation', count: 7, gen(r) {
      const p = person(r), rent = r.step(850, 1900, 25), dep = r.pick([1, 1.5]) * rent, app = r.pick([35, 50, 75]), truck = r.step(90, 300, 5), last = r.next() < 0.4, tot = r2(rent * (last ? 2 : 1) + dep + app + truck);
      return { prompt: `${p.name} is renting an apartment for ${$(rent)}/month. Due before move-in: first month's rent${last ? ', last month’s rent' : ''}, a security deposit of ${$(dep)}, a ${$(app)} application fee, and ${$(truck)} for a moving truck. How much cash does ${p.sub} need?`,
        ...numeric(tot), solutionSteps: [`Rent due up front = ${$(rent)}${last ? ' × 2 = ' + money(rent * 2) : ''}.`, `Add deposit, fee and truck: ${$(dep)} + ${$(app)} + ${$(truck)}.`, `Total = ${money(tot)}.`] }; } },
    { id: 'prorate', skill: 5, type: 'calculation', count: 7, gen(r) {
      const p = person(r), rent = r.step(900, 2100, 25), days = r.pick([30, 31]), day = r.int(5, 25), stay = days - day + 1, pr = r2(rent / days * stay);
      return { prompt: `${p.name} moves in on day ${day} of a ${days}-day month. Rent is ${$(rent)}/month, prorated by the day (including move-in day). What is the first month's prorated rent?`,
        ...numeric(pr), solutionSteps: [`Days lived = ${days} − ${day} + 1 = ${stay}.`, `Daily rent = ${$(rent)} ÷ ${days} = ${money(rent / days)}.`, `Prorated rent = ${$(rent)} × ${stay}/${days} = ${money(pr)}.`] }; } },
    { id: 'roommate-split', skill: 5, type: 'calculation', count: 6, gen(r) {
      const p = person(r), rent = r.step(1400, 2800, 50), util = r.step(120, 260, 5), share = r.pick([0.4, 0.45, 0.55, 0.6]), amt = r2(rent * share + util / 2);
      return { prompt: `${p.name} and a roommate rent a two-bedroom for ${$(rent)}/month. ${p.Sub} takes the ${share > 0.5 ? 'larger' : 'smaller'} room and pays ${pct(share, 0)} of the rent; they split ${$(util)} of utilities evenly. What does ${p.name} pay each month?`,
        ...numeric(amt), solutionSteps: [`Rent share = ${pct(share, 0)} × ${$(rent)} = ${money(rent * share)}.`, `Utilities = ${$(util)} ÷ 2 = ${money(util / 2)}.`, `Total = ${money(amt)}.`] }; } },
    { id: 'deposit-back', skill: 5, type: 'calculation', count: 6, gen(r) {
      const p = person(r), dep = r.step(800, 2000, 50), clean = r.pick([0, 75, 120]), hole = r.pick([0, 150, 225]), paint = r.pick([200, 300]), back = dep - clean - hole;
      return { prompt: `${p.name} paid a ${$(dep)} security deposit. At move-out the landlord lists: cleaning beyond normal use ${$(clean)}, wall damage repair ${$(hole)}, and repainting walls faded by five years of normal use ${$(paint)}. If only damage beyond normal wear and tear can be deducted, how much should ${p.name} get back?`,
        ...numeric(back), solutionSteps: ['Faded paint after years of normal use is wear and tear, so it cannot be deducted.', `Deductions = ${$(clean)} + ${$(hole)} = ${money(clean + hole)}.`, `Refund = ${$(dep)} − ${money(clean + hole)} = ${money(back)}.`] }; } }
  ],
  lesson: { skill: 5, title: 'Renting Your First Place', minutes: 50,
    objectives: ['Apply the 30% rent guideline to an income.', 'Calculate move-in costs, prorated rent and roommate splits.', 'Explain what a lease, a security deposit and renters insurance do.'],
    vocab: ['Rent-to-income ratio', 'Prorated rent', 'Move-in costs', 'Normal wear and tear', 'Roommate agreement'],
    hook: 'A listing says $1,250/month. How much cash do you need to get the keys?',
    notes: [{ h: '30% guideline', body: 'Rent ≤ 30% of gross monthly income. Hourly × hours × 52 ÷ 12 = monthly gross.' }, { h: 'Up-front costs', body: 'First month (sometimes last), deposit, application fees, moving costs, utility deposits.' }, { h: 'Getting the deposit back', body: 'Document the unit at move-in with photos; deposits cover damage, not normal wear and tear.' }],
    examples: [{ problem: 'Move in on the 18th of a 30-day month; rent $1,350.', steps: ['Days = 30 − 18 + 1 = 13', '1,350 × 13/30 = $585'], answer: '$585 prorated rent' }],
    discussion: ['What should roommates agree on in writing before signing a lease together?'],
    misconceptions: [['The landlord’s insurance covers my belongings.', 'It covers the building; renters insurance covers your belongings.']],
    reflection: ['How many months of rent would you want saved before moving out?'],
    extension: 'Compare a cheaper apartment farther away with commuting costs against a closer, pricier one.',
    differentiation: { support: ['Give a move-in checklist with blanks for each cost.'], extend: ['Build a first-year housing budget including utilities and renters insurance.'] },
    realWorld: 'About a third of U.S. households rent their homes.' }
};

/* ---------- Banking & Saving · skill 5: scams and identity protection ---------- */
const banking = {
  skillName: 'Spot scams and protect your identity',
  vocab: [
    { term: 'Phishing', skill: 5, def: 'A message that pretends to be from a trusted company to trick you into sharing passwords or account numbers', example: 'A text says your bank account is locked and links to a fake login page.' },
    { term: 'Identity theft', skill: 5, def: 'When someone uses your personal information, such as your Social Security number, to open accounts or make charges', example: 'A credit card is opened in your name without your knowledge.' },
    { term: 'Credit freeze', skill: 5, def: 'A free block that stops lenders from viewing your credit report, so new accounts cannot be opened in your name', example: 'You can lift the freeze when you apply for a loan.' },
    { term: 'Fraud alert', skill: 5, def: 'A note on your credit report telling lenders to verify your identity before opening credit', example: 'Placing an alert with one bureau notifies the other two.' },
    { term: 'Fake check scam', skill: 5, def: 'A scam where you deposit a check, send part of the money back, and later the check bounces', example: 'An “overpayment” for something you sold online.' }
  ],
  concepts: [
    { skill: 5, q: 'Your bank calls and asks you to confirm your PIN to stop a fraud alert. What should you do?', a: 'Hang up and call the number on the back of your card', d: ['Give the PIN so the alert is cleared', 'Give only the last two digits', 'Text the PIN instead'], why: 'Banks do not ask for your PIN; scammers fake caller ID.' },
    { skill: 5, q: 'Select ALL warning signs of a scam.', all: ['Pressure to act right now', 'Payment by gift card or wire', 'A request to keep it secret'], wrong: ['A receipt emailed after a store purchase', 'A statement you can view by logging in yourself'], why: 'Urgency, unusual payment methods and secrecy are classic red flags.' },
    { skill: 5, q: 'Which federal site helps you report identity theft and make a recovery plan?', a: 'IdentityTheft.gov', d: ['Any site that offers a free credit score', 'Your social media account', 'The company that called you'], why: 'IdentityTheft.gov is run by the Federal Trade Commission.' }
  ],
  claims: [
    { skill: 5, claim: 'If a check has cleared in my account, it cannot bounce.', verdict: 2, model: 'Never safe to assume. Banks make deposited funds available quickly, but a fake check can be returned days or weeks later, and you owe the money back.', example: 'Deposit a $2,400 fake check, send back $1,900: when it bounces you lose the $1,900 plus fees.' }
  ],
  families: [
    { id: 'fake-check', skill: 5, type: 'calculation', count: 7, gen(r) {
      const p = person(r), item = r.pick(['a bike', 'a used phone', 'a guitar', 'concert tickets']), price = r.step(150, 600, 10), check = r2(price + r.step(800, 2200, 50)), fee = r.pick([15, 25, 35]), loss = r2(check - price + fee);
      return { prompt: `${p.name} sells ${item} online for ${$(price)}. The buyer mails a check for ${$(check)} and asks ${p.obj} to send back the extra by gift card. ${p.Sub} does. A week later the check bounces and the bank charges a ${$(fee)} returned-check fee. How much money does ${p.name} lose (not counting the item)?`,
        ...numeric(loss), solutionSteps: [`Amount sent back = ${$(check)} − ${$(price)} = ${money(check - price)}.`, `The fake check is reversed, so that money was ${p.pos} own. Add the fee: ${money(check - price)} + ${$(fee)} = ${money(loss)}.`, 'Never accept overpayment and send money back; a legitimate buyer pays the exact price.'] }; } },
    { id: 'debit-liability', skill: 5, type: 'calculation', count: 7, gen(r) {
      const p = person(r), stolen = r.step(300, 1800, 10), when = r.pick([['within two business days of learning of the theft', 50], ['five days after learning of the theft, but within 60 days of the statement', 500]]), owe = Math.min(stolen, when[1]);
      return { prompt: `A thief uses ${p.name}'s lost debit card for ${$(stolen)} of purchases. Under federal Regulation E, liability is at most $50 if reported within two business days and at most $500 if reported later but within 60 days of the statement. ${p.Sub} reports it ${when[0]}. What is the most ${p.sub} can lose?`,
        ...numeric(owe), solutionSteps: [`Reported ${when[0].startsWith('within two') ? 'within two business days' : 'after two business days but within 60 days'}: limit ${$(when[1])}.`, `Loss is the smaller of ${$(stolen)} and ${$(when[1])} = ${money(owe)}.`, 'Report a lost card immediately; credit cards cap liability at $50 regardless.'] }; } },
    { id: 'credit-vs-debit', skill: 5, type: 'comparison', count: 6, gen(r) {
      const p = person(r), stolen = r.step(700, 2400, 10), debit = Math.min(stolen, 500), credit = Math.min(stolen, 50), d = debit - credit;
      return { prompt: `${p.name}'s card is stolen and used for ${$(stolen)}. ${p.Sub} reports it after four days. If it were a debit card, liability could reach $500 (Regulation E); a credit card's liability is capped at $50 (Fair Credit Billing Act). How much more could ${p.sub} lose with the debit card?`,
        ...numeric(d), solutionSteps: [`Debit: smaller of ${$(stolen)} and $500 = ${$(debit)}.`, `Credit: smaller of ${$(stolen)} and $50 = ${$(credit)}.`, `Difference = ${money(d)}. Debit fraud also takes money from your checking account while it is investigated.`] }; } },
    { id: 'scam-spot', skill: 5, type: 'scenario', count: 8, gen(r, k) {
      const p = person(r), s = pick([
        ['a text saying a package could not be delivered, with a link to pay a $1.99 fee', 'Do not click; check the tracking number on the shipper’s own site'],
        ['an email from “Lakeview Credit Union Security” sent from lakeview-cu-support.net asking to verify a login', 'Do not use the link; log in through the bank’s app or known website'],
        ['a caller who says they are from the IRS and demands payment in gift cards today', 'Hang up: government agencies do not demand gift cards'],
        ['a job offer that pays $600 a week to reship packages from home, starting before any interview', 'Decline: reshipping jobs are a common way to move stolen goods'],
        ['a message from a “friend” on social media asking to borrow money through a payment app urgently', 'Contact the friend another way to confirm before sending anything'],
        ['a pop-up saying the computer has a virus and to call a support number', 'Close the browser and do not call; real security warnings do not ask you to phone'],
        ['an offer to “pay off your student loans” for an upfront fee', 'Decline and contact the loan servicer directly; you never need to pay for help with federal loans'],
        ['a seller who will only take payment by wire transfer for a car priced far below market', 'Walk away: a too-good price plus wire-only payment is a scam pattern']
      ], k);
      const wrong = ['Reply with the information they ask for so it is resolved', 'Send a small payment to test whether it is real', 'Forward it to friends to ask what they think first', 'Follow the instructions quickly before the deadline'];
      return { prompt: `${p.name} receives ${s[0]}. What is the best response?`, ...mc(r, s[1], r.sample(wrong, 3)), solutionSteps: [s[1] + '.', 'Red flags: urgency, unusual payment methods, links or numbers you did not look up yourself.', 'Report scams at ReportFraud.ftc.gov.'] }; } }
  ],
  lesson: { skill: 5, title: 'Scams, Fraud and Protecting Your Identity', minutes: 50,
    objectives: ['Recognize the warning signs of common scams.', 'Explain liability limits for lost or stolen debit and credit cards.', 'Describe a credit freeze, a fraud alert and steps to recover from identity theft.'],
    vocab: ['Phishing', 'Identity theft', 'Credit freeze', 'Fraud alert', 'Fake check scam'],
    hook: 'Show three messages (one real, two fake). Students vote which to trust and explain the clues.',
    notes: [{ h: 'Red flags', body: 'Urgency, secrecy, payment by gift card, wire or crypto, links you did not ask for, overpayments.' }, { h: 'Liability limits', body: 'Debit (Regulation E): $50 if reported within two business days, up to $500 within 60 days of the statement. Credit cards: $50 maximum.' }, { h: 'If it happens', body: 'Contact the bank, freeze credit at all three bureaus (free), and use IdentityTheft.gov for a recovery plan.' }],
    examples: [{ problem: 'A $2,000 fake check for a $300 item; you send back $1,700.', steps: ['Check bounces: the $2,000 is removed', 'You already sent $1,700 of your own money'], answer: 'You lose $1,700 plus any bank fees.' }],
    discussion: ['Why do scammers ask for gift cards or wire transfers instead of credit cards?'],
    misconceptions: [['If my bank shows the money, the check is good.', 'Funds can be available before a check is verified; it can still bounce later.']],
    reflection: ['What two settings or habits will you use to protect your accounts?'],
    extension: 'Research the steps to place and lift a credit freeze at one bureau and make a how-to card.',
    differentiation: { support: ['Give a red-flag checklist to use while sorting sample messages.'], extend: ['Compare the cost of fraud on debit vs credit cards in several scenarios.'] },
    realWorld: 'Consumers reported losing more than $12 billion to fraud in 2024, according to the Federal Trade Commission.' }
};

export const newSkills = { credit, borrowing, housing, banking };
