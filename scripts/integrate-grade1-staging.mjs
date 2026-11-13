/* Branch-only artifact integration. Deliberately absent from default/public builds. */
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
export function integrate({source,out}){
 const branch=execFileSync('git',['branch','--show-current'],{cwd:source,encoding:'utf8'}).trim();
 if(branch!=='grade1-question-bank')throw Error('Grade 1 staging requires grade1-question-bank; never run against main');
 const manifest=JSON.parse(fs.readFileSync(path.join(source,'question-banks/math1/manifest.json')));
 if(manifest.review.editorialApproval.approved!==false||manifest.banks.some(b=>b.approved!==false))throw Error('Unexpected Grade 1 approval status');
 const folder=path.join(out,'grade1-staging');fs.mkdirSync(path.join(folder,'banks'),{recursive:true});
 const copy=(from,to)=>{fs.mkdirSync(path.dirname(to),{recursive:true});fs.copyFileSync(path.join(source,from),to);};
 copy('src/grade1-staging-runtime.js',path.join(folder,'runtime.js'));
 const banks=[];
 for(const entry of manifest.banks){
  const rel='question-banks/'+entry.path,bank=JSON.parse(fs.readFileSync(path.join(source,rel)));
  copy(rel,path.join(folder,'banks',entry.unitId+'.json'));
  banks.push({courseId:'math1',unitId:entry.unitId,path:'banks/'+entry.unitId+'.json',approved:false});
  const meta='question-banks/math1/meta/'+entry.unitId+'.meta.json';copy(meta,path.join(out,'elementary/math1/meta',entry.unitId+'.meta.json'));
  for(const q of bank.questions)if(q.diagram){const asset=q.diagram.spec.src;if(!asset.startsWith('question-banks/assets/math1/')||asset.includes('..'))throw Error('Unsafe Grade 1 asset');copy(asset,path.join(out,asset));copy(asset,path.join(out,'elementary',asset));}
 }
 fs.writeFileSync(path.join(folder,'manifest.json'),JSON.stringify({version:1,staging:true,banks},null,2));
 // Load the scoped adapter extension before the native approved-bank bridge starts.
 for(const page of ['worksheet.html','menu-assessment.html','lesson-planner.html','printables.html']){
  const file=path.join(out,'worksheet-generator',page);let text=fs.readFileSync(file,'utf8');
  const match=text.match(/<script src="\.\.\/question-bank-loader\.js[^>]*><\/script>/);if(!match)throw Error('Missing loader in '+page);
  text=text.replace(match[0],match[0]+'\n<script src="../grade1-staging/runtime.js"></script>');fs.writeFileSync(file,text);
 }
 const player=path.join(out,'elementary/worksheet-generator/elementary-resource.js');let code=fs.readFileSync(player,'utf8');
 code=code.replace("for (const file of tools[tool]) {", "if (id==='math1') await script('../../grade1-staging/runtime.js');\n for (const file of tools[tool]) {");fs.writeFileSync(player,code);
 const planner=path.join(out,'worksheet-generator/planner/planner-ui.js');
 let ui=fs.readFileSync(planner,'utf8');
 ui=ui.replace("'discrete', 'grade5'", "'discrete', 'grade1', 'grade2', 'grade3', 'grade4', 'grade5'").replaceAll('|grade5)', '|grade[1-5])');
 fs.writeFileSync(planner,ui);
 const nativeFile=path.join(out,'worksheet-generator/algebra2-bank-native.js');
 let nativeCode=fs.readFileSync(nativeFile,'utf8');
 nativeCode=nativeCode.replaceAll('family: [^)]*_error\\)', 'family: (?:[^)]*_error|err_[^)]*)\\)');
 // `approved` on a native worksheet item is the existing print-control flag,
 // separate from editorial bank approval. Keep it for unedited source keys.
 nativeCode=nativeCode.replace('approved:true,skill:q.skillId',"approved:true,staging:q.id.startsWith('m1-'),skill:q.skillId");
 fs.writeFileSync(nativeFile,nativeCode);
 const menuFile=path.join(out,'worksheet-generator/menu/app.js');
 let menu=fs.readFileSync(menuFile,'utf8');
 menu=menu.replace("var st = p.verify && p.verify.status;", "if (p.staging && NS.isUneditedAlgebra2BankQuestion(p)) return '<span class=\"mm-badge\">Development preview</span>';\n    var st = p.verify && p.verify.status;");
 fs.writeFileSync(menuFile,menu);
 const catalog=path.join(out,'elementary-preload-catalog.js');fs.appendFileSync(catalog,"\nwindow.LIBRARY.courses.filter(c=>c.id==='grade1').forEach(c=>{c.staging=true;c.units.forEach(u=>u.artifacts.forEach(a=>a.description='Grade 1 development preview'));});\n");
 const html=path.join(out,'index.html');fs.writeFileSync(html,fs.readFileSync(html,'utf8').replace('Grades 1–4 question banks are coming soon.','Grade 1 bank available for staging review · Grades 2–4 banks coming soon.'));
 const app=path.join(out,'app.js');fs.writeFileSync(app,fs.readFileSync(app,'utf8').replace("c.preloaded ? units(c.units.length) + ' · resource templates ready · question banks coming soon'", "c.staging ? units(c.units.length) + ' · development preview' : c.preloaded ? units(c.units.length) + ' · resource templates ready · question banks coming soon'"));
 console.log('Grade 1 branch-only staging: eight unapproved banks; native generators, elementary games, flashcards and readiness checks.');
}
