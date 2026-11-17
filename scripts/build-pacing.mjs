/* Writes financial/pacing/index.html (2026-11-17): an 18-week half-credit semester plan, a 36-week full-year plan
 * and a standards map tagging every skill to the 2021 National Standards for Personal Financial Education
 * (Council for Economic Education and Jump$tart). Built from src/course.js, the Decision Labs, the Spreadsheet
 * Labs, the unit projects and financial/content/standards.mjs, so it changes when the course changes.
 * Run: node scripts/build-pacing.mjs (scripts/build-hub.mjs links to it). */
import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'node:fs';
import { course } from '../src/course.js';
import { SKILL_STANDARDS, MATH_STANDARDS, TOPICS, STANDARDS, SOURCE, describe } from '../financial/content/standards.mjs';
import '../financial/lib/finance.js';
import '../financial/decision-lab/scenarios.js';
const LABS = globalThis.FA_LABS;
const root = new URL('../', import.meta.url), P = p => new URL(p, root).pathname;
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const sheets = JSON.parse(readFileSync(P('financial/spreadsheet-labs/labs.json'), 'utf8')).labs;
const units = [];
for (const [i, u] of course.units.entries()) {
  const projects = existsSync(P(`financial/content/projects/${u.id}.mjs`)) ? (await import(new URL(`financial/content/projects/${u.id}.mjs`, root).href)).default : [];
  units.push({ id: u.id, n: i + 1, name: u.name, skills: u.skills.map((s, k) => ({ id: `${u.id}-skill-${String(k + 1).padStart(2, '0')}`, name: s })), lab: LABS[u.id]?.title, sheet: sheets.find(s => s.unit === u.id), project: projects[0]?.title });
}

/* ---- day-by-day plans ---- */
function semester() {
  const d = [['—', 'Course launch: money goals survey, pre-assessment']];
  for (const u of units) {
    const U = `Unit ${u.n}`;
    u.skills.forEach(s => d.push([U, `Lesson: ${s.name}`]));
    if (u.sheet) d.push([U, `Spreadsheet Lab: ${u.sheet.title.replace(/^Spreadsheet Lab \d: /, '')}`]);
    d.push([U, `Decision Lab: ${u.lab}`]);
    if (['budgeting', 'credit', 'retirement'].includes(u.id) && u.project) { d.push([U, `Project: ${u.project} (day 1)`]); d.push([U, `Project: ${u.project} (day 2)`]); }
    d.push([U, 'Review: Practice Test, Error Analysis, games']); d.push([U, `Unit ${u.n} assessment`]);
    if (u.n === 5) { d.push(['—', 'Midterm review (Units 1–5)']); d.push(['—', 'Midterm exam']); }
  }
  d.push(['—', 'Final review: Showdown across units']); d.push(['—', 'Final review: Practice Tests by level']); d.push(['—', 'Final exam']);
  while (d.length < 90) d.splice(d.length - 3, 0, ['—', 'Flex day: reteach, catch up, or a current-events money story']);
  return d;
}
function fullYear() {
  const d = [['—', 'Course launch: money goals survey'], ['—', 'Pre-assessment and spreadsheet basics']];
  for (const u of units) {
    const U = `Unit ${u.n}`;
    u.skills.forEach(s => { d.push([U, `Lesson: ${s.name}`]); d.push([U, `Practice and modeling: ${s.name}`]); });
    if (u.sheet) { d.push([U, `Spreadsheet Lab: ${u.sheet.title.replace(/^Spreadsheet Lab \d: /, '')} (build)`]); d.push([U, 'Spreadsheet Lab: questions and reflection']); }
    d.push([U, `Decision Lab: ${u.lab}`]);
    if (u.project) for (let k = 1; k <= 3; k++) d.push([U, `Project: ${u.project} (day ${k})`]);
    d.push([U, 'Real-world day: documents, graphs and a current-events story']);
    d.push([U, 'Review: Practice Test, Error Analysis, games']); d.push([U, `Unit ${u.n} assessment`]);
    if (u.n === 5) { d.push(['—', 'Midterm review']); d.push(['—', 'Midterm review: Showdown']); d.push(['—', 'Midterm exam']); }
  }
  for (let k = 1; k <= 5; k++) d.push(['—', `Capstone: plan a first year on your own (day ${k})`]);
  d.push(['—', 'Final review']); d.push(['—', 'Final review: Practice Tests by level']); d.push(['—', 'Final exam']);
  while (d.length < 180) d.splice(d.length - 3, 0, ['—', 'Flex day: reteach, catch up, or a guest speaker']);
  return d;
}
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
function calendar(days, weeks, id, title, intro) {
  if (days.length !== weeks * 5) throw Error(`${id}: ${days.length} days for ${weeks} weeks`);
  let rows = '';
  for (let w = 0; w < weeks; w++) {
    const wk = days.slice(w * 5, w * 5 + 5), unitsIn = [...new Set(wk.map(x => x[0]).filter(x => x !== '—'))];
    rows += `<tr><th scope="row">Week ${w + 1}<span class="pg-u">${esc(unitsIn.join(', ') || 'Course')}</span></th>${wk.map(x => `<td>${esc(x[1])}</td>`).join('')}</tr>`;
  }
  return `<section id="${id}"><h2>${esc(title)}</h2><p>${intro}</p><div class="fa-table-wrap"><table class="fa-table pg-cal"><thead><tr><th scope="col">Week</th>${DAYS.map(d => `<th scope="col">${d}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div></section>`;
}
const sem = semester(), year = fullYear();

/* ---- standards map ---- */
const covered = {};
for (const u of units) for (const s of u.skills) for (const c of SKILL_STANDARDS[s.id]) (covered[c] = covered[c] || new Set()).add(`Unit ${u.n}`);
const mapRows = units.flatMap(u => u.skills.map((s, k) => `<tr>${k ? '' : `<th scope="rowgroup" rowspan="${u.skills.length}">Unit ${u.n}: ${esc(u.name)}</th>`}<td>${esc(s.name)}</td><td>${SKILL_STANDARDS[s.id].map(c => `<span class="pg-std">${esc(describe(c))}</span>`).join('')}</td><td>${(MATH_STANDARDS[s.id] || []).map(esc).join(', ')}</td></tr>`)).join('');
const topicRows = Object.entries(TOPICS).map(([t, name]) => `<tr><th scope="row">${esc(name)}</th><td>${Object.entries(STANDARDS[t]).map(([n, label]) => { const c = `${t} 12-${n}`; return `<span class="pg-std">12-${n} ${esc(label)}: ${covered[c] ? [...covered[c]].join(', ') : '—'}</span>`; }).join('')}</td></tr>`).join('');

const unitList = units.map(u => `<li><a href="../../u/financial-algebra/${u.id}/">Unit ${u.n}: ${esc(u.name)}</a> · ${u.skills.length} skills${u.sheet ? ` · <a href="../spreadsheet-labs/?lab=${u.sheet.slug}">${esc(u.sheet.title)}</a>` : ''}</li>`).join('');
const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Financial Algebra Pacing Guide and Standards Map | Mr. K's Classroom</title>
<meta name="description" content="An 18-week semester plan and a 36-week full-year plan for Financial Algebra, with every skill mapped to the 2021 National Standards for Personal Financial Education.">
<link rel="canonical" href="https://mrksclassroom.com/financial/pacing/">
<link rel="stylesheet" href="../../styles.css">
<link rel="stylesheet" href="../lib/fa.css">
<style>
.pg-cal td,.pg-cal th{vertical-align:top;font-size:.9rem;min-width:120px}.pg-u{display:block;font-weight:400;font-size:.8rem;color:#555}
.pg-std{display:block;margin:2px 0}.pg-toc{display:flex;flex-wrap:wrap;gap:8px}
@media print{nav,.pg-toc,.no-print{display:none}.pg-cal td,.pg-cal th{font-size:8.5pt;min-width:0}section{break-before:page}section:first-of-type{break-before:auto}tr{break-inside:avoid}}
</style>
</head>
<body>
<main class="fa-page" id="main" tabindex="-1">
<nav><a href="../index.html">Financial Algebra</a></nav>
<header><p class="fa-pill">Teacher planning · Financial Algebra</p><h1>Pacing Guide and Standards Map</h1>
<p>Ready-to-use plans for an 18-week half-credit course and a 36-week full-year course, and a map from every skill to the ${esc(SOURCE.title)} from the ${esc(SOURCE.publisher)}. Use it to show that your state's personal finance requirement is covered.</p>
<p class="pg-toc no-print"><a class="fa-btn" href="#semester">Semester (18 weeks)</a><a class="fa-btn" href="#year">Full year (36 weeks)</a><a class="fa-btn" href="#standards">Standards map</a><a class="fa-btn" href="#coverage">Coverage by standard</a><button class="fa-btn" type="button" onclick="print()">Print</button></p></header>
<section><h2>Course at a glance</h2><ul>${unitList}</ul>
<p>Every lesson day has a ready lesson plan in the unit's Lesson Plan generator, at Support, Standard and Advanced levels. Review days use the Practice Test, Error Analysis and games; assessment days use the Assessment generator. The semester plan teaches one lesson per skill; the full-year plan adds a practice and modeling day for each skill, a project in every unit, both days of each Spreadsheet Lab and a capstone.</p></section>
${calendar(sem, 18, 'semester', 'Semester plan: 18 weeks, 90 class days (half credit)', 'One lesson per skill, every Decision Lab and Spreadsheet Lab, three projects (budgeting, credit and retirement), a midterm after Unit 5 and a final exam.')}
${calendar(year, 36, 'year', 'Full-year plan: 36 weeks, 180 class days (one credit)', 'Two days per skill, every lab and unit project, a real-world day in each unit, a midterm after Unit 5 and a five-day capstone.')}
<section id="standards"><h2>Standards map</h2><p>Each skill is tagged to grade 12 standards of the <a href="${esc(SOURCE.url)}">${esc(SOURCE.title)}</a>. Codes give the topic and the grade 12 standard number. The last column lists the Common Core high school math standards each skill practices, for schools that count the course as a math credit.</p>
<div class="fa-table-wrap"><table class="fa-table"><thead><tr><th scope="col">Unit</th><th scope="col">Skill</th><th scope="col">National standards (grade 12)</th><th scope="col">Math (Common Core)</th></tr></thead><tbody>${mapRows}</tbody></table></div></section>
<section id="coverage"><h2>Coverage by standard</h2><p>The grade 12 standards this course teaches, by topic, and the units that teach each one.</p>
<div class="fa-table-wrap"><table class="fa-table"><thead><tr><th scope="col">Topic</th><th scope="col">Standards and units</th></tr></thead><tbody>${topicRows}</tbody></table></div>
<p>Check your state's own standards too: most states base theirs on these national standards but add their own requirements.</p></section>
</main>
</body>
</html>
`;
mkdirSync(P('financial/pacing'), { recursive: true });
writeFileSync(P('financial/pacing/index.html'), html);
console.log(`pacing: semester ${sem.length} days, year ${year.length} days, ${Object.keys(covered).length} standards covered`);
