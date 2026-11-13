// Opens every generated project HTML page (student packets, teacher guides, supports) and reports any page whose content
// runs past the bottom of the Letter page (the print CSS hides overflow, so clipping would otherwise be silent).
// Usage: node tools/grade3-authoring/tests/print-overflow.cjs <scratch-dir-with-html>
const fs = require('fs'), path = require('path'), pw = require('playwright');
(async () => {
  const dir = process.argv[2], files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && !f.endsWith('-hero.html'));
  const b = await pw.chromium.launch(), p = await b.newPage({ viewport: { width: 816, height: 1056 } }); let bad = 0, pages = 0;
  for (const f of files) {
    await p.goto('file://' + path.resolve(dir, f)); await p.waitForTimeout(50);
    const r = await p.evaluate(() => Array.from(document.querySelectorAll('.pg')).map((g, i) => ({ i, over: g.scrollHeight - g.clientHeight })));
    pages += r.length;
    r.filter(x => x.over > 2).forEach(x => { bad++; console.log('OVERFLOW', f, 'page', x.i + 1, x.over + 'px'); });
  }
  await b.close(); console.log(`print overflow check: ${files.length} documents, ${pages} pages, ${bad} overflowing`); process.exit(bad ? 1 : 0);
})();
