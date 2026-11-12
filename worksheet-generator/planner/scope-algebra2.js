/* Algebra 2 lesson-planner scope generated from the shared course catalog.
   Each catalog skill is a selectable lesson topic; all questions come from the approved bank. */
(function(G){
'use strict';
['algebra2','prealgebra','prealgebra7','math6','math5','precalculus','calculus','statistics','discrete'].forEach(function(courseId){
var course=G.LIBRARY.courses.filter(function(c){return c.id===courseId;})[0];
var key={algebra2:'ALGEBRA2',prealgebra:'PREALGEBRA',prealgebra7:'PREALGEBRA7',math6:'MATH6',math5:'MATH5',precalculus:'PRECALCULUS',calculus:'CALCULUS',statistics:'STATISTICS',discrete:'DISCRETE'}[courseId],prefix={algebra2:'A2',prealgebra:'PA8',prealgebra7:'PA7',math6:'M6',math5:'M5',precalculus:'PC',calculus:'CA',statistics:'ST',discrete:'DM'}[courseId];
var catalog=G.MK_COURSE_CATALOG;
if(!course||!catalog||!catalog.getSkillRecords)throw new Error('Algebra 2 planner catalog is unavailable.');
var days=[],units=[],lessons={},SETS={},UNIT_SET={},dayTypes={
 Lesson:{do_now:'Retrieval from a previous topic',notes:'Teacher notes and guided examples',practice:'Approved question bank practice, scaffolded by difficulty',exit_ticket:'Short check for understanding'},
 Practice:{do_now:'Retrieval warm-up',notes:'Student reference and worked examples',practice:'Tiered practice from this unit',exit_ticket:'Self-assessment and one final check'},
 Quiz:{do_now:'Brief confidence warm-up',notes:'',practice:'Short quiz from this unit',exit_ticket:'Quiz reflection'},
 Review:{do_now:'Spiral warm-up',notes:'Unit study guide',practice:'Review stations covering selected unit topics',exit_ticket:'Unit self-assessment'},
 Assessment:{do_now:'Calm start',notes:'',practice:'Unit assessment from approved questions',exit_ticket:'Post-assessment reflection'},
 Flex:{do_now:'Targeted warm-up',notes:'Reteach notes',practice:'Corrections, reteach and enrichment',exit_ticket:'Correction reflection'}
};
var day=0,previousLesson=null;
course.units.forEach(function(unit,ui){
 var records=catalog.getSkillRecords(courseId,unit.id),unitNo=ui+1,setKey=prefix+'U'+unitNo,setId=courseId+'-'+unit.id;
 SETS[setKey]=setId;UNIT_SET[unitNo]=setKey;
 var start=day+1,ids=[],unitStd=[];
 var std=function(skillId){var list=G.MKSTD?G.MKSTD.content(G.MKSTD.forSkill(setId,skillId)):[];list.forEach(function(c){if(unitStd.indexOf(c)<0)unitStd.push(c);});return list.join(', ');};
 records.forEach(function(skill,si){
  var id=prefix+'-U'+unitNo+'-S'+(si+1),number=++day,title=skill.name,meta=courseId==='algebra2'&&G.MKPLAN_TEACH_ALGEBRA2_META?G.MKPLAN_TEACH_ALGEBRA2_META(skill.id):null;
  var verb=meta&&meta.obj?meta.obj:'work with '+title.charAt(0).toLowerCase()+title.slice(1);
  ids.push(id);lessons[id]={cover:'full',skills:[[setKey,skill.id,1,7]]};
  days.push({day:number,quarter:0,week:0,unit:unitNo,unit_title:unit.name,unit_day:(si+1)+' of '+records.length,
   day_type:'Lesson',lesson_id:id,title:title,standards:std(skill.id),
   content_objective:'Students will be able to '+verb+'.',
   language_objective:'Students will explain their mathematical reasoning using accurate mathematical vocabulary.',
   sentence_frame:'To '+verb.split(/,| and /)[0]+', I first ___ and then ___.',
   key_vocabulary:meta&&meta.voc?meta.voc.map(function(w){return w[0];}).join(', '):'',common_misconception:meta&&meta.watch?meta.watch:'',notes_style:'Guided notes',
   do_now_strategy:previousLesson?'Review a previously learned topic.':'Settle in and preview today’s learning.',
   do_now_source_ids:previousLesson?[previousLesson]:[],spiral_review_ids:previousLesson?[previousLesson]:[],
   lessons_covered:[id],components:dayTypes.Lesson});
  previousLesson=id;
 });
 var endLessons=day;
 var extras=[
  {type:'Practice',title:unit.name+' · Practice',id:prefix+'-U'+unitNo+'-PRACTICE'},
  {type:'Review',title:unit.name+' · Review',id:prefix+'-U'+unitNo+'-REVIEW'},
  {type:'Quiz',title:unit.name+' · Quiz',id:prefix+'-U'+unitNo+'-QUIZ'},
  {type:'Assessment',title:unit.name+' · Assessment',id:prefix+'-U'+unitNo+'-ASSESSMENT'}
 ];
 extras.forEach(function(x){
  var number=++day;
  days.push({day:number,quarter:0,week:0,unit:unitNo,unit_title:unit.name,unit_day:x.type,
   day_type:x.type,lesson_id:x.id,title:x.title,standards:G.MKSTD?G.MKSTD.sort(unitStd).join(', '):'',content_objective:'Review and assess the selected topics in '+unit.name+'.',
   language_objective:'Students will explain their mathematical reasoning using accurate mathematical vocabulary.',
   sentence_frame:'One strategy I used was ___.',key_vocabulary:'',common_misconception:'',
   notes_style:x.type==='Assessment'?'':'Guided review',do_now_strategy:'Review selected topics from this unit.',
   do_now_source_ids:ids.slice(-2),spiral_review_ids:ids,lessons_covered:ids.slice(),components:dayTypes[x.type]});
 });
 units.push({unit:unitNo,title:unit.name,start_day:start,end_day:day,total_days:day-start+1,lesson_ids:ids});
});
G['MKPLAN_SCOPE_'+key]={meta:{course:course.name,total_days:day,standards_framework:'Course skill catalog',version:'1.0',notes:'Skill-based planning topics are generated from the shared course catalog. Questions are selected from the approved course banks; this is not a district pacing calendar.'},day_types:dayTypes,units:units,days:days};
G['MKPLAN_SKILLS_'+key]={SETS:SETS,UNIT_SET:UNIT_SET,lessons:lessons};
});
})(window);

