/* Builds printable resources: cheat sheets (HTML + PDF) and unit projects (student packet, teacher guide, slides data, landing page).
 * PDFs via Playwright (Chromium). DOCX/PPTX are produced afterwards by scripts/build_office.py from dist JSON.
 * Usage: node scripts/build-print.mjs [unitId ...] */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { createRequire } from 'node:module';
const { chromium } = createRequire(new URL('./financial-cheat-sheets/package.json', import.meta.url))('playwright');
import '../financial/lib/render.js';
import { course } from '../src/course.js';
import { loadContent } from './build-banks.mjs';
import { writeCheatSheet } from './build-cheat-sheets.mjs';
const R = globalThis.FA_RENDER;
const root = new URL('../', import.meta.url), P = p => new URL(p, root).pathname;
const CSS = readFileSync(P('financial/lib/fa.css'), 'utf8');
const esc = R.esc, rich = R.rich;
const ul = a => '<ul>' + a.map(x => '<li>' + rich(x) + '</li>').join('') + '</ul>';
const ol = a => '<ol class="steps">' + a.map(x => '<li>' + rich(x) + '</li>').join('') + '</ol>';
const page = (title, body, extra = '') => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>
:root{--display:"Bricolage Grotesque","Trebuchet MS",system-ui,sans-serif;--body:"Atkinson Hyperlegible","Segoe UI",system-ui,sans-serif;--purple-bg:#7448ff;--purple-text:#5a2fd6;--purple-tint:#ebe3ff;--ink:#14173a;--line:#cfd3ea;--card:#fff;--edge:#14173a;--shadow:#14173a;--sun:#ffd23f}
body{margin:0;background:#f4f5fb;font-family:var(--body);color:#14173a;line-height:1.45}${CSS}
.cs{display:block;font-size:.9rem}.cs::after{content:"";display:block;clear:both}.cs>div{width:48.5%;float:left}.cs>div+div{float:right}.cs .box{break-inside:avoid;border:2px solid #14173a;border-radius:10px;padding:8px 10px;margin:0 0 12px}.cs h3{margin:0 0 4px;font-family:var(--display);color:var(--purple-text);font-size:1rem}
.cs .fa-table{font-size:.82rem}.cs ul{margin:2px 0;padding-left:18px;font-size:.88rem}
.banner{background:#7448ff;color:#fff;padding:14px 18px;border-radius:12px;margin-bottom:12px}.banner h1{margin:0;font-family:var(--display)}.banner p{margin:4px 0 0}
.meta{display:flex;gap:8px;flex-wrap:wrap}.meta span{background:#ebe3ff;color:#5a2fd6;border-radius:99px;padding:2px 10px;font-weight:700;font-size:.85rem}
.task{border:2px solid #14173a;border-radius:10px;padding:10px 14px;margin:10px 0;break-inside:avoid}.task h3{margin:0 0 4px;font-family:var(--display)}
.work{border:1px dashed #9aa0c8;min-height:1.6in;border-radius:8px;margin:6px 0}
.chk li{list-style:"☐  "}
${extra}</style></head><body><main class="fa-page">${body}</main></body></html>`;

/* ---------- Project packet & guide ---------- */
function rubricTable(rub) {
  return R.table({ headers: ['Category (points)', 'Exemplary (100%)', 'Proficient (~80%)', 'Developing (~60%)', 'Beginning (~30%)'], rows: rub.map(r => [`${r.category} (${r.points})`, ...r.levels]) }) + `<p><strong>Total: ${rub.reduce((s, r) => s + r.points, 0)} points.</strong> Alternative recommendations earn full credit when supported by accurate evidence.</p>`;
}
function docs(p) { return p.documents.map(d => `<h3 class="fa-section-h">${esc(d.title)}</h3>${R.table(d.table)}${d.note ? '<p class="fa-doc-kind">' + rich(d.note) + '</p>' : ''}`).join(''); }
function studentPacket(p, unit) {
  const body = `<section class="fa-sheet"><div class="banner"><h1>${esc(p.title)}</h1><p>${esc(p.tagline)}</p></div>
<div class="meta"><span>Unit ${p.unitNum}: ${esc(unit.name)}</span><span>${esc(p.days)}</span><span>${esc(p.grouping)}</span></div>
<p style="margin-top:10px">Name(s) ______________________________ Period ____ Due ________</p>
<h3 class="fa-section-h">Introduction</h3><p>${rich(p.intro)}</p><div class="fa-note">${rich(p.scenario)}</div>
<h3 class="fa-section-h">Learning goals</h3>${ul(p.goals)}
<h3 class="fa-section-h">Supporting documents and data</h3>${docs(p)}
<div class="fa-pagebreak"></div><h3 class="fa-section-h">Tasks</h3>${p.tasks.map((t, i) => `<div class="task"><h3>Task ${i + 1}: ${esc(t.title)}</h3>${ol(t.steps)}<p><strong>Deliverable:</strong> ${rich(t.deliverable)}</p><div class="work"></div></div>`).join('')}
<h3 class="fa-section-h">Reflection</h3>${p.reflection.map((q, i) => `<p><strong>${i + 1}.</strong> ${rich(q)}</p>${R.lines(3)}`).join('')}
<h3 class="fa-section-h">Submission checklist</h3><ul class="chk">${p.checklist.map(c => '<li>' + rich(c) + '</li>').join('')}</ul>
<div class="fa-pagebreak"></div><h3 class="fa-section-h">Scoring rubric</h3>${rubricTable(p.rubric)}
<p class="fa-doc-kind">All people, businesses, places, and numbers in this project are fictional. Rates and costs are illustrative assumptions.</p></section>`;
  return page(`${p.title} — Student Packet`, body);
}
function teacherGuide(p, unit) {
  const T = p.teacher;
  const body = `<section class="fa-sheet"><div class="banner" style="background:#14173a"><h1>${esc(p.title)} — Teacher Guide</h1><p>Financial Algebra · Unit ${p.unitNum}: ${esc(unit.name)}</p></div>
<div class="meta"><span>${esc(p.days)}</span><span>${esc(p.grouping)}</span><span>Skills: ${p.skills.map(s => 'Skill ' + (+s.slice(-2))).join(', ')}</span></div>
<h3 class="fa-section-h">Overview</h3><p>${rich(p.intro)}</p>
<h3 class="fa-section-h">Skills covered</h3>${ul(p.skills.map(s => unit.skills[+s.slice(-2) - 1] + ' (' + s + ')'))}
<h3 class="fa-section-h">Required materials</h3>${ul(T.materials)}
<h3 class="fa-section-h">Suggested pacing</h3>${R.table({ headers: ['Session', 'Focus'], rows: T.pacing })}
<h3 class="fa-section-h">Implementation guidance</h3>${ul(T.implementation)}
<h3 class="fa-section-h">Worked calculations</h3>${T.worked.map(w => `<div class="task"><h3>${esc(w.task)}</h3>${ol(w.work)}</div>`).join('')}
<h3 class="fa-section-h">Sample student responses</h3>${T.samples.map(s => `<div class="fa-model">${rich(s)}</div>`).join('')}
<h3 class="fa-section-h">Common misconceptions</h3>${ul(T.misconceptions)}
<h3 class="fa-section-h">Differentiation</h3><p><strong>Support</strong></p>${ul(T.differentiation.support)}<p><strong>Extend</strong></p>${ul(T.differentiation.extend)}
<h3 class="fa-section-h">Extension opportunities</h3>${ul(T.extensions)}
<h3 class="fa-section-h">100-point rubric</h3>${rubricTable(p.rubric)}
<h3 class="fa-section-h">Student documents (reference)</h3>${docs(p)}</section>`;
  return page(`${p.title} — Teacher Guide`, body);
}
function hero(p) {
  const pal = ['#7448ff', '#22c08a', '#ff8a1f', '#3547f5'][p.unitNum % 4];
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420" role="img" aria-label="${esc(p.title)} illustration"><rect width="720" height="420" rx="24" fill="#f4f5fb"/><rect x="40" y="60" width="380" height="260" rx="18" fill="#fff" stroke="#14173a" stroke-width="6"/><rect x="70" y="95" width="160" height="22" rx="11" fill="${pal}" opacity=".3"/><path d="M75 280 L145 220 L205 245 L275 170 L345 195 L395 130" fill="none" stroke="${pal}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><circle cx="540" cy="150" r="90" fill="${pal}" stroke="#14173a" stroke-width="6"/><text x="540" y="182" font-family="Trebuchet MS,sans-serif" font-size="96" font-weight="800" text-anchor="middle" fill="#fff">$</text><rect x="460" y="270" width="200" height="70" rx="14" fill="#ffd23f" stroke="#14173a" stroke-width="6"/><text x="560" y="315" font-family="Trebuchet MS,sans-serif" font-size="26" font-weight="800" text-anchor="middle" fill="#14173a">Unit ${p.unitNum}</text></svg>`;
}
function landing(p, unit) {
  const f = p.slug;
  return `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(p.title)} · Financial Algebra Project</title><style>
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#F4F6FB;color:#1d2433}.wrap{max-width:980px;margin:0 auto;padding:24px 18px 48px}
.hero{display:grid;grid-template-columns:1.1fr 1fr;gap:22px;align-items:center;background:#3b1f7a;color:#fff;border-radius:16px;padding:22px;border-bottom:6px solid #B8860B}.hero img{width:100%;border-radius:10px;display:block;background:#fff}
.kicker{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:#d9ccff;font-weight:700}h1{margin:.25em 0 .2em;font-size:2rem}.tag{color:#EEE8FF;font-size:1.05rem;margin:0}
.meta{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}.pill{background:rgba(255,255,255,.15);padding:4px 10px;border-radius:999px;font-size:.85rem}p.desc{font-size:1.02rem;line-height:1.5;margin:20px 2px}
.levels{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#fff;border-radius:14px;box-shadow:0 1px 4px rgba(0,0,0,.08);overflow:hidden;display:flex;flex-direction:column}
.card h2{margin:0;color:#fff;font-size:1.2rem;padding:12px 16px}.card p{margin:12px 16px;font-size:.92rem;line-height:1.4;flex:1}.btns{display:flex;flex-direction:column;gap:8px;padding:0 16px 16px}
.btn{display:block;text-align:center;text-decoration:none;border-radius:9px;padding:9px 10px;font-weight:600;font-size:.92rem;border:2px solid currentColor}.btn.primary{color:#fff!important}
@media (max-width:760px){.hero,.levels{grid-template-columns:1fr}}</style></head><body><div class="wrap">
<header class="hero"><div><div class="kicker">Financial Algebra · Unit ${p.unitNum}: ${esc(unit.name)} · Project</div><h1>${esc(p.title)}</h1><p class="tag">${esc(p.tagline)}</p>
<div class="meta"><span class="pill">${esc(p.days)}</span><span class="pill">${esc(p.grouping)}</span><span class="pill">Standard level</span></div></div><img src="hero.svg" alt="Project illustration for ${esc(p.title)}"></header>
<p class="desc">${esc(p.intro)}</p>
<section class="levels"><article class="card"><h2 style="background:#7448ff">Student packet</h2><p>Scenario, documents, tasks with work space, reflection, checklist, and rubric.</p><div class="btns"><a class="btn primary" style="background:#7448ff;border-color:#7448ff" href="${f}-student.pdf">View / print PDF</a><a class="btn" style="color:#7448ff" href="${f}-student.docx" download>Word (.docx), editable</a></div></article>
<article class="card"><h2 style="background:#2B6CB0">Presentation</h2><p>Launch slides to introduce the scenario, tasks, key math, and scoring.</p><div class="btns"><a class="btn primary" style="background:#2B6CB0;border-color:#2B6CB0" href="${f}-slides.pptx" download>PowerPoint (.pptx), editable</a></div></article>
<article class="card"><h2 style="background:#14173a">Teacher guide</h2><p>Pacing, worked calculations, sample responses, misconceptions, differentiation, and the 100-point rubric.</p><div class="btns"><a class="btn primary" style="background:#14173a;border-color:#14173a" href="${f}-teacher-guide.pdf">View / print PDF</a><a class="btn" style="color:#14173a" href="${f}-teacher-guide.docx" download>Word (.docx), editable</a></div></article></section>
</div></body></html>`;
}
export async function buildPrint(ids) {
  const browser = await chromium.launch(); const pg = await browser.newPage();
  const pdf = async (html, out) => { await pg.setContent(html, { waitUntil: 'load' }); await pg.pdf({ path: out, format: 'Letter', margin: { top: '0.5in', bottom: '0.55in', left: '0.5in', right: '0.5in' }, printBackground: true, displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#666">Mr. K\'s Classroom · Financial Algebra · Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>' }); };
  const officeJobs = [], made = [];
  for (const id of ids) {
    const content = await loadContent(id); if (!content) continue;
    const unit = course.units.find(u => u.id === id), n = course.units.indexOf(unit) + 1;
    made.push(await writeCheatSheet(unit, n, content.cheatSheet, pg));
    const pf = P(`financial/content/projects/${id}.mjs`);
    if (!existsSync(pf)) continue;
    const projects = (await import(new URL(`financial/content/projects/${id}.mjs`, root).href)).default;
    for (const p of projects) {
      const dir = P(`artifacts/financial-algebra-project-${p.slug}/`); mkdirSync(dir, { recursive: true });
      await pdf(studentPacket(p, unit), dir + p.slug + '-student.pdf');
      await pdf(teacherGuide(p, unit), dir + p.slug + '-teacher-guide.pdf');
      writeFileSync(dir + 'index.html', landing(p, unit)); writeFileSync(dir + 'hero.svg', hero(p));
      officeJobs.push({ dir, unitName: unit.name, ...p }); made.push(dir);
    }
  }
  await browser.close();
  mkdirSync(P('dist'), { recursive: true });
  writeFileSync(P('dist/office-jobs.json'), JSON.stringify(officeJobs));
  return made;
}
if (import.meta.url === `file://${process.argv[1]}`) {
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : course.units.map(u => u.id);
  const m = await buildPrint(ids); console.log('built', m.length, 'print targets');
}
