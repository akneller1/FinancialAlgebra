// Browser test for the Grade 1–3 Interactive Math tools (artifacts/math{1,2,3}-*/index.html).
// For every tool: the page loads with no console or page errors; no challenge is already ticked; a scripted student
// reaches all six "Try this" challenges using only the on-screen controls; random clicks on every button raise no errors;
// Teacher view links the worksheet and teacher key; Fit and Present keep the workspace on screen.
// Usage (repository root): node tools/elementary-interactive/tests/browser-tools.cjs
const http = require('http'), fs = require('fs'), path = require('path'), pw = require('playwright');
const ROOT = path.resolve(__dirname, '../../..');
const M = [1, 2, 3].flatMap(g => JSON.parse(fs.readFileSync(path.join(ROOT, `tools/grade${g}-authoring/interactive/manifest.json`), 'utf8')).tools);

/* Helpers injected into each page. setK presses a stepper's buttons (largest step that does not overshoot) until its value
   shows the target; c clicks a selector n times; type fills an input. */
const HELPERS = `
window.__h = {
  v(key) { const t = document.getElementById('v-' + key).textContent; const n = parseInt(t, 10); return isNaN(n) ? 0 : n; },
  setK(key, target) {
    for (let i = 0; i < 400; i++) {
      const v = this.v(key); if (v === target) return true;
      const diff = target - v, steps = [...document.querySelectorAll('button[data-k="' + key + '"]')].map(b => +b.dataset.s);
      const s = steps.filter(x => Math.sign(x) === Math.sign(diff) && Math.abs(x) <= Math.abs(diff)).sort((a, b) => Math.abs(b) - Math.abs(a))[0];
      if (!s) throw Error('cannot reach ' + key + '=' + target + ' from ' + v);
      document.querySelector('button[data-k="' + key + '"][data-s="' + s + '"]').click();
    }
    throw Error('stepper ' + key + ' stuck');
  },
  c(sel, n = 1) { for (let i = 0; i < n; i++) { const e = document.querySelector(sel); if (!e) throw Error('missing ' + sel); e.dispatchEvent(new MouseEvent('click', { bubbles: true })); } },
  sel(sel, v) { const e = document.querySelector(sel); e.value = v; e.dispatchEvent(new Event('change', { bubbles: true })); },
  type(sel, v) { const e = document.querySelector(sel); e.value = v; }
};`;

const t = 'button[data-k="t"]';
const SOLVE = {
  'math1-ten-frame-builder': h => { h.setK('a', 6); h.setK('b', 4); h.setK('a', 7); h.setK('b', 3); h.setK('a', 9); h.setK('b', 5); h.setK('a', 10); h.setK('b', 3); h.setK('b', 2); h.setK('take', 4); h.setK('take', 0); h.setK('b', 6); },
  'math1-tens-ones-builder': h => { h.setK('t', 3); h.setK('o', 4); h.setK('t', 0); h.setK('o', 14); h.c('#toBundle'); h.setK('t', 2); h.setK('o', 5); h.c('#toBreak'); h.setK('o', 0); h.setK('t', 10); h.setK('t', 12); h.c('#toCmp'); h.setK('t', 4); h.setK('o', 3); h.setK('tb', 4); h.setK('ob', 7); h.c('[data-sym="<"]'); },
  'math1-balance-scale': h => { h.setK('a', 4); h.setK('b', 3); h.setK('c', 5); h.setK('d', 2); h.setK('b', 6); h.setK('c', 7); h.setK('d', 3); h.setK('a', 7); h.setK('b', 0); h.setK('d', 0); h.setK('a', 6); h.setK('b', 2); h.setK('c', 2); h.setK('d', 6); h.setK('d', 9); h.setK('a', 9); h.setK('b', 5); h.setK('c', 10); h.setK('d', 4); },
  'math1-hundred-chart': h => { const go = v => h.c('.el-cell[data-v="' + v + '"]'); go(23); h.c('[data-h="10"]'); go(50); h.c('[data-h="-10"]'); go(7); h.c('[data-h="10"]', 9); go(120); go(45); h.c('[data-h="10"]', 3); go(68); h.c('[data-h="-10"]', 2); },
  'math1-clock-explorer': h => { const f = (s, n) => h.c('button[data-k="t"][data-s="' + s + '"]', n); f(60, 2); f(60, 4); f(30, 1); f(-30, 1); f(-60, 5); f(30, 2); f(60, 3); f(30, 1); f(30, 1); f(60, 5); f(-60, 3); f(-60, 1); },
  'math1-length-measurer': h => { h.c('#lmAdd', 7); h.c('[data-o="0"]'); h.c('#lmAdd', 4); h.c('[data-mode="gaps"]'); h.c('#lmAdd', 3); h.c('[data-mode="overlap"]'); h.c('#lmAdd', 6); h.c('[data-mode="ok"]'); h.c('[data-o="3"]'); h.c('#lmAdd', 11); h.c('[data-o="1"]'); h.c('#lmAdd', 6); },
  'math1-graph-builder': h => { h.setK(0, 5); h.setK(1, 5); h.setK(2, 2); h.c('[data-view="pic"]'); h.setK(2, 7); },
  'math1-equal-shares': h => { h.c('.el-part[data-i="0"]'); h.c('[data-shape="rectangle"]'); h.c('[data-parts="4"]'); h.c('.el-part[data-i="0"]'); h.c('[data-eq="0"]'); h.c('[data-eq="1"]'); h.c('#shAll'); h.c('[data-shape="square"]'); h.c('.el-part[data-i="0"]'); h.c('.el-part[data-i="1"]'); },
  'math2-place-value-blocks': h => { h.setK('h', 3); h.setK('t', 4); h.setK('o', 7); h.setK('h', 4); h.setK('t', 0); h.setK('o', 5); h.setK('h', 0); h.setK('o', 0); h.setK('t', 16); h.c('#pvB2'); h.setK('t', 0); h.setK('h', 10); h.setK('h', 5); h.setK('t', 1); h.setK('o', 2); h.c('#pvK2'); },
  'math2-number-line-jumps': h => { const j = (s, n) => h.c('[data-j="' + s + '"]', n); h.setK('start', 47); j(10, 2); j(1, 5); h.setK('start', 63); j(-10, 2); j(-1, 8); h.setK('start', 38); j(1, 2); j(10, 6); h.setK('start', 250); j(100, 3); h.setK('start', 300); j(-1, 1); h.setK('start', 1000); },
  'math2-array-builder': h => { h.setK('r', 3); h.setK('c', 4); h.setK('r', 4); h.setK('c', 3); h.setK('r', 2); h.setK('c', 5); h.setK('n', 7); h.setK('n', 14); h.setK('r', 4); },
  'math2-bar-model': h => { h.setK('a', 20); h.setK('b', 15); h.c('#bmShow'); h.c('[data-unk="b"]'); h.c('[data-mode="cmp"]'); h.setK('x', 42); h.setK('y', 30); h.setK('y', 42); h.c('[data-mode="ppw"]'); h.setK('a', 60); h.setK('b', 40); },
  'math2-clock-explorer': h => { const f = (s, n) => h.c('button[data-k="t"][data-s="' + s + '"]', n); f(60, 2); f(5, 3); f(60, 4); f(5, 6); f(5, 4); f(-5, 1); f(-60, 2); h.c('#ckPm'); f(60, 6); h.c('#ckPm'); f(60, 2); f(5, 6); },
  'math2-money-counter': h => { h.setK('q', 0); h.setK('d', 2); h.setK('p', 0); h.setK('n', 1); h.setK('d', 0); h.setK('n', 0); h.setK('q', 4); h.setK('q', 1); h.setK('d', 2); h.setK('p', 2); h.setK('b1', 3); h.setK('q', 2); h.setK('d', 0); h.setK('p', 0); h.setK('q', 1); h.setK('d', 2); h.setK('n', 1); },
  'math2-ruler-line-plot': h => {
    const LIN = [5, 3, 7, 5, 6, 4, 7, 5, 8], LCM = [12, 8, 15];
    const ans = (v) => { h.type('#rlIn', v); h.c('#rlCheck'); h.c('#rlNext'); };
    ans(LIN[0]); h.c('[data-z="1"]'); ans(LIN[1]); h.c('[data-u="cm"]'); ans(LCM[2]); h.c('[data-u="in"]'); h.c('[data-z="0"]');
    for (let i = 3; i <= 8; i++) ans(LIN[i]);
  },
  'math2-graph-builder': h => { h.c('[data-view="bar"]'); h.setK(0, 8); h.setK(1, 7); h.setK(3, 1); h.c('[data-view="pic"]'); h.setK(3, 2); h.setK(2, 2); },
  'math2-equal-shares': h => { h.c('[data-parts="3"]'); h.c('.el-part[data-i="0"]'); h.c('#shAll'); h.c('[data-shape="rectangle"]'); h.c('[data-eq="0"]'); h.c('[data-mode="grid"]'); h.setK('cols', 4); h.setK('rows', 3); h.setK('rows', 2); h.setK('cols', 6); h.c('[data-mode="shares"]'); h.c('[data-parts="4"]'); h.c('[data-eq="1"]'); h.c('.el-part[data-i="0"]'); h.c('.el-part[data-i="1"]'); },
  'math3-equal-groups': h => { h.setK('g', 4); h.setK('s', 6); h.setK('g', 6); h.setK('s', 4); h.c('[data-view="array"]'); h.setK('g', 3); h.setK('s', 7); h.c('[data-mode="div"]'); h.setK('T', 24); h.setK('d', 4); h.c('[data-how="group"]'); h.c('[data-how="share"]'); h.setK('d', 5); },
  'math3-break-apart-array': h => { h.setK('r', 7); h.setK('c', 8); h.setK('k', 5); h.setK('r', 6); h.setK('c', 9); h.setK('r', 4); h.setK('c', 6); h.c('#baRot'); h.setK('k', 2); h.setK('r', 8); h.setK('c', 7); h.setK('k', 2); },
  'math3-multiplication-table': h => { const cell = (a, b) => h.c('.el-cell[data-a="' + a + '"][data-b="' + b + '"]'); cell(6, 7); h.setK('row', 4); cell(7, 6); cell(2, 6); cell(3, 4); cell(4, 3); cell(6, 2); h.c('#mtEven'); h.c('#mtPz'); cell(7, 8); },
  'math3-rounding-number-line': h => { h.setK('n', 47); h.c('[data-p="100"]'); h.setK('n', 365); h.setK('n', 350); h.setK('n', 300); h.c('#rnEst'); h.setK('n', 386); h.setK('m', 214); },
  'math3-fraction-explorer': h => { h.c('[data-den="b"][data-v="4"]'); h.setK('a', 3); h.setK('a', 4); h.c('#fxCmp'); h.c('[data-den="b"][data-v="2"]'); h.setK('a', 1); h.c('[data-den="d"][data-v="8"]'); h.setK('c', 4); h.c('[data-den="b"][data-v="8"]'); h.setK('a', 3); h.c('[data-den="d"][data-v="4"]'); h.setK('c', 3); h.c('[data-den="b"][data-v="3"]'); h.setK('a', 6); h.c('[data-den="d"][data-v="3"]'); h.setK('c', 2); },
  'math3-clock-elapsed-time': h => { const f = (s, n) => h.c('button[data-k="t"][data-s="' + s + '"]', n); f(60, 3); f(5, 7); f(1, 2); h.c('[data-c="e"]'); f(60, 8); f(5, 4); f(1, 2); f(-60, 4); f(-5, 6); h.c('[data-c="s"]'); f(-60, 2); f(-5, 4); f(-1, 2); h.c('[data-c="e"]'); f(-60, 2); f(5, 3); f(1, 3); f(5, 7); h.c('[data-c="s"]'); f(60, 8); f(5, 7); h.c('[data-c="e"]'); f(60, 7); },
  'math3-graph-builder': h => { h.setK(0, 8); h.setK(1, 15); h.sel('#grKey', 5); h.c('[data-view="bar"]'); h.sel('#grScale', 10); h.setK(2, 40); h.setK(0, 21); h.setK(2, 8); h.c('[data-view="pic"]'); h.sel('#grKey', 2); },
  'math3-area-perimeter-grid': h => { h.setK('w', 4); h.setK('h', 3); h.setK('w', 6); h.setK('h', 2); h.setK('h', 4); h.setK('w', 4); h.c('[data-mode="paint"]'); [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [3, 0]].forEach(p => h.c('.el-cell[data-r="' + p[0] + '"][data-c="' + p[1] + '"]')); h.c('[data-mode="rect"]'); h.setK('w', 5); h.setK('h', 5); },
};

const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.pdf': 'application/pdf', '.json': 'application/json', '.jpg': 'image/jpeg', '.png': 'image/png' };
const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': mime[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });

(async () => {
  await new Promise(r => srv.listen(8767, r));
  const b = await pw.chromium.launch(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {}); let fails = 0;
  for (const tool of M) {
    const errs = [], p = await b.newPage({ viewport: { width: 1280, height: 800 } });
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); p.on('pageerror', e => errs.push(String(e)));
    const url = `http://localhost:8767/artifacts/${tool.slug}/index.html`;
    try {
      await p.goto(url); await p.addScriptTag({ content: HELPERS });
      const pre = await p.$$eval('.tl-ch li.done', l => l.length), total = await p.$$eval('.tl-ch li', l => l.length);
      if (pre) throw Error(pre + ' challenge(s) already ticked on load');
      if (total !== 6) throw Error('expected 6 challenges, found ' + total);
      if (!SOLVE[tool.slug]) throw Error('no solver');
      await p.evaluate(`(${SOLVE[tool.slug].toString()})(window.__h)`);
      const done = await p.$$eval('.tl-ch li', l => l.map(x => x.classList.contains('done')));
      if (done.some(d => !d)) throw Error('challenges not reached: ' + done.map((d, i) => d ? '' : i + 1).filter(Boolean).join(', '));
      // teacher view
      await p.click('#tsMode'); const links = await p.$$eval('#tsTeacher a', a => a.map(x => x.getAttribute('href')));
      if (!links.includes('worksheet.pdf') || !links.includes('teacher-key.pdf')) throw Error('teacher view links missing');
      if (!(await p.$eval('#notice details', d => d.open))) throw Error('teacher view should open the notice panel');
      // fuzz every enabled, visible button
      const n = await p.$$eval('#workspace button', l => l.length);
      for (let k = 0; k < Math.min(220, n * 6); k++) await p.evaluate(() => { const l = [...document.querySelectorAll('#workspace button, #workspace .el-part, #workspace .el-cell')].filter(x => !x.disabled && x.getClientRects().length); const x = l[Math.floor(Math.random() * l.length)]; if (x) x.dispatchEvent(new MouseEvent('click', { bubbles: true })); });
      await p.click('#tsReset'); await p.click('#tsFit');
      const fits = await p.evaluate(() => document.getElementById('workspace').getBoundingClientRect().bottom <= innerHeight + 2 && document.documentElement.scrollWidth <= innerWidth + 1);
      if (!fits) throw Error('Fit leaves the workspace off screen');
      if (await p.$$eval('.tl-ch li.done', l => l.length)) throw Error('Reset did not clear ticks');
      if (errs.length) throw Error('console: ' + errs.slice(0, 3).join(' | '));
      console.log('ok  ', tool.slug);
    } catch (e) { fails++; console.log('FAIL', tool.slug, '—', e.message); }
    await p.close();
  }
  await b.close(); srv.close();
  console.log(fails ? fails + ' tool(s) failed' : 'PASS: ' + M.length + ' tools load cleanly, all challenges reachable, teacher links present, Fit keeps the workspace on screen');
  process.exit(fails ? 1 : 0);
})();
