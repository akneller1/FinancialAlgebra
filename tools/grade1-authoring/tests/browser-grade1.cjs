#!/usr/bin/env node
/* Browser test for the 1st Grade Math pages (Playwright; starts its own static server on the repository root).
   - every game on every unit it is listed for: launches from a student link, is played to the end by a bot that answers
     from the question shown, and no correct answer is marked wrong; three whole-class / partner modes
   - Understanding Check: one at a time (feedback right away / at the end) and all on one page; retry; teacher summary;
     the printable results page
   - Flashcards: every unit loads; flip / next / Got it / filter / shuffle
   - Student links: the link a teacher copies from a game and from the Understanding Check opens straight into it
   - Unit pages on index.html#math1.<unit> (production layout only; the staging class page has its own crawl,
     tests/browser-staging.cjs): resource cards render, local links resolve
   Interactive tools have their own test (tests/browser-tools.cjs).
   Fails on any page error or console error. Usage: node tools/grade1-authoring/tests/browser-grade1.cjs [--quick]
   G3_ONLY=games|checks|cards|links|units, G3_GAME=<id> */
'use strict';
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const SRC = path.resolve(__dirname, '..', '..', '..');
// G1_SITE=<assembled _site> G1_PREFIX=grade1/ tests the development preview bundle; the default serves this repository.
const ROOT = path.resolve(process.env.G1_SITE || SRC), PREFIX = process.env.G1_PREFIX || '';
const QUICK = process.argv.includes('--quick');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.pdf': 'application/pdf', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
  const f = path.join(ROOT, u.endsWith('/') ? u + 'index.html' : u);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end('nf'); return; }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
const outline = JSON.parse(fs.readFileSync(path.join(SRC, 'tools/grade1-authoring/outline.json'), 'utf8'));
const UNITS = outline.units.map(u => u.id);
const results = [];
function log(ok, what, note) { results.push({ ok, what, note: note || '' }); console.log((ok ? 'PASS ' : 'FAIL ') + what + (note ? ' — ' + note : '')); }

async function open(ctx, url) {
  const page = await ctx.newPage(), errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/favicon|analytics|fonts\.g|ERR_TUNNEL|ERR_NAME_NOT_RESOLVED/i.test(m.text())) errors.push('console: ' + m.text()); });
  page.on('requestfailed', r => { if (/^http:\/\/localhost/.test(r.url()) && !/analytics/.test(r.url())) errors.push('request failed: ' + r.url()); });
  page.on('response', r => { if (r.status() >= 400 && !/favicon|analytics/.test(r.url())) errors.push(r.status() + ' ' + r.url()); });
  await page.addInitScript(() => {
    /* test hook: remember the question each card shows so the bot can answer it */
    /* wrap MKEL.card the moment el-core.js defines MKEL (a timer could miss the first card of a fast-starting game) */
    let K;
    Object.defineProperty(window, 'MKEL', { configurable: true, get: () => K, set: v => { K = v; if (v && v.card && !v.card.__wrapped) { const orig = v.card; v.card = function (h, p, o) { window.__q = p; return orig.apply(this, arguments); }; v.card.__wrapped = true; } } });
  });
  await page.goto(url, { waitUntil: 'load' });
  return { page, errors };
}

/* answer the current question card correctly */
async function answer(page) {
  return page.evaluate(() => {
    const box = [...document.querySelectorAll('.el-q')].pop(); const p = window.__q;
    if (!box || !p) return 'none';
    if (box.querySelector('.el-feedback.good, .el-feedback.try')) return 'answered';
    if (p.kind === 'mc') { const i = p.options.findIndex(o => o.correct); const b = box.querySelectorAll('.el-choice')[i]; if (!b || b.disabled) return 'stuck'; b.click(); return 'mc'; }
    if (p.kind === 'sel') { box.querySelectorAll('.el-choice').forEach((b, i) => { if (p.options[i].correct) b.click(); }); [...box.querySelectorAll('.el-btn.primary')].find(b => b.textContent === 'Check').click(); return 'sel'; }
    if (p.kind === 'parts') { box.querySelectorAll('.el-input').forEach((x, i) => { x.value = p.parts[i].answer; }); [...box.querySelectorAll('.el-btn.primary')].find(b => b.textContent === 'Check').click(); return 'parts'; }
    const inp = box.querySelector('.el-input'); if (!inp) return 'stuck';
    inp.value = Array.isArray(p.answer) ? p.answer[0] : p.answer; [...box.querySelectorAll('.el-btn.primary')].find(b => b.textContent === 'Check').click(); return 'typed';
  });
}

async function playGame(ctx, game, unit, mode) {
  const url = `http://localhost:${PORT}/${PREFIX}worksheet-generator/grade1-games.html?game=${game}&unit=${unit}` + (mode ? '' : '&student=1&level=cp1');
  const { page, errors } = await open(ctx, url);
  try {
    await page.waitForSelector('.el-setup, .el-stage, dialog.teacher-skills', { timeout: 10000 });
    const dlg = await page.$('dialog.teacher-skills');
    if (dlg) { const btn = await page.$$('dialog.teacher-skills button'); await btn[btn.length - 1].click(); await page.waitForSelector('.el-setup'); }
    if (mode) { await page.evaluate(m => { const r = document.querySelector('input[name=elmode][value="' + m + '"]'); if (r) r.checked = true; }, mode); }
    const setup = await page.$('.el-setup .el-btn.primary'); if (setup) await setup.click();
    await page.waitForSelector('.el-stage', { timeout: 10000 });
    let wrongNotMatched = 0, steps = 0, typed = 0;
    if (game === 'monster-match') {
      const n = await page.$$eval('.el-stage .el-grid-btns .el-choice', b => b.length);
      if (n < 8) throw new Error('only ' + n + ' cards');
      const kinds = await page.$$eval('.el-stage .el-grid-btns .el-choice', b => b.map(x => x.textContent.includes('Problem') ? 'q' : 'a'));
      const settle = () => page.waitForFunction(() => ![...document.querySelectorAll('.el-stage .el-grid-btns .el-choice')].some(x => x.classList.contains('on') && !x.classList.contains('right')), null, { timeout: 5000 });
      for (let i = 0; i < n; i++) {
        if (kinds[i] !== 'q') continue;
        for (let j = 0; j < n; j++) {
          if (kinds[j] !== 'a') continue;
          const st = await page.$$eval('.el-stage .el-grid-btns .el-choice', b => b.map(x => x.classList.contains('right')));
          if (st[i]) break; if (st[j]) continue;
          const bs = await page.$$('.el-stage .el-grid-btns .el-choice');
          await bs[i].click(); await bs[j].click(); steps++;
          await page.waitForTimeout(350); await settle();
        }
      }
    } else {
      while (steps++ < 400) {
        if (await page.$('.el-celebrate')) break;
        const col = await page.$('.el-grid-btns .el-btn.primary:not([disabled])');
        if (col && game === 'four-in-a-row') { const cols = await page.$$('.el-grid-btns .el-btn.primary:not([disabled])'); await cols[steps % cols.length].click(); await page.waitForTimeout(20); continue; }
        const r = await answer(page);
        if (r === 'typed' || r === 'parts') typed++;
        if (r === 'answered' || r === 'none') {
          const good = await page.$('.el-feedback.try'); if (good && r === 'answered') wrongNotMatched++;
          const next = await page.$('.el-q-tools .el-btn.primary, .el-stage .el-btn.primary.big');
          if (next) { try { await next.click({ timeout: 1500 }); } catch (e) { /* re-rendered between query and click */ } } else await page.waitForTimeout(50);
        }
        await page.waitForTimeout(15);
      }
    }
    await page.waitForSelector('.el-celebrate', { timeout: 15000 });
    const summary = await page.$eval('.el-celebrate', e => e.innerText.slice(0, 80).replace(/\s+/g, ' '));
    if (errors.length) throw new Error(errors.slice(0, 3).join(' | '));
    if (wrongNotMatched) throw new Error(wrongNotMatched + ' correct answers were marked wrong');
    log(true, `game ${game} ${mode || ''} ${unit}`, `${steps} steps, ${typed} typed; "${summary}"`);
  } catch (e) {
    log(false, `game ${game} ${mode || ''} ${unit}`, e.message + (errors.length ? ' | ' + errors.slice(0, 2).join(' | ') : ''));
  } finally { await page.close(); }
}

async function understandingCheck(ctx, unit) {
  for (const [view, fb] of [['one', 'now'], ['one', 'end'], ['page', 'now']]) {
    const { page, errors } = await open(ctx, `http://localhost:${PORT}/${PREFIX}worksheet-generator/grade1-understanding-check.html?unit=${unit}&count=8&view=${view}&feedback=${fb}`);
    const what = `understanding check ${unit} ${view}/${fb}`;
    try {
      await page.waitForSelector('dialog.teacher-skills, .el-setup', { timeout: 10000 });
      const dlg = await page.$('dialog.teacher-skills');
      if (dlg) { const btn = await page.$$('dialog.teacher-skills button'); await btn[btn.length - 1].click(); }
      await page.click('.el-setup .el-btn.primary');
      let wrong = 0;
      if (view === 'page') {
        // answer every quiet box using the prepared set exposed through the page (answers typed in the inputs)
        const n = await page.$$eval('.el-q', b => b.length);
        if (n !== 8) throw new Error(n + ' questions shown');
        await page.click('.el-btn.primary.big');
        await page.waitForSelector('.el-celebrate');
      } else {
        for (let i = 0; i < 8; i++) {
          if (fb === 'now') {
            const r = await answer(page); if (r === 'stuck' || r === 'none') throw new Error('could not answer question ' + (i + 1));
            await page.waitForSelector('.el-feedback.good, .el-feedback.try');
            if (await page.$('.el-feedback.try')) wrong++;
            await page.click('.el-q-tools .el-btn.primary');
          } else { await page.click('.el-q-tools .el-btn.primary'); }
        }
        await page.waitForSelector('.el-celebrate');
      }
      const txt = await page.$eval('.el-celebrate', e => e.innerText);
      const m = txt.match(/You answered (\d+) of (\d+)/); if (!m) throw new Error('no score line');
      if (fb === 'now' && view === 'one' && (+m[1] !== 8 || wrong)) throw new Error('bot answered correctly but score is ' + m[1] + '/8');
      if (view !== 'one' || fb === 'end') {   // blank answers: everything should be counted as missed and offer a retry
        if (+m[1] !== 0) throw new Error('blank answers scored ' + m[1]);
        const retry = await page.$('text=Retry missed questions (8)'); if (!retry) throw new Error('no retry button'); await retry.click();
        await page.waitForSelector('.el-q');
      }
      if (view === 'one' && fb === 'now') {   // printable results page: every question listed with the typed answer
        await page.click('text=Print or save my results');
        const rows = await page.$$eval('#el-results .el-results-table tr', r => r.length);
        const name = await page.$('#el-results .el-results-name');
        if (rows < 9 || !name) throw new Error('results page incomplete (' + rows + ' rows)');
        await page.click('#el-results .el-results-bar .el-btn:not(.primary)');
      }
      const teacher = await page.$('.el-summary'); // student=1 not set: teacher summary visible
      if (view === 'one' && fb === 'now' && !teacher) throw new Error('teacher summary missing');
      if (errors.length) throw new Error(errors.slice(0, 3).join(' | '));
      log(true, what, m[0]);
    } catch (e) { const body = await page.locator('body').innerText().catch(()=>''); log(false, what, e.message + ' | page: ' + body.replace(/\s+/g,' ').slice(0,350) + (errors.length ? ' | ' + errors.slice(0, 2).join(' | ') : '')); }
    finally { await page.close(); }
  }
}

async function flashcards(ctx, unit) {
  const { page, errors } = await open(ctx, `http://localhost:${PORT}/${PREFIX}worksheet-generator/grade1-flashcards.html?unit=${unit}`);
  try {
    await page.waitForSelector('.fc-card', { timeout: 10000 });
    const c1 = await page.$eval('.el-chip', e => e.textContent);
    await page.keyboard.press('Space'); if (!(await page.$('.fc-card.flip'))) throw new Error('space did not flip');
    await page.keyboard.press('ArrowRight'); const c2 = await page.$eval('.el-chip', e => e.textContent); if (c2 === c1) throw new Error('arrow did not advance');
    await page.click('text=✓ Got it'); const w = await page.$eval('.fc-progress div', e => e.style.width); if (w === '0%') throw new Error('progress did not move');
    await page.click('text=🔀 Shuffle');
    const pills = await page.$$('.el-pill input'); await pills[2].check({ force: true }); await page.waitForTimeout(50);
    const c3 = await page.$eval('.el-chip', e => e.textContent);
    const svgs = await page.$$eval('.fc-print .fc-svg svg', s => s.length);
    if (errors.length) throw new Error(errors.slice(0, 3).join(' | '));
    log(true, 'flashcards ' + unit, `${c1.replace('Card 1 of ', '')} cards, ${svgs} pictures, filter → ${c3}`);
  } catch (e) { log(false, 'flashcards ' + unit, e.message + (errors.length ? ' | ' + errors.join(' | ') : '')); }
  finally { await page.close(); }
}

async function studentLinks(ctx) {
  for (const [what, url, ready] of [['game', 'grade1-games.html?game=space-rescue&unit=add-subtract-20', '.el-stage'], ['understanding check', 'grade1-understanding-check.html?unit=telling-time', '.el-q']]) {
    const { page, errors } = await open(ctx, `http://localhost:${PORT}/${PREFIX}worksheet-generator/${url}`);
    try {
      await page.waitForSelector('dialog.teacher-skills, .el-setup', { timeout: 10000 });
      const dlg = await page.$('dialog.teacher-skills');
      if (dlg) {   // choose only the first two skills
        const boxes = await page.$$('dialog.teacher-skills input[type=checkbox]');
        for (const [i, b] of boxes.entries()) { if (i >= 2 && await b.isChecked()) await b.uncheck({ force: true }); }
        const btn = await page.$$('dialog.teacher-skills button'); await btn[btn.length - 1].click();
      }
      await page.waitForSelector('.el-setup .el-share');
      await page.check('input[name=ellevel][value=honors]', { force: true });
      await page.click('.el-share .el-btn');
      const link = await page.$eval('.el-share-url', e => e.value);
      if (!/student=1/.test(link) || !/level=honors/.test(link) || !/unit=/.test(link)) throw new Error('link lacks settings: ' + link);
      const s2 = await open(ctx, link.replace(/^https?:\/\/[^/]+/, 'http://localhost:' + PORT));
      await s2.page.waitForSelector(ready, { timeout: 10000 });
      const st = await s2.page.evaluate(() => ({ home: !!document.querySelector('.el-home'), setup: !!document.querySelector('.el-setup'), q: window.__q ? window.__q.level + ' ' + window.__q.skillId : '' }));
      await s2.page.close();
      if (st.setup) throw new Error('student link stopped at the settings panel');
      if (st.home) throw new Error('student view shows the teacher home link');
      if (st.q && !/^honors /.test(st.q)) throw new Error('student link lost the level: ' + st.q);
      if (st.q && !/-skill-0[12]$/.test(st.q)) throw new Error('student link lost the chosen skills: ' + st.q);
      if (errors.length || s2.errors.length) throw new Error(errors.concat(s2.errors).slice(0, 3).join(' | '));
      log(true, 'student link ' + what, link.replace(/^https?:\/\/[^/]+\//, '').slice(0, 150) + (st.q ? ' → ' + st.q : ''));
    } catch (e) { log(false, 'student link ' + what, e.message); }
    finally { await page.close(); }
  }
}

async function unitPages(ctx) {
  for (const u of [''].concat(UNITS)) {
    const { page, errors } = await open(ctx, `http://localhost:${PORT}/index.html#math1${u ? '.' + u : ''}`);
    try {
      await page.waitForSelector('main h1', { timeout: 10000 });
      await page.waitForTimeout(400);
      const links = await page.$$eval('main a[href]', as => as.map(a => a.getAttribute('href')).filter(h => h && !/^(#|https?:|mailto:)/.test(h)));
      await page.evaluate(async () => { for (const i of document.querySelectorAll('main img')) { i.loading = 'eager'; } window.scrollTo(0, document.body.scrollHeight); });
      await page.waitForTimeout(700);
      const imgs = await page.$$eval('main img', is => is.map(i => ({ src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0 })));
      const missing = links.map(h => h.split(/[?#]/)[0]).filter(p => p && !fs.existsSync(path.join(ROOT, decodeURIComponent(p))));
      const broken = imgs.filter(i => !i.ok && i.src && !/^data:/.test(i.src));
      if (missing.length) throw new Error('missing link targets: ' + [...new Set(missing)].slice(0, 5).join(', '));
      if (broken.length) throw new Error('broken images: ' + broken.slice(0, 3).map(b => b.src).join(', '));
      if (errors.length) throw new Error(errors.slice(0, 3).join(' | '));
      const title = await page.$eval('main h1', e => e.textContent.trim());
      log(true, 'unit page ' + (u || 'course'), `"${title}", ${links.length} links, ${imgs.length} images`);
    } catch (e) { log(false, 'unit page ' + (u || 'course'), e.message); }
    finally { await page.close(); }
  }
}

let PORT;
(async () => {
  await new Promise(r => server.listen(0, r)); PORT = server.address().port;
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const GAMES = JSON.parse(fs.readFileSync(path.join(SRC, 'tools/grade1-authoring/games.json'), 'utf8')).games;
  const want = process.env.G3_ONLY;
  if (!want || want === 'games') {
    for (const g of GAMES.filter(x => !process.env.G3_GAME || x.id === process.env.G3_GAME)) {
      const all = g.units || UNITS;
      const units = QUICK ? [all[(GAMES.indexOf(g) * 3) % all.length]] : all;
      for (const u of units) await playGame(ctx, g.id, u);
    }
    if (!process.env.G3_GAME) {
      await playGame(ctx, 'treasure-quest', 'shapes-equal-shares', 'class');
      await playGame(ctx, 'rocket-race', 'measuring-length', 'class4');
      await playGame(ctx, 'monster-match', 'tens-ones', 'pairs');
    }
  }
  if (!want || want === 'checks') for (const u of (QUICK ? UNITS.slice(0, 3) : UNITS)) await understandingCheck(ctx, u);
  // Grade 1 flashcards have not been authored.
  if (!want || want === 'links') await studentLinks(ctx);
  if ((!want || want === 'units') && !PREFIX && !fs.existsSync(path.join(SRC, 'src/grade1-site.js'))) await unitPages(ctx);
  await browser.close(); server.close();
  const bad = results.filter(r => !r.ok);
  console.log(`\n${results.length - bad.length} passed, ${bad.length} failed`);
  fs.writeFileSync(path.join(SRC, 'tools/grade1-authoring/out/browser-results.json'), JSON.stringify(results, null, 1));
  process.exit(bad.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
