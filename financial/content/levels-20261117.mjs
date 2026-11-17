/* Support and Advanced question families (2026-11-17), one of each per skill.
 *   Support: whole numbers, one step, the formula is given in the question.
 *   Advanced: several steps, solving for an unknown (rate, time, payment, amount), or comparing options.
 * Existing questions are sorted into the three levels by scripts/build-banks.mjs (levels.mjs); these families
 * fill each level to at least 16 questions per skill. Every family carries verify(prompt), which re-reads the
 * numbers from the question text and recomputes the answer without the generator's variables;
 * tests/fa-levels.test.mjs runs it on every generated question. */
import { M, money, $, $0, pct, person, numeric } from './kit.mjs';
import { TAX_2026 } from './real-data-2026.mjs';

const r2 = M.round2;
const nums = (s) => [...String(s).matchAll(/[−-]?\$?([\d,]+(?:\.\d+)?)/g)].map(m => Number(m[1].replace(/,/g, '')));
const dollars = (s) => [...String(s).matchAll(/\$([\d,]+(?:\.\d+)?)/g)].map(m => Number(m[1].replace(/,/g, '')));
const rates = (s) => [...String(s).matchAll(/([\d.]+)%/g)].map(m => Number(m[1]) / 100);
const after = (s, re) => Number(String(s).match(re)[1].replace(/,/g, ''));
const pmt = (P, apr, n) => { const i = apr / 12; return i ? P * i / (1 - (1 + i) ** -n) : P / n; };
function tax2026(taxable) { let t = 0, lo = 0; for (const b of TAX_2026.bracketsSingle) { if (taxable <= lo) break; t += (Math.min(taxable, b.upTo) - lo) * b.rate; lo = b.upTo; } return t; }
const int = (v) => numeric(v, { unit: 'count', display: String(v) });
const S = (skill, count, id, type, gen, verify) => ({ id: 'lv-s-' + id, skill, level: 'support', type, count, gen, verify });
const A = (skill, count, id, type, gen, verify) => ({ id: 'lv-a-' + id, skill, level: 'advanced', type, count, gen, verify });
const steps = (...a) => a.filter(Boolean);

/* ---------- Unit 1: Careers & Income ---------- */
const income = [
  S(1, 4, 'hourly-annual', 'calculation', r => { const p = person(r), w = r.int(14, 30); return { prompt: `${p.name} earns $${w} per hour and works 2,080 hours a year (40 hours × 52 weeks). Annual pay = hourly rate × 2,080. What is ${p.pos} annual pay?`, ...numeric(w * 2080), solutionSteps: steps(`$${w} × 2,080 = ${$0(w * 2080)}.`) }; },
    p => dollars(p)[0] * 2080),
  A(1, 4, 'offer-compare', 'comparison', r => { const p = person(r), sal = r.step(46000, 60000, 1000), hrs = r.pick([45, 48, 50]), w = r.pick([22, 23.5, 24, 25.5]), ot = r.pick([3, 4, 5]);
    const a = sal, b = r2(w * 40 * 50 + w * 1.5 * ot * 50), d = r2(Math.abs(a - b));
    return { prompt: `${p.name} compares two offers. Offer A: ${$0(sal)} salary, about ${hrs} hours a week. Offer B: ${money(w)} per hour for 40 hours plus ${ot} overtime hours a week at 1.5 times the rate, for 50 weeks. How much more does the higher-paying offer earn in a year?`,
      ...numeric(d), solutionSteps: steps(`Offer B regular: ${money(w)} × 40 × 50 = ${money(w * 2000)}.`, `Offer B overtime: ${money(w)} × 1.5 × ${ot} × 50 = ${money(w * 75 * ot)}.`, `Offer B total ${money(b)} vs Offer A ${$0(a)}: difference ${money(d)}.`, `Per hour, Offer A pays ${money(sal / (hrs * 52))} because of its long hours.`) }; },
    p => { const [sal, w] = dollars(p), ot = after(p, /plus (\d+) overtime/); return Math.abs(sal - (w * 2000 + w * 75 * ot)); }),
  S(2, 4, 'net-simple', 'calculation', r => { const p = person(r), g = r.step(800, 2400, 50), d = r.step(120, 500, 10); return { prompt: `${p.name}'s gross pay is $${g.toLocaleString('en-US')} and total deductions are $${d}. Net pay = gross pay − deductions. What is ${p.pos} net pay?`, ...numeric(g - d), solutionSteps: steps(`$${g.toLocaleString('en-US')} − $${d} = ${$0(g - d)}.`) }; },
    p => { const [g, d] = dollars(p); return g - d; }),
  A(2, 7, 'gross-from-net', 'calculation', r => { const p = person(r), rate = r.pick([0.18, 0.2, 0.22, 0.24, 0.25]), net = r.step(1200, 3200, 0.5), g = r2(net / (1 - rate));
    return { prompt: `About ${pct(rate, 0)} of ${p.name}'s gross pay goes to taxes and deductions. ${p.Sub} wants net pay of ${money(net)} per paycheck. What gross pay per paycheck does ${p.sub} need?`,
      ...numeric(g, { tolerance: 0.01 }), solutionSteps: steps(`Net = gross × (1 − ${rate}) = gross × ${(1 - rate).toFixed(2)}.`, `Gross = ${money(net)} ÷ ${(1 - rate).toFixed(2)} = ${money(g)}.`, 'Adding the rate to the net (net × 1.2) is a common mistake: the rate is a share of gross, not of net.') }; },
    p => dollars(p)[0] / (1 - rates(p)[0])),
  S(3, 8, 'ytd-add', 'calculation', r => { const p = person(r), ytd = r.step(9000, 30000, 100), now = r.step(900, 2000, 50); return { prompt: `${p.name}'s year-to-date gross pay before this paycheck was $${ytd.toLocaleString('en-US')}. This paycheck's gross pay is $${now.toLocaleString('en-US')}. New YTD = old YTD + this paycheck. What does the stub show for year-to-date gross?`, ...numeric(ytd + now), solutionSteps: steps(`$${ytd.toLocaleString('en-US')} + $${now.toLocaleString('en-US')} = ${$0(ytd + now)}.`) }; },
    p => { const [a, b] = dollars(p); return a + b; }),
  A(3, 4, 'missing-deduction', 'document', r => { const p = person(r), g = r.step(1400, 2800, 0.5), fed = r2(g * r.pick([0.07, 0.08, 0.09])), ss = r2(g * 0.062), med = r2(g * 0.0145), st = r2(g * r.pick([0.03, 0.04, 0.05])), net = r2(g - fed - ss - med - st);
    return { prompt: `A pay stub shows gross pay ${money(g)}, federal tax ${money(fed)}, Social Security ${money(ss)}, Medicare ${money(med)}, and net pay ${money(net)}. The state tax amount is smudged. What is the state tax?`,
      ...numeric(st), solutionSteps: steps(`Total deductions = gross − net = ${money(g)} − ${money(net)} = ${money(g - net)}.`, `State tax = ${money(g - net)} − (${money(fed)} + ${money(ss)} + ${money(med)}) = ${money(st)}.`) }; },
    p => { const [g, f, s, m, n] = dollars(p); return g - n - f - s - m; }),
  S(4, 4, 'tax-10', 'calculation', r => { const p = person(r), t = r.step(3000, 12000, 100); return { prompt: `In 2026 the first $12,400 of a single filer's taxable income is taxed at 10%. ${p.name} has taxable income of $${t.toLocaleString('en-US')}. Tax = 10% × taxable income. What is ${p.pos} federal income tax?`, ...numeric(t * 0.1), solutionSteps: steps(`0.10 × $${t.toLocaleString('en-US')} = ${money(t * 0.1)}.`) }; },
    p => dollars(p)[1] * 0.1),
  A(4, 4, 'tax-401k-2026', 'calculation', r => { const p = person(r), gross = r.step(60000, 140000, 1000), k = r.pick([0.04, 0.06, 0.08, 0.1]), taxable = gross - gross * k - TAX_2026.standardDeduction.single, t = r2(tax2026(taxable));
    return { prompt: `${p.name} earns ${$0(gross)} in 2026, puts ${pct(k, 0)} of pay into a traditional 401(k) (pre-tax), and takes the ${$0(TAX_2026.standardDeduction.single)} standard deduction. Using the 2026 single-filer brackets (10% to $12,400; 12% to $50,400; 22% to $105,700; 24% to $201,775), what is ${p.pos} federal income tax?`,
      ...numeric(t), solutionSteps: steps(`401(k) = ${pct(k, 0)} × ${$0(gross)} = ${$0(gross * k)}.`, `Taxable = ${$0(gross)} − ${$0(gross * k)} − ${$0(TAX_2026.standardDeduction.single)} = ${$0(taxable)}.`, `Tax by brackets = ${money(t)}.`, 'The pre-tax 401(k) lowers taxable income, so it lowers the tax.') }; },
    p => { const [gross, sd] = dollars(p), k = rates(p)[0]; return tax2026(gross - gross * k - sd); })
];

/* ---------- Unit 2: Budgeting & Spending ---------- */
const budgeting = [
  S(1, 4, 'cash-flow', 'calculation', r => { const p = person(r), i = r.step(1800, 4200, 50), e = r.step(1500, 4000, 50); return { prompt: `${p.name}'s monthly income is $${i.toLocaleString('en-US')} and monthly expenses are $${e.toLocaleString('en-US')}. Cash flow = income − expenses. What is ${p.pos} monthly cash flow?`, ...numeric(i - e), solutionSteps: steps(`$${i.toLocaleString('en-US')} − $${e.toLocaleString('en-US')} = ${money(i - e)}.`, i - e < 0 ? 'Negative cash flow means spending more than earning.' : 'Positive cash flow can go to savings.') }; },
    p => { const [i, e] = dollars(p); return i - e; }),
  A(1, 4, 'goal-months', 'calculation', r => { const p = person(r), inc = r.step(2400, 4200, 50), exp = r.step(1800, inc - 200, 50), annual = r.step(600, 1500, 50), goal = r.step(1500, 6000, 100), cf = r2(inc - exp - annual / 12), m = Math.ceil(goal / cf);
    return { prompt: `${p.name} earns $${inc.toLocaleString('en-US')} a month and spends $${exp.toLocaleString('en-US')} a month, plus a $${annual.toLocaleString('en-US')} insurance bill once a year. Saving the rest, how many whole months will it take to save $${goal.toLocaleString('en-US')}?`,
      ...int(m), solutionSteps: steps(`Set aside the yearly bill monthly: $${annual.toLocaleString('en-US')} ÷ 12 = ${money(annual / 12)}.`, `Monthly savings = ${$0(inc)} − ${$0(exp)} − ${money(annual / 12)} = ${money(cf)}.`, `$${goal.toLocaleString('en-US')} ÷ ${money(cf)} = ${(goal / cf).toFixed(2)}, so ${m} months (round up).`) }; },
    p => { const [inc, exp, annual, goal] = dollars(p); return Math.ceil(goal / (inc - exp - annual / 12)); }),
  S(2, 6, 'fixed-total', 'calculation', r => { const p = person(r), rent = r.step(700, 1400, 25), phone = r.step(30, 80, 5), car = r.step(150, 400, 10); return { prompt: `${p.name}'s fixed expenses are rent $${rent.toLocaleString('en-US')}, phone $${phone} and car payment $${car}. Add them. What are ${p.pos} total fixed expenses per month?`, ...numeric(rent + phone + car), solutionSteps: steps(`$${rent.toLocaleString('en-US')} + $${phone} + $${car} = ${$0(rent + phone + car)}.`) }; },
    p => dollars(p).reduce((a, b) => a + b, 0)),
  A(2, 4, 'cut-percent', 'calculation', r => { const p = person(r), v = r.step(600, 1500, 10), save = r.step(60, Math.floor(v * 0.3), 5), pc = r2(save / v * 100);
    return { prompt: `${p.name} spends $${v.toLocaleString('en-US')} a month on variable expenses and wants to free up $${save} a month for savings by cutting them. By what percent must ${p.sub} cut variable spending, to the nearest tenth of a percent?`,
      ...numeric(pc, { unit: '%', d: 1, tolerance: 0.05 }), solutionSteps: steps(`Percent cut = $${save} ÷ $${v.toLocaleString('en-US')}.`, `= ${(save / v).toFixed(4)} ≈ ${pc.toFixed(1)}%.`) }; },
    p => { const [v, s] = dollars(p); return s / v * 100; }),
  S(3, 4, 'how-many', 'calculation', r => { const p = person(r), b = r.step(40, 200, 5), c = r.pick([6, 7, 8, 9, 12, 15]); return { prompt: `${p.name} has $${b} to spend on books that cost $${c} each. Number of books = budget ÷ price, rounded down. How many books can ${p.sub} buy?`, ...int(Math.floor(b / c)), solutionSteps: steps(`$${b} ÷ $${c} = ${(b / c).toFixed(2)}.`, `Round down: ${Math.floor(b / c)} books.`) }; },
    p => { const [b, c] = dollars(p); return Math.floor(b / c); }),
  A(3, 4, 'two-items', 'calculation', r => { const p = person(r), B = r.step(120, 300, 10), a = r.pick([11.5, 12.25, 13.75, 14.5]), y = r.int(2, 5), m = r.pick([8.5, 9.25, 10.75]), tax = 0.08, x = Math.floor((B / (1 + tax) - y * m) / a);
    if (x < 1) return null;
    return { prompt: `${p.name} has $${B} for a team outing. Lunch for each of ${y} coaches costs ${money(m)}, and each player ticket costs ${money(a)}. Sales tax of 8% is added to everything. What is the greatest number of player tickets ${p.sub} can buy?`,
      ...int(x), solutionSteps: steps(`Before tax, the total must be ≤ $${B} ÷ 1.08 = ${money(B / 1.08)}.`, `Coaches' lunches = ${y} × ${money(m)} = ${money(y * m)}.`, `Tickets ≤ (${money(B / 1.08)} − ${money(y * m)}) ÷ ${money(a)} = ${((B / 1.08 - y * m) / a).toFixed(2)} → ${x}.`) }; },
    p => { const [B, m, a] = dollars(p), y = after(p, /each of (\d+) coaches/); return Math.floor((B / 1.08 - y * m) / a); }),
  S(4, 4, 'habit-year', 'calculation', r => { const p = person(r), c = r.pick([3, 4, 5, 6]), d = r.pick([3, 4, 5]); return { prompt: `${p.name} buys a $${c} drink ${d} days a week. Yearly cost = price × days per week × 52. How much is that per year?`, ...numeric(c * d * 52), solutionSteps: steps(`$${c} × ${d} × 52 = ${$0(c * d * 52)}.`) }; },
    p => dollars(p)[0] * after(p, /drink (\d+) days/) * 52),
  A(4, 4, 'buy-vs-rent', 'comparison', r => { const p = person(r), item = r.pick(['a tuxedo', 'a carpet cleaner', 'a camping tent', 'a graphing calculator']), buy = r.step(120, 400, 10), rent = r.step(20, 60, 5), m = Math.ceil(buy / rent);
    return { prompt: `${p.name} can buy ${item} for $${buy} or rent one for $${rent} each time it is used. After how many uses does buying become cheaper than renting?`,
      ...int(buy % rent === 0 ? buy / rent + 1 : m), solutionSteps: steps(`Renting n times costs $${rent}n; buying costs $${buy}.`, `$${buy} ÷ $${rent} = ${(buy / rent).toFixed(2)}.`, `Buying is cheaper from use ${buy % rent === 0 ? buy / rent + 1 : m} on.`) }; },
    p => { const [buy, rent] = dollars(p); return buy % rent === 0 ? buy / rent + 1 : Math.ceil(buy / rent); })
];

/* ---------- Unit 3: Banking & Saving ---------- */
const banking = [
  S(1, 5, 'fee-year', 'calculation', r => { const p = person(r), f = r.pick([5, 8, 10, 12, 15]); return { prompt: `${p.name}'s checking account charges a $${f} monthly fee. Yearly cost = monthly fee × 12. How much does ${p.sub} pay in a year?`, ...numeric(f * 12), solutionSteps: steps(`$${f} × 12 = $${f * 12}.`) }; },
    p => dollars(p)[0] * 12),
  A(1, 5, 'fee-breakeven', 'calculation', r => { const fee = r.pick([6, 8, 10, 12]), apy = r.pick([0.03, 0.04, 0.045, 0.05]), bal = r2(fee * 12 / apy);
    return { prompt: `A savings account charges $${fee} a month but pays ${pct(apy)} APY. What balance earns enough interest in a year to cover the fees?`,
      ...numeric(bal, { tolerance: 0.01 }), solutionSteps: steps(`Yearly fees = $${fee} × 12 = $${fee * 12}.`, `Balance × ${apy} = $${fee * 12}, so balance = $${fee * 12} ÷ ${apy} = ${money(bal)}.`, 'Below that balance the account loses money.') }; },
    p => dollars(p)[0] * 12 / rates(p)[0]),
  S(2, 9, 'si-basic', 'calculation', r => { const p = person(r), P = r.step(500, 5000, 100), rate = r.pick([2, 3, 4, 5]), t = r.int(1, 4); return { prompt: `${p.name} deposits $${P.toLocaleString('en-US')} at ${rate}% simple interest for ${t} years. Use I = P × r × t. How much interest does ${p.sub} earn?`, ...numeric(P * rate / 100 * t), solutionSteps: steps(`I = $${P.toLocaleString('en-US')} × 0.0${rate} × ${t} = ${money(P * rate / 100 * t)}.`) }; },
    p => dollars(p)[0] * rates(p)[0] * after(p, /for (\d+) years/)),
  A(2, 9, 'si-time', 'calculation', r => { const p = person(r), P = r.step(2000, 9000, 250), rate = r.pick([0.025, 0.03, 0.035, 0.04]), I = r.step(300, 1500, 25), t = r2(I / (P * rate));
    return { prompt: `${p.name} has ${$0(P)} earning ${pct(rate)} simple interest. How many years will it take to earn ${$0(I)} in interest, to the nearest hundredth of a year?`,
      ...numeric(t, { unit: 'count', display: String(t), tolerance: 0.01 }), solutionSteps: steps('I = Prt, so t = I ÷ (P × r).', `t = ${$0(I)} ÷ (${$0(P)} × ${rate}) = ${t}.`) }; },
    p => { const [P, I] = dollars(p); return I / (P * rates(p)[0]); }),
  S(3, 4, 'cd-year', 'calculation', r => { const p = person(r), P = r.step(1000, 10000, 500), apy = r.pick([3, 4, 5]); return { prompt: `${p.name} puts $${P.toLocaleString('en-US')} in a 1-year CD paying ${apy}% APY. Interest = deposit × APY. How much interest does ${p.sub} earn?`, ...numeric(P * apy / 100), solutionSteps: steps(`$${P.toLocaleString('en-US')} × 0.0${apy} = ${money(P * apy / 100)}.`) }; },
    p => dollars(p)[0] * rates(p)[0]),
  A(3, 7, 'cd-penalty', 'comparison', r => { const p = person(r), P = r.step(3000, 15000, 500), cd = r.pick([0.045, 0.05, 0.052]), sav = r.pick([0.03, 0.035, 0.038]), pen = r.pick([3, 6]);
    const cdNet = r2(P * cd * 1.5 - P * cd / 12 * pen), sv = r2(P * sav * 1.5), d = r2(Math.abs(cdNet - sv));
    return { prompt: `${p.name} has ${$0(P)}. A 2-year CD pays ${pct(cd)} simple interest but charges ${pen} months of interest if cashed out early; a savings account pays ${pct(sav)}. ${p.Sub} expects to need the money after 18 months. Using simple interest, how much more does the better choice earn?`,
      ...numeric(d), solutionSteps: steps(`CD: ${$0(P)} × ${cd} × 1.5 = ${money(P * cd * 1.5)}, minus penalty ${$0(P)} × ${cd} ÷ 12 × ${pen} = ${money(P * cd / 12 * pen)} → ${money(cdNet)}.`, `Savings: ${$0(P)} × ${sav} × 1.5 = ${money(sv)}.`, `The ${cdNet > sv ? 'CD' : 'savings account'} earns ${money(d)} more.`) }; },
    p => { const [P] = dollars(p), [cd, sav] = rates(p), pen = after(p, /charges (\d+) months/); return Math.abs(P * cd * 1.5 - P * cd / 12 * pen - P * sav * 1.5); }),
  S(4, 10, 'ending-balance', 'document', r => { const p = person(r), s = r.step(200, 1500, 10), d = r.step(100, 900, 10), w = r.step(50, 700, 10); return { prompt: `${p.name}'s statement starts at $${s.toLocaleString('en-US')}. Deposits total $${d} and withdrawals total $${w}. Ending balance = start + deposits − withdrawals. What is the ending balance?`, ...numeric(s + d - w), solutionSteps: steps(`$${s.toLocaleString('en-US')} + $${d} − $${w} = ${money(s + d - w)}.`) }; },
    p => { const [s, d, w] = dollars(p); return s + d - w; }),
  A(4, 8, 'missing-transaction', 'document', r => { const p = person(r), s = r.step(400, 2000, 0.01), deps = [r.step(100, 800, 0.01), r.step(50, 400, 0.01)], ch = [r.step(20, 300, 0.01), r.step(20, 300, 0.01)], miss = r.step(30, 250, 0.01), e = r2(s + deps[0] + deps[1] - ch[0] - ch[1] - miss);
    return { prompt: `${p.name}'s statement: starting balance ${money(s)}, deposits ${money(deps[0])} and ${money(deps[1])}, checks ${money(ch[0])} and ${money(ch[1])}, one debit-card purchase with the amount torn off, and an ending balance of ${money(e)}. What was the purchase amount?`,
      ...numeric(miss), solutionSteps: steps(`Start + deposits − checks = ${money(s + deps[0] + deps[1] - ch[0] - ch[1])}.`, `Purchase = ${money(s + deps[0] + deps[1] - ch[0] - ch[1])} − ${money(e)} = ${money(miss)}.`) }; },
    p => { const [s, d1, d2, c1, c2, e] = dollars(p); return s + d1 + d2 - c1 - c2 - e; }),
  S(5, 5, 'debit-50', 'calculation', r => { const p = person(r), x = r.step(150, 900, 10); return { prompt: `A thief spends $${x} with ${p.name}'s stolen debit card. ${p.Sub} reports it within two business days, so ${p.pos} loss is capped at $50. Refund = amount stolen − $50. How much does the bank give back?`, ...numeric(x - 50), solutionSteps: steps(`$${x} − $50 = $${x - 50}.`) }; },
    p => dollars(p)[0] - 50),
  A(5, 8, 'scam-total', 'calculation', r => { const p = person(r), check = r.step(1800, 3000, 50), price = r.step(200, 500, 10), fee = r.pick([25, 35]), stolen = r.step(600, 1500, 10);
    const loss = r2(check - price + fee + Math.min(stolen, 500));
    return { prompt: `${p.name} accepted a $${check.toLocaleString('en-US')} check for a $${price} item and sent the buyer the difference; the check bounced with a $${fee} fee. The same week ${p.pos} debit card was used for $${stolen.toLocaleString('en-US')} and ${p.sub} reported it after five days (limit $500). What is ${p.pos} total loss, not counting the item?`,
      ...numeric(loss), solutionSteps: steps(`Fake check: $${check.toLocaleString('en-US')} − $${price} + $${fee} = ${money(check - price + fee)}.`, `Debit fraud reported after two business days: the smaller of $${stolen.toLocaleString('en-US')} and $500 = ${money(Math.min(stolen, 500))}.`, `Total = ${money(loss)}.`) }; },
    p => { const [check, price, fee, stolen] = dollars(p); return check - price + fee + Math.min(stolen, 500); })
];

/* ---------- Unit 4: Credit Cards & Debt ---------- */
const credit = [
  S(1, 8, 'mo-rate', 'calculation', r => { const p = person(r), b = r.step(200, 2000, 50), m = r.pick([1, 2]); return { prompt: `${p.name}'s card charges ${m}% interest per month. ${p.Sub} owes $${b.toLocaleString('en-US')}. Interest = balance × monthly rate. How much interest is charged this month?`, ...numeric(b * m / 100), solutionSteps: steps(`$${b.toLocaleString('en-US')} × 0.0${m} = ${money(b * m / 100)}.`) }; },
    p => dollars(p)[0] * rates(p)[0]),
  A(1, 12, 'adb-3', 'calculation', r => { const p = person(r), apr = r.pick([0.1999, 0.2299, 0.2499]), b1 = r.step(300, 1200, 5), b2 = b1 + r.step(80, 500, 5), b3 = b2 - r.step(50, 300, 5), d1 = r.int(6, 10), d2 = r.int(8, 12), d3 = 30 - d1 - d2;
    const adb = (b1 * d1 + b2 * d2 + b3 * d3) / 30, it = r2(adb * apr / 365 * 30);
    return { prompt: `In a 30-day cycle ${p.name}'s balance was $${b1.toLocaleString('en-US')} for ${d1} days, $${b2.toLocaleString('en-US')} for ${d2} days, and $${b3.toLocaleString('en-US')} for ${d3} days. The APR is ${pct(apr, 2)}. Using the average daily balance and a daily rate of APR ÷ 365, what is the interest for the cycle?`,
      ...numeric(it, { tolerance: 0.02 }), solutionSteps: steps(`ADB = (${b1}×${d1} + ${b2}×${d2} + ${b3}×${d3}) ÷ 30 = ${money(adb)}.`, `Interest = ${money(adb)} × ${apr} ÷ 365 × 30 = ${money(it)}.`) }; },
    p => { const [b1, b2, b3] = dollars(p), d = [...p.matchAll(/for (\d+) days/g)].map(m => +m[1]), apr = rates(p)[0]; return (b1 * d[0] + b2 * d[1] + b3 * d[2]) / 30 * apr / 365 * 30; }),
  S(2, 8, 'zero-months', 'calculation', r => { const p = person(r), b = r.step(300, 2400, 50), pay = r.pick([50, 75, 100, 150, 200]); return { prompt: `${p.name} owes $${b.toLocaleString('en-US')} on a 0% interest card and pays $${pay} a month. Months = balance ÷ payment, rounded up. How many months to pay it off?`, ...int(Math.ceil(b / pay)), solutionSteps: steps(`$${b.toLocaleString('en-US')} ÷ $${pay} = ${(b / pay).toFixed(2)} → ${Math.ceil(b / pay)} months.`) }; },
    p => { const [b, pay] = dollars(p); return Math.ceil(b / pay); }),
  A(2, 9, 'payoff-payment', 'calculation', r => { const p = person(r), b = r.step(1500, 6000, 100), apr = r.pick([0.1899, 0.2199, 0.2499]), n = r.pick([12, 18, 24, 36]), pay = r2(pmt(b, apr, n));
    return { prompt: `${p.name} wants to pay off ${$0(b)} at ${pct(apr, 2)} APR in ${n} equal monthly payments with no new charges. What is the monthly payment? Use P = B·i ÷ (1 − (1 + i)^−n), with i = APR ÷ 12.`,
      ...numeric(pay, { tolerance: 0.02 }), solutionSteps: steps(`i = ${apr} ÷ 12 = ${(apr / 12).toFixed(6)}.`, `P = ${$0(b)} × i ÷ (1 − (1 + i)^−${n}) = ${money(pay)}.`, `Total paid ${money(pay * n)}; interest ${money(pay * n - b)}.`) }; },
    p => pmt(dollars(p)[0], rates(p)[0], after(p, /in (\d+) equal/))),
  S(3, 9, 'bt-fee', 'calculation', r => { const p = person(r), b = r.step(1000, 6000, 100), f = r.pick([3, 4, 5]); return { prompt: `${p.name} transfers $${b.toLocaleString('en-US')} to a card with a ${f}% transfer fee. Fee = balance × fee rate. What is the fee?`, ...numeric(b * f / 100), solutionSteps: steps(`$${b.toLocaleString('en-US')} × 0.0${f} = ${money(b * f / 100)}.`) }; },
    p => dollars(p)[0] * rates(p)[0]),
  A(3, 10, 'avalanche-first', 'comparison', r => { const p = person(r), a = { b: r.step(400, 900, 50), apr: r.pick([0.2499, 0.2799]) }, b = { b: r.step(1500, 3500, 100), apr: r.pick([0.1499, 0.1799]) }, extra = r.pick([100, 150, 200]);
    const save = r2(extra * (a.apr - b.apr) / 12);
    return { prompt: `${p.name} owes $${a.b} on a store card at ${pct(a.apr, 2)} and $${b.b.toLocaleString('en-US')} on a Visa at ${pct(b.apr, 2)}. ${p.Sub} has $${extra} extra this month. How much more interest does ${p.sub} avoid next month by sending the extra to the higher-APR card instead of the other one?`,
      ...numeric(save), solutionSteps: steps(`Extra on the store card saves $${extra} × ${a.apr} ÷ 12 = ${money(extra * a.apr / 12)}.`, `Extra on the Visa saves $${extra} × ${b.apr} ÷ 12 = ${money(extra * b.apr / 12)}.`, `Difference = ${money(save)} per month, and it keeps growing: that is the avalanche method.`) }; },
    p => { const [, , extra] = dollars(p), [a, b] = rates(p); return extra * (a - b) / 12; }),
  S(4, 4, 'util-basic', 'calculation', r => { const p = person(r), l = r.pick([1000, 2000, 4000, 5000]), b = r.step(100, l * 0.8, 100); return { prompt: `${p.name} has a $${l.toLocaleString('en-US')} credit limit and a $${b.toLocaleString('en-US')} balance. Utilization = balance ÷ limit × 100%. What is ${p.pos} utilization?`, ...numeric(b / l * 100, { unit: '%', d: 0 }), solutionSteps: steps(`$${b.toLocaleString('en-US')} ÷ $${l.toLocaleString('en-US')} = ${(b / l).toFixed(2)} = ${b / l * 100}%.`) }; },
    p => { const [l, b] = dollars(p); return b / l * 100; }),
  A(4, 4, 'cash-adv-cost', 'calculation', r => { const p = person(r), a = r.step(200, 800, 20), apr = r.pick([0.2799, 0.2999]), d = r.pick([20, 35, 50]), fee = Math.max(10, a * 0.05), cost = r2(fee + a * apr / 365 * d);
    return { prompt: `${p.name} takes a $${a} cash advance with a fee of 5% (at least $10) and ${pct(apr, 2)} APR charged daily from day one. ${p.Sub} repays it after ${d} days. What is the total cost of the advance?`,
      ...numeric(cost, { tolerance: 0.02 }), solutionSteps: steps(`Fee = max($10, 5% × $${a}) = ${money(fee)}.`, `Interest = $${a} × ${apr} ÷ 365 × ${d} = ${money(a * apr / 365 * d)}.`, `Total = ${money(cost)}.`) }; },
    p => { const [a] = dollars(p), apr = rates(p)[1], d = after(p, /after (\d+) days/); return Math.max(10, a * 0.05) + a * apr / 365 * d; }),
  S(5, 4, 'drop-off-year', 'concept', r => { const p = person(r), y = r.int(2019, 2026); return { prompt: `A late payment stays on a credit report for about 7 years. ${p.name} missed a payment in ${y}. In what year will it drop off? (Year + 7)`, ...int(y + 7), solutionSteps: steps(`${y} + 7 = ${y + 7}.`, 'Paying on time from now on still helps the score long before then.') }; },
    p => after(p, /payment in (\d{4})/) + 7),
  A(5, 6, 'mortgage-score', 'comparison', r => { const p = person(r), P = r.step(180000, 360000, 5000), good = r.pick([0.0625, 0.065, 0.0675]), fair = r2((good + r.pick([0.0075, 0.01, 0.0125])) * 10000) / 10000;
    const d = r2((pmt(P, fair, 360) - pmt(P, good, 360)) * 360);
    return { prompt: `${p.name} borrows ${$0(P)} for 30 years. With a strong credit score the rate is ${pct(good, 3)}; with a fair score it is ${pct(fair, 3)}. How much more interest does the fair-score loan cost over 30 years? (Payment = P·i ÷ (1 − (1 + i)^−360), i = rate ÷ 12)`,
      ...numeric(d, { tolerance: 2 }), solutionSteps: steps(`Strong: payment ${money(pmt(P, good, 360))}.`, `Fair: payment ${money(pmt(P, fair, 360))}.`, `Difference × 360 = ${money(d)}.`) }; },
    p => { const [P] = dollars(p), [a, b] = rates(p); return (pmt(P, b, 360) - pmt(P, a, 360)) * 360; })
];

/* ---------- Unit 5: Auto Loans & Borrowing ---------- */
const borrowing = [
  S(1, 9, 'total-payments', 'calculation', r => { const p = person(r), pay = r.step(200, 500, 10), n = r.pick([36, 48, 60]); return { prompt: `${p.name}'s car loan payment is $${pay} a month for ${n} months. Total of payments = payment × number of payments. What is the total?`, ...numeric(pay * n), solutionSteps: steps(`$${pay} × ${n} = ${$0(pay * n)}.`) }; },
    p => dollars(p)[0] * after(p, /for (\d+) months/)),
  A(1, 11, 'afford-amount', 'calculation', r => { const p = person(r), pay = r.step(250, 550, 10), apr = r.pick([0.059, 0.069, 0.079]), n = r.pick([48, 60]), i = apr / 12, P = r2(pay * (1 - (1 + i) ** -n) / i);
    return { prompt: `${p.name} can afford $${pay} a month for ${n} months at ${pct(apr)} APR. What is the largest amount ${p.sub} can borrow? Use P = payment × (1 − (1 + i)^−n) ÷ i with i = APR ÷ 12.`,
      ...numeric(P, { tolerance: 0.05 }), solutionSteps: steps(`i = ${apr} ÷ 12 = ${i.toFixed(6)}.`, `P = $${pay} × (1 − (1 + i)^−${n}) ÷ i = ${money(P)}.`, 'Remember taxes, fees and insurance on top of the loan.') }; },
    p => { const [pay] = dollars(p), apr = rates(p)[0], n = after(p, /for (\d+) months/), i = apr / 12; return pay * (1 - (1 + i) ** -n) / i; }),
  S(2, 6, 'monthly-rate', 'calculation', r => { const a = r.pick([6, 9, 12, 18, 24]); return { prompt: `A loan has an APR of ${a}%. Monthly rate = APR ÷ 12. What is the monthly rate?`, ...numeric(a / 12, { unit: '%', d: 2 }), solutionSteps: steps(`${a}% ÷ 12 = ${a / 12}%.`) }; },
    p => rates(p)[0] * 100 / 12),
  A(2, 8, 'offer-total', 'comparison', r => { const p = person(r), P = r.step(15000, 28000, 500), a = { apr: r.pick([0.049, 0.059]), n: 60 }, b = { apr: r.pick([0.029, 0.039]), n: 48, fee: r.pick([400, 600, 800]) };
    const ta = pmt(P, a.apr, 60) * 60, tb = pmt(P, b.apr, 48) * 48 + b.fee, d = r2(Math.abs(ta - tb));
    return { prompt: `${p.name} is financing ${$0(P)}. Lender A: ${pct(a.apr)} APR for 60 months, no fees. Lender B: ${pct(b.apr)} APR for 48 months plus a $${b.fee} loan fee. How much less does the cheaper offer cost in total?`,
      ...numeric(d, { tolerance: 0.1 }), solutionSteps: steps(`A: ${money(pmt(P, a.apr, 60))} × 60 = ${money(ta)}.`, `B: ${money(pmt(P, b.apr, 48))} × 48 + $${b.fee} = ${money(tb)}.`, `Difference = ${money(d)}.`) }; },
    p => { const [P, fee] = dollars(p), [a, b] = rates(p); return Math.abs(pmt(P, a, 60) * 60 - (pmt(P, b, 48) * 48 + fee)); }),
  S(3, 8, 'first-int', 'calculation', r => { const b = r.step(6000, 24000, 1000), m = r.pick([0.005, 0.004, 0.006]); return { prompt: `A loan balance is $${b.toLocaleString('en-US')} and the monthly rate is ${m}. Interest = balance × monthly rate. How much interest is in the first payment?`, ...numeric(b * m), solutionSteps: steps(`$${b.toLocaleString('en-US')} × ${m} = ${money(b * m)}.`) }; },
    p => { const n = nums(p); return n[0] * n[1]; }),
  A(3, 10, 'balance-2', 'calculation', r => { const P = r.step(9000, 26000, 500), apr = r.pick([0.054, 0.066, 0.078]), n = 60, pay = r2(pmt(P, apr, n)), i = apr / 12; let b = P; for (let k = 0; k < 2; k++) b = r2(b + r2(b * i) - pay);
    return { prompt: `A ${$0(P)} car loan at ${pct(apr)} APR has a payment of ${money(pay)}. Build the first two rows of the amortization schedule (round interest to the cent each month). What is the balance after payment 2?`,
      ...numeric(b, { tolerance: 0.02 }), solutionSteps: steps(`Row 1: interest ${money(P * i)}, principal ${money(pay - P * i)}.`, 'Row 2: interest on the new balance, then subtract the principal again.', `Balance after 2 payments = ${money(b)}.`) }; },
    p => { const [P, pay] = dollars(p), i = rates(p)[0] / 12; let b = P; for (let k = 0; k < 2; k++) b = r2(b + r2(b * i) - pay); return b; }),
  S(4, 11, 'cost-down', 'calculation', r => { const p = person(r), dn = r.step(1000, 4000, 500), pay = r.step(220, 480, 10), n = r.pick([36, 48, 60]); return { prompt: `${p.name} pays $${dn.toLocaleString('en-US')} down and $${pay} a month for ${n} months. Total cost = down payment + payment × months. What is the total cost?`, ...numeric(dn + pay * n), solutionSteps: steps(`$${pay} × ${n} = ${$0(pay * n)}.`, `+ $${dn.toLocaleString('en-US')} = ${$0(dn + pay * n)}.`) }; },
    p => { const [dn, pay] = dollars(p); return dn + pay * after(p, /for (\d+) months/); }),
  A(4, 11, 'finance-pct', 'calculation', r => { const P = r.step(12000, 30000, 500), apr = r.pick([0.059, 0.074, 0.089]), n = r.pick([60, 72]), fees = r.pick([300, 495, 650]), fc = pmt(P, apr, n) * n - P + fees, pc = r2(fc / P * 100);
    return { prompt: `A ${$0(P)} loan at ${pct(apr)} APR for ${n} months also has $${fees} in fees. The finance charge is all interest plus fees. What percent of the amount borrowed is the finance charge, to the nearest tenth of a percent?`,
      ...numeric(pc, { unit: '%', d: 1, tolerance: 0.05 }), solutionSteps: steps(`Payment = ${money(pmt(P, apr, n))}; interest = ${money(pmt(P, apr, n) * n - P)}.`, `Finance charge = ${money(fc)}.`, `${money(fc)} ÷ ${$0(P)} = ${pc.toFixed(1)}%.`) }; },
    p => { const [P, fees] = dollars(p), apr = rates(p)[0], n = after(p, /for (\d+) months/); return (pmt(P, apr, n) * n - P + fees) / P * 100; }),
  S(5, 5, 'gas-month', 'calculation', r => { const p = person(r), mi = r.pick([600, 750, 900, 1200]), mpg = r.pick([25, 30]), g = r.pick([3, 4]); return { prompt: `${p.name} drives ${mi} miles a month in a car that gets ${mpg} miles per gallon, with gas at $${g} a gallon. Fuel cost = miles ÷ MPG × price. What is the monthly fuel cost?`, ...numeric(mi / mpg * g), solutionSteps: steps(`${mi} ÷ ${mpg} = ${mi / mpg} gallons.`, `× $${g} = ${money(mi / mpg * g)}.`) }; },
    p => after(p, /drives (\d+) miles/) / after(p, /gets (\d+) miles/) * dollars(p)[0]),
  A(5, 9, 'five-year-tco', 'comparison', r => { const p = person(r), pa = r.step(24000, 32000, 500), pb = pa - r.step(4000, 8000, 500), ra = 0.15, rb = r.pick([0.18, 0.2]), mi = 12000, ma = r.pick([38, 42]), mb = r.pick([24, 26]), gas = r.pick([3.3, 3.6]);
    const ca = pa - pa * (1 - ra) ** 5 + mi / ma * gas * 5, cb = pb - pb * (1 - rb) ** 5 + mi / mb * gas * 5, d = r2(Math.abs(ca - cb));
    return { prompt: `${p.name} compares Car A ($${pa.toLocaleString('en-US')}, loses ${pct(ra, 0)} of its value a year, ${ma} MPG) with Car B ($${pb.toLocaleString('en-US')}, loses ${pct(rb, 0)} a year, ${mb} MPG). Over 5 years of 12,000 miles a year with gas at ${money(gas)}, counting depreciation and fuel only, how much less does the cheaper-to-own car cost?`,
      ...numeric(d, { tolerance: 0.05 }), solutionSteps: steps(`A: depreciation ${money(pa - pa * (1 - ra) ** 5)} + fuel ${money(mi / ma * gas * 5)} = ${money(ca)}.`, `B: depreciation ${money(pb - pb * (1 - rb) ** 5)} + fuel ${money(mi / mb * gas * 5)} = ${money(cb)}.`, `Difference = ${money(d)}: the lower price ${cb < ca ? 'wins' : 'does not win'} here.`) }; },
    p => { const [pa, pb, gas] = dollars(p), [ra, rb] = rates(p), ma = after(p, /a year, (\d+) MPG\) with/), mb = after(p, /a year, (\d+) MPG\)\. Over/); return Math.abs((pa - pa * (1 - ra) ** 5 + 12000 / ma * gas * 5) - (pb - pb * (1 - rb) ** 5 + 12000 / mb * gas * 5)); })
];

/* ---------- Unit 6: Investing ---------- */
const investing = [
  S(1, 7, 'one-year', 'calculation', r => { const p = person(r), P = r.step(500, 8000, 100), g = r.pick([4, 5, 6, 8]); return { prompt: `${p.name} invests $${P.toLocaleString('en-US')} and it grows ${g}% in one year. Growth = amount × rate. How much does it grow?`, ...numeric(P * g / 100), solutionSteps: steps(`$${P.toLocaleString('en-US')} × 0.0${g} = ${money(P * g / 100)}.`) }; },
    p => dollars(p)[0] * rates(p)[0]),
  A(1, 9, 'years-to-target', 'calculation', r => { const p = person(r), P = r.step(2000, 10000, 500), rate = r.pick([0.05, 0.06, 0.07, 0.08]), mult = r.pick([1.5, 2, 2.5, 3]), T = P * mult, y = Math.ceil(Math.log(mult) / Math.log(1 + rate));
    return { prompt: `${p.name} invests ${$0(P)} at ${pct(rate, 0)} compounded annually. After how many whole years will it first reach ${$0(T)}?`,
      ...int(y), solutionSteps: steps(`Solve ${$0(P)}(1 + ${rate})^t ≥ ${$0(T)}: (1.0${rate * 100})^t ≥ ${mult}.`, `t ≥ log(${mult}) ÷ log(${1 + rate}) = ${(Math.log(mult) / Math.log(1 + rate)).toFixed(2)}.`, `So ${y} years.`) }; },
    p => { const [P, T] = dollars(p), rate = rates(p)[0]; return Math.ceil(Math.log(T / P) / Math.log(1 + rate)); }),
  S(2, 8, 'deposits-total', 'calculation', r => { const p = person(r), m = r.pick([25, 50, 75, 100, 200]), y = r.pick([5, 10, 20]); return { prompt: `${p.name} invests $${m} a month for ${y} years. Total deposited = monthly amount × 12 × years. How much does ${p.sub} put in?`, ...numeric(m * 12 * y), solutionSteps: steps(`$${m} × 12 × ${y} = ${$0(m * 12 * y)}.`) }; },
    p => dollars(p)[0] * 12 * after(p, /for (\d+) years/)),
  A(2, 10, 'deposit-for-goal', 'calculation', r => { const p = person(r), goal = r.step(10000, 60000, 1000), rate = r.pick([0.05, 0.06, 0.07]), y = r.pick([5, 8, 10, 15]), i = rate / 12, n = y * 12, d = r2(goal * i / ((1 + i) ** n - 1));
    return { prompt: `${p.name} wants ${$0(goal)} in ${y} years from equal monthly deposits earning ${pct(rate, 0)} compounded monthly. What monthly deposit is needed? Use D = FV·i ÷ ((1 + i)^n − 1), i = rate ÷ 12, n = months.`,
      ...numeric(d, { tolerance: 0.02 }), solutionSteps: steps(`i = ${rate} ÷ 12; n = ${y} × 12 = ${n}.`, `D = ${$0(goal)} × i ÷ ((1 + i)^${n} − 1) = ${money(d)}.`, `Deposits total ${money(d * n)}; the rest is growth.`) }; },
    p => { const [goal] = dollars(p), rate = rates(p)[0], y = after(p, /in (\d+) years/), i = rate / 12, n = y * 12; return goal * i / ((1 + i) ** n - 1); }),
  S(3, 5, 'two-rates', 'comparison', r => { const p = person(r), P = r.step(1000, 9000, 500), a = r.pick([2, 3]), b = r.pick([6, 7, 8]); return { prompt: `${p.name} compares putting $${P.toLocaleString('en-US')} in savings at ${a}% or in a fund that averages ${b}%. Difference after one year = amount × (higher rate − lower rate). How much more does the fund earn in a year?`, ...numeric(P * (b - a) / 100), solutionSteps: steps(`$${P.toLocaleString('en-US')} × (0.0${b} − 0.0${a}) = ${money(P * (b - a) / 100)}.`) }; },
    p => { const [P] = dollars(p), [a, b] = rates(p); return P * (b - a); }),
  A(3, 5, 'start-early', 'comparison', r => { const m = r.pick([100, 150, 200]), rate = r.pick([0.06, 0.07]), y1 = 40, y2 = 30, fa = M.futureValue(0, m, rate, 12, y1), fb = M.futureValue(0, m, rate, 12, y2), d = r2(fa - fb);
    return { prompt: `Two friends each invest $${m} a month at ${pct(rate, 0)} compounded monthly until age 65. One starts at 25 (40 years), the other at 35 (30 years). How much more does the early starter have at 65? Use FV = D·((1 + i)^n − 1) ÷ i.`,
      ...numeric(d, { tolerance: 1 }), solutionSteps: steps(`Start at 25: n = 480, FV = ${money(fa)}.`, `Start at 35: n = 360, FV = ${money(fb)}.`, `Difference = ${money(d)}, though the extra deposits were only $${m * 120}.`) }; },
    p => { const [m] = dollars(p), rate = rates(p)[0], i = rate / 12, fv = n => m * ((1 + i) ** n - 1) / i; return fv(480) - fv(360); }),
  S(4, 4, 'drop-dollars', 'calculation', r => { const p = person(r), v = r.step(2000, 20000, 1000), d = r.pick([10, 15, 20, 25]); return { prompt: `${p.name}'s $${v.toLocaleString('en-US')} investment falls ${d}%. Loss = value × percent drop. How many dollars did it lose?`, ...numeric(v * d / 100), solutionSteps: steps(`$${v.toLocaleString('en-US')} × 0.${d} = ${$0(v * d / 100)}.`) }; },
    p => dollars(p)[0] * rates(p)[0]),
  A(4, 7, 'up-down', 'calculation', r => { const p = person(r), u = r.pick([0.1, 0.2, 0.25, 0.3]), dn = r.pick([0.1, 0.2, 0.25, 0.3]), net = r2(((1 + u) * (1 - dn) - 1) * 100);
    return { prompt: `${p.name}'s fund rises ${pct(u, 0)} one year and falls ${pct(dn, 0)} the next. What is the overall percent change over the two years? (A loss is negative.)`,
      ...numeric(net, { unit: '%', d: 2, tolerance: 0.01 }), solutionSteps: steps(`Multiply the growth factors: ${(1 + u).toFixed(2)} × ${(1 - dn).toFixed(2)} = ${((1 + u) * (1 - dn)).toFixed(4)}.`, `Change = ${net.toFixed(2)}%.`, 'Equal percent gains and losses do not cancel out.') }; },
    p => { const [u, d] = rates(p); return ((1 + u) * (1 - d) - 1) * 100; })
];

/* ---------- Unit 7: Housing ---------- */
const housing = [
  S(1, 10, 'rent-year', 'calculation', r => { const p = person(r), rent = r.step(800, 2200, 25); return { prompt: `${p.name} pays $${rent.toLocaleString('en-US')} a month in rent. Yearly rent = monthly rent × 12. What is the yearly rent?`, ...numeric(rent * 12), solutionSteps: steps(`$${rent.toLocaleString('en-US')} × 12 = ${$0(rent * 12)}.`) }; },
    p => dollars(p)[0] * 12),
  A(1, 14, 'rent-growth', 'calculation', r => { const p = person(r), rent = r.step(900, 2000, 25), g = r.pick([0.03, 0.04, 0.05]), tot = r2((rent + rent * (1 + g) + rent * (1 + g) ** 2) * 12);
    return { prompt: `${p.name}'s rent is $${rent.toLocaleString('en-US')} a month this year and rises ${pct(g, 0)} each year. How much rent will ${p.sub} pay in total over the next 3 years?`,
      ...numeric(tot, { tolerance: 0.05 }), solutionSteps: steps(`Year 1: $${rent.toLocaleString('en-US')} × 12 = ${money(rent * 12)}.`, `Year 2: ${money(rent * (1 + g))} × 12; Year 3: ${money(rent * (1 + g) ** 2)} × 12.`, `Total = ${money(tot)}.`) }; },
    p => { const [rent] = dollars(p), g = rates(p)[0]; return (rent + rent * (1 + g) + rent * (1 + g) ** 2) * 12; }),
  S(2, 4, 'loan-amount', 'calculation', r => { const p = person(r), price = r.step(150000, 400000, 10000), d = r.step(10000, 80000, 5000); return { prompt: `${p.name} buys a $${price.toLocaleString('en-US')} home with a $${d.toLocaleString('en-US')} down payment. Loan = price − down payment. How much does ${p.sub} borrow?`, ...numeric(price - d), solutionSteps: steps(`$${price.toLocaleString('en-US')} − $${d.toLocaleString('en-US')} = ${$0(price - d)}.`) }; },
    p => { const [a, b] = dollars(p); return a - b; }),
  A(2, 6, 'mortgage-interest', 'calculation', r => { const p = person(r), P = r.step(160000, 380000, 5000), rate = r.pick([0.06, 0.065, 0.07]), y = r.pick([15, 30]), n = y * 12, I = r2(pmt(P, rate, n) * n - P);
    return { prompt: `${p.name} takes a ${$0(P)} mortgage at ${pct(rate)} for ${y} years. How much interest will ${p.sub} pay over the whole loan? Use payment = P·i ÷ (1 − (1 + i)^−n), i = rate ÷ 12.`,
      ...numeric(I, { tolerance: 2 }), solutionSteps: steps(`n = ${n}; payment = ${money(pmt(P, rate, n))}.`, `Total paid = ${money(pmt(P, rate, n) * n)}.`, `Interest = ${money(I)}.`) }; },
    p => { const [P] = dollars(p), rate = rates(p)[0], y = after(p, /for (\d+) years/); return pmt(P, rate, y * 12) * y * 12 - P; }),
  S(3, 5, 'tax-month', 'calculation', r => { const t = r.step(1800, 7200, 60); return { prompt: `A home's property tax is $${t.toLocaleString('en-US')} a year. Monthly amount = yearly tax ÷ 12. How much is set aside each month?`, ...numeric(t / 12), solutionSteps: steps(`$${t.toLocaleString('en-US')} ÷ 12 = ${money(t / 12)}.`) }; },
    p => dollars(p)[0] / 12),
  A(3, 9, 'piti-pmi', 'calculation', r => { const p = person(r), price = r.step(220000, 420000, 5000), dp = r.pick([0.05, 0.1]), rate = r.pick([0.065, 0.07]), tx = r.pick([0.011, 0.014]), ins = r.step(1200, 2200, 100), pmiR = 0.007, L = price * (1 - dp);
    const tot = r2(pmt(L, rate, 360) + price * tx / 12 + ins / 12 + L * pmiR / 12);
    return { prompt: `${p.name} buys a ${$0(price)} home with ${pct(dp, 0)} down on a 30-year loan at ${pct(rate)}. Property tax is ${pct(tx)} of the price per year, insurance is $${ins.toLocaleString('en-US')} a year, and PMI is 0.7% of the loan per year because the down payment is under 20%. What is the total monthly payment (PITI + PMI)?`,
      ...numeric(tot, { tolerance: 0.05 }), solutionSteps: steps(`Loan = ${$0(L)}; P&I = ${money(pmt(L, rate, 360))}.`, `Tax ${money(price * tx / 12)}, insurance ${money(ins / 12)}, PMI ${money(L * pmiR / 12)} per month.`, `Total = ${money(tot)}.`) }; },
    p => { const [price, ins] = dollars(p), [dp, rate, tx] = rates(p), L = price * (1 - dp); return pmt(L, rate, 360) + price * tx / 12 + ins / 12 + L * 0.007 / 12; }),
  S(4, 10, 'lost-interest', 'calculation', r => { const p = person(r), d = r.step(10000, 60000, 5000), g = r.pick([3, 4, 5]); return { prompt: `${p.name} uses $${d.toLocaleString('en-US')} of savings for a down payment instead of keeping it in an account earning ${g}%. Lost interest for one year = amount × rate. How much interest does ${p.sub} give up?`, ...numeric(d * g / 100), solutionSteps: steps(`$${d.toLocaleString('en-US')} × 0.0${g} = ${$0(d * g / 100)}.`) }; },
    p => dollars(p)[0] * rates(p)[0]),
  A(4, 7, 'equity-vs-invest', 'comparison', r => { const p = person(r), price = r.step(220000, 400000, 10000), dp = r.pick([0.1, 0.2]), app = r.pick([0.02, 0.03, 0.04]), ret = r.pick([0.05, 0.06, 0.07]);
    const D = price * dp, gainHome = price * ((1 + app) ** 5 - 1), gainInv = D * ((1 + ret) ** 5 - 1), d = r2(Math.abs(gainHome - gainInv));
    return { prompt: `${p.name} puts ${pct(dp, 0)} down on a ${$0(price)} home. Over 5 years the home appreciates ${pct(app, 0)} a year, while the down payment could have earned ${pct(ret, 0)} a year invested. Comparing appreciation on the whole home with growth of the down payment only, how big is the difference after 5 years?`,
      ...numeric(d, { tolerance: 1 }), solutionSteps: steps(`Home gain = ${$0(price)} × (1.0${app * 100}^5 − 1) = ${money(gainHome)}.`, `Investment gain = ${$0(D)} × (1.0${ret * 100}^5 − 1) = ${money(gainInv)}.`, `Difference = ${money(d)}. Leverage lets a small down payment gain on the whole price, though selling costs and repairs reduce it.`) }; },
    p => { const [price] = dollars(p), [dp, app, ret] = rates(p); return Math.abs(price * ((1 + app) ** 5 - 1) - price * dp * ((1 + ret) ** 5 - 1)); }),
  S(5, 4, 'split-3', 'calculation', r => { const p = person(r), rent = r.step(1500, 3300, 150); return { prompt: `${p.name} and two roommates split a $${rent.toLocaleString('en-US')} rent evenly. Each share = rent ÷ 3. What is each person's share?`, ...numeric(rent / 3), solutionSteps: steps(`$${rent.toLocaleString('en-US')} ÷ 3 = ${money(rent / 3)}.`) }; },
    p => dollars(p)[0] / 3),
  A(5, 6, 'two-year-lease', 'calculation', r => { const p = person(r), rent = r.step(950, 1900, 25), g = r.pick([0.03, 0.04, 0.05]), dep = rent, ins = r.pick([12, 15, 18]), tot = r2(rent * 12 + rent * (1 + g) * 12 + ins * 24);
    return { prompt: `${p.name} signs a 12-month lease at $${rent.toLocaleString('en-US')}/month and renews for a second year at a ${pct(g, 0)} increase. Renters insurance is $${ins} a month. The $${dep.toLocaleString('en-US')} deposit is refunded in full. What does ${p.sub} spend on rent and insurance over the two years?`,
      ...numeric(tot), solutionSteps: steps(`Year 1 rent: ${money(rent * 12)}. Year 2: ${money(rent * (1 + g))} × 12 = ${money(rent * (1 + g) * 12)}.`, `Insurance: $${ins} × 24 = ${money(ins * 24)}.`, `Total = ${money(tot)} (the refunded deposit is not a cost).`) }; },
    p => { const [rent, ins] = dollars(p), g = rates(p)[0]; return rent * 12 + rent * (1 + g) * 12 + ins * 24; })
];

/* ---------- Unit 8: Insurance & Risk ---------- */
const insurance = [
  S(1, 4, 'premium-year', 'calculation', r => { const p = person(r), m = r.step(60, 220, 5); return { prompt: `${p.name}'s car insurance costs $${m} a month. Yearly premium = monthly × 12. What is the yearly premium?`, ...numeric(m * 12), solutionSteps: steps(`$${m} × 12 = ${$0(m * 12)}.`) }; },
    p => dollars(p)[0] * 12),
  A(1, 7, 'deductible-breakeven', 'calculation', r => { const p = person(r), lo = r.pick([250, 500]), hi = r.pick([1000, 1500, 2000]), save = r.pick([120, 150, 180, 240]), y = (hi - lo) / save;
    return { prompt: `Raising ${p.name}'s deductible from $${lo} to $${hi.toLocaleString('en-US')} lowers the premium by $${save} a year. How many claim-free years does it take for the premium savings to equal the extra deductible, to the nearest tenth of a year?`,
      ...numeric(Math.round(y * 10) / 10, { unit: 'count', display: String(Math.round(y * 10) / 10), tolerance: 0.05 }), solutionSteps: steps(`Extra deductible = $${hi.toLocaleString('en-US')} − $${lo} = $${hi - lo}.`, `$${hi - lo} ÷ $${save} = ${y.toFixed(2)} years.`, 'If you expect a claim sooner, the lower deductible may be better.') }; },
    p => { const [lo, hi, save] = dollars(p); return Math.round((hi - lo) / save * 10) / 10; }),
  S(2, 6, 'copays', 'calculation', r => { const p = person(r), c = r.pick([20, 25, 30, 40]), v = r.int(2, 8); return { prompt: `${p.name} has ${v} doctor visits this year with a $${c} copay each. Total copays = visits × copay. How much does ${p.sub} pay?`, ...numeric(c * v), solutionSteps: steps(`${v} × $${c} = $${c * v}.`) }; },
    p => after(p, /has (\d+) doctor/) * dollars(p)[0]),
  A(2, 9, 'two-bills-oop', 'calculation', r => { const p = person(r), ded = r.pick([1000, 1500, 2000]), co = r.pick([0.2, 0.3]), max = r.pick([4000, 5000, 6000]), b1 = r.step(800, 3000, 50), b2 = r.step(6000, 30000, 500);
    const pays = (bill, used) => { const d = Math.min(bill, Math.max(0, ded - used.d)); return { d, c: (bill - d) * co }; };
    const one = pays(b1, { d: 0 }), two = pays(b2, { d: one.d }), tot = Math.min(max, one.d + one.c + two.d + two.c);
    return { prompt: `${p.name}'s plan has a $${ded.toLocaleString('en-US')} deductible, ${pct(co, 0)} coinsurance and a $${max.toLocaleString('en-US')} out-of-pocket maximum. ${p.Sub} has a $${b1.toLocaleString('en-US')} bill in March and a $${b2.toLocaleString('en-US')} bill in June. How much does ${p.sub} pay in total for the year?`,
      ...numeric(r2(tot)), solutionSteps: steps(`March: deductible ${money(one.d)} + coinsurance ${money(one.c)}.`, `June: remaining deductible ${money(two.d)} + coinsurance ${money(two.c)}.`, `Total ${money(one.d + one.c + two.d + two.c)}${one.d + one.c + two.d + two.c > max ? `, capped at $${max.toLocaleString('en-US')}` : ''} → ${money(tot)}.`) }; },
    p => { const [ded, max, b1, b2] = dollars(p), co = rates(p)[0]; let used = 0, tot = 0; for (const b of [b1, b2]) { const d = Math.min(b, Math.max(0, ded - used)); used += d; tot += d + (b - d) * co; } return Math.min(max, tot); }),
  S(3, 9, 'ev-one', 'calculation', r => { const pr = r.pick([1, 2, 5, 10]), pay = r.step(1000, 20000, 1000); return { prompt: `There is a ${pr}% chance of a $${pay.toLocaleString('en-US')} loss. Expected loss = probability × amount. What is the expected loss?`, ...numeric(pay * pr / 100), solutionSteps: steps(`0.${String(pr).padStart(2, '0')} × $${pay.toLocaleString('en-US')} = ${money(pay * pr / 100)}.`) }; },
    p => rates(p)[0] * dollars(p)[0]),
  A(3, 6, 'premium-margin', 'calculation', r => { const pr = r.pick([0.01, 0.02, 0.03, 0.05]), loss = r.step(4000, 25000, 500), margin = r.pick([0.2, 0.25, 0.3]), prem = r2(pr * loss * (1 + margin));
    return { prompt: `An insurer covers renters who each have a ${pct(pr, 0)} chance of a $${loss.toLocaleString('en-US')} claim. To cover expected claims plus ${pct(margin, 0)} for costs and profit, what yearly premium should it charge each renter?`,
      ...numeric(prem), solutionSteps: steps(`Expected claim per renter = ${pr} × $${loss.toLocaleString('en-US')} = ${money(pr * loss)}.`, `Add ${pct(margin, 0)}: ${money(pr * loss)} × ${1 + margin} = ${money(prem)}.`) }; },
    p => { const [pr, m] = rates(p); return pr * dollars(p)[0] * (1 + m); }),
  S(4, 11, 'emergency-fund', 'calculation', r => { const p = person(r), e = r.step(1500, 4000, 100), m = r.pick([3, 6]); return { prompt: `${p.name}'s essential expenses are $${e.toLocaleString('en-US')} a month. An emergency fund of ${m} months = monthly expenses × ${m}. How much should ${p.sub} save?`, ...numeric(e * m), solutionSteps: steps(`$${e.toLocaleString('en-US')} × ${m} = ${$0(e * m)}.`) }; },
    p => dollars(p)[0] * after(p, /fund of (\d+) months/)),
  A(4, 11, 'worst-case', 'comparison', r => { const p = person(r), prem = r.step(600, 1500, 50), ded = r.pick([500, 1000, 2500]), loss = r.step(8000, 30000, 1000), d = r2(loss - (prem + ded));
    return { prompt: `${p.name} could buy a policy for $${prem.toLocaleString('en-US')} a year with a $${ded.toLocaleString('en-US')} deductible, or go without. In a bad year with a $${loss.toLocaleString('en-US')} covered loss, how much more would ${p.sub} pay without insurance?`,
      ...numeric(d), solutionSteps: steps(`Insured worst case = premium + deductible = $${prem.toLocaleString('en-US')} + $${ded.toLocaleString('en-US')} = ${$0(prem + ded)}.`, `Uninsured = $${loss.toLocaleString('en-US')}.`, `Difference = ${money(d)}: insurance limits the worst case.`) }; },
    p => { const [prem, ded, loss] = dollars(p); return loss - prem - ded; })
];

/* ---------- Unit 9: College & Careers ---------- */
const college = [
  S(1, 4, 'four-years', 'calculation', r => { const p = person(r), c = r.step(9000, 30000, 500); return { prompt: `College costs ${p.name} $${c.toLocaleString('en-US')} a year. Four-year cost = yearly cost × 4. What is the four-year cost?`, ...numeric(c * 4), solutionSteps: steps(`$${c.toLocaleString('en-US')} × 4 = ${$0(c * 4)}.`) }; },
    p => dollars(p)[0] * 4),
  A(1, 9, 'rising-tuition', 'calculation', r => { const p = person(r), c = r.step(9000, 28000, 500), g = r.pick([0.03, 0.04, 0.05]), tot = r2(c * (1 + (1 + g) + (1 + g) ** 2 + (1 + g) ** 3));
    return { prompt: `${p.name}'s first-year cost is $${c.toLocaleString('en-US')}, and costs rise ${pct(g, 0)} each year. What is the total cost of four years?`,
      ...numeric(tot, { tolerance: 0.05 }), solutionSteps: steps(`Years: $${c.toLocaleString('en-US')}, ${money(c * (1 + g))}, ${money(c * (1 + g) ** 2)}, ${money(c * (1 + g) ** 3)}.`, `Total = ${money(tot)}.`) }; },
    p => { const [c] = dollars(p), g = rates(p)[0]; return c * (1 + (1 + g) + (1 + g) ** 2 + (1 + g) ** 3); }),
  S(2, 7, 'ten-year-total', 'calculation', r => { const p = person(r), pay = r.step(120, 450, 10); return { prompt: `${p.name}'s student loan payment is $${pay} a month for 10 years (120 payments). Total paid = payment × 120. What is the total?`, ...numeric(pay * 120), solutionSteps: steps(`$${pay} × 120 = ${$0(pay * 120)}.`) }; },
    p => dollars(p)[0] * 120),
  A(2, 9, 'capitalized-payment', 'calculation', r => { const p = person(r), P = r.step(15000, 32000, 1000), rate = r.pick([0.0553, 0.0653, 0.0705]), yrs = 4, cap = P + P * rate * yrs, pay = r2(pmt(cap, rate, 120));
    return { prompt: `${p.name} borrows ${$0(P)} in unsubsidized loans at ${pct(rate, 2)}. Interest accrues for 4 years in school and is added to the balance, then ${p.sub} repays over 10 years. What is the monthly payment? (Payment = P·i ÷ (1 − (1 + i)^−120), i = rate ÷ 12.)`,
      ...numeric(pay, { tolerance: 0.02 }), solutionSteps: steps(`Accrued interest = ${$0(P)} × ${rate} × 4 = ${money(P * rate * yrs)}.`, `New balance = ${money(cap)}.`, `Payment = ${money(pay)}.`) }; },
    p => { const [P] = dollars(p), rate = rates(p)[0]; return pmt(P + P * rate * 4, rate, 120); }),
  S(3, 8, 'salary-gap', 'comparison', r => { const a = r.step(32000, 45000, 1000), b = a + r.step(5000, 30000, 1000); return { prompt: `Job A pays $${a.toLocaleString('en-US')} a year and Job B pays $${b.toLocaleString('en-US')}. Difference = higher − lower. How much more does Job B pay each year?`, ...numeric(b - a), solutionSteps: steps(`$${b.toLocaleString('en-US')} − $${a.toLocaleString('en-US')} = ${$0(b - a)}.`) }; },
    p => { const [a, b] = dollars(p); return b - a; }),
  A(3, 10, 'raises-sum', 'calculation', r => { const s = r.step(42000, 70000, 1000), g = r.pick([0.02, 0.03, 0.04]), tot = r2(s * ((1 + g) ** 10 - 1) / g);
    return { prompt: `A job starts at $${s.toLocaleString('en-US')} and gives a ${pct(g, 0)} raise every year. What are total earnings over the first 10 years? Use total = S·((1 + g)^10 − 1) ÷ g.`,
      ...numeric(tot, { tolerance: 1 }), solutionSteps: steps(`Year 1: $${s.toLocaleString('en-US')}; year 10: ${money(s * (1 + g) ** 9)}.`, `Sum = $${s.toLocaleString('en-US')} × ((1.0${g * 100})^10 − 1) ÷ ${g} = ${money(tot)}.`) }; },
    p => { const [s] = dollars(p), g = rates(p)[0]; return s * ((1 + g) ** 10 - 1) / g; }),
  S(4, 12, 'payback-whole', 'calculation', r => { const g = r.step(2000, 10000, 1000), y = r.int(2, 8); return { prompt: `A training program costs $${(g * y).toLocaleString('en-US')} and raises earnings by $${g.toLocaleString('en-US')} a year. Payback = cost ÷ yearly gain. How many years until it pays for itself?`, ...int(y), solutionSteps: steps(`$${(g * y).toLocaleString('en-US')} ÷ $${g.toLocaleString('en-US')} = ${y} years.`) }; },
    p => { const [c, g] = dollars(p); return c / g; }),
  A(4, 9, 'payback-forgone', 'calculation', r => { const cost = r.step(20000, 80000, 1000), yrs = r.pick([2, 4]), wage = r.step(24000, 34000, 1000), gain = r.step(12000, 28000, 1000), y = (cost + wage * yrs) / gain;
    return { prompt: `A ${yrs}-year program costs $${cost.toLocaleString('en-US')} in total. While in school a student gives up a job paying $${wage.toLocaleString('en-US')} a year. Afterward earnings rise by $${gain.toLocaleString('en-US')} a year. Counting the lost wages, how many years after graduating until the program pays off, to the nearest tenth?`,
      ...numeric(Math.round(y * 10) / 10, { unit: 'count', display: String(Math.round(y * 10) / 10), tolerance: 0.05 }), solutionSteps: steps(`Lost wages = $${wage.toLocaleString('en-US')} × ${yrs} = ${$0(wage * yrs)}.`, `Total cost = ${$0(cost + wage * yrs)}.`, `÷ $${gain.toLocaleString('en-US')} = ${y.toFixed(2)} years.`) }; },
    p => { const [cost, wage, gain] = dollars(p), yrs = after(p, /A (\d)-year program/); return Math.round((cost + wage * yrs) / gain * 10) / 10; })
];

/* ---------- Unit 10: Retirement & Inflation ---------- */
const retirement = [
  S(1, 8, 'next-year-price', 'calculation', r => { const item = r.pick(['A sandwich', 'A bus pass', 'A haircut', 'A video game']), pr = r.pick([10, 20, 40, 60, 80, 100]), i = r.pick([2, 3, 5]); return { prompt: `${item} costs $${pr} today. With ${i}% inflation, next year's price = price × (1 + rate). What will it cost next year?`, ...numeric(pr * (1 + i / 100)), solutionSteps: steps(`$${pr} × 1.0${i} = ${money(pr * (1 + i / 100))}.`) }; },
    p => dollars(p)[0] * (1 + rates(p)[0])),
  A(1, 9, 'years-to-multiply', 'calculation', r => { const i = r.pick([0.02, 0.025, 0.03, 0.035, 0.04]), [word, k] = r.pick([['double', 2], ['rise by half', 1.5], ['triple', 3]]), y = Math.log(k) / Math.log(1 + i);
    return { prompt: `If inflation averages ${pct(i)} a year, how many years until prices ${word} (multiply by ${k}), to the nearest tenth of a year? Solve (1 + rate)^t = ${k}.`,
      ...numeric(Math.round(y * 10) / 10, { unit: 'count', display: String(Math.round(y * 10) / 10), tolerance: 0.05 }), solutionSteps: steps(`t = log ${k} ÷ log(${1 + i}) = ${y.toFixed(2)}.`, k === 2 ? `Rule of 72 check: 72 ÷ ${i * 100} = ${(72 / (i * 100)).toFixed(1)}.` : 'Each extra year multiplies prices by the same factor.') }; },
    p => { const k = after(p, /multiply by ([\d.]+)\)/); return Math.round(Math.log(k) / Math.log(1 + rates(p)[0]) * 10) / 10; }),
  S(2, 10, 'contrib-total', 'calculation', r => { const p = person(r), a = r.step(1000, 8000, 500), y = r.pick([10, 20, 30, 40]); return { prompt: `${p.name} contributes $${a.toLocaleString('en-US')} a year for ${y} years. Total contributed = yearly amount × years. How much does ${p.sub} put in?`, ...numeric(a * y), solutionSteps: steps(`$${a.toLocaleString('en-US')} × ${y} = ${$0(a * y)}.`) }; },
    p => dollars(p)[0] * after(p, /for (\d+) years/)),
  A(2, 8, 'match-fv', 'calculation', r => { const p = person(r), sal = r.step(40000, 80000, 1000), c = 0.06, mr = 0.5, rate = r.pick([0.06, 0.07]), y = r.pick([20, 30]), mo = sal * c / 12 * (1 + mr), i = rate / 12, fv = r2(mo * ((1 + i) ** (y * 12) - 1) / i);
    return { prompt: `${p.name} earns $${sal.toLocaleString('en-US')} and contributes 6% of pay monthly; the employer adds 50% of that. Ignoring raises, what will the account hold after ${y} years at ${pct(rate, 0)} compounded monthly? Use FV = D·((1 + i)^n − 1) ÷ i.`,
      ...numeric(fv, { tolerance: 1 }), solutionSteps: steps(`Monthly deposit = $${sal.toLocaleString('en-US')} × 0.06 ÷ 12 × 1.5 = ${money(mo)}.`, `n = ${y * 12}, i = ${rate} ÷ 12.`, `FV = ${money(fv)}.`) }; },
    p => { const [sal] = dollars(p), rate = rates(p)[2], y = after(p, /after (\d+) years/), mo = sal * 0.06 / 12 * 1.5, i = rate / 12; return mo * ((1 + i) ** (y * 12) - 1) / i; }),
  S(3, 5, 'contrib-pct', 'calculation', r => { const p = person(r), sal = r.step(30000, 90000, 1000), c = r.pick([3, 4, 5, 6, 10]); return { prompt: `${p.name} earns $${sal.toLocaleString('en-US')} and contributes ${c}% to a 401(k). Contribution = salary × percent. How much does ${p.sub} contribute in a year?`, ...numeric(sal * c / 100), solutionSteps: steps(`$${sal.toLocaleString('en-US')} × 0.${String(c).padStart(2, '0')} = ${$0(sal * c / 100)}.`) }; },
    p => dollars(p)[0] * rates(p)[0]),
  A(3, 10, 'pretax-savings', 'calculation', r => { const p = person(r), gross = r.step(55000, 120000, 1000), c = r.pick([0.05, 0.08, 0.1]), sd = TAX_2026.standardDeduction.single, save = r2(tax2026(gross - sd) - tax2026(gross - gross * c - sd));
    return { prompt: `${p.name} earns ${$0(gross)} in 2026 and takes the $16,100 standard deduction. How much federal income tax does ${p.sub} save by putting ${pct(c, 0)} of pay into a traditional 401(k)? Brackets: 10% to $12,400; 12% to $50,400; 22% to $105,700; 24% to $201,775.`,
      ...numeric(save), solutionSteps: steps(`Without: tax on ${$0(gross - sd)} = ${money(tax2026(gross - sd))}.`, `With: tax on ${$0(gross - gross * c - sd)} = ${money(tax2026(gross - gross * c - sd))}.`, `Savings = ${money(save)}.`) }; },
    p => { const [gross, sd] = dollars(p), c = rates(p)[0]; return tax2026(gross - sd) - tax2026(gross - gross * c - sd); }),
  S(4, 7, 'worth-next-year', 'calculation', r => { const a = r.pick([100, 500, 1000, 2000]), i = r.pick([2, 4, 5]); return { prompt: `With ${i}% inflation, $${a.toLocaleString('en-US')} a year from now buys what today's amount ÷ (1 + rate) buys. What is it worth in today's dollars?`, ...numeric(a / (1 + i / 100)), solutionSteps: steps(`$${a.toLocaleString('en-US')} ÷ 1.0${i} = ${money(a / (1 + i / 100))}.`) }; },
    p => dollars(p)[0] / (1 + rates(p)[0])),
  A(4, 10, 'nominal-needed', 'calculation', r => { const real = r.pick([0.03, 0.04, 0.05]), i = r.pick([0.02, 0.025, 0.03, 0.035]), n = r2(((1 + real) * (1 + i) - 1) * 100);
    return { prompt: `To grow purchasing power by ${pct(real, 0)} a year when inflation is ${pct(i)}, what nominal return is needed, to the nearest hundredth of a percent? Use (1 + nominal) = (1 + real)(1 + inflation).`,
      ...numeric(n, { unit: '%', d: 2, tolerance: 0.01 }), solutionSteps: steps(`(1 + ${real})(1 + ${i}) = ${((1 + real) * (1 + i)).toFixed(5)}.`, `Nominal = ${n.toFixed(2)}%. Adding the rates gives ${pct(real + i)}, slightly low.`) }; },
    p => { const [real, i] = rates(p); return ((1 + real) * (1 + i) - 1) * 100; })
];

export const levelFamilies = { income, budgeting, banking, credit, borrowing, investing, housing, insurance, college, retirement };
