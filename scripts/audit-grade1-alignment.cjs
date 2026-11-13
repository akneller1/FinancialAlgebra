#!/usr/bin/env node
'use strict';
/* Read-only skill-level alignment triage across every published Grade 1 item.
 * Findings are *editorial candidates* (not independently established wrong
 * answers). Do not use this script to relabel/publish questions.
 */
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const outline=read('course-outlines/grade1.json');
const GROUPS={
 data:'Data & graphs',time:'Time',geometry:'Shapes & solids',partition:'Equal parts',
 measurement:'Length',place:'Place value & number order',arithmetic:'Addition & subtraction',
 unknown:'Needs human inspection'
};
function category(check){
 if(!check)return 'unknown';
 if(check.k==='key'||check.k==='expr')return 'unknown';
 if(check.fn==='tf')return category(check.inner);
 if(check.fn==='claims')return 'unknown';
 const fn=check.fn||'';
 if(/^(?:tally_|graph_|most_of|sort_)/.test(fn))return 'data';
 if(/^(?:clock|half_hour)/.test(fn))return 'time';
 if(/^(?:partition_|equal_parts)/.test(fn))return 'partition';
 if(/^(?:shape_|solid_name)/.test(fn))return 'geometry';
 if(/^(?:longer|shorter|length|ruler|more_count)/.test(fn))return 'measurement';
 if(/^(?:tens_|ten_ones|teen_parts|digit_value|ones_of|equiv_ones|count_|which_number|symbol|sorted|number_)/.test(fn))return 'place';
 if(/^(?:add|sub|add3|missing_part|related|strategy|eq_text|true_eq|missing_same|equals_word|story_eq|tf_eq)/.test(fn))return 'arithmetic';
 return 'unknown';
}
function isIncompatible(unit,idx,group,q,chk){
 // Only flag questions which have a *provably different* subject. 
 if(unit==='geometry-time'){
  if(idx>=9&&idx<=12)return group!=='unknown'&&group!=='time';
  if(idx>=5&&idx<=8)return group!=='unknown'&&group!=='partition';
  if(idx>=1&&idx<=4)return ['time','measurement','data','place','arithmetic'].includes(group);
 }
 if(unit==='adding-within-100')return ['time','data','geometry','partition','measurement'].includes(group);
 if(unit==='adding-subtracting-working-data'){
  if(idx<=3)return ['data','time','geometry','partition','measurement'].includes(group);
  return ['time','geometry','partition','measurement','place'].includes(group);
 }
 if(unit==='addition-subtraction-story-problems')return ['time','geometry','partition','measurement','place','data'].includes(group);
 if(unit==='adding-subtracting-within-20')return ['time','geometry','partition','measurement','data'].includes(group);
 if(unit==='numbers-to-99')return ['time','geometry','partition','measurement','data'].includes(group);
 if(unit==='length-measurement-120'){
  if(idx===6)return ['time','geometry','partition','measurement','data'].includes(group);
  if(idx<=5||idx===7||idx===8)return ['time','geometry','partition','data','place'].includes(group);
 }
 return false;
}
function strictAdd100(unit,idx,check,q){
 if(unit!=='adding-within-100'||![1,2,4,7].includes(idx))return null;
 if(q.format==='select-all'||q.format==='open-response')return null;
 if(check?.fn!=='add')return null;
 const a=Number(check.a),b=Number(check.b);
 if(!Number.isInteger(a)||!Number.isInteger(b))return null;
 const oneDigit=Math.min(a,b)<10, twoDigits=Math.max(a,b)>=10;
 const bothTwo=a>=10&&b>=10,carry=(a%10)+(b%10)>=10;
 if(idx===1&&!(oneDigit&&twoDigits&&!carry))return 'Expected one 2-digit plus one 1-digit addend without carrying.';
 if(idx===2&&!(bothTwo&&!carry))return 'Expected two 2-digit addends without carrying.';
 if(idx===4&&!(oneDigit&&twoDigits&&carry))return 'Expected one 2-digit and one 1-digit addend composing a ten.';
 if(idx===7&&!(bothTwo&&carry))return 'Expected two 2-digit addends composing a ten.';
 return null;
}
const counts={questions:0,skillLevels:0,derived:0,domainFacts:0,domainFactsExplicitlyOffDomain:0,
 hardMismatch:0,strictAdd100Mismatches:0,needsInspection:0};
const unitSummaries=[],skillRows=[],findings=[];
function flag(code,unit,skill,q,group,fn,reason){
 findings.push({code,unit,skill,questionId:q.id,format:q.format,level:q.level,group,fn,
                prompt:q.prompt.slice(0,300),reason});
}
for(const u of outline.units){
 const bank=read('question-banks/math1/'+u.id+'.json'),checks=read('tools/grade1-authoring/out/'+u.id+'.checks.json');
 const units={unitId:u.id,total:0,hardMismatch:0,strictAdd100Mismatches:0,domainFacts:0,derived:0};
 for(let si=1;si<=u.skills.length;si++){
  const skillId=u.id+'-skill-'+String(si).padStart(2,'0');
  const items=bank.questions.filter(q=>q.skillId===skillId);
  const row={skillId,name:u.skills[si-1],total:items.length,hardMismatch:0,strictAdd100Mismatches:0,domainFacts:0,derived:0,byCategory:{}};
  if(items.length!==90)throw Error(skillId+' has '+items.length+' rather than 90');
  counts.skillLevels+=3;
  for(const q of items){
   counts.questions++;units.total++;
   const chk=checks[q.id]||{},ck=chk.q||{},fn=ck.fn||ck.k;
   const group=category(ck);
   row.byCategory[group]=(row.byCategory[group]||0)+1;
   const isDerived=/-(?:02[5-9]|030)$/.test(q.id);
   if(isDerived){counts.derived++;units.derived++;row.derived++;}
   const isFiller=/facts_(?:oa|nbt|md|g)/i.test(chk.family||'');
   if(isFiller){counts.domainFacts++;units.domainFacts++;row.domainFacts++;}
   const mismatch=isIncompatible(u.id,si,group,q,ck);
   if(mismatch){
    counts.hardMismatch++;units.hardMismatch++;row.hardMismatch++;
    if(isFiller)counts.domainFactsExplicitlyOffDomain++;
    flag('OFF_TARGET_DOMAIN',u.id,skillId,q,group,fn,
       'Skill '+row.name+' does not assess '+GROUPS[group]+'.');
   }
   const strict=strictAdd100(u.id,si,ck,q);
   if(strict){
    counts.strictAdd100Mismatches++;units.strictAdd100Mismatches++;row.strictAdd100Mismatches++;
    flag('WRONG_ADDEND_STRUCTURE',u.id,skillId,q,group,fn,strict);
   }
  }
  skillRows.push(row);
 }
 unitSummaries.push(units);
}
if(counts.questions!==8370)throw Error('Unexpected question count: '+counts.questions);
const report={status:'EDITORIAL_ALIGNMENT_TRIAGE_REQUIRED',counts,units:unitSummaries,
 skillRows,findings,
 explanation:'Narrow deterministic domain checks. Off-target flags identify clear subject mismatches, but do not exhaustively prove grade-level alignment. No content is changed.'};
fs.writeFileSync(path.join(root,'grade1-alignment-report.json'),JSON.stringify(report,null,2));
const top=[...skillRows].sort((a,b)=>(b.hardMismatch+b.strictAdd100Mismatches)-(a.hardMismatch+a.strictAdd100Mismatches)).slice(0,30);
let md='# Grade 1 skill-alignment audit (read-only)\n\n';
md+='**Editorial alignment triage required.** The original mathematics/semantic checks pass, but they do not prove individual questions assess the assigned skill.\n\n';
md+='| Measure | Count |\n|---|---:|\n'+
Object.entries(counts).map(([k,n])=>'| '+k+' | '+n+' |').join('\n')+'\n\n';
md+='## Units\n\n| Unit | Questions | Off-target domain | Wrong addend structure | Generic domain facts | Derived formats |\n|---|---:|---:|---:|---:|---:|\n';
for(const u of unitSummaries)md+='| '+u.unitId+' | '+u.total+' | '+u.hardMismatch+' | '+u.strictAdd100Mismatches+' | '+u.domainFacts+' | '+u.derived+' |\n';
md+='\n## Most affected specific skills\n\n';
for(const row of top)md+='- '+row.skillId+' — '+row.name+': '+row.hardMismatch+' off-domain + '+row.strictAdd100Mismatches+' structurally wrong; '+row.domainFacts+' generic-family questions\n';
md+='\n## Sample likely mismatches\n\n';
for(const f of findings.slice(0,38))md+='- '+f.questionId+' ('+f.skill+'): '+f.prompt.replace(/\s+/g,' ').slice(0,140)+' — '+f.reason+'\n';
md+='\nThis is a **triage report**: no automatic source rewriting, reassignment or bank approval. Carefully replace off-target questions with examples that actually test the specified skill while retaining unit counts and teacher-selected filters.\n';
fs.writeFileSync(path.join(root,'grade1-alignment-report.md'),md);
if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,md.slice(0,14000));
console.log(JSON.stringify({counts,units:unitSummaries,top:top.slice(0,12).map(s=>({id:s.skillId,off:s.hardMismatch,wrong:s.strictAdd100Mismatches,domainFacts:s.domainFacts})),samples:findings.slice(0,8)},null,2));
