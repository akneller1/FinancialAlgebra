#!/usr/bin/env node
const fs=require('node:fs'),{chromium}=require('playwright');
const base=process.env.GRADE1_BASE||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']}),page=await browser.newPage({viewport:{width:1280,height:900}});
 const errors=[],broken=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)broken.push(r.status()+' '+r.url());});
 page.setDefaultTimeout(20000);fs.mkdirSync('grade1-integration-results',{recursive:true});let pages=0;
 try{
 const outline=JSON.parse(fs.readFileSync('course-outlines/grade1.json'));
 async function open(tool,unit,extra={}){
  const p=new URLSearchParams({course:'math1',unit,tool,student:'1',level:'cp1',...extra});
  await page.goto(base+'/elementary/worksheet-generator/elementary-resource.html?'+p);
  await page.waitForFunction(()=>window.G5&&window.MK_GRADE1_STAGING);
 }
 // All unit banks flow through the real loader into each study guide.
 for(const u of outline.units){
  await open('flashcards',u.id);await page.locator('.fc-card').waitFor();await page.locator('.fc-card').click();pages++;
  await open('check',u.id);await page.locator('.g5-q').first().waitFor();pages++;
 }
 // Every shared game boots with Grade 1 content in a single selected skill.
 for(const game of ['math-quest','treasure-trail','space-explorer','math-builders','picture-reveal','math-race','math-soccer','connect-four','puzzle-masters']){
  const u=outline.units[0];await open('games',u.id,{game,skills:JSON.stringify([u.id+'-skill-01'])});
  await page.locator('.g5-stage').waitFor();if(/not enough|unavailable|not published/i.test(await page.locator('#app').innerText()))throw Error('Game failed '+game);pages++;
 }
 // Exercise the actual shared Puzzle Masters engine for all 279 selections.
 await page.setViewportSize({width:390,height:844});
 const puzzle=await page.evaluate(async()=>{
  const source=await(await fetch('grade5/g5-games.js')).text(),outline=await(await fetch('../course-outlines/grade1.json')).json();
  const timer=window.setTimeout;window.setTimeout=(fn,ms,...args)=>timer(fn,ms===300||ms===1400?0:ms,...args);
  let scopes=0,images=0;
  const pause=()=>new Promise(r=>timer(r,5));
  for(const u of outline.units)for(let i=0;i<u.skills.length;i++)for(const level of ['cp2','cp1','honors']){
   const skill=u.id+'-skill-'+String(i+1).padStart(2,'0');document.querySelector('#app').replaceChildren();
   G5.P=new URLSearchParams({unit:u.id,game:'puzzle-masters'});
   G5.chooseSkills=(info,start)=>start([skill]);G5.setupPanel=(host,cfg)=>cfg.start({level,mode:'solo'});
   window.eval(source);
   for(let attempt=0;!document.querySelector('.g5-stage [data-card-kind]')&&attempt<2000;attempt++)await pause();
   const qs=[...document.querySelectorAll('[data-card-kind=q]')],as=[...document.querySelectorAll('[data-card-kind=a]')];
   if(qs.length<4)throw Error('Insufficient real-engine cards '+skill+'/'+level);
   for(const q of qs){
    if(!q.dataset.questionId.startsWith('m1-'))throw Error('Wrong bank');
    q.click();for(const im of q.querySelectorAll('img')){await im.decode();images++;}
    const j=as.findIndex(a=>a.dataset.answerValue===q.dataset.answerValue),a=as.splice(j,1)[0];if(!a)throw Error('Missing equivalent answer');a.click();
    for(let attempt=0;!q.disabled&&attempt<200;attempt++)await pause();if(!q.disabled)throw Error('Match failed '+skill);
   }
   if(!/Puzzle solved/.test(document.querySelector('#app').innerText))throw Error('Not solved '+skill+'/'+level);
   if(document.documentElement.scrollWidth>innerWidth+2)throw Error('Mobile overflow '+skill+'/'+level);
   if(MK_GRADE1_STAGING.originalAvailable('math1',u.id))throw Error('Bank became verified');
   scopes++;
  }
  window.setTimeout=timer;return {scopes,images};
 });
 await page.screenshot({path:'grade1-integration-results/puzzle-mobile.png',fullPage:true});
 await page.setViewportSize({width:1280,height:900});
 // The native Classroom engines receive the adapted Grade 1 course without approval.
 for(const [file,button] of [['worksheet.html','#mmBuildBtn'],['menu-assessment.html','#mmBuildBtn'],['printables.html','#prNew'],['lesson-planner.html','#plNew']]){
  await page.goto(base+'/worksheet-generator/'+file+'#unit=grade1-'+outline.units[0].id);
  await page.waitForFunction(()=>window.MK_COURSE_BANKS_READY);await page.evaluate(()=>MK_COURSE_BANKS_READY);
  await page.locator(button).waitFor();await page.locator(button).click();
  await page.waitForTimeout(300);
  const state=await page.evaluate(()=>({registered:!!MKMENU.skillSets['grade1-adding-subtracting-working-data']?.authoredBank,verified:MK_GRADE1_STAGING.originalAvailable('grade1','adding-subtracting-working-data'),pending:!!window.MK_PRELOADED_UNITS?.['grade1-adding-subtracting-working-data'],course:window.MKPLAN_COURSE,selected:(document.querySelector('#mmUnitSel')||document.querySelector('#prUnit'))?.value,failures:[...document.querySelectorAll('.pl-missing')].map(x=>x.textContent)}));
  if(!state.registered||state.verified||state.pending||state.failures.length)throw Error(file+' '+JSON.stringify(state));
  if(file!=='lesson-planner.html'&&state.selected!=='grade1-'+outline.units[0].id)throw Error('Wrong generator selection '+file+' '+state.selected);
  if(file==='lesson-planner.html'&&state.course!=='grade1')throw Error('Wrong planner course');
  await page.screenshot({path:'grade1-integration-results/'+file+'.png',fullPage:true});pages++;
 }
 if(errors.length||broken.length)throw Error(JSON.stringify({errors,broken}));
 fs.writeFileSync('grade1-integration-results/report.json',JSON.stringify({passed:true,pages,puzzle,errors,broken},null,2));console.log(JSON.stringify({passed:true,pages,puzzle}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
