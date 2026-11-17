/* Writes financial/resources.json (integration manifest) and financial/index.html (resource hub for review/staging). */
import { writeFileSync, readFileSync, existsSync } from 'node:fs';
import {GAMES} from '../financial/games/deck.mjs';
import { course } from '../src/course.js';
import {resourceThumbnail,resourceHref} from '../financial/lib/resource-previews.mjs';
import '../financial/lib/render.js';
import '../financial/lib/finance.js';
import '../financial/decision-lab/scenarios.js';
const R = globalThis.FA_RENDER, LABS = globalThis.FA_LABS;
const SHEETS = JSON.parse(readFileSync(new URL('../financial/spreadsheet-labs/labs.json', import.meta.url), 'utf8')).labs;
import { SKILL_STANDARDS, describe } from '../financial/content/standards.mjs';
const root = new URL('../', import.meta.url), P = p => new URL(p, root).pathname;
const index = JSON.parse(readFileSync(P('financial/banks/index.json'), 'utf8'));
const units = [];
for (const [i, u] of course.units.entries()) {
  const stats = index.units.find(x => x.unitId === u.id);
  const projects = existsSync(P(`financial/content/projects/${u.id}.mjs`)) ? (await import(new URL(`financial/content/projects/${u.id}.mjs`, root).href)).default : [];
  units.push({
    unitId: u.id, unitNum: i + 1, name: u.name, skills: u.skills.map((s, k) => { const id = `${u.id}-skill-${String(k + 1).padStart(2, '0')}`; return { id, name: s, standards: (SKILL_STANDARDS[id] || []).map(describe) }; }),
    questionCount: stats?.questions || 0, classroomExportCount: stats?.classroomExport || 0, flashcards: stats?.cards || 0,
    resources: {
      games: GAMES.map(g=>({id:g.id,title:g.name,path:`financial/games/index.html?unit=${u.id}&game=${g.id}`,description:g.description})),
      lessonPlan: `financial/generators/index.html?unit=${u.id}&mode=lesson`,
      worksheet: `financial/generators/index.html?unit=${u.id}&mode=worksheet`,
      assessment: `financial/generators/index.html?unit=${u.id}&mode=assessment`,
      errorAnalysis: `financial/generators/index.html?unit=${u.id}&mode=worksheet&format=error`,
      practiceTest: `financial/practice/index.html?unit=${u.id}`,
      flashcards: `financial/flashcards/index.html?unit=${u.id}`,
      cheatSheet: `artifacts/financial-algebra-${u.id}-cheat-sheet/cheat-sheet.pdf`,
      decisionLab: LABS[u.id] ? { title: LABS[u.id].title, path: `financial/decision-lab/index.html?lab=${u.id}`, teacherPath: `financial/decision-lab/index.html?lab=${u.id}&teacher=1` } : null,
      spreadsheetLabs: SHEETS.filter(l => l.unit === u.id).map(l => ({ title: l.title, path: `financial/spreadsheet-labs/index.html?lab=${l.slug}`, template: `financial/spreadsheet-labs/${l.file}`, description: l.blurb })),
      pacingGuide: 'financial/pacing/index.html',
      projects: projects.map(p => ({ slug: p.slug, title: p.title, grouping: p.grouping, days: p.days, path: `artifacts/financial-algebra-project-${p.slug}/index.html` })),
      classroomBank: `question-banks/financial-algebra/${u.id}.json`, extendedBank: `financial/banks/${u.id}.json`,
      classroomGames: ['showdown', 'connect-four', 'tic-tac-toe', 'picture-reveal', 'detective'].map(g => ({ game: g, note: 'Uses the Classroom bank (multiple-choice/short-answer items only).' }))
    }
  });
}
const manifest = { schema: 'fa-resources-1', courseId: 'financial-algebra', levels: ['support', 'standard', 'advanced'], classroomLevelCodes: { support: 'cp2', standard: 'cp1', advanced: 'honors' }, generated: 'scripts/build-hub.mjs', pacingGuide: 'financial/pacing/index.html', spreadsheetLabs: 'financial/spreadsheet-labs/index.html', units };
writeFileSync(P('financial/resources.json'), JSON.stringify(manifest, null, 1));
const card = (t, href, sub, unitId) => `<a class="fa-panel flat hub-link" href="${resourceHref(href)}"><img src="../${resourceThumbnail(href.replace(/^\.\.\//,''),unitId)}" alt="" width="720" height="450" loading="lazy" style="width:100%;height:auto;aspect-ratio:8/5;object-fit:contain;border-radius:8px"><strong>${R.esc(t)}</strong>${sub ? `<span>${R.esc(sub)}</span>` : ''}</a>`;
const body = units.map(u => { const r = u.resources; return `<section class="fa-panel" id="${u.unitId}"><h2><span class="fa-pill">Unit ${u.unitNum}</span> ${R.esc(u.name)}</h2><p>${u.skills.map(s => R.esc(s.name)).join(' · ')}</p><p class="fa-doc-kind">${u.questionCount} bank items · ${u.flashcards} flashcards · ${r.projects.length} project${r.projects.length === 1 ? '' : 's'}</p><div class="fa-grid">
${card('Lesson Plan', '../' + r.lessonPlan, 'Printable notes, examples, practice and key',u.unitId)}${card('Worksheet', '../' + r.worksheet, '8 formats + key',u.unitId)}${card('Assessment', '../' + r.assessment, 'Configurable points + worked key',u.unitId)}${card('Practice Test', '../' + r.practiceTest, 'Self-checking',u.unitId)}${card('Flashcards', '../' + r.flashcards, 'Terms, formulas, principles',u.unitId)}${card('Cheat Sheet', '../' + r.cheatSheet, 'Printable PDF',u.unitId)}${r.decisionLab ? card('Decision Lab: ' + r.decisionLab.title, '../' + r.decisionLab.path, '7-step guided decision',u.unitId) : ''}${r.spreadsheetLabs.map(l=>card(l.title,'../'+l.path,l.description,u.unitId)).join('')}${r.games.map(g=>card(g.title,'../'+g.path,g.description,u.unitId)).join('')}${r.projects.map(p => card('Project: ' + p.title, '../' + p.path, p.grouping + ' · ' + p.days,u.unitId)).join('')}</div></section>`; }).join('');
writeFileSync(P('financial/index.html'), `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Financial Algebra Resources | Mr. K's Classroom</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="../styles.css"><link rel="stylesheet" href="lib/fa.css?v=fa-1"><style>.hub-link{display:flex;flex-direction:column;gap:2px;text-decoration:none;color:inherit;margin:0}.hub-link span{font-size:.85rem;color:var(--ink-soft,#4a4f78)}.hub-link:hover{border-color:var(--fa-accent)}</style></head>
<body><main class="fa-page" id="main" tabindex="-1"><p><a href="../index.html">← Financial Algebra outline</a></p><h1>Financial Algebra Resource Library</h1><p>Three levels: Support, Standard and Advanced. All people, companies, and numbers are fictional; rates and returns are illustrative assumptions. <a href="decision-lab/index.html">All Decision Labs</a> · <a href="spreadsheet-labs/index.html">Spreadsheet Labs</a> · <a href="pacing/index.html">Pacing guide and standards map</a></p>${body}</main></body></html>`);
console.log('hub + manifest written for', units.length, 'units');

