/* Real-browser smoke test for every Financial Algebra page (optional; needs Playwright + Chromium).
 * Usage: node tests/fa-browser.cjs   (starts its own static server on a free port) */
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.pdf': 'application/pdf' };
const server = http.createServer((q, s) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f.endsWith('/') ? f + 'index.html' : f, (e, d) => { if (e) { s.writeHead(404); s.end(); } else { s.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); s.end(d); } }); });
const units = JSON.parse(fs.readFileSync(path.join(root, 'financial/resources.json'))).units;
(async () => {
  await new Promise(r => server.listen(0, r)); const base = 'http://localhost:' + server.address().port + '/';
  const b = await chromium.launch(); const failures = []; let checks = 0;
  async function visit(url, fn, viewport) {
    const p = await b.newPage({ viewport: viewport || { width: 1100, height: 900 } }); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/fonts\.g|ERR_TUNNEL|ERR_NAME|net::/.test(m.text())) errs.push(m.text()); });
    p.on('requestfailed', r => { if (!/fonts\.g/.test(r.url())) errs.push('request failed ' + r.url()); });
    await p.goto(base + url); await p.waitForTimeout(250);
    try { await fn(p); } catch (e) { errs.push(e.message); }
    const overflow = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    if (viewport && overflow > 2) errs.push('horizontal overflow ' + overflow + 'px');
    if (errs.length) failures.push(url + ' → ' + errs.join(' | ')); checks++; await p.close();
  }
  const count = (p, sel) => p.$$eval(sel, x => x.length);
  for (const u of units) {
    const r = u.resources;
    for (const mode of ['worksheet', 'assessment', 'lesson', 'practice']) await visit(r[{ worksheet: 'worksheet', assessment: 'assessment', lesson: 'lessonPlan', practice: 'practiceTest' }[mode]], async p => { if (await count(p, '.fa-q') < 3) throw Error(mode + ' rendered too few questions'); });
    await visit(r.worksheet, async p => { for (const f of ['case-study', 'compare', 'document', 'analysis', 'decision', 'vocabulary', 'math', 'mixed']) { await p.selectOption('#wsFormat', f); await p.click('#go'); if (await count(p, '.fa-sheet:first-child .fa-q') < 2) throw Error('format ' + f + ' empty'); } });
    await visit(r.lessonPlan, async p => { for (const o of await p.$$eval('#lessonSkill option', x => x.map(y => y.value))) { await p.selectOption('#lessonSkill', o); await p.click('#go'); if (!(await p.textContent('#output')).includes('Learning objectives')) throw Error('lesson ' + o); } });
    await visit(r.flashcards, async p => { await p.click('#card'); await p.click('#know'); if (!/Card 1 of/.test(await p.textContent('#status'))) throw Error('flashcards status'); });
    await visit(r.decisionLab.teacherPath, async p => { for (let s = 0; s < 7; s++) await p.click(`button[data-step="${s}"]`); await p.click('button[data-step="4"]'); const rng = await p.$('input[type=range]'); if (rng) { await rng.fill(await rng.getAttribute('max')); await rng.dispatchEvent('input'); } if (await count(p, '#live table') !== 1) throw Error('lab table'); });
    await visit(r.decisionLab.path, async () => {}, { width: 390, height: 844 });
    await visit(r.worksheet, async () => {}, { width: 390, height: 844 });
    await visit(r.cheatSheet.replace('cheat-sheet.pdf', 'cheat-sheet.html'), async () => {});
    for (const pr of r.projects) await visit(pr.path, async p => { for (const h of await p.$$eval('a[href]', x => x.map(a => a.getAttribute('href')))) if (!fs.existsSync(path.join(root, path.dirname(pr.path), h))) throw Error('broken link ' + h); });
  }
  await visit('financial/index.html', async p => { if (await count(p, '.hub-link') < 80) throw Error('hub links'); });
  await visit('financial/index.html', async () => {}, { width: 390, height: 844 });
  await b.close(); server.close();
  console.log(`${checks} page checks, ${failures.length} failures`); failures.forEach(f => console.log('FAIL', f));
  process.exit(failures.length ? 1 : 0);
})();
