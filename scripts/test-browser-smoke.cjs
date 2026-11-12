#!/usr/bin/env node
/* Real Chromium smoke coverage for Mr. K's Classroom.
 * Reports launch/DOM failures, not mathematical correctness or print fidelity.
 * Starts against a locally generated _site served through HTTP.
 */
'use strict';
const fs=require('node:fs');
const {chromium}=require('playwright');
const base=process.env.SMOKE_BASE_URL||'http://127.0.0.1:8765';
const output='browser-smoke-results';
fs.mkdirSync(output,{recursive:true});
const results=[],errors=[],missing=[];
const save=(step,status,details='')=>results.push({step,status,details});
async function run(){
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const desktop=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1,acceptDownloads:true});
 const page=await desktop.newPage();
 page.setDefaultTimeout(12000);
 function watch(p,label){
  p.on('pageerror',err=>errors.push({page:label,message:err.message}));
  p.on('response',res=>{if(res.url().startsWith(base)&&res.status()>=400)missing.push({page:label,url:res.url(),status:res.status()})});
 }
 watch(page,'desktop');
 const navigate=async(path)=>page.goto(base+path,{waitUntil:'domcontentloaded',timeout:45000});
 async function check(path,label,selector,critical=true){
  try{
   const response=await navigate(path);
   if(!response||response.status()>=400)throw Error('HTTP '+(response?response.status():'no response'));
   await page.locator(selector).first().waitFor({state:'visible',timeout:30000});
   save(label,'PASS',await page.title());
   return true;
  }catch(err){save(label,critical?'FAIL':'REVIEW',err.message);return false}
 }
 try{
  if(await check('/','Homepage','#main h1')){
   await page.screenshot({path:output+'/homepage-desktop.png',fullPage:true});
   const catalog=await page.evaluate(()=>window.LIBRARY&&window.LIBRARY.courses.map(c=>({id:c.id,name:c.name,units:c.units.map(u=>({id:u.id,name:u.name}))})));
   if(!catalog||catalog.length!==11)throw Error('Expected 11 courses, received '+(catalog?catalog.length:0));
   let checked=0;
   for(const c of catalog){
    await page.evaluate(t=>{location.hash=t},'#'+c.id);
    await page.waitForFunction(label=>document.querySelector('#main h1')?.textContent.includes(label),c.name,{timeout:6000});
    checked++;
    for(const u of c.units){
     await page.evaluate(t=>{location.hash=t},'#'+c.id+'.'+u.id);
     await page.waitForFunction(label=>document.querySelector('#main h1')?.textContent.includes(label),u.name,{timeout:6000});
     checked++;
    }
   }
   save('11 courses and '+(checked-11)+' unit routes','PASS','Rendered dynamically in Chromium');
   await page.evaluate(()=>{location.hash='#algebra.systems-of-equations'});
   await page.waitForFunction(()=>document.querySelector('#main h1')?.textContent.includes('Systems of Equations'));
   await page.screenshot({path:output+'/algebra-systems-unit.png',fullPage:true});
  }
 }catch(e){save('Course and unit navigation','FAIL',e.message)}
 for(const [path,label,selector] of [
  ['/about.html','About page','main h1'],
  ['/skills.html','Skills and standards browser','#results'],
  ['/backup.html','Saved-work backup','#export'],
  ['/worksheet-generator/worksheet.html','Worksheet generator','#mmMain'],
  ['/worksheet-generator/menu-assessment.html','Assessment generator','#mmMain'],
  ['/worksheet-generator/lesson-planner.html','Lesson planner','#plMain'],
  ['/worksheet-generator/printables.html','Printable generator','#prApp']
 ]){
  const ok=await check(path,label,selector);
  if(!ok)continue;
  if(label==='Worksheet generator'||label==='Assessment generator'){
   try{
    await page.locator('#mmBuildBtn').first().waitFor({state:'visible',timeout:18000});
    await page.locator('#mmBuildBtn').click({timeout:8000});
    await page.waitForTimeout(850);
    const view=await page.locator('#mmView').innerText();
    save(label+' build interaction',view&&view.length>30?'PASS':'REVIEW','Generated view text length '+(view||'').length);
   }catch(e){save(label+' build interaction','REVIEW',e.message)}
  }
  if(label==='Lesson planner'){
   try{
    await page.locator('#plNew').waitFor({state:'visible',timeout:15000});
    await page.locator('#plNew').click();
    await page.waitForTimeout(450);
    const len=(await page.locator('#plView').innerText()).length;
    save('Planner: regenerate problem set',len>60?'PASS':'REVIEW','Preview length '+len);
    await page.screenshot({path:output+'/planner-preview.png',fullPage:true});
   }catch(e){save('Planner regeneration','REVIEW',e.message)}
  }
  if(label==='Printable generator'){
   try{
    await page.locator('#prPreview').waitFor({state:'attached',timeout:16000});
    // The generator renders a temporary 29-character loading message before
    // building and independently checking its questions asynchronously.
    await page.waitForFunction(()=>{
     const preview=document.querySelector('#prPreview');
     return preview && !preview.querySelector('.pr-busy') &&
       !/Making and checking problems/i.test(preview.textContent||'');
    },null,{timeout:45000});
    const preview=await page.locator('#prPreview').innerText();
    const len=preview.trim().length;
    const hasContent=!!(await page.locator('#prPreview .page, #prPreview .mm-page, #prPreview .pr-page').count());
    const seemsBroken=/unable to|failed to|cannot generate|error generating/i.test(preview);
    save('Printable: preview',!seemsBroken&&(hasContent||len>150)?'PASS':'REVIEW',
     'Final preview length '+len+'; rendered page elements '+hasContent+'; excerpt: '+preview.slice(0,150));
    await page.screenshot({path:output+'/printable-preview.png',fullPage:true});
   }catch(e){save('Printable preview','REVIEW',e.message)}
  }
 }
 for (const [path,label] of [
  ['/artifacts/expressions-equations-balance-scale/index.html','Equation Balance Scale presentation'],
  ['/artifacts/statistics-regression-influence-lab/index.html','Statistics regression presentation']
 ]) {
  if (!await check(path,label,'.lab-present-button',false)) continue;
  try {
   const button=page.locator('.lab-present-button');
   await button.click();
   await page.waitForFunction(()=>document.querySelector('.lab-page')?.classList.contains('lab-presenting'));
   const inMode=await button.getAttribute('aria-pressed');
   const presentStage=await page.locator('.lab-grid .stage').count();
   save(label+' controls',inMode==='true'&&presentStage>0?'PASS':'REVIEW','Presenter toggle and interactive stage');
   const zoomOut=page.locator('.lab-zoom-control[aria-label="Zoom out"]');
   const zoomIn=page.locator('.lab-zoom-control[aria-label="Zoom in"]');
   const zoomValue=page.locator('.lab-zoom-value');
   await zoomOut.click();
   const shrunk=(await zoomValue.innerText()).trim()==='90%';
   const scaled=await page.evaluate(()=>{
    const content=document.querySelector('.lab-content'),stage=document.querySelector('.lab-grid .stage'),panel=document.querySelector('.lab-grid .panel');
    const g=stage.getBoundingClientRect(),c=panel.getBoundingClientRect();
    return {wrapper:!!content,stageWidth:g.width,controlsWidth:c.width,stageRight:g.right,controlsRight:c.right,viewport:innerWidth,sideBySide:c.left>g.left};
   });
   const balanced=scaled.wrapper&&scaled.controlsWidth>100&&scaled.stageWidth>100&&
    scaled.controlsRight<=scaled.viewport+6&&scaled.stageRight<=scaled.viewport+6&&scaled.sideBySide;
   save(label+' full-page scaling',balanced?'PASS':'REVIEW',JSON.stringify(scaled));
   await zoomIn.click();
   const restoredZoom=(await zoomValue.innerText()).trim()==='100%';
   await page.locator('.lab-zoom-fit').click();
   const fitValue=(await zoomValue.innerText()).trim();
   const range=parseInt(fitValue,10);
   const fitted=Number.isFinite(range)&&range>=50&&range<=100;
   const fitBounds=await page.evaluate(()=>{
    const g=document.querySelector('.lab-grid .stage').getBoundingClientRect();
    const p=document.querySelector('.lab-grid .panel').getBoundingClientRect();
    return {bottom:Math.round(Math.max(g.bottom,p.bottom)),right:Math.round(Math.max(g.right,p.right)),height:innerHeight,width:innerWidth};
   });
   const bothVisible=fitBounds.bottom<=fitBounds.height+6&&fitBounds.right<=fitBounds.width+6;
   save(label+' Fit both panels',bothVisible?'PASS':'REVIEW',JSON.stringify(fitBounds)+' zoom '+fitValue);
   await page.locator('.lab-zoom-reset').click();
   const reset=(await zoomValue.innerText()).trim()==='100%';
   save(label+' zoom controls',shrunk&&restoredZoom&&fitted&&reset?'PASS':'REVIEW',
    'Zoom out/in: '+shrunk+'/'+restoredZoom+'; fitted: '+fitValue+'; reset: '+reset);
   await page.screenshot({path:output+'/'+(label.startsWith('Equation')?'present-balance-scale':'present-regression')+'.png',fullPage:true});
   await button.click();
   const restored=await page.locator('.lab-page').evaluate(el=>!el.classList.contains('lab-presenting'));
   save(label+' exit',restored?'PASS':'REVIEW','Original student layout restored');
  }catch(e){save(label+' toggle','REVIEW',e.message)}
 }
 for(const [course,unit,game] of [
  ['algebra','systems-of-equations','flashcards'],
  ['geometry','circles','flashcards'],
  ['algebra2','functions-transformations','flashcards'],
  ['math6','ratios-rates-percent-proportions','flashcards']
 ]){
  const label='Student game '+course+'/'+unit;
  const path='/worksheet-generator/course-game.html?course='+course+'&unit='+unit+'&game='+game+'&student=1';
  if(await check(path,label,'#app',false)){
   try{
    await page.waitForFunction(()=>!document.querySelector('#app')?.textContent.includes('Loading mathematics game'),null,{timeout:40000});
    const txt=await page.locator('#app').innerText();
    save(label+' initialized',/Unable to load|not available for this unit/i.test(txt)?'REVIEW':'PASS',txt.slice(0,170));
   }catch(e){save(label+' initialized','REVIEW',e.message)}
  }
 }
 const mobile=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
 const phone=await mobile.newPage();watch(phone,'mobile');
 try{
  await phone.goto(base+'/',{waitUntil:'domcontentloaded',timeout:45000});
  await phone.locator('#main h1').waitFor();
  const width=await phone.evaluate(()=>({document:document.documentElement.scrollWidth,viewport:innerWidth}));
  save('Mobile homepage overflow',width.document>width.viewport+8?'REVIEW':'PASS',JSON.stringify(width));
  await phone.screenshot({path:output+'/homepage-mobile.png',fullPage:true});
 }catch(e){save('Mobile homepage','FAIL',e.message)}
 await mobile.close();await desktop.close();await browser.close();
 const uniqueMissing=[...new Map(missing.map(x=>[x.url,x])).values()];
 const uniqueErrors=[...new Map(errors.map(x=>[x.page+'|'+x.message,x])).values()];
 const report={createdAt:new Date().toISOString(),base,results,consoleExceptions:uniqueErrors,missingAssets:uniqueMissing};
 fs.writeFileSync(output+'/report.json',JSON.stringify(report,null,2));
 let md='# Chromium smoke test\n\n| Check | Result | Details |\n|---|---|---|\n';
 for(const r of results)md+='| '+r.step.replaceAll('|','/')+' | '+r.status+' | '+String(r.details).slice(0,130).replaceAll('|','/').replace(/\n/g,' ')+' |\n';
 md+='\nUncaught browser exceptions: '+uniqueErrors.length+'; missing local assets: '+uniqueMissing.length+'.\n';
 fs.writeFileSync(output+'/summary.md',md);
 if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,md);
 const failed=results.filter(x=>x.status==='FAIL');
 console.log(JSON.stringify({passed:results.filter(x=>x.status==='PASS').length,review:results.filter(x=>x.status==='REVIEW').length,failed,exceptions:uniqueErrors.slice(0,10),missing:uniqueMissing.slice(0,15)},null,2));
 if(failed.length||uniqueMissing.length)process.exitCode=1;
}
run().catch(err=>{console.error(err);process.exitCode=1});
