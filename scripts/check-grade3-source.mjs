// Grade 3 source preflight: run with node scripts/check-grade3-source.mjs
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd(),read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const outline=read('tools/grade3-authoring/outline.json'),manifest=read('manifest.json');
let errors=[],questions=0,skills=0,diagrams=0;
for(const unit of outline.units){
 const entries=manifest.banks.filter(b=>b.courseId==='math3'&&b.unitId===unit.id);
 if(entries.length!==1||!entries[0].preview)errors.push(unit.id+': missing preview-only manifest registration');
 const file='question-banks/math3/'+unit.id+'.json';
 if(!fs.existsSync(path.join(root,file))){errors.push(file+': missing');continue;}
 const bank=read(file);questions+=bank.questions.length;skills+=unit.skills.length;
 const allowed=new Set(unit.skills.map((_,i)=>unit.id+'-skill-'+String(i+1).padStart(2,'0')));
 for(const q of bank.questions){
  if(!allowed.has(q.skillId))errors.push(q.id+': unknown skill '+q.skillId);
  if(!['cp2','cp1','honors'].includes(q.level))errors.push(q.id+': invalid level');
  if(q.diagram?.type==='image'){
   diagrams++;const src=q.diagram.spec?.src;
   if(!src||src.includes('..')||path.isAbsolute(src)||!fs.existsSync(path.join(root,src)))errors.push(q.id+': missing/unsafe diagram '+src);
  }
 }
 for(const p of ['question-banks/math3/checks/'+unit.id+'.json','worksheet-generator/grade3/flashcards/'+unit.id+'.json','artifacts/math3-'+unit.id+'-cheat-sheet/worksheet.pdf'])
  if(!fs.existsSync(path.join(root,p)))errors.push('Missing '+p);
}
for(const p of ['tools/grade3-authoring/staging/assemble-grade3.mjs','worksheet-generator/grade3-games.html','worksheet-generator/grade3-flashcards.html','worksheet-generator/grade3-understanding-check.html'])
 if(!fs.existsSync(path.join(root,p)))errors.push('Missing '+p);
console.log(JSON.stringify({units:outline.units.length,skills,questions,diagrams,errors:errors.slice(0,30),errorCount:errors.length},null,2));
if(errors.length)process.exitCode=1;
