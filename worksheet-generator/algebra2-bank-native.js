/* Reuse authored Algebra 2 items in existing players. No question, diagram,
 * distractor, or worked solution is generated here. Source keys are not
 * independently verified mathematics. */
(function(G){'use strict';
const NS=G.MKMENU, GB=G.MKGAMES;
if(!NS||!GB||!G.MK_BANK_LOADER)return;
const prefix='algebra2-', registry=new Map(),isBank=id=>registry.has(id);
const raw=new Map();
NS.courseLevelName=function(id,level){return /^(prealgebra(?:7)?|math[56])-/.test(id)?{cp2:'Remedial',cp1:'Standard',honors:'Advanced'}[level]:(NS.LEVELS[level]||NS.LEVELS.cp1).long;};
function level(c,policy){return policy&&['cp2','cp1','honors'].includes(policy.level)?policy.level:c<=2?'cp2':c<=5?'cp1':'honors'}
function tarsiaEligible(q){return ['short-answer','multiple-choice'].includes(q.format)&&typeof q.answer==='string'&&q.answer.trim().length>0&&q.answer.length<=20&&typeof q.prompt==='string'&&q.prompt.length<=110&&!/[\r\n]|<table|\\begin\{(?:array|matrix)/i.test(q.prompt)&&!q.diagram&&!(q.parts||[]).length}
NS.tarsiaEligible=tarsiaEligible;
function pool(id,skill,c,policy,formats){return G.MK_QUESTION_BANKS.select({courseId:registry.get(id).courseId,unitId:registry.get(id).unitId,skillIds:[skill],level:policy?.level==='mixed'?undefined:level(c,policy),formats:formats||['short-answer','multiple-choice','select-all','open-response']}).filter(q=>(!policy?.authoredErrorAnalysis || /family: [^)]*_error\)/.test(q.sourceNotes||''))&&(!policy?.authoredTarsia||tarsiaEligible(q)))}

function text(a){return typeof a==='object'?JSON.stringify(a):String(a)}
function figure(q){return q.diagram?.type==='image'?{kind:'authored-image',src:q.diagram.spec.src,alt:q.diagram.spec.alt}:null}
function problem(q,id,c){const parts=Array.isArray(q.parts)&&q.parts.length?q.parts.map((part,i)=>({answer:text(part.answer),prompt:part.prompt||'',label:String.fromCharCode(97+i)})):[{answer:text(Array.isArray(q.answer)?q.answer.join('; '):q.answer),prompt:''}];return {uid:q.id,sourceId:q.id,source:'authored-bank',authoredFormat:q.format,authoredErrorAnalysis:/family: [^)]*_error\)/.test(q.sourceNotes||''),authoredOptions:q.options||[],approved:true,skill:q.skillId,c,tag:q.skillId,prompt:q.prompt,fig:figure(q),parts,steps:(q.solutionSteps||[]).map(t=>({t})),key:q.id,sig:q.id,verify:{status:'source-key',issues:[]}}}
// Match only the author's explicit A/B pair IDs; coincidentally equal answers are not a pair.
NS.authoredPartnerPairs=function(id,skills,lv){
 if(!isBank(id))return [];
 const rec=registry.get(id), groups=new Map();
 for(const q of G.MK_QUESTION_BANKS.select({courseId:rec.courseId,unitId:rec.unitId,skillIds:skills,level:lv==='mixed'?undefined:lv,formats:['short-answer']})){
  const m=/Partner Check pair (\S+) \((A|B)\)/.exec(q.sourceNotes||'');if(!m)continue;
  if(!groups.has(m[1]))groups.set(m[1],{});groups.get(m[1])[m[2]]=q;
 }
 const out=[];
 for(const [pairId,g] of groups){
  if(!g.A||!g.B||g.A.skillId!==g.B.skillId||g.A.level!==g.B.level||g.A.answer!==g.B.answer||g.A.prompt===g.B.prompt)continue;
  const c=(NS.LEVELS[g.A.level]||NS.LEVELS.cp1).tiers[1];
  const make=q=>{const p=problem(q,id,c);p.prompt=p.prompt.replace(/^Partner [AB]\.\s*/,'');return {p,key:p.parts[0].answer,skill:q.skillId,c,tag:q.skillId,wrong:[]}};
  out.push({A:make(g.A),B:make(g.B),same:true,pairId});
 }
 return out;
};
function choose(items,seed,used){const rng=G.MKWS.rng.make(G.MKWS.rng.hash(String(seed)));return rng.shuffle(items).find(q=>!used?.keys?.has(q.id))}
/* Easy → Medium → Harder inside one class level. Authored items carry no difficulty number, so each is scored by
   the number of solution steps, parts and prompt length (open response a little higher).
   The level's items are split into thirds by that score and c picks the third: the level's lowest tier → the easiest
   third, its highest → the hardest. If that third is used up the nearest third is used; with policy.adjacentLevels
   (the lesson planner) a neighbouring level is tried before the slot is reported empty. */
const FORM_SCORE={'open-response':1.5};   // the form barely counts, so easy slots do not use up the few items of one form
function itemScore(q){return (FORM_SCORE[q.format]||0)+0.45*(q.solutionSteps||[]).length+0.8*((q.parts||[]).length)+Math.min(2,String(q.prompt||'').length/160)+(q.diagram?0.3:0)}
function third(c,lv){const t=(NS.LEVELS[lv]||NS.LEVELS.cp1).tiers;return c<=t[0]?0:c>=t[2]?2:1}
function chooseGraded(items,seed,used,c,lv){
 const rng=G.MKWS.rng.make(G.MKWS.rng.hash(String(seed))), sorted=items.slice().sort((a,b)=>itemScore(a)-itemScore(b)||(a.id<b.id?-1:1));
 const n=sorted.length, cut=[0,Math.round(n/3),Math.round(2*n/3),n], want=third(c,lv);
 for(const k of [0,1,2].sort((a,b)=>Math.abs(a-want)-Math.abs(b-want)||b-a)){
  const q=rng.shuffle(sorted.slice(cut[k],cut[k+1])).find(q=>!used?.keys?.has(q.id)); if(q)return q;
 }
 return null;
}
const generate=NS.generateProblem;
NS.generateProblem=function(id,skill,c,policy,seed,used){
 if(!isBank(id))return generate.apply(this,arguments);
 const lv=level(c,policy);
 // formal tests and choice menus keep the original random draw from the level (their slots already ramp by tier)
 let q=policy?.questionPool==='formal'?choose(pool(id,skill,c,policy,policy?.authoredFormats),seed,used):chooseGraded(pool(id,skill,c,policy,policy?.authoredFormats),seed,used,c,lv);
 // The banks hold few CP2 and Honors questions per skill and form. Rather than leave a slot empty, the generators
 // (worksheets, tests, menus, the planner) take an unused question from the nearest level and say so on the item.
 // Games call GB.makeItems / GB.buildDeck instead and keep each level exact. policy.adjacentLevels === false turns this off.
 let from=null;
 if(!q&&policy?.adjacentLevels!==false&&policy?.level!=='mixed'){
  const order={cp2:['cp1','honors'],cp1:third(c,lv)===2?['honors','cp2']:['cp2','honors'],honors:['cp1','cp2']}[lv]||[];
  for(const alt of order){q=choose(pool(id,skill,c,Object.assign({},policy,{level:alt}),policy?.authoredFormats),seed,used);if(q){from=alt;break}}
 }
 if(!q)return {failed:true,reason:'No unused authored questions match these skills and difficulty.'};
 used?.keys?.add(q.id);used?.sigs?.add(q.id);
 const out=problem(q,id,c);
 if(from){out.bankLevel=from;out.verify.issues=['From the '+NS.courseLevelName(id,from)+' bank: no unused '+NS.courseLevelName(id,lv)+' question of this kind is left.']}
 return out;
};
const distractors=GB.distractors, answerOk=GB.answerOk, makeItems=GB.makeItems, has=GB.hasGameItems, deck=GB.buildDeck;
GB.distractors=function(p,k,rng,n){if(p.source!=='authored-bank')return distractors.apply(this,arguments);return (raw.get(p.sourceId)?.options||[]).filter(o=>!o.correct).map(o=>o.text).slice(0,n)};
GB.answerOk=function(p,k,answer){if(p.source!=='authored-bank')return answerOk.apply(this,arguments);return {ok:String(answer)===String(p.parts[k].answer),status:'source-key'}};
GB.hasGameItems=function(id,skill){return isBank(id)?pool(id,skill,4,{level:'cp1'},['multiple-choice','short-answer']).length>0:has.apply(this,arguments)};
function item(q,id,c){return {id:q.id,sourceId:q.id,p:problem(q,id,c),k:0,skill:q.skillId,skillName:NS.skillSets[id].byId[q.skillId].name,tag:q.skillId,tagName:NS.skillSets[id].byId[q.skillId].name,c,q:{prompt:q.prompt,fig:figure(q),ask:(q.format==='select-all'?'Select all that apply.\n':'')+(q.parts||[]).map((p,i)=>'('+String.fromCharCode(97+i)+') '+p.prompt).join('\n')},answer:text(q.answer),steps:q.solutionSteps.map(t=>({t})),options:(q.options||[]).map(o=>({a:o.text,ok:o.correct===true})),typed:null}}
GB.makeItems=function(id,skill,c,policy,seed,used){
 if(!isBank(id))return makeItems.apply(this,arguments);
 const q=choose(pool(id,skill,c,policy,policy?.authoredFormats),seed,used);if(!q)return [];
 used?.keys?.add(q.id);return [item(q,id,c)];
};
// Keep each selected difficulty exact. Native procedural decks otherwise retry
// nearby tiers, which would cross authored CP2/CP1/Honors boundaries.
GB.buildDeck=function(id,slots,opts,done){
 if(!isBank(id))return deck.apply(this,arguments);
 opts=opts||{};const used={keys:new Set()},out=[];
 for(const [i,slot] of slots.entries()){
  const game=G.document?.body.getAttribute('data-game');
  const formats=game==='showdown'?['short-answer','multiple-choice','select-all','open-response']:game==='flashcards'?['short-answer','multiple-choice']:['multiple-choice'];
  const seed=(opts.seed||Date.now())+'|'+i;
  const q=slot.level==='mixed'?(choose(pool(id,slot.skill,slot.c,null,formats),seed,used)||choose(pool(id,slot.skill,slot.c,{level:'mixed'},formats),seed,used)):choose(pool(id,slot.skill,slot.c,slot.level?{level:slot.level}:null,formats),seed,used);
  if(q){used.keys.add(q.id);const it=item(q,id,slot.c);it.slot=slot;out.push(it)}
 }
 if(opts.progress)opts.progress(slots.length,slots.length);done(out);
};

// Preserve the native menu/worksheet/lesson-planner workflows for Algebra 2 while
// drawing only from the approved bank and its authored answer keys.
const nativeFormats={open:'short-answer',mc:'multiple-choice',multi:'select-all',mcas:'open-response'};
function sourceQuestion(p){return p&&p.source==='authored-bank'?raw.get(p.sourceId):null}
// Teacher keys list each approved question's own standards tags (menu/standards.js).
NS.sourceStandards=function(p){const q=p&&p.sourceId?raw.get(p.sourceId):null;return q&&Array.isArray(q.standards)?q.standards.slice():[]};
function menuSource(p){return JSON.stringify([p.prompt||'',(p.parts||[]).map(function(x){return [x.prompt||'',x.answer||'']}),p.fig||null,p.work||null])}
// Only the exact unmodified source item may bypass manual teacher approval.
// An edited item has source='edited'; a teacher-created item has source='manual'.
NS.isUneditedAlgebra2BankQuestion=function(p){
 if(!p||p.source!=='authored-bank'||p.edited||p.manual||!p.sourceId)return false;
 const q=raw.get(p.sourceId);
 if(!q||!p.skill||p.skill!==q.skillId)return false;
 const original=problem(q,null,p.c);
 return menuSource(p)===menuSource(original);
};
const makeChoices=NS.makeChoices,makeMulti=NS.makeMultiSelect,makeMcas=NS.makeMcas;
NS.makeChoices=function(p){
 const q=sourceQuestion(p);if(!q)return makeChoices.apply(this,arguments);
 const opts=q.options||[],correct=opts.map((o,i)=>o.correct===true?i:-1).filter(i=>i>=0);
 if(q.format!=='multiple-choice'||correct.length!==1||opts.length<2)return {fail:'This approved question is not a single-answer multiple-choice item.'};
 return {opts:opts.map(o=>o.text),key:correct[0],src:menuSource(p)};
};
NS.makeMultiSelect=function(p){
 const q=sourceQuestion(p);if(!q)return makeMulti.apply(this,arguments);
 const opts=q.options||[],keys=opts.map((o,i)=>o.correct===true?i:-1).filter(i=>i>=0);
 if(q.format!=='select-all'||keys.length<2||opts.length<4)return {fail:'This approved question is not a select-all item.'};
 return {opts:opts.map(o=>o.text),keys,direction:'Select all that apply.',src:JSON.stringify([q.id,opts])};
};
NS.makeMcas=function(p){
 const q=sourceQuestion(p);if(!q)return makeMcas.apply(this,arguments);
 return q.format==='open-response'&&(q.parts||[]).length>=4?{parts:q.parts.length}:{fail:'This approved question does not have four or more connected parts.'};
};
function authoredAvailable(id,skill,level,format){
 const item=registry.get(id);if(!item)return false;
 return G.MK_QUESTION_BANKS.select({courseId:item.courseId,unitId:item.unitId,skillIds:[skill],level:level,formats:[format]}).length>0;
}
const multiUnit=NS.multiUnitSupported,multiCap=NS.multiCapable,mcCap=NS.mcCapable,mcasCap=NS.mcasCapable,skillFmt=NS.skillFormatOk;
NS.multiUnitSupported=function(id){return isBank(id)?NS.skillSets[id].skills.some(s=>authoredAvailable(id,s.id,'cp1','select-all')):multiUnit.apply(this,arguments)};
NS.multiCapable=function(id,skill,c){return isBank(id)?['cp2','cp1','honors'].some(level=>authoredAvailable(id,skill,level,'select-all')):multiCap.apply(this,arguments)};
NS.mcCapable=function(id,skill,c){return isBank(id)?['cp2','cp1','honors'].some(level=>authoredAvailable(id,skill,level,'multiple-choice')):mcCap.apply(this,arguments)};
NS.mcasCapable=function(id,skill,c){return isBank(id)?['cp2','cp1','honors'].some(level=>authoredAvailable(id,skill,level,'open-response')):mcasCap.apply(this,arguments)};
NS.skillFormatOk=function(id,skill,format,c){
 if(!isBank(id))return skillFmt.apply(this,arguments);
 const bankFormat={open:'short-answer',mc:'multiple-choice',multi:'select-all',mcas:'open-response'}[format]||'short-answer';
 return ['cp2','cp1','honors'].some(level=>authoredAvailable(id,skill,level,bankFormat));
};
NS.authoredFormatForMenu=function(id,sectionFormat){
 return isBank(id)?[nativeFormats[sectionFormat]||'short-answer']:null;
};

const figHtml=NS.figHtml;
NS.figHtml=function(fig){
 if(fig?.kind!=='authored-image')return figHtml.apply(this,arguments);
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 return '<img class="authored-bank-image" src="../'+esc(fig.src)+'" alt="'+esc(fig.alt)+'" style="display:block;max-width:100%;max-height:280px;object-fit:contain;margin:12px auto">';
};
var loadBanks=G.MK_APPROVED_RESOURCE_BANKS?G.MK_APPROVED_RESOURCE_BANKS.ready:G.MK_BANK_LOADER.loadFromSite('question-banks/manifest.json','../');
G.MK_ALGEBRA2_NATIVE_READY=loadBanks.then(function(){
 const course=G.LIBRARY.courses.find(c=>c.id==='algebra2');
 G.LIBRARY.courses.forEach(c=>{
  let group=NS.CATALOG.find(g=>g.course===c.name);if(!group){group={course:c.name,units:[]};NS.CATALOG.push(group)}
  if(c.id==='algebra2')group.units=c.units.map(u=>[c.id+'-'+u.id,u.name]);
  c.units.forEach(u=>{
   const id=(c.id==='algebra'?'algebra1-':c.id+'-')+u.id;
   if(!G.MK_QUESTION_BANKS.available(c.id,u.id))return;
   if(!group.units.some(item=>item[0]===id))group.units.push([id,u.name]);
   const records=G.MK_COURSE_CATALOG.getSkillRecords(c.id,u.id),tags={};records.forEach(s=>tags[s.name]=s.name);
   registry.set(id,{courseId:c.id,unitId:u.id});
   G.MK_QUESTION_BANKS.select({courseId:c.id,unitId:u.id}).forEach(q=>raw.set(q.id,q));
   const printableKinds=['maze','color','partner','who','stations','tarsia','error'];
   NS.registerSkillSet({id,unitName:u.name,courseName:c.name,authoredBank:true,title:u.name+' Activities',tags,gaps:[],skills:records.map(s=>({id:s.id,name:s.name,tag:s.name,blurb:'Questions selected from the approved '+c.name+' bank.',print:printableKinds,generate:function(){throw Error('Authored bank selection required')}}))});
  });
 });
 // Preserve original levels while selecting authored banks by exact level.
 if(G.document?.body.hasAttribute('data-algebra2-game')) { GB.LEVELS.cp2.tiers=[1,1,1];GB.LEVELS.cp1.tiers=[4,4,4];GB.LEVELS.honors.tiers=[6,6,6]; }
 return course;
});
G.MK_COURSE_BANKS_READY=G.MK_ALGEBRA2_NATIVE_READY;
})(window);

