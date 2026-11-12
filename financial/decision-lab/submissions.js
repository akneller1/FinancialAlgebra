/* Complete student submissions and teacher guides. No student data leaves this device. */
(function(G){
'use strict';
var current, R=G.FA_RENDER;
function answer(x){return '<div class="lab-response">'+R.esc(String(x==null||x===''?'Not answered':x))+'</div>';}
function option(id){return (current.lab.options.find(function(o){return o.id===id;})||{}).name||'Not answered';}
function questions(list,prefix,guide){return list.map(function(q,i){var v=current.defaults;return '<section class="lab-answer"><p><strong>'+(i+1)+'.</strong> '+R.rich(typeof q.prompt==='function'?q.prompt(v):q.prompt)+'</p>'+(guide?'<p><strong>Answer:</strong> '+current.fmt(q.answer(v),q.fmt)+'</p>'+(q.solution?'<p>'+R.rich(q.solution(v))+'</p>':''):answer(current.resp[prefix+i]))+'</section>';}).join('');}
function report(guide){
 var c=current,L=c.lab,r=c.resp;
 var rows=[['Initial choice',option(r.initial)],['Why? What feels most important right now?',r.initialWhy],['Final choice',option(r.final)],['Justify your recommendation using at least two numbers from your investigation and one non-financial factor.',r.finalWhy],['Which assumption changed the result the most? Describe what happened.',r.sensitivity]].concat(L.reflection.map(function(q,i){return[q,r['ref'+i]];}));
 var settings=L.vars.map(function(v){function show(value){return v.type==='toggle'?(value?'Yes':'No'):c.fmt(value,v.fmt);}return[v.label,show(c.defaults[v.id]),show(c.vars[v.id])];});
 return '<section class="fa-sheet"><header><p>Financial Decision Lab · '+(guide?'Teacher guide':'Student work')+'</p><h1>'+R.esc(L.title)+'</h1></header>'+(guide?'<p>Use default assumptions to check the investigation and challenge answers. Evaluate recommendations using the student’s changed settings and evidence. Different choices can earn full credit when justified.</p>':'<p><strong>Name:</strong> '+R.esc(r.studentName||'Not provided')+' · <strong>Class:</strong> '+R.esc(r.studentClass||'Not provided')+' · <strong>Date:</strong> '+R.esc(r.studentDate||'Not provided')+'</p><p>Exported: '+R.esc(new Date().toLocaleString())+'</p>')+
 '<h2>Situation</h2><p>'+R.rich(L.situation)+'</p>'+R.table({headers:['Fact','Detail'],rows:L.person.facts})+'<p><strong>Goal:</strong> '+R.rich(L.goal)+'</p><h2>Options</h2>'+L.options.map(function(o){return '<h3>'+R.esc(o.name)+'</h3>'+R.table({headers:['Detail','Value'],rows:o.details});}).join('')+(L.assumptions?'<p>'+R.rich(L.assumptions)+'</p>':'')+
 '<h2>Scenario settings</h2>'+R.table({headers:['Assumption','Default','Current setting'],rows:settings})+'<h2>Investigation — default assumptions</h2>'+questions(L.questions,'q',guide)+'<h2>Challenges — default assumptions</h2>'+questions(L.challenges,'c',guide)+'<h2>Comparison at default assumptions</h2>'+c.resultsTable(c.defaults)+
 (guide?'<h2>Sample recommendation</h2><p>'+R.rich(L.teacher.model)+'</p><h2>Teaching notes and common misconceptions</h2><ul>'+L.teacher.notes.concat(L.teacher.misconceptions).map(function(n){return '<li>'+R.rich(n)+'</li>';}).join('')+'</ul><h2>Rubric</h2>'+R.rubric(L.rubric||c.rubric()):'<h2>Comparison with student’s current settings</h2>'+c.resultsTable(c.vars)+'<h2>Decisions and reflection</h2>'+rows.map(function(row){return '<section class="lab-answer"><h3>'+R.esc(row[0])+'</h3>'+answer(row[1])+'</section>';}).join(''))+'</section>';
}
function print(guide){current.save();document.getElementById('printSummary').innerHTML=report(guide);document.body.classList.add('lab-report');G.print();}
G.addEventListener('afterprint',function(){document.body.classList.remove('lab-report');});
function attach(c){
 current=c;var panel=document.createElement('section');panel.className='fa-panel fa-noprint lab-submission-tools';panel.setAttribute('aria-label','Your work');
 panel.innerHTML='<div class="fa-grid">'+['studentName','studentClass','studentDate'].map(function(key,i){return '<label class="fa-field">'+['Name','Class / period','Date'][i]+'<input data-resp="'+key+'"'+(i===2?' type="date"':'')+' value="'+R.esc(c.resp[key]||'')+'"></label>';}).join('')+'</div><p><button class="fa-btn primary" id="exportWork">Export My Work / Save as PDF</button> <button class="fa-btn" id="newStudent">Start new student</button>'+(c.student?'':' <button class="fa-btn" id="generateStudentLink">Generate student link</button>')+(c.teacher?' <button class="fa-btn" id="printGuide">Print teacher guide</button>':'')+'</p><p>Choose “Save as PDF” in the print dialog, then attach the file in Google Classroom. Unanswered questions are labeled; partial work is welcome.</p><p id="saveStatus" role="status"></p><p>Work stays in this browser on this device. On a shared device, start a new student before working.</p><div id="studentLinkResult"></div>';
 document.querySelector('#app header').after(panel);
 document.getElementById('exportWork').onclick=function(){print(false);};
 document.getElementById('newStudent').onclick=function(){if(G.confirm('Clear saved work for this lab and start a new student? Export your work first.'))c.reset();};
 if(c.teacher)document.getElementById('printGuide').onclick=function(){print(true);};
 if(!c.student)document.getElementById('generateStudentLink').onclick=function(){
  var url=new URL(G.location.href);url.search='';url.hash='';url.searchParams.set('lab',c.labId);url.searchParams.set('student','1');url.searchParams.set('settings',JSON.stringify(c.vars));url.searchParams.set('assignment',Date.now().toString(36));
  var area=document.getElementById('studentLinkResult');area.innerHTML='<p>This link starts with your current settings. Students can change them during exploration. It includes no student responses.</p><label class="fa-field">Student link<input class="lab-share-link" readonly value="'+R.esc(url.href)+'"></label><button class="fa-btn" id="copyStudentLink">Copy link</button><p role="status" id="linkStatus"></p>';
  var input=area.querySelector('input');input.select();document.getElementById('copyStudentLink').onclick=function(){function fallback(){input.focus();input.select();}if(G.navigator.clipboard)G.navigator.clipboard.writeText(input.value).then(function(){document.getElementById('linkStatus').textContent='Copied!';},fallback);else fallback();};
 };
}
G.FA_SUBMISSIONS={attach:attach,print:print,report:report};
})(window);
