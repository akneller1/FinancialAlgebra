/* Cheat sheet style shared by every cheat sheet on the site (Andrey 2026-10-25: all cheat sheets in the newest
   unit-pack style). Used by scripts/unit-packs/build.cjs and scripts/cheat-sheets/build.cjs.
   cheatSheetHtml({unitNo, unitName, focus, morefocus, front: [6 sections], back: [6 sections], course})
   Section kinds: vocab, table, example, list, mistakes, words, props, pemdas, sets, html, figure. */
'use strict';
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const katex = require(path.join(ROOT, 'worksheet-generator/vendor/katex/katex.min.js'));
function tex(s) { return katex.renderToString(s, { throwOnError: true }); }
function mt(s) { return String(s).split(/(⟨[^⟩]*⟩)/).map(p => /^⟨/.test(p) ? tex(p.slice(1, -1)) : p).join(''); }
const KCSS = 'file://' + path.join(ROOT, 'worksheet-generator/vendor/katex/katex.min.css');
const FONT = '"DejaVu Sans",Verdana,Geneva,sans-serif';
function doc(css, body) {
  return '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="' + KCSS + '"><style>@page{size:letter;margin:0}*{box-sizing:border-box}body{margin:0;font-family:' + FONT + ';color:#111}' +
    '.pg{width:8.5in;height:11in;padding:.5in .55in;position:relative;page-break-after:always;overflow:hidden}.pg:last-child{page-break-after:auto}.katex{font-size:1.05em}' + css + '</style></head><body>' + body + '</body></html>';
}
/* ---- cheat sheet ---- */
const COL = { purple: ['#7b4fd0', '#f0e9ff'], blue: ['#2563eb', '#e6efff'], green: ['#16a34a', '#e6f8ec'], orange: ['#ea7a12', '#fff1e0'], pink: ['#db2777', '#fde8f1'], teal: ['#0d9488', '#e0f6f3'] };
const CCSS = '.pg{padding:.32in .35in}.ban{background:#ffd23f;border:3px solid #1f2a6b;border-radius:16px;text-align:center;padding:.06in;box-shadow:3px 3px 0 #1f2a6b}.ban b{font-family:"DejaVu Sans",sans-serif;font-size:21pt;white-space:nowrap;color:#1f2a6b;letter-spacing:-.01em}.ban b span{color:#2563eb}' +
  '.foc{text-align:center;font-size:10pt;margin:.08in 0 .1in;color:#1f2a6b}.foc b{color:#2563eb}.pg{display:flex;flex-direction:column}.grid{flex:1;display:grid;grid-template-columns:1fr 1fr;align-content:stretch;gap:.12in}.sec{border:2.4px solid var(--c);border-radius:12px;background:var(--t);padding:0 0 .08in;overflow:hidden;font-size:9pt;line-height:1.42}' +
  '.sec h2{margin:0 0 .06in;background:var(--c);color:#fff;font-size:11.5pt;padding:.04in .1in;letter-spacing:.02em;text-transform:uppercase}.sec h2 i{display:inline-block;background:#fff;color:var(--c);border-radius:50%;width:.26in;height:.26in;text-align:center;font-style:normal;margin-right:6px;line-height:.26in}' +
  '.in{padding:0 .1in}.vt{width:100%;border-collapse:collapse;background:#fff}.vt td{border:1px solid #ddd;padding:3px 5px;vertical-align:top}.vt td:first-child{font-weight:700;color:var(--c);width:22%}' +
  '.ex{background:#fff;border:1.5px dashed var(--c);border-radius:8px;padding:.05in .08in;margin-top:.05in}.ex b.l{color:var(--c)}.ans{display:inline-block;border:2px solid var(--c);border-radius:8px;padding:1px 8px;font-weight:700;background:#fff;margin-top:3px}' +
  '.pem{display:grid;grid-template-columns:auto 1fr;gap:2px 8px;align-items:center}.pem b{display:inline-block;width:.24in;text-align:center;background:var(--c);color:#fff;border-radius:4px}' +
  '.sets{position:relative;height:1.55in;margin:.02in .1in}.sets div{position:absolute;border:2px solid var(--c);border-radius:12px;padding:2px 6px;background:rgba(255,255,255,.55);font-weight:700;font-size:8pt}' +
  '.ok{color:#15803d;font-weight:700}.no{color:#dc2626;font-weight:700}ul{margin:.02in 0;padding-left:.18in}li{margin:1px 0}.ft{text-align:center;font-size:8pt;margin-top:.08in;color:#555}.vt.pl td:first-child{font-weight:400;color:#111;width:auto}.fig{text-align:center;margin:.02in 0 .04in}.fig svg{max-width:100%;height:auto}';
function secHtml(s, n) {
  const c = COL[s.color]; let b = '';
  if (s.kind === 'vocab') b = '<table class="vt">' + s.rows.map(r => '<tr><td>' + r[0] + '</td><td>' + mt(r[1]) + '</td><td>' + mt(r[2]) + '</td></tr>').join('') + '</table>';
  else if (s.kind === 'pemdas') b = '<div class="pem">' + [['P', 'Parentheses', 'grouping first'], ['E', 'Exponents', 'powers'], ['M', 'Multiply', 'left to right,'], ['D', 'Divide', 'together'], ['A', 'Add', 'left to right,'], ['S', 'Subtract', 'together']].map(r => '<b>' + r[0] + '</b><span><b style="background:none;color:#111;width:auto">' + r[1] + '</b> — ' + r[2] + '</span>').join('') + '</div>' + exHtml(s);
  else if (s.kind === 'example') b = '<div>' + mt(s.text) + '</div>' + exHtml(s);
  else if (s.kind === 'sets') b = '<div class="sets"><div style="left:0;top:0;right:0;bottom:0">Real numbers</div><div style="left:.08in;top:.22in;width:62%;bottom:.08in">Rational ⟨\\tfrac{a}{b}⟩'.replace(/⟨([^⟩]*)⟩/g, (m, t) => tex(t)) + '</div><div style="left:.18in;top:.48in;width:44%;bottom:.14in">Integers …, −2, −1</div><div style="left:.28in;top:.74in;width:30%;bottom:.2in">Whole 0, 1, 2</div><div style="left:.38in;top:1.0in;width:17%;bottom:.26in;font-size:7pt">Natural 1, 2, 3</div><div style="right:.08in;top:.22in;width:30%;bottom:.08in">Irrational ' + tex('\\sqrt{2},\\ \\pi') + '</div></div><div class="in">Every rational number is a fraction ' + tex('\\tfrac{a}{b}') + ' (or a decimal that ends or repeats). Irrational decimals never end or repeat.</div>';
  else if (s.kind === 'props') b = '<table class="vt">' + s.rows.map(r => '<tr><td>' + r[0] + '<div style="font-weight:400;color:#555;font-size:7.5pt">' + r[1] + '</div></td><td>' + mt(r[2]) + '</td><td>' + mt(r[3]) + '</td></tr>').join('') + '</table>';
  else if (s.kind === 'mistakes') b = '<div class="ok">✔ Do remember</div><ul>' + s.good.map(x => '<li>' + mt(x) + '</li>').join('') + '</ul><div class="no">✘ Common mistakes</div><ul>' + s.bad.map(x => '<li>' + mt(x[0]) + ': ' + mt(x[1]) + '</li>').join('') + '</ul>';
  else if (s.kind === 'words') b = '<table class="vt">' + s.rows.map(r => '<tr><td style="width:65%;font-weight:400;color:#111">' + mt(r[0]) + '</td><td style="font-weight:700">' + mt(r[1]) + '</td></tr>').join('') + '</table>';
  else if (s.kind === 'table') b = '<table class="vt' + (s.plain ? ' pl' : '') + '">' + (s.head ? '<tr>' + s.head.map(h => '<td style="font-weight:700;color:var(--c);background:var(--t)">' + mt(h) + '</td>').join('') + '</tr>' : '') + s.rows.map(r => '<tr>' + r.map(x => '<td>' + mt(x) + '</td>').join('') + '</tr>').join('') + '</table>' + (s.after ? '<div style="margin-top:4px">' + mt(s.after) + '</div>' : '');
  else if (s.kind === 'html') b = mt(s.html);
  else if (s.kind === 'figure') b = '<div class="fig">' + s.svg + '</div>' + (s.text ? '<div>' + mt(s.text) + '</div>' : '') + (s.example ? exHtml(s) : '');
  else if (s.kind === 'list') b = '<ul>' + s.items.map(x => '<li>' + mt(x) + '</li>').join('') + '</ul>';
  if (s.fig) b = s.figFirst ? '<div class="fig">' + s.fig + '</div>' + b : b + '<div class="fig">' + s.fig + '</div>';
  return '<div class="sec" style="--c:' + c[0] + ';--t:' + c[1] + '"><h2><i>' + n + '</i>' + s.title + '</h2><div class="in">' + b + '</div></div>';
}
function exHtml(s) { return '<div class="ex"><b class="l">Example:</b> ' + mt(s.example) + '<br>' + s.steps.map(st => '<b class="l">' + mt(st[0]) + '</b> ' + mt(st[1])).join('<br>') + '<br><span class="ans">Answer: ' + mt(s.answer) + '</span></div>'; }
/* Elementary treatment (5th Grade, theme: 'elementary'): same layout and section kinds, friendlier type,
   rounded cards, softer colors and a rainbow banner. Other courses are unchanged. */
const ECSS = '.pg{background:#fffdf6}.ban{background:linear-gradient(90deg,#ffe27a,#ffc6a8 50%,#b8e6ff);border:3px solid #22408a;border-radius:24px;box-shadow:0 4px 0 #22408a}' +
  '.ban b{font-family:Inter,"DejaVu Sans",sans-serif;font-weight:900;color:#22408a}.ban b span{color:#d63c7a}.foc{font-size:10.5pt;color:#22408a}.foc b{color:#d63c7a}' +
  '.sec{border-width:3px;border-radius:18px;background:#fff;box-shadow:0 3px 0 var(--c);font-size:10pt;line-height:1.4}.sec .katex{font-size:1.08em}.fig svg{max-height:1.9in}' +
  '.sec h2{font-family:Inter,"DejaVu Sans",sans-serif;text-transform:none;letter-spacing:0;font-size:12.5pt;border-radius:14px 14px 0 0;padding:.05in .12in}' +
  '.sec h2 i{background:#fff;color:var(--c)}.vt{font-size:9.1pt;line-height:1.3}.vt td{border-color:#e6e9f2}.vt td:first-child{width:27%}.ex{background:var(--t);border-style:solid}.ans{background:#fffbe6}' +
  '.ok{color:#15803d}.no{color:#c2410c}.ft{color:#22408a}';
function cheatSheetHtml(C) {
  const ch = C.cheat || C, title = '<b style="font-size:' + Math.min(21, 21 * 40 / ('Unit ' + C.unitNo + ' · ' + C.unitName + ' Cheat Sheet').length).toFixed(1) + 'pt">Unit ' + C.unitNo + ' · <span>' + C.unitName + '</span> Cheat Sheet</b>';
  return doc(CCSS + (C.theme === 'elementary' ? ECSS : ''), '<div class="pg"><div class="ban">' + title + '</div><div class="foc"><b>Unit ' + C.unitNo + ' focus:</b> ' + ch.focus + '</div><div class="grid">' + ch.front.map((s, i) => secHtml(s, i + 1)).join('') + '</div><div class="ft">Front · ' + (C.course ? C.course + ' · ' : '') + 'Mr. K’s Classroom</div></div>' +
    '<div class="pg"><div class="ban">' + title + '</div><div class="foc"><b>More practice:</b> ' + ch.morefocus + '</div><div class="grid">' + ch.back.map((s, i) => secHtml(s, i + 1)).join('') + '</div><div class="ft">Back · ' + (C.course ? C.course + ' · ' : '') + 'Mr. K’s Classroom</div></div>');
}


module.exports = { tex, mt, doc, COL, CCSS, secHtml, exHtml, cheatSheetHtml, ROOT };
