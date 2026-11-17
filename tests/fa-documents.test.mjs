/* Real-world documents (2026-11-17): every new document question recomputes from the numbers shown in its own
 * document and prompt; every new document kind renders at all three levels and is labeled fictional. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { documentFamilies } from '../financial/content/documents-20261117.mjs';
const json = (p) => JSON.parse(readFileSync(new URL('../' + p, import.meta.url), 'utf8'));
const KINDS = ['w2', 'form-1040', 'utility-bill', 'credit-report', 'loan-disclosure', 'auto-declarations', 'explanation-of-benefits', 'lease-summary', 'fund-fact-sheet', 'benefits-summary'];

test('every new document question recomputes from its own document', () => {
  let n = 0;
  for (const [unit, fams] of Object.entries(documentFamilies)) {
    const qs = json(`financial/banks/${unit}.json`).questions;
    for (const f of fams) {
      const mine = qs.filter(q => q.family === f.id);
      assert.equal(mine.length, f.count, f.id);
      for (const q of mine) {
        const v = f.verify(q), tol = Math.max(q.numeric.tolerance, 0.011);
        assert.ok(Number.isFinite(v), q.id + ' verify gave ' + v);
        assert.ok(Math.abs(v - q.numeric.value) <= tol, `${q.id}: answer ${q.numeric.value}, recomputed ${v}`);
        n++;
      }
    }
  }
  assert.equal(n, 90);
});

test('each new kind appears at Support, Standard and Advanced, is fictional, and is not a game item', () => {
  const all = Object.keys(documentFamilies).flatMap(u => json(`financial/banks/${u}.json`).questions).filter(q => /^lv-d-/.test(q.family));
  for (const k of KINDS) {
    const of = all.filter(q => q.scenario.document.kind === k);
    for (const lv of ['support', 'standard', 'advanced']) assert.ok(of.some(q => q.level === lv), k + ' at ' + lv);
  }
  for (const q of all) {
    assert.ok(q.scenario.document.notes.some(t => /Fictional/.test(t)), q.id);
    assert.equal(q.gameEligible, false, q.id);
    assert.equal(q.type, 'document', q.id);
  }
});
