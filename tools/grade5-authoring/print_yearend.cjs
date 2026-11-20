// Grade 5 audit (2026-11-19) #9, #15, #16: prints the practice tests, reference sheet, pacing guide and lab worksheets to
// PDF and makes the card thumbnails from the first page (labs: from the interactive page). Usage (repository root):
//   python3 tools/grade5-authoring/yearend.py && node tools/grade5-authoring/print_yearend.cjs
'use strict';
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path'), os = require('os');
const ROOT = path.resolve(__dirname, '../..');
const JOBS = [
  ['math5-practice-test-a', [['exam.html', 'exam.pdf'], ['key.html', 'teacher-key.pdf']], 'exam.html'],
  ['math5-practice-test-b', [['exam.html', 'exam.pdf'], ['key.html', 'teacher-key.pdf']], 'exam.html'],
  ['math5-reference-sheet', [['index.html', 'reference-sheet.pdf']], 'index.html'],
  ['math5-pacing-guide', [['index.html', 'pacing-guide.pdf']], 'index.html'],
  ['math5-decimal-grid-lab', [['worksheet.html', 'worksheet.pdf'], ['teacher-key.html', 'teacher-key.pdf']], 'index.html'],
  ['math5-scaling-lab', [['worksheet.html', 'worksheet.pdf'], ['teacher-key.html', 'teacher-key.pdf']], 'index.html']];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [slug, files, thumbFrom] of JOBS) {
    const dir = path.join(ROOT, slug);
    for (const [src, out] of files) {
      await p.goto('file://' + path.join(dir, src)); await p.waitForTimeout(300);
      const buf = await p.pdf({ path: path.join(dir, out), format: 'Letter', printBackground: true, preferCSSPageSize: true });
      console.log(slug, out, (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length, 'pages');
    }
    await p.setViewportSize({ width: 1000, height: 625 }); await p.goto('file://' + path.join(dir, thumbFrom)); await p.waitForTimeout(500);
    const tmp = path.join(os.tmpdir(), 'thumb-' + slug + '.png'); await p.screenshot({ path: tmp, clip: { x: 0, y: 0, width: 1000, height: 625 } });
    execFileSync('python3', ['-c', `from PIL import Image\nIm=Image.open('${tmp}').convert('RGB').resize((720,450),Image.LANCZOS)\nIm.save('${path.join(ROOT, 'thumbs', slug + '.jpg')}',quality=86)`]);
  }
  await b.close();
})();
