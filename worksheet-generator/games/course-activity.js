/* Established Algebra 1 activity formats, fed only by existing course content. */
(async function(G){'use strict';
await G.MK_ALGEBRA2_NATIVE_READY;
const source=G.MK_COURSE_ACTIVITY_SOURCE,p=new URLSearchParams(location.search),escape=p.get('game')==='escape-room',kind=escape?'Escape Room':'Detective';
const app=document.getElementById('app');document.title=(source.unit?.name||'Classroom')+' '+kind;
if(!source.unit){app.textContent='Select a valid course and unit.';return}
const all=source.records();let ids=all.map(s=>s.id);
function el(tag,host,text){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;host.appendChild(n);return n}
function setup(selected){
 ids=selected;app.replaceChildren();el('h1',app,source.unit.name+' '+kind);
 const label=el('label',app,'Difficulty '),level=el('select',label);level.id='activityLevel';level.className='gm-sel';for(const [v,t] of [['cp2','CP2'],['cp1','CP1'],['honors','Honors']]){const o=el('option',level,['math5','math6','prealgebra7','prealgebra'].includes(source.courseId)?{cp2:'Remedial',cp1:'Standard',honors:'Advanced'}[v]:t);o.value=v}level.value='cp1';
 el('p',app,escape?'Five rooms, interactive locks, a cipher, hints, key cards, and a final password. Work as a team: ten minutes, with a 30-second penalty for incorrect submissions.':'Solve problems to collect evidence. Clear suspects, locations, and methods, then make your final accusation.');
 const start=el('button',app,'Start '+kind);start.id='activityStart';start.className='gm-btn primary';const status=el('p',app);status.id='activityStatus';status.setAttribute('role','status');
 start.onclick=async()=>{const qs=source.select(level.value,ids,G.MK_QUESTION_BANKS.available(source.courseId,source.unit.id)?120:20);const mc=qs.filter(q=>q.format==='multiple-choice');if((escape?qs.length:mc.length)<(escape?5:10)){status.textContent=qs.length?'Choose more skills at this difficulty to fill this activity.':'Questions are not available for this course and unit yet. The activity settings are ready for a future bank.';return}start.disabled=true;try{if(escape)await startEscape(qs,level.value);else await startMystery(mc,level.value)}catch(e){status.textContent='Unable to open activity: '+e.message;start.disabled=false}};
 if(!['algebra','geometry'].includes(source.courseId)&&!G.MK_QUESTION_BANKS.available(source.courseId,source.unit.id))status.textContent='Questions are not available for this course and unit yet. The activity settings are ready for a future bank.';
}
function loadCSS(path){const l=el('link',document.head);l.rel='stylesheet';l.href=path+'?v=unit-themes-20261105'}
function script(path){return new Promise((resolve,reject)=>{const s=el('script',document.body);s.src=path+'?v=unit-themes-20261105';s.onload=resolve;s.onerror=()=>reject(Error('Activity engine unavailable'))})}
async function startMystery(qs,level){
 const data=await fetch('games/mystery-case.json',{cache:'no-store'}).then(r=>r.json());data.unit=source.courseId+'-'+source.unit.id+'-'+level;data.eyebrow=source.course.name+' · Detective';data.title=source.unit.name+' Detective';data.tagline='Solve each problem to earn evidence and crack the case.';data.inputHint='Choose an answer, then check it to unlock your evidence.';data.symbols=[];
 data.questions=qs.slice(0,10).map(q=>({sourceId:q.id,skill:all.find(s=>s.id===q.skillId)?.name||q.skillId,instr:'',html:source.question(q),answer:{t:'source-choice',v:q.options.findIndex(o=>o.correct)},options:q._graphOptions||q.options.map(o=>source.html(o.text)),hint:source.html(q.solutionSteps[0]||''),steps:q.solutionSteps.map(source.html)}));
 G.MK_ACTIVE_MYSTERY_CASE=data;loadCSS('games/mystery.css');app.className='';document.getElementById('activityHeader').hidden=true;await script('games/mystery-runtime.js');
}
async function startEscape(qs,selectedLevel){
 const base=await fetch('games/escape-room.json',{cache:'no-store'}).then(r=>r.json()),used=new Set();
 // Every course unit has its own story, password, cipher message and clue word (games/escape-themes.json).
 const themes=await fetch('games/escape-themes.json',{cache:'no-store'}).then(r=>r.ok?r.json():{}).catch(()=>({}));
 const theme=themes[source.courseId+'/'+source.unit.id]||null;
 const roomWord=theme?theme.room:'gallery',RoomWord=roomWord.replace(/\b\w/g,c=>c.toUpperCase());
 function take(test){const q=qs.find(q=>!used.has(q.id)&&test(q));if(q)used.add(q.id);return q}
 function numericValue(q){
  const raw=String(q && q.answer!=null?q.answer:'').trim().replace(/−/g,'-');
  const match=/^(?:[A-Za-z]\s*=\s*)?([+-]?\d+(?:\.0+)?)$/.exec(raw);
  return match?Number(match[1]):null;
 }
 function numeric(q){return numericValue(q)!==null}
 function shiftQuestion(q){
  const n=numericValue(q);
  return Number.isInteger(n)&&n>=1&&n<=25 &&
    !/\b(which of the following|choose (?:the|an) (?:answer|option)|select all|which graph)\b/i.test(q.prompt||'');
 }
 function orderedSteps(q){
  const original=(q.solutionSteps||[]).map(s=>String(s||'').trim()).filter(Boolean);
  const unique=original.filter((step,i)=>original.findIndex(x=>x.toLowerCase()===step.toLowerCase())===i);
  if(unique.length>=4)return unique;
  // Two-line slope comparisons benefit from separate mathematical actions:
  // calculate m1, calculate m2, compare, and classify.
  if(unique.length>=2&&/\b(parallel|perpendicular)\b/i.test(q.prompt||'')){
   const slope=/^(?:find|calculate|determine)\s+both\s+slopes:\s*(.+?)\s+and\s+(.+?)\.?$/i.exec(unique[0]);
   if(slope){
    return [
      'Find the slope of the first line: '+slope[1].replace(/\.$/,'')+'.',
      'Find the slope of the second line: '+slope[2].replace(/\.$/,'')+'.',
      unique[1],
      'Compare the slopes and classify the two lines: '+String(q.answer||'').trim()+'.'
    ];
   }
  }
  // A three-step solution needs a separate conclusion, not repeated filler.
  if(unique.length===3)return unique.concat([
   'State the final result and check that it answers the question: '+String(q.answer||'').trim()+'.'
  ]);
  if(unique.length===2){
   return [
    'Identify the mathematical relationship, property, or equation needed to solve the problem.',
    unique[0],unique[1],
    'Verify the result against the original information: '+String(q.answer||'').trim()+'.'
   ];
  }
  // Do not manufacture a meaningless sorting puzzle from a one-line answer.
  return null;
 }
 function scene(q){const em=theme?theme.scene:['🏺','🖼️','📜','🗝️'];return q.diagram?.type==='image'?{kind:'image',src:q.diagram.spec.src,alt:q.diagram.spec.alt.replace(/"/g,'&quot;')}:{kind:'emoji',bg:theme?theme.bg:'#1d1530',floor:theme?theme.floor:'#3a2b4a',items:[{e:em[0],x:80,y:170,s:60},{e:em[1],x:170,y:150,s:56},{e:em[2],x:250,y:160,s:50},{e:em[3],x:330,y:170,s:50}]}}
 function prompt(q,includeOptions){return source.question(q)+(includeOptions&&q.options?'<ol type="A">'+q.options.map((o,i)=>'<li>'+(q._graphOptions?q._graphOptions[i]:source.html(o.text))+'</li>').join('')+'</ol>':'')}
 function stage(q,i){return {name:all.find(s=>s.id===q.skillId)?.name||RoomWord+' '+(i+1),sourceId:q.id,stamp:(theme?theme.stamps:[41,12,87,23,55])[i],letter:(theme?theme.letters:['M','C','T','O','E'])[i],story:'Solve the '+roomWord+' challenge to unlock the next door and collect its key card.',scene:scene(q),hints:q.solutionSteps.slice(0,3).map(source.html),key:source.html(String(q.answer))}}
 function choice(q,i){return {...stage(q,i),type:'bankChoice',title:'Unlock the door',prompt:prompt(q,false),options:q._graphOptions||q.options.map(o=>source.html(o.text)),answer:q.options.findIndex(o=>o.correct)}}
 // Reserve a numerical item for the cipher before building other rooms.
 const unitCipher=G.MK_CIPHER_QUESTIONS&&G.MK_CIPHER_QUESTIONS.create({
   courseId:source.courseId,unitId:source.unit.id,level:selectedLevel
 });
 // Systems must always require solving a system, not an unrelated numeric subskill.
 // Other units prefer approved numeric items from the selected unit/skills, then a
 // topic-specific numerical challenge. Never fall back to a generic equation.
 const bankCipher=source.unit.id.includes('system')?null:
   take(q=>q.format==='short-answer'&&shiftQuestion(q))||take(shiftQuestion);
 const q2=bankCipher||unitCipher;
 if(!q2||!shiftQuestion(q2))throw Error('No verified unit-aligned numerical cipher problem is available for this unit.');
 const q1=take(numeric)||take(q=>q.format==='multiple-choice');
 if(!q1)throw Error('This selection needs a numeric or multiple-choice lock question.');
 const first=numeric(q1)?{...stage(q1,0),type:'fields',title:'The '+RoomWord+' Lock',prompt:prompt(q1,true),fields:[{label:'Answer =',answer:numericValue(q1)}],button:'Open the door'}:choice(q1,0);
 const cipher={...stage(q2,1),type:'cipher',title:'The Cipher',
   prompt:prompt(q2,false),plain:theme?theme.cipher:'THE NEXT KEY IS BEHIND THE PLANETS',
   shift:numericValue(q2),answer:theme?theme.clue:'PLANETS',askLabel:theme?theme.ask:'Where is the next key?'};
 const q3=take(q=>q.format==='multiple-choice');if(!q3)throw Error('Choose more skills for the classification room.');const classify={...stage(q3,2),type:'classify',title:'The Answer Panels',prompt:prompt(q3,false),items:['Choose the correct panel.'],options:q3._graphOptions||q3.options.map(o=>source.html(o.text)),answer:[q3.options.findIndex(o=>o.correct)]};
 const q4=take(q=>orderedSteps(q)?.length>=4&&q.solutionSteps.length>=4)||
   take(q=>orderedSteps(q)?.length>=4&&q.solutionSteps.length>=3)||
   take(q=>orderedSteps(q)?.length>=4);
 if(!q4)throw Error('This unit and level need a multi-step problem for the sorting room. Select additional skills.');
 const sortedSteps=orderedSteps(q4);
 if(!sortedSteps||sortedSteps.length<4)throw Error('Sorting room requires at least four meaningful reasoning steps.');
 const order={...stage(q4,3),type:'order',title:'Put the Work in Order',
   prompt:prompt(q4,true),steps:sortedSteps.map(source.html)};
 const q5=take(q=>numeric(q)&&Number.isInteger(Number(q.answer))&&Number(q.answer)>=0&&Number(q.answer)<=9)||take(numeric)||take(q=>q.format==='multiple-choice');if(!q5)throw Error('Choose more skills for the final lock.');
 const last=numeric(q5)?{...stage(q5,4),type:'fields',ui:Number.isInteger(Number(q5.answer))&&Number(q5.answer)>=0&&Number(q5.answer)<=9?'dial':'fields',title:'The Final '+RoomWord,prompt:prompt(q5,true),fields:[{label:'Answer',answer:numericValue(q5)}],button:'Turn the handle'}:choice(q5,4);
 const story=theme?{title:theme.title,emoji:theme.introEmoji,endEmoji:theme.endEmoji,intro:theme.intro,word:theme.word,outro:theme.outro,
   finalStory:'The last door has a five-letter keypad. A note on it says: “Lay your key cards from the smallest stamp to the largest. The letters spell the password.”',finalAsk:'Password?'}:
   {title:source.unit.name+' Escape Room',intro:'The museum is locked for the night. Solve five gallery challenges, collect the key cards, and open the final door before the alarms reset.'};
 const room={...base,...story,id:source.courseId+'-'+source.unit.id,stages:[first,cipher,classify,order,last]};G.MK_ACTIVE_ESCAPE_ROOM=room;
 loadCSS('games/escape.css');const header=document.getElementById('activityHeader');header.innerHTML='<h1>'+source.unit.name+' Escape Room</h1><div id="dots"></div><div>Hints used: <b id="hu">0</b> &nbsp; <span id="clock">10:00</span></div>';
 const host=document.createElement('div');host.id='app';app.replaceWith(host);el('div',document.body).id='key';await script('games/escape-runtime.js');
}
G.TeacherSkills.choose(all,setup);
})(window).catch(e=>{document.getElementById('app').textContent='Unable to load activity: '+e.message});
