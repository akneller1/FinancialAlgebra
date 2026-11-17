/* Three levels for Financial Algebra (2026-11-17): level counts per skill, the Classroom level codes, the rules for
 * Support and Advanced questions, and an independent recomputation of every new level question from its text. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { course } from '../src/course.js';
import { levelFamilies } from '../financial/content/levels-20261117.mjs';
const root = new URL('../', import.meta.url);
const json = (p) => JSON.parse(readFileSync(new URL(p, root), 'utf8'));
const CODE = { support: 'cp2', standard: 'cp1', advanced: 'honors' };

test('every skill has 16+ Support, 15+ Standard and 16+ Advanced questions', () => {
  for (const u of course.units) {
    const b = json(`financial/banks/${u.id}.json`), c = {};
    for (const q of b.questions) { assert.ok(CODE[q.level], q.id + ' level ' + q.level); (c[q.skillId] = c[q.skillId] || { support: 0, standard: 0, advanced: 0 })[q.level]++; }
    for (const [skill, n] of Object.entries(c)) {
      assert.ok(n.support >= 16 && n.standard >= 15 && n.advanced >= 16, `${skill}: ${JSON.stringify(n)}`);
    }
  }
});

test('Classroom export uses cp2 / cp1 / honors to match each question', () => {
  for (const u of course.units) {
    const ext = new Map(json(`financial/banks/${u.id}.json`).questions.map(q => [q.id, q.level]));
    const cls = json(`question-banks/financial-algebra/${u.id}.json`).questions;
    for (const lv of ['cp2', 'cp1', 'honors']) assert.ok(cls.some(q => q.level === lv), u.id + ' exports ' + lv);
    for (const q of cls) assert.equal(q.level, CODE[ext.get(q.id)], q.id);
  }
});

test('Support questions use whole-dollar amounts; definition checks are Support; open responses are Advanced', () => {
  for (const u of course.units) for (const q of json(`financial/banks/${u.id}.json`).questions) {
    if (/^lv-s-/.test(q.family)) assert.ok(!/\$[\d,]+\.(?!00)\d\d/.test(q.prompt), q.id + ' Support prompt uses cents: ' + q.prompt);   // "$1,150.00" is still whole dollars
    if (q.type === 'vocabulary') assert.equal(q.level, 'support', q.id);
    if (q.format === 'open-response') assert.equal(q.level, 'advanced', q.id);
  }
});

test('every new level question recomputes independently from its text', () => {
  let n = 0;
  for (const u of course.units) {
    const fams = Object.fromEntries((levelFamilies[u.id] || []).map(f => [f.id, f]));
    for (const q of json(`financial/banks/${u.id}.json`).questions.filter(q => /^lv-/.test(q.family))) {
      const f = fams[q.family]; assert.ok(f, 'no family ' + q.family);
      assert.equal(q.level, f.level, q.id);
      const want = f.verify(q.prompt), got = q.numeric.value, tol = Math.max(q.numeric.tolerance ?? 0.01, 0.011);
      assert.ok(Math.abs(want - got) <= tol, `${q.id}: text gives ${want}, key ${got}\n${q.prompt}`);
      n++;
    }
  }
  assert.ok(n >= 600, 'found ' + n);
});
