/* Algebra modeling with graphs (2026-11-17): every question recomputes from the numbers in its own prompt,
 * caption and marked points; every unit has graph questions at all three levels; the renderer draws an SVG. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { course } from '../src/course.js';
import { modelingFamilies } from '../financial/content/modeling-20261117.mjs';
import '../financial/lib/finance.js';
import '../financial/lib/render.js';
const json = (p) => JSON.parse(readFileSync(new URL('../' + p, import.meta.url), 'utf8'));

test('every modeling question recomputes from what the student sees', () => {
  let n = 0;
  for (const [unit, fams] of Object.entries(modelingFamilies)) for (const f of fams) {
    const qs = json(`financial/banks/${unit}.json`).questions.filter(q => q.family === f.id);
    assert.equal(qs.length, f.count, f.id);
    for (const q of qs) {
      const v = f.verify(q), tol = Math.max(q.numeric.tolerance, 0.011);
      assert.ok(Math.abs(v - q.numeric.value) <= tol, `${q.id}: key ${q.numeric.value}, recomputed ${v}\n${q.prompt}`);
      n++;
    }
  }
  assert.equal(n, 90);
});

test('all ten units have graph questions at Support, Standard and Advanced, with full worked solutions', () => {
  for (const u of course.units) {
    const qs = json(`financial/banks/${u.id}.json`).questions.filter(q => /^lv-m-/.test(q.family));
    for (const lv of ['support', 'standard', 'advanced']) assert.ok(qs.some(q => q.level === lv), u.id + ' ' + lv);
    for (const q of qs) {
      assert.equal(q.type, 'modeling'); assert.ok(q.scenario.graph.series.length >= 1 && q.scenario.graph.caption, q.id);
      const s = q.solutionSteps.join('\n');
      assert.match(s, /Formula:/, q.id); assert.match(s, /Spreadsheet:/, q.id); assert.match(q.solutionSteps.at(-1), /^So /, q.id);
    }
  }
});

test('graphs render as labeled SVG with one polyline per series', () => {
  const q = json('financial/banks/borrowing.json').questions.find(q => /^lv-m-/.test(q.family));
  const h = globalThis.FA_RENDER.question(q, { teacher: true });
  assert.match(h, /<svg class="fa-g-svg" viewBox="0 0 560 320" role="img" aria-label="[^"]+"/);
  assert.equal((h.match(/<polyline/g) || []).length, q.scenario.graph.series.length);
  assert.match(h, /Algebra modeling/);
});
