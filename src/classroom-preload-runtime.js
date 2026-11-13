/* Development-only registration for native Classroom generators before banks exist.
   Bank-backed units keep their normal validated implementation. */
(function(G){
 'use strict';
 var N=G.MKMENU;if(!N||!G.MK_ELEMENTARY_PRELOAD)return;
 var pending=Object.create(null);
 function register(){
  G.MK_ELEMENTARY_PRELOAD.forEach(function(course){
   course.units.forEach(function(unit){
    var id=course.id+'-'+unit.id;
    if(G.MK_QUESTION_BANKS&&G.MK_QUESTION_BANKS.available(course.id,unit.id))return;
    pending[id]=true;
    var records=G.MK_COURSE_CATALOG.getSkillRecords(course.id,unit.id),tags={};
    records.forEach(function(s){tags[s.name]=s.name;});
    N.registerSkillSet({id:id,unitName:unit.name,courseName:course.name,preloaded:true,
     gaps:['Question bank coming soon. Settings are ready; generation starts when this unit’s bank is added.'],tags:tags,
     skills:records.map(function(s){return {id:s.id,name:s.name,tag:s.name,blurb:s.name,
      print:['maze','color','partner','who','stations','tarsia','error'],
      generate:function(){throw Error('Question bank coming soon');}};})});
   });
  });
 }
 var generate=N.generateProblem;
 N.generateProblem=function(id){return pending[id]?{failed:true,reason:'Question bank coming soon.'}:generate.apply(this,arguments);};
 // Formats can be configured before items are authored, without declaring any questions available.
 ['skillFormatOk','multiUnitSupported','multiCapable','mcCapable','mcasCapable'].forEach(function(name){
  var original=N[name];if(original)N[name]=function(id){return pending[id]?true:original.apply(this,arguments);};
 });
 var ready=G.MK_COURSE_BANKS_READY||Promise.resolve();
 G.MK_COURSE_BANKS_READY=ready.then(function(value){register();return value;});
 G.MK_ALGEBRA2_NATIVE_READY=G.MK_COURSE_BANKS_READY;
 G.MK_PRELOADED_PLANNER_UNIT=function(courseId,key){
  var course=G.MK_ELEMENTARY_PRELOAD.find(function(c){return c.id===courseId;}),match=/^u(\d+)$/.exec(key||'');
  var unit=course&&match&&course.units[Number(match[1])-1];
  return unit?courseId+'-'+unit.id:null;
 };
 if(G.document){
  function message(){
   var hash=new URLSearchParams(G.location.hash.slice(1)),id=hash.get('unit');
   var selected=G.document.getElementById('mmUnitSel')||G.document.getElementById('prUnit');
   if(selected)id=selected.value;
   var course=hash.get('course')||G.MKPLAN_COURSE;
   var planner=G.document.getElementById('plUnit');
   if(planner)id=G.MK_PRELOADED_PLANNER_UNIT(course,planner.value);
   var missing=!!pending[id];
   var notice=G.document.getElementById('preloadedBankNotice');
   if(!notice){notice=G.document.createElement('p');notice.id='preloadedBankNotice';notice.setAttribute('role','status');notice.style.cssText='margin:12px auto;padding:14px 20px;max-width:1200px;background:#fff4d6;color:#302a20;border:1px solid #ddc47c;border-radius:10px';G.document.body.insertBefore(notice,G.document.querySelector('main'));}
   notice.hidden=!missing;notice.textContent='Question bank coming soon. Choose skills, levels, and question types now; questions and teacher keys will be available when this unit is ready.';
   return missing;
  }
  G.MK_COURSE_BANKS_READY.then(function(){
   if(G.document.readyState==='loading')G.document.addEventListener('DOMContentLoaded',function(){G.setTimeout(message,0);});else G.setTimeout(message,0);
  });
  G.document.addEventListener('change',function(){Promise.resolve().then(message);});
  G.addEventListener('hashchange',function(){Promise.resolve().then(message);});
  G.document.addEventListener('click',function(e){
   var button=e.target.closest&&e.target.closest('button');
   if(button&&['mmBuildBtn','prNew','prPrint','plNew','plPrintS','plPrintK','plPptxStudent','plPptxTeacher'].includes(button.id)&&message()){
    e.preventDefault();e.stopImmediatePropagation();
   }
  },true);
 }
 G.MK_PRELOADED_UNITS=pending;
})(window);
