/* Thumbnails for the Spreadsheet Lab cards (2026-11-17): thumbs/financial-algebra/<unit>-spreadsheet.svg. */
import { writeFileSync, readFileSync } from 'node:fs';
import { course } from '../src/course.js';
const root = new URL('../', import.meta.url);
const labs = JSON.parse(readFileSync(new URL('financial/spreadsheet-labs/labs.json', root), 'utf8')).labs;
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const SAMPLE = { budget: [['Rent', '$1,100.00'], ['Groceries', '$380.00'], ['Total', '=SUM(B9:B18)'], ['Net cash flow', '=B6-B19']], amortization: [['Payment', '=ROUND(PMT(B2/12,B3,-B1),2)'], ['Interest', '=ROUND(E8*$B$2/12,2)'], ['Principal', '=B9-C9'], ['Balance', '=E8-D9']], 'pmt-fv': [['Loan payment', '=PMT(B4/12,B5,-B3)'], ['Savings growth', '=FV(B10/12,B11,-B9)'], ['Goal deposit', '=PMT(B16/12,B17,0,-B15)'], ['Check', '=FV(B16/12,B17,-B18)']] };
for (const l of labs) {
  const u = course.units.find(x => x.id === l.unit), n = course.units.indexOf(u) + 1, rows = SAMPLE[l.slug];
  let g = '';
  rows.forEach((r, i) => { const y = 176 + i * 52; g += `<rect x="30" y="${y}" width="40" height="52" fill="#eef0f7" stroke="#b9bfd8"/><text x="50" y="${y + 33}" font-family="Arial,sans-serif" font-size="18" text-anchor="middle" fill="#555">${i + 2}</text><rect x="70" y="${y}" width="230" height="52" fill="white" stroke="#b9bfd8"/><text x="84" y="${y + 33}" font-family="Arial,sans-serif" font-size="20" fill="#222">${esc(r[0])}</text><rect x="300" y="${y}" width="390" height="52" fill="${r[1].startsWith('=') ? '#fff6d6' : 'white'}" stroke="#b9bfd8"/><text x="314" y="${y + 33}" font-family="Consolas,monospace" font-size="20" fill="#1a6b3c">${esc(r[1])}</text>`; });
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="720" height="450" viewBox="0 0 720 450" role="img" aria-label="Spreadsheet Lab preview: ${esc(u.name)}"><rect width="720" height="450" fill="#eaf6ef"/><rect width="720" height="101" fill="#1a7a46"/><text x="30" y="46" font-family="Arial,sans-serif" font-size="32" font-weight="700" fill="white">Spreadsheet Lab</text><text x="31" y="80" font-family="Arial,sans-serif" font-size="18" fill="white">UNIT ${n}  /  ${esc(u.name)}</text><text x="32" y="148" font-family="Arial,sans-serif" font-size="26" font-weight="700" fill="#1a7a46">${esc(l.title.replace(/^Spreadsheet Lab \d: /, ''))}</text><rect x="30" y="160" width="660" height="16" fill="#eef0f7" stroke="#b9bfd8"/>${g}</svg>`;
  writeFileSync(new URL(`thumbs/financial-algebra/${l.unit}-spreadsheet.svg`, root), svg);
}
console.log('spreadsheet thumbnails:', labs.length);
