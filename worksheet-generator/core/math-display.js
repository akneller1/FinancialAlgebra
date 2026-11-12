/* Shared display-only renderer. The formatter is reused from Algebra 1 Connect 4.
 * Source questions and answer values are never modified. */
(function(G){'use strict';
/*FM-START*/
/* Math mini-syntax -> HTML.
   <= >= != -> ≤ ≥ ≠     - -> −     * -> ·     -> -> →     ' -> ′
   [[top ; bottom]]       stacked fraction (nestable)
   x^2  x^-3  x^{n+1}     superscript (after ^: optional -, then digits or ONE letter, or a {group})
   x_1  x_{ab}            subscript
   rt{...}  cbrt{...}     square / cube root
   ov{AB}                 overline (segment)
   sys{eq1 ;; eq2}        system of equations with a left brace
   tbl{x&&0&&1 ;; y&&3&&5} horizontal table, rows split by ;; cells by &&
   @{text}                upright text, no formatting
   v{Ipr}                 each letter italic (variable run the automatic rules would treat as a word)
   Single letters are italic variables. 2-4 capital letters are italic point names (AB, ABC)
   except known names (SSS, SAS, ASA, AAS, HL, AA, CPCTC, SOH, CAH, TOA ...). Runs of 2 lowercase
   letters are products of variables (xy) except unit words (cm, ft, in, ln ...). Longer words are upright.
   "or" and "and" become connector words. "pi" becomes π. */
const FM_UPRIGHT_CAPS=new Set(['SSS','SAS','ASA','AAS','HL','AA','SSA','SAA','CPCTC','SOH','CAH','TOA','LL','LA','HA','AAA','NO','IF','OR','AND','II','III','IV','QI','ZPP','FOIL','GCF','LCD','LCM','PEMDAS','SA','RHS','RSH','SOHCAHTOA','AM','PM']);
const FM_UNITS=new Set(['cm','mm','km','ft','in','yd','mi','ln','if','is','no','of','to','at','or','as','by','on','so','up','it','be','we','my','us','am','pm','mph','sq','cu']);
/* "a" / "an" used as an article in a sentence ("cut by a transversal", "solve an equation", "A circle has ...") is a
   word, not a variable: lowercase before a word of 3+ letters unless a variable is being named (let a, if a, when a ...);
   capital A/An only at the start of a sentence, so point names ("angle A measures") stay italic. */
const FM_VARCTX=new Set(['let','if','when','where','for','solve','find','and','of','with','then','than']);
function fmArticle(s,i,m){
  if(!/^(a|an|A|An)$/.test(m))return false;
  const next=/^ ([a-z][a-z]+)/.exec(s.slice(i+m.length));
  if(!next||next[1].length<3||next[1]==='and'||next[1]==='or')return false;
  const before=s.slice(0,i),prev=(/([A-Za-z]+)\s*$/.exec(before)||[])[1];
  if(m[0]==='A')return /(^|[.!?:\n]\s*)$/.test(before);
  return !(prev&&FM_VARCTX.has(prev.toLowerCase()));
}
function fmEsc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function fmMatch(s,i,open,close){ /* s[i..] starts with open; return index just after the matching close */
  let d=0;
  for(let j=i;j<s.length;){
    if(s.startsWith(open,j)){d++;j+=open.length;}
    else if(s.startsWith(close,j)){d--;j+=close.length;if(d===0)return j;}
    else j++;
  }
  return s.length;
}
function fmSplit(s,sep){ /* split at top level only */
  const out=[];let d=0,b=0,last=0;
  for(let j=0;j<s.length;j++){
    if(s.startsWith('[[',j)){d++;j++;}
    else if(s.startsWith(']]',j)){d--;j++;}
    else if(s[j]==='{')b++;
    else if(s[j]==='}')b--;
    else if(!d&&!b&&s.startsWith(sep,j)){
      if(sep===';'&&(s[j+1]===';'||s[j-1]===';'))continue;
      out.push(s.slice(last,j));last=j+sep.length;j+=sep.length-1;
    }
  }
  out.push(s.slice(last));return out;
}
function fm(s){
  s=String(s);let out='',i=0;const n=s.length;
  const grp=(open)=>{ /* read a {group} starting at s[i]==='{' */
    const e=fmMatch(s,i,'{','}');const inner=s.slice(i+1,e-1);i=e;return inner;};
  while(i<n){
    const c=s[i];
    if(s.startsWith('[[',i)){
      const e=fmMatch(s,i,'[[',']]'),inner=s.slice(i+2,e-2),parts=fmSplit(inner,';');
      out+=`<span class="fr"><span class="fn">${fm(parts[0].trim())}</span><span class="fd">${fm((parts[1]||'').trim())}</span></span>`;i=e;continue;
    }
    if(s.startsWith('rt{',i)){i+=2;out+=`<span class="rt"><span class="rts">√</span><span class="rtc">${fm(grp())}</span></span>`;continue;}
    if(s.startsWith('cbrt{',i)){i+=4;out+=`<span class="rt"><sup class="rti">3</sup><span class="rts">√</span><span class="rtc">${fm(grp())}</span></span>`;continue;}
    if(s.startsWith('v{',i)&&!/[A-Za-z]/.test(s[i-1]||' ')){i+=1;out+=grp().split('').map(ch=>/[A-Za-z]/.test(ch)?`<i>${ch}</i>`:fmEsc(ch)).join('');continue;}
    if(s.startsWith('ov{',i)){i+=2;out+=`<span class="ov">${fm(grp())}</span>`;continue;}
    if(s.startsWith('@{',i)){i+=1;out+=`<span class="tx">${fmEsc(grp())}</span>`;continue;}
    if(s.startsWith('sys{',i)){i+=3;const rows=fmSplit(grp(),';;');
      out+=`<span class="sys"><span class="eqs">${rows.map(r=>`<span>${fm(r.trim())}</span>`).join('')}</span></span>`;continue;}
    if(s.startsWith('tbl{',i)){i+=3;const rows=fmSplit(grp(),';;');
      out+=`<table class="tbl">${rows.map((r,k)=>`<tr>${r.split('&&').map(x=>k?`<td>${fm(x.trim())}</td>`:`<th>${fm(x.trim())}</th>`).join('')}</tr>`).join('')}</table>`.replace(/<tr>(<t[hd]>.*?<\/t[hd]>)/g,(m,a)=>'<tr>'+a.replace(/<td>/,'<th scope="row">').replace(/<\/td>/,'</th>'));continue;}
    if(c==='^'||c==='_'){
      i++;let inner='';
      if(s[i]==='{')inner=grp();
      else{let m=/^-?(?:\d+(?:\.\d+)?|[A-Za-z])/.exec(s.slice(i));if(m){inner=m[0];i+=inner.length;}}
      out+=`<${c==='^'?'sup':'sub'} class="s">${fm(inner)}</${c==='^'?'sup':'sub'}>`;continue;
    }
    if(/[A-Za-z]/.test(c)){
      let m=/^[A-Za-z]+/.exec(s.slice(i))[0];
      /* a trailing digit-free run; handle special words */
      if(m==='or'||m==='and'){out+=`<span class="w">${m}</span>`;}
      else if(m==='pi'){out+='π';}
      else if(fmArticle(s,i,m)){out+=`<span class="tx">${m}</span>`;}
      else if(m.length===1){out+=`<i>${m}</i>`;}
      else if(FM_UPRIGHT_CAPS.has(m)||FM_UNITS.has(m)){out+=`<span class="tx">${m}</span>`;}
      else if(/^[A-Z]{2,4}$/.test(m)){out+=`<i>${m}</i>`;}
      else if(/^[a-z]{2}$/.test(m)||/^[a-z]{3,4}$/.test(m)&&!/[aeiouy]/.test(m)){out+=m.split('').map(ch=>`<i>${ch}</i>`).join('');}
      else{out+=`<span class="tx">${m}</span>`;}
      i+=m.length;continue;
    }
    if(s.startsWith('<=',i)){out+='≤';i+=2;continue;}
    if(s.startsWith('>=',i)){out+='≥';i+=2;continue;}
    if(s.startsWith('!=',i)){out+='≠';i+=2;continue;}
    if(s.startsWith('->',i)){out+='→';i+=2;continue;}
    if(c==='<'){out+='&lt;';i++;continue;}
    if(c==='>'){out+='&gt;';i++;continue;}
    if(c==='&'){out+='&amp;';i++;continue;}
    if(c==='-'){out+='−';i++;continue;}
    if(c==='*'){out+='·';i++;continue;}
    if(c==="'"){out+=/[A-Za-z]/.test(s[i-1]||'')&&/[A-Za-z]/.test(s[i+1]||'')?"'":'′';i++;continue;}
    if(c==='\n'){out+='<br>';i++;continue;}
    if(c===' '&&s[i+1]===' '){out+='&ensp;';i+=2;continue;}
    out+=c;i++;
  }
  return out;
}
/* plain text with inline math in {{ ... }} */
function inl(s){
  s=String(s);let out='',i=0;
  while(i<s.length){
    const j=s.indexOf('{{',i);
    if(j<0){out+=fmEsc(s.slice(i));break;}
    out+=fmEsc(s.slice(i,j));
    let k=j+2,d=0,end=-1;
    for(;k<s.length;k++){
      if(s[k]==='{')d++;
      else if(s[k]==='}'){if(d===0&&s[k+1]==='}'){end=k;break;}d--;}
    }
    if(end<0){out+=fmEsc(s.slice(j));break;}
    out+=`<span class="m">${fm(s.slice(j+2,end))}</span>`;i=end+2;
  }
  return out;
}
const FM_CSS=`
.fr{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:.86em;margin:0 .14em;line-height:1.15}
.fr .fn{padding:0 .22em .07em;border-bottom:.075em solid currentColor}
.fr .fd{padding:.07em .22em 0}
sup.s,sub.s{font-size:.66em;line-height:0;font-style:normal}
sup.s{vertical-align:.62em} sub.s{vertical-align:-.3em}
.rt{display:inline-flex;align-items:stretch;white-space:nowrap}
.rts{font-style:normal;margin-right:-.05em}
.rtc{border-top:.075em solid currentColor;padding:0 .12em;margin-top:.12em}
.rti{font-size:.55em;line-height:1;align-self:flex-start;margin-right:-.15em;margin-top:.1em}
.ov{border-top:.075em solid currentColor;padding-top:.02em}
.tx{font-style:normal;font-family:inherit}
.w{font-style:normal;font-weight:700;font-size:.62em;letter-spacing:.07em;text-transform:uppercase;margin:0 .5em;opacity:.85}
.sys{display:inline-flex;align-items:center;vertical-align:middle}
.sys::before{content:"";width:.5em;align-self:stretch;margin:.05em .25em .05em 0;border:.09em solid currentColor;border-right:0;border-radius:.45em 0 0 .45em}
.eqs{display:flex;flex-direction:column;align-items:flex-start;gap:.2em;padding:.1em 0}
table.tbl{display:inline-table;border-collapse:collapse;font-size:.8em;margin:.2em 0;vertical-align:middle}
table.tbl th,table.tbl td{border:.08em solid currentColor;padding:.12em .7em;text-align:center;font-weight:400}
table.tbl th[scope=row]{font-weight:700}
table.tbl tr:first-child th{font-weight:700}
.m{white-space:normal}
`;
/*FM-END*/

function leftStart(s,end){
 let i=end-1;while(i>=0&&/\s/.test(s[i]))i--;const last=i+1;
 if(s.slice(i-1,i+1)===']]') {let d=1;i-=2;while(i>=0&&d){if(s.slice(i-1,i+1)===']]'){d++;i-=2}else if(s.slice(i-1,i+1)==='[['){d--;i-=2}else i--}return i+1;}
 if(s[i]===')'||s[i]==='}') {const close=s[i],open=close===')'?'(':'{';let d=1;i--;while(i>=0&&d){if(s[i]===close)d++;if(s[i]===open)d--;i--}if(d)return last;let start=i+1;if(s[start-1]==='^'||s[start-1]==='_')return leftStart(s,start-1);const fn=/(?:[A-Za-z]|sin|cos|tan|log|ln|sqrt|√)$/.exec(s.slice(0,start));if(fn)start-=fn[0].length;return start;}
 while(i>=0&&/[A-Za-z0-9.πθ²³⁰¹⁴⁵⁶⁷⁸⁹ⁿˣ⁻^_]/.test(s[i]))i--;
 const atom=s.slice(i+1,last);if(/^[A-Za-z]{3,}$/.test(atom))return last;
 if(s[i]===')'&&/^[²³⁰¹⁴-⁹ⁿˣ^_]/.test(atom))return leftStart(s,i+1);
 return i+1;
}
function rightPower(s,end){const m=/^(?:[²³⁰¹⁴⁵⁶⁷⁸⁹ⁿˣ⁻]+|\^(?:\{[^{}]+\}|[−-]?\d+))/.exec(s.slice(end));return m?end+m[0].length:end}
function rightEnd(s,start){
 let i=start;while(/\s/.test(s[i]||''))i++;let sign=i;if(/[+−-]/.test(s[i]||''))i++;
 if(s[i]==='('||s[i]==='{'){const open=s[i],close=open==='('?')':'}';let d=1;i++;while(i<s.length&&d){if(s[i]===open)d++;if(s[i]===close)d--;i++}return d?start:rightPower(s,i);}
 const fn=/^(?:[A-Za-z]|sin|cos|tan|log|ln|sqrt|√)\(/.exec(s.slice(i));if(fn){const startGroup=i+fn[0].length-1;return rightEnd(s,startGroup);}
 const match=/^(?:\d+(?:\.\d+)?|[A-Za-zπθ](?:[²³⁰¹⁴⁵⁶⁷⁸⁹ⁿˣ⁻]+)?)(?:\^(?:\{[^{}]+\}|[−-]?\d+))?/.exec(s.slice(i));
 return match?rightPower(s,i+match[0].length):start;
}
function fractions(src){
 let s=String(src),offset=0;
 // Calendar dates are text, not division expressions.
 const dates=[];s=s.replace(/\b\d{1,2}\/\d{1,2}\/\d{2,4}\b/g,m=>{dates.push(m);return '\uE000'+(dates.length-1)+'\uE001'});
 for(let guard=0;guard<100;guard++){
  const slash=s.indexOf('/',offset);if(slash<0)break;
  const l=leftStart(s,slash),r=rightEnd(s,slash+1);
  if(l>=slash||r<=slash+1){offset=slash+1;continue}
  const numerator=s.slice(l,slash).trim(),denominator=s.slice(slash+1,r).trim();
  const next='[['+fractions(numerator)+' ; '+fractions(denominator)+']]';s=s.slice(0,l)+next+s.slice(r);offset=l+next.length;
 }
 return s.replace(/\uE000(\d+)\uE001/g,(_,n)=>dates[+n]);
}
function html(value,options){
 const rendered=String(value==null?'':value).split(/(⟨[^⟩]*⟩)/).map(part=>{
  if(/^⟨/.test(part)&&G.katex){return G.katex.renderToString(part.slice(1,-1).replace(/\\frac/g,'\\dfrac'),{throwOnError:false,output:'html',trust:false})}
  let mini=fractions(part);mini=mini.replace(/\^\(([^()]*)\)/g,'^{$1}');
  return fm(mini).replace(/\n/g,'<br>');
 }).join('');
 return options&&options.prose?'<span class="mk-prose">'+rendered+'</span>':rendered;
}
function decorate(root){
 if(!root||!G.document)return;
 const walk=G.document.createTreeWalker(root,4),nodes=[];let node;
 while((node=walk.nextNode()))if(node.parentElement&&!node.parentElement.closest('script,style,textarea,select,option,.katex,.mk-math,.fr')&&/\/(?!\/)/.test(node.nodeValue)&&fractions(node.nodeValue)!==node.nodeValue)nodes.push(node);
 nodes.forEach(n=>{const span=G.document.createElement('span');span.className='mk-math';span.innerHTML=html(n.nodeValue);n.replaceWith(span)});
}
G.MK_MATH_DISPLAY={html,fractions,decorate};
if(G.document){
 const script=G.document.currentScript,link=G.document.createElement('link');link.rel='stylesheet';link.href=new URL('math-display.css?v=worksheet-layout-20261111',script.src).href;G.document.head.appendChild(link);
 const selector='.af-prompt,.gm-q,.gm-opt,.gm-sol,.prompt,.statement,.choices,.problem,.display,.eq,.q,.solution,.steps,.st,.item,.ord,.pm-text,.pm-big,#prPreview .page';
 let pending=false;function scan(){pending=false;G.document.querySelectorAll(selector).forEach(decorate)}
 function schedule(){if(!pending){pending=true;queueMicrotask(scan)}}
 new MutationObserver(schedule).observe(G.document.body,{childList:true,subtree:true,characterData:true});schedule();
}
})(typeof window!=='undefined'?window:globalThis);
