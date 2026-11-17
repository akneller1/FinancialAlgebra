/* Algebra modeling with graphs (2026-11-17). One family per unit, three questions per level:
 *   linear cost functions, piecewise tax brackets, compound growth curves, break-even points and where two
 *   options cross (bank accounts, loan offers, rent vs buy, health plans, college vs work).
 * Every question carries a graph (scenario.graph, drawn as SVG by lib/render.js) and a caption with the model,
 * so it can be answered from the text too. Worked solutions show the formula, the substitution, a spreadsheet
 * entry and what the answer means. verify(q) re-reads numbers from the prompt, caption and marked points (not the
 * generator's variables) and recomputes the answer; tests/fa-modeling.test.mjs runs it on every question. */
import { M, money, $0, pct, person, numeric } from './kit.mjs';
import { TAX_2026 } from './real-data-2026.mjs';

const r2 = M.round2, LV = ['support', 'standard', 'advanced'];
const dollars = (s) => [...String(s).matchAll(/\$([\d,]+(?:\.\d+)?)/g)].map(m => Number(m[1].replace(/,/g, '')));
const rates = (s) => [...String(s).matchAll(/([\d.]+)%/g)].map(m => Number(m[1]) / 100);
const after = (s, re) => Number(String(s).match(re)[1].replace(/,/g, ''));
const cap = (q) => q.scenario.graph.caption;
const int = (v) => numeric(v, { unit: 'count', display: String(v) });
const nice = (v) => { const e = 10 ** Math.floor(Math.log10(v)), f = v / e; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * e; };
/* Build a graph by sampling functions. */
function graph({ title, xl, xmax, xstep, yl, series, marks, caption, ymin = 0, xmoney = false, n = 60 }) {
  const ss = series.map(s => ({ name: s.name, pts: Array.from({ length: n + 1 }, (_, i) => { const x = xmax * i / n; return [r2(x), r2(s.f(x))]; }) }));
  const ys = ss.flatMap(s => s.pts.map(p => p[1])).concat((marks || []).map(m => m.y));
  const hi = Math.max(...ys), mn = Math.min(...ys, 0), step = nice((hi - mn) / 5), lo = ymin < 0 ? Math.floor(mn / step) * step : 0;
  return { title, x: { label: xl, min: 0, max: xmax, step: xstep, money: xmoney }, y: { label: yl, min: lo, max: Math.ceil(hi / step - 1e-9) * step, step, money: true }, series: ss, marks: marks || [], caption };
}
const F = (unit, skill, id, gen, verify) => ({ unit, fam: { id: 'lv-m-' + id, skill, type: 'modeling', count: 9, game: false, activities: ['worksheet', 'assessment', 'lesson', 'practice-test'], gen, verify } });
const tax = (x) => { let t = 0, lo = 0; for (const b of TAX_2026.bracketsSingle) { if (x <= lo) break; t += (Math.min(x, b.upTo) - lo) * b.rate; lo = b.upTo; } return t; };

const fams = [
  /* ---------- Income: tax brackets as a piecewise function ---------- */
  F('income', 4, 'tax-piecewise', (r, k) => { const p = person(r), level = LV[k % 3];
    const caption = 'T(x) = 0.10x for x ≤ $12,400; T(x) = $1,240 + 0.12(x − $12,400) for $12,400 < x ≤ $50,400; T(x) = $5,800 + 0.22(x − $50,400) for $50,400 < x ≤ $105,700. (2026 federal brackets, single filer.)';
    const g = graph({ title: '2026 federal income tax, single filer', xl: 'Taxable income x', xmax: 100000, xstep: 20000, xmoney: true, yl: 'Tax T(x)', series: [{ name: 'T(x)', f: tax }], marks: [{ x: 12400, y: 1240, label: '($12,400, $1,240)' }, { x: 50400, y: 5800, label: '($50,400, $5,800)' }], caption });
    if (level === 'support') { const x = r.pick([r.step(3000, 12000, 500), r.step(14000, 50000, 500), r.step(52000, 99000, 500)]), rate = x <= 12400 ? 10 : x <= 50400 ? 12 : 22;
      return { level, prompt: `The graph shows tax as a piecewise function of taxable income. ${p.name} has $${x.toLocaleString('en-US')} of taxable income. What is the slope of the graph at that income, as a percent? (That slope is ${p.pos} marginal tax rate.)`, scenario: { graph: g },
        ...numeric(rate, { unit: '%', d: 0, tolerance: 0 }), solutionSteps: [`Formula: on each piece, slope = rise ÷ run = tax rate for that bracket.`, `$${x.toLocaleString('en-US')} is in the piece ${x <= 12400 ? 'up to $12,400' : x <= 50400 ? 'from $12,400 to $50,400' : 'from $50,400 to $105,700'}, where T(x) has slope ${rate / 100}.`, `Spreadsheet: =IF(${x}<=12400,10%,IF(${x}<=50400,12%,22%)) → ${rate}%.`, `So each extra dollar ${p.name} earns is taxed ${rate}¢; the earlier dollars keep their lower rates.`] }; }
    if (level === 'standard') { const x = r.step(14000, 99000, 100), t = r2(tax(x));
      return { level, prompt: `Use the piecewise function T(x) in the caption. What is the federal tax on $${x.toLocaleString('en-US')} of taxable income?`, scenario: { graph: g }, ...numeric(t),
        solutionSteps: [`Formula: ${x <= 50400 ? 'T(x) = $1,240 + 0.12(x − $12,400)' : 'T(x) = $5,800 + 0.22(x − $50,400)'} for this piece.`, `Substitute: ${x <= 50400 ? `$1,240 + 0.12($${x.toLocaleString('en-US')} − $12,400) = $1,240 + ${money(0.12 * (x - 12400))}` : `$5,800 + 0.22($${x.toLocaleString('en-US')} − $50,400) = $5,800 + ${money(0.22 * (x - 50400))}`} = ${money(t)}.`, `Spreadsheet: ${x <= 50400 ? `=1240+0.12*(${x}-12400)` : `=5800+0.22*(${x}-50400)`}.`, `So the tax is ${money(t)}, about ${(t / x * 100).toFixed(1)}% of taxable income, well below the top rate of the piece.`] }; }
    const t = r.step(2000, 15000, 5), x = r2(t <= 5800 ? 12400 + (t - 1240) / 0.12 : 50400 + (t - 5800) / 0.22);
    return { level, prompt: `${p.name}'s federal tax was $${t.toLocaleString('en-US')}. Using T(x) in the caption, what was ${p.pos} taxable income? Round to the nearest dollar.`, scenario: { graph: g }, ...numeric(Math.round(x), { tolerance: 1 }),
      solutionSteps: [`Formula: find the piece first. T($50,400) = $5,800, so $${t.toLocaleString('en-US')} is on the ${t <= 5800 ? '12%' : '22%'} piece.`, t <= 5800 ? `Solve $1,240 + 0.12(x − $12,400) = $${t.toLocaleString('en-US')}: x = $12,400 + [[$${t.toLocaleString('en-US')} − $1,240 || 0.12]] = ${money(x)}.` : `Solve $5,800 + 0.22(x − $50,400) = $${t.toLocaleString('en-US')}: x = $50,400 + [[$${t.toLocaleString('en-US')} − $5,800 || 0.22]] = ${money(x)}.`, `Spreadsheet: ${t <= 5800 ? `=12400+(${t}-1240)/0.12` : `=50400+(${t}-5800)/0.22`}.`, `So ${p.name} had about ${$0(x)} of taxable income. Working backward through a piecewise function means finding the right piece first.`] }; },
    (q) => { if (q.level === 'support') { const x = dollars(q.prompt)[0]; return x <= 12400 ? 10 : x <= 50400 ? 12 : 22; } if (q.level === 'standard') return tax(dollars(q.prompt)[0]); const t = dollars(q.prompt)[0]; return t <= 5800 ? 12400 + (t - 1240) / 0.12 : 50400 + (t - 5800) / 0.22; }),

  /* ---------- Budgeting: a linear cost function ---------- */
  F('budgeting', 3, 'linear-cost', (r, k) => { const p = person(r), level = LV[k % 3];
    const ctx = r.pick([{ what: 'phone plan', u: 'gigabytes of data', s: 'GB', F: r.step(15, 35, 5), m: r.pick([2, 3, 4, 5]) }, { what: 'tutoring service', u: 'hours of tutoring', s: 'hour', F: r.step(20, 40, 5), m: r.pick([12, 15, 18, 20]) }, { what: 'bike-share membership', u: 'rides', s: 'ride', F: r.step(10, 25, 5), m: r.pick([1.5, 2, 2.5]) }]);
    const c = (x) => ctx.F + ctx.m * x, x1 = 2, x2 = r.pick([6, 8, 10]);
    const g = graph({ title: `Monthly cost of a ${ctx.what}`, xl: ctx.u.replace(/^./, s => s.toUpperCase()) + ' per month, x', xmax: 12, xstep: 2, yl: 'Monthly cost C(x)', series: [{ name: 'C(x)', f: c }], marks: [{ x: x1, y: c(x1), label: `(${x1}, ${money(c(x1))})` }, { x: x2, y: c(x2), label: `(${x2}, ${money(c(x2))})` }],
      caption: level === 'standard' ? 'The cost is a linear function: a flat monthly fee plus a fixed price for each unit.' : `C(x) = ${money(ctx.F)} + ${money(ctx.m)}x` });
    if (level === 'support') { const x = r.pick([3, 5, 7, 9, 11]), v = c(x);
      return { level, prompt: `The ${ctx.what} costs C(x) = ${money(ctx.F)} + ${money(ctx.m)}x a month, where x is the number of ${ctx.u}. What does ${p.name} pay in a month with ${x} ${x === 1 ? ctx.s : ctx.u}?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: [`Formula: C(x) = fixed fee + price per ${ctx.s} × x.`, `Substitute: ${money(ctx.F)} + ${money(ctx.m)} × ${x} = ${money(v)}.`, `Spreadsheet: =${ctx.F}+${ctx.m}*${x}.`, `So ${p.name}'s bill is ${money(v)}; the point (${x}, ${money(v)}) is on the line.`] }; }
    if (level === 'standard') { const sl = r2((c(x2) - c(x1)) / (x2 - x1));
      return { level, prompt: `Use the two marked points on the graph of the ${ctx.what}'s monthly cost. What is the slope of the line, the price per ${ctx.s}?`, scenario: { graph: g }, ...numeric(sl),
        solutionSteps: [`Formula: slope m = [[C₂ − C₁ || x₂ − x₁]].`, `Substitute: [[${money(c(x2))} − ${money(c(x1))} || ${x2} − ${x1}]] = ${money(c(x2) - c(x1))} ÷ ${x2 - x1} = ${money(sl)}.`, `Spreadsheet: =SLOPE({${money(c(x1)).slice(1)},${money(c(x2)).slice(1)}},{${x1},${x2}}) or =(${r2(c(x2))}-${r2(c(x1))})/(${x2}-${x1}).`, `So every extra ${ctx.s} adds ${money(sl)} to the bill; the y-intercept, ${money(ctx.F)}, is the fee paid even with 0 ${ctx.u}.`] }; }
    const B = Math.round(ctx.F + ctx.m * r.int(4, 11) + r.pick([0, 0.4, 0.7]) * ctx.m), x = Math.floor((B - ctx.F) / ctx.m + 1e-9);
    return { level, prompt: `${p.name} budgets $${B} a month for the ${ctx.what}, which costs C(x) = ${money(ctx.F)} + ${money(ctx.m)}x. What is the greatest whole number of ${ctx.u} ${p.sub} can use and stay within budget?`, scenario: { graph: g }, ...int(x),
      solutionSteps: [`Formula: solve C(x) ≤ budget: ${money(ctx.F)} + ${money(ctx.m)}x ≤ $${B}.`, `Substitute: x ≤ [[$${B} − ${money(ctx.F)} || ${money(ctx.m)}]] = ${((B - ctx.F) / ctx.m).toFixed(2)}.`, `Spreadsheet: =ROUNDDOWN((${B}-${ctx.F})/${ctx.m},0).`, `So ${p.name} can use ${x} ${ctx.u}; one more would cost ${money(c(x + 1))}, over the $${B} budget. On the graph, it is the last whole x where the line is at or below $${B}.`] }; },
    (q) => { const c = cap(q); if (q.level === 'standard') { const pts = q.scenario.graph.marks.map(m => [Number(m.label.match(/\((\d+),/)[1]), dollars(m.label)[0]]); return (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0]); } const [Fx, m] = dollars(c); if (q.level === 'support') return Fx + m * after(q.prompt, /with (\d+) /); const B = dollars(q.prompt)[0]; return Math.floor((B - Fx) / m + 1e-9); }),

  /* ---------- Banking: two accounts' fees cross ---------- */
  F('banking', 1, 'fee-lines', (r, k) => { const p = person(r), level = LV[k % 3], c1 = r.pick([0.5, 1, 1.5]), gap = r.pick([1.5, 2, 2.5, 3]), c2 = c1 + gap, a = gap * r.int(2, 6);
    const A = (x) => a + c1 * x, B = (x) => c2 * x, xs = a / gap;
    const g = graph({ title: 'Monthly cost of two checking accounts', xl: 'Out-of-network ATM withdrawals per month, x', xmax: 12, xstep: 2, yl: 'Monthly cost', series: [{ name: `Account A: A(x) = ${money(a)} + ${money(c1)}x`, f: A }, { name: `Account B: B(x) = ${money(c2)}x`, f: B }], marks: [{ x: xs, y: A(xs), label: 'A = B' }], caption: `Account A: A(x) = ${money(a)} + ${money(c1)}x. Account B: B(x) = ${money(c2)}x.` });
    if (level === 'support') { const x = r.int(2, 11), v = A(x);
      return { level, prompt: `Account A charges ${money(a)} a month plus ${money(c1)} per out-of-network ATM withdrawal. What does it cost ${p.name} in a month with ${x} withdrawals?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: A(x) = monthly fee + fee per withdrawal × x.', `Substitute: ${money(a)} + ${money(c1)} × ${x} = ${money(v)}.`, `Spreadsheet: =${a}+${c1}*${x}.`, `So Account A costs ${money(v)} that month${v > B(x) ? `, more than Account B's ${money(B(x))}` : v < B(x) ? `, less than Account B's ${money(B(x))}` : ', the same as Account B'}.`] }; }
    if (level === 'standard') return { level, prompt: `For how many withdrawals a month do the two accounts cost the same? (Where the lines cross.)`, scenario: { graph: g }, ...int(xs),
      solutionSteps: ['Formula: set A(x) = B(x).', `Substitute: ${money(a)} + ${money(c1)}x = ${money(c2)}x → ${money(a)} = ${money(gap)}x → x = ${money(a)} ÷ ${money(gap)} = ${xs}.`, `Spreadsheet: =${a}/(${c2}-${c1}).`, `So at ${xs} withdrawals both cost ${money(A(xs))}. Fewer withdrawals: Account B is cheaper. More: Account A is cheaper.`] };
    const x = r.pick([r.int(1, Math.max(1, xs - 1)), r.int(xs + 1, 12)]), d = r2(Math.abs(A(x) - B(x)) * 12);
    return { level, prompt: `${p.name} makes ${x} out-of-network withdrawals every month. Over a year, how much less does the cheaper account cost?`, scenario: { graph: g }, ...numeric(d),
      solutionSteps: [`Formula: yearly difference = 12 × |A(x) − B(x)|.`, `Substitute: A(${x}) = ${money(A(x))}, B(${x}) = ${money(B(x))}; 12 × ${money(Math.abs(A(x) - B(x)))} = ${money(d)}.`, `Spreadsheet: =12*ABS((${a}+${c1}*${x})-${c2}*${x}).`, `So Account ${A(x) < B(x) ? 'A' : 'B'} saves ${p.name} ${money(d)} a year: ${x} is ${x > xs ? 'right' : 'left'} of the crossing point at ${xs}.`] }; },
    (q) => { const [a, c1, c2] = dollars(cap(q)); if (q.level === 'standard') return a / (c2 - c1); if (q.level === 'support') return a + c1 * after(q.prompt, /with (\d+) withdrawals/); const x = after(q.prompt, /makes (\d+) /); return 12 * Math.abs(a + c1 * x - c2 * x); }),

  /* ---------- Credit: interest as a linear function of the balance ---------- */
  F('credit', 1, 'interest-lines', (r, k) => { const p = person(r), level = LV[k % 3], a1 = r.pick([0.18, 0.1999, 0.2149]), a2 = r.pick([0.2499, 0.2799, 0.2999]);
    const g = graph({ title: 'Monthly interest on a credit card balance', xl: 'Balance B', xmax: 5000, xstep: 1000, xmoney: true, yl: 'Monthly interest I(B)', series: [{ name: `Card A, APR ${pct(a1, 2)}`, f: b => b * a1 / 12 }, { name: `Card B, APR ${pct(a2, 2)}`, f: b => b * a2 / 12 }], caption: `I(B) = (APR ÷ 12) × B. Card A: APR ${pct(a1, 2)}. Card B: APR ${pct(a2, 2)}.` });
    if (level === 'support') { const b = r.step(500, 4800, 50), v = r2(b * a1 / 12);
      return { level, prompt: `${p.name} carries a $${b.toLocaleString('en-US')} balance on Card A. Using I(B) = (APR ÷ 12) × B, what is one month's interest?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: I = (APR ÷ 12) × B.', `Substitute: (${a1} ÷ 12) × $${b.toLocaleString('en-US')} = ${money(v)}.`, `Spreadsheet: =${a1}/12*${b}.`, `So carrying the balance costs ${money(v)} this month, about ${money(v * 12)} over a year if nothing changes.`] }; }
    if (level === 'standard') { const b = r.step(1000, 5000, 100), d = r2(b * (a2 - a1) / 12);
      return { level, prompt: `On a $${b.toLocaleString('en-US')} balance, how much more interest does Card B charge in a month than Card A? (The vertical gap between the lines.)`, scenario: { graph: g }, ...numeric(d),
        solutionSteps: ['Formula: gap = (APR_B − APR_A) ÷ 12 × B.', `Substitute: [[${a2} − ${a1} || 12]] × $${b.toLocaleString('en-US')} = ${money(d)}.`, `Spreadsheet: =(${a2}-${a1})/12*${b}.`, `So Card B costs ${money(d)} more each month on this balance. The gap grows with the balance because the lines have different slopes.`] }; }
    const t = r.step(25, 100, 5), b = r2(t / (a2 / 12));
    return { level, prompt: `What Card B balance makes the monthly interest exactly $${t}? Round to the nearest cent.`, scenario: { graph: g }, ...numeric(b, { tolerance: 0.01 }),
      solutionSteps: ['Formula: solve (APR ÷ 12) × B = I for B: B = [[I || APR ÷ 12]].', `Substitute: B = [[$${t} || ${a2} ÷ 12]] = ${money(b)}.`, `Spreadsheet: =${t}/(${a2}/12).`, `So a balance of about ${$0(b)} on Card B costs $${t} a month in interest, ${money(t * 12)} a year, before paying down any of the balance.`] }; },
    (q) => { const [a1, a2] = rates(cap(q)); if (q.level === 'support') return dollars(q.prompt)[0] * a1 / 12; if (q.level === 'standard') return dollars(q.prompt)[0] * (a2 - a1) / 12; return dollars(q.prompt)[0] / (a2 / 12); }),

  /* ---------- Borrowing: where two loan offers cross ---------- */
  F('borrowing', 2, 'offers-cross', (r, k) => { const p = person(r), level = LV[k % 3], pA = r.step(280, 420, 1), gap = r.pick([8, 10, 12, 15, 20]), pB = pA + gap, f = gap * r.int(12, 40), n = r.pick([48, 60]);
    const A = (m) => f + pA * m, B = (m) => pB * m, ms = f / gap;
    const g = graph({ title: 'Total paid on two loan offers', xl: 'Months, m', xmax: n, xstep: 12, yl: 'Total paid', series: [{ name: `Offer A: A(m) = ${money(f)} + ${money(pA)}m`, f: A }, { name: `Offer B: B(m) = ${money(pB)}m`, f: B }], marks: [{ x: ms, y: A(ms), label: 'A = B' }], caption: `Offer A: ${money(f)} origination fee and ${money(pA)} a month. Offer B: no fee and ${money(pB)} a month. Both last ${n} months.` });
    if (level === 'support') { const m = r.int(6, n), v = A(m);
      return { level, prompt: `Using Offer A's model A(m) = ${money(f)} + ${money(pA)}m, how much has ${p.name} paid after ${m} months?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: A(m) = fee + payment × m.', `Substitute: ${money(f)} + ${money(pA)} × ${m} = ${money(v)}.`, `Spreadsheet: =${f}+${pA}*${m}.`, `So after ${m} months Offer A has cost ${money(v)}, against ${money(B(m))} for Offer B.`] }; }
    if (level === 'standard') return { level, prompt: `After how many months have the two offers cost the same total? (Where the lines cross.)`, scenario: { graph: g }, ...int(ms),
      solutionSteps: ['Formula: set A(m) = B(m): fee + p_A·m = p_B·m, so m = [[fee || p_B − p_A]].', `Substitute: m = [[${money(f)} || ${money(pB)} − ${money(pA)}]] = ${money(f)} ÷ ${money(gap)} = ${ms}.`, `Spreadsheet: =${f}/(${pB}-${pA}).`, `So the fee is "paid back" by the lower payment after ${ms} months. If the loan runs longer than that, Offer A costs less overall.`] };
    const d = r2(Math.abs(A(n) - B(n)));
    return { level, prompt: `Both loans run the full ${n} months. How much less does the cheaper offer cost in total?`, scenario: { graph: g }, ...numeric(d),
      solutionSteps: ['Formula: difference = |A(n) − B(n)|.', `Substitute: A(${n}) = ${money(f)} + ${money(pA)} × ${n} = ${money(A(n))}; B(${n}) = ${money(pB)} × ${n} = ${money(B(n))}.`, `Spreadsheet: =ABS((${f}+${pA}*${n})-${pB}*${n}).`, `So Offer ${A(n) < B(n) ? 'A' : 'B'} saves ${money(d)}: the lines cross at month ${ms}, ${ms < n ? 'before' : 'after'} the loan ends.`] }; },
    (q) => { const c = cap(q), [f, pA, pB] = dollars(c), n = after(c, /last (\d+) months/); if (q.level === 'standard') return f / (pB - pA); if (q.level === 'support') return f + pA * after(q.prompt, /after (\d+) months/); return Math.abs(f + pA * n - pB * n); }),

  /* ---------- Investing: compound growth curves ---------- */
  F('investing', 1, 'growth-curves', (r, k) => { const p = person(r), level = LV[k % 3], P = r.step(1000, 10000, 500), a = r.pick([0.03, 0.04]), b = r.pick([0.07, 0.08, 0.09]);
    const g = graph({ title: `Growth of ${$0(P)} at two rates`, xl: 'Years, t', xmax: 30, xstep: 5, yl: 'Value', series: [{ name: `${pct(a, 0)} a year`, f: t => P * (1 + a) ** t }, { name: `${pct(b, 0)} a year`, f: t => P * (1 + b) ** t }], caption: `V(t) = ${$0(P)}(1 + r)^t, compounded yearly, with r = ${pct(a, 0)} and r = ${pct(b, 0)}.` });
    if (level === 'support') { const t = r.int(5, 25), v = r2(P * (1 + b) ** t);
      return { level, prompt: `${p.name} invests ${$0(P)} at ${pct(b, 0)} a year, compounded yearly. Using V(t) = ${$0(P)}(1 + ${b})^t, what is it worth after ${t} years?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: V(t) = P(1 + r)^t.', `Substitute: ${$0(P)} × ${(1 + b).toFixed(2)}^${t} = ${money(v)}.`, `Spreadsheet: =FV(${b},${t},0,-${P}) or =${P}*(1+${b})^${t}.`, `So ${$0(P)} grows to ${money(v)}, ${(v / P).toFixed(2)} times the start, without adding money.`] }; }
    if (level === 'standard') { const t = r.pick([10, 15, 20, 25, 30]), d = r2(P * ((1 + b) ** t - (1 + a) ** t));
      return { level, prompt: `After ${t} years, how much more is the ${pct(b, 0)} investment worth than the ${pct(a, 0)} one? (The gap between the curves.)`, scenario: { graph: g }, ...numeric(d),
        solutionSteps: [`Formula: gap = P(1 + ${b})^t − P(1 + ${a})^t.`, `Substitute: ${money(P * (1 + b) ** t)} − ${money(P * (1 + a) ** t)} = ${money(d)}.`, `Spreadsheet: =${P}*(1+${b})^${t}-${P}*(1+${a})^${t}.`, `So the higher rate is worth ${money(d)} more after ${t} years. The curves pull apart faster each year because each year's growth earns growth too.`] }; }
    const m = r.pick([2, 3]), t = Math.ceil(Math.log(m) / Math.log(1 + b) - 1e-12);
    return { level, prompt: `At ${pct(b, 0)} a year, after how many whole years is ${p.name}'s investment first worth at least ${m === 2 ? 'twice' : 'three times'} the ${$0(P)} ${p.sub} started with?`, scenario: { graph: g }, ...int(t),
      solutionSteps: [`Formula: solve P(1 + r)^t ≥ ${m}P, so t ≥ ln ${m} ÷ ln(1 + r).`, `Substitute: t ≥ ln ${m} ÷ ln ${(1 + b).toFixed(2)} = ${(Math.log(m) / Math.log(1 + b)).toFixed(2)}, so ${t} whole years.`, `Spreadsheet: =ROUNDUP(NPER(${b},0,-${P},${m * P}),0) or =ROUNDUP(LN(${m})/LN(1+${b}),0).`, `So the money ${m === 2 ? 'doubles' : 'triples'} in ${t} years at ${pct(b, 0)}. At ${pct(a, 0)} it would take ${Math.ceil(Math.log(m) / Math.log(1 + a) - 1e-12)} years.`] }; },
    (q) => { const c = cap(q), P = dollars(c)[0], [a, b] = rates(c); if (q.level === 'support') return P * (1 + b) ** after(q.prompt, /after (\d+) years/); if (q.level === 'standard') { const t = after(q.prompt, /After (\d+) years/); return P * ((1 + b) ** t - (1 + a) ** t); } const m = /twice/.test(q.prompt) ? 2 : 3; return Math.ceil(Math.log(m) / Math.log(1 + b) - 1e-12); }),

  /* ---------- Housing: rent vs buy, where the costs cross ---------- */
  F('housing', 1, 'rent-buy-cross', (r, k) => { const p = person(r), level = LV[k % 3], R = r.step(15000, 24000, 600), gap = r.pick([1500, 2000, 2500, 3000]), O = R - gap, U = gap * r.int(3, 8);
    const rent = (t) => R * t, buy = (t) => U + O * t, ts = U / gap;
    const g = graph({ title: 'Unrecoverable housing costs over time', xl: 'Years, t', xmax: 10, xstep: 1, yl: 'Total cost', series: [{ name: `Rent: ${$0(R)}t`, f: rent }, { name: `Buy: ${$0(U)} + ${$0(O)}t`, f: buy }], marks: [{ x: ts, y: rent(ts), label: 'break-even' }],
      caption: `Renting costs ${$0(R)} a year. Buying costs ${$0(U)} up front (closing and moving costs) plus ${$0(O)} a year in mortgage interest, property tax, insurance and upkeep. Equity is not counted.` });
    if (level === 'support') { const t = r.int(2, 9), v = buy(t);
      return { level, prompt: `Using the buying model, what are ${p.name}'s total unrecoverable costs after ${t} years?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: Buy(t) = up-front cost + yearly cost × t.', `Substitute: ${$0(U)} + ${$0(O)} × ${t} = ${$0(v)}.`, `Spreadsheet: =${U}+${O}*${t}.`, `So buying has cost ${$0(v)} after ${t} years, compared with ${$0(rent(t))} for renting.`] }; }
    if (level === 'standard') return { level, prompt: `After how many years do renting and buying have the same total unrecoverable cost (the break-even point)?`, scenario: { graph: g }, ...int(ts),
      solutionSteps: ['Formula: set Rent(t) = Buy(t): R·t = U + O·t, so t = [[U || R − O]].', `Substitute: t = [[${$0(U)} || ${$0(R)} − ${$0(O)}]] = ${$0(U)} ÷ ${$0(gap)} = ${ts}.`, `Spreadsheet: =${U}/(${R}-${O}).`, `So buying only pays off for someone who stays more than ${ts} years; a shorter stay favors renting.`] };
    const t = r.pick([2, 3, 9, 10].filter(x => x !== ts)), d = Math.abs(rent(t) - buy(t));
    return { level, prompt: `${p.name} expects to move after ${t} years. Which costs less over that time, and by how much? Give the difference.`, scenario: { graph: g }, ...numeric(d),
      solutionSteps: ['Formula: difference = |Rent(t) − Buy(t)|.', `Substitute: Rent(${t}) = ${$0(rent(t))}; Buy(${t}) = ${$0(buy(t))}.`, `Spreadsheet: =ABS(${R}*${t}-(${U}+${O}*${t})).`, `So ${rent(t) < buy(t) ? 'renting' : 'buying'} saves ${$0(d)}: ${t} years is ${t < ts ? 'before' : 'after'} the ${ts}-year break-even.`] }; },
    (q) => { const [R, U, O] = dollars(cap(q)); if (q.level === 'standard') return U / (R - O); if (q.level === 'support') return U + O * after(q.prompt, /after (\d+) years/); const t = after(q.prompt, /after (\d+) years/); return Math.abs(R * t - U - O * t); }),

  /* ---------- Insurance: two health plans as piecewise functions ---------- */
  F('insurance', 1, 'plan-piecewise', (r, k) => { const p = person(r), level = LV[k % 3];
    const A = { prem: r.step(80, 140, 5), ded: r.pick([3000, 3500, 4000]), co: 0.2, max: r.pick([7000, 7500]) }, B = { prem: r.step(260, 340, 5), ded: r.pick([500, 750, 1000]), co: 0.2, max: r.pick([3000, 3500]) };
    const oop = (pl, b) => Math.min(pl.max, b <= pl.ded ? b : pl.ded + pl.co * (b - pl.ded)), tot = (pl, b) => pl.prem * 12 + oop(pl, b);
    const g = graph({ title: 'Total yearly cost of two health plans', xl: 'Medical bills in the year, b', xmax: 20000, xstep: 4000, xmoney: true, yl: 'Yearly cost', series: [{ name: 'Plan A (high deductible)', f: b => tot(A, b) }, { name: 'Plan B (low deductible)', f: b => tot(B, b) }],
      caption: `Plan A: ${money(A.prem)} a month, ${$0(A.ded)} deductible, then 20% coinsurance, out-of-pocket maximum ${$0(A.max)}. Plan B: ${money(B.prem)} a month, ${$0(B.ded)} deductible, then 20% coinsurance, out-of-pocket maximum ${$0(B.max)}.` });
    if (level === 'support') { const b = r.step(200, A.ded - 100, 50), v = tot(A, b);
      return { level, prompt: `${p.name} has $${b.toLocaleString('en-US')} of medical bills this year on Plan A (below the deductible, so ${p.sub} pays all of them). What is ${p.pos} total yearly cost, premiums included?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: for bills b ≤ deductible, cost = 12 × premium + b.', `Substitute: 12 × ${money(A.prem)} + $${b.toLocaleString('en-US')} = ${money(v)}.`, `Spreadsheet: =12*${A.prem}+${b}.`, `So Plan A costs ${money(v)} this year; Plan B would cost ${money(tot(B, b))}. In a low-bill year the cheaper premium wins.`] }; }
    if (level === 'standard') { let b; do { b = r.step(B.ded + 500, 12000, 100); } while (oop(B, b) >= B.max); const v = tot(B, b);
      return { level, prompt: `${p.name} has $${b.toLocaleString('en-US')} of medical bills on Plan B. What is the total yearly cost, premiums included?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: for bills above the deductible (and below the maximum), cost = 12 × premium + deductible + 20% × (b − deductible).', `Substitute: 12 × ${money(B.prem)} + ${$0(B.ded)} + 0.2 × ($${b.toLocaleString('en-US')} − ${$0(B.ded)}) = ${money(B.prem * 12)} + ${money(oop(B, b))} = ${money(v)}.`, `Spreadsheet: =12*${B.prem}+MIN(${B.max},${B.ded}+0.2*(${b}-${B.ded})).`, `So Plan B costs ${money(v)}; Plan A would cost ${money(tot(A, b))}. This is the middle piece of Plan B's graph.`] }; }
    let lo = 0, hi = 20000; const d = (b) => tot(A, b) - tot(B, b);
    if (d(0) * d(hi) > 0) return null;
    for (let i = 0; i < 80; i++) { const mid = (lo + hi) / 2; if (d(lo) * d(mid) <= 0) hi = mid; else lo = mid; }
    const x = Math.round(lo);
    return { level, prompt: `At what level of medical bills do the two plans cost the same for the year? Round to the nearest dollar.`, scenario: { graph: g }, ...numeric(x, { tolerance: 1 }),
      solutionSteps: [`Formula: set A(b) = B(b), using the piece of each graph where they cross.`, `At $0 of bills, A = ${money(tot(A, 0))} and B = ${money(tot(B, 0))}; the plans cross at b ≈ ${$0(x)}, where both cost about ${money(tot(A, x))}.`, `Spreadsheet: put bills in A2:A201 (0, 100, 200…), =12*${A.prem}+MIN(${A.max},IF(A2<=${A.ded},A2,${A.ded}+0.2*(A2-${A.ded}))) in B2, the Plan B formula in C2, then find where B − C changes sign (or use Goal Seek).`, `So below about ${$0(x)} of bills Plan A is cheaper; above it Plan B is. Someone expecting a big year should pick Plan B.`] }; },
    (q) => { const c = cap(q).split('Plan B:'), pa = (s) => { const [prem, ded, max] = dollars(s); return { prem, ded, max }; }, A = pa(c[0]), B = pa(c[1]);
      const tot = (pl, b) => pl.prem * 12 + Math.min(pl.max, b <= pl.ded ? b : pl.ded + 0.2 * (b - pl.ded));
      if (q.level !== 'advanced') return tot(q.level === 'support' ? A : B, dollars(q.prompt)[0]);
      let best = 0, bd = Infinity; for (let b = 0; b <= 20000; b++) { const v = Math.abs(tot(A, b) - tot(B, b)); if (v < bd) { bd = v; best = b; } } return best; }),

  /* ---------- College: when the degree path catches up ---------- */
  F('college', 4, 'catch-up', (r, k) => { const p = person(r), level = LV[k % 3], sA = r.step(30000, 38000, 1000), sB = sA + r.step(14000, 26000, 1000), c = r.step(12000, 24000, 1000);
    const A = (t) => sA * t, B = (t) => t <= 4 ? -c * t : -4 * c + sB * (t - 4), ts = (4 * c + 4 * sB) / (sB - sA);
    const g = graph({ title: 'Cumulative net earnings: work now vs a 4-year degree', xl: 'Years after high school, t', xmax: 20, xstep: 2, yl: 'Net earnings', ymin: -1, series: [{ name: `Work now: ${$0(sA)}t`, f: A }, { name: `Degree: −${$0(c)}t for t ≤ 4, then −${$0(4 * c)} + ${$0(sB)}(t − 4)`, f: B }],
      caption: `Work now: earn ${$0(sA)} a year. Degree: pay ${$0(c)} a year for 4 years with no earnings, then earn ${$0(sB)} a year. (Simplified: no raises, taxes or interest.)` });
    if (level === 'support') { const t = r.int(5, 20), v = A(t);
      return { level, prompt: `On the "work now" path, what has ${p.name} earned in total after ${t} years?`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: A(t) = salary × t.', `Substitute: ${$0(sA)} × ${t} = ${$0(v)}.`, `Spreadsheet: =${sA}*${t}.`, `So ${$0(v)}; the degree path stands at ${$0(B(t))} at the same point.`] }; }
    if (level === 'standard') { const t = r.int(6, 20), v = B(t);
      return { level, prompt: `On the degree path, what are ${p.name}'s cumulative net earnings after ${t} years? Use the second piece of the function.`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: [`Formula: for t > 4, B(t) = −4 × cost + new salary × (t − 4).`, `Substitute: −4 × ${$0(c)} + ${$0(sB)} × (${t} − 4) = −${$0(4 * c)} + ${$0(sB * (t - 4))} = ${$0(v)}.`, `Spreadsheet: =-4*${c}+${sB}*(${t}-4).`, `So after ${t} years the degree path is at ${$0(v)} against ${$0(A(t))} for working now${v >= A(t) ? '; it has caught up' : '; it has not caught up yet'}.`] }; }
    const t = Math.ceil(ts - 1e-9);
    return { level, prompt: `After how many whole years does the degree path first catch up with (equal or pass) the work-now path?`, scenario: { graph: g }, ...int(t),
      solutionSteps: ['Formula: solve A(t) = B(t) with the second piece: sA·t = −4c + sB(t − 4), so t = [[4c + 4sB || sB − sA]].', `Substitute: t = [[4 × ${$0(c)} + 4 × ${$0(sB)} || ${$0(sB)} − ${$0(sA)}]] = ${$0(4 * c + 4 * sB)} ÷ ${$0(sB - sA)} = ${ts.toFixed(2)}, so year ${t}.`, `Spreadsheet: =ROUNDUP((4*${c}+4*${sB})/(${sB}-${sA}),0).`, `So the degree pays off in year ${t}, when ${p.name} is about ${18 + t}. Raises, loan interest or a different field would move this point.`] }; },
    (q) => { const [sA, c, sB] = dollars(cap(q)); const A = t => sA * t, B = t => t <= 4 ? -c * t : -4 * c + sB * (t - 4); if (q.level === 'support') return A(after(q.prompt, /after (\d+) years/)); if (q.level === 'standard') return B(after(q.prompt, /after (\d+) years/)); let t = 5; while (B(t) < A(t) - 1e-9) t++; return t; }),

  /* ---------- Retirement: inflation as exponential growth ---------- */
  F('retirement', 1, 'inflation-curves', (r, k) => { const p = person(r), level = LV[k % 3], P = r.pick([4, 6, 12, 20, 45, 120]), a = 0.02, b = r.pick([0.03, 0.04, 0.05]);
    const g = graph({ title: `Price of a $${P} item with inflation`, xl: 'Years, t', xmax: 40, xstep: 5, yl: 'Price', series: [{ name: `${pct(a, 0)} inflation`, f: t => P * (1 + a) ** t }, { name: `${pct(b, 0)} inflation`, f: t => P * (1 + b) ** t }], caption: `Price(t) = $${P}(1 + i)^t, with i = ${pct(a, 0)} and i = ${pct(b, 0)} a year.` });
    if (level === 'support') { const t = r.pick([5, 10, 20, 30]), v = r2(P * (1 + b) ** t);
      return { level, prompt: `With ${pct(b, 0)} inflation, what will the $${P} item cost in ${t} years? Use Price(t) = $${P}(1 + ${b})^t.`, scenario: { graph: g }, ...numeric(v),
        solutionSteps: ['Formula: Price(t) = P(1 + i)^t.', `Substitute: $${P} × ${(1 + b).toFixed(2)}^${t} = ${money(v)}.`, `Spreadsheet: =${P}*(1+${b})^${t}.`, `So the same item costs ${money(v)}: a dollar then buys about ${(100 / (1 + b) ** t).toFixed(0)}¢ of today's goods.`] }; }
    if (level === 'standard') { const t = r.pick([10, 20, 30, 40]), d = r2(P * ((1 + b) ** t - (1 + a) ** t));
      return { level, prompt: `After ${t} years, how much more does the item cost with ${pct(b, 0)} inflation than with ${pct(a, 0)}?`, scenario: { graph: g }, ...numeric(d),
        solutionSteps: [`Formula: gap = P(1 + ${b})^t − P(1 + ${a})^t.`, `Substitute: ${money(P * (1 + b) ** t)} − ${money(P * (1 + a) ** t)} = ${money(d)}.`, `Spreadsheet: =${P}*(1+${b})^${t}-${P}*(1+${a})^${t}.`, `So a few points of inflation add ${money(d)} to this one price after ${t} years. Retirement plans have to assume a rate, and the choice matters.`] }; }
    const t = Math.ceil(Math.log(2) / Math.log(1 + b) - 1e-12);
    return { level, prompt: `With ${pct(b, 0)} inflation, after how many whole years has the price first at least doubled?`, scenario: { graph: g }, ...int(t),
      solutionSteps: ['Formula: solve (1 + i)^t ≥ 2, so t ≥ ln 2 ÷ ln(1 + i).', `Substitute: ln 2 ÷ ln ${(1 + b).toFixed(2)} = ${(Math.log(2) / Math.log(1 + b)).toFixed(2)}, so ${t} years. (Rule of 72: 72 ÷ ${b * 100} ≈ ${(72 / (b * 100)).toFixed(1)}.)`, `Spreadsheet: =ROUNDUP(LN(2)/LN(1+${b}),0).`, `So prices double in ${t} years; ${p.name} would need twice the income then to buy the same things.`] }; },
    (q) => { const c = cap(q), P = dollars(c)[0], [a, b] = rates(c); if (q.level === 'support') return P * (1 + b) ** after(q.prompt, /in (\d+) years/); if (q.level === 'standard') { const t = after(q.prompt, /After (\d+) years/); return P * ((1 + b) ** t - (1 + a) ** t); } return Math.ceil(Math.log(2) / Math.log(1 + b) - 1e-12); })
];

export const modelingFamilies = {};
for (const f of fams) (modelingFamilies[f.unit] = modelingFamilies[f.unit] || []).push(f.fam);
