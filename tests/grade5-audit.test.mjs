// Grade 5 audit (2026-11-19). Batch 5A: #2 answer forms, #6 reproducible build and file layout, #8 true/false wording,
// #10 singular/plural text, #20 the Support label. (#3, the Classroom grader, is tested in the Classroom repository.)
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import vm from 'node:vm';

const read = (p) => readFileSync(new URL('../' + p, import.meta.url), 'utf8');
const exists = (p) => existsSync(new URL('../' + p, import.meta.url));
const units = readdirSync(new URL('../math5/', import.meta.url)).filter((f) => f.endsWith('.json'));
const all = units.flatMap((f) => JSON.parse(read('math5/' + f)).questions);
const text = (q) => [q.prompt, typeof q.answer === 'string' ? q.answer : JSON.stringify(q.answer), ...(q.solutionSteps || []),
  ...(q.options || []).map((o) => o.text), ...(q.parts || []).flatMap((p) => [p.prompt, p.answer]), q.diagram?.spec?.alt || ''].join(' \n ');

function matcher() {
  const g = { document: {}, location: { search: '' }, URLSearchParams };
  g.window = g; vm.createContext(g);
  vm.runInContext(read('worksheet-generator/grade5/g5-core.js'), g);
  return g.G5.matches;
}

test('#2 the Grade 5 checker requires the form a prompt asks for, and accepts equal forms elsewhere', () => {
  const M = matcher();
  const cases = [
    ['4/6', '2/3', 'Write 10/15 in simplest form.', false], ['2/3', '2/3', 'Write 10/15 in simplest form.', true],
    ['3/2', '1 1/2', 'Write 6/4 in simplest form.', true], ['6/4', '1 1/2', 'Write 6/4 in simplest form.', false],
    ['1 2/4', '1 1/2', 'Write 6/4 in simplest form.', false], ['0.75', '3/4', 'Write 6/8 in simplest form.', false],
    ['17/4', '4 1/4', 'Write the answer as a mixed number.', false], ['4 1/4', '4 1/4', 'Write the answer as a mixed number.', true],
    ['6/8', '3/4', 'What is 1/2 + 1/4?', true], ['0.75', '3/4', 'What is 1/2 + 1/4?', true],
    ['>', 'greater than', '', true], ['less than', '<', '', true], ['< 1', 'less than 1', '', true], ['less', 'less than 1', '', false],
    ['90 remainder 2', '90 R 2', '', true], ['90r2', '90 R 2', '', true], ['90 R 3', '90 R 2', '', false],
    ['x axis', 'the x‑axis', '', true], ['y-axis', 'the x‑axis', '', false],
    ['5 ft 3 in', '5 feet 3 inches', '', true], ['32 cu units', '32 cubic units', '', true], ['32 square units', '32 cubic units', '', false],
    ['4 lb', '4 pounds', '', true], ['4 oz', '4 pounds', '', false], ['3,4', '(3, 4)', '', true]];
  for (const [t, k, p, want] of cases) assert.equal(M(t, k, p), want, `typed ${t}, key ${k}, prompt ${p}`);
  for (const q of all) {
    if (q.format === 'short-answer') assert.ok(M(q.answer, q.answer, q.prompt), q.id + ' key accepted: ' + q.answer);
    for (const p of q.parts || []) assert.ok(M(p.answer, p.answer, p.prompt), q.id + ' part accepted: ' + p.answer);
  }
  for (const f of ['worksheet-generator/grade5/g5-core.js', 'worksheet-generator/grade5/understanding-check.js'])
    assert.ok(!/matches\((?:inp|input|x)\.value, p\.(?:answer|parts\[i\]\.answer)\)/.test(read(f)), f + ' passes the prompt to the checker');
});

test('#6 the bank, diagrams and checks live where the build writes them', () => {
  assert.ok(read('tools/grade5-authoring/build.py').includes('bdir = os.path.join(ROOT, COURSE_ID)'), 'build writes math5/');
  assert.ok(read('tools/grade5-authoring/build.py').includes('PYTHONHASHSEED'), 'build is deterministic');
  let figs = 0;
  for (const q of all.filter((q) => q.diagram)) {
    figs++;
    const src = q.diagram.spec.src;
    assert.match(src, new RegExp(`^question-banks/assets/math5/[a-z-]+/${q.id}\\.png$`), q.id + ' diagram path');
    assert.ok(exists(src), q.id + ' diagram file');
  }
  assert.ok(figs >= 900, figs + ' diagrams');
  assert.equal(readdirSync(new URL('../', import.meta.url)).filter((f) => /^m5-.*\.png$/.test(f)).length, 0, 'no loose Grade 5 diagrams at the root');
  assert.ok(!read('.github/workflows/validate.yml').includes('question-banks/math5'), 'CI reads the published banks');
  assert.match(read('.github/workflows/validate.yml'), /G5_NODRAW=1 python3 tools\/grade5-authoring\/build\.py[\s\S]{0,80}git diff --exit-code -- math5/, 'CI checks that a rebuild reproduces the bank');
});

test('#8 true/false items name the problem and ask a question', () => {
  const tf = all.filter((q) => /^Is this answer correct\?\nProblem: /.test(q.prompt));
  assert.ok(tf.length >= 150, tf.length + ' true/false items');
  assert.ok(!all.some((q) => q.prompt.startsWith('True or false?')), 'no "True or false? 24 + 13.5" fragments');
  for (const q of tf) assert.match(q.prompt.split('\n')[1], /[.?!)]$/, q.id + ' problem is a sentence: ' + q.prompt.split('\n')[1]);
});

test('#10 one of a thing is singular', () => {
  for (const q of all) {
    const m = /(?<![\d.,/])(?<!\d )\b1 (cubes|layers|rows|columns|pieces|inches|feet|units|tens|hundredths|tenths|cubic units|square units)\b|\bthere are 1 [a-z]/.exec(text(q));
    assert.equal(m, null, q.id + ': ' + (m && m[0]));
  }
});

test('#20 the CP2 level is called Support', () => {
  for (const f of ['src/grade5-site.js', 'src/grade5-student-links.js', 'worksheet-generator/grade5/g5-core.js', 'worksheet-generator/grade5/generators-core.js',
    'worksheet-generator/grade5/generators.js', 'tools/grade5-authoring/projects/projects.py', 'tools/grade5-authoring/g5lib.py'])
    assert.ok(!/Remedial/.test(read(f)), f);
  for (const d of readdirSync(new URL('../', import.meta.url)).filter((f) => /^math5-project-/.test(f)))
    assert.ok(!/Remedial/.test(read(d + '/index.html')), d);
});
