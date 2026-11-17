/* Sorts Financial Algebra questions into three levels (2026-11-17).
 *   support  · Support (Classroom code cp2)
 *   standard · Standard (cp1)
 *   advanced · Advanced (honors)
 * Questions written for a level (families with an explicit level, ids "lv-…") keep it. Every other question gets an
 * effort score: solution steps, prompt length, comparisons and documents, cents, and solving for an unknown.
 * Definition checks are always Support and multi-part open responses always Advanced. Within each skill the
 * middle of the effort ranking (at least 15 questions, or 40%) stays Standard, and the easier and harder ends
 * become Support and Advanced. Deterministic: ties break by question id. */
export const LEVELS = ['support', 'standard', 'advanced'];
export const CLASSROOM_CODE = { support: 'cp2', standard: 'cp1', advanced: 'honors' };
export function effort(q) {
  if (q.type === 'vocabulary') return -Infinity;
  if (q.format === 'open-response') return Infinity;
  let s = (q.solutionSteps || []).length + Math.min(2, String(q.prompt || '').length / 160);
  if (q.type === 'comparison' || q.type === 'document') s += 1;
  if (q.type === 'concept' || q.type === 'claim') s -= 0.5;
  if (/\d\.\d\d/.test(q.prompt || '')) s += 0.5;
  if (/what (annual )?(interest )?rate|how many (months|years)|how long|what (monthly )?(deposit|payment) (is )?needed|solve|break-even|at least|greatest/i.test(q.prompt || '')) s += 1.5;
  if (q.scenario && (q.scenario.table || q.scenario.document)) s += 0.75;
  return s;
}
export function assignLevels(questions) {
  const bySkill = {};
  for (const q of questions) if (!/^lv-/.test(q.family || '')) (bySkill[q.skillId] = bySkill[q.skillId] || []).push(q);
  for (const qs of Object.values(bySkill)) {
    const free = qs.filter(q => Number.isFinite(effort(q))).sort((a, b) => effort(a) - effort(b) || (a.id < b.id ? -1 : 1));
    const n = free.length, std = Math.min(n, Math.max(15, Math.round(n * 0.4))), lo = Math.floor((n - std) / 2), hi = lo + std;
    free.forEach((q, i) => { q.level = i < lo ? 'support' : i >= hi ? 'advanced' : 'standard'; });
    for (const q of qs) if (!Number.isFinite(effort(q))) q.level = effort(q) < 0 ? 'support' : 'advanced';
  }
  return questions;
}
