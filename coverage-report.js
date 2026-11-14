/* Teacher-facing coverage dashboard. Counts only verified questions registered in the
   new shared adapter. Legacy generator coverage is intentionally not asserted. */
(function(root){
'use strict';
var C=root.MK_COURSE_CATALOG, B=root.MK_QUESTION_BANKS;
function report(library, courseId){
 if(!C||!B||!library) return [];
 return library.courses.filter(function(c){return !courseId||c.id===courseId;}).map(function(c){
  var unitReports=c.units.map(function(u){
   var records=C.getSkillRecords(c.id,u.id);
   var coverage=B.coverage(c.id,u.id);
   var covered=coverage.filter(function(s){return s.verified && ['cp2','cp1','honors'].every(function(level){return s.counts[level]>0;});}).length;
   var questions=coverage.reduce(function(n,s){return n+(s.verified?s.counts.cp2+s.counts.cp1+s.counts.honors:0);},0);
   return {id:u.id,name:u.name,skillCount:records.length,fullyCovered:covered,approvedQuestions:questions,skills:coverage};
  });
  return {id:c.id,name:c.name,unitCount:c.units.length,skillCount:unitReports.reduce(function(n,u){return n+u.skillCount;},0),
   fullyCovered:unitReports.reduce(function(n,u){return n+u.fullyCovered;},0),approvedQuestions:unitReports.reduce(function(n,u){return n+u.approvedQuestions;},0),units:unitReports};
 });
}
root.MK_COVERAGE_REPORT={version:1,report:report};
})(typeof window!=='undefined'?window:globalThis);
