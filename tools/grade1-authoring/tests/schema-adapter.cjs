// Validate every math1 bank (practice + checks) with the site's own question-bank-adapter.js.
const fs = require('fs'), path = require('path'), vm = require('vm');
const [adapterPath, root] = process.argv.slice(2);
const outline = JSON.parse(fs.readFileSync(path.join(root, 'course-outlines/grade1.json'), 'utf8'));
const skills = {}; outline.units.forEach(u => skills[u.id] = u.skills);
globalThis.MK_COURSE_CATALOG = { getSkillRecords: (c, u) => c === 'math1' ? (skills[u] || []).map((n, i) => ({ id: u + '-skill-' + String(i + 1).padStart(2, '0'), name: n, index: i + 1 })) : [] };
vm.runInThisContext(fs.readFileSync(adapterPath, 'utf8'));
let bad = 0, n = 0, files = 0;
for (const sub of ['', 'checks']) {
  for (const u of outline.units) {
    const f = path.join(root, 'question-banks/math1', sub, u.id + '.json');
    const bank = JSON.parse(fs.readFileSync(f, 'utf8'));
    const r = MK_QUESTION_BANKS.validate(bank); files++; n += bank.questions.length;
    if (!r.ok) { bad++; console.log(f, r.errors.slice(0, 5)); }
    const reg = MK_QUESTION_BANKS.register(JSON.parse(JSON.stringify(bank)), { verified: true });
    if (sub === '' && !reg.ok) { bad++; console.log('register', u.id, reg.errors.slice(0, 3)); }
  }
}
const sel = MK_QUESTION_BANKS.select({ courseId: 'math1', unitId: 'count-120', level: 'honors', formats: ['multiple-choice'] });
console.log(`adapter.validate: ${files} files, ${n} questions, ${bad} failing; select(honors MC, count-120) -> ${sel.length}`);
process.exit(bad ? 1 : 0);
