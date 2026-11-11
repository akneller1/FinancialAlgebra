import test from 'node:test';
import assert from 'node:assert/strict';
import '../financial/lib/finance.js';
const M = globalThis.FA_MATH;
const near = (a, b, tol = 0.01, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg || ''} expected ${b}, got ${a}`);

test('rounding and basic interest', () => {
  assert.equal(M.round2(1.005), 1.01); assert.equal(M.round2(-2.345), -2.35);
  near(M.simpleInterest(2000, 0.03, 2), 120);
  near(M.compoundAmount(1000, 0.05, 1, 2), 1102.5);
  near(M.apy(0.04, 12), 0.040742, 1e-6);
  near(M.compoundAmount(5000, 0.08, 1, 30), 50313.28, 0.01);
});
test('annuities and goals', () => {
  near(M.fvAnnuity(100, 0.06, 12, 10), 16387.93, 0.01);
  near(M.depositForGoal(16387.93, 0.06, 12, 10), 100, 0.01);
  near(M.presentValue(1102.5, 0.05, 1, 2), 1000, 1e-6);
  near(M.ruleOf72(8), 9, 1e-9);
});
test('loan payment and amortization reconcile', () => {
  near(M.loanPayment(20000, 0.06, 60), 386.66);
  near(M.loanPayment(320000, 0.0675, 360), 2075.51);
  for (const [P, apr, n] of [[17500, 0.079, 60], [12500, 0.079, 48], [342000, 0.0675, 360], [3000, 0, 12]]) {
    const a = M.amortize(P, apr, n);
    assert.equal(a.months, n, 'term');
    assert.equal(a.rows.at(-1).balance, 0);
    near(a.rows.reduce((s, r) => s + r.principal, 0), P, 0.02, 'principal sums');
    near(a.totalPaid - a.totalInterest, P, 0.02, 'paid − interest = P');
  }
  near(M.remainingBalance(20000, 0.06, 60, 60), 0, 0.5); // payment is rounded to cents, so the closed form ends within cents
});
test('lease, card, and payoff models', () => {
  const l = M.leasePayment(31000, 17980, 36, 0.0025); near(l.payment, 484.12);
  near(M.cardInterest(3400, 0.2499), 70.81); near(M.minimumPayment(3400, 0.2499), 104.81);
  const p = M.payoff(3400, 0.2499, { type: 'fixed', amount: 150 }); assert.equal(p.months, 31); assert.ok(p.rows.at(-1).balance === 0);
  assert.ok(M.payoff(5000, 0.3, { type: 'fixed', amount: 100 }).neverPaysOff, 'payment below interest never pays off');
  const av = M.multiDebtPayoff([{ name: 'a', balance: 1000, apr: 0.29, minPayment: 25 }, { name: 'b', balance: 3000, apr: 0.1, minPayment: 50 }], 300, 'avalanche');
  const sn = M.multiDebtPayoff([{ name: 'a', balance: 1000, apr: 0.29, minPayment: 25 }, { name: 'b', balance: 3000, apr: 0.1, minPayment: 50 }], 300, 'snowball');
  assert.ok(av.totalInterest <= sn.totalInterest);
  near(M.adbInterest([{ balance: 600, days: 12 }, { balance: 900, days: 18 }], 0.24), 15.39);
});
test('taxes and paychecks (course tax table)', () => {
  const t = M.federalIncomeTax(54000); assert.equal(t.taxable, 39000); near(t.tax, 4440);
  near(M.progressiveTax(30000).tax, 3360);
  const n = M.netPay(50000); near(n.socialSecurity + n.medicare, 3825);
  assert.ok(M.netPay(63500).net > M.netPay(60500).net, 'raise never lowers take-home');
  near(M.weeklyPay(20, 46), 980);
  near(M.annualFromHourly(26, 40, 52, 4), 62192);
});
test('insurance, housing, retirement', () => {
  const pl = { premium: 210, deductible: 2000, coinsurance: 0.2, oopMax: 6000, copay: 35 };
  near(M.healthPlanCost(pl, 2500, 4).outOfPocket, 2240); near(M.healthPlanCost(pl, 100000, 4).outOfPocket, 6000);
  near(M.expectedValue([{ p: 0.02, value: 10000 }, { p: 0.98, value: 0 }]), 200);
  near(M.claimPayout(4300, 500), 3800);
  const m = M.mortgage(380000, 0.2, 0.0675, 30, 0.012, 1500, 0.007, 0); assert.equal(m.pmi, 0); near(m.piti, m.principalInterest + 380 + 125);
  const rb = M.rentVsBuy({ years: 7, rent: 2100, price: 380000, downPct: 0.2, apr: 0.0675, taxRate: 0.012, insuranceYr: 1500, closingPct: 0.03, maintenancePct: 0.01, appreciation: 0.03, sellingPct: 0.06, investReturn: 0.05, rentGrowth: 0.03 });
  assert.ok(rb.equity > 0 && rb.buyNetCost > 0 && rb.rentTotal > 0);
  near(M.realReturn(0.06, 0.025), 0.034146, 1e-6); near(M.inflate(100, 0.03, 1), 103);
  near(M.purchasingPower(M.inflate(5000, 0.025, 30), 0.025, 30), 5000, 1e-6);
  near(M.retirementBalance({ salary: 50000, contribPct: 0.06, matchRate: 0.5, matchLimit: 0.06, r: 0.06, years: 42 }).monthlyEmployer, 125);
  near(M.nestEggNeeded(40000), 1000000);
});
