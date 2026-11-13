#!/usr/bin/env node
const fs=require('node:fs'),{chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{}),args:['--no-sandbox']});
 try{
 const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto((process.env.GRADE1_BASE||'http://127.0.0.1:8765')+'/tools/grade1-authoring/staging-games.html');
 await page.waitForFunction(()=>window.stagingGame);
 const result=await page.evaluate(async()=>{
  const outline=await(await fetch('../../course-outlines/grade1.json')).json();let scopes=0,images=0;
  for(const u of outline.units){
   const bank=await(await fetch('../../question-banks/math1/'+u.id+'.json')).json();
   for(let i=0;i<u.skills.length;i++)for(const level of ['cp2','cp1','honors']){
    const skill=u.id+'-skill-'+String(i+1).padStart(2,'0'),root=document.querySelector('#game');
    const game=G1StagingPuzzle.mount(root,bank.questions,skill,level,'../../');
    const model=game.model;
    // Click actual buttons. Equivalent answers are interchangeable, including repeated values.
    const unused=model.cards.filter(c=>c.kind==='answer');
    for(const q of model.cards.filter(c=>c.kind==='question')){
     root.querySelector('[data-card-id="'+q.id+'"]').click();
     for(const img of root.querySelectorAll('img')){await img.decode();if(!img.naturalWidth)throw Error('Broken image '+img.src);images++;}
     const j=unused.findIndex(a=>a.value===q.value),answer=unused.splice(j,1)[0];
     if(!answer)throw Error('Unmatchable '+skill+'/'+level);
     root.querySelector('[data-card-id="'+answer.id+'"]').click();
    }
    if(!game.state().solved||!root.textContent.includes('Puzzle solved!'))throw Error('Not solved '+skill+'/'+level);
    if(document.documentElement.scrollWidth>window.innerWidth+2)throw Error('Mobile overflow '+skill+'/'+level);
    scopes++;
   }
  }
  return {scopes,images};
 });
 if(errors.length)throw Error(errors.join('\n'));
 fs.mkdirSync('grade1-browser-results',{recursive:true});
 await page.screenshot({path:'grade1-browser-results/puzzle-mobile.png',fullPage:true});
 fs.writeFileSync('grade1-browser-results/puzzle.json',JSON.stringify({...result,errors},null,2));
 console.log(JSON.stringify(result));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
