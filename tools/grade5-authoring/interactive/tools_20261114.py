"""Two more Grade 5 Interactive Math tools (2026-11-14) for the units that had none:
  math5-line-plot-fair-share   (Data, Line Plots, and Problem Solving: 5.MD.B.2)
  math5-quadrilateral-family   (Geometry and Classifying Shapes: 5.G.B.3, 5.G.B.4)
Same page shell as the published math5-* tools (copied from math5-volume-builder/index.html), same TOOL challenge API.
Writes math5-<slug>/index.html at the repository root, plus Explore & Reflect worksheet/key HTML and print jobs.
Usage: python3 tools/grade5-authoring/interactive/tools_20261114.py /tmp/g5new && node tools/grade5-authoring/print/print.cjs /tmp/g5new/jobs.json"""
import html, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
TMP = sys.argv[1] if len(sys.argv) > 1 else "/tmp/g5new"
os.makedirs(TMP, exist_ok=True)
ref = open(os.path.join(ROOT, "math5-volume-builder", "index.html"), encoding="utf-8").read()
HEAD = ref[:ref.index("<main")]
SCRIPTS = re.search(r'(<script src="\.\./worksheet-generator/grade5/g5-figs\.js[^<]*</script><script src="[^"]*tool-shell\.js[^"]*"></script>)', ref).group(1)

TOOLS = []


def tool(slug, title, desc, intro, body, script, worksheet):
    TOOLS.append(dict(slug="math5-" + slug, title=title, description=desc, intro=intro, body=body, script=script, worksheet=worksheet))


tool("line-plot-fair-share", "Line Plot Fair Share",
     "Make a line plot of measurements in eighths, find the total, and share it equally to find the fair share (the mean). See how one new value changes the fair share.",
     "Each ✕ is one jar of water. Use + and − to add or remove jars at each amount (in liters). Then look at the total and the fair share.",
     """<div class="g5-row" id="lpRows" style="justify-content:center;gap:.25rem"></div>
<div class="ts-model" id="lpPlot"></div><div class="ts-out" id="lpOut" aria-live="polite"></div>
<div class="g5-actions" style="justify-content:center"><button class="g5-btn alt" id="lpClear">Clear</button></div>""",
     r"""
var T=[1,2,3,4,5,6,7,8],c={},made={},live=false;function lab(n){var g=TOOL.gcd(n,8);return n===8?'1':(n/g)+'/'+(8/g);}
function reset(){T.forEach(function(t){c[t]=0});c[2]=1;c[4]=2;c[6]=1;made={};live=false;draw();}
function fr(n,d){if(n===0)return '0';return TOOL.mixed(n,d);}
function draw(){
 TOOL.$('lpRows').innerHTML=T.map(function(t){return '<div class="ts-step" style="flex-direction:column"><button aria-label="Add a jar at '+lab(t)+' liter" data-t="'+t+'" data-s="1">+</button><span style="font-weight:800">'+c[t]+'</span><button aria-label="Remove a jar at '+lab(t)+' liter" data-t="'+t+'" data-s="-1">−</button><span class="g5-note" style="font-size:.75rem">'+TOOL.mixed(t,8)+'</span></div>';}).join('');
 Array.prototype.forEach.call(document.querySelectorAll('#lpRows button'),function(b){b.onclick=function(){var t=+b.dataset.t;c[t]=Math.max(0,Math.min(6,c[t]+(+b.dataset.s)));live=true;draw();}});
 TOOL.$('lpClear').onclick=function(){T.forEach(function(t){c[t]=0});live=true;draw();};
 TOOL.$('lpPlot').innerHTML=G5FIGS.lineplot(['0'].concat(T.map(lab)),[0].concat(T.map(function(t){return c[t]})),{xlabel:'Water in each jar (liters)',title:'Line plot of the jars'});
 var n=0,tot=0,lo=null,hi=null;T.forEach(function(t){n+=c[t];tot+=t*c[t];if(c[t]){if(lo===null)lo=t;hi=t;}});
 var out=n?('Jars: <b>'+n+'</b> · Total: <b>'+fr(tot,8)+' L</b>'+' · Fair share (total ÷ '+n+'): <b>'+TOOL.mixed(tot,8*n)+' L</b>'+'<br>Greatest − least: '+fr(hi-lo,8)+' L'):'No jars yet. Use + to add some.';
 TOOL.$('lpOut').innerHTML=out;
 if(n&&live)made[T.map(function(t){return c[t]}).join(',')]={n:n,tot:tot};
 if(live)TOOL.update(O,{n:n,tot:tot,share:n?tot/(8*n):null,range:n?hi-lo:null,c:c,made:made});}
var O={title:'Line Plot Fair Share',reset:reset,challenges:[
 {text:'Make a line plot of 6 jars with a total of exactly 3 liters.',test:function(s){return s.n===6&&s.tot===24}},
 {text:'Make the fair share exactly 1/2 liter with jars that are NOT all 1/2 liter.',test:function(s){return s.n>1&&s.share===0.5&&s.c[4]!==s.n}},
 {text:'Make the greatest amount minus the least amount equal 5/8 liter.',test:function(s){return s.range===5}},
 {text:'Make 4 jars whose fair share is 3/4 liter.',test:function(s){return s.n===4&&s.tot===24}},
 {text:'Add one jar so that the fair share goes UP. Then remove it.',test:function(s){var k=Object.keys(s.made).map(function(x){return s.made[x]});return k.some(function(a){return k.some(function(b){return b.n===a.n+1&&b.tot*a.n>a.tot*b.n})})}}],
 teacher:['5.MD.B.2: make a line plot of measurements in fractions of a unit (1/2, 1/4, 1/8) and redistribute the total equally.','The fair share is total ÷ number of jars: the mean, without the word.','Ask: which jars give water away and which receive it when the water is shared equally?'],
 notice:['The total is the sum of every ✕: count each amount as many times as it has ✕ marks.','The fair share is the total divided by the number of jars.','A new jar above the fair share raises it; a new jar below it lowers it.','The fair share is always between the least and the greatest amount.']};
TOOL.init(O);reset();""",
     [("Start with the line plot shown when the tool opens. How many jars are there? What is the total?", "4 jars; total 2 liters (1/4 + 1/2 + 1/2 + 3/4)"),
      ("What is the fair share for that line plot?", "1/2 liter (2 ÷ 4)"),
      ("Make 5 jars: 1/8, 3/8, 3/8, 5/8, 7/8. What is the total?", "19/8 = 2 3/8 liters"),
      ("What is the greatest amount minus the least amount for those 5 jars?", "3/4 liter (7/8 − 1/8)"),
      ("Make 6 jars with a total of 3 liters. Write your 6 amounts.", "Example: 1/2, 1/2, 1/2, 1/2, 1/2, 1/2 (any six amounts that add to 3)"),
      ("For 6 jars that total 3 liters, what is the fair share?", "1/2 liter"),
      ("A line plot has 4 jars: 1/4, 1/4, 3/4, 3/4. Add a jar of 1 liter. Does the fair share go up or down? What is the new fair share?", "Up: 3 liters ÷ 5 = 3/5 liter (it was 1/2)."),
      ("Reflect: Explain how to find the fair share from a line plot.", "Add every amount shown by an ✕ to get the total, then divide by the number of ✕ marks.")])

tool("quadrilateral-family", "Quadrilateral Family",
     "Change the bottom side, top side, height and slant of a four-sided figure. Watch which names fit: trapezoid, parallelogram, rectangle, rhombus, square.",
     "Use the + and − buttons. The checklist shows every name the shape has right now, and why.",
     """<div class="g5-row" id="qfCtl" style="justify-content:center;gap:.6rem"></div>
<div class="ts-model" id="qfShape"></div><div class="ts-out" id="qfOut" aria-live="polite"></div>""",
     r"""
var K=[['B','Bottom side',2,8],['T','Top side',1,8],['H','Height',2,6],['S','Slant',-3,3]],v={},seen={},live=false;
function reset(){v={B:6,T:3,H:4,S:1};seen={};live=false;draw();}
function props(){var B=v.B,T=v.T,H=v.H,S=v.S,tl=S,tr=S+T;
 /* corners: (0,0) (B,0) (tr,H) (tl,H); the top is always parallel to the bottom */
 var left=Math.sqrt(tl*tl+H*H),right=Math.sqrt((tr-B)*(tr-B)+H*H);
 var par2=T===B&&true,right4=par2&&S===0,eq4=par2&&Math.abs(left-B)<1e-9;
 var leftEq=Math.abs(left-right)<1e-9;
 return {pairs:par2?2:1,right4:right4,eq4:eq4,square:right4&&eq4,rect:right4,rhombus:eq4,para:par2,trap:true,left:left,right:right,iso:!par2&&leftEq};}
function draw(){
 TOOL.$('qfCtl').innerHTML=K.map(function(k){return '<div class="ts-step" style="flex-direction:column"><span class="g5-note">'+k[1]+'</span><div class="ts-step"><button aria-label="Decrease '+k[1]+'" data-k="'+k[0]+'" data-s="-1">−</button><b style="min-width:2ch;text-align:center">'+v[k[0]]+'</b><button aria-label="Increase '+k[1]+'" data-k="'+k[0]+'" data-s="1">+</button></div></div>';}).join('');
 Array.prototype.forEach.call(document.querySelectorAll('#qfCtl button'),function(b){b.onclick=function(){var k=K.filter(function(q){return q[0]===b.dataset.k})[0];v[k[0]]=Math.max(k[2],Math.min(k[3],v[k[0]]+(+b.dataset.s)));live=true;draw();}});
 var p=props(),sc=40,ox=30+Math.max(0,-v.S)*sc,W=Math.max(v.B,v.S+v.T)*sc+ox+30,Hh=v.H*sc+60;
 var pts=[[0,0],[v.B,0],[v.S+v.T,v.H],[v.S,v.H]].map(function(q){return (ox+q[0]*sc)+','+(Hh-30-q[1]*sc)}).join(' ');
 var g='';for(var x=0;x<=W;x+=sc)g+='<line x1="'+x+'" y1="0" x2="'+x+'" y2="'+Hh+'" stroke="#E2E8F0"/>';for(var y=Hh-30;y>=0;y-=sc)g+='<line x1="0" y1="'+y+'" x2="'+W+'" y2="'+y+'" stroke="#E2E8F0"/>';
 TOOL.$('qfShape').innerHTML='<svg viewBox="0 0 '+W+' '+Hh+'" role="img" aria-label="Quadrilateral on a grid">'+g+'<polygon points="'+pts+'" fill="#C4B5FD" fill-opacity=".55" stroke="#5B21B6" stroke-width="4" stroke-linejoin="round"/></svg>';
 var rows=[['Quadrilateral',true,'4 straight sides'],['Trapezoid',p.trap,'at least one pair of parallel sides (top and bottom)'],['Parallelogram',p.para,p.para?'2 pairs of parallel sides':'top and bottom are different lengths, so the slanted sides are not parallel'],
  ['Rectangle',p.rect,p.rect?'a parallelogram with 4 right angles':(p.para?'the angles are not right angles':'not a parallelogram')],['Rhombus',p.rhombus,p.rhombus?'a parallelogram with 4 equal sides':'the sides are not all equal'],['Square',p.square,p.square?'a rectangle AND a rhombus':'needs 4 right angles and 4 equal sides']];
 TOOL.$('qfOut').innerHTML=rows.map(function(r){return (r[1]?'✅ <b>':'⬜ ')+r[0]+(r[1]?'</b>':'')+' — '+r[2]}).join('<br>')+'<br><span class="g5-note">Side lengths: bottom '+v.B+', top '+v.T+', left '+(Math.round(p.left*100)/100)+', right '+(Math.round(p.right*100)/100)+'</span>';
 if(live){if(p.rect&&!p.square)seen.rectNotSq=1;if(p.rhombus&&!p.square)seen.rhNotSq=1;if(!p.para)seen.trapOnly=1;if(p.square)seen.square=1;if(p.para&&!p.rect&&!p.rhombus)seen.paraOnly=1;}
 TOOL.update(O,{seen:seen});}
var O={title:'Quadrilateral Family',reset:reset,challenges:[
 {text:'Make a trapezoid that is not a parallelogram.',test:function(s){return s.seen.trapOnly}},
 {text:'Make a parallelogram that is not a rectangle and not a rhombus.',test:function(s){return s.seen.paraOnly}},
 {text:'Make a rectangle that is not a square.',test:function(s){return s.seen.rectNotSq}},
 {text:'Make a square. Which names does it have?',test:function(s){return s.seen.square}},
 {text:'Make a rhombus that is not a square. (Hint: try bottom 5, height 4.)',test:function(s){return s.seen.rhNotSq}}],
 teacher:['5.G.B.3–4: attributes of a category belong to every subcategory; classify in a hierarchy.','This tool uses the inclusive definition: a trapezoid has at least one pair of parallel sides, so every parallelogram is a trapezoid. Some programs use “exactly one pair”; tell students which definition your class uses.','The 3-4-5 right triangle makes the rhombus challenge possible with whole-number moves (slant 3, height 4, sides 5).'],
 notice:['Every square is a rectangle and a rhombus, but not every rectangle or rhombus is a square.','Every rectangle and every rhombus is a parallelogram.','A shape keeps all the names of the families above it.','Changing the slant changes the angles but not the parallel sides.']};
TOOL.init(O);reset();""",
     [("When the tool opens, which names does the shape have?", "Quadrilateral and trapezoid"),
      ("What must be true about the top and bottom sides for the shape to be a parallelogram?", "They must be the same length (so both pairs of sides are parallel)."),
      ("Make bottom 6, top 6, height 4, slant 0. Which names fit?", "Quadrilateral, trapezoid, parallelogram, rectangle"),
      ("Change the height to 6. Which new name appears? Why?", "Square (and rhombus): all four sides are 6 and all angles are right angles."),
      ("Make bottom 5, top 5, height 4, slant 3. What are the side lengths? Which names fit?", "All four sides are 5. Quadrilateral, trapezoid, parallelogram, rhombus (not rectangle)."),
      ("True or false: every rectangle is a square. Explain.", "False. A rectangle needs only 4 right angles; its sides do not have to be equal."),
      ("True or false: every square is a rhombus. Explain.", "True. A square has 4 equal sides and 2 pairs of parallel sides, so it is a rhombus."),
      ("Reflect: Draw or describe the family tree from quadrilateral down to square.", "Quadrilateral → trapezoid → parallelogram → rectangle and rhombus → square (a square is both).")])

# ------------------------------------------------------------------ write pages, worksheets and print jobs
FOOT = "</script></body></html>\n"
for t in TOOLS:
    d = os.path.join(ROOT, t["slug"])
    os.makedirs(d, exist_ok=True)
    head = re.sub(r"<title>[^<]*</title>", f"<title>{html.escape(t['title'])} · 5th Grade Math | Mr. K's Classroom</title>", HEAD)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(t["description"])}">', head)
    page = (head + f'<main class="g5"><div class="ts-grid"><section class="g5-card" id="tool"><h1>{html.escape(t["title"])}</h1><p class="g5-sub">{html.escape(t["intro"])}</p>{t["body"]}</section>\n'
            '<aside><section class="g5-card" id="challenges"></section><section class="g5-card" id="notice"></section></aside></div></main>\n' + SCRIPTS + "\n<script>\n" + t["script"] + "\n" + FOOT)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)

sys.path.insert(0, os.path.dirname(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location("ws", os.path.join(os.path.dirname(__file__), "worksheets.py"))
src = open(os.path.join(os.path.dirname(__file__), "worksheets.py"), encoding="utf-8").read()
ns = {"__name__": "ws_lib", "__file__": os.path.join(os.path.dirname(__file__), "worksheets.py")}
exec(src.split("jobs = []")[0], ns)  # CSS, fx() and page() from the published worksheet builder
jobs = []
for t in TOOLS:
    qs = t["worksheet"]
    first, second = qs[:5], qs[5:]
    def block(items, key, start):
        return "".join(f'<div class="q"><b>{start + i + 1}.</b> {ns["fx"](q)}</div>' + (f'<div class="ans">{ns["fx"](a)}</div>' if key else '<div class="ln"></div><div class="ln"></div>') for i, (q, a) in enumerate(items))
    for key in (False, True):
        p1 = ns["page"](t, f'<div class="box"><h2>Get started</h2><div style="font-size:10.5pt">{html.escape(t["description"])} Open the tool and use it to answer each question.</div></div><div class="box"><h2>Explore</h2>{block(first, key, 0)}</div>', key)
        p2 = ns["page"](t, f'<div class="box"><h2>Explore more</h2>{block(second[:-1], key, len(first))}</div><div class="box" style="border-color:#059669"><h2 style="color:#059669">Reflect</h2>{block(second[-1:], key, len(qs) - 1)}' +
                        ('' if key else '<div class="ln"></div><div class="ln"></div>') + '</div>' + ('<div class="box" style="border-color:#EA7A12"><h2 style="color:#EA7A12">Teacher notes</h2><div style="font-size:10.5pt">Accept equivalent forms (for example 1/2 = 2/4 = 0.5) and any correct example where several answers are possible. Have students explain using the tool’s picture.</div></div>' if key else ''), key)
        f = os.path.join(TMP, f'{t["slug"]}-{"key" if key else "ws"}.html')
        open(f, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset=utf-8><style>{ns['CSS']}</style></head><body>{p1}{p2}</body></html>")
        jobs.append({"html": f, "pdf": os.path.join(ROOT, t["slug"], "teacher-key.pdf" if key else "worksheet.pdf")})
    jobs.append({"url": f"http://localhost:8767/{t['slug']}/index.html", "jpg": os.path.join(ROOT, "thumbs", t["slug"] + ".jpg"), "w": 1200, "h": 750, "wait": 500})
json.dump(jobs, open(os.path.join(TMP, "jobs.json"), "w"))
print(len(TOOLS), "tools,", len(jobs), "print jobs →", os.path.join(TMP, "jobs.json"))
