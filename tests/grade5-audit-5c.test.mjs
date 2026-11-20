// Grade 5 audit (2026-11-19). Batch 5C, source side: #7 per-skill teaching notes, #9 practice tests and reference sheet,
// #15 pacing guide, #16 labs. (#1 Graphing Practice and #19 the release setting are tested in the Classroom repository.)
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import vm from 'node:vm';

const read = (p) => readFileSync(new URL('../' + p, import.meta.url), 'utf8');
const exists = (p) => existsSync(new URL('../' + p, import.meta.url));
const outline = JSON.parse(read('tools/grade5-authoring/outline.json'));
const banks = Object.fromEntries(outline.units.map((u) => [u.id, JSON.parse(read('math5/' + u.id + '.json')).questions]));
const byId = new Map(Object.values(banks).flat().map((q) => [q.id, q]));

test('#7 every skill has its own teaching note', () => {
  const w = {}; w.window = w;
  vm.runInNewContext(read('worksheet-generator/grade5/skill-notes.js'), w);
  const N = w.G5_SKILL_NOTES, bigs = new Set();
  for (const u of outline.units) {
    assert.equal(N[u.id].length, u.skills.length, u.id + ': one note per skill');
    for (const n of N[u.id]) {
      assert.ok(n.big.length > 40 && n.steps.length === 3 && n.watch.length === 2 && n.ask.length > 15, u.id + ': note shape');
      bigs.add(n.big);
    }
  }
  assert.equal(bigs.size, 55, 'no two skills share a key idea');
});

test('#9 two practice tests from the verified bank, no shared items, with checked constructed responses', () => {
  const pt = JSON.parse(read('tools/grade5-authoring/out/practice-tests.json'));
  assert.equal(pt.tests.a.length, 38); assert.equal(pt.tests.b.length, 38);
  assert.equal(new Set([...pt.tests.a, ...pt.tests.b]).size, 76, 'no item in both tests');
  for (const ex of ['a', 'b']) {
    const qs = pt.tests[ex].map((id) => byId.get(id));
    assert.ok(qs.every((q) => q && ['cp1', 'honors'].includes(q.level) && !/-g\d{2}$/.test(q.id)), ex + ': core Standard and Advanced items');
    const doms = new Set(qs.map((q) => q.standards[0].split('.')[1]));
    for (const d of ['OA', 'NBT', 'NF', 'MD', 'G']) assert.ok(doms.has(d), ex + ': covers ' + d);
    assert.equal(pt.cr[ex].length, 2); assert.ok(pt.cr[ex].every((c) => c.parts.length === 4));
    for (const f of ['exam.html', 'key.html', 'exam.pdf', 'teacher-key.pdf']) assert.ok(exists(`math5-practice-test-${ex}/${f}`), ex + ' ' + f);
    const key = read(`math5-practice-test-${ex}/key.html`).replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/[\s/]/g, '');
    for (const id of pt.tests[ex]) {
      const q = byId.get(id);
      if (q.format === 'short-answer') assert.ok(key.includes(String(q.answer).replace(/[\s/]/g, '')), id + ' key in the teacher key');
    }
  }
  execFileSync('python3', ['-c', 'import sys; sys.path.insert(0, "tools/grade5-authoring"); import yearend; yearend.check_cr(); yearend.check_labs()'], { cwd: new URL('..', import.meta.url) });
  assert.ok(exists('math5-reference-sheet/reference-sheet.pdf') && /not the official MCAS reference sheet/.test(read('math5-reference-sheet/index.html')));
});

test('#15 the pacing guide covers every unit in 180 days and ends with the MCAS review', () => {
  const h = read('math5-pacing-guide/index.html');
  for (const u of outline.units) assert.ok(h.includes(u.name.replace(/&/g, '&amp;')), 'pacing guide lists ' + u.name);
  assert.match(h, /MCAS review/); assert.match(h, /–180<\/td>/);
  assert.ok(exists('math5-pacing-guide/pacing-guide.pdf'));
});

test('#16 two labs on the shared tool shell with worksheets and keys, listed in the resource catalog', () => {
  for (const slug of ['decimal-grid-lab', 'scaling-lab']) {
    const h = read(`math5-${slug}/index.html`);
    assert.match(h, /grade5\/tool-shell\.js/); assert.match(h, /challenges:\[/);
    for (const f of ['worksheet.pdf', 'teacher-key.pdf']) assert.ok(exists(`math5-${slug}/${f}`), slug + ' ' + f);
    assert.ok(exists(`thumbs/math5-${slug}.jpg`));
  }
  const cat = read('grade5-resource-catalog.js');
  assert.match(cat, /'decimal-operations':\['place-value-builder','decimal-grid-lab'\]/);
  assert.match(cat, /'scaling-lab'\]/);
  for (const p of ['math5-reference-sheet/reference-sheet.pdf', 'math5-pacing-guide/pacing-guide.pdf', "'math5-practice-test-'+x+'/exam.pdf'"]) assert.ok(cat.includes(p), 'catalog lists ' + p);
});
