/* Spreadsheet labs (2026-11-17): question sets that match the three downloadable templates in
 * financial/spreadsheet-labs/ (budget, amortization table, PMT and FV). Each question shows a small spreadsheet
 * with its formulas and asks what a cell displays, so students practice reading and writing formulas the way they
 * will in Google Sheets or Excel. Nine questions per lab, three per level. verify(q) re-reads the grid. */
import { M, money, pct, person, numeric } from './kit.mjs';

const r2 = M.round2, LV = ['support', 'standard', 'advanced'];
const pmt = (P, apr, n) => { const i = apr / 12; return i ? P * i / (1 - (1 + i) ** -n) : P / n; };
const fv = (c, apr, n) => { const i = apr / 12; return c * ((1 + i) ** n - 1) / i; };
const grid = (cols, rows, caption) => ({ headers: ['', ...cols], rows: rows.map((r, i) => [String(i + 1), ...r]), caption: caption || 'Spreadsheet: formulas are shown in the cells that have them.' });
/* Read a cell such as "B4" from the grid. */
export function cell(q, ref) {
  const t = q.scenario.table, col = t.headers.indexOf(ref.replace(/\d+/g, '')), row = t.rows.find(r => r[0] === ref.replace(/\D+/g, ''));
  return row[col];
}
const val = (s) => Number(String(s).replace(/[$,%\s]/g, '')) / (/%/.test(s) ? 100 : 1);
const L = (unit, skill, id, gen, verify) => ({ unit, fam: { id: 'lv-x-' + id, skill, type: 'calculation', count: 9, game: false, activities: ['worksheet', 'assessment', 'lesson', 'spreadsheet-lab'], gen, verify } });

const labs = [
  L('budgeting', 1, 'budget', (r, k) => { const p = person(r), level = LV[k % 3];
    const items = [['Net pay (monthly)', r.step(1800, 3600, 25)], ['Rent', r.step(650, 1300, 25)], ['Utilities', r.step(60, 180, 5)], ['Phone', r.step(30, 80, 5)], ['Groceries', r.step(200, 450, 10)], ['Gas and transit', r.step(60, 220, 10)], ['Fun', r.step(40, 200, 10)]];
    const inc = items[0][1], exp = items.slice(1).reduce((a, x) => a + x[1], 0), net = inc - exp;
    const rows = [['Item', 'Monthly amount'], ...items.map(([n, v]) => [n, '$' + v.toLocaleString('en-US')]), ['Total expenses', '=SUM(B3:B8)'], ['Net cash flow', '=B2-B9']];
    const t = grid(['A', 'B'], rows, `${p.name}'s budget template (Spreadsheet Lab 1). Formulas are shown in B9 and B10.`);
    if (level === 'support') return { level, prompt: `What value does cell B9, =SUM(B3:B8), display?`, scenario: { table: t }, ...numeric(exp),
      solutionSteps: ['Formula: =SUM(B3:B8) adds every expense in rows 3 to 8.', `Substitute: ${items.slice(1).map(x => '$' + x[1].toLocaleString('en-US')).join(' + ')} = $${exp.toLocaleString('en-US')}.`, 'Spreadsheet: type =SUM( then drag from B3 to B8 and close the parenthesis.', `So ${p.name}'s expenses total $${exp.toLocaleString('en-US')} a month.`] };
    if (level === 'standard') return { level, prompt: `What value does cell B10, =B2-B9, display? (A negative result means a deficit.)`, scenario: { table: t }, ...numeric(net),
      solutionSteps: ['Formula: net cash flow = income − total expenses, so =B2-B9.', `Substitute: $${inc.toLocaleString('en-US')} − $${exp.toLocaleString('en-US')} = ${money(net)}.`, 'Spreadsheet: B9 must hold =SUM(B3:B8) first; B10 then updates whenever any amount changes.', net >= 0 ? `So ${p.name} has ${money(net)} left each month for savings or goals.` : `So ${p.name} is ${money(-net)} short each month and needs to cut spending or earn more.`] };
    const target = r.pick([100, 150, 200, 250]), need = inc - (exp - items[6][1]) - target;
    if (need < 0) return null;
    return { level, prompt: `${p.name} wants B10 to show exactly $${target} so it can go to savings. What amount in B8 (Fun) does that? (In Excel this is Data → What-If Analysis → Goal Seek; in Google Sheets, solve it by hand or with the Goal Seek add-on.)`, scenario: { table: t }, ...numeric(need),
      solutionSteps: [`Formula: B2 − (other expenses + B8) = $${target}, so B8 = B2 − other expenses − $${target}.`, `Substitute: other expenses = $${(exp - items[6][1]).toLocaleString('en-US')}; B8 = $${inc.toLocaleString('en-US')} − $${(exp - items[6][1]).toLocaleString('en-US')} − $${target} = ${money(need)}.`, `Spreadsheet: Goal Seek with Set cell B10, To value ${target}, By changing cell B8.`, need < items[6][1] ? `So ${p.name} would cut Fun from $${items[6][1]} to ${money(need)} a month to save $${target}.` : `So ${p.name} could spend up to ${money(need)} on Fun and still save $${target}.`] }; },
    (q) => { const v = (ref) => val(cell(q, ref)), exp = ['B3', 'B4', 'B5', 'B6', 'B7', 'B8'].reduce((a, c) => a + v(c), 0); if (q.level === 'support') return exp; if (q.level === 'standard') return v('B2') - exp; return v('B2') - (exp - v('B8')) - Number(q.prompt.match(/exactly \$(\d+)/)[1]); }),

  L('borrowing', 3, 'amortization', (r, k) => { const p = person(r), level = LV[k % 3], P = r.step(6000, 24000, 500), apr = r.pick([0.045, 0.06, 0.075, 0.09]), n = r.pick([12, 24, 36, 48]), pay = r2(pmt(P, apr, n));
    const i1 = r2(P * apr / 12), b1 = r2(P - (pay - i1)), i2 = r2(b1 * apr / 12), b2 = r2(b1 - (pay - i2));
    const rows = [['Loan amount', '$' + P.toLocaleString('en-US'), '', '', ''], ['APR', pct(apr, 1), '', '', ''], ['Months', String(n), '', '', ''], ['Payment', '=ROUND(PMT(B2/12,B3,-B1),2)', '', '', ''], ['', '', '', '', ''], ['Payment #', 'Payment', 'Interest', 'Principal', 'Balance'], ['0', '', '', '', '=B1'], ['1', '=$B$4', '=ROUND(E7*$B$2/12,2)', '=B8-C8', '=E7-D8'], ['2', '=$B$4', '=ROUND(E8*$B$2/12,2)', '=B9-C9', '=E8-D9']];
    const t = grid(['A', 'B', 'C', 'D', 'E'], rows, `${p.name}'s amortization template (Spreadsheet Lab 2). B4 displays ${money(pay)}.`);
    if (level === 'support') return { level, prompt: `What value does cell C8, =ROUND(E7*$B$2/12,2), display? (The interest in month 1.)`, scenario: { table: t }, ...numeric(i1),
      solutionSteps: ['Formula: interest = balance × APR ÷ 12, rounded to the cent.', `Substitute: $${P.toLocaleString('en-US')} × ${apr} ÷ 12 = ${money(i1)}.`, 'Spreadsheet: $B$2 is an absolute reference, so the formula still points at the APR when it is filled down the table.', `So ${money(i1)} of the first ${money(pay)} payment is interest; the other ${money(pay - i1)} pays down the loan.`] };
    if (level === 'standard') return { level, prompt: `What value does cell E9 display: the balance after payment 2?`, scenario: { table: t }, ...numeric(b2),
      solutionSteps: ['Formula: each row: interest = previous balance × APR ÷ 12; principal = payment − interest; new balance = previous balance − principal.', `Row 8: interest ${money(i1)}, principal ${money(pay - i1)}, balance ${money(b1)}.`, `Row 9: interest = ${money(b1)} × ${apr} ÷ 12 = ${money(i2)}; principal = ${money(pay - i2)}; balance = ${money(b1)} − ${money(pay - i2)} = ${money(b2)}.`, 'Spreadsheet: select A9:E9 and fill down to row ' + (n + 7) + ' to finish the table; the last balance should be about $0.', `So after two payments ${p.name} still owes ${money(b2)}.`] };
    const tot = r2(pay * n - P);
    return { level, prompt: `${p.name} adds cell B5 with =B4*B3-B1. What does it display, the total interest over the life of the loan?`, scenario: { table: t }, ...numeric(tot),
      solutionSteps: ['Formula: total interest = payment × number of payments − amount borrowed.', `Substitute: ${money(pay)} × ${n} − $${P.toLocaleString('en-US')} = ${money(pay * n)} − $${P.toLocaleString('en-US')} = ${money(tot)}.`, `Spreadsheet: =B4*B3-B1, or =SUM(C8:C${n + 7}) once the table is filled down (the two can differ by a few cents of rounding).`, `So borrowing $${P.toLocaleString('en-US')} for ${n} months costs ${money(tot)} in interest, ${(tot / P * 100).toFixed(1)}% of the loan.`] }; },
    (q) => { const P = val(cell(q, 'B1')), apr = val(cell(q, 'B2')), n = val(cell(q, 'B3')), pay = r2(pmt(P, apr, n)); const i1 = r2(P * apr / 12), b1 = r2(P - pay + i1); if (q.level === 'support') return i1; if (q.level === 'standard') { const i2 = r2(b1 * apr / 12); return r2(b1 - pay + i2); } return pay * n - P; }),

  L('investing', 2, 'pmt-fv', (r, k) => { const p = person(r), level = LV[k % 3];
    if (level === 'support') { const c = r.step(25, 300, 25), apr = r.pick([0.04, 0.05, 0.06, 0.07]), n = r.pick([60, 120, 180, 240]), v = r2(fv(c, apr, n));
      const t = grid(['A', 'B'], [['Monthly deposit', '$' + c], ['APR', pct(apr, 0)], ['Months', String(n)], ['Future value', '=FV(B2/12,B3,-B1)']], 'PMT and FV template (Spreadsheet Lab 3).');
      return { level, prompt: `${p.name} saves the same amount every month. What does cell B4, =FV(B2/12,B3,-B1), display?`, scenario: { table: t }, ...numeric(v),
        solutionSteps: ['Formula: FV = deposit × [(1 + i)^n − 1] ÷ i, with i = APR ÷ 12.', `Substitute: $${c} × [(1 + ${apr} ÷ 12)^${n} − 1] ÷ (${apr} ÷ 12) = ${money(v)}.`, 'Spreadsheet: =FV(rate per period, number of periods, payment). The deposit is negative because it leaves your pocket.', `So $${c} a month for ${n / 12} years grows to ${money(v)}; ${money(c * n)} of that is deposits and ${money(v - c * n)} is interest.`] }; }
    if (level === 'standard') { const P = r.step(5000, 30000, 500), apr = r.pick([0.049, 0.059, 0.069, 0.079]), n = r.pick([36, 48, 60, 72]), v = r2(pmt(P, apr, n));
      const t = grid(['A', 'B'], [['Amount borrowed', '$' + P.toLocaleString('en-US')], ['APR', pct(apr, 1)], ['Months', String(n)], ['Monthly payment', '=PMT(B2/12,B3,-B1)']], 'PMT and FV template (Spreadsheet Lab 3).');
      return { level, prompt: `What monthly payment does cell B4, =PMT(B2/12,B3,-B1), display?`, scenario: { table: t }, ...numeric(v),
        solutionSteps: ['Formula: PMT = P × i ÷ [1 − (1 + i)^−n], with i = APR ÷ 12.', `Substitute: $${P.toLocaleString('en-US')} × (${apr} ÷ 12) ÷ [1 − (1 + ${apr} ÷ 12)^−${n}] = ${money(v)}.`, 'Spreadsheet: =PMT(rate per period, number of periods, present value). -B1 makes the answer positive.', `So ${p.name} pays ${money(v)} a month, ${money(v * n)} in all: ${money(v * n - P)} of interest.`] }; }
    const goal = r.step(5000, 40000, 1000), apr = r.pick([0.03, 0.04, 0.05]), n = r.pick([24, 36, 48, 60]), v = r2(goal / fv(1, apr, n));
    const t = grid(['A', 'B'], [['Savings goal', '$' + goal.toLocaleString('en-US')], ['APR', pct(apr, 0)], ['Months', String(n)], ['Deposit needed', '=PMT(B2/12,B3,0,-B1)']], 'PMT and FV template (Spreadsheet Lab 3).');
    return { level, prompt: `${p.name} wants $${goal.toLocaleString('en-US')} in ${n} months for a car down payment. What monthly deposit does cell B4, =PMT(B2/12,B3,0,-B1), display?`, scenario: { table: t }, ...numeric(v),
      solutionSteps: ['Formula: deposit = goal × i ÷ [(1 + i)^n − 1], the FV formula solved for the deposit.', `Substitute: $${goal.toLocaleString('en-US')} × (${apr} ÷ 12) ÷ [(1 + ${apr} ÷ 12)^${n} − 1] = ${money(v)}.`, 'Spreadsheet: =PMT(rate, periods, 0, -goal): present value 0, future value = the goal. Check with =FV(B2/12,B3,-B4), which should show the goal.', `So ${p.name} needs to save ${money(v)} a month; interest supplies ${money(goal - v * n)} of the goal.`] }; },
    (q) => { const v = (ref) => val(cell(q, ref)), f = cell(q, 'B4'); if (/^=FV/.test(f)) return fv(v('B1'), v('B2'), v('B3')); if (/,0,-B1/.test(f)) return v('B1') / fv(1, v('B2'), v('B3')); return pmt(v('B1'), v('B2'), v('B3')); })
];

export const spreadsheetFamilies = {};
for (const l of labs) (spreadsheetFamilies[l.unit] = spreadsheetFamilies[l.unit] || []).push(l.fam);
