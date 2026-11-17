/* Independent check of the 2026-11-16 applied families: re-reads the numbers from each prompt and recomputes the
 * answer from scratch (no FA_MATH), then compares with the stored key. Also guards the dated 2026 tax figures. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { TAX_2026 } from '../financial/content/real-data-2026.mjs';
const root = new URL('../', import.meta.url);
const bank = (u) => JSON.parse(readFileSync(new URL(`financial/banks/${u}.json`, root), 'utf8')).questions;
const money = (s) => [...s.matchAll(/[−-]?\$([\d,]+(?:\.\d+)?)/g)].map(m => Number(m[1].replace(/,/g, '')));
const pcts = (s) => [...s.matchAll(/([\d.]+)%/g)].map(m => Number(m[1]) / 100);
const ints = (s, re) => Number(s.match(re)[1]);
const num = (q) => q.numeric ? q.numeric.value : Number(String(q.answer).replace(/[^\d.\-]/g, ''));
const r2 = (x) => Math.round(x * 100 + 1e-9) / 100;
const pmt = (P, apr, n) => { const i = apr / 12; return P * i / (1 - (1 + i) ** -n); };
function tax(taxable, br) { let t = 0, lo = 0; for (const b of br) { if (taxable <= lo) break; t += (Math.min(taxable, b.upTo) - lo) * b.rate; lo = b.upTo; } return t; }

const CHECK = {
  'ap-commission-month': (p) => { const [base, sales] = money(p), [rate] = pcts(p); return base + rate * sales; },
  'ap-fica-check': (p) => { const [g] = money(p); return r2(g * 0.062) + r2(g * 0.0145); },
  'ap-ytd-periods': (p) => { const [per, ytd] = money(p); return ytd / per; },
  'ap-stub-net-check': (p) => { const [g, ...d] = money(p); return g - d.reduce((a, b) => a + b, 0); },
  'ap-tax-2026': (p) => { const [gross, sd] = money(p); return tax(Math.max(0, gross - sd), TAX_2026.bracketsSingle); },
  'ap-ss-wage-base': (p) => { const [base, sal] = money(p); return Math.min(base, sal) * 0.062; },
  'ap-rule-503020': (p) => { const [net] = money(p); return net * (/needs/.test(p.split('should go to')[1]) ? 0.5 : /wants/.test(p.split('should go to')[1]) ? 0.3 : 0.2); },
  'ap-variable-average': (p) => { const m = money(p); return (m[0] + m[1] + m[2]) / 3; },
  'ap-max-units': (p) => { const [budget, fixed, each] = money(p); return Math.floor((budget - fixed) / each); },
  'ap-annual-plan': (p) => { const [mo, yr] = money(p); return mo * 12 - yr; },
  'ap-overdraft': (p) => { const [bal, buy, fee] = money(p); return bal - buy - fee; },
  'ap-fee-waiver': (p) => { const [fee, min, ...b] = money(p); return b.filter(x => x < min).length * fee; },
  'ap-si-solve': (p) => { const [P, I] = money(p), t = ints(p, /After (\d+) years/); return I / (P * t) * 100; },
  'ap-apy-compare': (p) => { const [dep] = money(p), [a, b] = pcts(p); return Math.abs(r2(dep * (1 + a / 12) ** 12 - dep) - r2(dep * b)); },
  'ap-reconcile': (p) => { const [s, d, c1, c2] = money(p); return s + d - c1 - c2; },
  'ap-carry-part': (p) => { const [bal, paid] = money(p), [apr] = pcts(p); return (bal - paid) * apr / 12; },
  'ap-util-target': (p) => { const [lim] = money(p), [t] = pcts(p); return lim * t; },
  'ap-late-cost': (p) => { const [fee, bal] = money(p), [apr, pen] = pcts(p); return bal * (pen - apr) / 12 + fee; },
  'ap-transfer-fee': (p) => { const [bal] = money(p), pc = pcts(p); return bal * pc[pc.length - 1]; },
  'ap-payment-split': (p) => { const [bal, pay, it] = money(p); return pay - it; },
  'ap-total-interest': (p) => { const [P, pay] = money(p), n = ints(p, /for (\d+) months/); return pay * n - P; },
  'ap-down-payment': (p) => { const m = money(p), [dp] = pcts(p); return m[0] * (1 - dp) - (m[1] || 0); },
  'ap-first-interest': (p) => { const [P, pay] = money(p), [apr] = pcts(p); return pay - r2(P * apr / 12); },
  'ap-term-compare': (p) => { const [, a, b] = money(p); return b * 72 - a * 48; },
  'ap-rule-72': (p) => 72 / pcts(p)[0] / 100,
  'ap-div-yield': (p) => { const [price, div] = money(p); return div * 4 / price * 100; },
  'ap-expense-ratio': (p) => { const [bal] = money(p), [a, b] = pcts(p); return bal * (b - a); },
  'ap-allocation-drop': (p) => { const [tot] = money(p), [st, drop] = pcts(p); return tot * st * (1 - drop) + tot * (1 - st); },
  'ap-contributed-vs-growth': (p) => { const [m, fv] = money(p), y = ints(p, /for (\d+) years/); return fv - m * 12 * y; },
  'ap-rule-28': (p) => { const [inc] = money(p); return inc / 12 * 0.28; },
  'ap-cash-to-close': (p) => { const [price] = money(p), [dp, cc] = pcts(p); return price * (dp + cc); },
  'ap-escrow-tax': (p) => { const [v, ins] = money(p), [rate] = pcts(p); return (v * rate + ins) / 12; },
  'ap-opportunity': (p) => { const [dp] = money(p), [rate] = pcts(p), y = ints(p, /over (\d+) years/); return dp * (1 + rate) ** y - dp; },
  'ap-claim-net': (p) => { const [d, ded] = money(p); return Math.max(0, d - ded); },
  'ap-coinsurance': (p) => { const [ded, max, bill] = money(p), [co] = pcts(p); return Math.min(max, Math.min(bill, ded) + Math.max(0, bill - ded) * co); },
  'ap-warranty-ev': (p) => { const [cost, repair] = money(p), [prob] = pcts(p); return prob * repair - cost; },
  'ap-annual-premium': (p) => { const [a, da, b, db, claim] = money(p); return Math.abs((a * 12 + Math.min(da, claim)) - (b * 12 + Math.min(db, claim))); },
  'ap-net-price-calc': (p) => { const [c, g, s] = money(p); return c - g - s; },
  'ap-unsub-accrue': (p) => { const [P] = money(p), [rate] = pcts(p), y = Number(p.match(/for ([\d.]+) years/)[1]); return P * rate * y; },
  'ap-career-gap': (p) => { const [a, b] = money(p), y = ints(p, /over (\d+) years/); return (b - a) * y; },
  'ap-payback-simple': (p) => { const [c, g] = money(p); return Math.round(c / g * 10) / 10; },
  'ap-match-calc': (p) => { const [sal] = money(p), pc = pcts(p); return sal * Math.min(pc[0], 0.06) * pc[1]; },
  'ap-nest-egg-4': (p) => { const [spend, ss] = money(p); return Math.max(0, spend - ss) / 0.04; },
  'ap-future-price': (p) => { const [price] = money(p), [i] = pcts(p), y = ints(p, /in (\d+) years/); return price * (1 + i) ** y; },
  'ap-real-return': (p) => { const [n, i] = pcts(p); return ((1 + n) / (1 + i) - 1) * 100; }
};
const TOL = { 'ap-total-interest': 0.06, 'ap-term-compare': 0.06, 'ap-contributed-vs-growth': 0.06, 'ap-div-yield': 0.06, 'ap-payback-simple': 0.06, 'ap-real-return': 0.006 };

test('every applied question recomputes independently from its prompt', () => {
  const units = ['income', 'budgeting', 'banking', 'credit', 'borrowing', 'investing', 'housing', 'insurance', 'college', 'retirement'];
  let n = 0; const seen = new Set();
  for (const u of units) for (const q of bank(u).filter(q => q.family.startsWith('ap-'))) {
    if (q.format !== 'short-answer') continue;
    const f = CHECK[q.family]; assert.ok(f, 'no independent check for ' + q.family); seen.add(q.family);
    const want = f(q.prompt), got = num(q);
    assert.ok(Math.abs(want - got) <= (TOL[q.family] ?? 0.011), `${q.id}: prompt gives ${want}, key says ${got}\n${q.prompt}`);
    n++;
  }
  assert.ok(n >= 250, 'expected 250+ applied numeric questions, found ' + n);
  assert.equal(seen.size, Object.keys(CHECK).length, 'every checker used');
});

test('marginal-rate questions match the 2026 single-filer table', () => {
  for (const q of bank('income').filter(q => q.family === 'ap-marginal-2026')) {
    const [gross, sd] = money(q.prompt), taxable = Math.max(0, gross - sd);
    const b = TAX_2026.bracketsSingle.find(b => taxable <= b.upTo);
    assert.equal(q.answer, Math.round(b.rate * 100) + '%', q.id);
  }
});

test('2026 tax figures are dated, sourced and not stale', () => {
  assert.equal(TAX_2026.standardDeduction.single, 16100);
  assert.deepEqual(TAX_2026.bracketsSingle.slice(0, 4).map(b => b.upTo), [12400, 50400, 105700, 201775]);
  assert.equal(TAX_2026.socialSecurityWageBase, 184500);
  const age = (Date.now() - Date.parse(TAX_2026.asOfDate)) / 864e5;
  assert.ok(age < 460, `real-data-2026.mjs is ${Math.round(age)} days old: update the figures for the new tax year`);
  for (const q of bank('income').filter(q => /2026/.test(q.family))) assert.match(q.prompt, /2026/, q.id + ' must state the year');
});
