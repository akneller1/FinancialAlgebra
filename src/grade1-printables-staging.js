/* Grade 1 development-only printable selection. Reuses unchanged authored items. */
(function(G){
 'use strict';
 var N=G.MKMENU,PR=N.printables,bank=G.MK_QUESTION_BANKS,cache={};
 function scoped(id){return /^grade1-/.test(id||'');}
 function key(value){return String(value).trim().toLowerCase().replace(/−/g,'-').replace(/\s+/g,' ').replace(/\.$/,'');}
 function plainPrompt(q){return q.prompt.replace(/^(Find the answer\. |Work it out\. )/,'').replace(/ You may use counters or a drawing\.$/,'').replace(/\s+/g,' ').trim();}
 function shuffled(items,seed){
  var s=2166136261;String(seed).split('').forEach(function(c){s=Math.imul(s^c.charCodeAt(0),16777619)>>>0;});
  var out=items.slice();for(var i=out.length-1;i>0;i--){s^=s<<13;s^=s>>>17;s^=s<<5;var j=(s>>>0)%(i+1),t=out[i];out[i]=out[j];out[j]=t;}return out;
 }
 function pool(id,level){
  var token=id+'|'+level;if(cache[token])return cache[token];
  var unit=id.slice(7),seen=new Set();
  return cache[token]=bank.select({courseId:'grade1',unitId:unit,level:level,formats:['short-answer','multiple-choice']}).filter(function(q){
   if(Number(q.id.slice(-3))>24)return false;
   var identity=plainPrompt(q)+'|'+(q.diagram&&q.diagram.spec.alt||'');
   if(seen.has(identity))return false;seen.add(identity);return true;
  });
 }
 function selection(cfg){return pool(cfg.unitId,cfg.level).filter(function(q){return cfg.skills&&cfg.skills[q.skillId];});}
 function item(id,q){var p=N.grade1StagingQuestion(id,q.id);if(!p||p.failed)throw Error('Grade 1 source question unavailable: '+q.id);return {p:p,key:String(q.answer),skill:q.skillId,c:p.c,tag:q.skillId,wrong:[]};}
 function signature(q){return G.MK_GRADE1_STAGING.content[q.id];}
 function pairs(id,questions){
  var groups={};questions.forEach(function(q){var k=q.skillId+'|'+key(q.answer);(groups[k]||(groups[k]=[])).push(q);});
  var out=[];
  Object.keys(groups).forEach(function(k){var qs=groups[k];for(var i=0;i<qs.length;i++){
   var other=qs.slice(i+1).find(function(q){return signature(q)!==signature(qs[i])&&plainPrompt(q)!==plainPrompt(qs[i]);});
   if(other){out.push({A:item(id,qs[i]),B:item(id,other),same:true,pairId:qs[i].id+'|'+other.id});break;}
  }});return out;
 }
 function balanced(list,want,skillOf){var groups={},out=[];list.forEach(function(x){var s=skillOf(x);(groups[s]||(groups[s]=[])).push(x);});
  while(out.length<want&&Object.keys(groups).some(function(s){return groups[s].length;}))Object.keys(groups).forEach(function(s){if(out.length<want&&groups[s].length)out.push(groups[s].shift());});return out;
 }
 function partner(cfg,v){
  var list=shuffled(pairs(cfg.unitId,selection(cfg)),String(cfg.seed)+'|partner|'+v),used=new Set();
  list=list.filter(function(p){var k=key(p.A.key);if(used.has(k))return false;used.add(k);return true;});
  var want=Math.max(1,Math.min(12,cfg.count||8)),rows=balanced(list,want,function(p){return p.A.skill;});
  if(!rows.length)return {error:'The selected skill and level do not contain two different problems with the same answer. Choose another skill or use Problem & Answer Matching.'};
  return {kind:'partner',grade1Staging:true,rows:rows,levelNote:rows.length<want?'This selection has '+rows.length+' different partner pairs at the selected level.':''};
 }
 function matching(cfg,v){
  var qs=balanced(shuffled(selection(cfg),String(cfg.seed)+'|match|'+v),Math.max(1,Math.min(12,cfg.count||8)),function(q){return q.skillId;});
  if(!qs.length)return {error:'Choose at least one available skill.'};
  var values=new Map();qs.forEach(function(q){if(!values.has(key(q.answer)))values.set(key(q.answer),String(q.answer));});
  var answers=shuffled(Array.from(values.values()),String(cfg.seed)+'|answers|'+v).map(function(a,i){return {letter:String.fromCharCode(65+i),value:a};});
  return {kind:'answer-match',grade1Staging:true,items:qs.map(function(q){var it=item(cfg.unitId,q);it.letter=answers.find(function(a){return key(a.value)===key(q.answer);}).letter;return it;}),answers:answers};
 }
 var capable=PR.capable,build=PR.build;
 PR.MODES['answer-match']={prompt:500,answer:200,fig:true,wrong:0};
 PR.KINDS.push({id:'answer-match',name:'Problem & Answer Matching',blurb:'Solve each problem and write its answer letter. Letters may be used more than once.'});
 PR.capable=function(id,skill,kind,level){
  if(kind==='answer-match')return scoped(id)&&pool(id,level||'cp1').some(function(q){return q.skillId===skill;});
  if(scoped(id)&&kind==='partner')return pairs(id,pool(id,level||'cp1').filter(function(q){return q.skillId===skill;})).length>0;
  return capable.apply(this,arguments);
 };
 PR.build=function(cfg,v){
  if(!scoped(cfg.unitId))return build.apply(this,arguments);
  if(cfg.kind==='partner')return partner(cfg,v||0);
  if(cfg.kind==='answer-match')return matching(cfg,v||0);
  return build.apply(this,arguments);
 };
 function esc(t){return String(t).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
 function question(it){var p=it.p;return '<p style="white-space:pre-wrap;overflow-wrap:anywhere;font-size:17px;line-height:1.4">'+esc(p.prompt)+'</p>'+(p.fig?'<img src="../'+esc(p.fig.src)+'" alt="'+esc(p.fig.alt)+'" style="display:block;width:100%;height:190px;object-fit:contain;margin:10px auto">':'');}
 function solution(it){return '<div class="mm-ans" style="overflow-wrap:anywhere"><b>Answer:</b> '+esc(it.key)+'</div><ol>'+it.p.steps.map(function(s){return '<li>'+esc(s.t||s.m||'')+'</li>';}).join('')+'</ol>';}
 function page(title,body){return {nofoot:true,html:'<div class="mm-body pc g1-printable" style="font-family:Arial,sans-serif"><h1 style="font-size:25px">'+esc(title)+'</h1>'+body+'</div>'};}
 function chunk(items,n,fn){var out=[];for(var i=0;i<items.length;i+=n)out.push(fn(items.slice(i,i+n),i));return out;}
 function pages(cfg,B,v,nV,teacher){
  var title=N.skillSets[cfg.unitId].unitName+' · '+N.courseLevelName(cfg.unitId,cfg.level)+' · Version '+String.fromCharCode(65+v),out=[];
  if(B.kind==='partner'){
   if(teacher)return chunk(B.rows,1,function(rows,i){var r=rows[0];return page('Partner Check · Teacher key', '<p>'+esc(title)+'</p><h2>Pair '+(i+1)+'</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:24px"><section><h3>Partner A</h3>'+question(r.A)+solution(r.A)+'</section><section><h3>Partner B</h3>'+question(r.B)+solution(r.B)+'</section></div>');});
   var per=B.rows.some(function(r){return r.A.p.fig||r.B.p.fig||r.A.p.prompt.length>140||r.B.p.prompt.length>140;})?1:2;
   ['A','B'].forEach(function(who){out=out.concat(chunk(B.rows,per,function(rows,i){
    return page('Partner Check · Partner '+who,'<p>'+esc(title)+'</p><p>Name: ____________________ &nbsp; Partner: ____________________</p><p>Solve each problem. Compare answers with your partner. If they differ, find the mistake together.</p>'+rows.map(function(r,j){return '<section><h2>Pair '+(i+j+1)+'</h2>'+question(r[who])+'<div style="min-height:'+(per===1?150:70)+'px;border-bottom:1px solid #999">Show your thinking:</div><p>My answer: ____________________</p><p>Do our answers match? □ Yes □ No</p></section>';}).join(''));
   }));});return out;
  }
  if(!teacher)out=chunk(B.answers,4,function(answers,i){return page('Problem & Answer Matching · Answer bank','<p>'+esc(title)+'</p><p>Solve each numbered problem and write an answer letter. A letter may be used more than once.</p>'+answers.map(function(a){return '<div style="padding:18px;border-bottom:1px solid #bbb;white-space:pre-wrap;overflow-wrap:anywhere"><b>'+a.letter+'.</b> '+esc(a.value)+'</div>';}).join(''));});
  var per=B.items.some(function(it){return it.p.fig||it.p.prompt.length>140;})?1:2;
  return out.concat(chunk(B.items,per,function(items,i){return page('Problem & Answer Matching'+(teacher?' · Teacher key':''),'<p>'+esc(title)+'</p>'+items.map(function(it,j){return '<section><h2>Problem '+(i+j+1)+'</h2>'+question(it)+(teacher?'<p><b>Answer letter: '+it.letter+'</b></p>'+solution(it):'<div style="min-height:'+(per===1?140:70)+'px;border-bottom:1px solid #999">Show your thinking:</div><p>Answer letter: __________</p>')+'</section>';}).join(''));}));

 }
 G.MK_GRADE1_PRINTABLES={pages:pages,partner:partner,matching:matching,key:key};
})(window);
