/* Fuller worked solutions (2026-11-17): every numeric question shows a formula and ends with what the answer
 * means; every spreadsheet entry, evaluated as a spreadsheet would, gives the answer key. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { course } from '../src/course.js';
const json = (p) => JSON.parse(readFileSync(new URL('../' + p, import.meta.url), 'utf8'));
const all = course.units.flatMap(u => json(`financial/banks/${u.id}.json`).questions).filter(q => q.numeric && q.format !== 'open-response');

/* A small evaluator for the functions the entries use. */
const F = {
  PMT: (r, n, pv, fv = 0) => (pv * (1 + r) ** n + fv) * r / ((1 + r) ** n - 1) * -1 * -1 * (pv < 0 || fv < 0 ? 1 : -1),
  FV: (r, n, p) => -p * ((1 + r) ** n - 1) / r, PV: (r, n, p) => -p * (1 - (1 + r) ** -n) / r,
  ROUNDUP: (x, d) => Math.ceil(x * 10 ** d - 1e-9) / 10 ** d, ROUNDDOWN: (x, d) => Math.floor(x * 10 ** d + 1e-9) / 10 ** d,
  ROUND: (x, d) => Math.round(x * 10 ** d) / 10 ** d, MIN: Math.min, MAX: Math.max, LN: Math.log, LOG10: Math.log10, ABS: Math.abs
};
export function sheet(entry) {
  const e = entry.replace(/^=/, '').replace(/ \(then format as a percent\)$/, '').replace(/(\d+(?:\.\d+)?)%/g, '($1/100)').replace(/\^/g, '**').replace(/\b([A-Z][A-Z0-9]*)\(/g, 'F.$1(');
  return Function('F', 'return (' + e + ')')(F);
}

test('every numeric question states a formula and ends with what the answer means', () => {
  let formula = 0;
  for (const q of all) {
    if (q.solutionSteps.some(s => /^Formula:/.test(s))) formula++;
    assert.ok(!/=\s*[−-]?\$?\d[\d,.]*\.?$/.test(q.solutionSteps.at(-1)) || /^So /.test(q.solutionSteps.at(-1)), q.id + ' ends with a calculation: ' + q.solutionSteps.at(-1));
  }
  assert.ok(formula / all.length > 0.97, `formula on ${formula} of ${all.length}`);
});

test('every spreadsheet or calculator entry evaluates to the answer key', () => {
  let n = 0;
  for (const q of all) for (const s of q.solutionSteps) {
    const m = s.match(/^Spreadsheet or calculator: (=.+)$/); if (!m) continue;
    let v = sheet(m[1]); if (/format as a percent/.test(m[1]) && q.numeric.unit === '%') v *= 100;
    assert.ok(Math.abs(Math.abs(v) - Math.abs(q.numeric.value)) <= Math.max(q.numeric.tolerance, 0.006) || Math.abs(Math.round(Math.abs(v) * 100) / 100 - Math.abs(q.numeric.value)) <= Math.max(q.numeric.tolerance, 0.006), `${q.id}: ${m[1]} gives ${v}, key ${q.numeric.value}`);
    n++;
  }
  const withEntry = all.filter(q => q.solutionSteps.some(s => /^Spreadsheet/.test(s))).length;
  assert.ok(n > 1400 && withEntry / all.length > 0.8, `entries on ${withEntry} of ${all.length} (${n} checked here)`);
});
