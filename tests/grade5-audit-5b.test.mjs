// Grade 5 audit (2026-11-19). Batch 5B: #4 Advanced multi-step items, #5 constructed-response tasks, #11 vocabulary,
// #12 decimal point and powers of ten, #13 line-plot fair share, #14 figures for every skill, #17 thin families.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import vm from 'node:vm';

const read = (p) => readFileSync(new URL('../' + p, import.meta.url), 'utf8');
const banks = readdirSync(new URL('../math5/', import.meta.url)).filter((f) => f.endsWith('.json')).map((f) => JSON.parse(read('math5/' + f)));
const all = banks.flatMap((b) => b.questions);
const added = all.filter((q) => /-g\d{2}$/.test(q.id));
const family = (q) => (/family: ([a-z0-9_]+)/.exec(q.sourceNotes || '') || [])[1] || '';
const skills = [...new Set(all.map((q) => q.skillId))];

test('#4 every skill has at least 2 Advanced multi-step items with 2 or more worked steps', () => {
  assert.equal(skills.length, 55);
  for (const s of skills) {
    const ms = added.filter((q) => q.skillId === s && q.level === 'honors' && family(q).startsWith('ms_'));
    assert.ok(ms.length >= 2, s + ': ' + ms.length + ' multi-step items');
    for (const q of ms) assert.ok(q.solutionSteps.length >= 2, q.id + ': multi-step means at least 2 steps');
  }
});

test('#5 every unit has 2 connected constructed-response tasks (Standard and Advanced), 4 parts each', () => {
  for (const b of banks) {
    const cr = added.filter((q) => q.id.startsWith('m5-') && b.questions.includes(q) && q.format === 'open-response');
    assert.equal(cr.length, 2, b.unitId + ' constructed-response tasks');
    assert.deepEqual(cr.map((q) => q.level).sort(), ['cp1', 'honors'], b.unitId + ' levels');
    for (const q of cr) {
      assert.equal(q.parts.length, 4, q.id);
      assert.ok(q.parts.every((p) => p.prompt && p.answer), q.id + ' parts have prompts and answers');
    }
  }
});

test('#12 and #13 the place-chart shift (5.NBT.A.2) and line-plot fair share (5.MD.B.2) items exist with figures', () => {
  const shift = added.filter((q) => family(q) === 'pt_shift'), fair = added.filter((q) => family(q) === 'lp_fair_share');
  assert.ok(shift.length >= 6 && shift.every((q) => q.standards.includes('5.NBT.A.2') && q.diagram), 'place-chart items');
  assert.ok(fair.length >= 6 && fair.every((q) => q.standards.includes('5.MD.B.2') && q.diagram), 'fair-share items');
});

test('#14 every skill has at least one figure', () => {
  for (const s of skills) assert.ok(all.some((q) => q.skillId === s && q.diagram), s + ' has a figure');
});

test('#17 the verifier finds no thin skill-levels', () => {
  const checks = readdirSync(new URL('../tools/grade5-authoring/out/', import.meta.url)).filter((f) => f.endsWith('.checks.json'));
  assert.equal(checks.length, 11);
  // every skill and level draws from at least 2 families in the core bank plus the added items
  for (const s of skills) for (const l of ['cp2', 'cp1', 'honors']) {
    const fams = new Set(all.filter((q) => q.skillId === s && q.level === l).map(family));
    assert.ok(fams.size >= 2, `${s} ${l}: ${fams.size} families`);
  }
});

test('#11 the core Grade 5 terms are in the vocabulary games, flashcards and lesson generator', () => {
  const w = { MKVOCAB_BANKS: {} }; w.window = w;
  vm.runInNewContext(read('worksheet-generator/vocabulary-data-middle-grades.js'), w);
  const terms = Object.entries(w.MKVOCAB_BANKS).filter(([k]) => k.startsWith('math5-')).flatMap(([, v]) => v.split(';').map((r) => r.split('|')[0]));
  assert.ok(terms.length >= 130, terms.length + ' terms');
  for (const t of ['improper fraction', 'benchmark fraction', 'parallelogram', 'rhombus', 'trapezoid', 'isosceles triangle', 'scalene triangle',
    'equilateral triangle', 'edge', 'face', 'vertex', 'rectangular prism', 'numerical expression', 'brackets [ ]', 'braces { }',
    'customary units', 'metric units', 'unlike denominators', 'first quadrant', 'measurement data'])
    assert.ok(terms.includes(t), 'missing term ' + t);
  assert.ok(!terms.includes('volume-three-dimensional-figures') && terms.includes('volume'), 'the volume term is named volume');
  const vol = JSON.parse(read('worksheet-generator/grade5/flashcards/volume-three-dimensional-figures.json')).cards;
  assert.ok(vol.some((c) => c.front === 'Volume') && !vol.some((c) => /three.dimensional.figures/i.test(c.front)), 'flashcard front reads Volume');
  const g = {}; g.window = g;
  vm.runInNewContext(read('worksheet-generator/grade5/generators-content.js'), g);
  const C = g.G5_GENERATOR_CONTENT.units || g.G5_GENERATOR_CONTENT;
  const cs = C['classifying-two-dimensional-figures'].vocabulary.map((v) => v.term);
  for (const t of ['parallelogram', 'rhombus', 'trapezoid', 'rectangle', 'square']) assert.ok(cs.includes(t), 'lesson generator term ' + t);
  // the definitions agree with the unit's questions: exactly one pair of parallel sides, exactly two equal sides
  const defs = JSON.stringify(C) + read('worksheet-generator/vocabulary-data-middle-grades.js');
  assert.ok(!/trapezoid[^}|]*at least one pair/i.test(defs) && !/isosceles[^}|]*at least 2/i.test(defs), 'definitions match the bank');
});
