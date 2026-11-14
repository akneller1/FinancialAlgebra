// The four shared Classroom generators (the same pages Algebra 1 uses) and the printable Understanding Check,
// opened for 1st Grade Math units the way the unit pages link to them (#unit=math1-<unit>).
//   python3 -m http.server 8766 &          (repository root)
//   G1_BASE=http://127.0.0.1:8766/ node tools/grade1-authoring/tests/browser-generators.cjs [--all] [--shots=dir]
// For each page it checks: a Grade 1 unit is the one selected, a preview is built, the preview holds real question
// text, an answer key exists, the levels read Remedial / Standard / Advanced, and the print layout exports to a PDF.
// Default: three units; --all: every unit. Fails on a page error or console error.
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
const BASE = process.env.G1_BASE || 'http://127.0.0.1:8766/';
const SET = process.env.G1_SET || 'grade1';   // the development preview adapts the math1 banks to the native id grade1 (the unit cards link #unit=grade1-<unit>)
const ALL = process.argv.includes('--all');
const SHOTS = (process.argv.find(a => a.startsWith('--shots=')) || '').split('=')[1];
const O = require('../outline.json');
const UNITS = ALL ? O.units : [O.units[2], O.units[6], O.units[8]];
const PAGES = [
  ['lesson planner', 'lesson-planner.html', '#plView', '#plNew'],
  ['worksheet', 'worksheet.html', '#mmView', '#mmBuildBtn'],
  ['assessment', 'menu-assessment.html', '#mmView', '#mmBuildBtn'],
  ['activity: maze', 'printables.html', '#prPreview', null, '&kind=maze'],
  ['activity: tarsia', 'printables.html', '#prPreview', null, '&kind=tarsia'],
  ['activity: stations', 'printables.html', '#prPreview', null, '&kind=stations'],
  ...(SET === 'math1' ? [['understanding check (printable)', 'practice-test.html', 'main, body', null]] : [])
];
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 1360, height: 900 } });
  let pass = 0; const fails = [];
  for (const u of UNITS) for (const [label, file, view, button, extra] of PAGES) {
    const what = label + ' / ' + u.id, errs = [];
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push('PAGEERROR ' + String(e.message).slice(0, 140)));
    p.on('console', m => { if (m.type() === 'error' && !/fonts\.g|ERR_TUNNEL|ERR_NAME|analytics|net::ERR_FAILED|Failed to load resource/.test(m.text())) errs.push('CONSOLE ' + m.text().slice(0, 140)); });
    p.on('response', r => { if (r.url().startsWith(BASE) && r.status() >= 400 && !/analytics\.js/.test(r.url())) errs.push(r.status() + ' ' + r.url().slice(BASE.length)); });
    p.on('dialog', d => d.dismiss().catch(() => {}));
    try {
      await p.goto(BASE + 'worksheet-generator/' + file + '#unit=' + SET + '-' + u.id + (extra || ''), { waitUntil: 'load', timeout: 40000 });
      await p.waitForSelector(view.split(',')[0], { state: 'attached', timeout: 30000 });
      let frameText = '';
      if (button && button.startsWith('FRAME:')) {
        await p.waitForTimeout(1500);
        const fr = p.frames().find(f => /vocabulary\.html/.test(f.url()));
        if (!fr) throw new Error('vocabulary frame not found');
        await fr.locator(button.slice(6)).click({ timeout: 20000 });
        await fr.waitForTimeout(800);
        frameText = await fr.evaluate(() => document.body.innerText);
        if (frameText.length < 400) throw new Error('vocabulary activity not built (' + frameText.length + ' chars)');
      } else if (button) { await p.locator(button).first().waitFor({ state: 'visible', timeout: 20000 }); await p.locator(button).first().click(); }
      await p.waitForFunction(v => { const e = document.querySelector(v.split(',')[0]) || document.body; return e && !e.querySelector('.pr-busy') && !/Making and checking problems|Loading/i.test((e.textContent || '').slice(0, 200)) && (e.innerText || '').trim().length > 150; }, view, { timeout: 60000 });
      await p.waitForTimeout(700);
      const info = await p.evaluate(([v, names, SET_]) => {
        const e = document.querySelector(v.split(',')[0]) || document.body, body = document.body.innerText;
        const sel = [...document.querySelectorAll('select')].map(s => s.value).filter(x => String(x).startsWith(SET_ + '-'));
        const hashSel = location.hash.includes('unit=' + SET_ + '-');
        const levels = ['Remedial', 'Standard', 'Advanced'].filter(l => body.includes(l) || [...document.querySelectorAll('option,button,label')].some(o => (o.textContent || '').trim() === l));
        const old = ['CP2', 'CP1', 'Honors'].filter(l => [...document.querySelectorAll('option,label')].some(o => (o.textContent || '').trim() === l));
        const txt = (e.innerText || '') + ' ' + body;
        return { g4: names.some(n => txt.includes(n)) || /M4-U\d/.test(txt), len: (e.innerText || '').trim().length, sel: sel[0] || '', hashSel, levels, old, key: /answer key|teacher key|answers|solution/i.test(body), fr: e.querySelectorAll('.fr').length,
          img: [...e.querySelectorAll('img')].filter(i => i.complete && i.naturalWidth === 0).length, pages: e.querySelectorAll('.page, .mm-page, .pr-page, .pl-page, .sheet').length, title: document.title, h: (document.querySelector('h1') || {}).textContent || '' };
      }, [view, [u.name].concat(u.skills.map(k => k[0])), SET]);
      await p.emulateMedia({ media: 'print' });
      const pdf = await p.pdf({ format: 'Letter', printBackground: true });
      const nPages = (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
      await p.emulateMedia({ media: 'screen' });
      if (SHOTS && u === UNITS[0]) { fs.mkdirSync(SHOTS, { recursive: true }); await p.screenshot({ path: path.join(SHOTS, label.replace(/[^a-z]+/g, '-') + '.png') }); fs.writeFileSync(path.join(SHOTS, label.replace(/[^a-z]+/g, '-') + '.pdf'), pdf); }
      const problems = [];
      if (frameText) { info.g4 = info.g4 || /1st Grade Math/.test(frameText); info.key = info.key || /key|answer/i.test(frameText); info.len += frameText.length; }
      if (!info.g4) problems.push('no Grade 1 content from this unit in the preview');
      if (info.len < 150) problems.push('preview too short (' + info.len + ')');
      if (!info.key) problems.push('no answer key wording on the page');
      if (info.img) problems.push(info.img + ' broken image(s)');
      if (info.old.length && info.levels.length < 3) problems.push('levels read ' + info.old.join('/') + ' instead of Remedial/Standard/Advanced');
      if (nPages < 1 || pdf.length < 8000) problems.push('PDF export looks empty (' + nPages + ' pages, ' + pdf.length + ' bytes)');
      if (errs.length) problems.push([...new Set(errs)].slice(0, 3).join(' | '));
      if (problems.length) { fails.push(what + ' :: ' + problems.join('; ')); console.log('FAIL ' + what + ' — ' + problems.join('; ')); }
      else { pass++; console.log('PASS ' + what + ' — unit ' + (info.sel || 'from link') + ', preview ' + info.len + ' chars, ' + info.fr + ' stacked fractions, levels ' + info.levels.join('/') + ', PDF ' + nPages + ' pages'); }
    } catch (e) { fails.push(what + ' :: ' + String(e.message).slice(0, 200)); console.log('FAIL ' + what + ' — ' + String(e.message).slice(0, 200) + (errs.length ? ' | ' + errs.slice(0, 2).join(' | ') : '')); }
    await p.close();
  }
  await b.close();
  console.log('\n' + pass + ' passed, ' + fails.length + ' failed');
  process.exit(fails.length ? 1 : 0);
})();
