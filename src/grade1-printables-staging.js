/* Grade 1 development-only printable selection. Reuses unchanged authored items. */
(function(G){
 'use strict';
 var N=G.MKMENU,PR=N.printables,bank=G.MK_QUESTION_BANKS,cache={};
 var originalFigure=N.figHtml;
 if(originalFigure)N.figHtml=function(fig){var html=originalFigure.apply(this,arguments);return fig&&fig.kind==='authored-image'&&fig.src.includes('/math1/')?html.replace('max-height:280px','height:190px;max-height:190px'):html;};
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
 function stationWork(cfg,v){
  var selected=Object.keys(cfg.skills||{}).filter(function(s){return cfg.skills[s];});
  if(!selected.length)return {error:'Choose at least one skill.'};
  var n=Math.max(1,Math.min(cfg.stations||4,selected.length)),per=Math.max(4,Math.min(12,cfg.perStation||8)),stations=[];
  for(var i=0;i<n;i++){
   var group=selected.slice(Math.round(i*selected.length/n),Math.round((i+1)*selected.length/n));
   var qs=balanced(shuffled(selection(cfg).filter(function(q){return group.includes(q.skillId);}),cfg.seed+'|station|'+v+'|'+i),per,function(q){return q.skillId;});
   if(!qs.length)return {error:'No questions match the selected skills and level.'};
   stations.push({skills:group,title:group.map(function(id){return N.skillSets[cfg.unitId].byId[id].name;}).join('; '),items:qs.map(function(q){return item(cfg.unitId,q);})});
  }
  return {kind:'stations',grade1Staging:true,stations:stations,levelNote:stations.some(function(s){return s.items.length<per;})?'The selected skills provide '+stations.map(function(s){return s.items.length;}).join(', ')+' questions per station at this level.':''};
 }
 function errors(cfg,v){
  var qs=bank.select({courseId:'grade1',unitId:cfg.unitId.slice(7),level:cfg.level,formats:['short-answer']}).filter(function(q){return cfg.skills&&cfg.skills[q.skillId]&&/family: err_/.test(q.sourceNotes||'');});
  qs=balanced(shuffled(qs,cfg.seed+'|error|'+v),cfg.count||6,function(q){return q.skillId;});
  if(!qs.length)return {error:'No authored mistake-analysis questions match this selection.'};
  return {kind:'error',grade1Staging:true,levelNote:qs.length<(cfg.count||6)?'This selection contains '+qs.length+' authored mistake-analysis questions at this level.':'',cases:qs.map(function(q){return {item:item(cfg.unitId,q),authored:true,name:'',wrong:'',work:[]};})};
 }
 function coloring(cfg,v){
  var seen=new Set(),qs=shuffled(selection(cfg),cfg.seed+'|color|'+v).filter(function(q){var k=key(q.answer);if(String(q.answer).length>30||seen.has(k))return false;seen.add(k);return true;});
  var ids=Object.keys(PR.SCENES||{});if(!ids.length)return {error:'The coloring pictures are unavailable.'};
  var scene=cfg.picture&&PR.SCENES[cfg.picture]?cfg.picture:shuffled(ids,cfg.seed+'|scene|'+v)[0],sc=PR.SCENES[scene],palette=Array.from(new Set(sc.groups.map(function(g){return g.color;})));
  qs=balanced(qs,Math.min(10,palette.length),function(q){return q.skillId;});
  if(qs.length<2)return {error:'This coloring activity needs at least two different short answers at the selected level. Choose more skills, or use Problem & Answer Matching.'};
  var colors=shuffled(palette,cfg.seed+'|palette|'+v).slice(0,qs.length),items=qs.map(function(q){return item(cfg.unitId,q);});
  return {kind:'color',grade1Color:true,levelNote:items.length<10?'This selection uses '+items.length+' questions and colors. Regions with the same problem number use the same color.':'',scene:scene,sceneName:sc.name,items:items,colorOf:colors,groupNum:sc.groups.map(function(g,i){return i%items.length+1;}),code:colors.map(function(c,i){return {color:c,hex:PR.SCENE_COLORS[c],num:i+1,answer:items[i].key};})};
 }
 var capable=PR.capable,build=PR.build;
 PR.MODES['answer-match']={prompt:500,answer:200,fig:true,wrong:0};
 PR.KINDS.push({id:'answer-match',name:'Problem & Answer Matching',blurb:'Solve each problem and write its answer letter. Letters may be used more than once.'});
 PR.capable=function(id,skill,kind,level){
  if(kind==='answer-match')return scoped(id)&&pool(id,level||'cp1').some(function(q){return q.skillId===skill;});
  if(scoped(id)&&['stations','error','color'].includes(kind)){
   if(kind==='error')return bank.select({courseId:'grade1',unitId:id.slice(7),level:level||'cp1',skillIds:[skill],formats:['short-answer']}).some(function(q){return /family: err_/.test(q.sourceNotes||'');});
   var qs=pool(id,level||'cp1').filter(function(q){return q.skillId===skill;});
   return kind==='color'?new Set(qs.filter(function(q){return String(q.answer).length<=30;}).map(function(q){return key(q.answer);})).size>=2:qs.length>0;
  }
  if(scoped(id)&&kind==='partner')return pairs(id,pool(id,level||'cp1').filter(function(q){return q.skillId===skill;})).length>0;
  return capable.apply(this,arguments);
 };
 PR.build=function(cfg,v){
  if(!scoped(cfg.unitId))return build.apply(this,arguments);
  if(cfg.kind==='partner')return partner(cfg,v||0);
  if(cfg.kind==='answer-match')return matching(cfg,v||0);
  if(cfg.kind==='stations')return stationWork(cfg,v||0);
  if(cfg.kind==='error')return errors(cfg,v||0);
  if(cfg.kind==='color')return coloring(cfg,v||0);
  var native={maze:PR.buildMaze,tarsia:PR.buildTarsia,who:PR.buildWho}[cfg.kind];
  if(!native)return build.apply(this,arguments);
  var result;for(var retry=0;retry<3;retry++){
   result=native(Object.assign({},cfg,{seed:String(cfg.seed)+(retry?'|retry'+retry:'')}),v||0);if(!result.error)return result;
  }
  return {error:result.error.replace(/Choose more skills[\s\S]*$/,'').trim()+' Questions stay at '+N.courseLevelName(cfg.unitId,cfg.level)+'. Choose more compatible skills, or use Problem & Answer Matching.'};
 };
 function esc(t){return String(t).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
 function question(it){var p=it.p;return '<p style="white-space:pre-wrap;overflow-wrap:anywhere;font-size:17px;line-height:1.4;margin:8px 0">'+esc(p.prompt)+'</p>'+(p.fig?'<img src="../'+esc(p.fig.src)+'" alt="'+esc(p.fig.alt)+'" style="display:block;width:100%;height:190px;object-fit:contain;margin:10px auto">':'');}
 function solution(it){return '<div class="mm-ans" style="overflow-wrap:anywhere"><b>Answer:</b> '+esc(it.key)+'</div><ol style="margin:6px 0;padding-left:22px;font-size:15px;line-height:1.35">'+it.p.steps.map(function(s){return '<li>'+esc(s.t||s.m||'')+'</li>';}).join('')+'</ol>';}
 function page(title,body){return {nofoot:true,html:'<div class="mm-body pc g1-printable" style="font-family:Arial,sans-serif"><h1 style="font-size:25px">'+esc(title)+'</h1>'+body+'</div>'};}
 function chunk(items,n,fn){var out=[];for(var i=0;i<items.length;i+=n)out.push(fn(items.slice(i,i+n),i));return out;}
 function workPages(cfg,items,title,teacher,extra){
  var per=items.some(function(it){return it.p.fig||it.p.prompt.length>120;})?1:2;
  return chunk(items,per,function(list,start){return page(title+(teacher?' · Teacher key':''),'<p>'+esc(N.skillSets[cfg.unitId].unitName)+' · '+esc(N.courseLevelName(cfg.unitId,cfg.level))+'</p>'+list.map(function(it,i){return '<section><h2>Problem '+(start+i+1)+'</h2>'+question(it)+(teacher?solution(it)+(extra?extra(it,start+i):''):'<div style="min-height:'+(per===1?170:85)+'px;border-bottom:1px solid #999">Show your thinking:</div><p>Answer: ____________________</p>'+(extra?extra(it,start+i):''))+'</section>';}).join(''));});
 }
 function colorPages(cfg,B,v,nV,teacher,cover){return [cover].concat(workPages(cfg,B.items,'Color by Number · Problems',teacher,function(it,i){return '<p>Color: '+(teacher?esc(B.colorOf[i]):'____________________')+'</p>';}));}
 function pages(cfg,B,v,nV,teacher){
  var title=N.skillSets[cfg.unitId].unitName+' · '+N.courseLevelName(cfg.unitId,cfg.level)+' · Version '+String.fromCharCode(65+v),out=[];
  if(B.kind==='stations')return B.stations.reduce(function(out,s,i){return out.concat(workPages(cfg,s.items,'Station '+(i+1)+' · '+s.title,teacher));},[]);
  if(B.kind==='error')return workPages(cfg,B.cases.map(function(c){return c.item;}),'Error Analysis',teacher);
  if(B.kind==='partner'){
   var visual=B.rows.some(function(r){return r.A.p.fig||r.B.p.fig;}),long=B.rows.some(function(r){return r.A.p.prompt.length>100||r.B.p.prompt.length>100;});
   if(teacher){
    var keyPer=visual?1:long?2:3;
    return chunk(B.rows,keyPer,function(rows,i){return page('Partner Check · Teacher key','<p>'+esc(title)+'</p>'+rows.map(function(r,j){return '<section><h2 style="font-size:18px;margin:12px 0 6px">Pair '+(i+j+1)+'</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:24px"><section><h3 style="font-size:16px;margin:6px 0">Partner A</h3>'+question(r.A)+solution(r.A)+'</section><section><h3 style="font-size:16px;margin:6px 0">Partner B</h3>'+question(r.B)+solution(r.B)+'</section></div></section>';}).join(''));});
   }
   var per=visual||long?1:3;
   ['A','B'].forEach(function(who){out=out.concat(chunk(B.rows,per,function(rows,i){
    return page('Partner Check · Partner '+who,'<p>'+esc(title)+'</p><p>Name: ____________________ &nbsp; Partner: ____________________</p><p>Solve each problem. Compare answers with your partner. If they differ, find the mistake together.</p>'+rows.map(function(r,j){return '<section><h2>Pair '+(i+j+1)+'</h2>'+question(r[who])+'<div style="min-height:'+(per===1?150:55)+'px;border-bottom:1px solid #999">Show your thinking:</div><p>My answer: ____________________</p><p>Do our answers match? □ Yes □ No</p></section>';}).join(''));
   }));});return out;
  }
  var compactChoices=B.answers.every(function(a){return a.value.length<=60;})&&B.answers.reduce(function(n,a){return n+a.value.length;},0)<=200;
  var choices='<p>Write an answer letter for each problem. Letters may be used more than once.</p><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;border:1px solid #999;padding:12px">'+B.answers.map(function(a){return '<div style="overflow-wrap:anywhere"><b>'+a.letter+'.</b> '+esc(a.value)+'</div>';}).join('')+'</div>';
  if(!teacher&&!compactChoices)out=chunk(B.answers,4,function(answers,i){return page('Problem & Answer Matching · Answer bank','<p>'+esc(title)+'</p><p>Solve each numbered problem and write an answer letter. A letter may be used more than once.</p>'+answers.map(function(a){return '<div style="padding:18px;border-bottom:1px solid #bbb;white-space:pre-wrap;overflow-wrap:anywhere"><b>'+a.letter+'.</b> '+esc(a.value)+'</div>';}).join(''));});
  var per=B.items.some(function(it){return it.p.fig||it.p.prompt.length>140;})?1:2;
  return out.concat(chunk(B.items,per,function(items,i){return page('Problem & Answer Matching'+(teacher?' · Teacher key':''),'<p>'+esc(title)+'</p>'+(!teacher&&compactChoices?choices:'')+items.map(function(it,j){return '<section><h2>Problem '+(i+j+1)+'</h2>'+question(it)+(teacher?'<p><b>Answer letter: '+it.letter+'</b></p>'+solution(it):'<div style="min-height:'+(per===1?140:70)+'px;border-bottom:1px solid #999">Show your thinking:</div><p>Answer letter: __________</p>')+'</section>';}).join(''));}));

 }
 G.MK_GRADE1_PRINTABLES={pages:pages,partner:partner,matching:matching,colorPages:colorPages,key:key};
})(window);
