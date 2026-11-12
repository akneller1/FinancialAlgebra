(function(){
'use strict';
const $=id=>document.getElementById(id);
/* Courses and units come from the shared curriculum catalog (MKMENU.CATALOG, extended from data.js by
   menu/course-catalog-bridge.js). A unit is offered when a vocabulary bank exists for it, so new
   courses appear without another hand-kept list here. */
const bankId=id=>window.MKVOCAB_BANK_ID?window.MKVOCAB_BANK_ID(id):id;
const bankText=id=>(window.MKVOCAB_BANKS||{})[bankId(id)]||'';
const catalog=((window.MKMENU&&MKMENU.CATALOG)||[]).map(g=>({course:g.course,units:g.units.filter(u=>bankText(u[0]))})).filter(g=>g.units.length);
const math=value=>window.MK_MATH_DISPLAY?window.MK_MATH_DISPLAY.html(value):esc(value);
const types=[['match','Matching',5],['blank','Fill in the blank',4],['draw','Draw / illustrate',2],['example','Write an example',2],['cross','Crossword',8]];
let selected=[],last=null,turn=0;
const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const shuffle=a=>{let b=a.slice();for(let i=b.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]}return b};
const parse=(str)=>String(str||'').split(';').filter(Boolean).map((row,i)=>{let [term,definition,example,draw]=row.split('|');return {id:'bank'+i,term:term.trim(),definition:(definition||'').trim(),example:(example||'').trim(),draw:(draw||'').trim()}});
const crosswordUnitIds=()=>Array.from(document.querySelectorAll('#crossUnits input:checked')).map(x=>x.value);
function crossVocabulary(){
 const units=crosswordUnitIds(),seen=new Set(),out=[];
 units.forEach(id=>parse(bankText(id)).forEach(t=>{
   const key=normalize(t.term);
   if(key.length<3||key.length>23||seen.has(key)||!t.definition)return;
   seen.add(key);out.push({...t,id:id+':'+t.id,unitId:id});
 }));
 // Add teacher-authored vocabulary without repeating words already in a selected unit.
 $('custom').value.split('\n').filter(x=>x.includes('|')).forEach((line,i)=>{
   const [term,definition,example,draw]=line.split('|'),key=normalize(term||'');
   if(key.length<3||key.length>23||!definition||seen.has(key))return;
   seen.add(key);out.push({id:'custom:'+i,term:term.trim(),definition:definition.trim(),example:(example||'').trim(),draw:(draw||'').trim()});
 });
 return out;
}
function loadCrossUnits(){
 const c=catalog.find(x=>x.course===$('course').value),units=c?c.units:[];
 const chosen=crosswordUnitIds();
 $('crossUnits').innerHTML=units.map(x=>'<label><input type="checkbox" value="'+esc(x[0])+'" '+(chosen.includes(x[0])||!chosen.length&&x[0]===$('unit').value?'checked':'')+'> '+esc(x[1])+'</label>').join('');
 $('crossUnits').querySelectorAll('input').forEach(x=>x.onchange=updateCrossCount);
 updateCrossCount();
}
function updateCrossCount(){
 const n=crossVocabulary().length;
 $('crossCount').textContent=crosswordUnitIds().length+' units · '+n+' unique crossword words available';
}
const current=()=>{let id=$('unit').value,source=parse(bankText(id)),extra=$('custom').value.split('\n').filter(x=>x.includes('|')).map((r,i)=>{let [term,definition,example,draw]=r.split('|');return {id:'extra'+i,term:term.trim(),definition:(definition||'').trim(),example:(example||'').trim(),draw:(draw||'').trim()}});return source.filter(x=>selected.includes(x.id)).concat(extra).filter(x=>x.term&&x.definition)};
function requestedUnit(){const u=new URL(location.href).searchParams.get('unit');if(!u)return null;const all=catalog.flatMap(c=>c.units.map(x=>x[0]));if(all.includes(u))return u;return all.find(id=>bankId(id)===u)||u;}
function loadUnits(){let c=catalog.find(x=>x.course===$('course').value);$('unit').innerHTML=(c?c.units:[]).map(x=>'<option value="'+esc(x[0])+'">'+esc(x[1])+'</option>').join('');let u=requestedUnit();if(u&&Array.from($('unit').options).some(x=>x.value===u))$('unit').value=u;loadTerms();loadCrossUnits()}
function loadTerms(){const middle=/^(prealgebra7?|math[56])-/.test($('unit').value);Array.from($('level').options).forEach(o=>o.textContent=middle?({cp2:'Remedial',cp1:'Standard',honors:'Advanced'}[o.value]||o.value):o.value.toUpperCase());let all=parse(bankText($('unit').value));selected=all.map(x=>x.id);$('terms').innerHTML=all.map(x=>'<label><input type="checkbox" data-id="'+x.id+'" checked> '+esc(x.term)+'</label>').join('');$('terms').querySelectorAll('input').forEach(x=>x.addEventListener('change',()=>{selected=Array.from($('terms').querySelectorAll('input:checked')).map(x=>x.dataset.id)}))}
function config(){return Object.fromEntries(types.map(([id])=>[id,$('use_'+id).checked?Math.max(0,Math.min(20,Number($('f_'+id).value)||0)):0]))}
function fit(terms,n){return shuffle(terms).slice(0,Math.min(n,terms.length))}
function normalize(t){return t.toUpperCase().replace(/[^A-Z]/g,'')}
function crossword(terms){const items=terms.map(x=>({...x,word:normalize(x.term)})).filter(x=>x.word.length>=3&&x.word.length<=23);if(items.length<2)return null;let best=null;
for(let attempt=0;attempt<160;attempt++){let size=29,grid=Array.from({length:size},()=>Array(size).fill('')),placements=[];
 let order=shuffle(items).sort((a,b)=>b.word.length-a.word.length);
 function valid(w,r,c,d){let dr=d?1:0,dc=d?0:1;if(r<1||c<1||r+dr*(w.length-1)>=size-1||c+dc*(w.length-1)>=size-1)return -1;let before=grid[r-dr]?.[c-dc],after=grid[r+dr*w.length]?.[c+dc*w.length];if(before||after)return -1;let crosses=0;for(let k=0;k<w.length;k++){let y=r+dr*k,x=c+dc*k,v=grid[y][x];if(v&&v!==w[k])return -1;if(v){crosses++;continue}if(d){if(grid[y][x-1]||grid[y][x+1])return -1}else if(grid[y-1][x]||grid[y+1][x])return -1;}return crosses;}
 for(let idx=0;idx<order.length;idx++){let a=order[idx],poss=[];for(let d=0;d<2;d++)for(let r=1;r<size-1;r++)for(let c=1;c<size-1;c++){let hits=valid(a.word,r,c,d);if(hits>=0&&(idx===0||hits>0))poss.push({r,c,d,hits})}if(!poss.length)continue;poss.sort((a,b)=>b.hits-a.hits);let choice=idx===0?poss[Math.floor(Math.random()*Math.min(30,poss.length))]:poss[Math.floor(Math.random()*Math.min(5,poss.length))];for(let k=0;k<a.word.length;k++)grid[choice.r+choice.d*k][choice.c+(1-choice.d)*k]=a.word[k];placements.push({...choice,...a})}
 if(!best||placements.length>best.placements.length)best={grid,placements};if(placements.length===items.length)break;
}if(!best||best.placements.length!==items.length)return null;
let p=best.placements,rows=p.flatMap(x=>[x.r,x.r+(x.d?x.word.length-1:0)]),cols=p.flatMap(x=>[x.c,x.c+(x.d?0:x.word.length-1)]),r0=Math.min(...rows),r1=Math.max(...rows),c0=Math.min(...cols),c1=Math.max(...cols);
let cells=best.grid.slice(r0,r1+1).map(a=>a.slice(c0,c1+1)),starts={};p.forEach(x=>{x.r-=r0;x.c-=c0;starts[x.r+','+x.c]=true});let numbering={},i=1;for(let r=0;r<cells.length;r++)for(let c=0;c<cells[r].length;c++)if(starts[r+','+c])numbering[r+','+c]=i++;
p.forEach(x=>x.number=numbering[x.r+','+x.c]);return {cells,placements:p,numbering};}
function crossHtml(x,key){let h='<table class="crossword" aria-label="Crossword puzzle">';x.cells.forEach((line,r)=>{h+='<tr>';line.forEach((v,c)=>{h+=v?'<td>'+(x.numbering[r+','+c]?'<sup>'+x.numbering[r+','+c]+'</sup>':'')+(key?esc(v):'')+'</td>':'<td class="block"></td>'});h+='</tr>'});h+='</table><div class="clues">';[0,1].forEach(d=>{h+='<h3>'+(d?'Down':'Across')+'</h3>';x.placements.filter(p=>p.d===d).sort((a,b)=>a.number-b.number).forEach(p=>h+='<p><b>'+p.number+'.</b> '+esc(p.definition)+'</p>')});return h+'</div>'}
function modeTypes(){return types.map(x=>x[0]);}
function honorsTask(t,mode){let term=t.term.toLowerCase();let ex=t.example||t.definition;if(mode==='example'){if(/slope|rate|linear|intercept|quadratic|function|sequence|exponent|logarithm|polynomial|inequal|system|probability|statistics|correlation/.test(term))return 'Construct TWO different examples of '+t.term+'. Explain what property both satisfy and one important difference between them. Include calculations, a graph, or algebraic verification where appropriate.';if(/angle|triangle|circle|parallel|perpendicular|dilation|reflection|rotation|similar|congruen|radius|tangent|vector|distance|volume|area/.test(term))return 'Construct a labeled diagram demonstrating '+t.term+'. State the relevant theorem, definition, or relationship and justify why your diagram satisfies it.';return 'Create a nontrivial example and a convincing non-example of '+t.term+'. Justify both using the precise mathematical definition.';}if(mode==='draw')return t.draw+' Then add a second contrasting case or counterexample and explain the mathematical difference.';return 'Explain why the following is an instance of '+t.term+': '+ex+'. State the defining property, and explain a limitation or condition that matters.';}
function render(){let vocab=current(),counts=config(),allowed=modeTypes(),unit=$('unit').selectedOptions[0]?.textContent||'',level=$('level').value.toUpperCase();if(vocab.length<2 && (counts.match||counts.blank||counts.draw||counts.example)){$('status').textContent='Select at least two terms for the non-crossword activities.';return}let label=counts.cross && crosswordUnitIds().length>1?'Multi-unit':unit;let h='<h1>'+esc(label)+' · Vocabulary Review</h1><p>'+esc($('level').selectedOptions[0].textContent)+' · '+esc($('mastery').selectedOptions[0].textContent)+'</p><div class="name">Name: ______________________________ &nbsp; Date: _____________</div>',key='<div class="key"><h1>Teacher answer key</h1><p>'+esc(label)+'</p>',made=0,notes=[];
function section(label,body,answers){h+='<section><h2>'+label+'</h2>'+body+'</section>';key+='<section><h2>'+label+'</h2>'+answers+'</section>';made++;}
if(allowed.includes('match')&&counts.match){let terms=fit(vocab,counts.match),defs=shuffle(terms);section('Recognize · Matching','<p>Match each term to its definition. Write the correct letter.</p><div class="matching"><div>'+terms.map((t,i)=>'<div>____ '+(i+1)+'. '+esc(t.term)+'</div>').join('')+'</div><div>'+defs.map((t,i)=>'<div>'+String.fromCharCode(65+i)+'. '+math(t.definition)+'</div>').join('')+'</div></div>',terms.map((t,i)=>(i+1)+'. '+String.fromCharCode(65+defs.indexOf(t))).join('<br>'))}
if(allowed.includes('blank')&&counts.blank){let terms=fit(vocab,counts.blank);section('Recognize and Explain · Fill in the Blank','<p>'+(level==='HONORS'?'Identify each term precisely. After naming it, give an additional condition, limitation, or distinguishing feature.':'Write the correct term for each definition.')+'</p>'+($('wordbank').checked?'<div class="wordbank">Word bank: '+esc(shuffle(terms.map(x=>x.term)).join(' · '))+'</div>':'')+terms.map((t,i)=>'<div class="q">'+(i+1)+'. '+math(t.definition)+'<div class="answerline"></div>'+(level==='HONORS'?'<div class="answerline"></div>':'')+'</div>').join(''),terms.map((t,i)=>(i+1)+'. '+esc(t.term)+' — '+math(t.definition)).join('<br>'))}
if(allowed.includes('draw')&&counts.draw){let terms=fit(vocab.filter(x=>x.draw),counts.draw);if(terms.length)section('Explain · Draw and Label','<p>Make a clear drawing and label all relevant parts.</p>'+terms.map((t,i)=>'<div class="q">'+(i+1)+'. '+esc(level==='HONORS'?honorsTask(t,'draw'):t.draw)+'<div class="draw"></div></div>').join(''),terms.map((t,i)=>(i+1)+'. '+math(t.draw)+' — one acceptable representation: '+math(t.example)).join('<br>'));else notes.push('No diagram-compatible terms are selected.')}
if(allowed.includes('example')&&counts.example){let terms=fit(vocab,counts.example);section('Apply · Create and Justify','<p>Create a mathematically correct example. Then explain why it fits the term.</p>'+terms.map((t,i)=>'<div class="q">'+(i+1)+'. '+esc(level==='HONORS'?honorsTask(t,'example'):t.term+': Write your own example and justify it.')+'<div class="answerline"></div><div class="answerline"></div><div class="answerline"></div>'+(level==='HONORS'?'<div class="answerline"></div><div class="answerline"></div>':'')+'</div>').join(''),terms.map((t,i)=>(i+1)+'. Sample: '+math(t.example)+' — '+math(t.definition)+' (other valid answers accepted)').join('<br><br>'))}
if(allowed.includes('cross')&&counts.cross){
 let pool=crossVocabulary(),n=Math.min(counts.cross,pool.length),x=null,chosen=[];
 // Try several vocabulary combinations rather than failing because one random subset doesn't interlock.
 for(let attempt=0;attempt<4&&n>=2;attempt++){
   let terms=fit(pool,n),candidate=crossword(terms);
   if(candidate){x=candidate;chosen=terms;break;}
   if(attempt===3&&n>2){n--;attempt=-1;}
 }
 if(x)section('Recognize · Crossword','<p>Complete the grid using the Across and Down definitions. Spaces and punctuation are omitted.</p>'+crossHtml(x,false),crossHtml(x,true));
 else notes.push('Crossword needs at least two compatible words. Select more units, or change the terms and regenerate.');
}
key+='</div>';if(!made){$('status').textContent='Choose at least one activity available at this mastery level.';return}last={h,key};$('preview').innerHTML=h+key;$('status').textContent='Generated '+made+' sections with '+vocab.length+' selected terms. '+notes.join(' ');document.body.classList.remove('print-key')}
types.forEach(([id,name,n])=>{$('formats').insertAdjacentHTML('beforeend','<div class="section"><label><input type="checkbox" id="use_'+id+'" checked> Include '+name+'</label><label for="f_'+id+'">Questions / terms</label><input style="width:80px" id="f_'+id+'" type="number" min="0" max="20" value="'+n+'"></div>');$('use_'+id).onchange=()=>{$('f_'+id).disabled=!$('use_'+id).checked;render()};$('f_'+id).onchange=render});
$('course').innerHTML=catalog.map(x=>'<option>'+esc(x.course)+'</option>').join('');$('course').onchange=()=>{$('crossUnits').innerHTML='';loadUnits()};$('unit').onchange=()=>{history.replaceState(null,'',location.pathname+'?unit='+encodeURIComponent($('unit').value));loadTerms();loadCrossUnits()};let requested=requestedUnit(),found=requested&&catalog.find(c=>c.units.some(u=>u[0]===requested));if(found)$('course').value=found.course;else if(catalog.some(c=>c.course==='Algebra 1'))$('course').value='Algebra 1';if(requested&&!found)$('status').textContent='No vocabulary bank is available for '+requested+'.';loadUnits();
$('crossAll').onclick=()=>{$('crossUnits').querySelectorAll('input').forEach(x=>x.checked=true);updateCrossCount()};
$('crossNone').onclick=()=>{$('crossUnits').querySelectorAll('input').forEach(x=>x.checked=false);updateCrossCount()};
$('custom').addEventListener('input',updateCrossCount);
$('allTerms').onclick=()=>{$('terms').querySelectorAll('input').forEach(x=>x.checked=true);selected=Array.from($('terms').querySelectorAll('input')).map(x=>x.dataset.id)};
$('noTerms').onclick=()=>{$('terms').querySelectorAll('input').forEach(x=>x.checked=false);selected=[]};
$('generate').onclick=render;$('reshuffle').onclick=render;$('print').onclick=()=>{if(!last)render();if(!last)return;document.body.classList.remove('print-key');window.print()};
$('keyPrint').onclick=()=>{if(!last)render();if(!last)return;document.body.classList.add('print-key');window.print();document.body.classList.remove('print-key')};
render();
})();