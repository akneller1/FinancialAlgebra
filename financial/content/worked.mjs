/* Fuller worked solutions (2026-11-17). Every numeric question's solution should show
 *   1. the formula, 2. the numbers substituted in, 3. a calculator or spreadsheet entry, 4. what the answer means.
 * Most questions already show the substitution. This module adds what is missing:
 *   - "Formula:" from FAMILY_FORMULA, else from a formula the question or its steps already state in words;
 *   - "Spreadsheet:" built from the step whose arithmetic produces the answer, and only when re-evaluating that
 *     expression gives the answer key (so the entry is always right);
 *   - "So …": the family's own closing interpretation when it has one, else MEANING[skill] with the answer.
 * Applied in scripts/build-banks.mjs; tests/fa-worked-solutions.test.mjs checks the result. */
const NUM = /[−-]?\$?\d[\d,]*(?:\.\d+)?%?/g;
const clean = (s) => String(s).replace(/\*\*(.+?)\*\*/g, '$1');
/* Turn a displayed expression into a spreadsheet formula, or null if it has words or unknowns. */
export function toSheet(expr) {
  let e = clean(expr).trim().replace(/\[\[([^\[\]]+?)\|\|([^\[\]]+?)\]\]/g, '(($1)/($2))')
    .replace(/(?:the\s+)?smaller of\s+(\$?[\d,.]+%?)\s+and\s+(\$?[\d,.]+%?)/gi, 'min($1,$2)').replace(/(?:the\s+)?larger of\s+(\$?[\d,.]+%?)\s+and\s+(\$?[\d,.]+%?)/gi, 'max($1,$2)');
  e = e.replace(/\b(min|max)\(/gi, (m, f) => f.toLowerCase() + '(');
  if (/[A-Za-z]/.test(e.replace(/\b(?:ln|log)(?=\s*\(|\s+\d)/g, '').replace(/\b(?:min|max)\(/g, ''))) return null;
  e = e.replace(/\b(ln|log)\s+(\d+(?:\.\d+)?)/g, '$1($2)');
  if (!/[×÷+\-−*/^⁰¹²³⁴⁵⁶⁷⁸⁹(]/.test(e.replace(/^[−-]/, ''))) return null;
  e = e.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]+/g, (m) => '^' + [...m].map(c => '⁰¹²³⁴⁵⁶⁷⁸⁹'.indexOf(c)).join('')).replace(/[−–]/g, '-').replace(/×/g, '*').replace(/÷/g, '/').replace(/\$/g, '').replace(/(\d),(?=\d{3}\b)/g, '$1')
    .replace(/(\d+(?:\.\d+)?)%/g, '($1/100)').replace(/\s+/g, '').replace(/(\d|\))\(/g, '$1*(').replace(/\)(\d)/g, ')*$1');
  if (!/^[\d.+\-*/()^,a-z]+$/.test(e) || /[a-z]/.test(e.replace(/\b(?:ln|log|min|max)\(/g, '')) || !/[*/+\-^]/.test(e.replace(/^-/, ''))) return null;
  return e;
}
export function evalSheet(e) { try { const js = e.replace(/\^/g, '**').replace(/\bln\(/g, 'Math.log(').replace(/\blog\(/g, 'Math.log10(').replace(/\bmin\(/g, 'Math.min(').replace(/\bmax\(/g, 'Math.max('); return Function('"use strict";return (' + js + ')')(); } catch { return NaN; } }
/* The tidy display version: =1240+0.12*(38500-12400) */
const pretty = (e) => '=' + e.replace(/\bmin\(/g, 'MIN(').replace(/\bmax\(/g, 'MAX(').replace(/\bln\(/g, 'LN(').replace(/\blog\(/g, 'LOG10(').replace(/\(\((\d+(?:\.\d+)?)\/100\)\)/g, '$1%').replace(/\((\d+(?:\.\d+)?)\/100\)/g, '$1%').replace(/\(\(([^()]+)\)\/\(([^()]+)\)\)/g, '($1)/($2)').replace(/(?<![A-Za-z0-9])\((\d+(?:\.\d+)?)\)/g, '$1');
export function sheetEntry(q) {
  const target = q.numeric.value, unit = q.numeric.unit, tol = Math.max(q.numeric.tolerance || 0, 0.006);
  const ok = (v) => [1, ...(unit === '%' ? [100] : [])].find(k => Math.abs(v * k - target) <= tol || Math.abs(Math.round(v * k * 100) / 100 - target) <= tol);
  const cands = [], results = [];
  for (const s of q.solutionSteps) for (const part of clean(s).split(/[;:](?:\s|$)|\.(?:\s|$)|→/)) {
    const sides = part.split(/\s=\s|≈|≥|≤/).map(x => x.trim()).filter(Boolean);
    for (let i = 0; i < sides.length; i++) {
      let side = sides[i];
      /* "+ $1,000 = $28,000" continues the previous result. */
      if (/^[+−×÷-]\s*\$?\d/.test(side) && results.length) side = '(' + results[results.length - 1] + ')' + side;
      const e = /^\(/.test(side) && results.length && side.startsWith('(' + results[results.length - 1]) ? (toSheet(side.slice(results[results.length - 1].length + 2)) !== null || true ? toSheet('(' + side.slice(1, results[results.length - 1].length + 1).replace(/\*/g, '×').replace(/\//g, '÷') + ')' + side.slice(results[results.length - 1].length + 2)) : null) : toSheet(/^(?:ln|log|min|max)\b/i.test(side) ? side : side.replace(/^[^\d$([−-]*/, '')); if (!e) continue;
      cands.push(e);
      const shown = sides[i + 1] && sides[i + 1].match(/^[−-]?\$?([\d,]+(?:\.\d+)?)/);
      if (shown) { const v = evalSheet(e), sv = Number(shown[1].replace(/,/g, '')) * (/^[−-]/.test(sides[i + 1]) ? -1 : 1); if (Math.abs(v - sv) < 0.011 * Math.max(1, Math.abs(sv) / 1000)) results.push(e); }
    }
  }
  for (const e of cands.slice().reverse()) { const v = evalSheet(e); if (Number.isFinite(v)) { const k = ok(v); if (k) return pretty(e) + (k === 100 ? ' (then format as a percent)' : ''); } }
  /* The answer may combine two earlier results: a difference or a total. */
  const R = results.slice(-4), wrap = (e) => /^[\d.]+$/.test(e) ? e : '(' + e + ')';
  for (let a = R.length - 1; a >= 0; a--) for (let b = R.length - 1; b >= 0; b--) if (a !== b) {
    for (const [op, f] of [['-', (x, y) => x - y], ['+', (x, y) => x + y]]) { if (op === '+' && a < b) continue; const v = f(evalSheet(R[a]), evalSheet(R[b])); if (ok(v) === 1) return pretty(wrap(R[a]) + op + wrap(R[b])); }
  }
  if (R.length > 2) { const v = R.reduce((t, e) => t + evalSheet(e), 0); if (ok(v) === 1) return pretty(R.map(wrap).join('+')); }
  /* A total of the last few expressions (e.g. three years of rent). */
  for (let k = 2; k <= Math.min(6, cands.length); k++) { const last = cands.slice(-k), v = last.reduce((t, e) => t + evalSheet(e), 0); if (ok(v) === 1) return pretty(last.map(wrap).join('+')); }
  /* Growth factors: a percent answer from (factor − 1). */
  if (unit === '%') for (const e of cands.slice().reverse()) { const v = evalSheet(e); if (Number.isFinite(v) && Math.abs((v - 1) * 100 - target) <= tol) return pretty(wrap(e) + '-1') + ' (then format as a percent)'; }
  /* Two amounts the steps show: one minus the other. */
  const lits = [...new Set([...clean(q.solutionSteps.join(' ')).matchAll(/\$([\d,]+(?:\.\d+)?)/g)].map(m => m[1].replace(/,/g, '')))].slice(0, 16);
  const T = 0.006, far = (x) => Math.abs(x - target) > 0.5 && Math.abs(x) > 0.5;
  for (const a of lits) for (const b of lits) if (a !== b && far(+a) && far(+b) && Math.abs(Number(a) - Number(b) - target) <= T && target > 0) return '=' + a + '-' + b;
  for (const e of R.slice(-2)) for (const a of lits) { const v = evalSheet(e); if (!far(v) || !far(+a)) continue; if (Math.abs(Number(a) - v - target) <= T) return pretty(a + '-' + wrap(e)); if (Math.abs(v - Number(a) - target) <= T) return pretty(wrap(e) + '-' + a); }
  /* Rounded answers: a count rounded up or down, or dollars rounded down to stay within a budget. */
  const text = q.solutionSteps.join(' ');
  for (const e of cands.slice().reverse()) { const v = evalSheet(e); if (!Number.isFinite(v)) continue;
    if ((/round(?:ed)? up|→/i.test(text) || unit === 'count') && Math.ceil(v - 1e-9) === target && Math.abs(v - target) < 1) return '=ROUNDUP(' + pretty(e).slice(1) + ',0)';
    if (/round(?:ed)? down/i.test(text) && Math.floor(v + 1e-9) === target && Math.abs(v - target) < 1) return '=ROUNDDOWN(' + pretty(e).slice(1) + ',0)'; }
  return financeEntry(q, ok);
}
/* Loan and savings questions whose steps name the rate, term and amount: try the spreadsheet's own functions and
   keep the one that reproduces the answer key. */
function financeEntry(q, ok) {
  if (!(q.numeric.value > 0)) return null;
  const text = clean(q.prompt + ' ' + q.solutionSteps.join(' ') + ' ' + JSON.stringify(q.scenario || ''));
  const nums = [...new Set([...text.matchAll(/\$?(\d[\d,]*(?:\.\d+)?)(%?)/g)].map(m => Number(m[1].replace(/,/g, '')) / (m[2] ? 100 : 1)))];
  const rates = nums.filter(x => x > 0 && x < 0.4), terms = nums.filter(x => Number.isInteger(x) && x >= 2 && x <= 600), amts = nums.filter(x => x >= 10);
  const PMT = (i, n, pv, fv = 0) => (pv * (1 + i) ** n + fv) * i / ((1 + i) ** n - 1), FV = (i, n, d) => d * ((1 + i) ** n - 1) / i, PV = (i, n, d) => d * (1 - (1 + i) ** -n) / i;
  const f = (x) => String(Math.round(x * 1e6) / 1e6);
  for (const r of rates) for (const n of terms) for (const a of amts) {
    const tries = [[PMT(r / 12, n, a), `=PMT(${f(r)}/12,${n},-${f(a)})`], [FV(r / 12, n, a), `=FV(${f(r)}/12,${n},-${f(a)})`], [PV(r / 12, n, a), `=PV(${f(r)}/12,${n},-${f(a)})`], [PMT(r / 12, n, 0, a), `=PMT(${f(r)}/12,${n},0,-${f(a)})`]];
    for (const [v, e] of tries) { if (!Number.isFinite(v)) continue; if (ok(v) === 1) return e; if (Math.floor(v) === q.numeric.value && /round down/i.test(q.solutionSteps.join(' '))) return '=ROUNDDOWN(' + e.slice(1) + ',0)'; }
  }
  return null;
}
/* A formula the question or steps already state with words or letters on both sides, e.g. "I = Prt". */
const rhs0 = (r) => (r.match(/\(/g) || []).length > (r.match(/\)/g) || []).length - 1 && false;
export function statedFormula(q) {
  const texts = [...clean(q.prompt).split(/(?<=[.?])\s+/), ...q.solutionSteps.map(clean)];
  for (const t of texts) for (const piece of t.split(/[.;]\s|:\s|,\s(?=[a-z])/)) {
    const m = piece.match(/^\s*(?:Use\s+|So\s+|Solve\s+)?([A-Za-z][\w’' &/-]{0,38}?)\s=\s(.+?)\s*$/);
    if (!m || /\$/.test(piece) || !/[A-Za-z]{1,}/.test(m[2]) || /\d{3,}/.test(piece)) continue;
    const rhs = m[2].replace(/\s*[=≈].*$/, '').replace(/[.)]+$/, (x) => (rhs0(m[2]) ? x : '')).replace(/\.$/, '');
    if (!/[A-Za-z]/.test(rhs) || /^\d/.test(rhs) || rhs.length > 90 || (rhs.match(/\(/g) || []).length !== (rhs.match(/\)/g) || []).length || (rhs.match(/\[\[/g) || []).length !== (rhs.match(/\]\]/g) || []).length) continue;
    return (m[1] + ' = ' + rhs).trim();
  }
  return null;
}
const isMeaning = (s) => !/=\s*[−-]?\$?\d/.test(s) && !/^\$?[\d,.]+\s*[×÷+−]/.test(s) && /[a-z]{4,}/.test(s);
export function enrich(q, FAMILY_FORMULA, MEANING) {
  if (!q.numeric || q.format === 'open-response' || /^lv-[mx]-/.test(q.family)) return q;
  const steps = q.solutionSteps.slice(), has = (re) => steps.some(s => re.test(s));
  const endsWithMeaning = isMeaning(steps[steps.length - 1]) && !/^(Correct result|Mistake)/.test(steps[steps.length - 1]);
  if (!has(/^Formula:/)) { const f = FAMILY_FORMULA[q.family] || statedFormula(q); if (f) steps.splice(/^Mistake:/.test(steps[0]) ? 1 : 0, 0, 'Formula: ' + f.replace(/\.$/, '') + '.'); }
  if (!has(/^(Spreadsheet|Calculator)/)) { const e = sheetEntry(q); if (e) steps.splice(steps.length - (endsWithMeaning ? 1 : 0), 0, 'Spreadsheet or calculator: ' + e); }
  if (!endsWithMeaning) { const m = MEANING[q.skillId]; if (m) steps.push(m.replace('{A}', q.answer)); }
  return { ...q, solutionSteps: steps };
}
