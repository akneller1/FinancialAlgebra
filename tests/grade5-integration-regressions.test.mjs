import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const root = new URL('../', import.meta.url);
const source = p => fs.readFileSync(new URL(p, root), 'utf8');
test('teacher generators do not offer student links', () => {
  assert.doesNotMatch(source('worksheet-generator/grade5/generators.js'), /copyStudentLink|Copy student link/);
});
test('question metadata response is decoded before distractor lookup', () => {
  const c=source('worksheet-generator/grade5/generators.js');
  assert.match(c, /return response\.json\(\)/);
});
test('legacy student link skill picker remains available', () => {
  const context={location:{href:'https://example.org/grade5.html'},URL,console};
  context.window=context;
  vm.runInNewContext(source('src/grade5-student-links.js'),context);
  const g=context.MK_GRADE5_STUDENT_LINKS;
  assert.equal(typeof g.chooseSkills,'function');
  const url=g.destination({type:'Printable',path:'worksheet-generator/grade5-generators.html?unit=decimal-operations&mode=assessment'},'honors');
  const p=new URL(url).searchParams;
  assert.equal(p.get('mode'),'assessment');
  assert.equal(p.get('student'),'1');
  assert.equal(p.get('level'),'honors');
});
