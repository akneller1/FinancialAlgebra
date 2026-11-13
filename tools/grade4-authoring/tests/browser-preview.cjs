/* Browser crawl of 4th Grade Math in the integrated development preview (production Classroom shell).
   After: CLASSROOM_SOURCE_DIR=../classroom node scripts/assemble-classroom-preview.mjs
   Serve <classroom>/_site (python3 -m http.server 8771) and run:
     G4_BASE=http://127.0.0.1:8771/ node tools/grade4-authoring/tests/browser-preview.cjs [--shots=dir]
   Checks: /#grade4 lists ten units; every unit page renders its cards with loaded thumbnails; every local link on a
   card answers 200; the old grade4.html address redirects; Grade 5 and Financial Algebra still open. */
'use strict';
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
const BASE = process.env.G4_BASE || 'http://127.0.0.1:8771/';
const SHOTS = (process.argv.find(a => a.startsWith('--shots=')) || '').split('=')[1];
const O = require('../outline.json');
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 1360, height: 900 } });
  let pass = 0; const fails = [];
  const ok = (what, cond, note) => { if (cond) { pass++; console.log('PASS ' + what + (note ? ' — ' + note : '')); } else { fails.push(what + ' ' + (note || '')); console.log('FAIL ' + what + (note ? ' — ' + note : '')); } };
  const open = async (url, wait) => {
    const p = await ctx.newPage(), errs = [];
    p.on('pageerror', e => errs.push('pageerror ' + e.message.slice(0, 120)));
    p.on('response', r => { if (r.url().startsWith(BASE) && r.status() >= 400 && !/favicon/.test(r.url())) errs.push(r.status() + ' ' + r.url().slice(BASE.length)); });
    await p.goto(BASE + url, { waitUntil: 'load', timeout: 40000 });
    await p.waitForTimeout(wait || 1200);
    return { p, errs };
  };
  const checked = new Set();
  { // course page
    const { p, errs } = await open('#grade4');
    const text = await p.evaluate(() => document.body.innerText);
    const found = O.units.filter(u => text.includes(u.name)).length;
    ok('course page /#grade4', found === O.units.length && /4th Grade/.test(text) && !errs.length, found + '/10 units' + (errs.length ? '; ' + errs.slice(0, 3).join(' | ') : ''));
    if (SHOTS) { fs.mkdirSync(SHOTS, { recursive: true }); await p.screenshot({ path: path.join(SHOTS, 'course.png'), fullPage: false }); }
    await p.close();
  }
  for (const [i, u] of O.units.entries()) {
    const { p, errs } = await open('#grade4.' + u.id, 1500);
    const info = await p.evaluate(() => {
      const cards = [...document.querySelectorAll('.card, li.card, [class*="resource-card"]')];
      const imgs = [...document.querySelectorAll('main img')];
      return { cards: cards.length, broken: imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')),
        links: [...document.querySelectorAll('main a[href]')].map(a => a.href).filter(h => h.startsWith(location.origin)), text: document.body.innerText };
    });
    const local = [...new Set(info.links.map(h => h.split('#')[0]))].filter(h => !checked.has(h));
    const bad = [];
    for (const h of local) {
      checked.add(h);
      const r = await ctx.request.get(h).catch(() => null);
      if (!r || r.status() >= 400) bad.push((r ? r.status() : 'ERR') + ' ' + h.slice(BASE.length));
    }
    const want = ['Lesson Plan', 'Worksheet', 'Activity', 'Assessment', 'Flashcards', 'Understanding Check', 'Cheat Sheet', 'Projects', 'Interactive Math'];
    const missing = want.filter(t => !info.text.includes(t) && !(t === 'Interactive Math' && u.id === 'data-line-plots-word-problems'));   // Unit 10 has no tool
    ok('unit ' + (i + 1) + ' ' + u.id, info.cards >= 12 && !info.broken.length && !bad.length && !missing.length && !errs.length,
      info.cards + ' cards, ' + local.length + ' new links checked' + (missing.length ? '; missing ' + missing.join(', ') : '') + (info.broken.length ? '; broken images ' + info.broken.slice(0, 3).join(', ') : '') + (bad.length ? '; ' + bad.slice(0, 3).join(', ') : '') + (errs.length ? '; ' + errs.slice(0, 3).join(' | ') : ''));
    if (SHOTS && i === 6) await p.screenshot({ path: path.join(SHOTS, 'unit7.png'), fullPage: true });
    await p.close();
  }
  { // old address and neighbors
    const { p } = await open('grade4.html', 1500);
    ok('grade4.html redirects into the shell', /#grade4/.test(p.url()), p.url().slice(BASE.length)); await p.close();
    for (const [what, url, re] of [['Grade 5 course still opens', '#grade5', /5th Grade/], ['Financial Algebra still opens', 'financial-algebra/', /Financial Algebra/]]) {
      const r = await open(url, 1500); const t = await r.p.evaluate(() => document.body.innerText);
      ok(what, re.test(t) && !r.errs.filter(e => /pageerror/.test(e)).length, r.errs.slice(0, 2).join(' | ')); await r.p.close();
    }
  }
  await b.close();
  console.log('\n' + pass + ' passed, ' + fails.length + ' failed');
  process.exit(fails.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
