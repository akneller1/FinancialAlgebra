#!/usr/bin/env node
'use strict';
/* Branch-only semantic QA: inspect what the English sentence actually asks,
 * not just whether the stored mathematical check agrees with its own answer. */
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const units=read('course-outlines/grade1.json').units;
const findings=[],tested={questions:0,diagrams:0};
function add(code,q,check,reason,severity='blocking'){
 findings.push({code,severity,id:q.id,prompt:q.prompt,storedAnswer:q.answer,check:check?.fn||check?.k||null,reason});
}
const integer=x=>/^\d+$/.test(String(x).trim());
for(const unit of units){
 const bank=read('question-banks/math1/'+unit.id+'.json');
 const checks=read('tools/grade1-authoring/out/'+unit.id+'.checks.json');
 for(const q of bank.questions){
  tested.questions++;if(q.diagram)tested.diagrams++;
  const text=q.prompt||'',answer=String(q.answer);
  const chk=checks[q.id]||{},check=chk.q||{},fn=check.fn||'';
  if(q.format==='short-answer'&&
    /(?:how many (?:straight )?(?:sides|corners|vertices|faces)\b|count the (?:straight )?(?:sides|corners)\b|(?:shape|figure) has _+ (?:straight )?sides\b)/i.test(text) &&
    !integer(answer))
   add('COUNT_ASKED_SHAPE_ANSWER',q,check,'The question asks a numerical count but the answer is a shape name.');
  if(/\bhad some\b/i.test(text)&&/\bgave\b/i.test(text)&&/\bmore\b/i.test(text)&&/\bnow\b/i.test(text)&&/\bstart(?:ed)? with\b/i.test(text)&&integer(answer)){
   const m=text.match(/\bgave\b[\s\S]*?\b(\d+)\s+more\b[\s\S]*?\bnow\b[\s\S]*?\bhas\b\s+(\d+)\b/i);
   if(m&&+answer!==+m[2]-+m[1])
    add('START_UNKNOWN_STORY',q,check,'Added '+m[1]+' to the starting quantity to reach '+m[2]+'; correct starting quantity: '+(+m[2]-+m[1])+'.');
  }
  const shapes=chk.diagram?.data?.shapes;
  if(Array.isArray(shapes)&&/^(?:circle|square|rectangle|triangle|hexagon|cube|cylinder|sphere|cone)$/i.test(answer)
    && (/\b(?:which|what) shape\b|\bname the shape\b/i.test(text)||fn==='shape_attr_name') &&
    !shapes.some(s=>String(s.type).toLowerCase()===answer.toLowerCase()))
   add('ANSWER_NOT_IN_DRAWN_SHAPES',q,check,'Drawing contains '+shapes.map(x=>x.type).join(', ')+', but not '+answer+'.');
  if(fn==='shape_attr_name'&&/two triangles are put together along one side/i.test(text)&&answer.toLowerCase()==='hexagon')
   add('TWO_TRIANGLES_CANNOT_FORM_HEXAGON',q,check,'Two triangles joined along one full side have four outer sides, not six.');
  if(['clock_minutes','half_hour'].includes(fn)&&integer(answer)&&
    /\b(?:what time|time is shown|read the clock|write the time|clock shows ___)\b/i.test(text)&&!/\bminutes?\b/i.test(text))
   add('TIME_VS_MINUTES',q,check,'Asked for a time, stored check returns number of minutes.');
  if(fn==='partition_count'&&integer(answer)&&
    /\b(?:parts called|name one part|each part is one|two equal parts are called|four equal parts are called)\b/i.test(text))
   add('PART_COUNT_VS_NAME',q,check,'Asked for a name of a fraction part, stored check returns a count.');
  if(['tally_most','graph_most','most_of'].includes(fn)&&
    /\b(?:how many (?:in all|marks|rows)|what is the total|count the tally marks|add the rows)\b/i.test(text))
   add('MOST_CATEGORY_VS_TOTAL',q,check,'Question asks total; check returns name of most-frequent category.');
  if(['tally_one','graph_one'].includes(fn)&&/\b(?:in all|what is the total|count the tally marks|add the rows)\b/i.test(text))
   add('CATEGORY_COUNT_VS_TOTAL',q,check,'Question asks total; check returns one category count.');
  if(['shorter','longer'].includes(fn)&&
    ((fn==='shorter'&&/\bwhich (?:object|one|item)?\s*(?:is )?longer\b/i.test(text))||
     (fn==='longer'&&/\bwhich (?:object|one|item)?\s*(?:is )?shorter\b/i.test(text))))
   add('LONGER_SHORTER_REVERSED',q,check,'Question asks opposite comparison from stored check.');
  if(fn==='tens_from_ones'&&integer(answer)&&/\bones (?:digit|place)\b|\bhow many ones\b/i.test(text))
   add('TENS_VS_ONES',q,check,'Check expects tens, question asks ones.');
  if(/\b1 tens\b|\b1 ones\b/i.test(text))
   add('SINGULAR_TENS_ONES',q,check,'Use 1 ten/1 one, not plural.', 'editorial');
  if(/\bHow many ones are in \d+ tens? and \d+ ones?\b/i.test(text))
   add('ONES_PLACE_AMBIGUITY',q,check,'Clarify ones digit or loose ones.', 'editorial');
 }
}
const groups={};for(const f of findings)(groups[f.code]||(groups[f.code]=[])).push(f);
const categories=Object.entries(groups).map(([code,items])=>({code,count:items.length,severity:items[0].severity,samples:items.slice(0,12)})).sort((a,b)=>b.count-a.count);
const blocking=findings.filter(x=>x.severity==='blocking');
const report={status:blocking.length?'SEMANTIC_ERRORS_FOUND':'SEMANTIC_PATTERN_CHECKS_PASS',tested,blockingFindings:blocking.length,editorialFindings:findings.length-blocking.length,categories,disclaimer:'Pattern-based checks are not exhaustive. Further editorial review is required.'};
fs.writeFileSync(path.join(root,'grade1-semantic-report.json'),JSON.stringify(report,null,2));
let md='# Grade 1 semantic audit\n\nResult: **'+report.status+'**. Blocking findings: '+blocking.length+'; editorial wording issues: '+report.editorialFindings+'.\n\n';
for(const group of categories){
 md+='## '+group.code+' ('+group.count+')\n\n';
 for(const f of group.samples)md+='- '+f.id+': '+f.prompt.replace(/\s+/g,' ').slice(0,200)+' | Stored: '+JSON.stringify(f.storedAnswer)+' | '+f.reason+'\n';
 md+='\n';
}
md+='These are real answer/prompt compatibility checks, separate from the arithmetic verifier. All banks remain approved:false.\n';
fs.writeFileSync(path.join(root,'grade1-semantic-report.md'),md);
if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,md.slice(0,10000));
console.log(JSON.stringify({status:report.status,blocking:blocking.length,editorial:report.editorialFindings,categories:categories.map(x=>({code:x.code,count:x.count})),samples:blocking.slice(0,8)},null,2));
if(blocking.length)process.exitCode=1;
