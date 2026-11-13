#!/usr/bin/env node
'use strict';
// Branch-only Grade 1 teacher preview browser validation. Never approves/publishes.
const fs=require('node:fs');
const {chromium}=require('playwright');
const base=process.env.GRADE1_BASE||'http://127.0.0.1:8765';
const result={passed:0,failed:[],jsErrors:[],brokenAssets:[],diagramRenders:0,skillsTested:0,levelsTested:0};
fs.mkdirSync('grade1-browser-results',{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1280,height:860}});
 page.setDefaultTimeout(6000);
 page.on('pageerror',e=>result.jsErrors.push(e.message));
 page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)result.brokenAssets.push(r.status()+' '+r.url())});
 async function test(label){
  const q=(await page.locator('#prompt').innerText()).trim();
  const meta=(await page.locator('#id').innerText()).trim();
  if(!q||/Choose a different skill|No questions match/.test(q))throw Error('No question shown: '+meta);
  const format=await page.locator('#format').inputValue();
  const level=await page.locator('#level').inputValue();
  if(!meta.includes(' · '+level+' · '+format))throw Error('Wrong question format or level: '+meta);
  const choice=page.locator('#choices .choice');
  const part=page.locator('#parts div');
  if(['multiple-choice','select-all'].includes(format)&&await choice.count()<2)throw Error('Missing choice controls: '+meta);
  if(format==='open-response'&&await part.count()<4)throw Error('Missing multipart content: '+meta);
  const img=page.locator('#diagram');
  if(await img.isVisible()){
   await page.waitForFunction(()=>{
    const x=document.querySelector('#diagram');return x&&!x.hidden&&x.complete&&x.naturalWidth>0;
   },null,{timeout:3500});
   result.diagramRenders++;
  }
  await page.locator('#toggle').click();
  if(!(await page.locator('#answer').innerText()).includes('Answer:'))throw Error('Reveal lacks answer');
  await page.locator('#toggle').click();
  result.passed++;
 }
 try{
  const p=await page.goto(base+'/tools/grade1-authoring/preview.html',{waitUntil:'domcontentloaded',timeout:15000});
  if(!p||p.status()!==200)throw Error('Preview page HTTP '+p?.status());
  await page.locator('#unit option').nth(7).waitFor({state:'attached',timeout:12000});
  const units=await page.locator('#unit option').evaluateAll(nodes=>nodes.map(n=>n.value));
  if(units.length!==8)throw Error('Expected 8 units, got '+units.length);
  for(const [index,unit] of units.entries()){
   await page.selectOption('#unit',unit);
   await page.waitForFunction(()=>document.querySelector('#count')?.textContent.startsWith('Question '),null,{timeout:8000});
   const skills=await page.locator('#skill option').evaluateAll(nodes=>nodes.map(n=>n.value));
   if(!skills.length)throw Error('No skills for '+unit);
   // Every one of the 93 skills: inspect all 4 formats at Standard difficulty.
   await page.selectOption('#level','cp1');
   for(const skill of skills){
    await page.selectOption('#skill',skill);
    for(const format of ['short-answer','multiple-choice','select-all','open-response']){
     await page.selectOption('#format',format);
     try{await test(skill+' / '+format)}
     catch(e){result.failed.push({unit,skill,format,error:e.message});if(result.failed.length>=8)throw Error('Too many viewer failures');}
    }
    result.skillsTested++;
   }
   // All three difficulty levels get an additional multi-format smoke.
   await page.selectOption('#skill',skills[0]);
   for(const level of ['cp2','cp1','honors']){
    await page.selectOption('#level',level);
    for(const format of ['short-answer','multiple-choice','select-all','open-response']){
     await page.selectOption('#format',format);
     try{await test(unit+' / '+level+' / '+format)}
     catch(e){result.failed.push({unit,level,format,error:e.message});if(result.failed.length>=8)throw Error('Too many viewer failures');}
    }
    result.levelsTested++;
   }
   if(index<2)await page.screenshot({path:'grade1-browser-results/unit'+(index+1)+'.png',fullPage:true,timeout:10000});
  }
 }catch(e){result.failed.push({scope:'setup or loop',error:e.message})}
 finally{
  await browser.close();
  result.jsErrors=[...new Set(result.jsErrors)];
  result.brokenAssets=[...new Set(result.brokenAssets)];
  fs.writeFileSync('grade1-browser-results/report.json',JSON.stringify(result,null,2));
  const summary='# Grade 1 review-only Chromium validation\n\n'+
    'Passed '+result.passed+' question samples across '+result.skillsTested+
    ' skills and '+result.levelsTested+' extra difficulty checks; '+
    result.diagramRenders+' sample image loads; '+result.failed.length+' case failures; '+
    result.jsErrors.length+' JS exceptions; '+result.brokenAssets.length+' HTTP failures.\n\n'+
    result.failed.slice(0,20).map(x=>'- '+JSON.stringify(x)).join('\n')+'\n';
  fs.writeFileSync('grade1-browser-results/summary.md',summary);
  if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,summary);
  console.log(summary);
  if(result.failed.length||result.jsErrors.length||result.brokenAssets.length)process.exitCode=1;
 }
})().catch(e=>{console.error(e);process.exitCode=1});
