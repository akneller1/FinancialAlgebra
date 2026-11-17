/* Spreadsheet Labs, pacing guide and standards map (2026-11-17). */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { course } from '../src/course.js';
import { spreadsheetFamilies } from '../financial/content/spreadsheet-20261117.mjs';
import { SKILL_STANDARDS, TOPICS, STANDARDS } from '../financial/content/standards.mjs';
const root = new URL('../', import.meta.url), read = p => readFileSync(new URL(p, root), 'utf8'), json = p => JSON.parse(read(p));

test('each lab has a template, steps with formulas, a check line and nine verified questions at three levels', () => {
  const labs = json('financial/spreadsheet-labs/labs.json').labs;
  assert.deepEqual(labs.map(l => l.slug), ['budget', 'amortization', 'pmt-fv']);
  for (const l of labs) {
    assert.ok(statSync(new URL('financial/spreadsheet-labs/' + l.file, root)).size > 4000, l.file);
    assert.ok(l.steps.length >= 6 && l.steps.some(s => /=[A-Z]+\(/.test(s)), l.slug + ' steps');
    assert.match(l.check, /^Check your sheet/);
    const fam = spreadsheetFamilies[l.unit].find(f => f.id === l.family), qs = json(`financial/banks/${l.unit}.json`).questions.filter(q => q.family === l.family);
    assert.equal(qs.length, 9, l.slug);
    for (const lv of ['support', 'standard', 'advanced']) assert.equal(qs.filter(q => q.level === lv).length, 3, l.slug + ' ' + lv);
    for (const q of qs) assert.ok(Math.abs(fam.verify(q) - q.numeric.value) <= 0.011, `${q.id}: ${fam.verify(q)} vs ${q.numeric.value}`);
  }
});

test('the lab page reads labs.json and the unit bank, and the manifest lists each lab on its unit', () => {
  const page = read('financial/spreadsheet-labs/index.html'), man = json('financial/resources.json');
  assert.match(page, /fetch\('labs\.json'\)/); assert.match(page, /'\.\.\/banks\/' \+ lab\.unit/);
  for (const l of json('financial/spreadsheet-labs/labs.json').labs) assert.ok(man.units.find(u => u.unitId === l.unit).resources.spreadsheetLabs.some(x => x.path.endsWith('lab=' + l.slug)), l.slug);
});

test('every skill maps to valid national standards, and the bank carries them', () => {
  for (const u of course.units) {
    const b = json(`financial/banks/${u.id}.json`);
    u.skills.forEach((_, k) => {
      const id = `${u.id}-skill-${String(k + 1).padStart(2, '0')}`, codes = SKILL_STANDARDS[id];
      assert.ok(codes && codes.length, id);
      for (const c of codes) { const [t, n] = c.split(' 12-'); assert.ok(TOPICS[t] && STANDARDS[t][n], c); }
      assert.equal(b.skills[k].standards.length, codes.length, id);
    });
  }
});

test('pacing guide: 18 weeks and 36 weeks of five days, every unit scheduled with its assessment', () => {
  const h = read('financial/pacing/index.html');
  const sem = h.slice(h.indexOf('id="semester"'), h.indexOf('id="year"')), year = h.slice(h.indexOf('id="year"'), h.indexOf('id="standards"'));
  assert.equal((sem.match(/<th scope="row">Week /g) || []).length, 18);
  assert.equal((year.match(/<th scope="row">Week /g) || []).length, 36);
  for (const part of [sem, year]) for (let n = 1; n <= course.units.length; n++) assert.match(part, new RegExp(`Unit ${n} assessment`));
  for (const u of course.units) for (const s of u.skills) assert.ok(h.includes(s.replace(/&/g, '&amp;').replace(/'/g, '&#39;')), s);
});
