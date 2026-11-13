/* Browser test for the Grade 4 Interactive Math tools. Drives real controls and checks readouts, challenges,
   zoom, Fit and Present (picture AND controls must stay inside the window). BASE=http://127.0.0.1:8765/ */
const { chromium } = require('playwright');
const base = process.env.BASE || 'http://127.0.0.1:8765/';
const set = (p, id, v) => p.$eval('#' + id, (e, v) => { e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, v);
const clickN = async (p, sel, n) => { for (let i = 0; i < n; i++) await p.click(sel); };
const stp = (k, s) => `[data-k="${k}"][data-s="${s}"]`;
const T = {
  'place-value-blocks': async p => { await clickN(p, stp(0, 1), 6); await p.click('#pvRe'); return [/1,352/.test(await p.textContent('#pvNum')), 'regroup 12 ones -> 1,352']; },
  'array-area-models': async p => { await set(p, 'amR', 6); await set(p, 'amC', 14); await set(p, 'amS', 10); return [/60 \+ 24 = 84/.test(await p.textContent('#amOut')), '6x14 split 60+24=84']; },
  'division-groups': async p => { await set(p, 'dvN', 23); await set(p, 'dvD', 4); return [/23 ÷ 4 = 5 R 3/.test(await p.textContent('#dvOut')), '23÷4=5R3']; },
  'equivalent-fractions': async p => { await clickN(p, stp('k', 1), 2); return [(await p.getAttribute('#efModel svg', 'aria-label')).includes('8 of 12'), '2/3 = 8/12']; },
  'fraction-number-line': async p => { await p.selectOption('#nlD', '5'); await p.click(stp('a', -1)); await p.click(stp('j', 1)); return [(await p.getAttribute('#nlModel svg', 'aria-label')).includes('3 jumps of 2 over 5'), '3 x 2/5']; },
  'decimal-grids': async p => { await clickN(p, stp('at', 1), 2); await clickN(p, stp('a', -1), 5); await clickN(p, stp('bt', -1), 2); await clickN(p, stp('b', -1), 5); return [/0\.40 > 0\.35/.test(await p.textContent('#dgOut')), '0.40 > 0.35']; },
  'angle-explorer': async p => { await set(p, 'agA', 90); const a = /right/.test(await p.textContent('#agOut')); await set(p, 'agA', 35); await set(p, 'agB', 55); return [a && /35° \+ 55° = 90°/.test(await p.textContent('#agOut')), 'right angle; 35+55=90']; },
  'area-perimeter': async p => { await set(p, 'apW', 6); await set(p, 'apH', 4); await p.click('#apPin'); await set(p, 'apW', 8); await set(p, 'apH', 3); return [/Same area, different perimeter/.test(await p.textContent('#apOut')), '6x4 vs 8x3 same area']; },
  'symmetry-shapes': async p => { await p.selectOption('#syS', 'square'); let n = 0; for (const d of [0, 45, 90, 135, 30]) { await set(p, 'syA', d); if (/Yes!/.test(await p.textContent('#syOut'))) n++; } await p.selectOption('#syS', 'parallelogram'); let m = 0; for (let d = 0; d < 180; d += 5) { await set(p, 'syA', d); if (/Yes!/.test(await p.textContent('#syOut'))) m++; } return [n === 4 && m === 0, 'square 4 lines, parallelogram 0']; }
};
(async () => {
  const b = await chromium.launch(); let fail = 0;
  for (const [slug, fn] of Object.entries(T)) {
    for (const [vw, vh] of [[1280, 800], [1920, 1080], [1024, 600], [390, 780]]) {
      const p = await b.newPage({ viewport: { width: vw, height: vh } }); const errs = [];
      p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error' && !/fonts\.g/.test(m.text())) errs.push(m.text()); });
      await p.goto(base + 'artifacts/math4-' + slug + '/index.html'); await p.waitForTimeout(150);
      const pre = await p.$$eval('#challenges li.done', l => l.length);
      const [ok, what] = await fn(p);
      const done = await p.$$eval('#challenges li.done', l => l.length);
      // zoom in: picture and controls scale together
      const m0 = await p.evaluate(() => { const r = s => document.querySelector(s).getBoundingClientRect(), f = s => parseFloat(getComputedStyle(document.querySelector(s)).fontSize); return [f('.tl-out'), f('.tl-controls button, .tl-controls label'), r('.tl-model').width, r('.tl-controls').width, document.documentElement.scrollWidth - innerWidth]; });
      await p.click('#tsIn'); await p.click('#tsIn');
      const m1 = await p.evaluate(() => { const r = s => document.querySelector(s).getBoundingClientRect(), f = s => parseFloat(getComputedStyle(document.querySelector(s)).fontSize); return [f('.tl-out'), f('.tl-controls button, .tl-controls label'), r('.tl-model').width, r('.tl-controls').width, document.documentElement.scrollWidth - innerWidth]; });
      const narrow = vw < 700, both = m1[0] > m0[0] * 1.1 && m1[1] > m0[1] * 1.1 && m1[2] > 40 && m1[3] > 40 && m1[4] <= 2;
      // Present + Fit: whole workspace (picture, controls, readout) inside the window
      await p.click('#tsPresent'); await p.waitForTimeout(400);
      const fit = await p.evaluate(() => { const ws = document.getElementById('workspace').getBoundingClientRect(), c = document.querySelector('.tl-controls').getBoundingClientRect(), m = document.querySelector('.tl-model').getBoundingClientRect(), o = document.querySelector('.tl-out').getBoundingClientRect();
        const inside = r => r.top >= -1 && r.bottom <= innerHeight + 1 && r.left >= -1 && r.right <= innerWidth + 1 && r.width > 40 && r.height > 10;
        return { ws: inside(ws), c: inside(c), m: inside(m), o: inside(o), hscroll: document.documentElement.scrollWidth > innerWidth + 2, z: document.getElementById('tsZoom').textContent }; });
      const fitOk = (fit.ws && fit.c && fit.m && fit.o && !fit.hscroll);
      await p.click('#tsPresent'); await p.click('#tsReset'); await p.waitForTimeout(100);
      const after = await p.$$eval('#challenges li.done', l => l.length);
      const student = await b.newPage(); await student.goto(base + 'artifacts/math4-' + slug + '/index.html?student=1'); const noT = !(await student.$('#tsMode')) && !(await student.$('#tsHome')); await student.close();
      const good = ok && !errs.length && pre === 0 && done >= 1 && both && fitOk && after <= 1 && noT;
      if (!good) fail++;
      console.log((good ? 'PASS ' : 'FAIL ') + slug.padEnd(22) + `${vw}x${vh} ${what}; challenges ${pre}->${done}->reset ${after}; zoomBoth=${both} presentFit=${fitOk} (${fit.z}) studentView=${noT}` + (errs.length ? ' ERR ' + errs[0] : '') + (fitOk ? '' : ' ' + JSON.stringify(fit)));
      await p.close();
    }
  }
  await b.close(); console.log(fail ? fail + ' FAILED' : 'ALL TOOL CHECKS PASSED'); process.exit(fail ? 1 : 0);
})();
