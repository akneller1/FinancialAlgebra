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
  var colors=palette.slice(0,qs.length),items=qs.map(function(q){return item(cfg.unitId,q);});
  return {kind:'color',grade1Color:true,levelNote:items.length<10?'This selection uses '+items.length+' questions and colors. Regions with the same problem number use the same color.':'',scene:scene,sceneName:sc.name,items:items,colorOf:colors,groupNum:sc.groups.map(function(g,i){return i%items.length+1;}),code:colors.map(function(c,i){return {color:c,hex:PR.SCENE_COLORS[c],num:i+1,answer:items[i].key};})};
 }
 function mazeOptions(cfg){return '<label class="field"><span class="lbl">Maze size</span><select id="prMazeSize">'+[['auto','Automatic · up to 8 problems'],['small','Small · 3 problems'],['medium','Medium · 8 problems'],['large','Large · 15 problems']].map(function(o){return '<option value="'+o[0]+'"'+((cfg.grade1MazeSize||'auto')===o[0]?' selected':'')+'>'+o[1]+'</option>';}).join('')+'</select></label>';}
 function maze(cfg,v){
  var needed={small:3,medium:8,large:15}[cfg.grade1MazeSize]||3,distinct=new Set(bank.select({courseId:'grade1',unitId:cfg.unitId.slice(7),level:cfg.level,formats:['short-answer','multiple-choice']}).filter(function(q){return cfg.skills[q.skillId];}).map(function(q){return key(q.answer);}));
  if(distinct.size<needed)return {error:'This maze size needs '+needed+' different answers; the selected '+N.courseLevelName(cfg.unitId,cfg.level)+' questions provide '+distinct.size+'. Choose Automatic or a smaller maze, add compatible skills, or use Problem & Answer Matching.'};
  var B;for(var retry=0;retry<3;retry++){
   B=PR.buildMaze(Object.assign({},cfg,{seed:String(cfg.seed)+(retry?'|retry'+retry:'')}),v);
   if(!B.error){B.grade1Maze=true;B.items.forEach(function(it){it.numberedRoom=true;});return B;}
  }
  return {error:B.error.replace(/Choose more skills[\s\S]*$/,'').trim()+' Questions stay at '+N.courseLevelName(cfg.unitId,cfg.level)+'. Choose Automatic or a smaller maze, add compatible skills, or use Problem & Answer Matching.'};
 }
 function whoQuestions(cfg){
  var seen=new Set();return bank.select({courseId:'grade1',unitId:cfg.unitId.slice(7),level:cfg.level,formats:['multiple-choice']}).filter(function(q){
   if(!cfg.skills[q.skillId]||Number(q.id.slice(-3))>24)return false;
   var identity=plainPrompt(q)+'|'+(q.diagram&&q.diagram.spec.alt||''),opts=q.options||[];
   if(seen.has(identity)||opts.length!==4||opts.filter(function(o){return o.correct;}).length!==1||new Set(opts.map(function(o){return key(o.text);})).size!==4||!opts.some(function(o){return o.correct&&key(o.text)===key(q.answer);}))return false;
   seen.add(identity);return true;
  });
 }
 function who(cfg,v){
  var qs=balanced(shuffled(whoQuestions(cfg),cfg.seed+'|who-source|'+v),10,function(q){return q.skillId;});
  if(qs.length<10)return {error:'This mystery needs 10 different multiple-choice questions; the selected '+N.courseLevelName(cfg.unitId,cfg.level)+' skills provide '+qs.length+'. Add compatible skills, or use Problem & Answer Matching.'};
  var items=qs.map(function(q){var it=item(cfg.unitId,q);it.wrong=q.options.filter(function(o){return !o.correct;}).map(function(o){return o.text;});return it;});
  var B=PR.buildWho(cfg,v,items);if(!B.error)B.grade1Who=true;return B;
 }
 function tri(up,i,j){return up?[[i,j],[i+1,j],[i,j+1]]:[[i+1,j],[i,j+1],[i+1,j+1]];}
 function triangle(side){var out=[];for(var j=0;j<side;j++)for(var i=0;i<side-j;i++){out.push(tri(true,i,j));if(i<side-j-1)out.push(tri(false,i,j));}return out;}
 function edgeKey(p,q){var a=p.join(','),b=q.join(',');return a<b?a+'|'+b:b+'|'+a;}
 function edgeMap(tris){var edges={};tris.forEach(function(t,i){[[0,1],[1,2],[2,0]].forEach(function(e,k){var id=edgeKey(t[e[0]],t[e[1]]);(edges[id]||(edges[id]=[])).push({piece:i,side:k});});});return edges;}
 function tarsiaDefinitions(){
  return [{id:'starter',shape:'trapezoid',tris:triangle(2).slice(0,3)}, {id:'small',shape:'triangle',tris:triangle(2)}, {id:'medium',shape:'triangle',tris:triangle(3)}, {id:'large',shape:'triangle',tris:triangle(4)}, {id:'full',shape:'hexagon',tris:PR.TARSIA_SHAPES.hexagon.tris()}].map(function(d){d.edges=edgeMap(d.tris);d.matches=Object.keys(d.edges).filter(function(k){return d.edges[k].length===2;});return d;});
 }
 function tarsia(cfg,v){
  var used=new Set(),qs=shuffled(selection(cfg),cfg.seed+'|tarsia|'+v).filter(function(q){var k=key(q.answer);if(used.has(k))return false;used.add(k);return true;});
  var defs=tarsiaDefinitions(),size=cfg.tarsiaSize||'auto',d;
  if(size==='auto')d=defs.filter(function(x){return x.tris.length<=9&&x.matches.length<=qs.length;}).pop();
  else d=defs.find(function(x){return x.id===size;});
  if(!d||d.matches.length>qs.length)return {error:'Tarsia needs '+(d?d.matches.length:2)+' different answers for this size; the selected '+N.courseLevelName(cfg.unitId,cfg.level)+' questions provide '+qs.length+'. Choose Automatic, add compatible skills, or use Stations.'};
  qs=balanced(qs,d.matches.length,function(q){return q.skillId;});
  var items=qs.map(function(q,i){var it=item(cfg.unitId,q);it.num=i+1;it.numberedEdge=true;return it;});
  var labels=new Set(items.map(function(it){return key(it.key);})),codes=shuffled(items.map(function(it,i){return i+1;}),cfg.seed+'|codes|'+v),answerBank=[];
  if(codes.length>1&&codes.every(function(x,i){return x===i+1;}))codes.push(codes.shift());
  items.forEach(function(it,i){
   if(it.key.length<=10)it.edgeAnswer=it.key;
   else{var n=codes[i],label='Code C'+n;while(labels.has(key(label))){n++;label='Code C'+n;}labels.add(key(label));it.edgeAnswer=label;answerBank.push({label:label,answer:it.key});}
  });
  var pieces=d.tris.map(function(t){return {pts:t.map(function(p){return p.slice();}),text:['','',''],kind:['','','']};}),placed=shuffled(items,cfg.seed+'|edges|'+v);
  d.matches.forEach(function(k,i){var pair=shuffled(d.edges[k],cfg.seed+'|side|'+v+'|'+i),it=placed[i];pieces[pair[0].piece].text[pair[0].side]='P'+it.num;pieces[pair[0].piece].kind[pair[0].side]='q';pieces[pair[1].piece].text[pair[1].side]=it.edgeAnswer;pieces[pair[1].piece].kind[pair[1].side]='a';it.edge=k;});
  var order=shuffled(pieces.map(function(p,i){return i;}),cfg.seed+'|pieces|'+v);if(order.every(function(x,i){return x===i;}))order.push(order.shift());
  var scrambled=order.map(function(pi,i){return {piece:pi,slot:i,turn:shuffled([0,1,2],cfg.seed+'|turn|'+v+'|'+i)[0]};});
  return {kind:'tarsia',grade1Tarsia:true,shape:d.shape,size:d.id,pieces:pieces,items:items,scrambled:scrambled,answerBank:answerBank,levelNote:pieces.length+' pieces and '+items.length+' matches at '+N.courseLevelName(cfg.unitId,cfg.level)+'. Blank edges form the outside; coded answers are listed in the answer bank.'};
 }
 function tarsiaOptions(cfg){return '<label class="field"><span class="lbl">Puzzle size</span><select id="prTarsiaSize">'+[['auto','Automatic · up to 9 pieces'],['starter','Starter · 3 pieces / 2 matches'],['small','Small · 4 pieces / 3 matches'],['medium','Medium · 9 pieces / 9 matches'],['large','Large · 16 pieces / 18 matches'],['full','Full · 24 pieces / 30 matches']].map(function(o){return '<option value="'+o[0]+'"'+((cfg.tarsiaSize||'auto')===o[0]?' selected':'')+'>'+o[1]+'</option>';}).join('')+'</select></label>';}
 var capable=PR.capable,build=PR.build;
 PR.MODES['answer-match']={prompt:500,answer:200,fig:true,wrong:0};
 PR.KINDS.push({id:'answer-match',name:'Problem & Answer Matching',blurb:'Solve each problem and write its answer letter. Letters may be used more than once.'});
 PR.capable=function(id,skill,kind,level){
  if(kind==='answer-match')return scoped(id)&&pool(id,level||'cp1').some(function(q){return q.skillId===skill;});
  if(scoped(id)&&kind==='who')return whoQuestions({unitId:id,level:level||'cp1',skills:{[skill]:true}}).length>=1;
  if(scoped(id)&&kind==='tarsia')return new Set(pool(id,level||'cp1').filter(function(q){return q.skillId===skill;}).map(function(q){return key(q.answer);})).size>=2;
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
  if(cfg.kind==='maze')return maze(cfg,v||0);
  if(cfg.kind==='who')return who(cfg,v||0);
  if(cfg.kind==='tarsia')return tarsia(cfg,v||0);
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
 function mazePages(cfg,B,v,nV,teacher,cover){
  var out=[cover];if(teacher)out.push(page('Maze · Route','<p>'+esc(N.skillSets[cfg.unitId].unitName)+' · '+esc(N.courseLevelName(cfg.unitId,cfg.level))+'</p><p>Start at the top left. Follow these numbered problems to the finish:</p><p style="font-size:22px;line-height:1.8">'+B.path.map(function(rc){var r=B.rooms.find(function(r){return r.r===rc[0]&&r.c===rc[1];});return r.finish?'FINISH':'Problem '+r.item.num;}).join(' → ')+'</p><p>The highlighted route is shown on the maze key. The following pages include solutions for every room, including dead ends.</p>'));
  return out.concat(workPages(cfg,B.items,'Maze · Numbered problems',teacher).map(function(p){return Object.assign({},p,{html:p.html.replace(/height:190px/g,'height:320px')});}));
 }
 function whoPages(cfg,B,v,nV,teacher){
  var S=B.S,letter=function(n){return 'ABCD'[n];},heading=S.name+' · '+N.courseLevelName(cfg.unitId,cfg.level),out=[];
  function clears(t){return t.p!==undefined?S.suspects[t.p].n+' and '+S.places[t.l].n:S.methods[t.m].n;}
  if(teacher)out.push(page('Mystery · Teacher guide','<p>'+esc(heading)+'</p><h2>Case solution</h2><p>'+esc(S.suspects[B.culprit.p].n)+' · '+esc(S.places[B.culprit.l].n)+' · '+esc(S.methods[B.culprit.m].n)+'</p><h2>Setup</h2><p>Use this as a teacher-led reading activity. Print the student case board and clue cards. Read each problem and answer clue aloud as needed. Students solve the math, choose an answer, then cross out only what that clue clears.</p><p>The ten correct clues leave exactly one suspect, one place, and one method. A wrong answer can remove the solution or leave extra possibilities; recheck the math together.</p>'));
  else out.push(page('Mystery · Case board','<p>'+esc(heading)+'</p><p>Name: ____________________</p><p>'+esc(S.intro.replace(/<[^>]*>/g,''))+'</p><p>Solve each clue card. Read the clue beside your answer. Cross out the people, places, or methods it clears. Write the card number beside each one. One of each will be left.</p><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">'+[['Suspects',S.suspects],['Places',S.places],['Methods',S.methods]].map(function(group){return '<section><h2 style="font-size:20px">'+group[0]+'</h2>'+group[1].map(function(x){return '<p style="font-size:16px;min-height:55px;overflow-wrap:anywhere">□ '+esc(x.n)+'<br>Card: _____</p>';}).join('')+'</section>';}).join('')+'</div><p>The person: ____________________</p><p>The place: ____________________</p><p>The method: ____________________</p>'));
  B.cards.forEach(function(c,i){out.push(page('Mystery · Clue card '+(i+1)+(teacher?' · Teacher key':''),'<p>'+esc(heading)+'</p>'+question(c.item)+'<div style="font-size:15px;line-height:1.4">'+c.opts.map(function(o,j){return '<section style="padding:9px 0;border-bottom:1px solid #aaa"><b>'+letter(j)+'. '+esc(o.a)+'</b><br>'+esc(o.clue)+'</section>';}).join('')+'</div>'+(teacher?'<p><b>Correct choice: '+letter(c.pos)+'</b> · Clears: '+esc(clears(c.truth))+'</p>'+solution(c.item):'<p>My choice: _____</p><div style="min-height:60px;border-bottom:1px solid #aaa">Show your thinking:</div>')));});
  return out;
 }
 function tarsiaPages(cfg,B,v,nV,teacher,covers){
  var bankPages=chunk(B.answerBank,4,function(list){return page('Tarsia · Answer bank','<p>Some triangle edges use a code instead of a long answer. Solve the question first, then find its answer here.</p>'+list.map(function(a){return '<div style="padding:14px;border-bottom:1px solid #aaa;overflow-wrap:anywhere"><b>'+esc(a.label)+':</b> '+esc(a.answer)+'</div>';}).join(''));});
  return covers.concat(bankPages,workPages(cfg,B.items,'Tarsia · Numbered problems',teacher,function(it){return '<p>Puzzle edge: '+(teacher?esc(it.edgeAnswer):'____________________')+'</p>';}));
 }
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
 G.MK_GRADE1_PRINTABLES={pages:pages,partner:partner,matching:matching,colorPages:colorPages,tarsiaPages:tarsiaPages,whoPages:whoPages,mazePages:mazePages,mazeOptions:mazeOptions,tarsiaOptions:tarsiaOptions,key:key};
})(window);
