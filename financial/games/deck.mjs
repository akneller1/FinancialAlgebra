// Adapter for the existing Classroom game engines. Never invent answer choices.
export const GAMES = [
 {id:'showdown',name:'Showdown',description:'Teams choose categories and point values in a financial review showdown.'},
 {id:'connect-four',name:'Connect 4',description:'Answer correctly to earn a disc. Includes the chance to steal.'},
 {id:'tic-tac-toe',name:'Tic-Tac-Toe',description:'Solve a financial question to claim a square for your team.'},
 {id:'picture-reveal',name:'Picture Reveal',description:'Uncover a mystery picture by answering financial questions.'},
 {id:'detective',name:'Detective',description:'Solve financial questions, collect evidence, and crack the case.'}
];
export function eligible(bank){
 const skills=new Set(bank.skills.map(s=>s.id));
 return bank.questions.filter(q=>q.gameEligible===true && q.format==='multiple-choice' && skills.has(q.skillId) &&
  Array.isArray(q.options) && q.options.length>=2 && q.options.length<=4 && q.options.filter(o=>o.correct===true).length===1 &&
  new Set(q.options.map(o=>String(o.text).trim().toLowerCase())).size===q.options.length);
}
export function createDeck(bank,rng){
 const pool=eligible(bank),seen=new Set();
 return function(slots){
  const used=new Set();
  return slots.flatMap(slot=>{
   const candidates=pool.filter(q=>q.skillId===slot.skill && !used.has(q.id));
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
