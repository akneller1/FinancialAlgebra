/* Interactive Practice Test — shares the menu generator's independently checked questions. */
(function(G){
'use strict';
var N=G.MKMENU, W=G.MKWS, root=document.getElementById('practice'), STORE='mk-readiness-auto-v3';
var state=null,config={unit:'algebra1-expressions-equations',level:'cp1',count:10,mode:'test',format:'mixed',minutes:0,skills:[]};
var STORE_PREFIX=STORE+':';
var esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
var fmt=s=>N.mathSafe(String(s||''));
var levels={cp2:2,cp1:4,honors:6};
function save(){try{localStorage.setItem(STORE_PREFIX+config.unit,JSON.stringify({state:state,config:config}));}catch(e){}if(state&&!state.done)updateProgress();}
function upgradeInequalityChoices(){
 if(!state||!Array.isArray(state.questions)||state.done||!N.inequalityChoices)return;
 state.questions.forEach(function(q){
   if(!q||q.kind!=='mc'||!q.problem)return;
   var v=N.inequalityChoices(q.problem);
   if(!v)return;
   if(q.choices&&q.choices.inequalityMode===v.inequalityMode&&
      q.choices.key===v.key&&JSON.stringify(q.choices.graphs||[])===JSON.stringify(v.graphs||[]))return;
   q.choices={opts:v.opts,key:v.key,graphs:v.graphs,prompt:v.prompt,inequalityMode:v.inequalityMode};
   q.response=null;q.checked=false;q.correct=null;
 });
}
function read(){try{var routeUnit=new URLSearchParams((G.location.hash||'').replace(/^#/,'' )).get('unit'),raw=routeUnit?localStorage.getItem(STORE_PREFIX+routeUnit):null,d=raw?JSON.parse(raw):null;if(!d){d=JSON.parse(localStorage.getItem(STORE)||'null');if(routeUnit&&d&&d.config&&d.config.unit!==routeUnit)d=null;}if(d&&d.config){config=d.config;state=d.state||null;upgradeInequalityChoices();}}catch(e){}}
function courseForUnit(unit){return N.CATALOG.filter(function(group){return group.units.some(function(u){return u[0]===unit;});})[0]||N.CATALOG[0];}
function units(){var group=courseForUnit(config.unit);return group.units.filter(function(u){return N.skillSets[u[0]];});}
function chosen(){return N.skillSets[config.unit];}
function skills(){return chosen().skills.filter(s=>config.skills.indexOf(s.id)!==-1);}
function studentURL(){
 var base=G.location.origin+G.location.pathname;
 var selected=config.skills&&config.skills.length?config.skills:chosen().skills.map(x=>x.id);
 var p=new URLSearchParams();
 [['unit',config.unit],['student','1'],['level',config.level],['count',config.count],['format',config.format],['minutes',config.minutes],['skills',selected.join(',')]].forEach(x=>p.set(x[0],String(x[1])));
 return base+'#'+p.toString();
}
function refreshStudentLink(){var el=root.querySelector('#pt-student-link');if(el)el.value=studentURL();}
function shareControls(){return '<div class="pt-share-tools"><button type="button" class="pt-secondary" id="pt-share">Copy student link</button><label class="pt-share-label">Student assessment link<input id="pt-student-link" aria-label="Student assessment link" readonly value="'+esc(studentURL())+'"></label><p class="pt-muted">Opens a fresh assessment with these unit, level, question, format, time and skill settings. Student results stay on their device.</p></div>';}
function copyStudentLink(){
 var url=studentURL(),field=root.querySelector('#pt-student-link'),button=root.querySelector('#pt-share');
 if(field)field.value=url;
 function label(t){if(button)button.textContent=t;}
 function fallback(){if(field){field.focus();field.select();try{if(G.document.execCommand&&G.document.execCommand('copy')){label('Copied!');return;}}catch(e){}}label('Select link to copy');}
 if(G.navigator.clipboard&&G.navigator.clipboard.writeText)G.navigator.clipboard.writeText(url).then(()=>label('Copied!')).catch(fallback);
 else fallback();
}
function bindShare(){var el=root.querySelector('#pt-share');if(el)el.onclick=copyStudentLink;}
function controls(){return '<section class="pt-card"><span class="pt-eyebrow">'+(/^math5-/.test(config.unit)?'GRADE 5 · UNDERSTANDING CHECK':'ASSESSMENT READINESS · VERSION 2')+'</span><h1>'+(/^math5-/.test(config.unit)?'Understanding Check':'Assessment Readiness Check')+'</h1><p>Take a unit-style assessment, review your performance by skill, and generate a targeted reassessment.</p><div class="pt-fields"><label>Unit<select id="pt-unit">'+units().map(u=>'<option value="'+esc(u[0])+'" '+(config.unit===u[0]?'selected':'')+'>'+esc(u[1])+'</option>').join('')+'</select></label><label>Level<select id="pt-level">'+['cp2','cp1','honors'].map(l=>'<option value="'+l+'" '+(config.level===l?'selected':'')+'>'+(/^prealgebra(?:7)?-|^math[56]-/.test(config.unit)?{cp2:'Remedial',cp1:'Standard',honors:'Advanced'}[l]:l.toUpperCase())+'</option>').join('')+'</select></label><label>Questions<select id="pt-count">'+[5,10,15,20,25].map(n=>'<option '+(config.count===n?'selected':'')+'>'+n+'</option>').join('')+'</select></label><label>Time limit<select id="pt-minutes">'+[0,20,30,45].map(n=>'<option value="'+n+'" '+(config.minutes===n?'selected':'')+'>'+(n?n+' minutes':'Untimed')+'</option>').join('')+'</select></label><label>Format<select id="pt-format">'+(chosen().authoredBank?'<option value="mixed" '+(config.format==='mixed'?'selected':'')+'>Mixed</option><option value="mc" '+(config.format==='mc'?'selected':'')+'>Multiple choice and select-all</option><option value="self" '+(config.format==='self'?'selected':'')+'>Written response (self-review)</option>':'<option value="mixed" '+(config.format==='mixed'?'selected':'')+'>Mixed</option><option value="mc" '+(config.format==='mc'?'selected':'')+'>Multiple choice</option><option value="self" '+(config.format==='self'?'selected':'')+'>Automatically graded short answer</option>')+'</select></label></div><h2>Choose skills</h2><div class="pt-skills">'+chosen().skills.map(s=>'<label><input type="checkbox" data-skill="'+esc(s.id)+'" '+(config.skills.includes(s.id)?'checked':'')+'> '+esc(s.name)+'</label>').join('')+'</div><div class="pt-actions"><button id="pt-all" class="pt-secondary">Select all</button><button id="pt-build">Generate printable assessment</button></div>'+shareControls()+'<p class="pt-muted">Results stay on this device. '+(chosen().authoredBank?'Approved bank questions are used. Multiple choice and select-all are graded from the bank key; written responses are self-reviewed against worked solutions.':'Every included question supports automatic grading; unsupported question formats are excluded.')+'</p></section>';}
function setup(){config.mode='test';if(state&&!state.done){root.innerHTML='<section class="pt-card"><h1>Assessment saved</h1><p>Your unfinished assessment is saved in this browser.</p><div class="pt-actions"><button id="pt-resume">Resume assessment</button><button id="pt-discard" class="pt-secondary">Discard and create new</button></div>'+shareControls()+'</section>';bindShare();root.querySelector('#pt-resume').onclick=show;root.querySelector('#pt-discard').onclick=()=>{if(confirm('Discard your saved assessment?')){state=null;save();setup();}};return;}if(!N.skillSets[config.unit])config.unit=units()[0][0];root.innerHTML=controls();root.querySelector('#pt-unit').onchange=function(e){config.unit=e.target.value;config.skills=chosen().skills.map(function(s){return s.id;});try{G.history.replaceState(null,'','#unit='+config.unit);}catch(err){}state=null;save();setup();};['level','count','format','minutes'].forEach(f=>root.querySelector('#pt-'+f).onchange=e=>{config[f]=(f==='count'||f==='minutes')?+e.target.value:e.target.value;save();refreshStudentLink();});root.querySelectorAll('[data-skill]').forEach(x=>x.onchange=()=>{config.skills=Array.from(root.querySelectorAll('[data-skill]:checked')).map(el=>el.dataset.skill);save();refreshStudentLink();});root.querySelector('#pt-all').onclick=()=>{config.skills=chosen().skills.map(s=>s.id);save();setup();};root.querySelector('#pt-build').onclick=()=>build();bindShare();}
/* Visual multiple choice for systems of linear inequalities.
   Draw distractors from the verified teacher graph, never from an unverified text description. */
function graphChoices(p){return N.inequalityChoices?N.inequalityChoices(p):null;}
function choiceMarkup(q,j){
 return q.choices&&q.choices.graphs&&N.figHtml
   ? '<span class="pt-graph-option">'+N.figHtml(q.choices.graphs[j])+'</span>'
   : fmt(q.choices.opts[j]);
}
function makeQuestion(skill,seed,index,used){
 var policy={level:config.level,intOnly:config.level!=='honors'}, tier=levels[config.level]+(index%3===0?-1:index%3===2?1:0);
 var p=N.generateProblem(config.unit,skill.id,Math.max(1,Math.min(7,tier)),policy,seed,used);
 if(p.failed)return null;
 var mode=config.format==='mc'?'mc':config.format==='self'?'self':index%2===0?'mc':'self';
 var choices=null;
 if(mode==='mc'){
   var made=N.makeChoices(p);
   if(!made.fail){if(made.derived)p=made.derived;choices={opts:made.opts,key:made.key,graphs:made.graphs,prompt:made.prompt};}
   else if(config.format==='mc')return null;
   else mode='self';
 }
 if(mode==='self'&&G.MKPRACTICE&&G.MKPRACTICE.supports(p))mode='auto';
 return {id:config.unit+'-'+seed+'-'+index,skill:skill.id,skillName:skill.name,problem:p,kind:mode,choices:choices,response:null,checked:false,correct:null,review:false};
}
function autoKind(p,choice){
 if(!p||p.failed||!p.parts||p.parts.length!==1)return null;
 var graph={problem:p,kind:'auto'};
 if(G.MKEXPGRAPH&&G.MKEXPGRAPH.target(graph))return 'auto';
 if(G.MKSYSTEM&&G.MKSYSTEM.target(graph))return 'auto';
 if(G.MKLINE&&G.MKLINE.target(graph))return 'auto';
 if(G.MKPARABOLA&&G.MKPARABOLA.target(graph))return 'auto';
 if(G.MKGRAPH&&(G.MKGRAPH.supports(graph)||G.MKGRAPH.pointTarget(graph)))return 'auto';
 if(choice&&choice.opts&&choice.opts.length===4&&Number.isInteger(choice.key)&&choice.key>=0&&choice.key<4)return 'mc';
 if(G.MKPRACTICE&&G.MKPRACTICE.supports(p))return 'auto';
 return null;
}
function bankProblem(q){
 var sourceAnswer=Array.isArray(q.answer)?q.answer.join('; '):q.answer;
 var parts=(q.parts&&q.parts.length?q.parts:[{answer:sourceAnswer,prompt:''}]).map(function(part,i){
   return {answer:typeof part.answer==='object'?JSON.stringify(part.answer):String(part.answer==null?'':part.answer),prompt:part.prompt||'',label:part.label||String.fromCharCode(97+i)};
 });
 return {uid:q.id,sourceId:q.id,source:'authored-bank',skill:q.skillId,tag:q.skillId,prompt:q.prompt,
   fig:q.diagram&&q.diagram.type==='image'?{kind:'authored-image',src:q.diagram.spec.src,alt:q.diagram.spec.alt}:null,
   parts:parts,steps:(q.solutionSteps||[]).map(function(t){return {t:t};})};
}
function buildAuthored(selected,overrides){
 var bank=G.MK_QUESTION_BANKS,courseId=config.unit.split('-')[0],unitId=config.unit.slice(courseId.length+1);
 var formats=config.format==='mc'?['multiple-choice','select-all']:config.format==='self'?['short-answer','open-response']:['multiple-choice','select-all','short-answer','open-response'];
 var pools=selected.map(function(skill){return bank.select({courseId:courseId,unitId:unitId,skillIds:[skill.id],level:config.level,formats:formats}).sort(function(){return Math.random()-0.5;});});
 var questions=[],requested=Math.max(5,Math.min(25,+config.count||10));
 while(questions.length<requested&&pools.some(function(pool){return pool.length;})){
   for(var i=0;i<pools.length&&questions.length<requested;i++){
     if(!pools[i].length)continue;
     var q=pools[i].shift(),kind=q.format==='multiple-choice'?'mc':q.format==='select-all'?'multi':'self';
     var options=(q.options||[]).map(function(o){return o.text;});
     var choices=kind==='mc'?{opts:options,key:(q.options||[]).findIndex(function(o){return o.correct===true;})}
       :kind==='multi'?{opts:options,keys:(q.options||[]).map(function(o,j){return o.correct===true?j:-1;}).filter(function(j){return j>=0;})}:null;
     var skill=chosen().byId[q.skillId],problem=bankProblem(q);
     questions.push({id:q.id,skill:q.skillId,skillName:skill?skill.name:q.skillId,problem:problem,kind:kind,choices:choices,response:null,checked:false,correct:null,review:false});
   }
 }
 var missing=selected.filter(function(skill){return !questions.some(function(q){return q.skill===skill.id;});}).map(function(skill){return skill.name;});
 if(!questions.length){alert('No approved questions match this unit, level, and format. Try a different level, format, or skill selection.');return;}
 if(questions.length<requested)alert('Only '+questions.length+' of '+requested+' requested approved questions are available for this unit, level, and format.');
 if(missing.length)console.warn('Assessment Readiness: selected Algebra 2 skills without matching approved questions:',missing);
 var previous=state&&state.done?state.questions.filter(function(q){return q.correct===true;}).length+'/'+state.questions.length:null;
 state={questions:questions,index:0,done:false,started:Date.now(),deadline:config.minutes?Date.now()+config.minutes*60000:null,mode:'test',previousScore:overrides&&overrides.length?previous:null,source:'authored-bank',paperView:true,autoGraded:questions.every(function(q){return q.kind==='mc'||q.kind==='multi';}),missingSkills:missing};
 save();show();
}
function build(overrides){
 config.mode='test';
 var selected=overrides&&overrides.length?chosen().skills.filter(x=>overrides.includes(x.id)):skills();
 if(!selected.length){alert('Select at least one skill.');return;}
 if(chosen().authoredBank){buildAuthored(selected,overrides);return;}
 var questions=[],candidates=[],seen=new Set(),skipped=0,requested=config.count;
 var excludedBySkill={};
 // Use the same verified teacher Assessment Generator, but accept ONLY fully gradeable questions.
 for(var attempt=0;attempt<7&&candidates.length<Math.max(requested*6,selected.length*5);attempt++){
   var ac=N.defaultConfig(config.unit,'test');
   ac.level=config.level;ac.seed=Math.floor(Math.random()*1e9);ac.versions=1;ac.questionPool='practice';ac.skills={};
   selected.forEach(x=>ac.skills[x.id]=true);
   var remaining=Math.max(requested,selected.length*3);
   var mcCount=config.format==='self'?0:config.format==='mc'?remaining*2:remaining;
   var openCount=config.format==='mc'?0:config.format==='self'?remaining*2:remaining;
   ac.sections=N.testSections('std');
   ac.sections[0].offered=ac.sections[0].required=mcCount;
   ac.sections[1].offered=ac.sections[1].required=openCount;
   ac.sections=ac.sections.filter(x=>x.offered>0);
   var generated=N.newAssessment(ac);
   generated.versions[0].sections.forEach(function(sec){
     sec.items.forEach(function(p){
       if(candidates.length>=Math.max(requested*6,selected.length*5))return;
       var fingerprint=[p.skill,p.variant||'',N.studentText(p).replace(/\s+/g,'')].join('|');
       if(p.failed||seen.has(fingerprint)){skipped++;return;}
       var choice=p.mc&&p.mc.opts&&p.mc.opts.length>=2?{opts:p.mc.opts,key:p.mc.key,graphs:p.mc.graphs,prompt:p.mc.prompt}:null;
       var graph={problem:p,kind:'auto'};
       if((G.MKEXPGRAPH&&G.MKEXPGRAPH.target(graph))||(G.MKSYSTEM&&G.MKSYSTEM.target(graph))||(G.MKLINE&&G.MKLINE.target(graph))||(G.MKPARABOLA&&G.MKPARABOLA.target(graph))||(G.MKGRAPH&&(G.MKGRAPH.supports(graph)||G.MKGRAPH.pointTarget(graph))))choice=null;
       var kind=autoKind(p,choice);
       if(choice && p.mc && p.mc.inequalityMode && N.inequalityChoices){
         var verifiedChoice=N.inequalityChoices(p);
         if(!verifiedChoice){skipped++;return;}
         choice={opts:verifiedChoice.opts,key:verifiedChoice.key,
                 graphs:verifiedChoice.graphs,prompt:verifiedChoice.prompt};
         kind='mc';
       }
       if(!kind){skipped++;excludedBySkill[p.skill]=(excludedBySkill[p.skill]||0)+1;return;}
       var sk=chosen().byId[p.skill];
       seen.add(fingerprint);
       candidates.push({id:p.uid,skill:p.skill,skillName:sk?sk.name:p.tag,problem:p,kind:kind,choices:kind==='mc'?choice:null,response:null,checked:false,correct:null,review:false});
     });
   });
 }
 // Round-robin across selected skills, preferring a different question template
 // before repeating one. This prevents a single high-yield skill from filling
 // the assessment while other selected skills never appear.
 var counts={},variants={};
 selected.forEach(function(sk){counts[sk.id]=0;variants[sk.id]={};});
 while(questions.length<requested&&candidates.length){
   var best=-1,bestScore=-Infinity;
   candidates.forEach(function(q,i){
     var variant=q.problem.variant||q.problem.tag||q.skill;
     var score=-(counts[q.skill]||0)*100-(variants[q.skill][variant]||0)*30;
     // Prefer questions that are not merely a different set of numbers in
     // the same skill/template, without compromising the verified answer.
     if(q.problem.fig)score+=2;
     if(score>bestScore){bestScore=score;best=i;}
   });
   if(best<0)break;
   var q=candidates.splice(best,1)[0],v=q.problem.variant||q.problem.tag||q.skill;
   counts[q.skill]=(counts[q.skill]||0)+1;
   variants[q.skill][v]=(variants[q.skill][v]||0)+1;
   questions.push(q);
 }
 var missing=selected.filter(function(sk){return !counts[sk.id];}).map(function(sk){return sk.name;});
 if(missing.length)console.warn('Assessment Readiness: selected skills without gradeable questions:',missing);
 if(skipped)console.warn('Assessment Readiness: excluded ungradeable or duplicate questions:',skipped,excludedBySkill);
 if(!questions.length){alert('No fully auto-gradable questions could be generated. Try a different skill selection or choose Multiple Choice.');return;}
 if(questions.length<requested)alert('Only '+questions.length+' of '+requested+' requested questions could be generated with reliable automatic grading. Unsupported questions were excluded; no self-graded questions were included.');
 var previous=state&&state.done?state.questions.filter(q=>q.correct===true).length+'/'+state.questions.length:null;
 state={questions:questions,index:0,done:false,started:Date.now(),deadline:config.minutes?Date.now()+config.minutes*60000:null,mode:'test',previousScore:overrides&&overrides.length?previous:null,source:'assessment-generator',paperView:true,autoGraded:true,unsupportedExcluded:skipped,missingSkills:missing};
 save();show();
}
function problemHTML(q){
 var p=q.problem,visual=q.choices&&q.choices.graphs;
 var prompt=(q.choices&&q.choices.prompt)||(p.mc&&p.mc.prompt)||p.prompt;
 return '<div class="pt-problem">'+fmt(prompt)
   +(p.fig&&N.figHtml&&!visual?N.figHtml(p.fig):'')
   +(p.parts||[]).map((part,i)=>part.prompt?'<div class="pt-part">'+(part.label?esc(part.label)+' ':'')+fmt(part.prompt)+'</div>':'').join('')+'</div>';
}
function solutionMath(value){
 var source=String(value==null?'':value).trim();
 if(!source)return '';
 if(source.indexOf('⟨')>=0)return fmt(source);
 // Use the site's own marked-math renderer, rather than relying on raw TeX as HTML.
 // If KaTeX is unavailable, preserve readable math instead of exposing commands.
 if(G.katex&&typeof G.katex.renderToString==='function'){
   try{return G.katex.renderToString(source,{throwOnError:false,output:'html',trust:false});}catch(e){}
 }
 var plain=source.replace(/\\cdot/g,' × ').replace(/\\times/g,' × ')
   .replace(/\\div/g,' ÷ ').replace(/\\pm/g,' ± ')
   .replace(/\^\{([^{}]*)\}/g,'^($1)')
   .replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g,'($1)/($2)');
 return esc(plain);
}
function diagnosticFeedback(q){
 if(q.correct!==false)return '';
 var tip='';
 if(G.MKLINE&&G.MKLINE.target(q)&&G.MKLINE.diagnose)tip=G.MKLINE.diagnose(q);
 else if(G.MKPARABOLA&&G.MKPARABOLA.target(q)&&G.MKPARABOLA.diagnose)tip=G.MKPARABOLA.diagnose(q);
 else if(G.MKEXPGRAPH&&G.MKEXPGRAPH.target(q))tip='Evaluate the function at each assigned x-value, remembering any vertical shift.';
 else if(G.MKSYSTEM&&G.MKSYSTEM.target(q))tip='Check the slope and intercept of both lines; the intersection must satisfy both equations.';
 else if(G.MKGRAPH&&G.MKGRAPH.supports(q))tip='Check the endpoints, open or closed circles, and which directions are shaded.';
 if(!tip)return '';
 return '<div class="pt-diagnostic"><strong>What to check:</strong> '+esc(tip)+'</div>';
}
function feedback(q){var p=q.problem,part=p.parts[0];var lines=(p.steps||[]).map(x=>'<li>'+(x.t?fmt(x.t):'')+(x.m?'<div class="pt-step-math">'+solutionMath(x.m)+'</div>':'')+'</li>').join('');return diagnosticFeedback(q)+'<div class="pt-explain"><strong>Answer:</strong> '+(p.parts||[]).map(x=>fmt(x.answer)).join(' · ')+(lines?'<h3>Worked solution</h3><ol>'+lines+'</ol>':'<p>Compare your process with the verified answer above.</p>')+(p.parts||[]).map(x=>x.answerFig&&N.figHtml?N.figHtml(x.answerFig):'').join('')+'</div>';}
function item(q,i){var answered=isAnswered(q),visible=state.done||state.mode==='practice'&&q.checked,choice=q.kind==='mc'||q.kind==='multi';var options=choice?'<div class="pt-options">'+q.choices.opts.map(function(v,j){var checked=q.kind==='multi'?Array.isArray(q.response)&&q.response.indexOf(j)>=0:+q.response===j&&answered;return '<label class="pt-option"><input type="'+(q.kind==='multi'?'checkbox':'radio')+'" name="pt-answer-'+i+'" value="'+j+'" '+(checked?'checked':'')+' '+(visible?'disabled':'')+'> '+choiceMarkup(q,j)+'</label>';}).join('')+'</div>':'<label class="pt-response">Show your work and enter your response<textarea id="pt-written" rows="4" '+(visible?'disabled':'')+' placeholder="Explain your solution...">'+esc(q.response||'')+'</textarea></label>';return '<section class="pt-card"><div class="pt-top"><span class="pt-eyebrow">'+esc(q.skillName)+'</span><strong>Question '+(i+1)+' of '+state.questions.length+'</strong></div>'+problemHTML(q)+options+(visible?'<div class="pt-status '+(q.correct===true?'pt-good':q.correct===false?'pt-bad':'')+'">'+(q.correct===true?'Correct':q.correct===false?'Needs review':'Compare your work')+'</div>'+feedback(q)+(q.kind==='self'&&q.correct===null?'<div class="pt-actions"><button data-grade="yes">My work is correct</button><button data-grade="no" class="pt-secondary">I need more practice</button></div>':''):'')+'</section>';}
function paperHTML(){
 if(!state)return '';
 var ABC='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
 return '<div class="pt-paper-head"><span>MR. K’S CLASSROOM · ASSESSMENT READINESS</span><h2>'+esc(chosen().unitName||'Algebra 1')+'</h2><p>Name: ______________________________ Date: ______________</p><p><strong>Directions:</strong> Show all work on separate paper. Read the test below or print/save it as a PDF. Enter only your final answers into the numbered answer sheet on this page. Do not include your work in the answer boxes.</p></div>'+
 state.questions.map(function(q,i){return '<section class="pt-paper-question"><div class="pt-paper-number">'+(i+1)+'.</div><div class="pt-paper-content">'+problemHTML(q)+((q.kind==='mc'||q.kind==='multi')?'<div class="pt-paper-choices">'+q.choices.opts.map((v,j)=>'<div>'+ABC[j]+'. '+choiceMarkup(q,j)+'</div>').join('')+'</div>':'')+'</div></section>';}).join('');
}
function isAnswered(q){return q.response!==null&&q.response!==undefined&&q.response!=='';}
function updateProgress(){
 if(!state||state.done||!root.querySelector('#pt-progress-count'))return;
 var answered=state.questions.filter(isAnswered).length,total=state.questions.length;
 root.querySelector('#pt-progress-count').textContent=answered+' of '+total+' answered';
 root.querySelector('#pt-progress-fill').style.width=(total?100*answered/total:0)+'%';
 var summary=root.querySelector('#pt-finish-summary');if(summary)summary.textContent=(total-answered)+' unanswered · '+state.questions.filter(q=>q.review).length+' marked for review. You can change answers until you submit.';
 root.querySelectorAll('[data-jump]').forEach(function(button){
   var q=state.questions[+button.dataset.jump];
   button.classList.toggle('answered',isAnswered(q));
   button.classList.toggle('flagged',!!q.review);
   button.setAttribute('aria-label','Question '+(+button.dataset.jump+1)+(isAnswered(q)?', answered':', unanswered')+(q.review?', marked for review':''));
 });
 root.querySelectorAll('[data-review-toggle]').forEach(function(button){
   var marked=!!state.questions[+button.dataset.reviewToggle].review;
   button.classList.toggle('pt-marked',marked);button.setAttribute('aria-pressed',String(marked));
   button.textContent=marked?'Marked for review':'Mark for review';
 });
}
function answerControl(q,i){
 var value=q.response===null?'':q.response;
 if(G.MKEXPGRAPH&&G.MKEXPGRAPH.target(q))return G.MKEXPGRAPH.render(q,i);
 if(G.MKSYSTEM&&G.MKSYSTEM.target(q))return G.MKSYSTEM.render(q,i);
 if(G.MKLINE&&G.MKLINE.target(q))return G.MKLINE.render(q,i);
 if(G.MKPARABOLA&&G.MKPARABOLA.target(q))return G.MKPARABOLA.render(q,i);
 if(G.MKGRAPH&&G.MKGRAPH.supports(q))return G.MKGRAPH.render(q,i);
 if(G.MKGRAPH&&G.MKGRAPH.pointTarget(q))return G.MKGRAPH.pointHTML(q,i);
 if(q.kind==='mc'||q.kind==='multi')return '<fieldset class="pt-mc-row pt-mc-inline" data-mc-question="'+i+'"><legend>'+(q.kind==='multi'?'Select all that apply':'Choose your answer')+'</legend><div class="pt-mc-buttons">'+q.choices.opts.map(function(opt,j){var selected=q.kind==='multi'?Array.isArray(q.response)&&q.response.indexOf(j)>=0:q.response===j;return '<button type="button" class="pt-mc-choice'+(selected?' selected':'')+'" data-'+(q.kind==='multi'?'multi':'mc')+'-answer="'+i+'" data-mc-choice="'+j+'" aria-pressed="'+(selected?'true':'false')+'"><span class="pt-choice-letter">'+('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[j]||String(j+1))+'</span><span class="pt-choice-text">'+choiceMarkup(q,j)+'</span></button>';}).join('')+'</div></fieldset>';
 if(q.kind==='self'&&q.problem.source==='authored-bank')return '<label class="pt-response">Show your work and enter your response<textarea data-authored-response="'+i+'" rows="5" placeholder="Explain your reasoning...">'+esc(value)+'</textarea></label><p class="pt-muted">After submitting, compare your work with the answer and worked solution, then rate your readiness.</p>';
 return '<div class="pt-math-response"><label class="pt-inline-answer" for="pt-answer-'+i+'">Final answer<input id="pt-answer-'+i+'" aria-label="Answer to question '+(i+1)+'" data-answer="'+i+'" autocomplete="off" inputmode="text" placeholder="Type or use the keypad" value="'+esc(value)+'"></label>'+
 '<div class="pt-live-preview"><div class="pt-preview-heading">Live math preview <span>Display only — not a correctness check</span></div><div class="pt-preview-content" data-preview="'+i+'" aria-label="Formatted preview of your answer"></div></div>'+ 
 '<div class="pt-math-pad" data-math-pad="'+i+'" role="group" aria-label="Math symbols for question '+(i+1)+'">'+[
 ['−','-'],['a/b','fraction'],['x²','square'],['xⁿ','power'],['√','sqrt'],['Next','next'],['≤','<='],['≥','>='],['=','='],['(', '('],[')',')'],['+','+'],['⌫','backspace']
 ].map(function(k){return '<button type="button" data-math-insert="'+esc(k[1])+'" aria-label="'+esc(k[0]==='⌫'?'Delete previous character':'Insert '+k[0])+'">'+k[0]+'</button>';}).join('')+'</div>'+
 '<p class="pt-muted pt-pad-hint">Tap a/b, √ or xⁿ to insert an editable template. Selected digits are placeholders; type to replace them, then use Next to jump to a denominator. Type numbers and variables normally; the grader accepts supported answer formats.</p></div>';
}
function assessmentHTML(){
 return '<div class="pt-student-intro"><strong>Directions:</strong> Do your work on paper, then enter or select your answer directly below each question. Use Print / Save PDF for a paper copy.</div>'+
 state.questions.map(function(q,i){return '<section class="pt-card pt-student-question" id="pt-question-'+(i+1)+'" aria-labelledby="pt-q-label-'+i+'">'+
 '<div class="pt-student-qhead"><span id="pt-q-label-'+i+'">Question '+(i+1)+' of '+state.questions.length+'</span><span class="pt-qskill">'+esc(q.skillName)+'</span></div>'+
 problemHTML(q)+'<div class="pt-inline-control">'+answerControl(q,i)+'</div>'+
 '<div class="pt-question-footer"><button type="button" class="pt-review-toggle" data-review-toggle="'+i+'" aria-pressed="'+(q.review?'true':'false')+'">'+(q.review?'Marked for review':'Mark for review')+'</button><span class="pt-saved-label">Autosaved on this device</span></div></section>';}).join('');
}
function printPaper(){
 var holder=G.document.createElement('div');holder.className='pt-print-standalone';holder.innerHTML=paperHTML();G.document.body.appendChild(holder);G.document.body.classList.add('pt-printing-paper');
 var clean=function(){G.document.body.classList.remove('pt-printing-paper');holder.remove();G.removeEventListener('afterprint',clean);};
 G.addEventListener('afterprint',clean);G.print();
}
function tickTimer(){
 if(!state||state.done||!state.deadline)return;
 var remain=Math.max(0,state.deadline-Date.now()),el=root.querySelector('#pt-timer');
 if(el)el.textContent='Time remaining: '+Math.floor(remain/60000)+':'+String(Math.floor(remain/1000)%60).padStart(2,'0');
 if(remain===0)submit(true);
}
var timerHandle=G.setInterval(tickTimer,1000);
function show(){
 if(!state){setup();return;}
 if(state.done){results();return;}
 if(state.deadline&&Date.now()>=state.deadline){submit(true);return;}
 state.mode='test';
 root.innerHTML='<header class="pt-header"><div><span class="pt-eyebrow">ASSESSMENT READINESS</span><h1>'+esc(chosen().unitName||'Algebra 1')+' Unit Test</h1><p class="pt-muted" id="pt-timer">'+(state.deadline?'Timed assessment':'Untimed assessment')+'</p></div><button class="pt-secondary" id="pt-exit">Save & exit</button></header>'+
 '<div class="pt-sticky-progress"><div class="pt-student-progress-row"><strong id="pt-progress-count"></strong><span>Answers save automatically</span></div><div class="pt-progress"><div id="pt-progress-fill"></div></div><nav class="pt-nav" aria-label="Jump to question">'+state.questions.map((q,i)=>'<button type="button" data-jump="'+i+'">'+(i+1)+'</button>').join('')+'</nav></div>'+
 '<div class="pt-actions"><button id="pt-print-paper">Print / Save Test as PDF</button></div>'+shareControls()+
 assessmentHTML()+'<section class="pt-card pt-finish"><h2>Ready to submit?</h2><p id="pt-finish-summary">Review your answers before submitting.</p><button id="pt-submit">'+(state.questions.some(function(q){return q.kind==='self';})?'Submit for self-review':'Submit answers for grading')+'</button></section>';

 bindShare();root.querySelector('#pt-print-paper').onclick=printPaper;
 root.querySelector('#pt-exit').onclick=()=>{state.paused=true;save();setup();};
 root.querySelectorAll('[data-jump]').forEach(function(b){b.onclick=()=>root.querySelector('#pt-question-'+(+b.dataset.jump+1)).scrollIntoView({behavior:'smooth',block:'start'});});
 root.querySelectorAll('[data-review-toggle]').forEach(function(b){b.onclick=function(){var q=state.questions[+b.dataset.reviewToggle];q.review=!q.review;save();updateProgress();};});
 root.querySelectorAll('[data-multi-answer]').forEach(function(btn){
   btn.onclick=function(){
     var i=+btn.dataset.multiAnswer,q=state.questions[i],choice=+btn.dataset.mcChoice,selected=Array.isArray(q.response)?q.response.slice():[],at=selected.indexOf(choice);
     if(at<0)selected.push(choice);else selected.splice(at,1);q.response=selected.length?selected:null;save();updateProgress();
     var group=btn.closest('[data-mc-question]');group.querySelectorAll('[data-multi-answer]').forEach(function(b){var on=Array.isArray(q.response)&&q.response.indexOf(+b.dataset.mcChoice)>=0;b.classList.toggle('selected',on);b.setAttribute('aria-pressed',String(on));});
   };
 });
 root.querySelectorAll('[data-authored-response]').forEach(function(el){el.oninput=function(){var q=state.questions[+el.dataset.authoredResponse];q.response=el.value.trim()||null;save();updateProgress();};});
 root.querySelectorAll('[data-mc-answer]').forEach(function(btn){
   btn.onclick=function(){
     var i=+btn.dataset.mcAnswer,q=state.questions[i],choice=+btn.dataset.mcChoice;
     q.response=q.response===choice?null:choice;
     save();updateProgress();
     var group=btn.closest('[data-mc-question]');
     group.querySelectorAll('[data-mc-answer]').forEach(function(b){
       var selected=q.response===+b.dataset.mcChoice;
       b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',String(selected));
     });
   };
 });
 root.querySelectorAll('[data-math-pad]').forEach(function(pad){
  pad.querySelectorAll('[data-math-insert]').forEach(function(button){
   button.onclick=function(){
    var input=root.querySelector('#pt-answer-'+pad.dataset.mathPad);if(!input)return;
    var kind=button.dataset.mathInsert,at=input.selectionStart==null?input.value.length:input.selectionStart,end=input.selectionEnd==null?at:input.selectionEnd;
    var change=G.MKMATHINPUT.insert(input.value,at,end,kind);
    input.value=change.text;
    input.focus();
    input.setSelectionRange(change.start,change.end);
    input.dispatchEvent(new Event('input',{bubbles:true}));
    input.focus();
   };
  });
 });
 root.querySelectorAll('[data-answer]').forEach(function(el){
  el.oninput=function(){
   var i=+el.dataset.answer,q=state.questions[i],v=el.value.trim();
   q.response=q.kind==='mc'?(v?(/^[ABCD]$/i.test(v)?'ABCD'.indexOf(v.toUpperCase()):v):null):(v||null);
   save();updateProgress();
   if(G.MKMATHPREVIEW)G.MKMATHPREVIEW.update(el,root.querySelector('[data-preview="'+i+'"]'));
  };
  if(G.MKMATHPREVIEW)G.MKMATHPREVIEW.update(el,root.querySelector('[data-preview="'+el.dataset.answer+'"]'));
 });
 if(G.MKGRAPH){G.MKGRAPH.bind(root,state,save);G.MKGRAPH.bindPoints(root,state,save);}if(G.MKLINE)G.MKLINE.bind(root,state,save);if(G.MKSYSTEM)G.MKSYSTEM.bind(root,state,save);if(G.MKEXPGRAPH)G.MKEXPGRAPH.bind(root,state,save);if(G.MKPARABOLA)G.MKPARABOLA.bind(root,state,save);
 root.querySelector('#pt-submit').onclick=()=>submit();
 updateProgress();
 tickTimer();
}
function go(i){state.index=Math.max(0,Math.min(state.questions.length-1,i));save();show();}
function submit(forced){var missing=state.questions.filter(q=>!isAnswered(q)).length;if(!forced&&!confirm('Submit assessment now? '+missing+' question(s) are unanswered. '+state.questions.filter(q=>q.review).length+' marked for review.'))return;state.questions.forEach(q=>{if(q.kind==='multi'){var actual=Array.isArray(q.response)?q.response.slice().sort(function(a,b){return a-b;}):[],expected=(q.choices.keys||[]).slice().sort(function(a,b){return a-b;});q.correct=actual.length===expected.length&&actual.every(function(v,i){return v===expected[i];});}else if(q.kind==='mc'){q.correct=typeof q.response==='number'&&q.response===q.choices.key;}else if(G.MKEXPGRAPH&&G.MKEXPGRAPH.target(q)){q.correct=G.MKEXPGRAPH.grade(q).status==='correct';}else if(G.MKSYSTEM&&G.MKSYSTEM.target(q)){q.correct=G.MKSYSTEM.grade(q).status==='correct';}else if(G.MKLINE&&G.MKLINE.target(q)){q.correct=G.MKLINE.grade(q).status==='correct';}else if(G.MKPARABOLA&&G.MKPARABOLA.target(q)){q.correct=G.MKPARABOLA.grade(q).status==='correct';}else if(G.MKGRAPH&&G.MKGRAPH.pointTarget(q)){var gg=G.MKGRAPH.pointGrade(q);q.correct=gg.status==='correct';}else if(G.MKGRAPH&&G.MKGRAPH.supports(q)){var gg=G.MKGRAPH.grade(q);q.correct=gg.status==='correct';}else if(q.kind==='auto'){var g=G.MKPRACTICE.grade(q.problem,q.response);q.correct=g.status==='correct';if(g.status==='self')q.invalidResponse='This response could not be graded automatically.';else q.invalidResponse=g.status==='invalid'?g.message:null;}if(q.kind==='self'&&(q.response===null||q.response===''))q.correct=false;q.checked=true;});state.done=true;state.finished=Date.now();save();results();}
function stats(){var buckets={};state.questions.forEach(q=>{var b=buckets[q.skill]||(buckets[q.skill]={name:q.skillName,correct:0,graded:0,missing:0});if(q.correct===null)b.missing++;else{b.graded++;if(q.correct)b.correct++;}});return Object.entries(buckets).map(([id,b])=>Object.assign({id:id},b));}
function recommendations(){
 var list=stats().filter(b=>b.graded>0).sort((a,b)=>a.correct/a.graded-b.correct/b.graded);
 if(!list.length)return 'Review your written responses to see which skills need more practice.';
 var weak=list.filter(b=>b.correct/b.graded<0.8).slice(0,3);
 if(!weak.length)return 'Strong results on the skills assessed. Try another version to confirm your understanding.';
 return 'Focus next on: '+weak.map(b=>b.name).join('; ')+'. Select Practice my weak skills for fresh questions.';
}
function responseLabel(q){var v=q.response;if(v===null||v===undefined||v===''||(Array.isArray(v)&&!v.length))return '(blank)';if(Array.isArray(v)&&q.choices)return v.map(function(i){return q.choices.opts[i];}).join(', ');if(typeof v!=='string')return String(v);if(v.startsWith('expplot:'))return 'Plotted exponential function';if(v.startsWith('system:'))return 'Two plotted lines';if(v.startsWith('line:'))return 'Drawn line and shading';if(v.startsWith('parabola:'))return 'Five-point parabola';if(v.startsWith('graph:'))return 'Interactive number-line graph';if(v.startsWith('point:'))return 'Plotted point '+v.slice(6);return v;}
function results(){var qs=state.questions,graded=qs.filter(q=>q.correct!==null),good=graded.filter(q=>q.correct).length,remaining=qs.length-graded.length;root.innerHTML='<section class="pt-card"><span class="pt-eyebrow">ASSESSMENT REPORT</span><h1>Assessment Readiness Report</h1><p class="pt-score">'+(graded.length?Math.round(good/graded.length*100)+'%':'Self-review required')+'</p><p>'+good+' / '+graded.length+' graded correctly'+(remaining?' · '+remaining+' awaiting self-assessment':'')+'</p><h2>Your study plan</h2><p>'+esc(recommendations())+'</p><h2>Skills breakdown</h2>'+stats().map(b=>'<div class="pt-skillbar"><div><strong>'+esc(b.name)+'</strong><span>'+b.correct+'/'+b.graded+' graded'+(b.missing?' · '+b.missing+' unreviewed':'')+'</span></div><div class="pt-track"><div style="width:'+(b.graded?100*b.correct/b.graded:0)+'%"></div></div></div>').join('')+'<div class="pt-actions"><button id="pt-weak">Practice my weak skills</button><button id="pt-retry" class="pt-secondary">New version</button><button id="pt-print" class="pt-secondary">Print report</button><button id="pt-new" class="pt-secondary">New setup</button></div>'+shareControls()+'<h2>Review answers</h2>'+qs.map((q,i)=>'<details class="pt-review"><summary>Question '+(i+1)+' · '+esc(q.skillName)+' · '+(q.correct===null?'Self-check':q.correct?'Correct':'Incorrect')+'</summary>'+problemHTML(q)+'<p><strong>Your response: </strong>'+(q.kind==='mc'&&typeof q.response==='number'?fmt(q.choices.opts[q.response]):esc(responseLabel(q)))+'</p>'+feedback(q)+(q.invalidResponse?'<p class="pt-bad">'+esc(q.invalidResponse)+'</p>':'')+(q.kind==='self'?'<div class="pt-actions"><button data-self="'+i+'" data-val="yes">Correct</button><button data-self="'+i+'" data-val="no" class="pt-secondary">Needs practice</button></div>':'')+'</details>').join('')+'</section>';
 bindShare();root.querySelector('#pt-weak').onclick=()=>{var weak=stats().filter(b=>(b.graded>0&&b.correct/b.graded<0.8)||b.missing>0).map(b=>b.id);if(!weak.length){alert('No weak skills identified. Try a new version!');return;}config.count=Math.min(10,Math.max(5,weak.length*3));config.minutes=0;config.mode='test';build(weak);};
 root.querySelector('#pt-retry').onclick=()=>build();root.querySelector('#pt-print').onclick=()=>{root.querySelectorAll('details.pt-review').forEach(d=>d.open=true);print();};root.querySelector('#pt-new').onclick=()=>{state=null;save();setup();};
 root.querySelectorAll('[data-self]').forEach(b=>b.onclick=()=>{qs[+b.dataset.self].correct=b.dataset.val==='yes';save();results();});
}
function startPractice(){
 read();var params=new URLSearchParams((G.location.hash||'').replace(/^#/,'')),student=params.get('student')==='1',requested=/unit=([a-z0-9-]+)/.exec(G.location.hash||'');
 if(params.get('setup')==='1')state=null;
 if(requested&&requested[1].indexOf('algebra2-')===0&&!N.skillSets[requested[1]]){root.innerHTML='<section class="pt-card"><h1>Algebra 2 questions are unavailable</h1><p>The approved Algebra 2 bank did not finish loading. Refresh this page to try again.</p></section>';return;}
 if(student&&N.skillSets[params.get('unit')]){config.unit=params.get('unit');config.level=['cp2','cp1','honors'].includes(params.get('level'))?params.get('level'):'cp1';config.count=[5,10,15,20,25].includes(+params.get('count'))?+params.get('count'):10;config.format=['mixed','mc','self'].includes(params.get('format'))?params.get('format'):'mixed';config.minutes=[0,20,30,45].includes(+params.get('minutes'))?+params.get('minutes'):0;config.skills=(params.get('skills')||'').split(',').filter(function(id){return N.skillSets[config.unit].byId[id];});if(!config.skills.length)config.skills=N.skillSets[config.unit].skills.map(function(x){return x.id;});state=null;}
 config.mode='test';if(state&&!state.done){state.mode='test';save();}
 if(requested&&N.skillSets[requested[1]]&&(!state||state.done||requested[1]!==config.unit)){config.unit=requested[1];config.skills=N.skillSets[config.unit].skills.map(function(skill){return skill.id;});state=null;}
 if(!N.skillSets[config.unit])config.unit=units()[0][0];
 if(state&&!state.done){root.innerHTML='<section class="pt-card"><h1>Continue your practice test?</h1><p>Your previous assessment is saved in this browser.</p><div class="pt-actions"><button id="resume">Resume test</button><button id="fresh" class="pt-secondary">Start fresh</button></div>'+shareControls()+'</section>';bindShare();root.querySelector('#resume').onclick=show;root.querySelector('#fresh').onclick=function(){state=null;save();setup();};}
 else if(state&&state.done)results();else setup();
}
if(G.MK_COURSE_BANKS_READY)G.MK_COURSE_BANKS_READY.then(startPractice,startPractice);else startPractice();
})(window);