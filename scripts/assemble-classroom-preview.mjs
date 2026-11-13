/* Compose the development website from the production Classroom shell and engines.
   Source repositories stay separate. Only this deployment artifact is assembled. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const source=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const classroom=path.resolve(process.env.CLASSROOM_SOURCE_DIR||path.join(source,'../classroom'));
const out=path.join(classroom,'_site');
const run=file=>execFileSync(process.execPath,[path.join(classroom,'scripts',file)],{cwd:classroom,stdio:'inherit',env:{...process.env,GRADE5_SOURCE_DIR:source,FINANCIAL_ALGEBRA_SOURCE_DIR:source}});
run('build-site.mjs');run('integrate-approved-courses.mjs');run('integrate-financial-algebra.mjs');
if(!fs.existsSync(path.join(out,'grade5/grade5-main-catalog.js')))throw Error('Preview requires the assembled integrated Grade 5 release');
const outlines=[1,2,3,4].map(n=>JSON.parse(fs.readFileSync(path.join(source,'course-outlines/grade'+n+'.json'),'utf8')));
const colors=['red','orange','orange','green'],arts=['first','second','third','fourth'];
const games=[['math-quest','Math Quest','quest'],['treasure-trail','Treasure Trail','treasure'],['space-explorer','Space Explorer','space'],['math-builders','Math Builders','builders'],['picture-reveal','Picture Reveal','reveal'],['math-race','Math Race','race'],['math-soccer','Math Soccer','soccer'],['connect-four','Connect 4','connect4'],['puzzle-masters','Puzzle Masters','puzzle']];
const generators=[['lesson','Lesson Plan','lesson-planner.html','lesson-planner'],['worksheet','Worksheet','worksheet.html','worksheet-generator'],['activity','Activity','printables.html','printable-generator'],['assessment','Assessment','menu-assessment.html','assessment-generator']];
const courses=outlines.map((c,i)=>({id:'grade'+(i+1),name:c.name,blurb:c.description,color:colors[i],art:arts[i],preloaded:true,units:c.units.map(u=>{
 const query='?course='+c.id+'&unit='+encodeURIComponent(u.id),set='grade'+(i+1)+'-'+u.id;
 const mk=(title,url,type,format,thumb)=>({title,path:url,type,bankFormat:format,thumb,description:'Questions for this unit are coming soon.'});
 const artifacts=generators.map(([mode,title,page,format])=>mk(title+' Generator','worksheet-generator/'+page+'#unit='+set,'Generator',format,'grade5/thumbs/math5-generator-'+mode+'.svg'));
 for(const [id,title,thumb] of games)artifacts.push(mk(title,'elementary/worksheet-generator/elementary-resource.html'+query+'&tool=games&game='+id,'Game',id==='connect-four'?'connect-four':id==='picture-reveal'?'picture-reveal':'topic-games','grade5/thumbs/math5-game-'+thumb+'.svg'));
 if(/fraction/i.test(u.name))artifacts.push(mk('Fraction Frenzy','elementary/worksheet-generator/elementary-resource.html'+query+'&tool=games&game=fraction-frenzy','Game','topic-games','grade5/thumbs/math5-game-frenzy.svg'));
 artifacts.push({...mk('Error Analysis','worksheet-generator/printables.html#unit='+set+'&kind=error','Generator','printable-generator','grade5/thumbs/math5-generator-activity.svg'),visibleInBrowse:true});
 artifacts.push(mk('Flashcards','elementary/worksheet-generator/elementary-resource.html'+query+'&tool=flashcards','Study Guide','flashcards','grade5/thumbs/math5-flashcards.svg'));
 artifacts.push(mk('Understanding Check','elementary/worksheet-generator/elementary-resource.html'+query+'&tool=check','Study Guide','interactive-practice-test','grade5/thumbs/math5-understanding-check.svg'));
 return {id:u.id,name:u.name,artifacts};
})}));
const skillData=Object.fromEntries(outlines.map((c,i)=>['grade'+(i+1),Object.fromEntries(c.units.map(u=>[u.id,u.skills]))]));
// The Grade 4 authoring package is optional while its native bank is not yet
// integrated. Import the assembler only when approved Grade 4 banks actually
// exist; fail explicitly if approval is set but its staging module is absent.
const manifest=JSON.parse(fs.readFileSync(path.join(source,'manifest.json'),'utf8'));
const approvedGrade4Banks=manifest.banks.filter(b=>b.courseId==='math4'&&b.approved===true);
if(approvedGrade4Banks.length){
 const assembler=path.join(source,'tools/grade4-authoring/staging/assemble-grade4.mjs');
 if(!fs.existsSync(assembler))throw Error('Approved Grade 4 banks require '+assembler+'; refusing to publish incomplete Grade 4 resources');
 const {assembleGrade4,grade4Ready}=await import(new URL('../tools/grade4-authoring/staging/assemble-grade4.mjs',import.meta.url));
 if(!grade4Ready(source))throw Error('Grade 4 banks approved but staging assembler reports course not ready');
 const g4=assembleGrade4({source,out}),i=courses.findIndex(c=>c.id==='grade4');
 skillData.grade4=g4.skills;delete g4.skills;courses[i]=g4;
}
// Grade 3 is available only in this noindex development build.
const previewGrade3=manifest.banks.filter(b=>b.courseId==='math3'&&(b.preview===true||b.approved===true));
if(previewGrade3.length){
 const assembler=path.join(source,'tools/grade3-authoring/staging/assemble-grade3.mjs');
 if(!fs.existsSync(assembler))throw Error('Grade 3 preview banks require '+assembler);
 const {assembleGrade3,grade3Ready}=await import(new URL('../tools/grade3-authoring/staging/assemble-grade3.mjs',import.meta.url));
 if(!grade3Ready(source))throw Error('Grade 3 staging assembler reports course not ready');
 const g3=assembleGrade3({source,out}),i=courses.findIndex(c=>c.id==='grade3');
 skillData.grade3=g3.skills;delete g3.skills;courses[i]=g3;
}
// Grade 2 is staged only when its complete preview package is present.
const previewGrade2=manifest.banks.filter(b=>b.courseId==='math2'&&(b.preview===true||b.approved===true));
if(previewGrade2.length){
 if(previewGrade2.length!==12 || new Set(previewGrade2.map(b=>b.unitId)).size!==12)throw Error('Grade 2 preview requires exactly 12 distinct unit banks');
 if(previewGrade2.some(b=>b.approved!==false||b.preview!==true))throw Error('Grade 2 must remain unapproved preview content in staging');
 for(const b of previewGrade2){
   if(typeof b.path!=='string'||!b.path.startsWith('question-banks/math2/')||b.path.includes('..')||!fs.existsSync(path.join(source,b.path)))throw Error('Missing or unsafe Grade 2 preview bank '+b.unitId);
 }
 const assembler=path.join(source,'tools/grade2-authoring/staging/assemble-grade2.mjs');
 if(!fs.existsSync(assembler))throw Error('Grade 2 preview banks require '+assembler);
 const {assembleGrade2,grade2Ready}=await import(new URL('../tools/grade2-authoring/staging/assemble-grade2.mjs',import.meta.url));
 if(!grade2Ready(source))throw Error('Grade 2 staging assembler reports course not ready');
 const g2=assembleGrade2({source,out}),i=courses.findIndex(c=>c.id==='grade2');
 if(i<0)throw Error('Grade 2 course placeholder missing');
 skillData.grade2=g2.skills;delete g2.skills;courses[i]=g2;
}
const approvedGrades=courses.filter(c=>c.approved).map(c=>c.id.slice(5)),pendingGrades=courses.filter(c=>!c.approved).map(c=>c.id.slice(5));
const catalog=`/* Development artifact: production Classroom renderer, preloaded elementary courses. */\n(function(G){var courses=${JSON.stringify(courses)},skills=${JSON.stringify(skillData)};G.MK_ELEMENTARY_PRELOAD=courses;G.LIBRARY.courses=G.LIBRARY.courses.filter(c=>!courses.some(p=>p.id===c.id)).concat(courses);var C=G.MK_COURSE_CATALOG,old=C.getSkills,records=C.getSkillRecords;C.getSkills=function(c,u){return skills[c]&&skills[c][u]?skills[c][u].slice():old(c,u)};C.getSkillRecords=function(c,u){return skills[c]&&skills[c][u]?skills[c][u].map((name,i)=>({id:u+'-skill-'+String(i+1).padStart(2,'0'),name,index:i+1})):records(c,u)};G.LIBRARY.courses.forEach(c=>c.units.forEach(u=>u.artifacts.forEach(a=>{for(var k of ['path','thumb'])if(typeof a[k]==='string')a[k]=a[k].replace(/^\\/grade5\\//,'grade5/')})));})(window);\n`;
fs.writeFileSync(path.join(out,'elementary-preload-catalog.js'),catalog);
fs.copyFileSync(path.join(source,'src/classroom-preload-runtime.js'),path.join(out,'worksheet-generator/elementary-preload-runtime.js'));
// Use the production app, with only development visibility/routes added.
const appFile=path.join(out,'app.js');let app=fs.readFileSync(appFile,'utf8');
app=app.replace('  L.courses = L.courses.filter',"  SOON = SOON.filter(function(c){return !L.courses.some(function(p){return p.id===c.id&&!p.comingSoon;});});\n  L.courses = L.courses.filter");
app=app.replace('  function unitView(c, u) {','  function unitView(c, u) {\n    if (c.preloaded) return algebraUnitView(c, u);');
if(!app.includes('if (c.preloaded) return algebraUnitView'))throw Error('Classroom unit renderer changed; update preview integration');
app=app.replace("['grade5','financial-algebra'].includes(it.c.id)","['grade1','grade2','grade3','grade4','grade5','financial-algebra'].includes(it.c.id)");
app=app.replace("if (/^https:\\/\\//i.test(path)","if (/^elementary\\//.test(path) || /^grade[1-5]\\//.test(path)) return path; if (/^https:\\/\\//i.test(path)");
// Approved elementary courses (Grade 4) list their unit projects the way released Grade 5 does.
app=app.replace("(c.id === 'grade5' ? category('projects', 'Projects', ['other'])","((c.id === 'grade5' || c.approved) ? category('projects', 'Projects', ['other'])");
app=app.replace("var items = u ? u.artifacts : (c && c.id === 'grade5'", "var items = u ? u.artifacts : (c && (c.id === 'grade5' || c.preloaded)");
app=app.replace("(c.planned ? units(c.units.length)", "(c.preloaded ? units(c.units.length) + (c.approved ? ' · ' + c.approved : ' · resource templates ready · question banks coming soon') : c.planned ? units(c.units.length)");
fs.writeFileSync(appFile,app);
const htmlFile=path.join(out,'index.html');let html=fs.readFileSync(htmlFile,'utf8');
html=html.replace('<script src="app.js','<script src="elementary-preload-catalog.js?v=integrated-model-20261113"></script>\n<script src="app.js');
html=html.replace('</head>','<meta name="robots" content="noindex,nofollow">\n</head>');
html=html.replace(/(<a class="brand"[^>]*href=")[^"]+(")/, '$1./index.html$2');
html=html.replace('<main id="main"','<p style="margin:10px auto;max-width:1200px;padding:10px 20px;background:#fff4d6;border-radius:8px">Development preview · '+(approvedGrades.length?'Grade '+approvedGrades.join(', ')+' has approved question banks. ':'')+'Grades '+pendingGrades[0]+'–'+pendingGrades[pendingGrades.length-1]+' question banks are coming soon.</p>\n<main id="main"');
fs.writeFileSync(htmlFile,html);
for(const page of ['worksheet.html','menu-assessment.html','lesson-planner.html','printables.html','vocabulary.html']){
 const file=path.join(out,'worksheet-generator',page);if(!fs.existsSync(file))continue;
 let text=fs.readFileSync(file,'utf8');
 // Register outlined skills before native discovery/scopes, then initialize pending unit controls after native bank loading.
 text=text.replace('<script src="../course-catalog.js', '<script src="../course-catalog.js');
 const match=text.match(/<script src="\.\.\/course-catalog\.js[^>]*><\/script>/);
 if(!match)throw Error('Missing shared course catalog in '+page);
 text=text.replace(match[0],match[0]+'\n<script src="../elementary-preload-catalog.js?v=integrated-model-20261113"></script>');
 const native=text.match(/<script src="algebra2-bank-native\.js[^>]*><\/script>/);
 if(native)text=text.replace(native[0],native[0]+'\n<script src="elementary-preload-runtime.js?v=integrated-model-20261113-3"></script>');
 text=text.replace('</head>','<meta name="robots" content="noindex,nofollow"></head>');
 fs.writeFileSync(file,text);
}
// Shared games and study tools also load the full approved manifest. Register
// elementary skills there before their adapters initialize, just as in generators.
for(const page of fs.readdirSync(path.join(out,'worksheet-generator')).filter(name=>name.endsWith('.html'))){
 const file=path.join(out,'worksheet-generator',page);
 let text=fs.readFileSync(file,'utf8');
 if(text.includes('elementary-preload-catalog.js'))continue;
 const match=text.match(/<script src="\.\.\/course-catalog\.js[^>]*><\/script>/);
 if(!match)continue;
 text=text.replace(match[0],match[0]+'\n<script src="../elementary-preload-catalog.js?v=shared-activities-20261113"></script>');
 fs.writeFileSync(file,text);
}
// Keep a requested empty vocabulary unit selected instead of substituting Algebra 1.
const vocabularyFile=path.join(out,'worksheet-generator/vocabulary-builder.js');
let vocabulary=fs.readFileSync(vocabularyFile,'utf8');
vocabulary=vocabulary.replace('u=>bankText(u[0])','u=>bankText(u[0])||/^grade[1-4]-/.test(u[0])');
fs.writeFileSync(vocabularyFile,vocabulary);
const vocabularyPage=path.join(out,'worksheet-generator/vocabulary.html');
fs.writeFileSync(vocabularyPage,fs.readFileSync(vocabularyPage,'utf8').replace(/vocabulary-builder\.js[^"]*/g,'vocabulary-builder.js?v=elementary-preload-3'));

// Package only shared elementary players and outlines; no standalone course renderer is used for browsing.
const elementary=path.join(out,'elementary');fs.mkdirSync(elementary,{recursive:true});
const copy=rel=>{const to=path.join(elementary,rel);fs.mkdirSync(path.dirname(to),{recursive:true});fs.copyFileSync(path.join(source,rel),to)};
for(const rel of ['worksheet-generator/elementary-resource.html','worksheet-generator/elementary-resource.js','question-bank-adapter.js','question-bank-loader.js','src/outline-template.js','src/elementary-resources.js','assets/favicon.svg','worksheet-generator/core/math-display.js','worksheet-generator/core/math-display.css','worksheet-generator/games/skill-setup.js'])copy(rel);
fs.cpSync(path.join(source,'worksheet-generator/grade5'),path.join(elementary,'worksheet-generator/grade5'),{recursive:true});
for(let grade=1;grade<=4;grade++){
 copy('course-outlines/grade'+grade+'.json');
 const redirect=prefix=>`<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex"><script>var u=location.hash.replace(/^#(?:math|grade)[1-4]\\.?/,'');location.replace('${prefix}#grade${grade}'+(u?'.'+u:''));</script></head><body><a href="${prefix}#grade${grade}">Open Grade ${grade}</a></body></html>`;
 fs.writeFileSync(path.join(out,'grade'+grade+'.html'),redirect('./'));
 fs.writeFileSync(path.join(elementary,'grade'+grade+'.html'),redirect('../'));
}
// Adapt future approved banks once, just as integrated Grade 5 does today.
const nativePath=path.join(out,'question-banks/manifest.json'),native=JSON.parse(fs.readFileSync(nativePath,'utf8'));
const scoped=[];
for(const entry of manifest.banks.filter(b=>/^math[1-4]$/.test(b.courseId)&&(b.approved===true||((b.courseId==='math3'||b.courseId==='math2')&&b.preview===true)))){
 const bank=JSON.parse(fs.readFileSync(path.join(source,entry.path),'utf8')),gradeId=entry.courseId.replace('math','grade');
 const target='question-banks/'+gradeId+'/'+entry.unitId+'.json';
 const adapted=structuredClone(bank);adapted.courseId=gradeId;
 for(const q of adapted.questions)if(q.diagram?.type==='image'){
  const rel=q.diagram.spec.src;
  if(rel.includes('..')||path.isAbsolute(rel))throw Error('Unsafe bank diagram '+rel);
  const to=rel.replace(/^question-banks\/assets\/math([23])\//,(_,n)=>'question-banks/assets/grade'+n+'/');fs.mkdirSync(path.dirname(path.join(out,to)),{recursive:true});fs.copyFileSync(path.join(source,rel),path.join(out,to));q.diagram.spec.src=to;
 }
 fs.mkdirSync(path.dirname(path.join(out,target)),{recursive:true});fs.writeFileSync(path.join(out,target),JSON.stringify(adapted));
 native.banks=native.banks.filter(b=>!(b.courseId===gradeId&&b.unitId===entry.unitId));native.banks.push({courseId:gradeId,unitId:entry.unitId,path:target,approved:true});
 copy(entry.path);scoped.push(entry);
 for(const q of bank.questions)if(q.diagram?.type==='image')copy(q.diagram.spec.src);
 const meta=bank.courseId+'/meta/'+entry.unitId+'.meta.json';if(fs.existsSync(path.join(source,meta)))copy(meta);
}
fs.writeFileSync(nativePath,JSON.stringify(native,null,2)+'\n');
fs.writeFileSync(path.join(elementary,'manifest.json'),JSON.stringify({version:1,banks:scoped},null,2));
// Every direct legacy generator URL also resolves to the native Classroom generator.
let player=fs.readFileSync(path.join(elementary,'worksheet-generator/elementary-resource.html'),'utf8');
player=player.replace('</head>',`<script>(function(){var p=new URLSearchParams(location.search);if(p.get('tool')!=='generators')return;var pages={lesson:'lesson-planner.html',worksheet:'worksheet.html',activity:'printables.html',assessment:'menu-assessment.html'};var mode=p.get('mode')||'lesson',course=(p.get('course')||'').replace('math','grade');if(pages[mode])location.replace('../../worksheet-generator/'+pages[mode]+'#unit='+course+'-'+p.get('unit')+(mode==='activity'?'&kind='+(p.get('kind')||'maze'):''));})();</script></head>`);
fs.writeFileSync(path.join(elementary,'worksheet-generator/elementary-resource.html'),player);
const sha=execFileSync('git',['rev-parse','HEAD'],{cwd:classroom,encoding:'utf8'}).trim();
fs.writeFileSync(path.join(out,'development-build.json'),JSON.stringify({model:'integrated-classroom-grade5',classroomCommit:sha,courses:courses.map(c=>c.id),units:courses.reduce((n,c)=>n+c.units.length,0),nativeGenerators:generators.map(g=>g[2])},null,2));
console.log('Development preview assembled from Classroom '+sha+': '+courses.reduce((n,c)=>n+c.units.length,0)+' preloaded units ('+courses.filter(c=>c.approved).map(c=>c.id).join(', ')+' with approved banks); native generators and integrated Grade 5 renderer.');
