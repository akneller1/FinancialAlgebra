/* Builds Financial Algebra question banks from authored content.
 * Outputs:
 *   financial/banks/<unit>.json                 extended FA bank (schema "fa-bank-1")
 *   question-banks/financial-algebra/<unit>.json  Classroom schemaVersion 1 export (level "cp1" = the single Standard level)
 *   financial/banks/index.json                  unit list + counts
 *   financial/flashcards/decks.js               flashcard decks (window.FA_DECKS)
 * Usage: node scripts/build-banks.mjs [unitId ...]
 */
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { buildUnit } from '../financial/content/kit.mjs';
import { course } from '../src/course.js';
const root = new URL('../', import.meta.url);
const P = p => new URL(p, root);

export const UNIT_ORDER = course.units.map(u => u.id);
export async function loadContent(id) {
  const f = P(`financial/content/${id}.mjs`);
  if (!existsSync(f)) return null;
  return (await import(f.href)).default;
}
const strip = s => String(s).replace(/\*\*(.+?)\*\*/g, '$1').replace(/\[\[(.+?)\|\|(.+?)\]\]/g, (_, a, b) => a.trim() + ' ÷ ' + b.trim());
function tableText(t) {
  if (!t) return '';
  return '\n' + (t.caption ? t.caption + '\n' : '') + [t.headers, ...t.rows].map(r => r.join(' | ')).join('\n');
}
function docText(d) {
  if (!d) return '';
  return '\n' + d.title + (d.meta ? '\n' + d.meta.map(m => m[0] + ': ' + m[1]).join('; ') : '') + tableText(d.table) + (d.notes ? '\n' + d.notes.join('\n') : '');
}
export function toClassroom(q) {
  const ok = (q.format === 'multiple-choice' || q.format === 'short-answer') ? q.gameEligible : q.format === 'select-all' ? true : q.format === 'open-response' ? (q.parts || []).length >= 4 : false;
  if (!ok) return null;
  const sc = q.scenario || {};
  const prompt = strip((sc.text ? sc.text + '\n' : '') + q.prompt + tableText(sc.table) + docText(sc.document));
  const out = { id: q.id, skillId: q.skillId, level: 'cp1', format: q.format, prompt, answer: q.format === 'select-all' ? q.answer : strip(q.answer), solutionSteps: q.solutionSteps.map(strip).filter(Boolean) };
  if (q.options) out.options = q.options.map(o => ({ text: strip(o.text), correct: o.correct }));
  if (q.parts) out.parts = q.parts.map(p => ({ prompt: strip(p.prompt), answer: strip(p.answer) }));
  if (q.rubric) out.solutionSteps = out.solutionSteps.concat('Rubric (' + q.rubric.reduce((s, c) => s + c.points, 0) + ' pts):', ...q.rubric.map(c => `${c.criterion} (${c.points}): ${c.full}`));
  if (q.modelResponse) out.solutionSteps.push('Model response: ' + strip(q.modelResponse));
  out.sourceNotes = `Financial Algebra original item (family ${q.family}; type ${q.type}). Fictional scenario; hypothetical values. Single course level "standard" stored as cp1 for Classroom schema compatibility.`;
  return out;
}
export async function buildAll(ids = UNIT_ORDER) {
  const summary = [];
  const decks = {};
  for (const id of ids) {
    const content = await loadContent(id);
    if (!content) continue;
    const unit = course.units.find(u => u.id === id);
    const questions = buildUnit(id, content);
    const ext = { schema: 'fa-bank-1', courseId: 'financial-algebra', unitId: id, unitName: unit.name, level: 'standard', generated: 'deterministic', assumptions: 'All people, employers, institutions, prices, and rates are fictional or illustrative. See financial/lib/finance.js ASSUMPTIONS.', skills: unit.skills.map((s, i) => ({ id: `${id}-skill-${String(i + 1).padStart(2, '0')}`, name: s })), vocab: content.vocab, lessons: content.lessons, cheatSheet: content.cheatSheet, questions };
    mkdirSync(P('financial/banks'), { recursive: true }); mkdirSync(P('question-banks/financial-algebra'), { recursive: true });
    writeFileSync(P(`financial/banks/${id}.json`), JSON.stringify(ext, null, 1));
    const cls = { schemaVersion: 1, courseId: 'financial-algebra', unitId: id, questions: questions.map(toClassroom).filter(Boolean) };
    writeFileSync(P(`question-banks/financial-algebra/${id}.json`), JSON.stringify(cls, null, 1));
    decks[id] = { unit: unit.name, cards: content.vocab.map((v, i) => ({ id: `${id}-card-${i + 1}`, skillId: `${id}-skill-${String(v.skill).padStart(2, '0')}`, front: v.term, back: v.def, example: v.example || '', watch: v.mis || '' })).concat((content.flashExtras || []).map((c, i) => ({ id: `${id}-card-x${i + 1}`, skillId: `${id}-skill-${String(c.skill).padStart(2, '0')}`, front: c.front, back: c.back, example: c.example || '', watch: c.watch || '', kind: c.kind || 'principle' }))) };
    const bySkill = {}; questions.forEach(q => { bySkill[q.skillId] = (bySkill[q.skillId] || 0) + 1; });
    summary.push({ unitId: id, name: unit.name, questions: questions.length, classroomExport: cls.questions.length, bySkill, cards: decks[id].cards.length, lessons: content.lessons.length });
  }
  writeFileSync(P('financial/banks/index.json'), JSON.stringify({ schema: 'fa-bank-index-1', units: summary }, null, 1));
  mkdirSync(P('financial/flashcards'), { recursive: true });
  writeFileSync(P('financial/flashcards/decks.js'), '/* Generated by scripts/build-banks.mjs */\nwindow.FA_DECKS=' + JSON.stringify(decks) + ';\n');
  // Drop-in for the Classroom vocabulary flashcard/printable builder (MKVOCAB_BANKS format: term|definition|example;...)
  const mk = Object.fromEntries(Object.entries(decks).map(([id, d]) => ['financial-algebra-' + id, d.cards.filter(c => !c.kind).map(c => [c.front, c.back, c.example].map(x => String(x).replace(/[|;]/g, ',')).join('|')).join(';')]));
  writeFileSync(P('financial/flashcards/mkvocab-financial-algebra.js'), '/* Generated. Adds Financial Algebra decks to the Classroom vocabulary system without replacing existing banks. */\nwindow.MKVOCAB_BANKS=Object.assign(window.MKVOCAB_BANKS||{},' + JSON.stringify(mk) + ');\n');
  return summary;
}
if (import.meta.url === `file://${process.argv[1]}`) {
  const s = await buildAll(process.argv.slice(2).length ? process.argv.slice(2) : undefined);
  console.table(s.map(x => ({ unit: x.unitId, q: x.questions, cls: x.classroomExport, cards: x.cards, ...x.bySkill })));
}
