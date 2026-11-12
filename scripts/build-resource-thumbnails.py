"""Distinct, unit-specific previews following the established Classroom SVG style.
Keep cheat-sheet contact sheets: they show the actual two PDF pages.
"""
from pathlib import Path
import json,html,textwrap
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'thumbs/financial-algebra';OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'financial/resources.json').read_text())
INK='#17213a'
PALETTE={'lesson':('#7145ac','#f0eafa'),'worksheet':('#286999','#e7f2fb'),'assessment':('#ad3d55','#fbeaf0'),'practice':('#14786d','#e4f5ef'),'flashcards':('#b46a18','#fff1d9'),'lab':('#3657b6','#e9eeff'),'guide':('#53637d','#edf1f7'),'project':('#277a57','#e8f4e9')}
LABELS={'lesson':'Lesson Plan','worksheet':'Worksheet','assessment':'Assessment','practice':'Understanding Check','flashcards':'Flashcards','lab':'Decision Lab','guide':'Teacher Guide','project':'Unit Project'}
TOPICS={
'income':('PAYCHECK','$20 × 40 hours = $800','Hourly pay','Salary','Compare job offers'),
'budgeting':('MONTHLY BUDGET','$2,800 − $2,350 = $450','Needs','Wants','Build a spending plan'),
'banking':('SAVINGS ACCOUNT','$1,000 × 0.04 = $40','Account A','Account B','Compare banking costs'),
'credit':('CREDIT CARD','$600 × 0.02 = $12','Minimum payment','Larger payment','Choose a payoff strategy'),
'borrowing':('AUTO LOAN','$420 × 60 = $25,200','Shorter loan','Longer loan','Compare total loan costs'),
'investing':('COMPOUND GROWTH','$1,000 × 1.07 = $1,070','Start now','Start later','Explore saving over time'),
'housing':('HOUSING COSTS','$1,600 + $200 = $1,800','Rent','Buy','Compare housing choices'),
'insurance':('INSURANCE CLAIM','$8,000 − $1,000 = $7,000','Lower premium','Lower deductible','Choose a health plan'),
'college':('COLLEGE COSTS','$12,000 + $8,000 = $20,000','Pathway A','Pathway B','Compare education paths'),
'retirement':('PURCHASING POWER','$100 × 1.03 = $103','Save today','Save later','Plan for your future')}
def txt(x,y,v,size=20,c=INK,b=False,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{700 if b else 400}" text-anchor="{anchor}" fill="{c}">{html.escape(str(v))}</text>'
def box(x,y,w,h,f='white',c='#b9c7d7',r=12):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" stroke="{c}" stroke-width="2"/>'
def path(d,c=INK,w=4,f='none'):
 return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{f}" stroke-linecap="round" stroke-linejoin="round"/>'
def wrap(v,x,y,width=30,size=20,c=INK,b=False,n=3):
 return ''.join(txt(x,y+i*(size+7),s,size,c,b) for i,s in enumerate(textwrap.wrap(v,width)[:n]))
def check(x,y,c):return path(f'M{x} {y}l10 11 23-27',c,6)
def badge(x,y,w,v,c):return box(x,y,w,31,c,c,7)+txt(x+w/2,y+21,v,13,'white',True,'middle')
def scene(uid,c):
 if uid=='income':return box(12,38,126,87,'white',c)+path('M52 38V22h46v16M12 70h126M68 65v17h16V65',c,5)+txt(76,112,'$',32,c,True,'middle')
 if uid=='budgeting':return f'<circle cx="75" cy="76" r="58" fill="white" stroke="{c}" stroke-width="4"/>'+path('M75 18V76L125 106A58 58 0 0 0 75 18',c,3,c)+path('M75 76L28 111',c)+txt(75,153,'PLAN • SPEND • SAVE',11,c,True,'middle')
 if uid=='banking':return path('M10 44L75 12 140 44Z',c,4,'white')+path('M17 50h116M12 127h126M8 140h134',c,6)+''.join(path(f'M{x} 60v55',c,10) for x in [32,75,118])+txt(75,43,'$',22,c,True,'middle')
 if uid=='credit':return box(8,32,137,88,'white',c)+box(8,53,137,19,c,c,0)+box(23,83,26,18,'#ffdb74',c,4)+path('M65 100h60M23 135h102',c)
 if uid=='borrowing':return path('M15 85L30 51h87l20 34v36H15Z',c,4,'white')+path('M38 59L28 85h95l-14-26M76 59v26',c)+''.join(f'<circle cx="{x}" cy="121" r="16" fill="{c}"/>' for x in [38,114])+path('M23 102h15M116 102h14',c,5)
 if uid=='investing':return path('M15 17v116h128',c)+''.join(box(29+j*32,113-h,22,h,c,c,3) for j,h in enumerate([27,49,77]))+path('M22 92L59 68 92 57 133 16M111 18l22-2-3 23',c,5)
 if uid=='housing':return path('M7 70L76 12 145 70M23 60v80h105V60',c,5,'white')+box(66,94,30,46,'#e1ebf7',c,2)+box(37,77,20,22,'#ffdf84',c,2)+path('M111 38V18h17v35',c,5)
 if uid=='insurance':return path('M75 10L131 30v49c0 28-23 49-56 66-33-17-56-38-56-66V30Z',c,5,'white')+path('M48 77l21 22 39-48',c,10)
 if uid=='college':return path('M4 51L74 18 145 51 74 84Z',c,4,c)+path('M30 68v38q44 31 88 0V68M140 54v58',c,5)+box(132,111,16,24,'#ffda69',c,3)+path('M29 136h92',c,5)
 return box(20,27,112,106,'white',c)+path('M20 55h112M44 15v25M108 15v25',c,6)+txt(76,108,'2035',26,c,True,'middle')+path('M5 148h143',c)
def preview(u,kind,bank,p=None):
 uid=u['unitId'];c,bg=PALETTE[kind];topic,calc,a,b,q=TOPICS[uid]
 s=box(0,0,720,450,bg,bg,0)+box(0,0,720,101,c,c,0)+txt(30,46,LABELS[kind],32,'white',True)+txt(31,80,f"UNIT {u['unitNum']}  /  {u['name']}",18,'white')
 if kind=='lesson':
  s+=box(25,124,440,298)+txt(47,158,'TODAY’S LEARNING',17,c,True)
  for j,(label,sub) in enumerate([('Explore',u['skills'][0]['name']),('Model',calc),('Apply',q)]):
   y=194+j*77;s+=f'<circle cx="61" cy="{y}" r="17" fill="{c}"/>'+txt(61,y+6,j+1,18,'white',True,'middle')+txt(94,y+3,label,21,c,True)+wrap(sub,94,y+29,36,15,n=2)
  s+=f'<g transform="translate(512 150)">{scene(uid,c)}</g>'+badge(493,347,195,'TEACH • MODEL • TRY',c)
 elif kind=='worksheet':
  s+=box(28,121,449,306)+txt(48,158,'Name: ____________________',17)+path('M48 173h407','#c0cfdd',2)+txt(49,205,'1. Calculate and explain.',19,c,True)+txt(69,245,calc,23)+path('M69 274h359M69 296h359','#bdcddd',2)+txt(49,331,'2. Compare two choices.',19,c,True)+path('M69 361h359M69 388h359','#bdcddd',2)+f'<g transform="translate(520 148)">{scene(uid,c)}</g>'+badge(504,350,181,'PRACTICE + KEY',c)
 elif kind=='assessment':
  s+=box(55,126,397,296,'white',c)+box(163,115,178,29,'#e1e7f0',c,7)+txt(82,180,'SHOW WHAT YOU KNOW',19,c,True)+txt(82,216,topic,15)
  for j,label in enumerate(['A','B','C','D']):
   y=250+j*31;s+=f'<circle cx="97" cy="{y}" r="10" fill="{c if j==1 else "white"}" stroke="{c}" stroke-width="2"/>'+txt(97,y+4,label,11,'white' if j==1 else c,True,'middle')+path(f'M122 {y}h{210-j*18}','#b8c3d3',3)
  s+=f'<g transform="translate(510 154)">{scene(uid,c)}</g>'+badge(491,349,198,'REASON • JUSTIFY',c)
 elif kind=='flashcards':
  v=bank['vocab'][0];s+='<g transform="rotate(-9 256 265)">'+box(53,150,356,224,'#f3d7aa',c)+txt(80,190,'FINANCIAL VOCABULARY',14,c,True)+'</g>'
  s+='<g transform="rotate(5 395 284)">'+box(215,169,452,240,'white',c)+txt(242,203,'THINK → FLIP → REMEMBER',14,c,True)+wrap(v['term'],243,247,27,26,c,True,2)+wrap(v['def'],243,318,45,15,n=3)+'</g>'+f'<g transform="translate(34 270) scale(.72)">{scene(uid,c)}</g>'
 elif kind=='practice':
  s+=box(30,124,307,291)+txt(53,165,'TRY IT',23,c,True)+wrap(q,53,207,21,24,b=True,n=2)
  for j in range(3):s+=f'<circle cx="66" cy="{300+j*35}" r="11" fill="white" stroke="{c}" stroke-width="2"/>'+path(f'M88 {300+j*35}h185','#bfcccf',3)
  s+=path('M349 260h34m-12-12 12 12-12 12',c,6)+box(395,124,295,291,'#f9fffc',c)+check(428,169,c)+txt(474,181,'FEEDBACK',22,c,True)+wrap(calc,418,226,22,20,b=True,n=2)+txt(418,296,'Read the explanation.',17)+txt(418,327,'Find your next step.',17)+badge(416,356,249,'REFLECT • REVIEW • RETRY',c)
 elif kind=='lab':
  s+=txt(32,142,q,26,c,True)
  for x,label,k in [(30,a,0),(397,b,1)]:
   s+=box(x,166,292,185,'white',c)+wrap(label,x+18,199,23,20,c,True,n=2)
   for j,w in enumerate(([216,140,183] if k==0 else [150,218,118])):s+=box(x+18,237+j*30,w,13,c if j==k else '#d8e2ff',c,3)
  s+=txt(359,274,'VS',23,c,True,'middle')+f'<g transform="translate(302 335) scale(.61)">{scene(uid,c)}</g>'+txt(40,405,'COST',17,c,True)+txt(164,405,'RISK',17,c,True)+txt(487,405,'FLEXIBILITY',17,c,True)
 elif kind=='guide':
  s+=box(32,127,407,291)+txt(56,165,'DISCUSSION NOTES',21,c,True)
  for j,(label,sub) in enumerate([('Ask','What assumptions matter?'),('Listen','How can students justify a choice?'),('Connect',u['skills'][0]['name'])]):
   y=207+j*77;s+=check(54,y-5,c)+txt(101,y,label,20,c,True)+wrap(sub,101,y+26,35,15,n=2)
  s+=f'<g transform="translate(522 146)">{scene(uid,c)}</g>'+badge(486,346,208,'PROMPTS + REASONING',c)
 else:
  s+=f'<g transform="translate(45 160) scale(1.5)">{scene(uid,c)}</g>'+wrap(p['title'].replace('Capstone: ',''),316,164,24,27,c,True,n=3)+wrap(p['grouping']+' · '+p['days'],318,273,33,16,n=2)+badge(318,337,343,'INVESTIGATE → DECIDE → PRESENT',c)+txt(318,400,topic,16,c,True)
 return '<svg xmlns="http://www.w3.org/2000/svg" width="720" height="450" viewBox="0 0 720 450" role="img" aria-label="'+html.escape(LABELS[kind]+' preview: '+(p['title'] if p else u['name']),quote=True)+'">'+s+'</svg>'
count=0
for u in manifest['units']:
 uid=u['unitId'];bank=json.loads((ROOT/f'financial/banks/{uid}.json').read_text())
 for kind in LABELS:
  if kind=='project':continue
  (OUT/f'{uid}-{kind}.svg').write_text(preview(u,kind,bank));count+=1
 for p in u['resources']['projects']:
  (OUT/f"{uid}-project-{p['slug']}.svg").write_text(preview(u,'project',bank,p));count+=1
print(f'Built {count} distinct activity and project previews; kept actual PDF thumbnails.')
