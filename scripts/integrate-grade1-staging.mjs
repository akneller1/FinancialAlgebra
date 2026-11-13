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
 const banks=[],content={};
 function canonical(value){
  if(Array.isArray(value))return value.map(canonical);
  if(value&&typeof value==='object')return Object.fromEntries(Object.keys(value).sort().filter(k=>!['person','color','caption'].includes(k)).map(k=>[k,canonical(value[k])]));
  return value;
 }
 for(const entry of manifest.banks){
  const rel='question-banks/'+entry.path,bank=JSON.parse(fs.readFileSync(path.join(source,rel)));
  const checks=JSON.parse(fs.readFileSync(path.join(source,'tools/grade1-authoring/out',entry.unitId+'.checks.json')));
  bank.questions.forEach(q=>{content[q.id]=JSON.stringify(canonical(checks[q.id].q||checks[q.id].parts));});
  copy(rel,path.join(folder,'banks',entry.unitId+'.json'));
  banks.push({courseId:'math1',unitId:entry.unitId,path:'banks/'+entry.unitId+'.json',approved:false});
  const meta='question-banks/math1/meta/'+entry.unitId+'.meta.json';copy(meta,path.join(out,'elementary/math1/meta',entry.unitId+'.meta.json'));
  for(const q of bank.questions)if(q.diagram){const asset=q.diagram.spec.src;if(!asset.startsWith('question-banks/assets/math1/')||asset.includes('..'))throw Error('Unsafe Grade 1 asset');copy(asset,path.join(out,asset));copy(asset,path.join(out,'elementary',asset));}
 }
 fs.writeFileSync(path.join(folder,'manifest.json'),JSON.stringify({version:1,staging:true,banks},null,2));
 fs.writeFileSync(path.join(folder,'content-index.json'),JSON.stringify(content));
 copy('src/grade1-printables-staging.js',path.join(folder,'printables.js'));
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
 nativeCode=nativeCode.replace('const generate=NS.generateProblem;',"NS.grade1StagingQuestion=function(id,qid){const q=raw.get(qid);return /^grade1-/.test(id)&&isBank(id)&&q&&NS.skillSets[id].byId[q.skillId]?problem(q,id,NS.LEVELS[q.level].tiers[1]):null;};\nconst generate=NS.generateProblem;");
 fs.writeFileSync(nativeFile,nativeCode);
 const printablePage=path.join(out,'worksheet-generator/printables.html');
 let printableHtml=fs.readFileSync(printablePage,'utf8');
 printableHtml=printableHtml.replace(/(<script src="menu\/printables-ui\.js[^>]*>)/,'<script src="../grade1-staging/printables.js"></script>\n<script>(function(){var p=new URLSearchParams(location.hash.slice(1));if((p.get("unit")||"").startsWith("grade1-")&&["match","matching"].includes(p.get("kind"))){p.set("kind","answer-match");history.replaceState(null,"","#"+p);}})();</script>\n$1');
 fs.writeFileSync(printablePage,printableHtml);
 const printableEngine=path.join(out,'worksheet-generator/menu/printables.js');
 let engineCode=fs.readFileSync(printableEngine,'utf8');
 engineCode=engineCode.replace('PR.buildWho = function (cfg, vIdx) {','PR.buildWho = function (cfg, vIdx, grade1Items) {').replace("var items = gather(cfg, vIdx, 10, 'who',", "var items = (/^grade1-/.test(cfg.unitId)&&grade1Items) || gather(cfg, vIdx, 10, 'who',");
 fs.writeFileSync(printableEngine,engineCode);
 const printableUI=path.join(out,'worksheet-generator/menu/printables-ui.js');
 let printableCode=fs.readFileSync(printableUI,'utf8');
 printableCode=printableCode.replace('  function whoPages(cfg, B, v, nV, key) {','  function whoPages(cfg, B, v, nV, key) {\n    if(B.grade1Who)return G.MK_GRADE1_PRINTABLES.whoPages(cfg,B,v,nV,key);');
 printableCode=printableCode.replace("var fs = large ? 13 : (sIn > 1.6 ? 8 : 7.4);", "var fs = B.grade1Tarsia ? (large ? 16 : (sIn > 1.6 ? 14 : 11)) : (large ? 13 : (sIn > 1.6 ? 8 : 7.4));");
 printableCode=printableCode.replace("story + st + (kind === 'tarsia'", "story + st + (kind==='tarsia'&&/^grade1-/.test(unit)?G.MK_GRADE1_PRINTABLES.tarsiaOptions(cfg):'') + (kind === 'tarsia'");
 printableCode=printableCode.replace("if ($('#prTarsiaLayout'))", "if ($('#prTarsiaSize')) $('#prTarsiaSize').onchange=function(e){cfg.tarsiaSize=e.target.value;save();rebuild();};\n    if ($('#prTarsiaLayout'))");
 printableCode=printableCode.replace('  function tarsiaPages(cfg, B, v, nV, key) {', `  function tarsiaPages(cfg, B, v, nV, key) {
    if(B.grade1Tarsia){
      var layout=cfg.tarsiaLayout||'standard',sections=layout==='large'?Math.ceil(B.pieces.length/6):1,covers=[];
      for(var section=0;section<sections;section++)covers.push({nofoot:true,html:'<div class="mm-body pc pt">'+tarsiaHead(cfg,nV,v,unitName(cfg)+' Tarsia'+(key?' · Teacher key':''),B.shape+' · '+B.pieces.length+' pieces · '+B.items.length+' matches',!key)+(section===0?'<p style="font-size:15px;margin:6px 0">'+(key?'Solved puzzle. Each P-edge touches its correct answer.':'Solve the numbered problems. P1 means Problem 1. Match touching edges and build the '+B.shape+'. Blank edges go outside. C-codes use the answer bank.')+'</p>':'')+'<div class="pr-tbox">'+tarsiaSvg(B,key,layout,section)+'</div></div>'});
      return G.MK_GRADE1_PRINTABLES.tarsiaPages(cfg,B,v,nV,key,covers);
    }
  `);
 printableCode=printableCode.replace("sc.groups.forEach(function (g) { out += '<g fill=", "sc.groups.forEach(function (g, gi) { out += '<g fill=");
 printableCode=printableCode.replace('PR.SCENE_COLORS[g.color]', 'PR.SCENE_COLORS[B.grade1Color?B.colorOf[B.groupNum[gi]-1]:g.color]');
 printableCode=printableCode.replace('.test(g.color)', '.test(B.grade1Color?B.colorOf[B.groupNum[gi]-1]:g.color)');
 printableCode=printableCode.replace('  function colorPages(cfg, B, v, nV, key) {',
  '  function colorPages(cfg, B, v, nV, key) {\n    if(B.grade1Color){var cover={nofoot:true,brand:true,html:\'<div class="mm-body pc">\'+nameDate(key)+\'<div class="pc-ctitle">\'+esc(unitName(cfg)+\": Color By Number\")+\'</div><div class="pc-sbox">\'+sceneSvg(B,key)+\'</div>\'+colorCode(B,key)+\'</div>\'};return G.MK_GRADE1_PRINTABLES.colorPages(cfg,B,v,nV,key,cover);}');
 printableCode=printableCode.replace('  PR.pageEls = function',"  var originalPages=PR.pages;PR.pages=function(cfg,B,v,nV,key){return B.grade1Staging?G.MK_GRADE1_PRINTABLES.pages(cfg,B,v,nV,key):originalPages.apply(this,arguments);};\n  PR.pageEls = function");
 fs.writeFileSync(printableUI,printableCode);
 const menuFile=path.join(out,'worksheet-generator/menu/app.js');
 let menu=fs.readFileSync(menuFile,'utf8');
 menu=menu.replace("var st = p.verify && p.verify.status;", "if (p.staging && NS.isUneditedAlgebra2BankQuestion(p)) return '<span class=\"mm-badge\">Development preview</span>';\n    var st = p.verify && p.verify.status;");
 fs.writeFileSync(menuFile,menu);
 const catalog=path.join(out,'elementary-preload-catalog.js');fs.appendFileSync(catalog,"\nwindow.LIBRARY.courses.filter(c=>c.id==='grade1').forEach(c=>{c.staging=true;c.units.forEach(u=>u.artifacts.forEach(a=>a.description='Grade 1 development preview'));});\n");
 const html=path.join(out,'index.html');fs.writeFileSync(html,fs.readFileSync(html,'utf8').replace('Grades 1–4 question banks are coming soon.','Grade 1 bank available for staging review · Grades 2–4 banks coming soon.'));
 const app=path.join(out,'app.js');fs.writeFileSync(app,fs.readFileSync(app,'utf8').replace("c.preloaded ? units(c.units.length) + ' · resource templates ready · question banks coming soon'", "c.staging ? units(c.units.length) + ' · development preview' : c.preloaded ? units(c.units.length) + ' · resource templates ready · question banks coming soon'"));
 console.log('Grade 1 branch-only staging: eight unapproved banks; native generators, elementary games, flashcards and readiness checks.');
}
