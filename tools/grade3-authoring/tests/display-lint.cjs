// Renders every student-facing string of the Grade 3 banks through the site's own math-display.js and flags
// text that would display badly: English words broken into italic "variables", stray slashes, raw markup.
const fs = require('fs'), vm = require('vm'), path = require('path');
const root = path.resolve(__dirname, '..', '..', '..');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'worksheet-generator/core/math-display.js'), 'utf8').replace('if(G.document)', 'if(false)'), ctx);
const html = ctx.MK_MATH_DISPLAY.html;
const OK_SINGLE = new Set(['x', 'y', 'n', 'p', 'l', 'w', 'h', 'V', 'B', 'A', 'C', 'D', 'P', 'R', 'E', 'F', 'G', 'Q', 'S', 'T', 'X', 'K', 'M', 'W', 'c', 'r', 'm', 's', 'k']);
const dir = path.join(root, 'question-banks/math3');
let issues = [], n = 0;
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.json'))) {
  const bank = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  for (const q of bank.questions) {
    const texts = [q.prompt, ...(q.options || []).map(o => o.text), ...(q.parts || []).map(p => p.prompt), ...(q.parts || []).map(p => p.answer),
      ...(Array.isArray(q.answer) ? q.answer : [q.answer]), ...q.solutionSteps];
    for (const t of texts) {
      n++;
      // '(a) … ; (b) …' part labels are the site-wide open-response answer convention (see math6 banks)
      const h = html(String(t).replace(/(^|; |\n)\(([a-d])\) /g, '$1Part. '));
      const multi = h.match(/(<i>[A-Za-z]<\/i>){2,}/g);
      if (multi) issues.push([q.id, 'italic word: ' + multi[0].replace(/<\/?i>/g, ''), t]);
      for (const m of h.matchAll(/<i>([A-Za-z])<\/i>/g)) if (!OK_SINGLE.has(m[1])) { issues.push([q.id, 'italic letter ' + m[1], t]); break; }
      if (/\//.test(h.replace(/<[^>]+>/g, ''))) issues.push([q.id, 'slash left unstacked', t]);
    }
  }
}
const by = {};
for (const [id, what, t] of issues) { by[what] = by[what] || []; by[what].push([id, t]); }
for (const [k, v] of Object.entries(by).sort((a, b) => b[1].length - a[1].length)) console.log(v.length.toString().padStart(5), k, '| e.g.', v[0][0], JSON.stringify(v[0][1]).slice(0, 140));
console.log(`display lint: ${n} strings, ${issues.length} issues`);
process.exit(issues.length ? 1 : 0);
