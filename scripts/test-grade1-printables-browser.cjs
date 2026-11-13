#!/usr/bin/env node
const fs=require('node:fs'),{chromium}=require('playwright');
const base=process.env.GRADE1_BASE||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']}),page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[],broken=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)broken.push(r.status()+' '+r.url());});
 try{
 await page.goto(base+'/worksheet-generator/printables.html#unit=grade1-adding-subtracting-working-data&kind=answer-match');
 await page.waitForFunction(()=>window.MK_COURSE_BANKS_READY);await page.evaluate(()=>MK_COURSE_BANKS_READY);
 await page.locator('input[name=prKind][value=answer-match]:checked').waitFor({state:'attached'});
 await page.locator('#prPreview .g1-printable').first().waitFor();
 const models=await page.evaluate(()=>{
  const PR=MKMENU.printables,classes=LIBRARY.courses.filter(c=>c.id==='grade1');let scopes=0,partner=0;
  for(const c of classes)for(const u of c.units)for(const s of MK_COURSE_CATALOG.getSkillRecords(c.id,u.id))for(const level of ['cp2','cp1','honors']){
   const cfg={...PR.defaultConfig('grade1-'+u.id,'answer-match'),skills:{[s.id]:true},level,seed:'browser-contract'};
   const m=PR.build(cfg,0);if(m.error||!m.items.length)throw Error('No matching selection '+s.id+'/'+level);
   const qs=MK_QUESTION_BANKS.select({courseId:'grade1',unitId:u.id,level,skillIds:[s.id]});
   for(const it of m.items){const q=qs.find(q=>q.id===it.p.sourceId);if(!q||q.prompt!==it.p.prompt)throw Error('Scope or source text changed');if(!m.answers.some(a=>a.letter===it.letter&&MK_GRADE1_PRINTABLES.key(a.value)===MK_GRADE1_PRINTABLES.key(q.answer)))throw Error('Wrong matching key');}
   const p=PR.build({...cfg,kind:'partner'},0);
   if(!p.error){partner++;for(const r of p.rows){const a=qs.find(q=>q.id===r.A.p.sourceId),b=qs.find(q=>q.id===r.B.p.sourceId);if(!a||!b||a.id===b.id||a.skillId!==b.skillId||MK_GRADE1_STAGING.content[a.id]===MK_GRADE1_STAGING.content[b.id]||MK_GRADE1_PRINTABLES.key(a.answer)!==MK_GRADE1_PRINTABLES.key(b.answer))throw Error('Invalid source pair');}}
   if(MK_GRADE1_STAGING.originalAvailable('grade1',u.id))throw Error('Approval changed');scopes++;
  }
  return {scopes,partner};
 });
 if(models.scopes!==279||models.partner!==187)throw Error('Unexpected printable coverage '+JSON.stringify(models));
 const rendered=await page.evaluate(async()=>{
  const PR=MKMENU.printables;let samples=0,images=0,pages=0;
  const host=document.querySelector('#prPreview');
  for(const c of LIBRARY.courses.filter(c=>c.id==='grade1'))for(const u of c.units)for(const level of ['cp2','cp1','honors'])for(const kind of ['answer-match','partner']){
   const records=MK_COURSE_CATALOG.getSkillRecords('grade1',u.id),s=records.find(s=>kind==='answer-match'||PR.capable('grade1-'+u.id,s.id,kind,level));if(!s)continue;
   const cfg={...PR.defaultConfig('grade1-'+u.id,kind),skills:{[s.id]:true},level,seed:'rendered-sample',count:4},B=PR.build(cfg,0);if(B.error)throw Error(B.error);
   for(const teacher of [false,true]){
    const elements=PR.pageEls(cfg,B,0,1,teacher);host.replaceChildren(...elements);
    for(const img of host.querySelectorAll('img')){await img.decode();images++;}
    if(!teacher&&host.querySelector('.mm-ans'))throw Error('Teacher solution leaked');
    if(teacher&&!host.querySelector('.mm-ans'))throw Error('Missing key');
    const expectedImages=kind==='partner'?B.rows.reduce((n,r)=>n+!!r.A.p.fig+!!r.B.p.fig,0):B.items.filter(it=>it.p.fig).length;
    if(host.querySelectorAll('img').length!==expectedImages)throw Error('Dropped source diagram');
    for(const body of host.querySelectorAll('.g1-printable'))if(body.scrollHeight>body.clientHeight+2||body.scrollWidth>body.clientWidth+2)throw Error('Printable overflow '+u.id+'/'+level+'/'+kind+'/'+teacher+' '+body.scrollHeight+'/'+body.clientHeight);
    pages+=elements.length;
   }samples++;
  }
  return {samples,images,pages};
 });
 fs.mkdirSync('grade1-integration-results',{recursive:true});
 // Preserve readable images of a visual matching sheet and its teacher key.
 await page.goto(base+'/worksheet-generator/printables.html#unit=grade1-geometry-time&kind=answer-match');
 await page.locator('#prPreview .g1-printable').first().waitFor();
 await page.locator('#prPreview .mm-page').nth(1).screenshot({path:'grade1-integration-results/matching-printable.png'});
 await page.goto(base+'/worksheet-generator/printables.html#unit=grade1-adding-subtracting-working-data&kind=partner');
 await page.locator('#prPreview .g1-printable').first().waitFor();
 await page.locator('#prPreview .mm-page').first().screenshot({path:'grade1-integration-results/partner-printable.png'});
 if(errors.length||broken.length)throw Error(JSON.stringify({errors,broken}));
 fs.writeFileSync('grade1-integration-results/printables-browser.json',JSON.stringify({passed:true,models,rendered,errors,broken},null,2));console.log(JSON.stringify({passed:true,models,rendered}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
