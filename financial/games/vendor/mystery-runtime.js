(function(CASE){


/* compound inequality answers: parsed into a true/false test for any x, then compared with the key */
function ineqPred(raw){
  const s=String(raw==null?'':raw).toLowerCase().replace(/[−–—]/g,'-').replace(/≤/g,'<=').replace(/≥/g,'>=').replace(/=</g,'<=').replace(/=>/g,'>=').replace(/\s+/g,'');
  if(!s) return null;
  const num=t=>{ if(/^[-+]?\d+(\.\d+)?$/.test(t)) return parseFloat(t); const m=t.match(/^([-+]?\d+)\/(\d+)$/); return m&&+m[2]?parseInt(m[1],10)/parseInt(m[2],10):NaN; };
  const clauses=[];
  for(const c of s.split('or')){
    const atoms=[];
    for(const a of c.split('and')){
      const parts=a.split(/(<=|>=|<|>)/);
      if(parts.length<3||parts.length%2===0) return null;
      const ops=[], opd=[];
      for(let i=0;i<parts.length;i++){
        if(i%2){ ops.push(parts[i]); continue; }
        if(parts[i]==='x') opd.push('x'); else { const v=num(parts[i]); if(isNaN(v)) return null; opd.push(v); }
      }
      if(!opd.includes('x')) return null;
      atoms.push({ops,opd});
    }
    clauses.push(atoms);
  }
  return xv=>clauses.some(atoms=>atoms.every(a=>{
    for(let i=0;i<a.ops.length;i++){
      const L=a.opd[i]==='x'?xv:a.opd[i], R=a.opd[i+1]==='x'?xv:a.opd[i+1], o=a.ops[i];
      if(!(o==='<'?L<R:o==='<='?L<=R:o==='>'?L>R:L>=R)) return false;
    }
    return true;
  }));
}
function ineqCheck(raw,A){
  const f=ineqPred(raw);
  if(!f) return {ok:false,parse:true,msg:"I couldn't read that. Write it like 0 < x ≤ 9, or x < -1 or x ≥ 8. You can use the symbol buttons."};
  const g=ineqPred(A.v), bad=[];
  for(let k=-80;k<=80;k++){ const p=k/2; if(f(p)!==g(p)) bad.push(p); }
  if(!bad.length) return {ok:true};
  if(bad.every(Number.isInteger)) return {ok:false,msg:'Close! Check each endpoint: use < or > when the number is NOT included, and <= or >= when it IS included.'};
  const wantOr=A.v.indexOf('or')>=0, gotOr=String(raw).toLowerCase().indexOf('or')>=0;
  if(wantOr&&!gotOr) return {ok:false,msg:'This problem has two separate pieces. Join them with OR.'};
  if(!wantOr&&gotOr) return {ok:false,msg:'Both conditions must be true at the same time. Write one inequality like a < x < b.'};
  if(A.flip) return {ok:false,msg:'Not quite. Remember: multiplying or dividing by a negative number reverses the inequality symbol.'};
  return {ok:false,msg:'Not quite. Check your work and try again.'};
}

/* ---------- general typed-answer engine ---------- */
const SUP={'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'-'};
function nrm(s){
  s=String(s==null?'':s).toLowerCase();
  s=s.replace(/[−–—]/g,'-').replace(/[×·⋅]/g,'*').replace(/÷/g,'/').replace(/[ ]/g,' ');
  s=s.replace(/([⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)/g,m=>'^'+m.split('').map(c=>SUP[c]).join(''));
  s=s.replace(/π/g,'pi').replace(/√/g,'sqrt').replace(/°/g,'').replace(/\s+/g,'');
  s=s.replace(/degrees?|deg/g,'');
  return s;
}
function tokenize(s){
  const t=[];let i=0;
  while(i<s.length){
    const c=s[i];
    if(/[0-9.]/.test(c)){let j=i;while(j<s.length&&/[0-9.]/.test(s[j]))j++;const n=parseFloat(s.slice(i,j));if(isNaN(n))throw 0;t.push({k:'n',v:n});i=j;}
    else if(c==='p'&&s.startsWith('pi',i)){t.push({k:'n',v:Math.PI,pi:1});i+=2;}
    else if(c==='s'&&s.startsWith('sqrt',i)){t.push({k:'f'});i+=4;}
    else if(c==='x'||c==='y'){t.push({k:'v',v:c});i++;}
    else if('+-*/^()'.includes(c)){t.push({k:'o',v:c});i++;}
    else throw 0;
  }
  return t;
}
function parseExpr(s){
  const T=tokenize(s);let p=0;
  const peek=()=>T[p];
  const startsAtom=t=>t&&(t.k==='n'||t.k==='v'||t.k==='f'||(t.k==='o'&&t.v==='('));
  function expr(){let l=term();while(peek()&&peek().k==='o'&&(peek().v==='+'||peek().v==='-')){const o=T[p++].v;const r=term();l=o==='+'?add(l,r):sub(l,r);}return l;}
  function term(){let l=unary();for(;;){const t=peek();if(!t)break;if(t.k==='o'&&(t.v==='*'||t.v==='/')){p++;const r=unary();l=t.v==='*'?mul(l,r):div(l,r);}else if(startsAtom(t)){const r=unary();l=mul(l,r);}else break;}return l;}
  function unary(){const t=peek();if(t&&t.k==='o'&&(t.v==='-'||t.v==='+')){p++;const u=unary();return t.v==='-'?neg(u):u;}return power();}
  function power(){const b=atom();const t=peek();if(t&&t.k==='o'&&t.v==='^'){p++;const e=unary();return pw(b,e);}return b;}
  function atom(){
    const t=T[p++];if(!t)throw 0;
    if(t.k==='n')return ()=>t.v;
    if(t.k==='v')return env=>{const v=env[t.v];if(v===undefined)throw 0;return v;};
    if(t.k==='f'){const a=atom();return env=>Math.sqrt(a(env));}
    if(t.k==='o'&&t.v==='('){const e=expr();const c=T[p++];if(!c||c.v!==')')throw 0;return e;}
    throw 0;
  }
  const add=(a,b)=>e=>a(e)+b(e),sub=(a,b)=>e=>a(e)-b(e),mul=(a,b)=>e=>a(e)*b(e),div=(a,b)=>e=>a(e)/b(e),neg=a=>e=>-a(e),pw=(a,b)=>e=>Math.pow(a(e),b(e));
  const f=expr();if(p!==T.length)throw 0;return f;
}
const PTS=[1.7,2.3,3.1,0.6,-0.9,-2.4,4.6];
function same(f,g,vars){
  for(const x of PTS){const env={x:x,y:x*0.37+1.1};const a=f(env),b=g(env);if(!isFinite(a)||!isFinite(b)||Math.abs(a-b)>1e-6*Math.max(1,Math.abs(a),Math.abs(b)))return false;}
  return true;
}
function val(s){return parseExpr(nrm(s))({x:0,y:0});}
function valNum(s){const v=parseExpr(s)({});return v;}
function stripUnits(s){return s.replace(/(squareunits|squnits|squarefeet|squareinches|cubicunits|units?|feet|foot|ft|miles?|mi|inches|in|cm|meters?|m)(\^?\d)?$/,'');}
function stripLhs(s){return s.replace(/^[a-z]\s*=\s*/,'');}
function expandPM(s){ // "3±sqrt5" -> ["3+sqrt5","3-sqrt5"]; "±4" -> ["4","-4"]
  s=s.replace(/±/g,'±');const i=s.indexOf('±');if(i<0)return [s];
  const a=s.slice(0,i),b=s.slice(i+1);return [a+'+'+b,a+'-'+b].map(z=>z.replace(/^\+/,''));
}
function closeTo(a,b,tol){return isFinite(a)&&Math.abs(a-b)<=(tol!=null?tol:1e-6*Math.max(1,Math.abs(b)));}
const BAD='Not quite. Check your work and try again.';
function pe(msg){return {ok:false,parse:true,msg:msg||"I couldn't read that. Check the format shown under the answer box."};}
function checkNum(raw,a){
  let s=nrm(String(raw).replace(/(\d),(?=\d{3}(?!\d))/g,'$1').replace(/\s*%\s*$/,'')).replace(/:/g,'/');
  s=stripLhs(stripUnits(s)); if(!s)return pe();
  let v;try{v=parseExpr(s)({});}catch(e){return pe();}
  const want=parseExpr(nrm(a.v))({});
  if(!closeTo(v,want,a.tol))return {ok:false,msg:BAD};
  if(a.exact&&!/pi|sqrt/.test(nrm(raw)))return {ok:false,msg:'That is the right size, but leave your answer exact: use π or a radical (√) instead of a decimal.'};
  return {ok:true};
}
function parseList(raw){
  let s=String(raw==null?'':raw).toLowerCase().replace(/\s+(or|and)\s+/g,',').replace(/;/g,',');
  const segs=s.split(',').map(z=>nrm(z)).filter(z=>z.length);const out=[];
  for(const g of segs){const h=stripLhs(g);for(const e of expandPM(h)){out.push(parseExpr(e)({}));}}
  return out;
}
function checkNums(raw,a){
  let got;try{got=parseList(String(raw).replace(/[{}]/g,''));}catch(e){return pe();}
  if(!got.length)return pe();
  const want=[];for(const w of a.v)for(const e of expandPM(nrm(w)))want.push(parseExpr(e)({}));
  got.sort((p,q)=>p-q);want.sort((p,q)=>p-q);
  const g2=got.filter((v,i)=>i===0||Math.abs(v-got[i-1])>1e-9);
  if(g2.length!==want.length||g2.some((v,i)=>!closeTo(v,want[i])))return {ok:false,msg:g2.length<want.length?'This problem has more than one solution. Give all of them.':BAD};
  return {ok:true};
}
function splitTop(s){const out=[];let d=0,cur='';for(const c of s){if(c==='(')d++;if(c===')')d--;if(c===','&&d===0){out.push(cur);cur='';}else cur+=c;}out.push(cur);return out;}
function checkPoint(raw,a){
  let s=nrm(raw);s=s.replace(/^\((.*)\)$/,'$1');
  const parts=splitTop(s);if(parts.length!==2)return pe('Type an ordered pair, like (2, 3).');
  const l1=/^x=/.test(parts[0]),l2=/^y=/.test(parts[1]);if(l1!==l2)return pe('Type an ordered pair, like (2, 3).');
  let g;try{g=[parts[0].replace(/^x=/,''),parts[1].replace(/^y=/,'')].map(z=>parseExpr(z)({}));}catch(e){return pe('Type an ordered pair, like (2, 3).');}
  const w=a.v.map(z=>parseExpr(nrm(z))({}));
  return closeTo(g[0],w[0])&&closeTo(g[1],w[1])?{ok:true}:{ok:false,msg:BAD};
}
function checkExpr(raw,a){
  const n0=nrm(raw);let s=n0.replace(/^(y|f\(x\))=/,'');
  if(!s)return pe();
  let f;try{f=parseExpr(s);}catch(e){return pe();}
  const g=parseExpr(nrm(a.v));
  let ok=true;try{ok=same(f,g);}catch(e){ok=false;}
  if(!ok)return {ok:false,msg:BAD};
  const par=(s.match(/\(/g)||[]).length, xs=(s.match(/x/g)||[]).length;
  if(a.minParens&&par<a.minParens)return {ok:false,msg:'That is equal to the right thing, but it is not factored the way the problem asks. Write it as a product of factors.'};
  if(a.maxParens!=null&&par>a.maxParens)return {ok:false,msg:'That is equal, but multiply it out and write it in expanded form.'};
  if(a.posExp&&/\^-|\^\(-/.test(s))return {ok:false,msg:'That is equal, but write it with a positive exponent.'};
  if(a.simplified&&(xs>1||/\)\^|\)\(/.test(s)))return {ok:false,msg:'That is equal, but simplify it further: combine everything into one term.'};
  if(a.forms&&!a.forms.includes(s.replace(/\*/g,'')))return {ok:false,msg:'That is equal, but it is not factored completely. Pull out the greatest common factor.'};
  return {ok:true};
}
function checkYIneq(raw,a){
  let s=nrm(raw).replace(/≤/g,'<=').replace(/≥/g,'>=').replace(/=</g,'<=').replace(/=>/g,'>=');
  s=s.replace(/≤/g,'<=');
  const m=s.match(/^(.*?)(<=|>=|<|>)(.*)$/);if(!m||/(<=|>=|<|>)/.test(m[3]))return pe('Write it like y > 2x + 1. Use <= and >= for ≤ and ≥.');
  let op=m[2],L=m[1],Rr=m[3],ex;
  if(L==='y')ex=Rr;else if(Rr==='y'){ex=L;op={'<':'>','>':'<','<=':'>=','>=':'<='}[op];}
  else return pe('Get y alone on one side, like y > 2x + 1.');
  let f;try{f=parseExpr(ex);}catch(e){return pe('Write it like y > 2x + 1. Use <= and >= for ≤ and ≥.');}
  const g=parseExpr(nrm(a.e));
  const sameLine=same(f,g);
  if(sameLine&&op===a.op)return {ok:true};
  if(sameLine)return {ok:false,msg:'The line is right! Check the inequality symbol: dashed line → < or >, solid line → ≤ or ≥, shaded above → >/≥, shaded below → </≤.'};
  return {ok:false,msg:BAD};
}
function normText(s){return String(s==null?'':s).toLowerCase().replace(/[∠△∆]/g,'').replace(/angle/g,'').replace(/[^a-z0-9]/g,'');}
function checkText(raw,a){
  const g=normText(raw);if(!g)return pe();
  return a.v.some(z=>normText(z)===g)?{ok:true}:{ok:false,msg:BAD};
}
function checkAns(raw,a){
  if(!String(raw||'').trim())return pe('Type your answer first.');
  switch(a.t){
    case 'source-choice':return {ok:String(raw)===String(a.v),msg:BAD};
    case 'num':return checkNum(raw,a);
    case 'nums':return checkNums(raw,a);
    case 'point':return checkPoint(raw,a);
    case 'expr':return checkExpr(raw,a);
    case 'yineq':return checkYIneq(raw,a);
    case 'text':return checkText(raw,a);
    default:return ineqCheck(raw,a);
  }
}

let KEY='mrk-whodunit-'+CASE.unit;
(function(){const P=CASE.palette;if(!P)return;const h=c=>[1,3,5].map(i=>parseInt(c.slice(i,i+2),16));const mix=(c,k)=>'#'+h(c).map(v=>Math.round(v*k).toString(16).padStart(2,'0')).join('');const r=document.documentElement.style;r.setProperty('--navy',P.navy);r.setProperty('--amber',P.accent);r.setProperty('--amberd',mix(P.accent,.5));r.setProperty('--amber2',mix(P.accent,.78));const a=h(P.accent);r.setProperty('--glow','rgba('+a.join(',')+',.28)');})();
const N=CASE.questions.length;
let teacherQuestions=new Set(CASE.questions);
let S={phase:'intro',i:0,tm:0,hn:0,sn:0,miss:0,hintShown:false,stepsShown:false,sel:{p:null,l:null,m:null},msg:''};
try{const r=JSON.parse(localStorage.getItem(KEY)||'null');if(r&&typeof r.i==='number'&&['ask','reveal','accuse','won'].includes(r.phase)){S.phase=r.phase;S.i=r.i;S.tm=r.tm||0;S.hn=r.hn||0;S.sn=r.sn||0;}}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify({phase:S.phase,i:S.i,tm:S.tm,hn:S.hn,sn:S.sn}));}catch(e){}}
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
function avatar(s){
  const hc=s.hairColor||'#222';
  let hair='';
  if(s.hair==='short')hair=`<path d="M20 27c-1-10 5-16 12-16s13 6 12 16c-3-6-7-8-12-8s-9 2-12 8z" fill="${hc}"/>`;
  if(s.hair==='long')hair=`<path d="M19 30c-2-12 4-19 13-19s15 7 13 19v10h-5V28c-4-3-12-3-16 0v12h-5z" fill="${hc}"/>`;
  if(s.hair==='bun')hair=`<circle cx="32" cy="10" r="6" fill="${hc}"/><path d="M20 27c-1-10 5-15 12-15s13 5 12 15c-3-6-7-8-12-8s-9 2-12 8z" fill="${hc}"/>`;
  if(s.hair==='bald')hair=`<path d="M21 28c-1 2-1 5 0 7h-2c-1-3-1-6 1-8zM43 28c1 2 1 5 0 7h2c1-3 1-6-1-8z" fill="${hc}"/>`;
  let acc='';
  if(s.acc==='glasses')acc='<g fill="none" stroke="#222" stroke-width="1.6"><circle cx="27.5" cy="28" r="4"/><circle cx="36.5" cy="28" r="4"/><path d="M31.5 28h1"/></g>';
  if(s.acc==='chef')acc='<g fill="#fff" stroke="#c9ced8"><rect x="22" y="14" width="20" height="7" rx="2"/><circle cx="25" cy="12" r="5"/><circle cx="32" cy="9" r="6"/><circle cx="39" cy="12" r="5"/></g>';
  if(s.acc==='cap')acc='<g fill="#1b2d52"><path d="M20 23c0-8 5-11 12-11s12 3 12 11z"/><rect x="18" y="22" width="28" height="3" rx="1.5"/></g><circle cx="32" cy="16" r="2" fill="#f2a33a"/>';
  if(s.acc==='bowtie')acc='<path d="M26 44l6 3-6 3zM38 44l-6 3 6 3z" fill="#b83a31"/>';
  const eyes=s.acc==='glasses'?'':'<circle cx="28" cy="28" r="1.4" fill="#222"/><circle cx="36" cy="28" r="1.4" fill="#222"/>';
  return `<svg class="av" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="32" fill="${s.bg}"/><path d="M9 64c0-14 10-20 23-20s23 6 23 20z" fill="${s.color}"/><rect x="29" y="38" width="6" height="7" fill="${s.skin}"/><circle cx="32" cy="28" r="11" fill="${s.skin}"/>${hair}${eyes}<path d="M28 33q4 3 8 0" stroke="#7a3b2a" stroke-width="1.4" fill="none" stroke-linecap="round"/>${acc}</svg>`;
}
function clearedSets(){
  const s=(S.phase==='ask')?S.i:(S.phase==='reveal'?S.i+1:N);
  const c={p:new Set(),l:new Set(),m:new Set()};let last=null;
  CASE.clues.slice(0,s).forEach((cl,k)=>{if(cl.p)c.p.add(cl.p);if(cl.l)c.l.add(cl.l);if(cl.m)c.m.add(cl.m);if(k===s-1&&S.phase==='reveal')last=cl;});
  return {c,last,s};
}
function board(interactive){
  const {c,last}=clearedSets();
  const isNew=(t,id)=>last&&last[t]===id?' new':'';
  const pick=(t,id)=>interactive&&S.sel[t]===id?' pick':'';
  const tag=interactive?'button':'div';
  const mk=(t,id,inner)=>`<${tag} class="card${c[t].has(id)?' cleared':''}${isNew(t,id)}${pick(t,id)}" ${interactive?`data-t="${t}" data-id="${id}" type="button" ${c[t].has(id)?'':''}`:''}>${inner}</${tag}>`;
  return `<div class="cols">
   <div class="col"><h3>${esc(CASE.labels.p)}</h3>${CASE.suspects.map(s=>mk('p',s.id,avatar(s)+`<span><span class="nm">${esc(s.name)}</span><br><span class="rl">${esc(s.role)}</span></span>`)).join('')}</div>
   <div class="col"><h3>${esc(CASE.labels.l)}</h3>${CASE.places.map((s,k)=>mk('l',s.id,`<span class="ic">${k+1}</span><span class="nm">${esc(s.name)}</span>`)).join('')}</div>
   <div class="col"><h3>${esc(CASE.labels.m)}</h3>${CASE.methods.map((s,k)=>mk('m',s.id,`<span class="ic">${String.fromCharCode(65+k)}</span><span class="nm">${esc(s.name)}</span>`)).join('')}</div>
  </div>`;
}
function effectText(cl){
  const nm=(arr,id)=>(arr.find(x=>x.id===id)||{}).name;
  const bits=[];if(cl.p)bits.push(nm(CASE.suspects,cl.p));if(cl.l)bits.push(nm(CASE.places,cl.l));if(cl.m)bits.push(nm(CASE.methods,cl.m));
  return 'Cleared: '+bits.join(' · ');
}
function log(){
  const {s}=clearedSets();
  if(!s)return '<p class="hint">No clues yet. Solve a problem to earn your first one.</p>';
  return '<ol class="log">'+CASE.clues.slice(0,s).map((cl,k)=>`<li><b>#${k+1}</b><span>${esc(cl.text)}</span></li>`).join('')+'</ol>';
}
function header(){
  const done=(S.phase==='ask')?S.i:(S.phase==='reveal'?S.i+1:N);
  return `<header class="top"><div><div class="eyebrow">${esc(CASE.eyebrow)}</div><h1>${esc(CASE.title)}</h1><p class="sub">${esc(CASE.tagline)}</p></div><span style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span class="pill">${S.phase==='intro'?'Case file':(S.phase==='accuse'||S.phase==='won'?'All clues found':'Clues earned: '+done+' of '+N)}</span>${S.phase==='intro'||S.phase==='won'?'':'<button class="action" id="restart" style="padding:8px 13px">Restart case</button>'}</span></header>`;
}
function render(){
  while(S.phase==='ask' && S.i<N && !teacherQuestions.has(CASE.questions[S.i])) S.i++;
  if(S.phase==='ask' && S.i>=N) S.phase='accuse';
  let h=header();
  if(S.phase==='intro'){
    h+=`<div class="panel story" style="max-width:820px;margin:0 auto"><h2 style="margin-top:0">The case</h2>${CASE.intro.map(p=>`<p>${p}</p>`).join('')}
    <div class="rules"><b>How to crack the case</b><ol>${CASE.rules.map(r=>`<li>${r}</li>`).join('')}</ol></div>
    <div class="actions"><button class="action primary" id="start">Open the case file</button></div></div>`;
  } else if(S.phase==='won'){
    h+=won();
  } else {
    h+=`<div class="layout"><section class="panel"><div class="sectionhead"><h2>Case board</h2><span class="hint" style="margin:0">${S.phase==='accuse'?'Choose one from each column':'Struck-out cards are cleared'}</span></div>${board(S.phase==='accuse')}
      <div class="sectionhead" style="margin-top:18px"><h2>Evidence log</h2></div>${log()}</section><section class="panel" id="side">${side()}</section></div>`;
  }
  $('#app').innerHTML=h;wire();
  const inp=$('#ans'); if(inp&&S.phase==='ask')inp.focus();
}
function fmtQ(q){return `<div class="problem"><div class="skill">${esc(q.skill)}</div><div class="instr">${q.instr}</div>${q.html?`<div class="display">${q.html}</div>`:''}</div>`;}
function side(){
  if(S.phase==='ask'){
    const q=CASE.questions[S.i];
    return `<div class="sectionhead"><h2>Clue ${S.i+1} of ${N}</h2></div><div class="progress"><div class="bar" style="width:${S.i/N*100}%"></div></div>${fmtQ(q)}
    <label class="inputlabel" for="ans">Your answer</label>
    ${q.options?'<input id="ans" type="hidden"><div class="source-choices">'+q.options.map((o,i)=>'<button class="source-choice" type="button" data-source-choice="'+i+'" aria-pressed="false">'+o+'</button>').join('')+'</div>':'<input id="ans" class="ans" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="'+esc(q.placeholder||CASE.placeholder)+'">'}
    ${(CASE.symbols||[]).length?'<div class="syms">':'<div style="display:none">'}${(CASE.symbols||[]).map(s=>`<button class="sym" type="button" data-sym="${s}" aria-label="insert ${s}">${s}</button>`).join('')}</div>
    <p class="hint">${esc(CASE.inputHint)}</p>
    <div class="actions"><button class="action primary" id="check">Check answer</button>${S.miss>=2&&!S.hintShown?'<button class="action" id="hint">Get a hint</button>':''}${S.miss>=4&&!S.stepsShown?'<button class="action" id="steps">Show the steps</button>':''}</div>
    <div class="feedback ${S.msg?'bad':''}" id="fb" role="status" aria-live="polite">${S.msg}</div>
    ${S.hintShown?`<div class="solution"><h3>Hint</h3><div>${q.hint}</div></div>`:''}
    ${S.stepsShown?`<div class="solution"><h3>Worked solution</h3>${q.steps.map(s=>`<div class="st">${s}</div>`).join('')}<p class="hint">Now type the answer to earn the clue.</p></div>`:''}`;
  }
  if(S.phase==='reveal'){
    const cl=CASE.clues[S.i], last=S.i===N-1;
    return `<div class="sectionhead"><h2>Clue ${S.i+1} unlocked</h2></div><div class="progress"><div class="bar" style="width:${(S.i+1)/N*100}%"></div></div>
    <div class="clue"><div class="tag">New evidence</div><p>${esc(cl.text)}</p><div class="eff">${esc(effectText(cl))}</div></div>
    <div class="actions"><button class="action ${last?'amber':'primary'}" id="next">${last?'Make your accusation':'Next problem'}</button></div>`;
  }
  if(S.phase==='accuse'){
    const ok=S.sel.p&&S.sel.l&&S.sel.m;
    return `<div class="sectionhead"><h2>Make your accusation</h2></div>
    <p style="line-height:1.55;margin-top:0">All ${N} clues are in. Look at your case board: tap the one ${esc(CASE.labels.p.toLowerCase().replace(/^the /,'').replace(/s$/,''))}, the one ${esc(CASE.labels.l.toLowerCase().replace(/^the /,'').replace(/s$/,''))} and the one ${esc(CASE.labels.m.toLowerCase().replace(/^the /,'').replace(/s$/,''))} that were <b>not</b> cleared.</p>
    <div class="clue" style="animation:none"><div class="tag">Your accusation</div><p>${accuseLine()}</p></div>
    <div class="actions"><button class="action amber" id="accuse" ${ok?'':'disabled'}>Accuse!</button></div>
    <div class="feedback ${S.msg?'bad':''}" role="status" aria-live="polite">${S.msg}</div>`;
  }
  return '';
}
function accuseLine(){
  const f=(arr,id,ph)=>{const x=arr.find(a=>a.id===id);return x?`<b>${esc(x.name)}</b>`:`<span style="color:var(--muted)">${ph}</span>`;};
  return CASE.accuseTemplate.replace('{p}',f(CASE.suspects,S.sel.p,'(choose a suspect)')).replace('{l}',f(CASE.places,S.sel.l,'(choose a place)')).replace('{m}',f(CASE.methods,S.sel.m,'(choose a method)'));
}
function won(){
  const e=CASE.ending;
  return `<div class="panel win" style="max-width:860px;margin:0 auto"><h2>Case closed!</h2><p style="font-size:1.1rem;line-height:1.6">${e}</p>
  <div class="stats"><div class="stat"><b>${N} of ${N}</b>clues earned</div><div class="stat"><b>${S.tm}</b>wrong tries</div><div class="stat"><b>${S.hn+S.sn}</b>hints and steps used</div></div>
  ${board(false)}
  <div class="actions" style="justify-content:center"><button class="action primary" id="again">Play again</button></div></div>`;
}
function wire(){
  const on=(id,fn)=>{const el=document.getElementById(id);if(el)el.addEventListener('click',fn);};
  on('start',()=>{S.phase='ask';S.i=0;save();render();});
  on('restart',()=>{if(confirm('Start the case over? Your clues will be cleared.')){reset();S.phase='ask';S.i=0;save();render();}});
  on('again',reset);
  document.querySelectorAll('[data-source-choice]').forEach(b=>b.onclick=()=>{$('#ans').value=b.dataset.sourceChoice;document.querySelectorAll('[data-source-choice]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));});
  on('check',check);on('hint',()=>{S.hintShown=true;S.hn++;save();render();keepVal();});
  on('steps',()=>{S.stepsShown=true;S.sn++;save();render();});
  on('next',()=>{if(S.i===N-1){S.phase='accuse';S.i=N;}else{S.i++;S.phase='ask';}S.miss=0;S.hintShown=false;S.stepsShown=false;S.msg='';save();render();});
  on('accuse',accuse);
  const inp=$('#ans');if(inp)inp.addEventListener('keydown',e=>{if(e.key==='Enter')check();});
  document.querySelectorAll('.sym').forEach(b=>b.addEventListener('click',()=>{const i=$('#ans');if(!i)return;const t=b.dataset.sym;const a=i.selectionStart??i.value.length,z=i.selectionEnd??a;const ins=t==='or'?' or ':t;i.value=i.value.slice(0,a)+ins+i.value.slice(z);i.focus();i.selectionStart=i.selectionEnd=a+ins.length;}));
  document.querySelectorAll('button.card[data-t]').forEach(b=>b.addEventListener('click',()=>{S.sel[b.dataset.t]=b.dataset.id;S.msg='';render();}));
}
function keepVal(){}
function check(){
  const i=$('#ans');if(!i)return;const q=CASE.questions[S.i];const r=checkAns(i.value,q.answer);
  if(r.ok){S.phase='reveal';S.msg='';save();render();return;}
  if(r.parse){S.msg=r.msg;const v=i.value;render();$('#ans').value=v;$('#ans').focus();return;}
  S.miss++;S.tm++;S.msg=r.msg;const v=i.value;save();render();$('#ans').value=v;$('#ans').focus();
}
function accuse(){
  const t=CASE.culprit;
  if(S.sel.p===t.p&&S.sel.l===t.l&&S.sel.m===t.m){S.phase='won';save();render();confetti();return;}
  const wrong=[];if(S.sel.p!==t.p)wrong.push(CASE.labels.p.toLowerCase().replace(/^the /,'').replace(/s$/,''));if(S.sel.l!==t.l)wrong.push(CASE.labels.l.toLowerCase().replace(/^the /,'').replace(/s$/,''));if(S.sel.m!==t.m)wrong.push(CASE.labels.m.toLowerCase().replace(/^the /,'').replace(/s$/,''));
  S.tm++;S.msg='Not quite: check your evidence log. At least one choice ('+wrong.join(', ')+') has already been cleared by a clue.';S.sel={p:null,l:null,m:null};save();render();
}
function reset(){S={phase:'intro',i:0,tm:0,hn:0,sn:0,miss:0,hintShown:false,stepsShown:false,sel:{p:null,l:null,m:null},msg:''};try{localStorage.removeItem(KEY);}catch(e){}render();}
function confetti(){const c=document.createElement('div');c.className='confetti';const cols=['#f2a33a','#345bd5','#1f7a4d','#b83a31','#7a3fb0'];for(let k=0;k<70;k++){const e=document.createElement('i');e.style.left=Math.random()*100+'%';e.style.background=cols[k%cols.length];e.style.animationDuration=(2.2+Math.random()*2.4)+'s';e.style.animationDelay=(Math.random()*.8)+'s';c.appendChild(e);}document.body.appendChild(c);setTimeout(()=>c.remove(),6000);}
window.MK_MYSTERY_STATE=()=>S;window.MK_MYSTERY_CASE=CASE;render();

})(window.MK_ACTIVE_MYSTERY_CASE);

