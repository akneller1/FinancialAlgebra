/* Applies the one-money-style-per-question rule (normalizeMoney in financial/content/kit.mjs) to the built
 * Financial Algebra banks without rebuilding them, so nothing else in the files changes.
 * Files: financial/banks/<unit>.json and question-banks/financial-algebra/<unit>.json (the "questions" lists).
 * Usage: node scripts/normalize-money.mjs          (writes the files and reports how many questions changed)
 *        node scripts/normalize-money.mjs --check  (changes nothing; exits 1 if any question still mixes styles)
 * New builds (scripts/build-banks.mjs) already apply the rule. */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { normalizeMoney } from '../financial/content/kit.mjs';
const root = new URL('../', import.meta.url);
const check = process.argv.includes('--check');
let changed = 0, total = 0;
for (const dir of ['financial/banks/', 'question-banks/financial-algebra/']) {
  for (const name of readdirSync(new URL(dir, root)).filter(n => n.endsWith('.json') && n !== 'index.json')) {
    const file = new URL(dir + name, root), text = readFileSync(file, 'utf8'), data = JSON.parse(text);
    if (!Array.isArray(data.questions)) continue;
    let n = 0;
    data.questions = data.questions.map(q => { total++; const fixed = normalizeMoney(q); if (JSON.stringify(fixed) !== JSON.stringify(q)) n++; return fixed; });
    changed += n;
    if (n && !check) writeFileSync(file, JSON.stringify(data, null, text.includes('\n ') ? (text.match(/\n( +)/)[1].length) : 0) + (text.endsWith('\n') ? '\n' : ''));
    if (n) console.log(`${dir}${name}: ${n} question(s) ${check ? 'mix money styles' : 'updated'}`);
  }
}
console.log(`${changed} of ${total} questions ${check ? 'mix money styles' : 'updated'}.`);
if (check && changed) process.exit(1);
