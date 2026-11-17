/* Applied scenario families added 2026-11-16 to replace term-matching and "which term is illustrated" recall.
 * Every answer is computed from the inputs here (and, where one exists, the course finance library FA_MATH);
 * tests/fa-applied.test.mjs recomputes each answer independently from the numbers in the prompt.
 * Merged into each unit's families by scripts/build-banks.mjs. */
import { M, money, $, $0, pct, person, mc, numeric, table } from './kit.mjs';
import { TAX_2026 } from './real-data-2026.mjs';

const r2 = M.round2;
const usd = (x) => money(x);
const pctText = (x, d = 1) => pct(x, d);

/* ---------- Unit 1: Careers & Income ---------- */
const income = [
  { id: 'commission-month', skill: 1, type: 'calculation', count: 7, gen(r) {
    const p = person(r), base = r.step(1800, 2800, 50), rate = r.pick([0.03, 0.04, 0.05, 0.06]), sales = r.step(18000, 60000, 500);
    const pay = r2(base + rate * sales);
    return { prompt: `${p.name} sells furniture for a base salary of ${$(base)} per month plus ${pctText(rate, 0)} commission on sales. Last month ${p.sub} sold ${$(sales)}. What was ${p.pos} gross pay for the month?`,
      ...numeric(pay), solutionSteps: [`Commission = ${pctText(rate, 0)} × ${$(sales)} = ${money(rate * sales)}.`, `Gross pay = base + commission = ${$(base)} + ${money(rate * sales)} = ${money(pay)}.`, 'Commission pay rises and falls with sales, so a budget should plan around the base salary.'] }; } },
  { id: 'fica-check', skill: 2, type: 'calculation', count: 7, gen(r) {
    const p = person(r), gross = r.step(900, 2600, 0.5), ss = r2(gross * 0.062), med = r2(gross * 0.0145), tot = r2(ss + med);
    return { prompt: `${p.name}'s gross pay this period is ${money(gross)}. How much is withheld for FICA (Social Security 6.2% plus Medicare 1.45%)?`,
      ...numeric(tot), solutionSteps: [`Social Security: 6.2% × ${money(gross)} = ${money(ss)}.`, `Medicare: 1.45% × ${money(gross)} = ${money(med)}.`, `FICA = ${money(ss)} + ${money(med)} = ${money(tot)} (7.65% of gross).`], misconceptions: ['Using only the Social Security rate, or applying FICA to net pay instead of gross pay.'] }; } },
  { id: 'ytd-periods', skill: 3, type: 'calculation', count: 7, gen(r) {
    const p = person(r), freq = r.pick([['biweekly', 26], ['weekly', 52], ['semimonthly', 24]]), per = r.step(780, 2400, 0.5), n = r.int(5, Math.min(freq[1] - 2, 20));
    const ytd = r2(per * n);
    return { prompt: `${p.name}'s ${freq[0]} pay stub shows gross pay of ${money(per)} this period and year-to-date gross pay of ${money(ytd)}. If every paycheck has been the same, how many paychecks has ${p.sub} received so far this year, including this one?`,
      ...numeric(n, { unit: 'count', display: String(n) }), solutionSteps: [`Year-to-date ÷ per-period amount = ${money(ytd)} ÷ ${money(per)}.`, `= ${n} paychecks.`, `With ${freq[1]} ${freq[0]} paychecks in a year, ${freq[1] - n} remain.`] }; } },
  { id: 'stub-net-check', skill: 3, type: 'calculation', count: 7, gen(r) {
    const p = person(r), gross = r.step(1100, 2600, 0.5), fed = r2(gross * r.pick([0.06, 0.07, 0.08, 0.09])), ss = r2(gross * 0.062), med = r2(gross * 0.0145), st = r2(gross * r.pick([0.03, 0.04, 0.05])), ret = r2(gross * r.pick([0, 0.03, 0.05]));
    const net = r2(gross - fed - ss - med - st - ret);
    return { prompt: `A pay stub lists: gross pay ${money(gross)}; federal income tax ${money(fed)}; Social Security ${money(ss)}; Medicare ${money(med)}; state tax ${money(st)}${ret ? `; 401(k) ${money(ret)}` : ''}. What net pay should the stub show?`,
      ...numeric(net), solutionSteps: [`Total deductions = ${[fed, ss, med, st, ret].filter(x => x).map(x => money(x)).join(' + ')} = ${money(gross - net)}.`, `Net pay = ${money(gross)} − ${money(gross - net)} = ${money(net)}.`, 'If the stub shows a different number, there is a payroll error to report.'] }; } },
  // #7: real 2026 federal figures, date-stamped in every prompt.
  { id: 'tax-2026', skill: 4, type: 'calculation', count: 8, gen(r) {
    const p = person(r), gross = r.step(30000, 98000, 500), taxable = Math.max(0, gross - TAX_2026.standardDeduction.single), t = M.progressiveTax(taxable, TAX_2026.bracketsSingle);
    return { prompt: `Using the ${TAX_2026.year} federal brackets for single filers (IRS figures, as of ${TAX_2026.asOf}), ${p.name} earns ${$0(gross)} and takes the ${$0(TAX_2026.standardDeduction.single)} standard deduction. What is ${p.pos} federal income tax?`,
      scenario: { table: table(['Rate', 'Taxable income (single, ' + TAX_2026.year + ')'], TAX_2026.bracketsSingle.slice(0, 4).map((b, i, a) => [pctText(b.rate, 0), (i ? $0(a[i - 1].upTo + 1) : '$0') + ' – ' + $0(b.upTo)]), `${TAX_2026.year} federal brackets, single filers (source: ${TAX_2026.source})`) },
      ...numeric(t.tax), solutionSteps: [`Taxable income = ${$0(gross)} − ${$0(TAX_2026.standardDeduction.single)} = ${$0(taxable)}.`, ...t.rows.map(x => `${pctText(x.rate, 0)} × (${$0(x.to)} − ${$0(x.from)}) = ${money(x.tax)}.`), `Total federal income tax = ${money(t.tax)}.`], misconceptions: ['Applying the top bracket rate to all taxable income.'] }; } },
  { id: 'marginal-2026', skill: 4, type: 'concept', count: 7, gen(r) {
    const p = person(r), gross = r.step(22000, 140000, 500), taxable = Math.max(0, gross - TAX_2026.standardDeduction.single), t = M.progressiveTax(taxable, TAX_2026.bracketsSingle);
    const ans = pctText(t.marginalRate, 0), d = ['10%', '12%', '22%', '24%', '32%'].filter(x => x !== ans);
    return { prompt: `In ${TAX_2026.year} (IRS figures as of ${TAX_2026.asOf}), ${p.name} is a single filer earning ${$0(gross)} who takes the ${$0(TAX_2026.standardDeduction.single)} standard deduction. What is ${p.pos} marginal tax rate?`,
      ...mc(r, ans, d), solutionSteps: [`Taxable income = ${$0(gross)} − ${$0(TAX_2026.standardDeduction.single)} = ${$0(taxable)}.`, `${$0(taxable)} falls in the ${ans} bracket of the ${TAX_2026.year} single-filer table.`, `The marginal rate applies only to the last dollars earned; the effective rate is lower (${pctText(t.effectiveRate)} of taxable income).`] }; } },
  { id: 'ss-wage-base', skill: 2, type: 'calculation', count: 6, gen(r) {
    const p = person(r), salary = r.step(150000, 260000, 1000), base = TAX_2026.socialSecurityWageBase, ss = r2(Math.min(salary, base) * 0.062);
    return { prompt: `In ${TAX_2026.year}, Social Security tax is 6.2% of wages up to ${$0(base)} (the wage base, SSA figure as of ${TAX_2026.asOf}). How much Social Security tax does ${p.name} pay on a salary of ${$0(salary)}?`,
      ...numeric(ss), solutionSteps: [salary > base ? `Only the first ${$0(base)} is taxed for Social Security.` : `${$0(salary)} is below the ${$0(base)} wage base, so all of it is taxed.`, `6.2% × ${$0(Math.min(salary, base))} = ${money(ss)}.`, 'Medicare (1.45%) has no wage base, so it applies to every dollar.'] }; } }
];

/* ---------- Unit 2: Budgeting & Spending ---------- */
const budgeting = [
  { id: 'rule-503020', skill: 1, type: 'calculation', count: 7, gen(r) {
    const p = person(r), net = r.step(2100, 4800, 25), part = r.pick([['needs', 0.5], ['wants', 0.3], ['savings and debt payments', 0.2]]), v = r2(net * part[1]);
    return { prompt: `${p.name} takes home ${$(net)} per month and follows the 50/30/20 guideline. How much should go to ${part[0]} each month?`,
      ...numeric(v), solutionSteps: ['50/30/20 means 50% needs, 30% wants, 20% savings and debt payments.', `${part[0][0].toUpperCase() + part[0].slice(1)}: ${pctText(part[1], 0)} × ${$(net)} = ${money(v)}.`, 'The guideline is a starting point; high rent may push needs above 50%.'] }; } },
  { id: 'variable-average', skill: 2, type: 'calculation', count: 7, gen(r) {
    const p = person(r), bill = r.pick(['electric', 'grocery', 'gas (fuel)', 'phone data overage']), xs = [r.step(60, 220, 0.01), r.step(60, 220, 0.01), r.step(60, 220, 0.01)], avg = r2((xs[0] + xs[1] + xs[2]) / 3);
    return { prompt: `${p.name}'s ${bill} costs for the last three months were ${xs.map(x => money(x)).join(', ')}. What monthly amount should ${p.sub} budget, using the average?`,
      ...numeric(avg), solutionSteps: [`Sum = ${money(xs[0] + xs[1] + xs[2])}.`, `Average = sum ÷ 3 = ${money(avg)}.`, 'Variable expenses change month to month, so budgets use an average (or a little more).'] }; } },
  { id: 'max-units', skill: 3, type: 'calculation', count: 7, gen(r) {
    const p = person(r), budget = r.step(180, 600, 10), fixed = r.step(25, 80, 5), each = r.pick([12.5, 14, 16.75, 18, 22.5]), n = Math.floor((budget - fixed) / each);
    return { prompt: `${p.name} has ${$(budget)} for a party. The room costs ${$(fixed)}, and each guest's meal costs ${$(each)}. Write the inequality ${fixed} + ${each}g ≤ ${budget}. What is the greatest number of guests ${p.sub} can invite?`,
      ...numeric(n, { unit: 'count', display: String(n) }), solutionSteps: [`${each}g ≤ ${budget} − ${fixed} = ${budget - fixed}.`, `g ≤ ${(budget - fixed) / each === Math.floor((budget - fixed) / each) ? n : ((budget - fixed) / each).toFixed(2)}.`, `Guests must be whole people, so round down: ${n} guests.`], misconceptions: ['Rounding up, which goes over budget.'] }; } },
  { id: 'annual-plan', skill: 4, type: 'comparison', count: 7, gen(r) {
    const p = person(r), svc = r.pick(['music streaming', 'gym', 'cloud storage', 'video streaming']), mo = r.pick([9.99, 11.99, 14.99, 24.99, 34.99]), yr = r2(mo * 12 * r.pick([0.75, 0.8, 0.83, 0.85])), save = r2(mo * 12 - yr);
    return { prompt: `A ${svc} plan costs ${money(mo)} per month or ${money(yr)} paid once per year. If ${p.name} would keep it all year, how much does the annual plan save?`,
      ...numeric(save), solutionSteps: [`Monthly for a year = ${money(mo)} × 12 = ${money(mo * 12)}.`, `Savings = ${money(mo * 12)} − ${money(yr)} = ${money(save)}.`, 'The annual plan only saves money if you would really keep the service for the whole year.'] }; } }
];

/* ---------- Unit 3: Banking & Saving ---------- */
const banking = [
  { id: 'overdraft', skill: 1, type: 'calculation', count: 7, gen(r) {
    const p = person(r), bal = r.step(40, 260, 0.01), buy = r2(bal + r.step(5, 90, 0.01)), fee = r.pick([29, 34, 35]), nb = r2(bal - buy - fee);
    return { prompt: `${p.name} has ${money(bal)} in checking and makes a ${money(buy)} debit-card purchase. The bank covers it and charges a ${$(fee)} overdraft fee. What is the new balance?`,
      ...numeric(nb), solutionSteps: [`${money(bal)} − ${money(buy)} = ${money(bal - buy)}.`, `Subtract the fee: ${money(bal - buy)} − ${$(fee)} = ${money(nb)}.`, 'A negative balance means the account owes the bank; turning off overdraft coverage would have declined the purchase.'] }; } },
  { id: 'fee-waiver', skill: 1, type: 'calculation', count: 6, gen(r) {
    const p = person(r), min = r.pick([500, 1000, 1500]), fee = r.pick([8, 10, 12, 15]), bals = Array.from({ length: 6 }, () => r.step(min - 600, min + 700, 10)), months = bals.filter(b => b < min).length, tot = months * fee;
    return { prompt: `${p.name}'s checking account charges ${$(fee)} in any month the minimum daily balance falls below ${$(min)}. Over six months the minimum balances were ${bals.map(b => $(b)).join(', ')}. What did ${p.sub} pay in monthly fees?`,
      ...numeric(tot), solutionSteps: [`Months below ${$(min)}: ${months}.`, `${months} × ${$(fee)} = ${money(tot)}.`, 'Keeping a cushion above the minimum, or choosing a no-fee account, avoids the charge.'] }; } },
  { id: 'si-solve', skill: 2, type: 'calculation', count: 7, gen(r) {
    const p = person(r), P = r.step(1500, 9000, 100), rate = r.pick([0.02, 0.025, 0.03, 0.035, 0.04]), t = r.pick([2, 3, 4, 5]), I = r2(P * rate * t);
    return { prompt: `${p.name} deposits ${$(P)} in a CD that pays simple interest. After ${t} years it has earned ${money(I)} in interest. What is the annual interest rate?`,
      ...numeric(rate * 100, { unit: '%', d: 1 }), solutionSteps: ['I = Prt, so r = I ÷ (P × t).', `r = ${money(I)} ÷ (${$(P)} × ${t}) = ${(rate).toFixed(3)}.`, `As a percent: ${pctText(rate)}.`] }; } },
  { id: 'apy-compare', skill: 3, type: 'comparison', count: 7, gen(r) {
    const p = person(r), dep = r.step(2000, 12000, 500), a = r.pick([0.042, 0.045, 0.048]), b = r2(a * 10000 - r.pick([5, 10, 15])) / 10000;
    const A = r2(dep * (1 + a / 12) ** 12 - dep), B = r2(dep * b);
    const better = A > B ? 'Account A' : 'Account B', diff = r2(Math.abs(A - B));
    return { prompt: `${p.name} will deposit ${$(dep)} for one year. Account A pays ${pctText(a)} APR compounded monthly. Account B pays ${pctText(b, 2)} APY. How much more interest does the better account earn in one year?`,
      ...numeric(diff), solutionSteps: [`A: ${$(dep)} × (1 + ${a}/12)¹² − ${$(dep)} = ${money(A)}.`, `B: ${$(dep)} × ${b} = ${money(B)} (APY already includes compounding).`, `${better} earns ${money(diff)} more. Compare savings accounts using APY.`] }; } },
  { id: 'reconcile', skill: 4, type: 'document', count: 7, game: true, gen(r) {
    const p = person(r), stmt = r.step(600, 2400, 0.01), dep = r.step(100, 500, 0.01), checks = [r.step(20, 180, 0.01), r.step(20, 180, 0.01)], adj = r2(stmt + dep - checks[0] - checks[1]);
    return { prompt: `${p.name}'s bank statement shows a balance of ${money(stmt)}. A ${money(dep)} deposit has not cleared yet, and two checks for ${money(checks[0])} and ${money(checks[1])} are outstanding. What is the adjusted (true) balance?`,
      ...numeric(adj), solutionSteps: ['Adjusted balance = statement balance + deposits in transit − outstanding checks.', `${money(stmt)} + ${money(dep)} − ${money(checks[0])} − ${money(checks[1])} = ${money(adj)}.`, 'This should match the balance in the check register.'] }; } }
];

/* ---------- Unit 4: Credit Cards & Debt ---------- */
const credit = [
  { id: 'carry-part', skill: 1, type: 'calculation', count: 7, gen(r) {
    const p = person(r), bal = r.step(500, 3200, 0.01), paid = r.step(100, Math.floor(bal * 0.8), 10), apr = r.pick([0.1999, 0.2249, 0.2499, 0.2799]), left = r2(bal - paid), it = r2(left * apr / 12);
    return { prompt: `${p.name}'s statement balance is ${money(bal)} at ${pctText(apr, 2)} APR. ${p.Sub} pays ${$(paid)} by the due date. Estimate next month's interest on the unpaid balance (APR ÷ 12).`,
      ...numeric(it), solutionSteps: [`Unpaid balance = ${money(bal)} − ${$(paid)} = ${money(left)}.`, `Monthly rate = ${pctText(apr, 2)} ÷ 12.`, `Interest ≈ ${money(left)} × ${(apr / 12).toFixed(5)} = ${money(it)}. Paying the full ${money(bal)} would make this $0.`] }; } },
  { id: 'util-target', skill: 4, type: 'calculation', count: 7, gen(r) {
    const p = person(r), lim = r.step(1500, 9000, 500), target = r.pick([0.1, 0.3]), cap = r2(lim * target);
    return { prompt: `${p.name} has a ${$0(lim)} credit limit and wants to keep utilization at or below ${pctText(target, 0)}. What is the largest balance ${p.sub} should carry when the statement closes?`,
      ...numeric(cap), solutionSteps: ['Utilization = balance ÷ limit.', `Balance ≤ ${pctText(target, 0)} × ${$0(lim)} = ${money(cap)}.`, 'Lower utilization generally helps a credit score.'] }; } },
  { id: 'late-cost', skill: 4, type: 'calculation', count: 6, gen(r) {
    const p = person(r), bal = r.step(1200, 4000, 0.01), apr = r.pick([0.2199, 0.2399]), pen = 0.2999, fee = r.pick([30, 35, 41]), extra = r2(bal * (pen - apr) / 12 + fee);
    return { prompt: `${p.name} misses a payment. The card charges a ${$(fee)} late fee and raises the APR from ${pctText(apr, 2)} to a ${pctText(pen, 2)} penalty APR. On a ${money(bal)} balance, how much more does the next month cost than if ${p.sub} had paid on time?`,
      ...numeric(extra), solutionSteps: [`Extra interest = ${money(bal)} × (${pctText(pen, 2)} − ${pctText(apr, 2)}) ÷ 12 = ${money(bal * (pen - apr) / 12)}.`, `Add the late fee: ${money(bal * (pen - apr) / 12)} + ${$(fee)} = ${money(extra)}.`, 'A penalty APR can last many months, so the real cost is usually higher.'] }; } },
  { id: 'transfer-fee', skill: 3, type: 'calculation', count: 7, gen(r) {
    const p = person(r), bal = r.step(1500, 7000, 50), feeP = r.pick([0.03, 0.04, 0.05]), apr = r.pick([0.2299, 0.2599]), fee = r2(bal * feeP), oneMonth = r2(bal * apr / 12);
    return { prompt: `${p.name} moves a ${$(bal)} balance from a ${pctText(apr, 2)} card to a 0% promotional card with a ${pctText(feeP, 0)} transfer fee. How much is the transfer fee?`,
      ...numeric(fee), solutionSteps: [`Fee = ${pctText(feeP, 0)} × ${$(bal)} = ${money(fee)}.`, `One month of interest on the old card ≈ ${$(bal)} × ${pctText(apr, 2)} ÷ 12 = ${money(oneMonth)}.`, `The fee equals about ${(fee / oneMonth).toFixed(1)} months of the old interest, so the transfer pays off if the promo lasts longer and the balance is paid down.`] }; } },
  { id: 'payment-split', skill: 2, type: 'calculation', count: 7, gen(r) {
    const p = person(r), bal = r.step(900, 5000, 0.01), apr = r.pick([0.1899, 0.2199, 0.2499]), pay = r.step(60, 250, 5), it = r2(bal * apr / 12), prin = r2(pay - it);
    if (prin <= 0) return null;
    return { prompt: `${p.name} owes ${money(bal)} at ${pctText(apr, 2)} APR and pays ${$(pay)} this month. If interest is ${money(it)}, how much of the payment reduces the balance?`,
      ...numeric(prin), solutionSteps: [`Interest = ${money(bal)} × ${pctText(apr, 2)} ÷ 12 = ${money(it)}.`, `Principal = ${$(pay)} − ${money(it)} = ${money(prin)}.`, `New balance = ${money(bal)} − ${money(prin)} = ${money(bal - prin)}.`] }; } }
];

/* ---------- Unit 5: Auto Loans & Borrowing ---------- */
const borrowing = [
  { id: 'total-interest', skill: 4, type: 'calculation', count: 8, gen(r) {
    const p = person(r), P = r.step(9000, 28000, 500), apr = r.pick([0.059, 0.069, 0.079, 0.089]), n = r.pick([36, 48, 60, 72]), pay = r2(M.loanPayment(P, apr, n)), I = r2(pay * n - P);
    return { prompt: `${p.name} borrows ${$0(P)} for a car at ${pctText(apr)} APR for ${n} months. The monthly payment is ${money(pay)}. How much interest will ${p.sub} pay over the loan?`,
      ...numeric(I, { tolerance: 0.05 }), solutionSteps: [`Total paid = ${money(pay)} × ${n} = ${money(pay * n)}.`, `Interest = total paid − amount borrowed = ${money(pay * n)} − ${$0(P)} = ${money(I)}.`, 'Longer terms lower the payment but raise total interest.'] }; } },
  { id: 'down-payment', skill: 1, type: 'calculation', count: 7, gen(r) {
    const p = person(r), price = r.step(14000, 36000, 250), dp = r.pick([0.1, 0.15, 0.2]), trade = r.pick([0, 0, 1500, 2500]), loan = r2(price * (1 - dp) - trade);
    return { prompt: `${p.name} buys a car for ${$0(price)}, puts ${pctText(dp, 0)} down${trade ? `, and gets ${$0(trade)} for a trade-in` : ''}. How much does ${p.sub} need to finance?`,
      ...numeric(loan), solutionSteps: [`Down payment = ${pctText(dp, 0)} × ${$0(price)} = ${money(price * dp)}.`, trade ? `Trade-in reduces the amount by ${$0(trade)}.` : 'No trade-in.', `Amount financed = ${money(loan)}.`] }; } },
  { id: 'first-interest', skill: 3, type: 'calculation', count: 7, gen(r) {
    const P = r.step(8000, 30000, 250), apr = r.pick([0.049, 0.064, 0.072, 0.085]), n = r.pick([48, 60]), pay = r2(M.loanPayment(P, apr, n)), it = r2(P * apr / 12), prin = r2(pay - it);
    return { prompt: `The first row of an amortization schedule for a ${$0(P)} loan at ${pctText(apr)} APR has a payment of ${money(pay)}. How much of that first payment goes to principal?`,
      ...numeric(prin), solutionSteps: [`Interest = ${$0(P)} × ${pctText(apr)} ÷ 12 = ${money(it)}.`, `Principal = ${money(pay)} − ${money(it)} = ${money(prin)}.`, `Balance after payment 1 = ${money(P - prin)}.`] }; } },
  { id: 'term-compare', skill: 2, type: 'comparison', count: 7, gen(r) {
    const p = person(r), P = r.step(12000, 26000, 500), apr = r.pick([0.065, 0.075, 0.085]), a = r2(M.loanPayment(P, apr, 48)), b = r2(M.loanPayment(P, apr, 72)), d = r2(b * 72 - a * 48);
    return { prompt: `${p.name} can finance ${$0(P)} at ${pctText(apr)} APR for 48 months (${money(a)}/month) or 72 months (${money(b)}/month). How much more does the 72-month loan cost in total?`,
      ...numeric(d, { tolerance: 0.05 }), solutionSteps: [`48 months: ${money(a)} × 48 = ${money(a * 48)}.`, `72 months: ${money(b)} × 72 = ${money(b * 72)}.`, `Difference = ${money(d)}. The lower payment costs more overall.`] }; } }
];

/* ---------- Unit 6: Investing ---------- */
const investing = [
  { id: 'rule-72', skill: 1, type: 'calculation', count: 7, gen(r) {
    const p = person(r), rate = r.pick([3, 4, 6, 8, 9, 12]), yrs = r2(72 / rate);
    return { prompt: `${p.name}'s investment grows about ${rate}% per year. Using the Rule of 72, about how many years will it take to double?`,
      ...numeric(yrs, { unit: 'count', display: String(yrs) + ' years', tolerance: 0 }), solutionSteps: ['Rule of 72: years to double ≈ 72 ÷ annual rate (as a whole number).', `72 ÷ ${rate} = ${yrs}.`, 'The rule is an estimate; it is most accurate for rates between about 6% and 10%.'] }; } },
  { id: 'div-yield', skill: 3, type: 'calculation', count: 7, gen(r) {
    const price = r.step(20, 180, 0.5), yld = r.pick([0.015, 0.02, 0.025, 0.03, 0.035, 0.04]), div = r2(price * yld / 4);
    const y = r2((div * 4 / price) * 100);
    return { prompt: `A stock trades at ${money(price)} and pays a quarterly dividend of ${money(div)}. What is its annual dividend yield, to the nearest tenth of a percent?`,
      ...numeric(y, { unit: '%', d: 1, tolerance: 0.05 }), solutionSteps: [`Annual dividend = ${money(div)} × 4 = ${money(div * 4)}.`, `Yield = ${money(div * 4)} ÷ ${money(price)} = ${(div * 4 / price).toFixed(4)}.`, `≈ ${y.toFixed(1)}%.`] }; } },
  { id: 'expense-ratio', skill: 3, type: 'comparison', count: 7, gen(r) {
    const p = person(r), bal = r.step(5000, 60000, 500), a = r.pick([0.0003, 0.0005, 0.001]), b = r.pick([0.0075, 0.01, 0.012]), d = r2(bal * (b - a));
    return { prompt: `${p.name} has ${$0(bal)} invested. Fund A charges an expense ratio of ${pctText(a, 2)}; Fund B charges ${pctText(b, 2)}. How much more does Fund B cost per year?`,
      ...numeric(d), solutionSteps: [`Fund A: ${pctText(a, 2)} × ${$0(bal)} = ${money(bal * a)}.`, `Fund B: ${pctText(b, 2)} × ${$0(bal)} = ${money(bal * b)}.`, `Difference = ${money(d)} per year, and the gap grows as the balance grows.`] }; } },
  { id: 'allocation-drop', skill: 4, type: 'calculation', count: 7, gen(r) {
    const p = person(r), tot = r.step(10000, 80000, 1000), st = r.pick([0.6, 0.7, 0.8, 0.9]), drop = r.pick([0.15, 0.2, 0.25, 0.3]), nv = r2(tot * st * (1 - drop) + tot * (1 - st));
    return { prompt: `${p.name} has ${$0(tot)} invested: ${pctText(st, 0)} in stocks and the rest in bonds. If stocks fall ${pctText(drop, 0)} and bonds stay flat, what is the new portfolio value?`,
      ...numeric(nv), solutionSteps: [`Stocks: ${$0(tot * st)} × (1 − ${pctText(drop, 0)}) = ${money(tot * st * (1 - drop))}.`, `Bonds: ${$0(tot * (1 - st))}.`, `New value = ${money(nv)}, a ${pctText((tot - nv) / tot)} drop overall. Diversification softened the fall.`] }; } },
  { id: 'contributed-vs-growth', skill: 2, type: 'calculation', count: 6, gen(r) {
    const p = person(r), m = r.pick([100, 150, 200, 250]), y = r.pick([10, 20, 30]), rate = r.pick([0.06, 0.07]), fv = r2(M.futureValue(0, m, rate, 12, y)), paid = m * 12 * y, g = r2(fv - paid);
    return { prompt: `${p.name} invests ${$(m)} per month for ${y} years at ${pctText(rate, 0)} compounded monthly and ends with ${money(fv)}. How much of that is growth (not ${p.pos} own deposits)?`,
      ...numeric(g, { tolerance: 0.05 }), solutionSteps: [`Total deposited = ${$(m)} × 12 × ${y} = ${$0(paid)}.`, `Growth = ${money(fv)} − ${$0(paid)} = ${money(g)}.`, 'The longer the time, the larger the share that is growth.'] }; } }
];

/* ---------- Unit 7: Housing ---------- */
const housing = [
  { id: 'rule-28', skill: 2, type: 'calculation', count: 7, gen(r) {
    const p = person(r), inc = r.step(42000, 120000, 1000), cap = r2(inc / 12 * 0.28);
    return { prompt: `Lenders often suggest housing costs of no more than 28% of gross monthly income. ${p.name} earns ${$0(inc)} per year. What is the maximum monthly housing payment under this guideline?`,
      ...numeric(cap), solutionSteps: [`Gross monthly income = ${$0(inc)} ÷ 12 = ${money(inc / 12)}.`, `28% × ${money(inc / 12)} = ${money(cap)}.`, 'The payment includes principal, interest, property tax and insurance.'] }; } },
  { id: 'cash-to-close', skill: 2, type: 'calculation', count: 7, gen(r) {
    const p = person(r), price = r.step(180000, 420000, 5000), dp = r.pick([0.035, 0.05, 0.1, 0.2]), cc = r.pick([0.02, 0.03, 0.04]), cash = r2(price * (dp + cc));
    return { prompt: `${p.name} buys a ${$0(price)} home with ${pctText(dp)} down. Closing costs are ${pctText(cc, 0)} of the price. How much cash does ${p.sub} need at closing?`,
      ...numeric(cash), solutionSteps: [`Down payment = ${pctText(dp)} × ${$0(price)} = ${money(price * dp)}.`, `Closing costs = ${pctText(cc, 0)} × ${$0(price)} = ${money(price * cc)}.`, `Cash needed = ${money(cash)}.`] }; } },
  { id: 'escrow-tax', skill: 3, type: 'calculation', count: 7, gen(r) {
    const val = r.step(160000, 480000, 5000), rate = r.pick([0.009, 0.011, 0.014, 0.018, 0.021]), ins = r.step(900, 2400, 50), mo = r2((val * rate + ins) / 12);
    return { prompt: `A home is assessed at ${$0(val)} with a property tax rate of ${pctText(rate)}. Homeowners insurance is ${$0(ins)} per year. How much is added to the monthly mortgage payment for escrow?`,
      ...numeric(mo), solutionSteps: [`Property tax = ${pctText(rate)} × ${$0(val)} = ${money(val * rate)} per year.`, `Tax + insurance = ${money(val * rate + ins)} per year.`, `÷ 12 = ${money(mo)} per month.`] }; } },
  { id: 'opportunity', skill: 4, type: 'calculation', count: 7, gen(r) {
    const p = person(r), dp = r.step(20000, 90000, 1000), rate = r.pick([0.04, 0.05, 0.06]), y = r.pick([5, 10]), lost = r2(dp * (1 + rate) ** y - dp);
    return { prompt: `Instead of investing it, ${p.name} uses ${$0(dp)} as a down payment. If that money could have earned ${pctText(rate, 0)} per year compounded annually, what growth does ${p.sub} give up over ${y} years?`,
      ...numeric(lost), solutionSteps: [`Invested value = ${$0(dp)} × (1 + ${rate})^${y} = ${money(dp * (1 + rate) ** y)}.`, `Opportunity cost = ${money(dp * (1 + rate) ** y)} − ${$0(dp)} = ${money(lost)}.`, 'Home equity can also grow, so compare both sides before deciding.'] }; } }
];

/* ---------- Unit 8: Insurance & Risk ---------- */
const insurance = [
  { id: 'claim-net', skill: 1, type: 'calculation', count: 7, gen(r) {
    const p = person(r), damage = r.step(800, 9000, 25), ded = r.pick([250, 500, 1000, 2000]), pay = Math.max(0, damage - ded);
    return { prompt: `${p.name}'s car has ${$(damage)} of covered damage. The collision deductible is ${$0(ded)}. How much does the insurance company pay?`,
      ...numeric(pay), solutionSteps: ['The policyholder pays the deductible first; insurance pays the rest of a covered loss.', `${$(damage)} − ${$0(ded)} = ${money(pay)}.`, pay === 0 ? 'The damage is below the deductible, so filing a claim pays nothing.' : `${p.name} pays ${$0(ded)}.`] }; } },
  { id: 'coinsurance', skill: 2, type: 'calculation', count: 8, gen(r) {
    const p = person(r), bill = r.step(2000, 30000, 100), ded = r.pick([1000, 1500, 2500]), co = r.pick([0.1, 0.2, 0.3]), max = r.pick([5000, 6500, 8000]);
    const owe = Math.min(max, Math.min(bill, ded) + Math.max(0, bill - ded) * co);
    return { prompt: `${p.name}'s health plan has a ${$0(ded)} deductible, ${pctText(co, 0)} coinsurance and a ${$0(max)} out-of-pocket maximum. A hospital bill is ${$0(bill)}. How much does ${p.name} pay?`,
      ...numeric(owe), solutionSteps: [`Deductible: ${p.name} pays the first ${$0(Math.min(bill, ded))}.`, `Coinsurance: ${pctText(co, 0)} × (${$0(bill)} − ${$0(ded)}) = ${money(Math.max(0, bill - ded) * co)}.`, `Total ${money(Math.min(bill, ded) + Math.max(0, bill - ded) * co)}${Math.min(bill, ded) + Math.max(0, bill - ded) * co > max ? `, capped at the ${$0(max)} maximum` : ''}: ${money(owe)}.`] }; } },
  { id: 'warranty-ev', skill: 3, type: 'calculation', count: 7, gen(r) {
    const item = r.pick(['laptop', 'phone', 'washing machine', 'TV']), cost = r.step(60, 220, 5), prob = r.pick([0.05, 0.08, 0.1, 0.12, 0.15]), repair = r.step(200, 700, 10), ev = r2(prob * repair - cost);
    return { prompt: `A ${$(cost)} extended warranty on a ${item} covers one repair. The chance of needing a ${$(repair)} repair during the warranty is ${pctText(prob, 0)}. What is the buyer's expected value of the warranty?`,
      ...numeric(ev), solutionSteps: [`Expected payout = ${pctText(prob, 0)} × ${$(repair)} = ${money(prob * repair)}.`, `Expected value = ${money(prob * repair)} − ${$(cost)} = ${money(ev)}.`, ev < 0 ? 'Negative: on average the buyer loses money, which is how the seller profits.' : 'Positive: this warranty is priced in the buyer’s favor.'] }; } },
  { id: 'annual-premium', skill: 1, type: 'comparison', count: 7, gen(r) {
    const p = person(r), a = r.step(95, 180, 1), b = r.step(150, 260, 1), da = r.pick([1000, 2000]), db = r.pick([250, 500]), claim = r.step(1500, 4000, 100);
    const A = a * 12 + Math.min(da, claim), B = b * 12 + Math.min(db, claim), better = A < B ? 'Plan A' : 'Plan B', diff = r2(Math.abs(A - B));
    if (A === B) return null;
    return { prompt: `Plan A costs ${$(a)}/month with a ${$0(da)} deductible. Plan B costs ${$(b)}/month with a ${$0(db)} deductible. If ${p.name} has one ${$0(claim)} claim this year, how much less does the cheaper plan cost in total?`,
      ...numeric(diff), solutionSteps: [`Plan A: ${$(a)} × 12 + ${$0(Math.min(da, claim))} = ${money(A)}.`, `Plan B: ${$(b)} × 12 + ${$0(Math.min(db, claim))} = ${money(B)}.`, `${better} costs ${money(diff)} less with one claim; with no claims, the lower premium wins.`] }; } }
];

/* ---------- Unit 9: College & Careers ---------- */
const college = [
  { id: 'net-price-calc', skill: 1, type: 'calculation', count: 7, gen(r) {
    const p = person(r), coa = r.step(18000, 62000, 500), grant = r.step(2000, 12000, 250), sch = r.step(0, 9000, 250), net = coa - grant - sch;
    return { prompt: `A college's cost of attendance is ${$0(coa)} per year. ${p.name} receives ${$0(grant)} in grants and ${$0(sch)} in scholarships. What is ${p.pos} net price per year?`,
      ...numeric(net), solutionSteps: ['Net price = cost of attendance − grants − scholarships (gift aid you do not repay).', `${$0(coa)} − ${$0(grant)} − ${$0(sch)} = ${money(net)}.`, 'Loans are not subtracted; they reduce what you pay now but must be repaid.'] }; } },
  { id: 'unsub-accrue', skill: 2, type: 'calculation', count: 7, gen(r) {
    const p = person(r), P = r.step(3500, 7500, 500), rate = r.pick([0.0553, 0.0653, 0.0705]), yrs = r.pick([3, 4, 4.5]), I = r2(P * rate * yrs);
    return { prompt: `${p.name} borrows a ${$0(P)} unsubsidized student loan at ${pctText(rate, 2)} simple interest, which builds while ${p.sub} is in school for ${yrs} years. How much interest accrues before repayment starts?`,
      ...numeric(I), solutionSteps: ['I = Prt.', `${$0(P)} × ${rate} × ${yrs} = ${money(I)}.`, 'If unpaid, this interest can be added to the balance (capitalized) when repayment begins.'] }; } },
  { id: 'career-gap', skill: 3, type: 'comparison', count: 7, gen(r) {
    const a = r.step(36000, 48000, 500), b = r.step(52000, 78000, 500), yrs = r.pick([5, 10, 15]), d = (b - a) * yrs;
    return { prompt: `Career A pays ${$0(a)} per year and Career B pays ${$0(b)} per year. Ignoring raises, how much more does Career B earn over ${yrs} years?`,
      ...numeric(d), solutionSteps: [`Yearly difference = ${$0(b)} − ${$0(a)} = ${$0(b - a)}.`, `× ${yrs} years = ${money(d)}.`, 'Also weigh training cost and time out of the workforce.'] }; } },
  { id: 'payback-simple', skill: 4, type: 'calculation', count: 7, gen(r) {
    const cost = r.step(12000, 60000, 1000), gain = r.step(4000, 15000, 500), yrs = cost / gain;
    return { prompt: `A certificate program costs ${$0(cost)} and is expected to raise yearly earnings by ${$0(gain)}. To the nearest tenth of a year, how long until the extra earnings cover the cost?`,
      ...numeric(Math.round(yrs * 10) / 10, { unit: 'count', display: (Math.round(yrs * 10) / 10) + ' years', tolerance: 0.05 }), solutionSteps: ['Payback period = cost ÷ yearly gain.', `${$0(cost)} ÷ ${$0(gain)} = ${yrs.toFixed(2)}.`, `≈ ${(Math.round(yrs * 10) / 10)} years.`] }; } }
];

/* ---------- Unit 10: Retirement & Inflation ---------- */
const retirement = [
  { id: 'match-calc', skill: 3, type: 'calculation', count: 7, gen(r) {
    const p = person(r), sal = r.step(38000, 95000, 1000), c = r.pick([0.02, 0.04, 0.06, 0.08]), mr = r.pick([0.5, 1]), lim = 0.06, m = r2(sal * Math.min(c, lim) * mr);
    return { prompt: `${p.name} earns ${$0(sal)} and contributes ${pctText(c, 0)} to a 401(k). The employer matches ${mr === 1 ? '100%' : '50%'} of contributions up to 6% of salary. How much does the employer add per year?`,
      ...numeric(m), solutionSteps: [`Matched contribution rate = the smaller of ${pctText(c, 0)} and 6% = ${pctText(Math.min(c, lim), 0)}.`, `Match = ${mr === 1 ? '100%' : '50%'} × ${pctText(Math.min(c, lim), 0)} × ${$0(sal)} = ${money(m)}.`, c < lim ? `Raising contributions to 6% would earn the full match.` : 'This captures the full match.'] }; } },
  { id: 'nest-egg-4', skill: 2, type: 'calculation', count: 7, gen(r) {
    const p = person(r), spend = r.step(30000, 80000, 1000), ss = r.step(12000, 26000, 500), gap = Math.max(0, spend - ss), egg = r2(gap / 0.04);
    return { prompt: `${p.name} expects to spend ${$0(spend)} per year in retirement and receive ${$0(ss)} per year from Social Security. Using the 4% rule, how much should ${p.sub} have saved?`,
      ...numeric(egg), solutionSteps: [`Needed from savings = ${$0(spend)} − ${$0(ss)} = ${$0(gap)} per year.`, `4% rule: savings ≈ ${$0(gap)} ÷ 0.04 = ${money(egg)}.`, 'The 4% rule is a rough guide, not a guarantee.'] }; } },
  { id: 'future-price', skill: 1, type: 'calculation', count: 7, gen(r) {
    const [item, price] = r.pick([['a month of groceries', 420], ['a used car', 9500], ['a year of rent', 18000], ['a movie ticket', 13.5], ['a tank of gas', 52], ['a year of college tuition', 11200]]), i = r.pick([0.025, 0.03, 0.035]), y = r.pick([10, 20, 30]), fp = r2(price * (1 + i) ** y);
    return { prompt: `${item[0].toUpperCase() + item.slice(1)} costs ${$(price)} today. If inflation averages ${pctText(i)} per year, what will it cost in ${y} years?`,
      ...numeric(fp), solutionSteps: [`Future price = ${$(price)} × (1 + ${i})^${y}.`, `= ${$(price)} × ${((1 + i) ** y).toFixed(4)} = ${money(fp)}.`, 'Prices roughly double every 72 ÷ (rate) years.'] }; } },
  { id: 'real-return', skill: 4, type: 'calculation', count: 7, gen(r) {
    const n = r.pick([0.04, 0.05, 0.06, 0.07, 0.08]), i = r.pick([0.02, 0.025, 0.03, 0.035]), real = r2(((1 + n) / (1 + i) - 1) * 100);
    return { prompt: `An investment earns ${pctText(n, 0)} per year while inflation is ${pctText(i)}. What is the real (inflation-adjusted) return, to the nearest hundredth of a percent?`,
      ...numeric(real, { unit: '%', d: 2, tolerance: 0.01 }), solutionSteps: ['Real return = (1 + nominal) ÷ (1 + inflation) − 1.', `(1 + ${n}) ÷ (1 + ${i}) − 1 = ${((1 + n) / (1 + i) - 1).toFixed(5)}.`, `≈ ${real.toFixed(2)}%. The shortcut ${pctText(n, 0)} − ${pctText(i)} = ${pctText(n - i)} is close but slightly high.`] }; } }
];

// Family ids carry an "ap-" prefix so they never collide with a unit's original families.
const tag = (fams) => fams.map(f => ({ ...f, id: 'ap-' + f.id }));
export const applied = Object.fromEntries(Object.entries({ income, budgeting, banking, credit, borrowing, investing, housing, insurance, college, retirement }).map(([k, v]) => [k, tag(v)]));
