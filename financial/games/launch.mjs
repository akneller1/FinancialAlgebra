import {GAMES,eligible,createDeck,gameItem} from './deck.mjs?v=fa-games-1';
const app=document.getElementById('app'),p=new URLSearchParams(location.search),unit=p.get('unit')||'income',game=p.get('game')||'showdown';
const render=window.FA_RENDER;
function script(path){return new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=new URL(path,import.meta.url);s.onload=resolve;s.onerror=()=>reject(Error('The game engine could not load. Please reload.'));document.body.append(s);});}
function style(path){const l=document.createElement('link');l.rel='stylesheet';l.href=new URL(path,import.meta.url);document.head.append(l);}
async function start(){
 const record=GAMES.find(g=>g.id===game);if(!record||! /^[a-z-]+$/.test(unit))throw Error('Choose a valid Financial Algebra game and unit.');
 const res=await fetch(new URL('../banks/'+unit+'.json',import.meta.url));if(!res.ok)throw Error('This unit could not load. Return to the course and choose a unit.');
 const bank=await res.json();const all=eligible(bank);if(!all.length)throw Error('No game questions are available for this unit.');
 const name=bank.unitName+' '+record.name;document.title=name+' | Financial Algebra';document.getElementById('gameName').textContent=name;
 document.getElementById('courseBack').href+='\x23financial-algebra.'+unit;
 const setId='financial-algebra-'+unit,rng=window.MKWS.rng.make(Date.now()),draw=createDeck(bank,rng);
 if(game==='detective'){
  window.TeacherSkills.choose(bank.skills,ids=>{
   app.replaceChildren();const h=document.createElement('h1');h.textContent=name;app.append(h);
   const info=document.createElement('p');info.textContent='Standard · Solve ten questions to earn evidence and make your accusation.';app.append(info);
   const b=document.createElement('button');b.className='gm-btn primary';b.textContent='Start Detective';app.append(b);
   const status=document.createElement('p');status.setAttribute('role','status');app.append(status);
   b.onclick=async()=>{try{
    const pool=all.filter(q=>ids.includes(q.skillId));if(pool.length<10){status.textContent='These skills have '+pool.length+' game questions. Choose additional skills to play the ten-clue case.';const again=document.createElement('button');again.className='gm-btn';again.textContent='Choose skills again';again.onclick=()=>location.reload();app.append(again);return;}
    b.disabled=true;
    // Round-robin skills so the case covers the selected topics.
    const groups=ids.map(id=>rng.shuffle(pool.filter(q=>q.skillId===id))),qs=[];
    while(qs.length<10)for(const group of groups)if(group.length&&qs.length<10)qs.push(group.pop());
    const response=await fetch(new URL('vendor/mystery-case.json',import.meta.url));if(!response.ok)throw Error('The case file could not load.');const data=await response.json();
    data.unit=setId+'-'+ids.slice().sort().join('_')+'-'+qs.map(q=>q.id).join('_');
    data.eyebrow='Financial Algebra · Standard';data.title=name;data.tagline='Use financial reasoning to earn clues and solve the mystery.';
    data.symbols=[];data.inputHint='Choose an answer, then check it to collect evidence.';
    data.questions=qs.map(q=>({sourceId:q.id,skill:bank.skills.find(s=>s.id===q.skillId).name,instr:'',
     html:render.scenario(q.scenario)+'<div class="prompt">'+render.rich(q.prompt)+'</div>',answer:{t:'source-choice',v:q.options.findIndex(o=>o.correct)},
     options:q.options.map(o=>render.rich(o.text)),hint:render.rich(q.solutionSteps?.[0]||''),steps:(q.solutionSteps||[]).map(render.rich)}));
    window.MK_ACTIVE_MYSTERY_CASE=data;style('vendor/mystery.css');app.className='';await script('vendor/mystery-runtime.js');
   }catch(e){status.textContent=e.message;b.disabled=false;}};
  });return;
 }
 const tags=Object.fromEntries(bank.skills.map(s=>[s.id,s.name]));const skills=bank.skills.map(s=>({...s,tag:s.id}));
 window.MKMENU={skillSets:{[setId]:{unitName:bank.unitName,courseName:'Financial Algebra',authoredBank:true,tags,skills,byId:Object.fromEntries(skills.map(s=>[s.id,s]))}},figHtml:html=>html};
 window.MK_MATH_DISPLAY={html:render.rich};
 window.MKGAMES={LEVELS:{cp1:{name:'Standard',tiers:[1,2,3]}},HINTS:{},
  hasGameItems:(_,id)=>all.some(q=>q.skillId===id),hasFlashcardItems:()=>true,
  buildDeck:(_,slots,opts,done)=>{const result=draw(slots).map(q=>gameItem(q,render));opts?.progress?.(result.length,slots.length);done(result);}};
 document.body.dataset.unit=setId;document.body.dataset.game=game;document.body.dataset.title=name;
 await script('vendor/games.js');
}
start().catch(e=>{app.replaceChildren();const message=document.createElement('p');message.setAttribute('role','alert');message.textContent=e.message;app.append(message);});
