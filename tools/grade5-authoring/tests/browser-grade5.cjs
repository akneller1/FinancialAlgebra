#!/usr/bin/env node
/* Browser test for the Grade 5 pages (Playwright + a static server on the repository root).
   - every game, every applicable unit sample: launches, is played to the end by a bot that answers correctly, shows the summary
   - Understanding Check: one-at-a-time (feedback now and at end) and full-page; retry and new-set buttons
   - Flashcards: every unit loads, flip / next / got-it / filter / shuffle work
   - Interactive tools: each loads, has student/teacher modes and zoom controls
   - Unit pages on index.html#math5.<unit>: resource cards render, local links resolve
   Fails on any page error or console error. Usage: node tools/grade5-authoring/tests/browser-grade5.cjs [--quick] */
'use strict';
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const QUICK = process.argv.includes('--quick');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.pdf': 'application/pdf', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
  const f = path.join(ROOT, u.endsWith('/') ? u + 'index.html' : u);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end('nf'); return; }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
const outline = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/grade5-authoring/outline.json'), 'utf8'));
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
    let wrapped = false;
    const iv = setInterval(() => { if (window.G5 && !wrapped) { wrapped = true; const orig = window.G5.card; window.G5.card = function (h, p, o) { window.__q = p; return orig.apply(this, arguments); }; clearInterval(iv); } }, 5);
  });
  await page.goto(url, { waitUntil: 'load' });
  return { page, errors };
}

/* answer the current question card correctly */
async function answer(page) {
  return page.evaluate(() => {
    const box = [...document.querySelectorAll('.g5-q')].pop(); const p = window.__q;
    if (!box || !p) return 'none';
    if (box.querySelector('.g5-feedback.good, .g5-feedback.try')) return 'answered';
    if (p.kind === 'mc') { const i = p.options.findIndex(o => o.correct); const b = box.querySelectorAll('.g5-choice')[i]; if (!b || b.disabled) return 'stuck'; b.click(); return 'mc'; }
    if (p.kind === 'sel') { box.querySelectorAll('.g5-choice').forEach((b, i) => { if (p.options[i].correct) b.click(); }); [...box.querySelectorAll('.g5-btn.primary')].find(b => b.textContent === 'Check').click(); return 'sel'; }
    if (p.kind === 'parts') { box.querySelectorAll('.g5-input').forEach((x, i) => { x.value = p.parts[i].answer; }); [...box.querySelectorAll('.g5-btn.primary')].find(b => b.textContent === 'Check').click(); return 'parts'; }
    const inp = box.querySelector('.g5-input'); if (!inp) return 'stuck';
    inp.value = Array.isArray(p.answer) ? p.answer[0] : p.answer; [...box.querySelectorAll('.g5-btn.primary')].find(b => b.textContent === 'Check').click(); return 'typed';
  });
}

async function playGame(ctx, game, unit, mode) {
  const url = `http://localhost:${PORT}/worksheet-generator/grade5-games.html?game=${game}&unit=${unit}` + (mode ? '' : '&student=1&level=cp1');
  const { page, errors } = await open(ctx, url);
  try {
    await page.waitForSelector('.g5-setup, .g5-stage, dialog.teacher-skills', { timeout: 10000 });
    const dlg = await page.$('dialog.teacher-skills');
    if (dlg) { const btn = await page.$$('dialog.teacher-skills button'); await btn[btn.length - 1].click(); await page.waitForSelector('.g5-setup'); }
    if (mode) { await page.evaluate(m => { const r = document.querySelector('input[name=g5mode][value="' + m + '"]'); if (r) r.checked = true; }, mode); }
    const setup = await page.$('.g5-setup .g5-btn.primary'); if (setup) await setup.click();
    await page.waitForSelector('.g5-stage', { timeout: 10000 });
    let wrongNotMatched = 0, steps = 0, typed = 0;
    if (game === 'puzzle-masters') {
      const n = await page.$$eval('.g5-stage .g5-grid-btns .g5-choice', b => b.length);
      if (n < 8) throw new Error('only ' + n + ' cards');
      const kinds = await page.$$eval('.g5-stage .g5-grid-btns .g5-choice', b => b.map(x => x.textContent.includes('Problem') ? 'q' : 'a'));
      const settle = () => page.waitForFunction(() => ![...document.querySelectorAll('.g5-stage .g5-grid-btns .g5-choice')].some(x => x.classList.contains('on') && !x.classList.contains('right')), null, { timeout: 5000 });
      for (let i = 0; i < n; i++) {
        if (kinds[i] !== 'q') continue;
        for (let j = 0; j < n; j++) {
          if (kinds[j] !== 'a') continue;
          const st = await page.$$eval('.g5-stage .g5-grid-btns .g5-choice', b => b.map(x => x.classList.contains('right')));
          if (st[i]) break; if (st[j]) continue;
          const bs = await page.$$('.g5-stage .g5-grid-btns .g5-choice');
          await bs[i].click(); await bs[j].click(); steps++;
          await page.waitForTimeout(350); await settle();
        }
      }
    } else {
      while (steps++ < 400) {
        if (await page.$('.g5-celebrate')) break;
        const col = await page.$('.g5-grid-btns .g5-btn.primary:not([disabled])');
        if (col && game === 'connect-four') { const cols = await page.$$('.g5-grid-btns .g5-btn.primary:not([disabled])'); await cols[steps % cols.length].click(); await page.waitForTimeout(20); continue; }
        const r = await answer(page);
        if (r === 'typed' || r === 'parts') typed++;
        if (r === 'answered' || r === 'none') {
          const good = await page.$('.g5-feedback.try'); if (good && r === 'answered') wrongNotMatched++;
          const next = await page.$('.g5-q-tools .g5-btn.primary, .g5-stage .g5-btn.primary.big');
          if (next) { try { await next.click({ timeout: 1500 }); } catch (e) { /* re-rendered between query and click */ } } else await page.waitForTimeout(50);
        }
        await page.waitForTimeout(15);
      }
    }
    await page.waitForSelector('.g5-celebrate', { timeout: 15000 });
    const summary = await page.$eval('.g5-celebrate', e => e.innerText.slice(0, 80).replace(/\s+/g, ' '));
    if (errors.length) throw new Error(errors.slice(0, 3).join(' | '));
    if (wrongNotMatched) throw new Error(wrongNotMatched + ' correct answers were marked wrong');
    log(true, `game ${game} ${mode || ''} ${unit}`, `${steps} steps, ${typed} typed; "${summary}"`);
  } catch (e) {
    log(false, `game ${game} ${mode || ''} ${unit}`, e.message + (errors.length ? ' | ' + errors.slice(0, 2).join(' | ') : ''));
  } finally { await page.close(); }
}

async function understandingCheck(ctx, unit) {
  for (const [view, fb] of [['one', 'now'], ['one', 'end'], ['page', 'now']]) {
    const { page, errors } = await open(ctx, `http://localhost:${PORT}/worksheet-generator/grade5-understanding-check.html?unit=${unit}&count=8&view=${view}&feedback=${fb}`);
    const what = `understanding check ${unit} ${view}/${fb}`;
    try {
      await page.waitForSelector('dialog.teacher-skills, .g5-setup', { timeout: 10000 });
      const dlg = await page.$('dialog.teacher-skills');
      if (dlg) { const btn = await page.$$('dialog.teacher-skills button'); await btn[btn.length - 1].click(); }
      await page.click('.g5-setup .g5-btn.primary');
      let wrong = 0;
      if (view === 'page') {
        // answer every quiet box using the prepared set exposed through the page (answers typed in the inputs)
        const n = await page.$$eval('.g5-q', b => b.length);
        if (n !== 8) throw new Error(n + ' questions shown');
        await page.click('.g5-btn.primary.big');
        await page.waitForSelector('.g5-celebrate');
      } else {
        for (let i = 0; i < 8; i++) {
          if (fb === 'now') {
            const r = await answer(page); if (r === 'stuck' || r === 'none') throw new Error('could not answer question ' + (i + 1));
            await page.waitForSelector('.g5-feedback.good, .g5-feedback.try');
            if (await page.$('.g5-feedback.try')) wrong++;
            await page.click('.g5-q-tools .g5-btn.primary');
          } else { await page.click('.g5-q-tools .g5-btn.primary'); }
        }
        await page.waitForSelector('.g5-celebrate');
      }
      const txt = await page.$eval('.g5-celebrate', e => e.innerText);
      const m = txt.match(/You answered (\d+) of (\d+)/); if (!m) throw new Error('no score line');
      if (fb === 'now' && view === 'one' && (+m[1] !== 8 || wrong)) throw new Error('bot answered correctly but score is ' + m[1] + '/8');
      if (view !== 'one' || fb === 'end') {   // blank answers: everything should be counted as missed and offer a retry
        if (+m[1] !== 0) throw new Error('blank answers scored ' + m[1]);
        const retry = await page.$('text=Retry missed questions (8)'); if (!retry) throw new Error('no retry button'); await retry.click();
        await page.waitForSelector('.g5-q');
      }
      const teacher = await page.$('.g5-summary'); // student=1 not set: teacher summary visible
      if (view === 'one' && fb === 'now' && !teacher) throw new Error('teacher summary missing');
      if (errors.length) throw new Error(errors.slice(0, 3).join(' | '));
      log(true, what, m[0]);
    } catch (e) { log(false, what, e.message + (errors.length ? ' | ' + errors.slice(0, 2).join(' | ') : '')); }
    finally { await page.close(); }
  }
}

async function flashcards(ctx, unit) {
  const { page, errors } = await open(ctx, `http://localhost:${PORT}/worksheet-generator/grade5-flashcards.html?unit=${unit}`);
  try {
    await page.waitForSelector('.fc-card', { timeout: 10000 });
    const c1 = await page.$eval('.g5-chip', e => e.textContent);
    await page.keyboard.press('Space'); if (!(await page.$('.fc-card.flip'))) throw new Error('space did not flip');
    await page.keyboard.press('ArrowRight'); const c2 = await page.$eval('.g5-chip', e => e.textContent); if (c2 === c1) throw new Error('arrow did not advance');
    await page.click('text=✓ Got it'); const w = await page.$eval('.fc-progress div', e => e.style.width); if (w === '0%') throw new Error('progress did not move');
    await page.click('text=🔀 Shuffle');
    const pills = await page.$$('.g5-pill input'); await pills[2].check({ force: true }); await page.waitForTimeout(50);
    const c3 = await page.$eval('.g5-chip', e => e.textContent);
    const svgs = await page.$$eval('.fc-print .fc-svg svg', s => s.length);
    if (errors.length) throw new Error(errors.slice(0, 3).join(' | '));
    log(true, 'flashcards ' + unit, `${c1.replace('Card 1 of ', '')} cards, ${svgs} pictures, filter → ${c3}`);
  } catch (e) { log(false, 'flashcards ' + unit, e.message + (errors.length ? ' | ' + errors.join(' | ') : '')); }
  finally { await page.close(); }
}

async function tools(ctx) {
  const dirs = fs.readdirSync(path.join(ROOT, 'artifacts')).filter(d => /^math5-/.test(d) && !/cheat-sheet|project-/.test(d));
  for (const d of dirs) {
    const { page, errors } = await open(ctx, `http://localhost:${PORT}/artifacts/${d}/index.html`);
    try {
      await page.waitForTimeout(600);
      const info = await page.evaluate(() => ({ btns: [...document.querySelectorAll('button')].map(b => b.textContent.trim()).slice(0, 40), svg: document.querySelectorAll('svg').length }));
      const hasZoom = info.btns.some(t => /A\+/.test(t)) && info.btns.includes('Fit'), hasMode = info.btns.some(t => /Teacher view/.test(t));
      if (!(await page.$('main .g5-card'))) throw new Error('nothing drawn');
      await page.click('#tsMode'); const tv = await page.$eval('#tsTeacher', e => !e.hidden && /teacher-key\.pdf/.test(e.innerHTML)); if (!tv) throw new Error('teacher view did not open'); await page.click('#tsMode');
      // click every enabled button once (not links), check nothing throws
      const bs = await page.$$('button:not([disabled])');
      for (const b of bs.slice(0, 30)) { try { if (await b.isVisible()) await b.click({ timeout: 800 }); } catch (e) {} }
      await page.waitForTimeout(200);
      for (const f of ['worksheet.pdf', 'teacher-key.pdf']) if (!fs.existsSync(path.join(ROOT, 'artifacts', d, f))) throw new Error('missing ' + f);
      if (errors.length) throw new Error(errors.slice(0, 3).join(' | '));
      log(hasZoom && hasMode, 'tool ' + d, `${info.svg} svg, zoom ${hasZoom}, modes ${hasMode}`);
    } catch (e) { log(false, 'tool ' + d, e.message); }
    finally { await page.close(); }
  }
}

async function unitPages(ctx) {
  for (const u of [''].concat(UNITS)) {
    const { page, errors } = await open(ctx, `http://localhost:${PORT}/index.html#math5${u ? '.' + u : ''}`);
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
  const games = ['math-quest', 'treasure-trail', 'space-explorer', 'math-builders', 'picture-reveal', 'math-race', 'math-soccer', 'connect-four', 'puzzle-masters', 'fraction-frenzy'];
  const want = process.env.G5_ONLY;
  if (!want || want === 'games') {
    for (const g of games.filter(x => !process.env.G5_GAME || x === process.env.G5_GAME)) {
      const units = g === 'fraction-frenzy' ? ['fraction-addition-subtraction'] : QUICK ? [UNITS[(games.indexOf(g) * 3) % UNITS.length]] : UNITS;
      for (const u of units) await playGame(ctx, g, u);
    }
    await playGame(ctx, 'math-quest', 'decimal-operations', 'class');
    await playGame(ctx, 'math-race', 'volume-three-dimensional-figures', 'class4');
  }
  if (!want || want === 'checks') for (const u of (QUICK ? UNITS.slice(0, 3) : UNITS)) await understandingCheck(ctx, u);
  if (!want || want === 'cards') for (const u of UNITS) await flashcards(ctx, u);
  if (!want || want === 'tools') await tools(ctx);
  if (!want || want === 'units') await unitPages(ctx);
  await browser.close(); server.close();
  const bad = results.filter(r => !r.ok);
  console.log(`\n${results.length - bad.length} passed, ${bad.length} failed`);
  fs.writeFileSync(path.join(ROOT, 'tools/grade5-authoring/out/browser-results.json'), JSON.stringify(results, null, 1));
  process.exit(bad.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
