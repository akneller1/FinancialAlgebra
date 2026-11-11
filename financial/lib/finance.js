/* Financial Algebra — deterministic financial math engine.
 * Plain script: attaches globalThis.FA_MATH in browsers and Node (import for side effects).
 * Every function is pure. Money is rounded to cents ONLY where a real institution would round
 * (payments, statement interest, tax withholding). Projections keep full precision until display.
 * All rates are decimals (0.05 = 5%). All values are hypothetical classroom assumptions.
 */
(function (G) {
  'use strict';
  var EPS = 1e-9;
  function round2(x) { return Math.round((x + (x >= 0 ? EPS : -EPS)) * 100) / 100; }
  function round(x, d) { var f = Math.pow(10, d || 0); return Math.round((x + (x >= 0 ? EPS : -EPS)) * f) / f; }
  function sum(a) { return a.reduce(function (s, v) { return s + v; }, 0); }

  /* Explicit, labeled course assumptions. Not current law; illustrative only. */
  var ASSUMPTIONS = {
    taxYearLabel: 'Course Tax Table (illustrative, simplified; not an official IRS table)',
    standardDeduction: 15000,
    federalBrackets: [ // single filer, marginal
      { upTo: 12000, rate: 0.10 }, { upTo: 48000, rate: 0.12 }, { upTo: 103000, rate: 0.22 },
      { upTo: 197000, rate: 0.24 }, { upTo: 250000, rate: 0.32 }, { upTo: Infinity, rate: 0.35 }
    ],
    socialSecurityRate: 0.062, medicareRate: 0.0145, // FICA = 7.65% (wage-base cap ignored at these incomes)
    stateFlatRate: 0.05, // flat state income tax similar to Massachusetts; state exemptions ignored
    creditMinimum: { pctOfBalance: 0.01, plusInterest: true, floor: 25 },
    weeksPerYear: 52, hoursPerWeek: 40, overtimeMultiplier: 1.5
  };

  /* ---------- Income ---------- */
  function annualFromHourly(rate, hoursPerWeek, weeks, otHoursPerWeek) {
    weeks = weeks == null ? 52 : weeks; otHoursPerWeek = otHoursPerWeek || 0;
    return rate * hoursPerWeek * weeks + rate * ASSUMPTIONS.overtimeMultiplier * otHoursPerWeek * weeks;
  }
  function weeklyPay(rate, hours) { // overtime beyond 40 at 1.5x
    var reg = Math.min(hours, 40), ot = Math.max(0, hours - 40);
    return round2(rate * reg + rate * ASSUMPTIONS.overtimeMultiplier * ot);
  }
  function hourlyEquivalent(salary, hoursPerWeek, weeks) { return salary / ((hoursPerWeek || 40) * (weeks || 52)); }
  var PERIODS = { weekly: 52, biweekly: 26, semimonthly: 24, monthly: 12, annual: 1 };
  function perPeriod(annual, freq) { return annual / PERIODS[freq]; }

  function progressiveTax(taxable, brackets) {
    brackets = brackets || ASSUMPTIONS.federalBrackets;
    var tax = 0, lower = 0, rows = [];
    for (var i = 0; i < brackets.length && taxable > lower; i++) {
      var top = Math.min(taxable, brackets[i].upTo), amt = top - lower;
      if (amt > 0) { var t = amt * brackets[i].rate; tax += t; rows.push({ from: lower, to: top, rate: brackets[i].rate, tax: round2(t) }); }
      lower = brackets[i].upTo;
    }
    return { tax: round2(tax), rows: rows, marginalRate: rows.length ? rows[rows.length - 1].rate : 0, effectiveRate: taxable > 0 ? tax / taxable : 0 };
  }
  function federalIncomeTax(gross, preTax) {
    var taxable = Math.max(0, gross - (preTax || 0) - ASSUMPTIONS.standardDeduction);
    var r = progressiveTax(taxable);
    r.taxable = taxable; r.effectiveOnGross = gross > 0 ? r.tax / gross : 0;
    return r;
  }
  /* Annual paycheck model. preTax = 401(k)/health premiums (reduce income-tax wages, not FICA, in this course model).
   * Health premiums are pre-tax for FICA in reality too; course simplifies: FICA on gross minus healthPremium. */
  function netPay(gross, opts) {
    opts = opts || {};
    var retirement = (opts.retirementPct || 0) * gross, health = opts.healthPremium || 0;
    var fed = federalIncomeTax(gross, retirement + health).tax;
    var ficaBase = gross - health;
    var ss = round2(ficaBase * ASSUMPTIONS.socialSecurityRate), med = round2(ficaBase * ASSUMPTIONS.medicareRate);
    var stateRate = opts.stateRate == null ? ASSUMPTIONS.stateFlatRate : opts.stateRate;
    var state = round2(Math.max(0, gross - retirement - health) * stateRate);
    var deductions = fed + ss + med + state + retirement + health;
    return { gross: round2(gross), federal: fed, socialSecurity: ss, medicare: med, state: state,
      retirement: round2(retirement), health: round2(health), totalDeductions: round2(deductions), net: round2(gross - deductions) };
  }

  /* ---------- Budgeting ---------- */
  function cashFlow(income, expenses) { // arrays or numbers
    var i = Array.isArray(income) ? sum(income) : income, e = Array.isArray(expenses) ? sum(expenses) : expenses;
    return round2(i - e);
  }
  function percentOf(part, whole) { return whole ? part / whole : 0; }
  function rule503020(net) { return { needs: round2(net * 0.5), wants: round2(net * 0.3), savings: round2(net * 0.2) }; }
  function monthsToGoal(goal, monthly, start) { start = start || 0; return monthly > 0 ? Math.max(0, Math.ceil((goal - start) / monthly - EPS)) : Infinity; }
  function annualize(amount, freq) { return amount * PERIODS[freq]; }
  function breakEven(fixedCost, savingPerUse) { return savingPerUse > 0 ? Math.ceil(fixedCost / savingPerUse - EPS) : Infinity; }

  /* ---------- Interest & growth ---------- */
  function simpleInterest(P, r, t) { return P * r * t; }
  function compoundAmount(P, r, n, t) { return n === Infinity ? P * Math.exp(r * t) : P * Math.pow(1 + r / n, n * t); }
  function apy(r, n) { return n === Infinity ? Math.exp(r) - 1 : Math.pow(1 + r / n, n) - 1; }
  /* Future value of level deposits made each compounding period (end of period unless timing==='begin'). */
  function fvAnnuity(pmt, r, n, t, timing) {
    var i = r / n, N = Math.round(n * t);
    var fv = i === 0 ? pmt * N : pmt * (Math.pow(1 + i, N) - 1) / i;
    return timing === 'begin' ? fv * (1 + i) : fv;
  }
  function futureValue(P, pmt, r, n, t, timing) { return compoundAmount(P, r, n, t) + fvAnnuity(pmt, r, n, t, timing); }
  function presentValue(FV, r, n, t) { return FV / Math.pow(1 + r / n, n * t); }
  function depositForGoal(goal, r, n, t) { var i = r / n, N = Math.round(n * t); return i === 0 ? goal / N : goal * i / (Math.pow(1 + i, N) - 1); }
  function growthTable(P, pmt, r, years) { // annual compounding of monthly deposits approximated with monthly compounding
    var rows = [], bal = P, contrib = P;
    for (var y = 1; y <= years; y++) {
      bal = futureValue(bal, pmt, r, 12, 1); contrib += pmt * 12;
      rows.push({ year: y, balance: bal, contributions: contrib, growth: bal - contrib });
    }
    return rows;
  }
  function ruleOf72(ratePct) { return 72 / ratePct; }
  function yearsToDouble(r, n) { return Math.log(2) / (n * Math.log(1 + r / n)); }

  /* ---------- Loans ---------- */
  function loanPayment(P, apr, months) {
    var i = apr / 12;
    return round2(i === 0 ? P / months : P * i / (1 - Math.pow(1 + i, -months)));
  }
  function amortize(P, apr, months, payment) {
    var i = apr / 12, pay = payment || loanPayment(P, apr, months), bal = P, rows = [], totInt = 0, totPaid = 0;
    for (var m = 1; m <= months * 4 && bal > 0.004; m++) {
      var interest = round2(bal * i), p = (m === months && !payment) ? round2(bal + interest) : Math.min(pay, round2(bal + interest)), principal = round2(p - interest);
      if (principal <= 0) throw Error('Payment does not cover interest');
      bal = round2(bal - principal); totInt += interest; totPaid += p;
      rows.push({ month: m, payment: round2(p), interest: interest, principal: principal, balance: bal });
    }
    return { payment: pay, rows: rows, totalInterest: round2(totInt), totalPaid: round2(totPaid), months: rows.length };
  }
  function totalLoanCost(P, apr, months, down, fees) {
    var a = amortize(P, apr, months);
    return { payment: a.payment, totalInterest: a.totalInterest, totalPaid: a.totalPaid, totalCost: round2(a.totalPaid + (down || 0) + (fees || 0)) };
  }
  /* Simplified closed-end lease: depreciation + rent charge (money factor). */
  function leasePayment(capCost, residual, months, moneyFactor) {
    var dep = (capCost - residual) / months, rent = (capCost + residual) * moneyFactor;
    return { depreciation: round2(dep), rentCharge: round2(rent), payment: round2(dep + rent) };
  }
  function mileageOverage(allowedPerYear, actualPerYear, years, perMile) { return round2(Math.max(0, (actualPerYear - allowedPerYear) * years) * perMile); }
  function depreciatedValue(price, annualRate, years) { return price * Math.pow(1 - annualRate, years); }

  /* ---------- Credit cards ---------- */
  function monthlyRate(apr) { return apr / 12; }
  function cardInterest(balance, apr) { return round2(balance * apr / 12); }
  function averageDailyBalance(segments) { // [{balance, days}]
    var days = sum(segments.map(function (s) { return s.days; }));
    return sum(segments.map(function (s) { return s.balance * s.days; })) / days;
  }
  function adbInterest(segments, apr) { var d = sum(segments.map(function (s) { return s.days; })); return round2(averageDailyBalance(segments) * apr / 365 * d); }
  function minimumPayment(balance, apr, rule) {
    rule = rule || ASSUMPTIONS.creditMinimum;
    var interest = cardInterest(balance, apr);
    var m = round2(balance * rule.pctOfBalance + (rule.plusInterest ? interest : 0));
    return round2(Math.min(balance + interest, Math.max(rule.floor, m)));
  }
  /* strategy: {type:'fixed', amount} or {type:'minimum'} or {type:'fixedPlusNew', amount, charge} */
  function payoff(balance, apr, strategy, maxMonths) {
    maxMonths = maxMonths || 1200;
    var bal = balance, rows = [], totInt = 0, totPaid = 0;
    for (var m = 1; m <= maxMonths && bal > 0.004; m++) {
      var interest = cardInterest(bal, apr);
      var pay = strategy.type === 'minimum' ? minimumPayment(bal, apr) : strategy.amount;
      pay = Math.min(pay, round2(bal + interest));
      if (pay <= interest && m > 1) return { months: Infinity, totalInterest: Infinity, totalPaid: Infinity, rows: rows, neverPaysOff: true };
      bal = round2(bal + interest - pay); totInt += interest; totPaid += pay;
      rows.push({ month: m, interest: interest, payment: round2(pay), balance: bal });
    }
    return { months: bal > 0.004 ? Infinity : rows.length, totalInterest: round2(totInt), totalPaid: round2(totPaid), rows: rows, neverPaysOff: bal > 0.004 };
  }
  /* Avalanche (highest APR first) vs snowball (smallest balance first) with a fixed total budget. */
  function multiDebtPayoff(debts, monthlyBudget, method, maxMonths) {
    maxMonths = maxMonths || 600;
    var ds = debts.map(function (d) { return { name: d.name, bal: d.balance, apr: d.apr, min: d.minPayment }; });
    var totInt = 0, m = 0, order = [];
    while (ds.some(function (d) { return d.bal > 0.004; }) && m < maxMonths) {
      m++;
      ds.forEach(function (d) { if (d.bal > 0) { var it = cardInterest(d.bal, d.apr); d.bal = round2(d.bal + it); totInt += it; } });
      var budget = monthlyBudget;
      ds.forEach(function (d) { if (d.bal > 0) { var p = Math.min(d.min, d.bal); d.bal = round2(d.bal - p); budget -= p; } });
      var active = ds.filter(function (d) { return d.bal > 0.004; }).sort(function (a, b) { return method === 'avalanche' ? b.apr - a.apr : a.bal - b.bal; });
      for (var k = 0; k < active.length && budget > 0.004; k++) { var x = Math.min(budget, active[k].bal); active[k].bal = round2(active[k].bal - x); budget = round2(budget - x); }
      ds.forEach(function (d) { if (d.bal <= 0.004 && order.indexOf(d.name) < 0) order.push(d.name); });
    }
    return { months: m, totalInterest: round2(totInt), payoffOrder: order };
  }

  /* ---------- Housing ---------- */
  function mortgage(price, downPct, apr, years, taxRate, insuranceYr, pmiRate, hoaMonthly) {
    var loan = price * (1 - downPct), pi = loanPayment(loan, apr, years * 12);
    var tax = round2(price * (taxRate || 0) / 12), ins = round2((insuranceYr || 0) / 12);
    var pmi = downPct < 0.2 ? round2(loan * (pmiRate || 0) / 12) : 0;
    return { loan: loan, principalInterest: pi, tax: tax, insurance: ins, pmi: pmi, hoa: hoaMonthly || 0, piti: round2(pi + tax + ins + pmi + (hoaMonthly || 0)) };
  }
  function remainingBalance(P, apr, months, paidMonths) {
    var i = apr / 12, pay = loanPayment(P, apr, months);
    return i === 0 ? P - pay * paidMonths : P * Math.pow(1 + i, paidMonths) - pay * (Math.pow(1 + i, paidMonths) - 1) / i;
  }
  /* Rent vs buy over a horizon; returns net cost (outflows minus equity recovered) for each choice. */
  function rentVsBuy(o) {
    var y = o.years, rentTotal = 0, rent = o.rent;
    for (var k = 0; k < y; k++) { rentTotal += (rent + (o.rentersInsurance || 0)) * 12; rent *= 1 + (o.rentGrowth || 0); }
    var m = mortgage(o.price, o.downPct, o.apr, o.termYears || 30, o.taxRate, o.insuranceYr, o.pmiRate, o.hoa);
    var down = o.price * o.downPct, closing = o.price * (o.closingPct || 0);
    var maint = 0; for (var j = 0; j < y; j++) maint += o.price * Math.pow(1 + (o.appreciation || 0), j) * (o.maintenancePct || 0);
    var owned = m.piti * 12 * y + down + closing + maint;
    var value = o.price * Math.pow(1 + (o.appreciation || 0), y), bal = remainingBalance(m.loan, o.apr, (o.termYears || 30) * 12, y * 12);
    var sale = value * (o.sellingPct || 0), equity = value - bal - sale;
    var forgone = down + closing; var oppCost = forgone * (Math.pow(1 + (o.investReturn || 0), y) - 1);
    var buyNet = owned - equity + oppCost;
    return { rentTotal: round2(rentTotal), buyOutflow: round2(owned), equity: round2(equity), opportunityCost: round2(oppCost), buyNetCost: round2(buyNet), monthlyOwn: m.piti, homeValue: round2(value), loanBalance: round2(bal) };
  }
  function affordability(grossAnnual, frontRatio) { return round2(grossAnnual / 12 * (frontRatio || 0.28)); }
  function debtToIncome(monthlyDebt, grossMonthly) { return grossMonthly ? monthlyDebt / grossMonthly : 0; }

  /* ---------- Insurance & risk ---------- */
  function expectedValue(outcomes) { return sum(outcomes.map(function (o) { return o.p * o.value; })); }
  /* Health plan annual cost for a given amount of covered medical bills. */
  function healthPlanCost(plan, bills, copayVisits) {
    var ded = Math.min(bills, plan.deductible), rest = Math.max(0, bills - plan.deductible);
    var oop = ded + rest * plan.coinsurance + (plan.copay || 0) * (copayVisits || 0);
    oop = Math.min(oop, plan.oopMax == null ? Infinity : plan.oopMax);
    return { premiums: round2(plan.premium * 12), outOfPocket: round2(oop), total: round2(plan.premium * 12 + oop) };
  }
  function claimPayout(loss, deductible, limit) { return round2(Math.max(0, Math.min(loss - deductible, limit == null ? Infinity : limit))); }

  /* ---------- College ROI ---------- */
  function netPrice(coa, grants, scholarships) { return round2(coa - (grants || 0) - (scholarships || 0)); }
  function paybackYears(extraCost, extraAnnualIncome) { return extraAnnualIncome > 0 ? extraCost / extraAnnualIncome : Infinity; }
  function careerEarnings(start, growth, years, startDelay) {
    var tot = 0, s = start; for (var y = 0; y < years; y++) { if (y >= (startDelay || 0)) { tot += s; s *= 1 + growth; } } return tot;
  }
  function earningsBy(age, startAge, start, growth) { var tot = 0, s = start; for (var a = startAge; a < age; a++) { tot += s; s *= 1 + growth; } return tot; }

  /* ---------- Inflation & retirement ---------- */
  function inflate(amount, rate, years) { return amount * Math.pow(1 + rate, years); }
  function purchasingPower(amount, rate, years) { return amount / Math.pow(1 + rate, years); }
  function realReturn(nominal, inflation) { return (1 + nominal) / (1 + inflation) - 1; }
  function cpiAdjust(price, cpiThen, cpiNow) { return price * cpiNow / cpiThen; }
  function retirementBalance(o) { // monthly contributions with employer match, monthly compounding
    var emp = o.salary * o.contribPct / 12, match = o.salary * Math.min(o.contribPct, o.matchLimit || 0) * (o.matchRate || 0) / 12;
    return { monthlyEmployee: emp, monthlyEmployer: match, balance: futureValue(o.start || 0, emp + match, o.r, 12, o.years) };
  }
  function nestEggNeeded(annualSpend, withdrawalRate) { return annualSpend / (withdrawalRate || 0.04); }

  G.FA_MATH = {
    ASSUMPTIONS: ASSUMPTIONS, PERIODS: PERIODS, round2: round2, round: round, sum: sum,
    annualFromHourly: annualFromHourly, weeklyPay: weeklyPay, hourlyEquivalent: hourlyEquivalent, perPeriod: perPeriod,
    progressiveTax: progressiveTax, federalIncomeTax: federalIncomeTax, netPay: netPay,
    cashFlow: cashFlow, percentOf: percentOf, rule503020: rule503020, monthsToGoal: monthsToGoal, annualize: annualize, breakEven: breakEven,
    simpleInterest: simpleInterest, compoundAmount: compoundAmount, apy: apy, fvAnnuity: fvAnnuity, futureValue: futureValue,
    presentValue: presentValue, depositForGoal: depositForGoal, growthTable: growthTable, ruleOf72: ruleOf72, yearsToDouble: yearsToDouble,
    loanPayment: loanPayment, amortize: amortize, totalLoanCost: totalLoanCost, leasePayment: leasePayment, mileageOverage: mileageOverage, depreciatedValue: depreciatedValue,
    monthlyRate: monthlyRate, cardInterest: cardInterest, averageDailyBalance: averageDailyBalance, adbInterest: adbInterest, minimumPayment: minimumPayment, payoff: payoff, multiDebtPayoff: multiDebtPayoff,
    mortgage: mortgage, remainingBalance: remainingBalance, rentVsBuy: rentVsBuy, affordability: affordability, debtToIncome: debtToIncome,
    expectedValue: expectedValue, healthPlanCost: healthPlanCost, claimPayout: claimPayout,
    netPrice: netPrice, paybackYears: paybackYears, careerEarnings: careerEarnings, earningsBy: earningsBy,
    inflate: inflate, purchasingPower: purchasingPower, realReturn: realReturn, cpiAdjust: cpiAdjust, retirementBalance: retirementBalance, nestEggNeeded: nestEggNeeded
  };
})(typeof window !== 'undefined' ? window : globalThis);
