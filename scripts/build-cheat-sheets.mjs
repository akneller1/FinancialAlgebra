/* Dedicated cheat-sheet build. Does not touch project packets, guides or manifests. */
import { writeFileSync, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { course } from '../src/course.js';
import { loadContent } from './build-banks.mjs';
const require = createRequire(new URL('./financial-cheat-sheets/package.json', import.meta.url));
const { chromium } = require('playwright');
const { cheatSheetHtml } = require('./style.cjs');
const root = new URL('../', import.meta.url);
const esc = s => String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function landing(unit,n) {
 return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(unit.name)} Cheat Sheet</title><style>body{margin:0;font-family:system-ui,sans-serif;background:#f4f5fb}header{padding:12px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}a{color:#5a2fd6;font-weight:700}iframe{width:100%;height:calc(100vh - 80px);border:0}</style></head><body><header><strong>Unit ${n}: ${esc(unit.name)} — Cheat Sheet</strong><a href="cheat-sheet.pdf?v=classroom-design-2">Open PDF</a><a href="cheat-sheet.html">Printable web version</a><span>2 Letter pages · Print double-sided, flip on long edge · 100% scale</span></header><iframe src="cheat-sheet.pdf?v=classroom-design-2" title="${esc(unit.name)} cheat sheet PDF"></iframe></body></html>`;
}
export async function writeCheatSheet(unit,n,cs,pg) {
 if(cs.front?.length!==6 || cs.back?.length!==6) throw Error(`${unit.id}: needs six panels per page`);
 const dir = new URL(`artifacts/financial-algebra-${unit.id}-cheat-sheet/`,root).pathname;
 mkdirSync(dir,{recursive:true});
 const html = cheatSheetHtml({unitNo:n,unitName:unit.name,course:'Financial Algebra',...cs});
 writeFileSync(dir+'cheat-sheet.html',html);
 writeFileSync(dir+'index.html',landing(unit,n));
 if(!pg) {
  execFileSync(process.env.PYTHON || 'python3',[new URL('./financial-cheat-sheets/render-validate.py',import.meta.url).pathname,dir+'cheat-sheet.html',dir+'cheat-sheet.pdf'],{stdio:'inherit'});
  return dir+'cheat-sheet.pdf';
 }
 await pg.goto(pathToFileURL(dir+'cheat-sheet.html').href,{waitUntil:'load'});
 await pg.evaluate(()=>document.fonts.ready);
 const problems = await pg.evaluate(()=>{
  const out=[];
  for(const el of document.querySelectorAll('.pg,.sec,.in,.ban,.sec h2,.ans,.katex-html')) {
   if(el.scrollHeight>el.clientHeight+2 || el.scrollWidth>el.clientWidth+2) out.push(el.className+': '+el.textContent.slice(0,70));
  }
  for(const el of document.querySelectorAll('.sec')) {
   const inner=el.querySelector('.in').getBoundingClientRect(), panel=el.getBoundingClientRect();
   if(inner.bottom>panel.bottom-4) out.push('content crosses panel bottom: '+el.querySelector('h2').textContent);
  }
  if(document.querySelectorAll('.katex-error').length) out.push('KaTeX error');
  return out;
 });
 if(problems.length) throw Error(unit.id+' overflow:\n'+problems.join('\n'));
 await pg.pdf({path:dir+'cheat-sheet.pdf',format:'Letter',printBackground:true,preferCSSPageSize:true,margin:{top:0,bottom:0,left:0,right:0},displayHeaderFooter:false});
 return dir+'cheat-sheet.pdf';
}
export async function buildCheatSheets(ids=course.units.map(u=>u.id)) {
 for(const id of ids) if(!course.units.some(u=>u.id===id)) throw Error('Unknown unit: '+id);
 const browser=process.env.PDF_ENGINE==='weasyprint'?null:await chromium.launch(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{});
 try {
  const pg=browser?await browser.newPage():null;
  for(const id of ids){const u=course.units.find(u=>u.id===id);const c=await loadContent(id);await writeCheatSheet(u,course.units.indexOf(u)+1,c.cheatSheet,pg);console.log('Built '+id);}
 } finally {if(browser) await browser.close();}
}
if(import.meta.url===pathToFileURL(process.argv[1]).href) await buildCheatSheets(process.argv.slice(2).length?process.argv.slice(2):undefined);
