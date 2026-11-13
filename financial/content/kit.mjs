/* Build-time authoring kit for Financial Algebra question families (Node ESM).
 * Deterministic: every variant is produced from a seeded RNG, so builds are reproducible. */
import '../lib/finance.js';
export const M = globalThis.FA_MATH;

export function rng(seed) {
  let a = typeof seed === 'number' ? seed : [...String(seed)].reduce((h, c) => Math.imul(h ^ c.charCodeAt(0), 2654435761) >>> 0, 1779033703);
  const next = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const r = {
    next, int: (lo, hi) => lo + Math.floor(next() * (hi - lo + 1)),
    step: (lo, hi, s) => lo + s * Math.floor(next() * (Math.floor((hi - lo) / s) + 1)),
    pick: arr => arr[Math.floor(next() * arr.length)],
    shuffle: arr => { const a2 = arr.slice(); for (let i = a2.length - 1; i > 0; i--) { const j = Math.floor(next() * (i + 1)); [a2[i], a2[j]] = [a2[j], a2[i]]; } return a2; },
    sample: (arr, n) => r.shuffle(arr).slice(0, n)
  };
  return r;
}

/* ---------- formatting ---------- */
export const money = (x, cents = true) => {
  const neg = x < 0, v = Math.abs(M.round2(x));
  const s = cents ? v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : Math.round(v).toLocaleString('en-US');
  return (neg ? '−$' : '$') + s;
};
export const $ = x => money(x, !Number.isInteger(M.round2(x)));      // drop .00 on whole dollars
export const $0 = x => money(x, false);
/* One money style per question: if any dollar amount in the question shows cents ($45.50), every whole amount
   shows .00 too ($1,500.00); otherwise whole amounts drop .00 ($2,100). Mixed "$1,500 … $2,100.00" never appears.
   Applied to every generated question in buildUnit; scripts/normalize-money.mjs applies it to built banks. */
const MONEY_RE = /([−-]?\$)(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?(?![\d,]\d)/g;
const MONEY_SKIP = new Set(['id', 'unitId', 'skillId', 'level', 'family', 'type', 'format', 'activityTypes', 'gameEligible', 'value', 'tolerance', 'unit']);
function eachString(o, fn, key) {
  if (typeof o === 'string') return MONEY_SKIP.has(key) ? o : fn(o);
  if (Array.isArray(o)) return o.map(v => eachString(v, fn, key));
  if (o && typeof o === 'object') { const out = {}; for (const k of Object.keys(o)) out[k] = MONEY_SKIP.has(k) ? o[k] : eachString(o[k], fn, k); return out; }
  return o;
}
export function normalizeMoney(q) {
  let cents = false;
  eachString(q, s => { for (const m of s.matchAll(MONEY_RE)) if (m[3] && !/^0+$/.test(m[3])) cents = true; return s; });
  return eachString(q, s => s.replace(MONEY_RE, (all, sign, whole, dec) => {
    if (dec && !/^0+$/.test(dec)) return all;
    return sign + whole + (cents ? '.00' : '');
  }));
}
export const pct = (x, d = 1) => (Math.round(x * 100 * 10 ** d) / 10 ** d).toString() + '%';
export const num = (x, d = 0) => (Math.round(x * 10 ** d) / 10 ** d).toLocaleString('en-US');

/* ---------- fictional cast (no real people; names are common and varied) ---------- */
export const PEOPLE = [
  ['Maya', 'she'], ['Jordan', 'they'], ['Luis', 'he'], ['Aaliyah', 'she'], ['Dev', 'he'], ['Sofia', 'she'], ['Marcus', 'he'],
  ['Priya', 'she'], ['Elijah', 'he'], ['Hana', 'she'], ['Tyler', 'he'], ['Camila', 'she'], ['Noah', 'he'], ['Zara', 'she'],
  ['Andre', 'he'], ['Mei', 'she'], ['Owen', 'he'], ['Fatima', 'she'], ['Diego', 'he'], ['Grace', 'she'], ['Kofi', 'he'],
  ['Riley', 'they'], ['Nadia', 'she'], ['Sam', 'they'], ['Isaiah', 'he'], ['Leah', 'she'], ['Mateo', 'he'], ['Imani', 'she']
];
export const TOWNS = ['Riverton', 'Maple Falls', 'Harbor City', 'Cedar Grove', 'Lakeview', 'Brookside', 'Pine Ridge', 'Westfield Commons'];
export const JOBS = [
  ['medical assistant', 41000], ['electrician apprentice', 44000], ['retail store supervisor', 39000], ['dental hygienist', 78000],
  ['line cook', 34000], ['HVAC technician', 52000], ['bank teller', 36000], ['graphic designer', 54000], ['paralegal', 50000],
  ['registered nurse', 82000], ['software support specialist', 58000], ['auto mechanic', 47000], ['preschool teacher', 37000],
  ['logistics coordinator', 49000], ['physical therapy aide', 33000], ['welder', 48000], ['pharmacy technician', 39000]
];
export function person(r, used) {
  let p; let guard = 0;
  do { p = r.pick(PEOPLE); guard++; } while (used && used.has(p[0]) && guard < 50);
  if (used) used.add(p[0]);
  const [name, pr] = p;
  const P = { they: ['they', 'them', 'their', 'are', 'have'], he: ['he', 'him', 'his', 'is', 'has'], she: ['she', 'her', 'her', 'is', 'has'] }[pr];
  return { name, sub: P[0], obj: P[1], pos: P[2], be: P[3], has: P[4], Sub: P[0][0].toUpperCase() + P[0].slice(1), Pos: P[2][0].toUpperCase() + P[2].slice(1) };
}

/* ---------- question helpers ---------- */
/* Multiple choice: correct + distractors -> options (deterministically shuffled, de-duplicated). */
export function mc(r, correct, distractors, why) {
  const seen = new Set([String(correct)]); const ds = [];
  for (const d of distractors) { const s = String(d); if (!seen.has(s)) { seen.add(s); ds.push(s); } }
  if (ds.length < 2) throw Error('mc needs 2+ distinct distractors for ' + correct);
  const options = r.shuffle([{ text: String(correct), correct: true }, ...ds.slice(0, 3).map(t => ({ text: t, correct: false }))]);
  return { format: 'multiple-choice', answer: String(correct), options, distractorNotes: why || undefined };
}
export function selectAll(r, correctList, wrongList) {
  const options = r.shuffle([...correctList.map(t => ({ text: t, correct: true })), ...wrongList.map(t => ({ text: t, correct: false }))]);
  return { format: 'select-all', answer: correctList.slice(), options };
}
export function numeric(value, opts = {}) {
  const v = M.round2(value);
  return { format: 'short-answer', answer: opts.display || (opts.unit === '%' ? pct(value / 100, opts.d ?? 1) : opts.unit === 'count' ? String(v) : money(v)), numeric: { value: v, tolerance: opts.tolerance ?? (opts.unit === 'count' ? 0 : 0.01), unit: opts.unit || 'USD' } };
}
export const table = (headers, rows, caption) => ({ headers, rows, caption });

/* Default analytic rubric for open responses (4 criteria x 4 points = 16, scaled by generators). */
export function rubric(specific = {}) {
  return [
    { criterion: 'Financial accuracy', points: 4, full: specific.accuracy || 'All calculations correct, labeled, and rounded to cents where money is reported.', partial: 'Minor arithmetic or rounding errors that do not change the conclusion.', none: 'Major errors or missing calculations.' },
    { criterion: 'Use of evidence', points: 4, full: specific.evidence || 'Cites specific numbers from the scenario or document to support each claim.', partial: 'Uses some numbers but leaves claims unsupported.', none: 'No reference to the data.' },
    { criterion: 'Reasoning & tradeoffs', points: 4, full: specific.reasoning || 'Weighs at least two advantages/disadvantages, including a non-numeric factor, and states assumptions.', partial: 'Mentions tradeoffs without weighing them.', none: 'Opinion only.' },
    { criterion: 'Recommendation & communication', points: 4, full: specific.recommendation || 'Clear, defensible recommendation; explains what new information would change it. Alternative defensible conclusions earn full credit.', partial: 'Recommendation present but vague.', none: 'No recommendation.' }
  ];
}
export const CLAIM_OPTIONS = ['Always true', 'Sometimes true — it depends on the situation', 'Never true'];

/* Build all items for a unit from its authored content.
 * Each family: {id, skill:1..4, type, count, gen(r,k)} -> question fields. */
export function buildUnit(unitId, content) {
  const out = []; const prompts = new Set();
  const push = (q, fam, k) => {
    q = normalizeMoney(q);
    const id = `fa-${unitId}-s${String(q.skill).padStart(2, '0')}-${fam}-${String(k + 1).padStart(2, '0')}`;
    const key = (q.prompt + JSON.stringify(q.scenario || '')).replace(/\s+/g, ' ');
    if (prompts.has(key)) return false; prompts.add(key);
    const { skill, ...rest } = q;
    out.push({ id, unitId, skillId: `${unitId}-skill-${String(skill).padStart(2, '0')}`, level: 'standard', family: fam, ...rest });
    return true;
  };
  // vocabulary: term->definition and definition->term
  const V = content.vocab;
  V.forEach((v, i) => {
    const r = rng(unitId + 'v' + i);
    const others = V.filter(o => o !== v);
    const dDefs = r.sample(others, 3).map(o => o.def);
    push({ skill: v.skill, type: 'vocabulary', prompt: `What does **${v.term}** mean?`, ...mc(r, v.def, dDefs), solutionSteps: [`${v.term}: ${v.def}`, v.example ? 'Example: ' + v.example : 'Connect the term to its use in a budget or contract.'], misconceptions: v.mis ? [v.mis] : [], activityTypes: ['flashcards', 'showdown', 'connect4', 'tictactoe', 'picture-reveal', 'detective', 'worksheet', 'assessment'], gameEligible: true }, 'vocab-def', i);
    const dTerms = r.sample(others, 3).map(o => o.term);
    push({ skill: v.skill, type: 'vocabulary', prompt: `Which term matches this description? “${v.def}”`, ...mc(r, v.term, dTerms), solutionSteps: [`The description defines ${v.term}.`, v.example ? 'Example: ' + v.example : ''].filter(Boolean), activityTypes: ['showdown', 'connect4', 'tictactoe', 'picture-reveal', 'worksheet', 'assessment'], gameEligible: true }, 'vocab-term', i);
    if (v.example) {
      const dEx = r.sample(others.filter(o => o.example), 3).map(o => o.term);
      if (dEx.length >= 2) push({ skill: v.skill, type: 'concept', prompt: `Which financial term is illustrated? ${v.example}`, ...mc(r, v.term, dEx), solutionSteps: [`This is an example of ${v.term}: ${v.def}`], activityTypes: ['showdown', 'connect4', 'worksheet', 'assessment'], gameEligible: true }, 'vocab-ex', i);
    }
  });
  (content.concepts || []).forEach((c, i) => {
    const r = rng(unitId + 'c' + i);
    push({ skill: c.skill, type: c.type || 'concept', prompt: c.q, ...(c.all ? selectAll(r, c.all, c.wrong) : mc(r, c.a, c.d)), solutionSteps: [c.why], misconceptions: c.mis ? [c.mis] : [], activityTypes: c.all ? ['worksheet', 'assessment'] : ['showdown', 'connect4', 'tictactoe', 'detective', 'worksheet', 'assessment'], gameEligible: !c.all && c.q.length < 260 }, 'concept', i);
  });
  (content.claims || []).forEach((c, i) => {
    const r = rng(unitId + 'cl' + i);
    const correct = CLAIM_OPTIONS[c.verdict];
    push({ skill: c.skill, type: 'claim', prompt: `Evaluate the claim: “${c.claim}”`, format: 'multiple-choice', answer: correct, options: CLAIM_OPTIONS.map(t => ({ text: t, correct: t === correct })), solutionSteps: [c.model], modelResponse: c.model, misconceptions: [c.claim], activityTypes: ['showdown', 'worksheet', 'assessment', 'detective'], gameEligible: true }, 'claim', i);
    push({ skill: c.skill, type: 'claim', format: 'open-response', prompt: `A friend says: “${c.claim}” Do you agree? Use a specific numerical example to support or refute the claim.`,
      parts: [{ prompt: 'State whether the claim is always, sometimes, or never true.', answer: correct }, { prompt: 'Give a specific numerical example.', answer: c.example || 'Answers vary; see model response.' }, { prompt: 'Explain the financial principle involved.', answer: c.model }, { prompt: 'Describe a situation where a reasonable person might see it differently.', answer: c.other || 'Answers vary; accept any defensible situation.' }],
      answer: correct, solutionSteps: [c.model], modelResponse: c.model + (c.example ? ' Example: ' + c.example : ''), rubric: rubric({ evidence: 'Supports the verdict with a correct, specific numerical example.' }), activityTypes: ['worksheet', 'assessment', 'lesson'], gameEligible: false }, 'claim-cer', i);
  });
  for (const fam of content.families) {
    let made = 0;
    for (let k = 0; made < fam.count && k < fam.count * 4; k++) {
      const r = rng(`${unitId}:${fam.id}:${k}`);
      const q = fam.gen(r, k);
      if (!q) continue;
      const base = { skill: fam.skill, type: fam.type, activityTypes: fam.activities || defaultActivities(fam.type, q.format), gameEligible: fam.game ?? (q.format !== 'open-response' && !q.scenario?.document && (q.prompt.length < 280)) };
      if (q.format === 'open-response' && !q.rubric) q.rubric = rubric(fam.rubric);
      if (push({ ...base, ...q }, fam.id, made)) made++;
    }
  }
  return out;
}
function defaultActivities(type, format) {
  if (format === 'open-response') return ['worksheet', 'assessment', 'lesson', 'project-practice'];
  if (type === 'document') return ['worksheet', 'assessment', 'lesson'];
  if (type === 'calculation') return ['worksheet', 'assessment', 'showdown', 'escape-room', 'practice-test'];
  return ['worksheet', 'assessment', 'practice-test'];
}
export const an = w => (/^(?:[aeio]|u(?!ni|s[eu])|hvac|hour|honest)/i.test(w) ? 'an ' : 'a ') + w;
