#!/usr/bin/env node
'use strict';
/* Smoke-test the quarantined Grade 1 question/diagram viewer in Chromium.
 * This is NOT a test of production Grade 5-style game engines. */
const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const base=process.env.GRADE1_BASE||'http://127.0.0.1:8765';
const output='grade1-browser-results';
fs.mkdirSync(output,{recursive:true});
const report={passed:0,failed:[],errors:[],missing:[],diagramsOpened:0};
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1365,height:900}});
 page.on('pageerror',e=>report.errors.push(e.message));
 page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)report.missing.push(r.url()+' '+r.status());});
 try{
  const response=await page.goto(base+'/tools/grade1-authoring/preview.html',{waitUntil:'domcontentloaded'});
  if(response?.status()!==200)throw Error('Viewer returned '+response?.status());
  await page.locator('#unit option').nth(7).waitFor({state:'attached',timeout:15000});
  const units=await page.locator('#unit option').evaluateAll(nodes=>nodes.map(n=>n.value));
  if(units.length!==8)throw Error('Expected eight units, found '+units.length);
  for(let i=0;i<units.length;i++){
   await page.selectOption('#unit',units[i]);
   await page.waitForFunction(unit=>document.querySelector('#id')?.textContent.startsWith('m1-'),units[i],{timeout:12000});
   for(const level of ['cp2','cp1','honors']){
    await page.selectOption('#level',level);
    for(const fmt of ['short-answer','multiple-choice','select-all','open-response']){
     await page.selectOption('#format',fmt);
     try{
      await page.waitForFunction(()=>document.querySelector('#count')?.textContent.startsWith('Question '),null,{timeout:8000});
      const text=(await page.locator('#prompt').innerText()).trim();
      if(!text||text.includes('Choose a different skill'))throw Error('Missing question prompt');
      const id=(await page.locator('#id').innerText()).trim();
      if(!id.includes(' · '+level+' · '+fmt))throw Error('Wrong selection '+id);
      if(fmt==='multiple-choice'||fmt==='select-all'){
       const n=await page.locator('#choices .choice').count();
       if(n<2)throw Error('No answer options');
      }
      if(fmt==='open-response'&&await page.locator('#parts div').count()<4)throw Error('Missing multi-part response');
      const img=page.locator('#diagram');
      if(await img.isVisible()){
       await page.waitForFunction(()=>{const im=document.querySelector('#diagram');return !im.hidden&&im.complete&&im.naturalWidth>0;},null,{timeout:7000});
       report.diagramsOpened++;
      }
      await page.locator('#toggle').click();
      if(!await page.locator('#answer').isVisible())throw Error('Answer/reasoning missing');
      if(!(await page.locator('#answer').innerText()).includes('Answer:'))throw Error('Empty answer');
      await page.locator('#toggle').click();
      report.passed++;
     }catch(e){report.failed.push({unit:units[i],level,format:fmt,error:e.message});}
    }
   }
   if(i<4)await page.screenshot({path:output+'/unit-'+(i+1)+'.png',fullPage:true});
  }
 }catch(e){report.failed.push({unit:'init',error:e.message});}
 finally{
  await browser.close();
  report.errors=[...new Set(report.errors)];
  report.missing=[...new Set(report.missing)];
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2));
  const summary='# Grade 1 development-only browser viewer smoke\n\n'+
   'Passed '+report.passed+' format × level × unit renders; failures '+report.failed.length+
   '; diagrams opened '+report.diagramsOpened+'; JavaScript errors '+report.errors.length+
   '; missing network assets '+report.missing.length+'.\n\n'+
   report.failed.slice(0,20).map(x=>'- '+JSON.stringify(x)).join('\n');
  fs.writeFileSync(path.join(output,'summary.md'),summary);
  if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,summary);
  console.log(JSON.stringify(report,null,2));
  if(report.failed.length||report.errors.length||report.missing.length)process.exitCode=1;
 }
})().catch(e=>{console.error(e);process.exitCode=1});
