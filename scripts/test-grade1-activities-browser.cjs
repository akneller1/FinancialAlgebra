#!/usr/bin/env node
const fs=require('node:fs'),{chromium}=require('playwright');
const base=process.env.GRADE1_BASE||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']}),page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[],broken=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)broken.push(r.status()+' '+r.url());});
 try{
 await page.goto(base+'/worksheet-generator/printables.html#unit=grade1-adding-subtracting-working-data&kind=color');
 await page.waitForFunction(()=>window.MK_COURSE_BANKS_READY);await page.evaluate(()=>MK_COURSE_BANKS_READY);
 await page.locator('#prPreview .pc-scene').waitFor();
 const result=await page.evaluate(async()=>{
  const PR=MKMENU.printables,host=document.querySelector('#prPreview'),all=new Map();let rendered=0,pages=0,images=0,blocked=0;
  const courses=LIBRARY.courses.filter(c=>c.id==='grade1');
  for(const c of courses)for(const u of c.units)MK_QUESTION_BANKS.select({courseId:'grade1',unitId:u.id}).forEach(q=>all.set(q.id,q));
  function ids(B,set=new Set(),seen=new Set()){if(!B||typeof B!=='object'||seen.has(B))return set;seen.add(B);if(B.sourceId)set.add(B.sourceId);Object.values(B).forEach(x=>{if(x&&typeof x==='object')ids(x,set,seen)});return set;}
  for(const c of courses)for(const u of c.units)for(const kind of ['maze','color','tarsia','stations','error']){
   const cfg={...PR.defaultConfig('grade1-'+u.id,kind),level:'cp1',seed:'full-activity-audit'},B=PR.build(cfg,0);
   if(B.error){blocked++;continue;}
   const sources=[...ids(B)].map(id=>all.get(id));if(!sources.length||sources.some(q=>!q||q.level!==cfg.level||!cfg.skills[q.skillId]))throw Error('Wrong source scope '+u.id+'/'+kind);
   for(const teacher of [false,true]){
    const els=PR.pageEls(cfg,B,0,1,teacher);host.replaceChildren(...els);pages+=els.length;
    for(const img of host.querySelectorAll('img')){await img.decode();images++;}
    const present=[...host.querySelectorAll('img')].map(im=>im.src);
    for(const q of sources.filter(q=>q.diagram))if(!present.includes(new URL('../'+q.diagram.spec.src,location.href).href))throw Error('Source image missing '+q.id+'/'+kind);
    if(!teacher&&host.querySelector('.mm-ans'))throw Error('Source solutions leaked '+kind);
    for(const body of host.querySelectorAll('.mm-body'))if(body.scrollHeight>body.clientHeight+2||body.scrollWidth>body.clientWidth+2)throw Error('Page overflow '+u.id+'/'+kind+'/'+teacher+' '+body.scrollHeight+'/'+body.clientHeight);
    if(kind==='color'&&teacher){
     const fills=[...host.querySelector('.pc-scene').children].filter(el=>el.tagName.toLowerCase()==='g'&&el.getAttribute('fill')!=='none').map(el=>el.getAttribute('fill').toLowerCase());
     const expected=B.groupNum.map(n=>PR.SCENE_COLORS[B.colorOf[n-1]].toLowerCase());
     if(JSON.stringify(fills)!==JSON.stringify(expected))throw Error('Color key contradicts answer-to-color mapping');
    }
   }rendered++;
  }
  return {rendered,pages,images,blocked};
 });
 // A deliberately oversized puzzle must fail without changing the selected level.
 await page.goto(base+'/worksheet-generator/printables.html#unit=grade1-adding-subtracting-working-data&kind=tarsia');await page.reload();
 await page.locator('input[name=prLevel][value=cp2]').check();
 const ids=await page.locator('.prSkill').evaluateAll(xs=>xs.map(x=>x.value));
 for(const id of ids.slice(1))await page.locator('.prSkill[value="'+id+'"]').uncheck();
 await page.locator('#prTarsiaSize').selectOption('large');
 await page.locator('#prPreview .pr-err').waitFor();
 if(!await page.locator('#prPrintS').isDisabled()||!await page.locator('#prPrintK').isDisabled())throw Error('Unavailable puzzle may print');
 if(!/Remedial/.test(await page.locator('#prPreview .pr-err').innerText()))throw Error('Missing selected-level explanation');
 fs.mkdirSync('grade1-integration-results',{recursive:true});
 await page.goto(base+'/worksheet-generator/printables.html#unit=grade1-adding-subtracting-working-data&kind=color');await page.reload();
 await page.locator('input[name=prLevel][value=cp2]').check();await page.locator('#prPreview .pc-scene').waitFor();
 await page.locator('#prPreview .mm-page').first().screenshot({path:'grade1-integration-results/color-remedial.png'});
 await page.locator('[data-doc=key]').click();await page.locator('#prPreview .pc-redk').first().waitFor();
 await page.locator('#prPreview .mm-page').first().screenshot({path:'grade1-integration-results/color-remedial-key.png'});
 if(errors.length||broken.length)throw Error(JSON.stringify({errors,broken}));
 fs.writeFileSync('grade1-integration-results/activities-browser.json',JSON.stringify({passed:true,...result,errors,broken},null,2));console.log(JSON.stringify({passed:true,...result}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
