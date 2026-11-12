/* Standalone student Study Guide; no handout generator controls. */
(async function(){
'use strict';
const R=window.FA_RENDER,$=id=>document.getElementById(id),p=new URLSearchParams(location.search),student=p.get('student')==='1';
let bank,index,items=[],results={};
const selected=()=>[...document.querySelectorAll('[data-skill]:checked')].map(x=>x.value);
function shuffle(list){const a=list.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function eligible(q){return q.format!=='open-response'&&(q.options?.length||(q.numeric&&!String(q.answer).includes(';')));}
async function load(unit){
 if(!index.units.some(u=>u.unitId===unit))unit=index.units[0].unitId;
 const r=await fetch('../banks/'+unit+'.json');if(!r.ok)throw Error();bank=await r.json();$('unit').value=unit;$('unitTitle').textContent=bank.unitName;
 let assigned;try{assigned=p.has('skills')?JSON.parse(p.get('skills')):null;if(assigned&&!Array.isArray(assigned))assigned=[];}catch{assigned=[];}
 $('skills').innerHTML='<legend>Skills</legend>'+bank.skills.map(s=>'<label style="display:block;margin:8px 0"><input type="checkbox" data-skill value="'+R.esc(s.id)+'"'+(!assigned||assigned.includes(s.id)?' checked':'')+'> '+R.esc(s.name)+'</label>').join('');
 $('questions').innerHTML='';$('review').hidden=true;$('shareResult').hidden=true;$('status').textContent='Choose skills and start a practice test.';
 if(student){$('teacherNav').hidden=true;$('setup').hidden=true;start();}
}
function start(ids=selected()){
 if(!ids.length){$('status').textContent='Select at least one skill, or ask your teacher for a new link.';return;}
 const pool=shuffle(bank.questions.filter(q=>ids.includes(q.skillId)&&eligible(q))),first=ids.map(id=>pool.find(q=>q.skillId===id)).filter(Boolean);
 items=shuffle(first.concat(pool.filter(q=>!first.includes(q))).slice(0,12));results={};
 if(!items.length){$('status').textContent='No practice questions available for these skills.';return;}
 $('questions').innerHTML=items.map((q,i)=>'<section class="fa-panel">'+R.question({...q,options:null},{n:i+1,showType:false})+'<div class="practice-choices">'+(q.options?q.options.map((o,j)=>'<label><input type="'+(q.format==='select-all'?'checkbox':'radio')+'" name="q'+i+'" value="'+j+'"> '+R.rich(o.text)+'</label>').join(''):'<label class="fa-field">Your answer'+(q.numeric.unit==='USD'?' ($)':q.numeric.unit==='%'?' (%)':'')+'<input id="answer'+i+'" inputmode="decimal"></label>')+'</div><button class="fa-btn" data-check="'+i+'">Check answer</button><div role="status" id="feedback'+i+'"></div></section>').join('');$('review').hidden=false;update();
}
function update(){
 $('status').textContent=Object.values(results).filter(Boolean).length+' correct · '+Object.keys(results).length+' of '+items.length+' checked';
 $('skillScore').innerHTML=bank.skills.filter(s=>items.some(q=>q.skillId===s.id)).map(s=>{const ids=items.map((q,i)=>q.skillId===s.id?i:null).filter(i=>i!==null);return '<p><strong>'+R.esc(s.name)+':</strong> '+ids.filter(i=>results[i]).length+' correct out of '+ids.length+' ('+ids.filter(i=>i in results).length+' checked)</p>';}).join('');$('retry').disabled=!items.some((q,i)=>results[i]===false);
}
$('questions').onclick=e=>{
 const b=e.target.closest('[data-check]');if(!b)return;const i=+b.dataset.check,q=items[i],chosen=[...document.querySelectorAll('input[name="q'+i+'"]:checked')].map(x=>+x.value);
 if(q.options&&!chosen.length||!q.options&&!$('answer'+i).value.trim()){$('feedback'+i).textContent='Enter an answer first.';return;}
 if(q.options)results[i]=q.options.every((o,j)=>!!o.correct===chosen.includes(j));
 else{const s=$('answer'+i).value.trim().replace(/[−–]/g,'-').replace(/^(-?)\s*\$\s*/,'$1').replace(/%$/,'').trim();results[i]=/^[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?$/.test(s)&&Math.abs(Number(s.replace(/,/g,''))-q.numeric.value)<=(q.numeric.tolerance||0)+1e-9;}
 $('feedback'+i).innerHTML='<p class="fa-key"><strong>'+(results[i]?'Correct.':'Review this one.')+'</strong> '+R.rich(Array.isArray(q.answer)?q.answer.join('; '):q.answer)+'</p><ol>'+q.solutionSteps.map(s=>'<li>'+R.rich(s)+'</li>').join('')+'</ol>';b.disabled=true;b.closest('section').querySelectorAll('input').forEach(x=>x.disabled=true);update();
};
$('start').onclick=()=>start();$('retry').onclick=()=>start([...new Set(items.filter((q,i)=>results[i]===false).map(q=>q.skillId))]);$('unit').onchange=()=>load($('unit').value).catch(fail);
$('share').onclick=()=>{if(!selected().length){$('status').textContent='Select at least one skill.';return;}const url=new URL(location.href);url.search='';url.hash='';url.searchParams.set('unit',bank.unitId);url.searchParams.set('student','1');url.searchParams.set('skills',JSON.stringify(selected()));$('shareLink').value=url.href;$('shareResult').hidden=false;$('shareLink').select();};
$('copy').onclick=async()=>{try{await navigator.clipboard.writeText($('shareLink').value);$('status').textContent='Student link copied.';}catch{$('shareLink').focus();$('shareLink').select();}};
function fail(){$('status').textContent='Unable to load the practice test. Please reload and try again.';}
try{const r=await fetch('../banks/index.json');if(!r.ok)throw Error();index=await r.json();$('unit').innerHTML=index.units.map(u=>'<option value="'+R.esc(u.unitId)+'">'+R.esc(u.name)+'</option>').join('');await load(p.get('unit')||'income');}catch{fail();}
})();
