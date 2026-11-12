"""Grade 5 Interactive Math tools: writes artifacts/math5-<slug>/index.html and manifest.json.
Usage: python3 tools/math5/interactive/tools.py   (then build_pdfs.cjs for worksheets, keys and thumbnails)
Each tool: live model, clear controls (mouse, touch, keyboard), Try-this challenges, What-should-I-notice panel,
zoom/fit/present/reset. No network calls; all math done with exact integer/fraction arithmetic."""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · 5th Grade Math | Mr. K's Classroom</title><meta name="description" content="{desc}">
<link rel="stylesheet" href="../../worksheet-generator/grade5/g5.css?v=grade5-20261111"><link rel="stylesheet" href="../../worksheet-generator/core/math-display.css">
<style>
.ts-grid{{display:grid;grid-template-columns:minmax(0,2fr) minmax(16rem,1fr);gap:1rem;align-items:start}}@media(max-width:860px){{.ts-grid{{grid-template-columns:1fr}}}}
.ts-ch{{padding-left:1.2rem}}.ts-ch li{{margin:.35rem 0}}.ts-ch li.done{{color:#065F46;font-weight:700}}.ts-ch .box{{font-size:1.15rem}}
.ts-big{{font-family:var(--display);font-size:2.4rem;font-weight:800;text-align:center;margin:.3rem 0}}
.ts-model{{text-align:center}}.ts-model svg{{max-width:100%;height:auto;max-height:300px;width:auto}}#pvChart svg{{max-height:140px}}#pvBlocks svg{{max-height:150px}}#fxModel svg{{width:100%;max-height:none}}#cpGrid svg{{width:100%;max-height:none}}
.ts-step{{display:flex;align-items:center;gap:.3rem}}.ts-step button{{min-width:44px;min-height:44px;border-radius:12px;border:2px solid #CBD5E1;background:#fff;font-weight:800;font-size:1.2rem}}
.ts-out{{background:#F8FAFC;border-radius:14px;padding:.6rem .9rem;margin:.6rem 0;font-size:1.1rem}}
.ts-out b{{color:var(--purple)}}input[type=range]{{width:100%;accent-color:var(--purple);min-height:32px}}
details summary{{font-weight:800;cursor:pointer;color:var(--purple)}}.fr{{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1;font-size:.9em}}.fr .fn{{border-bottom:2px solid currentColor;padding:0 .15em}}
</style></head><body>
<main class="g5"><div class="ts-grid"><section class="g5-card" id="tool"><h1>{title}</h1><p class="g5-sub">{intro}</p>{body}</section>
<aside><section class="g5-card" id="challenges"></section><section class="g5-card" id="notice"></section></aside></div></main>
<script src="../../worksheet-generator/grade5/g5-figs.js?v=grade5-20261111"></script><script src="../../worksheet-generator/grade5/tool-shell.js?v=grade5-20261111"></script>
<script>
{script}
</script></body></html>
"""

TOOLS = []


def tool(slug, unit, title, desc, intro, topics, body, script, worksheet):
    TOOLS.append(dict(slug="math5-" + slug, unit=unit, title=title, description=desc, intro=intro, topics=topics, body=body, script=script, worksheet=worksheet))


# ------------------------------------------------------------------ 1 Decimal Place-Value Builder
tool("place-value-builder", "place-value-number-sense", "Decimal Place-Value Builder",
     "Build numbers digit by digit in a place-value chart, multiply and divide by 10, and see expanded form, word form and base-ten blocks change.",
     "Use the + and − buttons to build a number. Then press × 10 or ÷ 10 and watch every digit move.", ["Place value", "Decimals", "Powers of 10"],
     """<div id="pvRows" class="g5-row" style="justify-content:center;gap:.4rem"></div>
<div class="ts-big" id="pvNum" aria-live="polite">0</div>
<div class="g5-actions" style="justify-content:center"><button class="g5-btn" id="pvTimes">× 10</button><button class="g5-btn" id="pvDiv">÷ 10</button><button class="g5-btn alt" id="pvClear">Clear</button></div>
<div class="ts-model" id="pvChart"></div><div class="ts-out" id="pvInfo"></div><div class="ts-model" id="pvBlocks"></div>""",
     r"""
var PL=[3,2,1,0,-1,-2,-3],NAMES={3:'thousands',2:'hundreds',1:'tens',0:'ones','-1':'tenths','-2':'hundredths','-3':'thousandths'};
var d={},st={times:0,div:0};function reset(){PL.forEach(function(p){d[p]=0});d[0]=3;d[-1]=0;d[-2]=7;st={times:0,div:0};draw();}
function val(){return PL.reduce(function(a,p){return a+d[p]*Math.pow(10,p+3)},0);} // in thousandths (exact integer)
function str(){var v=val(),w=Math.floor(v/1000),f=String(v%1000).padStart(3,'0').replace(/0+$/,'');return w.toLocaleString('en-US')+(f?'.'+f:'');}
var ONES='zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split(' '),TENS=',,twenty,thirty,forty,fifty,sixty,seventy,eighty,ninety'.split(',');
function words(n){if(n<20)return ONES[n];if(n<100)return TENS[Math.floor(n/10)]+(n%10?'-'+ONES[n%10]:'');if(n<1000)return ONES[Math.floor(n/100)]+' hundred'+(n%100?' '+words(n%100):'');return words(Math.floor(n/1000))+' thousand'+(n%1000?' '+words(n%1000):'');}
function wordForm(){var v=val(),w=Math.floor(v/1000),f=String(v%1000).padStart(3,'0').replace(/0+$/,'');if(!f)return words(w);var k=f.length,n=+f,u=['tenth','hundredth','thousandth'][k-1]+(n===1?'':'s');return (w?words(w)+' and ':'')+words(n)+' '+u;}
function expanded(){var t=[];PL.forEach(function(p){if(d[p])t.push(d[p]+' × '+(p>=0?Math.pow(10,p).toLocaleString('en-US'):TOOL.frac(1,Math.pow(10,-p))))});return t.join(' + ')||'0';}
function shift(dir){if(dir>0&&d[3])return alert('That would need a ten-thousands place. Try ÷ 10 first.');if(dir<0&&d[-3])return alert('That would need a ten-thousandths place. Try × 10 first.');
 var nd={};PL.forEach(function(p){nd[p]=d[p-dir]||0});d=nd;if(dir>0)st.times++;else st.div++;draw();}
function draw(){
 TOOL.$('pvRows').innerHTML=PL.map(function(p){return '<div class="ts-step" style="flex-direction:column"><button aria-label="Increase '+NAMES[p]+'" data-p="'+p+'" data-s="1">+</button><span style="font-weight:800;font-size:1.3rem" aria-label="'+NAMES[p]+' digit">'+d[p]+'</span><button aria-label="Decrease '+NAMES[p]+'" data-p="'+p+'" data-s="-1">−</button><span class="g5-note" style="font-size:.7rem">'+NAMES[p]+'</span></div>'+(p===0?'<div style="font-size:2rem;align-self:center">.</div>':'');}).join('');
 Array.prototype.forEach.call(document.querySelectorAll('#pvRows button'),function(b){b.onclick=function(){var p=+b.dataset.p;d[p]=(d[p]+(+b.dataset.s)+10)%10;draw();}});
 TOOL.$('pvNum').textContent=str();
 TOOL.$('pvChart').innerHTML=G5FIGS.pvchart(str().replace(/,/g,''),{lo:Math.min(-1,PL.filter(function(p){return d[p]}).reduce(function(a,p){return Math.min(a,p)},0))});
 TOOL.$('pvInfo').innerHTML='<b>Expanded form:</b> '+expanded()+'<br><b>Word form:</b> '+wordForm();
 var v=val();TOOL.$('pvBlocks').innerHTML=(v<10000&&v%10===0)?'<p class="g5-note">Base-ten blocks (flat = 1, rod = 0.1, small cube = 0.01)</p>'+G5FIGS.blocks(d[0],d[-1],d[-2],{decimal:true}):'<p class="g5-note">Blocks show numbers less than 10 with up to two decimal places.</p>';
 TOOL.update(O,{v:val(),d:d,st:st});}
var O={title:'Decimal Place-Value Builder',reset:reset,challenges:[
 {text:'Build the number 4.06.',test:function(s){return s.v===4060}},
 {text:'Build 0.125 (one hundred twenty-five thousandths).',test:function(s){return s.v===125}},
 {text:'Build 5.55. How does each 5 compare with the 5 to its right?',test:function(s){return s.v===5550}},
 {text:'Press × 10 two times. Where did each digit go?',test:function(s){return s.st.times>=2}},
 {text:'Press ÷ 10 three times in a row.',test:function(s){return s.st.div>=3}},
 {text:'Make a number between 2.4 and 2.5.',test:function(s){return s.v>2400&&s.v<2500}}],
 notice:['Each place is worth 10 times the place to its right and 1/10 of the place to its left.','× 10 moves every digit one place left; ÷ 10 moves every digit one place right.','A zero at the end of a decimal (0.50) does not change its value.','The word form ends with the name of the last place: tenths, hundredths or thousandths.']};
TOOL.init(O);reset();""",
     [("Build 3.47. Write it in expanded form.", "3 × 1 + 4 × 1/10 + 7 × 1/100"), ("Build 3.47 and press × 10. What number do you get?", "34.7"),
      ("Start again with 3.47 and press ÷ 10. What number do you get?", "0.347"), ("In 5.55, the first 5 is worth how many times the second 5?", "10 times"),
      ("Build 0.125. Write it in word form.", "one hundred twenty-five thousandths"), ("Which is greater: 0.6 or 0.58? Use the chart to explain.", "0.6, because 6 tenths > 5 tenths"),
      ("Build 2.3 with blocks. How many rods are there?", "3 rods (3 tenths)"), ("Reflect: Why do the digits move left when you multiply by 10?", "Each place is 10 times the place to its right, so each digit becomes worth 10 times as much.")])

# ------------------------------------------------------------------ 2 Area Model Explorer
tool("area-model-explorer", "multi-digit-multiplication-division", "Area Model Explorer",
     "Split rectangles into partial products to multiply two-digit numbers, then switch to fractions and multiply parts of a whole.",
     "Choose the factors. The rectangle splits into parts by place value (or into equal fraction parts).", ["Area model", "Partial products", "Multiplying fractions"],
     """<div class="g5-row"><div class="g5-field"><label for="amMode">Mode</label><select id="amMode"><option value="w">Whole numbers</option><option value="f">Fractions</option></select></div></div>
<div id="amW" class="g5-row"><div class="g5-field"><label for="amA">First factor: <b id="amAv"></b></label><input type="range" id="amA" min="10" max="99" value="23"></div><div class="g5-field"><label for="amB">Second factor: <b id="amBv"></b></label><input type="range" id="amB" min="10" max="99" value="14"></div></div>
<div id="amF" class="g5-row g5-hidden"><div class="g5-field"><label>First fraction</label><div class="ts-step"><button data-k="a" data-s="-1" aria-label="numerator down">−</button><b id="amfa"></b><button data-k="a" data-s="1" aria-label="numerator up">+</button> / <button data-k="b" data-s="-1" aria-label="denominator down">−</button><b id="amfb"></b><button data-k="b" data-s="1" aria-label="denominator up">+</button></div></div>
<div class="g5-field"><label>Second fraction</label><div class="ts-step"><button data-k="c" data-s="-1" aria-label="numerator down">−</button><b id="amfc"></b><button data-k="c" data-s="1" aria-label="numerator up">+</button> / <button data-k="d" data-s="-1" aria-label="denominator down">−</button><b id="amfd"></b><button data-k="d" data-s="1" aria-label="denominator up">+</button></div></div></div>
<div class="ts-model" id="amModel"></div><div class="ts-out" id="amOut" aria-live="polite"></div>""",
     r"""
var f={a:1,b:2,c:3,d:4};function reset(){TOOL.$('amMode').value='w';TOOL.$('amA').value=23;TOOL.$('amB').value=14;f={a:1,b:2,c:3,d:4};draw();}
function grid(){var a=f.a,b=f.b,c=f.c,d=f.d,S=240,s='<svg viewBox="0 0 300 290">';
 for(var i=0;i<b;i++)for(var j=0;j<d;j++){var inA=i<a,inC=j<c;s+='<rect x="'+(40+i*S/b)+'" y="'+(30+(d-1-j)*S/d)+'" width="'+(S/b)+'" height="'+(S/d)+'" fill="'+(inA&&inC?'#7C3AED':inA?'#FDE68A':inC?'#BFDBFE':'#fff')+'" stroke="#1E293B" stroke-width="1.2"/>';}
 s+='<rect x="40" y="30" width="'+S+'" height="'+S+'" fill="none" stroke="#1E293B" stroke-width="3"/><text x="160" y="20" text-anchor="middle" font-size="13" font-weight="700">1 whole</text>';
 s+='<text x="'+(40+a*S/b/2)+'" y="285" text-anchor="middle" font-size="14" font-weight="700" fill="#B45309">'+a+'/'+b+'</text><text x="30" y="'+(30+S-c*S/d/2)+'" text-anchor="end" font-size="14" font-weight="700" fill="#1D4ED8">'+c+'/'+d+'</text></svg>';return s;}
function draw(){var m=TOOL.$('amMode').value;TOOL.$('amW').classList.toggle('g5-hidden',m!=='w');TOOL.$('amF').classList.toggle('g5-hidden',m!=='f');
 if(m==='w'){var A=+TOOL.$('amA').value,B=+TOOL.$('amB').value,at=A-A%10,ao=A%10,bt=B-B%10,bo=B%10;TOOL.$('amAv').textContent=A;TOOL.$('amBv').textContent=B;
  var top=ao?[at,ao]:[at],side=bo?[bt,bo]:[bt],cells=side.map(function(s){return top.map(function(t){return (s*t).toLocaleString('en-US')})});
  TOOL.$('amModel').innerHTML=G5FIGS.area(top.map(String),side.map(String),cells);
  var parts=[];side.forEach(function(s){top.forEach(function(t){parts.push(s*t)})});
  TOOL.$('amOut').innerHTML='<b>'+A+' × '+B+'</b> = '+parts.map(function(p){return p.toLocaleString('en-US')}).join(' + ')+' = <b>'+(A*B).toLocaleString('en-US')+'</b>';
  TOOL.update(O,{m:m,A:A,B:B,parts:parts});}
 else{['a','b','c','d'].forEach(function(k){TOOL.$('amf'+k).textContent=f[k]});TOOL.$('amModel').innerHTML=grid();
  var n=f.a*f.c,dd=f.b*f.d;TOOL.$('amOut').innerHTML=TOOL.frac(f.a,f.b)+' × '+TOOL.frac(f.c,f.d)+' = '+TOOL.frac(n,dd)+(TOOL.gcd(n,dd)>1?' = <b>'+TOOL.mixed(n,dd)+'</b>':'')+'<br><span class="g5-note">The whole is cut into '+f.b+' × '+f.d+' = '+dd+' equal parts; the purple part is '+f.a+' × '+f.c+' = '+n+' of them.</span>';
  TOOL.update(O,{m:m,f:f,n:n,d:dd});}}
Array.prototype.forEach.call(document.querySelectorAll('#amF button'),function(b){b.onclick=function(){var k=b.dataset.k,s=+b.dataset.s;f[k]+=s;if(f.b<2)f.b=2;if(f.d<2)f.d=2;if(f.b>10)f.b=10;if(f.d>10)f.d=10;if(f.a<1)f.a=1;if(f.c<1)f.c=1;if(f.a>f.b)f.a=f.b;if(f.c>f.d)f.c=f.d;draw();}});
['amMode','amA','amB'].forEach(function(id){TOOL.$(id).oninput=draw;});
var O={title:'Area Model Explorer',reset:reset,challenges:[
 {text:'Show 23 × 14. Which part of the model is the biggest?',test:function(s){return s.m==='w'&&s.A===23&&s.B===14}},
 {text:'Make a model with a partial product of 600.',test:function(s){return s.m==='w'&&s.parts.indexOf(600)>=0}},
 {text:'Find two factors whose product is more than 5,000.',test:function(s){return s.m==='w'&&s.A*s.B>5000}},
 {text:'Switch to fractions and show 1/2 × 1/3.',test:function(s){return s.m==='f'&&s.f.a===1&&s.f.b===2&&s.f.c===1&&s.f.d===3}},
 {text:'Make a fraction product equal to 3/8.',test:function(s){return s.m==='f'&&s.n*8===s.d*3}},
 {text:'Make a fraction product equal to 1/4 using two different fractions.',test:function(s){return s.m==='f'&&s.n*4===s.d&&!(s.f.a*s.f.d===s.f.b*s.f.c)}}],
 notice:['Each box is one partial product: tens × tens, tens × ones, ones × tens, ones × ones.','Adding all the boxes gives the whole product.','For fractions, the whole is cut into (denominator × denominator) equal parts.','Multiplying two fractions less than 1 gives a product smaller than either fraction.']};
TOOL.init(O);reset();""",
     [("Show 36 × 24. List the four partial products.", "600, 120, 120, 24"), ("What is 36 × 24?", "864"), ("Show 45 × 13. Which partial product is the largest?", "400 (40 × 10)"),
      ("Explain why 48 × 25 is not just 40 × 20 + 8 × 5.", "That leaves out 40 × 5 and 8 × 20; the full product is 1,200."), ("Switch to fractions. Show 2/3 × 3/4. What fraction is purple?", "6/12 = 1/2"),
      ("How many equal parts is the whole cut into for 2/5 × 1/2?", "10"), ("Find 3/4 × 1/2.", "3/8"), ("Reflect: Why is 1/2 × 1/3 smaller than 1/3?", "You are taking half of one third, which is less than the whole third.")])

# ------------------------------------------------------------------ 3 Expression Builder
tool("expression-builder", "numerical-expressions-patterns", "Expression Builder",
     "Type or tap to build numerical expressions with parentheses, brackets and braces, then watch them evaluated one step at a time.",
     "Build an expression with the buttons (or type it). Press Evaluate to see each step in order.", ["Order of operations", "Grouping symbols", "Expressions"],
     """<div class="g5-field"><label for="exIn">Expression</label><input type="text" id="exIn" value="2 × [5 + (6 − 2)]" autocomplete="off" style="font-size:1.4rem"></div>
<div class="g5-actions" id="exKeys"></div>
<div class="g5-actions"><button class="g5-btn green" id="exGo">Evaluate step by step</button><button class="g5-btn alt" id="exBack">⌫</button><button class="g5-btn alt" id="exClr">Clear</button></div>
<ol class="ts-out" id="exSteps" aria-live="polite" style="padding-left:2rem"></ol>""",
     r"""
var used={};function reset(){TOOL.$('exIn').value='2 × [5 + (6 − 2)]';TOOL.$('exSteps').innerHTML='';used={};TOOL.update(O,{v:null,used:used,depth:0});}
var KEYS=['7','8','9','+','(',')','4','5','6','−','[',']','1','2','3','×','{','}','0','÷',' '];
TOOL.$('exKeys').innerHTML=KEYS.map(function(k){return '<button class="g5-btn alt" style="min-width:3rem" data-k="'+k+'">'+(k===' '?'space':k)+'</button>'}).join('');
Array.prototype.forEach.call(document.querySelectorAll('#exKeys button'),function(b){b.onclick=function(){var i=TOOL.$('exIn');i.value+=(/[0-9]/.test(b.dataset.k)&&/[0-9]$/.test(i.value)?'':(i.value&&!/[ (\[{]$/.test(i.value)&&!/[)\]}]/.test(b.dataset.k)?' ':''))+b.dataset.k;i.focus();}});
TOOL.$('exBack').onclick=function(){var i=TOOL.$('exIn');i.value=i.value.replace(/\s*\S\s*$/,'');};TOOL.$('exClr').onclick=function(){TOOL.$('exIn').value='';};
function R(n,d){d=d||1;var g=TOOL.gcd(n,d)||1;if(d<0){n=-n;d=-d;}return {n:n/g,d:d/g};}
function fmt(x){return x.d===1?String(x.n):(Math.abs(x.n)>x.d?TOOL.mixed(x.n,x.d):TOOL.frac(x.n,x.d));}
function lex(s){var t=[],m,re=/\s*(\d+|[-−+×*÷/()\[\]{}])\s*/g,pos=0;s=s.trim();while(pos<s.length){re.lastIndex=pos;m=re.exec(s);if(!m||m.index!==pos)throw Error('I don’t understand “'+s.slice(pos,pos+3)+'”.');var v=m[1];if(/\d/.test(v))t.push({n:R(+v)});else t.push({o:{'-':'−','*':'×','/':'÷'}[v]||v});pos=re.lastIndex;}return t;}
var OPEN='([{',CLOSE=')]}';
function show(t,hi){return t.map(function(x,i){var s=x.n?fmt(x.n):x.o;return hi&&i>=hi[0]&&i<=hi[1]?'<mark style="background:#FDE68A;border-radius:6px;padding:0 3px">'+s+'</mark>':s;}).join(' ');}
function opAt(t,a,b,ops){for(var i=a+1;i<b;i++)if(t[i].o&&ops.indexOf(t[i].o)>=0&&t[i-1].n&&t[i+1].n)return i;return -1;}
function apply(x,o,y){if(o==='+')return R(x.n*y.d+y.n*x.d,x.d*y.d);if(o==='−')return R(x.n*y.d-y.n*x.d,x.d*y.d);if(o==='×')return R(x.n*y.n,x.d*y.d);if(y.n===0)throw Error('You can’t divide by 0.');return R(x.n*y.d,x.d*y.n);}
function check(t){var st=[];t.forEach(function(x){if(x.o&&OPEN.indexOf(x.o)>=0)st.push(x.o);if(x.o&&CLOSE.indexOf(x.o)>=0){var o=st.pop();if(OPEN.indexOf(o)!==CLOSE.indexOf(x.o))throw Error('The grouping symbols don’t match.');}});if(st.length)throw Error('A grouping symbol is not closed.');
 for(var i=0;i<t.length;i++){var a=t[i],b=t[i+1];if(b&&a.n&&b.n)throw Error('Two numbers are next to each other; add an operation.');if(b&&a.o&&b.o&&'+−×÷'.indexOf(a.o)>=0&&'+−×÷'.indexOf(b.o)>=0)throw Error('Two operations are next to each other.');}
 if(!t.length||(t[0].o&&OPEN.indexOf(t[0].o)<0)||(t[t.length-1].o&&CLOSE.indexOf(t[t.length-1].o)<0))throw Error('An expression must start and end with a number or a grouping symbol.');}
function depth(t){var d=0,m=0;t.forEach(function(x){if(x.o&&OPEN.indexOf(x.o)>=0){d++;m=Math.max(m,d)}if(x.o&&CLOSE.indexOf(x.o)>=0)d--;});return m;}
function step(t){var open=-1;for(var i=0;i<t.length;i++){if(t[i].o&&OPEN.indexOf(t[i].o)>=0)open=i;if(t[i].o&&CLOSE.indexOf(t[i].o)>=0){var a=open,b=i;break;}}
 if(a===undefined){a=-1;b=t.length;}
 if(a>=0&&b-a===2)return {t:t.slice(0,a).concat([t[a+1]]).concat(t.slice(b+1)),hi:[a,b],why:'Remove the grouping symbols around a single number.'};
 var k=opAt(t,a,b,['×','÷']),why=k>=0?'Multiply or divide (left to right)':'Add or subtract (left to right)';if(k<0)k=opAt(t,a,b,['+','−']);
 var v=apply(t[k-1].n,t[k].o,t[k+1].n);return {t:t.slice(0,k-1).concat([{n:v}]).concat(t.slice(k+2)),hi:[k-1,k+1],why:(a>=0?'Inside '+t[a].o+' '+t[b].o+': ':'')+why+'.'};}
TOOL.$('exGo').onclick=function(){var out=TOOL.$('exSteps');try{var t=lex(TOOL.$('exIn').value);check(t);var d=depth(t),lines=[],guard=0;var orig=t;
 while(t.length>1&&guard++<60){var s=step(t);lines.push('<li>'+show(t,s.hi)+'<br><span class="g5-note">'+s.why+'</span></li>');t=s.t;}
 lines.push('<li><b>= '+fmt(t[0].n)+'</b></li>');out.innerHTML=lines.join('');var key=orig.filter(function(x){return x.n}).map(function(x){return x.n.n}).sort().join(',');used[key]=used[key]||{};used[key][fmt(t[0].n)]=1;
 TOOL.update(O,{v:t[0].n,depth:d,used:used,src:TOOL.$('exIn').value,ops:orig.filter(function(x){return x.o&&'+−×÷'.indexOf(x.o)>=0}).length});}catch(e){out.innerHTML='<li style="color:#9A3412">'+e.message+'</li>';}};
TOOL.$('exIn').onkeydown=function(e){if(e.key==='Enter')TOOL.$('exGo').click();};
var O={title:'Expression Builder',reset:reset,challenges:[
 {text:'Evaluate the starting expression 2 × [5 + (6 − 2)].',test:function(s){return s.v&&s.v.n===18&&s.v.d===1&&/\[/.test(s.src||'')}},
 {text:'Build an expression with ( ), [ ] AND { } and evaluate it.',test:function(s){return s.depth>=3}},
 {text:'Build an expression that equals exactly 20 using at least three operations.',test:function(s){return s.v&&s.v.n===20&&s.v.d===1&&s.ops>=3}},
 {text:'Use the same numbers, but move the parentheses to get a different answer.',test:function(s){return Object.keys(s.used||{}).some(function(k){return Object.keys(s.used[k]).length>=2})}},
 {text:'Build an expression whose value is a fraction (not a whole number).',test:function(s){return s.v&&s.v.d>1}}],
 notice:['Work from the inside out: ( ) first, then [ ], then { }.','Inside each group: multiply and divide left to right, then add and subtract left to right.','Moving the grouping symbols can change the value even with the same numbers.','3 × (a + b) is always 3 times as large as (a + b).']};
TOOL.init(O);reset();""",
     [("Evaluate 4 + 3 × 2. What is done first?", "3 × 2 first; the answer is 10."), ("Evaluate (4 + 3) × 2.", "14"), ("Evaluate 2 × [5 + (6 − 2)]. List the steps.", "6 − 2 = 4; 5 + 4 = 9; 2 × 9 = 18"),
      ("Evaluate {20 − [3 × (4 − 1)]} ÷ 11.", "1"), ("Put parentheses in 3 + 5 × 2 to make it equal 16.", "(3 + 5) × 2"), ("Write an expression for: add 8 and 7, then multiply by 2.", "(8 + 7) × 2 = 30"),
      ("How does 3 × (125 + 48) compare with 125 + 48?", "3 times as large"), ("Reflect: Why do we need grouping symbols?", "They show which part to do first, so everyone gets the same answer.")])

# ------------------------------------------------------------------ 4 Fraction Explorer
tool("fraction-explorer", "fraction-addition-subtraction", "Fraction Explorer",
     "Build two fractions with fraction bars, find equivalent fractions and a common denominator, and compare, add or subtract them.",
     "Change the numerators and denominators. Choose Compare, Add or Subtract to see the common denominator at work.", ["Fractions", "Equivalent fractions", "Common denominators"],
     """<div class="g5-row"><div class="g5-field"><label>Fraction A</label><div class="ts-step"><button data-k="a" data-s="-1" aria-label="A numerator down">−</button><b id="fxa"></b><button data-k="a" data-s="1" aria-label="A numerator up">+</button> / <button data-k="b" data-s="-1" aria-label="A denominator down">−</button><b id="fxb"></b><button data-k="b" data-s="1" aria-label="A denominator up">+</button></div></div>
<div class="g5-field"><label>Fraction B</label><div class="ts-step"><button data-k="c" data-s="-1" aria-label="B numerator down">−</button><b id="fxc"></b><button data-k="c" data-s="1" aria-label="B numerator up">+</button> / <button data-k="d" data-s="-1" aria-label="B denominator down">−</button><b id="fxd"></b><button data-k="d" data-s="1" aria-label="B denominator up">+</button></div></div>
<div class="g5-field"><label for="fxOp">Do this</label><select id="fxOp"><option value="cmp">Compare</option><option value="add">Add</option><option value="sub">Subtract</option></select></div></div>
<div class="ts-model" id="fxModel"></div><div class="ts-out" id="fxOut" aria-live="polite"></div>""",
     r"""
var f;function reset(){f={a:1,b:2,c:1,d:3};TOOL.$('fxOp').value='add';draw();}
function lcm(a,b){return a*b/TOOL.gcd(a,b);}
function draw(){['a','b','c','d'].forEach(function(k){TOOL.$('fx'+k).textContent=f[k]});var op=TOOL.$('fxOp').value,L=lcm(f.b,f.d),A=f.a*L/f.b,C=f.c*L/f.d;
 var rows=[{d:f.b,n:f.a,color:'#3B82F6',label:f.a+'/'+f.b},{d:f.d,n:f.c,color:'#F59E0B',label:f.c+'/'+f.d},{d:L,n:Math.min(A,L),color:'#93C5FD',label:A+'/'+L},{d:L,n:Math.min(C,L),color:'#FCD34D',label:C+'/'+L}];
 var res,txt;if(op==='add'){res=A+C;txt=TOOL.frac(f.a,f.b)+' + '+TOOL.frac(f.c,f.d)+' = '+TOOL.frac(A,L)+' + '+TOOL.frac(C,L)+' = '+TOOL.frac(res,L)+' = <b>'+TOOL.mixed(res,L)+'</b>';}
 else if(op==='sub'){res=A-C;txt=res<0?'The second fraction is bigger. Try switching them!':TOOL.frac(f.a,f.b)+' − '+TOOL.frac(f.c,f.d)+' = '+TOOL.frac(A,L)+' − '+TOOL.frac(C,L)+' = '+TOOL.frac(res,L)+' = <b>'+(res===0?'0':TOOL.mixed(res,L))+'</b>';}
 else{txt=TOOL.frac(f.a,f.b)+' = '+TOOL.frac(A,L)+' and '+TOOL.frac(f.c,f.d)+' = '+TOOL.frac(C,L)+', so <b>'+TOOL.frac(f.a,f.b)+' '+(A>C?'&gt;':A<C?'&lt;':'=')+' '+TOOL.frac(f.c,f.d)+'</b>';}
 if(op!=='cmp'&&res>=0&&res<=2*L){var whole=Math.floor(res/L),rem=res%L,rr=[];for(var w=0;w<whole;w++)rr.push({d:L,n:L,color:'#10B981',label:w===whole-1&&!rem?TOOL.mixed(res,L).replace(/<[^>]+>/g,'')+'':''});if(rem||!whole)rr.push({d:L,n:rem,color:'#10B981',label:''});rows=rows.concat(rr);}
 TOOL.$('fxModel').innerHTML=G5FIGS.fbars(rows.map(function(r){return {d:r.d,n:r.n,color:r.color,label:r.label}}),{width:460,rowH:28});
 TOOL.$('fxOut').innerHTML='<span class="g5-note">Least common denominator: '+L+'</span><br>'+txt;
 TOOL.update(O,{f:f,op:op,A:A,C:C,L:L,res:res});}
Array.prototype.forEach.call(document.querySelectorAll('#tool .ts-step button'),function(b){b.onclick=function(){var k=b.dataset.k;f[k]+=+b.dataset.s;f.b=Math.max(1,Math.min(12,f.b));f.d=Math.max(1,Math.min(12,f.d));f.a=Math.max(0,Math.min(f.b,f.a));f.c=Math.max(0,Math.min(f.d,f.c));draw();}});
TOOL.$('fxOp').onchange=draw;
var O={title:'Fraction Explorer',reset:reset,challenges:[
 {text:'Show two equivalent fractions with different denominators.',test:function(s){return s.f.a*s.f.d===s.f.b*s.f.c&&s.f.b!==s.f.d&&s.f.a>0}},
 {text:'Add two fractions with unlike denominators.',test:function(s){return s.op==='add'&&s.f.b!==s.f.d&&s.f.a>0&&s.f.c>0}},
 {text:'Find two unlike fractions whose sum is exactly 1.',test:function(s){return s.op==='add'&&s.f.b!==s.f.d&&s.res===s.L}},
 {text:'Make a subtraction whose answer is 1/6.',test:function(s){return s.op==='sub'&&s.res*6===s.L}},
 {text:'Compare: find a case where the fraction with the bigger denominator is the bigger fraction.',test:function(s){return s.op==='cmp'&&((s.f.d>s.f.b&&s.C>s.A)||(s.f.b>s.f.d&&s.A>s.C))}}],
 notice:['To add or subtract, the parts must be the same size: rename with a common denominator.','Equivalent fractions name the same amount with different-sized parts.','Add only the numerators; the common denominator stays the same.','1/2 + 1/3 is 5/6, not 2/5.']};
TOOL.init(O);reset();""",
     [("Show 1/2 and 1/3. What is the least common denominator?", "6"), ("Find 1/2 + 1/3.", "5/6"), ("Find 3/4 − 1/6.", "7/12"), ("Which is greater: 3/5 or 5/8?", "5/8 (24/40 < 25/40)"),
      ("Find two different fractions that are equivalent to 2/3.", "Examples: 4/6, 6/9, 8/12"), ("Find 2/3 + 3/4. Write the answer as a mixed number.", "1 5/12"),
      ("Explain why 1/2 + 1/3 is not 2/5.", "2/5 is less than 1/2, but adding 1/3 must make the sum bigger than 1/2."), ("Reflect: Why do we need a common denominator?", "So that we are adding parts of the same size.")])

# ------------------------------------------------------------------ 5 Measurement Converter
tool("measurement-converter", "measurement-conversions", "Measurement Converter",
     "Convert customary and metric measurements, see the conversion fact as a picture, and decide when to multiply or divide.",
     "Pick a kind of measurement, type an amount, and choose the units. The picture shows how many small units fit in one big unit.", ["Measurement", "Unit conversion", "Customary and metric units"],
     """<div class="g5-row"><div class="g5-field"><label for="mcKind">Measure</label><select id="mcKind"></select></div><div class="g5-field"><label for="mcAmt">Amount</label><input type="number" id="mcAmt" value="3" min="0" step="any"></div>
<div class="g5-field"><label for="mcFrom">From</label><select id="mcFrom"></select></div><div class="g5-field"><label for="mcTo">To</label><select id="mcTo"></select></div></div>
<div class="ts-big" id="mcRes" aria-live="polite"></div><div class="ts-out" id="mcSteps"></div><div class="ts-model" id="mcPic"></div>""",
     r"""
var K={'Customary length':{u:{in:1,ft:12,yd:36,mi:63360},names:{in:'inches',ft:'feet',yd:'yards',mi:'miles'}},'Customary weight':{u:{oz:1,lb:16,T:32000},names:{oz:'ounces',lb:'pounds',T:'tons'}},
'Customary capacity':{u:{'fl oz':1,c:8,pt:16,qt:32,gal:128},names:{'fl oz':'fluid ounces',c:'cups',pt:'pints',qt:'quarts',gal:'gallons'}},'Metric length':{u:{mm:1,cm:10,m:1000,km:1000000},names:{mm:'millimeters',cm:'centimeters',m:'meters',km:'kilometers'}},
'Metric mass':{u:{g:1,kg:1000},names:{g:'grams',kg:'kilograms'}},'Metric capacity':{u:{mL:1,L:1000},names:{mL:'milliliters',L:'liters'}}};
var st={big2small:0,small2big:0,seen:{}};
function fill(){var k=K[TOOL.$('mcKind').value],keys=Object.keys(k.u);TOOL.$('mcFrom').innerHTML=keys.map(function(u){return '<option value="'+u+'">'+k.names[u]+' ('+u+')</option>'}).join('');TOOL.$('mcTo').innerHTML=TOOL.$('mcFrom').innerHTML;TOOL.$('mcFrom').value=keys[1];TOOL.$('mcTo').value=keys[0];}
function reset(){TOOL.$('mcKind').innerHTML=Object.keys(K).map(function(k){return '<option>'+k+'</option>'}).join('');TOOL.$('mcKind').value='Customary length';fill();TOOL.$('mcAmt').value=3;st={big2small:0,small2big:0,seen:{}};draw();}
function dec(n){var s=(Math.round(n*1e6)/1e6).toLocaleString('en-US',{maximumFractionDigits:6});return s;}
function draw(){var kn=TOOL.$('mcKind').value,k=K[kn],a=+TOOL.$('mcAmt').value,fr=TOOL.$('mcFrom').value,to=TOOL.$('mcTo').value,f=k.u[fr],t=k.u[to];
 if(!(a>=0)){TOOL.$('mcRes').textContent='Type an amount';return;}
 var res=a*f/t,metric=/Metric/.test(kn),fact,step;
 if(f===t){fact='Same unit';step='No conversion needed.';}
 else if(f>t){var r=f/t;fact='1 '+fr+' = '+r.toLocaleString('en-US')+' '+to;step='Bigger unit → smaller unit, so <b>multiply</b>: '+dec(a)+' × '+r.toLocaleString('en-US')+' = '+dec(res);st.big2small++;}
 else{var r2=t/f;fact='1 '+to+' = '+r2.toLocaleString('en-US')+' '+fr;step='Smaller unit → bigger unit, so <b>divide</b>: '+dec(a)+' ÷ '+r2.toLocaleString('en-US')+' = '+dec(res);st.small2big++;}
 var extra='';if(!metric&&f<t&&res%1){var whole=Math.floor(res),left=Math.round((res-whole)*t/f*1e6)/1e6;extra='<br>That is also <b>'+whole+' '+to+' '+dec(left)+' '+fr+'</b>.';}
 TOOL.$('mcRes').textContent=dec(a)+' '+fr+' = '+dec(res)+' '+to;TOOL.$('mcSteps').innerHTML='<b>Fact:</b> '+fact+'<br>'+step+extra;
 var big=f>t?fr:to,small=f>t?to:fr,n=k.u[big]/k.u[small];
 TOOL.$('mcPic').innerHTML=f===t?'':(n<=16?G5FIGS.fbars([{d:1,n:1,color:'#14B8A6',label:''},{d:n,n:n,color:'#F59E0B',label:''}],{width:460,rowH:30})+'<p class="g5-note">Top: 1 '+k.names[big].replace(/s$/,'')+'. Bottom: '+n+' '+k.names[small]+'.</p>':'<p class="g5-note">1 '+k.names[big].replace(/s$/,'')+' = '+n.toLocaleString('en-US')+' '+k.names[small]+' (too many to draw!)</p>');
 st.seen[kn+':'+fr+'>'+to]=res;TOOL.update(O,{kn:kn,fr:fr,to:to,a:a,res:res,st:st});}
['mcAmt','mcFrom','mcTo'].forEach(function(id){TOOL.$(id).oninput=draw;});TOOL.$('mcKind').onchange=function(){fill();draw();};
var O={title:'Measurement Converter',reset:reset,challenges:[
 {text:'Convert 3 feet to inches.',test:function(s){return s.fr==='ft'&&s.to==='in'&&s.a===3}},
 {text:'Convert from a smaller unit to a bigger unit.',test:function(s){return s.st.small2big>0}},
 {text:'Find how many cups are in 1 gallon.',test:function(s){return s.fr==='gal'&&s.to==='c'&&s.a===1}},
 {text:'Convert 5 centimeters to meters.',test:function(s){return s.fr==='cm'&&s.to==='m'&&s.a===5}},
 {text:'Find a measurement that converts to 2,000 of a smaller unit.',test:function(s){return s.res===2000&&s.a<2000}}],
 notice:['Bigger unit → smaller unit: multiply. Smaller unit → bigger unit: divide.','Metric units use powers of 10, so the digits just move places.','1 ft = 12 in, 1 yd = 3 ft, 1 lb = 16 oz, 1 gal = 4 qt, 1 qt = 2 pt, 1 pt = 2 c.','The amount gets bigger when you change to a smaller unit.']};
TOOL.init(O);reset();""",
     [("Convert 3 ft to inches.", "36 in"), ("Convert 50 in to feet and inches.", "4 ft 2 in"), ("How many cups are in 1 gallon?", "16 cups"), ("Convert 2.5 kg to grams.", "2,500 g"),
      ("Convert 350 cm to meters.", "3.5 m"), ("Convert 3 lb 4 oz to ounces.", "52 oz"), ("When do you multiply to convert? When do you divide?", "Multiply going to a smaller unit; divide going to a bigger unit."),
      ("Reflect: Why does the number get bigger when you change feet to inches?", "Inches are smaller, so it takes more of them to make the same length.")])

# ------------------------------------------------------------------ 6 Volume Builder
tool("volume-builder", "volume-three-dimensional-figures", "Volume Builder",
     "Stack unit cubes into rectangular prisms, see layers and base area, and connect counting cubes to V = l × w × h and composite figures.",
     "Use the sliders to set length, width and height. Turn on a second prism to build a composite figure.", ["Volume", "Unit cubes", "Composite figures"],
     """<div class="g5-row"><div class="g5-field"><label for="vbL">Length: <b id="vbLv"></b></label><input type="range" id="vbL" min="1" max="8" value="4"></div><div class="g5-field"><label for="vbW">Width: <b id="vbWv"></b></label><input type="range" id="vbW" min="1" max="6" value="3"></div><div class="g5-field"><label for="vbH">Height: <b id="vbHv"></b></label><input type="range" id="vbH" min="1" max="6" value="2"></div></div>
<label class="g5-chip"><input type="checkbox" id="vbTwo"> Add a second prism</label>
<div class="g5-row g5-hidden" id="vbTwoRow"><div class="g5-field"><label for="vbL2">Length 2: <b id="vbL2v"></b></label><input type="range" id="vbL2" min="1" max="6" value="2"></div><div class="g5-field"><label for="vbH2">Height 2: <b id="vbH2v"></b></label><input type="range" id="vbH2" min="1" max="6" value="4"></div></div>
<div class="g5-row" style="justify-content:center;align-items:flex-end" id="vbModel"></div><div class="ts-out" id="vbOut" aria-live="polite"></div>""",
     r"""
var ids=['vbL','vbW','vbH','vbL2','vbH2'],made={};function reset(){TOOL.$('vbL').value=4;TOOL.$('vbW').value=3;TOOL.$('vbH').value=2;TOOL.$('vbL2').value=2;TOOL.$('vbH2').value=4;TOOL.$('vbTwo').checked=false;made={};draw();}
function draw(){var l=+TOOL.$('vbL').value,w=+TOOL.$('vbW').value,h=+TOOL.$('vbH').value,two=TOOL.$('vbTwo').checked,l2=+TOOL.$('vbL2').value,h2=+TOOL.$('vbH2').value;
 ids.forEach(function(i){TOOL.$(i+'v').textContent=TOOL.$(i).value});TOOL.$('vbTwoRow').classList.toggle('g5-hidden',!two);
 var v1=l*w*h,v2=two?l2*w*h2:0;TOOL.$('vbModel').innerHTML='<div style="flex:1 1 260px">'+G5FIGS.cubes(l,w,h,{color:'#3B82F6'})+'<p class="g5-note">Prism A</p></div>'+(two?'<div style="flex:1 1 200px">'+G5FIGS.cubes(l2,w,h2,{color:'#F59E0B'})+'<p class="g5-note">Prism B (same width)</p></div>':'');
 TOOL.$('vbOut').innerHTML='Prism A: base layer '+l+' × '+w+' = <b>'+(l*w)+'</b> cubes; '+h+' layer'+(h>1?'s':'')+'; V = '+l+' × '+w+' × '+h+' = <b>'+v1+' cubic units</b>'+(two?'<br>Prism B: V = '+l2+' × '+w+' × '+h2+' = <b>'+v2+' cubic units</b><br>Composite figure: '+v1+' + '+v2+' = <b>'+(v1+v2)+' cubic units</b>':'');
 if(!two)made[l+'x'+w+'x'+h]=v1;TOOL.update(O,{l:l,w:w,h:h,v:v1,two:two,total:v1+v2,made:made});}
ids.forEach(function(i){TOOL.$(i).oninput=draw;});TOOL.$('vbTwo').onchange=draw;
var O={title:'Volume Builder',reset:reset,challenges:[
 {text:'Build a prism with a volume of 24 cubic units.',test:function(s){return !s.two&&s.v===24}},
 {text:'Build volume 24 a second, different way.',test:function(s){return Object.keys(s.made).filter(function(k){return s.made[k]===24}).length>=2}},
 {text:'Build a cube with 27 unit cubes.',test:function(s){return !s.two&&s.l===3&&s.w===3&&s.h===3}},
 {text:'Make a base area of 12 and a height of 3.',test:function(s){return !s.two&&s.l*s.w===12&&s.h===3}},
 {text:'Build a composite figure with a total volume of 40 cubic units.',test:function(s){return s.two&&s.total===40}}],
 notice:['Volume = cubes in one layer × number of layers = l × w × h = B × h.','Different prisms can have the same volume.','Volume is additive: add the volumes of parts that do not overlap.','Volume is measured in cubic units.']};
TOOL.init(O);reset();""",
     [("Build 4 × 3 × 2. How many cubes are in the bottom layer?", "12"), ("What is the volume of 4 × 3 × 2?", "24 cubic units"), ("Find two different prisms with volume 36.", "Examples: 6 × 3 × 2, 4 × 3 × 3"),
      ("A prism has base area 15 and height 4. What is its volume?", "60 cubic units"), ("Build a composite figure: Prism A 3 × 2 × 4 and Prism B 2 × 2 × 2. Total volume?", "32 cubic units"),
      ("Why do we use cubic units for volume?", "Volume counts cubes that fill space in three directions."), ("If you double the height, what happens to the volume?", "It doubles."),
      ("Reflect: Explain why l × w × h counts every cube, even hidden ones.", "l × w counts one full layer, and h counts how many layers are stacked.")])

# ------------------------------------------------------------------ 7 Coordinate Plane Explorer
tool("coordinate-explorer", "coordinate-plane-graphing", "Coordinate Plane Explorer",
     "Plot points in the first quadrant by clicking or typing, connect them into shapes, measure distances along grid lines, and graph two-rule patterns.",
     "Click the grid (or type an ordered pair) to plot points. Turn on Connect to make a shape, or make points from two patterns.", ["Coordinate plane", "Ordered pairs", "Patterns"],
     """<div class="g5-row"><div class="g5-field"><label for="cpX">x</label><input type="number" id="cpX" min="0" max="10" value="3"></div><div class="g5-field"><label for="cpY">y</label><input type="number" id="cpY" min="0" max="10" value="5"></div>
<div class="g5-actions" style="margin:0"><button class="g5-btn" id="cpPlot">Plot point</button><button class="g5-btn alt" id="cpUndo">Undo</button><label class="g5-chip"><input type="checkbox" id="cpConnect"> Connect</label></div></div>
<div class="g5-row"><div class="g5-field"><label for="cpRa">Pattern: x adds</label><input type="number" id="cpRa" min="1" max="5" value="1"></div><div class="g5-field"><label for="cpRb">y adds</label><input type="number" id="cpRb" min="1" max="5" value="2"></div><div class="g5-actions" style="margin:0"><button class="g5-btn alt" id="cpPat">Make pattern points</button></div></div>
<div class="ts-model" id="cpGrid" style="max-width:520px;margin:auto"></div><div class="ts-out" id="cpOut" aria-live="polite"></div>""",
     r"""
var P=[],st={pattern:false};function reset(){P=[];st={pattern:false};TOOL.$('cpConnect').checked=false;draw();}
function add(x,y){if(x<0||y<0||x>10||y>10||x%1||y%1)return alert('Use whole numbers from 0 to 10.');if(P.some(function(p){return p[0]===x&&p[1]===y}))return;P.push([x,y]);draw();}
function draw(){var L='ABCDEFGHIJKLMNOP';TOOL.$('cpGrid').innerHTML=G5FIGS.q1({max:10,cell:44,points:P.map(function(p,i){return [p[0],p[1],L[i]||'']}),poly:TOOL.$('cpConnect').checked&&P.length>2?P:null,segs:TOOL.$('cpConnect').checked&&P.length===2?[[P[0][0],P[0][1],P[1][0],P[1][1]]]:[]});
 var svg=TOOL.$('cpGrid').querySelector('svg');svg.style.cursor='crosshair';svg.onclick=function(e){var r=svg.getBoundingClientRect(),vb=svg.viewBox.baseVal,sx=(e.clientX-r.left)*vb.width/r.width,sy=(e.clientY-r.top)*vb.height/r.height,x=Math.round((sx-30)/44),y=Math.round((vb.height-26-sy)/44);add(x,y);};
 var out=P.map(function(p,i){return '<b>'+(L[i]||'')+'</b> ('+p[0]+', '+p[1]+')'}).join(' · ')||'No points yet.';
 if(P.length>=2){var a=P[P.length-2],b=P[P.length-1];if(a[0]===b[0])out+='<br>The last two points are on the same vertical line: '+Math.abs(a[1]-b[1])+' units apart.';else if(a[1]===b[1])out+='<br>The last two points are on the same horizontal line: '+Math.abs(a[0]-b[0])+' units apart.';}
 TOOL.$('cpOut').innerHTML=out;TOOL.update(O,{P:P,st:st,connect:TOOL.$('cpConnect').checked});}
TOOL.$('cpPlot').onclick=function(){add(+TOOL.$('cpX').value,+TOOL.$('cpY').value);};TOOL.$('cpUndo').onclick=function(){P.pop();draw();};TOOL.$('cpConnect').onchange=draw;
TOOL.$('cpPat').onclick=function(){var a=+TOOL.$('cpRa').value,b=+TOOL.$('cpRb').value;P=[];for(var i=0;i*a<=10&&i*b<=10;i++)P.push([i*a,i*b]);st.pattern={a:a,b:b};draw();};
function isRect(P){if(P.length!==4)return false;var xs=P.map(function(p){return p[0]}),ys=P.map(function(p){return p[1]}),ux=xs.filter(function(v,i){return xs.indexOf(v)===i}),uy=ys.filter(function(v,i){return ys.indexOf(v)===i});if(ux.length!==2||uy.length!==2)return false;return ux.every(function(x){return uy.every(function(y){return P.some(function(p){return p[0]===x&&p[1]===y})})});}
var O={title:'Coordinate Plane Explorer',reset:reset,challenges:[
 {text:'Plot the point (3, 5).',test:function(s){return s.P.some(function(p){return p[0]===3&&p[1]===5})}},
 {text:'Plot a point on the x-axis (not the origin).',test:function(s){return s.P.some(function(p){return p[1]===0&&p[0]>0})}},
 {text:'Plot two points that are 6 units apart on the same horizontal line.',test:function(s){return s.P.some(function(a){return s.P.some(function(b){return a[1]===b[1]&&Math.abs(a[0]-b[0])===6})})}},
 {text:'Plot 4 points that are the corners of a rectangle, then connect them.',test:function(s){return s.connect&&isRect(s.P)}},
 {text:'Make pattern points where each y-value is 3 times its x-value.',test:function(s){return s.st.pattern&&s.st.pattern.b===3*s.st.pattern.a}}],
 notice:['The first number tells how far to move right; the second tells how far to move up.','(3, 5) and (5, 3) are different points.','Points on the same horizontal line have the same y-coordinate; subtract the x-coordinates to find the distance.','When x adds a and y adds b, the points line up in a straight path.']};
TOOL.init(O);reset();""",
     [("Plot (2, 7). Describe how you moved from the origin.", "2 units right, then 7 units up"), ("Plot (7, 2). Is it the same point as (2, 7)?", "No"), ("Plot (1, 4) and (8, 4). How far apart are they?", "7 units"),
      ("Plot three corners of a rectangle: (2, 1), (6, 1), (6, 5). Where is the fourth corner?", "(2, 5)"), ("What is the perimeter of that rectangle?", "16 units"),
      ("Make pattern points with x adds 2 and y adds 4. List the first three points.", "(0, 0), (2, 4), (4, 8)"),
      ("In those pattern points, how does y compare with x?", "y is 2 times x"), ("Reflect: Why does the order of the numbers in an ordered pair matter?", "The first number is the move right and the second is the move up; switching them gives a different point.")])


def main():
    man = []
    for t in TOOLS:
        d = os.path.join(ROOT, "artifacts", t["slug"])
        os.makedirs(d, exist_ok=True)
        html = HEAD.format(title=t["title"], desc=t["description"], intro=t["intro"], body=t["body"], script=t["script"])
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
        man.append({k: t[k] for k in ("slug", "unit", "title", "description", "topics", "worksheet")})
    json.dump({"tools": man}, open(os.path.join(os.path.dirname(__file__), "manifest.json"), "w"), indent=1, ensure_ascii=False)
    print("tools written:", len(man))


if __name__ == "__main__":
    main()
