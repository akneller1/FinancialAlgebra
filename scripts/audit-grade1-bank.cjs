#!/usr/bin/env node
'use strict';
/* Branch-only Grade 1 QA. Reads all banks, diagrams and meta as checked out by GitHub Actions.
 * Mathematical correctness is independently checked by verify1.py, not this script.
 * All banks remain approved:false. Nothing is registered as student-verified or deployed. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const exists=p=>fs.existsSync(path.join(root,p));
const manifest=JSON.parse(read('question-banks/math1/manifest.json'));
const outline=JSON.parse(read('course-outlines/grade1.json'));
const errors=[],editorial=[],byUnit=[],perSkill=[];
const totals={units:0,skills:0,questions:0,diagrams:0,questionFormats:{},levels:{},ambiguousOnesWording:0,singularTensOnes:0,puzzleMastersRestrictedSkillLevels:0,sourceNotesClaimClaude:0,exactCrossSkillDuplicateCopies:0,metaRecords:0};
const expectedRecords={};
function issue(message){errors.push(message);}
const skillMap=new Map();
for(const unit of outline.units){
 const m=new Map();
 for(let i=0;i<unit.skills.length;i++)m.set(unit.id+'-skill-'+String(i+1).padStart(2,'0'),{name:unit.skills[i],index:i+1});
 skillMap.set(unit.id,m);
 expectedRecords[unit.id]=[...m].map(([id,v])=>({id,name:v.name,index:v.index}));
}
const sandbox={window:{MK_COURSE_CATALOG:{
 getSkillRecords(courseId,unitId){return ['math1','grade1'].includes(courseId)?(expectedRecords[unitId]||[]):[];}
}}};
vm.runInNewContext(read('question-bank-adapter.js'),sandbox,{filename:'question-bank-adapter.js'});
const adapter=sandbox.window.MK_QUESTION_BANKS;
const seenIds=new Set(),seenExact=new Map(),seenPng=new Set();
if(manifest.version!==1||manifest.courseId!=='math1'||manifest.banks.length!==8)issue('Grade 1 manifest must contain exactly eight math1 units');
if(manifest.review?.editorialApproval?.approved!==false)issue('Editorial approval must remain false');
if(manifest.review?.mathematicalValidation?.status!=='passed')issue('Mathematical validation result not recorded');
const validFormats=new Set(['short-answer','multiple-choice','select-all','open-response']);
const expectedUnits=outline.units.map(x=>x.id).join('|');
if(manifest.banks.map(x=>x.unitId).join('|')!==expectedUnits)issue('Bank manifest order/IDs differ from canonical Grade 1 outline');
for(const entry of manifest.banks){
 const u=outline.units.find(x=>x.id===entry.unitId);
 if(!u){issue('Unknown unit '+entry.unitId);continue;}
 if(entry.approved!==false||entry.editorialApproval!=='pending')issue('Bank accidentally enabled: '+entry.unitId);
 if(entry.teacherUse===true)issue('Unreviewed bank teacherUse must not be enabled: '+entry.unitId);
 const bankFile='question-banks/'+entry.path;
 if(!exists(bankFile)){issue('Missing bank '+bankFile);continue;}
 const bank=JSON.parse(read(bankFile)),metaFile='question-banks/math1/meta/'+entry.unitId+'.meta.json';
 const metadata=exists(metaFile)?JSON.parse(read(metaFile)):{};
 if(!exists(metaFile))issue('Missing question metadata '+metaFile);
 const valid=adapter.validate(bank);
 if(!valid.ok)issue('Shared Grade 5 bank adapter rejects '+entry.unitId+': '+valid.errors.slice(0,10).join('; '));
 // Register as UNVERIFIED: the production loader must not select this data.
 const registered=adapter.register(bank,{verified:false});
 if(!registered.ok)issue('Adapter failed to register quarantined '+entry.unitId);
 if(adapter.available('math1',entry.unitId))issue('An unapproved bank is unexpectedly available to students: '+entry.unitId);
 if(adapter.select({courseId:'math1',unitId:entry.unitId}).length!==0)issue('Unapproved bank unexpectedly exposes questions: '+entry.unitId);
 const qids=new Set(),skills=skillMap.get(u.id),byScope=new Map(),imageCountBefore=totals.diagrams;
 for(const q of bank.questions||[]){
  totals.questions++;
  totals.questionFormats[q.format]=(totals.questionFormats[q.format]||0)+1;
  totals.levels[q.level]=(totals.levels[q.level]||0)+1;
  if(!validFormats.has(q.format))issue('Invalid question format '+q.id);
  if(qids.has(q.id)||seenIds.has(q.id))issue('Duplicate question ID '+q.id);
  qids.add(q.id);seenIds.add(q.id);
  if(!skills.has(q.skillId))issue('Unknown skill ID '+q.id+' '+q.skillId);
  if(!q.solutionSteps?.length)issue('Missing worked solution '+q.id);
  const scope=q.skillId+'/'+q.level;
  if(!byScope.has(scope))byScope.set(scope,[]);
  byScope.get(scope).push(q);
  if(!(q.id in metadata))issue('Missing item metadata '+q.id);
  else totals.metaRecords++;
  if(/original claude-authored/i.test(q.sourceNotes||''))totals.sourceNotesClaimClaude++;
  if(/\bHow many ones are in \d+ tens? and \d+ ones?\b/i.test(q.prompt))totals.ambiguousOnesWording++;
  if(/\b1 tens\b|\b1 ones\b/i.test(q.prompt))totals.singularTensOnes++;
  const exact=[q.prompt,(q.options||[]).map(o=>o.text).slice().sort().join('|'),JSON.stringify(q.answer),q.diagram?.spec?.alt||''].join('§').toLowerCase().replace(/\s+/g,' ').trim();
  const prior=seenExact.get(exact);
  if(prior&&prior.skillId!==q.skillId)totals.exactCrossSkillDuplicateCopies++;
  else if(!prior)seenExact.set(exact,{id:q.id,skillId:q.skillId});
  if(q.diagram){
   totals.diagrams++;
   const src=q.diagram?.spec?.src;
   if(typeof src!=='string'||!src.startsWith('question-banks/assets/math1/')||src.includes('..')){
    issue('Unsafe or incorrect diagram path '+q.id+' → '+src);continue;
   }
   if(!exists(src)){issue('Missing diagram '+q.id+' → '+src);continue;}
   seenPng.add(src);
   const png=fs.readFileSync(path.join(root,src));
   const signature=png.subarray(0,8).toString('hex');
   if(signature!=='89504e470d0a1a0a'||png.readUInt32BE(16)!==720||png.readUInt32BE(20)!==480)
    issue('Incorrect PNG signature/dimensions '+q.id);
   if(!q.diagram.spec.alt?.trim())issue('Missing image alt text '+q.id);
  }
 }
 for(const [scope,questions] of byScope){
  const eligible=questions.filter(q=>q.format==='short-answer'&&!q.diagram&&q.prompt.length<=110&&String(q.answer).length<=18&&!q.prompt.includes('\n'));
  const answerSet=new Set(eligible.map(q=>String(q.answer).trim().toLowerCase()));
  const restricted=answerSet.size<4;
  if(restricted)totals.puzzleMastersRestrictedSkillLevels++;
  perSkill.push({scope,questionCount:questions.length,textOnlyShortAnswers:eligible.length,distinctTextOnlyAnswers:answerSet.size,puzzleMastersRestricted:restricted});
  if(questions.length!==30)issue('Expected 30 questions in '+scope+'; found '+questions.length);
 }
 byUnit.push({unitId:entry.unitId,questions:bank.questions?.length||0,diagrams:totals.diagrams-imageCountBefore,skills:skills.size,adapterValid:valid.ok});
 totals.units++;
 totals.skills+=skills.size;
}
if(totals.questions!==8370||totals.skills!==93||totals.diagrams!==3405)issue('Unexpected total count: '+JSON.stringify(totals));
if(totals.metaRecords!==totals.questions)issue('Question metadata incomplete');
const allOnDisk=fs.readdirSync(path.join(root,'question-banks/assets/math1'),{withFileTypes:true})
 .filter(x=>x.isDirectory()).flatMap(x=>fs.readdirSync(path.join(root,'question-banks/assets/math1',x.name))
 .filter(x=>x.endsWith('.png')).map(y=>'question-banks/assets/math1/'+x.name+'/'+y));
if(allOnDisk.length!==3405)issue('Expected 3,405 PNG assets on disk, found '+allOnDisk.length);
for(const p of allOnDisk)if(!seenPng.has(p))issue('Orphan diagram asset '+p);
editorial.push({code:'EDITORIAL_APPROVAL_PENDING',count:totals.questions,action:'Teacher review of wording, grade-level cognitive demand, and visual quality is still needed.'});
if(totals.singularTensOnes)editorial.push({code:'GRAMMAR_SINGULAR_TENS_ONES',count:totals.singularTensOnes,action:'Correct "1 tens"/"1 ones" in prompts, options and worked solutions (and generator source).'});
if(totals.ambiguousOnesWording)editorial.push({code:'ONES_PLACE_AMBIGUITY',count:totals.ambiguousOnesWording,action:'Specify "ones digit"/"unbundled ones" instead of ambiguous "How many ones are in X tens and Y ones?"'});
if(totals.puzzleMastersRestrictedSkillLevels)editorial.push({code:'PUZZLE_MASTERS_SKILL_FILTER',count:totals.puzzleMastersRestrictedSkillLevels,action:'When a single skill/level is selected, the game needs four distinct text-only short-answer pairs; provide fallback or eligible bank items.'});
if(totals.sourceNotesClaimClaude)editorial.push({code:'PROVENANCE_LABEL',count:totals.sourceNotesClaimClaude,action:'Check whether "Claude-authored" is accurate for all bank items; avoid unsupported provenance statements.'});
const report={status:errors.length?'FAILED':'TECHNICAL_CHECKS_PASSED_EDITORIAL_PENDING',branch:'grade1-question-bank',manifestApproval:false,counts:totals,byUnit,firstRestrictedPairs:perSkill.filter(s=>s.puzzleMastersRestricted).slice(0,35),errors:errors.slice(0,100),editorial};
const loc=path.join(root,'grade1-qa-report.json');
fs.writeFileSync(loc,JSON.stringify(report,null,2));
const summary='# Grade 1 branch-only integration audit\n\n'+
 'Technical result: **'+report.status+'**. Public site unchanged; all 8 units remain **approved: false**.\n\n'+
 '| Measure | Count |\n|---|---:|\n'+
 ['units','skills','questions','diagrams','metaRecords','exactCrossSkillDuplicateCopies','singularTensOnes','ambiguousOnesWording','puzzleMastersRestrictedSkillLevels','sourceNotesClaimClaude'].map(k=>'| '+k+' | '+totals[k]+' |').join('\n')+
 '\n\n## Editorial issues (not mathematical errors)\n\n'+editorial.map(x=>'- **'+x.code+'** ('+x.count+'): '+x.action).join('\n')+
 '\n\n## Technical errors\n\n'+(errors.length?errors.slice(0,25).map(x=>'- '+x).join('\n'):'None.')+'\n';
fs.writeFileSync(path.join(root,'grade1-qa-report.md'),summary);
if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,summary);
console.log(JSON.stringify({status:report.status,counts:totals,errors:errors.slice(0,15),editorial},null,2));
if(errors.length)process.exitCode=1;
