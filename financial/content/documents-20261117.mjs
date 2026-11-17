/* Real-world documents (2026-11-17): W-2, simple 1040, utility bill, credit report, Truth-in-Lending disclosure,
 * auto insurance declarations, lease summary, explanation of benefits, fund fact sheet and retirement benefits
 * summary. Every one is fictional and labeled so. Each family cycles through three questions, one per level:
 *   Support: read a value, or one step with the document.  Standard: a check or calculation from two or more lines.
 *   Advanced: several steps, or combining the document with a situation.
 * verify(q) reads the numbers back out of the rendered document and the question text (not the generator's
 * variables) and recomputes the answer; tests/fa-documents.test.mjs runs it on every question. */
import { M, money, $, $0, pct, person, mc, numeric, table } from './kit.mjs';
import { TAX_2026 } from './real-data-2026.mjs';

const r2 = M.round2;
const LV = ['support', 'standard', 'advanced'];
const num = (s) => Number(String(s).replace(/[−]/g, '-').replace(/[$,%\s]/g, '').replace(/[^\d.\-].*$/, ''));
/* Find a value in a document by label: form boxes, then meta, then the last column of a table row. */
export function docValue(q, label) {
  const d = q.scenario && q.scenario.document, re = label instanceof RegExp ? label : new RegExp(label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
  for (const b of (d.boxes || [])) if (re.test(b[0])) return num(b[1]);
  for (const m of (d.meta || [])) if (re.test(m[0])) return num(m[1]);
  for (const row of ((d.table && d.table.rows) || [])) if (re.test(row[0])) return num(row[row.length - 1]);
  throw Error('no ' + label + ' in ' + q.id);
}
const rows = (q) => q.scenario.document.table.rows;
function tax2026(taxable) { let t = 0, lo = 0; for (const b of TAX_2026.bracketsSingle) { if (taxable <= lo) break; t += (Math.min(taxable, b.upTo) - lo) * b.rate; lo = b.upTo; } return t; }
const EMPLOYERS = ['Brookside Medical Group', 'Pine Ridge Builders', 'Harbor City Logistics', 'Lakeview Credit Union', 'Maple Falls School District', 'Westfield Design Co.'];
const NOTE = 'Fictional document for classroom use.';
const D = (skill, count, id, gen, verify) => ({ id: 'lv-d-' + id, skill, type: 'document', count, game: false, gen, verify });

/* ---------- Income: W-2 and a simple 1040 (2026 figures) ---------- */
function w2(r, p) {
  const gross = r.step(32000, 88000, 50), k = r.pick([0, 0, 0.04, 0.06]), wages = r2(gross * (1 - k)), fedTax = r2(tax2026(Math.max(0, wages - TAX_2026.standardDeduction.single)));
  const withheld = r2(fedTax + r.step(-400, 1200, 10)), ss = r2(gross * 0.062), med = r2(gross * 0.0145);
  return { gross, k, wages, fedTax, withheld, ss, med, doc: { kind: 'w2', title: 'Form W-2 Wage and Tax Statement 2026', meta: [['Employee', p.name], ['Employer', r.pick(EMPLOYERS)]],
    boxes: [['1 Wages, tips, other compensation', money(wages)], ['2 Federal income tax withheld', money(withheld)], ['3 Social security wages', money(gross)], ['4 Social security tax withheld', money(ss)], ['5 Medicare wages and tips', money(gross)], ['6 Medicare tax withheld', money(med)], ...(k ? [['12a Code D (401(k) deferrals)', money(gross - wages)]] : [])],
    notes: [NOTE, 'Box 1 leaves out pre-tax 401(k) deferrals; boxes 3 and 5 include them.'] } };
}
const income = [
  D(4, 9, 'w2', (r, k) => { const p = person(r), w = w2(r, p), level = LV[k % 3];
    if (level === 'support') return { level, prompt: `Use ${p.name}'s W-2. How much federal income tax was withheld during the year?`, scenario: { document: w.doc }, ...numeric(w.withheld), solutionSteps: ['Federal income tax withheld is in box 2.', `Box 2 = ${money(w.withheld)}.`] };
    if (level === 'standard') return { level, prompt: `Social Security tax is 6.2% of box 3. Check ${p.name}'s W-2: what should box 4 be?`, scenario: { document: w.doc }, ...numeric(r2(w.gross * 0.062)), solutionSteps: [`Box 3 = ${money(w.gross)}.`, `6.2% × ${money(w.gross)} = ${money(w.gross * 0.062)}.`, 'It matches box 4, so the withholding is right.'] };
    const due = r2(w.withheld - w.fedTax);
    return { level, prompt: `Using ${p.name}'s W-2 and the 2026 figures for a single filer (standard deduction $16,100; 10% to $12,400, 12% to $50,400, 22% to $105,700), what refund will ${p.sub} get? If ${p.sub} owes money, give a negative number.`, scenario: { document: w.doc },
      ...numeric(due), solutionSteps: [`Taxable income = box 1 − $16,100 = ${money(w.wages)} − $16,100 = ${money(Math.max(0, w.wages - 16100))}.`, `Tax = ${money(w.fedTax)}.`, `Refund = withheld − tax = ${money(w.withheld)} − ${money(w.fedTax)} = ${money(due)}${due < 0 ? ' (owes)' : ''}.`] }; },
    (q) => { if (q.level === 'support') return docValue(q, /^2 /); if (q.level === 'standard') return r2(docValue(q, /^3 /) * 0.062); const wages = docValue(q, /^1 /); return docValue(q, /^2 /) - r2(tax2026(Math.max(0, wages - 16100))); }),
  D(4, 9, 'form-1040', (r, k) => { const p = person(r), level = LV[k % 3], wages = level === 'standard' ? r.step(20000, 62000, 50) : r.step(28000, 96000, 50), taxable = Math.max(0, wages - 16100), t = r2(tax2026(taxable)), withheld = r2(t + r.step(-500, 1500, 10));
    const L = (n, label, v) => [n + ' ' + label, v];
    const boxes = [L('1a', 'Wages (W-2 box 1)', money(wages)), L('12', 'Standard deduction', '$16,100.00'), L('15', 'Taxable income', level === 'support' ? '?' : money(taxable)), L('16', 'Tax', level === 'support' ? '—' : level === 'standard' ? '?' : money(t)), L('25a', 'Federal income tax withheld', money(withheld)), L('34', 'Refund (or 37 Amount you owe)', '?')];
    const doc = { kind: 'form-1040', title: 'Form 1040 (simplified) · 2026 · Single', meta: [['Name', p.name]], boxes, notes: [NOTE, '2026 single brackets: 10% to $12,400; 12% to $50,400; 22% to $105,700.'] };
    if (level === 'support') return { level, prompt: `Fill in line 15 of ${p.name}'s simplified 1040. Taxable income = line 1a − line 12.`, scenario: { document: doc }, ...numeric(taxable), solutionSteps: [`${money(wages)} − $16,100.00 = ${money(taxable)}.`] };
    if (level === 'standard') return { level, prompt: `Fill in line 16 (tax) of ${p.name}'s simplified 1040 using the 2026 brackets in the note.`, scenario: { document: doc }, ...numeric(t), solutionSteps: [`10% of the first $12,400 = $1,240.00.`, taxable > 12400 ? `12% of ${money(Math.min(taxable, 50400) - 12400)} = ${money((Math.min(taxable, 50400) - 12400) * 0.12)}.` : 'All taxable income is in the 10% bracket.', `Tax = ${money(t)}.`] };
    return { level, prompt: `Complete ${p.name}'s simplified 1040: find line 34, the refund (withholding minus tax). If ${p.sub} owes, give a negative number.`, scenario: { document: doc }, ...numeric(r2(withheld - t)), solutionSteps: [`Line 15 = ${money(taxable)}; line 16 = ${money(t)}.`, `Refund = ${money(withheld)} − ${money(t)} = ${money(withheld - t)}.`] }; },
    (q) => { const wages = docValue(q, /^1a /), taxable = Math.max(0, wages - 16100); if (q.level === 'support') return taxable; if (q.level === 'standard') return r2(tax2026(taxable)); return docValue(q, /^25a /) - r2(tax2026(taxable)); })
];

/* ---------- Budgeting: a utility bill ---------- */
const budgeting = [
  D(2, 9, 'utility-bill', (r, k) => { const p = person(r), level = LV[k % 3], prev = r.step(20000, 60000, 1), use = r.step(380, 1400, 1), rate = r.pick([0.13, 0.15, 0.16, 0.18]), fixed = r.pick([10, 12, 15]), tax = 0.05;
    const energy = r2(use * rate), sub = r2(energy + fixed), total = r2(sub * (1 + tax));
    const doc = { kind: 'utility-bill', title: 'Riverton Power & Light — Electric Bill', meta: [['Account holder', p.name], ['Service period', 'Oct 3 – Nov 2'], ['Previous meter reading', prev.toLocaleString('en-US') + ' kWh'], ['Current meter reading', (prev + use).toLocaleString('en-US') + ' kWh']],
      table: table(['Charge', 'Amount'], [['Customer charge (fixed)', money(fixed)], ['Energy rate', '$' + rate.toFixed(2) + ' per kWh'], ['Sales tax', '5% of charges']]), notes: [NOTE] };
    if (level === 'support') return { level, prompt: `How many kilowatt-hours (kWh) did ${p.name} use this month? Usage = current reading − previous reading.`, scenario: { document: doc }, ...numeric(use, { unit: 'count', display: use + ' kWh' }), solutionSteps: [`${(prev + use).toLocaleString('en-US')} − ${prev.toLocaleString('en-US')} = ${use} kWh.`] };
    if (level === 'standard') return { level, prompt: `What are ${p.name}'s charges before tax? (Usage × rate + customer charge)`, scenario: { document: doc }, ...numeric(sub), solutionSteps: [`Usage = ${use} kWh.`, `${use} × $${rate.toFixed(2)} = ${money(energy)}.`, `+ ${money(fixed)} = ${money(sub)}.`] };
    const avg = r.step(70, 150, 5);
    return { level, prompt: `${p.name} budgets $${avg} a month for electricity. What is the total due with tax, and how far over (positive) or under (negative) budget is it? Give the amount over budget.`, scenario: { document: doc }, ...numeric(r2(total - avg)), solutionSteps: [`Charges = ${use} × $${rate.toFixed(2)} + ${money(fixed)} = ${money(sub)}.`, `With 5% tax: ${money(sub)} × 1.05 = ${money(total)}.`, `${money(total)} − $${avg} = ${money(total - avg)}.`] }; },
    (q) => { const use = docValue(q, /Current meter/) - docValue(q, /Previous meter/); if (q.level === 'support') return use; const rate = docValue(q, /Energy rate/), sub = r2(r2(use * rate) + docValue(q, /Customer charge/)); if (q.level === 'standard') return sub; return r2(sub * 1.05) - Number(q.prompt.match(/budgets \$([\d.]+)/)[1]); })
];

/* ---------- Credit: a credit report excerpt ---------- */
const CREDITORS = ['Northstar Visa', 'Bayline Mastercard', 'Summit Store Card', 'Crestview Auto Loan', 'Lakeview Student Loan'];
const credit = [
  D(5, 9, 'credit-report', (r, k) => { const p = person(r), level = LV[k % 3];
    const cards = [0, 1, 2].map(i => ({ name: CREDITORS[i], limit: r.step(500, 5000, 250), late: r.pick([0, 0, 0, 1, 2]) })); cards.forEach(c => { c.bal = r.step(0, Math.floor(c.limit * 0.8), 10); });
    const loan = { name: CREDITORS[3], bal: r.step(4000, 15000, 50), late: r.pick([0, 0, 1]) };
    const doc = { kind: 'credit-report', title: 'Credit Report Excerpt — Fictional Bureau', meta: [['Consumer', p.name], ['Report date', 'Nov 1, 2026']],
      table: table(['Account', 'Type', 'Limit', 'Balance', '30-day lates (24 mo)'], [...cards.map(c => [c.name, 'Revolving', $0(c.limit), $0(c.bal), String(c.late)]), [loan.name, 'Installment', '—', $0(loan.bal), String(loan.late)]]), notes: [NOTE, 'Utilization counts revolving accounts only.'] };
    if (level === 'support') { const n = [...cards, loan].reduce((a, c) => a + c.late, 0); return { level, prompt: `How many 30-day late payments in all does ${p.name}'s report show?`, scenario: { document: doc }, ...numeric(n, { unit: 'count', display: String(n) }), solutionSteps: [`Add the last column: ${[...cards, loan].map(c => c.late).join(' + ')} = ${n}.`, 'Payment history is the largest factor in most scores.'] }; }
    const L = cards.reduce((a, c) => a + c.limit, 0), B = cards.reduce((a, c) => a + c.bal, 0);
    if (level === 'standard') return { level, prompt: `What is ${p.name}'s overall credit utilization on revolving accounts, to the nearest tenth of a percent?`, scenario: { document: doc }, ...numeric(r2(B / L * 100), { unit: '%', d: 1, tolerance: 0.05 }), solutionSteps: [`Revolving balances = ${$0(B)}; limits = ${$0(L)}.`, `${$0(B)} ÷ ${$0(L)} = ${(B / L).toFixed(4)} ≈ ${(B / L * 100).toFixed(1)}%.`, 'The installment loan is not part of utilization.'] };
    const pay = Math.max(0, r2(B - 0.1 * L));
    return { level, prompt: `${p.name} wants overall revolving utilization at 10% before applying for a mortgage. What is the least total amount ${p.sub} must pay down on the cards?`, scenario: { document: doc }, ...numeric(pay), solutionSteps: [`10% of total limits = 0.10 × ${$0(L)} = ${money(0.1 * L)}.`, `Pay down = ${$0(B)} − ${money(0.1 * L)} = ${money(pay)}.`, 'Paying before the statement closes lowers the balance that gets reported.'] }; },
    (q) => { const rs = rows(q), rev = rs.filter(x => x[1] === 'Revolving'); if (q.level === 'support') return rs.reduce((a, x) => a + num(x[4]), 0); const L = rev.reduce((a, x) => a + num(x[2]), 0), B = rev.reduce((a, x) => a + num(x[3]), 0); if (q.level === 'standard') return B / L * 100; return Math.max(0, B - 0.1 * L); })
];

/* ---------- Borrowing: Truth-in-Lending disclosure ---------- */
const pmt = (P, apr, n) => { const i = apr / 12; return P * i / (1 - (1 + i) ** -n); };
const borrowing = [
  D(4, 9, 'tila', (r, k) => { const p = person(r), level = LV[k % 3], P = r.step(9000, 28000, 50), apr = r.pick([0.0549, 0.0649, 0.0749, 0.0849]), n = r.pick([48, 60, 72]), pay = r2(pmt(P, apr, n)), tot = r2(pay * n), fc = r2(tot - P), down = r.step(1000, 5000, 500);
    const boxes = [['ANNUAL PERCENTAGE RATE', pct(apr, 2)], ['FINANCE CHARGE', level === 'standard' ? '?' : money(fc)], ['Amount Financed', money(P)], ['Total of Payments', level === 'support' ? '?' : money(tot)], ['Your payment schedule', level === 'advanced' ? `${n} monthly payments of ?` : `${n} monthly payments of ${money(pay)}`, true]];
    const doc = { kind: 'loan-disclosure', title: 'Truth-in-Lending Disclosure — Riverton Auto Credit', meta: [['Borrower', p.name], ['Cash down payment', $0(down)]], boxes, notes: [NOTE] };
    if (level === 'support') return { level, prompt: `Fill in the Total of Payments box on ${p.name}'s disclosure. Total of payments = monthly payment × number of payments.`, scenario: { document: doc }, ...numeric(tot), solutionSteps: [`${money(pay)} × ${n} = ${money(tot)}.`] };
    if (level === 'standard') return { level, prompt: `Fill in the FINANCE CHARGE box: total of payments − amount financed.`, scenario: { document: doc }, ...numeric(fc), solutionSteps: [`${money(tot)} − ${money(P)} = ${money(fc)}.`, 'The finance charge is the dollar cost of the credit.'] };
    return { level, prompt: `The payment amount is missing. Using the APR, amount financed and number of payments, find the monthly payment, then the total sale price (cash down + total of payments). Give the total sale price. (Payment = P·i ÷ (1 − (1 + i)^−n), i = APR ÷ 12.)`, scenario: { document: doc }, ...numeric(r2(down + tot), { tolerance: 0.1 }), solutionSteps: [`i = ${apr} ÷ 12; payment = ${money(pay)}.`, `Total of payments = ${money(pay)} × ${n} = ${money(tot)}.`, `Total sale price = ${$0(down)} + ${money(tot)} = ${money(down + tot)}.`] }; },
    (q) => { const d = q.scenario.document, sched = d.boxes.find(b => /schedule/i.test(b[0]))[1], n = num(sched.match(/^(\d+)/)[1]); if (q.level === 'support') return r2(num(sched.split(' of ')[1]) * n); if (q.level === 'standard') return docValue(q, /Total of Payments/) - docValue(q, /Amount Financed/); const P = docValue(q, /Amount Financed/), apr = docValue(q, /ANNUAL/) / 100; return docValue(q, /Cash down/) + r2(r2(pmt(P, apr, n)) * n); })
];

/* ---------- Insurance: auto declarations page and an explanation of benefits ---------- */
const insurance = [
  D(1, 9, 'auto-declarations', (r, k) => { const p = person(r), level = LV[k % 3], liab = r.step(180, 420, 1), coll = r.step(120, 320, 1), comp = r.step(40, 120, 1), um = r.step(20, 60, 1), dColl = r.pick([500, 1000]), prop = r.pick([25000, 50000]), six = liab + coll + comp + um;
    const doc = { kind: 'auto-declarations', title: 'Auto Policy Declarations — 6-month term', meta: [['Named insured', p.name], ['Vehicle', '2019 sedan']],
      table: table(['Coverage', 'Limits / deductible', '6-month premium'], [['Liability (bodily injury / property damage)', `$50,000 / $100,000 / $${prop.toLocaleString('en-US')}`, money(liab)], ['Collision', `$${dColl.toLocaleString('en-US')} deductible`, money(coll)], ['Comprehensive', '$250 deductible', money(comp)], ['Uninsured motorist', '$50,000 / $100,000', money(um)]]), notes: [NOTE, 'Liability limits: per person / per accident / property damage.'] };
    if (level === 'support') return { level, prompt: `What is ${p.name}'s total premium for the 6-month term? Add the premium column.`, scenario: { document: doc }, ...numeric(six), solutionSteps: [`${money(liab)} + ${money(coll)} + ${money(comp)} + ${money(um)} = ${money(six)}.`] };
    if (level === 'standard') return { level, prompt: `What does ${p.name}'s car insurance cost per month, to the cent?`, scenario: { document: doc }, ...numeric(r2(six / 6)), solutionSteps: [`6-month total = ${money(six)}.`, `÷ 6 = ${money(six / 6)} per month.`] };
    const own = r.step(2500, 9000, 50), other = r.step(prop - 8000, prop + 15000, 500), oop = dColl + Math.max(0, other - prop);
    return { level, prompt: `${p.name} causes a crash: $${own.toLocaleString('en-US')} of damage to ${p.pos} own car and $${other.toLocaleString('en-US')} to the other driver's car. Using the declarations page, how much does ${p.name} pay out of pocket?`, scenario: { document: doc }, ...numeric(oop), solutionSteps: [`Own car: collision pays after the $${dColl.toLocaleString('en-US')} deductible.`, `Other car: property-damage limit $${prop.toLocaleString('en-US')}${other > prop ? `, so ${p.name} owes the extra $${(other - prop).toLocaleString('en-US')}` : ' covers it'}.`, `Out of pocket = ${money(oop)}.`] }; },
    (q) => { const rs = rows(q), sum = rs.reduce((a, x) => a + num(x[2]), 0); if (q.level === 'support') return sum; if (q.level === 'standard') return r2(sum / 6); const ded = num(rs[1][1]), prop = num(rs[0][1].split('/')[2]), [own, other] = [...q.prompt.matchAll(/\$([\d,]+)/g)].map(m => num(m[1])); return ded + Math.max(0, other - prop); }),
  D(2, 9, 'eob', (r, k) => { const p = person(r), level = LV[k % 3], billed = r.step(600, 4800, 10), allowed = r2(billed * r.pick([0.55, 0.6, 0.65, 0.7])), dedLeft = level === 'advanced' ? r.step(200, Math.floor(allowed * 0.6), 10) : 0, co = 0.2;
    const youOwe = r2(dedLeft + (allowed - dedLeft) * co), planPaid = r2(allowed - youOwe);
    const doc = { kind: 'explanation-of-benefits', title: 'Explanation of Benefits — This is not a bill', meta: [['Member', p.name], ['Service', r.pick(['Outpatient imaging', 'Urgent care visit', 'Physical therapy', 'Lab tests'])], ['Deductible remaining before this claim', money(dedLeft)], ['Coinsurance after deductible', '20%']],
      table: table(['Line', 'Amount'], [['Amount billed', money(billed)], ['Allowed amount', money(allowed)], ['Plan paid', level === 'support' ? money(planPaid) : '?'], ['You owe', level === 'support' ? '?' : '—']]), notes: [NOTE, 'You never pay more than the allowed amount at an in-network provider.'] };
    if (level === 'support') return { level, prompt: `How much does ${p.name} owe? You owe = allowed amount − plan paid.`, scenario: { document: doc }, ...numeric(youOwe), solutionSteps: [`${money(allowed)} − ${money(planPaid)} = ${money(youOwe)}.`] };
    if (level === 'standard') return { level, prompt: `${p.name}'s deductible is already met, so ${p.sub} pays 20% coinsurance on the allowed amount. How much does ${p.sub} owe?`, scenario: { document: doc }, ...numeric(youOwe), solutionSteps: [`20% × ${money(allowed)} = ${money(youOwe)}.`, `The plan pays ${money(planPaid)}; the billed amount above the allowed amount is written off.`] };
    return { level, prompt: `${p.name} still had part of the deductible left (see the EOB). ${p.Sub} pays that part first, then 20% of the rest of the allowed amount. How much does ${p.sub} owe?`, scenario: { document: doc }, ...numeric(youOwe), solutionSteps: [`Deductible part = ${money(dedLeft)}.`, `Coinsurance = 20% × (${money(allowed)} − ${money(dedLeft)}) = ${money((allowed - dedLeft) * co)}.`, `Total = ${money(youOwe)}.`] }; },
    (q) => { const allowed = docValue(q, /Allowed/), left = docValue(q, /Deductible remaining/); if (q.level === 'support') return r2(allowed - docValue(q, /Plan paid/)); return r2(left + (allowed - left) * 0.2); })
];

/* ---------- Housing: a lease summary ---------- */
const housing = [
  D(5, 9, 'lease', (r, k) => { const p = person(r), level = LV[k % 3], rent = r.step(850, 1950, 25), dep = rent, petDep = r.pick([0, 250, 300]), petRent = petDep ? r.pick([25, 35, 50]) : 0, fee = r.pick([50, 75]), daily = r.pick([10, 15]), grace = 5;
    const doc = { kind: 'lease-summary', title: 'Residential Lease — Key Terms', meta: [['Tenant', p.name], ['Term', '12 months'], ['Rent due', '1st of each month']],
      table: table(['Term', 'Amount'], [['Monthly rent', money(rent)], ['Security deposit', money(dep)], ['Pet deposit', money(petDep)], ['Monthly pet rent', money(petRent)], ['Late fee (after the 5th)', `${money(fee)} plus ${money(daily)} per day after the 5th`]]), notes: [NOTE, 'Deposits are refundable minus damage beyond normal wear and tear.'] };
    if (level === 'support') { const v = rent + dep + petDep + petRent; return { level, prompt: `How much must ${p.name} pay at move-in: first month's rent and pet rent plus both deposits?`, scenario: { document: doc }, ...numeric(v), solutionSteps: [`${money(rent)} + ${money(petRent)} + ${money(dep)} + ${money(petDep)} = ${money(v)}.`] }; }
    if (level === 'standard') { const day = r.int(6, 15), lf = fee + daily * (day - grace); return { level, prompt: `${p.name} pays rent on day ${day} of the month. Using the lease, what is the late fee?`, scenario: { document: doc }, ...numeric(lf), solutionSteps: [`Days after the 5th: ${day} − 5 = ${day - grace}.`, `${money(fee)} + ${money(daily)} × ${day - grace} = ${money(lf)}.`] }; }
    const ins = r.pick([12, 15, 18]), y = r2((rent + petRent) * 12 + ins * 12);
    return { level, prompt: `${p.name} also pays $${ins} a month for renters insurance. What will ${p.sub} spend in the first year on rent, pet rent and insurance (deposits are refunded)?`, scenario: { document: doc }, ...numeric(y), solutionSteps: [`Rent + pet rent = ${money(rent + petRent)} × 12 = ${money((rent + petRent) * 12)}.`, `Insurance = $${ins} × 12 = ${money(ins * 12)}.`, `Total = ${money(y)}.`] }; },
    (q) => { const rent = docValue(q, /Monthly rent/), pr = docValue(q, /pet rent/); if (q.level === 'support') return rent + docValue(q, /Security/) + docValue(q, /Pet deposit/) + pr; if (q.level === 'standard') { const cell = rows(q).find(x => /Late fee/.test(x[0]))[1], [fee, daily] = [...cell.matchAll(/\$([\d,.]+)/g)].map(m => num(m[1])), day = Number(q.prompt.match(/day (\d+)/)[1]); return fee + daily * (day - 5); } const ins = Number(q.prompt.match(/pays \$([\d.]+) a month/)[1]); return (rent + pr) * 12 + ins * 12; })
];

/* ---------- Investing: a fund fact sheet ---------- */
const investing = [
  D(3, 9, 'fund-fact-sheet', (r, k) => { const p = person(r), level = LV[k % 3], er = r.pick([0.0004, 0.001, 0.0065, 0.0095]), ret = r.pick([0.06, 0.07, 0.08]), bal = r.step(2000, 40000, 500);
    const doc = { kind: 'fund-fact-sheet', title: r.pick(['Cedar Total Market Index Fund', 'Harbor Growth Fund', 'Pine Ridge Balanced Fund']) + ' — Fact Sheet', meta: [['Expense ratio', pct(er, 2)], ['10-year average annual return (before fees)', pct(ret, 1)], ['Holdings', r.pick(['3,500 U.S. stocks', '70% stocks / 30% bonds', '120 large companies'])]], notes: [NOTE, 'Past returns do not guarantee future results.'] };
    if (level === 'support') return { level, prompt: `${p.name} has $${bal.toLocaleString('en-US')} in this fund. Yearly fee = balance × expense ratio. What is the fee?`, scenario: { document: doc }, ...numeric(r2(bal * er)), solutionSteps: [`$${bal.toLocaleString('en-US')} × ${pct(er, 2)} = ${money(bal * er)}.`] };
    if (level === 'standard') { const net = r2((ret - er) * 100); return { level, prompt: `What is the fund's return after fees, as a percent to the nearest hundredth? (Return before fees − expense ratio)`, scenario: { document: doc }, ...numeric(net, { unit: '%', d: 2, tolerance: 0.005 }), solutionSteps: [`${pct(ret, 1)} − ${pct(er, 2)} = ${net.toFixed(2)}%.`] }; }
    const y = 20, a = bal * (1 + ret - er) ** y, b = bal * (1 + ret - 0.012) ** y, d = r2(a - b);
    return { level, prompt: `If this fund keeps its average return, how much more would ${p.name}'s $${bal.toLocaleString('en-US')} grow to in 20 years here than in a similar fund charging 1.2% a year? (Grow by return − fee each year.)`, scenario: { document: doc }, ...numeric(d, { tolerance: 1 }), solutionSteps: [`This fund: $${bal.toLocaleString('en-US')} × (1 + ${(ret - er).toFixed(4)})^20 = ${money(a)}.`, `1.2% fund: × (1 + ${(ret - 0.012).toFixed(4)})^20 = ${money(b)}.`, `Difference = ${money(d)}.`] }; },
    (q) => { const er = docValue(q, /Expense/) / 100, ret = docValue(q, /10-year/) / 100; if (q.level === 'standard') return (ret - er) * 100; const bal = Number(q.prompt.match(/\$([\d,]+)/)[1].replace(/,/g, '')); if (q.level === 'support') return r2(bal * er); return bal * (1 + ret - er) ** 20 - bal * (1 + ret - 0.012) ** 20; })
];

/* ---------- Retirement: a benefits summary (match and vesting) ---------- */
const retirement = [
  D(3, 9, 'benefits-summary', (r, k) => { const p = person(r), level = LV[k % 3], sal = r.step(36000, 90000, 1000), c = r.pick([0.04, 0.06, 0.08]), mr = r.pick([0.5, 1]), cap = 0.06, per = 26;
    const doc = { kind: 'benefits-summary', title: '401(k) Plan Highlights — ' + r.pick(EMPLOYERS), meta: [['Employee', p.name], ['Salary', $0(sal)], ['Your contribution', pct(c, 0) + ' of pay'], ['Paychecks per year', String(per)]],
      table: table(['Feature', 'Details'], [['Employer match', `${mr === 1 ? '100%' : '50%'} of what you contribute, up to 6% of pay`], ['Vesting of employer money', '25% per full year of service (fully vested after 4 years)'], ['Your own contributions', 'Always 100% yours']]), notes: [NOTE] };
    if (level === 'support') return { level, prompt: `How much does ${p.name} contribute from each paycheck? Per paycheck = salary × contribution rate ÷ paychecks per year.`, scenario: { document: doc }, ...numeric(r2(sal * c / per)), solutionSteps: [`${$0(sal)} × ${pct(c, 0)} ÷ ${per} = ${money(sal * c / per)}.`] };
    const match = r2(sal * Math.min(c, cap) * mr);
    if (level === 'standard') return { level, prompt: `How much does the employer contribute to ${p.name}'s 401(k) in a year?`, scenario: { document: doc }, ...numeric(match), solutionSteps: [`Matched rate = the smaller of ${pct(c, 0)} and 6% = ${pct(Math.min(c, cap), 0)}.`, `Match = ${mr === 1 ? '100%' : '50%'} × ${pct(Math.min(c, cap), 0)} × ${$0(sal)} = ${money(match)}.`] };
    const yrs = r.int(1, 3), vested = r2(match * yrs * Math.min(1, 0.25 * yrs));
    return { level, prompt: `${p.name} leaves the job after exactly ${yrs} full year${yrs > 1 ? 's' : ''}, having received the same employer match each year. Ignoring investment growth, how much of the employer's money can ${p.sub} keep?`, scenario: { document: doc }, ...numeric(vested), solutionSteps: [`Employer money = ${money(match)} × ${yrs} = ${money(match * yrs)}.`, `Vested = ${Math.min(100, 25 * yrs)}%.`, `${p.Sub} keeps ${money(vested)}.`] }; },
    (q) => { const sal = docValue(q, /Salary/), c = docValue(q, /Your contribution/) / 100, per = docValue(q, /Paychecks/); if (q.level === 'support') return r2(sal * c / per); const mr = /100%/.test(rows(q)[0][1]) ? 1 : 0.5, match = r2(sal * Math.min(c, 0.06) * mr); if (q.level === 'standard') return match; const yrs = Number(q.prompt.match(/exactly (\d+)/)[1]); return r2(match * yrs * Math.min(1, 0.25 * yrs)); })
];

export const documentFamilies = { income, budgeting, credit, borrowing, insurance, housing, investing, retirement };
