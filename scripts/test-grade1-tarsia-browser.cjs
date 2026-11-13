#!/usr/bin/env node
const fs=require('node:fs'),{chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']}),page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 try{
  await page.goto((process.env.GRADE1_BASE||'http://127.0.0.1:8765')+'/worksheet-generator/printables.html#unit=grade1-adding-subtracting-working-data&kind=tarsia');
  await page.waitForFunction(()=>window.MK_COURSE_BANKS_READY);await page.evaluate(()=>MK_COURSE_BANKS_READY);
  await page.locator('#prTarsiaSize').waitFor();
  const result=await page.evaluate(async()=>{
   const PR=MKMENU.printables,host=document.querySelector('#prPreview'),result={rendered:0,pages:0,images:0,codes:0,sizes:{}};
   for(const unit of LIBRARY.courses.find(c=>c.id==='grade1').units)for(const size of ['starter','small','medium','large','full']){
    const cfg={...PR.defaultConfig('grade1-'+unit.id,'tarsia'),level:'cp1',seed:'tarsia-layout-audit',tarsiaSize:size},B=PR.build(cfg,0);if(B.error)continue;
    result.sizes[size]=(result.sizes[size]||0)+1;result.codes+=B.answerBank.length;
    for(const layout of ['standard','compact','large'])for(const teacher of [false,true]){
     cfg.tarsiaLayout=layout;const els=PR.pageEls(cfg,B,0,1,teacher);host.replaceChildren(...els);result.pages+=els.length;
     for(const img of host.querySelectorAll('img')){await img.decode();result.images++;}
     for(const body of host.querySelectorAll('.mm-body'))if(body.scrollHeight>body.clientHeight+2||body.scrollWidth>body.clientWidth+2)throw Error('Tarsia overflow '+unit.id+'/'+size+'/'+layout+'/'+teacher+' '+body.scrollHeight+'/'+body.clientHeight);
     if(!teacher&&host.querySelector('.mm-ans'))throw Error('Student solution leak');
     for(const code of B.answerBank)if(!host.textContent.includes(code.answer)||!host.textContent.includes(code.label))throw Error('Missing coded answer');
     for(const it of B.items)if(!host.textContent.includes(it.p.prompt))throw Error('Missing source prompt');
     result.rendered++;
    }
   }
   if(!result.images||!result.codes||Object.keys(result.sizes).length!==5)throw Error('Incomplete Tarsia cases');
   return result;
  });
  await page.locator('#prTarsiaSize').selectOption('small');
  await page.locator('#prPreview').getByText(/4 pieces · 3 matches/).first().waitFor();
  fs.mkdirSync('grade1-integration-results',{recursive:true});
  await page.locator('#prPreview .mm-page').first().screenshot({path:'grade1-integration-results/tarsia-student.png'});
  await page.locator('[data-doc=key]').click();
  await page.locator('#prPreview').getByText(/Solved puzzle/).first().waitFor();
  await page.locator('#prPreview .mm-page').first().screenshot({path:'grade1-integration-results/tarsia-key.png'});
  if(errors.length)throw Error(JSON.stringify(errors));
  fs.writeFileSync('grade1-integration-results/tarsia-browser.json',JSON.stringify({passed:true,...result},null,2));console.log(JSON.stringify({passed:true,...result}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
