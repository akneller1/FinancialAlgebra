// Adapter for the existing Classroom game engines. Never invent answer choices: see derivedOptions below.
export const GAMES = [
 {id:'showdown',name:'Showdown',description:'Teams choose categories and point values in a financial review showdown.'},
 {id:'connect-four',name:'Connect 4',description:'Answer correctly to earn a disc. Includes the chance to steal.'},
 {id:'tic-tac-toe',name:'Tic-Tac-Toe',description:'Solve a financial question to claim a square for your team.'},
 {id:'picture-reveal',name:'Picture Reveal',description:'Uncover a mystery picture by answering financial questions.'},
 {id:'detective',name:'Detective',description:'Solve financial questions, collect evidence, and crack the case.'}
];
/* Multiple-choice questions play as written. A numeric question (2026-11-17) plays with choices taken only from its
 * own work: values the worked steps reach on the way (a student who stops one step early) and numbers given in the
 * question (a student who copies one). Nothing is made up; a question that does not yield two such values stays out
 * of the games. Advanced questions may run a little longer than other game cards. */
const num=s=>Number(String(s).replace(/−/g,'-').replace(/[$,%\s]/g,''));
function fmt(v,unit,cents){const a=Math.abs(v),neg=v<0?'−':'';if(unit==='USD')return neg+'$'+a.toLocaleString('en-US',{minimumFractionDigits:cents||!Number.isInteger(a)?2:0,maximumFractionDigits:2});if(unit==='%')return (Math.round(v*100)/100)+'%';return String(Math.round(v*100)/100);}
export function derivedOptions(q){
 if(q.format!=='short-answer'||!q.numeric||String(q.answer).includes(';'))return null;
 const ans=q.numeric.value,unit=q.numeric.unit,tol=Math.max(q.numeric.tolerance||0.01,0.01);
 const re=unit==='%'?/(-?[\d,]*\.?\d+)%/g:unit==='USD'?/([−-]?\$[\d,]+(?:\.\d+)?)/g:/=\s*(-?[\d,]+(?:\.\d+)?)/g,seen=new Map();
 for(const t of [...(q.solutionSteps||[]),q.prompt])for(const m of String(t).matchAll(re)){const v=num(m[1]);if(Number.isFinite(v)&&v!==0&&Math.abs(v-ans)>tol*2)seen.set(v.toFixed(2),v);}
 const ds=[...seen.values()].sort((a,b)=>Math.abs(Math.log(Math.abs(a/ans)))-Math.abs(Math.log(Math.abs(b/ans)))).slice(0,3);
 if(ds.length<2)return null;
 const texts=new Set([String(q.answer)]),options=[{text:String(q.answer),correct:true}];
 const cents=/\.\d\d\b/.test(String(q.answer));   // one money style per card, like the questions
 for(const v of ds){const t=fmt(v,unit,cents);if(!texts.has(t)){texts.add(t);options.push({text:t,correct:false});}}
 return options.length>=3?options:null;
}
const fitsGame=q=>q.gameEligible===true||(q.level==='advanced'&&q.format!=='open-response'&&!q.scenario?.document&&String(q.prompt).length<450);
export function eligible(bank){
 const skills=new Set(bank.skills.map(s=>s.id));
 return bank.questions.map(q=>q.format==='multiple-choice'?q:(fitsGame(q)&&derivedOptions(q)?{...q,format:'multiple-choice',options:derivedOptions(q),derivedChoices:true}:null)).filter(q=>q&&fitsGame(q)&&q.format==='multiple-choice'&&skills.has(q.skillId)&&
  Array.isArray(q.options)&&q.options.length>=2&&q.options.length<=4&&q.options.filter(o=>o.correct===true).length===1&&
  new Set(q.options.map(o=>String(o.text).trim().toLowerCase())).size===q.options.length);
}
/* Levels (2026-11-17). Games use Classroom codes: cp2 Support, cp1 Standard, honors Advanced. A slot asks for a level by
 * slot.level (a code, or 'mixed' for a Showdown board that climbs Support → Advanced by row) or by difficulty tier slot.c
 * (1, 2, 3). A skill with no questions at that level falls back to its other levels so a board never has holes. */
export const LEVEL_OF={cp2:'support',cp1:'standard',honors:'advanced'};
const MIXED_ROWS=['cp2','cp2','cp1','honors','honors'],TIER=['cp2','cp1','honors'];
export function slotLevel(slot){
 if(slot.level==='mixed')return LEVEL_OF[MIXED_ROWS[Math.max(0,Math.min(4,slot.row||0))]];
 if(LEVEL_OF[slot.level])return LEVEL_OF[slot.level];
 if(slot.c)return LEVEL_OF[TIER[Math.max(0,Math.min(2,slot.c-1))]];
 return 'standard';
}
export function createDeck(bank,rng){
 const pool=eligible(bank),seen=new Set();
 return function(slots){
  const used=new Set();
  return slots.flatMap(slot=>{
   const want=slotLevel(slot),forSkill=pool.filter(q=>q.skillId===slot.skill && !used.has(q.id)),atLevel=forSkill.filter(q=>!q.level||q.level===want);
   const candidates=atLevel.length?atLevel:forSkill;
   let fresh=candidates.filter(q=>!seen.has(q.id));
   if(!fresh.length){candidates.forEach(q=>seen.delete(q.id));fresh=candidates;}
   if(!fresh.length)return [];
   const q=rng.shuffle(fresh)[0];used.add(q.id);seen.add(q.id);
   return [{...q,options:rng.shuffle(q.options.map(o=>({...o}))),slot:{...slot}}];
  });
 };
}
export function gameItem(q,render){
 return {id:q.id,sourceId:q.id,skill:q.skillId,slot:q.slot,
  q:{prompt:q.prompt,fig:q.scenario?render.scenario(q.scenario):null},
  answer:q.options.find(o=>o.correct).text,
  options:q.options.map(o=>({a:o.text,ok:o.correct===true})),
  steps:(q.solutionSteps||[]).map(t=>({t})),typed:null};
}
