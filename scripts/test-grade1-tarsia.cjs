#!/usr/bin/env node
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const site=path.resolve(process.env.GRADE1_SITE||'../classroom/_site'),manifest=JSON.parse(fs.readFileSync('question-banks/math1/manifest.json'));
const native=require(path.resolve('../classroom/worksheet-generator/menu/tests/load.cjs'))(['games/bank.js','menu/printables.js']);
const all=new Map(),banks=new Map(),skillSets={};
for(const e of manifest.banks){const b=JSON.parse(fs.readFileSync('question-banks/'+e.path));banks.set(e.unitId,b.questions);b.questions.forEach(q=>all.set(q.id,q));skillSets['grade1-'+e.unitId]={unitName:e.unitId};}
const PR=native.MKMENU.printables;
const G={MKMENU:{printables:PR,skillSets,courseLevelName(id,l){return l},grade1StagingQuestion(id,qid){const q=all.get(qid);return {sourceId:qid,prompt:q.prompt,steps:q.solutionSteps.map(t=>({t})),c:4,fig:q.diagram?{src:q.diagram.spec.src,alt:q.diagram.spec.alt}:null};}},MK_GRADE1_STAGING:{content:JSON.parse(fs.readFileSync(path.join(site,'grade1-staging/content-index.json')))},MK_QUESTION_BANKS:{select(o){return banks.get(o.unitId).filter(q=>q.level===o.level&&o.formats.includes(q.format));}}};
vm.runInNewContext(fs.readFileSync(path.join(site,'grade1-staging/printables.js'),'utf8'),{window:G,Set,Map,Math});
const sides=[[0,1],[1,2],[2,0]],norm=G.MK_GRADE1_PRINTABLES.key;
function edge(a,b){return [a.join(','),b.join(',')].sort().join('|');}
function check(B,cfg){
 const E=new Map(),V=new Set(),triangles=new Set(),neighbors=B.pieces.map(()=>[]),labels=new Map(B.items.map(it=>['P'+it.num,it]));
 for(const [i,p] of B.pieces.entries()){
  assert.equal(p.pts.length,3);const triangle=p.pts.map(q=>q.join(',')).sort().join('|');assert(!triangles.has(triangle));triangles.add(triangle);
  for(const [k,[a,b]] of sides.entries()){
   const A=p.pts[a],Z=p.pts[b],dx=Z[0]-A[0]+(Z[1]-A[1])/2,dy=(Z[1]-A[1])*Math.sqrt(3)/2;assert(Math.abs(Math.hypot(dx,dy)-1)<1e-9);
   V.add(A.join(','));V.add(Z.join(','));const id=edge(A,Z);if(!E.has(id))E.set(id,[]);E.get(id).push({piece:i,text:p.text[k],kind:p.kind[k],a:A.join(','),b:Z.join(',')});
  }
 }
 let inside=0;const boundary=new Map(),usedLabels=new Set();
 for(const incidences of E.values()){
  assert(incidences.length===1||incidences.length===2);
  if(incidences.length===1){const x=incidences[0];assert.equal(x.text,'');assert.equal(x.kind,'');for(const [a,b] of [[x.a,x.b],[x.b,x.a]]){if(!boundary.has(a))boundary.set(a,[]);boundary.get(a).push(b);}continue;}
  inside++;const q=incidences.find(x=>x.kind==='q'),a=incidences.find(x=>x.kind==='a');assert(q&&a);const it=labels.get(q.text);assert(it);assert(!usedLabels.has(q.text));usedLabels.add(q.text);assert.equal(a.text,it.edgeAnswer);
  if(it.key.length<=10)assert.equal(it.edgeAnswer,it.key);else assert.equal(B.answerBank.find(x=>x.label===it.edgeAnswer).answer,it.key);
  neighbors[q.piece].push(a.piece);neighbors[a.piece].push(q.piece);
 }
 assert.equal(inside,B.items.length);assert.equal(usedLabels.size,B.items.length);assert.equal(V.size-E.size+B.pieces.length,1);
 const visited=new Set(),queue=[0];while(queue.length){const n=queue.pop();if(visited.has(n))continue;visited.add(n);queue.push(...neighbors[n]);}assert.equal(visited.size,B.pieces.length);
 let corners=0;for(const [point,adj] of boundary){assert.equal(adj.length,2);const p=point.split(',').map(Number),a=adj[0].split(',').map(Number),b=adj[1].split(',').map(Number);if((a[0]-p[0])*(b[1]-p[1])-(a[1]-p[1])*(b[0]-p[0]))corners++;}
 assert.equal(corners,{triangle:3,trapezoid:4,hexagon:6}[B.shape]);
 assert.equal(new Set(B.items.map(it=>norm(it.key))).size,B.items.length);assert.equal(new Set(B.items.map(it=>it.p.sourceId)).size,B.items.length);
 for(const it of B.items){const q=all.get(it.p.sourceId);assert(q);assert(cfg.skills[q.skillId]);assert.equal(q.level,cfg.level);assert.equal(it.p.prompt,q.prompt);assert.equal(it.key,String(q.answer));assert.equal(!!it.p.fig,!!q.diagram);}
 assert.deepEqual([...B.scrambled.map(x=>x.piece)].sort((a,b)=>a-b),Array.from(B.pieces,(p,i)=>i));assert.equal(new Set(B.scrambled.map(x=>x.slot)).size,B.pieces.length);assert(B.scrambled.every(x=>Number.isInteger(x.turn)&&x.turn>=0&&x.turn<3));
}
let scopes=0,available=0,shapes={},sizeChecks=0;const unavailable=[];
for(const [unit,qs] of banks)for(const skill of new Set(qs.map(q=>q.skillId)))for(const level of ['cp2','cp1','honors']){
 const cfg={kind:'tarsia',unitId:'grade1-'+unit,skills:{[skill]:true},level,seed:'geometry-and-answers'};
 for(const size of ['auto','starter','small','medium','large','full']){
  const B=PR.build({...cfg,tarsiaSize:size},0);sizeChecks++;
  if(!B.error){check(B,cfg);assert.equal(JSON.stringify(B),JSON.stringify(PR.build({...cfg,tarsiaSize:size},0)));if(size==='auto'){available++;shapes[B.pieces.length]=(shapes[B.pieces.length]||0)+1;assert(B.pieces.length<=9);}}
  else if(size==='auto')unavailable.push({skill,level,error:B.error});
 }scopes++;
}
// Whole units can also request the larger layouts; validate their exact geometry.
for(const [unit,qs] of banks)for(const size of ['large','full']){const cfg={kind:'tarsia',unitId:'grade1-'+unit,skills:Object.fromEntries([...new Set(qs.map(q=>q.skillId))].map(s=>[s,true])),level:'cp1',seed:'large-layout',tarsiaSize:size},B=PR.build(cfg,0);if(!B.error)check(B,cfg);}
assert.equal(scopes,279);assert(available>260);const result={passed:true,scopes,available,unavailable,shapes,sizeChecks};
fs.mkdirSync('grade1-integration-results',{recursive:true});fs.writeFileSync('grade1-integration-results/tarsia.json',JSON.stringify(result,null,2));console.log(JSON.stringify({...result,unavailable:unavailable.length}));
