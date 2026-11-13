// Prints HTML jobs to PDF (Letter) and takes JPG screenshots, with Playwright's Chromium.
// Usage: node tools/math5/print/print.cjs jobs.json   jobs: [{html:"path.html", pdf:"out.pdf"} | {url:"http://…", jpg:"out.jpg", w, h}]
const fs = require('fs'), path = require('path'), pw = require('playwright');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await pw.chromium.launch(); let n = 0;
  for (const j of jobs) {
    const p = await b.newPage(j.jpg || j.png ? { viewport: { width: j.w || 1200, height: j.h || 750 }, deviceScaleFactor: (j.outW || 720) / (j.w || 1200) } : {});
    await p.goto(j.url || 'file://' + path.resolve(j.html)); await p.waitForTimeout(j.wait || 250);
    if (j.pdf) { fs.mkdirSync(path.dirname(j.pdf), { recursive: true }); await p.pdf({ path: j.pdf, format: 'Letter', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } }); }
    if (j.jpg) { fs.mkdirSync(path.dirname(j.jpg), { recursive: true }); await p.screenshot({ path: j.jpg, type: 'jpeg', quality: 85 }); }
    if (j.png) { fs.mkdirSync(path.dirname(j.png), { recursive: true }); await p.screenshot({ path: j.png }); }
    await p.close(); n++;
  }
  await b.close(); console.log('printed', n, 'jobs');
})();
